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

    const evaluate = async (expression) => {
      const result = await client.call("Runtime.evaluate", {
        expression,
        returnByValue: true,
        awaitPromise: true,
      });
      if (result.exceptionDetails) {
        throw new Error(result.exceptionDetails.text || "Browser evaluation failed.");
      }
      return result.result.value;
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

    await waitFor(
      () =>
        evaluate(`document.readyState === "complete" &&
          document.querySelector("#loading-card")?.hidden === true &&
          document.querySelector("#home-view")?.hidden === false`),
      "Course home",
    );
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

    await evaluate(`(() => {
      location.hash = "#home";
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
        evaluate(`location.hash === "#main-content" &&
          document.activeElement === document.querySelector("#main-content")`),
      "Skip-link keyboard target",
    );

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
        viewportLayout.primaryHeight >= 44,
        `${viewport.label} primary control was shorter than 44 pixels`,
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
            button.width >= 44 && button.height >= 44,
            `${viewport.label} tab ${index + 1} was smaller than 44 by 44 pixels`,
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
          JSON.parse(localStorage.getItem("ai-workflow-course-state-v1")).fontSize === 125`),
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
      }))()`);
      assert.ok(
        readerLayout.page <= readerLayout.viewport,
        `${documentId} overflowed the 320 CSS-pixel/200%-reflow viewport`,
      );
      assert.ok(
        readerLayout.reader <= readerLayout.viewport,
        `${documentId} reader overflowed its viewport`,
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
    const reader = await evaluate(`(() => ({
      text: document.querySelector("#reader-content").textContent,
      meta: document.querySelector("#reader-meta").textContent,
      practicalPanelHidden: document.querySelector("#practical-pass-panel").hidden,
    }))()`);
    assert.ok(reader.text.includes("All files (*.*)"));
    assert.ok(!reader.text.includes("All files (.)"));
    assert.match(reader.meta, /Read: about \d+ minutes?/);
    assert.match(reader.meta, /Practice: \d+–\d+ hours/);
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
          `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1"))
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
          `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1"))
            .practicalPassed.includes("course-1-foundation-01")`,
        ),
      "Practical self-check state",
    );
    const stored = await evaluate(
      `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1"))`,
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
    await waitFor(
      () =>
        evaluate(
          `document.activeElement === document.querySelector("#settings-view h1")`,
        ),
      "Route heading focus",
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

    await evaluate(`window.confirm = () => true;
      document.querySelector("#reset-progress").click();`);
    await waitFor(
      () =>
        evaluate(`(() => {
          const stored = localStorage.getItem("ai-workflow-course-state-v1");
          return location.hash === "#home" &&
            (!stored || JSON.parse(stored).completed.length === 0);
        })()`),
      "Confirmed reset and Home route",
    );

    const backupText = JSON.stringify(backupPayload);
    await evaluate(`(() => {
      window.confirm = () => true;
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
    await waitFor(
      () =>
        evaluate(`JSON.parse(localStorage.getItem("ai-workflow-course-state-v1"))
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
    const failedSaveMessage = await evaluate(`(async () => {
      const originalSetItem = Storage.prototype.setItem;
      Storage.prototype.setItem = function () {
        throw new DOMException("Storage is blocked.", "QuotaExceededError");
      };
      try {
        window.confirm = () => true;
        const input = document.querySelector("#import-progress");
        const transfer = new DataTransfer();
        transfer.items.add(new File(
          [${JSON.stringify(JSON.stringify(changedBackupPayload))}],
          "blocked-save.json",
          { type: "application/json" }
        ));
        input.files = transfer.files;
        input.dispatchEvent(new Event("change", { bubbles: true }));
        await new Promise((resolve) => setTimeout(resolve, 250));
        return document.querySelector("#toast").textContent;
      } finally {
        Storage.prototype.setItem = originalSetItem;
      }
    })()`);
    assert.match(failedSaveMessage, /backup was not imported/i);
    assert.equal(
      await evaluate(`localStorage.getItem("ai-workflow-course-state-v1")`),
      stateBeforeFailedSave,
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
      const storedState = JSON.parse(
        localStorage.getItem("ai-workflow-course-state-v1")
      );
      return {
        hidden: toast.hidden,
        text: toast.textContent,
        storedMigration: storedState.migration,
      };
    })()`);
    assert.equal(migrationNotice.hidden, false);
    assert.match(migrationNotice.text, /migrated/i);
    assert.equal(migrationNotice.storedMigration, null);
    const migratedState = await evaluate(
      `JSON.parse(localStorage.getItem("ai-workflow-course-state-v1"))`,
    );
    assert.equal(migratedState.schemaVersion, 2);
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
      );
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
      "Browser smoke passed: six responsive viewports, visible 44px five-tab navigation where applicable, unobscured primary controls, all 21 pages at 320px/125% text, table containment, skip-link and route focus, two-way sidebar focus wrapping and restoration, reduced motion, light/dark contrast, forced colours, Course 1 isolation, exact wildcard rendering, separate reading/practice state, backup/import/reset, blocked-storage honesty, one-time schema-v1 migration, and offline reload/search.\n",
    );
  } finally {
    client?.close();
    chromeProcess?.kill();
    previewProcess?.kill();
    await rm(temporaryDirectory, { recursive: true, force: true, maxRetries: 4 });
  }
}

await main();
