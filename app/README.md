# Controlled Artificial Intelligence (AI) Workflow Foundations Progressive Web App (PWA)

This dependency-free static reader is generated from the course Markdown one
directory above it. The Markdown remains the source of truth.

## Build and test

Run from this `app` folder with Node 22 or newer:

```powershell
npm ci
npm test
$env:BASE_PATH="/ai-workflow-course/"
npm run build
npm run smoke:browser
npm run smoke:update
```

The production artifact is `app/dist`. Do not edit generated files there.
The two local browser checks use installed Chrome. The first opens every
required page at the 320 CSS-pixel equivalent of 200% reflow and exercises
keyboard navigation, forced colours, backup/import/reset, blocked-storage
reporting, old-state migration, and offline reload/search. The second serves a
controlled previous and current build at one scope, then verifies **Later**,
**Update now**, state retention, targeted cache cleanup, and cold reopen. Set
`CHROME_PATH` if Chrome is installed in a non-standard location.

The build:

- reads the complete structure from `../curriculum.json`;
- bundles nine foundations, nine implementation modules, the career sequence,
  references, worksheets, update records, and the optional non-core Course 4
  Controlled Document Intake capstone lessons;
- derives a deterministic content hash;
- generates the manifest, version record, PNG icons, and versioned service
  worker;
- applies the repository subpath to every install and cache URL.

The PWA has a separate Course 1 learning view and Career Path view. The Career
Path marks the advanced Course 4 capstone prototype separately and links to its
overview through an intentional disclosure. Document-level `courseId` metadata
keeps those lessons attached to Course 4 while Course 1 remains the current
course. Later-course pages are excluded from the default Course 1 menu and
search.

The interface shows reading time separately from practical effort. Per-document
`estimatedPracticeHours` metadata is preferred; module Markdown estimates and a
conservative foundation fallback keep older bundles readable. Page-read marks
and practical-task self-checks are separate revision-aware records. Even 100%
reading is never labelled as course competence, and a practical self-check is
explicitly described as the learner's record rather than an independent
assessment. Stable lesson IDs and revisions let a materially revised lesson
reopen both records without losing its learner note. A learner note is local
to the browser profile but is not private from other applications served from
the same website origin. State is migrated from the earlier course bundle when
possible.

The PWA stores page-read marks, practical self-checks, notes, theme, and reading
size only in browser `localStorage`. Export and import include all of that
local state. It contains no AI or capstone runtime, Google Cloud or GitHub
credential, billing authority, or real-data upload facility. It only displays
the capstone instructions; the runnable demonstration remains a separate
learner project.

## Update contract

Course changes are made in the Markdown source and verified before commit. A
push to `main` runs package validation, both offline workflow suites, PWA unit
tests, the production build, both real-Chrome checks, and then the GitHub Pages
deployment. The content hash changes the service-worker cache version. Existing
installations show a visible update prompt and activate the new worker only
after the learner chooses **Update now**.

The worker fetches every new precache resource with `cache: "reload"` so an old
HTTP cache cannot silently repopulate the new version.
