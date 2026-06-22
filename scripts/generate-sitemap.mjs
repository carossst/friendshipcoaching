#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const outPath = path.join(ROOT, "sitemap.xml");

const BASE = String(seo.defaults.baseUrl).replace(/\/+$/, "");

const entries = (seo.pages || [])
  .filter((page) => page.status === "live")
  .map((page) => {
    const loc = `${BASE}${page.path}`;
    return [
      "  <url>",
      `    <loc>${loc}</loc>`,
      `    <lastmod>${page.lastmod}</lastmod>`,
      `    <changefreq>${page.changefreq}</changefreq>`,
      `    <priority>${page.priority}</priority>`,
      "  </url>"
    ].join("\n");
  });

const guideEntries = (seo.guides || [])
  .filter((guide) => guide.status === "live")
  .map((guide) => {
    const loc = `${BASE}/guides/${guide.slug}/`;
    return [
      "  <url>",
      `    <loc>${loc}</loc>`,
      `    <lastmod>${guide.lastmod}</lastmod>`,
      "    <changefreq>monthly</changefreq>",
      "    <priority>0.7</priority>",
      "  </url>"
    ].join("\n");
  });

const xml = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  "  <!-- GENERATED FILE - do not hand-edit. Run: npm run generate:sitemap -->",
  [...entries, ...guideEntries].join("\n"),
  "</urlset>",
  ""
].join("\n");

fs.writeFileSync(outPath, xml, "utf8");
console.log(`sitemap.xml written: ${entries.length + guideEntries.length} live URLs.`);
