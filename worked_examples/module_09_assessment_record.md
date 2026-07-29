# Completed Example — Independent Course 1 Assessment Record

This fictional example demonstrates the assessor's record format. It does not
contain reusable oral-answer scripts and it is not a learner answer key.

## Assessment identity and boundary

- Artifact ID: `WORKED-M09-ASSESSMENT`
- Version/date: `2.0 / 2026-07-28`
- Learner code: `WORKED-LEARNER`
- Independent assessor code: `WORKED-ASSESSOR`
- Independent calibration assessor codes: `WORKED-CAL-A` and `WORKED-CAL-B`
- Assessor conflict/help declaration: did not create or edit the evidence;
  provided no correction during assessment
- Workflow: fictional low-stock review list
- Data: synthetic only
- Acceptance status: role-simulated operational acceptance rehearsal;
  `EXTERNAL UAT NOT VERIFIED`
- Scope: Course 1 learning evidence only; no certification, client acceptance,
  production approval, legal compliance, security assurance, or accessibility
  assurance

## Calibration record — two assessors only

Both calibration assessors independently classified the four shuffled
vignettes in `ASSESSOR_CALIBRATION_CASES.md` before either opened the learner
result or `ASSESSOR_CALIBRATION_KEY.md`. They recorded their judgments before
discussion:

| Case | Required classification | WORKED-CAL-A | WORKED-CAL-B | Exact agreement |
|---|---:|---:|---:|:---:|
| Cedar | 3 | 3 | 3 | yes |
| Harbor | 1 | 1 | 1 | yes |
| Linden | 4 | 4 | 4 | yes |
| Maple | 2 | 2 | 2 | yes |

Both assessors declared no role in creating or correcting the evidence.
Their separate pre-discussion records were locked first:

- `calibration_assessor_a.md` / SHA-256 `WORKED-CAL-A-HASH`;
- `calibration_assessor_b.md` / SHA-256 `WORKED-CAL-B-HASH`.

The separate `calibration_resolution.md` cited both locked hashes and recorded
the exact agreement above. Neither original calibration record was edited
after comparison.

Automatic failure/rework and pass/`NOT YET` calibration:
`ASSESSOR CALIBRATION: PASS`. `WORKED-CAL-A`, also identified as
`WORKED-ASSESSOR`, then performed the artifact assessment.

## Pass prerequisites

| Prerequisite | Assessor result | Example evidence | Assessor reason |
|---|:---:|---|---|
| synthetic data only | PASS | `worked/source-register.md` | source inventory is fictional and bounded |
| no secrets or external action | PASS | `worked/safety-drill.md` | prohibited paths are absent and control evidence is present |
| deterministic path works without AI | PASS | `worked/rule-test.txt` | frozen expected cases pass |
| learner-authored bounded rule and tests | PASS | `worked/learner-rule-test.txt` | normal, boundary, and failure cases are present |
| supported claims and visible failures | PASS | `worked/failure-evidence.md` | unsupported and malformed cases stop |
| approval invalidation and fallback | PASS | `worked/review-drill.md` | changed revision cannot reuse approval |
| limitations and assumptions explicit | PASS | `worked/handover.md` | synthetic and external-UAT limits are prominent |
| unseen transfer and delayed retention | PASS | `worked/transfer-and-retention.md` | different work area and delayed result passed |

All prerequisites pass, so official scoring may continue.

## Six-area rubric — assessor only

| Area | Weight | Assessor level | Points | Evidence, cap, and reason |
|---|---:|---:|---:|---|
| Process discovery and opportunity selection | 20 | 3 | 15 | Locked multi-outcome decision and unseen transfer are supported. Synthetic evidence caps the claim. |
| Data quality and deterministic controls | 20 | 3 | 15 | Dictionary, full rule-example matrix, expected issues, and learner-authored rule tests pass. |
| Bounded AI and evidence | 15 | 3 | 11.25 | Optional AI remains replaceable; a different offline contract has citations, validators, fallback, and adversarial cases. |
| Human control and failure behaviour | 15 | 3 | 11.25 | Exact-revision approval, edit/reject/expire, safe failures, fallback, and zero actions are evidenced. |
| Dutch SME risk and tool-fit screen | 15 | 3 | 11.25 | Risk, existing-tool, ownership, cost, escalation, and exit questions are explicit without a compliance claim. |
| Evaluation, adoption, and handover | 15 | 3 | 11.25 | Operator rehearsal, defect/retest, retention, runbook, owners, and handover pass; external UAT remains unverified. |

- Official total: `75`
- Every area at least level 3: `yes`
- Artifact-assessment result: `PASS`
- Level 4 not awarded because no other intended user performed real synthetic
  UAT in this example.

## Independent oral result — assessor only

The assessor asked the ten fixed questions one at a time without showing a
prepared answer. This example records results and reasons, not answer wording:

| Question topic | Result | Evidence | Assessor observation |
|---|:---:|---|---|
| business problem and boundary | SUPPORTED | `worked/process-map.md` | learner separated internal review from external action |
| evidence that it is worth investigating | SUPPORTED | `worked/baseline.md` | learner called the value provisional |
| authoritative data | SUPPORTED | `worked/data-dictionary.md` | source and derived output were distinguished |
| deterministic decisions | SUPPORTED | `worked/rule-register.md` | learner named rule and boundary examples |
| optional AI contribution | SUPPORTED | `worked/ai-contract.md` | learner kept AI optional and source-bound |
| AI failure | SUPPORTED | `worked/fallback-rehearsal.md` | deterministic fallback was described |
| exact reviewer decision | SUPPORTED | `worked/review-drill.md` | exact revision and evidence were named |
| forbidden capability | SUPPORTED | `worked/safety-drill.md` | no send, order, payment, deletion, or write-back |
| regression detection | SUPPORTED | `worked/regression-policy.md` | frozen expected cases and failure routes were named |
| final decision | SUPPORTED | `worked/final-decision.md` | evidence and limitation matched the label |

Follow-ups on evidence versus assumption, approval invalidation, and the unseen
transfer were all `SUPPORTED`.

`LEARNER ORAL COMPETENCE: VERIFIED`

## Transfer, retention, and communication

- unseen second-domain transfer: `PASS`;
- delayed retention after 9 days: `PASS`;
- Dutch explanation: bounded rehearsal reviewed by a Dutch-speaking fictional
  reviewer; no client-readiness claim;
- real external UAT: `NOT VERIFIED`.

## Assessment result and limitations

- Independent artifact assessment: `PASS`
- Independent oral assessment: `VERIFIED`
- Course 1 competence: `PASS`
- Separate workflow decision: `ACCEPT FOR SYNTHETIC PORTFOLIO`

Limitations: fictional assessor example, synthetic data, small volume,
role-simulated acceptance only, no real client discovery, no production
environment, no market-demand proof, and no professional certification or
legal/compliance assurance.
