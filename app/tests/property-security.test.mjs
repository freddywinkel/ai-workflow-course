import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { safeLink } from "../src/markdown.js";
import {
  MAX_ARCHIVED_NOTES,
  MAX_NOTE_CODE_POINTS,
  STATE_SCHEMA_VERSION,
  assertBoundedJson,
  createStorageEnvelope,
  decodeStorageRecord,
  mergeConcurrentState,
  validateBackupPayload,
} from "../src/state.js";

const appRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const corpusPath = resolve(appRoot, "..", "quality", "property-regression-corpus.json");
const corpus = JSON.parse(await readFile(corpusPath, "utf8"));

function generator(seed) {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

function randomToken(next, length = 12) {
  const alphabet = "abcdefghijklmnopqrstuvwxyz0123456789";
  let value = "";
  for (let index = 0; index < length; index += 1) {
    value += alphabet[Math.floor(next() * alphabet.length)];
  }
  return value;
}

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

const validationContext = {
  courseId: "controlled-ai-workflow-foundations",
  allowedStateKeys: Object.keys(defaultState()),
  allowedDocumentIds: new Set(["lesson-a", "lesson-b", "lesson-c"]),
  allowedGroupIds: new Set(["foundations", "modules"]),
  allowedPracticalDocumentIds: new Set(["lesson-a", "lesson-b"]),
  allowedBundleSchemaVersions: new Set([2]),
};

function backup(state) {
  return {
    exportType: "ai-workflow-course-progress",
    exportedAt: "2026-07-29T08:00:00.000Z",
    bundleSchemaVersion: 2,
    courseId: "controlled-ai-workflow-foundations",
    courseVersion: "2.6.0",
    state,
  };
}

test("PWA-PROP-001 generated URL corpus never enables a non-HTTPS scheme", () => {
  const next = generator(corpus.seed);
  for (const value of corpus.dangerousUrlFragments) {
    assert.equal(safeLink(value), "#unsafe-link", value);
  }
  for (const value of corpus.safeUrlFragments) {
    assert.notEqual(safeLink(value), "#unsafe-link", value);
  }
  for (let index = 0; index < corpus.generatedCasesPerProperty; index += 1) {
    const scheme = randomToken(next, 3 + Math.floor(next() * 10));
    const candidate = `${scheme}:payload-${randomToken(next)}`;
    const result = safeLink(candidate);
    assert.equal(result, "#unsafe-link", candidate);
  }
});

test("PWA-PROP-002 generated disjoint concurrent edits preserve both writers", () => {
  const next = generator(corpus.seed ^ 0x5f3759df);
  for (let index = 0; index < corpus.generatedCasesPerProperty; index += 1) {
    const localId = `local-${randomToken(next)}`;
    const remoteId = `remote-${randomToken(next)}`;
    const base = defaultState();
    const local = defaultState();
    const remote = defaultState();
    local.completed = [localId];
    local.notes = { [localId]: `local-${index}` };
    remote.completed = [remoteId];
    remote.notes = { [remoteId]: `remote-${index}` };
    const result = mergeConcurrentState(base, local, remote);
    assert.deepEqual(result.conflicts, []);
    assert.deepEqual(new Set(result.state.completed), new Set([localId, remoteId]));
    assert.deepEqual(result.state.notes, {
      [remoteId]: `remote-${index}`,
      [localId]: `local-${index}`,
    });
  }
});

test("PWA-PROP-003 generated same-note edits always remain conflicts", () => {
  const next = generator(corpus.seed ^ 0xa5a5a5a5);
  for (let index = 0; index < corpus.generatedCasesPerProperty; index += 1) {
    const id = `lesson-${randomToken(next)}`;
    const base = defaultState();
    const local = defaultState();
    const remote = defaultState();
    base.notes[id] = "base";
    local.notes[id] = `local-${index}`;
    remote.notes[id] = `remote-${index}`;
    const result = mergeConcurrentState(base, local, remote);
    assert.deepEqual(result.conflicts, [`notes.${id}`]);
    assert.equal(result.state.notes[id], `remote-${index}`);
  }
});

test("PWA-PROP-004 generated storage envelopes round-trip exact state only", () => {
  const next = generator(corpus.seed ^ 0x9e3779b9);
  for (let index = 1; index <= corpus.generatedCasesPerProperty; index += 1) {
    const state = defaultState();
    state.notes["lesson-a"] = randomToken(next, 1 + Math.floor(next() * 40));
    const writerId = `writer-${randomToken(next, 16)}`;
    const envelope = createStorageEnvelope(state, index, writerId);
    const decoded = decodeStorageRecord(JSON.stringify(envelope));
    assert.equal(decoded.revision, index);
    assert.equal(decoded.writerId, writerId);
    assert.deepEqual(decoded.state, state);
    assert.throws(
      () => decodeStorageRecord(JSON.stringify({ ...envelope, extra: true })),
      /unsupported fields/,
    );
  }
});

test("PWA-PROP-005 exact JSON and note boundaries fail closed", () => {
  for (const depth of corpus.jsonDepthBoundaries) {
    let value = "leaf";
    for (let index = 0; index < depth; index += 1) value = { next: value };
    if (depth <= 12) {
      assert.doesNotThrow(() => assertBoundedJson(value, { maxDepth: 12 }));
    } else {
      assert.throws(
        () => assertBoundedJson(value, { maxDepth: 12 }),
        /nested too deeply/,
      );
    }
  }

  for (const length of corpus.noteCodePointBoundaries) {
    const state = defaultState();
    state.notes["lesson-a"] = "x".repeat(length);
    const payload = backup(state);
    if (length <= MAX_NOTE_CODE_POINTS) {
      assert.doesNotThrow(() => validateBackupPayload(payload, validationContext));
    } else {
      assert.throws(
        () => validateBackupPayload(payload, validationContext),
        /too long/,
      );
    }
  }
});

test("PWA-PROP-006 generated malformed state branches reject by named boundary", () => {
  assert.doesNotThrow(() => assertBoundedJson([null, "text", 1, true]));
  assert.throws(
    () => assertBoundedJson(new Date()),
    /unsupported value/,
  );
  assert.throws(
    () => assertBoundedJson(Array.from({ length: 3 }), { maxItems: 2 }),
    /too many items/,
  );
  assert.throws(
    () => assertBoundedJson({ one: 1, two: 2 }, { maxProperties: 1 }),
    /too many properties/,
  );
  assert.throws(
    () => assertBoundedJson(JSON.parse('{"__proto__":true}')),
    /unsafe field/,
  );

  assert.deepEqual(decodeStorageRecord(""), {
    kind: "empty",
    revision: 0,
    writerId: null,
    state: null,
  });
  assert.equal(decodeStorageRecord('{"legacy":true}').kind, "legacy");
  for (const revision of [0, -1, 1.5, "1"]) {
    const envelope = {
      storageFormat: "ai-workflow-course-storage-v1",
      revision,
      writerId: "writer-12345678",
      state: defaultState(),
    };
    assert.throws(
      () => decodeStorageRecord(JSON.stringify(envelope)),
      /invalid revision/,
    );
    assert.throws(
      () => createStorageEnvelope(defaultState(), revision, "writer-12345678"),
      /positive integer/,
    );
  }
  for (const writerId of [null, "short", "bad_writer_underscore"]) {
    const envelope = {
      storageFormat: "ai-workflow-course-storage-v1",
      revision: 1,
      writerId,
      state: defaultState(),
    };
    assert.throws(
      () => decodeStorageRecord(JSON.stringify(envelope)),
      /invalid writer identifier/,
    );
    assert.throws(
      () => createStorageEnvelope(defaultState(), 1, writerId),
      /Writer identifier is invalid/,
    );
  }
});

test("PWA-PROP-007 generated merge branches preserve deletion and scalar conflicts", () => {
  const base = defaultState();
  base.notes["lesson-a"] = "remove me";
  base.theme = "system";
  base.lastUpdateCheck = "2026-07-28T08:00:00.000Z";

  const local = structuredClone(base);
  delete local.notes["lesson-a"];
  local.theme = "light";
  local.lastUpdateCheck = "invalid";

  const remote = structuredClone(base);
  remote.theme = "dark";
  remote.fontSize = 110;
  remote.lastUpdateCheck = "2026-07-29T08:00:00.000Z";

  const result = mergeConcurrentState(base, local, remote);
  assert.equal(Object.hasOwn(result.state.notes, "lesson-a"), false);
  assert.equal(result.state.theme, "dark");
  assert.equal(result.state.fontSize, 110);
  assert.equal(result.state.lastUpdateCheck, "2026-07-29T08:00:00.000Z");
  assert.deepEqual(result.conflicts, ["theme"]);
});

test("PWA-PROP-008 backup schema mutation table exercises every closed field family", () => {
  const validState = defaultState();
  const validPayload = backup(validState);
  const cases = [
    ["wrong product", { ...validPayload, exportType: "other" }, /Not a supported/],
    ["wrong course", { ...validPayload, courseId: "other" }, /Not a supported/],
    ["bad time", { ...validPayload, exportedAt: "yesterday" }, /invalid export time/],
    [
      "bad bundle schema",
      { ...validPayload, bundleSchemaVersion: "2" },
      /unsupported bundle schema/,
    ],
    ["bad course version", { ...validPayload, courseVersion: "v2" }, /invalid course version/],
    ["array state", { ...validPayload, state: [] }, /no valid state/],
    [
      "bad state schema",
      { ...validPayload, state: { ...validState, schemaVersion: 99 } },
      /unsupported state schema/,
    ],
    [
      "duplicate completed",
      { ...validPayload, state: { ...validState, completed: ["lesson-a", "lesson-a"] } },
      /unique supported identifiers/,
    ],
    [
      "revision mismatch",
      {
        ...validPayload,
        state: {
          ...validState,
          completed: ["lesson-a"],
          completionRevisions: {},
        },
      },
      /invalid page revision/,
    ],
    [
      "notes not map",
      { ...validPayload, state: { ...validState, notes: [] } },
      /must be an object/,
    ],
    [
      "unknown note",
      { ...validPayload, state: { ...validState, notes: { unknown: "text" } } },
      /unknown page/,
    ],
    [
      "invalid note value",
      { ...validPayload, state: { ...validState, notes: { "lesson-a": 1 } } },
      /invalid note/,
    ],
    [
      "too many archives",
      {
        ...validPayload,
        state: {
          ...validState,
          archivedLegacyNotes: Object.fromEntries(
            Array.from({ length: MAX_ARCHIVED_NOTES + 1 }, (_value, index) => [
              `old-${index}`,
              "x",
            ]),
          ),
        },
      },
      /too many archived notes/,
    ],
    [
      "invalid archived note",
      {
        ...validPayload,
        state: { ...validState, archivedLegacyNotes: { "old-1": 1 } },
      },
      /invalid archived note/,
    ],
    [
      "archived note too long",
      {
        ...validPayload,
        state: {
          ...validState,
          archivedLegacyNotes: { "old-1": "x".repeat(MAX_NOTE_CODE_POINTS + 1) },
        },
      },
      /archived progress-backup note is too long/i,
    ],
    [
      "unknown last document",
      { ...validPayload, state: { ...validState, lastDocument: "unknown" } },
      /unknown last page/,
    ],
    [
      "bad theme",
      { ...validPayload, state: { ...validState, theme: "sepia" } },
      /invalid theme/,
    ],
    [
      "bad text size",
      { ...validPayload, state: { ...validState, fontSize: 126 } },
      /invalid text size/,
    ],
    [
      "bad update time",
      { ...validPayload, state: { ...validState, lastUpdateCheck: "today" } },
      /invalid update-check time/,
    ],
    [
      "bad migration object",
      { ...validPayload, state: { ...validState, migration: [] } },
      /must be an object/,
    ],
  ];
  for (const [label, payload, pattern] of cases) {
    assert.throws(
      () => validateBackupPayload(payload, validationContext),
      pattern,
      label,
    );
  }
});

test("PWA-PROP-009 service-worker release identity checks cannot be omitted", async () => {
  const serviceWorker = await readFile(resolve(appRoot, "src", "sw.js"), "utf8");
  for (const requiredCheck of [
    /manifest\?\.schemaVersion !== 1/,
    /manifest\.buildId !== BUILD_ID/,
    /manifest\.contentHash !== CONTENT_HASH/,
    /manifest\.provenance\?\.commit !== BUILD_PROVENANCE/,
    /sha256\(bytes\)\) !== ASSET_MANIFEST_SHA256/,
  ]) {
    assert.match(serviceWorker, requiredCheck);
  }
});
