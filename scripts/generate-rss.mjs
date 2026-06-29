#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const BASE = String(seo.defaults.baseUrl).replace(/\/+$/, "");

function esc(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

const liveGuides = (seo.guides || [])
  .filter((g) => g.status === "live")
  .sort((a, b) => new Date(b.lastmod) - new Date(a.lastmod));

const items = liveGuides.map((g) => `
    <item>
      <title>${esc(g.h1)}</title>
      <link>${BASE}/guides/${g.slug}/</link>
      <guid isPermaLink="true">${BASE}/guides/${g.slug}/</guid>
      <description>${esc(g.description)}</description>
      <pubDate>${new Date(g.lastmod + "T00:00:00Z").toUTCString()}</pubDate>
    </item>`).join("\n");

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>The Friendship Practice — Guides</title>
    <link>${BASE}/guides/</link>
    <description>Practical guides on friendship by Carole Stromboni.</description>
    <language>en-us</language>
    <copyright>© 2026 Carole Stromboni</copyright>
    <atom:link href="${BASE}/feed.xml" rel="self" type="application/rss+xml"/>
${items}
  </channel>
</rss>
`;

fs.writeFileSync(path.join(ROOT, "feed.xml"), xml, "utf8");
console.log(`feed.xml written: ${liveGuides.length} guides.`);
