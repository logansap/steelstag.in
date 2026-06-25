"""
Renders each SteelStag label as a high-res PNG (4x = ~384 DPI)
by screenshotting isolated HTML fragments via Playwright,
then compiles them into a single print-ready PDF via img2pdf.
"""
import asyncio, os, subprocess, sys, threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Install img2pdf if needed
try:
    import img2pdf
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'img2pdf', '-q'])
    import img2pdf

from playwright.async_api import async_playwright

BASE = Path(__file__).parent
OUT  = BASE / 'SteelStag-ManufacturerPack-SS2026' / '02-Labels'
OUT.mkdir(exist_ok=True)

# 1px @ 96dpi = 0.2646mm  â†'  1mm = 3.7795px
# At 4x device pixel ratio that's effectively ~384 DPI
PX = 3.7795   # px per mm at 96dpi
DPR = 4       # device pixel ratio

def mm(v): return v * PX   # logical px

BLEED = 3  # mm

# Shared CSS (fonts, resets, variables) â€" same as labels.html
SHARED_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Oxanium:wght@600;800&family=Goldman&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --ink:   #1a1a1a;
  --steel: #6b7280;
  --light: #e5e7eb;
  --gold:  #b8a98a;
}
body { background: transparent; }

/* bleed wrapper */
.bleed {
  position: relative;
  overflow: visible;
}
.bleed::before {
  content: '';
  position: absolute;
  inset: -{bleed}px;
  border: 0.5px solid rgba(255,100,100,0.5);
  pointer-events: none;
}
/* crop marks */
.bleed::after {
  content: '';
  position: absolute;
  inset: -{bleed}px;
}
""".replace('{bleed}', str(int(mm(BLEED))))

def page(w_mm, h_mm, body_css, html_body, bg='#ffffff'):
    w_px = mm(w_mm)
    h_px = mm(h_mm)
    b_px = mm(BLEED)
    total_w = w_px + b_px * 2
    total_h = h_px + b_px * 2
    mark_gap = mm(1)    # gap between label edge and crop mark start
    mark_len = mm(4)    # length of each crop mark line
    # crop marks start just outside the bleed area
    m0 = 0              # canvas edge
    m1 = b_px - mark_gap                      # end of crop mark (inward side)
    m_right0 = total_w - b_px + mark_gap      # start of right crop marks
    m_top0   = total_h - b_px + mark_gap
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
  <!-- crop marks: 4 corners Ã— 2 lines each, with gap from label edge -->
  <g stroke="#555" stroke-width="0.75" fill="none">
    <!-- top-left -->
    <line x1="{m0}" y1="{b_px}" x2="{m1}" y2="{b_px}"/>
    <line x1="{b_px}" y1="{m0}" x2="{b_px}" y2="{m1}"/>
    <!-- top-right -->
    <line x1="{m_right0}" y1="{b_px}" x2="{total_w}" y2="{b_px}"/>
    <line x1="{total_w - b_px}" y1="{m0}" x2="{total_w - b_px}" y2="{m1}"/>
    <!-- bottom-left -->
    <line x1="{m0}" y1="{total_h - b_px}" x2="{m1}" y2="{total_h - b_px}"/>
    <line x1="{b_px}" y1="{m_top0}" x2="{b_px}" y2="{total_h}"/>
    <!-- bottom-right -->
    <line x1="{m_right0}" y1="{total_h - b_px}" x2="{total_w}" y2="{total_h - b_px}"/>
    <line x1="{total_w - b_px}" y1="{m_top0}" x2="{total_w - b_px}" y2="{total_h}"/>
  </g>
</svg>
</body></html>"""

# â"€â"€ Label definitions â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

CARE_ICONS_WHITE = """
<!-- Wash 30&deg; â€" tub with curved bottom -->
<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" style="width:18px;height:18px;opacity:0.65">
  <path d="M3 8 Q3 19 12 19 Q21 19 21 8 Z"/>
  <path d="M3 8 L3 7 Q3 5 5 5 L19 5 Q21 5 21 7 L21 8"/>
  <text x="12" y="16" text-anchor="middle" font-size="5.5" fill="#fff" stroke="none" font-family="sans-serif">30&deg;</text>
</svg>
<!-- No bleach â€" triangle with X -->
<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" style="width:18px;height:18px;opacity:0.65">
  <path d="M3 20 L12 4 L21 20 Z"/>
  <line x1="8" y1="11" x2="16" y2="18"/>
  <line x1="16" y1="11" x2="8" y2="18"/>
</svg>
<!-- Tumble dry â€" circle with inner circle -->
<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" style="width:18px;height:18px;opacity:0.65">
  <circle cx="12" cy="12" r="9"/>
  <circle cx="12" cy="12" r="4.5"/>
</svg>
<!-- Do not iron â€" iron shape with X -->
<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" style="width:18px;height:18px;opacity:0.65">
  <path d="M4 17 L4 14 Q4 10 9 10 L20 10 L20 17 Z"/>
  <rect x="9" y="17" width="6" height="2" rx="0.5"/>
  <line x1="6" y1="11.5" x2="18" y2="16.5" stroke="#fff" stroke-width="1.5"/>
  <line x1="18" y1="11.5" x2="6" y2="16.5" stroke="#fff" stroke-width="1.5"/>
</svg>
<!-- Do not dry clean â€" circle with P and X -->
<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.5" style="width:18px;height:18px;opacity:0.65">
  <circle cx="12" cy="12" r="9"/>
  <text x="12" y="16.5" text-anchor="middle" font-size="9" fill="#fff" stroke="none" font-family="serif" font-style="italic">P</text>
  <line x1="4.5" y1="5.5" x2="19.5" y2="18.5" stroke="#fff" stroke-width="1.5"/>
</svg>
"""

CARE_ICONS_DARK = """
<!-- Wash 30&deg; â€" tub with curved bottom -->
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <path d="M3 8 Q3 19 12 19 Q21 19 21 8 Z"/>
  <path d="M3 8 L3 7 Q3 5 5 5 L19 5 Q21 5 21 7 L21 8"/>
  <text x="12" y="16" text-anchor="middle" font-size="5.5" fill="#444" stroke="none" font-family="sans-serif">30&deg;</text>
</svg>
<!-- No bleach â€" triangle with X -->
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <path d="M3 20 L12 4 L21 20 Z"/>
  <line x1="8" y1="11" x2="16" y2="18"/>
  <line x1="16" y1="11" x2="8" y2="18"/>
</svg>
<!-- Tumble dry â€" circle with inner circle -->
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <circle cx="12" cy="12" r="9"/>
  <circle cx="12" cy="12" r="4.5"/>
</svg>
<!-- Do not iron â€" iron shape with red X -->
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <path d="M4 17 L4 14 Q4 10 9 10 L20 10 L20 17 Z"/>
  <rect x="9" y="17" width="6" height="2" rx="0.5"/>
  <line x1="6" y1="11.5" x2="18" y2="16.5" stroke="#444" stroke-width="1.8"/>
  <line x1="18" y1="11.5" x2="6" y2="16.5" stroke="#444" stroke-width="1.8"/>
</svg>
<!-- Do not dry clean â€" circle with P and red X -->
<svg viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="1.5" style="width:22px;height:22px">
  <circle cx="12" cy="12" r="9"/>
  <text x="12" y="16.5" text-anchor="middle" font-size="9" fill="#444" stroke="none" font-family="serif" font-style="italic">P</text>
  <line x1="4.5" y1="5.5" x2="19.5" y2="18.5" stroke="#444" stroke-width="1.8"/>
</svg>
"""

LABELS = [

  # 1. Neck Labels â€" 50Ã—30mm, one per size, transparent bg
  *[dict(
    name=f'neck-label-{code.lower()}',
    out=f'Neck-Labels/NeckLabel-{code}-300dpi.png',
    w=50, h=30, bg='transparent',
    css="""
      .label { justify-content: center; gap: 5px; padding: 8px; background: transparent; }
      .label img { width: 85px; height: auto; }
      .made-in { font-size: 6.5px; letter-spacing: 0.22em; text-transform: uppercase; color: #555; font-family: Inter, sans-serif; }
      .size-b  { font-family: Oxanium, sans-serif; font-weight: 800; font-size: 9px; color: #333; letter-spacing: 0.05em; }
    """,
    html=f"""
      <img src="http://localhost:{{PORT}}/logo.png" />
      <span class="made-in">100% Combed Cotton</span>
      <span class="made-in">Made in India</span>
      <span class="size-b">{code}</span>
    """,
  ) for code in ['S', 'M', 'L', 'XL']],

  # 2. Wash Care Label â€" 40Ã—60mm
  dict(
    name='wash-care-label',
    out='Wash-Care/WashCareLabel-300dpi.png',
    w=40, h=60, bg='#ffffff',
    css="""
      .label { padding: 12px 10px; gap: 7px; }
      .brand  { font-family: Goldman, sans-serif; font-weight: 400; font-size: 9px; letter-spacing: 0.08em; color: var(--ink); }
      .div    { width: 100%; height: 1px; background: var(--light); }
      .icons  { display: flex; gap: 5px; flex-wrap: wrap; justify-content: center; }
      .fabric { font-size: 6.5px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--steel); text-align: center; line-height: 1.7; font-family: Inter, sans-serif; }
      .origin { font-size: 6px; letter-spacing: 0.2em; text-transform: uppercase; color: #bbb; margin-top: auto; font-family: Inter, sans-serif; }
    """,
    html=f"""
      <span class="brand">SteelStag</span>
      <div class="div"></div>
      <div class="icons">{CARE_ICONS_DARK}</div>
      <div class="div"></div>
      <div class="fabric">100% Combed Cotton<br/>Pre-shrunk</div>
      <div class="div"></div>
      <div class="fabric" style="color:#666">Do not bleach<br/>Wash dark colors separately<br/>Iron on reverse</div>
      <span class="origin">Made in India</span>
    """,
  ),

  # 3aâ€"3d. Size Stickers â€" 30mm circle
  *[dict(
    name=f'size-sticker-{code.lower()}',
    out=f'Size-Stickers/SizeSticker-{code}-300dpi.png',
    w=30, h=30, bg='transparent',
    css=f"""
      .label {{ background: {color}; border-radius: 50%; justify-content: center; gap: 3px; }}
      .sz  {{ font-family: Oxanium, sans-serif; font-weight: 800; font-size: {'36' if code != 'XL' else '28'}px; color: #fff; line-height: 1; letter-spacing: -0.02em; }}
      .sub {{ font-size: 7px; letter-spacing: 0.25em; text-transform: uppercase; color: rgba(255,255,255,0.45); font-family: Inter, sans-serif; }}
    """,
    html=f'<span class="sz">{code}</span><span class="sub">{name}</span>',
  ) for code, name, color in [
    ('S',  'Small',   '#6b6560'),
    ('M',  'Medium',  '#4a4440'),
    ('L',  'Large',   '#332e2b'),
    ('XL', 'X-Large', '#1a1a1a'),
  ]],

  # 4. Hang Tag Front â€" 50Ã—85mm
  dict(
    name='hang-tag-front',
    out='Hang-Tags/HangTag-Front-300dpi.png',
    w=50, h=85, bg='#1a1a1a',
    css="""
      .label { gap: 0; }
      .hole  { width: 10px; height: 10px; border-radius: 50%; border: 1.5px solid #555; margin-top: 14px; flex-shrink: 0; background: #1a1a1a; }
      .logo-area { width: 100%; display: flex; align-items: center; justify-content: center; padding: 16px 0 12px; }
      .logo-area img { width: 120px; height: auto; }
      .tag-body  { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; padding: 10px 18px; text-align: center; }
      .gold-rule { width: 40px; height: 1px; background: linear-gradient(90deg, transparent, #b8a98a, transparent); }
      .tagline   { font-size: 7px; letter-spacing: 0.32em; text-transform: uppercase; color: rgba(255,255,255,0.45); line-height: 2; font-family: Inter, sans-serif; }
      .prem-text { font-size: 6px; letter-spacing: 0.2em; text-transform: uppercase; color: #b8a98a; line-height: 2.2; font-family: Inter, sans-serif; }
      .bottom-bar { width: 100%; border-top: 1px solid #2a2a2a; padding: 9px 8px; display: flex; align-items: center; justify-content: center; }
      .website   { font-size: 6px; letter-spacing: 0.22em; text-transform: uppercase; color: rgba(255,255,255,0.25); font-family: Inter, sans-serif; }
    """,
    html="""
      <div class="hole"></div>
      <div class="logo-area"><img src="http://localhost:{PORT}/logo.png" /></div>
      <div class="tag-body">
        <div class="gold-rule"></div>
        <div class="tagline">Color. Nothing else.</div>
        <div class="gold-rule"></div>
        <div class="prem-text">Premium Solid Tees<br/>100% Combed Cotton<br/>Made in India</div>
      </div>
      <div class="bottom-bar"><span class="website">steelstag.in</span></div>
    """,
  ),

  # 5. Hang Tag Back â€" 50Ã—85mm
  dict(
    name='hang-tag-back',
    out='Hang-Tags/HangTag-Back-300dpi.png',
    w=50, h=85, bg='#141414',
    css="""
      .label { gap: 0; }
      .hole  { width: 10px; height: 10px; border-radius: 50%; border: 1.5px solid #555; margin-top: 14px; flex-shrink: 0; background: #141414; }
      .logo-top { width: 100%; display: flex; align-items: center; justify-content: center; padding: 10px 0 6px; }
      .logo-top img { width: 70px; height: auto; opacity: 0.85; }
      .back-body { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; padding: 8px 20px 14px; text-align: center; }
      .gold-rule { width: 30px; height: 1px; background: linear-gradient(90deg, transparent, #b8a98a, transparent); }
      .title { font-family: Oxanium, sans-serif; font-weight: 800; font-size: 8px; letter-spacing: 0.3em; text-transform: uppercase; color: rgba(255,255,255,0.7); }
      .care-row { display: flex; gap: 8px; justify-content: center; }
      .back-text { font-size: 5.5px; letter-spacing: 0.18em; text-transform: uppercase; color: rgba(255,255,255,0.45); line-height: 2.2; font-family: Inter, sans-serif; }
      .footer    { font-size: 5px; letter-spacing: 0.15em; color: rgba(255,255,255,0.2); font-family: Goldman, sans-serif; font-weight: 400; }
    """,
    html=f"""
      <div class="hole"></div>
      <div class="logo-top"><img src="http://localhost:{{PORT}}/logo.png" /></div>
      <div class="back-body">
        <div class="gold-rule"></div>
        <div class="title">Care Instructions</div>
        <div class="care-row">{CARE_ICONS_WHITE}</div>
        <div class="gold-rule"></div>
        <div class="back-text">Do not bleach<br/>Wash dark colors separately<br/>Iron on reverse side<br/>Do not tumble dry</div>
        <div class="gold-rule"></div>
        <div class="footer">steelstag.in &nbsp;&middot;&nbsp; SteelStag&#x2122; 2026</div>
      </div>
    """,
  ),
]

# â"€â"€ Playwright render â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

async def render():
    # Spin up a local HTTP server so Chromium can load logo.png
    PORT = 7788
    handler = SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None  # silence logs
    server = HTTPServer(('localhost', PORT), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    os.chdir(BASE)
    thread.start()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        png_files = []

        for label in LABELS:
            # Substitute PORT into html strings
            html_body = label['html'].replace('{PORT}', str(PORT))
            html = page(label['w'], label['h'], label['css'], html_body, label.get('bg','#fff'))
            total_w = int((label['w'] + BLEED*2) * PX)
            total_h = int((label['h'] + BLEED*2) * PX)

            page_obj = await browser.new_page(
                viewport={'width': total_w, 'height': total_h},
                device_scale_factor=DPR,
            )
            await page_obj.set_content(html, wait_until='networkidle')
            path = str(OUT / label.get('out', f"{label['name']}-300dpi.png"))
            await page_obj.screenshot(path=path, full_page=False, omit_background=(label.get('bg') == 'transparent'))
            await page_obj.close()
            print(f'  ok  {label["name"]}')
            png_files.append(path)

        await browser.close()
        server.shutdown()

        # Combine into PDF
        pdf_path = str(OUT / 'SteelStag-Labels-PrintReady.pdf')
        with open(pdf_path, 'wb') as f:
            f.write(img2pdf.convert(png_files))
        print(f"PDF saved -> {pdf_path}")

asyncio.run(render())

