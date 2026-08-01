# Course 1 Audit Status and Repair Ledger

## Authority and current decision

This is the authoritative current product-status and repair-control record for
Course 1. Dated release acceptance records remain historical evidence, but this
file takes precedence when a later audit reopens a requirement.

- Course release under review: `2.6.0 UNVERIFIED personal-study edition`
- Audit window: `2026-07-28` to `2026-07-29` (`Europe/Amsterdam`)
- Personal-study release amendment and regression date: `2026-08-02`
- Current status: **`UNVERIFIED`**
- Distribution purpose: **`personal-synthetic-study`**
- Status owner: Course maintainer
- Audit-method authority:
  `COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md`
- Historical record affected:
  `release_evidence/COURSE_1_V2.5.0_ACCEPTANCE.md`
- Learner consequence: version 2.6.0 may be published only through the
  separately controlled personal-study lane and used for synthetic study and a
  literal-beginner trial. Public availability is not acceptance: it must not be
  used to award Course 1 completion or treated as proof of Course 2 readiness.
- Scope: Course 1 curriculum, local synthetic runner, assessment, shared
  course-reader Progressive Web App (PWA), release controls, and the Course 1
  to Course 2 handoff. Course 4 content and implementation quality are outside
  this decision except where their shared release path affects Course 1.

The earlier version 2.5.0 `PASS` was a dated decision based on the evidence
available then. It is preserved rather than rewritten and remains
**`SUPERSEDED`** for current-status purposes. The version 2.6.0 repair work
closes the reproducible local implementation defects found by the ground-up
audit: the complete bidirectional requirement-test-evidence graph and separate
all-33 final-adjudication gate now fail closed; rollback now uses one
non-contradictory per-key compare-and-preserve contract; content revision and
research/source verification have separate fields and evidence; and the
release/audit parsers reject the reproduced bypasses. The complete local
integration matrix passes. This personal-study edition is not an
accepted-release candidate: required literal-beginner, human specialist,
accepted-promotion, installed-client, and wider-device evidence does not yet
exist. The authoritative status is therefore `UNVERIFIED`, not `PASS`. The
separate distribution purpose is `personal-synthetic-study`; it is not a fifth
product status.

## Status rules

These are the only authoritative product-status values:

| Status | Meaning | Consequence |
|---|---|---|
| `PASS` | Every required High and Medium finding is closed with reproducible evidence; all required tests are current; the accepted artifact matches production; independent review and the installed-client check passed. | The named release may be used as the current Course 1 release within its stated synthetic-learning boundary. |
| `REPAIR REQUIRED` | One or more known requirements fail, a required implementation is missing, or a reproducible High or Medium defect remains. | Repair and retest. Do not promote, award a new Course 1 pass, or claim next-course readiness. |
| `UNVERIFIED` | Required evidence is missing, unavailable, expired, or could not be reproduced. No failure is being inferred. | Stop at the affected acceptance, completion, and progression gates until evidence exists. A separately authorized exact-artifact publication may still permit visibly labelled personal synthetic study. `UNVERIFIED` must never be converted to `PASS` by assumption. |
| `SUPERSEDED` | A historical decision was replaced by a later dated audit status or release. It may have been correct when recorded. | Keep the record unchanged as history and follow the newer authoritative status. |

`NO CHANGE` is a maintenance-run outcome, not a product status. A maintenance
run that finds no applicable edit leaves the existing authoritative status in
force.

### Repair-item status

- `OPEN`: no acceptable closure evidence yet.
- `PARTIAL`: governance or part of the requirement exists, but the complete
  implementation is incomplete or mixed.
- `EVIDENCE PENDING`: the implementation and applicable local regression
  checks pass, but closure requires human, repository, device,
  installed-client, or live-production evidence.
- `CLOSED`: the named closure evidence exists and was independently checked.
- `REOPENED`: a previously closed item was triggered again; treat it as open.

No High or Medium item may be waived to obtain a clean full-audit `PASS`.
Changing or removing a requirement requires an explicit, dated rationale and
the strategic-focus procedure.

### Reopen rules

Reopen the affected item and change the current release to `REPAIR REQUIRED`
or `UNVERIFIED` when any of these occurs:

1. a new High or Medium defect is reproduced;
2. a learner cannot complete a required step from a clean supported setup;
3. a security advisory affects a pinned dependency or release path;
4. an official source materially changes or its supporting claim cannot be
   reverified;
5. the public build, content hash, manifest, service worker, or accepted commit
   no longer agrees with the acceptance record;
6. an installed-client update loses, overwrites, or misattributes learner data;
7. a required test becomes flaky, is removed, or returns a different test
   count without an approved requirement change;
8. a supported platform or browser falls outside its declared support matrix;
9. a previous closure depended on evidence that has expired or cannot be
   reproduced.

Record the trigger, date, affected IDs, status change, learner consequence, and
next action here or in a dated linked audit report. Never alter an old
acceptance result to conceal the sequence of events.

## Repair ledger

Closure means the requirement, its regression test, and its evidence all pass.
File existence or a learner self-attestation alone is not closure.

### Technical and release findings

| ID | Severity | Requirement | Closure test and evidence | Status | Owner |
|---|---|---|---|---|---|
| `C1-TECH-001` | High | Audit events must use an allowed event vocabulary and lifecycle; impossible, unknown, duplicate, missing, or contradictory events must fail closed and reconciliation must detect them. | The event-specific schema and 67-test runner suite reject unknown, contradictory, missing, duplicate, equal-timestamp, and out-of-order events; independent clean-room evidence passes. | CLOSED | Runner maintainer |
| `C1-TECH-002` | Medium | Two tabs, browser windows, or installed/browser instances must not silently overwrite newer progress or notes. | The 44-test state suite and real-browser smoke cover independent writer identities, concurrent notes/progress, reset barriers, pending-note recovery, import/reset rollback, unsupported state, and concurrent recovery preservation. | CLOSED | PWA maintainer |
| `C1-TECH-003` | Medium | No supported build, validation, or continuous-integration environment may install a dependency with a known applicable vulnerability. | Exact fresh installs, `pip check`, the 67-test runner suite, and clean-room acceptance pass on Python 3.12.13, 3.13.14, and 3.14.6; the current online dependency audit passes. | CLOSED | Dependency maintainer |
| `C1-TECH-004` | Medium | Malformed expected-results data and wrong-type workspace paths must produce named beginner-safe stops; clean-room acceptance must require the declared exact test count. | Regression tests cover malformed expected CSV and file-as-folder input with no raw traceback or false lock message; deleting one expected test makes acceptance fail; independent clean-room evidence passes. | CLOSED | Runner maintainer |
| `C1-TECH-005` | Medium | Every practical gate must check every stated criterion, including an absent Git remote and the complete Module 3 example-category matrix. | Foundation 5 rejects any configured remote and passes only when no remote exists; the exact 44-case Module 3 matrix rejects a supplied meaningless `x` explanation and passes only after rule-specific correction; independent reproduction passes. | CLOSED | Curriculum maintainer |
| `C1-TECH-006` | Medium | Course 1 release acceptance and deployment must not depend on Course 4 implementation tests or treat Course 4 content as Course 1 evidence. | Local workflow inspection and scoped validation confirm separate Course 1 and Course 4 jobs and correct shared-reader triggers; deliberate GitHub-hosted failure and shared-change evidence remain repository-dependent. | EVIDENCE PENDING | Release maintainer |

### Course-goal and learning-content findings

| ID | Severity | Requirement | Closure test and evidence | Status | Owner |
|---|---|---|---|---|---|
| `C1-CONT-001` | High | The Course 1 promise must match what the learner independently does; “build” and “design” may be claimed only for bounded learner-authored work. | The promise, exercise, and observable rubric now align; closure still requires a literal learner to author the rule/tests and different offline contract without hidden help. | EVIDENCE PENDING | Curriculum maintainer |
| `C1-CONT-002` | High | Opportunity selection must test independent judgment rather than disclose the intended choice. | The unseen decision lab locks the learner decision before evaluator guidance is revealed; actual independent learner evidence remains required. | EVIDENCE PENDING | Assessment owner |
| `C1-CONT-003` | High | Final competence must be evidence-calibrated rather than primarily self-awarded. | Observable evidence caps and a bounded assessor sequence are implemented; an assessor must still apply them to an actual learner package. | EVIDENCE PENDING | Assessment owner |
| `C1-CONT-004` | High | Course 1 must test transfer of the controlled-workflow method to a second unseen synthetic work area. | The unseen transfer gate now checks the complete method; an actual learner must still complete it independently. | EVIDENCE PENDING | Assessment owner |
| `C1-CONT-005` | Medium | Safe AI-assisted building must include one real bounded AI-assisted change that the learner inspects, challenges, tests, and explains. | The lesson now requires a real bounded diff, rejected or narrowed unsafe hunks, tests, and acceptance rationale; learner evidence remains required. | EVIDENCE PENDING | Curriculum maintainer |
| `C1-CONT-006` | Medium | User acceptance testing (UAT) must test user tasks; technical contract and regression checks must be labelled separately. | User tasks and technical checks are separated and solo evidence is labelled `EXTERNAL UAT NOT VERIFIED`; an external operator test remains required. | EVIDENCE PENDING | Curriculum maintainer |
| `C1-CONT-007` | Medium | Long modules must distinguish concepts the beginner must understand from repetitive protected plumbing they only need to run, and their pass instructions must remain synchronized with controlled course inputs. | Modules 1, 2, 3, 5, and 7 use numbered blocks of no more than 60 minutes and explicit `UNDERSTAND` versus protected-plumbing labels. A final independent AI content pass found that Module 6 still hard-coded 61 tests while the current named-test manifest contained 67; Module 6 now derives the expected non-zero unique count from that manifest, compares the observed run to it, and a package regression rejects renewed hard-coding. Literal-beginner timing and usability evidence remain required. | EVIDENCE PENDING | Curriculum maintainer |
| `C1-CONT-008` | Medium | Precision and recall teaching must represent empty-set cases honestly rather than return a misleading perfect score. | Unit and lesson examples return `not applicable`/`null` for undefined empty-set cases, and independent content review confirms the convention. | CLOSED | Evaluation owner |
| `C1-CONT-009` | Medium | Course 1 must consistently distinguish synthetic discovery and acceptance rehearsal from real discovery, external UAT, and demonstrated client communication. | Traceability, promise, rubric, modules, and handoff consistently label synthetic rehearsal and do not claim completed real discovery, external UAT, or client communication; independent content review passes. | CLOSED | Curriculum maintainer |

### Audit and maintenance-governance findings

| ID | Severity | Requirement | Closure test and evidence | Status | Owner |
|---|---|---|---|---|---|
| `C1-GOV-001` | High | Current status must supersede stale historical acceptance without rewriting history. | This ledger is linked from release governance and version 2.5.0 is visibly marked historical and superseded. | CLOSED | Course maintainer |
| `C1-GOV-002` | High | Publishing must be controlled and direct unreviewed pushes must not publish. An accepted release requires candidate acceptance, promotion, live verification, and rollback; a personal-study publication must remain separately labelled and cannot close acceptance or competence gates. | The accepted-release controls inspect and bind the exact candidate and evidence. The isolated personal-study verifier accepts only `UNVERIFIED` plus `personal-synthetic-study`, rejects known defects or unclassified pending findings, deploys the exact tested artifact, and preserves the byte-verified legacy 2.5 rollback exception. Protected `main`, required checks, Pages review, live old-client update, and production rollback evidence remain repository-owner actions. | EVIDENCE PENDING | Repository owner |
| `C1-GOV-003` | High | Every product finding needs an ID, requirement, severity, owner, closure test, status, and reproducible evidence; independent-review disagreements must be retained and resolved. | This ledger and the version 2.6.0 evidence report retain the independent runner/PWA/content reviews and their adjudicated statuses. | CLOSED | Audit owner |
| `C1-GOV-004` | High | A literal beginner must complete the required journey on a clean supported Windows setup matching the declared learner environment. | The curriculum and machine preflight are ready; a fresh literal-beginner run must still record installation, every exercise, restarts, errors, corrections, duration, and final assessment without hidden state. | EVIDENCE PENDING | Beginner tester and audit owner |
| `C1-GOV-005` | Medium | Installation, browser, device, accessibility, offline, and update claims must match a declared support matrix. | Local current Chrome/Edge browser checks pass. The earlier target-size flake recurred in Edge with a measured `43.999969` pixels for a control styled at the required 44 pixels, proving browser sub-pixel reporting rather than a product undersize. The harness now retains the raw measurement and permits only an exact 0.01-pixel rounding tolerance for the 44-pixel minimum; a regression freezes both values, and final current-version plus old-client update runs pass in Chrome and Edge. Installed desktop/phone old-client, assistive-technology, and wider support-matrix evidence remain required. | EVIDENCE PENDING | PWA release reviewer |
| `C1-GOV-006` | Medium | Learner-state corruption and a bad production release must have tested, visible recovery paths. | Invalid-state quarantine, import/reset rollback, backup recovery, cache tamper recovery, and local rollback tooling pass; live last-known-good rollback and installed-client data preservation remain required. | EVIDENCE PENDING | PWA and release maintainers |
| `C1-GOV-007` | Medium | Maintenance must monitor dependency vulnerabilities, licences, end-of-life dates, and claim-level source currency rather than link availability alone. | Learner, validator, and maintainer dependency sets now have complete hash-required locks; the locked artifact inventory and Software Bill of Materials (SBOM) are machine-checked; third-party GitHub Actions use full commit hashes; toolchain versions are controlled; and offline plus online PyPI, Open Source Vulnerabilities (OSV), GitHub-action, licence, and source-claim checks pass locally. Repository alert settings, an actual scheduled-run record, and the named manual Organisation for Economic Co-operation and Development (OECD) source review remain external evidence gates. | EVIDENCE PENDING | Dependency and source owners |
| `C1-GOV-008` | Medium | Audit vocabulary must distinguish a confirmed defect from missing evidence. | Governance and evergreen instructions use `REPAIR REQUIRED` for known failures and `UNVERIFIED` only for missing evidence. | CLOSED | Audit owner |
| `C1-GOV-009` | Medium | Technical, AI-generated, human usability, Dutch SME practitioner, legal/privacy, and security review must be labelled separately. | Release evidence now labels completed automated and AI-assisted review separately from missing novice, practitioner, legal/privacy, security, accessibility, and live-release review. | EVIDENCE PENDING | Audit owner |
| `C1-GOV-010` | Medium | Course 1 exit evidence and Course 2 entry requirements must have a fixed interface that does not imply implementation readiness. | The handoff contract below is present; final Course 1 acceptance checks its package; Course 2 later verifies the same inputs without silently expanding authority. | CLOSED | Career-sequence owner |
| `C1-GOV-011` | High | Every normative requirement and named test must appear in one complete, current, machine-checked, bidirectional requirement-test-evidence graph with no missing, contradictory, duplicate, malformed, unparsed, or orphaned row. | The technical contract declares all 33 `C1-TST-*` IDs. A closed machine-readable graph binds all 118 `C1-TA-*` requirements to those tests in both directions through 133 edges; a closed manifest binds every test to an existing procedure or selector; and adversarial controls reject missing, contradictory, duplicate, unknown, orphaned, malformed, summary-only, candidate-mismatched, and incomplete evidence. A separate final-adjudication workflow downloads the exact already-promoted artifact and requires all 33 candidate-bound results, including provenance, before a final decision. Local native, browser, supply-chain, and quality executions pass, but all 33 acceptance records remain honestly `UNVERIFIED` until those results and the required independent executions are bound to one clean immutable candidate. | EVIDENCE PENDING | Technical-contract and audit owners |
| `C1-GOV-012` | High | Audit and release parsers must inventory records broadly, use closed schemas and ID families, parse only the exact authoritative structure, and fail closed on unknown, duplicate, malformed, or misleading data. | The package validator and promotion/rollback verifier require the exact current ledger inventory and reject missing or quoted finding rows, duplicate JSON keys, unknown fields, unsupported identifier families, malformed or unbackticked finding IDs, shifted cells, duplicate rows, orphaned graph nodes, non-authoritative status text, unsafe or missing evidence paths, hash mismatches, duplicate evidence, evidence bound to another candidate, self-authored summary-only evidence, incomplete declared procedure/environment artifact coverage, and incomplete operation-specific test evidence. Rollback additionally hash-validates the complete prior accepted promotion record for the exact target, with only the byte-pinned historical v2.5 exception. During the final integrated rerun, a missing Python coverage dependency exposed a quality-aggregator path whose layer was `FAIL` while the old overall result was `PASS`; the aggregator now treats every failed/nonzero command and every failed, unknown, or `NOT RUN` evidence layer as blocking, checks its maintainer runtime, and retains the reproduced false-pass regression. The ground-up artifact generator now validates all nine machine artifacts against its closed schema before writing, inventories all 30 ledger findings, detects threat/invariant and raw-evidence duplicates before mapping, rejects malformed/unknown/extra raw input, and removes only its exact owned stale-raw directory. Its exact version/date `raw/` output is also treated as opaque, hash-indexed evidence rather than generic package JSON, so adding a raw JSON record cannot silently change the learner validation report or PWA build identity; a regression test keeps unrelated `raw/` folders in scope. Closed schemas and adversarial regression tests cover every reproduced parser and aggregate-status bypass. | CLOSED | Audit-tool owner |
| `C1-GOV-013` | Medium | Rollback requirements must preserve transaction-owned prior state without overwriting an external concurrent write, and the test harness must not create the mutation it claims to detect. | `C1-TA-PWA-013` and `C1-TA-REC-007` now use one per-key compare-and-preserve contract: restore only a transaction-owned value, accept an already-restored snapshot, and preserve a third-party value for reconciliation. Primary state, reset barrier, recovery record, runtime state, route, visible render, and overall verification are reported separately. Deterministic tests distinguish application and harness actions, and real Chrome and Edge smoke tests exercise an opener-inherited `sessionStorage` writer identity plus rollback and external-write cases. A reproduced harness race showed the automatic update check changing state and replacing the expected failure toast during forced storage denial; the harness now waits on each page's own completed automatic check, records every denied storage call and raw transaction dimension, and restores the storage stub in `finally`. Three final consecutive Chrome current-version runs pass, as do the final Chrome and Edge current-version and old-client update runs. | CLOSED | PWA contract and test owners |
| `C1-GOV-014` | High | Normative audit, status, maintenance, learning, release, rollback, and historical-record authorities and their rendered consumers must not contradict each other or retain stale current-state language. | The ground-up protocol defines the authority hierarchy and `C1-AA-014`; current-status consumers defer to this ledger, historical records are visibly superseded, Evergreen is an explicitly authorized delta-repair procedure rather than a ground-up diagnosis, personal-study publication is separated from accepted-release promotion, and both exact-artifact paths preserve their own claims and gates. | CLOSED | Governance and release owners |
| `C1-GOV-015` | Medium | A content revision date and a research/source verification date must be separate claims with separate evidence; changing governance or release wording must not force a false source-currentness claim. | Curriculum schema 3 declares `contentRevisionThrough: 2026-08-02` and `sourceVerifiedThrough: 2026-07-28`; the generated PWA bundle remains schema 2 and retains `verifiedThrough` only as an equal source-date compatibility alias. The closed date contract names meanings, owners, evidence sources, and consumers. The PWA labels both claims separately. Package validation binds the content date to the latest page revision and the source date to `source_claims.json` plus its oldest entry review date, with no cross-date ceiling. Focused negative tests prove a content-only advance passes while a false source advance, alias drift, content-summary drift, or contract widening fails; the current Course 1 package validation passes. | CLOSED | Curriculum-schema and validator owners |

### Current 2.6.0 candidate evidence and remaining limits

The original repair-candidate report and audit-method gap review are retained as
dated historical evidence. The current re-adjudication package is retained as
local audit work under
`release_evidence/course1_ground_up_audit/2.6.0/2026-07-29/` and is deliberately
excluded from the public candidate because its raw machine evidence contains
local execution paths. This ledger remains the repository product-status
authority; the local audit package is not release evidence for promotion.

- The ground-up audit method and its reusable two-stage request are now
  controlled by `COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md` and
  `COURSE_1_AUDIT_REQUEST_TEMPLATE.md`.
- The local defects in `C1-GOV-011`, `C1-GOV-012`, `C1-GOV-013`, and
  `C1-GOV-015` are repaired. `C1-GOV-011` remains `EVIDENCE PENDING` because
  its 33 results have not been bound to one clean immutable candidate and
  independently executed through the final gate. No local suite or
  self-authored summary can make this study edition eligible for
  accepted-release promotion.
- The independently rechecked runner passes all 67 declared tests and
  clean-room acceptance. Fresh exact installations also pass on Python
  3.12.13, 3.13.14, and 3.14.6.
- The PWA passes all 55 unit, property, state, security, build, and migration
  tests plus current and old-to-new update smoke tests in both Chrome and Edge,
  including offline, cache-tamper, recovery, and concurrent-writer cases.
  These are local browser checks, not a public installed-client acceptance.
- Independent content review confirms the implemented opportunity,
  assessment, transfer, safe-building, user acceptance testing, block-plan,
  empty-set, and promise-boundary repairs. The requirements that judge learner
  performance remain `EVIDENCE PENDING` until a literal learner and, where
  required, a second adult produce the named evidence.
- Course 1 and Course 4 have separate local workflow scopes.
  `C1-TECH-006` remains `EVIDENCE PENDING` until GitHub records a deliberate
  Course 4-only failure and a shared-reader change.
- Direct push deployment was removed. Candidate validation, exact promotion,
  rollback tooling, dependency/source monitoring, and release templates exist.
  Branch protection, required checks, environment reviewers, scheduled-run
  evidence, live promotion, installed-client update, accessibility/device
  coverage, and production rollback remain external gates.
- Completed review types: automated curriculum/contract checks, exact Python
  matrix, local runner and clean-room tests, local PWA/browser tests,
  AI-assisted technical review, and AI-assisted curriculum review.
  Not completed: literal-novice usability, Dutch small and medium-sized
  enterprise practitioner review, independent legal/privacy review,
  independent security review, assistive-technology review, public
  production verification, and installed-device update/rollback.
- The integrated local evidence also includes the complete audit-tool suite,
  42 package
  checks with no warnings, 88 Python quality tests plus 467 generated subtests,
  Python line/branch coverage above the 90 percent threshold, PWA
  line/branch coverage above the 90 percent threshold, 9 of 9 mutation targets
  killed, 12 of 12 negative controls rejected, an online supply-chain audit
  with no reported vulnerability or advisory finding, and 26 automated source
  checks. The OECD market source still requires the recorded manual review.

## Personal-study publication lane

The user explicitly authorized this lane on 2026-08-02 so that the literal
beginner can access the repaired course before producing the human evidence
that the course is designed to collect. It is a distribution decision, not an
acceptance decision.

A personal-study publication must:

1. retain product status `UNVERIFIED` and distribution purpose
   `personal-synthetic-study` as separate machine-readable fields;
2. contain a persistent learner notice limiting use to synthetic personal
   study and denying Course 1 completion, Course 2 readiness, consulting,
   client, and production claims;
3. come from a pull request and an exact clean full commit;
4. pass the complete package, runner, Python matrix, PWA, browser-update,
   quality, source, and supply-chain jobs;
5. fail when any High or Medium finding is `OPEN`, `PARTIAL`, or `REOPENED`, or
   when an evidence-pending finding is outside the explicit study allowlist;
6. deploy the already tested artifact without rebuilding it;
7. preserve the prior learner state and the exact version 2.5 rollback target;
8. verify the public manifest-listed assets, asset manifest, and service worker
   byte-for-byte. `.nojekyll` is verified in the uploaded artifact but is not
   expected to be served by GitHub Pages;
9. leave every human learning, assessment, external-user, device,
   installed-client, final-acceptance, and Course 2 gate unchanged.

Publishing under this lane closes no ledger finding and cannot produce
`COURSE 1 COMPETENCE: PASS` or product `PASS`.

## Accepted-release lifecycle

### 1. Candidate

1. Create a review branch or pull request from a clean, synchronized tree.
2. Freeze the candidate commit, course version, content hash, build ID, test
   inventory, dependency lock, and finding IDs intended for closure.
3. Run Course 1 validation, runner tests, clean-room matrix, PWA tests,
   supported-browser checks, and source/security checks against that exact
   candidate.
4. Store raw or reproducible evidence. A summary without underlying evidence is
   not acceptance.

The workflow does not deploy an ordinary push. Repository protection is still
required so an unreviewed push cannot replace candidate source or bypass the
required review history. Until that setting is verified, avoid pushing a
repair candidate directly to `main`.

### 2. Acceptance for promotion

An independent reviewer who did not implement the relevant repair must:

1. inspect this ledger and every claimed closure;
2. reproduce the required tests;
3. record agreements, disagreements, and adjudication;
4. confirm no High or Medium item is `OPEN`, `PARTIAL`, or `REOPENED`, and no
   item is `EVIDENCE PENDING` except the promotion-dependent live checks in
   `C1-GOV-002`, `C1-GOV-005`, and `C1-GOV-006`;
5. mark the exact candidate **accepted for promotion**.

Acceptance for promotion is not yet the final product `PASS`, because public
identity and installed-client behavior still require verification.
The acceptance record must list the exact remaining promotion-dependent IDs;
the workflow rejects every other partial finding.

### 3. Promotion and live verification

1. Promote the exact accepted artifact; do not rebuild a different source
   state.
2. Verify the public version, commit locator, content hash, build ID, manifest,
   service worker, course bundle, console, navigation, offline behavior, and
   source boundary.
3. Use a preserved installed client from the prior `PASS` release. Exercise
   **Later**, **Update now**, foreground return, and cold reopen while
   preserving representative reading state, practical state, and notes.
4. Record the browser, version, operating system, device, install mode, release
   run, timestamps, and reviewer.
5. Only then set the promoted release to `PASS`.

If live evidence is unavailable, status is `UNVERIFIED`. If a known failure is
observed, status is `REPAIR REQUIRED` and rollback begins.

### 4. Rollback

1. Keep the last `PASS` commit, tag, accepted artifact identity, and release
   record available before promotion.
2. On a blocking live failure, stop further promotion and restore the exact
   last-known-good release through the controlled deployment path.
3. Verify public identity, offline cold reopen, and preserved learner state
   after rollback.
4. Record the failed candidate, trigger, rollback run, final public identity,
   and whether any learner data was affected.
5. Reopen the affected ledger IDs. The failed candidate cannot be relabelled
   `PASS` without a new candidate and complete acceptance.

## Course 1 and Course 4 release separation

Course 1 and Course 4 must have separate versions, product statuses, acceptance
records, test jobs, and release decisions.

- Course 1 acceptance covers its curriculum, local synthetic runner,
  assessment, and the shared reader behavior needed for Course 1.
- Course 4 acceptance covers its own lessons, cloud prototype, provider,
  billing, deployment, and teardown evidence.
- A Course 4 implementation or content failure must not block or substantively
  support an otherwise unchanged Course 1 release.
- A Course 4-only change must not silently change Course 1 completion,
  assessment, Resume, search, support promise, or accepted build identity.
- A change to genuinely shared PWA code, installed identity, navigation, state,
  or migration runs the shared PWA contract tests for both products, but each
  product still receives its own decision.
- Course 1 validation may verify that Course 4 is structurally non-core; it
  must not present that structural check as Course 4 content acceptance.

`C1-TECH-006` is `EVIDENCE PENDING`: Course 4 implementation tests run in a
separate non-deploying workflow, Course 1 uses the structural-only validator
scope, and Course 4-only directories are ignored by ordinary Course 1
triggers. Local implementation checks pass; closure still requires GitHub
workflow evidence for a deliberate Course 4-only failure and a shared-reader
change.

## Course 1 exit and Course 2 entry handoff

### Required Course 1 exit package

A learner is ready to enter Course 2 only when:

1. the Course 1 product release used has current status `PASS`;
2. every Course 1 prerequisite and calibrated assessment gate passes;
3. the learner preserves a synthetic-only portfolio package containing:
   - plain-language problem, boundary, intended purpose, and exclusions;
   - process, stakeholder, source, data-contract, and deterministic-rule
     evidence;
   - learner-authored rule and tests;
   - bounded AI contract and offline failure evidence;
   - human-review, approval, fallback, and no-external-action evidence;
   - evaluation, user-centred acceptance rehearsal, defect/retest, runbook,
     handover, and final decision;
   - unseen transfer-challenge evidence;
   - a limitations and unresolved-learning record;
4. the learner can explain the system and its limits without reading generated
   wording;
5. any solo test is labelled `EXTERNAL UAT NOT VERIFIED`;
6. no real, employer, client, medical, personal, confidential, credential, or
   regulated data is included.

### Course 2 entry boundary

Course 2 may use the Course 1 method and sanitized evidence as prior learning.
It must not treat the Course 1 runner as a client product or infer:

- permission to sell an implementation;
- production, legal, privacy, security, or regulated-domain competence;
- validated customer demand;
- completed real discovery or external UAT.

Course 2 begins with ethical outreach, confidentiality, interview and
observation practice, existing-system inspection, and a fictional diagnostic.
No external interview, paid diagnostic, employer observation, or client data
use is authorized by this handoff alone. Those actions require the Course 2
safety and authority gates.

## Full-audit exit gate

Course 1 returns to `PASS` only when:

1. all ledger High and Medium findings are `CLOSED`;
2. the frozen requirement-to-test map has no missing or contradictory row;
3. Course 1 and Course 4 release paths are separated;
4. dependency and source checks are current;
5. a clean supported Windows beginner journey passes;
6. fresh independent curriculum, runner, PWA, accessibility-boundary, and
   release-governance reviews agree or have documented adjudication;
7. the exact candidate is promoted and live identity matches;
8. a real installed-client update and rollback readiness check pass;
9. the Course 1 exit package satisfies the Course 2 handoff contract;
10. a dated acceptance record links every closure evidence item.
