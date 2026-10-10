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
export const GTAG_IDS = ['G-WK0QYDDV6X', 'AW-930149183'];

export const CONTACT_EMAIL = 'support@movingtoireland.co';
/** Legal entity behind the app and the site. */
export const PUBLISHER = 'Vavien Technology Limited';
export const SOCIAL = {
  instagram: 'https://instagram.com/movingtoirelandapp',
  twitter: 'https://twitter.com/MovingIreland',
};

/**
 * Affiliate partners. Links carry the partner's tracking id, so always render
 * them with rel="sponsored" and a data-placement for the click event.
 */
export const BUNQ = {
  url: 'https://www.getbunq.app/4FG8SPG/225JFQ/?uid=2325',
  /** From bunq's affiliate deck. Ask the bunq affiliate team before changing these claims. */
  points: [
    'Open an account in 5 minutes — no paperwork, no branch visit',
    '90 days to give your tax ID, so you can start before your PPS number arrives',
    'A free card straight away to settle in',
    'Spend, receive and hold money in 22 currencies',
    'App and support in English, and in your own language',
  ],
};

export const NAV = [
  { href: '/guides/', label: 'Guides' },
  { href: '/guides/cost-of-living/', label: 'Cost of living' },
  { href: '/guides/visas-and-permits/', label: 'Visas' },
  { href: '/guides/accommodation/', label: 'Housing' },
  { href: '/tools/take-home-pay-calculator/', label: 'Pay calculator' },
];

/** What the app offers beyond the articles — the reason to tap through. */
export const APP_FEATURES = [
  'Step-by-step checklist',
  'Tailored to your passport',
  'Pre-move & post-move',
  'Family & pet sections',
];
