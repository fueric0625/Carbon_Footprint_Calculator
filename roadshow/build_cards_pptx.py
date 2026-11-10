# -*- coding: utf-8 -*-
"""Rebuild the cue-card PDF, then emit the same cards as a PowerPoint deck.

Source of truth: roadshow/Group9_Script_Cards.html
"""
import math
import os
import subprocess

from lxml import html
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

INK = RGBColor(0x13, 0x1A, 0x17)
SOFT = RGBColor(0x46, 0x52, 0x4C)
MUTED = RGBColor(0x6E, 0x7A, 0x73)
LINE = RGBColor(0xE1, 0xE4, 0xDD)
GREEN = RGBColor(0x1B, 0x6B, 0x4F)
AMBER = RGBColor(0xA9, 0x64, 0x2B)
PAPER = RGBColor(0xFB, 0xFB, 0xF8)

LATIN = "Segoe UI"
CJK = "Microsoft YaHei"

W, H = 8.27, 11.69
M = 0.62
CW = W - 2 * M

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

EM = 1.24          # natural line height of Segoe UI, in em

from PIL import ImageFont
_FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
_FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
_cache = {}


def _font(size, bold):
    key = (int(round(size)), bold)
    if key not in _cache:
        try:
            _cache[key] = ImageFont.truetype(_FONT_BOLD if bold else _FONT_REG, key[0])
        except OSError:
            _cache[key] = None
    return _cache[key]


def lines_plain(text, size, width_in, bold=False):
    font = _font(size, bold)
    if font is None:
        return max(1, math.ceil(len(text) / max(10, int(width_in * 72 / (size * 0.55)))))
    limit = (width_in - 0.04) * 72 * 0.95   # 5% safety for PowerPoint metric drift
    n, cur = 1, ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if not cur or font.getlength(trial) <= limit:
            cur = trial
        else:
            n += 1
            cur = w
    return n


def lines_runs(runs, size, width_in):
    text = "".join(t for t, _, _ in runs)
    has_bold = any(b for _, b, _ in runs)
    return lines_plain(text, size, width_in / (1.05 if has_bold else 1.0))


# ------------------------------------------------------------------ html -> data
def cls(el):
    return el.get("class") or ""


def runs_of(el, bold=False, amber=False):
    out = []
    if el.text:
        out.append((el.text, bold, amber))
    for ch in el:
        b = bold or (ch.tag == "b")
        a = amber or ("amber" in cls(ch))
        out.extend(runs_of(ch, b, a))
        if ch.tail:
            out.append((ch.tail, bold, amber))
    return [(t, b, a) for t, b, a in out if t.strip()]


def txt(el):
    return " ".join(el.text_content().split())


def txt_br(el):
    out = [el.text or ""]
    for ch in el:
        out.append(" ")
        out.append(ch.text_content() or "")
        out.append(ch.tail or "")
    return " ".join("".join(out).split())


def parse_cards(path):
    root = html.parse(path).getroot()
    cards = []
    for sec in root.xpath('//section[contains(@class,"card")]'):
        time_el = sec.xpath('.//*[contains(@class,"time")]')
        pg_el = sec.xpath('.//*[contains(@class,"pg")]')
        title_el = sec.xpath('.//*[contains(@class,"title")]')
        sub_el = sec.xpath('.//*[contains(@class,"sub")]')
        next_el = sec.xpath('.//*[contains(@class,"next")]')

        blocks = []
        for p in sec.xpath('.//div[contains(@class,"blocks")]/p'):
            if "cue" in cls(p):
                blocks.append(("cue", runs_of(p)))
            elif "say" in cls(p):
                blocks.append(("say", runs_of(p)))

        table = sec.xpath('.//table')
        qa = sec.xpath('.//div[contains(@class,"qa")]')
        rescue = sec.xpath('.//div[contains(@class,"big3")]/p')
        ups = sec.xpath('.//p[contains(@class,"label")]')
        uls = sec.xpath('.//ul')

        cards.append({
            "time": txt(time_el[0]) if time_el else "",
            "pg": txt(pg_el[0]) if pg_el else "",
            "title": txt(title_el[0]) if title_el else "",
            "sub": txt(sub_el[0]) if sub_el else "",
            "next": txt(next_el[0]) if next_el else "",
            "blocks": blocks,
            "table": table[0] if table else None,
            "qa": qa,
            "labels": ups,
            "lists": uls,
            "rescue": rescue,
        })
    return cards


# ------------------------------------------------------------------ pptx helpers
def blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = PAPER
    return s


def _strip(shp):
    style = shp._element.find(qn("p:style"))
    if style is not None:
        shp._element.remove(style)
    shp.shadow.inherit = False
    return shp


def rect(slide, x, y, w, h, color):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                 Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    return _strip(shp)


def box(slide, x, y, w, h):
    b = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = b.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


def style_run(r, size, color=INK, bold=False, italic=False, spc=None):
    f = r.font
    f.name = LATIN
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    rPr = f._rPr
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        rPr.append(ea)
    ea.set("typeface", CJK)
    if spc is not None:
        rPr.set("spc", str(int(spc)))


def simple(slide, x, y, w, text, size, color=INK, bold=False, italic=False,
           spc=None, align=None, spacing=None):
    tf = box(slide, x, y, w, 0.4)
    p = tf.paragraphs[0]
    if align is not None:
        p.alignment = align
    if spacing is not None:
        p.line_spacing = spacing
    r = p.add_run()
    r.text = text
    style_run(r, size, color, bold=bold, italic=italic, spc=spc)
    return tf


def est_lines(chars, size, width_in, factor=0.52):
    per = max(10, int(width_in * 72 / (size * factor)))
    return max(1, math.ceil(chars / per))


def build(cards, out):
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)

    TOP, BOTTOM = 1.26, H - 0.62
    avail = BOTTOM - TOP

    for c in cards:
        s = blank(prs)

        simple(s, M, 0.50, CW * 0.8, c["time"], 9, GREEN, bold=True, spc=140)
        simple(s, W - M - 1.3, 0.50, 1.3, c["pg"], 9, MUTED, bold=True, spc=80,
               align=PP_ALIGN.RIGHT)
        rect(s, M, 0.72, CW, 0.011, LINE)
        simple(s, M, 0.84, CW, c["title"], 19, INK, bold=True)

        y = TOP
        if c["sub"]:
            simple(s, M, y - 0.10, CW, c["sub"], 10.5, MUTED)
            y += 0.30

        if c["blocks"]:
            y = flow_blocks(s, c["blocks"], y, avail)
        elif c["table"] is not None:
            y = flow_table(s, c["table"], y)
        elif c["qa"]:
            y = flow_qa(s, c["qa"], y)
        elif c["labels"] or c["lists"] or c.get("rescue"):
            y = flow_labels(s, c, y)

        rect(s, M, H - 0.62, CW, 0.011, LINE)
        simple(s, M, H - 0.50, CW, c["next"], 9, GREEN, bold=True)

    prs.save(out)
    return out


def flow_blocks(s, blocks, y, avail):
    SAY, CUE = 21.0, 11.5

    def measure(say_sz, cue_sz):
        tot = 0.0
        for kind, runs in blocks:
            if kind == "say":
                n = lines_runs(runs, say_sz, CW - 0.30)
                tot += n * say_sz * 1.38 * EM / 72 + 0.24
            else:
                n = lines_runs(runs, cue_sz, CW)
                tot += n * cue_sz * 1.45 * EM / 72 + 0.18
        return tot

    h = measure(SAY, CUE)
    if h > avail:
        k = max(0.70, avail / h)
        SAY, CUE = SAY * k, max(9.5, CUE * k)

    for kind, runs in blocks:
        if kind == "say":
            n = lines_runs(runs, SAY, CW - 0.30)
            hh = n * SAY * 1.38 * EM / 72
            rect(s, M, y + 0.12, 0.03, max(0.14, hh - 0.08), GREEN)
            tf = box(s, M + 0.22, y - 0.03, CW - 0.26, hh + 0.3)
            p = tf.paragraphs[0]
            p.line_spacing = 1.38
            for text, bold, amber in runs:
                r = p.add_run()
                r.text = text
                style_run(r, SAY, AMBER if amber else INK, bold=bold)
            y += hh + 0.34
        else:
            n = lines_runs(runs, CUE, CW)
            hh = n * CUE * 1.45 * EM / 72
            tf = box(s, M, y, CW, hh + 0.2)
            p = tf.paragraphs[0]
            p.line_spacing = 1.45
            for text, _, _ in runs:
                r = p.add_run()
                r.text = text
                style_run(r, CUE, MUTED, italic=True)
            y += hh + 0.20
    return y


def flow_table(s, table, y):
    cols = [(M, 0.62), (M + 0.72, 1.32), (M + 2.08, CW - 2.08)]
    for i, tr in enumerate(table.xpath(".//tr")):
        cells = [" ".join(td.text_content().split()) for td in tr.xpath("./th|./td")]
        if not cells:
            continue
        if i == 0:
            for j, ctext in enumerate(cells[:3]):
                simple(s, cols[j][0], y, cols[j][1], ctext, 8.5, MUTED,
                       bold=True, spc=110)
            rect(s, M, y + 0.20, CW, 0.008, LINE)
            y += 0.32
        else:
            for j, ctext in enumerate(cells[:3]):
                color = GREEN if j == 0 else (MUTED if j == 1 else INK)
                simple(s, cols[j][0], y, cols[j][1], ctext, 10.5, color,
                       bold=(j == 0))
            y += 0.30
    return y


def flow_qa(s, qa, y):
    for block in qa:
        for p_el in block.xpath("./p"):
            kind = cls(p_el)
            text = txt(p_el)
            if not text:
                continue
            size, color, bold = {"q": (12.5, INK, True),
                                 "a": (11.5, SOFT, False),
                                 "cn": (9.5, MUTED, False)}.get(kind, (11.5, INK, False))
            n = lines_plain(text, size, CW - 0.05)
            hh = n * size * 1.45 * EM / 72
            tf = box(s, M, y, CW, hh + 0.2)
            p = tf.paragraphs[0]
            p.line_spacing = 1.45
            r = p.add_run()
            r.text = text
            style_run(r, size, color, bold=bold)
            y += hh + (0.08 if kind == "cn" else 0.14)
        y += 0.06
    return y


def flow_labels(s, c, y):
    items = c["labels"] + c["lists"] + c.get("rescue", [])
    for el in sorted(items, key=lambda e: e.sourceline or 0):
        if el.tag == "p" and "label" in cls(el):
            y += 0.12
            simple(s, M, y, CW, txt(el).upper(), 9, GREEN, bold=True, spc=140)
            y += 0.32
        elif el.tag == "p":
            text = txt_br(el)
            n = lines_plain(text, 11.5, CW - 0.05)
            hh = n * 11.5 * 1.5 * EM / 72
            tf = box(s, M, y, CW, hh + 0.25)
            p = tf.paragraphs[0]
            p.line_spacing = 1.5
            r = p.add_run()
            r.text = text
            style_run(r, 11.5, INK)
            y += hh + 0.16
        elif el.tag == "ul":
            for li in el.xpath("./li"):
                text = " ".join(li.text_content().split())
                n = lines_plain(text, 11, CW - 0.25)
                hh = n * 11 * 1.5 * EM / 72
                tf = box(s, M + 0.05, y, CW - 0.2, hh + 0.25)
                p = tf.paragraphs[0]
                p.line_spacing = 1.5
                r = p.add_run()
                r.text = "\u2022  " + text
                style_run(r, 11, SOFT)
                y += hh + 0.10
            y += 0.12
    return y


if __name__ == "__main__":
    src = os.path.abspath(r"roadshow\Group9_Script_Cards.html")
    pdf = os.path.abspath(r"roadshow\Group9_Script_Cards.pdf")
    if os.path.exists(pdf):
        os.remove(pdf)
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + pdf, "file:///" + src.replace("\\", "/")],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("pdf bytes:", os.path.getsize(pdf) if os.path.exists(pdf) else "FAILED")

    cards = parse_cards(src)
    print("cards parsed:", len(cards))
    print(build(cards, r"roadshow\Group9_Script_Cards.pptx"))
