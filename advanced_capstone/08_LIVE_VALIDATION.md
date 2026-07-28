# Capstone Lab 8 — Prove the Real Private Cloud Path

## Outcome

You will run the guarded live acceptance script against the private service
with a short-lived identity token. It will exercise Google Document AI and
Gemini through Vertex AI with only frozen synthetic files. You will then use an
authenticated local proxy to recreate one manual review with a different
synthetic case.

The validation report stores states, counts, provider names, hashes, and
deletion flags. It deliberately stores no source text, prompt, model output,
credential, or real data.

The report format is JavaScript Object Notation (JSON). An approved result can
also be downloaded as comma-separated values (CSV).

Run this lesson and Lab 9 teardown in the same work session.

## Recorded reference result — actual PASS

The bundled metadata report was created by the real private service on
28 July 2026. Its observed result was `PASS`:

| Synthetic check | Observed result |
|---|---|
| C001 | `pending_approval`; 14 fields; 14 evidence links; approved CSV/JSON hashes recorded |
| C004 | `pending_approval`; 14 fields; 14 evidence links |
| C008 | `needs_review`; `TOTAL_DISCREPANCY` |
| C012 | `needs_review`; `UNTRUSTED_INSTRUCTION_DETECTED` |
| corrupt fixture | `PARSER_CORRUPT_FILE` |
| unknown hash | `SYNTHETIC_ALLOWLIST_REJECTED` |

For all four successful provider cases, the report recorded one page,
temporary-file deletion `true`, raw-file persistence `false`, provider mode
`google`, and model `gemini-3.5-flash-lite`. Document AI and Vertex AI were
both in `eu`. Cloud Run remained private in `europe-west4`.

Gemini selected candidate identifiers and one allowed action type. The
application, not Gemini, rendered the exact summary and action wording.

The final offline product audit strengthened the repeatable verifier after this
recorded run: it now checks the Cloud Run Identity and Access Management (IAM)
policy for public members and requires an unauthenticated request to return
`401` or `403` before minting a token. The dated report predates those two new
fields, and the deleted project was not recreated merely to rewrite evidence.

## Follow along — I show you exactly how

### Step 1 — Put a frozen corpus beside the practice demo

The live script expects `source_material` beside the copied `demo` folder.
Open Windows PowerShell:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$capstoneRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\controlled-intake-capstone'
$demoRoot = Join-Path $capstoneRoot 'demo'
$sourceMaterialSource = Join-Path $courseRoot 'future_courses\course_04_controlled_document_ai\source_material'
$sourceMaterialCopy = Join-Path $capstoneRoot 'source_material'
if (-not (Test-Path -LiteralPath $sourceMaterialCopy)) {
    Copy-Item -LiteralPath $sourceMaterialSource -Destination $sourceMaterialCopy -Recurse
}
Test-Path -LiteralPath (Join-Path $sourceMaterialCopy 'corpus\cases\C001\quotation.pdf')
```

Expected result: `True`. This copies course-owned synthetic files only. It does
not copy a credential.

### Step 2 — Re-check the irreversible gates

Run:

```powershell
$projectId = Read-Host 'Enter the dedicated controlled-intake project ID'
if ($projectId -notmatch '^controlled-intake-[a-z0-9-]{4,40}$') {
    throw 'Project ID refused.'
}
Set-Location -LiteralPath $demoRoot
```

Now open the Google Cloud Billing page and verify again:

- it says **Free trial**;
- the **Activate** button remains visible;
- paid activation is still `NO`;
- the €40 alerts still exist;
- available €5 service spend caps still exist; and
- the date is before 20 October 2026.

Stop if any answer is uncertain. Never click **Activate**.

### Step 3 — Understand what the script will call

Read without editing:

```powershell
notepad .\scripts\verify_live.ps1
notepad .\scripts\verify_live.py
```

The script will:

1. inspect the Cloud Run IAM policy and reject `allUsers` or
   `allAuthenticatedUsers`;
2. call `/api/health` without a token and require `401` or `403`;
3. mint a short-lived token for the signed-in learner;
4. call the private `/api/health` endpoint and confirm provider mode `google`;
5. confirm Document AI `eu`, Vertex AI `eu`, and the configured model;
6. process C001, C004, C008, and C012;
7. approve and hash exports for C001;
8. verify C008 and C012 route to review;
9. verify corrupt C010 and a changed hash stop before providers;
10. prove changed packages and unresolved findings cannot export;
11. verify temporary-file deletion flags; and
12. write metadata-only `evidence\live_validation.json`.

The health path is `/api/health`, not `/healthz`.

The learner has private invoker access for the lab. The script creates no key
file and removes the short-lived token from the process environment. This is a
development-only test method; do not reuse it as a production identity design.

### Step 4 — Run the guarded live proof once

Run:

```powershell
$trialConfirmation = 'FREE TRIAL CONFIRMED - DO NOT ACTIVATE'
$lessonFolder = Join-Path $capstoneRoot 'evidence\live-validation'
New-Item -ItemType Directory -Force -Path $lessonFolder | Out-Null

& .\scripts\verify_live.ps1 `
    -ProjectId $projectId `
    -FreeTrialConfirmation $trialConfirmation |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_live_validation_output.txt')
```

Expected result: a JSON message containing `"result": "PASS"`. If it fails,
do not rerun repeatedly. Save the failure and proceed to teardown.

Copy the metadata report:

```powershell
$liveReportSource = Join-Path $demoRoot 'evidence\live_validation.json'
if (-not (Test-Path -LiteralPath $liveReportSource)) {
    throw 'The live validation report is missing. Do not claim PASS.'
}
Copy-Item -LiteralPath $liveReportSource `
    -Destination (Join-Path $lessonFolder 'worked_live_validation.json') `
    -Force
```

### Step 5 — Verify the report without exposing document content

Run:

```powershell
$report = Get-Content -Raw -LiteralPath (Join-Path $lessonFolder 'worked_live_validation.json') |
    ConvertFrom-Json
$report.result
$report.data_boundary
$report.service | Format-List
$report.cases | Format-Table case_id,state,page_count,provider_mode,model_id,temporary_file_deleted,raw_file_persisted
$report.negative_tests | Format-List
$report.approved_export_evidence | Format-List
```

Expected result:

- report `PASS`;
- synthetic-only boundary;
- provider mode `google`;
- Document AI and Vertex AI locations `eu`;
- model `gemini-3.5-flash-lite`;
- C001 and C004 `pending_approval`;
- C008 `needs_review` with `TOTAL_DISCREPANCY`;
- C012 `needs_review` with `UNTRUSTED_INSTRUCTION_DETECTED`;
- temporary deletion `True`;
- raw persistence `False`;
- corrupt and unknown-hash safe stops; and
- approved C001 CSV/JSON hashes, not their contents.

### Step 6 — Re-check usage and billing

Open Billing reports and the application budget after the proof. Record the
displayed cost and usage time in:

```powershell
notepad (Join-Path $lessonFolder 'worked_post_validation_cost_check.md')
```

Do not claim the displayed amount is final because Google Cloud billing data
can arrive later. Do not paste a billing account identifier.

In the recorded reference run, the Billing screen displayed €0 and still
showed **Free trial** plus **Activate**. Paid activation remained `NO`. That €0
is a timestamped screen value, not proof that later settled usage will also be
zero.

## Now recreate it yourself

Perform one manual live review with frozen C006, which the automated live script
did not process.

In Windows PowerShell run:

```powershell
gcloud run services proxy controlled-document-intake `
    --project=$projectId `
    --region=europe-west4 `
    --port=8088
```

Leave that window open. In a second PowerShell window run:

```powershell
Start-Process 'http://127.0.0.1:8088'
```

In the private application:

1. select `$sourceMaterialCopy\corpus\cases\C006\quotation.pdf`;
2. confirm it is synthetic;
3. process it once;
4. confirm state `needs_review`;
5. inspect the missing `valid_until` field and its finding;
6. inspect at least two real evidence links;
7. choose `Needs correction`;
8. use fictional alias `reviewer-demo-02`;
9. confirm source review;
10. record the decision; and
11. confirm no export appears.

Close the browser tab and press `Ctrl+C` in the proxy window.

Create:

```powershell
notepad (Join-Path $lessonFolder 'recreated_live_c006.md')
```

Record only:

- case `C006`;
- provider mode `google`;
- state;
- finding code, without source text;
- number of evidence links inspected;
- temporary-file-deleted flag;
- raw-file-persisted flag;
- decision;
- export present `YES/NO`;
- external action present `YES/NO`; and
- time of the post-run Billing check.

Do not paste source text, model output, a filename containing a real identity,
an account email, a project billing identifier, or a credential.

## Ask Codex to check your work

Run `(Resolve-Path $lessonFolder).Path`, paste it, and send:

```text
READ-ONLY LIVE-ACCEPTANCE EVIDENCE REVIEW.

Inspect only this full local folder:
[PASTE FULL PATH]

Do not edit, delete, rename, upload, deploy, call Google Cloud, access a
secret, open Billing, or rerun validation. Stop for credentials, billing
account identifiers, account emails, source text, model output, or real data.

Return PASS or NOT YET for: automated report result PASS; provider mode google;
no public Identity and Access Management members; unauthenticated status 401 or
403; Document AI eu; Vertex AI eu; current model; expected states for C001,
C004, C008 and C012; corrupt and changed-hash safe stops; source-linked output;
temporary deletion true; raw persistence false; approved C001 export hashes
exist; C006 recreation needs_review with MISSING_FIELD:valid_until, needs
correction and no export; post-run cost check recorded as possibly delayed;
teardown still required. Cite filenames without reproducing identifiers or
content.
```

## Pass criteria

- The guarded live script passes once.
- Document AI and Gemini are both evidenced in the live path.
- Only frozen synthetic allowlisted files are accepted.
- Every summary item has source evidence.
- C001 approval produces export hashes.
- C008, C012, and manual C006 route to review.
- C010 and the changed file stop safely.
- Temporary deletion is reported for success and failure.
- The policy has no public member and an unauthenticated request is rejected.
- Post-run cost was checked without claiming finality.
- Codex returns PASS.
- You proceed immediately to Lab 9.

## Stop conditions

On any failure, do not weaken a guard and do not keep retrying paid-capable
calls. Preserve metadata-only failure evidence and proceed to teardown. Stop
immediately for real data, paid activation, ambiguous billing, an unknown
model, a non-European Union endpoint, or a missing deletion proof.

## Current official Google references

- [Authenticated Cloud Run service proxy](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/proxy)
- [Document AI synchronous processing](https://docs.cloud.google.com/document-ai/docs/send-request)
- [Document AI response anchors](https://docs.cloud.google.com/document-ai/docs/handle-response)
- [Vertex AI European Union data residency](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/data-residency)
- [Cloud Billing reports](https://docs.cloud.google.com/billing/docs/how-to/reports)
