# What you need to do (USAR ARP 455)

Files ready for you:

- `Prospectfolio_Minor_Project_Report_ARP455.docx` — full minor project report in the USAR format
- `Prospectfolio_Viva_Presentation.pptx` — viva PPT (19 slides)
- `assets/` — figures used in both
- `generate_report_and_ppt.py` — regenerate after you personalise numbers (optional)

The report is written in **original wording** about *your* Prospectfolio build (not copied thesis text), uses **British English**, **Times New Roman**, **1.5 spacing**, USAR margins, chapter order, APA references, and is sized for **≥ 30 pages** when printed.

---

## Before printing the report

1. **Replace every placeholder**
   - `[YOUR FULL NAME]`
   - `[YOUR ENROLLMENT NO.]`
   - Branch: keep only one of `AI-DS / AI-ML / IIOT / AR`
   - `[NAME OF SUPERVISOR]` and `[DESIGNATION OF SUPERVISOR]`
   - `[YYYY–YY]` academic session
   - Dates on Certificate and Declaration

2. **Get signatures (mandatory — unsigned reports are not evaluated)**
   - Certificate by Supervisor
   - Declaration (you + supervisor)
   - Any Dean / coordinator line your school asks for

3. **Refresh demo numbers (strongly recommended for plagiarism + viva consistency)**
   - Run the app (`npm run dev`)
   - Capture your own screenshots of ranks, frontier, and portfolio tiles
   - Replace Table 3 / Table 4 values and swap figures in `docs/assets` if they differ
   - Re-run `python3 docs/generate_report_and_ppt.py` if you updated assets

4. **Add university logo on the cover** (PDF template shows GGSIPU logo; insert it at the top of the cover page in Word)

5. **Print settings**
   - A4
   - Spiral binding
   - Check page numbers: Roman (i, ii, …) from Certificate → Abstract; Arabic (1, 2, …) from Introduction → end
   - In Word: Update fields (page numbers) after opening once

6. **Plagiarism hygiene (your responsibility)**
   - Do **not** paste text from the thesis PDF or paper abstracts into the report
   - The draft is already original project narrative + cited literature
   - Add 1–2 short paragraphs in your own voice in Acknowledgement / Conclusion
   - Run your college plagiarism tool on the final DOCX before binding
   - Keep similarity within your school’s limit; cite all papers in APA

7. **Submit**
   - Spiral-bound hard copy as required
   - Soft copy if the school asks (PDF export from Word is fine)

---

## Before the PPT / viva

1. Put your name, enrollment, branch, supervisor on **slide 1**
2. Practise a **5–7 minute** flow:
   - Problem → pipeline → move λ slider live → Top-CPT vs MV vs Bottom-CPT → limitations (synthetic data)
3. Keep the app running offline/local as backup
4. Be ready to open `src/lib/portfolio/cpt.ts` and `dea.ts` if asked “where is the formula?”

---

## Suggested viva answers (short)

| Question | Point to say |
|---|---|
| Why CPT? | Investors feel losses harder and distort probabilities; MV ignores that |
| Why DEA? | Rank stocks as units: variance in, CPT + return out |
| Why MARCOS? | DEA often ties many units at efficiency = 1 |
| Why synthetic data? | Reproducible demo without API keys; labelled in UI |
| Limitation? | Not live trading advice; no costs/rebalancing yet |

---

## Optional upgrades (if supervisor asks)

- Connect real Nifty price CSV instead of synthetic returns
- Add your college logo and scanned signed certificate pages into the PDF
- Record a 2-minute demo video for internal submission
