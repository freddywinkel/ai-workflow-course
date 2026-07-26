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
13. supports a kill switch and manual fallback;
14. produces an evaluation and a `PILOT`, `REWORK`, or `DO NOT PILOT`
    recommendation.

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
- explicit go, rework, or stop decision.

If the scorecard supports stopping, document why and select another fictional
low-risk process before continuing.

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

The implementation may use Python plus n8n, or an equivalent visual
orchestrator documented in a portability note.

Required characteristics:

- environment-specific settings are configuration;
- secrets are not in code or Git;
- the deterministic checker runs without a model API;
- every run has a traceable run ID;
- every run ends in a named state;
- errors are visible;
- duplicate retries are safe;
- output folders are separated from source data;
- tests can run without paid API calls.

## Optional live AI lab

The live AI step is optional for course completion. If used:

- select a currently supported model through configuration;
- use a provider API that can return JSON Schema-constrained output;
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
- kill switch.

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
- UAT record;
- runbook and fallback;
- change log;
- limitations and assumptions;
- five-minute portfolio demonstration;
- final pilot decision.

## Valid final decisions

### `PILOT`

Evidence supports a small, supervised, synthetic-to-client-test transition
after client IT, privacy, security, and process-owner review.

### `REWORK`

The use case may be useful, but data, rules, usability, ownership, or controls
are not ready.

### `DO NOT PILOT`

Existing software, weak economics, unacceptable risk, insufficient ownership,
or no measurable AI benefit makes the pilot unsuitable.

All three decisions can pass the course when supported honestly.

## Prohibited claims

Do not claim that the capstone:

- is production ready;
- complies with the AVG or AI Act;
- is secure enough for client data;
- provides legal or quality-system conclusions;
- proves a guaranteed saving;
- replaces an eQMS, ERP, CRM, accountant, lawyer, privacy officer, security
  specialist, or process owner.
