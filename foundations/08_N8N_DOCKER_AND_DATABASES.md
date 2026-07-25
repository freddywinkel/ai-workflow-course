# Foundation 8 — n8n, Docker, and Databases

## Outcome

You can explain where each course component runs, what it stores, and how to
tell configuration from durable application evidence.

## n8n

n8n is a visual workflow orchestrator. A **node** performs one step. A
connection passes data to another node. A trigger starts a workflow.

Examples:

- Manual Trigger starts a learning run.
- HTTP Request calls the FastAPI service.
- Switch selects a route from a declared reason code.
- Wait pauses before a retry or approval timeout.

Visual does not mean code-free. Expressions, credentials, request bodies,
branches, and retry settings are still software behaviour. Export the workflow
and test it.

n8n execution history helps operate the workflow, but it is not the capstone's
authoritative audit ledger. History settings or workflow deletion can change
what remains visible.

## Docker

A Docker **image** is a packaged filesystem and startup definition. A
**container** is a running instance of an image. A **volume** keeps selected
data when a container is replaced. Docker Compose describes related services
in YAML.

Useful mental model:

```text
docker-compose.yml  → recipe
image               → packaged appliance
container           → running appliance
volume              → durable cupboard
port                → numbered door
```

`docker compose up -d` starts services in the background. `docker compose ps`
shows their state. `docker compose logs` shows operational output. Recreating a
container is not the same as deleting its named volume, but never assume data
is backed up until you perform a restoration test.

The course binds n8n to `127.0.0.1`, which means local access only. Do not expose
it to the public internet for the capstone.

## FastAPI

FastAPI is the Python web framework used to expose the capstone's domain rules
as local API endpoints. n8n orchestrates; FastAPI validates and applies the
rules. This keeps critical rules testable rather than scattered through visual
expressions.

## Database and object storage

A relational database contains tables, rows, columns, keys, and constraints:

```text
table: extraction_runs
row: one extraction attempt
column: parser_version
primary key: unique run ID
foreign key: source-document ID
```

A transaction groups changes so they succeed or fail together. A constraint
prevents invalid database states. PostgreSQL is the database engine used here.

Object storage holds files. The course stores immutable originals separately
from derived text, chunks, and drafts. The database stores their metadata and
relationships.

Supabase supplies managed PostgreSQL and object storage. Row Level Security
(RLS) adds database policies that restrict which rows a user or tenant may
access. A powerful service-role credential can bypass normal policies, so keep
it server-side and test less-privileged access separately.

## How the pieces communicate

```text
synthetic file
    ↓
n8n trigger and routing
    ↓ HTTP request
FastAPI validation and domain rules
    ↓
private object storage + PostgreSQL state
    ↓
parser/OCR and model adapters
    ↓
FastAPI validation, approval, and audit
    ↓
n8n pause or draft-only connector
```

Git tracks code, configuration examples, schemas, tests, and redacted workflow
exports. Git must not track real `.env` files, secrets, database contents,
source originals, or generated private artifacts.

## Dashboard changes versus reproducible changes

Clicking in n8n or Supabase can change behaviour. Record and export the result:

- n8n: redacted workflow JSON plus import instructions;
- database: SQL migration, not only a dashboard screenshot;
- storage: documented bucket policies and automated tests;
- credentials: names and setup instructions, never the values;
- versions: exact image/package/model configuration.

Another person must be able to reproduce the demo without your remembered
clicks.

## Chapter check

Draw the architecture on paper and label:

- which component orchestrates;
- where deterministic rules live;
- where original files live;
- where state and audit records live;
- what Docker adds;
- what Git tracks and must not track.

You pass when you can explain the drawing without vendor marketing language.

