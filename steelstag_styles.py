"""
SteelStag style library and per-collection order scope.

Two separate things live here, and keeping them separate is the point:

  STYLE_LIBRARY   Permanent, reusable style definitions. A style stays here
                  for good once it has been developed, whether or not it is
                  being produced right now. This is brand design knowledge,
                  not order data.

  COLLECTIONS     Which styles a given collection/order actually produces.
                  Only styles listed in a collection's `active_styles` may
                  appear in that collection's Tech Pack, package or artwork.

ST-DS-002 Deep Scoop is the reason this file exists. It was developed and
fully specified, then dropped from the SS2026 bulk order. The old Tech Pack
generator had no way to express "developed but not in this order", so it kept
emitting Deep Scoop alongside the two styles actually being made — a live
source of contradiction for the factory. Deleting the style would have thrown
away the pattern work; leaving it in the generator kept shipping a third style
nobody ordered. It is retained here, marked inactive for SS2026, and available
to any future collection that switches it back on.

Consumed by verify_release.py, which fails the release if the shipped Tech Pack
mentions a style that is not active for the collection being released.
"""

# ── Style library ───────────────────────────────────────────────────────────
# Neck measurements are in inches, sizes S / M / L / XL, garment laid flat.
# Body measurements are shared across all styles and live in the Tech Pack
# (the manufacturer portal is their single source of truth); only the parts
# that genuinely differ per style are held here.

STYLE_LIBRARY = {
    'ST-RN-001': {
        'name': 'Round Neck',
        'description': "Men's Round Neck T-Shirt",
        'developed': 'SS2026',
        'neck_construction': (
            'Clean-bound / self-fabric tape - no rib band, folded self-fabric, '
            'single needle topstitch 1/8" from edge, lies flat'
        ),
        'sleeve_finish': 'Clean flat hem - twin needle, 1/4" hem, self-colour',
        'neck_measurements': {
            'Neck Width':      ('7',   '7¼', '7½', '7¾'),
            'Front Neck Drop': ('2⅞', '3', '3⅛', '3¼'),
            'Back Neck Drop':  ('1',   '1',    '1',    '1'),
            'Collar Band Ht':  ('NA',  'NA',   'NA',   'NA'),
        },
    },

    'ST-DS-002': {
        'name': 'Deep Scoop',
        'description': "Men's Deep Scoop T-Shirt",
        'developed': 'SS2026',
        # Retained for a future collection. Not part of the SS2026 bulk order.
        # Specification preserved exactly as developed - do not edit to match a
        # later season without raising a revision against that season.
        'neck_construction': (
            'Clean-bound / self-fabric tape - no rib band, folded self-fabric, '
            'single needle topstitch 1/8" from edge, lies flat'
        ),
        'sleeve_finish': 'Clean flat hem - twin needle, 1/4" hem, self-colour',
        'neck_measurements': {
            'Neck Width':      ('8',    '8½', '8¾', '9'),
            'Front Neck Drop': ('4¼', '4½', '4⅝', '4¾'),
            'Back Neck Drop':  ('1',    '1',    '1',    '1'),
            'Collar Band Ht':  ('NA',   'NA',   'NA',   'NA'),
        },
    },

    'ST-VN-003': {
        'name': 'V-Neck',
        'description': "Men's V-Neck T-Shirt",
        'developed': 'SS2026',
        'neck_construction': (
            'Clean-bound / self-fabric tape - no rib band, mitered V-point, '
            'folded self-fabric, single needle topstitch 1/8" from edge'
        ),
        'sleeve_finish': 'Clean flat hem - twin needle, 1/4" hem, self-colour',
        'neck_measurements': {
            'Neck Width':      ('6¾', '7',    '7¼', '7½'),
            'Front Neck Drop': ('3½', '3¾', '4',    '4¼'),
            'Back Neck Drop':  ('1',    '1',    '1',    '1'),
            'V-Point Depth':   ('3½', '3¾', '4',    '4¼'),
            'Collar Band Ht':  ('NA',   'NA',   'NA',   'NA'),
        },
    },
}

SIZES = ('S', 'M', 'L', 'XL')


# ── Collection / order scope ────────────────────────────────────────────────

COLLECTIONS = {
    'SS2026': {
        'title': 'SS2026 Core T-Shirt Launch',
        'version': 'v1.3',
        'active_styles': ['ST-RN-001', 'ST-VN-003'],
        'total_qty': 1200,
        'colours': ['Jet Black', 'Bright White', 'Seaport Teal',
                    'Wild Ginger', 'Brown Sugar'],
        'scope_note': (
            'ST-DS-002 Deep Scoop is retained in the style library for a future '
            'collection. It is not part of the SS2026 bulk order and must not '
            'appear in SS2026 Tech Pack content, artwork or packaging.'
        ),
    },
}

CURRENT_COLLECTION = 'SS2026'


def active_styles(collection=CURRENT_COLLECTION):
    """Style codes this collection actually produces."""
    return list(COLLECTIONS[collection]['active_styles'])


def inactive_styles(collection=CURRENT_COLLECTION):
    """Developed styles deliberately held back from this collection."""
    active = set(COLLECTIONS[collection]['active_styles'])
    return [code for code in STYLE_LIBRARY if code not in active]


def style(code):
    return STYLE_LIBRARY[code]


def describe(collection=CURRENT_COLLECTION):
    c = COLLECTIONS[collection]
    lines = [f"{collection} - {c['title']} ({c['version']}), {c['total_qty']:,} pcs", '', 'In production:']
    for code in active_styles(collection):
        lines.append(f"  {code}  {STYLE_LIBRARY[code]['name']}")
    held = inactive_styles(collection)
    if held:
        lines.append('')
        lines.append('Retained in the library, not in this order:')
        for code in held:
            lines.append(f"  {code}  {STYLE_LIBRARY[code]['name']}"
                         f"  (developed {STYLE_LIBRARY[code]['developed']})")
        lines.append('')
        lines.append(f"  {c['scope_note']}")
    return '\n'.join(lines)


if __name__ == '__main__':
    print(describe())
