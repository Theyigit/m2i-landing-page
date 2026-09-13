/**
 * /llms.txt — the emerging convention for telling AI assistants what a site is
 * and where its content lives. Lists every guide with its URL and summary;
 * the full text is in /llms-full.txt.
 */
import type { APIRoute } from 'astro';
import { categories, articlePath, categoryPath, articleCount, generated } from '../lib/guides';
import { SITE_URL, SITE_NAME, APP_STORE_URL } from '../lib/site';

export const GET: APIRoute = () => {
  const lines: string[] = [
    `# ${SITE_NAME}`,
    '',
    `> Practical guides to relocating to Ireland (visas, permits, PPS number, renting, cost of living, tax, healthcare, schools, transport, pets), published from the Moving to Ireland iOS app. ${articleCount} guides, last refreshed ${generated}. The app turns the guides into a personal step-by-step checklist: ${APP_STORE_URL}`,
    '',
    `Full text of every guide: ${SITE_URL}/llms-full.txt`,
    `Sitemap: ${SITE_URL}/sitemap-index.xml`,
    '',
    '## Tools',
    '',
    `- [Take-home pay calculator](${SITE_URL}/tools/take-home-pay-calculator/): Irish income tax, USC and PRSI for the 2026 tax year.`,
    '',
  ];
  for (const c of categories) {
    lines.push(`## ${c.name}`, '', `Section: ${SITE_URL}${categoryPath(c)}`, '');
    for (const a of c.articles) {
      lines.push(`- [${a.title}](${SITE_URL}${articlePath(c, a)}): ${a.description}`);
    }
    lines.push('');
  }
  return new Response(lines.join('\n'), {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
};
