# Advanced Capstone — Controlled Document Intake on Google Cloud

## What this is in normal human language

This is an optional, advanced build that comes after Course 1. It proves that
the controlled-workflow ideas from Course 1 can be moved from local practice
files to a small private cloud demonstration.

You build a working intake screen for fictional supplier quotations:

1. the application accepts only six exact made-up training documents;
2. Google Document AI reads a Portable Document Format (PDF) file;
3. fixed Python code extracts named fields and binds them to exact source text;
4. Gemini 3.5 Flash-Lite, reached through the Gemini Enterprise Agent Platform
   application programming interface that Google previously called the Vertex
   AI API, selects identifiers from a small list of verified candidates and
   selects one human-review action type already allowed by fixed findings;
5. fixed Python code turns those selections into exact source-linked summary
   wording and an exact action template, and rejects an unknown selection or
   an action linked to an unrelated source field;
6. a human reviews the exact output;
7. only an approved output can be downloaded as comma-separated values (CSV)
   and JavaScript Object Notation (JSON);
8. the temporary file is deleted after every success or failure; and
9. the private cloud resources are torn down after the live proof.

Artificial intelligence (AI) is used for bounded selection, not for writing
free-form instructions or exercising authority.
Optical character recognition (OCR) turns characters in an image or PDF into
machine-readable text. An application programming interface (API) is the
defined way one program asks another program to do something. Google Cloud Run
hosts the private web application and scales down to zero running instances
when unused.

Google [renamed Vertex AI Platform and Generative AI on Vertex AI in April
2026](https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes).
This course still says “Gemini through Vertex AI” where it helps you recognise
older material, but the current software flag is `enterprise=True`. Treat
cloud product names as updateable labels, not as the durable skill.

## Why it is not the Course 1 final project

Course 1 remains the beginner foundation and keeps its local Synthetic Small
and Medium-sized Enterprise (SME) Operations Exception Assistant. This cloud
lab belongs to the proposed Course 4, Controlled Document AI Systems.

It is bundled now because it provides a real advanced capstone and preserves
the longer career sequence. It does **not** mean:

- Course 4 is fully taught;
- you are ready for production or regulated systems;
- the demo may receive employer, client, medical, personal, or confidential
  material;
- a model output may approve, select, contact, pay, send, or update anything;
- a budget alert is a guaranteed spending stop; or
- provider-side instantaneous deletion or zero retention has been proved.

Reading is allowed after Course 1. Run the cloud part only after you understand
the Application Programming Interface (API), identity, deployment, rollback,
and client-owned-environment skills proposed for Course 3.

## Architecture

```text
[Browser holding one allowlisted synthetic PDF]
                     |
                     v
[Private Cloud Run service — Netherlands, europe-west4]
                     |
         [hash, type, size, page and cost gates]
                     |
          +----------+-----------+
          |                      |
          v                      v
[Document AI OCR — eu]   [Firestore counters only]
          |
          v
[fixed fields + exact page/text evidence]
          |
          v
[Gemini 3.5 Flash-Lite — eu, bounded candidate identifiers + allowed action type]
          |
          v
[fixed wording + citation, finding and action-evidence checks]
          |
          v
[human decision bound to exact SHA-256 hash]
          |
          v
[local CSV/JSON download, only after approval]
```

Secure Hash Algorithm 256-bit (SHA-256) creates a stable fingerprint. The raw
PDF is never written to Cloud Storage or Firestore. Firestore stores only total
run and page counters so the application can enforce a lifetime prototype
allowance.

## Permanent controls and replaceable technology

The replaceable parts are the model name, provider software development kit
(SDK), and cloud screen labels. They are replaceable only through a reviewed,
tested course release; the live prototype rejects a learner-side model or
deadline change. An SDK is a software library supplied to help code call a
service.

The durable parts are:

- a narrow intended purpose;
- exact synthetic-document allowlisting;
- source hashes and locators;
- deterministic field and arithmetic checks;
- schema validation around model output;
- meaningful human approval;
- approval bound to exact bytes;
- export and external-action restrictions;
- failure states and manual fallback;
- measured evaluation;
- cost and date stops;
- deletion and teardown proof.

When a model changes, keep these controls and rerun the frozen tests.

## Working implementation

The runnable source is in
[`controlled_document_intake_demo`](../future_courses/course_04_controlled_document_ai/controlled_document_intake_demo/README.md).
The frozen synthetic corpus remains in
[`source_material/corpus`](../future_courses/course_04_controlled_document_ai/source_material/corpus/README.md).

The application includes:

- a private web user interface;
- offline fake provider adapters;
- Google Document AI and Gemini adapters;
- a six-file SHA-256 allowlist;
- a Firestore transaction for total run/page caps;
- signed review packages;
- approved-only CSV and JSON exports;
- deployment, live-verification, and teardown scripts; and
- automated tests.

## Lesson order

1. [Readiness, data boundary, and €60 gate](00_READINESS_COST_GATE.md)
2. [Run the complete workflow locally](01_LOCAL_BASELINE.md)
3. [Protect source integrity and call Document AI safely](02_SOURCE_INTEGRITY_DOCUMENT_AI.md)
4. [Create exact evidence-linked fields](03_EVIDENCE_LINKED_EXTRACTION.md)
5. [Use Gemini for bounded candidate selection](04_GEMINI_SUMMARIES_ACTIONS.md)
6. [Require exact-output human approval and exports](05_HUMAN_APPROVAL_EXPORTS.md)
7. [Test and attack the whole workflow](06_TESTS_AND_EVALUATION.md)
8. [Deploy privately with cost controls](07_CLOUD_RUN_DEPLOYMENT.md)
9. [Run the live acceptance proof](08_LIVE_VALIDATION.md)
10. [Delete resources and prove teardown](09_TEARDOWN.md)

## Completion boundary

Complete means:

- every offline test passes;
- the private Google path processes the selected frozen synthetic cases;
- Document AI and Gemini both appear in observed live evidence;
- every draft statement cites a real evidence identifier;
- a changed package invalidates approval;
- rejected or unchecked output cannot export;
- CSV and JSON exports are created after one human approval;
- temporary deletion is proved after success and failure;
- actual live counts and export hashes are recorded without document text;
- the account remains a non-paid Free Trial;
- the live service is torn down; and
- the Course 1 progressive web app (PWA), an installable offline-capable
  website, still passes its existing contract.

This is portfolio evidence for a synthetic private demonstration. It is not
client deployment approval.

## Recorded reference result — 28 July 2026

The bundled reference implementation was deployed and validated once before it
was torn down. The metadata-only evidence records show:

- live result `PASS` through a private Identity and Access Management
  (IAM)-protected Cloud Run service in `europe-west4`;
- health metadata obtained from `/api/health`;
- Document AI and Vertex AI both configured for `eu`;
- C001 and C004 at `pending_approval`, each with 14 fields and 14 evidence
  links;
- C008 at `needs_review` with `TOTAL_DISCREPANCY`;
- C012 at `needs_review` with `UNTRUSTED_INSTRUCTION_DETECTED`;
- corrupt input stopped with `PARSER_CORRUPT_FILE` and an unknown hash stopped
  with `SYNTHETIC_ALLOWLIST_REJECTED`;
- one approved C001 CSV and JSON export represented by hashes only;
- temporary-file deletion reported true and raw-file persistence false for
  every live case;
- the account remained an unactivated Free Trial; the Billing screen displayed
  €0 at the recorded checks, but that amount can lag and is not a final-cost
  claim; and
- teardown result `PASS`, with the dedicated project in `DELETE_REQUESTED`.

The ordinary €40 alerts-only budget was deleted through the public Cloud
Billing Budget application programming interface. The two Preview spend caps
required deletion and absence verification in the Billing user interface.
After verification, no course budget rows remained. The live service is
therefore no longer available.

The final product audit then added stricter immutable Google-mode settings,
action-to-evidence checks, and repeatable private-access checks. The full
offline suite passed, but those fail-closed changes were not redeployed after
the dedicated project entered `DELETE_REQUESTED`. The dated records prove the
Google path immediately before that final offline hardening; they are not a
source-hash attestation for every later line.

The supporting records are
[`cloud_deployment_validation.json`](../future_courses/course_04_controlled_document_ai/controlled_document_intake_demo/evidence/cloud_deployment_validation.json),
[`live_validation.json`](../future_courses/course_04_controlled_document_ai/controlled_document_intake_demo/evidence/live_validation.json),
and
[`teardown_validation.json`](../future_courses/course_04_controlled_document_ai/controlled_document_intake_demo/evidence/teardown_validation.json).
