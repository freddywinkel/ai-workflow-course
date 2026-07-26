# Evaluation Plan

Version/date/owner/reviewer:  
Code/input/expected-result hashes: [record here]
Development versus frozen-test separation:  

## Claims and metrics

| Claim | Population/cases | Metric | Threshold | Zero-tolerance? | Evidence/report |
|---|---|---|---:|:---:|---|
| deterministic issues | frozen work-item rows | precision and recall | 100% | yes | |
| stable issue identity | repeat runs | exact match | 100% | yes | |
| AI-supported claims | all summary claims | linked to verified issue ID or rejected | 100% | yes | |
| schema-valid summary | all AI attempts | valid or explicit fallback | 100% | yes | |
| approval/action | lifecycle tests | invariant pass | 100% | yes | |
| hands-on time | matched synthetic runs | observed difference | report, no forecast | no | |

Define numerator/denominator and exclusions:  
Intentional-null rule:  
Normalisation/rounding:  
Human-scoring rubric:  

## Suites

| Suite | Network? | Fixtures | Command | Release-blocking? |
|---|:---:|---|---|:---:|
| unit | no | | | yes |
| data and rule | no | | | yes |
| provider-contract | no | | | yes |
| cached regression | no | | | yes |
| optional live-provider | yes | | | conditional |
| control lifecycle | no | | | yes |
| UAT | no | | | yes |

## Change triggers

- [ ] model/snapshot/reasoning
- [ ] prompt/schema
- [ ] input schema/normalisation
- [ ] deterministic rule/expected-result register
- [ ] calculation/domain rule
- [ ] approval/action
- [ ] dependency/infrastructure

Failure triage and expected-result change process: [record here]
