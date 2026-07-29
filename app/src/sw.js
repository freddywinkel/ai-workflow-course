const BASE_PATH = "__BASE_PATH__";
const BUILD_ID = "__BUILD_ID__";
const CONTENT_HASH = "__CONTENT_HASH__";
const BUILD_PROVENANCE = "__BUILD_PROVENANCE__";
const ASSET_MANIFEST_SHA256 = "__ASSET_MANIFEST_SHA256__";
const CACHE_PREFIX = "ai-workflow-course-";
const CANDIDATE_CACHE_NAME =
  `${CACHE_PREFIX}${BUILD_ID}-${ASSET_MANIFEST_SHA256}`;
const REPAIR_CACHE_NAME = `${CANDIDATE_CACHE_NAME}-repair`;
const ASSET_MANIFEST_URL = `${BASE_PATH}asset-manifest.json`;
const PRECACHE_ASSETS = Object.freeze({
  "index.html": "text/html",
  "bootstrap.js": "text/javascript",
  "app.js": "text/javascript",
  "markdown.js": "text/javascript",
  "state.js": "text/javascript",
  "styles.css": "text/css",
  "favicon.svg": "image/svg+xml",
  "course-content.json": "application/json",
  "manifest.webmanifest": "application/manifest+json",
  "version.json": "application/json",
  "icons/icon-192.png": "image/png",
  "icons/icon-512.png": "image/png",
  "icons/icon-maskable-512.png": "image/png",
  "icons/apple-touch-icon.png": "image/png",
});
const PRECACHE_PATHS = Object.freeze(Object.keys(PRECACHE_ASSETS));
const PRECACHE_URLS = Object.freeze(
  PRECACHE_PATHS.map((relativePath) => `${BASE_PATH}${relativePath}`),
);
const ALLOWED_PATHS = new Set([
  new URL(ASSET_MANIFEST_URL, self.location.origin).pathname,
  ...PRECACHE_URLS.map((url) => new URL(url, self.location.origin).pathname),
]);
let repairPromise = null;

function bytesToHex(bytes) {
  return [...new Uint8Array(bytes)]
    .map((value) => value.toString(16).padStart(2, "0"))
    .join("");
}

async function sha256(bytes) {
  return bytesToHex(await crypto.subtle.digest("SHA-256", bytes));
}

function expectedRelativePath(url) {
  const parsed = new URL(url, self.location.origin);
  const baseUrl = new URL(BASE_PATH, self.location.origin);
  if (
    parsed.origin !== self.location.origin ||
    !parsed.pathname.startsWith(baseUrl.pathname)
  ) {
    throw new Error("Asset URL is outside the service-worker scope.");
  }
  return decodeURIComponent(parsed.pathname.slice(baseUrl.pathname.length));
}

function requestFor(url, cache = "reload") {
  return new Request(new URL(url, self.location.origin), {
    cache,
    credentials: "same-origin",
    redirect: "error",
  });
}

function responseMediaType(response) {
  return (response.headers.get("Content-Type") || "")
    .split(";", 1)[0]
    .trim()
    .toLowerCase();
}

function assertResponseIdentity(requestUrl, response, expectedContentType) {
  const expectedUrl = new URL(requestUrl, self.location.origin);
  const finalUrl = new URL(response.url);
  if (
    !response.ok ||
    response.status !== 200 ||
    response.type === "opaque" ||
    response.redirected ||
    finalUrl.origin !== self.location.origin ||
    finalUrl.href !== expectedUrl.href ||
    responseMediaType(response) !== expectedContentType.toLowerCase()
  ) {
    throw new Error(`Asset response failed release checks: ${expectedUrl.pathname}`);
  }
}

function assertExactManifest(manifest) {
  if (
    manifest?.schemaVersion !== 1 ||
    manifest.buildId !== BUILD_ID ||
    manifest.contentHash !== CONTENT_HASH ||
    manifest.provenance?.commit !== BUILD_PROVENANCE ||
    !manifest.assets ||
    typeof manifest.assets !== "object" ||
    Array.isArray(manifest.assets)
  ) {
    throw new Error("Asset manifest identifies another release.");
  }

  const actualPaths = Object.keys(manifest.assets).sort();
  const expectedPaths = [...PRECACHE_PATHS].sort();
  if (
    actualPaths.length !== expectedPaths.length ||
    actualPaths.some((path, index) => path !== expectedPaths[index])
  ) {
    throw new Error("Asset manifest does not contain the exact release asset set.");
  }

  for (const relativePath of expectedPaths) {
    const metadata = manifest.assets[relativePath];
    if (
      !metadata ||
      Object.keys(metadata).sort().join(",") !== "contentType,sha256" ||
      !/^[a-f0-9]{64}$/.test(metadata.sha256) ||
      metadata.contentType !== PRECACHE_ASSETS[relativePath]
    ) {
      throw new Error(`Invalid asset metadata: ${relativePath}`);
    }
  }
}

async function verifyManifestResponse(response) {
  assertResponseIdentity(ASSET_MANIFEST_URL, response, "application/json");
  const preservedResponse = response.clone();
  const bytes = await response.arrayBuffer();
  if ((await sha256(bytes)) !== ASSET_MANIFEST_SHA256) {
    throw new Error("Asset manifest hash does not match the service worker.");
  }
  const manifest = JSON.parse(
    new TextDecoder("utf-8", { fatal: true }).decode(bytes),
  );
  assertExactManifest(manifest);
  return { manifest, response: preservedResponse };
}

async function loadVerifiedNetworkManifest() {
  const request = requestFor(ASSET_MANIFEST_URL);
  const response = await fetch(request);
  const verified = await verifyManifestResponse(response);
  return { ...verified, request };
}

async function loadVerifiedCachedManifest(cache) {
  const request = requestFor(ASSET_MANIFEST_URL);
  const response = await cache.match(request);
  if (!response) throw new Error("Verified asset manifest is unavailable.");
  const verified = await verifyManifestResponse(response);
  return { ...verified, request };
}

async function verifyAssetResponse(url, response, metadata) {
  assertResponseIdentity(url, response, metadata.contentType);
  const preservedResponse = response.clone();
  const bytes = await response.arrayBuffer();
  if ((await sha256(bytes)) !== metadata.sha256) {
    throw new Error(`Asset hash mismatch: ${expectedRelativePath(url)}`);
  }
  return preservedResponse;
}

async function fetchVerifiedAsset(url, metadata) {
  const request = requestFor(url);
  const response = await fetch(request);
  return {
    request,
    response: await verifyAssetResponse(url, response, metadata),
  };
}

async function loadVerifiedCachedAsset(cache, relativePath, metadata) {
  const url = `${BASE_PATH}${relativePath}`;
  const request = requestFor(url);
  const response = await cache.match(request);
  if (!response) {
    throw new Error(`Verified course asset is unavailable: ${relativePath}`);
  }
  return verifyAssetResponse(url, response, metadata);
}

async function populateReleaseCache(cacheName) {
  const cache = await caches.open(cacheName);
  const verifiedManifest = await loadVerifiedNetworkManifest();
  await cache.put(
    verifiedManifest.request,
    verifiedManifest.response.clone(),
  );
  for (const relativePath of PRECACHE_PATHS) {
    const verified = await fetchVerifiedAsset(
      `${BASE_PATH}${relativePath}`,
      verifiedManifest.manifest.assets[relativePath],
    );
    await cache.put(verified.request, verified.response);
  }
}

async function validateCachedRelease(cacheName) {
  const cacheNames = await caches.keys();
  if (!cacheNames.includes(cacheName)) {
    throw new Error("Verified release cache is unavailable.");
  }
  const cache = await caches.open(cacheName);
  const cachedRequests = await cache.keys();
  const actualUrls = cachedRequests.map((request) => request.url).sort();
  const expectedUrls = [
    new URL(ASSET_MANIFEST_URL, self.location.origin).href,
    ...PRECACHE_URLS.map((url) => new URL(url, self.location.origin).href),
  ].sort();
  if (
    actualUrls.length !== expectedUrls.length ||
    actualUrls.some((url, index) => url !== expectedUrls[index])
  ) {
    throw new Error("Verified release cache does not contain the exact asset set.");
  }

  const verifiedManifest = await loadVerifiedCachedManifest(cache);
  for (const relativePath of PRECACHE_PATHS) {
    await loadVerifiedCachedAsset(
      cache,
      relativePath,
      verifiedManifest.manifest.assets[relativePath],
    );
  }
  return verifiedManifest.manifest;
}

async function repairActiveRelease() {
  if (repairPromise) return repairPromise;
  repairPromise = (async () => {
    await caches.delete(REPAIR_CACHE_NAME);
    try {
      await populateReleaseCache(REPAIR_CACHE_NAME);
      await validateCachedRelease(REPAIR_CACHE_NAME);

      const stagedCache = await caches.open(REPAIR_CACHE_NAME);
      const activeCache = await caches.open(CANDIDATE_CACHE_NAME);
      for (const existingRequest of await activeCache.keys()) {
        await activeCache.delete(existingRequest);
      }
      for (const stagedRequest of await stagedCache.keys()) {
        const stagedResponse = await stagedCache.match(stagedRequest);
        if (!stagedResponse) {
          throw new Error("Verified repair cache changed during restoration.");
        }
        await activeCache.put(stagedRequest, stagedResponse);
      }
      await validateCachedRelease(CANDIDATE_CACHE_NAME);
    } finally {
      await caches.delete(REPAIR_CACHE_NAME);
    }
  })();
  try {
    return await repairPromise;
  } finally {
    repairPromise = null;
  }
}

function unavailableResponse(message) {
  return new Response(message, {
    status: 503,
    headers: {
      "Cache-Control": "no-store",
      "Content-Type": "text/plain; charset=utf-8",
      "X-Content-Type-Options": "nosniff",
    },
  });
}

async function serveVerifiedCachedPath(relativePath, unavailableMessage) {
  try {
    const cache = await caches.open(CANDIDATE_CACHE_NAME);
    const verifiedManifest = await loadVerifiedCachedManifest(cache);
    if (relativePath === "asset-manifest.json") {
      return verifiedManifest.response;
    }
    const metadata = verifiedManifest.manifest.assets[relativePath];
    if (!metadata) throw new Error("Requested asset is outside the release manifest.");
    return await loadVerifiedCachedAsset(cache, relativePath, metadata);
  } catch {
    try {
      await repairActiveRelease();
    } catch {
      // The current request remains unavailable if trusted bytes cannot be restored.
    }
    return unavailableResponse(unavailableMessage);
  }
}

function assertStructurallyValidNetworkVersion(version) {
  const sourceVerifiedThrough =
    version?.sourceVerifiedThrough ?? version?.verifiedThrough;
  const hasSeparatedDates =
    version?.sourceVerifiedThrough !== undefined ||
    version?.contentRevisionThrough !== undefined;
  if (
    !version ||
    !/^[a-f0-9]{12}$/.test(version.buildId || "") ||
    !/^[a-f0-9]{64}$/.test(version.contentHash || "") ||
    !/^\d+\.\d+\.\d+$/.test(version.courseVersion || "") ||
    !/^\d{4}-\d{2}-\d{2}$/.test(sourceVerifiedThrough || "") ||
    (version.verifiedThrough !== undefined &&
      version.verifiedThrough !== sourceVerifiedThrough) ||
    (hasSeparatedDates &&
      (!/^\d{4}-\d{2}-\d{2}$/.test(version.sourceVerifiedThrough || "") ||
        !/^\d{4}-\d{2}-\d{2}$/.test(version.contentRevisionThrough || ""))) ||
    !(
      version.commit === "working-copy" ||
      /^[a-f0-9]{40}$/.test(version.commit || "")
    )
  ) {
    throw new Error("Network version metadata is malformed.");
  }
}

async function fetchStructurallyValidNetworkVersion() {
  const url = `${BASE_PATH}version.json`;
  const response = await fetch(requestFor(url, "no-store"));
  assertResponseIdentity(url, response, "application/json");
  const preservedResponse = response.clone();
  const bytes = await response.arrayBuffer();
  const version = JSON.parse(
    new TextDecoder("utf-8", { fatal: true }).decode(bytes),
  );
  assertStructurallyValidNetworkVersion(version);
  return preservedResponse;
}

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      await caches.delete(CANDIDATE_CACHE_NAME);
      try {
        await populateReleaseCache(CANDIDATE_CACHE_NAME);
        await validateCachedRelease(CANDIDATE_CACHE_NAME);
      } catch (error) {
        await caches.delete(CANDIDATE_CACHE_NAME);
        throw error;
      }
    })(),
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      await validateCachedRelease(CANDIDATE_CACHE_NAME);
      const cacheNames = await caches.keys();
      await Promise.all(
        cacheNames
          .filter(
            (name) =>
              name.startsWith(CACHE_PREFIX) && name !== CANDIDATE_CACHE_NAME,
          )
          .map((name) => caches.delete(name)),
      );
      await self.clients.claim();
    })(),
  );
});

self.addEventListener("message", (event) => {
  const message = event.data;
  if (
    !message ||
    typeof message !== "object" ||
    Array.isArray(message) ||
    message.type !== "SKIP_WAITING"
  ) {
    return;
  }
  try {
    const clientUrl = new URL(event.source?.url || "");
    const messageKeys = Object.keys(message).sort();
    const isLegacyExplicitAction =
      messageKeys.length === 1 && messageKeys[0] === "type";
    const isCurrentExplicitAction =
      messageKeys.length === 2 &&
      messageKeys[0] === "type" &&
      messageKeys[1] === "workerScriptUrl" &&
      message.workerScriptUrl === self.location.href;
    if (
      event.source?.type !== "window" ||
      clientUrl.origin !== self.location.origin ||
      !clientUrl.pathname.startsWith(BASE_PATH) ||
      (!isLegacyExplicitAction && !isCurrentExplicitAction)
    ) {
      return;
    }
    event.waitUntil(
      (async () => {
        await validateCachedRelease(CANDIDATE_CACHE_NAME);
        await self.skipWaiting();
      })(),
    );
  } catch {
    // A foreign or malformed client message cannot activate this worker.
  }
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;

  const url = new URL(request.url);
  const scopePath = new URL(BASE_PATH, self.location.origin).pathname;
  if (
    url.origin !== self.location.origin ||
    !(url.pathname === scopePath.slice(0, -1) || url.pathname.startsWith(scopePath))
  ) {
    return;
  }

  if (url.pathname === `${scopePath}version.json`) {
    event.respondWith(
      fetchStructurallyValidNetworkVersion().catch(() =>
        serveVerifiedCachedPath(
          "version.json",
          "Verified version information is unavailable.",
        ),
      ),
    );
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(
      serveVerifiedCachedPath(
        "index.html",
        "Verified offline course shell is unavailable.",
      ),
    );
    return;
  }

  if (!ALLOWED_PATHS.has(url.pathname)) return;
  const relativePath = expectedRelativePath(url);
  event.respondWith(
    serveVerifiedCachedPath(
      relativePath,
      "Verified course asset is unavailable.",
    ),
  );
});
