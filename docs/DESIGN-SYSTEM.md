# Elvoro Golf static site — Design System

Written 2026-11-19 from `assets/styles.css` (733 lines, one stylesheet, no build step) at `main` `80df6f2`. If this file and the CSS disagree, the CSS wins.

## Brand source of truth
Brand colors, type and voice live in the **`elvoro-brand-guidelines` skill**. Read it before styling anything Elvoro-branded. This file only records what the stylesheet implements today.

## Look
Forest green, warm cream and gold. Serif headings, sans body, generous spacing (`assets/styles.css` header: "Substance over flash").

## Tokens (`:root`, `assets/styles.css` lines 7-39)
| Token | Value | Note |
|---|---|---|
| `--navy` | `#0B232D` | primary forest green (the name is a legacy; the value is green) |
| `--navy-deep` | `#061319` | near-black green, button text on gold |
| `--navy-soft` | `#14404A` | lifted green for gradients |
| `--off-white` | `#F6F2E8` | page background, warm cream |
| `--white` | `#FFFFFF` | |
| `--stone`, `--stone-light`, `--stone-deep` | `#CFC7B6`, `#ECE7D9`, `#B4A990` | neutrals |
| `--olive`, `--olive-soft` | `#C9A227`, `#D4AF37` | legacy names, gold values |
| `--gold`, `--gold-deep` | `#D4AF37`, `#B8941F` | accent; `--gold-deep` is used for eyebrow text on light |
| `--ink`, `--muted` | `#14242A`, `#5E6A62` | body text, secondary text |
| `--line`, `--line-dark` | `#DED7C6`, `rgba(212,175,55,0.18)` | hairlines |
| `--serif` | Cormorant Garamond, Georgia | headings |
| `--sans` | Inter, system sans | body |
| `--maxw`, `--gutter`, `--section` | `1240px`, `clamp(20px,5vw,64px)`, `clamp(72px,11vw,152px)` | layout rhythm |
| `--ease` | `cubic-bezier(0.22,1,0.36,1)` | motion |
A second `:root` block (around line 508) adds `--charcoal`, `--warm-gray`, `--announce-h` (38px), `--shadow-soft`, `--shadow-card`.

## Fonts
Loaded from Google Fonts in each page `<head>` (`index.html` line 10): Cormorant Garamond 400/500/600 and Inter 400/500/600.

## Components
- **Buttons** (lines 91-114, audit E8, 2026-11-11): primary is gold fill with `--navy-deep` text, 52px min height, uppercase, 0.14em tracking (`.btn`, `.btn--gold`). Secondary is a 1px outline: `.btn--outline-light` on dark, `.btn--ghost` on light.
- **Layout helpers:** `.wrap`, `.section`, `.stack-sm`, `.stack-md`, `.measure`, `.eyebrow`, `.lede`, `.display`.
- **Product cards:** `.product-card`, `.product-shot` with a hover `.shot-alt` image, `.swatches`.
- **Signup form:** `.field-row` (input plus button), `.form-success` with `role="status"`.

## Accessibility and motion
A global `:focus-visible` rule covers links, buttons and inputs (line 674). `prefers-reduced-motion` hides the hero and coming-soon video and stops the hero animation (lines 220 and 445). Breakpoints in use: 480, 560, 680, 720, 820, 900px.
