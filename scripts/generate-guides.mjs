#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const BASE = String(seo.defaults.baseUrl).replace(/\/+$/, "");
const ogImage = `${BASE}${seo.defaults.ogImage}`;

function esc(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function toId(text) {
  return text
    .toLowerCase()
    .replace(/['']/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function formatDate(dateText) {
  const date = new Date(`${dateText}T00:00:00Z`);
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC"
  }).format(date);
}

function renderGuide(guide, allGuides) {
  const canonical = `${BASE}/guides/${guide.slug}/`;
  const related = allGuides.filter((item) => item.slug !== guide.slug && item.status === "live").slice(0, 3);
  const faqGraph = (guide.faq || []).map((item) => ({
    "@type": "Question",
    name: item.q,
    acceptedAnswer: {
      "@type": "Answer",
      text: item.a
    }
  }));
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Article",
        headline: guide.h1,
        description: guide.description,
        author: {
          "@type": "Person",
          name: "Carole Stromboni",
          url: `${BASE}/about.html`
        },
        publisher: {
          "@type": "Organization",
          name: "The Friendship Practice",
          url: `${BASE}/`
        },
        dateModified: guide.lastmod,
        datePublished: guide.lastmod,
        mainEntityOfPage: canonical,
        image: ogImage,
        speakable: {
          "@type": "SpeakableSpecification",
          cssSelector: [".c-hero__title", ".c-hero__sub"]
        }
      },
      {
        "@type": "FAQPage",
        mainEntity: faqGraph
      },
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "The Friendship Practice",
            "item": `${BASE}/`
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": guide.h1,
            "item": canonical
          }
        ]
      }
    ]
  };

  const inlineCta = `
      <section class="u-section u-section--sm">
        <div class="u-container u-container--prose">
          <aside class="c-inline-cta">
            <p class="c-inline-cta__text">Reading is a good start. Doing is better. The free 7-day Friendship Challenge turns all of this into one small step a day.</p>
            <a class="c-btn c-btn--primary" href="/challenge.html">Start the free 7-day challenge</a>
          </aside>
        </div>
      </section>`;
  const ctaAt = Math.floor(((guide.sections || []).length - 1) / 2);
  const sectionsHtml = (guide.sections || [])
    .map(
      (section, i) => `
      <section class="u-section u-section--sm">
        <div class="u-container u-container--prose">
          <h2 class="c-heading c-heading--2" id="${toId(section.h2)}">${esc(section.h2)}</h2>
${section.paragraphs
  .map((paragraph) => `          <p class="c-body u-mt-6">${paragraph}</p>`)
  .join("\n")}
${section.cultureRef ? `          <aside class="c-culture-ref u-mt-8" aria-label="Pop culture example">
            <p class="c-culture-ref__label">${esc(section.cultureRef.show)}</p>
            <p class="c-culture-ref__body">${section.cultureRef.body}</p>
          </aside>` : ""}
${section.quote ? `          <blockquote class="c-quote u-mt-10">
            <p class="c-quote__text">${esc(section.quote)}</p>
            ${section.quoteAuthor ? `<cite class="c-quote__cite">${esc(section.quoteAuthor)}</cite>` : ""}
          </blockquote>
          ${section.quoteAuthor ? `<p class="c-share-quote u-mt-4"><a class="c-share-quote__link" href="https://twitter.com/intent/tweet?text=${encodeURIComponent('"' + section.quote + '" — ' + section.quoteAuthor + ', thefriendshippractice.com')}" rel="noopener noreferrer" target="_blank">Share on X →</a></p>` : ""}` : ""}
${section.connection ? `          <div class="c-connection u-mt-6">
            <p class="c-connection__label">In conversation with</p>
            <p class="c-connection__text">"${esc(section.connection.quote)}"</p>
            <p class="c-connection__cite">${esc(section.connection.author)}, ${esc(section.connection.role)}</p>
            <p class="c-connection__why">${esc(section.connection.why)}</p>
          </div>` : ""}
        </div>
      </section>${(guide.sections || []).length >= 4 && i === ctaAt ? "\n" + inlineCta : ""}`
    )
    .join("\n");

  const tocHtml = (guide.sections || []).length > 2
    ? `
    <section class="u-section u-section--sm">
      <div class="u-container u-container--prose">
        <nav class="c-toc" aria-label="Table of contents">
          <p class="c-toc__label">In this guide</p>
          <ol class="c-toc__list">
${(guide.sections || []).map((s) => `            <li class="c-toc__item"><a class="c-toc__link" href="#${toId(s.h2)}">${esc(s.h2)}</a></li>`).join("\n")}
          </ol>
        </nav>
      </div>
    </section>`
    : "";

  const faqHtml = (guide.faq || [])
    .map(
      (item) => `
        <details class="c-faq__item">
          <summary class="c-faq__btn">${esc(item.q)} <span class="c-faq__icon">+</span></summary>
          <p class="c-faq__answer">${esc(item.a)}</p>
        </details>`
    )
    .join("\n");

  const relatedHtml = related
    .map(
      (item) => `
        <a class="c-feature" href="/guides/${item.slug}/">
          <h3 class="c-feature__title">${esc(item.h1)}</h3>
          <p class="c-feature__text">${esc(item.description)}</p>
        </a>`
    )
    .join("\n");

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="${guide.status === "live" ? "index, follow" : "noindex, follow"}">
  <title>${esc(guide.title)}</title>
  <meta name="description" content="${esc(guide.description)}">
  <link rel="canonical" href="${canonical}">
${guide.alternateFr ? `  <link rel="alternate" hreflang="en" href="${canonical}">
  <link rel="alternate" hreflang="fr" href="${BASE}${guide.alternateFr}">
  <link rel="alternate" hreflang="x-default" href="${canonical}">` : ""}
  <meta name="theme-color" content="#faf7f2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#201711" media="(prefers-color-scheme: dark)">
  <meta name="author" content="Carole Stromboni">
  <link rel="stylesheet" href="/Fcoaching.css">
  <link rel="icon" href="/icons/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/icons/favicon.ico" sizes="32x32">
  <link rel="icon" href="/icons/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="/icons/favicon-16.png" sizes="16x16" type="image/png">
  <link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
  <meta property="og:title" content="${esc(guide.title)}">
  <meta property="og:description" content="${esc(guide.description)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="${canonical}">
  <meta property="og:image" content="${ogImage}">
  <meta property="og:image:alt" content="The Friendship Practice">
  <meta property="og:site_name" content="The Friendship Practice">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(guide.title)}">
  <meta name="twitter:description" content="${esc(guide.description)}">
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
    <nav class="c-breadcrumb" aria-label="Breadcrumb">
      <div class="u-container u-container--prose">
        <ol class="c-breadcrumb__list">
          <li class="c-breadcrumb__item"><a href="/">Home</a></li>
          <li class="c-breadcrumb__item"><a href="/guides/">Guides</a></li>
          <li class="c-breadcrumb__item" aria-current="page">${esc(guide.h1)}</li>
        </ol>
      </div>
    </nav>
    <section class="c-hero">
      <div class="u-container u-container--prose">
        <p class="c-hero__label">Friendship guide</p>
        <h1 class="c-hero__title">${esc(guide.h1)}</h1>
        <p class="c-hero__sub">${esc(guide.lead)}</p>
        <p class="c-body u-mt-6"><strong>Updated ${esc(formatDate(guide.lastmod))}</strong></p>
        <div class="c-hero__actions u-mt-8">
          <a class="c-btn c-btn--primary c-btn--lg" href="/challenge.html">Start the free 7-day challenge</a>
          <a class="c-btn c-btn--ghost c-btn--lg" href="/index.html">See the coaching practice</a>
        </div>
      </div>
    </section>

${guide.pullQuote ? `    <section class="u-section u-section--sm">
      <div class="u-container u-container--prose">
        <div class="c-author-quote">
          <img class="c-author-quote__photo" src="/Carolephotobio.jpg" alt="Carole Stromboni" width="112" height="112">
          <div class="c-author-quote__body">
            <p class="c-author-quote__text">"${esc(guide.pullQuote)}"</p>
            <cite class="c-author-quote__cite">Carole Stromboni</cite>
          </div>
        </div>
      </div>
    </section>` : ""}

    <section class="u-section">
      <div class="u-container u-container--prose">
        ${guide.intro.split(/\n\n+/).map((p, i) => `<p class="c-body${i > 0 ? " u-mt-6" : ""}">${p}</p>`).join("\n        ")}
${guide.authorNote ? `        <p class="c-body u-mt-6 c-body--author-note">${esc(guide.authorNote)}</p>` : ""}
      </div>
    </section>

${tocHtml}

${sectionsHtml}

    <section class="u-section u-bg-surface">
      <div class="u-container u-container--prose">
        <p class="c-label">About the author</p>
        <p class="c-body"><strong>Carole Stromboni</strong> is the founder of The Friendship Practice. She is the author of <em>Innover en pratique</em> (Eyrolles) and splits her time between Hawaii and Paris. Her work focuses on helping adults turn good intentions into concrete friendship practice. <a href="/index.html">Learn more about The Friendship Practice.</a></p>
      </div>
    </section>

    <section class="u-section u-bg-alt">
      <div class="u-container u-container--prose">
        <p class="c-label">Common questions</p>
        <h2 class="c-heading c-heading--2 u-mb-10">Quick answers</h2>
        <div class="c-faq">
${faqHtml}
        </div>
      </div>
    </section>

    <section class="u-section">
      <div class="u-container">
        <p class="c-label">Read next</p>
        <h2 class="c-heading c-heading--2 u-mb-10">More friendship guides</h2>
        <div class="c-features">
${relatedHtml}
        </div>
      </div>
    </section>

    <section class="u-section u-bg-surface">
      <div class="u-container u-container--prose">
        <p class="c-label">Next step</p>
        <h2 class="c-heading c-heading--2">See your friendship life clearly. Then change it.</h2>
        <p class="c-body u-mt-6">The free 7-day Friendship Challenge is a short daily reflection: who is in your circle, what feels off, and what you actually want from friendship before you try to change anything. Seven days, one step at a time.</p>
        <div class="c-hero__actions u-mt-8">
          <a class="c-btn c-btn--primary c-btn--lg" href="/challenge.html">Start the free 7-day challenge</a>
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
}

for (const guide of seo.guides || []) {
  if (guide.status !== "live" && guide.status !== "ready") continue;
  const dirPath = path.join(ROOT, "guides", guide.slug);
  fs.mkdirSync(dirPath, { recursive: true });
  const outPath = path.join(dirPath, "index.html");
  fs.writeFileSync(outPath, renderGuide(guide, seo.guides || []), "utf8");
}

console.log(`guides written: ${(seo.guides || []).filter((guide) => guide.status === "live" || guide.status === "ready").length}.`);
