# Course 1 Portable Contract Schemas

These JavaScript Object Notation (JSON) Schema Draft 2020-12 files define the
same artifact contract used by `course1_capstone/workflow.py`:

- `work_item.schema.json` — normalized synthetic work item;
- `issue.schema.json` — deterministic verified exception;
- `summary.schema.json` — source-linked offline-mock or fallback summary;
- `approval.schema.json` — one human decision bound to one exact draft;
- `audit_event.schema.json` — one material workflow event;
- `evaluation.schema.json` — the technical evaluation result.

The canonical identity of an issue is the exact triple
`(work_item_id, rule_code, field)`. The `issue_id` stores that triple as
`WI-0001|R001|title`. Never compare only the work-item identifier and rule:
one rule may correctly flag more than one field.

From the course repository, validate all schemas through the exact project
interpreter:

```powershell
$pythonExe = Join-Path (Get-Location) '.venv\Scripts\python.exe'
& $pythonExe -c "import json, pathlib, jsonschema; files=sorted(pathlib.Path('schemas').glob('*.schema.json')); [jsonschema.Draft202012Validator.check_schema(json.loads(p.read_text(encoding='utf-8'))) for p in files]; print(f'{len(files)} schemas OK')"
```

JSON Schema constrains representation. It does not prove that a value is true,
an issue is correct, or a workflow is compliant. The runner separately checks
business rules, cross-record conditions, evidence links, state transitions,
authorization, expiry, and idempotency.

Do not loosen a schema merely to make a failing mock or model response pass.
