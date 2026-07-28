# Foundation 3 — Reading Code and the Python Programming Language

## Outcome

You will create and run a small Python program, use three exact checks, and
explain its input, decision, output, and failure risk.

## Words you need first

- **Code** is a precise set of instructions written for a computer.
- **Python** is the programming language used for small, testable components in
  this course.
- **PowerShell** is the Windows command shell used to run the Python examples.
- **Notepad** is the Windows plain-text editor used to create the example files.
- A **Python source file** contains Python code and normally ends in `.py`.
- A **program** is code arranged to perform a task.
- A **variable** gives a name to a value.
- A **string** is text, such as `"waiting"`.
- A **Boolean** is either `True` or `False`.
- A **list** is an ordered collection of values in Python.
- A **membership check** asks whether a value appears in a collection.
- A **function** is a named, reusable block of code.
- An **input** is a value supplied to a function.
- An **output** is a value returned by a function.
- A **condition** chooses a path based on a true-or-false expression.
- A **test** compares observed behaviour with an expected result.
- An **assertion** is a test instruction that stops with an error if its
  condition is false.
- **Syntax** is the grammar of code. A syntax error means Python cannot
  understand the written structure.
- A **package** is an installable collection of code.
- A **network call** communicates with another computer or online service.
- A **credential** is a secret value, such as a password, key, or token, that
  can grant access.
- A **dataset** is a collection of related records used together.
- **Git** is the version-control tool installed during Windows Setup; its name
  is not an abbreviation. A **repository root** is the exact top-level project
  folder Git tracks.
- `COURSE_PROJECT.md` is the synthetic-project identity marker created by
  Windows Setup. A **resolved path** is the full unambiguous Windows path after
  folder shortcuts and relative pieces have been resolved.
- **Codex** is the artificial intelligence (AI) assistant used for the final
  read-only check. The check prompt limits file inspection to one practice
  folder and permits only the exact project Python file to execute the named
  local checks without making a change.

A program that runs is not automatically correct. Tests establish only the
specific examples and rules they exercise.

## Safety boundary

This lesson uses no package installation, network call, deletion, or real data.
Do not paste private code, credentials, or business records into an assistant.

## Follow along — I show you exactly how

### Prerequisites and start state

- Foundations 1 and 2 are complete.
- `Documents\controlled-ai-course-practice` exists.
- Windows Setup is complete, including the project virtual environment at
  `Documents\AI-workflow-learning\operations-exception-assistant\.venv`.
- PowerShell is closed or showing a ready prompt.

### Start or resume safely — run this at every new PowerShell session

PowerShell forgets variables when you close its window. Therefore, run this
whole block whenever you start or resume Foundation 3. On the first attempt,
leave `$lessonFolderName` as `foundation-03`. If the recovery decision below
created a numbered retry, replace only that quoted value with the exact retry
name PowerShell displayed:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$projectRoot = Join-Path $documentsPath "AI-workflow-learning\operations-exception-assistant"
$projectMarker = Join-Path $projectRoot "COURSE_PROJECT.md"
$expectedMarker = @'
# Course 1 synthetic learner project

This folder is only for the fictional Course 1 practice project.
Never place real client, employer, medical, or personal data here.
'@
if (-not (Test-Path -LiteralPath $projectMarker -PathType Leaf)) {
    throw "STOP: the exact Course 1 project marker is missing. Return to Windows Setup; do not execute project Python."
}
$actualMarker = (Get-Content -Raw -LiteralPath $projectMarker) -replace "`r`n", "`n"
$normalizedExpectedMarker = $expectedMarker -replace "`r`n", "`n"
if ($actualMarker -ne $normalizedExpectedMarker) {
    throw "STOP: the Course 1 project marker is unfamiliar. Do not enter or execute this folder."
}
$savedGitRoot = git -C $projectRoot rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "STOP: the marked Course 1 Git repository is missing or unreadable. Return to Windows Setup."
}
$resolvedProjectRoot = (Resolve-Path -LiteralPath $projectRoot).Path
$resolvedGitRoot = (Resolve-Path -LiteralPath $savedGitRoot).Path
if ($resolvedGitRoot -ne $resolvedProjectRoot) {
    throw "STOP: Git resolves to a different repository root. Do not execute project Python."
}
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonFolderName = "foundation-03"
if ($lessonFolderName -notmatch '^foundation-03(?:-retry-\d{2,})?$') {
    throw "STOP: use foundation-03 or a retry name created by this lesson."
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
    throw "STOP: the selected Foundation 3 attempt is a file, not a folder. Do not change it; use a fresh retry attempt."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new Foundation 3 attempt: $lessonFolderName"
}
else {
    "Existing Foundation 3 attempt found; nothing was overwritten: $lessonFolderName"
}

Set-Location -LiteralPath $lessonPath
Get-Location
$pythonExe
$pythonVersion
Get-ChildItem -Force
```

What this does:

- `$projectRoot` derives the one Course 1 project path from your real Windows
  Documents location;
- the exact `COURSE_PROJECT.md` check proves that the folder still has the
  complete synthetic Course 1 identity marker written by Windows Setup;
- `git rev-parse --show-toplevel` asks Git for the repository root, and the two
  resolved full paths must match before any project Python can run;
- `$pythonExe` stores the exact
  `AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`
  path, and `&` runs that exact file;
- `Test-Path` stops the lesson if that file or either required folder is
  missing;
- the version check accepts only a stable Python 3.14 patch such as
  `Python 3.14.6`, not an alpha, beta, or release candidate;
- the `if` block creates only the selected Foundation 3 attempt when absent;
- `New-FoundationRetryAttempt` creates only the next unused numbered retry
  when you deliberately call it;
- `Open-GuardedPracticeFile` creates a named file only when absent, or displays
  an existing file without opening it for editing;
- `Get-ChildItem -Force` shows existing contents before you edit anything.

Expected result: the location ends in
`controlled-ai-course-practice\foundation-03` or the selected numbered retry
name; the displayed executable path ends in
`AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`;
and the version is `Python 3.14` followed by a patch number. If existing files
are listed, apply the decision below before opening them.

### Decide whether to resume or use a fresh attempt

Apply this decision before Part B and again after every interruption:

1. An empty selected attempt continues at Part B.
2. The only expected names are `status_check.py`, `known_status.py`, and
   `priority_check.py`.
3. For an attempt containing only those names, use each guarded file step:
   - `EXISTING` plus exactly complete synthetic code means leave the file
     unchanged and skip its creation;
   - an absent expected file may be created;
   - incomplete, different, unfamiliar, wrong-kind, or apparently
     real/sensitive content means do not execute, edit, rename, delete, or
     overwrite anything in that attempt.
4. An unexpected item also requires a fresh attempt.
5. For either stop condition, run:

   ```powershell
   $lessonPath = New-FoundationRetryAttempt -BaseName "foundation-03" -PracticeRoot $practiceRoot
   $lessonFolderName = Split-Path -Leaf $lessonPath
   Set-Location -LiteralPath $lessonPath
   "Selected fresh attempt: $lessonFolderName"
   ```

   `Split-Path -Leaf` reads only the final folder name from the complete retry
   path; it does not move or change the folder.

6. Write down the displayed retry name. In a new PowerShell session, replace
   only `"foundation-03"` in `$lessonFolderName` with that exact name. Restart
   at Part B in the new empty attempt.

### Part B — write a function and its tests

1. Run this create-once guard:

   ```powershell
   Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "status_check.py"
   ```

   What this does: for an absent file, it creates the file once and opens that
   new file in Notepad. For an existing file, it displays the content without
   opening it for editing.

2. Leave an `EXISTING` file unchanged only when it exactly matches the complete
   program below; then continue to Part C. Any incomplete, different,
   unfamiliar, wrong-kind, or apparently real content requires a fresh retry
   attempt.
3. Only after `CREATED ONCE`, enter this exact code:

   ```python
   def needs_review(status):
       if status == "completed":
           return False
       return True


   assert needs_review("waiting") is True
   assert needs_review("completed") is False
   assert needs_review("") is True

   print("3 checks passed")
   ```

4. Click **File**, then **Save**. Close Notepad.

What the code does:

- `def` defines the function named `needs_review`.
- `status` is the input variable.
- `if` checks whether the input equals the string `"completed"`.
- `return False` is the output for completed work.
- every other input reaches `return True`;
- the three `assert` lines test waiting, completed, and blank input;
- `print` displays a message only after every assertion passes.

Python uses indentation to show which lines belong inside a function or
condition. The four spaces before the indented lines matter.

### Part C — use a list and the Python word `in`

The recreation below will ask you to use a list and a membership check. First
you will build and run one complete example.

1. Run this create-once guard:

   ```powershell
   Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "known_status.py"
   ```

2. Leave an `EXISTING` file unchanged only when it exactly matches the complete
   program below; then continue to Part D. Any incomplete, different,
   unfamiliar, wrong-kind, or apparently real content requires a fresh retry
   attempt.
3. Only after `CREATED ONCE`, enter this exact code:

   ```python
   def is_known_status(status):
       allowed_statuses = ["waiting", "in_progress", "completed"]
       return status in allowed_statuses


   assert is_known_status("waiting") is True
   assert is_known_status("completed") is True
   assert is_known_status("cancelled") is False

   print("3 membership checks passed")
   ```

4. Save and close Notepad, then run:

   ```powershell
   & $pythonExe ".\known_status.py"
   ```

Expected result:

```text
3 membership checks passed
```

Here, `allowed_statuses` is a list because the values are inside square
brackets. The expression `status in allowed_statuses` is `True` when the input
appears in that list and `False` when it does not. The function returns that
Boolean directly. You will reuse this pattern with different values in the
recreation.

### Part D — run and inspect the first program

1. In PowerShell, run:

   ```powershell
   & $pythonExe ".\status_check.py"
   ```

   What this does: Python reads and executes the local file. `.\` means “in the
   current folder.”

2. Run:

   ```powershell
   Get-ChildItem
   ```

3. Run:

   ```powershell
   Get-Content -LiteralPath "status_check.py"
   ```

   What the last two actions do: they confirm which file exists and show the
   exact saved code.

4. Run:

   ```powershell
   (Get-Location).Path
   ```

   What this does: it prints the exact full path. Save it for the Codex check.

### Expected result — exact

Running the program prints exactly:

```text
3 checks passed
```

No Python error appears. `Get-ChildItem` includes `status_check.py` and
`known_status.py`. The saved files contain the demonstrated assertions.

### Troubleshooting

- If `$pythonExe` is missing, not recognised, or reports the wrong version,
  rerun the complete **Start or resume safely** block. If it still stops,
  return to Windows Setup. Do not use a bare `python` command and do not
  download a similarly named package from an unverified site.
- If Python reports `IndentationError`, compare the leading spaces with the
  sample. Preserve that attempt and use a fresh retry with the demonstrated
  indentation; do not edit the existing file or use random tabs and spaces.
- If an assertion fails, Python prints `AssertionError`. Compare the function
  and that assertion with the exact sample, preserve the attempt, and use a
  fresh retry instead of deleting or editing the test.
- If Notepad saved `status_check.py.txt`, turn on extensions as taught in
  Foundation 1. Preserve that attempt and use a fresh retry with the correct
  `.py` name instead of renaming or overwriting the item.

## Now recreate it yourself

First make sure you ran the complete **Start or resume safely** block in this
PowerShell window. Then run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "priority_check.py"
```

Leave an `EXISTING` file unchanged only when it already meets every requirement
below. Any incomplete, different, unfamiliar, wrong-kind, or apparently real
content requires a fresh retry attempt and must not be executed. Only after
`CREATED ONCE`, create `priority_check.py` in the selected Foundation 3 attempt.

It must:

1. define a function named `is_allowed_priority` with one input named
   `priority`;
2. return `True` for `"low"`, `"medium"`, and `"high"`;
3. return `False` for `"urgent"` and for a blank string;
4. contain five assertions covering those five inputs;
5. print exactly `5 priority checks passed` only after the assertions pass.

Use a list such as `["low", "medium", "high"]` and the Python word `in` to
test membership. This is a different rule and dataset from the guided example.
Run the program yourself with the exact project interpreter:

```powershell
& $pythonExe ".\priority_check.py"
```

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
edit, move, rename, or delete anything. Do not install packages, change
settings, or contact an external system.

Report PASS or NOT YET for each criterion:
1. status_check.py defines needs_review and contains the three required
   assertions.
2. The expected output from status_check.py is exactly: 3 checks passed
3. known_status.py demonstrates a list and the Python word in, and its expected
   output is exactly: 3 membership checks passed
4. priority_check.py defines is_allowed_priority.
5. It accepts low, medium, and high; rejects urgent and blank; and contains five
   assertions for those inputs.
6. The expected output from priority_check.py is exactly:
   5 priority checks passed
7. None of the three files reads, writes, deletes, installs, or calls a network
   service.

First inspect each local Python file. If a file could change a file, setting, or
external system, do not execute it; report NOT YET. Otherwise, you may use only
the authorised project Python file to run status_check.py, known_status.py, and
priority_check.py from the authorised practice folder. This execution is part
of the read-only check: it may print output but must not change anything. Do not
use a bare python command. Explain any NOT YET result in beginner language.

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

- [ ] The derived `$pythonExe` path ends in
      `AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`
      and reports a stable Python 3.14 patch.
- [ ] The exact Course 1 project marker and resolved Git root matched before
      project Python ran.
- [ ] The selected attempt is `foundation-03` or the exact numbered
      `foundation-03-retry-XX` folder whose full path I gave to Codex.
- [ ] `status_check.py` prints exactly `3 checks passed`.
- [ ] `known_status.py` prints exactly `3 membership checks passed`.
- [ ] I can explain the list and the membership check demonstrated before the
      recreation.
- [ ] `priority_check.py` prints exactly `5 priority checks passed`.
- [ ] I can explain each function's input, condition, and Boolean output.
- [ ] I can explain why an assertion is stronger evidence than seeing no error.
- [ ] I know that these five examples do not prove every possible input.
- [ ] No package or service was used. I attest that all information I entered
      was synthetic and that I did not intentionally add secrets or real
      business data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
