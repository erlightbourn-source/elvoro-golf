# Elvoro Golf — Tags & Trim Pack

A print-ready design-development PDF covering the polo's **branding trims**, a
companion to the Polo Design Draft.

## Deliverable
- **`Elvoro-Tags-Trim-Pack.pdf`** — 6-page, US-Letter pack:
  1. **Cover** — title, palette.
  2. **Placement map** — back-view flat showing where each trim sits.
  3. **Tag 01 · Main label** — centre-fold woven label, sewn *behind the neck*
     (inside centre-back collar). Artwork + in-collar mock + spec.
  4. **Tag 02 · Side tag** — folded woven loop on the *left side seam*
     (crest only). Folded + opened views + side-seam mock + spec.
  5. **Half-moon** — interior back-neck half-moon patch in three treatments
     (forest/gold, cream/forest, tonal forest-on-forest).
  6. **Trim schedule** — summary table, palette and typography reference.

## Brand
Forest `#0B232D` · Gold `#D4AF37` · Cream `#F6F2E8` · Stone `#CFC7B6`.
Type: Cormorant Garamond (headings/wordmark) + Inter (labels/specs) — the same
system as the website.

> Dimensions, materials and placements are starting specs for development;
> confirm exact sizes and attach methods with the manufacturer before sampling.

## Regenerate
```bash
cd design
pip install reportlab pillow
python3 build_tags_trim_pack.py        # writes Elvoro-Tags-Trim-Pack.pdf
```
Fonts (`fonts/`) and crest artwork (`assets/`) are vendored so the build needs
no network. The crest PNGs are recoloured from `../assets/brand/elvoro-logo.png`.
