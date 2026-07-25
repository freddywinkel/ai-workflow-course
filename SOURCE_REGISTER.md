# Official Source Register

Register version: 1.1.0  
Audit completed: 2026-07-25, Europe/Amsterdam  
Scope: course technology, data controls, security, AVG/GDPR, AI Act, and excluded medical-software boundary  
Authority preference: primary law/public authority → official vendor documentation/release → official repository  

The preferred OpenAI documentation connector was unavailable in the authoring environment. The audit therefore used official OpenAI developer, policy, Help Center, and repository pages through live web access. This is a tooling limitation, not permission to substitute blogs.

## How to read this register

Volatility:

- **High:** verify at every prescribed course audit and before use.
- **Medium:** verify before the affected week and before an upgrade/real deployment.
- **Low:** stable primary law/concept, but check amendments and consolidated text.

Legal/status labels:

- `LAW—BINDING/APPLICABLE`
- `LAW—ADOPTED, NOT YET IN FORCE`
- `FINAL GUIDANCE—NON-BINDING`
- `VOLUNTARY CODE`
- `DRAFT/CONSULTATION—DO NOT RELY ON AS SETTLED`
- `NATIONAL ADVICE/PROPOSAL—NOT LAW`
- `OPERATIONAL GUIDANCE—NOT LAW`
- `VENDOR DOCUMENTATION`
- `OFFICIAL RELEASE/REPOSITORY`
- `WEB PLATFORM DOCUMENTATION`

Every dated/version/price/region/retention/plan statement is a snapshot. The evergreen audit supersedes it when newer primary evidence exists.

## OpenAI and model API

| ID | Source | Verified finding | Status | Applies | Volatility | Last verified |
|---|---|---|---|---|---|---|
| OAI-01 | [Responses migration](https://developers.openai.com/api/docs/guides/migrate-to-responses) | Responses is recommended for new projects. The Assistants API was deprecated 2025-08-26 and has a 2026-08-26 sunset. Responses storage must be configured deliberately. | VENDOR DOCUMENTATION | W5–7, W10–12 | High | 2026-07-25 |
| OAI-02 | [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | Responses supports schema-constrained output and detectable refusals. Current Python helper uses `client.responses.parse(..., text_format=YourPydanticModel)` and parsed content is available through the SDK result. Shape does not prove factual, semantic, or evidence correctness. | VENDOR DOCUMENTATION | W5–6, W10 | High | 2026-07-25 |
| OAI-03 | [Model catalog](https://developers.openai.com/api/docs/models) | Current GPT-5.6 family IDs: `gpt-5.6-sol` (capability), `gpt-5.6-terra` (balance), `gpt-5.6-luna` (cost-sensitive). All are configuration candidates, not permanent code constants. | VENDOR DOCUMENTATION | W5, W10–11 | High | 2026-07-25 |
| OAI-04 | [API pricing](https://developers.openai.com/api/docs/pricing) | Short-context text price snapshot per 1M tokens: Sol $5 input/$0.50 cached/$6.25 explicit cache write/$30 output; Terra $2.50/$0.25/$3.125/$15; Luna $1/$0.10/$1.25/$6. Eligible EU regional processing has a stated 10% uplift for models released from 2026-03-05. | VENDOR DOCUMENTATION | W5, W10–11 | High | 2026-07-25 |
| OAI-05 | [Data controls](https://developers.openai.com/api/docs/guides/your-data) | API content is not used for training by default. Default abuse-monitoring retention can be up to 30 days. Responses application state is retained at least 30 days when stored/default; use `store:false` for the course. ZDR/MAM requires eligibility/approval. | VENDOR DOCUMENTATION | W5, W8–9, W12 | High | 2026-07-25 |
| OAI-06 | [Data controls: regional table](https://developers.openai.com/api/docs/guides/your-data) | European projects/processing exist for listed endpoints/models and require actual regional project configuration/base URL. `store:false` is not ZDR. Regional support differs by feature; tools/third parties have separate paths. | VENDOR DOCUMENTATION | Setup, W5, W8, W11 | High | 2026-07-25 |
| OAI-07 | [Business data privacy](https://openai.com/business-data/) | OpenAI states business/API data is not used to train models by default. Contract and endpoint-specific retention still require review. | VENDOR DOCUMENTATION | W5, W8 | Medium | 2026-07-25 |
| OAI-08 | [Deprecations](https://developers.openai.com/api/docs/deprecations) | Assistants shutdown: 2026-08-26. Hosted Evals read-only: 2026-10-31; shutdown: 2026-11-30. Reusable prompt objects were also listed for 2026-11-30 shutdown. Keep prompts in version control and tests local/vendor-neutral. | VENDOR DOCUMENTATION | W5, W10, W12 | High | 2026-07-25 |
| OAI-09 | [Evals guidance](https://developers.openai.com/api/docs/guides/evals) | The hosted Evals platform is retiring on the dates above. Evaluation principles may be read, but the course foundation is pytest plus frozen JSONL. | VENDOR DOCUMENTATION | W10 | High | 2026-07-25 |
| OAI-10 | [File Search](https://developers.openai.com/api/docs/guides/tools-file-search) | Provider annotations can identify files but are not the capstone’s cryptographically verified page/region/span evidence ledger. | VENDOR DOCUMENTATION | W6 | High | 2026-07-25 |
| OAI-11 | [OpenAI Python releases](https://github.com/openai/openai-python/releases) | Current official SDK snapshot was 2.48.0. Pin the version used by the frozen release and rerun regression before update. | OFFICIAL RELEASE/REPOSITORY | Setup, W5, W12 | High | 2026-07-25 |
| OAI-12 | [OpenAI subprocessor list](https://openai.com/policies/sub-processor-list/) | The list was updated 2026-07-09 and includes processing-location detail. Re-check the selected service/contract and change-notice mechanism. | VENDOR DOCUMENTATION | W8, W11 | High | 2026-07-25 |

## Required technical stack

| ID | Source | Verified finding | Status | Applies | Volatility | Last verified |
|---|---|---|---|---|---|---|
| PY-01 | [Python downloads](https://www.python.org/downloads/) | CPython current snapshots: 3.14.6 and maintained 3.13.14. Course targets 3.13 for dependency maturity, subject to clean install. | OFFICIAL RELEASE/REPOSITORY | Setup | High | 2026-07-25 |
| PY-02 | [Python on Windows](https://docs.python.org/3/using/windows.html) | Official Python Install Manager is the current Windows path; use project virtual environments. | VENDOR DOCUMENTATION | Setup | Medium | 2026-07-25 |
| PY-03 | [Python `hashlib`](https://docs.python.org/3/library/hashlib.html) | SHA-256 is available through the standard library; hash exact streamed bytes. | VENDOR DOCUMENTATION | W3–4 | Low | 2026-07-25 |
| N8N-01 | [n8n releases](https://github.com/n8n-io/n8n/releases) | Stable snapshot 2.31.6; 2.32.5 was prerelease. Pin stable image/tag, not `latest`. | OFFICIAL RELEASE/REPOSITORY | Setup, W2, W12 | High | 2026-07-25 |
| N8N-02 | [n8n Docker installation](https://docs.n8n.io/deploy/host-n8n/install-options/install-with-docker) | Docker is recommended for most self-hosting; SQLite is default and PostgreSQL supported. `.n8n` volume remains necessary even with PostgreSQL. | VENDOR DOCUMENTATION | Setup, W2, W9, W12 | High | 2026-07-25 |
| N8N-03 | [n8n human approval](https://docs.n8n.io/build/integrate-ai/ai-examples/human-in-the-loop-for-tools) | Selected AI-agent tool calls can pause for reviewer approval/denial. This is transport/UI, not proof of exact-output domain approval. | VENDOR DOCUMENTATION | W7 | High | 2026-07-25 |
| N8N-04 | [n8n Wait node](https://docs.n8n.io/build/flow-logic/wait) | A workflow can pause and resume by duration or webhook event. Authenticate callbacks and enforce state, expiry, replay, and idempotency in the domain service. | VENDOR DOCUMENTATION | W2, W7, W9 | Medium | 2026-07-25 |
| N8N-05 | [n8n error workflows](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully) | Error workflows receive workflow/execution/error metadata; error handling does not replace the named domain state machine. | VENDOR DOCUMENTATION | W2, W9 | Medium | 2026-07-25 |
| N8N-06 | [n8n executions](https://docs.n8n.io/workflows/executions/all-executions/) | Failed runs can be retried with current/original workflow. Deleting a workflow deletes its execution history. n8n history is not the append-only audit ledger. | VENDOR DOCUMENTATION | W2, W9, W12 | Medium | 2026-07-25 |
| N8N-07 | [n8n security audit](https://docs.n8n.io/hosting/securing/security-audit/) | `n8n audit` checks credentials, expressions, filesystem, risky/community nodes, webhooks, settings, and outdated versions; it is not a penetration test. | VENDOR DOCUMENTATION | W9, W12 | Medium | 2026-07-25 |
| N8N-08 | [n8n external binary storage](https://docs.n8n.io/hosting/scaling/external-storage/) | Self-hosted S3 binary storage is an Enterprise feature. The course passes Supabase object references through n8n. | VENDOR DOCUMENTATION | W3, W9 | Medium | 2026-07-25 |
| N8N-09 | [n8n license](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) | Community code uses the Sustainable Use License; enterprise-marked files have separate terms. Private learning is acceptable; any later client-hosting model needs its own licensing review. | OFFICIAL RELEASE/REPOSITORY | Software matrix, W11–12 | Medium | 2026-07-25 |
| API-01 | [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/) | Current snapshot 0.140.0, released 2026-07-24. | OFFICIAL RELEASE/REPOSITORY | Setup, W2, W12 | High | 2026-07-25 |
| API-02 | [FastAPI version policy](https://fastapi.tiangolo.com/deployment/versions/) | FastAPI remains pre-1.0 and minor releases can break; lock tested graph and do not pin Starlette separately without reason. | VENDOR DOCUMENTATION | Setup, W10–12 | Medium | 2026-07-25 |
| API-03 | [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/) | `TestClient` is HTTPX-based and works directly with pytest. | VENDOR DOCUMENTATION | W2, W9–12 | Low | 2026-07-25 |
| PYD-01 | [Pydantic releases](https://github.com/pydantic/pydantic/releases) | Stable snapshot 2.13.4; 2.14.0a1 was prerelease. Exclude prereleases in the course lock. | OFFICIAL RELEASE/REPOSITORY | Setup, W5, W12 | High | 2026-07-25 |
| PYD-02 | [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) and [strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) | Default validation can coerce and ignore extras. Boundary models should deliberately use strict validation and `extra='forbid'`, followed by semantic validation. | VENDOR DOCUMENTATION | W3, W5, W10 | Medium | 2026-07-25 |
| TEST-01 | [pytest changelog](https://docs.pytest.org/en/stable/changelog.html) | Current snapshot 9.1.1. Pin and record the release environment. | OFFICIAL RELEASE/REPOSITORY | Setup, W10, W12 | High | 2026-07-25 |
| TEST-02 | [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html) | Tests/fixtures can be parameterised from stable case IDs and JSONL. | VENDOR DOCUMENTATION | W10 | Low | 2026-07-25 |
| DOC-01 | [Docling releases](https://github.com/docling-project/docling/releases) and [PyPI](https://pypi.org/project/docling/) | GitHub latest snapshot 2.115.0 while observed PyPI listing was 2.114.0. Treat discrepancy as a reason to resolve and pin the clean-install version, not to guess. | OFFICIAL RELEASE/REPOSITORY | Setup, W4, W12 | High | 2026-07-25 |
| DOC-02 | [Docling installation/OCR](https://docling-project.github.io/docling/getting_started/installation/) | Windows supported; OCR engines include EasyOCR, RapidOCR, Tesseract and others with different extras/system dependencies. Select one baseline and record model cache. | VENDOR DOCUMENTATION | Setup, W4 | High | 2026-07-25 |
| DOC-03 | [Docling supported formats](https://docling-project.github.io/docling/usage/supported_formats/) | PDF and DOCX supported; course scope remains only quote/terms/policy documents. | VENDOR DOCUMENTATION | W4 | Medium | 2026-07-25 |
| DOC-04 | [Docling provenance model](https://docling-project.github.io/docling/reference/docling_document/) | Provenance items can point to page, bounding box, and character span. Add source SHA-256, chunk ID, and support hash for integrity. | VENDOR DOCUMENTATION | W4, W6, W10 | Medium | 2026-07-25 |
| DOC-05 | [Docling repository license](https://github.com/docling-project/docling/blob/main/LICENSE) | Code is MIT-licensed; individual OCR/model weights can have separate licenses. | OFFICIAL RELEASE/REPOSITORY | Software matrix, W11 | Medium | 2026-07-25 |

## Supabase and PostgreSQL

| ID | Source | Verified finding | Status | Applies | Volatility | Last verified |
|---|---|---|---|---|---|---|
| SUP-01 | [Supabase regions](https://supabase.com/docs/guides/platform/regions) | One primary project region; European choices include Frankfurt and other named regions. Exact selected region must be recorded. | VENDOR DOCUMENTATION | Setup, W3, W8, W12 | High | 2026-07-25 |
| SUP-02 | [Bucket fundamentals](https://supabase.com/docs/guides/storage/buckets/fundamentals) and [Storage access control](https://supabase.com/docs/guides/storage/security/access-control) | Buckets are private by default; private access is controlled by RLS. Service-role keys bypass RLS and must stay server-side. | VENDOR DOCUMENTATION | W3, W8–9 | Medium | 2026-07-25 |
| SUP-03 | [Database RLS](https://supabase.com/docs/guides/database/postgres/row-level-security) | Exposed tables need RLS. Dashboard-created tables may enable it automatically; SQL-created tables require explicit enablement. Views can bypass RLS unless configured. | VENDOR DOCUMENTATION | W3, W8–10 | Medium | 2026-07-25 |
| SUP-04 | [API security](https://supabase.com/docs/guides/api/securing-your-api) | Grants and RLS both matter; test actual anonymous/authenticated roles and keep service keys outside clients. | VENDOR DOCUMENTATION | W3, W9 | Medium | 2026-07-25 |
| SUP-05 | [Database overview](https://supabase.com/docs/guides/database/overview) | Managed database backups do not include Storage objects. Restoration/deletion drills must cover rows and files separately. | VENDOR DOCUMENTATION | W3, W9, W12 | Medium | 2026-07-25 |
| SUP-06 | [pgvector](https://supabase.com/docs/guides/ai/vector-columns) | `vector` can store/query embeddings. Optional only; embeddings require tenancy, retention, deletion, and evaluation. | VENDOR DOCUMENTATION | W6, W10–11 | Medium | 2026-07-25 |
| SUP-07 | [Supabase license](https://github.com/supabase/supabase/blob/master/LICENSE) | Main repository is Apache-2.0; hosted-service terms are separate. | OFFICIAL RELEASE/REPOSITORY | Software matrix | Medium | 2026-07-25 |
| PG-01 | [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) | Unique/check/foreign-key constraints support source/idempotency/state integrity. | VENDOR DOCUMENTATION | W3, W7 | Low | 2026-07-25 |
| PG-02 | [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | State and approval/action concurrency require explicit transactions/locking and stale-write tests. | VENDOR DOCUMENTATION | W3, W7 | Low | 2026-07-25 |
| PG-03 | [PostgreSQL full-text search](https://www.postgresql.org/docs/current/textsearch.html) | Full-text search provides a vendor-neutral retrieval baseline for the short policy. | VENDOR DOCUMENTATION | W6 | Low | 2026-07-25 |

## Optional comparison and advanced tools

| ID | Source | Verified finding | Status | Applies | Volatility | Last verified |
|---|---|---|---|---|---|---|
| MS-01 | [Power Automate approvals](https://learn.microsoft.com/en-us/power-automate/get-started-approvals) | “Start and wait for an approval” pauses a cloud flow; approval records use Microsoft services/Dataverse. Licensing and exact-output binding need separate verification. | VENDOR DOCUMENTATION | W7, W11 | High | 2026-07-25 |
| MS-02 | [Power Automate licensing](https://learn.microsoft.com/en-us/power-platform/admin/power-automate-licensing/types) | Premium/AI capabilities depend on current licensing. Do not promise a free path. | VENDOR DOCUMENTATION | W11 | High | 2026-07-25 |
| AZ-01 | [Azure Document Intelligence Layout](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout?view=doc-intel-4.0.0) | Recommended v4.0 API (`2024-11-30`) extracts text, tables, spans, and bounding regions. | VENDOR DOCUMENTATION | W4, W11 | High | 2026-07-25 |
| AZ-02 | [Azure Document Intelligence privacy/security](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/document-intelligence/data-privacy-security) | Analyse results are temporarily retained (24-hour snapshot) and v4.0 supports early deletion; verify current region, limits, and account configuration. | VENDOR DOCUMENTATION | W8, W11 | High | 2026-07-25 |
| MAKE-01 | [Make error handling](https://help.make.com/overview-of-error-handling) and [incomplete executions](https://help.make.com/incomplete-executions) | Make supports skip/retry/resume/commit/rollback handlers and incomplete executions; incomplete executions are disabled by default. Substituted data is unsafe for evidence facts. | VENDOR DOCUMENTATION | W2, W9, W11 | High | 2026-07-25 |
| MAKE-02 | [Make organisations](https://help.make.com/organizations) | Organisation setup can include EU/US data-centre choice; verify exact plan/service processing before making a regional claim. | VENDOR DOCUMENTATION | W8, W11 | High | 2026-07-25 |
| MIS-01 | [Mistral OCR](https://docs.mistral.ai/studio-api/document-processing/basic_ocr) | Current Document AI path used `mistral-ocr-latest`/OCR 4 with structured page output, bounding boxes, and optional confidence. | VENDOR DOCUMENTATION | W4, W11 | High | 2026-07-25 |
| MIS-02 | [Mistral regional inference](https://docs.mistral.ai/studio-api/regional-inference) and [pricing](https://mistral.ai/pricing/api/) | EU endpoint `api.eu.mistral.ai`; eligible regional inference has 10% uplift. OCR 4 listed at $4/1,000 pages at audit. Regional feature set can be narrower. | VENDOR DOCUMENTATION | W8, W11 | High | 2026-07-25 |
| MIS-03 | [Mistral ZDR](https://help.mistral.ai/en/articles/347612-can-i-activate-zero-data-retention-zdr) and [training opt-out](https://help.mistral.ai/en/articles/455207-can-i-opt-out-of-my-input-or-output-data-being-used-for-training) | ZDR is plan/endpoint-specific; training opt-out, retention, and region are distinct controls. | VENDOR DOCUMENTATION | W8, W11 | High | 2026-07-25 |
| OLL-01 | [Ollama API](https://docs.ollama.com/api/introduction), [Structured Outputs](https://docs.ollama.com/capabilities/structured-outputs), and [OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility) | Local API defaults to loopback; JSON Schema/Pydantic output supported. OpenAI compatibility is partial and Responses is non-stateful. | VENDOR DOCUMENTATION | W5, W10–11 | High | 2026-07-25 |
| OLL-02 | [Ollama authentication](https://docs.ollama.com/api/authentication), [FAQ](https://docs.ollama.com/faq), [Windows](https://docs.ollama.com/windows) | Local loopback API has no authentication; model storage/hardware/context can be substantial. A `:cloud` model is not local. | VENDOR DOCUMENTATION | Setup, W9, W11 | High | 2026-07-25 |
| PF-01 | [Promptfoo configuration](https://www.promptfoo.dev/docs/configuration/guide/) and [CLI](https://www.promptfoo.dev/docs/usage/command-line/) | YAML evaluation and threshold exit status are available. Use only after local JSONL/pytest; do not depend on hosted results. | VENDOR DOCUMENTATION | Optional W10 | High | 2026-07-25 |
| PF-02 | [Promptfoo red-team configuration](https://www.promptfoo.dev/docs/red-team/configuration/) and [security](https://github.com/promptfoo/promptfoo/security) | Some red-team generation can be remote; local-only flag exists. Imported custom code runs unsandboxed. Use synthetic data. | VENDOR DOCUMENTATION | Optional W9–10 | High | 2026-07-25 |
| LF-01 | [Langfuse data model](https://langfuse.com/docs/observability/data-model), [scores](https://langfuse.com/docs/evaluation/scores/overview), [Docker Compose](https://langfuse.com/self-hosting/deployment/docker-compose) | Traces/observations/scores and local Compose exist. Simple local setup is not HA/backup proof; prompts/content often enter traces. | VENDOR DOCUMENTATION | Optional W9–10 | High | 2026-07-25 |

License snapshot: FastAPI, Pydantic, pytest, Docling, Promptfoo and Langfuse core were described in their official repositories as MIT (with noted enterprise/model exceptions); Supabase main repository Apache-2.0; n8n uses its Sustainable Use License. Re-check exact packages, model weights, enterprise directories, and hosted terms.

## AVG/GDPR, rights, and transfers

| ID | Source | Verified finding | Status | Applies | Volatility | Last verified |
|---|---|---|---|---|---|---|
| GDPR-01 | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) | Primary AVG/GDPR text: definitions, principles, legal bases, special categories, rights, Article 22, privacy by design, processors, security/DPIA, transfers. | LAW—BINDING/APPLICABLE | W1, W7–9, W12 | Low | 2026-07-25 |
| GDPR-02 | [CJEU C-683/21](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62021CJ0683) | Relevant to genuinely fictitious information; do not equate pseudonymised real records with fiction/anonymity. | LAW—BINDING/APPLICABLE | W8 | Low | 2026-07-25 |
| GDPR-03 | [EDPB Guidelines 07/2020](https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-of-controller-and-processor-in-the-gdpr_en) | Functional controller/processor/joint-controller analysis depends on actual activity and essential means. | FINAL GUIDANCE—NON-BINDING | W8 | Low | 2026-07-25 |
| GDPR-04 | [EDPB Opinion 22/2024](https://www.edpb.europa.eu/documents/opinion-of-the-board-art-64/opinion-222024-on-certain-obligations-following-from-the_en) | Processor/subprocessor chain obligations and controller information/verification considerations. | FINAL GUIDANCE—NON-BINDING | W8 | Low | 2026-07-25 |
| GDPR-05 | [AP privacy rights in practice](https://autoriteitpersoonsgegevens.nl/themas/basis-avg/privacyrechten-avg/voor-organisaties-privacyrechten-in-de-praktijk) | Dutch operational rights-handling guidance, including response workflow. | OPERATIONAL GUIDANCE—NOT LAW | W8, W12 | Medium | 2026-07-25 |
| GDPR-06 | [AP mandatory-DPIA list](https://www.autoriteitpersoonsgegevens.nl/documenten/lijst-verplichte-dpia) | National Article 35(4) mandatory list; re-check before any Dutch real-data deployment. | LAW—BINDING/APPLICABLE | W8 | Medium | 2026-07-25 |
| GDPR-07 | [EDPB-endorsed WP29 guidance](https://www.edpb.europa.eu/endorsed-wp29-guidelines_en) | Includes non-binding DPIA high-risk criteria; reasoned assessment is not a mechanical score. | FINAL GUIDANCE—NON-BINDING | W8 | Low | 2026-07-25 |
| GDPR-08 | [EDPB anonymisation Guidelines 02/2026](https://www.edpb.europa.eu/public-consultations/guidelines-022026-on-anonymisation_en) | Consultation draft in 2026; do not rely on it as settled final guidance. | DRAFT/CONSULTATION—DO NOT RELY ON AS SETTLED | W8, update audit | High | 2026-07-25 |
| GDPR-09 | [Commission adequacy decisions](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en) | Live adequacy register; must be checked for a real-data transfer assessment. | LAW—BINDING/APPLICABLE | W8, W11 | High | 2026-07-25 |
| GDPR-10 | [Commission SCC information](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en) | SCC implementation material; SCCs do not remove need to assess actual transfer conditions. | LAW—BINDING/APPLICABLE | W8, W11 | Medium | 2026-07-25 |
| GDPR-11 | [EDPB Recommendations 01/2020](https://www.edpb.europa.eu/documents/recommendation/recommendations-012020-on-measures-that-supplement-transfer-tools-to_en) | Transfer assessment and supplementary measures guidance. | FINAL GUIDANCE—NON-BINDING | W8 | Low | 2026-07-25 |

## AI Act and Dutch status

| ID | Source | Verified finding | Status | Applies | Volatility | Last verified |
|---|---|---|---|---|---|---|
| AIA-01 | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) | Primary AI Act with phased application; read with later amendment. | LAW—BINDING, PHASED APPLICATION | W8, W12 | Medium | 2026-07-25 |
| AIA-02 | [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) | Published 2026-07-24; enters into force 2026-07-27. Amends Article 4 and timing provisions. High-risk dates are generally 2027-12-02 for Annex III and 2028-08-02 for Annex I product systems; a limited provider-side Article 50(2) transition reaches 2026-12-02. Verify exact scope. | LAW—ADOPTED, NOT YET IN FORCE | W8, update audit | High | 2026-07-25 |
| AIA-03 | [Commission AI Act overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) | Official live explainer/timeline; verify against consolidated law. | FINAL GUIDANCE—NON-BINDING | W8, W12 | High | 2026-07-25 |
| AIA-04 | [Final Article 50 guidelines](https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems) | Final non-binding Commission guidance published July 2026; Article 50 obligations generally apply 2026-08-02. | FINAL GUIDANCE—NON-BINDING | W8, W12 | Medium | 2026-07-25 |
| AIA-05 | [Article 50 FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act) | Official explanatory material on direct interaction, synthetic marking, public-interest text, and substantive human review/editorial control. | FINAL GUIDANCE—NON-BINDING | W8 | Medium | 2026-07-25 |
| AIA-06 | [Code of Practice on AI-generated content](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content) | Voluntary code; adherence is not conclusive compliance proof. | VOLUNTARY CODE | W8, update audit | Medium | 2026-07-25 |
| AIA-07 | [Draft high-risk classification guidelines](https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems) | Consultation draft; do not teach as final/binding classification. | DRAFT/CONSULTATION—DO NOT RELY ON AS SETTLED | W8, update audit | High | 2026-07-25 |
| AIA-08 | [AI-system definition guidelines](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-ai-system-definition-facilitate-first-ai-acts-rules-application) | Commission interpretation explicitly non-binding. | FINAL GUIDANCE—NON-BINDING | W8 | Medium | 2026-07-25 |
| AIA-09 | [AP meaningful human-intervention consultation](https://www.autoriteitpersoonsgegevens.nl/documenten/consultatie-betekenisvolle-menselijke-tussenkomst) | Consultation/draft design material; not a binding legal test. | DRAFT/CONSULTATION—DO NOT RELY ON AS SETTLED | W7–8 | High | 2026-07-25 |
| AIA-10 | [AP AI-literacy guide](https://autoriteitpersoonsgegevens.nl/documenten/aan-de-slag-met-ai-geletterdheid) | Useful operational guidance from January 2025 but predates amended 2026 Article 4 wording; annotate and re-check. | OPERATIONAL GUIDANCE—NOT LAW | W8 | High | 2026-07-25 |
| AIA-11 | [AP/RDI final advice on Dutch supervision](https://www.autoriteitpersoonsgegevens.nl/system/files?file=2024-11%2FEindadvies+Inrichting+AI-toezicht+Nederland_AP_RDI.pdf) | Advice on supervisory allocation; not itself final designating law. | NATIONAL ADVICE/PROPOSAL—NOT LAW | W8, update audit | High | 2026-07-25 |
| AIA-12 | [Dutch cabinet step on AI supervision](https://www.rijksoverheid.nl/actueel/nieuws/2026/04/20/kabinet-zet-stap-met-toezicht-op-europese-ai-regels) | Described a legislative proposal/consultation-stage national arrangement at audit; do not present authorities as finally designated without enacted text. | NATIONAL ADVICE/PROPOSAL—NOT LAW | W8, update audit | High | 2026-07-25 |
| AIA-13 | [AP/RDI sandbox proposal](https://www.autoriteitpersoonsgegevens.nl/system/files?file=2025-03%2FVormvoorstel+regulatory+sandbox+AI-verordening.pdf) | Proposed sandbox design; not proof of an available operational route. | NATIONAL ADVICE/PROPOSAL—NOT LAW | W8, update audit | High | 2026-07-25 |

## Security, incidents, and medical boundary

| ID | Source | Verified finding | Status | Applies | Volatility | Last verified |
|---|---|---|---|---|---|---|
| SEC-01 | [NCSC five basic principles](https://www.ncsc.nl/basisprincipes/resultaten) | Dutch operational baseline: map risks, secure behaviour, protect systems, manage access, prepare for incidents. | OPERATIONAL GUIDANCE—NOT LAW | W9, W12 | Medium | 2026-07-25 |
| SEC-02 | [NCSC SOC/CIRP preparation](https://www.ncsc.nl/soc/soc-voorbereiden) | Incident-plan/playbook preparation material. | OPERATIONAL GUIDANCE—NOT LAW | W9 | Medium | 2026-07-25 |
| SEC-03 | [NCSC incident-response plan](https://www.ncsc.nl/incidenten-en-herstellen/incident-response-plan) | Practical incident-response structure for organisations. | OPERATIONAL GUIDANCE—NOT LAW | W9 | Medium | 2026-07-25 |
| SEC-04 | [OWASP Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) and [LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | Prompt injection needs layered instruction/data, capability, validation, approval, and monitoring controls; prompt text alone is insufficient. | OPERATIONAL GUIDANCE—NOT LAW | W9–10 | Medium | 2026-07-25 |
| SEC-05 | [AP breach response](https://autoriteitpersoonsgegevens.nl/themas/beveiliging/datalekken/datalek-dit-moet-u-doen) | Dutch operational breach guidance used with GDPR Articles 33–34. Fictional corpus incident does not cause a real AP notification. | OPERATIONAL GUIDANCE—NOT LAW | W9 | Medium | 2026-07-25 |
| SEC-06 | [EDPB Guidelines 01/2021](https://www.edpb.europa.eu/documents/guideline/guidelines-012021-on-examples-regarding-personal-data-breach-notification_en) | Worked personal-data-breach examples and notification reasoning. | FINAL GUIDANCE—NON-BINDING | W9 | Low | 2026-07-25 |
| MED-00 | [AP health-data topic](https://autoriteitpersoonsgegevens.nl/themas/gezondheid) | Dutch authority explains that health information receives special AVG protection. The course excludes it independently of medical-device status. | OPERATIONAL GUIDANCE—NOT LAW | W8 boundary | Medium | 2026-07-25 |
| MED-01 | [MDR — Regulation (EU) 2017/745](https://eur-lex.europa.eu/eli/reg/2017/745/oj/eng) | Binding medical-device framework; intended medical purpose is central to software qualification. | LAW—BINDING/APPLICABLE | W8 boundary | Low | 2026-07-25 |
| MED-02 | [MDCG 2019-11 rev.1](https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en) | Updated June 2025 software qualification/classification guidance; non-binding. Human review does not automatically prevent qualification. | FINAL GUIDANCE—NON-BINDING | W8 boundary | Medium | 2026-07-25 |
| MED-03 | [MDCG 2025-6](https://health.ec.europa.eu/latest-updates/mdcg-2025-6-faq-interplay-between-medical-devices-regulation-vitro-diagnostic-medical-devices-2025-06-19_en) | Guidance on MDR/IVDR and AI Act interplay. | FINAL GUIDANCE—NON-BINDING | W8 boundary | Medium | 2026-07-25 |
| MED-04 | [IGJ safe digital-care products](https://www.igj.nl/onderwerpen/themas-in-het-toezicht/digitale-zorg/veilige-producten) | Dutch regulator operational guidance for digital-care/medical software. | OPERATIONAL GUIDANCE—NOT LAW | W8 boundary | Medium | 2026-07-25 |
| MED-05 | [IGJ generative-AI warning](https://www.igj.nl/documenten/2025/02/10/igj-roept-zorgaanbieders-op-ga-zorgvuldig-om-met-invoering-van-generatieve-ai-toepassingen) | Diagnosis/prescribing support can enter medical-device functionality; course excludes these uses. | OPERATIONAL GUIDANCE—NOT LAW | W8 boundary | Medium | 2026-07-25 |

## Course PWA, publication, and scheduled maintenance

| ID | Source | Verified finding | Status | Applies | Volatility | Last verified |
|---|---|---|---|---|---|---|
| PWA-01 | [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) | A custom Pages deployment uses a build artifact plus a deploy job with `pages: write` and `id-token: write`. Current documented majors include `actions/configure-pages@v5`, `actions/upload-pages-artifact@v4`, and `actions/deploy-pages@v4`. | VENDOR DOCUMENTATION | PWA release | High | 2026-07-25 |
| PWA-02 | [GitHub `setup-node`](https://github.com/actions/setup-node) and [`setup-python`](https://github.com/actions/setup-python) | Current documented major for both setup actions is v6; checkout examples use `actions/checkout@v6`. Re-audit action majors and security advisories before changing the workflow. | OFFICIAL RELEASE/REPOSITORY | PWA release | High | 2026-07-25 |
| PWA-03 | [Codex scheduled tasks](https://developers.openai.com/codex/app/automations) | Desktop scheduled tasks can work with local projects in the project directory or a worktree. The computer must remain on, the desktop app must be running, and unattended runs use configured sandbox permissions. | VENDOR DOCUMENTATION | Course maintenance | High | 2026-07-25 |
| PWA-04 | [Apple: turn a website into an app](https://support.apple.com/en-ca/guide/iphone/iphea86e5236/ios) | Current iPhone path is Safari → Share → Add to Home Screen → enable Open as Web App → Add. The app includes this install path and does not claim background scheduling by iOS. | VENDOR DOCUMENTATION | PWA install | Medium | 2026-07-25 |
| PWA-05 | [Service-worker update](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/update), [`skipWaiting`](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerGlobalScope/skipWaiting), and [`controllerchange`](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerContainer/controllerchange_event) | The reader explicitly checks its registration, leaves a new worker waiting, activates it only after the learner chooses the visible update action, and reloads once after controller change. | WEB PLATFORM DOCUMENTATION | PWA update | Medium | 2026-07-25 |

## Audit decisions carried into the course

1. Use Responses, not Assistants.
2. Use local JSONL/pytest, not hosted OpenAI Evals.
3. Call current Python `responses.parse` through an adapter and set `store=False`.
4. Structured Outputs supplies shape only; evidence and semantic validators remain authoritative.
5. Benchmark Terra/Luna; Sol only as optional quality ceiling; IDs configurable.
6. Pin n8n stable Docker image; its execution history is not the domain ledger.
7. Keep n8n approval as transport/UI and enforce exact-output approval in Python/PostgreSQL.
8. Keep source binaries in private Supabase Storage, pass references through n8n, and back up storage separately.
9. Keep pgvector, Promptfoo, and Langfuse optional.
10. Teach legal status explicitly and re-audit the 2026 amendment/Article 50/Dutch arrangements before Week 1 and Week 7.

## Next mandatory review

Earliest of:

- immediately before the learner starts Week 1;
- immediately before Week 7;
- 2026-09-25;
- any relevant deprecation, security advisory, pricing/region/data-control change, legal amendment, finalisation of draft guidance, or Dutch supervisory legislation.

Use [`EVERGREEN_UPDATE_PROMPT.md`](EVERGREEN_UPDATE_PROMPT.md). If live browsing is unavailable, the correct outcome is `UNVERIFIED`, not an update based on memory.
