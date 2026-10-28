#!/usr/bin/env python3
"""
Adds the same Pan-India dispatch banner strip at the bottom of every page
(right above the footer), matching the one already at the top. Idempotent.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = 'id="panIndiaBannerBottom"'

BANNER_TEXT = (
    'Pan-India Fast Dispatch &nbsp;|&nbsp; Ready Stock for Industrial Combustion '
    '&amp; Gas Equipment &nbsp;|&nbsp; Surface &amp; Air Cargo Available'
)

def bottom_banner():
    return (
        f'<div {MARKER} style="background:var(--ink);color:#fff;font-family:\'Barlow\',sans-serif;'
        f'font-weight:700;font-size:0.78rem;letter-spacing:0.01em;text-align:center;padding:9px 14px;'
        f'line-height:1.45;">{BANNER_TEXT}</div>\n'
    )

FOOTER_PATTERNS = [
    re.compile(r'(\n)(<footer id="contact">)'),
    re.compile(r'(\n)(<footer id="contact-footer")'),
]

def process(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if MARKER in content:
        return False
    for pat in FOOTER_PATTERNS:
        m = pat.search(content)
        if m:
            new_content = content[:m.start()] + '\n' + bottom_banner() + content[m.start(1)+1:]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    print('  SKIP (no footer anchor found):', path)
    return False

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
