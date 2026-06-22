# SEO Playbook

This site uses a lighter version of the SEO workflow from the pickleball quiz project.

## Source Of Truth

- `seo-pages.json`
  - page-level metadata
  - indexability status
  - sitemap settings
- `scripts/generate-guides.mjs`
  - writes guide pages in `guides/<slug>/index.html`
- `scripts/generate-sitemap.mjs`
  - writes `sitemap.xml`
- `scripts/generate-robots.mjs`
  - writes `robots.txt`
- `scripts/generate-llms-txt.mjs`
  - writes `llms.txt`
- `scripts/validate-seo.mjs`
  - checks HTML heads against `seo-pages.json`

## Status Model

- `live`
  - indexable
  - included in sitemap
- `ready`
  - deployed page that stays `noindex,follow`
  - excluded from sitemap
- `private`
  - transactional or utility page
  - `noindex,follow`
  - excluded from sitemap

## Current Intent

- `index.html` is the main search entry point.
- `guides/` contains generated editorial SEO pages.
- Legal pages stay indexable for trust and policy coverage.
- `challenge.html` is now indexable and included in the sitemap.
- Confirmation, intake, thank-you, and `404.html` stay out of search.

## Commands

```bash
npm run generate:guides
npm run generate:sitemap
npm run generate:robots
npm run generate:llms
npm run test:seo
npm run publish:seo
```
