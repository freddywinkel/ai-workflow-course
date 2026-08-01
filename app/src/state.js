export const STATE_SCHEMA_VERSION = 3;
export const STORAGE_FORMAT = "ai-workflow-course-storage-v1";
export const BACKUP_MAX_BYTES = 5 * 1024 * 1024;
export const MAX_NOTE_CODE_POINTS = 50000;
export const MAX_TOTAL_NOTE_CODE_POINTS = 1000000;
export const MAX_ARCHIVED_NOTES = 100;

const BLOCKED_KEYS = new Set(["__proto__", "prototype", "constructor"]);
const ARRAY_FIELDS = ["completed", "practicalPassed", "expandedGroups"];
const MAP_FIELDS = [
  "completionRevisions",
  "practicalPassRevisions",
  "notes",
  "archivedLegacyNotes",
];
const SCALAR_FIELDS = [
  "schemaVersion",
  "lastDocument",
  "theme",
  "fontSize",
  "lastUpdateCheck",
  "migration",
  "resetEpoch",
];

export function cloneJson(value) {
  return JSON.parse(JSON.stringify(value));
}

function sameValue(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function exactKeys(value, expected, label) {
  const actual = Object.keys(value).sort();
  const wanted = [...expected].sort();
  if (!sameValue(actual, wanted)) {
    throw new Error(`${label} contains unsupported fields.`);
  }
}

function isCanonicalIsoTimestamp(value) {
  if (typeof value !== "string") return false;
  const parsed = new Date(value);
  return !Number.isNaN(parsed.getTime()) && parsed.toISOString() === value;
}

function isSafeStoredIdentifier(value) {
  return (
    typeof value === "string" &&
    value.length >= 1 &&
    value.length <= 200 &&
    !BLOCKED_KEYS.has(value) &&
    !/[\u0000-\u001f\u007f]/.test(value)
  );
}

function requireUniqueStringArray(value, label, allowedValues = null) {
  if (
    !Array.isArray(value) ||
    value.some(
      (item) =>
        !isSafeStoredIdentifier(item) ||
        (allowedValues !== null && !allowedValues.has(item)),
    ) ||
    new Set(value).size !== value.length
  ) {
    throw new Error(`${label} must contain unique supported identifiers.`);
  }
}

function requirePlainMap(value, label) {
  if (
    !value ||
    typeof value !== "object" ||
    Array.isArray(value) ||
    Object.getPrototypeOf(value) !== Object.prototype
  ) {
    throw new Error(`${label} must be an object.`);
  }
}

export function assertBoundedJson(
  value,
  {
    maxDepth = 12,
    maxProperties = 500,
    maxItems = 500,
    label = "JSON",
  } = {},
) {
  const visit = (item, depth) => {
    if (depth > maxDepth) throw new Error(`${label} is nested too deeply.`);
    if (item === null || ["string", "number", "boolean"].includes(typeof item)) {
      return;
    }
    if (Array.isArray(item)) {
      if (item.length > maxItems) throw new Error(`${label} contains too many items.`);
      item.forEach((entry) => visit(entry, depth + 1));
      return;
    }
    if (typeof item !== "object" || Object.getPrototypeOf(item) !== Object.prototype) {
      throw new Error(`${label} contains an unsupported value.`);
    }
    const keys = Object.keys(item);
    if (keys.length > maxProperties) {
      throw new Error(`${label} contains too many properties.`);
    }
    for (const key of keys) {
      if (BLOCKED_KEYS.has(key)) throw new Error(`${label} contains an unsafe field.`);
      visit(item[key], depth + 1);
    }
  };
  visit(value, 0);
}

export function decodeStorageRecord(raw) {
  if (!raw) return { kind: "empty", revision: 0, writerId: null, state: null };
  const parsed = JSON.parse(raw);
  assertBoundedJson(parsed, { label: "Saved course state" });
  if (parsed?.storageFormat !== STORAGE_FORMAT) {
    return { kind: "legacy", revision: 0, writerId: null, state: parsed };
  }
  exactKeys(
    parsed,
    ["storageFormat", "revision", "writerId", "state"],
    "Saved course state",
  );
  if (!Number.isSafeInteger(parsed.revision) || parsed.revision < 1) {
    throw new Error("Saved course state has an invalid revision.");
  }
  if (
    typeof parsed.writerId !== "string" ||
    !/^[A-Za-z0-9-]{8,80}$/.test(parsed.writerId)
  ) {
    throw new Error("Saved course state has an invalid writer identifier.");
  }
  return {
    kind: "envelope",
    revision: parsed.revision,
    writerId: parsed.writerId,
    state: parsed.state,
  };
}

export function createStorageEnvelope(state, revision, writerId) {
  if (!Number.isSafeInteger(revision) || revision < 1) {
    throw new Error("Storage revision must be a positive integer.");
  }
  if (typeof writerId !== "string" || !/^[A-Za-z0-9-]{8,80}$/.test(writerId)) {
    throw new Error("Writer identifier is invalid.");
  }
  return {
    storageFormat: STORAGE_FORMAT,
    revision,
    writerId,
    state: cloneJson(state),
  };
}

function mergeSetField(baseValues, localValues, remoteValues) {
  const base = new Set(baseValues);
  const local = new Set(localValues);
  const merged = new Set(remoteValues);
  for (const value of base) {
    if (!local.has(value)) merged.delete(value);
  }
  for (const value of local) {
    if (!base.has(value)) merged.add(value);
  }
  return [...merged];
}

function mergeMapField(baseMap, localMap, remoteMap, field, conflicts) {
  const merged = { ...remoteMap };
  const keys = new Set([
    ...Object.keys(baseMap),
    ...Object.keys(localMap),
    ...Object.keys(remoteMap),
  ]);
  for (const key of keys) {
    const baseHas = Object.hasOwn(baseMap, key);
    const localHas = Object.hasOwn(localMap, key);
    const remoteHas = Object.hasOwn(remoteMap, key);
    const localChanged =
      localHas !== baseHas || (localHas && !sameValue(localMap[key], baseMap[key]));
    const remoteChanged =
      remoteHas !== baseHas || (remoteHas && !sameValue(remoteMap[key], baseMap[key]));
    if (
      localChanged &&
      remoteChanged &&
      (localHas !== remoteHas ||
        (localHas && !sameValue(localMap[key], remoteMap[key])))
    ) {
      conflicts.push(`${field}.${key}`);
      continue;
    }
    if (!localChanged) continue;
    if (localHas) merged[key] = cloneJson(localMap[key]);
    else delete merged[key];
  }
  return merged;
}

export function mergeConcurrentState(baseState, localState, remoteState) {
  const base = cloneJson(baseState);
  const local = cloneJson(localState);
  const remote = cloneJson(remoteState);
  const merged = cloneJson(remote);
  const conflicts = [];

  for (const field of ARRAY_FIELDS) {
    merged[field] = mergeSetField(base[field] || [], local[field] || [], remote[field] || []);
  }
  for (const field of MAP_FIELDS) {
    merged[field] = mergeMapField(
      base[field] || {},
      local[field] || {},
      remote[field] || {},
      field,
      conflicts,
    );
  }
  for (const field of SCALAR_FIELDS) {
    if (field === "lastUpdateCheck") {
      const values = [local[field], remote[field]].filter(
        (value) => typeof value === "string" && !Number.isNaN(Date.parse(value)),
      );
      merged[field] = values.sort().at(-1) || null;
      continue;
    }
    const localChanged = !sameValue(local[field], base[field]);
    const remoteChanged = !sameValue(remote[field], base[field]);
    if (localChanged && remoteChanged && !sameValue(local[field], remote[field])) {
      conflicts.push(field);
      continue;
    }
    if (localChanged) merged[field] = cloneJson(local[field]);
  }
  return { state: merged, conflicts };
}

export function validateBackupPayload(
  payload,
  {
    courseId,
    allowedStateKeys,
    allowedDocumentIds,
    allowedGroupIds,
    allowedPracticalDocumentIds = allowedDocumentIds,
    allowedBundleSchemaVersions = new Set([2]),
    legacy = false,
  },
) {
  assertBoundedJson(payload, { label: "Progress backup" });
  exactKeys(
    payload,
    [
      "exportType",
      "exportedAt",
      "bundleSchemaVersion",
      "courseId",
      "courseVersion",
      "state",
    ],
    "Progress backup",
  );
  if (payload.exportType !== "ai-workflow-course-progress" || payload.courseId !== courseId) {
    throw new Error("Not a supported course progress backup.");
  }
  if (!isCanonicalIsoTimestamp(payload.exportedAt)) {
    throw new Error("The progress backup has an invalid export time.");
  }
  if (
    !Number.isSafeInteger(payload.bundleSchemaVersion) ||
    !(allowedBundleSchemaVersions instanceof Set) ||
    !allowedBundleSchemaVersions.has(payload.bundleSchemaVersion)
  ) {
    throw new Error("The progress backup has an unsupported bundle schema.");
  }
  if (
    typeof payload.courseVersion !== "string" ||
    !/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(payload.courseVersion)
  ) {
    throw new Error("The progress backup has an invalid course version.");
  }
  if (!payload.state || typeof payload.state !== "object" || Array.isArray(payload.state)) {
    throw new Error("The progress backup has no valid state.");
  }
  exactKeys(payload.state, allowedStateKeys, "Progress backup state");
  if (
    (legacy && payload.state.schemaVersion !== 1) ||
    (!legacy && ![2, STATE_SCHEMA_VERSION].includes(payload.state.schemaVersion))
  ) {
    throw new Error("The progress backup has an unsupported state schema.");
  }

  for (const field of legacy ? ["completed"] : ["completed", "practicalPassed"]) {
    const allowed =
      legacy ? null : field === "practicalPassed" ? allowedPracticalDocumentIds : allowedDocumentIds;
    requireUniqueStringArray(
      payload.state[field],
      `Progress backup ${field}`,
      allowed,
    );
  }
  requireUniqueStringArray(
    payload.state.expandedGroups,
    "Progress backup expandedGroups",
    legacy ? new Set([...allowedGroupIds, "weeks"]) : allowedGroupIds,
  );

  for (const field of legacy
    ? []
    : ["completionRevisions", "practicalPassRevisions"]) {
    requirePlainMap(payload.state[field], `Progress backup ${field}`);
    const entries = Object.entries(payload.state[field]);
    const progressField =
      field === "completionRevisions" ? "completed" : "practicalPassed";
    const allowed =
      field === "completionRevisions"
        ? allowedDocumentIds
        : allowedPracticalDocumentIds;
    if (
      entries.some(
        ([id, revision]) =>
          !allowed.has(id) ||
          typeof revision !== "string" ||
          !/^\d{4}-\d{2}-\d{2}(?:\|practice:[1-9]\d*)?$/.test(revision),
      ) ||
      entries.length !== payload.state[progressField].length ||
      entries.some(([id]) => !payload.state[progressField].includes(id))
    ) {
      throw new Error("The progress backup contains an invalid page revision.");
    }
  }

  requirePlainMap(payload.state.notes, "Progress backup notes");
  if (!legacy) {
    requirePlainMap(
      payload.state.archivedLegacyNotes,
      "Progress backup archived notes",
    );
  }
  const noteEntries = Object.entries(payload.state.notes);
  const archivedEntries = legacy
    ? []
    : Object.entries(payload.state.archivedLegacyNotes);
  if (archivedEntries.length > MAX_ARCHIVED_NOTES) {
    throw new Error("The progress backup contains too many archived notes.");
  }
  let totalNoteCodePoints = 0;
  for (const [id, note] of noteEntries) {
    if (!isSafeStoredIdentifier(id) || typeof note !== "string") {
      throw new Error("The progress backup contains an invalid note.");
    }
    if (!legacy && !allowedDocumentIds.has(id)) {
      throw new Error("The progress backup contains a note for an unknown page.");
    }
    const noteLength = [...note].length;
    if (noteLength > MAX_NOTE_CODE_POINTS) {
      throw new Error("A progress-backup note is too long.");
    }
    totalNoteCodePoints += noteLength;
  }
  for (const [id, note] of archivedEntries) {
    if (!isSafeStoredIdentifier(id) || typeof note !== "string") {
      throw new Error("The progress backup contains an invalid archived note.");
    }
    const noteLength = [...note].length;
    if (noteLength > MAX_NOTE_CODE_POINTS) {
      throw new Error("An archived progress-backup note is too long.");
    }
    totalNoteCodePoints += noteLength;
  }
  if (totalNoteCodePoints > MAX_TOTAL_NOTE_CODE_POINTS) {
    throw new Error("The progress backup contains too much note text.");
  }

  if (
    payload.state.lastDocument !== null &&
    (!isSafeStoredIdentifier(payload.state.lastDocument) ||
      (!legacy && !allowedDocumentIds.has(payload.state.lastDocument)))
  ) {
    throw new Error("The progress backup has an unknown last page.");
  }
  if (!["system", "light", "dark"].includes(payload.state.theme)) {
    throw new Error("The progress backup has an invalid theme.");
  }
  if (
    !Number.isInteger(payload.state.fontSize) ||
    payload.state.fontSize < 90 ||
    payload.state.fontSize > 125
  ) {
    throw new Error("The progress backup has an invalid text size.");
  }
  if (
    payload.state.lastUpdateCheck !== null &&
    !isCanonicalIsoTimestamp(payload.state.lastUpdateCheck)
  ) {
    throw new Error("The progress backup has an invalid update-check time.");
  }

  if (!legacy && payload.state.migration !== null) {
    requirePlainMap(payload.state.migration, "Progress backup migration");
    exactKeys(
      payload.state.migration,
      [
        "fromSchemaVersion",
        "migratedAt",
        "unmappedCompleted",
        "unmappedNoteIds",
      ],
      "Progress backup migration",
    );
    if (
      payload.state.migration.fromSchemaVersion !== 1 ||
      !isCanonicalIsoTimestamp(payload.state.migration.migratedAt)
    ) {
      throw new Error("The progress backup has invalid migration metadata.");
    }
    requireUniqueStringArray(
      payload.state.migration.unmappedCompleted,
      "Progress backup unmapped completions",
    );
    requireUniqueStringArray(
      payload.state.migration.unmappedNoteIds,
      "Progress backup unmapped note identifiers",
    );
    const archivedIds = Object.keys(payload.state.archivedLegacyNotes).sort();
    const unmappedNoteIds = [...payload.state.migration.unmappedNoteIds].sort();
    if (
      payload.state.migration.unmappedCompleted.some((id) =>
        allowedDocumentIds.has(id),
      ) ||
      payload.state.migration.unmappedNoteIds.some((id) =>
        allowedDocumentIds.has(id),
      ) ||
      !sameValue(archivedIds, unmappedNoteIds)
    ) {
      throw new Error("The progress backup migration does not match this course.");
    }
  }
}
