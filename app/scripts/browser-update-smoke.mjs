import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createReadStream, existsSync } from "node:fs";
import {
  cp,
  mkdtemp,
  readFile,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { createServer } from "node:http";
import { createServer as createPortProbe } from "node:net";
import { tmpdir } from "node:os";
import { extname, join, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = resolve(fileURLToPath(new URL(".", import.meta.url)));
const appRoot = resolve(scriptDirectory, "..");
const basePath = "/ai-workflow-course/";
const storageKey = "ai-workflow-course-state-v1";

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

async function makePreviousSnapshot(currentRoot, previousRoot) {
  await cp(currentRoot, previousRoot, { recursive: true });
  const versionPath = join(previousRoot, "version.json");
  const version = JSON.parse(await readFile(versionPath, "utf8"));
  const currentBuildId = version.buildId;
  const previousBuildId = "000000000000";
  assert.notEqual(currentBuildId, previousBuildId);

  for (const relativePath of ["index.html", "sw.js"]) {
    const path = join(previousRoot, relativePath);
    const source = await readFile(path, "utf8");
    assert.ok(source.includes(currentBuildId));
    await writeFile(
      path,
      source.replaceAll(currentBuildId, previousBuildId),
      "utf8",
    );
  }
  version.buildId = previousBuildId;
  await writeFile(versionPath, `${JSON.stringify(version, null, 2)}\n`, "utf8");
  return { currentBuildId, previousBuildId };
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
  const previousSnapshot = join(temporaryDirectory, "previous");
  const profileDirectory = join(temporaryDirectory, "chrome-profile");
  await cp(join(appRoot, "dist"), currentSnapshot, { recursive: true });
  const { currentBuildId, previousBuildId } = await makePreviousSnapshot(
    currentSnapshot,
    previousSnapshot,
  );

  let activeRoot = previousSnapshot;
  const port = await availablePort();
  const debugPort = await availablePort();
  const previewUrl = `http://127.0.0.1:${port}${basePath}`;
  const server = createServer(async (request, response) => {
    try {
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
        evaluate(`JSON.parse(localStorage.getItem(${JSON.stringify(storageKey)}))
          .notes["course-1-foundation-01"] === "Update test note."`),
      "Previous-release progress",
    );
    await evaluate(`caches.open("unrelated-update-smoke-sentinel")`);

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
      await evaluate(`JSON.parse(localStorage.getItem(${JSON.stringify(storageKey)}))
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

    const retainedState = await evaluate(
      `JSON.parse(localStorage.getItem(${JSON.stringify(storageKey)}))`,
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
      cacheNames.includes(`ai-workflow-course-${currentBuildId}`),
      `current cache missing from ${JSON.stringify(cacheNames)}`,
    );
    assert.ok(!cacheNames.includes(`ai-workflow-course-${previousBuildId}`));

    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          window.__COURSE_APP__?.buildId === ${JSON.stringify(currentBuildId)} &&
          JSON.parse(localStorage.getItem(${JSON.stringify(storageKey)}))
            .notes["course-1-foundation-01"] === "Update test note."`),
      "Cold reopen after update",
    );

    process.stdout.write(
      `Update smoke passed: Later preserved build ${previousBuildId}; Update now activated ${currentBuildId}; reading, practice, notes, and unrelated caches survived; obsolete course cache was removed.\n`,
    );
  } finally {
    client?.close();
    chromeProcess?.kill();
    await new Promise((resolveClose) => server.close(resolveClose));
    await rm(temporaryDirectory, { recursive: true, force: true, maxRetries: 4 });
  }
}

await main();
