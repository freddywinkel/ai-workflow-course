# Windows Setup and Reproduction Guide

## Beginner: how to use this guide

If you have never used PowerShell, complete
[`foundations/02_COMMAND_LINE_SURVIVAL.md`](foundations/02_COMMAND_LINE_SURVIVAL.md)
before running anything on this page. The command blocks below are instructions
for your computer, not prose to paste into an AI chat.

For each block:

1. Open PowerShell from the Windows Start menu.
2. Run one line at a time unless the text explicitly says otherwise.
3. Do not copy the prompt (`PS C:\...>`), the backticks, the language label, or
   example output.
4. Run `Get-Location` first and verify the folder.
5. Read all output before moving on.
6. If the result differs, stop and use
   [`templates/debugging_record.md`](templates/debugging_record.md). Do not keep
   pasting later commands over an unresolved failure.

Installation changes the computer and may require a restart. This guide never
requires weakening PowerShell's machine-wide execution policy. Do not run an
administrator terminal unless the documented installer explicitly requests it.

Verified against the course authoring machine on 2026-07-25:

- Windows with PowerShell;
- Git and `winget` available;
- WSL available;
- Docker not found on `PATH`;
- Node not found on `PATH`;
- `python` resolves to a non-working Windows Store alias rather than a usable runtime.

Do not assume your state is identical. Capture the output of the preflight commands.

## 1. Preflight

Open a fresh PowerShell window:

```powershell
$PSVersionTable.PSVersion
git --version
winget --version
wsl --status
docker --version
docker compose version
python --version
py --version
node --version
```

These commands only ask installed programs for status or version information.
Several may return “not recognized” on a new machine; that is an observation,
not a reason to skip ahead. Record each result. The command names mean:

| Command | What it checks |
|---|---|
| `$PSVersionTable.PSVersion` | PowerShell version |
| `git --version` | whether Git is callable |
| `winget --version` | whether Windows Package Manager is callable |
| `wsl --status` | Windows Subsystem for Linux state |
| `docker ...` | Docker and Compose availability |
| `python ...` / `py ...` | Python launchers |
| `node --version` | Node.js availability |

Create `artifacts/weekly/week-00-preflight.txt` in your capstone repository and paste the output after removing usernames, machine names, account IDs, and paths you do not want to retain.

## 2. Install Python

Use the official Python Install Manager for Windows. The course targets Python 3.13 for broad package compatibility, even though a newer feature series may exist.

```powershell
winget install 9NQ7512CXL7T
```

Close and reopen PowerShell, then:

```powershell
py install 3.13
py -V:3.13 --version
```

If `python` still opens the Microsoft Store or fails, use `py -V:3.13` explicitly and review the official Windows troubleshooting guidance. Do not copy an unknown `python.exe` onto `PATH`.

## 3. Install Docker Desktop

The simplest course path runs n8n and local development services through Docker Compose:

```powershell
winget install --id Docker.DockerDesktop --exact
```

Docker Desktop may require a Windows sign-out/restart, WSL 2 update, virtualization support, and acceptance of its current license terms. Read those terms before installation. After restarting:

```powershell
docker --version
docker compose version
docker run --rm hello-world
```

If Docker Desktop cannot be used, acceptable course fallbacks are:

- a current n8n Cloud trial/plan containing only synthetic data; or
- a local Node installation supported by the current n8n release and n8n installed through npm.

Record the fallback in an architecture decision record. Do not silently switch execution models.

## 4. Optional Node installation

Node is not required when n8n runs in Docker. Install the current supported LTS only if a Week 11 connector or optional tool requires it:

```powershell
winget install --id OpenJS.NodeJS.LTS --exact
node --version
npm --version
```

Check n8n’s current supported Node range before using an npm-based n8n installation.

## 5. Create the capstone repository

Before this section, complete the files/text, command-line, Python, and Git
foundation chapters. The following commands:

1. create a new project folder;
2. move PowerShell into it;
3. initialise local Git tracking;
4. create a project-only Python environment;
5. activate that environment;
6. update its package installer.

```powershell
New-Item -ItemType Directory -Path "$env:USERPROFILE\Documents\supplier-review-system"
Set-Location "$env:USERPROFILE\Documents\supplier-review-system"
git init
py -V:3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

After each line, read the result. Use `Get-Location` after `Set-Location`, use
`git status --short` after `git init`, and use
`python -m pip --version` after activation. The displayed Python/pip path should
point inside `.venv`.

If PowerShell blocks activation, do not weaken the machine-wide execution policy. You can call the virtual-environment interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip --version
```

Copy [`requirements-course.txt`](requirements-course.txt) into the repository, then:

```powershell
python -m pip install -r requirements-course.txt
python -m pip freeze > artifacts\weekly\week-00-pip-freeze.txt
```

The requirements file constrains compatible major/minor families, not a permanent frozen release. After the first successful install, create a lock file using your selected package manager and commit it. The evergreen update audit determines when to refresh it.

## 6. Environment variables

Create `.env.example` with names only:

```dotenv
APP_ENV=dev
APP_BASE_URL=http://host.docker.internal:8000
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_SOURCE_BUCKET=source-originals
SUPABASE_DERIVED_BUCKET=derived-artifacts
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_EXTRACT=gpt-5.6-terra
MODEL_DRAFT=gpt-5.6-terra
MODEL_COMPARE=gpt-5.6-luna
MODEL_EMBED=
MODEL_RESPONSE_STORE=false
KILL_SWITCH=true
ACTION_MODE=stub
LOG_LEVEL=INFO
```

This block is file content, **not PowerShell commands**. Create the file in your
text editor and paste the lines into it. Empty values are placeholders. Never
put a real key into `.env.example`.

Add `.env`, credentials, local databases, derived documents, model caches, and test outputs to `.gitignore`. Commit `.env.example`; never commit `.env`.

Keep `KILL_SWITCH=true` and `ACTION_MODE=stub` until Week 7 explicitly tests the action boundary.

## 7. Start n8n locally

Use the current official n8n Docker instructions as the authority. A minimal learning-only Compose service can begin as:

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:${N8N_VERSION}
    ports:
      - "127.0.0.1:5678:5678"
    environment:
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - GENERIC_TIMEZONE=Europe/Amsterdam
      - TZ=Europe/Amsterdam
      - N8N_SECURE_COOKIE=false
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

This YAML block is file content, **not a PowerShell command**. Save it as
`docker-compose.yml` in the project root. Indentation is meaningful. The later
`docker compose ...` block contains commands.

Rules:

- set `N8N_VERSION` to a version verified by the evergreen audit; do not use an unrecorded floating image in the frozen demo;
- generate a long random `N8N_ENCRYPTION_KEY`, store it outside Git, and back it up securely;
- bind only to localhost for this course;
- do not expose the editor or webhook port to the public internet;
- do not paste API keys into Code nodes or workflow JSON;
- export redacted workflow JSON to `n8n/`;
- back up n8n state before upgrades.

Start and inspect:

```powershell
docker compose pull
docker compose up -d
docker compose ps
docker compose logs --tail 100 n8n
```

Open `http://localhost:5678`, create a local owner account, enable available two-factor authentication, and create credentials through the credential UI.

## 8. Supabase project

Create a separate course project:

1. choose a European region and record the exact region;
2. use a generated database password stored in a password manager;
3. create private buckets `source-originals` and `derived-artifacts`;
4. enable and test Row Level Security on exposed tables;
5. keep the service-role key server-side only;
6. verify that the anonymous key cannot list or fetch private objects;
7. record backup limitations, including object-storage coverage;
8. set a course deletion date.

Start local-first if desired: use PostgreSQL in Docker through Week 6, then migrate through SQL scripts. The schema and tests—not a dashboard configuration—are the reproducible source.

## 9. OpenAI API project

Create a dedicated API project:

1. set a small spend limit and alert;
2. create a project-scoped key;
3. review current data controls and region eligibility;
4. use `store: false`;
5. do not upload the corpus to provider-managed file stores;
6. rotate/delete the key after the course.

If you are eligible for a European regional project, record the configured project region and required base URL. Do not claim EU processing merely because you are located in the EU or use a European Supabase region.

## 10. Smoke tests

### Python and imports

```powershell
python -c "import fastapi, pydantic, pytest, openai; print('core imports ok')"
python -c "import docling; print('docling import ok')"
```

### FastAPI

Create a temporary health route, run:

```powershell
python -m uvicorn supplier_review.api.main:app --reload --port 8000
```

This starts a server and normally does not return to the prompt. Leave that
PowerShell window open. Use a second PowerShell window for the request below.
Press Ctrl+C in the server window when the lesson tells you to stop it.

From a second terminal:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Expected shape:

```json
{"status":"ok","environment":"dev","kill_switch":true}
```

### n8n to FastAPI

From an n8n HTTP Request node, call `http://host.docker.internal:8000/health`. Save the response, status, and timestamp. A browser-only success does not prove container-to-host connectivity.

### Test runner

```powershell
pytest --version
pytest -q
```

### Secret check

Before the first commit:

```powershell
git status --short
git diff -- . ':!*.lock'
```

Inspect workflow exports and artifacts for keys, tokens, real email addresses, local usernames, and connection strings.

## 11. Setup gate

Pass only when:

- the selected Python interpreter and virtual environment are explicit;
- core imports succeed;
- n8n is reachable only locally;
- n8n can call the FastAPI health route;
- `pytest` runs;
- Git shows no secrets;
- Docker/n8n/Python/package versions are recorded;
- the kill switch is on and action mode is stubbed.

If any external account is unavailable, continue with documented local stubs through Week 4. An unavailable model account blocks Week 5’s live API lab but not schema, fixture, or mocked-response tests.

## Common setup failures

| Symptom | Likely cause | Safe response |
|---|---|---|
| `python` opens Store | Windows app execution alias | use official Python manager and `py -V:3.13`; fix aliases |
| `Activate.ps1` blocked | execution policy | call `.venv\Scripts\python.exe` directly |
| n8n cannot reach API | `localhost` resolves inside container | use `host.docker.internal` |
| n8n cookie/login loop | local HTTP vs secure-cookie setting | use the documented local-only setting; never copy it to public hosting |
| Docling install is large | PyTorch/model dependencies | use the documented CPU path and retain disk-space notes |
| OCR language is wrong | missing Dutch/English model/config | install/configure required language data, then rerun scan cases |
| Supabase query works with service key only | RLS/policy not tested | test anon/authenticated roles; service key must not mask policy failure |
| key appears in Git | `.gitignore` too late or workflow export leak | revoke it, remove from history safely, add secret scanning |
