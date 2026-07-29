# Foundation 8 — Safe Artificial Intelligence (AI)-Assisted Building

A **function** is a named, reusable block of code. A **claim** is a statement
presented as true, **evidence** is material that supports it, and a
**limitation** states what the evidence does not establish. **Codex** is the AI
assistant used first to propose one bounded change and later to perform the
final read-only check.

## Outcome

You will create and test one small data-quality function, ask Codex for one
bounded change proposal, inspect and narrow its diff, apply only the accepted
part yourself, test it, and record the evidence and limitations. Codex will
inspect the final practice folder without changing it.

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
| 1 | 60 minutes | Learn the required words, safe change loop, and safety boundary. |
| 2 | 60 minutes | Run the start/resume block and make the explicit resume/retry decision. |
| 3 | 60 minutes | Complete Part A and Part B; stop after the smallest program passes its original tests. |
| 4 | 60 minutes | Complete Part C, compare the exact result, and troubleshoot only observed mismatches. |
| 5 | 60 minutes | Recreate Step 1 and Step 2: request a bounded proposal, inspect it, and reject or narrow unsafe hunks. |
| 6 | 60 minutes | Recreate Step 3 and Step 4: apply only the accepted part yourself and test it. |
| 7 | 60 minutes | Ask Codex for the bounded read-only check, explain every accepted change, and apply every pass criterion. |

## Words you need first

- **Context** is the information available to an assistant for one request.
- An **AI coding assistant** proposes explanations, code, tests, or changes from
  instructions and available context.
- An **acceptance criterion** is an observable condition that must be true
  before work is accepted.
- A **database** is structured durable storage that can be queried and updated.
- A **side effect** is a change outside a function's returned value, such as
  writing a file, sending a request, or changing a database.
- A **boundary case** is an input near a rule's limit, such as blank text.
- A **regression** is damage to behaviour that worked before.
- A **package** is an installable collection of code.
- A **dependency** is another package or service the project relies on.
- A **diff** is a line-by-line view of a change.
- **Read-only inspection** means observing files and output without changing
  them.
- **Python** is the programming language used for the examples.
- `None` is Python's explicit value for “no value.”
- A **dictionary** is a Python value that maps named keys to values.
- A **list** is an ordered collection of values. A **membership check** asks
  whether a value appears in a collection.
- An **assertion** is an executable expectation that stops with an error when
  its condition is false.
- A **reason code** is a stable machine-readable label for a result, such as
  `R001`.
- **Syntax** is the grammar of code.
- A **repository** is a project folder tracked by a version-control tool.
- **PowerShell** is the Windows command shell used to run the examples.
  **Notepad** is the Windows plain-text editor used to create their files.
- A **dataset** is a collection of related records used together. A
  **production repository** contains code used for a live service or real work.
- A **security credential** is a value that can grant access. Examples include
  a password (a secret phrase), an access key or token (a service-issued access
  value), a cookie (saved session data), a certificate (digital identity
  evidence), and a private key (secret cryptographic key material).
- **Environment configuration** is settings supplied outside the main program.
  A **secret** is an access-granting value that must be protected. **Source
  code** is the human-readable program text. A **log** is time-ordered
  operational information about what software did.
- A **network call** communicates with another computer or online service.

**Git**, the version-control tool whose name is not an acronym, can show and
record diffs. This lesson does not require a new Git repository, but the same
review discipline applies.

## The safe change loop

1. Inspect current files and behaviour.
2. State one observable outcome.
3. Name what must not change.
4. Plan the smallest reversible change.
5. Explain input, output, side effects, and failures.
6. Inspect the diff or exact saved file.
7. Test success, failure, and boundary cases.
8. Observe the real output.
9. Record evidence and limitations.
10. Keep only a change you can explain.

Generated code and commands are proposals. An assistant may use outdated
syntax, invent a package, weaken a safety check, or claim success without
observing the relevant result.

## Safety boundary

Never give an unapproved AI service:

- passwords, access keys, tokens, cookies, certificates, or private keys;
- environment configuration containing secrets;
- employer, client, supplier, employee, or patient records;
- database exports, private source code, or unredacted logs;
- confidential prompts, contracts, or screenshots.

The practice programs use only built-in Python and fictional dictionaries.
They install nothing and make no network call. The bounded Codex conversation
is the AI-assisted part; never place a secret or real work data in it.

## Follow along — I show you exactly how

### Prerequisites and start state

- Foundations 1–7 are complete.
- Windows Setup is complete, including the project virtual environment at
  `Documents\AI-workflow-learning\operations-exception-assistant\.venv`.
- PowerShell and Notepad are available.
- `Documents\controlled-ai-course-practice` exists.
- No secret, real dataset, or production repository is open.

### Start or resume safely — run this at every new PowerShell session

PowerShell forgets variables when you close its window. Run this whole block
whenever you start or resume Foundation 8:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$projectRoot = Join-Path $documentsPath "AI-workflow-learning\operations-exception-assistant"
$projectMarker = Join-Path $projectRoot "COURSE_PROJECT.md"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonFolderName = "foundation-08"
if ($lessonFolderName -notmatch '^foundation-08(?:-retry-\d{2,})?$') {
    throw "STOP: use foundation-08 or a retry name created by this lesson."
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

$expectedProjectMarker = @'
# Course 1 synthetic learner project

This folder is only for the fictional Course 1 practice project.
Never place real client, employer, medical, or personal data here.
'@
if (-not (Test-Path -LiteralPath $projectMarker -PathType Leaf)) {
    throw "STOP: the exact Course 1 project marker is missing. Return to Windows Setup."
}
$actualProjectMarker = (
    Get-Content -Raw -LiteralPath $projectMarker
) -replace "`r`n", "`n"
$normalizedExpectedProjectMarker = $expectedProjectMarker -replace "`r`n", "`n"
if ($actualProjectMarker -ne $normalizedExpectedProjectMarker) {
    throw "STOP: the Course 1 project marker is unfamiliar. Do not execute this folder."
}
$projectGitRoot = git -C $projectRoot rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "STOP: the marked Course 1 Git repository is missing or unreadable."
}
if (
    (Resolve-Path -LiteralPath $projectGitRoot).Path -ne
    (Resolve-Path -LiteralPath $projectRoot).Path
) {
    throw "STOP: Git resolves to a different repository root. Do not continue."
}
if (-not (Test-Path -LiteralPath $pythonExe -PathType Leaf)) {
    throw "STOP: the exact course Python file is missing. Return to Windows Setup; do not use a bare python command."
}
$pythonVersion = & $pythonExe --version
if ($LASTEXITCODE -ne 0 -or $pythonVersion -notmatch '^Python 3\.14\.\d+$') {
    throw "STOP: expected a stable Python 3.14 patch from the project virtual environment."
}
if (-not (Test-Path -LiteralPath $practiceRoot -PathType Container)) {
    throw "STOP: the controlled-ai-course-practice folder is missing. Return to Foundation 1."
}
if (Test-Path -LiteralPath $lessonPath -PathType Leaf) {
    throw "STOP: the selected Foundation 8 attempt is a file, not a folder. Do not change it."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new Foundation 8 attempt: $lessonFolderName"
}
else {
    "Existing Foundation 8 attempt found; nothing was overwritten: $lessonFolderName"
}

Set-Location -LiteralPath $lessonPath
Get-Location
$pythonExe
$pythonVersion
Get-ChildItem -Force
```

This derives the exact project interpreter from your real Documents path,
requires the exact synthetic Course 1 identity marker, confirms Git resolves
to that project rather than a parent or different repository, checks that the
interpreter exists, accepts only a stable Python 3.14 patch, creates the lesson
folder only when absent, and shows existing contents before you edit.
The displayed executable path must end in
`AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`,
and the current location must end in `foundation-08` or the selected numbered
retry name.

### Decide whether to resume or use a fresh attempt

The two helper functions have narrow jobs:
`New-FoundationRetryAttempt` creates the next unused retry folder;
`Open-GuardedPracticeFile` creates a named file only when absent, or displays an
existing file without opening it for editing.

Apply this decision before Part A and after every interruption:

1. An empty attempt continues at Part A.
2. The only expected names are `title_check.py`, `title_check_evidence.md`,
   `ai_priority_change_proposal.md`, `ai_priority_change_decision.md`,
   `priority_check.py`, and `priority_check_evidence.md`. For an attempt
   containing only those names, use each guarded step:
   - `EXISTING` plus exactly complete synthetic content means leave the file
     unchanged and skip its creation;
   - an absent expected file may be created;
   - incomplete, different, unfamiliar, or apparently real/sensitive content
     means do not execute, edit, rename, delete, or overwrite anything.
3. An unexpected item also requires a fresh attempt.
4. For either stop condition, run:

   ```powershell
   $lessonPath = New-FoundationRetryAttempt -BaseName "foundation-08" -PracticeRoot $practiceRoot
   $lessonFolderName = Split-Path -Leaf $lessonPath
   Set-Location -LiteralPath $lessonPath
   "Selected fresh attempt: $lessonFolderName"
   ```

5. Record the retry name. In a new PowerShell session, replace only
   `"foundation-08"` in `$lessonFolderName` with that exact name. Restart at
   Part A in the new empty folder.

### Part A — define the bounded requirement

The guided requirement is:

> Given one fictional record, return reason code `R001` when its `title` is
> missing, empty, or spaces only. Otherwise return `None`. Do not read or write
> a file and do not call a service.

Acceptance criteria:

1. `"Synthetic request"` returns `None`.
2. `""` returns `"R001"`.
3. `"   "` returns `"R001"`.
4. a missing `title` key returns `"R001"`.
5. the function has no side effect.

### Part B — create and run the smallest program

Make sure you ran the complete **Start or resume safely** block in this
PowerShell window. Confirm that `Get-ChildItem -Force` showed no unfamiliar or
real-data file.

Run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "title_check.py"
```

If it reports `EXISTING`, leave the file unchanged only when it exactly matches
the complete program below; otherwise use a fresh retry attempt and do not
execute it. Only after `CREATED ONCE` should you enter:

```python
def title_reason_code(record):
    title = record.get("title")
    if title is None or not str(title).strip():
        return "R001"
    return None


assert title_reason_code({"title": "Synthetic request"}) is None
assert title_reason_code({"title": ""}) == "R001"
assert title_reason_code({"title": "   "}) == "R001"
assert title_reason_code({}) == "R001"

print("4 title checks passed")
```

Save and close Notepad.

What the function does:

- `record.get("title")` reads the value safely and returns `None` if the key is
  absent;
- `str(title).strip()` turns a value into text and removes outer spaces;
- `not` is true when no text remains;
- the function returns only a reason code or `None`;
- it has no file, database, or network instruction.

Run:

```powershell
& $pythonExe ".\title_check.py"
```

Expected output:

```text
4 title checks passed
```

### Part C — record claim, evidence, and limitation

Run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "title_check_evidence.md"
```

If it reports `EXISTING`, leave the file unchanged only when it exactly matches
the completed evidence below; otherwise use a fresh retry attempt. Only after
`CREATED ONCE` should you enter:

```markdown
# Title-check evidence

Claim: the function reports R001 for a missing, empty, or spaces-only title.

Evidence: four assertions passed and the observed output was
`4 title checks passed`.

Side effects: none identified in the function.

Limitation: these four cases do not prove behaviour for every possible Python
value.
```

Save and close Notepad.

Run:

```powershell
Get-Content -LiteralPath ".\title_check.py"
```

What this does: it shows the exact saved program for your own review.

Run:

```powershell
(Get-Location).Path
```

What this does: it prints the exact full lesson-folder path for the Codex
check.

### Expected result — exact

- `title_check.py` contains one function and four assertions;
- running it prints exactly `4 title checks passed`;
- no package is installed and no file or network side effect occurs;
- `title_check_evidence.md` separates the claim, evidence, side effects, and
  limitation.

### Troubleshooting

- If an assertion fails, do not delete or edit it. Compare the displayed
  function with the acceptance criteria, preserve that attempt, and use a fresh
  retry.
- If the exact project Python reports a syntax or indentation error, compare
  punctuation and leading spaces with the sample, preserve that attempt, and
  use a fresh retry rather than overwriting the file.
- If `$pythonExe` is missing, not recognised, or reports the wrong version,
  rerun the complete **Start or resume safely** block. If it still stops,
  return to Windows Setup. Do not use a bare `python` command.
- If an assistant proposes installing a package for this function, reject that
  expansion; built-in Python is sufficient.
- If the selected attempt already exists, do not delete or overwrite it. Apply
  the attempt decision and use a fresh retry for any non-complete file.

## Now recreate it yourself

### Step 1 — Ask for a bounded proposal, not an automatic edit

Run `(Get-Location).Path` and copy the full Foundation 8 attempt path. Send this
prompt to Codex. **pandas** is a third-party Python data package; this small
rule does not need it.

```text
BOUNDED AI-ASSISTED CHANGE PROPOSAL — DO NOT EDIT FILES.

You may inspect READ-ONLY only this full synthetic practice folder:
[PASTE THE EXACT FOUNDATION-08 ATTEMPT PATH]

Read title_check.py only as a small style example. Do not create, edit, move,
rename, or delete anything. Do not inspect another path, use a network tool,
install a package, or run code.

Propose a unified diff that creates priority_check.py for this requirement:
- return R003 unless priority is exactly low, medium, or high;
- return None for those three values;
- have no file, log, database, package, or network side effect;
- include five assertions: low, medium, high, urgent, and missing;
- print exactly 5 priority checks passed.

Keep the diff minimal. After the diff, list any tempting optional expansions
that were deliberately excluded, including file logging, pandas, telemetry,
and network lookup. Do not claim the proposal works; it has not been run.
```

Codex's response is a proposal, not accepted code. Create the evidence file:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "ai_priority_change_proposal.md"
```

Only after `CREATED ONCE`, paste the complete proposal beneath the heading
`# AI priority-change proposal`. Save and close it.

### Step 2 — Inspect, challenge, and narrow the proposal

Before making your decision, inspect this fixed unsafe alternative as well.
It is deliberately over-scoped so that every learner has real lines to reject,
even when Codex produced a perfectly bounded proposal. **Do not apply any line
from this block.**

```diff
# UNSAFE-HUNK-01 — unnecessary dependency
+import pandas as pd

# UNSAFE-HUNK-02 — forbidden file side effect
+with open("priority-audit.log", "a") as log_file:
+    log_file.write(str(record))

# UNSAFE-HUNK-03 — forbidden network action
+import requests
+requests.post("https://example.invalid/lookup", json=record)

# UNSAFE-HUNK-04 — unrelated refactor
-def title_reason_code(record):
+def shared_reason_code(record, field_name):
```

The comments are hunk labels for this exercise. They are not a valid program
and are not suggestions. Reject all four because they add an unnecessary
dependency, file writing, a network action, and an unrelated change.

Create the decision file:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "ai_priority_change_decision.md"
```

Only after `CREATED ONCE`, complete:

```markdown
# AI priority-change decision

Requested outcome:
Must not change:

| Proposed part | Accept / narrow / reject | Evidence-based reason |
|---|---|---|
| actual Codex diff hunk/lines: [cite exact part] | | |
| actual Codex assertions/print hunk: [cite exact part] | | |
| UNSAFE-HUNK-01 — pandas dependency | REJECT | |
| UNSAFE-HUNK-02 — file logging | REJECT | |
| UNSAFE-HUNK-03 — network action | REJECT | |
| UNSAFE-HUNK-04 — unrelated refactor | REJECT | |

Diff inspected line by line: YES / NO
Accepted lines can be explained: YES / NO
All fixed unsafe hunks rejected: YES / NO
Actual proposal hunk accepted, narrowed, or rejected:
Test still required:
```

You must record a decision on at least one exact hunk or group of lines from
the actual Codex diff and reject all four fixed unsafe hunks. Optional ideas
that Codex already excluded do not count as rejection evidence. If the actual
diff itself includes file writing, a package, telemetry, network access,
unrelated refactoring, or a changed acceptance criterion, cite and reject
those lines too. Do not apply the proposal unchanged merely because Codex
produced it.

### Step 3 — Apply only the accepted bounded part yourself

Run the recreation program's create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "priority_check.py"
```

If it reports `EXISTING`, leave the file unchanged only when it already meets
every requirement and assertion below; otherwise use a fresh retry attempt and
do not execute it. After `CREATED ONCE`, type only the lines you accepted from
the proposal. The meaningfully different requirement is:

> Return reason code `R003` unless `priority` is exactly `low`, `medium`, or
> `high`. Return `None` for those three allowed values. Have no side effects.

Include five assertions:

- `low`, `medium`, and `high` each return `None`;
- `urgent` returns `R003`;
- a missing `priority` key returns `R003`.

Print exactly `5 priority checks passed`. Do not copy the title function and
merely rename the file. Explain why a list membership check is appropriate for
this new rule.

Before running it, display the exact applied file and compare it line by line
with `ai_priority_change_decision.md`:

```powershell
Get-Content -LiteralPath ".\priority_check.py"
```

### Step 4 — Test the accepted change

Run the recreation with the exact project interpreter:

```powershell
& $pythonExe ".\priority_check.py"
```

Only after the program prints its exact success message, run:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "priority_check_evidence.md"
```

Leave an `EXISTING` file unchanged only when it is complete; otherwise use a
fresh retry attempt. After `CREATED ONCE`, record the claim, exact observed
output, side-effect assessment, one honest limitation, the accepted diff
boundary, and the rejected or narrowed expansion.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PRACTICE-FOLDER PATH]` with the full path output from
`(Get-Location).Path`. Replace `[PASTE THE EXACT PROJECT PYTHON PATH]` with the
full path printed for `$pythonExe` by the **Start or resume safely** block.

```text
You may access exactly these two locations, for only these purposes:
1. Inspect READ-ONLY this one practice folder:
   [PASTE THE EXACT PRACTICE-FOLDER PATH]
2. Execute, but do not edit or replace, this one project Python file:
   [PASTE THE EXACT PROJECT PYTHON PATH]

Do not browse, list, read, or inspect any other folder or file. Do not create,
edit, move, rename, or delete anything. Do not install a package, change Git
state or settings, or contact any external service.

Report PASS or NOT YET for each criterion:
1. title_check.py returns None for a normal title and R001 for empty,
   spaces-only, and missing title, with four assertions.
2. Running title_check.py is expected to print exactly:
   4 title checks passed
3. priority_check.py returns None for low/medium/high and R003 for urgent and a
   missing priority, with five assertions.
4. Running priority_check.py is expected to print exactly:
   5 priority checks passed
5. Both functions have no file, database, package-installation, or network side
   effect.
6. Both function evidence files state claim, observed evidence, side effects,
   and a limitation.
7. ai_priority_change_proposal.md preserves the actual AI proposal and does not
   claim it passed before execution.
8. ai_priority_change_decision.md records a line-by-line inspection, a decision
   on at least one exact hunk or line group from the actual Codex proposal,
   rejection of UNSAFE-HUNK-01 through UNSAFE-HUNK-04 with a plain-language
   reason for each, accepted bounded lines, and the remaining test requirement.

First inspect each local Python file. If a file could change a file, setting, or
external system, do not execute it; report NOT YET. Otherwise, you may use only
the authorised project Python file to run title_check.py and priority_check.py
from the authorised practice folder. This execution is part of the read-only
check: it may print output but must not change anything. Do not use a bare
python command. Explain NOT YET in beginner language.
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

- [ ] Both programs print their exact expected pass messages.
- [ ] The exact Course 1 project marker and resolved Git root matched before
      project Python ran.
- [ ] Both programs were run through the derived project `$pythonExe`, which
      reports a stable Python 3.14 patch.
- [ ] I can explain each function's input, output, and absence of side effects.
- [ ] I can connect every assertion to one acceptance criterion.
- [ ] Both evidence files distinguish claim, evidence, and limitation.
- [ ] The actual bounded AI proposal and my inspection decision are preserved.
- [ ] I cited and decided at least one exact hunk or line group from the actual
      Codex proposal, rejected UNSAFE-HUNK-01 through UNSAFE-HUNK-04, and can
      explain every accepted line.
- [ ] I tested the applied file after inspection; the proposal itself is not
      recorded as proof.
- [ ] I can explain why generated code and commands remain proposals.
- [ ] No dependency or network call was introduced. I attest that all
      information I entered was synthetic and that I did not intentionally add
      secrets or real data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
