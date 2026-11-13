#!/usr/bin/env python3
import json, html as H
from pathlib import Path

ROOT = Path("/workspace/bim-reference")
BUILD = ROOT / "_build"
CANON = "https://bimchart.net"
CHECKED, CHECKED_ISO = "Nov 13, 2026", "2026-11-13"
NAV = [
    ("index.html", "Home"),
    ("modeling.html", "Modeling"),
    ("revit-addins.html", "Revit add-ins"),
    ("coordination.html", "Coordination"),
    ("spooling.html", "Spooling"),
    ("visualization.html", "Visualization"),
    ("updates.html", "Updates"),
]
HERO_SVG = (BUILD / "hero.svg").read_text()
COMMON_HOW = """
<li><strong>Popularity</strong> is a 1–5 judgment (halves allowed) of how commonly a product shows up in recent firm surveys, review directories, or marketplace ranks — relative to the other products on this page, not a computed formula.</li>
<li><strong>Captions</strong> name the source and a “checked Nov 2026” date. If there was no usable source, the caption says “Editorial estimate.”</li>
<li><strong>Learning curve</strong> is editorial (Gentler / Moderate / Steep) based on typical new-user experience, not a test score.</li>
<li><strong>Cost</strong> is a five-step scale (Free / $ / $$ / $$$ / $$$$) for a single commercial seat. See “How cost is rated.” Captions cite a source or say the rating is an estimate.</li>
"""

def e(s):
    return H.escape(s, quote=True)

def head(title, description, path):
    url = CANON + path
    typ = "website" if path == "/" else "article"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="{typ}">
<meta property="og:site_name" content="BIM Reference Library">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{CANON}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="BIM Reference Library: a dark blueprint grid and city skyline">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{CANON}/og-image.png">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&family=Rajdhani:wght@600;700&display=swap">
<link rel="stylesheet" href="theme.css">
</head>
"""

def nav(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{e(label)}</a></li>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<nav class="topnav" aria-label="Primary">
  <div class="inner">
    <a class="brand" href="index.html">
      <svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true">
        <rect x="1" y="1" width="26" height="26" fill="none" stroke="#3de8ff" stroke-width="1"/>
        <path d="M4 24 V12 H8 V24 M10 24 V8 H16 V24 M18 24 V14 H24 V24" fill="#3de8ff"/>
        <path d="M4 24 H24" stroke="#3de8ff" fill="none"/>
      </svg>
      BIM Reference Library
    </a>
    <ul class="nav-links">{''.join(items)}</ul>
  </div>
</nav>
"""

def footer(home=False):
    # Same wording and Ko-fi markup as ammo-reference (and date-calculator / tire-size-tool).
    updated = ""
    if home:
        updated = f'<p class="kofi updated">Last updated <time datetime="{CHECKED_ISO}">{CHECKED}</time> · <a href="updates.html">See what changed →</a></p>\n'
    return f"""<footer class="site-footer">
{updated}<p class="kofi">Free and ad-free. If this site helped you, <a href="https://ko-fi.com/marcustravis" target="_blank" rel="noopener">buy me a coffee →</a></p>
</footer>
"""

def hero(eyebrow, title, lede, checked=True):
    check = ""
    if checked:
        check = f'<p class="checked">Data last checked: <time datetime="{CHECKED_ISO}">{CHECKED}</time> · <a href="updates.html">What changed</a></p>'
    return f"""<header class="hero">
  <div class="hero-art">{HERO_SVG}</div>
  <div class="hero-copy">
    <span class="eyebrow">{e(eyebrow)}</span>
    <h1>{e(title)}</h1>
    <p class="lede">{lede}</p>
    {check}
  </div>
</header>
"""

def chips(data):
    seen, tags = set(), []
    for d in data:
        for t in d["tags"]:
            if t not in seen:
                seen.add(t); tags.append(t)
    out = ['<button class="chip" data-f="all" aria-pressed="true">All</button>']
    for t in tags:
        out.append(f'<button class="chip" data-f="{e(t)}" aria-pressed="false">{e(t)}</button>')
    return "\n".join(out)

def wrap(inner):
    return f'<div class="page-bg"></div>\n{inner}'

def write_catalog(sec):
    data = json.loads((BUILD / sec["json"]).read_text())
    payload = [{k: d[k] for k in ("name","maker","knownFor","tags","price","pop","popCaption","cost","costCaption","learn","pro","con","url","icon","iconOfficial")} for d in data]
    html = head(sec["title"] + " · BIM Reference Library", sec["description"], "/" + sec["slug"])
    html += "<body>\n" + wrap(nav(sec["file"]))
    html += '<div class="wrap chart-wrap" id="main">\n'
    html += hero("Independent BIM software guide", sec["title"], sec["lede"])
    html += f"""  <div id="catalog">
  <div class="toolbar">
    <div class="chips" role="group" aria-label="Filter">{chips(data)}</div>
    <label class="search">Search
      <input type="search" id="search" placeholder="Name, maker, or tag" autocomplete="off">
    </label>
    <label class="sort">Sort
      <select id="sort">
        <option value="pop">Popularity</option>
        <option value="name">Name</option>
        <option value="cost-asc">Cost: cheapest first</option>
        <option value="cost-desc">Cost: priciest first</option>
      </select>
    </label>
  </div>
  <p class="count" id="count"></p>
  <div class="table-box">
    <table class="chart">
      <thead>
        <tr>
          <th><button type="button" class="th-btn" data-k="name">Software</button></th>
          <th>Known for</th>
          <th><button type="button" class="th-btn" data-k="pop">Popularity</button></th>
          <th><button type="button" class="th-btn" data-k="cost">Cost</button></th>
          <th>Learning curve</th>
          <th>Pros &amp; cons</th>
          <th>Official site</th>
        </tr>
      </thead>
      <tbody id="rows"></tbody>
    </table>
  </div>
  </div>
  <div class="notes">
    <section>
      <h2>How the ratings work</h2>
      <ul>{COMMON_HOW}<li>{e(sec["relative"])}</li></ul>
    </section>
    <section>
      <h2>How cost is rated</h2>
      <ul>
        <li>Cost uses a published annual price for one commercial seat when we could find one this session: the cheapest official annual rate, or monthly × 12 if only monthly is listed. Perpetual licenses are rated on the first-year purchase price.</li>
        <li><strong>Free</strong> — no license fee for the core product (open source or free commercial use).</li>
        <li><strong>$</strong> — under about $500 / year.</li>
        <li><strong>$$</strong> — about $500–2,000 / year.</li>
        <li><strong>$$$</strong> — about $2,000–5,000 / year.</li>
        <li><strong>$$$$</strong> — about $5,000+ / year, or quote-only enterprise pricing with no public list price.</li>
        <li>If the vendor only quotes, or no public figure turned up, the caption says so and the band is an editorial estimate — never an invented dollar amount. Always confirm current pricing with the vendor.</li>
      </ul>
    </section>
    <section>
      <h2>Sources and limits</h2>
      <p>{e(sec["limits"])}</p>
    </section>
    <section>
      <h2>Independence</h2>
      <p>This site is ad-free and has no affiliate links. Official-site buttons go straight to the vendor. Stars are not paid placement.</p>
    </section>
    <section>
      <h2>About the icons</h2>
      <p>The first column is meant to look like the software’s desktop shortcut. Official vendor or App Store app icons are used when we could find one this session. If not, the tile is a generated initials icon in the same rounded-square style.</p>
    </section>
  </div>
</div>
{footer()}
<script src="app.js"></script>
<script src="scroll-hint.js"></script>
<script>
const DATA = {json.dumps(payload, ensure_ascii=False)};
initCatalog(DATA, {{ noun: {json.dumps(sec["noun"])}, defaultSort: "pop" }});
</script>
</body>
</html>
"""
    (ROOT / sec["file"]).write_text(html)
    sourced = sum(1 for d in data if d["sourced"])
    editorial = len(data) - sourced
    print(f"wrote {sec['file']}: {len(data)} products, sourced={sourced}, editorial={editorial}")
    return len(data), sourced, editorial

def write_home(counts):
    cards = [
        ("modeling.html", f"{counts['modeling'][0]} tools", "Modeling", "Revit, SketchUp, Archicad, Tekla, AutoCAD, Rhino, and other authoring platforms."),
        ("revit-addins.html", f"{counts['revit-addins'][0]} add-ins", "Revit add-ins", "pyRevit, DiRoots, Ideate, CTC, content managers, and other daily Revit tools."),
        ("coordination.html", f"{counts['coordination'][0]} tools", "Coordination &amp; clash", "Navisworks, BIM Collaborate, Revizto, Solibri, and issue-tracking tools."),
        ("spooling.html", f"{counts['spooling'][0]} tools", "Spooling &amp; fabrication", "SysQue, Fabrication, EVOLVE, MSUITE, Stratus, and steel shop platforms."),
        ("visualization.html", f"{counts['visualization'][0]} tools", "Visualization", "Enscape, Twinmotion, Lumion, D5, V-Ray, and related renderers."),
    ]
    grid = "".join(
        f'<a class="card" href="{href}"><span class="cnt">{cnt}</span><span class="nm">{name}</span><span class="ds">{ds}</span><span class="go">Open guide →</span></a>'
        for href, cnt, name, ds in cards
    )
    html = head(
        "BIM Reference Library",
        "Free, ad-free guide to BIM software: modeling tools, Revit add-ins, coordination, spooling, and visualization, with cited popularity ratings.",
        "/",
    )
    html += "<body>\n" + wrap(nav("index.html"))
    html += '<div class="wrap chart-wrap" id="main">\n'
    html += hero("Independent BIM software guide", "BIM Reference Library",
                 "A free, ad-free field guide to the software people actually use to design, coordinate, fabricate, and visualize buildings. Popularity is cited, not invented.")
    html += f"""  <section class="grp">
    <h2>Start here</h2>
    <div class="grid">{grid}</div>
  </section>
  <div class="notes">
    <section>
      <h2>How to use this site</h2>
      <p>Each section opens as a compact, scrollable comparison chart — one row per product — that you can filter, search, and sort. Stars are a 1–5 popularity judgment with a source caption. Cost uses a Free / $ / $$ / $$$ / $$$$ scale with a source caption. Learning-curve labels are editorial. Official-site links are not affiliate links.</p>
    </section>
    <section>
      <h2>Where the numbers come from</h2>
      <p>The main firm-adoption source is the Confluence 2025 AEC Tech Stack Survey (Q4 2025). European figures for Archicad and ALLPLAN come from the European Architectural Barometer Q4 2025. Review counts come from G2, checked in November 2026. If a product has no usable source, the caption says “Editorial estimate.”</p>
    </section>
    <section>
      <h2>What this is not</h2>
      <p>This is not a vendor ranking you should buy from blindly. It is a starting map for people learning the BIM software landscape.</p>
    </section>
  </div>
</div>
{footer(home=True)}
</body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    print("wrote index.html")

def write_updates():
    html = head("Updates · BIM Reference Library", "What changed on the BIM Reference Library, in plain English.", "/updates")
    html += "<body>\n" + wrap(nav("updates.html"))
    html += '<div class="wrap chart-wrap" id="main">\n'
    html += hero("Changelog", "Updates", "A short, plain-English record of what changed on this site.", checked=False)
    html += f"""  <article>
    <div class="log">
      <h3>Site launch</h3>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>The first public version of the BIM Reference Library went live, with five guides — Modeling, Revit add-ins, Coordination &amp; clash, Spooling &amp; fabrication, and Visualization — plus this updates page. Popularity captions were researched in November 2026. See CHANGELOG.md in the repository for sources.</p>
    </div>
    <div class="log">
      <h3>Product cards render fix</h3>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Fixed a JavaScript typo that left section pages without their product cards after the first deploy. Hover glow now also applies to those cards, not only the homepage section tiles.</p>
    </div>
    <div class="log">
      <h3>Custom domain and Git auto-deploy</h3>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>The site now lives at <a href="https://bimchart.net">bimchart.net</a>. The pages.dev address still works; search engines are pointed at the .net copy. Pushing to the GitHub <code>main</code> branch now publishes automatically.</p>
    </div>
    <div class="log">
      <h3>Auto-deploy on push confirmed</h3>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>The Cloudflare Workers and Pages GitHub App now has access to this repository, so a push to <code>main</code> publishes the site without a manual deploy.</p>
    </div>
    <div class="log">
      <h3>Ko-fi footer</h3>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Every page now has the same Ko-fi support line used on ammochart.net.</p>
    </div>
    <div class="log">
      <h3>Footer matches other sites</h3>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>The page footer is now only the shared Ko-fi line used on ammochart.net and Marcus's other sites. The homepage also has the "Last updated / See what changed" line, like ammochart's home page.</p>
    </div>
    <div class="log">
      <h3>Cost ratings on every card</h3>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Each product card now has a Cost row on a Free / $ / $$ / $$$ / $$$$ scale, with a caption citing a published price or marking the band as an estimate. You can sort each guide cheapest-first or priciest-first.</p>
    </div>
    <div class="log">
      <h3>Comparison charts, not more cards</h3>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Section pages are now compact, horizontally scrollable comparison charts in the same style as the ammo reference charts: sticky headers, filter chips, click-to-sort columns, and a small visual in the first column. That visual is the product’s desktop or app icon when we could find an official one, or a generated initials tile if we could not.</p>
    </div>
  </article>
</div>
{footer()}
</body>
</html>
"""
    (ROOT / "updates.html").write_text(html)
    print("wrote updates.html")

def write_404():
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Page not found · BIM Reference Library</title>
<meta name="robots" content="noindex">
<link rel="icon" href="{CANON}/favicon.ico" sizes="any">
<link rel="icon" href="{CANON}/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{CANON}/apple-touch-icon.png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&amp;family=Rajdhani:wght@600;700&amp;display=swap">
<link rel="stylesheet" href="{CANON}/theme.css">
<script>
(function(){{var p=location.pathname;if(p.length>1&&p.charAt(p.length-1)==="/")location.replace(p.slice(0,-1)+location.search+location.hash);}})();
</script>
</head>
<body>
<div class="page-bg"></div>
<div class="wrap" id="main">
  <span class="eyebrow">Error 404</span>
  <h1>Page not found</h1>
  <p class="lede">That page is not here. It may have moved, or the link has a typo. Try one of these instead.</p>
  <div class="grid">
    <a class="card" href="{CANON}/"><span class="nm">All guides</span><span class="go">Home →</span></a>
    <a class="card" href="{CANON}/modeling"><span class="nm">Modeling</span><span class="go">Open →</span></a>
    <a class="card" href="{CANON}/revit-addins"><span class="nm">Revit add-ins</span><span class="go">Open →</span></a>
    <a class="card" href="{CANON}/coordination"><span class="nm">Coordination</span><span class="go">Open →</span></a>
    <a class="card" href="{CANON}/spooling"><span class="nm">Spooling</span><span class="go">Open →</span></a>
    <a class="card" href="{CANON}/visualization"><span class="nm">Visualization</span><span class="go">Open →</span></a>
  </div>
</div>
{footer()}
</body>
</html>
"""
    (ROOT / "404.html").write_text(html)
    print("wrote 404.html")

def write_meta(stats):
    pages = ["/", "/modeling", "/revit-addins", "/coordination", "/spooling", "/visualization", "/updates"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        sm.append(f"  <url><loc>{CANON}{p}</loc></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {CANON}/sitemap.xml\n")
    (ROOT / "_headers").write_text(
        f"# Tell search engines that bimchart.net is the main address.\n"
        f"# bimchart.pages.dev keeps working; it just points Google to the .net copy.\n"
        f"/*\n  Link: <{CANON}/:splat>; rel=\"canonical\"\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n"
    )
    (ROOT / "README.md").write_text(f"""# BIM Reference Library

**Live site:** [{CANON}]({CANON})

A free, ad-free field guide to BIM software — modeling tools, Revit add-ins, coordination and clash detection, spooling and fabrication, and visualization. Built as a plain static site (HTML, CSS, and JavaScript, no build step).

There are no ads and no affiliate links. Official-site links go to the vendor.

Many ratings are relative judgments with cited sources. Check the vendor and your own office standards before you buy or standardize on a tool.

## Local preview

Open `index.html` in a browser, or serve the folder with any static file server.

## Data

Comparison-chart rows are driven by a `DATA` array on each section page. After changing facts, also update `CHANGELOG.md` and add a short note on `updates.html`.

Visitor stats (optional): Cloudflare Web Analytics, from the Pages project Metrics page.

## Sources

The November 2026 research notes and source list live in `CHANGELOG.md`.
""")
    (ROOT / "CHANGELOG.md").write_text(f"""# Changelog

All notable changes to the BIM Reference Library, with sources.

## {CHECKED} — Initial public release

Published the first version of the site: homepage plus five section guides (Modeling, Revit add-ins, Coordination & clash, Spooling & fabrication, Visualization), an Updates page, sitemap, robots.txt, and a 404 page.

Popularity scores are 1–5 judgments (halves allowed), relative to other products on the same page. Each card caption cites a source and a checked date. Captions that say “Editorial estimate” had no usable quantitative source in this research pass. Review counts and firm-penetration figures were not invented.

### Sources used in November 2026

- Confluence 2025 AEC Tech Stack Survey (Q4 2025), published by AVAIL / Confluence: [PDF](https://3222494.fs1.hubspotusercontent-na1.net/hubfs/3222494/Tech%20Stack%20Survey/2025/Confluence%202025%20Tech%20Stack%20Survey%20Report.pdf). Design-firm sample. Used for firm penetration (e.g. Revit 94.7%, AutoCAD 85.8%, SketchUp 73.5%, Rhino 49.6%, Navisworks 71%, Autodesk Construction Cloud 94%, Enscape for Revit 80.5%) and for the alphabetical inventory of firms indicating use (pyRevit 90, DiRoots Tools 63, Ideate and CTC suites, Revizto 46, Advance Steel 16, and others cited on cards).
- European Architectural Barometer, Q4 2025, as summarized by USP Research, for Archicad and Allplan usage among BIM-user firms in selected European countries: [overview](https://www.usp-research.com/insights/blogs/market-overview-of-bim-and-cad-software-usage-of-european-architects/).
- G2 product and category pages checked November 2026, including Revit (1,256 reviews, 4.6/5), SketchUp (1,328, 4.5/5), AutoCAD (~1,800–2,012, 4.4/5), Archicad (291–298, 4.6/5), Vectorworks Architect (216–264, 4.4/5), Tekla Structures (63, 4.5/5), ALLPLAN (25, 4.4/5), BricsCAD (135, 4.5/5), OpenBuildings Designer (16, 4.3/5), Navisworks (~193–208, 4.6/5), Enscape (456, 4.6/5). A G2 “Autodesk Forma” listing with thousands of reviews appears to mix Autodesk Construction Cloud history and was **not** used.
- Autodesk App Store recaps: Bird Tools write-up of APS-powered Revit add-in download ranks as of 7 February 2025; NTCLSoft “most downloaded apps” recap (Lumion LiveSync); mid-2024 5-star add-in recap for historical COINS Auto-Section Box (130 reviews) and DiRootsOne (54 reviews).
- Autodesk Community threads (2025–2026) reporting that COINS Auto-Section Box was later taken down from the Autodesk App Store.
- Official vendor sites for product URLs, plus Autodesk Revit’s public starting price of $251 / month (autodesk.com/products/revit/overview, checked November 2026).
- G2 / Capterra review totals for EVOLVE, MSUITE, and SysQue (1–2 reviews) were recorded only to explain why they were *not* used as a ranking basis.

### Product counts at launch

- Modeling: {stats['modeling'][0]} (sourced {stats['modeling'][1]}, editorial {stats['modeling'][2]})
- Revit add-ins: {stats['revit-addins'][0]} (sourced {stats['revit-addins'][1]}, editorial {stats['revit-addins'][2]})
- Coordination & clash: {stats['coordination'][0]} (sourced {stats['coordination'][1]}, editorial {stats['coordination'][2]})
- Spooling & fabrication: {stats['spooling'][0]} (sourced {stats['spooling'][1]}, editorial {stats['spooling'][2]})
- Visualization: {stats['visualization'][0]} (sourced {stats['visualization'][1]}, editorial {stats['visualization'][2]})

## {CHECKED} — Product cards render fix

Fixed a JavaScript typo (`initCatalog` required a `#catalog` element that the pages did not include), which left section pages without product cards after the first deploy. Hover glow now also applies to product cards, not only homepage section tiles.

## {CHECKED} — Custom domain and Git auto-deploy

The canonical site address is now [https://bimchart.net](https://bimchart.net). `bimchart.pages.dev` remains available and points search engines at the .net copy via canonical tags and `_headers`. Automatic production deploys on push to `main` were enabled by reconnecting the GitHub source on the Cloudflare Pages project.

## {CHECKED} — Auto-deploy on push confirmed

Production deploys now start automatically when commits are pushed to `main`, after the Cloudflare Workers and Pages GitHub App was granted access to this repository.

## {CHECKED} — Ko-fi footer

Added the same Ko-fi support line used on ammochart.net to every page footer.

## {CHECKED} — Footer matches other sites

The page footer is now only the shared Ko-fi line used on ammochart.net and Marcus's other sites. The homepage also has the "Last updated / See what changed" line, like ammochart's home page.

## {CHECKED} — Cost ratings

Added a Cost row (Free / $ / $$ / $$$ / $$$$) to every product card, researched in November 2026 from vendor pricing pages and official shops. Bands: Free (no license fee); $ under about $500/year; $$ about $500–2,000/year; $$$ about $2,000–5,000/year; $$$$ about $5,000+/year or quote-only enterprise with no public list price. Captions cite the source or say the rating is an estimate. No prices were invented. Sort options now include cheapest first and priciest first.

Official figures used include Autodesk list prices for Revit ($3,005/year), AutoCAD ($2,095/year), Navisworks Manage ($2,835/year), 3ds Max ($2,010/year), and Forma Site Design ($700/year); Graphisoft Archicad Studio ($2,414/year); Vectorworks Architect ($1,530/year); ALLPLAN Concept ($2,892/year); SketchUp Pro ($399/year); the RhinoARQ bundle ($1,695 perpetual); Chaos Enscape Solo ($574.80/year), V-Ray Solo ($540/year), and Veras Pro ($348/year); Twinmotion ($445/year over the $1M revenue threshold); Lumion Pro ($1,149/year); AVAIL ($250/year); DiRootsOne Premium ($120/year US / €100); IdeateApps ($495/year); CTC BIM Project Suite ($410); Bird Tools individual apps ($10–$49.50/year); Victaulic Tools for Revit ($200/license); Solibri Essential (€1,428/year); and BIMcollab Zoom Single (about €720/year). Many fabrication, coordination, and specialist tools remain quote-only.

## {CHECKED} — Comparison charts

Replaced the product-card grids on all five section pages with a compact, horizontally scrollable comparison chart in the same layout as the ammo reference charts (filter chips, count, sticky sortable headers, first-column visual, and a mobile scroll hint). The first column shows a 128 px desktop/app icon for each product, stored in /icons and not hotlinked. Official vendor or App Store icons were used when they could be found; the rest are generated initials tiles in the same rounded-square style. Popularity, cost, captions, filters, and cheapest/priciest sort options are unchanged.
""")
    print("wrote sitemap, robots, _headers, README, CHANGELOG")

def main():
    sections = json.loads((BUILD / "sections.json").read_text())
    stats = {}
    for sec in sections:
        stats[sec["slug"]] = write_catalog(sec)
    write_home(stats)
    write_updates()
    write_404()
    write_meta(stats)
    print("DONE", stats)

if __name__ == "__main__":
    main()
