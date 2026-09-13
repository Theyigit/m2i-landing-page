/** Site-wide constants. Change the domain here and in astro.config.mjs. */

export const SITE_URL = 'https://www.movingtoireland.co';
export const SITE_NAME = 'Moving to Ireland';
export const APP_NAME = 'Moving to Ireland';

/** Stable schema.org node ids, emitted once per page by Base.astro. */
export const ORG_ID = `${SITE_URL}/#organization`;
export const WEBSITE_ID = `${SITE_URL}/#website`;

export const APP_ID = 'id6446055261';
export const APP_STORE_URL = `https://apps.apple.com/app/moving-to-ireland/${APP_ID}`;

/** As reported by the App Store lookup API. Update when it moves. */
export const APP_RATING = { value: 4.9, count: 11 };

/**
 * Google tag ids loaded on every page: the Google Ads tag the old site carried.
 * Add a GA4 measurement id (G-…) here to get page analytics too. An empty list
 * disables the tag entirely.
 */
export const GTAG_IDS = ['AW-930149183'];

export const CONTACT_EMAIL = 'support@movingtoireland.co';
export const AUTHOR = 'Yigit Yilmaz';
export const SOCIAL = {
  instagram: 'https://instagram.com/movingtoirelandapp',
  twitter: 'https://twitter.com/MovingIreland',
};

export const NAV = [
  { href: '/guides/', label: 'Guides' },
  { href: '/guides/accommodation/', label: 'Housing' },
  { href: '/guides/paperwork/', label: 'Paperwork' },
  { href: '/guides/healthcare/', label: 'Healthcare' },
];

/** What the app offers beyond the articles — the reason to tap through. */
export const APP_FEATURES = [
  'Step-by-step checklist',
  'Tailored to your passport',
  'Pre-move & post-move',
  'Family & pet sections',
];
