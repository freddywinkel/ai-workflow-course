const config = window.__COURSE_APP__;
const STORAGE_KEY = "ai-workflow-course-state-v1";
const CORE_GROUPS = new Set(["foundations", "weeks"]);
const views = {
  home: document.querySelector("#home-view"),
  reader: document.querySelector("#reader-view"),
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

function loadState() {
  const fallback = {
    schemaVersion: 1,
    completed: [],
    notes: {},
    lastDocument: null,
    theme: "system",
    fontSize: 100,
    lastUpdateCheck: null,
    expandedGroups: ["foundations"],
  };
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || "null");
    if (!parsed || parsed.schemaVersion !== 1) return fallback;
    return {
      ...fallback,
      ...parsed,
      completed: Array.isArray(parsed.completed) ? parsed.completed : [],
      notes: parsed.notes && typeof parsed.notes === "object" ? parsed.notes : {},
      expandedGroups: Array.isArray(parsed.expandedGroups)
        ? parsed.expandedGroups
        : fallback.expandedGroups,
    };
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

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}

function safeLink(value) {
  const href = String(value).trim();
  if (
    href.startsWith("#") ||
    href.startsWith("/") ||
    href.startsWith("./") ||
    href.startsWith("../") ||
    /^[a-zA-Z0-9_.-]+(?:\/[a-zA-Z0-9_.#?&=%-]+)*$/.test(href)
  ) {
    return href;
  }
  try {
    const url = new URL(href);
    if (["https:", "http:", "mailto:"].includes(url.protocol)) return href;
  } catch {
    // Invalid or unsafe links become inert text targets.
  }
  return "#unsafe-link";
}

function renderInline(rawValue) {
  const tokens = [];
  let value = String(rawValue);

  value = value.replace(/`([^`\n]+)`/g, (_match, code) => {
    const token = `\u0000CODE${tokens.length}\u0000`;
    tokens.push(`<code>${escapeHtml(code)}</code>`);
    return token;
  });

  value = value.replace(/\[([^\]\n]+)\]\(([^)\n]+)\)/g, (_match, label, rawHref) => {
    const href = rawHref.trim().replace(/\s+"[^"]*"$/, "");
    const safe = safeLink(href);
    const external = /^https?:\/\//i.test(safe);
    const token = `\u0000LINK${tokens.length}\u0000`;
    tokens.push(
      `<a href="${escapeAttribute(safe)}"${external ? ' target="_blank" rel="noopener noreferrer"' : ""}>${escapeHtml(label)}</a>`,
    );
    return token;
  });

  value = escapeHtml(value)
    .replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>")
    .replace(/__([^_\n]+)__/g, "<strong>$1</strong>")
    .replace(/(^|[^\w])\*([^*\n]+)\*(?!\w)/g, "$1<em>$2</em>")
    .replace(/(^|[^\w])_([^_\n]+)_(?!\w)/g, "$1<em>$2</em>");

  return value.replace(/\u0000(?:CODE|LINK)(\d+)\u0000/g, (_match, index) => {
    return tokens[Number(index)] || "";
  });
}

function headingId(value) {
  return value
    .toLowerCase()
    .replace(/<[^>]+>/g, "")
    .replace(/&[a-z0-9#]+;/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function isBlockStart(lines, index) {
  const line = lines[index] || "";
  const next = lines[index + 1] || "";
  return (
    !line.trim() ||
    /^```/.test(line.trim()) ||
    /^#{1,6}\s+/.test(line) ||
    /^>\s?/.test(line) ||
    /^[-*_]{3,}\s*$/.test(line.trim()) ||
    /^\s*[-*+]\s+/.test(line) ||
    /^\s*\d+\.\s+/.test(line) ||
    (line.includes("|") && /^\s*\|?[\s:|-]+\|[\s:|-|]*\s*$/.test(next))
  );
}

function splitTableRow(line) {
  return line
    .trim()
    .replace(/^\||\|$/g, "")
    .split("|")
    .map((cell) => cell.trim());
}

function renderMarkdown(markdown) {
  const lines = String(markdown).replace(/\r\n?/g, "\n").split("\n");
  const output = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    const trimmed = line.trim();

    if (!trimmed) {
      index += 1;
      continue;
    }

    const fence = trimmed.match(/^```([a-zA-Z0-9_+-]*)\s*$/);
    if (fence) {
      const language = fence[1].toLowerCase();
      const codeLines = [];
      index += 1;
      while (index < lines.length && !/^```\s*$/.test(lines[index].trim())) {
        codeLines.push(lines[index]);
        index += 1;
      }
      if (index < lines.length) index += 1;
      const isCommand =
        /^(powershell|shell|bash|sh|console|terminal|cmd)$/.test(language) ||
        codeLines.some((codeLine) =>
          /^(git|python|py|docker|npm|npx|winget|curl|pytest|uvicorn)\b/.test(
            codeLine.trim(),
          ),
        );
      if (isCommand) {
        output.push(
          '<p class="command-warning"><span aria-hidden="true">◇</span><span>Beginner check: confirm the current folder and understand the command before copying it.</span></p>',
        );
      }
      output.push(
        `<div class="code-block"><button class="copy-code" type="button" aria-label="Copy code block">Copy</button><pre${language ? ` data-language="${escapeAttribute(language)}"` : ""}><code>${escapeHtml(codeLines.join("\n"))}</code></pre></div>`,
      );
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const rendered = renderInline(heading[2]);
      output.push(`<h${level} id="${headingId(rendered)}">${rendered}</h${level}>`);
      index += 1;
      continue;
    }

    if (/^[-*_]{3,}\s*$/.test(trimmed)) {
      output.push("<hr>");
      index += 1;
      continue;
    }

    if (
      line.includes("|") &&
      index + 1 < lines.length &&
      /^\s*\|?[\s:|-]+\|[\s:|-|]*\s*$/.test(lines[index + 1])
    ) {
      const headers = splitTableRow(line);
      index += 2;
      const rows = [];
      while (index < lines.length && lines[index].includes("|") && lines[index].trim()) {
        rows.push(splitTableRow(lines[index]));
        index += 1;
      }
      output.push(
        `<div class="table-wrap" tabindex="0" aria-label="Scrollable table"><table><thead><tr>${headers.map((cell) => `<th scope="col">${renderInline(cell)}</th>`).join("")}</tr></thead><tbody>${rows
          .map(
            (row) =>
              `<tr>${headers.map((_header, cellIndex) => `<td>${renderInline(row[cellIndex] || "")}</td>`).join("")}</tr>`,
          )
          .join("")}</tbody></table></div>`,
      );
      continue;
    }

    if (/^>\s?/.test(line)) {
      const quoteLines = [];
      while (index < lines.length && /^>\s?/.test(lines[index])) {
        quoteLines.push(lines[index].replace(/^>\s?/, ""));
        index += 1;
      }
      output.push(`<blockquote><p>${renderInline(quoteLines.join(" "))}</p></blockquote>`);
      continue;
    }

    const unordered = line.match(/^\s*[-*+]\s+(.+)$/);
    const ordered = line.match(/^\s*\d+\.\s+(.+)$/);
    if (unordered || ordered) {
      const orderedList = Boolean(ordered);
      const items = [];
      const listPattern = orderedList ? /^\s*\d+\.\s+(.+)$/ : /^\s*[-*+]\s+(.+)$/;
      while (index < lines.length) {
        const match = lines[index].match(listPattern);
        if (!match) break;
        let item = match[1];
        const task = item.match(/^\[([ xX])\]\s+(.+)$/);
        if (task) {
          item = `<span class="markdown-task${task[1].toLowerCase() === "x" ? " checked" : ""}" aria-hidden="true">${iconSvg("check")}</span>${renderInline(task[2])}`;
        } else {
          item = renderInline(item);
        }
        items.push(`<li>${item}</li>`);
        index += 1;
      }
      output.push(`<${orderedList ? "ol" : "ul"}>${items.join("")}</${orderedList ? "ol" : "ul"}>`);
      continue;
    }

    const paragraph = [trimmed];
    index += 1;
    while (index < lines.length && !isBlockStart(lines, index)) {
      paragraph.push(lines[index].trim());
      index += 1;
    }
    output.push(`<p>${renderInline(paragraph.join(" "))}</p>`);
  }

  return output.join("\n");
}

function groupTitle(groupId) {
  return courseBundle.groups.find((group) => group.id === groupId)?.title || groupId;
}

function coreDocuments() {
  return courseBundle.documents.filter((document) => {
    if (document.group === "weeks") return true;
    return /^foundations\/\d{2}_/.test(document.sourcePath);
  });
}

function learningPositionLabel(courseDocument) {
  const foundationMatch = courseDocument.sourcePath.match(/^foundations\/(\d{2})_/);
  if (foundationMatch) {
    return `Foundation ${Number(foundationMatch[1])} of ${courseBundle.course.foundationCount}`;
  }
  const weekMatch = courseDocument.sourcePath.match(/^weeks\/WEEK_(\d{2})\.md$/);
  if (weekMatch) {
    return `Week ${Number(weekMatch[1])} of ${courseBundle.course.weekCount}`;
  }
  return groupTitle(courseDocument.group);
}

function completedCoreCount() {
  const completed = new Set(state.completed);
  return coreDocuments().filter((document) => completed.has(document.id)).length;
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
  progress.setAttribute("aria-valuetext", `${percent}% of core course complete`);
  document
    .querySelectorAll(".nav-document")
    .forEach((button) =>
      button.classList.toggle("completed", state.completed.includes(button.dataset.documentId)),
    );
}

function renderCourseNavigation() {
  const navigation = document.querySelector("#course-nav");
  navigation.replaceChildren();
  const completed = new Set(state.completed);

  for (const group of courseBundle.groups) {
    const wrapper = document.createElement("section");
    wrapper.className = "nav-group";
    wrapper.dataset.groupId = group.id;
    const expanded = state.expandedGroups.includes(group.id);
    const groupDocuments = group.documents
      .map((id) => documentById.get(id))
      .filter(Boolean);
    const completedCount = groupDocuments.filter((document) =>
      completed.has(document.id),
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
      if (completed.has(courseDocument.id)) button.classList.add("completed");
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
  const weekDocs = core.filter((document) => document.group === "weeks");
  const foundationCompleted = foundationDocs.filter((document) =>
    state.completed.includes(document.id),
  ).length;
  const weekCompleted = weekDocs.filter((document) =>
    state.completed.includes(document.id),
  ).length;
  const percent = core.length ? Math.round((completed / core.length) * 100) : 0;
  const foundationPercent = foundationDocs.length
    ? Math.round((foundationCompleted / foundationDocs.length) * 100)
    : 0;
  const weekPercent = weekDocs.length
    ? Math.round((weekCompleted / weekDocs.length) * 100)
    : 0;
  const resume =
    documentById.get(state.lastDocument) ||
    core.find((document) => !state.completed.includes(document.id)) ||
    core[0];
  const nextDocuments = core
    .filter((document) => !state.completed.includes(document.id))
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
        <span class="hero-kicker"><span aria-hidden="true"></span>Learn by building one bounded system</span>
        <h1>From zero coding knowledge to a <em>working document workflow.</em></h1>
        <p>Begin with the foundations, then build a source-grounded supplier-document workflow in twelve careful increments. AI drafts; a human always decides.</p>
        <div class="hero-actions">
          <button class="button" type="button" data-home-action="resume">
            <span>${resume ? `Continue: ${escapeHtml(resume.title)}` : "Start the course"}</span>
            ${iconSvg("arrow")}
          </button>
          <button class="button button-quiet" type="button" data-home-action="foundations">Explore the beginner path</button>
        </div>
        <div class="proof-chips" aria-label="Course safeguards">
          <span>${iconSvg("layers")}8 foundations</span>
          <span>${iconSvg("document")}12 build weeks</span>
          <span>${iconSvg("shield")}Synthetic data only</span>
        </div>
      </div>
      <div class="workflow-preview" aria-label="Capstone workflow preview">
        <div class="workflow-preview-header">
          <span>Capstone flow</span>
          <small><span aria-hidden="true"></span>Human-controlled</small>
        </div>
        <ol>
          <li>
            <span class="workflow-stage-icon">${iconSvg("document")}</span>
            <span><small>01 · Intake</small><strong>Source documents</strong></span>
          </li>
          <li>
            <span class="workflow-stage-icon">${iconSvg("extract")}</span>
            <span><small>02 · Structure</small><strong>Evidence-linked facts</strong></span>
          </li>
          <li>
            <span class="workflow-stage-icon">${iconSvg("review")}</span>
            <span><small>03 · Decide</small><strong>Human review</strong></span>
          </li>
          <li>
            <span class="workflow-stage-icon workflow-stage-approved">${iconSvg("shield")}</span>
            <span><small>04 · Release</small><strong>Approved memo</strong></span>
          </li>
        </ol>
        <div class="workflow-assurance">${iconSvg("check")}No action without approval</div>
      </div>
    </section>
    <section class="progress-overview" aria-label="Course progress summary">
      <article class="progress-card progress-card-main">
        <div class="progress-ring" style="--progress: ${percent}" role="img" aria-label="${percent}% of the core course complete">
          <span><strong>${percent}%</strong><small>complete</small></span>
        </div>
        <div>
          <span class="eyebrow">Overall journey</span>
          <h2>${completed ? "Keep building your proof" : "Your learning path is ready"}</h2>
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
          <span>Build weeks</span>
          <strong>${weekCompleted}<small> / ${weekDocs.length}</small></strong>
        </div>
        <div class="mini-progress mini-progress-gold" aria-hidden="true"><span style="width:${weekPercent}%"></span></div>
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
                          <span><small>${escapeHtml(learningPositionLabel(document))} · about ${Math.max(1, Math.ceil(document.wordCount / 210))} min</small><strong>${escapeHtml(document.title)}</strong></span>
                          ${iconSvg("arrow")}
                        </button>
                      </li>`,
                  )
                  .join("")
              : '<li><p>Use Week 12’s acceptance gate and keep the evergreen audit schedule active.</p></li>'
          }
        </ul>
      </section>
      <section class="dashboard-card freshness-card">
        <div class="freshness-heading">
          <span class="freshness-icon">${iconSvg("shield")}</span>
          <span class="version-chip">v${escapeHtml(courseBundle.course.version)}</span>
        </div>
        <span class="eyebrow">Source currency</span>
        <h2>${escapeHtml(freshness)}</h2>
        <time datetime="${escapeAttribute(courseBundle.course.verifiedThrough)}">${escapeHtml(courseBundle.course.verifiedThrough)}</time>
        <p>Run the live audit again before Week 7 and after material legal, security, or vendor changes.</p>
        <button class="button button-quiet" type="button" data-home-action="updates">${iconSvg("shield")}Open update centre</button>
      </section>
    </div>
  `;

  views.home.querySelector('[data-home-action="resume"]')?.addEventListener("click", () => {
    if (resume) navigateToDocument(resume.id);
  });
  views.home
    .querySelector('[data-home-action="foundations"]')
    ?.addEventListener("click", () => {
      const foundationIndex =
        courseBundle.documents.find(
          (document) => document.sourcePath === "foundations/README.md",
        ) || foundationDocs[0];
      if (foundationIndex) navigateToDocument(foundationIndex.id);
    });
  views.home
    .querySelector('[data-home-action="updates"]')
    ?.addEventListener("click", () => navigate("settings"));
  views.home.querySelectorAll("[data-document-id]").forEach((button) => {
    button.addEventListener("click", () => navigateToDocument(button.dataset.documentId));
  });
  document.title = "Workflow Builder — AI Workflow Course";
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
    <span>${iconSvg("clock")}About ${Math.max(1, Math.ceil(courseDocument.wordCount / 210))} min</span>
    <span>${iconSvg("layers")}${escapeHtml(learningPositionLabel(courseDocument))}</span>
    <span title="Source: ${escapeAttribute(courseDocument.sourcePath)}">${iconSvg("document")}${escapeHtml(lessonPosition)}</span>
  `;
  const content = document.querySelector("#reader-content");
  content.innerHTML = renderMarkdown(courseDocument.markdown);
  wireCourseLinks(content, courseDocument);
  wireCodeCopy(content);

  const completeButton = document.querySelector("#complete-button");
  const isComplete = state.completed.includes(id);
  completeButton.setAttribute("aria-pressed", String(isComplete));
  completeButton.querySelector("span:last-child").textContent = isComplete
    ? "Completed"
    : "Mark complete";

  document.querySelector("#checkpoint-alert").hidden =
    courseDocument.sourcePath !== "weeks/WEEK_07.md";
  const note = document.querySelector("#learner-note");
  note.value = state.notes[id] || "";
  document.querySelector("#note-save-status").textContent = "Saved locally";

  const position = courseBundle.documents.findIndex((document) => document.id === id);
  setDocumentPager(
    document.querySelector("#previous-document"),
    courseBundle.documents[position - 1],
    "Previous",
  );
  setDocumentPager(
    document.querySelector("#next-document"),
    courseBundle.documents[position + 1],
    "Next",
  );

  document.querySelectorAll(".nav-document").forEach((button) => {
    if (button.dataset.documentId === id) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });

  document.title = `${courseDocument.title} — Workflow Builder`;
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
  document.title = "Search — Workflow Builder";
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
    `v${courseBundle.course.version}`;
  document.querySelector("#settings-verified-date").textContent =
    courseBundle.course.verifiedThrough;
  document.querySelector("#settings-build-id").textContent = config.buildId;
  document.querySelector("#last-update-check").textContent = state.lastUpdateCheck
    ? new Date(state.lastUpdateCheck).toLocaleString()
    : "Not yet";
  applyAppearance();
  document.title = "Settings — Workflow Builder";
}

function renderRoute() {
  closeSidebar();
  const route = window.location.hash.replace(/^#/, "") || "home";
  if (route.startsWith("doc=")) {
    renderDocument(decodeURIComponent(route.slice(4)));
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
  const index = state.completed.indexOf(currentDocument.id);
  if (index >= 0) state.completed.splice(index, 1);
  else state.completed.push(currentDocument.id);
  saveState();
  renderCourseNavigation();
  updateProgressUi();
  renderDocument(currentDocument.id);
  showToast(index >= 0 ? "Marked incomplete." : "Lesson marked complete.");
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

async function importProgress(file) {
  try {
    const payload = JSON.parse(await file.text());
    if (
      payload?.exportType !== "ai-workflow-course-progress" ||
      payload?.state?.schemaVersion !== 1
    ) {
      throw new Error("Not a supported course progress backup.");
    }
    if (!window.confirm("Replace progress and notes on this device with this backup?")) {
      return;
    }
    state.completed = Array.isArray(payload.state.completed)
      ? payload.state.completed.filter((id) => documentById.has(id))
      : [];
    state.notes =
      payload.state.notes && typeof payload.state.notes === "object"
        ? Object.fromEntries(
            Object.entries(payload.state.notes)
              .filter(([id, note]) => documentById.has(id) && typeof note === "string")
              .map(([id, note]) => [id, note.slice(0, 50000)]),
          )
        : {};
    state.lastDocument = documentById.has(payload.state.lastDocument)
      ? payload.state.lastDocument
      : null;
    state.theme = ["system", "light", "dark"].includes(payload.state.theme)
      ? payload.state.theme
      : "system";
    state.fontSize = Math.max(
      90,
      Math.min(125, Number(payload.state.fontSize) || 100),
    );
    saveState();
    renderCourseNavigation();
    updateProgressUi();
    applyAppearance();
    renderRoute();
    showToast("Progress backup imported.");
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
  Object.assign(state, {
    schemaVersion: 1,
    completed: [],
    notes: {},
    lastDocument: null,
    theme: "system",
    fontSize: 100,
    lastUpdateCheck: null,
    expandedGroups: ["foundations"],
  });
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
    if (manual) showToast("Update checks need Safari or a browser with service workers.");
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
        showToast("A deployment is available; checking its service worker…");
        await serviceWorkerRegistration.update();
      } else {
        showToast(`You have the latest published course (v${config.courseVersion}).`);
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
        else if (state.lastDocument) navigateToDocument(state.lastDocument);
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
      courseBundle?.schemaVersion !== 1 ||
      !Array.isArray(courseBundle.documents) ||
      !Array.isArray(courseBundle.groups)
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
    state.completed = state.completed.filter((id) => documentById.has(id));
    if (state.lastDocument && !documentById.has(state.lastDocument)) {
      state.lastDocument = null;
    }
    saveState();
    renderCourseNavigation();
    updateProgressUi();
    renderRoute();
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
