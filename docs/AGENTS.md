# AGENTS.md — working in elvoro-golf (static fallback site)

For AI agents. Read `docs/ARCHITECTURE.md`, `docs/DESIGN-SYSTEM.md` and `docs/PRODUCT-REQUIREMENTS.md` first. Written 2026-11-19.

## Hard rules
1. **This repo is public and GitHub Pages publishes every tracked file.** There is no export rule or build step (see ARCHITECTURE.md). Anything under `docs/` is visible on GitHub and would be served if the domain pointed back at Pages. Put no secrets, inbox addresses, unreleased pricing or marketing drafts in any tracked file. Local-only notes go in `.claude/`, which `.gitignore` excludes.
2. **Do not treat this repo as the live store.** `elvorogolf.com` is Shopify. Live theme changes follow the Shopify theme repo's own process (`dev_theme_action.sh`), not a push here.
3. **Never push to `main` and never merge.** Work on a branch, open a PR with `gh pr create`. A push to `main` rebuilds GitHub Pages. Merges happen on Evan's tap.
4. **Brand work uses the `elvoro-brand-guidelines` skill.** Outward brand changes need Evan's approval.
5. **No invented claims, prices or reviews.** Prices on the pages are $60 per polo today; fabric specs still marked "confirming soon" stay that way until confirmed.
6. **Do not touch `assets/site.js` `FORM_ENDPOINT`** or paste any Mailchimp keys. The privacy page must match what the script stores (`ev_src`, 30 days, no cookies); update `privacy.html` in the same PR if that changes.
7. **Keep `noindex` on `coming-soon.html`, `404.html`, `journal.html`** and keep `sitemap.xml` and `robots.txt` consistent with the pages that exist.

## Work loop
- `git fetch origin && git worktree add ~/Movies/<name> -b dev/<task> origin/main`. The main checkout at `~/Movies/elvoro-golf` can be dirty (untracked `marketing/`, `tax-exempt/`); do not edit it.
- Small commits; check HTML parses and links resolve; look at the page at 390px and desktop.
- Say what you checked and what you did not.

## Commands that exist
| Task | Command |
|---|---|
| Local preview | `python3 -m http.server 8000` in the repo root |
| Pages status | `gh api repos/erlightbourn-source/elvoro-golf/pages` |
| Open a PR | `gh pr create` from a `dev/<task>` branch |
