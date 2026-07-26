# Foundation 7 — AI and Controlled Workflows

## Outcome

You can decide whether a workflow step belongs to an exact rule, an AI model,
or an authorised person. You can explain why AI output is a candidate—not a
fact or decision—and design a bounded path for uncertainty, review, and
failure.

## Start with the work, not the model

An AI implementation begins with an observed process:

- What starts one unit of work?
- What information is available?
- Which steps follow fixed rules?
- Which steps require interpretation?
- Who has authority to decide or act?
- What evidence must remain afterwards?
- How does work continue when a tool fails?

Do not begin with “Where can we add an agent?” A bad or unnecessary process does
not become valuable because AI performs it faster.

Write a bounded intended purpose:

> This workflow assists [authorised user] with [specific task] using [allowed
> input] to produce [bounded output]. It does not [excluded decisions or
> actions]. [Role] reviews [evidence] before [consequential step].

If that sentence cannot be made specific, the workflow is not ready to build.

## Three kinds of responsibility

Allocate each step deliberately:

| Best owner | Suitable work | Example |
|---|---|---|
| Deterministic rule or code | exact, repeatable checks and calculations | required field, allowed status, overdue date, duplicate reference |
| AI model | bounded interpretation or drafting where variation is expected | classify unclear text, summarise verified issues, draft an internal explanation |
| Authorised person | judgement, exception handling, accountability, or consequential decision | correct the source record, accept a residual risk, approve an external action |

The categories can work together. For example:

1. exact rules detect overdue work;
2. AI drafts a summary using only those issue records;
3. a person checks the summary against the records;
4. the system records accept, edit, reject, or escalate.

Do not use AI for a rule that can be stated exactly. Do not ask a model to
approve its own interpretation.

## What a language model does

A large language model produces candidate text or structured values based on
its instructions and supplied context. It can handle varied language, but it
does not automatically:

- know which company record is current;
- understand local authority and policy;
- distinguish a plausible claim from a supported fact;
- calculate perfectly;
- preserve the same behaviour after a model update;
- recognise confidential data unless the controls and instructions do so;
- take responsibility for an outcome.

A **hallucination** is plausible-looking output that is false or unsupported.
Fluency and confidence are presentation qualities, not evidence.

## Prompts, context, and untrusted input

A **prompt** contains instructions and context for one model request. A
**token** is a piece of text used for input/output limits and pricing.

Anything received from a document, form, email, website, or user is untrusted
input. It may be wrong, malformed, confidential, or contain text such as
“ignore all previous instructions.” That last case is a **prompt injection**.
Treat source content as data, never as authority over the workflow.

Keep these separate:

- system/developer instructions;
- permitted business rules;
- source content;
- model output;
- human decision.

Never paste employer or customer data into an AI service merely to test whether
a prompt works. Use the fictional course data until a later, formally approved
implementation establishes contracts, access, retention, and data handling.

## Structured output constrains shape, not truth

A model may be asked for a fixed shape:

```json
{
  "summary": "Three high-severity issues require review.",
  "issue_ids": ["ISS-002", "ISS-004", "ISS-009"],
  "limitations": ["No source records were corrected."]
}
```

A schema can require `issue_ids` to be an array. It cannot prove that the
listed issues exist or that “three” is the correct count.

After an AI response:

1. validate its structure;
2. reject fields or citations that do not exist;
3. recalculate counts and exact facts deterministically;
4. flag omissions, unsupported additions, and contradictions;
5. show the evidence to a reviewer;
6. record the outcome.

If a model cannot produce a valid result, route the item to a visible manual or
exception queue. Do not silently continue with partial output.

## Evidence and provenance

**Evidence** is the material that supports a claim. **Provenance** records where
data came from and how it changed.

For a spreadsheet workflow, useful evidence may include:

- source filename and export time;
- work-item ID;
- field name and observed value;
- rule code and rule version;
- issue ID;
- model and prompt version, if AI was used;
- reviewer, decision, time, and correction;
- run or trace ID connecting the records.

An AI summary should cite stable issue IDs. A reviewer should be able to move
from a sentence to the issue record and then to the relevant source row.

## A controlled workflow pattern

```text
receive an allowed synthetic input
→ preserve an untouched snapshot
→ validate file and required structure
→ run exact data-quality rules
→ route invalid or uncertain input visibly
→ optionally ask AI for a bounded draft
→ validate the draft against issue records
→ let an authorised person accept, edit, reject, or escalate
→ record the exact outcome
→ retain a manual fallback and a kill switch
```

The model is replaceable. The process definition, rule register, evidence,
review design, testing, and ownership are the durable parts.

## Levels of autonomy

Use the lowest level that produces the required value:

| Level | System behaviour | Course position |
|---|---|---|
| 0 — inform | display source data and fixed checks | safe starting point |
| 1 — draft | prepare an internal draft for review | normal AI exercise |
| 2 — prepare action | prepare an exact action but require approval before execution | later controlled pilot only |
| 3 — limited automatic action | execute a narrowly bounded, reversible, monitored action | outside this foundation |
| 4 — open-ended autonomous action | choose goals/actions broadly | not an SME starter workflow |

Greater autonomy increases the need for authority, monitoring, access control,
reconciliation, incident response, and evidence. “Human in the loop” is not a
decorative approval button: the person needs time, authority, relevant evidence,
and a usable reject/escalate route.

## Failure is a normal route

Declare what happens when:

- a required column is missing;
- a file is duplicated or too large;
- a date cannot be parsed;
- the model times out or refuses;
- output fails its schema;
- a citation refers to a missing issue;
- a reviewer edits or rejects a draft;
- the workflow tool or data store is unavailable.

Use stable reason codes, cap retries, and send unresolved work to an owned queue.
A timeout does not prove that nothing happened; reconcile before repeating a
potential action.

## Practice

Use the fictional
[`expected_issues.csv`](../practice_data/expected_issues.csv).

1. Select five issue rows.
2. Write an exact, non-AI calculation for:
   - total selected issues;
   - count by severity;
   - list of issue IDs.
3. Draft a three-sentence internal summary using only those calculated facts and
   the `expected_message` values.
4. Mark each sentence with the issue IDs that support it.
5. Add one unsupported sentence deliberately.
6. Act as reviewer: reject or remove the unsupported sentence and record why.
7. Write the manual fallback if summary generation fails.

You may perform the drafting yourself. Using a live model is optional and must
not involve real data.

## Chapter check

You pass when you can explain:

- intended purpose and negative scope;
- deterministic rule versus AI interpretation versus human authority;
- why fluent or schema-valid output can still be wrong;
- prompt injection and why source content is untrusted;
- evidence and provenance;
- meaningful human review;
- why a manual route, stable reason code, and kill switch are part of the
  workflow;
- which parts remain valuable when today’s AI tools are replaced.
