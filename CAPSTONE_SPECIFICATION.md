# Capstone Specification — Synthetic Small and Medium-sized Enterprise (SME) Operations Exception Assistant

## How to use this reference

This is the final acceptance reference, not an unguided practice task. Complete
Modules 1–9 in order. Each module first demonstrates its part of the capstone,
then asks you to recreate it, gives you a read-only Codex inspection prompt,
and states the pass criteria. Return here only to confirm that the combined
result is complete.

## Purpose

Demonstrate that you can diagnose, design, build, evaluate, and hand over one
bounded workflow without confusing a technical prototype with a production
solution.

## Fictional organization

`Northstar Services BV` is a fictional Dutch business-to-business (B2B)
service SME. **BV** is the Dutch abbreviation for *besloten vennootschap*, a
private limited company. Its operations team reviews a weekly export of work
items. The manual process is slow and inconsistent, but the organization has
not yet proved that artificial intelligence (AI) is needed.

All supplied records are synthetic.

## Required outcome

The system:

1. accepts `practice_data/work_items.csv`;
2. validates its structure;
3. applies deterministic exception rules;
4. produces issue records that can be compared with
   `practice_data/expected_issues.csv`;
5. creates a readable rule-based report;
6. creates a schema-constrained offline-mock or deterministic-fallback summary
   using only verified issue records;
7. verifies every summary and review-action issue reference;
8. creates a review package showing source row, issue, and limitation;
9. supports approve, edit, reject, and expire;
10. invalidates approval after an edit;
11. writes approved content only to a local draft outbox;
12. records material audit events;
13. keeps `EXTERNAL_ACTIONS_ENABLED=false` and supports a manual fallback;
14. produces an evaluation and exactly one Course 1 recommendation:
    `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or `DO NOT CONTINUE`.

For the frozen supplied dataset, the deterministic result is 13 expected issue
keys across 15 work items using rules R001–R011 and the assessment date
`2026-07-26`. The canonical issue key is the exact triple
`(work_item_id, rule_code, field)`. The string form is
`WI-0002|R007|owner_role`. A comparison that omits `field` does not satisfy
this specification.

## Required process evidence

Before building, produce:

- stakeholder and user map;
- as-is process map;
- two observed manual walkthroughs using synthetic cases;
- baseline for volume, handling time, waiting time, and rework assumptions;
- opportunity scorecard;
- intended purpose and exclusions;
- rule/AI/human allocation;
- build-versus-buy check;
- explicit Module 2 selection decision: select for synthetic proof, discover
  further, or discard.

Course 1 has one required reference workflow: the supplied Synthetic SME
Operations Exception Assistant. Do not replace it with another workflow inside
Modules 3-9, because their fixtures, runner, checks, and answer keys implement
this exact reference. If the scorecard supports stopping, preserve that
evidence-backed stop decision and still complete the reference workflow as a
controlled skills exercise. The final recommendation may honestly be `DO NOT
CONTINUE`; building the reference does not turn that stop into a business
approval. A supported stop is evidence of judgment, not a failed exercise.

## Required data evidence

Produce:

- source inventory;
- data dictionary;
- field-level source-of-truth decisions;
- null, duplicate, type, and date rules;
- synthetic-data statement;
- expected-issue register;
- data-quality findings;
- written evaluation date and locale assumptions.

Do not “clean” the supplied evaluation data by deleting difficult cases.

## Required implementation

The working reference implementation is in `course1_capstone/`. Module 4
copies `workflow.py` and `cli.py` into the learner repository; Modules 4-6
execute those copies through the exact project interpreter. The implementation
uses only Python's standard library at runtime and has no network client or
external-action function. Completion does not depend on a visual workflow tool
or vendor.

Required characteristics:

- environment-specific settings are configuration;
- secrets are not in code or **Git**, the version-control tool that records file
  changes;
- the deterministic checker runs without a model application programming
  interface (API);
- every run has a traceable run ID;
- every run keeps a named last valid `current_state`;
- every stopped command records a visible `failed_manual` attempt outcome
  without disguising or overwriting that last valid workflow state, while
  preserving every repeated attempt separately;
- duplicate retries are safe;
- output folders are separated from source data;
- tests run without paid API calls;
- input is refused without the exact synthetic-data acknowledgement;
- summary actions are limited to source-linked `human_review` actions with
  `external_action=false`;
- summary headlines, group prose, and review instructions are rendered from
  controlled allow-listed templates rather than trusted because of a
  self-declared boolean;
- one exclusive local workspace/run lock prevents simultaneous processes from
  racing; an abandoned visible lock is removed only after human verification;
- only an approved, evidence-reviewed, unexpired exact revision can create
  local CSV and JSON;
- run identity includes the exact input, expected-oracle presence/hash, fixed
  date, rules, pipeline, prompt, requested adapter mode, and mock/fallback
  versions;
- approval binds a recomputed manifest of the source, issue JSON/CSV, summary,
  control, run configuration, and review package;
- the JSON/CSV export pair is checked and staged before publication, and CSV
  formula prefixes are made spreadsheet-safe without changing JSON/source
  evidence;
- approve, edit, reject, and expire cause separate enforced states;
- every generated issue, summary, run configuration, control, state, review
  package, review manifest, decision, audit event, and evaluation matches the
  canonical schema in `schemas/`.

The runnable artifact flow is:

```text
synthetic CSV
  -> input validation
  -> deterministic R001-R011 issues
  -> offline mock or deterministic fallback
  -> source-linked review package and protected manifest
  -> explicit human decision
  -> exact artifact/decision/revision/expiry recheck
  -> approved local CSV and JSON only
```

## Later-course live AI boundary

No live provider is used in the Course 1 capstone or its acceptance tests.
Course 1 teaches the replaceable boundary with an offline mock and fault
simulation. A later course may authorize a separate synthetic live lab after
its value, provider fit, cost, privacy, security, and teardown are assessed.
The following requirements belong to that later course, not to Course 1. If
such a later lab is approved:

- select a currently supported model through configuration;
- use a provider API that can return JavaScript Object Notation (JSON)
  Schema-constrained output;
- record the provider, model identifier, prompt version, date, latency, and
  cost estimate;
- send only synthetic verified issue records;
- detect refusal and invalid output;
- verify all issue IDs after generation;
- compare the later live result with the frozen Course 1 offline mock.

Using a flagship model is not a course requirement. Promotional credit or an
expiry date is not sufficient reason to add a provider to Course 1.

## Human-control acceptance

The reviewer must be able to see:

- why each item was flagged;
- the original synthetic row values needed to understand the issue;
- which text came from deterministic rules;
- which text came from the offline mock or deterministic fallback;
- unsupported or uncertain statements;
- the exact draft being approved;
- what will and will not happen after approval;
- how to reject, edit, expire, or use the manual fallback.

The approval action must never imply that the reviewer is certifying legal or
regulatory compliance.

## Required tests

### Normal and edge cases

- valid row with no exception;
- missing required value;
- invalid status;
- duplicate item ID;
- duplicate reference;
- contradictory dates;
- overdue open item;
- required review without evidence;
- stale update;
- malformed input;
- untrusted instructions in free text.
- a dangerous free-text review instruction paired with
  `external_action=false`;
- schema-valid evaluation, state, or export evidence edited after creation;
- two simultaneous operations targeting the same workspace or run.

### Operational failures

- missing file;
- unexpected header;
- duplicate retry;
- AI disabled;
- AI timeout;
- AI refusal;
- malformed AI JSON;
- unknown AI issue reference;
- edited draft after approval;
- edit decision and new revision;
- rejected decision;
- explicit expire decision;
- expired review;
- `EXTERNAL_ACTIONS_ENABLED=false` safety control;
- tampering that changes `EXTERNAL_ACTIONS_ENABLED` to true.
- schema-valid issue or review-package tampering;
- a changed reviewer, reason, or prior expiry in a saved decision;
- damaged state or audit JSON;
- an existing conflicting half-export or simulated second-file write failure;
- spreadsheet-formula prefixes after optional whitespace/control characters.

### Invariants

- no issue exists without a rule result;
- no AI factual claim exists without a verified issue ID or unsupported label;
- no external action occurs;
- one run key creates at most one logical CSV-and-JSON export pair per approved
  revision;
- changed protected review evidence cannot reuse an old approval;
- changing any material decision field invalidates its local decision
  fingerprint (which is tamper detection, not reviewer authentication);
- no failed export leaves one newly approved JSON/CSV filename without its pair;
- manual fallback produces a usable report;
- a failed run never appears successful.

### Executable acceptance

`course1_capstone/tests/SCENARIO_MATRIX.md` maps every scenario above to a
fixture or automated test. From the course repository, run:

```powershell
$pythonExe = Join-Path (Get-Location) '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Course project Python missing. Complete Windows Setup.'
}
& $pythonExe -m unittest discover -s course1_capstone\tests -v
```

Acceptance requires every test to report `ok`, the final result `OK`, and exit
code 0. Do not substitute bare `python` or remove a failing test.

## Evaluation

Report at least:

- expected issues detected;
- missed issues;
- false alarms;
- unsupported generated claims;
- correct issue references;
- simulated refusal and failure handling;
- repeatability across identical runs;
- manual versus assisted handling time;
- observed local prototype cost, with live-provider cost marked `not
  applicable` in Course 1;
- reviewer usability;
- limitations and unresolved risks.

Do not use a mandatory percentage-improvement threshold. Small synthetic timing
studies are not forecasts.

The runnable Modules 4-6 evaluation remains `REWORK` even when all technical
tests pass. That is deliberate: the runner cannot prove discovery, value, risk
ownership, usability, adoption, or handover. Module 8 records one
`PROVISIONAL PRE-UAT` recommendation. Module 9 preserves it, adds UAT,
defect/retest, adoption, and handover evidence, then records exactly one
`FINAL POST-UAT` Course 1 recommendation.

## Required handover pack

- one-page intended purpose and boundary;
- as-is and to-be maps;
- architecture diagram;
- data dictionary;
- rule register;
- prompt and schema versions;
- test and evaluation report;
- risk and escalation screen;
- tool-fit and ownership record;
- review instructions;
- user acceptance testing (UAT) record;
- runbook and fallback;
- change log;
- limitations and assumptions;
- five-minute portfolio demonstration;
- final Course 1 decision.

## One repository and artifact map

Windows setup creates the only capstone **repository**, a project folder whose
changes are tracked together by Git, at:

```text
Documents\AI-workflow-learning\operations-exception-assistant
```

Foundations remain separate in `Documents\controlled-ai-course-practice`.
Modules 1–9 write their evidence into the repository structure below. Each
module explains the artifact, demonstrates it, lets you recreate it, asks
Codex for a read-only check, and adds a Git checkpoint only after `PASS`.

| Module | Required capstone evidence | Repository location |
|---:|---|---|
| 1 | as-is map and observation; stakeholder/user map; baseline/value record | `evidence/module-01/` |
| 2 | opportunity brief; workflow opportunity scorecard; intended purpose and exclusions | `evidence/module-02/` |
| 3 | frozen data/rules record; data dictionary and quality check; expected issues | `evidence/module-03/` |
| 4 | runnable rule-first workflow; recreated synthetic input; 13- and 5-issue checks; input failures; retry; to-be map; architecture record | `src/course1_capstone/`, `evidence/module-04/` |
| 5 | bounded offline mock; source-linked review actions; learner candidate; all AI failure fallbacks | `evidence/module-05/` |
| 6 | non-overwriting Module 5 evidence copies; exact-revision decisions; approve/edit/reject/expire; local CSV/JSON; full executable acceptance | `evidence/module-06/` |
| 7 | data flow; risk/escalation screen; tool-fit and ownership record | `evidence/module-07/` |
| 8 | regression and value evaluation; `PROVISIONAL PRE-UAT` Course 1 recommendation | `evidence/module-08/` |
| 9 | executable user acceptance testing (UAT); defect/retest; adoption/training; runbook; `FINAL POST-UAT` decision; six-area assessment; ten oral answers; change log; portfolio demonstration | `evidence/module-09/` |

Module 9 also creates `CAPSTONE_INDEX.md` and `CHANGELOG.md` at the repository
root. `CAPSTONE_INDEX.md` links every required artifact and its module gate.
The final repository is the reproducible portfolio package; do not copy loose
module folders into a second project.

## Valid final decisions

### `ACCEPT FOR SYNTHETIC PORTFOLIO`

Evidence supports packaging the fictional, controlled demonstration as
portfolio evidence. It does not authorize a client test or production use.

### `REWORK`

The use case may be useful, but data, rules, usability, ownership, or controls
are not ready.

### `DO NOT CONTINUE`

Existing software, weak economics, unacceptable risk, insufficient ownership,
or no measurable AI benefit supports a safe closeout.

All three decisions can pass the course when supported honestly.

Course 2 teaches client discovery and assessment. Course 3 teaches preparation
and governance for a supervised pilot. No Course 1 decision permits real data,
an external action, or a synthetic-to-client transition.

## Prohibited claims

Do not claim that the capstone:

- is production ready;
- complies with the Algemene verordening gegevensbescherming (AVG), the Dutch
  name for the General Data Protection Regulation, or the European Union AI
  Act;
- is secure enough for client data;
- provides legal or quality-system conclusions;
- proves a guaranteed saving;
- replaces an electronic quality management system (eQMS), enterprise resource
  planning (ERP) system, customer relationship management (CRM) system,
  accountant, lawyer, privacy officer, security specialist, or process owner.
