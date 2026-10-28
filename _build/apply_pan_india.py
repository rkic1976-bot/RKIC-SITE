#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pan-India checklist rollout — applies banner, pan-india service section,
RFQ button, WhatsApp dynamic message, billing notice, datasheet link
across index/about/contact, all product pages, category pages, brand pages.
Idempotent: checks for marker strings before inserting.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BANNER_MARKER = 'id="panIndiaBanner"'
BANNER_HTML = '''<div id="panIndiaBanner" style="background:var(--flame);color:#fff;font-family:'Barlow',sans-serif;font-weight:700;font-size:0.78rem;letter-spacing:0.01em;text-align:center;padding:9px 14px;line-height:1.45;">Pan-India Fast Dispatch &nbsp;|&nbsp; Ready Stock for Industrial Combustion &amp; Gas Equipment &nbsp;|&nbsp; Surface &amp; Air Cargo Available</div>
'''

SERVICE_MARKER = 'id="panIndiaService"'
SERVICE_HTML = '''<section id="panIndiaService" style="padding:40px 0 8px;border-top:1px solid var(--line);">
  <div class="wrap">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--flame);">Pan-India Service</div>
    <h2 style="font-size:clamp(1.25rem,2.6vw,1.6rem);font-weight:600;margin:6px 0 0;max-width:38ch;">Ready stock, fast dispatch, GST-compliant billing &mdash; anywhere in India.</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin-top:24px;">
      <div style="border:1px solid var(--line);border-radius:4px;padding:18px;background:#fff;">
        <div style="font-weight:700;font-size:0.86rem;margin-bottom:8px;">Industries We Supply</div>
        <div style="font-size:0.84rem;color:var(--text-dim);line-height:1.8;">Textile Processing &middot; Furnaces &amp; Ovens &middot; Ceramics &middot; Forging &middot; Boilers &amp; EPC Plants</div>
      </div>
      <div style="border:1px solid var(--line);border-radius:4px;padding:18px;background:#fff;">
        <div style="font-weight:700;font-size:0.86rem;margin-bottom:8px;">Logistics &amp; Delivery Partners</div>
        <div style="font-size:0.84rem;color:var(--text-dim);line-height:1.6;">Same-day / 24-hr dispatch for ready inventory via V-Trans, TCI, Safexpress, Blue Dart.</div>
      </div>
      <div style="border:1px solid var(--line);border-radius:4px;padding:18px;background:#fff;">
        <div style="font-weight:700;font-size:0.86rem;margin-bottom:8px;">Billing</div>
        <div style="font-size:0.84rem;color:var(--text-dim);line-height:1.6;">100% GST Compliant B2B Invoicing with E-Way Bill Support for All States.</div>
      </div>
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;font-family:'IBM Plex Mono',monospace;font-size:0.68rem;color:var(--text-dim);">
      <span style="border:1px solid var(--line);border-radius:20px;padding:6px 13px;">GSTIN: 24ADPPK7006A1ZY</span>
      <span style="border:1px solid var(--line);border-radius:20px;padding:6px 13px;">MSME/Udyam: UDYAM-GJ-22-0126661</span>
      <span style="border:1px solid var(--line);border-radius:20px;padding:6px 13px;">D-U-N-S: 920713349</span>
      <span style="border:1px solid var(--line);border-radius:20px;padding:6px 13px;">GeM Seller ID: 3VSX240012704275</span>
    </div>
  </div>
</section>
'''

def insert_banner(content):
    if BANNER_MARKER in content:
        return content, False
    anchor = '<div class="sticky-stack">\n'
    if anchor not in content:
        return content, False
    content = content.replace(anchor, anchor + BANNER_HTML, 1)
    return content, True

def insert_service_before(content, footer_anchor):
    if SERVICE_MARKER in content:
        return content, False
    if footer_anchor not in content:
        return content, False
    content = content.replace(footer_anchor, SERVICE_HTML + footer_anchor, 1)
    return content, True

def process_simple(path, footer_anchor):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    c, b1 = insert_banner(c)
    c, b2 = insert_service_before(c, footer_anchor)
    if c != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
    return b1, b2

# ---------- product pages (banner + service + RFQ + WA dynamic + billing note + datasheet link) ----------

RFQ_OLD = '''<a class="pg-btn pg-btn-secondary" href="../contact">Contact Us</a>
      </div>'''

def rfq_new(product_id):
    return '''<a class="pg-btn pg-btn-secondary" href="../contact">Contact Us</a>
        <button type="button" class="pg-btn pg-btn-secondary" id="rfqOpenBtn" style="cursor:pointer;">Get a Quote (RFQ)</button>
        <a class="pg-btn pg-btn-secondary" href="../datasheets/%s.pdf" target="_blank" rel="noopener">Download Datasheet (PDF)</a>
        <div style="width:100%%;font-size:0.76rem;color:var(--text-dim);margin-top:4px;">100%% GST Compliant B2B Invoicing &middot; E-Way Bill Support for All States</div>
      </div>''' % product_id

RFQ_MODAL_MARKER = 'id="rfqModal"'
RFQ_MODAL_HTML = '''<div id="rfqModal" style="display:none;position:fixed;inset:0;background:rgba(20,20,20,0.55);z-index:9999;align-items:center;justify-content:center;padding:20px;">
  <div style="background:#fff;border-radius:6px;max-width:420px;width:100%;padding:26px;position:relative;font-family:'Barlow',sans-serif;max-height:90vh;overflow-y:auto;">
    <button type="button" id="rfqCloseBtn" aria-label="Close" style="position:absolute;top:10px;right:12px;background:none;border:none;font-size:1.2rem;cursor:pointer;color:var(--ink);">&times;</button>
    <h3 style="font-family:'Barlow Condensed',sans-serif;font-size:1.3rem;font-weight:700;margin:0 0 4px;">Request a Quote</h3>
    <p style="font-size:0.84rem;color:var(--text-dim);margin:0 0 16px;">Fill in your requirement &mdash; our technical desk will respond with pricing &amp; lead time.</p>
    <form id="rfqForm">
      <input type="hidden" name="_subject" value="RFQ Request from Website">
      <input type="hidden" name="Product" id="rfqProductField" value="">
      <input type="hidden" name="Page URL" id="rfqUrlField" value="">
      <label style="display:block;font-size:0.76rem;font-weight:600;margin:10px 0 4px;">Company Name *</label>
      <input required name="Company Name" type="text" style="width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:3px;font-size:0.88rem;font-family:inherit;box-sizing:border-box;">
      <label style="display:block;font-size:0.76rem;font-weight:600;margin:10px 0 4px;">City / State *</label>
      <input required name="City/State" type="text" style="width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:3px;font-size:0.88rem;font-family:inherit;box-sizing:border-box;">
      <label style="display:block;font-size:0.76rem;font-weight:600;margin:10px 0 4px;">Quantity Required *</label>
      <input required name="Quantity" type="text" style="width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:3px;font-size:0.88rem;font-family:inherit;box-sizing:border-box;">
      <label style="display:block;font-size:0.76rem;font-weight:600;margin:10px 0 4px;">Required Model *</label>
      <input required name="Required Model" id="rfqModelField" type="text" style="width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:3px;font-size:0.88rem;font-family:inherit;box-sizing:border-box;">
      <button type="submit" style="margin-top:16px;width:100%;background:#075E54;color:#fff;border:none;padding:13px;border-radius:3px;font-weight:600;font-size:0.9rem;cursor:pointer;">Submit RFQ</button>
      <div id="rfqStatus" style="margin-top:10px;font-size:0.8rem;"></div>
    </form>
  </div>
</div>
<script>
(function(){
  var openBtn=document.getElementById('rfqOpenBtn');
  var modal=document.getElementById('rfqModal');
  var closeBtn=document.getElementById('rfqCloseBtn');
  var form=document.getElementById('rfqForm');
  var status=document.getElementById('rfqStatus');
  var prodField=document.getElementById('rfqProductField');
  var urlField=document.getElementById('rfqUrlField');
  var modelField=document.getElementById('rfqModelField');
  var pageTitleEl=document.querySelector('.pg-title');
  var productName=pageTitleEl?pageTitleEl.textContent.trim():document.title;
  if(openBtn){
    openBtn.addEventListener('click', function(){
      prodField.value=productName;
      urlField.value=location.href;
      if(modelField && !modelField.value) modelField.value=productName;
      modal.style.display='flex';
    });
  }
  if(closeBtn) closeBtn.addEventListener('click', function(){ modal.style.display='none'; });
  if(modal) modal.addEventListener('click', function(e){ if(e.target===modal) modal.style.display='none'; });
  if(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      status.textContent='Sending...';
      status.style.color='var(--text-dim)';
      fetch('https://formspree.io/f/mppznvnq', {
        method:'POST',
        body:new FormData(form),
        headers:{'Accept':'application/json'}
      }).then(function(r){
        if(r.ok){
          status.textContent='Thank you — we will get back to you shortly.';
          status.style.color='#1D6A4C';
          form.reset();
          setTimeout(function(){ modal.style.display='none'; status.textContent=''; }, 2200);
        } else {
          status.textContent='Something went wrong — please WhatsApp or call us instead.';
          status.style.color='#C5432F';
        }
      }).catch(function(){
        status.textContent='Network error — please WhatsApp or call us instead.';
        status.style.color='#C5432F';
      });
    });
  }
  var waFloat=document.querySelector('.wa-float');
  if(waFloat){
    var msg='Hello RKIC, I am interested in: '+productName+'\\nProduct Page: '+location.href;
    waFloat.href='https://wa.me/919824136145?text='+encodeURIComponent(msg);
  }
})();
</script>
'''

def process_product(path, product_id):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    orig = c
    c, _ = insert_banner(c)
    c, _ = insert_service_before(c, '<footer id="contact">')
    if RFQ_OLD in c and 'id="rfqOpenBtn"' not in c:
        c = c.replace(RFQ_OLD, rfq_new(product_id), 1)
    if RFQ_MODAL_MARKER not in c:
        # insert modal right before </body>
        c = c.replace('</body>', RFQ_MODAL_HTML + '</body>', 1)
    if c != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False

def main():
    with open('/tmp/products_list.json') as f:
        products = json.load(f)
    pid_set = {p['id'] for p in products}

    changed = {'banner_service': 0, 'products': 0}

    # index / about
    for rel in ['index.html', 'about.html']:
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            b1, b2 = process_simple(p, '<footer id="contact">')
            if b1 or b2: changed['banner_service'] += 1

    # contact.html — different footer id
    cpath = os.path.join(ROOT, 'contact.html')
    if os.path.exists(cpath):
        b1, b2 = process_simple(cpath, '<footer id="contact-footer"')
        if b1 or b2: changed['banner_service'] += 1

    # categories
    for fn in sorted(os.listdir(os.path.join(ROOT, 'categories'))):
        if not fn.endswith('.html'): continue
        p = os.path.join(ROOT, 'categories', fn)
        with open(p, encoding='utf-8') as f:
            head = f.read(2000)
        if 'class="topbar"' not in open(p, encoding='utf-8').read():
            continue
        b1, b2 = process_simple(p, '<footer id="contact">')
        if b1 or b2: changed['banner_service'] += 1

    # brands
    for fn in sorted(os.listdir(os.path.join(ROOT, 'brands'))):
        if not fn.endswith('.html'): continue
        p = os.path.join(ROOT, 'brands', fn)
        b1, b2 = process_simple(p, '<footer id="contact">')
        if b1 or b2: changed['banner_service'] += 1

    # products
    for fn in sorted(os.listdir(os.path.join(ROOT, 'products'))):
        if not fn.endswith('.html'): continue
        pid = fn[:-5]
        p = os.path.join(ROOT, 'products', fn)
        with open(p, encoding='utf-8') as f:
            content = f.read()
        if 'class="topbar"' not in content:
            continue  # redirect stub, skip
        if pid not in pid_set:
            # e.g. honeywell-elster-rabo-model-range-gas-flow-meter.html orphan page — still apply banner+service, skip RFQ specifics gracefully
            pass
        if process_product(p, pid):
            changed['products'] += 1

    print(json.dumps(changed, indent=2))

if __name__ == '__main__':
    main()
