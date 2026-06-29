#!/usr/bin/env node
// Run after publishing: node scripts/submit-indexnow.mjs
// Notifies Bing/Yandex/Seznam of updated URLs via IndexNow.

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const BASE = String(seo.defaults.baseUrl).replace(/\/+$/, "");
const KEY = "f3e7588c6e7bdc1e6df1a7a210d9fe05";
const HOST = new URL(BASE).hostname;

const livePageUrls = (seo.pages || [])
  .filter((p) => p.status === "live")
  .map((p) => `${BASE}${p.path}`);

const liveGuideUrls = (seo.guides || [])
  .filter((g) => g.status === "live")
  .map((g) => `${BASE}/guides/${g.slug}/`);

const urlList = [...livePageUrls, ...liveGuideUrls];

const body = JSON.stringify({
  host: HOST,
  key: KEY,
  keyLocation: `${BASE}/${KEY}.txt`,
  urlList
});

const res = await fetch("https://api.indexnow.org/indexnow", {
  method: "POST",
  headers: { "Content-Type": "application/json; charset=utf-8" },
  body
});

if (res.ok || res.status === 202) {
  console.log(`IndexNow: submitted ${urlList.length} URLs. Status: ${res.status}`);
} else {
  const text = await res.text();
  console.error(`IndexNow error ${res.status}:`, text);
  process.exit(1);
}
