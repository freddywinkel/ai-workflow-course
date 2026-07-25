# Week 7 — Meaningful Human Approval and Exact-Output Actions

## Outcome

You will implement approve, edit, reject, and timeout paths. A reviewer will see source evidence and uncertainty; approval will bind to the exact proposed-output hash; an edited output will require fresh approval; and the only action adapter will create a draft in a controlled sink.

## Beginner checkpoint

Before beginning, rerun the evergreen audit as required by the course. Then
revisit hash, idempotency, and human approval in
[AI and document workflows](../foundations/06_AI_AND_DOCUMENT_WORKFLOWS.md).
Explain why “the reviewer clicked Approve” is insufficient unless the record
identifies the reviewer, exact output hash, decision time, and validity.

Keep the action adapter as a local draft-only stub. Test changed-output,
expired, rejected, duplicate, and missing-approval paths before the happy path
is considered complete.

Safe AI-assistance request:

```text
Review my approval contract as a safety critic. Do not edit code. Trace approve,
edit, reject, expire, duplicate, and retry paths. Identify any path that could
execute without a valid approval for the exact current output hash, then
propose one failing test at a time.
```

## Concepts

- meaningful human review versus rubber stamping;
- proposed output and canonical byte representation;
- cryptographic binding;
- reviewer identity, role, and authority;
- approval expiry and revocation;
- maker/checker and two-person approval;
- optimistic/stale state;
- action idempotency;
- draft versus send;
- time-of-check/time-of-use;
- review usability and cognitive load.

## Official readings

Run [`../EVERGREEN_UPDATE_PROMPT.md`](../EVERGREEN_UPDATE_PROMPT.md) before beginning this week.

1. [n8n human-in-the-loop tool calls](https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools) — compare platform pause/approval features with the domain approval contract.
2. [Microsoft Power Automate approvals](https://learn.microsoft.com/en-us/power-automate/get-started-approvals) — comparison for approval UX and lifecycle.
3. [Dutch AP framework on meaningful human intervention](https://www.autoriteitpersoonsgegevens.nl/documenten/betekenisvolle-menselijke-tussenkomst) — check current status; consultation-stage or non-binding material must be labelled accurately.
4. [GDPR Article 22 in the consolidated regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A02016R0679-20160504) — understand why “a human clicked approve” is not automatically meaningful. The capstone avoids decisions with legal or similarly significant effects.
5. [OWASP Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html) — transaction binding and re-authentication principles.

The n8n pause is transport/orchestration. Your approval database record and exact-output verification remain the authorization authority.

## Guided build

### 1. Define canonical proposed bytes

Choose one action representation, for example UTF-8 JSON with:

- stable key ordering;
- LF line endings;
- Unicode NFC;
- explicit schema/version;
- no volatile timestamps inside the hashed content unless intended;
- exact memo text and intended draft recipient/subject fields.

Calculate:

```text
proposed_output_sha256 = SHA256(canonical_action_bytes)
```

Display this hash, shortened for humans but fully available, in the review screen.

### 2. Build the review package

The reviewer must see:

- case and trace IDs;
- document names, source hashes, and receipt time;
- proposed memo/action;
- each factual assertion linked to evidence;
- source excerpt and page/region/span;
- declared versus calculated values;
- missing/conflicting/unsupported items;
- model/parser/prompt/schema versions in an expandable technical panel;
- approval expiry;
- what action will occur and what will **not** occur;
- buttons for approve, edit, reject;
- manual fallback.

Do not show a confidence score without the observable reason and evidence. Do not preselect Approve.

### 3. Implement decisions

`ApprovalDecision` endpoint rules:

- reviewer is authenticated and authorised for tenant/run;
- current state is `pending_approval`;
- submitted output hash equals stored current proposal hash;
- decision time is before expiry;
- rejection requires an optional/required comment according to policy;
- approval record is immutable;
- audit event and state change occur transactionally.

For **edit**:

1. save reviewer’s edited candidate as a new proposed-output version;
2. render and hash it;
3. invalidate/leave inapplicable prior approvals;
4. rerun citation/prohibited-claim validation;
5. return to `pending_approval`;
6. require an explicit subsequent approval.

Never treat an edit action as approval.

### 4. Implement expiry and rejection

Use an injectable clock in tests.

- pending proposal expires after 48 hours;
- expired proposal cannot be acted on;
- resubmission creates a fresh proposal/version and expiry;
- rejected run performs no action;
- rejection cannot be changed by overwriting the row; create a new authorised lifecycle if rework is allowed.

### 5. Implement two-person approval

C018 requires two distinct reviewer IDs because net expenditure exceeds EUR 5,000:

- same reviewer twice does not count;
- both approvals bind to the same current output hash;
- edit after one approval invalidates the approval set;
- expiry of either required approval prevents action;
- reviewer separation is deterministic policy, not model output.

### 6. Build a draft-only action adapter

Interface:

```python
class ActionAdapter(Protocol):
    def create_draft(self, approved_action: ApprovedAction) -> ActionResult: ...
```

Default `LocalDraftOutboxAdapter` writes to a private table/folder. It cannot send, pay, delete, or modify source records.

Before action:

1. acquire run/action lock;
2. check kill switch;
3. reload current proposal bytes and hash;
4. validate approval count, identities, tenant, state, and expiry;
5. reserve unique idempotency key;
6. create draft;
7. record result and `completed` audit event atomically or reconcile safely.

An action retry uses the same idempotency key and returns the first successful result.

### 7. Orchestrate the pause

n8n:

1. receives `pending_approval`;
2. sends a localhost/test notification with review URL;
3. waits or polls by run ID;
4. routes `approved`, `rejected`, `expired`, or `failed_manual`;
5. requests action only for `approved`;
6. displays completion or manual recovery.

The URL alone is not authorization. Test stale links and another tenant.

### 8. Run adversarial lifecycle tests

- approve unchanged output → one draft;
- approve, then mutate one byte → zero drafts;
- edit → pending again → approve new hash → one draft;
- reject → zero drafts;
- timeout → zero drafts;
- duplicate action request → one draft;
- concurrent action requests → one draft;
- same reviewer twice on C018 → zero drafts;
- two distinct approvals on exact C018 hash → one draft;
- valid approval but kill switch on → zero drafts and visible safe state;
- audit write fails → no action.

## Capstone increment

The end-to-end path now exists through a controlled draft:

```text
source → parse → extract → validate → draft → review → exact-hash approval → local draft → audit
```

There is still no live mailbox permission and no send action.

## Required artifact

`artifacts/weekly/week-07/`:

- canonical-output specification;
- review UI or generated review package;
- ApprovalDecision and ActionExecution code/schema;
- approval and action threat notes;
- n8n approval-pause workflow export;
- local draft adapter;
- all lifecycle test results;
- screen recording or screenshots of approve/edit/reject/expire;
- human-review usability notes from one trial reviewer if available;
- weekly evidence record.

## Test gate

Pass only if:

- review shows exact proposed content, evidence, uncertainty, and intended action;
- one-byte mutation invalidates approval;
- editing never implies approval;
- rejection and expiry produce no action;
- duplicate/concurrent requests produce at most one draft;
- wrong tenant/reviewer/stale link fails;
- C018 needs two distinct approvals for the same hash;
- kill switch and audit failure prevent action;
- no adapter can send externally;
- every decision and attempt is traceable without storing unnecessary source text in logs.

## Common failures

- **Approval in n8n only:** persist and validate the domain approval contract.
- **Approving a database row that can change:** bind to canonical bytes and hash.
- **Edit-and-send button:** separate edit, revalidation, re-hash, and approval.
- **Reviewer sees summary but not evidence:** review cannot be meaningful without source access and uncertainty.
- **Idempotency generated per retry:** derive/reuse it for the logical action.
- **Two approval rows from same person:** enforce distinct identities.
- **Expiry checked at approval but not action:** re-check immediately before execution.

## Estimated time

| Activity | Time |
|---|---:|
| Live audit and readings | 1.25 h |
| Canonical output and review package | 1.75 h |
| Decision lifecycle | 2.0 h |
| Action/idempotency boundary | 1.75 h |
| n8n pause and lifecycle tests | 1.5 h |
| Evidence and usability review | 0.75 h |
| **Total** | **9.0 h** |
