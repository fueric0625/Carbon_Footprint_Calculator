# -*- coding: utf-8 -*-
"""Rebuild the Milestone 3a logs with a dated post-review section.

The originals are PDFs with no editable source, so both logs are rebuilt from
their recorded text. Nothing in the 2026-11-09 record is altered; a new dated
section is appended to each.
"""
import io
import os
import shutil

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONT = "Arial"
INK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x59, 0x59, 0x59)


def new_doc():
    d = Document()
    sec = d.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(2.2)
    sec.right_margin = Cm(2.2)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    st = d.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(10)
    st.font.color.rgb = INK
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.line_spacing = 1.15
    return d


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.makeelement(qn("w:shd"), {
        qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): hex_fill})
    tcPr.append(shd)


def para(doc, txt, size=10, bold=False, color=INK, before=0, after=4, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(txt)
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return p


def cell_text(cell, chunks, size=10):
    """chunks: list of (text, bold) tuples, rendered as paragraphs."""
    cell.text = ""
    first = True
    for txt, bold in chunks:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(txt)
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = bold


def grid(doc, rows, widths, header=False, label_col=True):
    t = doc.add_table(rows=0, cols=len(widths))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
    for row in rows:
        cells = t.add_row().cells
        trPr = t.rows[-1]._tr.get_or_add_trPr()
        trPr.append(trPr.makeelement(qn("w:cantSplit"), {}))
        for i, val in enumerate(row):
            cells[i].width = Cm(widths[i])
            chunks = val if isinstance(val, list) else [(val, False)]
            cell_text(cells[i], chunks)
            if label_col and i == 0:
                shade(cells[i], "F2F2F2")
    for r in t.rows:
        for i, c in enumerate(r.cells):
            c.width = Cm(widths[i])
    return t


def rule(doc, before=8, after=8):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    pPr = p._p.get_or_add_pPr()
    bdr = pPr.makeelement(qn("w:pBdr"), {})
    bottom = bdr.makeelement(qn("w:bottom"), {
        qn("w:val"): "single", qn("w:sz"): "6", qn("w:space"): "1",
        qn("w:color"): "BFBFBF"})
    bdr.append(bottom)
    pPr.append(bdr)


# ------------------------------------------------------------------ content
REVISIT_A = (
    "Li Ming still needs to see his footprint for one teaching semester, which "
    "activities are counted, which are left out, and which number he can change "
    "to lower the result. This revisit adds two needs. He needs to see that the "
    "semester length is an assumption, not a fact from the shared profile, and "
    "he needs the headline to separate sourced kg CO₂ from unverified kg CO₂e."
)

F1 = [
    ("What We Found",
     "Weekly and monthly activities are scaled by a fixed 18-week semester. The "
     "page does not let Li Ming change that number. If the semester is shorter, "
     "food and city travel should fall, while high-speed rail should stay the same."),
    ("Evidence and Role Code(s)",
     "Prototype 1 stores the period as constants: 18 weeks, 4.5 months, and 126 "
     "electricity days. Metro kilometres and meal counts are multiplied by 18. "
     "High-speed rail is already entered per teaching semester. Role codes: C, U."),
    ("What We Decided to Do and Why",
     "Add an editable field, “Weeks in a teaching semester”, default 18. Weekly "
     "activities use this number. Monthly activities use 1 month = 4 weeks, so "
     "months equal weeks divided by 4. Electricity days equal weeks times 7. "
     "High-speed rail and clothing stay per semester. The note states that 18 "
     "weeks is an assumption. Reset returns the field to 18."),
]

F2 = [
    ("What We Found",
     "The headline is written as kg CO₂e, but the total mixes units. Electricity "
     "and high-speed rail use sourced kg CO₂ factors. The other quantified items, "
     "including food, still use unverified kg CO₂e. With the default profile, beef "
     "or lamb is about 324 kg and fills the top suggestions, even though those "
     "per-meal factors have no meal weight."),
    ("Evidence and Role Code(s)",
     "Prototype 1 cites electricity at 0.5737 kg CO₂/kWh and high-speed rail at "
     "0.02709 kg CO₂/passenger·km. Food, metro, and ride-hailing remain marked "
     "“not yet verified”. The ride-hailing suggestion also called 0.20 kg/km a "
     "per-passenger factor. Role codes: C, R."),
    ("What We Decided to Do and Why",
     "Change the headline to a reported mixed total. Show sourced kg CO₂ and "
     "unverified kg CO₂e on separate lines. If a suggestion uses an unverified "
     "per-meal factor, say the comparison is illustrative because the profile "
     "gives no meal weight. State the ride-hailing factor as kg/km. Do not invent "
     "a meal weight, and do not add showers, parcels, clothing, or waste to the total."),
]

C_TEXT = (
    "The final calculator addresses these two findings first: an editable "
    "teaching-semester length, then a mixed-unit result label with the suggestion "
    "caveat. No other scope was added."
)

REVISIT_D = [
    ("Why this section exists",
     "Between the review and the submission, the page was revised again on "
     "2026-11-10. None of it changes the boundary or the categories, so the "
     "decision recorded in section C still holds. It is recorded here so the "
     "final calculator and this log describe the same file."),
    ("Food rows rebuilt (role code C)",
     "Each food row is now meals per week × a portion in grams × a factor per "
     "kilogram of food, instead of one figure per meal. The four default portions "
     "are 100, 250, 400, and 400 g, which reproduce the previous per-meal values "
     "exactly: 324, 216, 72, and 36 kg. The default result is therefore unchanged."),
    ("The meal weight is now an input (role codes C, R)",
     "Finding 2 said the profile gives no meal weight and that we should not "
     "invent one. The portion is now an editable field labelled as an assumption, "
     "so the weight is visible and can be changed rather than hidden inside a "
     "per-meal factor. This settles Finding 2 without asserting a weight as fact."),
    ("Presentation changed (role code U)",
     "The page was restyled to match the slides, the copy was shortened, each step "
     "gained an icon, and each category on the results page links back to its step. "
     "No input, factor, or boundary was added or removed."),
    ("Test result, 2026-11-10",
     "Default: 783.7 kg reported, food 648.0 kg, food mass 113.4 kg. Beef "
     "suggestion −159.3 kg to 624.4 kg; other meat −90.0 kg to 693.7 kg; "
     "electricity unchanged at −14.5 kg to 769.3 kg. The beef figure moved only "
     "because the portion is explicit: 27 meals × 100 g × (60 − 1) kg CO₂e/kg."),
]

AI_INTRO = (
    "Prototype 1 was copied to Group9_Final_Calculator.html and was not "
    "overwritten. Each round below is one accepted change. The prompts are the key "
    "instructions given to the tool. The test results were checked in the browser "
    "after the page was built."
)

R1 = [
    ("Issue and Intended Improvement",
     "Prototype 1 multiplies weekly and monthly activities by a fixed 18 weeks and "
     "4.5 months. Li Ming cannot see that this length is an assumption, and he "
     "cannot try another semester length. High-speed rail and clothing are already "
     "per semester and should not be scaled again."),
    ("Exact Key Prompt(s)",
     "From Prototype 1, add an editable field “Weeks in a teaching semester”, "
     "default 18. Multiply weekly activities by this number. Convert monthly "
     "activities with 1 month = 4 weeks, so months in the semester equal weeks "
     "divided by 4. Electricity days equal weeks times 7. Do not multiply "
     "high-speed rail or clothing. Label the semester length as an assumption, not "
     "a shared-profile fact. Reset restores 18 weeks and Li Ming’s defaults."),
    ("Group Decision and Revision",
     "Accepted. The field was added on the energy step of "
     "Group9_Final_Calculator.html. The note states the assumption, the month rule, "
     "and that high-speed rail and clothing stay per semester."),
    ("Test Result or Remaining Issue",
     "With the default 18 weeks, the reported total is 783.7 kg. Metro is 540.0 "
     "km/semester and high-speed rail is 880.0 km/semester. After the weeks field "
     "is changed to 16, the reported total falls to 699.3 kg, metro falls to 480.0 "
     "km, beef or lamb falls from 54.0 to 48.0 meals, and electricity is scaled to "
     "112 days. High-speed rail stays 880.0 km. Reset returns the weeks field to 18 "
     "and the total to 783.7 kg."),
]

R2 = [
    ("Issue and Intended Improvement",
     "Prototype 1 labels the headline kg CO₂e, but electricity and high-speed rail "
     "are sourced kg CO₂, while food and the other city modes are unverified kg "
     "CO₂e. Beef or lamb is about 324 kg under the default profile, so food "
     "suggestions look like a verified ranking even though the profile gives no "
     "meal weight. The ride-hailing suggestion also used the wrong unit."),
    ("Exact Key Prompt(s)",
     "Change the results headline so it is a mixed reported total, not a complete "
     "CO₂e figure. Show sourced kg CO₂ for electricity and high-speed rail "
     "separately from unverified kg CO₂e for the other quantified activities. If a "
     "reduction suggestion uses an unverified per-meal factor, say the comparison "
     "is illustrative because the profile gives no meal weight. State the "
     "ride-hailing factor as 0.20 kg/km, not kg per passenger-kilometre. Do not "
     "invent a meal weight, and do not add showers, parcels, clothing, or waste to "
     "the total."),
    ("Group Decision and Revision",
     "Accepted. The headline now reads “kg reported / teaching semester”. Sourced "
     "CO₂ and unverified CO₂e are listed separately. Food and unverified transport "
     "suggestions say the comparison is illustrative. The electricity suggestion "
     "stays in kg CO₂. Shared-profile defaults were not changed."),
    ("Test Result or Remaining Issue",
     "At the default 18 weeks, the results page shows 783.7 kg reported / teaching "
     "semester. It then states: sourced kg CO₂ is electricity 72.3 kg and "
     "high-speed rail 23.8 kg, together 96.1 kg; unverified kg CO₂e for the other "
     "quantified activities is 687.6 kg. The beef suggestion says the comparison "
     "uses unverified per-meal factors and is illustrative. The electricity "
     "suggestion uses kg CO₂ and does not use that caveat. Showers, parcels, "
     "clothing, and waste remain outside the total."),
]

R3 = [
    ("Issue and Intended Improvement",
     "Revision 2 left the meal factor as a figure per meal and stated that the "
     "profile gives no meal weight. That left the largest block of the result, 648 "
     "kg or 83 per cent of the total, on a unit no published factor uses, and it "
     "could not be improved without stating a weight. The page was also long and "
     "dark to read on a projector."),
    ("Exact Key Prompt(s)",
     "Rebuild the food rows as meals per week × a portion in grams × a factor per "
     "kilogram of food. Make the portion an editable input, default 100 / 250 / "
     "400 / 400 g, so the default result stays 783.7 kg. Label the portions as "
     "assumptions and update the factor table to per-kilogram units. Then restyle "
     "the page on the same palette as the slides, shorten the copy, add an icon per "
     "step, and let each category on the results page jump back to its step."),
    ("Group Decision and Revision",
     "Accepted. The food model is portion-based; the portion is labelled an "
     "assumption and is not a profile fact. The factor table now gives per-kilogram "
     "factors marked provisional. The page was restyled, the copy shortened, and an "
     "Edit link added per category. Nothing was added to the boundary: no new "
     "category, no new factor."),
    ("Test Result or Remaining Issue",
     "2026-11-10: default total 783.7 kg, food 648.0 kg, food mass 113.4 kg. Beef "
     "suggestion −159.3 kg to 624.4 kg; other meat −90.0 kg to 693.7 kg; "
     "electricity unchanged at −14.5 kg to 769.3 kg. Raising the beef portion to "
     "200 g moves food to 972.0 kg, as expected. Remaining issue: the per-kilogram "
     "factors are still provisional, and food, metro, and ride-hailing still have "
     "no published source — the same disclosure as before, now stated per kilogram."),
]


# ------------------------------------------------------------------ builders
def build_revisit(path):
    d = new_doc()
    para(d, "Revisit 2 Review Log", size=17, bold=True, after=10)

    grid(d, [[[("Group No.: ", True), ("9", False)],
              [("Calculator Version Reviewed: ", True), ("Prototype 1", False)],
              [("Date: ", True), ("2026-11-09", False)]]],
         widths=[5.6, 7.4, 3.6], label_col=False)

    para(d, "Use the role sheets and the Master Group Worksheet to summarize the "
            "group’s main decisions. Do not copy every observation from the role "
            "sheets.", size=9, color=GREY, before=6, after=10)

    para(d, "A   Client Needs Update", size=11.5, bold=True, before=6, after=4)
    grid(d, [[REVISIT_A]], widths=[16.6], label_col=False)

    para(d, "B   Review Findings and Decisions", size=11.5, bold=True, before=14, after=2)
    para(d, "Summarize the most important findings. Use specific evidence rather "
            "than copying the full role worksheets.", size=9, color=GREY, after=8)

    for i, finding in enumerate((F1, F2), start=1):
        para(d, "Finding %d" % i, size=10.5, bold=True, before=8, after=4)
        grid(d, [[[(lab, True)], [(txt, False)]] for lab, txt in finding],
             widths=[4.4, 12.2])

    para(d, "Role codes: U Client/User   F Product Function and Stability   "
            "C Carbon Accounting   R Results and Reduction Guidance",
         size=8.5, color=GREY, before=6, after=10)

    para(d, "C   Priority Revisions", size=11.5, bold=True, before=6, after=4)
    grid(d, [[C_TEXT]], widths=[16.6], label_col=False)

    rule(d, before=14, after=6)
    para(d, "D   Post-review changes, 2026-11-10", size=11.5, bold=True, after=2)
    para(d, "Appended after the review session. The 2026-11-09 record above is "
            "unchanged.", size=9, color=GREY, after=8)
    grid(d, [[[(lab, True)], [(txt, False)]] for lab, txt in REVISIT_D],
         widths=[4.4, 12.2])

    d.save(path)
    return path


def build_ai(path):
    d = new_doc()
    para(d, "AI Interaction 2 Log", size=17, bold=True, after=10)

    grid(d, [[[("Group No.: ", True), ("9", False)],
              [("Version Before Revision: ", True), ("Prototype 1", False)],
              [("AI Tool(s): ", True), ("Cursor (Grok); AI coding agent for Revision 3", False)],
              [("Date: ", True), ("2026-11-09, 2026-11-10", False)]]],
         widths=[3.6, 5.2, 5.6, 4.2], label_col=False)

    para(d, AI_INTRO, size=9.5, color=GREY, before=6, after=10)

    for i, rev in enumerate((R1, R2, R3), start=1):
        para(d, "Key AI-Assisted Revision %d" % i, size=11.5, bold=True,
             before=10, after=4)
        if i == 3:
            para(d, "Post-review, 2026-11-10", size=9, color=GREY, after=4)
        t = grid(d, [[[(lab, True)], [(txt, False)]] for lab, txt in rev],
                 widths=[4.4, 12.2])
        # the prompt row reads as a quoted instruction: light grey fill
        for c in t.rows[1].cells:
            shade(c, "F7F7F7")

    d.save(path)
    return path


if __name__ == "__main__":
    os.makedirs(r"logs\src", exist_ok=True)
    os.makedirs(r"logs\.backup", exist_ok=True)
    for src in ("Group9_M3a_Revisit2_Log.pdf", "Group9_M3a_AI2_Log.pdf"):
        p = os.path.join("logs", src)
        if os.path.exists(p):
            shutil.copy2(p, os.path.join("logs", ".backup", src))
    print(build_revisit(r"logs\src\Group9_M3a_Revisit2_Log.docx"))
    print(build_ai(r"logs\src\Group9_M3a_AI2_Log.docx"))
