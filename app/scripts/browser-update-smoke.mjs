import assert from "node:assert/strict";
import { execFileSync, spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { createReadStream, existsSync } from "node:fs";
import {
  cp,
  mkdir,
  mkdtemp,
  readFile,
  readdir,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { createServer } from "node:http";
import { createServer as createPortProbe } from "node:net";
import { tmpdir } from "node:os";
import { dirname, extname, join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = resolve(fileURLToPath(new URL(".", import.meta.url)));
const appRoot = resolve(scriptDirectory, "..");
const courseRoot = resolve(appRoot, "..");
const basePath = "/ai-workflow-course/";
const storageKey = "ai-workflow-course-state-v1";
const legacyV25 = Object.freeze({
  commit: "69d868a713d42b19b12ec11c64898b29e829be71",
  courseVersion: "2.5.0",
  buildId: "ad5f59e8f800",
  contentHash:
    "ddc88ff3b2a9ac9080b05abebad5f578de122406a6bab00bb52b28a92353258a",
  artifactTreeSha256:
    "df958cd62ff5ddd76cace021d86c46eb6f4a252215467487170639d72d84462d",
});

function chromeExecutable() {
  const candidates = [
    process.env.CHROME_PATH,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ].filter(Boolean);
  const executable = candidates.find((candidate) => existsSync(candidate));
  if (!executable) {
    throw new Error(
      "Chrome was not found. Set CHROME_PATH to run the update smoke test.",
    );
  }
  return executable;
}

async function availablePort() {
  const server = createPortProbe();
  await new Promise((resolveListen, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolveListen);
  });
  const address = server.address();
  const port = typeof address === "object" && address ? address.port : null;
  await new Promise((resolveClose) => server.close(resolveClose));
  if (!port) throw new Error("Could not reserve a local test port.");
  return port;
}

async function waitFor(check, description, timeoutMs = 15000) {
  const deadline = Date.now() + timeoutMs;
  let lastError;
  while (Date.now() < deadline) {
    try {
      const result = await check();
      if (result) return result;
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolveWait) => setTimeout(resolveWait, 100));
  }
  throw new Error(
    `${description} did not become ready.${lastError ? ` ${lastError.message}` : ""}`,
  );
}

async function createCdpClient(webSocketUrl) {
  const socket = new WebSocket(webSocketUrl);
  await new Promise((resolveOpen, reject) => {
    socket.addEventListener("open", resolveOpen, { once: true });
    socket.addEventListener("error", reject, { once: true });
  });
  let nextId = 1;
  const pending = new Map();
  socket.addEventListener("message", (event) => {
    const message = JSON.parse(String(event.data));
    if (!message.id || !pending.has(message.id)) return;
    const { resolve: resolveCall, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(message.error.message));
    else resolveCall(message.result);
  });
  return {
    close() {
      socket.close();
    },
    call(method, params = {}) {
      const id = nextId;
      nextId += 1;
      return new Promise((resolveCall, reject) => {
        pending.set(id, {
          resolve: resolveCall,
          reject: (error) => reject(new Error(`${method}: ${error.message}`)),
        });
        socket.send(JSON.stringify({ id, method, params }));
      });
    },
  };
}

function gitBlob(commit, relativePath) {
  return execFileSync("git", ["show", `${commit}:${relativePath}`], {
    cwd: courseRoot,
    encoding: null,
    maxBuffer: 32 * 1024 * 1024,
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
  });
}

function assertSafeFixturePath(relativePath) {
  assert.equal(typeof relativePath, "string");
  assert.ok(relativePath.length > 0);
  assert.equal(relativePath.includes("\\"), false);
  assert.equal(relativePath.startsWith("/"), false);
  assert.equal(/^[a-zA-Z]:/.test(relativePath), false);
  assert.equal(relativePath.split("/").includes(".."), false);
}

async function artifactTreeSha256(root) {
  const relativeFiles = [];
  async function walk(directory, prefix = "") {
    const entries = await readdir(directory, { withFileTypes: true });
    for (const entry of entries) {
      const relativePath = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) {
        await walk(join(directory, entry.name), relativePath);
      } else if (entry.isFile()) {
        relativeFiles.push(relativePath);
      }
    }
  }
  await walk(root);
  relativeFiles.sort();
  const digest = createHash("sha256");
  for (const relativePath of relativeFiles) {
    const bytes = await readFile(
      join(root, ...relativePath.split("/")),
    );
    digest.update(relativePath);
    digest.update("\0");
    digest.update(createHash("sha256").update(bytes).digest());
    digest.update("\n");
  }
  return digest.digest("hex");
}

async function materialiseLegacyV25(previousRoot) {
  execFileSync("git", ["cat-file", "-e", `${legacyV25.commit}^{commit}`], {
    cwd: courseRoot,
    stdio: "ignore",
    windowsHide: true,
  });
  const curriculumBytes = gitBlob(legacyV25.commit, "curriculum.json");
  const curriculum = JSON.parse(curriculumBytes.toString("utf8"));
  const paths = new Set([
    "curriculum.json",
    "app/scripts/build.mjs",
    "app/src/index.html",
    "app/src/styles.css",
    "app/src/app.js",
    "app/src/markdown.js",
    "app/src/sw.js",
    "app/src/favicon.svg",
  ]);
  for (const group of curriculum.groups || []) {
    for (const document of group.documents || []) {
      assertSafeFixturePath(document.sourcePath);
      paths.add(document.sourcePath);
    }
  }
  for (const relativePath of paths) {
    assertSafeFixturePath(relativePath);
    const destination = join(previousRoot, ...relativePath.split("/"));
    await mkdir(dirname(destination), { recursive: true });
    const bytes =
      relativePath === "curriculum.json"
        ? curriculumBytes
        : gitBlob(legacyV25.commit, relativePath);
    await writeFile(destination, bytes);
  }
  const legacyAppRoot = join(previousRoot, "app");
  execFileSync(process.execPath, ["scripts/build.mjs"], {
    cwd: legacyAppRoot,
    env: {
      ...process.env,
      BASE_PATH: basePath,
      GITHUB_SHA: legacyV25.commit,
    },
    encoding: "utf8",
    maxBuffer: 8 * 1024 * 1024,
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
  });
  const dist = join(legacyAppRoot, "dist");
  const version = JSON.parse(await readFile(join(dist, "version.json"), "utf8"));
  assert.deepEqual(
    {
      commit: version.commit,
      courseVersion: version.courseVersion,
      buildId: version.buildId,
      contentHash: version.contentHash,
    },
    {
      commit: legacyV25.commit.slice(0, 12),
      courseVersion: legacyV25.courseVersion,
      buildId: legacyV25.buildId,
      contentHash: legacyV25.contentHash,
    },
    "The pinned legacy source did not reproduce the accepted v2.5 identity.",
  );
  assert.equal(
    existsSync(join(dist, "asset-manifest.json")),
    false,
    "The v2.5 fixture must retain its historical no-manifest artifact format.",
  );
  assert.equal(
    await artifactTreeSha256(dist),
    legacyV25.artifactTreeSha256,
    "The pinned legacy source did not reproduce the accepted v2.5 artifact tree.",
  );
  return dist;
}

async function releaseCacheName(snapshotRoot) {
  const version = JSON.parse(
    await readFile(join(snapshotRoot, "version.json"), "utf8"),
  );
  if (!existsSync(join(snapshotRoot, "asset-manifest.json"))) {
    return `ai-workflow-course-${version.buildId}`;
  }
  const manifestBytes = await readFile(
    join(snapshotRoot, "asset-manifest.json"),
  );
  const manifestHash = createHash("sha256")
    .update(manifestBytes)
    .digest("hex");
  return `ai-workflow-course-${version.buildId}-${manifestHash}`;
}

function storedStateExpression(key) {
  return `(() => {
    const record = JSON.parse(localStorage.getItem(${JSON.stringify(key)}));
    return record?.state || record;
  })()`;
}

function mimeType(path) {
  return (
    {
      ".css": "text/css; charset=utf-8",
      ".html": "text/html; charset=utf-8",
      ".js": "text/javascript; charset=utf-8",
      ".json": "application/json; charset=utf-8",
      ".png": "image/png",
      ".svg": "image/svg+xml",
      ".webmanifest": "application/manifest+json; charset=utf-8",
    }[extname(path)] || "application/octet-stream"
  );
}

async function main() {
  const temporaryDirectory = await mkdtemp(
    join(tmpdir(), "course1-pwa-update-smoke-"),
  );
  const currentSnapshot = join(temporaryDirectory, "current");
  const legacySource = join(temporaryDirectory, "legacy-v2.5-source");
  const failedSnapshot = join(temporaryDirectory, "failed-candidate");
  const profileDirectory = join(temporaryDirectory, "chrome-profile");
  await cp(join(appRoot, "dist"), currentSnapshot, { recursive: true });
  const previousSnapshot = await materialiseLegacyV25(legacySource);
  const currentVersion = JSON.parse(
    await readFile(join(currentSnapshot, "version.json"), "utf8"),
  );
  assert.equal(currentVersion.courseVersion, "2.6.0");
  assert.equal(currentVersion.productStatus, "UNVERIFIED");
  assert.equal(
    currentVersion.distributionPurpose,
    "personal-synthetic-study",
  );
  const workflowCommit = String(process.env.GITHUB_SHA || "").toLowerCase();
  if (/^[0-9a-f]{40}$/.test(workflowCommit)) {
    assert.equal(currentVersion.commit, workflowCommit);
  } else {
    assert.match(currentVersion.commit, /^(?:working-copy|[0-9a-f]{40})$/);
  }
  const currentBuildId = currentVersion.buildId;
  const previousBuildId = legacyV25.buildId;
  assert.notEqual(currentBuildId, previousBuildId);
  await cp(currentSnapshot, failedSnapshot, { recursive: true });
  const failedStylesPath = join(failedSnapshot, "styles.css");
  const failedStyles = await readFile(failedStylesPath, "utf8");
  await writeFile(
    failedStylesPath,
    `${failedStyles}\n/* Intentionally mismatched candidate for the smoke test. */\n`,
    "utf8",
  );
  const currentCacheName = await releaseCacheName(currentSnapshot);
  const previousCacheName = await releaseCacheName(previousSnapshot);
  const failedCacheName = await releaseCacheName(failedSnapshot);
  assert.equal(failedCacheName, currentCacheName);
  assert.notEqual(currentCacheName, previousCacheName);

  let activeRoot = previousSnapshot;
  let networkAvailable = true;
  const port = await availablePort();
  const debugPort = await availablePort();
  const previewUrl = `http://127.0.0.1:${port}${basePath}`;
  const server = createServer(async (request, response) => {
    try {
      if (!networkAvailable) {
        response.writeHead(503, {
          "Cache-Control": "no-store",
          "Content-Type": "text/plain; charset=utf-8",
        });
        response.end("Offline test");
        return;
      }
      const url = new URL(request.url || "/", `http://${request.headers.host}`);
      if (!url.pathname.startsWith(basePath)) {
        response.writeHead(302, { Location: basePath });
        response.end();
        return;
      }
      const relativePath = decodeURIComponent(url.pathname.slice(basePath.length));
      const requestedPath = resolve(
        activeRoot,
        relativePath && !relativePath.endsWith("/")
          ? relativePath
          : "index.html",
      );
      if (
        requestedPath !== activeRoot &&
        !requestedPath.startsWith(`${activeRoot}${sep}`)
      ) {
        response.writeHead(403);
        response.end("Forbidden");
        return;
      }
      const fileStat = await stat(requestedPath);
      if (!fileStat.isFile()) throw new Error("Not a file");
      const headers = {
        "Content-Type": mimeType(requestedPath),
        "Cache-Control": requestedPath.endsWith("version.json")
          ? "no-store"
          : "no-cache",
      };
      if (requestedPath.endsWith("sw.js")) {
        headers["Service-Worker-Allowed"] = basePath;
      }
      response.writeHead(200, headers);
      if (request.method === "HEAD") response.end();
      else createReadStream(requestedPath).pipe(response);
    } catch {
      response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      response.end("Not found");
    }
  });

  let chromeProcess;
  let client;
  try {
    await new Promise((resolveListen, reject) => {
      server.once("error", reject);
      server.listen(port, "127.0.0.1", resolveListen);
    });
    chromeProcess = spawn(
      chromeExecutable(),
      [
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        `--remote-debugging-port=${debugPort}`,
        `--user-data-dir=${profileDirectory}`,
        "about:blank",
      ],
      { stdio: "ignore", windowsHide: true },
    );

    const target = await waitFor(async () => {
      const response = await fetch(`http://127.0.0.1:${debugPort}/json/list`);
      if (!response.ok) return null;
      const targets = await response.json();
      return targets.find((candidate) => candidate.type === "page");
    }, "Chrome debugging target");
    client = await createCdpClient(target.webSocketDebuggerUrl);
    await client.call("Page.enable");
    await client.call("Runtime.enable");

    const evaluate = async (expression) => {
      const result = await client.call("Runtime.evaluate", {
        expression,
        returnByValue: true,
        awaitPromise: true,
      });
      if (result.exceptionDetails) {
        throw new Error(result.exceptionDetails.text || "Browser evaluation failed.");
      }
      return result.result.value;
    };
    const assertCurrentStudyRelease = async (label, checkSettings = false) => {
      const release = await evaluate(`(() => {
        const boundary = document.querySelector("#release-boundary");
        const pill = document.querySelector(".release-pill");
        return {
          boundaryText: boundary?.textContent?.replace(/\\s+/g, " ").trim() || "",
          boundaryVisible: Boolean(
            boundary &&
            !boundary.hidden &&
            getComputedStyle(boundary).display !== "none" &&
            getComputedStyle(boundary).visibility !== "hidden" &&
            boundary.getClientRects().length
          ),
          pillText: pill?.textContent?.trim() || "",
          pillLabel: pill?.getAttribute("aria-label") || "",
          pillVisible: Boolean(
            pill &&
            !pill.hidden &&
            getComputedStyle(pill).display !== "none" &&
            getComputedStyle(pill).visibility !== "hidden" &&
            pill.getClientRects().length
          ),
          productStatus: window.__COURSE_APP__?.productStatus || "",
          distributionPurpose:
            window.__COURSE_APP__?.distributionPurpose || "",
          settingsProductStatus:
            document.querySelector("#settings-product-status")?.textContent?.trim() || "",
          settingsDistributionPurpose:
            document.querySelector("#settings-distribution-purpose")?.textContent?.trim() || "",
        };
      })()`);
      assert.equal(release.boundaryVisible, true, `${label}: release boundary hidden`);
      assert.match(release.boundaryText, /UNVERIFIED personal-study release/);
      assert.match(release.boundaryText, /Use synthetic data only/);
      assert.match(release.boundaryText, /cannot award Course 1 completion/);
      assert.equal(release.pillVisible, true, `${label}: release pill hidden`);
      assert.equal(release.pillText, "UNVERIFIED");
      assert.match(release.pillLabel, /UNVERIFIED personal-study release/);
      assert.equal(release.productStatus, "UNVERIFIED");
      assert.equal(release.distributionPurpose, "personal-synthetic-study");
      if (checkSettings) {
        assert.equal(release.settingsProductStatus, "UNVERIFIED");
        assert.equal(
          release.settingsDistributionPurpose,
          "Personal study with synthetic data only",
        );
      }
    };

    await client.call("Page.navigate", { url: previewUrl });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          navigator.serviceWorker?.controller !== null &&
          window.__COURSE_APP__?.buildId === ${JSON.stringify(previousBuildId)}`),
      "Controlled previous release",
    );

    await evaluate(`location.hash = "#doc=course-1-foundation-01"`);
    await waitFor(
      () => evaluate(`document.querySelector("#reader-view")?.hidden === false`),
      "Previous-release lesson",
    );
    await evaluate(`document.querySelector("#complete-button").click();
      document.querySelector("#practical-pass-button").click();
      const note = document.querySelector("#learner-note");
      note.value = "Update test note.";
      note.dispatchEvent(new Event("input", { bubbles: true }));`);
    await waitFor(
      () =>
        evaluate(`${storedStateExpression(storageKey)}
          .notes["course-1-foundation-01"] === "Update test note."`),
      "Previous-release progress",
    );
    assert.equal(
      await evaluate(`(() => {
        const record = JSON.parse(
          localStorage.getItem(${JSON.stringify(storageKey)})
        );
        return record?.schemaVersion === 2 && record?.state === undefined;
      })()`),
      true,
      "The immutable v2.5 client did not exercise its historical raw state format.",
    );
    await evaluate(`caches.open("unrelated-update-smoke-sentinel")`);

    activeRoot = failedSnapshot;
    await evaluate(`navigator.serviceWorker.getRegistration().then(
      (registration) => registration.update()
    ).catch(() => null)`);
    await waitFor(
      () =>
        evaluate(`navigator.serviceWorker.getRegistration().then(
          (registration) =>
            registration.installing === null &&
            registration.waiting === null &&
            navigator.serviceWorker.controller !== null
        )`),
      "Rejected mismatched candidate",
      20000,
    );
    assert.equal(
      await evaluate(`window.__COURSE_APP__.buildId`),
      previousBuildId,
    );
    const cachesAfterFailedCandidate = await evaluate(`caches.keys()`);
    assert.ok(cachesAfterFailedCandidate.includes(previousCacheName));
    assert.ok(!cachesAfterFailedCandidate.includes(failedCacheName));

    activeRoot = currentSnapshot;
    await evaluate(`navigator.serviceWorker.getRegistration().then(
      (registration) => registration.update()
    )`);
    await waitFor(
      () =>
        evaluate(
          `document.querySelector("#update-banner")?.hidden === false`,
        ),
      "Waiting update banner",
    );
    assert.equal(
      await evaluate(`window.__COURSE_APP__.buildId`),
      previousBuildId,
    );

    await evaluate(`document.querySelector("#update-later").click()`);
    assert.equal(
      await evaluate(`document.querySelector("#update-banner").hidden`),
      true,
    );
    assert.equal(
      await evaluate(`window.__COURSE_APP__.buildId`),
      previousBuildId,
    );
    assert.equal(
      await evaluate(`${storedStateExpression(storageKey)}
        .notes["course-1-foundation-01"]`),
      "Update test note.",
    );

    await evaluate(`location.hash = "#settings"`);
    await waitFor(
      () => evaluate(`document.querySelector("#settings-view")?.hidden === false`),
      "Previous-release Settings",
    );
    await evaluate(`document.querySelector("#settings-update-button").click()`);
    await waitFor(
      () =>
        evaluate(
          `document.querySelector("#update-banner")?.hidden === false`,
        ),
      "Redisplayed waiting update",
    );
    await evaluate(`document.querySelector("#apply-update").click()`);
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          window.__COURSE_APP__?.buildId === ${JSON.stringify(currentBuildId)}`),
      "Activated current release",
      20000,
    );
    await evaluate(`location.hash = "#settings"`);
    await waitFor(
      () => evaluate(`document.querySelector("#settings-view")?.hidden === false`),
      "Current personal-study Settings",
    );
    await assertCurrentStudyRelease("Activated current release", true);

    const retainedState = await evaluate(
      storedStateExpression(storageKey),
    );
    assert.equal(
      await evaluate(`(() => {
        const record = JSON.parse(
          localStorage.getItem(${JSON.stringify(storageKey)})
        );
        return (
          record?.storageFormat === "ai-workflow-course-storage-v1" &&
          Number.isInteger(record?.revision) &&
          record.revision > 0 &&
          record?.state?.schemaVersion === 3
        );
      })()`),
      true,
      "The current release did not migrate v2.5 state into the verified envelope.",
    );
    assert.ok(retainedState.completed.includes("course-1-foundation-01"));
    assert.ok(retainedState.practicalPassed.includes("course-1-foundation-01"));
    assert.equal(
      retainedState.notes["course-1-foundation-01"],
      "Update test note.",
    );
    const cacheNames = await evaluate(`caches.keys()`);
    assert.ok(cacheNames.includes("unrelated-update-smoke-sentinel"));
    assert.ok(
      cacheNames.includes(currentCacheName),
      `current cache missing from ${JSON.stringify(cacheNames)}`,
    );
    assert.ok(!cacheNames.includes(previousCacheName));

    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          window.__COURSE_APP__?.buildId === ${JSON.stringify(currentBuildId)} &&
          ${storedStateExpression(storageKey)}
            .notes["course-1-foundation-01"] === "Update test note."`),
      "Cold reopen after update",
    );
    await assertCurrentStudyRelease("Cold reopen after update", true);

    const tamperedAssetUrl = `${previewUrl}course-content.json`;
    const tamperResult = await evaluate(`(async () => {
      const cache = await caches.open(${JSON.stringify(currentCacheName)});
      await cache.put(
        ${JSON.stringify(tamperedAssetUrl)},
        new Response('{"tampered":true}', {
          status: 200,
          headers: { "Content-Type": "application/json; charset=utf-8" },
        }),
      );
      const response = await fetch(${JSON.stringify(tamperedAssetUrl)}, {
        cache: "no-store",
      });
      return { status: response.status, body: await response.text() };
    })()`);
    assert.deepEqual(tamperResult, {
      status: 503,
      body: "Verified course asset is unavailable.",
    });

    const expectedCourseHash = JSON.parse(
      await readFile(join(currentSnapshot, "asset-manifest.json"), "utf8"),
    ).assets["course-content.json"].sha256;
    await waitFor(
      () =>
        evaluate(`(async () => {
          const cache = await caches.open(${JSON.stringify(currentCacheName)});
          const response = await cache.match(${JSON.stringify(tamperedAssetUrl)});
          if (!response) return false;
          const digest = await crypto.subtle.digest(
            "SHA-256",
            await response.arrayBuffer(),
          );
          const hex = [...new Uint8Array(digest)]
            .map((value) => value.toString(16).padStart(2, "0"))
            .join("");
          return hex === ${JSON.stringify(expectedCourseHash)};
        })()`),
      "Verified cache restoration after same-origin mutation",
    );
    const restoredResult = await evaluate(`(async () => {
      const response = await fetch(${JSON.stringify(tamperedAssetUrl)}, {
        cache: "no-store",
      });
      const body = await response.json();
      return {
        status: response.status,
        contentHash: body.course.contentHash,
      };
    })()`);
    assert.equal(restoredResult.status, 200);
    assert.match(restoredResult.contentHash, /^[a-f0-9]{64}$/);

    const manifestUrl = `${previewUrl}asset-manifest.json`;
    const stylesUrl = `${previewUrl}styles.css`;
    const manifestTamperResult = await evaluate(`(async () => {
      const cache = await caches.open(${JSON.stringify(currentCacheName)});
      await cache.put(
        ${JSON.stringify(manifestUrl)},
        new Response('{"schemaVersion":1,"tampered":true}', {
          status: 200,
          headers: { "Content-Type": "application/json; charset=utf-8" },
        }),
      );
      const response = await fetch(${JSON.stringify(stylesUrl)}, {
        cache: "no-store",
      });
      return { status: response.status, body: await response.text() };
    })()`);
    assert.deepEqual(manifestTamperResult, {
      status: 503,
      body: "Verified course asset is unavailable.",
    });
    await waitFor(
      () =>
        evaluate(`fetch(${JSON.stringify(stylesUrl)}, { cache: "no-store" })
          .then((response) => response.status === 200)`),
      "Verified manifest restoration after same-origin mutation",
    );

    networkAvailable = false;
    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          window.__COURSE_APP__?.buildId === ${JSON.stringify(currentBuildId)} &&
          ${storedStateExpression(storageKey)}
            .notes["course-1-foundation-01"] === "Update test note."`),
      "Verified offline shell and version fallback",
    );
    await assertCurrentStudyRelease("Offline reopen", true);

    process.stdout.write(
      `Update smoke passed: immutable v2.5 ${previousBuildId} sent its legacy explicit Update now message and activated ${currentBuildId}; a mismatched candidate was rejected; Later kept v2.5 active; reading, practice, notes, and unrelated caches survived schema migration; obsolete release caches were removed; asset and manifest cache mutations returned 503 and were restored from verified network bytes; the verified offline shell and cached version fallback reopened with the server unavailable.\n`,
    );
  } finally {
    client?.close();
    chromeProcess?.kill();
    await new Promise((resolveClose) => server.close(resolveClose));
    await rm(temporaryDirectory, { recursive: true, force: true, maxRetries: 4 });
  }
}

await main();
