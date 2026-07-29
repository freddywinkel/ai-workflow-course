# Reusable Worksheets and Checklists

Copy a template into your learner or engagement folder before completing it.
Keep the blank original. Course 1 uses only the supplied synthetic data and
does not connect to employer or customer systems.

These templates are not standalone practice tasks. The matching module first
shows a completed fictional example, then tells you which blank template to
copy for your independent recreation and supplies the read-only Codex check.
Do not fill a template by guessing before reaching that lesson.

Terms used below: **artificial intelligence (AI)** and **user acceptance
testing (UAT)**.

## Course 1 — required consulting records

These nine records form a small, coherent engagement trail. The modules call
out the exact record where it is first needed; the first four mappings are:

- Module 1: stakeholder/user map and baseline/value record;
- Module 2: workflow opportunity scorecard;
- Module 3: data dictionary and quality check;
- Module 4: architecture decision and diagrams.

| Module first used | Template | Purpose |
|---:|---|---|
| 1 | [`stakeholder_and_user_map.md`](stakeholder_and_user_map.md) | identify users, owners, authority, needs, and adoption risks |
| 1 | [`baseline_and_value_record.md`](baseline_and_value_record.md) | define the manual baseline, value hypothesis, and honest measures |
| 2 | [`workflow_opportunity_scorecard.md`](workflow_opportunity_scorecard.md) | select a bounded problem using evidence and stop conditions |
| 3 | [`data_dictionary_and_quality_check.md`](data_dictionary_and_quality_check.md) | define fields, source, quality rules, provenance, and input acceptance |
| 7 | [`risk_and_escalation_screen.md`](risk_and_escalation_screen.md) | screen unsafe scope and assign risk, pause, fallback, and escalation routes |
| 7 | [`tool_fit_and_ownership_record.md`](tool_fit_and_ownership_record.md) | compare the simplest tool options and assign lifecycle ownership |
| 9 | [`uat_script.md`](uat_script.md) | let representative users test business scenarios and exception routes |
| 9 | [`adoption_and_training_plan.md`](adoption_and_training_plan.md) | prepare users, support, training, feedback, and adoption measures |
| 8 and 9 | [Course 1 decision record](pilot_decision_record.md) | record the Module 8 `PROVISIONAL PRE-UAT` recommendation, then preserve and reassess it as `FINAL POST-REHEARSAL`; use `FINAL POST-UAT` only with separate real synthetic UAT evidence; neither authorizes a client pilot |

The sequence is logical, not rigid. Revisit earlier records when evidence
changes the process, data, risk, or value hypothesis.

## Course 1 — supporting records

Use these existing templates when relevant:

| Template | Use |
|---|---|
| [`ai_assistance_log.md`](ai_assistance_log.md) | every material AI-assisted implementation change |
| [`debugging_record.md`](debugging_record.md) | an unresolved command, build, import, or test failure |
| [`weekly_evidence_record.md`](weekly_evidence_record.md) | optional module progress and gate evidence |
| [`architecture_decision_record.md`](architecture_decision_record.md) | a material technical decision with alternatives and consequences |
| [`acceptance_and_handover.md`](acceptance_and_handover.md) | Module 9 Course 1 closeout, ownership, recovery, limitations, and evidence index; it is not production acceptance |

## Advanced follow-on templates

The templates below are retained for later courses or more demanding
implementations. They are **not Course 1 completion requirements** and should
not be used to imply production, legal, privacy, security, or regulatory
readiness.

| Template | Advanced use |
|---|---|
| [`process_and_purpose_worksheet.md`](process_and_purpose_worksheet.md) | detailed intended-purpose, allocation, and manual-baseline analysis |
| [`data_flow_avg_ai_act.md`](data_flow_avg_ai_act.md) | structured privacy and AI Act role screen with specialist input |
| [`vendor_and_transfer_review.md`](vendor_and_transfer_review.md) | vendor, contract, processing-location, and transfer diligence |
| [`approval_design_review.md`](approval_design_review.md) | exact-output approval and action lifecycle |
| [`threat_model.md`](threat_model.md) | deeper technical threat and incident analysis |
| [`evaluation_plan.md`](evaluation_plan.md) | frozen test populations, metrics, and regression gates |
| [`runbook_and_fallback.md`](runbook_and_fallback.md) | production-oriented operations, recovery, and drills |

## Completion rules

- Give each completed artifact an ID, owner, date, and version.
- Label observation, report, assumption, decision, and unresolved question.
- Link evidence for material claims.
- Use roles instead of real names in the synthetic course.
- Never include secrets, personal data, or confidential business content.
- Do not mark a box complete without observed evidence.
- Record “not tested” or “unknown” honestly.
- A Course 1 result is a synthetic portfolio demonstration, not production
  approval.
- Course 2 teaches client discovery and assessment. Course 3 teaches supervised
  pilot preparation and governance.
