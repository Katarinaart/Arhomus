#!/usr/bin/env python3
from pathlib import Path
import re

SRC = Path('tilda/arhomus_vivol_exact_template.html')
OUT_DIR = Path('tilda')
MAX_CHARS = 220_000

text = SRC.read_text(encoding='utf-8')
m = re.search(r'<body[^>]*>(.*)</body>', text, flags=re.S | re.I)
body = m.group(1) if m else text

# First try split by Tilda record boundaries
chunks = []
if '<!--/record-->' in body:
    pieces = re.split(r'(<!--/record-->)', body)
    records, buf = [], ''
    for p in pieces:
        buf += p
        if p == '<!--/record-->':
            records.append(buf)
            buf = ''
    if buf:
        records.append(buf)

    cur = ''
    for rec in records:
        if cur and len(cur) + len(rec) > MAX_CHARS:
            chunks.append(cur)
            cur = rec
        else:
            cur += rec
    if cur:
        chunks.append(cur)

# If still too big or no markers: hard split near closing tag
if not chunks or max(len(c) for c in chunks) > MAX_CHARS:
    chunks = []
    i = 0
    n = len(body)
    while i < n:
        j = min(i + MAX_CHARS, n)
        if j < n:
            k = body.rfind('</div>', i, j)
            if k != -1 and k > i + MAX_CHARS // 2:
                j = k + len('</div>')
        chunks.append(body[i:j])
        i = j

for idx, chunk in enumerate(chunks, 1):
    out = OUT_DIR / f'arhomus_vivol_t123_part{idx}.html'
    out.write_text(f'<!-- ARHOMUS donor template part {idx}/{len(chunks)} -->\n' + chunk, encoding='utf-8')

print('body length:', len(body))
print('chunks:', len(chunks), [len(c) for c in chunks])
