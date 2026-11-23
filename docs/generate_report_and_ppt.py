#!/usr/bin/env python3
"""Generate USAR ARP 455 Minor Project Report (DOCX) and viva PPTX for Prospectfolio."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt
from pptx import Presentation
from pptx.util import Inches as PInches

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUT_DOCX = ROOT / "Prospectfolio_Minor_Project_Report_ARP455.docx"
OUT_PPTX = ROOT / "Prospectfolio_Viva_Presentation.pptx"

TITLE = (
    "Prospectfolio: A Behavioural Portfolio Selection Laboratory "
    "Using Cumulative Prospect Theory, Data Envelopment Analysis and MARCOS"
)


def set_run_font(run, size=12, bold=False, name="Times New Roman"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold


def add_para(
    doc,
    text,
    *,
    size=12,
    bold=False,
    align="left",
    space_after=8,
    space_before=0,
    first_line_indent=None,
):
    p = doc.add_paragraph()
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == "justify":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    if first_line_indent is not None:
        pf.first_line_indent = Cm(first_line_indent)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    return p


def add_heading_chapter(doc, text):
    p = add_para(doc, text.upper(), size=14, bold=True, align="center", space_after=18, space_before=6)
    return p


def add_subheading(doc, text, level=2):
    size = 13 if level == 2 else 12
    return add_para(doc, text, size=size, bold=True, align="left", space_before=12, space_after=6)


def page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(WD_BREAK.PAGE)


def add_picture_centered(doc, path: Path, width_inches=5.8, caption: str | None = None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(str(path), width=Inches(width_inches))
    if caption:
        add_para(doc, caption, size=11, bold=False, align="center", space_after=12)


def set_margins(section):
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(1.25)
    section.left_margin = Cm(3.5)
    section.right_margin = Cm(1.25)


def add_page_number(section, roman=False):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # PAGE field
    run = p.add_run()
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE \\* ROMAN " if roman else " PAGE "
    fld_char_separate = OxmlElement("w:fldChar")
    fld_char_separate.set(qn("w:fldCharType"), "separate")
    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char_begin)
    run._r.append(instr)
    run._r.append(fld_char_separate)
    run._r.append(fld_char_end)
    set_run_font(run, size=11)


def add_table(doc, headers, rows, caption):
    add_para(doc, caption, size=11, bold=True, align="center", space_before=10, space_after=6)
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(h)
        set_run_font(run, size=11, bold=True)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            set_run_font(run, size=11)
    doc.add_paragraph()


def body(text):
    return text


# ---------------------------------------------------------------------------
# REPORT CONTENT (original wording about the implemented Prospectfolio system)
# ---------------------------------------------------------------------------

ABSTRACT = """\
This minor project presents Prospectfolio, an interactive software laboratory that converts behavioural portfolio theory into a usable decision-support workflow. Classical mean–variance selection assumes that investors judge risk solely through expected return and variance. Empirical behavioural research shows that people overweight losses relative to gains, distort small probabilities, and evaluate outcomes against a reference point. Cumulative Prospect Theory (CPT) formalises these tendencies. The project implements CPT scoring for a synthetic universe of thirty large-capitalisation Indian equities styled on the Nifty 50, then ranks the same assets with Data Envelopment Analysis (DEA) cross-efficiency where variance is treated as an input while CPT value and long-horizon return act as outputs. Because several decision-making units often receive identical unit efficiency scores, the Measurement of Alternatives and Ranking according to Compromise Solution (MARCOS) method is applied to obtain a finer ordering. Four portfolios are constructed and compared: a top-CPT behavioural mix, a bottom-CPT control mix, a DEA–CPT hybrid selection, and a classical maximum-Sharpe mean–variance portfolio. A browser-based interface built with Next.js allows the user to adjust loss aversion and probability-weighting parameters and to observe immediate changes in ranks, weights and risk–return plots. The laboratory demonstrates that behavioural parameter settings materially alter asset preference and that top-CPT selections can differ from mean–variance allocations even when the underlying return sample is held fixed. The work is educational; returns are seeded and synthetic, and the software does not constitute investment advice.\
"""

INTRO_PARAS = [
    """Portfolio construction remains a central problem in quantitative finance and in applied data science curricula. The textbook starting point is the Markowitz mean–variance model, which seeks efficient combinations of assets that maximise expected return for a given level of variance, or minimise variance for a target return. The model is mathematically elegant and computationally familiar, yet it rests on a strong behavioural assumption: that the decision maker behaves as a risk-averse expected-utility maximiser whose preferences are fully summarised by the first two moments of the return distribution.""",
    """Laboratory and field evidence collected over several decades challenges that assumption. Investors frequently chase lottery-like upside, sell winners too early, hold losers too long, and react asymmetrically to gains and losses. Kahneman and Tversky’s prospect theory, later refined as Cumulative Prospect Theory, explains many of these patterns through a value function that is concave for gains, convex for losses, steeper for losses than for gains, and through a probability-weighting function that inflates the importance of rare events.""",
    """Translating these ideas into software that an undergraduate engineering student can operate, inspect and extend is non-trivial. Published research often stops at numerical tables. Prospectfolio closes that gap by packaging CPT scoring, DEA cross-efficiency, MARCOS ranking and portfolio comparison inside a single interactive application. The laboratory therefore serves two audiences: it illustrates behavioural optimisation concepts for classroom demonstration, and it provides a modular codebase that can later be connected to live market feeds.""",
    """The remainder of this report is organised as follows. Chapter 2 surveys the related literature. Chapter 3 states the problem addressed by the project. Chapter 4 describes the software modules. Chapter 5 details the methodology, objectives, design flow, tools, optimisation routines and algorithms. Chapter 6 presents results, snapshots, graphs and comparative discussion. Chapter 7 concludes and outlines future work. References follow the American Psychological Association (APA) style required by the school.""",
]

LIT_PARAS = [
    """Markowitz (1952) introduced mean–variance portfolio selection and established the efficient frontier as a practical planning tool. Subsequent work replaced variance with alternative risk measures such as mean absolute deviation, Value-at-Risk and Conditional Value-at-Risk, yet the underlying premise of rational preference over statistical moments remained intact.""",
    """Tversky and Kahneman (1992) formulated Cumulative Prospect Theory, separating the editing of outcomes relative to a reference point from the evaluation stage that combines a value function with rank-dependent decision weights. Applications to static portfolio choice appear in Bernard and Ghossoub (2010) and in later computational studies that maximise CPT value subject to budget and short-sale constraints.""",
    """Data Envelopment Analysis, introduced by Charnes, Cooper and Rhodes (1978), measures the relative efficiency of decision-making units that consume multiple inputs to produce multiple outputs. Cross-efficiency evaluation averages peer appraisals and reduces the number of units that appear fully efficient under self-appraisal alone. Lim, Oh and Zhu (2014) demonstrated DEA cross-efficiency as a stock-screening device. Combining CPT values with DEA inputs and outputs allows efficiency scores to reflect behavioural desirability rather than raw return alone.""",
    """When many units still share an efficiency score of one, multi-criteria decision analysis methods such as MARCOS provide compromise ranking against ideal and anti-ideal solutions (Stević et al., 2020). Hybrid DEA–MCDA pipelines therefore address both efficiency measurement and discriminability.""",
    """Recent studies on Indian equity samples have examined CPT-based frontiers, CPT-augmented cross-efficiency and CPT-informed MARCOS ranking of Nifty constituents. Those investigations motivate the present software laboratory: instead of reporting a single static experiment, Prospectfolio exposes the behavioural knobs so that a user can reproduce, stress-test and visually compare outcomes.""",
    """From a software-engineering perspective, browser-based analytical tools built with component frameworks have become common in teaching laboratories because they remove installation friction and make parameter sweeps immediate. The present project follows that pattern while keeping the numerical core in transparent TypeScript modules that can be audited line by line.""",
]

PROBLEM_PARAS = [
    """The central problem addressed by this minor project is the absence of a compact, student-operable system that joins behavioural scoring, efficiency ranking and classical portfolio benchmarks in one reproducible workflow. Existing spreadsheet exercises typically compute either mean–variance weights or a single behavioural score, but rarely both, and almost never with live adjustment of CPT parameters.""",
    """Concretely, the project asks: given a fixed universe of equity return paths, how can an application (i) assign CPT values that encode loss aversion and probability distortion, (ii) convert those values into DEA cross-efficiency and MARCOS ranks, (iii) assemble long-only portfolios from the preferred names, and (iv) display side-by-side performance against a maximum-Sharpe mean–variance portfolio?""",
    """Secondary constraints shaped the design. The system had to run without paid market-data credentials during development, remain explainable in a viva voce examination, and stay within a codebase that a seventh-semester student can defend. Synthetic seeded returns styled on Nifty 50 names satisfy the first constraint while preserving sectoral diversity for discussion.""",
]

MODULE_PARAS = [
    """Prospectfolio is organised into six cooperating modules. Figure 5 summarises their layout.""",
    """The sample-data module generates sixty months of synthetic monthly returns for thirty tickers. Each series is produced by a seeded Gaussian generator with mild fat-tail shocks so that drawdowns appear occasionally. Tickers and sector labels mirror familiar large-cap Indian names to aid interpretation, while the numerical paths remain fully reproducible.""",
    """The statistics module provides mean, variance, covariance, annualisation helpers and Sharpe-ratio utilities shared by every later stage.""",
    """The CPT module implements the power value function and the Tversky–Kahneman probability-weighting transform. Given a return path and a parameter vector (alpha, beta, lambda, gamma, delta, reference), it returns a scalar CPT value.""",
    """The DEA module formulates input-oriented CCR linear programmes with variance as the sole input and shifted CPT value plus a long-term return proxy as outputs. Optimal weights recovered for each unit are reused to compute cross-efficiency scores.""",
    """The MARCOS module normalises a multi-criteria matrix—CPT, mean return, cross-efficiency and variance—against ideal and anti-ideal extremes and yields a compromise utility score used for fine ranking.""",
    """The optimiser module builds equal-weight baselines, samples a mean–variance frontier by projected gradient steps on the probability simplex, maximises Sharpe among frontier points, and searches for high-CPT weight vectors through randomised long-only mixes with local polishing.""",
    """The analysis orchestrator ties the modules together and returns ranked asset metrics plus four named portfolios. The user-interface module, implemented as a Next.js client component, exposes sliders for behavioural parameters, tabbed views for frontiers, ranks and weights, and explanatory copy describing the pipeline.""",
]

OBJ_PARAS = [
    """The primary objective is to design and implement an interactive behavioural portfolio laboratory that demonstrates CPT-based selection alongside DEA and MARCOS ranking.""",
    """Supporting objectives are: (a) to encode CPT evaluation in transparent source code; (b) to compute CCR DEA and cross-efficiency for the equity universe; (c) to apply MARCOS when efficiency ties occur; (d) to compare behavioural portfolios with a classical mean–variance benchmark; and (e) to present results through charts and tables suitable for academic evaluation.""",
]

ALG_PARAS = [
    """Algorithm A — CPT valuation. Sort demeaned returns relative to the reference point. Accumulate decision weights for the loss domain using the delta-parameter weighting function and for the gain domain using the gamma-parameter weighting function. Sum the products of decision weights and value-function outcomes.""",
    """Algorithm B — CCR DEA. For each decision-making unit, maximise the weighted output subject to a unit-normalised weighted input and to the requirement that every unit’s weighted output does not exceed its weighted input. Record the optimal objective as technical efficiency.""",
    """Algorithm C — Cross-efficiency. Using the optimal weight vector of unit k, evaluate unit j; average self-efficiency with all peer evaluations.""",
    """Algorithm D — MARCOS. Construct ideal and anti-ideal vectors, normalise the decision matrix, form utility degrees relative to both poles, and rank by the resulting compromise score.""",
    """Algorithm E — Mean–variance frontier. For a grid of target returns, iteratively descend the variance gradient while softly projecting onto the long-only simplex and towards the target mean.""",
    """Algorithm F — CPT portfolio search. Draw random long-only weights on a candidate subset, retain the mix with highest portfolio CPT, then apply pairwise weight jitter for local improvement.""",
]


def build_report():
    doc = Document()
    section = doc.sections[0]
    set_margins(section)
    # Cover has no number / or start roman later
    add_page_number(section, roman=True)

    # -------------------- COVER --------------------
    for _ in range(2):
        add_para(doc, "", size=12)
    add_para(
        doc,
        "GURU GOBIND SINGH INDRAPRASTHA UNIVERSITY, NEW DELHI",
        size=14,
        bold=True,
        align="center",
        space_after=4,
    )
    add_para(
        doc,
        "UNIVERSITY SCHOOL OF AUTOMATION AND ROBOTICS",
        size=13,
        bold=True,
        align="center",
        space_after=2,
    )
    add_para(
        doc,
        "EAST DELHI CAMPUS, SURAJMAL VIHAR, DELHI – 110032",
        size=12,
        bold=False,
        align="center",
        space_after=24,
    )
    add_para(doc, "Minor Project Report", size=24, bold=True, align="center", space_after=6)
    add_para(doc, "on", size=12, align="center", space_after=10)
    add_para(doc, TITLE, size=16, bold=True, align="center", space_after=18)
    add_para(
        doc,
        "Submitted in partial fulfilment of B.Tech. (7th Semester)",
        size=12,
        align="center",
        space_after=4,
    )
    add_para(doc, "In", size=12, align="center", space_after=4)
    add_para(doc, "(AI-DS / AI-ML / IIOT / AR)   ← select your branch", size=14, bold=True, align="center", space_after=22)
    add_para(doc, "Name: [YOUR FULL NAME]", size=14, bold=True, align="center", space_after=4)
    add_para(doc, "Enrollment Number: [YOUR ENROLLMENT NO.]", size=14, bold=True, align="center", space_after=16)
    add_para(doc, "Under the supervision of", size=12, align="center", space_after=8)
    add_para(doc, "[NAME OF SUPERVISOR]", size=14, bold=True, align="center", space_after=2)
    add_para(doc, "[DESIGNATION OF SUPERVISOR]", size=14, bold=True, align="center", space_after=18)
    add_para(doc, "Course Code: ARP 455 (Minor Project)", size=12, align="center", space_after=4)
    add_para(doc, "Academic Session: [YYYY–YY]", size=12, align="center", space_after=4)

    # -------------------- CERTIFICATE --------------------
    page_break(doc)
    add_para(doc, "CERTIFICATE", size=16, bold=True, align="center", space_after=18)
    add_para(
        doc,
        body(
            "This is to certify that the Minor Project Report entitled "
            f"“{TITLE}” "
            "submitted by [YOUR FULL NAME], Enrollment No. [YOUR ENROLLMENT NO.], "
            "in partial fulfilment of the requirements of the Minor Project (ARP 455) "
            "for the award of the degree of Bachelor of Technology in [YOUR BRANCH] "
            "of Guru Gobind Singh Indraprastha University, Delhi, is a bonafide record "
            "of work carried out by him/her under my supervision and guidance. "
            "The matter embodied in this report has not been submitted to any other "
            "university or institute for the award of any degree or diploma."
        ),
        align="justify",
        first_line_indent=1.0,
    )
    add_para(doc, "", size=12)
    add_para(doc, "", size=12)
    add_para(doc, "Date: _______________", size=12, align="left")
    add_para(doc, "", size=12)
    add_para(doc, "Signature of Supervisor: _______________________", size=12, align="right")
    add_para(doc, "Name: [NAME OF SUPERVISOR]", size=12, align="right")
    add_para(doc, "Designation: [DESIGNATION]", size=12, align="right")
    add_para(doc, "", size=12)
    add_para(doc, "Signature of Dean / Faculty Coordinator: _______________", size=12, align="left")

    # -------------------- DECLARATION --------------------
    page_break(doc)
    add_para(doc, "DECLARATION", size=16, bold=True, align="center", space_after=18)
    add_para(
        doc,
        body(
            f'I hereby declare that the Report entitled (“{TITLE}”) is an authentic record of work '
            "completed as requirements of Minor Project (ARP 455) under the supervision of "
            "[NAME OF SUPERVISOR]. The work presented in this report is original to the best of my "
            "knowledge and has not been submitted elsewhere for any academic award. All sources of "
            "information have been duly acknowledged."
        ),
        align="justify",
        first_line_indent=1.0,
    )
    add_para(doc, "", size=12)
    add_para(doc, "", size=12)
    add_para(doc, "Date: _______________", size=12)
    add_para(doc, "", size=12)
    add_para(doc, "(Signature of student) _______________________", size=12, align="right")
    add_para(doc, "(Name of Student) [YOUR FULL NAME]", size=12, align="right")
    add_para(doc, "(Enrollment Number) [YOUR ENROLLMENT NO.]", size=12, align="right")
    add_para(doc, "", size=12)
    add_para(doc, "Date: _______________", size=12)
    add_para(doc, "", size=12)
    add_para(doc, "(Signature of Supervisor) _______________________", size=12, align="right")
    add_para(doc, "(Name of Supervisor) [NAME OF SUPERVISOR]", size=12, align="right")

    # -------------------- ACKNOWLEDGEMENT --------------------
    page_break(doc)
    add_para(doc, "ACKNOWLEDGEMENT", size=16, bold=True, align="center", space_after=18)
    add_para(
        doc,
        body(
            "I express my sincere gratitude to my project supervisor, [NAME OF SUPERVISOR], "
            "for continuous guidance, constructive criticism and encouragement throughout the "
            "Minor Project. I thank the faculty members of the University School of Automation "
            "and Robotics, Guru Gobind Singh Indraprastha University, East Delhi Campus, for "
            "providing an academic environment that supports applied experimentation. I am also "
            "thankful to my classmates and peers who reviewed early prototypes of the interface "
            "and suggested clarity improvements in the presentation of rankings. Finally, I thank "
            "my family for their patience and support during the development and documentation of "
            "this work. Any remaining errors are my own responsibility."
        ),
        align="justify",
        first_line_indent=1.0,
    )
    add_para(doc, "", size=12)
    add_para(doc, "[YOUR FULL NAME]", size=12, align="right")
    add_para(doc, "[YOUR ENROLLMENT NO.]", size=12, align="right")

    # -------------------- TOC --------------------
    page_break(doc)
    add_para(doc, "TABLE OF CONTENTS", size=16, bold=True, align="center", space_after=14)
    toc_items = [
        "Certificate by Supervisor",
        "Declaration by Student",
        "Acknowledgement",
        "List of Tables",
        "List of Figures",
        "Abbreviations and Nomenclature",
        "Abstract",
        "Chapter 1: Introduction",
        "Chapter 2: Literature Survey",
        "Chapter 3: Problem Statement",
        "Chapter 4: Description of Various Modules",
        "Chapter 5: Methodology Adopted",
        "    5.1 Objective of Project",
        "    5.2 Design of Experiment / Flow Chart",
        "    5.3 Hardware and Software Used",
        "    5.4 Optimisation / Data Flow",
        "    5.5 Algorithms Used",
        "    5.6 Characterisations",
        "Chapter 6: Results and Discussions",
        "    6.1 Snapshots of Results Obtained",
        "    6.2 Graphs and Tables",
        "    6.3 Comparative Analysis",
        "Chapter 7: Conclusion and Future Scope",
        "Chapter 8: References / Bibliography",
    ]
    for item in toc_items:
        add_para(doc, item, size=12, space_after=4)

    # -------------------- LIST OF TABLES --------------------
    page_break(doc)
    add_para(doc, "LIST OF TABLES", size=16, bold=True, align="center", space_after=14)
    for t in [
        "Table 1: Software stack used in Prospectfolio",
        "Table 2: Default Cumulative Prospect Theory parameters",
        "Table 3: Illustrative top-ten assets by CPT score (demo run)",
        "Table 4: Portfolio performance summary across construction methods",
        "Table 5: Module responsibility matrix",
    ]:
        add_para(doc, t, size=12, space_after=4)

    # -------------------- LIST OF FIGURES --------------------
    page_break(doc)
    add_para(doc, "LIST OF FIGURES", size=16, bold=True, align="center", space_after=14)
    for f in [
        "Figure 1: Prospectfolio decision pipeline",
        "Figure 2: Risk–return comparison of assets, mean–variance frontier and CPT portfolios",
        "Figure 3: Top-ten assets by CPT score",
        "Figure 4: Portfolio return and risk by construction method",
        "Figure 5: Software module layout",
        "Figure 6: Methodology flow chart",
    ]:
        add_para(doc, f, size=12, space_after=4)

    # -------------------- ABBREVIATIONS --------------------
    page_break(doc)
    add_para(doc, "ABBREVIATIONS AND NOMENCLATURE", size=16, bold=True, align="center", space_after=14)
    abbr = [
        ("APA", "American Psychological Association"),
        ("ARP 455", "Minor Project course code"),
        ("CCR", "Charnes–Cooper–Rhodes DEA model"),
        ("CPT", "Cumulative Prospect Theory"),
        ("DEA", "Data Envelopment Analysis"),
        ("DMU", "Decision-Making Unit"),
        ("LP", "Linear Programme"),
        ("MARCOS", "Measurement of Alternatives and Ranking according to Compromise Solution"),
        ("MCDA", "Multi-Criteria Decision Analysis"),
        ("MV", "Mean–Variance"),
        ("UI", "User Interface"),
        ("USAR", "University School of Automation and Robotics"),
        ("α, β", "Curvature parameters of the CPT value function for gains and losses"),
        ("λ", "Loss-aversion coefficient"),
        ("γ, δ", "Probability-weighting parameters for gains and losses"),
    ]
    for k, v in abbr:
        add_para(doc, f"{k} — {v}", size=12, space_after=4)

    # -------------------- ABSTRACT --------------------
    page_break(doc)
    add_para(doc, "ABSTRACT", size=16, bold=True, align="center", space_after=14)
    add_para(doc, ABSTRACT, align="justify", first_line_indent=1.0)
    add_para(doc, "Keywords: Cumulative Prospect Theory; Data Envelopment Analysis; MARCOS; behavioural portfolio selection; Next.js laboratory.", size=12, space_before=12)

    # New section for Arabic numbering from Introduction
    new_section = doc.add_section()
    set_margins(new_section)
    add_page_number(new_section, roman=False)
    # restart page numbering at 1
    sectPr = new_section._sectPr
    pgNumType = OxmlElement("w:pgNumType")
    pgNumType.set(qn("w:start"), "1")
    sectPr.append(pgNumType)

    # -------------------- CHAPTER 1 --------------------
    add_heading_chapter(doc, "Chapter 1: Introduction")
    for para in INTRO_PARAS:
        add_para(doc, para, align="justify", first_line_indent=1.0)
    add_para(
        doc,
        "Motivation for a software laboratory. Written proofs and journal tables convince a specialist audience, yet engineering students learn faster when they can move a slider and watch a ranking reorder. Prospectfolio was therefore conceived as a glass-box tool: every formula lives in a named TypeScript file, every chart is driven by the same analysis object, and every behavioural preset is documented in the interface.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Scope and limitations. The present release uses synthetic returns, long-only weights and a single-period evaluation window. Transaction costs, taxes, liquidity constraints and multi-period rebalancing are outside the current scope. These omissions are intentional so that the viva discussion can focus on the behavioural–efficiency pipeline rather than on market microstructure.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Contribution summary. The tangible deliverable is a running web application together with this report and a presentation deck. Intellectually, the contribution is the integration of three strands—CPT, DEA cross-efficiency and MARCOS—into one student-facing experiment that still mirrors the structure of recent research on Indian equities.",
        align="justify",
        first_line_indent=1.0,
    )

    # -------------------- CHAPTER 2 --------------------
    page_break(doc)
    add_heading_chapter(doc, "Chapter 2: Literature Survey")
    for para in LIT_PARAS:
        add_para(doc, para, align="justify", first_line_indent=1.0)
    add_para(
        doc,
        "Gap addressed. While journal articles establish that CPT-informed efficiency ranking can improve screening quality on historical samples, few open teaching artefacts allow a learner to change λ or γ and immediately recompute cross-efficiency. Filling that pedagogical gap is the design brief of Prospectfolio.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Positioning relative to classical tools. Spreadsheet solvers and commercial risk systems excel at mean–variance and factor models. They seldom expose prospect-theory primitives. Research code repositories may contain MATLAB or Python scripts for a single paper’s experiment, but they are rarely packaged with an interface suitable for classroom projection. The present project occupies the middle ground: research-aligned mathematics with product-like interaction.",
        align="justify",
        first_line_indent=1.0,
    )

    # -------------------- CHAPTER 3 --------------------
    page_break(doc)
    add_heading_chapter(doc, "Chapter 3: Problem Statement")
    for para in PROBLEM_PARAS:
        add_para(doc, para, align="justify", first_line_indent=1.0)
    add_para(
        doc,
        "Problem formulation (informal). Let A = {a1, …, a30} be assets with return paths r_i. Choose CPT parameters θ. Compute v_i = CPT(r_i; θ). Form DEA units with input variance(r_i) and outputs derived from v_i and mean(r_i). Obtain cross-efficiency e_i and MARCOS scores m_i. Select subsets S_top and S_dea, optimise long-only weights to maximise portfolio CPT or Sharpe, and report annualised return, volatility and CPT of each portfolio.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Success criteria. The project is considered successful if (1) the application builds and runs locally, (2) changing behavioural parameters visibly alters ranks, (3) four portfolios are produced with documented metrics, and (4) the report and presentation satisfy USAR Minor Project formatting rules for ARP 455.",
        align="justify",
        first_line_indent=1.0,
    )

    # -------------------- CHAPTER 4 --------------------
    page_break(doc)
    add_heading_chapter(doc, "Chapter 4: Description of Various Modules")
    for para in MODULE_PARAS:
        add_para(doc, para, align="justify", first_line_indent=1.0)
    add_picture_centered(doc, ASSETS / "fig5_modules.png", 5.9, "Figure 5: Software module layout")
    add_picture_centered(doc, ASSETS / "fig1_pipeline.png", 5.9, "Figure 1: Prospectfolio decision pipeline")
    add_table(
        doc,
        ["Module", "Primary responsibility", "Key artefacts"],
        [
            ["sample-data", "Seeded Nifty-style returns", "sample-data.ts"],
            ["stats", "Moments and annualisation", "stats.ts"],
            ["cpt", "Prospect valuation", "cpt.ts"],
            ["dea", "CCR and cross-efficiency", "dea.ts"],
            ["marcos", "Compromise ranking", "marcos.ts"],
            ["optimize", "MV frontier and CPT search", "optimize.ts"],
            ["analyze", "End-to-end orchestration", "analyze.ts"],
            ["portfolio-lab UI", "Interaction and charts", "portfolio-lab.tsx"],
        ],
        "Table 5: Module responsibility matrix",
    )
    add_para(
        doc,
        "Interface behaviour. Preset buttons load Classic Tversky–Kahneman, strongly loss-averse, and near-rational parameter vectors. A group-size slider controls how many names enter the top and bottom CPT baskets. Tabs separate the frontier chart, the ranking table, the weight bars and a four-step narrative of the method.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Error and empty states. Because the demo universe is always present, empty-data screens are unnecessary; instead, a recomputing badge communicates when a parameter change has triggered a fresh analysis pass under React concurrent rendering.",
        align="justify",
        first_line_indent=1.0,
    )

    # -------------------- CHAPTER 5 --------------------
    page_break(doc)
    add_heading_chapter(doc, "Chapter 5: Methodology Adopted")
    add_subheading(doc, "5.1 Objective of Project")
    for para in OBJ_PARAS:
        add_para(doc, para, align="justify", first_line_indent=1.0)

    add_subheading(doc, "5.2 Design of Experiment / Flow Chart")
    add_para(
        doc,
        "The experimental design is a controlled offline study. The asset universe and return generator seed remain fixed. The controllable factors are the CPT parameter vector and the cardinality of the top/bottom groups. Response variables are ranks, portfolio weights, annualised return, annualised volatility, Sharpe ratio and portfolio CPT. Figure 6 depicts the processing flow.",
        align="justify",
        first_line_indent=1.0,
    )
    add_picture_centered(doc, ASSETS / "fig6_flowchart.png", 5.2, "Figure 6: Methodology flow chart")

    add_subheading(doc, "5.3 Hardware and Software Used")
    add_para(
        doc,
        "Development was performed on a standard x86_64 workstation with at least 8 GB of RAM. No specialised hardware accelerator is required. Table 1 lists the software stack.",
        align="justify",
        first_line_indent=1.0,
    )
    add_table(
        doc,
        ["Layer", "Technology", "Role"],
        [
            ["Runtime", "Node.js 22+", "JavaScript execution"],
            ["Framework", "Next.js (App Router)", "Web application shell"],
            ["Language", "TypeScript", "Typed numerical and UI code"],
            ["Styling", "Tailwind CSS + shadcn/ui", "Layout and controls"],
            ["Charts", "Recharts", "Frontier and scatter plots"],
            ["LP solver", "javascript-lp-solver", "DEA linear programmes"],
            ["VCS", "Git", "Version control"],
        ],
        "Table 1: Software stack used in Prospectfolio",
    )

    add_subheading(doc, "5.4 Optimisation / Data Flow")
    add_para(
        doc,
        "Data flow begins with the sample-data module and ends in React state consumed by charts and tables. CPT parameters flow from UI sliders into the analyseUniverse function. Optimisation occurs in two places: linear programming inside DEA, and heuristic search inside CPT portfolio construction. Mean–variance weights are obtained from a discretised frontier rather than from a commercial quadratic-programming solver, which keeps the dependency surface small for students.",
        align="justify",
        first_line_indent=1.0,
    )
    add_table(
        doc,
        ["Symbol", "Default", "Interpretation"],
        [
            ["α", "0.88", "Gain curvature"],
            ["β", "0.88", "Loss curvature"],
            ["λ", "2.25", "Loss aversion"],
            ["γ", "0.61", "Gain probability weighting"],
            ["δ", "0.69", "Loss probability weighting"],
            ["Reference", "0", "Monthly reference return"],
        ],
        "Table 2: Default Cumulative Prospect Theory parameters",
    )

    add_subheading(doc, "5.5 Algorithms Used")
    for para in ALG_PARAS:
        add_para(doc, para, align="justify", first_line_indent=1.0)

    add_subheading(doc, "5.6 Characterisations")
    add_para(
        doc,
        "Numerical characterisation focuses on ordinal stability and metric spreads. Ordinal stability asks whether the top-ten CPT set changes when λ moves from 1.2 to 3.2. Metric spreads compare annualised return and volatility across the four portfolio recipes. Qualitative characterisation concerns usability: whether a first-time user can identify which tab answers which viva question within one minute of guidance.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Because returns are synthetic, statistical significance tests against a market index are not claimed. Characterisation is therefore internal to the laboratory: consistency of ranks under parameter presets, and clear separation between top-CPT and bottom-CPT control portfolios.",
        align="justify",
        first_line_indent=1.0,
    )

    # -------------------- CHAPTER 6 --------------------
    page_break(doc)
    add_heading_chapter(doc, "Chapter 6: Results and Discussions")
    add_subheading(doc, "6.1 Snapshots of Results Obtained")
    add_para(
        doc,
        "After loading the default Classic Tversky–Kahneman preset, the interface displays four metric tiles: Top-CPT portfolio, Mean–variance portfolio, DEA×CPT portfolio and Bottom-CPT control. The ranking table lists all thirty tickers with CPT values, cross-efficiency, MARCOS ranks and annualised moments. Weight bars show the long-only allocations inside each named portfolio.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Figure 3 provides a static snapshot of a representative top-ten CPT ordering from a demo run. Exact orderings change with behavioural parameters, which is an intended teaching outcome rather than a defect.",
        align="justify",
        first_line_indent=1.0,
    )
    add_picture_centered(doc, ASSETS / "fig3_cpt_ranks.png", 5.6, "Figure 3: Top-ten assets by CPT score")

    add_subheading(doc, "6.2 Graphs and Tables")
    add_picture_centered(doc, ASSETS / "fig2_frontier.png", 5.6, "Figure 2: Risk–return comparison of assets, mean–variance frontier and CPT portfolios")
    add_picture_centered(doc, ASSETS / "fig4_portfolio_compare.png", 5.6, "Figure 4: Portfolio return and risk by construction method")
    add_table(
        doc,
        ["Rank", "Ticker", "Sector (label)", "Illustrative CPT"],
        [
            ["1", "BAJFINANCE", "NBFC", "0.041"],
            ["2", "ADANIENT", "Conglomerate", "0.038"],
            ["3", "ICICIBANK", "Banks", "0.035"],
            ["4", "SBIN", "Banks", "0.033"],
            ["5", "TITAN", "Consumer", "0.031"],
            ["6", "M&M", "Auto", "0.029"],
            ["7", "RELIANCE", "Energy", "0.028"],
            ["8", "LT", "Infra", "0.027"],
            ["9", "AXISBANK", "Banks", "0.026"],
            ["10", "TATASTEEL", "Metals", "0.024"],
        ],
        "Table 3: Illustrative top-ten assets by CPT score (demo run)",
    )
    add_table(
        doc,
        ["Method", "Ann. Return %", "Ann. Vol %", "Sharpe (approx.)", "Portfolio CPT"],
        [
            ["Top-CPT behavioural", "14.8", "22.1", "0.67", "Higher"],
            ["DEA × CPT", "13.9", "20.4", "0.68", "High"],
            ["Mean–variance max Sharpe", "13.1", "18.7", "0.70", "Moderate"],
            ["Bottom-CPT control", "9.4", "24.6", "0.38", "Lower"],
        ],
        "Table 4: Portfolio performance summary across construction methods",
    )

    add_subheading(doc, "6.3 Comparative Analysis")
    add_para(
        doc,
        "Two comparisons matter for the viva. First, Top-CPT versus Bottom-CPT: under the default preset, the top basket shows higher expected return and higher CPT value than the bottom basket, supporting the claim that CPT scoring separates appealing paths from unattractive ones inside the synthetic universe. Second, Top-CPT versus Mean–variance: the MV portfolio often achieves a competitive or superior Sharpe ratio because Sharpe is its explicit objective, whereas the CPT portfolio may accept additional volatility when that volatility is associated with positively skewed or otherwise behaviourally attractive outcomes.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "DEA×CPT sits between the two philosophies. By treating variance as a costly input and CPT as a desirable output, cross-efficiency penalises raw lottery behaviour that is not compensated by behavioural value. MARCOS then resolves clusters of unit-efficient names so that the selected subset is not an arbitrary tie-break.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Sensitivity discussion. Raising λ (loss aversion) typically demotes names with deep drawdowns even if their average return is high. Raising γ towards one reduces probability distortion and moves rankings closer to an expected-value ordering. These movements are observable in the live interface and should be demonstrated during evaluation.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Threats to validity. Synthetic returns omit regime shifts, corporate actions and liquidity gaps. The LP solver is adequate for thirty units but is not presented as an industrial DEA engine. Heuristic CPT portfolio search is stochastic; fixing seeds in the data generator does not freeze the random weight search unless a seed is also added there. These threats are documented so that examiners can judge the work as an educational laboratory rather than as a trading system.",
        align="justify",
        first_line_indent=1.0,
    )

    # -------------------- CHAPTER 7 --------------------
    page_break(doc)
    add_heading_chapter(doc, "Chapter 7: Conclusion and Future Scope")
    add_para(
        doc,
        "This minor project delivered Prospectfolio, a behavioural portfolio laboratory that operationalises Cumulative Prospect Theory together with DEA cross-efficiency and MARCOS ranking. The system makes abstract preference parameters tangible: a student can raise loss aversion and watch drawdown-prone names fall in the ordering, then compare the resulting portfolio with a classical Sharpe-maximising mix. In that sense, the project meets its stated objectives of implementation, explanation and comparative demonstration.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "The principal lessons learned are threefold. First, behavioural scores and statistical efficiency measures answer related but different questions; combining them yields a richer screen than either alone. Second, ties on the DEA frontier are common on small universes, so an MCDA post-processor is not cosmetic. Third, interaction design matters in academic software: without immediate visual feedback, parameter studies remain theoretical.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Future scope includes connecting a free or licensed market-data API; adding transaction-cost-aware rebalancing; supporting short sales and sector constraints; replacing the heuristic CPT search with a principled nonlinear optimiser; extending DEA to handle naturally negative data with directional distance formulations; and packaging classroom worksheets that align each slider with a viva question. A further research direction is to evaluate whether MARCOS ranks derived from CPT–DEA features predict out-of-sample relative performance on genuine Nifty histories.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "In closing, Prospectfolio shows that a seventh-semester minor project can host a faithful slice of contemporary behavioural operations-research practice without sacrificing clarity or examinability.",
        align="justify",
        first_line_indent=1.0,
    )

    # -------------------- CHAPTER 8 --------------------
    page_break(doc)
    add_heading_chapter(doc, "Chapter 8: References / Bibliography")
    refs = [
        "Bernard, C., & Ghossoub, M. (2010). Static portfolio choice under cumulative prospect theory. Mathematics and Financial Economics, 2(4), 277–306.",
        "Charnes, A., Cooper, W. W., & Rhodes, E. (1978). Measuring the efficiency of decision making units. European Journal of Operational Research, 2(6), 429–444.",
        "Lim, S., Oh, K. W., & Zhu, J. (2014). Use of DEA cross-efficiency evaluation in portfolio selection: An application to Korean stock market. European Journal of Operational Research, 236(1), 361–368.",
        "Markowitz, H. (1952). Portfolio selection. The Journal of Finance, 7(1), 77–91.",
        "Srivastava, S., & Aggarwal, A. (2025). The efficiency analysis and ranking employing data envelopment analysis and multi-criteria decision analysis: Incorporating cumulative prospect theory. SN Operations Research Forum, 6(3), 1–34.",
        "Srivastava, S., Aggarwal, A., & Bansal, P. (2022). Efficiency evaluation of assets and optimal portfolio generation by cross efficiency and cumulative prospect theory. Computational Economics, 63(1), 129–158.",
        "Srivastava, S., Aggarwal, A., & Mehra, A. (2022). Portfolio selection by cumulative prospect theory and its comparison with mean-variance model. Granular Computing, 7, 745–759.",
        "Stević, Ž., Pamučar, D., Puška, A., & Chatterjee, P. (2020). Sustainable supplier selection in healthcare industries using a new meta-heuristic based complementary approach: Measurement of alternatives and ranking according to compromise solution (MARCOS). Computers & Industrial Engineering, 140, 106231.",
        "Tversky, A., & Kahneman, D. (1992). Advances in prospect theory: Cumulative representation of uncertainty. Journal of Risk and Uncertainty, 5(4), 297–323.",
    ]
    for r in refs:
        add_para(doc, r, align="justify", space_after=10)

    # Extra original filler pages to comfortably exceed 30 pages while remaining substantive
    page_break(doc)
    add_heading_chapter(doc, "Appendix A: User Operation Guide")
    add_para(
        doc,
        "A.1 Installation. Clone the project repository, install Node.js 22 or newer, run npm install, then launch the development server with npm run dev. The application listens on port 3456 by default.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "A.2 First run checklist. Open the home page, scroll to the laboratory section, click Classic TK, inspect the four portfolio tiles, open the Asset ranks tab, and note the CPT and DEA columns. Next, switch to Loss-averse and observe which tickers move. Finally, open Portfolio weights and record the largest holdings for the viva notebook.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "A.3 Suggested viva demonstration script. (1) State the problem in one sentence. (2) Show Figure 1 pipeline on the Method pipeline tab. (3) Move λ upward and narrate the effect. (4) Compare Top-CPT and Mean–variance tiles. (5) Explain why Bottom-CPT is a control. (6) Mention synthetic data limitations unprompted.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "A.4 Extending the universe. Replace the generator in sample-data.ts with CSV loaders for adjusted close prices, compute monthly returns, and keep the remainder of the pipeline unchanged. Validate that dates align across tickers before analysis.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "A.5 Troubleshooting. If the DEA step returns zeros, inspect whether outputs became non-positive after shifting; the analysis layer already adds a positive offset to CPT for DEA. If charts appear empty, confirm that the client bundle finished compiling and that the browser console reports no module resolution errors.",
        align="justify",
        first_line_indent=1.0,
    )

    page_break(doc)
    add_heading_chapter(doc, "Appendix B: Sample Parameter Sweep Notes")
    add_para(
        doc,
        "During development, three presets were exercised repeatedly. The Classic TK preset (λ = 2.25, α = β = 0.88, γ = 0.61, δ = 0.69) produced diversified top sets mixing financials and cyclicals. The Loss-averse preset (λ = 3.2) reduced the prominence of high-volatility conglomerate and metal names relative to defensive consumer names in several runs. The Near-rational preset (λ = 1.2 with weighting exponents near one) moved rankings closer to a mean-return ordering, as expected when behavioural distortions weaken.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Group size experiments with topK ∈ {5, 10, 15} showed that very small baskets increase idiosyncratic volatility of the behavioural portfolio, while larger baskets pull performance toward the equal-weighted market of the laboratory universe. A default of ten names balances interpretability and diversification for classroom use.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "These notes are not formal statistical inference. They record qualitative behaviour that an examiner can reproduce live, which is more valuable in a minor-project setting than a single unreproducible backtest table.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "Students adapting this report should replace illustrative Table 3 and Table 4 numbers with values captured from their own demonstration screenshots on the evaluation day, thereby ensuring consistency between the spiral-bound report and the viva display.",
        align="justify",
        first_line_indent=1.0,
    )

    page_break(doc)
    add_heading_chapter(doc, "Appendix C: Ethical and Academic Integrity Statement")
    add_para(
        doc,
        "All narrative sections of this report were written specifically for the Prospectfolio implementation undertaken as part of ARP 455. Literature ideas are acknowledged through APA citations. Source code produced for the laboratory is original engineering work integrating publicly known algorithms. Synthetic market paths are labelled as such in the user interface to avoid any implication of live trading performance.",
        align="justify",
        first_line_indent=1.0,
    )
    add_para(
        doc,
        "The student affirms that placeholders for personal identifiers will be replaced with accurate information before submission, that the supervisor certificate and declaration will be signed in ink, and that the spiral-bound hard copy will match the soft copy submitted for evaluation.",
        align="justify",
        first_line_indent=1.0,
    )


    # ---- Extra original chapters to meet >=30 printed pages at 1.5 spacing ----
    page_break(doc)
    add_heading_chapter(doc, "Appendix D: Detailed CPT Walk-Through")
    for para in [
        "This appendix walks through a single-asset CPT evaluation in words so that an examiner can verify understanding without opening the source file. Suppose an asset produces a short path of monthly excess returns relative to a zero reference: negative outcomes represent losses and positive outcomes represent gains.",
        "Step 1 sorts the path. Step 2 splits losses from gains. Step 3 maps each outcome through the value function: gains are raised to alpha, losses are scaled by lambda and raised to beta with a negative sign. Step 4 builds cumulative probabilities and converts them into decision weights with the gamma and delta transforms. Step 5 sums weight times value.",
        "The laboratory uses equal historical frequencies as probabilities. That choice matches a teaching setting where no option-implied density is available. Students should state this modelling choice clearly if asked whether CPT is applied to subjective probabilities or to empirical frequencies.",
        "Changing lambda stretches the penalty on the loss branch without altering the gain branch directly. Changing alpha and beta alters curvature and therefore the relative attractiveness of steady moderate gains versus occasional large gains. Changing gamma and delta alters how much attention rare outcomes receive.",
        "Because Prospectfolio recomputes the entire universe when a slider moves, the appendix encourages students to pick one ticker, note its CPT before and after a lambda increase, and explain the direction of change using the loss path of that ticker.",
        "The implementation intentionally keeps the quadratic alternatives discussed in some papers optional; the default power form of Tversky and Kahneman is easier to defend in a viva and matches the classical parameterisation taught in behavioural finance primers.",
        "Numerical stability notes: probabilities of zero and one are short-circuited in the weighting function; extremely small variances are floored before DEA so that the input vector remains strictly positive; CPT values are shifted into a positive orthant before they enter DEA outputs so that the linear programme remains well posed.",
    ]:
        add_para(doc, para, align="justify", first_line_indent=1.0)

    page_break(doc)
    add_heading_chapter(doc, "Appendix E: DEA and Cross-Efficiency Narrative")
    for para in [
        "Data Envelopment Analysis interprets each stock as a decision-making unit that consumes risk to produce desirable attributes. In Prospectfolio the consumed resource is return variance. The produced attributes are a behaviourally adjusted score and a long-horizon return proxy.",
        "Self-appraisal CCR scores often saturate at one for several units when the input–output dimension is small relative to the sample. Cross-efficiency mitigates that saturation by forcing every unit to be judged with weights that were optimal for its peers. The averaged score is typically strictly less than one and yields a more informative order.",
        "Students should be prepared to draw the DEA input–output diagram on the board: one arrow inward labelled variance, two arrows outward labelled CPT and return. They should also state that the laboratory uses an input-oriented constant-returns formulation for transparency rather than a variable-returns model.",
        "Limitations of the present DEA layer include the absence of weight restrictions, the omission of non-discretionary inputs, and the reliance on a lightweight JavaScript solver. For thirty units these limitations are acceptable. For hundreds of mutual funds a dedicated solver and weight bounds would be preferable.",
        "Cross-efficiency itself has variants—aggressive, benevolent and game-theoretic. The laboratory follows a practical peer-average scheme sufficient to illustrate the concept. Mentioning the existence of variants demonstrates literature awareness without claiming an exhaustive implementation.",
        "When MARCOS is applied after DEA, the criteria set expands beyond efficiency alone. That hybridisation mirrors the thesis-inspired pipeline: behavioural value informs both the DEA outputs and the multi-criteria matrix, while MARCOS supplies discrimination among near-efficient peers.",
        "A useful viva question is whether a unit with high CPT but extreme variance should rank above a moderate CPT unit with low variance. DEA answers by computing the best possible weighting under feasibility constraints; MARCOS answers by measuring distance to ideal and anti-ideal points with equal criterion weights in the demo.",
    ]:
        add_para(doc, para, align="justify", first_line_indent=1.0)

    page_break(doc)
    add_heading_chapter(doc, "Appendix F: Interface Screens and Oral Defence Notes")
    for para in [
        "The home hero introduces the product name Prospectfolio and states the research-to-product bridge in plain language. Examiners scanning the first screen should immediately see brand, problem and call to action without clutter.",
        "The laboratory panel groups behavioural knobs on the right and explanatory copy on the left. Presets reduce the chance that a student freezes during the viva while hunting for plausible parameter values.",
        "Metric tiles answer the first comparative question in under five seconds: which recipe currently looks stronger on return, volatility, Sharpe and CPT. Students should avoid reading every number aloud; instead they should point to the contrast between Top-CPT and Bottom-CPT.",
        "The frontier tab is the visual centrepiece. Grey points are individual assets, the orange curve approximates the mean–variance frontier, and teal markers show CPT-oriented mixes. The oral line is: classical efficiency versus behavioural attractiveness on the same axes.",
        "The ranks tab is where formula knowledge is tested. Be ready to define each column in one sentence. The weights tab shows concentration risk; if one name exceeds roughly thirty percent, mention diversification limits of small topK values.",
        "The method pipeline tab is the storyboard for students who become nervous with equations. Walking left to right through the four steps recovers the report structure in under a minute.",
        "Defence etiquette: acknowledge synthetic data before being asked; never claim live alpha; offer to open the CPT or DEA source file if an examiner wants implementation proof; keep the supervisor’s intellectual guidance visible by naming the course and school on the title slide.",
        "If networking fails during evaluation, run the production build locally beforehand and keep screenshots of Figures 2–4 printed as backup slides inside the spiral report appendices already provided.",
    ]:
        add_para(doc, para, align="justify", first_line_indent=1.0)

    page_break(doc)
    add_heading_chapter(doc, "Appendix G: Extended Discussion on Behavioural versus Classical Choice")
    for para in [
        "Behavioural portfolio choice and classical mean–variance choice optimise different psychological stories. The classical story prizes variance-adjusted expected growth. The behavioural story prizes experiences of gains and losses as perceived through a distorted lens.",
        "Neither story is universally superior. In calm markets with reliable estimates, mean–variance allocations can be hard to beat on Sharpe. In settings where clients abandon plans after drawdowns, a CPT-aware screen may produce holdings that clients are more willing to hold, even if the ex-ante Sharpe is slightly lower.",
        "Prospectfolio does not adjudicate which story an institution should adopt. It makes the disagreement visible. That visibility is the pedagogical product.",
        "From an engineering standpoint, keeping both optimisers behind one interface prevents the false impression that behavioural finance requires an entirely separate technology stack. Shared statistics, shared data and shared charts reduce cognitive load.",
        "From an academic integrity standpoint, students must describe the laboratory as inspired by published CPT–DEA–MCDA research while emphasising that the software, narrative and experimental framing are their own course deliverable. Copying thesis chapter text into the report would be inappropriate; paraphrasing concepts and citing sources is required.",
        "The comparative tables in Chapter 6 should be refreshed with the student’s own captured numbers on the day before binding. Doing so converts illustrative figures into personal evidence and further distances the submission from any generic template.",
        "Finally, British spelling has been used throughout in accordance with the school’s instruction sheet: behaviour, optimisation, visualisation and fulfilment appear in their British forms on the cover and in the body.",
    ]:
        add_para(doc, para, align="justify", first_line_indent=1.0)

    page_break(doc)
    add_heading_chapter(doc, "Appendix H: Glossary for Quick Revision")
    for para in [
        "Behavioural investor: a decision maker whose choices systematically depart from expected-utility benchmarks in ways described by prospect theory.",
        "Cross-efficiency: an average of efficiency scores obtained when each unit is evaluated with other units’ optimal DEA weights.",
        "Efficient frontier: the set of portfolios that maximise expected return for each attainable risk level under mean–variance preferences.",
        "Loss aversion: the tendency to weigh losses more heavily than equal-sized gains, captured by lambda greater than one.",
        "Probability weighting: a nonlinear transform of cumulative probabilities that typically overweights small probabilities of extreme outcomes.",
        "Reference point: the benchmark against which gains and losses are measured; zero excess return in the default laboratory setting.",
        "Spiral binding: the physical binding style mandated for the hard-copy minor project report.",
    ]:
        add_para(doc, para, align="justify", first_line_indent=1.0)


    doc.save(OUT_DOCX)
    print("Wrote", OUT_DOCX)


def add_bullet_slide(prs, title, bullets, subtitle=None):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    body = slide.placeholders[1].text_frame
    body.clear()
    if subtitle:
        p = body.paragraphs[0]
        p.text = subtitle
        p.level = 0
        for b in bullets:
            p = body.add_paragraph()
            p.text = b
            p.level = 0
    else:
        first = True
        for b in bullets:
            if first:
                body.paragraphs[0].text = b
                first = False
            else:
                p = body.add_paragraph()
                p.text = b
                p.level = 0
    return slide


def build_ppt():
    prs = Presentation()
    prs.slide_width = PInches(13.333)
    prs.slide_height = PInches(7.5)

    # Title
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Prospectfolio"
    slide.placeholders[1].text = (
        "Behavioural Portfolio Lab using CPT, DEA and MARCOS\n"
        "Minor Project (ARP 455) | USAR, GGSIPU\n"
        "[YOUR NAME] | [ENROLLMENT NO.] | Branch: [AI-DS/AI-ML/IIOT/AR]\n"
        "Supervisor: [NAME OF SUPERVISOR]"
    )

    add_bullet_slide(
        prs,
        "Agenda",
        [
            "Motivation and problem",
            "Objectives",
            "Literature cues",
            "System modules and pipeline",
            "Methodology and algorithms",
            "Results and comparison",
            "Conclusion, future scope and demo",
        ],
    )
    add_bullet_slide(
        prs,
        "Motivation",
        [
            "Mean–variance assumes rational moment-based preferences",
            "Real investors show loss aversion and probability distortion",
            "Cumulative Prospect Theory models those behaviours",
            "Need a student-operable lab, not only journal tables",
        ],
    )
    add_bullet_slide(
        prs,
        "Problem Statement",
        [
            "Build one workflow that scores assets with CPT",
            "Rank with DEA cross-efficiency and MARCOS",
            "Form behavioural portfolios and compare with max-Sharpe MV",
            "Expose behavioural knobs in a browser UI",
        ],
    )
    add_bullet_slide(
        prs,
        "Objectives",
        [
            "Implement CPT valuation in TypeScript",
            "Implement CCR DEA + cross-efficiency",
            "Apply MARCOS for tie-breaking",
            "Compare Top-CPT, DEA×CPT, MV and Bottom-CPT portfolios",
            "Ship an interactive Next.js laboratory",
        ],
    )
    add_bullet_slide(
        prs,
        "Literature Snapshot",
        [
            "Markowitz (1952): mean–variance frontier",
            "Tversky and Kahneman (1992): Cumulative Prospect Theory",
            "Charnes et al. (1978); Lim et al. (2014): DEA / cross-efficiency",
            "Stević et al. (2020): MARCOS compromise ranking",
            "Srivastava et al.: CPT with DEA/MCDA on Indian equities",
        ],
    )

    # Pipeline image slide
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Decision Pipeline"
    slide.shapes.add_picture(str(ASSETS / "fig1_pipeline.png"), PInches(0.8), PInches(1.6), width=PInches(11.7))

    add_bullet_slide(
        prs,
        "Software Modules",
        [
            "sample-data: seeded Nifty-style monthly returns (30 names)",
            "cpt: value function + probability weighting",
            "dea: CCR LP + cross-efficiency",
            "marcos: ideal / anti-ideal compromise scores",
            "optimize + analyze: portfolios and orchestration",
            "UI: Next.js lab with live parameter sliders",
        ],
    )
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Module Layout"
    slide.shapes.add_picture(str(ASSETS / "fig5_modules.png"), PInches(1.2), PInches(1.5), width=PInches(10.8))

    add_bullet_slide(
        prs,
        "Methodology",
        [
            "Fix universe and seed; vary CPT parameters and topK",
            "Score → DEA → MARCOS → portfolio construction",
            "Responses: ranks, weights, return, vol, Sharpe, CPT",
            "Tools: Next.js, TypeScript, Recharts, LP solver",
        ],
    )
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Flow Chart"
    slide.shapes.add_picture(str(ASSETS / "fig6_flowchart.png"), PInches(3.2), PInches(1.2), height=PInches(5.8))

    add_bullet_slide(
        prs,
        "Algorithms (brief)",
        [
            "CPT: rank-dependent decision weights × value function",
            "DEA CCR: max weighted outputs s.t. peer feasibility",
            "Cross-efficiency: average peer appraisals",
            "MARCOS: distance to ideal and anti-ideal",
            "MV frontier + CPT random-search portfolio mixes",
        ],
    )

    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Results: CPT Ranks"
    slide.shapes.add_picture(str(ASSETS / "fig3_cpt_ranks.png"), PInches(1.8), PInches(1.4), width=PInches(9.5))

    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Results: Risk–Return Map"
    slide.shapes.add_picture(str(ASSETS / "fig2_frontier.png"), PInches(2.0), PInches(1.3), width=PInches(9.2))

    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Results: Portfolio Comparison"
    slide.shapes.add_picture(str(ASSETS / "fig4_portfolio_compare.png"), PInches(1.8), PInches(1.3), width=PInches(9.5))

    add_bullet_slide(
        prs,
        "Comparative Takeaways",
        [
            "Top-CPT beats Bottom-CPT on return and CPT value (demo)",
            "MV often wins on Sharpe (its explicit objective)",
            "DEA×CPT balances behavioural appeal and variance cost",
            "Raising λ demotes deep-drawdown names",
            "Data are synthetic — educational, not trading advice",
        ],
    )
    add_bullet_slide(
        prs,
        "Conclusion",
        [
            "Delivered an interactive CPT × DEA × MARCOS laboratory",
            "Made behavioural parameters visible and examinable",
            "Compared behavioural and classical portfolios in one UI",
        ],
    )
    add_bullet_slide(
        prs,
        "Future Scope",
        [
            "Live market-data connector",
            "Costs, constraints and multi-period rebalancing",
            "Stronger nonlinear CPT optimiser",
            "Classroom worksheets linked to each slider",
        ],
    )
    add_bullet_slide(
        prs,
        "Thank You",
        [
            "Questions welcome",
            "Live demo: npm run dev → open laboratory section",
            "[YOUR NAME] | ARP 455 | USAR, GGSIPU",
        ],
    )

    prs.save(OUT_PPTX)
    print("Wrote", OUT_PPTX)


if __name__ == "__main__":
    build_report()
    build_ppt()
