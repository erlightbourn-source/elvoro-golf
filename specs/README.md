# Elvoro Golf — Design Specification Packs

Technical specification packs for the manufacturing team, in the house style
of the original **Polo Design Specifications** pack.

## Hat Design Specifications

`Elvoro_Hat_Design_Specs.pdf` — the **Founders Collection — Headwear** drop
(SS26). Built to parallel the three Founders polos, sharing colourway, motif,
and logo language so the caps merchandise alongside them.

| Style | Code | Mirrors polo |
| --- | --- | --- |
| Forest Crest Cap — Forest Green | `EG-HW-01` | Forest Star (`EG-ST-03`) |
| Heritage Monogram Cap — Bone | `EG-HW-02` | Heritage Monogram (`EG-HM-02`) |
| Founders Stripe Cap — Founders White | `EG-HW-03` | Double Stripe (`EG-FC-01`) |

Each style page carries the same fields as the polo pack — Colourway,
Pattern / Print, Fabric, Trim & Construction, Logo Placement — plus front and
side production mockups. The master brand palette (Forest Green `#0B232D`,
Heritage Gold `#D4AF37`, Bone `#E5DCC7`, Founders White `#F0EDE8`) is carried
over unchanged.

### Regenerating

```bash
pip install reportlab pillow
python3 specs/build_hat_specs.py
```

The script pulls the official crest from `assets/brand/` and renders the
five-page pack to `Elvoro_Hat_Design_Specs.pdf`. Edit the style data near the
bottom of `build_hat_specs.py` to adjust colourways, patterns, or trim.
