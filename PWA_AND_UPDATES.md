# PWA and Course Updates

## What the PWA is

The PWA is an offline course reader and local progress tracker.

It:

- bundles the complete Course 1 Markdown and the optional Course 4 Controlled
  Document Intake capstone lessons;
- shows a separate Career Path tab;
- keeps later-course lessons out of the default Course 1 menu and search;
- tracks Course 1 pages read separately from practical-task self-checks;
- stores notes, appearance, reading records, and self-checks in local browser
  storage;
- searches Course 1 reading material;
- installs on supported desktop and mobile browsers;
- presents learner-controlled course updates.

It does not:

- run either capstone or deploy cloud resources;
- contain an AI model;
- store an application programming interface (API) key, Google Cloud
  credential, or billing permission;
- connect to GitHub after installation except for static course updates;
- synchronize progress;
- present the optional Course 4 prototype as the complete Course 4 or as
  production readiness.

## Canonical structure

`curriculum.json` is the canonical information architecture:

- stable lesson IDs;
- lesson revisions;
- an optional document-level `courseId` for material that belongs to a later
  career course;
- ordered groups and reading sequence;
- progress eligibility;
- estimated practical effort, separately from automatically calculated reading
  minutes;
- current-course promise and boundary;
- module summaries;
- career-course roadmap.

Markdown remains the lesson-content source of truth.

The build fails when curriculum metadata references a missing, duplicated, or
invalid source.

## Progress model

Course 1 version 2.5.0 uses stable lesson identifiers (IDs) plus revision
dates. This
prevents:

- a renamed file from losing progress unnecessarily;
- a substantially rewritten lesson from remaining falsely completed;
- future course cards from inflating Course 1 progress.

The Course 4 capstone pages are deliberately non-core. They stay out of the
default Course 1 menu and search and are opened intentionally from a disclosure
in Career Path. They can still be marked read page-by-page, but those reading
marks do not count toward Course 1 reading or practical records, do not appear
in Course 1 Resume, and do not alter Course 1's 21 required learning-sequence
pages: the readiness check, software check, Windows Setup, nine foundations,
and nine modules.

For every required learning-sequence page, a page-read mark and a
practical-task self-check are
separate, revision-aware records. Reaching 100% pages read is never labelled as
course completion or competence. The practical record means only that the
learner says the recreated task met every stated criterion; it is not an
independent assessment, rubric decision, or evidence of consultant readiness.

The app migrates the old schema-v1 local state:

- appearance and reading size are preserved;
- notes are retained where possible;
- earlier completion marks become page-read marks only and never create
  practical self-checks;
- reading and practical records are preserved only for equivalent lessons;
- rewritten lessons require reading and practical checks again;
- future planned courses never receive completion controls.

Export a progress backup before a major release. The backup includes page-read
marks, practical self-checks, notes, and appearance preferences.

`course.learningSequenceIds` controls Resume and previous/next. The 21 required
pages are the readiness check, Beginner Software Check, Windows Setup, nine
foundations, and nine modules. The software check and setup appear between
Foundations 2 and 3, where their tools are first needed. Reference pages and
later-course pages do not inflate either required total.

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
node scripts\browser-smoke.mjs
node scripts\browser-update-smoke.mjs
```

Generated files belong in `app/dist`. Do not edit them directly.
The Chrome checks cover all 21 required pages at 320 CSS pixels (the reflow
equivalent of 200% zoom on a 640-pixel-wide view), keyboard and forced-colour
operation, backup/import/reset, blocked storage, old-state migration, offline
reload/search, and a controlled previous-to-current service-worker update.

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

- before revising a later-course live artificial intelligence (AI) provider
  lab;
- before running or revising the optional Google Cloud capstone;
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
8. Run `npm run smoke:browser` and `npm run smoke:update`.
9. Visually inspect the named mobile and desktop layouts.
10. Rehearse the real published old-installed-client update when a prior live
    release is available.
11. Publish only after `RELEASE_VALIDATION.md` passes.
