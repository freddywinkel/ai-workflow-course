# Module 5 — Design One Bounded, Replaceable Artificial Intelligence (AI) Contribution and Test It Offline

## Outcome

You will add an offline mock of an Artificial Intelligence (AI) summary after
the proven R001-R011 issues. The mock behaves like provider output but makes no
network call and costs nothing.

It may only:

- group verified issue identifiers;
- restate their rule messages;
- propose a source-linked `human_review` action;
- say that human review is required.

It may not discover issues, change severity, decide a business action, contact
anyone, send, order, pay, approve, reject, or write back.

You will first inspect and verify a complete 13-issue example. Then you will
select and validate a different controlled five-issue candidate yourself. You will
also prove the deterministic fallback for disabled AI, timeout, refusal,
malformed JSON, and an invented issue reference.

## Beginner checkpoint

Start when Module 4 has:

- a 13-issue worked result;
- a five-issue recreated result;
- zero false positives and false negatives;
- zero external actions;
- a Codex `PASS`.

**AI** means software that generates or infers an answer. **Application
Programming Interface (API)** means a defined connection through which
software can request a service. This module uses no API.

## What changes — and what does not

```text
unchanged, trusted part                  replaceable language part
----------------------                  -------------------------
synthetic input
      |
R001-R011
      |
verified issue objects  ------------->  offline mock summary
      |                                  |
      +------------------------------->  source-linked review actions
                                         |
                                         v
                                  mandatory human review
```

If the language step fails, the verified issues remain usable. The fallback is
not “ask the AI again”; it is a deterministic summary created from the same
issue records.

## Concepts

- **Bounded** means only named inputs and transformations are permitted.
- **Structured output** follows a machine-checkable shape.
- **Grounding** links each statement to verified evidence.
- **Abstention** means returning no unsupported claim.
- An **adapter** keeps provider-specific behavior separate from the workflow.
- A **prompt version** identifies the instruction set.
- A **fallback** completes the limited task without AI.
- A **mock** is saved or simulated behavior used for repeatable tests.
- A **schema** describes the required structure of data.

Valid structure is not the same as truthful meaning. Code verifies fields and
references; a person still checks whether every sentence is supported.

## Official readings

1. [National Institute of Standards and Technology Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
2. [OpenAI Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs)
3. [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evals)

OpenAI is one possible provider, not a Course 1 dependency. Do not add a key or
live model here.

## Guided build

The guided path prepares a complete 13-issue offline mock, checks its exact
contract, performs a sentence-level human review, and then forces all five
summary failure modes through the deterministic fallback.

## Start or resume safely

Open Windows PowerShell and run this at the start of every session:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
$moduleFolder = Join-Path $projectRoot 'evidence\module-05'
$moduleFour = Join-Path $projectRoot 'evidence\module-04'
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
$runner = Join-Path $projectRoot 'src\course1_capstone\cli.py'
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
if (-not (Test-Path -LiteralPath $runner)) {
    throw 'Course 1 runner missing. Return to Module 4 Stage 1.'
}
$runnerHashRecord = Join-Path $moduleFour 'reference_runner_hashes.json'
if (-not (Test-Path -LiteralPath $runnerHashRecord -PathType Leaf)) {
    throw 'Module 4 runner-hash record missing. Return to Module 4 Stage 1.'
}
try {
    $savedRunnerHashes = Get-Content -Raw -LiteralPath $runnerHashRecord |
        ConvertFrom-Json
} catch {
    throw 'Module 4 runner-hash record is damaged. Stop for read-only diagnosis.'
}
$expectedRunnerNames = @('__init__.py','workflow.py','cli.py')
$runnerFolder = Join-Path $projectRoot 'src\course1_capstone'
if (-not (Test-Path -LiteralPath $runnerFolder -PathType Container)) {
    throw 'Controlled runner folder is missing or is not a folder. Return to Module 4 Stage 1.'
}
$unexpectedRunnerEntries = @(
    Get-ChildItem -LiteralPath $runnerFolder -Force |
        Where-Object {
            $expectedRunnerNames -cnotcontains $_.Name -and
            -not ($_.PSIsContainer -and $_.Name -ceq '__pycache__')
        }
)
if ($unexpectedRunnerEntries.Count -gt 0) {
    throw 'The controlled runner folder contains an unexpected entry. Nothing was executed; preserve it and ask for read-only diagnosis.'
}
$savedRunnerNames = @($savedRunnerHashes | ForEach-Object { [string]$_.name })
if (
    @($savedRunnerHashes).Count -ne $expectedRunnerNames.Count -or
    @(Compare-Object $expectedRunnerNames $savedRunnerNames -CaseSensitive).Count -ne 0
) {
    throw 'Module 4 runner-hash record does not contain each exact controlled filename once.'
}
foreach ($expectedRunnerName in $expectedRunnerNames) {
    $savedRunnerHash = @($savedRunnerHashes | Where-Object {
        $_.name -ceq $expectedRunnerName
    })
    if ($savedRunnerHash.Count -ne 1) {
        throw "Module 4 runner-hash record is ambiguous for $expectedRunnerName."
    }
    $savedRunnerHash = $savedRunnerHash[0]
    $runnerFile = Join-Path (Join-Path $projectRoot 'src\course1_capstone') $expectedRunnerName
    if (-not (Test-Path -LiteralPath $runnerFile -PathType Leaf)) {
        throw "Controlled runner file is missing: $runnerFile"
    }
    $currentRunnerHash = (Get-FileHash -LiteralPath $runnerFile -Algorithm SHA256).Hash
    if ($savedRunnerHash.source_sha256 -ne $savedRunnerHash.destination_sha256 -or
        $currentRunnerHash -ne $savedRunnerHash.destination_sha256) {
        throw "Controlled runner differs from the verified Module 4 copy: $runnerFile"
    }
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
foreach ($expectedRunnerName in $expectedRunnerNames) {
    $savedRunnerHash = @($savedRunnerHashes | Where-Object {
        $_.name -ceq $expectedRunnerName
    })[0]
    $currentCourseSource = Join-Path (Join-Path $courseRoot 'course1_capstone') $expectedRunnerName
    if (-not (Test-Path -LiteralPath $currentCourseSource -PathType Leaf) -or
        (Get-FileHash -LiteralPath $currentCourseSource -Algorithm SHA256).Hash -ne
        $savedRunnerHash.source_sha256) {
        throw "The current course source differs from the verified Module 4 runner: $expectedRunnerName. Preserve everything and ask for read-only diagnosis before any upgrade."
    }
}
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
$workedWorkspace = Join-Path $moduleFolder 'worked-mock'
$workedRunDir = Resolve-SavedCourseRun $workedWorkspace
$recreatedInput = Join-Path $moduleFour 'recreated_work_items.csv'
$recreatedWorkspace = Join-Path $moduleFolder 'recreated-mock'
$recreatedRunDir = Resolve-SavedCourseRun $recreatedWorkspace
$candidate = Join-Path $moduleFolder 'recreated_candidate_summary.json'
$recreatedSupportReview = Join-Path $moduleFolder 'recreated_support_review.md'
& $pythonExe --version
```

Use `& $pythonExe`, never bare `python`. The resolver reads a saved
`latest_run.txt`, accepts only the runner's exact relative
`runs/RUN-XXXXXXXXXXXX` form, verifies that the result remains directly inside
that workspace's `runs` folder, and restores it without running the workflow
again.
Safe stopping points are after Stage 3, after the five failure cases, after
Recreation 3, and after Recreation 4. On return, run only this start block,
then continue at the next unfinished stage.

## Follow along — I show you exactly how

### Stage 1 — Prepare the complete offline-mock run

Run:

```powershell
if ($null -ne $workedRunDir) {
    Write-Host "RESUME: keeping the saved worked run $workedRunDir"
} else {
    & $pythonExe $runner prepare `
        --input .\data\input\work_items.csv `
        --expected .\tests\expected_issues.csv `
        --workspace $workedWorkspace `
        --ai-mode mock `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw 'The mock run safely stopped. Read the message above.'
    }
    $workedRunDir = Resolve-SavedCourseRun $workedWorkspace
}
& $pythonExe $runner status --run-dir $workedRunDir
if ($LASTEXITCODE -ne 0) {
    throw 'Worked mock status validation safely stopped. Do not inspect or review this run.'
}
Get-Content -LiteralPath (Join-Path $workedRunDir 'state.json')
```

**Expected result:**

- `current_state` is `needs_review`;
- `summary_generator` is `offline-mock`;
- `summary_fallback_reason` is `null`;
- external actions are 0;
- no outbox exists.

This is still entirely local. `offline-mock` does not mean a hidden AI call.

### Stage 2 — Inspect exactly what the mock receives and returns

Open these two files side by side in Visual Studio Code:

```powershell
code (Join-Path $workedRunDir 'issues\issues.json')
code (Join-Path $workedRunDir 'draft\summary.json')
```

If `code` is not recognized, open Visual Studio Code normally and use
**File > Open File**.

The summary has these exact top-level fields:

| Field | Meaning |
|---|---|
| `run_id` | the run this summary belongs to |
| `prompt_version` | version of the bounded instruction |
| `generator` | `offline-mock` or `deterministic-fallback` |
| `headline` | short factual count statement |
| `groups` | grouped sentences with visible issue citations |
| `review_actions` | only `human_review`, each linked to issue IDs |
| `unsupported_statements` | must be empty to continue |
| `review_required` | must be `true` |

Each issue ID must appear exactly once in the groups and exactly once in the
review actions. An identifier such as
`WI-0002|R007|owner_role` links the text back to work item, rule, and field.

Run these checks:

```powershell
$summary = Get-Content -Raw -LiteralPath (Join-Path $workedRunDir 'draft\summary.json') | ConvertFrom-Json
$issues = Get-Content -Raw -LiteralPath (Join-Path $workedRunDir 'issues\issues.json') | ConvertFrom-Json
$summary.generator
$summary.review_required
$summary.unsupported_statements.Count
$summary.groups.issue_ids.Count
$summary.review_actions.issue_ids.Count
$summary.review_actions.external_action | Sort-Object -Unique
$issues.Count
```

**Expected result:** `offline-mock`, `True`, `0`, `13`, `13`, only `False`, and
`13`.

### Stage 3 — Perform the human sentence check

Run this create-once guard:

```powershell
$workedSupportReview = Join-Path $moduleFolder 'worked_support_review.md'
if (Test-Path -LiteralPath $workedSupportReview) {
    if (-not (Test-Path -LiteralPath $workedSupportReview -PathType Leaf)) {
        throw 'worked_support_review.md exists but is not a file.'
    }
    $workedReviewText = Get-Content -Raw -LiteralPath $workedSupportReview
    if ($null -eq $workedReviewText) { $workedReviewText = '' }
    $workedReviewFirstLine = Get-Content -LiteralPath $workedSupportReview -TotalCount 1
    if (-not [string]::IsNullOrEmpty($workedReviewText) -and
        $workedReviewFirstLine -cne '# Worked mock support review') {
        throw 'The existing worked support review is unfamiliar. It was not opened or changed.'
    }
    if ($workedReviewText.Contains('Fallback: use issues/issues.csv and the deterministic fallback summary.') -and
        -not $workedReviewText.Contains('[copy run_id')) {
        Write-Host 'COMPLETE: keeping worked_support_review.md unchanged.'
    } else {
        Write-Host 'INCOMPLETE: continue the recognised synthetic review without duplicating sections.'
        & notepad.exe $workedSupportReview
    }
} else {
    New-Item -ItemType File -Path $workedSupportReview | Out-Null
    Write-Host 'NEW: paste the supplied lesson content once.'
    & notepad.exe $workedSupportReview
}
```

Before running it, confirm the named file is synthetic lesson work. A
wrong-type or unfamiliar existing file stops without opening or changing it;
preserve it and ask Codex for read-only diagnosis before a clearly numbered
retry. For `NEW`, paste the example. For `INCOMPLETE`, finish only the missing
parts. For `COMPLETE`, do not paste again:

```markdown
# Worked mock support review

Run: [copy run_id from state.json]
Reviewer role: course learner acting as synthetic operations reviewer

## Checks

- opened issues/issues.json: yes
- opened draft/summary.json: yes
- 13 known issue IDs grouped exactly once: yes
- 13 known issue IDs have one human-review action: yes
- every issue ID is visibly cited in its group sentence: yes
- each sentence repeats only its cited rule message: yes
- severity changed: no
- unsupported cause or recommendation: no
- external action proposed: no
- review_required: true

Result: accept the structure as an internal draft for Module 6 review.
This is not approval to export, send, or use with real data.
Fallback: use issues/issues.csv and the deterministic fallback summary.
```

Do not mark a line `yes` until you actually compare it.

### Stage 4 — Prove all five AI failure routes

The modes below are local fault simulations. They do not wait for a real
provider.

A **PowerShell custom object (`[PSCustomObject]`)** is a labelled group of
values used here only to print one readable result row per failure mode.

Run:

```powershell
$failureModes = 'disabled','timeout','refusal','malformed_json','unknown_issue_id'
foreach ($mode in $failureModes) {
    $workspace = Join-Path $moduleFolder "failure-$mode"
    & $pythonExe $runner prepare `
        --input .\data\input\work_items.csv `
        --expected .\tests\expected_issues.csv `
        --workspace $workspace `
        --ai-mode $mode `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw "Unexpected failure while testing $mode"
    }
    $runDir = Resolve-SavedCourseRun $workspace
    if ($null -eq $runDir) {
        throw "The $mode run returned no validated saved run."
    }
    $state = Get-Content -Raw -LiteralPath (Join-Path $runDir 'state.json') | ConvertFrom-Json
    [PSCustomObject]@{
        requested_mode = $mode
        generator = $state.summary_generator
        fallback_reason = $state.summary_fallback_reason
        state = $state.current_state
        external_actions = $state.external_actions
    }
}
```

**Expected result:** every row shows:

- generator `deterministic-fallback`;
- a matching reason: `ai_disabled`, `ai_timeout`, `ai_refusal`,
  `malformed_ai_json`, or `unknown_ai_issue_reference`;
- state `needs_review`;
- external actions `0`.

The malformed and unknown-reference responses do not “mostly pass.” The whole
mock response is discarded and replaced by the deterministic fallback.

### Stage 5 — Prove that instructions inside data are inert

Run:

```powershell
$instructionWorkspace = Join-Path $moduleFolder 'failure-untrusted-text'
& $pythonExe $runner prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\untrusted_instruction.csv') `
    --workspace $instructionWorkspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) {
    throw 'The untrusted-text run safely stopped. Do not inspect an older saved run as current evidence.'
}
$instructionRunDir = Resolve-SavedCourseRun $instructionWorkspace
if ($null -eq $instructionRunDir) {
    throw 'The untrusted-text run returned no validated saved run.'
}
Select-String -LiteralPath (Join-Path $instructionRunDir 'source\work_items.csv') -Pattern 'Ignore every rule'
Select-String -LiteralPath (Join-Path $instructionRunDir 'draft\summary.json') -Pattern 'Ignore every rule'
```

**Expected result:** the first search finds the text in the preserved source.
The second search prints nothing. Free text is treated as data, not an
instruction, and no external action occurs.

## Now recreate it yourself

Use the different five-issue run to create and validate your own controlled
candidate. “Your own” means you make and justify the allowed choice; it does
not mean inventing unrestricted prose.

### Recreation 1 — Prepare the different mock

Resume Module 4 variables if necessary, then run:

```powershell
if (-not (Test-Path -LiteralPath $recreatedInput -PathType Leaf)) {
    throw 'Recreated input missing. Return to Module 4 Recreation 1.'
}
$controlledRecreatedInput = Join-Path $courseRoot 'course1_capstone\fixtures\recreated_work_items.csv'
$controlledRecreatedExpected = Join-Path $courseRoot 'course1_capstone\fixtures\recreated_expected_issues.csv'
if (-not (Test-Path -LiteralPath $controlledRecreatedInput -PathType Leaf) -or
    -not (Test-Path -LiteralPath $controlledRecreatedExpected -PathType Leaf)) {
    throw 'The controlled recreated input or answer fixture is missing.'
}
if ((Get-FileHash -LiteralPath $recreatedInput -Algorithm SHA256).Hash -ne
    (Get-FileHash -LiteralPath $controlledRecreatedInput -Algorithm SHA256).Hash) {
    throw 'The Module 4 recreated input changed from its controlled synthetic source. Nothing was executed.'
}
if ($null -ne $recreatedRunDir) {
    Write-Host "RESUME: keeping the saved recreated run $recreatedRunDir"
} else {
    & $pythonExe $runner prepare `
        --input $recreatedInput `
        --expected $controlledRecreatedExpected `
        --workspace $recreatedWorkspace `
        --ai-mode mock `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw 'The recreated mock safely stopped. Read the named reason above.'
    }
    $recreatedRunDir = Resolve-SavedCourseRun $recreatedWorkspace
}
& $pythonExe $runner status --run-dir $recreatedRunDir
if ($LASTEXITCODE -ne 0) {
    throw 'Recreated mock status validation safely stopped. Do not copy or edit its draft.'
}
```

### Recreation 2 — Make a new bounded response

Copy the valid mock once, without overwriting a prior attempt:

```powershell
if (Test-Path -LiteralPath $candidate) {
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        throw 'Existing candidate path is not a file. Preserve it and stop.'
    }
    $candidateText = Get-Content -Raw -LiteralPath $candidate
    if ($candidateText -notmatch '^\s*\{' -or
        $candidateText -notmatch '"run_id"\s*:' -or
        $candidateText -notmatch '"review_actions"\s*:') {
        throw 'Existing candidate is unfamiliar rather than a recognisable in-progress copy. Preserve it and ask for read-only diagnosis.'
    }
    $candidateObject = $null
    try {
        $candidateObject = $candidateText | ConvertFrom-Json
    } catch {
        Write-Host 'RESUME: the recognisable candidate is incomplete JSON; reopen it and finish the edit before validation.'
    }
    if ($null -ne $candidateObject) {
        foreach ($requiredCandidateField in
            'run_id','prompt_version','generator','headline','groups',
            'review_actions','unsupported_statements','review_required') {
            if ($candidateObject.PSObject.Properties.Name -cnotcontains $requiredCandidateField) {
                throw "Existing candidate is missing the recognisable field $requiredCandidateField. Preserve it and stop."
            }
        }
    }
    Write-Host 'KEEPING your existing candidate summary'
} else {
    $candidateSource = Join-Path $recreatedRunDir 'draft\summary.json'
    if (-not (Test-Path -LiteralPath $candidateSource -PathType Leaf)) {
        throw 'The controlled recreated draft is missing.'
    }
    Copy-Item -LiteralPath $candidateSource -Destination $candidate
    if ((Get-FileHash -LiteralPath $candidateSource -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash) {
        throw 'The new candidate copy did not match its source.'
    }
}
code $candidate
```

In your candidate:

1. change only the headline from
   `5 verified synthetic issues require human review.` to the other controlled
   option: `Human review is required for 5 verified synthetic issues.`;
2. keep every severity-group label exactly as generated;
3. keep every group sentence exactly constructed from its bracketed issue ID
   and controlled rule message;
4. keep every bracketed issue ID in the sentence it supports;
5. keep each issue ID in exactly one group;
6. keep exactly one `human_review` action per issue;
7. keep each review instruction in its exact controlled
   `Review field ...; do not perform an external action.` form;
8. keep every `external_action` as `false`;
9. keep `unsupported_statements` empty and `review_required` true;
10. do not add a cause, recommendation, payment, message, priority change,
    binding decision, or other external action.

Why the edit is intentionally narrow: the durable Artificial Intelligence
(AI) pattern is to select among bounded candidates while trusted code renders
the source-linked wording. A self-declared `external_action: false` cannot make
a dangerous free-text instruction safe.

You are recreating the controlled transformation, not merely renaming a file.

### Recreation 3 — Validate your candidate

Run:

```powershell
& $pythonExe $runner validate-summary `
    --run-dir $recreatedRunDir `
    --candidate $candidate
$LASTEXITCODE
Get-Content -LiteralPath (Join-Path $recreatedRunDir 'review\candidate-validation.json')
```

**Expected result:** `PASS`, exit code `0`, five issue references, human support
review required, and external actions 0.

If you receive `unknown_ai_issue_reference`, `uncited_summary`,
`missing_ai_issue_reference`, or `summary_contract`, repair only the named
problem. Do not remove the validator.

### Recreation 4 — Perform your own support review

Create the review at the exact path
`evidence\module-05\recreated_support_review.md`. The command below creates
the review headings once and keeps a prior review unchanged:

```powershell
$recreatedSupportReview = Join-Path $moduleFolder 'recreated_support_review.md'
if (Test-Path -LiteralPath $recreatedSupportReview) {
    if (-not (Test-Path -LiteralPath $recreatedSupportReview -PathType Leaf) -or
        (Get-Content -LiteralPath $recreatedSupportReview -TotalCount 1) -cne '# Recreated support review') {
        throw 'Existing recreated support review is the wrong type or unfamiliar. Preserve it and stop.'
    }
    Write-Host "KEEPING your existing $recreatedSupportReview"
} else {
    @'
# Recreated support review

| Candidate sentence | Cited issue IDs | Supported by exact rule message? | Added cause/action? | Accept/edit/reject |
|---|---|:---:|:---:|---|

Reviewer role:
Date:
All five issues checked:
Accepted for the Module 6 review package:
Deterministic fallback route:
'@ | Set-Content -LiteralPath $recreatedSupportReview -Encoding utf8
}
notepad $recreatedSupportReview
```

Complete the table with one row per sentence. Then record:

- reviewer role;
- date;
- whether all five issues were checked;
- whether the candidate is accepted for the Module 6 review package;
- the deterministic fallback route.

## Ask Codex to check your work

Run these three commands and paste each full path into its matching placeholder:

```powershell
(Resolve-Path $moduleFolder).Path
(Resolve-Path (Join-Path $projectRoot 'src\course1_capstone')).Path
(Resolve-Path $runnerHashRecord).Path
```

Then send:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only these three full paths:
[PASTE FULL MODULE-05 PATH]
[PASTE FULL SRC\COURSE1_CAPSTONE PATH]
[PASTE FULL MODULE-04 REFERENCE_RUNNER_HASHES.JSON PATH]

Learner attestation: I created these files for this fictional exercise and
have not knowingly put real client, employer, personal, medical, credential,
or secret data in them. This statement is an attestation, not proof.

You may only list names, read files, and calculate hashes inside the authorised
module and runner folders and the one authorised hash-record file. Do not
inspect any other Module 4 artifact. Do not create, edit, delete, rename, move,
or format any file. Do not
execute the runner, lesson scripts, or tests, use a network, or inspect a
parent or other location. If apparent sensitive data is noticed,
do not quote or repeat it: return NOT YET with only the filename and general
category, then stop. If none is noticed, say that non-detection is not proof
that none exists.

Return:
1. PASS or NOT YET;
2. checks that issue detection remains deterministic and upstream;
3. worked 13-issue mock and learner-created 5-issue candidate;
4. every known issue ID grouped once, visibly cited, and linked to exactly one
human_review action with external_action false;
5. no invented issue, changed severity, cause, recommendation, or action;
6. human sentence-level support reviews and deterministic fallback;
7. evidence for disabled, timeout, refusal, malformed JSON, unknown ID, and
untrusted free-text handling;
8. whether the authorised artifacts show any configured network call, secret,
paid service, or external action; say explicitly that non-detection is not
proof of absence;
9. the smallest learner-made corrections if NOT YET.

Remain read-only. Do not generate a replacement summary.
```

## Pass criteria

- [ ] Exact project Python is used through `$pythonExe`.
- [ ] The runner still matches Module 4's verified three-file SHA-256 record.
- [ ] The worked mock uses 13 verified issues only.
- [ ] The recreated candidate uses all 5 verified issues only.
- [ ] Every issue is grouped and cited exactly once.
- [ ] Every issue has exactly one source-linked human-review action.
- [ ] `unsupported_statements` is empty and `review_required` is true.
- [ ] Human review checks every sentence against evidence.
- [ ] All five AI failure modes use deterministic fallback.
- [ ] Untrusted free text remains inert source data.
- [ ] No provider, key, network, real data, or external action is used.
- [ ] Codex returns `PASS` in read-only mode.

### Record your Module 5 PASS in Git

Only after Codex returns `PASS`, rerun the complete **Start or resume safely**
block in this same PowerShell window so the exact marker and Git-root checks
pass again:

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence\module-05"
git commit --only -m "complete module 5 evidence" -- "evidence/module-05"
git status --short
```

`git commit --only` restricts this checkpoint to the repeated module path,
even if a different file had already been staged.

## Consultant lens

The durable asset is the boundary: verified input, constrained output,
reference validation, human meaning check, and fallback. In a later course, an
approved provider or model can be replaced without changing that contract.

## Capstone increment

The capstone now has source-linked offline-mock summaries and human-review
actions plus tested fallbacks. It still waits for a meaningful human decision
and cannot create an export.

## Required artifact

`evidence/module-05` contains the worked mock, human support review, five
fallback runs, untrusted-text result, learner-created five-issue candidate,
candidate validation, and recreated support review.

## Test gate

All Module 5 pass criteria and the read-only Codex review must pass. Every
known issue is grouped, cited, and linked to one human-review action exactly
once; every fault uses fallback; no unsupported or external action survives.

## Stop or rework

Stop if the mock receives unnecessary raw data, invents or omits an issue,
changes severity, includes an unsupported statement, proposes an external
action, uses a provider key, or lacks a deterministic fallback.

## Common failures

- Trusting valid JSON as proof that wording is supported.
- Letting the language step detect deterministic issues.
- Hiding an omitted reference in polished prose.
- Treating the offline mock as a real provider result.
- Weakening the contract after a deliberately malformed response fails.

## Estimated time

8-12 hours, best completed as three to five sessions.

Suggested sessions: three to five sessions of about 2-3 hours.
