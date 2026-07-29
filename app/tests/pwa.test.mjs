import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFile, stat } from "node:fs/promises";
import { join, resolve } from "node:path";
import { before, test } from "node:test";
import { fileURLToPath } from "node:url";
import {
  renderMarkdown,
  stripLeadingDocumentTitle,
} from "../src/markdown.js";

const appRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const courseRoot = resolve(appRoot, "..");
const distRoot = join(appRoot, "dist");
const nodeExecutable = process.execPath;
let buildModule;
let bundle;
let manifest;
let version;
let packageMetadata;
let appSource;
let stateSource;
let bootstrapSource;
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
  packageMetadata = JSON.parse(
    await readFile(join(appRoot, "package.json"), "utf8"),
  );
  appSource = await readFile(join(distRoot, "app.js"), "utf8");
  stateSource = await readFile(join(distRoot, "state.js"), "utf8");
  bootstrapSource = await readFile(join(distRoot, "bootstrap.js"), "utf8");
  serviceWorkerSource = await readFile(join(distRoot, "sw.js"), "utf8");
  htmlSource = await readFile(join(distRoot, "index.html"), "utf8");
  cssSource = await readFile(join(distRoot, "styles.css"), "utf8");
});

test("schema-v2 bundle contains nine foundations and nine implementation modules", () => {
  assert.equal(bundle.schemaVersion, 2);
  assert.equal(bundle.program.id, "controlled-ai-workflow-consultant-path");
  assert.equal(bundle.course.id, "course-1-controlled-ai-workflow-foundations");
  assert.equal(packageMetadata.version, bundle.course.version);
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
  assert.equal(bundle.course.sourceVerifiedThrough, "2026-07-28");
  assert.equal(bundle.course.contentRevisionThrough, "2026-07-29");
  assert.equal(
    bundle.course.verifiedThrough,
    bundle.course.sourceVerifiedThrough,
  );
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
  assert.match(appSource, /does not affect Course 1 reading or practice records/);
  assert.match(appSource, /Mark page read/);
  assert.match(appSource, /courseOneDocuments\(\)/);
  assert.match(
    appSource,
    /\.filter\(\(courseDocument\) => belongsToCourseOne\(courseDocument\)\)/,
  );
  assert.match(cssSource, /\.reader-meta \.reader-course-boundary/);
});

test("Course 1 practice-hour metadata survives the build", () => {
  const coreDocuments = bundle.documents.filter((document) => document.core);
  assert.equal(coreDocuments.length, 18);
  for (const document of coreDocuments) {
    assert.ok(
      Number.isFinite(document.estimatedPracticeHours?.minimum),
      `${document.id} is missing a minimum practice estimate`,
    );
    assert.ok(
      Number.isFinite(document.estimatedPracticeHours?.maximum),
      `${document.id} is missing a maximum practice estimate`,
    );
    assert.ok(document.estimatedPracticeHours.minimum > 0);
    assert.ok(
      document.estimatedPracticeHours.maximum >=
        document.estimatedPracticeHours.minimum,
    );
  }
  for (const onboardingId of [
    "course-1-readiness-check",
    "course-1-beginner-software-check",
    "course-1-windows-setup",
  ]) {
    const onboarding = bundle.documents.find(
      (document) => document.id === onboardingId,
    );
    assert.ok(onboarding?.estimatedPracticeHours, `${onboardingId} lost its estimate`);
  }
  assert.match(
    String(buildModule.createCourseBundle),
    /estimatedPracticeHours:\s*documentMetadata\.estimatedPracticeHours \|\| null/,
  );
});

test("default Course 1 navigation and search exclude later-course lessons", () => {
  assert.match(
    appSource,
    /\.filter\(\(courseDocument\) => belongsToCourseOne\(courseDocument\)\)/,
  );
  assert.match(appSource, /if \(!groupDocuments\.length\) continue/);
  assert.match(appSource, /return courseOneDocuments\(\)/);
  assert.match(htmlSource, /Search Course 1/);
  assert.match(htmlSource, /Later-course prototypes are intentionally excluded/);

  const helperSource = appSource.match(
    /function searchDocuments\(query\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(helperSource);
  const courseOne = bundle.documents.filter(
    (document) => document.courseId === bundle.course.id,
  );
  const searchDocuments = Function(
    "courseBundle",
    "courseOneDocuments",
    `${helperSource}; return searchDocuments;`,
  )(bundle, () => courseOne);
  for (const query of ["cloud run", "teardown", "document ai"]) {
    assert.equal(
      searchDocuments(query).every(
        (result) => result.document.courseId === bundle.course.id,
      ),
      true,
    );
  }
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
  assert.equal(
    secondVersion.sourceVerifiedThrough,
    bundle.course.sourceVerifiedThrough,
  );
  assert.equal(
    secondVersion.contentRevisionThrough,
    bundle.course.contentRevisionThrough,
  );
  assert.equal(
    secondVersion.verifiedThrough,
    secondVersion.sourceVerifiedThrough,
  );
});

test("legacy schema-v2 curriculum dates migrate without changing source currency", async () => {
  const current = JSON.parse(
    await readFile(join(courseRoot, "curriculum.json"), "utf8"),
  );
  const legacy = structuredClone(current);
  legacy.schemaVersion = 2;
  delete legacy.course.sourceVerifiedThrough;
  delete legacy.course.contentRevisionThrough;
  const migrated = buildModule.normaliseCurriculumMetadata(legacy);

  assert.equal(migrated.schemaVersion, 3);
  assert.equal(migrated.course.sourceVerifiedThrough, "2026-07-28");
  assert.equal(migrated.course.contentRevisionThrough, "2026-07-29");
  assert.equal(
    migrated.course.verifiedThrough,
    migrated.course.sourceVerifiedThrough,
  );
  assert.equal(legacy.course.sourceVerifiedThrough, undefined);
});

test("build ids change with commit provenance and generated-asset logic", () => {
  const inputs = {
    contentHash: "content-hash",
    sourceAssets: [["app.js", "application source"]],
    buildScriptSource: "manifest and icon logic version one",
    basePath: "/ai-workflow-course/",
    commit: "1111111111111111111111111111111111111111",
  };
  const first = buildModule.createBuildId(inputs);
  const repeated = buildModule.createBuildId(inputs);
  const changed = buildModule.createBuildId({
    ...inputs,
    buildScriptSource: "manifest and icon logic version two",
  });
  const changedCommit = buildModule.createBuildId({
    ...inputs,
    commit: "2222222222222222222222222222222222222222",
  });
  assert.equal(repeated, first);
  assert.notEqual(changed, first);
  assert.notEqual(changedCommit, first);
  assert.match(first, /^[a-f0-9]{12}$/);
  assert.throws(
    () => buildModule.createBuildId({ ...inputs, commit: "" }),
    /commit provenance is required/,
  );
});

test("candidate provenance requires one clean full-commit source identity", () => {
  const commit = "1".repeat(40);
  assert.equal(
    buildModule.selectBuildProvenance({
      mode: "candidate",
      workflowCommit: commit,
      repositoryCommit: commit,
      repositoryClean: true,
    }),
    commit,
  );
  assert.equal(
    buildModule.selectBuildProvenance({
      mode: "development",
      workflowCommit: commit,
      repositoryCommit: commit,
      repositoryClean: false,
    }),
    "working-copy",
  );
  for (const candidate of [
    {
      mode: "candidate",
      workflowCommit: commit.slice(0, 12),
      repositoryCommit: commit,
      repositoryClean: true,
    },
    {
      mode: "candidate",
      workflowCommit: commit,
      repositoryCommit: "2".repeat(40),
      repositoryClean: true,
    },
    {
      mode: "candidate",
      workflowCommit: commit,
      repositoryCommit: commit,
      repositoryClean: false,
    },
  ]) {
    assert.throws(
      () => buildModule.selectBuildProvenance(candidate),
      /Candidate/,
    );
  }
  assert.throws(
    () =>
      buildModule.selectBuildProvenance({
        mode: "audit-ish",
        workflowCommit: commit,
        repositoryCommit: commit,
        repositoryClean: true,
      }),
    /COURSE1_BUILD_MODE/,
  );
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
  assert.equal(serviceWorkerSource.includes("__BUILD_PROVENANCE__"), false);
  assert.equal(serviceWorkerSource.includes("__ASSET_MANIFEST_SHA256__"), false);
});

test("service worker preserves a learner-controlled waiting update", () => {
  const installHandler = serviceWorkerSource.match(
    /self\.addEventListener\("install"[\s\S]+?\n}\);/,
  )?.[0];
  assert.ok(installHandler);
  assert.doesNotMatch(installHandler, /skipWaiting/);
  assert.doesNotMatch(installHandler, /startsWith\(CACHE_PREFIX\)/);
  assert.match(serviceWorkerSource, /cache = "reload"/);
  assert.match(serviceWorkerSource, /loadVerifiedNetworkManifest/);
  assert.match(serviceWorkerSource, /fetchVerifiedAsset/);
  assert.match(
    serviceWorkerSource,
    /CANDIDATE_CACHE_NAME =\s*\n?\s*`\$\{CACHE_PREFIX\}\$\{BUILD_ID\}-\$\{ASSET_MANIFEST_SHA256\}`/,
  );
  assert.match(
    serviceWorkerSource,
    /caches\.delete\(CANDIDATE_CACHE_NAME\)/,
  );
  assert.match(serviceWorkerSource, /type !== "SKIP_WAITING"/);
  assert.match(serviceWorkerSource, /self\.skipWaiting\(\)/);
  assert.match(serviceWorkerSource, /isLegacyExplicitAction/);
  assert.match(serviceWorkerSource, /isCurrentExplicitAction/);
  assert.match(serviceWorkerSource, /event\.source\?\.type !== "window"/);
  assert.match(
    serviceWorkerSource,
    /await validateCachedRelease\(CANDIDATE_CACHE_NAME\);\s+await self\.skipWaiting\(\)/,
  );
  assert.match(serviceWorkerSource, /\^\[a-f0-9\]\{40\}\$/);
  assert.match(serviceWorkerSource, /validateCachedRelease\(CANDIDATE_CACHE_NAME\)/);
  assert.match(serviceWorkerSource, /loadVerifiedCachedManifest/);
  assert.match(serviceWorkerSource, /loadVerifiedCachedAsset/);
  assert.match(serviceWorkerSource, /repairActiveRelease/);
  assert.match(serviceWorkerSource, /status: 503/);
  assert.match(serviceWorkerSource, /BUILD_PROVENANCE/);
  assert.match(serviceWorkerSource, /manifest\.provenance\?\.commit/);
  assert.match(serviceWorkerSource, /Asset manifest does not contain the exact release asset set/);
  assert.match(serviceWorkerSource, /request\.mode === "navigate"/);
  assert.match(serviceWorkerSource, /course-content\.json/);
  assert.match(serviceWorkerSource, /markdown\.js/);

  const activationHandler = serviceWorkerSource.match(
    /self\.addEventListener\("activate"[\s\S]+?\n}\);/,
  )?.[0];
  assert.ok(activationHandler);
  assert.ok(
    activationHandler.indexOf("validateCachedRelease(CANDIDATE_CACHE_NAME)") <
      activationHandler.indexOf("caches.keys()"),
  );

  const verifiedServe = serviceWorkerSource.match(
    /async function serveVerifiedCachedPath[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(verifiedServe);
  assert.match(verifiedServe, /loadVerifiedCachedManifest\(cache\)/);
  assert.match(verifiedServe, /loadVerifiedCachedAsset\(cache/);
  assert.match(verifiedServe, /repairActiveRelease\(\)/);
  assert.match(verifiedServe, /unavailableResponse\(unavailableMessage\)/);
  assert.match(
    serviceWorkerSource,
    /fetchStructurallyValidNetworkVersion\(\)\.catch\(\(\) =>\s*serveVerifiedCachedPath\(/,
  );
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

test("Markdown keeps literal wildcard text inside strong labels", () => {
  const rendered = renderMarkdown(
    "Choose **All files (*.*)** in the file picker.",
  );
  assert.equal(
    rendered,
    "<p>Choose <strong>All files (*.*)</strong> in the file picker.</p>",
  );
  assert.doesNotMatch(rendered, /<em>\.<\/em>/);
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
  assert.match(
    appSource,
    /postMessage\(\{[\s\S]+?type: "SKIP_WAITING"[\s\S]+?workerScriptUrl: waiting\.scriptURL/,
  );
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
  assert.match(appSource, /setAttribute\(\s*"aria-valuenow"/);
  assert.match(appSource, /setAttribute\(\s*"aria-valuetext"/);
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
  assert.match(
    appSource,
    /addEventListener\("hashchange",\s*\(\) => \{\s*pendingRouteFocus = true;\s*renderRoute\(\);\s*}\)/,
  );
  assert.match(cssSource, /min-height: 44px/);
  assert.match(cssSource, /\.brand\s*\{[\s\S]+?min-height: 44px/);
  assert.match(cssSource, /\.copy-code[\s\S]+?min-height: 44px/);
  assert.match(cssSource, /input\[type="range"\][\s\S]+?min-height: 44px/);
  assert.match(cssSource, /env\(safe-area-inset-bottom/);
  assert.match(cssSource, /@media \(max-width: 920px\)/);
  assert.match(cssSource, /@media \(max-width: 360px\)/);
  assert.match(cssSource, /@media \(forced-colors: active\)/);
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

test("the 320-pixel layout has single-column safeguards and no fixed page floor", () => {
  const narrowRules = cssSource.match(
    /@media \(max-width: 360px\) \{[\s\S]+?\n\}\n\n@media \(prefers-reduced-motion/,
  )?.[0];
  assert.ok(narrowRules);
  assert.match(
    narrowRules,
    /\.progress-overview\s*\{[\s\S]+?grid-template-columns: 1fr/,
  );
  assert.match(
    narrowRules,
    /\.bottom-nav button\s*\{[\s\S]+?min-width: 0/,
  );
  assert.match(narrowRules, /overflow-wrap: anywhere/);
  assert.doesNotMatch(
    cssSource,
    /(?:html|body)\s*\{[^}]*min-width:\s*[1-9]\d{2}px/,
  );
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
    "MAX_NOTE_CODE_POINTS",
    `${captureSource}; return captureNoteInState;`,
  )(noteState, false, 50000);
  captureNoteInState("lesson-one", "Keep this note");
  assert.equal(noteState.notes["lesson-one"], "Keep this note");
  captureNoteInState("lesson-two", "x".repeat(50010));
  assert.equal(noteState.notes["lesson-two"].length, 50000);
  captureNoteInState("lesson-one", "   ");
  assert.equal("lesson-one" in noteState.notes, false);

  assert.match(appSource, /localStorage\.setItem\(STORAGE_KEY, encoded\)/);
  assert.match(appSource, /localStorage\.getItem\(STORAGE_KEY\) !== encoded/);
  assert.match(appSource, /Progress could not be saved on this device/);
  assert.match(appSource, /mergeConcurrentState\(base, state, remote\.state\)/);
  assert.match(appSource, /Another course window changed the same item/);

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
    { id: "module-nine", core: true },
    { id: "reference-page", core: false, group: "reference" },
  ];
  const byId = new Map(documents.map((document) => [document.id, document]));
  const sequence = documents.slice(0, 7);
  const makeResume = (lastDocument, completedIds, practicalPassedIds = completedIds) =>
    Function(
      "learningSequenceDocuments",
      "documentById",
      "state",
      "isDocumentComplete",
      "requiresPracticalSelfCheck",
      "isPracticalPassed",
      `${helperSource}; return resumeDocument;`,
    )(
      () => sequence,
      byId,
      { lastDocument },
      (document) => completedIds.has(document.id),
      (document) => sequence.some((candidate) => candidate.id === document.id),
      (document) => practicalPassedIds.has(document.id),
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
    "software-check",
  );
  assert.equal(
    makeResume("module-nine", new Set())().id,
    "readiness",
  );
  assert.equal(
    makeResume(
      "windows-setup",
      new Set([...completedThroughFoundationTwo, "software-check"]),
    )().id,
    "windows-setup",
  );
  assert.equal(
    makeResume(
      "foundation-three",
      new Set([
        ...completedThroughFoundationTwo,
        "software-check",
        "windows-setup",
        "foundation-three",
      ]),
      new Set([
        ...completedThroughFoundationTwo,
        "software-check",
        "windows-setup",
      ]),
    )().id,
    "foundation-three",
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
  assert.match(appSource, /"Page read"[\s\S]+?"Read again"[\s\S]+?"Page not read"/);
  assert.match(
    appSource,
    /const activeView = Object\.values\(views\)\.find[\s\S]+?querySelector\("h1"\)/,
  );
  assert.match(appSource, /heading\.setAttribute\("tabindex", "-1"\)/);
  const renderRouteSource = appSource.match(
    /function renderRoute\(\) \{[\s\S]+?^}/m,
  )?.[0];
  assert.ok(renderRouteSource);
  assert.doesNotMatch(renderRouteSource, /querySelector\("#main-content"\)/);
  assert.match(
    appSource,
    /querySelector\("\.skip-link"\)\.addEventListener\("click"[\s\S]+?preventDefault\(\)[\s\S]+?querySelector\("#main-content"\)[\s\S]+?focus\(\{ preventScroll: true }\)[\s\S]+?scrollIntoView/,
  );
});

test("reader keeps one page title and removes only the source document title", () => {
  assert.match(htmlSource, /<h1 id="reader-title"><\/h1>/);
  assert.equal(
    stripLeadingDocumentTitle("# Page title\n\n## First section\n\nBody"),
    "## First section\n\nBody",
  );
  assert.equal(
    stripLeadingDocumentTitle("## No source title\n\nBody"),
    "## No source title\n\nBody",
  );
  for (const courseDocument of bundle.documents) {
    const rendered = renderMarkdown(
      stripLeadingDocumentTitle(courseDocument.markdown),
    );
    assert.equal(
      (rendered.match(/<h1(?:\s|>)/g) || []).length,
      0,
      `${courseDocument.id} must rely on the reader's single visible h1`,
    );
  }
  assert.match(appSource, /stripLeadingDocumentTitle\(courseDocument\.markdown\)/);
});

test("effort and installation language reflect real practice and all devices", () => {
  assert.match(appSource, /total course hours/);
  assert.match(appSource, /estimatedPracticeHours \|\| courseDocument\?\.practiceHours/);
  assert.match(appSource, /Read: about \$\{readingMinutes\}/);
  assert.match(
    appSource,
    /Practice — AUTHOR ESTIMATE, NOT BEGINNER MEASURED: \$\{practiceHours\.minimum\}\\u2013\$\{practiceHours\.maximum\} hours/,
  );
  assert.match(appSource, /class="reader-effort-reading"/);
  assert.match(appSource, /class="reader-effort-practice"/);
  assert.doesNotMatch(appSource, /allow extra practice time/);
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
    "Evidence-linked offline mock summary",
    "Human review and action",
  ]) {
    assert.match(appSource, new RegExp(label));
  }
  assert.match(appSource, /class="progress-ring \$\{progressClass\(percent\)\}"/);
  assert.match(appSource, /courseDocument\.kind === "foundation"/);
  assert.match(appSource, /courseDocument\.kind === "module"/);
  assert.match(appSource, /Required page \$\{requiredPosition \+ 1\}/);
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
    /const showPracticeContract =[\s\S]+?requiresPracticalSelfCheck\(courseDocument\)[\s\S]+?courseDocument\.group === "course-4-capstone"/,
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
  assert.match(appSource, /Course 4 has one optional advanced prototype/);
  assert.match(appSource, /progressive web app \(PWA\)/);
  assert.match(
    appSource,
    /progressive web app \\\(PWA\\\)\/i\.test\(rawCareerSummary\)/,
  );
  assert.match(appSource, /data-career-action="course"/);
  assert.match(appSource, /data-career-action="prototype"/);
  assert.match(appSource, /Show the later-course prototype link/);
  assert.match(appSource, /Open the later-course prototype/);
  assert.match(cssSource, /\.later-course-disclosure/);
  assert.match(cssSource, /\.career-course-card\.current/);
  assert.match(cssSource, /\.career-course-card\.prototype/);
  assert.match(cssSource, /\.career-detail-grid/);
});

test("first visible abbreviations are expanded in beginner language", () => {
  assert.match(
    htmlSource,
    /<strong>Controlled artificial intelligence<\/strong>/,
  );
  assert.match(
    appSource,
    /design a bounded artificial intelligence \(AI\) contribution, test its controls with an offline stand-in/,
  );
  assert.match(appSource, /Course 1 makes no live AI call/);
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
  assert.match(appSource, /Research and source review date/);
  assert.match(appSource, /Sources verified through:/);
  assert.match(appSource, /Course content revised through:/);
  assert.match(htmlSource, /Research and sources verified through/);
  assert.match(htmlSource, /Course content revised through/);
  assert.match(htmlSource, /Application and reading settings/);
  assert.match(appSource, /different fictional names or data/);
  assert.match(
    appSource,
    /Codex, the artificial intelligence \(AI\) course assistant/,
  );
  assert.match(appSource, /Read: about \$\{readingMinutes\}/);
  assert.match(htmlSource, />Escape<\/kbd>/);
  assert.match(htmlSource, /Safari<\/strong>, Apple’s web browser/);
  assert.match(
    htmlSource,
    /does not send progress or notes to GitHub or an artificial intelligence provider/,
  );
  assert.match(htmlSource, /same freddywinkel\.github\.io website origin/);
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
  assert.match(stateSource, /STATE_SCHEMA_VERSION = 3/);
  assert.match(stateSource, /STORAGE_FORMAT = "ai-workflow-course-storage-v1"/);
  assert.match(appSource, /parsed\.schemaVersion === 1/);
  assert.match(appSource, /function migrateSchemaV1\(legacy\)/);
  assert.match(appSource, /courseDocument\.legacyIds\.includes\(storedId\)/);
  assert.match(appSource, /completed:/);
  assert.match(appSource, /completionRevisions:/);
  assert.match(appSource, /notes:/);
  assert.match(appSource, /archivedLegacyNotes:/);
  assert.match(appSource, /lastDocument:/);
  assert.match(appSource, /validateBackupPayload\(payload/);
  assert.match(appSource, /const runtimeSnapshot = captureRuntimeSnapshot\(\)/);
  assert.match(appSource, /const previousVisible = runtimeSnapshot\.state/);
  assert.match(appSource, /recoveryType: "pre-import-state"/);
  assert.match(appSource, /rollbackStateTransaction\(/);
  assert.match(appSource, /concurrentRecoveryPreserved/);
  assert.match(appSource, /primarySnapshotVerified/);
  assert.match(appSource, /resetBarrierSnapshotVerified/);
  assert.match(appSource, /recoverySnapshotVerified/);
  assert.match(appSource, /runtimeStateVerified/);
  assert.match(appSource, /visibleRenderVerified/);
  assert.match(appSource, /reconciliationRequired/);
  assert.match(
    appSource,
    /current !== transactionOwned\[property\][\s\S]+?current !== snapshot\[property\]/,
  );
  assert.match(appSource, /changed externally and preserved/);
  assert.match(appSource, /Overall rollback:/);
  assert.match(appSource, /renderCourseNavigation\(\)[\s\S]+?renderRoute\(\)/);
  assert.match(appSource, /stateStorageQuarantined = false/);
  assert.match(appSource, /allowedPracticalDocumentIds: practicalDocumentIds/);
  assert.match(appSource, /allowedBundleSchemaVersions: bundleSchemaVersions/);
  assert.match(
    appSource,
    /writeStorageValueAndVerify\(STORAGE_KEY, resetRaw\)[\s\S]+?window\.history\.replaceState[\s\S]+?renderRoute\(\)/,
  );
  assert.match(
    appSource,
    /state\.completionRevisions\[courseDocument\.id\] ===[\s\S]+?completionRevisionFor\(courseDocument\)/,
  );
  assert.match(appSource, /\[1, 2, STATE_SCHEMA_VERSION\]\.includes/);
  assert.match(appSource, /requestInAppConfirmation/);
  assert.match(appSource, /action-confirmation-dialog/);
  assert.doesNotMatch(appSource, /window\.confirm\(/);
  assert.doesNotMatch(appSource, /sessionStorage/);
  assert.match(appSource, /stateStorageQuarantined = true/);
  assert.match(appSource, /if \(!stateStorageQuarantined\) saveState\(\)/);
  assert.doesNotMatch(serviceWorkerSource, /localStorage/);
});

test("page reading and practical self-checks are separate backward-compatible records", () => {
  assert.match(htmlSource, /id="complete-button"[^>]+aria-pressed="false"/);
  assert.match(htmlSource, /id="practical-pass-button"[^>]+aria-pressed="false"/);
  assert.match(htmlSource, /not an independent assessment or proof of consultant competence/);
  assert.match(appSource, /practicalPassed: \[\]/);
  assert.match(appSource, /practicalPassRevisions: \{\}/);
  assert.match(appSource, /function togglePracticalPassed\(\)/);
  assert.match(appSource, /Practical self-check recorded\. This is not an independent assessment\./);
  assert.match(appSource, /Reading every page does not mean you passed the practical work\./);
  assert.match(appSource, /const documents = learningSequenceDocuments\(\)/);
  assert.match(
    appSource,
    /return learningSequenceDocuments\(\)\.filter\(\(courseDocument\) =>/,
  );
  assert.match(appSource, /requiredIds\.includes\(courseDocument\.id\)/);
  assert.match(htmlSource, /0 of 21 required Course 1 pages read/);
  assert.match(htmlSource, /0 of 21 required practical tasks self-attested/);
  assert.match(appSource, /state\.practicalPassRevisions\[courseDocument\.id\]/);
  assert.match(
    appSource,
    /imported\.practicalPassed = imported\.practicalPassed\.filter/,
  );
  assert.match(
    appSource,
    /imported\.practicalPassRevisions = Object\.fromEntries/,
  );
  assert.match(
    htmlSource,
    /pages read, practical self-checks, local learning notes, and reading settings/,
  );

  const defaultStateSource = appSource.match(
    /function defaultState\(\) \{[\s\S]+?^\}/m,
  )?.[0];
  assert.ok(defaultStateSource);
  const createDefaultState = Function(
    "STATE_SCHEMA_VERSION",
    `${defaultStateSource}; return defaultState;`,
  )(3);
  const freshState = createDefaultState();
  assert.deepEqual(freshState.completed, []);
  assert.deepEqual(freshState.practicalPassed, []);
  assert.deepEqual(freshState.practicalPassRevisions, {});
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
  const onboardingDocument = bundle.documents.find(
    (document) =>
      !document.core &&
      bundle.course.learningSequenceIds.includes(document.id),
  );
  assert.ok(onboardingDocument);
  assert.equal(
    completionRevisionFor(onboardingDocument),
    `${onboardingDocument.revision}|practice:${bundle.course.practiceRevision}`,
  );
  assert.match(coreDocument.revision, /^\d{4}-\d{2}-\d{2}$/);
  assert.match(
    appSource,
    /state\.completionRevisions\[courseDocument\.id\] !==[\s\S]+?completionRevisionFor\(courseDocument\)/,
  );
  assert.match(
    appSource,
    /\^\\d\{4\}-\\d\{2\}-\\d\{2\}\(\?:\\\|practice:\[1-9\]\\d\*\)\?\$/,
  );
  assert.match(appSource, /notes: safeMap\(source\.notes\)/);
  assert.match(appSource, /\["system", "light", "dark"\]\.includes\(source\.theme\)/);
});

test("built JavaScript is syntactically valid and required artifacts exist", async () => {
  for (const file of ["app.js", "bootstrap.js", "markdown.js", "state.js", "sw.js"]) {
    execFileSync(nodeExecutable, ["--check", join(distRoot, file)], {
      stdio: "pipe",
    });
  }
  for (const file of [
    "scripts/build.mjs",
    "scripts/serve.mjs",
    "scripts/browser-smoke.mjs",
    "scripts/browser-update-smoke.mjs",
  ]) {
    execFileSync(nodeExecutable, ["--check", join(appRoot, file)], {
      stdio: "pipe",
    });
  }
  for (const file of [
    "index.html",
    "bootstrap.js",
    "app.js",
    "markdown.js",
    "state.js",
    "styles.css",
    "asset-manifest.json",
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
