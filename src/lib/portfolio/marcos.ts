/**
 * MARCOS (Measurement of Alternatives and Ranking according to COmpromise Solution)
 * used in the thesis to break DEA ties via ideal / anti-ideal benchmarking.
 *
 * criteria: higherIsBetter flags aligned with values columns
 */
export function marcosScores(
  values: number[][],
  higherIsBetter: boolean[],
): number[] {
  const n = values.length;
  if (n === 0) return [];
  const m = values[0].length;

  const ideal: number[] = [];
  const anti: number[] = [];
  for (let j = 0; j < m; j++) {
    const col = values.map((row) => row[j]);
    if (higherIsBetter[j]) {
      ideal.push(Math.max(...col));
      anti.push(Math.min(...col));
    } else {
      ideal.push(Math.min(...col));
      anti.push(Math.max(...col));
    }
  }

  // Normalize vs ideal
  const norm = values.map((row) =>
    row.map((v, j) => {
      if (higherIsBetter[j]) {
        return ideal[j] === 0 ? 0 : v / ideal[j];
      }
      return v === 0 ? 0 : ideal[j] / v;
    }),
  );

  const idealNorm = ideal.map((v, j) =>
    higherIsBetter[j] ? 1 : ideal[j] === 0 ? 0 : ideal[j] / ideal[j],
  );
  const antiNorm = anti.map((v, j) => {
    if (higherIsBetter[j]) return ideal[j] === 0 ? 0 : v / ideal[j];
    return v === 0 ? 0 : ideal[j] / v;
  });

  // Equal criterion weights for the demo
  const w = Array.from({ length: m }, () => 1 / m);

  const Si = norm.map((row) => row.reduce((s, v, j) => s + v * w[j], 0));
  const Sp = idealNorm.reduce((s, v, j) => s + v * w[j], 0);
  const Sm = antiNorm.reduce((s, v, j) => s + v * w[j], 0);

  return Si.map((si) => {
    const kpi = si / Math.max(1e-12, Sp);
    const kmi = si / Math.max(1e-12, Sm);
    const f = (kpi + kmi) / Math.max(1e-12, 1 + (1 - kpi) / Math.max(1e-12, kpi) + (1 - kmi) / Math.max(1e-12, kmi));
    // Utility degree style score in (0,1]
    return Math.min(1, Math.max(0, f));
  });
}
