# Prospectfolio — Behavioural Portfolio Lab

A practical web app inspired by Sweksha Srivastava’s Ph.D. work on **Cumulative Prospect Theory (CPT)** in **portfolio optimisation**, **DEA**, and **MCDA (MARCOS)**.

## What it does

1. Scores a Nifty-style stock universe with **CPT** (loss aversion, probability weighting).
2. Ranks assets with **DEA cross-efficiency** (variance as input; CPT + return as outputs).
3. Breaks DEA ties with **MARCOS**.
4. Builds **top-CPT**, **DEA×CPT**, and **mean–variance** portfolios and plots them on a risk–return map.

## Run locally

```bash
npm install
npm run dev -- --port 3456
```

Open [http://localhost:3456](http://localhost:3456).

## Stack

- Next.js (App Router) + TypeScript + Tailwind + shadcn/ui
- Recharts for frontiers
- `javascript-lp-solver` for CCR DEA LPs

## Note

Returns are **synthetic** (seeded) for a reproducible demo without market-data APIs. This is an educational tool, not financial advice.
