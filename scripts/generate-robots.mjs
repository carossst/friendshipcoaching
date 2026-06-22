#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const outPath = path.join(ROOT, "robots.txt");
const BASE = String(seo.defaults.baseUrl).replace(/\/+$/, "");

const privatePaths = (seo.pages || [])
  .filter((page) => page.status === "private")
  .map((page) => `Disallow: ${page.path}`);

const lines = [
  "# robots.txt - thefriendshippractice.com",
  "# Public pages may be crawled. Transactional pages stay out of search.",
  "",
  "User-agent: *",
  "Allow: /",
  ...privatePaths,
  "",
  "User-agent: OAI-SearchBot",
  "Allow: /",
  "",
  "User-agent: ChatGPT-User",
  "Allow: /",
  "",
  "User-agent: PerplexityBot",
  "Allow: /",
  "",
  "User-agent: Claude-User",
  "Allow: /",
  "",
  "User-agent: Claude-SearchBot",
  "Allow: /",
  "",
  "User-agent: GPTBot",
  "Allow: /",
  "",
  "User-agent: ClaudeBot",
  "Allow: /",
  "",
  "User-agent: Google-Extended",
  "Allow: /",
  "",
  `Sitemap: ${BASE}/sitemap.xml`,
  ""
];

fs.writeFileSync(outPath, lines.join("\n"), "utf8");
console.log(`robots.txt written: ${privatePaths.length} transactional paths disallowed.`);
