# Course Overview — From a Small and Medium-sized Enterprise (SME) Problem to a Controlled Demonstration

## Target learner

This course is for a learner who:

- wants to move towards artificial intelligence (AI) workflow implementation
  consulting for Dutch SMEs;
- may have no coding, **command-line** experience with typed computer
  instructions, **automation** experience with software performing repeatable
  steps, or **application programming interface (API)** experience with defined
  software-to-software requests and responses;
- is willing to learn one small concept at a time and verify observed results;
- wants a foundation that remains useful when AI products change;
- accepts that **production consulting**—work on systems used in real daily
  business operations—requires later courses and real delivery experience.

## Course promise

You will take one fictional, low-risk administrative process from an unclear
problem to a tested, documented, human-controlled demonstration.

You will not merely assemble an automation. You will produce the evidence a
responsible implementation consultant needs:

- why this problem was selected;
- what the current process costs or delays;
- what is **authoritative data**, meaning the agreed official source, and what
  is not;
- which steps are rules, AI, or human judgment;
- how failures become visible;
- what the workflow does when AI is unavailable;
- who reviews the output;
- whether the measured result supports `ACCEPT FOR SYNTHETIC PORTFOLIO`,
  `REWORK`, or `DO NOT CONTINUE`;
- how another person could operate and stop it.

All three final decisions can pass when supported by evidence.
`ACCEPT FOR SYNTHETIC PORTFOLIO` means only that the fictional demonstration
is suitable to show as portfolio evidence. No Course 1 outcome authorizes a
client pilot, real data, production use, or an external action.

## The practice method

Every foundation and module first demonstrates the skill with exact actions,
then asks you to recreate it with different fictional material. **Codex** is
the course workspace assistant you are using now. Each lesson ends with a
copy-and-paste Codex prompt for **read-only** inspection, which allows Codex to
inspect and explain the one practice folder you name but not change it, plus an
objective pass checklist.

The sequence is deliberate:

```text
follow the worked example
  → compare your result with the expected result
  → recreate the skill with different fictional material
  → ask Codex to inspect only that folder without changing it
  → correct your own work until the pass criteria are met
```

You never have to guess what a finished exercise should look like. Codex may
explain and inspect; you perform the recreation and corrections.

## Role boundary after completion

**Synthetic data** means fully fictional practice information rather than data
copied from real people or work. A **bounded workflow** has a clear start, end,
scope, and owner. A **risk and tool-fit pre-screen** is an early check for
obvious safety concerns and whether existing software already fits the need.

| Capability | After Course 1 |
|---|---|
| Explain a bounded workflow | Yes |
| Build and test with synthetic data | Yes |
| Produce a portfolio case study | Yes |
| Run a basic risk and tool-fit pre-screen | Yes |
| Offer legal or compliance conclusions | No |
| Process real client data independently | No |
| Deploy a production integration—a live connection between real business systems—independently | No |
| Configure regulated platforms—systems subject to formal legal or industry controls—professionally | No |
| Call yourself an experienced consultant | No |

The career roadmap in the progressive web app (PWA), an installable website
that works like an app, shows how later courses close these gaps.

## Learning design

The course uses three layers.

### Layer 1 — Beginner foundations

The foundations teach enough technical literacy to understand and supervise a
small workflow:

1. files and plain text;
2. command-line survival;
3. code and Python, a beginner-friendly programming language;
4. web application programming interfaces (APIs) and JavaScript Object
   Notation (JSON);
5. Git—a version-control tool that records file changes—and safe changes;
6. spreadsheets, comma-separated values (CSV) files, and data quality;
7. AI and controlled workflows;
8. safe AI-assisted building;
9. workflow tools and data stores.

### Layer 2 — Nine project modules

Each module adds one consultant capability and one **capstone** increment. The
capstone is the final combined project.

Terms used in the evidence table:

- an **as-is map** shows the process as it works now; a **stakeholder map**
  names the people and groups affected; and a **manual baseline** records
  current volume, time, errors, and rework before automation;
- a **scorecard** compares options using stated criteria; an **intended
  purpose** states exactly what the workflow should and should not do; and a
  **module selection decision** records whether to select a synthetic proof,
  investigate further, or discard that opportunity;
- a **data dictionary** explains every field; a **data contract** states
  required fields, formats, and allowed values; and **expected issues** are the
  known correct answers used to test detection;
- a **rule-first workflow** uses fixed ordinary code before optional AI, while
  **failure tests** confirm that expected problems are visible;
- a **bounded summary** may discuss only supplied facts and verified issue
  identifiers; a **review package** groups the draft, sources, and controls a
  human needs to decide;
- an **approval lifecycle** names review stages such as pending, approved, and
  expired; a **local outbox** stores drafts without sending them; and a **data
  flow** shows where information enters, moves, and leaves;
- a **risk screen** is an early check for obvious safety or legal concerns; a
  **tool-fit decision** compares the need with available software; and a
  **regression report** confirms that previously passing cases still pass;
- **user acceptance testing (UAT)** lets intended users check that the workflow
  meets their needs, while a **runbook** gives operating, stopping, and recovery
  instructions.

| Module | Consultant capability | Main evidence |
|---:|---|---|
| 1 | Observe before proposing | As-is map, stakeholder map, manual baseline |
| 2 | Select and bound a worthwhile opportunity | Scorecard, intended purpose, module selection |
| 3 | Identify authoritative data and rules | Data dictionary, contract, expected issues |
| 4 | Build reliable logic without AI | Rule-first workflow, to-be map, architecture diagram, and failure tests |
| 5 | Add AI only where it helps | Bounded summary supported by issue identifiers (IDs) |
| 6 | Preserve meaningful human control | Review package, approval lifecycle, local outbox |
| 7 | Screen risk and existing-tool fit | Data flow, risk screen, tool-fit decision |
| 8 | Evaluate utility and value | Regression report and evidence-backed Course 1 decision |
| 9 | Prepare people and handover | UAT evidence, runbook, training, change log, and demonstration |

### Layer 3 — Capstone acceptance

The final demonstration is assessed on discovery, data and rules, bounded AI,
human control, Dutch SME **guardrails** (stated limits that prevent unsafe
use), evaluation, adoption, and handover.

## The fictional scenario

**Besloten vennootschap (BV)** is Dutch for a private limited company.
`Northstar Services BV` is a fictional Dutch business-to-business (B2B) service
company. Its operations team exports a weekly work-item **register**, a table
used to track tasks, from an imaginary business system. The register contains
deliberately designed normal cases and **defects**, meaning intentional errors
for the learner to find.

No company, customer, employee, or person in the data is real.

The learner must detect and explain issues such as:

- a missing owner;
- an overdue open item;
- duplicate IDs or references;
- an unsupported status;
- impossible or contradictory dates;
- a required review without evidence;
- a **stale record** that has not been updated when expected;
- **malformed input** whose structure is invalid;
- **untrusted text** attempting to influence the AI step.

## Rule-first allocation

A **deterministic** piece of code produces the same result whenever it receives
the same input.

| Task | Default owner |
|---|---|
| Required fields, dates, duplicates, allowed statuses | Deterministic code |
| Whether a flagged item needs business action | Human reviewer |
| Plain-language grouping of already verified issues | Optional AI |
| Compliance, legal, employment, credit, or clinical judgment | Excluded / specialist |
| Sending or updating another system | Excluded in Course 1 |

If AI is removed, the exception report must still work.

## Evidence habit

Every module produces a required **artifact**, meaning a file that proves what
you did. Windows setup creates one project **repository**, meaning a project
folder tracked by Git. Every Module 1–9 artifact belongs in that repository,
not in the foundation practice folder and not inside the PWA source files used
to build the course reader.

In the suggested structure below, `README.md` (“read me”) is the main
instruction file written in Markdown (`.md`); `data` holds input; `docs` means
documents;
`prompts` holds AI instructions; `src` means source code; `tests` holds
automated checks; `output` holds generated results; and `evidence` holds proof
of completed work:

```text
operations-exception-assistant/
  README.md
  CAPSTONE_INDEX.md
  CHANGELOG.md
  data/
  docs/
  prompts/
  src/
  tests/
  output/
  evidence/
    module-01/
    module-02/
    module-03/
    module-04/
    module-05/
    module-06/
    module-07/
    module-08/
    module-09/
```

The exact Windows location is
`Documents\AI-workflow-learning\operations-exception-assistant`. Foundations
remain in `Documents\controlled-ai-course-practice` because they are isolated
skill exercises. Do not create a second module project. Each module shows how
to save its files under `evidence\module-NN` and make a Git checkpoint only
after that module passes.

Do not store **secrets**—passwords, keys, or other access-granting values—or
real data in Git.

## Gates, not calendar pressure

Each **gate** is a pass checklist that must be satisfied before you continue.
The 140–180 hour estimate is a planning range, not a deadline. The additional
time covers following a worked example, recreating the skill independently,
and correcting your own work after read-only review.

At roughly 20 hours per week, a literal beginner may need 7–10 calendar weeks.
At 8–10 hours per week, 16–23 weeks is more realistic. Stop when:

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

- **parsing**, meaning reading a file's structure with software, for Portable
  Document Format (PDF) and Microsoft Word document (`.docx`) files;
- optical character recognition (OCR), software that extracts text from images,
  and page-level evidence locators that point back to an exact source page;
- **retrieval**, which finds relevant stored content, and **vector databases**,
  which find mathematically similar content;
- production APIs and **multi-tenant databases**, in which one service keeps
  several customers' data separated;
- **Open Authorization (OAuth) connectors**, integrations that use delegated
  account permission, and **external write-back**, which changes data in another
  system;
- **production security architecture**, the design that protects a live system;
- advanced legal and vendor assessments;
- regulated platform configuration;
- **autonomous agents**, which can choose and perform several actions with
  limited supervision.

Deferring these topics is sequencing, not deletion. The Career Path tab shows
where they return.

## Course boundary and valid final decisions

A consultant is paid for judgment, not for forcing AI into every process.
Course 1 ends with exactly one of these evidence-backed decisions:

- `ACCEPT FOR SYNTHETIC PORTFOLIO`: package the controlled fictional
  demonstration as portfolio evidence;
- `REWORK`: record the gaps, corrective plan, and evidence needed for another
  Course 1 review;
- `DO NOT CONTINUE`: close the fictional project safely and record why.

All three can pass. A well-supported `DO NOT CONTINUE` decision may show that:

- existing software already solves the problem;
- the baseline is too small to justify the effort;
- data quality is too weak;
- the failure consequence is too high;
- the proposed AI step adds no measurable value;
- the organization cannot yet own or support the workflow.

Course 2 teaches client discovery and a paid assessment without promising an
implementation. Course 3 teaches how to design, authorize, and govern a
supervised pilot. Course 1 never transitions from synthetic data to a client
test.
