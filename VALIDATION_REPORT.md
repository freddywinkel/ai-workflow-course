# Course 1 Package Validation Report

Course: **Controlled Artificial Intelligence (AI) Workflow Foundations**

Course version: `2.1.0`

Curriculum verified through: `2026-07-26`

Result: **PASS**

Checks: 27; failures: 0; warnings: 0

## Scope

This report covers the current curriculum manifest, configured lesson files,
the 9 foundation and 9 module progress lessons, module structure, current
JSON contracts, synthetic practice data, and current internal links.
`future_courses/`, `app/dist/`, dependency folders, Git metadata, caches, and
external websites are outside this deterministic validation.

| Status | Check | Detail |
|---|---|---|
| PASS | curriculum-load | curriculum.json parsed as a JSON object |
| PASS | curriculum-metadata | Course 1 metadata is complete through 2026-07-26 |
| PASS | curriculum-groups | 6 configured groups have stable IDs and valid structure |
| PASS | curriculum-stable-ids | 60 unique current IDs and 34 unique legacy IDs |
| PASS | curriculum-documents | 60 unique configured lesson paths and revisions are valid |
| PASS | curriculum-core-groups | only foundations and modules are configured as progress groups |
| PASS | career-metadata | 6 ordered career courses; Course 1 is the only current course |
| PASS | progress-foundations | exactly 9 ordered foundation progress lessons |
| PASS | progress-modules | exactly 9 ordered module progress lessons |
| PASS | progress-total | 18 progress lessons: 9 foundations plus 9 modules |
| PASS | module-structure | all 9 modules use the 12 required headings in order |
| PASS | beginner-practice-structure | all 18 progress lessons use the ordered follow, recreate, inspect, and pass loop |
| PASS | beginner-practice-codex-check | all 18 progress lessons include bounded read-only Codex inspection prompts |
| PASS | beginner-practice-pass-criteria | all 18 progress lessons include objective pass checklists |
| PASS | beginner-first-use-terms | 18 required first-use expansions and product explanations are present in onboarding |
| PASS | current-json-syntax | 8 in-scope JSON files parsed |
| PASS | schema-set | 5 current schema files include all required Course 1 contracts |
| PASS | schema-structure | 5 schemas have unique IDs and closed object contracts |
| PASS | schema-meta-validation | jsonschema accepted all 5 schemas as Draft 2020-12 |
| PASS | yaml-parse | stack-manifest.yaml parsed as a mapping |
| PASS | practice-files | practice README, work_items.csv, and expected_issues.csv are present |
| PASS | practice-shape | 12 work-item columns / 15 rows and 6 issue columns / 13 rows |
| PASS | practice-unique-keys | work-item IDs, issue IDs, and expected comparison keys are unique and referentially valid |
| PASS | practice-rule-register | R001-R011 are documented and covered using fixed date 2026-07-26 |
| PASS | practice-synthetic-safety | fixed fictional identifiers, role-only ownership, no personal-data columns, and explicit no-real-data guarantees |
| PASS | practice-rule-oracle | standard-library evaluator reproduces all 13 frozen issues, including both R010 duplicates and fixed-date R011 |
| PASS | internal-links | 50 current local targets exist; 0 archived/generated targets ignored |

## Limits

A PASS confirms deterministic package structure; it does not confirm external
source currency, legal compliance, production security, model quality, visual
layout, accessibility, or a learner's implementation. Those require the live
source audit, PWA tests and visual review, and the course evaluation and UAT
gates.
