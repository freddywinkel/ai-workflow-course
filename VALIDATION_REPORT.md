# Package Validation Report

Course root: repository root (`.`)  
Result: **PASS**  
Checks: 16; failures: 0; warnings: 0

| Status | Check | Detail |
|---|---|---|
| PASS | required-files | 34 required files present |
| PASS | week-count-and-names | exactly WEEK_01.md through WEEK_12.md |
| PASS | week-structure | all nine required headings appear in order |
| PASS | json-parse | 46 JSON files parsed |
| PASS | jsonl-parse | 2 JSONL files / 40 rows parsed |
| PASS | yaml-parse | stack-manifest.yaml parsed |
| PASS | json-schema-meta-validation | both schemas valid under Draft 2020-12 |
| PASS | golden-schema-validation | 20 golden rows validate against the course schema |
| PASS | internal-links | 137 local targets exist |
| PASS | corpus-case-set | 20 ordered unique cases agree |
| PASS | corpus-states | all manifest/gold checkpoint states are named states |
| PASS | corpus-file-integrity | 59 referenced files match metadata |
| PASS | corpus-C009-duplicate | quotation and terms are byte-identical to C001 |
| PASS | corpus-C010-corrupt | exact specified corrupt bytes |
| PASS | corpus-safety-flags | all cases carry strict synthetic/no-data flags |
| PASS | corpus-checksum-file | 84 checksum entries verified |

This is deterministic structural validation only. External-source currency and visual quality require the live audit and render review.
