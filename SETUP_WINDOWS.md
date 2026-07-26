# Windows Setup — Course 1

## Goal

Create a local learning environment for the **Synthetic Small and Medium-sized
Enterprise (SME) Operations Exception Assistant**. It uses only fictional data
and remains separate from employer or client systems.

## Before you begin

Finish Foundations 1 and 2 first. They teach folders, paths, plain text, and
the Windows **command line**, a text-based way to give the computer
instructions, using built-in software. This setup then installs **Python**, a
programming language, and **Git**, a version-control tool that records file
changes, before Foundations 3–5 ask you to use them. If folder, path, file, or
command is still unfamiliar, repeat the matching worked example instead of
guessing.

Terms used in this guide:

- **artificial intelligence (AI):** software that can generate or classify
  content but may still produce incorrect results;
- **File Explorer:** the Windows application for viewing files and folders;
- **Notepad:** the plain-text editor included with Windows;
- **Windows PowerShell:** the built-in Windows command-line tool used in this
  guide;
- **Visual Studio Code:** a text and code editor;
- **Git:** a version-control tool that records changes to files in a
  **repository**, the project folder Git tracks; Git is a name, not an
  abbreviation;
- **Python:** the programming language used for the **capstone**, the final
  project that combines all course modules;
- **virtual environment:** an isolated folder containing the Python
  **packages**, reusable units of code, for one project;
- **Node.js:** software that runs JavaScript, a programming language used by
  websites and automation tools, outside a web browser;
- **n8n** (pronounced “n-eight-n”): a workflow-automation application; the name
  is not an abbreviation you need to expand;
- **comma-separated values (CSV):** a plain-text table format;
- **application programming interface (API):** a defined way for software
  systems to exchange requests and responses;
- **pytest:** the Python testing tool used in this course;
- **secret:** a password-like value, such as an access key, that must not be
  shared or stored in tracked course files;
- **Codex:** the course workspace assistant you are using now. A **read-only**
  Codex check may inspect and explain named files but may not change them.

Work through one numbered action at a time. Compare the observed result with
the expected result before continuing. If your screen or output differs, stop
and ask Codex to explain the difference. Do not keep clicking or pasting
commands at random.

## Follow along — I show you exactly how

This first rehearsal creates a harmless practice folder. It does not install
anything and does not touch the final capstone.

### A. Create the rehearsal folder with File Explorer

1. Press `Windows key + E`. This opens **File Explorer**, the Windows
   application for viewing files and folders.
2. In the left side of File Explorer, select **Documents**.
3. Select **New → Folder**.
4. Type `controlled-ai-course-practice`, then press `Enter`.
5. Open `controlled-ai-course-practice`.
6. Select **New → Folder** again.
7. Type `setup-follow-along`, then press `Enter`.
8. Open `setup-follow-along`.
9. Select **View → Show → File name extensions**. A check mark should appear.
10. Right-click an empty area and select **New → Text Document**.
11. Rename the file to `setup-check.txt`.
12. Open the file in **Notepad**, the plain-text editor included with Windows,
    and type:

    ```text
    This is a fictional Course 1 setup rehearsal.
    I know the full folder path.
    I will not put secrets or real work data here.
    ```

13. Press `Ctrl+S`—hold the Control key and tap S—to save, then close Notepad.
14. Reopen `setup-check.txt` and confirm the three lines remain.

Expected result:

```text
Documents
└── controlled-ai-course-practice
    └── setup-follow-along
        └── setup-check.txt
```

If you see `setup-check.txt.txt`, remove only the extra final `.txt`. Do not
delete the entire file.

### B. Inspect the same folder with PowerShell

1. Select the Windows **Start** button.
2. Type `PowerShell`.
3. Open **Windows PowerShell**. PowerShell is the Windows tool in which you
   type commands.
4. The next command uses `Set-Location` to change the folder affected by later
   commands. `$env:USERPROFILE` is an **environment variable**, a Windows
   setting that contains the path to your own user folder, so you do not need
   to type your account name. Copy the command, paste it into PowerShell, and
   press `Enter`:

    ```powershell
    Set-Location "$env:USERPROFILE\Documents\controlled-ai-course-practice\setup-follow-along"
    ```

5. `Get-Location` prints the current folder without changing it. Run:

    ```powershell
    Get-Location
    ```

   Expected result: the printed path ends with
   `Documents\controlled-ai-course-practice\setup-follow-along`.

6. `Get-ChildItem` lists the items inside the current folder without changing
   them. Run:

    ```powershell
    Get-ChildItem
    ```

   Expected result: `setup-check.txt` appears in the list.

7. `Get-Content` prints the text stored in a file without changing it. The
   `.\` at the start means “inside the current folder.” Run:

    ```powershell
    Get-Content ".\setup-check.txt"
    ```

   Expected result: PowerShell prints the same three lines you typed.

Do not continue if `Get-Location` points somewhere else. Run the
`Set-Location` command again and check it.

## Install the required tools once

The interfaces and supported versions can change. First run the live check in
[EVERGREEN_UPDATE_PROMPT.md](EVERGREEN_UPDATE_PROMPT.md). It must confirm the
current official download pages and supported versions.

Record the checked date and answers in a Notepad file named
`setup-version-check.txt` inside `setup-follow-along`.

### 1. Install Visual Studio Code

1. Open <https://code.visualstudio.com/download>.
2. A Windows **User Installer** installs the application for your Windows
   account rather than for every account on the computer. Choose the User
   Installer for your computer.
3. Open the downloaded installer.
4. Read each screen. Keep the default installation folder.
5. **PATH** is the list of folders Windows searches when you type a command. If
   offered, enable **Add to PATH** and **Add “Open with Code” action**.
6. Finish the installation and open Visual Studio Code.
7. Select **File → Open Folder** and open
   `Documents\controlled-ai-course-practice\setup-follow-along`.
8. Confirm `setup-check.txt` is visible in the Explorer panel on the left.

### 2. Install Git for Windows

1. Open <https://git-scm.com/download/win>.
2. **64-bit** describes the standard processor and Windows type on most modern
   computers; your live version check should confirm the correct installer.
   Download and open the official 64-bit installer unless that check says your
   computer requires another version.
3. Keep the installer defaults unless a foundation or current official
   instruction explains a different choice.
4. Finish the installation.
5. Close every PowerShell window, then open a new PowerShell window.
6. The `--version` option asks a program to print its installed version without
   changing anything. Run:

    ```powershell
    git --version
    ```

Expected result: a line beginning with `git version`. Record the full line in
`setup-version-check.txt`.

If PowerShell says `git` is not recognized, restart Windows once. If it still
fails, stop and ask Codex to diagnose the installation; do not reinstall
repeatedly.

### 3. Install Python

1. Open <https://www.python.org/downloads/windows/>.
2. Choose the current course-supported Windows installer from your live check.
3. Open the installer.
4. Enable **Add python.exe to PATH** if that option is shown.
5. Select **Install Now**.
6. Finish the installation.
7. Close PowerShell and open it again. The **Python Launcher for Windows**,
   typed as `py`, starts installed Python versions; `--list` asks it to show
   them. Run:

    ```powershell
    py --list
    ```

8. `--version` asks the selected Python installation to print its version.
   Then run:

    ```powershell
    py --version
    ```

Expected result: Python prints a supported version. Record both outputs in
`setup-version-check.txt`. Later commands use `py`; if your audited setup
requires an exact version such as `py -3.13`, use that exact version
consistently.

### 4. Install Node.js for n8n

1. Open <https://nodejs.org/en/download>.
2. Choose the supported **Long-Term Support (LTS)** release confirmed by the
   current [n8n installation documentation](https://docs.n8n.io/hosting/installation/npm/).
3. Open the Windows installer and keep the ordinary defaults.
4. Finish the installation.
5. Close PowerShell and open it again. **Node Package Manager (npm)** installs
   and runs reusable JavaScript components called **packages**. The following
   commands ask Node.js and npm to print their versions. Run:

    ```powershell
    node --version
    npm --version
    ```

Expected result: each command prints one version. Record both in
`setup-version-check.txt`.

## Now recreate it yourself — build the real learner project

You have rehearsed creating, locating, and inspecting a safe folder. Now create
the separate capstone project. Type or paste one command at a time and check the
stated result.

### 1. Create and enter the project folder

Open a new PowerShell window. In the commands below, `New-Item` creates
something; `-ItemType Directory` says that the new item is a folder; `-Path`
provides its location; and `-Force` prevents an error if that folder already
exists without erasing it. `Set-Location` enters the project folder, and
`Get-Location` prints the current folder. Run:

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Documents\AI-workflow-learning" -Force
New-Item -ItemType Directory -Path "$env:USERPROFILE\Documents\AI-workflow-learning\operations-exception-assistant" -Force
Set-Location "$env:USERPROFILE\Documents\AI-workflow-learning\operations-exception-assistant"
Get-Location
```

The final output must end with:

```text
Documents\AI-workflow-learning\operations-exception-assistant
```

Do not place this project in an **employer-synchronized folder**, meaning a
folder that is automatically copied into an employer cloud or server account.

### 2. Start Git and create a Python virtual environment

The commands below do four things:

1. `git init` makes the current folder a Git repository.
2. `py -m venv .venv` asks the Python Launcher (`py`) to run the `venv`
   module—`venv` is short for virtual environment—and create that isolated
   environment in a folder named `.venv`.
3. `Activate.ps1` runs a PowerShell script (`.ps1`) that makes this PowerShell
   window use the isolated environment.
4. `python --version` prints the version of the active Python.

Run:

```powershell
git init
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

Expected result: the prompt usually begins with `(.venv)` and Python prints the
audited version.

If activation is blocked, do not weaken PowerShell security globally. Use:

```powershell
.\.venv\Scripts\python.exe --version
```

Then ask Codex to explain the exact activation error.

### 3. Create the project folders

The next command creates eight folders. `data\input` holds fictional input;
`docs` is short for documents; `evidence` holds proof of completed work;
`output` holds generated results; `local_outbox` holds unsent drafts; `prompts`
holds AI instructions; `src` is short for source code; and `tests` holds
automated checks. Run:

```powershell
New-Item -ItemType Directory -Path "data\input","docs","evidence","output","local_outbox","prompts","src","tests" -Force
Get-ChildItem
```

Expected result: all eight named folders appear.

### 4. Create the ignore file

The `.gitignore` file contains rules telling Git which local or generated files
not to track. An **environment file**, named `.env`, stores local configuration
and may contain secrets; `.env.example` is a safe, empty template showing which
settings are expected. In the content below, `.venv/` ignores the virtual
environment; `.env` and `.env.*` ignore local setting files; `!.env.example`
makes the safe example file trackable; `__pycache__/` and `.pytest_cache/`
ignore temporary Python and pytest files; `output/` and `local_outbox/` ignore
generated results and drafts; and `*.log` ignores files whose names end in
`.log`.

1. Open Visual Studio Code.
2. Select **File → Open Folder**.
3. Open
   `Documents\AI-workflow-learning\operations-exception-assistant`.
4. In the Explorer panel, select **New File**.
5. Name the file `.gitignore`.
6. Paste and save:

    ```text
    .venv/
    .env
    .env.*
    !.env.example
    __pycache__/
    .pytest_cache/
    output/
    local_outbox/
    *.log
    ```

7. `git status` lists files that Git sees as changed or **untracked**, meaning
   not yet recorded by Git, without changing them. In PowerShell, while still
   inside the project folder, run:

    ```powershell
    git status
    ```

Expected result: `.venv` is not shown as thousands of untracked files.

### 5. Copy the course requirements and fictional data

`requirements-course.txt` is a plain-text list of the Python packages this
course needs. The **project root** is the top-level
`operations-exception-assistant` folder. `work_items.csv` is the fictional input
table, and `expected_issues.csv` is the answer key used by tests.

Use File Explorer. Do not edit the originals.

1. Locate this Course 1 source folder.
2. Copy `requirements-course.txt` into the project root.
3. Copy `practice_data\work_items.csv` to
   `data\input\work_items.csv`.
4. Copy `practice_data\expected_issues.csv` to
   `tests\expected_issues.csv`.
5. Open each destination folder and confirm the copied file exists.

If you cannot locate the Course 1 source folder, ask Codex:

```text
Please locate the AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE folder on my computer in
READ-ONLY mode. Do not change anything. Tell me the exact path and confirm
whether requirements-course.txt, practice_data\work_items.csv, and
practice_data\expected_issues.csv exist. Do not copy them for me.
```

### 6. Install the Course 1 Python packages

`pip` is Python's package installer. In these commands, `python -m` asks Python
to run a named **module**, a runnable unit of Python code; `--upgrade` requests
a newer available version; `-r` means “read the package list from this file”;
and `--version` only prints the installed pytest version. In the activated
environment, run one command at a time:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-course.txt
python -m pytest --version
```

Expected result: the last command prints a pytest version. Do not install
requirements from the archived future course.

### 7. Create configuration without a real secret

The `.env.example` file is the shareable configuration template introduced
above. In the content below:

- `EVALUATION_DATE` records when the setup was checked;
- `AI_MODE=offline` prevents use of an external AI service;
- `AI_MODEL` is a placeholder for a future AI system and version choice;
- `OPENAI_API_KEY` is the empty placeholder for an **application programming
  interface key (API key)**, a secret value that could authorize access to an
  OpenAI service; **OpenAI** is the company that provides that service; and
- `KILL_SWITCH` is an emergency setting intended to disable the optional AI
  step.

In Visual Studio Code, create `.env.example` in the project root:

```text
EVALUATION_DATE=2026-07-26
AI_MODE=offline
AI_MODEL=replace-after-live-audit
OPENAI_API_KEY=
KILL_SWITCH=false
```

Keep `OPENAI_API_KEY=` empty.

Copy `.env.example` to a new file named `.env`. Do not add a real key. The
`--short` option asks `git status` for a compact result. Run:

```powershell
git status --short
```

Expected result: `.env.example` may appear, but `.env` must not appear because
Git ignores it.

### 8. Create and run the smoke tests

A **smoke test** is a quick basic check that the setup can perform its most
important minimum actions. In the Python code below:

- `from pathlib import Path` makes Python's built-in path tool available;
- `def` defines a function, and names beginning with `test_` tell pytest which
  functions to run;
- `Path` represents a file or folder path, `.is_file()` checks that a file
  exists, and `.resolve()` produces its full path;
- `assert` requires a condition to be true, `!=` means “is not equal to,” and
  `None` means that the test function returns no value.

In Visual Studio Code, create `tests\test_smoke.py`:

```python
from pathlib import Path


def test_synthetic_input_exists() -> None:
    assert Path("data/input/work_items.csv").is_file()


def test_output_is_not_source() -> None:
    assert Path("output").resolve() != Path("data/input").resolve()
```

The `-q` option means quiet output: pytest prints a short result instead of
extra detail. In PowerShell, run:

```powershell
python -m pytest -q
```

Expected result:

```text
2 passed
```

If the result says `failed` or `error`, stop. Copy the complete error into your
private course notes and ask Codex to explain it. Do not ask Codex to hide or
skip the test.

### 9. Start and stop the local n8n learning instance

`N8N_USER_FOLDER` is an environment-variable name that tells n8n where to keep
this course's local configuration. **npx** is the command name for the package
runner supplied with npm; it is not an abbreviation you need to expand. After
n8n starts, `Ctrl+C`—hold the Control key and tap C—stops the running command.
Run:

```powershell
$env:N8N_USER_FOLDER = "$env:USERPROFILE\Documents\AI-workflow-learning\.n8n-course"
npx n8n
```

Open only the **local address** printed by n8n, meaning the web address served
on this computer. Do not create or connect an employer account. Press `Ctrl+C`
in PowerShell to stop n8n.

Record whether start and stop both worked in
`evidence\setup-check.txt`. Before later sessions, set the same
`N8N_USER_FOLDER` again.

## Ask Codex to check your work

Replace the placeholder with the full project path from `Get-Location`, then
send:

```text
Please inspect this Course 1 setup folder in READ-ONLY mode:
[PASTE THE FULL operations-exception-assistant PATH HERE]

Do not create, edit, rename, move, delete, install, or download anything. Do
not reveal or print secret values. Check only this folder. Verify the eight
required subfolders, .gitignore rules, requirements-course.txt,
data/input/work_items.csv, tests/expected_issues.csv, .env.example with an
empty OPENAI_API_KEY, tests/test_smoke.py, and evidence/setup-check.txt.
Confirm that .env and .venv are not tracked by Git without opening or printing
.env. Report PASS or NOT YET against the setup pass criteria. If it is NOT
YET, explain the exact smallest correction and let me perform it.
```

Codex cannot prove from files alone that an installer was trustworthy or that
n8n stopped correctly. Your recorded command outputs remain part of the
evidence.

## Pass criteria

- [ ] `Get-Location` shows the exact capstone folder.
- [ ] Git, Python, Node.js, npm, pytest, and n8n versions were recorded.
- [ ] The eight required project folders exist.
- [ ] `.venv` and `.env` are ignored by Git.
- [ ] The copied CSV files remain fictional course data.
- [ ] `OPENAI_API_KEY=` remains empty.
- [ ] The smoke test result is `2 passed`.
- [ ] n8n starts locally and stops with `Ctrl+C`.
- [ ] No real data, **credential** (username, password, or access token), or
      employer/client connection was introduced.
- [ ] Codex reports `PASS` after read-only inspection.

## Clean removal

The environment is intentionally local. Do not practise deletion commands.
When removal is genuinely needed, first confirm the exact **resolved targets**,
meaning the full unambiguous folder paths, are inside
`Documents\AI-workflow-learning`, then remove only the capstone and
`.n8n-course` folders through File Explorer. Never select your whole Documents
folder.
