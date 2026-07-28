# Completed Example — User Acceptance Test Script

- Artifact ID: WORKED-M09-UAT
- Version/date: 1.0 / 2026-07-28
- Author/UAT lead: course learner in a separate tester role
- Workflow/release: fictional low-stock review list 1.0
- Intended-purpose version: 1.0
- Test environment and data: synthetic local rows / STOCK-UAT-1
- Module 8 recommendation/status:
  `ACCEPT FOR SYNTHETIC PORTFOLIO` / `PROVISIONAL PRE-UAT`

User Acceptance Testing (UAT) asks whether intended work can be performed. This
solo example is labelled **EXTERNAL UAT NOT VERIFIED**; it is not evidence from
an independent user.

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
| UAT-01 | valid rows above thresholds | filter runs | named success; zero issues; source hash unchanged | matched | PASS |
| UAT-02 | below-threshold, blank, and text quantities | filter runs | exact linked review issues; no value invented | matched | PASS |
| UAT-03 | required header renamed | input validates | named failure; no review list | matched | PASS |
| UAT-04 | invalid quantity dependency is inspected | issue evidence is selected | one exact issue with raw value, source row, and rule | matched | PASS |
| UAT-05 | duplicate item identifier is inspected | issue evidence is selected | both source rows remain separately traceable | matched | PASS |
| UAT-06 | unsupported summary issue ID | summary validates | draft refused; rule list remains usable | matched | PASS |
| UAT-07 | reviewer approves exact draft | local export is requested | current content hash and revision bound to two local files | matched | PASS |
| UAT-08 | approved draft is edited | export is attempted | approval invalidated; no export | matched | PASS |
| UAT-09 | timeout and external-action tamper | fallback and safety checks run | manual fallback remains usable; `EXTERNAL_ACTIONS_ENABLED=false`; no action | matched | PASS |

Every scenario preserved a synthetic result note, state, reason code, and
source hash. Keyboard operation and 200% zoom remained usable. No unauthorised
action occurred.

## Defect log

| ID | Scenario | Severity | Observed evidence | Owner | Fix/retest | Status |
|---|---|---|---|---|---|---|
| UAT-D01 | first draft called the list “ready to order” | high | rejected wording record | reviewer | replace with “internal review draft”; rerun UAT-08 | closed |

## UAT result

9 passed, 0 failed, 0 blocked after the recorded retest. High-severity defects
open: 0. Independent users represented: 0. Requirements not tested: concurrent
users, live integration, real accessibility needs, and production operation.
Decision: **ACCEPT FOR SYNTHETIC PORTFOLIO**. This is a solo role simulation:
**EXTERNAL UAT NOT VERIFIED**. Lead/process-owner review: learner / fictional
operations lead / 2026-07-28.

Effect on the provisional recommendation: confirmed after UAT-D01 was rejected,
corrected, and retested. Decision stage/status: **FINAL POST-UAT**.
