# Architecture

System design for the Fungua Systems marketing site — what exists today, and what's explicitly deferred and why. Written the way a senior engineer sizes a system: build what the current requirements justify, document the trigger conditions for what comes next, and don't build ahead of need.

## 1. Overview

This is a **static marketing site**, not an application. Five HTML pages, one stylesheet, self-hosted fonts, no server-side logic, no runtime dependencies. It is intentionally the simplest architecture that satisfies the current requirement: tell visitors what Fungua Systems is, and let them get in touch.

```
Visitor's browser
      │  HTTPS GET
      ▼
Cloudflare global edge cache  ──serves static files, no origin compute──▶  Visitor
      ▲
      │  git push (auto-deploy)
GitHub repo (source of truth)
```

There is no application server in this diagram because there is nothing that needs one yet — no user accounts, no data being written, no per-request logic.

## 2. Why no framework

Next.js/Astro-style SSG frameworks earn their complexity when a site has *dynamic* content — a CMS feeding pages, personalization, or frequent structural changes by non-technical editors. Every page here is authored by one person and changes rarely. A framework would add a Node build pipeline, a `node_modules` tree, and a deploy step that can fail — for zero runtime benefit, since the framework's own best output *is* static HTML, which is what's already being hand-authored here. Introducing one now would be solving a problem that doesn't exist yet.

**Trigger to revisit:** if a second person starts editing copy, or the number of pages exceeds ~15–20 and the current Python generator (`build/build.py`) becomes unwieldy, move to Astro (keeps the SSG-to-static output model) rather than Next.js (which assumes a server runtime this site doesn't need).

## 3. File structure

```
├── index.html, about.html, approach.html, labs.html, contact.html   # generated output — this is what deploys
├── build/
│   └── build.py               # generator: shared template + per-page content, run locally, output committed
├── assets/
│   ├── css/style.css          # single design-token-driven stylesheet, ~230 lines, no per-page CSS
│   ├── fonts/*.woff2          # self-hosted, Latin-subsetted, 6 files / ~80KB total
│   └── img/                   # favicon.png, favicon-32.png, og-image.png
├── robots.txt, sitemap.xml, llms.txt
├── LICENSE (MIT)
├── README.md
└── ARCHITECTURE.md
```

Pages are plain files, not framework routes — `/about.html` is a real file Cloudflare's edge serves directly, no routing layer involved.

## 4. UI architecture

- **Design tokens** (`:root` custom properties in `style.css`): a locked color palette (charcoal base, brass accent), three typefaces each with one job (display, body, label), and a single spacing/type scale. No page introduces a one-off color or font.
- **Shared chrome, unique content**: every page gets the same nav (with `aria-current="page"` marking the active link) and footer via the generator template; only the `<main>` content differs per page.
- **Navigation model**: true multi-page — each nav item is a real page load to a real URL, not a scroll-to-anchor or client-side route swap. This was a deliberate choice over an SPA: it means every page is independently indexable, independently linkable, needs zero JavaScript to navigate, and works identically whether or not the visitor (or a crawler, or an AI agent) executes JS at all.
- **One signature visual motif** (the opening-ring mark, echoing "fungua" = "to open"), reused consistently across the nav logo, favicon, and social share image — not a different graphic in every context.

## 5. Data & API layer — current state: none, by design

There is no database and no API endpoint in this repository. That's not an omission — there is no data being collected yet (the contact "flow" is a `mailto:` link, which needs no backend), so a database would have nothing to store and an API would have nothing to serve. Building either now would be dead weight.

### What triggers each one, and what it would look like

**A real contact form** (vs. the current `mailto:` link) — triggered by: wanting submissions logged/searchable rather than living in an inbox.
- `POST /api/contact` as a **Cloudflare Pages Function** (`functions/api/contact.js`) — same platform, no new hosting vendor.
- Validated server-side with **Zod** before it touches storage.
- Stored in **Cloudflare D1** (SQL) or **KV** (simple key-value) — both free-tier, both native to the hosting already in place.
- Rate-limited at the edge (Cloudflare's own rate limiting) to prevent spam, before adding a paid dependency like Upstash.

Sketch of the schema, once it's real:
```sql
CREATE TABLE contact_submissions (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  message TEXT NOT NULL,
  submitted_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

**Multi-tenancy** — flagged explicitly because it was raised and doesn't apply today. This becomes a real requirement only if Fungua Systems ships a *product* that other organizations log into with isolated data — for example, if the fuel-monitoring platform (see Labs) is built and multiple client companies each need a private dashboard over their own sensor data. At that point the shape would be a `tenants` table, a `tenant_id` foreign key on every tenant-scoped table, and row-level scoping on every query — a real, well-understood pattern, just not one this static site has any use for. Building it now, with no product and no second tenant to isolate, would be structure with nothing behind it.

## 6. Performance

- Zero JS frameworks, zero render-blocking third-party requests.
- Fonts self-hosted and subsetted to the Latin characters actually used (English + Swahili share the same 26-letter base) — 80KB total across 6 files, versus a typical multi-family Google Fonts CDN load.
- Critical fonts preloaded (`<link rel="preload">`) so headline text doesn't flash unstyled.
- No layout-shifting images above the fold — the hero graphic is inline SVG/CSS, not a loaded image file.

## 7. Accessibility

- Contrast independently calculated, not eyeballed: body text 15.3:1, muted text 6.4:1, links 9.5:1 against the background — all pass WCAG AA, most pass AAA.
- Visible focus states on every interactive element (`:focus-visible`).
- `prefers-reduced-motion` respected — the hero animation becomes a static end-state for anyone who's set that preference.
- Skip-to-content link for keyboard/screen-reader users.
- `lang="sw"` correctly marks the Swahili phrases so screen readers switch pronunciation rules instead of reading them as mispronounced English.
- Semantic landmarks (`<nav>`, `<main>`, `<footer>`) on every page.

## 8. Agent & crawler readability

- `robots.txt` + `sitemap.xml` for conventional search indexing.
- `llms.txt` — an emerging convention (not yet a formal standard) that gives AI agents a concise, structured summary of the site instead of making them parse full HTML across every page.
- `Organization` JSON-LD structured data on every page, so both search engines and AI agents get an unambiguous, machine-readable answer to "what is this and who runs it."

## 9. Scaling story

The honest answer: this architecture already scales further than most backend-heavy sites do, for free. Static files served from Cloudflare's edge cache have no origin server to become a bottleneck — the same file gets served from whichever edge location is closest to each visitor, whether that's 10 visitors a day or 10,000. The point at which this needs to change is not traffic — it's when the site needs to *do* something dynamic (accounts, a form with server-side storage, personalization). That's section 5, not this one.

## 10. Email

Cloudflare Email Routing (`you@yourdomain.com` → forwarded to Gmail, free) requires owning a domain on Cloudflare's DNS — it cannot attach to the free `.workers.dev` subdomain this project currently runs on. Deferred until the domain purchase; see the project chat history for the exact setup steps once that happens.
