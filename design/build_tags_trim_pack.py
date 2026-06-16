#!/usr/bin/env python3
"""
Elvoro Golf — Tags & Trim Pack
Generates a print-ready design-development PDF: neck label, side-seam tag,
and interior half-moon patch designs. Companion to the Polo Design Draft.
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

A = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(A, "fonts")
IMAGES = os.path.join(A, "assets")
OUT = os.environ.get("OUT", os.path.join(A, "Elvoro-Tags-Trim-Pack.pdf"))

# ---- palette ----
GREEN      = HexColor("#0B232D")
GREEN_DEEP = HexColor("#061319")
GREEN_SOFT = HexColor("#14404A")
GOLD       = HexColor("#D4AF37")
GOLD_DEEP  = HexColor("#B8941F")
CREAM      = HexColor("#F6F2E8")
CREAM_2    = HexColor("#ECE7D9")
STONE      = HexColor("#CFC7B6")
STONE_DEEP = HexColor("#B4A990")
INK        = HexColor("#14242A")
MUTED      = HexColor("#5E6A62")
LINE       = HexColor("#DED7C6")
WHITE      = HexColor("#FFFFFF")

# ---- fonts ----
def rf(name, fn):
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONTS, fn)))
rf("Cor",   "Cormorant-Regular.ttf")
rf("CorM",  "Cormorant-Medium.ttf")
rf("CorSB", "Cormorant-SemiBold.ttf")
rf("CorI",  "Cormorant-Italic-var.ttf")
rf("Sans",  "Inter-Regular.ttf")
rf("SansM", "Inter-Medium.ttf")
rf("SansSB","Inter-SemiBold.ttf")
rf("SansB", "Inter-Bold.ttf")

SERIF, SERIF_M, SERIF_SB, SERIF_I = "Cor", "CorM", "CorSB", "CorI"
SANS, SANS_M, SANS_SB, SANS_B = "Sans", "SansM", "SansSB", "SansB"

W, H = 612.0, 792.0          # US Letter portrait
MX = 54                       # outer margin

def img(name): return ImageReader(os.path.join(IMAGES, name))

# ============ text helpers ============
def tw(c, s, font, size, track=0):
    return pdfmetrics.stringWidth(s, font, size) + track * max(len(s) - 1, 0)

def text(c, x, y, s, font, size, color, track=0, align="l"):
    c.setFillColor(color)
    w = tw(c, s, font, size, track)
    if align == "c": x -= w / 2
    elif align == "r": x -= w
    to = c.beginText(x, y)
    to.setFont(font, size)
    if track: to.setCharSpace(track)
    to.setFillColor(color)
    to.textOut(s)
    c.drawText(to)
    return w

def para(c, x, y, lines, font, size, color, leading, align="l", cx=None):
    for ln in lines:
        if align == "c":
            text(c, cx, y, ln, font, size, color, align="c")
        else:
            text(c, x, y, ln, font, size, color)
        y -= leading
    return y

def hairline(c, x1, y, x2, color=GOLD, w=0.8, alpha=1.0):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(w)
    if alpha < 1: c.setStrokeAlpha(alpha)
    c.line(x1, y, x2, y); c.restoreState()

def place(c, name, cx, cy, w=None, h=None):
    """draw image centered at (cx,cy) preserving aspect; specify w or h."""
    ir = img(name); iw, ih = ir.getSize(); ar = iw / ih
    if w and not h: h = w / ar
    if h and not w: w = h * ar
    c.drawImage(ir, cx - w / 2, cy - h / 2, w, h, mask="auto",
                preserveAspectRatio=True)
    return w, h

def eyebrow(c, x, y, s, color=GOLD_DEEP, align="l", size=8.2):
    return text(c, x, y, s.upper(), SANS_SB, size, color, track=2.6, align=align)

# ============ page furniture ============
def page_bg(c, color):
    c.setFillColor(color); c.rect(0, 0, W, H, fill=1, stroke=0)

def footer(c, idx, label, dark=False):
    col = STONE if dark else MUTED
    acc = GOLD if dark else GOLD_DEEP
    y = 34
    hairline(c, MX, y + 12, W - MX, GOLD if dark else LINE, 0.6,
             0.5 if dark else 1)
    text(c, MX, y, "ELVORO GOLF", SANS_SB, 7, acc, track=1.8)
    text(c, W / 2, y, label.upper(), SANS, 7, col, track=1.8, align="c")
    text(c, W - MX, y, f"{idx:02d} / 06", SANS, 7, col, track=1.4, align="r")

def header(c, eb, title, sub=None, color_eb=GOLD_DEEP, color_t=INK,
           color_s=MUTED):
    eyebrow(c, MX, H - 78, eb, color_eb)
    text(c, MX, H - 116, title, SERIF_SB, 30, color_t)
    if sub:
        text(c, MX, H - 136, sub, SERIF_I, 14, color_s)
    hairline(c, MX, H - 150, W - MX, LINE, 0.8)

# ============ spec block ============
def spec_block(c, x, y, w, title, rows, dark=False):
    """y = top. returns bottom y."""
    label_col = GOLD if dark else GOLD_DEEP
    key_col   = STONE_DEEP if dark else MUTED
    val_col   = CREAM if dark else INK
    line_col  = GOLD if dark else LINE
    eyebrow(c, x, y, title, label_col)
    yy = y - 18
    for k, v in rows:
        hairline(c, x, yy + 12, x + w, line_col, 0.5, 0.4 if dark else 1)
        text(c, x, yy, k.upper(), SANS_SB, 7.2, key_col, track=1.4)
        # value may wrap
        words = v.split(" "); line = ""; vx = x + 92; lines = []
        maxw = w - 96
        for word in words:
            t = (line + " " + word).strip()
            if tw(c, t, SANS, 8.6) > maxw and line:
                lines.append(line); line = word
            else:
                line = t
        if line: lines.append(line)
        for i, ln in enumerate(lines):
            text(c, vx, yy - i * 11, ln, SANS, 8.6, val_col)
        yy -= max(20, 11 * len(lines) + 9)
    return yy

# ============ swatch ============
def swatch(c, x, y, w, h, color, name, hexv, on_dark=False):
    c.setFillColor(color); c.setStrokeColor(GOLD if on_dark else LINE)
    c.setLineWidth(0.6); c.rect(x, y, w, h, fill=1, stroke=1)
    tcol = CREAM if on_dark else INK
    mcol = STONE if on_dark else MUTED
    text(c, x, y - 14, name.upper(), SANS_SB, 7.5, tcol, track=1.2)
    text(c, x, y - 25, hexv, SANS, 7.5, mcol, track=0.6)

# ====================================================================
# garment drawing — stylised technical flats
# ====================================================================
def polo_back(c, ox, oy, s, stroke=GREEN, lw=1.6, fill=None):
    """Back-view polo technical flat. Bottom-left origin (ox,oy), scale s.
       Local box ~ 200 wide x 232 tall."""
    def P(x, y): return (ox + x * s, oy + y * s)
    c.saveState()
    p = c.beginPath()
    # start hem left
    p.moveTo(*P(26, 0))
    p.lineTo(*P(174, 0))                       # hem
    p.lineTo(*P(178, 118))                      # right side seam up
    p.lineTo(*P(150, 150))                      # to underarm right
    p.lineTo(*P(198, 150))                      # sleeve hem right outer
    p.lineTo(*P(190, 182))                      # sleeve top right
    p.lineTo(*P(150, 196))                      # shoulder to neck right
    p.curveTo(*P(135, 205), *P(118, 208), *P(118, 208))  # collar base right
    p.lineTo(*P(132, 232))                      # collar up right
    p.lineTo(*P(68, 232))                       # collar top
    p.lineTo(*P(82, 208))                       # collar down left
    p.curveTo(*P(82, 208), *P(65, 205), *P(50, 196))     # neck to shoulder left
    p.lineTo(*P(10, 182))                       # sleeve top left
    p.lineTo(*P(2, 150))                        # sleeve hem left outer
    p.lineTo(*P(50, 150))                       # underarm left
    p.lineTo(*P(22, 118))                       # left side seam
    p.close()
    if fill is not None:
        c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(lw)
        c.drawPath(p, fill=1, stroke=1)
    else:
        c.setStrokeColor(stroke); c.setLineWidth(lw); c.drawPath(p, stroke=1)
    # collar fold line
    c.setLineWidth(lw * 0.7)
    cp = c.beginPath(); cp.moveTo(*P(82, 214)); cp.lineTo(*P(118, 214))
    c.drawPath(cp, stroke=1)
    # back yoke seam
    yk = c.beginPath(); yk.moveTo(*P(50, 196)); yk.lineTo(*P(150, 196))
    c.setLineWidth(lw * 0.55); c.setDash(2, 2); c.drawPath(yk, stroke=1)
    c.setDash()
    # side vents
    for vx in (26, 174):
        vv = c.beginPath(); vv.moveTo(*P(vx, 0)); vv.lineTo(*P(vx, 16))
        c.setLineWidth(lw * 0.6); c.drawPath(vv, stroke=1)
    c.restoreState()
    return P

# ---- woven main label artwork ----
def neck_label(c, cx, cy, w, fold_tab=True):
    """Centre-fold woven main label, drawn centered at (cx, top-ish cy).
       w = label width. Returns (x0,y0,w,h)."""
    h = w * 0.46
    x0 = cx - w / 2; y0 = cy - h / 2
    c.saveState()
    # ground
    c.setFillColor(GREEN); c.setStrokeColor(GOLD_DEEP); c.setLineWidth(0.8)
    c.roundRect(x0, y0, w, h, 3, fill=1, stroke=0)
    # inner gold keyline
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.roundRect(x0 + 5, y0 + 5, w - 10, h - 10, 2, fill=0, stroke=1)
    # crest
    place(c, "crest_gold.png", cx, y0 + h * 0.66, h=h * 0.40)
    # wordmark
    text(c, cx, y0 + h * 0.30, "ELVORO", SERIF_SB, w * 0.135, GOLD,
         track=w * 0.012, align="c")
    text(c, cx, y0 + h * 0.155, "GOLF", SANS_M, w * 0.045, GOLD,
         track=w * 0.030, align="c")
    # top sew line (stitch dots) — caught in collar seam
    c.setFillColor(GOLD_DEEP)
    n = 26
    for i in range(n):
        sx = x0 + 6 + (w - 12) * i / (n - 1)
        c.circle(sx, y0 + h - 2.0, 0.5, fill=1, stroke=0)
    c.restoreState()
    return x0, y0, w, h

# ---- side seam folded tab ----
def side_tab(c, cx, cy, w):
    """Folded woven loop tab (crest only) drawn centered at (cx,cy)."""
    h = w * 2.5
    x0 = cx - w / 2; y0 = cy - h / 2
    c.saveState()
    c.setFillColor(GREEN); c.setStrokeColor(GOLD_DEEP); c.setLineWidth(0.7)
    c.roundRect(x0, y0, w, h, 2.5, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(0.6)
    c.roundRect(x0 + 3, y0 + 3, w - 6, h - 6, 2, fill=0, stroke=1)
    place(c, "crest_gold.png", cx, cy, h=w * 0.62)
    c.restoreState()
    return x0, y0, w, h

# ---- half-moon patch ----
def half_moon(c, cx, cy, w, ground, edge, logo_img, wordmark=True,
              word_col=None, tonal=False):
    """Half-moon (D shape, flat side up) patch centered at (cx,cy)."""
    r = w / 2; h = r
    c.saveState()
    p = c.beginPath()
    p.moveTo(cx - r, cy + 1)
    p.lineTo(cx + r, cy + 1)
    # semicircle down
    k = 0.5523 * r
    p.curveTo(cx + r, cy + 1 - k, cx + k, cy + 1 - r, cx, cy + 1 - r)
    p.curveTo(cx - k, cy + 1 - r, cx - r, cy + 1 - k, cx - r, cy + 1)
    p.close()
    c.setFillColor(ground)
    c.setStrokeColor(edge); c.setLineWidth(1.0)
    c.drawPath(p, fill=1, stroke=1)
    # top straight stitch (sew edge over neck seam)
    c.setStrokeColor(edge); c.setLineWidth(0.5); c.setDash(2.2, 2.2)
    c.line(cx - r + 4, cy - 3, cx + r - 4, cy - 3)
    c.setDash()
    # crest
    place(c, logo_img, cx, cy - r * 0.34, h=r * 0.44)
    if wordmark:
        text(c, cx, cy - r * 0.62, "ELVORO GOLF", SANS_SB, r * 0.115,
             word_col, track=r * 0.022, align="c")
    c.restoreState()

# ====================================================================
# PAGES
# ====================================================================
c = canvas.Canvas(OUT, pagesize=(W, H))
c.setTitle("Elvoro Golf — Tags & Trim Pack")
c.setAuthor("Elvoro Golf")
c.setSubject("Label, side tag & half-moon trim designs")

# ---------- PAGE 1 — COVER ----------
page_bg(c, GREEN)
# corner watermark crest (clipped inside the frame)
c.saveState()
fp = c.beginPath(); fp.rect(MX - 16, 46, W - 2 * (MX - 16), H - 92)
c.clipPath(fp, stroke=0); c.setFillAlpha(0.9)
place(c, "crest_greensoft.png", W - 36, 120, w=300)
c.restoreState()
# frame
c.setStrokeColor(GOLD); c.setLineWidth(1.0)
c.rect(MX - 16, 46, W - 2 * (MX - 16), H - 92, fill=0, stroke=1)
c.setStrokeColor(GOLD_DEEP); c.setLineWidth(0.5)
c.rect(MX - 11, 51, W - 2 * (MX - 11), H - 102, fill=0, stroke=1)

place(c, "crest_gold.png", W / 2, H - 232, w=132)
eyebrow(c, W / 2, H - 312, "Elvoro Golf  ·  Design Development", GOLD,
        align="c", size=9)
text(c, W / 2, H - 372, "Tags & Trim Pack", SERIF_SB, 56, CREAM, align="c")
hairline(c, W / 2 - 60, H - 392, W / 2 + 60, GOLD, 0.8)
para(c, 0, H - 420,
     ["Woven main label · side-seam tag · interior half-moon.",
      "A companion to the Polo Design Draft."],
     SERIF_I, 13.5, STONE, 20, align="c", cx=W / 2)

# palette row
labels = [("Forest", "#0B232D", GREEN_SOFT), ("Gold", "#D4AF37", GOLD),
          ("Cream", "#F6F2E8", CREAM), ("Stone", "#CFC7B6", STONE)]
sw = 96; gap = 18; total = 4 * sw + 3 * gap; sx = (W - total) / 2; sy = 168
for i, (nm, hx, col) in enumerate(labels):
    x = sx + i * (sw + gap)
    c.setFillColor(col); c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.rect(x, sy, sw, 44, fill=1, stroke=1)
    text(c, x, sy - 14, nm.upper(), SANS_SB, 7.5, CREAM, track=1.4)
    text(c, x, sy - 25, hx, SANS, 7.5, STONE, track=0.6)
eyebrow(c, W / 2, 96, "Confidential — for design development  ·  June 2026",
        STONE_DEEP, align="c", size=7.5)
c.showPage()

# ---------- PAGE 2 — PLACEMENT MAP ----------
page_bg(c, CREAM)
header(c, "Orientation", "Where each trim sits",
       "Back view — three brand touch-points, one quiet system.")
# polo flat
P = polo_back(c, 150, 250, 1.18, stroke=GREEN, lw=1.6, fill=WHITE)
# markers
def marker(c, px, py, tx, ty, label, desc, side="r"):
    c.setFillColor(GOLD); c.setStrokeColor(GOLD); c.setLineWidth(0.9)
    c.circle(px, py, 3.0, fill=1, stroke=0)
    c.line(px, py, tx, ty)
    ax = tx if side == "r" else tx
    al = "l" if side == "r" else "r"
    c.circle(tx, ty, 1.4, fill=1, stroke=0)
    text(c, ax + (6 if side == "r" else -6), ty + 3, label, SANS_SB, 9,
         INK, track=0.8, align=al)
    text(c, ax + (6 if side == "r" else -6), ty - 9, desc, SANS, 7.6,
         MUTED, align=al)
# behind-neck label point (collar centre)
nx, ny = P(100, 222)
marker(c, nx, ny, W - 150, H - 250, "01 · Main label",
       "Inside centre-back collar", "r")
# half-moon point (just below collar)
hx, hy = P(100, 192)
marker(c, hx, hy, W - 150, H - 320, "03 · Half-moon",
       "Interior back-neck seam", "r")
# side tag point (left side seam, lower) — label routed into empty lower-left
sxp, syp = P(23, 34)
c.setFillColor(GOLD); c.setStrokeColor(GOLD); c.setLineWidth(0.9)
c.circle(sxp, syp, 3.0, fill=1, stroke=0)
lx, ly = 120, 196
c.line(sxp, syp, lx, ly); c.circle(lx, ly, 1.4, fill=1, stroke=0)
text(c, MX, ly + 3, "02 · Side tag", SANS_SB, 9, INK, track=0.8)
text(c, MX, ly - 9, "Left side seam", SANS, 7.6, MUTED)
text(c, MX, ly - 19, "≈ 11 cm above hem", SANS, 7.6, MUTED)
# small caption box
ty = 150
eyebrow(c, MX, ty, "Principle", GOLD_DEEP)
para(c, MX, ty - 16,
     ["Branding is restrained and consistent: the crest leads, the wordmark",
      "supports, gold on forest throughout. Nothing shouts — every mark is",
      "felt on the inside as much as it is seen on the outside."],
     SANS, 9, INK, 13)
footer(c, 2, "Placement map")
c.showPage()

# ---------- PAGE 3 — NECK / MAIN LABEL ----------
page_bg(c, CREAM)
header(c, "Tag 01 · Main label", "Behind-the-neck label",
       "Centre-fold woven label, caught in the collar seam.")
# big artwork on a tonal stage
stage_y = H - 360
c.setFillColor(CREAM_2); c.setStrokeColor(LINE); c.setLineWidth(0.8)
c.roundRect(MX, stage_y - 40, W - 2 * MX, 232, 6, fill=1, stroke=1)
neck_label(c, W / 2, stage_y + 96, 250)
eyebrow(c, W / 2, stage_y - 22, "Woven label — shown at ~ 2× scale",
        MUTED, align="c", size=7.5)
# context mock — inside collar with label
mock_cx = 165; mock_cy = H - 470
c.saveState()
# collar band (inside)
c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.2)
cp = c.beginPath()
cp.moveTo(mock_cx - 95, mock_cy + 26)
cp.curveTo(mock_cx - 40, mock_cy - 8, mock_cx + 40, mock_cy - 8,
           mock_cx + 95, mock_cy + 26)
cp.lineTo(mock_cx + 95, mock_cy + 46)
cp.curveTo(mock_cx + 40, mock_cy + 12, mock_cx - 40, mock_cy + 12,
           mock_cx - 95, mock_cy + 46)
cp.close(); c.drawPath(cp, fill=1, stroke=1)
# neck tape
c.setFillColor(GREEN)
tp = c.beginPath()
tp.moveTo(mock_cx - 95, mock_cy + 6)
tp.curveTo(mock_cx - 40, mock_cy - 26, mock_cx + 40, mock_cy - 26,
           mock_cx + 95, mock_cy + 6)
tp.lineTo(mock_cx + 95, mock_cy - 2)
tp.curveTo(mock_cx + 40, mock_cy - 34, mock_cx - 40, mock_cy - 34,
           mock_cx - 95, mock_cy - 2)
tp.close(); c.drawPath(tp, fill=1, stroke=0)
c.restoreState()
neck_label(c, mock_cx, mock_cy - 34, 96)
eyebrow(c, mock_cx, mock_cy - 78, "In place · inside collar", MUTED,
        align="c", size=7.5)
# spec
spec_block(c, W / 2 + 26, H - 452, W / 2 - MX - 26, "Specification", [
    ("Finished", "50 × 22 mm (centre-fold, sewn at top edge)"),
    ("Type", "Woven damask label, satin weave"),
    ("Ground", "Forest #0B232D"),
    ("Logo / text", "Gold #D4AF37 — crest, ELVORO wordmark, GOLF"),
    ("Placement", "Centred at centre-back, caught in collar seam"),
    ("Care side", "Reverse: size, fibre, care, country of origin"),
])
footer(c, 3, "Main label")
c.showPage()

# ---------- PAGE 4 — SIDE TAG ----------
page_bg(c, CREAM)
header(c, "Tag 02 · Side mark", "Side-seam tag",
       "A small folded loop — the crest, glimpsed from the side.")
# stage with folded tab + flat
stage_y = H - 360
c.setFillColor(CREAM_2); c.setStrokeColor(LINE); c.setLineWidth(0.8)
c.roundRect(MX, stage_y - 40, W - 2 * MX, 232, 6, fill=1, stroke=1)
# folded loop (left)
side_tab(c, MX + 120, stage_y + 86, 34)
eyebrow(c, MX + 120, stage_y - 22, "Folded loop", MUTED, align="c", size=7.5)
# unfolded flat (right) — crest mirrored across fold line
ux = W - MX - 150; uy = stage_y + 86; uw = 150; uh = 60
c.setFillColor(GREEN); c.setStrokeColor(GOLD_DEEP); c.setLineWidth(0.7)
c.roundRect(ux - uw / 2, uy - uh / 2, uw, uh, 3, fill=1, stroke=0)
c.setStrokeColor(GOLD); c.setLineWidth(0.5)
c.setDash(2, 2); c.line(ux, uy - uh / 2 + 4, ux, uy + uh / 2 - 4); c.setDash()
place(c, "crest_gold.png", ux - uw / 4, uy, h=uh * 0.6)
place(c, "crest_gold.png", ux + uw / 4, uy, h=uh * 0.6)
eyebrow(c, ux, stage_y - 22, "Opened flat (fold at centre)", MUTED,
        align="c", size=7.5)
# context mock — lower-left side seam with tab
mx0 = 150; my0 = H - 540
c.saveState()
c.setFillColor(WHITE); c.setStrokeColor(GREEN); c.setLineWidth(1.2)
c.rect(mx0, my0, 150, 120, fill=1, stroke=0)
# side seam (left edge) + hem
c.setStrokeColor(GREEN); c.setLineWidth(1.4)
c.line(mx0, my0, mx0, my0 + 120)           # side seam
c.line(mx0, my0, mx0 + 150, my0)            # hem
c.setStrokeColor(GREEN); c.setLineWidth(0.5); c.setDash(2, 2)
c.line(mx0 + 5, my0 + 8, mx0 + 145, my0 + 8)
c.setDash()
c.restoreState()
# tab protruding from seam ~ 11cm up
side_tab(c, mx0 - 2, my0 + 70, 16)
text(c, mx0 + 16, my0 + 70, "← side tag", SANS, 8, MUTED)
text(c, mx0 + 16, my0 + 12, "hem", SANS, 7.5, MUTED)
eyebrow(c, mx0 + 75, my0 - 16, "Lower-left side seam", MUTED, align="c",
        size=7.5)
# spec
spec_block(c, W / 2 + 26, H - 452, W / 2 - MX - 26, "Specification", [
    ("Finished", "12 × 22 mm folded loop (45 mm opened)"),
    ("Type", "Woven loop tag, fold at centre"),
    ("Ground", "Forest #0B232D"),
    ("Mark", "Gold crest only — no wordmark"),
    ("Placement", "Left side seam, ~11 cm above hem"),
    ("Attach", "Caught in seam, bartacked at fold"),
])
footer(c, 4, "Side tag")
c.showPage()

# ---------- PAGE 5 — HALF-MOON ----------
page_bg(c, CREAM)
header(c, "Interior · Half-moon", "Back-neck half-moon",
       "The moon patch that finishes the neckline — three treatments.")
stage_y = H - 372
c.setFillColor(CREAM_2); c.setStrokeColor(LINE); c.setLineWidth(0.8)
c.roundRect(MX, stage_y - 52, W - 2 * MX, 244, 6, fill=1, stroke=1)
# three variants
cols = [MX + 92, W / 2, W - MX - 92]
yv = stage_y + 96
half_moon(c, cols[0], yv, 150, GREEN, GOLD, "crest_gold.png",
          word_col=GOLD)
half_moon(c, cols[1], yv, 150, CREAM, GREEN, "crest_green.png",
          word_col=GREEN)
half_moon(c, cols[2], yv, 150, GREEN, GREEN_SOFT, "crest_greensoft.png",
          word_col=GREEN_SOFT)
names = [("A · Primary", "Forest twill / gold"),
         ("B · Light", "Cream twill / forest"),
         ("C · Tonal", "Forest on forest")]
for cx, (nm, ds) in zip(cols, names):
    text(c, cx, stage_y - 14, nm, SANS_SB, 8.5, INK, track=0.6, align="c")
    text(c, cx, stage_y - 26, ds, SANS, 7.6, MUTED, align="c")
eyebrow(c, W / 2, stage_y - 44, "Half-moon patch — shown at ~ 1.4× scale",
        MUTED, align="c", size=7.5)
# spec
spec_block(c, MX, H - 470, W - 2 * MX, "Specification", [
    ("Shape", "Half-moon (D), flat edge up · ~120 × 45 mm finished"),
    ("Material", "Brushed cotton twill, folded edges"),
    ("Branding", "Embroidered or printed crest + ELVORO GOLF arc"),
    ("Placement", "Centred, flat edge to centre-back neck seam"),
    ("Attach", "Edge-stitched over the neck seam, covering the tape"),
])
footer(c, 5, "Half-moon")
c.showPage()

# ---------- PAGE 6 — TRIM SCHEDULE ----------
page_bg(c, GREEN)
c.saveState()
fp = c.beginPath(); fp.rect(0, 0, W, H); c.clipPath(fp, stroke=0)
place(c, "crest_greensoft.png", W - 30, 130, w=300)
c.restoreState()
eyebrow(c, MX, H - 78, "Summary", GOLD)
text(c, MX, H - 116, "Trim schedule", SERIF_SB, 30, CREAM)
text(c, MX, H - 136, "Everything in one view.", SERIF_I, 14, STONE)
hairline(c, MX, H - 150, W - MX, GOLD, 0.8, 0.6)
# table
heads = ["Ref", "Element", "Size", "Material", "Colour", "Placement"]
xcols = [MX, MX + 36, MX + 132, MX + 212, MX + 300, MX + 388]
wmaxs = [32, 90, 74, 84, 82, 116]
ty = H - 178
for hd, xx in zip(heads, xcols):
    text(c, xx, ty, hd.upper(), SANS_SB, 7.4, GOLD, track=1.2)
hairline(c, MX, ty - 8, W - MX, GOLD, 0.6, 0.6)
rows = [
    ("01", "Main label", "50×22 mm", "Woven damask", "Forest / gold",
     "Inside collar · CB"),
    ("02", "Side tag", "12 mm loop", "Woven loop", "Forest / gold",
     "Left side seam"),
    ("03", "Half-moon", "120×45 mm", "Cotton twill", "3 colourways",
     "Back-neck, interior"),
]
ry = ty - 28
for r in rows:
    maxlines = 1
    for val, xx, wmax in zip(r, xcols, wmaxs):
        words = val.split(" "); line = ""; lines = []
        for word in words:
            t = (line + " " + word).strip()
            if tw(c, t, SANS, 8.4) > wmax and line:
                lines.append(line); line = word
            else:
                line = t
        if line: lines.append(line)
        maxlines = max(maxlines, len(lines))
        for i, ln in enumerate(lines):
            col = GOLD if xx == MX else CREAM
            fnt = SANS_SB if xx == MX else SANS
            text(c, xx, ry - i * 11, ln, fnt, 9 if xx == MX else 8.4, col)
    step = 18 + 11 * (maxlines - 1)
    hairline(c, MX, ry - step + 4, W - MX, GREEN_SOFT, 0.5, 0.8)
    ry -= step + 12
# palette
py = ry - 22
eyebrow(c, MX, py, "Palette", GOLD)
pl = [("Forest", "#0B232D", GREEN_SOFT), ("Gold", "#D4AF37", GOLD),
      ("Cream", "#F6F2E8", CREAM), ("Stone", "#CFC7B6", STONE)]
px = MX
for nm, hx, col in pl:
    c.setFillColor(col); c.setStrokeColor(GOLD); c.setLineWidth(0.5)
    c.rect(px, py - 52, 84, 34, fill=1, stroke=1)
    text(c, px, py - 64, nm.upper(), SANS_SB, 7, CREAM, track=1)
    text(c, px, py - 74, hx, SANS, 7, STONE)
    px += 100
# typography (stacked below palette)
ty2 = py - 108
eyebrow(c, MX, ty2, "Typography", GOLD)
text(c, MX, ty2 - 26, "Cormorant Garamond", SERIF_SB, 19, CREAM)
text(c, MX, ty2 - 40, "Editorial serif — wordmark & headings", SANS, 8, STONE)
text(c, MX + 270, ty2 - 24, "Inter", SANS_SB, 15, CREAM)
text(c, MX + 270, ty2 - 40, "Labels, specifications & supporting text",
     SANS, 8, STONE)
footer(c, 6, "Trim schedule", dark=True)
c.showPage()

c.save()
print("WROTE", OUT)
