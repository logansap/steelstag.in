"""
Generate TechPack PDF from the manufacturer portal HTML.
The portal is the single source of truth — run this script after
any content changes to regenerate the PDF.

Output: manufacturer/downloads/SteelStag-TechPack-SS2026-v1.0.pdf
        SteelStag-ManufacturerPack-SS2026/01-TechPack/SteelStag-TechPack-SS2026.pdf
"""
import asyncio, sys, subprocess, threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

BASE = Path(__file__).parent
HTML = BASE / 'manufacturer' / 'index.html'
OUTS = [
    BASE / 'manufacturer' / 'downloads' / 'SteelStag-TechPack-SS2026-v1.0.pdf',
    BASE / 'SteelStag-ManufacturerPack-SS2026' / '01-TechPack' / 'SteelStag-TechPack-SS2026.pdf',
]

PORT = 8932

try:
    from playwright.async_api import async_playwright
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'playwright', '-q'])
    subprocess.check_call([sys.executable, '-m', 'playwright', 'install', 'chromium', '--quiet'])
    from playwright.async_api import async_playwright


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE), **kwargs)


def start_server():
    server = HTTPServer(('localhost', PORT), SilentHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


async def render():
    server = start_server()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f'http://localhost:{PORT}/manufacturer/index.html',
                        wait_until='networkidle')
        # Wait for Google Fonts to load
        await page.wait_for_timeout(1500)
        pdf_bytes = await page.pdf(
            format='A4',
            margin={'top': '18mm', 'right': '22mm', 'bottom': '18mm', 'left': '22mm'},
            print_background=True,
        )
        await browser.close()
    server.shutdown()

    for out in OUTS:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(pdf_bytes)
        print(f'  saved → {out.relative_to(BASE)}  ({len(pdf_bytes)//1024} KB)')

    print('Done.')


asyncio.run(render())
