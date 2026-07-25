# Week 3 — Source Integrity, Private Storage, and Database State

## Outcome

You will ingest actual synthetic files without losing their identity. Each accepted source receives a document ID and SHA-256 hash, is stored privately as an immutable original, appears in a manifest, and advances through database-controlled state. Raw and derived data are separated.

## Beginner checkpoint

Revisit [files and paths](../foundations/01_FILES_AND_TEXT.md),
[small Python functions](../foundations/03_CODE_AND_PYTHON.md), and the database
section of
[n8n, Docker, and databases](../foundations/08_N8N_DOCKER_AND_DATABASES.md).
You should be able to explain file bytes, hash, table, row, primary key,
constraint, object storage, and immutable original.

Do the SHA-256 exercise on one copied synthetic file before writing database
code. Confirm that hashing the same unchanged bytes twice returns the same value
and that changing a copy returns a different value.

Safe AI-assistance request:

```text
Teach me a streaming SHA-256 function for one local synthetic file. Explain
every line, inputs, output, file-reading mode, and failure. Add tests for known
bytes, an empty file, a missing file, and repeated hashing. Do not upload, move,
rename, or delete any file.
```

## Concepts

- byte-level SHA-256 and content identity;
- immutable/original versus derived artifacts;
- MIME sniffing versus filename extension;
- safe filenames and opaque object keys;
- object storage versus relational metadata;
- database constraints, transactions, and row locking;
- tenancy and Row Level Security (RLS);
- retention class versus ad hoc deletion;
- duplicate, version, and related-document semantics;
- source manifest and chain of custody;
- backup scope.

## Official readings

1. [Python `hashlib`](https://docs.python.org/3/library/hashlib.html) — streaming cryptographic hashes.
2. [Supabase Storage access control](https://supabase.com/docs/guides/storage/security/access-control) — private objects and RLS.
3. [Supabase API security](https://supabase.com/docs/guides/api/securing-your-api) — RLS, grants, service-role boundaries.
4. [Supabase Database overview](https://supabase.com/docs/guides/database/overview) — PostgreSQL and backup scope.
5. [Supabase project regions](https://supabase.com/docs/guides/platform/regions) — region selection is a project configuration, not a geographic assumption.
6. [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) and [transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

Record that database backups and object-storage objects can have different coverage. A successful database restore does not by itself prove source files are recoverable.

## Guided build

### 1. Validate before trust

Create a file intake service that:

1. enforces a small maximum byte size;
2. accepts only PDF and DOCX for this capstone;
3. sanitises the display filename;
4. detects file signature/media type rather than trusting extension;
5. computes SHA-256 while streaming bytes;
6. generates `source_id` before object storage;
7. uses an opaque object key such as `tenant/source_id/original`;
8. writes object and metadata with compensating cleanup if one side fails;
9. emits an audit event without raw contents.

The intentionally corrupt PDF should pass only the coarse file-signature step if that matches your policy, then fail safely during parsing. Document the boundary.

### 2. Create the database schema

At minimum:

```sql
create type workflow_state as enum (
  'received', 'validated', 'parsed', 'needs_review',
  'pending_approval', 'approved', 'rejected', 'expired',
  'completed', 'failed_manual'
);

create table source_documents (
  source_id uuid primary key,
  tenant_id text not null,
  sha256 char(64) not null,
  original_filename text not null,
  media_type text not null,
  byte_size bigint not null check (byte_size > 0),
  received_at timestamptz not null,
  storage_uri text not null,
  parser_status text not null default 'not_started',
  retention_class text not null,
  unique (tenant_id, sha256)
);

create table workflow_runs (
  run_id uuid primary key,
  tenant_id text not null,
  current_state workflow_state not null,
  state_version integer not null default 1,
  created_at timestamptz not null,
  updated_at timestamptz not null
);
```

Add join tables because one case can have a quotation and terms, and the shared policy may be referenced rather than duplicated.

Add an append-only `audit_events` table and a database role used by the application that cannot update/delete audit rows. Preserve `previous_event_hash` and `event_hash`.

### 3. Implement transition authority

Write one domain function:

```text
transition(run_id, tenant_id, expected_state, target_state, prerequisites, actor)
```

Within one transaction:

- select the run for update;
- check tenant and expected state/version;
- validate allowed transition and prerequisites;
- insert audit event;
- update current state/version;
- commit.

Test two simultaneous attempts. One must win; the stale one must fail clearly.

### 4. Configure private storage

Create private `source-originals` and `derived-artifacts` buckets. Policies should ensure:

- a tenant can access only its prefix or authorised object rows;
- the browser/anonymous role cannot list originals;
- only the server worker can create immutable source objects;
- derived outputs never overwrite originals;
- service credentials stay in the FastAPI/worker boundary.

The course demo may simulate users with two synthetic tenant identities. Prove cross-tenant denial.

### 5. Generate and verify manifests

For each accepted source, write a manifest entry:

```json
{
  "source_id": "...",
  "tenant_id": "tenant-demo-a",
  "sha256": "...",
  "byte_size": 12345,
  "media_type": "application/pdf",
  "storage_uri": "...",
  "received_at": "...",
  "retention_class": "course-30d",
  "code_commit": "..."
}
```

Download an original through the authorised server, recompute the hash, and compare. Do this after upload and during the Week 12 restoration drill.

### 6. Exercise partial failure

Test:

- object write succeeds, metadata transaction fails;
- metadata reserved, object write fails;
- network response is lost after both succeed;
- same bytes, different filename;
- different bytes, same filename;
- same bytes in another tenant;
- zero-byte file;
- misleading `.pdf` extension;
- oversized input;
- unauthorised cross-tenant read.

Choose explicit compensation or reconciliation for each. Never “retry everything” without checking existing state.

## Capstone increment

Ingest at least:

- one normal PDF quotation;
- one DOCX terms document;
- the shared internal purchasing policy;
- the designated byte-identical duplicate;
- one deliberately corrupt PDF.

The normal files reach `validated`; the duplicate is auditable without creating duplicate work; corrupt handling remains visible. Do not parse yet.

## Required artifact

`artifacts/weekly/week-03/`:

- SQL migrations and rollback notes;
- storage and RLS policy export;
- source-ingestion code and tests;
- raw/derived object-key convention;
- manifest for the five exercised inputs;
- hash verification report;
- partial-failure/reconciliation matrix;
- cross-tenant denial evidence;
- weekly evidence record.

## Test gate

Pass only if:

- recomputed stored-object hashes equal received hashes;
- originals cannot be overwritten through the application path;
- raw and derived objects have distinct buckets/prefixes and IDs;
- same-tenant duplicate bytes do not create a second source/action path;
- same filename with different bytes is not treated as duplicate;
- tenant A cannot read tenant B’s row or object;
- a stale state transition fails;
- partial failures are either compensated or visibly reconcilable;
- audit events cannot be updated/deleted by the application role;
- the backup plan explicitly covers both database and storage objects.

## Common failures

- **Hashing extracted text:** hash exact source bytes first; derived text gets its own hash.
- **Filename as identity:** filenames are untrusted labels and collide.
- **Public bucket during development:** begin private and prove access paths.
- **Service-role key in n8n/browser:** keep it behind the domain API.
- **RLS enabled without policies/tests:** enabled RLS can deny everything or be bypassed by a powerful server key; test actual roles.
- **Object and row assumed atomic:** design compensation/reconciliation across services.
- **Deleting a duplicate silently:** record the attempt and relationship without duplicate work.

## Estimated time

| Activity | Time |
|---|---:|
| Storage/database readings | 1.25 h |
| Schema and transition function | 2.0 h |
| Intake, hashing, object storage | 2.25 h |
| RLS and tenant tests | 1.25 h |
| Failure/reconciliation tests | 1.25 h |
| Evidence and review | 0.75 h |
| **Total** | **8.75 h** |
