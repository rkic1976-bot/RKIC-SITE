// RKIC — "You May Also Need" (Related Products) renderer for standalone product pages.
// Depends on: RKIC_PRODUCTS (from related-products-data.js) and a per-page
// `const CURRENT_PRODUCT_ID = '...';` declared before this script tag.
// Matching preference: same sub-category first, then same category, then same brand.
// Renders into #relatedGrid; hides #relatedSection entirely if nothing matches.
(function(){
  if (typeof RKIC_PRODUCTS === 'undefined' || typeof CURRENT_PRODUCT_ID === 'undefined') return;
  var grid = document.getElementById('relatedGrid');
  var section = document.getElementById('relatedSection');
  if (!grid) return;

  var current = null;
  for (var i = 0; i < RKIC_PRODUCTS.length; i++) {
    if (RKIC_PRODUCTS[i].id === CURRENT_PRODUCT_ID) { current = RKIC_PRODUCTS[i]; break; }
  }
  if (!current) { if (section) section.style.display = 'none'; return; }

  var pool = RKIC_PRODUCTS.filter(function(p){ return p.id !== CURRENT_PRODUCT_ID; });
  var picked = [];
  var used = {};
  function addFrom(list){
    for (var j = 0; j < list.length && picked.length < 4; j++){
      var p = list[j];
      if (!used[p.id]) { picked.push(p); used[p.id] = true; }
    }
  }
  if (current.subcategory) {
    addFrom(pool.filter(function(p){ return p.category === current.category && p.subcategory === current.subcategory; }));
  }
  addFrom(pool.filter(function(p){ return p.category === current.category; }));
  addFrom(pool.filter(function(p){ return p.brand === current.brand; }));

  if (picked.length === 0) { if (section) section.style.display = 'none'; return; }

  var html = '';
  picked.forEach(function(p){
    html += '<a class="related-card" href="' + p.id + '.html">' +
      '<div class="related-thumb"><img src="' + p.thumb + '" alt="' + p.name + '" loading="lazy"></div>' +
      '<div class="related-name">' + p.name + '</div>' +
      (p.code ? '<div class="related-code">' + p.code + '</div>' : '') +
      '</a>';
  });
  grid.innerHTML = html;
})();
