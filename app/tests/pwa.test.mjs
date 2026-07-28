import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFile, stat } from "node:fs/promises";
import { join, resolve } from "node:path";
import { before, test } from "node:test";
import { fileURLToPath } from "node:url";
import { renderMarkdown } from "../src/markdown.js";

const appRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const courseRoot = resolve(appRoot, "..");
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

test("schema-v2 bundle contains nine foundations and nine implementation modules", () => {
  assert.equal(bundle.schemaVersion, 2);
  assert.equal(bundle.program.id, "controlled-ai-workflow-consultant-path");
  assert.equal(bundle.course.id, "course-1-controlled-ai-workflow-foundations");
  const foundationFiles = bundle.documents.filter(
    (document) => document.group === "foundations",
  );
  const moduleFiles = bundle.documents.filter(
    (document) => document.group === "modules",
  );
  assert.equal(foundationFiles.length, 9);
  assert.deepEqual(
    foundationFiles.map((document) => document.sourcePath),
    [
      "foundations/01_FILES_AND_TEXT.md",
      "foundations/02_COMMAND_LINE_SURVIVAL.md",
      "foundations/03_CODE_AND_PYTHON.md",
      "foundations/04_WEB_APIS_AND_JSON.md",
      "foundations/05_GIT_AND_SAFE_CHANGES.md",
      "foundations/06_SPREADSHEETS_CSV_AND_DATA_QUALITY.md",
      "foundations/07_AI_AND_CONTROLLED_WORKFLOWS.md",
      "foundations/08_SAFE_AI_ASSISTED_BUILDING.md",
      "foundations/09_WORKFLOW_TOOLS_AND_DATA_STORES.md",
    ],
  );
  assert.deepEqual(
    moduleFiles.map((document) => document.sourcePath),
    Array.from({ length: 9 }, (_value, index) => {
      return `modules/MODULE_${String(index + 1).padStart(2, "0")}.md`;
    }),
  );
  assert.equal(bundle.course.foundationCount, 9);
  assert.equal(bundle.course.moduleCount, 9);
  assert.equal(bundle.course.coreLessonCount, 18);
  assert.ok(
    bundle.documents.some((document) => document.sourcePath === "COURSE_CHANGELOG.md"),
  );
});

test("every bundled course page has stable revisioned metadata and content", () => {
  const ids = new Set();
  const aliases = new Set();
  const careerCourseIds = new Set(bundle.career.courses.map((course) => course.id));
  for (const document of bundle.documents) {
    assert.match(document.id, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
    assert.match(document.revision, /^\d{4}-\d{2}-\d{2}$/);
    assert.ok(document.title);
    assert.ok(document.sourcePath);
    assert.ok(document.markdown.length > 20);
    assert.ok(
      careerCourseIds.has(document.courseId),
      `unknown courseId ${document.courseId} on ${document.id}`,
    );
    assert.equal(typeof document.core, "boolean");
    assert.equal(ids.has(document.id), false, `duplicate id ${document.id}`);
    ids.add(document.id);
    for (const alias of document.legacyIds) {
      assert.equal(aliases.has(alias), false, `duplicate legacy id ${alias}`);
      aliases.add(alias);
    }
  }
  for (const id of ids) assert.equal(aliases.has(id), false, `id also used as alias ${id}`);
  for (const group of bundle.groups) {
    for (const id of group.documents) assert.ok(ids.has(id), `missing grouped id ${id}`);
  }
});

test("optional Course 4 capstone is bundled without changing the Course 1 contract", () => {
  const expectedCoreIds = [
    "course-1-foundation-01",
    "course-1-foundation-02",
    "course-1-foundation-03",
    "course-1-foundation-04",
    "course-1-foundation-05",
    "course-1-foundation-06",
    "course-1-foundation-07",
    "course-1-foundation-08",
    "course-1-foundation-09",
    "course-1-module-01",
    "course-1-module-02",
    "course-1-module-03",
    "course-1-module-04",
    "course-1-module-05",
    "course-1-module-06",
    "course-1-module-07",
    "course-1-module-08",
    "course-1-module-09",
  ];
  const expectedLearningSequenceIds = [
    "course-1-readiness-check",
    "course-1-foundation-01",
    "course-1-foundation-02",
    "course-1-beginner-software-check",
    "course-1-windows-setup",
    "course-1-foundation-03",
    "course-1-foundation-04",
    "course-1-foundation-05",
    "course-1-foundation-06",
    "course-1-foundation-07",
    "course-1-foundation-08",
    "course-1-foundation-09",
    "course-1-module-01",
    "course-1-module-02",
    "course-1-module-03",
    "course-1-module-04",
    "course-1-module-05",
    "course-1-module-06",
    "course-1-module-07",
    "course-1-module-08",
    "course-1-module-09",
  ];
  const expectedCapstoneDocuments = [
    ["course-4-capstone-overview", "advanced_capstone/README.md"],
    [
      "course-4-capstone-readiness-and-cost-gate",
      "advanced_capstone/00_READINESS_COST_GATE.md",
    ],
    ["course-4-capstone-local-baseline", "advanced_capstone/01_LOCAL_BASELINE.md"],
    [
      "course-4-capstone-document-ai-eu",
      "advanced_capstone/02_SOURCE_INTEGRITY_DOCUMENT_AI.md",
    ],
    [
      "course-4-capstone-evidence-linked-extraction",
      "advanced_capstone/03_EVIDENCE_LINKED_EXTRACTION.md",
    ],
    [
      "course-4-capstone-vertex-gemini-eu",
      "advanced_capstone/04_GEMINI_SUMMARIES_ACTIONS.md",
    ],
    [
      "course-4-capstone-human-approval-and-exports",
      "advanced_capstone/05_HUMAN_APPROVAL_EXPORTS.md",
    ],
    [
      "course-4-capstone-tests-and-evaluation",
      "advanced_capstone/06_TESTS_AND_EVALUATION.md",
    ],
    [
      "course-4-capstone-cloud-run-deployment",
      "advanced_capstone/07_CLOUD_RUN_DEPLOYMENT.md",
    ],
    [
      "course-4-capstone-live-validation",
      "advanced_capstone/08_LIVE_VALIDATION.md",
    ],
    ["course-4-capstone-teardown", "advanced_capstone/09_TEARDOWN.md"],
  ];
  const coreIds = bundle.documents
    .filter((document) => document.core)
    .map((document) => document.id);
  const capstoneGroup = bundle.groups.find(
    (group) => group.id === "course-4-capstone",
  );
  const capstoneDocuments = expectedCapstoneDocuments.map(([id]) => {
    return bundle.documents.find((document) => document.id === id);
  });

  assert.equal(bundle.course.coreLessonCount, 18);
  assert.deepEqual(coreIds, expectedCoreIds);
  assert.deepEqual(bundle.course.learningSequenceIds, expectedLearningSequenceIds);
  assert.ok(capstoneGroup);
  assert.equal(capstoneGroup.core, false);
  assert.equal(capstoneGroup.kind, "advanced");
  assert.deepEqual(capstoneGroup.documents, expectedCapstoneDocuments.map(([id]) => id));
  assert.deepEqual(
    capstoneDocuments.map((document) => [document?.id, document?.sourcePath]),
    expectedCapstoneDocuments,
  );
  assert.equal(
    capstoneDocuments.every(
      (document) =>
        document?.courseId === "course-4-controlled-document-ai-systems" &&
        document.core === false,
    ),
    true,
  );
  assert.equal(
    expectedCapstoneDocuments.some(([id]) =>
      bundle.course.learningSequenceIds.includes(id),
    ),
    false,
  );
  assert.match(
    appSource,
    /courseDocument\.courseId === courseBundle\.course\.id/,
  );
  assert.match(appSource, /does not affect Course 1 progress/);
  assert.match(appSource, /Mark page complete/);
  assert.match(
    appSource,
    /courseDocument\.core \|\| courseDocument\.group === "course-4-capstone"/,
  );
  assert.match(cssSource, /\.reader-meta \.reader-course-boundary/);
});

test("content hashes and build ids are stable for identical inputs", async () => {
  const curriculum = JSON.parse(
    await readFile(join(courseRoot, "curriculum.json"), "utf8"),
  );
  const digestInput = [
    JSON.stringify(curriculum),
    bundle.documents
      .map((document) => `${document.sourcePath}\n${document.markdown}`)
      .join("\n---COURSE-DOCUMENT---\n"),
  ].join("\n---CURRICULUM-METADATA---\n");
  const expectedHash = createHash("sha256").update(digestInput).digest("hex");
  assert.equal(bundle.course.contentHash, expectedHash);
  const secondBundle = await buildModule.createCourseBundle();
  assert.equal(secondBundle.course.contentHash, bundle.course.contentHash);
  const firstBuildId = version.buildId;
  await buildModule.build();
  const secondVersion = JSON.parse(
    await readFile(join(distRoot, "version.json"), "utf8"),
  );
  assert.equal(secondVersion.buildId, firstBuildId);
  assert.equal(secondVersion.contentHash, bundle.course.contentHash);
  assert.equal(secondVersion.bundleSchemaVersion, 2);
  assert.equal(secondVersion.programId, bundle.program.id);
  assert.equal(secondVersion.courseId, bundle.course.id);
  assert.match(secondVersion.courseVersion, /^\d+\.\d+\.\d+$/);
});

test("build ids also change when the build and generated-asset logic changes", () => {
  const inputs = {
    contentHash: "content-hash",
    sourceAssets: [["app.js", "application source"]],
    buildScriptSource: "manifest and icon logic version one",
    basePath: "/ai-workflow-course/",
  };
  const first = buildModule.createBuildId(inputs);
  const repeated = buildModule.createBuildId(inputs);
  const changed = buildModule.createBuildId({
    ...inputs,
    buildScriptSource: "manifest and icon logic version two",
  });
  assert.equal(repeated, first);
  assert.notEqual(changed, first);
  assert.match(first, /^[a-f0-9]{12}$/);
});

test("career metadata separates the current course from the later consultant path", () => {
  assert.match(
    bundle.career.targetRole,
    /Small and Medium-sized Enterprises \(SMEs\)/,
  );
  assert.deepEqual(
    bundle.career.courses.map((course) => course.sequence),
    [1, 2, 3, 4, 5, 6],
  );
  assert.equal(bundle.career.courses[0].id, bundle.course.id);
  assert.deepEqual(
    bundle.career.courses.map((course) => course.status),
    [
      "current",
      "proposed",
      "proposed",
      "prototype-capstone-available",
      "proposed",
      "proposed",
    ],
  );
  assert.equal(
    bundle.career.courses[3].prototypeDocumentId,
    "course-4-capstone-overview",
  );
  assert.equal(
    bundle.career.optionalSpecializations.some(
      (specialization) =>
        specialization.id === "specialization-quality-document-operations",
    ),
    true,
  );
  assert.match(bundle.course.capstone.title, /SME Operations Exception Assistant/);
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
  assert.match(serviceWorkerSource, /markdown\.js/);
});

test("Markdown lists keep wrapped lines inside their list items", () => {
  assert.match(appSource, /from "\.\/markdown\.js"/);
  assert.doesNotMatch(appSource, /function renderMarkdown\(/);

  const rendered = renderMarkdown(`## What you need before starting

- A Windows computer on which you are allowed to install software.
- A normal text editor. Visual Studio Code is recommended, but Notepad is
  sufficient for the first two chapters.
- The supplied synthetic course files.
- Willingness to stop when you do not understand a command or when observed
  output differs from the lesson.`);

  const unorderedLists = rendered.match(/<ul>/g) || [];
  const listItems = rendered.match(/<li(?:\s|>)/g) || [];
  assert.equal(unorderedLists.length, 1);
  assert.equal(listItems.length, 4);
  assert.match(
    rendered,
    /<li>A normal text editor[^<]*Notepad is sufficient for the first two chapters\.<\/li>/,
  );
  assert.match(
    rendered,
    /<li>Willingness to stop[^<]*observed output differs from the lesson\.<\/li>/,
  );
  assert.doesNotMatch(rendered, /<p>(?:sufficient|output differs)/);

  let wrappedItemsChecked = 0;
  for (const courseDocument of bundle.documents) {
    const lines = courseDocument.markdown.replace(/\r\n?/g, "\n").split("\n");
    let fenced = false;
    let sourceListItems = 0;
    for (let index = 0; index < lines.length; index += 1) {
      if (/^\s*```/.test(lines[index])) {
        fenced = !fenced;
        continue;
      }
      if (fenced) continue;
      const marker = lines[index].match(/^([ \t]*)(?:[-*+]|\d+\.)\s+(.+)$/);
      if (!marker) continue;
      sourceListItems += 1;
      const baseIndent = marker[1].replaceAll("\t", "    ").length;
      const continuation = [];
      for (let lookahead = index + 1; lookahead < lines.length; lookahead += 1) {
        const next = lines[lookahead];
        if (!next.trim() || /^([ \t]*)(?:[-*+]|\d+\.)\s+/.test(next)) break;
        const indent = (next.match(/^[ \t]*/)?.[0] || "")
          .replaceAll("\t", "    ").length;
        if (indent <= baseIndent || /^```/.test(next.trim())) break;
        continuation.push(next);
      }
      if (!continuation.length) continue;
      wrappedItemsChecked += 1;
      const isolated = renderMarkdown([lines[index], ...continuation].join("\n"));
      assert.equal(
        (isolated.match(/<li(?:\s|>)/g) || []).length,
        1,
        `${courseDocument.sourcePath}:${index + 1} did not remain one list item`,
      );
      assert.doesNotMatch(
        isolated,
        /<p>/,
        `${courseDocument.sourcePath}:${index + 1} detached a continuation`,
      );
    }
    const fullPage = renderMarkdown(courseDocument.markdown);
    assert.equal(
      (fullPage.match(/<li(?:\s|>)/g) || []).length,
      sourceListItems,
      `${courseDocument.sourcePath} changed the number of list items`,
    );
    assert.doesNotMatch(fullPage, /\u0000|>CODE\d+</);
  }
  assert.ok(wrappedItemsChecked >= 87);
});

test("Markdown lists preserve nesting, numbering, and task hanging indents", () => {
  const nested = renderMarkdown(`6. Switch on result:
   - accepted;
   - permanent rejection;
   - transient failure;
   - unexpected response.
7. Wait and retry.
8. Success log.
9. Manual-failure queue.`);
  assert.match(
    nested,
    /^<ol start="6"><li>Switch on result:<ul><li>accepted;<\/li><li>permanent rejection;<\/li><li>transient failure;<\/li><li>unexpected response\.<\/li><\/ul><\/li><li>Wait and retry\.<\/li><li>Success log\.<\/li><li>Manual-failure queue\.<\/li><\/ol>$/,
  );

  const continued = renderMarkdown(`9. Boundary reading.
10. Second reading.`);
  assert.match(continued, /^<ol start="9">/);

  const task = renderMarkdown(`- [ ] I can recognise Markdown, JSON, YAML, and
  environment files.`);
  assert.match(task, /class="markdown-task-item"/);
  assert.match(
    task,
    /<span class="markdown-task-text">I can recognise Markdown, JSON, YAML, and environment files\.<\/span>/,
  );
  assert.doesNotMatch(task, /<p>environment files/);
});

test("Markdown list boundaries stay safe around blocks and inline code links", () => {
  const rendered = renderMarkdown(`- Safe item
  <script>alert("no")</script>

\`\`\`json
{"ok": true}
\`\`\`

| Field | Value |
| --- | --- |
| state | received |`);

  assert.match(
    rendered,
    /<li>Safe item &lt;script&gt;alert\(&quot;no&quot;\)&lt;\/script&gt;<\/li>/,
  );
  assert.equal((rendered.match(/class="code-block"/g) || []).length, 1);
  assert.equal((rendered.match(/class="table-wrap"/g) || []).length, 1);

  const linkedCode = renderMarkdown(
    "1. [`01_FILES_AND_TEXT.md`](01_FILES_AND_TEXT.md) — start here.",
  );
  assert.match(
    linkedCode,
    /<a href="01_FILES_AND_TEXT\.md"><code>01_FILES_AND_TEXT\.md<\/code><\/a>/,
  );
  assert.doesNotMatch(linkedCode, />CODE\d+</);
});

test("CommonMark secure URL autolinks render as safe external links", () => {
  const rendered = renderMarkdown(
    "Download it from <https://example.com/tool?channel=stable&lang=en>.",
  );
  assert.match(
    rendered,
    /<a href="https:\/\/example\.com\/tool\?channel=stable&amp;lang=en" target="_blank" rel="noopener noreferrer">https:\/\/example\.com\/tool\?channel=stable&amp;lang=en<\/a>/,
  );
  assert.match(
    renderMarkdown("Do not open <javascript:alert(1)>."),
    /&lt;javascript:alert\(1\)&gt;/,
  );
  assert.doesNotMatch(renderMarkdown("<http://example.com>"), /<a href=/);
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
  assert.match(
    cssSource,
    /\.skip-link\s*\{[\s\S]+?translateY\(calc\(-100% - var\(--safe-top\) - 1rem\)\)/,
  );
  assert.match(cssSource, /\.skip-link:focus\s*\{/);
  assert.match(
    appSource,
    /renderHome\(\);[\s\S]+?const resetRouteScroll = \(\) => window\.scrollTo\(\{ top: 0, behavior: "instant" \}\);[\s\S]+?resetRouteScroll\(\);[\s\S]+?window\.setTimeout\(resetRouteScroll, 0\);[\s\S]+?if \(pendingRouteFocus\)/,
  );
  assert.match(
    appSource,
    /querySelector\("\.brand"\)[\s\S]+?preventDefault\(\)[\s\S]+?navigate\("home"\)/,
  );
  assert.match(appSource, /focus\(\{ preventScroll: true \}\)/);
  assert.match(cssSource, /min-height: 44px/);
  assert.match(cssSource, /\.brand\s*\{[\s\S]+?min-height: 44px/);
  assert.match(cssSource, /\.copy-code[\s\S]+?min-height: 44px/);
  assert.match(cssSource, /input\[type="range"\][\s\S]+?min-height: 44px/);
  assert.match(cssSource, /env\(safe-area-inset-bottom/);
  assert.match(cssSource, /@media \(max-width: 920px\)/);
  assert.doesNotMatch(cssSource, /min-width:\s*320px/);
  assert.match(
    cssSource,
    /@media \(max-width: 920px\)[\s\S]+?\.bottom-nav\s*\{[\s\S]+?bottom: 0;[\s\S]+?min-height: calc\(4\.45rem \+ var\(--safe-bottom\)\);[\s\S]+?background: var\(--paper-raised\);/,
  );
  const bottomNavigation = htmlSource.match(
    /<nav class="bottom-nav"[\s\S]+?<\/nav>/,
  )?.[0];
  assert.ok(bottomNavigation);
  assert.equal((bottomNavigation.match(/<button /g) || []).length, 5);
  assert.match(bottomNavigation, /data-route="career"[\s\S]+?<span>Career<\/span>/);
  assert.match(cssSource, /grid-template-columns: repeat\(5, 1fr\)/);
  assert.doesNotMatch(cssSource, /width:\s*[4-9]\d{2,}px;\s*\/\* mobile/);
});

test("learner notes are captured before navigation and report real storage results", () => {
  const captureSource = appSource.match(
    /function captureNoteInState\(documentId, noteValue\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(captureSource);
  const noteState = { notes: {} };
  const captureNoteInState = Function(
    "state",
    "noteStorageDirty",
    `${captureSource}; return captureNoteInState;`,
  )(noteState, false);
  captureNoteInState("lesson-one", "Keep this note");
  assert.equal(noteState.notes["lesson-one"], "Keep this note");
  captureNoteInState("lesson-two", "x".repeat(50010));
  assert.equal(noteState.notes["lesson-two"].length, 50000);
  captureNoteInState("lesson-one", "   ");
  assert.equal("lesson-one" in noteState.notes, false);

  const saveSource = appSource.match(
    /function saveState\(\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(saveSource);
  const messages = [];
  const makeSaveState = (storage) =>
    Function(
      "localStorage",
      "STORAGE_KEY",
      "state",
      "showToast",
      "noteStorageDirty",
      `${saveSource}; return saveState;`,
    )(
      storage,
      "course-state",
      noteState,
      (message) => messages.push(message),
      true,
    );
  assert.equal(makeSaveState({ setItem() {} })(), true);
  assert.equal(
    makeSaveState({
      setItem() {
        throw new Error("storage full");
      },
    })(),
    false,
  );
  assert.match(messages.at(-1), /could not be saved/);

  const wireEventsSource = appSource.match(
    /function wireEvents\(\) \{[\s\S]+?^}/m,
  )?.[0];
  assert.ok(wireEventsSource);
  assert.ok(
    wireEventsSource.indexOf("captureNoteInState(documentId, event.currentTarget.value)") <
      wireEventsSource.indexOf("window.setTimeout(persistPendingNote, 450)"),
  );
  assert.match(wireEventsSource, /addEventListener\("pagehide", flushPendingNote\)/);
  assert.match(
    wireEventsSource,
    /document\.visibilityState === "hidden"\) flushPendingNote\(\)/,
  );
  const persistSource = appSource.match(
    /function persistPendingNote\(\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(persistSource);
  assert.doesNotMatch(persistSource, /currentDocument|learner-note/);
  assert.match(persistSource, /saved \? "Saved locally" : "Not saved on this device"/);
  assert.match(appSource, /function navigate\(route\) \{\s+flushPendingNote\(\)/);
  assert.match(appSource, /function toggleCompleted\(\) \{[\s\S]+?flushPendingNote\(\)/);
  assert.match(appSource, /noteTimer === null && !noteStorageDirty/);
  assert.doesNotMatch(appSource, /textContent = "Saved locally"/);
  assert.match(htmlSource, /maxlength="50000"/);
  assert.match(htmlSource, /<label id="notes-title" for="learner-note">/);
  assert.match(htmlSource, /aria-labelledby="notes-title"/);
  assert.doesNotMatch(htmlSource, /id="note-save-status"[^>]*>Saved locally/);
  assert.match(cssSource, /\.save-status\.save-error/);
});

test("actionable sequence includes onboarding pages and ignores arbitrary references", () => {
  const foundationTwoIndex = bundle.course.learningSequenceIds.indexOf(
    "course-1-foundation-02",
  );
  assert.ok(foundationTwoIndex >= 0);
  assert.deepEqual(
    bundle.course.learningSequenceIds.slice(
      foundationTwoIndex,
      foundationTwoIndex + 4,
    ),
    [
      "course-1-foundation-02",
      "course-1-beginner-software-check",
      "course-1-windows-setup",
      "course-1-foundation-03",
    ],
  );

  const helperSource = appSource.match(
    /function resumeDocument\(\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(helperSource);
  const documents = [
    { id: "readiness", core: false, group: "start" },
    { id: "foundation-one", core: true },
    { id: "foundation-two", core: true },
    { id: "software-check", core: false, group: "start" },
    { id: "windows-setup", core: false, group: "start" },
    { id: "foundation-three", core: true },
    { id: "reference-page", core: false, group: "reference" },
  ];
  const byId = new Map(documents.map((document) => [document.id, document]));
  const sequence = documents.slice(0, 6);
  const makeResume = (lastDocument, completedIds) =>
    Function(
      "learningSequenceDocuments",
      "documentById",
      "state",
      "isDocumentComplete",
      `${helperSource}; return resumeDocument;`,
    )(
      () => sequence,
      byId,
      { lastDocument },
      (document) => completedIds.has(document.id),
    );
  const completedThroughFoundationTwo = new Set([
    "readiness",
    "foundation-one",
    "foundation-two",
  ]);
  assert.equal(
    makeResume("reference-page", completedThroughFoundationTwo)().id,
    "software-check",
  );
  assert.equal(
    makeResume("foundation-two", completedThroughFoundationTwo)().id,
    "software-check",
  );
  assert.equal(
    makeResume("windows-setup", completedThroughFoundationTwo)().id,
    "windows-setup",
  );

  const pagerSource = appSource.match(
    /function pagerDocumentsFor\(courseDocument\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(pagerSource);
  const pagerDocumentsFor = Function(
    "learningSequenceDocuments",
    "courseBundle",
    "documentById",
    `${pagerSource}; return pagerDocumentsFor;`,
  )(
    () => sequence,
    {
      groups: [
        { id: "start", documents: ["readiness", "software-check", "windows-setup"] },
        { id: "reference", documents: ["reference-page"] },
      ],
    },
    byId,
  );
  const pager = pagerDocumentsFor(byId.get("foundation-two"));
  const pagerIndex = pager.findIndex(
    (courseDocument) => courseDocument.id === "foundation-two",
  );
  assert.deepEqual(
    pager.slice(pagerIndex, pagerIndex + 4).map((courseDocument) => courseDocument.id),
    [
      "foundation-two",
      "software-check",
      "windows-setup",
      "foundation-three",
    ],
  );
  assert.deepEqual(
    pagerDocumentsFor(byId.get("reference-page")).map(
      (courseDocument) => courseDocument.id,
    ),
    ["reference-page"],
  );
});

test("course navigation waits for content and announces state and route focus", () => {
  const initialiseSource = appSource.match(
    /async function initialise\(\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(initialiseSource);
  assert.ok(
    initialiseSource.indexOf("wireEvents();") >
      initialiseSource.indexOf("courseBundle = await response.json();"),
  );
  assert.match(htmlSource, /id="app-shell" aria-busy="true"/);
  assert.match(htmlSource, /id="menu-button"[^>]+disabled/);
  assert.match(appSource, /function setCourseShellReady\(\)/);
  assert.match(appSource, /querySelectorAll\("\[data-route\]"\)/);
  assert.match(appSource, /class="sr-only nav-document-status"/);
  assert.match(appSource, /"Completed"[\s\S]+?"Review again"[\s\S]+?"Not completed"/);
  assert.match(
    appSource,
    /const activeView = Object\.values\(views\)\.find[\s\S]+?querySelector\("h1"\)/,
  );
  assert.match(appSource, /heading\.setAttribute\("tabindex", "-1"\)/);
  assert.doesNotMatch(appSource, /querySelector\("#main-content"\)\.focus/);
});

test("effort and installation language reflect real practice and all devices", () => {
  assert.match(appSource, /total course hours/);
  assert.match(appSource, /minutes reading · allow extra practice time/);
  assert.doesNotMatch(appSource, /\} minutes<\/span>/);
  assert.match(htmlSource, /Install Course 1 on this device/);
  assert.match(htmlSource, /Desktop computer or Android device/);
  assert.match(htmlSource, /iPhone or iPad/);
  assert.match(htmlSource, /Install app/);
  assert.match(htmlSource, /Add to Home Screen/);
  assert.match(cssSource, /\.install-platform/);
});

test("visual refresh stays purposeful, offline and theme-safe", () => {
  assert.match(appSource, /class="workflow-preview"/);
  for (const label of [
    "Fictional operations data",
    "Problems found by fixed rules",
    "Evidence-linked AI summary",
    "Human review and action",
  ]) {
    assert.match(appSource, new RegExp(label));
  }
  assert.match(appSource, /class="progress-ring"/);
  assert.match(appSource, /courseDocument\.kind === "foundation"/);
  assert.match(appSource, /courseDocument\.kind === "module"/);
  assert.match(appSource, /Core lesson \$\{corePosition \+ 1\}/);
  assert.match(appSource, /class="module-card-grid"/);
  assert.match(appSource, /class="career-bridge"/);
  assert.match(htmlSource, /<svg class="ui-icon"/);
  assert.match(htmlSource, /aria-hidden="true" focusable="false"/);
  assert.doesNotMatch(htmlSource, /fonts\.(googleapis|gstatic)\.com/);
  assert.doesNotMatch(htmlSource, /<img[^>]+src="https?:/);
  assert.match(cssSource, /prefers-reduced-motion: reduce/);
  assert.match(cssSource, /-webkit-backdrop-filter/);
  assert.match(cssSource, /:root\[data-theme="dark"\] \.button:not\(\.button-quiet\)/);
  assert.doesNotMatch(cssSource, /:root\[data-theme="dark"\] \.button\s*\{/);
});

test("beginner practice contract is visible on home, core lessons, and Course 4 capstone pages", () => {
  for (const phase of [
    "Follow along",
    "Now recreate it",
    "Ask Codex",
    "Pass criteria",
  ]) {
    assert.match(appSource, new RegExp(phase));
  }
  assert.match(
    appSource,
    /Every practical lesson uses the same four steps/,
  );
  assert.match(appSource, /exact practice folder to inspect/);
  assert.match(
    appSource,
    /The check is read-only: Codex may report what it sees inside that folder/,
  );
  assert.match(appSource, /must not edit, move, or delete your files/);
  assert.match(
    appSource,
    /class="practice-contract practice-contract-home"[\s\S]+?practiceContractMarkup\(\)/,
  );
  assert.match(htmlSource, /id="practice-contract-reader"/);
  assert.match(
    appSource,
    /const showPracticeContract =[\s\S]+?courseDocument\.core \|\| courseDocument\.group === "course-4-capstone"/,
  );
  assert.match(appSource, /practiceContract\.hidden = !showPracticeContract/);
  assert.match(appSource, /if \(showPracticeContract\)/);
  assert.match(appSource, /practiceContractMarkup\(\{ compact: true \}\)/);
  assert.match(cssSource, /\.practice-contract-steps/);
  assert.match(
    cssSource,
    /\.practice-contract-reader \.practice-contract-steps\s*\{[\s\S]+?repeat\(2, minmax\(0, 1fr\)\)/,
  );
});

test("career view separates Course 1, the optional prototype, and proposed courses", () => {
  assert.match(htmlSource, /id="career-view"/);
  assert.match(
    htmlSource,
    /class="sidebar-link" type="button" data-route="career"/,
  );
  assert.match(appSource, /function renderCareer\(\)/);
  assert.match(appSource, /career\.courses/);
  assert.match(appSource, /career\.optionalSpecializations/);
  assert.match(appSource, /Course 1 is taught in full/);
  assert.match(appSource, /one optional advanced capstone prototype/);
  assert.match(appSource, /progressive web app \(PWA\)/);
  assert.match(
    appSource,
    /progressive web app \\\(PWA\\\)\/i\.test\(rawCareerSummary\)/,
  );
  assert.match(appSource, /data-career-action="course"/);
  assert.match(appSource, /data-career-action="prototype"/);
  assert.match(appSource, /Open the optional capstone/);
  assert.match(cssSource, /\.career-course-card\.current/);
  assert.match(cssSource, /\.career-course-card\.prototype/);
  assert.match(cssSource, /\.career-detail-grid/);
});

test("first visible abbreviations are expanded in beginner language", () => {
  assert.match(
    htmlSource,
    /<strong>Controlled artificial intelligence<\/strong>/,
  );
  assert.match(appSource, /add artificial intelligence \(AI\) only where it helps/);
  assert.match(
    appSource,
    /Artificial intelligence \(AI\) for small and medium-sized enterprises \(SMEs\)/,
  );
  assert.match(appSource, /progressive web app \(PWA\)/);
  assert.doesNotMatch(htmlSource, /<strong>Controlled AI Workflow<\/strong>/);
  assert.doesNotMatch(htmlSource, /Dutch SME consulting path/);
  assert.match(appSource, /build fixed, rule-based checks/);
  assert.match(appSource, /Made-up practice data only/);
  assert.match(appSource, /Made-up final practice project/);
  assert.match(appSource, /Problems found by fixed rules/);
  assert.match(
    appSource,
    /Cannot send or change anything outside the practice files/,
  );
  assert.match(appSource, /Research review date/);
  assert.match(htmlSource, /Application and reading settings/);
  assert.match(appSource, /different fictional names or data/);
  assert.match(
    appSource,
    /Codex, the artificial intelligence \(AI\) course assistant/,
  );
  assert.match(appSource, /About \$\{Math\.max[\s\S]+?\} minutes/);
  assert.match(htmlSource, />Escape<\/kbd>/);
  assert.match(htmlSource, /Safari<\/strong>, Apple’s web browser/);
  assert.match(htmlSource, /GitHub, the online service that hosts this course/);
  assert.doesNotMatch(appSource, /build deterministic checks/);
  assert.doesNotMatch(appSource, /Synthetic capstone/);
  assert.doesNotMatch(appSource, /Source currency/);
  assert.doesNotMatch(appSource, /browser with service workers/);
  assert.doesNotMatch(appSource, /A deployment is available/);
});

test("learning sequence and checkpoints use bundle metadata rather than old paths", () => {
  assert.match(
    appSource,
    /courseBundle\.documents\.filter\(\(courseDocument\) => courseDocument\.core\)/,
  );
  assert.match(appSource, /courseBundle\.course\.learningSequenceIds/);
  assert.match(
    appSource,
    /const nextDocuments = learningSequenceDocuments\(\)/,
  );
  assert.match(appSource, /const nextLesson = resumeDocument\(\)/);
  assert.match(appSource, /group\.documents\.indexOf\(courseDocument\.id\)/);
  assert.match(appSource, /courseDocument\.checkpoint/);
  assert.match(appSource, /candidate\.lessonId === courseDocument\.id/);
  assert.match(appSource, /const pagerDocuments = pagerDocumentsFor\(courseDocument\)/);
  assert.doesNotMatch(appSource, /weeks\/WEEK_07\.md/);
  assert.doesNotMatch(appSource, /sourcePath\.match\(\^foundations/);
});

test("schema-v1 progress migrates to stable revisioned lesson ids", () => {
  assert.match(appSource, /localStorage\.setItem\(STORAGE_KEY/);
  assert.match(appSource, /const STATE_SCHEMA_VERSION = 2/);
  assert.match(appSource, /parsed\.schemaVersion === 1/);
  assert.match(appSource, /function migrateSchemaV1\(legacy\)/);
  assert.match(appSource, /courseDocument\.legacyIds\.includes\(storedId\)/);
  assert.match(appSource, /completed:/);
  assert.match(appSource, /completionRevisions:/);
  assert.match(appSource, /notes:/);
  assert.match(appSource, /archivedLegacyNotes:/);
  assert.match(appSource, /lastDocument:/);
  assert.match(
    appSource,
    /state\.completionRevisions\[courseDocument\.id\] ===[\s\S]+?completionRevisionFor\(courseDocument\)/,
  );
  assert.match(appSource, /\[1, STATE_SCHEMA_VERSION\]\.includes/);
  assert.match(appSource, /window\.confirm\(/);
  assert.doesNotMatch(serviceWorkerSource, /localStorage/);
});

test("course practice revision reopens old completions without changing lesson dates", () => {
  assert.ok(Number.isInteger(bundle.course.practiceRevision));
  assert.ok(bundle.course.practiceRevision >= 2);
  const coreDocument = bundle.documents.find((document) => document.core);
  assert.ok(coreDocument);
  const helperSource = appSource.match(
    /function completionRevisionFor\(courseDocument\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(helperSource);
  const completionRevisionFor = Function(
    "courseBundle",
    `${helperSource}; return completionRevisionFor;`,
  )(bundle);
  const effectiveRevision = completionRevisionFor(coreDocument);
  assert.equal(
    effectiveRevision,
    `${coreDocument.revision}|practice:${bundle.course.practiceRevision}`,
  );
  assert.notEqual(effectiveRevision, coreDocument.revision);
  assert.match(coreDocument.revision, /^\d{4}-\d{2}-\d{2}$/);
  assert.match(
    appSource,
    /state\.completionRevisions\[courseDocument\.id\] !==[\s\S]+?completionRevisionFor\(courseDocument\)/,
  );
  assert.match(
    appSource,
    /\^\\d\{4\}-\\d\{2\}-\\d\{2\}\(\?:\\\|practice:\[1-9\]\\d\*\)\?\$/,
  );
  assert.match(appSource, /notes: parsed\.notes/);
  assert.match(appSource, /theme: \["system", "light", "dark"\]/);
});

test("built JavaScript is syntactically valid and required artifacts exist", async () => {
  for (const file of ["app.js", "markdown.js", "sw.js"]) {
    execFileSync(nodeExecutable, ["--check", join(distRoot, file)], {
      stdio: "pipe",
    });
  }
  for (const file of [
    "index.html",
    "app.js",
    "markdown.js",
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
