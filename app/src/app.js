import {
  escapeAttribute,
  escapeHtml,
  renderMarkdown as renderCourseMarkdown,
} from "./markdown.js";

const config = window.__COURSE_APP__;
const STORAGE_KEY = "ai-workflow-course-state-v1";
const STATE_SCHEMA_VERSION = 2;
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
  } catch {
    showToast("Progress could not be saved on this device.");
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
  if (
    !courseDocument.core ||
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

function groupTitle(groupId) {
  return courseBundle.groups.find((group) => group.id === groupId)?.title || groupId;
}

function coreDocuments() {
  return courseBundle.documents.filter((courseDocument) => courseDocument.core);
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

function completedCoreCount() {
  return coreDocuments().filter((courseDocument) =>
    isDocumentComplete(courseDocument),
  ).length;
}

function updateProgressUi() {
  const documents = coreDocuments();
  const completed = completedCoreCount();
  const percent = documents.length ? Math.round((completed / documents.length) * 100) : 0;
  document.querySelector("#sidebar-progress-label").textContent = `${percent}% complete`;
  document.querySelector("#sidebar-progress-count").textContent =
    `${completed} of ${documents.length} lessons`;
  document.querySelector("#sidebar-progress-bar").style.width = `${percent}%`;
  const progress = document.querySelector(".progress-track");
  progress.setAttribute("aria-valuenow", String(percent));
  progress.setAttribute("aria-valuetext", `${percent}% of Course 1 complete`);
  document.querySelectorAll(".nav-document").forEach((button) => {
    const courseDocument = documentById.get(button.dataset.documentId);
    button.classList.toggle(
      "completed",
      Boolean(courseDocument && isDocumentComplete(courseDocument)),
    );
    button.classList.toggle(
      "needs-review",
      Boolean(courseDocument && needsRevisionReview(courseDocument)),
    );
  });
}

function renderCourseNavigation() {
  const navigation = document.querySelector("#course-nav");
  navigation.replaceChildren();

  for (const group of courseBundle.groups) {
    const wrapper = document.createElement("section");
    wrapper.className = "nav-group";
    wrapper.dataset.groupId = group.id;
    const expanded = state.expandedGroups.includes(group.id);
    const groupDocuments = group.documents
      .map((id) => documentById.get(id))
      .filter(Boolean);
    const completedCount = groupDocuments.filter((courseDocument) =>
      isDocumentComplete(courseDocument),
    ).length;

    const toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "nav-group-toggle";
    toggle.setAttribute("aria-expanded", String(expanded));
    toggle.innerHTML = `${iconSvg("chevron", "ui-icon chevron")}<strong>${escapeHtml(group.title)}</strong><small>${completedCount}/${groupDocuments.length}</small>`;

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
      if (isDocumentComplete(courseDocument)) button.classList.add("completed");
      if (needsRevisionReview(courseDocument)) button.classList.add("needs-review");
      button.innerHTML = `<span class="nav-check" aria-hidden="true">${iconSvg("check")}</span><span>${escapeHtml(courseDocument.title)}</span>`;
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

  const core = coreDocuments();
  const completed = completedCoreCount();
  const foundationDocs = core.filter((document) => document.group === "foundations");
  const moduleDocs = core.filter((document) => document.group === "modules");
  const foundationCompleted = foundationDocs.filter(isDocumentComplete).length;
  const moduleCompleted = moduleDocs.filter(isDocumentComplete).length;
  const percent = core.length ? Math.round((completed / core.length) * 100) : 0;
  const foundationPercent = foundationDocs.length
    ? Math.round((foundationCompleted / foundationDocs.length) * 100)
    : 0;
  const modulePercent = moduleDocs.length
    ? Math.round((moduleCompleted / moduleDocs.length) * 100)
    : 0;
  const resume =
    documentById.get(state.lastDocument) ||
    core.find((document) => !isDocumentComplete(document)) ||
    core[0];
  const nextDocuments = core
    .filter((document) => !isDocumentComplete(document))
    .slice(0, 3);
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
        <p>Start from zero technical knowledge. Learn to inspect the work, choose a small problem with clear limits, build fixed, rule-based checks, add artificial intelligence (AI) only where it helps, and keep a human responsible for every consequential decision.</p>
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
            <span><small>03 · Explain</small><strong>Evidence-linked AI summary</strong></span>
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
        <div class="progress-ring" style="--progress: ${percent}" role="img" aria-label="${percent}% of the core course complete">
          <span><strong>${percent}%</strong><small>complete</small></span>
        </div>
        <div>
          <span class="eyebrow">Course 1 progress</span>
          <h2>${completed ? "Keep building your evidence" : "Your foundation is ready"}</h2>
          <p>${completed} of ${core.length} core lessons complete</p>
        </div>
      </article>
      <article class="progress-card">
        <span class="progress-card-icon">${iconSvg("layers")}</span>
        <div>
          <span>Foundations</span>
          <strong>${foundationCompleted}<small> / ${foundationDocs.length}</small></strong>
        </div>
        <div class="mini-progress" aria-hidden="true"><span style="width:${foundationPercent}%"></span></div>
      </article>
      <article class="progress-card">
        <span class="progress-card-icon progress-card-icon-gold">${iconSvg("document")}</span>
        <div>
          <span>Modules</span>
          <strong>${moduleCompleted}<small> / ${moduleDocs.length}</small></strong>
        </div>
        <div class="mini-progress mini-progress-gold" aria-hidden="true"><span style="width:${modulePercent}%"></span></div>
      </article>
    </section>
    <div class="dashboard-grid">
      <section class="dashboard-card next-steps-card">
        <span class="eyebrow">Your next steps</span>
        <h2>${nextDocuments.length ? "One clear step at a time" : "Core course complete"}</h2>
        <ul class="path-list">
          ${
            nextDocuments.length
              ? nextDocuments
                  .map(
                    (document, index) => `
                      <li>
                        <button class="${index === 0 ? "path-featured" : ""}" type="button" data-document-id="${escapeAttribute(document.id)}">
                          <span class="path-number">${String(index + 1).padStart(2, "0")}</span>
                          <span><small>${escapeHtml(learningPositionLabel(document))} · about ${Math.max(1, Math.ceil(document.wordCount / 210))} minutes</small><strong>${escapeHtml(document.title)}</strong></span>
                          ${iconSvg("arrow")}
                        </button>
                      </li>`,
                  )
                  .join("")
              : '<li><p>Use Module 9’s final pass checklist, keep the documented manual way of working available, and continue reviewing course updates.</p></li>'
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
            const revised = needsRevisionReview(courseDocument);
            const status = complete ? "Complete" : revised ? "Review revision" : "Ready";
            return `
              <button class="module-card${complete ? " complete" : ""}${revised ? " revised" : ""}" type="button" data-document-id="${escapeAttribute(courseDocument.id)}">
                <span class="module-card-top">
                  <span class="module-number">${String(index + 1).padStart(2, "0")}</span>
                  <span class="module-status">${escapeHtml(status)}</span>
                </span>
                <strong>${escapeHtml(courseDocument.title.replace(/^Module \d+\s*[—-]\s*/, ""))}</strong>
                <small>About ${Math.max(1, Math.ceil(courseDocument.wordCount / 210))} minutes · revision ${escapeHtml(courseDocument.revision)}</small>
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
  const nextLesson =
    coreDocuments().find((courseDocument) => !isDocumentComplete(courseDocument)) ||
    coreDocuments()[0];

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
        <p>Only Course 1 is taught in this learning app. The later cards are a curriculum plan, not completed qualifications or promises of work.</p>
      </div>
      <ol class="career-course-list">
        ${career.courses
          .map(
            (course) => `
              <li class="career-course-card${course.status === "current" ? " current" : ""}">
                <span class="career-sequence">${String(course.sequence).padStart(2, "0")}</span>
                <div class="career-course-copy">
                  <span class="career-status">${course.status === "current" ? "Current · taught here" : "Proposed separate course"}</span>
                  <h3>${escapeHtml(course.title)}</h3>
                  <p>${escapeHtml(course.purpose)}</p>
                  <div class="exit-evidence">
                    <small>Advance when you can show</small>
                    <strong>${escapeHtml(course.exitEvidence)}</strong>
                  </div>
                  ${
                    course.status === "current"
                      ? `<button class="button" type="button" data-career-action="course">${nextLesson ? `Continue ${escapeHtml(learningPositionLabel(nextLesson))}` : "Open Course 1"} ${iconSvg("arrow")}</button>`
                      : ""
                  }
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
  saveState();

  document.querySelector("#reader-group").textContent = groupTitle(courseDocument.group);
  document.querySelector("#reader-title").textContent = courseDocument.title;
  const core = coreDocuments();
  const corePosition = core.findIndex((document) => document.id === courseDocument.id);
  const lessonPosition =
    corePosition >= 0
      ? `Core lesson ${corePosition + 1} of ${core.length}`
      : `${groupTitle(courseDocument.group)} page`;
  document.querySelector("#reader-meta").innerHTML = `
    <span>${iconSvg("clock")}About ${Math.max(1, Math.ceil(courseDocument.wordCount / 210))} minutes</span>
    <span>${iconSvg("layers")}${escapeHtml(learningPositionLabel(courseDocument))}</span>
    <span title="${escapeAttribute(lessonPosition)}">${iconSvg("document")}Revision ${escapeHtml(courseDocument.revision)}</span>
  `;
  const content = document.querySelector("#reader-content");
  content.innerHTML = renderCourseMarkdown(courseDocument.markdown);
  wireCourseLinks(content, courseDocument);
  wireCodeCopy(content);

  const completeButton = document.querySelector("#complete-button");
  const isComplete = isDocumentComplete(courseDocument);
  const revised = needsRevisionReview(courseDocument);
  completeButton.setAttribute("aria-pressed", String(isComplete));
  completeButton.querySelector("span:last-child").textContent = isComplete
    ? "Completed"
    : revised
      ? "Mark reviewed"
      : "Mark complete";

  const practiceContract = document.querySelector("#practice-contract-reader");
  practiceContract.hidden = !courseDocument.core;
  if (courseDocument.core) {
    practiceContract.innerHTML = practiceContractMarkup({ compact: true });
  }

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
  document.querySelector("#revision-alert").hidden = !revised;
  const note = document.querySelector("#learner-note");
  note.value = state.notes[id] || "";
  document.querySelector("#note-save-status").textContent = "Saved locally";

  const group = courseBundle.groups.find(
    (candidate) => candidate.id === courseDocument.group,
  );
  const pagerDocuments = courseDocument.core
    ? core
    : (group?.documents || [])
        .map((documentId) => documentById.get(documentId))
        .filter(Boolean);
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

  document.title = `${courseDocument.title} — Course 1`;
  window.scrollTo({ top: 0, behavior: "instant" });
}

function searchDocuments(query) {
  const normalised = query.trim().toLowerCase();
  if (!normalised) return [];
  const terms = normalised.split(/\s+/).filter(Boolean);
  return courseBundle.documents
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
    ? `${results.length} matching course page${results.length === 1 ? "" : "s"}`
    : "No course pages matched. Try a shorter or plainer term.";

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
  if (pendingRouteFocus) {
    window.scrollTo({ top: 0, behavior: "instant" });
    if (route !== "search") {
      window.setTimeout(() => {
        document.querySelector("#main-content").focus({ preventScroll: true });
      }, 0);
    }
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
  saveState();
  renderCourseNavigation();
  updateProgressUi();
  renderDocument(currentDocument.id);
  showToast(wasComplete ? "Marked incomplete." : "Lesson marked complete.");
}

function saveCurrentNote() {
  if (!currentDocument) return;
  const note = document.querySelector("#learner-note").value;
  if (note.trim()) state.notes[currentDocument.id] = note;
  else delete state.notes[currentDocument.id];
  saveState();
  document.querySelector("#note-save-status").textContent = "Saved locally";
}

function showInstallDialog() {
  const dialog = document.querySelector("#install-dialog");
  if (typeof dialog.showModal === "function") dialog.showModal();
  else dialog.setAttribute("open", "");
}

function exportProgress() {
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
    replaceState(imported);
    saveState();
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
    "Reset every completion mark, private note, and reading preference on this device? This cannot be undone unless you exported a backup.",
  );
  if (!confirmed) return;
  localStorage.removeItem(STORAGE_KEY);
  replaceState(defaultState());
  renderCourseNavigation();
  updateProgressUi();
  applyAppearance();
  renderHome();
  showToast("Local progress and notes reset.");
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

function wireEvents() {
  window.addEventListener("hashchange", renderRoute);
  window.addEventListener("online", updateConnectionStatus);
  window.addEventListener("offline", updateConnectionStatus);
  window.addEventListener("focus", () => checkForUpdates());
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") checkForUpdates();
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
          const target =
            documentById.get(state.lastDocument) ||
            coreDocuments().find((courseDocument) => !isDocumentComplete(courseDocument)) ||
            coreDocuments()[0];
          if (target) navigateToDocument(target.id);
        }
      } else {
        navigate(button.dataset.route);
      }
    });
  });

  document.querySelector("#complete-button").addEventListener("click", toggleCompleted);
  document.querySelector("#learner-note").addEventListener("input", () => {
    window.clearTimeout(noteTimer);
    document.querySelector("#note-save-status").textContent = "Saving…";
    noteTimer = window.setTimeout(saveCurrentNote, 450);
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
  wireEvents();

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
    renderRoute();
    if (state.migration?.fromSchemaVersion === 1) {
      const archivedCount = state.migration.unmappedNoteIds?.length || 0;
      showToast(
        archivedCount
          ? `Progress migrated. ${archivedCount} old note${archivedCount === 1 ? "" : "s"} kept in the backup archive.`
          : "Your existing progress was migrated to the revised course.",
        5200,
      );
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
