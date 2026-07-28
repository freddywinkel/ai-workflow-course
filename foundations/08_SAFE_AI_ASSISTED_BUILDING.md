# Foundation 8 — Safe Artificial Intelligence (AI)-Assisted Building

A **function** is a named, reusable block of code. A **claim** is a statement
presented as true, **evidence** is material that supports it, and a
**limitation** states what the evidence does not establish. **Codex** is the AI
assistant used for the final read-only check.

## Outcome

You will create and test one small data-quality function, record the evidence
for its claim, and then transfer the method to a different rule. Codex will
inspect the final practice folder without changing it.

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

This lesson uses only built-in Python and fictional dictionaries. It installs
nothing and makes no network call.

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
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonPath = Join-Path $practiceRoot "foundation-08"

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
    throw "STOP: foundation-08 is a file, not a folder. Do not rename or delete it; ask Codex to inspect read-only."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new foundation-08 folder."
}
else {
    "Existing foundation-08 folder found; nothing was overwritten."
}

Set-Location -LiteralPath $lessonPath
Get-Location
$pythonExe
$pythonVersion
Get-ChildItem -Force
```

This derives the exact project interpreter from your real Documents path,
checks that it exists, accepts only a stable Python 3.14 patch, creates the
lesson folder only when absent, and shows existing contents before you edit.
The displayed executable path must end in
`AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe`,
and the current location must end in
`controlled-ai-course-practice\foundation-08`.

If existing files are listed, inspect them before continuing. Resume only your
own synthetic lesson attempt. Do not overwrite unfamiliar material and do not
use a folder containing real data.

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

Run:

```powershell
notepad "title_check.py"
```

Enter:

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

Run:

```powershell
notepad "title_check_evidence.md"
```

Enter:

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

- If an assertion fails, do not delete it. Compare the function and input with
  the stated acceptance criteria.
- If the exact project Python reports a syntax or indentation error, compare
  punctuation and leading spaces with the sample.
- If `$pythonExe` is missing, not recognised, or reports the wrong version,
  rerun the complete **Start or resume safely** block. If it still stops,
  return to Windows Setup. Do not use a bare `python` command.
- If an assistant proposes installing a package for this function, reject that
  expansion; built-in Python is sufficient.
- If `foundation-08` already exists, do not delete it. Inspect its contents
  before continuing.

## Now recreate it yourself

Create `priority_check.py` for a meaningfully different requirement:

> Return reason code `R003` unless `priority` is exactly `low`, `medium`, or
> `high`. Return `None` for those three allowed values. Have no side effects.

Include five assertions:

- `low`, `medium`, and `high` each return `None`;
- `urgent` returns `R003`;
- a missing `priority` key returns `R003`.

Print exactly `5 priority checks passed`. Create
`priority_check_evidence.md` with the claim, exact observed output, side-effect
assessment, and one honest limitation.

Do not copy the title function and merely rename the file. Explain why a list
membership check is appropriate for this new rule.

Run the recreation with the exact project interpreter:

```powershell
& $pythonExe ".\priority_check.py"
```

## Ask Codex to check your work

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, or delete anything. Do not install a
package, change Git state, or contact any external service.

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
6. Both evidence files state claim, observed evidence, side effects, and a
   limitation.

You may derive only
Documents\AI-workflow-learning\operations-exception-assistant\.venv\Scripts\python.exe
and use that exact executable to run the two local Python files. Do not use a
bare python command. Make no changes. Explain NOT YET in beginner language.
This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] Both programs print their exact expected pass messages.
- [ ] Both programs were run through the derived project `$pythonExe`, which
      reports a stable Python 3.14 patch.
- [ ] I can explain each function's input, output, and absence of side effects.
- [ ] I can connect every assertion to one acceptance criterion.
- [ ] Both evidence files distinguish claim, evidence, and limitation.
- [ ] I can explain why generated code and commands remain proposals.
- [ ] No dependency, network call, secret, or real data was introduced.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
