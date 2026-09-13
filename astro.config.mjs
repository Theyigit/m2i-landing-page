import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import guides from './src/data/guides.json' with { type: 'json' };

// Every guide is regenerated from the same content build, so one date
// describes them all.
const LAST_MOD = new Date(`${guides.generated}T00:00:00Z`).toISOString();

export default defineConfig({
  site: 'https://www.movingtoireland.co',
  output: 'static',
  // Directory output makes the trailing slash the real URL; canonicals and the
  // sitemap follow the same form so the two variants never compete.
  trailingSlash: 'always',
  build: { inlineStylesheets: 'always' },
  // The App Store listing links the legal pages at their old Jekyll paths.
  redirects: {
    '/privacypolicy': '/privacy/',
    '/termsofservice': '/terms/',
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404'),
      serialize(item) {
        const path = new URL(item.url).pathname;
        const priority =
          path === '/'
            ? 1
            : path === '/guides/'
              ? 0.9
              : path === '/privacy/' || path === '/terms/'
                ? 0.3
                : path.split('/').filter(Boolean).length === 2
                  ? 0.8 // category hubs
                  : 0.7; // articles
        return {
          ...item,
          lastmod: LAST_MOD,
          changefreq: priority <= 0.3 ? 'yearly' : 'monthly',
          priority,
        };
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
