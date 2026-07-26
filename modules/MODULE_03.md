# Module 3 — Understand the Data and Rules

## Outcome

You will create a data dictionary, deterministic rule register, issue-output
contract, rule order, and frozen expected-result comparison before writing a
workflow.

## Beginner checkpoint

Start when Module 2 passes. You need Foundations 3 and 6 and the supplied
`practice_data` folder. All data must remain synthetic.

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
2. [European Commission: GDPR processing principles](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en)
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

## Follow along — I show you exactly how

### Stage 1 — Create the practice folder and mini-dataset

Open Windows PowerShell and run:

```powershell
$practiceBase = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'controlled-ai-course-practice'
$moduleFolder = Join-Path $practiceBase 'module-03'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
notepad .\worked_jobs.csv
```

International Organization for Standardization (ISO) date format uses
`YYYY-MM-DD`: year, month, then day. Click **Yes**, paste, save, and close
Notepad:

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

`Import-Csv` reads each row without editing the file.

**Expected result:** `4`, then the five headers, then four rows.

**Troubleshooting:**

- If the count is 0, confirm the header and rows were saved.
- If everything appears under one header, confirm commas separate values.
- Never correct the source row merely because it looks wrong.

### Stage 2 — Follow the complete contract

Run `notepad .\worked_data_and_rules.md`, click **Yes**, paste, and save:

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

Create `worked_boundary.csv` in Notepad:

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

## Now recreate it yourself

Use the different Course 1 fixture and rule set:

1. Run:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$sourceData = Join-Path $courseRoot 'practice_data\work_items.csv'
$sourceGold = Join-Path $courseRoot 'practice_data\expected_issues.csv'
$sourceReadme = Join-Path $courseRoot 'practice_data\README.md'
Copy-Item -LiteralPath $sourceData -Destination .\recreated_work_items.csv
Copy-Item -LiteralPath $sourceGold -Destination .\recreated_expected_issues.csv
Copy-Item -LiteralPath $sourceReadme -Destination .\recreated_requirements.md
Get-FileHash -LiteralPath $sourceData -Algorithm SHA256
Get-FileHash -LiteralPath .\recreated_work_items.csv -Algorithm SHA256
```

The two hashes must match.

2. Read `recreated_requirements.md`.
3. Create `recreated_data_and_rules.md` yourself. Include:

- all 12 fields and their blank meanings;
- R001 through R011 with exact condition, field, severity, dependency, evidence,
  and requirement source;
- fixed assessment date `2026-07-26`;
- rule order and explicit skip behaviour for invalid dates;
- an issue contract containing `work_item_id`, `source_reference`, field, raw
  value, rule, severity, message, and assessment date;
- one valid, failing, blank/not-applicable, and boundary example per applicable
  rule;
- a manual map of all 13 expected `(work_item_id, rule_code)` pairs;
- a data-minimisation decision.

4. Reuse the demonstrated `Sort-Object -Unique` pattern and verify counts and
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

5. Re-run the source and copy hashes. They must still match.

If your rules use “today,” “unusual,” or “use judgement,” replace that language
with a configured value or an explicit human escalation.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path` to obtain the full path, replace
`[PASTE FULL PATH HERE]`, and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
[PASTE FULL PATH HERE]

Do not create, edit, delete, rename, move, or format anything. Do not inspect
the parent folder or another location. This folder must contain no secrets and
no real client or workplace data. Stop if you find credentials, personal data,
or health data.

Inspect the worked and recreated CSV/Markdown files. Return:
1. PASS or NOT YET;
2. checks for: 12-field dictionary; exact R001-R011 coverage; fixed date
2026-07-26; raw values preserved; blanks distinguished from zero; invalid dates
blocking dependent checks; duplicate rule reporting both rows; evidence-linked
issue contract; 15 input rows; 13 unique expected keys; boundary cases; no AI
used for deterministic checks; synthetic-only data; unchanged source-copy
content where observable;
3. the smallest corrections for me to make if NOT YET.

Remain read-only and do not provide replacement files.
```

## Pass criteria

- [ ] The worked four-issue answer is understood and reproduced.
- [ ] Source copies remain byte-identical to supplied files.
- [ ] The recreated data dictionary covers all 12 fields.
- [ ] The rule register covers R001–R011 exactly.
- [ ] Fixed date `2026-07-26` is configuration, not “today.”
- [ ] Invalid dates do not trigger dependent date checks.
- [ ] Blank and zero are distinct.
- [ ] Every issue carries source evidence.
- [ ] All 13 expected keys are mapped without changing the answer key.
- [ ] AI is excluded from deterministic issue detection and severity.
- [ ] Codex returns `PASS` read-only.

## Consultant lens

Data definitions and business rules require an authorised owner, source,
version, effective date, exceptions, and examples. “Everyone knows what
overdue means” is not an implementable requirement.

## Capstone increment

The capstone now has a frozen source, data dictionary, R001–R011 register,
issue contract, boundary cases, rule dependencies, and expected result.

## Required artifact

The teaching contract produces the worked CSV/Markdown files and
`recreated_data_and_rules.md` under `module-03`.

## Test gate

The **Pass criteria** are the complete gate.

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

8–10 hours.
