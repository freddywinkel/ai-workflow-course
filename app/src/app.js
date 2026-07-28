import {
  escapeAttribute,
  escapeHtml,
  renderMarkdown as renderCourseMarkdown,
} from "./markdown.js";

const config = window.__COURSE_APP__;
const STORAGE_KEY = "ai-workflow-course-state-v1";
const STATE_SCHEMA_VERSION = 2;
const FOUNDATION_PRACTICE_HOURS = Object.freeze({
  "course-1-foundation-01": { minimum: 4, maximum: 6 },
  "course-1-foundation-02": { minimum: 4, maximum: 6 },
  "course-1-foundation-03": { minimum: 8, maximum: 12 },
  "course-1-foundation-04": { minimum: 6, maximum: 10 },
  "course-1-foundation-05": { minimum: 5, maximum: 8 },
  "course-1-foundation-06": { minimum: 6, maximum: 10 },
  "course-1-foundation-07": { minimum: 5, maximum: 8 },
  "course-1-foundation-08": { minimum: 6, maximum: 10 },
  "course-1-foundation-09": { minimum: 6, maximum: 10 },
});
const views = {
  home: document.querySelector("#home-view"),
  reader: document.querySelector("#reader-view"),
  career: document.querySelector("#career-view"),
  search: document.querySelector("#search-view"),
  settings: document.querySelector("#settings-view"),
};

let courseBundle;
let documentById = new Map();
let documentByPath = new Map();
let currentDocument = null;
let serviceWorkerRegistration = null;
let pendingUpdateWorker = null;
let deferredInstallPrompt = null;
let reloadingForUpdate = false;
let toastTimer = null;
let noteTimer = null;
let noteStorageDirty = false;
let lastAutomaticUpdateCheck = 0;
let pendingRouteFocus = false;
let pendingLegacyState = null;

const state = loadState();

const ICON_PATHS = Object.freeze({
  arrow: '<path d="M5 12h14m-5-5 5 5-5 5"/>',
  check: '<path d="m5 12.5 4.2 4.2L19 7"/>',
  chevron: '<path d="m7 9 5 5 5-5"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  document:
    '<path d="M7 3h7l4 4v14H7Z"/><path d="M14 3v5h5M10 12h5M10 16h5"/>',
  extract:
    '<path d="M5 4h14v5H5ZM5 15h14v5H5Z"/><path d="M9 9v6M15 9v6"/>',
  layers: '<path d="m12 3 9 5-9 5-9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
  review:
    '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 4 4M8 10.5l1.7 1.7 3.5-4"/>',
  shield: '<path d="M12 3 5 6v5c0 4.8 2.8 8.1 7 10 4.2-1.9 7-5.2 7-10V6Z"/><path d="m9 12 2 2 4-5"/>',
});

function iconSvg(name, className = "ui-icon") {
  return `<svg class="${className}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${ICON_PATHS[name] || ""}</svg>`;
}

function practiceContractMarkup({ compact = false } = {}) {
  const introduction = compact
    ? "Use the same four steps for every practical lesson."
    : "Every practical lesson uses the same four steps. This helps you learn the skill instead of only copying an example.";
  return `
    <div class="practice-contract-heading">
      <span class="practice-contract-icon">${iconSvg("layers")}</span>
      <div>
        <span class="eyebrow">Beginner practice method</span>
        <h2>How practical lessons work</h2>
        <p>${introduction}</p>
      </div>
    </div>
    <ol class="practice-contract-steps">
      <li>
        <span>1</span>
        <div><strong>Follow along</strong><p>Complete the guided example and notice what each step does.</p></div>
      </li>
      <li>
        <span>2</span>
        <div><strong>Now recreate it with different data</strong><p>Close the worked example and create a new result with different fictional names or data.</p></div>
      </li>
      <li>
        <span>3</span>
        <div><strong>Ask Codex, the artificial intelligence (AI) course assistant, to check</strong><p>Tell Codex the exact practice folder to inspect. The check is read-only: Codex may report what it sees inside that folder, but it must not edit, move, or delete your files.</p></div>
      </li>
      <li>
        <span>4</span>
        <div><strong>Pass criteria</strong><p>Compare your result with the lesson’s exact checklist. Continue only when every item passes.</p></div>
      </li>
    </ol>
  `;
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

function normaliseV2State(parsed) {
  const fallback = defaultState();
  return {
    ...fallback,
    ...parsed,
    schemaVersion: STATE_SCHEMA_VERSION,
    completed: Array.isArray(parsed.completed) ? parsed.completed : [],
    completionRevisions:
      parsed.completionRevisions && typeof parsed.completionRevisions === "object"
        ? parsed.completionRevisions
        : {},
    practicalPassed: Array.isArray(parsed.practicalPassed)
      ? parsed.practicalPassed
      : [],
    practicalPassRevisions:
      parsed.practicalPassRevisions &&
      typeof parsed.practicalPassRevisions === "object"
        ? parsed.practicalPassRevisions
        : {},
    notes: parsed.notes && typeof parsed.notes === "object" ? parsed.notes : {},
    archivedLegacyNotes:
      parsed.archivedLegacyNotes && typeof parsed.archivedLegacyNotes === "object"
        ? parsed.archivedLegacyNotes
        : {},
    expandedGroups: Array.isArray(parsed.expandedGroups)
      ? parsed.expandedGroups
      : fallback.expandedGroups,
  };
}

function loadState() {
  const fallback = defaultState();
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if (!parsed) return fallback;
    if (parsed.schemaVersion === STATE_SCHEMA_VERSION) return normaliseV2State(parsed);
    if (parsed.schemaVersion === 1) {
      pendingLegacyState = parsed;
      return {
        ...fallback,
        theme: ["system", "light", "dark"].includes(parsed.theme)
          ? parsed.theme
          : fallback.theme,
        fontSize: Math.max(90, Math.min(125, Number(parsed.fontSize) || 100)),
        lastUpdateCheck: parsed.lastUpdateCheck || null,
      };
    }
    return fallback;
  } catch {
    return fallback;
  }
}

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    noteStorageDirty = false;
    return true;
  } catch {
    showToast("Progress could not be saved on this device.");
    return false;
  }
}

function documentForStoredId(storedId) {
  if (documentById.has(storedId)) return documentById.get(storedId);
  return courseBundle.documents.find((courseDocument) =>
    courseDocument.legacyIds.includes(storedId),
  );
}

function completionRevisionFor(courseDocument) {
  const practiceRevision = Number(courseBundle?.course?.practiceRevision);
  const requiredIds = courseBundle?.course?.learningSequenceIds;
  if (
    !Array.isArray(requiredIds) ||
    !requiredIds.includes(courseDocument.id) ||
    !Number.isInteger(practiceRevision) ||
    practiceRevision < 1
  ) {
    return courseDocument.revision;
  }
  return `${courseDocument.revision}|practice:${practiceRevision}`;
}

function migrateSchemaV1(legacy) {
  const migrated = defaultState();
  const unmappedCompleted = [];
  const unmappedNotes = {};

  for (const storedId of Array.isArray(legacy.completed) ? legacy.completed : []) {
    const courseDocument = documentForStoredId(storedId);
    if (!courseDocument) {
      unmappedCompleted.push(storedId);
      continue;
    }
    if (!migrated.completed.includes(courseDocument.id)) {
      migrated.completed.push(courseDocument.id);
      migrated.completionRevisions[courseDocument.id] = courseDocument.revision;
    }
  }

  if (legacy.notes && typeof legacy.notes === "object") {
    for (const [storedId, value] of Object.entries(legacy.notes)) {
      if (typeof value !== "string") continue;
      const note = value.slice(0, 50000);
      const courseDocument = documentForStoredId(storedId);
      if (!courseDocument) {
        unmappedNotes[storedId] = note;
        continue;
      }
      const previous = migrated.notes[courseDocument.id];
      migrated.notes[courseDocument.id] = previous
        ? `${previous}\n\n--- Migrated note ---\n\n${note}`.slice(0, 50000)
        : note;
    }
  }

  const lastDocument = documentForStoredId(legacy.lastDocument);
  migrated.lastDocument = lastDocument?.id || null;
  migrated.theme = ["system", "light", "dark"].includes(legacy.theme)
    ? legacy.theme
    : "system";
  migrated.fontSize = Math.max(90, Math.min(125, Number(legacy.fontSize) || 100));
  migrated.lastUpdateCheck = legacy.lastUpdateCheck || null;
  migrated.expandedGroups = Array.isArray(legacy.expandedGroups)
    ? [
        ...new Set(
          legacy.expandedGroups
            .map((groupId) => (groupId === "weeks" ? "modules" : groupId))
            .filter((groupId) =>
              courseBundle.groups.some((group) => group.id === groupId),
            ),
        ),
      ]
    : ["foundations"];
  migrated.archivedLegacyNotes = unmappedNotes;
  migrated.migration = {
    fromSchemaVersion: 1,
    migratedAt: new Date().toISOString(),
    unmappedCompleted,
    unmappedNoteIds: Object.keys(unmappedNotes),
  };
  return migrated;
}

function isDocumentComplete(courseDocument) {
  return (
    state.completed.includes(courseDocument.id) &&
    state.completionRevisions[courseDocument.id] ===
      completionRevisionFor(courseDocument)
  );
}

function needsRevisionReview(courseDocument) {
  return (
    state.completed.includes(courseDocument.id) &&
    Boolean(state.completionRevisions[courseDocument.id]) &&
    state.completionRevisions[courseDocument.id] !==
      completionRevisionFor(courseDocument)
  );
}

function requiresPracticalSelfCheck(courseDocument) {
  const requiredIds = courseBundle?.course?.learningSequenceIds;
  return Boolean(
    courseDocument?.courseId === courseBundle?.course?.id &&
      Array.isArray(requiredIds) &&
      requiredIds.includes(courseDocument.id),
  );
}

function isPracticalPassed(courseDocument) {
  return (
    requiresPracticalSelfCheck(courseDocument) &&
    state.practicalPassed.includes(courseDocument.id) &&
    state.practicalPassRevisions[courseDocument.id] ===
      completionRevisionFor(courseDocument)
  );
}

function needsPracticalRevisionReview(courseDocument) {
  return (
    requiresPracticalSelfCheck(courseDocument) &&
    state.practicalPassed.includes(courseDocument.id) &&
    Boolean(state.practicalPassRevisions[courseDocument.id]) &&
    state.practicalPassRevisions[courseDocument.id] !==
      completionRevisionFor(courseDocument)
  );
}

function groupTitle(groupId) {
  return courseBundle.groups.find((group) => group.id === groupId)?.title || groupId;
}

function belongsToCourseOne(courseDocument) {
  return courseDocument?.courseId === courseBundle.course.id;
}

function coreDocuments() {
  return courseBundle.documents.filter((courseDocument) => courseDocument.core);
}

function courseOneDocuments() {
  return courseBundle.documents.filter(belongsToCourseOne);
}

function learningSequenceDocuments() {
  const sequenceIds = courseBundle.course.learningSequenceIds;
  if (!Array.isArray(sequenceIds) || !sequenceIds.length) {
    return coreDocuments();
  }
  const sequence = sequenceIds
    .map((documentId) => documentById.get(documentId))
    .filter(Boolean);
  return sequence.length ? sequence : coreDocuments();
}

function resumeDocument() {
  const sequence = learningSequenceDocuments();
  const lastDocument = documentById.get(state.lastDocument);
  const lastIsActionable = sequence.some(
    (courseDocument) => courseDocument.id === lastDocument?.id,
  );
  if (
    lastIsActionable &&
    (!isDocumentComplete(lastDocument) ||
      (requiresPracticalSelfCheck(lastDocument) &&
        !isPracticalPassed(lastDocument)))
  ) {
    return lastDocument;
  }
  return (
    sequence.find((courseDocument) => !isDocumentComplete(courseDocument)) ||
    sequence.find(
      (courseDocument) =>
        requiresPracticalSelfCheck(courseDocument) &&
        !isPracticalPassed(courseDocument),
    ) ||
    sequence[0] ||
    null
  );
}

function pagerDocumentsFor(courseDocument) {
  const sequence = learningSequenceDocuments();
  if (
    sequence.some(
      (candidateDocument) => candidateDocument.id === courseDocument.id,
    )
  ) {
    return sequence;
  }
  const group = courseBundle.groups.find(
    (candidate) => candidate.id === courseDocument.group,
  );
  return (group?.documents || [])
    .map((documentId) => documentById.get(documentId))
    .filter(Boolean);
}

function learningPositionLabel(courseDocument) {
  const group = courseBundle.groups.find((candidate) => candidate.id === courseDocument.group);
  if (!group) return courseDocument.group;
  const position = group.documents.indexOf(courseDocument.id);
  if (courseDocument.kind === "foundation" && position >= 0) {
    return `Foundation ${position + 1} of ${group.documents.length}`;
  }
  if (courseDocument.kind === "module" && position >= 0) {
    return `Module ${position + 1} of ${group.documents.length}`;
  }
  return groupTitle(courseDocument.group);
}

function practiceHoursFor(courseDocument) {
  const explicit =
    courseDocument?.estimatedPracticeHours || courseDocument?.practiceHours;
  if (
    Number.isFinite(explicit?.minimum) &&
    Number.isFinite(explicit?.maximum) &&
    explicit.minimum > 0 &&
    explicit.maximum >= explicit.minimum
  ) {
    return {
      minimum: Math.round(explicit.minimum),
      maximum: Math.round(explicit.maximum),
    };
  }

  const estimate = String(courseDocument?.markdown || "").match(
    /^## Estimated time\s*\n+\s*(\d+)\s*[\u2013-]\s*(\d+)\s+hours\b/im,
  );
  if (estimate) {
    return {
      minimum: Number.parseInt(estimate[1], 10),
      maximum: Number.parseInt(estimate[2], 10),
    };
  }
  return FOUNDATION_PRACTICE_HOURS[courseDocument?.id] || null;
}

function effortFor(courseDocument) {
  const readingMinutes = Math.max(1, Math.ceil(courseDocument.wordCount / 210));
  const practiceHours = practiceHoursFor(courseDocument);
  return {
    readingMinutes,
    readingLabel: `Read: about ${readingMinutes} minute${readingMinutes === 1 ? "" : "s"}`,
    practiceLabel: practiceHours
      ? `Practice: ${practiceHours.minimum}\u2013${practiceHours.maximum} hours`
      : requiresPracticalSelfCheck(courseDocument)
        ? "Practice: plan several focused sessions"
        : null,
  };
}

function effortText(courseDocument) {
  const effort = effortFor(courseDocument);
  return [effort.readingLabel, effort.practiceLabel]
    .filter(Boolean)
    .join(" \u00b7 ");
}

function completedCoreCount() {
  return learningSequenceDocuments().filter((courseDocument) =>
    isDocumentComplete(courseDocument),
  ).length;
}

function practicalPassedCoreCount() {
  return learningSequenceDocuments().filter((courseDocument) =>
    isPracticalPassed(courseDocument),
  ).length;
}

function updateProgressUi() {
  const documents = learningSequenceDocuments();
  const completed = completedCoreCount();
  const practicalPassed = practicalPassedCoreCount();
  const percent = documents.length ? Math.round((completed / documents.length) * 100) : 0;
  const practicalPercent = documents.length
    ? Math.round((practicalPassed / documents.length) * 100)
    : 0;
  document.querySelector("#sidebar-progress-label").textContent = `${percent}% pages read`;
  document.querySelector("#sidebar-progress-count").textContent =
    `${completed} of ${documents.length} pages`;
  document.querySelector("#sidebar-progress-bar").style.width = `${percent}%`;
  const progress = document.querySelector(".progress-track");
  progress.setAttribute("aria-valuenow", String(percent));
  progress.setAttribute(
    "aria-valuetext",
    `${completed} of ${documents.length} Course 1 pages read`,
  );
  document.querySelector("#sidebar-practice-count").textContent =
    `${practicalPassed} of ${documents.length} self-checks`;
  document.querySelector("#sidebar-practice-bar").style.width =
    `${practicalPercent}%`;
  const practicalProgress = document.querySelector(".progress-track-practice");
  practicalProgress.setAttribute("aria-valuenow", String(practicalPercent));
  practicalProgress.setAttribute(
    "aria-valuetext",
    `${practicalPassed} of ${documents.length} practical tasks self-attested`,
  );
  document.querySelectorAll(".nav-document").forEach((button) => {
    const courseDocument = documentById.get(button.dataset.documentId);
    if (courseDocument) updateNavigationDocumentState(button, courseDocument);
  });
}

function updateNavigationDocumentState(button, courseDocument) {
  const complete = isDocumentComplete(courseDocument);
  const practicalPassed = isPracticalPassed(courseDocument);
  const needsReview = needsRevisionReview(courseDocument);
  const practiceNeedsReview = needsPracticalRevisionReview(courseDocument);
  button.classList.toggle("completed", complete);
  button.classList.toggle("practice-passed", practicalPassed);
  button.classList.toggle("needs-review", needsReview);
  button.classList.toggle("practice-needs-review", practiceNeedsReview);
  const status = complete
    ? "Page read"
    : needsReview
      ? "Read again"
      : "Page not read";
  const practiceStatus = requiresPracticalSelfCheck(courseDocument)
    ? practicalPassed
      ? " Practical self-check recorded."
      : practiceNeedsReview
        ? " Practical self-check needs review."
        : " Practical self-check not recorded."
    : "";
  const statusText = button.querySelector(".nav-document-status");
  if (statusText) statusText.textContent = ` — ${status}.${practiceStatus}`;
}

function renderCourseNavigation() {
  const navigation = document.querySelector("#course-nav");
  navigation.replaceChildren();

  for (const group of courseBundle.groups) {
    const groupDocuments = group.documents
      .map((id) => documentById.get(id))
      .filter((courseDocument) => belongsToCourseOne(courseDocument));
    if (!groupDocuments.length) continue;

    const wrapper = document.createElement("section");
    wrapper.className = "nav-group";
    wrapper.dataset.groupId = group.id;
    const expanded = state.expandedGroups.includes(group.id);
    const completedCount = groupDocuments.filter((courseDocument) =>
      isDocumentComplete(courseDocument),
    ).length;

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "nav-group-toggle";
    toggle.setAttribute("aria-expanded", String(expanded));
    toggle.innerHTML = `${iconSvg("chevron", "ui-icon chevron")}<strong>${escapeHtml(group.title)}</strong><small>${completedCount}/${groupDocuments.length} read</small>`;

    const list = document.createElement("ul");
    list.className = "nav-group-list";
    list.hidden = !expanded;

    toggle.addEventListener("click", () => {
      const willExpand = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(willExpand));
      list.hidden = !willExpand;
      state.expandedGroups = willExpand
        ? [...new Set([...state.expandedGroups, group.id])]
        : state.expandedGroups.filter((id) => id !== group.id);
      saveState();
    });

    for (const courseDocument of groupDocuments) {
      const item = document.createElement("li");
      const button = document.createElement("button");
      button.type = "button";
      button.className = "nav-document";
      button.dataset.documentId = courseDocument.id;
      button.innerHTML = `<span class="nav-check" aria-hidden="true">${iconSvg("check")}</span><span>${escapeHtml(courseDocument.title)}</span><span class="sr-only nav-document-status"></span>`;
      updateNavigationDocumentState(button, courseDocument);
      button.addEventListener("click", () => {
        navigateToDocument(courseDocument.id);
        closeSidebar();
      });
      item.append(button);
      list.append(item);
    }

    wrapper.append(toggle, list);
    navigation.append(wrapper);
  }
}

function showOnly(viewName) {
  Object.entries(views).forEach(([name, view]) => {
    view.hidden = name !== viewName;
  });
  document.querySelector("#loading-card").hidden = true;
  document.querySelectorAll(".bottom-nav button").forEach((button) => {
    const route = button.dataset.route;
    const selected =
      route === viewName ||
      (route === "course" && viewName === "reader") ||
      (route === "home" && viewName === "home");
    if (selected) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
  document.querySelectorAll(".sidebar-link[data-route]").forEach((button) => {
    if (button.dataset.route === viewName) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
}

function navigate(route) {
  flushPendingNote();
  pendingRouteFocus = true;
  const target = route.startsWith("#") ? route : `#${route}`;
  if (window.location.hash === target) {
    renderRoute();
  } else {
    window.location.hash = target;
  }
}

function navigateToDocument(id) {
  navigate(`doc=${encodeURIComponent(id)}`);
}

function renderHome() {
  showOnly("home");
  currentDocument = null;
  document.querySelectorAll(".nav-document").forEach((button) => {
    button.removeAttribute("aria-current");
  });

  const requiredDocs = learningSequenceDocuments();
  const completed = completedCoreCount();
  const practicalPassed = practicalPassedCoreCount();
  const foundationDocs = requiredDocs.filter((document) => document.group === "foundations");
  const moduleDocs = requiredDocs.filter((document) => document.group === "modules");
  const foundationCompleted = foundationDocs.filter(isDocumentComplete).length;
  const moduleCompleted = moduleDocs.filter(isDocumentComplete).length;
  const percent = requiredDocs.length
    ? Math.round((completed / requiredDocs.length) * 100)
    : 0;
  const practicalPercent = requiredDocs.length
    ? Math.round((practicalPassed / requiredDocs.length) * 100)
    : 0;
  const foundationPercent = foundationDocs.length
    ? Math.round((foundationCompleted / foundationDocs.length) * 100)
    : 0;
  const modulePercent = moduleDocs.length
    ? Math.round((moduleCompleted / moduleDocs.length) * 100)
    : 0;
  const resume = resumeDocument();
  const nextDocuments = learningSequenceDocuments()
    .filter(
      (document) =>
        !isDocumentComplete(document) ||
        (requiresPracticalSelfCheck(document) && !isPracticalPassed(document)),
    )
    .slice(0, 3);
  const estimatedHours = courseBundle.course.estimatedHours;
  const effortLabel =
    Number.isFinite(estimatedHours?.minimum) &&
    Number.isFinite(estimatedHours?.maximum)
      ? `${estimatedHours.minimum}–${estimatedHours.maximum} total course hours`
      : null;
  const verifiedDate = new Date(`${courseBundle.course.verifiedThrough}T12:00:00`);
  const ageDays = Number.isNaN(verifiedDate.getTime())
    ? null
    : Math.floor((Date.now() - verifiedDate.getTime()) / 86400000);
  const freshness =
    ageDays === null
      ? "Verification date unavailable"
      : ageDays > 84
        ? "Live audit due before continuing"
        : "Within the regular review window";

  views.home.innerHTML = `
    <section class="hero">
      <div class="hero-copy">
        <span class="hero-kicker"><span aria-hidden="true"></span>Course 1 of the consultant path</span>
        <h1>Learn to build one <em>controlled business workflow.</em></h1>
        <p>Start from zero technical knowledge. Learn to inspect the work, choose a small problem with clear limits, build fixed, rule-based checks, design a bounded artificial intelligence (AI) contribution, test its controls with an offline stand-in, and keep a human responsible for every consequential decision. Course 1 makes no live AI call.</p>
        <div class="hero-actions">
          <button class="button" type="button" data-home-action="resume">
            <span>${resume ? `Continue: ${escapeHtml(resume.title)}` : "Start the course"}</span>
            ${iconSvg("arrow")}
          </button>
          <button class="button button-quiet" type="button" data-home-action="career">See the full career sequence</button>
        </div>
        <div class="proof-chips" aria-label="Course safeguards">
          <span>${iconSvg("layers")}${courseBundle.course.foundationCount} foundations</span>
          <span>${iconSvg("document")}${courseBundle.course.moduleCount} implementation modules</span>
          ${effortLabel ? `<span>${iconSvg("clock")}${escapeHtml(effortLabel)}</span>` : ""}
          <span>${iconSvg("shield")}Made-up practice data only</span>
        </div>
      </div>
      <div class="workflow-preview" aria-label="Final practice project workflow preview">
        <div class="workflow-preview-header">
          <span>Made-up final practice project</span>
          <small><span aria-hidden="true"></span>Human-controlled</small>
        </div>
        <ol>
          <li>
            <span class="workflow-stage-icon">${iconSvg("document")}</span>
            <span><small>01 · Observe</small><strong>Fictional operations data</strong></span>
          </li>
          <li>
            <span class="workflow-stage-icon">${iconSvg("extract")}</span>
            <span><small>02 · Check</small><strong>Problems found by fixed rules</strong></span>
          </li>
          <li>
            <span class="workflow-stage-icon">${iconSvg("review")}</span>
            <span><small>03 · Explain</small><strong>Evidence-linked offline mock summary</strong></span>
          </li>
          <li>
            <span class="workflow-stage-icon workflow-stage-approved">${iconSvg("shield")}</span>
            <span><small>04 · Decide</small><strong>Human review and action</strong></span>
          </li>
        </ol>
        <div class="workflow-assurance">${iconSvg("check")}Cannot send or change anything outside the practice files</div>
      </div>
    </section>
    <section class="practice-contract practice-contract-home" aria-label="Beginner practice method">
      ${practiceContractMarkup()}
    </section>
    <section class="progress-overview" aria-label="Course progress summary">
      <article class="progress-card progress-card-main">
        <div class="progress-ring" style="--progress: ${percent}" role="img" aria-label="${completed} of ${requiredDocs.length} required Course 1 pages read">
          <span><strong>${percent}%</strong><small>pages read</small></span>
        </div>
        <div>
          <span class="eyebrow">Reading progress</span>
          <h2>${completed === requiredDocs.length ? "All required pages read" : completed ? "Keep reading and building" : "Your foundation is ready"}</h2>
          <p>${completed} of ${requiredDocs.length} required pages read, including readiness and setup. Reading every page does not mean you passed the practical work.</p>
        </div>
      </article>
      <article class="progress-card practice-progress-card">
        <span class="progress-card-icon progress-card-icon-gold">${iconSvg("shield")}</span>
        <div>
          <span>Practical self-checks</span>
          <strong>${practicalPassed}<small> / ${requiredDocs.length}</small></strong>
        </div>
        <div class="mini-progress mini-progress-gold" role="progressbar" aria-label="Practical task self-checks" aria-valuemin="0" aria-valuemax="${requiredDocs.length}" aria-valuenow="${practicalPassed}" aria-valuetext="${practicalPassed} of ${requiredDocs.length} required practical tasks self-attested"><span style="width:${practicalPercent}%"></span></div>
        <p class="practice-progress-note">Your own checklist record, not an independent assessment.</p>
      </article>
      <article class="progress-card">
        <span class="progress-card-icon">${iconSvg("layers")}</span>
        <div>
          <span>Foundations read</span>
          <strong>${foundationCompleted}<small> / ${foundationDocs.length}</small></strong>
        </div>
        <div class="mini-progress" aria-hidden="true"><span style="width:${foundationPercent}%"></span></div>
      </article>
      <article class="progress-card">
        <span class="progress-card-icon progress-card-icon-gold">${iconSvg("document")}</span>
        <div>
          <span>Modules read</span>
          <strong>${moduleCompleted}<small> / ${moduleDocs.length}</small></strong>
        </div>
        <div class="mini-progress mini-progress-gold" aria-hidden="true"><span style="width:${modulePercent}%"></span></div>
      </article>
    </section>
    <div class="dashboard-grid">
      <section class="dashboard-card next-steps-card">
        <span class="eyebrow">Your next steps</span>
        <h2>${nextDocuments.length ? "One clear step at a time" : "Reading and self-check records complete"}</h2>
        <ul class="path-list">
          ${
            nextDocuments.length
              ? nextDocuments
                  .map(
                    (document, index) => `
                      <li>
                        <button class="${index === 0 ? "path-featured" : ""}" type="button" data-document-id="${escapeAttribute(document.id)}">
                          <span class="path-number">${String(index + 1).padStart(2, "0")}</span>
                          <span><small>${escapeHtml(learningPositionLabel(document))} · ${escapeHtml(effortText(document))}${isDocumentComplete(document) ? " · practice self-check still open" : ""}</small><strong>${escapeHtml(document.title)}</strong></span>
                          ${iconSvg("arrow")}
                        </button>
                      </li>`,
                  )
                  .join("")
              : '<li><p>Your reading and practical self-check records are complete. Use Module 9’s scored rubric and evidence checks before claiming the Course 1 capability. A self-check is not external proof or consultant readiness.</p></li>'
          }
        </ul>
      </section>
      <section class="dashboard-card freshness-card">
        <div class="freshness-heading">
          <span class="freshness-icon">${iconSvg("shield")}</span>
          <span class="version-chip">Version ${escapeHtml(courseBundle.course.version)}</span>
        </div>
        <span class="eyebrow">Research review date</span>
        <h2>${escapeHtml(freshness)}</h2>
        <time datetime="${escapeAttribute(courseBundle.course.verifiedThrough)}">${escapeHtml(courseBundle.course.verifiedThrough)}</time>
        <p>Review the research sources after important legal, security, artificial intelligence model, or supplier changes.</p>
        <button class="button button-quiet" type="button" data-home-action="updates">${iconSvg("shield")}Open update centre</button>
      </section>
    </div>
    <section class="course-overview" aria-labelledby="module-overview-title">
      <div class="section-heading">
        <div>
          <span class="eyebrow">Course 1 at a glance</span>
          <h2 id="module-overview-title">${courseBundle.course.moduleCount} modules, one controlled implementation</h2>
        </div>
        <p>The foundations teach the tools. The modules apply them in the order a responsible implementation should happen.</p>
      </div>
      <div class="module-card-grid">
        ${moduleDocs
          .map((courseDocument, index) => {
            const complete = isDocumentComplete(courseDocument);
            const practicePassed = isPracticalPassed(courseDocument);
            const revised =
              needsRevisionReview(courseDocument) ||
              needsPracticalRevisionReview(courseDocument);
            const status = !complete
              ? revised
                ? "Read revision"
                : "Ready to read"
              : practicePassed
                ? "Practice checked"
                : revised
                  ? "Recheck practice"
                  : "Practice open";
            return `
              <button class="module-card${complete && practicePassed ? " complete" : ""}${revised ? " revised" : ""}" type="button" data-document-id="${escapeAttribute(courseDocument.id)}">
                <span class="module-card-top">
                  <span class="module-number">${String(index + 1).padStart(2, "0")}</span>
                  <span class="module-status">${escapeHtml(status)}</span>
                </span>
                <strong>${escapeHtml(courseDocument.title.replace(/^Module \d+\s*[—-]\s*/, ""))}</strong>
                <small>${escapeHtml(effortText(courseDocument))} · revision ${escapeHtml(courseDocument.revision)}</small>
                ${iconSvg("arrow")}
              </button>
            `;
          })
          .join("")}
      </div>
    </section>
    <section class="career-bridge">
      <div>
        <span class="eyebrow">Keep the boundary clear</span>
        <h2>This course is the technical foundation—not your entire consulting career.</h2>
        <p>Later courses separately cover finding valuable problems, client implementation and adoption, rules and oversight, commercial practice, and supervised market entry.</p>
      </div>
      <button class="button" type="button" data-home-action="career">Open career sequence ${iconSvg("arrow")}</button>
    </section>
  `;

  views.home.querySelector('[data-home-action="resume"]')?.addEventListener("click", () => {
    if (resume) navigateToDocument(resume.id);
  });
  views.home
    .querySelectorAll('[data-home-action="career"]')
    .forEach((button) => button.addEventListener("click", () => navigate("career")));
  views.home
    .querySelector('[data-home-action="updates"]')
    ?.addEventListener("click", () => navigate("settings"));
  views.home.querySelectorAll("[data-document-id]").forEach((button) => {
    button.addEventListener("click", () => navigateToDocument(button.dataset.documentId));
  });
  document.title = `${courseBundle.course.shortTitle} — ${courseBundle.course.title}`;
}

function renderCareer() {
  showOnly("career");
  currentDocument = null;
  document.querySelectorAll(".nav-document").forEach((button) => {
    button.removeAttribute("aria-current");
  });

  const career = courseBundle.career;
  const rawCareerSummary = String(career.summary);
  const careerSummary = /progressive web app \(PWA\)/i.test(rawCareerSummary)
    ? rawCareerSummary
    : rawCareerSummary.replace(/\bPWA\b/, "progressive web app (PWA)");
  const nextLesson = resumeDocument();
  const careerStatusLabel = (course) => {
    if (course.status === "current") return "Current · taught here";
    if (course.status === "prototype-capstone-available") {
      return "Optional advanced capstone available";
    }
    return "Proposed separate course";
  };
  const careerActionMarkup = (course) => {
    if (course.status === "current") {
      return `<button class="button" type="button" data-career-action="course">${nextLesson ? `Continue ${escapeHtml(learningPositionLabel(nextLesson))}` : "Open Course 1"} ${iconSvg("arrow")}</button>`;
    }
    if (
      course.status === "prototype-capstone-available" &&
      documentById.has(course.prototypeDocumentId)
    ) {
      return `
        <details class="later-course-disclosure">
          <summary>Show the later-course prototype link</summary>
          <p>This material is not part of Course 1. Open it intentionally from the Career path when its prerequisites and timing make sense.</p>
          <button class="button" type="button" data-career-action="prototype" data-document-id="${escapeHtml(course.prototypeDocumentId)}">Open the later-course prototype ${iconSvg("arrow")}</button>
        </details>
      `;
    }
    return "";
  };

  views.career.innerHTML = `
    <section class="career-hero">
      <span class="hero-kicker"><span aria-hidden="true"></span>Artificial intelligence (AI) for small and medium-sized enterprises (SMEs)</span>
      <h1>${escapeHtml(career.targetRole)}</h1>
      <p>${escapeHtml(careerSummary)}</p>
      <div class="career-role-card">
        <span>${iconSvg("shield")}</span>
        <div>
          <small>The durable professional value</small>
          <strong>${escapeHtml(courseBundle.program.durableValue)}</strong>
        </div>
      </div>
    </section>
    <section class="career-roadmap" aria-labelledby="career-roadmap-title">
      <div class="section-heading">
        <div>
          <span class="eyebrow">Courses 1–6</span>
          <h2 id="career-roadmap-title">Build proof in a deliberate order</h2>
        </div>
        <p>Course 1 is taught in full. Later-course lessons stay out of the Course 1 menu and search. Course 4 has one optional advanced prototype that you can intentionally reveal here; the remaining later-course content is still a curriculum plan, not a completed qualification or promise of work.</p>
      </div>
      <ol class="career-course-list">
        ${career.courses
          .map(
            (course) => `
              <li class="career-course-card${course.status === "current" ? " current" : ""}${course.status === "prototype-capstone-available" ? " prototype" : ""}">
                <span class="career-sequence">${String(course.sequence).padStart(2, "0")}</span>
                <div class="career-course-copy">
                  <span class="career-status">${careerStatusLabel(course)}</span>
                  <h3>${escapeHtml(course.title)}</h3>
                  <p>${escapeHtml(course.purpose)}</p>
                  <div class="exit-evidence">
                    <small>Advance when you can show</small>
                    <strong>${escapeHtml(course.exitEvidence)}</strong>
                  </div>
                  ${careerActionMarkup(course)}
                </div>
              </li>
            `,
          )
          .join("")}
      </ol>
    </section>
    <section class="career-detail-grid">
      <article class="career-detail-card specialization-card">
        <span class="eyebrow">Optional specialisation</span>
        ${career.optionalSpecializations
          .map(
            (specialization) => `
              <h2>${escapeHtml(specialization.title)}</h2>
              <span class="version-chip">${escapeHtml(specialization.status.replaceAll("-", " "))}</span>
              <p>${escapeHtml(specialization.purpose)}</p>
            `,
          )
          .join("")}
      </article>
      <article class="career-detail-card">
        <span class="eyebrow">Checks before you advance</span>
        <h2>Do not skip the controls</h2>
        <ul class="career-gate-list">
          ${career.readinessGates
            .map((gate) => `<li>${iconSvg("check")}<span>${escapeHtml(gate)}</span></li>`)
            .join("")}
        </ul>
      </article>
    </section>
    <section class="pace-card">
      <div>
        <span class="eyebrow">A sustainable pace</span>
        <h2>Design for the capacity you will have later</h2>
      </div>
      <dl>
        <div><dt>For now</dt><dd>${escapeHtml(career.suggestedPace.currentCapacity)}</dd></div>
        <div><dt>After recovery</dt><dd>${escapeHtml(career.suggestedPace.laterCapacity)}</dd></div>
        <div><dt>When to advance</dt><dd>${escapeHtml(career.suggestedPace.sequenceRule)}</dd></div>
      </dl>
    </section>
  `;

  views.career
    .querySelector('[data-career-action="course"]')
    ?.addEventListener("click", () => {
      if (nextLesson) navigateToDocument(nextLesson.id);
      else navigate("home");
    });
  views.career
    .querySelectorAll('[data-career-action="prototype"]')
    .forEach((button) => {
      button.addEventListener("click", () => {
        if (documentById.has(button.dataset.documentId)) {
          navigateToDocument(button.dataset.documentId);
        }
      });
    });
  document.title = `Career sequence — ${courseBundle.program.title}`;
}

function setDocumentPager(button, document, direction) {
  if (!document) {
    button.disabled = true;
    button.replaceChildren();
    return;
  }
  button.disabled = false;
  const isNext = direction === "Next";
  button.innerHTML = `
    <span class="pager-direction">
      ${isNext ? "" : iconSvg("arrow", "ui-icon arrow-back")}
      <small>${escapeHtml(direction)}</small>
      ${isNext ? iconSvg("arrow") : ""}
    </span>
    <strong>${escapeHtml(document.title)}</strong>
  `;
  button.onclick = () => navigateToDocument(document.id);
}

function wireCourseLinks(container, courseDocument) {
  container.querySelectorAll("a[href]").forEach((link) => {
    const href = link.getAttribute("href");
    if (!href || href === "#unsafe-link") {
      if (href === "#unsafe-link") {
        link.removeAttribute("href");
        link.title = "Unsafe link removed";
      }
      return;
    }
    if (/^(https?:|mailto:)/i.test(href)) return;

    if (href.startsWith("#")) {
      link.addEventListener("click", (event) => {
        const target = document.getElementById(href.slice(1));
        if (target) {
          event.preventDefault();
          target.scrollIntoView({ block: "start" });
        }
      });
      return;
    }

    try {
      const resolvedUrl = new URL(
        href,
        `https://course.invalid/${courseDocument.sourcePath}`,
      );
      const resolvedPath = decodeURIComponent(resolvedUrl.pathname.replace(/^\//, ""));
      const linkedDocument = documentByPath.get(resolvedPath);
      if (linkedDocument) {
        link.addEventListener("click", (event) => {
          event.preventDefault();
          navigateToDocument(linkedDocument.id);
          if (resolvedUrl.hash) {
            window.setTimeout(() => {
              document.getElementById(resolvedUrl.hash.slice(1))?.scrollIntoView({
                block: "start",
              });
            }, 50);
          }
        });
      } else {
        link.href = `${config.repositoryUrl}/blob/main/${resolvedPath}`;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
      }
    } catch {
      link.removeAttribute("href");
    }
  });
}

function wireCodeCopy(container) {
  container.querySelectorAll(".copy-code").forEach((button) => {
    button.addEventListener("click", async () => {
      const code = button.nextElementSibling?.textContent || "";
      try {
        await navigator.clipboard.writeText(code);
        button.textContent = "Copied";
        showToast("Code copied. Read it before running it.");
        window.setTimeout(() => {
          button.textContent = "Copy";
        }, 1800);
      } catch {
        showToast("Copy was blocked. Select the code manually.");
      }
    });
  });
}

function renderDocument(id) {
  const courseDocument = documentById.get(id);
  if (!courseDocument) {
    navigate("home");
    return;
  }

  showOnly("reader");
  currentDocument = courseDocument;
  state.lastDocument = id;
  const routeStateSaved = saveState();

  document.querySelector("#reader-group").textContent = groupTitle(courseDocument.group);
  document.querySelector("#reader-title").textContent = courseDocument.title;
  const requiredDocs = learningSequenceDocuments();
  const requiredPosition = requiredDocs.findIndex(
    (document) => document.id === courseDocument.id,
  );
  const belongsToCurrentCourse =
    courseDocument.courseId === courseBundle.course.id;
  const effort = effortFor(courseDocument);
  const lessonPosition =
    requiredPosition >= 0
      ? `Required page ${requiredPosition + 1} of ${requiredDocs.length}`
      : `${groupTitle(courseDocument.group)} page`;
  document.querySelector("#reader-meta").innerHTML = `
    <span class="reader-effort-reading">${iconSvg("clock")}${escapeHtml(effort.readingLabel)}</span>
    ${effort.practiceLabel ? `<span class="reader-effort-practice">${iconSvg("layers")}${escapeHtml(effort.practiceLabel)}</span>` : ""}
    <span>${iconSvg("layers")}${escapeHtml(learningPositionLabel(courseDocument))}</span>
    <span title="${escapeAttribute(lessonPosition)}">${iconSvg("document")}Revision ${escapeHtml(courseDocument.revision)}</span>
    ${
      belongsToCurrentCourse
        ? ""
        : `<span class="reader-course-boundary">${iconSvg("shield")}Optional Course ${escapeHtml(String(courseBundle.career.courses.find((course) => course.id === courseDocument.courseId)?.sequence || ""))} page · does not affect Course 1 reading or practice records</span>`
    }
  `;
  const content = document.querySelector("#reader-content");
  content.innerHTML = renderCourseMarkdown(courseDocument.markdown);
  wireCourseLinks(content, courseDocument);
  wireCodeCopy(content);

  const completeButton = document.querySelector("#complete-button");
  const isComplete = isDocumentComplete(courseDocument);
  const revised = needsRevisionReview(courseDocument);
  completeButton.setAttribute("aria-pressed", String(isComplete));
  completeButton.querySelector("span:last-child").textContent =
    !belongsToCurrentCourse
      ? isComplete
        ? "Page read"
        : revised
          ? "Mark page read again"
          : "Mark page read"
      : isComplete
        ? "Page read"
        : revised
          ? "Mark page read again"
          : "Mark page read";

  const practiceContract = document.querySelector("#practice-contract-reader");
  const showPracticeContract =
    requiresPracticalSelfCheck(courseDocument) ||
    courseDocument.group === "course-4-capstone";
  practiceContract.hidden = !showPracticeContract;
  if (showPracticeContract) {
    practiceContract.innerHTML = practiceContractMarkup({ compact: true });
  }

  const practicalPanel = document.querySelector("#practical-pass-panel");
  const practicalButton = document.querySelector("#practical-pass-button");
  const showPracticalPass = requiresPracticalSelfCheck(courseDocument);
  const practicalPassed = isPracticalPassed(courseDocument);
  const practicalNeedsReview = needsPracticalRevisionReview(courseDocument);
  practicalPanel.hidden = !showPracticalPass;
  practicalButton.setAttribute("aria-pressed", String(practicalPassed));
  practicalButton.querySelector("span:last-child").textContent = practicalPassed
    ? "Practical self-check recorded"
    : practicalNeedsReview
      ? "Recheck and record the revised practical task"
      : "I passed every practice criterion";

  const checkpoint =
    courseDocument.checkpoint ||
    courseBundle.course.checkpoints?.find(
      (candidate) => candidate.lessonId === courseDocument.id,
    );
  const checkpointAlert = document.querySelector("#checkpoint-alert");
  checkpointAlert.hidden = !checkpoint;
  if (checkpoint) {
    document.querySelector("#checkpoint-title").textContent =
      checkpoint.title || "Course checkpoint";
    document.querySelector("#checkpoint-message").textContent =
      checkpoint.message || "Pause and verify your evidence before continuing.";
    document.querySelector("#checkpoint-update-button").hidden =
      checkpoint.action !== "check-updates";
  }
  const revisionAlert = document.querySelector("#revision-alert");
  revisionAlert.hidden = !(revised || practicalNeedsReview);
  const note = document.querySelector("#learner-note");
  note.value = state.notes[id] || "";
  setNoteSaveStatus(
    routeStateSaved ? "Saved locally" : "Not saved on this device",
    { error: !routeStateSaved },
  );

  const pagerDocuments = pagerDocumentsFor(courseDocument);
  const position = pagerDocuments.findIndex((document) => document.id === id);
  setDocumentPager(
    document.querySelector("#previous-document"),
    pagerDocuments[position - 1],
    "Previous",
  );
  setDocumentPager(
    document.querySelector("#next-document"),
    pagerDocuments[position + 1],
    "Next",
  );

  document.querySelectorAll(".nav-document").forEach((button) => {
    if (button.dataset.documentId === id) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });

  const courseSequence = courseBundle.career.courses.find(
    (course) => course.id === courseDocument.courseId,
  )?.sequence;
  document.title = `${courseDocument.title} — Course ${courseSequence || 1}`;
  window.scrollTo({ top: 0, behavior: "instant" });
}

function searchDocuments(query) {
  const normalised = query.trim().toLowerCase();
  if (!normalised) return [];
  const terms = normalised.split(/\s+/).filter(Boolean);
  return courseOneDocuments()
    .map((document) => {
      const title = document.title.toLowerCase();
      const text = document.searchableText.toLowerCase();
      let score = 0;
      for (const term of terms) {
        if (title.includes(term)) score += 30;
        const occurrences = text.split(term).length - 1;
        score += Math.min(occurrences, 12);
      }
      if (!terms.every((term) => title.includes(term) || text.includes(term))) score = 0;
      return { document, score, firstIndex: text.indexOf(terms[0]) };
    })
    .filter((result) => result.score > 0)
    .sort((a, b) => b.score - a.score || a.document.order - b.document.order)
    .slice(0, 30);
}

function highlightedSnippet(text, query, index) {
  const start = Math.max(0, index - 80);
  const end = Math.min(text.length, start + 230);
  const excerpt = `${start > 0 ? "…" : ""}${text.slice(start, end)}${end < text.length ? "…" : ""}`;
  const escaped = escapeHtml(excerpt);
  const escapedQuery = escapeHtml(query.trim());
  if (!escapedQuery) return escaped;
  const expression = new RegExp(
    `(${escapedQuery.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`,
    "ig",
  );
  return escaped.replace(expression, "<mark>$1</mark>");
}

function renderSearchResults() {
  const query = document.querySelector("#search-input").value;
  const results = searchDocuments(query);
  const summary = document.querySelector("#search-summary");
  const container = document.querySelector("#search-results");
  container.replaceChildren();

  if (!query.trim()) {
    summary.textContent = "Type a term or question fragment.";
    return;
  }

  summary.textContent = results.length
    ? `${results.length} matching Course 1 page${results.length === 1 ? "" : "s"}`
    : "No Course 1 pages matched. Try a shorter or plainer term.";

  for (const result of results) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "search-result";
    button.innerHTML = `
      <small>${escapeHtml(groupTitle(result.document.group))}</small>
      <strong>${escapeHtml(result.document.title)}</strong>
      <span>${highlightedSnippet(result.document.searchableText, query.split(/\s+/)[0], result.firstIndex)}</span>
    `;
    button.addEventListener("click", () => navigateToDocument(result.document.id));
    container.append(button);
  }
}

function renderSearch() {
  showOnly("search");
  currentDocument = null;
  document.title = "Search — Course 1";
  window.setTimeout(() => document.querySelector("#search-input").focus(), 0);
}

function applyAppearance() {
  document.documentElement.dataset.theme = state.theme;
  const systemIsDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const dark = state.theme === "dark" || (state.theme === "system" && systemIsDark);
  document.querySelector("#theme-color-meta").content = dark ? "#0d1917" : "#f6f3ec";
  document.documentElement.style.setProperty("--reader-scale", state.fontSize / 100);
  document.querySelector("#font-size").value = String(state.fontSize);
  document.querySelector("#font-size-output").value = `${state.fontSize}%`;
  document.querySelectorAll("[data-theme-value]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.themeValue === state.theme));
  });
}

function renderSettings() {
  showOnly("settings");
  currentDocument = null;
  document.querySelector("#settings-course-version").textContent =
    `Version ${courseBundle.course.version}`;
  document.querySelector("#settings-verified-date").textContent =
    courseBundle.course.verifiedThrough;
  document.querySelector("#settings-build-id").textContent = config.buildId;
  document.querySelector("#last-update-check").textContent = state.lastUpdateCheck
    ? new Date(state.lastUpdateCheck).toLocaleString()
    : "Not yet";
  applyAppearance();
  document.title = "Settings — Course 1";
}

function renderRoute() {
  if (!courseBundle) return;
  flushPendingNote();
  closeSidebar();
  const route = window.location.hash.replace(/^#/, "") || "home";
  if (route.startsWith("doc=")) {
    renderDocument(decodeURIComponent(route.slice(4)));
  } else if (route === "career") {
    renderCareer();
  } else if (route === "search") {
    renderSearch();
  } else if (route === "settings") {
    renderSettings();
  } else {
    renderHome();
  }
  // A hash change can come from our buttons, browser history, or a copied URL.
  // Reset once now and once after the browser's built-in fragment scrolling,
  // because route names such as #settings can also match an element ID.
  const resetRouteScroll = () => window.scrollTo({ top: 0, behavior: "instant" });
  resetRouteScroll();
  window.setTimeout(resetRouteScroll, 0);
  if (pendingRouteFocus) {
    window.setTimeout(() => {
      const activeView = Object.values(views).find((view) => !view.hidden);
      const heading = activeView?.querySelector("h1");
      if (!heading) return;
      const hadTabIndex = heading.hasAttribute("tabindex");
      if (!hadTabIndex) heading.setAttribute("tabindex", "-1");
      heading.focus({ preventScroll: true });
      if (!hadTabIndex) {
        heading.addEventListener(
          "blur",
          () => heading.removeAttribute("tabindex"),
          { once: true },
        );
      }
    }, 0);
  }
  pendingRouteFocus = false;
}

function openSidebar() {
  document.body.classList.add("sidebar-open");
  document.querySelector("#menu-button").setAttribute("aria-expanded", "true");
  for (const selector of [".topbar", ".main", ".bottom-nav"]) {
    document.querySelector(selector).inert = true;
  }
  document.querySelector("#sidebar-close-button")?.focus();
}

function closeSidebar({ restoreFocus = false } = {}) {
  const wasOpen = document.body.classList.contains("sidebar-open");
  document.body.classList.remove("sidebar-open");
  document.querySelector("#menu-button").setAttribute("aria-expanded", "false");
  for (const selector of [".topbar", ".main", ".bottom-nav"]) {
    document.querySelector(selector).inert = false;
  }
  if (wasOpen && restoreFocus) document.querySelector("#menu-button").focus();
}

function trapSidebarFocus(event) {
  if (event.key !== "Tab" || !document.body.classList.contains("sidebar-open")) return;
  const sidebar = document.querySelector("#course-sidebar");
  const focusable = [...sidebar.querySelectorAll("button:not([disabled]), a[href]")]
    .filter((element) => !element.closest("[hidden]") && element.getClientRects().length);
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable.at(-1);
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

function showToast(message, duration = 2800) {
  const toast = document.querySelector("#toast");
  window.clearTimeout(toastTimer);
  toast.textContent = message;
  toast.hidden = false;
  toastTimer = window.setTimeout(() => {
    toast.hidden = true;
  }, duration);
}

function updateConnectionStatus() {
  const online = navigator.onLine;
  document.querySelector("#connection-pill").classList.toggle("offline", !online);
  document.querySelector("#connection-text").textContent = online ? "Online" : "Offline";
  if (!online) showToast("Offline: using the course saved on this device.");
}

function toggleCompleted() {
  if (!currentDocument) return;
  flushPendingNote();
  const wasComplete = isDocumentComplete(currentDocument);
  const index = state.completed.indexOf(currentDocument.id);
  if (wasComplete) {
    if (index >= 0) state.completed.splice(index, 1);
    delete state.completionRevisions[currentDocument.id];
  } else {
    if (index < 0) state.completed.push(currentDocument.id);
    state.completionRevisions[currentDocument.id] =
      completionRevisionFor(currentDocument);
  }
  const saved = saveState();
  renderCourseNavigation();
  updateProgressUi();
  renderDocument(currentDocument.id);
  showToast(
    saved
      ? wasComplete
        ? "Page marked unread. Your separate practical self-check was not changed."
        : "Page marked read. Practical work is recorded separately."
      : "The lesson changed on screen but could not be saved on this device.",
  );
}

function togglePracticalPassed() {
  if (!currentDocument || !requiresPracticalSelfCheck(currentDocument)) return;
  flushPendingNote();
  const wasPassed = isPracticalPassed(currentDocument);
  const index = state.practicalPassed.indexOf(currentDocument.id);
  if (wasPassed) {
    if (index >= 0) state.practicalPassed.splice(index, 1);
    delete state.practicalPassRevisions[currentDocument.id];
  } else {
    if (index < 0) state.practicalPassed.push(currentDocument.id);
    state.practicalPassRevisions[currentDocument.id] =
      completionRevisionFor(currentDocument);
  }
  const saved = saveState();
  renderCourseNavigation();
  updateProgressUi();
  renderDocument(currentDocument.id);
  showToast(
    saved
      ? wasPassed
        ? "Practical self-check removed."
        : "Practical self-check recorded. This is not an independent assessment."
      : "The practical self-check changed on screen but could not be saved.",
    wasPassed ? 2800 : 4200,
  );
}

function setNoteSaveStatus(message, { error = false } = {}) {
  const status = document.querySelector("#note-save-status");
  status.textContent = message;
  status.classList.toggle("save-error", error);
}

function captureNoteInState(documentId, noteValue) {
  if (!documentId) return;
  const note = String(noteValue).slice(0, 50000);
  if (note.trim()) state.notes[documentId] = note;
  else delete state.notes[documentId];
  noteStorageDirty = true;
}

function persistPendingNote() {
  window.clearTimeout(noteTimer);
  noteTimer = null;
  const saved = saveState();
  setNoteSaveStatus(
    saved ? "Saved locally" : "Not saved on this device",
    { error: !saved },
  );
  return saved;
}

function flushPendingNote() {
  if (noteTimer === null && !noteStorageDirty) return true;
  return persistPendingNote();
}

function showInstallDialog() {
  const dialog = document.querySelector("#install-dialog");
  if (typeof dialog.showModal === "function") dialog.showModal();
  else dialog.setAttribute("open", "");
}

function exportProgress() {
  flushPendingNote();
  const payload = {
    exportType: "ai-workflow-course-progress",
    exportedAt: new Date().toISOString(),
    bundleSchemaVersion: courseBundle.schemaVersion,
    courseId: courseBundle.course.id,
    courseVersion: courseBundle.course.version,
    state,
  };
  const blob = new Blob([`${JSON.stringify(payload, null, 2)}\n`], {
    type: "application/json",
  });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `ai-workflow-course-progress-${new Date().toISOString().slice(0, 10)}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
  showToast("Progress backup exported.");
}

function sanitiseV2StateForCurrentCourse(rawState) {
  const imported = normaliseV2State(rawState);
  imported.completed = imported.completed.filter((id) => documentById.has(id));
  imported.completionRevisions = Object.fromEntries(
    Object.entries(imported.completionRevisions)
      .filter(
        ([id, revision]) =>
          documentById.has(id) &&
          typeof revision === "string" &&
          /^\d{4}-\d{2}-\d{2}(?:\|practice:[1-9]\d*)?$/.test(revision),
      ),
  );
  imported.practicalPassed = imported.practicalPassed.filter((id) => {
    const courseDocument = documentById.get(id);
    return requiresPracticalSelfCheck(courseDocument);
  });
  imported.practicalPassRevisions = Object.fromEntries(
    Object.entries(imported.practicalPassRevisions)
      .filter(
        ([id, revision]) =>
          requiresPracticalSelfCheck(documentById.get(id)) &&
          typeof revision === "string" &&
          /^\d{4}-\d{2}-\d{2}(?:\|practice:[1-9]\d*)?$/.test(revision),
      ),
  );
  imported.notes = Object.fromEntries(
    Object.entries(imported.notes)
      .filter(([id, note]) => documentById.has(id) && typeof note === "string")
      .map(([id, note]) => [id, note.slice(0, 50000)]),
  );
  imported.archivedLegacyNotes = Object.fromEntries(
    Object.entries(imported.archivedLegacyNotes)
      .filter(([_id, note]) => typeof note === "string")
      .map(([id, note]) => [id, note.slice(0, 50000)]),
  );
  imported.lastDocument = documentById.has(imported.lastDocument)
    ? imported.lastDocument
    : null;
  imported.theme = ["system", "light", "dark"].includes(imported.theme)
    ? imported.theme
    : "system";
  imported.fontSize = Math.max(90, Math.min(125, Number(imported.fontSize) || 100));
  imported.expandedGroups = imported.expandedGroups.filter((groupId) =>
    courseBundle.groups.some((group) => group.id === groupId),
  );
  return imported;
}

function replaceState(replacement) {
  for (const key of Object.keys(state)) delete state[key];
  Object.assign(state, replacement);
}

async function importProgress(file) {
  try {
    const payload = JSON.parse(await file.text());
    if (
      payload?.exportType !== "ai-workflow-course-progress" ||
      payload?.courseId !== courseBundle.course.id ||
      ![1, STATE_SCHEMA_VERSION].includes(payload?.state?.schemaVersion)
    ) {
      throw new Error("Not a supported course progress backup.");
    }
    if (!window.confirm("Replace progress and notes on this device with this backup?")) {
      return;
    }
    const imported =
      payload.state.schemaVersion === 1
        ? migrateSchemaV1(payload.state)
        : sanitiseV2StateForCurrentCourse(payload.state);
    const previousState = JSON.parse(JSON.stringify(state));
    replaceState(imported);
    if (!saveState()) {
      replaceState(previousState);
      throw new Error(
        "The backup was not imported because this browser could not save it.",
      );
    }
    renderCourseNavigation();
    updateProgressUi();
    applyAppearance();
    renderRoute();
    showToast(
      payload.state.schemaVersion === 1
        ? "Older backup imported and migrated."
        : "Progress backup imported.",
    );
  } catch (error) {
    showToast(error.message || "That backup could not be imported.", 4500);
  } finally {
    document.querySelector("#import-progress").value = "";
  }
}

function resetProgress() {
  const confirmed = window.confirm(
    "Reset every page-read mark, practical self-check, private note, and reading preference on this device? This cannot be undone unless you exported a backup.",
  );
  if (!confirmed) return;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    showToast(
      "Nothing was reset because this browser could not change local storage.",
      4500,
    );
    return;
  }
  replaceState(defaultState());
  renderCourseNavigation();
  updateProgressUi();
  applyAppearance();
  navigate("home");
  showToast("Local reading, practical self-checks, and notes reset.");
}

function showUpdateReady(worker = serviceWorkerRegistration?.waiting) {
  if (!worker) return;
  pendingUpdateWorker = worker;
  document.querySelector("#update-banner").hidden = false;
}

async function checkForUpdates({ manual = false } = {}) {
  if (!serviceWorkerRegistration) {
    if (manual) showToast("This browser cannot check for offline course updates.");
    return;
  }
  if (!navigator.onLine) {
    if (manual) showToast("You are offline. Reconnect before checking.");
    return;
  }

  const now = Date.now();
  if (!manual && now - lastAutomaticUpdateCheck < 5 * 60 * 1000) return;
  lastAutomaticUpdateCheck = now;

  const buttons = [
    document.querySelector("#update-button"),
    document.querySelector("#settings-update-button"),
    document.querySelector("#checkpoint-update-button"),
  ].filter(Boolean);
  buttons.forEach((button) => {
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
  });

  try {
    await serviceWorkerRegistration.update();
    await new Promise((resolve) => window.setTimeout(resolve, 1100));
    state.lastUpdateCheck = new Date().toISOString();
    saveState();
    if (serviceWorkerRegistration.waiting) {
      showUpdateReady();
    } else if (manual) {
      const response = await fetch(`${config.basePath}version.json`, {
        cache: "no-store",
      });
      const latest = response.ok ? await response.json() : null;
      if (latest?.buildId && latest.buildId !== config.buildId) {
        showToast("A published course update is available; preparing it…");
        await serviceWorkerRegistration.update();
      } else {
        showToast(`You have the latest published course (Version ${config.courseVersion}).`);
      }
    }
    if (!views.settings.hidden) renderSettings();
  } catch {
    if (manual) showToast("The update check failed. Your saved course still works.", 4200);
  } finally {
    buttons.forEach((button) => {
      button.disabled = false;
      button.removeAttribute("aria-busy");
    });
  }
}

async function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) return;
  try {
    serviceWorkerRegistration = await navigator.serviceWorker.register(
      `${config.basePath}sw.js`,
      {
        scope: config.basePath,
        updateViaCache: "none",
      },
    );

    if (serviceWorkerRegistration.waiting && navigator.serviceWorker.controller) {
      showUpdateReady(serviceWorkerRegistration.waiting);
    }

    serviceWorkerRegistration.addEventListener("updatefound", () => {
      const installingWorker = serviceWorkerRegistration.installing;
      if (!installingWorker) return;
      installingWorker.addEventListener("statechange", () => {
        if (
          installingWorker.state === "installed" &&
          navigator.serviceWorker.controller
        ) {
          showUpdateReady(installingWorker);
        }
      });
    });

    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (reloadingForUpdate) return;
      reloadingForUpdate = true;
      window.location.reload();
    });

    window.setTimeout(() => checkForUpdates(), 900);
  } catch {
    showToast("Offline installation is unavailable; the online course still works.", 4200);
  }
}

function setCourseShellReady() {
  document.querySelector("#app-shell").setAttribute("aria-busy", "false");
  document.querySelector("#menu-button").disabled = false;
  document.querySelectorAll("[data-route]").forEach((button) => {
    button.disabled = false;
  });
  document.querySelector(".brand").setAttribute("aria-disabled", "false");
}

function wireEvents() {
  window.addEventListener("hashchange", renderRoute);
  window.addEventListener("online", updateConnectionStatus);
  window.addEventListener("offline", updateConnectionStatus);
  window.addEventListener("focus", () => checkForUpdates());
  window.addEventListener("pagehide", flushPendingNote);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") flushPendingNote();
    else checkForUpdates();
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (state.theme === "system") applyAppearance();
  });

  document.querySelector("#menu-button").addEventListener("click", () => {
    if (document.body.classList.contains("sidebar-open")) closeSidebar({ restoreFocus: true });
    else openSidebar();
  });
  document
    .querySelector("#sidebar-close-button")
    .addEventListener("click", () => closeSidebar({ restoreFocus: true }));
  document
    .querySelector("#sidebar-scrim")
    .addEventListener("click", () => closeSidebar({ restoreFocus: true }));
  document.addEventListener("keydown", (event) => {
    trapSidebarFocus(event);
    if (event.key === "Escape" && document.body.classList.contains("sidebar-open")) {
      closeSidebar({ restoreFocus: true });
    }
    if (event.key === "Escape" && !views.search.hidden) {
      document.querySelector("#search-input").value = "";
      renderSearchResults();
    }
  });

  document.querySelector(".brand").addEventListener("click", (event) => {
    event.preventDefault();
    navigate("home");
  });

  document.querySelectorAll("[data-route]").forEach((button) => {
    button.addEventListener("click", () => {
      if (button.dataset.route === "course") {
        if (window.matchMedia("(max-width: 920px)").matches) openSidebar();
        else {
          const target = resumeDocument();
          if (target) navigateToDocument(target.id);
        }
      } else {
        navigate(button.dataset.route);
      }
    });
  });

  document.querySelector("#complete-button").addEventListener("click", toggleCompleted);
  document
    .querySelector("#practical-pass-button")
    .addEventListener("click", togglePracticalPassed);
  document.querySelector("#learner-note").addEventListener("input", (event) => {
    const documentId = currentDocument?.id;
    if (!documentId) return;
    captureNoteInState(documentId, event.currentTarget.value);
    window.clearTimeout(noteTimer);
    setNoteSaveStatus("Saving…");
    noteTimer = window.setTimeout(persistPendingNote, 450);
  });
  document.querySelector("#search-input").addEventListener("input", renderSearchResults);

  document.querySelectorAll("[data-theme-value]").forEach((button) => {
    button.addEventListener("click", () => {
      state.theme = button.dataset.themeValue;
      saveState();
      applyAppearance();
    });
  });
  document.querySelector("#font-size").addEventListener("input", (event) => {
    state.fontSize = Number(event.target.value);
    saveState();
    applyAppearance();
  });

  document.querySelector("#install-button").addEventListener("click", showInstallDialog);
  document.querySelector("#native-install-button").addEventListener("click", async () => {
    if (!deferredInstallPrompt) return;
    deferredInstallPrompt.prompt();
    await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
    document.querySelector("#native-install-button").hidden = true;
    document.querySelector("#install-dialog").close();
  });
  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferredInstallPrompt = event;
    document.querySelector("#native-install-button").hidden = false;
  });

  document.querySelector("#export-progress").addEventListener("click", exportProgress);
  document.querySelector("#import-progress").addEventListener("change", (event) => {
    const [file] = event.target.files;
    if (file) importProgress(file);
  });
  document.querySelector("#reset-progress").addEventListener("click", resetProgress);

  [
    document.querySelector("#update-button"),
    document.querySelector("#settings-update-button"),
    document.querySelector("#checkpoint-update-button"),
  ].forEach((button) =>
    button.addEventListener("click", () => checkForUpdates({ manual: true })),
  );
  document.querySelector("#update-later").addEventListener("click", () => {
    document.querySelector("#update-banner").hidden = true;
  });
  document.querySelector("#apply-update").addEventListener("click", () => {
    const waiting = pendingUpdateWorker || serviceWorkerRegistration?.waiting;
    if (!waiting) {
      document.querySelector("#update-banner").hidden = true;
      showToast("The update is no longer waiting. Checking again…");
      checkForUpdates({ manual: true });
      return;
    }
    document.querySelector("#apply-update").disabled = true;
    waiting.postMessage({ type: "SKIP_WAITING" });
  });
}

async function initialise() {
  applyAppearance();
  updateConnectionStatus();

  try {
    const response = await fetch(`${config.basePath}course-content.json`);
    if (!response.ok) throw new Error(`Course bundle returned ${response.status}`);
    courseBundle = await response.json();
    if (
      courseBundle?.schemaVersion !== 2 ||
      !Array.isArray(courseBundle.documents) ||
      !Array.isArray(courseBundle.groups) ||
      !Array.isArray(courseBundle.career?.courses)
    ) {
      throw new Error("Course bundle has an unsupported shape");
    }
    documentById = new Map(
      courseBundle.documents.map((courseDocument) => [
        courseDocument.id,
        courseDocument,
      ]),
    );
    documentByPath = new Map(
      courseBundle.documents.map((courseDocument) => [
        courseDocument.sourcePath,
        courseDocument,
      ]),
    );
    if (pendingLegacyState) {
      replaceState(migrateSchemaV1(pendingLegacyState));
      pendingLegacyState = null;
    } else {
      replaceState(sanitiseV2StateForCurrentCourse(state));
    }
    saveState();
    renderCourseNavigation();
    updateProgressUi();
    wireEvents();
    setCourseShellReady();
    renderRoute();
    if (state.migration?.fromSchemaVersion === 1) {
      const archivedCount = state.migration.unmappedNoteIds?.length || 0;
      showToast(
        archivedCount
          ? `Progress migrated. ${archivedCount} old note${archivedCount === 1 ? "" : "s"} kept in the backup archive.`
          : "Your existing progress was migrated to the revised course.",
        5200,
      );
      state.migration = null;
      saveState();
    }
    await registerServiceWorker();
  } catch (error) {
    const loading = document.querySelector("#loading-card");
    loading.innerHTML = `
      <div>
        <strong>The course could not open.</strong>
        <p>${escapeHtml(error.message || "Unknown loading error")}. Reconnect and reload; no local progress was deleted.</p>
        <button class="button" type="button" id="reload-app">Reload course</button>
      </div>
    `;
    document.querySelector("#reload-app").addEventListener("click", () => {
      window.location.reload();
    });
  }
}

initialise();
