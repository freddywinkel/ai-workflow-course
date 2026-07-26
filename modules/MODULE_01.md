# Module 1 — Observe the Work Before You Automate

Lesson ID: `course-1-module-01`
Revision: 2026-07-26

## Outcome

You will observe and describe a small operational process before choosing any
software or AI. You will produce an evidence-based map of the current work,
separate facts from assumptions, and measure a simple manual baseline.

The practice case is entirely fictional. A small Dutch service company exports
a daily work-item register. An operations coordinator checks that register for
missing, inconsistent, and overdue items and prepares an internal exception
list. During this course, you will turn that manual check into the **Synthetic
SME Operations Exception Assistant**.

At the end of this module, you should be able to explain:

- what starts and finishes one check;
- which person performs each step;
- which file or system supplies the information;
- where waiting, correction, and uncertainty occur;
- what evidence the process leaves behind;
- how long the manual work takes.

You will not design an AI solution yet.

## Beginner checkpoint

First complete the relevant beginner foundations, especially files and text,
command-line survival, web APIs and JSON, and AI and document workflows.

In your own words, explain these terms before continuing:

- **process:** connected steps that produce an outcome;
- **record:** one item being handled, such as one work item;
- **exception:** a record that may need attention because a stated rule is not
  met;
- **source of truth:** the agreed place whose value is authoritative;
- **assumption:** something plausible that has not yet been confirmed;
- **baseline:** a measurement of the present situation used for comparison.

If any term remains unclear, use the glossary or ask an AI tutor for an
explanation and a new example. Do not ask it to complete the observation for
you.

Use only the supplied synthetic files. Do not substitute workplace exports,
client files, copied emails, names, patient data, employee data, or other real
information.

## Concepts

- **Outcome before tool:** “The coordinator knows which records need attention”
  is an outcome. “Build a chatbot” is a possible tool, not an outcome.
- **Trigger:** the event that starts the process. Here it is the availability of
  a new register export.
- **Completion condition:** the observable point at which the process is done.
  Here it is a reviewed internal exception list, not a corrected source system.
- **Unit of work:** the smallest repeatable item. In the capstone this is one
  row identified by `work_item_id`.
- **Actor:** a person or system performing a step. Use role names, such as
  “operations coordinator,” rather than invented personal names.
- **Handoff:** movement of work or information between actors or systems.
- **Active time:** time spent doing the task.
- **Wait time:** time in which the task is blocked or sitting in a queue.
- **Rework:** repeated work caused by missing, unclear, or incorrect
  information.
- **Control point:** a place where a check or reviewer can stop progress.
- **Evidence:** something that lets another person understand what happened,
  such as a row identifier, rule result, timestamp, or review decision.
- **Observed fact versus assumption:** “Row W-014 has no owner” is an
  observation. “People often forget owners because the form is confusing” is
  an assumption until investigated.

An as-is map describes what happens now, including workarounds and failures. It
is not a diagram of the system you hope to build.

## Official readings

Read for the principles; you do not need to memorise the pages.

1. [GOV.UK Service Manual: understand users and their needs](https://www.gov.uk/service-manual/service-standard/point-1-understand-user-needs)
   explains why discovery begins with the user and the problem rather than a
   preferred solution.
2. [GOV.UK Service Manual: learning about users and their needs](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs)
   distinguishes research evidence from opinions and assumptions.
3. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
   introduces the Map function: intended purpose, users, context, impacts,
   limitations, and risk must be understood before an AI system is built.

For each source, record the URL, access date, one relevant idea, and whether the
source is law, official guidance, a voluntary framework, or technical
documentation. This habit will later help you advise clients without presenting
guidance as law.

## Guided build

### 1. Set a safe observation boundary

Write this at the top of your notes:

> This exercise uses only the supplied synthetic practice data. It does not
> describe my employer, a client, or a real person. It creates no external
> message, decision, payment, or source-system change.

If you accidentally paste real information into your notes or an AI service,
stop. Remove it from your learner project, record what happened, and restart
with the synthetic files.

### 2. Understand the fictional job

The fictional operations coordinator receives
`practice_data/work_items.csv`. The coordinator:

1. keeps the original export unchanged;
2. checks whether the required values and formats are present;
3. checks combinations of values, such as status and completion date;
4. identifies open items whose due date has passed;
5. records each possible issue with the work-item identifier and affected
   field;
6. asks a human reviewer to verify the list;
7. sends nothing and changes nothing in the source system.

The final two controls are deliberate. Finding a possible issue is different
from deciding how the business should resolve it.

### 3. Perform the check manually

Open `practice_data/work_items.csv` in a plain-text editor or spreadsheet. Do
not edit or save over it. Do not open `practice_data/expected_issues.csv` yet;
that is the answer key used later.

Start a timer and inspect all rows. In a separate note, record each possible
issue using this structure:

| Work item | Field | What you observed | Why it may need attention | Confidence |
|---|---|---|---|---|
| | | | | high / medium / low |

Use the value `2026-07-26` as the reference date when deciding whether an open
item appears overdue. A fixed date makes later tests repeatable.

Record:

- total active minutes;
- interruptions or waiting;
- how many rows you inspected;
- how many possible issues you noted;
- fields that were hard to interpret;
- checks you repeated;
- points where you wanted a rule or second opinion.

Do not change your results to make them look better. Uncertainty is useful
discovery evidence.

### 4. Map the current process

Create this table and describe the manual process in enough detail that a
different beginner could repeat it:

| Step | Actor or system | Input | Work or decision | Output or evidence | Active time | Wait time | Failure or rework |
|---:|---|---|---|---|---:|---:|---|
| 1 | | | | | | | |

Include at least these stages:

1. export becomes available;
2. original file is preserved;
3. rows and fields are inspected;
4. candidate exceptions are recorded;
5. a reviewer checks the evidence;
6. the reviewed exception list is complete.

Add the current manual fallback: if the file cannot be read or a rule is
unclear, the coordinator stops and routes the item to the process owner rather
than guessing.

### 5. Separate observation from explanation

Create two lists:

- **Observed:** facts visible in the synthetic file or measured during your
  manual run.
- **Unconfirmed:** possible causes, business meanings, or user needs that would
  require an interview or an authoritative procedure.

Then write five discovery questions you would ask an operations coordinator.
Useful questions include:

- What outcome tells you this check is complete?
- Which mistakes consume the most correction time?
- Which fields have an authoritative definition?
- Which issues can wait, and which require immediate attention?
- What do you do when the export is unavailable or ambiguous?

Do not invent answers. An unanswered question is better than fabricated
evidence.

### 6. Record a manual baseline

Use a simple baseline table:

| Run | Rows checked | Active minutes | Possible issues found | Corrections to your own notes | Unresolved questions |
|---|---:|---:|---:|---:|---:|
| First full manual check | | | | | |

This first measurement does not prove a general business case. It is a starting
point that will later be compared with a matched assisted run using the same
kind of input and the same scoring rules.

## Consultant lens

A client may ask, “Can you automate our spreadsheet?” That sentence is not a
complete problem definition.

A controlled implementation consultant first asks:

- What business outcome is the spreadsheet supporting?
- Who owns the process and who has authority to approve a rule?
- How often does the work occur and at what volume?
- Where do errors and delays actually arise?
- Which system is authoritative?
- What is the present fallback?
- What would improve if the check became faster?
- What new harm could an incorrect exception list cause?

Do not copy a client's proposed solution into a proposal and label it
discovery. The valuable skill is turning messy descriptions into a process that
can be observed, bounded, tested, and handed over.

In a future client engagement, obtain permission before observing staff or
viewing data. Record role-based findings and minimise personal information.
This course does not authorise workplace research.

## Capstone increment

The capstone now has:

- a fictional user and business outcome;
- one trigger and one completion condition;
- a row-level unit of work;
- an as-is manual process map;
- an initial manual exception list;
- baseline measurements;
- unresolved questions and a manual fallback.

There is intentionally no workflow, code, AI prompt, or vendor selection yet.

## Required artifact

In your learner project, create
`artifacts/process_observation.md`. This path is illustrative; create the
folders if your course setup uses a different learner-work directory.

The artifact must contain:

1. the synthetic-only boundary statement;
2. trigger, completion condition, unit of work, user, and source of truth;
3. the step-by-step as-is map;
4. observed facts and unconfirmed assumptions in separate sections;
5. five unanswered discovery questions;
6. the manual candidate-exception list;
7. the manual baseline;
8. the current fallback and control points.

## Test gate

Pass this module only when all statements are true:

- [ ] Another beginner can follow your map without asking what happens next.
- [ ] Every candidate issue points to a `work_item_id` and field.
- [ ] The original CSV remains unchanged.
- [ ] Observations and assumptions are visibly separate.
- [ ] The baseline shows actual measured time, not an estimate.
- [ ] The trigger, completion condition, process owner, reviewer, and fallback
      are named.
- [ ] No real organisation or person is described.
- [ ] No proposed AI feature is treated as an observed need.

As a final check, explain the process aloud in two minutes without mentioning a
software product. If you cannot, simplify the map.

## Stop or rework

Stop and rework this module when:

- real, confidential, personal, health, employment, or client data entered the
  exercise;
- you cannot identify who owns or reviews the result;
- “the AI decides” appears in the current manual process;
- the map begins after the important work has already happened;
- completion is vague, such as “the spreadsheet is processed”;
- you have no measured manual run;
- you silently guessed the meaning of a field or business rule.

Record the reason for rework. In consulting, recognising insufficient evidence
is a professional result, not a failure.

## Common failures

- Drawing the future solution instead of the current work.
- Mapping only software clicks and missing conversations, waits, and
  workarounds.
- Treating the first stakeholder's explanation as complete evidence.
- Confusing a blank value with a confirmed business error.
- Counting elapsed time as active labour without distinguishing the two.
- Describing “the business” as the actor instead of a specific role.
- Measuring a specially easy run and calling it the normal baseline.
- Opening the answer key and adjusting observations to match it.
- Adding AI because the course title contains AI.

## Estimated time

6–8 hours:

- 1 hour for concepts and official readings;
- 2 hours for the manual inspection and notes;
- 2 hours for the as-is map and discovery questions;
- 1 hour for the baseline and test gate;
- up to 2 additional hours if foundational terms or the process map need
  rework.
