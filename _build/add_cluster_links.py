#!/usr/bin/env python3
"""
Idempotently inserts a small "Industrial Clusters We Serve" internal-link
row into the existing #panIndiaService section (right after the GSTIN/MSME/
DUNS/GeM badge chips, before the closing </div></section>), on every page
that already has that section. Links point at the 4 new SEO cluster pages
under /industrial-supply/.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = 'id="clusterLinksRow"'

CLUSTERS = [
    ('Morbi Ceramic Zone', 'morbi-ceramic-zone'),
    ('Pune Auto Hub', 'pune-auto-hub'),
    ('Ahmedabad–Vapi Chemical Belt', 'ahmedabad-vapi-chemical-belt'),
    ('Faridabad / NCR', 'faridabad-ncr'),
]

BADGE_END = '''      <span style="border:1px solid var(--line);border-radius:20px;padding:6px 13px;">GeM Seller ID: 3VSX240012704275</span>
    </div>'''

def links_row(prefix):
    chips = ''.join(
        f'<a href="{prefix}industrial-supply/{slug}" style="border:1px solid var(--line);border-radius:20px;padding:6px 13px;color:var(--ink);text-decoration:none;">{name}</a>'
        for name, slug in CLUSTERS
    )
    return (
        BADGE_END
        + f'\n    <div {MARKER} style="display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;font-family:\'IBM Plex Mono\',monospace;font-size:0.7rem;">\n'
        + f'      <span style="color:var(--text-dim);align-self:center;">Industrial Clusters We Serve:</span>\n'
        + f'      {chips}\n'
        + '    </div>'
    )

def process(path, prefix):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if 'id="panIndiaService"' not in content:
        return False
    if MARKER in content:
        return False
    if BADGE_END not in content:
        print('  SKIP (badge anchor not found):', path)
        return False
    new_content = content.replace(BADGE_END, links_row(prefix), 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    changed = 0
    for name in ('index.html', 'about.html', 'contact.html'):
        p = os.path.join(ROOT, name)
        if os.path.exists(p) and process(p, ''):
            changed += 1
    for folder in ('products', 'categories', 'brands'):
        d = os.path.join(ROOT, folder)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.html'):
                continue
            if process(os.path.join(d, fn), '../'):
                changed += 1
    print('changed', changed, 'files')

if __name__ == '__main__':
    main()
