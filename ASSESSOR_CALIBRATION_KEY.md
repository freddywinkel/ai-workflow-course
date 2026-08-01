# Course 1 Assessor Calibration Key

## Open only after both calibration records are locked

Do not open this page until both assessors have completed their separate
records and each record has its own matching Secure Hash Algorithm 256-bit
(SHA-256) lock. This page is for comparison and resolution, not for editing an
original classification.

## Fixed key and rationale

| Case | Required level | Required result | Rationale |
|---|---:|:---:|---|
| Cedar | 3 | PASS | Mandatory synthetic evidence and retained skill are present, but operator acceptance remains role-simulated and external User Acceptance Testing (UAT) is unverified. |
| Harbor | 1 | NOT YET | An unsupported claim and an enabled external action are automatic failures; presentation quality cannot compensate. |
| Linden | 4 | PASS | Level 3 evidence is present plus independent synthetic operation, retention, transfer, defect/retest, and handover without builder intervention. |
| Maple | 2 | NOT YET | The intended control is visible, but missing source, owner, and learner boundary-test evidence require rework. |

## Agreement rule

Calibration passes only when both assessors:

- match all four required levels;
- identify Harbor's automatic failures;
- identify Maple's evidence cap/rework result;
- agree that Cedar passes at Competent rather than Strong;
- agree that Linden meets the Strong anchor; and
- agree on the pass versus `NOT YET` boundary.

If either record differs, the assessors discuss the written evidence and this
key, then document the exact disagreement and resolution in
`calibration_resolution.md`. They never average classifications and never edit
the locked originals. Unresolved disagreement means
`ASSESSOR CALIBRATION: NOT YET`.
