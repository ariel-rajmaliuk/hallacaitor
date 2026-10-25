# Hallacaitor

[Español](../README.md)

**A fully printable, manually operated workbench to help assemble Venezuelan hallacas.** MIT licensed. CAD alpha v0.2.0; not physically built or food-contact validated.

![Hallacaitor CAD overview](assets/hero.png)

It combines dough portion rings (60/80/100 ml), a rolling pin with thickness rings (3/4/5 mm), a folding/tying base with indexed wings, ingredient organizers and a blunt threading needle. All permanent parts, shafts, keys and joints are printed. Food, leaves, string and food-contact barriers are external consumables. Cooking, leaf preparation/cutting, the central fold and final knot remain manual.

Start with the **minimum kit** from [parts.json](../config/parts.json), not the whole machine. Print calibration coupons, assemble the folding module and use paper/simulated packets before real leaves. Do not use bare FDM prints in direct contact with dough or filling. Food-safe material claims do not certify a finished printed tool.

- [Printable STL files](../stl)
- [Bill of materials](bom.md)
- [Assembly guide](assembly.md)
- [Illustrated manual (Spanish PDF)](manual/Hallacaitor_v02.pdf)
- [Drawings](drawings)
- [Digital checks and physical test protocol](testing.md)
- [Primary references](references.md)

Reference printer: 220×220×250 mm. Units: mm. Long shafts are oriented horizontally (the roller shaft diagonally). The optional ingredient lid needs inversion in the slicer. No printer-specific G-code is supplied.

```bash
python scripts/export.py --kit minimum
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/check_motion.py
```

There are no physical test results or proven throughput claims. Contributions with measurements and real printing/leaf-handling tests are welcome. See [CONTRIBUTING](../CONTRIBUTING.md).
