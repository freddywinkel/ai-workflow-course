# Capstone Lab 1 — Run the Complete Workflow Locally First

## Outcome

You will run the real web application with offline fake adapters, process the
clean C001 synthetic quotation, inspect source-linked fields, approve the exact
result, and download comma-separated values (CSV) and JavaScript Object
Notation (JSON). No Google service or credit is used.

## Concepts

- A **provider adapter** is a small code layer that calls either a fake local
  service or the real vendor service.
- A **virtual environment** is a private Python package folder for one project.
- A **test client** calls the application without opening a public network
  service.
- `localhost` means only this computer.
- The fake adapter reads born-digital PDF text. It is not a substitute for the
  live Document AI optical character recognition (OCR) proof.

## Follow along — I show you exactly how

### Step 1 — Prepare a separate practice copy

Open Windows PowerShell:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$sourceDemo = Join-Path $courseRoot 'future_courses\course_04_controlled_document_ai\controlled_document_intake_demo'
$capstoneRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\controlled-intake-capstone'
$demoRoot = Join-Path $capstoneRoot 'demo'
New-Item -ItemType Directory -Force -Path $capstoneRoot | Out-Null
if (Test-Path $demoRoot) {
    throw 'The demo practice folder already exists. Inspect it instead of overwriting it.'
}
Copy-Item -LiteralPath $sourceDemo -Destination $demoRoot -Recurse
Set-Location -LiteralPath $demoRoot
```

This copies only course-owned demo code. It does not copy a credential.

### Step 2 — Create the Python environment

Run:

```powershell
python --version
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --requirement .\requirements-dev.txt
```

Expected result: Python 3.12 and successful package installation. If
PowerShell blocks activation, return to Course 1 Windows Setup. Do not weaken
the computer's policy globally.

### Step 3 — Run the frozen tests

```powershell
$env:PROVIDER_MODE = 'fake'
python -m pytest
```

Expected result: every test passes. A warning is not a failed test. Save the
last line in:

```powershell
python -m pytest | Tee-Object -FilePath .\evidence_local_tests.txt
```

### Step 4 — Start the private local application

Run:

```powershell
python -m uvicorn controlled_intake.main:app --app-dir .\src --host 127.0.0.1 --port 8080 --no-access-log
```

Leave this PowerShell window open. Open a second PowerShell window and run:

```powershell
Start-Process 'http://127.0.0.1:8080'
```

Expected screen: **Controlled Document Intake** with a clear “Synthetic
fixtures only” boundary.

### Step 5 — Process the worked C001 fixture

In the app:

1. choose the original file at
   `source_material\corpus\cases\C001\quotation.pdf` inside the course;
2. tick the synthetic confirmation;
3. click **Process synthetic document**;
4. confirm case `C001`, one page, and `pending approval`;
5. inspect at least two source quotes;
6. choose `Approve exact export`;
7. keep reviewer alias `reviewer-demo-01`;
8. tick the source-review box;
9. click **Record human decision**;
10. download JSON and CSV.

Expected result:

- the quote reference is `Q-C001-2026`;
- every present field has an evidence identifier;
- the processing proof says the temporary file was deleted;
- download buttons appear only after approval;
- no email, payment, supplier selection, or external update occurs.

Save the two downloads in:

```text
AI-workflow-learning\controlled-intake-capstone\evidence\local-worked\
```

Close the browser tab. In the server window press `Ctrl+C`.

### Step 6 — Prove the server used no Google provider

Open the JSON export in Notepad. Find:

```json
"provider_mode": "fake"
```

Do not edit the export.

## Now recreate it yourself

Repeat the local process with C006:

```text
source_material\corpus\cases\C006\quotation.pdf
```

This time:

- predict the state before processing;
- do not approve the draft;
- choose `Needs correction`;
- write a fictional-only comment explaining the missing field;
- prove no CSV or JSON download buttons appear.

Create `evidence\local-recreated\prediction.md` containing your prediction,
observed state, missing field, and why no export was created.

Then run C008 as a second recreation. Predict the declared/calculated total
discrepancy before processing. Record the finding code but do not copy model
wording into your evidence.

## Ask Codex to check your work

Run `(Resolve-Path $capstoneRoot).Path` and send:

```text
READ-ONLY CONTROLLED INTAKE LOCAL REVIEW.

I authorize inspection of only:
[PASTE FULL PATH]

Do not edit, create, delete, rename, move, upload, install, or run a server.
You may run only the existing automated tests read-only if I separately say
"run the tests". Stop if you find a credential, real client/work document,
personal data, or health data.

Check:
1. the copied demo has no .env credential;
2. evidence_local_tests.txt reports all tests passing;
3. the worked C001 JSON/CSV agree on document hash, field names, source pages,
proposal hash, and approved fictional reviewer alias;
4. provider_mode is fake and raw_file_persisted is false;
5. C006 recreation predicts and records the missing valid-through field;
6. C006 has no approved export;
7. C008 prediction and total-discrepancy finding agree;
8. no external-action state or real data exists.

Return PASS or NOT YET with exact file evidence.
```

## Pass criteria

- The complete test suite passes.
- C001 produces source-linked fields and both export formats after approval.
- JSON and CSV agree.
- C006 and C008 reach `needs_review`.
- Unapproved recreation output cannot export.
- The local provider is visibly fake.
- No credential or real data exists.
- Codex returns PASS.

## Stop conditions

Stop if a selected hash is rejected; do not weaken the allowlist. Stop if a
test fails; do not edit the expected answer to make it green. Stop immediately
if a real document is selected.
