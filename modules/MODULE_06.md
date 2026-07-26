# Module 6 — Keep Humans in Control

## Outcome

Create a review and approval lifecycle in which a competent reviewer can
understand the evidence, edit or reject the draft, and approve only an exact
revision. Approval creates a local draft artifact and no external action.

## Beginner checkpoint

- deterministic issues remain authoritative;
- AI failure leaves a usable report;
- every summary issue reference is verified;
- you can explain the current named states;
- you understand that “human in the loop” is not meaningful without
  information, authority, and time.

## Concepts

### Meaningful review

A reviewer needs:

- evidence;
- domain competence;
- authority to decide;
- time to inspect;
- an actual reject or edit path;
- clarity about what approval will do.

### Exact revision

Approval applies to one exact draft. Hashing the canonical draft makes a later
change detectable.

### Time-of-check versus time-of-use

If content changes after review, the old approval must not authorize the new
content.

### Draft-only action

Course 1 writes only to `local_outbox/`. It never sends email, updates a record,
or triggers a payment.

## Official readings

- [European Commission AI literacy Q&A](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers)
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [Python `hashlib`](https://docs.python.org/3/library/hashlib.html)

## Guided build

### 1. Assemble a review package

Show:

- run ID and state;
- input hash and rule-set version;
- issue count by severity;
- each issue ID and rule explanation;
- the relevant synthetic source values;
- rule-based report;
- AI or offline summary with generator label;
- unsupported statements;
- known limitations;
- the exact draft revision;
- what approval will do.

Do not hide deterministic issues behind a polished AI paragraph.

### 2. Define reviewer decisions

Support:

- `approve`;
- `edit`;
- `reject`;
- `expire`.

Require an optional or mandatory reason according to your written design.
Never label a button “confirm compliance”.

### 3. Canonicalize and hash the draft

Before review:

1. serialize the draft using a documented stable method;
2. calculate SHA-256;
3. store revision number and hash;
4. show the reviewer the content represented by that hash.

Use `schemas/approval.schema.json` for the decision record.

### 4. Invalidate approval after edits

An edit:

- creates a new draft revision;
- creates a new hash;
- records an edit event;
- returns the run to `pending_approval`;
- cannot reuse the previous approval.

Test a one-character change.

### 5. Implement expiry

Use a short synthetic expiry interval for testing. An expired review cannot be
approved without creating a new review event.

### 6. Create the local draft outbox

After valid approval, write:

```text
local_outbox/<run_id>-r<revision>.md
local_outbox/<run_id>-r<revision>.json
```

The metadata includes approval ID, draft hash, and `delivery_status:
"draft_only"`.

Do not add SMTP, CRM, ERP, or filesystem paths outside the project.

### 7. Add a kill switch

When `KILL_SWITCH=true`:

- no AI call occurs;
- no approval can create a new outbox item;
- deterministic reporting remains available;
- the audit log records the blocked action.

### 8. Demonstrate manual fallback

Write a procedure for:

1. opening the rule report;
2. reviewing issues without the summary;
3. recording a manual decision;
4. communicating it through the normal human process outside the prototype;
5. reconciling later without duplicate effects.

### 9. Test the lifecycle

Test:

- approve exact revision;
- edit then attempt old approval;
- reject;
- expire;
- duplicate approval click;
- missing reviewer role;
- changed hash;
- kill switch;
- outbox write failure;
- AI summary absent.

## Consultant lens

Ask:

- Who currently owns the decision?
- What evidence do they need?
- What authority can never be delegated?
- How much review time is realistic?
- What happens during absence?
- Which exact action follows approval?
- Can the client reverse it?

Stop when:

- the “reviewer” is only clicking through;
- the person cannot understand the evidence;
- an approval authorizes changing content;
- the action is irreversible or consequential;
- no manual process exists.

Client-style deliverable:

- approval design, role matrix, review mock-up, lifecycle tests, and fallback.

## Capstone increment

The capstone now reaches:

```text
issues_ready → summary_ready → needs_review
→ pending_approval → approved_draft | rejected | expired
```

No state represents external delivery.

## Required artifact

- `evidence/module_06_approval_design.md`;
- review package example;
- decision records for all four outcomes;
- edit-invalidates-approval test;
- kill-switch test;
- local outbox example;
- manual fallback procedure.

## Test gate

- [ ] Reviewer sees source values, issues, generator, and limitations.
- [ ] Approve, edit, reject, and expire work.
- [ ] Approval is bound to exact revision and SHA-256.
- [ ] Any edit invalidates old approval.
- [ ] Duplicate approval creates no duplicate outbox item.
- [ ] Kill switch blocks AI and outbox creation.
- [ ] No external action exists.
- [ ] Manual fallback works without AI or n8n.

## Stop or rework

Stop if:

- approval is a decorative button;
- reviewer identity or role is absent;
- a mutable draft can be sent;
- the workflow requires external write-back to demonstrate value;
- failure makes manual completion impossible.

## Common failures

- hashing one representation but showing another;
- accepting approval after an edit;
- using “human in the loop” as a safety claim without usability evidence;
- putting unsupported AI prose above the issue evidence;
- retrying an outbox write without an idempotency key.

## Estimated time

10–14 hours.
