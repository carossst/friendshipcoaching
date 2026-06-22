#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const BASE = String(seo.defaults.baseUrl).replace(/\/+$/, "");
const OG_IMAGE = `${BASE}${seo.defaults.ogImage}`;

function read(file) {
  return fs.readFileSync(path.join(ROOT, file), "utf8");
}

function expectMatch(html, regex, expected, label, errors) {
  const match = html.match(regex);
  const actual = match ? match[1].trim() : null;
  if (actual !== expected) {
    errors.push(`${label}: expected "${expected}" but found "${actual ?? "missing"}"`);
  }
}

const errors = [];

for (const page of seo.pages || []) {
  const html = read(page.file);
  const expectedRobots = page.status === "live" ? "index, follow" : "noindex, follow";
  const expectedCanonical = `${BASE}${page.path}`;

  expectMatch(html, /<title>([^<]+)<\/title>/i, page.title, `${page.file} title`, errors);
  expectMatch(
    html,
    /<meta\s+name="description"\s+content="([^"]+)"/i,
    page.description,
    `${page.file} meta description`,
    errors
  );
  if (page.file !== "404.html") {
    expectMatch(
      html,
      /<link\s+rel="canonical"\s+href="([^"]+)"/i,
      expectedCanonical,
      `${page.file} canonical`,
      errors
    );
  }
  expectMatch(
    html,
    /<meta\s+name="robots"\s+content="([^"]+)"/i,
    expectedRobots,
    `${page.file} robots`,
    errors
  );
  if (page.file !== "404.html") {
    expectMatch(
      html,
      /<meta\s+property="og:url"\s+content="([^"]+)"/i,
      expectedCanonical,
      `${page.file} og:url`,
      errors
    );
    expectMatch(
      html,
      /<meta\s+property="og:image"\s+content="([^"]+)"/i,
      OG_IMAGE,
      `${page.file} og:image`,
      errors
    );
    expectMatch(
      html,
      /<meta\s+name="twitter:image"\s+content="([^"]+)"/i,
      OG_IMAGE,
      `${page.file} twitter:image`,
      errors
    );
  }
}

for (const guide of seo.guides || []) {
  const html = read(path.join("guides", guide.slug, "index.html"));
  const expectedRobots = guide.status === "live" ? "index, follow" : "noindex, follow";
  const expectedCanonical = `${BASE}/guides/${guide.slug}/`;

  expectMatch(html, /<title>([^<]+)<\/title>/i, guide.title, `${guide.slug} title`, errors);
  expectMatch(
    html,
    /<meta\s+name="description"\s+content="([^"]+)"/i,
    guide.description,
    `${guide.slug} meta description`,
    errors
  );
  expectMatch(
    html,
    /<link\s+rel="canonical"\s+href="([^"]+)"/i,
    expectedCanonical,
    `${guide.slug} canonical`,
    errors
  );
  expectMatch(
    html,
    /<meta\s+name="robots"\s+content="([^"]+)"/i,
    expectedRobots,
    `${guide.slug} robots`,
    errors
  );
  expectMatch(
    html,
    /<meta\s+property="og:url"\s+content="([^"]+)"/i,
    expectedCanonical,
    `${guide.slug} og:url`,
    errors
  );
  expectMatch(
    html,
    /<meta\s+property="og:image"\s+content="([^"]+)"/i,
    OG_IMAGE,
    `${guide.slug} og:image`,
    errors
  );
  expectMatch(
    html,
    /<meta\s+name="twitter:image"\s+content="([^"]+)"/i,
    OG_IMAGE,
    `${guide.slug} twitter:image`,
    errors
  );
}

if (errors.length) {
  console.error("SEO validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(`SEO validation passed for ${(seo.pages || []).length + (seo.guides || []).length} documents.`);
