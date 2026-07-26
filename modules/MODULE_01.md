# Module 1 — Observe the Work Before You Automate

## Outcome

You will observe a small operational process, distinguish evidence from
assumptions, map the current work, and measure a manual baseline. You will not
choose a tool or add artificial intelligence (AI) yet.

A small or medium-sized enterprise (SME) is a business that is smaller than a
large enterprise. The final practice project, also called a **capstone**, is the
**Synthetic SME Operations Exception Assistant** for a fictional Dutch SME. It
uses no employer, client, patient, employee, or other real data.

## Beginner checkpoint

Start here when you can create a folder, open a plain-text file, and copy an
exact command. If those actions are unfamiliar, complete Foundations 1 and 2
first.

Comma-separated values (CSV) is a plain-text table format; `.csv` is its file
name ending.

For this module, the start state is:

- the course folder exists on your computer;
- `practice_data/work_items.csv` is present;
- no practice folder contains real or confidential information.

## Concepts

- A **process** is a connected set of steps that produces an outcome.
- A **trigger** starts one run of the process.
- A **completion condition** is observable proof that the run is finished.
- A **unit of work** is one item handled by the process.
- An **actor** is a person or system performing a step.
- A **handoff** moves work or information between actors.
- **Active time** is time spent working; **wait time** is time spent blocked.
- A **baseline** measures the current method before improvement.
- An **observation** is visible or measured. An **assumption** is not yet
  confirmed.
- A **source of truth** is the agreed authoritative record.
- **Markdown** is plain text with simple heading and table symbols; `.md` is
  its file name ending.
- **Unicode Transformation Format 8-bit (UTF-8)** is the text encoding used for
  the practice files.
- **Secure Hash Algorithm 256-bit (SHA-256)** creates a repeatable digital
  fingerprint of exact file bytes; the later command spells the option
  `SHA256`.

## Official readings

GOV.UK is the United Kingdom government's public guidance website. The United
States National Institute of Standards and Technology (NIST) publishes a
voluntary AI risk framework; it is guidance, not Dutch law.

1. [GOV.UK Service Manual: understand users and their needs](https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs)
2. [GOV.UK Service Manual: learning about users and their needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs)
3. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

## Guided build

The worked example and independent recreation below are the complete practice
for this module. Do not add workplace interviews or real files.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files.

## Follow along — I show you exactly how

### Stage 1 — Create one controlled practice folder

**Prerequisites and start state:** Windows is open. The course files remain
unchanged.

1. Press the Windows key, type `PowerShell`, and click **Windows PowerShell**.
   PowerShell is the Windows command-line application used to run exact text
   commands.
2. Copy and run:

```powershell
$practiceBase = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'controlled-ai-course-practice'
$moduleFolder = Join-Path $practiceBase 'module-01'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
(Get-Location).Path
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE without quotation marks'
$guidedSourceCsv = Join-Path $courseRoot 'practice_data\work_items.csv'
$guidedSourceCsv
Test-Path -LiteralPath $guidedSourceCsv
```

`Join-Path` safely combines a parent path with a child name. `New-Item` creates
the practice folder. `Set-Location` makes it the current folder.

`Read-Host` pauses and stores exactly the course-folder path you paste.
The second `Join-Path` constructs the complete source-file path without asking
you to type every backslash. `Test-Path` checks that the named source exists; it
does not open or change it.

**Expected result:** the first path ends in
`\Documents\controlled-ai-course-practice\module-01`, the next path ends in
`\practice_data\work_items.csv`, and the final line is `True`.

**Troubleshooting:**

- If PowerShell shows a red “access denied” message, confirm that the printed
  base is your Documents folder and rerun PowerShell normally, not as another
  user.
- If the prompt begins in another folder, that is harmless; `Set-Location`
  corrects it.
- If `Test-Path` prints `False`, confirm that `$courseRoot` names the course
  folder containing `practice_data`, then repeat the `Read-Host`, second
  `Join-Path`, and `Test-Path` lines. Do not continue with a guessed path.

### Stage 2 — Create, copy, and verify a worked source

1. In PowerShell, run:

```powershell
notepad .\worked_queue.csv
```

Notepad is Windows' plain-text editor. When asked to create the file, click
**Yes**. Paste:

```csv
job_id,status,due_date,owner_role
JB-101,in_progress,2026-07-25,repairs
JB-102,completed,2026-07-24,
JB-103,waiting,2026-07-20,
JB-104,new,2026-08-03,intake
```

Press **Ctrl+S**, then close Notepad. The first CSV line is the header and each
later line is one row.

2. Create a guided copy and compare the exact bytes:

```powershell
$workedSource = Join-Path $moduleFolder 'worked_queue.csv'
$workedCopy = Join-Path $moduleFolder 'worked_queue_copy.csv'
Copy-Item -LiteralPath $workedSource -Destination $workedCopy
$workedSourceHash = Get-FileHash -LiteralPath $workedSource -Algorithm SHA256
$workedCopyHash = Get-FileHash -LiteralPath $workedCopy -Algorithm SHA256
$workedSourceHash
$workedCopyHash
$workedSourceHash.Hash -eq $workedCopyHash.Hash
```

`Copy-Item` copies the exact named source to the exact `-Destination`.
`-LiteralPath` treats the path as written rather than interpreting wildcard
characters. `Get-FileHash` reads a file and calculates its SHA-256 fingerprint;
it does not edit the file. `.Hash` selects the fingerprint value, and `-eq`
asks whether the two values are equal.

**Expected result:** PowerShell displays two `SHA256` records with different
paths but the same 64-character hash, followed by `True`.

**Troubleshooting:** if the final result is `False`, close both CSV files, rerun
`Copy-Item`, and then rerun the four hash lines. Do not edit either file merely
to make the hashes match.

### Stage 3 — Time and map the worked observation

1. Start a timer. Run `notepad .\worked_queue.csv`, inspect all four rows, then
   stop the timer.
2. Run:

```powershell
notepad .\worked_observation.md
```

Click **Yes** and paste the completed Markdown example:

```markdown
# Worked process observation

Synthetic-only boundary: This file describes a fictional queue. It contains no
real organisation, client, employee, patient, or confidential information.

## Process boundary

- Trigger: the daily queue export becomes available.
- Completion: a human reviewer has checked the internal attention list.
- Unit of work: one row identified by job_id.
- Source of truth: the fictional queue export.
- User: operations coordinator.
- Reviewer: operations lead.
- Fallback: stop and ask the process owner when a field meaning is unclear.

## As-is process

| Step | Actor | Action | Evidence | Possible failure |
|---:|---|---|---|---|
| 1 | source system | produces CSV export | unchanged source file | file missing |
| 2 | coordinator | opens and scans every row | manual notes | row skipped |
| 3 | coordinator | records values that may need attention | job_id and field | meaning guessed |
| 4 | operations lead | checks notes against the source | review decision | reviewer unavailable |
| 5 | coordinator | closes the check | reviewed list | no completion evidence |

## Observed

- The file has four data rows.
- JB-102 and JB-103 have a blank owner_role.
- JB-101, JB-102, and JB-103 have dates before 2026-07-26.

## Unconfirmed assumptions

- A blank owner may be an error.
- A date before 2026-07-26 may mean overdue.
- Completed work may or may not require an owner.

## Discovery questions

1. Which statuses require an owner?
2. What exact comparison defines overdue?
3. Who approves those rules?
4. What should happen when the CSV header changes?
5. What proves that review is complete?

## Baseline

- Rows inspected: 4
- Active time: REPLACE WITH YOUR MEASURED TIME
- Repeated checks: REPLACE WITH WHAT YOU RECHECKED
- Unresolved questions: 5
```

Replace the two `REPLACE` lines with your real observation results. Press
**Ctrl+S** and close Notepad.

3. Verify without changing the files:

```powershell
Get-ChildItem -LiteralPath $moduleFolder
Get-Content .\worked_observation.md
```

**Expected output:** `worked_queue.csv`, `worked_queue_copy.csv`, and
`worked_observation.md` appear, and the observation displays with your measured
time. Notice that the example records suspicious values but does not declare an
exception before rules are authorised.

**Troubleshooting:**

- If the file is named `worked_queue.csv.txt`, open File Explorer, click
  **View > Show > File name extensions**, then rename it to
  `worked_queue.csv`.
- If accented or punctuation characters look wrong, reopen Notepad and choose
  **File > Save As > Encoding: UTF-8**.
- If your measured time is unusually short or long, keep it. A baseline is
  evidence, not a performance test.

## Now recreate it yourself

Use different synthetic data: the supplied 15-row capstone register.

1. Reuse the demonstrated `Read-Host`, `Join-Path`, `Copy-Item`, and
   `Get-FileHash` pattern. In PowerShell, run:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$sourceCsv = Join-Path $courseRoot 'practice_data\work_items.csv'
Copy-Item -LiteralPath $sourceCsv -Destination .\recreated_work_items.csv
Get-FileHash -LiteralPath $sourceCsv -Algorithm SHA256
Get-FileHash -LiteralPath .\recreated_work_items.csv -Algorithm SHA256
```

The two SHA-256 values must match; matching values show that the copy has the
same bytes.

2. Time one manual inspection of `recreated_work_items.csv`. Do not open
   `expected_issues.csv`.
3. Create `recreated_observation.md` in Notepad. Use the worked example's
   sections, but write a new map for the 15-row work-item process. Include:
   trigger, completion, actors, source of truth, fallback, at least five
   observations, at least five clearly labelled assumptions, five discovery
   questions, active time, and repeated checks.
4. Run both hash commands again. The source and recreated copy must still
   match.

This is recreation, not copying: your observations, timing, and questions must
come from the different 15-row file.

## Ask Codex to check your work

Codex is the AI coding assistant in this application. First run
`(Resolve-Path $moduleFolder).Path` to obtain the full path and replace
`[PASTE FULL PATH HERE]` below with that one printed path. Then copy the prompt:

```text
READ-ONLY COURSE REVIEW.

I authorize you to inspect only this full path:
[PASTE FULL PATH HERE]

Do not create, edit, delete, rename, move, or format any file. Do not inspect
the parent folder or any other location. Do not run a command that changes
state. This folder must contain no secrets and no real client or workplace
data; stop if you see credentials, personal data, or health data.

Check worked_queue.csv, worked_queue_copy.csv, worked_observation.md, and
recreated_observation.md. Return exactly:
1. PASS or NOT YET;
2. a checklist against these criteria: synthetic boundary; trigger; observable
completion; unit of work; actors; source of truth; fallback; step-by-step as-is
map; observations separated from assumptions; five discovery questions;
worked queue and guided copy are byte-identical; measured active time; no
proposed AI solution presented as observed fact;
3. for NOT YET, the smallest corrections I should make myself.

Do not make the corrections. Do not judge writing style beyond clarity and the
criteria.
```

## Pass criteria

- [ ] The authorised folder is exactly `module-01`, not its parent.
- [ ] Worked and recreated files contain synthetic information only.
- [ ] The worked queue and guided copy produce matching SHA-256 values.
- [ ] The recreated CSV still matches its source hash.
- [ ] Both observations state trigger, completion, unit, actors, source, and
      fallback.
- [ ] Process steps include evidence and failure points.
- [ ] Observations and assumptions are separate.
- [ ] The recreated file has at least five observations and five assumptions.
- [ ] Active time is measured rather than estimated.
- [ ] No AI feature or software product is treated as an observed user need.
- [ ] Codex returns `PASS`, or you correct the work yourself and request another
      read-only check.

## Consultant lens

A client request such as “automate our spreadsheet” is not yet a problem
definition. A controlled implementation consultant first finds the outcome,
owner, authoritative data, current evidence, delay, rework, and fallback. A
responsible observation may conclude that the process needs clarification
before automation.

Workplace observation requires permission. This synthetic exercise grants no
permission to inspect an employer's systems or interview colleagues.

## Capstone increment

You now have an as-is process map and honest manual baseline for the Synthetic
SME Operations Exception Assistant.

## Required artifact

The evidence already created under the teaching contract is:

- `worked_queue.csv`;
- `worked_queue_copy.csv`;
- `worked_observation.md`;
- `recreated_work_items.csv`;
- `recreated_observation.md`;
- the read-only Codex result copied into `codex_check.txt` if you choose to
  retain it.

## Test gate

The module gate is exactly the **Pass criteria** above. There are no hidden
tasks.

## Stop or rework

Stop if real or confidential data appears, a file hash changes unexpectedly,
the process has no owner or completion condition, or you find yourself guessing
field meanings. Rework using synthetic data and recorded assumptions.

## Common failures

- Mapping the desired future system instead of current work.
- Recording software clicks but missing waits, handoffs, and review.
- Calling a blank field an error before a rule is authorised.
- Replacing measured time with an attractive estimate.
- Asking Codex to repair files instead of checking them read-only.

## Estimated time

6–8 hours, including the worked example, independent recreation, and recheck.
