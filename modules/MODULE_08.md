# Module 8 — Evaluate Usefulness and Business Value

## Outcome

You will calculate rule quality, inspect summary support, compare active time,
model cost and capacity honestly, record usability evidence, and make a
bounded **provisional pre-User Acceptance Testing (pre-UAT) recommendation**
before claiming value. Module 9 adds User Acceptance Testing (UAT),
defects/retests, adoption, and handover
evidence before you finalise the Course 1 decision.

## Beginner checkpoint

Start when Modules 1–7 pass. Inputs, expected results, configuration, code, and
prompt versions must be frozen for the evaluation run.

## Concepts

- An **evaluation set** has fixed inputs and expected results.
- **Precision** is true positives divided by all reported positives.
- **Recall** is true positives divided by all expected positives.
- A **false positive** is extra; a **false negative** is missed.
- **Supported-claim rate** is supported statements divided by statements
  checked.
- A **matched baseline** compares equivalent manual and assisted work.
- **Regression** is a previously passing behaviour that fails after change.
- A **decision threshold** is written before seeing a result.
- Course 1 uses exactly three decision labels:
  `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, and `DO NOT CONTINUE`.
  Each is a valid pass when the recorded evidence supports it.
- Module 8 records one of those labels as a
  `PROVISIONAL PRE-UAT` recommendation. It is not the final Course 1 decision.
  Module 9 must reassess the recommendation after UAT, defect/retest, adoption,
  and handover evidence and mark the resulting decision `FINAL POST-UAT`.

## Official readings

The United States National Institute of Standards and Technology (NIST)
publishes voluntary artificial intelligence (AI) risk guidance. OpenAI is one
AI provider and supplies the evaluation guide below. GOV.UK is the United
Kingdom government's public guidance website.

1. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
2. [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evals)
3. [GOV.UK Service Manual: measuring success](https://www.gov.uk/service-manual/measuring-success)

## Guided build

The worked example has attractive time savings but deliberately poor rule
quality, so the correct decision is rework. The independent recreation uses
the different 13-issue capstone result.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files. Comma-separated
values (CSV) stores the test rows; JavaScript Object Notation (JSON) stores the
metric report. EUR is the three-letter currency code for the euro.

Python is the programming language used to calculate the metrics. Markdown is
a plain-text format for headings, lists, and tables; `.md` is its file name
ending.

## Start or resume safely

At the start of every study session, rerun Stage 1. PowerShell forgets its
temporary variables when closed, while your files remain. Stage 1 restores the
course, project, module, and earlier-evidence paths; defines the project Python;
and restores the create-once helpers. Before any lesson write, it requires the
exact synthetic-course marker and proves that the marked folder is the Git
repository root. It does not open, replace, or erase a lesson file. Copy and
text-creation helpers below skip an existing destination.

After any session break:

1. rerun Stage 1;
2. before Recreation 1 or any later recreation, rerun the complete Module 4
   source/provenance locator block under Recreation 1;
3. before starting or resuming either timer, rerun the earlier-evidence locator
   block under Recreation 2;
4. if PowerShell closed or the timer was interrupted, reject that timing
   attempt and restart its timer from zero. Never reconstruct elapsed time from
   memory.

Suggested sessions:

1. create the imperfect worked set and calculate its metrics;
2. finish the worked decision, support review, time/cost scenarios, and
   regression rule;
3. evaluate the different capstone result, complete the decision worksheet,
   run the Codex check, and make the Git checkpoint.

Save every file and note the last numbered step before stopping. A file reported
as `SKIP CREATE` already exists and is left closed and unchanged. Open it
yourself only when you deliberately intend to continue its incomplete content;
never paste a worked example over completed evidence.

## Follow along — I show you exactly how

### Stage 1 — Restore all paths and create-once helpers safely

Open Windows PowerShell and run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
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
$moduleFolder = Join-Path $projectRoot 'evidence\module-08'
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Course Python not found. Complete Windows Setup before Module 8.'
}
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
if (-not (Test-Path -LiteralPath (Join-Path $courseRoot 'practice_data\expected_issues.csv'))) {
    throw 'That course folder does not contain the Course 1 practice data.'
}
$moduleOneBaseline = Join-Path $projectRoot 'evidence\module-01\baseline_and_value_record.md'
$moduleTwoBrief = Join-Path $projectRoot 'evidence\module-02\recreated_opportunity_brief.md'
$moduleThreeRules = Join-Path $projectRoot 'evidence\module-03\recreated_data_and_rules.md'
$moduleFour = Join-Path $projectRoot 'evidence\module-04'
$moduleFiveSupport = Join-Path $projectRoot 'evidence\module-05\worked_support_review.md'
$moduleSixWorkedParent = Join-Path $projectRoot 'evidence\module-06\worked-decision'
$moduleSixCopyRecord = Join-Path $moduleSixWorkedParent 'initial_copy_hashes.json'
if (-not (Test-Path -LiteralPath $moduleSixCopyRecord -PathType Leaf)) {
    throw 'Module 6 worked-copy record is missing. Complete Module 6 Stage 1 first.'
}
try {
    $moduleSixCopy = Get-Content -Raw -LiteralPath $moduleSixCopyRecord |
        ConvertFrom-Json
} catch {
    throw 'Module 6 worked-copy record is not recognisable JSON. Preserve it and ask for read-only diagnosis.'
}
$moduleSixRunId = [string]$moduleSixCopy.source_run_id
if ($moduleSixRunId -cnotmatch '^RUN-[A-F0-9]{12}$' -or
    $moduleSixCopy.destination_run_leaf -cne $moduleSixRunId) {
    throw 'Module 6 worked-copy record does not name one exact protected run.'
}
$moduleSixRunDir = Join-Path $moduleSixWorkedParent $moduleSixRunId
if (-not (Test-Path -LiteralPath $moduleSixRunDir -PathType Container)) {
    throw 'Module 6 worked decision run is missing. Complete Module 6 first.'
}
$resolvedModuleSixParent = (Resolve-Path -LiteralPath $moduleSixWorkedParent).Path
$resolvedModuleSixRun = (Resolve-Path -LiteralPath $moduleSixRunDir).Path
if ((Split-Path -Parent $resolvedModuleSixRun) -ne $resolvedModuleSixParent) {
    throw 'Module 6 worked decision run resolves outside its controlled parent.'
}
$moduleSixStatePath = Join-Path $resolvedModuleSixRun 'state.json'
try {
    $moduleSixState = Get-Content -Raw -LiteralPath $moduleSixStatePath |
        ConvertFrom-Json
} catch {
    throw 'Module 6 worked decision state is missing or not recognisable JSON.'
}
if ($moduleSixState.run_id -cne $moduleSixRunId -or
    $moduleSixState.current_state -cne 'approved_draft') {
    throw 'Module 6 worked decision is not the exact completed approved-draft run.'
}
$moduleSixSummary = Join-Path $resolvedModuleSixRun 'draft\summary.json'
$moduleSixDecision = Join-Path $resolvedModuleSixRun 'review\decision-r1.json'
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function Copy-NewPracticeFile {
    param([string]$Source, [string]$Destination)
    if (Test-Path -LiteralPath $Destination) {
        Write-Host "SKIP COPY: $Destination already exists and was left unchanged."
    } else {
        Copy-Item -LiteralPath $Source -Destination $Destination
        Write-Host "CREATED COPY: $Destination"
    }
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
            Write-Host "SKIP CREATE: $Path has the required completion markers and was left unchanged."
            return
        }
        Move-ToNumberedPreservedFile -Path $Path
    }
    [System.IO.File]::WriteAllText($Path, '', $utf8NoBom)
    Write-Host "CREATED NEW TEXT FILE: $Path. Any incomplete prior attempt was preserved."
    notepad $Path
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
    Write-Host "PRESERVED PRIOR ATTEMPT: $candidate"
}
New-Item -ItemType Directory -Force -Path $moduleFolder | Out-Null
Set-Location -LiteralPath $moduleFolder
$pythonExe
```

Stage 1 is now complete. It did not open a lesson file. To create
`worked_expected.csv` once, run:

```powershell
Start-NewPracticeTextFile -Path .\worked_expected.csv -RequiredPatterns `
    'work_item_id,rule_code,field,severity', `
    'WI-7004,R011,reference,medium'
```

If PowerShell says `CREATED NEW TEXT FILE`, paste and save the complete example
below from the beginning. Any empty or incomplete prior attempt has been kept
under a numbered `-preserved-` name. If it says `SKIP CREATE`, the required
first and last markers already exist; do not paste it again.

```csv
work_item_id,rule_code,field,severity
WI-7001,R001,status,high
WI-7002,R004,review_completed,high
WI-7003,R007,due_date,medium
WI-7004,R011,reference,medium
```

Create `worked_found.csv`:

```powershell
Start-NewPracticeTextFile -Path .\worked_found.csv -RequiredPatterns `
    'work_item_id,rule_code,field,severity', `
    'WI-7999,R009,owner_role,medium'
```

Paste the complete CSV below only when the helper says it created the file.
An incomplete prior attempt is preserved under a numbered name. On
`SKIP CREATE`, retain the completed evidence.

```csv
work_item_id,rule_code,field,severity
WI-7001,R001,status,high
WI-7002,R004,review_completed,high
WI-7003,R007,due_date,medium
WI-7999,R009,owner_role,medium
```

The system found three expected issues, added one false issue, and missed one.

### Stage 2 — Calculate exact metrics

Create `evaluate_worked.py`:

```powershell
Start-NewPracticeTextFile -Path .\evaluate_worked.py -RequiredPatterns `
    'def main() -> None:', `
    'if __name__ == "__main__":'
```

Paste the complete Python below only into a newly created empty file. The
helper preserves an incomplete prior attempt before recreating the normal file.
If it says `SKIP CREATE`, do not replace the completed program.

```python
from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
EXPECTED_FILE = BASE / "worked_expected.csv"
FOUND_FILE = BASE / "worked_found.csv"
REPORT_FILE = BASE / "worked_metrics.json"


def load(path: Path) -> dict[tuple[str, str, str], str]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    result: dict[tuple[str, str, str], str] = {}
    for row in rows:
        key = (row["work_item_id"], row["rule_code"], row["field"])
        if key in result:
            raise ValueError(f"Duplicate key in {path.name}: {key}")
        result[key] = row["severity"]
    return result


def ratio(numerator: int, denominator: int) -> float:
    return 1.0 if denominator == 0 else numerator / denominator


def main() -> None:
    expected = load(EXPECTED_FILE)
    found = load(FOUND_FILE)
    expected_keys = set(expected)
    found_keys = set(found)
    true_positive = expected_keys & found_keys
    false_positive = found_keys - expected_keys
    false_negative = expected_keys - found_keys
    severity_mismatches = sorted(
        key for key in true_positive if expected[key] != found[key]
    )
    high_expected = {key for key, value in expected.items() if value == "high"}
    high_found_correctly = high_expected & found_keys

    report = {
        "expected": len(expected_keys),
        "found": len(found_keys),
        "true_positive": len(true_positive),
        "false_positive": sorted(false_positive),
        "false_negative": sorted(false_negative),
        "precision": ratio(len(true_positive), len(found_keys)),
        "recall": ratio(len(true_positive), len(expected_keys)),
        "high_severity_recall": ratio(
            len(high_found_correctly), len(high_expected)
        ),
        "severity_mismatches": severity_mismatches,
    }
    REPORT_FILE.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

Run:

```powershell
& $pythonExe .\evaluate_worked.py
```

**Expected result:** precision `0.75`, recall `0.75`, high-severity recall
`1.0`, one false positive, one false negative, and no severity mismatch.

**Troubleshooting:**

- If a duplicate-key error appears, do not delete evidence blindly; identify
  why one logical issue was recorded twice.
- If precision and recall are confused, remember: precision asks “of what was
  reported, how much was right?” Recall asks “of what should be found, how much
  was found?”

### Stage 3 — Complete the value and usefulness decision

Create `worked_evaluation_decision.md`:

```powershell
Start-NewPracticeTextFile -Path .\worked_evaluation_decision.md -RequiredPatterns `
    'WORKED-M08-DECISION', `
    'Decision stage/status: PROVISIONAL PRE-UAT', `
    'It does not authorize a client pilot, production use, or real data.'
```

Paste the completed example below only when the helper says it created the
file. The helper preserves an incomplete prior attempt first. A resumed lesson
keeps a completed worked decision unchanged.

```markdown
# Worked Course 1 evaluation decision record

- Artifact ID: WORKED-M08-DECISION
- Version/date: 1.0 / 2026-07-28
- Author and decision owner: course learner in a fictional evaluator role
- Evaluation type: COURSE 1 SYNTHETIC PORTFOLIO WORK ONLY
- Decision stage/status: PROVISIONAL PRE-UAT

## Evaluation hypothesis and scope

Test whether a rule-first local exception report can identify all frozen
fictional issues, keep every summary claim linked to an issue, require review,
and reduce active handling time. Inputs and outputs are synthetic local files.
The workflow cannot send, pay, delete, update a source system, or authorize
business use. The manual fallback is the documented row-by-row check.

## Entry-gate result

Process, owner, baseline, data contract, risk screen, tool ownership, and
synthetic test entry criteria are present. User Acceptance Testing and training
are not yet complete and remain Module 9 work.

## Thresholds written before decision

- Precision: 100% on frozen synthetic set.
- Recall: 100%.
- High-severity recall: 100%.
- Severity mismatches: 0.
- Supported summary statements: 100%.
- External actions: 0.
- Manual fallback drill: pass.

## Observed rule result

- Precision: 75% — fail.
- Recall: 75% — fail.
- High-severity recall: 100% — pass.
- Severity mismatches: 0 — pass.

## Summary support

Four statements checked; four supported; supported-claim rate 100%. This does
not repair the rule failures upstream.

## Matched active-time method

The matched task is: use the same frozen input and rules to produce one
source-linked attention package, check every issue and summary statement,
record only human-review actions, and save an explicit review decision.

Manual timer boundary:

1. Start immediately before opening the frozen input and rules.
2. Identify and record every issue without using the generated or expected
   issue files.
3. Write the short source-linked summary and human-review actions.
4. Check every recorded issue, statement, and action against source and rule.
5. Stop immediately after saving the review decision.

Assisted timer boundary:

1. Start immediately before opening the generated issue and summary package.
2. Check every generated issue against the same frozen source and rules.
3. Check every summary statement and human-review action.
4. Save the explicit review decision.
5. Stop immediately after that save.

Both timers include human review and corrections. Both exclude installation,
learning, breaks, and unattended computer time. The same fictional reviewer
performs both tasks. In this worked measurement, manual active time is 30
minutes and assisted active time including review is 15 minutes.

## Completed low/expected/high cost scenarios — not forecasts

Common assumptions: loaded labour is EUR 45/hour; manual time is 30 minutes per
run; assisted review is 15 minutes per run. Setup is shown separately as a
one-time allocation. The recurring assisted total includes **review,
licence/usage, maintenance, support, training, fallback, and incident** costs.

| Scenario | Runs/month | Manual cost formula | Review cost formula | Licence/usage | Maintenance | Support | Training | Fallback | Incident | Recurring difference formula | One-time setup | First-month difference |
|---|---:|---|---|---:|---|---|---|---|---|---|---|---|
| low | 4 | 4 × 30 / 60 × 45 = EUR 90.00 | 4 × 15 / 60 × 45 = EUR 45.00 | EUR 5.00 | 0.5 h × 45 = EUR 22.50 | 0.25 h × 45 = EUR 11.25 | 0.25 h × 45 = EUR 11.25 | 1 × 30 / 60 × 45 = EUR 22.50 | 0.25 h × 45 = EUR 11.25 | 90 − (45 + 5 + 22.50 + 11.25 + 11.25 + 22.50 + 11.25) = **EUR -38.75** | 1 h × 45 = EUR 45.00 | -38.75 − 45 = **EUR -83.75** |
| expected | 8 | 8 × 30 / 60 × 45 = EUR 180.00 | 8 × 15 / 60 × 45 = EUR 90.00 | EUR 10.00 | 1 h × 45 = EUR 45.00 | 0.5 h × 45 = EUR 22.50 | 0.5 h × 45 = EUR 22.50 | 1 × 30 / 60 × 45 = EUR 22.50 | 0.5 h × 45 = EUR 22.50 | 180 − (90 + 10 + 45 + 22.50 + 22.50 + 22.50 + 22.50) = **EUR -55.00** | 2 h × 45 = EUR 90.00 | -55 − 90 = **EUR -145.00** |
| high | 16 | 16 × 30 / 60 × 45 = EUR 360.00 | 16 × 15 / 60 × 45 = EUR 180.00 | EUR 20.00 | 2 h × 45 = EUR 90.00 | 1 h × 45 = EUR 45.00 | 1 h × 45 = EUR 45.00 | 2 × 30 / 60 × 45 = EUR 45.00 | 1 h × 45 = EUR 45.00 | 360 − (180 + 20 + 90 + 45 + 45 + 45 + 45) = **EUR -110.00** | 4 h × 45 = EUR 180.00 | -110 − 180 = **EUR -290.00** |

Capacity released is 1, 2, and 4 hours respectively, but none is automatically
cash saved. The negative results are valid evidence: attractive time results
do not make this worked case economically positive after all named costs.
Unpriced residual risk remains a limitation rather than being hidden as zero.

## Usability check

Tasks: find source row; find rule; distinguish severity; reject draft; use
fallback. Four of five completed without help. Fallback instructions were
unclear.

## Defects and residual risk

DEFECT-01: one expected issue was missed. DEFECT-02: one unsupported issue was
added. DEFECT-03: fallback wording caused hesitation. Owners are the learner
for correction and the fictional operations lead for rule confirmation.
Retest the unchanged frozen set after repair. External actions remain disabled.

## Provisional recommendation

REWORK. Precision, recall, and usability thresholds fail. Attractive time and
cost scenarios do not override quality. Repair the missed/extra rule result and
fallback wording, rerun the frozen set, then decide again.

This provisional recommendation closes only this synthetic evaluation run.
Module 9 must reassess it after UAT, defect/retest, adoption, and handover
evidence. It does not authorize a client pilot, production use, or real data.
```

This is the complete decision logic: quality gates come before benefit claims.

### Stage 4 — Define regression control

Create `worked_regression_policy.md`:

```powershell
Start-NewPracticeTextFile -Path .\worked_regression_policy.md -RequiredPatterns `
    '# Worked regression policy', `
    'Do not change expected results merely because implementation changed.'
```

Paste the policy below only into a newly created file. An incomplete prior
attempt is preserved first. On `SKIP CREATE`, retain the completed policy.

```markdown
# Worked regression policy

Rerun the frozen evaluation after changes to input schema, rules, assessment
date, parsing, issue identity, severity, prompt, response contract, provider
configuration, approval, or output.

Do not change expected results merely because implementation changed. A gold
change requires a documented requirement change, owner approval, version
change, and review of prior evidence.
```

## Now recreate it yourself

Evaluate the different capstone result:

### Recreation 1 — Copy and prove the exact Module 4 result

This copy has a provenance record. **Provenance** means evidence of exactly
where a file came from. The record stores the precise Module 4 run locator,
portable project-relative source and destination paths, and both SHA-256
fingerprints. It does not store your Windows username or absolute computer
path.

```powershell
if (-not (Get-Variable -Name moduleFour -ErrorAction SilentlyContinue)) {
    throw 'Module paths are not loaded. Rerun Stage 1, then restart Recreation 1.'
}
$moduleFourWorkspace = Join-Path $moduleFour 'worked'
function Get-SavedCourseRunLocator {
    param([string]$Workspace)
    $latest = Join-Path $Workspace 'latest_run.txt'
    if (-not (Test-Path -LiteralPath $latest -PathType Leaf)) {
        throw 'Module 4 worked-run locator is missing or is not a file. Return to Module 4 Stage 4.'
    }
    $locatorLines = @(Get-Content -LiteralPath $latest)
    if ($locatorLines.Count -ne 1) {
        throw 'Module 4 worked-run locator must contain exactly one line.'
    }
    $locator = [string]$locatorLines[0]
    if ([string]::IsNullOrWhiteSpace($locator) -or
        $locator -cne $locator.Trim() -or
        [System.IO.Path]::IsPathRooted($locator) -or
        $locator -cnotmatch '^runs[\\/]RUN-[A-F0-9]{12}$') {
        throw 'Module 4 worked-run locator is empty or unsafe.'
    }
    return $locator
}
function Resolve-SavedCourseRun {
    param([string]$Workspace)
    $locator = Get-SavedCourseRunLocator $Workspace
    $runDir = Join-Path $Workspace $locator
    if (-not (Test-Path -LiteralPath $runDir -PathType Container)) {
        throw 'The saved Module 4 worked-run folder is missing.'
    }
    $runsRoot = (Resolve-Path -LiteralPath (Join-Path $Workspace 'runs')).Path
    $resolvedRunDir = (Resolve-Path -LiteralPath $runDir).Path
    if ((Split-Path -Parent $resolvedRunDir) -ne $runsRoot) {
        throw 'The saved Module 4 run resolves outside its exact runs folder.'
    }
    return $resolvedRunDir
}
$moduleFourRunLocator = Get-SavedCourseRunLocator $moduleFourWorkspace
$moduleFourRunDir = Resolve-SavedCourseRun $moduleFourWorkspace
$generatedIssues = Join-Path $moduleFourRunDir 'issues\issues.csv'
if (-not (Test-Path -LiteralPath $generatedIssues)) {
    throw 'The Module 4 generated issues file is missing. Rerun Module 4 Stage 4.'
}
$generatedSourceHash = (Get-FileHash -LiteralPath $generatedIssues -Algorithm SHA256).Hash
$generatedDestination = Join-Path $moduleFolder 'recreated_found.csv'
$sourceProjectRelative = Join-Path 'evidence\module-04\worked' `
    (Join-Path $moduleFourRunLocator 'issues\issues.csv')
$destinationProjectRelative = 'evidence\module-08\recreated_found.csv'
$provenancePath = Join-Path $moduleFolder 'recreated_module4_provenance.json'
$controlledExpectedSource = Join-Path $courseRoot 'practice_data\expected_issues.csv'
$recreatedExpectedDestination = Join-Path $moduleFolder 'recreated_expected.csv'
Copy-NewPracticeFile $controlledExpectedSource $recreatedExpectedDestination
if (-not (Test-Path -LiteralPath $controlledExpectedSource -PathType Leaf) -or
    -not (Test-Path -LiteralPath $recreatedExpectedDestination -PathType Leaf)) {
    throw 'SAFE STOP: the controlled or recreated expected-issues file is missing.'
}
$controlledExpectedHash = (
    Get-FileHash -LiteralPath $controlledExpectedSource -Algorithm SHA256
).Hash
$recreatedExpectedHash = (
    Get-FileHash -LiteralPath $recreatedExpectedDestination -Algorithm SHA256
).Hash
if ($controlledExpectedHash -ne $recreatedExpectedHash) {
    throw 'SAFE STOP: recreated_expected.csv does not match the controlled course answer key. Preserve it and follow the numbered mismatch-recovery steps below.'
}
Write-Host 'Verified: recreated_expected.csv exactly matches the controlled course answer key.'
if (Test-Path -LiteralPath $generatedDestination) {
    $existingDestinationHash = (
        Get-FileHash -LiteralPath $generatedDestination -Algorithm SHA256
    ).Hash
    if ($existingDestinationHash -ne $generatedSourceHash) {
        throw 'SAFE STOP: recreated_found.csv exists but does not match the exact Module 4 source. Preserve it and follow the numbered mismatch-recovery steps below.'
    }
    Write-Host 'Resume: recreated_found.csv already matches the exact Module 4 source.'
} else {
    Copy-Item -LiteralPath $generatedIssues -Destination $generatedDestination
}
$generatedDestinationHash = (
    Get-FileHash -LiteralPath $generatedDestination -Algorithm SHA256
).Hash
if ($generatedDestinationHash -ne $generatedSourceHash) {
    throw 'SAFE STOP: the Module 4 source and Module 8 destination hashes differ.'
}
$provenance = [ordered]@{
    source_module = 'Module 4 worked run'
    module4_run_locator = $moduleFourRunLocator
    source_project_relative = $sourceProjectRelative
    source_sha256 = $generatedSourceHash
    destination_project_relative = $destinationProjectRelative
    destination_sha256 = $generatedDestinationHash
}
if (Test-Path -LiteralPath $provenancePath) {
    try {
        $existingProvenance = Get-Content -Raw -LiteralPath $provenancePath |
            ConvertFrom-Json
    } catch {
        throw 'SAFE STOP: the existing provenance record cannot be read. Preserve it and follow the numbered mismatch-recovery steps below.'
    }
    if (
        $existingProvenance.module4_run_locator -ne $provenance.module4_run_locator -or
        $existingProvenance.source_project_relative -ne $provenance.source_project_relative -or
        $existingProvenance.destination_project_relative -ne $provenance.destination_project_relative -or
        $existingProvenance.source_sha256 -ne $provenance.source_sha256 -or
        $existingProvenance.destination_sha256 -ne $provenance.destination_sha256
    ) {
        throw 'SAFE STOP: the existing provenance record describes different evidence. Preserve it and follow the numbered mismatch-recovery steps below.'
    }
    Write-Host 'Resume: the existing provenance record still matches both files.'
} else {
    [System.IO.File]::WriteAllText(
        $provenancePath,
        ($provenance | ConvertTo-Json),
        $utf8NoBom
    )
}
Copy-NewPracticeFile .\evaluate_worked.py .\evaluate_recreated.py
Get-Content -LiteralPath $provenancePath
$recreatedEvaluatorNeedsEdit = Select-String -LiteralPath `
    .\evaluate_recreated.py `
    -Pattern 'worked_expected.csv','worked_found.csv','worked_metrics.json' `
    -Quiet
if ($recreatedEvaluatorNeedsEdit) {
    notepad .\evaluate_recreated.py
} else {
    Write-Host 'SKIP EDIT: evaluate_recreated.py already uses recreated names.'
}
```

The two hashes in `recreated_module4_provenance.json` must be identical. If a
`SAFE STOP` reports a mismatch, do not delete or overwrite either file. Run
this preservation block once, then rerun all of Recreation 1:

```powershell
if (-not (Get-Command Move-ToNumberedPreservedFile -ErrorAction SilentlyContinue)) {
    throw 'Preservation helper is not loaded. Rerun Stage 1 before recovery.'
}
Move-ToNumberedPreservedFile -Path (Join-Path $moduleFolder 'recreated_found.csv')
Move-ToNumberedPreservedFile -Path (Join-Path $moduleFolder 'recreated_expected.csv')
Move-ToNumberedPreservedFile -Path (
    Join-Path $moduleFolder 'recreated_module4_provenance.json'
)
```

This creates numbered preserved files and never replaces an earlier attempt.
Do not continue to the calculation until Recreation 1 completes without a safe
stop.

Change the three file-name constants to the recreated names and save, but do
not run the evaluator yet.

Before seeing the recreated metric result, lock the decision thresholds. This
separates a real precommitted gate from a target written after the answer is
known. Run:

```powershell
if (-not (Get-Variable -Name moduleTwoBrief -ErrorAction SilentlyContinue)) {
    throw 'Module 2 path is not loaded. Rerun Stage 1 before locking thresholds.'
}
if (-not (Test-Path -LiteralPath $moduleTwoBrief -PathType Leaf)) {
    throw 'The Module 2 recreated opportunity brief is missing. Return to Module 2.'
}
$moduleTwoBriefHash = (
    Get-FileHash -LiteralPath $moduleTwoBrief -Algorithm SHA256
).Hash
Start-NewPracticeTextFile `
    -Path .\recreated_precommitted_thresholds.md `
    -RequiredPatterns `
        '# Recreated precommitted thresholds', `
        'THRESHOLDS LOCKED BEFORE METRICS', `
        $moduleTwoBriefHash
notepad $moduleTwoBrief
$moduleTwoBriefHash
```

If the helper created a new file, paste and complete this record before
running `evaluate_recreated.py`. Copy the displayed Module 2 hash exactly. If
an incomplete record existed, it was preserved under a numbered name. On
`SKIP CREATE`, do not rewrite the locked thresholds.

```markdown
# Recreated precommitted thresholds

- Recorded before executing evaluate_recreated.py: YES
- Source provisional-threshold path: evidence/module-02/recreated_opportunity_brief.md
- Source Module 2 SHA-256: REPLACE WITH DISPLAYED HASH
- Precision: 100%
- Recall: 100%
- High-severity recall: 100%
- Severity mismatches: 0
- Supported summary statements: 100%
- External actions: 0
- Manual fallback drill: PASS
- Five-task usability record: all tasks attempted; every defect remains visible
- Decision rule: any missed quality, support, external-action, or fallback gate requires REWORK or DO NOT CONTINUE
- Completion marker: THRESHOLDS LOCKED BEFORE METRICS
```

Save and close the record. Then run this gate and the evaluator. This block
recomputes the Module 2 hash itself, so it is also safe to rerun after closing
and reopening PowerShell:

```powershell
if (-not (Get-Variable -Name moduleTwoBrief -ErrorAction SilentlyContinue)) {
    throw 'Module 2 path is not loaded. Rerun Stage 1 before the threshold gate.'
}
if (-not (Test-Path -LiteralPath $moduleTwoBrief -PathType Leaf)) {
    throw 'The Module 2 recreated opportunity brief is missing. Return to Module 2.'
}
$moduleTwoBriefHash = (
    Get-FileHash -LiteralPath $moduleTwoBrief -Algorithm SHA256
).Hash
$thresholdPath = Join-Path $moduleFolder 'recreated_precommitted_thresholds.md'
if (-not (Test-Path -LiteralPath $thresholdPath -PathType Leaf)) {
    throw 'The precommitted threshold record is missing. Create and complete it before running the evaluator.'
}
$thresholdText = Get-Content -Raw -LiteralPath $thresholdPath
if ($null -eq $thresholdText) { $thresholdText = '' }
$requiredThresholdText = @(
    'Recorded before executing evaluate_recreated.py: YES',
    'Precision: 100%',
    'Recall: 100%',
    'High-severity recall: 100%',
    'Severity mismatches: 0',
    'Supported summary statements: 100%',
    'External actions: 0',
    'Manual fallback drill: PASS',
    'THRESHOLDS LOCKED BEFORE METRICS',
    $moduleTwoBriefHash
)
$missingThresholdText = @($requiredThresholdText | Where-Object {
    -not $thresholdText.Contains($_)
})
if ($missingThresholdText.Count -ne 0) {
    $missingThresholdText
    throw 'Precommitted thresholds are incomplete. Do not run the evaluator.'
}
Get-FileHash -LiteralPath $thresholdPath -Algorithm SHA256
& $pythonExe .\evaluate_recreated.py
```

**Expected result:** 13 expected, 13 found, precision 1.0, recall 1.0,
high-severity recall 1.0, no false positives, no false negatives, and no
severity mismatches.

### Recreation 2 — Measure matched manual and assisted work

First locate the exact earlier evidence. The Module 1 record is a historical
baseline. The Module 3 evidence is the exact learner-created data-and-rules
record used for the manual and assisted checks. Module 5 contains the
statement-level support review; Module 6 contains the exact summary and human
decision for the 13-issue package.

Run this locator block immediately before the first timing attempt and rerun it
after every session break, before any restarted manual or assisted timer:

```powershell
if (-not (Get-Variable -Name moduleThreeRules -ErrorAction SilentlyContinue)) {
    throw 'Earlier evidence paths are not loaded. Rerun Stage 1 first.'
}
$matchedEvidence = @(
    $moduleOneBaseline,
    $moduleThreeRules,
    $moduleFiveSupport,
    $moduleSixSummary,
    $moduleSixDecision
)
$missingMatchedEvidence = @($matchedEvidence | Where-Object {
    -not (Test-Path -LiteralPath $_)
})
if ($missingMatchedEvidence.Count -ne 0) {
    $missingMatchedEvidence
    throw 'Matched timing evidence is missing. Return to the named earlier module.'
}
Get-Item -LiteralPath $matchedEvidence
```

Open `baseline_and_value_record.md`. Record its path, measured time, and task
boundary in a new file called `recreated_matched_timing.md`. It proves what you
measured in Module 1, but it is **not** the matched manual result unless its
task included the same complete attention package and review decision. The
steps below deliberately make the comparison equivalent.

Create the two learner files once, before starting the timer:

```powershell
Start-NewPracticeTextFile -Path .\recreated_manual_attention_package.md
Start-NewPracticeTextFile -Path .\recreated_matched_timing.md
```

If either command says `SKIP CREATE`, inspect that file before timing. A
complete prior measurement is reused, not overwritten. An incomplete file from
an interrupted timer is invalid; follow the recovery procedure below rather
than continuing its elapsed time. Close the empty manual-package window before
starting; the timed block reopens it. You may record only the historical Module
1 boundary in the timing file before the timer starts.

Perform the manual measurement:

1. Close unrelated windows and prepare a phone timer or the PowerShell
   stopwatch below.
2. Do not open `recreated_expected.csv`, `recreated_found.csv`, or prior
   summary/decision evidence during this manual run.
3. Start immediately before opening the frozen 15-row source and the exact
   Module 3 data-and-rules evidence.
4. Manually create `recreated_manual_attention_package.md`. Record every issue
   identity, its source row and rule, a short source-linked summary, only
   human-review actions, and a review decision.
5. Recheck every issue, statement, and action; save the decision; then stop.

```powershell
$manualTimer = [System.Diagnostics.Stopwatch]::StartNew()
notepad (Join-Path $projectRoot 'data\input\work_items.csv')
notepad $moduleThreeRules
notepad .\recreated_manual_attention_package.md
```

After saving and closing those files, run immediately:

```powershell
$manualTimer.Stop()
$manualMinutesObserved = [Math]::Round($manualTimer.Elapsed.TotalMinutes, 2)
$manualMinutesObserved
notepad .\recreated_matched_timing.md
```

Write the manual start boundary, stop boundary, time, row count, issue count,
reviewer role, corrections, final decision, and the exact Module 3
`evidence\module-03\recreated_data_and_rules.md` path in
`recreated_matched_timing.md`.

Now perform the assisted measurement on the same task:

1. Start immediately before opening the generated 13-issue package.
2. Check every issue in `recreated_found.csv` against the same source and exact
   Module 3 data-and-rules evidence.
3. Check every statement and action in the Module 6 summary, using the exact
   Module 5 support review as evidence.
4. Confirm the Module 6 decision and write your fresh result in
   `recreated_assisted_review.md`.
5. Save that review and stop immediately.

Create the fresh assisted-review file once before starting:

```powershell
Start-NewPracticeTextFile -Path .\recreated_assisted_review.md
```

Close the newly created empty review window. Then start the timer; the timed
block reopens it:

```powershell
$assistedTimer = [System.Diagnostics.Stopwatch]::StartNew()
notepad .\recreated_found.csv
notepad (Join-Path $projectRoot 'data\input\work_items.csv')
notepad $moduleThreeRules
notepad $moduleFiveSupport
notepad $moduleSixSummary
notepad $moduleSixDecision
notepad .\recreated_assisted_review.md
```

After saving and closing the fresh review, run:

```powershell
$assistedTimer.Stop()
$assistedMinutesObserved = [Math]::Round(
    $assistedTimer.Elapsed.TotalMinutes,
    2
)
$assistedMinutesObserved
notepad .\recreated_matched_timing.md
```

Record the assisted start boundary, stop boundary, time, row count, issue
count, Module 3 evidence path, statement/action checks, corrections, and review
decision beside the manual result. If the inputs, deliverable, or review depth
differed, label the comparison `NOT MATCHED` and repeat it; do not calculate a
saving from it.

#### If a timer is interrupted

An interrupted stopwatch, closed PowerShell window, computer restart, or
uncertain start/stop moment invalidates that attempt.

1. Rerun Stage 1 first. This restores the module folder and the
   `Move-ToNumberedPreservedFile` helper after a closed window or computer
   restart.
2. Open `recreated_matched_timing.md` and record `INVALID — INTERRUPTED`, which
   timer failed, and what happened.
3. Preserve only that timer's partial learner file. If the **manual** timer was
   interrupted, run:

```powershell
Move-ToNumberedPreservedFile -Path .\recreated_manual_attention_package.md
```

If the **assisted** timer was interrupted, run this instead:

```powershell
Move-ToNumberedPreservedFile -Path .\recreated_assisted_review.md
```

4. Rerun the complete earlier-evidence locator block at the start of
   Recreation 2.
5. Recreate the missing learner file with `Start-NewPracticeTextFile`.
6. Restart that timer from zero and repeat every step for that measurement.

Do not run both choices unless both timers were interrupted. The numbered
preserved file remains evidence of the interruption; the normal file name is
reserved for the fresh complete attempt.

### Recreation 3 — Calculate three complete cost scenarios

Run this calculator. Enter the two minutes recorded in
`recreated_matched_timing.md`. The example scenario assumptions are visible in
the code; change one only when you explain the new assumption in your decision
record.

```powershell
$costScenarioPath = Join-Path $moduleFolder 'recreated_cost_scenarios.csv'
$costScenarioComplete = $false
if (Test-Path -LiteralPath $costScenarioPath -PathType Leaf) {
    try {
        $existingCostRows = @(Import-Csv -LiteralPath $costScenarioPath)
        $requiredCostColumns = @(
            'scenario','runs_per_month','manual_hours','review_hours',
            'capacity_hours','manual_cost','review_cost','licence_usage_cost',
            'maintenance_cost','support_cost','training_cost','fallback_cost',
            'incident_cost','recurring_assisted_cost','recurring_difference',
            'one_time_setup_cost','first_month_difference'
        )
        $existingCostColumns = if ($existingCostRows.Count -gt 0) {
            @($existingCostRows[0].PSObject.Properties.Name)
        } else {
            @()
        }
        $numericCostColumns = @(
            'runs_per_month','manual_hours','review_hours','capacity_hours',
            'manual_cost','review_cost','licence_usage_cost',
            'maintenance_cost','support_cost','training_cost','fallback_cost',
            'incident_cost','recurring_assisted_cost','recurring_difference',
            'one_time_setup_cost','first_month_difference'
        )
        $negativeAllowed = @(
            'capacity_hours','recurring_difference','first_month_difference'
        )
        $strictlyPositive = @(
            'runs_per_month','manual_hours','review_hours'
        )
        $numericCellsComplete = $true
        foreach ($row in $existingCostRows) {
            foreach ($column in $numericCostColumns) {
                $cellText = [string]$row.$column
                $parsed = $false
                $parsedNumber = 0.0
                $numberCultures = @(
                    [System.Globalization.CultureInfo]::InvariantCulture,
                    [System.Globalization.CultureInfo]::CurrentCulture,
                    [System.Globalization.CultureInfo]::GetCultureInfo('nl-NL')
                )
                foreach ($numberCulture in $numberCultures) {
                    $parsedNumber = 0.0
                    if ([double]::TryParse(
                        $cellText,
                        [System.Globalization.NumberStyles]::Float,
                        $numberCulture,
                        [ref]$parsedNumber
                    )) {
                        $parsed = $true
                        break
                    }
                }
                if (
                    -not $parsed -or
                    [double]::IsNaN($parsedNumber) -or
                    [double]::IsInfinity($parsedNumber) -or
                    ($column -notin $negativeAllowed -and $parsedNumber -lt 0) -or
                    ($column -in $strictlyPositive -and $parsedNumber -le 0)
                ) {
                    $numericCellsComplete = $false
                }
            }
        }
        $costScenarioComplete = (
            $existingCostRows.Count -eq 3 -and
            @($existingCostRows.scenario | Sort-Object) -join ',' -eq
                'expected,high,low' -and
            @($requiredCostColumns | Where-Object {
                $_ -notin $existingCostColumns
            }).Count -eq 0 -and
            $numericCellsComplete
        )
    }
    catch {
        $costScenarioComplete = $false
    }
}
if ($costScenarioComplete) {
    Write-Host "SKIP CREATE: complete cost scenarios already exist at $costScenarioPath"
    $scenarioResults = $existingCostRows
    $scenarioResults | Format-Table -AutoSize
}
else {
    if (Test-Path -LiteralPath $costScenarioPath) {
        Move-ToNumberedPreservedFile -Path $costScenarioPath
    }
$manualMinutes = [double](Read-Host 'Enter matched manual minutes per run')
$assistedMinutes = [double](Read-Host 'Enter matched assisted minutes per run')
if ($manualMinutes -le 0 -or $assistedMinutes -le 0) {
    throw 'Both matched times must be greater than zero.'
}
$loadedHourlyRate = 45.0
$scenarioInputs = @(
    [PSCustomObject]@{
        scenario = 'low'; runs = 4; licence_usage = 5.0
        maintenance_hours = 0.5; support_hours = 0.25; training_hours = 0.25
        fallback_runs = 1; incident_hours = 0.25; setup_hours = 1
    },
    [PSCustomObject]@{
        scenario = 'expected'; runs = 8; licence_usage = 10.0
        maintenance_hours = 1; support_hours = 0.5; training_hours = 0.5
        fallback_runs = 1; incident_hours = 0.5; setup_hours = 2
    },
    [PSCustomObject]@{
        scenario = 'high'; runs = 16; licence_usage = 20.0
        maintenance_hours = 2; support_hours = 1; training_hours = 1
        fallback_runs = 2; incident_hours = 1; setup_hours = 4
    }
)
$scenarioResults = foreach ($item in $scenarioInputs) {
    $manualHours = $item.runs * $manualMinutes / 60
    $reviewHours = $item.runs * $assistedMinutes / 60
    $manualCost = $manualHours * $loadedHourlyRate
    $reviewCost = $reviewHours * $loadedHourlyRate
    $maintenanceCost = $item.maintenance_hours * $loadedHourlyRate
    $supportCost = $item.support_hours * $loadedHourlyRate
    $trainingCost = $item.training_hours * $loadedHourlyRate
    $fallbackCost = (
        $item.fallback_runs * $manualMinutes / 60 * $loadedHourlyRate
    )
    $incidentCost = $item.incident_hours * $loadedHourlyRate
    $setupCost = $item.setup_hours * $loadedHourlyRate
    $recurringAssistedCost = (
        $reviewCost + $item.licence_usage + $maintenanceCost +
        $supportCost + $trainingCost + $fallbackCost + $incidentCost
    )
    $recurringDifference = $manualCost - $recurringAssistedCost
    [PSCustomObject]@{
        scenario = $item.scenario
        runs_per_month = $item.runs
        manual_hours = [Math]::Round($manualHours, 2)
        review_hours = [Math]::Round($reviewHours, 2)
        capacity_hours = [Math]::Round($manualHours - $reviewHours, 2)
        manual_cost = [Math]::Round($manualCost, 2)
        review_cost = [Math]::Round($reviewCost, 2)
        licence_usage_cost = $item.licence_usage
        maintenance_cost = [Math]::Round($maintenanceCost, 2)
        support_cost = [Math]::Round($supportCost, 2)
        training_cost = [Math]::Round($trainingCost, 2)
        fallback_cost = [Math]::Round($fallbackCost, 2)
        incident_cost = [Math]::Round($incidentCost, 2)
        recurring_assisted_cost = [Math]::Round($recurringAssistedCost, 2)
        recurring_difference = [Math]::Round($recurringDifference, 2)
        one_time_setup_cost = [Math]::Round($setupCost, 2)
        first_month_difference = [Math]::Round(
            $recurringDifference - $setupCost,
            2
        )
    }
}
$scenarioResults | Format-Table -AutoSize
$scenarioResults | Export-Csv -NoTypeInformation -Encoding UTF8 `
    -LiteralPath $costScenarioPath
}
```

The formulas are:

- manual cost = runs × manual minutes / 60 × hourly rate;
- review cost = runs × assisted minutes / 60 × hourly rate;
- fallback cost = fallback runs × manual minutes / 60 × hourly rate;
- maintenance, support, training, incident, and setup cost = hours × hourly
  rate;
- recurring assisted cost = review + licence/usage + maintenance + support +
  training + fallback + incident;
- recurring difference = manual cost − recurring assisted cost;
- first-month difference = recurring difference − one-time setup.

Record all three rows, formulas, assumptions, and the warning `SCENARIOS — NOT
FORECASTS`. Capacity is not automatically cash saved, and unpriced risk must
remain visible as a limitation.

### Recreation 3A — Perform the five-task usability check

Use the current synthetic evidence and manual fallback. You are the course
learner acting in a separate tester role. This is self-testing, so record
`EXTERNAL UAT NOT VERIFIED`; Module 9 handles User Acceptance Testing.

Run:

```powershell
Start-NewPracticeTextFile `
    -Path .\recreated_usability_test.md `
    -RequiredPatterns `
        '# Recreated five-task usability test', `
        'EXTERNAL UAT NOT VERIFIED', `
        'Completion marker: USABILITY TEST COMPLETE'
```

If the helper created a new file, paste this table. If an incomplete attempt
existed, it was preserved under a numbered name. On `SKIP CREATE`, keep the
completed record unchanged.

```markdown
# Recreated five-task usability test

- Tester role: course learner acting as a separate tester
- Independence limitation: EXTERNAL UAT NOT VERIFIED

| Task | Expected result | Observed result | Help, error, and time | PASS or DEFECT | Evidence path |
|---|---|---|---|---|---|
| Find one issue's exact source row | correct row and raw value found | | | | |
| Find the rule behind that issue | exact rule code and rule evidence found | | | | |
| Distinguish severity from issue identity | severity explained without changing the issue key | | | | |
| Reject an unsupported draft statement | statement is rejected and not treated as evidence | | | | |
| Use the manual fallback | owner, source file, and next safe manual step found | | | | |

Defects and smallest correction:
Retest needed:
Effect on provisional decision:
Completion marker: REPLACE WITH USABILITY TEST COMPLETE AFTER ALL FIVE TASKS
```

Perform every task rather than predicting it. Record the observed result,
whether help was needed, any error, active time, `PASS` or `DEFECT`, and a
relative evidence path. Replace the completion placeholder only after all five
rows are filled. Any unresolved defect must remain visible and prevents an
unsupported positive recommendation.

### Recreation 4 — Complete the provisional decision

Copy the Course 1 final-decision worksheet. It is the same record listed in the
template catalogue; using it here prevents a different decision format from
appearing at the end:

```powershell
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\pilot_decision_record.md') .\recreated_evaluation_decision.md
notepad .\recreated_evaluation_decision.md
```

`Copy-NewPracticeFile` creates the worksheet only when it is absent. If it says
`SKIP COPY`, Notepad is opening your existing file only so you can continue
unfinished fields; do not paste a fresh template over it.

Set `Decision stage/status` to `PROVISIONAL PRE-UAT`. Mark the UAT,
training/adoption, and handover gates `NOT YET — MODULE 9`; do not invent a
pass. Complete every other relevant field. Include:

- the exact `recreated_precommitted_thresholds.md` path and SHA-256, proving
  the thresholds were locked before the recreated metrics;
- actual rule metrics;
- every Module 5 summary statement and its support decision;
- the exact Module 1 historical-baseline path and its measured boundary;
- the exact Module 3
  `evidence\module-03\recreated_data_and_rules.md` path used in both timed runs;
- the new matched manual and assisted boundaries and times, both including the
  same complete package and human review;
- the exact Module 5 support-review and Module 6 summary/decision paths;
- the completed low, expected, and high rows from
  `recreated_cost_scenarios.csv`, including their formulas;
- licence/usage, review, maintenance, support, training, fallback, and incident
  costs;
- one-time setup cost and any unpriced residual risk;
- the completed five-task `recreated_usability_test.md`, tester role,
  self-test limitation, observations, help/errors/time, defects, and evidence;
- limitations, including self-testing and synthetic data;
- exactly one **provisional recommendation**:
  `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or `DO NOT CONTINUE`.

At this stage, `ACCEPT FOR SYNTHETIC PORTFOLIO` means only that the measured
technical/value evidence supports carrying that recommendation into Module 9.
It does not yet permit even a completed portfolio claim. `REWORK` means record
and repair the gaps. `DO NOT CONTINUE` means preserve the evidence and prepare
an honest closure. Module 9 reassesses and finalises the label. Course 1 never
transitions to a client or live business implementation.

### Recreation 5 — Record regression control and verify

Create `recreated_regression_policy.md` using the capstone's actual change
triggers. Then verify:

```powershell
Start-NewPracticeTextFile -Path .\recreated_regression_policy.md
```

Complete the policy only when the helper created a new file. If it reports
`SKIP CREATE`, open the file only to continue genuinely incomplete content;
never replace a completed policy.

```powershell
Select-String -Path .\recreated_evaluation_decision.md -Pattern 'PROVISIONAL PRE-UAT','precision','recall','supported','synthetic','SCENARIOS — NOT FORECASTS','fallback','decision'
Select-String -Path .\recreated_precommitted_thresholds.md -Pattern 'THRESHOLDS LOCKED BEFORE METRICS','Precision: 100%','External actions: 0'
Select-String -Path .\recreated_usability_test.md -Pattern 'EXTERNAL UAT NOT VERIFIED','Find one issue','Use the manual fallback','Completion marker: USABILITY TEST COMPLETE'
Get-Content -LiteralPath .\recreated_module4_provenance.json
Import-Csv -LiteralPath .\recreated_cost_scenarios.csv |
    Format-Table scenario,review_cost,licence_usage_cost,maintenance_cost,support_cost,training_cost,fallback_cost,incident_cost,one_time_setup_cost
```

**Expected result:** the provisional status, precommitted gates, all five
usability tasks, and all decision evidence categories are found; provenance
shows identical source and destination hashes; and the cost table shows
exactly `low`, `expected`, and `high` with every named cost.

## Ask Codex to check your work

Run this read-only precheck. It reopens the provenance record, locates only the
one exact Module 4 source file, and confirms that its current hash still
matches the Module 8 copy:

```powershell
$moduleEightReviewFolder = (Resolve-Path -LiteralPath $moduleFolder).Path
$savedProvenance = Get-Content -Raw -LiteralPath `
    (Join-Path $moduleFolder 'recreated_module4_provenance.json') |
    ConvertFrom-Json
$exactModuleFourIssues = (
    Resolve-Path -LiteralPath (
        Join-Path $projectRoot $savedProvenance.source_project_relative
    )
).Path
$exactControlledExpected = (
    Resolve-Path -LiteralPath (
        Join-Path $courseRoot 'practice_data\expected_issues.csv'
    )
).Path
$exactModuleOneBaseline = (
    Resolve-Path -LiteralPath (
        Join-Path $projectRoot 'evidence\module-01\baseline_and_value_record.md'
    )
).Path
$exactModuleTwoBrief = (
    Resolve-Path -LiteralPath (
        Join-Path $projectRoot 'evidence\module-02\recreated_opportunity_brief.md'
    )
).Path
$exactModuleThreeRules = (
    Resolve-Path -LiteralPath (
        Join-Path $projectRoot 'evidence\module-03\recreated_data_and_rules.md'
    )
).Path
$exactModuleFiveSupport = (
    Resolve-Path -LiteralPath (
        Join-Path $projectRoot 'evidence\module-05\worked_support_review.md'
    )
).Path
$exactModuleSixSummary = (
    Resolve-Path -LiteralPath $moduleSixSummary
).Path
$exactModuleSixDecision = (
    Resolve-Path -LiteralPath $moduleSixDecision
).Path
$currentModuleTwoBriefHash = (
    Get-FileHash -LiteralPath $exactModuleTwoBrief -Algorithm SHA256
).Hash
$thresholdRecordPath = Join-Path $moduleFolder 'recreated_precommitted_thresholds.md'
$thresholdRecordText = Get-Content -Raw -LiteralPath $thresholdRecordPath
if (-not $thresholdRecordText.Contains(
    "Source Module 2 SHA-256: $currentModuleTwoBriefHash"
)) {
    throw 'SAFE STOP: the current Module 2 brief hash does not match the precommitted threshold record.'
}
$thresholdRecordHash = (
    Get-FileHash -LiteralPath $thresholdRecordPath -Algorithm SHA256
).Hash
$reviewSourceHash = (
    Get-FileHash -LiteralPath $exactModuleFourIssues -Algorithm SHA256
).Hash
$reviewDestinationHash = (
    Get-FileHash -LiteralPath `
        (Join-Path $moduleFolder 'recreated_found.csv') `
        -Algorithm SHA256
).Hash
$controlledExpectedReviewHash = (
    Get-FileHash -LiteralPath $exactControlledExpected -Algorithm SHA256
).Hash
$recreatedExpectedReviewHash = (
    Get-FileHash -LiteralPath `
        (Join-Path $moduleFolder 'recreated_expected.csv') `
        -Algorithm SHA256
).Hash
if (
    $reviewSourceHash -ne $savedProvenance.source_sha256 -or
    $reviewDestinationHash -ne $savedProvenance.destination_sha256 -or
    $reviewSourceHash -ne $reviewDestinationHash
) {
    throw 'SAFE STOP: source, provenance, and destination no longer match.'
}
if ($controlledExpectedReviewHash -ne $recreatedExpectedReviewHash) {
    throw 'SAFE STOP: the recreated answer key no longer matches the controlled course answer key.'
}
$moduleEightReviewFolder
$exactModuleFourIssues
$exactControlledExpected
$exactModuleOneBaseline
$exactModuleTwoBrief
$exactModuleThreeRules
$exactModuleFiveSupport
$exactModuleSixSummary
$exactModuleSixDecision
$thresholdRecordHash
```

The first nine outputs are full paths; the final output is the threshold
record's SHA-256 evidence. Copy the nine printed full paths into the nine
placeholders below. This
grants Codex access to one Module 8 folder, the one controlled course answer
key, and seven exact earlier evidence files—not
any earlier module folder or parent:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only these nine local paths:
1. this full Module 8 evidence folder:
[PASTE FULL MODULE 8 FOLDER PATH HERE]
2. this one exact Module 4 generated issues file:
[PASTE FULL MODULE 4 ISSUES FILE PATH HERE]
3. this one exact controlled Course 1 expected-issues answer key:
[PASTE FULL CONTROLLED EXPECTED-ISSUES FILE PATH HERE]
4. this one exact Module 1 baseline file:
[PASTE FULL MODULE 1 BASELINE FILE PATH HERE]
5. this one exact Module 2 opportunity brief:
[PASTE FULL MODULE 2 OPPORTUNITY BRIEF PATH HERE]
6. this one exact Module 3 data-and-rules evidence file:
[PASTE FULL MODULE 3 DATA-AND-RULES FILE PATH HERE]
7. this one exact Module 5 support-review file:
[PASTE FULL MODULE 5 SUPPORT-REVIEW FILE PATH HERE]
8. this one exact Module 6 summary file:
[PASTE FULL MODULE 6 SUMMARY FILE PATH HERE]
9. this one exact Module 6 decision file:
[PASTE FULL MODULE 6 DECISION FILE PATH HERE]

Learner attestation: I created these files for this fictional exercise and
have not knowingly put real client, employer, personal, medical, credential,
or secret data in them. This statement is an attestation, not proof.

You may use only read-only directory-listing, file-reading, and SHA-256 hashing
commands within exactly these nine paths. Do not create, edit, delete, rename,
move, or format anything. Do not run project scripts, workflows, or tests, and
do not use network or cloud commands. Do not inspect any parent, a sibling, or
another path. If apparent sensitive data is noticed, do not quote or repeat it:
return NOT YET with only the filename and general category, then stop. If none
is noticed, say that non-detection is not proof that none exists.

Return:
1. PASS or NOT YET;
2. checks for: the provenance record's exact Module 4 run locator and portable
project-relative source/destination paths with no username or absolute path;
the current source SHA-256; the Module 8 destination SHA-256; all three
hash records matching; the recreated expected-issues answer key exactly
matching the controlled course answer key; safe-stop instructions for a resume
mismatch; frozen
expected and found sets; unique keys; correct
true-positive/false-positive/false-negative arithmetic; precision and recall;
high-severity recall; severity match; statement-level support review; matched
manual and assisted task boundaries; both times including equivalent human
review; exact Module 1, Module 2, Module 3 data-and-rules, Module 5, and Module
6 evidence paths; Stage 1 requires the exact `COURSE_PROJECT.md` marker and
proves the resolved Git root equals the prescribed project folder before any
lesson write; the current Module 2 brief hash equals the source hash recorded
in `recreated_precommitted_thresholds.md`, and that threshold record's own
SHA-256 is reported; thresholds are locked before the evaluator runs; the
Module 3 file is used in both timed runs; exactly low, expected, and
high labelled cost scenarios; formulas; review, licence/usage, maintenance,
support, training, fallback, incident, and one-time setup costs; unpriced risk
visible; Stage 1 restores all later variables/helpers without opening or
overwriting evidence; guided and recreated text files use create-once/skip
instructions; an interrupted timer is marked invalid, its partial learner file
is preserved, and the timer restarts from zero; all five usability tasks with
expected and observed results, help/errors/time, pass/defect, evidence, tester
role, and self-test limitation; thresholds locked before metrics; quality
overriding attractive value; synthetic-portfolio-only boundary; regression
triggers; gold-change control; Decision stage/status exactly PROVISIONAL
PRE-UAT; UAT, adoption, and handover explicitly not yet verified; exactly one
permitted provisional recommendation with evidence;
3. the smallest corrections for me to make if NOT YET.

Remain read-only and do not recalculate by changing files.
```

## Pass criteria

- [ ] Worked arithmetic produces 0.75 precision and recall and leads to REWORK.
- [ ] Rerunning Stage 1 first verifies the exact `COURSE_PROJECT.md` marker and
      resolved Git root, then restores the course, project, module,
      earlier-evidence, Python, copy, text-creation, and preservation
      variables/helpers without opening or overwriting completed evidence.
- [ ] The worked example demonstrates exact equivalent manual and assisted
      timer boundaries before the recreation.
- [ ] The worked low/expected/high table shows formulas and review,
      licence/usage, maintenance, support, training, fallback, incident, and
      setup costs.
- [ ] `recreated_module4_provenance.json` records the exact Module 4 run
      locator, canonical project-relative source and destination, and matching
      SHA-256 values without a username or absolute computer path.
- [ ] An existing mismatched destination or provenance record safely stops;
      numbered preservation instructions do not overwrite the earlier attempt.
- [ ] `recreated_expected.csv` is a byte-for-byte SHA-256 match for the
      controlled `practice_data\expected_issues.csv` answer key on first run,
      resume, and the final read-only precheck.
- [ ] The read-only review records the learner's synthetic-data statement as
      an attestation rather than proof and says non-detection is not proof of
      absence.
- [ ] Recreated arithmetic reports all 13 expected keys correctly.
- [ ] `recreated_precommitted_thresholds.md` records the Module 2 brief path
      and hash and locks exact quality, support, fallback, and zero-action gates
      before `evaluate_recreated.py` is executed.
- [ ] Summary support is scored statement by statement.
- [ ] Module 1 historical evidence, the exact Module 3
      `recreated_data_and_rules.md`, and exact Module 5 support-review and
      Module 6 summary/decision paths are recorded.
- [ ] The newly timed manual and assisted runs use the same input, rules,
      deliverable, reviewer depth, and start/stop boundaries and include review.
- [ ] An interrupted timer is recorded as invalid; its partial learner file is
      preserved under a numbered name; the evidence locator is rerun; and that
      timer restarts from zero.
- [ ] Low, expected, and high cost/value figures are labelled scenarios, not
      forecasts, and preserve their formulas and assumptions.
- [ ] Review, support, maintenance, training, fallback, and incident costs are
      included.
- [ ] Licence/usage and one-time setup costs are included; unpriced residual
      risk is visible rather than treated as zero.
- [ ] All five usability tasks record expected and observed results,
      help/errors/time, pass or defect, evidence paths, tester role, and
      `EXTERNAL UAT NOT VERIFIED`.
- [ ] The provisional recommendation follows thresholds, not enthusiasm.
- [ ] Decision status is `PROVISIONAL PRE-UAT`; UAT, adoption, and handover are
      explicitly not yet verified.
- [ ] The provisional recommendation is exactly
      `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or `DO NOT CONTINUE`; every
      outcome can pass when evidence-backed.
- [ ] Regression and gold-change policies are explicit.
- [ ] Codex returns `PASS` read-only.

### Record your Module 8 PASS in Git

Do this only after Codex returns `PASS`. Rerun the complete Stage 1 block first,
even if this PowerShell window is still open. Stop if its project-marker or
Git-root guard fails. Then run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-08"
git commit --only -m "complete module 8 evidence" -- "evidence/module-08"
git status --short
```

`git commit --only` restricts this checkpoint to the repeated module path,
even if a different file had already been staged. If Git reports
`nothing to commit`, confirm that the module evidence was already recorded and
unchanged. Never add secrets, real data, or unrelated files.

## Consultant lens

Value claims require a baseline, a denominator, tested quality, full costs, and
limits. A demo that saves time while missing issues is not a successful
implementation.

## Capstone increment

The capstone has frozen metrics, summary support scoring, time and cost
scenarios, usability evidence, a bounded provisional pre-UAT recommendation,
and regression policy.

## Required artifact

The teaching contract creates worked and recreated datasets, metric reports,
evaluation decisions, and regression policies under `evidence/module-08`.

## Test gate

The **Pass criteria** are the complete gate.

## Stop or rework

Stop when expected results change after seeing output, denominators are hidden,
review time is omitted, savings are presented as guaranteed, quality gates are
overridden, or synthetic evidence is used to claim production readiness.

## Common failures

- Reporting only “accuracy.”
- Ignoring false negatives.
- Comparing an easy assisted case with a hard manual case.
- Treating time capacity as cash.
- Letting one perfect run replace regression policy.

## Estimated time

8–12 hours.
