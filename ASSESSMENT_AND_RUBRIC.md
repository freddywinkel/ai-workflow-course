# Assessment and Rubric

## How to use this reference

This is the mandatory Course 1 assessment reference, but it is not a separate
22nd learning page. Module 9 first shows a completed fictional assessment,
then tells you exactly how to recreate the six-area rubric and ten oral answers
for your different capstone, verify the arithmetic, and request a bounded
read-only Codex check. Use this page alongside that Module 9 exercise.

Do not score from confidence. Every prerequisite, level, calculation, and oral
answer needs a relative evidence path in
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

Give each area one whole-number level from 1 to 4 using the descriptions below.
For each area, calculate:

`area points = area weight × level ÷ 4`

Add the six area-point results. The maximum is 100. Example: a level 4 in the
20% area earns `20 × 4 ÷ 4 = 20` points; level 3 earns 15 points. A learner
with levels `4, 3, 3, 3, 3, 3` earns 80 points.

Course 1 passes only when:

- every pass prerequisite above passes;
- the total is at least 75 points; and
- every area is level 3 (Competent) or level 4 (Strong).

Do not average away an unsafe area. Record the six levels, six calculated
point values, total, prerequisite result, assessor role, and date in the final
assessment evidence. Module 9 supplies an exact PowerShell arithmetic check.

The rubric score answers, “Did the learner demonstrate Course 1 competence?”
The capstone decision answers, “What should happen to this synthetic
prototype?” They are independent. A competent learner may correctly decide
`REWORK` or `DO NOT CONTINUE`; a positive prototype decision cannot repair a
failed course rubric.

## Performance levels

### 4 — Strong

Evidence is reproducible, assumptions are separated from observations, failure
behaviour is tested, decisions follow the evidence, and another person can
operate the demonstration.

### 3 — Competent

The required artifacts exist, important claims are supported, controls work,
and limitations are clear. Minor gaps do not undermine the boundary. When no
independent tester is available, a documented role-separated self-test is
allowed at this level if it is labelled `EXTERNAL UAT NOT VERIFIED`.

### 2 — Rework

The main idea is visible but evidence, tests, ownership, usability, or risk
screening is incomplete.

### 1 — Unsafe or unsupported

The learner relies on AI output, guesses data meaning, hides failures, skips
human authority, or makes production/compliance claims without evidence.

## Area 1 — Process discovery and opportunity selection

Strong evidence includes:

- a clear process trigger, input, output, owner, users, systems, handoffs, and
  fallback;
- two manual walkthroughs;
- an honest baseline with assumption labels;
- an opportunity score that considers frequency, value, reversibility,
  existing-tool fit, data readiness, and failure consequence;
- intended purpose and exclusions;
- explicit allocation to rule, AI, or human;
- a justified Module 2 selection decision for a synthetic proof, further
  discovery, or discard.

Automatic rework:

- beginning with a tool instead of a process;
- invented return on investment (ROI);
- no process owner;
- no build-versus-buy check.

## Area 2 — Data quality and deterministic controls

Strong evidence includes:

- source inventory and data dictionary;
- stable IDs and named authoritative fields;
- explicit missing, duplicate, type, date, and allowed-value rules;
- reproducible issue IDs;
- correct handling of the supplied expected issues;
- separation between source, derived issues, and output;
- fixed evaluation-date assumptions.

Automatic rework:

- silently filling missing values;
- changing expected results to match faulty code;
- AI determining objective data-quality rules.

## Area 3 — Bounded AI and evidence

Strong evidence includes:

- AI is optional and replaceable;
- structured output;
- prompt and schema versions;
- verified issue records are the only factual input;
- issue references are checked after generation;
- refusal, timeout, malformed output, and unsupported claims are tested;
- a rule-based fallback remains usable.

Automatic rework:

- AI creates authoritative exceptions;
- raw untrusted instructions control the prompt;
- schema validity is treated as truth;
- no offline test path.

## Area 4 — Human control and failure behaviour

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

Strong evidence includes:

- normal, edge, adversarial, and operational failure cases;
- false-positive, false-negative, supported-claim, time, cost, and usability
  results;
- limitations and unresolved risks;
- user acceptance testing (UAT) with another person using synthetic data for
  a Strong rating, or a clearly labelled role-separated self-test for a
  Competent rating;
- user instructions and role-specific AI literacy;
- runbook, fallback, support owner, and change record;
- portfolio story that separates facts from assumptions;
- evidence-backed `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or
  `DO NOT CONTINUE`.

Automatic rework:

- claiming savings from one synthetic timing run;
- demo succeeds only when the builder operates it;
- no owner after handover.

An independent tester is not required to complete Course 1. Without one, the
learner must not claim real user acceptance or production usability. This
keeps the course possible for a solo beginner while preserving the difference
between practice evidence and real-world validation.

## Oral demonstration questions

The learner must write and then answer aloud in plain language:

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

For each answer, record one supporting evidence path and exactly
`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES` or `NO`. A missing answer,
an unsupported answer, or `NO` means `NOT YET`. Codex may check whether the
record is complete and evidence-linked, but it must not supply missing answers
or raise scores for the learner.

## Objective Course 1 pass gate

Course 1 passes only when all of the following are true:

1. every prerequisite is explicitly `PASS` with evidence;
2. all six areas have whole-number levels;
3. every area is level 3 or 4;
4. the weighted total is at least 75;
5. all ten oral questions have supported plain-language answers;
6. all ten answers are marked
   `ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`;
7. Module 9's bounded read-only Codex review returns `PASS`.

Keep this course result separate from the workflow decision. A passing learner
may correctly finalise `REWORK` or `DO NOT CONTINUE`; an
`ACCEPT FOR SYNTHETIC PORTFOLIO` decision does not rescue a failed rubric.
