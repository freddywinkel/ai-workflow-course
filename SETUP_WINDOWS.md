# Windows Setup — Course 1

## Goal

Create a local synthetic-data learning environment that you can inspect,
remove, and rebuild. Do not connect employer or client systems.

## Before installing

Run [EVERGREEN_UPDATE_PROMPT.md](EVERGREEN_UPDATE_PROMPT.md). It must confirm:

- the selected Python release is supported by the course dependencies;
- the selected Node.js release is supported by the current stable n8n release;
- official installation URLs still apply;
- optional model/API examples still use supported interfaces.

Record the results in `evidence/setup_audit.md` in your capstone repository.

## 1. Create separate folders

In PowerShell:

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Documents\AI-workflow-learning" -Force
Set-Location "$env:USERPROFILE\Documents\AI-workflow-learning"
New-Item -ItemType Directory -Path "operations-exception-assistant" -Force
```

Do not place the capstone inside an employer-synchronized folder.

## 2. Install an editor

Install Visual Studio Code from:

<https://code.visualstudio.com/download>

Open the capstone folder. Confirm the Explorer shows the exact folder you
created.

## 3. Install Git

Install Git for Windows from:

<https://git-scm.com/download/win>

Close and reopen PowerShell, then run:

```powershell
git --version
```

Record the observed version. A printed version proves Git starts; it does not
prove the rest of the setup.

## 4. Install Python

Use the official Windows installer:

<https://www.python.org/downloads/windows/>

The examples target Python 3.13, but any live-audited Python 3.12+ version that
passes the dependency tests is acceptable.

Run:

```powershell
py --list
py -3.13 --version
```

If `py -3.13` is unavailable, use the exact installed version in every later
command and document the choice.

## 5. Create the project and virtual environment

```powershell
Set-Location "$env:USERPROFILE\Documents\AI-workflow-learning\operations-exception-assistant"
git init
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

If PowerShell blocks activation, read the error and use the narrowest
appropriate solution. Do not globally weaken execution policy without
understanding the consequence. You can always call the environment directly:

```powershell
.\.venv\Scripts\python.exe --version
```

## 6. Create a safe `.gitignore`

Create `.gitignore` in the capstone repository:

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

Run:

```powershell
git status
```

Verify that `.venv` is not listed as thousands of untracked files.

## 7. Install the Course 1 Python dependencies

Copy `requirements-course.txt` from this course package into the capstone
repository, then:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-course.txt
python -m pytest --version
```

Do not install the archived supplier-course requirements.

## 8. Install Node.js for n8n

Use the official Node.js download page:

<https://nodejs.org/en/download>

Choose a supported LTS version confirmed by the current n8n documentation:

<https://docs.n8n.io/hosting/installation/npm/>

Close and reopen PowerShell:

```powershell
node --version
npm --version
```

## 9. Start a local n8n learning instance

Use a dedicated local data folder:

```powershell
$env:N8N_USER_FOLDER = "$env:USERPROFILE\Documents\AI-workflow-learning\.n8n-course"
npx n8n
```

Open only the local address printed by n8n. Stop it with `Ctrl+C`.

Before later study sessions, set the same `N8N_USER_FOLDER` again. Do not reuse
an employer n8n account or tenant.

## 10. Copy only the synthetic practice data

Create:

```text
operations-exception-assistant/
  data/
    input/
  docs/
  evidence/
  output/
  local_outbox/
  prompts/
  src/
  tests/
```

Copy:

- `practice_data/work_items.csv` to `data/input/work_items.csv`;
- `practice_data/expected_issues.csv` to `tests/expected_issues.csv`.

Do not edit the originals in the course package.

## 11. Create configuration without secrets

`.env.example`:

```text
EVALUATION_DATE=2026-07-26
AI_MODE=offline
AI_MODEL=replace-after-live-audit
OPENAI_API_KEY=
KILL_SWITCH=false
```

Copy it to `.env`, which must remain ignored.

The course passes with `AI_MODE=offline`. Do not create an API key yet.

## 12. Run smoke tests

Create `tests/test_smoke.py`:

```python
from pathlib import Path


def test_synthetic_input_exists() -> None:
    assert Path("data/input/work_items.csv").is_file()


def test_output_is_not_source() -> None:
    assert Path("output").resolve() != Path("data/input").resolve()
```

Run:

```powershell
python -m pytest -q
git status
```

## Setup gate

Continue only when:

- [ ] I know the absolute capstone folder.
- [ ] Git status is understandable.
- [ ] `.venv` and `.env` are ignored.
- [ ] Python and pytest start inside the virtual environment.
- [ ] n8n starts locally and stops cleanly.
- [ ] the supplied synthetic CSV exists in the copied input folder.
- [ ] the smoke tests pass.
- [ ] no real data or credential has been introduced.
- [ ] I recorded observed versions and the live-audit date.

## Clean removal

The learning environment is intentionally local. To remove it, first confirm
the exact resolved paths are inside
`Documents\AI-workflow-learning`. Then remove the capstone and dedicated
`.n8n-course` folders using Windows Explorer or a carefully scoped PowerShell
command. Never target your Documents folder broadly.
