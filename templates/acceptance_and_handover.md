# Acceptance and Handover Checklist

Release/version/commit:  
Date/owner/reviewer/reproducer:  
Source-register verified:  
Release-manifest hash:  

## Frozen inputs

- [ ] exact dependency lock/Python
- [ ] n8n image tag or digest/workflow hash
- [ ] parser/OCR/model-cache versions
- [ ] model IDs/snapshots/settings
- [ ] prompt/schema/canonicalisation hashes
- [ ] SQL migrations/policy version
- [ ] corpus manifest/gold hashes
- [ ] action mode draft-only; kill switch defaults on
- [ ] secrets scan clean

## Acceptance

| Gate | Threshold | Observed | Report/hash | Pass? |
|---|---:|---:|---|:---:|
| named-state closure | 100% | | | |
| schema-valid or explicit failure | 100% | | | |
| required-field accuracy | ≥90% | | | |
| locator correctness | ≥95% | | | |
| memo supported/labelled | 100% | | | |
| unauthorised final/external actions | 0 | | | |
| duplicate actions | 0 | | | |
| declared safe fallbacks | 100% | | | |
| matched hands-on improvement | ≥30% | | | |
| clean reproduction | 1 complete run | | | |

## Drills

- [ ] approve/edit/reject/expire
- [ ] one-byte mutation invalidates approval
- [ ] C018 two distinct approvals
- [ ] injection/corrupt/duplicate/arithmetic conflict
- [ ] tenant isolation
- [ ] parser/model/storage/audit outage
- [ ] kill switch/manual packet
- [ ] backup restoration/hash match/no action replay
- [ ] deletion across source/derived/index/cache/log/audit/provider

## Handover

- [ ] README/setup
- [ ] architecture/contracts/state
- [ ] runbook/fallback
- [ ] threat model/residual risk
- [ ] data/retention/deletion map
- [ ] source/version snapshot
- [ ] limitations
- [ ] demo script
- [ ] artifact hashes

Known blockers/limitations:  
Decision: RELEASE / DO NOT RELEASE  
Sign-off/date:  

