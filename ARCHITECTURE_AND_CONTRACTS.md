# Architecture and Contracts — Course 1 Capstone

This is an implementation reference, not an unguided exercise. Follow the
worked examples and recreation tasks in Modules 3–6 before using it.

Terms used below:

- **artificial intelligence (AI):** the optional generative step;
- **identifier (ID):** a value that uniquely names a fictional issue;
- **comma-separated values (CSV):** the plain-text table format used for the
  synthetic input.

## Design objective

Build the smallest system that proves controlled workflow reasoning:

- deterministic checks remain authoritative;
- the AI step is optional and replaceable;
- every AI factual statement refers to a verified issue ID;
- a human controls the draft outcome;
- no external system is updated;
- every run ends in a visible state;
- the workflow still provides value when AI is unavailable.

## Logical architecture

```text
practice_data/work_items.csv
  │
  ▼
input validation ──invalid──► failed_manual
  │ valid
  ▼
deterministic rules
  │
  ├── no issues ────────────► no_action_needed
  │
  ▼
verified issue register
  │
  ├── AI disabled/failed ───► rule_based_report
  │
  ▼
bounded AI summary
  │
  ├── unsupported claim ────► needs_review
  ▼
review package
  │
  ├── reject ───────────────► rejected
  ├── expire ───────────────► expired
  ├── edit ─────────────────► pending_approval (new revision)
  └── approve ──────────────► approved_draft
                                │
                                ▼
                         local draft outbox
```

## Trust boundaries

Treat all of these as untrusted until validated:

- CSV cells;
- filenames;
- descriptions containing instructions;
- AI output;
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
| AI adapter | Summarize verified issues into a schema | Finding authoritative exceptions |
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
  "issue_id": "ISS-001",
  "work_item_id": "WI-0002",
  "rule_code": "R007",
  "severity": "medium",
  "field": "owner_role",
  "observed_value": "",
  "message": "Active work requires an owner role."
}
```

Issue IDs must be stable for identical input, configuration, and evaluation
date.

### AI summary

The summary schema lives in `schemas/summary.schema.json`.

It must contain:

- run ID;
- prompt version;
- model configuration identifier or `offline-fixture`;
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
- reviewer identifier suitable for synthetic use;
- decision: `approve`, `edit`, `reject`, or `expire`;
- exact draft revision and content hash;
- timestamp;
- optional reason.

Editing creates a new draft revision and invalidates prior approval.

### Audit event

The audit-event schema lives in `schemas/audit_event.schema.json`.

Events include:

- input accepted or rejected;
- rules completed;
- AI requested, refused, failed, or completed;
- unsupported claim detected;
- review opened;
- draft edited;
- approved, rejected, or expired;
- local outbox entry created;
- retry deduplicated;
- `EXTERNAL_ACTIONS_ENABLED=false` safety control used.

## Named states

Course 1 uses a deliberately small state machine:

```text
received
validated
issues_ready
summary_ready
needs_review
pending_approval
approved_draft
rejected
expired
no_action_needed
failed_manual
```

Rules:

- only validated input reaches the rule engine;
- only verified issues reach the AI adapter;
- no AI output bypasses summary verification;
- only a reviewed draft can become `approved_draft`;
- approval is bound to an exact draft revision and hash;
- no course state represents “sent”, “paid”, or “updated externally”;
- retries must not create duplicate outbox entries;
- unexpected errors end in `failed_manual`, never silent success.

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

The default course run uses an offline fixture. A live model call is an
optional lab.

When enabled:

- the model identifier comes from configuration;
- the API key comes from an environment variable;
- only verified issue records are provided;
- raw employer or client data is forbidden;
- structured output is required;
- refusal, timeout, malformed output, and unsupported references are explicit
  failure classes;
- the workflow falls back to the rule-based report.

Do not let the AI step:

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
- AI mode and configured model identifier.

Reprocessing the same key must reuse or safely replace the same logical run. It
must not duplicate audit or outbox effects.

## Minimum failure matrix

| Failure | Required behaviour |
|---|---|
| Missing input file | `failed_manual`, clear message |
| Invalid CSV header | reject before rules |
| Malformed date | issue or input failure according to written contract |
| Duplicate retry | no duplicate outbox record |
| AI timeout | rule-based report remains available |
| AI refusal | record refusal, continue without AI |
| Unknown issue reference | reject summary and send to review |
| Draft edited after approval | approval invalidated |
| Reviewer unavailable | item remains pending or expires |
| Safe-stop condition active | skip AI and any outbox creation |

## Course 1 deployment boundary

The capstone runs privately with synthetic files. It is not:

- a production service;
- multi-tenant;
- connected to client systems;
- approved for real personal data;
- a legal compliance tool;
- a Veeva or eQMS integration;
- a medical device.

Those capabilities require later courses, client controls, and specialist
review.
