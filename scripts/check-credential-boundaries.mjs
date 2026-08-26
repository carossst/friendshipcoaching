#!/usr/bin/env node
// Sweeps every live page for two specific compliance risks:
//
// 1. Carole described with a credential she doesn't claim (researcher,
//    scientist, psychologist, therapist, clinician, academic expert).
//    Proximity-based: flags a credential word only when it appears near
//    an actual mention of Carole, so citing a real cited researcher
//    ("Jeffrey Hall, a researcher at...") never trips it.
//
// 2. The service itself described as therapy / a clinic / mental health
//    care, as an exact phrase (safe to match literally, unlike single
//    words like "therapist" which also appear correctly in disclaimers
//    such as "not a substitute for a licensed therapist").
//
// Reads local files via seo-pages.json, not a live HTTP crawl - this repo
// is the source of truth. Reporter only, never edits files.

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));

const CREDENTIAL_WORDS = [
  "researcher", "chercheuse", "chercheur",
  "scientist", "scientifique",
  "psychologist", "psychologue",
  "therapist", "thérapeute",
  "clinician", "clinicienne", "clinicien",
  "academic expert", "experte académique", "expert académique"
];

const FORBIDDEN_SERVICE_PHRASES = [
  "friendship therapy", "relationship therapy", "social skills clinic",
  "psychological practice", "mental health service", "mental health clinic",
  "thérapie de l’amitié", "thérapie de l'amitié", "thérapie relationnelle",
  "clinique de compétences sociales", "cabinet de psychologie",
  "service de santé mentale", "clinique de santé mentale"
];

const NAME_PATTERN = /\bcarole\b/gi;
// Split into sentences rather than a fixed character window: a fixed
// window crosses sentence boundaries and flags unrelated neighboring
// sentences (e.g. "...therapist-client privilege... Carole can decline...").
const SENTENCE_SPLIT = /(?<=[.!?])\s+(?=[A-ZÀ-Ý])/g;

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
    .replace(/&rsquo;/g, "’");
}

// Block-level closing tags mark the end of a discrete unit of meaning
// (a citation, a heading, a list item...). Without a forced boundary here,
// e.g. <cite>Carole Stromboni</cite> glues onto whatever text follows in
// the DOM with no punctuation between them, which can fabricate a "sentence"
// that never existed in the copy and confuses proximity checks downstream.
const BLOCK_BOUNDARY_TAGS = ["cite", "p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote", "summary", "div", "section"];

function visibleText(html) {
  const withoutScripts = html
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<!--[\s\S]*?-->/g, " ");
  const bodyMatch = withoutScripts.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  let bodyHtml = bodyMatch ? bodyMatch[1] : withoutScripts;
  for (const tag of BLOCK_BOUNDARY_TAGS) {
    bodyHtml = bodyHtml.replace(new RegExp(`</${tag}>`, "gi"), `</${tag}>. `);
  }
  return decodeEntities(bodyHtml.replace(/<[^>]+>/g, " ")).replace(/\s+/g, " ").trim();
}

function escapeRegExp(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function wordRegex(word) {
  return new RegExp(`(?<![\\p{L}])${escapeRegExp(word)}(?![\\p{L}])`, "iu");
}

function checkCredentialProximity(file, text) {
  const issues = [];
  const sentences = text.split(SENTENCE_SPLIT);
  for (const sentence of sentences) {
    if (!NAME_PATTERN.test(sentence)) continue;
    NAME_PATTERN.lastIndex = 0;
    for (const word of CREDENTIAL_WORDS) {
      if (wordRegex(word).test(sentence)) {
        issues.push({ file, check: "credential-near-carole", word, excerpt: sentence.trim() });
      }
    }
  }
  return issues;
}

function checkServicePhrases(file, text) {
  const issues = [];
  const lower = text.toLowerCase();
  for (const phrase of FORBIDDEN_SERVICE_PHRASES) {
    const idx = lower.indexOf(phrase.toLowerCase());
    if (idx !== -1) {
      const start = Math.max(0, idx - 40);
      const end = Math.min(text.length, idx + phrase.length + 40);
      issues.push({
        file,
        check: "forbidden-service-phrase",
        word: phrase,
        excerpt: (start > 0 ? "…" : "") + text.slice(start, end) + (end < text.length ? "…" : "")
      });
    }
  }
  return issues;
}

function main() {
  const files = targets();
  let total = 0;
  const seen = new Set();

  for (const file of files) {
    const fullPath = path.join(ROOT, file);
    if (!fs.existsSync(fullPath)) {
      console.error(`Missing file listed in seo-pages.json: ${file}`);
      continue;
    }
    const html = fs.readFileSync(fullPath, "utf8");
    const text = visibleText(html);
    const issues = [...checkCredentialProximity(file, text), ...checkServicePhrases(file, text)];

    for (const issue of issues) {
      const key = `${issue.file}|${issue.check}|${issue.word}|${issue.excerpt}`;
      if (seen.has(key)) continue;
      seen.add(key);
      total += 1;
      console.log(issue.file);
      console.log(`  check: ${issue.check}  flagged: "${issue.word}"`);
      console.log(`  excerpt: ${issue.excerpt}`);
      console.log("");
    }
  }

  console.log(`Checked ${files.length} live pages. ${total} issue(s) found.`);
  process.exit(total > 0 ? 1 : 0);
}

main();
