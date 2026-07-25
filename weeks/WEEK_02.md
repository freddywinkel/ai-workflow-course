# Week 2 — APIs and Reliable Non-AI Orchestration

## Outcome

You will build a reliable n8n intake-to-log workflow using only synthetic JSON and a small FastAPI service. It will authenticate, validate, branch, retry only safe operations, preserve a trace ID, and route exhausted failures visibly. No model call occurs this week.

## Beginner checkpoint

This is the first coding week. Revisit
[PowerShell](../foundations/02_COMMAND_LINE_SURVIVAL.md),
[Python](../foundations/03_CODE_AND_PYTHON.md),
[APIs and JSON](../foundations/04_WEB_APIS_AND_JSON.md), and
[n8n/Docker/databases](../foundations/08_N8N_DOCKER_AND_DATABASES.md).

Before building, you should be able to point to the method, URL, headers, body,
and status code in a fictional HTTP exchange and explain object, array, string,
Boolean, and null in JSON. Build one endpoint and one workflow branch at a
time. After every generated function, fill one
[AI assistance log](../templates/ai_assistance_log.md).

Safe AI-assistance request:

```text
Teach me one FastAPI endpoint only: POST /v1/intake/metadata. First explain the
request and response JSON. Then propose the smallest Pydantic models, endpoint,
and tests. Do not add a database, AI call, file upload, or other endpoint.
```

## Concepts

- JSON objects, arrays, nulls, types, and JSON Schema;
- HTTP methods, URLs, headers, status families, timeouts, and request IDs;
- authentication versus authorization;
- synchronous response versus asynchronous work;
- retryable versus permanent errors;
- exponential backoff and jitter;
- idempotency;
- webhook validation;
- correlation/trace IDs;
- orchestration versus domain logic;
- credentials as managed secrets;
- dead-letter/manual route.

## Official readings

1. [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) — requests, response models, validation, errors.
2. [n8n HTTP Request node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/) — credentials, response handling, timeout/retry options.
3. [n8n error handling](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully) — error workflows and execution behaviour.
4. [n8n execution data](https://docs.n8n.io/workflows/executions/all-executions/) — execution retention and retry considerations.
5. [MDN HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) — use as the protocol reference.

Note the n8n operational warning: workflow execution history is not your domain audit ledger, and deleting a workflow can affect its associated execution history. Export required evidence separately.

## Guided build

### 1. Define the API envelope

Create Pydantic request/response models:

```json
{
  "request_id": "UUID",
  "tenant_id": "tenant-demo-a",
  "received_at": "RFC3339 UTC",
  "document": {
    "filename": "quote.pdf",
    "media_type": "application/pdf",
    "byte_size": 12345
  }
}
```

Response:

```json
{
  "request_id": "same UUID",
  "trace_id": "server UUID",
  "accepted": true,
  "state": "received",
  "reason_code": null
}
```

Use enumerated reason codes such as `UNSUPPORTED_MEDIA_TYPE`, `FILE_TOO_LARGE`, `INVALID_TENANT`, and `DUPLICATE_REQUEST`.

### 2. Build FastAPI endpoints

Implement:

- `GET /health`;
- `POST /v1/intake/metadata`;
- `GET /v1/runs/{run_id}`;
- a test-only failure endpoint that can return 400, 401, 409, 429, 500, or sleep beyond timeout.

Rules:

- 400/401/403/404/409 validation conflicts are not blindly retried;
- 429 and transient 5xx may be retried with a capped policy;
- every response has `request_id` or `trace_id`;
- exception responses expose a safe reason, never a stack trace or secret;
- domain validation lives in Python, not scattered n8n expressions.

### 3. Create the n8n workflow

Nodes:

1. Manual Trigger or localhost webhook.
2. Set/Edit Fields: build the synthetic envelope.
3. Code or expression: generate/request a UUID if absent.
4. IF/Switch: reject missing required envelope values before HTTP.
5. HTTP Request: call FastAPI with a credential reference.
6. Switch on result:
   - accepted;
   - permanent rejection;
   - transient failure;
   - unexpected response.
7. Wait/backoff and retry transient failures up to the declared cap.
8. Success log.
9. Manual-failure queue/log.

Do not use an AI Agent node. Do not write database rows directly from n8n.

### 4. Make retries observable

Record per attempt:

- trace and request IDs;
- attempt number;
- endpoint class, not secret query strings;
- status/reason code;
- start/end UTC;
- latency;
- next retry time;
- final route.

Do not log request bodies containing source text.

### 5. Test HTTP behaviour

Use pytest with FastAPI’s test client or `httpx`:

- schema-valid request → 202/accepted;
- missing tenant → 422 or declared 400;
- unsupported media type → permanent rejection;
- same request ID twice → same run or explicit conflict, not two runs;
- simulated 429 twice then success → exactly three attempts;
- 500 beyond cap → visible manual route;
- timeout → visible manual route;
- malformed server JSON → visible manual route;
- lost client response followed by retry → one accepted run.

Keep a stub clock or reduce retry delays in tests.

### 6. Export reproducibly

Export the redacted n8n workflow JSON to `n8n/intake-to-log.json`. Review it for embedded headers, credentials, instance URLs, personal email addresses, and execution payloads. Add a Markdown node or companion README explaining credentials and environment variables required to import it.

## Capstone increment

The capstone can now accept a synthetic metadata envelope, create a run in `received`, return a trace ID, and safely distinguish permanent from transient failures. The file bytes are still a test fixture; Week 3 adds authoritative hashing and storage.

Create failure injection parameters only in `test`, never in `demo` or future production configuration.

## Required artifact

`artifacts/weekly/week-02/`:

- API envelope JSON Schema;
- OpenAPI export from FastAPI;
- redacted n8n workflow JSON;
- workflow README/node map;
- retry matrix;
- automated HTTP test report;
- screenshots or execution exports for success, permanent error, recovered retry, and exhausted retry;
- weekly evidence record.

## Test gate

Pass only if:

- malformed JSON cannot enter `received`;
- a repeated request cannot create two runs;
- retries occur only for declared transient errors;
- the final route is visible after exhausted retries;
- all branches preserve trace/request IDs;
- credentials are references, not workflow values;
- logs contain no source text, tokens, keys, or stack traces;
- a fresh n8n import can call the local API after following the README;
- model/API AI functionality is absent.

## Common failures

- **Retrying 400-series failures:** distinguish caller correction from transient service recovery.
- **Using n8n execution ID as business ID:** generate domain request/run IDs and persist them independently.
- **Business rules in IF nodes:** centralise them in tested Python functions; n8n routes on reason codes.
- **No timeout:** set connect/read/overall limits and test them.
- **Credential embedded in header expression:** use n8n credentials and inspect exported JSON.
- **Duplicate after lost response:** make intake idempotent before adding file storage.
- **Error workflow without original trace ID:** pass a minimal error context explicitly.

## Estimated time

| Activity | Time |
|---|---:|
| HTTP/JSON readings and exercises | 1.5 h |
| FastAPI envelope and endpoints | 2.0 h |
| n8n workflow | 2.25 h |
| Retry/failure tests | 1.75 h |
| Export, secret review, evidence | 1.0 h |
| **Total** | **8.5 h** |
