#!/usr/bin/env python3
"""
Elvoro Golf — Hat Design Specifications generator.

Produces a technical specification pack for the Founders Collection headwear
drop, mirroring the structure and house style of the Polo Design Specifications
pack: title page, collection overview + master brand palette, and one detailed
spec page per style (colourway, pattern/print, fabric, trim & construction,
front + side mockups, logo placement).

Run:  python3 specs/build_hat_specs.py
Out:  specs/Elvoro_Hat_Design_Specs.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "Elvoro_Hat_Design_Specs.pdf")
LOGO_GREEN = os.path.join(ROOT, "assets", "brand", "elvoro-logo-green.png")
CREST = os.path.join(ROOT, "assets", "brand", "elvoro-crest.png")

# ---- Brand palette -----------------------------------------------------------
FOREST = HexColor("#0B232D")
GOLD = HexColor("#D4AF37")
BONE = HexColor("#E5DCC7")
WHITE_F = HexColor("#F0EDE8")
INK = HexColor("#1A1A1A")
MUTE = HexColor("#6E6E6E")
HAIR = HexColor("#D8D4CB")
PAPER = HexColor("#FBFAF7")

PAGE_W, PAGE_H = letter
MX = 22 * mm  # page margin
DATE = "16 June 2026"

SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SANS = "Helvetica"
SANS_B = "Helvetica-Bold"


def tracked(c, x, y, text, font, size, color, tracking=0.0, center=False):
    """Draw text with manual letter-spacing (tracking in points)."""
    c.setFont(font, size)
    c.setFillColor(color)
    widths = [c.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1 if len(text) > 1 else 0)
    cx = x - total / 2.0 if center else x
    for ch, w in zip(text, widths):
        c.drawString(cx, y, ch)
        cx += w + tracking
    return total


# ---- Reusable chrome ---------------------------------------------------------
def page_frame(c, footer_left, footer_right):
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # top rule
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.4)
    c.line(MX, PAGE_H - 20 * mm, PAGE_W - MX, PAGE_H - 20 * mm)
    tracked(c, MX, PAGE_H - 17.5 * mm, "ELVORO GOLF", SERIF_B, 10, FOREST, 2.2)
    c.setFont(SANS, 8)
    c.setFillColor(MUTE)
    c.drawRightString(PAGE_W - MX, PAGE_H - 17.5 * mm, "HAT DESIGN SPECIFICATIONS")
    # footer
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.7)
    c.line(MX, 16 * mm, PAGE_W - MX, 16 * mm)
    c.setFont(SANS, 7.5)
    c.setFillColor(MUTE)
    c.drawString(MX, 12.5 * mm, footer_left)
    c.drawRightString(PAGE_W - MX, 12.5 * mm, footer_right)


def swatch(c, x, y, w, h, fill, name, hexv, dark_text=False):
    c.setFillColor(fill)
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.6)
    c.rect(x, y, w, h, fill=1, stroke=1)
    c.setFont(SANS_B, 7.6)
    c.setFillColor(INK)
    c.drawString(x, y - 4.2 * mm, name)
    c.setFont("Courier", 7.4)
    c.setFillColor(MUTE)
    c.drawString(x, y - 7.6 * mm, hexv)


def section_label(c, x, y, text):
    tracked(c, x, y, text.upper(), SANS_B, 8.5, GOLD, 1.6)
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.6)
    c.line(x, y - 2.2 * mm, x + 46 * mm, y - 2.2 * mm)


def spec_rows(c, x, y, rows, label_w=30 * mm, line_h=5.0 * mm, val_w=64 * mm):
    """Render label/value rows; wraps long values. Returns final y."""
    for label, value in rows:
        c.setFont(SANS_B, 7.8)
        c.setFillColor(FOREST)
        c.drawString(x, y, label)
        c.setFont(SANS, 7.8)
        c.setFillColor(INK)
        # naive word-wrap on value
        words = value.split()
        line = ""
        first = True
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, SANS, 7.8) > val_w and line:
                c.drawString(x + label_w, y, line)
                y -= 3.7 * mm
                line = w
                first = False
            else:
                line = test
        if line:
            c.drawString(x + label_w, y, line)
        y -= line_h
    return y


# ---- Cap illustration --------------------------------------------------------
def draw_cap_front(c, cx, cy, scale, crown, panel_line, brim, logo="crest",
                   logo_color=GOLD, pattern=None):
    """Stylised front-elevation of a 6-panel cap centred at (cx, cy)."""
    s = scale
    c.saveState()
    # crown (rounded trapezoid dome)
    p = c.beginPath()
    p.moveTo(cx - 42 * s, cy - 6 * s)
    p.curveTo(cx - 46 * s, cy + 30 * s, cx - 24 * s, cy + 50 * s, cx, cy + 50 * s)
    p.curveTo(cx + 24 * s, cy + 50 * s, cx + 46 * s, cy + 30 * s, cx + 42 * s, cy - 6 * s)
    p.close()
    c.setFillColor(crown)
    c.setStrokeColor(panel_line)
    c.setLineWidth(0.8)
    c.drawPath(p, fill=1, stroke=1)

    # tonal pattern dots/marks inside crown
    if pattern == "star":
        c.setFillColor(panel_line)
        for gx in range(-3, 4):
            for gy in range(0, 5):
                px = cx + gx * 11 * s
                py = cy + 2 * s + gy * 9 * s
                if (px - cx) ** 2 / (42 * s) ** 2 + (py - cy - 18 * s) ** 2 / (40 * s) ** 2 < 0.7:
                    _star(c, px, py, 1.6 * s, panel_line)
    elif pattern == "monogram":
        c.setFillColor(panel_line)
        for gx in range(-3, 4):
            for gy in range(0, 5):
                px = cx + gx * 12 * s + (6 * s if gy % 2 else 0)
                py = cy + 2 * s + gy * 9 * s
                if (px - cx) ** 2 / (42 * s) ** 2 + (py - cy - 18 * s) ** 2 / (40 * s) ** 2 < 0.65:
                    _diamond(c, px, py, 1.9 * s, panel_line)
    elif pattern == "stripe":
        c.setStrokeColor(panel_line)
        c.setLineWidth(0.9 * s)
        for off in range(-3, 4):
            xx = cx + off * 12 * s
            c.line(xx - 0.8 * s, cy - 4 * s, xx - 0.8 * s, cy + 46 * s)
            c.line(xx + 0.8 * s, cy - 4 * s, xx + 0.8 * s, cy + 46 * s)

    # centre + side panel seams
    c.setStrokeColor(panel_line)
    c.setLineWidth(0.8)
    c.line(cx, cy - 4 * s, cx, cy + 50 * s)
    pa = c.beginPath()
    pa.moveTo(cx - 16 * s, cy - 5 * s)
    pa.curveTo(cx - 18 * s, cy + 22 * s, cx - 12 * s, cy + 40 * s, cx, cy + 50 * s)
    c.drawPath(pa, stroke=1, fill=0)
    pb = c.beginPath()
    pb.moveTo(cx + 16 * s, cy - 5 * s)
    pb.curveTo(cx + 18 * s, cy + 22 * s, cx + 12 * s, cy + 40 * s, cx, cy + 50 * s)
    c.drawPath(pb, stroke=1, fill=0)

    # top button
    c.setFillColor(panel_line)
    c.circle(cx, cy + 50 * s, 1.6 * s, fill=1, stroke=0)

    # brim (front curve)
    bp = c.beginPath()
    bp.moveTo(cx - 42 * s, cy - 6 * s)
    bp.curveTo(cx - 50 * s, cy - 20 * s, cx + 50 * s, cy - 20 * s, cx + 42 * s, cy - 6 * s)
    bp.close()
    c.setFillColor(brim)
    c.setStrokeColor(panel_line)
    c.setLineWidth(0.8)
    c.drawPath(bp, fill=1, stroke=1)

    # front crest logo
    if logo == "crest" and os.path.exists(CREST):
        try:
            c.drawImage(ImageReader(_tinted_crest(logo_color)), cx - 9 * s, cy + 8 * s,
                        width=18 * s, height=19.4 * s, mask="auto",
                        preserveAspectRatio=True)
        except Exception:
            _shield(c, cx, cy + 18 * s, 5 * s, logo_color)
    else:
        _shield(c, cx, cy + 18 * s, 5 * s, logo_color)
    c.restoreState()


def draw_cap_side(c, cx, cy, scale, crown, panel_line, brim):
    """Stylised side-profile of the cap."""
    s = scale
    c.saveState()
    dome = c.beginPath()
    dome.moveTo(cx - 34 * s, cy - 4 * s)
    dome.curveTo(cx - 36 * s, cy + 34 * s, cx + 30 * s, cy + 40 * s, cx + 36 * s, cy + 2 * s)
    dome.lineTo(cx + 36 * s, cy - 4 * s)
    dome.close()
    c.setFillColor(crown)
    c.setStrokeColor(panel_line)
    c.setLineWidth(0.8)
    c.drawPath(dome, fill=1, stroke=1)
    # panel seam
    c.line(cx + 2 * s, cy - 4 * s, cx + 8 * s, cy + 38 * s)
    # button
    c.setFillColor(panel_line)
    c.circle(cx + 6 * s, cy + 39 * s, 1.4 * s, fill=1, stroke=0)
    # brim extends to the right/front
    bp = c.beginPath()
    bp.moveTo(cx - 34 * s, cy - 4 * s)
    bp.curveTo(cx - 64 * s, cy - 10 * s, cx - 70 * s, cy - 16 * s, cx - 66 * s, cy - 18 * s)
    bp.curveTo(cx - 62 * s, cy - 20 * s, cx - 40 * s, cy - 12 * s, cx - 34 * s, cy - 9 * s)
    bp.close()
    c.setFillColor(brim)
    c.setStrokeColor(panel_line)
    c.drawPath(bp, fill=1, stroke=1)
    # sweatband hint
    c.setStrokeColor(panel_line)
    c.setLineWidth(0.6)
    c.line(cx - 34 * s, cy - 3 * s, cx + 35 * s, cy - 1 * s)
    c.restoreState()


def _star(c, x, y, r, color):
    import math
    c.setFillColor(color)
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((x + rr * math.cos(ang), y + rr * math.sin(ang)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for px, py in pts[1:]:
        p.lineTo(px, py)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def _diamond(c, x, y, r, color):
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(x, y + r)
    p.lineTo(x + r, y)
    p.lineTo(x, y - r)
    p.lineTo(x - r, y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def _shield(c, x, y, r, color):
    c.setStrokeColor(color)
    c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(x - r, y + r)
    p.lineTo(x + r, y + r)
    p.lineTo(x + r, y - r * 0.4)
    p.curveTo(x + r, y - r * 1.4, x, y - r * 1.8, x, y - r * 1.8)
    p.curveTo(x, y - r * 1.8, x - r, y - r * 1.4, x - r, y - r * 0.4)
    p.close()
    c.drawPath(p, fill=0, stroke=1)


_CREST_CACHE = {}


def _tinted_crest(color):
    """Return an ImageReader of the crest recoloured to `color` (gold/navy/etc.)."""
    key = color.hexval()
    if key in _CREST_CACHE:
        return _CREST_CACHE[key]
    from PIL import Image
    im = Image.open(CREST).convert("RGBA")
    r = int(color.red * 255)
    g = int(color.green * 255)
    b = int(color.blue * 255)
    px = im.load()
    for j in range(im.height):
        for i in range(im.width):
            _, _, _, a = px[i, j]
            if a > 0:
                px[i, j] = (r, g, b, a)
    from io import BytesIO
    buf = BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    _CREST_CACHE[key] = ImageReader(buf)
    return _CREST_CACHE[key]


# ---- Pages -------------------------------------------------------------------
def page_title(c):
    c.setFillColor(FOREST)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.rect(14 * mm, 14 * mm, PAGE_W - 28 * mm, PAGE_H - 28 * mm, fill=0, stroke=1)

    if os.path.exists(LOGO_GREEN):
        iw = 52 * mm
        ih = iw * 1180 / 1000
        c.drawImage(LOGO_GREEN, (PAGE_W - iw) / 2, PAGE_H - 30 * mm - ih,
                    width=iw, height=ih, mask="auto", preserveAspectRatio=True)

    yy = PAGE_H - 30 * mm - 52 * mm * 1180 / 1000 - 16 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(PAGE_W / 2 - 30 * mm, yy + 6 * mm, PAGE_W / 2 + 30 * mm, yy + 6 * mm)
    tracked(c, PAGE_W / 2, yy - 6 * mm, "HAT DESIGN SPECIFICATIONS", SERIF, 22, WHITE_F, 3.2, center=True)
    tracked(c, PAGE_W / 2, yy - 16 * mm, "FOUNDERS COLLECTION — HEADWEAR · THREE STYLES · SS26",
            SANS, 9.5, GOLD, 2.0, center=True)
    tracked(c, PAGE_W / 2, yy - 24 * mm, f"TECHNICAL SPECIFICATION PACK · {DATE}",
            SANS, 8.5, BONE, 1.6, center=True)

    c.setFont(SANS, 8)
    c.setFillColor(BONE)
    c.drawCentredString(PAGE_W / 2, 24 * mm,
                        "Prepared for the Elvoro Golf design & manufacturing team · Confidential")
    c.showPage()


def page_overview(c):
    page_frame(c, "Collection Overview", f"{DATE} · Confidential")
    x = MX
    y = PAGE_H - 34 * mm
    tracked(c, x, y, "ELVORO GOLF HEADWEAR", SANS_B, 9, MUTE, 1.4)
    y -= 9 * mm
    c.setFont(SERIF_B, 22)
    c.setFillColor(FOREST)
    c.drawString(x, y, "Collection Overview")
    y -= 9 * mm
    c.setFont(SANS, 9.2)
    c.setFillColor(INK)
    intro = ("Three caps in the Elvoro Founders Collection — Headwear, built to production "
             "spec with the official Elvoro Golf crest. Each style shares the house headwear "
             "silhouette — structured front panels, pre-curved visor, full buckram-backed "
             "crest zone, moisture-wicking sweatband and a clean rear closure — differentiated "
             "by crown colour, tonal pattern and trim. The drop is engineered to sit alongside "
             "the three Founders polos, sharing colourway, motif and logo language.")
    for ln in _wrap(c, intro, SANS, 9.2, PAGE_W - 2 * MX):
        c.drawString(x, y, ln)
        y -= 4.6 * mm

    y -= 4 * mm
    styles = [
        ("Forest Crest Cap — Forest Green", "EG-HW-01"),
        ("Heritage Monogram Cap — Bone", "EG-HW-02"),
        ("Founders Stripe Cap — Founders White", "EG-HW-03"),
    ]
    colw = (PAGE_W - 2 * MX) / 3
    for i, (nm, code) in enumerate(styles):
        bx = x + i * colw
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.7)
        c.rect(bx, y - 30 * mm, colw - 6 * mm, 30 * mm, fill=0, stroke=1)
        crown = [FOREST, BONE, WHITE_F][i]
        pline = [HexColor("#1E3F30"), HexColor("#C8B98F"), HexColor("#C8C6C1")][i]
        brim = [FOREST, BONE, WHITE_F][i]
        logo_c = [GOLD, GOLD, FOREST][i]
        pat = ["star", "monogram", "stripe"][i]
        draw_cap_front(c, bx + (colw - 6 * mm) / 2, y - 21 * mm, 0.26,
                       crown, pline, brim, logo_color=logo_c, pattern=pat)
        c.setFont(SANS_B, 7.8)
        c.setFillColor(FOREST)
        c.drawCentredString(bx + (colw - 6 * mm) / 2, y - 25.5 * mm, _short(nm))
        c.setFont("Courier", 7.2)
        c.setFillColor(GOLD)
        c.drawCentredString(bx + (colw - 6 * mm) / 2, y - 28.5 * mm, code)

    y -= 44 * mm
    section_label(c, x, y, "Master Brand Palette")
    y -= 10 * mm
    sw_w, sw_h = 34 * mm, 16 * mm
    gap = (PAGE_W - 2 * MX - 4 * sw_w) / 3
    palette = [
        (FOREST, "Forest Green", "#0B232D"),
        (GOLD, "Heritage Gold", "#D4AF37"),
        (BONE, "Bone", "#E5DCC7"),
        (WHITE_F, "Founders White", "#F0EDE8"),
    ]
    for i, (col, nm, hx) in enumerate(palette):
        swatch(c, x + i * (sw_w + gap), y - sw_h, sw_w, sw_h, col, nm, hx)

    y -= sw_h + 16 * mm
    section_label(c, x, y, "House Standards — Headwear")
    y -= 9 * mm
    notes = [
        "Crest reproduced from master vector artwork only · minimum front height 38 mm.",
        "Embroidery: flat satin for crest body, 3-D foam puff permitted on structured fronts only.",
        "All caps one-size, adjustable closure · interior woven Elvoro neck label at centre rear.",
        "Colour, motif and thread to match the SS26 Founders polo pack for cross-collection unity.",
    ]
    c.setFont(SANS, 8.4)
    for n in notes:
        c.setFillColor(GOLD)
        c.drawString(x, y, "—")
        c.setFillColor(INK)
        c.drawString(x + 5 * mm, y, n)
        y -= 5.2 * mm
    c.showPage()


def page_style(c, code, title, footer_tag, colourway, pattern, fabric, trim,
               logo_rows, crown, pline, brim, logo_c, pat_kind):
    page_frame(c, f"{title} · {code}", f"{DATE} · Confidential")
    x = MX
    y = PAGE_H - 32 * mm
    tracked(c, x, y, f"FOUNDERS COLLECTION — HEADWEAR · SS26 · STYLE {code}",
            SANS_B, 8, MUTE, 1.2)
    y -= 8.5 * mm
    c.setFont(SERIF_B, 20)
    c.setFillColor(FOREST)
    c.drawString(x, y, title)
    y -= 3 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.0)
    c.line(x, y, x + 60 * mm, y)

    col_x = x
    col_w = 92 * mm
    top = y - 8 * mm

    # LEFT COLUMN — specs
    yy = top
    section_label(c, col_x, yy, "Colourway")
    yy -= 7 * mm
    sw = 7 * mm
    for i, (nm, hx, col) in enumerate(colourway):
        rowy = yy - i * 8.2 * mm
        c.setFillColor(col)
        c.setStrokeColor(HAIR)
        c.setLineWidth(0.6)
        c.rect(col_x, rowy - sw + 2 * mm, sw, sw, fill=1, stroke=1)
        c.setFont(SANS_B, 7.8)
        c.setFillColor(INK)
        c.drawString(col_x + sw + 3 * mm, rowy, nm)
        c.setFont("Courier", 7.2)
        c.setFillColor(MUTE)
        c.drawString(col_x + sw + 3 * mm, rowy - 3.4 * mm, hx)
    yy -= len(colourway) * 8.2 * mm + 4 * mm

    section_label(c, col_x, yy, "Pattern / Print")
    yy -= 7 * mm
    yy = spec_rows(c, col_x, yy, pattern, label_w=24 * mm, val_w=66 * mm)
    yy -= 2 * mm

    section_label(c, col_x, yy, "Fabric")
    yy -= 7 * mm
    yy = spec_rows(c, col_x, yy, fabric, label_w=27 * mm, val_w=63 * mm)

    # RIGHT COLUMN — mockups
    rx = col_x + col_w + 8 * mm
    rw = PAGE_W - MX - rx
    ry = top
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.7)
    c.rect(rx, ry - 56 * mm, rw, 56 * mm, fill=0, stroke=1)
    tracked(c, rx + 3 * mm, ry - 5 * mm, "FRONT · PRODUCTION MOCKUP", SANS_B, 7, MUTE, 1.0)
    draw_cap_front(c, rx + rw / 2, ry - 36 * mm, 0.40, crown, pline, brim,
                   logo_color=logo_c, pattern=pat_kind)

    ry -= 56 * mm + 6 * mm
    c.setStrokeColor(HAIR)
    c.rect(rx, ry - 40 * mm, rw, 40 * mm, fill=0, stroke=1)
    tracked(c, rx + 3 * mm, ry - 5 * mm, "SIDE PROFILE", SANS_B, 7, MUTE, 1.0)
    draw_cap_side(c, rx + rw / 2 + 6 * mm, ry - 26 * mm, 0.40, crown, pline, brim)

    ry -= 40 * mm + 7 * mm
    section_label(c, rx, ry, "Logo Placement")
    ry -= 7 * mm
    ry = spec_rows(c, rx, ry, logo_rows, label_w=30 * mm, val_w=rw - 32 * mm)

    # BOTTOM — trim & construction (full width)
    by = min(yy, ry) - 4 * mm
    if by > 34 * mm:
        section_label(c, col_x, by, "Trim & Construction")
        by -= 7 * mm
        half = (PAGE_W - 2 * MX) / 2
        left = trim[: (len(trim) + 1) // 2]
        right = trim[(len(trim) + 1) // 2:]
        ly = spec_rows(c, col_x, by, left, label_w=26 * mm, val_w=half - 30 * mm)
        spec_rows(c, col_x + half, by, right, label_w=26 * mm, val_w=half - 30 * mm)
    c.showPage()


def _wrap(c, text, font, size, maxw):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, font, size) > maxw and line:
            lines.append(line)
            line = w
        else:
            line = test
    if line:
        lines.append(line)
    return lines


def _short(nm):
    return nm.split(" — ")[0]


# ---- Style data --------------------------------------------------------------
def build():
    c = canvas.Canvas(OUT, pagesize=letter)
    c.setTitle("Elvoro Golf — Hat Design Specifications")
    c.setAuthor("Elvoro Golf")

    page_title(c)
    page_overview(c)

    # EG-HW-01 — Forest Crest Cap (mirrors Forest Star polo)
    page_style(
        c, "EG-HW-01", "Forest Crest Cap — Forest Green", "Forest Green",
        colourway=[
            ("Crown — Forest Green", "#0B232D", FOREST),
            ("Tonal Star", "#1E3F30", HexColor("#1E3F30")),
            ("Visor — Forest Green", "#0B232D", FOREST),
            ("Logo — Gold", "#D4AF37", GOLD),
            ("Closure — Antique Gold", "#D4AF37", GOLD),
        ],
        pattern=[
            ("Type", "Tonal jacquard star on square grid, front & side panels"),
            ("Repeat", "16 mm grid · star 7 mm"),
            ("Colour", "Self-tone #1E3F30 on Forest Green ground"),
            ("Placement", "Straight set, continuous across crown · crest zone kept clear"),
        ],
        fabric=[
            ("Construction", "Structured 6-panel, performance piqué w/ tonal jacquard star"),
            ("Composition", "90% polyester / 10% elastane"),
            ("Weight", "≈ 205 g/m²"),
            ("Finish", "Moisture-wicking · 4-way stretch · UPF 40"),
        ],
        trim=[
            ("Profile", "Mid profile, structured · buckram-backed front two panels"),
            ("Visor", "Pre-curved, 7-row stitch · self-fabric upper, forest undervisor"),
            ("Eyelets", "Self-fabric stitched · one per panel"),
            ("Button", "Fabric-covered self crown button"),
            ("Sweatband", "Moisture-wicking, forest green · woven Elvoro tab"),
            ("Closure", "Antique-gold metal clasp & slide strap"),
            ("Stitching", "Tonal forest · single-needle topstitch"),
            ("Logo", "Embroidery, front centre · metallic gold #D4AF37 satin"),
        ],
        logo_rows=[
            ("Position", "Front centre, panels 1–2"),
            ("Logo height", "≈ 52 mm"),
            ("Drop from crown", "26 mm from top seam"),
            ("Centred", "On front centre seam"),
            ("Application", "Embroidery · Metallic gold satin"),
        ],
        crown=FOREST, pline=HexColor("#1E3F30"), brim=FOREST, logo_c=GOLD, pat_kind="star",
    )

    # EG-HW-02 — Heritage Monogram Cap (mirrors Heritage Monogram polo)
    page_style(
        c, "EG-HW-02", "Heritage Monogram Cap — Bone", "Heritage Bone",
        colourway=[
            ("Crown — Bone", "#E5DCC7", BONE),
            ("Tonal Monogram", "#C8B98F", HexColor("#C8B98F")),
            ("Visor Tipping — Forest", "#0B232D", FOREST),
            ("Logo — Gold", "#D4AF37", GOLD),
            ("Closure — Horn", "#D8C9A6", HexColor("#D8C9A6")),
        ],
        pattern=[
            ("Type", "Tonal woven monogram — 4-point diamond/star on square grid"),
            ("Repeat", "18 mm grid · motif 9 mm"),
            ("Colour", "Tone-on-tone #C8B98F on Bone ground"),
            ("Placement", "All-over, straight set · front crest zone engineered clear"),
        ],
        fabric=[
            ("Construction", "Unstructured 6-panel, performance piqué w/ tonal dobby monogram"),
            ("Composition", "90% polyester / 10% elastane"),
            ("Weight", "≈ 200 g/m²"),
            ("Finish", "Moisture-wicking · dimensional stretch · wrinkle-resist"),
        ],
        trim=[
            ("Profile", "Low profile, soft / unstructured · relaxed crown"),
            ("Visor", "Pre-curved · FOREST GREEN #0B232D twin-line tip on visor edge"),
            ("Eyelets", "Stitched self-fabric · one per panel"),
            ("Button", "Fabric-covered self crown button"),
            ("Sweatband", "Moisture-wicking, bone · forest twin-line bind"),
            ("Closure", "Horn-look slide buckle on bone cotton strap"),
            ("Stitching", "Tonal bone · forest twin-line accent to match polo tipping"),
            ("Logo", "Embroidery, front centre · metallic gold #D4AF37 satin"),
        ],
        logo_rows=[
            ("Position", "Front centre, panels 1–2"),
            ("Logo height", "≈ 50 mm"),
            ("Drop from crown", "28 mm from top seam"),
            ("Centred", "On front centre seam"),
            ("Application", "Embroidery · Metallic gold satin"),
        ],
        crown=BONE, pline=HexColor("#C8B98F"), brim=BONE, logo_c=GOLD, pat_kind="monogram",
    )

    # EG-HW-03 — Founders Stripe Cap (mirrors Double Stripe polo)
    page_style(
        c, "EG-HW-03", "Founders Stripe Cap — Founders White", "Founders White",
        colourway=[
            ("Crown — Founders White", "#F0EDE8", WHITE_F),
            ("Double Stripe — Soft Grey", "#C8C6C1", HexColor("#C8C6C1")),
            ("Visor — Founders White", "#F0EDE8", WHITE_F),
            ("Logo Thread — Navy", "#0B232D", FOREST),
            ("Closure — Pearl", "#FBFAF7", HexColor("#FBFAF7")),
        ],
        pattern=[
            ("Type", "Yarn-dyed DOUBLE feeder stripe — twin pin-stripes grouped in pairs"),
            ("Repeat", "Pair-to-pair 22 mm · 3 mm gap within each pair"),
            ("Line weight", "1.3 mm pin-line (×2 per pair)"),
            ("Colour", "Soft Grey #C8C6C1 on Founders White ground"),
            ("Placement", "Pairs run even & continuous across crown · match across panel seams"),
        ],
        fabric=[
            ("Construction", "Structured 6-panel, performance single-jersey feeder stripe"),
            ("Composition", "88% recycled polyester / 12% elastane"),
            ("Weight", "≈ 180 g/m²"),
            ("Finish", "Moisture-wicking · 4-way stretch · anti-pill · UPF 30"),
        ],
        trim=[
            ("Profile", "Mid profile, structured · rope detail at visor break"),
            ("Visor", "Pre-curved · self-fabric, soft-grey braided rope cord on front seam"),
            ("Eyelets", "Self-fabric stitched · one per panel"),
            ("Button", "Fabric-covered self crown button"),
            ("Sweatband", "Moisture-wicking, white · woven Elvoro tab"),
            ("Closure", "Pearl-white clasp & slide strap"),
            ("Stitching", "Tonal white · single-needle topstitch"),
            ("Logo", "Embroidery, front centre · navy #0B232D satin · alt: soft heat-transfer"),
        ],
        logo_rows=[
            ("Position", "Front centre, panels 1–2"),
            ("Logo height", "≈ 50 mm"),
            ("Drop from crown", "27 mm from top seam"),
            ("Centred", "On front centre seam"),
            ("Application", "Embroidery · Navy satin"),
        ],
        crown=WHITE_F, pline=HexColor("#C8C6C1"), brim=WHITE_F, logo_c=FOREST, pat_kind="stripe",
    )

    c.save()
    print("wrote", OUT)


if __name__ == "__main__":
    build()
