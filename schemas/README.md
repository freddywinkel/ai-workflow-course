# Portable Contract Schemas

- [`contracts.schema.json`](contracts.schema.json) validates the six core records.
- [`golden_case.schema.json`](golden_case.schema.json) validates one corpus gold record at the course boundary.

Use JSON Schema Draft 2020-12. Generate Pydantic models and database migrations from one reviewed domain definition, then test that serialised records validate here. Do not loosen the schema to make a failed model response pass.

Validation example:

```powershell
python -c "import json, jsonschema; s=json.load(open('schemas/contracts.schema.json', encoding='utf-8')); jsonschema.Draft202012Validator.check_schema(s); print('schema ok')"
```

The schema constrains representation, not truth. Semantic, evidence, tenant, state, approval, and idempotency checks remain code/database responsibilities.

