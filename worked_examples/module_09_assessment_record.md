# Completed Example — Course 1 Assessment Record

This is a fictional worked example, not a learner answer key. It shows how to
turn evidence into the mandatory six-area score and ten plain-language oral
answers. The selected low-stock workflow is synthetic, local, and rule-only.

## Assessment identity and boundary

- Artifact ID: WORKED-M09-ASSESSMENT
- Version/date: 1.0 / 2026-07-28
- Assessor role: course learner performing a documented self-assessment
- Workflow: fictional low-stock review list 1.0
- Data: synthetic only
- External actions: none
- UAT status: `EXTERNAL UAT NOT VERIFIED`

This assessment supports a Course 1 learning result only. It is not a
professional certification, client acceptance, production approval, or legal,
privacy, security, or accessibility assurance.

## Pass prerequisites

| Prerequisite | Result | Example evidence |
|---|:---:|---|
| only synthetic data used | PASS | `worked/source-register.md` |
| no secrets in code, notes, screenshots, or Git | PASS | `worked/secret-check.txt` |
| deterministic report works with AI disabled | PASS | `worked/rule-test.txt` |
| every run has a named last valid workflow state and every stopped command has a named attempt outcome | PASS | `worked/state-results.md` |
| expected exceptions tested | PASS | `worked/frozen-metrics.json` |
| unsupported AI claims cannot pass silently | PASS | AI excluded; boundary in `worked/tool-decision.md` |
| no send, payment, deletion, or source update exists | PASS | `worked/safety-drill.md` |
| editing invalidates approval | PASS | `worked/review-drill.md` |
| manual fallback demonstrated | PASS | `worked/fallback-rehearsal.md` |
| limitations and assumptions explicit | PASS | `worked/handover.md` |
| learner explains the system without generated wording | PASS | ten oral answers below |

Every prerequisite passes, so scoring may continue.

## Six-area rubric

| Area | Weight | Level (1-4) | Points = weight x level / 4 | Evidence and reason |
|---|---:|---:|---:|---|
| Process discovery and opportunity selection | 20 | 3 | 15 | Trigger, owner, users, two walkthroughs, baseline, alternatives, and selection are in the worked discovery pack. The evidence is synthetic rather than client-validated. |
| Data quality and deterministic controls | 20 | 3 | 15 | Dictionary, IDs, rule table, frozen expected results, source links, and fixed date all pass. Reproduction is local and small-volume only. |
| Bounded AI and evidence | 15 | 3 | 11.25 | AI was deliberately excluded because it added no justified value; the rule-based output and boundary are evidenced. |
| Human control and failure behaviour | 15 | 3 | 11.25 | Review, changed-output invalidation, stop states, external-action block, and fallback are demonstrated in the synthetic drill. |
| Dutch SME risk and tool-fit screen | 15 | 3 | 11.25 | Data sensitivity, retention, access, vendor, existing-tool fit, ownership, recurring effort, escalation, and exit were screened without a compliance claim. |
| Evaluation, adoption, and handover | 15 | 3 | 11.25 | Metrics, scenarios, role training, UAT, defect/retest, runbook, owners, and final decision exist. Solo testing remains `EXTERNAL UAT NOT VERIFIED`, so Strong is not claimed. |

Calculation:

- points: `15 + 15 + 11.25 + 11.25 + 11.25 + 11.25`;
- total: `75`;
- every area is at least level `3`;
- score gate: `PASS`.

The score is exactly the minimum pass. It does not turn missing independent
user evidence into a Strong result.

## Ten oral demonstration answers

Each answer below is short enough to say naturally. The learner would still
need to say it aloud without reading this example.

### 1. What business problem are you solving?

A fictional inventory coordinator repeatedly scans a stock sheet to find
quantities below agreed thresholds. The workflow makes that review list; it
does not order anything. Evidence: `worked/process-map.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 2. What evidence says it is worth solving?

Two synthetic walkthroughs show the same repeated scan and a timed baseline.
That suggests a practice opportunity, not proven client demand or savings.
Evidence: `worked/baseline.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 3. Which data is authoritative?

The preserved synthetic source rows and the approved threshold table are
authoritative. The exception list is derived and can be regenerated.
Evidence: `worked/data-dictionary.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 4. Which decisions are deterministic?

Header checks, value checks, threshold comparisons, issue identities, and
named states follow written rules and must give the same result on the same
input. Evidence: `worked/rule-register.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 5. What does AI contribute?

Nothing in this selected worked solution. The evidence did not justify adding
AI, so a rule-only workflow is the safer fit. Evidence:
`worked/tool-decision.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 6. What happens when AI fails?

There is no AI dependency here. If a later optional summary were unavailable
or unsupported, the reviewer would use the deterministic issue list and
manual fallback. Evidence: `worked/fallback-rehearsal.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 7. What exactly does the reviewer approve?

The reviewer approves one exact, source-linked internal review list after
checking its rules, source values, version, and limitations. Any change
requires a new review. Evidence: `worked/review-drill.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 8. What can the system never do?

It cannot send, order, pay, delete, update the source, choose a supplier, or
make an external decision. Evidence: `worked/safety-drill.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 9. How would you detect regression?

I would rerun the frozen normal, edge, failure, review, and fallback cases
after a change and compare the named states and exact issue identities with
the approved expected results. Evidence: `worked/regression-policy.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

### 10. Why is your final Course 1 decision justified?

The frozen synthetic checks, safe failures, role-simulated UAT, defect retest,
training, and handover meet the practice thresholds, so
`ACCEPT FOR SYNTHETIC PORTFOLIO` is supported. The label stays limited to a
synthetic demonstration because no client, real data, production operation, or
independent user acceptance exists. Evidence: `worked/final-decision.md`.

`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`

## Assessment result and limitations

- Prerequisites: PASS
- Rubric total: 75/100
- Every area at least Competent: yes
- Ten supported oral answers: yes
- Oral delivery without reading generated wording: yes
- Course 1 assessment: PASS
- Separate final prototype decision: `ACCEPT FOR SYNTHETIC PORTFOLIO`

Limitations: self-assessed fictional example, synthetic data, tiny volume,
role-separated solo UAT, no independent user, no production environment, and
no professional certification or legal/compliance assurance.
