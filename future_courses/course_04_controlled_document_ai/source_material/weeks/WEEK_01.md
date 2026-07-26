# Week 1 — Process, Purpose, and State Design

## Outcome

You will define a small, testable supplier-document process before writing automation. You will know what enters, what is produced, what the AI may do, what only deterministic code or a human may do, and how every run can safely end.

## Beginner checkpoint

Complete the [foundation gate](../foundations/README.md#foundation-gate) first.
For this week, revisit
[AI and document workflows](../foundations/06_AI_AND_DOCUMENT_WORKFLOWS.md).
No coding is required until the repository setup at the end. A state machine is
just a list of allowed stages and the rules for moving between them.

Before continuing, explain in your own words: intended purpose, deterministic
versus probabilistic, state, transition, invariant, and manual fallback. Use the
[glossary](../foundations/GLOSSARY.md) rather than guessing.

Safe AI-assistance request:

```text
Act as a tutor. Ask me one question at a time about the manual supplier-review
process. Help me distinguish observations, assumptions, AI tasks, rule-based
tasks, and human decisions. Do not design code or expand the stated scope.
```

## Concepts

- **Intended purpose:** the precise use, user, context, input, output, and limitation of the system.
- **As-is versus to-be:** observe the manual process before designing the assisted one.
- **Unit of work:** one supplier review case, containing at most a quotation, terms, and the shared internal policy.
- **Control point:** a place where a rule, test, or reviewer may stop progression.
- **Probabilistic versus deterministic:** language interpretation can be probabilistic; authorization, calculations, hashes, and state changes are deterministic.
- **State machine:** a finite set of named states and allowed transitions.
- **Invariant:** a condition that must always remain true.
- **Manual baseline:** observed time and quality against which the assisted workflow will later be compared.
- **Negative scope:** explicit exclusions that prevent the project from drifting into consequential or sensitive use.

## Official readings

Read for engineering principles, not memorisation:

1. [European Commission: GDPR data-processing principles](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en) — purpose limitation, minimisation, accuracy, storage limitation, security, accountability.
2. [European Commission: data protection by design and by default](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations/what-does-data-protection-design-and-default-mean_en) — translate safeguards into architecture from the start.
3. [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — read the Govern, Map, Measure, and Manage framing.
4. [`ARCHITECTURE_AND_CONTRACTS.md`](../ARCHITECTURE_AND_CONTRACTS.md) — this course’s normative contracts and state machine.

Record each reading in your source log: URL, access date, relevant claim, and whether it is law, guidance, or a technical recommendation.

## Guided build

### 1. Perform the manual task twice

Select two simple cases from the supplied corpus. Start a timer. Without AI:

1. open the quotation and terms;
2. record supplier name, quote reference/date, currency, line items, subtotal, discount, VAT, total, delivery, payment terms, validity, warranty, termination, and governing law;
3. identify missing or conflicting information;
4. compare relevant facts with the internal policy;
5. draft a neutral review memo that does not recommend a supplier;
6. self-check every assertion against a source.

Record:

- active hands-on minutes;
- elapsed minutes;
- corrections made;
- required fields correct against the supplied gold answer;
- memo assertions with valid evidence;
- unresolved uncertainty.

Do not optimise the second run merely to manufacture a favorable baseline. Describe any learning effect.

### 2. Draw the as-is process

Use [`../templates/process_and_purpose_worksheet.md`](../templates/process_and_purpose_worksheet.md). Include:

- trigger and completion;
- people and systems;
- files, copies, and handoffs;
- decisions and calculations;
- waiting time;
- error/rework loops;
- current evidence trail;
- current fallback.

Mark observed facts separately from assumptions.

### 3. Write the intended purpose

Use this form:

> The system assists a trained internal reviewer at a fictional small organisation by extracting and organising commercial facts from a supplier quotation and terms, checking deterministic calculations and stated policy conditions, and drafting a source-cited review memo. It does not select, rank, recommend, contact, contract with, or pay a supplier. A human reviews the source evidence and exact proposed output before any draft-only follow-up action.

Adapt it only within the course boundary. Add:

- authorised user;
- document types;
- output;
- data type;
- environment;
- expected benefit;
- foreseeable misuse;
- exclusions;
- conditions that force manual handling.

### 4. Allocate each task

Create a table with columns:

```text
task | AI | parser/OCR | deterministic rule | human | reason | failure route
```

Required allocations:

- source acceptance, hash, duplicate check: deterministic;
- text/table candidate extraction: parser/OCR;
- commercial-field interpretation: AI plus evidence;
- arithmetic and policy thresholds: deterministic;
- ambiguity/conflict resolution: human;
- memo wording: AI draft plus evidence validation;
- supplier decision: outside system/human;
- approval validity and action: deterministic.

If “AI” is the only marked column for a consequential step, redesign it.

### 5. Specify the state machine

Copy the course states:

```text
received
validated
parsed
needs_review
pending_approval
approved
rejected
expired
completed
failed_manual
```

For every allowed transition, write:

- initiating event;
- required preconditions;
- database transaction;
- audit event;
- timeout;
- retry rule;
- forbidden transitions;
- human-facing message.

Write tests in plain English first. Examples:

- Given a corrupt PDF in `validated`, parsing failure moves it to `failed_manual`.
- Given a memo in `pending_approval`, editing one character changes its hash and prevents `approved → completed`.
- Given a duplicate source hash, intake creates a duplicate audit event but no second action.

### 6. Create the repository and evidence habit

Create the repository structure from [`../COURSE_OVERVIEW.md`](../COURSE_OVERVIEW.md). Add:

- intended purpose;
- process map;
- allocation table;
- state-transition table;
- baseline results;
- a decision record explaining why supplier recommendation is excluded.

Commit with a message such as:

```text
docs: define bounded supplier review workflow
```

## Capstone increment

The capstone has a frozen boundary, manual baseline, and testable lifecycle. Assign IDs:

- process: `PROC-SUPPLIER-REVIEW-001`;
- intended purpose: `PURPOSE-001`;
- state-machine version: `STATE-001`;
- baseline runs: `BASE-001` and `BASE-002`.

Choose the two baseline cases before looking at their gold answers. Keep their result sheets; Week 11 repeats matched cases.

## Required artifact

`artifacts/weekly/week-01/` must contain:

- completed process and purpose worksheet;
- as-is map;
- AI/parser/rule/human allocation table;
- state transition table;
- 12 or more plain-language invariant/transition tests;
- baseline timing and quality record for two cases;
- architecture decision record for negative scope;
- weekly evidence record.

## Test gate

Pass only if:

- a reader can identify the exact beginning and end of one case;
- all ten named states have an entry rule and terminal/follow-on behaviour;
- no supplier choice or external action is delegated to AI;
- every failure condition has a named safe state;
- approval invalidation after editing is explicit;
- baseline quality was checked against gold answers after completion;
- exclusions cover all forbidden data/use cases in the course overview;
- another person can explain the workflow from your artifacts without asking what “done” means.

Run a 15-minute tabletop exercise: draw three random failure cards—duplicate upload, corrupt file, altered approved output, provider outage, missing terms, conflicting total—and trace each to a named state.

## Common failures

- **Starting with a tool canvas:** return to the observed process and unit of work.
- **Vague purpose (“process supplier documents”):** add actor, inputs, output, limits, and context.
- **Treating `needs_review` as a terminal dumping ground:** define reviewer options and evidence shown.
- **Using confidence as authorization:** require observable evidence and deterministic approval rules.
- **Baseline without quality:** time alone rewards fast mistakes; score correctness and citation support.
- **Happy-path-only states:** use the supplied corpus categories to force failures into the design.
- **Scope creep into recommendation:** the memo reports facts, conflicts, policy implications, and open questions; it does not rank suppliers.

## Estimated time

| Activity | Time |
|---|---:|
| Official readings and notes | 1.25 h |
| Two manual baseline cases | 2.0 h |
| As-is map and intended purpose | 1.5 h |
| Allocation and state design | 2.0 h |
| Tabletop tests and revision | 1.25 h |
| Evidence packaging and reflection | 0.75 h |
| **Total** | **8.75 h** |
