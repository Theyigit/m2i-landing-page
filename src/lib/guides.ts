/**
 * Typed access to src/data/guides.json, the output of scripts/build_content.py.
 * Pages import from here rather than the JSON so the shape is declared once.
 */

import data from '../data/guides.json' with { type: 'json' };

export interface Article {
  slug: string;
  title: string;
  appTitle: string;
  /** The app's own label, e.g. "Special content for US citizens". */
  note: string;
  audience: string[];
  description: string;
  wordCount: number;
  readMinutes: number;
  previewWordCount: number;
  previewShare: number;
  previewHtml: string;
  sections: string[];
}

export interface Category {
  slug: string;
  name: string;
  tagline: string;
  audience: string[];
  articles: Article[];
}

export const generated: string = data.generated;
export const previewShare: number = data.previewShare;
export const articleCount: number = data.articleCount;
export const wordCount: number = data.wordCount;
export const categories: Category[] = data.categories as Category[];

export const categoryPath = (c: Category) => `/guides/${c.slug}/`;
export const articlePath = (c: Category, a: Article) => `/guides/${c.slug}/${a.slug}/`;

export function findCategory(slug: string): Category | undefined {
  return categories.find((c) => c.slug === slug);
}

/** Editorial one-liners for the category cards; the app's taglines are terse. */
export const CATEGORY_BLURBS: Record<string, string> = {
  'pre-move':
    'Passports, visas, what to sell, what to bring, and how to move your money before you land.',
  pets: 'The rules, airlines and airports for bringing a pet — and the rental market you will face with one.',
  paperwork: 'PPS number, residence permit, bank account and proof of address, in the order they unblock each other.',
  accommodation:
    'A twelve-step route through the hardest part of the move: budget, search, viewings, lease and your rights.',
  utilities: 'Phone, electricity, gas, water, broadband, the TV licence and the bins.',
  transportation:
    'Buses and trains, the Leap card, and what happens to your driving licence depending on where it was issued.',
  healthcare: 'How the HSE works, finding a GP, emergencies, insurance and children’s health.',
  schooling: 'Pre-school to third level: how Irish education is structured and how to enrol your child.',
};

/** Emoji glyphs for the category cards. */
export const CATEGORY_ICONS: Record<string, string> = {
  'pre-move': '🧳',
  pets: '🐾',
  paperwork: '🪪',
  accommodation: '🏠',
  utilities: '💡',
  transportation: '🚌',
  healthcare: '🩺',
  schooling: '🎓',
};
