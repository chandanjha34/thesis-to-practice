import solver from "javascript-lp-solver";

export type DeaUnit = {
  id: string;
  /** Inputs (lower is better), e.g. variance */
  inputs: number[];
  /** Outputs (higher is better), e.g. CPT value, mean return */
  outputs: number[];
};

type LpModel = {
  optimize: string;
  opType: "max" | "min";
  constraints: Record<string, { max?: number; min?: number; equal?: number }>;
  variables: Record<string, Record<string, number>>;
};

/**
 * Input-oriented CCR DEA for one DMU.
 * Returns technical efficiency in [0, 1].
 */
export function ccrEfficiency(units: DeaUnit[], targetIndex: number): number {
  const target = units[targetIndex];
  const m = target.inputs.length;
  const s = target.outputs.length;

  const model: LpModel = {
    optimize: "efficiency",
    opType: "max",
    constraints: {},
    variables: {},
  };

  for (let i = 0; i < m; i++) {
    model.variables[`v${i}`] = { inNorm: target.inputs[i], [`v${i}`]: 1 };
    model.constraints[`v${i}`] = { min: 0 };
  }
  for (let r = 0; r < s; r++) {
    model.variables[`u${r}`] = {
      efficiency: Math.max(1e-9, target.outputs[r]),
      [`u${r}`]: 1,
    };
    model.constraints[`u${r}`] = { min: 0 };
  }

  model.constraints.inNorm = { equal: 1 };

  for (let k = 0; k < units.length; k++) {
    const cName = `dmu${k}`;
    model.constraints[cName] = { max: 0 };
    for (let r = 0; r < s; r++) {
      const key = `u${r}`;
      model.variables[key][cName] =
        (model.variables[key][cName] ?? 0) + units[k].outputs[r];
    }
    for (let i = 0; i < m; i++) {
      const key = `v${i}`;
      model.variables[key][cName] =
        (model.variables[key][cName] ?? 0) - units[k].inputs[i];
    }
  }

  try {
    const result = solver.Solve(model);
    if (!result.feasible) return 0;
    const eff = Number(result.efficiency ?? 0);
    return Math.min(1, Math.max(0, eff));
  } catch {
    const outSum = target.outputs.reduce((a, b) => a + Math.max(0, b), 0);
    const inSum = target.inputs.reduce((a, b) => a + Math.max(1e-9, b), 0);
    return outSum / inSum;
  }
}

/** Self-efficiency for every unit */
export function deaScores(units: DeaUnit[]): number[] {
  return units.map((_, i) => ccrEfficiency(units, i));
}

/**
 * Aggressive cross-efficiency: evaluate unit j with optimal weights of unit k,
 * then average over peers (Sexton / Doyle–Green style, as used with CPT in the thesis).
 */
export function crossEfficiencyScores(units: DeaUnit[]): number[] {
  const n = units.length;
  const self = deaScores(units);
  const matrix: number[][] = Array.from({ length: n }, () => Array(n).fill(0));

  for (let k = 0; k < n; k++) {
    const weights = recoverWeights(units, k);
    for (let j = 0; j < n; j++) {
      const num = weights.u.reduce(
        (s, ur, r) => s + ur * units[j].outputs[r],
        0,
      );
      const den = weights.v.reduce(
        (s, vi, i) => s + vi * Math.max(1e-12, units[j].inputs[i]),
        0,
      );
      matrix[k][j] = den > 0 ? num / den : 0;
    }
  }

  return units.map((_, j) => {
    let sum = self[j];
    for (let k = 0; k < n; k++) {
      if (k === j) continue;
      sum += matrix[k][j];
    }
    return sum / n;
  });
}

function recoverWeights(
  units: DeaUnit[],
  targetIndex: number,
): { v: number[]; u: number[] } {
  const target = units[targetIndex];
  const m = target.inputs.length;
  const s = target.outputs.length;

  const model: LpModel = {
    optimize: "efficiency",
    opType: "max",
    constraints: {},
    variables: {},
  };

  for (let i = 0; i < m; i++) {
    model.variables[`v${i}`] = { inNorm: target.inputs[i], [`v${i}`]: 1 };
    model.constraints[`v${i}`] = { min: 0 };
  }
  for (let r = 0; r < s; r++) {
    model.variables[`u${r}`] = {
      efficiency: Math.max(1e-9, target.outputs[r]),
      [`u${r}`]: 1,
    };
    model.constraints[`u${r}`] = { min: 0 };
  }
  model.constraints.inNorm = { equal: 1 };

  for (let k = 0; k < units.length; k++) {
    const cName = `dmu${k}`;
    model.constraints[cName] = { max: 0 };
    for (let r = 0; r < s; r++) {
      model.variables[`u${r}`][cName] =
        (model.variables[`u${r}`][cName] ?? 0) + units[k].outputs[r];
    }
    for (let i = 0; i < m; i++) {
      model.variables[`v${i}`][cName] =
        (model.variables[`v${i}`][cName] ?? 0) - units[k].inputs[i];
    }
  }

  try {
    const result = solver.Solve(model);
    const vRaw = Array.from({ length: m }, (_, i) =>
      Number(result[`v${i}`] ?? 0),
    );
    const uRaw = Array.from({ length: s }, (_, r) =>
      Number(result[`u${r}`] ?? 0),
    );
    const v =
      vRaw.reduce((a, b) => a + b, 0) === 0
        ? Array.from({ length: m }, (_, i) => (i === 0 ? 1 : 0))
        : vRaw;
    const u =
      uRaw.reduce((a, b) => a + b, 0) === 0
        ? Array.from({ length: s }, (_, i) => (i === 0 ? 1 : 0))
        : uRaw;
    return { v, u };
  } catch {
    return {
      v: Array.from({ length: m }, () => 1),
      u: Array.from({ length: s }, () => 1),
    };
  }
}
