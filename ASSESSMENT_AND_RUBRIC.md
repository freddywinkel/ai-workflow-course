# Assessment and Rubric

## How to use this reference

This is the mandatory Course 1 assessment reference, but it is not a separate
22nd learning page. Module 9 first shows a completed fictional assessment, then
has the learner assemble an evidence index, complete a separate self-reflection,
perform an unseen transfer task, and prepare for independent artifact and oral
assessment. Use this page alongside that Module 9 exercise.

The learner does not award their own competence result. A bounded read-only
Codex check may verify whether named artifacts and evidence links exist; it
cannot assign the final rubric levels or verify that speech occurred. Every
prerequisite, assessor level, calculation, oral result, transfer result, and
limitation needs a relative evidence path in
`evidence/module-09/recreated_course_assessment.md`.

## Assessment principle

Course 1 assesses controlled implementation judgment, not how much technology
you used.

The following can all be excellent outcomes:

- a rule-only workflow because artificial intelligence (AI) added no value;
- a bounded future AI-summary contract whose controls were strongly verified
  with the Course 1 offline mock;
- a `REWORK` decision because data quality is poor;
- a `DO NOT CONTINUE` decision because existing software is better;
- an `ACCEPT FOR SYNTHETIC PORTFOLIO` decision because every control and
  evidence gate passed.

All three named Course 1 decisions can pass when evidence-backed. None
authorizes a client pilot, real data, production use, or external action.

## Assessment roles and separate results

| Role/result | What it records | What it cannot claim |
|---|---|---|
| learner self-reflection | confidence, difficulty, help, time, and a proposed evidence map | a competence score or independent pass |
| bounded Codex artifact check | whether named files, fields, calculations, and evidence links are present | oral competence, independent judgment, real UAT, or final rubric levels |
| independent artifact assessor | evidence-backed prerequisite and rubric decisions without editing the work | speech that was not observed |
| independent oral assessor | live answers and follow-ups, one question at a time | production readiness or consulting certification |

Use these separate statuses:

- `LEARNER ARTIFACTS: READY FOR ASSESSMENT` or `NOT YET`;
- `LEARNER SELF-REFLECTION: RECORDED`;
- `ASSESSOR CALIBRATION: PASS`, `NOT YET`, or `PENDING`;
- `INDEPENDENT ARTIFACT ASSESSMENT: PASS`, `NOT YET`, or `PENDING`;
- `LEARNER ORAL COMPETENCE: VERIFIED`, `NOT YET`, or
  `SELF-ATTESTED ONLY`;
- `COURSE 1 COMPETENCE: PASS`, `NOT YET`, or `ASSESSMENT PENDING`.

`COURSE 1 COMPETENCE: PASS` requires both independent artifact assessment and
independent oral verification. If no independent assessor is available, keep
`ASSESSMENT PENDING`; completing files or speaking alone cannot self-award
competence.

## Pass prerequisites

All prerequisites must pass before scoring:

- only synthetic data was used;
- no secrets are stored in code, screenshots, notes, or **Git**, the
  version-control tool that records file changes;
- the deterministic report works with AI disabled;
- every run has a named last valid workflow state and every stopped command has
  a separate named attempt outcome;
- expected exceptions are tested;
- unsupported AI claims cannot pass silently;
- no external send, payment, deletion, or record update exists;
- editing invalidates approval;
- manual fallback is demonstrated;
- limitations and assumptions are explicit;
- the learner can explain the system without relying on generated wording.

Any failure is a stop/rework condition.

Record every prerequisite as `PASS` or `FAIL` with an evidence path. If one is
`FAIL`, the assessment result is `NOT YET` and rubric scoring cannot turn it
into a pass.

## Weighted rubric

| Area | Weight |
|---|---:|
| Process discovery and opportunity selection | 20% |
| Data quality and deterministic controls | 20% |
| Bounded AI and evidence | 15% |
| Human control and failure behaviour | 15% |
| Dutch small and medium-sized enterprise (SME) risk and tool-fit screen | 15% |
| Evaluation, adoption, and handover | 15% |

### Exact calculation

The independent artifact assessor gives each area one whole-number level from
1 to 4 using the descriptions and evidence caps below. The learner may record a
proposed level only inside the separate self-reflection; it never populates the
official score. For each area, calculate:

`area points = area weight × level ÷ 4`

Add the six area-point results. The maximum is 100. Example: a level 4 in the
20% area earns `20 × 4 ÷ 4 = 20` points; level 3 earns 15 points. A learner
with levels `4, 3, 3, 3, 3, 3` earns 80 points.

Course 1 passes only when:

- every pass prerequisite above passes;
- the total is at least 75 points; and
- every area is level 3 (Competent) or level 4 (Strong).

Do not average away an unsafe area. Record the six assessor levels, six
calculated point values, total, prerequisite result, assessor identity code and
role, calibration result, conflicts or help given, and date in the final
assessment evidence. Module 9 supplies an exact PowerShell arithmetic check.

The rubric score answers, “Did the learner demonstrate Course 1 competence?”
The capstone decision answers, “What should happen to this synthetic
prototype?” They are independent. A competent learner may correctly decide
`REWORK` or `DO NOT CONTINUE`; a positive prototype decision cannot repair a
failed course rubric.

## Calibration anchors and evidence caps

Before either assessor opens the learner result, at least two independent
assessors separately classify the four shuffled, unlabelled vignettes in
[Course 1 Assessor Calibration Cases](ASSESSOR_CALIBRATION_CASES.md). They must
not open the [Calibration Key](ASSESSOR_CALIBRATION_KEY.md) until both original
records are complete and locked. The key maps the cases to these observable
anchors:

1. **Level 1 — unsafe or unsupported:** an automatic failure survives and the
   learner cannot explain the boundary.
2. **Level 2 — rework:** the intended control is visible, but required evidence
   is missing.
3. **Level 3 — competent:** every mandatory synthetic artifact and failure gate
   is supported, limitations are explicit, and acceptance may remain
   role-simulated with `EXTERNAL UAT NOT VERIFIED`.
4. **Level 4 — strong:** Level 3 plus independent synthetic operation,
   retention, transfer, defect/retest, and handover without builder
   intervention.

The four calibration cases align assessors on the global safety boundary; they
do not replace the area-specific Level 1–4 tables below. The artifact assessor
must cite the matching observable anchor in every one of the six areas.

Each assessor records an identity code, role, date, conflict/help declaration,
and classification in a separate record before discussion. Lock each record
with its own Secure Hash Algorithm 256-bit (SHA-256) fingerprint before either
assessor sees the other's classifications. They must agree exactly on
automatic failure/rework and pass versus `NOT YET` before one calibrated
artifact assessor scores learner work. A disagreement is resolved from the
written anchor and evidence in a separate resolution record that cites both
locked hashes; never edit the original calibration records or average the
levels. If a second assessor is unavailable, record
`ASSESSOR CALIBRATION: PENDING`; the learner may continue practicing but
cannot receive `COURSE 1 COMPETENCE: PASS`.

These caps override confidence and total points:

| Missing evidence | Maximum affected level |
|---|---:|
| locked multi-outcome opportunity decision or unseen transfer | Area 1: 2 |
| learner-authored deterministic rule with normal, boundary, and failure tests, or complete R001–R011 category matrix | Area 2: 2 |
| different second-domain bounded offline AI contract | Area 3: 2 |
| approve/edit/reject/expire, exact-revision binding, safe failure, or fallback evidence | Area 4: 2 |
| risk screen, existing-tool comparison, owner, or exit path | Area 5: 2 |
| actual operator-task rehearsal, defect/retest, handover, or delayed-retention evidence | Area 6: 2 |
| external UAT by another consenting person | Areas 1 and 6 cannot exceed 3 |

Any automatic failure remains level 1 regardless of how many files exist.

## Performance levels

### 4 — Strong

Evidence is reproducible, assumptions are separated from observations, failure
behaviour is tested, decisions follow the evidence, and another person can
operate the demonstration.

### 3 — Competent

The required artifacts exist, important claims are supported, controls work,
and limitations are clear. Minor gaps do not undermine the boundary. When no
independent operator is available, a documented role-simulated operational
acceptance rehearsal is allowed at this level if it is labelled
`EXTERNAL UAT NOT VERIFIED`.

### 2 — Rework

The main idea is visible but evidence, tests, ownership, usability, or risk
screening is incomplete.

### 1 — Unsafe or unsupported

The learner relies on AI output, guesses data meaning, hides failures, skips
human authority, or makes production/compliance claims without evidence.

## Area 1 — Process discovery and opportunity selection

### Area 1 observable level anchors

| Level | Observable evidence |
|---:|---|
| 1 — unsafe or unsupported | The learner starts from a preferred tool, invents a return on investment, omits the process owner or fallback, or cannot explain the process boundary. |
| 2 — rework | A synthetic process and boundary are visible, but the trigger, owner, manual baseline, existing-tool question, locked multi-outcome decision, or supported next-evidence step is missing or internally inconsistent. |
| 3 — competent | The learner completes the two synthetic walkthroughs, as-is and stakeholder maps, assumption-labelled baseline, scorecard, intended purpose and exclusions, locked Module 2 decision, and unseen second-domain transfer; each decision follows the evidence and may legitimately be non-positive. |
| 4 — strong | Level 3 is met, and another consenting intended user can use the candidate instructions with synthetic material to validate the stated boundary and decision evidence without builder intervention; the learner then handles a new transfer variation without copying course nouns or claiming real client discovery. |

Strong evidence includes:

- a clear process trigger, input, output, owner, users, systems, handoffs, and
  fallback;
- two manual walkthroughs;
- an honest baseline with assumption labels;
- an opportunity score that considers frequency, value, reversibility,
  existing-tool fit, data readiness, and failure consequence;
- intended purpose and exclusions;
- explicit allocation to rule, AI, or human;
- a locked multi-outcome Module 2 decision made before calibration;
- a justified Module 2 selection decision for a synthetic proof, further
  discovery, or discard;
- an evidence-backed unseen second-domain transfer decision.

Automatic rework:

- beginning with a tool instead of a process;
- invented return on investment (ROI);
- no process owner;
- no build-versus-buy check.

## Area 2 — Data quality and deterministic controls

### Area 2 observable level anchors

| Level | Observable evidence |
|---:|---|
| 1 — unsafe or unsupported | The learner lets AI define objective rules, silently fills missing values, changes the expected-results oracle to fit faulty code, or cannot trace an issue to source, field, and rule. |
| 2 — rework | Some deterministic controls work, but the data dictionary, required rule-category matrix, complete R001–R011 expected keys, stable issue identity, learner-authored R012 rule, or normal/boundary/failure tests are incomplete. |
| 3 — competent | The source inventory, dictionary, contract, fixed evaluation date, complete R001–R011 matrix and expected keys, source-linked issues, and isolated learner-authored R012 rule are reproducible; the R012 tests cover normal, exact boundary, beyond boundary, wrong type, Boolean, and negative input. |
| 4 — strong | Level 3 is met, and the learner independently explains a new field or boundary case, predicts its result before running it, diagnoses a deliberately introduced deterministic defect from evidence, and corrects and retests it without an answer being supplied. |

Strong evidence includes:

- source inventory and data dictionary;
- stable IDs and named authoritative fields;
- explicit missing, duplicate, type, date, and allowed-value rules;
- reproducible issue IDs;
- correct handling of the supplied expected issues;
- separation between source, derived issues, and output;
- fixed evaluation-date assumptions;
- complete valid, failing, blank/not-applicable, and boundary examples for
  R001–R011;
- one isolated learner-authored deterministic rule with normal, exact-boundary,
  beyond-boundary, wrong-type, and negative-input tests.

Automatic rework:

- silently filling missing values;
- changing expected results to match faulty code;
- AI determining objective data-quality rules.

## Area 3 — Bounded AI and evidence

### Area 3 observable level anchors

| Level | Observable evidence |
|---:|---|
| 1 — unsafe or unsupported | AI creates authoritative exceptions or external actions, untrusted text controls instructions, schema validity is treated as truth, or the learner cannot separate generated wording from evidence. |
| 2 — rework | The supplied offline mock works, but the learner's different-domain contract, exact citations, deterministic validators, adversarial cases, fallback, or human authority is missing or copied without explanation. |
| 3 — competent | The learner designs the required different-domain offline contract with fixed inputs and labels, schema-constrained output, exact source links, rejection checks, deterministic fallback, human decision boundary, and adversarial cases, without claiming a live model or implementation. |
| 4 — strong | Level 3 is met, and the learner independently challenges a novel adversarial output, identifies the unsupported part from its exact evidence, and makes a justified `NO AI` or bounded-AI decision that another person can reproduce without builder prompting. |

Strong evidence includes:

- AI is optional and replaceable;
- structured output;
- prompt and schema versions;
- verified issue records are the only factual input;
- issue references are checked after generation;
- refusal, timeout, malformed output, and unsupported claims are tested;
- a rule-based fallback remains usable;
- a different learner-designed offline AI contract has fixed candidate labels,
  exact citations, deterministic validators, fallback, human authority, and
  adversarial examples without claiming implementation.

Automatic rework:

- AI creates authoritative exceptions;
- raw untrusted instructions control the prompt;
- schema validity is treated as truth;
- no offline test path.

## Area 4 — Human control and failure behaviour

### Area 4 observable level anchors

| Level | Observable evidence |
|---:|---|
| 1 — unsafe or unsupported | Review is ceremonial, an external action can occur without exact approval, a failure is shown as success, or the learner cannot name who has decision authority. |
| 2 — rework | Human review is described, but an approve, edit, reject, expire, revision-binding, approval-invalidation, visible-failure, retry, or manual-fallback route is absent or untested. |
| 3 — competent | Approve, edit, reject, and expire are exercised; approval is bound to the exact revision; edits invalidate approval; failures and duplicates are visible; external actions remain disabled; and the manual fallback and resumption owner are evidenced. |
| 4 — strong | Level 3 is met, and another consenting operator uses only the runbook and synthetic evidence to recognise a safe failure, choose an authorised review route, use fallback, and explain approval invalidation without builder intervention. |

Strong evidence includes:

- usable approve, edit, reject, and expire paths;
- reviewer authority and responsibility are stated;
- deterministic and AI content are distinguishable;
- approval is bound to the exact revision;
- edit invalidates approval;
- `EXTERNAL_ACTIONS_ENABLED=false` and the manual fallback work;
- retry and duplicate effects are controlled;
- failures are visible.

Automatic failure:

- external action without exact review;
- ceremonial approval where the reviewer lacks evidence or authority;
- silent failure shown as success.

## Area 5 — Dutch SME risk and tool-fit screen

### Area 5 observable level anchors

| Level | Observable evidence |
|---:|---|
| 1 — unsafe or unsupported | The learner makes a compliance conclusion, uses real sensitive data, proposes regulated or consequential use without escalation, or cannot name a risk owner. |
| 2 — rework | A risk screen exists, but an existing-tool comparison, data category, retention/access/vendor/transfer question, recurring-cost owner, specialist escalation, or exit path is missing. |
| 3 — competent | The synthetic pre-screen covers the required privacy, AI-use, vendor, security, retention, access, transfer, backup, deletion, owner, cost, existing-tool, and exit questions and states clearly that it is not legal or compliance advice. |
| 4 — strong | Level 3 is met, and the learner independently handles a novel scope or data-category change by updating the screen, narrowing or stopping the proposed use, identifying the correct specialist escalation, and explaining the decision accurately without presenting legal advice. |

Strong evidence includes:

- personal/special-category data screen;
- purpose, minimisation, retention, access, vendor, transfer, logging, backup,
  and deletion questions;
- basic provider/deployer and AI-use risk triage;
- specialist escalation points;
- review of existing Microsoft, Google, enterprise resource planning (ERP),
  customer relationship management (CRM), document management system (DMS), or
  other native capabilities;
- ownership and recurring-cost record;
- no claim of legal compliance.

Automatic rework:

- real sensitive data in the demonstration;
- regulated or consequential decisions;
- custom build proposed without checking existing capabilities.

## Area 6 — Evaluation, adoption, and handover

### Area 6 observable level anchors

| Level | Observable evidence |
|---:|---|
| 1 — unsafe or unsupported | The learner invents savings, hides defects, treats a successful demo as production proof, or cannot show a safe operational route. |
| 2 — rework | Some tests pass, but empty-denominator handling, failure cases, TECH-01–TECH-09 evidence, operator tasks, defect/retest, retention, adoption, runbook, owner, or handover evidence is missing. |
| 3 — competent | Metrics include empty-set handling; technical and operator rehearsals, defects/retests, training, adoption, runbook, fallback, owners, transfer, delayed retention, handover, and an evidence-backed final decision are complete; solo work remains `EXTERNAL UAT NOT VERIFIED`. |
| 4 — strong | Level 3 is met, and another consenting intended user performs predefined synthetic UAT tasks with role/experience, time, help, comments, interventions, defects, and retest recorded; another person can then operate and stop the demonstration from the handover without builder intervention. |

Strong evidence includes:

- normal, edge, adversarial, and operational failure cases;
- false-positive, false-negative, supported-claim, time, cost, and usability
  results;
- limitations and unresolved risks;
- user acceptance testing (UAT) with another person using synthetic data for
  a Strong rating, or a clearly labelled role-simulated operational acceptance
  rehearsal for a Competent rating;
- user instructions and role-specific AI literacy;
- runbook, fallback, support owner, and change record;
- portfolio story that separates facts from assumptions;
- role-simulated operator tasks that locate an issue, trace source and rule,
  interpret output, choose approve/edit/reject, recognise safe failure, and use
  fallback;
- delayed retention and unseen transfer results;
- evidence-backed `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or
  `DO NOT CONTINUE`.

Automatic rework:

- claiming savings from one synthetic timing run;
- demo succeeds only when the builder operates it;
- no owner after handover.

Real external UAT is not required for a Competent artifact level. Without it,
the learner must retain `EXTERNAL UAT NOT VERIFIED` and cannot claim real user
acceptance or production usability. An independent calibrated assessor is
still required for the Course 1 competence result.

## Oral demonstration questions

Before the assessment, the learner may list one evidence path per topic but
must not write or receive a script of the answers. An independent assessor asks
one question at a time:

1. What business problem are you solving?
2. What evidence says it is worth solving?
3. Which data is authoritative?
4. Which decisions are deterministic?
5. What does AI contribute?
6. What happens when AI fails?
7. What exactly does the reviewer approve?
8. What can the system never do?
9. How would you detect regression?
10. Why is your final Course 1 decision justified?

The assessor asks at least three unscripted follow-ups across:

- evidence versus assumption;
- a failure or fallback;
- the unseen transfer decision.

At least one follow-up must target an answer that is weak, vague, or
unsupported by the cited evidence. The learner may answer `I do not know` when
that is truthful, but must name a safe next step: consult the authoritative
artifact, stop the affected workflow, ask the responsible owner, or record the
uncertainty for investigation. A confident invented answer is not safer and
does not pass.

For each answer the assessor records `SUPPORTED`, `PARTIAL`, or `UNSUPPORTED`,
one evidence path, and a concise reason. The learner must not read a prepared or
generated answer. Codex may verify that the record is complete and
evidence-linked, but cannot verify speech or fill a missing answer.

If no independent person observed the assessment, record
`LEARNER ORAL COMPETENCE: SELF-ATTESTED ONLY`. That is useful reflection but is
not a verified competence pass. Record only the score and concise evidence by
default. Audio, video, screen recording, or quotations are optional and each
requires separate explicit consent; the assessment record itself is
sufficient.

## Delayed retention and unseen transfer

Immediate recreation does not prove retained or transferable skill.

- The unseen transfer uses the second work area assigned in Module 9 and has no
  worked solution. The learner records boundary, authority, rule/AI/human
  allocation, failure, evidence, approval, tool options, and a supported
  continue/discover/rework/stop decision.
- The unseen transfer and answer-free task card have matching hashes in an
  immutable JavaScript Object Notation (JSON) lock with a machine-generated
  Coordinated Universal Time (UTC) timestamp.
- Seven to fourteen elapsed whole days later, using the locked task card before
  reopening worked answers, the learner creates a record with machine check
  time and calculated elapsed interval, explains the rule/AI/human boundary,
  evidence versus assumption, safe stop, fallback, and approval invalidation,
  then performs one bounded earlier task.
- The independent assessor records help, re-study, result, and limitation.

Missing transfer or delayed-retention evidence keeps the affected area at level
2 and the competence result at `NOT YET`.

## Course 1 competence gate

Course 1 passes only when all of the following are true:

1. at least two independent assessors pass the fixed-anchor calibration;
2. every prerequisite is explicitly `PASS` with evidence;
3. a calibrated independent artifact assessor assigns all six whole-number
   levels;
4. every area is level 3 or 4;
5. the weighted total is at least 75;
6. the locked independent opportunity decision and unseen transfer pass;
7. machine-dated delayed retention passes inside the 7–14-day window and the
   transfer/task-card hashes still match;
8. an independent oral assessor verifies all ten plain-language answers and
   required follow-ups;
9. Module 9's bounded read-only Codex review reports
   `LEARNER ARTIFACTS: READY FOR ASSESSMENT`;
10. calibration, artifact, oral, role-simulated acceptance, and external-UAT
    statuses remain separate and honestly labelled.

Keep this course result separate from the workflow decision. A passing learner
may correctly finalise `REWORK` or `DO NOT CONTINUE`; an
`ACCEPT FOR SYNTHETIC PORTFOLIO` decision does not rescue a failed rubric.
