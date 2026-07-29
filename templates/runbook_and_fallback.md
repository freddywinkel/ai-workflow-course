# Runbook and Manual Fallback

System/release:  
Owner/on-call placeholder:  
Last drill/date:  
Kill-switch location:  

## Normal operation

Start/stop:  
Health checks:  
Expected state/latency:  
Daily/weekly checks:  
Credential rotation:  
Source/model/dependency update process:  

## Reason-code playbook

| Reason/state | Diagnose | Safe immediate action | Retry/reconcile | Manual owner | Evidence to retain |
|---|---|---|---|---|---|
| | | | | | |

## Safe-stop controls

Activation:  
What it blocks:  
What remains available:  
Verification:  
Re-enable authority/criteria:  

## Manual fallback Standard Operating Procedure (SOP)

1. Stop new model/action calls.
2. Preserve and re-hash originals.
3. Export a minimal manual work packet.
4. Complete the manual extraction/calculation/memo template.
5. Independently review source evidence.
6. Record manual decision and exact output.
7. Do not infer/backfill system approval.
8. Reconcile run/audit state before resuming.

Manual packet contents and redaction:  

## Backup/restore

Database:  
Object storage:  
n8n volume/workflows/encryption key:  
Git/prompts/schemas:  
Restore order and hash verification:  
Recovery Time Objective (RTO) / Recovery Point Objective (RPO) observed:

## Incident

Detect → contain → revoke/isolate → preserve → assess → notify owner → recover → verify → learn  
Personal-data breach decision owner and template:  
