export function mean(xs: number[]): number {
  if (xs.length === 0) return 0;
  return xs.reduce((a, b) => a + b, 0) / xs.length;
}

export function variance(xs: number[]): number {
  if (xs.length < 2) return 0;
  const m = mean(xs);
  return xs.reduce((acc, x) => acc + (x - m) ** 2, 0) / (xs.length - 1);
}

export function stdev(xs: number[]): number {
  return Math.sqrt(variance(xs));
}

export function covariance(xs: number[], ys: number[]): number {
  const n = Math.min(xs.length, ys.length);
  if (n < 2) return 0;
  const mx = mean(xs.slice(0, n));
  const my = mean(ys.slice(0, n));
  let s = 0;
  for (let i = 0; i < n; i++) s += (xs[i] - mx) * (ys[i] - my);
  return s / (n - 1);
}

export function covMatrix(returnsList: number[][]): number[][] {
  const n = returnsList.length;
  const C: number[][] = Array.from({ length: n }, () => Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    for (let j = i; j < n; j++) {
      const c = covariance(returnsList[i], returnsList[j]);
      C[i][j] = c;
      C[j][i] = c;
    }
  }
  return C;
}

export function portfolioVariance(weights: number[], cov: number[][]): number {
  let v = 0;
  for (let i = 0; i < weights.length; i++) {
    for (let j = 0; j < weights.length; j++) {
      v += weights[i] * weights[j] * cov[i][j];
    }
  }
  return Math.max(0, v);
}

export function portfolioReturn(weights: number[], means: number[]): number {
  return weights.reduce((s, w, i) => s + w * means[i], 0);
}

/** Annualize monthly mean/vol for display */
export function annualizeReturn(monthly: number): number {
  return (1 + monthly) ** 12 - 1;
}

export function annualizeVol(monthlyStd: number): number {
  return monthlyStd * Math.sqrt(12);
}

export function sharpeRatio(meanRet: number, vol: number, rf = 0): number {
  if (vol <= 1e-12) return 0;
  return (meanRet - rf) / vol;
}

export function normalizeWeights(ws: number[]): number[] {
  const clipped = ws.map((w) => Math.max(0, w));
  const s = clipped.reduce((a, b) => a + b, 0);
  if (s <= 1e-12) return clipped.map(() => 1 / clipped.length);
  return clipped.map((w) => w / s);
}
