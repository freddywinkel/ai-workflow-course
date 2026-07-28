# Risk and Escalation Screen

Artifact ID:
Version/date:
Author/reviewer:
Workflow/intended-purpose version:

This is a practical first screen, not legal, security, privacy, or regulatory
advice.

## Course 1 stop screen

If any answer is **yes** or **unknown**, stop that path and escalate.

| Question | Yes/No/Unknown | Evidence | Escalation role |
|---|:---:|---|---|
| Does the input contain real personal, confidential, or special-category data? | | | |
| Could output materially affect a person's rights, care, work, money, access, or opportunity? | | | |
| Is there a medical, safety-critical, legal, financial, or regulated intended purpose? | | | |
| Could the system send, pay, purchase, sign, delete, publish, grant access, or write back automatically? | | | |
| Is any data destination, retention, training use, or support access unresolved? | | | |
| Is the process, data, system, or decision owner missing? | | | |
| Is meaningful review or manual fallback unavailable? | | | |
| Would failure be hard to detect or reverse? | | | |

Course path after screen: CONTINUE SYNTHETIC ONLY / SELECT LOWER-RISK USE CASE /
SPECIALIST REVIEW REQUIRED

## Risk register

Use probability and impact as LOW / MEDIUM / HIGH. Do not multiply scores to
hide uncertainty.

| ID | Scenario/cause | Affected outcome | Probability | Impact | Prevent | Detect | Recover | Residual risk | Owner |
|---|---|---|:---:|:---:|---|---|---|---|---|
| RK-001 | | | | | | | | | |

Include at least:

- wrong or missing input;
- duplicate or stale work;
- unsupported AI output;
- prompt injection or malformed content;
- unauthorised access or data exposure;
- timeout, outage, or partial completion;
- reviewer error or automation bias;
- user non-adoption or workaround;
- unowned alert, credential, bill, or update;
- inability to restore or continue manually.

## Escalation routes

Use roles, not personal contact details, in Course 1.

| Trigger/reason code | Immediate safe action | Evidence to preserve | Decision role | Response target | Resume criteria |
|---|---|---|---|---|---|
| | | | | | |

## Pause and kill controls

How new runs are paused:
What `EXTERNAL_ACTIONS_ENABLED=false` blocks:
What remains available:
How the stopped state is verified:
Who may re-enable and on what evidence:
Manual fallback owner and location:

## Decision

Risks accepted for synthetic demonstration:
Risks that block later implementation or require escalation:
Specialist or owner review required:
Next test/control:
Decision: CONTINUE SYNTHETIC TEST / REWORK / DO NOT CONTINUE
Decision owner/date:
