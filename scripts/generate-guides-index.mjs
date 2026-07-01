#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const BASE = String(seo.defaults.baseUrl).replace(/\/+$/, "");
const ogImage = `${BASE}${seo.defaults.ogImage}`;
const canonical = `${BASE}/guides/`;

function esc(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

const liveGuides = (seo.guides || []).filter((g) => g.status === "live");
const guidesBySlug = Object.fromEntries(liveGuides.map((g) => [g.slug, g]));

const pageMeta = (seo.pages || []).find((p) => p.path === "/guides/") || {};
const pageTitle = pageMeta.title || "Friendship Guides | The Friendship Practice";
const pageDescription = pageMeta.description || "Practical guides on friendship, by Carole Stromboni.";

const categories = [
  {
    label: "Are you an expat?",
    headline: "Making friends in a country that isn't yours yet.",
    slugs: [
      "how-to-make-friends-as-an-expat",
      "how-to-meet-people-in-a-new-city",
      "how-to-reconnect-with-old-friends"
    ]
  },
  {
    label: "Working from home?",
    headline: "Remote work removed the social structure. Here's how to replace it.",
    slugs: [
      "how-to-make-friends-when-you-work-from-home",
      "how-to-keep-work-friendships-after-going-remote",
      "how-to-follow-up-after-meeting-someone"
    ]
  },
  {
    label: "Are you a new parent?",
    headline: "Friendship changes after a baby. Here's how to navigate it.",
    slugs: [
      "how-to-make-friends-as-a-new-parent",
      "how-to-stay-friends-after-a-baby",
      "how-to-keep-friends-as-an-adult"
    ]
  },
  {
    label: "Just turned 30?",
    headline: "The social structures of your 20s are gone. These ones actually work.",
    slugs: [
      "how-to-make-friends-after-30",
      "how-to-make-friends-as-an-adult",
      "why-making-friends-as-an-adult-is-hard"
    ]
  },
  {
    label: "New to a city?",
    headline: "Starting a social life in a place where you know almost no one.",
    slugs: [
      "how-to-meet-people-in-a-new-city",
      "how-to-turn-acquaintances-into-friends",
      "how-to-make-friends-as-an-adult"
    ]
  },
  {
    label: "Building connection",
    slugs: [
      "how-to-follow-up-after-meeting-someone",
      "how-to-turn-acquaintances-into-friends",
      "how-to-know-if-someone-wants-to-be-your-friend",
      "how-to-be-a-better-friend",
      "how-men-can-rebuild-friendships",
      "how-to-introduce-friends-to-each-other"
    ]
  },
  {
    label: "Keeping friendships alive",
    slugs: [
      "how-to-keep-friends-as-an-adult",
      "why-do-friendships-fade",
      "how-to-reconnect-with-old-friends",
      "one-sided-friendship",
      "when-a-friendship-ends",
      "how-to-make-friends-after-a-friendship-ends"
    ]
  },
  {
    label: "Understanding friendship",
    slugs: [
      "why-making-friends-as-an-adult-is-hard",
      "why-male-friendships-fade",
      "what-is-friendship-coaching",
      "friendship-quotes"
    ]
  }
];

function renderCategory(cat) {
  const guides = cat.slugs.map((slug) => guidesBySlug[slug]).filter(Boolean);
  const cards = guides
    .map(
      (guide) => `
        <a class="c-feature" href="/guides/${guide.slug}/">
          <h3 class="c-feature__title">${esc(guide.h1)}</h3>
          <p class="c-feature__text">${esc(guide.description)}</p>
        </a>`
    )
    .join("\n");

  return `
    <section class="u-section">
      <div class="u-container">
        <p class="c-label">${esc(cat.label)}</p>
        ${cat.headline ? `<h2 class="c-heading c-heading--2 u-mb-10">${esc(cat.headline)}</h2>` : ""}
        <div class="c-features${cat.headline ? "" : " u-mt-8"}">
${cards}
        </div>
      </div>
    </section>`;
}

const categoriesHtml = categories.map(renderCategory).join("\n");

const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "name": "Friendship Guides",
      "description": "Practical guides on making friends as an adult, keeping friendships alive, reconnecting with old friends, and more. By Carole Stromboni at The Friendship Practice.",
      "url": canonical,
      "author": {
        "@type": "Person",
        "name": "Carole Stromboni",
        "url": `${BASE}/about.html`
      },
      "publisher": {
        "@type": "Organization",
        "name": "The Friendship Practice",
        "url": `${BASE}/`
      }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "The Friendship Practice",
          "item": `${BASE}/`
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Friendship Guides",
          "item": canonical
        }
      ]
    }
  ]
};

const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index, follow">
  <title>${esc(pageTitle)}</title>
  <meta name="description" content="${esc(pageDescription)}">
  <link rel="canonical" href="${canonical}">
  <meta name="theme-color" content="#faf7f2">
  <meta name="author" content="Carole Stromboni">
  <link rel="stylesheet" href="/Fcoaching.css">
  <link rel="icon" href="/icons/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/icons/favicon.ico" sizes="32x32">
  <link rel="icon" href="/icons/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="/icons/favicon-16.png" sizes="16x16" type="image/png">
  <link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
  <meta property="og:title" content="${esc(pageTitle)}">
  <meta property="og:description" content="${esc(pageMeta.ogDescription || pageDescription)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="${canonical}">
  <meta property="og:image" content="${ogImage}">
  <meta property="og:image:alt" content="The Friendship Practice">
  <meta property="og:site_name" content="The Friendship Practice">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(pageTitle)}">
  <meta name="twitter:description" content="${esc(pageDescription)}">
  <meta name="twitter:image" content="${ogImage}">
  <script type="application/ld+json">
  ${JSON.stringify(jsonLd, null, 2)}
  </script>
</head>
<body>
  <a class="u-sr-only" href="#main-content">Skip to content</a>
  <header class="c-nav">
    <nav class="c-nav__inner" aria-label="Primary navigation">
      <a class="c-nav__logo" href="/index.html" aria-label="The Friendship Practice home">
        <img class="c-nav__logo-img" src="/icons/favicon.svg" alt="" width="36" height="36">
        <span class="c-nav__logo-text">The Friendship Practice</span>
      </a>
      <div class="c-nav__actions">
        <a class="c-nav__link" href="/about.html">About</a>
        <a class="c-btn c-btn--ghost c-btn--sm" href="/challenge.html">Start the free challenge</a>
      </div>
    </nav>
  </header>

  <main id="main-content">
    <section class="c-hero">
      <div class="u-container u-container--prose">
        <p class="c-hero__label">The Friendship Practice</p>
        <h1 class="c-hero__title">Friendship guides</h1>
        <p class="c-hero__sub">Practical guides for the five situations that make adult friendship genuinely hard: expat life, remote work, new parenthood, life after 30, and starting over in a new city. Written by Carole Stromboni.</p>
      </div>
    </section>

${categoriesHtml}

    <section class="u-section u-bg-surface">
      <div class="u-container u-container--prose">
        <p class="c-label">Next step</p>
        <h2 class="c-heading c-heading--2">Practice friendship on better foundations.</h2>
        <p class="c-body u-mt-6">If you want more than general advice, start with the free 7-day Friendship Challenge. It helps you look clearly at your friendship life before trying to fix it.</p>
        <div class="c-hero__actions u-mt-8">
          <a class="c-btn c-btn--primary c-btn--lg" href="/challenge.html">Start the challenge</a>
          <a class="c-btn c-btn--ghost c-btn--lg" href="/about.html">About Carole Stromboni</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="c-footer">
    <div class="c-footer__inner">
      <div>
        <p class="c-footer__copy">© 2026 Carole Stromboni · The Friendship Practice</p>
        <p class="c-footer__note u-mt-2">Friendship coaching, not therapy or crisis support.</p>
      </div>
      <nav class="c-footer__links" aria-label="Legal">
        <a href="/about.html">About</a>
        <a href="/terms.html">Terms</a>
        <a href="/privacy.html">Privacy</a>
        <a href="/disclaimer.html">Disclaimer</a>
        <a href="/refund-cancellation.html">Refund and cancellation</a>
      </nav>
    </div>
  </footer>
  <script data-goatcounter="https://friendc.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
`;

fs.mkdirSync(path.join(ROOT, "guides"), { recursive: true });
fs.writeFileSync(path.join(ROOT, "guides", "index.html"), html, "utf8");
console.log(`guides/index.html written: ${liveGuides.length} guides listed.`);
