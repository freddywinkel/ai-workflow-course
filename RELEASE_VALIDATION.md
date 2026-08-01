# Release Validation — Course 1 version 2.6.0 and Progressive Web App (PWA)

## How release status is recorded

This bundled page is the reusable execution protocol. Its empty checkboxes are
instructions for a release reviewer, not the authoritative status of version
2.6.0. Historical release results are stored outside the PWA bundle under
`release_evidence/`. The authoritative **current** product status, reopened
requirements, repair closure evidence, and status precedence are in
[`COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md`](COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md).
The version 2.5.0 acceptance record is preserved as dated evidence and is
currently `SUPERSEDED`. The ledger currently records version 2.6.0 as
`UNVERIFIED`: the known local implementation defects are repaired, but the
personal-study release is not an accepted candidate and required human,
repository-control, installed-client, device, accepted-promotion, and final
live-verification evidence is still missing. `C1-GOV-007` and `C1-GOV-011` are
`EVIDENCE PENDING`; the all-33-test final-adjudication gate is implemented, but
its 33 candidate-bound acceptance records do not yet exist. `C1-GOV-013` and
`C1-GOV-015` are `CLOSED`. Always read the ledger rather than carrying this
dated explanation forward as an independent status decision.

Do not write a derived build ID or content hash into this page: this page is
part of that hash, so doing so would change the value being recorded. The
unbundled acceptance record can safely capture the final identifiers and the
real installed-client result after deployment.

## Release rule

Do not treat publication as acceptance merely because the build succeeds. A
release passes only when course structure, content, learner state, PWA
behavior, responsive layout, and installed-update behavior have been checked.

Version 2.6.0 has a separately authorized **personal synthetic study** lane.
That lane may publish the exact tested artifact only while its product status
remains `UNVERIFIED`, its distribution purpose remains
`personal-synthetic-study`, every known implementation defect is closed, the
automated release gates pass, and the fixed boundary notice remains visible.
It permits reading and synthetic exercises only. It cannot award Course 1
completion, support Course 2 progression, prove consulting ability, or
authorize client, production, real, employer, medical, personal,
confidential, or credential data.

A known failure is `REPAIR REQUIRED`; missing evidence is `UNVERIFIED`. Neither
may be reported as `PASS`. Follow the ledger's candidate → acceptance for
promotion → byte/fingerprint-identical promotion revalidation build → deploy
that tested artifact without another rebuild → live verification → rollback
lifecycle.
Do not mark the release `PASS` until the public identity and a preserved real
installed-client update have passed. Keep the last `PASS` artifact and rollback
evidence available before promotion.

Course 1 and Course 4 require separate statuses, tests, acceptance records, and
release decisions. Course 1 may verify only that Course 4 remains structurally
non-core. A Course 4 implementation failure must not block or support a Course
1 decision unless a genuinely shared PWA contract changed.

Ordinary pull requests and pushes validate but cannot publish. An explicitly
authorized manual `personal-study` dispatch may publish the separate study
artifact; it is not a promotion or acceptance decision. Candidate
preservation, post-build acceptance, manual accepted promotion, live
verification, and emergency rollback are defined in
[`ROLLBACK_RUNBOOK.md`](ROLLBACK_RUNBOOK.md). Repository branch, environment,
Pages, alert, and notification settings remain owner-controlled evidence; the
workflow files cannot prove those settings are enabled.

## 1. Package structure

- [ ] `curriculum.json` parses.
- [ ] One career course is marked current.
- [ ] Nine foundation and nine module progress lessons exist.
- [ ] Course 1 has exactly 18 core foundation/module lessons and exactly 21
      required `learningSequenceIds`: readiness, software check, Windows Setup,
      nine foundations, and nine modules.
- [ ] The optional `course-4-capstone` group is non-core and contains exactly
      the overview plus Labs 0–9.
- [ ] Every capstone page has the Course 4 `courseId` and no Course 4 page
      appears in the Course 1 learning sequence.
- [ ] All stable IDs are unique.
- [ ] All revision dates are valid.
- [ ] `contentRevisionThrough` equals the latest bundled page revision.
- [ ] `sourceVerifiedThrough` equals the evidence-backed
      `source_claims.json` date and remains independent of content edits.
- [ ] The deprecated `verifiedThrough` compatibility alias equals
      `sourceVerifiedThrough` and is not used as a revision ceiling.
- [ ] The PWA displays the source-review and content-revision dates as two
      separately labelled claims.
- [ ] Every configured source exists exactly once.
- [ ] Every module contains the required headings in order.
- [ ] Every foundation and module contains one ordered follow-along,
      recreation, read-only Codex check, and pass-criteria sequence.
- [ ] Every Codex check is limited to one pasted full folder path, explicitly
      forbids changes, and checks for secrets or real data.
- [ ] Required onboarding abbreviations and unfamiliar product names are
      explained before use.
- [ ] Internal links resolve outside ignored future-course archives.
- [ ] JavaScript Object Notation (JSON) schemas pass meta-validation.
- [ ] `stack-manifest.yaml` parses.

Run:

```powershell
& .\.venv\Scripts\python.exe tools\validate_package.py --scope course1
```

Expected: `PASS`.

The separate Course 4 workflow runs `--scope full`, the Course 4 lesson
contract, its fake-provider implementation tests, and the shared-reader tests.
Those results are not Course 1 acceptance evidence.

## 2. Synthetic data

- [ ] `work_items.csv` has 15 rows and 12 expected columns.
- [ ] `expected_issues.csv` has 13 unique issue keys.
- [ ] Rules R001–R011 reproduce all expected issue keys.
- [ ] Assessment date is `2026-07-26`.
- [ ] No real person, employer, customer, or transaction appears.
- [ ] Archived supplier data is excluded from Course 1 validation and PWA.
- [ ] Course 4 pages remain non-core, outside Course 1 completion, and owned by
      the separate Course 4 validation workflow.

Course 4 implementation, cloud, billing, deployment, and teardown evidence is
intentionally not repeated or accepted here. It belongs to the separate
Course 4 release record and workflow. Course 1 checks only that the optional
later material remains synthetic, non-core, and isolated from Course 1
completion.

## 3. Content consistency

- [ ] README, Overview, Architecture, Capstone, Rubric, modules, schemas, and
      practice-data README describe the same project.
- [ ] Course 1 boundary is prominent.
- [ ] No lesson claims production readiness or legal compliance.
- [ ] `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, and `DO NOT CONTINUE` are the
      only Course 1 final decisions and each remains a valid evidence-backed
      result.
- [ ] Course 1 never authorizes a client pilot; discovery belongs in Course 2
      and supervised low-risk pilot delivery belongs in Course 3.
- [ ] Model IDs are configuration, not durable dependencies.
- [ ] Course 1 makes no live AI or provider call; it tests a possible bounded
      future AI contribution with a deterministic offline mock.
- [ ] Future courses are visibly planned. The Course 4 capstone is labelled an
      optional advanced prototype, not a complete course or production proof.
- [ ] Vague practice instructions were not reintroduced.
- [ ] Foundation 1 includes literal File Explorer and Notepad actions, expected
      files, a different recreation, and a read-only inspection prompt.
- [ ] Source register was opened and checked on the release date.
- [ ] `source_claims.json` contains an owner, access date, locator, freshness
      limit, and review trigger for every registered claim.
- [ ] The online source audit passed, with every `manual-browser` locator
      separately inspected by a reviewer.
- [ ] Exact Python pins, licence allow-list, tracked CycloneDX Software Bill of
      Materials (SBOM), PyPI artifact evidence, Open Source Vulnerabilities
      (OSV) results, and the dependency-free Node package lock passed.

Run the machine-readable gates:

```powershell
& .\.venv\Scripts\python.exe tools\audit_course1_supply_chain.py --online
& .\.venv\Scripts\python.exe tools\audit_course1_sources.py --online
```

These automated gates prove the checked-in hash-required Python lock, local
full-commit Action inventory, CycloneDX inventory, and configured toolchain
contract. GitHub repository security settings, actual scheduled-run history,
and exact hosted-runner/browser identities remain repository/run evidence.
The local `C1-GOV-007` implementation checks pass. Keep the finding
`EVIDENCE PENDING`—and keep the product from `PASS`—until repository alert
settings, an actual scheduled-run record, and the required named manual source
review are recorded.

## 4. PWA build and tests

From `app`:

```powershell
$env:BASE_PATH="/ai-workflow-course/"
node --test tests\*.test.mjs
node scripts\build.mjs
node scripts\browser-smoke.mjs
node scripts\browser-update-smoke.mjs
```

From the repository root, in a disposable maintainer environment:

```powershell
python -m pip install --require-hashes -r requirements-course.txt -r tools\requirements-maintainer.txt
$nodeExe = (Get-Command node).Source
python tools\accept_course1_quality.py --node $nodeExe --report C:\path\to\course1-quality.json
```

- [ ] Bundle schema is 2.
- [ ] Curriculum metadata is inside the content hash.
- [ ] Stable lesson IDs and revisions are present.
- [ ] Optional document-level `courseId` metadata survives the build.
- [ ] Course 4 pages remain non-core, Course 1 remains nine foundations plus
      nine modules, and the required reading/practical totals remain 21.
- [ ] Built JavaScript passes syntax checks.
- [ ] Real Chrome opens all 21 required pages at 320 CSS pixels without page
      overflow and passes keyboard, forced-colour, backup/import/reset,
      blocked-storage, schema-v1 migration, and offline checks.
- [ ] A controlled previous-to-current service-worker update preserves
      reading, practical checks, notes, and unrelated caches through
      **Later**, **Update now**, and cold reopen.
- [ ] The update rehearsal serves JavaScript as GitHub Pages does
      (`application/javascript`), while the service worker accepts only that
      production alias or the manifest-declared `text/javascript` value.
- [ ] Course 4 implementation tests are absent from the Course 1 deployment
      dependency chain.
- [ ] A genuine shared-reader change runs the shared PWA tests in both product
      workflows without turning a Course 4 result into Course 1 evidence.
- [ ] Manifest ID, scope, and start URL remain `/ai-workflow-course/`.
- [ ] Service-worker cache prefix remains compatible.
- [ ] No generated placeholder remains.
- [ ] No external font or image is required.
- [ ] Critical Python and importable PWA security modules meet the closed 90%
      line and 90% branch coverage contract.
- [ ] Persistent and generated property tests pass.
- [ ] All nine named security mutants are caught in disposable copies.
- [ ] All 12 cross-system deliberately broken controls are caught in
      disposable copies.
- [ ] The live checkout is hash-unchanged by mutation and negative-control
      runs.
- [ ] Maintainer-only coverage tooling remains absent from the learner
      requirement lock.

`--skip-mutations` is a repair-iteration aid that deliberately makes the
quality result fail. It is never acceptable release evidence. Node coverage
applies only to importable security modules; service-worker coverage comes
from controlled browser behavior and mutation tests.

## 5. Information architecture

Verify:

- [ ] Overview tab explains who the course is for and its boundary.
- [ ] Course navigation follows curriculum metadata.
- [ ] Career tab shows Courses 1–6, the optional specialization, and a distinct
      Course 4 prototype status.
- [ ] **Open the optional capstone** opens the Course 4 overview.
- [ ] Course 4 page marks are visibly separate and never change Course 1's
      21-page reading/practical totals or Resume.
- [ ] Default search includes Course 1 lessons and references but excludes the
      optional Course 4 capstone.
- [ ] Settings and progress backup work.
- [ ] Previous/next follows explicit reading order.
- [ ] Resume opens the next incomplete current lesson.
- [ ] No supplier-specific home copy remains.

## 6. Learner-state migration

Create both a schema-v1 state and a Course 1 version 2.5.0 state before loading
Course 1 version 2.6.0.

- [ ] Theme and font size survive.
- [ ] Notes survive or are retained for export.
- [ ] Equivalent retained foundations preserve completion.
- [ ] Version 2.6.0's practice revision reopens materially rewritten page-read
      and practical checks for review without changing stable lesson IDs.
- [ ] unknown old IDs are not misapplied.
- [ ] old JSON backup import works.
- [ ] reset requires confirmation.
- [ ] a migration notice explains any invalidated completion.

## 7. Accessibility and responsive behavior

Test at:

- 320×568;
- 390×844;
- 430×932;
- 834×1112;
- desktop 1440×900; and
- landscape 844×390.

For each relevant size:

- [ ] no horizontal page overflow;
- [ ] five bottom tabs remain readable and tappable;
- [ ] content is not hidden behind the bottom bar or safe area;
- [ ] sidebar opens, traps focus, closes, and restores focus;
- [ ] skip link works;
- [ ] headings receive logical focus after navigation;
- [ ] 125% reader text remains usable;
- [ ] dark and light themes have sufficient contrast;
- [ ] tables scroll inside their wrapper;
- [ ] reduced motion is respected;
- [ ] landscape does not make the primary controls unreachable.

## 8. Offline behavior

- [ ] First visit succeeds online.
- [ ] Course bundle and Career tab load offline.
- [ ] Optional Course 4 lesson pages can be read offline after the app has
      cached the release.
- [ ] notes and completion save offline.
- [ ] search works offline.
- [ ] app does not claim the capstone itself runs offline.
- [ ] unavailable external source links fail normally without damaging the app.

## 9. Installed-client update

Use an installed or controlled Course 1 version 2.5.0 client:

1. load and record old build/version;
2. save representative progress and notes;
3. publish or serve Course 1 version 2.6.0 at the same scope;
4. foreground or focus the old client;
5. verify the update prompt appears;
6. choose **Later** and confirm the old version remains usable;
7. choose **Update now**;
8. confirm the new service worker activates;
9. verify the version 2.6.0 Overview, 21-page practice loop, Course 4 link, and
   Career tab;
10. verify the persistent `UNVERIFIED` personal-study boundary on Home, a
    lesson, Career, and Settings;
11. verify state migration;
12. cold reload and reopen the installed PWA.

- [ ] new precache resources were fetched with `cache: "reload"`;
- [ ] no broad cache deletion occurred;
- [ ] local state was not erased;
- [ ] the product status is still `UNVERIFIED` and distribution purpose is
      still `personal-synthetic-study` after activation and cold reopen;
- [ ] Course 1 version 2.6.0 is still present after cold reopen.

## 10. Final release record

This section is the accepted-release path. A personal-study publication does
not create this record, close its evidence gaps, or change the product to
`PASS`.

Create a new version-specific acceptance record under `release_evidence/`
from
`release_evidence/templates/course1-promotion-acceptance.template.json`.
Store the post-review record in a separate evidence commit so it does not alter
the already tested candidate. Never overwrite an earlier decision to hide a
later finding. The pre-promotion `evidence` array must contain one closed,
path-and-SHA-256-bound technical evidence record for each of the 32 tests that
can finish before public deployment. `C1-TST-PROV-001` is deliberately excluded
because it requires the public artifact; it remains promotion-dependent and
must be recorded after deployment. Each technical evidence record must
hash-bind non-empty raw files under `release_evidence/` that collectively cover
every procedure and environment declared for that test. Typed
command/environment summaries are not accepted as substitutes. The verifier
rejects a missing, extra, duplicate, unknown, wrong-class, wrong-candidate,
wrong-hash, or incomplete-coverage pre-promotion test record.

The controlled promotion verifies the 32 feasible pre-deployment tests. After
deployment, create
`release_evidence/templates/course1-final-technical-acceptance.template.json`
in a separate evidence commit and run the dedicated **Course 1
post-deployment final technical adjudication** workflow. Its fail-closed
verifier requires the exact preserved promotion artifact, the prior
hash-checked promotion decision, matching public identities, valid deployment
chronology, and all 33 test records including `C1-TST-PROV-001`. Keep final
technical acceptance and `C1-GOV-011` `EVIDENCE PENDING` until that separate
run passes. The gate is implemented; an implemented empty gate is not evidence
that all 33 tests passed for one immutable candidate. Record:

- course version;
- curriculum version;
- candidate commit and accepted tag or immutable artifact;
- build ID;
- content hash;
- asset-manifest SHA-256, complete uploaded artifact-tree SHA-256, and exact
  public-served-tree SHA-256;
- content-revision-through date;
- research/source-verified-through date;
- current ledger status and every finding ID claimed closed;
- source audit result;
- package validator result;
- PWA test result;
- operating systems, devices, install modes, viewports, browser names and
  versions tested;
- offline result;
- installed-update result;
- rollback-readiness or rollback-drill result;
- independent-review reports and any disagreement adjudication;
- known limitations;
- release decision and reviewer.

For a normal `manifest-v1` candidate, `version.json`, the asset manifest,
service worker, acceptance record, workflow input, and technical evidence must
all use the same full lower-case 40-character commit. A short commit is not a
release identity. A development build records `working-copy` and is never
eligible for promotion. The rollback-only `legacy-v2.5` exception is the exact
allowlisted artifact described in `ROLLBACK_RUNBOOK.md`; its record uses
`assetManifestSha256: null`, and its historical 12-character `version.json`
commit is accepted only because the complete commit, artifact tree, and file
set are independently fixed by that exception.

The controlled workflow verifies the record against the exact candidate before
it can upload a Pages artifact. The separate rollback workflow uses
`release_evidence/templates/course1-rollback-authorization.template.json`;
its `lastKnownGoodAcceptanceRecord` is a closed `path` plus `sha256` locator,
not descriptive text. For `manifest-v1`, the verifier hash-checks and parses
that prior promotion decision, requires its exact rollback-target identity and
complete evidence, and rejects a future or non-independent decision. The
legacy v2.5 exception accepts only the pinned historical Markdown record.
Record the rehearsal or live outcome with
`release_evidence/templates/course1-rollback-evidence.template.json`.

The uploaded manifest-v1 tree contains `.nojekyll`, but GitHub Pages treats it
as a publication-control file rather than a public asset. Public byte
verification must therefore compare the manifest-listed assets plus
`asset-manifest.json` and `sw.js` exactly, record that public-served-tree hash,
verify production-compatible media types for every served file, and separately
require `.nojekyll` in the uploaded artifact. A public 404 for `.nojekyll` is
expected and must not be misreported as an artifact mismatch.

The post-deployment workflow must also run
`app/scripts/browser-public-smoke.mjs` in a new Chrome profile. It must observe
the exact service worker in `activated` control, the exact manifest-bound cache,
the visible `UNVERIFIED` study boundary, and a successful offline reopen.

If the controlled pre-promotion update rehearsal cannot be performed, label the
candidate `UNVERIFIED` and do not promote it. If the real public
installed-client check cannot be completed immediately after exact-artifact
promotion, the release remains `UNVERIFIED` rather than `PASS`; follow the
ledger's rollback decision instead of assuming success.
