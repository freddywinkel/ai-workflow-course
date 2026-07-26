# Acceptance and Handover Checklist

Release/version/commit:  
Date/owner/reviewer/reproducer:  
Source-register verified:  
Release-manifest hash:  

## Frozen inputs

- [ ] exact dependency lock/Python
- [ ] workflow definition or script hash
- [ ] input and expected-result hashes
- [ ] model IDs/snapshots/settings
- [ ] prompt/schema/canonicalisation hashes
- [ ] storage and retention configuration
- [ ] action mode draft-only; kill switch defaults on
- [ ] secrets scan clean

## Acceptance

| Gate | Threshold | Observed | Report/hash | Pass? |
|---|---:|---:|---|:---:|
| named-state closure | 100% | | | |
| schema-valid or explicit failure | 100% | | | |
| deterministic issue precision/recall | 100% | | | |
| AI claims linked to verified issue IDs | 100% | | | |
| unsupported AI claims reach a safe fallback | 100% | | | |
| unauthorised final/external actions | 0 | | | |
| duplicate actions | 0 | | | |
| declared safe fallbacks | 100% | | | |
| matched hands-on improvement | ≥30% | | | |
| clean reproduction | 1 complete run | | | |

## Drills

- [ ] approve/edit/reject/expire
- [ ] one-byte mutation invalidates approval
- [ ] duplicate run does not create duplicate draft
- [ ] malformed row/duplicate reference/date conflict
- [ ] untrusted text cannot change workflow instructions
- [ ] model/storage/audit outage
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
