# Foundation 9 — Workflow Tools and Data Stores

## Outcome

You can explain the role of an orchestrator, code component, connector, and data
store; compare tool choices using business ownership and risk; and sketch the
smallest maintainable architecture for a controlled SME workflow.

## A workflow is not its drawing tool

A workflow is the connected work that moves one unit from a trigger to a
declared completion or exception state. A product such as n8n, Power Automate,
or another orchestrator may implement parts of it, but the business process also
includes people, rules, evidence, queues, decisions, and fallback.

Tool names will change. Keep these assets portable:

- as-is and proposed process maps;
- intended purpose and exclusions;
- data dictionary;
- rule register;
- input/output schemas;
- acceptance and UAT cases;
- decision and audit requirements;
- runbook, fallback, and ownership;
- exportable configuration and version records.

## Tool categories

### Spreadsheet and manual checklist

Useful for early discovery, a manual baseline, small volumes, and transparent
rule experiments.

Limits include concurrent editing, access control, hidden formulas, weak state
management, and difficult audit at scale. A spreadsheet can be an appropriate
pilot tool without being the final system.

### Built-in platform automation

Many business suites provide forms, lists, approvals, rules, and connectors.
Using an organisation’s existing platform may reduce new accounts and handover
work.

Check licence, environment administration, data region, identity, connector
permissions, exportability, monitoring, and who can maintain it after handover.

### Visual workflow orchestrator

An orchestrator such as n8n or a comparable low-code tool runs connected steps:

- a **trigger** starts a run;
- a **node** or step performs work;
- a **connector** communicates with another system;
- a branch routes work based on a declared result;
- a queue or wait state holds unresolved work.

Visual does not mean code-free. Expressions, credentials, permissions, retry
settings, and branches are software behaviour. Export and test configuration
instead of relying on remembered dashboard clicks.

### Code or API service

Small code components are useful for exact validation, calculations, schemas,
and rules that are awkward or unsafe inside visual expressions.

FastAPI is one Python framework that can expose tested functions through a local
API. It is an option, not a requirement. Code adds maintenance responsibility,
so use it when its testability or control is worth that cost.

### Data store

Files, lists, spreadsheets, databases, and object storage serve different
purposes:

- a file may preserve one immutable input snapshot;
- a list may hold simple shared work state;
- a relational database stores structured rows, relationships, and constraints;
- object storage holds larger files;
- an audit ledger records important events.

Do not select a database because it sounds professional. Select the smallest
store that preserves required integrity, access, history, scale, and recovery.

## Separate four kinds of data

1. **Source input** — the received snapshot or reference.
2. **Workflow state** — current status, owner, timestamps, and reason code.
3. **Derived artifact** — issue record, draft, calculation, or summary.
4. **Audit event** — who or what did what, when, to which version, and with what
   result.

Operational logs help diagnose software. They are not automatically an
authoritative audit record and should not contain full sensitive inputs.

Keep source data immutable where evidence matters. Corrections become a new
version or a recorded source-system change, not a silent overwrite.

## The minimum viable architecture

For the fictional work-item exercise, a sufficient architecture can be:

```text
untouched CSV snapshot
    ↓ deliberate import
deterministic rule checker
    ↓
structured issue records
    ↓ optional bounded AI draft
human review: accept / edit / reject / escalate
    ↓
summary and append-only audit event
```

This may begin as a spreadsheet plus a small script. Add an orchestrator,
database, container, or external model only when a named requirement justifies
it.

## When Docker is useful

A Docker **image** packages a filesystem and startup definition. A
**container** is a running instance. A **volume** preserves selected data when
a container is replaced. Docker Compose describes related services in YAML.

Docker can improve repeatability for a local lab, but it does not create:

- a backup;
- secure configuration;
- user access control;
- correct workflow rules;
- operational ownership.

Never expose a local course service to the public internet merely to make a
demo accessible. Recreating a container is not a restoration test.

## Tool-fit questions

Before selecting a tool, answer:

| Area | Question |
|---|---|
| Process fit | Does it support the required states, exceptions, and approval? |
| Existing environment | Can the SME use a platform it already owns and administers? |
| Data control | Where do input, logs, backups, support data, and AI inference go? |
| Identity and access | Can least-privileged roles be implemented and reviewed? |
| Evidence | Can decisions, versions, errors, and manual actions be traced? |
| Reliability | How are timeouts, duplicates, partial writes, and outages handled? |
| Ownership | Who operates it, pays for it, changes it, and receives alerts? |
| Portability | Can configuration, schemas, and data be exported in usable formats? |
| Cost | What are licence, usage, implementation, support, and exit costs? |
| Capability | Can the future owner understand and maintain it? |

A tool is a poor fit if only the consultant can operate it.

## Connectors and permissions

A connector uses credentials to reach another system. Treat it as a trust
boundary.

For every connector, record:

- system and purpose;
- permitted read/write operations;
- identity and least-privileged role;
- data transferred;
- region and vendor involvement;
- timeout, retry, duplicate, and rate-limit behaviour;
- revocation and credential rotation;
- test environment and owner.

Start with read-only imports. Do not connect this course to employer or customer
systems. External write-back belongs to a later approved pilot with exact
authority and reconciliation.

## Reproducible changes and handover

Dashboard changes disappear into memory unless exported or documented.

Preserve:

- workflow export with credentials removed;
- code, schemas, and tests in Git;
- migrations or list definitions;
- configuration names, never secret values;
- tool and model versions;
- setup and rollback steps;
- alert and exception owners;
- backup and restoration evidence;
- licence and recurring-cost owner.

Another competent person should be able to reproduce the synthetic
demonstration and safely stop it without the original builder.

## Practice

Draw two architectures for the fictional work-item workflow:

1. spreadsheet plus manual review;
2. orchestrator plus a tested rule component and structured store.

For each, identify:

- trigger and completion condition;
- source input and system of record;
- exact-rule location;
- optional AI boundary;
- human decision;
- exception queue;
- audit record;
- manual fallback;
- owner and recurring cost.

Then choose the simpler option unless the second architecture satisfies a
requirement the first cannot. Record that requirement, not a preference for a
brand.

## Chapter check

You pass when you can explain:

- workflow versus orchestrator;
- trigger, node, connector, API, and data store;
- source input, workflow state, derived artifact, log, and audit event;
- when a spreadsheet is enough and when it is not;
- why a visual workflow still needs tests and ownership;
- why Docker is packaging rather than a backup or security control;
- least privilege and read-only-first integration;
- why maintainability and handover are part of tool selection.
