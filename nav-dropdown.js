// RKIC — shared Products/Brands header dropdown (desktop), built to match the
// dynamic mega-menu on index.html exactly. Loaded by every standalone
// products/*.html, categories/*.html and brands/*.html page (all one folder
// level deep, hence the "../" relative paths below — same depth as
// brand-data.js / related-products-data.js, which this depends on).
// Depends on: RKIC_PRODUCTS (related-products-data.js) and RKIC_BRANDS
// (brand-data.js), both already loaded on these pages before this file.
// If categories / subcategoryMap on index.html (search "const categories ="
// and "const subcategoryMap" there) are ever changed, mirror the change here.
// Added 19 Sep 2026 — replaces the old per-page hardcoded <details> link lists,
// which had drifted out of sync with index.html (missing subcategories, wrong
// column layout, no search box). See products-added-list.md.
(function(){
  if (typeof RKIC_PRODUCTS === 'undefined' || typeof RKIC_BRANDS === 'undefined') return;

  // Root-level pages (about.html, contact.html, index.html) need no "../"
  // prefix; pages one folder deep (products/, categories/, brands/) do.
  var prefix = /\/(products|categories|brands)\//.test(location.pathname) ? '../' : '';

  var categories = [
    "FILTERS","FLAME ARRESTORS","FLAME MONITORING SYSTEMS","FLAME RELAY",
    "FLAME SAFEGUARD","GAS FLOW METERS","GAS TRAIN SYSTEMS","HOSE PIPE FITTINGS","IGNITION CABLE",
    "IGNITION ELECTRODES","IGNITION SPARES","IGNITION SPARK ELECTRODES","IGNITION TRANSFORMERS",
    "MANUAL BALL VALVES","MULTIBLOCKS","PHOTOCELL","PILOT BURNERS","PRESSURE GAUGES",
    "PRESSURE REGULATOR VALVES","PRESSURE SWITCHES","RATIO REGULATORS","SAFETY RELIEF VALVES",
    "SEQUENCE CONTROLLERS","SERVO MOTORS","SLAM SHUT OFF VALVES","SOLENOID VALVES",
    "UV FLAME DETECTORS","UV FLAME SENSOR","VALVE PROVING SYSTEMS"
  ];
  var subcategoryMap = {
    'PRESSURE REGULATOR VALVES': ['High Pressure Regulator', 'Low Pressure Regulator', 'Oxygen Regulator', 'Ammonia Regulator', 'CO2 Regulator', 'LPG Auto Change Over Regulator'],
    'SOLENOID VALVES': ['Brahma Solenoid Valve', 'Kromschröder Solenoid Valve', 'Elektrogas Solenoid Valve', 'Solenoid Coil', 'Coil Connector'],
    'IGNITION TRANSFORMERS': ['Brahma', 'Cofi', 'Danfoss', 'Honeywell Kromschröder', 'Honeywell Technologies'],
    'GAS FLOW METERS': ['Diaphragm Gas Meters', 'Turbine Gas Meter Quantometer', 'RPD Rotary Gas Meter'],
    'SEQUENCE CONTROLLERS': ['Burner Control', 'Burner Control Unit (BCU)']
  };
  // Real standalone pages for each subcategory filter (12 Oct 2026) — replaces
  // the old index.html#/subcategory/... hash-routing link, which was a real
  // crawlable <a href> rendered unconditionally into every products/,
  // categories/ and brands/ page's nav, flagged as a Google-crawling concern.
  // One entry (Kromschröder Solenoid Valve) has zero products / no standalone
  // page yet, so it falls back to the parent category page.
  var subcategoryHrefMap = {
    'GAS FLOW METERS||Diaphragm Gas Meters': 'categories/gas-flow-meters-diaphragm-gas-meters.html',
    'GAS FLOW METERS||Turbine Gas Meter Quantometer': 'categories/gas-flow-meters-turbine-gas-meter-quantometer.html',
    'GAS FLOW METERS||RPD Rotary Gas Meter': 'categories/gas-flow-meters-rpd-rotary-gas-meter.html',
    'IGNITION TRANSFORMERS||Brahma': 'categories/ignition-transformers-brahma.html',
    'IGNITION TRANSFORMERS||Cofi': 'categories/ignition-transformers-cofi.html',
    'IGNITION TRANSFORMERS||Danfoss': 'categories/ignition-transformers-danfoss.html',
    'IGNITION TRANSFORMERS||Honeywell Kromschröder': 'categories/ignition-transformers-honeywell-kromschroder.html',
    'IGNITION TRANSFORMERS||Honeywell Technologies': 'categories/ignition-transformers-honeywell-technologies.html',
    'PRESSURE REGULATOR VALVES||High Pressure Regulator': 'categories/pressure-regulator-valves-high-pressure-regulator.html',
    'PRESSURE REGULATOR VALVES||Low Pressure Regulator': 'categories/pressure-regulator-valves-low-pressure-regulator.html',
    'PRESSURE REGULATOR VALVES||Oxygen Regulator': 'categories/pressure-regulator-valves-oxygen-regulator.html',
    'PRESSURE REGULATOR VALVES||Ammonia Regulator': 'categories/pressure-regulator-valves-ammonia-regulator.html',
    'PRESSURE REGULATOR VALVES||CO2 Regulator': 'categories/pressure-regulator-valves-co2-regulator.html',
    'PRESSURE REGULATOR VALVES||LPG Auto Change Over Regulator': 'categories/pressure-regulator-valves-lpg-auto-change-over-regulator.html',
    'SEQUENCE CONTROLLERS||Burner Control': 'categories/sequence-controllers-burner-control.html',
    'SEQUENCE CONTROLLERS||Burner Control Unit (BCU)': 'categories/sequence-controllers-burner-control-unit-bcu.html',
    'SOLENOID VALVES||Brahma Solenoid Valve': 'categories/solenoid-valves-brahma-solenoid-valve.html',
    'SOLENOID VALVES||Elektrogas Solenoid Valve': 'categories/solenoid-valves-elektrogas-solenoid-valve.html',
    'SOLENOID VALVES||Solenoid Coil': 'categories/solenoid-valves-solenoid-coil.html',
    'SOLENOID VALVES||Coil Connector': 'categories/solenoid-valves-coil-connector.html',
    'SOLENOID VALVES||Kromschröder Solenoid Valve': 'categories/solenoid-valves.html'
  };
  function subcategoryHref(catName, subName){
    var key = catName + '||' + subName;
    var rel = subcategoryHrefMap[key] || ('categories/' + categorySlug(catName) + '.html');
    return prefix + rel;
  }

  // ---- Category icons — matches index.html's nav-mega grid exactly (10 Oct 2026) ----
  var categoryIconKey = {
    'MANUAL BALL VALVES':'valve','MULTIBLOCKS':'valve','SLAM SHUT OFF VALVES':'valve',
    'PRESSURE REGULATOR VALVES':'valve','RATIO REGULATORS':'valve','SOLENOID VALVES':'valve',
    'IGNITION CABLE':'spark','IGNITION ELECTRODES':'spark','IGNITION SPARES':'spark','IGNITION SPARK ELECTRODES':'spark','IGNITION TRANSFORMERS':'spark',
    'PILOT BURNERS':'flame','FLAME ARRESTORS':'flame','FLAME MONITORING SYSTEMS':'flame','FLAME RELAY':'flame','FLAME SAFEGUARD':'flame',
    'UV FLAME DETECTORS':'eye','UV FLAME SENSOR':'eye','PHOTOCELL':'eye',
    'SEQUENCE CONTROLLERS':'gear','SERVO MOTORS':'gear',
    'GAS TRAIN SYSTEMS':'pipe','HOSE PIPE FITTINGS':'pipe',
    'GAS FLOW METERS':'gauge','PRESSURE GAUGES':'gauge','PRESSURE SWITCHES':'gauge',
    'VALVE PROVING SYSTEMS':'shield','SAFETY RELIEF VALVES':'shield',
    'FILTERS':'filter'
  };
  var navIconPaths = {
    valve:'<circle cx="12" cy="12" r="3"/><path d="M4 12h5M15 12h5"/>',
    flame:'<path d="M12 2c2 3-1 4-1 7a3 3 0 1 0 6 0c0-2-1-3-1-5 3 2 4 5 4 8a7 7 0 1 1-14 0c0-4 3-6 6-10z"/>',
    gauge:'<path d="M4 15a8 8 0 1 1 16 0"/><path d="M12 15l3-4"/><circle cx="12" cy="15" r="1"/>',
    pipe:'<rect x="3" y="10" width="18" height="4" rx="1"/><circle cx="6" cy="12" r="1"/><circle cx="18" cy="12" r="1"/>',
    spark:'<path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/>',
    eye:'<path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z"/><circle cx="12" cy="12" r="3"/>',
    shield:'<path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6l8-4z"/>',
    filter:'<path d="M4 4h16l-6 8v6l-4 2v-8z"/>',
    gear:'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>'
  };
  function categoryIconSVG(name){
    var key = categoryIconKey[name] || 'gear';
    return '<svg class="nav-cat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' + navIconPaths[key] + '</svg>';
  }

  // Matches index.html's categorySlugOverrides exactly (search "categorySlugOverrides"
  // there) — a couple of categories have a real page filename that doesn't match the
  // plain slugified name. Mirror any change there here too.
  var categorySlugOverrides = { 'FILTERS': 'filters-strainers', 'PRESSURE GAUGES': 'pressure-gauge-accessories' };
  function categoryCount(name){ return RKIC_PRODUCTS.filter(function(p){ return p.category === name; }).length; }
  function categorySlug(name){ return categorySlugOverrides[name] || name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
  function categoryHref(name){ return categoryCount(name) > 0 ? prefix + 'categories/' + categorySlug(name) + '.html' : 'javascript:void(0)'; }

  // ---- Products grid: category rows + collapsed-by-default subcategory toggles ----
  var navProductsGrid = document.getElementById('navProductsGrid');
  if(navProductsGrid){
    categories.forEach(function(name){
      var subNames = subcategoryMap[name] || [];
      var hasSub = subNames.length > 0;
      if(hasSub){
        var row = document.createElement('div');
        row.className = 'nav-cat-row';
        row.dataset.cat = name;
        var a = document.createElement('a');
        a.href = categoryHref(name);
        a.className = 'nav-drop-link';
        a.innerHTML = categoryIconSVG(name) + '<span>' + name + '</span>';
        var toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'nav-cat-toggle';
        toggle.setAttribute('aria-label', 'Show ' + name + ' subcategories');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = '<span class="nav-cat-caret">⌄</span>';
        var subsRow = document.createElement('div');
        subsRow.className = 'nav-cat-subs';
        subsRow.dataset.parent = name;
        subNames.forEach(function(subName){
          var sa = document.createElement('a');
          sa.href = subcategoryHref(name, subName);
          sa.innerHTML = '<span>↳ ' + subName + '</span>';
          subsRow.appendChild(sa);
        });
        toggle.addEventListener('click', function(e){
          e.stopPropagation(); e.preventDefault();
          var isOpen = row.classList.toggle('expanded');
          toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
          subsRow.style.display = isOpen ? 'flex' : 'none';
        });
        row.appendChild(a);
        row.appendChild(toggle);
        navProductsGrid.appendChild(row);
        navProductsGrid.appendChild(subsRow);
      } else {
        var a2 = document.createElement('a');
        a2.href = categoryHref(name);
        a2.className = 'nav-drop-link';
        a2.innerHTML = categoryIconSVG(name) + '<span>' + name + '</span>';
        navProductsGrid.appendChild(a2);
      }
    });
  }

  // ---- Mobile drawer products list: same category/subcategory data as the desktop
  // grid above, rendered into the hamburger drawer's #drawerProductsSub placeholder
  // (markup: `<div class="drawer-sub" id="drawerProductsSub"></div>` inside the
  // Products <li class="drawer-item">). Replaces the old per-page hardcoded list,
  // which had a stray link to a non-existent "Electronic Pressure Gauge Dmg" category
  // and was missing/stale on the subcategory expand options. Added 12 Oct 2026. ----
  var drawerProductsSub = document.getElementById('drawerProductsSub');
  if(drawerProductsSub){
    categories.forEach(function(name){
      var subNames = subcategoryMap[name] || [];
      if(subNames.length){
        var item = document.createElement('div');
        item.className = 'drawer-cat-item';
        var row = document.createElement('div');
        row.className = 'drawer-cat-row';
        var a = document.createElement('a');
        a.href = categoryHref(name);
        a.textContent = name;
        var toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'drawer-cat-toggle';
        toggle.setAttribute('aria-label', 'Show sub-categories');
        toggle.innerHTML = '<span class="chev">⌄</span>';
        toggle.addEventListener('click', function(){ item.classList.toggle('open'); });
        row.appendChild(a);
        row.appendChild(toggle);
        var subList = document.createElement('div');
        subList.className = 'drawer-subcat-list';
        subNames.forEach(function(subName){
          var sa = document.createElement('a');
          sa.href = subcategoryHref(name, subName);
          sa.className = 'drawer-sub-sublink';
          sa.textContent = '↳ ' + subName;
          subList.appendChild(sa);
        });
        item.appendChild(row);
        item.appendChild(subList);
        drawerProductsSub.appendChild(item);
      } else {
        var a2 = document.createElement('a');
        a2.href = categoryHref(name);
        a2.textContent = name;
        drawerProductsSub.appendChild(a2);
      }
    });
  }

  // ---- Live search (products + categories), same matching rule as index.html ----
  var navProductsFilter = document.getElementById('navProductsFilter');
  var navProductsResults = document.getElementById('navProductsResults');
  var brandLogoOf = {};
  RKIC_BRANDS.forEach(function(b){ brandLogoOf[b.name] = b.logo; });

  function renderNavProductResults(rawQuery){
    var q = rawQuery.trim().toLowerCase();
    navProductsResults.innerHTML = '';
    var prodMatches = RKIC_PRODUCTS.filter(function(p){
      return (p.name + ' ' + p.brand + ' ' + p.category + ' ' + (p.subcategory || '') + ' ' + p.code).toLowerCase().indexOf(q) !== -1;
    }).slice(0, 50);
    var catMatches = categories.filter(function(c){ return c.toLowerCase().indexOf(q) !== -1; }).slice(0, 15);
    if(prodMatches.length === 0 && catMatches.length === 0){
      var div = document.createElement('div');
      div.className = 'search-empty nav-drop-hint';
      div.textContent = '"' + rawQuery + '" se koi match nahi mila.';
      navProductsResults.appendChild(div);
      return;
    }
    if(prodMatches.length){
      var kicker = document.createElement('div');
      kicker.className = 'search-kicker';
      kicker.textContent = 'Products';
      navProductsResults.appendChild(kicker);
      prodMatches.forEach(function(p){
        var a = document.createElement('a');
        a.href = prefix + 'products/' + p.id + '.html';
        a.className = 'search-product-row';
        var brandHTML = brandLogoOf[p.brand] ? '<img class="srp-brand-logo" src="' + brandLogoOf[p.brand] + '" alt="' + p.brand + '">' : (p.brand + ' · ');
        a.innerHTML = '<img src="' + p.thumb + '" alt="' + p.name + '"><span class="srp-info"><span class="srp-name">' + p.name + '</span><span class="srp-meta">' + brandHTML + p.category + '</span></span><span class="code">' + p.code + '</span>';
        navProductsResults.appendChild(a);
      });
    }
    if(catMatches.length){
      var kicker2 = document.createElement('div');
      kicker2.className = 'search-kicker';
      kicker2.textContent = 'Categories';
      navProductsResults.appendChild(kicker2);
      catMatches.forEach(function(name){
        var a = document.createElement('a');
        a.href = categoryHref(name);
        a.innerHTML = '<span>' + name + '</span>';
        navProductsResults.appendChild(a);
      });
    }
  }
  if(navProductsFilter && navProductsResults && navProductsGrid){
    navProductsFilter.addEventListener('input', function(e){
      var q = e.target.value.trim();
      if(!q){
        navProductsGrid.hidden = false;
        navProductsResults.hidden = true;
      } else {
        navProductsGrid.hidden = true;
        navProductsResults.hidden = false;
        renderNavProductResults(q);
      }
    });
    navProductsFilter.addEventListener('click', function(e){ e.stopPropagation(); });
    var navProductsEl = document.getElementById('navProducts');
    if(navProductsEl){
      navProductsEl.querySelector('.nav-drop-btn').addEventListener('click', function(){
        navProductsFilter.value = '';
        navProductsGrid.hidden = false;
        navProductsResults.hidden = true;
        navProductsGrid.querySelectorAll('.nav-cat-row.expanded').forEach(function(row){
          row.classList.remove('expanded');
          var btn = row.querySelector('.nav-cat-toggle');
          if(btn) btn.setAttribute('aria-expanded', 'false');
        });
        navProductsGrid.querySelectorAll('.nav-cat-subs').forEach(function(s){ s.style.display = 'none'; });
      });
    }
  }

  // ---- Brands grid: 6-column, logo stacked above name — matches #navBrandsPanel on index.html ----
  var navBrandsPanel = document.getElementById('navBrandsPanel');
  if(navBrandsPanel){
    RKIC_BRANDS.forEach(function(b){
      var a = document.createElement('a');
      a.href = prefix + 'brands/' + b.slug + '.html';
      a.className = 'nav-drop-link';
      a.innerHTML = (b.logo ? '<img src="' + b.logo + '" alt="' + b.name + '" class="nav-drop-brand-logo" loading="lazy">' : '') + '<span class="nav-drop-brand-name">' + b.name + '</span>';
      navBrandsPanel.appendChild(a);
    });
  }

  // ---- Desktop dropdown open/close: mutual exclusion + outside click — matches index.html exactly ----
  ['navProducts', 'navBrands'].forEach(function(id){
    var el = document.getElementById(id);
    if(!el) return;
    var btn = el.querySelector('.nav-drop-btn');
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      var isOpen = el.classList.contains('open');
      document.querySelectorAll('.nav-dropdown.open').forEach(function(d){ d.classList.remove('open'); });
      if(!isOpen) el.classList.add('open');
    });
  });
  document.addEventListener('click', function(){
    document.querySelectorAll('.nav-dropdown.open').forEach(function(d){ d.classList.remove('open'); });
  });

  // ---- Mega-menu close (✕) button — matches index.html exactly (10 Oct 2026) ----
  document.querySelectorAll('.nav-mega-close').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.stopPropagation();
      var dropdown = btn.closest('.nav-dropdown');
      if(dropdown) dropdown.classList.remove('open');
    });
  });
})();
