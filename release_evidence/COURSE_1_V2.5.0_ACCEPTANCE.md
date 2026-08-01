# Course 1 version 2.5.0 acceptance record

> **Historical record — `SUPERSEDED` for current status on 2026-07-28.**
> This file preserves the release decision made from the evidence available at
> that time. Later technical, curriculum, and audit-governance reviews reopened
> High and Medium requirements. The authoritative current status is always the
> value in
> [`COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md`](../COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md).
> Do not use the historical `PASS` below as a current clean-audit result or as
> proof of Course 2 readiness.

- Verified: 2026-07-28
- Reviewer: Codex, with independent curriculum and Progressive Web App (PWA)
  audits
- Decision: PASS — released and verified at the Course 1 product scope
- Qualification: this computer still needs the learner's manual Python setup
  before Python-dependent lessons

## Scope

This acceptance covers Course 1, **Controlled Artificial Intelligence (AI)
Workflow Foundations**, its local synthetic capstone runner, and the shared
course-reader PWA.

Course 4 content, its Google Cloud implementation, later career courses, and
the advanced capstone were not audited or accepted here. The package validator
checked only that Course 4 remains non-core and structurally isolated from the
Course 1 sequence. An existing separate continuous-integration job for Course
4 is not evidence for this Course 1 decision.

## Release identity

- Course version: `2.5.0`
- Curriculum schema version: `2`
- Practice revision: `4`
- Accepted bundled-source commit:
  `69d868a713d42b19b12ec11c64898b29e829be71`
- Public build ID: `ad5f59e8f800`
- Public content hash:
  `ddc88ff3b2a9ac9080b05abebad5f578de122406a6bab00bb52b28a92353258a`
- Verified-through date: `2026-07-28`
- Public URL:
  `https://freddywinkel.github.io/ai-workflow-course/`

The final local build made from the accepted bundled source and the public
GitHub Pages assets have the same version, build ID, and content hash. The
later commit that adds this acceptance record changes the publishing commit
shown in `version.json`, but it does not change the bundled course, build ID,
or content hash.

## Beginner and curriculum acceptance

- Independent Modules 1–9 audit: PASS, with no remaining blocker or
  medium-severity finding.
- All 18 core progress lessons use the same beginner loop: exact guided
  example, different recreation, bounded read-only Codex check, and objective
  pass criteria.
- All nine module review prompts are path-scoped, read-only, synthetic-only,
  and explain that a learner attestation is not proof and non-detection is not
  proof of absence.
- First-use technical abbreviations and product names are expanded or
  explained.
- Resume paths preserve familiar evidence, reject unfamiliar files, and give
  numbered preservation/recovery instructions instead of overwriting work.
- Windows PowerShell 5.1 parsing:
  - Modules 1–9: PASS, 154/154 fenced blocks.
  - Broader Course 1 learner material: PASS, 232/232 fenced blocks across 25
    setup, foundation, module, schema, and runner-guidance files.
- Learner examples: PASS, 3/3 Python blocks compile and 11/11
  comma-separated-values (CSV) blocks have consistent rows.
- Package validator: PASS, 37/37 checks, zero failures, zero warnings.
- JSON checks: 15 current files parsed; all 11 schemas passed Draft 2020-12
  meta-validation.

## Runner and clean-room acceptance

- Exact runner test suite:
  - Python 3.12.13: PASS, 61/61.
  - Python 3.13.14: PASS, 61/61.
  - Python 3.14.6: PASS, 61/61.
- Clean-room acceptance repeated on all three Python versions: PASS.
- Each clean-room run used a disposable workspace and seven separate command
  processes, found 13 frozen synthetic issues, reached `approved_draft`,
  created one 13-record JSON export and one 13-row CSV export, performed zero
  external actions, preserved 30 protected source files, and removed the
  temporary workspace.
- A separate fresh Module 5 to Module 6 run preserved its exact `RUN-...`
  identity through copy, approval, and export.
- The review manifest binds eight protected artifacts, including the protected
  expected-issues evidence.
- The Module 8 answer key is hash-checked against the controlled course copy on
  creation, resume, and final precheck.
- Same-run locking, stale-lock recovery, atomic initial preparation,
  transaction rollback, audit reconciliation, exact decision binding, formula
  neutralisation in CSV, and idempotent retry scenarios are covered by tests.
- Runner source passes Ruff's core error checks and formatting check.
- Synthetic course files only; no client, employer, medical, personal, or
  credential data was used.

## Progressive Web App acceptance

- Application tests: PASS, 34/34.
- Production Pages build: PASS.
- Browser smoke: PASS.
- Six responsive viewports passed:
  - 320 by 568
  - 390 by 844
  - 430 by 932
  - 834 by 1112
  - 1440 by 900
  - 844 by 390 landscape
- All 21 Course 1 learner pages passed at 320 pixels and 125% reader text.
- Skip-link and route focus, browser Back/Forward focus, sidebar focus
  wrapping and restoration, reduced motion, forced colours, light/dark
  contrast, table containment, visible controls, backup/import/reset,
  blocked-storage honesty, and schema-v1 migration passed.
- Offline reload and Course 1 search passed against the accepted built
  service worker and precache.
- Controlled old-to-new update smoke passed: **Later** kept the old release;
  **Update now** activated the candidate; reading state, practical state,
  notes, and an unrelated cache survived; only the obsolete course cache was
  removed.
- Public assets were re-read after the bundled-source deployment.
  `version.json`, the manifest, service worker, index, and 83-document course
  bundle agree on version `2.5.0`, build `ad5f59e8f800`, the public base path,
  nine foundations, and nine modules. The final publishing commit is the
  commit containing this record; `version.json` is the authoritative locator.
- Live rendered desktop review passed with no browser log errors.

## Real preserved-client update

PASS from the public v2.4.0 release to public v2.5.0.

- Starting release: version `2.4.0`, build `9c8e758aefbb`.
- Starting learner state: 1 of 21 pages read, 0 of 21 practical self-checks,
  and the private note
  `Synthetic v2.4 update-proof note — keep this after the v2.5 release.`
- **Later** dismissed the release prompt while leaving v2.4.0, the route,
  progress, and note usable.
- A later manual check offered the update again.
- **Update now** activated version `2.5.0`, build `ad5f59e8f800`, without a
  native browser confirmation dialogue.
- The private note and practical state survived.
- The reading completion reopened intentionally because the page and Course 1
  practice contract were revised. The PWA labels this clearly as
  **Mark page read again**; this is controlled re-review, not lost data.

## Source audit

PASS for the Course 1 release boundary on 2026-07-28.

- All 22 external links presented in learner lessons returned successfully.
- 26 of 27 source-register links passed the automated request check.
- The remaining official Organisation for Economic Co-operation and
  Development (OECD) page rejected the automated client but opened
  successfully in a normal browser:
  `https://www.oecd.org/en/publications/ai-adoption-by-small-and-medium-sized-enterprises_426399c1-en.html`.
- Redirected references were updated to current canonical pages for the
  European Commission, n8n, OpenAI, and the Dutch National Cyber Security
  Centre.
- Time-sensitive vendor, legal, security, interface, model, and price details
  remain dated references that must be checked again before real client work.
- Source availability is not proof of market demand, legal compliance, or
  production suitability.

## Current-computer gate

Read-only verification on this Windows computer:

- Windows PowerShell: `5.1.26100.8894`
- Git: `2.54.0.windows.1`
- Visual Studio Code: `1.130.0`
- Windows Package Manager (`winget`): `1.29.280`
- `python`: only the non-working Microsoft Store alias
- Python launcher (`py`): absent

The course detects this exact condition before Python-dependent practice and
provides an official, checkpointed installation route without weakening the
PowerShell execution policy. The learner can start the first two foundations
now, but must complete Windows Setup before Foundation 3 and later executable
work. No system-wide Python installation was performed during this audit.

## Release gate and boundaries

- GitHub Actions run:
  `https://github.com/freddywinkel/ai-workflow-course/actions/runs/30392023092`
- Course 1 clean-room matrix: PASS on Python 3.12, 3.13, and 3.14.
- PWA validation, build, Chrome smoke, and Pages deployment: PASS.
- No paid billing, cloud deployment, live AI provider, or external business
  action was used for Course 1.
- Course 1 does not claim consultant certification, customer demand,
  production readiness, legal compliance, or permission to use real data.
- Final decision: PASS at the Course 1 product scope, with the documented
  manual Python setup remaining for this learner computer.
