# Search titles, meta descriptions, short intros, and visible FAQs.
# Every fact here must already appear on the site (chart rows, captions, or "Sources and limits").
SEO = {
"home": {
  "title": "BIM Reference Library: BIM Software & Hardware Comparison Charts",
  "description": "Free, ad-free comparison charts for BIM software and hardware: modeling, Revit add-ins, clash detection, MEP spooling, rendering, scanners, and AEC drones.",
  "intro_q": "What is the BIM Reference Library?",
  "intro": "bimchart.net is a free, ad-free set of comparison charts for the software and reality-capture hardware used to design, coordinate, fabricate, and visualize buildings. Each section is one scrollable chart with a row per product. You can compare popularity, cost, learning curve, and pros and cons, and each row links to the vendor’s official site.",
  "faq": [
    ("Is bimchart.net free, and are the links paid?", "Yes, it is free. The site has no ads and no affiliate links. Official-site links go straight to the vendor, and star ratings are not paid placement."),
    ("Where do the popularity ratings come from?", "For software, the main source is the Confluence 2025 AEC Tech Stack Survey (Q4 2025). Archicad and ALLPLAN also cite the European Architectural Barometer Q4 2025, and G2 review counts were checked in November 2026. That survey has no product-level scanner or drone figures, so popularity on those pages is an editorial estimate. Every rating has a caption naming its source, or it says “Editorial estimate.”"),
    ("How is cost rated?", "Cost uses a five-step scale: Free, $, $$, $$$, and $$$$. Software is rated on a published annual price for one commercial seat. Scanners and drones are rated on a purchase-price band for one unit or kit. Each section explains its bands. If a vendor only gives quotes, the caption marks the band as an estimate. No dollar amounts are made up."),
    ("Is the learning curve a measured score?", "No. Learning curve (Gentler, Moderate, or Steep) is an editorial rating based on what new users typically go through. It is not a test score."),
    ("How current is the data?", "Product data was last checked on the date shown at the top of each section page (November 2026). The Updates page lists every change in plain English."),
  ],
},
"modeling": {
  "title": "BIM Modeling Software Compared: Revit, Archicad, SketchUp & More",
  "description": "Compare 11 BIM and CAD authoring tools, including Revit, AutoCAD, SketchUp, Rhino, Archicad, and Tekla, on cited popularity, cost, and learning curve.",
  "intro_q": "Which BIM modeling software do firms use most?",
  "intro": "In the Confluence 2025 AEC Tech Stack Survey of design firms, Autodesk Revit showed up in 94.7% of firms, AutoCAD in 85.8%, SketchUp in 73.5%, and Rhino in 49.6%. That sample leans toward US architecture firms. In Europe, Archicad and ALLPLAN are much stronger: the European Architectural Barometer Q4 2025 shows Archicad at 61% of French and 51% of German BIM-user firms.",
  "faq": [
    ("What is the most widely used BIM modeling software?", "Autodesk Revit. It showed up in 94.7% of firms in the Confluence 2025 AEC Tech Stack Survey and had 1,256 G2 reviews (4.6/5) when checked in November 2026."),
    ("Which modeling tools cost less than Revit?", "Revit’s official list price is $3,005 a year. Tools on this chart with lower published prices include SketchUp Pro at $399 a year, Forma Site Design at $700 a year, BricsCAD BIM at $1,166 a year (reseller Novedge), and Vectorworks Architect at $1,530 a year. Always confirm current pricing with the vendor."),
    ("Which BIM modeling tools run on a Mac?", "On this chart, AutoCAD, SketchUp, Rhino, Archicad, Vectorworks Architect, and BricsCAD BIM list macOS. Revit, Tekla Structures, OpenBuildings Designer, and ALLPLAN are Windows tools. SketchUp and Forma also run in a web browser."),
    ("Why does Archicad rate lower than its European use suggests?", "The main survey is US-heavy, and only 10 firms in it listed Archicad. The chart also cites the European Architectural Barometer Q4 2025, where 61% of French and 51% of German BIM-user firms reported Archicad. Popularity is relative to the other tools on this page, not a universal score."),
  ],
},
"revit-addins": {
  "title": "Best Revit Add-ins Compared: pyRevit, DiRoots, Ideate, CTC & More",
  "description": "Compare 12 widely used Revit add-ins, including pyRevit, AVAIL, DiRoots, Ideate, CTC, and RevitLookup, on cited firm counts, cost, and learning curve.",
  "intro_q": "Which Revit add-ins are most widely used?",
  "intro": "In the Confluence 2025 tech-stack inventory, pyRevit was listed by 90 firms, AVAIL by 68, DiRoots Tools by 63, and Ideate Explorer by 51. CTC BIM Manager Suite (42 firms) and RevitLookup (50) are also common. Several of the most-used add-ins are free or have a free tier.",
  "faq": [
    ("What is the most popular Revit add-in?", "On this chart it is pyRevit. 90 firms listed it in the Confluence 2025 inventory, among the highest counts for Revit utilities in that survey. It is free and open source."),
    ("Are there free Revit add-ins worth installing?", "Yes. pyRevit and RevitLookup are free and open source. AVAIL has a free single-user tier, and DiRoots has a free feature-limited tier. RevitLookup is aimed at power users and developers."),
    ("What happened to COINS Auto-Section Box?", "It was historically a top Autodesk App Store download, and 34 firms listed it in Confluence 2025. It has since been reported removed from the Autodesk App Store, and no current public price was found."),
    ("Why are some add-ins marked “Editorial estimate”?", "Xrev Transmit and AGACAD are marked as estimates because no 2025–2026 firm count was found for them. Ratings are relative to the other Revit add-ins on this page."),
  ],
},
"coordination": {
  "title": "BIM Clash Detection & Coordination Software Compared",
  "description": "Compare 9 BIM coordination and clash detection tools, including Navisworks, BIM Collaborate Pro, Revizto, Solibri, and Dalux, on popularity and cost.",
  "intro_q": "What software do BIM teams use for clash detection?",
  "intro": "Autodesk Navisworks is the default clash and 4D coordination tool in many US firms. It was used by 71% of firms in the Confluence 2025 survey. Cloud coordination is just as common: Autodesk Construction Cloud showed up in 94% of firms. Revizto, Trimble Connect, Newforma Konekt, and Solibri also have firm counts, and Dalux, BIMcollab Zoom, and Verity are rated as editorial estimates.",
  "faq": [
    ("What is the most common clash detection software?", "Autodesk Navisworks. 71% of firms in the Confluence 2025 survey used it, and 80 firms listed Navisworks Manage in its inventory. Its official list price is $2,835 a year for Manage."),
    ("What is the difference between Navisworks and BIM Collaborate Pro?", "Navisworks Manage is a Windows desktop tool for federated-model clash detection and 4D. BIM Collaborate Pro, now sold as Forma Design Collaboration, is cloud worksharing and model coordination inside Autodesk Construction Cloud."),
    ("Which tools are built for IFC and openBIM workflows?", "On this chart, Solibri (rule-based model checking and IFC quality control) and BIMcollab Zoom (open BCF issue management) carry the IFC / openBIM tag. Trimble Connect also federates IFC models."),
    ("Can I check a model against laser scans?", "Yes. ClearEdge3D Verity compares the coordinated model to laser scans to find what was actually installed. Its rating here is an editorial estimate."),
  ],
},
"spooling": {
  "title": "MEP Spooling & Fabrication Software: SysQue, EVOLVE, MSUITE",
  "description": "Compare 9 MEP spooling and steel fabrication tools, including SysQue, Autodesk Fabrication, EVOLVE, MSUITE, Stratus, Advance Steel, Tekla PowerFab, and SDS/2.",
  "intro_q": "What is spooling and fabrication software?",
  "intro": "Spooling software takes a constructible model into the shop. It splits pipe, duct, and steel into spools and assemblies, then outputs shop drawings, cut lists, and fabrication packages. Some MEP tools run inside Revit (SysQue, EVOLVE, MSUITE, Victaulic Tools). Others are AutoCAD-based or cloud shop-floor platforms (Autodesk Fabrication, Stratus). Steel shops use Advance Steel, SDS/2, and Tekla PowerFab.",
  "faq": [
    ("Which MEP spooling tools work inside Revit?", "On this chart, Trimble SysQue, EVOLVE Mechanical / Electrical, MSUITE BIM + FAB, and Victaulic Tools for Revit are Revit add-ins. Autodesk Fabrication (CADmep, CAMduct, ESTmep) is the AutoCAD-based suite, and Stratus is a cloud BIM-to-fab platform."),
    ("Why are most spooling ratings editorial estimates?", "The main survey leans toward architecture firms and undercounts contractor shops. G2 and Capterra had only 1–2 reviews each for EVOLVE, MSUITE, and SysQue, which is too few to rank by. Only Advance Steel (16 firms) and SysQue (5) have survey counts, so the others are marked as editorial estimates."),
    ("What software do steel fabricators use?", "This chart covers Autodesk Advance Steel and SDS/2 for steel detailing and shop drawings, and Tekla PowerFab for steel fabrication management from estimate to shop floor (paired with Tekla Structures)."),
    ("How should I choose a spooling tool?", "Talk to shops that already do this work before you buy. Most vendors here sell by quote, so cost bands are often estimates. Confirm pricing and content support with the vendor."),
  ],
},
"visualization": {
  "title": "BIM Rendering Software Compared: Enscape, Twinmotion, Lumion",
  "description": "Compare 9 rendering tools used with BIM models, including Enscape, Twinmotion, Lumion, D5 Render, V-Ray, and Veras, on popularity, cost, and learning curve.",
  "intro_q": "Which rendering software is most used with Revit?",
  "intro": "Enscape is the clear leader. Enscape for Revit showed up in 80.5% of firms in the Confluence 2025 survey, well ahead of the next tier: Twinmotion, Lumion, D5 Render, and 3ds Max. Real-time tools like Enscape, Twinmotion, Lumion, and D5 trade some control for speed. V-Ray and 3ds Max are production renderers for high-end stills and animation.",
  "faq": [
    ("What is the most popular renderer for Revit?", "Enscape. Enscape for Revit showed up in 80.5% of firms (92 listings) in Confluence 2025, and it had 456 G2 reviews (4.6/5) when checked in November 2026."),
    ("Is there a free BIM rendering option?", "Twinmotion is free if your revenue over the last 12 months was under $1 million USD. Otherwise it is $445 per seat per year. D5 Render has a free Community edition for non-commercial use. Commercial work needs D5 Pro."),
    ("What is the difference between real-time and production rendering?", "Real-time tools (Enscape, Twinmotion, Lumion, D5 Render, Chaos Vantage) update as you move through the model. Production tools (Chaos V-Ray, Autodesk 3ds Max) take longer per image and give finer control for marketing and film-quality views."),
    ("Does this page include AI rendering tools?", "Veras is listed for AI visualization from Revit, Forma, and the web (32 firms in Confluence 2025). General generative AI tools from the same survey category are not listed here as BIM visualization products."),
  ],
},
"scanning": {
  "title": "Laser Scanners for Scan-to-BIM Compared: Leica, FARO, Trimble, NavVis",
  "description": "Compare 13 laser and SLAM scanners for scan-to-BIM and as-builts, including Leica RTC360 and BLK360, FARO Focus, Trimble X9, NavVis VLX 3, and Matterport.",
  "intro_q": "Which laser scanners do BIM teams use for scan-to-BIM?",
  "intro": "Most BIM as-built work uses one of three scanner types. Terrestrial tripod scanners (Leica RTC360, FARO Focus, Trimble X9) give the most controlled captures. Mobile SLAM scanners (Leica BLK2GO, NavVis VLX 3, FARO Orbis) are faster to walk through interiors. Compact kits (Leica BLK360, Matterport Pro3) are lighter and cheaper to start with. Popularity on this page is an editorial judgment because no product-level scanner survey was found.",
  "faq": [
    ("How much does a laser scanner for BIM cost?", "Prices vary a lot by class. The official Leica shop lists the RTC360 (“Leica RTC”) at $46,000 and the BLK360 at $26,500. Matterport Pro3 starts at $1,995, plus a required Professional subscription starting at $245 a month. Many other scanners are quote-only, so their bands are marked as estimates."),
    ("What is the difference between a tripod scanner and a SLAM scanner?", "A terrestrial tripod scanner captures from fixed stations for controlled, registered scans. A mobile SLAM scanner is carried, handheld or wearable, and captures while you walk. That is faster for interiors, stairs, and large buildings where tripod setups are slow."),
    ("Which scanners are best for building interiors?", "On this chart, the Leica BLK2GO, NavVis VLX 3, FARO ZEB Horizon, and NavVis MLX carry the Interiors tag. All four are mobile SLAM scanners."),
    ("Why is scanner popularity an editorial estimate?", "The Confluence 2025 survey covers software only. A BuiltWorlds 2026 reality-capture report found that 81% of organizations already using reality capture used LiDAR scanners, but that is a category figure, not a brand share. No firm percentages or review counts were made up."),
  ],
},
"drones": {
  "title": "Drones for AEC & BIM Compared: DJI Matrice, Skydio, Wingtra",
  "description": "Compare 8 reality-capture drones for AEC and BIM, including DJI Matrice 350 RTK, Mavic 3 Enterprise, Skydio X10, and WingtraRAY, on LiDAR, RTK, and cost.",
  "intro_q": "Which drones do AEC and BIM teams fly for reality capture?",
  "intro": "DJI enterprise platforms lead this chart: the Matrice 350 RTK (with a Zenmuse L2 LiDAR or P1 photogrammetry payload), the compact Mavic 3 Enterprise, and the Matrice 4E. US-made options include the Skydio X10 and Freefly Astro. WingtraRAY (VTOL) and AgEagle eBee X (fixed wing) cover large mapping areas. Popularity here is an editorial judgment.",
  "faq": [
    ("Which drones on this chart can carry LiDAR?", "The DJI Matrice 350 RTK with the Zenmuse L2, and WingtraRAY with its official LiDAR payload option. Freefly Astro can carry a third-party LiDAR payload. The Mavic 3 Enterprise, Matrice 4E, Autel EVO Max 4T, and eBee X do not have onboard LiDAR."),
    ("How much does a mapping drone cost?", "Authorized reseller listings checked in November 2026 show the DJI Mavic 3 Enterprise at $4,509, the Matrice 4E Worry-Free Plus Combo at $5,189, and the Matrice 350 RTK aircraft at $11,500. A typical M350 + Zenmuse L2 kit is about $27,000. Skydio, Freefly, Autel, Wingtra, and AgEagle aircraft are quote-only here, so their bands are estimates."),
    ("Are there US-made drones for AEC work?", "Yes. On this chart, the Skydio X10 and Freefly Astro carry the US-made tag."),
    ("Why is drone popularity an editorial estimate?", "The Confluence 2025 survey covers software only. BuiltWorlds 2026 reported that 100% of surveyed organizations already using reality capture used drones, but that is a category figure, not a brand share. No firm percentages or review counts were made up."),
  ],
},
"updates": {
  "title": "Updates & Changelog · BIM Reference Library",
  "description": "A plain-English changelog for bimchart.net: new sections, chart and rating changes, data checks, and site fixes, with dates.",
},
}
