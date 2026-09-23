# Print2Pack Saudi Arabia — correction pass

Correcting and rebuilding **https://www.print2pack-saudi.com** — the site for
**Print 2 Pack Saudi Arabia**, a paper, printing, packaging and plastic trade fair held
**16–18 November 2026** in Jeddah.

**The job:** **one continuous project — correct the site and rebuild it**, worked on from
now until it is completely finished. No deadline, no deferred phases.

**Method:** the rebuild goes in its own codebase and the domain switches over when it is
done, so the live site keeps taking bookings while it is being built.

## Where this stands

- ✅ Full crawl done, **26 pages**, saved in `snapshots/`
- ✅ Design system drafted from the live site — `brand/design-system.html`
- ⏳ **Stage 1 is blocked on access.** Nothing can change on the current site until the
  client gives a login, or introduces the current developer.
- ▶️ **Stage 2, the rebuild, does not wait for that and can start today.**

## What the crawl actually found

Run on 2026-09-22 against the live site. **These are counts, not estimates.**

| | |
|---|---|
| Pages crawled | 26 |
| **Pages with no `<h1>`** | **26 — every single page** |
| **Pages with no `<title>`** | **2** — `/m/accommodation`, `/m/post-show-report` |
| Pages with no meta description | 6 |
| **Pages still naming 2024 or 2025** | **12** |
| Pages with zoom disabled | 26 — all of them |
| **Images with no alt text** | **528 of 608 (87%)** |

Plus: duplicate titles on `/show-gallery/8` and `/show-gallery/9`, and the venue is named
two different ways — "Jeddah Center for Exhibitions and Events" on the homepage,
"Jeddah Forums and Events Center" on the venue page.

## The plan

### Stage 1 — content corrections to the live site *(blocked on access)*
1. ⬜ **Back up the site before touching anything**
2. ⬜ Paste approved titles and descriptions from `content/titles.md`
3. ⬜ Add an `<h1>` to every page
4. ⬜ Replace oversized images
5. ⬜ Add alt text
6. ⬜ Fix the viewport tag so pinch-zoom works
7. ⬜ Trace the blank block on the desktop homepage
8. ⬜ Test that Book a Stand and Visitor Registration reach a real inbox

### Forms — built, waiting on one secret
Both forms are live in the site: **`/register/`** and **`/book-a-stand/`**, English and
Arabic, with client-side validation, a honeypot, and a required PDPL consent box linking
to `/privacy/`.

The handler is `site/shared/submit.js`, wrapped for both hosts —
`site/functions/api/` (Cloudflare Pages) and `site/api/` (Vercel). It re-checks everything
the browser checked, emails the organiser, and sends the person a confirmation.

⚠️ **It needs three environment variables before it can deliver anything:**
`RESEND_API_KEY`, `FROM_EMAIL`, and optionally `NOTIFY_EMAIL` (defaults to
`ksa@nilefairs.com`). **Without them the endpoint returns 503 and the form tells the
visitor to email directly** — deliberately loud, so nobody's registration is swallowed.

### Stage 2 — the rebuild *(start now, no access needed)*
9. ⬜ Pick the stack and scaffold the project
10. ⬜ Build the design system in CSS from `brand/design-system.html`
11. ⬜ Ask the client for the logo as a **vector file** — it is currently a 196×130 JPEG
12. ⬜ Rebuild all 26 pages
13. ⬜ **Arabic version with right-to-left layout** — about 40% of the work
14. ✅ Both forms built, validated, bilingual, with honeypot and consent.
    ⬜ Set `RESEND_API_KEY` + `FROM_EMAIL` to switch delivery on.
    ⬜ Write the privacy notice content (`/privacy/` exists, needs text).
15. ⬜ Structured event data for search engines
16. ⬜ **301 redirects from every existing `/m/...` address**
17. ⬜ An editor so the client can update exhibitor lists and galleries themselves
18. ⬜ Switch the domain over

### Throughout
19. ✅ **Images done.** `images.py` downloaded all 163, resized and converted them to
    WebP, and repointed every reference. **3.7 MB → 1.2 MB, 66% smaller.** Originals kept
    in `assets/original/`. One file 404s on the client's own server — listed below.
20. ⬜ `report.py` — before/after comparison
21. ⬜ Arabic copy for the new titles

## Running it

```bash
python3 audit.py before     # crawl and snapshot what search engines see
python3 shots.py before     # screenshot every page, desktop + phone

# ...after the fixes are live:
python3 audit.py after
python3 shots.py after
```

`audit.py` is standard library only — no pip install. One second between requests, because
this is a live site that is currently selling stands.

`shots.py` needs **Google Chrome** (already installed) and **Pillow**. It drives headless
Chrome at 1440px and 390px wide, trims the blank space under short pages, and writes a
contact sheet (`shots/before-index.html`) you can open and flip through. Roughly 20 seconds
per page — about eight minutes for the whole site.

## Live preview

**https://site-chi-lyart-68.vercel.app** — the current build, public, for sharing while we work.

(`print2pack-2026.vercel.app` is also aliased to it, but Vercel's Deployment Protection
sits in front of every alias except the auto-generated production one. Turning it off is
one toggle: Project → Settings → Deployment Protection → Vercel Authentication → Disabled.)

⚠️ Vercel's free Hobby plan forbids commercial use, and this is client work. It is fine as
a temporary preview for showing people, but **the real deployment must move to Cloudflare
Pages or Netlify**, both of which allow commercial use on their free tiers. The `_redirects`
file is also a Cloudflare/Netlify format — **Vercel ignores it, so the 301s from the old
`/m/...` URLs are not active here.**

## The site

The rebuild lives in `site/` — **Astro 7**, static output, deployable to Cloudflare Pages
or Netlify for free.

```bash
cd site
npm install      # first time only
npm run dev      # http://localhost:4321
npm run build    # static files into site/dist/
```

**Why Astro:** it resizes and compresses every image at build time (the old site serves a
2590px logo), it ships almost no JavaScript, `.astro` files are HTML with light templating,
and English/Arabic routing is built in.

**What is already standing:**
- `src/styles/tokens.css` — the design system as CSS variables. Two brand colours,
  neutrals derived from indigo, ink on orange.
- `src/data/site.js` — **every shared fact in one place**: dates, venue, address, contact,
  navigation. The old site named the venue two different ways; this makes that impossible.
- `src/layouts/Base.astro` — sets `lang` and `dir`, writes the meta and canonical tags,
  emits **ExhibitionEvent structured data**, loads only the font weights actually used,
  and **leaves pinch-zoom enabled**.
- `src/components/Header.astro`, `Footer.astro` — full navigation with dropdowns, a mobile
  menu, and the language switch.
- `src/pages/index.astro` and `src/pages/ar/index.astro` — **English and Arabic homepages,
  with right-to-left proven working.**
- `src/data/pages.js` — title, description, H1 and opening paragraph for **all 23 inner
  pages in both languages**, using the corrected 2026 copy.
- `src/layouts/Page.astro` + `src/pages/[slug].astro` + `src/pages/ar/[slug].astro` —
  **one template, 46 pages.** Adding a page means adding an entry to `pages.js`.

- `extract.py` → `content/extracted.json` — **the body content pulled off the live site in
  both languages**, reduced to structured blocks (heading / paragraph / list / table /
  image). The old Bootstrap markup is deliberately not carried over, only the words.
- `src/components/Blocks.astro` — renders those blocks in the new design system, with
  `srcset`, `sizes`, `width` and `height` on every image.
- `images.py` → `site/public/img/` — every image downloaded, resized to 1400px and 700px,
  converted to WebP. **3.7 MB of originals became 1.2 MB.** Re-runnable and resumable.

**48 pages build, and all of them pass the checks the old site failed:** every page has a
title, a description and exactly one `<h1>`; pinch-zoom works everywhere; no page names a
stale year; every page carries ExhibitionEvent structured data. 24 English, 24 Arabic.

## Layout

```
site/                 the rebuild — Astro
audit.py              the crawler
shots.py              screenshots every page, desktop + phone
report.py             before/after comparison        (to write)
snapshots/            JSON snapshots, one per run
shots/desktop/        full-page screenshots, 1440px
shots/mobile/         full-page screenshots, 390px
shots/*-index.html    contact sheet — open this one
content/titles.md     proposed titles, descriptions, H1s — the client approves this
assets/original/      images downloaded from the live site
assets/optimised/     the compressed replacements
```

## Rules for this job

1. **Back up before touching the live site.** It is taking real bookings.
2. **The rebuild lives in its own codebase.** The domain switches over only when it is done.
3. **Nothing goes live without written approval of the text.**
4. **Keep the before-snapshot and before-screenshots.** They are the only record of what
   the site was, and the proof of what changed.
5. **Everything visual follows `brand/design-system.html`.**

## Open questions for the client

1. Who controls the page content — is there an admin panel, and who has the login?
2. Are the 2026 dates and venue name confirmed? Which venue name is correct?
3. Where do Book a Stand and Visitor Registration submissions go today?
4. `/m/exhibitor-list-2025` — is that a historical archive to keep, or should it become 2026?
5. Should the Arabic pages be corrected in the same pass?
