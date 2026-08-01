# Course Changelog

## 2.6.0 personal-study publication — 2026-08-02

- Added a separately authorized publication lane for **personal synthetic
  study** with distribution purpose `personal-synthetic-study`. The product
  status remains **`UNVERIFIED`**; public availability is not Course 1
  acceptance or evidence that the learner passed.
- Added the same persistent boundary to the course metadata, built Progressive
  Web App (PWA), update experience, Settings, release workflow, and study
  verifier. The release cannot claim Course 2, consulting, client, or
  production readiness and never authorizes real, employer, client, medical,
  personal, confidential, or credential data.
- Kept the accepted-release promotion and final 33-test adjudication separate.
  Missing learner, assessor, device, installed-client, repository, and live
  acceptance evidence therefore remains visible rather than being waived.
- Corrected public-byte verification to compare the exact files GitHub Pages
  serves. `.nojekyll` remains inside the uploaded artifact as a deployment
  control file and is recorded separately because GitHub Pages does not expose
  it as a public file.
- Corrected the installed-client update boundary after the first public v2.6
  study deployment exposed GitHub Pages' `application/javascript` media type.
  The service worker now accepts that one production alias for manifest-declared
  `text/javascript`, the old-client rehearsal simulates it, and live verification
  rejects every incompatible public media type. The fresh-profile browser gate
  also closes Chrome gracefully, retries temporary-profile cleanup, and preserves
  a diagnostic report if cleanup itself fails.
- Advanced bundled content revision to `2026-08-02` without changing the
  independent `2026-07-28` source-verification claim or Course 1 practice
  revision.

## 2.6.0 — 2026-07-28

### Full Course 1 repair candidate

> **Current-status note — 2026-07-29:** This section records the initial 2.6.0
> repair work, not a current acceptance decision. A later audit-of-the-audit
> opened or partially reopened `C1-GOV-011`, `C1-GOV-012`, and `C1-GOV-013`;
> the subsequent local repairs closed `C1-GOV-012`, `C1-GOV-013`, and
> `C1-GOV-015`. `C1-GOV-007` and `C1-GOV-011` are `EVIDENCE PENDING`; the
> all-33-test gate for `C1-GOV-011` is implemented, but its immutable
> candidate-bound records do not yet exist. The authoritative ledger currently
> records `UNVERIFIED`; follow
> `COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md`.

### Beginner glossary reference — 2026-07-30

- Expanded the existing optional Beginner Glossary with the supplied common
  artificial-intelligence and programming abbreviations plus short forms that
  actually occur in Course 1.
- Kept the glossary outside the 21-page required learning sequence, explained
  ambiguous terms such as `AP` and `NN`, and distinguished abbreviations from
  product names, command names, variable names, and ordinary shortenings.
- Advanced bundled content revision to `2026-07-30` without changing the
  separate `2026-07-28` research/source-verification claim. This content
  change requires a new exact candidate and does not establish release
  acceptance.

- Reconciled the Course 1 promise with the work the learner actually authors:
  the supplied runner is assembled and challenged, one bounded deterministic
  rule is authored and tested, and one different artificial-intelligence (AI)
  contract is designed offline.
- Added independent opportunity calibration, observable Level 1–4 evidence
  anchors, a live oral-assessment protocol, an unseen second-domain transfer
  task, delayed-retention evidence, and an early two-assessor disclosure.
- Split long beginner modules into study blocks of no more than 60 minutes and
  labelled what the learner must understand versus protected plumbing they may
  run and observe.
- Replaced the weak rule-example matrix check with 44 rule-specific cases,
  meaningful learner explanations, and preserved deliberate-failure and
  corrected-retest evidence.

### Runner and evidence integrity

- Enforced strictly ordered audit timestamps and rejected decisions that
  predate or equal the evidence they claim to review.
- Added event-specific audit schemas, streaming input limits, bounded
  identity-checked file reads, owned export staging, no-overwrite publication,
  and beginner-safe command-line failure evidence.
- Preserved the exact 67-test manifest and clean-room negative control across
  Python 3.12, 3.13, and 3.14.

### Progressive web app state and update safety

- Replaced native browser confirmations with an accessible in-app dialog that
  supports focus, cancellation, and Escape without triggering browser dialogue
  suppression.
- Added per-window writer identities, deterministic multi-window merge and
  conflict handling, revisioned reset barriers, pending-note recovery,
  unsupported-state quarantine, hostile-backup validation, and verified
  import/reset rollback through storage and visible rendering.
- Preserved concurrent recovery evidence in the tested simultaneous-reset
  case. The broader exact-rollback versus external-write contract remains open
  under `C1-GOV-013`.
- Bound each service-worker cache to commit and manifest provenance, verified
  every cached response before use, rejected asset or manifest tampering with a
  safe error, and preserved the last valid offline release when a candidate
  update fails.

### Release and maintenance controls

- Separated Course 1 validation from Course 4 implementation acceptance,
  removed direct-push publishing, and added controlled candidate, promotion,
  rollback, dependency, licence, vulnerability, Software Bill of Materials
  (SBOM), and claim-source checks.
- Separated bundled-page revision metadata from research/source verification:
  content is revised through `2026-07-30`, while source evidence remains
  verified through `2026-07-28`. The old `verifiedThrough` field remains only
  as a PWA compatibility alias for the source date, never as a content-revision
  ceiling.
- Added initial fail-closed promotion controls for exact six-column
  audit-ledger rows: the tested unknown-severity/status, shifted, duplicate,
  open, reopened, and partially implemented cases are rejected, and pending
  evidence is allowed only for the three named live-promotion gates.
  At the time of this initial candidate, additional malformed-ID,
  rollback-status, closed-JSON, and evidence-locator bypasses remained
  `PARTIAL` under `C1-GOV-012`; the later audit-control repair closed them.
  That repair also rejects quoted finding rows, replaces self-authored
  command/environment summaries with hash-bound raw artifact coverage for
  every declared procedure and environment, and binds normal rollback to the
  complete prior accepted promotion record for the exact target. The legacy
  v2.5 exception is pinned to its exact historical acceptance path and hash.
- This entry records a repair candidate, not a product acceptance decision.
  Literal-beginner completion, human assessment, installed-device/browser,
  repository-control, and public promotion evidence remain separate gates.

## 2.5.0 — 2026-07-28 — historical, superseded

### Historical literal-beginner completion decision

This dated entry is retained as history. Later audits superseded its release
decision; follow the current audit ledger rather than treating the wording
below as a current product pass.

- Reworked readiness and Foundations 1–9 so a learner can close every window,
  return later, and make an explicit resume-or-retry decision without
  overwriting prior evidence.
- Added create-once guards and numbered retry folders to every file-creating
  foundation exercise, including safe Git recovery when a repository is
  incomplete, dirty, or already has different history.
- Clarified that Course 1 performs no live model call or model-written work.
  The only permitted model interaction in the AI foundation is the final,
  bounded, read-only Codex evidence check.
- Made every foundation check require the learner's synthetic-only attestation
  and explain that an automated non-detection result is not proof that a folder
  contains no sensitive information.

### Controlled workflow integrity

- Bound each run to a canonical configuration covering the source, expected
  oracle, fixed date, rules, pipeline, prompt, adapter mode, and
  mock/fallback versions.
- Added a protected review manifest over the source, issue JSON and
  spreadsheet-safe issue CSV, summary, control, run configuration, and review
  package. Approval and export recompute those hashes from the actual files.
- Bound every approval field to a recomputed decision identifier, while
  explicitly documenting that this is local tamper detection rather than
  authentication or a digital signature.
- Added strict runtime validation for every saved contract, formula-safe CSV,
  atomic paired CSV/JSON publication with rollback, short immutable
  safe-stop evidence, and long-Windows-path coverage.
- Added exclusive fail-closed workspace/run locks, pre-mutation audit checks,
  transactional decision/revision recovery, exact evaluation/export
  reconciliation, and strict wrong-type/filesystem safe stops.
- Unified duplicate preparation, decisions, revisions, validation, export,
  inspection, and failure recording under one same-workspace lock; made first
  run publication retry-safe; protected the expected oracle as run evidence;
  and reconciled required audit events with every material workflow state.
- Replaced self-declared safe free text with controlled headline, group, and
  review-instruction templates rendered from verified evidence.
- Expanded the executable Course 1 runner suite from 41 to 61 adversarial and
  normal-path tests across Python 3.12, 3.13, and 3.14.

### Practice and PWA corrections

- Corrected Module 8's timing inputs, resume variables, interrupted-timer
  handling, and create-once evidence behavior.
- Corrected Module 9's failure exercises to verify
  `failures/latest.json`, follow its immutable numbered history record, and
  preserve a portable evidence copy.
- Updated Module 6 so the learner inspects and records both the draft and
  protected review-manifest hashes before deciding.
- Added exact project-marker and resolved Git-root checks before every module
  can create evidence or execute the runner, plus byte-for-byte runner-copy
  verification and durable Module 5–6 resume paths.
- Made Modules 4, 5, 6, and 9 reject every unexpected runner entry before
  Python execution; preserved the exact protected `RUN-…` folder name when
  Module 6 copies a Module 5 run; and made Modules 8 and 9 validate saved run
  locators as one exact safe line inside the controlled `runs` folder.
- Made worked lesson files create-once and interruption-safe, with unfamiliar
  files preserved or safely stopped instead of overwritten.
- Changed Resume to return to the first incomplete reading or practical gate,
  preventing an out-of-order last-opened page from bypassing prerequisites.
- Made application navigation and browser Back/Forward navigation move keyboard
  focus to the new page heading, with an end-to-end browser regression check.
- Raised the practice revision so materially changed required pages reopen
  while notes, appearance, and unrelated local state remain preserved.

## 2.4.0 — 2026-07-28

### Literal-beginner Course 1 execution

- Rebuilt the Windows start route around the official Python Install Manager
  and stable Python 3.14, while verifying compatibility on Python 3.12, 3.13,
  and 3.14.
- Removed virtual-environment activation and PowerShell policy changes from the
  learner path. Every command uses the project's Python interpreter directly.
- Added exact checks for the Windows Store command alias, Documents-folder
  location, disk space, browser, Git, internet access, and safe restart or
  resume behavior.
- Fully pinned the Course 1 dependency tree and kept cloud accounts, paid
  services, application programming interface (API) keys, Node.js, n8n, and
  Google Cloud outside the required Course 1 path.
- Added safe start-or-resume sections and realistic session divisions to every
  module and required setup page.

### Runnable Course 1 reference workflow

- Added `course1_capstone`, a complete synthetic-only offline workflow that
  validates inputs, runs deterministic rules, creates source-linked summaries,
  records human approve/edit/reject/expire decisions, exports approved
  comma-separated values (CSV) and JavaScript Object Notation (JSON), and keeps
  an audit trail.
- Rebuilt Modules 4–6 around that working reference: first follow the exact
  demonstration, then recreate it with different fictional data, ask Codex for
  a bounded read-only check, and pass objective criteria.
- Added explicit normal, malformed-input, missing-file, duplicate, retry,
  artificial intelligence (AI) timeout/refusal/invalid-output, stale-revision,
  missing-evidence, edit, rejection, expiry, tamper, and fallback scenarios.
- Standardised issue identity as work-item identifier, rule code, and field;
  aligned the five current JSON schemas; and added generated-output schema
  validation.

### Assessment and evidence alignment

- Standardised the opportunity scorecard at nine factors scored 0–3, for a
  maximum of 27.
- Added completed worked examples for the risk/tool-fit and evaluation lessons,
  plus a requirement-to-practice traceability map.
- Aligned Module 8 with the actual 13-issue evaluation and a
  `PROVISIONAL PRE-UAT` recommendation, then made Module 9 preserve and reassess
  it as the `FINAL POST-UAT` decision after executable UAT, defect/retest,
  adoption, and handover evidence.
- Integrated the mandatory six-area rubric and ten oral answers into Module 9
  with a completed example, exact arithmetic check, independent recreation,
  bounded Codex review, and objective pass gate.
- Made the Module 9 solo route honest: a competent Course 1 pass is possible
  with tester-role evidence, while independent user acceptance testing remains
  explicitly unverified and is required for a Strong rating.

### Progressive web app and release controls

- Changed required progress to the complete 21-page learning sequence:
  readiness, software check, Windows Setup, nine foundations, and nine modules.
- Aligned the displayed 137–181 total-hour range with the exact sum of those
  21 page-level practice ranges.
- Kept page-read marks separate from revision-aware practical self-checks, so
  100% reading is never presented as competence.
- Kept later-course material out of default navigation and search, behind an
  intentional Career disclosure.
- Added exact wildcard rendering, 320-pixel and forced-colour safeguards,
  keyboard checks, backup/restore coverage, and a reusable real-Chrome smoke
  test.
- Added a fresh-process Course 1 acceptance runner and made it a GitHub Pages
  release gate across the supported Python range.

## 2.3.0 — 2026-07-28

### Optional advanced Course 4 capstone

- Added an optional **Controlled Document Intake** capstone to Course 4, while
  keeping Course 1's 18 core lesson identifiers and learning sequence
  unchanged.
- Added a beginner-readable readiness and cost gate followed by nine practical
  labs: local baseline, European Union (EU)-regional Document AI, evidence-
  linked extraction, Gemini candidate selection through Vertex AI, fixed
  source-linked summary/action wording, exact-output human approval,
  comma-separated values (CSV) and JavaScript Object Notation (JSON) exports,
  tests, private Cloud Run deployment, live validation, and teardown.
- Recorded an actual synthetic-only live `PASS` through private Cloud Run in
  `europe-west4`, with Document AI and Vertex AI in `eu`, followed by teardown
  to project state `DELETE_REQUESTED`.
- Recorded that the Free Trial stayed unactivated. The Billing display showed
  €0 at the checks, explicitly subject to reporting delay.
- Kept the capstone outside Course 1 completion and Resume. It is an advanced
  prototype, not a shortcut to production consulting readiness or the complete
  Course 4.

### Safety, cost, and data boundaries

- Limited the capstone to synthetic documents and explicitly prohibited real
  client, employer, medical, or personal data.
- Added a €60 maximum-spend gate, scale-to-zero settings, low quotas, resource
  labels, automatic uploaded-file deletion, live acceptance evidence, and
  resource-deletion evidence.
- Documented the actual budget teardown boundary: the ordinary alerts-only
  budget was deleted through the public Budget application programming
  interface, while the two Preview spend caps required Billing
  user-interface deletion and verification.
- Kept paid-billing activation outside the course's authority. The learner
  must stop unless the existing Google Cloud Free Trial and budget controls
  are independently confirmed; the course never instructs the learner to
  upgrade to paid billing.
- Added an explicit deadline gate for the Google Cloud credit expiry on
  26 October 2026.
- Made the Google-mode deadline, model, prompt ceiling, output-token ceiling,
  and signing-secret boundary fail closed, while keeping the offline fake mode
  usable after the live lab closes.
- Bound proposed action types to fixed findings and restricted each action's
  evidence identifiers to relevant source-field types.
- Strengthened repeatable private-access validation: public Cloud Run Identity
  and Access Management members are rejected and an unauthenticated health
  request must return `401` or `403` before a learner token is used.

### Progressive web app integration

- Added document-level `courseId` metadata so the reader can bundle optional
  material from another career course without changing the Course 1 identity.
- Added a distinct Course 4 prototype status and an **Open the optional
  capstone** action in the Career Path tab.
- Added package and PWA regression checks for the 11-page capstone bundle,
  frozen Course 1 contract, implementation package, required practice loop,
  and career-status boundary.
- Added the complete offline capstone test suite as a required, credential-free
  GitHub Pages release job.

## 2.2.0 — 2026-07-28

### One reproducible learner project

- Kept foundation rehearsals in `controlled-ai-course-practice`, then moved
  every module increment into the one Git repository created during Windows
  Setup: `AI-workflow-learning\operations-exception-assistant`.
- Added a consistent `evidence\module-01` through `evidence\module-09`
  structure, a pass-only Git checkpoint after every module, and a final
  `CAPSTONE_INDEX.md` plus project `CHANGELOG.md`.
- Connected every required capstone artifact to the module that teaches and
  produces it, including the previously unused stakeholder, baseline,
  opportunity, and data-quality worksheets.

### Honest Course 1 decision boundary

- Replaced conflicting pilot language with exactly three evidence-backed
  Course 1 outcomes: `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, and
  `DO NOT CONTINUE`.
- Made all three outcomes completable in Module 9. None authorizes a client
  pilot: discovery belongs in Course 2 and supervised low-risk pilot delivery
  belongs in Course 3.
- Standardised the external-action safety setting as
  `EXTERNAL_ACTIONS_ENABLED=false`.
- Replaced ambiguous kill-switch and Course 1 pilot-phase wording with
  explicit safe-stop, synthetic-portfolio, and later-course boundaries.

### Beginner setup and durable dependencies

- Separated the learner's read-only software check from the maintainer-only
  course update prompt.
- Made the core Course 1 path local and rule-first; the OpenAI package and n8n
  are optional labs rather than required setup.
- Pinned the small required Python package set, taught the learner to record
  the installed environment, and pinned release validation and GitHub Actions
  dependencies.
- Added the missing Python list and membership demonstration before the
  learner recreates it independently.

### Progressive web app product fixes

- Prevented learner notes from being lost during immediate navigation and
  report storage failures truthfully.
- Made Resume choose the next incomplete actionable lesson.
- Added an actionable learning sequence so Resume and previous/next insert the
  read-only software check and Windows Setup between Foundations 2 and 3,
  without counting those setup gates as core progress.
- Added secure CommonMark web links, an accessible note label and lesson
  statuses, heading focus after navigation, clearer install guidance, and
  reading-time wording that does not understate practice time.
- Reset each newly rendered page to the top after button, browser-history, or
  copied-link navigation.
- Included the build generator in update identity so manifest or icon build
  changes reach existing installed clients.
- Added regression checks for the unified repository, artifact coverage,
  decision vocabulary, maintainer boundary, links, learner state,
  accessibility, and update identity.

## 2.1.0 — 2026-07-26

### Literal-beginner practice

- Rebuilt every foundation and module exercise around a four-part
  **follow → recreate → ask Codex to check → pass** method.
- Added exact Windows clicks, commands, expected results, and bounded
  troubleshooting before independent work.
- Added a meaningfully different recreation task so copying the demonstration
  is not treated as understanding.
- Added copy-and-paste prompts for read-only Codex inspection of one explicitly
  named practice folder.
- Added objective pass criteria and kept corrections in the learner's hands.
- Rewrote the Windows setup and readiness rehearsal for a learner with no
  assumed computer or coding knowledge.
- Added a first-use terminology rule: abbreviations are written in full before
  their short form, and unfamiliar product names such as Git are defined before
  use.
- Increased the beginner planning range to 140–180 hours to include the worked
  example, independent recreation, and correction loop.

## 2.0.0 — 2026-07-26

### Career outcome

- Changed the end goal from a supplier-document system builder to a first
  foundation for becoming a **Controlled AI Workflow Implementation Consultant
  for Dutch SMEs**.
- Added an honest Course 1 capability boundary.
- Added a separate career sequence covering diagnostics, integrations,
  controlled document AI, production governance, adoption, and optional
  quality/eQMS specialization.

### Curriculum

- Preserved and expanded the absolute-beginner foundation.
- Added spreadsheets, CSV, and SME data quality as a dedicated foundation.
- Reframed AI as a bounded workflow component rather than the system authority.
- Replaced “safe vibe coding” with professional safe AI-assisted building.
- Simplified workflow-tool and data-store learning; moved Docker, FastAPI,
  Supabase, OCR, RAG, and multi-tenancy to later courses.
- Replaced 12 calendar weeks with nine gate-based consultant modules.
- Added a consultant lens, stop/rework behavior, and client-style artifact to
  every module.

### Capstone

- Replaced the advanced supplier-document capstone with a Synthetic SME
  Operations Exception Assistant using 15 fictional work items.
- Added a frozen 13-issue expected register and rules R001–R011.
- Made the deterministic exception report useful without AI.
- Made the live model lab optional and kept model ID in configuration.
- Added meaningful review, exact-revision approval, local draft outbox, kill
  switch, fallback, evaluation, UAT, adoption, and handover.
- Made `PILOT`, `REWORK`, and `DO NOT PILOT` equally valid evidence-based
  outcomes.

### Preserved advanced material

- Moved the former 12 weeks, 20-case supplier corpus, supplier schemas, and
  generation tools into
  `future_courses/course_04_controlled_document_ai/source_material/`.
- Excluded archived source material from Course 1 progress and validation.

### PWA architecture

- Added canonical `curriculum.json`.
- Added stable lesson IDs and revisions.
- Made course grouping, progress, reading order, checkpoints, and career path
  metadata-driven.
- Added a separate Career tab.
- Added state-v1 migration and old-backup support.
- Included curriculum metadata in the content and service-worker build hash.
- Preserved manifest identity, base path, cache prefix, offline bundle, and
  learner-controlled updates.

### Validation

- Replaced fixed 8-foundation/12-week/supplier-corpus assertions with
  metadata-driven Course 1 checks.
- Added practice-data and schema checks.
- Expanded PWA tests for career separation, stable IDs, migration, mobile
  navigation, and offline/update behavior.

## 1.2.x and earlier

The earlier course built a controlled synthetic supplier quotation and terms
review system. Its engineering material remains preserved as future Course 4
source material. See the archived legacy documents for the detailed 1.x
history and design.
