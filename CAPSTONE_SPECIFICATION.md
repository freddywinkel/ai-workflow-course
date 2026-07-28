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
6. optionally creates a schema-constrained AI summary using only verified
   issue records;
7. verifies every AI issue reference;
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
`2026-07-26`.

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

If the scorecard supports stopping, document why. You may either select another
fictional low-risk process or carry the stopped decision through the remaining
modules as a documented closeout. A supported stop is evidence of judgment,
not a failed exercise.

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

The implementation may use Python plus an optional visual workflow tool, or an
equivalent documented method. Completion must not depend on a particular
vendor.

Required characteristics:

- environment-specific settings are configuration;
- secrets are not in code or **Git**, the version-control tool that records file
  changes;
- the deterministic checker runs without a model application programming
  interface (API);
- every run has a traceable run ID;
- every run ends in a named state;
- errors are visible;
- duplicate retries are safe;
- output folders are separated from source data;
- tests can run without paid API calls.

## Optional live AI lab

The live AI step is optional for course completion. If used:

- select a currently supported model through configuration;
- use a provider API that can return JavaScript Object Notation (JSON)
  Schema-constrained output;
- record the provider, model identifier, prompt version, date, latency, and
  cost estimate;
- send only synthetic verified issue records;
- detect refusal and invalid output;
- verify all issue IDs after generation;
- compare the live result with the offline fixture.

Using a flagship model is not a course requirement.

## Human-control acceptance

The reviewer must be able to see:

- why each item was flagged;
- the original synthetic row values needed to understand the issue;
- which text came from deterministic rules;
- which text was drafted by AI;
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
- expired review;
- `EXTERNAL_ACTIONS_ENABLED=false` safety control.

### Invariants

- no issue exists without a rule result;
- no AI factual claim exists without a verified issue ID or unsupported label;
- no external action occurs;
- one run key creates at most one local outbox item per approved revision;
- a changed draft cannot reuse an old approval;
- manual fallback produces a usable report;
- a failed run never appears successful.

## Evaluation

Report at least:

- expected issues detected;
- missed issues;
- false alarms;
- unsupported AI claims;
- correct issue references;
- refusal and failure handling;
- repeatability across identical runs;
- manual versus assisted handling time;
- observed cost for any live call;
- reviewer usability;
- limitations and unresolved risks.

Do not use a mandatory percentage-improvement threshold. Small synthetic timing
studies are not forecasts.

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
| 4 | rule-first implementation; tests; to-be map; architecture diagram | `evidence/module-04/` |
| 5 | bounded optional AI evidence; prompt/schema versions; offline fallback | `evidence/module-05/` |
| 6 | review package; approval lifecycle; local outbox and failure evidence | `evidence/module-06/` |
| 7 | data flow; risk/escalation screen; tool-fit and ownership record | `evidence/module-07/` |
| 8 | regression and value evaluation; final Course 1 decision record | `evidence/module-08/` |
| 9 | user acceptance testing (UAT); adoption/training; runbook; change log; portfolio demonstration | `evidence/module-09/` |

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
