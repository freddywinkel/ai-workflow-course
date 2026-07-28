# Module 6 — Make Human Control Real and Complete the Runnable Workflow

## Outcome

You will complete the runnable Course 1 workflow by:

1. opening the source-linked review package;
2. recording one explicit human decision;
3. binding that decision to one exact draft hash and revision;
4. proving approve, edit, reject, and expire have different effects;
5. proving a changed or expired draft cannot use old approval;
6. creating local CSV and JSON only after valid approval;
7. validating audit events, evaluation, and every required failure test.

Nothing is sent. The outbox is a local practice folder, not a message queue or
client-system connection.

## Beginner checkpoint

Start when Module 5 passes and contains:

- the worked 13-issue mock and support review;
- your recreated five-issue candidate and support review;
- all five deterministic fallback results;
- zero external actions;
- a Codex `PASS`.

## What meaningful human control means

“A person is somewhere in the loop” is not enough. A meaningful reviewer must
have:

- evidence: the source row, field, value, rule, summary, and action;
- identity: a named role, never anonymous silence;
- a specific object: exact draft revision and fingerprint;
- choices: approve, edit, reject, or expire;
- time: approval has an expiry;
- authority: the workflow actually obeys the decision;
- traceability: a valid audit event;
- a fallback: usable issue evidence when automation stops.

## Decision flow

```text
needs_review
     |
     +-- approve + evidence checked --> approved_for_local_export
     |                                      |
     |                              hash/revision/expiry recheck
     |                                      |
     |                                      v
     |                               approved_draft
     |                               local CSV + JSON
     |
     +-- edit --> changes_requested --> new revision --> needs_review again
     |
     +-- reject --> rejected --> no export
     |
     +-- expire --> expired --> no export
```

## Concepts

- A **revision** is one identified version of a draft.
- A **hash** is a fingerprint of exact bytes.
- **Secure Hash Algorithm 256-bit (SHA-256)** is the hash method used here.
- **Time of check versus time of use** means a decision can become invalid
  after it was recorded but before export.
- A **local draft outbox** stores prepared files on this computer only.
- An **audit event** records one material event using required fields.
- **Comma-separated values (CSV)** is a plain-text table.
- **JavaScript Object Notation (JSON)** is structured plain text.
- **User Acceptance Testing (UAT)** means intended users test whether a
  workflow supports its intended task. Full UAT is taught in Module 9.

## Official readings

1. [European Commission: European Union AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
2. [National Institute of Standards and Technology AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
3. [Python hashlib documentation](https://docs.python.org/3/library/hashlib.html)

These readings are context, not a legal or compliance assessment.

## Guided build

The guided path reviews and approves the complete worked draft, creates its
local exports, inspects canonical audit events, and then proves the evidence,
stale-update, edit, expiry, and external-action controls with separate failure
runs.

## Start or resume safely

Open Windows PowerShell and run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
$moduleFolder = Join-Path $projectRoot 'evidence\module-06'
$moduleFive = Join-Path $projectRoot 'evidence\module-05'
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
$runner = Join-Path $projectRoot 'src\course1_capstone\cli.py'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Project Python missing. Return to Windows Setup.'
}
if (-not (Test-Path -LiteralPath $runner)) {
    throw 'Course 1 runner missing. Return to Module 4 Stage 1.'
}
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot '.git'))) {
    throw 'Project Git repository missing. Return to Windows Setup.'
}
New-Item -ItemType Directory -Force -Path $moduleFolder | Out-Null
Set-Location -LiteralPath $projectRoot
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
if (-not (Test-Path -LiteralPath (Join-Path $courseRoot 'course1_capstone\tests'))) {
    throw 'That course folder does not contain the Course 1 tests.'
}
& $pythonExe --version
```

Use `& $pythonExe`, never bare `python`.

## Follow along — I show you exactly how

### Stage 1 — Open the complete worked review package

Run:

```powershell
$workedWorkspace = Join-Path $moduleFive 'worked-mock'
$workedLatest = Join-Path $workedWorkspace 'latest_run.txt'
if (-not (Test-Path -LiteralPath $workedLatest)) {
    throw 'Module 5 worked run missing. Return to Module 5 Stage 1.'
}
$moduleFiveWorkedRunLocator = (Get-Content -LiteralPath $workedLatest).Trim()
$moduleFiveWorkedRunDir = Join-Path $workedWorkspace $moduleFiveWorkedRunLocator
$workedRunDir = Join-Path $moduleFolder 'worked-decision-run'
if (Test-Path -LiteralPath $workedRunDir) {
    Write-Host "KEEPING your existing $workedRunDir"
} else {
    Copy-Item -LiteralPath $moduleFiveWorkedRunDir -Destination $workedRunDir -Recurse
    Write-Host "COPIED the exact Module 5 run to $workedRunDir"
}
$workedSupportReviewSource = Join-Path $moduleFive 'worked_support_review.md'
$workedSupportReviewCopy = Join-Path $moduleFolder 'source-m5-worked_support_review.md'
if (-not (Test-Path -LiteralPath $workedSupportReviewSource)) {
    throw 'Module 5 worked support review missing.'
}
if (Test-Path -LiteralPath $workedSupportReviewCopy) {
    Write-Host "KEEPING your existing $workedSupportReviewCopy"
} else {
    Copy-Item -LiteralPath $workedSupportReviewSource -Destination $workedSupportReviewCopy
}
& $pythonExe $runner status --run-dir $workedRunDir
Get-Content -LiteralPath (Join-Path $workedRunDir 'review\review_package.json')
Get-FileHash -LiteralPath (Join-Path $workedRunDir 'draft\summary.json') -Algorithm SHA256
```

Before deciding, open:

```powershell
code (Join-Path $workedRunDir 'source\work_items.csv')
code (Join-Path $workedRunDir 'issues\issues.csv')
code (Join-Path $workedRunDir 'draft\summary.json')
code (Join-Path $workedRunDir 'review\review_package.json')
code $workedSupportReviewCopy
```

If `code` is unavailable, use Visual Studio Code **File > Open File**.

Do not continue until you can answer:

1. Which 13 issues exist?
2. Which source row, field, and raw value supports each?
3. Does every sentence visibly cite known issue IDs?
4. Is every action only `human_review`?
5. Are external actions zero?
6. What exact SHA-256 hash are you reviewing?

### Stage 2 — Record an exact approve decision

Only after completing the checks above, run:

The letter `Z` at the end of the expiry means Coordinated Universal Time
(UTC).

```powershell
& $pythonExe $runner decide `
    --run-dir $workedRunDir `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Checked all 13 synthetic source links, summary statements, and human-review actions.' `
    --expected-revision 1 `
    --evidence-reviewed `
    --expires-at 2099-01-01T00:00:00Z
if ($LASTEXITCODE -ne 0) {
    throw 'Approval safely stopped. Read the named reason above.'
}
Get-Content -LiteralPath (Join-Path $workedRunDir 'review\decision-r1.json')
```

The runner records the current decision time. This guided synthetic exercise
uses a visible far-future expiry so a study break does not invalidate your
worked evidence. A real implementation needs a proportionate, much shorter
expiry based on process risk. If you omit the expiry, the runner uses 24 hours.
The record includes:

- decision ID;
- run ID;
- reviewer role;
- decision;
- draft revision;
- exact draft SHA-256;
- decision and expiry times;
- `evidence_reviewed: true`;
- reason.

An approval is not transferable to “whatever file is latest.”

The decision is recorded in the copied run under
`evidence\module-06\worked-decision-run`. Module 5 evidence remains unchanged.

### Stage 3 — Create the approved local drafts

Run:

```powershell
& $pythonExe $runner export --run-dir $workedRunDir
if ($LASTEXITCODE -ne 0) {
    throw 'Export safely stopped. Read the named reason above.'
}
Get-ChildItem -LiteralPath (Join-Path $workedRunDir 'outbox')
Get-Content -LiteralPath (Join-Path $workedRunDir 'state.json')
Get-Content -LiteralPath (Join-Path $workedRunDir 'evaluation.json')
```

**Expected result:**

- `approved-r1.csv` and `approved-r1.json`;
- state `approved_draft`;
- local export count `2`;
- external actions `0`;
- 13 records in each export.

Check the CSV count:

```powershell
(Import-Csv -LiteralPath (Join-Path $workedRunDir 'outbox\approved-r1.csv')).Count
```

Expected: `13`.

Run the export command again. The same two files remain and no second logical
export event is created.

### Stage 4 — Inspect the canonical audit events

Run:

```powershell
$events = Get-Content -LiteralPath (Join-Path $workedRunDir 'audit\events.jsonl') |
    ForEach-Object { $_ | ConvertFrom-Json }
$events | Format-Table event_type,state,actor_type,occurred_at
$events | ForEach-Object {
    [PSCustomObject]@{
        event_id = $_.event_id
        has_run_id = -not [string]::IsNullOrWhiteSpace($_.run_id)
        has_details = $null -ne $_.details
    }
}
```

Every event must contain:

- `event_id`;
- `run_id`;
- `event_type`;
- `state`;
- `occurred_at`;
- `actor_type`;
- `details`.

The local export event says `external_actions: 0`. It must never claim a
message was sent.

A **PowerShell custom object (`[PSCustomObject]`)** is the labelled display row
used by the audit-check command; it does not change the audit file.

## Failure lab — prove the controls before relying on them

Every red `SAFE STOP` below is expected. Each scenario uses a fresh synthetic
workspace so it cannot damage the worked run. The runner also prints a
`FAILURE_EVIDENCE=` path and records the failed attempt with
`external_actions: 0`.

### Failure 1 — Required review without evidence

```powershell
$noEvidenceWorkspace = Join-Path $moduleFolder 'failure-no-evidence'
& $pythonExe $runner prepare `
    --input .\data\input\work_items.csv `
    --expected .\tests\expected_issues.csv `
    --workspace $noEvidenceWorkspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$noEvidenceRunLocator = (Get-Content -LiteralPath `
    (Join-Path $noEvidenceWorkspace 'latest_run.txt')).Trim()
$noEvidenceRun = Join-Path $noEvidenceWorkspace $noEvidenceRunLocator
& $pythonExe $runner decide `
    --run-dir $noEvidenceRun `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Deliberately omitted evidence confirmation for this failure test.' `
    --expected-revision 1
$LASTEXITCODE
Test-Path -LiteralPath (Join-Path $noEvidenceRun 'outbox')
```

Expected: `review_evidence_required`, exit code `1`, outbox `False`.

### Failure 2 — Stale revision update

```powershell
$staleWorkspace = Join-Path $moduleFolder 'failure-stale'
& $pythonExe $runner prepare `
    --input .\data\input\work_items.csv `
    --expected .\tests\expected_issues.csv `
    --workspace $staleWorkspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$staleRunLocator = (Get-Content -LiteralPath `
    (Join-Path $staleWorkspace 'latest_run.txt')).Trim()
$staleRun = Join-Path $staleWorkspace $staleRunLocator
& $pythonExe $runner decide `
    --run-dir $staleRun `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Deliberately used the wrong revision for this failure test.' `
    --expected-revision 2 `
    --evidence-reviewed
$LASTEXITCODE
```

Expected: `stale_update`, exit code `1`.

### Failure 3 — Edited draft after approval

```powershell
$editedWorkspace = Join-Path $moduleFolder 'failure-edited'
& $pythonExe $runner prepare `
    --input .\data\input\work_items.csv `
    --expected .\tests\expected_issues.csv `
    --workspace $editedWorkspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$editedRunLocator = (Get-Content -LiteralPath `
    (Join-Path $editedWorkspace 'latest_run.txt')).Trim()
$editedRun = Join-Path $editedWorkspace $editedRunLocator
& $pythonExe $runner decide `
    --run-dir $editedRun `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Synthetic approval used only for the edit invalidation test.' `
    --expected-revision 1 `
    --evidence-reviewed
Add-Content -LiteralPath (Join-Path $editedRun 'draft\summary.json') -Value ' ' -NoNewline
& $pythonExe $runner export --run-dir $editedRun
$LASTEXITCODE
Test-Path -LiteralPath (Join-Path $editedRun 'outbox')
```

Expected: `edited_draft_after_approval`, exit code `1`, outbox `False`.

### Failure 4 — Expired approval

Fixed UTC times make this failure repeatable.

```powershell
$expiredWorkspace = Join-Path $moduleFolder 'failure-expired'
& $pythonExe $runner prepare `
    --input .\data\input\work_items.csv `
    --expected .\tests\expected_issues.csv `
    --workspace $expiredWorkspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$expiredRunLocator = (Get-Content -LiteralPath `
    (Join-Path $expiredWorkspace 'latest_run.txt')).Trim()
$expiredRun = Join-Path $expiredWorkspace $expiredRunLocator
& $pythonExe $runner decide `
    --run-dir $expiredRun `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Synthetic approval with fixed times for the expiry test.' `
    --expected-revision 1 `
    --evidence-reviewed `
    --decided-at 2026-07-28T10:00:00Z `
    --expires-at 2026-07-28T11:00:00Z
& $pythonExe $runner export `
    --run-dir $expiredRun `
    --checked-at 2026-07-28T12:00:00Z
$LASTEXITCODE
Get-Content -LiteralPath (Join-Path $expiredRun 'state.json')
```

Expected: `expired_review`, exit code `1`, state `expired`, no outbox.

### Failure 5 — External-action control tampered

```powershell
$controlWorkspace = Join-Path $moduleFolder 'failure-control'
& $pythonExe $runner prepare `
    --input .\data\input\work_items.csv `
    --expected .\tests\expected_issues.csv `
    --workspace $controlWorkspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$controlRunLocator = (Get-Content -LiteralPath `
    (Join-Path $controlWorkspace 'latest_run.txt')).Trim()
$controlRun = Join-Path $controlWorkspace $controlRunLocator
& $pythonExe $runner decide `
    --run-dir $controlRun `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Synthetic approval used only for the control tamper test.' `
    --expected-revision 1 `
    --evidence-reviewed
$controlPath = Join-Path $controlRun 'control.json'
$control = Get-Content -Raw -LiteralPath $controlPath | ConvertFrom-Json
$control.EXTERNAL_ACTIONS_ENABLED = $true
$control | ConvertTo-Json | Set-Content -LiteralPath $controlPath -Encoding utf8
& $pythonExe $runner export --run-dir $controlRun
$LASTEXITCODE
Test-Path -LiteralPath (Join-Path $controlRun 'outbox')
```

Expected: `external_action_blocked`, exit code `1`, outbox `False`.

This tampering is allowed only in the isolated synthetic failure folder.

## Now recreate it yourself

Recreate the complete decision lifecycle with the different five-issue
candidate.

### Recreation 1 — Locate the five-issue run and your candidate

```powershell
$moduleFiveRecreatedWorkspace = Join-Path $moduleFive 'recreated-mock'
$recreatedLatest = Join-Path $moduleFiveRecreatedWorkspace 'latest_run.txt'
$moduleFiveCandidate = Join-Path $moduleFive 'recreated_candidate_summary.json'
$moduleFiveSupportReview = Join-Path $moduleFive 'recreated_support_review.md'
if (-not (Test-Path -LiteralPath $recreatedLatest)) {
    throw 'Module 5 recreated run missing.'
}
if (-not (Test-Path -LiteralPath $moduleFiveCandidate)) {
    throw 'Module 5 candidate summary missing.'
}
if (-not (Test-Path -LiteralPath $moduleFiveSupportReview)) {
    throw 'Module 5 recreated support review missing.'
}
$moduleFiveRecreatedRunLocator = (Get-Content -LiteralPath $recreatedLatest).Trim()
$moduleFiveRecreatedRunDir = Join-Path `
    $moduleFiveRecreatedWorkspace $moduleFiveRecreatedRunLocator
$recreatedRunDir = Join-Path $moduleFolder 'recreated-decision-run'
$candidate = Join-Path $moduleFolder 'recreated_candidate_summary.json'
$recreatedSupportReviewCopy = Join-Path $moduleFolder 'source-m5-recreated_support_review.md'
if (Test-Path -LiteralPath $recreatedRunDir) {
    Write-Host "KEEPING your existing $recreatedRunDir"
} else {
    Copy-Item -LiteralPath $moduleFiveRecreatedRunDir -Destination $recreatedRunDir -Recurse
    Write-Host "COPIED the exact Module 5 recreated run to $recreatedRunDir"
}
if (Test-Path -LiteralPath $candidate) {
    Write-Host "KEEPING your existing $candidate"
} else {
    Copy-Item -LiteralPath $moduleFiveCandidate -Destination $candidate
}
if (Test-Path -LiteralPath $recreatedSupportReviewCopy) {
    Write-Host "KEEPING your existing $recreatedSupportReviewCopy"
} else {
    Copy-Item -LiteralPath $moduleFiveSupportReview -Destination $recreatedSupportReviewCopy
}
& $pythonExe $runner status --run-dir $recreatedRunDir
```

All learner evidence that Module 6 will change or later ask Codex to assess now
sits under `evidence\module-06`. Module 5 remains the unchanged source.

### Recreation 2 — Request an edit of revision 1

Create the review at the exact path
`evidence\module-06\recreated_review_r1.md`. The command below creates the
headings once and never overwrites a prior review:

```powershell
$reviewR1 = Join-Path $moduleFolder 'recreated_review_r1.md'
if (Test-Path -LiteralPath $reviewR1) {
    Write-Host "KEEPING your existing $reviewR1"
} else {
    @'
# Recreated review — revision 1

Run ID:
Draft revision: 1
Source-linked issues checked:
Candidate sentences checked:
Issue IDs checked in groups and actions:
Unsupported statements or external actions found:
Exact draft SHA-256:
Manual fallback:
Decision: edit
Exact wording to change:
'@ | Set-Content -LiteralPath $reviewR1 -Encoding utf8
}
notepad $reviewR1
```

Complete and save it in your own words before continuing. Record all five
evidence checks, decision `edit`, and the exact wording you want changed.

Then run:

```powershell
& $pythonExe $runner decide `
    --run-dir $recreatedRunDir `
    --decision edit `
    --reviewer-role course_learner `
    --reason 'Use my validated candidate wording and require a complete new review.' `
    --expected-revision 1
& $pythonExe $runner revise `
    --run-dir $recreatedRunDir `
    --replacement $candidate `
    --expected-revision 1
& $pythonExe $runner status --run-dir $recreatedRunDir
```

Expected: revision `2`, state `needs_review`, no active decision, no outbox.

### Recreation 3 — Review and approve revision 2

Create the second review at the exact path
`evidence\module-06\recreated_review_r2.md`. This command creates it once and
keeps a prior version unchanged:

```powershell
$reviewR2 = Join-Path $moduleFolder 'recreated_review_r2.md'
if (Test-Path -LiteralPath $reviewR2) {
    Write-Host "KEEPING your existing $reviewR2"
} else {
    @'
# Recreated review — revision 2

Run ID:
Draft revision: 2
All five source-linked issues checked:
All candidate sentences checked:
Each issue ID appears exactly once in groups and actions:
Unsupported statements or external actions found:
Exact revision 2 SHA-256:
Manual fallback:
Decision: approve
Reason:
'@ | Set-Content -LiteralPath $reviewR2 -Encoding utf8
}
notepad $reviewR2
```

Complete and save it before continuing. Actually check:

- all five source-linked issues;
- all candidate sentences;
- every issue ID exactly once in groups and actions;
- no unsupported statement or external action;
- exact revision 2 hash;
- manual fallback.

Then run:

```powershell
Get-FileHash -LiteralPath (Join-Path $recreatedRunDir 'draft\summary.json') -Algorithm SHA256
& $pythonExe $runner decide `
    --run-dir $recreatedRunDir `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Reviewed revision 2 against all five synthetic source-linked issues.' `
    --expected-revision 2 `
    --evidence-reviewed `
    --expires-at 2099-01-01T00:00:00Z
& $pythonExe $runner export --run-dir $recreatedRunDir
(Import-Csv -LiteralPath (Join-Path $recreatedRunDir 'outbox\approved-r2.csv')).Count
```

Expected: `PASS` and count `5`.

### Recreation 4 — Prove reject and explicit expire separately

Prepare two fresh recreated workspaces and choose different decisions:

```powershell
$recreatedDecisionInput = Join-Path $recreatedRunDir 'source\work_items.csv'
foreach ($decision in 'reject','expire') {
    $workspace = Join-Path $moduleFolder "recreated-$decision"
    $latestPath = Join-Path $workspace 'latest_run.txt'
    if (Test-Path -LiteralPath $latestPath) {
        Write-Host "KEEPING your existing $workspace"
    } else {
        & $pythonExe $runner prepare `
            --input $recreatedDecisionInput `
            --workspace $workspace `
            --ai-mode mock `
            --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
        if ($LASTEXITCODE -ne 0) {
            throw "The $decision recreation safely stopped before a run was created."
        }
    }
    $runLocator = (Get-Content -LiteralPath $latestPath).Trim()
    $runDir = Join-Path $workspace $runLocator
    & $pythonExe $runner decide `
        --run-dir $runDir `
        --decision $decision `
        --reviewer-role course_learner `
        --reason "Synthetic $decision decision; local export must remain blocked." `
        --expected-revision 1
    & $pythonExe $runner export --run-dir $runDir
    Write-Host "Expected safe stop above for $decision; exit code $LASTEXITCODE"
}
```

Both exports must safely stop with `decision_not_approved`.

## Run the complete executable acceptance suite

First confirm that your copied runner still matches the course reference:

```powershell
$learnerWorkflowHash = (Get-FileHash -LiteralPath (Join-Path $projectRoot 'src\course1_capstone\workflow.py') -Algorithm SHA256).Hash
$courseWorkflowHash = (Get-FileHash -LiteralPath (Join-Path $courseRoot 'course1_capstone\workflow.py') -Algorithm SHA256).Hash
$learnerCliHash = (Get-FileHash -LiteralPath (Join-Path $projectRoot 'src\course1_capstone\cli.py') -Algorithm SHA256).Hash
$courseCliHash = (Get-FileHash -LiteralPath (Join-Path $courseRoot 'course1_capstone\cli.py') -Algorithm SHA256).Hash
$learnerWorkflowHash -eq $courseWorkflowHash
$learnerCliHash -eq $courseCliHash
```

Expected: `True` and `True`. If either is false, do not overwrite anything.
Ask Codex to inspect the difference.

Run all tests with the exact project Python:

`Push-Location` temporarily moves into the course folder. `Pop-Location`
returns to the learner project even when the paths contain spaces.

```powershell
Push-Location -LiteralPath $courseRoot
& $pythonExe -m unittest discover -s course1_capstone\tests -v
$testExitCode = $LASTEXITCODE
Pop-Location
$testExitCode
```

**Expected result:** every test says `ok`, the final result is `OK`, and exit
code is `0`. The suite covers:

- frozen and recreated accuracy;
- schemas for work items, issues, summary, approval, audit, and evaluation;
- duplicate ID and retry;
- required evidence and stale update;
- malformed, missing, and wrong-header input;
- AI disabled, timeout, refusal, malformed JSON, and unknown issue ID;
- untrusted free text;
- edited, rejected, edit-requested, and expired reviews;
- external action false and tamper blocking;
- approved local CSV/JSON;
- manual fallback and audit contract.

If `ModuleNotFoundError: No module named 'jsonschema'` appears, return to Windows
Setup and install the pinned course requirements through `$pythonExe`. Do not
use a global Python or remove the schema tests.

Record a path-neutral result for every attempt without overwriting an earlier
one. A failed Python traceback can contain your absolute Windows path and
username, so raw diagnostics must **not** be saved inside the Git repository.
The code below shows the raw output on screen, keeps a temporary diagnostic
copy outside the repository, and saves only a structured status, test count,
result line, and exit code as course evidence.

```powershell
$attemptNumber = 1
do {
    $acceptancePath = Join-Path $moduleFolder ('automated_acceptance_attempt_{0:D2}.json' -f $attemptNumber)
    $attemptNumber += 1
} while (Test-Path -LiteralPath $acceptancePath)
$recordedAttempt = $attemptNumber - 1
$rawDiagnosticsPath = [System.IO.Path]::GetTempFileName()
Push-Location -LiteralPath $courseRoot
$testOutput = & $pythonExe -m unittest discover -s course1_capstone\tests -v *>&1
$testExitCode = $LASTEXITCODE
Pop-Location
$testText = @($testOutput | ForEach-Object { $_.ToString() })
$testText | Set-Content -LiteralPath $rawDiagnosticsPath -Encoding utf8
$testText | ForEach-Object { Write-Host $_ }
$ranLine = $testText | Where-Object { $_ -match '^Ran \d+ tests?' } |
    Select-Object -Last 1
$resultLine = $testText | Where-Object { $_ -match '^(OK|FAILED)' } |
    Select-Object -Last 1
[PSCustomObject]@{
    schema_version = 1
    attempt = $recordedAttempt
    suite = 'course1_capstone unittest discovery'
    status = if ($testExitCode -eq 0) { 'PASS' } else { 'FAIL' }
    exit_code = $testExitCode
    tests_run = if ($ranLine -match '^Ran (\d+) tests?') { [int]$Matches[1] } else { $null }
    result = if ($resultLine) { $resultLine } else { 'NO RESULT LINE' }
    raw_diagnostics_committed = $false
    raw_diagnostics_location = 'outside_repository_temporary_file'
} | ConvertTo-Json | Set-Content -LiteralPath $acceptancePath -Encoding utf8
Write-Host "SAVED path-neutral evidence attempt $recordedAttempt"
if ($testExitCode -ne 0) {
    Write-Host 'Raw diagnostics are outside the repository. Do not add them to Git.'
    Write-Host 'Run: notepad $rawDiagnosticsPath'
    throw 'Automated acceptance failed. Preserve the structured FAIL record and repair the named failure.'
}
```

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path`, paste it below, and send:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
[PASTE FULL MODULE-06 PATH]

Do not edit, create, delete, move, rename, format, or execute anything. Do not
inspect a parent folder. This path must contain no secrets and no real client,
real work, personal, or medical data. Stop if it does.

Return:
1. PASS or NOT YET;
2. worked approval bound to exact run, revision, hash, reviewer, reason, and
expiry;
3. local approved CSV/JSON with 13 records and external actions 0;
4. required-evidence, stale-update, edited-draft, expired-review, and tampered
control safe-stop evidence;
5. recreated edit -> revision 2 -> new review -> approve -> five-record export;
6. reject and explicit expire blocking export;
7. canonical audit events, evaluation, manual fallback, and idempotent retry;
8. every numbered path-neutral automated acceptance record, with the
highest-numbered attempt showing status PASS, result OK, and exit code 0;
9. synthetic data only and no network, provider key, paid service, or external
action;
10. the smallest learner-made corrections if NOT YET.

Remain read-only. Do not provide replacement files.
```

## Pass criteria

- [ ] Exact project Python is used through `$pythonExe`.
- [ ] Evidence review is explicit before approval.
- [ ] Approval is bound to one run, revision, hash, reviewer, reason, and expiry.
- [ ] Approve, edit, reject, and expire cause different enforced states.
- [ ] Edited, stale, expired, rejected, and evidence-free cases cannot export.
- [ ] `EXTERNAL_ACTIONS_ENABLED=false` is explicit and tampering blocks export.
- [ ] Approved output is local CSV and JSON only.
- [ ] Worked export has 13 records; recreated revision 2 export has 5.
- [ ] Audit events contain every required field and claim zero external actions.
- [ ] Manual fallback is complete and role-owned.
- [ ] All automated tests pass with exit code 0.
- [ ] All data is synthetic and secret-free.
- [ ] Codex returns `PASS` in read-only mode.

### Record your Module 6 PASS in Git

Only after Codex returns `PASS`:

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence\module-06"
git commit -m "complete module 6 evidence"
git status --short
```

## Consultant lens

Human control is a tested system behavior, not a sentence in a policy. The
durable pattern is evidence -> exact revision -> explicit decision -> recheck
at use -> limited effect -> audit -> fallback.

## Capstone increment

The technical Course 1 slice is now runnable from input through controlled
local export. Passing it proves a bounded synthetic capability only. Modules
7-9 still test risk ownership, tool fit, evaluation, adoption, handover, and
the supported final Course 1 recommendation.

## Required artifact

`evidence/module-06` contains non-overwriting source copies of the required
Module 5 worked and recreated evidence, the worked decision and exports,
canonical audit and evaluation evidence, five manual failure runs, both
learner-written recreated reviews, the recreated edit and revision-2
lifecycle, reject and expire results, and path-neutral structured automated
acceptance records. Raw traceback diagnostics stay outside the Git repository.
The decisions, local exports, and run evidence checked by the Module 6 Codex
prompt are therefore all inside its authorized folder.

## Test gate

All Module 6 pass criteria, all automated schema and workflow tests, and the
read-only Codex review must pass. The final automated result is `OK` with exit
code 0.

## Stop or rework

Stop if evidence-free, stale, changed, rejected, edit-requested, expired, or
externally enabled work can export; if an audit event lacks a required field;
if any test fails; or if any real data, secret, network, or paid provider is
introduced.

## Common failures

- Approving “the latest draft” instead of one exact revision and hash.
- Treating silence or a missing review record as approval.
- Calling a local draft a sent message.
- Reusing approval after an edit.
- Removing a failed test instead of repairing the named control.

## Estimated time

8-12 hours, best completed as three to five sessions.

Suggested sessions: three to five sessions of about 2-3 hours.
