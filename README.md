# AI Workflow & Document Systems — 12-Week Builder Course

Version: 1.2.2
Verified through: 2026-07-25  
Language: English, with Dutch/EU legal terms where useful  
Workload: 8–10 hours per week  
Endpoint: a private, reproducible technical demonstration using synthetic data

Course reader: [open the installable PWA](https://freddywinkel.github.io/ai-workflow-course/)  
Repository: [freddywinkel/ai-workflow-course](https://github.com/freddywinkel/ai-workflow-course)

## What you will prove

By the end of this course, you will have built and demonstrated one bounded workflow:

> Fictional supplier quotations and terms enter a controlled system. The system preserves and hashes the originals, parses them, extracts commercial facts with evidence, performs deterministic checks, retrieves an internal purchasing policy, and drafts a source-cited review memo. A human can approve, edit, reject, or let the proposal expire. The system never recommends a supplier and never performs a final action without approval for the exact output being acted on.

The course teaches the technical capability behind an AI workflow and document-systems studio. It deliberately does **not** teach sales, positioning, pricing, client acquisition, contracts, or studio operations.

## Safety boundary

Use only the supplied synthetic corpus while taking this course. Do not introduce real client or personal data.

Excluded throughout:

- health data or other special-category personal data;
- BSNs or national identifiers;
- children’s data;
- employment, credit, insurance, housing, education-admission, policing, migration, or similar consequential decisions;
- medical diagnosis, treatment, triage, or medical-device functionality;
- automatic supplier selection, payments, binding messages, deletions, or record changes.

The capstone is decision support for a human reviewer, not automated decision-making. Legal material is practical engineering guidance, not legal advice.

## Canonical learning path

```text
intake
  → immutable source + SHA-256
  → parsing/OCR
  → evidence-aware extraction
  → deterministic validation
  → grounded draft
  → human review
  → approved action
  → audit event
  → evaluation feedback
```

The required path uses:

- n8n for orchestration, retries, connectors, and approval pauses;
- Python, FastAPI, Pydantic, Docling, and pytest for parsing, contracts, validation, hashes, and tests;
- OpenAI Responses API with Structured Outputs, with model IDs supplied through configuration;
- Supabase in a European region for private object storage, PostgreSQL state, audit records, and optional pgvector retrieval;
- Git plus an append-only application audit ledger.

Microsoft 365, Google Workspace, Make, Mistral OCR, Azure Document Intelligence, and Ollama are comparison or portability labs. They are not parallel mandatory tracks. Promptfoo and Langfuse are optional extensions after the local regression harness works.

## Start here

If you have no coding or command-line experience, that is now an explicitly
supported starting point. Do not begin with the Windows installation commands.
Start with the short [`Beginner Foundations`](foundations/README.md), keep the
[`plain-language glossary`](foundations/GLOSSARY.md) open, and pass the
foundation gate first.

Then:

1. Run the live-audit prompt in [`EVERGREEN_UPDATE_PROMPT.md`](EVERGREEN_UPDATE_PROMPT.md). Do not start if it returns `UNVERIFIED`.
2. Read [`COURSE_OVERVIEW.md`](COURSE_OVERVIEW.md), including the proof rules and stop conditions.
3. Complete [`SETUP_WINDOWS.md`](SETUP_WINDOWS.md) and its smoke tests.
4. Read the contracts and state machine in [`ARCHITECTURE_AND_CONTRACTS.md`](ARCHITECTURE_AND_CONTRACTS.md).
5. Work through Weeks 1–12 in order. Do not continue through a failed weekly gate.
6. Freeze the corpus and run the acceptance process in [`CAPSTONE_SPECIFICATION.md`](CAPSTONE_SPECIFICATION.md).

The 8–10 hour estimate describes the formal project work. A literal beginner
should expect additional learning time, especially in Weeks 2–5, and may split
one course week across two calendar weeks. Understanding and passing the gate
matters more than preserving the calendar.

## Course map

| Stage | Focus | Required proof |
|---|---|---|
| [Foundations](foundations/README.md) | Files, PowerShell, Python, APIs, Git, AI, n8n, Docker, and databases | Foundation gate explained in your own words |
| [1](weeks/WEEK_01.md) | Process and state design | Bounded intended purpose, as-is map, exclusions, allocation, baseline |
| [2](weeks/WEEK_02.md) | APIs and non-AI orchestration | Reliable intake-to-log workflow with branching and retries |
| [3](weeks/WEEK_03.md) | Source integrity and storage | Immutable source, hash, manifest, private storage, state |
| [4](weeks/WEEK_04.md) | Parsing and OCR | PDF/DOCX/table/scan provenance plus safe corrupt-file handling |
| [5](weeks/WEEK_05.md) | LLM extraction | Schema-constrained extraction with refusal/null/validation handling |
| [6](weeks/WEEK_06.md) | Retrieval and grounded drafting | Evidence ledger and citation-complete review memo |
| [7](weeks/WEEK_07.md) | Meaningful human approval | Exact-output approval, expiry, rejection, idempotency |
| [8](weeks/WEEK_08.md) | AVG and AI safety engineering | Data-flow, DPIA screen, vendor and transparency records |
| [9](weeks/WEEK_09.md) | Security, failures, observability | Safe fallbacks, isolation, traces, restoration drill |
| [10](weeks/WEEK_10.md) | Evaluation-driven development | Frozen JSONL gold set and vendor-neutral regression runner |
| [11](weeks/WEEK_11.md) | Integration and portability | One connector, provider comparison, timing study, hardening |
| [12](weeks/WEEK_12.md) | Acceptance and handover | Frozen private release and clean-start evidence-backed demo |

## Key package contents

- [`SOFTWARE_MATRIX.md`](SOFTWARE_MATRIX.md): required and comparison tools, selection rules, costs, and replacement boundaries.
- [`foundations/`](foundations/README.md): beginner lessons, CLI survival guide,
  safe vibe-coding workflow, and glossary.
- [`BEGINNER_READINESS_CHECK.md`](BEGINNER_READINESS_CHECK.md): explicit audit
  of beginner assumptions, remaining realities, and the self-check gate.
- [`SOURCE_REGISTER.md`](SOURCE_REGISTER.md): dated, official-source register with applicability and volatility.
- [`CAPSTONE_SPECIFICATION.md`](CAPSTONE_SPECIFICATION.md): scope, frozen corpus, metrics, and acceptance tests.
- [`ASSESSMENT_AND_RUBRIC.md`](ASSESSMENT_AND_RUBRIC.md): weekly gates and final scoring.
- [`templates/`](templates/README.md): fillable engineering worksheets and operational checklists.
- [`schemas/`](schemas/README.md): portable JSON Schemas for the system contracts and gold cases.
- [`corpus/`](corpus/README.md): synthetic inputs, manifest, hashes, and gold answers.
- [`tools/`](tools/README.md): deterministic corpus generation and package validation.
- [`COURSE_CHANGELOG.md`](COURSE_CHANGELOG.md): dated course changes and source-audit history.
- [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md): generated structural and machine-readable package checks.
- [`RELEASE_VALIDATION.md`](RELEASE_VALIDATION.md): reproducibility, live-link, and page-render review for this issued copy.
- [`updates/`](updates/README.md): dated evergreen-audit reports and revised-copy records.
- [`PWA_AND_UPDATES.md`](PWA_AND_UPDATES.md): iPhone/iPad installation,
  local-progress limits, and the safe automatic-update path.

## Non-negotiable proof rules

1. A model’s fluent output is never proof. Schemas, deterministic checks, locators, tests, and a reviewer supply proof.
2. Source files are immutable. Derived text, chunks, OCR, embeddings, and drafts live separately.
3. Document text is untrusted data, never an instruction to the workflow.
4. Every factual memo assertion has verified evidence or is labelled `UNSUPPORTED — NEEDS REVIEW`.
5. Approval binds to the cryptographic hash of the exact proposed output. Editing invalidates approval.
6. An action is allowed only once for one approval and one idempotency key.
7. Every run terminates in a named, visible state—even when a dependency fails.
8. Logs contain operational metadata, not raw document contents, secrets, or unnecessary personal data.
9. A manual fallback must remain usable when AI, OCR, storage, or orchestration is unavailable.
10. Product or legal claims marked volatile must be checked with the evergreen update prompt at the prescribed checkpoints.

## Checkpoints for live re-verification

Run the evergreen audit:

- immediately before Week 1;
- immediately before Week 7;
- every 8–12 weeks thereafter;
- sooner after a vendor deprecation, security advisory, material legal change, or failed migration test.

The source audit performed for this edition used official vendor and public-authority pages. The preferred OpenAI documentation connector was unavailable in the build environment, so official OpenAI web documentation was used and this limitation is recorded in the source register.
