#!/usr/bin/env node
// Post-build: write a Markdown twin of every built HTML page.
//
// /guides/foo/index.html  ->  /guides/foo.md   (served at /guides/foo.md)
// /index.html             ->  /index.md
//
// AI crawlers and assistants read a page's Markdown twin instead of parsing
// the full HTML. Each page links to its twin with
// <link rel="alternate" type="text/markdown">. Only the main content is
// converted (nav, footer, scripts and forms are dropped).
import { promises as fs } from 'node:fs';
import path from 'node:path';
import TurndownService from 'turndown';
import { tables, strikethrough } from 'turndown-plugin-gfm';

const DIST = process.argv[2] || 'dist';
const SITE = (process.env.SITE_URL || process.argv[3] || '').replace(/\/$/, '');

const td = new TurndownService({ headingStyle: 'atx', codeBlockStyle: 'fenced', bulletListMarker: '-' });
td.remove(['script', 'style', 'noscript', 'svg', 'form', 'button', 'iframe', 'nav', 'footer']);
// Drop anything explicitly marked as chrome/interactive.
td.addRule('skip-marked', {
  filter: (node) => node.nodeType === 1 && (
    node.getAttribute('data-md-skip') != null ||
    /\b(breadcrumbs?|share|cookie|toc-toggle|skip-link)\b/i.test(node.getAttribute('class') || '')
  ),
  replacement: () => '',
});
td.use([tables, strikethrough]);
// Tables with no rows (filled in by client-side JS) crash the GFM table plugin.
// Added after the plugin so it takes precedence.
td.addRule('skip-empty-table', {
  filter: (node) => /^(TABLE|THEAD|TBODY|TFOOT)$/.test(node.nodeName) && (node.closest('table')?.rows.length ?? 0) === 0,
  replacement: () => '',
});

function pick(html, re) { const m = html.match(re); return m ? m[1].trim() : ''; }
function decode(s) {
  return s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/&nbsp;/g, ' ');
}

export function htmlToMarkdown(html, url) {
  const title = decode(pick(html, /<title[^>]*>([\s\S]*?)<\/title>/i)).replace(/\s+/g, ' ');
  const description = decode(pick(html, /<meta\s+name="description"\s+content="([^"]*)"/i) || pick(html, /<meta\s+content="([^"]*)"\s+name="description"/i));
  const main = pick(html, /<main[^>]*>([\s\S]*?)<\/main>/i) || pick(html, /<article[^>]*>([\s\S]*?)<\/article>/i) || pick(html, /<body[^>]*>([\s\S]*?)<\/body>/i);
  let body = td.turndown(main).replace(/\n{3,}/g, '\n\n').trim();
  // Absolute links so the document stands alone.
  if (SITE) body = body.replace(/\]\((\/[^)\s]*)\)/g, `](${SITE}$1)`);
  const front = [`# ${title}`, description ? `\n> ${description}` : '', url ? `\nSource: ${url}` : ''].filter(Boolean).join('\n');
  return `${front}\n\n${body}\n`;
}

async function* walk(dir) {
  for (const e of await fs.readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (e.name === 'index.html') yield p;
  }
}

async function main() {
  let n = 0;
  for await (const file of walk(DIST)) {
    const rel = path.relative(DIST, path.dirname(file));           // '' | 'guides/foo'
    if (/^404$/.test(rel)) continue;
    const html = await fs.readFile(file, 'utf8');
    const urlPath = rel ? `/${rel.split(path.sep).join('/')}/` : '/';
    const out = rel ? path.join(DIST, `${rel}.md`) : path.join(DIST, 'index.md');
    await fs.writeFile(out, htmlToMarkdown(html, SITE ? SITE + urlPath : ''));
    n++;
  }
  console.log(`build-markdown: wrote ${n} .md files under ${DIST}`);
}

if (import.meta.url === `file://${process.argv[1]}`) main().catch((e) => { console.error(e); process.exit(1); });
