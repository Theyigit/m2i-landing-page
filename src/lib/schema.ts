/**
 * Builders for structured data. Base.astro publishes the Organization and
 * WebSite nodes on every page, so everything here references them by @id.
 */

import { SITE_URL, WEBSITE_ID } from './site';
import { generated } from './guides';

type Crumb = { name: string; path?: string };

/** `path` is omitted on the last crumb — the current page is not a link. */
export function breadcrumbs(trail: Crumb[]) {
  return {
    '@type': 'BreadcrumbList',
    itemListElement: [{ name: 'Home', path: '/' }, ...trail].map((crumb, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: crumb.name,
      ...(crumb.path ? { item: `${SITE_URL}${crumb.path}` } : {}),
    })),
  };
}

export function collectionPage(opts: { path: string; name: string; description: string }) {
  return {
    '@type': 'CollectionPage',
    '@id': `${SITE_URL}${opts.path}#webpage`,
    url: `${SITE_URL}${opts.path}`,
    name: opts.name,
    description: opts.description,
    inLanguage: 'en-IE',
    isPartOf: { '@id': WEBSITE_ID },
    dateModified: generated,
  };
}

export function itemList(name: string, items: { name: string; path: string }[]) {
  return {
    '@type': 'ItemList',
    name,
    numberOfItems: items.length,
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      url: `${SITE_URL}${item.path}`,
    })),
  };
}
