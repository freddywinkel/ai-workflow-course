# Foundation 6 — Spreadsheets, Comma-Separated Values (CSV), and Data Quality

**PowerShell** is the Windows command shell used to import and inspect the
practice tables in this lesson.

## Outcome

You will create a small CSV table, import it safely with PowerShell, detect two
data-quality issues using exact rules, and create a traceable issue file.

## Study plan — seven blocks of no more than 60 minutes

**Time label: AUTHOR ESTIMATE — NOT BEGINNER MEASURED.** The published
6–7-hour range is a planning estimate, not measured novice completion time.
Use each row as a separate study segment. Stop when the row is complete or
when 60 focused minutes have elapsed, whichever happens first. Record the last
completed part using synthetic wording, save and close files, and take a break.
Run **Start or resume safely** in every new PowerShell session; never combine
blocks.

| Block | Maximum | Work and safe stopping point |
|---:|---:|---|
| 1 | 60 minutes | Learn the tabular-data and quality words plus the safety boundary. |
| 2 | 60 minutes | Run the start/resume block and make the explicit resume/retry decision. |
| 3 | 60 minutes | Complete Part A and inspect the source Comma-Separated Values (CSV) file as plain text. |
| 4 | 60 minutes | Complete Part B and confirm the imported row count. |
| 5 | 60 minutes | Complete Part C and explain both exact checks before accepting their output. |
| 6 | 60 minutes | Complete Part D, compare the exact result, and troubleshoot only observed mismatches. |
| 7 | 60 minutes | Recreate the task with different rows/rules, ask Codex for the bounded check, and apply every pass criterion. |

## Words you need first

- A **spreadsheet** is a grid used to organise and calculate tabular data.
- A **workbook** is a spreadsheet file. It can contain multiple
  **worksheets**, also called sheets or tabs.
- A **row** represents one declared record or unit of work.
- A **column** represents one named attribute of those records.
- A **header row** contains the column names.
- A **cell** is the intersection of one row and one column.
- **Comma-separated values (CSV)** is a plain-text table format. It does not
  preserve spreadsheet colours, formulas, multiple worksheets, filters, or
  comments.
- A **delimiter** is the character separating fields. This course file uses a
  comma. Some Dutch spreadsheet exports use a semicolon.
- **Unicode Transformation Format 8-bit (UTF-8)** is the text encoding used in
  this lesson.
- An **identifier (ID)** is a stable value that identifies one record, such as
  `WI-201`. Treat it as text, not a number to calculate with.
- A **data type** says what kind of value a field holds, such as text, date,
  number, or Boolean.
- A **Boolean** is a true-or-false value.
- A **blank** means no value is recorded. It is not automatically zero, false,
  or not applicable.
- A **deterministic rule** should produce the same result for the same input and
  rule version.
- A **regular expression** is a text pattern. This lesson uses one to check the
  visible shape of a date.
- `YYYY-MM-DD` means four-digit year, two-digit month, and two-digit day,
  separated by dashes.
- A **PowerShell object** is a structured value whose fields can be addressed by
  name.
- **Notepad** is the Windows plain-text editor used to create the CSV files.
- An **export** is a copied snapshot taken out of another system.
- A **variable** is a named value held in the current PowerShell session, such
  as `$workItems`.
- `Import-Csv` is a PowerShell command that reads CSV rows into PowerShell
  objects.
- `Format-Table` displays objects as a table; `-AutoSize` adjusts the displayed
  column widths to their contents.
- `Where-Object` keeps only objects that meet a stated condition.
- `Select-Object` chooses which named fields to display.
- In a PowerShell pipeline, the vertical bar `|` passes output to the next
  command, and `$_` means the current object being checked.
- `IsNullOrWhiteSpace` checks whether text is missing, empty, or contains only
  spaces. `-notmatch` checks that text does not match a stated pattern.
- A **reason code** is a stable machine-readable label for a rule result, such
  as `R001`.
- An **issue record** stores what a check found and links it to the affected
  record, field, and reason code.
- **Codex** is the artificial intelligence (AI) assistant used for the final
  read-only check. The check prompt limits it to one practice folder.

Five useful data-quality dimensions are:

| Dimension | Beginner question |
|---|---|
| Completeness | Is every required value present? |
| Validity | Does each value follow its allowed format or list? |
| Consistency | Do related values agree? |
| Uniqueness | Is an identifier or record repeated only when allowed? |
| Timeliness | Is the value current enough for its purpose? |

A **true positive** is an expected issue that a check finds. A **false
positive** is a reported issue that is not actually an issue under the rule. A
**false negative** is an expected issue the check misses.

## Safety boundary

Use only the three fictional rows below. An export from a workplace system can
contain confidential or personal data even when names are removed. Do not use
one in this lesson and do not upload a real spreadsheet to Codex.

## Follow along — I show you exactly how

### Prerequisites and start state

- Foundations 1–5 are complete.
- PowerShell and Notepad are available.
- `Documents\controlled-ai-course-practice` exists.
- No real spreadsheet or business export is open.

### Start or resume safely — run this at every new PowerShell session

Run this whole block whenever you start or resume Foundation 6:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonFolderName = "foundation-06"
if ($lessonFolderName -notmatch '^foundation-06(?:-retry-\d{2,})?$') {
    throw "STOP: use foundation-06 or a retry name created by this lesson."
}
$lessonPath = Join-Path $practiceRoot $lessonFolderName

function New-FoundationRetryAttempt {
    param([string]$BaseName, [string]$PracticeRoot)
    $retryNumber = 1
    do {
        $retryName = "$BaseName-retry-{0:D2}" -f $retryNumber
        $retryPath = Join-Path $PracticeRoot $retryName
        $retryNumber += 1
    } while (Test-Path -LiteralPath $retryPath)
    New-Item -ItemType Directory -Path $retryPath -ErrorAction Stop | Out-Null
    $retryPath
}

function Open-GuardedPracticeFile {
    param([string]$AttemptPath, [string]$FileName)
    $filePath = Join-Path $AttemptPath $FileName
    if (Test-Path -LiteralPath $filePath -PathType Container) {
        throw "STOP: $FileName is a folder. Do not change it; use a fresh retry attempt."
    }
    if (Test-Path -LiteralPath $filePath -PathType Leaf) {
        "EXISTING — DO NOT EDIT OR OVERWRITE: $FileName"
        Get-Content -LiteralPath $filePath
        return
    }
    New-Item -ItemType File -Path $filePath -ErrorAction Stop | Out-Null
    "CREATED ONCE — enter the requested content: $FileName"
    notepad $filePath
}

if (-not (Test-Path -LiteralPath $practiceRoot -PathType Container)) {
    throw "STOP: the controlled-ai-course-practice folder is missing. Return to Foundation 1."
}
if (Test-Path -LiteralPath $lessonPath -PathType Leaf) {
    throw "STOP: the selected Foundation 6 attempt is a file, not a folder. Do not change it."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new Foundation 6 attempt: $lessonFolderName"
}
else {
    "Existing Foundation 6 attempt found; nothing was overwritten: $lessonFolderName"
}

Set-Location -LiteralPath $lessonPath
Get-Location
Get-ChildItem -Force
```

Expected result: the location ends in `foundation-06` or the selected numbered
retry name. The block creates an absent attempt and lists existing contents
without changing them.

### Decide whether to resume or use a fresh attempt

The two helper functions have narrow jobs:
`New-FoundationRetryAttempt` creates the next unused retry folder;
`Open-GuardedPracticeFile` creates a named file only when absent, or displays an
existing file without opening it for editing.

Apply this decision before Part A and again after any interruption:

1. If the attempt is empty, continue to Part A.
2. The only expected names are `work_items.csv`, `found_issues.csv`,
   `service_queue.csv`, and `recreated_issues.csv`. If the attempt contains
   only those names, use each guarded file step below:
   - `EXISTING` plus exactly complete synthetic content means close or leave
     the file unchanged and skip its creation;
   - an expected file that is absent may be created;
   - an incomplete, different, unfamiliar, or apparently real/sensitive file
     means do not edit, rename, delete, or overwrite anything in this attempt.
3. An unexpected item also requires a fresh attempt.
4. To create the next unused retry, run:

   ```powershell
   $lessonPath = New-FoundationRetryAttempt -BaseName "foundation-06" -PracticeRoot $practiceRoot
   $lessonFolderName = Split-Path -Leaf $lessonPath
   Set-Location -LiteralPath $lessonPath
   "Selected fresh attempt: $lessonFolderName"
   ```

5. Write down the displayed retry name. In a new PowerShell session, replace
   only `"foundation-06"` in `$lessonFolderName` with that exact name before
   running the start block. A retry always restarts at Part A in the new empty
   folder.

### Part A — create the source CSV

Run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "work_items.csv"
```

If the output starts with `EXISTING`, compare the displayed file with the exact
table below. If it is complete, skip its creation and continue to Part B. For
any other existing content, use a fresh retry attempt. Only when the output
starts with `CREATED ONCE` should you enter the table:

Enter these exact four lines:

```csv
work_item_id,title,status,due_date,owner_role
WI-201,Confirm address,in_progress,2026-08-04,operations
WI-202,Close duplicate,completed,2026-07-25,
WI-203,Review reference,waiting,not-a-date,quality
```

Save and close Notepad.

What this creates: one header row and three fictional work-item rows. There are
five columns. `WI-202` has a deliberately blank `owner_role`; `WI-203` has a
deliberately invalid date shape.

### Part B — import and count the rows

Run:

```powershell
$workItems = Import-Csv -LiteralPath ".\work_items.csv"
```

What this does: `Import-Csv` reads the table into PowerShell objects. The
variable `$workItems` holds the imported rows in the current PowerShell window.
It does not modify the source file.

Run:

```powershell
$workItems.Count
```

Expected output:

```text
3
```

Run:

```powershell
$workItems | Format-Table -AutoSize
```

Expected result: a table with three rows and the five named columns.

### Part C — run two exact checks

Run:

```powershell
$workItems | Where-Object { [string]::IsNullOrWhiteSpace($_.owner_role) } | Select-Object work_item_id, status
```

What this does:

- `Where-Object` keeps rows that meet the condition in braces;
- `$_` means the current row;
- `IsNullOrWhiteSpace` checks for a missing, empty, or spaces-only value;
- `Select-Object` shows only the two named fields.

Expected result: one row for `WI-202` with status `completed`.

Run:

```powershell
$workItems | Where-Object { $_.due_date -notmatch '^\d{4}-\d{2}-\d{2}$' } | Select-Object work_item_id, due_date
```

What this does: the regular expression checks for four digits, a dash, two
digits, a dash, and two digits. It is a format check, not proof that a calendar
date exists.

Expected result: one row for `WI-203` with due date `not-a-date`.

### Part D — record the issues separately

Run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "found_issues.csv"
```

If the output starts with `EXISTING`, compare it with the exact issue table
below. Leave an exact completed file unchanged and skip its creation. For any
other existing content, use a fresh retry attempt. Only after `CREATED ONCE`
should you enter:

```csv
issue_id,work_item_id,field,rule_code,message
ISS-A,WI-202,owner_role,R001,Required owner role is missing
ISS-B,WI-203,due_date,R004,Date does not use YYYY-MM-DD
```

Save and close Notepad.

`R001` and `R004` are the stable reason codes for these two rule results. The
issue rows point back to the work item and field. The source file remains
unchanged.

Run:

```powershell
Import-Csv -LiteralPath ".\found_issues.csv" | Format-Table -AutoSize
```

Run:

```powershell
(Get-Location).Path
```

What the final two commands do: the import command reads and displays the issue
file; the path command prints the exact full folder path. Neither changes the
CSV files.

### Expected result — exact

- `work_items.csv` has one header plus three data rows and five columns.
- `$workItems.Count` prints `3`.
- the missing-owner check returns only `WI-202`;
- the date-shape check returns only `WI-203`;
- `found_issues.csv` contains exactly two issue rows, `ISS-A` and `ISS-B`;
- `work_items.csv` still contains its original four lines.

### Troubleshooting

- If the table appears as one column or the file is named `.csv.txt`, do not
  correct or overwrite that attempt. Preserve it and use a fresh retry with
  commas and the correct `.csv` extension.
- If `$workItems.Count` is not `3`, compare the displayed file with the sample.
  Do not overwrite it; preserve that attempt and use a fresh retry.
- If PowerShell forgets `$workItems`, you opened a new terminal. Run the
  `Import-Csv` assignment again.
- If a spreadsheet program changes dates or leading zeros, close it without
  saving and return to the untouched CSV. Import settings must be deliberate.

## Now recreate it yourself

Run the create-once guard for the recreation input:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "service_queue.csv"
```

If it reports `EXISTING`, leave the file unchanged only when it already meets
every requirement below; otherwise use a fresh retry attempt. After
`CREATED ONCE`, create the file with these six headers:

```text
ticket_id,category,state,opened_date,target_date,assigned_role
```

Create four fictional rows using IDs `T-91` through `T-94`. Include exactly:

- one valid active row with an assigned role;
- one active row with a blank `assigned_role`;
- one row with invalid state `paused`, where the allowed states are `new`,
  `active`, and `done`;
- one row whose `opened_date` uses `2026/08/02` instead of `2026-08-02`.

Then run:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "recreated_issues.csv"
```

If it reports `EXISTING`, leave the file unchanged only when it is exactly
complete; otherwise use a fresh retry attempt. After `CREATED ONCE`, add one
traceable issue row for each of those three deliberate problems. Choose three
new issue IDs and three stable rule codes. Use PowerShell to confirm four input
rows and three issue rows.

Run these exact read-only counts:

```powershell
@(Import-Csv -LiteralPath ".\service_queue.csv").Count
@(Import-Csv -LiteralPath ".\recreated_issues.csv").Count
```

Expected output: `4`, followed by `3`.

This uses a different unit of work, fields, identifiers, states, and issue codes
from the guided example.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, or delete anything. Do not correct source
values. Run only read-only CSV inspection commands.

Report PASS or NOT YET for each criterion:
1. work_items.csv has exactly 3 data rows and 5 columns.
2. WI-202 alone has a blank owner_role.
3. WI-203 alone fails the YYYY-MM-DD shape check.
4. found_issues.csv contains exactly the traceable ISS-A/R001 and ISS-B/R004
   issue rows described in the lesson.
5. service_queue.csv has exactly 4 data rows and the 6 required headers.
6. Its three deliberate problems are one blank assigned role, state paused,
   and opened date 2026/08/02.
7. recreated_issues.csv contains exactly one traceable issue for each of those
   three problems.

Explain NOT YET in beginner language and make no changes.
I attest that I created this attempt with synthetic course data only and did
not intentionally add secrets, personal data, client data, employer data, or
other real work data. If you notice content that appears sensitive, stop the
inspection,
do not quote or repeat it, report only the file name and general category, and
report NOT YET. If you notice none, say: "No apparent sensitive content noticed
in this bounded inspection; this is not proof that none exists." Do not claim
that an inspection proves the folder is free of secrets or real data.
```

## Pass criteria

- [ ] I can explain row, column, header, cell, CSV, delimiter, ID, and blank.
- [ ] I imported CSV without changing the source.
- [ ] My exact row counts are 3 for `work_items.csv` and 4 for
      `service_queue.csv`.
- [ ] My issue files point to the relevant input ID, field, and rule code.
- [ ] I can explain the five data-quality dimensions.
- [ ] I can distinguish a date-shape check from proof of a valid calendar date.
- [ ] I attest that all data I entered was synthetic and that I did not
      intentionally add secrets or real personal, employer, or client data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
