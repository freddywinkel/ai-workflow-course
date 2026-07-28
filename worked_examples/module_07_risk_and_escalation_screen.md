# Completed Example — Risk and Escalation Screen

- Artifact ID: WORKED-M07-RISK
- Version/date: 1.0 / 2026-07-28
- Author/reviewer: course learner / fictional operations lead
- Workflow/intended-purpose version: low-stock review list 1.0

This is a practical first screen, not legal, security, privacy, or regulatory
advice.
Artificial intelligence (AI) is optional software-generated assistance; it is
not used to create authoritative issues in this example.

## Course 1 stop screen

| Question | Yes/No/Unknown | Evidence | Escalation role |
|---|:---:|---|---|
| Real personal, confidential, or special-category data? | No | only synthetic item ID, quantity, and threshold | process owner if scope changes |
| Material effect on a person's rights, care, work, money, access, or opportunity? | No | internal stock-attention list only | process owner |
| Medical, safety-critical, legal, financial, or regulated purpose? | No | fictional office-supply stock check | qualified specialist if purpose changes |
| Automatic send, pay, purchase, sign, delete, publish, grant access, or write-back? | No | local draft only; external actions disabled | operations lead |
| Data destination, retention, training use, or support access unresolved? | No | approved local practice folder; delete after course | support role |
| Process, data, system, or decision owner missing? | No | fictional roles recorded below | operations lead |
| Meaningful review or manual fallback unavailable? | No | operations lead review and spreadsheet filter | operations lead |
| Failure hard to detect or reverse? | No | named failure state; source unchanged; manual filter | support role |

Course path after screen: **CONTINUE SYNTHETIC ONLY**.

## Risk register

| ID | Scenario/cause | Affected outcome | Probability | Impact | Prevent | Detect | Recover | Residual risk | Owner |
|---|---|---|:---:|:---:|---|---|---|---|---|
| RK-001 | missing or wrong header | rules cannot read input | medium | medium | fixed header contract | startup validation | stop and use manual filter | low | support role |
| RK-002 | duplicate or stale row | repeated/old issue | medium | medium | ID/date checks | reason-coded issue | reviewer rejects; correct input | low | process owner |
| RK-003 | unsupported summary | misleading explanation | medium | high | issue IDs only | schema and support check | rule-only fallback | low | reviewer |
| RK-004 | untrusted text resembles an instruction | workflow diversion | low | high | input is treated as data | unknown-ID/content checks | refuse summary; rule report remains | low | support role |
| RK-005 | unauthorised access | data exposure | low | medium | scoped local folder | access review | revoke access; preserve evidence | low in synthetic test | support role |
| RK-006 | timeout or partial completion | missing output | medium | medium | named states | non-zero failure and audit event | rerun after correction; manual fallback | low | operator |
| RK-007 | reviewer automation bias | bad draft accepted | medium | high | source links and reject option | approval record | invalidate approval and retest | medium | operations lead |
| RK-008 | user workaround/non-adoption | control bypass | medium | medium | task-based training | UAT observation | improve design or stop | medium | adoption owner |
| RK-009 | unowned bill, credential, or update | cost/security drift | low | high | no account or secret in Course 1 | dependency and scope checks | disable path; assign owner later | low | support role |
| RK-010 | restore/manual route fails | prolonged interruption | low | high | frozen files and instructions | fallback drill | restore tested copy; manual check | medium until drilled | support role |

## Escalation routes

| Trigger/reason code | Immediate safe action | Evidence to preserve | Decision role | Response target | Resume criteria |
|---|---|---|---|---|---|
| INPUT_INVALID | stop; do not guess | input hash, error, time | process owner | before next run | corrected synthetic input passes |
| SUMMARY_INVALID | use rule-only output | issue file and rejected draft | reviewer | same practice session | support check passes |
| APPROVAL_INVALID | block export | draft hash and approval event | operations lead | before export | exact current draft approved |
| SCOPE_CHANGE | stop new path | request and current boundary | operations lead/specialist | before design | separate assessment completed |

## Pause and kill controls

New runs pause by stopping the local command. `EXTERNAL_ACTIONS_ENABLED=false`
blocks every send, payment, deletion, source update, and live integration.
Deterministic local review and the manual CSV check remain available. The
stopped state is verified by a named failure and no approved export. Only the
fictional operations lead may approve resumption after a passing retest. The
operations coordinator owns the manual fallback in the local course runbook.

## Decision

Accepted for the synthetic demonstration: reversible local processing,
rule-only fallback, and bounded mock summary. Blocked later: real data,
external connections/actions, consequential use, and unowned services.
Specialist review is required before any such scope change. Next control:
execute every supplied failure fixture. Decision: **CONTINUE SYNTHETIC TEST**.
Decision owner/date: fictional operations lead / 2026-07-28.
