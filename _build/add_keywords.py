#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task #6: High-intent B2B keyword meta tags, site-wide.
- Product pages (256): already have <meta name="keywords">; append the two
  high-intent phrases + the exact brand/model code if not already present.
- Category pages (96) and Brand pages (14): have NO keywords meta tag yet;
  insert one right after <meta name="description">.
- index.html / about.html / contact.html: already have keywords; append
  the two high-intent phrases if missing.
Idempotent: re-running does not duplicate phrases already present.
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHRASE_1 = 'Authorized Supplier Pan India'
PHRASE_2 = 'Industrial Gas Train Spares Supplier India'

with open('/tmp/products_full.json', encoding='utf-8') as f:
    PRODUCTS = {p['id']: p for p in json.load(f)}

def append_keywords(content, extra_terms):
    """Append extra_terms (list of str) to the existing keywords meta tag content,
    skipping any already present (case-insensitive substring check)."""
    m = re.search(r'(<meta name="keywords" content=")([^"]*)(">)', content)
    if not m:
        return content, False
    existing = m.group(2)
    existing_lower = existing.lower()
    to_add = [t for t in extra_terms if t.lower() not in existing_lower]
    if not to_add:
        return content, False
    new_value = existing.rstrip(', ') + ', ' + ', '.join(to_add)
    new_tag = m.group(1) + new_value + m.group(3)
    return content[:m.start()] + new_tag + content[m.end():], True

def insert_keywords(content, terms):
    """Insert a brand-new keywords meta tag right after the description meta tag."""
    m = re.search(r'(<meta name="description" content="[^"]*">\n)', content)
    if not m:
        return content, False
    tag = '<meta name="keywords" content="' + html.escape(', '.join(terms)) + '">\n'
    return content[:m.end()] + tag + content[m.end():], True

def process_product(path, pid):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    product = PRODUCTS.get(pid)
    terms = [PHRASE_1, PHRASE_2]
    if product and product.get('code'):
        terms.append(str(product['code']))
    new_content, changed = append_keywords(content, terms)
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    return changed

def process_new_keywords(path, name_for_terms):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if 'id="clusterLinksRow"' not in content and '<meta name="keywords"' not in content:
        pass  # fine either way
    if '<meta name="keywords"' in content:
        new_content, changed = append_keywords(content, [PHRASE_1, PHRASE_2])
    else:
        terms = [name_for_terms, PHRASE_1, PHRASE_2, 'RKIC', 'R.K. Instruments & Controls', 'Surat Gujarat']
        new_content, changed = insert_keywords(content, terms)
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    return changed

def process_root(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    new_content, changed = append_keywords(content, [PHRASE_1, PHRASE_2])
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    return changed

def main():
    changed = 0
    skipped_no_data = 0

    prod_dir = os.path.join(ROOT, 'products')
    for fn in sorted(os.listdir(prod_dir)):
        if not fn.endswith('.html'):
            continue
        path = os.path.join(prod_dir, fn)
        with open(path, encoding='utf-8') as f:
            head = f.read(4000)
        if 'class="topbar"' not in head and 'topbar' not in open(path, encoding='utf-8').read():
            continue
        pid = fn[:-5]
        if pid not in PRODUCTS:
            skipped_no_data += 1
            continue
        if process_product(path, pid):
            changed += 1

    cat_dir = os.path.join(ROOT, 'categories')
    for fn in sorted(os.listdir(cat_dir)):
        if not fn.endswith('.html'):
            continue
        path = os.path.join(cat_dir, fn)
        title_m = None
        with open(path, encoding='utf-8') as f:
            c = f.read()
        tm = re.search(r'<title>([^|]*)\|', c)
        name = tm.group(1).strip() if tm else fn[:-5].replace('-', ' ').title()
        if process_new_keywords(path, name):
            changed += 1

    brand_dir = os.path.join(ROOT, 'brands')
    for fn in sorted(os.listdir(brand_dir)):
        if not fn.endswith('.html'):
            continue
        path = os.path.join(brand_dir, fn)
        with open(path, encoding='utf-8') as f:
            c = f.read()
        tm = re.search(r'<title>([^|]*)\|', c)
        name = tm.group(1).strip() if tm else fn[:-5].replace('-', ' ').title()
        if process_new_keywords(path, name):
            changed += 1

    for fn in ('index.html', 'about.html', 'contact.html'):
        path = os.path.join(ROOT, fn)
        if os.path.exists(path) and process_root(path):
            changed += 1

    print('changed', changed, 'files; skipped (no product data)', skipped_no_data)

if __name__ == '__main__':
    main()
