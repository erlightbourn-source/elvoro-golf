# Elvoro Golf — project notes

## Copy / voice rules (IMPORTANT)
Write plain, concrete, human copy. **Do not use AI-cliché "tell" words** — they read as machine-written and undercut the brand. Banned across all site copy, meta, and UI text:

> quiet, elevated/elevate, refined, restraint, curated, considered, timeless, effortless, understated, seamless, meticulous, crafted, thoughtfully, "more than just", "in today's fast-paced world", "look no further", "whether you're… or…"

Prefer specifics over abstract praise: "no loud logos," "tailored fit," "fabric that holds up," "let the play talk than the logo" — not "elevated, refined, quiet luxury." Before committing copy, grep the changed files for the banned list and confirm zero hits.

## Stack / deploy
- Static HTML/CSS/JS, no build. Single `assets/styles.css` (token-driven `:root`) + `assets/site.js`.
- Hosted on GitHub Pages from `main` root; deploy = commit + push, then the Pages build serves it (verify live with curl, allow CDN propagation).
- Live: https://erlightbourn-source.github.io/elvoro-golf/

## Current state (pre-launch)
- Two-shirt Drop One: Evergreen + Meridian, $60 each, shipping included.
- Waitlist only (no checkout). Email capture via FormSubmit alias → Gmail; size captured on PDP notify forms.
- GA4 wired in `site.js`, dormant until a real `GA_ID` is set.
- Open to the user: real launch date, launch discount %, founder identity + fabric specs, GA Measurement ID, domain purchase, $60-vs-positioning call.
