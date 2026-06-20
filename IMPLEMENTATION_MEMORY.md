# Implementation Memory

This file keeps the long-lived implementation memory for The Friendship Practice website.

Use it for:
- technical conventions that should survive across sessions
- SEO publication mechanics
- page status rules
- cross-file contracts
- architecture notes that are easy to forget

Do not use it for:
- a daily log
- temporary ideas
- copy experiments that are not shipped
- backlog grooming

## Document Map

- `README.md`
  - project overview
  - deployment notes
  - file map
- `SEO-PLAYBOOK.md`
  - SEO workflow
  - generation commands
  - indexing model
- `IMPLEMENTATION_MEMORY.md`
  - technical memory
  - architectural guardrails
  - non-obvious contracts
- `coding/CHANTIER_A_FAIRE.md`
  - current priorities
  - recommended next moves

## Project Shape

- Static HTML/CSS site with a very small Node-based SEO toolchain.
- No frontend framework.
- No build step for the main site shell.
- Generated files exist, but only for the SEO layer:
  - `guides/<slug>/index.html`
  - `sitemap.xml`
  - `robots.txt`
  - `llms.txt`

## Core Files

- `index.html`
  - main entry page
  - service positioning
  - FAQ
  - internal links to guides
- `challenge.html`
  - free 7-day challenge landing + tracker
  - now indexable
- `terms.html`, `privacy.html`, `disclaimer.html`, `refund-cancellation.html`
  - trust / legal pages
  - intentionally indexable
- `thank-you.html`, `intake.html`, `waitlist-confirmed.html`, `challenge-confirmed.html`, `404.html`
  - utility / transactional pages
  - intentionally non-indexable
- `Fcoaching.css`
  - single visual system for both core pages and generated guides
- `seo-pages.json`
  - single source of truth for page metadata and guide content
- `scripts/`
  - SEO generation and validation tooling

## SEO Tooling Contract

- `seo-pages.json` is the source of truth.
- Generated guides must never be edited by hand in `guides/`.
- If a guide needs copy or metadata changes:
  1. edit `seo-pages.json`
  2. run `npm run publish:seo`
- If a static hand-authored page changes title, description, or status:
  1. update the HTML file
  2. update `seo-pages.json`
  3. run `npm run publish:seo`

## Status Model

### Pages

- `live`
  - indexable
  - included in sitemap
- `ready`
  - deployed but `noindex, follow`
  - excluded from sitemap
- `private`
  - `noindex, follow`
  - excluded from sitemap
  - may also be disallowed in `robots.txt`

### Current Live Surface

As of `2026-06-20`, the public indexable surface is:
- home page
- challenge page
- legal pages
- 3 generated guide pages

## Current SEO Cluster

Current generated guides:
- `guides/how-to-make-friends-as-an-adult/`
- `guides/how-to-reconnect-with-old-friends/`
- `guides/why-making-friends-as-an-adult-is-hard/`

These guides are intentionally top-of-funnel:
- educational
- practical
- connected to the free challenge CTA
- linked from the home page

## Content Guardrails

- The site is coaching, not therapy.
- Do not blur the therapy boundary in SEO pages.
- Do not write crisis-oriented pages as if this service treats crisis.
- Keep the tone practical, calm, and specific.
- Avoid generic “self-help sludge” phrasing.
- Prefer concrete actions over abstract encouragement.

## Design Guardrails

- Reuse the existing CSS system in `Fcoaching.css`.
- Generated guides should feel native to the site, not like a separate blog theme.
- Do not add a JS-heavy content layer unless there is a strong reason.

## Publishing Commands

```bash
npm run generate:guides
npm run generate:sitemap
npm run generate:robots
npm run generate:llms
npm run test:seo
npm run publish:seo
```

## Known Gaps

- No git repository is initialized in this folder.
- No automated deployment hook is documented here yet.
- No analytics validation has been added for guide traffic or challenge conversion.
- No dedicated article template for author bio / published date blocks beyond the current generated layout.
- No content freshness workflow yet for revisiting guide pages after publication.

## Recommended Working Rule

For any future SEO work:
- start in `seo-pages.json`
- regenerate
- validate
- only then review output HTML
