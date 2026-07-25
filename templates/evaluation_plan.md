# Evaluation Plan

Version/date/owner/reviewer:  
Code/corpus/gold hashes:  
Development versus frozen-test separation:  

## Claims and metrics

| Claim | Population/cases | Metric | Threshold | Zero-tolerance? | Evidence/report |
|---|---|---|---:|:---:|---|
| named state | C001–C020 | exact match | 100% | yes | |
| required fields | eligible cases/fields | micro accuracy | ≥90% | no | |
| locators | required locators | correctness | ≥95% | no | |
| memo facts | all propositions | verified or labelled | 100% | yes | |
| approval/action | lifecycle tests | invariant pass | 100% | yes | |
| hands-on time | matched cases | median improvement | ≥30% | no | |

Define numerator/denominator and exclusions:  
Intentional-null rule:  
Normalisation/rounding:  
Human-scoring rubric:  

## Suites

| Suite | Network? | Fixtures | Command | Release-blocking? |
|---|:---:|---|---|:---:|
| unit | no | | | yes |
| parser | no | | | yes |
| provider-contract | no | | | yes |
| cached regression | no | | | yes |
| live regression | yes | | | yes |
| security | mixed | | | yes |
| acceptance | mixed | | | yes |

## Change triggers

- [ ] model/snapshot/reasoning
- [ ] prompt/schema
- [ ] parser/OCR/canonicalisation
- [ ] retrieval/embedding/policy
- [ ] calculation/domain rule
- [ ] approval/action
- [ ] dependency/infrastructure

Failure triage and gold-change process:  

