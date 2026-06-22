#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const outPath = path.join(ROOT, "llms.txt");
const BASE = String(seo.defaults.baseUrl).replace(/\/+$/, "");

const livePages = (seo.pages || []).filter((page) => page.status === "live");
const liveGuides = (seo.guides || []).filter((guide) => guide.status === "live");

const lines = [
  `# ${seo.defaults.siteName}`,
  "",
  `> ${seo.llms.summary}`,
  "",
  "## Offer",
  seo.llms.offer,
  "",
  "## Audience",
  seo.llms.audience,
  "",
  "## Contact",
  seo.llms.contactEmail,
  "",
  "## Public Pages",
  ...livePages.map((page) => `- ${BASE}${page.path} — ${page.description}`),
  ...liveGuides.map((guide) => `- ${BASE}/guides/${guide.slug}/ — ${guide.description}`),
  "",
  "## Notes",
  "- The coaching offer is practical support, not therapy or crisis care.",
  "- Transactional pages such as confirmation and intake pages are intentionally excluded from search indexing.",
  ""
];

fs.writeFileSync(outPath, lines.join("\n"), "utf8");
console.log(`llms.txt written: ${livePages.length + liveGuides.length} public pages listed.`);
