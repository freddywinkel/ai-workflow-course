# Course 1 Learning and Assessment Validation Contract

- Contract ID: `C1-LVC`
- Contract version: `1.0.0`
- Effective date: `2026-07-28`
- Scope: Course 1 only
- Course 4 and later courses: out of scope
- Strategic-fit decision: `STRATEGIC FIT: PASS`

## Purpose and authority

This is the authoritative contract for deciding what Course 1 evidence does and
does not prove about learning, assessment, beginner usability, and human use.
It complements technical package, runner, and Progressive Web App (PWA) tests.
Technical success cannot substitute for learning evidence.

The contract advances the main goal because a durable consulting path needs
capability gates that distinguish generated files, learner understanding,
independent judgment, communication, and real human use. It adds no platform,
provider, live data, paid service, or production claim.

Later repair work must map every changed learning outcome, assessment gate, and
release claim to the stable requirements below. Stable IDs must not be
renumbered or reused. Retired requirements remain recorded as retired.

This contract does not by itself:

- change a lesson, module, foundation, assessment, curriculum, PWA, or runner;
- certify the current release as beginner-validated;
- prove a learner's competence;
- authorize client work, a pilot, real data, external action, or production use.

## Evidence classes must remain separate

| Evidence class | What it can prove | What it cannot prove |
|---|---|---|
| `AUTOMATED_ARTIFACT` | required files, fields, calculations, schemas, test results, and bounded technical behavior exist | comprehension, independent judgment, oral ability, usability, or retention |
| `LEARNER_SELF_REFLECTION` | what the learner reports about confidence, effort, confusion, or having performed an action | that the reported action occurred or that the learner is competent |
| `INDEPENDENT_ARTIFACT_ASSESSMENT` | a person who did not create the work found evidence supporting defined rubric anchors | oral competence, real-user acceptance, or long-term retention |
| `INDEPENDENT_ORAL_ASSESSMENT` | the learner can explain and defend the work without supplied wording in a controlled live assessment | production readiness, client demand, or real UAT |
| `ROLE_SIMULATED_ACCEPTANCE_REHEARSAL` | the learner can rehearse operator, reviewer, and failure tasks with synthetic data | acceptance by an intended user or another person |
| `REAL_SYNTHETIC_UAT` | another consenting person completed realistic, predefined tasks using synthetic data | production usability, real-data fitness, or organisational adoption |
| `LITERAL_BEGINNER_TRIAL` | an eligible beginner could follow the tested course path under recorded conditions | that every beginner, device, or accessibility need will have the same result |
| `DELAYED_RETENTION` | the learner retained named knowledge or skills after a defined delay | indefinite retention or arbitrary-platform competence |
| `UNSEEN_TRANSFER` | the learner applied the control method to a new synthetic scenario not used in teaching | readiness for unrestricted consulting or production implementation |
| `ACCESSIBILITY_REVIEW` | the tested flows worked with the named device, browser, settings, and assistive technology | universal accessibility |

An acceptance record must name its evidence class. It must never upgrade
self-attestation, a model review, or an automated check into independent human
evidence.

## Release and learner-result language

Use only the status that the evidence supports:

| Status | Meaning |
|---|---|
| `TECHNICALLY VERIFIED` | package, content-structure, runner, and PWA gates passed |
| `LEARNING VALIDATION CANDIDATE` | the repaired learning contract is implemented, but required human evidence is incomplete |
| `COURSE 1 LEARNING ACCEPTANCE: PASS` | every mandatory requirement in the final-release gate below has current evidence |
| `COURSE 1 LEARNING ACCEPTANCE: NOT YET` | one or more mandatory learning requirements failed or lack evidence |
| `LEARNER ARTIFACTS: PASS` | the learner's files pass objective artifact checks |
| `LEARNER SELF-REFLECTION: RECORDED` | reflection is preserved but is not assessment proof |
| `LEARNER ORAL COMPETENCE: VERIFIED` | an independent live oral assessment passed |
| `LEARNER ORAL COMPETENCE: SELF-ATTESTED ONLY` | only the learner's statement exists |
| `EXTERNAL UAT NOT VERIFIED` | only role-simulated acceptance rehearsal exists |
| `REAL SYNTHETIC UAT: VERIFIED` | another consenting person completed the defined synthetic tasks |
| `FULL BEGINNER COMPLETION NOT VERIFIED` | no eligible literal beginner has completed the full required sequence |

`PASS`, `objective`, `independent`, `UAT`, `beginner-validated`,
`accessible`, and `competent` must not appear unqualified when the corresponding
evidence class is absent.

## Stable Course 1 requirements

### `C1-LV-001` — Claim-to-evidence traceability

Every claim about what Course 1 teaches, proves, validates, or prepares a
learner to do must identify:

- the observable capability;
- the evidence class;
- the assessment method;
- the pass condition;
- the limitation;
- the later-course or real-engagement boundary.

**Gate:** no learner-facing or release claim exceeds its recorded evidence.

### `C1-LV-002` — Automated artifact verification

Automated checks may verify only observable file and system properties. Each
check must state the exact property it tests. Counting headings, phrases,
checkboxes, or files is structural evidence and must not be described as proof
of comprehension or objective judgment.

**Gate:** required artifact checks have positive, negative, missing, malformed,
and contradictory examples where applicable. The release record reports
structural checks as structural checks.

### `C1-LV-003` — Learner self-reflection

Confidence, perceived difficulty, time, fatigue, confusion, and self-attested
actions are useful learning records. They remain separate from scored evidence.

**Gate:** self-reflection cannot raise a rubric level, satisfy an independent
assessment, verify oral competence, or convert role simulation into UAT.

### `C1-LV-004` — Independent artifact assessment

Course competence claims based on artifacts require an assessor who:

- did not create or edit the assessed learner artifacts;
- uses the fixed Course 1 rubric and anchor examples;
- records evidence paths and reasons;
- declares conflicts and assistance given;
- does not repair the work during assessment.

A bounded artificial-intelligence review may help locate evidence, but it is
recorded separately from the independent human decision.

**Gate:** every scored area has an assessor-supported level and evidence path.
Unsupported or disputed areas result in `NOT YET`, not an averaged pass.

### `C1-LV-005` — Oral competence

Written answers and the statement “answered aloud” are not proof of oral
competence. Verified oral competence requires a live assessment in which:

- questions are asked one at a time;
- the learner cannot read a prepared or generated answer;
- the assessor asks at least one evidence-based follow-up on a weak, vague, or
  unsupported answer;
- the learner can say “I do not know” and name a safe next step;
- the assessor records only the score and concise evidence unless the learner
  separately consents to recording audio or video.

**Gate:** all required concepts are explained accurately in the learner's own
words, unsafe overclaims are rejected, and follow-up answers remain consistent
with the artifacts. Otherwise record `SELF-ATTESTED ONLY` or `NOT YET`.

### `C1-LV-006` — Role-simulated operational acceptance rehearsal

When the learner acts as operator, reviewer, tester, or process owner, the
exercise is a `ROLE_SIMULATED_ACCEPTANCE_REHEARSAL`.

It may demonstrate:

- correct execution of synthetic normal and failure tasks;
- evidence tracing;
- approve, edit, reject, expire, fallback, and safe-stop reasoning;
- defect recording and retesting.

**Gate:** the evidence is labelled role-simulated and retains
`EXTERNAL UAT NOT VERIFIED`. It must not be titled or summarised as completed
real UAT.

### `C1-LV-007` — Real synthetic User Acceptance Testing

`REAL SYNTHETIC UAT` requires at least one other consenting person acting as an
intended user. The participant must receive the user instructions, not the
answer key, and use synthetic data only.

Record:

- predefined task and success criteria;
- participant role and relevant prior experience;
- help requested, errors, completion, time, comments, and observed defects;
- facilitator interventions;
- retest outcome after any correction;
- the limitation that this is synthetic and not production evidence.

**Gate:** only independent observed task evidence may change the status to
`REAL SYNTHETIC UAT: VERIFIED`.

### `C1-LV-008` — Literal-beginner validation

A literal beginner trial participant must start with:

- no Python programming experience;
- no Git workflow experience;
- no automation implementation experience;
- no prior use of this Course 1 answer material.

Previous general computer use is recorded rather than treated as failure.
The course author, repair agent, assessor, and participant roles must be
distinct in the evidence.

The facilitator may protect safety and privacy but must record every hint,
correction, or intervention. Hidden help is not allowed.

**Gate:** before a `BEGINNER-VALIDATED` claim:

1. at least two eligible beginners complete onboarding, Foundations 1–3, and
   one representative long-module segment under observation;
2. at least one eligible beginner completes the full required Course 1
   sequence;
3. no unresolved blocker requires undocumented expert intervention;
4. confusion, recovery, assistance, time, and fatigue evidence is preserved;
5. resulting changes are retested with the affected participant or a new
   eligible beginner.

If the full trial is incomplete, use `FULL BEGINNER COMPLETION NOT VERIFIED`.

### `C1-LV-009` — Current-computer execution

Compatibility claims for the learner's computer require actual execution, not
only software detection or instructions.

**Gate:** with the learner's approval for installation or configuration:

- the official setup path completes;
- the required commands work in a new PowerShell session;
- Foundation 3 completes;
- one representative runner workflow and test command complete;
- restart/resume behavior is checked;
- versions, environment, deviations, and unresolved limitations are recorded.

Until then, the release may say the machine is detected and instructions are
available, but not that the full course was executed on that computer.

### `C1-LV-010` — Delayed retention

Immediate recreation is near-term practice, not retained competence.

**Gate:** at completion of the unseen transfer, a create-once machine-generated
UTC timestamp and SHA-256 values lock the transfer and a separate answer-free
task card. From 7 elapsed days through before day 15, without first reopening
the worked answer, the learner uses that task card to create a record with a
machine check time and calculated elapsed interval, then must:

- explain the rule/AI/human boundary;
- identify evidence versus assumption;
- describe safe stop, fallback, and approval invalidation;
- perform one previously completed bounded task;
- record help and re-study required.

The result is `DELAYED RETENTION: PASS`, `PARTIAL`, or `NOT YET`; it cannot be
inferred from same-session work, learner-entered dates, or a missed window.

### `C1-LV-011` — Unseen transfer

The transfer task must use a new, synthetic, non-document scenario whose exact
answer is absent from the course. It may be design-only and must not require a
new platform or paid service.

The learner independently identifies:

- process boundary and owner;
- authoritative input and evidence;
- deterministic rules;
- any bounded optional AI contribution;
- human authority;
- failure, fallback, and escalation;
- evaluation evidence;
- a justified continue, discover further, rework, or stop decision.

**Gate:** an independent assessor applies fixed anchors. Multiple outcomes may
pass when supported. Copying the Course 1 example with renamed nouns does not
pass.

### `C1-LV-012` — Dutch-market communication

Course 1 remains primarily English. Preparation for Dutch SMEs requires a
bounded communication check, not a claim of real consulting experience.

**Gate:** the learner gives a short Dutch plain-language explanation to a
Dutch-speaking reviewer covering:

- the fictional business problem and boundary;
- rules, optional AI, and human authority;
- one failure and manual fallback;
- what evidence supports the decision;
- what the demonstration does not prove;
- the next safe discovery or escalation step.

The reviewer records comprehension questions, unclear jargon, overclaims, and
whether the learner corrected a misunderstanding. No real organisation or
client data is used. Until this occurs, use `DUTCH CLIENT COMMUNICATION:
REHEARSED OR UNVERIFIED`, not “client-ready.”

### `C1-LV-013` — Cognitive load and time evidence

Word counts, command counts, and author-estimated ranges are planning evidence,
not novice-time evidence.

Before a learning-acceptance release:

- every long lesson has visible sub-goals and safe stopping points;
- required understanding is distinguished from mechanical helper execution;
- prerequisite concepts are taught before use;
- a learner can resume without rereading the entire page;
- no single planned study segment assumes more than 60 focused minutes without
  an explicit break or stopping point;
- measured active time, elapsed time, help, errors, retries, fatigue, and
  abandonment are recorded during beginner trials.

**Gate:** published time ranges identify their sample and method. Until a full
beginner completion exists, total duration remains `AUTHOR ESTIMATE — NOT
BEGINNER MEASURED`.

### `C1-LV-014` — Accessibility evidence and limitations

Automated markup, keyboard, contrast, forced-colour, reflow, and responsive
tests are necessary but do not replace assistive-technology testing.

Before learning acceptance, manually test critical flows with:

- current NVDA with Chrome or Firefox on Windows;
- Windows Narrator with Microsoft Edge;
- keyboard only;
- Windows high contrast or forced colours;
- 200% zoom/reflow and the course's enlarged reader text.

Critical flows include first load, navigation, search, progress, lesson
reading, code-copy controls, scrollable tables, notes, update prompt,
backup/import, reset confirmation, offline messaging, and error/status
announcements.

Record technology versions, browser, task, announcement/focus result, defect,
and retest. If no screen-reader user participated, state
`SCREEN-READER USER VALIDATION NOT VERIFIED`. Never claim universal
accessibility from a finite test.

### `C1-LV-015` — Assessor calibration

Before independent scoring is used as a pass gate:

- the rubric has observable anchors for levels 1–4 in every area;
- at least two assessors score the same blinded anchor set independently;
- each records evidence before discussion;
- disagreements are resolved against the written anchor, not by averaging;
- the calibration result and unresolved ambiguity are recorded.

**Gate:** exact agreement is required on automatic failure/rework conditions
and on pass versus `NOT YET`. A one-level difference may remain only within the
same final result and must be documented. The learner's own score is reflection,
not one of the independent assessor scores.

### `C1-LV-016` — Human-trial safety, privacy, and consent

All trials use synthetic Course 1 data. Before participation, state:

- purpose and expected time;
- voluntary participation and right to stop;
- what observations will be recorded;
- whether screen, audio, or video recording is proposed;
- retention and deletion date;
- who can access the evidence;
- that participation is not employment, medical, or professional evaluation.

Do not collect unnecessary names, employer details, health information,
credentials, or client information. Use participant codes in release evidence.
Audio, video, screen recording, or quotations require explicit separate
consent.

**Gate:** missing consent or real/confidential data invalidates the trial
evidence and triggers safe handling; it is not copied into the repository.

### `C1-LV-017` — Learning-release decision

The final learning acceptance decision must list every stable requirement as:

- `PASS` with exact evidence;
- `NOT YET` with the failed condition;
- `NOT APPLICABLE` with a contract-supported reason.

Unperformed human checks are `NOT YET`, not assumed passes. A strong technical
release cannot average away missing beginner, oral, UAT, retention,
communication, or accessibility evidence.

## Before-final-release evidence set

The following is mandatory for `COURSE 1 LEARNING ACCEPTANCE: PASS`:

| Requirement | Minimum evidence |
|---|---|
| `C1-LV-001` | signed claim-to-evidence matrix for the release |
| `C1-LV-002` | current automated artifact report with negative-case evidence |
| `C1-LV-003` | assessment record visibly separates reflection from scores |
| `C1-LV-004` | one complete independent artifact assessment |
| `C1-LV-005` | one independently assessed live oral demonstration |
| `C1-LV-006` | complete labelled role-simulated rehearsal |
| `C1-LV-007` | one other-person synthetic UAT with defects and retest status |
| `C1-LV-008` | two sampled beginner trials and one full beginner completion |
| `C1-LV-009` | current-computer setup plus representative execution |
| `C1-LV-010` | 7–14-day delayed retention result |
| `C1-LV-011` | independently assessed unseen transfer result |
| `C1-LV-012` | Dutch-speaking reviewer result |
| `C1-LV-013` | measured cognitive-load/time evidence and labelled estimate |
| `C1-LV-014` | named assistive-technology manual checks and limitations |
| `C1-LV-015` | blinded assessor-calibration record |
| `C1-LV-016` | consent, minimisation, retention, and deletion evidence |
| `C1-LV-017` | final requirement-by-requirement decision |

The repaired course may be used locally, in an explicitly unpromoted
evidence-collection trial, or through the separately authorized
`personal-synthetic-study` publication lane when its applicable technical
safety gates pass. Public personal-study availability is distribution, not
learning validation: it cannot authorize completion awards, accepted-release
promotion, a current product `PASS`, Course 2 readiness, or consultant claims.
Every missing human check remains a visible limitation. The candidate or study
edition must not be described as fully beginner-validated or as proof of
consultant readiness.

## Evidence-record minimum fields

Store future release evidence outside the bundled content hash under:

`release_evidence/course1_learning_validation/<course-version>/`

Every record must contain:

- stable requirement ID;
- evidence class;
- course version, practice revision, build ID, and content hash;
- date and environment;
- participant or reviewer code and role;
- relevant prior experience;
- task and pass criteria fixed before execution;
- observed result, help, deviations, defects, and retest;
- data/consent statement;
- limitation;
- decision and reviewer.

Do not commit raw participant audio, video, screenshots containing personal
information, credentials, or real work data. A redacted structured result is
the release artifact.

## Change control

Changing a threshold, participant definition, evidence class, or mandatory
requirement is a material assessment change. It requires:

1. a documented reason;
2. comparison with the main goal and learner stage;
3. `STRATEGIC FIT: PASS`;
4. a new contract version;
5. preserved old evidence and decision history;
6. revalidation of affected claims.

Convenience, schedule pressure, an expiring credit, or difficulty finding a
participant is not evidence that a requirement should be weakened.
