import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFile, readdir, rm, mkdir, writeFile } from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { deflateSync } from "node:zlib";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const appRoot = resolve(scriptDirectory, "..");
const courseRoot = resolve(appRoot, "..");
const sourceRoot = join(appRoot, "src");
const outputRoot = join(appRoot, "dist");

function normaliseBasePath(value = "/") {
  const trimmed = String(value).trim();
  if (!trimmed || trimmed === "/") return "/";
  return `/${trimmed.replace(/^\/+|\/+$/g, "")}/`;
}

function documentId(sourcePath) {
  return sourcePath
    .replace(/\.md$/i, "")
    .replace(/README$/i, "index")
    .replace(/[\\/]+/g, "-")
    .replace(/_/g, "-")
    .replace(/[^a-zA-Z0-9-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
    .toLowerCase();
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

async function markdownFiles(directory, filter = () => true) {
  const names = await readdir(join(courseRoot, directory));
  return names
    .filter((name) => name.toLowerCase().endsWith(".md") && filter(name))
    .sort((a, b) => a.localeCompare(b, "en", { numeric: true }))
    .map((name) => `${directory}/${name}`.replaceAll("\\", "/"));
}

async function collectGroups() {
  const foundations = await markdownFiles("foundations");
  const foundationIndex = foundations.filter((path) => path.endsWith("/README.md"));
  const foundationLessons = foundations.filter((path) => /\/\d{2}_.+\.md$/.test(path));
  const glossary = foundations.filter((path) => path.endsWith("/GLOSSARY.md"));
  const weeks = await markdownFiles("weeks", (name) => /^WEEK_\d{2}\.md$/.test(name));
  const templates = await markdownFiles("templates");
  const updateReports = await markdownFiles(
    "updates",
    (name) => name !== "README.md",
  );

  return [
    {
      id: "start",
      title: "Start here",
      documents: [
        "README.md",
        "BEGINNER_READINESS_CHECK.md",
        "COURSE_OVERVIEW.md",
        "SETUP_WINDOWS.md",
      ],
    },
    {
      id: "foundations",
      title: "Beginner foundations",
      documents: [...foundationIndex, ...foundationLessons, ...glossary],
    },
    {
      id: "weeks",
      title: "Twelve-week build",
      documents: weeks,
    },
    {
      id: "reference",
      title: "Build reference",
      documents: [
        "ARCHITECTURE_AND_CONTRACTS.md",
        "SOFTWARE_MATRIX.md",
        "CAPSTONE_SPECIFICATION.md",
        "ASSESSMENT_AND_RUBRIC.md",
        "SOURCE_REGISTER.md",
      ],
    },
    {
      id: "worksheets",
      title: "Worksheets",
      documents: templates,
    },
    {
      id: "updates",
      title: "Updates and release",
      documents: [
        "PWA_AND_UPDATES.md",
        "EVERGREEN_UPDATE_PROMPT.md",
        "COURSE_CHANGELOG.md",
        "RELEASE_VALIDATION.md",
        "VALIDATION_REPORT.md",
        "updates/README.md",
        ...updateReports,
      ],
    },
  ];
}

async function createCourseBundle() {
  const groups = await collectGroups();
  const seenPaths = new Set();
  const documents = [];

  for (const group of groups) {
    const documentIds = [];
    for (const sourcePath of group.documents) {
      if (seenPaths.has(sourcePath)) continue;
      seenPaths.add(sourcePath);
      const absolutePath = join(courseRoot, ...sourcePath.split("/"));
      const markdown = await readFile(absolutePath, "utf8");
      const id = documentId(sourcePath);
      const searchableText = plainText(markdown);
      documents.push({
        id,
        title: titleFromMarkdown(markdown, sourcePath),
        group: group.id,
        order: documents.length,
        sourcePath,
        description: descriptionFromMarkdown(markdown),
        markdown,
        searchableText,
        wordCount: searchableText ? searchableText.split(/\s+/).length : 0,
      });
      documentIds.push(id);
    }
    group.documents = documentIds;
  }

  const rootReadme = documents.find((document) => document.sourcePath === "README.md");
  const version =
    rootReadme?.markdown.match(/^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)/m)?.[1] ||
    "0.0.0";
  const verifiedThrough =
    rootReadme?.markdown.match(/^Verified through:\s*(\d{4}-\d{2}-\d{2})/m)?.[1] ||
    "unknown";

  const digestInput = documents
    .map((document) => `${document.sourcePath}\n${document.markdown}`)
    .join("\n---COURSE-DOCUMENT---\n");
  const contentHash = createHash("sha256").update(digestInput).digest("hex");

  return {
    schemaVersion: 1,
    course: {
      title: "AI Workflow & Document Systems",
      subtitle: "A zero-to-builder course with human approval and traceable sources",
      version,
      verifiedThrough,
      contentHash,
      foundationCount: documents.filter((document) =>
        /^foundations\/\d{2}_/.test(document.sourcePath),
      ).length,
      weekCount: documents.filter((document) =>
        /^weeks\/WEEK_\d{2}\.md$/.test(document.sourcePath),
      ).length,
    },
    groups,
    documents,
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

async function gitCommit() {
  if (process.env.GITHUB_SHA) return process.env.GITHUB_SHA.slice(0, 12);
  try {
    return execFileSync("git", ["rev-parse", "--short=12", "HEAD"], {
      cwd: courseRoot,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
  } catch {
    return "working-copy";
  }
}

async function build() {
  const basePath = normaliseBasePath(process.env.BASE_PATH || "/");
  const bundle = await createCourseBundle();
  const sourceAssetNames = ["index.html", "styles.css", "app.js", "sw.js", "favicon.svg"];
  const sourceAssets = await Promise.all(
    sourceAssetNames.map(async (name) => [name, await readFile(join(sourceRoot, name), "utf8")]),
  );
  const assetDigest = sourceAssets.map(([name, body]) => `${name}\n${body}`).join("\n");
  const buildId = createHash("sha256")
    .update(`${bundle.course.contentHash}\n${assetDigest}\n${basePath}`)
    .digest("hex")
    .slice(0, 12);
  const commit = await gitCommit();
  const replacements = new Map([
    ["__BASE_PATH__", basePath],
    ["__BUILD_ID__", buildId],
    ["__COURSE_VERSION__", bundle.course.version],
    ["__VERIFIED_THROUGH__", bundle.course.verifiedThrough],
  ]);

  await rm(outputRoot, { recursive: true, force: true });
  await mkdir(join(outputRoot, "icons"), { recursive: true });

  for (const [name, source] of sourceAssets) {
    let output = source;
    for (const [placeholder, value] of replacements) {
      output = output.replaceAll(placeholder, value);
    }
    await writeFile(join(outputRoot, name), output, "utf8");
  }

  const manifest = {
    id: basePath,
    name: "AI Workflow & Document Systems Course",
    short_name: "AI Workflow",
    description: "A zero-to-builder course for safe, source-grounded AI document workflows.",
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
        courseVersion: bundle.course.version,
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
  await writeFile(join(outputRoot, ".nojekyll"), "", "utf8");

  const summary = {
    output: relative(courseRoot, outputRoot).replaceAll("\\", "/"),
    basePath,
    buildId,
    courseVersion: bundle.course.version,
    documents: bundle.documents.length,
    foundations: bundle.course.foundationCount,
    weeks: bundle.course.weekCount,
  };
  process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);
  return summary;
}

export {
  build,
  collectGroups,
  createCourseBundle,
  createIconPng,
  normaliseBasePath,
};

if (resolve(process.argv[1] || "") === fileURLToPath(import.meta.url)) {
  await build();
}
