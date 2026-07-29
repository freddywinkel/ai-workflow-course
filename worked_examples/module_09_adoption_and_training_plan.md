# Completed Example — Adoption and Training Plan

- Artifact ID: WORKED-M09-ADOPTION
- Version/date: 1.0 / 2026-07-28
- Author/reviewer: course learner / fictional operations lead
- Workflow/intended-purpose version: low-stock review list 1.0
- Adoption owner: fictional operations lead

User Acceptance Testing (UAT) means another consenting intended user tries
realistic work scenarios. The learner-only example is a role-simulated
operational acceptance rehearsal and remains `EXTERNAL UAT NOT VERIFIED`.
Artificial intelligence (AI) means the optional generated assistance whose
limitations must still be taught even when the selected worked solution uses
no AI.

## What changes for people

| Group | Current work | New/changed work | Benefit to test | Burden/concern | Involvement before decision |
|---|---|---|---|---|---|
| inventory coordinator | manually filter every row | run checked list, trace issues, request review | less repeated scanning | more state/evidence checks | performs synthetic tasks |
| operations lead | reviews manually prepared list | reviews exact source-linked draft | clearer evidence | explicit approval responsibility | role-simulates rule approval and review |
| support role | helps with saved spreadsheet | owns tested version and restore | clearer recovery | new update duty | rehearses restore |

## Required behaviours

| Role | Must be able to | Must not | Evidence |
|---|---|---|---|
| operator | validate input, run, trace, stop, use fallback | guess missing values or treat draft as order | eight-task demonstration |
| reviewer | inspect source/rule, approve/edit/reject, notice expiry | approve from summary alone | exact-draft drill |
| process owner | own rules, scope, and restart | let score override stop gate | decision record |
| support/admin | restore tested version and preserve evidence | silently patch expected results | restore/hash drill |

## Training design

| Audience | Objective | Method/practice | Duration | Trainer | Completion evidence |
|---|---|---|---:|---|---|
| operator/reviewer | purpose, input check, source trace, limitations | guided example then different synthetic case | 60 min | course learner | eight observed tasks |
| process/support owners | failure, fallback, restore, update control | tabletop plus restore drill | 45 min | course learner | signed fictional checklist |

The eight tasks are: open the correct input; validate its header; run the
workflow; trace an issue; identify AI/mock wording; approve/edit/reject; use
manual fallback; report a defect. Confidentiality, safe data handling,
`EXTERNAL_ACTIONS_ENABLED=false`, and escalation are included.

## Communication and involvement

| When | Audience | Message/decision | Channel | Owner | Feedback route |
|---|---|---|---|---|---|
| Before design | coordinator/lead | problem, purpose, exclusions | synthetic workshop | lead | question log |
| Before role-simulated rehearsal | learner acting through tester roles | release, cases, stop route | written briefing | rehearsal lead | defect log |
| Before decision | all roles | observed results and limits | review | lead | decision comments |
| After decision | support/operator | accepted scope or rework | handover | adoption owner | known-issue log |
| At decision | owner | synthetic-only decision | record | operations lead | dated change request |

## Support model

First line: fictional support role. Rule questions: operations lead. Technical
incident: support role. Privacy/security scope change: qualified specialist.
Response target: before the next synthetic run. Known issues are in the module
defect log. Temporary route: manual approved spreadsheet filter. Recurring
questions become a documented instruction or design change followed by retest.

## Adoption measures

| Measure | Definition/source | Baseline | Target | Frequency | Owner |
|---|---|---:|---:|---|---|
| eligible roles trained | completed task records / eligible roles | 0/4 | 4/4 synthetic roles | before decision | adoption owner |
| eligible work routed correctly | correct state / test cases | 0% | 100% frozen cases | each change | process owner |
| workaround/rejection rate | recorded manual/reject cases | unknown | observe, no target claim | each run | reviewer |
| unresolved exception age | time until owner decision | unknown | record only | each run | operations lead |
| usability | tasks without hidden help | 0/8 | at least 7/8 | rehearsal | adoption owner |
| unsafe-action rate | unauthorised effects / attempts | 0 | 0 | every test | process owner |

## Readiness

Role-simulated users tested; materials match release; rejection, escalation,
keyboard use, zoom, support, feedback, and manual work were checked. Real user
needs remain unverified. Decision: **READY FOR SYNTHETIC EVALUATION**. Open
risk: independent user evidence absent; owner: adoption owner. Decision
owner/date: fictional operations lead / 2026-07-28.
