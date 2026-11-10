# -*- coding: utf-8 -*-
"""Build the Group 9 roadshow deck.

Design system (shared with calculators/Group9_Final_Calculator.html):
  paper  #FBFBF8   ink  #131A17   soft #46524C   muted #6E7A73
  line   #E1E4DD   green #1B6B4F  amber #A9642B  blue #38699B
  Display type: Georgia.  UI/body type: Segoe UI.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from lxml import etree
import re

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P_NS = "{http://schemas.openxmlformats.org/presentationml/2006/main}"

PAPER = RGBColor(0xFB, 0xFB, 0xF8)
INK = RGBColor(0x13, 0x1A, 0x17)
SOFT = RGBColor(0x46, 0x52, 0x4C)
MUTED = RGBColor(0x6E, 0x7A, 0x73)
LINE = RGBColor(0xE1, 0xE4, 0xDD)
GREEN = RGBColor(0x1B, 0x6B, 0x4F)
AMBER = RGBColor(0xA9, 0x64, 0x2B)
BLUE = RGBColor(0x38, 0x69, 0x9B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TINT_AMBER = RGBColor(0xFA, 0xF3, 0xEA)
TINT_GREEN = RGBColor(0xEF, 0xF5, 0xF1)

DISPLAY = "Georgia"
UI = "Segoe UI"

W, H = 13.333, 7.5
M = 0.9
CW = W - 2 * M


def deck():
    p = Presentation()
    p.slide_width = Inches(W)
    p.slide_height = Inches(H)
    return p


def blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = PAPER
    return s


def tb(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    bodyPr = tf._txBody.find(A + "bodyPr")
    for tag in ("normAutofit", "spAutoFit"):
        el = bodyPr.find(A + tag)
        if el is not None:
            bodyPr.remove(el)
    if bodyPr.find(A + "noAutofit") is None:
        etree.SubElement(bodyPr, A + "noAutofit")
    return box


def para(tf, first=False):
    return tf.paragraphs[0] if first else tf.add_paragraph()


def run(p, text_, font=UI, size=14, color=INK, bold=False, spc=None, italic=False):
    r = p.add_run()
    r.text = text_
    f = r.font
    f.name = font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    if spc is not None:
        f._rPr.set("spc", str(int(spc)))
    return r


def text(slide, x, y, w, h, chunks, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT,
         line_spacing=None, space_after=None):
    box = tb(slide, x, y, w, h, anchor)
    tf = box.text_frame
    for i, ch in enumerate(chunks):
        p = para(tf, first=(i == 0))
        p.alignment = align
        if line_spacing is not None:
            p.line_spacing = line_spacing
        if space_after is not None:
            p.space_after = Pt(space_after)
        for spec in (ch.get("runs") if "runs" in ch else [ch]):
            seg_runs(p, spec.get("t", ""),
                     **{k: v for k, v in spec.items() if k != "t"})
    return box


def seg_runs(p, s, **kw):
    """Split out the subscript digits: Georgia has no U+2082, Segoe UI does."""
    for part in re.split(r"(₂)", s):
        if not part:
            continue
        if part == "₂":
            sub = dict(kw)
            sub["font"] = UI
            run(p, part, **sub)
        else:
            run(p, part, **kw)


def _plain(shp):
    """Drop the theme shape style so no inherited shadow or outline appears."""
    style = shp._element.find(P_NS + "style")
    if style is not None:
        shp._element.remove(style)
    shp.shadow.inherit = False
    return shp


def rule(slide, x, y, w, color=LINE, weight=1.0):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                 Inches(w), Pt(weight))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return _plain(shp)


def vrule(slide, x, y, h, color=LINE, weight=1.0):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                 Pt(weight), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return _plain(shp)


def block(slide, x, y, w, h, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                 Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return _plain(shp)


def chrome(slide, n, kicker, headline, headline_size=33):
    text(slide, M, 0.52, 6.4, 0.22,
         [{"t": kicker, "size": 9.5, "bold": True, "color": GREEN, "spc": 170}])
    text(slide, M, 0.80, CW - 1.2, 0.72,
         [{"t": headline, "font": DISPLAY, "size": headline_size, "color": INK}],
         line_spacing=1.06)
    text(slide, W - M - 1.0, 0.52, 1.0, 0.22,
         [{"t": "%02d" % n, "size": 9.5, "bold": True, "color": MUTED, "spc": 120}],
         align=PP_ALIGN.RIGHT)


def label(slide, x, y, w, t, color=MUTED):
    text(slide, x, y, w, 0.2,
         [{"t": t, "size": 9, "bold": True, "color": color, "spc": 150}])


def footnote(slide, t):
    rule(slide, M, 6.18, CW)
    text(slide, M, 6.33, CW - 0.6, 0.4,
         [{"t": t, "font": UI, "size": 13, "color": SOFT}])


# ---------------------------------------------------------------- slide 1
def s1(prs):
    s = blank(prs)
    text(s, M, 1.05, 7.0, 0.22,
         [{"t": "GROUP 9  ·  SDG2410J  ·  CARBON ACCOUNTING", "size": 9.5,
           "bold": True, "color": GREEN, "spc": 170}])
    text(s, M, 1.55, 7.3, 2.6,
         [{"t": "Li Ming’s personal carbon footprint", "font": DISPLAY,
           "size": 50, "color": INK}], line_spacing=1.02)
    text(s, M, 4.12, 7.3, 0.45,
         [{"t": "One teaching semester", "font": UI, "size": 21, "color": SOFT}])
    rule(s, M, 4.95, 7.1)
    text(s, M, 5.15, 7.0, 0.9,
         [{"t": "What is counted, what is left out, and which numbers have a source.",
           "font": UI, "size": 15, "color": SOFT}], line_spacing=1.35)

    x = 8.55
    rows = [("783.7 kg", "reported per teaching semester"),
            ("96.1 kg", "carries a published CO₂ factor"),
            ("687.6 kg", "no published source yet")]
    y = 2.35
    rule(s, x, y - 0.22, 3.88)
    for i, (big, small) in enumerate(rows):
        text(s, x, y, 3.88, 0.5,
             [{"t": big, "font": UI, "size": 27, "bold": True, "color": INK}])
        text(s, x, y + 0.47, 3.88, 0.3,
             [{"t": small, "font": UI, "size": 11.5, "color": MUTED}])
        y += 1.02
        if i < len(rows) - 1:
            rule(s, x, y - 0.16, 3.88)
    text(s, W - M - 1.0, H - 0.62, 1.0, 0.22,
         [{"t": "01", "size": 9.5, "bold": True, "color": MUTED, "spc": 120}],
         align=PP_ALIGN.RIGHT)


# ---------------------------------------------------------------- slide 2
def s2(prs):
    s = blank(prs)
    chrome(s, 2, "WHY  ·  LECTURES 1 AND 2", "Two things he needs from the result")

    rule(s, M, 2.08, CW)
    label(s, M, 2.28, 1.5, "NEED 01", GREEN)
    text(s, M + 1.55, 2.21, 9.5, 0.45,
         [{"t": "A semester, not only a total", "font": DISPLAY, "size": 24,
           "color": INK}])
    text(s, M + 1.55, 2.78, 9.3, 1.0,
         [{"t": "Lecture 1 set 3.84 and 2.54 t CO₂e per student per year side by side. "
                "They cannot be ranked until the unit and the boundary match.",
           "font": UI, "size": 14.5, "color": SOFT}], line_spacing=1.4)
    text(s, M + 1.55, 3.70, 9.3, 0.3,
         [{"t": "Sanity check: two 18-week semesters is about 1.6 t — below both.",
           "font": UI, "size": 11.5, "bold": True, "color": GREEN}])

    rule(s, M, 4.30, CW)
    label(s, M, 4.50, 1.5, "NEED 02", GREEN)
    text(s, M + 1.55, 4.43, 9.5, 0.45,
         [{"t": "A comparison he is allowed to trust", "font": DISPLAY, "size": 24,
           "color": INK}])
    text(s, M + 1.55, 5.00, 9.3, 1.0,
         [{"t": "Electricity and high-speed rail have published CO₂ factors. "
                "Food, metro, and ride-hailing do not. A large unverified number "
                "must not outrank a sourced one.",
           "font": UI, "size": 14.5, "color": SOFT}], line_spacing=1.4)

    footnote(s, "Both needs point the same way: a sourced number and an "
                "unverified one never share a headline.")


# ---------------------------------------------------------------- slide 3
def s3(prs):
    s = blank(prs)
    chrome(s, 3, "WHAT  ·  LECTURES 9 AND 10", "The result is one stated service")

    y = 2.45
    blocks = [
        (M, 3.00, "ACTIVITY DATA", "metro trips × km", "kept in the profile’s own unit", LINE),
        (4.42, 3.02, "EMISSION FACTOR", "kg CO₂e per unit", "matched to place, year, technology", LINE),
        (8.20, 4.20, "RESULT", "one teaching semester", "not a year, not a week", GREEN),
    ]
    for bx, bw, lab, big, small, col in blocks:
        rule(s, bx, y, bw, col, 1.4 if col is GREEN else 1.0)
        label(s, bx, y + 0.18, bw, lab, GREEN if col is GREEN else MUTED)
        text(s, bx, y + 0.46, bw, 0.45,
             [{"t": big, "font": UI, "size": 18, "bold": True, "color": INK}])
        text(s, bx, y + 0.95, bw, 0.55,
             [{"t": small, "font": UI, "size": 11.5, "color": MUTED}], line_spacing=1.3)

    text(s, 4.05, 2.96, 0.3, 0.35, [{"t": "×", "font": UI, "size": 22, "color": MUTED}])
    text(s, 7.84, 2.96, 0.3, 0.35, [{"t": "=", "font": UI, "size": 22, "color": MUTED}])

    rule(s, M, 4.55, CW)
    text(s, M, 4.78, 5.35, 1.2,
         [{"t": "A product result is reported per functional unit, not as the weight "
                "of what was consumed. The BMW vehicle study uses 200,000 km.",
           "font": UI, "size": 14, "color": SOFT}], line_spacing=1.4)
    text(s, 6.85, 4.78, 5.35, 1.2,
         [{"t": "This profile never says how many semesters make a year, so nothing "
                "in the file is multiplied by 52.",
           "font": UI, "size": 14, "color": SOFT}], line_spacing=1.4)

    footnote(s, "Every counted row is converted onto that semester before "
                "anything is added.")


# ---------------------------------------------------------------- slide 4
def s4(prs):
    s = blank(prs)
    chrome(s, 4, "HOW  ·  LECTURES 3, 7, 8, 4 AND 11",
           "A factor has to fit, and so does the question")

    text(s, M, 2.05, 6.0, 0.4,
         [{"t": "Place, year, technology", "font": DISPLAY, "size": 21, "color": INK}])

    y = 2.62
    for lab, val, src in [
        ("ELECTRICITY", "0.5737 kg CO₂/kWh", "Shanghai, 2023 · Announcement 2025 No. 47"),
        ("RAIL", "0.02709 kg CO₂/passenger·km", "China, 2019 · operation phase"),
    ]:
        rule(s, M, y, 6.05)
        label(s, M, y + 0.14, 2.0, lab)
        text(s, M, y + 0.38, 6.05, 0.4,
             [{"t": val, "font": UI, "size": 17, "bold": True, "color": INK}])
        text(s, M, y + 0.78, 6.05, 0.3,
             [{"t": src, "font": UI, "size": 11.5, "color": MUTED}])
        y += 1.42

    text(s, M, y + 0.06, 6.05, 0.8,
         [{"t": "The class sheet’s 0.4701 is Shanghai 2024 and is CO₂e. Both sources "
                "above report CO₂, so the page keeps CO₂.",
           "font": UI, "size": 11.5, "color": MUTED}], line_spacing=1.35)

    bx, bw = 7.35, W - M - 7.35
    block(s, bx, 2.05, bw, 3.45, TINT_AMBER)
    vrule(s, bx, 2.05, 3.45, AMBER, 2.5)
    text(s, bx + 0.36, 2.30, bw - 0.72, 0.4,
         [{"t": "An account, not a forecast", "font": DISPLAY, "size": 18,
           "color": AMBER}])
    text(s, bx + 0.36, 2.92, bw - 0.72, 2.7,
         [{"t": "This assigns emissions to one student inside a stated boundary — "
                "that is attributional.",
           "font": UI, "size": 12.5, "color": SOFT},
          {"t": "Replacing half the beef meals is not a consequential assessment: "
                "there is no baseline for what the food system would otherwise "
                "have done.",
           "font": UI, "size": 12.5, "color": SOFT}],
         line_spacing=1.4, space_after=8)


# ---------------------------------------------------------------- slide 5
def s5(prs):
    s = blank(prs)
    chrome(s, 5, "HOW THE PAGE ANSWERS HIM", "Three things he can actually use")

    cols = [
        ("01", "The profile stays filled in",
         "The shared facts are prefilled. Eighteen weeks is editable and labelled "
         "an assumption."),
        ("02", "The boundary stays visible",
         "Showers, parcels, clothing, and waste stay on the page and out of the total."),
        ("03", "The total names its units",
         "Sourced CO₂ and unverified CO₂e are listed apart, and meal advice says "
         "illustrative."),
    ]
    gap = 0.42
    cw = (CW - 2 * gap) / 3
    for i, (num, title, body) in enumerate(cols):
        x = M + i * (cw + gap)
        rule(s, x, 2.40, cw)
        text(s, x, 2.58, cw, 0.25,
             [{"t": num, "font": UI, "size": 10, "bold": True, "color": GREEN,
               "spc": 150}])
        text(s, x, 2.88, cw, 0.9,
             [{"t": title, "font": DISPLAY, "size": 21, "color": INK}],
             line_spacing=1.12)
        text(s, x, 3.70, cw, 1.6,
             [{"t": body, "font": UI, "size": 15, "color": SOFT}], line_spacing=1.5)

    footnote(s, "Five steps, one screen each. Reset returns the shared facts.")


# ---------------------------------------------------------------- slide 6
def s6(prs):
    s = blank(prs)
    chrome(s, 6, "DEMONSTRATION", "Three stops on the calculator")
    text(s, M, 1.62, CW - 0.5, 0.3,
         [{"t": "Nothing is retyped. One number changes. Then the result is read, "
                "not only displayed.", "font": UI, "size": 13, "color": MUTED}])

    steps = [
        ("01", "Transport",
         "Metro is weekly trips times kilometres. Ride-hailing is monthly and "
         "travelled alone. Rail is already per semester, so the weeks do not touch it."),
        ("02", "One change, on Energy",
         "Eighteen weeks is not a profile fact. Change it to 16: metro falls, rail "
         "stays at 880 km. Reset from the results page."),
        ("03", "Read the result",
         "96.1 kg CO₂ with a source, 687.6 kg CO₂e without. Beef advice through the "
         "word illustrative, then the 20 percent electricity cut."),
    ]
    gap = 0.5
    cw = (CW - 2 * gap) / 3
    for i, (num, title, body) in enumerate(steps):
        x = M + i * (cw + gap)
        text(s, x, 2.28, 1.2, 0.8,
             [{"t": num, "font": DISPLAY, "size": 40, "color": GREEN}])
        rule(s, x, 3.20, cw)
        text(s, x, 3.38, cw, 0.4,
             [{"t": title, "font": DISPLAY, "size": 20, "color": INK}])
        text(s, x, 3.90, cw, 1.8,
             [{"t": body, "font": UI, "size": 13, "color": SOFT}], line_spacing=1.45)

    footnote(s, "One live change is enough. The rest of the page is read, not clicked.")


# ---------------------------------------------------------------- slide 7
def s7(prs):
    s = blank(prs)
    chrome(s, 7, "SO WHAT  ·  ONE REVISION", "The unit")

    gap = 0.6
    cw = (CW - gap) / 2
    rows = [
        (2.30, [
            ("ISSUE", MUTED, "Prototype 1 called it kg CO₂e.",
             "Electricity and rail are published as CO₂, so the two cannot be "
             "carried under one name."),
            ("CHANGE", GREEN, "Now: kg reported per teaching semester.",
             "Sourced CO₂ and unverified CO₂e are listed apart, and meal advice "
             "says illustrative.")]),
        (4.15, [
            ("EFFECT", MUTED, "324 kg is not a verified ranking.",
             "He can see which advice is illustrative and which is arithmetic on a "
             "published factor."),
            ("STILL OPEN", AMBER, "Food, metro, and ride-hailing.",
             "No published source for any of the three. Disclosure is the current "
             "defense, not a fix.")]),
    ]
    for ry, items in rows:
        for i, (lab, color, head, body) in enumerate(items):
            x = M + i * (cw + gap)
            rule(s, x, ry, cw, LINE)
            label(s, x, ry + 0.14, cw, lab, color)
            text(s, x, ry + 0.44, cw - 0.35, 0.4,
                 [{"t": head, "font": DISPLAY, "size": 18, "color": INK}],
                 line_spacing=1.16)
            text(s, x, ry + 0.90, cw - 0.35, 0.7,
                 [{"t": body, "font": UI, "size": 12, "color": SOFT}], line_spacing=1.4)

    rule(s, M, 6.05, CW)
    text(s, M, 6.20, CW, 0.6,
         [{"t": "He can see which numbers have a source, and which numbers still "
                "cannot be used to rank.", "font": DISPLAY, "size": 18,
           "color": GREEN}], line_spacing=1.2)


# ---------------------------------------------------------------- slide 8
def s8(prs):
    s = blank(prs)
    chrome(s, 8, "DETAIL  ·  UNITS AND GASES", "One number, two units named")

    text(s, M, 1.78, CW, 0.4,
         [{"t": "CO₂e = Σ (gas × GWP100)", "size": 17, "bold": True, "color": INK}])
    text(s, M, 2.14, CW - 1.2, 0.4,
         [{"t": "A CO₂e total weights each gas by its 100-year warming potential. "
                "CO₂ and CO₂e are different baskets, so this page names them apart.",
           "font": UI, "size": 13, "color": MUTED}])

    gap = 0.6
    cw = (CW - gap) / 2
    cols = [
        (M, "SOURCED CO₂", GREEN, "96.1 kg", [
            "Electricity 72.3 kg · Shanghai 2023 · published as CO₂",
            "High-speed rail 23.8 kg · China 2019 · published as CO₂"]),
        (M + cw + gap, "UNVERIFIED CO₂e", AMBER, "687.6 kg", [
            "Food 648.0 kg · per-kilogram factors, portions assumed",
            "Metro 21.6 · ride-hailing 18.0 · walking 0.0 kg"]),
    ]
    for x, lab, color, big, lines in cols:
        rule(s, x, 2.78, cw, color, 1.6)
        text(s, x, 2.95, cw, 0.2,
             [{"t": lab, "size": 9.5, "bold": True, "color": color, "spc": 150}])
        text(s, x, 3.18, cw, 0.5,
             [{"t": big, "size": 30, "bold": True, "color": INK}])
        text(s, x, 3.82, cw - 0.2, 0.9,
             [{"t": ln, "font": UI, "size": 12, "color": SOFT} for ln in lines],
             line_spacing=1.45)

    block(s, M, 4.58, CW, 1.02, TINT_AMBER)
    vrule(s, M, 4.58, 1.02, AMBER, 2.5)
    text(s, M + 0.36, 4.80, CW - 0.75, 0.85,
         [{"t": "Both sourced rows are published as CO₂ only. Adding the other "
                "combustion gases would raise them, so 96.1 kg sits on the low side "
                "of a CO₂e.", "font": UI, "size": 13, "color": SOFT}], line_spacing=1.4)

    rule(s, M, 6.05, CW)
    text(s, M, 6.20, CW, 0.6,
         [{"t": "So the headline says reported and names both parts. It is not a "
                "compliant CO₂e total.", "font": DISPLAY, "size": 18,
           "color": GREEN}], line_spacing=1.2)


def main(out="roadshow/Group9_Roadshow_Slides.pptx"):
    prs = deck()
    for fn in (s1, s2, s3, s4, s5, s6, s7, s8):
        fn(prs)
    prs.save(out)
    print("wrote", out, len(prs.slides), "slides")


if __name__ == "__main__":
    main()
