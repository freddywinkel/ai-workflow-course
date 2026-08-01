import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { cp, mkdir, mkdtemp, readFile, readdir, rm } from "node:fs/promises";
import { createServer } from "node:net";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = resolve(fileURLToPath(new URL(".", import.meta.url)));
const appRoot = resolve(scriptDirectory, "..");
const basePath = "/ai-workflow-course/";

function chromeExecutable() {
  const candidates = [
    process.env.CHROME_PATH,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ].filter(Boolean);
  const executable = candidates.find((candidate) => existsSync(candidate));
  if (!executable) {
    throw new Error(
      "Chrome was not found. Set CHROME_PATH to run the local browser smoke test.",
    );
  }
  return executable;
}

async function availablePort() {
  const server = createServer();
  await new Promise((resolveListen, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolveListen);
  });
  const address = server.address();
  const port = typeof address === "object" && address ? address.port : null;
  await new Promise((resolveClose) => server.close(resolveClose));
  if (!port) throw new Error("Could not reserve a local test port.");
  return port;
}

async function waitFor(check, description, timeoutMs = 12000) {
  const deadline = Date.now() + timeoutMs;
  let lastError;
  while (Date.now() < deadline) {
    try {
      const result = await check();
      if (result) return result;
    } catch (error) {
      lastError = error;
    }
    await new Promise((resolveWait) => setTimeout(resolveWait, 80));
  }
  throw new Error(
    `${description} did not become ready.${lastError ? ` ${lastError.message}` : ""}`,
  );
}

async function createCdpClient(webSocketUrl) {
  const socket = new WebSocket(webSocketUrl);
  await new Promise((resolveOpen, reject) => {
    socket.addEventListener("open", resolveOpen, { once: true });
    socket.addEventListener("error", reject, { once: true });
  });
  let nextId = 1;
  const pending = new Map();
  socket.addEventListener("message", (event) => {
    const message = JSON.parse(String(event.data));
    if (!message.id || !pending.has(message.id)) return;
    const { resolve: resolveCall, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(message.error.message));
    else resolveCall(message.result);
  });
  return {
    close() {
      socket.close();
    },
    call(method, params = {}) {
      const id = nextId;
      nextId += 1;
      return new Promise((resolveCall, reject) => {
        pending.set(id, {
          resolve: resolveCall,
          reject: (error) => reject(new Error(`${method}: ${error.message}`)),
        });
        socket.send(JSON.stringify({ id, method, params }));
      });
    },
  };
}

async function main() {
  const previewPort = await availablePort();
  const debugPort = await availablePort();
  const temporaryDirectory = await mkdtemp(
    join(tmpdir(), "course1-pwa-browser-smoke-"),
  );
  const profileDirectory = join(temporaryDirectory, "chrome-profile");
  const downloadDirectory = join(temporaryDirectory, "downloads");
  const distSnapshot = join(temporaryDirectory, "dist");
  await mkdir(profileDirectory);
  await mkdir(downloadDirectory);
  await cp(join(appRoot, "dist"), distSnapshot, { recursive: true });
  const bundledCourse = JSON.parse(
    await readFile(join(distSnapshot, "course-content.json"), "utf8"),
  );
  const learningSequenceIds = bundledCourse.course.learningSequenceIds;
  const tableDocumentId = bundledCourse.documents.find((courseDocument) =>
    /(?:^|\n)\|[^\n]+\|\r?\n\|(?:\s*:?-{3,}:?\s*\|)+/m.test(
      courseDocument.markdown,
    ),
  )?.id;
  assert.ok(tableDocumentId, "The browser smoke needs one bundled Markdown table.");
  const previewUrl = `http://127.0.0.1:${previewPort}${basePath}`;
  let previewProcess;
  let chromeProcess;
  let client;
  let secondClient;
  let secondTargetId;

  try {
    previewProcess = spawn(process.execPath, ["scripts/serve.mjs"], {
      cwd: appRoot,
      env: {
        ...process.env,
        BASE_PATH: basePath,
        COURSE_DIST_PATH: distSnapshot,
        PORT: String(previewPort),
      },
      stdio: "ignore",
      windowsHide: true,
    });
    await waitFor(async () => {
      const response = await fetch(previewUrl);
      return response.ok;
    }, "Course preview");

    chromeProcess = spawn(
      chromeExecutable(),
      [
        "--headless=new",
        "--disable-gpu",
        "--disable-popup-blocking",
        "--no-first-run",
        "--no-default-browser-check",
        `--remote-debugging-port=${debugPort}`,
        `--user-data-dir=${profileDirectory}`,
        "about:blank",
      ],
      {
        stdio: "ignore",
        windowsHide: true,
      },
    );

    const target = await waitFor(async () => {
      const response = await fetch(`http://127.0.0.1:${debugPort}/json/list`);
      if (!response.ok) return null;
      const targets = await response.json();
      return targets.find((candidate) => candidate.type === "page");
    }, "Chrome debugging target");
    client = await createCdpClient(target.webSocketDebuggerUrl);
    await client.call("Page.enable");
    await client.call("Runtime.enable");
    await client.call("Network.enable");
    await client.call("Browser.setDownloadBehavior", {
      behavior: "allow",
      downloadPath: downloadDirectory,
    });
    await client.call("Emulation.setDeviceMetricsOverride", {
      width: 320,
      height: 1000,
      deviceScaleFactor: 1,
      mobile: true,
    });
    await client.call("Page.navigate", { url: previewUrl });

    const evaluateOn = async (targetClient, expression) => {
      const result = await targetClient.call("Runtime.evaluate", {
        expression,
        returnByValue: true,
        awaitPromise: true,
      });
      if (result.exceptionDetails) {
        throw new Error(result.exceptionDetails.text || "Browser evaluation failed.");
      }
      return result.result.value;
    };
    const evaluate = (expression) => evaluateOn(client, expression);
    const waitForAutomaticUpdateCheckOn = (targetEvaluate, label) =>
      waitFor(
        () =>
          targetEvaluate(`(() => {
            const raw = localStorage.getItem(
              "ai-workflow-course-state-v1"
            );
            if (!raw) return false;
            const checkedAt = Date.parse(
              JSON.parse(raw).state.lastUpdateCheck || ""
            );
            const updateButtons = [
              document.querySelector("#update-button"),
              document.querySelector("#settings-update-button"),
              document.querySelector("#checkpoint-update-button")
            ].filter(Boolean);
            return Number.isFinite(checkedAt) &&
              checkedAt >= performance.timeOrigin &&
              updateButtons.every(
                (button) => button.getAttribute("aria-busy") !== "true"
              );
          })()`),
        `${label} automatic update check`,
      );
    const assertReleaseBoundary = async (label) => {
      const release = await evaluate(`(() => {
        const boundary = document.querySelector("#release-boundary");
        const pill = document.querySelector(".release-pill");
        const boundaryStyle = boundary ? getComputedStyle(boundary) : null;
        const pillStyle = pill ? getComputedStyle(pill) : null;
        return {
          boundaryText: boundary?.textContent?.replace(/\\s+/g, " ").trim() || "",
          boundaryVisible: Boolean(
            boundary &&
            !boundary.hidden &&
            boundaryStyle.display !== "none" &&
            boundaryStyle.visibility !== "hidden" &&
            boundary.getClientRects().length
          ),
          pillText: pill?.textContent?.trim() || "",
          pillLabel: pill?.getAttribute("aria-label") || "",
          pillVisible: Boolean(
            pill &&
            !pill.hidden &&
            pillStyle.display !== "none" &&
            pillStyle.visibility !== "hidden" &&
            pill.getClientRects().length
          ),
          productStatus: window.__COURSE_APP__?.productStatus || "",
          distributionPurpose:
            window.__COURSE_APP__?.distributionPurpose || "",
        };
      })()`);
      assert.equal(release.boundaryVisible, true, `${label}: release boundary hidden`);
      assert.match(release.boundaryText, /UNVERIFIED personal-study release/);
      assert.match(release.boundaryText, /Use synthetic data only/);
      assert.match(release.boundaryText, /cannot award Course 1 completion/);
      assert.equal(release.pillVisible, true, `${label}: release pill hidden`);
      assert.equal(release.pillText, "UNVERIFIED");
      assert.match(release.pillLabel, /UNVERIFIED personal-study release/);
      assert.equal(release.productStatus, "UNVERIFIED");
      assert.equal(release.distributionPurpose, "personal-synthetic-study");
    };
    const approveActionDialog = async (label) => {
      try {
        await waitFor(
          () =>
            evaluate(`document.querySelector("#action-confirmation-dialog")?.open === true`),
          `${label} confirmation dialog`,
        );
      } catch (error) {
        const diagnostic = await evaluate(`({
          toast: document.querySelector("#toast")?.textContent || "",
          dialogExists: Boolean(
            document.querySelector("#action-confirmation-dialog")
          ),
          dialogOpen:
            document.querySelector("#action-confirmation-dialog")?.open ?? null
        })`);
        throw new Error(
          `${error.message} State=${JSON.stringify(diagnostic)}`,
        );
      }
      const accessibility = await evaluate(`(() => {
        const dialog = document.querySelector("#action-confirmation-dialog");
        const confirmButton = dialog.querySelector("#action-confirm-button");
        return {
          modal: dialog.open,
          labelledBy: dialog.getAttribute("aria-labelledby"),
          describedBy: dialog.getAttribute("aria-describedby"),
          confirmLabel: confirmButton.textContent.trim(),
          activeInside: dialog.contains(document.activeElement),
        };
      })()`);
      assert.equal(accessibility.modal, true);
      assert.equal(accessibility.labelledBy, "action-confirmation-title");
      assert.equal(accessibility.describedBy, "action-confirmation-message");
      assert.ok(accessibility.confirmLabel.length > 0);
      assert.equal(accessibility.activeInside, true);
      await evaluate(`document.querySelector("#action-confirm-button").click()`);
      await waitFor(
        () =>
          evaluate(`!document.querySelector("#action-confirmation-dialog")?.open`),
        `${label} confirmation close`,
      );
    };
    const setViewport = async (width, height) => {
      await client.call("Emulation.setDeviceMetricsOverride", {
        width,
        height,
        deviceScaleFactor: 1,
        mobile: width <= 920,
      });
      await waitFor(
        () => evaluate(`innerWidth === ${width} && innerHeight === ${height}`),
        `${width}x${height} viewport`,
      );
      if (width <= 920) {
        await waitFor(
          () =>
            evaluate(`document.body.classList.contains("sidebar-open") ||
              document.querySelector(".sidebar").getBoundingClientRect().right <= 0.5`),
          `${width}x${height} closed mobile sidebar`,
        );
      }
    };
    const pressKey = async ({
      key,
      code = key,
      windowsVirtualKeyCode,
      modifiers = 0,
      text,
    }) => {
      await client.call("Input.dispatchKeyEvent", {
        type: "rawKeyDown",
        key,
        code,
        windowsVirtualKeyCode,
        modifiers,
      });
      if (text) {
        await client.call("Input.dispatchKeyEvent", {
          type: "char",
          key,
          code,
          text,
          windowsVirtualKeyCode,
          modifiers,
        });
      }
      await client.call("Input.dispatchKeyEvent", {
        type: "keyUp",
        key,
        code,
        windowsVirtualKeyCode,
        modifiers,
      });
    };

    try {
      await waitFor(
        () =>
          evaluate(`document.readyState === "complete" &&
            document.querySelector("#loading-card")?.hidden === true &&
            document.querySelector("#home-view")?.hidden === false`),
        "Course home",
      );
    } catch (error) {
      const diagnostic = await evaluate(`(() => ({
        readyState: document.readyState,
        loadingHidden: document.querySelector("#loading-card")?.hidden,
        loadingText: document.querySelector("#loading-card")?.textContent?.trim(),
        homeHidden: document.querySelector("#home-view")?.hidden,
        appConfig: window.__COURSE_APP__ || null,
      }))()`);
      throw new Error(`${error.message} Browser state: ${JSON.stringify(diagnostic)}`);
    }
    // The first service worker takes control and the application deliberately
    // reloads once. Wait for that PWA lifecycle transition before interacting.
    await waitFor(
      () => evaluate(`navigator.serviceWorker?.controller !== null`),
      "Initial service-worker control",
    );
    await new Promise((resolveSettle) => setTimeout(resolveSettle, 450));
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          document.querySelector("#home-view")?.hidden === false`),
      "Stable course home",
    );
    await waitForAutomaticUpdateCheckOn(evaluate, "Primary startup");
    await assertReleaseBoundary("Home");

    const mainWriterBeforeDuplicate = await evaluate(`(() => {
      const envelope = JSON.parse(
        localStorage.getItem("ai-workflow-course-state-v1")
      );
      sessionStorage.setItem(
        "ai-workflow-course-writer-v1",
        envelope.writerId
      );
      return envelope.writerId;
    })()`);
    const targetsBeforeDuplicate = new Set(
      (
        await (
          await fetch(`http://127.0.0.1:${debugPort}/json/list`)
        ).json()
      ).map((candidate) => candidate.id),
    );
    assert.equal(
      await evaluate(`window.open(${JSON.stringify(previewUrl)}, "_blank") !== null`),
      true,
    );
    const secondTarget = await waitFor(async () => {
      const response = await fetch(`http://127.0.0.1:${debugPort}/json/list`);
      if (!response.ok) return null;
      const targets = await response.json();
      return targets.find(
        (candidate) =>
          candidate.type === "page" &&
          !targetsBeforeDuplicate.has(candidate.id) &&
          candidate.url.startsWith(previewUrl),
      );
    }, "Opener-created duplicate course window");
    secondTargetId = secondTarget.id;
    secondClient = await createCdpClient(secondTarget.webSocketDebuggerUrl);
    await secondClient.call("Page.enable");
    await secondClient.call("Runtime.enable");
    const evaluateSecond = (expression) => evaluateOn(secondClient, expression);
    await waitFor(
      () =>
        evaluateSecond(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          navigator.serviceWorker?.controller !== null`),
      "Second controlled course window",
    );
    await waitForAutomaticUpdateCheckOn(evaluateSecond, "Second-window startup");
    const duplicateWriterIdentity = await evaluateSecond(`(() => {
      const envelope = JSON.parse(
        localStorage.getItem("ai-workflow-course-state-v1")
      );
      return {
        inheritedSessionWriter: sessionStorage.getItem(
          "ai-workflow-course-writer-v1"
        ),
        storedWriter: envelope.writerId,
      };
    })()`);
    assert.equal(
      duplicateWriterIdentity.inheritedSessionWriter,
      mainWriterBeforeDuplicate,
      "The opener regression did not reproduce inherited session storage.",
    );
    assert.notEqual(
      duplicateWriterIdentity.storedWriter,
      mainWriterBeforeDuplicate,
      "A duplicated/opener tab reused the first page context's writer identity.",
    );

    await Promise.all([
      evaluate(`location.hash = "#doc=course-1-foundation-01"`),
      evaluateSecond(`location.hash = "#doc=course-1-foundation-02"`),
    ]);
    await waitFor(
      async () =>
        (await evaluate(
          `document.querySelector("#reader-view")?.hidden === false`,
        )) &&
        (await evaluateSecond(
          `document.querySelector("#reader-view")?.hidden === false`,
        )),
      "Two-window lesson routes",
    );
    await assertReleaseBoundary("Lesson");
    await Promise.all([
      evaluate(`document.querySelector("#complete-button").click()`),
      evaluateSecond(`document.querySelector("#complete-button").click()`),
    ]);
    try {
      await waitFor(
        () =>
          evaluate(`(() => {
            const envelope = JSON.parse(
              localStorage.getItem("ai-workflow-course-state-v1")
            );
            return envelope.revision >= 3 &&
              envelope.state.completed.includes("course-1-foundation-01") &&
              envelope.state.completed.includes("course-1-foundation-02");
          })()`),
        "Merged two-window progress",
      );
    } catch (error) {
      const [mainState, otherState] = await Promise.all([
        evaluate(`({
          raw: localStorage.getItem("ai-workflow-course-state-v1"),
          toast: document.querySelector("#toast")?.textContent || "",
          route: location.hash,
          pressed: document.querySelector("#complete-button")?.getAttribute("aria-pressed")
        })`),
        evaluateSecond(`({
          raw: localStorage.getItem("ai-workflow-course-state-v1"),
          toast: document.querySelector("#toast")?.textContent || "",
          route: location.hash,
          pressed: document.querySelector("#complete-button")?.getAttribute("aria-pressed")
        })`),
      ]);
      throw new Error(
        `${error.message} Main=${JSON.stringify(mainState)} Other=${JSON.stringify(otherState)}`,
      );
    }

    await Promise.all([
      evaluate(`location.hash = "#doc=course-1-foundation-03"`),
      evaluateSecond(`location.hash = "#doc=course-1-foundation-03"`),
    ]);
    await waitFor(
      async () =>
        (await evaluate(`document.querySelector("#learner-note") !== null`)) &&
        (await evaluateSecond(
          `document.querySelector("#learner-note") !== null`,
        )),
      "Two-window note editors",
    );
    await Promise.all([
      evaluate(`(() => {
        const note = document.querySelector("#learner-note");
        note.value = "Concurrent note from window A.";
        note.dispatchEvent(new Event("input", { bubbles: true }));
      })()`),
      evaluateSecond(`(() => {
        const note = document.querySelector("#learner-note");
        note.value = "Concurrent note from window B.";
        note.dispatchEvent(new Event("input", { bubbles: true }));
      })()`),
    ]);
    await waitFor(
      async () => {
        const mainToast = await evaluate(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        const secondToast = await evaluateSecond(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        const recoveryReason = await evaluate(`(() => {
          const raw = localStorage.getItem("ai-workflow-course-recovery-v1");
          return raw ? JSON.parse(raw).reason : "";
        })()`);
        return (
          /same item|nothing was overwritten/i.test(`${mainToast} ${secondToast}`) &&
          /conflict/i.test(recoveryReason)
        );
      },
      "Visible same-note conflict",
    );
    const concurrentState = await evaluate(`(() => {
      const envelope = JSON.parse(
        localStorage.getItem("ai-workflow-course-state-v1")
      );
      return {
        revision: envelope.revision,
        writerId: envelope.writerId,
        note: envelope.state.notes["course-1-foundation-03"],
      };
    })()`);
    assert.ok(concurrentState.revision >= 4);
    assert.match(concurrentState.writerId, /^[A-Za-z0-9-]{8,80}$/);
    assert.ok(
      [
        "Concurrent note from window A.",
        "Concurrent note from window B.",
      ].includes(concurrentState.note),
    );
    await evaluate(`location.hash = "#settings"`);
    await waitFor(
      () =>
        evaluate(`document.querySelector("#settings-view")?.hidden === false`),
      "Settings before reset cancellation",
    );
    const stateBeforeCancelledReset = await evaluate(
      `localStorage.getItem("ai-workflow-course-state-v1")`,
    );
    await evaluate(`(() => {
      const resetButton = document.querySelector("#reset-progress");
      resetButton.focus();
      resetButton.click();
    })()`);
    await waitFor(
      () =>
        evaluate(`document.querySelector("#action-confirmation-dialog")?.open === true`),
      "Reset cancellation dialog",
    );
    await client.call("Input.dispatchKeyEvent", {
      type: "keyDown",
      key: "Escape",
      code: "Escape",
      windowsVirtualKeyCode: 27,
    });
    await client.call("Input.dispatchKeyEvent", {
      type: "keyUp",
      key: "Escape",
      code: "Escape",
      windowsVirtualKeyCode: 27,
    });
    await waitFor(
      () =>
        evaluate(`!document.querySelector("#action-confirmation-dialog")?.open`),
      "Escape-cancelled reset",
    );
    assert.equal(
      await evaluate(`localStorage.getItem("ai-workflow-course-state-v1")`),
      stateBeforeCancelledReset,
    );
    assert.equal(
      await evaluate(
        `document.activeElement === document.querySelector("#reset-progress")`,
      ),
      true,
      "Focus did not return to the reset control after cancellation.",
    );
    await evaluate(`location.hash = "#doc=course-1-foundation-03"`);
    await waitFor(
      () =>
        evaluate(`document.querySelector("#learner-note") !== null`),
      "Note editor after reset cancellation",
    );
    const pendingResetNote = "Unsaved note present when the other window reset.";
    await Promise.all([
      evaluate(`window.confirm = () => {
        throw new Error("Native confirm must not be used.");
      }`),
      evaluateSecond(`window.confirm = () => {
        throw new Error("Native confirm must not be used.");
      }`),
    ]);
    await evaluate(`(() => {
      window.__toastHistory = [];
      const toast = document.querySelector("#toast");
      new MutationObserver(() => {
        if (toast.textContent) window.__toastHistory.push(toast.textContent);
      }).observe(toast, { childList: true, subtree: true });
    })()`);
    await evaluate(`document.querySelector("#reset-progress").click()`);
    await waitFor(
      () =>
        evaluate(`document.querySelector("#action-confirmation-dialog")?.open === true`),
      "Cross-window reset confirmation dialog",
    );
    await evaluateSecond(`(() => {
      const note = document.querySelector("#learner-note");
      note.value = ${JSON.stringify(pendingResetNote)};
      note.dispatchEvent(new Event("input", { bubbles: true }));
    })()`);
    await evaluate(`document.querySelector("#action-confirm-button").click()`);
    await waitFor(
      () =>
        evaluate(`!document.querySelector("#action-confirmation-dialog")?.open`),
      "Cross-window reset confirmation close",
    );
    try {
      await waitFor(
        async () => {
          const [mainReset, otherReset] = await Promise.all([
            evaluate(`({
              route: location.hash,
              stored: localStorage.getItem("ai-workflow-course-state-v1")
            })`),
            evaluateSecond(`({
              route: location.hash,
              stored: localStorage.getItem("ai-workflow-course-state-v1"),
              toast: document.querySelector("#toast")?.textContent || "",
              recovery: localStorage.getItem("ai-workflow-course-recovery-v1")
            })`),
          ]);
          let pendingRecovery = false;
          if (otherReset.recovery) {
            const recovery = JSON.parse(otherReset.recovery);
            const recoveredEnvelope = JSON.parse(recovery.raw);
            pendingRecovery =
              /pending local note/i.test(recovery.reason) &&
              recoveredEnvelope.state.notes["course-1-foundation-03"] ===
                pendingResetNote;
          }
          return (
            mainReset.route === "#home" &&
            (!mainReset.stored ||
              (() => {
                const state = JSON.parse(mainReset.stored).state;
                return (
                  state.completed.length === 0 &&
                  state.practicalPassed.length === 0 &&
                  Object.keys(state.notes).length === 0
                );
              })()) &&
            otherReset.route === "#home" &&
            (!otherReset.stored ||
              (() => {
                const state = JSON.parse(otherReset.stored).state;
                return (
                  state.completed.length === 0 &&
                  state.practicalPassed.length === 0 &&
                  Object.keys(state.notes).length === 0
                );
              })()) &&
            /reset in another window/i.test(otherReset.toast) &&
            /unsaved note|recovery record/i.test(otherReset.toast) &&
            pendingRecovery
          );
        },
        "Cross-window reset with pending-note recovery",
      );
    } catch (error) {
      const [mainReset, otherReset] = await Promise.all([
        evaluate(`({
          route: location.hash,
          stored: localStorage.getItem("ai-workflow-course-state-v1"),
          barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1"),
          recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
          toastHistory: window.__toastHistory || [],
          toast: document.querySelector("#toast")?.textContent || ""
        })`),
        evaluateSecond(`({
          route: location.hash,
          stored: localStorage.getItem("ai-workflow-course-state-v1"),
          barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1"),
          recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
          toast: document.querySelector("#toast")?.textContent || ""
        })`),
      ]);
      throw new Error(
        `${error.message} Main=${JSON.stringify(mainReset)} Other=${JSON.stringify(otherReset)}`,
      );
    }
    await client.call("Target.closeTarget", { targetId: secondTargetId });
    secondClient.close();
    secondClient = null;
    secondTargetId = null;
    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true`),
      "Primary window reload after conflict",
    );
    await waitForAutomaticUpdateCheckOn(evaluate, "Primary post-conflict reload");

    if ((await evaluate(`location.hash`)) === "#home") {
      await evaluate(`location.hash = "#career"`);
      await waitFor(
        () =>
          evaluate(`location.hash === "#career" &&
            document.querySelector("#career-view")?.hidden === false`),
        "Temporary career route before Home focus check",
      );
    }
    await evaluate(`location.hash = "#home"`);
    await waitFor(
      () =>
        evaluate(`location.hash === "#home" &&
          document.querySelector("#home-view")?.hidden === false &&
          document.activeElement === document.querySelector("#home-view h1")`),
      "Home route heading focus",
    );
    await evaluate(`(() => {
      const body = document.body;
      body.setAttribute("tabindex", "-1");
      body.focus();
      body.removeAttribute("tabindex");
    })()`);
    await pressKey({
      key: "Tab",
      code: "Tab",
      windowsVirtualKeyCode: 9,
    });
    await waitFor(
      () =>
        evaluate(`(() => {
          const link = document.querySelector(".skip-link");
          const rect = link.getBoundingClientRect();
          return document.activeElement === link &&
            rect.width > 0 && rect.height > 0 && rect.top >= -0.5;
        })()`),
      "Visible keyboard skip link",
    );
    const skipLinkFocus = await evaluate(`(() => {
      const link = document.querySelector(".skip-link");
      const rect = link.getBoundingClientRect();
      return {
        focused: document.activeElement === link,
        visible: rect.width > 0 && rect.height > 0 && rect.top >= -0.5,
      };
    })()`);
    assert.equal(skipLinkFocus.focused, true);
    assert.equal(skipLinkFocus.visible, true);
    await pressKey({
      key: "Enter",
      code: "Enter",
      windowsVirtualKeyCode: 13,
    });
    await waitFor(
      () =>
        evaluate(`location.hash === "#home" &&
          document.activeElement === document.querySelector("#main-content")`),
      "Skip-link keyboard target without route change",
    );

    const minimumTargetSize = 44;
    const targetSizeTolerance = 0.01;
    const viewportCases = [
      { width: 320, height: 568, label: "small phone portrait" },
      { width: 390, height: 844, label: "phone portrait" },
      { width: 430, height: 932, label: "large phone portrait" },
      { width: 834, height: 1112, label: "tablet portrait" },
      { width: 1440, height: 900, label: "desktop" },
      { width: 844, height: 390, label: "short landscape" },
    ];
    for (const viewport of viewportCases) {
      await setViewport(viewport.width, viewport.height);
      await evaluate(`location.hash = "#home"`);
      await waitFor(
        () =>
          evaluate(`document.querySelector("#home-view")?.hidden === false &&
            Boolean(document.querySelector('[data-home-action="resume"]'))`),
        `${viewport.label} home`,
      );
      await assertReleaseBoundary(`${viewport.label} home`);
      const viewportLayout = await evaluate(`(async () => {
        const primary = document.querySelector('[data-home-action="resume"]');
        primary.scrollIntoView({ block: "center", behavior: "instant" });
        await new Promise((resolve) =>
          requestAnimationFrame(() => requestAnimationFrame(resolve))
        );
        const nav = document.querySelector(".bottom-nav");
        const navRect = nav.getBoundingClientRect();
        const navVisible = nav.getClientRects().length > 0;
        const buttons = [...nav.querySelectorAll("button")];
        const buttonChecks = buttons.map((button) => {
          const rect = button.getBoundingClientRect();
          const hit = document.elementFromPoint(
            rect.left + rect.width / 2,
            rect.top + rect.height / 2
          );
          return {
            enabled: !button.disabled,
            height: rect.height,
            width: rect.width,
            insideViewport:
              rect.left >= -0.5 &&
              rect.right <= innerWidth + 0.5 &&
              rect.top >= -0.5 &&
              rect.bottom <= innerHeight + 0.5,
            topmostAtCentre: Boolean(hit && button.contains(hit)),
          };
        });
        const primaryRect = primary.getBoundingClientRect();
        const primaryHit = document.elementFromPoint(
          primaryRect.left + primaryRect.width / 2,
          primaryRect.top + primaryRect.height / 2
        );
        return {
          innerWidth,
          innerHeight,
          pageScrollWidth: document.documentElement.scrollWidth,
          bodyScrollWidth: document.body.scrollWidth,
          navVisible,
          navLeft: navRect.left,
          navRight: navRect.right,
          navBottom: navRect.bottom,
          buttonChecks,
          primaryHeight: primaryRect.height,
          primaryVisible:
            primaryRect.top >= -0.5 &&
            primaryRect.bottom <= (navVisible ? navRect.top : innerHeight) - 0.5,
          primaryTopmostAtCentre: Boolean(
            primaryHit && primary.contains(primaryHit)
          ),
          primaryHit:
            primaryHit &&
            primaryHit.tagName.toLowerCase() + "." + (primaryHit.className || ""),
          primaryRect: {
            top: primaryRect.top,
            right: primaryRect.right,
            bottom: primaryRect.bottom,
            left: primaryRect.left,
          },
        };
      })()`);
      assert.equal(viewportLayout.innerWidth, viewport.width);
      assert.equal(viewportLayout.innerHeight, viewport.height);
      assert.ok(
        viewportLayout.pageScrollWidth <= viewport.width,
        `${viewport.label} page scroll width was ${viewportLayout.pageScrollWidth}`,
      );
      assert.ok(
        viewportLayout.bodyScrollWidth <= viewport.width,
        `${viewport.label} body scroll width was ${viewportLayout.bodyScrollWidth}`,
      );
      assert.ok(
        viewportLayout.primaryHeight + targetSizeTolerance >= minimumTargetSize,
        `${viewport.label} primary control was ${viewportLayout.primaryHeight} pixels high; expected at least ${minimumTargetSize} allowing ${targetSizeTolerance} pixel browser rounding`,
      );
      assert.equal(
        viewportLayout.primaryVisible,
        true,
        `${viewport.label} primary control was obscured by fixed navigation`,
      );
      assert.equal(
        viewportLayout.primaryTopmostAtCentre,
        true,
        `${viewport.label} primary control was not tappable at its centre: ${JSON.stringify({
          hit: viewportLayout.primaryHit,
          rect: viewportLayout.primaryRect,
        })}`,
      );
      if (viewport.width <= 920) {
        assert.equal(viewportLayout.navVisible, true);
        assert.ok(viewportLayout.navLeft >= -0.5);
        assert.ok(viewportLayout.navRight <= viewport.width + 0.5);
        assert.ok(viewportLayout.navBottom <= viewport.height + 0.5);
        assert.equal(viewportLayout.buttonChecks.length, 5);
        for (const [index, button] of viewportLayout.buttonChecks.entries()) {
          assert.equal(button.enabled, true, `${viewport.label} tab ${index + 1}`);
          assert.ok(
            button.width + targetSizeTolerance >= minimumTargetSize &&
              button.height + targetSizeTolerance >= minimumTargetSize,
            `${viewport.label} tab ${index + 1} measured ${button.width} by ${button.height} pixels; expected at least ${minimumTargetSize} by ${minimumTargetSize} allowing ${targetSizeTolerance} pixel browser-rounding tolerance`,
          );
          assert.equal(
            button.insideViewport,
            true,
            `${viewport.label} tab ${index + 1} was clipped`,
          );
          assert.equal(
            button.topmostAtCentre,
            true,
            `${viewport.label} tab ${index + 1} was not tappable at its centre`,
          );
        }
      } else {
        assert.equal(viewportLayout.navVisible, false);
      }
    }
    await setViewport(320, 568);

    const layout = await evaluate(`(() => {
      const bottom = document.querySelector(".bottom-nav").getBoundingClientRect();
      const buttons = [...document.querySelectorAll(".bottom-nav button")]
        .map((button) => button.getBoundingClientRect());
      return {
        innerWidth,
        scrollWidth: document.documentElement.scrollWidth,
        bottomLeft: bottom.left,
        bottomRight: bottom.right,
        buttonCount: buttons.length,
        visibleButtons: buttons.filter((rect) =>
          rect.width > 0 && rect.left >= -0.5 && rect.right <= innerWidth + 0.5
        ).length,
        laterCourseNavLinks:
          document.querySelectorAll('#course-nav [data-document-id^="course-4-"]').length,
      };
    })()`);
    assert.equal(layout.innerWidth, 320);
    assert.ok(layout.scrollWidth <= 320, `page scroll width was ${layout.scrollWidth}`);
    assert.ok(layout.bottomLeft >= -0.5);
    assert.ok(layout.bottomRight <= 320.5);
    assert.equal(layout.buttonCount, 5);
    assert.equal(layout.visibleButtons, 5);
    assert.equal(layout.laterCourseNavLinks, 0);

    await client.call("Emulation.setEmulatedMedia", {
      features: [{ name: "forced-colors", value: "active" }],
    });
    assert.equal(
      await evaluate(`matchMedia("(forced-colors: active)").matches`),
      true,
    );
    const forcedColourFocus = await evaluate(`(() => {
      const button = document.querySelector(".bottom-nav button:not([disabled])");
      button.focus();
      const style = getComputedStyle(button);
      return {
        focused: document.activeElement === button,
        visible: button.getClientRects().length > 0,
        colour: style.color,
        background: style.backgroundColor,
      };
    })()`);
    assert.equal(forcedColourFocus.focused, true);
    assert.equal(forcedColourFocus.visible, true);
    assert.notEqual(forcedColourFocus.colour, forcedColourFocus.background);
    await assertReleaseBoundary("Forced colours");
    assert.notEqual(
      await evaluate(
        `getComputedStyle(document.querySelector("#release-boundary")).borderBottomStyle`,
      ),
      "none",
    );
    await client.call("Emulation.setEmulatedMedia", { features: [] });

    await client.call("Emulation.setEmulatedMedia", {
      features: [{ name: "prefers-reduced-motion", value: "reduce" }],
    });
    const reducedMotion = await evaluate(`(() => {
      const longestSeconds = (value) =>
        Math.max(
          ...value.split(",").map((part) => {
            const duration = part.trim();
            if (duration.endsWith("ms")) return parseFloat(duration) / 1000;
            return parseFloat(duration) || 0;
          })
        );
      return {
        matches: matchMedia("(prefers-reduced-motion: reduce)").matches,
        scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior,
        sidebarTransitionSeconds: longestSeconds(
          getComputedStyle(document.querySelector(".sidebar")).transitionDuration
        ),
        skipLinkTransitionSeconds: longestSeconds(
          getComputedStyle(document.querySelector(".skip-link")).transitionDuration
        ),
        settingsCardTransitionSeconds: longestSeconds(
          getComputedStyle(document.querySelector(".settings-card")).transitionDuration
        ),
      };
    })()`);
    assert.equal(reducedMotion.matches, true);
    assert.equal(reducedMotion.scrollBehavior, "auto");
    for (const [name, seconds] of Object.entries(reducedMotion).filter(
      ([name]) => name.endsWith("Seconds"),
    )) {
      assert.ok(seconds <= 0.001, `${name} remained ${seconds} seconds`);
    }
    await client.call("Emulation.setEmulatedMedia", { features: [] });

    await evaluate(`location.hash = "#settings"`);
    await waitFor(
      () => evaluate(`document.querySelector("#settings-view")?.hidden === false`),
      "Settings for colour-contrast checks",
    );
    for (const theme of ["light", "dark"]) {
      await evaluate(
        `document.querySelector('[data-theme-value="${theme}"]').click()`,
      );
      await waitFor(
        () =>
          evaluate(
            `document.documentElement.dataset.theme === ${JSON.stringify(theme)}`,
          ),
        `${theme} theme`,
      );
      await new Promise((resolveThemeTransition) =>
        setTimeout(resolveThemeTransition, 220),
      );
      const contrast = await evaluate(`(() => {
        const channels = (value) => {
          const match = value.match(/[\\d.]+/g);
          if (!match || match.length < 3) throw new Error("Unsupported colour: " + value);
          return match.slice(0, 3).map(Number);
        };
        const luminance = (value) => {
          const linear = channels(value).map((channel) => {
            const ratio = channel / 255;
            return ratio <= 0.04045
              ? ratio / 12.92
              : Math.pow((ratio + 0.055) / 1.055, 2.4);
          });
          return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
        };
        const ratio = (foreground, background) => {
          const first = luminance(foreground);
          const second = luminance(background);
          return (Math.max(first, second) + 0.05) /
            (Math.min(first, second) + 0.05);
        };
        const pair = (foreground, background) => ({
          foreground,
          background,
          ratio: ratio(foreground, background),
        });
        const bodyStyle = getComputedStyle(document.body);
        const card = document.querySelector(".settings-card");
        const cardStyle = getComputedStyle(card);
        const cardHeadingStyle = getComputedStyle(card.querySelector("h2"));
        const cardParagraphStyle = getComputedStyle(card.querySelector("p"));
        const primaryStyle = getComputedStyle(
          document.querySelector("#install-button")
        );
        const quietStyle = getComputedStyle(
          document.querySelector("#export-progress")
        );
        return {
          theme: document.documentElement.dataset.theme,
          forest: getComputedStyle(document.documentElement)
            .getPropertyValue("--forest").trim(),
          paper: getComputedStyle(document.documentElement)
            .getPropertyValue("--paper").trim(),
          pairs: {
            body: pair(bodyStyle.color, bodyStyle.backgroundColor),
            cardHeading: pair(cardHeadingStyle.color, cardStyle.backgroundColor),
            cardParagraph: pair(cardParagraphStyle.color, cardStyle.backgroundColor),
            primaryButton: pair(
              primaryStyle.color,
              primaryStyle.backgroundColor
            ),
            quietButton: pair(quietStyle.color, quietStyle.backgroundColor),
          },
        };
      })()`);
      assert.equal(contrast.theme, theme);
      for (const [pairName, colours] of Object.entries(contrast.pairs)) {
        assert.ok(
          colours.ratio >= 4.5,
          `${theme} ${pairName} contrast was ${colours.ratio.toFixed(2)}:1 (${colours.foreground} on ${colours.background}; --forest ${contrast.forest}; --paper ${contrast.paper})`,
        );
      }
    }

    await evaluate(`(() => {
      const range = document.querySelector("#font-size");
      range.value = "125";
      range.dispatchEvent(new Event("input", { bubbles: true }));
    })()`);
    await waitFor(
      () =>
        evaluate(`document.querySelector("#font-size-output").value === "125%" &&
          JSON.parse(localStorage.getItem("ai-workflow-course-state-v1")).state.fontSize === 125`),
      "125 percent reader text setting",
    );
    await evaluate(
      `location.hash = ${JSON.stringify(`#doc=${tableDocumentId}`)}`,
    );
    await waitFor(
      () =>
        evaluate(`document.querySelector("#reader-view")?.hidden === false &&
          Boolean(document.querySelector("#reader-content table"))`),
      "Reader page with a table",
    );
    const enlargedReader = await evaluate(`(() => {
      const content = document.querySelector("#reader-content");
      const table = content.querySelector("table");
      const wrapper = table.closest(".table-wrap");
      const contentRect = content.getBoundingClientRect();
      const wrapperRect = wrapper.getBoundingClientRect();
      return {
        scale: getComputedStyle(document.documentElement)
          .getPropertyValue("--reader-scale").trim(),
        fontSize: parseFloat(getComputedStyle(content).fontSize),
        viewport: innerWidth,
        pageScrollWidth: document.documentElement.scrollWidth,
        readerScrollWidth: document.querySelector("#reader-view").scrollWidth,
        wrapperIsParent: table.parentElement === wrapper,
        wrapperOverflowX: getComputedStyle(wrapper).overflowX,
        wrapperInsideReader:
          wrapperRect.left >= contentRect.left - 0.5 &&
          wrapperRect.right <= contentRect.right + 0.5,
        wrapperClientWidth: wrapper.clientWidth,
        contentClientWidth: content.clientWidth,
      };
    })()`);
    assert.equal(enlargedReader.scale, "1.25");
    assert.ok(
      enlargedReader.fontSize >= 20,
      `125% reader text rendered at only ${enlargedReader.fontSize}px`,
    );
    assert.ok(enlargedReader.pageScrollWidth <= enlargedReader.viewport);
    assert.ok(enlargedReader.readerScrollWidth <= enlargedReader.viewport);
    assert.equal(enlargedReader.wrapperIsParent, true);
    assert.equal(enlargedReader.wrapperOverflowX, "auto");
    assert.equal(enlargedReader.wrapperInsideReader, true);
    assert.ok(
      enlargedReader.wrapperClientWidth <= enlargedReader.contentClientWidth,
    );

    for (const documentId of learningSequenceIds) {
      await evaluate(`location.hash = ${JSON.stringify(`#doc=${documentId}`)}`);
      await waitFor(
        () =>
          evaluate(
            `location.hash === ${JSON.stringify(`#doc=${documentId}`)} &&
              document.querySelector("#reader-view")?.hidden === false &&
              document.querySelector("#reader-content")?.textContent.length > 0`,
          ),
        `Required page ${documentId}`,
      );
      const readerLayout = await evaluate(`(() => ({
        viewport: innerWidth,
        page: document.documentElement.scrollWidth,
        reader: document.querySelector("#reader-view").scrollWidth,
        h1Count: document.querySelector("#reader-view").querySelectorAll("h1").length,
      }))()`);
      assert.ok(
        readerLayout.page <= readerLayout.viewport,
        `${documentId} overflowed the 320 CSS-pixel/200%-reflow viewport`,
      );
      assert.ok(
        readerLayout.reader <= readerLayout.viewport,
        `${documentId} reader overflowed its viewport`,
      );
      assert.equal(
        readerLayout.h1Count,
        1,
        `${documentId} must expose exactly one reader h1`,
      );
    }

    await evaluate(`location.hash = "#doc=course-1-foundation-01"`);
    await waitFor(
      () =>
        evaluate(
          `document.querySelector("#reader-title")?.textContent.includes("Files")`,
        ),
      "Foundation 1 reader",
    );
    await evaluate(`document.querySelector(".skip-link").click()`);
    await waitFor(
      () =>
        evaluate(`location.hash === "#doc=course-1-foundation-01" &&
          document.querySelector("#reader-view")?.hidden === false &&
          document.activeElement === document.querySelector("#main-content")`),
      "Skip link preserves the active lesson route",
    );
    const reader = await evaluate(`(() => ({
      text: document.querySelector("#reader-content").textContent,
      meta: document.querySelector("#reader-meta").textContent,
      practicalPanelHidden: document.querySelector("#practical-pass-panel").hidden,
    }))()`);
    assert.ok(reader.text.includes("All files (*.*)"));
    assert.ok(!reader.text.includes("All files (.)"));
    assert.match(reader.meta, /Read: about \d+ minutes?/);
    assert.match(
      reader.meta,
      /Practice — AUTHOR ESTIMATE, NOT BEGINNER MEASURED: \d+–\d+ hours/,
    );
    assert.equal(reader.practicalPanelHidden, false);

    if (
      await evaluate(
        `document.querySelector("#complete-button").getAttribute("aria-pressed") === "true"`,
      )
    ) {
      await evaluate(`document.querySelector("#complete-button").click()`);
    }
    if (
      await evaluate(
        `document.querySelector("#practical-pass-button").getAttribute("aria-pressed") === "true"`,
      )
    ) {
      await evaluate(`document.querySelector("#practical-pass-button").click()`);
    }
    await evaluate(`document.querySelector("#complete-button").click()`);
    await waitFor(
      () =>
        evaluate(
          `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1")).state
            .completed.includes("course-1-foundation-01")`,
        ),
      "Page-read state",
    );
    await waitFor(
      () =>
        evaluate(
          `document.querySelector("#practical-pass-panel").hidden === false &&
            document.querySelector("#practical-pass-button")
              .getAttribute("aria-pressed") === "false"`,
        ),
      "Unrecorded practical button",
    );
    await evaluate(`document.querySelector("#practical-pass-button").click()`);
    await waitFor(
      () =>
        evaluate(
          `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1")).state
            .practicalPassed.includes("course-1-foundation-01")`,
        ),
      "Practical self-check state",
    );
    const stored = await evaluate(
      `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1")).state`,
    );
    assert.ok(
      stored.completed.includes("course-1-foundation-01"),
      `page-read state was ${JSON.stringify(stored.completed)}`,
    );
    assert.ok(
      stored.practicalPassed.includes("course-1-foundation-01"),
      `practical state was ${JSON.stringify(stored.practicalPassed)}`,
    );
    assert.ok(stored.completionRevisions["course-1-foundation-01"]);
    assert.ok(stored.practicalPassRevisions["course-1-foundation-01"]);

    await evaluate(`document.querySelector("#export-progress").click()`);
    const backupFileName = await waitFor(async () => {
      const names = await readdir(downloadDirectory);
      return names.find((name) => name.endsWith(".json"));
    }, "Progress-backup download");
    const backupPayload = JSON.parse(
      await readFile(join(downloadDirectory, backupFileName), "utf8"),
    );
    assert.equal(backupPayload.exportType, "ai-workflow-course-progress");
    assert.equal(backupPayload.courseId, bundledCourse.course.id);
    assert.ok(
      backupPayload.state.completed.includes("course-1-foundation-01"),
    );
    assert.ok(
      backupPayload.state.practicalPassed.includes("course-1-foundation-01"),
    );

    await evaluate(`location.hash = "#career"`);
    await waitFor(
      () =>
        evaluate(
          `document.querySelector(".later-course-disclosure summary")?.textContent.includes("later-course prototype")`,
        ),
      "Career path",
    );
    await assertReleaseBoundary("Career");
    assert.equal(
      await evaluate(
        `document.querySelector(".later-course-disclosure") instanceof HTMLDetailsElement`,
      ),
      true,
    );
    await evaluate(
      `document.querySelector(".later-course-disclosure summary").focus()`,
    );
    assert.equal(
      await evaluate(
        `document.activeElement === document.querySelector(".later-course-disclosure summary")`,
      ),
      true,
    );
    await client.call("Input.dispatchKeyEvent", {
      type: "rawKeyDown",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    await client.call("Input.dispatchKeyEvent", {
      type: "char",
      text: " ",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    await client.call("Input.dispatchKeyEvent", {
      type: "keyUp",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    assert.equal(
      await evaluate(`document.querySelector(".later-course-disclosure").open`),
      true,
    );

    await evaluate(
      `document.querySelector('.bottom-nav [data-route="settings"]').focus()`,
    );
    await client.call("Input.dispatchKeyEvent", {
      type: "rawKeyDown",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    await client.call("Input.dispatchKeyEvent", {
      type: "char",
      text: " ",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    await client.call("Input.dispatchKeyEvent", {
      type: "keyUp",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    await waitFor(
      () =>
        evaluate(
          `location.hash === "#settings" &&
            document.querySelector("#settings-view")?.hidden === false`,
        ),
      "Keyboard navigation to Settings",
    );
    await assertReleaseBoundary("Settings");
    assert.deepEqual(
      await evaluate(`({
        productStatus:
          document.querySelector("#settings-product-status")?.textContent?.trim(),
        distributionPurpose:
          document.querySelector("#settings-distribution-purpose")?.textContent?.trim()
      })`),
      {
        productStatus: "UNVERIFIED",
        distributionPurpose: "Personal study with synthetic data only",
      },
    );
    await waitFor(
      () =>
        evaluate(
          `document.activeElement === document.querySelector("#settings-view h1")`,
        ),
      "Route heading focus",
    );
    await evaluate(`history.back()`);
    await waitFor(
      () =>
        evaluate(
          `location.hash === "#career" &&
            document.querySelector("#career-view")?.hidden === false &&
            document.activeElement === document.querySelector("#career-view h1")`,
        ),
      "Browser Back route heading focus",
    );
    await evaluate(`history.forward()`);
    await waitFor(
      () =>
        evaluate(
          `location.hash === "#settings" &&
            document.querySelector("#settings-view")?.hidden === false &&
            document.activeElement === document.querySelector("#settings-view h1")`,
        ),
      "Browser Forward route heading focus",
    );
    await evaluate(`document.querySelector("#menu-button").focus()`);
    await client.call("Input.dispatchKeyEvent", {
      type: "rawKeyDown",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    await client.call("Input.dispatchKeyEvent", {
      type: "char",
      text: " ",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    await client.call("Input.dispatchKeyEvent", {
      type: "keyUp",
      key: " ",
      code: "Space",
      windowsVirtualKeyCode: 32,
    });
    await waitFor(
      () => evaluate(`document.body.classList.contains("sidebar-open")`),
      "Keyboard-opened course menu",
    );
    assert.equal(
      await evaluate(
        `document.activeElement === document.querySelector("#sidebar-close-button")`,
      ),
      true,
    );
    await pressKey({
      key: "Tab",
      code: "Tab",
      windowsVirtualKeyCode: 9,
      modifiers: 8,
    });
    assert.equal(
      await evaluate(`(() => {
        const focusable = [...document.querySelector("#course-sidebar")
          .querySelectorAll("button:not([disabled]), a[href]")]
          .filter((element) =>
            !element.closest("[hidden]") && element.getClientRects().length
          );
        return document.activeElement === focusable.at(-1);
      })()`),
      true,
    );
    await pressKey({
      key: "Tab",
      code: "Tab",
      windowsVirtualKeyCode: 9,
    });
    assert.equal(
      await evaluate(
        `document.activeElement === document.querySelector("#sidebar-close-button")`,
      ),
      true,
    );
    await client.call("Input.dispatchKeyEvent", {
      type: "keyDown",
      key: "Escape",
      code: "Escape",
      windowsVirtualKeyCode: 27,
    });
    await client.call("Input.dispatchKeyEvent", {
      type: "keyUp",
      key: "Escape",
      code: "Escape",
      windowsVirtualKeyCode: 27,
    });
    await waitFor(
      () => evaluate(`!document.body.classList.contains("sidebar-open")`),
      "Keyboard-closed course menu",
    );
    assert.equal(
      await evaluate(
        `document.activeElement === document.querySelector("#menu-button")`,
      ),
      true,
    );

    await evaluate(`window.confirm = () => {
        throw new Error("Native confirm must not be used.");
      };
      document.querySelector("#reset-progress").click();`);
    await approveActionDialog("Confirmed reset");
    await waitFor(
      () =>
        evaluate(`(() => {
          const stored = localStorage.getItem("ai-workflow-course-state-v1");
          return location.hash === "#home" &&
            (!stored || JSON.parse(stored).state.completed.length === 0);
        })()`),
      "Confirmed reset and Home route",
    );

    const backupText = JSON.stringify(backupPayload);
    await evaluate(`(() => {
      const input = document.querySelector("#import-progress");
      const transfer = new DataTransfer();
      transfer.items.add(new File(
        [${JSON.stringify(backupText)}],
        "course-progress.json",
        { type: "application/json" }
      ));
      input.files = transfer.files;
      input.dispatchEvent(new Event("change", { bubbles: true }));
    })()`);
    await approveActionDialog("Progress import");
    await waitFor(
      () =>
        evaluate(`JSON.parse(localStorage.getItem("ai-workflow-course-state-v1")).state
          .practicalPassed.includes("course-1-foundation-01")`),
      "Progress-backup import",
    );

    const wrongCoursePayload = {
      ...backupPayload,
      courseId: "different-course",
    };
    const stateBeforeWrongImport = await evaluate(
      `localStorage.getItem("ai-workflow-course-state-v1")`,
    );
    await evaluate(`(() => {
      const input = document.querySelector("#import-progress");
      const transfer = new DataTransfer();
      transfer.items.add(new File(
        [${JSON.stringify(JSON.stringify(wrongCoursePayload))}],
        "wrong-course.json",
        { type: "application/json" }
      ));
      input.files = transfer.files;
      input.dispatchEvent(new Event("change", { bubbles: true }));
    })()`);
    await waitFor(
      () =>
        evaluate(
          `document.querySelector("#toast").textContent.includes("Not a supported")`,
        ),
      "Wrong-course backup rejection",
    );
    assert.equal(
      await evaluate(`localStorage.getItem("ai-workflow-course-state-v1")`),
      stateBeforeWrongImport,
    );

    const changedBackupPayload = JSON.parse(backupText);
    changedBackupPayload.state.notes["course-1-foundation-01"] =
      "This must not survive a failed save.";
    const stateBeforeFailedSave = await evaluate(
      `localStorage.getItem("ai-workflow-course-state-v1")`,
    );
    const blockedStorageImportDiagnostic = () =>
      evaluate(`(() => {
        const probe = window.__blockedStorageImportProbe;
        const input = document.querySelector("#import-progress");
        const dialog = document.querySelector("#action-confirmation-dialog");
        return {
          probePresent: Boolean(probe),
          stubInstalled: Boolean(
            probe && Storage.prototype.setItem === probe.stubSetItem
          ),
          setItemCalls: probe?.setItemCalls || [],
          toast: document.querySelector("#toast")?.textContent || "",
          toastHidden: document.querySelector("#toast")?.hidden ?? null,
          inputValue: input?.value ?? null,
          inputFiles: input
            ? [...input.files].map((file) => ({
                name: file.name,
                size: file.size,
                type: file.type
              }))
            : null,
          dialogExists: Boolean(dialog),
          dialogOpen: dialog?.open ?? null,
          dialogTitle:
            dialog?.querySelector("#action-confirmation-title")
              ?.textContent || "",
          activeElement: document.activeElement?.id || "",
          storage: {
            primary: localStorage.getItem("ai-workflow-course-state-v1"),
            recovery: localStorage.getItem(
              "ai-workflow-course-recovery-v1"
            ),
            barrier: localStorage.getItem(
              "ai-workflow-course-reset-barrier-v1"
            )
          },
          location: location.href,
          readyState: document.readyState
        };
      })()`);
    let blockedStorageImportError = null;
    let blockedStorageFailureDiagnostic = null;
    let blockedStorageImportResult = null;
    let blockedStorageCleanup = null;
    try {
      await evaluate(`(() => {
        if (window.__blockedStorageImportProbe) {
          throw new Error("Blocked-storage import probe was already installed.");
        }
        const originalSetItem = Storage.prototype.setItem;
        const probe = {
          originalSetItem,
          setItemCalls: []
        };
        probe.stubSetItem = function (key) {
          probe.setItemCalls.push({
            key: String(key),
            storageArea:
              this === localStorage
                ? "localStorage"
                : this === sessionStorage
                  ? "sessionStorage"
                  : "other"
          });
          throw new DOMException("Storage is blocked.", "QuotaExceededError");
        };
        window.__blockedStorageImportProbe = probe;
        Storage.prototype.setItem = probe.stubSetItem;
        const toast = document.querySelector("#toast");
        toast.hidden = true;
        toast.textContent = "";
        const input = document.querySelector("#import-progress");
        const transfer = new DataTransfer();
        transfer.items.add(new File(
          [${JSON.stringify(JSON.stringify(changedBackupPayload))}],
          "blocked-save.json",
          { type: "application/json" }
        ));
        input.files = transfer.files;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      })()`);
      await approveActionDialog("Blocked-storage import");
      blockedStorageImportResult = await waitFor(
        async () => {
          const diagnostic = await blockedStorageImportDiagnostic();
          const deniedLocalStorageWrite = diagnostic.setItemCalls.some(
            (call) => call.storageArea === "localStorage",
          );
          const importFinished =
            diagnostic.inputValue === "" &&
            diagnostic.dialogOpen !== true;
          return deniedLocalStorageWrite && importFinished
            ? diagnostic
            : null;
        },
        "Blocked-storage import completion",
      );
      assert.equal(
        blockedStorageImportResult.stubInstalled,
        true,
        "The full Storage.prototype.setItem denial was not active through import completion.",
      );
      assert.match(
        blockedStorageImportResult.toast,
        /backup was not imported/i,
      );
      assert.equal(
        blockedStorageImportResult.storage.primary,
        stateBeforeFailedSave,
      );
    } catch (error) {
      blockedStorageImportError = error;
      try {
        blockedStorageFailureDiagnostic =
          await blockedStorageImportDiagnostic();
      } catch (diagnosticError) {
        blockedStorageFailureDiagnostic = {
          diagnosticError: diagnosticError.message
        };
      }
    } finally {
      try {
        blockedStorageCleanup = await evaluate(`(() => {
          const probe = window.__blockedStorageImportProbe;
          if (!probe) {
            return {
              probePresent: false,
              stubWasInstalled: false,
              restored: false,
              setItemCalls: []
            };
          }
          const stubWasInstalled =
            Storage.prototype.setItem === probe.stubSetItem;
          Storage.prototype.setItem = probe.originalSetItem;
          const restored =
            Storage.prototype.setItem === probe.originalSetItem;
          const setItemCalls = [...probe.setItemCalls];
          delete window.__blockedStorageImportProbe;
          return {
            probePresent: true,
            stubWasInstalled,
            restored,
            setItemCalls
          };
        })()`);
      } catch (error) {
        blockedStorageImportError ||= error;
        if (!blockedStorageFailureDiagnostic) {
          try {
            blockedStorageFailureDiagnostic =
              await blockedStorageImportDiagnostic();
          } catch (diagnosticError) {
            blockedStorageFailureDiagnostic = {
              diagnosticError: diagnosticError.message
            };
          }
        }
      }
    }
    if (blockedStorageImportError) {
      throw new Error(
        `${blockedStorageImportError.message} ` +
          `State=${JSON.stringify(blockedStorageFailureDiagnostic)} ` +
          `Cleanup=${JSON.stringify(blockedStorageCleanup)}`,
      );
    }
    assert.equal(
      blockedStorageCleanup?.stubWasInstalled,
      true,
      "The blocked-storage stub was replaced before test cleanup.",
    );
    assert.equal(
      blockedStorageCleanup?.restored,
      true,
      "Storage.prototype.setItem was not restored after the blocked-storage import.",
    );
    assert.ok(
      blockedStorageCleanup.setItemCalls.some(
        (call) => call.storageArea === "localStorage",
      ),
      "The blocked-storage import did not exercise a denied localStorage write.",
    );

    const transactionImportSnapshot = await evaluate(`({
      primary: localStorage.getItem("ai-workflow-course-state-v1"),
      recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
      barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1")
    })`);
    await evaluate(`(() => {
      window.__originalStorageRemoveItem = Storage.prototype.removeItem;
      let failedOnce = false;
      Storage.prototype.removeItem = function (key) {
        if (
          !failedOnce &&
          key === "ai-workflow-course-recovery-v1"
        ) {
          failedOnce = true;
          throw new DOMException("Simulated finalisation failure.", "QuotaExceededError");
        }
        return window.__originalStorageRemoveItem.call(this, key);
      };
      const input = document.querySelector("#import-progress");
      const transfer = new DataTransfer();
      transfer.items.add(new File(
        [${JSON.stringify(JSON.stringify(changedBackupPayload))}],
        "rollback-import.json",
        { type: "application/json" }
      ));
      input.files = transfer.files;
      input.dispatchEvent(new Event("change", { bubbles: true }));
    })()`);
    await approveActionDialog("Rollback import");
    const rollbackImportMessage = await waitFor(
      async () => {
        const message = await evaluate(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        return /backup was not imported/i.test(message) ? message : null;
      },
      "Rolled-back import result",
    );
    await evaluate(`(() => {
      Storage.prototype.removeItem = window.__originalStorageRemoveItem;
      delete window.__originalStorageRemoveItem;
    })()`);
    assert.match(rollbackImportMessage, /overall rollback: verified/i);
    assert.match(rollbackImportMessage, /primary data: restored/i);
    assert.match(rollbackImportMessage, /visible course: restored/i);
    assert.deepEqual(
      await evaluate(`({
        primary: localStorage.getItem("ai-workflow-course-state-v1"),
        recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
        barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1")
      })`),
      transactionImportSnapshot,
    );

    const renderImportSnapshot = await evaluate(`({
      primary: localStorage.getItem("ai-workflow-course-state-v1"),
      recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
      barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1"),
      route: location.hash,
      fontValue: document.querySelector("#font-size-output").value,
      theme: document.documentElement.dataset.theme,
      title: document.title
    })`);
    const renderFailureImportPayload = structuredClone(changedBackupPayload);
    renderFailureImportPayload.state.fontSize =
      Number(renderImportSnapshot.fontValue.replace("%", "")) === 90 ? 125 : 90;
    renderFailureImportPayload.state.theme =
      renderImportSnapshot.theme === "dark" ? "light" : "dark";
    await evaluate(`(() => {
      const originalReplaceChildren = Element.prototype.replaceChildren;
      let injected = false;
      Element.prototype.replaceChildren = function (...nodes) {
        if (!injected && this.id === "course-nav") {
          injected = true;
          Element.prototype.replaceChildren = originalReplaceChildren;
          throw new Error("Simulated render-stage import failure.");
        }
        return originalReplaceChildren.apply(this, nodes);
      };
      const input = document.querySelector("#import-progress");
      const transfer = new DataTransfer();
      transfer.items.add(new File(
        [${JSON.stringify(JSON.stringify(renderFailureImportPayload))}],
        "render-failure-import.json",
        { type: "application/json" }
      ));
      input.files = transfer.files;
      input.dispatchEvent(new Event("change", { bubbles: true }));
    })()`);
    await approveActionDialog("Render-failure import");
    const renderImportFailureMessage = await waitFor(
      async () => {
        const message = await evaluate(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        return /backup was not imported/i.test(message) ? message : null;
      },
      "Render-stage import rollback result",
    );
    assert.match(renderImportFailureMessage, /overall rollback: verified/i);
    assert.match(renderImportFailureMessage, /visible course: restored/i);
    assert.deepEqual(
      await evaluate(`({
        primary: localStorage.getItem("ai-workflow-course-state-v1"),
        recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
        barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1"),
        route: location.hash,
        fontValue: document.querySelector("#font-size-output").value,
        theme: document.documentElement.dataset.theme,
        title: document.title
      })`),
      renderImportSnapshot,
    );

    const resetRecoverySentinel = JSON.stringify({
      recoveryType: "test-existing-recovery",
      savedAt: "2026-07-28T12:00:00.000Z",
      raw: transactionImportSnapshot.primary,
    });
    await evaluate(
      `localStorage.setItem("ai-workflow-course-recovery-v1", ${JSON.stringify(resetRecoverySentinel)})`,
    );
    const resetTransactionSnapshot = await evaluate(`({
      primary: localStorage.getItem("ai-workflow-course-state-v1"),
      recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
      barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1")
    })`);
    await evaluate(`(() => {
      window.__originalStorageSetItem = Storage.prototype.setItem;
      let failedOnce = false;
      Storage.prototype.setItem = function (key, value) {
        if (
          !failedOnce &&
          key === "ai-workflow-course-reset-barrier-v1"
        ) {
          failedOnce = true;
          throw new DOMException("Simulated reset failure.", "QuotaExceededError");
        }
        return window.__originalStorageSetItem.call(this, key, value);
      };
      document.querySelector("#reset-progress").click();
    })()`);
    await approveActionDialog("Rollback reset");
    const rollbackResetMessage = await waitFor(
      async () => {
        const message = await evaluate(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        return /nothing was reset/i.test(message) ? message : null;
      },
      "Rolled-back reset result",
    );
    await evaluate(`(() => {
      Storage.prototype.setItem = window.__originalStorageSetItem;
      delete window.__originalStorageSetItem;
    })()`);
    assert.match(rollbackResetMessage, /overall rollback: verified/i);
    assert.match(rollbackResetMessage, /primary data: restored/i);
    assert.match(rollbackResetMessage, /visible course: restored/i);
    assert.deepEqual(
      await evaluate(`({
        primary: localStorage.getItem("ai-workflow-course-state-v1"),
        recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
        barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1")
      })`),
      resetTransactionSnapshot,
    );

    const renderResetSnapshot = await evaluate(`({
      primary: localStorage.getItem("ai-workflow-course-state-v1"),
      recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
      barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1"),
      route: location.hash,
      fontValue: document.querySelector("#font-size-output").value,
      theme: document.documentElement.dataset.theme,
      title: document.title
    })`);
    await evaluate(`(() => {
      const originalReplaceChildren = Element.prototype.replaceChildren;
      let injected = false;
      Element.prototype.replaceChildren = function (...nodes) {
        if (!injected && this.id === "course-nav") {
          injected = true;
          Element.prototype.replaceChildren = originalReplaceChildren;
          throw new Error("Simulated render-stage reset failure.");
        }
        return originalReplaceChildren.apply(this, nodes);
      };
      document.querySelector("#reset-progress").click();
    })()`);
    await approveActionDialog("Render-failure reset");
    const renderResetFailureMessage = await waitFor(
      async () => {
        const message = await evaluate(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        return /nothing was reset/i.test(message) ? message : null;
      },
      "Render-stage reset rollback result",
    );
    assert.match(
      renderResetFailureMessage,
      /visible course: restored/i,
    );
    assert.match(renderResetFailureMessage, /overall rollback: verified/i);
    assert.deepEqual(
      await evaluate(`({
        primary: localStorage.getItem("ai-workflow-course-state-v1"),
        recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
        barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1"),
        route: location.hash,
        fontValue: document.querySelector("#font-size-output").value,
        theme: document.documentElement.dataset.theme,
        title: document.title
      })`),
      renderResetSnapshot,
    );

    const raceTargetsBeforeOpen = new Set(
      (
        await (
          await fetch(`http://127.0.0.1:${debugPort}/json/list`)
        ).json()
      ).map((candidate) => candidate.id),
    );
    assert.equal(
      await evaluate(`(() => {
        window.__rollbackRaceWindow = window.open(
          ${JSON.stringify(previewUrl)},
          "_blank"
        );
        return window.__rollbackRaceWindow !== null;
      })()`),
      true,
    );
    const raceTarget = await waitFor(async () => {
      const response = await fetch(`http://127.0.0.1:${debugPort}/json/list`);
      if (!response.ok) return null;
      const targets = await response.json();
      return targets.find(
        (candidate) =>
          candidate.type === "page" &&
          !raceTargetsBeforeOpen.has(candidate.id) &&
          candidate.url.startsWith(previewUrl),
      );
    }, "Combined rollback-race course window");
    secondTargetId = raceTarget.id;
    secondClient = await createCdpClient(raceTarget.webSocketDebuggerUrl);
    await secondClient.call("Page.enable");
    await secondClient.call("Runtime.enable");
    await waitFor(
      () =>
        evaluateSecond(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          navigator.serviceWorker?.controller !== null`),
      "Combined rollback-race controlled window",
    );
    const recoveryInjectionReason =
      "Test harness injected one external recovery after the reset barrier; this write is not attributed to the product.";
    const injectionSetup = await evaluateSecond(`(() => {
        const storageKey = "ai-workflow-course-state-v1";
        const recoveryKey = "ai-workflow-course-recovery-v1";
        const barrierKey = "ai-workflow-course-reset-barrier-v1";
        const baseRaw = localStorage.getItem(storageKey);
        const recoveryBefore = localStorage.getItem(recoveryKey);
        let injectionCount = 0;
        window.__injectExternalRecoveryAfterResetBarrier = () => {
          const barrierRaw = localStorage.getItem(barrierKey);
          if (!barrierRaw) {
            throw new Error("The reset barrier was not visible in window B.");
          }
          injectionCount += 1;
          const recovery = JSON.stringify({
            recoveryType: "course-state-recovery",
            savedAt: "2026-07-29T00:00:00.000Z",
            reason: ${JSON.stringify(recoveryInjectionReason)},
            raw: baseRaw,
          });
          localStorage.setItem(recoveryKey, recovery);
          if (localStorage.getItem(recoveryKey) !== recovery) {
            throw new Error("Window B could not verify its injected recovery.");
          }
          window.__externalRecoveryInjection = {
            injectionCount,
            recoveryBefore,
            recoveryAfter: recovery,
            primaryAtInjection: localStorage.getItem(storageKey),
            barrierAtInjection: barrierRaw,
            reason: ${JSON.stringify(recoveryInjectionReason)}
          };
          return recovery;
        };
        return { baseRaw, recoveryBefore };
      })()`);
    const combinedRaceSnapshot = await evaluate(`({
      primary: localStorage.getItem("ai-workflow-course-state-v1"),
      recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
      barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1"),
      route: location.hash,
      fontValue: document.querySelector("#font-size-output").value,
      theme: document.documentElement.dataset.theme,
      title: document.title
    })`);
    await evaluate(`(() => {
      const originalReplaceChildren = Element.prototype.replaceChildren;
      let injected = false;
      Element.prototype.replaceChildren = function (...nodes) {
        if (!injected && this.id === "course-nav") {
          injected = true;
          Element.prototype.replaceChildren = originalReplaceChildren;
          window.__combinedRaceRecovery =
            window.__rollbackRaceWindow
              .__injectExternalRecoveryAfterResetBarrier();
          throw new Error(
            "Simulated render-stage reset failure after window B recovery."
          );
        }
        return originalReplaceChildren.apply(this, nodes);
      };
      document.querySelector("#reset-progress").click();
    })()`);
    await approveActionDialog("Combined two-window render-failure reset");
    const combinedRaceMessage = await waitFor(
      async () => {
        const message = await evaluate(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        return /overall rollback: verified/i.test(message) ? message : null;
      },
      "Combined two-window render-failure rollback result",
    );
    assert.match(
      combinedRaceMessage,
      /recovery copy: changed externally and preserved/i,
    );
    assert.match(combinedRaceMessage, /primary data: restored/i);
    assert.match(combinedRaceMessage, /reset barrier: restored/i);
    assert.match(combinedRaceMessage, /runtime state: restored/i);
    assert.match(combinedRaceMessage, /visible course: restored/i);
    const combinedRaceResult = await evaluate(`(() => {
      const recovery = localStorage.getItem(
        "ai-workflow-course-recovery-v1"
      );
      return {
        primary: localStorage.getItem("ai-workflow-course-state-v1"),
        recovery,
        barrier: localStorage.getItem(
          "ai-workflow-course-reset-barrier-v1"
        ),
        route: location.hash,
        fontValue: document.querySelector("#font-size-output").value,
        theme: document.documentElement.dataset.theme,
        title: document.title,
        injectedRecovery: window.__combinedRaceRecovery
      };
    })()`);
    const recoveryInjectionEvidence = await evaluateSecond(
      `window.__externalRecoveryInjection`,
    );
    assert.equal(combinedRaceResult.primary, combinedRaceSnapshot.primary);
    assert.equal(combinedRaceResult.barrier, combinedRaceSnapshot.barrier);
    assert.equal(combinedRaceResult.route, combinedRaceSnapshot.route);
    assert.equal(combinedRaceResult.fontValue, combinedRaceSnapshot.fontValue);
    assert.equal(combinedRaceResult.theme, combinedRaceSnapshot.theme);
    assert.equal(combinedRaceResult.title, combinedRaceSnapshot.title);
    assert.equal(
      combinedRaceResult.recovery,
      combinedRaceResult.injectedRecovery,
      "Rollback overwrote the recovery copy written by window B.",
    );
    assert.notEqual(
      combinedRaceResult.recovery,
      combinedRaceSnapshot.recovery,
      "The combined regression did not create a distinct concurrent recovery.",
    );
    assert.equal(recoveryInjectionEvidence.injectionCount, 1);
    assert.equal(
      recoveryInjectionEvidence.recoveryBefore,
      combinedRaceSnapshot.recovery,
    );
    assert.equal(
      recoveryInjectionEvidence.recoveryAfter,
      combinedRaceResult.recovery,
    );
    assert.equal(recoveryInjectionEvidence.reason, recoveryInjectionReason);
    assert.equal(injectionSetup.baseRaw, combinedRaceSnapshot.primary);
    assert.equal(injectionSetup.recoveryBefore, combinedRaceSnapshot.recovery);
    assert.notEqual(
      recoveryInjectionEvidence.barrierAtInjection,
      combinedRaceSnapshot.barrier,
      "The harness recovery was not deterministically injected after the reset barrier.",
    );
    assert.notEqual(
      recoveryInjectionEvidence.primaryAtInjection,
      combinedRaceSnapshot.primary,
      "The harness recovery was not deterministically injected after the reset primary write.",
    );
    await client.call("Target.closeTarget", { targetId: secondTargetId });
    secondClient?.close();
    secondClient = null;
    secondTargetId = null;
    await evaluate(`(() => {
      const recoveryKey = "ai-workflow-course-recovery-v1";
      const previousRecovery = ${JSON.stringify(combinedRaceSnapshot.recovery)};
      if (previousRecovery === null) localStorage.removeItem(recoveryKey);
      else localStorage.setItem(recoveryKey, previousRecovery);
      delete window.__combinedRaceRecovery;
      delete window.__rollbackRaceWindow;
    })()`);

    const externalKeyPlan = await evaluate(`(() => {
      const primaryBefore = localStorage.getItem(
        "ai-workflow-course-state-v1"
      );
      const recoveryBefore = localStorage.getItem(
        "ai-workflow-course-recovery-v1"
      );
      const barrierBefore = localStorage.getItem(
        "ai-workflow-course-reset-barrier-v1"
      );
      const primaryEnvelope = JSON.parse(primaryBefore);
      primaryEnvelope.revision += 1000;
      primaryEnvelope.writerId = "test-harness-external-primary";
      const barrierEnvelope = structuredClone(primaryEnvelope);
      barrierEnvelope.revision += 1;
      barrierEnvelope.writerId = "test-harness-external-barrier";
      barrierEnvelope.state.resetEpoch = "test-harness-external-reset";
      return {
        primaryBefore,
        recoveryBefore,
        barrierBefore,
        primaryExternal: JSON.stringify(primaryEnvelope),
        barrierExternal: JSON.stringify(barrierEnvelope)
      };
    })()`);
    await evaluate(`(() => {
      const plan = ${JSON.stringify(externalKeyPlan)};
      const originalReplaceChildren = Element.prototype.replaceChildren;
      let injectionCount = 0;
      Element.prototype.replaceChildren = function (...nodes) {
        if (injectionCount === 0 && this.id === "course-nav") {
          injectionCount += 1;
          Element.prototype.replaceChildren = originalReplaceChildren;
          localStorage.setItem(
            "ai-workflow-course-state-v1",
            plan.primaryExternal
          );
          localStorage.setItem(
            "ai-workflow-course-reset-barrier-v1",
            plan.barrierExternal
          );
          window.__externalOwnedKeyInjection = {
            injectionCount,
            primaryAfter: localStorage.getItem(
              "ai-workflow-course-state-v1"
            ),
            barrierAfter: localStorage.getItem(
              "ai-workflow-course-reset-barrier-v1"
            ),
            recoveryAtInjection: localStorage.getItem(
              "ai-workflow-course-recovery-v1"
            ),
            attribution:
              "Test harness wrote both values; neither write is attributed to the product."
          };
          throw new Error(
            "Simulated render failure after external primary and barrier writes."
          );
        }
        return originalReplaceChildren.apply(this, nodes);
      };
      document.querySelector("#reset-progress").click();
    })()`);
    await approveActionDialog("External primary-and-barrier rollback");
    const externalKeyMessage = await waitFor(
      async () => {
        const message = await evaluate(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        return /primary data: changed externally and preserved/i.test(message) &&
          /reset barrier: changed externally and preserved/i.test(message) &&
          /overall rollback: not fully verified/i.test(message)
          ? message
          : null;
      },
      "External primary-and-barrier reconciliation result",
    );
    assert.match(externalKeyMessage, /recovery copy: restored/i);
    assert.match(externalKeyMessage, /runtime state: restored/i);
    assert.match(externalKeyMessage, /visible course: restored/i);
    assert.match(externalKeyMessage, /stop using this window/i);
    const externalKeyResult = await evaluate(`({
      primary: localStorage.getItem("ai-workflow-course-state-v1"),
      recovery: localStorage.getItem("ai-workflow-course-recovery-v1"),
      barrier: localStorage.getItem("ai-workflow-course-reset-barrier-v1"),
      injection: window.__externalOwnedKeyInjection
    })`);
    assert.equal(externalKeyResult.primary, externalKeyPlan.primaryExternal);
    assert.equal(externalKeyResult.barrier, externalKeyPlan.barrierExternal);
    assert.equal(externalKeyResult.recovery, externalKeyPlan.recoveryBefore);
    assert.equal(externalKeyResult.injection.injectionCount, 1);
    assert.equal(
      externalKeyResult.injection.primaryAfter,
      externalKeyPlan.primaryExternal,
    );
    assert.equal(
      externalKeyResult.injection.barrierAfter,
      externalKeyPlan.barrierExternal,
    );
    assert.equal(
      externalKeyResult.injection.attribution,
      "Test harness wrote both values; neither write is attributed to the product.",
    );
    await evaluate(`(() => {
      const plan = ${JSON.stringify(externalKeyPlan)};
      localStorage.setItem(
        "ai-workflow-course-state-v1",
        plan.primaryBefore
      );
      if (plan.recoveryBefore === null) {
        localStorage.removeItem("ai-workflow-course-recovery-v1");
      } else {
        localStorage.setItem(
          "ai-workflow-course-recovery-v1",
          plan.recoveryBefore
        );
      }
      if (plan.barrierBefore === null) {
        localStorage.removeItem("ai-workflow-course-reset-barrier-v1");
      } else {
        localStorage.setItem(
          "ai-workflow-course-reset-barrier-v1",
          plan.barrierBefore
        );
      }
      delete window.__externalOwnedKeyInjection;
    })()`);

    await evaluate(`(() => {
      window.__originalStorageRemoveItem = Storage.prototype.removeItem;
      window.__originalStorageSetItem = Storage.prototype.setItem;
      Storage.prototype.removeItem = function (key) {
        if (key === "ai-workflow-course-reset-barrier-v1") {
          throw new DOMException("Simulated barrier rollback failure.", "QuotaExceededError");
        }
        return window.__originalStorageRemoveItem.call(this, key);
      };
      Storage.prototype.setItem = function (key, value) {
        if (key === "ai-workflow-course-state-v1") {
          throw new DOMException("Simulated state-write failure.", "QuotaExceededError");
        }
        return window.__originalStorageSetItem.call(this, key, value);
      };
      document.querySelector("#reset-progress").click();
    })()`);
    await approveActionDialog("Unverified reset");
    const unverifiedResetMessage = await waitFor(
      async () => {
        const message = await evaluate(
          `document.querySelector("#toast")?.textContent || ""`,
        );
        return /overall rollback: not fully verified/i.test(message)
          ? message
          : null;
      },
      "Unverified reset warning",
    );
    assert.doesNotMatch(unverifiedResetMessage, /nothing was reset/i);
    assert.match(unverifiedResetMessage, /reset barrier: unverified/i);
    assert.match(unverifiedResetMessage, /stop using this window/i);
    await evaluate(`(() => {
      Storage.prototype.removeItem = window.__originalStorageRemoveItem;
      Storage.prototype.setItem = window.__originalStorageSetItem;
      delete window.__originalStorageRemoveItem;
      delete window.__originalStorageSetItem;
      localStorage.setItem(
        "ai-workflow-course-state-v1",
        ${JSON.stringify(resetTransactionSnapshot.primary)}
      );
      localStorage.setItem(
        "ai-workflow-course-recovery-v1",
        ${JSON.stringify(resetTransactionSnapshot.recovery)}
      );
      localStorage.removeItem("ai-workflow-course-reset-barrier-v1");
    })()`);

    const storageBeforeBlockedStartup = await evaluate(
      `localStorage.getItem("ai-workflow-course-state-v1")`,
    );
    const blockedStorageScript = await client.call(
      "Page.addScriptToEvaluateOnNewDocument",
      {
        source: `(() => {
          const originalGetItem = Storage.prototype.getItem;
          window.__readStorageWithoutBlock = (key) =>
            originalGetItem.call(localStorage, key);
          Storage.prototype.getItem = function (key) {
            if (
              this === localStorage &&
              key === "ai-workflow-course-state-v1"
            ) {
              throw new DOMException("Storage read blocked.", "SecurityError");
            }
            return originalGetItem.call(this, key);
          };
        })();`,
      },
    );
    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true`),
      "Blocked-storage startup",
    );
    const blockedStartup = await waitFor(async () => {
      const result = await evaluate(`({
        homeLoaded: document.querySelector("#home-view")?.hidden === false,
        toast: document.querySelector("#toast")?.textContent || "",
        raw: window.__readStorageWithoutBlock(
          "ai-workflow-course-state-v1"
        )
      })`);
      return /could not be read/i.test(result.toast) ? result : null;
    }, "Blocked-storage startup warning");
    assert.equal(blockedStartup.homeLoaded, true);
    assert.equal(blockedStartup.raw, storageBeforeBlockedStartup);
    await evaluate(`(() => {
      const range = document.querySelector("#font-size");
      range.value = "105";
      range.dispatchEvent(new Event("input", { bubbles: true }));
    })()`);
    assert.equal(
      await evaluate(
        `window.__readStorageWithoutBlock("ai-workflow-course-state-v1")`,
      ),
      storageBeforeBlockedStartup,
    );
    await client.call("Page.removeScriptToEvaluateOnNewDocument", {
      identifier: blockedStorageScript.identifier,
    });
    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true`),
      "Storage-readable startup",
    );

    const unsupportedEnvelope = JSON.stringify({
      storageFormat: "ai-workflow-course-storage-v1",
      revision: 900,
      writerId: "future-writer-12345",
      state: {
        schemaVersion: 999,
        futureState: "must remain untouched",
      },
    });
    await evaluate(
      `localStorage.setItem("ai-workflow-course-state-v1", ${JSON.stringify(unsupportedEnvelope)})`,
    );
    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true`),
      "Unsupported-schema startup",
    );
    const quarantineState = await waitFor(async () => {
      const result = await evaluate(`(() => {
        const recoveryRaw = localStorage.getItem(
          "ai-workflow-course-recovery-v1"
        );
        const recovery = recoveryRaw ? JSON.parse(recoveryRaw) : null;
        return {
          toast: document.querySelector("#toast")?.textContent || "",
          primary: localStorage.getItem("ai-workflow-course-state-v1"),
          recoveryPrimary: recovery?.raw || null
        };
      })()`);
      return /quarantined|not overwritten/i.test(result.toast) ? result : null;
    }, "Unsupported-schema quarantine warning");
    assert.equal(quarantineState.primary, unsupportedEnvelope);
    assert.equal(quarantineState.recoveryPrimary, unsupportedEnvelope);
    await evaluate(`(() => {
      const range = document.querySelector("#font-size");
      range.value = "110";
      range.dispatchEvent(new Event("input", { bubbles: true }));
    })()`);
    assert.equal(
      await evaluate(`localStorage.getItem("ai-workflow-course-state-v1")`),
      unsupportedEnvelope,
    );
    await evaluate(`(() => {
      const input = document.querySelector("#import-progress");
      const transfer = new DataTransfer();
      transfer.items.add(new File(
        [${JSON.stringify(backupText)}],
        "quarantine-recovery-import.json",
        { type: "application/json" }
      ));
      input.files = transfer.files;
      input.dispatchEvent(new Event("change", { bubbles: true }));
    })()`);
    await approveActionDialog("Quarantine recovery import");
    await waitFor(
      () =>
        evaluate(`JSON.parse(
          localStorage.getItem("ai-workflow-course-state-v1")
        ).state.schemaVersion === 3`),
      "Verified import replacing quarantined state",
    );
    const postQuarantineRevision = await evaluate(
      `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1")).revision`,
    );
    await evaluate(`(() => {
      const range = document.querySelector("#font-size");
      range.value = "115";
      range.dispatchEvent(new Event("input", { bubbles: true }));
    })()`);
    await waitFor(
      () =>
        evaluate(`JSON.parse(
          localStorage.getItem("ai-workflow-course-state-v1")
        ).revision > ${postQuarantineRevision}`),
      "Saving after verified quarantine import",
    );

    await evaluate(`localStorage.setItem(
      "ai-workflow-course-state-v1",
      JSON.stringify({
        schemaVersion: 1,
        completed: ["course-1-foundation-01"],
        notes: { "course-1-foundation-01": "Legacy note retained." },
        lastDocument: "course-1-foundation-01",
        theme: "dark",
        fontSize: 110,
        expandedGroups: ["foundations"]
      })
    )`);
    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true`),
      "Schema-v1 reload",
    );
    await waitFor(
      () =>
        evaluate(`document.querySelector("#toast")?.hidden === false &&
          /migrated/i.test(document.querySelector("#toast")?.textContent || "")`),
      "One-time migration notice",
    );
    const migrationNotice = await evaluate(`(() => {
      const toast = document.querySelector("#toast");
      const storedEnvelope = JSON.parse(
        localStorage.getItem("ai-workflow-course-state-v1")
      );
      const storedState = storedEnvelope.state;
      return {
        hidden: toast.hidden,
        text: toast.textContent,
        storageFormat: storedEnvelope.storageFormat,
        revision: storedEnvelope.revision,
        storedMigration: storedState.migration,
      };
    })()`);
    assert.equal(migrationNotice.hidden, false);
    assert.match(migrationNotice.text, /migrated/i);
    assert.equal(migrationNotice.storageFormat, "ai-workflow-course-storage-v1");
    assert.ok(migrationNotice.revision >= 1);
    assert.equal(migrationNotice.storedMigration, null);
    const migratedState = await evaluate(
      `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1")).state`,
    );
    assert.equal(migratedState.schemaVersion, 3);
    assert.ok(migratedState.completed.includes("course-1-foundation-01"));
    assert.deepEqual(migratedState.practicalPassed, []);
    assert.equal(
      migratedState.notes["course-1-foundation-01"],
      "Legacy note retained.",
    );
    assert.equal(migratedState.migration, null);

    await client.call("Page.reload", { ignoreCache: false });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true`),
      "Post-migration reload",
    );
    const repeatedMigrationNotice = await evaluate(`(() => {
      const toast = document.querySelector("#toast");
      const storedState = JSON.parse(
        localStorage.getItem("ai-workflow-course-state-v1")
      ).state;
      return {
        hidden: toast.hidden,
        text: toast.textContent,
        storedMigration: storedState.migration,
      };
    })()`);
    assert.equal(repeatedMigrationNotice.storedMigration, null);
    assert.ok(
      repeatedMigrationNotice.hidden ||
        !/migrated/i.test(repeatedMigrationNotice.text),
      "Migration notice recurred after the migrated state was saved.",
    );

    await client.call("Network.emulateNetworkConditions", {
      offline: true,
      latency: 0,
      downloadThroughput: 0,
      uploadThroughput: 0,
    });
    await client.call("Page.reload", { ignoreCache: true });
    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true`),
      "Offline cold reload",
    );
    assert.equal(
      await evaluate(
        `fetch("https://example.invalid/offline-check", { cache: "no-store" })
          .then(() => true, () => false)`,
      ),
      false,
    );
    await evaluate(`location.hash = "#doc=course-1-module-09"`);
    await waitFor(
      () =>
        evaluate(
          `document.querySelector("#reader-title")?.textContent.includes("Acceptance")`,
        ),
      "Offline lesson navigation",
    );
    await assertReleaseBoundary("Offline lesson");
    await evaluate(`location.hash = "#search"`);
    await waitFor(
      () => evaluate(`document.querySelector("#search-view")?.hidden === false`),
      "Offline search route",
    );
    const offlineSearchCount = await evaluate(`(() => {
      const input = document.querySelector("#search-input");
      input.value = "approval";
      input.dispatchEvent(new Event("input", { bubbles: true }));
      return document.querySelectorAll(".search-result").length;
    })()`);
    assert.ok(offlineSearchCount > 0);
    await client.call("Network.emulateNetworkConditions", {
      offline: false,
      latency: 0,
      downloadThroughput: -1,
      uploadThroughput: -1,
    });

    process.stdout.write(
      "Browser smoke passed: opener-duplicated tabs use distinct writer identities; two-window progress merges, same-note conflicts, and pending-note reset recovery are explicit; in-app confirmations support focus and Escape; import/reset rollback reports primary, barrier, recovery, runtime, route, render, and overall results separately; deterministic harness-attributed external recovery/primary/barrier writes are preserved by per-key comparison; blocked and unsupported storage is quarantined without overwrite; six responsive viewports, visible navigation, route focus, accessibility modes, Course 1 isolation, backup/migration, and offline reload/search also pass.\n",
    );
  } finally {
    if (secondTargetId && client) {
      try {
        await client.call("Target.closeTarget", { targetId: secondTargetId });
      } catch {
        // Chrome teardown below is the final fallback.
      }
    }
    secondClient?.close();
    client?.close();
    chromeProcess?.kill();
    previewProcess?.kill();
    await rm(temporaryDirectory, { recursive: true, force: true, maxRetries: 4 });
  }
}

await main();
