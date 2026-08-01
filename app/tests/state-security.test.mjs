import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { safeLink } from "../src/markdown.js";
import {
  BACKUP_MAX_BYTES,
  STATE_SCHEMA_VERSION,
  assertBoundedJson,
  createStorageEnvelope,
  decodeStorageRecord,
  mergeConcurrentState,
  validateBackupPayload,
} from "../src/state.js";

const appRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));

function defaultState() {
  return {
    schemaVersion: STATE_SCHEMA_VERSION,
    completed: [],
    completionRevisions: {},
    practicalPassed: [],
    practicalPassRevisions: {},
    notes: {},
    archivedLegacyNotes: {},
    lastDocument: null,
    theme: "system",
    fontSize: 100,
    lastUpdateCheck: null,
    expandedGroups: ["foundations"],
    migration: null,
  };
}

function backup(state = defaultState()) {
  return {
    exportType: "ai-workflow-course-progress",
    exportedAt: "2026-07-28T12:00:00.000Z",
    bundleSchemaVersion: 2,
    courseId: "controlled-ai-workflow-foundations",
    courseVersion: "2.6.0",
    state,
  };
}

const validationContext = {
  courseId: "controlled-ai-workflow-foundations",
  allowedStateKeys: Object.keys(defaultState()),
  allowedDocumentIds: new Set(["lesson-a", "lesson-b"]),
  allowedGroupIds: new Set(["foundations", "modules"]),
  allowedPracticalDocumentIds: new Set(["lesson-a"]),
  allowedBundleSchemaVersions: new Set([2]),
};

test("storage envelope has a monotonic revision and exact closed shape", () => {
  const envelope = createStorageEnvelope(defaultState(), 7, "writer-12345678");
  const decoded = decodeStorageRecord(JSON.stringify(envelope));
  assert.equal(decoded.kind, "envelope");
  assert.equal(decoded.revision, 7);
  assert.equal(decoded.writerId, "writer-12345678");
  assert.deepEqual(decoded.state, defaultState());

  const extra = { ...envelope, surprise: true };
  assert.throws(() => decodeStorageRecord(JSON.stringify(extra)), /unsupported fields/);
});

test("concurrent non-conflicting progress and notes merge without lost updates", () => {
  const base = defaultState();
  const local = defaultState();
  local.completed = ["lesson-a"];
  local.completionRevisions = { "lesson-a": "2026-07-28|practice:5" };
  const remote = defaultState();
  remote.notes = { "lesson-b": "Remember the evidence boundary." };

  const merged = mergeConcurrentState(base, local, remote);
  assert.deepEqual(merged.conflicts, []);
  assert.deepEqual(merged.state.completed, ["lesson-a"]);
  assert.equal(merged.state.notes["lesson-b"], "Remember the evidence boundary.");
});

test("concurrent edits to the same note produce an explicit conflict", () => {
  const base = defaultState();
  base.notes = { "lesson-a": "base" };
  const local = structuredClone(base);
  local.notes["lesson-a"] = "local";
  const remote = structuredClone(base);
  remote.notes["lesson-a"] = "remote";

  const merged = mergeConcurrentState(base, local, remote);
  assert.deepEqual(merged.conflicts, ["notes.lesson-a"]);
  assert.equal(merged.state.notes["lesson-a"], "remote");
});

test("backup validation is closed, bounded, and rejects prototype keys", () => {
  const valid = backup();
  valid.state.completed = ["lesson-a"];
  valid.state.completionRevisions = {
    "lesson-a": "2026-07-28|practice:5",
  };
  assert.doesNotThrow(() => validateBackupPayload(valid, validationContext));

  assert.throws(
    () => validateBackupPayload({ ...valid, surprise: true }, validationContext),
    /unsupported fields/,
  );
  const polluted = JSON.parse(
    JSON.stringify(valid).replace(
      '"migration":null',
      '"migration":null,"__proto__":{"polluted":true}',
    ),
  );
  assert.throws(
    () => validateBackupPayload(polluted, validationContext),
    /unsafe field/,
  );
  const unknown = structuredClone(valid);
  unknown.state.completed = ["unknown"];
  assert.throws(
    () => validateBackupPayload(unknown, validationContext),
    /unique supported identifiers/,
  );
});

test("backup metadata must be canonical and match the supported bundle contract", () => {
  const invalidTime = backup();
  invalidTime.exportedAt = "2026-07-28T12:00:00Z";
  assert.throws(
    () => validateBackupPayload(invalidTime, validationContext),
    /invalid export time/,
  );

  const invalidBundle = backup();
  invalidBundle.bundleSchemaVersion = 3;
  assert.throws(
    () => validateBackupPayload(invalidBundle, validationContext),
    /unsupported bundle schema/,
  );

  const invalidVersion = backup();
  invalidVersion.courseVersion = "latest";
  assert.throws(
    () => validateBackupPayload(invalidVersion, validationContext),
    /invalid course version/,
  );
});

test("backup progress identifiers are unique, exact, and type-limited", () => {
  const duplicate = backup();
  duplicate.state.completed = ["lesson-a", "lesson-a"];
  duplicate.state.completionRevisions = {
    "lesson-a": "2026-07-28|practice:5",
  };
  assert.throws(
    () => validateBackupPayload(duplicate, validationContext),
    /unique supported identifiers/,
  );

  const impossiblePractical = backup();
  impossiblePractical.state.practicalPassed = ["lesson-b"];
  impossiblePractical.state.practicalPassRevisions = {
    "lesson-b": "2026-07-28|practice:5",
  };
  assert.throws(
    () => validateBackupPayload(impossiblePractical, validationContext),
    /unique supported identifiers/,
  );

  const unknownLastPage = backup();
  unknownLastPage.state.lastDocument = "unknown";
  assert.throws(
    () => validateBackupPayload(unknownLastPage, validationContext),
    /unknown last page/,
  );

  const forgedRevision = backup();
  forgedRevision.state.completionRevisions = {
    "lesson-a": "2026-07-28|practice:5",
  };
  assert.throws(
    () => validateBackupPayload(forgedRevision, validationContext),
    /invalid page revision/,
  );
});

test("migration metadata exactly accounts for unknown progress and archived notes", () => {
  const migrated = backup();
  migrated.state.archivedLegacyNotes = {
    "legacy-note": "Preserved legacy note.",
  };
  migrated.state.migration = {
    fromSchemaVersion: 1,
    migratedAt: "2026-07-28T12:05:00.000Z",
    unmappedCompleted: ["legacy-page"],
    unmappedNoteIds: ["legacy-note"],
  };
  assert.doesNotThrow(() =>
    validateBackupPayload(migrated, validationContext),
  );

  const forgedSource = structuredClone(migrated);
  forgedSource.state.migration.fromSchemaVersion = 2;
  assert.throws(
    () => validateBackupPayload(forgedSource, validationContext),
    /invalid migration metadata/,
  );

  const missingArchive = structuredClone(migrated);
  missingArchive.state.migration.unmappedNoteIds = [];
  assert.throws(
    () => validateBackupPayload(missingArchive, validationContext),
    /does not match this course/,
  );

  const knownPageClaimedUnmapped = structuredClone(migrated);
  knownPageClaimedUnmapped.state.migration.unmappedCompleted = ["lesson-a"];
  assert.throws(
    () => validateBackupPayload(knownPageClaimedUnmapped, validationContext),
    /does not match this course/,
  );
});

test("JSON complexity and documented backup byte limit reject hostile input", () => {
  let deep = {};
  let cursor = deep;
  for (let index = 0; index < 14; index += 1) {
    cursor.next = {};
    cursor = cursor.next;
  }
  assert.throws(() => assertBoundedJson(deep), /nested too deeply/);
  assert.equal(BACKUP_MAX_BYTES, 5_242_880);
});

test("URL allowlist accepts HTTPS and course-relative links only", () => {
  assert.equal(safeLink("https://example.com/path"), "https://example.com/path");
  assert.equal(safeLink("../modules/MODULE_01.md"), "../modules/MODULE_01.md");
  for (const unsafe of [
    "http://example.com",
    "mailto:test@example.com",
    "javascript:alert(1)",
    "data:text/html,boom",
    "//example.com/path",
    "https://user:pass@example.com/path",
    "..%2f..%2fsecret",
    "folder\\secret",
    "https://example.com/\nheader",
  ]) {
    assert.equal(safeLink(unsafe), "#unsafe-link", unsafe);
  }
});

test("built app has strict CSP assets and a hash-bound service worker manifest", async () => {
  const [html, serviceWorker, manifest] = await Promise.all([
    readFile(join(appRoot, "dist", "index.html"), "utf8"),
    readFile(join(appRoot, "dist", "sw.js"), "utf8"),
    readFile(join(appRoot, "dist", "asset-manifest.json"), "utf8"),
  ]);
  assert.match(
    html,
    /default-src 'none'; script-src 'self'; style-src 'self'/,
  );
  assert.doesNotMatch(html, /<script(?![^>]*\bsrc=)/);
  assert.match(html, /bootstrap\.js/);
  assert.match(serviceWorker, /ASSET_MANIFEST_SHA256 = "[a-f0-9]{64}"/);
  assert.doesNotMatch(serviceWorker, /__ASSET_MANIFEST_SHA256__/);
  const parsed = JSON.parse(manifest);
  assert.equal(parsed.schemaVersion, 1);
  assert.match(parsed.provenance.commit, /^(?:working-copy|[a-f0-9]{40})$/);
  assert.match(
    serviceWorker,
    new RegExp(`BUILD_PROVENANCE = "${parsed.provenance.commit}"`),
  );
  assert.ok(parsed.assets["state.js"]);
  assert.ok(parsed.assets["course-content.json"]);
  assert.equal(Object.keys(parsed.assets).length, 14);
});
