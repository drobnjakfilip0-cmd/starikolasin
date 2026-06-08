const CACHE_NAME = 'domkulture-v1';

// App shell — cached on install
const SHELL = [
  '/',
  '/about/',
  '/casopis/',
  '/bioskop/',
  '/likovna-kolonija/',
  '/static/core/style.css',
  'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Alumni+Sans+SC:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
  '/media/images/logo.jpg',
];

// ── INSTALL: cache shell ─────────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(SHELL))
  );
  self.skipWaiting();
});

// ── ACTIVATE: remove old caches ──────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// ── FETCH: network-first for pages, cache-first for assets ───────
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET and cross-origin (except CDN assets we cached)
  if (request.method !== 'GET') return;
  if (url.origin !== location.origin &&
      !url.hostname.includes('cloudinary.com') &&
      !url.hostname.includes('fonts.g') &&
      !url.hostname.includes('cdnjs.cloudflare.com')) return;

  // Static assets, fonts, images → cache-first
  if (
    url.pathname.startsWith('/static/') ||
    url.pathname.startsWith('/media/') ||
    url.hostname.includes('fonts.g') ||
    url.hostname.includes('cloudinary.com') ||
    url.hostname.includes('cdnjs.cloudflare.com')
  ) {
    event.respondWith(
      caches.match(request).then(cached => {
        if (cached) return cached;
        return fetch(request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // HTML pages → network-first, fall back to cache
  event.respondWith(
    fetch(request)
      .then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        }
        return response;
      })
      .catch(() => caches.match(request).then(cached => cached || caches.match('/')))
  );
});
