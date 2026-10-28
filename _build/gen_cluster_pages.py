#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates industrial-cluster / city-targeted SEO landing pages, reusing the
site's standard header/footer (incl. pan-india banner, pan-india-service
section, RFQ modal, WhatsApp float) lifted from an already-patched product
page template.
"""
import os, re, html, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, 'products', 'beru-ck4-spark-plug-connector-ignition-spare.html')
OUT_DIR = os.path.join(ROOT, 'industrial-supply')
os.makedirs(OUT_DIR, exist_ok=True)

with open(TEMPLATE, encoding='utf-8') as f:
    src = f.read()

HEAD_META_OLD = src[src.index('<title>BERU'):src.index('</script>\n<link rel="preconnect"')]
# HEAD_META_OLD spans from <title> through the two JSON-LD scripts (ends right before the closing </script> + newline + preconnect link)
HEAD_META_OLD = HEAD_META_OLD + '</script>'

BODY_START_MARK = '<div class="wrap">\n  <div class="breadcrumb">'
TAIL_START_MARK = '<!-- OUR CLIENTS -->'

head_idx = src.index(BODY_START_MARK)
tail_idx = src.index(TAIL_START_MARK)

HEAD_CHUNK = src[:head_idx]
TAIL_CHUNK = src[tail_idx:]

# Strip product-specific wiring from the reused tail chunk.
# Keep related-products-data.js (defines window.RKIC_PRODUCTS, which the
# shared nav-dropdown.js mega-menu/search needs on every page) but drop
# CURRENT_PRODUCT_ID and related-products.js (the "You May Also Need" grid
# populator — a no-op without CURRENT_PRODUCT_ID, and there's no #relatedGrid
# on cluster pages anyway).
TAIL_CHUNK = re.sub(r'<script>var CURRENT_PRODUCT_ID = "[^"]*";</script>\n', '', TAIL_CHUNK)
TAIL_CHUNK = re.sub(r'<script src="\.\./related-products\.js[^"]*"[^>]*></script>\n', '', TAIL_CHUNK)
# mobile-quote-bar already points to #contact — fine to keep.

assert '{{HEAD_META}}' not in HEAD_CHUNK

def make_head(title, desc, keywords, canonical_slug):
    # NOTE: title/desc/keywords/og_title arrive ALREADY HTML-entity-encoded
    # (written that way in the PAGES dict below), so they are inserted as-is
    # into HTML text/attribute contexts — do NOT html.escape() them again
    # here, that would double-encode ("&amp;" -> "&amp;amp;"). For JSON-LD
    # (not an HTML context), we html.unescape() first so the JSON string
    # holds a real "&" rather than the literal text "&amp;".
    url = 'https://www.rkic.in/industrial-supply/' + canonical_slug
    og_title = title.split(' | ')[0]
    area = og_title.replace('Industrial Gas &amp; Burner Spares Supplier for ', '')
    json_org = html.unescape('R.K. Instruments &amp; Controls')
    json_service = html.unescape('Industrial Gas &amp; Burner Spares Supply')
    json_og_title = html.unescape(og_title)
    json_area = html.unescape(area)
    block = f'''<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://www.rkic.in/images/logo-header.webp">
<meta property="og:site_name" content="R.K. Instruments &amp; Controls">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{desc}">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Service","serviceType":"{json_service}","provider":{{"@type":"Organization","name":"{json_org}","url":"https://www.rkic.in/"}},"areaServed":"{json_area}","url":"{url}"}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.rkic.in/"}}, {{"@type": "ListItem", "position": 2, "name": "Industrial Supply", "item": "https://www.rkic.in/industrial-supply/"}}, {{"@type": "ListItem", "position": 3, "name": "{json_og_title}", "item": "{url}"}}]}}</script>'''
    return block

def card(title, text):
    return f'''      <div style="border:1px solid var(--line);border-radius:4px;padding:20px;background:#fff;">
        <div style="font-weight:700;font-size:0.92rem;margin-bottom:8px;">{title}</div>
        <div style="font-size:0.86rem;color:var(--text-dim);line-height:1.7;">{text}</div>
      </div>
'''

def cat_chip(name, slug):
    return f'<a href="../categories/{slug}" style="display:inline-block;border:1px solid var(--line);border-radius:20px;padding:8px 16px;margin:0 8px 8px 0;font-size:0.82rem;color:var(--ink);text-decoration:none;background:#fff;">{name}</a>'

def make_body(h1, intro, industries_html, categories, brands_line, page_name):
    cat_chips = ''.join(cat_chip(n, s) for n, s in categories)
    return f'''<div class="wrap">
  <div class="breadcrumb">
    <a href="../">Home</a><span class="sep">/</span><a href="../industrial-supply/">Industrial Supply</a><span class="sep">/</span>{h1}
  </div>
  <div style="padding:22px 0 10px;">
    <h1 style="font-size:clamp(1.6rem,3.6vw,2.3rem);font-weight:600;line-height:1.2;max-width:28ch;">{h1}</h1>
    <p style="font-size:0.98rem;color:var(--text-dim);line-height:1.7;max-width:70ch;margin-top:14px;">{intro}</p>
    <div style="margin-top:20px;display:flex;gap:12px;flex-wrap:wrap;">
      <a class="pg-btn pg-btn-primary" href="https://wa.me/919824136145?text={urllib.parse.quote('Hello RKIC, I need industrial gas/burner spares for ' + html.unescape(page_name) + '.')}" target="_blank" rel="noopener">Enquire on WhatsApp</a>
      <button type="button" class="pg-btn pg-btn-secondary" id="rfqOpenBtn" style="cursor:pointer;">Get a Quote (RFQ)</button>
      <a class="pg-btn pg-btn-secondary" href="../contact">Contact Us</a>
    </div>
  </div>

  <section style="padding:30px 0 10px;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--flame);">Industries We Serve Here</div>
    <h2 style="font-size:clamp(1.2rem,2.4vw,1.5rem);font-weight:600;margin:6px 0 20px;max-width:40ch;">What local plants run on our components.</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;">
{industries_html}    </div>
  </section>

  <section style="padding:30px 0 10px;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--flame);">Product Categories Shipped Here</div>
    <h2 style="font-size:clamp(1.2rem,2.4vw,1.5rem);font-weight:600;margin:6px 0 18px;">Browse by category.</h2>
    <div>{cat_chips}</div>
  </section>

  <section style="padding:30px 0 10px;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--flame);">Brands We Supply</div>
    <p style="font-size:0.9rem;color:var(--text-dim);margin-top:10px;max-width:70ch;line-height:1.7;">{brands_line}</p>
  </section>
</div>
'''

PAGES = [
    dict(
        slug='morbi-ceramic-zone',
        h1='Industrial Gas &amp; Burner Spares Supplier for Morbi Ceramic Zone',
        og_title='Industrial Gas &amp; Burner Spares Supplier for Morbi Ceramic Zone',
        desc='Authorized Supplier Pan India — RKIC supplies gas train spares, burner components &amp; flame safety equipment for Morbi\'s ceramic tile, sanitaryware &amp; roller kiln industry. Ready stock, fast dispatch.',
        keywords='Morbi ceramic industry gas equipment, burner spares Morbi, gas train supplier Gujarat, Industrial Gas Train Spares Supplier India, kiln burner components Morbi, Authorized Supplier Pan India',
        intro='Morbi\'s ceramic tile, sanitaryware and roller-kiln plants run on continuous, high-temperature combustion — and that means gas trains, solenoid valves and flame-safety components that can\'t fail. R.K. Instruments &amp; Controls (RKIC) stocks genuine Brahma, Dungs, Madas, Honeywell Kromschr&ouml;der and Siemens components ready for same-day dispatch to Morbi &amp; the wider Saurashtra ceramic belt, with full GST-compliant B2B invoicing and E-Way Bill support.',
        industries=[('Ceramic Tile &amp; Sanitaryware Kilns', 'Gas trains, ratio regulators and burner ignition components sized for roller-kiln and tunnel-kiln combustion lines.'),
                    ('Spray Dryers &amp; Body Preparation', 'Solenoid valves, pressure switches and flame monitoring for spray-dryer and body-prep furnace burners.'),
                    ('Glazing &amp; Frit Furnaces', 'High-temperature ignition transformers, electrodes and UV flame sensors for frit and glaze-line furnaces.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Solenoid Valves', 'solenoid-valves'), ('Pressure Regulator Valves', 'pressure-regulator-valves'), ('Ignition Transformers', 'ignition-transformers'), ('UV Flame Detectors', 'uv-flame-detectors'), ('Sequence Controllers', 'sequence-controllers')],
        brands='Brahma, Dungs, Madas, Honeywell Kromschr&ouml;der, Siemens, Elektrogas, Vanaz and our own Siltek &amp; R.K. Instruments &amp; Controls in-house range — all genuine, all ex-stock for Morbi dispatch.',
    ),
    dict(
        slug='pune-auto-hub',
        h1='Burner &amp; Gas Train Components Supplier for Pune Auto Industry',
        og_title='Burner &amp; Gas Train Components Supplier for Pune Auto Industry',
        desc='Authorized Supplier Pan India — RKIC supplies gas train spares, burner ignition &amp; flame safety equipment for Pune\'s automotive, forging &amp; foundry industry. Ready stock, surface &amp; air cargo dispatch.',
        keywords='Pune auto industry burner spares, gas train supplier Pune, forging furnace components Pune, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India, Pimpri Chinchwad industrial gas equipment',
        intro='Pune\'s automotive, forging and foundry corridor &mdash; from Pimpri-Chinchwad to Chakan and Talegaon &mdash; depends on reliable heat-treatment, forging-furnace and paint-shop combustion systems. RKIC dispatches genuine Brahma, Dungs, Honeywell Maxon, Siemens and Vanaz gas-train and flame-safety components to Pune manufacturers with same-day/24-hr surface and air cargo, plus 100% GST-compliant B2B billing across Maharashtra.',
        industries=[('Forging &amp; Heat-Treatment Furnaces', 'Gas trains, ratio regulators and high-temperature ignition components for forging and heat-treat furnace lines.'),
                    ('Automotive Paint-Shop Ovens', 'Solenoid valves, sequence controllers and flame safeguard systems for curing and paint-bake ovens.'),
                    ('Foundry &amp; Casting Operations', 'Pilot burners, UV flame sensors and pressure switches for induction and reverberatory furnace auxiliaries.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Sequence Controllers', 'sequence-controllers'), ('Pilot Burners', 'pilot-burners'), ('Flame Safeguard', 'flame-safeguard'), ('Servo Motors', 'servo-motors'), ('Multiblocks', 'multiblocks')],
        brands='Brahma, Dungs, Honeywell Maxon, Honeywell Eclipse, Siemens, Vanaz, Cofi and Elektrogas &mdash; genuine parts, ex-stock for dispatch across Pune, Chakan, Talegaon and Pimpri-Chinchwad.',
    ),
    dict(
        slug='ahmedabad-vapi-chemical-belt',
        h1='Gas Train &amp; Flame Safety Equipment Supplier for Ahmedabad&ndash;Vapi Chemical Belt',
        og_title='Gas Train &amp; Flame Safety Equipment Supplier for Ahmedabad&ndash;Vapi Chemical Belt',
        desc='Authorized Supplier Pan India — RKIC supplies gas trains, safety relief valves &amp; flame monitoring equipment for the Ahmedabad-Vapi-Vadodara chemical &amp; pharma belt. GST-compliant B2B billing, E-Way Bill support.',
        keywords='Ahmedabad chemical industry gas equipment, Vapi industrial gas supplier, gas train supplier Gujarat, safety relief valve supplier Gujarat, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India',
        intro='The Ahmedabad&ndash;Vadodara&ndash;Vapi chemical and pharma corridor runs some of India\'s most demanding process-heating and utility-boiler installations. RKIC supplies genuine Dungs, Madas, Honeywell Kromschr&ouml;der, Danfoss and Vanaz gas-train, safety relief valve and flame-monitoring equipment to this belt with ready stock, fast surface/air cargo dispatch and 100% GST-compliant B2B invoicing with E-Way Bill support across Gujarat.',
        industries=[('Chemical &amp; Pharma Process Heating', 'Gas trains, ratio regulators and pressure regulator valves for reactor and process-heater burner systems.'),
                    ('Utility &amp; EPC Boiler Plants', 'Safety relief valves, slam shut-off valves and valve proving systems for boiler-house safety compliance.'),
                    ('Specialty Chemical Furnaces', 'Flame monitoring systems, UV flame detectors and ignition electrodes for high-reliability furnace lines.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Safety Relief Valves', 'safety-relief-valves'), ('Slam Shut Off Valves', 'slam-shut-off-valves'), ('Valve Proving Systems', 'valve-proving-systems'), ('Flame Monitoring Systems', 'flame-monitoring-systems'), ('Pressure Regulator Valves', 'pressure-regulator-valves')],
        brands='Dungs, Madas, Honeywell Kromschr&ouml;der, Danfoss, Vanaz, Elektrogas and Siemens &mdash; genuine, ex-stock components dispatched across Ahmedabad, Vadodara and Vapi.',
    ),
    dict(
        slug='faridabad-ncr',
        h1='Industrial Combustion Spares Supplier for Faridabad &amp; NCR',
        og_title='Industrial Combustion Spares Supplier for Faridabad &amp; NCR',
        desc='Authorized Supplier Pan India — RKIC supplies burner, gas train &amp; ignition spares for Faridabad, Gurugram &amp; wider NCR industrial manufacturing. Ready stock, same-day/24-hr dispatch, GST-compliant billing.',
        keywords='Faridabad industrial gas equipment, NCR burner spares supplier, gas train supplier Delhi NCR, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India, Gurugram manufacturing gas equipment',
        intro='Faridabad\'s engineering and auto-ancillary manufacturing base, along with the wider NCR industrial belt, depends on dependable burner and gas-train components for heat-treatment, forging and process-heating lines. RKIC ships genuine Brahma, Dungs, Siemens, Honeywell and Cofi components to NCR manufacturers with same-day/24-hr surface and air cargo dispatch, and 100% GST-compliant B2B invoicing with E-Way Bill support for Delhi, Haryana &amp; UP.',
        industries=[('Heat-Treatment &amp; Forging', 'Gas trains, ignition transformers and ratio regulators for heat-treatment and forging furnace lines.'),
                    ('Auto-Ancillary Manufacturing', 'Solenoid valves, sequence controllers and pilot burners for component curing and process-heating ovens.'),
                    ('General Engineering &amp; Boiler Houses', 'Pressure gauges, safety relief valves and flame safeguard systems for industrial boiler plants.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Ignition Transformers', 'ignition-transformers'), ('Sequence Controllers', 'sequence-controllers'), ('Pressure Gauges', 'pressure-gauge-accessories'), ('Solenoid Valves', 'solenoid-valves'), ('Flame Relay', 'flame-relay')],
        brands='Brahma, Dungs, Siemens, Honeywell, Honeywell Kromschr&ouml;der, Cofi and Vanaz &mdash; genuine components, ex-stock for dispatch across Faridabad, Gurugram, Delhi and the wider NCR.',
    ),
    dict(
        slug='mumbai-pune-industrial-belt',
        h1='Burner &amp; Gas Train Spares Supplier for Mumbai&ndash;Pune Industrial Belt',
        og_title='Burner &amp; Gas Train Spares Supplier for Mumbai&ndash;Pune Industrial Belt',
        desc='Authorized Supplier Pan India — RKIC supplies gas trains, burner ignition &amp; flame safety components for the Mumbai-Pune engineering, automotive &amp; petrochemical corridor. Ready stock, fast dispatch.',
        keywords='Mumbai industrial gas equipment, Pune burner spares supplier, gas train supplier Maharashtra, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India, petrochemical burner components Mumbai',
        intro='The Mumbai&ndash;Pune industrial belt is Maharashtra\'s core manufacturing corridor &mdash; engineering goods, automotive assembly, petrochemicals and process industries clustered from Taloja and Thane through to Chakan and Pimpri-Chinchwad. RKIC supplies genuine Brahma, Dungs, Honeywell, Siemens and Vanaz gas-train, burner ignition and flame-safety components to this belt with ready stock, surface &amp; air cargo dispatch and 100% GST-compliant B2B invoicing across Maharashtra.',
        industries=[('Petrochemical &amp; Process Heating', 'Gas trains, pressure regulator valves and safety relief valves for process heaters and reactor furnaces.'),
                    ('Automotive &amp; Engineering Manufacturing', 'Solenoid valves, sequence controllers and ignition transformers for paint-bake ovens and heat-treatment lines.'),
                    ('Industrial Boiler Houses', 'Pressure switches, valve proving systems and flame safeguard systems for utility boiler plants across the corridor.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Solenoid Valves', 'solenoid-valves'), ('Safety Relief Valves', 'safety-relief-valves'), ('Sequence Controllers', 'sequence-controllers'), ('Pressure Switches', 'pressure-switches'), ('Valve Proving Systems', 'valve-proving-systems')],
        brands='Brahma, Dungs, Honeywell, Honeywell Kromschr&ouml;der, Siemens, Vanaz and Elektrogas &mdash; genuine, ex-stock components dispatched across Mumbai, Thane, Pune and the wider Maharashtra industrial belt.',
    ),
    dict(
        slug='bengaluru-chennai-corridor',
        h1='Gas Train &amp; Burner Components Supplier for Bengaluru&ndash;Chennai Corridor',
        og_title='Gas Train &amp; Burner Components Supplier for Bengaluru&ndash;Chennai Corridor',
        desc='Authorized Supplier Pan India — RKIC supplies gas trains, burner ignition &amp; flame monitoring equipment for Bengaluru &amp; Chennai\'s automotive, electronics &amp; general engineering industries. Ready stock, pan-India dispatch.',
        keywords='Bengaluru industrial gas equipment, Chennai burner spares supplier, gas train supplier Karnataka Tamil Nadu, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India, Tier-1 automotive gas components',
        intro='Bengaluru and Chennai anchor South India\'s automotive Tier-1, electronics and general engineering manufacturing base. RKIC dispatches genuine Brahma, Dungs, Siemens, Honeywell and Cofi gas-train, burner ignition and flame-monitoring components to this corridor with ready stock, surface &amp; air cargo dispatch and GST-compliant B2B billing across Karnataka &amp; Tamil Nadu.',
        industries=[('Automotive Tier-1 Manufacturing', 'Sequence controllers, solenoid valves and pilot burners for paint-shop and heat-treatment furnace lines.'),
                    ('General &amp; Precision Engineering', 'Gas trains, ratio regulators and ignition transformers for process-heating and annealing furnaces.'),
                    ('Industrial Boiler &amp; Utility Plants', 'Pressure switches, safety relief valves and flame safeguard systems for boiler-house compliance.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Sequence Controllers', 'sequence-controllers'), ('Pilot Burners', 'pilot-burners'), ('Ignition Transformers', 'ignition-transformers'), ('Pressure Switches', 'pressure-switches'), ('Safety Relief Valves', 'safety-relief-valves')],
        brands='Brahma, Dungs, Siemens, Honeywell, Honeywell Maxon, Cofi and Vanaz &mdash; genuine, ex-stock components dispatched across Bengaluru, Chennai and the wider Karnataka-Tamil Nadu industrial belt.',
    ),
    dict(
        slug='kolkata-hugli-belt',
        h1='Burner &amp; Boiler Spares Supplier for Kolkata&ndash;Hugli Industrial Belt',
        og_title='Burner &amp; Boiler Spares Supplier for Kolkata&ndash;Hugli Industrial Belt',
        desc='Authorized Supplier Pan India — RKIC supplies gas trains, burner ignition &amp; flame safety components for Kolkata &amp; the Hugli belt\'s jute, paper &amp; heavy engineering industries. Ready stock, pan-India dispatch.',
        keywords='Kolkata industrial gas equipment, Howrah burner spares supplier, gas train supplier West Bengal, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India, jute mill boiler components',
        intro='The Kolkata&ndash;Howrah Hugli belt is home to West Bengal\'s jute, paper and heavy-engineering industry, much of it running on coal- and gas-fired boiler and process-heating systems. RKIC supplies genuine Dungs, Madas, Honeywell Kromschr&ouml;der, Siemens and Vanaz gas-train, burner ignition and flame-safety components to this belt with ready stock, pan-India dispatch and 100% GST-compliant B2B invoicing with E-Way Bill support.',
        industries=[('Jute &amp; Paper Mill Boilers', 'Gas trains, pressure switches and valve proving systems for mill boiler-house safety compliance.'),
                    ('Heavy Engineering &amp; Foundries', 'Ignition transformers, UV flame detectors and pilot burners for furnace and foundry combustion lines.'),
                    ('Process Heating &amp; Utility Plants', 'Safety relief valves, ratio regulators and flame monitoring systems for industrial process heaters.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Pressure Switches', 'pressure-switches'), ('Valve Proving Systems', 'valve-proving-systems'), ('Ignition Transformers', 'ignition-transformers'), ('Safety Relief Valves', 'safety-relief-valves'), ('Flame Monitoring Systems', 'flame-monitoring-systems')],
        brands='Dungs, Madas, Honeywell Kromschr&ouml;der, Siemens, Vanaz and Brahma &mdash; genuine, ex-stock components dispatched across Kolkata, Howrah and the wider Hugli industrial belt.',
    ),
    dict(
        slug='chota-nagpur-steel-belt',
        h1='Industrial Furnace &amp; Gas Train Spares Supplier for Chota Nagpur Steel Belt',
        og_title='Industrial Furnace &amp; Gas Train Spares Supplier for Chota Nagpur Steel Belt',
        desc='Authorized Supplier Pan India — RKIC supplies high-temperature burner, gas train &amp; flame safety components for the Chota Nagpur steel &amp; heavy engineering belt (Jharkhand, Odisha, West Bengal). Ready stock, fast dispatch.',
        keywords='Chota Nagpur industrial gas equipment, Jharkhand steel plant burner spares, Odisha furnace components supplier, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India, steel plant gas train supplier',
        intro='The Chota Nagpur belt across Jharkhand, Odisha and West Bengal runs India\'s heaviest iron, steel and mineral-processing furnaces. RKIC supplies genuine Honeywell Kromschr&ouml;der, Dungs, Siemens, Madas and Brahma high-temperature gas-train, ignition and flame-safety components to this belt with ready stock, pan-India dispatch and 100% GST-compliant B2B invoicing across Jharkhand, Odisha &amp; West Bengal.',
        industries=[('Iron &amp; Steel Reheating Furnaces', 'High-temperature gas trains, ratio regulators and ignition transformers for reheat and annealing furnace lines.'),
                    ('Mineral Processing &amp; Sintering Plants', 'Pilot burners, UV flame detectors and flame safeguard systems for sinter and pellet-plant combustion.'),
                    ('Heavy Engineering &amp; Foundries', 'Solenoid valves, pressure switches and valve proving systems for foundry and forging furnace auxiliaries.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Ratio Regulators', 'ratio-regulators'), ('Ignition Transformers', 'ignition-transformers'), ('Pilot Burners', 'pilot-burners'), ('UV Flame Detectors', 'uv-flame-detectors'), ('Flame Safeguard', 'flame-safeguard')],
        brands='Honeywell Kromschr&ouml;der, Dungs, Siemens, Madas, Brahma and Vanaz &mdash; genuine, ex-stock components dispatched across Jamshedpur, Rourkela, Bokaro and the wider Chota Nagpur steel belt.',
    ),
    dict(
        slug='visakhapatnam-guntur-belt',
        h1='Gas Train &amp; Boiler Spares Supplier for Visakhapatnam&ndash;Guntur Belt',
        og_title='Gas Train &amp; Boiler Spares Supplier for Visakhapatnam&ndash;Guntur Belt',
        desc='Authorized Supplier Pan India — RKIC supplies gas trains, pressure regulators &amp; flame safety equipment for Andhra Pradesh\'s Visakhapatnam-Guntur fertilizer, cement &amp; petroleum belt. Ready stock, fast dispatch.',
        keywords='Visakhapatnam industrial gas equipment, Guntur burner spares supplier, Andhra Pradesh gas train supplier, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India, fertilizer plant boiler components',
        intro='The Visakhapatnam&ndash;Guntur belt anchors Andhra Pradesh\'s fertilizer, cement, sugar and petroleum-processing industry. RKIC supplies genuine Dungs, Madas, Honeywell Kromschr&ouml;der, Vanaz and Siemens gas-train, pressure regulation and flame-safety components to this belt with ready stock, pan-India dispatch and 100% GST-compliant B2B invoicing across Andhra Pradesh.',
        industries=[('Fertilizer &amp; Petroleum Processing', 'Gas trains, pressure regulator valves and safety relief valves for process-heater and reactor furnace systems.'),
                    ('Cement &amp; Sugar Mill Boilers', 'Pressure switches, valve proving systems and flame monitoring systems for boiler-house safety compliance.'),
                    ('Port-Linked Process Industries', 'Ignition transformers, UV flame detectors and pilot burners for continuous-process combustion lines.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Pressure Regulator Valves', 'pressure-regulator-valves'), ('Safety Relief Valves', 'safety-relief-valves'), ('Pressure Switches', 'pressure-switches'), ('Valve Proving Systems', 'valve-proving-systems'), ('Flame Monitoring Systems', 'flame-monitoring-systems')],
        brands='Dungs, Madas, Honeywell Kromschr&ouml;der, Vanaz, Siemens and Brahma &mdash; genuine, ex-stock components dispatched across Visakhapatnam, Guntur and the wider Andhra Pradesh industrial belt.',
    ),
    dict(
        slug='kollam-thiruvananthapuram-belt',
        h1='Industrial Gas Equipment Supplier for Kollam&ndash;Thiruvananthapuram Belt',
        og_title='Industrial Gas Equipment Supplier for Kollam&ndash;Thiruvananthapuram Belt',
        desc='Authorized Supplier Pan India — RKIC supplies gas trains, burner ignition &amp; flame safety components for Kerala\'s Kollam-Thiruvananthapuram agro-processing, rubber &amp; chemical industry. Ready stock, fast dispatch.',
        keywords='Kerala industrial gas equipment, Kollam burner spares supplier, Thiruvananthapuram gas train supplier, Industrial Gas Train Spares Supplier India, Authorized Supplier Pan India, rubber processing boiler components',
        intro='Kerala\'s Kollam&ndash;Thiruvananthapuram belt supports a mix of agro-processing, coir, rubber and chemical manufacturing, much of it reliant on steady steam and process-heating capacity. RKIC supplies genuine Dungs, Brahma, Siemens and Vanaz gas-train, burner ignition and flame-safety components to this belt with ready stock, pan-India dispatch and 100% GST-compliant B2B invoicing across Kerala.',
        industries=[('Agro-Processing &amp; Rubber Plants', 'Gas trains, solenoid valves and pressure regulator valves for drying and process-heating systems.'),
                    ('Chemical &amp; Specialty Processing', 'Safety relief valves, flame monitoring systems and ignition transformers for reactor and furnace lines.'),
                    ('Industrial Boiler Houses', 'Pressure switches, valve proving systems and flame safeguard systems for boiler-house compliance.')],
        categories=[('Gas Train Systems', 'gas-train-systems'), ('Solenoid Valves', 'solenoid-valves'), ('Pressure Regulator Valves', 'pressure-regulator-valves'), ('Safety Relief Valves', 'safety-relief-valves'), ('Pressure Switches', 'pressure-switches'), ('Flame Safeguard', 'flame-safeguard')],
        brands='Dungs, Brahma, Siemens, Vanaz, Madas and Honeywell &mdash; genuine, ex-stock components dispatched across Kollam, Thiruvananthapuram and the wider Kerala industrial belt.',
    ),
]

def industries_html(items):
    return ''.join(card(t, d) for t, d in items)

for p in PAGES:
    head_meta_new = make_head(p['og_title'] + ' | RKIC', p['desc'], p['keywords'], p['slug'])
    page_head = HEAD_CHUNK.replace(HEAD_META_OLD, head_meta_new)
    body = make_body(p['h1'], p['intro'], industries_html(p['industries']), p['categories'], p['brands'], p['og_title'])
    full = page_head + body + TAIL_CHUNK
    out_path = os.path.join(OUT_DIR, p['slug'] + '.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full)
    print('wrote', out_path)
