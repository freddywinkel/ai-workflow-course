# Course PWA and Automatic Updates

The course reader is a static progressive web app (PWA) published from this
repository. It contains no AI key, database password, learner account, or real
document data.

## What the app does

- presents the beginner foundations, glossary, twelve weeks, and course update
  history in a phone- and tablet-friendly reader;
- saves reading progress, completed sections, notes, text size, and theme on the
  current device;
- keeps the core reading material available after it has been opened online;
- checks for a newly published version at startup, when the app returns to the
  foreground, and when **Check for updates** is selected;
- asks before activating a waiting version, then reloads once under the new
  service worker.

Progress is deliberately local to each browser or installed app. It is not
synced between an iPhone and iPad and is removed if Safari website data for the
site is deleted. The course source remains in GitHub.

## Install on iPhone or iPad

1. Open `https://freddywinkel.github.io/ai-workflow-course/` in Safari.
2. Select Safari's **Share** button.
3. Select **Add to Home Screen**. If it is not visible, scroll the share sheet
   and choose **Edit Actions**.
4. Turn on **Open as Web App** when Safari presents that option.
5. Keep the suggested name or shorten it, then select **Add**.
6. Launch the new home-screen icon once while online so the reading material can
   be cached.

Safari, not an in-app browser, is required for the normal iOS/iPadOS
home-screen installation path.

## How a course change reaches the app

```text
official-source audit
  → dated change report
  → minimum justified course edits
  → deterministic course and app tests
  → Git commit and push
  → GitHub Pages validation/build/deploy
  → installed PWA detects a waiting version
  → learner accepts update
```

The app is generated from the course Markdown. A course edit does not require
hand-copying the same text into app source code.

## Scheduled audit

A Codex heartbeat attached to the course task runs every eight weeks. It uses
[`EVERGREEN_UPDATE_PROMPT.md`](EVERGREEN_UPDATE_PROMPT.md), checks primary
official sources, and stops with `UNVERIFIED` when browsing or a required
source is unavailable.

The computer must be on, the Codex desktop app must be running, and this local
repository must remain available when the heartbeat is due. The PWA itself does
not run research in the background.

The automation may publish only when all of these are true:

1. a dated audit report identifies the exact old and replacement statements;
2. enacted law, future applicable requirements, proposals, consultations,
   non-binding guidance, and vendor recommendations are labelled separately;
3. human approval, provenance, synthetic-data restrictions, manual fallback,
   and the vendor-neutral gold set remain intact;
4. the deterministic package validator and PWA tests pass;
5. the app builds for the repository subpath;
6. no secret, real client document, personal data, generated dependency folder,
   or unrelated workspace file is staged;
7. the GitHub Pages deployment succeeds and the live course/version can be
   verified.

When there is no applicable change, the automation records `NO CHANGE` without
creating a cosmetic course revision. When verification or testing fails, it
does not push or deploy and reports the blocker in the Codex task.

## Manual checkpoints

The scheduled audit does not replace the course checkpoints. Run the evergreen
audit manually:

- immediately before starting Week 1;
- immediately before starting Week 7;
- after a material deprecation, security advisory, or legal change;
- whenever the app's displayed verification date is older than the permitted
  course review interval.

Use the app's **Check for updates** action after an audit has been published.

## Recovery

If the app says it is offline, keep using the cached reading material and do
not assume a new audit was completed. Reconnect, open the app, and select
**Check for updates**.

If a new version cannot activate, close every open tab and installed copy of
the course, reopen the home-screen app, and check again. Clearing Safari website
data is a last resort because it also removes local progress.
