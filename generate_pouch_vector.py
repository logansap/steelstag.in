"""
Vector pouch artwork for the converter.

04-ColorReference/Packaging-Pouch-*-Mockup.png are visual references -- flat
raster, drawn with PIL, with a mockup surround. A converter cannot place those
on a dieline. This produces the same approved layout as real vector artwork on
a true 240 x 340 mm panel with 3 mm bleed, written by Chromium's PDF engine so
type stays live text with embedded fonts.

Output: 05-Packaging/SteelStag-Pouch-Front-v1.3.ai
        05-Packaging/SteelStag-Pouch-Back-v1.3.ai

These are BRAND LAYOUT files, not dielines. The converter still produces the
dieline (gusset, seal zones, zip) to their own standard and places this artwork
on it.

Proportions are carried over from the approved mockup. In the mockup the pouch
shape is inset inside the canvas, so its internal sizes are relative to a
209.7 mm panel; every dimension below is scaled by 240/209.7 so the mark and
type keep the same proportion of the pouch that was approved.
"""
import asyncio
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import pymupdf
from playwright.async_api import async_playwright

BASE = Path(__file__).parent
PACK = BASE / 'SteelStag-ManufacturerPack-SS2026'
OUT = PACK / '05-Packaging'
OUT.mkdir(exist_ok=True)
PORT = 7791

# ── geometry ────────────────────────────────────────────────────────────────
W_MM, H_MM = 240.0, 340.0      # finished panel
BLEED = 3.0                     # mm, all edges
TW, TH = W_MM + BLEED * 2, H_MM + BLEED * 2

KRAFT = '#C8A96E'
DARK = '#1A1A1A'
ZIP_BAND = '#AF946E'
BAND_TOP = H_MM * 0.65          # black band starts at 65% -- matches the spec

# mockup -> real panel scale (see module docstring)
K = 240.0 / 209.7
S = lambda v: v * 0.27502 * K   # mockup design units -> mm on the real panel

ZIP_H = S(80)
BANNER_W, BANNER_H = S(320), S(52)
BANNER_TOP = S(10)
# The master canvas is 1341 x 1342 with the mark occupying x 235..1096
# (861 px) and y 80..1262 (1182 px). Scaling the IMAGE by width would shrink
# the mark by the clear space, so size the image up so the MARK lands at the
# intended width, then offset for the padding.
M_CANVAS_W, M_CANVAS_H = 1341.0, 1342.0
M_MARK_W, M_MARK_H, M_MARK_TOP = 861.0, 1182.0, 80.0
MARK_W = 68.3 * K                       # printed width of the mark itself
IMG_W = MARK_W * M_CANVAS_W / M_MARK_W
IMG_H = IMG_W * M_CANVAS_H / M_CANVAS_W
MARK_H = IMG_H * M_MARK_H / M_CANVAS_H
MARK_OFFSET = IMG_H * M_MARK_TOP / M_CANVAS_H
TAG_PT = S(20) * 72 / 25.4
INFO_PT = S(19) * 72 / 25.4
INFO_LBL_PT = S(14) * 72 / 25.4
URL_PT = S(17) * 72 / 25.4

KRAFT_TOP = ZIP_H
KRAFT_H = BAND_TOP - KRAFT_TOP
BLOCK_H = MARK_H + S(70)
MARK_Y = KRAFT_TOP + max(S(40), (KRAFT_H - BLOCK_H) / 2)   # top of the MARK
IMG_Y = MARK_Y - MARK_OFFSET

CROP = f'''
<svg class="marks" viewBox="0 0 {TW} {TH}">
  <g stroke="#888" stroke-width="0.15" fill="none">
    <line x1="0" y1="{BLEED}" x2="{BLEED - 1}" y2="{BLEED}"/>
    <line x1="{BLEED}" y1="0" x2="{BLEED}" y2="{BLEED - 1}"/>
    <line x1="{TW - BLEED + 1}" y1="{BLEED}" x2="{TW}" y2="{BLEED}"/>
    <line x1="{TW - BLEED}" y1="0" x2="{TW - BLEED}" y2="{BLEED - 1}"/>
    <line x1="0" y1="{TH - BLEED}" x2="{BLEED - 1}" y2="{TH - BLEED}"/>
    <line x1="{BLEED}" y1="{TH - BLEED + 1}" x2="{BLEED}" y2="{TH}"/>
    <line x1="{TW - BLEED + 1}" y1="{TH - BLEED}" x2="{TW}" y2="{TH - BLEED}"/>
    <line x1="{TW - BLEED}" y1="{TH - BLEED + 1}" x2="{TW - BLEED}" y2="{TH}"/>
  </g>
</svg>'''


def shell(body, extra_css=''):
    return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"/>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Goldman&display=swap');
@page {{ size: {TW}mm {TH}mm; margin: 0; }}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {TW}mm; height: {TH}mm; }}
.sheet {{ position: relative; width: {TW}mm; height: {TH}mm; background: {KRAFT}; overflow: hidden; }}
/* everything positions from the TRIM origin, i.e. inset by the bleed */
.panel {{ position: absolute; left: {BLEED}mm; top: {BLEED}mm;
          width: {W_MM}mm; height: {H_MM}mm; }}
.band {{ position: absolute; left: -{BLEED}mm; right: -{BLEED}mm;
         top: {BAND_TOP}mm; bottom: -{BLEED}mm; background: {DARK}; }}
.zip  {{ position: absolute; left: -{BLEED}mm; right: -{BLEED}mm; top: -{BLEED}mm;
         height: {ZIP_H + BLEED}mm; background: {ZIP_BAND}; }}
.banner {{ position: absolute; left: 50%; transform: translateX(-50%);
           top: {BANNER_TOP}mm; width: {BANNER_W}mm; height: {BANNER_H}mm;
           background: {DARK}; display: flex; align-items: center; justify-content: center; }}
.banner span {{ font-family: Goldman, sans-serif; font-size: {URL_PT}pt; color: #B4AA9B; }}
.marks {{ position: absolute; left: 0; top: 0; width: {TW}mm; height: {TH}mm; }}
{extra_css}
</style></head><body><div class="sheet"><div class="panel">
{body}
</div>{CROP}</div></body></html>'''


FRONT_CSS = f'''
.logo {{ position: absolute; left: 50%; transform: translateX(-50%);
         top: {IMG_Y}mm; width: {IMG_W}mm; }}
.logo img {{ width: 100%; display: block; }}
.tag {{ position: absolute; left: 0; right: 0; top: {MARK_Y + MARK_H + S(14)}mm;
        text-align: center; font-family: Inter, sans-serif; font-weight: 300;
        font-size: {TAG_PT}pt; color: #50463C; }}
.rule {{ position: absolute; left: 50%; transform: translateX(-50%);
         top: {MARK_Y + MARK_H + S(40)}mm; width: {S(180)}mm; height: 0.18mm;
         background: #8C7D69; }}
.info {{ position: absolute; left: 0; right: 0; top: {BAND_TOP + S(40)}mm;
         display: flex; }}
.info > div {{ flex: 1; text-align: center; font-family: Inter, sans-serif; }}
.info .k {{ font-size: {INFO_LBL_PT}pt; color: #787369; letter-spacing: 0.08em; }}
.info .v {{ font-size: {INFO_PT}pt; color: #DCD7CD; font-weight: 600; margin-top: {S(10)}mm; }}
.info .sep {{ position: absolute; top: -{S(9)}mm; bottom: -{S(9)}mm; width: 0.15mm; background: #373A44; }}
'''

FRONT = f'''
<div class="zip"></div><div class="banner"><span>steelstag.in</span></div>
<div class="band"></div>
<div class="logo"><img src="http://localhost:{PORT}/logo.png"/></div>
<div class="tag">Color. Nothing else.</div>
<div class="rule"></div>
<div class="info">
  <div><div class="k">FABRIC</div><div class="v">100% Combed Cotton</div></div>
  <div style="position:relative"><div class="sep" style="left:0"></div>
      <div class="k">GSM</div><div class="v">180</div>
      <div class="sep" style="right:0"></div></div>
  <div><div class="k">ORIGIN</div><div class="v">Made in India</div></div>
</div>
'''

BACK_CSS = f'''
.brand {{ position: absolute; left: 0; right: 0; top: {BAND_TOP + S(44)}mm;
          text-align: center; font-family: Goldman, sans-serif;
          font-size: {INFO_PT}pt; color: #969188; }}
.url {{ position: absolute; left: 0; right: 0; top: {BAND_TOP + S(76)}mm;
        text-align: center; font-family: Inter, sans-serif;
        font-size: {INFO_LBL_PT}pt; color: #6E6A64; }}
'''

BACK = f'''
<div class="zip"></div><div class="banner"><span>steelstag.in</span></div>
<div class="band"></div>
<div class="brand">SteelStag<sup style="font-family:Inter,sans-serif;font-size:0.42em;vertical-align:super">&#8482;</sup></div>
<div class="url">steelstag.in</div>
'''


async def main():
    os.chdir(BASE)
    SimpleHTTPRequestHandler.log_message = lambda *a: None
    srv = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for side, html in (('Front', shell(FRONT, FRONT_CSS)),
                           ('Back', shell(BACK, BACK_CSS))):
            pg = await browser.new_page(viewport={'width': 1200, 'height': 1700})
            await pg.set_content(html, wait_until='networkidle')
            blob = await pg.pdf(margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
                                print_background=True, prefer_css_page_size=True)
            await pg.close()

            doc = pymupdf.open('pdf', blob)
            doc.set_metadata({
                'title': f'SteelStag SS2026 Pouch {side} - brand layout',
                'author': 'Anaishu Lifestyle Private Limited',
                'subject': f'240 x 340 mm panel + 3 mm bleed. Brand layout for the '
                           f'converter to place on their dieline. Not a dieline.',
            })
            path = OUT / f'SteelStag-Pouch-{side}-v1.3.ai'
            doc.save(path, garbage=3, deflate=True)
            r = doc[0].rect
            print(f'  {path.name}: {r.width / 72 * 25.4:.1f} x {r.height / 72 * 25.4:.1f} mm, '
                  f'text {len(doc[0].get_text().strip())} chars, '
                  f'vector {len(doc[0].get_drawings())}, raster {len(doc[0].get_images())}')
            doc.close()
        await browser.close()
    srv.shutdown()


if __name__ == '__main__':
    print('Generating vector pouch artwork...')
    asyncio.run(main())
    print('Done.')
