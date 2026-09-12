"""
Builds the SteelStag manufacturer package ZIP from the pack folder, and syncs
the portal's display assets from the same source.

The v1.2 ZIP was assembled by hand and had silently drifted: it was missing the
README, three of the four neck labels, all four size stickers and the dark logo,
and its folder layout did not match the layout the README described. This script
exists so that can't happen again -- it zips a declared manifest and fails loudly
if anything named in that manifest is missing.

Run order for a full release:
    python render-labels-win.py        # 02-Labels artwork + print-ready PDF
    python generate_color_assets.py    # 04-ColorReference artwork
    python generate_pouch_vector.py    # 05-Packaging vector pouch artwork
    python build_package.py --sync     # refresh manufacturer/assets from the pack
    python generate_techpack_pdf.py    # Tech Pack PDF (prints the portal page)
    python build_package.py            # build the ZIP

Usage:
    python build_package.py [--sync] [--verify-only] [--final]

--final exits non-zero unless every HANDOFF_REQUIRED file is present, so the
package cannot be issued as the final manufacturer artwork handoff while the
native Illustrator logo is still outstanding (OD-07).
"""
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

VERSION = 'v1.3'
BASE = Path(__file__).parent
PACK = BASE / 'SteelStag-ManufacturerPack-SS2026'
DOWNLOADS = BASE / 'manufacturer' / 'downloads'
ASSETS = BASE / 'manufacturer' / 'assets'
ZIP_PATH = DOWNLOADS / f'SteelStag-CompleteManufacturerPackage-SS2026-{VERSION}.zip'
ZIP_ROOT = f'SteelStag-ManufacturerPack-SS2026-{VERSION}'

# Every file that must be in the release, relative to PACK. Anything missing is
# a build failure, not a warning.
#
# This list is the answer to "what does the manufacturer actually need?".
# Deliberately NOT shipped: the full revision register
# (SteelStag-SS2026-Revision-History-*.md) is SteelStag's internal audit trail
# -- 41 change records, rejected options, open commercial decisions. The factory
# gets SteelStag-SS2026-Changes-for-Manufacturer-*.md instead, which carries the
# same practical content: what changed, what to do, what is on hold. Build
# scripts, the style library and the release gate are not shipped either.
MANIFEST = [
    'README.txt',
    f'SteelStag-SS2026-Changes-for-Manufacturer-{VERSION}.md',
    'label-viewer.html',

    f'01-TechPack/SteelStag-TechPack-SS2026-{VERSION}.pdf',
    f'01-TechPack/SteelStag-QuantityBreakdown-SS2026-{VERSION}.csv',

    f'02-Labels/SteelStag-Labels-PrintReady-{VERSION}.pdf',
    '02-Labels/Neck-Labels/NeckLabel-S-384dpi.png',
    '02-Labels/Neck-Labels/NeckLabel-M-384dpi.png',
    '02-Labels/Neck-Labels/NeckLabel-L-384dpi.png',
    '02-Labels/Neck-Labels/NeckLabel-XL-384dpi.png',
    '02-Labels/Wash-Care/WashCareLabel-384dpi.png',
    '02-Labels/Hang-Tags/HangTag-Front-384dpi.png',
    '02-Labels/Hang-Tags/HangTag-Back-384dpi.png',
    '02-Labels/Size-Stickers/SizeSticker-S-384dpi.png',
    '02-Labels/Size-Stickers/SizeSticker-M-384dpi.png',
    '02-Labels/Size-Stickers/SizeSticker-L-384dpi.png',
    '02-Labels/Size-Stickers/SizeSticker-XL-384dpi.png',
    '02-Labels/Retail-Sticker/RetailSticker-384dpi.png',

    '03-Logo/SteelStag-Logo-Transparent.png',
    '03-Logo/SteelStag-Logo-Dark.png',
    '03-Logo/SteelStag-Logo.svg',
    '03-Logo/SteelStag-Logo.pdf',
    # '03-Logo/SteelStag-Logo.ai' is appended by _manifest() once the native
    # file exists - see HANDOFF_REQUIRED / OD-07.

    '04-ColorReference/01-Jet-Black.png',
    '04-ColorReference/02-Bright-White.png',
    '04-ColorReference/03-Seaport-Teal.png',
    '04-ColorReference/04-Wild-Ginger.png',
    '04-ColorReference/05-Brown-Sugar.png',
    '04-ColorReference/Packaging-Pouch-Front-Mockup.png',
    '04-ColorReference/Packaging-Pouch-Back-Mockup.png',

    '05-Packaging/SteelStag-Pouch-Front-v1.3.ai',
    '05-Packaging/SteelStag-Pouch-Back-v1.3.ai',
]

# Portal display assets, copied from the pack so the page and the package can
# never show different artwork. (source relative to PACK, destination filename)
ASSET_SYNC = [
    ('02-Labels/Neck-Labels/NeckLabel-M-384dpi.png', 'NeckLabel-M-384dpi.png'),
    ('02-Labels/Wash-Care/WashCareLabel-384dpi.png', 'WashCareLabel-384dpi.png'),
    ('02-Labels/Hang-Tags/HangTag-Front-384dpi.png', 'HangTag-Front-384dpi.png'),
    ('02-Labels/Hang-Tags/HangTag-Back-384dpi.png', 'HangTag-Back-384dpi.png'),
    ('02-Labels/Retail-Sticker/RetailSticker-384dpi.png', 'RetailSticker-384dpi.png'),
    ('04-ColorReference/01-Jet-Black.png', '01-Jet-Black.png'),
    ('04-ColorReference/02-Bright-White.png', '02-Bright-White.png'),
    ('04-ColorReference/03-Seaport-Teal.png', '03-Seaport-Teal.png'),
    ('04-ColorReference/04-Wild-Ginger.png', '04-Wild-Ginger.png'),
    ('04-ColorReference/05-Brown-Sugar.png', '05-Brown-Sugar.png'),
    ('04-ColorReference/Packaging-Pouch-Front-Mockup.png', 'Packaging-Pouch-Front-Mockup.png'),
    ('04-ColorReference/Packaging-Pouch-Back-Mockup.png', 'Packaging-Pouch-Back-Mockup.png'),
    ('03-Logo/SteelStag-Logo-Transparent.png', 'logo.png'),
    ('03-Logo/SteelStag-Logo.svg', 'SteelStag-Logo.svg'),
    ('03-Logo/SteelStag-Logo.pdf', 'SteelStag-Logo.pdf'),
]

# Required before the package may be issued as the FINAL manufacturer artwork
# handoff. Absent -> the build still runs (so the rest stays verifiable and
# garment production is not held up) but the package is marked INTERIM and
# --final fails. See OD-07 in the revision history.
HANDOFF_REQUIRED = {
    '03-Logo/SteelStag-Logo.ai':
        'native Adobe Illustrator logo (OD-07) - produce by opening '
        'SteelStag-Logo.svg in Illustrator and Save As Adobe Illustrator (.ai), '
        'PDF-compatible on, no edits',
}

# Real file signatures, so a renamed file can't ship as the wrong format.
MAGIC = {
    '.png': b'\x89PNG\r\n\x1a\n',
    '.pdf': b'%PDF',
    '.svg': b'<svg',
    # A modern Illustrator file is a PDF container; a legacy one is PostScript.
    # Either is acceptable, a renamed PNG or SVG is not.
    '.ai': (b'%PDF', b'%!PS'),
}


def _manifest():
    """MANIFEST plus any handoff file that now exists."""
    extra = [rel for rel in HANDOFF_REQUIRED if (PACK / rel).is_file()]
    return MANIFEST + extra


def check_manifest():
    files = _manifest()
    missing = [p for p in files if not (PACK / p).is_file()]
    if missing:
        print('BUILD FAILED - missing from the pack folder:')
        for m in missing:
            print('   ', m)
        sys.exit(1)
    bad = []
    for p in files:
        want = MAGIC.get(Path(p).suffix.lower())
        if not want:
            continue
        head = (PACK / p).read_bytes()[:8]
        sigs = want if isinstance(want, tuple) else (want,)
        if not any(head.startswith(s) for s in sigs):
            bad.append(p)
    if bad:
        print('BUILD FAILED - file contents do not match the extension:')
        for b in bad:
            print('   ', b)
        sys.exit(1)
    print(f'  manifest OK - {len(files)} files present, all formats verified')


def handoff_status():
    """Returns (ready, [missing descriptions])."""
    missing = [f'{rel} - {why}' for rel, why in HANDOFF_REQUIRED.items()
               if not (PACK / rel).is_file()]
    return (not missing), missing


def report_handoff(final):
    ready, missing = handoff_status()
    print()
    if ready:
        print('  HANDOFF STATUS: READY - final manufacturer artwork handoff')
        return True
    print('  HANDOFF STATUS: INTERIM - NOT the final manufacturer artwork handoff')
    for m in missing:
        print(f'    missing: {m}')
    print('  Garment production is NOT blocked by this. Do not commit or deploy')
    print('  this package as the final handoff until the file above is added')
    print('  and the package is rebuilt.')
    if final:
        print('\n  --final requested but handoff is blocked.')
        sys.exit(2)
    return False


def sync_assets():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for src, dst in ASSET_SYNC:
        shutil.copy2(PACK / src, ASSETS / dst)
    stale = [f for f in ASSETS.iterdir()
             if f.is_file() and f.name not in {d for _, d in ASSET_SYNC}]
    for f in stale:
        f.unlink()
        print(f'  removed stale portal asset: {f.name}')
    print(f'  synced {len(ASSET_SYNC)} portal assets from the pack folder')


def build_zip():
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    for old in DOWNLOADS.glob('SteelStag-CompleteManufacturerPackage-SS2026-*.zip'):
        if old != ZIP_PATH:
            old.unlink()
            print(f'  removed superseded package: {old.name}')
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel in _manifest():
            z.write(PACK / rel, f'{ZIP_ROOT}/{rel}')
    size = ZIP_PATH.stat().st_size
    digest = hashlib.sha256(ZIP_PATH.read_bytes()).hexdigest()
    print(f'  built {ZIP_PATH.name}  ({size:,} bytes, {len(_manifest())} files)')
    print(f'  sha256 {digest}')

    with zipfile.ZipFile(ZIP_PATH) as z:
        assert z.testzip() is None, 'ZIP integrity check failed'
        names = {n for n in z.namelist()}
        for rel in _manifest():
            entry = f'{ZIP_ROOT}/{rel}'
            assert entry in names, f'missing from built ZIP: {entry}'
            assert z.read(entry) == (PACK / rel).read_bytes(), f'content mismatch: {entry}'
    print('  verified: every manifest file is byte-identical inside the ZIP')


if __name__ == '__main__':
    args = set(sys.argv[1:])
    final = '--final' in args
    print(f'SteelStag manufacturer package {VERSION}')
    check_manifest()
    if '--sync' in args:
        sync_assets()
        sys.exit(0)
    if '--verify-only' in args:
        report_handoff(final)
        sys.exit(0)
    build_zip()
    report_handoff(final)
    print('\nDone.')
