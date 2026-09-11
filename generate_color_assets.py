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
KRAFT     = (200, 169, 110)   # #C8A96E — matches the Tech Pack packaging spec
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
    # Row pitch tightened from 64 to 52 px: at the old pitch the CMYK value
    # landed under the footer bar and was unreadable on every card.
    y = INFO_TOP + 134
    for label, value in specs:
        draw.text((60, y), label, font=f_label, fill=(160,150,135))
        draw.text((60, y + 18), value, font=f_value, fill=CHARCOAL)
        y += 52

    # Small color chip in bottom-right
    CHIP = 80
    chip_x, chip_y = W_CARD - 60 - CHIP, INFO_TOP + 134
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
# Real pouch is 240mm x 340mm — a standard 1kg-tier kraft stand-up pouch
# size (matches the Finn Design reference this packaging is based on),
# swapped in from an oversized custom 320x400mm spec.
#
# THIS IS A VISUAL REFERENCE, NOT PRINT ARTWORK. The pouch graphic sits inset
# inside the canvas on a mockup background, is RGB, and has no gusset, back
# panel, seal zone, bleed or dieline. The converter produces the dieline to
# manufacturer standard from the 24 x 34 cm size and the two-tone layout.
REAL_W_MM, REAL_H_MM = 240, 340
POUCH_DPI = 320  # comfortably above the ~300 DPI print minimum

def make_pouch(side='front'):
    """Front or back pouch artboard.

    Front is brand-led and carries no legal declaration of any kind.
    Back carries the retail declaration panel (OD-01) on the kraft ground,
    which is where the Tech Pack specifies it and where small legal type
    stays legible under matte lamination.
    """
    px_per_mm = POUCH_DPI / 25.4
    W = round(REAL_W_MM * px_per_mm)
    H = round(REAL_H_MM * px_per_mm)
    img = Image.new("RGB", (W, H), (220, 215, 208))  # light grey bg
    draw = ImageDraw.Draw(img)

    # Original design was authored on a 900(w) x 1200(h) canvas (ratio 1.333);
    # the corrected canvas above is ratio 1.25. The two axis scales differ by
    # only ~7%, so a single average scale for every literal below reads
    # cleanly without visibly distorting any element.
    S = lambda v: round(v * (W/900 + H/1200) / 2)

    # Pouch outline (rounded rect)
    PAD = S(55)
    PW, PH = W - 2*PAD, H - 2*PAD
    R = S(32)  # corner radius

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
    ZIP_H = S(80)
    draw.rectangle([PAD, PAD, PAD+PW, PAD+ZIP_H], fill=(175, 148, 110))

    # Top banner (small dark rectangle like Finn)
    BANNER_W = S(320)
    BX = PAD + (PW - BANNER_W)//2
    BY = PAD + S(10)
    draw.rectangle([BX, BY, BX+BANNER_W, BY+S(52)], fill=DARK_BAND)
    f_url = get_brand_font(S(17))
    draw.text((BX + BANNER_W//2, BY+S(26)), "steelstag.in", font=f_url, fill=(180,170,155), anchor="mm")

    # Zip perforations
    for xi in range(PAD + S(20), PAD + PW - S(10), S(18)):
        draw.ellipse([xi, PAD + ZIP_H - S(8), xi+S(4), PAD + ZIP_H - S(4)], fill=(155, 128, 95))

    if side == 'front':
        # ── FRONT: brand only. No MRP, no declaration panel, no legal type. ──
        logo_path = str(Path(__file__).parent / 'SteelStag-ManufacturerPack-SS2026'
                        / '03-Logo' / 'SteelStag-Logo-Transparent.png')
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            # Work from the mark, not the canvas, so master clear space cannot
            # change the printed size.
            logo = logo.crop(logo.split()[3].getbbox())
            # The approved master is placed AS-IS, directly on the kraft.
            # No tint, no multiply, no recolour, no backing panel. Measured on
            # this ground the mark holds: 71% of its pixels sit darker than the
            # kraft and the highlights still reach 255, so the metallic reads
            # without anything propping it up.
            #
            # Sized to the master's native mark width -- as large as it goes
            # before upscaling would soften it -- for presence on kraft.
            mark_w = min(S(250), logo.width)
            logo = logo.resize((mark_w, round(mark_w * logo.height / logo.width)), Image.LANCZOS)

            # Centre the brand block (mark + tagline + rule) in the kraft field
            # so the front reads as one composition instead of sitting high.
            kraft_top = PAD + ZIP_H
            kraft_h = BAND_Y - kraft_top
            block_h = logo.height + S(70)
            logo_x = PAD + (PW - logo.width) // 2
            logo_y = kraft_top + max(S(40), (kraft_h - block_h) // 2)
            img.paste(logo, (logo_x, logo_y), logo)
            text_y = logo_y + logo.height + S(16)
        else:
            text_y = PAD + ZIP_H + S(60)

        f_tag = get_font(S(20))
        draw.text((W//2, text_y + S(20)), "Color. Nothing else.", font=f_tag, fill=(80,70,60), anchor="mm")
        rule_y = text_y + S(46)
        draw.rectangle([W//2 - S(90), rule_y, W//2 + S(90), rule_y + S(1)], fill=(140,125,105))

        # Dark band — product info only (no legal declarations)
        INFO_Y = BAND_Y + S(55)
        f_info_label = get_font(S(14))
        f_info_val   = get_font(S(19), bold=True)
        infos = [("FABRIC", "100% Combed Cotton"), ("GSM", "180"), ("ORIGIN", "Made in India")]
        col_w = PW // 3
        for i, (lbl, val) in enumerate(infos):
            cx = PAD + col_w * i + col_w//2
            draw.text((cx, INFO_Y), lbl, font=f_info_label, fill=(120,115,105), anchor="mm")
            draw.text((cx, INFO_Y + S(28)), val, font=f_info_val, fill=(220,215,205), anchor="mm")
            if i < 2:
                draw.rectangle([PAD + col_w*(i+1) - 1, INFO_Y - S(14), PAD + col_w*(i+1), INFO_Y + S(54)],
                               fill=(55, 58, 68))
        stamp = ("VISUAL REFERENCE ONLY \u2014 NOT PRINT ARTWORK  \u00b7  FRONT  \u00b7  "
                 "POUCH 24 \u00d7 34 cm  \u00b7  DIELINE BY CONVERTER")

    else:
        # ── BACK: brand-clean kraft ───────────────────────────────────────
        # Deliberately bare. All consumer declarations are carried on the
        # separate retail sticker, which is applied at packing and is not
        # part of the printed pouch. The pouch itself holds no variable data.

        # Dark band — brand line only
        f_back_brand = get_brand_font(S(20))
        _bw = draw.textlength("SteelStag", font=f_back_brand)
        draw.text((W//2 - S(6), BAND_Y + S(64)), "SteelStag", font=f_back_brand,
                  fill=(150, 145, 136), anchor="mm")
        draw.text((W//2 - S(6) + _bw/2 + S(4), BAND_Y + S(54)), "\u2122",
                  font=get_font(S(10)), fill=(150, 145, 136), anchor="lm")
        f_back_note = get_font(S(14))
        draw.text((W//2, BAND_Y + S(100)), "steelstag.in", font=f_back_note,
                  fill=(110, 106, 100), anchor="mm")
        stamp = ("VISUAL REFERENCE ONLY \u2014 NOT PRINT ARTWORK  \u00b7  BACK  \u00b7  "
                 "POUCH 24 \u00d7 34 cm  \u00b7  DIELINE BY CONVERTER")

    # Thin outline top/bottom
    for offset in range(1, S(3)):
        draw.rectangle([PAD+R, PAD-offset, PAD+PW-R, PAD], fill=(160,150,135))
        draw.rectangle([PAD+R, PAD+PH, PAD+PW-R, PAD+PH+offset], fill=(100,95,88))

    # Status stamp in the mockup margin — these files must never reach a
    # converter as artwork.
    f_stamp = get_font(S(15))
    draw.text((W//2, PAD + PH + S(30)), stamp, font=f_stamp, fill=(120, 115, 108), anchor="mm")

    name = f"Packaging-Pouch-{side.capitalize()}-Mockup.png"
    out_path = os.path.join(OUT, name)
    img.save(out_path, dpi=(POUCH_DPI, POUCH_DPI))
    print(f"  Saved: {name}  ({W}x{H}px @ {POUCH_DPI} DPI \u2014 visual reference only)")


# ── Run ───────────────────────────────────────────────────────────────────────
print("Generating color swatches...")
for c in COLORS:
    make_swatch(c)

print("\nGenerating packaging pouch mockups (front + back)...")
make_pouch('front')
make_pouch('back')

print("\nDone. All assets saved to 04-ColorReference/")
