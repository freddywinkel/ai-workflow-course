# Course 1 version 2.6.0 repair-candidate evidence

> **Historical evidence notice — superseded for current product-status
> purposes on 2026-07-29.** A later audit-of-the-audit opened or partially
> reopened `C1-GOV-011`, `C1-GOV-012`, `C1-GOV-013`, and `C1-GOV-015`: the technical
> requirement-to-test mapping is incomplete and contradictory; release/audit
> parsing still has fail-open cases; and exact-rollback wording conflicts with
> concurrent-write preservation. Content revision and source-verification
> dates are also conflated. The authoritative ledger therefore now
> records `REPAIR REQUIRED`. The checks below remain dated evidence for the
> repairs they actually exercised; they do not close the new findings or
> establish a current product decision. See
> [`COURSE_1_AUDIT_METHOD_GAP_REVIEW_2026-07-29.md`](../updates/COURSE_1_AUDIT_METHOD_GAP_REVIEW_2026-07-29.md).
>
> **Later follow-up — 2026-07-29:** the reproduced parser bypasses and the
> other known local implementation defects were subsequently repaired.
> `C1-GOV-013` and `C1-GOV-015` are `CLOSED`; `C1-GOV-007` and
> `C1-GOV-011` are `EVIDENCE PENDING`. The all-33-test gate for
> `C1-GOV-011` is implemented, but the immutable candidate-bound acceptance
> evidence is still missing. This historical report remains superseded; the
> authoritative current product status is `UNVERIFIED`, not `PASS`.

## Decision

- Audit started: `2026-07-28`
- Final integrated rerun completed: `2026-07-29`
- Timezone: `Europe/Amsterdam`
- Scope: Course 1 curriculum, local synthetic runner, Course 1 behavior in the
  shared Progressive Web App (PWA), and local release controls
- Local result: **AUTOMATED AND INDEPENDENT REPAIR CHECKS PASS**
- Product status: **`UNVERIFIED`**
- Deployment performed: no
- Cloud or billing action performed: no
- Real client, employer, medical, personal, confidential, or regulated data
  used: no

This is repair-candidate evidence, not release acceptance, learner competence,
Course 2 readiness, production readiness, or permission to sell an
implementation. The authoritative status and remaining gates are in
[`COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md`](../COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md).

The working tree was intentionally not committed, pushed, promoted, or
deployed during this repair. The current distribution therefore records the
base commit plus a content hash; it is not yet an immutable accepted candidate.

## Curriculum and learning-control result

- Course 1 now states what the learner assembles, authors, tests, and designs
  independently without presenting the supplied runner as entirely
  learner-built.
- Opportunity calibration withholds evaluator guidance until the learner
  records a decision.
- The rubric uses observable Level 1–4 evidence limits and requires another
  adult for the final assessed gates.
- The learner must transfer the controlled-workflow method to a second unseen
  synthetic work area.
- Foundation 8 requires one real bounded AI-assisted change, inspection of the
  proposed diff, rejection or narrowing of unsafe expansion, passing tests,
  and a plain-language acceptance rationale.
- Technical acceptance and user acceptance testing (UAT) are separated; solo
  rehearsal remains labelled `EXTERNAL UAT NOT VERIFIED`.
- Modules 1, 2, 3, 5, and 7 are split into numbered blocks of no more than
  60 minutes and distinguish `UNDERSTAND` from
  `PROTECTED PLUMBING — RUN AND OBSERVE`.
- Precision and recall examples represent undefined empty-set cases as not
  applicable rather than a misleading perfect score.
- The 11-rule Module 3 matrix contains 44 exact rule-specific cases. The
  supplied meaningless `x` explanation fails, a corrected case passes, the
  complete matrix passes, and failure/retest evidence is preserved.
- Independent curriculum review closed the implemented defects. Actual
  literal-beginner completion, assessor calibration, unseen transfer,
  retention, external UAT, and observed learner explanation remain required
  human evidence.

## Local runner result

Final clean-room acceptance on Python `3.12.13`:

| Check | Result |
|---|---|
| Declared runner tests | PASS, `67/67` |
| Exact test-manifest SHA-256 | `351312a904c90cb5219ff64ede849e7e04433c0e966c4b75058a95170292041e` |
| Expected issues | `13` |
| Local export files | `2` |
| External actions | `0` |
| Audit events | `8` |
| Protected source files unchanged | `31` |
| Temporary clean-room removed | yes |

The independently rechecked runner rejects unknown or contradictory audit
events, missing lifecycle events, duplicates, equal or decreasing timestamps,
malformed expected data, wrong-type workspace paths, oversized or replaced
inputs, unsafe export targets, and changed test inventories with named
failures. Its owned export staging does not overwrite unrelated files and
rolls back incomplete publication.

## Fresh exact Python matrix

Each environment was created separately, installed from the exact current
requirements, passed `pip check`, ran all 67 tests, and passed clean-room
acceptance.

| Python | Result |
|---|---|
| `3.12.13` | PASS |
| `3.13.14` | PASS |
| `3.14.6` | PASS |

This closes the named local Python compatibility and dependency repair. It does
not replace continuous-integration evidence for the eventual committed
candidate.

## PWA result

Final exact local runtime: Node.js `24.18.0`.

| Check | Result |
|---|---|
| PWA state, security, and contract tests | PASS, `44/44` |
| Production build | PASS |
| Google Chrome `150.0.7871.187` browser smoke | PASS |
| Microsoft Edge `150.0.4078.99` browser smoke | PASS |
| Update, cache-tamper, and offline smoke | PASS |
| npm advisory audit | PASS, `0` vulnerabilities |
| Main-agent desktop and 390 × 844 phone inspection | PASS; no UI code changed afterward |
| Main-agent browser console | PASS, no warnings or errors |

The browser checks cover distinct writer identities, concurrent progress and
notes, visible conflict recovery, pending-note recovery, reset barriers,
unsupported-state quarantine, strict import validation, import/reset rollback
through storage and rendering, preservation of newer recovery data, accessible
in-app confirmation, focus restoration, responsive navigation, offline use,
candidate rejection, update activation, state preservation, asset/manifest
tamper rejection, network repair, and last-valid-cache preservation.

The main-agent visual pass confirmed the home, career, and settings screens at
desktop and phone sizes. It also confirmed that reset uses an in-app dialog,
explicit cancellation restores focus, and no native browser confirmation is
created. The dedicated Chrome smoke separately verifies Escape cancellation.

Final local distribution identity after the version bump:

- Course version: `2.6.0`
- Build ID: `79fb73215b11`
- Content SHA-256:
  `88854c8ce6b62720e5ed3cbe8555741de5bfa46e3af15f52483d4d06fcddb130`
- Base commit recorded by the uncommitted build:
  `82abb64d7402f1102f459f7caef452510e4872a7`
- Asset-manifest SHA-256:
  `0cf7844d2ac09dce08a85ebc8e09296574507c55dfa7aab17629d04b073dfd4f`

## Package, source, and supply-chain result

| Check | Result |
|---|---|
| Course 1 package validator | PASS, `37` checks, `0` warnings |
| Tracked and candidate JSON parsing | PASS, `70` files |
| YAML parsing | PASS, `6` files |
| GitHub Actions static validation | PASS |
| Promotion-status regression tests | PASS, `11/11` |
| Repository whitespace/error scan | PASS |
| Exact Python dependency inventory | PASS, `13` packages |
| Licence allow-list, source hashes, PyPI metadata, and Software Bill of Materials agreement | PASS |
| PyPI and Open Source Vulnerabilities advisory checks | PASS, no reported vulnerabilities |
| Automated official-source checks | PASS, `26` |
| Organisation for Economic Co-operation and Development manual source check | PASS at the official locator during the audit window |

The source tool correctly returns `PASS_WITH_MANUAL_REVIEW_REQUIRED` until the
manual Organisation for Economic Co-operation and Development source is
opened. Link availability is not treated as proof that a claim remains
correct.

## Independent review

Separate reviewers re-ran and inspected the runner, PWA, curriculum repairs,
status vocabulary, and Course 1/Course 4 boundary. Their findings were retained
and adjudicated rather than silently overwritten.

- The final technical re-audit closed all 12 previously reported local
  technical defects in their defined scope.
- The final curriculum re-audit closed the Module 3 implementation gate and
  the long-session/block-plan implementation gate.
- The final governance read found stale historical wording, a missing evidence
  record, and a promotion-parser defect that could omit `EVIDENCE PENDING`
  rows. The parser now requires all six ledger columns, rejects unknown,
  shifted, duplicate, partial, open, and reopened rows, and permits pending
  evidence only for the three named live-promotion gates.
- Eleven direct promotion/rollback-status regressions pass. The current ledger correctly
  produces an expected rejection for its 11 non-promotion evidence gaps, and
  an empty recorded-ID list is also rejected because the three live-promotion
  IDs must match exactly.

The later audit-of-the-audit showed that this dated parser conclusion was too
broad. Malformed, unbackticked, wrong-prefix, and undeclared-family finding
IDs, rollback status matching, unknown or duplicate JSON keys, and unproved
evidence locators were not covered. See `C1-GOV-012`; the passing regressions
above remain evidence only for the cases they actually exercised.

All reviews were AI-assisted. They are independent of the owning edit, but are
not substitutes for the named human expert, novice, device, repository, or
live-production reviews.

## Learner-computer preflight

The target computer preflight recorded:

| Item | Observed |
|---|---|
| Operating system | Windows 11 Home, 64-bit |
| PowerShell | `5.1.26100.8894` |
| Git | `2.54.0.windows.1` |
| Visual Studio Code | `1.130.0` |
| Google Chrome | `150.0.7871.187` |
| Microsoft Edge | `150.0.4078.99` |
| Free space on the system drive | `766.3 GB` |
| Practice folder | exists and is empty |
| Implementation exercise folder | correctly absent before the modules |

Python is not yet installed for the learner through the supported Windows
setup route; the current `python` command is only the Windows application
alias. This is expected before the Beginner Software Check and Windows Setup
lesson. The clean test runtimes used for this audit do not count as the
learner's setup.

## Remaining evidence gates

The product remains `UNVERIFIED` until all applicable ledger items close.
Required evidence still includes:

1. literal-beginner completion on a fresh supported Windows learner setup,
   with time, confusion, errors, corrections, restarts, fatigue, and successful
   retest recorded;
2. independent learner authorship, unseen opportunity and transfer decisions,
   delayed retention, explanation, and calibrated second-adult assessment;
3. external operator UAT rather than solo rehearsal;
4. Dutch small and medium-sized enterprise practitioner, legal/privacy,
   security, accessibility, and assistive-technology review;
5. wider declared browser, desktop-install, and phone-install coverage;
6. protected repository settings, required checks, controlled Pages
   environment reviewers, and recorded Course 1/Course 4 workflow negative
   controls;
7. an immutable committed candidate and independent acceptance record;
8. exact-artifact public promotion, public identity verification, a preserved
   old installed-client update, and a production rollback that preserves
   learner state.

No missing gate may be converted to `PASS` by assumption.
