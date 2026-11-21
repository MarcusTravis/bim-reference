#!/usr/bin/env python3
import json, html as H, subprocess, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
import sys as _sys; _sys.path.insert(0, str(BUILD))
from seo_content import SEO
CANON = "https://bimchart.net"
CHECKED, CHECKED_ISO = "Nov 13, 2026", "2026-11-13"   # when product data was last researched
NOV14, NOV14_ISO = "Nov 14, 2026", "2026-11-14"     # date of the Nov 14 search/nav release (historical log entries)
UPDATED, UPDATED_ISO = "Nov 20, 2026", "2026-11-20"   # when the site itself last changed
ASSET_V = "20261120a"  # bump to bust browser caches for theme.css / *.js
import re as _re
def row_id(name):
    return "p-" + _re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
NAV = [
    ("index.html", "Home"),
    ("modeling.html", "Modeling"),
    ("revit-addins.html", "Revit add-ins"),
    ("coordination.html", "Coordination"),
    ("spooling.html", "Spooling"),
    ("visualization.html", "Visualization"),
    ("scanning.html", "Scanning"),
    ("drones.html", "Drones"),
    ("updates.html", "Updates"),
]
def url_for(f, prefix=""):
    """Clean URL that Cloudflare Pages serves for a file (modeling.html -> /modeling)."""
    path = "/" if f in ("index.html", "") else "/" + f[:-5]
    return (prefix.rstrip("/") + path) if prefix else path

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"

WEBSITE_ID = CANON + "/#website"
WEBSITE = {"@type": "WebSite", "@id": WEBSITE_ID, "url": CANON + "/", "name": "BIM Reference Library",
           "alternateName": "bimchart.net", "inLanguage": "en",
           "description": "Free, ad-free comparison charts for BIM software and reality-capture hardware."}

def breadcrumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": CANON + u} for i, (n, u) in enumerate(items)]}

def faq_ld(faq, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def intro_block(q, text):
    return f"""  <section class="intro" aria-labelledby="intro-h">
    <h2 id="intro-h">{e(q)}</h2>
    <p>{e(text)}</p>
  </section>
"""

def faq_block(faq):
    items = "".join(f'\n    <div class="faq-item">\n      <h3>{e(q)}</h3>\n      <p>{e(a)}</p>\n    </div>' for q, a in faq)
    return f"""  <section class="faq" id="faq" aria-labelledby="faq-h">
    <h2 id="faq-h">Frequently asked questions</h2>{items}
  </section>
"""

HERO_SVG = (BUILD / "hero.svg").read_text()
COMMON_HOW = """
<li><strong>Popularity</strong> is a 1–5 judgment (halves allowed) of how commonly a product shows up in recent firm surveys, review directories, or marketplace ranks — relative to the other products on this page, not a computed formula.</li>
<li><strong>Captions</strong> name the source and a “checked Nov 2026” date. If there was no usable source, the caption says “Editorial estimate.”</li>
<li><strong>Learning curve</strong> is editorial (Gentler / Moderate / Steep) based on typical new-user experience, not a test score.</li>
<li><strong>Cost</strong> is a five-step scale (Free / $ / $$ / $$$ / $$$$). See “How cost is rated” for the band definitions on this page. Captions cite a source or say the rating is an estimate.</li>
"""

FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;500;600;700&amp;family=Rajdhani:wght@600;700&amp;display=swap"

def e(s):
    return H.escape(s, quote=True)

def head(title, description, path, ld=None):
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
<meta name="twitter:image:alt" content="BIM Reference Library: a dark blueprint grid and city skyline">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#05080c">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="/theme.css?v={ASSET_V}">
<script src="/nav.js?v={ASSET_V}" defer></script>
{jsonld({"@context": "https://schema.org", "@graph": ld}) if ld else ""}</head>
"""

def nav(current, prefix=""):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{url_for(href, prefix)}"{cur}>{e(label)}</a></li>')
    brand = url_for("index.html", prefix)
    return f"""<a class="skip" href="#main">Skip to content</a>
<nav class="topnav" aria-label="Primary">
  <div class="inner">
    <a class="brand" href="{brand}">
      <svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true">
        <rect x="1" y="1" width="26" height="26" fill="none" stroke="#3de8ff" stroke-width="1"/>
        <path d="M4 24 V12 H8 V24 M10 24 V8 H16 V24 M18 24 V14 H24 V24" fill="#3de8ff"/>
        <path d="M4 24 H24" stroke="#3de8ff" fill="none"/>
      </svg>
      BIM Reference Library
    </a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">
      <span class="nav-toggle-bars" aria-hidden="true"></span>
    </button>
    <ul id="primary-nav" class="nav-links">{''.join(items)}</ul>
  </div>
</nav>
"""

def footer(home=False):
    # Same wording and Ko-fi markup as ammo-reference (and date-calculator / tire-size-tool).
    updated = ""
    if home:
        updated = f'<p class="kofi updated">Last updated <time datetime="{UPDATED_ISO}">{UPDATED}</time> · <a href="/updates">See what changed →</a></p>\n'
    return f"""<footer class="site-footer">
{updated}<p class="kofi">Free and ad-free. If this site helped you, <a href="https://ko-fi.com/marcustravis" target="_blank" rel="noopener">buy me a coffee →</a></p>
</footer>
"""

def hero(eyebrow, title, lede, checked=True):
    check = ""
    if checked:
        check = f'<p class="checked">Data last checked: <time datetime="{CHECKED_ISO}">{CHECKED}</time> · <a href="/updates">What changed</a></p>'
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

def _stars(n):
    full = int(n); half = (n - full) >= 0.5; empty = 5 - full - (1 if half else 0)
    return (f'<span class="starline" aria-label="{n:g} out of 5"><span class="stars">' + "★" * full + ("½" if half else "")
            + '</span><span class="stars off">' + "★" * empty + "</span></span>")

def _dollars(n):
    n = max(0, min(4, int(n or 0)))
    if n == 0:
        return '<span class="costline" aria-label="Free">Free</span>'
    return f'<span class="costline" aria-label="{n} of 4"><span class="cost-on">' + "$" * n + '</span><span class="cost-off">' + "$" * (4 - n) + "</span></span>"

def render_row(d, extra_keys):
    """Server-side copy of app.js row(), so the chart is in the HTML before JavaScript runs."""
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in d.get("tags", []))
    icon = (f'<img class="app-icon" src="/icons/{e(d["icon"])}.png" width="52" height="52" alt="" loading="lazy" decoding="async">'
            if d.get("icon") else "")
    site = f'<a class="official" href="{e(d["url"])}" rel="noopener noreferrer">Official site →</a>' if d.get("url") else ""
    extras = "".join(f'<td class="hw">{e(d.get(k, ""))}</td>' for k in extra_keys)
    return (f'<tr id="{e(d["id"])}"><td class="prod-cell"><div class="prod">{icon}<div><span class="cart">{e(d["name"])}</span>'
            f'<span class="year">{e(d["maker"])}</span></div></div></td>'
            f'<td class="purpose">{e(d["knownFor"])}<div class="tags">{tags}</div></td>{extras}'
            f'<td>{_stars(d["pop"])}<span class="sub">{e(d["popCaption"])}</span></td>'
            f'<td>{_dollars(d.get("cost"))}<span class="sub">{e(d.get("costCaption", ""))}</span></td>'
            f'<td>{e(d.get("learn") or "")}</td>'
            f'<td class="purpose"><div class="pc"><span class="pro">+ {e(d["pro"])}</span><span class="con">− {e(d["con"])}</span></div></td>'
            f'<td>{site}</td></tr>')

def write_catalog(sec):
    data = json.loads((BUILD / sec["json"]).read_text())
    base_keys = ("name","maker","knownFor","tags","price","pop","popCaption","cost","costCaption","learn","pro","con","url","icon","iconOfficial")
    extra_cols = sec.get("extraCols") or []
    extra_keys = [c["key"] for c in extra_cols]
    payload = [dict(id=row_id(d["name"]), **{k: d[k] for k in list(base_keys) + extra_keys if k in d}) for d in data]
    first_col = sec.get("firstCol", "Software")
    table_class = "chart chart-wide" if extra_cols else "chart"
    extra_ths = "".join(f'\n          <th>{e(c["label"])}</th>' for c in extra_cols)
    colspan = 7 + len(extra_cols)
    extras_js = json.dumps(extra_keys)
    if sec.get("kind") == "hardware":
        cost_how = """        <li>Cost on this page is a purchase-price band for one unit, or a clearly described kit, not an annual software seat. Always confirm current pricing with the vendor.</li>
        <li><strong>$</strong> — under about $15,000.</li>
        <li><strong>$$</strong> — about $15,000–40,000.</li>
        <li><strong>$$$</strong> — about $40,000–80,000.</li>
        <li><strong>$$$$</strong> — about $80,000+, or quote-only with no public list price found this session.</li>
        <li>Captions cite an official shop, an authorized reseller listing, or say the band is an estimate. No dollar amounts were invented.</li>"""
        visual_how = "The first column is a product photo from the vendor, stored locally and fitted to the same 128 px rounded tile used on the software charts. If no official photo could be fetched this session, the tile is a generated illustration in the same style."
        visual_title = "About the photos"
    else:
        cost_how = """        <li>Cost uses a published annual price for one commercial seat when we could find one this session: the cheapest official annual rate, or monthly × 12 if only monthly is listed. Perpetual licenses are rated on the first-year purchase price.</li>
        <li><strong>Free</strong> — no license fee for the core product (open source or free commercial use).</li>
        <li><strong>$</strong> — under about $500 / year.</li>
        <li><strong>$$</strong> — about $500–2,000 / year.</li>
        <li><strong>$$$</strong> — about $2,000–5,000 / year.</li>
        <li><strong>$$$$</strong> — about $5,000+ / year, or quote-only enterprise pricing with no public list price.</li>
        <li>If the vendor only quotes, or no public figure turned up, the caption says so and the band is an editorial estimate — never an invented dollar amount. Always confirm current pricing with the vendor.</li>"""
        visual_how = "The first column is meant to look like the software’s desktop shortcut. Official vendor or App Store app icons are used when we could find one this session. If not, the tile is a generated initials icon in the same rounded-square style."
        visual_title = "About the icons"
    seo = SEO[sec["slug"]]
    url = CANON + "/" + sec["slug"]
    ordered = sorted(payload, key=lambda d: (-(d.get("pop") or 0), d["name"].lower()))
    rows_html = "".join(render_row(d, extra_keys) for d in ordered)
    cols = [first_col, "Known for"] + [c["label"] for c in extra_cols] + ["Popularity (1–5)", "Cost (Free to $$$$)", "Learning curve (editorial rating)", "Pros and cons", "Official site"]
    ld = [
        {**WEBSITE},
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": seo["title"], "description": seo["description"],
         "isPartOf": {"@id": WEBSITE_ID}, "inLanguage": "en", "dateModified": UPDATED_ISO,
         "breadcrumb": {"@id": url + "#breadcrumb"}, "mainEntity": {"@id": url + "#chart"}},
        {**breadcrumbs([("Home", "/"), (sec["title"], "/" + sec["slug"])]), "@id": url + "#breadcrumb"},
        {"@type": "ItemList", "@id": url + "#chart", "name": sec["title"] + " comparison chart", "numberOfItems": len(ordered),
         "itemListOrder": "https://schema.org/ItemListOrderDescending",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": d["name"], "url": f'{url}#{d["id"]}'} for i, d in enumerate(ordered)]},
        {"@type": "Dataset", "@id": url + "#dataset", "name": sec["title"] + " comparison data (BIM Reference Library)",
         "description": f'{sec["description"]} One row per product ({len(ordered)} {sec["noun"]}) with maker, what it is known for, popularity with a source caption, a cost band with a source caption, an editorial learning-curve rating, and pros and cons.',
         "url": url, "isAccessibleForFree": True, "dateModified": CHECKED_ISO, "inLanguage": "en",
         "creator": {"@type": "Organization", "name": "BIM Reference Library", "url": CANON + "/"},
         "variableMeasured": cols, "includedInDataCatalog": {"@type": "DataCatalog", "name": "BIM Reference Library", "url": CANON + "/"}},
        faq_ld(seo["faq"], url),
    ]
    html = head(seo["title"], seo["description"], "/" + sec["slug"], ld)
    html += "<body>\n" + wrap(nav(sec["file"]))
    html += '<div class="wrap chart-wrap" id="main">\n'
    html += hero("Independent BIM software guide", sec["title"], sec["lede"])
    html += intro_block(seo["intro_q"], seo["intro"])
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
  <p class="count" id="count">Showing {len(ordered)} of {len(ordered)} {e(sec["noun"])}</p>
  <div class="table-box">
    <table class="{table_class}">
      <thead>
        <tr>
          <th><button type="button" class="th-btn" data-k="name">{e(first_col)}</button></th>
          <th>Known for</th>{extra_ths}
          <th><button type="button" class="th-btn" data-k="pop">Popularity</button></th>
          <th><button type="button" class="th-btn" data-k="cost">Cost</button></th>
          <th class="learn-th">Learning curve<span class="th-note">editorial rating</span></th>
          <th>Pros &amp; cons</th>
          <th>Official site</th>
        </tr>
      </thead>
      <tbody id="rows">{rows_html}</tbody>
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
{cost_how}
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
      <h2>{e(visual_title)}</h2>
      <p>{e(visual_how)}</p>
    </section>
  </div>
{faq_block(seo["faq"])}  <nav class="related" aria-label="Other guides"><h2>Other guides</h2><ul>{"".join(f'<li><a href="{url_for(f)}">{e(l)}</a></li>' for f, l in NAV if f not in ("index.html", "updates.html", sec["file"]))}</ul></nav>
</div>
{footer()}
<script src="/app.js?v={ASSET_V}"></script>
<script src="/scroll-hint.js?v={ASSET_V}"></script>
<script>
const DATA = {json.dumps(payload, ensure_ascii=False)};
initCatalog(DATA, {{ noun: {json.dumps(sec["noun"])}, defaultSort: "pop", extraCols: {extras_js} }});
</script>
</body>
</html>
"""
    (ROOT / sec["file"]).write_text(html)
    sourced = sum(1 for d in data if d["sourced"])
    editorial = len(data) - sourced
    cost_s = sum(1 for d in data if d.get("costSourced"))
    official = sum(1 for d in data if d.get("iconOfficial"))
    print(f"wrote {sec['file']}: {len(data)} products, pop sourced={sourced}, editorial={editorial}, cost sourced={cost_s}, official visuals={official}")
    return len(data), sourced, editorial, cost_s, official

SECTION_LABELS = {
    "modeling": "Modeling", "revit-addins": "Revit add-ins", "coordination": "Coordination & clash",
    "spooling": "Spooling & fabrication", "visualization": "Visualization",
    "scanning": "Scanning hardware", "drones": "Drones",
}

def search_index(sections):
    idx = []
    for sec in sections:
        for d in json.loads((BUILD / sec["json"]).read_text()):
            idx.append({
                "name": d["name"], "maker": d["maker"], "tags": d["tags"], "icon": d.get("icon"),
                "section": SECTION_LABELS[sec["slug"]],
                "href": f'{url_for(sec["file"])}#{row_id(d["name"])}',
            })
    return idx

def write_home(counts, sections):
    index = search_index(sections)
    index_js = json.dumps(index, ensure_ascii=False).replace("</", "<\\/")
    cards = [
        ("modeling.html", f"{counts['modeling'][0]} tools", "Modeling", "Revit, SketchUp, Archicad, Tekla, AutoCAD, Rhino, and other authoring platforms."),
        ("revit-addins.html", f"{counts['revit-addins'][0]} add-ins", "Revit add-ins", "pyRevit, DiRoots, Ideate, CTC, content managers, and other daily Revit tools."),
        ("coordination.html", f"{counts['coordination'][0]} tools", "Coordination &amp; clash", "Navisworks, BIM Collaborate, Revizto, Solibri, and issue-tracking tools."),
        ("spooling.html", f"{counts['spooling'][0]} tools", "Spooling &amp; fabrication", "SysQue, Fabrication, EVOLVE, MSUITE, Stratus, and steel shop platforms."),
        ("visualization.html", f"{counts['visualization'][0]} tools", "Visualization", "Enscape, Twinmotion, Lumion, D5, V-Ray, and related renderers."),
        ("scanning.html", f"{counts['scanning'][0]} scanners", "Scanning hardware", "Leica, FARO, Trimble, NavVis, Matterport, and other scan-to-BIM lasers."),
        ("drones.html", f"{counts['drones'][0]} drones", "Drones for AEC &amp; BIM", "DJI enterprise platforms, Skydio, Wingtra, Autel, and other reality-capture aircraft."),
    ]
    grid = "".join(
        f'<a class="card" href="{url_for(href)}"><span class="cnt">{cnt}</span><span class="nm">{name}</span><span class="ds">{ds}</span><span class="go">Open guide →</span></a>'
        for href, cnt, name, ds in cards
    )
    seo = SEO["home"]
    ld = [
        {**WEBSITE, "publisher": {"@type": "Organization", "name": "BIM Reference Library", "url": CANON + "/"}},
        {"@type": "WebPage", "@id": CANON + "/#webpage", "url": CANON + "/", "name": seo["title"], "description": seo["description"],
         "isPartOf": {"@id": WEBSITE_ID}, "inLanguage": "en", "dateModified": UPDATED_ISO, "mainEntity": {"@id": CANON + "/#sections"}},
        {"@type": "ItemList", "@id": CANON + "/#sections", "name": "BIM Reference Library guides", "numberOfItems": len(sections),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s_["title"], "url": CANON + "/" + s_["slug"]} for i, s_ in enumerate(sections)]},
        faq_ld(seo["faq"], CANON + "/"),
    ]
    html = head(seo["title"], seo["description"], "/", ld)
    html += "<body>\n" + wrap(nav("index.html"))
    html += '<div class="wrap chart-wrap" id="main">\n'
    html += hero("Independent BIM software guide", "BIM Reference Library",
                 "A free, ad-free field guide to the software and reality-capture hardware people actually use to design, capture, coordinate, fabricate, and visualize buildings. Popularity is cited, not invented.")
    html += intro_block(seo["intro_q"], seo["intro"])
    html += f"""  <section class="site-search" role="search" aria-labelledby="site-search-h">
    <h2 id="site-search-h">Search every product</h2>
    <label for="site-search">Software, scanners, and drones — by name, maker, or tag</label>
    <input type="search" id="site-search" placeholder="Try Revit, Leica, DJI, MEP, LiDAR…" autocomplete="off" spellcheck="false" aria-describedby="site-status" aria-controls="site-results">
    <p class="sr-status" id="site-status" aria-live="polite">Searches all {len(index)} products across every section.</p>
    <ul class="sr-list" id="site-results" hidden></ul>
  </section>
  <section class="grp">
    <h2>Start here</h2>
    <div class="grid">{grid}</div>
  </section>
  <div class="notes">
    <section>
      <h2>How to use this site</h2>
      <p>Search above to jump straight to any product’s row, or open a section. Each section opens as a compact, scrollable comparison chart — one row per product — that you can filter, search, and sort. Stars are a 1–5 popularity judgment with a source caption. Cost uses a Free / $ / $$ / $$$ / $$$$ scale with a source caption. Learning-curve labels are editorial. Official-site links are not affiliate links.</p>
    </section>
    <section>
      <h2>Where the numbers come from</h2>
      <p>The main firm-adoption source for software is the Confluence 2025 AEC Tech Stack Survey (Q4 2025). European figures for Archicad and ALLPLAN come from the European Architectural Barometer Q4 2025. Review counts come from G2, checked in November 2026. Scanning and drone pages have no comparable product-level firm survey in that report, so popularity there is an editorial judgment unless a caption cites another source. If a product has no usable source, the caption says “Editorial estimate.”</p>
    </section>
    <section>
      <h2>What this is not</h2>
      <p>This is not a vendor ranking you should buy from blindly. It is a starting map for people learning the BIM software landscape.</p>
    </section>
  </div>
{faq_block(seo["faq"])}</div>
{footer(home=True)}
<script>window.SEARCH_INDEX = {index_js};</script>
<script src="/home-search.js?v={ASSET_V}"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    print("wrote index.html")

def write_updates():
    u = CANON + "/updates"
    ld = [{**WEBSITE},
          {"@type": "WebPage", "@id": u + "#webpage", "url": u, "name": SEO["updates"]["title"], "description": SEO["updates"]["description"],
           "isPartOf": {"@id": WEBSITE_ID}, "inLanguage": "en", "dateModified": UPDATED_ISO, "breadcrumb": {"@id": u + "#breadcrumb"}},
          {**breadcrumbs([("Home", "/"), ("Updates", "/updates")]), "@id": u + "#breadcrumb"}]
    html = head(SEO["updates"]["title"], SEO["updates"]["description"], "/updates", ld)
    html += "<body>\n" + wrap(nav("updates.html"))
    html += '<div class="wrap chart-wrap" id="main">\n'
    html += hero("Changelog", "Updates", "A short, plain-English record of what changed on this site.", checked=False)
    html += f"""  <article>
    <div class="log">
      <h2>Site launch</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>The first public version of the BIM Reference Library went live, with five guides — Modeling, Revit add-ins, Coordination &amp; clash, Spooling &amp; fabrication, and Visualization — plus this updates page. Popularity captions were researched in November 2026. See CHANGELOG.md in the repository for sources.</p>
    </div>
    <div class="log">
      <h2>Product cards render fix</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Fixed a JavaScript typo that left section pages without their product cards after the first deploy. Hover glow now also applies to those cards, not only the homepage section tiles.</p>
    </div>
    <div class="log">
      <h2>Custom domain and Git auto-deploy</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>The site now lives at <a href="https://bimchart.net">bimchart.net</a>. The pages.dev address still works; search engines are pointed at the .net copy. Pushing to the GitHub <code>main</code> branch now publishes automatically.</p>
    </div>
    <div class="log">
      <h2>Auto-deploy on push confirmed</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>The Cloudflare Workers and Pages GitHub App now has access to this repository, so a push to <code>main</code> publishes the site without a manual deploy.</p>
    </div>
    <div class="log">
      <h2>Ko-fi footer</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Every page now has the same Ko-fi support line used on ammochart.net.</p>
    </div>
    <div class="log">
      <h2>Footer matches other sites</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>The page footer is now only the shared Ko-fi line used on ammochart.net and Marcus's other sites. The homepage also has the "Last updated / See what changed" line, like ammochart's home page.</p>
    </div>
    <div class="log">
      <h2>Cost ratings on every card</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Each product card now has a Cost row on a Free / $ / $$ / $$$ / $$$$ scale, with a caption citing a published price or marking the band as an estimate. You can sort each guide cheapest-first or priciest-first.</p>
    </div>
    <div class="log">
      <h2>Comparison charts, not more cards</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Section pages are now compact, horizontally scrollable comparison charts in the same style as the ammo reference charts: sticky headers, filter chips, click-to-sort columns, and a small visual in the first column. That visual is the product’s desktop or app icon when we could find an official one, or a generated initials tile if we could not.</p>
    </div>
    <div class="log">
      <h2>Official icons and learning-curve header</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Replaced generated initials tiles with official app icons or official product/vendor marks on all five section charts wherever those assets could be found. The Learning curve column now notes “editorial rating” once in the header instead of repeating “editorial” on every row.</p>
    </div>
    <div class="log">
      <h2>Scanning hardware and AEC drones</h2>
      <p><time datetime="{CHECKED_ISO}">{CHECKED}</time></p>
      <p>Added two new guides — Scanning hardware and Drones for AEC and BIM — each with a homepage tile and the same scrollable comparison chart used on the software sections. First-column visuals are official product photos when we could fetch them, or a generated illustration if not. Popularity is editorial on these pages (the Confluence 2025 survey is software-only). Cost is a purchase-price band with official or reseller citations, or an estimate when the vendor only quotes.</p>
    </div>
    <div class="log">
      <h2>Search every product, clearer charts</h2>
      <p><time datetime="{NOV14_ISO}">{NOV14}</time></p>
      <p>The homepage now has one search box that looks through every product on every chart — software, scanners, and drones — by name, maker, or tag. Each result shows the icon, name, and section, and jumps straight to that product’s row, which briefly lights up.</p>
      <p>Every chart now has an obvious scrollbar that stays pinned to the bottom of the screen while the chart is in view, plus edge fades and a “scroll sideways” cue, on desktop and phones. The “Showing X of Y” line now names each section correctly (modeling tools, Revit add-ins, coordination tools, spooling tools, visualization tools, scanners, drones) and follows every filter and search. Some filter labels were spelled out so they make sense without BIM jargon — for example “Authoring” is now “Model authoring” and “Clash” is now “Clash detection.” No product data or ratings changed.</p>
    </div>
    <div class="log">
      <h2>Compact mobile navigation</h2>
      <p><time datetime="{NOV14_ISO}">{NOV14}</time></p>
      <p>On phones, the top navigation no longer wraps across several sticky lines. It stays a single compact bar with a keyboard-accessible menu button (Esc and click-outside close it). The open menu lists every section and marks the page you are on. The desktop nav is unchanged. This applies on every page, including Updates and the 404 page.</p>
    </div>
    <div class="log">
      <h2>Clearer answers and search clean-up</h2>
      <p><time datetime="{UPDATED_ISO}">{UPDATED}</time></p>
      <p>Each guide now opens with a short, plain-English answer to its main question (for example, which modeling software firms use most) and ends with a short FAQ. Every fact in them comes from the chart rows and source notes already on the page. The homepage has the same intro and FAQ.</p>
      <p>Every chart now loads with its rows already in the page, so it appears without waiting for JavaScript and does not jump as it loads. Filters, search, and sorting still work the same. Product images load lazily. Pages have clearer titles and descriptions, structured data, a sitemap with real last-changed dates, and a short <a href="/llms.txt">llms.txt</a> summary for AI search tools. Links now use the site’s clean addresses (for example /modeling). No product data or ratings changed. “Data last checked” stays {CHECKED}.</p>
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
<link rel="stylesheet" href="{CANON}/theme.css?v={ASSET_V}">
<script src="{CANON}/nav.js?v={ASSET_V}" defer></script>
<script>
(function(){{var p=location.pathname;if(p.length>1&&p.charAt(p.length-1)==="/")location.replace(p.slice(0,-1)+location.search+location.hash);}})();
</script>
</head>
<body>
<div class="page-bg"></div>
{nav("", prefix=CANON + "/")}
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
    <a class="card" href="{CANON}/scanning"><span class="nm">Scanning</span><span class="go">Open →</span></a>
    <a class="card" href="{CANON}/drones"><span class="nm">Drones</span><span class="go">Open →</span></a>
  </div>
</div>
{footer()}
</body>
</html>
"""
    (ROOT / "404.html").write_text(html)
    print("wrote 404.html")

def write_meta(stats):
    pages = [f for f, _ in NAV]  # every indexable page; 404.html is noindex and stays out
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f in pages:
        sm.append(f"  <url><loc>{CANON}{url_for(f)}</loc><lastmod>{lastmod(f)}</lastmod></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot",
            "Perplexity-User", "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended", "DuckDuckBot"]
    robots = "# bimchart.net is a free, public reference site. Search engines and AI search/answer crawlers are welcome.\n"
    robots += "User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    robots += f"Sitemap: {CANON}/sitemap.xml\n"
    (ROOT / "robots.txt").write_text(robots)
    (ROOT / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY)
    write_llms(stats)
    (ROOT / "_headers").write_text(
        f"# Tell search engines that bimchart.net is the main address.\n"
        f"# bimchart.pages.dev keeps working; it just points Google to the .net copy.\n"
        f"/*\n  Link: <{CANON}/:splat>; rel=\"canonical\"\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n"
        "\n/icons/*\n  Cache-Control: public, max-age=2592000\n"
        "\n/og-image.png\n  Cache-Control: public, max-age=2592000\n"
        "\n/theme.css\n  Cache-Control: public, max-age=86400\n"
        "\n/*.js\n  Cache-Control: public, max-age=86400\n"
        "\n/llms.txt\n  Content-Type: text/plain; charset=utf-8\n"
    )
    (ROOT / "README.md").write_text(f"""# BIM Reference Library

**Live site:** [{CANON}]({CANON})

A free, ad-free field guide to BIM software and reality-capture hardware — modeling tools, Revit add-ins, coordination and clash detection, spooling and fabrication, visualization, scanning hardware, and AEC drones. Built as a plain static site (HTML, CSS, and JavaScript, no build step).

There are no ads and no affiliate links. Official-site links go to the vendor.

Many ratings are relative judgments with cited sources. Check the vendor and your own office standards before you buy or standardize on a tool.

## Local preview

Serve the folder with a static file server that supports clean URLs, for example `npx serve .` — internal links use the same extensionless addresses Cloudflare Pages serves (`/modeling`, not `/modeling.html`).

## Build

The HTML pages, `sitemap.xml`, `robots.txt`, `llms.txt`, `_headers`, this README, and `CHANGELOG.md` are generated by `python3 _build/generate.py` from the JSON files in `_build/`. Search titles, descriptions, intros, and FAQs live in `_build/seo_content.py`; only use facts that already appear on the charts.

## Search engines

- `sitemap.xml` lists every indexable page with its real last-changed date (from git history).
- `{INDEXNOW_KEY}.txt` at the site root is the IndexNow key file. After a deploy, notify IndexNow with the sitemap URLs (see CHANGELOG, Nov 20, 2026).

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

## {CHECKED} — Official icons and learning-curve header

Replaced generated initials tiles with official app icons or official product/vendor marks for 17 products, stored locally in /icons and shown on all five section charts: Revit (official 3D R badge from the Autodesk Revit Logo SVG on Wikimedia Commons); Archicad (official Graphisoft icon, Commons File:Archicad.svg); OpenBuildings (official Bentley Systems logo fitted on a tile; no product-specific app icon found); ALLPLAN (official ring mark from the Commons logo SVG); BricsCAD BIM (official mark from the Commons BricsCAD logo); CTC (official CTC wordmark from ctcsoftware.com); RevitLookup (official ProductIcon.png from lookup-foundation/RevitLookup); Bird Tools (official logo from birdtools-developers.com); Xrev Transmit (official Xrev mark from xrev.com.au); Newforma Konekt (official Newforma App Store icon); Solibri (official S app icon from solibri.com); Enscape (official E mark from the Commons Enscape logo SVG); Twinmotion (official product mark; vendor icon paths returned HTTP 403); 3ds Max (official 2022 rebrand desktop icon on Commons); V-Ray (official Chaos product icon from static.chaos.com); Vantage (official Chaos Vantage logo from static.chaos.com); and Victaulic Tools for Revit (official Victaulic logo; the SpoolTracker app icon was not used because it is a different product).

Nine tiles remain generated initials because no distinct official app icon or product mark could be fetched this session (Autodesk, UNIFI, AGACAD, COINS, SysQue, and Tekla PowerFab pages blocked a bot client or only exposed a parent-brand mark already used by another row): Navisworks, BIM Collaborate Pro, Advance Steel, Autodesk Fabrication, UNIFI, AGACAD, COINS Auto-Section Box, SysQue, and Tekla PowerFab.

On all five section charts, the Learning curve column now carries a single “editorial rating” note in the header. The per-row “editorial” caption was removed. The notes section still explains that learning-curve labels are editorial.

## {CHECKED} — Scanning hardware and AEC drones

Added two new section guides — Scanning hardware and Drones for AEC and BIM — with homepage tiles, nav links on every page, sitemap entries, and the same ammo-style comparison chart used on the software sections (filter chips, search, sort, sticky sortable headers, mobile scroll hint, first-column visual, popularity and cost with source captions, and a header-level “editorial rating” note on Learning curve). Hardware charts add comparison columns for type, range, accuracy, and scan speed (scanners) or payload, flight time, RTK, and LiDAR (drones). Those extra columns appear only on the new pages; the five software charts are unchanged.

Popularity on both new pages is editorial. The Confluence 2025 AEC Tech Stack Survey is software-only. BuiltWorlds 2026 Field Solutions reported category-level reality-capture use (drones 100%, 360 photography 88%, LiDAR scanners 81% among organizations already using reality capture) but not product shares. No firm-percentage or review counts were invented.

Cost uses a purchase-price band for one unit or a clearly described kit: $ under about $15,000; $$ about $15,000–40,000; $$$ about $40,000–80,000; $$$$ about $80,000+ or quote-only. Official Leica Geosystems shop prices checked November 2026: “Leica RTC” $46,000, BLK360 $26,500, BLK2GO $37,500 (BLK2GO PULSE $42,800). Official Matterport Pro3 starting at $1,995 plus a required Professional subscription from $245/month (matterport.com/pro3). Authorized reseller Moss Geospatial listings for FARO Focus Premium $41,860 / $51,950 / $63,900 (70 / 150 / 350 m) and Focus Core $32,940, and FARO Orbis $56,000. Authorized DJI reseller listings: Matrice 350 RTK aircraft $11,500 (Vertex Unmanned) / $11,129 drone-only (Indy Drone Supply), Zenmuse L2 $15,490, Zenmuse P1 $6,500, Mavic 3 Enterprise $4,509, Matrice 4E Worry-Free Plus Combo $5,189 (Vertex Unmanned). Other products are quote-only estimates with no invented dollar amount.

First-column visuals are official vendor product photos, stored locally, when they could be fetched; FARO Focus, FARO Orbis, FARO ZEB Horizon, NavVis MLX, Autel EVO Max 4T, and WingtraRAY use generated illustration tiles because no clean official packshot was retrieved this session.

## {NOV14} — Site-wide search, sticky chart scrollbar, clearer filter labels

- Homepage search box covers every product on all seven charts (software, scanners, drones) by name, maker, or tag. Results show the icon, name, and section and link to `section.html#p-<id>`; the chart page scrolls that row into view below the sticky nav and highlights it briefly. Every chart row now has a stable `id`.
- `scroll-hint.js` rebuilt on the ammochart.net approach and fixed: the previous copy referenced an undefined `touch` variable, so the script stopped before adding any scroll cues. Every chart now gets a hint bar with ◀ ▶ buttons, edge fades, and a custom-drawn scrollbar (track + thumb) that sticks to the bottom of the viewport while the chart is on screen, so it is visible on phones and with overlay scrollbars too.
- Results count line uses each section’s noun: modeling tools, Revit add-ins, coordination tools, spooling tools, visualization tools, scanners, drones (Modeling previously said “authoring tools”).
- Filter chip / row tag renames (data otherwise unchanged): Modeling — Authoring → Model authoring, Conceptual → Concept design, Computational → Computational design, Planning → Site planning; Revit add-ins — Production → Productivity, Data → Excel & data, Content → Content library; Coordination — Clash → Clash detection, 4D → 4D scheduling, CDE → Common data environment, Issues → Issue tracking, Field → Field app, QA → Quality checks, IFC → IFC / openBIM; Spooling — Detailing → Steel detailing, Content → Content library; Visualization — Real-time → Real-time rendering, 4D → 4D scheduling, AI → AI rendering; Scanning — Terrestrial → Terrestrial laser, SLAM → Mobile SLAM; Drones — RTK → RTK positioning, VTOL → VTOL (vertical takeoff); all software charts — Web → Web app.
- CSS/JS links carry a `?v=` version so browsers pick up the new files. Product data, ratings, and sources were not changed; “Data last checked” stays Nov 13, 2026.

## {NOV14} — Compact mobile navigation

On viewports 1099 px and narrower, the sticky top navigation collapses to a single compact bar with a hamburger menu button instead of wrapping to multiple lines. The menu is a keyboard-accessible disclosure (aria-expanded, aria-controls, Escape and click-outside to close) and the current page stays marked with aria-current. Desktop navigation is unchanged. Applied to every page, including the homepage, all seven section guides, Updates, and the 404 page.

## {UPDATED} — Search and AI-search pass

- Unique, descriptive `<title>` and meta description on every page (home, seven guides, Updates); one H1 per page; Updates log entries are now H2s. Canonicals, `og:url`, and the sitemap all use the clean URLs Cloudflare Pages serves (`/modeling`); internal links now point at those URLs directly instead of `*.html` (which 308-redirects). Added `twitter:image:alt`, `robots` max-image-preview, and `theme-color`. The 404 page stays `noindex` and out of the sitemap.
- Each guide opens with a short plain-English answer to its main question and ends with a visible 4-question FAQ; the homepage has an intro and a 5-question FAQ. Text is written from facts already on the charts and in each page's “Sources and limits” (Confluence 2025, European Architectural Barometer Q4 2025, G2, BuiltWorlds 2026, official/reseller prices). No new numbers.
- JSON-LD on every indexable page: `WebSite`; `BreadcrumbList`; `CollectionPage` + `ItemList` (one `ListItem` per chart row, in popularity order, linking to the row anchor) + `Dataset` on each guide; `FAQPage` matching the visible FAQ on the guides and home.
- Chart rows are now rendered into the HTML by the generator (same markup and default popularity sort as `app.js`), so crawlers and no-JS readers see the full chart and the table no longer shifts on load. Applied to all seven charts. Images use `loading="lazy"` and `decoding="async"` with fixed width/height.
- `sitemap.xml` has `<lastmod>` from git history; `robots.txt` allows everyone and names GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, Bingbot, and others; new `/llms.txt` summary; IndexNow key file `{INDEXNOW_KEY}.txt`.
- Google Fonts CSS loads without blocking first paint; static icons/CSS/JS get cache headers; the Ko-fi footer link is underlined so it is distinguishable in text (wording unchanged). Each guide links to the other guides.
- Product data, ratings, and sources did not change. “Data last checked” stays {CHECKED}.
""")
    print("wrote sitemap, robots, _headers, README, CHANGELOG")

INDEXNOW_KEY = "5916874163ae4f16d2478a185d0e2679"

def lastmod(f):
    """Last real change date for a page: today if the generated file differs from HEAD, else its last commit date."""
    try:
        changed = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", f], cwd=ROOT).returncode != 0
        if not changed:
            out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], cwd=ROOT, capture_output=True, text=True).stdout.strip()
            if out:
                return out
    except OSError:
        pass
    return datetime.date.today().isoformat()

def write_llms(stats):
    sections = json.loads((BUILD / "sections.json").read_text())
    L = ["# BIM Reference Library (bimchart.net)", "",
         "> Free, ad-free comparison charts for BIM software and reality-capture hardware: modeling, Revit add-ins, coordination and clash detection, MEP and steel spooling/fabrication, visualization and rendering, laser scanners, and AEC drones. One scrollable chart per section, one row per product.", "",
         "There are no ads and no affiliate links. Official-site links go straight to each vendor. Star ratings are not paid placement.", "",
         "## How the ratings work", "",
         "- Popularity: a 1–5 judgment (halves allowed) of how commonly a product shows up in recent firm surveys, review directories, or marketplace ranks, relative to the other products in the same section. Each rating has a caption naming its source and a “checked Nov 2026” date, or it says “Editorial estimate.”",
         "- Main software source: Confluence 2025 AEC Tech Stack Survey (Q4 2025, design-firm sample). Archicad and ALLPLAN also cite the European Architectural Barometer Q4 2025. G2 review counts were checked in November 2026.",
         "- Scanning and drone popularity is an editorial rating: the Confluence survey is software-only, and no product-level scanner or drone survey was found.",
         "- Cost: Free / $ / $$ / $$$ / $$$$. Software uses a published annual price for one commercial seat; hardware uses a purchase-price band for one unit or kit. Captions cite an official or reseller price, or mark the band as an estimate. No dollar amounts are invented.",
         "- Learning curve: an editorial rating (Gentler / Moderate / Steep), not a test score.",
         f"- Product data last checked: {CHECKED}. Site last updated: {UPDATED}.", "",
         "## Sections", ""]
    for sec in sections:
        data = json.loads((BUILD / sec["json"]).read_text())
        names = ", ".join(d["name"] for d in sorted(data, key=lambda d: (-(d.get("pop") or 0), d["name"].lower())))
        L.append(f'- [{sec["title"]}]({CANON}/{sec["slug"]}): {SEO[sec["slug"]]["description"]} Products: {names}.')
    L += ["", "## Other pages", "",
          f"- [Home]({CANON}/): overview, site-wide product search, and FAQ.",
          f"- [Updates]({CANON}/updates): plain-English changelog.",
          f"- [Sitemap]({CANON}/sitemap.xml)", "",
          "## Using this site as a source", "",
          "Cite the section page and the caption's source and date. Ratings are relative within a section and can go stale; confirm current pricing and features with the vendor.", ""]
    (ROOT / "llms.txt").write_text("\n".join(L))

def main():
    sections = json.loads((BUILD / "sections.json").read_text())
    stats = {}
    for sec in sections:
        stats[sec["slug"]] = write_catalog(sec)
    write_home(stats, sections)
    write_updates()
    write_404()
    write_meta(stats)
    print("DONE", stats)

if __name__ == "__main__":
    main()
