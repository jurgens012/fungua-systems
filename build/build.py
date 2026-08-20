#!/usr/bin/env python3
"""
Fungua Systems — static site generator.
Not a runtime dependency: run this locally after editing PAGES below,
commit the generated HTML files, and Cloudflare Pages deploys the
plain static output. No build step runs on the server.
"""
import os

LOGO_SVG = '''<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle cx="12" cy="12" r="8" fill="none" stroke="#E7B24B" stroke-width="2" stroke-linecap="round" stroke-dasharray="36 14" transform="rotate(70 12 12)"/>
      <circle cx="19.6" cy="12" r="0.9" fill="#E7B24B"/>
    </svg>'''

NAV_ITEMS = [
    ("about.html", "About"),
    ("approach.html", "Approach"),
    ("labs.html", "Labs"),
    ("contact.html", "Contact"),
]

HEAD_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">

<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="icon" type="image/png" sizes="1024x1024" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/favicon.png">
<meta name="theme-color" content="#10151B">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="https://fungua-systems.funguasystems.workers.dev/{path}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Fungua Systems">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="/assets/img/og-image.png">
<meta property="og:url" content="https://fungua-systems.funguasystems.workers.dev/{path}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="/assets/img/og-image.png">

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Fungua Systems",
  "url": "https://fungua-systems.funguasystems.workers.dev/",
  "slogan": "Technology solutions, open to everyone.",
  "founder": {{ "@type": "Person", "name": "Jurgens Matika" }},
  "email": "funguasystems@gmail.com"
}}
</script>

<link rel="preload" href="/assets/fonts/BricolageGrotesque-Bold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/IBMPlexSerif-Italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/IBMPlexMono-Regular.woff2" as="font" type="font/woff2" crossorigin>
<style>
  @font-face{{ font-family:'Bricolage Grotesque'; src:url('/assets/fonts/BricolageGrotesque-Regular.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
  @font-face{{ font-family:'Bricolage Grotesque'; src:url('/assets/fonts/BricolageGrotesque-Bold.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}
  @font-face{{ font-family:'IBM Plex Serif'; src:url('/assets/fonts/IBMPlexSerif-Regular.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
  @font-face{{ font-family:'IBM Plex Serif'; src:url('/assets/fonts/IBMPlexSerif-Italic.woff2') format('woff2'); font-weight:400; font-style:italic; font-display:swap; }}
  @font-face{{ font-family:'IBM Plex Mono'; src:url('/assets/fonts/IBMPlexMono-Regular.woff2') format('woff2'); font-weight:400; font-style:normal; font-display:swap; }}
  @font-face{{ font-family:'IBM Plex Mono'; src:url('/assets/fonts/IBMPlexMono-Bold.woff2') format('woff2'); font-weight:700; font-style:normal; font-display:swap; }}
</style>
<link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>

<nav>
  <div class="nav-inner">
    <a href="/index.html" class="brand">
      {logo}
      FUNGUA SYSTEMS
    </a>
    <input type="checkbox" id="navToggle">
    <label for="navToggle" class="nav-burger" aria-label="Toggle menu">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </label>
    <ul class="nav-links">
{navlinks}
    </ul>
  </div>
</nav>
'''

FOOT_TEMPLATE = '''
<footer>
  <div class="wrap" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px;">
    <span class="tag">Fungua Systems — <span lang="sw">teknolojia, wazi kwa wote</span>.</span>
    <div style="display:flex; gap:20px; align-items:center; font-family:var(--font-mono); font-size:0.75rem;">
      <a href="mailto:funguasystems@gmail.com" style="color:var(--text-muted); text-decoration:none;">Email</a>
      <a href="https://x.com/funguasystems" target="_blank" rel="noopener" style="color:var(--text-muted); text-decoration:none;">X</a>
      <a href="https://www.linkedin.com/company/fungua-systems" target="_blank" rel="noopener" style="color:var(--text-muted); text-decoration:none;">LinkedIn</a>
    </div>
    <span class="year">Nairobi, Kenya</span>
  </div>
</footer>
</body>
</html>
'''

def render_nav(current):
    lines = []
    for href, label in NAV_ITEMS:
        current_attr = ' aria-current="page"' if href == current else ''
        lines.append(f'      <li><a href="/{href}"{current_attr}>{label}</a></li>')
    return "\n".join(lines)

def write_page(path, title, description, current, body):
    head = HEAD_TEMPLATE.format(
        title=title, description=description, path=path,
        logo=LOGO_SVG, navlinks=render_nav(current)
    )
    html = head + body + FOOT_TEMPLATE
    out_path = os.path.join(OUT_DIR, path)
    with open(out_path, "w") as f:
        f.write(html)
    print("wrote", out_path)

OUT_DIR = "/mnt/user-data/outputs"

# ==========================================================================
# HOME
# ==========================================================================
home_body = '''
<header class="hero" id="top">
  <div class="wrap">
    <div class="hero-inner">
      <span class="eyebrow"><span lang="sw">SULUHISHO LA TEKNOLOJIA, WAZI KWA WOTE</span></span>
      <h1>Fungua Systems</h1>
      <p class="subhead">Technology solutions, open to everyone.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/contact.html">Get in touch</a>
        <a class="btn btn-ghost" href="/about.html">About the studio</a>
      </div>
    </div>
  </div>
  <div class="aperture" aria-hidden="true">
    <span class="core"></span>
    <span class="blade" style="--rot:0deg; animation-delay:.02s"></span>
    <span class="blade" style="--rot:30deg; animation-delay:.06s"></span>
    <span class="blade" style="--rot:60deg; animation-delay:.10s"></span>
    <span class="blade" style="--rot:90deg; animation-delay:.14s"></span>
    <span class="blade" style="--rot:120deg; animation-delay:.18s"></span>
    <span class="blade" style="--rot:150deg; animation-delay:.22s"></span>
    <span class="blade" style="--rot:180deg; animation-delay:.26s"></span>
    <span class="blade" style="--rot:210deg; animation-delay:.30s"></span>
    <span class="blade" style="--rot:240deg; animation-delay:.34s"></span>
    <span class="blade" style="--rot:270deg; animation-delay:.38s"></span>
    <span class="blade" style="--rot:300deg; animation-delay:.42s"></span>
    <span class="blade" style="--rot:330deg; animation-delay:.46s"></span>
  </div>
</header>

<main id="main">
<section aria-label="Site sections">
  <div class="wrap">
    <div class="teasers">
      <a class="teaser" href="/about.html">
        <span class="eyebrow">ABOUT</span>
        <h3>One studio, no single lane.</h3>
        <p>What Fungua Systems is, what it works on, and who's behind it.</p>
        <span class="go">View \u2192</span>
      </a>
      <a class="teaser" href="/approach.html">
        <span class="eyebrow">APPROACH</span>
        <h3>How we work.</h3>
        <p>Problem first, platform second. Documented as we build.</p>
        <span class="go">View \u2192</span>
      </a>
      <a class="teaser" href="/labs.html">
        <span class="eyebrow">LABS</span>
        <h3>In the workshop.</h3>
        <p>What's currently being built, in progress and unfinished.</p>
        <span class="go">View \u2192</span>
      </a>
      <a class="teaser" href="/contact.html">
        <span class="eyebrow">CONTACT</span>
        <h3>Say hello.</h3>
        <p>Have a problem worth solving, or want to back one?</p>
        <span class="go">View \u2192</span>
      </a>
    </div>
  </div>
</section>
</main>
'''

# ==========================================================================
# ABOUT
# ==========================================================================
about_body = '''
<div class="page-header">
  <div class="wrap">
    <span class="eyebrow">ABOUT</span>
    <h1>One studio, no single lane.</h1>
  </div>
</div>
<main id="main">
<section>
  <div class="wrap">
    <p class="lede">Fungua Systems is a Nairobi-built technology studio. We take on real, specific problems \u2014 in data, infrastructure, or software \u2014 and build the smallest reliable system that solves them. No shelf-ware, no platform for its own sake.</p>

    <div class="pillars" style="margin-top:56px;">
      <div class="pillar">
        <svg class="mark" viewBox="0 0 24 24" fill="none"><path d="M4 19V10M12 19V5M20 19v-6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        <h3>Data &amp; Intelligence</h3>
        <p>Dashboards, pipelines, and predictive models that turn scattered records into decisions.</p>
      </div>
      <div class="pillar">
        <svg class="mark" viewBox="0 0 24 24" fill="none"><rect x="4" y="4" width="16" height="6" rx="1" stroke="currentColor" stroke-width="1.6"/><rect x="4" y="14" width="16" height="6" rx="1" stroke="currentColor" stroke-width="1.6"/></svg>
        <h3>Infrastructure &amp; Cloud</h3>
        <p>Networks, servers, and cloud environments built to stay up, not just stand up.</p>
      </div>
      <div class="pillar">
        <svg class="mark" viewBox="0 0 24 24" fill="none"><path d="M8 9l-4 3 4 3M16 9l4 3-4 3M13 6l-2 12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        <h3>Software &amp; Automation</h3>
        <p>Web apps, agents, and workflow tools shaped around how people actually work.</p>
      </div>
    </div>

    <div class="founder">
      <div class="founder-mark">JM</div>
      <div class="founder-body">
        <span class="eyebrow">FOUNDER</span>
        <p style="margin-top:12px;">Fungua Systems is founded and built by Jurgens Matika, a Nairobi-based computer scientist working across business intelligence, cloud infrastructure, and software development \u2014 four years across government, NGO, and private-sector systems, now consolidated into one studio.</p>
        <div class="founder-links">
          <a href="https://jurgens-matika.netlify.app/" target="_blank" rel="noopener">Full profile</a>
          <a href="https://www.linkedin.com/in/jurgens-matika-3b0b36183/" target="_blank" rel="noopener">LinkedIn</a>
          <a href="https://github.com/jurgens012/" target="_blank" rel="noopener">GitHub</a>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
'''

# ==========================================================================
# APPROACH
# ==========================================================================
approach_body = '''
<div class="page-header">
  <div class="wrap">
    <span class="eyebrow">APPROACH</span>
    <h1>How we work.</h1>
  </div>
</div>
<main id="main">
<section>
  <div class="wrap">
    <div class="approach-grid">
      <div>
        <p class="lede">Every build starts from the problem, not the tech. We prototype lean, document as we go, and hand over systems someone else could pick up without us in the room.</p>
      </div>
      <ul class="principles">
        <li><span class="glyph">\u2192</span> Problem first, platform second</li>
        <li><span class="glyph">\u2192</span> Documented as we build, not after</li>
        <li><span class="glyph">\u2192</span> Small systems that actually get used</li>
      </ul>
    </div>
  </div>
</section>
</main>
'''

# ==========================================================================
# LABS
# ==========================================================================
labs_body = '''
<div class="page-header">
  <div class="wrap">
    <span class="eyebrow">LABS</span>
    <h1>In the workshop.</h1>
  </div>
</div>
<main id="main">
<section>
  <div class="wrap">
    <div class="labs-panel">
      <span class="eyebrow">FIRST BUILD \u2014 IN PROGRESS</span>
      <h3>The first Fungua Systems case study is being built.</h3>
      <p>Full write-up, prototype, and results land here once it's ready. In the meantime, finished technical work is documented on the founder's portfolio.</p>
      <a href="https://jurgens-matika.netlify.app/" target="_blank" rel="noopener">See finished work on the founder's portfolio \u2192</a>
    </div>
  </div>
</section>
</main>
'''

# ==========================================================================
# CONTACT
# ==========================================================================
contact_body = '''
<div class="page-header">
  <div class="wrap">
    <span class="eyebrow">CONTACT</span>
    <h1>Say hello.</h1>
  </div>
</div>
<main id="main">
<section>
  <div class="wrap">
    <div class="contact-cta">
      <h2>Have a problem worth solving \u2014 or want to back one?</h2>
      <a class="btn btn-primary" href="mailto:funguasystems@gmail.com?subject=Fungua%20Systems%20Inquiry">Email Fungua Systems</a>
    </div>
    <p class="contact-note">This goes straight to a real inbox, checked by the founder \u2014 not a form that disappears into a queue. Once Fungua Systems has its own domain, mail to that domain will route here automatically through Cloudflare Email Routing.</p>
  </div>
</section>
</main>
'''

write_page("index.html", "Fungua Systems \u2014 Technology solutions, open to everyone.",
           "Fungua Systems is a Nairobi-built technology studio working across data, infrastructure, and software to solve real problems.",
           None, home_body)
write_page("about.html", "About \u2014 Fungua Systems",
           "Fungua Systems is a Nairobi-built technology studio working across data, infrastructure, and software. Founded by Jurgens Matika.",
           "about.html", about_body)
write_page("approach.html", "Approach \u2014 Fungua Systems",
           "How Fungua Systems works: problem first, platform second, documented as we build.",
           "approach.html", approach_body)
write_page("labs.html", "Labs \u2014 Fungua Systems",
           "Current and upcoming Fungua Systems project case studies.",
           "labs.html", labs_body)
write_page("contact.html", "Contact \u2014 Fungua Systems",
           "Get in touch with Fungua Systems.",
           "contact.html", contact_body)

# ==========================================================================
# 404
# ==========================================================================
notfound_body = '''
<div class="page-header">
  <div class="wrap">
    <span class="eyebrow">404</span>
    <h1>This page hasn't been opened yet.</h1>
  </div>
</div>
<main id="main">
<section>
  <div class="wrap">
    <p class="lede">Whatever you were looking for isn't here \u2014 maybe it moved, maybe it doesn't exist yet. Start again from the front door.</p>
    <div class="hero-actions" style="margin-top:32px;">
      <a class="btn btn-primary" href="/index.html">Back to home</a>
    </div>
  </div>
</section>
</main>
'''

write_page("404.html", "Page not found \u2014 Fungua Systems",
           "This page could not be found.",
           None, notfound_body)
