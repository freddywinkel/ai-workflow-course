# PWA and Course Updates

## What the PWA is

The PWA is an offline course reader and local progress tracker.

It:

- bundles the current Course 1 Markdown;
- shows a separate Career Path tab;
- tracks completion only for current foundations and modules;
- stores notes, appearance, and progress in local browser storage;
- searches the bundled reading material;
- installs on supported desktop and mobile browsers;
- presents learner-controlled course updates.

It does not:

- run the capstone;
- contain an AI model;
- store an API key;
- connect to GitHub after installation except for static course updates;
- synchronize progress;
- include unfinished future-course lessons.

## Canonical structure

`curriculum.json` is the canonical information architecture:

- stable lesson IDs;
- lesson revisions;
- ordered groups and reading sequence;
- progress eligibility;
- current-course promise and boundary;
- module summaries;
- career-course roadmap.

Markdown remains the lesson-content source of truth.

The build fails when curriculum metadata references a missing, duplicated, or
invalid source.

## Progress model

Course 2.2 uses stable lesson identifiers (IDs) plus revision dates. This
prevents:

- a renamed file from losing progress unnecessarily;
- a substantially rewritten lesson from remaining falsely completed;
- future course cards from inflating Course 1 progress.

The app migrates the old schema-v1 local state:

- appearance and reading size are preserved;
- notes are retained where possible;
- completion is preserved only for lessons declared equivalent;
- rewritten lessons require completion again;
- future planned courses never receive completion controls.

Export a progress backup before a major release.

`course.learningSequenceIds` controls Resume and previous/next. It deliberately
places the read-only Beginner Software Check and Windows Setup between
Foundations 2 and 3. Those onboarding gates can be marked complete but do not
inflate the 18-lesson foundation/module progress percentage.

## Build

From `app` with Node.js 24 or another audited compatible release:

```powershell
node scripts/build.mjs
node --test tests\*.test.mjs
```

For the GitHub Pages subpath:

```powershell
$env:BASE_PATH="/ai-workflow-course/"
node scripts/build.mjs
```

Generated files belong in `app/dist`. Do not edit them directly.

## Content and update identity

The build ID changes when any of these change:

- curriculum metadata;
- bundled Markdown;
- PWA HTML, JavaScript, CSS, or service worker;
- the build script that creates the bundle, manifest, and icons;
- base path.

The content bundle includes its schema version, curriculum version,
current-course ID, content hash, and lesson metadata.

## Installed-update contract

Keep unchanged unless intentionally replacing the installed app:

- manifest ID;
- start URL;
- scope;
- GitHub Pages base path;
- service-worker cache prefix;
- local-storage key migration.

The service worker:

- fetches new precache resources with `cache: "reload"`;
- waits rather than activating silently;
- displays an update choice;
- activates after the learner selects **Update now**;
- deletes only obsolete caches with the course prefix;
- leaves local progress and notes untouched.

## Update schedule

The evergreen audit is a **maintainer workflow**. A learner must not run it as
an installation step because it can authorize edits and a new course release.
Maintainers run it:

- before revising the optional live artificial intelligence (AI) lab;
- before publishing guidance intended for a real client pilot in a later
  course;
- after a material AI Act, AVG, or AP guidance change;
- after a model, API, or data-policy change;
- after a major n8n, Microsoft, or Google workflow change;
- at least every 12 weeks while the course is active.

Durable concepts should rarely require revision. Put current tool and legal
details in updateable references instead of scattering them through lessons.

## Course update checklist

1. As a course maintainer, run `EVERGREEN_UPDATE_PROMPT.md`.
2. Update affected sources and `SOURCE_REGISTER.md`.
3. Update lesson revision dates in `curriculum.json`.
4. Add a changelog entry.
5. Run package validation.
6. Run PWA tests and production build.
7. Test Overview, Course, Career, Search, and Settings.
8. Test mobile and desktop layouts.
9. Test offline reading.
10. Rehearse an old-installed-client update.
11. Confirm migrated progress behavior.
12. Publish only after `RELEASE_VALIDATION.md` passes.
