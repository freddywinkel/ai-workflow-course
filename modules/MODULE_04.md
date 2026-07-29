# Module 4 — Safely Assemble, Test, and Extend the Rule-based Workflow

## Outcome

You will safely assemble and test the first working part supplied by the
course, then author one isolated deterministic rule and its tests. The supplied
working part will:

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

## What the supplied runner and your bounded extension do, in normal language

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
$projectMarker = Join-Path $projectRoot 'COURSE_PROJECT.md'
$expectedMarker = @'
# Course 1 synthetic learner project

This folder is only for the fictional Course 1 practice project.
Never place real client, employer, medical, or personal data here.
'@
if (-not (Test-Path -LiteralPath $projectMarker -PathType Leaf)) {
    throw 'Course project marker missing. Do not enter or execute this folder.'
}
$actualMarker = (Get-Content -Raw -LiteralPath $projectMarker) -replace "`r`n", "`n"
if ($actualMarker -ne ($expectedMarker -replace "`r`n", "`n")) {
    throw 'Course project marker is unfamiliar. Do not enter or execute this folder.'
}
$savedGitRoot = git -C $projectRoot rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0 -or
    (Resolve-Path -LiteralPath $savedGitRoot).Path -ne
    (Resolve-Path -LiteralPath $projectRoot).Path) {
    throw 'The marked Course 1 Git repository is missing or belongs to another folder.'
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
$controlledWorkedInput = Join-Path $courseRoot 'practice_data\work_items.csv'
$controlledWorkedExpected = Join-Path $courseRoot 'practice_data\expected_issues.csv'
$learnerWorkedInput = Join-Path $projectRoot 'data\input\work_items.csv'
$learnerWorkedExpected = Join-Path $projectRoot 'tests\expected_issues.csv'
foreach ($pair in @(
    @($controlledWorkedInput,$learnerWorkedInput),
    @($controlledWorkedExpected,$learnerWorkedExpected)
)) {
    if (-not (Test-Path -LiteralPath $pair[0] -PathType Leaf) -or
        -not (Test-Path -LiteralPath $pair[1] -PathType Leaf) -or
        (Get-FileHash -LiteralPath $pair[0] -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $pair[1] -Algorithm SHA256).Hash) {
        throw "Worked synthetic fixture is missing, wrong-type, or changed. Nothing was executed: $($pair[1])"
    }
}
$runner = Join-Path $projectRoot 'src\course1_capstone\cli.py'
$sourceRunner = Join-Path $courseRoot 'course1_capstone'
$runnerFolder = Join-Path $projectRoot 'src\course1_capstone'
$runnerHashRecord = Join-Path $moduleFolder 'reference_runner_hashes.json'
$expectedRunnerNames = @('__init__.py','workflow.py','cli.py')
function Assert-ControlledCourseRunner {
    if ((Test-Path -LiteralPath $runnerFolder) -and
        -not (Test-Path -LiteralPath $runnerFolder -PathType Container)) {
        throw 'Runner destination exists but is not a folder. Nothing was executed.'
    }
    if (Test-Path -LiteralPath $runnerFolder -PathType Container) {
        $unexpectedRunnerEntries = @(
            Get-ChildItem -LiteralPath $runnerFolder -Force |
                Where-Object {
                    $expectedRunnerNames -cnotcontains $_.Name -and
                    -not ($_.PSIsContainer -and $_.Name -ceq '__pycache__')
                }
        )
        if ($unexpectedRunnerEntries.Count -gt 0) {
            throw 'The controlled runner folder contains an unexpected entry. Preserve it and ask for read-only diagnosis.'
        }
    }
    $runnerArtifactsExist =
        (Test-Path -LiteralPath $runnerHashRecord) -or
        @($expectedRunnerNames | Where-Object {
            Test-Path -LiteralPath (Join-Path $runnerFolder $_)
        }).Count -gt 0
    if (-not $runnerArtifactsExist) {
        Write-Host 'FIRST SESSION: Stage 1 must create and verify the controlled runner before it is used.'
        return $false
    }
    if (-not (Test-Path -LiteralPath $runnerHashRecord)) {
        foreach ($expectedRunnerName in $expectedRunnerNames) {
            $sourceFile = Join-Path $sourceRunner $expectedRunnerName
            $destinationFile = Join-Path $runnerFolder $expectedRunnerName
            if (Test-Path -LiteralPath $destinationFile) {
                if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf) -or
                    -not (Test-Path -LiteralPath $destinationFile -PathType Leaf) -or
                    (Get-FileHash -LiteralPath $sourceFile -Algorithm SHA256).Hash -ne
                    (Get-FileHash -LiteralPath $destinationFile -Algorithm SHA256).Hash) {
                    throw "Unrecorded partial runner copy is wrong-type or differs from the current course source: $expectedRunnerName"
                }
            }
        }
        Write-Host 'RECOVERABLE PARTIAL COPY: existing controlled files match; rerun Stage 1 to finish and record all three.'
        return $false
    }
    if (-not (Test-Path -LiteralPath $runnerHashRecord -PathType Leaf)) {
        throw 'Runner files exist without a valid Module 4 hash record. Nothing was executed; preserve them for read-only diagnosis.'
    }
    try {
        $savedRunnerHashes = Get-Content -Raw -LiteralPath $runnerHashRecord |
            ConvertFrom-Json
    } catch {
        throw 'The Module 4 runner-hash record is damaged. Nothing was executed.'
    }
    $savedRunnerNames = @($savedRunnerHashes | ForEach-Object { [string]$_.name })
    if (
        @($savedRunnerHashes).Count -ne $expectedRunnerNames.Count -or
        @(Compare-Object $expectedRunnerNames $savedRunnerNames -CaseSensitive).Count -ne 0
    ) {
        throw 'The Module 4 runner-hash record does not contain each exact controlled filename once.'
    }
    foreach ($expectedRunnerName in $expectedRunnerNames) {
        $sourceFile = Join-Path $sourceRunner $expectedRunnerName
        $destinationFile = Join-Path $runnerFolder $expectedRunnerName
        $saved = @($savedRunnerHashes | Where-Object {
            $_.name -ceq $expectedRunnerName
        })
        if ($saved.Count -ne 1 -or
            -not (Test-Path -LiteralPath $sourceFile -PathType Leaf) -or
            -not (Test-Path -LiteralPath $destinationFile -PathType Leaf)) {
            throw "Controlled runner evidence is missing or ambiguous for $expectedRunnerName. Nothing was executed."
        }
        $sourceHash = (Get-FileHash -LiteralPath $sourceFile -Algorithm SHA256).Hash
        $destinationHash = (Get-FileHash -LiteralPath $destinationFile -Algorithm SHA256).Hash
        if ($saved[0].source_sha256 -ne $sourceHash -or
            $saved[0].destination_sha256 -ne $destinationHash -or
            $sourceHash -ne $destinationHash) {
            throw "Controlled runner or course source changed for $expectedRunnerName. Nothing was executed; preserve everything and ask for read-only diagnosis before any upgrade."
        }
    }
    Write-Host 'VERIFIED the current course source, learner runner, and Module 4 hash record.'
    return $true
}
$runnerReady = Assert-ControlledCourseRunner
function Resolve-SavedCourseRun {
    param([string]$Workspace)
    $latest = Join-Path $Workspace 'latest_run.txt'
    if (-not (Test-Path -LiteralPath $latest)) {
        return $null
    }
    if (-not (Test-Path -LiteralPath $latest -PathType Leaf)) {
        throw "Saved run locator is not a file: $latest"
    }
    $locatorLines = @(Get-Content -LiteralPath $latest)
    if ($locatorLines.Count -ne 1) {
        throw "Saved run locator must contain exactly one line: $latest"
    }
    $locator = [string]$locatorLines[0]
    if (
        [string]::IsNullOrWhiteSpace($locator) -or
        $locator -cne $locator.Trim() -or
        [System.IO.Path]::IsPathRooted($locator) -or
        $locator -cnotmatch '^runs[\\/]RUN-[A-F0-9]{12}$'
    ) {
        throw "Saved run locator is empty or unsafe: $latest"
    }
    $runDir = Join-Path $Workspace $locator
    if (-not (Test-Path -LiteralPath $runDir -PathType Container)) {
        throw "Saved run folder is missing: $runDir"
    }
    $runsRoot = (Resolve-Path -LiteralPath (Join-Path $Workspace 'runs')).Path
    $resolvedRunDir = (Resolve-Path -LiteralPath $runDir).Path
    if ((Split-Path -Parent $resolvedRunDir) -ne $runsRoot) {
        throw "Saved run resolves outside its exact runs folder: $latest"
    }
    return $resolvedRunDir
}
$workedWorkspace = Join-Path $moduleFolder 'worked'
$workedRunDir = Resolve-SavedCourseRun $workedWorkspace
$recreatedInput = Join-Path $moduleFolder 'recreated_work_items.csv'
$predictionPath = Join-Path $moduleFolder 'recreated_prediction.csv'
$correctedPredictionPath = Join-Path $moduleFolder 'recreated_prediction_corrected.csv'
$officialExpectedPath = Join-Path $courseRoot 'course1_capstone\fixtures\recreated_expected_issues.csv'
$recreatedWorkspace = Join-Path $moduleFolder 'recreated'
$recreatedRunDir = Resolve-SavedCourseRun $recreatedWorkspace
$correctedWorkspace = Join-Path $moduleFolder 'recreated-corrected'
$correctedRunDir = Resolve-SavedCourseRun $correctedWorkspace
& $pythonExe --version
```

Always use `& $pythonExe`. Do not replace it with bare `python`; Windows could
silently select another installation.

Safe session stops are after Stage 4, after Stage 7, after Recreation 1, and
after Recreation 3. On return, run the complete block above. It re-verifies
all three runner files against both the current course source and the durable
Module 4 hash record, then reconstructs the worked, first-attempt, and
corrected run folders from their saved relative locators. You do not need to
replay a state-changing stage merely to restore variables.

Suggested sessions:

1. copy and verify the supplied runner, then complete the worked run;
2. force and explain the four worked safe failures;
3. predict and run the different synthetic recreation;
4. preserve, diagnose, and correct the different attempt;
5. author the isolated R012 rule and its normal/boundary/failure tests;
6. complete the read-only check and correction gate.

### How to use this long module

Work in focused blocks of at most 60 minutes and stop at the named safe points.
Label each block in your notes:

- **UNDERSTAND:** explain the input gate, three-part issue identity,
  deterministic fallback, safe failure, and why a retry has one logical effect;
- **RUN HELPER:** execute the protected copy, hash, locator, and preservation
  commands exactly. You do not need to memorise their syntax, but you must know
  their stated purpose and stop if their result differs;
- **MAKE:** create the prediction, architecture explanation, and isolated
  learner-authored rule yourself;
- **GATE:** compare the observed result with the exact expected state before
  continuing.

Mini-gate A is after Stage 4: explain source → input validation → rule result →
review wait. Mini-gate B is after Stage 7: name all four failures and their
manual route. Mini-gate C is after Recreation 5: connect every learner-authored
test to its requirement.

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
$runnerComparisons = @()
foreach ($name in '__init__.py','workflow.py','cli.py') {
    $source = Join-Path $sourceRunner $name
    $destination = Join-Path $runnerFolder $name
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        throw "Reference runner source is missing or is not a file: $source"
    }
    $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
    if (Test-Path -LiteralPath $destination) {
        if (-not (Test-Path -LiteralPath $destination -PathType Leaf)) {
            throw "Runner destination is not a file. Nothing was executed: $destination"
        }
        $destinationHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
        if ($destinationHash -ne $sourceHash) {
            throw "Existing runner file differs from the controlled course source. Nothing was executed: $destination"
        }
        Write-Host "VERIFIED existing $destination"
    } else {
        Copy-Item -LiteralPath $source -Destination $destination
        $destinationHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
        if ($destinationHash -ne $sourceHash) {
            throw "Copied runner hash does not match its source. Nothing was executed: $destination"
        }
        Write-Host "COPIED AND VERIFIED $destination"
    }
    $runnerComparisons += [PSCustomObject]@{
        name = $name
        source_sha256 = $sourceHash
        destination_sha256 = $destinationHash
    }
}
$runnerHashRecord = Join-Path $moduleFolder 'reference_runner_hashes.json'
if (Test-Path -LiteralPath $runnerHashRecord) {
    if (-not (Test-Path -LiteralPath $runnerHashRecord -PathType Leaf)) {
        throw 'The saved runner-hash record is not a file. Stop and inspect Module 4.'
    }
    try {
        $savedComparisons = Get-Content -Raw -LiteralPath $runnerHashRecord |
            ConvertFrom-Json
    } catch {
        throw 'The saved runner-hash record is damaged. Stop and ask Codex for read-only diagnosis.'
    }
    if (@($savedComparisons).Count -ne $runnerComparisons.Count) {
        throw 'The saved runner-hash record no longer matches the controlled runner.'
    }
    foreach ($current in $runnerComparisons) {
        $saved = @($savedComparisons | Where-Object { $_.name -ceq $current.name })
        if (
            $saved.Count -ne 1 -or
            $saved[0].source_sha256 -ne $current.source_sha256 -or
            $saved[0].destination_sha256 -ne $current.destination_sha256
        ) {
            throw "The saved runner-hash record differs for $($current.name). Nothing was executed."
        }
    }
    Write-Host "VERIFIED existing $runnerHashRecord"
} else {
    $runnerComparisons |
        ConvertTo-Json -Depth 3 |
        Set-Content -LiteralPath $runnerHashRecord -Encoding utf8
    Write-Host "CREATED $runnerHashRecord"
}
$runnerReady = Assert-ControlledCourseRunner
if (-not $runnerReady) {
    throw 'Stage 1 could not establish the controlled runner. Nothing may execute.'
}
Get-ChildItem -LiteralPath $runnerFolder -File
```

**Expected result:** three files are listed and
`reference_runner_hashes.json` records matching source and destination
SHA-256 values. On a later session, the command prints `VERIFIED` and does not
erase your files. A missing, wrong-type, changed, or partly copied runner file
stops before Python imports or executes it. Never bypass that stop or replace
the recorded hash by hand; ask Codex for read-only diagnosis.

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
if (-not $runnerReady) {
    throw 'Complete Stage 1 verification before importing or executing the runner.'
}
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
if (-not $runnerReady) {
    throw 'Complete Stage 1 verification before preparing a controlled run.'
}
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
$workedRunDir = Resolve-SavedCourseRun $workedWorkspace
if ($null -eq $workedRunDir) {
    throw 'The worked prepare command returned no validated saved run.'
}
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
$workedRunDirAfterRetry = Resolve-SavedCourseRun $workedWorkspace
if ($null -eq $workedRunDirAfterRetry) {
    throw 'The retry returned no validated saved run.'
}
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
$duplicateIdExit = $LASTEXITCODE
if ($duplicateIdExit -ne 1) {
    throw 'Duplicate-ID failure did not produce the exact safe-stop exit code.'
}
$duplicateIdExit
```

Expected: `SAFE STOP: duplicate_work_item_id...` and exit code `1`.

Unexpected header:

```powershell
& $pythonExe .\src\course1_capstone\cli.py prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\unexpected_header.csv') `
    --workspace (Join-Path $moduleFolder 'failure-header') `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$headerExit = $LASTEXITCODE
if ($headerExit -ne 1) {
    throw 'Header failure did not produce the exact safe-stop exit code.'
}
$headerExit
```

Expected: `SAFE STOP: header_mismatch...` and exit code `1`.

Malformed CSV:

```powershell
& $pythonExe .\src\course1_capstone\cli.py prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\malformed_input.csv') `
    --workspace (Join-Path $moduleFolder 'failure-malformed') `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$malformedExit = $LASTEXITCODE
if ($malformedExit -ne 1) {
    throw 'Malformed-input failure did not produce the exact safe-stop exit code.'
}
$malformedExit
```

Expected: `SAFE STOP: malformed_input...` and exit code `1`.

Missing file:

```powershell
& $pythonExe .\src\course1_capstone\cli.py prepare `
    --input .\data\input\this-file-does-not-exist.csv `
    --workspace (Join-Path $moduleFolder 'failure-missing') `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$missingExit = $LASTEXITCODE
if ($missingExit -ne 1) {
    throw 'Missing-file failure did not produce the exact safe-stop exit code.'
}
$missingExit
```

Expected: `SAFE STOP: missing_file...` and exit code `1`.

Do not “fix” a safe stop by weakening validation.

### Stage 8 — Record evidence about the supplied design

Run this create-once guard:

```powershell
$workedArchitecturePath = Join-Path $moduleFolder 'worked_architecture.md'
if (Test-Path -LiteralPath $workedArchitecturePath) {
    if (-not (Test-Path -LiteralPath $workedArchitecturePath -PathType Leaf)) {
        throw 'worked_architecture.md exists but is not a file.'
    }
    $workedArchitectureText = Get-Content -Raw -LiteralPath $workedArchitecturePath
    if ($null -eq $workedArchitectureText) { $workedArchitectureText = '' }
    $workedArchitectureFirstLine = Get-Content -LiteralPath $workedArchitecturePath -TotalCount 1
    if (-not [string]::IsNullOrEmpty($workedArchitectureText) -and
        $workedArchitectureFirstLine -cne '# Worked to-be architecture') {
        throw 'The existing worked architecture is unfamiliar. It was not opened or changed.'
    }
    if ($workedArchitectureText.Contains('## Rejected alternatives') -and
        $workedArchitectureText.Contains('Reassessment trigger:')) {
        Write-Host 'COMPLETE: keeping worked_architecture.md unchanged.'
    } else {
        Write-Host 'INCOMPLETE: continue the recognised synthetic file without duplicating sections.'
        & notepad.exe $workedArchitecturePath
    }
} else {
    New-Item -ItemType File -Path $workedArchitecturePath | Out-Null
    Write-Host 'NEW: paste the supplied lesson content once.'
    & notepad.exe $workedArchitecturePath
}
```

Before running it, confirm the named file is synthetic lesson work. A
wrong-type or unfamiliar existing file stops without opening or changing it;
preserve it and ask Codex for read-only diagnosis before a clearly numbered
retry. For `NEW`, paste the completed example below. For `INCOMPLETE`, add only
the missing section. For `COMPLETE`, do not paste again:

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
$recreatedInputSource = Join-Path $courseRoot 'course1_capstone\fixtures\recreated_work_items.csv'
if (-not (Test-Path -LiteralPath $recreatedInputSource -PathType Leaf)) {
    throw 'The controlled recreated input source is missing or is not a file.'
}
if (Test-Path -LiteralPath $recreatedInput) {
    if (-not (Test-Path -LiteralPath $recreatedInput -PathType Leaf)) {
        throw 'Recreated input path exists but is not a file. Preserve it and stop.'
    }
    if ((Get-FileHash -LiteralPath $recreatedInputSource -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $recreatedInput -Algorithm SHA256).Hash) {
        throw 'Recreated input changed from its controlled synthetic source. Preserve it and ask for read-only diagnosis.'
    }
    Write-Host "KEEPING your existing $recreatedInput"
} else {
    Copy-Item -LiteralPath $recreatedInputSource -Destination $recreatedInput
    if ((Get-FileHash -LiteralPath $recreatedInputSource -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $recreatedInput -Algorithm SHA256).Hash) {
        throw 'The new recreated input copy did not match its controlled source.'
    }
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
    if (-not (Test-Path -LiteralPath $predictionPath -PathType Leaf) -or
        (Get-Content -LiteralPath $predictionPath -TotalCount 1) -cne 'work_item_id,rule_code,field') {
        throw 'Existing prediction is the wrong type or has an unfamiliar header. Preserve it and ask for read-only diagnosis.'
    }
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
if (-not $runnerReady) {
    throw 'Stage 1 has not yet created and verified the controlled runner in this session.'
}
if ($null -ne $recreatedRunDir) {
    Write-Host "RESUME: keeping the saved first-attempt run $recreatedRunDir"
} else {
    & $pythonExe .\src\course1_capstone\cli.py prepare `
        --input $recreatedInput `
        --workspace $recreatedWorkspace `
        --ai-mode disabled `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw 'The recreated run safely stopped. Read the named reason above.'
    }
    $recreatedRunDir = Resolve-SavedCourseRun $recreatedWorkspace
}
$predictionRows = @(Import-Csv -LiteralPath $predictionPath)
$predictedKeys = @($predictionRows | ForEach-Object {
    "$($_.work_item_id)|$($_.rule_code)|$($_.field)"
} | Sort-Object -Unique)
$firstAttemptFound = @(Import-Csv -LiteralPath (Join-Path $recreatedRunDir 'issues\issues.csv'))
$foundKeys = @($firstAttemptFound | ForEach-Object {
    "$($_.work_item_id)|$($_.rule_code)|$($_.field)"
} | Sort-Object -Unique)
$truePositiveKeys = @($predictedKeys | Where-Object { $foundKeys -ccontains $_ })
$falsePositiveKeys = @($predictedKeys | Where-Object { $foundKeys -cnotcontains $_ })
$falseNegativeKeys = @($foundKeys | Where-Object { $predictedKeys -cnotcontains $_ })
[PSCustomObject]@{
    detected_issues = $foundKeys.Count
    predicted_unique_keys = $predictedKeys.Count
    duplicate_prediction_rows = $predictionRows.Count - $predictedKeys.Count
    true_positives = $truePositiveKeys.Count
    false_positives = $falsePositiveKeys.Count
    false_negatives = $falseNegativeKeys.Count
}
```

This first evaluation is diagnostic learning evidence. If your prediction was
right, it shows:

- detected issues: 5;
- true positives: 5;
- false positives: 0;
- false negatives: 0.

If not, that is an expected learning outcome, not a failed module. Keep your
original prediction and its run unchanged. Create the exact notes and
corrected-copy paths below without overwriting a prior attempt:

```powershell
$predictionNotesPath = Join-Path $moduleFolder 'recreated_prediction_notes.md'
$correctedPredictionPath = Join-Path $moduleFolder 'recreated_prediction_corrected.csv'
if (Test-Path -LiteralPath $predictionNotesPath) {
    if (-not (Test-Path -LiteralPath $predictionNotesPath -PathType Leaf) -or
        (Get-Content -LiteralPath $predictionNotesPath -TotalCount 1) -cne '# Recreated prediction notes') {
        throw 'Existing prediction notes are the wrong type or unfamiliar. Preserve them and stop.'
    }
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
    if (-not (Test-Path -LiteralPath $correctedPredictionPath -PathType Leaf) -or
        (Get-Content -LiteralPath $correctedPredictionPath -TotalCount 1) -cne 'work_item_id,rule_code,field') {
        throw 'Existing corrected prediction is the wrong type or has an unfamiliar header. Preserve it and stop.'
    }
    Write-Host "KEEPING your existing $correctedPredictionPath"
} else {
    Copy-Item -LiteralPath $predictionPath -Destination $correctedPredictionPath
}
notepad $predictionNotesPath
notepad $correctedPredictionPath
```

Do not erase evidence of the learning mistake. The original
`recreated_prediction.csv` remains your first attempt.

After your attempt, compare the detected rules with the official answer:

```powershell
$official = Import-Csv -LiteralPath (Join-Path $courseRoot 'course1_capstone\fixtures\recreated_expected_issues.csv')
$recreatedFound = Import-Csv -LiteralPath (Join-Path $recreatedRunDir 'issues\issues.csv')
$officialKeys = $official | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)|$($_.field)" }
$recreatedKeys = $recreatedFound | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)|$($_.field)" }
Compare-Object $officialKeys $recreatedKeys
```

Expected: no output.

Use that comparison to correct
`recreated_prediction_corrected.csv`. Keep its exact three-column header and
save one row for each of the five official keys. Then run this separate,
non-overwriting corrected evaluation:

```powershell
$correctedPredictionPath = Join-Path $moduleFolder 'recreated_prediction_corrected.csv'
$officialExpectedPath = Join-Path $courseRoot 'course1_capstone\fixtures\recreated_expected_issues.csv'
if (-not (Test-Path -LiteralPath $correctedPredictionPath -PathType Leaf) -or
    -not (Test-Path -LiteralPath $officialExpectedPath -PathType Leaf)) {
    throw 'The corrected prediction or controlled answer file is missing.'
}
$official = Import-Csv -LiteralPath $officialExpectedPath
$corrected = Import-Csv -LiteralPath $correctedPredictionPath
$correctedKeys = $corrected | ForEach-Object {
    "$($_.work_item_id)|$($_.rule_code)|$($_.field)"
}
$officialKeys = $official | ForEach-Object {
    "$($_.work_item_id)|$($_.rule_code)|$($_.field)"
}
$correctedDifference = @(Compare-Object $officialKeys $correctedKeys)
if ($correctedDifference.Count -ne 0) {
    $correctedDifference
    throw 'Corrected prediction is not yet exact. Keep editing the corrected copy; do not change the first attempt.'
}
if ($null -ne $correctedRunDir) {
    Write-Host "RESUME: keeping the saved corrected run $correctedRunDir"
} else {
    & $pythonExe $runner prepare `
        --input $recreatedInput `
        --expected $correctedPredictionPath `
        --workspace $correctedWorkspace `
        --ai-mode disabled `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw 'The corrected evaluation safely stopped. Read the named reason above.'
    }
    $correctedRunDir = Resolve-SavedCourseRun $correctedWorkspace
}
$correctedEvaluation = Get-Content -Raw -LiteralPath `
    (Join-Path $correctedRunDir 'evaluation.json') | ConvertFrom-Json
if ($correctedEvaluation.detected_issue_count -ne 5 -or
    $correctedEvaluation.true_positives -ne 5 -or
    $correctedEvaluation.false_positives -ne 0 -or
    $correctedEvaluation.false_negatives -ne 0) {
    throw 'Corrected evaluation did not reach the exact 5/5/0/0 acceptance result.'
}
$correctedEvaluation
```

Expected: detected `5`, true positive `5`, false positive `0`, false negative
`0`. The first-attempt workspace remains evidence of what you initially
predicted; the corrected workspace is the Module 4 acceptance evidence.

### Recreation 4 — Explain the supplied design and your configuration

Create `evidence\module-04\recreated_architecture.md` in your own words. This
command creates a blank heading once and keeps a prior version unchanged:

```powershell
$recreatedArchitecturePath = Join-Path $moduleFolder 'recreated_architecture.md'
if (Test-Path -LiteralPath $recreatedArchitecturePath) {
    if (-not (Test-Path -LiteralPath $recreatedArchitecturePath -PathType Leaf) -or
        (Get-Content -LiteralPath $recreatedArchitecturePath -TotalCount 1) -cne '# Recreated architecture') {
        throw 'Existing recreated architecture is the wrong type or unfamiliar. Preserve it and stop.'
    }
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

### Recreation 5 — Author one bounded deterministic rule

Until this point you assembled, operated, and challenged a controlled runner
supplied by the course. That is important implementation work, but it is not
the same as independently authoring workflow logic. This small isolated task is
the exact boundary of the Course 1 “build” claim. Do not edit the supplied
runner.

First study this complete worked pattern. Imagine this first block is saved as
`follow_up_rule.py`:

```python
def follow_up_due(days_open, maximum_days):
    if (
        type(days_open) is not int
        or type(maximum_days) is not int
        or days_open < 0
        or maximum_days < 0
    ):
        raise ValueError("days_open and maximum_days must be non-negative integers")
    return days_open > maximum_days
```

For this worked rule:

- `2, 5` is a normal non-match;
- `5, 5` is the exact boundary and is still a non-match;
- `6, 5` is immediately beyond the boundary and matches;
- text, a Boolean value such as `True`, or a negative number is invalid and
  raises a visible error;
- the function returns a value and has no file, network, or other side effect.

This is the complete worked test pattern for that first rule:

```python
import unittest

from follow_up_rule import follow_up_due


class FollowUpDueTests(unittest.TestCase):
    def test_normal_non_match(self):
        self.assertFalse(follow_up_due(2, 5))

    def test_exact_boundary(self):
        self.assertFalse(follow_up_due(5, 5))

    def test_one_beyond_boundary(self):
        self.assertTrue(follow_up_due(6, 5))

    def test_text_is_invalid(self):
        with self.assertRaises(ValueError):
            follow_up_due("six", 5)

    def test_boolean_is_invalid(self):
        with self.assertRaises(ValueError):
            follow_up_due(True, 5)

    def test_negative_is_invalid(self):
        with self.assertRaises(ValueError):
            follow_up_due(-1, 5)


if __name__ == "__main__":
    unittest.main()
```

`unittest` is Python's built-in test framework. The second import line brings
`follow_up_due` from the separate `follow_up_rule.py` file into the test file;
without that line, the test would stop with a `NameError`, which means Python
does not know the name being called. Each method whose name begins with
`test_` is one check. `assertFalse` and `assertTrue` compare the returned result
with the expected Boolean value. `assertRaises` passes only when the named
error occurs inside its indented block. The final two lines let the file run
the tests when opened as a program. The exact-type check deliberately rejects
`True` and `False`: Python otherwise treats Boolean values as a special kind of
integer, but the business requirement permits quantities only. Study this
pattern; do not save it as your recreation.

Now author a different rule from this requirement:

> Given `remaining_units` and `reorder_floor`, return reason code `R012` only
> when remaining units are below the floor. Equality is not an issue. Both
> inputs must be non-negative quantity integers; text, Boolean values, other
> wrong types, and negative values must raise `ValueError`. The function must
> not read or write a file, use the network, or change another value.

Create three files once:

```powershell
$learnerRuleFiles = @{
    'learner_stock_rule.py' = '# Learner-authored deterministic rule'
    'test_learner_stock_rule.py' = '# Learner-authored rule tests'
    'learner_stock_rule_evidence.md' = '# Learner-authored rule evidence'
}
foreach ($entry in $learnerRuleFiles.GetEnumerator()) {
    $path = Join-Path $moduleFolder $entry.Key
    if (Test-Path -LiteralPath $path) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf) -or
            (Get-Content -LiteralPath $path -TotalCount 1) -cne $entry.Value) {
            throw "Existing learner-rule path is unfamiliar. Preserve it and stop: $path"
        }
        Write-Host "KEEPING existing $($entry.Key)"
    } else {
        $entry.Value | Set-Content -LiteralPath $path -Encoding utf8
        Write-Host "CREATED $($entry.Key)"
    }
}
notepad (Join-Path $moduleFolder 'learner_stock_rule.py')
notepad (Join-Path $moduleFolder 'test_learner_stock_rule.py')
```

Write the function yourself. Name it `stock_floor_reason_code`. Write at least
six `unittest` tests yourself:

1. a normal value above the floor returns `None`;
2. equality at the exact boundary returns `None`;
3. one unit below the boundary returns `R012`;
4. text input raises `ValueError`;
5. a Boolean input raises `ValueError`;
6. a negative input raises `ValueError`.

In `test_learner_stock_rule.py`, keep the required heading as the first line.
Then make these the first two non-comment code lines:

```python
import unittest
from learner_stock_rule import stock_floor_reason_code
```

The second line imports your function from `learner_stock_rule.py`. Both files
must be in the same Module 4 folder. If you omit that line, the tests cannot
call your function.

Do not copy the worked function and only rename it. Your code must return the
reason code rather than a Boolean value and your tests must call your function.
Run the tests and preserve a numbered result:

```powershell
$learnerTestNumber = 1
do {
    $learnerTestOutput = Join-Path $moduleFolder (
        'learner_rule_test_attempt_{0:D2}.txt' -f $learnerTestNumber
    )
    $learnerTestNumber += 1
} while (Test-Path -LiteralPath $learnerTestOutput)

& $pythonExe -m unittest -v test_learner_stock_rule.py 2>&1 |
    Tee-Object -FilePath $learnerTestOutput
$learnerTestExit = $LASTEXITCODE
if ($learnerTestExit -ne 0) {
    throw "Learner-authored rule tests did not pass. Preserve this attempt and correct only the named problem."
}
"PASS: learner-authored rule tests"
```

Expected output includes `Ran 6 tests`, `OK`, and
`PASS: learner-authored rule tests`. If you add more useful tests, the count may
be higher but never lower.

Complete `learner_stock_rule_evidence.md` with:

- the requirement in your own words;
- the input, output, invalid-input behavior, and side-effect boundary;
- a table linking every test to normal, exact-boundary, beyond-boundary, or
  failure behavior;
- the relative path to the passing numbered test output;
- one limitation;
- an explanation of why this one isolated rule does not mean you built the
  supplied capstone runner independently.

## Ask Codex to check your work

Run both commands and paste each full path into its matching placeholder:

```powershell
(Resolve-Path $moduleFolder).Path
(Resolve-Path (Join-Path $projectRoot 'src\course1_capstone')).Path
```

Then send:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only these two full paths:
[PASTE FULL MODULE-04 PATH]
[PASTE FULL SRC\COURSE1_CAPSTONE PATH]

Learner attestation: I created these files for this fictional exercise and
have not knowingly put real client, employer, personal, medical, credential,
or secret data in them. This statement is an attestation, not proof.

You may only list names, read files, and calculate hashes inside the two
authorised folders. Do not create, edit, delete, rename, move, or format any
file. Do not
execute the runner, lesson scripts, or tests, use a network, or inspect a
parent or other location. If apparent sensitive data is noticed,
do not quote or repeat it: return NOT YET with only the filename and general
category, then stop. If none is noticed, say that non-detection is not proof
that none exists.

Return:
1. PASS or NOT YET;
2. checks for the worked 13-issue run, preserved first prediction run, and
corrected 5/5/0/0 recreation run;
3. confirmation that comparisons use work_item_id + rule_code + field;
4. input hashes/source preservation, runner hashes against the Module 4 record,
named states, idempotent retry, audit and evaluation evidence, deterministic
fallback, and zero recorded external actions;
5. safe-stop evidence for duplicate ID, header mismatch, malformed input, and
missing file;
6. worked and recreated architecture records;
7. learner_stock_rule.py implements the stated R012 requirement without a side
effect; test_learner_stock_rule.py explicitly imports
stock_floor_reason_code from learner_stock_rule and has at least six
learner-authored normal, exact-boundary, beyond-boundary, text-input,
Boolean-input, and negative-input tests; the latest numbered output reports OK;
learner_stock_rule_evidence.md connects the tests to the requirement and states
the build limitation;
8. the smallest learner-made corrections if NOT YET.

Remain read-only. Do not provide replacement files.
```

## Pass criteria

- [ ] Exact project Python is used through `$pythonExe`.
- [ ] All three copied runner files match the controlled course source by
      SHA-256 before any import or execution.
- [ ] Worked input has 15 rows and 12 business columns.
- [ ] Worked result matches all 13 three-part expected keys.
- [ ] The original recreated prediction/run is preserved, and the separate
      corrected recreation reaches detected 5, true positive 5, false positive
      0, and false negative 0 against all five three-part expected keys.
- [ ] Every issue has source row, field, raw value, rule, severity, and date.
- [ ] An identical retry creates no duplicate logical effect.
- [ ] Duplicate ID, bad header, malformed input, and missing file safely stop.
- [ ] AI remains disabled and deterministic fallback is usable.
- [ ] No outbox exists and external actions equal 0.
- [ ] Both architecture records explain the controls.
- [ ] My isolated `stock_floor_reason_code` implements the written R012
      requirement and has no side effect.
- [ ] `test_learner_stock_rule.py` imports `stock_floor_reason_code` from
      `learner_stock_rule` before calling it.
- [ ] At least six normal, boundary, and failure tests pass and the numbered
      output is preserved.
- [ ] My evidence links each test to the requirement and says honestly that the
      supplied runner was assembled rather than independently authored.
- [ ] Codex returns `PASS` in read-only mode.

### Record your Module 4 PASS in Git

Only after Codex returns `PASS`, rerun the complete **Start or resume safely**
block in this same PowerShell window so the exact marker and Git-root checks
pass again:

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "src/course1_capstone"
git add -- "evidence\module-04"
git commit --only -m "complete module 4 evidence" -- `
    "src/course1_capstone" "evidence/module-04"
git status --short
```

`git commit --only` restricts this checkpoint to the two repeated paths, even
if a different file had already been staged. If Git says `nothing to commit`,
the same evidence may already be recorded. Never add real data, secrets, or
unrelated files.

## Consultant lens

The portable capability is not “writing Python.” It is defining a contract,
keeping source evidence, separating deterministic rules from variable
language, designing safe failures, and proving what a retry does.

## Capstone increment

The capstone now has one supplied runnable input-to-review workflow, exact rule
results, source-linked evidence, audit events, evaluation, idempotency, failure
routes, and deterministic fallback. Separately, you authored one bounded rule
with normal, boundary, and failure tests. The capstone still cannot export
because no human approval exists.

## Required artifact

`evidence/module-04` contains the worked run, the safely copied recreated
synthetic input, recreated run, unchanged first prediction, optional prediction
notes and corrected copy, four failure results, and both architecture records.
It also contains the isolated learner-authored stock rule, its tests, numbered
test output, and evidence record.
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

12–16 hours, best completed as 12–18 focused study blocks of 45–60 minutes.
This is an **AUTHOR ESTIMATE — NOT BEGINNER MEASURED**.
