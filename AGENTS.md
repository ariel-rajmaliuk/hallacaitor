# Working on Hallacaitor

- Read README.md and docs/design.md before changing CAD. This is a physical-tool CAD alpha, not a validated food appliance.
- Keep all permanent machine hardware printable. Do not silently introduce metal shafts, purchased springs, motors or adhesives. Food, leaf, string and food-contact barriers are separate consumables.
- Source of geometry: cad/hallacaitor.scad (Compact/reused parts) and cad/modular.scad (Familiar/Dock). Source of part names, quantities and print orientations: config/parts.json. Do not edit STL alone.
- Never mix v0.1 and v0.2 geometry. North and south wings are distinct handed parts; preserve their indexing arms on the right-hand end of the base.
- The three transverse needle routes must stay in the axial hinge gaps. Run motion/needle intersection checks after changing hinges, channels or indexing.
- The open thickness rings intentionally have 0.2 mm diametral interference at their seats. Distinguish that fit from accidental collision; elastic assembly is not simulated.
- After CAD changes run export.py, unit tests, validate.py and check_motion.py. Update the checked-in geometry report intentionally. If assembly transforms change, update the illustrations/drawings too.
- Rebuild the Compact manual, A4 template and Familiar manual PDFs after documentation changes and visually inspect rendered pages. Do not ship printer-specific G-code.
- Do not invent printing, food-contact, load, cooking-seal or throughput test results. examples/bench_log.csv must remain an empty template; put actual observations in separately dated files with printer/material details.
- Preserve the MIT license and attribution selected by Ariel. Do not copy third-party CAD, recipes or images into the repo without compatible rights and notices.

- Web content lives in web/content.json; build with scripts/build_site.py. All 61 part pages must have a local image, STL and source link. Keep config/stations.json, kit quantities and layout drawings consistent.
- Dock is gravity registration, storage posts are for two unloaded tiers only. Never describe them as captive locks or a validated working tower.
