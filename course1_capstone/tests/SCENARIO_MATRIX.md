# Course 1 executable scenario matrix

Run all scenarios from the course repository:

```powershell
$pythonExe = Join-Path (Get-Location) '.venv\Scripts\python.exe'
& $pythonExe -m unittest discover -s course1_capstone\tests -v
```

| Required scenario | Fixture or test | Expected control |
|---|---|---|
| valid row | `valid_no_issue.csv` | named `no_action_needed` state; no draft or export |
| missing required value | frozen and recreated data | R001 with source evidence |
| invalid status | frozen data | R002 |
| duplicate item ID | `duplicate_work_item_id.csv` | safe stop |
| duplicate reference | frozen data | R010 for both rows |
| contradictory dates | frozen and recreated data | R005 |
| overdue open item | frozen and recreated data | R011 |
| review without evidence | `test_required_review_without_evidence...` | safe stop |
| stale update | `test_stale_update...` | safe stop |
| malformed input | `malformed_input.csv` | safe stop |
| untrusted free-text instruction | `untrusted_instruction.csv` | inert source text |
| all untrusted prose fields | generated four-row fixture | source text never becomes summary prose |
| missing file | `test_missing_input_file...` | safe stop |
| unexpected header | `unexpected_header.csv` | safe stop |
| duplicate retry | `test_duplicate_retry...` | same run, one logical effect |
| overlapping decision/retry/failure recording | deterministic threaded lock test | one decision, retry, and failure event; no lost writes |
| interrupted initial prepare | injected write matrix for issue and no-action runs | private staging removed; retry publishes one logical history |
| changed run configuration | mode/oracle identity test | distinct run; no stale reuse |
| AI disabled | fault mode `disabled` | deterministic fallback |
| AI timeout | fault mode `timeout` | deterministic fallback |
| AI refusal | fault mode `refusal` | deterministic fallback |
| malformed AI JSON | fault mode `malformed_json` | deterministic fallback |
| unknown AI reference | fault mode `unknown_issue_id` | deterministic fallback |
| edited approved draft | `test_edited_draft...` | approval invalid |
| protected issue/manifest tamper | manifest and schema-valid message tests | export blocked |
| coordinated state/evaluation oracle tamper | protected-oracle test | inspect/export blocked by immutable run evidence |
| edited decision expiry/reason/reviewer | decision-integrity tests | export blocked |
| rejected review | decision test | no export |
| edit request | decision and revision tests | no export until new review |
| expired review | expiry test | no export and named expired state |
| external actions false | export and tamper tests | local CSV/JSON only |
| partial or failed paired export | conflict/promotion tests | no lone approved artifact |
| state/audit/evaluation failure after pair promotion | injected finalization tests | pair and controlled changes roll back; retry creates exactly one export audit event |
| missing, duplicate, or reordered material audit | audit-history reconciliation tests | fail closed; no audit event is invented |
| completed pair missing export audit | fail-closed export audit test | inspect/export blocked; existing pair is not changed |
| spreadsheet-formula prefixes | generated CSV fixture | safe CSV; exact JSON evidence |
| damaged state or audit | command-line corruption tests | named `failed_manual` evidence |
| repeated safe stop | repeated candidate failure | unique attempt history, unchanged business state |
| long Windows learner path | path-budget test | short latest/attempt evidence and atomic temp names remain below 260 characters |

The runner tests use only temporary folders, synthetic fixtures, and the
Python standard library. The schema-contract test additionally uses the pinned
`jsonschema` development dependency. No test makes a network call or performs
an external action.
