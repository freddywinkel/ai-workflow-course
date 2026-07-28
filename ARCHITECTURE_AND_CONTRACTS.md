# Architecture and Contracts — Course 1 Capstone

This is an implementation reference, not an unguided exercise. Follow the
worked examples and recreation tasks in Modules 3–6 before using it.

Terms used below:

- **artificial intelligence (AI):** the generative capability represented in
  Course 1 by an offline mock only;
- **identifier (ID):** a value that uniquely names a fictional issue;
- **comma-separated values (CSV):** the plain-text table format used for the
  synthetic input.

## Design objective

Build the smallest system that proves controlled workflow reasoning:

- deterministic checks remain authoritative;
- the offline-mock language step is optional and replaceable;
- every generated factual statement refers to a verified issue ID;
- a human controls the draft outcome;
- no external system is updated;
- every run keeps a visible last valid workflow state, and every stopped command
  records a visible attempt outcome;
- the workflow still provides value when AI is unavailable.

## Logical architecture

```text
practice_data/work_items.csv
  │
  ▼
input validation ──invalid──► safe stop + failed_manual attempt evidence
  │ valid
  ▼
deterministic rules
  │
  ├── no issues ────────────► no_action_needed
  │
  ▼
verified issue register
  │
  ├── mock disabled/failed ─► rule_based_report
  │
  ▼
bounded offline-mock summary
  │
  ├── disabled/failed/unsupported ─► deterministic fallback
  ▼
review package / needs_review
  │
  ├── reject ───────────────► rejected
  ├── expire ───────────────► expired
  ├── edit ─────────────────► changes_requested
  │                              │ revised draft
  │                              └──────────────► needs_review
  └── approve ──────────────► approved_for_local_export
                                │
                                ▼
                         local CSV/JSON outbox
                                │
                                ▼
                         approved_draft
```

## Trust boundaries

Treat all of these as untrusted until validated:

- CSV cells;
- filenames;
- descriptions containing instructions;
- offline-mock output;
- imported configuration;
- reviewer input;
- retry messages;
- timestamps supplied by another system.

The supplied synthetic data is safe to use, but it intentionally contains
malformed and adversarial examples.

## Course 1 components

| Component | Responsibility | Not responsible for |
|---|---|---|
| CSV loader | Read exact source rows and preserve row IDs | Correcting business meaning |
| Validator | Types, required fields, allowed values | Guessing missing values |
| Rule engine | Produce verified issue records | Writing persuasive prose |
| Orchestrator | Move work through named states | Becoming the source of truth |
| Offline mock adapter | Simulate a bounded summary of verified issues without a network call | Finding authoritative exceptions or calling a live provider |
| Summary verifier | Check issue references and allowed claims | Deciding business action |
| Review package | Show source row, issue, explanation, limitations | Hiding uncertainty |
| Approval service | Record approve/edit/reject/expire | Sending externally |
| Local outbox | Store approved draft artifact | Emailing or updating a client system |
| Audit log | Record material events | Replacing security monitoring |

## Core records

### Work item

The work-item schema lives in `schemas/work_item.schema.json`. The supplied CSV
contains:

- stable `work_item_id`;
- unique `source_reference`;
- title and non-personal `owner_role`;
- status and priority;
- received, due, and completed dates;
- optional amount and currency;
- operational category.

Never silently invent a required value.

### Verified issue

The issue schema lives in `schemas/issue.schema.json`.

```json
{
  "issue_id": "WI-0002|R007|owner_role",
  "work_item_id": "WI-0002",
  "source_reference": "REF-1002",
  "source_row": 3,
  "field": "owner_role",
  "raw_value": "",
  "rule_code": "R007",
  "severity": "medium",
  "message": "Active work requires an owner role.",
  "assessment_date": "2026-07-26"
}
```

The issue ID is the exact
`work_item_id|rule_code|field` occurrence identity. It and the remaining fields
must validate against the closed issue schema.

### Bounded summary

The summary schema lives in `schemas/summary.schema.json`.

It must contain:

- run ID;
- prompt version;
- generator value `offline-mock` or `deterministic-fallback`;
- grouped findings;
- referenced issue IDs;
- unsupported or uncertain statements;
- a plain limitation that a human must review the result.

Schema-valid output is not enough. Every referenced issue ID must exist in the
verified issue register, and every factual sentence must be supportable from
those issues.

### Approval decision

The approval schema lives in `schemas/approval.schema.json`.

A decision records:

- decision ID;
- run ID;
- reviewer role suitable for synthetic use;
- decision: `approve`, `edit`, `reject`, or `expire`;
- exact draft revision and content hash;
- decision and expiry timestamps;
- confirmation that the source-linked evidence was reviewed;
- a reason.

Editing creates a new draft revision and invalidates prior approval.

### Audit event

The audit-event schema lives in `schemas/audit_event.schema.json`.

Events include:

- input accepted or rejected;
- rules completed;
- offline mock requested, refused, failed, or completed;
- unsupported claim detected;
- review opened;
- draft edited;
- approved, rejected, or expired;
- local outbox entry created;
- retry deduplicated;
- `EXTERNAL_ACTIONS_ENABLED=false` safety control used.

## Named workflow states and command-attempt outcomes

Course 1 uses a deliberately small persistent workflow state machine:

```text
received
validated
issues_ready
summary_ready
needs_review
changes_requested
approved_for_local_export
approved_draft
rejected
expired
no_action_needed
```

`failed_manual` is different: it is the named outcome of a command attempt that
stopped safely. It is written to `failures\safe-stop-<reason>.json` and to the
audit trail. It does **not** overwrite the run's last valid `current_state`.
Overwriting that state after a malformed candidate, edited draft, or tampered
control would hide what had previously been valid.

The `status` command therefore reports both:

- `current_state`: the last valid persistent workflow state; and
- `latest_attempt_state`: the state of the newest audit event, which is
  `failed_manual` after a safe stop.

For a failure before a run exists, the workspace failure record is the named
attempt outcome and there is no run state to overwrite. Recovery is explicit:
stop, read the failure record, preserve it, correct the separate input or
candidate (or start a fresh isolated run), and retest. Never delete or relabel
the failed attempt as a success.

Rules:

- only validated input reaches the rule engine;
- only verified issues reach the offline mock adapter;
- no mock output bypasses summary verification;
- only a reviewed exact draft can become `approved_for_local_export`;
- only a valid, unexpired approval can create the local outbox and become
  `approved_draft`;
- approval is bound to an exact draft revision and hash;
- no course state represents “sent”, “paid”, or “updated externally”;
- retries must not create duplicate outbox entries;
- unexpected command attempts record `failed_manual`, never silent success,
  while the last valid workflow state remains visible.

## Deterministic rules

Required rules include:

- R001 required field;
- R002 allowed status;
- R003 allowed priority;
- R004 ISO date format;
- R005 due date not before received date;
- R006 status/completion-date relationship;
- R007 owner role for active or completed work;
- R008 non-negative amount;
- R009 EUR currency when amount is populated;
- R010 unique source reference;
- R011 overdue open work using the fixed date `2026-07-26`.

The exact expected issues are supplied in
`practice_data/expected_issues.csv`. It contains 13 expected issues for the 15
supplied rows. The learner may add separate test rules but may not change the
expected file merely to make failing code pass.

## AI boundary

Course 1 uses only the offline mock and deterministic fallback. Its timeout,
refusal, malformed-output, and unknown-reference modes are local simulations.
The Course 1 runner has no network client, provider key, paid call, or live
model option.

A live provider belongs to a later course and requires a separate decision on
value, provider fit, privacy, security, cost, monitoring, and teardown. It is
not an optional Course 1 lab.

Do not let either the Course 1 mock or a later live language step:

- create or remove issue records;
- change severity without a deterministic rule;
- determine compliance;
- choose a person, supplier, payment, or binding action;
- call external tools;
- update the source register.

## Idempotency and reproducibility

Derive a run key from:

- input file hash;
- rule-set version;
- fixed evaluation date;
- prompt version;
- offline generator mode and mock/fallback version.

Reprocessing the same key must reuse or safely replace the same logical run. It
must not duplicate audit or outbox effects.

## Minimum failure matrix

| Failure | Required behaviour |
|---|---|
| Missing input file | `failed_manual` attempt evidence and clear message; no run is invented |
| Invalid CSV header | reject before rules |
| Malformed date | issue or input failure according to written contract |
| Duplicate retry | no duplicate outbox record |
| Simulated AI timeout | rule-based report remains available |
| Simulated AI refusal | record refusal, continue without AI |
| Simulated unknown issue reference | reject candidate; preserve last valid workflow state and issue register |
| Draft edited after approval | block export; preserve approval evidence plus a named failed attempt |
| Reviewer unavailable | item remains pending or expires |
| Safe-stop condition active | skip AI and any outbox creation |

## Course 1 deployment boundary

The capstone runs privately with synthetic files. It is not:

- a production service;
- multi-tenant;
- connected to client systems;
- approved for real personal data;
- a legal compliance tool;
- a Veeva or electronic quality management system (eQMS) integration;
- a medical device.

Those capabilities require later courses, client controls, and specialist
review.
