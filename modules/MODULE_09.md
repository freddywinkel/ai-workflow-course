# Module 9 — Run User Acceptance Testing (UAT), Hand Over, and Pass the Course 1 Assessment

## Outcome

You will complete User Acceptance Testing (UAT), plan training and adoption,
write a runbook and fallback, assemble handover evidence, make a bounded final
post-UAT decision, complete the mandatory six-area Course 1 rubric and ten
plain-language oral answers, and write an honest portfolio case.

User Acceptance Testing (UAT) means intended users try realistic scenarios and
confirm whether the workflow supports the agreed work.

Passing Course 1 proves a synthetic foundation project. It does not certify you
as a production consultant or regulated-systems specialist.

## Beginner checkpoint

Start when Modules 1–8 pass. Module 8 produced a `PROVISIONAL PRE-UAT`
recommendation using one of the three permitted labels:
`ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or `DO NOT CONTINUE`. Module 9
does not copy that recommendation blindly. You add UAT, defect/retest,
adoption, and handover evidence, reassess the label, and mark the result
`FINAL POST-UAT`. This module closes and indexes the evidence honestly; it
does not force a positive decision. All acceptance work remains synthetic and
local.

## Concepts

- **User Acceptance Testing (UAT)** means intended users check whether a system
  supports agreed work in realistic scenarios.
- **Adoption** is sustained correct use, not simply installing software.
- A **runbook** tells an operator how to run, monitor, stop, recover, and
  escalate.
- **Handover** transfers evidence, instructions, access responsibilities,
  limitations, and continuing ownership.
- **Benefits realisation** measures whether the expected benefit appears after
  use.
- **Rollback** returns to a known safe earlier method or version.
- An **identifier (ID)** distinguishes one test or evidence item.
- **Information technology (IT)** is the function that manages organisational
  systems and support; a runbook must still name a responsible role.
- A **rubric** is a fixed scoring guide. Course 1 has six required areas. A
  passing score cannot hide an unsafe or weak area.
- An **oral demonstration** means explaining the work aloud in your own words,
  without reading generated wording.

## Official readings

GOV.UK is the United Kingdom government's public guidance website. The United
States National Institute of Standards and Technology (NIST) publishes
voluntary artificial intelligence (AI) risk guidance.

1. [GOV.UK Service Manual: testing with users](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing)
2. [GOV.UK Service Manual: set up and manage user support](https://www.gov.uk/service-manual/helping-people-to-use-your-service/set-up-and-manage-user-support)
3. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

## Guided build

The worked handover is for a simple fictional stock exception process. The
independent recreation uses the different Course 1 capstone and its actual
evidence.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files. Comma-separated
values (CSV) is the plain-text table format used by the scenario. A small or
medium-sized enterprise (SME) is a business smaller than a large enterprise.

Markdown is a plain-text format for headings, lists, and tables; `.md` is its
file name ending. **Given/When/Then** is a test-writing pattern: **Given**
describes the starting state, **When** names the action, and **Then** states the
observable expected result.

## Start or resume safely

At the start of every study session, rerun Stage 1. Closing PowerShell removes
temporary path variables, not your saved work. Stage 1 restores the paths and
returns to the same folder. Before any lesson write or runner execution, it
checks the safe path length, requires the exact synthetic-course marker, and
proves that the marked folder is the Git repository root. Template copies below
are create-once and will leave an existing learner file untouched.

Suggested sessions:

1. follow and rehearse the worked UAT/handover pack;
2. inspect the completed worksheets and execute nine isolated capstone
   scenarios;
3. complete adoption and handover, then reassess the Module 8 recommendation;
4. follow the worked assessment, recreate the six-area rubric and ten oral
   answers, and pass the objective score gate;
5. complete the portfolio/demo, assemble the index/change log, run the final
   bounded Codex check, correct gaps, and make the two final Git checkpoints.

Before stopping, save every file and note the last numbered step. Rerun Stage 1
after opening a new PowerShell window. Do not mark the course complete until
the final practical and rubric gates both pass.

## Follow along — I show you exactly how

**Expected result:** a complete worked UAT, adoption, runbook, handover, final
decision, and honest portfolio pack for a synthetic scenario.

### Stage 1 — Prepare the module folder

Open Windows PowerShell and run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
if ($projectRoot.Length -gt 140) {
    throw 'The prescribed Course 1 project path is too long for the deepest UAT evidence. Stop and ask Codex for a read-only path review; do not move or recreate the project yourself.'
}
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
$moduleFolder = Join-Path $projectRoot 'evidence\module-09'
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
$runner = Join-Path $projectRoot 'src\course1_capstone\cli.py'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Course Python not found. Complete Windows Setup before Module 9.'
}
if (-not (Test-Path -LiteralPath $runner)) {
    throw 'Course 1 runner not found. Return to Module 4 Stage 1.'
}
$runnerFolder = Join-Path $projectRoot 'src\course1_capstone'
$runnerHashRecord = Join-Path $projectRoot 'evidence\module-04\reference_runner_hashes.json'
if (-not (Test-Path -LiteralPath $runnerHashRecord -PathType Leaf)) {
    throw 'Module 4 runner-hash record is missing. Return to Module 4 Stage 1.'
}
try {
    $savedRunnerHashes = Get-Content -Raw -LiteralPath $runnerHashRecord |
        ConvertFrom-Json
} catch {
    throw 'Module 4 runner-hash record is damaged. Stop for read-only diagnosis.'
}
$expectedRunnerNames = @('__init__.py','workflow.py','cli.py')
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
if (@($savedRunnerHashes).Count -ne $expectedRunnerNames.Count -or
    @(Compare-Object $expectedRunnerNames $savedRunnerNames -CaseSensitive).Count -ne 0) {
    throw 'Module 4 runner-hash record does not contain each exact controlled filename once.'
}
foreach ($expectedRunnerName in $expectedRunnerNames) {
    $savedRunnerHash = @($savedRunnerHashes | Where-Object {
        $_.name -ceq $expectedRunnerName
    })
    $runnerFile = Join-Path $runnerFolder $expectedRunnerName
    if ($savedRunnerHash.Count -ne 1 -or
        $savedRunnerHash[0].source_sha256 -ne
        $savedRunnerHash[0].destination_sha256 -or
        -not (Test-Path -LiteralPath $runnerFile -PathType Leaf) -or
        (Get-FileHash -LiteralPath $runnerFile -Algorithm SHA256).Hash -ne
        $savedRunnerHash[0].destination_sha256) {
        throw "Controlled runner differs from the verified Module 4 copy: $expectedRunnerName"
    }
}
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
if (-not (Test-Path -LiteralPath (Join-Path $courseRoot 'course1_capstone\fixtures'))) {
    throw 'That course folder does not contain the Course 1 synthetic fixtures.'
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
New-Item -ItemType Directory -Force -Path $moduleFolder | Out-Null
Set-Location -LiteralPath $moduleFolder
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function Copy-NewPracticeFile {
    param([string]$Source, [string]$Destination)
    if (Test-Path -LiteralPath $Destination) {
        Write-Host "Resume: $Destination already exists and was left unchanged."
    } else {
        Copy-Item -LiteralPath $Source -Destination $Destination
        Write-Host "Created: $Destination"
    }
}
function Move-ToNumberedPreservedFile {
    param([Parameter(Mandatory)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return }
    $parent = Split-Path -Parent $Path
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($Path)
    $extension = [System.IO.Path]::GetExtension($Path)
    $number = 1
    do {
        $candidate = Join-Path $parent (
            '{0}-preserved-{1:D2}{2}' -f $stem, $number, $extension
        )
        $number++
    } while (Test-Path -LiteralPath $candidate)
    Move-Item -LiteralPath $Path -Destination $candidate
    Write-Host "PRESERVED INCOMPLETE ATTEMPT: $candidate"
}
function Start-NewPracticeTextFile {
    param(
        [Parameter(Mandatory)][string]$Path,
        [string[]]$RequiredPatterns = @()
    )
    if (Test-Path -LiteralPath $Path) {
        if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
            throw "Expected a text file but found another item: $Path"
        }
        $existingText = Get-Content -Raw -LiteralPath $Path
        if ($null -eq $existingText) { $existingText = '' }
        $hasContent = -not [string]::IsNullOrWhiteSpace($existingText)
        $missingPatterns = @($RequiredPatterns | Where-Object {
            -not $existingText.Contains($_)
        })
        $isComplete = (
            $hasContent -and
            ($RequiredPatterns.Count -eq 0 -or $missingPatterns.Count -eq 0)
        )
        if ($isComplete) {
            Write-Host "SKIP CREATE: $Path was left unchanged."
            return $false
        }
        Move-ToNumberedPreservedFile -Path $Path
    }
    [System.IO.File]::WriteAllText($Path, '', $utf8NoBom)
    Write-Host "CREATED: $Path. Any empty or incomplete prior attempt was preserved."
    return $true
}
function Confirm-SafeStopEvidence {
    param(
        [Parameter(Mandatory)][string]$BasePath,
        [Parameter(Mandatory)][string]$EvidenceBaseRelative,
        [Parameter(Mandatory)][string]$ExpectedErrorCode
    )
    $latestPath = Join-Path $BasePath 'failures\latest.json'
    if (-not (Test-Path -LiteralPath $latestPath)) {
        throw "Expected safe-stop pointer missing: $latestPath"
    }
    try {
        $latest = Get-Content -Raw -LiteralPath $latestPath | ConvertFrom-Json
    } catch {
        throw "Safe-stop pointer is not valid JSON: $latestPath"
    }
    if ($latest.error_code -ne $ExpectedErrorCode) {
        throw "Expected error_code $ExpectedErrorCode; observed $($latest.error_code)."
    }
    $historyRelative = [string]$latest.history_path
    if (
        $historyRelative -notmatch '^failures/a[0-9]{4,}\.json$' -or
        [System.IO.Path]::IsPathRooted($historyRelative) -or
        @($historyRelative -split '[\\/]' | Where-Object { $_ -eq '..' }).Count -ne 0
    ) {
        throw "Unsafe or unexpected history_path: $historyRelative"
    }
    $historyPath = Join-Path $BasePath $historyRelative
    if (-not (Test-Path -LiteralPath $historyPath)) {
        throw "Immutable safe-stop history file missing: $historyPath"
    }
    try {
        $history = Get-Content -Raw -LiteralPath $historyPath | ConvertFrom-Json
    } catch {
        throw "Immutable safe-stop history is not valid JSON: $historyPath"
    }
    if (
        $history.error_code -ne $ExpectedErrorCode -or
        $history.attempt_id -ne $latest.attempt_id
    ) {
        throw 'The latest safe-stop pointer and immutable history record do not match.'
    }
    $latestHash = (Get-FileHash -LiteralPath $latestPath -Algorithm SHA256).Hash
    $historyHash = (Get-FileHash -LiteralPath $historyPath -Algorithm SHA256).Hash
    if ($latestHash -ne $historyHash) {
        throw 'The latest safe-stop pointer and immutable history bytes do not match.'
    }
    [PSCustomObject]@{
        expected_error_code = $ExpectedErrorCode
        observed_error_code = $latest.error_code
        attempt_id = $latest.attempt_id
        latest_locator = (
            Join-Path $EvidenceBaseRelative 'failures\latest.json'
        ).Replace('\', '/')
        history_locator = (
            Join-Path $EvidenceBaseRelative $historyRelative
        ).Replace('\', '/')
        latest_sha256 = $latestHash
        history_sha256 = $historyHash
        immutable_history_verified = $true
    }
}
function Resolve-SavedCourseRun {
    param([string]$Workspace)
    $latest = Join-Path $Workspace 'latest_run.txt'
    if (-not (Test-Path -LiteralPath $latest -PathType Leaf)) {
        throw "Saved run locator is missing or is not a file: $latest"
    }
    $locatorLines = @(Get-Content -LiteralPath $latest)
    if ($locatorLines.Count -ne 1) {
        throw "Saved run locator must contain exactly one line: $latest"
    }
    $locator = [string]$locatorLines[0]
    if ([string]::IsNullOrWhiteSpace($locator) -or
        $locator -cne $locator.Trim() -or
        [System.IO.Path]::IsPathRooted($locator) -or
        $locator -cnotmatch '^runs[\\/]RUN-[A-F0-9]{12}$') {
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
    return [PSCustomObject]@{
        Locator = $locator
        Path = $resolvedRunDir
    }
}
& $pythonExe --version
$workedPackCreated = Start-NewPracticeTextFile `
    -Path .\worked_uat_and_handover.md `
    -RequiredPatterns `
        '# Worked UAT and handover', `
        'Limitations: no client, real data, production deployment, or proven cash saving.'
if ($workedPackCreated) {
    notepad .\worked_uat_and_handover.md
} else {
    Write-Host 'The complete worked pack already exists; Stage 1 left it closed.'
}
```

### Stage 2 — Read and recreate a complete worked pack

If Stage 1 printed `CREATED`, paste the complete worked pack below from the
beginning, save, and close. Any empty or incomplete prior attempt was preserved
under a numbered `-preserved-` name. If it printed `SKIP CREATE`, both required
completion markers already exist; the completed file stayed closed and you
must not paste the pack again.

```markdown
# Worked UAT and handover — fictional low-stock list

## Boundary

Synthetic local spreadsheet configuration. It identifies quantity below an
approved threshold for internal review. It does not use AI, order, message,
select suppliers, pay, or write to a source system.

## Roles

- Process owner: operations lead; approves rules and acceptance.
- User: inventory coordinator; runs and reviews the list.
- Support owner: office systems coordinator; supports access and restore.
- Tester: course learner acting in a separate tester role.

## UAT script and result

| ID | Given | When | Then | Evidence | Result |
|---|---|---|---|---|---|
| UAT-01 | all quantities meet thresholds | user runs filter | empty exception list and no action state | screenshot-free result note and row count | pass |
| UAT-02 | one quantity is below threshold | user runs filter | one issue shows item ID, raw value, threshold, rule | saved synthetic output | pass |
| UAT-03 | quantity cell is blank | user runs filter | item stops for human review; zero is not invented | failure note | pass |
| UAT-04 | expected header is renamed | user runs filter | safe stop and manual fallback | failure record | pass |
| UAT-05 | user tries to treat list as an order | reviewer checks boundary | wording says internal review only | review note | pass |

Acceptance threshold: all five pass; no external action; fallback usable.

## Usability observations

- User can find source item and rule without help.
- "No action" and "failed" are visually distinct in the written result.
- The phrase "high attention" is not used as an order instruction.
- Limitation: test is a role simulation, not external user evidence.

## Adoption and training

What changes: coordinator uses a saved filter and reviewed list.
What does not change: operations lead decides investigation and ordering.

Training tasks:
1. open the correct synthetic/source export;
2. confirm header and assessment configuration;
3. run the filter;
4. trace an issue to source values;
5. distinguish no-action, issue-ready, and failed;
6. reject or correct a list;
7. use manual fallback;
8. report an incident.

Training evidence: learner demonstrates every task once without hidden prompts.
Feedback route: support owner records questions and recurring mistakes.

## Runbook

Normal run:
1. Confirm approved input location and unchanged header.
2. Preserve the source export.
3. Run the configured filter.
4. Check state and issue count.
5. Trace every exception to source and rule.
6. Have the operations lead review.
7. Store the internal reviewed result.

Safe failure:
1. Stop; do not guess or change the source.
2. Record error, time, input identity, and last safe state.
3. Tell the support owner.
4. Use manual spreadsheet filter.
5. Resume only after a tested correction and owner approval.

Rollback: restore the last tested formula/filter copy and rerun frozen tests.
Backup: support owner keeps the tested file and instructions.
No external action is replayed because none exists.

## Handover inventory

- intended purpose and negative scope;
- data dictionary and rule source;
- configured filter and version;
- frozen test data and results;
- UAT record;
- user instructions and runbook;
- access, backup, restore, incident, and update owners;
- known limitations and residual risks;
- manual fallback and rollback;
- decision record.

## Known limitations

- Synthetic and small-volume only.
- One file layout and one approved threshold set.
- No live integration or concurrent-user test.
- No external user research.
- No legal, privacy, or security assurance beyond the stated screen.

## Final decision

ACCEPT FOR SYNTHETIC PORTFOLIO. The case may be demonstrated only with its
synthetic boundary and stated limitations. Do not deploy it to a business.
Later courses separately teach discovery and controlled implementation.

## Honest portfolio summary

Problem: a fictional coordinator repeatedly scans stock rows.
Approach: define exact rules, configure a read-only exception list, test
failures, retain human review, and document fallback.
Evidence: frozen synthetic tests and five role-simulated UAT scenarios pass.
Limitations: no client, real data, production deployment, or proven cash saving.
```

Run:

```powershell
Select-String -Path .\worked_uat_and_handover.md -Pattern 'UAT-01','UAT-05','Safe failure','Known limitations','ACCEPT FOR SYNTHETIC PORTFOLIO'
```

**Expected result:** all five elements are found. The complete pack connects
acceptance, training, operation, failure, ownership, limitations, and decision.

**Troubleshooting:**

- If UAT only says “works,” rewrite it as Given/When/Then with observable
  evidence.
- If training is a presentation, add tasks the learner must demonstrate.
- If the runbook says “contact IT,” name a support role and what evidence to
  provide.
- If acceptance silently means production release, restore the synthetic-only
  limitation.

### Stage 3 — Rehearse one worked scenario

Read UAT-04 aloud and perform a tabletop rehearsal:

1. say what the user sees;
2. name the state;
3. name the evidence recorded;
4. state the manual fallback;
5. state who approves resumption.

Record the answers in `worked_uat_rehearsal.md`. This demonstrates that the
runbook can be followed rather than merely filed.

Create or safely resume that record:

```powershell
$workedRehearsalCreated = Start-NewPracticeTextFile -Path .\worked_uat_rehearsal.md
notepad .\worked_uat_rehearsal.md
```

If the helper printed `CREATED`, record all five answers. If it printed
`SKIP CREATE`, continue only missing answers; do not replace a completed
rehearsal.

### Stage 4 — Inspect the completed worksheet-shaped examples

The combined worked pack shows how the records connect. Now inspect the three
completed versions that use the same headings as the blank worksheets:

```powershell
notepad (Join-Path $courseRoot 'worked_examples\module_09_uat_script.md')
notepad (Join-Path $courseRoot 'worked_examples\module_09_adoption_and_training_plan.md')
notepad (Join-Path $courseRoot 'worked_examples\module_09_acceptance_and_handover.md')
```

Read them in that order. They show where to put an observed result, a defect
and retest, role-specific training evidence, owners, recovery, and limitations.
They are a fictional low-stock example; your recreation below uses the
different Course 1 runner and evidence.

## Now recreate it yourself

Use the different Synthetic SME Operations Exception Assistant and the actual
Course 1 evidence.

### Recreation 1 — Copy the blank records without overwriting work

```powershell
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\uat_script.md') .\recreated_uat.md
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\adoption_and_training_plan.md') .\recreated_adoption.md
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\acceptance_and_handover.md') .\recreated_handover.md
```

Open all three files and write `EXTERNAL UAT NOT VERIFIED` near the top of
`recreated_uat.md` when you are testing alone:

```powershell
notepad .\recreated_uat.md
notepad .\recreated_adoption.md
notepad .\recreated_handover.md
```

A complete role-separated self-test can pass Course 1 at Competent level, but
it is not evidence that a real user can operate the workflow. An independent
person using synthetic data is needed only for a Strong UAT rating. Their
participation is optional and does not authorise workplace research.

### Recreation 2 — Execute nine isolated UAT scenarios

Do not merely write what you think would happen. Run each command below in the
separate scenario folder, compare the observable evidence with the stated
expectation, and then record your own observed result in `recreated_uat.md`.
Every input is synthetic, every output stays on this computer, and no command
contains a network or external-action function.

In status evidence, `current_state` is the last valid persistent workflow
state. `latest_attempt_state` is the newest audit-event state; it becomes
`failed_manual` after a safe stop without overwriting that last valid state.

Create the parent folder and the safe retry helper. Run this block again after
opening a new PowerShell window. The helper uses `UAT-01` for the first attempt
and then `UAT-01-retry-02`, `UAT-01-retry-03`, and so on. It never deletes,
resumes inside, or overwrites an interrupted attempt.

```powershell
$scenarioRoot = Join-Path $moduleFolder 'uat-scenarios'
New-Item -ItemType Directory -Force -Path $scenarioRoot | Out-Null
function New-UatAttemptFolder {
    param(
        [Parameter(Mandatory)]
        [ValidatePattern('^UAT-(0[1-9]|D01)$')]
        [string]$ScenarioId
    )
    $attemptNumber = 1
    $folderName = $ScenarioId
    $candidate = Join-Path $scenarioRoot $folderName
    while (Test-Path -LiteralPath $candidate) {
        $attemptNumber++
        $folderName = '{0}-retry-{1:D2}' -f $ScenarioId, $attemptNumber
        $candidate = Join-Path $scenarioRoot $folderName
    }
    New-Item -ItemType Directory -Path $candidate | Out-Null
    $attemptRecord = [ordered]@{
        scenario_id = $ScenarioId
        attempt_number = $attemptNumber
        attempt_folder = $folderName
        relative_path = (Join-Path 'uat-scenarios' $folderName)
        prior_attempts_preserved = ($attemptNumber -gt 1)
    }
    [System.IO.File]::WriteAllText(
        (Join-Path $candidate 'attempt-info.json'),
        ($attemptRecord | ConvertTo-Json),
        $utf8NoBom
    )
    Write-Host "Using fresh attempt: $($attemptRecord.relative_path)"
    return $candidate
}
```

If a scenario is interrupted or fails unexpectedly:

1. stop and leave its folder unchanged;
2. note the last visible error in `recreated_uat.md`;
3. correct only the cause outside that attempt folder;
4. rerun the **entire matching UAT block from its first line**;
5. use the new numbered retry printed by the helper;
6. compare and record the new result, while retaining the prior attempt as
   defect or interruption evidence.

Do not run only the remaining lines inside a partial attempt. Do not rename,
delete, or reuse it. Each `attempt-info.json` gives the exact relative path to
record.

A planned `SAFE STOP` that matches the scenario's stated exit code and
`error_code` is a completed passing test, not an unexpected failure. It does
not require a retry. When every scenario block completes as written on its
first attempt, no numbered retry folder is required.

#### UAT-01 — Clean input ends with no action needed

```powershell
$uat01Workspace = New-UatAttemptFolder -ScenarioId 'UAT-01'
& $pythonExe $runner prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\valid_no_issue.csv') `
    --workspace $uat01Workspace `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-01 unexpectedly failed.' }
$uat01SavedRun = Resolve-SavedCourseRun $uat01Workspace
$uat01RunLocator = $uat01SavedRun.Locator
$uat01Run = $uat01SavedRun.Path
& $pythonExe $runner status --run-dir $uat01Run |
    Tee-Object -FilePath (Join-Path $uat01Workspace 'observed-status.txt')
if ($LASTEXITCODE -ne 0) { throw 'UAT-01 status validation unexpectedly failed.' }
$uat01FixtureHash = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    (Join-Path $courseRoot 'course1_capstone\fixtures\failures\valid_no_issue.csv')).Hash
$uat01CopiedHash = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    (Join-Path $uat01Run 'source\work_items.csv')).Hash
$uat01Hashes = @(
    [PSCustomObject]@{
        Role = 'supplied_clean_fixture'
        RelativePath = 'course1_capstone/fixtures/failures/valid_no_issue.csv'
        SHA256 = $uat01FixtureHash
    }
    [PSCustomObject]@{
        Role = 'protected_run_copy'
        RelativePath = 'source/work_items.csv'
        SHA256 = $uat01CopiedHash
    }
)
$uat01Hashes | Format-Table Role,RelativePath,SHA256 -AutoSize
$uat01Hashes | Export-Csv -NoTypeInformation `
    -Encoding UTF8 -LiteralPath (Join-Path $uat01Workspace 'observed-source-hashes.csv')
[PSCustomObject]@{
    draft_exists = Test-Path -LiteralPath (Join-Path $uat01Run 'draft')
    outbox_exists = Test-Path -LiteralPath (Join-Path $uat01Run 'outbox')
} | Format-List | Out-File -Encoding utf8 `
    (Join-Path $uat01Workspace 'observed-absent-folders.txt')
```

**Given:** the supplied clean fixture. **When:** the workflow prepares a run.
**Then:** `current_state` is `no_action_needed`, `issue_count` is `0`,
`external_actions` is `0`, the two hashes match, and neither `draft` nor
`outbox` exists. Evidence in the fresh attempt folder:
`observed-status.txt`, `observed-source-hashes.csv`,
`observed-absent-folders.txt`, `attempt-info.json`, and the named run's
`state.json`.
The hash evidence deliberately uses neutral role names and repository-relative
paths. It does not store your Windows username or an absolute computer path.

#### UAT-02 — The frozen set produces exactly all 13 issue triples

```powershell
$uat02Workspace = New-UatAttemptFolder -ScenarioId 'UAT-02'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $uat02Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-02 unexpectedly failed.' }
$uat02SavedRun = Resolve-SavedCourseRun $uat02Workspace
$uat02RunLocator = $uat02SavedRun.Locator
$uat02Run = $uat02SavedRun.Path
Copy-Item -LiteralPath (Join-Path $uat02Run 'evaluation.json') `
    -Destination (Join-Path $uat02Workspace 'observed-evaluation.json')
(Import-Csv -LiteralPath (Join-Path $uat02Run 'issues\issues.csv')).Count
Get-Content -LiteralPath (Join-Path $uat02Workspace 'observed-evaluation.json')
```

**Given:** the frozen 15-row synthetic register and its 13 expected issue
identities. **When:** the workflow prepares UAT-02 with the offline mock and
compares the generated issues with the expected file. **Then:** count `13`;
true positives `13`; false positives `0`; false
negatives `0`; state `needs_review`; and external actions `0`. Evidence:
the fresh attempt's `attempt-info.json`, `observed-evaluation.json`, and the
named run's `issues\issues.csv`.

#### UAT-03 — An invalid header safely stops

```powershell
$uat03Workspace = New-UatAttemptFolder -ScenarioId 'UAT-03'
$uat03Output = & $pythonExe $runner prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\unexpected_header.csv') `
    --workspace $uat03Workspace `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY 2>&1
$uat03Exit = $LASTEXITCODE
$uat03Output | Tee-Object -FilePath (Join-Path $uat03Workspace 'observed-command.txt')
if ($uat03Exit -ne 1) { throw "UAT-03 expected exit code 1; observed $uat03Exit." }
$uat03FailureEvidence = Confirm-SafeStopEvidence `
    -BasePath $uat03Workspace `
    -EvidenceBaseRelative '.' `
    -ExpectedErrorCode 'header_mismatch'
[System.IO.File]::WriteAllText(
    (Join-Path $uat03Workspace 'observed-failure-evidence.json'),
    ($uat03FailureEvidence | ConvertTo-Json),
    $utf8NoBom
)
Get-Content -LiteralPath (Join-Path $uat03Workspace 'observed-failure-evidence.json')
```

**Given:** the supplied synthetic file with an unexpected column header.
**When:** the workflow tries to prepare UAT-03 with AI disabled. **Then:** the
command says `SAFE STOP`, exit code is `1`, error code is
`header_mismatch`, the command-attempt record state is `failed_manual`,
external actions are `0`, no run is invented, and no review draft or outbox
exists. Evidence in the fresh attempt folder: `attempt-info.json`,
`observed-command.txt`, `failures\latest.json`, the immutable
`failures/aNNNN.json` named by its `history_path`, and
`observed-failure-evidence.json`, which must show the expected and observed
error code `header_mismatch` and matching SHA-256 values.

#### UAT-04 — The invalid date dependency is source-linked

Create a fresh scenario run so its audit and failure evidence cannot change
another UAT scenario:

```powershell
$uat04Workspace = New-UatAttemptFolder -ScenarioId 'UAT-04'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $uat04Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-04 prepare unexpectedly failed.' }
$uat04SavedRun = Resolve-SavedCourseRun $uat04Workspace
$uat04RunLocator = $uat04SavedRun.Locator
$uat04Run = $uat04SavedRun.Path
$uat04Observed = Import-Csv -LiteralPath (Join-Path $uat04Run 'issues\issues.csv') |
    Where-Object {
        $_.work_item_id -eq 'WI-0003' -and
        $_.rule_code -eq 'R005' -and
        $_.field -eq 'due_date'
    }
if (@($uat04Observed).Count -ne 1) {
    throw 'UAT-04 expected exactly WI-0003|R005|due_date.'
}
$uat04Observed | Export-Csv -NoTypeInformation -Encoding UTF8 `
    -LiteralPath (Join-Path $uat04Workspace 'observed-r005.csv')
Get-Content -LiteralPath (Join-Path $uat04Workspace 'observed-r005.csv')
```

**Given:** a fresh run of the frozen synthetic register containing the
deliberately invalid date dependency for `WI-0003`. **When:** you select only
its R005 due-date issue from the generated issue file. **Then:** exactly one
issue has identity
`WI-0003|R005|due_date`, severity
`high`, the raw due date, source row, and message. Evidence:
the fresh attempt's `attempt-info.json` and `observed-r005.csv`.

#### UAT-05 — A duplicate reference reports both source rows

```powershell
$uat05Workspace = New-UatAttemptFolder -ScenarioId 'UAT-05'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $uat05Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-05 prepare unexpectedly failed.' }
$uat05SavedRun = Resolve-SavedCourseRun $uat05Workspace
$uat05RunLocator = $uat05SavedRun.Locator
$uat05Run = $uat05SavedRun.Path
$uat05Observed = Import-Csv -LiteralPath (Join-Path $uat05Run 'issues\issues.csv') |
    Where-Object {
        $_.rule_code -eq 'R010' -and
        $_.field -eq 'source_reference' -and
        $_.source_reference -eq 'REF-1006'
    }
if (@($uat05Observed).Count -ne 2) {
    throw 'UAT-05 expected two R010 records for REF-1006.'
}
$uat05Observed | Export-Csv -NoTypeInformation -Encoding UTF8 `
    -LiteralPath (Join-Path $uat05Workspace 'observed-r010-both-rows.csv')
Get-Content -LiteralPath (Join-Path $uat05Workspace 'observed-r010-both-rows.csv')
```

**Given:** a fresh run in which two synthetic rows share
`REF-1006`. **When:** you select all R010 source-reference issues for that
reference. **Then:** exactly two separate issue identities exist, one for
`WI-0006` and
one for `WI-0007`; neither row is lost. Evidence:
the fresh attempt's `attempt-info.json` and
`observed-r010-both-rows.csv`.

#### UAT-06 — An unknown summary reference is refused

```powershell
$uat06Workspace = New-UatAttemptFolder -ScenarioId 'UAT-06'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $uat06Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-06 prepare unexpectedly failed.' }
$uat06SavedRun = Resolve-SavedCourseRun $uat06Workspace
$uat06RunLocator = $uat06SavedRun.Locator
$uat06Run = $uat06SavedRun.Path
$uat06CandidatePath = Join-Path $uat06Workspace 'candidate-with-unknown-id.json'
$uat06Candidate = Get-Content -Raw -LiteralPath (Join-Path $uat06Run 'draft\summary.json') |
    ConvertFrom-Json
$uat06Candidate.groups[0].issue_ids[0] = 'WI-9999|R999|unknown'
[System.IO.File]::WriteAllText(
    $uat06CandidatePath,
    ($uat06Candidate | ConvertTo-Json -Depth 20),
    $utf8NoBom
)
$uat06Output = & $pythonExe $runner validate-summary `
    --run-dir $uat06Run `
    --candidate $uat06CandidatePath 2>&1
$uat06Exit = $LASTEXITCODE
$uat06Output | Tee-Object -FilePath (Join-Path $uat06Workspace 'observed-command.txt')
if ($uat06Exit -ne 1) { throw "UAT-06 expected exit code 1; observed $uat06Exit." }
$uat06FailureEvidence = Confirm-SafeStopEvidence `
    -BasePath $uat06Run `
    -EvidenceBaseRelative $uat06RunLocator `
    -ExpectedErrorCode 'unknown_ai_issue_reference'
[System.IO.File]::WriteAllText(
    (Join-Path $uat06Workspace 'observed-failure-evidence.json'),
    ($uat06FailureEvidence | ConvertTo-Json),
    $utf8NoBom
)
Get-Content -LiteralPath (Join-Path $uat06Workspace 'observed-failure-evidence.json')
& $pythonExe $runner status --run-dir $uat06Run |
    Tee-Object -FilePath (Join-Path $uat06Workspace 'observed-status-after-safe-stop.txt')
if ($LASTEXITCODE -ne 0) { throw 'UAT-06 status validation unexpectedly failed.' }
```

**Given:** a fresh valid mock summary changed to cite the nonexistent
identity `WI-9999|R999|unknown`. **When:** the summary validator checks that
candidate against the generated issue file. **Then:** `SAFE STOP`, exit code
`1`, error code
`unknown_ai_issue_reference`, latest attempt state `failed_manual`, last valid
`current_state` still `needs_review`, external actions `0`, and the
deterministic `issues\issues.csv` remains usable. Evidence:
the fresh attempt's `attempt-info.json`, `observed-command.txt`,
`observed-status-after-safe-stop.txt`, candidate, `failures\latest.json`, the
immutable `failures/aNNNN.json` followed from `history_path`, and
`observed-failure-evidence.json` showing
`unknown_ai_issue_reference` and matching SHA-256 values.

#### UAT-07 — Exact-draft approval permits two local draft exports

UAT-07 through UAT-09 use a **fixed synthetic test clock**:
`2026-07-28T10:00:00Z` for the fictional decision and
`2026-07-28T11:00:00Z` for the fictional export check. These values make the
test repeatable; they are not the date or time when you perform the course.
Keep them unchanged in these three test scenarios.

```powershell
$uat07Workspace = New-UatAttemptFolder -ScenarioId 'UAT-07'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $uat07Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-07 prepare unexpectedly failed.' }
$uat07SavedRun = Resolve-SavedCourseRun $uat07Workspace
$uat07RunLocator = $uat07SavedRun.Locator
$uat07Run = $uat07SavedRun.Path
$uat07SourceHashBefore = (Get-FileHash -Algorithm SHA256 `
    -LiteralPath (Join-Path $uat07Run 'source\work_items.csv')).Hash
& $pythonExe $runner decide `
    --run-dir $uat07Run `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Every synthetic issue, source link, statement, and action was reviewed.' `
    --expected-revision 1 `
    --evidence-reviewed `
    --decided-at 2026-07-28T10:00:00Z `
    --expires-at 2099-01-01T00:00:00Z
if ($LASTEXITCODE -ne 0) { throw 'UAT-07 approval unexpectedly failed.' }
& $pythonExe $runner export `
    --run-dir $uat07Run `
    --checked-at 2026-07-28T11:00:00Z
if ($LASTEXITCODE -ne 0) { throw 'UAT-07 local export unexpectedly failed.' }
& $pythonExe $runner status --run-dir $uat07Run |
    Tee-Object -FilePath (Join-Path $uat07Workspace 'observed-status.txt')
if ($LASTEXITCODE -ne 0) { throw 'UAT-07 status validation unexpectedly failed.' }
$uat07SourceHashAfter = (Get-FileHash -Algorithm SHA256 `
    -LiteralPath (Join-Path $uat07Run 'source\work_items.csv')).Hash
$uat07HashCheck = [PSCustomObject]@{
    source_sha256_before = $uat07SourceHashBefore
    source_sha256_after = $uat07SourceHashAfter
    source_unchanged = ($uat07SourceHashBefore -eq $uat07SourceHashAfter)
}
$uat07HashCheck | Format-List
$uat07HashCheck | ConvertTo-Json | Out-File -Encoding utf8 `
    (Join-Path $uat07Workspace 'observed-source-hash-check.json')
Get-ChildItem -LiteralPath (Join-Path $uat07Run 'outbox') -File
```

**Given:** a fresh UAT-07 run prepared from the frozen synthetic register.
**When:** a course-learner role reviews the evidence, approves exact revision
1, and requests the local export before expiry. **Then:** approval is bound to
revision `1` and its exact Secure Hash Algorithm
256-bit (SHA-256) value; state is `approved_draft`; exactly two local files
exist (`approved-r1.json` and `approved-r1.csv`); source hashes match; and
external actions are `0`. Evidence: the decision JSON, outbox files,
the fresh attempt's `attempt-info.json`, `observed-status.txt`, and
`observed-source-hash-check.json` with `source_unchanged: true`.

#### UAT-08 — Editing an approved draft invalidates approval

```powershell
$uat08Workspace = New-UatAttemptFolder -ScenarioId 'UAT-08'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $uat08Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-08 prepare unexpectedly failed.' }
$uat08SavedRun = Resolve-SavedCourseRun $uat08Workspace
$uat08RunLocator = $uat08SavedRun.Locator
$uat08Run = $uat08SavedRun.Path
& $pythonExe $runner decide `
    --run-dir $uat08Run `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Synthetic approval used only for the edit-invalidation test.' `
    --expected-revision 1 `
    --evidence-reviewed `
    --decided-at 2026-07-28T10:00:00Z `
    --expires-at 2099-01-01T00:00:00Z
if ($LASTEXITCODE -ne 0) { throw 'UAT-08 approval unexpectedly failed.' }
Add-Content -LiteralPath (Join-Path $uat08Run 'draft\summary.json') -Value ' '
$uat08Output = & $pythonExe $runner export `
    --run-dir $uat08Run `
    --checked-at 2026-07-28T11:00:00Z 2>&1
$uat08Exit = $LASTEXITCODE
$uat08Output | Tee-Object -FilePath (Join-Path $uat08Workspace 'observed-command.txt')
if ($uat08Exit -ne 1) { throw "UAT-08 expected exit code 1; observed $uat08Exit." }
$uat08StateAfter = Get-Content -Raw -LiteralPath `
    (Join-Path $uat08Run 'state.json') | ConvertFrom-Json
$uat08LastAudit = Get-Content -LiteralPath `
    (Join-Path $uat08Run 'audit\events.jsonl') |
    Where-Object { $_.Trim() } |
    Select-Object -Last 1 |
    ConvertFrom-Json
$uat08ObservedState = [ordered]@{
    current_state = $uat08StateAfter.current_state
    latest_attempt_state = $uat08LastAudit.state
    latest_event_type = $uat08LastAudit.event_type
    external_actions = $uat08StateAfter.external_actions
    local_export_count = $uat08StateAfter.local_export_count
}
[System.IO.File]::WriteAllText(
    (Join-Path $uat08Workspace 'observed-state-after-safe-stop.json'),
    ($uat08ObservedState | ConvertTo-Json),
    $utf8NoBom
)
$uat08FailureEvidence = Confirm-SafeStopEvidence `
    -BasePath $uat08Run `
    -EvidenceBaseRelative $uat08RunLocator `
    -ExpectedErrorCode 'edited_draft_after_approval'
[System.IO.File]::WriteAllText(
    (Join-Path $uat08Workspace 'observed-failure-evidence.json'),
    ($uat08FailureEvidence | ConvertTo-Json),
    $utf8NoBom
)
Get-Content -LiteralPath (Join-Path $uat08Workspace 'observed-failure-evidence.json')
Get-Content -LiteralPath (Join-Path $uat08Workspace 'observed-state-after-safe-stop.json')
Test-Path -LiteralPath (Join-Path $uat08Run 'outbox')
```

**Given:** a fresh UAT-08 draft that was approved at exact revision 1.
**When:** the approved summary file is edited and an export is attempted.
**Then:** `SAFE STOP`, exit code `1`, error code
`edited_draft_after_approval`, latest attempt state `failed_manual`, last valid
`current_state` still `approved_for_local_export`, external actions `0`, and no
outbox exists. Evidence: the fresh attempt's `attempt-info.json`,
`observed-command.txt`, `observed-state-after-safe-stop.json`, original
decision, `failures\latest.json`, the immutable `failures/aNNNN.json` followed
from `history_path`, and `observed-failure-evidence.json` showing
`edited_draft_after_approval` and matching SHA-256 values.

#### UAT-09 — External actions stay false and fallback stays usable

```powershell
$uat09Workspace = New-UatAttemptFolder -ScenarioId 'UAT-09'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $uat09Workspace `
    --ai-mode timeout `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-09 prepare unexpectedly failed.' }
$uat09SavedRun = Resolve-SavedCourseRun $uat09Workspace
$uat09RunLocator = $uat09SavedRun.Locator
$uat09Run = $uat09SavedRun.Path
Copy-Item -LiteralPath (Join-Path $uat09Run 'control.json') `
    -Destination (Join-Path $uat09Workspace 'observed-control-before.json')
Copy-Item -LiteralPath (Join-Path $uat09Run 'state.json') `
    -Destination (Join-Path $uat09Workspace 'observed-state-before.json')
Copy-Item -LiteralPath (Join-Path $uat09Run 'manual_fallback.md') `
    -Destination (Join-Path $uat09Workspace 'observed-manual-fallback.md')
& $pythonExe $runner decide `
    --run-dir $uat09Run `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Synthetic approval used only for the external-action control test.' `
    --expected-revision 1 `
    --evidence-reviewed `
    --decided-at 2026-07-28T10:00:00Z `
    --expires-at 2099-01-01T00:00:00Z
if ($LASTEXITCODE -ne 0) { throw 'UAT-09 approval unexpectedly failed.' }
$uat09ControlPath = Join-Path $uat09Run 'control.json'
$uat09Control = Get-Content -Raw -LiteralPath $uat09ControlPath | ConvertFrom-Json
$uat09Control.EXTERNAL_ACTIONS_ENABLED = $true
[System.IO.File]::WriteAllText(
    $uat09ControlPath,
    ($uat09Control | ConvertTo-Json -Depth 10),
    $utf8NoBom
)
$uat09Output = & $pythonExe $runner export `
    --run-dir $uat09Run `
    --checked-at 2026-07-28T11:00:00Z 2>&1
$uat09Exit = $LASTEXITCODE
$uat09Output | Tee-Object -FilePath (Join-Path $uat09Workspace 'observed-command.txt')
if ($uat09Exit -ne 1) { throw "UAT-09 expected exit code 1; observed $uat09Exit." }
Get-Content -LiteralPath (Join-Path $uat09Workspace 'observed-control-before.json')
Get-Content -LiteralPath (Join-Path $uat09Workspace 'observed-state-before.json')
Get-Content -LiteralPath (Join-Path $uat09Workspace 'observed-manual-fallback.md')
$uat09StateAfter = Get-Content -Raw -LiteralPath `
    (Join-Path $uat09Run 'state.json') | ConvertFrom-Json
$uat09LastAudit = Get-Content -LiteralPath `
    (Join-Path $uat09Run 'audit\events.jsonl') |
    Where-Object { $_.Trim() } |
    Select-Object -Last 1 |
    ConvertFrom-Json
$uat09ObservedState = [ordered]@{
    current_state = $uat09StateAfter.current_state
    latest_attempt_state = $uat09LastAudit.state
    latest_event_type = $uat09LastAudit.event_type
    external_actions = $uat09StateAfter.external_actions
    local_export_count = $uat09StateAfter.local_export_count
}
[System.IO.File]::WriteAllText(
    (Join-Path $uat09Workspace 'observed-state-after-safe-stop.json'),
    ($uat09ObservedState | ConvertTo-Json),
    $utf8NoBom
)
$uat09FailureEvidence = Confirm-SafeStopEvidence `
    -BasePath $uat09Run `
    -EvidenceBaseRelative $uat09RunLocator `
    -ExpectedErrorCode 'external_action_blocked'
[System.IO.File]::WriteAllText(
    (Join-Path $uat09Workspace 'observed-failure-evidence.json'),
    ($uat09FailureEvidence | ConvertTo-Json),
    $utf8NoBom
)
Get-Content -LiteralPath (Join-Path $uat09Workspace 'observed-failure-evidence.json')
Get-Content -LiteralPath (Join-Path $uat09Workspace 'observed-state-after-safe-stop.json')
Test-Path -LiteralPath (Join-Path $uat09Run 'outbox')
```

**Given:** a fresh UAT-09 run whose simulated AI timeout selected the
deterministic fallback and whose control initially disables external actions.
**When:** the draft is approved, the local control is deliberately tampered to
enable external actions, and export is attempted. **Then:** the original
control says `EXTERNAL_ACTIONS_ENABLED` is `false`; the
timeout uses the deterministic fallback; the fallback names an owner,
`issues/issues.csv`, and no external action; tampering produces `SAFE STOP`,
exit code `1`, error code `external_action_blocked`, latest attempt state
`failed_manual`, last valid `current_state` still
`approved_for_local_export`, external actions `0`, and no outbox. Evidence:
the fresh attempt's `attempt-info.json`, `observed-*` files,
`failures\latest.json`, and the immutable `failures/aNNNN.json` followed from
`history_path`. `observed-failure-evidence.json` must show
`external_action_blocked` and matching SHA-256 values.

### Recreation 3 — Record the nine observations and one defect/retest

List the exact attempt records before writing your results:

```powershell
Get-ChildItem -LiteralPath $scenarioRoot -Filter 'attempt-info.json' -Recurse |
    Sort-Object FullName |
    ForEach-Object {
        Get-Content -Raw -LiteralPath $_.FullName | ConvertFrom-Json
    } |
    Format-Table scenario_id,attempt_number,relative_path,prior_attempts_preserved
```

In `recreated_uat.md`, make one scenario record for UAT-01 through UAT-09.
For each record, write:

- tester role;
- Given/When/Then from the matching instruction;
- expected state or error code;
- the exact relative evidence path;
- what you actually observed;
- `PASS`, `FAIL`, or `BLOCKED`;
- any defect identifier and retest result.

Use the exact `relative_path` from `attempt-info.json`. If an **unexpected**
interruption or failure caused numbered retries, record every affected attempt
and identify the fresh attempt used for the final result. A later pass does not
erase the earlier evidence. A clean first-attempt completion—including a
planned, correctly evidenced `SAFE STOP`—needs no numbered retry.

Do not copy “pass” before checking the files. A red `SAFE STOP` is a passing
result when it is the stated safe behaviour.

Now create one deliberate draft defect so that you practise rejection and
retest instead of submitting an empty defect process:

```powershell
$defectFolder = New-UatAttemptFolder -ScenarioId 'UAT-D01'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $defectFolder `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'UAT-D01 prepare unexpectedly failed.' }
$defectSavedRun = Resolve-SavedCourseRun $defectFolder
$defectRunLocator = $defectSavedRun.Locator
$defectRun = $defectSavedRun.Path
$unsafeDraftPath = Join-Path $defectFolder 'unsafe-wording-draft.json'
$correctedDraftPath = Join-Path $defectFolder 'corrected-draft.json'
$defectDraft = Get-Content -Raw -LiteralPath (Join-Path $defectRun 'draft\summary.json') |
    ConvertFrom-Json
$defectDraft.headline = 'Ready to send these actions externally.'
[System.IO.File]::WriteAllText(
    $unsafeDraftPath,
    ($defectDraft | ConvertTo-Json -Depth 20),
    $utf8NoBom
)
$defectDraft.headline = '13 verified synthetic issues require human review.'
[System.IO.File]::WriteAllText(
    $correctedDraftPath,
    ($defectDraft | ConvertTo-Json -Depth 20),
    $utf8NoBom
)
& $pythonExe $runner validate-summary `
    --run-dir $defectRun `
    --candidate $correctedDraftPath |
    Tee-Object -FilePath (Join-Path $defectFolder 'retest-command.txt')
if ($LASTEXITCODE -ne 0) { throw 'UAT-D01 corrected-draft retest failed.' }
Copy-Item -LiteralPath (Join-Path $defectRun 'review\candidate-validation.json') `
    -Destination (Join-Path $defectFolder 'retest-validation.json')
```

Open both drafts. Record `UAT-D01` as a high-severity wording defect because
the first headline is unsupported and implies a forbidden external action.
Record the human decision `REJECT`, owner `course learner`, the corrected
headline, the successful structural/reference retest, and the remaining need
for statement-level human support review. Record the exact UAT-D01
`attempt-info.json` relative path and any numbered retry. Neither file sends
anything.

### Recreation 4 — Complete adoption and handover evidence

Complete `recreated_adoption.md` with role changes, eight demonstrated training
tasks, accessibility/support needs, feedback route, resistance or misuse
risks, owner, and refresher trigger.

Complete `recreated_handover.md` with:

- purpose, exclusions, architecture, files, versions, hashes, and states;
- data/rule/prompt/provider configuration and evaluation evidence;
- UAT and known defects;
- access, backup, restore, monitoring, incident, update, and exit owners;
- startup, normal run, safe failure, fallback, rollback, and deletion;
- residual risks and limitations.

### Recreation 5 — Reassess and finalise the post-UAT decision

Preserve the Module 8 record and copy it once into Module 9:

```powershell
$moduleEightDecision = Join-Path $projectRoot 'evidence\module-08\recreated_evaluation_decision.md'
if (-not (Test-Path -LiteralPath $moduleEightDecision)) {
    throw 'Module 8 provisional decision is missing. Return to Module 8.'
}
Copy-NewPracticeFile $moduleEightDecision .\recreated_final_decision.md
notepad .\recreated_final_decision.md
```

In the copied record:

1. preserve the Module 8 `PROVISIONAL PRE-UAT` recommendation and its evidence;
2. add the UAT-01 to UAT-09 result, UAT-D01 rejection/retest, adoption evidence,
   training result, handover readiness, defects, and residual limitations;
3. write whether this new evidence confirms or changes the recommendation and
   why;
4. set `Decision stage/status` to exactly `FINAL POST-UAT`;
5. choose exactly one final label: `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`,
   or `DO NOT CONTINUE`.

Then use the matching closeout path:

- `ACCEPT FOR SYNTHETIC PORTFOLIO`: package the synthetic evidence and state
  every limitation prominently. This does not authorize business use.
- `REWORK`: list each failed threshold, its evidence, the smallest corrective
  task, owner, and retest. Do not present the workflow as accepted.
- `DO NOT CONTINUE`: record the reason, preserve the audit trail, confirm
  external actions remain disabled, and close the exercise without promoting
  the workflow.

All three evidence-backed outcomes can pass Course 1. Course 1 never
transitions to client use. A final prototype label still cannot repair a failed
course rubric.

### Recreation 6 — Complete the mandatory Course 1 assessment

First open the complete fictional assessment example:

```powershell
notepad (Join-Path $courseRoot 'worked_examples\module_09_assessment_record.md')
notepad (Join-Path $courseRoot 'ASSESSMENT_AND_RUBRIC.md')
```

Read it from top to bottom. Notice that it:

- checks every prerequisite before scoring;
- scores all six areas separately;
- shows the weight calculation;
- answers all ten questions in plain language;
- cites evidence instead of giving confidence-based scores;
- keeps the rubric result separate from the final prototype decision.

Now recreate that method for your different capstone:

```powershell
$courseAssessmentCreated = Start-NewPracticeTextFile -Path .\recreated_course_assessment.md
notepad .\recreated_course_assessment.md
```

If the helper printed `CREATED`, create these exact sections. If it printed
`SKIP CREATE`, keep all existing work and continue only missing sections:

1. `Assessment identity and boundary`;
2. `Pass prerequisites`;
3. `Six-area rubric`;
4. `Objective calculation`;
5. `Ten oral demonstration answers`;
6. `Assessment result and limitations`.

In `Pass prerequisites`, copy every prerequisite from
`ASSESSMENT_AND_RUBRIC.md`, record `PASS` or `FAIL`, and give a relative
evidence path. Any `FAIL` means `NOT YET`; stop before scoring.

In `Six-area rubric`, make this table and complete every cell from evidence:

```markdown
| Area | Weight | Level (1-4) | Points = weight x level / 4 | Evidence and reason |
|---|---:|---:|---:|---|
| Process discovery and opportunity selection | 20 | | | |
| Data quality and deterministic controls | 20 | | | |
| Bounded AI and evidence | 15 | | | |
| Human control and failure behaviour | 15 | | | |
| Dutch SME risk and tool-fit screen | 15 | | | |
| Evaluation, adoption, and handover | 15 | | | |
```

Use only whole-number levels `1`, `2`, `3`, or `4`. A missing independent
tester limits UAT evidence to Competent for the relevant area and must retain
`EXTERNAL UAT NOT VERIFIED`; it does not prevent Course 1 completion.

Verify your arithmetic by replacing the six example `3` values below with your
six recorded levels in table order:

```powershell
$levels = @(3,3,3,3,3,3)
$weights = @(20,20,15,15,15,15)
if ($levels.Count -ne 6) { throw 'Enter exactly six rubric levels.' }
if (@($levels | Where-Object { $_ -notin 1,2,3,4 }).Count -ne 0) {
    throw 'Every rubric level must be a whole number from 1 through 4.'
}
$areaPoints = for ($index = 0; $index -lt 6; $index++) {
    $weights[$index] * $levels[$index] / 4
}
$total = ($areaPoints | Measure-Object -Sum).Sum
[PSCustomObject]@{
    levels = $levels -join ','
    points = $areaPoints -join ','
    total = $total
    every_area_competent = (@($levels | Where-Object { $_ -lt 3 }).Count -eq 0)
    score_gate_pass = ($total -ge 75)
}
```

**Expected gate for a pass:** exactly six point values, total at least `75`,
`every_area_competent` is `True`, and `score_gate_pass` is `True`. Copy the
displayed levels, points, and total into `recreated_course_assessment.md`.
Never raise a level merely to make the total pass.

Under `Ten oral demonstration answers`, write and then say aloud your own
answers to these exact questions:

1. What business problem are you solving?
2. What evidence says it is worth solving?
3. Which data is authoritative?
4. Which decisions are deterministic?
5. What does AI contribute?
6. What happens when AI fails?
7. What exactly does the reviewer approve?
8. What can the system never do?
9. How would you detect regression?
10. Why is your final Course 1 decision justified?

For each answer record: your plain-language answer, one evidence path, and
`ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES` or `NO`. Any missing
answer, unsupported answer, or `NO` means `NOT YET`.

### Recreation 7 — Complete the honest case and five-minute demonstration

Create `recreated_portfolio_case.md` with problem, method, controls, measured
synthetic evidence, what you learned, and limitations. For `REWORK`, label it
an incomplete learning case. For `DO NOT CONTINUE`, write a lessons-learned
closure instead of a success case.

Create `recreated_demo_script.md` for a five-minute demonstration:

- minute 0–1: problem and boundary;
- minute 1–2: deterministic issues and evidence;
- minute 2–3: bounded summary and support;
- minute 3–4: review, hash invalidation, and fallback;
- minute 4–5: evaluation, limitations, and decision.

Do not claim this exercise saved a client's time or money.

Create or safely resume both files:

```powershell
$portfolioCreated = Start-NewPracticeTextFile -Path .\recreated_portfolio_case.md
$demoCreated = Start-NewPracticeTextFile -Path .\recreated_demo_script.md
notepad .\recreated_portfolio_case.md
notepad .\recreated_demo_script.md
```

For each file, write the instructed content only when the helper printed
`CREATED`. When it printed `SKIP CREATE`, continue only genuinely incomplete
content and never paste a fresh replacement over a completed file.

Verify:

```powershell
Select-String -Path .\recreated_uat.md -Pattern 'UAT-01','UAT-09','Given','When','Then','failed_manual','UAT-D01','retest','EXTERNAL UAT NOT VERIFIED'
Select-String -Path .\recreated_handover.md -Pattern 'fallback','rollback','restore','incident','limitation','owner'
Select-String -Path .\recreated_final_decision.md -Pattern 'PROVISIONAL PRE-UAT','FINAL POST-UAT','UAT-D01','synthetic'
Select-String -Path .\recreated_course_assessment.md -Pattern 'Process discovery','Evaluation, adoption','total','What business problem','Why is your final Course 1 decision','ANSWERED ALOUD'
Select-String -Path .\recreated_portfolio_case.md -Pattern 'synthetic','not production','Course 1'
```

**Expected result:** every search term appears in the relevant evidence.
Missing terms identify work to finish; they are not permission to weaken
acceptance.

### Recreation 8 — Assemble the single capstone repository

The setup and every module now belong to this one Git repository. Create a
root index so another person can find the evidence without guessing.

Run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
$capstoneIndexCreated = Start-NewPracticeTextFile -Path .\CAPSTONE_INDEX.md
notepad .\CAPSTONE_INDEX.md
```

If the helper printed `CREATED`, create an `Artifact map` table with one row
for setup and one row for each Module 1 through Module 9. If it printed
`SKIP CREATE`, keep the existing index and continue only missing rows. For each
row record:

- the folder, such as `evidence/module-04`;
- the main worked and recreated artifacts;
- the pass evidence;
- the final rubric total and oral-answer record for Module 9;
- the Git commit identifier from `git log --oneline`;
- any limitation or rework still open.

Module 9 has not been committed yet because the read-only PASS comes first.
Enter `PENDING UNTIL FINAL PASS` in only that row. You will replace it with the
real identifier during the final checkpoint.

Also add these headings: `Synthetic boundary`, `Architecture and data flow`,
`Deterministic workflow`, `Bounded artificial-intelligence step`, `Human
control`, `Evaluation decision`, and `Closeout status`. Link them to repository
paths. Do not paste files into the index.

Then create the repository change history:

```powershell
$changeLogCreated = Start-NewPracticeTextFile -Path .\CHANGELOG.md
notepad .\CHANGELOG.md
```

If the helper printed `CREATED`, start it with the block below. If it printed
`SKIP CREATE`, do not paste a second heading; continue only the missing
closeout fields.

```markdown
# Project change log

## Course 1 closeout — REPLACE WITH ACTUAL LOCAL DATE (YYYY-MM-DD)

- Assembled setup and Modules 1–9 in one local Git repository.
- Final decision: REPLACE WITH ONE EXACT PERMITTED DECISION.
- External actions: disabled.
- Data: synthetic course data only.
- Known limitations: REPLACE WITH YOUR EVIDENCE.
```

Replace the date, decision, and limitation placeholders with your actual local
completion date and your own evidence. `CHANGELOG.md` records what changed;
`CAPSTONE_INDEX.md` records where the evidence is.

## Ask Codex to check your work

Run `(Resolve-Path $projectRoot).Path` to obtain the full project path. Replace
`[PASTE FULL PATH HERE]` and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full Course 1 project repository:
[PASTE FULL PATH HERE]

Learner attestation: I created these files for this fictional exercise and
have not knowingly put real client, employer, personal, medical, credential,
or secret data in them. This statement is an attestation, not proof.

You may use only read-only directory-listing, file-reading, and SHA-256 hashing
commands inside this repository. Do not create, edit, delete, rename, move, or
format anything. Do not run project scripts, workflows, or tests, and do not
use network or cloud commands. Do not inspect the parent or another path. If
apparent sensitive data is noticed, do not quote or repeat it: return NOT YET
with only the filename and general category, then stop. If none is noticed,
say that non-detection is not proof that none exists.

Return:
1. PASS or NOT YET;
2. checks for: nine distinct Given/When/Then UAT scenarios UAT-01 through
UAT-09; actual isolated command evidence and exact expected state/error for
each; Stage 1 checks the safe path length, exact `COURSE_PROJECT.md` marker,
and resolved Git root before any lesson write or runner execution; every
attempt has `attempt-info.json`; only when an unexpected
interruption or unexpected failure occurred, that attempt is preserved and its
rerun uses the next numbered retry; a clean first-attempt completion requires
no retry; UAT-03, UAT-06, UAT-08, and UAT-09 each check
`failures/latest.json`, the exact expected `error_code`, the `history_path`
immutable `failures/aNNNN.json`, and matching hashes; UAT-D01 rejection,
correction, and retest; exact-draft and
EXTERNAL_ACTIONS_ENABLED=false drills; role-specific
training with demonstrated tasks; feedback/support; complete normal and
safe-failure runbook; manual fallback; rollback; backup/restore; monitoring;
incident/update/exit owners; versions and hashes; limitations and residual
risks; the preserved PROVISIONAL PRE-UAT recommendation; reassessment using
UAT/defect/adoption/handover evidence; Decision stage/status exactly FINAL
POST-UAT; exactly one permitted evidence-backed final decision; the matching
accept/rework/closure path; honest portfolio or lessons-learned case;
five-minute demo; every assessment prerequisite explicitly PASS with evidence;
all six rubric areas scored at whole-number level 3 or 4; correct weighted
points; total at least 75; ten distinct supported plain-language answers; all
ten marked ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES; the rubric
result remains separate from the prototype decision; CAPSTONE_INDEX.md maps
setup and Modules 1-9; CHANGELOG.md
records the closeout; no claim of client savings, production readiness, or
consultant certification. Allow only the Module 9 commit cell to say PENDING
UNTIL FINAL PASS because this review must happen before that commit;
3. the smallest corrections for me to make if NOT YET.

Remain read-only. Do not run project code, workflows, or tests, change scores,
supply missing oral answers, or complete the handover/UAT for me. A PASS is
allowed only when every objective gate above is already evidenced.
```

## Pass criteria

- [ ] Worked UAT/handover and tabletop rehearsal are complete.
- [ ] Stage 1 checks the safe path length, exact `COURSE_PROJECT.md` marker,
      and resolved Git root before any lesson write or runner execution.
- [ ] UAT-01 through UAT-09 were actually executed in isolated folders and
      each record has Given/When/Then, expected state/error, observed evidence,
      result, and exact relative path.
- [ ] Every scenario and UAT-D01 has `attempt-info.json`; any unexpectedly
      interrupted or unexpectedly failed attempt remains unchanged, and its
      rerun uses and records the next numbered retry folder. Clean first
      attempts require no numbered retry.
- [ ] Solo testing says `EXTERNAL UAT NOT VERIFIED`; no real-user claim is
      made unless another consenting person actually tested synthetic data.
- [ ] Failures, review choices, hash invalidation, and fallback are tested.
- [ ] UAT-03, UAT-06, UAT-08, and UAT-09 each verify
      `failures/latest.json`, the expected `error_code`, the immutable
      `failures/aNNNN.json` followed from `history_path`, and matching hashes.
- [ ] UAT-D01 records the unsafe wording rejection, correction, and retest;
      any other defects are recorded and retested rather than hidden.
- [ ] Training is role-specific and demonstrated.
- [ ] Runbook covers normal run, stop, fallback, rollback, restore, and
      escalation.
- [ ] Handover assigns every continuing responsibility.
- [ ] The Module 8 `PROVISIONAL PRE-UAT` recommendation is preserved.
- [ ] The copied decision is reassessed using UAT, defect/retest, adoption, and
      handover evidence and marked exactly `FINAL POST-UAT`.
- [ ] The exact final decision is `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`,
      or `DO NOT CONTINUE`, and its evidence supports it.
- [ ] The matching accept, corrective, or safe-closure path is complete.
- [ ] Portfolio, incomplete case, or lessons-learned closure states evidence
      and limitations honestly.
- [ ] Every assessment prerequisite is explicitly `PASS` with an evidence path.
- [ ] All six rubric areas have an evidence-backed whole-number level of at
      least 3, the weighted total is at least 75, and the calculation is saved.
- [ ] All ten oral questions have a supported plain-language answer and are
      marked `ANSWERED ALOUD WITHOUT READING GENERATED TEXT: YES`.
- [ ] The rubric result and final prototype decision remain separate.
- [ ] Root `CAPSTONE_INDEX.md` maps setup and all nine modules.
- [ ] Root `CHANGELOG.md` records the dated decision and limitations.
- [ ] The read-only review records the learner's synthetic-data statement as
      an attestation rather than proof and says non-detection is not proof of
      absence.
- [ ] Codex returns `PASS` read-only.

### Record the final Course 1 PASS in Git

Do this only after Codex returns `PASS`. Rerun the complete Stage 1 block first,
even if this PowerShell window is still open. Stop if its project-marker,
Git-root, or path-length guard fails. The first commit records Module 9 just
like every earlier module. The second commit records the two root assembly
files. Then run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-09"
git commit --only -m "complete module 9 evidence" -- "evidence/module-09"
git log --oneline --max-count=10
```

Run `notepad .\CAPSTONE_INDEX.md`, replace `PENDING UNTIL FINAL PASS` with the
new Module 9 identifier shown by `git log`, save, and close Notepad. Then run:

```powershell
git add -- "CAPSTONE_INDEX.md" "CHANGELOG.md"
git commit --only -m "assemble Course 1 synthetic capstone" -- `
    "CAPSTONE_INDEX.md" "CHANGELOG.md"
git status --short
git log --oneline --max-count=10
```

Expected result: the newest commit assembles the Course 1 closeout, the next
commit records Module 9, and earlier module checkpoints are visible below it.
Both `git commit --only` commands restrict their checkpoint to the repeated
paths, even if a different file had already been staged. If Git reports
`nothing to commit`, confirm that the relevant named paths were already
recorded and unchanged. Never add a secret, real data, or unrelated file.

## Consultant lens

Implementation is not finished when code runs. It is finished only when users
can perform the work, owners accept responsibilities, failures have a route,
evidence supports the decision, and the organisation can continue without the
builder.

## Capstone increment

The Course 1 capstone is complete as an evidence-controlled synthetic project
with executable UAT, a defect/retest, adoption plan, runbook, handover, a
reassessed final decision, a passing six-area rubric, ten oral answers, and an
honest case or closure record.

## Required artifact

The teaching contract creates the worked pack/rehearsal and the recreated UAT,
scenario evidence, defect/retest, adoption, handover, final decision, Course 1
assessment, portfolio or closure, and demo evidence under `evidence/module-09`,
plus root `CAPSTONE_INDEX.md` and `CHANGELOG.md`.

## Test gate

The **Pass criteria** are the complete Course 1 gate.

## Stop or rework

Stop if UAT is vague or only imagined, defects are hidden, owners are
placeholders, fallback was not rehearsed, an action can escape, real data
appears, a weak rubric area is averaged away, oral answers are copied, or
synthetic evidence is presented as client proof.

## Common failures

- Asking whether users “like it” instead of testing tasks.
- Training features instead of roles and decisions.
- Handing over code without operation and incident ownership.
- Treating self-test as independent acceptance.
- Giving yourself unsupported rubric levels or reading generated oral answers.
- Calling Course 1 completion professional certification.

## Estimated time

16–22 hours.
