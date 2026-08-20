# Fungua Systems

**Technology solutions, open to everyone.**

A Nairobi-built technology studio's marketing site — static, fast, and open source. Live at [fungua-systems.pages.dev](https://fungua-systems.pages.dev/) (custom domain pending).

## Stack

Plain HTML, CSS, and zero JavaScript frameworks. No build step to deploy. This is a deliberate choice, not a placeholder — see [ARCHITECTURE.md](./ARCHITECTURE.md#why-no-framework) for the reasoning.

## Local development

No install required. Either:
- Open `index.html` directly in a browser, or
- Run a local static server for correct relative-path behavior:
  ```bash
  python3 -m http.server 8000
  # visit http://localhost:8000
  ```

## Editing content

Page content lives in `build/build.py` as plain Python string variables (`home_body`, `about_body`, etc.), rendered through a shared header/nav/footer template. To change copy:

```bash
python3 build/build.py   # regenerates index.html, about.html, approach.html, labs.html, contact.html
```

Then commit the regenerated HTML files — they're what actually gets deployed, not the generator.

## Deployment

Hosted on **Cloudflare Pages**, connected to this repo's `main` branch. No build command, no output directory override — the repo root *is* the output, since these are already static files. Every push to `main` redeploys automatically.

## File structure

```
├── index.html, about.html, approach.html, labs.html, contact.html
├── build/build.py          # static site generator (dev tool, not runtime)
├── assets/
│   ├── css/style.css       # single shared stylesheet, all pages
│   ├── fonts/*.woff2       # self-hosted, subsetted (~80KB total)
│   └── img/                # favicon, social share image
├── robots.txt, sitemap.xml, llms.txt   # crawler + AI-agent readability
├── LICENSE                 # MIT
└── ARCHITECTURE.md         # system design, current + planned
```

## License

MIT — see [LICENSE](./LICENSE).

## Contact

funguasystems@gmail.com
