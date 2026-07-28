# Completed Example — Tool Fit and Ownership Record

- Artifact ID: WORKED-M07-TOOL-FIT
- Version/date: 1.0 / 2026-07-28
- Author/reviewer: course learner / fictional operations lead
- Workflow/intended-purpose version: low-stock review list 1.0

Artificial intelligence (AI) is one option to assess, not the default
selection. An application programming interface (API) is a software connection;
this worked decision uses neither AI nor an API.

## Requirements before products

| Requirement | Must/Should/Could | Evidence/test | Owner |
|---|:---:|---|---|
| named success/failure/review states | Must | scenario tests | process owner |
| exact-draft review before use | Must | approval/hash drill | operations lead |
| local synthetic data and scoped access | Must | path/access check | support role |
| evidence and change history | Must | saved outputs and Git log | course learner |
| tiny weekly volume; no latency promise | Should | fictional baseline | process owner |
| use current spreadsheet environment first | Must | option comparison | operations lead |
| CSV export, backup, and manual exit | Must | restore drill | support role |
| plain-language keyboard-usable instructions | Must | task test | adoption owner |
| no paid recurring service for Course 1 | Must | software inventory | operations lead |

## Options

| Option | Requirements met | Gaps/risks | Setup effort | Recurring cost | Maintainable by | Evidence |
|---|---|---|---:|---:|---|---|
| Manual checklist/spreadsheet | all core control needs at tiny volume | repeated time | 1 hour | EUR 0 scenario | coordinator | current fallback |
| Existing business platform | unknown until client discovery | feature/ownership unknown | unknown | unknown | client admin | not tested |
| Visual orchestrator | possible states and approval | unnecessary service/admin burden | 1–2 days scenario | unknown | trained admin | not needed |
| Small code/API component | useful only as learning proof | maintenance skill | 2–4 days scenario | EUR 0 local | trained support role | Course 1 prototype |
| Combined architecture | excessive | highest complexity | unknown | unknown | several roles | reject now |

## Data and connector boundary

| Component/connector | Reads | Writes | Credential/role | Data destination | Retry/duplicate behaviour | Revoke/test owner |
|---|---|---|---|---|---|---|
| local spreadsheet filter | synthetic CSV | local review list | local user role | approved local folder | user replaces dated output only after review | support role |

Course 1 external writes: **none**. Course 1 real business-system connections:
**none**.

## Lifecycle ownership

| Responsibility | Owner role | Backup role | Procedure/evidence |
|---|---|---|---|
| Business outcome and scope | operations lead | business owner | decision record |
| Process rules and exceptions | operations lead | coordinator | versioned rule register |
| User access review | support role | operations lead | folder access list |
| Credentials and rotation | not applicable in Course 1 | support role | no credentials evidence |
| Workflow changes and testing | support role | course learner | frozen regression set |
| Model/prompt/schema updates | not applicable to selected no-AI option | reviewer | reassess before addition |
| Monitoring and exception queue | coordinator | operations lead | run checklist |
| User support and training | adoption owner | support role | task evidence |
| Vendor relationship and billing | not applicable | operations lead | no vendor/account |
| Backup and restoration test | support role | coordinator | hash-match drill |
| Incident response | operations lead | support role | stop/fallback record |
| Data retention/deletion | operations lead | support role | synthetic-folder schedule |
| Export, migration, and shutdown | support role | operations lead | CSV/manual exit test |

## Cost and exit

One-time effort is a one-hour configuration-and-test scenario. Monthly
licence/usage is EUR 0 for the local spreadsheet scenario; operating time is
measured, not promised. The data remains CSV. Replacement is the manual
approved filter. Shutdown removes the saved configuration after preserving
the evidence record; no credential revocation is needed. No vendor lock-in is
accepted.

## Decision

Selected option: configure the existing spreadsheet; retain the local Python
version only as a learning proof. No requirement rules out the spreadsheet.
Real client tools and costs remain unknown. Reassess if measured volume,
complexity, data, action, or system boundaries change. Decision: **SELECT FOR
SYNTHETIC TEST**. Decision owner/date: fictional operations lead / 2026-07-28.
