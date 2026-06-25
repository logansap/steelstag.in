"""
Regenerates 04-ColorReference assets for SteelStag SS2026:
  - 5 color swatch cards (Pantone + HEX + RGB + CMYK)
  - 1 packaging pouch mockup (Finn-style kraft + dark band)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math
from pathlib import Path

OUT = str(Path(__file__).parent / 'SteelStag-ManufacturerPack-SS2026' / '04-ColorReference')

# ── Accurate Pantone TCX → HEX ────────────────────────────────────────────────
COLORS = [
    {"num": "01", "name": "Jet Black",     "pantone": "19-0303 TCX", "hex": "#2B2926", "rgb": (43,  41,  38),  "cmyk": (0,  5,  12, 83)},
    {"num": "02", "name": "Bright White",  "pantone": "11-0601 TCX", "hex": "#EDE8E0", "rgb": (237, 232, 224), "cmyk": (0,  2,   6,  7)},
    {"num": "03", "name": "Seaport Teal",  "pantone": "17-5126 TCX", "hex": "#3A9B8C", "rgb": (58,  155, 140), "cmyk": (63,  0,  10, 39)},
    {"num": "04", "name": "Wild Ginger",   "pantone": "15-1157 TCX", "hex": "#C97B3A", "rgb": (201, 123,  58), "cmyk": (0,  39,  71, 21)},
    {"num": "05", "name": "Brown Sugar",   "pantone": "18-1048 TCX", "hex": "#8B4A2B", "rgb": (139,  74,  43), "cmyk": (0,  47,  69, 45)},
]

# Brand palette
CHARCOAL  = (30, 28, 26)
KRAFT     = (196, 168, 130)   # warm kraft paper
DARK_BAND = (28, 32, 40)      # deep navy/charcoal bottom
OFF_WHITE = (245, 241, 235)

W_CARD, H_CARD = 800, 1050   # swatch card size

# ── Font helpers ──────────────────────────────────────────────────────────────
GOLDMAN_REGULAR = r"C:\Users\anjan\AppData\Local\Microsoft\Windows\Fonts\Goldman-Regular.ttf"

def get_brand_font(size):
    return ImageFont.truetype(GOLDMAN_REGULAR, size)

def get_font(size, bold=False):
    candidates_bold   = ["georgiabd.ttf", "Georgia Bold.ttf", "timesbd.ttf", "arialbd.ttf", "calibrib.ttf"]
    candidates_normal = ["georgia.ttf", "Georgia.ttf", "times.ttf", "arial.ttf", "calibri.ttf"]
    dirs = [
        r"C:\Windows\Fonts",
        r"C:\Users\anjan\AppData\Local\Microsoft\Windows\Fonts",
    ]
    candidates = candidates_bold if bold else candidates_normal
    for d in dirs:
        for f in candidates:
            path = os.path.join(d, f)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    pass
    return ImageFont.load_default()

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def luminance(rgb):
    r, g, b = [x/255 for x in rgb]
    return 0.2126*r + 0.7152*g + 0.0722*b

def text_color(bg_rgb):
    return (255,255,255) if luminance(bg_rgb) < 0.45 else CHARCOAL

# ── 1. Color swatch cards ─────────────────────────────────────────────────────
def make_swatch(color):
    img = Image.new("RGB", (W_CARD, H_CARD), OFF_WHITE)
    draw = ImageDraw.Draw(img)

    rgb = color["rgb"]
    tc  = text_color(rgb)

    # Top header bar (brand)
    draw.rectangle([0, 0, W_CARD, 60], fill=CHARCOAL)
    f_hdr = get_brand_font(18)
    draw.text((W_CARD//2, 30), "SteelStag™  ·  SS2026", font=f_hdr, fill=(180,170,155), anchor="mm")

    # Large color swatch block
    SWATCH_TOP, SWATCH_BTM = 60, 650
    draw.rectangle([0, SWATCH_TOP, W_CARD, SWATCH_BTM], fill=rgb)

    # Subtle inner shadow at swatch bottom
    for i in range(12):
        alpha = int(40 * (i / 12))
        draw.rectangle([0, SWATCH_BTM - 12 + i, W_CARD, SWATCH_BTM - 12 + i + 1],
                       fill=(*CHARCOAL, alpha))

    # Color number watermark on swatch
    f_num = get_font(120, bold=True)
    num_tc = (*tc, 25)
    # Draw as grey ghost
    draw.text((W_CARD//2, (SWATCH_TOP + SWATCH_BTM)//2), color["num"],
              font=f_num, fill=(*tc[:3], 18), anchor="mm")

    # ── Info panel ────────────────────────────────────────────────────────────
    INFO_TOP = SWATCH_BTM + 10
    draw.rectangle([0, SWATCH_BTM, W_CARD, H_CARD], fill=OFF_WHITE)

    # Divider stripe (swatch color)
    draw.rectangle([0, SWATCH_BTM, W_CARD, SWATCH_BTM + 6], fill=rgb)

    # Color name
    f_name = get_font(52, bold=True)
    draw.text((60, INFO_TOP + 30), color["name"], font=f_name, fill=CHARCOAL)

    # Season label
    f_small = get_font(16)
    draw.text((60, INFO_TOP + 96), "SteelStag  ·  Spring / Summer 2026", font=get_brand_font(16), fill=(150,140,130))

    # Separator
    draw.rectangle([60, INFO_TOP + 120, W_CARD - 60, INFO_TOP + 121], fill=(200,195,185))

    # Colour specs grid
    specs = [
        ("PANTONE",  color["pantone"]),
        ("HEX",      color["hex"].upper()),
        ("RGB",      f'{color["rgb"][0]}  {color["rgb"][1]}  {color["rgb"][2]}'),
        ("CMYK",     f'{color["cmyk"][0]}  {color["cmyk"][1]}  {color["cmyk"][2]}  {color["cmyk"][3]}'),
    ]
    f_label = get_font(14)
    f_value = get_font(22, bold=True)
    col_positions = [60, 310, 560, 680]   # not used; do rows
    y = INFO_TOP + 138
    for label, value in specs:
        draw.text((60, y), label, font=f_label, fill=(160,150,135))
        draw.text((60, y + 18), value, font=f_value, fill=CHARCOAL)
        y += 64

    # Small color chip in bottom-right
    CHIP = 80
    chip_x, chip_y = W_CARD - 60 - CHIP, INFO_TOP + 138
    draw.rectangle([chip_x, chip_y, chip_x + CHIP, chip_y + CHIP], fill=rgb)
    draw.rectangle([chip_x, chip_y, chip_x + CHIP, chip_y + CHIP], outline=(200,195,185), width=1)

    # Footer
    draw.rectangle([0, H_CARD - 36, W_CARD, H_CARD], fill=CHARCOAL)
    draw.text((W_CARD//2, H_CARD - 18), "steelstag.in  ·  Color Reference  ·  Not for final colour matching — verify with physical Pantone swatch",
              font=f_label, fill=(130,120,110), anchor="mm")

    fname = os.path.join(OUT, f'{color["num"]}-{color["name"].replace(" ","-")}.png')
    img.save(fname, dpi=(300,300))
    print(f"  Saved: {os.path.basename(fname)}")


# ── 2. Packaging pouch mockup ─────────────────────────────────────────────────
def make_pouch():
    W, H = 900, 1200
    img = Image.new("RGB", (W, H), (220, 215, 208))  # light grey bg
    draw = ImageDraw.Draw(img)

    # Pouch outline (rounded rect)
    PAD = 55
    PW, PH = W - 2*PAD, H - 2*PAD
    R = 32  # corner radius

    def draw_rounded_rect(d, x0, y0, x1, y1, r, fill):
        d.rectangle([x0+r, y0, x1-r, y1], fill=fill)
        d.rectangle([x0, y0+r, x1, y1-r], fill=fill)
        d.ellipse([x0, y0, x0+2*r, y0+2*r], fill=fill)
        d.ellipse([x1-2*r, y0, x1, y0+2*r], fill=fill)
        d.ellipse([x0, y1-2*r, x0+2*r, y1], fill=fill)
        d.ellipse([x1-2*r, y1-2*r, x1, y1], fill=fill)

    # Main pouch body — kraft
    draw_rounded_rect(draw, PAD, PAD, PAD+PW, PAD+PH, R, KRAFT)

    # Dark band — bottom ~35% (visual mockup proportion)
    DARK_BAND = (26, 26, 26)   # matte black #1A1A1A
    BAND_Y = PAD + int(PH * 0.65)
    draw.rectangle([PAD, BAND_Y, PAD+PW, PAD+PH], fill=DARK_BAND)
    # Clip bottom corners
    draw_rounded_rect(draw, PAD, BAND_Y - R, PAD+PW, PAD+PH, R, DARK_BAND)

    # Top zip area — slightly darker kraft strip
    ZIP_H = 80
    draw.rectangle([PAD, PAD, PAD+PW, PAD+ZIP_H], fill=(175, 148, 110))

    # Top banner (small dark rectangle like Finn)
    BANNER_W = 320
    BX = PAD + (PW - BANNER_W)//2
    BY = PAD + 10
    draw.rectangle([BX, BY, BX+BANNER_W, BY+52], fill=DARK_BAND)
    f_url = get_brand_font(17)
    draw.text((BX + BANNER_W//2, BY+26), "steelstag.in", font=f_url, fill=(180,170,155), anchor="mm")

    # Zip perforations
    for xi in range(PAD + 20, PAD + PW - 10, 18):
        draw.ellipse([xi, PAD + ZIP_H - 8, xi+4, PAD + ZIP_H - 4], fill=(155, 128, 95))

    # Load stag logo and paste onto kraft area
    logo_path = str(Path(__file__).parent / 'SteelStag-ManufacturerPack-SS2026' / '03-Logo' / 'SteelStag-Logo-Transparent.png')
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        # Darken logo to match kraft contrast (multiply to charcoal)
        logo_size = 340
        logo = logo.resize((logo_size, int(logo_size * logo.height / logo.width)), Image.LANCZOS)
        # Tint logo charcoal
        r2,g2,b2,a2 = logo.split()
        dark_logo = Image.merge("RGBA", [
            Image.eval(r2, lambda x: int(x * 0.18)),
            Image.eval(g2, lambda x: int(x * 0.16)),
            Image.eval(b2, lambda x: int(x * 0.14)),
            a2
        ])
        logo_x = PAD + (PW - dark_logo.width)//2
        kraft_mid = PAD + int(PH * 0.45) // 2
        logo_y = PAD + ZIP_H + 20
        img.paste(dark_logo, (logo_x, logo_y), dark_logo)
        text_y = logo_y + dark_logo.height + 16
    else:
        text_y = PAD + ZIP_H + 60

    # Tagline — sits just below the brand name
    f_tag = get_font(20)
    draw.text((W//2, text_y + 20), "Color. Nothing else.", font=f_tag, fill=(80,70,60), anchor="mm")

    # Subtle horizontal rule below tagline
    rule_y = text_y + 46
    draw.rectangle([W//2 - 90, rule_y, W//2 + 90, rule_y + 1], fill=(140,125,105))

    # On dark band — fabric info
    INFO_Y = BAND_Y + 55
    f_info_label = get_font(14)
    f_info_val   = get_font(19, bold=True)
    infos = [
        ("FABRIC", "100% Combed Cotton"),
        ("GSM",    "125"),
        ("ORIGIN", "Made in India"),
    ]
    col_w = PW // 3
    for i, (lbl, val) in enumerate(infos):
        cx = PAD + col_w * i + col_w//2
        draw.text((cx, INFO_Y), lbl, font=f_info_label, fill=(120,115,105), anchor="mm")
        draw.text((cx, INFO_Y + 28), val, font=f_info_val, fill=(220,215,205), anchor="mm")
        if i < 2:
            draw.rectangle([PAD + col_w*(i+1) - 1, INFO_Y - 14, PAD + col_w*(i+1), INFO_Y + 54],
                           fill=(55, 58, 68))

    # Bottom of dark band — intentionally left clean

    # Pouch border / shadow suggestion
    draw_rounded_rect(draw, PAD-1, PAD-1, PAD+PW+1, PAD+PH+1, R+1, None)  # skip — just outline
    # Thin outline
    for offset in range(1, 3):
        draw.rectangle([PAD+R, PAD-offset, PAD+PW-R, PAD], fill=(160,150,135))
        draw.rectangle([PAD+R, PAD+PH, PAD+PW-R, PAD+PH+offset], fill=(100,95,88))

    out_path = os.path.join(OUT, "Packaging-Pouch-Mockup.png")
    img.save(out_path, dpi=(300,300))
    print(f"  Saved: Packaging-Pouch-Mockup.png")


# ── Run ───────────────────────────────────────────────────────────────────────
print("Generating color swatches...")
for c in COLORS:
    make_swatch(c)

print("\nGenerating packaging pouch mockup...")
make_pouch()

print("\nDone. All assets saved to 04-ColorReference/")
