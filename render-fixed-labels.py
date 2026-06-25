"""
Re-renders only the three changed labels:
  - Neck Labels (added 100% Combed Cotton line)
  - Wash Care Label (removed red from icons)
  - Size Stickers (changed to warm charcoal palette)

Outputs directly to the correct 02-Labels subfolders.
"""
import asyncio, os, sys, subprocess, threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

try:
    import img2pdf
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'img2pdf', '-q'])
    import img2pdf

from playwright.async_api import async_playwright

BASE = Path(r'C:\Users\anjan\OneDrive\Documents\Personal\Anaishu')
LABELS_ROOT = BASE / 'SteelStag-ManufacturerPack-SS2026' / '02-Labels'

PX    = 3.7795
DPR   = 4
BLEED = 3

def mm(v): return v * PX

SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Oxanium:wght@600;800&family=Goldman&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root { --ink: #1a1a1a; --steel: #6b7280; --light: #e5e7eb; --gold: #b8a98a; }
body { background: transparent; }
""".replace('{bleed}', str(int(mm(BLEED))))

def page(w_mm, h_mm, body_css, html_body, bg='#ffffff'):
    w_px    = mm(w_mm)
    h_px    = mm(h_mm)
    b_px    = mm(BLEED)
    total_w = w_px + b_px * 2
    total_h = h_px + b_px * 2
    m1       = b_px - mm(1)
    m_right0 = total_w - b_px + mm(1)
    m_top0   = total_h - b_px + mm(1)
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"/>
<style>
{SHARED_CSS}
html, body {{ width: {total_w}px; height: {total_h}px; overflow: hidden; background: transparent; }}
.label {{
  position: absolute;
  left: {b_px}px; top: {b_px}px;
  width: {w_px}px; height: {h_px}px;
  background: {bg};
  display: flex; flex-direction: column; align-items: center;
  overflow: hidden;
}}
{body_css}
</style>
</head><body>
<div class="label">{html_body}</div>
<svg style="position:absolute;inset:0;width:{total_w}px;height:{total_h}px;pointer-events:none" viewBox="0 0 {total_w} {total_h}">
  <g stroke="#555" stroke-width="0.75" fill="none">
    <line x1="0" y1="{b_px}" x2="{m1}" y2="{b_px}"/>
    <line x1="{b_px}" y1="0" x2="{b_px}" y2="{m1}"/>
    <line x1="{m_right0}" y1="{b_px}" x2="{total_w}" y2="{b_px}"/>
    <line x1="{total_w - b_px}" y1="0" x2="{total_w - b_px}" y2="{m1}"/>
    <line x1="0" y1="{total_h - b_px}" x2="{m1}" y2="{total_h - b_px}"/>
    <line x1="{b_px}" y1="{m_top0}" x2="{b_px}" y2="{total_h}"/>
    <line x1="{m_right0}" y1="{total_h - b_px}" x2="{total_w}" y2="{total_h - b_px}"/>
    <line x1="{total_w - b_px}" y1="{m_top0}" x2="{total_w - b_px}" y2="{total_h}"/>
  </g>
</svg>
</body></html>"""

# All icons monochrome — no red
CARE_ICONS_DARK = """
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <path d="M3 8 Q3 19 12 19 Q21 19 21 8 Z"/>
  <path d="M3 8 L3 7 Q3 5 5 5 L19 5 Q21 5 21 7 L21 8"/>
  <text x="12" y="16" text-anchor="middle" font-size="5.5" fill="#444" stroke="none" font-family="sans-serif">30°</text>
</svg>
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <path d="M3 20 L12 4 L21 20 Z"/>
  <line x1="8" y1="11" x2="16" y2="18"/><line x1="16" y1="11" x2="8" y2="18"/>
</svg>
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/>
</svg>
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <path d="M4 17 L4 14 Q4 10 9 10 L20 10 L20 17 Z"/>
  <rect x="9" y="17" width="6" height="2" rx="0.5"/>
  <line x1="6" y1="11.5" x2="18" y2="16.5" stroke="#444" stroke-width="1.8"/>
  <line x1="18" y1="11.5" x2="6" y2="16.5" stroke="#444" stroke-width="1.8"/>
</svg>
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <circle cx="12" cy="12" r="9"/>
  <text x="12" y="16.5" text-anchor="middle" font-size="9" fill="#444" stroke="none" font-family="serif" font-style="italic">P</text>
  <line x1="4.5" y1="5.5" x2="19.5" y2="18.5" stroke="#444" stroke-width="1.8"/>
</svg>
"""

PORT = 7789

LABELS = [
    # Neck Labels — now with 100% Combed Cotton
    *[{
        'name': f'NeckLabel-{code}-300dpi',
        'subfolder': 'Neck-Labels',
        'w': 50, 'h': 30, 'bg': 'transparent',
        'css': """
          .label { justify-content: center; gap: 4px; padding: 8px; background: transparent; }
          .label img { width: 75px; height: auto; }
          .info { font-size: 5.5px; letter-spacing: 0.22em; text-transform: uppercase;
                  color: #555; font-family: Inter, sans-serif; }
          .size-b { font-family: Oxanium, sans-serif; font-weight: 800; font-size: 9px;
                    color: #333; letter-spacing: 0.05em; }
        """,
        'html': f"""
          <img src="http://localhost:{PORT}/logo.png" />
          <span class="info">100% Combed Cotton</span>
          <span class="info">Made in India</span>
          <span class="size-b">{code}</span>
        """,
    } for code in ['S', 'M', 'L', 'XL']],

    # Wash Care Label — all monochrome
    {
        'name': 'WashCareLabel-300dpi',
        'subfolder': 'Wash-Care',
        'w': 40, 'h': 60, 'bg': '#ffffff',
        'css': """
          .label { padding: 12px 10px; gap: 7px; }
          .brand { font-family: Goldman, sans-serif; font-weight: 400; font-size: 9px;
                   letter-spacing: 0.15em; color: var(--ink); }
          .div   { width: 100%; height: 1px; background: var(--light); }
          .icons { display: flex; gap: 5px; flex-wrap: wrap; justify-content: center; }
          .fabric{ font-size: 6.5px; letter-spacing: 0.15em; text-transform: uppercase;
                   color: var(--steel); text-align: center; line-height: 1.7;
                   font-family: Inter, sans-serif; }
          .origin{ font-size: 6px; letter-spacing: 0.2em; text-transform: uppercase;
                   color: #bbb; margin-top: auto; font-family: Inter, sans-serif; }
        """,
        'html': f"""
          <span class="brand">SteelStag</span>
          <div class="div"></div>
          <div class="icons">{CARE_ICONS_DARK}</div>
          <div class="div"></div>
          <div class="fabric">100% Combed Cotton<br/>Pre-shrunk</div>
          <div class="div"></div>
          <div class="fabric" style="color:#aaa">Do not bleach<br/>Wash dark colors separately<br/>Iron on reverse</div>
          <span class="origin">Made in India</span>
        """,
    },

    # Size Stickers — warm charcoal palette
    *[{
        'name': f'SizeSticker-{code}-300dpi',
        'subfolder': 'Size-Stickers',
        'w': 30, 'h': 30, 'bg': 'transparent',
        'css': f"""
          .label {{ background: {color}; border-radius: 50%; justify-content: center; gap: 3px; }}
          .sz  {{ font-family: Oxanium, sans-serif; font-weight: 800;
                 font-size: {'36' if code != 'XL' else '28'}px; color: #fff;
                 line-height: 1; letter-spacing: -0.02em; }}
          .sub {{ font-size: 7px; letter-spacing: 0.25em; text-transform: uppercase;
                 color: rgba(255,255,255,0.45); font-family: Inter, sans-serif; }}
        """,
        'html': f'<span class="sz">{code}</span><span class="sub">{label}</span>',
    } for code, label, color in [
        ('S',  'Small',   '#6b6560'),
        ('M',  'Medium',  '#4a4440'),
        ('L',  'Large',   '#332e2b'),
        ('XL', 'X-Large', '#1a1a1a'),
    ]],
]

async def render():
    handler = SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None
    server = HTTPServer(('localhost', PORT), handler)
    os.chdir(BASE)
    import threading
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        all_pngs = []

        for label in LABELS:
            dest_dir = LABELS_ROOT / label['subfolder']
            dest_dir.mkdir(parents=True, exist_ok=True)
            out_path = str(dest_dir / f"{label['name']}.png")

            html = page(label['w'], label['h'], label['css'], label['html'], label.get('bg','#fff'))
            total_w = int((label['w'] + BLEED*2) * PX)
            total_h = int((label['h'] + BLEED*2) * PX)

            pg = await browser.new_page(
                viewport={'width': total_w, 'height': total_h},
                device_scale_factor=DPR,
            )
            await pg.set_content(html, wait_until='networkidle')
            await pg.screenshot(
                path=out_path,
                full_page=False,
                omit_background=(label.get('bg') == 'transparent'),
            )
            await pg.close()
            all_pngs.append(out_path)
            print(f"  OK{label['name']}")

        await browser.close()
        server.shutdown()

    # Rebuild the combined PDF
    pdf_path = str(LABELS_ROOT / 'AllLabels-PrintReady.pdf')
    # Collect all PNGs across all subfolders in order
    order = ['Neck-Labels', 'Wash-Care', 'Hang-Tags', 'Size-Stickers']
    ordered_pngs = []
    for folder in order:
        d = LABELS_ROOT / folder
        if d.exists():
            ordered_pngs += sorted([str(f) for f in d.glob('*.png') if not f.name.startswith('._')])
    with open(pdf_path, 'wb') as f:
        f.write(img2pdf.convert(ordered_pngs))
    print(f"\n  OKPDF rebuilt → {pdf_path}")

asyncio.run(render())
