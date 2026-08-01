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

## Current Course 1 status

The current version 2.6.0 personal-study edition is **`UNVERIFIED`**, not
`PASS`, and its separate distribution purpose is
`personal-synthetic-study`. The known local implementation defects are
repaired, but required human, installed-client, wider device, and final
acceptance evidence is missing. `C1-GOV-007` and
`C1-GOV-011` are `EVIDENCE PENDING`; the all-33-test final-adjudication gate is
implemented, but its 33 candidate-bound acceptance records do not yet exist.
`C1-GOV-013` and `C1-GOV-015` are `CLOSED`. The authoritative current decision
and evidence boundaries are in
[`COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md`](COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md).
Public availability permits only the labelled synthetic study use. It does not
close any finding, award Course 1 completion, or establish Course 2 readiness.

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

Course 1 version 2.6.0 uses stable lesson identifiers (IDs) plus revision
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
reload/search, and a controlled previous-to-current service-worker update. The
update check rebuilds the pinned accepted v2.5 source commit instead of
relabelling current code. It proves that v2.5 **Update now** can activate the
version 2.6 service worker after its asset bytes pass integrity checks while
preserving and migrating learner state. This is technical update evidence, not
a product `PASS`.

## Controlled publication

The GitHub Pages workflow treats ordinary pull requests and pushes as
validation only. They cannot deploy. A maintainer manually chooses one of:

- `validate`, which freezes and retains the tested candidate; or
- `personal-study`, which requires the exact full commit and the explicit
  `UNVERIFIED-SYNTHETIC-STUDY-ONLY` acknowledgement, runs the isolated study
  verifier, and publishes only the already tested artifact; or
- `promote`, which requires the candidate's full commit, an immutable
  post-review acceptance-record commit, and an exact matching acceptance
  record.

Both publication jobs download the tested artifact instead of rebuilding it
and target the main-only `github-pages` environment. Required-reviewer
protection is an owner-controlled repository setting and remains
`EVIDENCE PENDING` until its live setting is recorded. The personal-study
verifier rejects a known defect, a new unclassified pending
finding, missing status/purpose metadata, or weakened learner boundary. The
accepted-release verifier remains separate and still requires all human and
candidate-bound evidence. A separate manual rollback workflow restores only a
named full last-known-good commit after checking its authorization and rebuilt
identity. See [`ROLLBACK_RUNBOOK.md`](ROLLBACK_RUNBOOK.md).

The deployed study job then runs
`tools/verify_course1_public_artifact.py`: it redownloads the learner-facing
root and exact public file set, compares their bytes and production media types
with the tested artifact, recomputes the public-served-tree hash, and records
the expected public 404 for the uploaded `.nojekyll` control. The same job then
runs `app/scripts/browser-public-smoke.mjs` in a new Chrome profile, requires
the exact service worker and cache to activate, and reopens the course offline.
A mismatch fails the release run and invokes the rollback decision; deployment
alone is not completion.

This version 2.6.0 artifact is intentionally not eligible for the accepted
`promote` lane because its purpose is `personal-synthetic-study`. A future
accepted release requires a new reviewed commit that explicitly changes the
closed metadata and validators to `accepted-release-candidate`, reruns every
candidate and human gate, and produces a new exact artifact identity. Never
flip the purpose at deployment time or relabel this study artifact as
accepted.

Local and audit builds use `COURSE1_BUILD_MODE=development` by default and
record `working-copy`; that identity cannot be promoted. The candidate workflow
sets `COURSE1_BUILD_MODE=candidate`. Candidate mode stops before replacing
`app/dist` unless `GITHUB_SHA` and checked-out `HEAD` are the same full
40-character commit and the complete tracked and untracked source tree is
clean.

Course 4 fake-provider and implementation tests run in
`course4-offline.yml`. They are deliberately not dependencies of the Course 1
Pages promotion. Shared curriculum or PWA changes still run the shared-reader
contract in both workflows.

## Content and update identity

The build ID changes when any of these change:

- curriculum metadata;
- bundled Markdown;
- PWA HTML, JavaScript, CSS, or service worker;
- the build script that creates the bundle, manifest, and icons;
- base path.

The content bundle includes its schema version, curriculum version,
current-course ID, content hash, and lesson metadata.

Course dates have deliberately separate meanings:

- `contentRevisionThrough` is the latest `revision` date among bundled pages.
  A governance or wording edit can advance this date.
- `sourceVerifiedThrough` is the oldest current semantic-review date in
  `source_claims.json`. It advances only when the source owners actually
  recheck the claims and record that evidence.
- `verifiedThrough` is retained only as a deprecated compatibility alias for
  `sourceVerifiedThrough` in schema-v2 bundles and `version.json`. It is never
  a ceiling for page revisions.

The source curriculum uses schema version 3. The public PWA bundle remains
schema version 2 so an existing installed client keeps the same reader
contract. The build can migrate legacy schema-v2 curriculum metadata by
deriving the content date from page revisions and treating the old
`verifiedThrough` value only as the source-review date. Current source must
declare both dates explicitly, and the package validator rejects drift between
the source register, date contract, compatibility alias, page revisions, and
rendered consumers.

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

The evergreen audit is a **maintainer delta workflow**. It does not authorize
its own edits or a release. A learner must not run it as an installation step.
Maintainers choose its explicit read-only or approved-repair mode and run it:

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

1. As a course maintainer, read the current ledger and
   `COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md`, then run
   `EVERGREEN_UPDATE_PROMPT.md` in an explicit mode. A full/final audit uses
   the ground-up protocol; a delta repair requires prior approval and
   `STRATEGIC FIT: PASS`.

If step 1 is read-only, stop with the dated delta report and proposed repair
plan. Steps 2–14 apply only to an `APPROVED DELTA REPAIR`; publishing remains a
separate authorized release action.

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
11. Run the dependency, Software Bill of Materials (SBOM), licence,
    vulnerability, and claim-level source gates.
12. Preserve the last `PASS` artifact, acceptance identity, learner-state
    backup, and rollback authorization path.
13. Publish only through the explicitly authorized `personal-study` lane or
    the stricter accepted-release promotion lane. Never convert study
    publication into acceptance by wording.
14. Immediately verify the served manifest assets, asset manifest, service
    worker, browser behavior, offline reopen, and prior installed client. The
    uploaded `.nojekyll` control file is not expected to be served by GitHub
    Pages. Keep product and competence status `UNVERIFIED` until all later
    evidence passes.
