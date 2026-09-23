# Project brief — read this first

*Written 2026-09-22 so a new session can pick this up cold.*

## What this is

Client work for **Nile Trade Fairs**, fixing their trade-fair website
**https://www.print2pack-saudi.com** before their show.

Moustafa is a fresh Computer Science graduate: comfortable with **HTML and CSS**, knows
**Python** well, some JavaScript, and has not shipped a site before. Explain choices as you
go and prefer the simpler option where two are close.

## The site and the event

**Print 2 Pack Saudi Arabia** — a trade fair for the paper, printing, packaging and plastic
industries, organised by **Nile Trade Fairs**, who also run Paper-Me and shows in Egypt.

| | |
|---|---|
| Live site | https://www.print2pack-saudi.com |
| Event | **16–18 November 2026** |
| Venue | Jeddah Center for Exhibitions and Events (JCEE), El-Medina Road, Al Nuzha District |
| Languages | English + Arabic |
| Contact on the site | `ksa@nilefairs.com` · WhatsApp +966 54 062 8088 |

**All corrected copy uses 16–18 November 2026.**

## What the crawl found (2026-09-22, live site, 26 pages)

| | |
|---|---|
| Pages with no `<h1>` | **26 — all of them** |
| Pages with no `<title>` | 2 — `/m/accommodation`, `/m/post-show-report` |
| Pages with no meta description | 6 |
| **Pages still naming 2024 or 2025** | **12** |
| Pages with zoom disabled | 26 |
| Images with no alt text | **528 of 608 (87%)** |

Plus: the venue is named two different ways (*Jeddah Center for Exhibitions and Events* vs
*Jeddah Forums and Events Center*), and three gallery pages share one title.

**The headline for the client is the year.** `/m/book-a-stand` — the page that takes their
money — is titled *"Book a stand at PRINT2PACK Saudi Arabia 2024."* The show itself is
**16–18 November 2026**, which is the date all the corrected copy uses.

## State of play

**Done**
- `audit.py` — crawls the site, records what search engines see. 26 pages, 0 failures.
- `snapshots/before_*.json` — the before-snapshot. **Captured before any changes. Do not delete it.**
- `shots.py` — screenshots every page at 1440px and 390px, trims the blank tail,
  builds a contact sheet. 52 images in `shots/`.
- `content/titles.md` — **new title, description and H1 written for all 26 pages.**
  Ready to send for approval.

- `brand/design-system.html` — **design system for the rebuild**, every value sampled from
  the live site: palette, type scale, logo rules, components, Arabic/RTL notes.
  Published at https://claude.ai/artifact/Diftav1fa5DTsjy58WS2Tr
  **Use it for anything visual on this project.**

  **The decision, made 2026-09-22: two colours only — the two in the logo.**
  **Indigo `#241E70`** and **orange `#F17825`**. Everything else was cut, including the
  Saudi green from the first draft; national context lives in the photography, not a swatch.

  Every neutral is **the same indigo at a different lightness**: `#110F2D` ink ·
  `#201C53` deep · `#322C81` light · `#5C53C4` muted · `#B6B2E5` pale · `#E5E4F5` tint.
  Never a generic grey, never a new hue. The only exception is a muted state set
  (error / warning / success) used **inside messages only**.

  ⚠️ **White text on the orange scores 2.8:1 and fails accessibility at every size.**
  Put **ink `#110F2D`** on orange instead — 6.5:1, passes, and the brand colour is
  unchanged. **Orange is a fill, never a text colour** (2.6:1 on light grounds).

  Type: **Oswald** display, **Poppins** body, base **16px**.

## The plan — one job, worked start to finish

### Stage 1 — content corrections to the live site
Applied as soon as the client gives access. This also produces the copy the rebuild uses.

- ⬜ Back up the site before touching anything
- ⬜ Paste the approved titles and descriptions from `content/titles.md`
- ⬜ Add an `<h1>` to every page
- ⬜ Replace the oversized images with the compressed set
- ⬜ Add alt text
- ⬜ Fix the viewport tag so pinch-zoom works
- ⬜ Trace the blank block on the desktop homepage
- ⬜ Test that Book a Stand and Visitor Registration reach a real inbox

### Stage 2 — the rebuild · **can start now, no access needed**
New codebase, built alongside the live site, switched over when complete.

- ⬜ Pick the stack and scaffold the project
- ⬜ Build the design system in CSS from `brand/design-system.html`
- ⬜ Get the logo as a vector file from the client — currently a 196×130 JPEG
- ⬜ Rebuild all 26 pages
- ⬜ Full **Arabic version with right-to-left layout** — roughly 40% of the work
- ⬜ Rebuild Book a Stand and Visitor Registration, with reliable delivery and spam protection
- ⬜ Structured event data so search engines show dates and venue directly
- ⬜ **301 redirects from every existing `/m/...` address** — non-negotiable, or the
  existing search ranking is lost
- ⬜ An editor for the client's team: exhibitor lists and galleries without a developer
- ⬜ Switch the domain over

### Throughout
- ⬜ Download and compress the oversized images → `assets/`. **No access needed — the
  images are on public URLs.**
- ⬜ `report.py` — before/after comparison from two snapshots
- ⬜ Arabic copy for the new titles (ask the client who writes the Arabic)

**🚧 Only Stage 1 is blocked.** Nobody has a login yet — nothing can go live on the current
site until the client gives access to whatever manages the pages, or introduces the current
developer. The `/m/` URLs and `/uploads/configurationsite/` suggest a custom admin panel
built by someone else. **Stage 2 does not wait for this.**

## How to run it

```bash
python3 audit.py before     # crawl; already done — don't overwrite the before-snapshot
python3 shots.py before     # screenshots; already done

# after the fixes are live:
python3 audit.py after
python3 shots.py after
```

`audit.py` is standard library only. `shots.py` needs Google Chrome (installed at
`/Applications/Google Chrome.app`) and Pillow. Python here is **3.9.6** — no `match`, no
new-style union types at runtime.

Both are polite to the live site: one second between requests, and `shots.py` resumes if
it dies partway.

**Two traps already solved — don't reintroduce them.** The site writes its links with
backslashes, which browsers fix and `urljoin` does not. And the floating WhatsApp button
is fixed to the viewport, so it paints at the bottom of a tall screenshot and defeats a
naive crop — `trim()` ignores the right-hand strip because of it.

## Rules

1. **Never touch the live site without a backup first.** It is taking real bookings.
2. **Build the rebuild in its own codebase.** Switch the domain over only when it is finished.
3. **Nothing goes live without the client approving the text in writing.**
4. **Keep the before-snapshot and before-screenshots.** They are the only record of what the
   site looked like before this work, and the proof of what changed.
5. **Everything visual follows `brand/design-system.html`.** Two colours, neutrals from
   indigo, ink on orange, never white on orange.

## Open questions for the client

1. Who controls the page content — is there an admin panel, and who has the login?
2. Are the 2026 dates confirmed, and **which venue name is correct**?
3. Where do Book a Stand and Visitor Registration submissions go today?
4. Is `/m/exhibitor-list-2025` a historical archive, or should it become 2026?
5. Should the Arabic pages be corrected in the same pass, and who writes the Arabic?
6. Which editions are `/show-gallery/8` and `/show-gallery/9`?
7. **Assets we do not have and cannot invent:**
   - **Event photography.** The largest image on the whole site is 1600×987, and the
     gallery images are 300×200. There is nothing usable for a hero background.
   - **Hotel photographs** for the accommodation page.
   - **Which logo belongs to which company.** There are 147 exhibitor logos with no alt
     text and no names attached, and a separate table of company names. Matching them
     needs the client's own list.
8. ⚠️ **Typos in their Arabic content**, carried over from the live site: `ا ل طباعة`,
   `ا لتعبئة والتغليف`, `أ خرى` — Arabic words written with spaces between the letters,
   which breaks the word. Worth fixing on the way through, with the reviewer.

## The ECC plugin

`.claude/settings.json` enables **ECC** (`affaan-m/ECC`) **for this project only** — not
globally, and never in the notes vault.

**Hooks are deliberately off** (`hooks_enabled: false`). ECC ships 24 hooks, two of which
match every tool call. Skills and commands load; no local automation runs. To try them
later, flip `hooks_enabled` to `true` — `hook_profile` is already set to `minimal`.

`autoUpdate` is off too, so a new version with new hooks never arrives silently.

Read before it was installed: the hook scripts make **no network calls** (the only URLs in
them are comments), touch **no credentials**, and write only under `~/.claude/`. One of
them logs every bash command locally to `~/.claude/bash-commands.log`.

## Hosting

Deploy to **Cloudflare Pages** or **Netlify** — both allow commercial use on their free
tier, both give free SSL. **Not Vercel's free Hobby plan**: it forbids commercial use, and
being paid to build a site makes it commercial even if the site sells nothing.

Register the domain in the client's own name, with the team as technical contact.
