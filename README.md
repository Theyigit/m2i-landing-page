# Moving to Ireland — website

Marketing site and organic-traffic funnel for the
[Moving to Ireland](https://apps.apple.com/app/moving-to-ireland/id6446055261) iOS app
(source: `~/Developer/ProgressApp`). Same strategy as
[ukdrivingtestcentres.co.uk](https://github.com/Theyigit/uk-driving-test-centres-website):
content pages rank, every page funnels to the App Store.

**Domain:** `www.movingtoireland.co` (set in `astro.config.mjs`, `src/lib/site.ts`,
`public/CNAME` and the sitemap line of `public/robots.txt`).

## How the funnel works

The app bundles 55 guides (about 21,000 words) across 8 categories. The site
publishes the **opening ~20% of every guide** as its own page, then a Medium-style
gate: the last visible paragraph fades out under a "keep reading in the app" panel
listing the sections still to come. Only the preview is ever emitted — the rest of
each article never reaches the build output, so there is nothing to un-hide.

```
/                                  home: hero, categories, start-here, app features, FAQ
/guides/                           every guide grouped by category
/guides/<category>/                category hub, guides in the app's step order
/guides/<category>/<slug>/         guide preview + gate + neighbours + app CTA
/privacy/  /terms/                 legal (old /privacypolicy and /termsofservice redirect here)
```

## Content pipeline

```
~/Developer/ProgressApp/.../Content/content.json + <Category>/<n>-<slug>.html
   │   (Google Docs HTML exports, as bundled in the app)
   ▼
scripts/build_content.py  →  src/data/guides.json   (committed)
scripts/build_images.py   →  favicons, CTA screenshot WebP, OG card
```

```bash
npm run content:build   # re-run when the app's content changes
```

`build_content.py` strips the Google Docs CSS and classes, unwraps the
`google.com/url` redirect links, maps document styles to `h2`/`h3`/`strong`, and
cuts the preview at a block boundary near `PREVIEW_SHARE` (a long list or table can
push individual articles to 10–40%). Titles that were misspelt or ambiguous in the
app are corrected in `TITLE_FIXES`.

## Tech stack

Astro 6 static output, Tailwind CSS 4, no client JavaScript except the optional
deferred Google tag loader (`GTAG_IDS` in `src/lib/site.ts`: the Ads tag, plus a GA4 id if you add one). Requires Node 22+.

```bash
nvm use 22
npm install
npm run dev       # http://localhost:4321
npm run build     # → dist/
```

## Deploy

GitHub Pages via `.github/workflows/deploy.yml`. The repo was a Jekyll template
that Pages built itself; **Settings → Pages → Source must be switched to "GitHub
Actions"** once, after which every push to `master` deploys. `public/CNAME` keeps
the custom domain.
