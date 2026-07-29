# Completed Example — Role-Simulated Operational Acceptance Rehearsal

- Artifact ID: WORKED-M09-UAT
- Version/date: 1.0 / 2026-07-28
- Author/rehearsal lead: course learner in a separate tester role
- Workflow/release: fictional low-stock review list 1.0
- Intended-purpose version: 1.0
- Test environment and data: synthetic local rows / STOCK-UAT-1
- Module 8 recommendation/status:
  `ACCEPT FOR SYNTHETIC PORTFOLIO` / `PROVISIONAL PRE-UAT`

The TECH-numbered scenarios are technical regression checks. Because the
learner performs them alone, this evidence is a role-simulated operational
acceptance rehearsal labelled **EXTERNAL UAT NOT VERIFIED**; it is not User
Acceptance Testing (UAT) evidence from an intended user.

## Entry criteria

Purpose, exclusions, expected results, versions, roles, unchanged source,
fallback, stop control, and known limitations were checked and passed before
testing. No secret or real record exists.

## Tester orientation

Tester role: learner acting only as a fictional inventory coordinator.
Experience represented: none; this is a role simulation. Accessibility support:
plain text, keyboard operation, and 200% zoom. Allowed: create a local internal
review list. Forbidden: order, message, pay, rank suppliers, or write back.
Reject by recording the scenario as failed and using the manual filter.

## Scenario record

| ID | Given | When | Then / exact evidence | Observed | Result / defect |
|---|---|---|---|---|---|
| TECH-01 | valid rows above thresholds | filter runs | named success; zero issues; source hash unchanged | matched | PASS |
| TECH-02 | below-threshold, blank, and text quantities | filter runs | exact linked review issues; no value invented | matched | PASS |
| TECH-03 | required header renamed | input validates | named failure; no review list | matched | PASS |
| TECH-04 | invalid quantity dependency is inspected | issue evidence is selected | one exact issue with raw value, source row, and rule | matched | PASS |
| TECH-05 | duplicate item identifier is inspected | issue evidence is selected | both source rows remain separately traceable | matched | PASS |
| TECH-06 | unsupported summary issue ID | summary validates | draft refused; rule list remains usable | matched | PASS |
| TECH-07 | reviewer approves exact draft | local export is requested | current content hash and revision bound to two local files | matched | PASS |
| TECH-08 | approved draft is edited | export is attempted | approval invalidated; no export | matched | PASS |
| TECH-09 | timeout and external-action tamper | fallback and safety checks run | manual fallback remains usable; `EXTERNAL_ACTIONS_ENABLED=false`; no action | matched | PASS |

Every scenario preserved a synthetic result note, state, reason code, and
source hash. Keyboard operation and 200% zoom remained usable. No unauthorised
action occurred.

## Candidate intended-user tasks — not executed in this worked example

These separate UAT IDs are reserved for tasks another consenting intended user
could perform. They are not aliases for the TECH scenarios and are not marked
as passed.

| ID | Predefined task | Observable success criteria | Status |
|---|---|---|---|
| UAT-01 | locate one low-stock issue | correct item and evidence path found without hidden answer | NOT EXECUTED — EXTERNAL UAT NOT VERIFIED |
| UAT-02 | trace an issue to its source and rule | source row, raw value, threshold, and rule are identified | NOT EXECUTED — EXTERNAL UAT NOT VERIFIED |
| UAT-03 | explain the draft limitation | user states that the list is internal review evidence, not an order | NOT EXECUTED — EXTERNAL UAT NOT VERIFIED |
| UAT-04 | choose approve, edit, or reject | choice and exact affected revision are explained | NOT EXECUTED — EXTERNAL UAT NOT VERIFIED |
| UAT-05 | recognise a safe failure | user distinguishes failure from a successful zero-issue result | NOT EXECUTED — EXTERNAL UAT NOT VERIFIED |
| UAT-06 | use the manual fallback | manual route and resumption owner are correctly named | NOT EXECUTED — EXTERNAL UAT NOT VERIFIED |

If executed later, the facilitator first gives the complete participant
briefing in `templates/uat_script.md`: purpose/time, voluntary participation
and right to stop, exact observations, access, retention/deletion date,
non-evaluation boundary, and synthetic-only data minimisation. Participation
consent and each proposed screen/audio/video/quotation recording choice are
separate. Each task record then adds a non-identifying participant code,
briefing version, consent choices, access roles, deletion date, intended role
and prior process experience, predefined success criteria, start/end or
elapsed time, completion, errors, help, participant comments, facilitator
interventions, evidence, defects, correction, and retest. The record must state
that synthetic testing does not establish production usability, real-data
performance, client acceptance, or employment, medical, or professional
evaluation. Missing consent or prohibited data invalidates the evidence.

## Defect log

| ID | Scenario | Severity | Observed evidence | Owner | Fix/retest | Status |
|---|---|---|---|---|---|---|
| TECH-D01 | first draft called the list “ready to order” | high | rejected wording record | reviewer | replace with “internal review draft”; rerun TECH-08 | closed |

## Rehearsal result

9 passed, 0 failed, 0 blocked after the recorded retest. High-severity defects
open: 0. Independent users represented: 0. Requirements not tested: concurrent
users, live integration, real accessibility needs, and production operation.
Decision: **ACCEPT FOR SYNTHETIC PORTFOLIO**. This is a solo role simulation:
**EXTERNAL UAT NOT VERIFIED**. Lead/process-owner review: learner / fictional
operations lead / 2026-07-28.

Effect on the provisional recommendation: confirmed after TECH-D01 was rejected,
corrected, and retested. Decision stage/status:
**FINAL POST-REHEARSAL**. `FINAL POST-UAT` is not permitted because no other
consenting intended user participated.
