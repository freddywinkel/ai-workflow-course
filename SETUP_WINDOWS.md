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
- **Python Install Manager:** the current official Windows tool for installing
  and selecting Python runtimes;
- **runtime:** the installed Python program that actually runs Python code;
- **virtual environment:** an isolated folder containing the Python
  **packages**, reusable units of code, for one project;
- **stable release:** a finished software version intended for normal use;
- **prerelease:** an unfinished alpha, beta, or release-candidate version used
  for testing; Course 1 does not use one;
- **Node.js:** optional software that runs JavaScript, a programming language
  used by websites and some automation tools, outside a web browser; it is not
  required for Course 1;
- **n8n** (pronounced “n-eight-n”): an optional workflow-automation
  application; the name is not an abbreviation you need to expand;
- **comma-separated values (CSV):** a plain-text table format;
- **application programming interface (API):** a defined way for software
  systems to exchange requests and responses;
- **pytest:** the Python testing tool used in this course;
- **secret:** a password-like value, such as an access key, that must not be
  shared or stored in tracked course files;
- **Codex:** the course workspace assistant you are using now. A **read-only**
  Codex check may inspect and explain named files but may not change them.
- **application execution alias:** a Windows shortcut that may open the
  Microsoft Store even when a real Python runtime is not installed.

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
4. The first command asks Windows for your real Documents location. This is
   safer than assuming it is always directly under your user folder; Windows
   may redirect Documents. The answer is stored temporarily as
   `$documentsPath`. The second command uses `Set-Location` to change the
   folder affected by later commands. Copy both lines, paste them into
   PowerShell, and press `Enter`:

    ```powershell
    $documentsPath = [Environment]::GetFolderPath("MyDocuments")
    Set-Location -LiteralPath (Join-Path $documentsPath "controlled-ai-course-practice\setup-follow-along")
    ```

5. `Get-Location` prints the current folder without changing it. Run:

    ```powershell
    Get-Location
    ```

   Expected result: the printed path ends with
   `controlled-ai-course-practice\setup-follow-along`. The part before that may
   differ if Windows redirects Documents.

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

## Computer preflight — check before installing

This preflight checks this computer, not an imaginary perfect computer. It
does not install software or change a security setting. It briefly creates one
uniquely named empty test file inside the harmless practice folder, confirms
that it exists, and deletes that exact test file again. It does not touch an
existing learner project.

You need:

- at least 2 gigabytes (GB) free on the drive containing Documents;
- write access to your own practice folder;
- an internet connection for the official Python download and one-time package
  installation;
- a working browser;
- the complete Course 1 source folder;
- Visual Studio Code, Git, Python Install Manager, and a stable Python 3.14
  runtime by the end of setup.

No cloud account, GitHub account, paid subscription, application programming
interface (API) key, Node.js installation, n8n installation, or employer
system access is needed.

### A. Check Documents, free space, write access, and the course folder

1. Open the Course 1 source folder in File Explorer.
2. Select the address bar and copy the complete folder path. It must end with
   `AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE`.
3. Open a new PowerShell window.
4. Copy and run this block. When PowerShell asks for the path, paste it and
   press `Enter`.

Before you run it, these four square-bracket names need an explanation.
Square brackets tell PowerShell to use a built-in Windows or PowerShell helper;
they are not folder names and you do not have to install them.

- `[IO.Path]` uses the built-in **input/output (IO) path helper**.
  `GetPathRoot` reads the drive part of the Documents path, such as `C:\`. It
  does not change the path or the drive.
- `[IO.DriveInfo]` uses the built-in **drive-information helper**.
  `::new($driveRoot)` creates a temporary description of that drive in memory,
  and `AvailableFreeSpace` reads its free-space value. It does not reserve,
  remove, or write disk space.
- `[guid]` uses the built-in **globally unique identifier (GUID) helper**.
  `NewGuid()` creates a random-looking identifier for the temporary probe-file
  name. This makes it extremely unlikely that the check could choose the name
  of an existing file.
- `[pscustomobject]` means **PowerShell custom object**. It groups the named
  check results into one table-like result on screen. It does not create a
  file or send the results anywhere.

The block also uses `[math]::Round` to round a number for easier reading and
`1GB` as PowerShell's built-in value for one gigabyte. The only disk change is
the clearly named synthetic probe file described above; the `finally` section
removes that exact probe even when the write check reports an error.

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$courseSourcePath = Read-Host "Paste the full Course 1 source-folder path"
$requiredCourseFiles = @(
    "SETUP_WINDOWS.md",
    "requirements-course.txt",
    "practice_data\work_items.csv",
    "practice_data\expected_issues.csv"
)
$missingCourseFiles = @(
    $requiredCourseFiles | Where-Object {
        -not (Test-Path -LiteralPath (Join-Path $courseSourcePath $_) -PathType Leaf)
    }
)
$driveRoot = [IO.Path]::GetPathRoot($documentsPath)
$freeSpaceGB = [math]::Round(([IO.DriveInfo]::new($driveRoot).AvailableFreeSpace / 1GB), 1)
$probeFolder = Join-Path $documentsPath "controlled-ai-course-practice\preflight"
New-Item -ItemType Directory -Path $probeFolder -Force | Out-Null
$probePath = Join-Path $probeFolder ("write-check-" + [guid]::NewGuid().ToString() + ".tmp")
try {
    Set-Content -LiteralPath $probePath -Value "synthetic Course 1 write check"
    $writeCheck = Test-Path -LiteralPath $probePath -PathType Leaf
}
finally {
    if (Test-Path -LiteralPath $probePath -PathType Leaf) {
        Remove-Item -LiteralPath $probePath
    }
}
[pscustomobject]@{
    DocumentsPath = $documentsPath
    FreeSpaceGB = $freeSpaceGB
    AtLeast2GBFree = ($freeSpaceGB -ge 2)
    PracticeFolderWritable = $writeCheck
    CourseFolderFound = (Test-Path -LiteralPath $courseSourcePath -PathType Container)
    MissingCourseFiles = if ($missingCourseFiles.Count -eq 0) { "NONE" } else { $missingCourseFiles -join ", " }
    EffectivePowerShellPolicy = Get-ExecutionPolicy
}
```

Expected result:

- `AtLeast2GBFree` is `True`;
- `PracticeFolderWritable` is `True`;
- `CourseFolderFound` is `True`;
- `MissingCourseFiles` is `NONE`.

`EffectivePowerShellPolicy` may be `Restricted`. That is acceptable. Do not
change it: every required Course 1 Python command calls the virtual
environment's `python.exe` file directly, so activation is unnecessary.

If a value is different, stop and give Codex the displayed table. Do not give
Codex a username, password, key, or unrelated folder contents.

### B. Check internet and browser access

The next command requests the official Python Windows documentation and keeps
the result only in memory. It does not save the page.

```powershell
try {
    Invoke-WebRequest -Uri "https://docs.python.org/3/using/windows.html" -UseBasicParsing -TimeoutSec 20 | Out-Null
    "InternetCheck: PASS"
}
catch {
    "InternetCheck: NOT YET - " + $_.Exception.Message
}
```

Expected result: `InternetCheck: PASS`.

Then run:

```powershell
Start-Process "https://docs.python.org/3/using/windows.html"
```

Expected result: your normal browser opens the official page titled
**Using Python on Windows**. If the command reports `PASS` but no browser
opens, open the same address yourself in Microsoft Edge or Google Chrome.

### C. Check what Windows command names actually point to

This block only reports commands. It does not run Python and therefore cannot
trigger a Store installation.

```powershell
foreach ($commandName in "git","code","python","py","pymanager") {
    $foundCommand = Get-Command $commandName -ErrorAction SilentlyContinue
    if ($null -eq $foundCommand) {
        "$commandName : NOT FOUND"
    }
    else {
        "$commandName : $($foundCommand.Source)"
    }
}
```

On the computer audited on 2026-07-28, Visual Studio Code and Git were already
working, `python` pointed only to
`Microsoft\WindowsApps\python.exe`, and `py` and `pymanager` were not found.
That `python` result is a Store alias, not a working runtime. This is a normal
starting point. Continue with the manual Python steps below.

## Install the required tools once

The interfaces and supported versions can change. First use the learner-safe,
read-only software report in
[BEGINNER_SOFTWARE_CHECK.md](BEGINNER_SOFTWARE_CHECK.md). That report checks
official pages and tells you what is current. It never authorizes an assistant
to edit files, install software, or rewrite this course. The separate evergreen
audit is for course maintainers, not a learner setup step.

Record the checked date and answers in a Notepad file named
`setup-version-check.txt` inside `setup-follow-along`.

### 1. Install Visual Studio Code

1. In a new PowerShell window, run:

    ```powershell
    code --version
    ```

2. If this prints a version, Visual Studio Code is already installed. On the
   computer audited on 2026-07-28 it printed `1.130.0`; open the application
   and continue at step 8. Do not reinstall it simply because a download page
   offers a newer version.
3. Only if the command is not found, open
   <https://code.visualstudio.com/download>.
4. A Windows **User Installer** installs the application for your Windows
   account rather than for every account on the computer. Choose the User
   Installer for your computer.
5. Open the downloaded installer. Read each screen and keep the default
   installation folder.
6. **PATH** is the list of folders Windows searches when you type a command. If
   offered, enable **Add to PATH** and **Add “Open with Code” action**.
7. Finish the installation and open Visual Studio Code.
8. Select **File → Open Folder** and open
   `Documents\controlled-ai-course-practice\setup-follow-along`.
9. Confirm `setup-check.txt` is visible in the Explorer panel on the left.

### 2. Install Git for Windows

1. In PowerShell, run:

    ```powershell
    git --version
    ```

2. If this prints a line beginning with `git version`, Git is already
   installed. On the computer audited on 2026-07-28 it printed
   `git version 2.54.0.windows.1`; record that full line and skip to the Python
   section. A working current-supported Git does not need to be reinstalled
   for this course.
3. Only if the command is not found, open
   <https://git-scm.com/download/win>.
4. **64-bit** describes the standard processor and Windows type on most modern
   computers; your live version check should confirm the correct installer.
   Download and open the official 64-bit installer unless that check says your
   computer requires another version.
5. Keep the installer defaults unless a foundation or current official
   instruction explains a different choice.
6. Finish the installation.
7. Close every PowerShell window, then open a new PowerShell window.
8. The `--version` option asks a program to print its installed version without
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

The official Python guidance for Windows now uses **Python Install Manager**.
The manager and the Python runtime are two separate things: first install the
manager, then tell it which stable Python runtime to install. Do these actions
yourself; Codex must not activate a paid service, change system settings, or
perform the installation for you.

1. Open the official Windows guidance:
   <https://docs.python.org/3/using/windows.html>.
2. Follow its **Python install manager → Installation** link. The dated
   2026-07-28 audit found stable Python Install Manager 26.3 at
   <https://www.python.org/downloads/release/pymanager-263/>. On that page,
   under **Files → Windows**, choose **Installer (MSIX)**, Microsoft's modern
   Windows app-package format. Do not choose the legacy **Microsoft Installer
   (MSI) package**, the older Windows Installer format, or a manager version
   containing `beta`. If your new software check identifies a later stable
   manager, use the current stable MSIX linked by the official Windows guidance
   instead of this dated release page. The Microsoft Store version is also
   official and identical, but use only one source; do not install both
   variants.
3. Open the downloaded installer and select **Install**. This is a per-user
   manager; you do not need to make a machine-wide installation.
4. Close every PowerShell window and open a new one.
5. `Get-Command` reports where a command comes from. Run:

    ```powershell
    Get-Command pymanager
    ```

   Expected result: PowerShell displays an application named `pymanager.exe`.
   If it says the term is not recognized, stop and use the official
   troubleshooting section linked above. Do not repeatedly reinstall it.

6. Ask the manager to show the best available stable 3.14 runtime:

    ```powershell
    pymanager list --online --one 3.14
    ```

   `--online` checks the official runtime list and `--one` shows the best
   match. The Course 1 target is stable Python 3.14. Do not select a version
   containing `a`, `b`, or `rc`; those letters indicate an alpha, beta, or
   release candidate prerelease. If no stable 3.14 result appears, stop and ask
   for a dated course compatibility audit instead of choosing a different
   version yourself.

7. Install the current stable 3.14 patch:

    ```powershell
    pymanager install 3.14
    ```

   Wait until the command completes. This is the one required Python runtime
   download. The current manager installer may already bundle the matching
   runtime; if the manager reports that stable 3.14 is already installed,
   continue to verification instead of reinstalling it.

8. Confirm the managed runtime and its exact version:

    ```powershell
    pymanager list --only-managed 3.14
    pymanager exec -V:3.14 --version
    ```

Expected result: the second command prints `Python 3.14` followed by a patch
number, with no `a`, `b`, or `rc`. On 2026-07-28 the clean-room audit used
Python 3.14.6. A later stable 3.14 patch is acceptable after the dated software
check confirms it. Record both command outputs in `setup-version-check.txt`.

Do not use the bare `python` command during this course. Before setup it can be
a Store alias, and after setup it can change when other runtimes are installed.
The project will call its own exact `.venv\Scripts\python.exe` instead.

### Optional later — visual workflow-tool crosswalk

Do not install Node.js or n8n for the required Course 1 path. The capstone uses
local Python, files, and an offline artificial-intelligence fixture. This keeps
the foundation reproducible and prevents a fast-changing vendor interface from
becoming a learning blocker.

After the complete offline capstone passes, you may compare its trigger,
validation, rule, human-review, fallback, and evidence steps with a visual
workflow tool. Before that optional comparison, obtain a new dated software
report, confirm the tool's official compatibility page, and record and pin the
exact versions selected. A **Long-Term Support (LTS)** release receives planned
maintenance for longer than a short-lived release; use it only when the
selected tool's current official compatibility page supports it. Do not run an
unversioned package command.

## Now recreate it yourself — build the real learner project

You have rehearsed creating, locating, and inspecting a safe folder. Now create
the separate capstone project. Type or paste one command at a time and check the
stated result.

### 1. Create and enter the project folder

Open a new PowerShell window. In the commands below, `New-Item` creates
something; `-ItemType Directory` says that the new item is a folder; `-Path`
provides its location; and `-Force` prevents an error if the folder already
exists without erasing its contents. `Join-Path` safely combines folder names.
`Set-Location` enters the project folder, and `Get-Location` prints the current
folder. Run:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$learningRoot = Join-Path $documentsPath "AI-workflow-learning"
$projectRoot = Join-Path $learningRoot "operations-exception-assistant"
New-Item -ItemType Directory -Path $learningRoot -Force | Out-Null
New-Item -ItemType Directory -Path $projectRoot -Force | Out-Null
Set-Location -LiteralPath $projectRoot
Get-Location
```

The final output must end with:

```text
AI-workflow-learning\operations-exception-assistant
```

Do not place this project in an **employer-synchronized folder**, meaning a
folder that is automatically copied into an employer cloud or server account.

### 2. Start Git and create a Python virtual environment

The commands below do five things:

1. `git init` makes the current folder a Git repository.
2. The two `git config --local` commands give this practice repository a
   clearly fictional author name and email address. `--local` means the
   settings apply only inside this repository.
3. `$pythonExe` stores the exact future virtual-environment Python path.
4. `pymanager exec -V:3.14 -m venv .venv` asks the manager to use stable
   Python 3.14 and run `venv`—short for virtual environment—to create the
   isolated `.venv` folder. The `if` condition prevents overwriting an
   environment that already exists.
5. The direct `.venv\Scripts\python.exe` command prints the selected Python
   version. It works even when PowerShell scripts are restricted.

Run:

```powershell
git init
git config --local user.name "Course Learner"
git config --local user.email "course-learner@example.invalid"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $pythonExe -PathType Leaf) {
    "Existing virtual environment found; creation skipped."
}
else {
    pymanager exec -V:3.14 -m venv .venv
}
& $pythonExe --version
git status --short
```

Expected result: Python prints stable `Python 3.14` followed by a patch number.
The PowerShell prompt does **not** need to begin with `(.venv)`.

If `& $pythonExe --version` fails, stop. Run these read-only checks and give
the complete output to Codex:

```powershell
Get-Location
Test-Path -LiteralPath $pythonExe -PathType Leaf
pymanager list --only-managed 3.14
Get-ExecutionPolicy
```

Do not try to activate the virtual environment, change the execution policy,
delete `.venv`, or create another environment until the cause is understood.

### Start or resume every later setup session

PowerShell forgets variables when you close its window. This is normal. At the
start of every new setup or Course 1 study session, open a new PowerShell
window and run this same block:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$projectRoot = Join-Path $documentsPath "AI-workflow-learning\operations-exception-assistant"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
Set-Location -LiteralPath $projectRoot
Get-Location
& $pythonExe --version
git status --short
```

Expected result: the location ends in
`AI-workflow-learning\operations-exception-assistant`, Python prints a stable
3.14 version, and Git prints either a short change list or no lines at all.
No lines from `git status --short` means there are no unrecorded changes.

If `Set-Location` or the Python command fails, do not recreate or overwrite
anything. Use File Explorer to confirm the exact project path, then ask Codex
to diagnose the mismatch in read-only mode.

### Safe troubleshooting table

Use this table before trying another command:

| What you observe | What it usually means | Safe next action |
|---|---|---|
| Typing bare `python` opens the Microsoft Store | Windows used an application execution alias | Close the Store. Use `pymanager` only to create `.venv`, then use `& $pythonExe` |
| `pymanager` is not recognized after installation | The old PowerShell window has not refreshed its commands, or manager registration needs repair | Close PowerShell, open a new window, and retry `Get-Command pymanager`; then use the official troubleshooting page |
| PowerShell says running scripts is disabled | The execution policy is restrictive | Do not activate the environment and do not change policy; use `& $pythonExe` |
| `Set-Location` cannot find the path | Windows uses a different Documents location or the folder name differs | Run `[Environment]::GetFolderPath("MyDocuments")`, inspect the folder in File Explorer, and correct only the path |
| `$pythonExe` is not recognized as a command | The variable was lost when PowerShell closed | Run the complete **Start or resume** block again |
| `Test-Path -LiteralPath $pythonExe` prints `False` | The virtual environment is missing or the project path is wrong | Stop and ask Codex to inspect the two exact paths in read-only mode; do not delete or recreate `.venv` |
| Package installation reports a certificate, proxy, or connection error | The network could not safely reach the package source | Record the full error and ask for diagnosis; do not disable certificate checking |
| A command reports `Access denied` | The selected folder or computer policy does not allow that action | Stop. Do not run PowerShell as administrator; confirm you are using your own practice folder |
| Git shows an unfamiliar file | A file changed outside the step you expected | Do not add or commit it until you inspect and understand it |

When asking Codex for help, include the command you ran, the complete error,
`Get-Location`, and the result of
`Test-Path -LiteralPath $pythonExe -PathType Leaf`. Do not include `.env`
contents, usernames, keys, employer paths, or real data.

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
3. Open the exact `operations-exception-assistant` path printed by
   `Get-Location` in step 1. Do not guess where Windows stores Documents.
4. Look for `.gitignore` in the Explorer panel. If it already exists, do not
   replace it. Open it, compare it with the nine lines below, and ask Codex for
   the smallest correction if a line is missing. Then continue at step 7.
5. If it does not exist, select **New File**.
6. Name the file `.gitignore`, paste the following content, and save:

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

`requirements-course.txt` is a plain-text list of the exactly pinned Python
packages this offline course needs. A **version pin** selects one exact package
version instead of accepting whatever happens to be newest. The **project
root** is the top-level
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

If any destination file already exists, select **Cancel** when Windows asks
whether to replace it. Do not overwrite learner work during a resumed setup.
Ask Codex to compare the source and destination files in read-only mode and
explain whether the existing file is already correct.

If you cannot locate the Course 1 source folder, ask Codex:

```text
Please locate the AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE folder on my computer in
READ-ONLY mode. Do not change anything. Tell me the exact path and confirm
whether requirements-course.txt, practice_data\work_items.csv, and
practice_data\expected_issues.csv exist. Do not copy them for me.
```

### 6. Install the Course 1 Python packages

`pip` is Python's package installer. In these commands, `& $pythonExe` runs the
exact Python file stored in the variable; `-m` asks Python to run a named
**module**, a runnable unit of Python code; `-r` means “read the package list
from this file”; and `--version` only prints a version. The requirements file
pins the complete dependency tree, so setup does not silently choose newer
packages.

First run the **Start or resume** block above if this is a new PowerShell
window. Then run one command at a time:

```powershell
& $pythonExe -m pip --version
& $pythonExe -m pip install -r requirements-course.txt
& $pythonExe -m pytest --version
& $pythonExe -c "import importlib.metadata; print('jsonschema', importlib.metadata.version('jsonschema'))"
```

Expected result: pip prints its path inside `.venv`, pytest prints `9.0.2`, and
jsonschema prints `4.26.0`. Do not run an unpinned pip upgrade. Do not install
requirements from the archived future course. OpenAI provider software is not
in the required file; the bounded artificial-intelligence lesson uses an
offline saved response.

If the install says it cannot reach the package index, rerun the internet
preflight once. If it says there is no matching package, record the complete
message and stop; do not remove a version pin or choose a random substitute.

### 7. Create configuration without a real secret

The `.env.example` file is the shareable configuration template introduced
above. In the content below:

- `EVALUATION_DATE` records when the setup was checked;
- `AI_MODE=offline` prevents use of an external AI service;
- `EXTERNAL_ACTIONS_ENABLED=false` is an explicit safety setting: the workflow
  is not allowed to send, order, pay, approve, or write to another system.

In Visual Studio Code, create `.env.example` in the project root:

```text
EVALUATION_DATE=2026-07-26
AI_MODE=offline
EXTERNAL_ACTIONS_ENABLED=false
```

`2026-07-26` is the frozen Course 1 evaluation date used by the supplied rules
and expected results. It is configuration, not today's date. Do not replace it
with the date on which you happen to study.

If `.env.example` already exists, do not replace it. Confirm that it has a real
fixed date and the two safe values shown above, then continue.

Copy `.env.example` to a new file named `.env`. Do not add a real key or any
provider setting. If `.env` already exists, do not replace or open it; continue
with the existing ignored file. The
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

If `tests\test_smoke.py` already exists, do not replace it. Ask Codex to compare
it with this example in read-only mode and let you make any needed correction.

The `-q` option means quiet output: pytest prints a short result instead of
extra detail. First run the **Start or resume** block if needed, then run:

```powershell
& $pythonExe -m pytest -q
```

Expected result:

```text
2 passed
```

If the result says `failed` or `error`, stop. Copy the complete error into your
private course notes and ask Codex to explain it. Do not ask Codex to hide or
skip the test.

### 9. Freeze and record the setup in Git

`pip list --format=freeze` prints the exact installed Python package tree,
including pip. `Set-Content` writes that output to the named evidence file. The
Git commands then record only the safe setup files and fictional course data.
They do not upload anything.

First create `evidence\setup-check.txt` in Notepad. Record the date, the exact
Git, Python, pytest, and jsonschema version output, `2 passed`, and the
sentence `External actions remain disabled.` Do not record a username,
computer name, folder path, key, or other secret. If the file already exists,
open and continue it without deleting earlier evidence.

Then run:

```powershell
$dependencyEvidencePath = ".\evidence\setup-dependencies.txt"
if (Test-Path -LiteralPath $dependencyEvidencePath -PathType Leaf) {
    "Existing dependency evidence found; it was not overwritten."
}
else {
    & $pythonExe -m pip list --format=freeze | Set-Content -LiteralPath $dependencyEvidencePath
}
Get-Content .\evidence\setup-dependencies.txt
git status --short
git add -- ".gitignore" ".env.example" "requirements-course.txt" "data/input/work_items.csv" "tests/expected_issues.csv" "tests/test_smoke.py" "evidence/setup-check.txt" "evidence/setup-dependencies.txt"
git commit -m "initialize Course 1 project"
git status --short
```

Expected result: the dependency file includes the exact pytest and jsonschema
versions, Git creates one commit, and the final status does not list any of
those setup files. A **commit** is a recorded local snapshot. No remote service
or GitHub account is needed.

If Git reports `nothing to commit`, run `git status --short`. Continue only
when the named setup files were already recorded in an earlier commit. If Git
names a file you do not recognise, stop and inspect it before adding anything.

## Ask Codex to check your work

Replace the placeholder with the full project path from `Get-Location`, then
send:

```text
Please inspect this Course 1 setup folder in READ-ONLY mode:
[PASTE THE FULL operations-exception-assistant PATH HERE]

Do not create, edit, rename, move, delete, install, or download anything. Do
not reveal or print secret values. Inspect only this folder, plus run
non-mutating Git, Python-version, and PowerShell-policy checks for this setup.
Verify the eight required subfolders, .gitignore rules,
requirements-course.txt with exact version pins,
data/input/work_items.csv, tests/expected_issues.csv, .env.example with
EVALUATION_DATE=2026-07-26, AI_MODE=offline, and
EXTERNAL_ACTIONS_ENABLED=false, tests/test_smoke.py, evidence/setup-check.txt,
and evidence/setup-dependencies.txt containing pytest 9.0.2 and jsonschema
4.26.0.
Confirm that .env and .venv are not tracked by Git without opening or printing
.env. Confirm that .venv\Scripts\python.exe exists and reports a stable Python
3.14 patch, and report the effective PowerShell policy without changing it.
Do not rerun tests because that could create cache files; inspect the recorded
2-passed evidence instead. Report PASS or NOT YET against the setup pass
criteria. If it is NOT YET, explain the exact smallest correction and let me
perform it.
```

Codex cannot prove from files alone that an installer was trustworthy. Your
recorded command outputs remain part of the evidence.

## Pass criteria

- [ ] The preflight reports at least 2 GB free, a writable practice folder, a
      working internet check and browser, and no missing required course file.
- [ ] `Get-Location` shows the exact capstone folder.
- [ ] Python Install Manager and a stable, non-prerelease Python 3.14 runtime
      were installed manually.
- [ ] The effective PowerShell policy was not weakened and activation was not
      required.
- [ ] Git, Python, pytest, and jsonschema versions were recorded.
- [ ] Every Python command used the project's exact
      `.venv\Scripts\python.exe`.
- [ ] The eight required project folders exist.
- [ ] `.venv` and `.env` are ignored by Git.
- [ ] The copied CSV files remain fictional course data.
- [ ] `AI_MODE=offline` and `EXTERNAL_ACTIONS_ENABLED=false` are recorded.
- [ ] The smoke test result is `2 passed`.
- [ ] `evidence\setup-dependencies.txt` records the exact installed package
      tree.
- [ ] The safe setup files and fictional inputs are recorded in the first
      local Git commit.
- [ ] No real data, **credential** (username, password, or access token), or
      employer/client connection was introduced.
- [ ] Codex reports `PASS` after read-only inspection.

## Clean removal

The preflight cleaned up only the uniquely named test file it had just
created. Do not practise any other deletion command. When removal is genuinely
needed, first confirm the exact **resolved targets**, meaning the full
unambiguous folder paths, are inside the real Documents location's
`AI-workflow-learning` folder, then remove only the capstone folder through
File Explorer. Never select your whole Documents folder.
