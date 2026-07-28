# User Acceptance Test Script

Artifact ID:
Version/date:
Author:
UAT lead:
Workflow/release:
Intended-purpose version:
Test environment: SYNTHETIC / [stop if not approved]
Test dataset/version:

## Entry criteria

- [ ] Intended purpose, scope, and exclusions are agreed.
- [ ] Representative synthetic cases and expected results are frozen.
- [ ] Rule, prompt, schema, workflow, and tool versions are recorded.
- [ ] Tester roles and decision authority are clear.
- [ ] Source files are unchanged and secrets are absent.
- [ ] Exception route, manual fallback, and
      `EXTERNAL_ACTIONS_ENABLED=false` safety control are usable.
- [ ] Known limitations are visible to testers.

If an entry criterion fails, record it; do not turn it into a passed scenario.

## Tester orientation

Tester role/group:
Normal process experience represented:
Accessibility or language support:
What the workflow is allowed to do:
What it will not do:
How to reject, report an issue, or stop:

## Scenario record

Copy this section for each scenario.

### UAT-[NNN] — [Scenario name]

Requirement/acceptance criterion:
Tester role:
Preconditions and input case IDs:

| Step | User/system action | Expected result and evidence | Observed result | Pass? |
|---:|---|---|---|:---:|
| 1 | | | | |

Expected final state/reason code:
Source unchanged?
Audit/issue records present?
Usability/accessibility observation:
Defect or follow-up ID:
Tester decision/date: PASS / FAIL / BLOCKED

## Required scenario coverage

- [ ] normal valid input;
- [ ] missing required field/column;
- [ ] invalid date, value, or state;
- [ ] duplicate input or repeated trigger;
- [ ] unsupported or contradictory AI draft;
- [ ] reviewer accepts exact output;
- [ ] reviewer edits, rejects, and escalates;
- [ ] timeout, tool outage, or partial failure;
- [ ] manual fallback;
- [ ] `EXTERNAL_ACTIONS_ENABLED=false` safety control or pause;
- [ ] unauthorised action does not occur;
- [ ] user can understand limitations and next step.

## Defect log

| ID | Scenario | Severity | Observed evidence | Owner | Fix/retest | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

## UAT result

Scenarios passed/failed/blocked:
Open high-severity defects:
User groups not represented:
Requirements not tested:
Workarounds or burden introduced:
Decision: ACCEPT FOR SYNTHETIC PORTFOLIO / REWORK / DO NOT CONTINUE
UAT lead/date:
Process-owner review/date:
