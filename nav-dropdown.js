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

  var categories = [
    "BOILER CONNECTOR PLUG","BOILERS","BURNER CONNECTOR PLUG","BURNERS","BUTTERFLY VALVES",
    "ELECTRONIC PRESSURE GAUGE DMG","FILTERS | STRAINERS","FLAME ARRESTORS","FLAME MONITORING SYSTEMS",
    "FLAME SAFEGUARD","GAS FLOW METERS","GAS TRAIN SYSTEMS","HOSE PIPE FITTINGS","IGNITION CABLE",
    "IGNITION ELECTRODES","IGNITION SPARES","IGNITION TRANSFORMERS","LPG AUTOMATIC CHANGEOVER DEVICE",
    "MANUAL BALL VALVES","MULTIBLOCKS","NON RETURN VALVES","PILOT BURNERS","PRESSURE GAUGE ACCESSORIES",
    "PRESSURE REGULATOR VALVES","PRESSURE SWITCHES","RATIO REGULATORS","SAFETY RELIEF VALVES","SENSORS",
    "SEQUENCE CONTROLLERS","SERVO MOTORS","SLAM SHUT OFF VALVES","SOLENOID VALVES","SPARK ELECTRODES",
    "VALVE PROVING SYSTEMS"
  ];
  var subcategoryMap = {
    'PRESSURE REGULATOR VALVES': ['High Pressure Regulator', 'Low Pressure Regulator', 'Oxygen Regulator', 'Ammonia Regulator'],
    'SENSORS': ['Flame Relay', 'UV Flame Sensor', 'Photocell'],
    'SOLENOID VALVES': ['Brahma Solenoid Valve', 'Kromschröder Solenoid Valve', 'Elektrogas Solenoid Valve', 'Solenoid Coil', 'Coil Connector'],
    'IGNITION TRANSFORMERS': ['Ignition Transformer', 'Modutrol Transformer'],
    'GAS FLOW METERS': ['Diaphragm Gas Meters', 'Turbine Gas Meter Quantometer', 'RPD Rotary Gas Meter'],
    'SEQUENCE CONTROLLERS': ['Burner Control', 'Burner Control Unit (BCU)']
  };

  function categoryCount(name){ return RKIC_PRODUCTS.filter(function(p){ return p.category === name; }).length; }
  function categorySlug(name){ return name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
  function categoryHref(name){ return categoryCount(name) > 0 ? '../categories/' + categorySlug(name) + '.html' : '../index.html#/category/' + encodeURIComponent(name); }

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
        a.innerHTML = '<span>' + name + '</span>';
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
          sa.href = '../index.html#/subcategory/' + encodeURIComponent(subName);
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
        a2.innerHTML = '<span>' + name + '</span>';
        navProductsGrid.appendChild(a2);
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
    }).slice(0, 10);
    var catMatches = categories.filter(function(c){ return c.toLowerCase().indexOf(q) !== -1; }).slice(0, 6);
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
        a.href = '../products/' + p.id + '.html';
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
      a.href = '../brands/' + b.slug + '.html';
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
})();
