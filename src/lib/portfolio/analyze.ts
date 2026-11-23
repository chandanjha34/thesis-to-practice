import { computeCptValue, portfolioCptValue } from "./cpt";
import { crossEfficiencyScores, deaScores, type DeaUnit } from "./dea";
import { marcosScores } from "./marcos";
import {
  equalWeight,
  maximizeCptPortfolio,
  maxSharpePortfolio,
  meanVarianceFrontier,
} from "./optimize";
import {
  annualizeReturn,
  annualizeVol,
  covMatrix,
  mean,
  normalizeWeights,
  portfolioReturn,
  portfolioVariance,
  sharpeRatio,
  stdev,
  variance,
} from "./stats";
import type {
  AnalysisResult,
  Asset,
  AssetMetrics,
  CptParams,
  FrontierPoint,
  PortfolioResult,
} from "./types";

function rankDesc(values: number[]): number[] {
  const indexed = values.map((v, i) => ({ v, i }));
  indexed.sort((a, b) => b.v - a.v);
  const ranks = Array(values.length).fill(0);
  indexed.forEach((item, rank) => {
    ranks[item.i] = rank + 1;
  });
  return ranks;
}

function buildPortfolio(
  assets: Asset[],
  indices: number[],
  weights: number[],
  method: string,
  params: CptParams,
): PortfolioResult {
  const subset = indices.map((i) => assets[i]);
  const returnsList = subset.map((a) => a.returns);
  const means = returnsList.map(mean);
  const cov = covMatrix(returnsList);
  const w = normalizeWeights(weights);
  const mRet = portfolioReturn(w, means);
  const mVar = portfolioVariance(w, cov);
  const vol = Math.sqrt(mVar);

  return {
    tickers: subset.map((a) => a.ticker),
    weights: w,
    expectedReturn: annualizeReturn(mRet),
    volatility: annualizeVol(vol),
    sharpe: sharpeRatio(annualizeReturn(mRet), annualizeVol(vol)),
    cptValue: portfolioCptValue(w, returnsList, params),
    method,
  };
}

export function analyzeUniverse(
  assets: Asset[],
  params: CptParams,
  topK = 10,
): AnalysisResult {
  const cptValues = assets.map((a) => computeCptValue(a.returns, params));
  // Shift CPT to positive for DEA outputs (thesis uses CPT as desirable output)
  const minCpt = Math.min(...cptValues);
  const cptForDea = cptValues.map((v) => v - minCpt + 0.01);
  const means = assets.map((a) => mean(a.returns));
  const vars = assets.map((a) => Math.max(1e-8, variance(a.returns)));

  const units: DeaUnit[] = assets.map((a, i) => ({
    id: a.ticker,
    inputs: [vars[i]],
    outputs: [cptForDea[i], Math.max(1e-6, means[i] + 0.05)], // long-term return proxy
  }));

  const deaEff = deaScores(units);
  const crossEff = crossEfficiencyScores(units);

  // MARCOS on: CPT (↑), mean return (↑), cross-efficiency (↑), variance (↓)
  const marcos = marcosScores(
    assets.map((_, i) => [cptValues[i], means[i], crossEff[i], vars[i]]),
    [true, true, true, false],
  );

  const cptRanks = rankDesc(cptValues);
  const deaRanks = rankDesc(crossEff);
  const marcosRanks = rankDesc(marcos);

  const metrics: AssetMetrics[] = assets.map((a, i) => {
    const vol = stdev(a.returns);
    return {
      ticker: a.ticker,
      name: a.name,
      sector: a.sector,
      meanReturn: annualizeReturn(means[i]),
      variance: vars[i],
      volatility: annualizeVol(vol),
      sharpe: sharpeRatio(annualizeReturn(means[i]), annualizeVol(vol)),
      cptValue: cptValues[i],
      deaEfficiency: deaEff[i],
      crossEfficiency: crossEff[i],
      marcosScore: marcos[i],
      cptRank: cptRanks[i],
      deaRank: deaRanks[i],
      marcosRank: marcosRanks[i],
    };
  });

  // Top / bottom CPT groups (thesis bifurcation)
  const byCpt = [...assets.keys()].sort((i, j) => cptValues[j] - cptValues[i]);
  const topIdx = byCpt.slice(0, topK);
  const bottomIdx = byCpt.slice(-topK);

  const topReturns = topIdx.map((i) => assets[i].returns);
  const bottomReturns = bottomIdx.map((i) => assets[i].returns);
  const allReturns = assets.map((a) => a.returns);

  const topW = maximizeCptPortfolio(topReturns, params);
  const bottomW = maximizeCptPortfolio(bottomReturns, params);
  const mvW = maxSharpePortfolio(allReturns);

  // DEA-cross portfolio: top-K by cross-efficiency, equal then CPT-tilted
  const byDea = [...assets.keys()].sort((i, j) => crossEff[j] - crossEff[i]);
  const deaIdx = byDea.slice(0, topK);
  const deaReturns = deaIdx.map((i) => assets[i].returns);
  const deaW = maximizeCptPortfolio(deaReturns, params, 500);

  const portfolios = {
    topCpt: buildPortfolio(assets, topIdx, topW, "Top-CPT behavioural", params),
    bottomCpt: buildPortfolio(
      assets,
      bottomIdx,
      bottomW,
      "Bottom-CPT behavioural",
      params,
    ),
    meanVariance: buildPortfolio(
      assets,
      [...assets.keys()],
      mvW,
      "Mean–variance (max Sharpe)",
      params,
    ),
    deaCross: buildPortfolio(
      assets,
      deaIdx,
      deaW,
      "DEA cross-efficiency + CPT",
      params,
    ),
  };

  // Frontiers
  const mvFrontier = meanVarianceFrontier(allReturns, 14);
  const frontierMv: FrontierPoint[] = mvFrontier.map((pt, i) => ({
    risk: annualizeVol(pt.risk) * 100,
    return: annualizeReturn(pt.ret) * 100,
    label: `MV-${i + 1}`,
    kind: "mean-variance",
  }));

  // CPT frontier: sample CPT-max portfolios under risk caps
  const frontierCpt: FrontierPoint[] = [];
  const cov = covMatrix(allReturns);
  const meansAll = allReturns.map(mean);
  for (let p = 0; p < 10; p++) {
    const w = maximizeCptPortfolio(allReturns, params, 350);
    // diversify samples by jittering
    const jittered = normalizeWeights(
      w.map((x) => x * (0.7 + Math.random() * 0.6)),
    );
    const risk = Math.sqrt(portfolioVariance(jittered, cov));
    const ret = portfolioReturn(jittered, meansAll);
    frontierCpt.push({
      risk: annualizeVol(risk) * 100,
      return: annualizeReturn(ret) * 100,
      label: `CPT-${p + 1}`,
      kind: "cpt",
    });
  }
  // Also plot equal-weight CPT-optimized on top group
  frontierCpt.push({
    risk: portfolios.topCpt.volatility * 100,
    return: portfolios.topCpt.expectedReturn * 100,
    label: "Top CPT",
    kind: "cpt",
  });

  // Asset scatter
  const assetPoints: FrontierPoint[] = metrics.map((m) => ({
    risk: m.volatility * 100,
    return: m.meanReturn * 100,
    label: m.ticker,
    kind: "asset",
  }));

  return {
    assets: metrics,
    frontierMv: [...frontierMv, ...assetPoints],
    frontierCpt,
    portfolios,
    params,
  };
}

export { equalWeight };
