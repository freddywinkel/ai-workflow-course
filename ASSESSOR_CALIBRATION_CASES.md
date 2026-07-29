# Course 1 Assessor Calibration Cases

## Purpose

This is the blinded case set for Course 1 assessor calibration. It contains no
learner result and no answer key. Each assessor classifies every case
independently before viewing the other assessor's record or
`ASSESSOR_CALIBRATION_KEY.md`.

**User Acceptance Testing (UAT)** means another consenting intended user
performs realistic synthetic tasks.

Use the whole-number rubric levels 1, 2, 3, or 4 from
`ASSESSMENT_AND_RUBRIC.md`. For each case, record:

- the level;
- the evidence that controls the level;
- any automatic failure or evidence cap;
- whether the evidence is enough for `PASS` or remains `NOT YET`.

Do not average cases or award points. This exercise calibrates the boundary
between levels; it does not assess the learner.

## Case Cedar

The learner used synthetic data only. All mandatory artifacts and failure
routes have evidence. The learner authored the isolated deterministic rule and
tests, completed the unseen transfer, preserved limitations, and performed the
operator tasks personally. No other intended user performed the tasks, so the
record says `EXTERNAL UAT NOT VERIFIED`. The delayed-retention task passed.

## Case Harbor

The demonstration looks polished and its happy path passes. One generated
statement has no source-linked issue. A configuration still permits an
external message, and the learner cannot explain what exact evidence the
reviewer approves. The portfolio text calls the result safe because the demo
worked once.

## Case Linden

All evidence described in Case Cedar is present. In addition, another
consenting intended user completed the synthetic operator tasks without
builder intervention, the defect/retest trail is complete, delayed retention
and unseen transfer passed, and the handover lets another person run, stop, and
recover the demonstration.

## Case Maple

The intended control and synthetic boundary are visible, and no external
action occurs. However, one required source link is absent, the owner for one
failure route is blank, and the learner-authored rule has no boundary test.
The learner says these items can be added later.

## Independent record

Assessor code:
Role:
Date:
Conflict/help declaration:
Learner evidence opened before classification: YES / NO
Other assessor record viewed before classification: YES / NO

| Case | Level 1–4 | Automatic failure or cap | PASS or NOT YET | Evidence-based reason |
|---|---:|---|:---:|---|
| Cedar | | | | |
| Harbor | | | | |
| Linden | | | | |
| Maple | | | | |

Automatic failure/rework boundary:
Pass versus `NOT YET` boundary:
