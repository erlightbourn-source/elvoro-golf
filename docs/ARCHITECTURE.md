# Elvoro Golf static site — Architecture

Written 2026-11-19 from this repo at `main` `80df6f2`, the GitHub Pages API, and live header checks the same day.

## Status: dormant fallback
`https://elvorogolf.com/` is served by **Shopify**, not this repo. Verified 2026-11-19: its `robots.txt` begins "# Shopify storefront" and the response carries Shopify timing headers. The live theme is a separate repo (`~/Movies/elvoro-shopify-theme`, Liquid). This repo is a static fallback and the source of the pre-launch copy; treat edits here as not live.

## Stack
Plain HTML files at the repo root, one stylesheet `assets/styles.css`, one script `assets/site.js` (signup forms, scroll reveal, source attribution). No framework, no build step, no package manager, no tests. Images and video sit in `assets/` (hero, polos, `assets/og/` share images, `assets/brand/` logos).

## Hosting and publish path
- Repo: `github.com/erlightbourn-source/elvoro-golf`, **public** (`gh repo view`, 2026-11-19).
- GitHub Pages is **enabled**: `gh api repos/erlightbourn-source/elvoro-golf/pages` returned `status: built`, `build_type: legacy`, source branch `main`, path `/`, `cname: elvorogolf.com`. A push to `main` rebuilds Pages.
- `.nojekyll` is tracked, so Pages serves tracked files as-is. There is no `.gitattributes`, no export rules and no build config, so **every tracked file is published by Pages, including anything under `docs/`**.
- `CNAME` contains `elvorogolf.com`. `.gitignore` says it is held out of deploy, but the file is tracked, so it is in the published tree.
- The domain now points at Shopify, so the Pages origin redirects: `https://erlightbourn-source.github.io/elvoro-golf/...` answers 301 to `http://elvorogolf.com/...` (checked for `docs/ARCHITECTURE.md`; `https://elvorogolf.com/docs/ARCHITECTURE.md` then answers 302 from Shopify, not file content). So the docs are not readable on the site today, but they are readable on GitHub because the repo is public. The Pages certificate state is `bad_authz` (not fixed here).
- History: commit `3195554` (2026-09-22) unpublished `CLAUDE.md`, `README.md`, `MAILCHIMP-SETUP.md` and `marketing/*.md` after they were served publicly. They are now ignored at the root (`.gitignore`), which is why the docs live in tracked `docs/` here.

## Third-party calls
| Piece | Where | Role |
|---|---|---|
| FormSubmit.co | `assets/site.js` (`FORM_ENDPOINT`) | Delivers each signup to Evan's inbox |
| Mailchimp | `assets/site.js` (`MAILCHIMP.action`, empty) | Not wired; falls back to FormSubmit |
| Google Fonts | each page `<head>` | Cormorant Garamond and Inter |
| Cloudflare Web Analytics | beacon at the end of each page | Traffic counts |

## SEO plumbing
`sitemap.xml` (10 URLs), `robots.txt` (points at `https://elvorogolf.com/sitemap.xml`, disallows `/coming-soon.html`), `.well-known/security.txt`, canonical tags on `https://elvorogolf.com/...`, JSON-LD on the home, shop and product pages.

## Verifying a change
No test suite. Check HTML with Python `html.parser` (0 mismatched tags), grep for broken relative links, and open the page at 390px and desktop width with `python3 -m http.server`. A branch is not a deploy: only a push to `main` rebuilds Pages, and the live domain is Shopify anyway.
