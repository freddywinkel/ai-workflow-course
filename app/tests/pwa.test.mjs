import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readFile, stat } from "node:fs/promises";
import { join, resolve } from "node:path";
import { before, test } from "node:test";
import { fileURLToPath } from "node:url";

const appRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const distRoot = join(appRoot, "dist");
const nodeExecutable = process.execPath;
let buildModule;
let bundle;
let manifest;
let version;
let appSource;
let serviceWorkerSource;
let htmlSource;
let cssSource;

before(async () => {
  process.env.BASE_PATH = "/ai-workflow-course/";
  buildModule = await import("../scripts/build.mjs");
  await buildModule.build();
  bundle = JSON.parse(await readFile(join(distRoot, "course-content.json"), "utf8"));
  manifest = JSON.parse(await readFile(join(distRoot, "manifest.webmanifest"), "utf8"));
  version = JSON.parse(await readFile(join(distRoot, "version.json"), "utf8"));
  appSource = await readFile(join(distRoot, "app.js"), "utf8");
  serviceWorkerSource = await readFile(join(distRoot, "sw.js"), "utf8");
  htmlSource = await readFile(join(distRoot, "index.html"), "utf8");
  cssSource = await readFile(join(distRoot, "styles.css"), "utf8");
});

test("course bundle contains the complete beginner path and twelve weeks", () => {
  const foundationFiles = bundle.documents.filter((document) =>
    /^foundations\/\d{2}_/.test(document.sourcePath),
  );
  const weekFiles = bundle.documents.filter((document) =>
    /^weeks\/WEEK_\d{2}\.md$/.test(document.sourcePath),
  );
  assert.equal(foundationFiles.length, 8);
  assert.deepEqual(
    weekFiles.map((document) => document.sourcePath),
    Array.from({ length: 12 }, (_value, index) => {
      return `weeks/WEEK_${String(index + 1).padStart(2, "0")}.md`;
    }),
  );
  assert.ok(
    bundle.documents.some(
      (document) => document.sourcePath === "foundations/GLOSSARY.md",
    ),
  );
  assert.ok(
    bundle.documents.some((document) => document.sourcePath === "COURSE_CHANGELOG.md"),
  );
});

test("every bundled course page has a unique id, title, source and content", () => {
  const ids = new Set();
  for (const document of bundle.documents) {
    assert.ok(document.id);
    assert.ok(document.title);
    assert.ok(document.sourcePath);
    assert.ok(document.markdown.length > 20);
    assert.equal(ids.has(document.id), false, `duplicate id ${document.id}`);
    ids.add(document.id);
  }
  for (const group of bundle.groups) {
    for (const id of group.documents) assert.ok(ids.has(id), `missing grouped id ${id}`);
  }
});

test("content hashes and build ids are stable for identical inputs", async () => {
  const secondBundle = await buildModule.createCourseBundle();
  assert.equal(secondBundle.course.contentHash, bundle.course.contentHash);
  const firstBuildId = version.buildId;
  await buildModule.build();
  const secondVersion = JSON.parse(
    await readFile(join(distRoot, "version.json"), "utf8"),
  );
  assert.equal(secondVersion.buildId, firstBuildId);
  assert.equal(secondVersion.contentHash, bundle.course.contentHash);
  assert.match(secondVersion.courseVersion, /^\d+\.\d+\.\d+$/);
});

test("GitHub Pages base path is used everywhere it must be", () => {
  assert.equal(manifest.start_url, "/ai-workflow-course/");
  assert.equal(manifest.scope, "/ai-workflow-course/");
  assert.equal(manifest.id, "/ai-workflow-course/");
  assert.match(htmlSource, /href="\/ai-workflow-course\/manifest\.webmanifest"/);
  assert.match(htmlSource, /src="\/ai-workflow-course\/app\.js"/);
  assert.match(serviceWorkerSource, /const BASE_PATH = "\/ai-workflow-course\/"/);
  for (const source of [htmlSource, appSource, serviceWorkerSource, cssSource]) {
    assert.equal(source.includes("__BASE_PATH__"), false);
    assert.equal(source.includes("__BUILD_ID__"), false);
  }
});

test("service worker preserves a learner-controlled waiting update", () => {
  const installHandler = serviceWorkerSource.match(
    /self\.addEventListener\("install"[\s\S]+?\n}\);/,
  )?.[0];
  assert.ok(installHandler);
  assert.match(installHandler, /cache: "reload"/);
  assert.doesNotMatch(installHandler, /skipWaiting/);
  assert.match(serviceWorkerSource, /type === "SKIP_WAITING"/);
  assert.match(serviceWorkerSource, /self\.skipWaiting\(\)/);
  assert.match(serviceWorkerSource, /caches\.delete/);
  assert.match(serviceWorkerSource, /const cache = await caches\.open\(CACHE_NAME\)/);
  assert.match(serviceWorkerSource, /request\.mode === "navigate"/);
  assert.match(serviceWorkerSource, /course-content\.json/);
});

test("app checks on startup, focus, foreground return and manual action", () => {
  assert.match(appSource, /updateViaCache: "none"/);
  assert.match(appSource, /serviceWorkerRegistration\.update\(\)/);
  assert.match(appSource, /addEventListener\("updatefound"/);
  assert.match(appSource, /addEventListener\("controllerchange"/);
  assert.match(appSource, /addEventListener\("focus"/);
  assert.match(appSource, /visibilitychange/);
  assert.match(appSource, /update-button/);
  assert.match(appSource, /postMessage\(\{ type: "SKIP_WAITING" \}\)/);
  assert.match(appSource, /pendingUpdateWorker/);
  assert.match(appSource, /reloadingForUpdate/);
});

test("install metadata and generated PNG icons are valid", async () => {
  assert.equal(manifest.display, "standalone");
  assert.equal(manifest.icons.some((icon) => icon.sizes === "192x192"), true);
  assert.equal(manifest.icons.some((icon) => icon.sizes === "512x512"), true);
  assert.equal(
    manifest.icons.some((icon) => String(icon.purpose).includes("maskable")),
    true,
  );
  for (const file of [
    "icon-192.png",
    "icon-512.png",
    "icon-maskable-512.png",
    "apple-touch-icon.png",
  ]) {
    const bytes = await readFile(join(distRoot, "icons", file));
    assert.deepEqual([...bytes.subarray(0, 8)], [137, 80, 78, 71, 13, 10, 26, 10]);
    assert.ok(bytes.length > 500, `${file} is unexpectedly small`);
  }
});

test("mobile and accessibility essentials are present", () => {
  assert.match(htmlSource, /class="skip-link"/);
  assert.match(htmlSource, /viewport-fit=cover/);
  assert.match(htmlSource, /apple-mobile-web-app-capable/);
  assert.match(htmlSource, /aria-live="polite"/);
  assert.match(htmlSource, /aria-label="Check for course updates"/);
  assert.match(htmlSource, /aria-label="Search the course"/);
  assert.match(htmlSource, /id="update-banner"/);
  assert.match(htmlSource, /id="install-dialog"/);
  assert.match(htmlSource, /id="sidebar-close-button"/);
  assert.match(htmlSource, /role="progressbar"/);
  assert.match(htmlSource, /aria-valuemin="0"/);
  assert.match(htmlSource, /aria-valuemax="100"/);
  assert.doesNotMatch(htmlSource, /class="progress-track"\s+aria-hidden="true"/);
  assert.match(htmlSource, /id="search-summary" role="status" aria-live="polite"/);
  assert.match(appSource, /setAttribute\("aria-valuenow"/);
  assert.match(appSource, /setAttribute\("aria-valuetext"/);
  assert.match(appSource, /trapSidebarFocus/);
  assert.match(appSource, /focus\(\{ preventScroll: true \}\)/);
  assert.match(cssSource, /min-height: 44px/);
  assert.match(cssSource, /\.brand\s*\{[\s\S]+?min-height: 44px/);
  assert.match(cssSource, /\.copy-code[\s\S]+?min-height: 44px/);
  assert.match(cssSource, /input\[type="range"\][\s\S]+?min-height: 44px/);
  assert.match(cssSource, /env\(safe-area-inset-bottom/);
  assert.match(cssSource, /@media \(max-width: 920px\)/);
  assert.doesNotMatch(cssSource, /width:\s*[4-9]\d{2,}px;\s*\/\* mobile/);
});

test("visual refresh stays purposeful, offline and theme-safe", () => {
  assert.match(appSource, /class="workflow-preview"/);
  for (const label of [
    "Source documents",
    "Evidence-linked facts",
    "Human review",
    "Approved memo",
  ]) {
    assert.match(appSource, new RegExp(label));
  }
  assert.match(appSource, /class="progress-ring"/);
  assert.match(appSource, /Foundation \$\{Number/);
  assert.match(appSource, /Core lesson \$\{corePosition \+ 1\}/);
  assert.match(htmlSource, /<svg class="ui-icon"/);
  assert.match(htmlSource, /aria-hidden="true" focusable="false"/);
  assert.doesNotMatch(htmlSource, /fonts\.(googleapis|gstatic)\.com/);
  assert.doesNotMatch(htmlSource, /<img[^>]+src="https?:/);
  assert.match(cssSource, /prefers-reduced-motion: reduce/);
  assert.match(cssSource, /-webkit-backdrop-filter/);
  assert.match(cssSource, /:root\[data-theme="dark"\] \.button:not\(\.button-quiet\)/);
  assert.doesNotMatch(cssSource, /:root\[data-theme="dark"\] \.button\s*\{/);
});

test("local progress survives course updates and reset is confirmed", () => {
  assert.match(appSource, /localStorage\.setItem\(STORAGE_KEY/);
  assert.match(appSource, /completed:/);
  assert.match(appSource, /notes:/);
  assert.match(appSource, /lastDocument:/);
  assert.match(appSource, /window\.confirm\(/);
  assert.doesNotMatch(serviceWorkerSource, /localStorage/);
});

test("built JavaScript is syntactically valid and required artifacts exist", async () => {
  for (const file of ["app.js", "sw.js"]) {
    execFileSync(nodeExecutable, ["--check", join(distRoot, file)], {
      stdio: "pipe",
    });
  }
  for (const file of [
    "index.html",
    "app.js",
    "styles.css",
    "course-content.json",
    "manifest.webmanifest",
    "sw.js",
    "version.json",
    ".nojekyll",
  ]) {
    assert.ok((await stat(join(distRoot, file))).isFile(), `${file} missing`);
  }
});

test("base-path normalisation rejects accidental missing slashes", () => {
  assert.equal(buildModule.normaliseBasePath("ai-workflow-course"), "/ai-workflow-course/");
  assert.equal(buildModule.normaliseBasePath("/ai-workflow-course"), "/ai-workflow-course/");
  assert.equal(buildModule.normaliseBasePath("/ai-workflow-course/"), "/ai-workflow-course/");
  assert.equal(buildModule.normaliseBasePath(""), "/");
});
