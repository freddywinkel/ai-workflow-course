# Assessment Gates and Final Rubric

## Gate policy

Every week has a pass/fail gate in its module. A later week may be studied after a failure, but the capstone cannot be released until all prerequisite gates are passed with observed evidence.

These conditions are absolute:

- no real/sensitive/prohibited data;
- no unnamed run state;
- no unsupported factual claim presented as supported;
- no cross-tenant evidence/access;
- no action without exact valid approval;
- no duplicate final action;
- no supplier recommendation/selection;
- no send/payment/binding action;
- no secret in repository/workflow export/evidence;
- every declared failure has a visible safe route.

An absolute failure cannot be averaged away by a high score.

## Weekly gate register

| Week | Gate evidence | Pass recorded by |
|---:|---|---|
| 1 | purpose, exclusions, process, baseline, state tabletop | |
| 2 | API/orchestration/retry/idempotency tests | |
| 3 | hash/storage/state/RLS/partial-write tests | |
| 4 | PDF/DOCX/table/scan/corrupt provenance tests | |
| 5 | schema/refusal/null/evidence/semantic/model benchmark | |
| 6 | retrieval/evidence-ledger/memo grounding tests | |
| 7 | approve/edit/reject/expire/hash/idempotency tests | |
| 8 | boundary/role/DPIA/vendor/retention/literacy evidence | |
| 9 | threat/failure/tenant/log/kill-switch/restore tests | |
| 10 | frozen JSONL regression and metric report | |
| 11 | connector/provider/timing/hardening report | |
| 12 | frozen release, clean reproduction, deletion and acceptance | |

## Final scoring rubric

Minimum overall score: 80/100 **and** every mandatory condition.

### 1. Source integrity and provenance — 20 points

| Evidence | Points |
|---|---:|
| exact received bytes hashed, immutable, private, and manifest-linked | 5 |
| raw/derived separation and versioned parser/canonicalisation | 4 |
| page/region/span locators plus supporting-text hashes | 5 |
| provenance persists through extraction/memo and survives restore | 4 |
| duplicates/corrupt/partial writes handled correctly | 2 |

Zero for this section if originals can be overwritten or evidence can point across tenants.

### 2. Extraction and deterministic validation — 15 points

| Evidence | Points |
|---|---:|
| strict portable schemas, nullable/missing/conflict semantics | 3 |
| Responses/provider adapter and full version tuple | 3 |
| independent decimal/date/policy validation | 4 |
| ≥90% required-field accuracy with per-field report | 3 |
| refusals/incomplete/schema/semantic failures routed safely | 2 |

### 3. Grounded drafting and citations — 15 points

| Evidence | Points |
|---|---:|
| measured retrieval and active policy version | 3 |
| verified evidence ledger, including derived calculations | 4 |
| proposition-level memo contract | 3 |
| ≥95% locator correctness | 3 |
| 100% factual assertions supported or visibly unsupported; no forbidden claim | 2 |

### 4. Human approval and action safety — 15 points

| Evidence | Points |
|---|---:|
| usable review of source/evidence/uncertainty/action | 3 |
| exact canonical output hash and edit invalidation | 4 |
| approve/reject/expire/rework lifecycle | 3 |
| C018 two distinct reviewers | 2 |
| idempotent draft-only action, time-of-use recheck, kill switch | 3 |

Zero for this section and fail release if any action occurs without a valid exact-output approval.

### 5. Privacy, legal-status, security, and failures — 15 points

| Evidence | Points |
|---|---:|
| fictional-data boundary and excluded-use/medical gates | 3 |
| AVG/AI Act roles, DPIA screen, vendor/transfer/status distinctions | 3 |
| retention/rights/deletion across all layers | 3 |
| threat model, injection/tenant/secrets controls | 3 |
| outage/dead-letter/manual route, observability, restore | 3 |

This score is engineering literacy, not a legal-compliance certificate.

### 6. Evaluation quality — 10 points

| Evidence | Points |
|---|---:|
| frozen 20-case manifest/gold with reviewed hashes | 2 |
| vendor-neutral local runner and offline deterministic suite | 3 |
| exact metrics, exclusions, per-case/field results | 2 |
| adversarial/mutation/failure tests | 2 |
| non-zero release-gate exit and retained reports | 1 |

### 7. Reproducibility, runbook, and demonstration — 10 points

| Evidence | Points |
|---|---:|
| full stack/config/version/release manifest | 2 |
| clean-start C001 reproduction | 3 |
| runbook/manual fallback/deletion/restoration | 2 |
| matched median hands-on improvement ≥30%, quality not reduced | 2 |
| evidence-backed demo and honest limitations | 1 |

## Evidence quality levels

| Level | Description |
|---|---|
| 0 | assertion only; no artifact |
| 1 | screenshot/narrative without reproducible procedure |
| 2 | stored artifact plus manual verification |
| 3 | automated repeatable check with versioned input/output |
| 4 | independent/fresh-environment reproduction plus negative test |

Prefer Level 3–4 for release-blocking controls.

## Final assessor form

Release:  
Commit/tag:  
Evaluation report/hash:  
Source register verified date:  
Clean-start reproducer/date:  

| Section | Maximum | Awarded | Blocking issue |
|---|---:|---:|---|
| source integrity/provenance | 20 | | |
| extraction/validation | 15 | | |
| grounded drafting | 15 | | |
| approval/action | 15 | | |
| privacy/security/failures | 15 | | |
| evaluation | 10 | | |
| reproduction/handover | 10 | | |
| **Total** | **100** | | |

Mandatory conditions all pass: yes / no  
Decision: RELEASE PRIVATE DEMO / DO NOT RELEASE  
Known limitations accepted for synthetic demo:  
Assessor/date:  

