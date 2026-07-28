# Module 4 — Build the Rule-Based Workflow Before Adding Artificial Intelligence (AI)

## Outcome

Python is a programming language. You will run a complete local Python workflow
that preserves the synthetic source, applies R001–R011 without AI, writes stable
issue records, records named states, and reproduces the 13 frozen expected
issues. You will then recreate the run with a different synthetic dataset and
expected result.

Artificial Intelligence (AI) means software that can generate or infer an
answer rather than follow only fixed rules. This module deliberately starts
with fixed, inspectable business rules.

Windows PowerShell is the Windows command application used for the exact
commands below.

## Beginner checkpoint

Start when Module 3 passes and `python --version` prints a Python version.
If Windows says Python is not found, return to Foundation 3 rather than
changing the instructions.

## Concepts

- **Validation** checks that input meets an explicit contract.
- **Normalisation** creates a controlled value while preserving the raw value.
- **Idempotency** means repeating the same input does not create duplicate
  logical effects.
- A **run identifier (ID)** identifies one processing run.
- A **named state** makes success, waiting, or failure visible.
- **JavaScript Object Notation (JSON)** is a plain-text structured-data format.
- **Comma-separated values (CSV)** is a plain-text table format.
- **Secure Hash Algorithm 256-bit (SHA-256)** creates the file fingerprints
  used below; PowerShell spells its command option `SHA256`.
- **International Organization for Standardization (ISO) date format** uses
  `YYYY-MM-DD`: year, month, then day.
- **EUR** is the three-letter currency code for the euro.
- Python's standard-library **`hashlib` module** calculates hashes such as
  SHA-256.
- A **manual failure** stops safely and sends the case to a person.

## Official readings

1. [Python `csv` module](https://docs.python.org/3/library/csv.html)
2. [Python errors and exceptions](https://docs.python.org/3/tutorial/errors.html)
3. [Python `hashlib` module](https://docs.python.org/3/library/hashlib.html)

## Guided build

The worked script is complete and runnable. Read each labelled function before
running it. The independent recreation changes the data and output names and
requires a new prediction.

Notepad is the Windows plain-text editor used to create practice files.

## Follow along — I show you exactly how

### Stage 1 — Prepare controlled inputs

Open Windows PowerShell and run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
if (-not (Test-Path (Join-Path $projectRoot '.git'))) {
    throw 'Project repository not found. Complete Windows Setup before Module 4.'
}
$moduleFolder = Join-Path $projectRoot 'evidence\module-04'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
Copy-Item -LiteralPath (Join-Path $courseRoot 'practice_data\work_items.csv') -Destination .\worked_work_items.csv
Copy-Item -LiteralPath (Join-Path $courseRoot 'practice_data\expected_issues.csv') -Destination .\worked_expected_issues.csv
Copy-Item -LiteralPath (Join-Path $courseRoot 'templates\architecture_decision_record.md') -Destination .\recreated_architecture_decision.md
Get-FileHash .\worked_work_items.csv -Algorithm SHA256
```

Record the printed Secure Hash Algorithm 256-bit (SHA-256) value in
`input_hash_before.txt`. Do this in Notepad.

**Expected result:** two CSV files and one 64-character hexadecimal hash.

Create `worked_architecture_decision.md` in Notepad and paste:

```markdown
# ADR-001 — Local deterministic rule checker

Status: accepted
Date: 2026-07-28
Owner/reviewer: course learner acting in both synthetic roles

## Context

The synthetic exception process needs reproducible R001-R011 checks, preserved
source input, visible failures, and no external action.

## Decision drivers

- Safety/integrity: source remains unchanged; invalid input stops safely.
- Evidence/provenance: every issue links to row, field, raw value, and rule.
- Portability: comma-separated values and JSON remain readable.
- Cost/latency: local standard-library Python needs no paid service.
- Privacy/security: synthetic files stay local and contain no secret.
- Operability: a person can inspect output and use manual fallback.

## Options considered

| Option | Benefits | Risks/costs | Evidence/test |
|---|---|---|---|
| Manual inspection only | simplest fallback | inconsistent at volume | retained as fallback |
| Local deterministic Python | exact and testable | learner must maintain rules | selected; frozen expected set |
| Generative AI issue detection | flexible wording | variable and unnecessary | rejected for rule detection |

## Decision

Use local deterministic Python for validation and R001-R011. Exclude network
calls, source write-back, and external actions.

## Consequences

Positive: exact repeatable evidence.
Negative/residual risk: incorrect written rules still produce incorrect code.
Required controls: frozen expected set, hashes, named failure state, review.
Migration/exit path: keep CSV and documented rules; use manual review.

## Verification

Tests: 13 worked issue keys plus a different five-issue recreation.
Reassessment trigger: input schema, rule, severity, or action scope changes.
```

Create `worked_to_be_architecture.md` in Notepad and paste:

```text
# Worked to-be architecture

[Preserved synthetic CSV input]
              |
              v
[Header and value validation] -- invalid --> [failed_manual + evidence]
              |
              v
[Deterministic rules R001-R011]
              |
              v
[Stable issue CSV + JSON run summary]
              |
              v
[Human review in later modules]

External connections: none.
External actions: none.
Source write-back: none.
```

This is a **to-be architecture diagram**: a compact picture of the designed
future workflow, including its safe failure route. The arrows show flow; they
do not run code.

### Stage 2 — Create the complete deterministic checker

Run `notepad .\worked_checker.py`, click **Yes**, paste the complete program,
save, and close:

```python
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT_FILE = BASE / "worked_work_items.csv"
OUTPUT_FILE = BASE / "found_issues.csv"
SUMMARY_FILE = BASE / "run_summary.json"
FAILURE_FILE = BASE / "failed_manual.json"
ASSESSMENT_DATE = date.fromisoformat("2026-07-26")

HEADERS = [
    "work_item_id", "source_reference", "title", "owner_role", "status",
    "priority", "received_date", "due_date", "completed_date", "amount",
    "currency", "category",
]
STATUSES = {"new", "in_progress", "waiting", "completed", "cancelled"}
OPEN_STATUSES = {"new", "in_progress", "waiting"}
OWNER_STATUSES = {"in_progress", "waiting", "completed"}
PRIORITIES = {"low", "medium", "high"}
DATE_FIELDS = ("received_date", "due_date", "completed_date")


def blank(value: str) -> bool:
    return value.strip() == ""


def parse_date(value: str) -> date | None:
    if len(value) != 10 or value[4] != "-" or value[7] != "-":
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.isoformat() == value else None


def parse_amount(value: str) -> Decimal | None:
    try:
        parsed = Decimal(value)
    except (InvalidOperation, ValueError):
        return None
    return parsed if parsed.is_finite() else None


def add_issue(
    issues: list[dict[str, str]],
    row: dict[str, str],
    field: str,
    rule: str,
    severity: str,
    message: str,
) -> None:
    work_id = row["work_item_id"]
    issues.append(
        {
            "issue_id": f"{work_id}|{rule}|{field}",
            "work_item_id": work_id,
            "source_reference": row["source_reference"],
            "field": field,
            "raw_value": row[field],
            "rule_code": rule,
            "severity": severity,
            "message": message,
            "assessment_date": ASSESSMENT_DATE.isoformat(),
        }
    )


def main() -> None:
    input_bytes = INPUT_FILE.read_bytes()
    input_hash = hashlib.sha256(input_bytes).hexdigest()
    states = ["received"]

    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != HEADERS:
            raise ValueError(
                f"Header mismatch. Expected {HEADERS}; got {reader.fieldnames}"
            )
        rows = list(reader)
    states.append("validated")

    issues: list[dict[str, str]] = []
    parsed_dates: dict[str, dict[str, date | None]] = {}

    for row in rows:
        for field in (
            "work_item_id", "source_reference", "title",
            "received_date", "category",
        ):
            if blank(row[field]):
                add_issue(
                    issues, row, field, "R001", "medium",
                    f"Required {field} is missing.",
                )

        status = row["status"].strip()
        priority = row["priority"].strip()
        if status not in STATUSES:
            add_issue(
                issues, row, "status", "R002", "high",
                "Status is not in the allowed list.",
            )
        if priority not in PRIORITIES:
            add_issue(
                issues, row, "priority", "R003", "medium",
                "Priority is not in the allowed list.",
            )

        row_dates: dict[str, date | None] = {}
        for field in DATE_FIELDS:
            raw = row[field].strip()
            parsed = parse_date(raw) if raw else None
            row_dates[field] = parsed
            if raw and parsed is None:
                add_issue(
                    issues, row, field, "R004", "high",
                    "Date must use ISO format YYYY-MM-DD.",
                )
        parsed_dates[row["work_item_id"]] = row_dates

        received = row_dates["received_date"]
        due = row_dates["due_date"]
        if received is not None and due is not None and due < received:
            add_issue(
                issues, row, "due_date", "R005", "high",
                "Due date is before received date.",
            )

        completed_raw = row["completed_date"].strip()
        if status == "completed" and not completed_raw:
            add_issue(
                issues, row, "completed_date", "R006", "high",
                "Completed work requires a completion date.",
            )
        elif status in (STATUSES - {"completed"}) and completed_raw:
            add_issue(
                issues, row, "completed_date", "R006", "medium",
                "Non-completed work must not have a completion date.",
            )

        if status in OWNER_STATUSES and blank(row["owner_role"]):
            add_issue(
                issues, row, "owner_role", "R007", "medium",
                "Active work requires an owner role.",
            )

        amount_raw = row["amount"].strip()
        currency = row["currency"].strip()
        if amount_raw:
            amount = parse_amount(amount_raw)
            if amount is None or amount < 0:
                add_issue(
                    issues, row, "amount", "R008", "high",
                    "Amount must be a non-negative decimal.",
                )
            if currency != "EUR":
                add_issue(
                    issues, row, "currency", "R009", "medium",
                    "A populated amount requires currency EUR.",
                )
        elif currency:
            add_issue(
                issues, row, "currency", "R009", "medium",
                "Currency must be blank when amount is blank.",
            )

    reference_counts = Counter(
        row["source_reference"].strip()
        for row in rows
        if row["source_reference"].strip()
    )
    for row in rows:
        reference = row["source_reference"].strip()
        if reference and reference_counts[reference] > 1:
            add_issue(
                issues, row, "source_reference", "R010", "high",
                f"Source reference {reference} is duplicated.",
            )

    for row in rows:
        due = parsed_dates[row["work_item_id"]]["due_date"]
        if (
            row["status"].strip() in OPEN_STATUSES
            and due is not None
            and due < ASSESSMENT_DATE
        ):
            add_issue(
                issues, row, "due_date", "R011", "high",
                "Open work is overdue on the fixed assessment date.",
            )

    issues.sort(
        key=lambda item: (
            item["work_item_id"], item["rule_code"], item["field"]
        )
    )
    output_fields = [
        "issue_id", "work_item_id", "source_reference", "field", "raw_value",
        "rule_code", "severity", "message", "assessment_date",
    ]
    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(issues)

    states.append("issues_ready" if issues else "no_action_needed")
    summary = {
        "run_id": "RUN-" + hashlib.sha256(
            (input_hash + ASSESSMENT_DATE.isoformat()).encode("utf-8")
        ).hexdigest()[:12],
        "input_sha256": input_hash,
        "assessment_date": ASSESSMENT_DATE.isoformat(),
        "states": states,
        "issue_count": len(issues),
        "output_file": OUTPUT_FILE.name,
        "external_actions": 0,
    }
    SUMMARY_FILE.write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    if FAILURE_FILE.exists():
        FAILURE_FILE.unlink()
    print(f"{summary['run_id']}: {len(issues)} issues; state={states[-1]}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        FAILURE_FILE.write_text(
            json.dumps(
                {"state": "failed_manual", "error": str(error)}, indent=2
            ) + "\n",
            encoding="utf-8",
        )
        print(f"SAFE STOP: {error}")
        raise SystemExit(1)
```

What each part does:

- constants make file names and the assessment date explicit;
- parsing functions refuse invalid dates and amounts;
- `add_issue` keeps source evidence with each result;
- `main` checks the header before rules;
- deterministic checks create issues;
- duplicate and overdue checks run after valid prerequisites exist;
- output is overwritten on an identical rerun, so no duplicate effect occurs;
- exceptions create `failed_manual.json` and stop.

### Stage 3 — Run and verify the worked example

Run:

```powershell
python .\worked_checker.py
$found = Import-Csv .\found_issues.csv
$gold = Import-Csv .\worked_expected_issues.csv
$found.Count
$foundKeys = $found | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)" }
$goldKeys = $gold | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)" }
Compare-Object $goldKeys $foundKeys
Get-Content .\run_summary.json
Get-FileHash .\worked_work_items.csv -Algorithm SHA256
```

**Expected output:**

- `RUN-...: 13 issues; state=issues_ready`;
- count `13`;
- `Compare-Object` prints nothing, meaning the key sets match;
- JSON shows `external_actions` equal to 0;
- the input hash matches `input_hash_before.txt`.

Run the checker again. The run ID and issue count must remain identical, and
`found_issues.csv` must still contain 13 rows.

**Troubleshooting:**

- `SyntaxError` usually means a line was missed while pasting. Compare the line
  shown in red with the worked program.
- A header mismatch means the CSV changed or the wrong file was copied. Do not
  relax the header check.
- Extra `Compare-Object` lines identify missed (`<=`) or extra (`=>`) keys.
- Never edit `worked_expected_issues.csv` to remove a difference.

## Now recreate it yourself

1. Create `recreated_items.csv` in Notepad:

```csv
work_item_id,source_reference,title,owner_role,status,priority,received_date,due_date,completed_date,amount,currency,category
WI-9001,REF-9001,,ops,new,low,2026-07-20,2026-08-01,,,,general
WI-9002,REF-9002,Valid completed item,ops,completed,medium,2026-07-10,2026-07-20,2026-07-19,0,EUR,general
WI-9003,REF-9003,Due before received,ops,completed,high,2026-07-12,2026-07-10,2026-07-15,,,general
WI-9004,REF-9004,Unexpected completion,ops,in_progress,medium,2026-07-20,2026-08-01,2026-07-25,,,general
WI-9005,REF-9005,Negative amount,ops,completed,high,2026-07-01,2026-07-20,2026-07-19,-1,EUR,general
WI-9006,REF-9006,Overdue waiting item,ops,waiting,high,2026-07-01,2026-07-10,,,,general
```

2. Write `recreated_expected.csv` yourself with this exact content:

```csv
work_item_id,rule_code
WI-9001,R001
WI-9003,R005
WI-9004,R006
WI-9005,R008
WI-9006,R011
```

This is the result you predict before running the checker. It is different
from the worked example because the six recreated rows are new.
3. Copy the program and open it:

```powershell
Copy-Item .\worked_checker.py .\recreated_checker.py
notepad .\recreated_checker.py
```

Change only:

- `worked_work_items.csv` to `recreated_items.csv`;
- `found_issues.csv` to `recreated_found_issues.csv`;
- `run_summary.json` to `recreated_run_summary.json`;
- `failed_manual.json` to `recreated_failed_manual.json`.

Save, close, and run:

```powershell
python .\recreated_checker.py
$recreatedFound = Import-Csv .\recreated_found_issues.csv
$recreatedExpected = Import-Csv .\recreated_expected.csv
$recreatedFound.Count
$recreatedFound | Select-Object work_item_id,rule_code,field,severity
$recreatedKeys = $recreatedFound | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)" }
$recreatedExpectedKeys = $recreatedExpected | ForEach-Object { "$($_.work_item_id)|$($_.rule_code)" }
Compare-Object $recreatedExpectedKeys $recreatedKeys
```

**Expected output:** five issues with the five predicted pairs and no
`Compare-Object` output.

This recreation uses different rows, identifiers, amounts, statuses, and rule
combinations. If it fails, fix your data or the four configured file names;
do not weaken a rule.

Using the worked decision as the example, complete the different
`recreated_architecture_decision.md`, then create
`recreated_to_be_architecture.md`. Your new diagram must show the capstone's
preserved input, validation, deterministic rules, named success and
`failed_manual` states, evidence outputs, later bounded summary and human
review, manual fallback, and zero external action or source write-back. Use
your own layout rather than copying the worked low-detail diagram.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path` to obtain the full path, replace
`[PASTE FULL PATH HERE]`, and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
[PASTE FULL PATH HERE]

Do not edit, create, delete, rename, move, format, or execute files. Do not
inspect the parent or another folder. This folder must contain no secrets and
no real client or workplace data. Stop if you find credentials, personal data,
or health data.

Inspect the Python, CSV, JSON, and architecture files. Return:
1. PASS or NOT YET;
2. checks for: exact header stop; preserved raw values; configured date
2026-07-26; R001-R011 implemented deterministically; invalid-date dependency;
both duplicate rows reported; stable issue IDs; evidence fields; 13 worked
issues matching gold keys; five recreated issues matching its expected keys;
stable rerun design; named states; failed_manual path; zero external actions;
synthetic data only; worked and completed recreated architecture decisions;
worked and recreated to-be diagrams with the normal path, failure path,
evidence, human review, and system boundaries;
3. the smallest corrections I should make if NOT YET.

Remain read-only. Do not run the scripts or supply replacement code.
```

## Pass criteria

- [ ] Worked run produces exactly 13 matching issue keys.
- [ ] Independent run produces exactly five predicted issue keys.
- [ ] Input hashes remain unchanged.
- [ ] Header mismatch causes a safe stop.
- [ ] Invalid dates cannot feed dependent comparisons.
- [ ] Every issue includes row, field, raw value, rule, severity, and date.
- [ ] Identical reruns have the same run ID and no duplicate rows.
- [ ] States and `failed_manual` are visible.
- [ ] External actions remain zero.
- [ ] Worked and recreated architecture decisions and to-be diagrams show
      normal flow, safe failure, evidence, human review, and system boundaries.
- [ ] Codex returns `PASS` read-only.

### Record your Module 4 PASS in Git

Do this only after Codex returns `PASS`. Git records the evidence inside the
same project repository created during Windows Setup. It does not upload it.

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-04"
git commit -m "complete module 4 evidence"
git status --short
```

If Git reports `nothing to commit`, confirm that `evidence/module-04` was
already recorded and unchanged. Never add a secret, real workplace file, or
unfamiliar file merely to make the message disappear.

## Consultant lens

The first implementation should make deterministic business rules visible,
testable, and replaceable. A workflow canvas may orchestrate the same steps
later, but it must not hide contracts or failure behaviour.

## Capstone increment

The capstone has a to-be architecture, functioning non-AI issue detector,
stable outputs, named states, deterministic evaluation, and manual failure
route.

## Required artifact

The teaching contract creates worked and recreated code, inputs, outputs,
expected results, hashes, run summaries, an architecture decision, and to-be
diagrams under `evidence/module-04`.

## Test gate

The **Pass criteria** are the complete gate.

## Stop or rework

Stop when input was modified, gold was edited, a rule was weakened to pass,
exceptions disappear without a named failure state, or any external action was
added.

## Common failures

- Pasting partial Python code.
- Comparing unvalidated dates.
- Using the current day instead of configuration.
- Appending duplicate output on rerun.
- Treating a traceback as an adequate business failure route.

## Estimated time

12–16 hours.
