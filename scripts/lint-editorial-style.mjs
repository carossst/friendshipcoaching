#!/usr/bin/env node
// Editorial style linter: reads every live local page/guide, extracts visible
// text (title, meta description, alt/aria-label, body text), and flags
// forbidden phrasing from editorial-style-rules.json.
//
// Runs against local files listed in seo-pages.json, not a live HTTP crawl:
// this repo IS the source of truth, so there is no need to fetch the site
// over the network to audit it.
//
// This is a reporter, not an auto-fixer. It never edits files.

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const rules = JSON.parse(fs.readFileSync(path.join(ROOT, "scripts", "editorial-style-rules.json"), "utf8"));

const SCIENCE_PAGES = new Set(["science-of-friendship.html", "fr/science-amitie.html"]);

function targets() {
  const files = [];
  for (const page of seo.pages || []) {
    if (page.status !== "live") continue;
    files.push(page.file);
  }
  for (const guide of seo.guides || []) {
    if (guide.status !== "live") continue;
    files.push(path.join("guides", guide.slug, "index.html"));
  }
  return files;
}

function decodeEntities(str) {
  return str
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#0?39;/g, "'")
    .replace(/&rsquo;/g, "’")
    .replace(/&mdash;/g, "—")
    .replace(/&ndash;/g, "–");
}

function stripTags(html) {
  return html.replace(/<[^>]+>/g, " ");
}

function extractSources(html) {
  const sources = [];

  const withoutScripts = html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<!--[\s\S]*?-->/g, " ");

  const titleMatch = html.match(/<title>([^<]*)<\/title>/i);
  if (titleMatch) sources.push({ source: "title", text: decodeEntities(titleMatch[1]) });

  const descMatch = html.match(/<meta\s+name="description"\s+content="([^"]*)"/i);
  if (descMatch) sources.push({ source: "meta description", text: decodeEntities(descMatch[1]) });

  for (const m of html.matchAll(/\balt="([^"]*)"/gi)) {
    if (m[1].trim()) sources.push({ source: "alt", text: decodeEntities(m[1]) });
  }
  for (const m of html.matchAll(/\baria-label="([^"]*)"/gi)) {
    if (m[1].trim()) sources.push({ source: "aria-label", text: decodeEntities(m[1]) });
  }

  const bodyMatch = withoutScripts.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  const bodyHtml = bodyMatch ? bodyMatch[1] : withoutScripts;
  const visibleText = decodeEntities(stripTags(bodyHtml)).replace(/\s+/g, " ").trim();
  sources.push({ source: "visible text", text: visibleText });

  return sources;
}

function fileLang(file) {
  const normalized = file.replace(/\\/g, "/");
  return normalized === "fr" || normalized.startsWith("fr/") ? "fr" : "en";
}

function applicableCategories(file) {
  const isScience = SCIENCE_PAGES.has(file.replace(/\\/g, "/"));
  return Object.entries(rules).filter(([key, def]) => {
    if (key.startsWith("_")) return false;
    if (isScience && def.scope === "guides") return false;
    return true;
  });
}

// anglicisms_fr's flat "phrases" list is FR-only by definition (loanwords
// that are wrong in French copy but perfectly normal English words on the
// English pages) - never check it against an English-language file.
function categoryPhrases(key, def, lang) {
  if (Array.isArray(def.phrases)) return key === "anglicisms_fr" && lang !== "fr" ? [] : def.phrases;
  return Array.isArray(def[lang]) ? def[lang] : [];
}

function escapeRegExp(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

const phraseRegexCache = new Map();
function phraseRegex(phrase) {
  if (phraseRegexCache.has(phrase)) return phraseRegexCache.get(phrase);
  // Word-boundary match. \b doesn't understand accented letters as word
  // chars in JS regex, so use lookaround on non-letter boundaries instead,
  // which works for both English and French text.
  const re = new RegExp(`(?<![\\p{L}])${escapeRegExp(phrase)}(?![\\p{L}])`, "iu");
  phraseRegexCache.set(phrase, re);
  return re;
}

function findIssues(file, sources) {
  const issues = [];
  const cats = applicableCategories(file);
  const lang = fileLang(file);

  for (const { source, text } of sources) {
    for (const [key, def] of cats) {
      for (const phrase of categoryPhrases(key, def, lang)) {
        if (phraseRegex(phrase).test(text)) {
          issues.push({ category: key, source, phrase, excerpt: excerptAround(text, phrase) });
        }
      }
    }
    if (source === "visible text" && text.includes("—")) {
      issues.push({ category: "em_dash", source, phrase: "—", excerpt: excerptAround(text, "—") });
    }
  }
  return issues;
}

function excerptAround(text, phrase) {
  const idx = text.toLowerCase().indexOf(phrase.toLowerCase());
  if (idx === -1) return text.slice(0, 80);
  const start = Math.max(0, idx - 40);
  const end = Math.min(text.length, idx + phrase.length + 40);
  return (start > 0 ? "…" : "") + text.slice(start, end) + (end < text.length ? "…" : "");
}

function main() {
  const files = targets();
  let totalIssues = 0;
  const seenExcerpts = new Set();

  for (const file of files) {
    const fullPath = path.join(ROOT, file);
    if (!fs.existsSync(fullPath)) {
      console.error(`Missing file listed in seo-pages.json: ${file}`);
      continue;
    }
    const html = fs.readFileSync(fullPath, "utf8");
    const sources = extractSources(html);
    const issues = findIssues(file, sources);

    for (const issue of issues) {
      const dedupeKey = `${file}|${issue.category}|${issue.phrase}|${issue.excerpt}`;
      if (seenExcerpts.has(dedupeKey)) continue;
      seenExcerpts.add(dedupeKey);
      totalIssues += 1;
      console.log(file);
      console.log(`  category: ${issue.category}  source: ${issue.source}`);
      console.log(`  phrase: "${issue.phrase}"`);
      console.log(`  excerpt: ${issue.excerpt}`);
      console.log("");
    }
  }

  console.log(`Checked ${files.length} live pages. ${totalIssues} issue(s) found.`);
  process.exit(totalIssues > 0 ? 1 : 0);
}

main();
