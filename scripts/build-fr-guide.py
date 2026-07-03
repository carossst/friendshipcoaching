#!/usr/bin/env python3
"""Build a French guide page from a content dict.

Usage: import build_fr_guide; html = build_fr_guide.build(guide_dict)
Guide dict keys: slug, en_slug, title, description, og_description (optional),
h1, lead, pull_quote, intro, sections[], author_note, faq[], date ("2026-07-02").
Section keys: id, h2, paragraphs[] (HTML allowed), quote (opt), culture (opt: label, body).
FAQ keys: q, a (a: HTML allowed; JSON-LD gets tag-stripped version).
"""
import json, re

BASE = "https://thefriendshippractice.com"

def _strip(html):
    return re.sub(r"<[^>]+>", "", html)

def build(g):
    canonical = f"{BASE}/fr/guides/{g['slug']}/"
    en_url = f"{BASE}/guides/{g['en_slug']}/"
    og_desc = g.get("og_description", g["description"])
    date = g.get("date", "2026-07-02")

    faq_ld = [{
        "@type": "Question", "name": _strip(f["q"]),
        "acceptedAnswer": {"@type": "Answer", "text": _strip(f["a"])}
    } for f in g["faq"]]
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": g["h1"], "description": g["description"],
             "inLanguage": "fr",
             "author": {"@type": "Person", "name": "Carole Stromboni", "url": f"{BASE}/about.html"},
             "publisher": {"@type": "Organization", "name": "The Friendship Practice", "url": f"{BASE}/"},
             "dateModified": date, "datePublished": date, "mainEntityOfPage": canonical},
            {"@type": "FAQPage", "mainEntity": faq_ld},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "The Friendship Practice", "item": f"{BASE}/fr/"},
                {"@type": "ListItem", "position": 2, "name": g["h1"], "item": canonical}]}
        ]
    }

    sections_html = []
    for s in g["sections"]:
        parts = [f'    <section class="u-section u-section--sm">\n      <div class="u-container u-container--prose">']
        parts.append(f'        <h2 class="c-heading c-heading--2" id="{s["id"]}">{s["h2"]}</h2>')
        for p in s["paragraphs"]:
            parts.append(f'        <p class="c-body u-mt-6">{p}</p>')
        if s.get("quote"):
            parts.append(f'''        <blockquote class="c-quote u-mt-10">
          <p class="c-quote__text">{s["quote"]}</p>
        </blockquote>''')
        if s.get("culture"):
            parts.append(f'''        <aside class="c-culture-ref u-mt-8" aria-label="Exemple de la pop culture">
          <p class="c-culture-ref__label">{s["culture"]["label"]}</p>
          <p class="c-culture-ref__body">{s["culture"]["body"]}</p>
        </aside>''')
        parts.append("      </div>\n    </section>")
        sections_html.append("\n".join(parts))

    faq_html = "\n".join(f'''          <details class="c-faq__item">
            <summary class="c-faq__btn">{f["q"]} <span class="c-faq__icon">+</span></summary>
            <p class="c-faq__answer">{f["a"]}</p>
          </details>''' for f in g["faq"])

    return f'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index, follow">
  <title>{g["title"]}</title>
  <meta name="description" content="{g["description"]}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="{en_url}">
  <link rel="alternate" hreflang="fr" href="{canonical}">
  <link rel="alternate" hreflang="x-default" href="{en_url}">
  <meta name="theme-color" content="#faf7f2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#201711" media="(prefers-color-scheme: dark)">
  <meta name="author" content="Carole Stromboni">
  <link rel="stylesheet" href="/Fcoaching.css">
  <link rel="icon" href="/icons/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/icons/favicon.ico" sizes="32x32">
  <link rel="icon" href="/icons/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="/icons/favicon-16.png" sizes="16x16" type="image/png">
  <link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
  <meta property="og:title" content="{g["title"]}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{BASE}/icons/og-image.jpg">
  <meta property="og:image:alt" content="The Friendship Practice">
  <meta property="og:site_name" content="The Friendship Practice">
  <meta property="og:locale" content="fr_FR">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{g["title"]}">
  <meta name="twitter:description" content="{og_desc}">
  <meta name="twitter:image" content="{BASE}/icons/og-image.jpg">
  <script type="application/ld+json">
  {json.dumps(json_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
  <a class="u-sr-only" href="#main-content">Aller au contenu</a>
  <header class="c-nav">
    <nav class="c-nav__inner" aria-label="Navigation principale">
      <a class="c-nav__logo" href="/fr/" aria-label="The Friendship Practice, accueil">
        <img class="c-nav__logo-img" src="/icons/favicon.svg" alt="" width="36" height="36">
        <span class="c-nav__logo-text">The Friendship Practice</span>
      </a>
      <div class="c-nav__actions">
        <a class="c-nav__link" href="{en_url.replace(BASE, "")}" lang="en">English</a>
        <a class="c-btn c-btn--ghost c-btn--sm" href="/fr/defi.html">Le défi gratuit</a>
      </div>
    </nav>
  </header>

  <main id="main-content">
    <section class="c-hero">
      <div class="u-container u-container--prose">
        <p class="c-hero__label">Guide amitié</p>
        <h1 class="c-hero__title">{g["h1"]}</h1>
        <p class="c-hero__sub">{g["lead"]}</p>
        <p class="c-body u-mt-6"><strong>Mis à jour le 2 juillet 2026</strong></p>
        <div class="c-hero__actions u-mt-8">
          <a class="c-btn c-btn--primary c-btn--lg" href="/fr/defi.html">Commencer le défi gratuit</a>
          <a class="c-btn c-btn--ghost c-btn--lg" href="/fr/">Découvrir le coaching</a>
        </div>
      </div>
    </section>

    <section class="u-section u-section--sm">
      <div class="u-container u-container--prose">
        <blockquote class="c-quote">
          <p class="c-quote__text">{g["pull_quote"]}</p>
          <cite class="c-quote__cite">Carole Stromboni</cite>
        </blockquote>
      </div>
    </section>

    <section class="u-section u-section--sm">
      <div class="u-container u-container--prose">
        <p class="c-body">{g["intro"]}</p>
      </div>
    </section>

{chr(10).join(sections_html)}

    <section class="u-section u-section--sm u-bg-alt">
      <div class="u-container u-container--prose">
        <p class="c-label">Note de Carole</p>
        <p class="c-body u-mt-4">{g["author_note"]}</p>
      </div>
    </section>

    <section class="u-section">
      <div class="u-container">
        <p class="c-label">FAQ</p>
        <h2 class="c-heading c-heading--2 u-mb-10">Questions fréquentes</h2>
        <div class="c-faq">
{faq_html}
        </div>
      </div>
    </section>

    <section class="u-section u-bg-surface">
      <div class="u-container u-container--prose">
        <p class="c-label">Prochaine étape</p>
        <h2 class="c-heading c-heading--2">Voyez clair dans votre vie amicale. Puis changez-la.</h2>
        <p class="c-body u-mt-6">Le défi gratuit de 7 jours est une courte réflexion quotidienne : qui est dans vos cercles, ce qui vous pèse, et ce que vous voulez vraiment de l'amitié avant d'essayer de changer quoi que ce soit. Sept jours, un pas à la fois.</p>
        <div class="c-hero__actions u-mt-8">
          <a class="c-btn c-btn--primary c-btn--lg" href="/fr/defi.html">Commencer le défi gratuit</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="c-footer">
    <div class="c-footer__inner">
      <div>
        <p class="c-footer__copy">© 2026 Carole Stromboni · The Friendship Practice</p>
        <p class="c-footer__note u-mt-2">Du coaching, pas une thérapie ni un soutien de crise. <a href="{en_url.replace(BASE, "")}" lang="en">English version</a></p>
      </div>
      <nav class="c-footer__links" aria-label="Pages légales">
        <a href="/about.html" lang="en">About</a>
        <a href="/terms.html" lang="en">Terms</a>
        <a href="/privacy.html" lang="en">Privacy</a>
        <a href="/disclaimer.html" lang="en">Disclaimer</a>
      </nav>
    </div>
  </footer>
  <script data-goatcounter="https://friendc.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
'''

def write_guide(g):
    import os
    d = os.path.join("fr", "guides", g["slug"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(build(g))
    print(f"built fr/guides/{g['slug']}/")
