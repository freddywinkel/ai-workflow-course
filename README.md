# Course 1 — Controlled Artificial Intelligence (AI) Workflow Foundations for Dutch Small and Medium-sized Enterprises (SMEs)

- Version: 2.2.0
- Verified through: 2026-07-28
- Language: English, with Dutch and European Union (EU) terms where useful
- Format: self-paced, gate-based learning—you continue after proving a skill,
  not merely after spending a set number of days
- Estimated effort for a literal beginner: 140–180 hours
- End result: a private, **reproducible** portfolio demonstration—someone can
  repeat the documented steps and obtain the same result—using fictional
  practice data

Course reader: [open the installable progressive web app (PWA)](https://freddywinkel.github.io/ai-workflow-course/).
A PWA is a website that can also be installed and used like an app.

Course repository: [freddywinkel/ai-workflow-course](https://github.com/freddywinkel/ai-workflow-course).
A **repository** is the project folder whose files and changes are tracked
together.

## The purpose of this course

This is the first technical course in a longer path towards becoming a
**Controlled AI Workflow Implementation Consultant for Dutch SMEs**. From this
point onward, **AI** means artificial intelligence, **SME** means small and
medium-sized enterprise, and **PWA** means progressive web app.

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
diagnostics (structured problem assessments), integrations (connections between
systems), production engineering (building for real daily use), governance
(rules, ownership, and oversight), adoption (helping people use the change), and
consulting delivery. Those later courses are a roadmap, not part of this
course's completion percentage.

## What you will build

You will build a **Synthetic SME Operations Exception Assistant**. Here,
**synthetic** means completely fictional rather than copied from real work.

Before reading the flow below:

- a **schema** describes the fields, formats, and values that data is allowed to
  contain;
- a **deterministic rule** gives the same result whenever it receives the same
  input;
- a **workflow state** is a named stage such as `NEW` or `REVIEWED`;
- a **local draft outbox** is a folder of prepared messages that are not
  actually sent; and
- an **audit event** is a dated record of what happened, while an **evaluation
  result** records whether the workflow met a stated test.

```text
fictional comma-separated values (CSV) or spreadsheet-style export
  → schema and data-quality checks
  → deterministic exception rules
  → named workflow state
  → optional AI summary using verified issue identifiers (IDs)
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
beginner a safer and more transferable foundation than starting with optical
character recognition (OCR), software that extracts text from images; **vector
search**, which finds similar content by mathematical similarity; **autonomous
agents**, which can choose and perform several actions with limited supervision;
**production integrations**, which connect systems used in real daily work; or
**regulated data**, which is subject to formal legal or industry controls.

## How every practical lesson works

You are not expected to learn by being given a vague task and guessing what to
do. Every foundation and module uses the same four-part loop:

1. **Follow along — I show you exactly how.** You receive the starting point,
   exact Windows clicks or commands, an explanation of what each action does,
   the result you should see, and a small troubleshooting check.
2. **Now recreate it yourself.** You repeat the skill with different fictional
   names or data. This checks whether you understood the idea instead of merely
   copying.
3. **Ask Codex to check your work.** **Codex** is the course workspace assistant
   you are using now. The lesson provides a copy-and-paste prompt. You replace
   its placeholder with the full path to that lesson's practice folder. Codex
   then inspects only that folder in read-only mode and reports **PASS** or
   **NOT YET**, with exact corrections.
4. **Pass criteria.** You mark the lesson complete only when every stated
   criterion is visible in your files or output.

**Read-only** means Codex may inspect and explain your files but may not edit,
rename, move, or delete them. Never authorize a broad inspection of your whole
computer when one practice folder is enough. Never put passwords, secret keys,
employer data, client data, patient data, or other real personal information in
a practice folder.

If a lesson names a technical term before it makes sense to you, stop and ask:

> Explain this term as if I have never used it. Tell me what it is, why it is
> needed here, and give one harmless example. Do not perform the task for me.

The course spells out abbreviations at their first use. Product names are also
introduced before use. For example, **Git** is the name of a version-control
tool that records changes to files; it is not an abbreviation.

## What completing Course 1 proves

You can:

- map one **bounded** administrative process, with a clear start, end, and
  scope, and identify its owner, users, systems, handoffs between people or
  systems, exceptions, and manual fallback;
- create a **baseline**, meaning measurements of the current volume, handling
  time, waiting time, and rework before a change;
- write an intended purpose, exclusions, and a **build-versus-buy decision**
  that compares creating something with purchasing existing software;
- define a small **data contract**—the agreed required fields, formats, and
  allowed values—and deterministic business rules;
- build a reproducible rule-first workflow;
- add one optional, schema-constrained AI step without making AI authoritative;
- design meaningful human review and prevent unapproved actions;
- run a practical Dutch SME privacy, AI, vendor, and security **pre-screen**, an
  early check for obvious concerns that need a specialist;
- evaluate normal cases, **edge cases** at unusual but possible boundaries,
  failures, time, cost, and usability;
- produce a **user acceptance testing (UAT)** script for intended users to check
  the workflow, a **runbook** with operating and recovery instructions, a
  limitations record, handover pack, and honest portfolio demonstration.

## What it does not prove

Course 1 does **not** make you ready to:

- deploy **production systems**, meaning systems used for real daily work,
  independently;
- process real client, employer, patient, employee, or other personal data;
- provide legal, privacy, security, compliance, accounting, or medical advice;
- implement clinical, employment, credit, insurance, housing, education,
  migration, policing, or other consequential decision systems;
- configure **Veeva**, a commercial quality and document-management platform,
  or another **regulated platform** that must meet formal control requirements
  professionally;
- promise savings before measuring a real process;
- call yourself an experienced AI consultant.

The honest exit position is **workflow analyst in training with a controlled
synthetic portfolio project**.

## Course structure

### Beginner foundations

Nine foundation lessons teach files; **Windows PowerShell**, a tool for typing
commands; **Python**, a programming language; application programming
interfaces (APIs), which define how software exchanges requests and responses;
Git; spreadsheets and comma-separated values (CSV) data; AI limitations; safe
AI-assisted building; workflow tools; and **data stores**, meaning places where
a workflow keeps information. Start here if you have no technical experience.

### Course 1 modules

1. Observe the process.
2. Select and bound the opportunity.
3. Understand the data and rules.
4. Build the non-AI workflow first.
5. Add one bounded AI step.
6. Keep humans in control.
7. Apply Dutch SME guardrails and choose the right tool.
8. Evaluate usefulness and business value.
9. Run user acceptance testing (UAT), plan adoption, and hand over the
   demonstration.

Each module has an **evidence artifact**, a file that proves what you did, and a
**gate**, a checklist that must pass before you continue. A calendar is not a
gate. Do not continue merely because a scheduled week has ended.

## Safety boundary

Use only supplied or self-created synthetic data.

Excluded throughout:

- real client or employer information;
- personal data; **special-category personal data**, meaning especially
  sensitive types such as health information; Dutch citizen service numbers
  (*burgerservicenummers*, BSNs); or other national identifiers;
- patient, sample, clinical, or medical information;
- credentials such as usernames and passwords; **access tokens**, which are
  secret strings that grant software access; private **uniform resource
  locators (URLs)**, meaning non-public web addresses; or internal
  configurations;
- autonomous sending, payment, deletion, record change, or binding action;
- high-impact decisions about people;
- claims that the workflow proves compliance.

Course 1 has three valid final outcomes:

- **`ACCEPT FOR SYNTHETIC PORTFOLIO`** — the controlled demonstration is
  complete enough to show as fictional portfolio evidence;
- **`REWORK`** — the evidence identifies specific gaps to correct and retest;
- **`DO NOT CONTINUE`** — the evidence supports a safe stop and documented
  closeout.

All three can pass when the decision is honest and evidence-backed. None
authorizes a client pilot, real data, production use, or external action.

## Start here

1. Read the [Beginner Readiness Check](BEGINNER_READINESS_CHECK.md).
2. Complete Foundations 1 and 2 in the
   [Beginner Foundations](foundations/README.md). They teach folders and the
   Windows command tool without requiring extra software.
3. Run the read-only
   [Beginner Software Check](BEGINNER_SOFTWARE_CHECK.md). It checks current
   official download guidance without editing files or installing anything.
4. Complete [SETUP_WINDOWS.md](SETUP_WINDOWS.md). It installs the tools needed
   for later foundations and tells you exactly what to click, type, and check.
5. Finish Foundations 3–9.
6. Read the [Course Overview](COURSE_OVERVIEW.md).
7. Work through Modules 1–9 in order. Foundations stay in their safe practice
   folder. All module evidence goes into the one Git-tracked project created
   during Windows setup:
   `Documents\AI-workflow-learning\operations-exception-assistant`.
8. Complete the **capstone**, the final project that combines all module work
   in that same repository.
   Use [CAPSTONE_SPECIFICATION.md](CAPSTONE_SPECIFICATION.md) and
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

The maintainer-only evergreen audit keeps product, law, and source references
current. It is not a beginner setup task and it does not authorize real use.
Course 2 teaches client discovery and assessment; Course 3 teaches how to
prepare and govern a supervised pilot.
