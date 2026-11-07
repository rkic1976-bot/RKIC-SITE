// Lightweight live counts for pages that don't load the full products-data.js
// (e.g. contact.html). Single source of truth: products-data.js (products.length)
// and brand-data.js (RKIC_BRANDS.length). Bump this file whenever a product is
// added/removed, same workflow step as updating brand-data.js/sitemap.xml.
window.RKIC_STATS = { products: 256, brands: 14 };
