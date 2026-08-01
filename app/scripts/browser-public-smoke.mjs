import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { mkdir, mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { createServer } from "node:net";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = resolve(fileURLToPath(new URL(".", import.meta.url)));
const appRoot = resolve(scriptDirectory, "..");
const expectedPath = "/ai-workflow-course/";
const cachePrefix = "ai-workflow-course-";

function parseArguments(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!flag?.startsWith("--") || value === undefined) {
      throw new Error("Arguments must be supplied as --name value pairs.");
    }
    values[flag.slice(2)] = value;
  }
  for (const required of ["public-url", "expected-commit", "dist", "report"]) {
    if (!values[required]) throw new Error(`Missing --${required}.`);
  }
  return values;
}

function checkedPublicUrl(value) {
  const parsed = new URL(value);
  if (
    parsed.protocol !== "https:" ||
    parsed.username ||
    parsed.password ||
    parsed.search ||
    parsed.hash ||
    parsed.pathname !== expectedPath ||
    parsed.hostname === "localhost" ||
    parsed.hostname.endsWith(".localhost")
  ) {
    throw new Error(`Public URL must be one HTTPS origin ending in ${expectedPath}`);
  }
  return parsed.href;
}

function checkedCommit(value) {
  const commit = value.trim().toLowerCase();
  if (!/^[a-f0-9]{40}$/.test(commit)) {
    throw new Error("Expected commit must be one full lower-case Git SHA.");
  }
  return commit;
}

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
    throw new Error("Chrome was not found. Set CHROME_PATH for the public PWA check.");
  }
  return executable;
}

async function availablePort() {
  const server = createServer();
  await new Promise((resolveListen, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolveListen);
  });
  const address = server.address();
  const port = typeof address === "object" && address ? address.port : null;
  await new Promise((resolveClose) => server.close(resolveClose));
  if (!port) throw new Error("Could not reserve a Chrome debugging port.");
  return port;
}

async function waitFor(check, description, timeoutMs = 30000) {
  const deadline = Date.now() + timeoutMs;
  let lastError;
  while (Date.now() < deadline) {
    try {
      const value = await check();
      if (value) return value;
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolveWait) => setTimeout(resolveWait, 120));
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
  const listeners = new Map();
  socket.addEventListener("message", (event) => {
    const message = JSON.parse(String(event.data));
    if (message.id && pending.has(message.id)) {
      const { resolve: resolveCall, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) reject(new Error(message.error.message));
      else resolveCall(message.result);
      return;
    }
    for (const listener of listeners.get(message.method) || []) {
      listener(message.params || {});
    }
  });
  return {
    close() {
      socket.close();
    },
    on(method, listener) {
      const current = listeners.get(method) || [];
      current.push(listener);
      listeners.set(method, current);
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

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

async function writeReport(path, report) {
  const destination = resolve(path);
  await mkdir(dirname(destination), { recursive: true });
  await writeFile(destination, `${JSON.stringify(report, null, 2)}\n`, "utf8");
}

async function waitForProcessExit(childProcess, timeoutMs) {
  if (!childProcess || childProcess.exitCode !== null) return true;
  return new Promise((resolveExit) => {
    let settled = false;
    const finish = (exited) => {
      if (settled) return;
      settled = true;
      clearTimeout(timeout);
      childProcess.off("exit", onExit);
      resolveExit(exited);
    };
    const onExit = () => finish(true);
    const timeout = setTimeout(
      () => finish(childProcess.exitCode !== null),
      timeoutMs,
    );
    childProcess.once("exit", onExit);
    if (childProcess.exitCode !== null) finish(true);
  });
}

async function main() {
  const args = parseArguments(process.argv.slice(2));
  const publicUrl = checkedPublicUrl(args["public-url"]);
  const expectedCommit = checkedCommit(args["expected-commit"]);
  const dist = resolve(appRoot, args.dist);
  const version = JSON.parse(await readFile(join(dist, "version.json"), "utf8"));
  const manifestBytes = await readFile(join(dist, "asset-manifest.json"));
  const manifest = JSON.parse(manifestBytes.toString("utf8"));
  assert.equal(version.commit, expectedCommit);
  assert.equal(version.courseVersion, "2.6.0");
  assert.equal(version.productStatus, "UNVERIFIED");
  assert.equal(version.distributionPurpose, "personal-synthetic-study");
  assert.equal(manifest.buildId, version.buildId);
  assert.equal(manifest.provenance?.commit, expectedCommit);

  const manifestSha256 = sha256(manifestBytes);
  const expectedCacheName = `${cachePrefix}${version.buildId}-${manifestSha256}`;
  const expectedCacheUrls = [
    new URL("asset-manifest.json", publicUrl).href,
    ...Object.keys(manifest.assets).map((relative) => new URL(relative, publicUrl).href),
  ].sort();
  const profileDirectory = await mkdtemp(join(tmpdir(), "course1-public-pwa-"));
  assert.deepEqual(await readdir(profileDirectory), []);
  const debugPort = await availablePort();
  const checkedUrl = new URL(publicUrl);
  checkedUrl.searchParams.set("course1-public-browser", expectedCommit);
  let chromeProcess;
  let client;
  let offline = false;
  const browserEvents = [];
  const report = {
    result: "FAIL",
    publicUrl,
    expectedCommit,
    courseVersion: version.courseVersion,
    buildId: version.buildId,
    productStatus: version.productStatus,
    distributionPurpose: version.distributionPurpose,
    expectedCacheName,
    expectedCacheUrls,
    freshProfile: true,
    browserEvents,
  };

  try {
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
    client.on("Runtime.exceptionThrown", (event) => {
      browserEvents.push({ type: "exception", detail: event.exceptionDetails?.text || "" });
    });
    client.on("Log.entryAdded", (event) => {
      if (["error", "warning"].includes(event.entry?.level)) {
        browserEvents.push({
          type: "log",
          level: event.entry.level,
          text: event.entry.text,
          url: event.entry.url || "",
        });
      }
    });
    await client.call("Page.enable");
    await client.call("Runtime.enable");
    await client.call("Network.enable");
    await client.call("Log.enable");
    report.browser = await client.call("Browser.getVersion");

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

    await client.call("Page.navigate", { url: checkedUrl.href });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          window.__COURSE_APP__?.buildId === ${JSON.stringify(version.buildId)} &&
          window.__COURSE_APP__?.productStatus === "UNVERIFIED" &&
          window.__COURSE_APP__?.distributionPurpose === "personal-synthetic-study"`),
      "Current public study release",
    );
    report.onlineRelease = await evaluate(`(() => {
      const boundary = document.querySelector("#release-boundary");
      const pill = document.querySelector(".release-pill");
      return {
        title: document.title,
        boundaryText: boundary?.textContent?.replace(/\\s+/g, " ").trim() || "",
        boundaryVisible: Boolean(boundary && !boundary.hidden && boundary.getClientRects().length),
        pillText: pill?.textContent?.trim() || "",
        pillVisible: Boolean(pill && !pill.hidden && pill.getClientRects().length),
      };
    })()`);
    assert.equal(report.onlineRelease.boundaryVisible, true);
    assert.match(report.onlineRelease.boundaryText, /UNVERIFIED personal-study release/);
    assert.match(report.onlineRelease.boundaryText, /Use synthetic data only/);
    assert.equal(report.onlineRelease.pillText, "UNVERIFIED");
    assert.equal(report.onlineRelease.pillVisible, true);

    report.registration = await waitFor(
      () =>
        evaluate(`(async () => {
          const registration = await navigator.serviceWorker.getRegistration(
            ${JSON.stringify(publicUrl)}
          );
          const controller = navigator.serviceWorker.controller;
          if (
            !registration ||
            registration.scope !== ${JSON.stringify(publicUrl)} ||
            registration.installing ||
            registration.waiting ||
            registration.active?.state !== "activated" ||
            controller?.scriptURL !== ${JSON.stringify(new URL("sw.js", publicUrl).href)}
          ) return null;
          return {
            scope: registration.scope,
            activeState: registration.active.state,
            activeScriptUrl: registration.active.scriptURL,
            controllerScriptUrl: controller.scriptURL,
          };
        })()`),
      "Fresh-profile service-worker activation",
    );

    report.cache = await evaluate(`(async () => {
      const names = (await caches.keys()).filter((name) =>
        name.startsWith(${JSON.stringify(cachePrefix)})
      ).sort();
      const cache = await caches.open(${JSON.stringify(expectedCacheName)});
      const urls = (await cache.keys()).map((request) => request.url).sort();
      return { names, urls };
    })()`);
    assert.deepEqual(report.cache.names, [expectedCacheName]);
    assert.deepEqual(report.cache.urls, expectedCacheUrls);

    await client.call("Network.emulateNetworkConditions", {
      offline: true,
      latency: 0,
      downloadThroughput: 0,
      uploadThroughput: 0,
      connectionType: "none",
    });
    offline = true;
    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          window.__COURSE_APP__?.buildId === ${JSON.stringify(version.buildId)} &&
          navigator.serviceWorker.controller?.scriptURL ===
            ${JSON.stringify(new URL("sw.js", publicUrl).href)}`),
      "Offline public PWA reopen",
    );
    report.offlineRelease = await evaluate(`(() => ({
      buildId: window.__COURSE_APP__?.buildId || "",
      productStatus: window.__COURSE_APP__?.productStatus || "",
      distributionPurpose: window.__COURSE_APP__?.distributionPurpose || "",
      boundaryVisible: Boolean(
        document.querySelector("#release-boundary")?.getClientRects().length
      ),
      pillText: document.querySelector(".release-pill")?.textContent?.trim() || "",
    }))()`);
    assert.deepEqual(report.offlineRelease, {
      buildId: version.buildId,
      productStatus: "UNVERIFIED",
      distributionPurpose: "personal-synthetic-study",
      boundaryVisible: true,
      pillText: "UNVERIFIED",
    });
    const fatalBrowserEvents = browserEvents.filter(
      (event) => event.type === "exception" || event.level === "error",
    );
    report.fatalBrowserEvents = fatalBrowserEvents;
    assert.deepEqual(fatalBrowserEvents, []);
    report.result = "PASS";
  } catch (error) {
    report.failure = error instanceof Error ? error.message : String(error);
  } finally {
    if (client && offline) {
      try {
        await client.call("Network.emulateNetworkConditions", {
          offline: false,
          latency: 0,
          downloadThroughput: -1,
          uploadThroughput: -1,
          connectionType: "wifi",
        });
      } catch {
        // Cleanup continues even if Chrome has already exited.
      }
    }
    if (client && chromeProcess?.exitCode === null) {
      try {
        await Promise.race([
          client.call("Browser.close").catch(() => undefined),
          new Promise((resolveWait) => setTimeout(resolveWait, 1500)),
        ]);
      } catch {
        // The process fallback below still closes Chrome.
      }
    }
    client?.close();
    if (chromeProcess && !(await waitForProcessExit(chromeProcess, 3000))) {
      chromeProcess.kill();
      await waitForProcessExit(chromeProcess, 3000);
    }
    try {
      await rm(profileDirectory, {
        recursive: true,
        force: true,
        maxRetries: 15,
        retryDelay: 200,
      });
    } catch (error) {
      report.cleanupFailure = error instanceof Error ? error.message : String(error);
      if (report.result === "PASS") {
        report.result = "FAIL";
        report.failure = `Temporary Chrome profile cleanup failed: ${report.cleanupFailure}`;
      }
    }
    report.verifiedAt = new Date().toISOString();
    await writeReport(args.report, report);
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  }
  return report.result === "PASS" ? 0 : 1;
}

process.exitCode = await main();
