import type { Asset } from "./types";

/**
 * Synthetic monthly returns inspired by Nifty-50 style large-cap behaviour.
 * Seeded so demos are reproducible without live market APIs.
 */
function mulberry32(seed: number) {
  return function next() {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function makeReturns(
  seed: number,
  months: number,
  annualMu: number,
  annualVol: number,
): number[] {
  const rand = mulberry32(seed);
  const mu = annualMu / 12;
  const sigma = annualVol / Math.sqrt(12);
  const out: number[] = [];
  for (let i = 0; i < months; i++) {
    // Box–Muller
    const u1 = Math.max(1e-12, rand());
    const u2 = rand();
    const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    // Mild fat tails + occasional drawdowns
    const shock = rand() < 0.04 ? -0.08 - rand() * 0.06 : 0;
    out.push(mu + sigma * z + shock);
  }
  return out;
}

const UNIVERSE: Array<{
  ticker: string;
  name: string;
  sector: string;
  mu: number;
  vol: number;
  seed: number;
}> = [
  { ticker: "RELIANCE", name: "Reliance Industries", sector: "Energy", mu: 0.14, vol: 0.22, seed: 101 },
  { ticker: "TCS", name: "Tata Consultancy", sector: "IT", mu: 0.12, vol: 0.18, seed: 102 },
  { ticker: "HDFCBANK", name: "HDFC Bank", sector: "Banks", mu: 0.13, vol: 0.2, seed: 103 },
  { ticker: "INFY", name: "Infosys", sector: "IT", mu: 0.11, vol: 0.19, seed: 104 },
  { ticker: "ICICIBANK", name: "ICICI Bank", sector: "Banks", mu: 0.15, vol: 0.24, seed: 105 },
  { ticker: "HINDUNILVR", name: "Hindustan Unilever", sector: "FMCG", mu: 0.1, vol: 0.15, seed: 106 },
  { ticker: "ITC", name: "ITC", sector: "FMCG", mu: 0.11, vol: 0.17, seed: 107 },
  { ticker: "SBIN", name: "State Bank of India", sector: "Banks", mu: 0.16, vol: 0.28, seed: 108 },
  { ticker: "BHARTIARTL", name: "Bharti Airtel", sector: "Telecom", mu: 0.13, vol: 0.21, seed: 109 },
  { ticker: "KOTAKBANK", name: "Kotak Mahindra Bank", sector: "Banks", mu: 0.12, vol: 0.22, seed: 110 },
  { ticker: "LT", name: "Larsen & Toubro", sector: "Infra", mu: 0.14, vol: 0.23, seed: 111 },
  { ticker: "AXISBANK", name: "Axis Bank", sector: "Banks", mu: 0.14, vol: 0.26, seed: 112 },
  { ticker: "ASIANPAINT", name: "Asian Paints", sector: "Consumer", mu: 0.1, vol: 0.18, seed: 113 },
  { ticker: "MARUTI", name: "Maruti Suzuki", sector: "Auto", mu: 0.12, vol: 0.25, seed: 114 },
  { ticker: "SUNPHARMA", name: "Sun Pharma", sector: "Pharma", mu: 0.11, vol: 0.2, seed: 115 },
  { ticker: "TITAN", name: "Titan Company", sector: "Consumer", mu: 0.15, vol: 0.24, seed: 116 },
  { ticker: "BAJFINANCE", name: "Bajaj Finance", sector: "NBFC", mu: 0.18, vol: 0.32, seed: 117 },
  { ticker: "WIPRO", name: "Wipro", sector: "IT", mu: 0.09, vol: 0.21, seed: 118 },
  { ticker: "ULTRACEMCO", name: "UltraTech Cement", sector: "Materials", mu: 0.13, vol: 0.22, seed: 119 },
  { ticker: "NESTLEIND", name: "Nestlé India", sector: "FMCG", mu: 0.1, vol: 0.14, seed: 120 },
  { ticker: "POWERGRID", name: "Power Grid", sector: "Utilities", mu: 0.11, vol: 0.16, seed: 121 },
  { ticker: "NTPC", name: "NTPC", sector: "Utilities", mu: 0.12, vol: 0.18, seed: 122 },
  { ticker: "TATASTEEL", name: "Tata Steel", sector: "Metals", mu: 0.14, vol: 0.35, seed: 123 },
  { ticker: "JSWSTEEL", name: "JSW Steel", sector: "Metals", mu: 0.13, vol: 0.34, seed: 124 },
  { ticker: "M&M", name: "Mahindra & Mahindra", sector: "Auto", mu: 0.15, vol: 0.27, seed: 125 },
  { ticker: "HCLTECH", name: "HCL Technologies", sector: "IT", mu: 0.12, vol: 0.2, seed: 126 },
  { ticker: "ADANIENT", name: "Adani Enterprises", sector: "Conglomerate", mu: 0.2, vol: 0.45, seed: 127 },
  { ticker: "TECHM", name: "Tech Mahindra", sector: "IT", mu: 0.1, vol: 0.23, seed: 128 },
  { ticker: "ONGC", name: "ONGC", sector: "Energy", mu: 0.12, vol: 0.28, seed: 129 },
  { ticker: "COALINDIA", name: "Coal India", sector: "Energy", mu: 0.11, vol: 0.24, seed: 130 },
];

const MONTHS = 60;

export const SAMPLE_ASSETS: Asset[] = UNIVERSE.map((u) => ({
  id: u.ticker,
  ticker: u.ticker,
  name: u.name,
  sector: u.sector,
  returns: makeReturns(u.seed, MONTHS, u.mu, u.vol),
}));

export const DEFAULT_CPT_PARAMS = {
  alpha: 0.88,
  beta: 0.88,
  lambda: 2.25,
  gamma: 0.61,
  delta: 0.69,
  reference: 0,
};
