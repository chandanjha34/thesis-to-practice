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

## USAR Minor Project (ARP 455) pack

See [`docs/WHAT_YOU_NEED_TO_DO.md`](docs/WHAT_YOU_NEED_TO_DO.md).

| File | Purpose |
|---|---|
| `docs/Prospectfolio_Minor_Project_Report_ARP455.docx` | Formatted project report |
| `docs/Prospectfolio_Viva_Presentation.pptx` | Viva presentation |
| `docs/generate_report_and_ppt.py` | Regenerates DOCX + PPTX |

```bash
python3 docs/generate_report_and_ppt.py
```

## Note

Returns are **synthetic** (seeded) for a reproducible demo without market-data APIs. This is an educational tool, not financial advice.
