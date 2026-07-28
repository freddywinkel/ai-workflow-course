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
| missing file | `test_missing_input_file...` | safe stop |
| unexpected header | `unexpected_header.csv` | safe stop |
| duplicate retry | `test_duplicate_retry...` | same run, one logical effect |
| AI disabled | fault mode `disabled` | deterministic fallback |
| AI timeout | fault mode `timeout` | deterministic fallback |
| AI refusal | fault mode `refusal` | deterministic fallback |
| malformed AI JSON | fault mode `malformed_json` | deterministic fallback |
| unknown AI reference | fault mode `unknown_issue_id` | deterministic fallback |
| edited approved draft | `test_edited_draft...` | approval invalid |
| rejected review | decision test | no export |
| edit request | decision and revision tests | no export until new review |
| expired review | expiry test | no export and named expired state |
| external actions false | export and tamper tests | local CSV/JSON only |

The tests use only temporary folders, synthetic fixtures, and the Python
standard library. They make no network call and perform no external action.
