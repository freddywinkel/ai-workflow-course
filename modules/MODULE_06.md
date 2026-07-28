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
$runnerHashRecord = Join-Path (Join-Path $projectRoot 'evidence\module-04') 'reference_runner_hashes.json'
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
if (-not (Test-Path -LiteralPath (Join-Path $courseRoot 'course1_capstone\tests'))) {
    throw 'That course folder does not contain the Course 1 tests.'
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
function Read-CourseRunState {
    param([string]$RunDir)
    $statePath = Join-Path $RunDir 'state.json'
    if (-not (Test-Path -LiteralPath $statePath -PathType Leaf)) {
        throw "Controlled run state is missing: $statePath"
    }
    try {
        $state = Get-Content -Raw -LiteralPath $statePath | ConvertFrom-Json
    } catch {
        throw "Controlled run state is not recognisable JSON: $statePath"
    }
    if ($state.run_id -cnotmatch '^RUN-[A-F0-9]{12}$' -or
        -not ($state.draft_revision -is [int] -or $state.draft_revision -is [long]) -or
        [string]::IsNullOrWhiteSpace([string]$state.current_state)) {
        throw "Controlled run state has an unfamiliar contract: $statePath"
    }
    return $state
}
function Get-OrCreateCourseFailureRun {
    param([string]$Workspace)
    $runDir = Resolve-SavedCourseRun $Workspace
    if ($null -ne $runDir) {
        Write-Host "RESUME: keeping the validated failure-lab run $runDir"
        return $runDir
    }
    & $pythonExe $runner prepare `
        --input $learnerWorkedInput `
        --expected $learnerWorkedExpected `
        --workspace $Workspace `
        --ai-mode mock `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw "Failure-lab preparation safely stopped: $Workspace"
    }
    $runDir = Resolve-SavedCourseRun $Workspace
    if ($null -eq $runDir) {
        throw "Failure-lab preparation did not create a validated run: $Workspace"
    }
    return $runDir
}
function Get-CourseHashInventory {
    param([string]$Root)
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
        throw "Controlled source run is missing or is not a folder: $Root"
    }
    $resolvedRoot = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\')
    return @(
        Get-ChildItem -LiteralPath $resolvedRoot -Recurse -File |
            ForEach-Object {
                [PSCustomObject]@{
                    path = $_.FullName.Substring($resolvedRoot.Length).TrimStart('\').Replace('\','/')
                    sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
                }
            } |
            Sort-Object path
    )
}
function Copy-CourseDecisionRunOnce {
    param(
        [string]$SourceRun,
        [string]$DestinationRun,
        [string]$CopyRecord,
        [string[]]$ImmutableRelativePaths
    )
    $sourceRunLeaf = Split-Path -Leaf $SourceRun
    $destinationRunLeaf = Split-Path -Leaf $DestinationRun
    if ($sourceRunLeaf -cnotmatch '^RUN-[A-F0-9]{12}$' -or
        $destinationRunLeaf -cne $sourceRunLeaf) {
        throw 'A decision-run copy must keep the exact protected RUN identifier as its folder name.'
    }
    $destinationParent = Split-Path -Parent $DestinationRun
    if ((Test-Path -LiteralPath $destinationParent) -and
        -not (Test-Path -LiteralPath $destinationParent -PathType Container)) {
        throw "Decision-run parent exists but is not a folder: $destinationParent"
    }
    $sourceFiles = Get-CourseHashInventory $SourceRun
    if (Test-Path -LiteralPath $DestinationRun) {
        if (-not (Test-Path -LiteralPath $DestinationRun -PathType Container)) {
            throw "Decision-run destination exists but is not a folder: $DestinationRun"
        }
        if ((Test-Path -LiteralPath $CopyRecord) -and
            -not (Test-Path -LiteralPath $CopyRecord -PathType Leaf)) {
            throw "Initial-copy record path exists but is not a file: $CopyRecord"
        }
        if (-not (Test-Path -LiteralPath $CopyRecord -PathType Leaf)) {
            $recoveredDestinationFiles = Get-CourseHashInventory $DestinationRun
            $sourceText = $sourceFiles | ConvertTo-Json -Compress -Depth 5
            $destinationText = $recoveredDestinationFiles |
                ConvertTo-Json -Compress -Depth 5
            if ($sourceText -cne $destinationText) {
                throw "Existing decision run has no copy record and is not an exact initial copy. Preserve it and ask for read-only diagnosis: $DestinationRun"
            }
            [PSCustomObject]@{
                schema_version = 1
                source_run_id = $sourceRunLeaf
                destination_run_leaf = $destinationRunLeaf
                source_files = $sourceFiles
                initial_destination_files = $recoveredDestinationFiles
            } | ConvertTo-Json -Depth 6 |
                Set-Content -LiteralPath $CopyRecord -Encoding utf8
            Write-Host "RECOVERED the missing initial-copy record for exact copy $DestinationRun"
        }
        try {
            $savedCopy = Get-Content -Raw -LiteralPath $CopyRecord | ConvertFrom-Json
        } catch {
            throw "Initial-copy record is damaged. Preserve the run and ask for read-only diagnosis: $CopyRecord"
        }
        if ($savedCopy.source_run_id -cne $sourceRunLeaf -or
            $savedCopy.destination_run_leaf -cne $destinationRunLeaf) {
            throw "Initial-copy record does not name this exact protected run. Preserve it and ask for read-only diagnosis: $CopyRecord"
        }
        $savedSourceText = @($savedCopy.source_files) | ConvertTo-Json -Compress -Depth 5
        $savedDestinationText = @($savedCopy.initial_destination_files) |
            ConvertTo-Json -Compress -Depth 5
        $currentSourceText = $sourceFiles | ConvertTo-Json -Compress -Depth 5
        if ($savedSourceText -cne $savedDestinationText -or
            $savedSourceText -cne $currentSourceText) {
            throw "Module 5 source or initial-copy evidence changed. Preserve both runs and ask for read-only diagnosis: $DestinationRun"
        }
        foreach ($relativePath in $ImmutableRelativePaths) {
            $savedFile = @($savedCopy.initial_destination_files | Where-Object {
                $_.path -ceq $relativePath
            })
            $destinationFile = Join-Path $DestinationRun ($relativePath.Replace('/','\'))
            if ($savedFile.Count -ne 1 -or
                -not (Test-Path -LiteralPath $destinationFile -PathType Leaf) -or
                (Get-FileHash -LiteralPath $destinationFile -Algorithm SHA256).Hash -ne
                $savedFile[0].sha256) {
                throw "Immutable copied evidence changed at $relativePath. Preserve the run and ask for read-only diagnosis."
            }
        }
        Write-Host "RESUME: verified source provenance for $DestinationRun"
        return
    }
    if (Test-Path -LiteralPath $CopyRecord) {
        throw "A copy record exists without its decision run. Preserve it and ask for read-only diagnosis: $CopyRecord"
    }
    if (-not (Test-Path -LiteralPath $destinationParent)) {
        New-Item -ItemType Directory -Path $destinationParent | Out-Null
    }
    Copy-Item -LiteralPath $SourceRun -Destination $DestinationRun -Recurse
    $destinationFiles = Get-CourseHashInventory $DestinationRun
    $sourceText = $sourceFiles | ConvertTo-Json -Compress -Depth 5
    $destinationText = $destinationFiles | ConvertTo-Json -Compress -Depth 5
    if ($sourceText -cne $destinationText) {
        throw "New decision-run copy does not match its Module 5 source: $DestinationRun"
    }
    [PSCustomObject]@{
        schema_version = 1
        source_run_id = $sourceRunLeaf
        destination_run_leaf = $destinationRunLeaf
        source_files = $sourceFiles
        initial_destination_files = $destinationFiles
    } | ConvertTo-Json -Depth 6 |
        Set-Content -LiteralPath $CopyRecord -Encoding utf8
    Write-Host "COPIED, VERIFIED, AND RECORDED $DestinationRun"
}
$immutableRunEvidence = @(
    'source/work_items.csv',
    'source/expected_issues.evidence',
    'issues/issues.json',
    'issues/issues.csv',
    'control.json',
    'run_config.json'
)
$workedImmutableEvidence = @(
    $immutableRunEvidence +
    'draft/summary.json' +
    'review/review_package.json' +
    'review/review_manifest.json'
)
$moduleFiveWorkedWorkspace = Join-Path $moduleFive 'worked-mock'
$moduleFiveWorkedRunDir = Resolve-SavedCourseRun $moduleFiveWorkedWorkspace
$workedDecisionParent = Join-Path $moduleFolder 'worked-decision'
if ((Test-Path -LiteralPath $workedDecisionParent) -and
    -not (Test-Path -LiteralPath $workedDecisionParent -PathType Container)) {
    throw 'Module 6 worked-decision parent exists but is not a folder.'
}
$workedRunDir = Join-Path $workedDecisionParent (Split-Path -Leaf $moduleFiveWorkedRunDir)
if ((Test-Path -LiteralPath $workedRunDir) -and
    -not (Test-Path -LiteralPath $workedRunDir -PathType Container)) {
    throw 'Module 6 worked decision path exists but is not a folder.'
}
$workedSupportReviewSource = Join-Path $moduleFive 'worked_support_review.md'
$workedSupportReviewCopy = Join-Path $moduleFolder 'source-m5-worked_support_review.md'
$moduleFiveRecreatedWorkspace = Join-Path $moduleFive 'recreated-mock'
$moduleFiveRecreatedRunDir = Resolve-SavedCourseRun $moduleFiveRecreatedWorkspace
$moduleFiveCandidate = Join-Path $moduleFive 'recreated_candidate_summary.json'
$moduleFiveSupportReview = Join-Path $moduleFive 'recreated_support_review.md'
$recreatedDecisionParent = Join-Path $moduleFolder 'recreated-decision'
if ((Test-Path -LiteralPath $recreatedDecisionParent) -and
    -not (Test-Path -LiteralPath $recreatedDecisionParent -PathType Container)) {
    throw 'Module 6 recreated-decision parent exists but is not a folder.'
}
$recreatedRunDir = Join-Path $recreatedDecisionParent (Split-Path -Leaf $moduleFiveRecreatedRunDir)
if ((Test-Path -LiteralPath $recreatedRunDir) -and
    -not (Test-Path -LiteralPath $recreatedRunDir -PathType Container)) {
    throw 'Module 6 recreated decision path exists but is not a folder.'
}
$candidate = Join-Path $moduleFolder 'recreated_candidate_summary.json'
$recreatedSupportReviewCopy = Join-Path $moduleFolder 'source-m5-recreated_support_review.md'
$reviewR1 = Join-Path $moduleFolder 'recreated_review_r1.md'
$reviewR2 = Join-Path $moduleFolder 'recreated_review_r2.md'
$workedCopyRecord = Join-Path $workedDecisionParent 'initial_copy_hashes.json'
$recreatedCopyRecord = Join-Path $recreatedDecisionParent 'initial_copy_hashes.json'
$workedRunExists = Test-Path -LiteralPath $workedRunDir -PathType Container
$workedRecordExists = Test-Path -LiteralPath $workedCopyRecord
if ($workedRecordExists -and
    -not (Test-Path -LiteralPath $workedCopyRecord -PathType Leaf)) {
    throw 'Worked initial-copy record exists but is not a file.'
}
if ($workedRecordExists -and -not $workedRunExists) {
    throw 'Worked initial-copy record exists without its decision run. Preserve it and ask for read-only diagnosis.'
}
if ($workedRunExists -and $workedRecordExists) {
    Copy-CourseDecisionRunOnce `
        -SourceRun $moduleFiveWorkedRunDir `
        -DestinationRun $workedRunDir `
        -CopyRecord $workedCopyRecord `
        -ImmutableRelativePaths $workedImmutableEvidence
} elseif ($workedRunExists) {
    $workedSourceInventory = Get-CourseHashInventory $moduleFiveWorkedRunDir
    $workedDestinationInventory = Get-CourseHashInventory $workedRunDir
    if (($workedSourceInventory | ConvertTo-Json -Compress -Depth 5) -cne
        ($workedDestinationInventory | ConvertTo-Json -Compress -Depth 5)) {
        throw 'Record-less worked decision run is not an exact initial copy. Preserve it and ask for read-only diagnosis.'
    }
    Write-Host 'RECOVERABLE PARTIAL STAGE: rerun Stage 1 to create the worked initial-copy record.'
}
if (Test-Path -LiteralPath $workedSupportReviewCopy) {
    if (-not (Test-Path -LiteralPath $workedSupportReviewSource -PathType Leaf) -or
        -not (Test-Path -LiteralPath $workedSupportReviewCopy -PathType Leaf)) {
        throw 'Worked support-review source or copy is wrong-type.'
    }
    if ((Get-FileHash -LiteralPath $workedSupportReviewSource -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $workedSupportReviewCopy -Algorithm SHA256).Hash) {
        throw 'Worked support-review copy changed from its Module 5 source.'
    }
} elseif ($workedRunExists -or $workedRecordExists) {
    Write-Host 'RECOVERABLE PARTIAL STAGE: rerun Stage 1 to copy the worked support review.'
}
$recreatedRunExists = Test-Path -LiteralPath $recreatedRunDir -PathType Container
$recreatedRecordExists = Test-Path -LiteralPath $recreatedCopyRecord
if ($recreatedRecordExists -and
    -not (Test-Path -LiteralPath $recreatedCopyRecord -PathType Leaf)) {
    throw 'Recreated initial-copy record exists but is not a file.'
}
if ($recreatedRecordExists -and -not $recreatedRunExists) {
    throw 'Recreated initial-copy record exists without its decision run. Preserve it and ask for read-only diagnosis.'
}
if ($recreatedRunExists -and $recreatedRecordExists) {
    Copy-CourseDecisionRunOnce `
        -SourceRun $moduleFiveRecreatedRunDir `
        -DestinationRun $recreatedRunDir `
        -CopyRecord $recreatedCopyRecord `
        -ImmutableRelativePaths $immutableRunEvidence
} elseif ($recreatedRunExists) {
    $recreatedSourceInventory = Get-CourseHashInventory $moduleFiveRecreatedRunDir
    $recreatedDestinationInventory = Get-CourseHashInventory $recreatedRunDir
    if (($recreatedSourceInventory | ConvertTo-Json -Compress -Depth 5) -cne
        ($recreatedDestinationInventory | ConvertTo-Json -Compress -Depth 5)) {
        throw 'Record-less recreated decision run is not an exact initial copy. Preserve it and ask for read-only diagnosis.'
    }
    Write-Host 'RECOVERABLE PARTIAL STAGE: rerun Recreation 1 to create the recreated initial-copy record.'
}
if (Test-Path -LiteralPath $candidate) {
    if (-not (Test-Path -LiteralPath $moduleFiveCandidate -PathType Leaf) -or
        -not (Test-Path -LiteralPath $candidate -PathType Leaf) -or
        (Get-FileHash -LiteralPath $moduleFiveCandidate -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash) {
        throw 'Recreated candidate copy is wrong-type or changed from its Module 5 source.'
    }
} elseif ($recreatedRunExists -or $recreatedRecordExists) {
    Write-Host 'RECOVERABLE PARTIAL STAGE: rerun Recreation 1 to copy the candidate.'
}
if (Test-Path -LiteralPath $recreatedSupportReviewCopy) {
    if (-not (Test-Path -LiteralPath $moduleFiveSupportReview -PathType Leaf) -or
        -not (Test-Path -LiteralPath $recreatedSupportReviewCopy -PathType Leaf) -or
        (Get-FileHash -LiteralPath $moduleFiveSupportReview -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $recreatedSupportReviewCopy -Algorithm SHA256).Hash) {
        throw 'Recreated support-review copy is wrong-type or changed from its Module 5 source.'
    }
} elseif ($recreatedRunExists -or $recreatedRecordExists -or
    (Test-Path -LiteralPath $candidate)) {
    Write-Host 'RECOVERABLE PARTIAL STAGE: rerun Recreation 1 to copy the support review.'
}
& $pythonExe --version
```

Use `& $pythonExe`, never bare `python`. This start block reconstructs both
Module 5 source runs, both Module 6 decision-run paths, the candidate, support
reviews, and both learner review paths. It reads durable locators and
hash/provenance records, verifies every completed copied component, and labels
a safe partial copy stage for you to finish. It does not create a first copy or
repeat a decision, revision, or export.

Safe stopping points are after the worked export, after the isolated failure
tests, after Recreation 2, and after Recreation 3. On return, rerun this start
block and continue at the next unfinished stage. Do not replay a completed
decision or revision merely to restore variables.

## Follow along — I show you exactly how

### Stage 1 — Open the complete worked review package

Run:

```powershell
Copy-CourseDecisionRunOnce `
    -SourceRun $moduleFiveWorkedRunDir `
    -DestinationRun $workedRunDir `
    -CopyRecord $workedCopyRecord `
    -ImmutableRelativePaths $workedImmutableEvidence
if (-not (Test-Path -LiteralPath $workedSupportReviewSource -PathType Leaf)) {
    throw 'Module 5 worked support review missing.'
}
if (Test-Path -LiteralPath $workedSupportReviewCopy) {
    if (-not (Test-Path -LiteralPath $workedSupportReviewCopy -PathType Leaf) -or
        (Get-FileHash -LiteralPath $workedSupportReviewCopy -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $workedSupportReviewSource -Algorithm SHA256).Hash) {
        throw 'Saved worked support-review copy is wrong-type or differs from its Module 5 source.'
    }
    Write-Host "RESUME: verified $workedSupportReviewCopy"
} else {
    Copy-Item -LiteralPath $workedSupportReviewSource -Destination $workedSupportReviewCopy
    if ((Get-FileHash -LiteralPath $workedSupportReviewCopy -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $workedSupportReviewSource -Algorithm SHA256).Hash) {
        throw 'New worked support-review copy did not match its source.'
    }
}
& $pythonExe $runner status --run-dir $workedRunDir
if ($LASTEXITCODE -ne 0) {
    throw 'Worked copy status validation safely stopped. Do not review or decide from this run.'
}
Get-Content -LiteralPath (Join-Path $workedRunDir 'review\review_package.json')
Get-FileHash -LiteralPath (Join-Path $workedRunDir 'draft\summary.json') -Algorithm SHA256
Get-Content -LiteralPath (Join-Path $workedRunDir 'review\review_manifest.json')
Get-FileHash -LiteralPath (Join-Path $workedRunDir 'review\review_manifest.json') -Algorithm SHA256
```

Before deciding, open:

```powershell
code (Join-Path $workedRunDir 'source\work_items.csv')
code (Join-Path $workedRunDir 'issues\issues.csv')
code (Join-Path $workedRunDir 'draft\summary.json')
code (Join-Path $workedRunDir 'review\review_package.json')
code (Join-Path $workedRunDir 'review\review_manifest.json')
code $workedSupportReviewCopy
```

If `code` is unavailable, use Visual Studio Code **File > Open File**.

Do not continue until you can answer:

1. Which 13 issues exist?
2. Which source row, field, and raw value supports each?
3. Does every sentence visibly cite known issue IDs?
4. Is every action only `human_review`?
5. Are external actions zero?
6. What is the exact draft SHA-256 hash?
7. Which eight protected artifact paths are listed in the review manifest?
8. What is the exact review-manifest SHA-256 hash?

### Stage 2 — Record an exact approve decision

Only after completing the checks above, run:

The letter `Z` at the end of the expiry means Coordinated Universal Time
(UTC).

```powershell
$workedState = Read-CourseRunState $workedRunDir
if ($workedState.current_state -ceq 'needs_review' -and
    $workedState.draft_revision -eq 1 -and
    $null -eq $workedState.active_decision_path) {
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
    $workedState = Read-CourseRunState $workedRunDir
} elseif ($workedState.current_state -cin @('approved_for_local_export','approved_draft') -and
    $workedState.draft_revision -eq 1 -and
    $workedState.active_decision_path -ceq 'review/decision-r1.json') {
    Write-Host 'RESUME: the exact revision 1 approval already exists.'
} else {
    throw "Worked decision is not at the exact before-or-after approval state. Nothing was repeated: $($workedState.current_state), revision $($workedState.draft_revision)"
}
if ($workedState.current_state -cnotin @('approved_for_local_export','approved_draft')) {
    throw 'Worked approval did not reach its exact expected state.'
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
- exact protected review-manifest SHA-256;
- decision and expiry times;
- `evidence_reviewed: true`;
- reason.

The manifest binds the exact source, issue JSON and spreadsheet-safe CSV,
summary, control, run configuration, and review package that you inspected.
The runner recomputes those hashes before both decision and export; it does not
trust the saved manifest by itself. The decision ID is also recomputed from
every material decision field. This detects local accidental or simple
editing. It does not authenticate a person and is not a digital signature.

An approval is not transferable to “whatever file is latest.”

The decision is recorded in the copied run under
`evidence\module-06\worked-decision\RUN-…`. The final folder keeps the exact
protected run identifier shown in Module 5. Module 5 evidence remains unchanged.

### Stage 3 — Create the approved local drafts

Run:

```powershell
$workedState = Read-CourseRunState $workedRunDir
if ($workedState.current_state -ceq 'approved_for_local_export' -and
    $workedState.draft_revision -eq 1) {
    & $pythonExe $runner export --run-dir $workedRunDir
    if ($LASTEXITCODE -ne 0) {
        throw 'Export safely stopped. Read the named reason above.'
    }
    $workedState = Read-CourseRunState $workedRunDir
} elseif ($workedState.current_state -ceq 'approved_draft' -and
    $workedState.draft_revision -eq 1 -and
    $workedState.local_export_count -eq 2) {
    Write-Host 'RESUME: the exact two-file local export already exists.'
} else {
    throw "Worked export is not at the exact before-or-after state. Nothing was repeated: $($workedState.current_state)"
}
if ($workedState.current_state -cne 'approved_draft' -or
    $workedState.local_export_count -ne 2) {
    throw 'Worked export did not reach the exact approved-draft state.'
}
foreach ($approvedFile in 'approved-r1.csv','approved-r1.json') {
    if (-not (Test-Path -LiteralPath (Join-Path (Join-Path $workedRunDir 'outbox') $approvedFile) -PathType Leaf)) {
        throw "Expected approved output is missing: $approvedFile"
    }
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

Prove the runner's sequential retry directly. This block records both output
hashes and the logical export-event count, retries the same export, and requires
all three to remain unchanged:

```powershell
$workedOutbox = Join-Path $workedRunDir 'outbox'
$workedAudit = Join-Path $workedRunDir 'audit\events.jsonl'
$workedExportPaths = @(
    (Join-Path $workedOutbox 'approved-r1.csv'),
    (Join-Path $workedOutbox 'approved-r1.json')
)
$beforeExportHashes = @(
    Get-FileHash -LiteralPath $workedExportPaths -Algorithm SHA256 |
        Select-Object -ExpandProperty Hash
)
$beforeExportEvents = @(
    Get-Content -LiteralPath $workedAudit |
        ForEach-Object { $_ | ConvertFrom-Json } |
        Where-Object { $_.event_type -ceq 'local_export_created' }
).Count
& $pythonExe $runner export --run-dir $workedRunDir
if ($LASTEXITCODE -ne 0) {
    throw 'The sequential export retry safely stopped instead of returning the existing result.'
}
$afterExportHashes = @(
    Get-FileHash -LiteralPath $workedExportPaths -Algorithm SHA256 |
        Select-Object -ExpandProperty Hash
)
$afterExportEvents = @(
    Get-Content -LiteralPath $workedAudit |
        ForEach-Object { $_ | ConvertFrom-Json } |
        Where-Object { $_.event_type -ceq 'local_export_created' }
).Count
if (@(Compare-Object $beforeExportHashes $afterExportHashes).Count -ne 0 -or
    $beforeExportEvents -ne 1 -or
    $afterExportEvents -ne 1) {
    throw 'The sequential retry changed an output hash or created another logical export event.'
}
Write-Host 'PASS: same two output hashes and one logical export event after retry.'
```

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
$noEvidenceRun = Get-OrCreateCourseFailureRun $noEvidenceWorkspace
$noEvidenceState = Read-CourseRunState $noEvidenceRun
if ($noEvidenceState.current_state -cne 'needs_review' -or
    $noEvidenceState.draft_revision -ne 1 -or
    $null -ne $noEvidenceState.active_decision_path) {
    throw 'The no-evidence lab is not at the exact undecided revision 1 state.'
}
& $pythonExe $runner decide `
    --run-dir $noEvidenceRun `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Deliberately omitted evidence confirmation for this failure test.' `
    --expected-revision 1
$noEvidenceExit = $LASTEXITCODE
if ($noEvidenceExit -ne 1 -or
    (Test-Path -LiteralPath (Join-Path $noEvidenceRun 'outbox'))) {
    throw 'The no-evidence attempt did not produce the exact safe stop with no outbox.'
}
$noEvidenceExit
```

Expected: `review_evidence_required`, exit code `1`, outbox `False`.

### Failure 2 — Stale revision update

```powershell
$staleWorkspace = Join-Path $moduleFolder 'failure-stale'
$staleRun = Get-OrCreateCourseFailureRun $staleWorkspace
$staleState = Read-CourseRunState $staleRun
if ($staleState.current_state -cne 'needs_review' -or
    $staleState.draft_revision -ne 1 -or
    $null -ne $staleState.active_decision_path) {
    throw 'The stale-revision lab is not at the exact undecided revision 1 state.'
}
& $pythonExe $runner decide `
    --run-dir $staleRun `
    --decision approve `
    --reviewer-role course_learner `
    --reason 'Deliberately used the wrong revision for this failure test.' `
    --expected-revision 2 `
    --evidence-reviewed
$staleExit = $LASTEXITCODE
if ($staleExit -ne 1 -or
    (Test-Path -LiteralPath (Join-Path $staleRun 'outbox'))) {
    throw 'The stale-revision attempt did not produce the exact safe stop with no outbox.'
}
$staleExit
```

Expected: `stale_update`, exit code `1`.

### Failure 3 — Edited draft after approval

```powershell
$editedWorkspace = Join-Path $moduleFolder 'failure-edited'
$editedRun = Get-OrCreateCourseFailureRun $editedWorkspace
$editedState = Read-CourseRunState $editedRun
if ($editedState.current_state -ceq 'needs_review') {
    if ($editedState.draft_revision -ne 1 -or
        $null -ne $editedState.active_decision_path) {
        throw 'Edited-draft lab is not at the exact undecided revision 1 state.'
    }
    & $pythonExe $runner decide `
        --run-dir $editedRun `
        --decision approve `
        --reviewer-role course_learner `
        --reason 'Synthetic approval used only for the edit invalidation test.' `
        --expected-revision 1 `
        --evidence-reviewed
    if ($LASTEXITCODE -ne 0) {
        throw 'Edited-draft lab approval safely stopped before intentional tampering.'
    }
    $editedState = Read-CourseRunState $editedRun
} elseif ($editedState.current_state -cne 'approved_for_local_export' -or
    $editedState.active_decision_path -cne 'review/decision-r1.json') {
    throw "Edited-draft lab is in an unfamiliar state: $($editedState.current_state)"
}
$editedDraft = Join-Path $editedRun 'draft\summary.json'
$editedBackup = Join-Path $moduleFolder 'failure-edited-original-summary.json'
if (Test-Path -LiteralPath $editedBackup) {
    if (-not (Test-Path -LiteralPath $editedBackup -PathType Leaf) -or
        (Get-FileHash -LiteralPath $editedBackup -Algorithm SHA256).Hash.ToLowerInvariant() -ne
        $editedState.draft_sha256) {
        throw 'Edited-draft backup is wrong-type or differs from the approved original.'
    }
} else {
    Copy-Item -LiteralPath $editedDraft -Destination $editedBackup
}
$originalBytes = [System.IO.File]::ReadAllBytes($editedBackup)
$currentBytes = [System.IO.File]::ReadAllBytes($editedDraft)
$stillOriginal =
    $currentBytes.Length -eq $originalBytes.Length -and
    -not (Compare-Object $originalBytes $currentBytes -SyncWindow 0)
if ($stillOriginal) {
    Add-Content -LiteralPath $editedDraft -Value ' ' -NoNewline
    $currentBytes = [System.IO.File]::ReadAllBytes($editedDraft)
}
$prefixMatches = $currentBytes.Length -eq ($originalBytes.Length + 1)
if ($prefixMatches) {
    for ($byteIndex = 0; $byteIndex -lt $originalBytes.Length; $byteIndex++) {
        if ($currentBytes[$byteIndex] -ne $originalBytes[$byteIndex]) {
            $prefixMatches = $false
            break
        }
    }
}
if (-not $prefixMatches -or $currentBytes[-1] -ne 32) {
    throw 'Edited-draft lab contains an unfamiliar change. Preserve it and ask for read-only diagnosis.'
}
& $pythonExe $runner export --run-dir $editedRun
$editedExit = $LASTEXITCODE
if ($editedExit -ne 1 -or
    (Test-Path -LiteralPath (Join-Path $editedRun 'outbox'))) {
    throw 'The edited-draft attempt did not produce the exact safe stop with no outbox.'
}
$editedExit
```

Expected: `edited_draft_after_approval`, exit code `1`, outbox `False`.

### Failure 4 — Expired approval

Fixed UTC times make this failure repeatable.

```powershell
$expiredWorkspace = Join-Path $moduleFolder 'failure-expired'
$expiredRun = Get-OrCreateCourseFailureRun $expiredWorkspace
$expiredState = Read-CourseRunState $expiredRun
if ($expiredState.current_state -ceq 'needs_review') {
    if ($expiredState.draft_revision -ne 1 -or
        $null -ne $expiredState.active_decision_path) {
        throw 'Expiry lab is not at the exact undecided revision 1 state.'
    }
    & $pythonExe $runner decide `
        --run-dir $expiredRun `
        --decision approve `
        --reviewer-role course_learner `
        --reason 'Synthetic approval with fixed times for the expiry test.' `
        --expected-revision 1 `
        --evidence-reviewed `
        --decided-at 2026-07-28T10:00:00Z `
        --expires-at 2026-07-28T11:00:00Z
    if ($LASTEXITCODE -ne 0) {
        throw 'Expiry-lab approval safely stopped before the expiry check.'
    }
    $expiredState = Read-CourseRunState $expiredRun
}
if ($expiredState.current_state -ceq 'approved_for_local_export' -and
    $expiredState.active_decision_path -ceq 'review/decision-r1.json') {
    & $pythonExe $runner export `
        --run-dir $expiredRun `
        --checked-at 2026-07-28T12:00:00Z
    $expiredExit = $LASTEXITCODE
    if ($expiredExit -ne 1) {
        throw 'The expiry check did not produce the expected safe-stop exit code.'
    }
    $expiredState = Read-CourseRunState $expiredRun
} elseif ($expiredState.current_state -ceq 'expired' -and
    $expiredState.active_decision_path -ceq 'review/decision-r1.json') {
    Write-Host 'RESUME: the exact expiry safe stop is already recorded.'
} else {
    throw "Expiry lab is in an unfamiliar state: $($expiredState.current_state)"
}
if ($expiredState.current_state -cne 'expired' -or
    $expiredState.active_decision_path -cne 'review/decision-r1.json' -or
    (Test-Path -LiteralPath (Join-Path $expiredRun 'outbox'))) {
    throw 'Expiry lab did not end in expired state with no outbox.'
}
Get-Content -LiteralPath (Join-Path $expiredRun 'state.json')
```

Expected: `expired_review`, exit code `1`, state `expired`, no outbox.

### Failure 5 — External-action control tampered

```powershell
$controlWorkspace = Join-Path $moduleFolder 'failure-control'
$controlRun = Get-OrCreateCourseFailureRun $controlWorkspace
$controlState = Read-CourseRunState $controlRun
if ($controlState.current_state -ceq 'needs_review') {
    if ($controlState.draft_revision -ne 1 -or
        $null -ne $controlState.active_decision_path) {
        throw 'Control-tamper lab is not at the exact undecided revision 1 state.'
    }
    & $pythonExe $runner decide `
        --run-dir $controlRun `
        --decision approve `
        --reviewer-role course_learner `
        --reason 'Synthetic approval used only for the control tamper test.' `
        --expected-revision 1 `
        --evidence-reviewed
    if ($LASTEXITCODE -ne 0) {
        throw 'Control-tamper lab approval safely stopped before intentional tampering.'
    }
    $controlState = Read-CourseRunState $controlRun
} elseif ($controlState.current_state -cne 'approved_for_local_export' -or
    $controlState.active_decision_path -cne 'review/decision-r1.json') {
    throw "Control-tamper lab is in an unfamiliar state: $($controlState.current_state)"
}
$controlPath = Join-Path $controlRun 'control.json'
try {
    $control = Get-Content -Raw -LiteralPath $controlPath | ConvertFrom-Json
} catch {
    throw 'Control-tamper lab control is not recognisable JSON. Preserve it and ask for read-only diagnosis.'
}
if ($control.EXTERNAL_ACTIONS_ENABLED -ceq $false) {
    $control.EXTERNAL_ACTIONS_ENABLED = $true
    $control | ConvertTo-Json | Set-Content -LiteralPath $controlPath -Encoding utf8
} elseif ($control.EXTERNAL_ACTIONS_ENABLED -ceq $true) {
    Write-Host 'RESUME: the isolated control is already intentionally tampered.'
} else {
    throw 'Control-tamper lab contains an unfamiliar control value.'
}
& $pythonExe $runner export --run-dir $controlRun
$controlExit = $LASTEXITCODE
if ($controlExit -ne 1 -or
    (Test-Path -LiteralPath (Join-Path $controlRun 'outbox'))) {
    throw 'The control-tamper attempt did not produce the exact safe stop with no outbox.'
}
$controlExit
```

Expected: `external_action_blocked`, exit code `1`, outbox `False`.

This tampering is allowed only in the isolated synthetic failure folder.

## Now recreate it yourself

Recreate the complete decision lifecycle with the different five-issue
candidate.

### Recreation 1 — Locate the five-issue run and your candidate

```powershell
if (-not (Test-Path -LiteralPath $moduleFiveCandidate -PathType Leaf)) {
    throw 'Module 5 candidate summary missing.'
}
if (-not (Test-Path -LiteralPath $moduleFiveSupportReview -PathType Leaf)) {
    throw 'Module 5 recreated support review missing.'
}
Copy-CourseDecisionRunOnce `
    -SourceRun $moduleFiveRecreatedRunDir `
    -DestinationRun $recreatedRunDir `
    -CopyRecord $recreatedCopyRecord `
    -ImmutableRelativePaths $immutableRunEvidence
if (Test-Path -LiteralPath $candidate) {
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf) -or
        (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $moduleFiveCandidate -Algorithm SHA256).Hash) {
        throw 'Saved candidate copy is wrong-type or differs from its Module 5 source.'
    }
    Write-Host "RESUME: verified $candidate"
} else {
    Copy-Item -LiteralPath $moduleFiveCandidate -Destination $candidate
    if ((Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $moduleFiveCandidate -Algorithm SHA256).Hash) {
        throw 'New candidate copy did not match its source.'
    }
}
if (Test-Path -LiteralPath $recreatedSupportReviewCopy) {
    if (-not (Test-Path -LiteralPath $recreatedSupportReviewCopy -PathType Leaf) -or
        (Get-FileHash -LiteralPath $recreatedSupportReviewCopy -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $moduleFiveSupportReview -Algorithm SHA256).Hash) {
        throw 'Saved recreated support-review copy is wrong-type or differs from its Module 5 source.'
    }
    Write-Host "RESUME: verified $recreatedSupportReviewCopy"
} else {
    Copy-Item -LiteralPath $moduleFiveSupportReview -Destination $recreatedSupportReviewCopy
    if ((Get-FileHash -LiteralPath $recreatedSupportReviewCopy -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $moduleFiveSupportReview -Algorithm SHA256).Hash) {
        throw 'New recreated support-review copy did not match its source.'
    }
}
& $pythonExe $runner status --run-dir $recreatedRunDir
if ($LASTEXITCODE -ne 0) {
    throw 'Recreated copy status validation safely stopped. Do not review or decide from this run.'
}
```

All learner evidence that Module 6 will change or later ask Codex to assess now
sits under `evidence\module-06`. Module 5 remains the unchanged source.

### Recreation 2 — Request an edit of revision 1

Create the review at the exact path
`evidence\module-06\recreated_review_r1.md`. The command below creates the
headings once and never overwrites a prior review:

```powershell
if (Test-Path -LiteralPath $reviewR1) {
    if (-not (Test-Path -LiteralPath $reviewR1 -PathType Leaf) -or
        (Get-Content -LiteralPath $reviewR1 -TotalCount 1) -cne '# Recreated review — revision 1') {
        throw 'Existing revision 1 review is the wrong type or unfamiliar. Preserve it and stop.'
    }
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
Eight protected manifest paths checked:
Exact review-manifest SHA-256:
Manual fallback:
Decision: edit
Exact wording to change:
'@ | Set-Content -LiteralPath $reviewR1 -Encoding utf8
}
notepad $reviewR1
```

Complete and save it in your own words before continuing. Record every
evidence check, both exact hashes, decision `edit`, and the exact wording you
want changed.

Then run:

```powershell
Get-FileHash -LiteralPath (Join-Path $recreatedRunDir 'review\review_manifest.json') -Algorithm SHA256
$recreatedState = Read-CourseRunState $recreatedRunDir
if ($recreatedState.current_state -ceq 'needs_review' -and
    $recreatedState.draft_revision -eq 1 -and
    $null -eq $recreatedState.active_decision_path) {
    & $pythonExe $runner decide `
        --run-dir $recreatedRunDir `
        --decision edit `
        --reviewer-role course_learner `
        --reason 'Use my validated candidate wording and require a complete new review.' `
        --expected-revision 1
    if ($LASTEXITCODE -ne 0) {
        throw 'Edit decision safely stopped. The revision command was not run.'
    }
    $recreatedState = Read-CourseRunState $recreatedRunDir
}
if ($recreatedState.current_state -ceq 'changes_requested' -and
    $recreatedState.draft_revision -eq 1 -and
    $recreatedState.active_decision_path -ceq 'review/decision-r1.json') {
    & $pythonExe $runner revise `
        --run-dir $recreatedRunDir `
        --replacement $candidate `
        --expected-revision 1
    if ($LASTEXITCODE -ne 0) {
        throw 'Revision safely stopped. Read the named reason above.'
    }
    $recreatedState = Read-CourseRunState $recreatedRunDir
} elseif ($recreatedState.current_state -ceq 'needs_review' -and
    $recreatedState.draft_revision -eq 2 -and
    $null -eq $recreatedState.active_decision_path) {
    Write-Host 'RESUME: revision 2 already exists and awaits a new review.'
} else {
    throw "Recreated run is not at the exact before-or-after revision state. Nothing was repeated: $($recreatedState.current_state), revision $($recreatedState.draft_revision)"
}
& $pythonExe $runner status --run-dir $recreatedRunDir
if ($LASTEXITCODE -ne 0) {
    throw 'Status validation safely stopped after revision.'
}
```

Expected: revision `2`, state `needs_review`, no active decision, no outbox.

### Recreation 3 — Review and approve revision 2

Create the second review at the exact path
`evidence\module-06\recreated_review_r2.md`. This command creates it once and
keeps a prior version unchanged:

```powershell
if (Test-Path -LiteralPath $reviewR2) {
    if (-not (Test-Path -LiteralPath $reviewR2 -PathType Leaf) -or
        (Get-Content -LiteralPath $reviewR2 -TotalCount 1) -cne '# Recreated review — revision 2') {
        throw 'Existing revision 2 review is the wrong type or unfamiliar. Preserve it and stop.'
    }
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
Eight protected manifest paths checked:
Exact review-manifest SHA-256:
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
- all eight protected manifest paths and the exact manifest hash;
- manual fallback.

Then run:

```powershell
Get-FileHash -LiteralPath (Join-Path $recreatedRunDir 'draft\summary.json') -Algorithm SHA256
Get-FileHash -LiteralPath (Join-Path $recreatedRunDir 'review\review_manifest.json') -Algorithm SHA256
$recreatedState = Read-CourseRunState $recreatedRunDir
if ($recreatedState.current_state -ceq 'needs_review' -and
    $recreatedState.draft_revision -eq 2 -and
    $null -eq $recreatedState.active_decision_path) {
    & $pythonExe $runner decide `
        --run-dir $recreatedRunDir `
        --decision approve `
        --reviewer-role course_learner `
        --reason 'Reviewed revision 2 against all five synthetic source-linked issues.' `
        --expected-revision 2 `
        --evidence-reviewed `
        --expires-at 2099-01-01T00:00:00Z
    if ($LASTEXITCODE -ne 0) {
        throw 'Revision 2 approval safely stopped. Export was not run.'
    }
    $recreatedState = Read-CourseRunState $recreatedRunDir
} elseif ($recreatedState.current_state -cin @('approved_for_local_export','approved_draft') -and
    $recreatedState.draft_revision -eq 2 -and
    $recreatedState.active_decision_path -ceq 'review/decision-r2.json') {
    Write-Host 'RESUME: the exact revision 2 approval already exists.'
} else {
    throw "Recreated approval is not at the exact before-or-after state. Nothing was repeated: $($recreatedState.current_state), revision $($recreatedState.draft_revision)"
}
if ($recreatedState.current_state -ceq 'approved_for_local_export') {
    & $pythonExe $runner export --run-dir $recreatedRunDir
    if ($LASTEXITCODE -ne 0) {
        throw 'Revision 2 export safely stopped. Read the named reason above.'
    }
    $recreatedState = Read-CourseRunState $recreatedRunDir
} elseif ($recreatedState.current_state -ceq 'approved_draft' -and
    $recreatedState.local_export_count -eq 2) {
    Write-Host 'RESUME: the exact two-file revision 2 export already exists.'
} else {
    throw "Recreated export is not at the exact before-or-after state: $($recreatedState.current_state)"
}
if ($recreatedState.current_state -cne 'approved_draft' -or
    $recreatedState.local_export_count -ne 2) {
    throw 'Revision 2 export did not reach the exact approved-draft state.'
}
(Import-Csv -LiteralPath (Join-Path $recreatedRunDir 'outbox\approved-r2.csv')).Count
```

Expected: `PASS` and count `5`.

### Recreation 4 — Prove reject and explicit expire separately

Prepare two fresh recreated workspaces and choose different decisions:

```powershell
$recreatedDecisionInput = Join-Path $recreatedRunDir 'source\work_items.csv'
foreach ($decision in 'reject','expire') {
    $workspace = Join-Path $moduleFolder "recreated-$decision"
    $runDir = Resolve-SavedCourseRun $workspace
    if ($null -eq $runDir) {
        & $pythonExe $runner prepare `
            --input $recreatedDecisionInput `
            --workspace $workspace `
            --ai-mode mock `
            --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
        if ($LASTEXITCODE -ne 0) {
            throw "The $decision recreation safely stopped before a run was created."
        }
        $runDir = Resolve-SavedCourseRun $workspace
    } else {
        Write-Host "RESUME: keeping the validated run $runDir"
    }
    $expectedDecisionState = if ($decision -ceq 'reject') { 'rejected' } else { 'expired' }
    $decisionState = Read-CourseRunState $runDir
    if ($decisionState.current_state -ceq 'needs_review' -and
        $decisionState.draft_revision -eq 1 -and
        $null -eq $decisionState.active_decision_path) {
        & $pythonExe $runner decide `
            --run-dir $runDir `
            --decision $decision `
            --reviewer-role course_learner `
            --reason "Synthetic $decision decision; local export must remain blocked." `
            --expected-revision 1
        if ($LASTEXITCODE -ne 0) {
            throw "The $decision decision safely stopped. Export was not attempted."
        }
        $decisionState = Read-CourseRunState $runDir
    } elseif ($decisionState.current_state -ceq $expectedDecisionState -and
        $decisionState.draft_revision -eq 1 -and
        $decisionState.active_decision_path -ceq 'review/decision-r1.json') {
        Write-Host "RESUME: the exact $decision decision already exists."
    } else {
        throw "The $decision run is not at its exact before-or-after state. Nothing was repeated: $($decisionState.current_state)"
    }
    if ($decisionState.current_state -cne $expectedDecisionState) {
        throw "The $decision decision did not reach state $expectedDecisionState."
    }
    & $pythonExe $runner export --run-dir $runDir
    $blockedExportExit = $LASTEXITCODE
    if ($blockedExportExit -ne 1 -or
        (Test-Path -LiteralPath (Join-Path $runDir 'outbox'))) {
        throw "The $decision export did not produce the exact safe stop with no outbox."
    }
    Write-Host "EXPECTED SAFE STOP for $decision; exit code $blockedExportExit"
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
code is `0`. This course revision must say `Ran 61 tests`; a different count is
a safe stop until the course owner intentionally updates this stated contract.
The suite covers:

- frozen and recreated accuracy;
- schemas for work items, issues, summary, approval, audit, evaluation,
  control, state, run configuration, review package, and review manifest;
- duplicate ID and retry;
- required evidence and stale update;
- malformed, missing, and wrong-header input;
- AI disabled, timeout, refusal, malformed JSON, and unknown issue ID;
- untrusted free text;
- edited, rejected, edit-requested, and expired reviews;
- canonical run identity and protected-artifact tamper blocking;
- decision-field tamper blocking;
- spreadsheet-safe CSV with exact JSON/source evidence;
- atomic paired local CSV/JSON export and safe rollback;
- short repeated-failure evidence on long Windows paths;
- manual fallback, damaged-state recovery, and audit contract.

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
$expectedCourseOneTests = 61
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
$testsRun = if ($ranLine -match '^Ran (\d+) tests?') {
    [int]$Matches[1]
} else {
    $null
}
$acceptancePassed =
    $testExitCode -eq 0 -and
    $testsRun -eq $expectedCourseOneTests -and
    $resultLine -ceq 'OK'
[PSCustomObject]@{
    schema_version = 1
    attempt = $recordedAttempt
    suite = 'course1_capstone unittest discovery'
    status = if ($acceptancePassed) { 'PASS' } else { 'FAIL' }
    exit_code = $testExitCode
    tests_run = $testsRun
    expected_tests = $expectedCourseOneTests
    result = if ($resultLine) { $resultLine } else { 'NO RESULT LINE' }
    raw_diagnostics_committed = $false
    raw_diagnostics_location = 'outside_repository_temporary_file'
} | ConvertTo-Json | Set-Content -LiteralPath $acceptancePath -Encoding utf8
Write-Host "SAVED path-neutral evidence attempt $recordedAttempt"
if (-not $acceptancePassed) {
    Write-Host 'Raw diagnostics are outside the repository. Do not add them to Git.'
    Write-Host "Open the raw diagnostics with: notepad.exe `"$rawDiagnosticsPath`""
    throw "Automated acceptance failed. Required: exit 0, exactly $expectedCourseOneTests tests, result OK. Preserve the structured FAIL record and repair the named failure."
}
```

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
[PASTE FULL MODULE-06 PATH]
[PASTE FULL SRC\COURSE1_CAPSTONE PATH]
[PASTE FULL MODULE-04 REFERENCE_RUNNER_HASHES.JSON PATH]

Learner attestation: I created these files for this fictional exercise and
have not knowingly put real client, employer, personal, medical, credential,
or secret data in them. This statement is an attestation, not proof.

You may only list names, read files, and calculate hashes inside the authorised
module and runner folders and the one authorised hash-record file. Do not
inspect any other Module 4 or Module 5 artifact. Do not create, edit, delete,
rename, move, or format any file. Do not
execute the runner, lesson scripts, or tests, use a network, or inspect a
parent or other location. If apparent sensitive data is noticed,
do not quote or repeat it: return NOT YET with only the filename and general
category, then stop. If none is noticed, say that non-detection is not proof
that none exists.

Return:
1. PASS or NOT YET;
2. worked approval bound to the exact run, revision, draft hash, protected
   review-manifest hash, reviewer, reason, and expiry;
3. local approved CSV/JSON with 13 records and external actions 0;
4. required-evidence, stale-update, edited-draft, expired-review, and tampered
control safe-stop evidence;
5. recreated edit -> revision 2 -> new review -> approve -> five-record export;
6. reject and explicit expire blocking export;
7. canonical audit events, evaluation, manual fallback, and idempotent retry;
8. every numbered path-neutral automated acceptance record, with the
   highest-numbered attempt showing status PASS, exactly 61 of 61 expected
   tests, result OK, and exit code 0; treat the learner-created record as
   evidence of the run, not independent proof that the suite executed;
9. whether the authorised artifacts are consistent with synthetic-only work
   and show any configured network call, provider key, paid service, or
   external action; say explicitly that non-detection is not proof of absence;
10. the smallest learner-made corrections if NOT YET.

Remain read-only. Do not provide replacement files.
```

## Pass criteria

- [ ] Exact project Python is used through `$pythonExe`.
- [ ] The runner still matches Module 4's verified three-file SHA-256 record.
- [ ] Evidence review is explicit before approval.
- [ ] Approval is bound to one run, revision, draft hash, protected
      review-manifest hash, reviewer, reason, and expiry.
- [ ] Every protected artifact and material decision field is rechecked before
      local export.
- [ ] Approve, edit, reject, and expire cause different enforced states.
- [ ] Edited, stale, expired, rejected, and evidence-free cases cannot export.
- [ ] `EXTERNAL_ACTIONS_ENABLED=false` is explicit and tampering blocks export.
- [ ] Approved output is local CSV and JSON only.
- [ ] Worked export has 13 records; recreated revision 2 export has 5.
- [ ] Audit events contain every required field and claim zero external actions.
- [ ] Manual fallback is complete and role-owned.
- [ ] Exactly 61 automated tests pass with result `OK` and exit code 0.
- [ ] All data is synthetic and secret-free.
- [ ] Codex returns `PASS` in read-only mode.

### Record your Module 6 PASS in Git

Only after Codex returns `PASS`, rerun the complete **Start or resume safely**
block in this same PowerShell window so the exact marker and Git-root checks
pass again:

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence\module-06"
git commit --only -m "complete module 6 evidence" -- "evidence/module-06"
git status --short
```

`git commit --only` restricts this checkpoint to the repeated module path,
even if a different file had already been staged.

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
