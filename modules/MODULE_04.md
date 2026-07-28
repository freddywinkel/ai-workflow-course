# Module 4 — Build and Test the Rule-based Workflow

## Outcome

You will build the first working part of the Course 1 capstone. It will:

1. read only a fictional comma-separated values (CSV) file;
2. reject unsafe or malformed input;
3. apply the fixed rules R001-R011;
4. create 13 source-linked issue records;
5. create a deterministic summary fallback;
6. write audit and evaluation evidence;
7. perform zero external actions.

You first follow the complete worked example. Then you repeat the method with a
different six-row synthetic file and make your own prediction before seeing the
answer.

Artificial Intelligence (AI) remains disabled in this module. Module 5 adds a
bounded offline mock after the rule results are proven.

## Beginner checkpoint

Start only after Module 3 passes and the Windows setup created:

- `data\input\work_items.csv`;
- `tests\expected_issues.csv`;
- `.venv\Scripts\python.exe`;
- a Git repository.

**Git** is the version-control tool that records file changes. **Python** is the
programming language used by the runner.

## What you are building, in normal language

Think of the runner as a guarded desk:

```text
fictional CSV
     |
     v
[door check: correct file and columns?] -- no --> safe stop
     |
     v
[R001-R011: fixed, visible checks]
     |
     v
[source-linked issue list]
     |
     v
[deterministic summary + human-review package]
     |
     v
[wait for a human; do not send anything]
```

The code does not decide what the business should do. It only exposes
predefined exceptions and prepares evidence for a reviewer.

## Concepts

- **Validation** checks whether input meets an explicit contract.
- **Deterministic** means the same valid input and rules produce the same
  result.
- **Idempotency** means a retry does not create a second logical effect.
- A **run identifier (ID)** identifies one processing run.
- A **named state** makes success, waiting, or failure visible.
- **JavaScript Object Notation (JSON)** is a structured plain-text format.
- **JavaScript Object Notation Lines (JSONL)** stores one JSON object per line.
- **Secure Hash Algorithm 256-bit (SHA-256)** creates a fingerprint of exact
  file bytes.
- An **Architecture Decision Record (ADR)** explains a technical choice, its
  alternatives, controls, and consequences.
- A **safe stop** ends processing visibly and routes the case to a person.

Every issue uses this identity:

```text
(work_item_id, rule_code, field)
```

Do not compare only `work_item_id` and `rule_code`. One rule can correctly
flag more than one field.

## Official readings

1. [Python CSV module](https://docs.python.org/3/library/csv.html)
2. [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
3. [Python hashlib module](https://docs.python.org/3/library/hashlib.html)

You may finish the guided work before reading every linked page.

## Guided build

The guided path first runs the smallest input and rule functions, then the
complete worked run, an idempotent retry, and four named safe failures. Keep
the worked evidence unchanged; the separate recreation is where you make your
own prediction and explanation.

## Start or resume safely

Open a new Windows PowerShell window and run this block at the start of every
session. PowerShell forgets variables when you close it; your saved files
remain.

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
$moduleFolder = Join-Path $projectRoot 'evidence\module-04'
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot '.git'))) {
    throw 'Project repository missing. Return to Windows Setup.'
}
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Project Python missing. Return to Windows Setup.'
}
New-Item -ItemType Directory -Force -Path $moduleFolder | Out-Null
Set-Location -LiteralPath $projectRoot
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
if (-not (Test-Path -LiteralPath (Join-Path $courseRoot 'course1_capstone\workflow.py'))) {
    throw 'That course folder does not contain course1_capstone\workflow.py.'
}
& $pythonExe --version
```

Always use `& $pythonExe`. Do not replace it with bare `python`; Windows could
silently select another installation.

## Follow along — I show you exactly how

### Stage 1 — Copy the controlled reference runner without overwriting work

Run:

```powershell
$sourceRunner = Join-Path $courseRoot 'course1_capstone'
$runnerFolder = Join-Path $projectRoot 'src\course1_capstone'
if (-not (Test-Path -LiteralPath (Join-Path $sourceRunner 'workflow.py'))) {
    throw 'course1_capstone\workflow.py was not found in that course folder.'
}
New-Item -ItemType Directory -Force -Path $runnerFolder | Out-Null
foreach ($name in '__init__.py','workflow.py','cli.py') {
    $destination = Join-Path $runnerFolder $name
    if (Test-Path -LiteralPath $destination) {
        Write-Host "KEEPING existing $destination"
    } else {
        Copy-Item -LiteralPath (Join-Path $sourceRunner $name) -Destination $destination
        Write-Host "COPIED $destination"
    }
}
Get-ChildItem -LiteralPath $runnerFolder
```

**Expected result:** three files are listed. On a later session, the command
prints `KEEPING` and does not erase your files.

The supplied runner is reference code, not a mystery service. It imports only
Python standard-library modules and contains no network or external-action
function. Open `src\course1_capstone\workflow.py` in Visual Studio Code and use
search to find:

- `load_work_items`;
- `detect_issues`;
- `create_bounded_summary`;
- `record_decision`;
- `export_approved`.

Read the name and first paragraph of each function. You do not need to
understand every code line yet.

### Stage 2 — Run only the input check

This small command calls `load_work_items` and stops before any rule or output:

```powershell
& $pythonExe -c "from pathlib import Path; from src.course1_capstone.workflow import load_work_items; raw, rows = load_work_items(Path('data/input/work_items.csv')); print(f'PASS: {len(rows)} rows; {len(rows[0]) - 1} business columns; {len(raw)} source bytes')"
```

**Expected result:** `PASS: 15 rows; 12 business columns; ... source bytes`.

What happened:

1. the code opened the file read-only;
2. decoded it as Unicode Transformation Format 8-bit (UTF-8) text;
3. required the exact 12-column header;
4. required exactly 12 values per row;
5. refused duplicate or malformed work-item IDs;
6. returned the rows in memory;
7. wrote nothing.

### Stage 3 — Run only the deterministic rules

Run:

```powershell
& $pythonExe -c "from pathlib import Path; from src.course1_capstone.workflow import load_work_items, detect_issues; _, rows = load_work_items(Path('data/input/work_items.csv')); issues = detect_issues(rows); print(f'PASS: {len(issues)} issues'); [print(i['issue_id']) for i in issues]"
```

**Expected result:** `PASS: 13 issues`, followed by 13 identifiers such as:

```text
WI-0002|R007|owner_role
```

Read that identifier aloud as: “work item 0002, rule R007, field owner role.”
The field is part of the identity.

### Stage 4 — Prepare the complete worked run with AI disabled

Run:

```powershell
$workedWorkspace = Join-Path $moduleFolder 'worked'
& $pythonExe .\src\course1_capstone\cli.py prepare `
    --input .\data\input\work_items.csv `
    --expected .\tests\expected_issues.csv `
    --workspace $workedWorkspace `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) {
    throw 'The worked run safely stopped. Read the message above before changing anything.'
}
$workedRunLocator = (Get-Content -LiteralPath `
    (Join-Path $workedWorkspace 'latest_run.txt')).Trim()
$workedRunDir = Join-Path $workedWorkspace $workedRunLocator
Get-Content -LiteralPath (Join-Path $workedRunDir 'state.json')
Get-Content -LiteralPath (Join-Path $workedRunDir 'evaluation.json')
```

**Expected result:**

- the command says `PASS: prepared controlled run`;
- `current_state` is `needs_review`;
- `summary_generator` is `deterministic-fallback`;
- 13 issues were detected;
- true positives are 13;
- false positives and false negatives are 0;
- external actions are 0;
- no `outbox` folder exists.

`I_CONFIRM_SYNTHETIC_DATA_ONLY` forces a deliberate acknowledgement. It does
not magically prove that a file is synthetic. Never use the flag for real,
workplace, client, medical, or personal data.

### Stage 5 — Verify the exact answer key

Run:

```powershell
$found = Import-Csv -LiteralPath (Join-Path $workedRunDir 'issues\issues.csv')
$expected = Import-Csv -LiteralPath .\tests\expected_issues.csv
$foundKeys = $found | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)|$($_.field)" }
$expectedKeys = $expected | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)|$($_.field)" }
Compare-Object $expectedKeys $foundKeys
$found.Count
```

**Expected result:** `Compare-Object` prints nothing and the count is `13`.
Nothing means the two key sets match.

Never edit the expected file to make a difference disappear.

### Stage 6 — Prove that an identical retry is safe

Run the exact Stage 4 `prepare` command again. Then run:

```powershell
$workedRunLocatorAfterRetry = (Get-Content -LiteralPath `
    (Join-Path $workedWorkspace 'latest_run.txt')).Trim()
$workedRunDirAfterRetry = Join-Path $workedWorkspace $workedRunLocatorAfterRetry
$workedRunDir -eq $workedRunDirAfterRetry
(Get-Content -LiteralPath (Join-Path $workedRunDir 'audit\events.jsonl') |
    Select-String '"event_type": "duplicate_retry_ignored"').Count
Test-Path -LiteralPath (Join-Path $workedRunDir 'outbox')
```

**Expected result:**

- `True`: the same input created the same run;
- `1`: one retry event, even if you repeat the retry;
- `False`: no output was approved or exported.

### Stage 7 — See safe failure before changing anything

These failures are deliberate lessons. Red text is the correct result.
Every safe stop also prints a `FAILURE_EVIDENCE=` path and saves a
`failed_manual` command-attempt record with external actions 0. If a valid run
already exists, that record does not overwrite its last valid `current_state`.

Duplicate work-item ID:

```powershell
& $pythonExe .\src\course1_capstone\cli.py prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\duplicate_work_item_id.csv') `
    --workspace (Join-Path $moduleFolder 'failure-duplicate-id') `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$LASTEXITCODE
```

Expected: `SAFE STOP: duplicate_work_item_id...` and exit code `1`.

Unexpected header:

```powershell
& $pythonExe .\src\course1_capstone\cli.py prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\unexpected_header.csv') `
    --workspace (Join-Path $moduleFolder 'failure-header') `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$LASTEXITCODE
```

Expected: `SAFE STOP: header_mismatch...` and exit code `1`.

Malformed CSV:

```powershell
& $pythonExe .\src\course1_capstone\cli.py prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\malformed_input.csv') `
    --workspace (Join-Path $moduleFolder 'failure-malformed') `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$LASTEXITCODE
```

Expected: `SAFE STOP: malformed_input...` and exit code `1`.

Missing file:

```powershell
& $pythonExe .\src\course1_capstone\cli.py prepare `
    --input .\data\input\this-file-does-not-exist.csv `
    --workspace (Join-Path $moduleFolder 'failure-missing') `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$LASTEXITCODE
```

Expected: `SAFE STOP: missing_file...` and exit code `1`.

Do not “fix” a safe stop by weakening validation.

### Stage 8 — Record the worked design evidence

Create `evidence\module-04\worked_architecture.md` in Visual Studio Code:

```markdown
# Worked to-be architecture and ADR-001

ADR means Architecture Decision Record.
Status: accepted for synthetic Course 1 proof only

## Decision

Use a local deterministic Python checker before any optional AI summary.

## Why

- the 13 expected issues are defined by explicit rules;
- the source remains unchanged;
- each issue links to source row, field, raw value, and rule;
- failures stop visibly;
- no provider, network, key, or paid service is needed;
- CSV and JSON keep the evidence portable.

## Rejected alternatives

- manual inspection only: retained as fallback but less repeatable;
- AI issue detection: unnecessary and variable for R001-R011;
- source-system write-back: outside Course 1 and unsafe here.

## Flow

synthetic CSV -> validate -> R001-R011 -> source-linked issues
              -> deterministic fallback -> human review wait
invalid input -> failed/manual route

External actions: none.
Reassessment trigger: input contract, rule, severity, or action scope changes.
```

This is a completed example. Your recreation below must use your own words.

## Now recreate it yourself

Use the different six-row synthetic dataset below. Predict before running and
keep your first attempt as learning evidence.

### Recreation 1 — Copy a new synthetic input safely

Run:

```powershell
$recreatedInput = Join-Path $moduleFolder 'recreated_work_items.csv'
if (Test-Path -LiteralPath $recreatedInput) {
    Write-Host "KEEPING your existing $recreatedInput"
} else {
    Copy-Item -LiteralPath (Join-Path $courseRoot 'course1_capstone\fixtures\recreated_work_items.csv') -Destination $recreatedInput
    Write-Host "CREATED $recreatedInput"
}
Import-Csv -LiteralPath $recreatedInput | Format-Table work_item_id,status,received_date,due_date,completed_date,amount
```

### Recreation 2 — Predict before running

Create the prediction file at the exact path
`evidence\module-04\recreated_prediction.csv`. The command below writes only
the header on the first attempt and keeps an existing attempt unchanged:

```powershell
$predictionPath = Join-Path $moduleFolder 'recreated_prediction.csv'
if (Test-Path -LiteralPath $predictionPath) {
    Write-Host "KEEPING your existing $predictionPath"
} else {
    'work_item_id,rule_code,field' | Set-Content -LiteralPath $predictionPath -Encoding utf8
    Write-Host "CREATED $predictionPath"
}
notepad $predictionPath
```

Inspect each row and ask in order:

1. is a required value blank?
2. is status allowed?
3. is priority allowed?
4. are populated dates in `YYYY-MM-DD` form?
5. is due date before received date?
6. does completed status agree with completed date?
7. does active work have an owner role?
8. is amount a non-negative decimal?
9. does populated amount use EUR?
10. is source reference duplicated?
11. is open work overdue on 2026-07-26?

Add one line for each predicted issue. Save before continuing.

### Recreation 3 — Run and check your prediction

Run:

```powershell
$recreatedWorkspace = Join-Path $moduleFolder 'recreated'
$recreatedLatest = Join-Path $recreatedWorkspace 'latest_run.txt'
if (Test-Path -LiteralPath $recreatedLatest) {
    Write-Host "KEEPING your existing $recreatedWorkspace"
} else {
    & $pythonExe .\src\course1_capstone\cli.py prepare `
        --input $recreatedInput `
        --expected $predictionPath `
        --workspace $recreatedWorkspace `
        --ai-mode disabled `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw 'The recreated run safely stopped. Read the named reason above.'
    }
}
$recreatedRunLocator = (Get-Content -LiteralPath $recreatedLatest).Trim()
$recreatedRunDir = Join-Path $recreatedWorkspace $recreatedRunLocator
Get-Content -LiteralPath (Join-Path $recreatedRunDir 'evaluation.json')
```

Your first target is:

- detected issues: 5;
- true positives: 5;
- false positives: 0;
- false negatives: 0.

If not, keep your original prediction unchanged. Create the exact optional
notes and corrected-copy paths below without overwriting a prior attempt:

```powershell
$predictionNotesPath = Join-Path $moduleFolder 'recreated_prediction_notes.md'
$correctedPredictionPath = Join-Path $moduleFolder 'recreated_prediction_corrected.csv'
if (Test-Path -LiteralPath $predictionNotesPath) {
    Write-Host "KEEPING your existing $predictionNotesPath"
} else {
    @'
# Recreated prediction notes

What I predicted:
What the runner found:
Why they differed:
What I will check next time:
'@ | Set-Content -LiteralPath $predictionNotesPath -Encoding utf8
}
if (Test-Path -LiteralPath $correctedPredictionPath) {
    Write-Host "KEEPING your existing $correctedPredictionPath"
} else {
    Copy-Item -LiteralPath $predictionPath -Destination $correctedPredictionPath
}
notepad $predictionNotesPath
notepad $correctedPredictionPath
```

Do not erase evidence of the learning mistake. The original
`recreated_prediction.csv` remains your first attempt.

After your attempt, compare against the official answer:

```powershell
$official = Import-Csv -LiteralPath (Join-Path $courseRoot 'course1_capstone\fixtures\recreated_expected_issues.csv')
$recreatedFound = Import-Csv -LiteralPath (Join-Path $recreatedRunDir 'issues\issues.csv')
$officialKeys = $official | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)|$($_.field)" }
$recreatedKeys = $recreatedFound | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)|$($_.field)" }
Compare-Object $officialKeys $recreatedKeys
```

Expected: no output.

### Recreation 4 — Explain your design

Create `evidence\module-04\recreated_architecture.md` in your own words. This
command creates a blank heading once and keeps a prior version unchanged:

```powershell
$recreatedArchitecturePath = Join-Path $moduleFolder 'recreated_architecture.md'
if (Test-Path -LiteralPath $recreatedArchitecturePath) {
    Write-Host "KEEPING your existing $recreatedArchitecturePath"
} else {
    @'
# Recreated architecture

'@ | Set-Content -LiteralPath $recreatedArchitecturePath -Encoding utf8
}
notepad $recreatedArchitecturePath
```

Complete that file with:

- the different input and expected issue count;
- the validation gate;
- deterministic rules;
- canonical three-part issue identity;
- summary fallback;
- human-review wait;
- all four failure routes you ran;
- why external actions remain impossible.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path`, paste the full path below, and send:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
[PASTE FULL MODULE-04 PATH]

Do not edit, create, delete, move, rename, format, or execute anything. Do not
inspect a parent folder. This path must contain no secrets and no real client,
real work, personal, or medical data. Stop if it does.

Return:
1. PASS or NOT YET;
2. checks for the worked 13-issue run and recreated 5-issue run;
3. confirmation that comparisons use work_item_id + rule_code + field;
4. input hashes/source preservation, named states, idempotent retry, audit and
evaluation evidence, deterministic fallback, zero external actions;
5. safe-stop evidence for duplicate ID, header mismatch, malformed input, and
missing file;
6. worked and recreated architecture records;
7. the smallest learner-made corrections if NOT YET.

Remain read-only. Do not provide replacement files.
```

## Pass criteria

- [ ] Exact project Python is used through `$pythonExe`.
- [ ] Worked input has 15 rows and 12 business columns.
- [ ] Worked result matches all 13 three-part expected keys.
- [ ] Recreated result matches all 5 three-part expected keys.
- [ ] Every issue has source row, field, raw value, rule, severity, and date.
- [ ] An identical retry creates no duplicate logical effect.
- [ ] Duplicate ID, bad header, malformed input, and missing file safely stop.
- [ ] AI remains disabled and deterministic fallback is usable.
- [ ] No outbox exists and external actions equal 0.
- [ ] Both architecture records explain the controls.
- [ ] Codex returns `PASS` in read-only mode.

### Record your Module 4 PASS in Git

Only after Codex returns `PASS`:

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "src/course1_capstone"
git add -- "evidence\module-04"
git commit -m "complete module 4 evidence"
git status --short
```

If Git says `nothing to commit`, the same evidence may already be recorded.
Never add real data, secrets, or unrelated files.

## Consultant lens

The portable capability is not “writing Python.” It is defining a contract,
keeping source evidence, separating deterministic rules from variable
language, designing safe failures, and proving what a retry does.

## Capstone increment

The capstone now has one runnable input-to-review workflow, exact rule results,
source-linked evidence, audit events, evaluation, idempotency, failure routes,
and deterministic fallback. It still cannot export because no human approval
exists.

## Required artifact

`evidence/module-04` contains the worked run, the safely copied recreated
synthetic input, recreated run, unchanged first prediction, optional prediction
notes and corrected copy, four failure results, and both architecture records.
`src/course1_capstone` contains the unchanged reference runner.

## Test gate

All Module 4 pass criteria and the read-only Codex review must pass. The worked
comparison has 13 exact three-part keys; the recreation has 5; all four input
failures return exit code 1; the retry has one logical effect.

## Stop or rework

Stop and rework if a source file changes, a comparison omits `field`, a safe
failure appears successful, a retry duplicates evidence, an outbox exists, or
external actions are not zero.

## Common failures

- Running bare `python` instead of `& $pythonExe`.
- Treating red safe-stop text as a broken lesson.
- Editing the expected file to make a comparison pass.
- Erasing the first prediction instead of explaining a difference.
- Comparing only the work item and rule while dropping the field.

## Estimated time

12-16 hours, best completed as four to six sessions.

Suggested sessions: four to six sessions of about 2-3 hours.
