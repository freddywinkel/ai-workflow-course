# Module 9 — Rehearse Operational Acceptance, Hand Over, and Pass the Course 1 Assessment

## Outcome

You will execute a role-simulated operational acceptance rehearsal, prepare a
candidate User Acceptance Testing (UAT) script, plan training and adoption,
write a runbook and fallback, assemble handover evidence, make a bounded final
post-rehearsal decision, complete an unseen second-domain transfer and delayed
retention check, prepare evidence for an independently scored six-area rubric
and live oral assessment, and write an honest portfolio case.

User Acceptance Testing (UAT) means another consenting intended user tries
realistic scenarios and confirms whether the workflow supports the agreed
work. When you perform the same tasks yourself while acting in another role,
the evidence is a role-simulated operational acceptance rehearsal—not real
UAT—and remains `EXTERNAL UAT NOT VERIFIED`.

Passing Course 1 proves a synthetic foundation project. It does not certify you
as a production consultant or regulated-systems specialist.

## Beginner checkpoint

Start when Modules 1–8 pass. Module 8 produced a `PROVISIONAL PRE-UAT`
recommendation using one of the three permitted labels:
`ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or `DO NOT CONTINUE`. Module 9
does not copy that recommendation blindly. You add technical regression
scenarios, role-simulated operator tasks, defect/retest, adoption, and handover
evidence, reassess the label, and mark the result `FINAL POST-REHEARSAL`. Use
`FINAL POST-UAT` only when another consenting person actually performs the
candidate tasks and that evidence is recorded separately. This module closes
and indexes the evidence honestly; it does not force a positive decision. All
acceptance work remains synthetic and local.

## Concepts

- A **role-simulated operational acceptance rehearsal** means the learner
  performs predefined operator and reviewer tasks while keeping
  `EXTERNAL UAT NOT VERIFIED`.
- **User Acceptance Testing (UAT)** means another consenting intended user
  checks whether a system supports agreed work in realistic scenarios.
- **Adoption** is sustained correct use, not simply installing software.
- A **runbook** tells an operator how to run, monitor, stop, recover, and
  escalate.
- **Handover** transfers evidence, instructions, access responsibilities,
  limitations, and continuing ownership.
- **Benefits realisation** measures whether the expected benefit appears after
  use.
- **Rollback** returns to a known safe earlier method or version.
- An **identifier (ID)** distinguishes one test or evidence item.
- The identifier prefix **Operational Acceptance Rehearsal operator task
  (OAR-OP)** labels each hands-on operator task in the solo rehearsal.
- **Secure Hash Algorithm 256-bit (SHA-256)** creates a repeatable fingerprint
  of exact file bytes.
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

1. follow and rehearse the worked operational-acceptance/handover pack;
2. inspect the completed worksheets and execute nine isolated capstone
   scenarios;
3. complete adoption and handover, then reassess the Module 8 recommendation;
4. complete unseen transfer, delayed retention when due, self-reflection, and
   the evidence pack for independent artifact and oral assessment;
5. complete the portfolio/demo, assemble the index/change log, run the final
   bounded Codex check, correct gaps, and make the two final Git checkpoints.

Treat each numbered item as several focused blocks of at most 60 minutes:

- **UNDERSTAND:** explain the operator task, evidence, decision, fallback,
  owner, and limitation;
- **RUN HELPER:** execute path, copy, locator, and preservation commands
  exactly; understand their purpose and stop conditions rather than memorising
  them;
- **PERFORM:** carry out the operator, reviewer, transfer, and oral tasks
  yourself;
- **GATE:** record observed evidence before moving to the next scenario.

Safe mini-gates are after the worked rehearsal, after scenarios TECH-01 through
TECH-06, after TECH-09 and TECH-D01, after handover, after unseen transfer, and
after independent assessment. Stop at one of these points whenever attention
drops; do not finish a long command sequence from memory.

Before stopping, save every file and note the last numbered step. Rerun Stage 1
after opening a new PowerShell window. Do not mark the course complete until
the final practical and rubric gates both pass.

## Follow along — I show you exactly how

**Expected result:** a complete worked operational acceptance rehearsal,
candidate UAT script, adoption, runbook, handover, final decision, unseen
transfer, assessment evidence, and honest portfolio pack for a synthetic
scenario.

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
    -Path .\worked_acceptance_and_handover.md `
    -RequiredPatterns `
        '# Worked role-simulated acceptance rehearsal and handover', `
        'EXTERNAL UAT NOT VERIFIED', `
        'Limitations: no client, real data, production deployment, or proven cash saving.'
if ($workedPackCreated) {
    notepad .\worked_acceptance_and_handover.md
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
# Worked role-simulated acceptance rehearsal and handover — fictional low-stock list

**Evidence status:** `ROLE_SIMULATED_ACCEPTANCE_REHEARSAL`

**External-user status:** `EXTERNAL UAT NOT VERIFIED`

## Boundary

Synthetic local spreadsheet configuration. It identifies quantity below an
approved threshold for internal review. It does not use AI, order, message,
select suppliers, pay, or write to a source system.

## Roles

- Process owner: operations lead; approves rules and acceptance.
- User: inventory coordinator; runs and reviews the list.
- Support owner: office systems coordinator; supports access and restore.
- Tester: course learner acting in a separate tester role.

## Technical regression and role-simulated result

| ID | Given | When | Then | Evidence | Result |
|---|---|---|---|---|---|
| TECH-01 | all quantities meet thresholds | user runs filter | empty exception list and no action state | screenshot-free result note and row count | pass |
| TECH-02 | one quantity is below threshold | user runs filter | one issue shows item ID, raw value, threshold, rule | saved synthetic output | pass |
| TECH-03 | quantity cell is blank | user runs filter | item stops for human review; zero is not invented | failure note | pass |
| TECH-04 | expected header is renamed | user runs filter | safe stop and manual fallback | failure record | pass |
| TECH-05 | user tries to treat list as an order | reviewer checks boundary | wording says internal review only | review note | pass |

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
- technical rehearsal, candidate UAT script, and role-simulated result record;
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
Evidence: frozen synthetic tests and five role-simulated technical regression
scenarios pass.
Limitations: no client, real data, production deployment, or proven cash saving.
```

Run:

```powershell
Select-String -Path .\worked_acceptance_and_handover.md -Pattern 'TECH-01','TECH-05','Safe failure','Known limitations','ACCEPT FOR SYNTHETIC PORTFOLIO'
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

Read TECH-04 aloud and perform a tabletop rehearsal:

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
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\uat_script.md') .\recreated_acceptance_rehearsal.md
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\adoption_and_training_plan.md') .\recreated_adoption.md
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\acceptance_and_handover.md') .\recreated_handover.md
```

Open all three files and write `EXTERNAL UAT NOT VERIFIED` near the top of
`recreated_acceptance_rehearsal.md` when you are testing alone:

```powershell
notepad .\recreated_acceptance_rehearsal.md
notepad .\recreated_adoption.md
notepad .\recreated_handover.md
```

A complete role-simulated operational acceptance rehearsal can support a
Competent artifact level, but it is not evidence that a real user can operate
the workflow. Another consenting person using synthetic data is required for a
Strong real-UAT rating. A separate independent calibrated assessor is still
required for the Course 1 competence decision; neither activity authorises
workplace research.

### Recreation 2 — Execute nine technical regression scenarios as rehearsal

Do not merely write what you think would happen. Run each command below in the
separate scenario folder, compare the observable evidence with the stated
expectation, and then record your own observed result in `recreated_acceptance_rehearsal.md`.
Every input is synthetic, every output stays on this computer, and no command
contains a network or external-action function.

The `TECH-NN` prefix identifies solo technical regression evidence. It is
deliberately different from `UAT-NN`, which is reserved for candidate tasks
performed by another consenting intended user. Running TECH scenarios yourself
does not create UAT; the evidence status remains
`ROLE-SIMULATED OPERATIONAL ACCEPTANCE REHEARSAL`.

In status evidence, `current_state` is the last valid persistent workflow
state. `latest_attempt_state` is the newest audit-event state; it becomes
`failed_manual` after a safe stop without overwriting that last valid state.

Create the parent folder and the safe retry helper. Run this block again after
opening a new PowerShell window. The helper uses `TECH-01` for the first attempt
and then `TECH-01-retry-02`, `TECH-01-retry-03`, and so on. It never deletes,
resumes inside, or overwrites an interrupted attempt.

```powershell
$scenarioRoot = Join-Path $moduleFolder 'technical-scenarios'
New-Item -ItemType Directory -Force -Path $scenarioRoot | Out-Null
function New-TechAttemptFolder {
    param(
        [Parameter(Mandatory)]
        [ValidatePattern('^TECH-(0[1-9]|D01)$')]
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
        relative_path = (Join-Path 'technical-scenarios' $folderName)
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
2. note the last visible error in `recreated_acceptance_rehearsal.md`;
3. correct only the cause outside that attempt folder;
4. rerun the **entire matching TECH block from its first line**;
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

#### TECH-01 — Clean input ends with no action needed

```powershell
$tech01Workspace = New-TechAttemptFolder -ScenarioId 'TECH-01'
& $pythonExe $runner prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\valid_no_issue.csv') `
    --workspace $tech01Workspace `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-01 unexpectedly failed.' }
$tech01SavedRun = Resolve-SavedCourseRun $tech01Workspace
$tech01RunLocator = $tech01SavedRun.Locator
$tech01Run = $tech01SavedRun.Path
& $pythonExe $runner status --run-dir $tech01Run |
    Tee-Object -FilePath (Join-Path $tech01Workspace 'observed-status.txt')
if ($LASTEXITCODE -ne 0) { throw 'TECH-01 status validation unexpectedly failed.' }
$tech01FixtureHash = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    (Join-Path $courseRoot 'course1_capstone\fixtures\failures\valid_no_issue.csv')).Hash
$tech01CopiedHash = (Get-FileHash -Algorithm SHA256 -LiteralPath `
    (Join-Path $tech01Run 'source\work_items.csv')).Hash
$tech01Hashes = @(
    [PSCustomObject]@{
        Role = 'supplied_clean_fixture'
        RelativePath = 'course1_capstone/fixtures/failures/valid_no_issue.csv'
        SHA256 = $tech01FixtureHash
    }
    [PSCustomObject]@{
        Role = 'protected_run_copy'
        RelativePath = 'source/work_items.csv'
        SHA256 = $tech01CopiedHash
    }
)
$tech01Hashes | Format-Table Role,RelativePath,SHA256 -AutoSize
$tech01Hashes | Export-Csv -NoTypeInformation `
    -Encoding UTF8 -LiteralPath (Join-Path $tech01Workspace 'observed-source-hashes.csv')
[PSCustomObject]@{
    draft_exists = Test-Path -LiteralPath (Join-Path $tech01Run 'draft')
    outbox_exists = Test-Path -LiteralPath (Join-Path $tech01Run 'outbox')
} | Format-List | Out-File -Encoding utf8 `
    (Join-Path $tech01Workspace 'observed-absent-folders.txt')
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

#### TECH-02 — The frozen set produces exactly all 13 issue triples

```powershell
$tech02Workspace = New-TechAttemptFolder -ScenarioId 'TECH-02'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $tech02Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-02 unexpectedly failed.' }
$tech02SavedRun = Resolve-SavedCourseRun $tech02Workspace
$tech02RunLocator = $tech02SavedRun.Locator
$tech02Run = $tech02SavedRun.Path
Copy-Item -LiteralPath (Join-Path $tech02Run 'evaluation.json') `
    -Destination (Join-Path $tech02Workspace 'observed-evaluation.json')
(Import-Csv -LiteralPath (Join-Path $tech02Run 'issues\issues.csv')).Count
Get-Content -LiteralPath (Join-Path $tech02Workspace 'observed-evaluation.json')
```

**Given:** the frozen 15-row synthetic register and its 13 expected issue
identities. **When:** the workflow prepares TECH-02 with the offline mock and
compares the generated issues with the expected file. **Then:** count `13`;
true positives `13`; false positives `0`; false
negatives `0`; state `needs_review`; and external actions `0`. Evidence:
the fresh attempt's `attempt-info.json`, `observed-evaluation.json`, and the
named run's `issues\issues.csv`.

#### TECH-03 — An invalid header safely stops

```powershell
$tech03Workspace = New-TechAttemptFolder -ScenarioId 'TECH-03'
$tech03Output = & $pythonExe $runner prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\unexpected_header.csv') `
    --workspace $tech03Workspace `
    --ai-mode disabled `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY 2>&1
$tech03Exit = $LASTEXITCODE
$tech03Output | Tee-Object -FilePath (Join-Path $tech03Workspace 'observed-command.txt')
if ($tech03Exit -ne 1) { throw "TECH-03 expected exit code 1; observed $tech03Exit." }
$tech03FailureEvidence = Confirm-SafeStopEvidence `
    -BasePath $tech03Workspace `
    -EvidenceBaseRelative '.' `
    -ExpectedErrorCode 'header_mismatch'
[System.IO.File]::WriteAllText(
    (Join-Path $tech03Workspace 'observed-failure-evidence.json'),
    ($tech03FailureEvidence | ConvertTo-Json),
    $utf8NoBom
)
Get-Content -LiteralPath (Join-Path $tech03Workspace 'observed-failure-evidence.json')
```

**Given:** the supplied synthetic file with an unexpected column header.
**When:** the workflow tries to prepare TECH-03 with AI disabled. **Then:** the
command says `SAFE STOP`, exit code is `1`, error code is
`header_mismatch`, the command-attempt record state is `failed_manual`,
external actions are `0`, no run is invented, and no review draft or outbox
exists. Evidence in the fresh attempt folder: `attempt-info.json`,
`observed-command.txt`, `failures\latest.json`, the immutable
`failures/aNNNN.json` named by its `history_path`, and
`observed-failure-evidence.json`, which must show the expected and observed
error code `header_mismatch` and matching SHA-256 values.

#### TECH-04 — The invalid date dependency is source-linked

Create a fresh scenario run so its audit and failure evidence cannot change
another technical scenario:

```powershell
$tech04Workspace = New-TechAttemptFolder -ScenarioId 'TECH-04'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $tech04Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-04 prepare unexpectedly failed.' }
$tech04SavedRun = Resolve-SavedCourseRun $tech04Workspace
$tech04RunLocator = $tech04SavedRun.Locator
$tech04Run = $tech04SavedRun.Path
$tech04Observed = Import-Csv -LiteralPath (Join-Path $tech04Run 'issues\issues.csv') |
    Where-Object {
        $_.work_item_id -eq 'WI-0003' -and
        $_.rule_code -eq 'R005' -and
        $_.field -eq 'due_date'
    }
if (@($tech04Observed).Count -ne 1) {
    throw 'TECH-04 expected exactly WI-0003|R005|due_date.'
}
$tech04Observed | Export-Csv -NoTypeInformation -Encoding UTF8 `
    -LiteralPath (Join-Path $tech04Workspace 'observed-r005.csv')
Get-Content -LiteralPath (Join-Path $tech04Workspace 'observed-r005.csv')
```

**Given:** a fresh run of the frozen synthetic register containing the
deliberately invalid date dependency for `WI-0003`. **When:** you select only
its R005 due-date issue from the generated issue file. **Then:** exactly one
issue has identity
`WI-0003|R005|due_date`, severity
`high`, the raw due date, source row, and message. Evidence:
the fresh attempt's `attempt-info.json` and `observed-r005.csv`.

#### TECH-05 — A duplicate reference reports both source rows

```powershell
$tech05Workspace = New-TechAttemptFolder -ScenarioId 'TECH-05'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $tech05Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-05 prepare unexpectedly failed.' }
$tech05SavedRun = Resolve-SavedCourseRun $tech05Workspace
$tech05RunLocator = $tech05SavedRun.Locator
$tech05Run = $tech05SavedRun.Path
$tech05Observed = Import-Csv -LiteralPath (Join-Path $tech05Run 'issues\issues.csv') |
    Where-Object {
        $_.rule_code -eq 'R010' -and
        $_.field -eq 'source_reference' -and
        $_.source_reference -eq 'REF-1006'
    }
if (@($tech05Observed).Count -ne 2) {
    throw 'TECH-05 expected two R010 records for REF-1006.'
}
$tech05Observed | Export-Csv -NoTypeInformation -Encoding UTF8 `
    -LiteralPath (Join-Path $tech05Workspace 'observed-r010-both-rows.csv')
Get-Content -LiteralPath (Join-Path $tech05Workspace 'observed-r010-both-rows.csv')
```

**Given:** a fresh run in which two synthetic rows share
`REF-1006`. **When:** you select all R010 source-reference issues for that
reference. **Then:** exactly two separate issue identities exist, one for
`WI-0006` and
one for `WI-0007`; neither row is lost. Evidence:
the fresh attempt's `attempt-info.json` and
`observed-r010-both-rows.csv`.

#### TECH-06 — An unknown summary reference is refused

```powershell
$tech06Workspace = New-TechAttemptFolder -ScenarioId 'TECH-06'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $tech06Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-06 prepare unexpectedly failed.' }
$tech06SavedRun = Resolve-SavedCourseRun $tech06Workspace
$tech06RunLocator = $tech06SavedRun.Locator
$tech06Run = $tech06SavedRun.Path
$tech06CandidatePath = Join-Path $tech06Workspace 'candidate-with-unknown-id.json'
$tech06Candidate = Get-Content -Raw -LiteralPath (Join-Path $tech06Run 'draft\summary.json') |
    ConvertFrom-Json
$tech06Candidate.groups[0].issue_ids[0] = 'WI-9999|R999|unknown'
[System.IO.File]::WriteAllText(
    $tech06CandidatePath,
    ($tech06Candidate | ConvertTo-Json -Depth 20),
    $utf8NoBom
)
$tech06Output = & $pythonExe $runner validate-summary `
    --run-dir $tech06Run `
    --candidate $tech06CandidatePath 2>&1
$tech06Exit = $LASTEXITCODE
$tech06Output | Tee-Object -FilePath (Join-Path $tech06Workspace 'observed-command.txt')
if ($tech06Exit -ne 1) { throw "TECH-06 expected exit code 1; observed $tech06Exit." }
$tech06FailureEvidence = Confirm-SafeStopEvidence `
    -BasePath $tech06Run `
    -EvidenceBaseRelative $tech06RunLocator `
    -ExpectedErrorCode 'unknown_ai_issue_reference'
[System.IO.File]::WriteAllText(
    (Join-Path $tech06Workspace 'observed-failure-evidence.json'),
    ($tech06FailureEvidence | ConvertTo-Json),
    $utf8NoBom
)
Get-Content -LiteralPath (Join-Path $tech06Workspace 'observed-failure-evidence.json')
& $pythonExe $runner status --run-dir $tech06Run |
    Tee-Object -FilePath (Join-Path $tech06Workspace 'observed-status-after-safe-stop.txt')
if ($LASTEXITCODE -ne 0) { throw 'TECH-06 status validation unexpectedly failed.' }
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

#### TECH-07 — Exact-draft approval permits two local draft exports

TECH-07 through TECH-09 use a **fixed synthetic test clock**:
`2026-07-28T10:00:00Z` for the fictional decision and
`2026-07-28T11:00:00Z` for the fictional export check. These values make the
test repeatable; they are not the date or time when you perform the course.
Keep them unchanged in these three test scenarios.

```powershell
$tech07Workspace = New-TechAttemptFolder -ScenarioId 'TECH-07'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $tech07Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-07 prepare unexpectedly failed.' }
$tech07SavedRun = Resolve-SavedCourseRun $tech07Workspace
$tech07RunLocator = $tech07SavedRun.Locator
$tech07Run = $tech07SavedRun.Path
$tech07SourceHashBefore = (Get-FileHash -Algorithm SHA256 `
    -LiteralPath (Join-Path $tech07Run 'source\work_items.csv')).Hash
& $pythonExe $runner decide `
    --run-dir $tech07Run `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Every synthetic issue, source link, statement, and action was reviewed.' `
    --expected-revision 1 `
    --evidence-reviewed `
    --decided-at 2026-07-28T10:00:00Z `
    --expires-at 2099-01-01T00:00:00Z
if ($LASTEXITCODE -ne 0) { throw 'TECH-07 approval unexpectedly failed.' }
& $pythonExe $runner export `
    --run-dir $tech07Run `
    --checked-at 2026-07-28T11:00:00Z
if ($LASTEXITCODE -ne 0) { throw 'TECH-07 local export unexpectedly failed.' }
& $pythonExe $runner status --run-dir $tech07Run |
    Tee-Object -FilePath (Join-Path $tech07Workspace 'observed-status.txt')
if ($LASTEXITCODE -ne 0) { throw 'TECH-07 status validation unexpectedly failed.' }
$tech07SourceHashAfter = (Get-FileHash -Algorithm SHA256 `
    -LiteralPath (Join-Path $tech07Run 'source\work_items.csv')).Hash
$tech07HashCheck = [PSCustomObject]@{
    source_sha256_before = $tech07SourceHashBefore
    source_sha256_after = $tech07SourceHashAfter
    source_unchanged = ($tech07SourceHashBefore -eq $tech07SourceHashAfter)
}
$tech07HashCheck | Format-List
$tech07HashCheck | ConvertTo-Json | Out-File -Encoding utf8 `
    (Join-Path $tech07Workspace 'observed-source-hash-check.json')
Get-ChildItem -LiteralPath (Join-Path $tech07Run 'outbox') -File
```

**Given:** a fresh TECH-07 run prepared from the frozen synthetic register.
**When:** a course-learner role reviews the evidence, approves exact revision
1, and requests the local export before expiry. **Then:** approval is bound to
revision `1` and its exact Secure Hash Algorithm
256-bit (SHA-256) value; state is `approved_draft`; exactly two local files
exist (`approved-r1.json` and `approved-r1.csv`); source hashes match; and
external actions are `0`. Evidence: the decision JSON, outbox files,
the fresh attempt's `attempt-info.json`, `observed-status.txt`, and
`observed-source-hash-check.json` with `source_unchanged: true`.

#### TECH-08 — Editing an approved draft invalidates approval

```powershell
$tech08Workspace = New-TechAttemptFolder -ScenarioId 'TECH-08'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $tech08Workspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-08 prepare unexpectedly failed.' }
$tech08SavedRun = Resolve-SavedCourseRun $tech08Workspace
$tech08RunLocator = $tech08SavedRun.Locator
$tech08Run = $tech08SavedRun.Path
& $pythonExe $runner decide `
    --run-dir $tech08Run `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Synthetic approval used only for the edit-invalidation test.' `
    --expected-revision 1 `
    --evidence-reviewed `
    --decided-at 2026-07-28T10:00:00Z `
    --expires-at 2099-01-01T00:00:00Z
if ($LASTEXITCODE -ne 0) { throw 'TECH-08 approval unexpectedly failed.' }
Add-Content -LiteralPath (Join-Path $tech08Run 'draft\summary.json') -Value ' '
$tech08Output = & $pythonExe $runner export `
    --run-dir $tech08Run `
    --checked-at 2026-07-28T11:00:00Z 2>&1
$tech08Exit = $LASTEXITCODE
$tech08Output | Tee-Object -FilePath (Join-Path $tech08Workspace 'observed-command.txt')
if ($tech08Exit -ne 1) { throw "TECH-08 expected exit code 1; observed $tech08Exit." }
$tech08StateAfter = Get-Content -Raw -LiteralPath `
    (Join-Path $tech08Run 'state.json') | ConvertFrom-Json
$tech08LastAudit = Get-Content -LiteralPath `
    (Join-Path $tech08Run 'audit\events.jsonl') |
    Where-Object { $_.Trim() } |
    Select-Object -Last 1 |
    ConvertFrom-Json
$tech08ObservedState = [ordered]@{
    current_state = $tech08StateAfter.current_state
    latest_attempt_state = $tech08LastAudit.state
    latest_event_type = $tech08LastAudit.event_type
    external_actions = $tech08StateAfter.external_actions
    local_export_count = $tech08StateAfter.local_export_count
}
[System.IO.File]::WriteAllText(
    (Join-Path $tech08Workspace 'observed-state-after-safe-stop.json'),
    ($tech08ObservedState | ConvertTo-Json),
    $utf8NoBom
)
$tech08FailureEvidence = Confirm-SafeStopEvidence `
    -BasePath $tech08Run `
    -EvidenceBaseRelative $tech08RunLocator `
    -ExpectedErrorCode 'edited_draft_after_approval'
[System.IO.File]::WriteAllText(
    (Join-Path $tech08Workspace 'observed-failure-evidence.json'),
    ($tech08FailureEvidence | ConvertTo-Json),
    $utf8NoBom
)
Get-Content -LiteralPath (Join-Path $tech08Workspace 'observed-failure-evidence.json')
Get-Content -LiteralPath (Join-Path $tech08Workspace 'observed-state-after-safe-stop.json')
Test-Path -LiteralPath (Join-Path $tech08Run 'outbox')
```

**Given:** a fresh TECH-08 draft that was approved at exact revision 1.
**When:** the approved summary file is edited and an export is attempted.
**Then:** `SAFE STOP`, exit code `1`, error code
`edited_draft_after_approval`, latest attempt state `failed_manual`, last valid
`current_state` still `approved_for_local_export`, external actions `0`, and no
outbox exists. Evidence: the fresh attempt's `attempt-info.json`,
`observed-command.txt`, `observed-state-after-safe-stop.json`, original
decision, `failures\latest.json`, the immutable `failures/aNNNN.json` followed
from `history_path`, and `observed-failure-evidence.json` showing
`edited_draft_after_approval` and matching SHA-256 values.

#### TECH-09 — External actions stay false and fallback stays usable

```powershell
$tech09Workspace = New-TechAttemptFolder -ScenarioId 'TECH-09'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $tech09Workspace `
    --ai-mode timeout `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-09 prepare unexpectedly failed.' }
$tech09SavedRun = Resolve-SavedCourseRun $tech09Workspace
$tech09RunLocator = $tech09SavedRun.Locator
$tech09Run = $tech09SavedRun.Path
Copy-Item -LiteralPath (Join-Path $tech09Run 'control.json') `
    -Destination (Join-Path $tech09Workspace 'observed-control-before.json')
Copy-Item -LiteralPath (Join-Path $tech09Run 'state.json') `
    -Destination (Join-Path $tech09Workspace 'observed-state-before.json')
Copy-Item -LiteralPath (Join-Path $tech09Run 'manual_fallback.md') `
    -Destination (Join-Path $tech09Workspace 'observed-manual-fallback.md')
& $pythonExe $runner decide `
    --run-dir $tech09Run `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Synthetic approval used only for the external-action control test.' `
    --expected-revision 1 `
    --evidence-reviewed `
    --decided-at 2026-07-28T10:00:00Z `
    --expires-at 2099-01-01T00:00:00Z
if ($LASTEXITCODE -ne 0) { throw 'TECH-09 approval unexpectedly failed.' }
$tech09ControlPath = Join-Path $tech09Run 'control.json'
$tech09Control = Get-Content -Raw -LiteralPath $tech09ControlPath | ConvertFrom-Json
$tech09Control.EXTERNAL_ACTIONS_ENABLED = $true
[System.IO.File]::WriteAllText(
    $tech09ControlPath,
    ($tech09Control | ConvertTo-Json -Depth 10),
    $utf8NoBom
)
$tech09Output = & $pythonExe $runner export `
    --run-dir $tech09Run `
    --checked-at 2026-07-28T11:00:00Z 2>&1
$tech09Exit = $LASTEXITCODE
$tech09Output | Tee-Object -FilePath (Join-Path $tech09Workspace 'observed-command.txt')
if ($tech09Exit -ne 1) { throw "TECH-09 expected exit code 1; observed $tech09Exit." }
Get-Content -LiteralPath (Join-Path $tech09Workspace 'observed-control-before.json')
Get-Content -LiteralPath (Join-Path $tech09Workspace 'observed-state-before.json')
Get-Content -LiteralPath (Join-Path $tech09Workspace 'observed-manual-fallback.md')
$tech09StateAfter = Get-Content -Raw -LiteralPath `
    (Join-Path $tech09Run 'state.json') | ConvertFrom-Json
$tech09LastAudit = Get-Content -LiteralPath `
    (Join-Path $tech09Run 'audit\events.jsonl') |
    Where-Object { $_.Trim() } |
    Select-Object -Last 1 |
    ConvertFrom-Json
$tech09ObservedState = [ordered]@{
    current_state = $tech09StateAfter.current_state
    latest_attempt_state = $tech09LastAudit.state
    latest_event_type = $tech09LastAudit.event_type
    external_actions = $tech09StateAfter.external_actions
    local_export_count = $tech09StateAfter.local_export_count
}
[System.IO.File]::WriteAllText(
    (Join-Path $tech09Workspace 'observed-state-after-safe-stop.json'),
    ($tech09ObservedState | ConvertTo-Json),
    $utf8NoBom
)
$tech09FailureEvidence = Confirm-SafeStopEvidence `
    -BasePath $tech09Run `
    -EvidenceBaseRelative $tech09RunLocator `
    -ExpectedErrorCode 'external_action_blocked'
[System.IO.File]::WriteAllText(
    (Join-Path $tech09Workspace 'observed-failure-evidence.json'),
    ($tech09FailureEvidence | ConvertTo-Json),
    $utf8NoBom
)
Get-Content -LiteralPath (Join-Path $tech09Workspace 'observed-failure-evidence.json')
Get-Content -LiteralPath (Join-Path $tech09Workspace 'observed-state-after-safe-stop.json')
Test-Path -LiteralPath (Join-Path $tech09Run 'outbox')
```

**Given:** a fresh TECH-09 run whose simulated AI timeout selected the
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

In `recreated_acceptance_rehearsal.md`, make one scenario record for TECH-01 through TECH-09.
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
$defectFolder = New-TechAttemptFolder -ScenarioId 'TECH-D01'
& $pythonExe $runner prepare `
    --input (Join-Path $projectRoot 'data\input\work_items.csv') `
    --expected (Join-Path $projectRoot 'tests\expected_issues.csv') `
    --workspace $defectFolder `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) { throw 'TECH-D01 prepare unexpectedly failed.' }
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
if ($LASTEXITCODE -ne 0) { throw 'TECH-D01 corrected-draft retest failed.' }
Copy-Item -LiteralPath (Join-Path $defectRun 'review\candidate-validation.json') `
    -Destination (Join-Path $defectFolder 'retest-validation.json')
```

Open both drafts. Record `TECH-D01` as a high-severity wording defect because
the first headline is unsupported and implies a forbidden external action.
Record the human decision `REJECT`, owner `course learner`, the corrected
headline, the successful structural/reference retest, and the remaining need
for statement-level human support review. Record the exact TECH-D01
`attempt-info.json` relative path and any numbered retry. Neither file sends
anything.

### Recreation 3B — Perform the six operator tasks

The nine TECH-numbered scenarios are a technical regression rehearsal. They do
not by themselves show that an operator can use the evidence. Perform these
six user-centred tasks yourself and label the result honestly:

```powershell
$operatorRehearsal = Join-Path $moduleFolder 'recreated_operator_rehearsal.md'
if (Test-Path -LiteralPath $operatorRehearsal) {
    if (-not (Test-Path -LiteralPath $operatorRehearsal -PathType Leaf) -or
        (Get-Content -LiteralPath $operatorRehearsal -TotalCount 1) -cne '# Role-simulated operator rehearsal') {
        throw 'Existing operator rehearsal is unfamiliar. Preserve it and stop.'
    }
    Write-Host "KEEPING existing $operatorRehearsal"
} else {
    @'
# Role-simulated operator rehearsal

Status: EXTERNAL UAT NOT VERIFIED
Tester: course learner acting in a separate operator role

| ID | Task performed without hidden answer | Observed result and evidence path | Help or confusion | PASS / DEFECT |
|---|---|---|---|---|
| OAR-OP-01 | locate one issue in the review package | | | |
| OAR-OP-02 | trace that issue to source row, raw field, and deterministic rule | | | |
| OAR-OP-03 | explain one summary sentence and its exact supporting issue IDs | | | |
| OAR-OP-04 | choose approve, edit, or reject and explain what exact revision is affected | | | |
| OAR-OP-05 | recognise a named safe failure and distinguish it from no-action success | | | |
| OAR-OP-06 | follow the manual fallback and name who may authorise resumption | | | |

Defects:
Smallest correction:
Retest:
External-user limitation:
'@ | Set-Content -LiteralPath $operatorRehearsal -Encoding utf8
}
notepad $operatorRehearsal
```

Actually perform each task using the saved synthetic scenario folders before
writing `PASS`. Record the exact relative path you used. If you consult the
lesson after starting a task, record that help; do not silently convert it into
independent performance. Any defect remains visible and requires correction
and retest.

This record remains a role-simulated operational acceptance rehearsal. It is
not completed User Acceptance Testing (UAT) and must retain
`EXTERNAL UAT NOT VERIFIED`.

If another person later performs the same tasks, first give them the candidate
user instructions and the following plain-language briefing. Do this **before**
asking for consent or starting a task:

1. Purpose and time: this is a synthetic Course 1 usability exercise; state
   the planned tasks and expected duration.
2. Choice: participation is voluntary. The person may pause, skip a task, or
   stop at any time without giving a reason or suffering a consequence.
3. Observation: say exactly that you will record task completion, elapsed
   time, errors, help requested, comments, facilitator interventions, defects,
   corrections, and retest results.
4. Recording: say whether screen, audio, video, or quotations are proposed.
   Each requires a separate explicit `YES`; ordinary participation consent is
   not recording consent. Default to no recording.
5. Access and deletion: name who may access the structured record and state
   its planned deletion date. Delete any temporary observation notes by that
   date as well.
6. Boundary: participation is **not** employment, medical, or professional
   evaluation. It proves neither production usability nor real-data fitness.
7. Data: use only supplied fictional data and a non-identifying participant
   code. Do not collect a name, employer, health information, credentials,
   client information, or other unnecessary personal information.

Ask the person to explain back the voluntary-stop and recording choices, answer
questions, and then record each consent choice. A `NO` to optional recording
does not prevent participation. A `NO` to participation means stop immediately
and create no UAT result.

Preserve the allowed observations in a separate
`external_synthetic_uat.md` record. Before testing, assign candidate
task IDs `UAT-01` onward and define each task and its observable success
criteria. For every participant, record the non-identifying participant code, briefing
version, participation consent, optional recording choices, access roles,
retention/deletion date, intended role, prior process experience, start/end or
elapsed time, completion, errors, help requested, comments, facilitator
interventions, defects, correction, and retest. State that the test used
synthetic data and does not establish production usability or performance with
real data. Missing participation consent, prohibited data, an undisclosed
observation, or a recording without separate consent invalidates the evidence:
stop, do not copy it into the repository, and ask for safe handling guidance.
Only a valid separate record may say `REAL SYNTHETIC UAT: VERIFIED`.

### Recreation 4 — Complete adoption and handover evidence

Complete `recreated_adoption.md` with role changes, eight demonstrated training
tasks, accessibility/support needs, feedback route, resistance or misuse
risks, owner, and refresher trigger.

Complete `recreated_handover.md` with:

- purpose, exclusions, architecture, files, versions, hashes, and states;
- data/rule/prompt/provider configuration and evaluation evidence;
- technical/operator rehearsal, candidate UAT script, external UAT status, and
  known defects;
- access, backup, restore, monitoring, incident, update, and exit owners;
- startup, normal run, safe failure, fallback, rollback, and deletion;
- residual risks and limitations.

### Recreation 5 — Reassess and finalise the post-rehearsal decision

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
2. add the TECH-01 to TECH-09 technical rehearsal result, OAR-OP-01 through
   OAR-OP-06 operator result, TECH-D01 rejection/retest, adoption evidence,
   training result, handover readiness, defects, and residual limitations;
3. write whether this new evidence confirms or changes the recommendation and
   why;
4. set `Decision stage/status` to exactly `FINAL POST-REHEARSAL` when only the
   learner performed the tasks; use `FINAL POST-UAT` only when the separate
   `external_synthetic_uat.md` evidence says
   `REAL SYNTHETIC UAT: VERIFIED`;
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

All three evidence-backed outcomes can pass the workflow decision. Course 1
never transitions to client use. A final prototype label still cannot repair a
failed or pending independent course assessment.

### Recreation 6 — Complete the unseen second-domain transfer

This scenario has not been used in the worked course. It has no answer key and
multiple decisions can pass when supported.

> A fictional community centre coordinates 24 room setups per week. Its
> synthetic table has room ID, session date, setup-owner role, chairs required,
> chairs set, safety-check status, and handover status. Three safety statuses
> are blank. Staff say setup problems happen, but no active-time or rework
> baseline exists. The existing booking system's native checklist and reminder
> capabilities have not been inspected. A manager asks for “AI automation.”
> No personal data, message, booking update, or external action is permitted.

Create the transfer record:

```powershell
$transferPath = Join-Path $moduleFolder 'unseen_second_domain_transfer.md'
if (Test-Path -LiteralPath $transferPath) {
    if (-not (Test-Path -LiteralPath $transferPath -PathType Leaf) -or
        (Get-Content -LiteralPath $transferPath -TotalCount 1) -cne '# Unseen second-domain transfer') {
        throw 'Existing transfer record is unfamiliar. Preserve it and stop.'
    }
    Write-Host "KEEPING existing $transferPath"
} else {
    @'
# Unseen second-domain transfer

## Process boundary and roles

## Evidence, assumptions, decisions, and unresolved questions

## Authoritative data and missing-data behaviour

## Deterministic rules and exact boundaries

## Optional AI contribution or NO AI decision

## Human authority and approval invalidation

## Normal, boundary, failure, and adversarial cases

## Evidence, audit, fallback, and manual route

## Tool options

## Decision, reason, and evidence that could change it
'@ | Set-Content -LiteralPath $transferPath -Encoding utf8
    Write-Host "CREATED $transferPath"
}
notepad $transferPath
```

Without copying the capstone nouns, complete every supplied heading:

1. process start, end, owner, user, reviewer, input, output, and fallback;
2. observations, assumptions, decisions, and unresolved questions;
3. authoritative fields and missing-data behavior;
4. at least three deterministic rules with exact boundary examples;
5. what AI may contribute, or a justified `NO AI` decision;
6. what only a human may decide;
7. normal, boundary, failure, and adversarial cases;
8. source evidence, approval, invalidation, audit, and manual route;
9. existing-tool, configured workflow, custom-code, and no-build options;
10. one final `CONTINUE WITH SYNTHETIC PROOF`, `DISCOVER FURTHER`, `REWORK`, or
    `DO NOT CONTINUE` decision with evidence that could change it.

The final decision is not graded by positivity. It is graded by evidence,
boundaries, alternatives, and safe handling of uncertainty. Lock the completed
record and create the separate answer-free retention task card:

```powershell
$transferHashPath = Join-Path $moduleFolder 'unseen_second_domain_transfer.sha256'
$transferLockPath = Join-Path $moduleFolder 'unseen_second_domain_transfer_lock.json'
$retentionTaskCardPath = Join-Path $moduleFolder 'retention_task_card.md'
$currentTransferHash = (
    Get-FileHash -LiteralPath $transferPath -Algorithm SHA256
).Hash
if (Test-Path -LiteralPath $transferHashPath) {
    $lockedTransferHash = (
        Get-Content -Raw -LiteralPath $transferHashPath
    ).Trim()
    if ($lockedTransferHash -cne $currentTransferHash) {
        throw 'The locked unseen transfer changed. Preserve it and write only a separate reassessment.'
    }
    Write-Host 'PASS: existing unseen-transfer lock still matches'
} else {
    $currentTransferHash |
        Set-Content -LiteralPath $transferHashPath -Encoding ascii
    Write-Host 'CREATED: unseen-transfer lock'
}

if (Test-Path -LiteralPath $transferLockPath) {
    if (-not (Test-Path -LiteralPath $transferLockPath -PathType Leaf)) {
        throw 'The transfer timing lock is not a file. Preserve it and stop.'
    }
    $transferLock = Get-Content -Raw -LiteralPath $transferLockPath |
        ConvertFrom-Json
    if ($transferLock.lock_schema -cne 'course1-transfer-lock-v1') {
        throw 'The transfer timing lock schema is unfamiliar. Preserve it and stop.'
    }
    $null = [DateTimeOffset]::Parse($transferLock.locked_at_utc)
    if ($transferLock.transfer_sha256 -cne $currentTransferHash) {
        throw 'The machine-dated transfer lock does not match the transfer. Preserve both and stop.'
    }
    if (-not (Test-Path -LiteralPath $retentionTaskCardPath -PathType Leaf)) {
        throw 'The locked retention task card is missing. Preserve the lock and stop.'
    }
    $currentTaskCardHash = (
        Get-FileHash -LiteralPath $retentionTaskCardPath -Algorithm SHA256
    ).Hash
    if ($transferLock.retention_task_card_sha256 -cne $currentTaskCardHash) {
        throw 'The retention task card changed after locking. Preserve it and stop.'
    }
    Write-Host 'PASS: existing machine-dated transfer lock and task card match'
} else {
    if (Test-Path -LiteralPath $retentionTaskCardPath) {
        throw 'An unlocked retention task card already exists. Preserve it and stop.'
    }
    $lockedAtUtc = [DateTimeOffset]::UtcNow
    $retentionTaskCardTemplate = @'
# Delayed retention task card

This card was created and locked when the unseen transfer was completed. It
contains the task only—no worked answer.

Machine lock time (UTC): __LOCKED_AT_UTC__
Eligible from (UTC): __DUE_START_UTC__
Eligible until, exclusive (UTC): __DUE_END_UTC__

On or after the eligible-from time and before the eligible-until time:

1. Do not open Module 9, Module 4, worked examples, or earlier written answers.
2. Open only this card and the machine lock named below.
3. Run the PowerShell block below. It verifies the unchanged locks, calculates
   elapsed time from the machine timestamps, and creates the record once.
4. Complete the explanation from memory, then run the named learner-authored
   rule tests. Record all help, errors, and uncertainty honestly.
5. An independent assessor assigns the final retention result.

If you already opened worked answers or a lesson containing the answer, record
`WORKED ANSWERS OPENED BEFORE CHECK: YES`. The attempt may still identify what
to restudy, but it is not clean delayed-retention evidence.

~~~powershell
$moduleFolder = '__MODULE_FOLDER__'
$projectRoot = '__PROJECT_ROOT__'
$transferPath = Join-Path $moduleFolder 'unseen_second_domain_transfer.md'
$transferLockPath = Join-Path $moduleFolder 'unseen_second_domain_transfer_lock.json'
$taskCardPath = Join-Path $moduleFolder 'retention_task_card.md'
$transferLock = Get-Content -Raw -LiteralPath $transferLockPath |
    ConvertFrom-Json
if ($transferLock.lock_schema -cne 'course1-transfer-lock-v1') {
    throw 'STOP: unfamiliar timing-lock schema.'
}
$transferHash = (Get-FileHash -LiteralPath $transferPath -Algorithm SHA256).Hash
$taskCardHash = (Get-FileHash -LiteralPath $taskCardPath -Algorithm SHA256).Hash
if ($transferHash -cne $transferLock.transfer_sha256 -or
    $taskCardHash -cne $transferLock.retention_task_card_sha256) {
    throw 'STOP: transfer or task-card hash does not match its lock.'
}
$lockedAt = [DateTimeOffset]::Parse($transferLock.locked_at_utc)
$checkedAt = [DateTimeOffset]::UtcNow
$elapsedTotalDays = ($checkedAt - $lockedAt).TotalDays
if ($elapsedTotalDays -lt 0) {
    throw 'STOP: the current clock is earlier than the machine lock.'
}
$elapsedWholeDays = [math]::Floor($elapsedTotalDays)
$dueStart = $lockedAt.AddDays(7)
$dueEndExclusive = $lockedAt.AddDays(15)
if ($checkedAt -lt $dueStart) {
    throw "PENDING: no record was created. Return at or after $($dueStart.ToString('o')) UTC."
}
$windowStatus = if ($checkedAt -lt $dueEndExclusive) {
    'ELIGIBLE'
} else {
    'MISSED'
}
$retentionPath = Join-Path $moduleFolder 'delayed_retention_record.md'
if (Test-Path -LiteralPath $retentionPath) {
    if (-not (Test-Path -LiteralPath $retentionPath -PathType Leaf) -or
        (Get-Content -LiteralPath $retentionPath -TotalCount 1) -cne '# Delayed retention record') {
        throw 'Existing delayed-retention record is unfamiliar. Preserve it and stop.'
    }
    Write-Host "KEEPING existing $retentionPath"
} else {
    @"
# Delayed retention record

Machine transfer-lock time (UTC): $($lockedAt.ToString('o'))
Machine retention-check time (UTC): $($checkedAt.ToString('o'))
Calculated elapsed total days: $([math]::Round($elapsedTotalDays, 6))
Calculated elapsed whole days: $elapsedWholeDays
Eligible from (UTC): $($dueStart.ToString('o'))
Eligible until, exclusive (UTC): $($dueEndExclusive.ToString('o'))
RETENTION WINDOW STATUS: $windowStatus
WORKED ANSWERS OPENED BEFORE CHECK: YES / NO

## Retained explanation

## Evidence versus assumption example

## Safe stop, fallback, and approval invalidation

## Fresh learner-rule test result

## Help, re-study, errors, and uncertainty

## Independent assessor result

DELAYED RETENTION: PENDING / PASS / PARTIAL / NOT YET
"@ | Set-Content -LiteralPath $retentionPath -Encoding utf8
    Write-Host "CREATED $retentionPath"
}
notepad $retentionPath
~~~

After writing the memory explanations, run the learner-authored Module 4 tests
from their known evidence folder without opening the lesson:

~~~powershell
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
$moduleFourFolder = Join-Path $projectRoot 'evidence\module-04'
Set-Location -LiteralPath $moduleFourFolder
& $pythonExe -m unittest -v test_learner_stock_rule.py
~~~
'@
    $retentionTaskCard = $retentionTaskCardTemplate
    $retentionTaskCard = $retentionTaskCard.Replace(
        '__LOCKED_AT_UTC__', $lockedAtUtc.ToString('o')
    )
    $retentionTaskCard = $retentionTaskCard.Replace(
        '__DUE_START_UTC__', $lockedAtUtc.AddDays(7).ToString('o')
    )
    $retentionTaskCard = $retentionTaskCard.Replace(
        '__DUE_END_UTC__', $lockedAtUtc.AddDays(15).ToString('o')
    )
    $retentionTaskCard = $retentionTaskCard.Replace(
        '__MODULE_FOLDER__', $moduleFolder.Replace("'", "''")
    )
    $retentionTaskCard = $retentionTaskCard.Replace(
        '__PROJECT_ROOT__', $projectRoot.Replace("'", "''")
    )
    $retentionTaskCard |
        Set-Content -LiteralPath $retentionTaskCardPath -Encoding utf8
    $taskCardHash = (
        Get-FileHash -LiteralPath $retentionTaskCardPath -Algorithm SHA256
    ).Hash
    [ordered]@{
        lock_schema = 'course1-transfer-lock-v1'
        locked_at_utc = $lockedAtUtc.ToString('o')
        transfer_sha256 = $currentTransferHash
        retention_task_card_sha256 = $taskCardHash
    } | ConvertTo-Json |
        Set-Content -LiteralPath $transferLockPath -Encoding utf8
    Write-Host 'CREATED: machine-dated transfer lock and answer-free retention task card'
}
$transferLock = Get-Content -Raw -LiteralPath $transferLockPath |
    ConvertFrom-Json
"Transfer SHA-256: $currentTransferHash"
"Locked at UTC: $($transferLock.locked_at_utc)"
"Retention due from UTC: $(([DateTimeOffset]::Parse($transferLock.locked_at_utc)).AddDays(7).ToString('o'))"
"Retention due until, exclusive UTC: $(([DateTimeOffset]::Parse($transferLock.locked_at_utc)).AddDays(15).ToString('o'))"
```

Any later correction must be a separate
`unseen_transfer_reassessment.md` that cites the original hash.

### Recreation 7 — Complete delayed retention when it becomes due

Wait until the machine-dated window printed at the end of Recreation 6. Close
this lesson now. When the window opens, use only
`retention_task_card.md`; it contains the answer-free task and the exact
commands that validate the locks, calculate elapsed time, and create
`delayed_retention_record.md`. Do not manually enter or change a date.

If you reopened this lesson or a worked answer before completing the memory
task, record `WORKED ANSWERS OPENED BEFORE CHECK: YES`. Do not hide the access
or claim clean retention. If you run the task-card block too early, it creates
nothing and stops with the exact eligible time. If the 7–14-day window is missed,
the machine-created record says `RETENTION WINDOW STATUS: MISSED`; an assessor
cannot turn that attempt into a clean pass, and must set the smallest new
delayed interval needed.

Record:

- the machine-created lock time, check time, and calculated elapsed days;
- `WORKED ANSWERS OPENED BEFORE CHECK: YES` or `NO`;
- your explanation of rule versus optional AI versus human authority;
- one example separating evidence from assumption;
- safe stop, manual fallback, and approval invalidation in your own words;
- the result of locating and rerunning your Module 4 learner-authored rule tests
  from the answer-free task card;
- help, re-study, errors, and remaining uncertainty;
- `DELAYED RETENTION: PASS`, `PARTIAL`, or `NOT YET`, assigned by the
  independent assessor.

Course competence remains `ASSESSMENT PENDING` until an eligible machine-dated
check is complete and independently assessed.

### Recreation 8 — Prepare the mandatory independent Course 1 assessment

Open the fictional assessor example and the authoritative rubric:

```powershell
notepad (Join-Path $courseRoot 'worked_examples\module_09_assessment_record.md')
notepad (Join-Path $courseRoot 'ASSESSMENT_AND_RUBRIC.md')
```

The example demonstrates assessor evidence; it is not a score for you to copy.
Create three separate records:

```powershell
Start-NewPracticeTextFile -Path .\learner_self_reflection.md
Start-NewPracticeTextFile -Path .\recreated_course_assessment.md
Start-NewPracticeTextFile -Path .\oral_assessment_record.md
notepad .\learner_self_reflection.md
notepad .\recreated_course_assessment.md
notepad .\oral_assessment_record.md
```

In `learner_self_reflection.md`, record confidence, difficulty, help, time,
fatigue, strengths, and suspected gaps. You may propose levels here, but label
them `LEARNER VIEW — NOT AN ASSESSOR SCORE`.

In `recreated_course_assessment.md`, prepare these sections:

1. `Assessment identity and synthetic boundary`;
2. `Artifact readiness evidence index`;
3. `Pass prerequisites`;
4. `Calibration record — assessor only`;
5. `Six-area rubric — assessor only`;
6. `Objective calculation — assessor only`;
7. `Transfer and delayed retention result — assessor only`;
8. `Independent oral result — assessor only`;
9. `Assessment result and limitations — assessor only`.

You may populate evidence paths and the synthetic boundary. Do not enter your
own official levels, points, assessor decision, or oral result.

Create the two blank calibration records. Their classifications must be
completed independently before either assessor sees the other's record or any
learner result:

```powershell
foreach ($slot in 'A','B') {
    $calibrationPath = Join-Path $moduleFolder (
        "calibration_assessor_$($slot.ToLower()).md"
    )
    $expectedHeader = "# Independent calibration record $slot"
    if (Test-Path -LiteralPath $calibrationPath) {
        if (-not (Test-Path -LiteralPath $calibrationPath -PathType Leaf) -or
            (Get-Content -LiteralPath $calibrationPath -TotalCount 1) -cne $expectedHeader) {
            throw "Calibration path is unfamiliar. Preserve it and stop: $calibrationPath"
        }
        Write-Host "KEEPING existing calibration record $slot"
    } else {
        @"
$expectedHeader

Assessor code:
Role:
Date:
Conflict/help declaration:
Learner evidence opened before classification: NO
Other assessor record viewed before classification: NO

Case Cedar classification and reason:
Case Harbor classification and reason:
Case Linden classification and reason:
Case Maple classification and reason:
Automatic failure/rework boundary:
Pass versus NOT YET boundary:

ASSESSOR CALIBRATION CLASSIFICATIONS RECORDED: NO
"@ | Set-Content -LiteralPath $calibrationPath -Encoding utf8
        Write-Host "CREATED calibration record $slot"
    }
}
```

Give assessor A only `calibration_assessor_a.md`,
[Assessor Calibration Cases](../ASSESSOR_CALIBRATION_CASES.md), and the
performance-level definitions in
`ASSESSMENT_AND_RUBRIC.md`. Do not give them
`ASSESSOR_CALIBRATION_KEY.md`. They complete the record without opening your
evidence, without seeing assessor B's file, and change the final marker to
`YES`. After they close it, lock it. Then repeat separately for assessor B:

```powershell
function Lock-IndependentCalibrationRecord {
    param([Parameter(Mandatory)][string]$RecordPath)
    if (-not (Test-Path -LiteralPath $RecordPath -PathType Leaf)) {
        throw "Calibration record is missing: $RecordPath"
    }
    $recordText = Get-Content -Raw -LiteralPath $RecordPath
    if (-not $recordText.Contains(
        'ASSESSOR CALIBRATION CLASSIFICATIONS RECORDED: YES'
    )) {
        throw "Assessor has not marked the calibration record complete: $RecordPath"
    }
    $currentHash = (
        Get-FileHash -LiteralPath $RecordPath -Algorithm SHA256
    ).Hash
    $lockPath = "$RecordPath.sha256"
    if (Test-Path -LiteralPath $lockPath) {
        $lockedHash = (Get-Content -Raw -LiteralPath $lockPath).Trim()
        if ($lockedHash -cne $currentHash) {
            throw "Locked calibration record changed. Preserve it and stop: $RecordPath"
        }
        Write-Host "PASS: existing calibration lock matches $RecordPath"
    } else {
        $currentHash | Set-Content -LiteralPath $lockPath -Encoding ascii
        Write-Host "LOCKED calibration record: $RecordPath"
    }
    return $currentHash
}

$calibrationA = Join-Path $moduleFolder 'calibration_assessor_a.md'
$calibrationB = Join-Path $moduleFolder 'calibration_assessor_b.md'

# Run this line only after assessor A completed and closed their record.
Lock-IndependentCalibrationRecord -RecordPath $calibrationA

# Run this line only after assessor B independently completed and closed theirs.
Lock-IndependentCalibrationRecord -RecordPath $calibrationB
```

Only after both locks exist may the assessors compare classifications. They
complete a separate resolution record:

```powershell
$calibrationResolution = Join-Path $moduleFolder 'calibration_resolution.md'
if (Test-Path -LiteralPath $calibrationResolution) {
    if (-not (Test-Path -LiteralPath $calibrationResolution -PathType Leaf) -or
        (Get-Content -LiteralPath $calibrationResolution -TotalCount 1) -cne '# Calibration resolution') {
        throw 'Calibration resolution is unfamiliar. Preserve it and stop.'
    }
    Write-Host 'KEEPING existing calibration resolution'
} else {
    @'
# Calibration resolution

Assessor A code:
Assessor A locked SHA-256:
Assessor B code:
Assessor B locked SHA-256:
Compared only after both locks existed: YES / NO
Case-level agreement or exact disagreement:
Resolution against the written anchor:
Automatic failure/rework agreement:
Pass versus NOT YET agreement:
ASSESSOR CALIBRATION: PENDING / PASS / NOT YET
'@ | Set-Content -LiteralPath $calibrationResolution -Encoding utf8
    Write-Host 'CREATED calibration resolution'
}
notepad $calibrationResolution
```

Only now open the
[Assessor Calibration Key](../ASSESSOR_CALIBRATION_KEY.md). The assessors cite
both hashes, compare every case with the fixed key, record exact agreement or
the evidence-based resolution, and end with `ASSESSOR CALIBRATION: PASS` or
`NOT YET`. Never edit either locked original. If assessor B is unavailable, do
not invent their record or result; leave the resolution `PENDING`.

At least two independent assessors who did not create, edit, or correct your
evidence first classify the four shuffled cases without the key. Each records
an identity code, role, date, conflict/help declaration, and classifications
before discussion. They must match the fixed key and agree exactly on
automatic failure/rework and pass versus `NOT YET`. If a second assessor is
unavailable, record `ASSESSOR CALIBRATION: PENDING`; you may continue
practicing, but Course 1 competence remains pending.

After calibration passes, one calibrated independent artifact assessor records
every prerequisite and six official levels with evidence. The assessor uses
this table:

```markdown
| Area | Weight | Assessor level (1-4) | Points = weight x level / 4 | Evidence, cap, and reason |
|---|---:|---:|---:|---|
| Process discovery and opportunity selection | 20 | | | |
| Data quality and deterministic controls | 20 | | | |
| Bounded AI and evidence | 15 | | | |
| Human control and failure behaviour | 15 | | | |
| Dutch SME risk and tool-fit screen | 15 | | | |
| Evaluation, adoption, and handover | 15 | | | |
```

After the assessor enters the six levels, replace the six example `3` values
below with those assessor values. This checks arithmetic; it does not create a
score:

```powershell
$assessorLevels = @(3,3,3,3,3,3)
$weights = @(20,20,15,15,15,15)
if ($assessorLevels.Count -ne 6) { throw 'Enter exactly six assessor levels.' }
if (@($assessorLevels | Where-Object { $_ -notin 1,2,3,4 }).Count -ne 0) {
    throw 'Every assessor level must be a whole number from 1 through 4.'
}
$areaPoints = for ($index = 0; $index -lt 6; $index++) {
    $weights[$index] * $assessorLevels[$index] / 4
}
$total = ($areaPoints | Measure-Object -Sum).Sum
[PSCustomObject]@{
    levels = $assessorLevels -join ','
    points = $areaPoints -join ','
    total = $total
    every_area_competent = (
        @($assessorLevels | Where-Object { $_ -lt 3 }).Count -eq 0
    )
    score_gate_pass = ($total -ge 75)
}
```

All ten oral questions are asked by the independent oral assessor one at a
time, without showing prepared answers. The assessor also asks at least three
evidence-based follow-ups, including at least one follow-up on an answer that
is weak, vague, or unsupported by the named evidence. The learner may say
`I do not know`, but must then name a safe next step such as checking the
authoritative artifact, stopping the workflow, asking the responsible owner,
or recording the uncertainty for investigation. Inventing an answer does not
pass. The assessor—not the learner—completes
`oral_assessment_record.md` with
`SUPPORTED`, `PARTIAL`, or `UNSUPPORTED`, evidence, and reason for each answer.
If no independent person observed it, record
`LEARNER ORAL COMPETENCE: SELF-ATTESTED ONLY` and
`COURSE 1 COMPETENCE: ASSESSMENT PENDING`.

### Recreation 9 — Complete the honest case and five-minute demonstration

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

Create `recreated_dutch_explanation.md` for a two-minute plain-Dutch
explanation. It must cover the fictional problem and synthetic boundary,
rules/optional AI/human authority, one failure and fallback, evidence,
limitations, and the next safe discovery or escalation step. Start with
`DUTCH CLIENT COMMUNICATION: REHEARSAL — NOT CLIENT-READY`.

A Dutch-speaking reviewer who did not write the text records questions, unclear
jargon, overclaims, and whether you corrected a misunderstanding. If no
reviewer is available, record `DUTCH-SPEAKING REVIEWER: UNVERIFIED`; do not
claim demonstrated client communication.

Create or safely resume all three files:

```powershell
$portfolioCreated = Start-NewPracticeTextFile -Path .\recreated_portfolio_case.md
$demoCreated = Start-NewPracticeTextFile -Path .\recreated_demo_script.md
$dutchExplanationCreated = Start-NewPracticeTextFile -Path .\recreated_dutch_explanation.md
notepad .\recreated_portfolio_case.md
notepad .\recreated_demo_script.md
notepad .\recreated_dutch_explanation.md
```

For each file, write the instructed content only when the helper printed
`CREATED`. When it printed `SKIP CREATE`, continue only genuinely incomplete
content and never paste a fresh replacement over a completed file.

Verify:

```powershell
Select-String -Path .\recreated_acceptance_rehearsal.md -Pattern 'TECH-01','TECH-09','Given','When','Then','failed_manual','TECH-D01','retest','EXTERNAL UAT NOT VERIFIED'
Select-String -Path .\recreated_handover.md -Pattern 'fallback','rollback','restore','incident','limitation','owner'
Select-String -Path .\recreated_operator_rehearsal.md -Pattern 'OAR-OP-01','OAR-OP-06','EXTERNAL UAT NOT VERIFIED','fallback'
Select-String -Path .\recreated_final_decision.md -Pattern 'PROVISIONAL PRE-UAT','FINAL POST-REHEARSAL','TECH-D01','synthetic'
Select-String -Path .\unseen_second_domain_transfer.md -Pattern 'authoritative','deterministic','human','fallback','decision'
Select-String -Path .\unseen_second_domain_transfer_lock.json -Pattern 'locked_at_utc','transfer_sha256','retention_task_card_sha256'
Select-String -Path .\retention_task_card.md -Pattern 'Delayed retention task card','Eligible from','Eligible until'
Select-String -Path .\delayed_retention_record.md -Pattern 'Machine transfer-lock time','Calculated elapsed whole days','RETENTION WINDOW STATUS','DELAYED RETENTION','WORKED ANSWERS OPENED BEFORE CHECK'
Select-String -Path .\recreated_course_assessment.md -Pattern 'Artifact readiness evidence index','Six-area rubric — assessor only','Assessment result and limitations — assessor only'
Select-String -Path .\oral_assessment_record.md -Pattern 'LEARNER ORAL COMPETENCE'
Select-String -Path .\recreated_portfolio_case.md -Pattern 'synthetic','not production','Course 1'
Select-String -Path .\recreated_dutch_explanation.md -Pattern 'DUTCH CLIENT COMMUNICATION','synthet','mens','fallback','niet'
```

**Expected result:** every search term appears in the relevant evidence.
Missing terms identify work to finish; they are not permission to weaken
acceptance.

### Recreation 10 — Assemble the single capstone repository

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
1. `LEARNER ARTIFACTS: READY FOR ASSESSMENT` or
   `LEARNER ARTIFACTS: NOT YET`;
2. checks for: nine distinct technical regression scenarios TECH-01 through
   TECH-09 executed as role-simulated rehearsal; exact isolated command
   evidence, expected state/error, attempt records, numbered retry preservation,
   immutable failure history, TECH-D01 rejection/correction/retest, and
   EXTERNAL_ACTIONS_ENABLED=false;
3. checks for OAR-OP-01 through OAR-OP-06 actually performed with observed
   evidence, help/defects, fallback, and `EXTERNAL UAT NOT VERIFIED`; report
   `REAL SYNTHETIC UAT: VERIFIED` only if a separate consenting-participant
   record actually supports it;
4. role-specific training, feedback/support, normal and safe-failure runbook,
   fallback, rollback, backup/restore, monitoring, owners, limitations, and
   residual risks;
5. the preserved PROVISIONAL PRE-UAT recommendation and a reassessed
   `FINAL POST-REHEARSAL` decision, or conditional `FINAL POST-UAT` only with
   real synthetic UAT evidence; exactly one supported workflow decision;
6. unseen_second_domain_transfer.md covers boundary, authority, rules,
   optional AI or NO AI, human decisions, failure, evidence, approval, tool
   options, and a supported multi-outcome decision; its SHA-256 lock matches;
   unseen_second_domain_transfer_lock.json has an immutable machine
   locked_at_utc and matching transfer/task-card hashes;
7. retention_task_card.md matches its locked hash and contains an answer-free
   route; delayed_retention_record.md uses machine lock/check timestamps,
   calculates elapsed total and whole days, falls inside the 7–14-day window,
   records answer access, retained concepts, bounded task result, help, and
   assessor status;
8. learner_self_reflection.md is separate from
   recreated_course_assessment.md; official prerequisite, calibration, rubric,
   points, retention, oral, and competence fields are assigned only by the two
   calibration assessors and the relevant independent artifact/oral assessor;
   calibration_assessor_a.md and calibration_assessor_b.md each match their
   create-once SHA-256 lock, and calibration_resolution.md cites both;
   oral_assessment_record.md records ten one-at-a-time
   questions and at least three follow-ups, or honestly says SELF-ATTESTED ONLY
   and ASSESSMENT PENDING;
9. the rubric result remains separate from the prototype decision;
   recreated_dutch_explanation.md covers boundary, rules/optional AI/human,
   failure/fallback, evidence, limitations, next safe step, and reviewer status;
   CAPSTONE_INDEX.md maps setup and Modules 1-9; CHANGELOG.md records the
   closeout; no claim of client savings, real discovery, external UAT,
   production readiness, client-ready communication, or consultant
   certification;
10. the smallest learner-made corrections if artifacts are NOT YET.

Remain read-only. Do not run project code, workflows, or tests, assign or
change rubric levels, verify speech you did not observe, supply missing oral
answers, or complete the handover/acceptance work. Artifact readiness is not a
competence pass.
```

## Pass criteria

- [ ] Worked operational-acceptance/handover and tabletop rehearsal are
      complete and labelled as synthetic role simulation.
- [ ] Stage 1 checks the safe path length, exact `COURSE_PROJECT.md` marker,
      and resolved Git root before any lesson write or runner execution.
- [ ] TECH-01 through TECH-09 were actually executed in isolated folders and
      each record has Given/When/Then, expected state/error, observed evidence,
      result, and exact relative path.
- [ ] Every scenario and TECH-D01 has `attempt-info.json`; any unexpectedly
      interrupted or unexpectedly failed attempt remains unchanged, and its
      rerun uses and records the next numbered retry folder. Clean first
      attempts require no numbered retry.
- [ ] Solo testing says `EXTERNAL UAT NOT VERIFIED`; no real-user claim is
      made unless another consenting person actually tested synthetic data.
- [ ] OAR-OP-01 through OAR-OP-06 were actually performed; issue location,
      source/rule tracing, output understanding, approve/edit/reject reasoning,
      safe-failure recognition, and manual fallback have observed evidence.
- [ ] Failures, review choices, hash invalidation, and fallback are tested.
- [ ] TECH-03, TECH-06, TECH-08, and TECH-09 each verify
      `failures/latest.json`, the expected `error_code`, the immutable
      `failures/aNNNN.json` followed from `history_path`, and matching hashes.
- [ ] TECH-D01 records the unsafe wording rejection, correction, and retest;
      any other defects are recorded and retested rather than hidden.
- [ ] Training is role-specific and demonstrated.
- [ ] Runbook covers normal run, stop, fallback, rollback, restore, and
      escalation.
- [ ] Handover assigns every continuing responsibility.
- [ ] The Module 8 `PROVISIONAL PRE-UAT` recommendation is preserved.
- [ ] The copied decision is reassessed using technical rehearsal,
      operator-task, defect/retest, adoption, and handover evidence and marked
      `FINAL POST-REHEARSAL`; `FINAL POST-UAT` appears only when separate real
      synthetic UAT evidence exists.
- [ ] The exact final decision is `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`,
      or `DO NOT CONTINUE`, and its evidence supports it.
- [ ] The matching accept, corrective, or safe-closure path is complete.
- [ ] Portfolio, incomplete case, or lessons-learned closure states evidence
      and limitations honestly.
- [ ] The locked unseen second-domain transfer passes independent assessment
      without copying the capstone nouns or receiving an answer key.
- [ ] The unseen transfer has an immutable JSON machine-time lock whose
      transfer and answer-free task-card hashes match.
- [ ] The delayed-retention record was machine-created inside the 7–14-day
      window, shows the calculated elapsed interval and honest answer-access
      statement, and has an independent result.
- [ ] Learner self-reflection is separate and cannot populate official scores.
- [ ] At least two independent assessors classified the fixed anchors before
      opening my result, recorded their decisions separately, and reached the
      required calibration agreement; otherwise competence remains pending.
- [ ] Both original calibration records match their separate SHA-256 locks,
      and the resolution record cites both hashes without rewriting either
      assessor's original classifications.
- [ ] Every assessment prerequisite is independently marked `PASS` with an
      evidence path.
- [ ] A calibrated independent artifact assessor assigns all six official
      whole-number levels; every area is at least 3, the total is at least 75,
      and the calculation is saved.
- [ ] An independent oral assessor verifies all ten one-at-a-time answers and
      at least three follow-ups without a prepared or generated script.
- [ ] The two-minute Dutch explanation is bounded and either has a
      Dutch-speaking reviewer record or remains explicitly `UNVERIFIED`; it
      never claims client readiness.
- [ ] The rubric result and final prototype decision remain separate.
- [ ] Root `CAPSTONE_INDEX.md` maps setup and all nine modules.
- [ ] Root `CHANGELOG.md` records the dated decision and limitations.
- [ ] The read-only review records the learner's synthetic-data statement as
      an attestation rather than proof and says non-detection is not proof of
      absence.
- [ ] Codex returns `LEARNER ARTIFACTS: READY FOR ASSESSMENT` read-only; this is
      not treated as the competence decision.

### Record the final Course 1 PASS in Git

Do this only after Codex reports artifact readiness and the independent artifact
and oral assessment records say `COURSE 1 COMPETENCE: PASS`. Rerun the complete
Stage 1 block first,
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

A synthetic implementation exercise is not finished when code runs. It is
finished when the learner can perform the defined operator tasks, owners and
responsibilities are explicit, failures have a route, evidence supports the
decision, and another person has a candidate script for later real UAT.

## Capstone increment

The Course 1 capstone is complete as an evidence-controlled synthetic project
with executable role-simulated technical and operator rehearsal, a candidate
UAT script, defect/retest, adoption plan, runbook, handover, reassessed final
decision, unseen transfer, delayed-retention result, independent six-area
rubric, independently observed oral answers, and an honest case or closure
record.

## Required artifact

The teaching contract creates the worked pack, candidate UAT script,
role-simulated technical/operator evidence, defect/retest, adoption, handover,
final decision, transfer and retention records, learner reflection, independent
Course 1 assessment, two locked assessor-calibration records and their
resolution, oral record, portfolio or closure, and demo evidence under
`evidence/module-09`, plus root `CAPSTONE_INDEX.md` and `CHANGELOG.md`.

## Test gate

The **Pass criteria** are the complete Course 1 gate.

## Stop or rework

Stop if acceptance rehearsal is vague or only imagined, solo evidence is called
real UAT, defects are hidden, owners are placeholders, fallback was not
rehearsed, an action can escape, real data appears, a weak rubric area is
averaged away, oral competence is self-awarded, or synthetic evidence is
presented as client proof.

## Common failures

- Asking whether users “like it” instead of testing tasks.
- Training features instead of roles and decisions.
- Handing over code without operation and incident ownership.
- Treating role simulation as independent acceptance.
- Giving yourself official rubric levels or treating self-attested speech as
  verified oral competence.
- Calling Course 1 completion professional certification.

## Estimated time

16–22 hours of active work plus the later 7–14-day retention check, best
completed as 18–26 focused study blocks of 45–60 minutes. This is an **AUTHOR
ESTIMATE — NOT BEGINNER MEASURED**.
