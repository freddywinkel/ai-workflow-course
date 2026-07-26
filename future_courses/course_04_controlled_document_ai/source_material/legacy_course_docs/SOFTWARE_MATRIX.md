# Software Matrix and Selection Rules

Verified: 2026-07-25. Product names, plans, versions, regions, data controls, and prices are volatile. Re-run [`EVERGREEN_UPDATE_PROMPT.md`](EVERGREEN_UPDATE_PROMPT.md) before installing or buying anything.

## Required learning stack

| Layer | Default | Why it is taught | Required use | Replacement boundary |
|---|---|---|---|---|
| Orchestration | n8n | visible HTTP/JSON flows, retries, connectors, pauses | intake, calls to your API, retry/error routes, approval notification | may be replaced if exported contracts and state rules remain |
| Domain service | Python + FastAPI | portable, testable business boundary | hashing, validation, transitions, approval/action checks | language may change; HTTP and JSON contracts may not |
| Data contracts | Pydantic + JSON Schema | code validation plus vendor-neutral artifact | every boundary object | generated equivalents are acceptable |
| Parsing | Docling | PDF/DOCX/table support and document provenance | local parsing and one OCR path | another parser must pass the same gold set |
| Regression | pytest | local, transparent, CI-friendly tests | deterministic, integration, and frozen-corpus tests | any runner that consumes the same JSONL and produces equivalent metrics |
| Model API | OpenAI Responses + Structured Outputs | current OpenAI API path and schema-constrained output | extraction and drafting labs | provider adapter must preserve contracts |
| Database | PostgreSQL through Supabase | relational state, constraints, audit records | state authority and metrics | local PostgreSQL is allowed through Week 6 |
| Object storage | private Supabase Storage bucket | private raw/derived separation and policies | demo storage by Week 8 | S3-compatible storage is acceptable if equivalent controls are proven |
| Retrieval | PostgreSQL full-text; optional pgvector | begin simple, add semantics only when measured | policy retrieval | vector retrieval is optional for the short policy |
| Version control | Git | exact code/prompt/schema evidence | all course work | none |

## Audited version snapshot

This is evidence for the 2026-07-25 edition, not permission to skip the pre-Week-1 audit.

| Component | Official snapshot observed | Course choice |
|---|---|---|
| CPython | 3.14.6 current; 3.13.14 maintained | Python 3.13 baseline for mature dependency compatibility |
| n8n | 2.31.6 stable; 2.32.5 prerelease | pin 2.31.6 unless the live audit and full tests justify a newer stable |
| FastAPI | 0.140.0 | direct pin; lock transitive graph |
| Pydantic | 2.13.4 stable; 2.14.0a1 prerelease | pin 2.13.4; exclude prereleases |
| pytest | 9.1.1 | direct pin |
| Docling | GitHub 2.115.0; PyPI 2.114.0 observed | pin installable 2.114.0 for the dated starter; resolve/retest if channels converge |
| OpenAI Python SDK | 2.48.0 | direct pin |

FastAPI remains pre-1.0, and Docling/OCR dependencies and model caches can change independently. The release record must include the complete resolved lock and OCR model/cache manifest, not only this table.

## Model policy for this edition

Do not embed a permanent model ID in code. Configure and record it.

| Workload | 2026-07-25 starting candidate | Comparison | Selection rule |
|---|---|---|---|
| extraction | `gpt-5.6-terra` | `gpt-5.6-luna` | choose the least costly configuration that passes the frozen field and locator gates |
| grounded memo | `gpt-5.6-terra` | `gpt-5.6-luna`; optionally `gpt-5.6-sol` | use a more capable model only if citation completeness or unsupported-claim tests improve materially |
| embeddings | optional and configurable | lexical retrieval baseline | add only if retrieval evaluation beats the lexical baseline |

OpenAI’s dated catalog described Sol as flagship, Terra as balancing intelligence and cost, and Luna as cost-sensitive. Prices at verification were, per million text tokens: Sol `$5` input / `$30` output; Terra `$2.50` / `$15`; Luna `$1` / `$6`. Treat these as dated audit facts, not a budget guarantee. The course benchmark records actual usage, latency, and current price-table inputs.

Use:

- the Responses API for new work;
- Structured Outputs for shape;
- `store: false` for the course calls;
- a local state store and audit ledger;
- explicit refusal, truncation, rate-limit, timeout, and schema-failure handling.

Do not use:

- the retiring Assistants API;
- OpenAI’s retiring hosted Evals platform as the course test foundation;
- ChatGPT consumer UI as a substitute for an API integration;
- provider file-search citations as the capstone evidence system;
- an LLM to perform arithmetic or authorize an action.

## Required accounts and cost controls

| Account | Needed by | Cost-control action |
|---|---|---|
| OpenAI API project | Week 5 | separate course project, low spend limit, key scoped to the project, alerts, delete/rotate after course |
| Supabase | Week 3 or local-first Week 6 | European region, free/low tier if suitable, private buckets, RLS enabled, no real data |
| n8n local | Week 2 | Docker local; no cloud subscription required |
| Git hosting | optional | private repository only; local Git is sufficient |
| Microsoft or Google developer account | Week 11 only | use a synthetic mailbox/folder and draft-only permission |

A ChatGPT subscription does not include OpenAI API usage. Confirm current billing terms in the API dashboard before Week 5.

## Comparison technologies

Complete one structured comparison; do not rebuild the whole system in each tool.

| Option | What to compare | Course lab |
|---|---|---|
| Power Automate | M365 connectors, approvals, licensing, environment/DLP controls | Week 11 architecture mapping or connector |
| Make | visual orchestration, EU organisation data centre, retry/error model | Week 2 paper comparison |
| Mistral OCR | page/document OCR response, regional endpoint and retention terms | Week 11 one-case parser comparison |
| Azure Document Intelligence | layout/table/bounding-region output, temporary processing, Azure region/config | Week 11 one-case parser comparison |
| Ollama | local model operation, JSON-schema output, hardware/quality/latency trade-off | Week 11 provider adapter comparison |
| Google Workspace | Drive/Gmail permissions and draft-only action | Week 11 connector option |
| Microsoft 365 | OneDrive/SharePoint/Outlook permissions and draft-only action | Week 11 connector option |

Comparison questions:

1. Can it preserve the six domain contracts?
2. Can it supply stable page/region/span evidence?
3. Where is content processed and retained under the actual selected plan?
4. Can credentials and tenants be isolated?
5. What happens during timeout, retry, duplicate, and partial failure?
6. Can a human see the evidence and exact proposed output?
7. Can an approval be bound to the output hash?
8. Can the gold set be run without vendor lock-in?
9. What are current license, usage, and exit constraints?

## Optional advanced extensions

Add these only after Week 10’s local tests pass:

- **Promptfoo:** convenient provider comparison and adversarial prompt matrices. Keep the JSONL gold set authoritative.
- **Langfuse:** prompt/version/trace dashboards. Configure redaction and retention before sending traces.
- **pgvector:** semantic policy retrieval when the retrieval evaluation justifies it.
- **OpenTelemetry:** cross-service traces when local structured logs no longer answer failures.

## License discipline

Before putting a component into a real implementation:

- record its package/repository URL, exact version, license and license URL;
- distinguish open-source code from separately licensed model weights;
- preserve third-party notices;
- check hosted-plan terms separately from code license;
- run vulnerability and dependency scans;
- record an exit/export path.

The course source register links to official license or repository pages where practical. The evergreen audit must re-check licenses because packages and hosted terms can change independently.

At this audit, FastAPI, Pydantic, pytest, Docling, Promptfoo, and Langfuse core used MIT licensing (with separate enterprise/model exceptions); Supabase’s main repository used Apache-2.0. n8n uses the Sustainable Use License rather than a conventional open-source license. Private learning is within the course boundary; any later arrangement that hosts client workflows or credentials requires a fresh n8n licensing review.

## Deliberately excluded tools

No agent framework is required. No low-code “AI agent” node may bypass the API contracts. No autonomous browser or computer-control tool is needed. No public web deployment, public webhook, real mailbox, real supplier document, fine-tuning, or custom model training is required.
