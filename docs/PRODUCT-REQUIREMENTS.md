# Elvoro Golf static site — Product Requirements

Written 2026-11-19 from this repo at `main` `80df6f2`. Unknowns are marked **TBD (not in code)**. Status: **dormant fallback**. `elvorogolf.com` is served by the Shopify store (see ARCHITECTURE.md), not by this repo.

## What it is
A static brand and pre-launch site for Elvoro Golf, a menswear brand "built on fit and fabric" (`assets/styles.css` header). Positioning line on the home page: "Confidence, worn well." (`index.html` H1). Performance golf polos, "no loud logos" (JSON-LD description in `index.html`).

## Users
| User | Goal |
|---|---|
| Visitor from IG/TikTok | See the product, learn the brand, join the list |
| Prospective buyer | Read fit and fabric, pick a size, get notified at launch |

## Pages (13 HTML files at the repo root)
Home `index.html`; shop `shop.html`; two products `product-evergreen.html` and `product-meridian.html`; `fit-fabric.html`; `about.html`; `contact.html`; `policies.html`; `privacy.html`; `terms.html`; `journal.html` (`noindex,follow`); `coming-soon.html` and `404.html` (both `noindex`). `sitemap.xml` lists 10 URLs; `robots.txt` disallows `/coming-soon.html`.

## Core flows
1. **Waitlist signup.** Email forms on `index.html`, `shop.html`, `about.html`, `contact.html`, `journal.html`, `coming-soon.html` and both product pages post through `assets/site.js` to FormSubmit.co, with email, optional size and product, a hidden honeypot field `company`, and a first-touch source (`ev_src`).
2. **Mailchimp (off).** `MAILCHIMP.action` in `assets/site.js` is an empty string, so Mailchimp is not wired; signups go to FormSubmit only.
3. **Browse.** Shop grid to product pages; product cards say "View & get notified", so there is no checkout on this site.

## Commerce facts on the pages
Both polos are listed at $60 (`shop.html`, `product-*.html`; `product-meridian.html` JSON-LD marks it `PreOrder`). Returns: 30 days from delivery for unworn items (`policies.html`). Operator is named as EV Tech Solutions LLC in `policies.html` (commit `7b5858d`).

## Requirements that still apply
- One H1 per page, a meta description, a canonical URL, and `noindex` on non-public pages (`coming-soon.html`, `404.html`, `journal.html`).
- No invented claims, prices or reviews. Fabric specs are marked "confirming soon" on the Meridian page; leave unconfirmed specs out.
- Privacy page must describe anything stored: `ev_src` is kept in sessionStorage and localStorage for 30 days, no cookies (`assets/site.js` lines 86-91, `privacy.html`, commit `c3d3ec1`).

## Non-goals
No checkout, accounts, database or server code on this repo. Selling happens on Shopify.

## Success metrics
**TBD (not in code).** The pages carry a Cloudflare Web Analytics beacon (bottom of `index.html`), but no targets are written down here.
