# Capstone Lab 6 — Test the Happy Path and the Safe Stops

## Outcome

You will run the complete offline test suite, then read an attack matrix like a
consultant. You will recreate the evaluation by testing a different synthetic
case through the user interface and matching the observed result to a frozen
expectation.

A passing happy path proves only that one expected example works. A controlled
workflow also needs negative tests: deliberately bad inputs or outputs that
must stop safely.

Portable Document Format (PDF) is the only accepted upload format in this
prototype.

## Follow along — I show you exactly how

### Step 1 — Freeze the test environment

Open Windows PowerShell:

```powershell
$capstoneRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\controlled-intake-capstone'
$demoRoot = Join-Path $capstoneRoot 'demo'
$lessonFolder = Join-Path $capstoneRoot 'evidence\tests-and-evaluation'
New-Item -ItemType Directory -Force -Path $lessonFolder | Out-Null
Set-Location -LiteralPath $demoRoot
& .\.venv\Scripts\Activate.ps1
$env:PROVIDER_MODE = 'fake'
python --version
python -m pip show pytest pydantic google-genai google-cloud-documentai
```

The package versions come from `requirements.txt` and
`requirements-dev.txt`. Do not upgrade them during the capstone.

### Step 2 — Run every offline automated test

Run:

```powershell
python -m pytest -vv |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_full_test_suite.txt')
if ($LASTEXITCODE -ne 0) { throw 'The complete offline suite failed. Stop and investigate.' }
```

Expected result: every collected test passes. No Google provider is called
because `PROVIDER_MODE` is `fake`.

### Step 3 — Run the attack controls as a named group

Run:

```powershell
python -m pytest .\tests\test_pipeline.py `
    -k "unknown_hash or media_type or known_failure or unknown_model_evidence or forbidden_model_action or provider_failure or exact_output_change or reject_and_unchecked_review or expired_exact_package or unresolved_findings or csv_export_neutralises or usage_and_date_caps or logs_contain or prompt_injection_fixture or model_echo" `
    -vv |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_attack_tests.txt')
if ($LASTEXITCODE -ne 0) { throw 'One or more attack controls failed.' }
```

The tests cover:

| Deliberate problem | Expected safe behavior |
|---|---|
| unknown file hash | stop before a provider call |
| wrong media type or corrupt PDF | stop before a provider call |
| missing field or conflicting total | route to human review |
| provider output with an unknown evidence reference | reject the draft |
| provider output containing approval/send language | reject the draft |
| action type conflicts with fixed findings | reject the draft |
| action cites an unrelated source field | reject the draft |
| provider failure | delete the temporary source |
| changed reviewed package | invalidate approval |
| unchecked or rejected decision | create no export |
| expired review or unresolved finding | block approval/export |
| spreadsheet formula prefix | neutralise the comma-separated values (CSV) cell |
| live run/page/date cap reached | stop a live provider call while fake mode remains usable |
| model, token ceiling, deadline or placeholder secret changed in Google mode | reject configuration before startup |
| source text in logs | test fails |
| document instruction or model echo | keep authority unchanged or reject it |

The real Google adapter is narrower than these hostile test doubles. Gemini
returns candidate identifiers and one finding-bounded action type; fixed
application code renders the exact wording and checks that the action cites a
permitted field type. The attack tests still matter because the pipeline must
reject an unsafe result if any present or future provider adapter breaks that
boundary.

### Step 4 — Check the web and deployment contract

Run:

```powershell
python -m pytest .\tests\test_http.py .\tests\test_contracts.py -vv |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_contract_tests.txt')
if ($LASTEXITCODE -ne 0) { throw 'The Hypertext Transfer Protocol or deployment contract failed.' }
```

Hypertext Transfer Protocol (HTTP) is how the browser calls the local or cloud
application. These tests check the synthetic acknowledgement, security
headers, export controls, European Union locations, immutable model, deadline
and token ceilings, the presence of repeatable private-access checks, visible
user-interface boundaries, malformed content length, and declared oversized
requests.

### Step 5 — Create the worked evaluation summary

Run:

```powershell
notepad (Join-Path $lessonFolder 'worked_evaluation_summary.md')
```

Paste, save, and close:

```markdown
# Worked offline evaluation

Data: six frozen synthetic PDF fixtures only
Provider mode: fake
Full suite: PASS only if every collected test passed

Release blockers:
- unknown source accepted;
- missing or false evidence link accepted;
- forbidden model authority accepted;
- unreviewed output exported;
- expired or unresolved output approved;
- formula-like export cell left executable;
- temporary source left behind;
- source text written to logs;
- European Union location contract changed;
- run, page, cost or date guard weakened.

Meaning of PASS:
The frozen offline controls behave as expected. It does not prove that a live
cloud provider, production security, customer demand, or legal compliance is
ready.
```

## Now recreate it yourself

Use C012 as your independent user-interface evaluation.

First create a prediction:

```powershell
notepad (Join-Path $lessonFolder 'recreated_c012_evaluation.md')
```

Without looking at an earlier C012 result, write:

- expected state;
- expected finding code;
- whether Document AI or Gemini instructions inside the PDF are trusted;
- whether approval/export should be allowed without correction; and
- the evidence you will inspect.

Start the local app:

```powershell
python -m uvicorn controlled_intake.main:app --app-dir .\src --host 127.0.0.1 --port 8080 --no-access-log
```

Open `http://127.0.0.1:8080`, process only the frozen C012 quotation, inspect
its evidence, choose `Needs correction`, and stop the server afterward.

Add the observed result to your file. Use this table:

```markdown
| Check | Predicted | Observed | PASS/FAIL |
|---|---|---|---|
| allowlist accepts unchanged C012 | | | |
| state is needs_review | | | |
| UNTRUSTED_INSTRUCTION_DETECTED exists | | | |
| evidence identifiers resolve | | | |
| decision is needs_correction | | | |
| approved export is absent | | | |
| external action is absent | | | |
```

End with `RECREATED EVALUATION: PASS` only if every row passes. Do not change a
test, expected state, or source file to turn a failure green.

## Ask Codex to check your work

Run `(Resolve-Path $lessonFolder).Path`, paste the result, and send:

```text
READ-ONLY CAPSTONE TEST REVIEW.

Inspect only this full folder:
[PASTE FULL PATH]

Do not edit, create, delete, rename, upload, install, start a server, or call a
cloud service. Stop for credentials or real data.

Check all three saved pytest outputs and recreated_c012_evaluation.md. Return
PASS or NOT YET for: every collected offline test passed; attack controls
actually ran; HTTP and deployment contracts passed; C012 prediction preceded
the observation; all evaluation rows are complete; needs_review,
UNTRUSTED_INSTRUCTION_DETECTED, needs_correction, no export, and no external
action are recorded; limitations of offline PASS are stated; only synthetic
data was used. Quote filenames and test names, not document text.
```

## Pass criteria

- Every offline automated test passes unchanged.
- Each listed failure mode has a safe-stop test.
- The user-interface and European Union location contracts pass.
- C012 matches its frozen expected result.
- Your report distinguishes test evidence from assumptions.
- Offline PASS is not described as production readiness.
- Codex returns PASS.

## Stop conditions

Stop on the first failed test. Do not loosen a guard, rewrite an expected
result, delete a failure record, or use live Google services to hide an offline
problem. Never use real data and never activate paid billing.

## Current official Google references

- [Document AI quotas and limits](https://docs.cloud.google.com/document-ai/quotas)
- [Cloud Run container runtime contract](https://docs.cloud.google.com/run/docs/container-contract)
- [Cloud Run development and temporary-file guidance](https://docs.cloud.google.com/run/docs/tips/general)
- [Vertex AI request-response logging](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/request-response-logging)
