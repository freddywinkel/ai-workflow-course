# Week 9 — Security, Failure Engineering, and Observability

## Outcome

You will threat-model and harden the complete workflow, including prompt-injection defence, tenant isolation, secrets, bounded retries, dead-letter/manual routes, alerts, traces, a kill switch, and a restoration drill. Declared dependency failures will produce visible safe outcomes.

## Beginner checkpoint

Revisit [PowerShell safety](../foundations/02_COMMAND_LINE_SURVIVAL.md),
[Git and secrets](../foundations/05_GIT_AND_SAFE_CHANGES.md), and the component
map in
[n8n, Docker, and databases](../foundations/08_N8N_DOCKER_AND_DATABASES.md).
Threat modelling begins with a drawing of assets, actors, entry points, and
trust boundaries; it does not begin by installing a security tool.

Run failure drills only against the synthetic local course environment. Before
any restore, deletion, credential rotation, or container/volume operation,
resolve the exact target and record the recovery method. Use the
[debugging record](../templates/debugging_record.md) for unexpected outcomes.

Safe AI-assistance request:

```text
Act as a threat-model tutor for this one data flow. Ask me to identify assets,
actors, entry points, and trust boundaries. Then list plausible threats and
testable controls. Do not run scanners, expose services, delete data, rotate
credentials, or change configuration.
```

## Concepts

- assets, actors, trust boundaries, threats, and controls;
- prompt injection and data/instruction separation;
- least privilege and tenant isolation;
- SSRF, unsafe file handling, and webhook abuse;
- secrets lifecycle;
- structured, redacted logs;
- trace, metric, alert, and audit distinctions;
- retry, circuit breaker, dead-letter/manual queue;
- kill switch and degraded/manual mode;
- backup versus restore;
- recovery-time and recovery-point objectives;
- incident evidence.
- operational/security incident versus AVG personal-data breach.

## Official readings

1. [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html).
2. [OWASP LLM01: Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).
3. [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html).
4. [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
5. [NCSC-NL basic principles for digital resilience](https://www.ncsc.nl/nieuws/ncsc-en-dtc-lanceren-gezamenlijke-basisprincipes-voor-digitale-weerbaarheid).
6. [n8n security audit](https://docs.n8n.io/hosting/securing/security-audit/).
7. [n8n error workflows](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully).
8. [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security) and [Storage access control](https://supabase.com/docs/guides/storage/security/access-control).
9. [AP: what to do after a data breach](https://autoriteitpersoonsgegevens.nl/themas/beveiliging/datalekken/datalek-dit-moet-u-doen).
10. [EDPB Guidelines 01/2021 on personal-data-breach examples](https://www.edpb.europa.eu/documents/guideline/guidelines-012021-on-examples-regarding-personal-data-breach-notification_en).

Use OWASP and NCSC as current security guidance, not as a certification checklist.

An operational incident is not automatically a personal-data breach. For real
personal data, the processor informs the controller without undue delay; the
controller assesses documentation, AP notification (where required, within 72
hours after awareness), and communication to affected people where high risk is
likely. A shorter internal target is a contractual/operational SLA, not the
statutory deadline. This course uses fictional data and never submits a real
regulator notification.

## Guided build

### 1. Create the threat model

Use [`../templates/threat_model.md`](../templates/threat_model.md). Cover assets:

- source documents;
- derived text/tables/embeddings;
- extraction and memo results;
- approval records;
- action credentials;
- API/provider keys;
- audit ledger;
- prompts, schemas, code, and gold answers.

Cover actors:

- authorised uploader/reviewer;
- mistaken or compromised user;
- malicious document author;
- cross-tenant user;
- dependency/provider;
- operator;
- unauthenticated network caller.

For each threat, record precondition, path, impact, preventive control, detective control, recovery, test case, and owner.

### 2. Defend against prompt injection

Layered controls:

- documents are always delimited and labelled untrusted;
- source content cannot supply tools, URLs, credentials, policy, or instructions;
- model receives an allowlisted chunk catalog;
- output is schema constrained;
- candidate evidence IDs are verified;
- arithmetic, state, authorization, and actions are deterministic;
- no model-call tool can send, delete, pay, or update;
- instruction-like text emits a finding;
- unsupported claims fail memo validation;
- human review shows the suspicious excerpt.

Run C012 and C013. Add mutations that place the benign injection string in filename, table cell, footer, and OCR image. Correct values and state must remain controlled.

### 3. Prove tenant isolation

Test through every layer:

- API route;
- database table and view;
- storage object and signed URL;
- derived text;
- retrieval query/vector index;
- evidence resolver;
- approval endpoint;
- action adapter;
- logs and exports.

Use the same C001 bytes for `tenant-demo-eu-001` and `tenant-demo-eu-002`. Deduplication is tenant-scoped. Tenant A must not learn whether tenant B has the same hash.

### 4. Harden secrets and network paths

- keep all service keys server-side;
- use scoped credentials per environment;
- rotate a test credential and prove recovery;
- redact `Authorization`, cookies, tokens, signed URLs, source text, and model input/output from general logs;
- allowlist outbound provider hosts where practical;
- reject arbitrary source URLs; accept uploaded bytes or approved object references;
- keep n8n/editor/API on localhost for the course;
- authenticate callbacks and prevent replay;
- scan Git history and n8n exports for secrets;
- record dependency hashes/lockfile.

### 5. Build the failure matrix

Inject:

- parser process crash;
- OCR model unavailable;
- database timeout;
- storage upload/download failure;
- model timeout, 429, 500, refusal, malformed output;
- approval callback replay;
- action adapter timeout after success;
- audit insert failure;
- corrupted derived text;
- retrieval no-result/wrong version;
- n8n restart during wait.

For each:

```text
failure | detection | attempts/backoff | terminal state | user message |
manual recovery | audit evidence | alert
```

Retries must be bounded and safe. Never resume with substitute evidence or guessed values.

### 6. Add observability

Structured event fields:

```text
timestamp, level, environment, trace_id, run_id, tenant pseudonym,
component, operation, state_from, state_to, reason_code,
attempt, latency_ms, version tuple, token counts, estimated cost
```

Separate:

- **audit:** governed business events;
- **logs:** diagnostic events with retention/redaction;
- **metrics:** counts/distributions;
- **alerts:** actionable conditions;
- **traces:** cross-component timing/causality.

Minimum metrics:

- runs by state/reason;
- parse/model/action latency;
- retry count;
- schema/semantic/evidence failure rate;
- manual-review rate;
- approval/rejection/expiry count;
- duplicate count;
- estimated model cost;
- deletion backlog.

Alert locally for audit-write failure, tenant-boundary denial anomaly, exhausted retries, action uncertainty, kill switch, and retention failure.

### 7. Implement kill switch and degraded mode

One server-side configuration prevents:

- new model calls;
- new action execution.

It still permits:

- health/status;
- viewing existing source/evidence;
- manual extraction/review;
- exporting a manual work packet;
- safe audit events;
- restoration/deletion operations.

Test activation during each state. It must not corrupt in-flight state or imply completion.

### 8. Perform a restoration drill

Back up:

- SQL schema/migrations and a test database snapshot;
- source and derived objects separately;
- n8n volume/workflow exports and encryption key procedure;
- prompts/schemas/code through Git;
- configuration names without secrets.

Restore to a clean local namespace:

1. restore database;
2. restore object storage;
3. import n8n workflow;
4. configure fresh credentials;
5. recompute source hashes;
6. reconstruct one run’s audit/state;
7. open its evidence;
8. keep kill switch on;
9. verify no action is replayed.

Record actual recovery time and gaps.

### 9. Run an incident and breach-decision tabletop

Scenario: a course API key appears in a workflow export, a synthetic memo is
briefly visible to the wrong synthetic tenant, and the model provider is down.

Execute:

```text
detect → stop outbound workflow → revoke/rotate → isolate → preserve evidence
→ assess confidentiality/integrity/availability → assess personal-data status
→ notify the internal owner/controller contact if relevant → recover → verify
→ record lessons
```

For this corpus, record `NO PERSONAL-DATA BREACH — NO AP REPORT` because the
records are fictional, while still documenting the security incident. Include
the hypothetical decision path for real data. Do not contact the AP.

## Capstone increment

The system can survive or safely stop for every declared outage. C012/C013 remain correct; cross-tenant paths are denied; one restored case retains source and evidence integrity; the kill switch preserves manual work.

## Required artifact

`artifacts/weekly/week-09/`:

- threat model;
- prompt-injection test matrix/results;
- tenant-isolation matrix/results;
- secrets/network checklist and scan results;
- failure-injection matrix/results;
- log schema, sample redacted trace, metrics/alert definitions;
- kill-switch tests;
- backup inventory and restoration report;
- incident timeline and breach-decision record;
- n8n security-audit output with findings triaged;
- weekly evidence record.

## Test gate

Pass only if:

- C012/C013 and placement mutations cannot change facts, instructions, approval, or action;
- tenant isolation holds at every listed layer;
- no secret or raw source content appears in Git, exports, general logs, or alert payloads;
- all declared failures reach visible named states/manual routes;
- retries are bounded and idempotent;
- uncertain action outcome never triggers a second action without reconciliation;
- kill switch blocks model/action but preserves manual access;
- database plus objects restore and hashes match;
- restoration does not replay an action;
- every tabletop event has a timestamp, owner, decision, and next step, and the
  fictional-data conclusion is not confused with a real breach notification;
- audit/log/metric/trace purposes are distinct.

## Common failures

- **Prompt-only defence:** enforce capability, schema, evidence, authorization, and action boundaries.
- **RLS tested only through service key:** service roles bypass controls; test user roles and views.
- **Logging entire model request:** minimise/redact and keep governed content separate.
- **Retry after uncertain action:** reconcile by idempotency key before another attempt.
- **Database backup called complete:** Storage objects need separate backup/restore.
- **Kill switch stops review too:** preserve degraded manual operation.
- **Security checklist with no test IDs:** map each control to an executable or tabletop test.
- **Calling every incident a reportable breach:** assess whether personal data
  is involved and document the controller’s risk/notification decision.

## Estimated time

| Activity | Time |
|---|---:|
| Security readings and threat model | 1.5 h |
| Injection and tenant tests | 2.0 h |
| Failure injection and recovery | 2.0 h |
| Observability and alerts | 1.25 h |
| Kill switch and restoration | 1.5 h |
| Incident tabletop, evidence, and triage | 1.25 h |
| **Total** | **9.5 h** |
