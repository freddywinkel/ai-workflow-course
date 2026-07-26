# Course 1 — Controlled AI Workflow Foundations for Dutch SMEs

- Version: 2.0.0
- Verified through: 2026-07-26
- Language: English, with Dutch and EU terms where useful
- Format: self-paced, gate-based learning
- Estimated effort for a literal beginner: 110–150 hours
Endpoint: a private, reproducible portfolio demonstration using synthetic data

Course reader: [open the installable PWA](https://freddywinkel.github.io/ai-workflow-course/)  
Repository: [freddywinkel/ai-workflow-course](https://github.com/freddywinkel/ai-workflow-course)

## The purpose of this course

This is the first technical course in a longer path towards becoming a
**Controlled AI Workflow Implementation Consultant for Dutch SMEs**.

The durable job is not “drawing automation boxes” or knowing one AI product.
It is learning to:

- observe how work is actually done;
- measure the problem before proposing technology;
- decide whether the right answer is process improvement, ordinary rules,
  existing software, a bounded AI step, or no automation;
- design a workflow with visible states, tests, human control, and a manual
  fallback;
- evaluate usefulness, cost, failure behaviour, and adoption honestly;
- explain assumptions, limitations, and escalation needs to a client.

The PWA's separate **Career Path** tab and the
[Career Sequence](CAREER_SEQUENCE.md) show the later courses that add paid
diagnostics, integrations, production engineering, governance, adoption, and
consulting delivery. Those later courses are a roadmap, not part of this
course's completion percentage.

## What you will build

You will build a **Synthetic SME Operations Exception Assistant**:

```text
fictional CSV or spreadsheet-style export
  → schema and data-quality checks
  → deterministic exception rules
  → named workflow state
  → optional AI summary using verified issue IDs
  → human approve, edit, reject, or expire
  → local draft outbox only
  → audit event and evaluation result
```

The workflow flags problems such as missing owners, overdue work, duplicate
references, contradictory dates, invalid statuses, and incomplete reviews.
Ordinary code determines the exceptions. AI may explain or group verified
exceptions, but it does not decide whether the business is compliant and it
does not update another system.

The project is deliberately based on structured synthetic data. That gives a
beginner a safer and more transferable foundation than starting with OCR,
vector search, autonomous agents, production integrations, or regulated data.

## What completing Course 1 proves

You can:

- map one bounded administrative process and identify its owner, users,
  systems, handoffs, exceptions, and fallback;
- create a baseline for volume, handling time, waiting time, and rework;
- write an intended purpose, exclusions, and a build-versus-buy decision;
- define a small data contract and deterministic business rules;
- build a reproducible rule-first workflow;
- add one optional, schema-constrained AI step without making AI authoritative;
- design meaningful human review and prevent unapproved actions;
- run a practical Dutch SME privacy, AI, vendor, and security pre-screen;
- evaluate normal cases, edge cases, failures, time, cost, and usability;
- produce a UAT script, runbook, limitations record, handover pack, and honest
  portfolio demonstration.

## What it does not prove

Course 1 does **not** make you ready to:

- deploy production systems independently;
- process real client, employer, patient, employee, or other personal data;
- provide legal, privacy, security, compliance, accounting, or medical advice;
- implement clinical, employment, credit, insurance, housing, education,
  migration, policing, or other consequential decision systems;
- configure Veeva or another regulated platform professionally;
- promise savings before measuring a real process;
- call yourself an experienced AI consultant.

The honest exit position is **workflow analyst in training with a controlled
synthetic portfolio project**.

## Course structure

### Beginner foundations

Nine foundation lessons teach files, PowerShell, Python, APIs, Git,
spreadsheets and CSV data, AI limitations, safe AI-assisted building, workflow
tools, and data stores. Start here if you have no technical experience.

### Course 1 modules

1. Observe the process.
2. Select and bound the opportunity.
3. Understand the data and rules.
4. Build the non-AI workflow first.
5. Add one bounded AI step.
6. Keep humans in control.
7. Apply Dutch SME guardrails and choose the right tool.
8. Evaluate usefulness and business value.
9. Run UAT, plan adoption, and hand over the demonstration.

Each module has an evidence artifact and a gate. A calendar is not a gate. Do
not continue merely because a scheduled week has ended.

## Safety boundary

Use only supplied or self-created synthetic data.

Excluded throughout:

- real client or employer information;
- personal data, special-category data, BSNs, or national identifiers;
- patient, sample, clinical, or medical information;
- credentials, access tokens, private URLs, or internal configurations;
- autonomous sending, payment, deletion, record change, or binding action;
- high-impact decisions about people;
- claims that the workflow proves compliance.

A technically correct **DO NOT PILOT** conclusion is a successful course
outcome when the evidence shows that the idea is unsafe, unnecessary, or not
worthwhile.

## Start here

1. Read the [Beginner Readiness Check](BEGINNER_READINESS_CHECK.md).
2. Complete the [Beginner Foundations](foundations/README.md).
3. Read the [Course Overview](COURSE_OVERVIEW.md).
4. Run the live check in [EVERGREEN_UPDATE_PROMPT.md](EVERGREEN_UPDATE_PROMPT.md).
5. Complete [SETUP_WINDOWS.md](SETUP_WINDOWS.md).
6. Work through Modules 1–9 in order.
7. Use [CAPSTONE_SPECIFICATION.md](CAPSTONE_SPECIFICATION.md) and
   [ASSESSMENT_AND_RUBRIC.md](ASSESSMENT_AND_RUBRIC.md) for final acceptance.

## PWA versus the workflow you build

The PWA is an offline course reader and progress tracker. It contains no AI and
does not run the capstone. You build the capstone separately while following
the lessons. Progress and private notes remain in the browser or installed
app.

## Design rule for a fast-changing AI market

Current tools, models, laws, prices, and interfaces are updateable references.
Process discovery, data contracts, deterministic controls, evaluation, human
oversight, failure recovery, adoption, and evidence are the durable curriculum.

Run the evergreen audit before starting the AI module and again before using
the material for any real pilot.
