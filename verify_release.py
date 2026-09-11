# -*- coding: utf-8 -*-
"""SteelStag SS2026 release gate. Run after build_package.py.

Checks what the v1.2 package got wrong: numerical totals, version consistency
across every artefact, the specific contradictions the audit found, agreement
between the two care artworks, printable artwork geometry / DPI / bleed, real
file signatures rather than extensions, ZIP completeness, and portal-to-pack
cross-references. Exit code 0 = releasable.
"""
import io, os, re, sys, zipfile, subprocess
from pathlib import Path
from PIL import Image, ImageStat

BASE = Path(__file__).parent
PACK = BASE / 'SteelStag-ManufacturerPack-SS2026'
ZIPF = BASE / 'manufacturer' / 'downloads' / 'SteelStag-CompleteManufacturerPackage-SS2026-v1.3.zip'
fails, warns = [], []

def ck(cond, msg):
    print(('  PASS  ' if cond else '  FAIL  ') + msg)
    if not cond: fails.append(msg)

def warn(cond, msg):
    if not cond:
        print('  WARN  ' + msg); warns.append(msg)

def techpack_text(layout=True):
    args = ['pdftotext'] + (['-layout'] if layout else []) + ['-enc', 'UTF-8']
    out = subprocess.run(
        args + [str(PACK / '01-TechPack' / 'SteelStag-TechPack-SS2026-v1.3.pdf'), '-'],
        capture_output=True)
    return out.stdout.decode('utf-8', 'replace').replace(chr(0xa0), ' ')

def flat(txt):
    """Table cells wrap mid-phrase in the PDF, so text checks run against a
    de-hyphenated, whitespace-flattened copy rather than the raw extraction."""
    return ' '.join(re.sub(r'-\s*\n\s*', '-', txt).split())

TP = techpack_text()          # -layout: preserves page/section order
# Presence checks run against the NON-layout extraction: -layout interleaves
# adjacent table columns, which splits a wrapped cell like the marketed-by
# address across unrelated text and makes substring checks lie.
TPF = flat(techpack_text(layout=False))
PORTAL = io.open(BASE / 'manufacturer' / 'index.html', encoding='utf-8').read()
README = io.open(PACK / 'README.txt', encoding='utf-8').read()
CSV = io.open(PACK / '01-TechPack' / 'SteelStag-QuantityBreakdown-SS2026-v1.3.csv', encoding='utf-8').read()

print('\n=== 1. NUMERICAL CONSISTENCY ===')
rows = [r.split(',') for r in CSV.strip().split('\n')[1:] if r.strip()]
data = [r for r in rows if r[0]]
total_row = [r for r in rows if not r[0]][0]
ok_rows = all(sum(int(c) for c in r[4:8]) == int(r[8]) for r in data)
ck(ok_rows, 'CSV: every row S+M+L+XL equals its Style Total')
grand = sum(int(r[8]) for r in data)
ck(grand == 1200, f'CSV: style totals sum to 1,200 (got {grand})')
ck(int(total_row[8]) == 1200, f'CSV: declared total row = 1,200 (got {total_row[8]})')
sizes = [sum(int(r[4 + i]) for r in data) for i in range(4)]
ck(sizes == [180, 422, 418, 180], f'CSV: size totals S/M/L/XL = 180/422/418/180 (got {sizes})')
ck(sum(sizes) == 1200, 'CSV: size totals sum to 1,200')
by_colour = {}
for r in data:
    by_colour[r[3]] = by_colour.get(r[3], 0) + int(r[8])
expect = {'Jet Black': 300, 'Bright White': 250, 'Seaport Teal': 200,
          'Wild Ginger': 200, 'Brown Sugar': 250}
ck(by_colour == expect, f'CSV: colour totals match the Tech Pack table ({by_colour})')
for colour, tot in expect.items():
    ck(re.search(re.escape(colour) + r'.{0,80}?' + f'{tot:,}'.replace(',', ',?') + r' pcs', TP, re.S) is not None
       or f'{tot} pcs' in TP, f'Tech Pack shows {colour} total {tot} pcs')
ck('1,200 pcs' in TP, 'Tech Pack states 1,200 pcs')
ck(TP.count('1,200') >= 2, 'Tech Pack repeats the 1,200 pc total consistently')

print('\n=== 2. VERSION CONSISTENCY ===')
ck('v1.3' in PORTAL and 'v1.2' not in PORTAL.replace('v1.2</td>', 'REVHIST'),
   'Portal carries v1.3 (v1.2 only inside the revision history table)')
ck('Version 1.3' in TP and 'v1.3' in TP, 'Tech Pack PDF states version 1.3 in the document body')
ck('Version 1.3' in TP and '11 September 2026' in TP, 'Tech Pack carries version + release date')
ck('Package Version: v1.3' in README, 'README states v1.3')
for f in ['01-TechPack/SteelStag-TechPack-SS2026-v1.3.pdf',
          '01-TechPack/SteelStag-QuantityBreakdown-SS2026-v1.3.csv',
          '02-Labels/SteelStag-Labels-PrintReady-v1.3.pdf',
          'SteelStag-SS2026-Revision-History-v1.3.md']:
    ck((PACK / f).is_file(), f'v1.3 filename present: {f}')
ck(not list((BASE / 'manufacturer' / 'downloads').glob('*v1.0*'))
   and not list((BASE / 'manufacturer' / 'downloads').glob('*v1.2*')),
   'No v1.0 / v1.2 artefacts left in downloads/')

print('\n=== 3. RESOLVED CONTRADICTIONS ===')
ck('0.5"' not in README and '+/-1/4"' in README, 'README tolerance now +/-1/4" (was +/-0.5")')
ck('Tolerance \u00b1\u00bc"' in PORTAL, 'Portal tolerance unchanged at \u00b1\u00bc"')
ck('28 cm \u00d7 20 cm' not in PORTAL and '28cm' not in PORTAL, 'Stale 28 cm fold removed')
ck('Manufacturer-standard retail fold' in PORTAL and '24 \u00d7 34 cm pouch' in PORTAL,
   'Folding now manufacturer standard for the 24 x 34 cm pouch')
ck('24 cm \u00d7 34 cm' in PORTAL, 'Pouch size still 24 x 34 cm')
for code in ['19-0303', '11-0601', '17-5126', '15-1157', '18-1048']:
    ck(code in TP, f'Pantone {code} is readable text in the Tech Pack')
    ck(code in README, f'Pantone {code} present in README')
ck('50 \u00d7 30 mm' in TP and '40 \u00d7 60 mm' in TP and '50 \u00d7 85 mm' in TP and '30 mm diameter' in TP,
   'All four label finished sizes are stated in the Tech Pack')
ck('3 mm bleed' in TP, 'Tech Pack states the 3 mm bleed')
ck('384 DPI' in TP and '384 DPI' in README, 'True 384 DPI stated in Tech Pack and README')
ck('are 300 DPI' not in README and '300dpi' not in README.replace('as 300 DPI',''),
   'README makes no stale 300 DPI claim (the 300 DPI warning is deliberate)')
spec_part = TP.split('Revision History')[0]
ck('Deep Scoop' not in spec_part and 'DS-002' not in spec_part,
   'Removed style ST-DS-002 appears nowhere in the specification body')
ck(TP.count('Deep Scoop') == TPF.split('Revision History')[-1].count('Deep Scoop'),
   'ST-DS-002 is mentioned only in the revision history, never in the specification body')
ck('Section 7' not in README and 'Section 9' not in README, 'Dangling section references removed')
ck('.docx' not in README, 'README no longer references a non-existent DOCX')
ck('QuantityBreakdown' in README, 'README now documents the quantity CSV')
ck('SteelStag-Logo.svg' in README and 'SteelStag-Logo.pdf' in README
   and 'SteelStag-Logo-Dark.png' in README, 'README documents every logo file')
ck('Revision History' in TP, 'Tech Pack contains the revision history table')
ck('approved in writing' not in TP and 'approved PP sample' not in TP,
   'Tech Pack asserts no unevidenced written approval')
ck('production reference as confirmed' in TP or 'agreed factory pattern' in TP,
   'Tech Pack states the actual production basis')
ck('DTG' not in TPF, 'Neck label no longer over-specifies a print technology')
ck('adhesion and wash durability' in TPF, 'Neck label states the outcome requirement instead')
ck('pre-washed / pre-shrunk before cutting' in TP.lower().replace('  ', ' '),
   'Pre-treatment stage stated explicitly')
ck('solid cartons' not in TPF, 'Prescriptive carton composition removed')
# pdftotext drops the hyphen when a hyphenated word wraps, so compare with
# hyphens removed from both sides.
_nh = lambda s: s.replace('-', '')
ck(_nh('SKU-wise quantities') in _nh(TPF) and _nh('carton-wise packing list') in _nh(TPF),
   'Carton packing stated as manufacturer standard with traceability')
ck('whichever is reached first' in TPF, 'Carton limit is 100 pcs or 18 kg, whichever first')
ck('no bleed and no crop marks' in TPF, 'Tech Pack states the neck label carries no bleed')
ck('no rework' in TP.lower() or 'require no rework' in TP, 'Tech Pack states garments need no rework')

print('\n=== 4. CARE INSTRUCTION CONSISTENCY ===')
R = io.open(BASE / 'render-labels-win.py', encoding='utf-8').read()
ck(R.count('Do not tumble dry \u2014 square with circle, crossed (ISO 3758)') == 2,
   'Both symbol sets use the ISO do-not-tumble-dry glyph')
ck('circle with inner circle' not in R, 'Invalid concentric-circle glyph removed')
ck(R.count('Iron permitted') == 2, 'Both symbol sets show ironing permitted')
ck('Do not iron' not in R, 'Crossed-iron glyph removed')
wash = R.split("name='wash-care-label'")[1].split('),')[0]
tagb = R.split("name='hang-tag-back'")[1].split('),')[0]
for phrase in ['Do not bleach', 'Wash dark colors separately', 'Do not tumble dry']:
    ck(phrase in wash.replace('<br/>', ' ') and phrase in tagb.replace('<br/>', ' '),
       f'Care text "{phrase}" appears on BOTH wash care label and hang tag')
ck('Iron on reverse' in wash and 'Iron on reverse side' in tagb,
   'Both artworks instruct ironing on the reverse (matches the iron symbol)')

print('\n=== 5. PRINTABLE ARTWORK: DIMENSIONS, DPI, BLEED ===')
BLEED_MM, PXMM = 3, 3.7795 * 4
# (trim_w, trim_h, bleed_mm) -- bleed only where the item is physically cut
EXPECT = {
    'Neck-Labels/NeckLabel-%s-384dpi.png': (50, 30, 0),
    'Wash-Care/WashCareLabel-384dpi.png': (40, 60, 3),
    'Hang-Tags/HangTag-Front-384dpi.png': (50, 85, 3),
    'Hang-Tags/HangTag-Back-384dpi.png': (50, 85, 3),
    'Size-Stickers/SizeSticker-%s-384dpi.png': (30, 30, 3),
}
for pat, (w, h, bl) in EXPECT.items():
    for code in (['S', 'M', 'L', 'XL'] if '%s' in pat else [None]):
        rel = pat % code if code else pat
        p = PACK / '02-Labels' / rel
        im = Image.open(p)
        dpi = im.info.get('dpi')
        ck(dpi is not None and abs(dpi[0] - 384) < 1,
           f'{rel}: DPI metadata present and = 384 (got {dpi})')
        mm_w = im.width / (dpi[0] / 25.4)
        mm_h = im.height / (dpi[1] / 25.4)
        # Canvas must never be SHORT of trim + 2x bleed; a small overshoot from
        # rounding the pixel canvas up is fine (it only adds bleed).
        for got, nominal, axis in ((mm_w, w + 2 * bl, 'W'), (mm_h, h + 2 * bl, 'H')):
            ck(nominal <= got <= nominal + 0.35,
               f'{rel}: {axis} places at {got:.2f} mm (needs >= {nominal} mm'
               f'{" = trim + 2x3 mm bleed" if bl else " = artwork area, no bleed"})')
        bleed_w, bleed_h = (mm_w - w) / 2, (mm_h - h) / 2
        ck(bleed_w >= bl and bleed_h >= bl,
           f'{rel}: bleed per edge {bleed_w:.2f} / {bleed_h:.2f} mm (needs >= {bl} mm)')
        rgba = im.convert('RGBA'); y = rgba.height // 2
        left = rgba.getpixel((0, y)); right = rgba.getpixel((rgba.width - 1, y))
        if bl:
            ck(left[3] > 0 and right[3] > 0, f'{rel}: artwork bleeds to the canvas edge')
        else:
            # No trimming -> no bleed and no crop marks. Corners must be empty:
            # a printed crop mark here would transfer onto the garment.
            corners = [rgba.getpixel(p) for p in
                       [(0, 0), (rgba.width - 1, 0), (0, rgba.height - 1), (rgba.width - 1, rgba.height - 1)]]
            ck(all(c[3] == 0 for c in corners),
               f'{rel}: no crop marks / bleed box in the artwork (corners empty)')
            alpha = rgba.split()[3]
            bb = alpha.getbbox()
            ck(bb is not None and bb[0] > 0 and bb[2] < rgba.width,
               f'{rel}: artwork sits inside the artwork area horizontally')

pdf = PACK / '02-Labels' / 'SteelStag-Labels-PrintReady-v1.3.pdf'
raw = pdf.read_bytes()
boxes = []
for m in re.finditer(rb'/MediaBox\s*\[([^\]]*)\]', raw):
    v = [float(x) for x in m.group(1).split()]
    boxes.append((round((v[2] - v[0]) / 72 * 25.4, 1), round((v[3] - v[1]) / 72 * 25.4, 1)))
ck(len(boxes) == 12, f'Labels PDF has 12 pages (got {len(boxes)})')

def count_pages(nom_w, nom_h):
    return sum(1 for bw, bh in boxes
               if nom_w <= bw <= nom_w + 0.35 and nom_h <= bh <= nom_h + 0.35)

ck(count_pages(50, 30) == 4, f'4 neck-label pages at 50 x 30 mm (artwork area, no bleed) — boxes {boxes}')
ck(count_pages(46, 66) == 1, '1 wash-care page at >=46 x 66 mm (40x60 + bleed)')
ck(count_pages(56, 91) == 2, '2 hang-tag pages at >=56 x 91 mm (50x85 + bleed)')
ck(count_pages(36, 36) == 4, '4 size-sticker pages at >=36 x 36 mm (30 dia + bleed)')
ck(count_pages(76, 44) == 1, '1 retail-sticker page at >=76 x 44 mm (70x38 + bleed)')
ck(all(bw >= 36 and bh >= 30 for bw, bh in boxes), 'Every PDF page is at least its trim size')

print('\n=== 6. COLOUR / PACKAGING ARTWORK ===')
for side in ('Front', 'Back'):
    pouch = Image.open(PACK / '04-ColorReference' / f'Packaging-Pouch-{side}-Mockup.png')
    ck(abs(pouch.info['dpi'][0] - 320) < 1,
       f'Pouch {side.lower()} tagged 320 DPI (got {pouch.info["dpi"]})')
    mm = (pouch.width / (pouch.info['dpi'][0] / 25.4),
          pouch.height / (pouch.info['dpi'][1] / 25.4))
    ck(abs(mm[0] - 240) < 0.5 and abs(mm[1] - 340) < 0.5,
       f'Pouch {side.lower()} canvas = 240 x 340 mm (got {mm[0]:.1f} x {mm[1]:.1f})')
    rgb = pouch.convert('RGB')
    # (300, 2600) is bare kraft on both artboards -- the back's declaration
    # panel now occupies the upper kraft area.
    ck(rgb.getpixel((300, 2600)) == (200, 169, 110),
       f'Pouch {side.lower()}: kraft = #C8A96E, matching the Tech Pack spec')
    ck(rgb.getpixel((1500, 3600)) == (26, 26, 26),
       f'Pouch {side.lower()}: dark band = #1A1A1A, matching the Tech Pack spec')
for n in ['01-Jet-Black', '02-Bright-White', '03-Seaport-Teal', '04-Wild-Ginger', '05-Brown-Sugar']:
    im = Image.open(PACK / '04-ColorReference' / f'{n}.png').convert('L')
    strip = im.crop((60, 962, 320, 992))     # CMYK value row, above the footer bar
    footer = im.crop((60, 1014, 320, 1050))  # footer bar must not overlap it
    ck(strip.getextrema()[0] < 120, f'{n}: CMYK value row is rendered')
    ck(im.crop((60, 995, 320, 1013)).getextrema()[0] > 200,
       f'{n}: clear gap between the CMYK row and the footer bar')

print('\n=== 7. REAL FILE FORMATS (not extensions) ===')
MAGIC = {'.png': (b'\x89PNG\r\n\x1a\n',), '.pdf': (b'%PDF',), '.svg': (b'<svg',),
         # A modern Illustrator file is a PDF container; a legacy one is
         # PostScript. Either is a real .ai; a renamed raster is not.
         '.ai': (b'%PDF', b'%!PS'),
         '.csv': None, '.txt': None, '.md': None, '.html': None}
for p in sorted(PACK.rglob('*')):
    if not p.is_file(): continue
    want = MAGIC.get(p.suffix.lower(), 'UNKNOWN')
    ck(want != 'UNKNOWN', f'{p.name}: known file type')
    if want and want != 'UNKNOWN':
        head = p.read_bytes()[:8]
        ck(any(head.startswith(s) for s in want),
           f'{p.relative_to(PACK)}: real format matches .{p.suffix[1:]}')
_ai = PACK / '03-Logo' / 'SteelStag-Logo.ai'
ck(_ai.is_file(), 'Adobe Illustrator deliverable supplied (OD-07)')
ck(_ai.read_bytes()[:4] == b'%PDF', '.ai is a real PDF-container Illustrator file, not a renamed raster')
import pymupdf as _mu
_aid = _mu.open(_ai)
ck(_aid.page_count == 1, '.ai has a single artboard')
_ap = _aid[0]
ck(abs(_ap.rect.width - 1005.75) < 0.01 and abs(_ap.rect.height - 911.25) < 0.01,
   f'.ai artboard is 1005.75 x 911.25 pt (got {_ap.rect.width:.2f} x {_ap.rect.height:.2f})')
ck(len(_ap.get_drawings()) == 25, f'.ai carries all 25 vector paths (got {len(_ap.get_drawings())})')
ck(len(_ap.get_images()) == 0, '.ai contains no embedded raster')
_svgp = _mu.open(PACK / '03-Logo' / 'SteelStag-Logo.pdf')[0]
ck(abs(_ap.rect.width - _svgp.rect.width) < 0.01
   and len(_ap.get_drawings()) == len(_svgp.get_drawings()),
   '.ai matches the approved PDF artwork exactly (artboard + path count)')
_aid.close()
_rf = ' '.join(README.split())
ck("does not carry Adobe's proprietary private-data stream" in _rf,
   'README discloses that the .ai is not a CC-native document')
ck('opens natively in Adobe Illustrator' in _rf,
   'README states the .ai opens natively in Illustrator')
ck('not one coordinate changed' in _rf,
   'README states the .ai was built from the approved artwork unchanged')
for f in ['SteelStag-Logo.svg', 'SteelStag-Logo.pdf',
          'SteelStag-Logo-Transparent.png', 'SteelStag-Logo-Dark.png']:
    ck((PACK / '03-Logo' / f).is_file(), f'Approved logo asset preserved: {f}')
ck('Traced-Approximate' not in ' '.join(p.name for p in (PACK / '03-Logo').iterdir()),
   'Approved logo artwork is not renamed or demoted')
ck('traced approximation' not in README.lower() and 'not tonally identical' not in README,
   'README does not demote the approved vector artwork')
ck('open it and re-save once' in _rf,
   'README states the one step needed if prepress wants a CC-native file')
svg = io.open(PACK / '03-Logo' / 'SteelStag-Logo.svg', encoding='utf-8').read()
ck('<image' not in svg and 'base64' not in svg, 'Logo SVG is true vector (no embedded raster)')

print('\n=== 8. STYLE SCOPE (library vs current order) ===')
sys.path.insert(0, str(BASE))
import steelstag_styles as SS
active, held = SS.active_styles('SS2026'), SS.inactive_styles('SS2026')
ck(active == ['ST-RN-001', 'ST-VN-003'], f'SS2026 active styles = {active}')
ck('ST-DS-002' in held and 'ST-DS-002' in SS.STYLE_LIBRARY,
   'ST-DS-002 Deep Scoop retained in the style library, inactive for SS2026')
ck(len(SS.STYLE_LIBRARY['ST-DS-002']['neck_measurements']) == 4,
   'Deep Scoop neck measurements preserved in full')
spec_body = TP.split('Revision History')[0]
for code in active:
    ck(code in spec_body, f'Active style {code} appears in the Tech Pack')
for code in held:
    ck(code not in spec_body,
       f'Inactive style {code} does NOT appear in the Tech Pack specification body')

print('\n=== 9. PACKAGE (ZIP) COMPLETENESS ===')
with zipfile.ZipFile(ZIPF) as z:
    names = z.namelist()
    ck(z.testzip() is None, 'ZIP integrity check passes')
    import importlib.util as _bu
    _bs = _bu.spec_from_file_location('bp_count', BASE / 'build_package.py')
    _bm = _bu.module_from_spec(_bs); _bs.loader.exec_module(_bm)
    _expected = len(_bm._manifest())
    ck(len(names) == _expected,
       f'ZIP contains every manifest file ({_expected}; got {len(names)})')
    root = 'SteelStag-ManufacturerPack-SS2026-v1.3/'
    ck(all(n.startswith(root) for n in names), 'ZIP has a single versioned root folder')
    need = ['README.txt', 'SteelStag-SS2026-Changes-for-Manufacturer-v1.3.md', 'label-viewer.html',
            '01-TechPack/SteelStag-TechPack-SS2026-v1.3.pdf',
            '01-TechPack/SteelStag-QuantityBreakdown-SS2026-v1.3.csv',
            '02-Labels/SteelStag-Labels-PrintReady-v1.3.pdf']
    for code in ['S', 'M', 'L', 'XL']:
        need.append(f'02-Labels/Neck-Labels/NeckLabel-{code}-384dpi.png')
        need.append(f'02-Labels/Size-Stickers/SizeSticker-{code}-384dpi.png')
    for n in need:
        ck(root + n in names, f'ZIP contains {n}')
    for n in names:
        ck(z.read(n) == (PACK / n[len(root):]).read_bytes(), f'ZIP entry matches source: {n[len(root):]}')
    # The download must carry only what the manufacturer needs.
    for _internal in ['SteelStag-SS2026-Revision-History', 'verify_release.py', 'build_package.py',
                      'steelstag_styles.py', 'generate_', 'render-labels']:
        ck(not any(_internal in n for n in names),
           f'Internal-only file is not in the download: {_internal}')

print('\n=== 10. RETAIL DECLARATION STICKER (OD-01) ===')
import io as _io
_gen = _io.open(BASE / 'generate_color_assets.py', encoding='utf-8').read()
_lab = _io.open(BASE / 'render-labels-win.py', encoding='utf-8').read()

def _drawn(block):
    """Only what the block actually renders. Comments describing what a side
    must NOT carry would otherwise trip the check - including the tail of the
    marker comment line itself, which the split leaves at the head of block."""
    body = block.split(chr(10), 1)[1] if chr(10) in block else ''
    return chr(10).join(ln.split('#')[0] for ln in body.split(chr(10)))

# --- the sticker artwork exists and is geometrically right ------------------
_st = PACK / '02-Labels' / 'Retail-Sticker' / 'RetailSticker-384dpi.png'
ck(_st.is_file(), 'Retail declaration sticker artwork exists')
_si = Image.open(_st)
_sdpi = _si.info.get('dpi')
ck(_sdpi is not None and abs(_sdpi[0] - 384) < 1, f'Sticker DPI metadata = 384 (got {_sdpi})')
_smm = (_si.width / (_sdpi[0] / 25.4), _si.height / (_sdpi[1] / 25.4))
for _got, _nom, _ax in ((_smm[0], 76, 'W'), (_smm[1], 44, 'H')):
    ck(_nom <= _got <= _nom + 0.35,
       f'Sticker {_ax} places at {_got:.2f} mm (70x38 trim + 2x3 mm bleed = {_nom} mm)')
_sr = _si.convert('RGBA')
ck(_sr.getpixel((0, _sr.height // 2))[3] > 0 and _sr.getpixel((_sr.width - 1, _sr.height // 2))[3] > 0,
   'Sticker artwork bleeds to the canvas edge')

# --- the sticker carries consumer-facing content ONLY ----------------------
_sticker_src = _drawn(_lab.split("name='retail-sticker'")[1].split('  # 5. Hang Tag Back')[0])
for _need in ['MRP', 'Size', 'SKU', 'Mfd/Pkd', 'Marketed by', 'Anaishu Lifestyle Private Limited',
              'Manufactured &amp; Packed by', 'Consumer care', 'hello@steelstag.in',
              'Made in India', 'Net qty', 'T-Shirt']:
    ck(_need in _sticker_src, f'Sticker prints consumer-facing field: {_need}')
# nothing internal may reach production artwork
for _banned in ['OD-01', 'OD-0', 'VALUES PENDING', 'values pending', 'BARCODE AREA', 'barcode area',
                'GTIN', 'pending', 'Pending', 'TBC', 'do not print', 'DO NOT PRINT',
                'Rajlakshmi', 'placeholder']:
    ck(_banned not in _sticker_src, f'Sticker artwork carries no internal text: "{_banned}"')

# --- the pouch carries no declarations at all ------------------------------
_front_src = _drawn(_gen.split('\u2500\u2500 FRONT:')[1].split('\u2500\u2500 BACK:')[0])
_back_src = _drawn(_gen.split('\u2500\u2500 BACK:')[1].split('# Thin outline')[0])
for _banned in ['MRP', 'DECLARATION', 'Marketed by', 'CONSUMER CARE', 'Consumer care',
                'BARCODE', 'PKD', 'OD-01', 'VALUES PENDING', 'GTIN']:
    ck(_banned not in _front_src, f'Pouch FRONT draws no "{_banned}"')
    ck(_banned not in _back_src, f'Pouch BACK draws no "{_banned}"')
ck('RetailSticker' not in _back_src and 'sticker_path' not in _back_src,
   'Pouch back is the bare printed pouch - no applied sticker in the artwork')
ck('FRONT' in _front_src and 'BACK' in _back_src, 'Each artboard stamp states which side it is')

# --- the specification, not the artwork, carries the outstanding values -----
ck('Retail Declaration Sticker' in TPF, 'Tech Pack specifies the retail declaration sticker')
ck('70\u00a0\u00d7\u00a038\u00a0mm'.replace('\u00a0', ' ') in TPF.replace('\u00a0', ' '),
   'Tech Pack states the sticker finished size')
ck('Do not print production stickers yet' in TPF, 'Tech Pack blocks production sticker printing')
ck('To be issued by SteelStag' in TPF, 'MRP marked as to be issued')
ck('Only if a GTIN is issued' in TPF, 'Barcode marked conditional in the spec')
ck('Manufactured & Packed by' in TPF or 'Manufactured &amp; Packed by' in TPF,
   'Combined manufactured-and-packed line specified')
ck('Rajlakshmi Cotton Mills' in TPF, 'Manufacturer of record named for written confirmation')
ck('which premises actually manufactures and packs this order' in TPF,
   'Factory asked which premises manufactures and packs')
ck('as it appears on your GST registration' in TPF,
   'Factory asked for GST-matching address wording')
for _frag in ['ANAISHU LIFESTYLE PRIVATE LIMITED', 'Anaishu Lifestyle Private Limited']:
    pass
for _frag in ['A-406', 'D. Chowdhary Madhusudan Complex', 'Dimna Chowk', 'Jamshedpur',
              'East Singhbhum', 'Jharkhand 831018']:
    ck(_frag in TPF, f'Marketed-by carries the registered detail: {_frag}')
    ck(_frag in README, f'README carries the registered detail: {_frag}')
_rm = ' '.join(README.split())
ck('is the MARKETER and is printed as such' in _rm and 'not the manufacturer or the packer' in _rm,
   'README distinguishes marketer from manufacturer/packer')
ck('is the marketer' in TPF.lower(), 'Tech Pack distinguishes marketer from manufacturer/packer')
# no invented statutory values anywhere
import re as _re
for _bad in [r'MRP\s*\u20b9\s*\d', r'\+91[\s\d]{6,}', r'Mfd/Pkd\s+\d{2}/\d{4}']:
    ck(_re.search(_bad, TPF) is None, f'No invented declaration value matching /{_bad}/')

for _side in ('Front', 'Back'):
    _f = PACK / '04-ColorReference' / f'Packaging-Pouch-{_side}-Mockup.png'
    ck(_f.is_file(), f'Pouch {_side.lower()} artboard exists')
ck(not (PACK / '04-ColorReference' / 'Packaging-Pouch-Mockup.png').is_file(),
   'Superseded single-artboard pouch mockup removed')

print('\n=== 11. SAMPLING / QC SCOPE (OD-04 closed) ===')
ck('No TOP submission required' in TPF, 'Tech Pack states TOP is not required')
ck('2 pcs per style' not in TPF.replace('previously listed as 2 pcs per style per colour', ''),
   'No live TOP requirement remains in the Tech Pack')
ck('NO TOP SUBMISSION REQUIRED' in README, 'README states TOP is not required')
ck('Final random production QC' in TPF, 'Final random production QC specified')
ck('random sampling across finished production' in TPF, 'Random sampling across finished production stated')

print('\n=== 12. FINAL HANDOFF STATUS (OD-07) ===')
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location('bp', BASE / 'build_package.py')
_bp = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_bp)
_ready, _missing = _bp.handoff_status()
print(f'  INFO  handoff ready = {_ready}')
for _m in _missing:
    print(f'  INFO  outstanding: {_m}')
ck('.ai' in _bp.MAGIC, 'Build validates .ai by real signature, not extension')
ck(_bp.MAGIC['.ai'] == (b'%PDF', b'%!PS'), 'Only genuine Illustrator containers accepted as .ai')
ck(_ready, 'Final artwork handoff is READY - no outstanding handoff files')
ck('SteelStag-Logo.ai' in _rf, 'README lists the Illustrator deliverable')
ck('SUPPLIED' in _rf, 'README marks the Illustrator deliverable as supplied')

print('\n=== 13. PORTAL / PACK CROSS-CHECK ===')
for rel, dst in [('02-Labels/Neck-Labels/NeckLabel-M-384dpi.png', 'NeckLabel-M-384dpi.png'),
                 ('02-Labels/Wash-Care/WashCareLabel-384dpi.png', 'WashCareLabel-384dpi.png'),
                 ('02-Labels/Hang-Tags/HangTag-Front-384dpi.png', 'HangTag-Front-384dpi.png'),
                 ('04-ColorReference/Packaging-Pouch-Front-Mockup.png', 'Packaging-Pouch-Front-Mockup.png'),
                 ('04-ColorReference/Packaging-Pouch-Back-Mockup.png', 'Packaging-Pouch-Back-Mockup.png')]:
    a = (PACK / rel).read_bytes(); b = (BASE / 'manufacturer' / 'assets' / dst).read_bytes()
    ck(a == b, f'Portal asset identical to pack source: {dst}')
for src in re.findall(r'<img[^>]*src="assets/([^"]+)"', PORTAL):
    ck((BASE / 'manufacturer' / 'assets' / src).is_file(), f'Portal image resolves: {src}')
href = re.findall(r'href="(downloads/[^"]+)"', PORTAL)
for h in set(href):
    ck((BASE / 'manufacturer' / h).is_file(), f'Portal download link resolves: {h}')
viewer = io.open(PACK / 'label-viewer.html', encoding='utf-8').read()
for src in re.findall(r'<img src="([^"]+)"', viewer):
    ck((PACK / src).is_file(), f'label-viewer image resolves: {src}')

print('\n=== 14. BRAND RULE: ONE LOGO APPEARANCE EVERYWHERE ===')
_L = PACK / '03-Logo'
_master = Image.open(_L / 'SteelStag-Logo-Transparent.png').convert('RGBA')
_mm = _master.split()[3].point(lambda v: 255 if v > 128 else 0)
_mb = _master.split()[3].getbbox()


def _gap_pct(mask, W, H):
    px = mask.load()
    rows = [sum(1 for x in range(0, W, 2) if px[x, y] > 128) for y in range(H)]
    top = next(y for y in range(H) if rows[y]); bot = max(y for y in range(H) if rows[y])
    cur, best = None, 0
    for y in range(top, bot):
        if rows[y] == 0:
            cur = y if cur is None else cur
        elif cur is not None:
            best = max(best, y - cur); cur = None
    return 100 * best / (bot - top)


_mgap = _gap_pct(_mm, _master.width, _master.height)

# -- the master itself: safe clear space so exports cannot clip -------------
_marg = (_mb[0], _master.width - _mb[2], _mb[1], _master.height - _mb[3])
ck(min(_marg) >= 80, f'Master has >=80px clear space on every side (L/R/T/B = {_marg})')
ck(abs(_mgap - 6.10) < 0.15, f'Master stag-to-wordmark gap is 6.10% (got {_mgap:.2f}%)')

# -- raster copies are the master, byte for byte ---------------------------
_ref_bytes = (_L / 'SteelStag-Logo-Transparent.png').read_bytes()
for _c in [BASE / 'manufacturer' / 'assets' / 'logo.png', BASE / 'logo.png']:
    ck(_c.read_bytes() == _ref_bytes, f'Raster copy is byte-identical to the master: {_c.name}')

# -- Logo-Dark is the same mark, same canvas, same spacing -----------------
_dk = Image.open(_L / 'SteelStag-Logo-Dark.png').convert('RGB')
ck(_dk.size == _master.size, f'Logo-Dark canvas matches the master {_master.size} (got {_dk.size})')
_dm = _dk.convert('L').point(lambda v: 255 if v > 40 else 0)
_dgap = _gap_pct(_dm, _dk.width, _dk.height)
ck(abs(_dgap - _mgap) < 0.2, f'Logo-Dark spacing matches the master ({_dgap:.2f}% vs {_mgap:.2f}%)')

# -- vector derivatives: same geometry and spacing (tone may differ) -------
import pymupdf
_vd = pymupdf.open(_L / 'SteelStag-Logo.ai')
_vp = _vd[0].get_pixmap(dpi=150, alpha=True)
_vi = Image.frombytes('RGBA', (_vp.width, _vp.height), _vp.samples)
_vm = _vi.split()[3].point(lambda v: 255 if v > 128 else 0)
_vgap = _gap_pct(_vm, _vi.width, _vi.height)
ck(abs(_vgap - _mgap) < 0.3, f'Vector derivative keeps the master spacing ({_vgap:.2f}% vs {_mgap:.2f}%)')
_vd.close()

# -- nothing may recolour the mark ----------------------------------------
_g = io.open(BASE / 'generate_color_assets.py', encoding='utf-8').read()
for _banned in ['Image.eval(r2', 'dark_logo', 'x * 0.18', 'x * 0.16', 'x * 0.14']:
    ck(_banned not in _g, f'No charcoal multiply / recolour of the mark: "{_banned}"')
ck('logo.crop(logo.split()[3].getbbox())' in _g,
   'Pouch sizes the mark from its own bounds, not the master canvas')

# -- pouch front keeps the full metallic range -----------------------------
# Find the mark by excluding the kraft ground, wherever it sits on the panel.
_pf = Image.open(PACK / '04-ColorReference' / 'Packaging-Pouch-Front-Mockup.png').convert('RGB')
_KRAFT = (200, 169, 110)
_reg = _pf.crop((700, 450, 2330, 2250))
_all = list(_reg.getdata())
_px = [p for p in _all
       if abs(p[0]-_KRAFT[0]) + abs(p[1]-_KRAFT[1]) + abs(p[2]-_KRAFT[2]) > 45]
ck(len(_px) > 50000, f'Pouch front mark located on the kraft field ({len(_px)} px)')
_lum = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in _px]
ck(max(_lum) > 200,
   f'Pouch front keeps the metallic highlight range (max luminance {max(_lum):.0f})')
_mgrey = ImageStat.Stat(_master.convert('L'), mask=_mm).mean[0]
ck(abs(sum(_lum) / len(_lum) - _mgrey) < 30,
   f'Pouch front mark tone matches the master ({sum(_lum)/len(_lum):.1f} vs {_mgrey:.1f})')
# the front must stay brand-led: no backing panel behind the mark
_gsrc = io.open(BASE / 'generate_color_assets.py', encoding='utf-8').read()
_front_block = _gsrc.split('\u2500\u2500 FRONT:')[1].split('\u2500\u2500 BACK:')[0]
for _b in ['panel_w', 'panel_pad_x', 'panel_y']:
    ck(_b not in _front_block, f'Pouch front has no backing panel behind the mark ("{_b}")')

# -- TM on every styled wordmark lockup ------------------------------------
_lab = io.open(BASE / 'render-labels-win.py', encoding='utf-8').read()
ck('<span class="brand">SteelStag<sup class="tm">\u2122</sup>' in _lab, 'Wash care wordmark carries the TM')
ck('<span class="s-brand">SteelStag<sup class="tm">\u2122</sup>' in _lab, 'Retail sticker wordmark carries the TM')
ck('SteelStag&#x2122; 2026' in _lab, 'Hang tag back wordmark carries the TM')
ck('SteelStag\u2122' in _g, 'Colour swatch wordmark carries the TM')
ck('"\\u2122"' in _g or '\u2122' in _g, 'Pouch back wordmark carries the TM')
ck('SteelStag<span' in PORTAL and '\u2122' in PORTAL, 'Portal sidebar wordmark carries the TM')

# -- the rule is published, not just followed ------------------------------
ck('approved visual master' in TPF.lower(), 'Tech Pack publishes the approved visual master')
ck('production derivative' in TPF.lower(), 'Tech Pack marks the vector files as derivatives')
ck('STEELSTAG BRAND RULE' in README, 'README publishes the brand rule')

print('\n' + '=' * 62)
print(f'RESULT: {len(fails)} failed, {len(warns)} warnings')
for f in fails: print('  FAIL:', f)
sys.exit(1 if fails else 0)
