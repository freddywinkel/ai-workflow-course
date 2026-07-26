# Course Overview — From SME Problem to Controlled Demonstration

## Target learner

This course is for a learner who:

- wants to move towards AI workflow implementation consulting for Dutch SMEs;
- may have no coding, command-line, automation, or API experience;
- is willing to learn one small concept at a time and verify observed results;
- wants a foundation that remains useful when AI products change;
- accepts that production consulting requires later courses and real delivery
  experience.

## Course promise

You will take one fictional, low-risk administrative process from an unclear
problem to a tested, documented, human-controlled demonstration.

You will not merely assemble an automation. You will produce the evidence a
responsible implementation consultant needs:

- why this problem was selected;
- what the current process costs or delays;
- what is authoritative data and what is not;
- which steps are rules, AI, or human judgment;
- how failures become visible;
- what the workflow does when AI is unavailable;
- who reviews the output;
- whether the measured result supports `PILOT`, `REWORK`, or `DO NOT PILOT`;
- how another person could operate and stop it.

## Role boundary after completion

| Capability | After Course 1 |
|---|---|
| Explain a bounded workflow | Yes |
| Build and test with synthetic data | Yes |
| Produce a portfolio case study | Yes |
| Run a basic risk and tool-fit pre-screen | Yes |
| Offer legal or compliance conclusions | No |
| Process real client data independently | No |
| Deploy a production integration independently | No |
| Configure regulated platforms professionally | No |
| Call yourself an experienced consultant | No |

The career roadmap in the PWA shows how later courses close these gaps.

## Learning design

The course uses three layers.

### Layer 1 — Beginner foundations

The foundations teach enough technical literacy to understand and supervise a
small workflow:

1. files and plain text;
2. command-line survival;
3. code and Python;
4. web APIs and JSON;
5. Git and safe changes;
6. spreadsheets, CSV, and data quality;
7. AI and controlled workflows;
8. safe AI-assisted building;
9. workflow tools and data stores.

### Layer 2 — Nine project modules

Each module adds one consultant capability and one capstone increment.

| Module | Consultant capability | Main evidence |
|---:|---|---|
| 1 | Observe before proposing | As-is map, stakeholder map, manual baseline |
| 2 | Select and bound a worthwhile opportunity | Scorecard, intended purpose, go/no-go |
| 3 | Identify authoritative data and rules | Data dictionary, contract, expected issues |
| 4 | Build reliable logic without AI | Rule-first workflow and failure tests |
| 5 | Add AI only where it helps | Bounded summary with issue-ID support |
| 6 | Preserve meaningful human control | Review package, approval lifecycle, local outbox |
| 7 | Screen risk and existing-tool fit | Data flow, risk screen, tool-fit decision |
| 8 | Evaluate utility and value | Regression report and pilot decision |
| 9 | Prepare people and handover | UAT evidence, runbook, training and demo |

### Layer 3 — Capstone acceptance

The final demonstration is assessed on discovery, data and rules, bounded AI,
human control, Dutch SME guardrails, evaluation, adoption, and handover.

## The fictional scenario

`Northstar Services BV` is a fictional Dutch B2B service company. Its
operations team exports a weekly work-item register from an imaginary business
system. The register contains deliberately designed normal cases and defects.

No company, customer, employee, or person in the data is real.

The learner must detect and explain issues such as:

- a missing owner;
- an overdue open item;
- duplicate IDs or references;
- an unsupported status;
- impossible or contradictory dates;
- a required review without evidence;
- a stale record;
- malformed input;
- untrusted text attempting to influence the AI step.

## Rule-first allocation

| Task | Default owner |
|---|---|
| Required fields, dates, duplicates, allowed statuses | Deterministic code |
| Whether a flagged item needs business action | Human reviewer |
| Plain-language grouping of already verified issues | Optional AI |
| Compliance, legal, employment, credit, or clinical judgment | Excluded / specialist |
| Sending or updating another system | Excluded in Course 1 |

If AI is removed, the exception report must still work.

## Evidence habit

Every module produces a required artifact. Store artifacts in a separate
project repository, not inside the PWA source. Suggested structure:

```text
operations-exception-assistant/
  README.md
  data/
  docs/
  prompts/
  src/
  tests/
  output/
  evidence/
```

Do not store secrets or real data in Git.

## Gates, not calendar pressure

The 110–150 hour estimate is a planning range, not a deadline.

At roughly 20 hours per week, a literal beginner may need 6–9 calendar weeks.
At 8–10 hours per week, 13–18 weeks is more realistic. Stop when:

- you cannot explain what a command changes;
- a test result differs from the lesson;
- data meaning is unclear;
- the workflow silently drops a failure;
- AI makes a claim without a verified issue ID;
- the review step is ceremonial;
- the proposed value is not measurable;
- privacy, security, legal, or domain questions exceed your competence.

## What moves to later courses

The previous supplier-document material is preserved for a future Controlled
Document AI course. Course 1 intentionally defers:

- PDF and DOCX parsing;
- OCR and page-level evidence locators;
- retrieval and vector databases;
- production APIs and multi-tenant databases;
- OAuth connectors and external write-back;
- production security architecture;
- advanced legal and vendor assessments;
- regulated platform configuration;
- autonomous agents.

Deferring these topics is sequencing, not deletion. The Career Path tab shows
where they return.

## Passing can mean “do not build”

A consultant is paid for judgment, not for forcing AI into every process.
Course 1 passes a well-supported `DO NOT PILOT` decision when the learner shows
that:

- existing software already solves the problem;
- the baseline is too small to justify the effort;
- data quality is too weak;
- the failure consequence is too high;
- the proposed AI step adds no measurable value;
- the organization cannot yet own or support the workflow.
