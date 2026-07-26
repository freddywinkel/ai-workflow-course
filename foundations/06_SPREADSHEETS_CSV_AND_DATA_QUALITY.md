# Foundation 6 — Spreadsheets, Comma-Separated Values (CSV), and Data Quality

**PowerShell** is the Windows command shell used to import and inspect the
practice tables in this lesson.

## Outcome

You will create a small CSV table, import it safely with PowerShell, detect two
data-quality issues using exact rules, and create a traceable issue file.

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

### Part A — create the lesson folder and source CSV

Open PowerShell and run:

```powershell
Set-Location ([Environment]::GetFolderPath("MyDocuments"))
```

```powershell
Set-Location "controlled-ai-course-practice"
```

```powershell
New-Item -ItemType Directory -Path "foundation-06"
```

```powershell
Set-Location "foundation-06"
```

What the setup commands do: they enter Documents, enter the existing practice
root, create only `foundation-06`, and enter it.

Run:

```powershell
notepad "work_items.csv"
```

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

Run:

```powershell
notepad "found_issues.csv"
```

Enter:

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

- If the table appears as one column, confirm the file uses commas and is named
  `.csv`, not `.csv.txt`.
- If `$workItems.Count` is not `3`, reopen the file and compare line breaks and
  commas with the sample.
- If PowerShell forgets `$workItems`, you opened a new terminal. Run the
  `Import-Csv` assignment again.
- If a spreadsheet program changes dates or leading zeros, close it without
  saving and return to the untouched CSV. Import settings must be deliberate.

## Now recreate it yourself

Create `service_queue.csv` with these six headers:

```text
ticket_id,category,state,opened_date,target_date,assigned_role
```

Create four fictional rows using IDs `T-91` through `T-94`. Include exactly:

- one valid active row with an assigned role;
- one active row with a blank `assigned_role`;
- one row with invalid state `paused`, where the allowed states are `new`,
  `active`, and `done`;
- one row whose `opened_date` uses `2026/08/02` instead of `2026-08-02`.

Then create `recreated_issues.csv` with one traceable issue row for each of those
three deliberate problems. Choose three new issue IDs and three stable rule
codes. Use PowerShell to confirm four input rows and three issue rows.

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
This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] I can explain row, column, header, cell, CSV, delimiter, ID, and blank.
- [ ] I imported CSV without changing the source.
- [ ] My exact row counts are 3 for `work_items.csv` and 4 for
      `service_queue.csv`.
- [ ] My issue files point to the relevant input ID, field, and rule code.
- [ ] I can explain the five data-quality dimensions.
- [ ] I can distinguish a date-shape check from proof of a valid calendar date.
- [ ] The exercise contains only synthetic data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
