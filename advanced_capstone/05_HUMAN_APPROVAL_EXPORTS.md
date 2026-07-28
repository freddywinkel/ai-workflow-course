# Capstone Lab 5 — Bind Human Approval to the Exact Output

## Outcome

You will prove that “a human is involved” is not enough. The reviewer must
inspect the source links, decide on one exact proposal, and receive exports
only when that exact proposal is approved.

The application creates a Secure Hash Algorithm 256-bit (SHA-256) proposal
fingerprint and a keyed signature. If any field changes after review, the
signature no longer matches. An unchecked, rejected, or correction-needed
proposal produces no comma-separated values (CSV) or JavaScript Object
Notation (JSON) export.

The exact package expires after 30 minutes. A package with unresolved findings
cannot be approved, and CSV cells that could be interpreted as spreadsheet
formulas are neutralised before export.

## Follow along — I show you exactly how

### Step 1 — Run the approval controls

Open Windows PowerShell:

```powershell
$capstoneRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\controlled-intake-capstone'
$demoRoot = Join-Path $capstoneRoot 'demo'
$lessonFolder = Join-Path $capstoneRoot 'evidence\human-approval'
New-Item -ItemType Directory -Force -Path $lessonFolder | Out-Null
Set-Location -LiteralPath $demoRoot
& .\.venv\Scripts\Activate.ps1
$env:PROVIDER_MODE = 'fake'
python -m pytest .\tests\test_pipeline.py `
    -k "exact_output_change or reject_and_unchecked_review or expired_exact_package or unresolved_findings or csv_export_neutralises" `
    -vv |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_approval_tests.txt')
if ($LASTEXITCODE -ne 0) { throw 'The worked approval tests failed.' }
```

Expected result: all five selected tests pass.

They prove these separate controls:

- a changed package produces `PACKAGE_CHANGED_AFTER_REVIEW`;
- an unchecked source review produces `SOURCE_REVIEW_REQUIRED`; and
- a rejected or correction-needed package produces no exports;
- an expired package produces `REVIEW_WINDOW_EXPIRED`;
- a package with findings produces `PACKAGE_NOT_APPROVABLE`; and
- formula-like spreadsheet cells are neutralised.

### Step 2 — Inspect the fixed approval code

Run:

```powershell
notepad .\src\controlled_intake\pipeline.py
notepad .\src\controlled_intake\exports.py
notepad .\src\controlled_intake\schemas.py
```

Find:

- `_sign` and `_verify_signature`;
- `source_links_checked`;
- the three decisions `approved`, `rejected`, and `needs_correction`;
- `approved_for_export`; and
- `review_expires_at`;
- `create_exports`; and
- `_safe_csv_cell`.

Close all three files without editing them.

### Step 3 — Approve the worked C001 output

Start the local application:

```powershell
python -m uvicorn controlled_intake.main:app --app-dir .\src --host 127.0.0.1 --port 8080 --no-access-log
```

Open a second PowerShell window:

```powershell
Start-Process 'http://127.0.0.1:8080'
```

In the application:

1. select the frozen C001 `quotation.pdf`;
2. confirm that it is a synthetic course fixture;
3. process it;
4. inspect every field, finding, summary statement, and proposed action;
5. open enough source links to confirm the claimed text;
6. confirm there are no unresolved findings;
7. finish the review before the displayed 30-minute expiry;
8. choose `Approve exact export`;
9. use the fictional alias `reviewer-demo-01`;
10. tick the source-review confirmation;
11. record the decision; and
12. download both formats.

Move the two downloads into:

```powershell
$workedFolder = Join-Path $lessonFolder 'worked-c001'
New-Item -ItemType Directory -Force -Path $workedFolder | Out-Null
explorer $workedFolder
```

Use File Explorer to move only the two synthetic C001 exports into that folder.
Do not move a real document there.

### Step 4 — Compare the two exports

Run:

```powershell
$jsonFile = Get-Item -LiteralPath (Read-Host 'Paste the full path to the worked C001 JSON export')
$csvFile = Get-Item -LiteralPath (Read-Host 'Paste the full path to the worked C001 CSV export')
Get-FileHash -LiteralPath $jsonFile.FullName -Algorithm SHA256
Get-FileHash -LiteralPath $csvFile.FullName -Algorithm SHA256
$json = Get-Content -Raw -LiteralPath $jsonFile.FullName | ConvertFrom-Json
$rows = Import-Csv -LiteralPath $csvFile.FullName
$json.package.case_id
$json.approval.decision
$json.approval.approved_for_export
$rows | Select-Object -First 3 field_name,value,decision,proposal_hash
```

Expected result:

- case `C001`;
- decision `approved`;
- `approved_for_export` is `True`;
- both formats contain the same proposal hash; and
- the CSV has one row per extracted field.

Save a comparison that does not copy source text:

```powershell
@"
# Worked C001 exact-output approval

JSON SHA-256: $((Get-FileHash $jsonFile.FullName -Algorithm SHA256).Hash)
CSV SHA-256: $((Get-FileHash $csvFile.FullName -Algorithm SHA256).Hash)
Case: $($json.package.case_id)
Decision: $($json.approval.decision)
Approved for export: $($json.approval.approved_for_export)
Proposal hash: $($json.package.proposal_hash)
CSV row count: $($rows.Count)
Source links checked: $($json.approval.source_links_checked)
Data boundary: synthetic course fixture only
"@ | Set-Content -LiteralPath (Join-Path $workedFolder 'worked_approval_comparison.md')
```

Close the browser and press `Ctrl+C` in the server window.

## Now recreate it yourself

Start the local app again and complete two different decisions:

1. Process C006. Inspect its missing-field finding, choose
   `Needs correction`, use `reviewer-demo-02`, confirm source review, and
   record the decision.
2. Process C001 again. Inspect it, choose `Reject`, use
   `reviewer-demo-03`, confirm source review, and record the decision.

Create:

```powershell
notepad (Join-Path $lessonFolder 'recreated_nonapproval_paths.md')
```

In your own words, record for each run:

- case identifier;
- observed workflow state;
- decision;
- whether source links were checked;
- whether `approved_for_export` was true or false;
- whether download buttons appeared; and
- why that result is correct.

Do not save or fabricate an export for either non-approved decision. Stop the
local server when finished.

## Ask Codex to check your work

Run `(Resolve-Path $lessonFolder).Path`, paste the returned path, and send:

```text
READ-ONLY EXACT-APPROVAL REVIEW.

Inspect only:
[PASTE FULL PATH]

Do not edit, create, delete, rename, upload, install, or run a server. Do not
open files outside this folder. Stop for credentials or any real, personal,
health, employer, or client data.

Check: all five focused tests passed; worked C001 JSON and CSV have the same
case, proposal hash, approval decision, reviewer alias, and source-review
status; their recorded SHA-256 hashes are complete; CSV row count matches the
field count; C006 needs-correction produced no export; rejected C001 produced
no export; expired packages and unresolved findings cannot approve; formula-like
CSV cells are neutralised; the learner explains why exact-output binding is
stronger than a generic human-in-the-loop claim.

Return PASS or NOT YET with filename evidence. Do not reproduce source quotes.
```

## Pass criteria

- The changed-output, unchecked-review, and rejected-output controls pass.
- The review-expiry, unresolved-finding, and spreadsheet-cell controls pass.
- The worked approval is bound to the exact proposal hash.
- Approved C001 produces matching CSV and JSON exports.
- C006 `needs_correction` produces no export.
- Rejected C001 produces no export.
- Only fictional reviewer aliases appear.
- No external action occurs.
- Codex returns PASS.

## Stop conditions

Stop if an export appears before exact approval, a proposal changes without
invalidating approval, a real name appears, or either export disagrees with the
approved package. Never use real documents and never activate paid billing.

## Current official Google references

- [Document AI response and source-anchor structure](https://docs.cloud.google.com/document-ai/docs/handle-response)
- [Cloud Run authentication overview](https://docs.cloud.google.com/run/docs/authenticating/overview)
- [Google Cloud service identity](https://docs.cloud.google.com/run/docs/securing/service-identity)
