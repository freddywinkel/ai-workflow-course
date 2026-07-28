# Course 1 Requirement-to-Practice Map

## Why this page exists

Nothing in the final Course 1 assessment should surprise you. This page shows
where each capability is first explained, where you follow a completed
example, where you recreate it with different synthetic material, and what
proves that it passed.

There are two related things:

1. `course1_capstone` is the supplied **working reference**. It lets you inspect
   and run a complete safe workflow without first inventing hundreds of lines
   of code.
2. Your learner project at
   `Documents\AI-workflow-learning\operations-exception-assistant` is **your
   recreation and evidence package**. Modules 4–6 copy the reference safely,
   make you run its parts, use different synthetic data, create a different
   summary, perform every human decision, and prove the controls.

You are not expected to build the complete program from a blank screen. Course
1 teaches you to understand, configure, test, challenge, explain, and hand over
a controlled implementation. Later courses add deeper independent engineering.

## Learning and evidence map

| Capability | First explained and demonstrated | Your different recreation | Passing evidence |
|---|---|---|---|
| Safe computer and project setup | Windows Setup | create your one local learner repository | preflight, two smoke tests, pinned dependency record, setup Git checkpoint |
| Observe real work without tool-first guessing | Module 1 | map the different 15-row fictional process | observation, stakeholder map, baseline, read-only Codex pass |
| Select or stop a worthwhile opportunity | Module 2 | score three different fictional candidates | one nine-factor 0–3 scorecard, hard-stop result, intended purpose |
| Define data and deterministic rules | Module 3 | predict all 13 frozen issue triples | dictionary, rule register, expected result, source hashes |
| Validate input and run deterministic checks | Module 4 Stages 1–5 | run a different six-row fixture with five expected issues | reference runner copied and verified by SHA-256 before execution; exact 13/13 and 5/5 issue triples; schemas and source links |
| Make retries and failures visible | Module 4 Stages 6–7 | predict, run, preserve, and correct a different attempt | duplicate retry; path-neutral missing-file, duplicate-ID, malformed-input, and header safe stops; every repeated attempt preserved; last valid workflow state kept separate from `failed_manual` attempt evidence even when state/audit JSON is damaged |
| Design a bounded, replaceable future AI contribution and test it without a live provider | Module 5 Stages 1–3 | select the alternate controlled headline for the different five-issue offline mock and validate the complete structure | known issue IDs only; trusted code renders group/action wording; sentence-level human support review; no live model call |
| Keep working when AI fails or is unsafe | Module 5 Stages 4–5 | validate the different mock and fallback | disabled, timeout, refusal, malformed JSON, unknown ID, and untrusted-text tests |
| Make approval meaningful | Module 6 Stages 1–4 | edit revision 1, review revision 2, then approve it | exact revision and protected-manifest hash; source, JSON/CSV issues, summary, control, configuration, and review package bound; all decision fields locally fingerprinted; completed evidence check; atomic logical export pair |
| Prove non-approval paths | Module 6 failure lab and recreation | separately edit, reject, and expire | no export after missing evidence, stale revision, edit, reject, or expiry |
| Prove no external action exists | Module 6 external-action drill | inspect the different run's control and audit | `EXTERNAL_ACTIONS_ENABLED=false`, tamper safe-stop, `external_actions=0` |
| Choose a proportionate tool and owners | Module 7 | complete different risk and tool-fit worksheets | scope-change stop, manual fallback, lifecycle roles, exit plan |
| Evaluate quality before value | Module 8 | copy the actual runner-generated 13-issue file, score it, and complete the decision form | precision/recall, support rate, scenarios not forecasts, one evidence-backed `PROVISIONAL PRE-UAT` recommendation |
| Test operation and handover | Module 9 | execute UAT-01 through UAT-09 in separate workspaces using neutral relative run locators, reject/correct/retest UAT-D01 in its own workspace, and complete adoption/handover | exact path-neutral command evidence, Given/When/Then UAT record, current-state/attempt-state distinction, defect/retest trail, adoption plan, runbook, owners |
| Finalise the workflow decision | Module 9 | preserve the Module 8 recommendation, add UAT/defect/adoption/handover evidence, and reassess it | `FINAL POST-UAT`, exactly one supported final label, matching accept/rework/closure path |
| Demonstrate Course 1 competence | Module 9 using Assessment and Rubric | follow the completed example, recreate all prerequisites/six scores/ten oral answers, verify arithmetic, then request a bounded read-only Codex check | every prerequisite passes, all six areas at least Competent, total at least 75, all ten answers spoken without reading generated text, Codex PASS |

## Executable failure map

The full automated command appears in Module 6. Its source-to-test mapping is
also in `course1_capstone/tests/SCENARIO_MATRIX.md`.

| Required scenario | Taught hands-on | Automated evidence |
|---|---|---|
| valid row with no issue | Module 4 | `no_action_needed`, no false success |
| missing required value, invalid status, contradictory dates, overdue work, duplicate reference | Modules 3–4 | correct deterministic issue triple |
| duplicate work-item ID | Module 4 | safe stop before rule output |
| required review without evidence | Module 6 | approval/export blocked |
| stale revision | Module 6 | decision blocked |
| malformed input, missing file, unexpected header | Module 4 | visible safe stop |
| duplicate retry/export retry | Modules 4 and 6 | one run and one logical local effect |
| simultaneous operation on one workspace/run | Module 6 automated suite | exclusive lock safely stops the second process; no duplicate or partial effect |
| AI disabled, timeout, refusal, malformed JSON, unknown issue ID | Module 5 | deterministic fallback remains usable |
| untrusted instructions in source text | Module 5 | text remains inert and absent from summary |
| dangerous free-text review instruction with `external_action=false` | Modules 5–6 automated suite | fixed safe instruction template rejects the candidate |
| edited approved draft | Module 6 | old approval invalid |
| schema-valid issue, review package, run configuration, or manifest edited after approval | Module 6 automated suite | recomputed protected evidence blocks export |
| reviewer, reason, or expiry edited in saved decision | Module 6 automated suite | recomputed decision ID blocks export |
| CSV formula prefix, including after whitespace/control | Module 6 automated suite | spreadsheet-safe CSV; exact JSON/source evidence |
| conflicting half-export or second-file promotion failure | Module 6 automated suite | no newly published lone approved artifact |
| edit, reject, and expire decisions | Module 6 | named non-export states |
| external-action control false or tampered | Module 6 | zero external actions; tampering blocks export |
| forged “evidence reviewed” value | Module 6 automated suite | export blocked |
| actual generated JSON contracts | Module 6 automated suite | work items, issues, summary, run configuration, control, state, review package, review manifest, approval, evaluation, and audit events validate |

## What passing does and does not mean

Passing proves that you can reason through and operate one controlled,
synthetic, local workflow foundation. It does not prove client demand,
production readiness, real-user adoption, legal compliance, security
assurance, or the ability to implement any arbitrary platform. Those are
separate later-course and real-engagement gates.

The rubric task is integrated into Module 9, so the required learning sequence
remains 21 pages. `ASSESSMENT_AND_RUBRIC.md` and the completed assessment
example are supporting references, not extra completion pages.
