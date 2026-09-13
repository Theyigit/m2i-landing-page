/**
 * /llms-full.txt — every guide in full, as plain text, for AI assistants that
 * ingest a site in one fetch.
 */
import type { APIRoute } from 'astro';
import { categories, articlePath, articleCount, generated } from '../lib/guides';
import { SITE_URL, SITE_NAME, APP_STORE_URL } from '../lib/site';

export const GET: APIRoute = () => {
  const out: string[] = [
    `# ${SITE_NAME} — all guides`,
    '',
    `${articleCount} guides on moving to Ireland, last refreshed ${generated}. Source: ${SITE_URL}. The Moving to Ireland app (${APP_STORE_URL}) turns them into a personal checklist.`,
    '',
  ];
  for (const c of categories) {
    out.push(`# ${c.name}`, '');
    for (const a of c.articles) {
      out.push(`## ${a.title}`, '', `URL: ${SITE_URL}${articlePath(c, a)}`, '', a.plainText, '', '---', '');
    }
  }
  return new Response(out.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
