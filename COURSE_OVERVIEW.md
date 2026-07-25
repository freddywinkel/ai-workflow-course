# Course Overview

## Learning contract

This is a build course, not a reading course. Each week ends with a stored artifact and an executable gate. You may use AI as a coding tutor, but you must be able to explain, reproduce, test, and safely stop every component it helps create.

The course assumes **no prior coding or CLI knowledge**. If terms such as
PowerShell, repository, JSON, function, API, container, or database are new,
complete [`foundations/README.md`](foundations/README.md) before setup. Use
[`foundations/07_SAFE_VIBE_CODING.md`](foundations/07_SAFE_VIBE_CODING.md) for
every AI-assisted change and
[`templates/ai_assistance_log.md`](templates/ai_assistance_log.md) to record
what you understood and verified.

Your weekly rhythm is:

1. **Orient (45–60 min):** read the outcome, gate, and official sources.
2. **Learn (90–120 min):** reproduce small examples and keep short notes.
3. **Build (4–5 h):** complete the guided build and capstone increment.
4. **Attack (60–90 min):** run negative, failure, and adversarial cases.
5. **Prove (45–60 min):** save the artifact, commands, results, and reflection.

Do not compensate for a failed gate by writing that something “should work.” Fix it, record an explicit safe failure, or stop and carry the failed gate into the next session.

## Prerequisites

There are no assumed technical prerequisites. The former prerequisites are now
taught in the beginner foundation sequence. Before Week 1, pass its
[`foundation gate`](foundations/README.md#foundation-gate), which covers:

- navigating folders and using a few safe PowerShell commands;
- editing Markdown, JSON, YAML, and `.env.example` files;
- reading very small Python functions;
- using Git status and diff before a commit;
- explaining basic API, AI, Docker, n8n, and database concepts.

You do not need prior n8n, API, OCR, database, or LLM-development experience.
Week 2 still teaches HTTP and JSON in the project context before any model call.
The foundations teach the vocabulary first so Week 2 is not your first exposure.

If a foundation check is not yet true, repeat that short lesson. Do not ask an
AI assistant to conceal the gap by generating the whole project.

## What “production-style” means here

The endpoint is not a public production deployment. “Production-style” means the private demo exhibits the controls a real implementation would need:

- explicit purpose and exclusions;
- reproducible environment and version records;
- immutable inputs and traceable transformations;
- schema-defined interfaces;
- safe state transitions;
- least-privilege storage and actions;
- deterministic validation around probabilistic output;
- meaningful human review;
- idempotency and retry safety;
- failure visibility and manual recovery;
- a frozen evaluation set;
- retention and deletion behaviour;
- documented limits and handover instructions.

## Repository you will create

Create a separate Git repository named `supplier-review-system` during Week 1:

```text
supplier-review-system/
├── README.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── docker-compose.yml
├── config/
│   ├── models.example.yaml
│   └── retention.example.yaml
├── docs/
│   ├── intended-purpose.md
│   ├── architecture.md
│   ├── data-flow.md
│   ├── threat-model.md
│   ├── runbook.md
│   └── evidence/
├── src/
│   └── supplier_review/
│       ├── api/
│       ├── domain/
│       ├── parsing/
│       ├── extraction/
│       ├── drafting/
│       ├── approvals/
│       ├── audit/
│       └── settings.py
├── sql/
├── n8n/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── regression/
│   └── fixtures/
├── scripts/
└── artifacts/
    ├── weekly/
    └── release/
```

The supplied course corpus remains read-only. Copy a deliberate working subset into your project only when a lab instructs you to do so.

## Environments and data boundary

Use three logical environments even if they run on one computer:

| Environment | Purpose | Data | External action |
|---|---|---|---|
| `dev` | active coding | synthetic, disposable | disabled |
| `test` | frozen regression | supplied synthetic corpus | stub only |
| `demo` | acceptance demonstration | frozen synthetic corpus | draft-only sink |

Never put the OpenAI key, Supabase service key, database password, or connector credential into Git, n8n workflow exports, screenshots, logs, or course artifacts. Use environment variables and the platform credential store.

## Definition of done for a weekly artifact

An artifact is done only when it has:

- a date and author/reviewer field;
- an artifact or version ID;
- links to the relevant source, test, or decision record;
- the exact command or procedure used to verify it;
- observed results, not expected results;
- known limitations and a next action if anything remains open;
- no secrets or raw sensitive content.

Use [`templates/weekly_evidence_record.md`](templates/weekly_evidence_record.md) for every gate.

## Stop conditions

Stop the workflow and route to `failed_manual` or `needs_review` when:

- a source cannot be hashed or privately stored;
- file type, size, or malware policy fails;
- the parser cannot produce stable source locators;
- OCR quality is below your declared threshold;
- structured output is absent, refused, truncated, or schema-invalid;
- a required commercial field is missing or conflicts across sources;
- a cited text hash no longer matches the source;
- the draft contains an unsupported factual assertion;
- the proposed output changed after approval;
- approval expired, is missing, or belongs to another tenant/run;
- an idempotency key already completed with different parameters;
- tenant identity or authorization is ambiguous;
- an external dependency fails beyond the retry policy;
- logging or audit persistence fails;
- the kill switch is active.

These are safe outcomes, not implementation embarrassments.

## How assessment works

Weekly gates are pass/fail prerequisites. The final rubric is evidence-weighted:

- source integrity and provenance: 20%;
- extraction and deterministic validation: 15%;
- grounded drafting and citation integrity: 15%;
- approval and action safety: 15%;
- privacy, security, and failure handling: 15%;
- evaluation quality: 10%;
- reproducibility, runbook, and demonstration: 10%.

See [`ASSESSMENT_AND_RUBRIC.md`](ASSESSMENT_AND_RUBRIC.md) for exact evidence requirements.

## When you may simplify

You may omit vector retrieval when the policy is short enough for deterministic section lookup. You may use local PostgreSQL before connecting Supabase. You may simulate an email connector with a draft outbox table. You may use one OCR engine. You may keep observability local.

You may not simplify away:

- immutable source hashes;
- source/derived separation;
- evidence locators;
- schema and semantic validation;
- approval tied to exact output hash;
- idempotency;
- named failure states;
- a gold dataset;
- manual fallback;
- deletion and restoration tests.

## AI-literacy goal

At the end you should be able to explain, without vendor language:

- what the model does and does not determine;
- where hallucination, extraction, OCR, and automation errors arise;
- why Structured Outputs constrain shape rather than truth;
- how evidence is bound to source content;
- how a human review can be meaningful rather than ceremonial;
- which actions remain deterministic;
- what data vendors receive and retain under the selected configuration;
- how to pause, inspect, recover, delete, and retest the system.
