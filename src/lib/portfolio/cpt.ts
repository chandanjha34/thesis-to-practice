import type { CptParams } from "./types";

/** Prelec / TK probability weighting */
function weight(p: number, exponent: number): number {
  const pClamped = Math.min(1, Math.max(0, p));
  if (pClamped === 0) return 0;
  if (pClamped === 1) return 1;
  const num = pClamped ** exponent;
  const den = (num + (1 - pClamped) ** exponent) ** (1 / exponent);
  return num / den;
}

/** Value function (Kahneman–Tversky power form) */
function value(x: number, params: CptParams): number {
  if (x >= 0) return x ** params.alpha;
  return -params.lambda * ((-x) ** params.beta);
}

/**
 * Discrete CPT value for an equally likely sample of outcomes
 * (asset monthly returns vs reference point).
 * Matches the behavioural scoring step used in the thesis pipeline.
 */
export function computeCptValue(returns: number[], params: CptParams): number {
  const prospects = returns.map((r) => r - params.reference);
  const n = prospects.length;
  if (n === 0) return 0;

  const sorted = [...prospects].sort((a, b) => a - b);
  const p = 1 / n;

  // Losses: outcomes ≤ 0, ranked ascending (most negative first in CPT indexing)
  const losses = sorted.filter((x) => x < 0);
  // Gains: outcomes ≥ 0, sorted ascending
  const gains = sorted.filter((x) => x >= 0);

  let cpt = 0;

  // Decision weights for losses (Tversky–Kahneman cumulative form)
  for (let i = 0; i < losses.length; i++) {
    const rankFromWorst = i + 1; // 1..L counting from most negative
    const F = rankFromWorst / n;
    const Fprev = i / n;
    const pi = weight(F, params.delta) - weight(Fprev, params.delta);
    cpt += pi * value(losses[i], params);
  }

  // Decision weights for gains (from best outcome downward in cumulative sense)
  for (let i = 0; i < gains.length; i++) {
    const betterOrEqual = gains.length - i; // count of outcomes ≥ this gain
    const strictlyBetter = gains.length - i - 1;
    const wCum = weight(betterOrEqual / n, params.gamma);
    const wPrev = weight(strictlyBetter / n, params.gamma);
    const pi = wCum - wPrev;
    cpt += pi * value(gains[i], params);
  }

  // Equal-probability fallback if rounding empties both (shouldn't happen)
  if (losses.length + gains.length === 0) {
    return prospects.reduce((s, x) => s + value(x, params) * p, 0);
  }

  return cpt;
}

/** CPT of a portfolio path (weighted combination of asset returns) */
export function portfolioCptValue(
  weights: number[],
  returnsList: number[][],
  params: CptParams,
): number {
  const T = returnsList[0]?.length ?? 0;
  const path: number[] = [];
  for (let t = 0; t < T; t++) {
    let r = 0;
    for (let i = 0; i < weights.length; i++) r += weights[i] * returnsList[i][t];
    path.push(r);
  }
  return computeCptValue(path, params);
}
