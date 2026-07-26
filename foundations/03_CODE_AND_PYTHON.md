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
- Python is installed using the course setup instructions.
- PowerShell is closed or showing a ready prompt.

### Part A — create the lesson folder

1. Open PowerShell: press the Windows key, type `PowerShell`, and click the
   result.
2. Run:

   ```powershell
   Set-Location ([Environment]::GetFolderPath("MyDocuments"))
   ```

3. Run:

   ```powershell
   Set-Location "controlled-ai-course-practice"
   ```

4. Run:

   ```powershell
   New-Item -ItemType Directory -Path "foundation-03"
   ```

5. Run:

   ```powershell
   Set-Location "foundation-03"
   ```

   What steps 2–5 do: they enter your Windows Documents folder, enter the
   existing practice root, create only the `foundation-03` folder, and then
   enter it.

6. Run:

   ```powershell
   python --version
   ```

   What this does: it asks the installed Python program for its version without
   running your code.

   Expected result: output begins with `Python 3.` and then returns to the
   prompt.

### Part B — write a function and its tests

1. Run:

   ```powershell
   notepad "status_check.py"
   ```

   What this does: it opens or creates a plain-text Python file in the current
   practice folder.

2. If Notepad asks whether to create the file, click **Yes**.
3. Type or paste this exact code:

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

### Part C — run and inspect the program

1. In PowerShell, run:

   ```powershell
   python ".\status_check.py"
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

No Python error appears. `Get-ChildItem` includes `status_check.py`, and the
saved file contains three assertions.

### Troubleshooting

- If `python` is not recognised, stop. Return to the course Windows setup; do
  not download a similarly named package from an unverified site.
- If Python reports `IndentationError`, compare the leading spaces with the
  sample. Do not use random tabs and spaces.
- If an assertion fails, Python prints `AssertionError`. Compare the function
  and that assertion with the exact sample instead of deleting the test.
- If Notepad saved `status_check.py.txt`, turn on extensions as taught in
  Foundation 1 and correct only the final `.txt`.

## Now recreate it yourself

Create `priority_check.py` in `foundation-03`. It must:

1. define a function named `is_allowed_priority` with one input named
   `priority`;
2. return `True` for `"low"`, `"medium"`, and `"high"`;
3. return `False` for `"urgent"` and for a blank string;
4. contain five assertions covering those five inputs;
5. print exactly `5 priority checks passed` only after the assertions pass.

Use a list such as `["low", "medium", "high"]` and the Python word `in` to
test membership. This is a different rule and dataset from the guided example.
Run the program yourself.

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
3. priority_check.py defines is_allowed_priority.
4. It accepts low, medium, and high; rejects urgent and blank; and contains five
   assertions for those inputs.
5. The expected output from priority_check.py is exactly:
   5 priority checks passed
6. Neither file reads, writes, deletes, installs, or calls a network service.

You may reason about the code and, if your environment permits, run only these
two local Python files to observe their output. Make no changes. Explain any
NOT YET result in beginner language.

This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] `python --version` reports Python 3.
- [ ] `status_check.py` prints exactly `3 checks passed`.
- [ ] `priority_check.py` prints exactly `5 priority checks passed`.
- [ ] I can explain each function's input, condition, and Boolean output.
- [ ] I can explain why an assertion is stronger evidence than seeing no error.
- [ ] I know that these five examples do not prove every possible input.
- [ ] No package, service, secret, or real business data was used.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
