import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFile, rm, mkdir, writeFile } from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { deflateSync } from "node:zlib";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const appRoot = resolve(scriptDirectory, "..");
const courseRoot = resolve(appRoot, "..");
const sourceRoot = join(appRoot, "src");
const outputRoot = join(appRoot, "dist");
const curriculumPath = join(courseRoot, "curriculum.json");

function normaliseBasePath(value = "/") {
  const trimmed = String(value).trim();
  if (!trimmed || trimmed === "/") return "/";
  return `/${trimmed.replace(/^\/+|\/+$/g, "")}/`;
}

function titleFromMarkdown(markdown, fallback) {
  const match = markdown.match(/^#\s+(.+)$/m);
  return match ? match[1].replace(/[*_`]/g, "").trim() : fallback;
}

function plainText(markdown) {
  return markdown
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/^>\s?/gm, "")
    .replace(/[*_~|>-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function descriptionFromMarkdown(markdown) {
  const paragraphs = markdown
    .replace(/^#.*$/m, "")
    .split(/\r?\n\s*\r?\n/)
    .map((value) => plainText(value))
    .filter((value) => value.length > 40);
  const description = paragraphs[0] || plainText(markdown);
  return description.length > 190 ? `${description.slice(0, 187)}…` : description;
}

function assertMetadata(condition, message) {
  if (!condition) throw new Error(`Invalid curriculum.json: ${message}`);
}

function isIsoDate(value) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    return false;
  }
  const parsed = new Date(`${value}T00:00:00Z`);
  return !Number.isNaN(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value;
}

function listedDocumentRevisions(curriculum) {
  if (!Array.isArray(curriculum?.groups)) return [];
  return curriculum.groups.flatMap((group) =>
    Array.isArray(group?.documents)
      ? group.documents
          .map((document) => document?.revision)
          .filter((revision) => typeof revision === "string")
      : [],
  );
}

function normaliseCurriculumMetadata(curriculum) {
  if (curriculum?.schemaVersion !== 2) return curriculum;
  const revisions = listedDocumentRevisions(curriculum).filter(isIsoDate);
  const legacySourceDate = curriculum.course?.verifiedThrough;
  return {
    ...curriculum,
    schemaVersion: 3,
    course: {
      ...curriculum.course,
      sourceVerifiedThrough: legacySourceDate,
      contentRevisionThrough:
        revisions.length > 0 ? [...revisions].sort().at(-1) : undefined,
      verifiedThrough: legacySourceDate,
    },
  };
}

function validateSourcePath(sourcePath, documentId) {
  assertMetadata(
    typeof sourcePath === "string" && sourcePath.endsWith(".md"),
    `document "${documentId}" must have a Markdown sourcePath`,
  );
  const normalised = sourcePath.replaceAll("\\", "/");
  assertMetadata(
    normalised === sourcePath &&
      !normalised.startsWith("/") &&
      !/^[a-zA-Z]:/.test(normalised) &&
      !normalised.split("/").includes(".."),
    `document "${documentId}" has an unsafe sourcePath`,
  );
}

async function readCurriculum() {
  let curriculum;
  try {
    curriculum = JSON.parse(await readFile(curriculumPath, "utf8"));
  } catch (error) {
    throw new Error(`Could not read curriculum.json: ${error.message}`);
  }

  curriculum = normaliseCurriculumMetadata(curriculum);
  assertMetadata(curriculum?.schemaVersion === 3, "schemaVersion must be 2 or 3");
  assertMetadata(curriculum.program?.id, "program.id is required");
  assertMetadata(curriculum.program?.title, "program.title is required");
  assertMetadata(curriculum.course?.id, "course.id is required");
  assertMetadata(curriculum.course?.title, "course.title is required");
  assertMetadata(
    /^\d+\.\d+\.\d+$/.test(curriculum.course?.version || ""),
    "course.version must be semantic version text",
  );
  assertMetadata(
    curriculum.course?.productStatus === "UNVERIFIED",
    "course.productStatus must be UNVERIFIED for this personal-study edition",
  );
  assertMetadata(
    curriculum.course?.distributionPurpose === "personal-synthetic-study",
    "course.distributionPurpose must be personal-synthetic-study",
  );
  assertMetadata(
    isIsoDate(curriculum.course?.sourceVerifiedThrough),
    "course.sourceVerifiedThrough must be an ISO date",
  );
  assertMetadata(
    isIsoDate(curriculum.course?.contentRevisionThrough),
    "course.contentRevisionThrough must be an ISO date",
  );
  assertMetadata(
    isIsoDate(curriculum.course?.verifiedThrough),
    "course.verifiedThrough compatibility alias must be an ISO date",
  );
  assertMetadata(
    curriculum.course.verifiedThrough === curriculum.course.sourceVerifiedThrough,
    "course.verifiedThrough must equal course.sourceVerifiedThrough",
  );
  assertMetadata(
    Array.isArray(curriculum.course?.coreGroupIds),
    "course.coreGroupIds must be an array",
  );
  assertMetadata(Array.isArray(curriculum.groups), "groups must be an array");
  assertMetadata(Array.isArray(curriculum.career?.courses), "career.courses must be an array");

  const groupIds = new Set();
  const documentIds = new Set();
  const legacyIds = new Set();
  const sourcePaths = new Set();
  const careerCourseIds = new Set();

  for (const course of curriculum.career.courses) {
    assertMetadata(course?.id && course?.title, "each career course needs an id and title");
    assertMetadata(
      Number.isInteger(course.sequence) && course.sequence > 0,
      `career course "${course.id}" needs a positive integer sequence`,
    );
    assertMetadata(!careerCourseIds.has(course.id), `duplicate career course "${course.id}"`);
    careerCourseIds.add(course.id);
  }
  assertMetadata(
    careerCourseIds.has(curriculum.course.id),
    "the current course must appear in career.courses",
  );

  for (const group of curriculum.groups) {
    assertMetadata(group?.id && group?.title, "every group needs an id and title");
    assertMetadata(!groupIds.has(group.id), `duplicate group id "${group.id}"`);
    groupIds.add(group.id);
    assertMetadata(
      Array.isArray(group.documents) && group.documents.length > 0,
      `group "${group.id}" must contain documents`,
    );
    for (const document of group.documents) {
      assertMetadata(document?.id, `a document in "${group.id}" is missing its stable id`);
      assertMetadata(
        /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(document.id),
        `document id "${document.id}" must be lower-case kebab-case`,
      );
      assertMetadata(
        !documentIds.has(document.id) && !legacyIds.has(document.id),
        `document id "${document.id}" is duplicated or conflicts with a legacy id`,
      );
      documentIds.add(document.id);
      const documentCourseId = document.courseId || curriculum.course.id;
      assertMetadata(
        careerCourseIds.has(documentCourseId),
        `document "${document.id}" references unknown course "${documentCourseId}"`,
      );
      assertMetadata(
        isIsoDate(document.revision),
        `document "${document.id}" needs an ISO revision date`,
      );
      validateSourcePath(document.sourcePath, document.id);
      assertMetadata(
        !sourcePaths.has(document.sourcePath),
        `sourcePath "${document.sourcePath}" is listed more than once`,
      );
      sourcePaths.add(document.sourcePath);
      assertMetadata(
        document.legacyIds === undefined || Array.isArray(document.legacyIds),
        `document "${document.id}" legacyIds must be an array`,
      );
      if (document.estimatedPracticeHours !== undefined) {
        const estimate = document.estimatedPracticeHours;
        assertMetadata(
          estimate &&
            Number.isFinite(estimate.minimum) &&
            Number.isFinite(estimate.maximum) &&
            estimate.minimum > 0 &&
            estimate.maximum >= estimate.minimum,
          `document "${document.id}" estimatedPracticeHours needs positive minimum and maximum values`,
        );
      }
      for (const legacyId of document.legacyIds || []) {
        assertMetadata(
          typeof legacyId === "string" && legacyId,
          `document "${document.id}" has an invalid legacy id`,
        );
        assertMetadata(
          !documentIds.has(legacyId) && !legacyIds.has(legacyId),
          `legacy id "${legacyId}" is ambiguous`,
        );
        legacyIds.add(legacyId);
      }
    }
  }

  for (const coreGroupId of curriculum.course.coreGroupIds) {
    assertMetadata(groupIds.has(coreGroupId), `unknown core group "${coreGroupId}"`);
  }

  const documentRevisions = listedDocumentRevisions(curriculum);
  const latestDocumentRevision = [...documentRevisions].sort().at(-1);
  assertMetadata(
    latestDocumentRevision === curriculum.course.contentRevisionThrough,
    "course.contentRevisionThrough must equal the latest document revision",
  );

  return curriculum;
}

async function collectGroups() {
  const curriculum = await readCurriculum();
  return curriculum.groups.map((group) => ({
    ...group,
    documents: group.documents.map((document) => ({ ...document })),
  }));
}

async function createCourseBundle() {
  const curriculum = await readCurriculum();
  const groups = [];
  const documents = [];

  for (const groupMetadata of curriculum.groups) {
    const group = {
      id: groupMetadata.id,
      title: groupMetadata.title,
      kind: groupMetadata.kind || "reference",
      core:
        groupMetadata.core === true ||
        curriculum.course.coreGroupIds.includes(groupMetadata.id),
      documents: [],
    };
    for (const documentMetadata of groupMetadata.documents) {
      const sourcePath = documentMetadata.sourcePath;
      const absolutePath = join(courseRoot, ...sourcePath.split("/"));
      let markdown;
      try {
        markdown = await readFile(absolutePath, "utf8");
      } catch (error) {
        throw new Error(
          `Curriculum source missing for "${documentMetadata.id}": ${sourcePath} (${error.message})`,
        );
      }
      const searchableText = plainText(markdown);
      documents.push({
        id: documentMetadata.id,
        revision: documentMetadata.revision,
        legacyIds: [...(documentMetadata.legacyIds || [])],
        title: documentMetadata.title || titleFromMarkdown(markdown, sourcePath),
        group: group.id,
        kind: group.kind,
        core: group.core,
        courseId: documentMetadata.courseId || curriculum.course.id,
        order: documents.length,
        sourcePath,
        description:
          documentMetadata.description || descriptionFromMarkdown(markdown),
        learningOutcome: documentMetadata.learningOutcome || null,
        estimatedPracticeHours:
          documentMetadata.estimatedPracticeHours || null,
        markdown,
        searchableText,
        wordCount: searchableText ? searchableText.split(/\s+/).length : 0,
      });
      group.documents.push(documentMetadata.id);
    }
    groups.push(group);
  }

  const digestInput = [
    JSON.stringify(curriculum),
    documents
      .map((document) => `${document.sourcePath}\n${document.markdown}`)
      .join("\n---COURSE-DOCUMENT---\n"),
  ].join("\n---CURRICULUM-METADATA---\n");
  const contentHash = createHash("sha256").update(digestInput).digest("hex");
  const coreDocuments = documents.filter((document) => document.core);
  const foundations = documents.filter((document) => document.group === "foundations");
  const modules = documents.filter((document) => document.group === "modules");

  return {
    schemaVersion: 2,
    program: curriculum.program,
    course: {
      ...curriculum.course,
      contentHash,
      foundationCount: foundations.length,
      moduleCount: modules.length,
      coreLessonCount: coreDocuments.length,
    },
    groups,
    documents,
    career: curriculum.career,
  };
}

function crc32(buffer) {
  let crc = 0xffffffff;
  for (const byte of buffer) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1));
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function pngChunk(type, data) {
  const typeBuffer = Buffer.from(type);
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length);
  const checksum = Buffer.alloc(4);
  checksum.writeUInt32BE(crc32(Buffer.concat([typeBuffer, data])));
  return Buffer.concat([length, typeBuffer, data, checksum]);
}

function createIconPng(size, maskable = false) {
  const rgba = Buffer.alloc(size * size * 4);
  const safeInset = maskable ? 0.16 : 0.08;
  const inset = Math.floor(size * safeInset);
  const radius = Math.floor(size * (maskable ? 0.22 : 0.18));

  function insideRoundedSquare(x, y) {
    if (x < inset || y < inset || x >= size - inset || y >= size - inset) return false;
    const left = inset + radius;
    const right = size - inset - radius - 1;
    const top = inset + radius;
    const bottom = size - inset - radius - 1;
    if (x >= left && x <= right) return true;
    if (y >= top && y <= bottom) return true;
    const cx = x < left ? left : right;
    const cy = y < top ? top : bottom;
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2;
  }

  function nearLine(x, y, x1, y1, x2, y2, width) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const lengthSquared = dx * dx + dy * dy;
    const projection = Math.max(
      0,
      Math.min(1, ((x - x1) * dx + (y - y1) * dy) / lengthSquared),
    );
    const px = x1 + projection * dx;
    const py = y1 + projection * dy;
    return (x - px) ** 2 + (y - py) ** 2 <= width ** 2;
  }

  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const offset = (y * size + x) * 4;
      let colour = [244, 241, 232, 255];
      if (insideRoundedSquare(x, y)) colour = [23, 58, 56, 255];

      const s = size;
      const lineWidth = Math.max(3, Math.floor(s * 0.035));
      const isFlow =
        nearLine(x, y, s * 0.31, s * 0.36, s * 0.69, s * 0.36, lineWidth) ||
        nearLine(x, y, s * 0.31, s * 0.5, s * 0.58, s * 0.5, lineWidth);
      const isCheck =
        nearLine(x, y, s * 0.43, s * 0.62, s * 0.53, s * 0.71, lineWidth) ||
        nearLine(x, y, s * 0.53, s * 0.71, s * 0.72, s * 0.53, lineWidth);
      const isNode =
        (x - s * 0.28) ** 2 + (y - s * 0.36) ** 2 <= (s * 0.045) ** 2 ||
        (x - s * 0.72) ** 2 + (y - s * 0.36) ** 2 <= (s * 0.045) ** 2 ||
        (x - s * 0.28) ** 2 + (y - s * 0.5) ** 2 <= (s * 0.045) ** 2;
      if (isFlow || isNode) colour = [109, 214, 187, 255];
      if (isCheck) colour = [255, 201, 93, 255];
      rgba.set(colour, offset);
    }
  }

  const raw = Buffer.alloc((size * 4 + 1) * size);
  for (let row = 0; row < size; row += 1) {
    const targetOffset = row * (size * 4 + 1);
    raw[targetOffset] = 0;
    rgba.copy(raw, targetOffset + 1, row * size * 4, (row + 1) * size * 4);
  }

  const header = Buffer.alloc(13);
  header.writeUInt32BE(size, 0);
  header.writeUInt32BE(size, 4);
  header[8] = 8;
  header[9] = 6;
  return Buffer.concat([
    Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]),
    pngChunk("IHDR", header),
    pngChunk("IDAT", deflateSync(raw, { level: 9 })),
    pngChunk("IEND", Buffer.alloc(0)),
  ]);
}

const FULL_GIT_COMMIT = /^[a-f0-9]{40}$/;
const BUILD_MODES = new Set(["development", "candidate"]);

function selectBuildProvenance({
  mode,
  workflowCommit,
  repositoryCommit,
  repositoryClean,
}) {
  const normalisedMode = String(mode || "").trim().toLowerCase();
  if (!BUILD_MODES.has(normalisedMode)) {
    throw new Error(
      "COURSE1_BUILD_MODE must be either development or candidate.",
    );
  }
  if (normalisedMode === "development") return "working-copy";
  if (!FULL_GIT_COMMIT.test(workflowCommit || "")) {
    throw new Error(
      "Candidate builds require GITHUB_SHA as one full lower-case 40-character commit.",
    );
  }
  if (!FULL_GIT_COMMIT.test(repositoryCommit || "")) {
    throw new Error(
      "Candidate builds require a Git checkout with one full 40-character HEAD commit.",
    );
  }
  if (repositoryCommit !== workflowCommit) {
    throw new Error("Candidate GITHUB_SHA does not match the checked-out HEAD commit.");
  }
  if (repositoryClean !== true) {
    throw new Error(
      "Candidate builds require a clean source tree; commit or remove every tracked and untracked source change first.",
    );
  }
  return workflowCommit;
}

function gitRepositoryContext() {
  try {
    const repositoryCommit = execFileSync("git", ["rev-parse", "HEAD"], {
      cwd: courseRoot,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    })
      .trim()
      .toLowerCase();
    const status = execFileSync(
      "git",
      ["status", "--porcelain=v1", "--untracked-files=all"],
      {
        cwd: courseRoot,
        encoding: "utf8",
        stdio: ["ignore", "pipe", "ignore"],
      },
    );
    return {
      repositoryCommit,
      repositoryClean: status.length === 0,
    };
  } catch {
    return {
      repositoryCommit: "",
      repositoryClean: false,
    };
  }
}

function buildProvenance() {
  const repository = gitRepositoryContext();
  return selectBuildProvenance({
    mode: process.env.COURSE1_BUILD_MODE || "development",
    workflowCommit: String(process.env.GITHUB_SHA || "").trim().toLowerCase(),
    repositoryCommit: repository.repositoryCommit,
    repositoryClean: repository.repositoryClean,
  });
}

function createBuildId({
  contentHash,
  sourceAssets,
  buildScriptSource,
  basePath,
  commit,
}) {
  if (typeof commit !== "string" || !commit.trim()) {
    throw new Error("Build commit provenance is required.");
  }
  const buildInputs = [
    ...sourceAssets,
    ["scripts/build.mjs", buildScriptSource],
  ];
  const assetDigest = buildInputs
    .map(([name, body]) => `${name}\n${body}`)
    .join("\n");
  return createHash("sha256")
    .update(
      `${contentHash}\n${assetDigest}\n${basePath}\ncommit:${commit.trim().toLowerCase()}`,
    )
    .digest("hex")
    .slice(0, 12);
}

function generatedProgressAndReaderRules() {
  const progress = Array.from(
    { length: 101 },
    (_, value) => `.progress-pct-${value}{--progress:${value}}`,
  );
  const reader = Array.from(
    { length: 36 },
    (_, index) => {
      const value = index + 90;
      return `.reader-scale-${value}{--reader-scale:${value / 100}}`;
    },
  );
  return `\n/* Generated fixed-value classes keep the strict Content Security Policy free of inline styles. */\n${[
    ...progress,
    ...reader,
  ].join("\n")}\n`;
}

async function build() {
  const basePath = normaliseBasePath(process.env.BASE_PATH || "/");
  const commit = buildProvenance();
  const bundle = await createCourseBundle();
  const sourceAssetNames = [
    "index.html",
    "styles.css",
    "bootstrap.js",
    "app.js",
    "markdown.js",
    "state.js",
    "sw.js",
    "favicon.svg",
  ];
  const sourceAssets = await Promise.all(
    sourceAssetNames.map(async (name) => [name, await readFile(join(sourceRoot, name), "utf8")]),
  );
  const buildScriptSource = await readFile(fileURLToPath(import.meta.url), "utf8");
  const buildId = createBuildId({
    contentHash: bundle.course.contentHash,
    sourceAssets,
    buildScriptSource,
    basePath,
    commit,
  });
  const replacements = new Map([
    ["__BASE_PATH__", basePath],
    ["__BUILD_ID__", buildId],
    ["__COURSE_VERSION__", bundle.course.version],
    ["__PRODUCT_STATUS__", bundle.course.productStatus],
    ["__DISTRIBUTION_PURPOSE__", bundle.course.distributionPurpose],
    ["__SOURCE_VERIFIED_THROUGH__", bundle.course.sourceVerifiedThrough],
    ["__CONTENT_REVISION_THROUGH__", bundle.course.contentRevisionThrough],
    ["__VERIFIED_THROUGH__", bundle.course.verifiedThrough],
    ["__CONTENT_HASH__", bundle.course.contentHash],
    ["__BUILD_PROVENANCE__", commit],
  ]);

  await rm(outputRoot, { recursive: true, force: true });
  await mkdir(join(outputRoot, "icons"), { recursive: true });

  for (const [name, source] of sourceAssets) {
    if (name === "sw.js") continue;
    let output = source;
    for (const [placeholder, value] of replacements) {
      output = output.replaceAll(placeholder, value);
    }
    if (name === "styles.css") output += generatedProgressAndReaderRules();
    await writeFile(join(outputRoot, name), output, "utf8");
  }

  const manifest = {
    id: basePath,
    name: "Controlled Artificial Intelligence (AI) Workflow Foundations",
    short_name: "Controlled Workflow",
    description:
      "Course 1 of the path to controlled artificial intelligence (AI) workflow implementation consulting for Dutch small and medium-sized enterprises (SMEs).",
    lang: "en",
    start_url: basePath,
    scope: basePath,
    display: "standalone",
    orientation: "any",
    background_color: "#f4f1e8",
    theme_color: "#173a38",
    categories: ["education", "productivity"],
    icons: [
      { src: "icons/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "icons/icon-512.png", sizes: "512x512", type: "image/png" },
      {
        src: "icons/icon-maskable-512.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
    ],
  };

  await writeFile(
    join(outputRoot, "course-content.json"),
    `${JSON.stringify(bundle)}\n`,
    "utf8",
  );
  await writeFile(
    join(outputRoot, "manifest.webmanifest"),
    `${JSON.stringify(manifest, null, 2)}\n`,
    "utf8",
  );
  await writeFile(
    join(outputRoot, "version.json"),
    `${JSON.stringify(
      {
        buildId,
        bundleSchemaVersion: bundle.schemaVersion,
        programId: bundle.program.id,
        courseId: bundle.course.id,
        courseVersion: bundle.course.version,
        productStatus: bundle.course.productStatus,
        distributionPurpose: bundle.course.distributionPurpose,
        sourceVerifiedThrough: bundle.course.sourceVerifiedThrough,
        contentRevisionThrough: bundle.course.contentRevisionThrough,
        verifiedThrough: bundle.course.verifiedThrough,
        contentHash: bundle.course.contentHash,
        commit,
      },
      null,
      2,
    )}\n`,
    "utf8",
  );
  await writeFile(join(outputRoot, "icons", "icon-192.png"), createIconPng(192));
  await writeFile(join(outputRoot, "icons", "icon-512.png"), createIconPng(512));
  await writeFile(
    join(outputRoot, "icons", "icon-maskable-512.png"),
    createIconPng(512, true),
  );
  await writeFile(join(outputRoot, "icons", "apple-touch-icon.png"), createIconPng(180));
  const precacheFiles = [
    "index.html",
    "bootstrap.js",
    "app.js",
    "markdown.js",
    "state.js",
    "styles.css",
    "favicon.svg",
    "course-content.json",
    "manifest.webmanifest",
    "version.json",
    "icons/icon-192.png",
    "icons/icon-512.png",
    "icons/icon-maskable-512.png",
    "icons/apple-touch-icon.png",
  ];
  const contentTypes = {
    ".css": "text/css",
    ".html": "text/html",
    ".js": "text/javascript",
    ".json": "application/json",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".webmanifest": "application/manifest+json",
  };
  const assetEntries = {};
  for (const relativePath of precacheFiles) {
    const bytes = await readFile(join(outputRoot, ...relativePath.split("/")));
    const extension = relativePath.slice(relativePath.lastIndexOf("."));
    assetEntries[relativePath] = {
      sha256: createHash("sha256").update(bytes).digest("hex"),
      contentType: contentTypes[extension],
    };
  }
  const assetManifestText = `${JSON.stringify(
    {
      schemaVersion: 1,
      buildId,
      contentHash: bundle.course.contentHash,
      provenance: {
        commit,
      },
      assets: assetEntries,
    },
    null,
    2,
  )}\n`;
  await writeFile(
    join(outputRoot, "asset-manifest.json"),
    assetManifestText,
    "utf8",
  );
  const assetManifestSha256 = createHash("sha256")
    .update(assetManifestText)
    .digest("hex");
  let serviceWorkerOutput = sourceAssets.find(([name]) => name === "sw.js")[1];
  for (const [placeholder, value] of replacements) {
    serviceWorkerOutput = serviceWorkerOutput.replaceAll(placeholder, value);
  }
  serviceWorkerOutput = serviceWorkerOutput.replaceAll(
    "__ASSET_MANIFEST_SHA256__",
    assetManifestSha256,
  );
  await writeFile(join(outputRoot, "sw.js"), serviceWorkerOutput, "utf8");
  await writeFile(join(outputRoot, ".nojekyll"), "", "utf8");

  const summary = {
    output: relative(courseRoot, outputRoot).replaceAll("\\", "/"),
    basePath,
    buildId,
    courseVersion: bundle.course.version,
    documents: bundle.documents.length,
    foundations: bundle.course.foundationCount,
    modules: bundle.course.moduleCount,
    coreLessons: bundle.course.coreLessonCount,
  };
  process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
  return summary;
}

export {
  build,
  collectGroups,
  createCourseBundle,
  createBuildId,
  createIconPng,
  normaliseCurriculumMetadata,
  normaliseBasePath,
  selectBuildProvenance,
};

if (resolve(process.argv[1] || "") === fileURLToPath(import.meta.url)) {
  await build();
}
