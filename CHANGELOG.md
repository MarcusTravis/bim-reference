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
