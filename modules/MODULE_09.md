# Module 9 — Run UAT, Plan Adoption, and Hand Over

## Outcome

Finish Course 1 with a synthetic user acceptance test, an operating and
fallback package, an adoption plan, and an honest five-minute portfolio
demonstration that another person can follow.

## Beginner checkpoint

- the evaluation report is reproducible;
- final decision criteria are written;
- review lifecycle and fallback pass;
- ownership gaps are visible;
- the system makes no production-readiness claim.

## Concepts

### User acceptance testing

UAT asks whether the intended user can complete the intended task in a
realistic context. It is not another developer test.

### Adoption

Successful implementation changes a process, responsibilities, and habits.
Training alone cannot repair a badly designed workflow.

### Handover

The recipient needs purpose, operation, limits, ownership, fallback, and
support information—not only source code.

### Benefits realization

Value is checked after use against the original baseline. A projected saving is
not yet a result.

## Official readings

- [European Commission AI literacy Q&A](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers)
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [OECD SME AI adoption report](https://www.oecd.org/en/publications/ai-adoption-by-small-and-medium-sized-enterprises_426399c1-en.html)

## Guided build

### 1. Define UAT roles

Use fictional roles:

- process owner;
- operations reviewer;
- workflow operator;
- technical support;
- privacy/security reviewer for future real use.

One person may play multiple roles in the course exercise, but document the
separation expected in a real client.

### 2. Write UAT scenarios

At minimum:

1. run the normal synthetic input;
2. find a high-severity issue and its source values;
3. distinguish deterministic output from the optional summary;
4. reject a draft;
5. edit and reapprove a new revision;
6. handle an AI failure using fallback;
7. activate the kill switch;
8. explain why nothing was sent externally;
9. locate the runbook;
10. report an unexpected problem.

Define expected results before the UAT session.

### 3. Run UAT with another person

Ask the participant to think aloud. Record:

- task completed or failed;
- time;
- confusion;
- help requested;
- error;
- suggested improvement.

Use only synthetic data. Obtain permission before recording a screen or voice.

### 4. Repair usability defects

Classify findings:

- must fix before demonstration;
- should fix later;
- accepted limitation;
- training need;
- unsupported request.

Retest every must-fix item. Do not hide it in a training document.

### 5. Create role-specific guidance

The reviewer needs:

- purpose and boundary;
- how to inspect issue evidence;
- how AI text is labelled;
- how to approve, edit, reject, or expire;
- how to use fallback;
- what must be escalated.

The operator needs:

- start and stop;
- input/output folders;
- configuration;
- failure states;
- kill switch;
- recovery;
- support route.

### 6. Write the runbook

Include:

- prerequisites;
- exact start command;
- expected successful state;
- where output appears;
- common errors;
- AI-off procedure;
- n8n-off manual procedure;
- kill switch;
- safe retry;
- backup or export;
- change and rollback method;
- owner and escalation placeholder.

Test the runbook from a clean start.

### 7. Assemble the handover pack

Required:

- intended purpose and exclusions;
- process and stakeholder maps;
- opportunity decision;
- data dictionary and rule register;
- architecture and states;
- risk and tool-fit screen;
- prompt/schema/model record;
- evaluation report;
- UAT record;
- runbook and fallback;
- role guidance;
- change log;
- ownership matrix;
- limitations;
- final pilot decision.

### 8. Write the portfolio case

Use this structure:

1. fictional context;
2. observed problem and assumptions;
3. baseline;
4. why rules came before AI;
5. architecture and safeguards;
6. evaluation result;
7. what failed and changed;
8. final decision;
9. boundary: synthetic demonstration, not production.

Do not present fictional metrics as client outcomes.

### 9. Record a five-minute demonstration

Show:

- problem and scope;
- one input case;
- deterministic issues;
- optional summary and issue IDs;
- review/edit/approval;
- local draft only;
- one failure and fallback;
- evaluation decision.

The recording must not contain secrets, employer names, browser history, or
personal notifications.

### 10. Complete the final decision

Choose `PILOT`, `REWORK`, or `DO NOT PILOT`.

If `PILOT`, the wording must say:

> suitable only for a later small, supervised, low-risk pilot after client
> process-owner, IT, privacy, and security review.

### 11. Identify the next course

Course 2 is Workflow Discovery and Paid Diagnostics. Do not compensate for a
weak market signal by building a larger product.

## Consultant lens

Ask:

- Who must adopt the new process?
- What changes in their responsibility?
- What could create resistance or shadow work?
- Who owns support after the consultant leaves?
- Which metric will be checked after two and six weeks?
- When will the workflow be paused or retired?

Request:

- process-owner acceptance;
- named support contact;
- UAT participants;
- training needs;
- normal and fallback operating procedures;
- benefit review date.

Stop when:

- nobody owns the workflow;
- UAT users cannot understand the evidence;
- training is being used to hide design defects;
- the client expects indefinite unpriced support;
- the demonstrated boundary differs from proposed use.

Client-style deliverable:

- UAT record, adoption plan, runbook, handover, and decision presentation.

## Capstone increment

The Synthetic SME Operations Exception Assistant is complete as a controlled
portfolio demonstration.

It is not deployed.

## Required artifact

- `evidence/module_09_uat.md`;
- completed UAT script;
- defect/retest record;
- adoption and training plan;
- runbook and fallback;
- handover index;
- portfolio case study;
- five-minute demonstration;
- signed self-assessment against `ASSESSMENT_AND_RUBRIC.md`;
- final pilot decision.

## Test gate

- [ ] Another person completes the UAT scenarios.
- [ ] Must-fix usability defects are retested.
- [ ] Role guidance distinguishes operator and reviewer needs.
- [ ] The runbook works from a clean start.
- [ ] Fallback and kill switch are demonstrated.
- [ ] The handover pack contains every required artifact.
- [ ] Portfolio metrics are clearly synthetic.
- [ ] The final decision follows evidence.
- [ ] I can answer all oral assessment questions in plain language.
- [ ] I state that Course 1 does not make the system production ready.

## Stop or rework

Do not mark complete if:

- only the builder can operate the workflow;
- UAT is a scripted presentation rather than user action;
- source, output, or secrets are mixed;
- the portfolio implies a real client;
- the final decision ignores unresolved blockers;
- no owner or manual fallback is documented.

## Common failures

- overtraining instead of fixing usability;
- handing over code without operations guidance;
- hiding accepted limitations;
- demonstrating only success;
- claiming consultant readiness from one course;
- starting another technical course before testing market demand.

## Estimated time

12–18 hours, including retest and portfolio preparation.
