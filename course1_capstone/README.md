# Course 1 runnable capstone — controlled operations exception workflow

## What this is

This folder contains the working reference implementation taught in Modules
4-6. It turns a synthetic comma-separated values (CSV) file into:

1. validated work items;
2. deterministic, source-linked issues;
3. a bounded offline-mock summary and human-review actions;
4. a review package;
5. one explicit human decision;
6. local CSV and JavaScript Object Notation (JSON) exports, but only after a
   valid approval;
7. audit and evaluation evidence.

It is not a client system. It has no network client, external-system connector,
send function, payment function, source write-back, or paid service.

The workflow runtime uses only Python's standard library. The automated schema
acceptance uses the pinned `jsonschema` package installed by Windows Setup;
that package validates file shapes and does not add a provider connection.

## Safety boundary

- Only fictional course data is allowed.
- The command refuses to start without
  `I_CONFIRM_SYNTHETIC_DATA_ONLY`.
- `EXTERNAL_ACTIONS_ENABLED` must be exactly `false`.
- The “AI” is a saved offline behavior. No provider or key is used.
- Timeout, refusal, malformed output, and unknown-reference modes are simulated
  locally and route to a deterministic fallback.
- Approve, edit, reject, and expire are separate recorded decisions.
- An approval is bound to one exact draft hash and revision.
- Only an unexpired approval with completed evidence review can create local
  draft exports.

The synthetic confirmation is a deliberate stop-and-think control, not a
technical way to prove that arbitrary data is fictional. You remain
responsible for never placing real data in this runner.

## Folder map

```text
course1_capstone/
├── cli.py                    learner-facing commands
├── workflow.py               controlled workflow logic
├── fixtures/                 synthetic recreation and failure inputs
└── tests/                    executable normal and failure scenarios
```

A prepared run has this structure:

```text
workspace/
├── latest_run.txt
└── runs/RUN-.../
    ├── source/work_items.csv
    ├── issues/issues.csv
    ├── issues/issues.json
    ├── draft/summary.json
    ├── review/review_package.json
    ├── review/decision-r1.json       only after a decision
    ├── audit/events.jsonl
    ├── evaluation.json
    ├── manual_fallback.md
    ├── control.json
    ├── state.json
    └── outbox/                       only after valid approval
```

`latest_run.txt` stores only a neutral workspace-relative locator such as
`runs/RUN-...`; it never stores your Windows username or an absolute computer
path. The learner lessons show how to join that locator to its workspace before
opening the run. Learner-facing command results likewise print only a run
identifier or an artifact path relative to the controlled workspace.

The `status` command separates `current_state`, the last valid persistent
workflow state, from `latest_attempt_state`, the newest audit-event state. A
safe stop records `latest_attempt_state: failed_manual` without overwriting
the last valid workflow state.

**JavaScript Object Notation Lines (JSONL)** means one JSON object per text
line. It lets the audit file append separate events while remaining readable.

## Exact interpreter rule

The Windows setup creates one project-specific Python environment. Every
course command calls its interpreter directly; activation is unnecessary.

From the learner project repository:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Project Python is missing. Return to Windows Setup.'
}
& $pythonExe --version
```

Do not replace `& $pythonExe` with bare `python`. The exact path prevents
Windows from silently using another Python installation.

## Maintainer acceptance command

From the course package repository, after its `.venv` is set up:

```powershell
$pythonExe = Join-Path (Get-Location) '.venv\Scripts\python.exe'
& $pythonExe -m unittest discover -s course1_capstone\tests -v
```

The complete mapping from acceptance requirement to test is in
`tests/SCENARIO_MATRIX.md`.

## Canonical issue identity

Every issue is identified by all three values:

```text
(work_item_id, rule_code, field)
```

The string form is `WI-0002|R007|owner_role`. Keeping the field prevents two
valid findings from collapsing when one rule applies to more than one field.

## Why the evaluation initially says REWORK

The runner proves only the technical slice taught in Modules 4-6. It cannot
prove process discovery, risk ownership, value, adoption, or handover. The
technical evaluation therefore remains `REWORK` until the learner completes
Modules 1-3 and 7-9 and records a supported final Course 1 decision. Passing
this runner is evidence of a bounded capability, not consulting or production
readiness.
