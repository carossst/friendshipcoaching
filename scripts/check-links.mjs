#!/usr/bin/env node
// Walks every live page/guide, extracts every internal <a href="..."> (incl.
// #fragments), and verifies each resolves to a real file on disk and, for
// fragments, a real id in the target file. Also checks same-page fragments.
//
// Reads local files via seo-pages.json, not a live HTTP crawl. Reporter
// only, never edits files.

import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const seo = JSON.parse(fs.readFileSync(path.join(ROOT, "seo-pages.json"), "utf8"));
const SITE_HOST = new URL(seo.defaults.baseUrl).host;

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

function extractHrefs(html) {
  const hrefs = [];
  for (const m of html.matchAll(/<a\s[^>]*\bhref="([^"]*)"/gi)) {
    hrefs.push(m[1]);
  }
  return hrefs;
}

function extractIds(html) {
  const ids = new Set();
  for (const m of html.matchAll(/\bid="([^"]+)"/gi)) {
    ids.add(m[1]);
  }
  return ids;
}

// path.join collapses a lone "/" into "" on some platforms and always
// strips a trailing slash, both of which matter here: "/" must resolve to
// the site root's index.html, and "/guides/" must resolve to
// guides/index.html, not a file named "guides".
function resolveToLocalFile(urlPath) {
  let p = urlPath;
  if (p === "") p = "/";
  if (p === "/") return "index.html";
  if (p.endsWith("/")) return p.slice(1) + "index.html";
  return p.slice(1);
}

function classifyHref(href) {
  if (!href || href.startsWith("mailto:") || href.startsWith("tel:") || href.startsWith("javascript:")) {
    return null; // not checkable, not an error
  }
  if (href.startsWith("#")) {
    return { kind: "same-page-fragment", fragment: href.slice(1) };
  }
  let urlPath = href;
  let isExternal = false;

  if (/^https?:\/\//i.test(href)) {
    const u = new URL(href);
    if (u.host !== SITE_HOST) {
      isExternal = true;
    } else {
      urlPath = u.pathname + (u.hash || "");
    }
  }
  if (isExternal) return null; // external links out of scope for this check

  if (!urlPath.startsWith("/")) {
    return null; // relative paths not used by this site's convention; skip rather than mis-resolve
  }

  const [pathPart, fragment] = urlPath.split("#");
  const cleanPath = pathPart.split("?")[0];
  return { kind: "internal", path: cleanPath, fragment };
}

const idCache = new Map();
function idsFor(file) {
  if (idCache.has(file)) return idCache.get(file);
  const fullPath = path.join(ROOT, file);
  if (!fs.existsSync(fullPath)) {
    idCache.set(file, null);
    return null;
  }
  const ids = extractIds(fs.readFileSync(fullPath, "utf8"));
  idCache.set(file, ids);
  return ids;
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
    const hrefs = extractHrefs(html);
    const ownIds = extractIds(html);

    for (const href of hrefs) {
      const classified = classifyHref(href);
      if (!classified) continue;

      let issue = null;

      if (classified.kind === "same-page-fragment") {
        if (!ownIds.has(classified.fragment)) {
          issue = `Same-page anchor "#${classified.fragment}" has no matching id on this page.`;
        }
      } else {
        const localFile = resolveToLocalFile(classified.path);
        const targetFullPath = path.join(ROOT, localFile);
        if (!fs.existsSync(targetFullPath)) {
          issue = `Links to "${href}" -> local file "${localFile}" does not exist.`;
        } else if (classified.fragment) {
          const ids = idsFor(localFile);
          if (ids && !ids.has(classified.fragment)) {
            issue = `Links to "${href}": target file exists but has no id="${classified.fragment}".`;
          }
        }
      }

      if (issue) {
        const key = `${file}|${href}|${issue}`;
        if (seen.has(key)) continue;
        seen.add(key);
        total += 1;
        console.log(file);
        console.log(`  ${issue}`);
        console.log("");
      }
    }
  }

  console.log(`Checked ${files.length} live pages. ${total} issue(s) found.`);
  process.exit(total > 0 ? 1 : 0);
}

main();
