#!/usr/bin/env python3
"""
Re-adds the Pan-India dispatch banner at the TOP of every page (inside
<div class="sticky-stack">, same spot as the original), navy color,
with the mobile-compact CSS rule. Idempotent.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = 'id="panIndiaBanner"'

BANNER_HTML = (
    '<div id="panIndiaBanner" class="pi-dispatch-banner" style="background:var(--ink);color:#fff;'
    'font-family:\'Barlow\',sans-serif;font-weight:700;font-size:0.78rem;letter-spacing:0.01em;'
    'text-align:center;padding:9px 14px;line-height:1.45;">Pan-India Fast Dispatch &nbsp;|&nbsp; '
    'Ready Stock for Industrial Combustion &amp; Gas Equipment &nbsp;|&nbsp; Surface &amp; Air Cargo Available</div>\n'
)

ANCHOR = '<div class="sticky-stack">\n'

MOBILE_CSS = "@media (max-width:560px){ .pi-dispatch-banner{ font-size:0.66rem !important; padding:7px 10px !important; letter-spacing:0 !important; } }"
CSS_ANCHOR_VARIANTS = [
    '@media (max-width:560px){ .topbar .wrap{ gap:14px; } }',
    '@media (max-width:520px){ .topbar .wrap{ gap:16px; } .topbar a span{ display:inline; } }',
]

def process(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if MARKER in content:
        return False
    if ANCHOR not in content:
        print('  SKIP (no sticky-stack anchor):', path)
        return False
    content = content.replace(ANCHOR, ANCHOR + BANNER_HTML, 1)
    if 'pi-dispatch-banner{ font-size' not in content:
        for anchor in CSS_ANCHOR_VARIANTS:
            if anchor in content:
                content = content.replace(anchor, anchor + '\n' + MOBILE_CSS, 1)
                break
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    changed = 0
    for name in ('index.html', 'about.html', 'contact.html'):
        p = os.path.join(ROOT, name)
        if os.path.exists(p) and process(p):
            changed += 1
    for folder in ('products', 'categories', 'brands', 'industrial-supply'):
        d = os.path.join(ROOT, folder)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.html') and process(os.path.join(d, fn)):
                changed += 1
    print('changed', changed, 'files')

if __name__ == '__main__':
    main()
