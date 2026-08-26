#!/usr/bin/env node
// Compares each page's FAQPage JSON-LD against its visible FAQ accordion.
// Catches: schema-only "ghost" FAQs with no visible counterpart, visible
// FAQ items missing from the schema, and question/answer text drift
// between the two (a common source of silently-invalid structured data,
// since nothing breaks visually when they fall out of sync).
//
// Reads local files via seo-pages.json, not a live HTTP crawl. Reporter
// only, never edits files.

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));

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

function normalize(str) {
  return decodeEntities(String(str || ""))
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    // Stripping an inline tag like <a>text</a>. leaves a space before the
    // punctuation that immediately followed it in the source; that space
    // never rendered, so drop it rather than flag it as a text mismatch.
    .replace(/\s+([.,!?;:])/g, "$1")
    .trim();
}

function extractJsonLdFaq(html) {
  const questions = [];
  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/gi)) {
    let data;
    try {
      data = JSON.parse(m[1]);
    } catch {
      questions.push({ error: "invalid-json" });
      continue;
    }
    const nodes = Array.isArray(data["@graph"]) ? data["@graph"] : [data];
    for (const node of nodes) {
      if (node["@type"] !== "FAQPage") continue;
      for (const entity of node.mainEntity || []) {
        questions.push({
          name: normalize(entity.name),
          answer: normalize(entity.acceptedAnswer && entity.acceptedAnswer.text)
        });
      }
    }
  }
  return questions;
}

function extractVisibleFaq(html) {
  const items = [];
  const detailsRe = /<details class="c-faq__item"[^>]*>([\s\S]*?)<\/details>/gi;
  for (const detailsMatch of html.matchAll(detailsRe)) {
    const block = detailsMatch[1];
    const summaryMatch = block.match(/<summary class="c-faq__btn">([\s\S]*?)<\/summary>/i);
    const answerMatch = block.match(/<p class="c-faq__answer">([\s\S]*?)<\/p>/i);
    if (!summaryMatch || !answerMatch) continue;
    const question = normalize(summaryMatch[1].replace(/<span class="c-faq__icon">[\s\S]*?<\/span>/i, ""));
    const answer = normalize(answerMatch[1]);
    items.push({ name: question, answer });
  }
  return items;
}

function compare(file, jsonLd, visible) {
  const issues = [];

  for (const q of jsonLd) {
    if (q.error) {
      issues.push({ file, kind: "invalid-json-ld", detail: "A JSON-LD block on this page is not valid JSON." });
      return issues;
    }
  }

  if (jsonLd.length === 0 && visible.length === 0) return issues;

  if (jsonLd.length !== visible.length) {
    issues.push({
      file,
      kind: "count-mismatch",
      detail: `FAQPage schema has ${jsonLd.length} question(s), visible accordion has ${visible.length}.`
    });
  }

  const visibleByName = new Map(visible.map((v) => [v.name, v]));
  const jsonByName = new Map(jsonLd.map((j) => [j.name, j]));

  for (const j of jsonLd) {
    if (!visibleByName.has(j.name)) {
      issues.push({ file, kind: "ghost-schema-faq", detail: `Question in JSON-LD but not visible: "${j.name}"` });
      continue;
    }
    const v = visibleByName.get(j.name);
    if (v.answer !== j.answer) {
      issues.push({
        file,
        kind: "answer-drift",
        detail: `Answer text differs for "${j.name}".\n    schema : ${j.answer}\n    visible: ${v.answer}`
      });
    }
  }

  for (const v of visible) {
    if (!jsonByName.has(v.name)) {
      issues.push({ file, kind: "missing-from-schema", detail: `Visible FAQ not in JSON-LD: "${v.name}"` });
    }
  }

  return issues;
}

function main() {
  const files = targets();
  let total = 0;

  for (const file of files) {
    const fullPath = path.join(ROOT, file);
    if (!fs.existsSync(fullPath)) {
      console.error(`Missing file listed in seo-pages.json: ${file}`);
      continue;
    }
    const html = fs.readFileSync(fullPath, "utf8");
    const jsonLd = extractJsonLdFaq(html);
    const visible = extractVisibleFaq(html);
    const issues = compare(file, jsonLd, visible);

    for (const issue of issues) {
      total += 1;
      console.log(issue.file);
      console.log(`  ${issue.kind}: ${issue.detail}`);
      console.log("");
    }
  }

  console.log(`Checked ${files.length} live pages. ${total} issue(s) found.`);
  process.exit(total > 0 ? 1 : 0);
}

main();
