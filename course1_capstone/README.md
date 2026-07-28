# Course 1 runnable capstone — controlled operations exception workflow

## What this is

This folder contains the working reference implementation taught in Modules
4-6. It turns a synthetic comma-separated values (CSV) file into:

1. validated work items;
2. deterministic, source-linked issues;
3. a bounded offline-mock summary and human-review actions;
4. a review package and protected review manifest;
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
- Values from the unconstrained source-reference, title, owner-role, and
  category prose fields remain inert and are never copied into generated
  summary prose. Controlled issue IDs, rule messages, fields, and row numbers
  provide the summary evidence instead.
- Headlines use one of two controlled count templates. Group prose is rendered
  from verified issue evidence, and review instructions use one exact
  source-row/field template that forbids external action. Setting a boolean to
  `false` never makes arbitrary action text safe.
- Approve, edit, reject, and expire are separate recorded decisions.
- A canonical run configuration binds the source hash, expected-oracle
  presence/hash, fixed date, rule/pipeline/prompt versions, requested adapter
  mode, and mock/fallback versions. A material change creates a different run.
- A review manifest fingerprints the protected source, issue JSON and
  spreadsheet-safe issue CSV, the copied expected-issue oracle (or explicit
  no-oracle marker), summary, control, run configuration, and review package.
- An approval is bound to one exact review-manifest hash and revision.
- `decision_id` is recomputed from every material decision field. This detects
  local accidental or unsophisticated editing; it does not authenticate the
  reviewer and is not a digital signature.
- Only an unexpired approval with completed evidence review can create local
  draft exports. The JSON/CSV pair is fully checked and staged before either
  approved filename is published. State, evaluation, and audit finalization is
  transactional: a later persistence failure removes the pair and restores the
  prior controlled files. A visible `outbox/INCOMPLETE.txt` marker blocks use if
  rollback itself cannot finish.
- Every workspace/run operation uses an exclusive local lock. A simultaneous
  operation safely stops. After a crash, verify that no runner process remains
  before a human removes an abandoned lock; never remove it merely to bypass
  the control.
- A new run is assembled and validated in a private staging folder. Its complete
  folder is published in one move, and `latest_run.txt` is written only after
  that publication. A failed first attempt can therefore be retried safely.

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
    ├── source/expected_issues.evidence
    ├── issues/issues.csv
    ├── issues/issues.json
    ├── draft/summary.json
    ├── review/review_package.json
    ├── review/review_manifest.json
    ├── review/decision-r1.json       only after a decision
    ├── audit/events.jsonl
    ├── evaluation.json
    ├── manual_fallback.md
    ├── control.json
    ├── run_config.json
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
the last valid workflow state. The stable
`failures/latest.json` shows the latest occurrence, while each immutable
occurrence is kept beside it as `failures/a0001.json`, `a0002.json`, and so on.
The error code is inside each file. These deliberately short names leave room
for the exact long Windows learner paths used in the course.

CSV files prefix a dangerous spreadsheet formula marker (`=`, `+`, `-`, or
`@`, including after leading whitespace/control characters) with an apostrophe.
The JSON register and protected source retain the exact evidence text.

A successful local export always has exactly one matching
`local_export_created` audit event. If that material event is missing,
duplicated, or out of order, the runner stops. It never invents a replacement
audit event.

**JavaScript Object Notation Lines (JSONL)** means one JSON object per text
line. It keeps separate audit events readable while each updated history is
written atomically.

## Recover an abandoned lock after a crash

Use this only after a computer or terminal crash and only when the runner says
`concurrent_operation`. A lock is a safety control, not an error to delete
routinely.

1. Close every terminal in which you started this Course 1 runner.
2. Open a new PowerShell window.
3. Run this exact process check:

```powershell
$runnerProcesses = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -and (
        $_.CommandLine -match 'course1_capstone[\\/]+cli\.py' -or
        $_.CommandLine -match 'course1_capstone\.cli'
    )
}
$runnerProcesses | Select-Object ProcessId, Name, CommandLine
if ($runnerProcesses) {
    throw 'STOP: a Course 1 runner process is still active. Do not remove any lock.'
}
'PROOF: no active Course 1 runner process was found.'
```

If this command reports an access error, you do not have proof: do not remove
the lock. If it shows any process row, wait for that process to finish or close
it normally, then run the check again.

4. Only after PowerShell prints the `PROOF` line, copy the exact lock path from
   the affected workspace or `RUN-...` folder and run:

```powershell
$lockPath = Read-Host 'Paste the exact full path to .course1-operation.lock'
if ((Split-Path -Leaf $lockPath) -cne '.course1-operation.lock') {
    throw 'STOP: this is not the Course 1 lock filename.'
}
Get-Item -LiteralPath $lockPath
Remove-Item -LiteralPath $lockPath
```

5. Run `status` before trying another decision, revision, or export. If `status`
   safely stops on an incomplete transaction or integrity mismatch, keep every
   file unchanged and use the manual recovery route; deleting another marker is
   not a repair.

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
