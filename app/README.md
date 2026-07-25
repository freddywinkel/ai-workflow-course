# Course PWA

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

- bundles the foundations, twelve weeks, glossary, references, worksheets, and
  update records;
- derives a deterministic content hash;
- generates the manifest, version record, PNG icons, and versioned service
  worker;
- applies the repository subpath to every install and cache URL.

The PWA stores completion, notes, theme, and reading size only in browser
`localStorage`. It contains no AI or GitHub credential.

## Update contract

Course changes are made in the Markdown source and verified before commit. A
push to `main` runs package validation, PWA tests, the production build, and the
GitHub Pages deployment. The content hash changes the service-worker cache
version. Existing installations show a visible update prompt and activate the
new worker only after the learner chooses **Update now**.

The worker fetches every new precache resource with `cache: "reload"` so an old
HTTP cache cannot silently repopulate the new version.
