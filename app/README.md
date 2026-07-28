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
```

The production artifact is `app/dist`. Do not edit generated files there.

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
overview. Document-level `courseId` metadata keeps those lessons attached to
Course 4 while Course 1 remains the current course. Course completion uses
stable lesson IDs and revisions, so a materially revised lesson can reopen for
review without losing its private note. State is migrated from the earlier
course bundle when possible.

The PWA stores completion, notes, theme, and reading size only in browser
`localStorage`. It contains no AI or capstone runtime, Google Cloud or GitHub
credential, billing authority, or real-data upload facility. It only displays
the capstone instructions; the runnable demonstration remains a separate
learner project.

## Update contract

Course changes are made in the Markdown source and verified before commit. A
push to `main` runs package validation, PWA tests, the production build, and the
GitHub Pages deployment. The content hash changes the service-worker cache
version. Existing installations show a visible update prompt and activate the
new worker only after the learner chooses **Update now**.

The worker fetches every new precache resource with `cache: "reload"` so an old
HTTP cache cannot silently repopulate the new version.
