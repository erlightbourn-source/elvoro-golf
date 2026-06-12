# Elvoro Golf — Website

Premium, quiet-luxury marketing + storefront site for **Elvoro Golf™**. Hand-built static HTML/CSS/JS — fast, portable, and structured to port cleanly into a Shopify theme.

## Run it
Open `index.html` in a browser, or serve the folder:
```bash
cd elvoro-golf && python3 -m http.server 8000
# → http://localhost:8000
```

## Pages
| File | Purpose |
|------|---------|
| `index.html` | Home — full-bleed hero, value strip, featured polos, editorial split, email capture |
| `shop.html` | Collection — 3 polos, signature product detail, fabric/fit/care |
| `about.html` | Founder voice, brand principles |
| `contact.html` | Contact form (with honeypot), support details, wholesale |
| `coming-soon.html` | Pre-launch gate — email capture + password store-preview modal |
| `policies.html` | Shipping · Returns · Privacy · Terms (anchored) |
| `assets/` | `styles.css`, `site.js`, `elvoro-logo.svg` |

## Design tokens (in `assets/styles.css` `:root`)
- **Navy** `#16243A` (primary) · deep `#0F1A2B`
- **Off-white** `#F6F3EC` · **White** `#FFFFFF`
- **Stone** `#CFC7B6` · light `#E5DFD2` · deep `#B4A990`
- **Olive accent** `#5E6B4F` (used sparingly)
- **Type:** Cormorant Garamond (editorial serif headlines) + Inter (body), via Google Fonts

> These are placeholders tuned to the brief. **Lock exact HEX from the final logo** and swap the `:root` values — everything cascades.

## What to supply (drops straight in)
- **Logo:** replace `assets/elvoro-logo.svg` and the inline header mark; add light/dark PNG + SVG
- **Photography:** every `.hero-media`, `.split-media`, and `.product-shot` has a `PHOTO SLOT` comment showing exactly where to add `<img>`. They currently render as tasteful tonal placeholders so the layout is photo-ready, not photo-dependent.
- **Copy:** product names/descriptions/fabric/pricing in `shop.html` + `index.html`; founder story in `about.html`
- **Forms:** `site.js` stubs submissions client-side. Wire `form[data-capture]` to Klaviyo/Shopify and `form[data-contact]` to your provider.

## "Protected" scope (from brief) — status
- **Pre-launch:** `coming-soon.html` delivers email capture + a password store-preview modal. On Shopify, use the native password page (Online Store → Preferences) and a Coming Soon theme/section; this page mirrors that UX.
- **Legal/IP:** ™ used throughout (name + logo); footer copyright; Privacy/Terms/Returns/Shipping live in `policies.html`. Register the trademark and have counsel finalize policy copy before launch.
- **Security:** ship over **HTTPS** (free via Shopify/host); checkout is **PCI-compliant** when on Shopify native checkout. Contact form includes a honeypot; enable Shopify/host spam protection (reCAPTCHA) too.
- **Brand:** secure domain variants (`.com`, `.co`, common misspellings) + social handles before launch.

## Recommended platform
**Shopify** — bundles pre-launch gating, PCI checkout, and policy tooling. This codebase maps 1:1 to Shopify sections/Liquid: header/footer → `sections/`, product grid → a product collection loop, capture forms → Shopify customer/newsletter forms.

## Notes
- Subtle motion only (scroll reveals, hover); honors `prefers-reduced-motion`.
- Fully responsive; minimal 4-item nav; lots of whitespace.
- No stock graphics, neon, countdown timers, or pop-ups — per brand guardrails.
