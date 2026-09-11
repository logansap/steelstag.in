# SteelStag SS2026 — Revision History

**Current version: v1.3 · Released 11 September 2026**
Contact: hello@steelstag.in · Portal: steelstag.in/manufacturer/

---

## Read this first

> **v1.3 changes documentation, artwork and packaging only.**
> **No garment fit, sizing, grading, measurement value, tolerance or construction detail has been changed.**
> **Garments already in production are unaffected and require no rework.**

Bulk production began under v1.2 on the basis of the Tech Pack plus direct
communication with SteelStag. v1.3 was raised after an independent consistency
audit of the manufacturer package. Its purpose is to make the written package
say what the factory and SteelStag have already agreed — not to change it.

Every change below is tagged with whether it affects goods in production. Only
one change in the whole release carries any garment-side action at all (R-03,
and that action is a confirmation, not a rework).

---

## Version summary

| Version | Date | Summary | Garment impact |
|---|---|---|---|
| v1.0 | 25 Jun 2026 | Initial manufacturer portal and Tech Pack release. 3 styles, 125 GSM, 32 × 40 cm pouch. | — |
| v1.1 | 25 Jun 2026 | Fabric 125 → 160 GSM. ST-DS-002 Deep Scoop taken out of the SS2026 order scope — the style is retained for a future collection, see R-28. Neck quality requirement and master carton spec added. | Yes — superseded before cutting |
| v1.2 | 06 Aug 2026 | Fabric 160 → 180 GSM across portal, Tech Pack and assets. Pouch 32 × 40 → 24 × 34 cm. | Yes — superseded before cutting |
| **v1.3** | **11 Sep 2026** | **Consistency release.** Pouch-size dependencies corrected; label sizes, bleed and print method published; label artwork, neck-label fit and care symbols corrected; declarations moved to an applied retail sticker; Pantone numbers published as text; tolerance restated consistently; logo brand rule frozen and enforced; style scope separated from the reusable style library; package contents and versioning fixed. | **No** |

**Note on v1.0–v1.2:** those revisions changed the specification without changing
the version identity shown on the portal or the Tech Pack — both continued to
read "v1.2 · Last updated 25 June 2026" while GSM and pouch size changed
underneath. That is the defect R-30 fixes. From v1.3 onward, any specification
change bumps the version and lands in this document.

---

## Change register

### Category key

- **SPECIFICATION CORRECTION** — a stated value was wrong or contradicted another document
- **ARTWORK / PRINT CORRECTION** — the supplied artwork file itself was defective
- **CLARIFICATION** — the value is unchanged; the wording now says what was already meant
- **MANUFACTURER STANDARD** — SteelStag does not need to control this; it is handed to manufacturer standard practice
- **ADMIN / VERSIONING** — release control, file naming, package contents

---

### R-01 · Package version and filenames aligned to v1.3

| | |
|---|---|
| **File / section** | `manufacturer/index.html` (sidebar, hero, badge); all versioned filenames |
| **Category** | ADMIN / VERSIONING |
| **Previous** | Portal `v1.2`; Tech Pack PDF `-v1.0.pdf` with no version inside the document; Labels PDF `-v1.0.pdf`; CSV `-v1.2.csv`; ZIP `-v1.2.zip` |
| **New** | Everything reads `v1.3`: `SteelStag-TechPack-SS2026-v1.3.pdf`, `SteelStag-Labels-PrintReady-v1.3.pdf`, `SteelStag-QuantityBreakdown-SS2026-v1.3.csv`, `SteelStag-CompleteManufacturerPackage-SS2026-v1.3.zip` |
| **Reason** | Five artefacts in one release carried three different version numbers. A quote or an approval could not be tied to a specific package state. |
| **Production impact** | None |
| **Factory action** | Use v1.3 files. Discard earlier copies. |
| **Affects goods in production** | **No** |

---

### R-02 · Production status corrected

| | |
|---|---|
| **File / section** | Portal → Production Summary; hero status badge |
| **Category** | ADMIN / VERSIONING |
| **Previous** | Status `Sampling`; Current Stage `Sampling and vendor selection`; row `Bulk Production — Only after written approval of lab dip, fit sample, and PP sample` |
| **New** | Status `In Production`; Current Stage `Bulk production in progress`; row relabelled `Production Basis — This Tech Pack, plus the agreed factory pattern and production reference as confirmed directly with SteelStag` |
| **Note** | The repository holds no record of a formal written lab dip / fit / PP sign-off, so v1.3 does not assert one. Production proceeded on the Tech Pack plus direct SteelStag–manufacturer communication, and that is what the portal now says. The approval sequence in the Production Workflow table remains the process for anything not yet signed off. |
| **Reason** | The portal still described the order as pre-sampling after bulk production had started. |
| **Production impact** | None — records the actual state |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-03 · Measurement tolerance restated consistently at ±¼"

| | |
|---|---|
| **File / section** | `README.txt` → Key Specifications |
| **Category** | SPECIFICATION CORRECTION |
| **Previous** | README: `Tolerance: ±0.5" all measurements` |
| **New** | README: `Tolerance: +/-1/4" (0.25") on all measurements` |
| **Conflicting source** | Tech Pack / portal Body Measurements: `Tolerance ±¼"` — unchanged, and unchanged since v1.0 |
| **Reason** | The README stated double the Tech Pack's tolerance. The Tech Pack governs and was the document issued to the factory, so the README was the stale copy. No measurement value or tolerance in the Tech Pack has been altered. |
| **Production impact** | None expected — the governing Tech Pack figure is unchanged |
| **Factory action** | **Confirm the run is being measured and QC'd to ±¼", not ±0.5".** If any part of the run was graded or inspected to ±0.5", tell SteelStag before the final inspection. |
| **Affects goods in production** | **Documentation only — but see factory action.** This is the one change in v1.3 that touches the garment side, and only as a confirmation. |

---

### R-04 · Sleeve length governance stated

| | |
|---|---|
| **File / section** | Portal → Body Measurements |
| **Category** | MANUFACTURER STANDARD |
| **Previous** | No sleeve length point of measure anywhere in the package |
| **New** | Row added: `Sleeve Length — Per the agreed factory pattern / production reference as confirmed with SteelStag; please record the measured value and return it to SteelStag` |
| **Reason** | Sleeve length is not derivable from armhole drop and sleeve opening. It was omitted from the written spec, but the garment is in production, so the agreed factory pattern already carries the value. Publishing an invented number would contradict what is being made. |
| **Production impact** | None — the agreed production reference is unchanged and remains the standard |
| **Factory action** | Measure the sleeve length on the current production reference and send it to SteelStag, so it can be written into the spec for SS2027. |
| **Affects goods in production** | **No** |

---

### R-05 · Measuring method clarified

| | |
|---|---|
| **File / section** | Portal → Body Measurements |
| **Category** | CLARIFICATION / MANUFACTURER STANDARD |
| **Previous** | Quality Standards said `Follow Tech Pack tolerance table. Do not assume if unclear.` — but the Tech Pack contains no flats and no point-of-measure diagram |
| **New** | Callout added: standard industry points of measure, garment laid flat; where a POM is not illustrated, manufacturer standard practice applies and the agreed factory pattern / production reference as confirmed with SteelStag is the controlling physical standard |
| **Reason** | The package told the factory not to assume while giving them nothing to check against. Measuring method is normal manufacturer practice and does not need to be SteelStag-controlled; the agreed production reference resolves anything ambiguous. |
| **Production impact** | None |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-06 · V-neck V-Point Depth datum clarified — values unchanged

| | |
|---|---|
| **File / section** | Portal → Neck Measurements (ST-VN-003) |
| **Category** | CLARIFICATION |
| **Previous** | `Front Neck Drop` and `V-Point Depth` listed at identical values (3½ / 3¾ / 4 / 4¼) with no measuring datum stated |
| **New** | Values **unchanged**. Callout added: measure both as already agreed with SteelStag for this run; the agreed factory pattern / production reference governs; no change to the V-neck block is authorised under v1.3 |
| **Reason** | The two POMs are normally measured from different datums, so identical values are ambiguous on paper. The V-neck is in production — changing either value now would change the garment. The agreed production reference already resolves it. |
| **Production impact** | None — explicitly no block change |
| **Factory action** | Continue to the agreed production reference. |
| **Affects goods in production** | **No** |

---

### R-07 · Pantone TCX numbers published as readable text

| | |
|---|---|
| **File / section** | Portal → Color Standards |
| **Category** | SPECIFICATION CORRECTION |
| **Previous** | Pantone codes existed only in HTML `alt` attributes (which do not print) and as ~4 pt type inside thumbnail images. The Tech Pack PDF contained the string `19-0303` zero times. The README that listed them was not in the ZIP. |
| **New** | A colour table now prints in the Tech Pack: Jet Black 19-0303 TCX · Bright White 11-0601 TCX · Seaport Teal 17-5126 TCX · Wild Ginger 15-1157 TCX · Brown Sugar 18-1048 TCX. Requirement callout now states that the Pantone number is the standard and the cards are indicative only. |
| **Reason** | The colour standard was not legibly recoverable from the primary specification document. |
| **Production impact** | None — the Pantone numbers themselves are unchanged, so any lab dip already submitted or agreed is unaffected |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-08 · Label finished sizes, bleed and print method published

| | |
|---|---|
| **File / section** | Portal → Labels & Branding; `README.txt`; `label-viewer.html` |
| **Category** | SPECIFICATION CORRECTION |
| **Previous** | No label dimension appeared anywhere in the delivered package. README pointed to "the techpack (Section 7)" — the Tech Pack has no numbered sections and no label dimensions. Real sizes existed only in the render script and in `label-viewer.html`, neither of which shipped in the ZIP. |
| **New** | Published in the Tech Pack, the README and the viewer: Neck Label **50 × 30 mm artwork area**, Wash Care **40 × 60 mm trim**, Hang Tag **50 × 85 mm trim**, Size Sticker **30 mm circle trim**. Print method added per item. Bleed is specified only where the item is physically trimmed or die-cut — see R-10. |
| **Reason** | Trims could not be ordered or printed to the correct size from the package as issued. |
| **Production impact** | Trim printing only |
| **Factory action** | Order and print trims to these finished sizes. |
| **Affects goods in production** | **No** — garments are unaffected; trims had not been printed |

---

### R-09 · Label PNG resolution corrected in filenames and metadata

| | |
|---|---|
| **File / section** | `02-Labels/**`; `render-labels-win.py` |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | Files named `*-300dpi.png` were rendered at **384 DPI** and carried **no DPI metadata at all** (no `pHYs` chunk). Placed at the stated 300 DPI, every label printed **28% oversize** — a 50 mm neck label would come out at 71.5 mm. |
| **New** | Files renamed `*-384dpi.png` and every PNG now carries a correct 384 DPI `pHYs` chunk. Resolution itself is unchanged. |
| **Reason** | The filename asserted a resolution the file did not have, and nothing in the file corrected it. |
| **Production impact** | Trim printing only |
| **Factory action** | Use the v1.3 files. Prefer `SteelStag-Labels-PrintReady-v1.3.pdf`, which is sized correctly regardless of placement settings. |
| **Affects goods in production** | **No** |

---

### R-10 · Label artwork now bleeds past the trim line

| | |
|---|---|
| **File / section** | `02-Labels/Hang-Tags/*`, `02-Labels/Size-Stickers/*`, `02-Labels/Wash-Care/*`, `02-Labels/Neck-Labels/*`; `render-labels-win.py` |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | 3 mm bleed was declared and crop marks were drawn, but no artwork extended into it. Measured on the released hang tag: black ink spanned exactly the 50 mm trim width, leaving a 2.91 mm **unprinted white margin** all round. Same on the die-cut size stickers. |
| **New** | On the three items that are physically cut — wash care label, both hang tags, size stickers — the background now runs to the canvas edge (measured: ink at x = 0 and x = W−1), giving 3.02–3.12 mm of real bleed per edge. Size stickers are now a 36 mm circle with the 30 mm die line marked. Crop-mark colour switches to light on dark grounds so it stays visible on the near-black tags.<br><br>**The neck label is excluded.** It is applied to the garment and nothing is trimmed, so it now renders at exactly its **50 × 30 mm artwork area with no bleed and no crop marks** — see R-32. The earlier v1.3 draft gave it a bleed and crop marks it does not need, which would have transferred printed crop marks onto the garment. |
| **Reason** | On a near-black hang tag, any cutting drift outward produced a white sliver — a visible reject class across 1,200 tags. |
| **Production impact** | Trim printing only |
| **Factory action** | Print from v1.3 artwork only. Destroy any earlier hang tag or sticker files. |
| **Affects goods in production** | **No** |

*Bleed and crop marks exist to survive a cutting operation. Where there is no cutting operation there is no bleed and no marks — dimensions and placement for the neck label live in the Tech Pack Labels table and in `label-viewer.html`, not in the production artwork.*

---

### R-11 · Care symbol corrected — tumble dry

| | |
|---|---|
| **File / section** | Wash Care Label and Hang Tag Back care symbol row |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | Third symbol drawn as **two concentric circles**. Under ISO 3758 a bare circle is the *dry-cleaning* symbol — so the row simultaneously showed "dry clean" (symbol 3) and "do not dry clean" (symbol 5). The intended meaning was tumble dry, which requires a **square** containing a circle. |
| **New** | Redrawn as a square containing a circle, crossed through = **do not tumble dry** (ISO 3758) |
| **Reason** | The symbol was not a valid care symbol for the meaning intended, and contradicted the symbol beside it. |
| **Production impact** | Trim printing only |
| **Factory action** | Print from v1.3 artwork only. |
| **Affects goods in production** | **No** |

---

### R-12 · Care symbol corrected — ironing

| | |
|---|---|
| **File / section** | Wash Care Label and Hang Tag Back care symbol row |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | Iron symbol was **crossed through** (do not iron) on a label whose own printed text read `IRON ON REVERSE` |
| **New** | Cross removed — plain iron symbol, ironing permitted. Temperature dots deliberately not added (see **OD-02**). |
| **Reason** | The symbol contradicted the printed instruction on the same label. The text is consistent across both artworks, so the symbol was the error. |
| **Production impact** | Trim printing only |
| **Factory action** | Print from v1.3 artwork only. |
| **Affects goods in production** | **No** |

---

### R-13 · Care text harmonised across both artworks

| | |
|---|---|
| **File / section** | Wash Care Label; Hang Tag Back |
| **Category** | SPECIFICATION CORRECTION |
| **Previous** | Wash Care Label: `Do not bleach / Wash dark colors separately / Iron on reverse` (no drying instruction). Hang Tag Back: the same three plus `Do not tumble dry`. The two care statements on one garment did not match. |
| **New** | Both now read: `Do not bleach / Wash dark colors separately / Iron on reverse / Do not tumble dry` |
| **Reason** | Harmonised to the existing, stricter SteelStag-authored statement rather than inventing a new one. Both artworks now carry an identical care set, and the symbol row matches the text on each. |
| **Production impact** | Trim printing only |
| **Factory action** | Print from v1.3 artwork only. |
| **Affects goods in production** | **No** |

---

### R-14 · Neck label print method stated

| | |
|---|---|
| **File / section** | Portal → Labels & Branding |
| **Category** | CLARIFICATION |
| **Previous** | Portal stated only `Size-specific S / M / L / XL`. The one statement of print method — `transparent bg, DTG print` — was in the README, which did not ship in the ZIP. A superseded internal document said `Woven / printed`, a third answer. |
| **New** | Portal states: `Applied to garment · print/transfer method as per manufacturer standard, subject to approved appearance, adhesion and wash durability · transparent-background artwork · size-specific S / M / L / XL` |
| **Reason** | The package named three different methods across three documents. Naming one specific technology (DTG) would over-specify a decision the factory is better placed to make; what SteelStag controls is the outcome — appearance, adhesion and wash durability — so that is what the spec now states. |
| **Production impact** | Trim / decoration only |
| **Factory action** | Confirm the neck print method at the trim approval stage. See **OD-03** for the Bright White contrast question. |
| **Affects goods in production** | **No** |

---

### R-15 · Wash care label type decided

| | |
|---|---|
| **File / section** | Portal → Labels & Branding |
| **Category** | CLARIFICATION / MANUFACTURER STANDARD |
| **Previous** | `Printed / woven as supplied` — an unresolvable choice, since only single-sided printed artwork exists and a woven label needs different artwork and a fold allowance |
| **New** | `Printed label, as supplied · substrate and attachment per manufacturer standard` |
| **Reason** | Only one artwork type was ever supplied. Substrate and attachment are normal manufacturer decisions. |
| **Production impact** | Trim only |
| **Factory action** | Confirm substrate at trim approval. |
| **Affects goods in production** | **No** |

---

### R-16 · Hang tag attachment handed to manufacturer standard

| | |
|---|---|
| **File / section** | Portal → Labels & Branding |
| **Category** | MANUFACTURER STANDARD |
| **Previous** | `Double-sided printed tag with cord` · placement `Left side seam` — no height, no card stock, no cord type. A superseded document said `attached with thread`, contradicting `with cord`. |
| **New** | `Double-sided printed tag · card stock, cord and attachment per manufacturer standard` · placement `Left side seam · height per manufacturer standard` |
| **Reason** | Tag attachment height and hardware are normal manufacturer practice and do not need SteelStag control. The artwork and finished size are controlled; the attachment is not. |
| **Production impact** | Finishing only |
| **Factory action** | Attach to manufacturer standard. |
| **Affects goods in production** | **No** |

---

### R-17 · Pouch folding instruction corrected for the 24 × 34 cm pouch

| | |
|---|---|
| **File / section** | Portal → Packaging |
| **Category** | SPECIFICATION CORRECTION / MANUFACTURER STANDARD |
| **Previous** | `Folding: Standard retail fold · approx. 28 cm × 20 cm` — carried over unchanged from v1.0, when the pouch was **32 × 40 cm** |
| **New** | `Folding: Manufacturer-standard retail fold sized to suit the approved 24 × 34 cm pouch` |
| **Reason** | The pouch size change to 24 × 34 cm was intentional; the dependent folding instruction was simply never updated and remained sized to the superseded 32 × 40 cm pouch. A 20 × 28 cm fold can physically fit a 24 × 34 cm pouch when correctly oriented, so this is not a fit failure — it is the removal of an unnecessarily prescriptive, stale instruction. An exact fold size does not need to be SteelStag-controlled; the requirement is that the folded garment presents well in the approved pouch. |
| **Production impact** | **Packaging change only. No garment fit or construction impact.** |
| **Factory action** | Fold to manufacturer standard for the approved 24 × 34 cm pouch. |
| **Affects goods in production** | **No** — garments already sewn are packed normally |

---

### R-18 · Pouch mockup marked as a visual reference, not print artwork

| | |
|---|---|
| **File / section** | `04-ColorReference/Packaging-Pouch-Mockup.png`; Portal → Packaging |
| **Category** | CLARIFICATION / ARTWORK CORRECTION |
| **Previous** | The mockup was presented as the packaging artwork and its generator described it as "print-ready at true 240 × 340 mm". Measured, the pouch graphic occupies only **209.5 × 310.8 mm** inside the canvas, sitting on a grey mockup background, in RGB, with no gusset, back panel, seal zone, bleed or dieline. |
| **New** | The image now carries a printed status stamp — `VISUAL REFERENCE ONLY — NOT PRINT ARTWORK · POUCH 24 × 34 cm · DIELINE BY CONVERTER`. The Tech Pack packaging table gains a `Print Artwork` row saying the dieline is produced by the converter to manufacturer standard. |
| **Reason** | Sent to a converter as artwork, the file would have produced an undersized pouch with a grey field printed on it. Pouch tooling is normal converter practice. |
| **Production impact** | Packaging only |
| **Factory action** | Have the converter produce the dieline from the 24 × 34 cm size and the two-tone layout. |
| **Affects goods in production** | **No** |

---

### R-19 · Kraft colour in the mockup corrected to the specified hex

| | |
|---|---|
| **File / section** | `generate_color_assets.py`; `Packaging-Pouch-Mockup.png` |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | Spec: `top 65% natural kraft (#C8A96E)`. Artwork actually rendered `#C4A882` (sampled from the delivered PNG). |
| **New** | Artwork corrected to `#C8A96E`, matching the Tech Pack. Verified by pixel sample. The black band was already correct at `#1A1A1A`. |
| **Reason** | Artwork aligned to the stated specification rather than the other way round, since the spec value is the SteelStag-authored one. |
| **Production impact** | Packaging only |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-20 · Master carton spec completed to manufacturer standard

| | |
|---|---|
| **File / section** | Portal → Packaging → Master Carton |
| **Category** | MANUFACTURER STANDARD |
| **Previous** | `Qty per Carton 100 pcs` and `Max Carton Weight 18 kg` were both stated as absolutes with no garment weight given anywhere, so the factory could not verify that 100 pcs stayed under 18 kg. No carton dimensions, no packing rule, no carton marking. |
| **New** | `Max 100 pcs, or 18 kg gross — whichever is reached first`; carton dimensions per manufacturer standard export packing; `Packing: per manufacturer standard export packing, maintaining SKU-wise quantities and a carton-wise packing list`; `Carton Marking: Brand · Style Code · Colour · Size · Qty · PO No.` |
| **Reason** | Removes an unverifiable conflict without inventing a garment weight. Carton construction, dimensions and the packing arrangement are normal manufacturer practice; what SteelStag needs is traceability, so the requirement is stated as SKU-wise quantities plus a carton-wise packing list rather than a prescribed carton composition. Marking fields restored from the earlier SteelStag packing spec. |
| **Production impact** | Packing only |
| **Factory action** | Pack to manufacturer standard within these limits. |
| **Affects goods in production** | **No** |

---

### R-21 · Logo AI deliverable validated — artwork preserved unchanged

| | |
|---|---|
| **File / section** | `03-Logo/`; `manufacturer/assets/` |
| **Category** | ADMIN / VERSIONING (file format only — **not** an artwork change) |
| **Previous** | The approved SteelStag vector artwork was supplied in a file carrying an `.ai` extension whose internal format was not a native Illustrator working file — verified by signature as PDF 1.5 written by Inkscape 1.4 / cairo 1.18.4, with no Illustrator private data. |
| **New** | **The approved vector artwork is preserved exactly — no shape, antler, typography, proportion, metallic treatment or appearance change of any kind.** It is supplied as `SteelStag-Logo.svg`, `SteelStag-Logo.pdf` and, since R-40, `SteelStag-Logo.ai`. |
| **Reason** | Two separate questions were conflated. **(A) Is the artwork approved and correct?** Yes — it is the owner-approved mark and is preserved untouched. **(B) Is the file format suitable for a manufacturer who specifically asked for Adobe Illustrator `.ai`?** No, and that is a real gap. This entry addresses (B) only. This is a format correction, not a logo redesign. |
| **Superseded by R-40** | The `.ai` is now supplied, built from this same artwork and verified against it. See R-40 for what it is and the one limitation that is disclosed with it. |
| **Production impact** | None |
| **Factory action** | Use the supplied v1.3 vector artwork (`.ai` / `.svg` / `.pdf`) for print production. |
| **Affects goods in production** | **No** |

---

### R-22 · Logo asset hierarchy published

| | |
|---|---|
| **File / section** | `README.txt` → 03-Logo; Portal → Labels & Branding → Logo Assets |
| **Category** | CLARIFICATION |
| **Previous** | Four logo files shipped with no statement of which to use for what. |
| **New** | The package now publishes one hierarchy, and states that **all formats are the same approved SteelStag artwork**:<br><br>**Production vector** — `SteelStag-Logo.svg`, `SteelStag-Logo.pdf` (and the `.ai` once produced, per R-21 / OD-07). Use for print production, scaling and tooling.<br>**Raster / preview** — `SteelStag-Logo-Transparent.png`, `SteelStag-Logo-Dark.png`. High-resolution masters.<br><br>An earlier v1.3 draft of this entry named the PNG as the single master and described the vector as a traced approximation to be avoided. **That is withdrawn.** The vector is approved artwork and is the correct asset for print production. |
| **Measured agreement between formats** | Rendered at matched scale and compared: **SVG vs PDF** — silhouette differs 0.35%, mean tonal delta 1.5/255 (i.e. the same file in two formats). **Vector vs PNG master** — silhouette differs 1.9%, mean tonal delta 5.7/255, mean grey 29.0 vs 33.5. At 1:1 the three assets read as the same mark with the same proportions and the same metallic treatment; the vector renders very slightly darker. The differences are visible only at high magnification. No asset is defective and none is being replaced. |
| **Reason** | The manufacturer specifically asked for vector artwork for print production. Directing them to a raster instead would have been wrong. |
| **Production impact** | None |
| **Factory action** | Use the vector for print production; use the PNG masters where a raster is wanted. Do not alter, stretch, recolour or re-typeset the mark in any format. |
| **Affects goods in production** | **No** |

---

### R-23 · Colour reference cards — CMYK values no longer clipped

| | |
|---|---|
| **File / section** | `04-ColorReference/01..05-*.png`; `generate_color_assets.py` |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | On all five cards the CMYK row was drawn under the footer bar and cut in half — the label printed, the numbers did not. |
| **New** | Row pitch tightened from 64 px to 52 px. All four spec rows (Pantone, HEX, RGB, CMYK) now render clear of the footer on every card. |
| **Reason** | A quarter of the printed colour data was unreadable. |
| **Production impact** | None — Pantone remains the standard; the cards are indicative only |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-24 · Pouch mockup DPI tag corrected

| | |
|---|---|
| **File / section** | `generate_color_assets.py` |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | Image generated at 320 DPI but tagged `321` DPI, so it opened at 239.3 × 338.9 mm instead of 240 × 340 mm |
| **New** | Tagged with the true `POUCH_DPI` (320). Verified: 3024 × 4283 px at 320 DPI = 240.0 × 340.0 mm. |
| **Reason** | Metadata did not match the file. |
| **Production impact** | None (reference image) |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-25 · Package contents completed and structure aligned to the README

| | |
|---|---|
| **File / section** | `SteelStag-CompleteManufacturerPackage-SS2026-v1.3.zip` |
| **Category** | ADMIN / VERSIONING |
| **Previous** | The v1.2 ZIP was assembled by hand and had drifted from the README: **no README, no revision history, only 1 of 4 neck labels, none of the 4 size stickers, no dark logo, no label viewer**, and a flat `downloads/ + assets/` layout that did not match the four-folder structure the README described. |
| **New** | The ZIP now mirrors the pack folder exactly (`README.txt`, revision history, `label-viewer.html`, `01-TechPack/`, `02-Labels/`, `03-Logo/`, `04-ColorReference/`) and contains **all 27 manifest files**, including every neck label and every size sticker. |
| **Reason** | The factory's download did not contain files the README told them to use. |
| **Production impact** | Trim printing — the missing files are now available |
| **Factory action** | Re-download the v1.3 package. |
| **Affects goods in production** | **No** |

---

### R-26 · Package build automated with a verified manifest

| | |
|---|---|
| **File / section** | `build_package.py` (new) |
| **Category** | ADMIN / VERSIONING |
| **Previous** | No build script existed. The ZIP was assembled by hand, which is how R-25 happened. |
| **New** | `build_package.py` zips a declared 27-file manifest, fails the build if any file is missing, verifies every file's real signature against its extension, syncs the portal's display assets from the same source, removes superseded ZIPs, and re-opens the built archive to confirm every entry is byte-identical to its source. |
| **Reason** | Prevents silent package drift from recurring. |
| **Production impact** | None |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-27 · Released artwork brought under version control

| | |
|---|---|
| **File / section** | `.gitignore` |
| **Category** | ADMIN / VERSIONING |
| **Previous** | `02-Labels/**/*.png` and `04-ColorReference/*.png` were git-ignored — the artwork that ships to the factory had no history and could not be diffed between revisions |
| **New** | Both patterns removed; the released package ZIP is also tracked |
| **Reason** | Released artwork is a deliverable. Without history there is no way to prove which artwork a given revision shipped. |
| **Production impact** | None |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-28 · Legacy Tech Pack generator refactored into current-order configuration and reusable style definitions

| | |
|---|---|
| **File / section** | `steelstag_styles.py` (new); `archive/generate_techpack_docx_SUPERSEDED.py`; `verify_release.py` |
| **Category** | ADMIN / VERSIONING |
| **Previous** | A live DOCX generator mixed three separate things in one file: reusable style definitions, the current order's scope, and its own drifted copies of global specifications — `Tolerance ±0.5"` (Tech Pack says ±¼"), pouch `top 45% kraft / bottom 55% black` with a `dark top band` (Tech Pack says 65/35), size sticker `on polybag outside`, hang tag `attached with thread` (Tech Pack says cord). Because it had no way to express *developed but not in this order*, it emitted **ST-DS-002 Deep Scoop** alongside the two styles actually being produced. It had been edited as recently as the 180 GSM bump, so it looked maintained. |
| **New** | Split into two things that were previously tangled:<br><br>**`STYLE_LIBRARY`** — permanent, reusable style definitions. **ST-DS-002 Deep Scoop is retained here in full**, with its neck measurements and construction preserved exactly as developed, marked inactive for SS2026 and available to any future collection that switches it back on.<br>**`COLLECTIONS['SS2026']`** — the current order's scope: `active_styles = ['ST-RN-001', 'ST-VN-003']`.<br><br>The configuration is load-bearing, not decorative: `verify_release.py` fails the release if the shipped Tech Pack mentions a style that is not active for the collection being released. The superseded generator is kept in `archive/` with a header pointing at the library; the portal remains the sole Tech Pack source. |
| **Reason** | Deep Scoop is **not discontinued** — it is simply not part of the SS2026 bulk order, and the owner intends to use it in a future collection. Deleting the style would have thrown away completed pattern work; leaving it in the generator kept shipping a third style nobody ordered. Separating the style library from the order scope solves both, and removes the stale global specifications along with it. |
| **Production impact** | None — the generator was not the source of any released file |
| **Factory action** | None. Produce the two SS2026 styles only: ST-RN-001 and ST-VN-003. |
| **Affects goods in production** | **No** |

---

### R-31 · Pre-treatment requirement recorded explicitly

| | |
|---|---|
| **File / section** | Portal → Product Specifications → Fabric; `README.txt` → Key Specifications |
| **Category** | CLARIFICATION |
| **Previous** | `Pre-treatment — Pre-washed and pre-shrunk` (no stage stated) |
| **New** | `Pre-treatment — Fabric to be pre-washed / pre-shrunk before cutting` |
| **Reason** | This requirement was already communicated to the manufacturer and is already being followed. It is written down here so it survives in the document rather than only in correspondence. **This is not a new v1.3 garment change** — no process, fabric or construction requirement has been added or altered. |
| **Production impact** | None — records an existing, already-communicated requirement |
| **Factory action** | None — continue as already agreed |
| **Affects goods in production** | **No** |

---

### R-32 · Neck-label artwork no longer clipped at the artwork boundary

| | |
|---|---|
| **File / section** | `02-Labels/Neck-Labels/*`; `render-labels-win.py` |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | The neck-label content stack was taller than the 50 × 30 mm artwork area and was clipped by it — measured, the artwork touched the top edge at 0.00 mm margin, cutting the antler tips and the bottom of the size character. In the pre-v1.3 files the surrounding bleed border made this read as intentional whitespace. |
| **New** | Logo width 85 → 78 px, padding 8 → 6 px, gap 5 → 4 px. Measured margins are now 0.99 mm top / 1.32 mm bottom inside the 50 × 30 mm area, with the full mark and the size character intact. Layout, proportion and content are otherwise unchanged. |
| **Reason** | The supplied neck-label artwork was cropping the brand mark. Found while removing the neck label's unnecessary bleed (R-10); the clipping was pre-existing, not introduced by v1.3. |
| **Production impact** | Trim / decoration only |
| **Factory action** | Print from the v1.3 files only. |
| **Affects goods in production** | **No** — no neck labels had been printed |

---

### R-33 · Retail declaration panel added to the pouch specification

| | |
|---|---|
| **File / section** | Portal → Packaging → Retail Declaration Panel; `README.txt`; `Packaging-Pouch-Mockup.png` |
| **Category** | SPECIFICATION CORRECTION |
| **Previous** | The retail pouch carried no declaration panel at all — no MRP, no manufacturer/packer identification, no consumer-care contact, no packing date. Raised by the audit as an owner decision (OD-01) with nothing in the package to act on. |
| **New** | The panel is now **specified and laid out on the back artwork**, with its fields, placement, print treatment and legibility requirement defined. The artwork carries visible placeholder tokens: `MRP ₹ [ MRP ] (incl. of all taxes)`, `[ MANUFACTURER / PACKER — LEGAL NAME & FULL ADDRESS ]`, `[ MARKETED BY — LEGAL NAME & ADDRESS, IF APPLICABLE ]`, `CONSUMER CARE [ PHONE ]`, `MFG [ MM/YYYY ]  PKD [ MM/YYYY ]`, `SIZE [ S / M / L / XL ]  NET QTY [ 1 N ]`, plus a reserved `[ BARCODE AREA ]`. The back mockup shows the panel boxed and headed `RETAIL DECLARATION PANEL — VALUES PENDING (OD-01)`, and its status stamp reads `BACK · DECLARATION VALUES PENDING — DO NOT PRINT`. The front carries none of it — see R-36. |
| **Reason** | Resolves the structure of OD-01 without inventing any value SteelStag has not supplied. The converter can now lay out and cost the panel, and there is a defined place for the values to land — but nothing can be printed with a placeholder in it. |
| **Values still outstanding** | MRP · manufacturer/packer legal name and full address · marketed-by details if applicable · consumer-care phone · MFG and PKD month/year · size and net quantity · barcode symbology and number. SteelStag issues these in writing. |
| **Production impact** | **Bulk pouch printing remains blocked** until the four values are issued. Nothing else is affected. |
| **Factory action** | Do not print production pouches. Do not substitute your own values. If prepress or the converter believes a further declaration is legally required for the destination market, raise it with SteelStag before tooling. |
| **Affects goods in production** | **No** — garment production and all garment trims are unaffected |

---

### R-34 · TOP sample requirement removed in favour of final random production QC

| | |
|---|---|
| **File / section** | Portal → Production Workflow; `README.txt` → Sampling and Approval |
| **Category** | SPECIFICATION CORRECTION |
| **Previous** | A TOP (top-of-production) stage requiring **2 pcs per style × per colour from the first bulk roll** appeared in the old README and the superseded DOCX generator, but not in the Tech Pack workflow. On 2 styles × 5 colours that is 20 pieces the factory may or may not have quoted, and the two documents disagreed. Raised as OD-04. |
| **New** | TOP is **not required for SS2026**. The workflow carries an explicit note saying so, and the Final Inspection stage now reads `Final random production QC — random sampling across finished production to AQL 2.5, plus measurement audit and shade check`. |
| **Reason** | Bulk production is already running, so a first-bulk-roll TOP submission no longer serves its purpose. Random sampling across finished production gives better coverage of the actual run than two pieces pulled from the front of it, and it is what the Tech Pack already specified at final inspection. This closes OD-04 rather than leaving the two documents in disagreement. |
| **Production impact** | Removes a sampling requirement. No garment change. |
| **Factory action** | Do not submit TOP samples. Final random production QC applies. |
| **Affects goods in production** | **No** |

---

### R-35 · Final artwork handoff gated on the native Illustrator file

| | |
|---|---|
| **File / section** | `build_package.py`; `README.txt` → 03-Logo |
| **Category** | ADMIN / VERSIONING |
| **Previous** | The missing native `.ai` (R-21) was recorded as an open item but nothing prevented the package being issued as final without it. |
| **New** | `build_package.py` now carries a `HANDOFF_REQUIRED` set. The build still runs and stays fully verifiable without the `.ai` — so garment production is never held up — but the package is reported as **INTERIM**, and `--final` exits non-zero. `.ai` is also added to the signature check (`%PDF` or `%!PS` accepted; a renamed PNG or SVG is not) and is appended to the shipped manifest automatically once the real file appears. |
| **Reason** | OD-07 blocks the **final manufacturer artwork handoff**, not garment production. The build now enforces exactly that distinction instead of relying on someone remembering it. |
| **Production impact** | None on garments. The package must not be committed or deployed as the final handoff until the `.ai` is added and the package rebuilt. |
| **Factory action** | None. |
| **Affects goods in production** | **No** |

---

### R-36 · Pouch split into front and back artboards; declaration panel moved to the back

| | |
|---|---|
| **File / section** | `04-ColorReference/Packaging-Pouch-Front-Mockup.png` and `-Back-Mockup.png`; `generate_color_assets.py`; Portal → Packaging; `README.txt` |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | One pouch artboard. The Tech Pack specified the declaration panel on the reverse (R-33), but the artwork drew it on the **front**, on the dark band — the artwork and the specification disagreed, and the front carried MRP and legal type. |
| **New** | Two artboards.<br><br>**Front** — brand only: stag mark, wordmark, tagline, and the fabric / GSM / origin line. **No MRP, no legal declaration panel, no legal type of any kind.**<br>**Back** — the Retail Declaration Panel on the kraft ground (where the spec already required single-colour legal type for legibility), with all seven field groups plus a reserved white barcode box, over a clean dark band carrying only the brand line. |
| **Reason** | The front is the shelf face and stays brand-led. Legal declarations belong on the back, which is also what the Tech Pack had specified all along — this brings the artwork into line with its own specification. Declaration fields and the print-blocking logic are unchanged; only placement moved. |
| **Production impact** | Packaging artwork only. **Bulk pouch printing remains blocked** under OD-01 until the values are issued. |
| **Factory action** | Give the converter both artboards. The panel must appear on the back only. |
| **Affects goods in production** | **No** |

---

### R-37 · Marketed-by entity populated from the company's statutory records

| | |
|---|---|
| **File / section** | Portal → Packaging → Retail Declaration Panel; `Packaging-Pouch-Back-Mockup.png`; `README.txt` |
| **Category** | SPECIFICATION CORRECTION |
| **Previous** | Every declaration field was a placeholder, including the marketed-by entity. |
| **New** | The marketed-by line is now **confirmed and printed solid** (no brackets) on the back artwork:<br><br>`MARKETED BY  ANAISHU LIFESTYLE PRIVATE LIMITED`<br>`A-406, 4th Floor, D. Chowdhary Madhusudan Complex,`<br>`Dimna Chowk, Mango, Jamshedpur,`<br>`East Singhbhum, Jharkhand 831018, India`<br><br>The consumer-care **email** `hello@steelstag.in` is also now printed; the telephone number remains a placeholder. |
| **Source** | GST Registration Certificate (Form GST REG-06), GSTIN **20ABECA6206E1ZE**, legal name and principal place of business as registered. The company's own master index directs that GST-certificate wording is used for address matching, so that wording is what appears on the pack. |
| **Not filled, and why** | **MRP** — not yet set; the manufacturer quotation and landed-cost calculation are still outstanding. **Manufacturer / packer** — see R-38. **Consumer-care telephone** — no company telephone number appears in the corporate records; a number must be designated. **MFG / PKD** — set at packing. **Net quantity** — not documented. **Barcode** — conditional, see below. |
| **Barcode** | Downgraded from *pending* to *conditional*. The company's plan is to seek an Amazon GTIN exemption before buying a GS1 prefix, so a GTIN may never be issued. The reserved box now reads *include only if a GTIN is used*. |
| **Production impact** | **Bulk pouch printing remains blocked.** One field of several is now final. |
| **Factory action** | None yet. Do not print. |
| **Affects goods in production** | **No** |

---

### R-38 · Manufacturer / packer line raised with the factory for written confirmation

| | |
|---|---|
| **File / section** | Portal → Packaging → Retail Declaration Panel; `README.txt` |
| **Category** | CLARIFICATION |
| **Previous** | `[ MANUFACTURER / PACKER — LEGAL NAME & FULL ADDRESS ]` with no indication of who that is or how it gets filled. |
| **New** | The panel now names **Rajlakshmi Cotton Mills Pvt. Ltd.** as the understood manufacturer of record and asks the factory to confirm, in writing: (1) the legal entity name exactly as registered; (2) **which premises** actually manufactures and packs this order; (3) the full address wording **as it appears on their GST registration**; (4) whether they are the packer for the pouch or whether packing happens elsewhere. It also states plainly that Anaishu Lifestyle Private Limited is the **marketer** — not the manufacturer or packer — and must not be shown as either. |
| **Why it is not filled** | The identity was taken from the factory's public contact page, which lists a Kolkata head office and **two** factories (Greater Noida, UP 201310 and Domjur, Howrah, WB 711411) and shows no GSTIN. A Legal Metrology declaration must name the entity and premises that actually manufacture and pack the goods. Choosing between two addresses on the factory's behalf, from a website, would be inventing a legal declaration — so the field stays a placeholder until the factory confirms. |
| **Production impact** | **Bulk pouch printing remains blocked** on this field. |
| **Factory action** | **Reply in writing with the four items above.** |
| **Affects goods in production** | **No** |

---

### R-39 · Declarations moved from the pouch artwork to an applied retail sticker

| | |
|---|---|
| **File / section** | `02-Labels/Retail-Sticker/RetailSticker-384dpi.png` (new); labels print-ready PDF p.12; `Packaging-Pouch-Back-Mockup.png`; Portal → Packaging → Retail Declaration Sticker; `README.txt` |
| **Category** | SPECIFICATION CORRECTION / ARTWORK |
| **Previous** | R-33 and R-36 put a large declaration panel into the back-of-pouch artwork, with bracketed placeholder tokens, an `OD-01` heading and a `VALUES PENDING` banner printed on the pouch face. |
| **New** | The panel is removed from the pouch entirely. Declarations are carried on a **70 × 38 mm self-adhesive retail sticker** applied to the back of the pouch, supplied as artwork (+3 mm bleed, 384 DPI, page 12 of the print-ready labels PDF).<br><br>**Fixed content printed on every sticker:** SteelStag · Made in India · Marketed by Anaishu Lifestyle Private Limited with the registered address · Manufactured & Packed by (rule for the confirmed factory wording) · Consumer care hello@steelstag.in · Men's T-Shirt · Net qty 1 N.<br>**Variable per-SKU content, overprinted at packing:** MRP, Size, SKU, Mfd/Pkd, and a barcode in the reserved lower-left area only if a GTIN is issued.<br><br>The sticker artwork carries **no internal codes, no status text and no instructions** — no `OD-01`, no "values pending", no "barcode area", no GTIN guidance. All of that now lives in the Tech Pack specification, where it belongs. The pouch back is brand-clean kraft with the sticker shown applied. |
| **Reason** | MRP, SKU, size and packing date are per-SKU variable data across 40 variants and change over time; printing them into the pouch would mean re-tooling the pouch whenever any of them moved. A sticker is the correct carrier. It also keeps the pouch premium and uncluttered, and separates consumer-facing artwork from internal project language. |
| **Production impact** | **The pouch no longer carries any pending value.** The OD-01 block now applies to the **sticker**, not the pouch. Pouch printing is technically independent of MRP / SKU / date — release is SteelStag's call. |
| **Factory action** | Do not run production stickers until SteelStag issues the MRP, the SKU list and the manufactured-and-packed-by wording in writing. Confirm the four manufacturer items in R-38. |
| **Affects goods in production** | **No** |

---

### R-40 · Adobe Illustrator deliverable supplied

| | |
|---|---|
| **File / section** | `03-Logo/SteelStag-Logo.ai` (new); Portal → Logo Assets; `README.txt` |
| **Category** | ADMIN / VERSIONING |
| **Previous** | R-21 recorded the `.ai` as outstanding because the release machine has no Adobe Illustrator, and SteelStag would not ship a renamed file without disclosure. |
| **New** | `SteelStag-Logo.ai` is supplied. A modern Illustrator file is a PDF container, and this is one — it opens natively in Illustrator with all **25 vector paths editable**, artboard **1005.75 × 911.25 pt**, no embedded raster. |
| **How it was made** | Built from the **same approved vector artwork** as `SteelStag-Logo.svg` and `SteelStag-Logo.pdf`. No re-tracing, no re-export through a raster step, not one coordinate changed. Document metadata stamped; content stream untouched. |
| **Verified** | Rendered and pixel-compared against the approved SVG: silhouette differs **0.35%**, mean tonal delta **1.5/255** — the same figures as SVG-vs-PDF, i.e. rendering noise only. Path count, artboard and raster count all match the approved PDF exactly. The release gate re-checks every one of these on each build. |
| **Disclosed limitation** | It does **not** carry Adobe's proprietary private-data stream — only Illustrator itself can write that. Illustrator generates it on first save. If prepress specifically requires a CC-native document, opening and re-saving once is sufficient; no artwork changes. This is stated in the README and in the Tech Pack, not left for the factory to discover. |
| **Why this and not a legacy PostScript `.ai`** | A genuine AI-8 PostScript file was the alternative, and the artwork would have suited it — 25 flat-filled polygons, no gradients, no curves. It was rejected because **nothing on this machine can rasterise PostScript**, so the file could not have been verified before shipping. An unverifiable artwork file is exactly the class of defect this revision exists to remove. |
| **Production impact** | None on garments. The package is now the **final manufacturer artwork handoff** rather than interim. |
| **Factory action** | Use `SteelStag-Logo.ai` for print production. |
| **Affects goods in production** | **No** |

---

### R-41 · One logo appearance everywhere — brand rule frozen and enforced

| | |
|---|---|
| **File / section** | `03-Logo/*`; `manufacturer/assets/logo.png`; `render-labels-win.py`; `generate_color_assets.py`; Portal → Logo Assets; `README.txt`; `verify_release.py` |
| **Category** | ARTWORK / PRINT CORRECTION |
| **Previous** | Three inconsistencies were measured against `SteelStag-Logo-Transparent.png`:<br>**(a)** `SteelStag-Logo-Dark.png` carried the wordmark 66 px tighter to the stag — gap **0.54%** of mark height against the master's **6.10%**. It was written at 21:36 on 25 Jun, ten minutes before the master at 21:46, and so predates the final `logo gap 70px` fix; it was never re-rendered.<br>**(b)** The pouch front multiplied the mark by `r×0.18 g×0.16 b×0.14`, rendering it at mean ink luminance **35.0** against the master's **132.9**, range crushed to 6–150 from 0–255. The metallic treatment was gone; it read as a flat black silhouette.<br>**(c)** Three styled wordmark lockups — wash care label, retail sticker, pouch back — carried no ™, while the portal sidebar, colour swatch cards and hang tag back did. |
| **New** | **(a)** `Logo-Dark` re-rendered from the master by compositing it on black. Same canvas, same position, gap now **6.11%**. No geometry touched.<br>**(b)** The charcoal multiply is **deleted**. The pouch front places the approved master **as-is, directly on the kraft ground, with no backing panel** — measured there, 71% of the mark’s pixels sit darker than the kraft and the highlights still reach 255, so the metallic reads unaided. A dark backing panel was built and reviewed as an alternative and rejected: it introduced a second black block on a front that already carries one, and the bare kraft is the more confident, brand-led composition. The mark is set at the master’s **native width** — as large as it goes before upscaling would soften it — for presence on kraft, and the brand block is centred in the kraft field. The pouch now sizes the mark from its own bounds rather than the master canvas, so clear space can never change the printed size.<br>**(c)** ™ added to all three missing lockups. Plain-text mentions of "SteelStag" in prose are deliberately left alone. |
| **Also** | The master gained **safe clear space**: canvas 1341 × 1215 → **1341 × 1342**, margins now ≥ 80 px on every side (it previously had **zero** bottom clear space, one pixel from clipping the `g` descender and the ™). **The artwork inside is pixel-for-pixel unchanged** — verified by cropping the new canvas back to the old bounds and diffing to an empty bounding box. Canvas width and the mark's horizontal position were deliberately held constant so every consumer that scales by width renders the mark at exactly the same size; the neck label and hang tag absorb the new vertical padding with matching negative margins. Confirmed: the neck label's content bounding box moved by **1 px**. |
| **Brand rule now published** | 1. The approved visual master is `SteelStag-Logo-Transparent.png`; all artwork must visually match it. 2. No recolouring, tinting, multiply, alternate spacing or regenerated geometry — if the mark does not read on a substrate, change what sits around it, not the mark. 3. `Logo-Dark.png` is the same mark on a dark ground, nothing else. 4. `.svg` / `.pdf` / `.ai` are **production derivatives**: same geometry and spacing, simplified 25-band metallic treatment, for processes that genuinely need vector — they must not replace the master in full-colour applications. |
| **Not done, deliberately** | The vector family was **not re-traced.** Re-tracing is what produced the darker rendering in the first place, and each pass drifts further from the master. The tone gap (ink grey 112.0 vs 132.1) is accepted and documented as the derivative's limitation rather than chased. |
| **Enforced** | `verify_release.py` section 14 now checks all of it on every build: master clear space and gap, raster copies byte-identical, Logo-Dark canvas and spacing, vector spacing, absence of any recolour code, pouch highlight range and tone, ™ on all six lockups, and that the rule is published in both the Tech Pack and the README. 24 checks. |
| **Production impact** | Artwork only. Pouch and hang-tag printing should use the v1.3 files. |
| **Factory action** | Use the v1.3 artwork. Discard any earlier logo file. |
| **Affects goods in production** | **No** |

---

### R-29 · Duplicate and stale copies removed

| | |
|---|---|
| **File / section** | `02-Labels/`; `manufacturer/downloads/`; `generate_techpack_pdf.py` |
| **Category** | ADMIN / VERSIONING |
| **Previous** | `AllLabels-PrintReady.pdf` and `SteelStag-Labels-PrintReady.pdf` were byte-identical copies under different names, and the README named only one. The Tech Pack PDF and CSV each existed in two locations that had to be kept in sync by hand. |
| **New** | One labels PDF. `manufacturer/downloads/` now holds only the release ZIP; the pack folder is the single canonical tree, and `generate_techpack_pdf.py` writes one output. |
| **Reason** | Duplicate copies under different names are how the released Labels PDF came to differ from what the committed script produces. |
| **Production impact** | None |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

### R-30 · Revision history published

| | |
|---|---|
| **File / section** | This document; Portal → Revision History |
| **Category** | ADMIN / VERSIONING |
| **Previous** | No revision history existed. The portal and Tech Pack both read `v1.2 · Last updated 25 June 2026` while GSM changed 125 → 160 → 180 and the pouch changed 32 × 40 → 24 × 34 underneath that identity. |
| **New** | This register, plus a summary Revision History section in the portal and therefore in the Tech Pack PDF. The portal now carries `Version 1.3 · Last updated 10 September 2026`. |
| **Reason** | Without it, neither side can prove which specification a quote, lab dip or approval was made against. |
| **Production impact** | None |
| **Factory action** | None |
| **Affects goods in production** | **No** |

---

## Deliberately NOT changed

These were raised by the audit and left alone on purpose, because changing them
would change a garment that is already in production against an agreed pattern.

| Item | Finding | Why unchanged |
|---|---|---|
| Body measurements | All 8 points of measure | In production against the agreed factory pattern. No change authorised. |
| Neck measurements | Both styles | In production against the agreed factory pattern. No change authorised. |
| Measurement tolerance in the Tech Pack | ±¼" | Unchanged — only the stale README copy was corrected (R-03) |
| Grading vs tolerance | Sleeve opening and armhole drop grade ¼" against a ±¼" tolerance; round-neck front neck drop grades ⅛". Adjacent sizes overlap within tolerance, so the measurement audit cannot reliably separate them. | Real, but fixing it means changing either the grade or the tolerance — both are garment changes on an approved, in-production style. Carried to **OD-05** for SS2027. |
| Chest / waist / sweep identical at every size | Straight side seam, no taper | Intentional block design, confirmed by the `½ Sweep (Straight)` label. Not a defect. |
| Style code gap (no ST-*-002) | ST-DS-002 is not in the SS2026 order | Not a gap to close. Deep Scoop keeps its code and is retained in the style library for a future collection (R-28). Renumbering live style codes would be worse than the apparent gap. |
| Fabric, GSM, dyeing, finish, construction, stitch density | — | Unchanged and in production. Pre-treatment wording was made explicit (R-31) but the requirement itself is unchanged and was already communicated. |
| Approved logo artwork | Vector and raster differ slightly in tone (1.9% silhouette, 5.7/255 mean) | The vector is owner-approved artwork. No logo asset is replaced, re-traced or altered in v1.3 — only the asset hierarchy and the missing `.ai` deliverable are addressed (R-21, R-22). |
| ST-DS-002 Deep Scoop style definition | Not part of the SS2026 order | Preserved in full in `steelstag_styles.py` for a future collection (R-28). Not deleted, not discontinued. |
| Quantities | 1,200 pcs; all colour, style and size splits | Verified correct — see below. No change. |

---

## Numerical verification (unchanged at v1.3)

| Check | Result |
|---|---|
| Row sums | 22+53+53+22 = 150 · 19+44+43+19 = 125 · 15+35+35+15 = 100 |
| Colour totals | 300 + 250 + 200 + 200 + 250 = 1,200 |
| Style totals | 600 + 600 = 1,200 |
| Size totals | S 180 · M 422 · L 418 · XL 180 = 1,200 |
| CSV vs Tech Pack | Identical |
| Carton limit | Max 100 pcs or 18 kg gross per carton, whichever comes first — carton count follows from actual packing |

The 1-piece M/L asymmetry at 125 pcs per style is the documented rounding
allowance and is explicitly permitted in either direction.

---

## Open owner decisions

**None of these stops garment production.** One (OD-01) blocks retail-sticker printing and one (OD-03)
blocks Bright White neck labels only. The pouch itself is no longer blocked (R-39), and the
final artwork handoff is no longer blocked (R-40).

| ID | Decision | Blocks | Notes |
|---|---|---|---|
| **OD-01** | Issue the retail sticker values: MRP · the 40-SKU code list · manufactured-and-packed-by wording (factory to confirm, R-38) · barcode only if a GTIN is used | **Retail sticker printing** — no longer the pouch | Declarations now sit on an applied **retail sticker**, not the pouch (R-39). Marketed-by, consumer-care email, commodity, net quantity and country of origin are **final and printed**. Mfd/Pkd is set at packing. What is left: MRP (awaiting the manufacturer quote and landed cost), the 40-SKU code list, the manufactured-and-packed-by wording (R-38), and a barcode only if a GTIN is actually issued. **The pouch carries none of these**, so pouch printing is no longer gated on them. |
| **OD-02** | Ironing temperature on the care label | Nothing | Unchanged. Symbol shows ironing permitted with no temperature dots. If a limit is wanted (2 dots / 150 °C is normal for 100% cotton), say so and the artwork is a one-line change — but decide before the care labels go on press or it is a reprint. |
| **OD-03** | Approve the Bright White neck label from a **physical sample** | **Bright White neck labels only** | One metallic-gradient artwork covers all five colourways. It reads correctly on the four dark grounds. For Bright White, have the factory print/apply a physical sample on the approved Bright White fabric and send it for approval. Judge it on the physical sample, not on screen. If it is rejected, SteelStag supplies a dark variant. The other four colourways proceed now. |
| **OD-05** | Grading vs tolerance for SS2027 | Nothing this season | See "Deliberately NOT changed". |
| **OD-06** | Whether the enzyme wash is a fabric-stage or garment-stage process, and therefore whether the measurement table is pre- or post-wash | Nothing this season | Already resolved in practice on the production floor. Fabric pre-wash / pre-shrink before cutting is now stated explicitly (R-31); the enzyme wash stage is not. Document it for SS2027. |
| **OD-08** | Factory to confirm the run is being measured and QC'd to ±¼" | Nothing — a one-line confirmation | The Tech Pack has said ±¼" since v1.0; only a stale README copy said ±0.5" (R-03). |

### Closed in v1.3

| ID | Was | Resolution |
|---|---|---|
| **OD-04** | Confirm whether TOP samples are required — 2 pcs per style per colour | **Closed.** TOP is not required for SS2026; final random production QC applies instead — see R-34. |
| **OD-07** | Produce the Adobe Illustrator `.ai` deliverable | **Closed.** Supplied as a PDF-container Illustrator file built from the approved artwork and verified against it — see R-40. The one limitation (no Adobe private-data stream until Illustrator re-saves it) is disclosed in the README and the Tech Pack. Handoff status is now READY. |

---

*SteelStag © 2026 — Confidential. For manufacturer use only.*
