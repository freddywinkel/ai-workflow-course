# Threat Model

System/intended-purpose version:  
Date/owner/reviewer:  
Diagram/version:  
Method: scenario-based / STRIDE / other  

## Assets and trust boundaries

| Asset | Confidentiality | Integrity | Availability | Owner | Backup/deletion |
|---|---:|---:|---:|---|---|
| | | | | | |

Trust boundaries and assumptions:  
Actors (authorised, mistaken, malicious, dependency, operator):  

## Threat register

| ID | Threat/path | Preconditions | Impact | Prevent | Detect | Recover | Test | Residual risk/owner |
|---|---|---|---|---|---|---|---|---|
| T-001 | | | | | | | | |

Required scenarios:

- document prompt injection;
- hostile/malformed/oversized/password-protected file;
- arbitrary URL/SSRF;
- cross-tenant access;
- secret/log/workflow-export leak;
- provider/parser/storage/database outage;
- partial write;
- duplicate/replay;
- approval replay or changed output;
- retrieval poisoning/wrong policy;
- observability content leak;
- operator compromise;
- backup/restore failure;
- vendor incident.

## Incident controls

Safe-stop control location/test:
Manual fallback:  
Credential rotation/revocation:  
Evidence preservation:  
Personal-data-breach decision owner:  
Residual risks accepted by:  
