export type Asset = {
  id: string;
  ticker: string;
  name: string;
  sector: string;
  /** Monthly excess returns (decimal), chronological */
  returns: number[];
};

export type CptParams = {
  /** Gain curvature α (Kahneman–Tversky ≈ 0.88) */
  alpha: number;
  /** Loss curvature β */
  beta: number;
  /** Loss aversion λ (≈ 2.25) */
  lambda: number;
  /** Probability weighting for gains γ */
  gamma: number;
  /** Probability weighting for losses δ */
  delta: number;
  /** Reference return (monthly); 0 = raw returns vs status quo */
  reference: number;
};

export type AssetMetrics = {
  ticker: string;
  name: string;
  sector: string;
  meanReturn: number;
  variance: number;
  volatility: number;
  sharpe: number;
  cptValue: number;
  deaEfficiency: number;
  crossEfficiency: number;
  marcosScore: number;
  cptRank: number;
  deaRank: number;
  marcosRank: number;
};

export type FrontierPoint = {
  risk: number;
  return: number;
  label: string;
  kind: "cpt" | "mean-variance" | "asset";
};

export type PortfolioResult = {
  tickers: string[];
  weights: number[];
  expectedReturn: number;
  volatility: number;
  sharpe: number;
  cptValue: number;
  method: string;
};

export type AnalysisResult = {
  assets: AssetMetrics[];
  frontierMv: FrontierPoint[];
  frontierCpt: FrontierPoint[];
  portfolios: {
    topCpt: PortfolioResult;
    bottomCpt: PortfolioResult;
    meanVariance: PortfolioResult;
    deaCross: PortfolioResult;
  };
  params: CptParams;
};
