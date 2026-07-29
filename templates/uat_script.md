# Role-Simulated Operational Acceptance Rehearsal and Candidate User Acceptance Test Record

**User Acceptance Testing (UAT)** means another consenting intended user
performs realistic synthetic tasks. A learner working alone may complete this
as a role-simulated operational acceptance rehearsal but must retain
`EXTERNAL UAT NOT VERIFIED`.

Artifact ID:
Version/date:
Author:
Rehearsal lead:
Evidence status: ROLE-SIMULATED OPERATIONAL ACCEPTANCE REHEARSAL / REAL SYNTHETIC UAT
External-user status: EXTERNAL UAT NOT VERIFIED / REAL SYNTHETIC UAT: VERIFIED
Workflow/release:
Intended-purpose version:
Test environment: SYNTHETIC / [stop if not approved]
Test dataset/version:
Module 8 recommendation/status: [one label] / PROVISIONAL PRE-UAT

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

## Technical regression scenario record

Copy this section for each solo technical scenario.

Use exactly `TECH-01` through `TECH-09`. These identifiers are technical
regression evidence, not User Acceptance Testing.

### TECH-[NN] — [Technical scenario name]

Requirement/acceptance criterion:
Tester role:
**Given** — preconditions and synthetic input case IDs:
**When** — exact user/system action:
**Then** — expected final state or reason code and exact relative evidence path:

| Step | Exact action | Expected relative evidence | Observed result | Pass? |
|---:|---|---|---|:---:|
| 1 | | | | |

Source unchanged?
Audit/issue records present?
Usability/accessibility observation:
Defect or follow-up ID:
Tester decision/date: PASS / FAIL / BLOCKED

## Candidate intended-user task record

Prepare these tasks, but do not mark them executed during solo rehearsal.
`UAT` means User Acceptance Testing and is reserved here for another consenting
intended user. Copy this section for each candidate task.

### Required participant briefing — complete before consent

Briefing version/date:
Purpose and predefined synthetic tasks:
Expected total time:
Voluntary choice explained: the person may pause, skip a task, or stop at any
time without giving a reason or suffering a consequence.
Exact observations proposed: completion, elapsed time, errors, help requested,
comments, facilitator interventions, defects, corrections, and retest.
Who may access the structured record:
Planned retention/deletion date:
Temporary observation-note deletion date:
Boundary explained: participation is not employment, medical, or professional
evaluation and is not production or real-data evidence.
Data-minimisation rule explained: use only supplied fictional data and a
non-identifying participant code; do not collect a name, employer, health
information, credentials, client information, or unnecessary personal data.
Questions answered:
Participant explained back the voluntary-stop and recording choices: YES / NO

### Separate consent choices

Participation consent: YES / NO
Screen recording proposed: NO / YES — separate consent: NOT PROPOSED / YES / NO
Audio recording proposed: NO / YES — separate consent: NOT PROPOSED / YES / NO
Video recording proposed: NO / YES — separate consent: NOT PROPOSED / YES / NO
Quotation proposed: NO / YES — separate consent: NOT PROPOSED / YES / NO

If participation consent is `NO`, stop and create no UAT result. A `NO` to any
optional recording still allows unrecorded participation. Missing consent,
prohibited data, an undisclosed observation, or recording without separate
consent invalidates the evidence: stop, do not copy it into the repository,
and ask for safe handling guidance.

### UAT-[NN] — [Intended-user task name]

Predefined task:
Observable success criteria:
Synthetic starting data:
Participant code:
Briefing version:
Participation consent recorded before testing: YES / NO
Separate recording/quotation choices:
Evidence access roles:
Retention/deletion date:
Intended role:
Prior experience with the represented process:
Start and end time or elapsed minutes:
Completed: YES / NO / PARTIAL
Errors observed:
Help requested:
Participant comments:
Facilitator interventions:
Evidence path:
Defect/correction/retest:
Synthetic limitation: this task uses fictional data and does not establish
production usability, real-data performance, client acceptance, or employment,
medical, or professional evaluation.

Until another person actually completes the task, record:
`NOT EXECUTED — EXTERNAL UAT NOT VERIFIED`.

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

## Rehearsal or UAT result

Scenarios passed/failed/blocked:
Open high-severity defects:
User groups not represented:
Requirements not tested:
Workarounds or burden introduced:
Effect of rehearsal or real UAT and defects/retests on the provisional recommendation:
Workflow decision: ACCEPT FOR SYNTHETIC PORTFOLIO / REWORK / DO NOT CONTINUE
Decision stage/status: FINAL POST-REHEARSAL / FINAL POST-UAT
Evidence rule: use FINAL POST-UAT only with another consenting intended user and a separate real synthetic UAT record
Rehearsal or UAT lead/date:
Process-owner review/date:
