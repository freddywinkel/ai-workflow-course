# Retention and Data Boundary

## The honest promise

This demo automatically deletes the application-controlled temporary source
file after every success or failure. It does not claim immediate provider-side
physical erasure or zero retention.

Only the six frozen synthetic Portable Document Format (PDF) files in
`fixtures/manifest.json` are allowed. Never use client, employer,
quality-system, medical, personal, confidential, or otherwise real data.

Approved exports use JavaScript Object Notation (JSON) and comma-separated
values (CSV).

## Data map

| Stage | Data present | Storage behavior |
|---|---|---|
| browser file picker | one synthetic PDF selected by the learner | held by the browser long enough to upload; close/refresh after the decision |
| Cloud Run request | bounded raw bytes | kept only for request processing |
| Cloud Run temporary source | synthetic PDF in the container's memory-backed writable filesystem | deleted in `finally` on success and failure; processing stops if deletion cannot be proved |
| Document AI synchronous request | raw PDF bytes | sent inline to the `eu` endpoint; no Cloud Storage input or output bucket |
| deterministic extraction | text, fields and source anchors | returned in the request result; not written to an application database |
| Gemini request | only source-linked candidate/evidence lines | no raw PDF; candidate identifiers and one finding-bounded action type returned through Vertex AI in `eu` |
| browser review | draft package and signature | held in the active page; no server-side review database |
| approved export | source-linked JSON and CSV | generated only after exact approval and downloaded to the learner's computer |
| Firestore | total runs, total pages, configured limits and update time | no filename, source hash, text, prompt, model output or export |
| Secret Manager | random signing secret | never downloaded into evidence or stored in `.env` for cloud use |
| Cloud Logging | synthetic case identifier, page count, state, provider and safe-stop code | no source text, prompt or model output; `_Default` target retention is one day |
| Artifact Registry | container image | contains application code and frozen allowlist, not uploaded documents |

## Application deletion

The pipeline performs this order:

1. confirm the exact synthetic hash;
2. validate media type, byte size, PDF structure and page count;
3. reserve the bounded usage;
4. create a temporary file on Cloud Run's memory-backed filesystem;
5. call Document AI;
6. delete the temporary file in a `finally` block;
7. verify that the path no longer exists;
8. continue to extraction and Gemini only after deletion succeeds.

Cloud Run instances may be reused between requests. That is why relying only
on instance shutdown is insufficient. The explicit per-request deletion is the
application control. The container filesystem itself is non-persistent when an
instance stops.

`raw_document_storage: false` means this application does not intentionally
persist the raw PDF. It does not prove that every provider copy, transient
memory page, security record, backup, or administrative log vanished
immediately.

## Google provider caveats

### Document AI

- The processor location is `eu` and the endpoint is
  `eu-documentai.googleapis.com`.
- Processing is synchronous with inline raw bytes.
- No Cloud Storage bucket or Document AI dataset is used.
- Google states that customer data is not used to train Document AI models.
- The official documentation does not give this demo a basis to promise
  instantaneous deletion of online input bytes.

### Gemini through Vertex AI

- The location is `eu`; the global endpoint/location is not used.
- The raw PDF is not sent. Gemini receives bounded source-linked candidate
  lines.
- Fixed findings first narrow the action type. Gemini returns candidate
  identifiers and that bounded action type, not free-form summary or action
  prose.
- The application maps those identifiers to verified values and evidence, then
  renders the exact summary sentences and one exact human-review action
  template. It rejects action evidence from a field type unrelated to that
  action.
- Google states it will not train or fine-tune generative models on customer
  data without permission.
- Request-response logging is disabled by default and must remain disabled.
- Do not enable Google Search grounding, Maps grounding, explicit context
  caching, session resumption, or request-response logging.
- Abuse monitoring and isolated in-memory caching may still apply. Google
  documents that default in-memory caching can retain data for up to 24 hours
  unless applicable zero-data-retention controls are enabled.

### Cloud Logging

The deployment attempts to set the `_Default` log bucket to one-day retention.
The `_Required` bucket contains administrative/system logs and has a longer
provider-defined retention period. No document content may be written to
either log.

## Browser and local export responsibility

After a decision:

1. download only an intentionally approved synthetic export;
2. close the application tab;
3. close the authenticated proxy;
4. delete unwanted local downloads through the normal Windows recycle path;
5. keep only metadata evidence needed for learning; and
6. never mix the practice folder with real work.

The application cannot automatically delete a file the learner chose to
download.

## If Cloud Storage is ever added

It is deliberately absent. Adding it changes the privacy claim and requires a
new review. At minimum, a future design would need an European Union location,
explicit object deletion, disabled seven-day soft delete, and a lifecycle rule
only as a delayed failsafe. Cloud Storage lifecycle execution is asynchronous
and is not immediate deletion.

## Teardown boundary

Delete the Cloud Run service, Document AI processor, Artifact Registry
repository, signing secret, runtime service account, Firestore counter
database, and dedicated project. Disable application programming interfaces
only after stored resources are deleted: disabling an interface does not
delete its data.

Project deletion has a recovery period, and billing/log records can remain
under Google retention rules. Report resource unavailability, not instant
physical erasure.

## Current official Google references

- [Document AI security](https://docs.cloud.google.com/document-ai/docs/security)
- [Document AI regional processing](https://docs.cloud.google.com/document-ai/docs/regions)
- [Document AI synchronous request](https://docs.cloud.google.com/document-ai/docs/send-request)
- [Cloud Run container filesystem](https://docs.cloud.google.com/run/docs/container-contract)
- [Cloud Run temporary-file guidance](https://docs.cloud.google.com/run/docs/tips/general)
- [Vertex AI zero-data-retention guidance](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/zero-data-retention)
- [Vertex AI request-response logging](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/request-response-logging)
- [Cloud Logging retention](https://docs.cloud.google.com/logging/quotas)
- [Cloud Storage soft delete](https://docs.cloud.google.com/storage/docs/soft-delete)
- [Cloud Storage lifecycle timing](https://docs.cloud.google.com/storage/docs/lifecycle)
