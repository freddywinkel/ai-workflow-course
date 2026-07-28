# Controlled Document Intake Demo

This folder contains the working technical demonstration used by the
[advanced capstone](../../../advanced_capstone/README.md). In normal human
language: it accepts one known made-up quotation, reads it, creates
source-linked fields, lets artificial intelligence (AI) select from verified
candidate identifiers, turns those selections into fixed source-linked
wording, waits for a human decision, and exports comma-separated values (CSV)
and JavaScript Object Notation (JSON) only after exact approval.

It has two modes:

- `fake`: runs locally with deterministic offline adapters and spends no cloud
  credit;
- `google`: uses Google Document AI, Gemini through Vertex AI, Firestore
  counters, and a private Google Cloud Run service.

This is a synthetic training proof, not a production or client system.

FastAPI is the Python web framework. Portable Document Format (PDF) is the only
accepted upload format. Optical character recognition (OCR) changes document
pixels or embedded characters into machine-readable text. Secure Hash
Algorithm 256-bit (SHA-256) creates source and output fingerprints.

## Non-negotiable boundary

- Process only the six exact frozen files in `fixtures/manifest.json`.
- Never use employer, client, quality-system, medical, personal, confidential,
  or otherwise real data.
- Never make the Cloud Run service unauthenticated.
- Never click **Activate** or upgrade the Google Cloud Free Trial to paid.
- Never deploy without the course cost gate.
- Stop new live calls on 20 October 2026.
- Tear down the dedicated project after the live proof.

## What is implemented

```text
browser
  -> private FastAPI application
  -> hash, PDF, size, page, date and usage gates
  -> memory-backed temporary file
  -> Document AI Enterprise Document OCR in eu
  -> deterministic fields and exact source anchors
  -> fixed findings narrow the allowed action type
  -> Gemini 3.5 Flash-Lite in eu selects bounded candidate identifiers
  -> application renders exact summary wording + exact action template
  -> schema, citation, finding, action-evidence and forbidden-action checks
  -> exact-output human decision
  -> approved-only local CSV/JSON download
  -> temporary-file deletion on success or failure
```

The raw Portable Document Format (PDF) file is not written to Cloud Storage,
Firestore, an application database, or logs. Firestore stores only prototype
run and page counters. See
[retention and data boundary](docs/RETENTION_AND_DATA_BOUNDARY.md) for the
important provider-retention caveats.

## Folder map

| Path | Purpose |
|---|---|
| `src/controlled_intake/` | application, providers, controls, schemas, evidence and exports |
| `static/` | private browser interface |
| `fixtures/manifest.json` | allowlist of six exact synthetic PDF hashes |
| `tests/` | offline happy-path, safe-stop, web and cloud-contract tests |
| `scripts/preflight.ps1` | checks project pattern, Free Trial confirmation and date gate |
| `scripts/deploy.ps1` | creates the bounded private Google resources |
| `scripts/verify_live.ps1` | proves no public Identity and Access Management (IAM) member, rejects an unauthenticated request, then mints a short-lived token and runs private live acceptance |
| `scripts/teardown.ps1` | dry-run and confirmed resource/project deletion |
| `Dockerfile` | Python 3.12 non-root Cloud Run container |
| `.env.example` | documented configuration and hard prototype limits |

The synthetic source corpus is outside this folder at
[`../source_material/corpus`](../source_material/corpus/README.md).

## Local quick start

Requirements:

- Windows PowerShell;
- Python 3.12;
- internet access only for the first package installation.

From this folder:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --requirement .\requirements-dev.txt
$env:PROVIDER_MODE = 'fake'
python -m pytest
python -m uvicorn controlled_intake.main:app --app-dir .\src --host 127.0.0.1 --port 8080 --no-access-log
```

Open `http://127.0.0.1:8080`. Press `Ctrl+C` to stop the server. Fake mode does
not call Google and does not prove live OCR.

The metadata-only health endpoint is `http://127.0.0.1:8080/api/health`. In the
cloud it is the same `/api/health` path behind private Cloud Run
authentication. There is no `/healthz` endpoint.

For beginner-safe follow-along work, start with
[Capstone Gate 0](../../../advanced_capstone/00_READINESS_COST_GATE.md) and
complete the lessons in order.

## Configuration contract

| Variable | Prototype value | Meaning |
|---|---|---|
| `PROVIDER_MODE` | `fake` locally, `google` in Cloud Run | chooses offline or Google adapters |
| `DOCUMENT_AI_LOCATION` | `eu` | European Union Document AI processor |
| `VERTEX_LOCATION` | `eu` | European Union Vertex AI model processing |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite` | current generally available bounded-selection model |
| `MAX_FILE_BYTES` | `5000000` | maximum request bytes |
| `MAX_PAGES_PER_DOCUMENT` | `3` | maximum pages per accepted PDF |
| `MAX_LIVE_RUNS` | `20` | lifetime prototype provider-call reservations |
| `MAX_TOTAL_PAGES` | `60` | lifetime prototype page reservations |
| `MAX_GEMINI_INPUT_CHARACTERS` | `24000` | prompt-size guard |
| `MAX_GEMINI_OUTPUT_TOKENS` | `800` | model-output guard |
| `REVIEW_TTL_MINUTES` | `30` | maximum time to approve the signed proposal |
| `LIVE_HARD_STOP` | `2026-10-20T00:00:00+00:00` | immutable Google-mode deadline; blocks new live provider calls |

Google mode rejects another model, a changed hard-stop date, the documented
placeholder secret, or wider input/output token limits. The application also
rejects wider file, page, run, page-total, and review-time settings. Do not
raise these values for the prototype. The date stop does not disable the
offline fake learning mode after the cloud lab closes.

## Cloud path

Read these before any Google deployment:

1. [Cost controls](docs/COST_CONTROLS.md)
2. [Retention and data boundary](docs/RETENTION_AND_DATA_BOUNDARY.md)
3. [Deployment and teardown](docs/DEPLOYMENT_AND_TEARDOWN.md)
4. [Beginner deployment lesson](../../../advanced_capstone/07_CLOUD_RUN_DEPLOYMENT.md)
5. [Live validation lesson](../../../advanced_capstone/08_LIVE_VALIDATION.md)
6. [Teardown lesson](../../../advanced_capstone/09_TEARDOWN.md)

The intended live locations are:

| Resource | Location |
|---|---|
| Cloud Run | `europe-west4` — Netherlands |
| Firestore | `europe-west4` |
| Secret Manager | `europe-west4` |
| Document AI | `eu` using `eu-documentai.googleapis.com` |
| Gemini through Vertex AI | `eu`, not the global location |
| Artifact Registry source image | `europe-west4` |
| Cloud Storage source staging, if created | dedicated project only |

## What a valid proof contains

- all offline tests passing unchanged;
- no `allUsers` or `allAuthenticatedUsers` Cloud Run member and a `401` or
  `403` response without a token;
- `provider_mode: google` from `/api/health`;
- Document AI and Vertex AI both reported in `eu`;
- the expected states for C001, C004, C008 and C012;
- corrupt-file and changed-hash safe stops;
- exact evidence identifiers on every app-rendered statement and action;
- every action citation linked to a field permitted for that action type;
- temporary deletion true and raw persistence false;
- one approved C001 export represented only by CSV/JSON hashes in the live
  report;
- a post-run cost check; and
- teardown evidence: the alerts-only budget absent after public application
  programming interface (API) deletion, both Preview spend caps absent after
  Billing user-interface deletion/verification, and no Billing account
  identifier recorded.

It must contain no raw document text, model output, access token, secret value,
account email, billing identifier, or real data.

## Recorded reference proof — completed and torn down

On 28 July 2026, the actual private Google path passed. This is an observed
result, not a proposed test:

| Check | Observed result |
|---|---|
| Cloud Run | private Identity and Access Management (IAM) only, `europe-west4`, ready, minimum 0, maximum 1 |
| health | `/api/health`, provider `google` |
| provider locations | Document AI `eu`; Vertex AI `eu` |
| C001 | `pending_approval`, 14 fields, 14 evidence links; approved CSV/JSON hashes recorded |
| C004 | `pending_approval`, 14 fields, 14 evidence links |
| C008 | `needs_review`, `TOTAL_DISCREPANCY` |
| C012 | `needs_review`, `UNTRUSTED_INSTRUCTION_DETECTED` |
| negative inputs | `PARSER_CORRUPT_FILE`; `SYNTHETIC_ALLOWLIST_REJECTED` |
| source handling | temporary file deleted; raw file not persisted |
| billing state | Free Trial remained unactivated; **Activate** stayed visible |
| displayed cost | €0 at the recorded checks; reporting may lag |
| teardown | `PASS`; dedicated project `DELETE_REQUESTED` |

The €40 alerts-only budget was deleted through the public Cloud Billing Budget
API. The two Preview spend caps required deletion and absence verification in
the Billing user interface; the final Billing check showed zero course budget
rows. The service was then deleted and cannot be used as a live demo.

The redacted records are in [`evidence`](evidence). They contain no document
text, model output, credential, account email, or Billing account identifier.

After teardown, the final product audit added stricter immutable configuration,
action-to-evidence checks, and repeatable private-access checks. Those
fail-closed changes passed the complete offline suite but were not redeployed
after the dedicated project had entered `DELETE_REQUESTED`. The recorded live
proof therefore proves the Google path used immediately before this final
offline hardening; it is not a hash attestation for every later source line.

## Known limits

- The fake adapter reads born-digital PDF text; only live Document AI proves
  image-only C004 OCR.
- A hash allowlist is appropriate only for a frozen synthetic demonstration.
- Source anchors and fixed checks improve verifiability but do not establish
  legal or factual correctness.
- Human approval here is single-reviewer training control, not production
  segregation of duties.
- Cloud Run scale-to-zero and maximum instances are cost throttles, not an
  exact euro cap.
- Application deletion is not proof of provider-side zero retention.
- The €60 amount is a maximum allocation, not a target or guaranteed technical
  cutoff.

## Current official Google references

- [Cloud Run locations](https://docs.cloud.google.com/run/docs/locations)
- [Document AI regions](https://docs.cloud.google.com/document-ai/docs/regions)
- [Gemini 3.5 Flash-Lite](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash-lite)
- [Vertex AI data residency](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/data-residency)
- [Google Cloud Free Trial](https://docs.cloud.google.com/free/docs/free-cloud-features)
