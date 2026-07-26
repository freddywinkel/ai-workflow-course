# Course 1 Portable Contract Schemas

These JSON Schema Draft 2020-12 files define the capstone boundaries:

- `work_item.schema.json` — normalized synthetic work item;
- `issue.schema.json` — deterministic verified exception;
- `summary.schema.json` — optional AI or offline summary;
- `approval.schema.json` — human decision bound to an exact draft revision;
- `audit_event.schema.json` — material workflow event.

Validate a schema:

```powershell
python -c "import json, jsonschema; s=json.load(open('schemas/work_item.schema.json', encoding='utf-8')); jsonschema.Draft202012Validator.check_schema(s); print('schema ok')"
```

JSON Schema constrains representation. It does not prove that a value is true,
that an issue is correct, or that a workflow is compliant. Deterministic rules,
cross-record checks, evidence verification, state transitions, authorization,
and idempotency remain separate responsibilities.

Do not loosen a schema merely to make a failing model response pass.
