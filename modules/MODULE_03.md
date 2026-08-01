# Module 3 — Understand the Data and Rules

## Outcome

You will create a data dictionary, deterministic rule register, issue-output
contract, rule order, and frozen expected-result comparison before writing a
workflow.

## Beginner checkpoint

Start when Module 2 passes and its evidence is committed with **Git**, a
version-control tool that records file changes, in the one project repository
created during Windows Setup. A **repository** is a project folder whose changes
are tracked together. You need Foundations 3 and 6 and the supplied
`practice_data` folder. All data must remain synthetic. Foundations remain in
`Documents\controlled-ai-course-practice`; Modules 1–9 do not.

Python is the programming language whose official documentation is linked
below.

## Concepts

- A **schema** describes expected fields and structural constraints.
- A **data dictionary** explains what every field means.
- A **raw value** is exactly what arrived; a **normalised value** is a
  controlled representation created after validation.
- A **deterministic rule** returns the same result for the same input and
  configuration.
- A **cross-field rule** uses more than one field.
- A **rule dependency** prevents a later check from using invalid input.
- A **gold set** is a frozen expected answer used for testing.
- A **true positive** is an expected issue found; a **false positive** is an
  extra issue; a **false negative** is a missed issue.
- **Provenance** links an output to its source row, field, value, and rule.
- **Secure Hash Algorithm 256-bit (SHA-256)** creates a repeatable digital
  fingerprint of exact file bytes; the later command spells the option
  `SHA256`.

## Official readings

Comma-separated values (CSV) is a plain-text table format, not an Excel
workbook. Microsoft Excel is a spreadsheet application that can silently
reinterpret dates or identifiers when opening CSV. The General Data Protection
Regulation (GDPR), called the Algemene verordening gegevensbescherming (AVG) in
Dutch, governs personal-data processing.

1. [Python documentation: CSV file reading and writing](https://docs.python.org/3/library/csv.html)
2. [European Commission: GDPR processing principles](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en)
3. [European Commission: data protection by design and by default](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations/what-does-data-protection-design-and-default-mean_en)

## Guided build

First solve a four-row contract completely. Then recreate the method for the
different 15-row Course 1 fixture.

Artificial intelligence (AI) is excluded from rule decisions in this module.
Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files. EUR is the
three-letter currency code for the euro.

Markdown is a plain-text format for headings, lists, and tables; `.md` is its
file name ending.

## Start or resume safely

At the start of every study session, rerun Stage 1. A closed PowerShell window
forgets `$projectRoot` and `$moduleFolder`; it does not remove your evidence.
Stage 1 restores those paths. The recreation copy step below checks for
existing destinations and leaves them unchanged, so restarting cannot silently
replace your work.

Suggested sessions:

Use ten focused blocks, each no longer than 60 minutes; most should take
45–60 minutes. Do not merge blocks. The ten-block plan remains within the
published 8–10-hour author estimate because reading and recovery speed vary.

- **UNDERSTAND** means you must explain field meaning, blank behavior, rule
  dependency, boundary, expected issue, or evidence link in your own words.
- **PROTECTED PLUMBING — RUN AND OBSERVE** means you may run supplied
  path/copy/hash and matrix-checker commands without memorising their syntax.
  You must know what they protect, inspect the output, and stop on a failure.

1. **PROTECTED PLUMBING — RUN AND OBSERVE:** run Stage 1, verify the project
   boundary, and create the four-row worked files without overwriting evidence.
2. **UNDERSTAND:** study the complete worked contract in Stage 2, including
   dictionary, rules, dependencies, provenance, and frozen expected issues.
3. **UNDERSTAND:** perform the Stage 3 boundary case and Stage 4 template
   mapping; explain zero versus blank and invalid-date skip behavior.
4. **PROTECTED PLUMBING — RUN AND OBSERVE:** copy and hash-check the different
   15-row source, answer key, requirements, and quality template.
5. **UNDERSTAND:** write the 12-field dictionary and R001–R005 conditions,
   dependencies, evidence, blank behavior, and examples.
6. **UNDERSTAND:** finish R006–R011, rule order, issue contract, all 13 expected
   triples, and the data-minimisation decision.
7. **UNDERSTAND + PROTECTED PLUMBING:** create matrix rows R001–R004 and run
   the supplied `x`-case failure/corrected-R003 retest lab; preserve both logs.
8. **UNDERSTAND:** complete bounded matrix rows R005–R008 with your own
   `because` reasons and row explanations.
9. **UNDERSTAND + PROTECTED PLUMBING:** finish R009–R011, run the 11-row
   checker, verify source hashes/counts, and complete the quality record.
10. **UNDERSTAND + PROTECTED PLUMBING:** run the bounded Codex semantic review,
    make your own corrections, rerun the matrix and evidence gates, and use
    only the supplied Module 3 Git checkpoint commands.

Before stopping, save every file and record the last completed numbered step.
Rerun Stage 1 in the next PowerShell window; never rebuild the folder from
memory.

## Follow along — I show you exactly how

### Stage 1 — Open the project evidence folder and create the mini-dataset

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
    throw 'Course project marker missing. Do not enter or change this folder.'
}
$actualMarker = (Get-Content -Raw -LiteralPath $projectMarker) -replace "`r`n", "`n"
if ($actualMarker -ne ($expectedMarker -replace "`r`n", "`n")) {
    throw 'Course project marker is unfamiliar. Do not enter or change this folder.'
}
$savedGitRoot = git -C $projectRoot rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0 -or
    (Resolve-Path -LiteralPath $savedGitRoot).Path -ne
    (Resolve-Path -LiteralPath $projectRoot).Path) {
    throw 'The marked Course 1 Git repository is missing or belongs to another folder.'
}
$moduleFolder = Join-Path $projectRoot 'evidence\module-03'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
(Get-Location).Path
function Open-CreateOnceCourseFile {
    param(
        [string]$Path,
        [string]$RecognizedStart,
        [string[]]$RequiredPatterns
    )
    if (Test-Path -LiteralPath $Path) {
        if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
            throw "Expected a lesson file but found another path type: $Path"
        }
        $content = Get-Content -Raw -LiteralPath $Path
        if ($null -eq $content) { $content = '' }
        $firstLine = Get-Content -LiteralPath $Path -TotalCount 1
        if (-not [string]::IsNullOrEmpty($content) -and
            $firstLine -cne $RecognizedStart) {
            throw "Existing file is unfamiliar. It was not opened or changed: $Path"
        }
        $complete = -not [string]::IsNullOrWhiteSpace($content)
        foreach ($pattern in $RequiredPatterns) {
            if (-not $content.Contains($pattern)) { $complete = $false }
        }
        if ($complete) {
            Write-Host "COMPLETE: keeping $Path unchanged."
            return
        }
        Write-Host 'INCOMPLETE: continue the recognised synthetic file without duplicating lines.'
    } else {
        New-Item -ItemType File -Path $Path | Out-Null
        Write-Host 'NEW: paste the supplied lesson content once.'
    }
    & notepad.exe $Path
}
Open-CreateOnceCourseFile `
    -Path (Join-Path $moduleFolder 'worked_jobs.csv') `
    -RecognizedStart 'job_id,status,due_date,amount,currency' `
    -RequiredPatterns @('J-204,in_progress,2026-07-24,90.00,')
```

The marker and Git-root checks are read-only and stop before any module file is
created unless this is the exact synthetic Course 1 project. The create-once
helper creates a missing worked file, reopens an empty or recognised incomplete
one, skips a complete one, and stops without opening a wrong-type or unfamiliar
file. Before every use, confirm the named file is synthetic lesson work.
Preserve an unfamiliar file and ask Codex for read-only diagnosis before a
clearly numbered retry. **Expected path:** it ends in
`\AI-workflow-learning\operations-exception-assistant\evidence\module-03`.
If the repository error appears, stop and complete Windows Setup; do not remove
the check.

International Organization for Standardization (ISO) date format uses
`YYYY-MM-DD`: year, month, then day. For `NEW`, paste, save, and close Notepad.
For `INCOMPLETE`, continue without duplicating existing rows. For `COMPLETE`,
move to the inspection:

```csv
job_id,status,due_date,amount,currency
J-201,new,2026-08-01,120.00,EUR
J-202,done,2026-07-20,40.00,EUR
J-203,waiting,20-07-2026,-5.00,EUR
J-204,in_progress,2026-07-24,90.00,
```

Inspect the raw table:

```powershell
$workedRows = Import-Csv .\worked_jobs.csv
$workedRows.Count
$workedRows[0].PSObject.Properties.Name
$workedRows | Format-Table
```

`Import-Csv` reads each row without editing the file. PowerShell represents
each imported row as an object. `PSObject.Properties.Name` asks that object for
the names of its fields—in this case, the five CSV headers. You do not need to
memorise the internal term `PSObject`.

**Expected result:** `4`, then the five headers, then four rows.

**Troubleshooting:**

- If the count is 0, confirm the header and rows were saved.
- If everything appears under one header, confirm commas separate values.
- Never correct the source row merely because it looks wrong.

### Stage 2 — Follow the complete contract

Run:

```powershell
Open-CreateOnceCourseFile `
    -Path (Join-Path $moduleFolder 'worked_data_and_rules.md') `
    -RecognizedStart '# Worked data and rules' `
    -RequiredPatterns @('## Frozen expected result','Expected total: 4','J-204')
```

For `NEW`, paste and save. For `INCOMPLETE`, add only the missing content. For
`COMPLETE`, do not paste the example again:

```markdown
# Worked data and rules

## Data dictionary

| Field | Meaning | Type/format | Requirement | Blank meaning |
|---|---|---|---|---|
| job_id | stable fictional job identifier | text | required and unique | invalid |
| status | current workflow state | text | new, in_progress, waiting, completed | invalid |
| due_date | target date | ISO date YYYY-MM-DD | required | invalid |
| amount | fictional amount | decimal text | zero or greater | invalid |
| currency | currency of amount | text | EUR when amount is populated | invalid here |

ISO means International Organization for Standardization. ISO date format puts
year, month, and day in the order YYYY-MM-DD.

## Rules

| Code | Exact condition | Severity | Dependency | Failure evidence |
|---|---|---|---|---|
| E001 | status is one of new, in_progress, waiting, completed | high | none | job_id, raw status |
| E002 | due_date is a real date written YYYY-MM-DD | high | none | job_id, raw due_date |
| E003 | amount parses as a decimal and is at least zero | high | none | job_id, raw amount |
| E004 | a populated amount has currency EUR | medium | amount is populated | job_id, raw currency |

## Rule order and failure behaviour

1. Preserve the raw row.
2. Check required structure.
3. Validate allowed values and formats.
4. Run dependent comparisons only on valid prerequisites.
5. Emit an evidence-linked issue; never repair the source silently.
6. Stop the run when the header changes.

## Issue output contract

Every issue contains job_id, field, raw_value, rule_code, severity, and a
factual message. It contains no invented cause or action.

## Frozen expected issues

| job_id | field | rule | severity | reason |
|---|---|---|---|---|
| J-202 | status | E001 | high | done is not allowed |
| J-203 | due_date | E002 | high | date is not YYYY-MM-DD |
| J-203 | amount | E003 | high | amount is negative |
| J-204 | currency | E004 | medium | amount is present but EUR is missing |

Expected total: 4. Valid row: J-201.

## Data minimisation

No name, email, address, customer, employee, or other personal field is needed.
Only the issue record, not every raw row, may enter a later AI summary step.
```

Verify that the rules predict the data:

```powershell
'waiting','new','waiting','completed' | Sort-Object -Unique
$workedRows | Group-Object status | Select-Object Name,Count
$workedRows | Select-Object job_id,status,due_date,amount,currency
Select-String -Path .\worked_data_and_rules.md -Pattern 'Expected total: 4','J-202','J-203','J-204'
```

`Sort-Object` sorts the incoming values. Its `-Unique` option keeps only one
copy of each value, so the repeated `waiting` appears once. The same pattern can
later show which rule codes are present in a longer file.

**Expected output:** `completed`, `new`, and `waiting` in sorted order; four
status groups; and matches for the total and three affected identifiers.

The important lesson is allocation: these exact checks belong in normal code,
not a language model.

### Stage 3 — Make and check one boundary case

Open the boundary file through the same guard:

```powershell
Open-CreateOnceCourseFile `
    -Path (Join-Path $moduleFolder 'worked_boundary.csv') `
    -RecognizedStart 'job_id,status,due_date,amount,currency' `
    -RequiredPatterns @('J-205,completed,2026-07-26,0,EUR')
```

For `NEW`, paste the row below. For `INCOMPLETE`, complete the recognised file
without duplicating the header. For `COMPLETE`, continue:

```csv
job_id,status,due_date,amount,currency
J-205,completed,2026-07-26,0,EUR
```

This row should pass all four worked rules: the allowed status is valid, the
date is valid, zero is not negative, and the amount has EUR.

Verify the raw value:

```powershell
Import-Csv .\worked_boundary.csv | Format-List
```

If you think zero means blank, return to Foundation 6. Zero is a supplied
number; blank is no supplied value.

### Stage 4 — See how the completed contract maps to the quality template

`worked_data_and_rules.md` contains the full worked reasoning. The reusable
**data dictionary and quality check** records the same decisions in a
consistent consulting format. Follow this smaller completed version before you
copy the blank template for the capstone.

Run:

```powershell
Open-CreateOnceCourseFile `
    -Path (Join-Path $moduleFolder 'worked_data_dictionary_and_quality_check.md') `
    -RecognizedStart '# Worked data dictionary and quality check' `
    -RequiredPatterns @('Expected issue count: 4','Known blind spot:')
```

For `NEW`, paste, save, and close. For `INCOMPLETE`, continue without
duplicating sections. For `COMPLETE`, move to the checks:

```markdown
# Worked data dictionary and quality check

- Artifact ID: WORKED-M03-DATA
- Version/date: 1.0 / 2026-07-28
- Dataset: worked_jobs.csv
- Status: FICTIONAL
- Unit: one fictional job
- Expected rows: 4
- Unique identifier: job_id
- Source correction: never automatic

## Field and quality examples

| Field | Meaning and blank | Exact quality check | Result |
|---|---|---|---|
| job_id | stable identifier; blank invalid | required and unique | no issue in worked rows |
| status | workflow state; blank invalid | allowed value | J-202 fails |
| due_date | target date; blank invalid | real YYYY-MM-DD date | J-203 fails |
| amount/currency | amount and its currency; blank currency invalid here | non-negative amount and EUR present | J-203 and J-204 fail |

Expected issue count: 4. Known blind spot: this check cannot decide why a
value is wrong. Decision: ACCEPT FOR SYNTHETIC TEST.
```

Check it:

```powershell
Get-Item .\worked_data_dictionary_and_quality_check.md
Select-String -Path .\worked_data_dictionary_and_quality_check.md -Pattern 'FICTIONAL','never automatic','Expected issue count: 4','Known blind spot'
```

**Expected result:** the file exists and all four concepts are found. If a
concept is missing, compare the pasted file with the completed example and
correct it yourself.

## Now recreate it yourself

Use the different Course 1 fixture and rule set:

1. Run:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$sourceData = Join-Path $courseRoot 'practice_data\work_items.csv'
$sourceGold = Join-Path $courseRoot 'practice_data\expected_issues.csv'
$sourceReadme = Join-Path $courseRoot 'practice_data\README.md'
$qualityTemplate = Join-Path $courseRoot 'templates\data_dictionary_and_quality_check.md'
function Copy-NewPracticeFile {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$ExpectedHeading,
        [switch]$MustRemainExact
    )
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Controlled course source is missing or is not a file: $Source"
    }
    if (Test-Path -LiteralPath $Destination) {
        if (-not (Test-Path -LiteralPath $Destination -PathType Leaf)) {
            throw "Practice path exists but is not a file. Preserve it and stop: $Destination"
        }
        if ($MustRemainExact) {
            $sourceHash = (Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash
            $destinationHash = (Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash
            if ($sourceHash -ne $destinationHash) {
                throw "Controlled working copy changed. Preserve it and ask for read-only diagnosis: $Destination"
            }
        } elseif ((Get-Content -LiteralPath $Destination -TotalCount 1) -cne $ExpectedHeading) {
            throw "Existing learner file is unfamiliar. Preserve it and ask for read-only diagnosis: $Destination"
        }
        Write-Host "Resume: $Destination already exists and was left unchanged."
    } else {
        Copy-Item -LiteralPath $Source -Destination $Destination
        $sourceHash = (Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash
        $destinationHash = (Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash
        if ($sourceHash -ne $destinationHash) {
            throw "New practice copy did not match its source: $Destination"
        }
        Write-Host "Created: $Destination"
    }
}
Copy-NewPracticeFile $sourceData .\recreated_work_items.csv '' -MustRemainExact
Copy-NewPracticeFile $sourceGold .\recreated_expected_issues.csv '' -MustRemainExact
Copy-NewPracticeFile $sourceReadme .\recreated_requirements.md '' -MustRemainExact
Copy-NewPracticeFile $qualityTemplate .\data_dictionary_and_quality_check.md '# Data Dictionary and Quality Check'
Get-FileHash -LiteralPath $sourceData -Algorithm SHA256
Get-FileHash -LiteralPath .\recreated_work_items.csv -Algorithm SHA256
Get-Item .\data_dictionary_and_quality_check.md
notepad.exe .\data_dictionary_and_quality_check.md
```

The two hashes must match.

2. Read `recreated_requirements.md`.
3. Create or reopen `recreated_data_and_rules.md` with this safe-restart block:

```powershell
$rulesPath = Join-Path $moduleFolder 'recreated_data_and_rules.md'
if (Test-Path -LiteralPath $rulesPath) {
    if (-not (Test-Path -LiteralPath $rulesPath -PathType Leaf) -or
        (Get-Content -LiteralPath $rulesPath -TotalCount 1) -cne '# Recreated data and rules') {
        throw 'Existing data-and-rules file is the wrong type or is unfamiliar. Preserve it and ask for read-only diagnosis.'
    }
    Write-Host "Resume: $rulesPath already exists and was left unchanged."
} else {
    "# Recreated data and rules`r`n" |
        Set-Content -LiteralPath $rulesPath -Encoding utf8
    Write-Host "Created: $rulesPath"
}
notepad.exe $rulesPath
```

   Complete it yourself. Include:

- all 12 fields and their blank meanings;
- R001 through R011 with exact condition, field, severity, dependency, evidence,
  and requirement source;
- fixed assessment date `2026-07-26`;
- rule order and explicit skip behaviour for invalid dates;
- an issue contract containing `work_item_id`, `source_reference`, field, raw
  value, rule, severity, message, and assessment date;
- one valid, failing, blank/not-applicable, and boundary example per applicable
  rule;
- a manual map of all 13 expected `(work_item_id, rule_code, field)` triples;
- a data-minimisation decision.

4. Create the complete rule-example matrix. This separate comma-separated
   values (CSV) file makes it possible to prove that no rule or example category
   disappeared inside prose. It also includes a learner-written explanation;
   the deterministic check can enforce a bounded case, while the explanation
   and later Codex review check whether you understand it.

First study this one-row formatting example for an unrelated fictional rule.
It is a demonstration only; do not add `R900` to your capstone matrix:

```csv
rule_code,valid_example,failing_example,blank_or_not_applicable,boundary_example,learner_explanation
R900,"case=R900-V; field=temperature_c; value=20; expect=NO_ISSUE; because=20 is inside the permitted range","case=R900-F; field=temperature_c; value=31; expect=ISSUE; because=31 is above the permitted maximum","case=R900-B; field=temperature_c; value=<BLANK>; expect=SAFE_STOP; because=the required measurement is absent","case=R900-D; field=temperature_c; value=30|31; expect=NO_ISSUE|ISSUE; because=30 is the last permitted value and 31 is the first failing value","The valid and failing cases sit on different sides of the rule. Blank input cannot be compared safely, and the boundary pair proves the exact transition."
```

Each example cell uses exactly five labelled parts:

```text
case=[CASE ID]; field=[FIELD]; value=[VALUE]; expect=[OUTCOME]; because=[YOUR REASON]
```

The first four parts are a small machine-checkable contract. You write the
`because` sentence yourself. The final `learner_explanation` cell explains how
the valid, failing, blank/not-applicable, and boundary cases differ. Double
quotation marks keep each description inside one CSV cell. Your different
recreation uses the real requirements for R001–R011 rather than copying this
unrelated temperature example.

```powershell
$matrixPath = Join-Path $moduleFolder 'recreated_rule_example_matrix.csv'
$matrixHeader = 'rule_code,valid_example,failing_example,blank_or_not_applicable,boundary_example,learner_explanation'
if (Test-Path -LiteralPath $matrixPath) {
    if (-not (Test-Path -LiteralPath $matrixPath -PathType Leaf) -or
        (Get-Content -LiteralPath $matrixPath -TotalCount 1) -cne $matrixHeader) {
        throw 'Existing rule-example matrix is the wrong type or has an unfamiliar header. Preserve it and ask for read-only diagnosis.'
    }
    Write-Host "Resume: $matrixPath already exists and was left unchanged."
} else {
    $matrixHeader | Set-Content -LiteralPath $matrixPath -Encoding utf8
    Write-Host "Created: $matrixPath"
}
notepad.exe $matrixPath
```

Add exactly one row for every rule `R001` through `R011`. Each row must contain
all four categories and one explanation:

- a valid example that does not trigger that rule;
- a failing example that does trigger it;
- a blank example, or `NOT APPLICABLE —` followed by the rule-specific reason;
- an exact boundary example at, immediately below, or immediately above a
  numeric/date threshold; for a categorical or structural rule, use the
  nearest allowed-to-disallowed transition, such as an allowed status versus
  one value outside the set, one unique reference versus adding a second row
  with the same reference (which makes both rows issues), or a present versus
  blank required field, and explain why that transition is the boundary.

Do not write only “valid” or “fails.” Record the actual synthetic field and
value, expected outcome, and why.

Use the exact bounded case cores below. The vertical bar (`|`) in a value means
“compare the case on the left with the case on the right.” `R001_ISSUE` means
the blank is handled by the required-value rule instead of being silently
reclassified by a later rule. For each rule, use suffix `-V` for the valid
case, `-F` for failing, `-B` for blank/not-applicable, and `-D` for boundary.
For example, the four R005 case IDs are `R005-V`, `R005-F`, `R005-B`, and
`R005-D`. Use the field text printed beside each rule exactly.

| Rule | Valid value → expectation | Failing value → expectation | Blank or not-applicable value → expectation | Boundary value → expectation |
|---|---|---|---|---|
| R001 `title` | `Synthetic request` → `NO_ISSUE` | `<BLANK>` → `ISSUE` | `<BLANK>` → `ISSUE` | `A\|<BLANK>` → `NO_ISSUE\|ISSUE` |
| R002 `status` | `new` → `NO_ISSUE` | `paused` → `ISSUE` | `<BLANK>` → `R001_ISSUE` | `waiting\|paused` → `NO_ISSUE\|ISSUE` |
| R003 `priority` | `medium` → `NO_ISSUE` | `urgent` → `ISSUE` | `<BLANK>` → `R001_ISSUE` | `high\|urgent` → `NO_ISSUE\|ISSUE` |
| R004 `due_date` | `2026-07-26` → `NO_ISSUE` | `2026-02-30` → `ISSUE` | `<BLANK>` → `NO_ISSUE` | `2026-02-28\|2026-02-29` → `NO_ISSUE\|ISSUE` |
| R005 `received_date+due_date` | `received:2026-07-20+due:2026-07-20` → `NO_ISSUE` | `received:2026-07-20+due:2026-07-19` → `ISSUE` | `received:2026-07-20+due:<BLANK>` → `NOT_APPLICABLE` | `received:2026-07-20+due:2026-07-20\|received:2026-07-20+due:2026-07-19` → `NO_ISSUE\|ISSUE` |
| R006 `status+completed_date` | `completed+2026-07-20` → `NO_ISSUE` | `completed+<BLANK>` → `ISSUE` | `new+<BLANK>` → `NO_ISSUE` | `completed+2026-07-20\|completed+<BLANK>` → `NO_ISSUE\|ISSUE` |
| R007 `status+owner_role` | `waiting+operations_coordinator` → `NO_ISSUE` | `waiting+<BLANK>` → `ISSUE` | `cancelled+<BLANK>` → `NOT_APPLICABLE` | `new+<BLANK>\|in_progress+<BLANK>` → `NO_ISSUE\|ISSUE` |
| R008 `amount` | `0.00` → `NO_ISSUE` | `-0.01` → `ISSUE` | `<BLANK>` → `NO_ISSUE` | `0.00\|-0.01` → `NO_ISSUE\|ISSUE` |
| R009 `amount+currency` | `1.00+EUR` → `NO_ISSUE` | `1.00+USD` → `ISSUE` | `<BLANK>+<BLANK>` → `NOT_APPLICABLE` | `<BLANK>+<BLANK>\|0.00+<BLANK>` → `NOT_APPLICABLE\|ISSUE` |
| R010 `source_reference` | `REF-1001+REF-1002` → `NO_ISSUE` | `REF-1001+REF-1001` → `ISSUE_BOTH_ROWS` | `REF-1001+<BLANK>` → `R001_ISSUE` | `REF-1001\|REF-1001+REF-1001` → `NO_ISSUE\|ISSUE_BOTH_ROWS` |
| R011 `status+due_date+assessment_date` | `waiting+2026-07-26+2026-07-26` → `NO_ISSUE` | `waiting+2026-07-25+2026-07-26` → `ISSUE` | `waiting+<BLANK>+2026-07-26` → `NOT_APPLICABLE` | `waiting+2026-07-26+2026-07-26\|waiting+2026-07-25+2026-07-26` → `NO_ISSUE\|ISSUE` |

The protected checker below contains those same exact cores. You may run this
checker without memorising its implementation. You **must understand** that it
checks structure, rule-specific cases, outcomes, non-placeholder reasons, and
explanation coverage; it cannot decide whether your prose is genuinely sound.

Save and close Notepad, then run the complete block. It first proves the
checker rejects a supplied meaningless `x` row, then proves a corrected R003
row passes, saves both results, and finally checks your 11-row matrix:

```powershell
$requiredColumns = @(
    'rule_code',
    'valid_example',
    'failing_example',
    'blank_or_not_applicable',
    'boundary_example',
    'learner_explanation'
)
$exampleContracts = @{
    R001 = @{
        valid_example = 'case=R001-V; field=title; value=Synthetic request; expect=NO_ISSUE; because='
        failing_example = 'case=R001-F; field=title; value=<BLANK>; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R001-B; field=title; value=<BLANK>; expect=ISSUE; because='
        boundary_example = 'case=R001-D; field=title; value=A|<BLANK>; expect=NO_ISSUE|ISSUE; because='
    }
    R002 = @{
        valid_example = 'case=R002-V; field=status; value=new; expect=NO_ISSUE; because='
        failing_example = 'case=R002-F; field=status; value=paused; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R002-B; field=status; value=<BLANK>; expect=R001_ISSUE; because='
        boundary_example = 'case=R002-D; field=status; value=waiting|paused; expect=NO_ISSUE|ISSUE; because='
    }
    R003 = @{
        valid_example = 'case=R003-V; field=priority; value=medium; expect=NO_ISSUE; because='
        failing_example = 'case=R003-F; field=priority; value=urgent; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R003-B; field=priority; value=<BLANK>; expect=R001_ISSUE; because='
        boundary_example = 'case=R003-D; field=priority; value=high|urgent; expect=NO_ISSUE|ISSUE; because='
    }
    R004 = @{
        valid_example = 'case=R004-V; field=due_date; value=2026-07-26; expect=NO_ISSUE; because='
        failing_example = 'case=R004-F; field=due_date; value=2026-02-30; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R004-B; field=due_date; value=<BLANK>; expect=NO_ISSUE; because='
        boundary_example = 'case=R004-D; field=due_date; value=2026-02-28|2026-02-29; expect=NO_ISSUE|ISSUE; because='
    }
    R005 = @{
        valid_example = 'case=R005-V; field=received_date+due_date; value=received:2026-07-20+due:2026-07-20; expect=NO_ISSUE; because='
        failing_example = 'case=R005-F; field=received_date+due_date; value=received:2026-07-20+due:2026-07-19; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R005-B; field=received_date+due_date; value=received:2026-07-20+due:<BLANK>; expect=NOT_APPLICABLE; because='
        boundary_example = 'case=R005-D; field=received_date+due_date; value=received:2026-07-20+due:2026-07-20|received:2026-07-20+due:2026-07-19; expect=NO_ISSUE|ISSUE; because='
    }
    R006 = @{
        valid_example = 'case=R006-V; field=status+completed_date; value=completed+2026-07-20; expect=NO_ISSUE; because='
        failing_example = 'case=R006-F; field=status+completed_date; value=completed+<BLANK>; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R006-B; field=status+completed_date; value=new+<BLANK>; expect=NO_ISSUE; because='
        boundary_example = 'case=R006-D; field=status+completed_date; value=completed+2026-07-20|completed+<BLANK>; expect=NO_ISSUE|ISSUE; because='
    }
    R007 = @{
        valid_example = 'case=R007-V; field=status+owner_role; value=waiting+operations_coordinator; expect=NO_ISSUE; because='
        failing_example = 'case=R007-F; field=status+owner_role; value=waiting+<BLANK>; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R007-B; field=status+owner_role; value=cancelled+<BLANK>; expect=NOT_APPLICABLE; because='
        boundary_example = 'case=R007-D; field=status+owner_role; value=new+<BLANK>|in_progress+<BLANK>; expect=NO_ISSUE|ISSUE; because='
    }
    R008 = @{
        valid_example = 'case=R008-V; field=amount; value=0.00; expect=NO_ISSUE; because='
        failing_example = 'case=R008-F; field=amount; value=-0.01; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R008-B; field=amount; value=<BLANK>; expect=NO_ISSUE; because='
        boundary_example = 'case=R008-D; field=amount; value=0.00|-0.01; expect=NO_ISSUE|ISSUE; because='
    }
    R009 = @{
        valid_example = 'case=R009-V; field=amount+currency; value=1.00+EUR; expect=NO_ISSUE; because='
        failing_example = 'case=R009-F; field=amount+currency; value=1.00+USD; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R009-B; field=amount+currency; value=<BLANK>+<BLANK>; expect=NOT_APPLICABLE; because='
        boundary_example = 'case=R009-D; field=amount+currency; value=<BLANK>+<BLANK>|0.00+<BLANK>; expect=NOT_APPLICABLE|ISSUE; because='
    }
    R010 = @{
        valid_example = 'case=R010-V; field=source_reference; value=REF-1001+REF-1002; expect=NO_ISSUE; because='
        failing_example = 'case=R010-F; field=source_reference; value=REF-1001+REF-1001; expect=ISSUE_BOTH_ROWS; because='
        blank_or_not_applicable = 'case=R010-B; field=source_reference; value=REF-1001+<BLANK>; expect=R001_ISSUE; because='
        boundary_example = 'case=R010-D; field=source_reference; value=REF-1001|REF-1001+REF-1001; expect=NO_ISSUE|ISSUE_BOTH_ROWS; because='
    }
    R011 = @{
        valid_example = 'case=R011-V; field=status+due_date+assessment_date; value=waiting+2026-07-26+2026-07-26; expect=NO_ISSUE; because='
        failing_example = 'case=R011-F; field=status+due_date+assessment_date; value=waiting+2026-07-25+2026-07-26; expect=ISSUE; because='
        blank_or_not_applicable = 'case=R011-B; field=status+due_date+assessment_date; value=waiting+<BLANK>+2026-07-26; expect=NOT_APPLICABLE; because='
        boundary_example = 'case=R011-D; field=status+due_date+assessment_date; value=waiting+2026-07-26+2026-07-26|waiting+2026-07-25+2026-07-26; expect=NO_ISSUE|ISSUE; because='
    }
}
$ruleExplanationTerms = @{
    R001 = @('required','blank')
    R002 = @('status','allowed')
    R003 = @('priority','allowed')
    R004 = @('date','format')
    R005 = @('due','received')
    R006 = @('completed','completion')
    R007 = @('owner','status')
    R008 = @('amount','negative')
    R009 = @('currency','eur')
    R010 = @('reference','duplicate')
    R011 = @('assessment','overdue')
}
function Test-RuleExampleMatrix {
    param(
        [Parameter(Mandatory)]
        [string]$Path,
        [string[]]$ExpectedCodes = @(1..11 | ForEach-Object {
            'R{0:D3}' -f $_
        })
    )
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Matrix file is missing: $Path"
    }
    $matrix = @(Import-Csv -LiteralPath $Path)
    if ($matrix.Count -ne $ExpectedCodes.Count) {
        throw "Expected exactly $($ExpectedCodes.Count) rule rows; observed $($matrix.Count)."
    }
    $actualColumns = @($matrix[0].PSObject.Properties.Name)
    if (($actualColumns -join '|') -cne ($requiredColumns -join '|')) {
        throw 'The rule-example matrix header or column order is incomplete or changed.'
    }
    $actualCodes = @($matrix.rule_code)
    if ($actualCodes.Count -ne @($actualCodes | Sort-Object -Unique).Count -or
        @(Compare-Object ($ExpectedCodes | Sort-Object) ($actualCodes | Sort-Object)).Count -ne 0) {
        throw "The matrix must cover only these rule codes, each once: $($ExpectedCodes -join ', ')."
    }
    foreach ($row in $matrix) {
        $code = [string]$row.rule_code
        foreach ($column in @(
            'valid_example',
            'failing_example',
            'blank_or_not_applicable',
            'boundary_example'
        )) {
            $cell = [string]$row.$column
            $prefix = [string]$exampleContracts[$code][$column]
            if (-not $cell.StartsWith(
                $prefix,
                [System.StringComparison]::Ordinal
            )) {
                throw "$code $column must start with its exact bounded case, field, value, and expectation contract."
            }
            $reason = $cell.Substring($prefix.Length).Trim()
            if ($reason.Length -lt 20 -or
                $reason -notmatch '\s' -or
                $reason -match '^(?i:x+|n/?a|valid|fails?|todo|tbd|test|example|placeholder)[.! ]*$') {
                throw "$code $column needs a learner-written reason of at least 20 meaningful characters."
            }
        }
        $explanation = [string]$row.learner_explanation
        if ($explanation.Trim().Length -lt 100) {
            throw "$code learner_explanation must contain at least 100 characters in the learner's own words."
        }
        foreach ($pattern in @(
            '(?i)\bvalid\b',
            '(?i)\bfail(?:ing|s|ed)?\b',
            '(?i)\bblank\b|not applicable',
            '(?i)\bboundar'
        )) {
            if ($explanation -notmatch $pattern) {
                throw "$code learner_explanation must discuss valid, failing, blank/not-applicable, and boundary behaviour."
            }
        }
        $lowerExplanation = $explanation.ToLowerInvariant()
        foreach ($term in $ruleExplanationTerms[$code]) {
            if (-not $lowerExplanation.Contains($term)) {
                throw "$code learner_explanation must use the rule-specific term '$term'."
            }
        }
    }
    "PASS: $($matrix.Count) rule rows satisfy the bounded case contracts and explanation structure"
}

function Write-CreateOnceTextEvidence {
    param([string]$Path, [string]$Text)
    if (Test-Path -LiteralPath $Path) {
        if (-not (Test-Path -LiteralPath $Path -PathType Leaf) -or
            (Get-Content -Raw -LiteralPath $Path).Trim() -cne $Text.Trim()) {
            throw "Existing checker evidence is unfamiliar. Preserve it and stop: $Path"
        }
        Write-Host "KEEPING existing $Path"
    } else {
        $Text | Set-Content -LiteralPath $Path -Encoding utf8
        Write-Host "CREATED $Path"
    }
}

$incorrectCasePath = Join-Path $moduleFolder 'supplied_incorrect_matrix_case.csv'
$correctedCasePath = Join-Path $moduleFolder 'supplied_corrected_matrix_case.csv'
$incorrectCase = [PSCustomObject][ordered]@{
    rule_code = 'R003'
    valid_example = 'x'
    failing_example = 'x'
    blank_or_not_applicable = 'x'
    boundary_example = 'x'
    learner_explanation = 'x'
}
$correctedCase = [PSCustomObject][ordered]@{
    rule_code = 'R003'
    valid_example = 'case=R003-V; field=priority; value=medium; expect=NO_ISSUE; because=medium is one of the three allowed priorities'
    failing_example = 'case=R003-F; field=priority; value=urgent; expect=ISSUE; because=urgent is outside the exact allowed priority set'
    blank_or_not_applicable = 'case=R003-B; field=priority; value=<BLANK>; expect=R001_ISSUE; because=the required-value rule handles a blank before R003'
    boundary_example = 'case=R003-D; field=priority; value=high|urgent; expect=NO_ISSUE|ISSUE; because=high is allowed and the next supplied category urgent is not'
    learner_explanation = 'For R003, a valid priority is in the allowed set and the failing value is outside it. A blank is handled first as missing required data. The categorical boundary changes from allowed high to disallowed urgent.'
}
foreach ($labCase in @(
    @($incorrectCasePath, $incorrectCase),
    @($correctedCasePath, $correctedCase)
)) {
    if (Test-Path -LiteralPath $labCase[0]) {
        $savedCase = @(Import-Csv -LiteralPath $labCase[0])
        if ($savedCase.Count -ne 1) {
            throw "Existing supplied lab case is unfamiliar. Preserve it and stop: $($labCase[0])"
        }
        foreach ($column in $requiredColumns) {
            if ([string]$savedCase[0].$column -cne [string]$labCase[1].$column) {
                throw "Existing supplied lab case changed. Preserve it and stop: $($labCase[0])"
            }
        }
        Write-Host "KEEPING existing $($labCase[0])"
    } else {
        $labCase[1] | Export-Csv -NoTypeInformation -Encoding utf8 `
            -LiteralPath $labCase[0]
        Write-Host "CREATED $($labCase[0])"
    }
}

try {
    $unexpectedNegativePass = Test-RuleExampleMatrix `
        -Path $incorrectCasePath `
        -ExpectedCodes @('R003')
    throw "The supplied incorrect case unexpectedly passed: $unexpectedNegativePass"
} catch {
    if ($_.Exception.Message -like 'The supplied incorrect case unexpectedly passed:*') {
        throw
    }
    $negativeEvidence = "EXPECTED FAILURE: $($_.Exception.Message)"
}
if ($negativeEvidence -notmatch 'R003 valid_example must start with') {
    throw 'The supplied incorrect case failed for an unexpected reason.'
}
Write-CreateOnceTextEvidence `
    -Path (Join-Path $moduleFolder 'matrix_checker_deliberate_failure.txt') `
    -Text $negativeEvidence

$positiveEvidence = Test-RuleExampleMatrix `
    -Path $correctedCasePath `
    -ExpectedCodes @('R003')
if ($positiveEvidence -notmatch '^PASS: 1 rule rows') {
    throw 'The supplied corrected case did not produce the expected pass.'
}
Write-CreateOnceTextEvidence `
    -Path (Join-Path $moduleFolder 'matrix_checker_correction_pass.txt') `
    -Text $positiveEvidence

Test-RuleExampleMatrix -Path $matrixPath
```

Expected evidence:

- `matrix_checker_deliberate_failure.txt` begins with `EXPECTED FAILURE:` and
  names `R003 valid_example`;
- `matrix_checker_correction_pass.txt` begins with `PASS: 1 rule rows`;
- the final output begins with `PASS: 11 rule rows`.

The first record must remain failed; never replace it with the corrected
result. This checker is intentionally stricter than a nonblank-cell check, but
it still cannot understand prose. The read-only Codex review below must inspect
the learner-written reasons and explanation for semantic correctness.

5. Reuse the demonstrated `Sort-Object -Unique` pattern and verify counts and
   coverage:

```powershell
$recreatedRows = Import-Csv .\recreated_work_items.csv
$recreatedGold = Import-Csv .\recreated_expected_issues.csv
$recreatedRows.Count
$recreatedGold.Count
$recreatedGold.rule_code | Sort-Object -Unique
Select-String -Path .\recreated_data_and_rules.md -Pattern 'R001','R011','2026-07-26','invalid date'
```

**Expected output:** 15 rows, 13 issues, R001 through R011, and four text
matches.

6. Re-run this self-contained comparison. It deliberately rebuilds
   `$sourceData`, so it still works after PowerShell has been closed:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$sourceData = Join-Path $courseRoot 'practice_data\work_items.csv'
$recreatedData = Join-Path $moduleFolder 'recreated_work_items.csv'
if (-not (Test-Path -LiteralPath $sourceData -PathType Leaf) -or
    -not (Test-Path -LiteralPath $recreatedData -PathType Leaf)) {
    throw 'A named source or recreated CSV is missing. Stop and inspect the paths.'
}
$sourceHash = (Get-FileHash -LiteralPath $sourceData -Algorithm SHA256).Hash
$recreatedHash = (Get-FileHash -LiteralPath $recreatedData -Algorithm SHA256).Hash
$sourceHash
$recreatedHash
$sourceHash -eq $recreatedHash
```

   The final line must be `True`. A `False` result is a safe stop; preserve
   both files and request read-only diagnosis.

7. Open `data_dictionary_and_quality_check.md` in Notepad and recreate the
   demonstrated quality record for the different 15-row fixture. Complete the
   dataset boundary, all 12 dictionary fields, R001–R011 quality rules, input
   profile, untouched-source and working-copy locations, transformation and
   provenance statement, issue counts, known blind spots, fields unsuitable
   for AI, and a reviewer/date decision. Reuse the facts in
   `recreated_data_and_rules.md`; the two files must not disagree. Do not alter
   the source or expected-answer files.

If your rules use “today,” “unusual,” or “use judgement,” replace that language
with a configured value or an explicit human escalation.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path` to obtain the full path, replace
`[PASTE FULL PATH HERE]`, and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
[PASTE FULL PATH HERE]

Learner attestation: I created these files for this fictional exercise and
have not knowingly put real client, employer, personal, medical, credential,
or secret data in them. This statement is an attestation, not proof.

You may only list names, read files, and calculate hashes inside the authorised
path. Do not create, edit, delete, rename, move, or format any file. Do not
execute lesson scripts, use a network, or inspect a parent
or other location. If apparent sensitive data is noticed, do not quote or
repeat it: return NOT YET with only the filename and general category, then
stop. If none is noticed, say that non-detection is not proof that none exists.

Inspect the worked and recreated comma-separated values (CSV) and Markdown
files, including worked_data_dictionary_and_quality_check.md,
recreated_rule_example_matrix.csv, and
data_dictionary_and_quality_check.md. Also inspect
supplied_incorrect_matrix_case.csv, supplied_corrected_matrix_case.csv,
matrix_checker_deliberate_failure.txt, and
matrix_checker_correction_pass.txt. Return:
1. PASS or NOT YET;
2. checks for: 12-field dictionary; exact R001-R011 coverage; fixed date
2026-07-26; raw values preserved; blanks distinguished from zero; invalid dates
blocking dependent checks; duplicate rule reporting both rows; evidence-linked
issue contract; 15 input rows; 13 unique expected keys; exactly one matrix row
for each R001-R011 rule; every matrix row has a semantically correct valid,
failing, blank-or-reasoned-not-applicable, and exact boundary example; every
bounded case uses the rule's correct field, value, expectation, and a meaningful
learner-written `because` reason; every `learner_explanation` accurately
explains all four categories in the learner's own words; the supplied `x` case
is preserved with `EXPECTED FAILURE`, the corrected R003 case is separately
preserved with `PASS`, and the failure record was not replaced by the retest;
no AI
used for deterministic checks; synthetic-only data; unchanged source-copy
content where observable; complete dataset boundary and input profile;
recreated_data_and_rules.md agrees with data_dictionary_and_quality_check.md;
3. the smallest corrections for me to make if NOT YET.

Remain read-only and do not provide replacement files.
```

## Pass criteria

- [ ] The worked four-issue answer is understood and reproduced.
- [ ] Source copies remain byte-identical to supplied files.
- [ ] The recreated data dictionary covers all 12 fields.
- [ ] The rule register covers R001–R011 exactly.
- [ ] `recreated_rule_example_matrix.csv` has exactly 11 unique rule rows and
      every rule has a correct valid, failing, blank-or-reasoned-not-applicable,
      and boundary example.
- [ ] Every matrix case matches its rule-specific field, value, and expected
      result contract; each has my meaningful `because` reason and each row has
      my 100-character-or-longer explanation of all four categories.
- [ ] The supplied meaningless `x` case is preserved as
      `EXPECTED FAILURE`, and the separate corrected R003 case is preserved as
      `PASS`; the failed record was not overwritten by the retest.
- [ ] Fixed date `2026-07-26` is configuration, not “today.”
- [ ] Invalid dates do not trigger dependent date checks.
- [ ] Blank and zero are distinct.
- [ ] Every issue carries source evidence.
- [ ] All 13 expected keys are mapped without changing the answer key.
- [ ] `data_dictionary_and_quality_check.md` completes the dataset boundary,
      12 fields, R001–R011, input profile, provenance, issue counts, blind
      spots, reviewer, and dated decision.
- [ ] The two recreated Markdown records do not disagree.
- [ ] AI is excluded from deterministic issue detection and severity.
- [ ] Codex returns `PASS` read-only.

## Consultant lens

Data definitions and business rules require an authorised owner, source,
version, effective date, exceptions, and examples. “Everyone knows what
overdue means” is not an implementable requirement.

## Capstone increment

The capstone now has a frozen source, completed data dictionary and quality
check, R001–R011 register, issue contract, boundary cases, rule dependencies,
and expected result.

## Required artifact

The teaching contract produces the worked CSV/Markdown files,
`worked_data_dictionary_and_quality_check.md`,
`recreated_data_and_rules.md`, and
`recreated_rule_example_matrix.csv`, and
`data_dictionary_and_quality_check.md` under `evidence\module-03`. It also
preserves the supplied incorrect and corrected matrix cases plus
`matrix_checker_deliberate_failure.txt` and
`matrix_checker_correction_pass.txt`.

## Test gate

The **Pass criteria** are the complete gate.

## After PASS — make the Git checkpoint

Do this only after Codex returns `PASS`. Inspect the module folder yourself and
confirm it contains only synthetic course evidence: no password, secret key,
personal data, employer data, client data, patient data, or unrelated file.
Rerun Stage 1 in this same PowerShell window so the exact marker and Git-root
checks pass again. Then run:

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-03"
git commit --only -m "complete module 3 evidence" -- "evidence/module-03"
git status --short
```

`git status --short` previews changes. `git add --` stages only this module;
`--` marks the end of Git options. `git commit --only` records only the
repeated module path, even if a different file had already been staged. If a
rerun reports “nothing to commit,” the unchanged evidence is already recorded.
Do not broaden the path to force a commit.

## Stop or rework

Stop when source or gold hashes change, field meaning remains ambiguous, an
invalid prerequisite still feeds another rule, AI is asked to guess a rule, or
real data enters the folder.

## Common failures

- Letting a spreadsheet alter dates or identifiers.
- Treating appearance as proof of data type.
- Silently correcting invalid input.
- Reporting only the second row in a duplicate pair.
- Editing the answer key to make a result pass.

## Estimated time

8–10 hours. This is an **AUTHOR ESTIMATE — NOT BEGINNER MEASURED**.
