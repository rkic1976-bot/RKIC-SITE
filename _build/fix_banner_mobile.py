#!/usr/bin/env python3
"""
Makes the Pan-India dispatch banner (bottom, id="panIndiaBannerBottom")
compact on mobile: smaller font + tighter padding under 560px, so it
doesn't wrap to a tall 2-line block. Idempotent.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS_ANCHOR = '@media (max-width:560px){ .topbar .wrap{ gap:14px; } }'
CSS_RULE = "@media (max-width:560px){ .pi-dispatch-banner{ font-size:0.66rem !important; padding:7px 10px !important; letter-spacing:0 !important; } }"

DIV_OLD_PREFIX = '<div id="panIndiaBannerBottom" style="'
DIV_NEW_PREFIX = '<div id="panIndiaBannerBottom" class="pi-dispatch-banner" style="'

def process(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if 'panIndiaBannerBottom' not in content:
        return False
    changed = False
    if 'pi-dispatch-banner' not in content:
        if CSS_ANCHOR in content:
            content = content.replace(CSS_ANCHOR, CSS_ANCHOR + '\n' + CSS_RULE, 1)
            changed = True
        else:
            print('  SKIP (css anchor not found):', path)
            return False
        if DIV_OLD_PREFIX in content:
            content = content.replace(DIV_OLD_PREFIX, DIV_NEW_PREFIX, 1)
            changed = True
        else:
            print('  SKIP (div prefix not found):', path)
            return False
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    return changed

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
