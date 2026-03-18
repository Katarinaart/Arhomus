#!/usr/bin/env python3
"""Retarget donor Vivol webarchive HTML to ARHOMUS branded template.

Usage:
  python scripts/retarget_vivol_template.py
"""
from pathlib import Path
import plistlib
import re

SRC = Path('Vivol | Одежда для смелых женщин.webarchive')
OUT = Path('tilda/arhomus_vivol_exact_template.html')

obj = plistlib.loads(SRC.read_bytes())
html = obj['WebMainResource']['WebResourceData'].decode('utf-8', 'ignore')

# 1) Core brand substitutions
subs = {
    'Vivol | Одежда для смелых женщин': 'ARHOMUS | Conceptual clothing',
    'vivol.store': 'arhomus.tilda.ws',
    'VIVOL': 'ARHOMUS',
    'Vivol': 'ARHOMUS',
    'Одежда для смелых женщин': 'Концептуальная одежда ARHOMUS',
}
for a, b in subs.items():
    html = html.replace(a, b)

# 2) Donor asset retargeting to local ARHOMUS assets from repo
asset_map = {
    # favicons / logos
    'https://static.tildacdn.com/tild6665-3435-4830-b033-663334343739/Slide_16_9_-_939.png': 'U8_black.PNG',
    'https://static.tildacdn.com/tild6339-3537-4530-a364-613266653537/1.png': 'U8_white.PNG',
    'https://static.tildacdn.com/tild6230-6366-4161-b166-323431663365/1.png': 'U8_white.PNG',
    'https://static.tildacdn.com/tild3066-6133-4866-a335-376133623136/3.svg': 'U8_white.PNG',
    'https://static.tildacdn.com/tild3530-6262-4063-a666-323164366133/_.svg': 'U8_white.PNG',
    # hero/content imagery
    'https://static.tildacdn.com/tild3038-3766-4631-b832-313038306665/_vivol_1.jpg': 'IMG_9903.JPG',
    'https://static.tildacdn.com/tild3262-3334-4661-b832-613437323464/170A7853-min_1.png': 'IMG_9903.JPG',
    'https://static.tildacdn.com/tild6361-3732-4239-b438-336261353337/170A7816-min_2.png': 'IMG_9903.JPG',
    'https://static.tildacdn.com/tild6431-6661-4637-a431-333265613365/59119825_2.png': 'IMG_9903.JPG',
    'https://static.tildacdn.com/tild3634-3366-4630-b864-316635326362/59119826_2.jpg': 'IMG_9903.JPG',
}

for src, dst in asset_map.items():
    html = html.replace(src, dst)

# Replace any remaining donor fashion images with ARHOMUS catalog placeholder
html = re.sub(
    r'https://static\.tildacdn\.com/[^"\']+\.(?:jpg|jpeg|png)',
    'Каталог Архомус.png',
    html,
    flags=re.IGNORECASE,
)

# Restore specific neutral technical assets that should stay external
html = html.replace('Каталог Архомус.png" crossorigin="anonymous"', 'https://static.tildacdn.com/css/tilda-cart-discounts-1.0.min.css" crossorigin="anonymous"')
html = html.replace('src="Каталог Архомус.png"></script><style class="sbs-anim-keyframes"', 'src="https://static.tildacdn.com/js/tilda-cart-discounts-1.0.min.js"></script><style class="sbs-anim-keyframes"')
html = html.replace('src="Каталог Архомус.png" class="t-input-phonemask__img"', 'src="https://static.tildacdn.com/lib/flags/flags7.png" class="t-input-phonemask__img"')

# add marker
html = html.replace('</head>', '\n<meta name="arhomus-template" content="donor-vivol-retargeted">\n</head>', 1)
OUT.write_text(html, encoding='utf-8')
print(f'Wrote {OUT} ({len(html)} chars)')
