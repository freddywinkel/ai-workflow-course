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
- **Codex** is the artificial intelligence (AI) assistant used for the final
  read-only check. The check prompt limits it to one practice folder.

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
whole block whenever you start or resume Foundation 3:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$projectRoot = Join-Path $documentsPath "AI-workflow-learning\operations-exception-assistant"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonPath = Join-Path $practiceRoot "foundation-03"

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
    throw "STOP: foundation-03 is a file, not a folder. Do not rename or delete it; ask Codex to inspect read-only."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new foundation-03 folder."
}
else {
    "Existing foundation-03 folder found; nothing was overwritten."
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
- `$pythonExe` stores the exact
  `AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`
  path, and `&` runs that exact file;
- `Test-Path` stops the lesson if that file or either required folder is
  missing;
- the version check accepts only a stable Python 3.14 patch such as
  `Python 3.14.6`, not an alpha, beta, or release candidate;
- the `if` block creates `foundation-03` only when it is absent;
- `Get-ChildItem -Force` shows existing contents before you edit anything.

Expected result: the location ends in
`controlled-ai-course-practice\foundation-03`; the displayed executable path
ends in
`AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`;
and the version is `Python 3.14` followed by a patch number. If existing files
are listed, inspect them before continuing. Do not delete the folder or paste
over a file automatically.

### Part B — write a function and its tests

1. Run this non-overwriting check:

   ```powershell
   $statusCheckPath = Join-Path $lessonPath "status_check.py"
   if (Test-Path -LiteralPath $statusCheckPath) {
       "Existing status_check.py found; it was not opened or overwritten."
       Get-Item -LiteralPath $statusCheckPath
   }
   else {
       notepad $statusCheckPath
   }
   ```

   What this does: for a new attempt, it opens Notepad with the correct new
   path. For a resumed attempt, it reports the existing item without changing
   it.

2. If an existing file was reported, first run
   `Get-Content -LiteralPath $statusCheckPath` to inspect it. If it is your own
   incomplete synthetic attempt, run `notepad $statusCheckPath` and correct
   only the unfinished work. If it is already complete, leave it unchanged and
   continue to Part C. If it is unfamiliar, is a folder, or contains real
   data, stop and ask Codex for read-only help.
3. For a new file, if Notepad asks whether to create it, click **Yes**.
4. For a new or deliberately resumed incomplete file, enter this exact code:

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

5. Click **File**, then **Save**. Close Notepad.

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

1. Run this non-overwriting check:

   ```powershell
   $knownStatusPath = Join-Path $lessonPath "known_status.py"
   if (Test-Path -LiteralPath $knownStatusPath) {
       "Existing known_status.py found; it was not opened or overwritten."
       Get-Item -LiteralPath $knownStatusPath
   }
   else {
       notepad $knownStatusPath
   }
   ```

2. If an existing file was reported, inspect it with
   `Get-Content -LiteralPath $knownStatusPath`. Resume only your own incomplete
   synthetic attempt. Leave a complete file unchanged. Stop if the item is
   unfamiliar, is a folder, or contains real data.
3. For a new file, if Notepad asks whether to create it, click **Yes**.
4. For a new or deliberately resumed incomplete file, enter this exact code:

   ```python
   def is_known_status(status):
       allowed_statuses = ["waiting", "in_progress", "completed"]
       return status in allowed_statuses


   assert is_known_status("waiting") is True
   assert is_known_status("completed") is True
   assert is_known_status("cancelled") is False

   print("3 membership checks passed")
   ```

5. Save and close Notepad, then run:

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
  sample. Do not use random tabs and spaces.
- If an assertion fails, Python prints `AssertionError`. Compare the function
  and that assertion with the exact sample instead of deleting the test.
- If Notepad saved `status_check.py.txt`, turn on extensions as taught in
  Foundation 1 and correct only the final `.txt`.

## Now recreate it yourself

First make sure you ran the complete **Start or resume safely** block in this
PowerShell window. Then run:

```powershell
$priorityCheckPath = Join-Path $lessonPath "priority_check.py"
if (Test-Path -LiteralPath $priorityCheckPath) {
    "Existing priority_check.py found; inspect it before deciding what remains."
    Get-Item -LiteralPath $priorityCheckPath
}
else {
    "No priority_check.py exists yet; it is safe to create this new file."
}
```

If the file exists, inspect it with
`Get-Content -LiteralPath $priorityCheckPath`. Resume only your own incomplete
synthetic attempt and leave a completed file unchanged. If it is unfamiliar,
is a folder, or contains real data, stop and ask for read-only help.

Create `priority_check.py` in `foundation-03`. It must:

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

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, or delete anything. Do not run any command
that changes files, installs packages, or contacts an external system.

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

You may reason about the code and, if your environment permits, derive only
Documents\AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe
and use that exact executable to run these three local files. Do not use a bare
python command. Make no changes. Explain any NOT YET result in beginner
language.

This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] The derived `$pythonExe` path ends in
      `AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`
      and reports a stable Python 3.14 patch.
- [ ] `status_check.py` prints exactly `3 checks passed`.
- [ ] `known_status.py` prints exactly `3 membership checks passed`.
- [ ] I can explain the list and the membership check demonstrated before the
      recreation.
- [ ] `priority_check.py` prints exactly `5 priority checks passed`.
- [ ] I can explain each function's input, condition, and Boolean output.
- [ ] I can explain why an assertion is stronger evidence than seeing no error.
- [ ] I know that these five examples do not prove every possible input.
- [ ] No package, service, secret, or real business data was used.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
