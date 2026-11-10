# -*- coding: utf-8 -*-
"""One page A4 hand-held card for the roadshow: the numbers, then the answers."""
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

DISPLAY = "Georgia"
UI = "Segoe UI"

W, H = 8.27, 11.69          # A4 portrait
M = 0.62
CW = W - 2 * M


def tb(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    bodyPr = tf._txBody.find(A + "bodyPr")
    for tag in ("normAutofit", "spAutoFit"):
        el = bodyPr.find(A + tag)
        if el is not None:
            bodyPr.remove(el)
    if bodyPr.find(A + "noAutofit") is None:
        etree.SubElement(bodyPr, A + "noAutofit")
    return box


def run(p, s, font=UI, size=9, color=INK, bold=False, spc=None):
    r = p.add_run()
    r.text = s
    f = r.font
    f.name = font
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = color
    if spc is not None:
        f._rPr.set("spc", str(int(spc)))
    return r


def seg(p, s, **kw):
    for part in re.split(r"(₂)", s):
        if not part:
            continue
        if part == "₂":
            sub = dict(kw)
            sub["font"] = UI
            run(p, part, **sub)
        else:
            run(p, part, **kw)


def text(slide, x, y, w, h, chunks, spacing=None, after=None,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tf = tb(slide, x, y, w, h, anchor).text_frame
    for i, ch in enumerate(chunks):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing is not None:
            p.line_spacing = spacing
        if after is not None:
            p.space_after = Pt(after)
        for spec in (ch.get("runs") if "runs" in ch else [ch]):
            seg(p, spec.get("t", ""), **{k: v for k, v in spec.items() if k != "t"})
    return tf


def _plain(shp):
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


def kicker(slide, y, t, color=GREEN):
    text(slide, M, y, CW, 0.16,
         [{"t": t, "size": 7.5, "bold": True, "color": color, "spc": 150}])


def main(out="roadshow/Group9_Roadshow_Card.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = PAPER

    # ---------------------------------------------------------- head
    kicker(s, 0.50, "GROUP 9  ·  SDG2410J  ·  ROADSHOW CARD")
    text(s, M, 0.70, CW, 0.4,
         [{"t": "The numbers, then the answers", "font": DISPLAY, "size": 20}])
    text(s, M, 1.06, CW, 0.2,
         [{"t": "Every figure re-checked in the browser on 10 November 2026. "
                "Nothing here is new; it is the same file you are about to open.",
           "size": 8, "color": MUTED}])
    rule(s, M, 1.30, CW, INK, 1.2)

    # ---------------------------------------------------------- default
    kicker(s, 1.44, "DEFAULT  ·  18 WEEKS")
    cols = [("783.7", "kg reported", INK),
            ("96.1", "sourced CO₂", GREEN),
            ("687.6", "unverified CO₂e", AMBER)]
    cw = CW / 3
    for i, (big, small, color) in enumerate(cols):
        x = M + i * cw
        text(s, x, 1.62, cw - 0.1, 0.35,
             [{"t": big, "size": 21, "bold": True, "color": color}])
        text(s, x, 1.96, cw - 0.1, 0.16,
             [{"t": small, "size": 8, "color": MUTED}])

    # three category columns
    groups = [
        ("Transport 63.4 kg", [
            "Walk 360 km · 0.0 kg",
            "Metro 540 km · 21.6 kg",
            "Ride-hail 90 km · 18.0 kg",
            "Rail 880 km · 23.8 kg",
        ]),
        ("Food 648.0 kg", [
            "Beef 54 × 100 g · 324.0",
            "Other meat 144 × 250 g · 216.0",
            "Fish/egg/soy 90 × 400 g · 72.0",
            "Plant 90 × 400 g · 36.0",
        ]),
        ("Energy 72.3 kg", [
            "Room 120 kWh / 30 days",
            "→ 504 kWh / 126 days",
            "His quarter 126 kWh",
            "× 0.5737 kg CO₂/kWh",
        ]),
    ]
    y = 2.26
    for i, (head, lines) in enumerate(groups):
        x = M + i * cw
        text(s, x, y, cw - 0.16, 0.18,
             [{"t": head, "size": 9, "bold": True}])
        text(s, x, y + 0.21, cw - 0.16, 0.9,
             [{"t": ln, "size": 7.5, "color": SOFT} for ln in lines],
             spacing=1.35)

    # ---------------------------------------------------------- 16 weeks
    rule(s, M, 3.42, CW)
    kicker(s, 3.52, "THE ONE CHANGE  ·  16 WEEKS  ·  THEN RESET")
    text(s, M, 3.72, 1.5, 0.3,
         [{"t": "699.3", "size": 16, "bold": True}])
    text(s, M, 3.98, 1.5, 0.16,
         [{"t": "kg reported", "size": 7.5, "color": MUTED}])
    text(s, M + 1.55, 3.72, CW - 1.55, 0.5,
         [{"t": "Sourced 88.1 · unverified 611.2. Metro 480 km · beef 48 meals · "
                "electricity 112 days. Rail stays 880 km — it was already per semester.",
           "size": 8, "color": SOFT}], spacing=1.35)

    # ---------------------------------------------------------- factors
    rule(s, M, 4.36, CW)
    kicker(s, 4.46, "THE TWO FACTORS WITH A SOURCE  ·  BOTH REPORT CO₂, NOT CO₂e")
    text(s, M, 4.66, CW, 0.34,
         [{"runs": [{"t": "Electricity  ", "size": 8, "bold": True},
                    {"t": "0.5737 kg CO₂/kWh  ·  Shanghai provincial average, 2023  ·  "
                          "Announcement 2025 No. 47", "size": 8, "color": SOFT}]}])
    text(s, M, 4.92, CW, 0.34,
         [{"runs": [{"t": "High-speed rail  ", "size": 8, "bold": True},
                    {"t": "0.02709 kg CO₂/passenger·km  ·  China 2019, operation phase  ·  "
                          "Tong et al. 2025", "size": 8, "color": SOFT}]}])

    # ---------------------------------------------------------- suggestions
    rule(s, M, 5.28, CW)
    kicker(s, 5.38, "THE TWO SUGGESTIONS TO READ ALOUD")
    text(s, M, 5.58, CW, 0.5,
         [{"runs": [{"t": "Beef  −159.3 → 624.4   ", "size": 8, "bold": True},
                    {"t": "“illustrative”: the per-kilogram factor is provisional and the "
                          "portion is our assumption.", "size": 8, "color": SOFT}]}], spacing=1.3)
    text(s, M, 5.82, CW, 0.5,
         [{"runs": [{"t": "Electricity  −14.5 → 769.3   ", "size": 8, "bold": True},
                    {"t": "the factor has a source, so the arithmetic is sourced; the 20 "
                          "percent is still a scenario.", "size": 8, "color": SOFT}]}], spacing=1.3)

    # ---------------------------------------------------------- Q&A
    rule(s, M, 6.22, CW, INK, 1.2)
    kicker(s, 6.36, "IF ASKED")
    qa = [
        ("Why 0.5737 and not the class sheet’s 0.4701?",
         "That one is Shanghai 2024 and it is CO₂e. This one is 2023 provincial average, and the source reports CO₂."),
        ("Why not multiply by 52?",
         "The profile mixes weeks, months, 30 days and semesters, and never says how many semesters make a year. One month = 4 weeks."),
        ("Why is food so large?",
         "3 beef meals a week × 18 weeks × an assumed 100 g portion × a provisional 60 kg CO₂e/kg. The portion is ours, so the ranking is illustrative."),
        ("Why is your figure below 2.54 and 3.84?",
         "Two 18-week semesters is about 1.6 t. Showers, shopping and waste are outside the boundary, and the year is 36 weeks, not 52."),
        ("Why leave out showers and waste?",
         "The profile gives counts, not energy, mass, or a treatment pathway. They stay on the page and out of the total."),
        ("Is 120 kWh Li Ming’s own use?",
         "No. It is the whole room over 30 days. He is one quarter of four, scaled to the semester."),
        ("A battery car is always lower, right?",
         "Only if asked. iX5 production 18.1 t against 11.7 t for the diesel X5; over 200,000 km on the European mix, 31.1 t against 58.3 t. Not an input to this calculator."),
    ]
    tf = tb(s, M, 6.56, CW, 4.6).text_frame
    for i, (q, a) in enumerate(qa):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.3
        p.space_after = Pt(5)
        seg(p, q, size=8, bold=True)
        p2 = tf.add_paragraph()
        p2.line_spacing = 1.3
        p2.space_after = Pt(7)
        seg(p2, a, size=8, color=SOFT)

    # footer
    rule(s, M, H - 0.62, CW)
    text(s, M, H - 0.50, CW, 0.2,
         [{"t": "Group 9 · one member · 7 min 30 s · slides uploaded before the deadline · "
                "use the final submitted HTML", "size": 7, "color": MUTED}])

    prs.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
