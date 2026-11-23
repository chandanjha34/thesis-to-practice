import {
  covMatrix,
  normalizeWeights,
  portfolioReturn,
  portfolioVariance,
  mean,
} from "./stats";
import { portfolioCptValue } from "./cpt";
import type { CptParams } from "./types";

/** Equal-weight portfolio over selected indices */
export function equalWeight(n: number): number[] {
  return Array.from({ length: n }, () => 1 / n);
}

/**
 * Long-only mean-variance: scan target returns and minimize variance
 * via projected gradient on simplex (no external QP dependency).
 */
export function meanVarianceFrontier(
  returnsList: number[][],
  points = 12,
): { weights: number[]; risk: number; ret: number }[] {
  const n = returnsList.length;
  const means = returnsList.map(mean);
  const cov = covMatrix(returnsList);
  const minRet = Math.min(...means);
  const maxRet = Math.max(...means);
  const out: { weights: number[]; risk: number; ret: number }[] = [];

  for (let p = 0; p < points; p++) {
    const target = minRet + ((maxRet - minRet) * p) / Math.max(1, points - 1);
    const w = optimizeVarianceForReturn(means, cov, target);
    out.push({
      weights: w,
      risk: Math.sqrt(portfolioVariance(w, cov)),
      ret: portfolioReturn(w, means),
    });
  }
  return out;
}

function optimizeVarianceForReturn(
  means: number[],
  cov: number[][],
  target: number,
): number[] {
  const n = means.length;
  let w = equalWeight(n);

  for (let iter = 0; iter < 400; iter++) {
    // Gradient of w'Σw is 2 Σ w
    const grad = Array.from({ length: n }, (_, i) => {
      let g = 0;
      for (let j = 0; j < n; j++) g += 2 * cov[i][j] * w[j];
      return g;
    });

    const step = 0.15 / (1 + iter * 0.01);
    w = normalizeWeights(w.map((wi, i) => wi - step * grad[i]));

    // Soft pull toward target return
    const r = portfolioReturn(w, means);
    const pull = 0.08 * (target - r);
    w = normalizeWeights(w.map((wi, i) => wi + pull * (means[i] - r)));
  }
  return w;
}

/** Max-Sharpe (excess over 0) on the MV frontier sample */
export function maxSharpePortfolio(returnsList: number[][]): number[] {
  const frontier = meanVarianceFrontier(returnsList, 20);
  let best = frontier[0];
  let bestSharpe = -Infinity;
  for (const pt of frontier) {
    const sh = pt.risk > 1e-12 ? pt.ret / pt.risk : -Infinity;
    if (sh > bestSharpe) {
      bestSharpe = sh;
      best = pt;
    }
  }
  return best.weights;
}

/**
 * CPT-oriented portfolio: maximize portfolio CPT over random long-only
 * mixes of a candidate set (behavioral investor construction from the thesis).
 */
export function maximizeCptPortfolio(
  returnsList: number[][],
  params: CptParams,
  samples = 800,
): number[] {
  const n = returnsList.length;
  let bestW = equalWeight(n);
  let best = portfolioCptValue(bestW, returnsList, params);

  for (let s = 0; s < samples; s++) {
    const raw = Array.from({ length: n }, () => Math.random());
    const w = normalizeWeights(raw);
    const val = portfolioCptValue(w, returnsList, params);
    if (val > best) {
      best = val;
      bestW = w;
    }
  }

  // Local polish
  for (let iter = 0; iter < 200; iter++) {
    const i = Math.floor(Math.random() * n);
    const j = Math.floor(Math.random() * n);
    if (i === j) continue;
    const trial = [...bestW];
    const delta = (Math.random() - 0.5) * 0.08;
    trial[i] += delta;
    trial[j] -= delta;
    const w = normalizeWeights(trial);
    const val = portfolioCptValue(w, returnsList, params);
    if (val > best) {
      best = val;
      bestW = w;
    }
  }

  return bestW;
}
