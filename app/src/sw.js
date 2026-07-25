const BASE_PATH = "__BASE_PATH__";
const BUILD_ID = "__BUILD_ID__";
const CACHE_PREFIX = "ai-workflow-course-";
const CACHE_NAME = `${CACHE_PREFIX}${BUILD_ID}`;
const PRECACHE_URLS = [
  BASE_PATH,
  `${BASE_PATH}index.html`,
  `${BASE_PATH}app.js`,
  `${BASE_PATH}styles.css`,
  `${BASE_PATH}favicon.svg`,
  `${BASE_PATH}course-content.json`,
  `${BASE_PATH}manifest.webmanifest`,
  `${BASE_PATH}version.json`,
  `${BASE_PATH}icons/icon-192.png`,
  `${BASE_PATH}icons/icon-512.png`,
  `${BASE_PATH}icons/icon-maskable-512.png`,
  `${BASE_PATH}icons/apple-touch-icon.png`,
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      await Promise.all(
        PRECACHE_URLS.map(async (url) => {
          const request = new Request(url, { cache: "reload" });
          const response = await fetch(request);
          if (!response.ok) {
            throw new Error(`Precache failed for ${url}: ${response.status}`);
          }
          await cache.put(request, response);
        }),
      );
    })(),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      const cacheNames = await caches.keys();
      await Promise.all(
        cacheNames
          .filter((name) => name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME)
          .map((name) => caches.delete(name)),
      );
      await self.clients.claim();
    })(),
  );
});

self.addEventListener("message", (event) => {
  if (event.data?.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin || !url.pathname.startsWith(BASE_PATH)) {
    return;
  }

  if (url.pathname.endsWith("/version.json")) {
    event.respondWith(
      fetch(new Request(request, { cache: "no-store" })).catch(async () => {
        const cache = await caches.open(CACHE_NAME);
        return cache.match(request);
      }),
    );
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(
      (async () => {
        const cache = await caches.open(CACHE_NAME);
        return (
          (await cache.match(BASE_PATH)) ||
          (await cache.match(`${BASE_PATH}index.html`)) ||
          fetch(request)
        );
      })(),
    );
    return;
  }

  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE_NAME);
      const cached = await cache.match(request);
      if (cached) return cached;
      try {
        const response = await fetch(request);
        if (response.ok) {
          await cache.put(request, response.clone());
        }
        return response;
      } catch {
        return new Response("Offline and not cached", {
          status: 503,
          headers: { "Content-Type": "text/plain; charset=utf-8" },
        });
      }
    })(),
  );
});
