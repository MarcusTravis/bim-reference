# Changelog

All notable changes to the BIM Reference Library, with sources.

## Nov 13, 2026 — Initial public release

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

- Modeling: 11 (sourced 11, editorial 0)
- Revit add-ins: 12 (sourced 10, editorial 2)
- Coordination & clash: 9 (sourced 6, editorial 3)
- Spooling & fabrication: 9 (sourced 2, editorial 7)
- Visualization: 9 (sourced 8, editorial 1)

## Nov 13, 2026 — Product cards render fix

Fixed a JavaScript typo (`initCatalog` required a `#catalog` element that the pages did not include), which left section pages without product cards after the first deploy. Hover glow now also applies to product cards, not only homepage section tiles.

## Nov 13, 2026 — Custom domain and Git auto-deploy

The canonical site address is now [https://bimchart.net](https://bimchart.net). `bimchart.pages.dev` remains available and points search engines at the .net copy via canonical tags and `_headers`. Automatic production deploys on push to `main` were enabled by reconnecting the GitHub source on the Cloudflare Pages project.

## Nov 13, 2026 — Auto-deploy on push confirmed

Production deploys now start automatically when commits are pushed to `main`, after the Cloudflare Workers and Pages GitHub App was granted access to this repository.

## Nov 13, 2026 — Ko-fi footer

Added the same Ko-fi support line used on ammochart.net to every page footer.

## Nov 13, 2026 — Footer matches other sites

The page footer is now only the shared Ko-fi line used on ammochart.net and Marcus's other sites. The homepage also has the "Last updated / See what changed" line, like ammochart's home page.

## Nov 13, 2026 — Cost ratings

Added a Cost row (Free / $ / $$ / $$$ / $$$$) to every product card, researched in November 2026 from vendor pricing pages and official shops. Bands: Free (no license fee); $ under about $500/year; $$ about $500–2,000/year; $$$ about $2,000–5,000/year; $$$$ about $5,000+/year or quote-only enterprise with no public list price. Captions cite the source or say the rating is an estimate. No prices were invented. Sort options now include cheapest first and priciest first.

Official figures used include Autodesk list prices for Revit ($3,005/year), AutoCAD ($2,095/year), Navisworks Manage ($2,835/year), 3ds Max ($2,010/year), and Forma Site Design ($700/year); Graphisoft Archicad Studio ($2,414/year); Vectorworks Architect ($1,530/year); ALLPLAN Concept ($2,892/year); SketchUp Pro ($399/year); the RhinoARQ bundle ($1,695 perpetual); Chaos Enscape Solo ($574.80/year), V-Ray Solo ($540/year), and Veras Pro ($348/year); Twinmotion ($445/year over the $1M revenue threshold); Lumion Pro ($1,149/year); AVAIL ($250/year); DiRootsOne Premium ($120/year US / €100); IdeateApps ($495/year); CTC BIM Project Suite ($410); Bird Tools individual apps ($10–$49.50/year); Victaulic Tools for Revit ($200/license); Solibri Essential (€1,428/year); and BIMcollab Zoom Single (about €720/year). Many fabrication, coordination, and specialist tools remain quote-only.

## Nov 13, 2026 — Comparison charts

Replaced the product-card grids on all five section pages with a compact, horizontally scrollable comparison chart in the same layout as the ammo reference charts (filter chips, count, sticky sortable headers, first-column visual, and a mobile scroll hint). The first column shows a 128 px desktop/app icon for each product, stored in /icons and not hotlinked. Official vendor or App Store icons were used when they could be found; the rest are generated initials tiles in the same rounded-square style. Popularity, cost, captions, filters, and cheapest/priciest sort options are unchanged.

## Nov 13, 2026 — Official icons and learning-curve header

Replaced generated initials tiles with official app icons or official product/vendor marks for 17 products, stored locally in /icons and shown on all five section charts: Revit (official 3D R badge from the Autodesk Revit Logo SVG on Wikimedia Commons); Archicad (official Graphisoft icon, Commons File:Archicad.svg); OpenBuildings (official Bentley Systems logo fitted on a tile; no product-specific app icon found); ALLPLAN (official ring mark from the Commons logo SVG); BricsCAD BIM (official mark from the Commons BricsCAD logo); CTC (official CTC wordmark from ctcsoftware.com); RevitLookup (official ProductIcon.png from lookup-foundation/RevitLookup); Bird Tools (official logo from birdtools-developers.com); Xrev Transmit (official Xrev mark from xrev.com.au); Newforma Konekt (official Newforma App Store icon); Solibri (official S app icon from solibri.com); Enscape (official E mark from the Commons Enscape logo SVG); Twinmotion (official product mark; vendor icon paths returned HTTP 403); 3ds Max (official 2022 rebrand desktop icon on Commons); V-Ray (official Chaos product icon from static.chaos.com); Vantage (official Chaos Vantage logo from static.chaos.com); and Victaulic Tools for Revit (official Victaulic logo; the SpoolTracker app icon was not used because it is a different product).

Nine tiles remain generated initials because no distinct official app icon or product mark could be fetched this session (Autodesk, UNIFI, AGACAD, COINS, SysQue, and Tekla PowerFab pages blocked a bot client or only exposed a parent-brand mark already used by another row): Navisworks, BIM Collaborate Pro, Advance Steel, Autodesk Fabrication, UNIFI, AGACAD, COINS Auto-Section Box, SysQue, and Tekla PowerFab.

On all five section charts, the Learning curve column now carries a single “editorial rating” note in the header. The per-row “editorial” caption was removed. The notes section still explains that learning-curve labels are editorial.

## Nov 13, 2026 — Scanning hardware and AEC drones

Added two new section guides — Scanning hardware and Drones for AEC and BIM — with homepage tiles, nav links on every page, sitemap entries, and the same ammo-style comparison chart used on the software sections (filter chips, search, sort, sticky sortable headers, mobile scroll hint, first-column visual, popularity and cost with source captions, and a header-level “editorial rating” note on Learning curve). Hardware charts add comparison columns for type, range, accuracy, and scan speed (scanners) or payload, flight time, RTK, and LiDAR (drones). Those extra columns appear only on the new pages; the five software charts are unchanged.

Popularity on both new pages is editorial. The Confluence 2025 AEC Tech Stack Survey is software-only. BuiltWorlds 2026 Field Solutions reported category-level reality-capture use (drones 100%, 360 photography 88%, LiDAR scanners 81% among organizations already using reality capture) but not product shares. No firm-percentage or review counts were invented.

Cost uses a purchase-price band for one unit or a clearly described kit: $ under about $15,000; $$ about $15,000–40,000; $$$ about $40,000–80,000; $$$$ about $80,000+ or quote-only. Official Leica Geosystems shop prices checked November 2026: “Leica RTC” $46,000, BLK360 $26,500, BLK2GO $37,500 (BLK2GO PULSE $42,800). Official Matterport Pro3 starting at $1,995 plus a required Professional subscription from $245/month (matterport.com/pro3). Authorized reseller Moss Geospatial listings for FARO Focus Premium $41,860 / $51,950 / $63,900 (70 / 150 / 350 m) and Focus Core $32,940, and FARO Orbis $56,000. Authorized DJI reseller listings: Matrice 350 RTK aircraft $11,500 (Vertex Unmanned) / $11,129 drone-only (Indy Drone Supply), Zenmuse L2 $15,490, Zenmuse P1 $6,500, Mavic 3 Enterprise $4,509, Matrice 4E Worry-Free Plus Combo $5,189 (Vertex Unmanned). Other products are quote-only estimates with no invented dollar amount.

First-column visuals are official vendor product photos, stored locally, when they could be fetched; FARO Focus, FARO Orbis, FARO ZEB Horizon, NavVis MLX, Autel EVO Max 4T, and WingtraRAY use generated illustration tiles because no clean official packshot was retrieved this session.

## Nov 14, 2026 — Site-wide search, sticky chart scrollbar, clearer filter labels

- Homepage search box covers every product on all seven charts (software, scanners, drones) by name, maker, or tag. Results show the icon, name, and section and link to `section.html#p-<id>`; the chart page scrolls that row into view below the sticky nav and highlights it briefly. Every chart row now has a stable `id`.
- `scroll-hint.js` rebuilt on the ammochart.net approach and fixed: the previous copy referenced an undefined `touch` variable, so the script stopped before adding any scroll cues. Every chart now gets a hint bar with ◀ ▶ buttons, edge fades, and a custom-drawn scrollbar (track + thumb) that sticks to the bottom of the viewport while the chart is on screen, so it is visible on phones and with overlay scrollbars too.
- Results count line uses each section’s noun: modeling tools, Revit add-ins, coordination tools, spooling tools, visualization tools, scanners, drones (Modeling previously said “authoring tools”).
- Filter chip / row tag renames (data otherwise unchanged): Modeling — Authoring → Model authoring, Conceptual → Concept design, Computational → Computational design, Planning → Site planning; Revit add-ins — Production → Productivity, Data → Excel & data, Content → Content library; Coordination — Clash → Clash detection, 4D → 4D scheduling, CDE → Common data environment, Issues → Issue tracking, Field → Field app, QA → Quality checks, IFC → IFC / openBIM; Spooling — Detailing → Steel detailing, Content → Content library; Visualization — Real-time → Real-time rendering, 4D → 4D scheduling, AI → AI rendering; Scanning — Terrestrial → Terrestrial laser, SLAM → Mobile SLAM; Drones — RTK → RTK positioning, VTOL → VTOL (vertical takeoff); all software charts — Web → Web app.
- CSS/JS links carry a `?v=` version so browsers pick up the new files. Product data, ratings, and sources were not changed; “Data last checked” stays Nov 13, 2026.
