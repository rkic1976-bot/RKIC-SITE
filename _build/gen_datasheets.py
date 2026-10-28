#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates a single-page branded technical PDF datasheet per product from
products-data.js data (specs table, description, product photo).
Output: /datasheets/<product-id>.pdf
"""
import json, os, io
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'datasheets')
os.makedirs(OUT_DIR, exist_ok=True)

INK = colors.HexColor('#33414E')
FLAME = colors.HexColor('#C5432F')
SAGE = colors.HexColor('#855E1C')
LINE = colors.HexColor('#D5D2C4')
PAPER = colors.HexColor('#F7F5EE')
DIM = colors.HexColor('#5B6B78')

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

def wrap_text(text, font, size, max_width):
    words = text.split()
    lines = []
    cur = ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if stringWidth(test, font, size) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def find_image(product):
    for key in ('imageLarge', 'image'):
        rel = product.get(key)
        if not rel:
            continue
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            return p
    return None

def draw_header(c, product):
    # top brand bar
    c.setFillColor(INK)
    c.rect(0, PAGE_H - 24*mm, PAGE_W, 24*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MARGIN, PAGE_H - 11*mm, 'R.K. Instruments & Controls')
    c.setFont('Helvetica', 8)
    c.drawString(MARGIN, PAGE_H - 16*mm, 'FLOW & FLAME CONTROL  |  Office No. 12, 1st Floor, Dhamanwala Service Complex, G.I.D.C., Pandesara, Surat - 394221, Gujarat, India')
    c.drawString(MARGIN, PAGE_H - 20*mm, 'Phone: +91 9824136145   Email: rkic1976@gmail.com   Web: www.rkic.in')
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(colors.white)
    label = 'TECHNICAL DATASHEET'
    w = stringWidth(label, 'Helvetica-Bold', 8)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 11*mm, label)

def draw_footer(c, product):
    c.setFillColor(LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN, 14*mm, PAGE_W - MARGIN, 14*mm)
    c.setFillColor(DIM)
    c.setFont('Helvetica', 7)
    c.drawString(MARGIN, 10.5*mm, 'GSTIN: 24ADPPK7006A1ZY   |   MSME/Udyam: UDYAM-GJ-22-0126661   |   D-U-N-S: 920713349   |   GeM Seller ID: 3VSX240012704275')
    c.drawString(MARGIN, 7*mm, 'Price available on request. 100% GST compliant B2B invoicing with E-Way Bill support for all states. Pan-India dispatch.')
    c.setFont('Helvetica', 6.3)
    c.drawRightString(PAGE_W - MARGIN, 3.3*mm, 'www.rkic.in/products/' + product['id'])

def build_pdf(product, out_path):
    c = canvas.Canvas(out_path, pagesize=A4)
    draw_header(c, product)

    y = PAGE_H - 32*mm

    # Title block
    c.setFillColor(INK)
    c.setFont('Helvetica-Bold', 15)
    title_lines = wrap_text(product['name'], 'Helvetica-Bold', 15, PAGE_W - 2*MARGIN)
    for line in title_lines[:2]:
        c.drawString(MARGIN, y, line)
        y -= 6.2*mm

    c.setFont('Helvetica', 9.5)
    c.setFillColor(DIM)
    meta_bits = []
    if product.get('brand'): meta_bits.append('Brand: ' + product['brand'])
    if product.get('code'): meta_bits.append('Code/Part No.: ' + str(product['code']))
    if product.get('category'): meta_bits.append('Category: ' + product['category'])
    c.drawString(MARGIN, y, '   |   '.join(meta_bits))
    y -= 9*mm

    # Image box (right side)
    img_box_w = 70*mm
    img_box_h = 70*mm
    img_x = PAGE_W - MARGIN - img_box_w
    img_y = y - img_box_h + 4*mm
    c.setStrokeColor(LINE)
    c.setFillColor(colors.white)
    c.rect(img_x, img_y, img_box_w, img_box_h, fill=1, stroke=1)
    img_path = find_image(product)
    if img_path:
        try:
            pil_img = Image.open(img_path).convert('RGB')
            pil_img.thumbnail((500, 500), Image.LANCZOS)
            buf = io.BytesIO()
            pil_img.save(buf, format='JPEG', quality=82)
            buf.seek(0)
            img = ImageReader(buf)
            iw, ih = pil_img.size
            scale = min((img_box_w - 6*mm) / iw, (img_box_h - 6*mm) / ih)
            dw, dh = iw * scale, ih * scale
            c.drawImage(img, img_x + (img_box_w - dw)/2, img_y + (img_box_h - dh)/2,
                        width=dw, height=dh, mask='auto')
        except Exception:
            pass

    # Specs table (left side, next to image)
    specs = product.get('specs') or {}
    table_w = PAGE_W - 2*MARGIN - img_box_w - 8*mm
    sx = MARGIN
    sy = y + 4*mm
    c.setFont('Helvetica-Bold', 9.5)
    c.setFillColor(INK)
    c.drawString(sx, sy, 'Specifications')
    sy -= 6*mm
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    row_h = 6.2*mm
    c.setFont('Helvetica', 8.3)
    for k, v in specs.items():
        if sy < 40*mm:
            break  # safety; specs are short in this dataset
        c.setFillColor(DIM)
        klines = wrap_text(str(k), 'Helvetica', 7.6, table_w * 0.40)[:2]
        ky = sy
        c.setFont('Helvetica', 7.6)
        for kl in klines:
            c.drawString(sx, ky, kl)
            ky -= 3.8*mm
        c.setFillColor(INK)
        vtext = str(v)
        vlines = wrap_text(vtext, 'Helvetica-Bold', 8.3, table_w * 0.58)[:2]
        c.setFont('Helvetica-Bold', 8.3)
        vy = sy
        for vl in vlines:
            c.drawString(sx + table_w * 0.42, vy, vl)
            vy -= 4.2*mm
        c.setFont('Helvetica', 8.3)
        n_lines = max(len(klines), len(vlines))
        c.line(sx, sy - (n_lines * 4.2)*mm + 2*mm, sx + table_w, sy - (n_lines * 4.2)*mm + 2*mm)
        sy -= row_h if n_lines <= 1 else row_h + (n_lines - 1) * 4.2*mm

    # Description
    desc_y = min(img_y, sy) - 10*mm
    c.setFont('Helvetica-Bold', 9.5)
    c.setFillColor(INK)
    c.drawString(MARGIN, desc_y, 'Description')
    desc_y -= 5.5*mm
    c.setFont('Helvetica', 8.3)
    c.setFillColor(DIM)
    desc = product.get('description') or ''
    for line in wrap_text(desc, 'Helvetica', 8.3, PAGE_W - 2*MARGIN):
        if desc_y < 24*mm:
            break
        c.drawString(MARGIN, desc_y, line)
        desc_y -= 4.6*mm

    # Media compatibility line (generic, since not in dataset per-product)
    desc_y -= 2*mm
    if desc_y > 20*mm:
        c.setFont('Helvetica-Oblique', 7.6)
        c.setFillColor(DIM)
        c.drawString(MARGIN, desc_y, 'Typical media compatibility: CNG, PNG, LPG, Air, Nitrogen — confirm against application before installation.')

    draw_footer(c, product)
    c.showPage()
    c.save()

def main():
    with open('/tmp/products_full.json') as f:
        products = json.load(f)
    count = 0
    for p in products:
        out_path = os.path.join(OUT_DIR, p['id'] + '.pdf')
        build_pdf(p, out_path)
        count += 1
    print('generated', count, 'datasheets ->', OUT_DIR)

if __name__ == '__main__':
    main()
