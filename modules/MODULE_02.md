# Module 2 — Select and Bound a Worthwhile Opportunity

Lesson ID: `course-1-module-02`
Revision: 2026-07-26

## Outcome

You will decide whether a workflow opportunity is suitable for a small,
controlled first implementation. You will define its intended purpose,
negative scope, expected value, success measures, owner, and stop conditions.

You are not trying to find the most impressive use of AI. You are selecting a
repeatable business problem that can be tested safely and reversed easily.

For the capstone, you will justify why an internal exception report based on
synthetic operational data is a better first project than an autonomous agent
that changes records, contacts customers, selects suppliers, or makes decisions
about people.

## Beginner checkpoint

Complete the Module 1 test gate. You should have an as-is process map and an
honest manual baseline.

Before continuing, explain:

- the difference between a problem and a proposed solution;
- the difference between an internal draft and an external action;
- why frequent, rule-based, reversible work is usually easier to pilot than a
  rare, high-consequence decision;
- why “we could use AI” is not evidence of business value.

The selection exercise is synthetic. It is not permission to test a workplace
process or process real data.

## Concepts

- **Opportunity:** a defined process improvement that may produce a measurable
  benefit.
- **Intended purpose:** who uses the system, in which context, with which input,
  for which bounded function and output.
- **Negative scope:** uses, data, users, and actions explicitly excluded.
- **Consequence:** what could happen if an output is late, wrong, misleading,
  disclosed, or acted on.
- **Reversibility:** how easily a person can stop the workflow and restore the
  previous way of working.
- **Data readiness:** whether permitted, sufficiently consistent input is
  available for testing and operation.
- **Rule clarity:** whether an authorised owner can state and approve the rules.
- **Value hypothesis:** a measurable benefit to test, not a promised return.
- **Sponsor:** the person who can provide resources and accept the project.
- **Process owner:** the person accountable for how the work should operate.
- **User:** the person doing or reviewing the work. One person may fill several
  roles in a small business, but the responsibilities still need names.
- **Scope change:** a requested change to purpose, data, user, output, or action
  that requires reassessment.

## Official readings

1. [CBS: use of AI technology by Dutch microbusinesses](https://www.cbs.nl/nl-nl/longread/rapportages/2026/gebruik-van-ai-technologie-door-nederlandse-microbedrijven?onepage=true)
   gives current Dutch evidence about adoption, common purposes, and barriers.
   Notice that lack of experience and privacy concerns matter; do not infer that
   AI itself causes higher productivity.
2. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
   describes intended purpose, context, users, impacts, limitations, and
   go/no-go decisions as part of mapping risk.
3. [European Commission: AI Act risk-based approach](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
   gives an official overview of prohibited, high-risk, transparency, and
   minimal-risk uses.
4. [European Commission: GDPR processing principles](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en)
   explains purpose limitation, minimisation, accuracy, storage limitation, and
   accountability.

The capstone exclusions below are deliberately conservative learning
boundaries. They are not a legal opinion or a declaration that every other use
is prohibited. A real client may require legal, privacy, security, sector, and
works-council review.

## Guided build

### 1. Apply the hard-stop screen

For this first course, reject an opportunity if it requires any of the
following:

- real or pseudonymised production data;
- personal, health, biometric, criminal-conviction, or other sensitive data;
- decisions about employment, education, credit, insurance, benefits,
  healthcare, policing, migration, or access to an essential service;
- diagnosis, treatment, dosing, safety-critical control, or legal advice;
- profiling, ranking, or scoring a person;
- supplier selection, contract acceptance, payment, or purchase approval;
- automatic external messages or source-system changes;
- a hidden AI interaction;
- a result for which no person has review authority;
- operation without a safe manual fallback.

This does not mean such work can never be done. It means it is unsuitable for
an absolute beginner's first independent implementation.

The Synthetic SME Operations Exception Assistant passes this screen because it
uses fictional non-personal data, prepares an internal draft, preserves source
records, and leaves judgement and correction to a human.

### 2. Compare three candidate opportunities

Score each candidate from 0 to 2 on the criteria below:

- **0:** poor or unknown;
- **1:** partly suitable or dependent on an assumption;
- **2:** clearly suitable with evidence.

| Criterion | Candidate A: general AI email responder | Candidate B: synthetic operations exception report | Candidate C: automatic approval and payment |
|---|---:|---:|---:|
| Repeated often enough to measure | | | |
| Clear business outcome | | | |
| Permitted and available data | | | |
| Rules can be approved | | | |
| Low consequence if wrong | | | |
| Easy human review | | | |
| Easy to stop and reverse | | | |
| Manual fallback exists | | | |
| Can test with representative synthetic cases | | | |
| Named owner and user | | | |
| **Total out of 20** | | | |

For every score, add one short evidence note and a confidence level. Do not use
the total to hide a hard stop. A candidate with a legal, privacy, safety, or
authority blocker remains stopped even if its numerical score is high.

Candidate B should be selected for the course. If your scoring selects another
candidate, explain which assumption caused the difference and recheck the
hard-stop screen.

### 3. Write the problem without naming a tool

Use this format:

> When [trigger], [user role] currently [manual work] in order to [business
> outcome]. The present process causes [observed delay, effort, error, or lack
> of visibility], evidenced by [baseline]. We will test whether a controlled
> assistant can improve [metric] without [unacceptable outcome].

For this capstone, the problem is the repeatable manual effort needed to find
and present possible issues in an operational register. The problem is not
“the company does not have an AI agent.”

### 4. Define intended purpose and negative scope

Use this course purpose statement:

> The system assists an operations coordinator at a fictional Dutch SME by
> reading the supplied synthetic work-item register, applying approved
> deterministic checks, and preparing an evidence-linked internal exception
> report. A later bounded AI step may rewrite only the already-established
> issues into plain language. A human reviews the report. The system does not
> change source records, decide how to resolve an issue, rank people or
> suppliers, send messages, approve work, enter a contract, or make a payment.

Write the following scope elements separately:

| Scope element | In scope | Out of scope |
|---|---|---|
| User | fictional operations coordinator and reviewer | customers, suppliers, public users |
| Input | supplied synthetic CSV-style work-item data | emails, free-form documents, real exports |
| Function | validation, deterministic issue detection, internal draft | prediction, recommendation, autonomous decision |
| Output | evidence-linked internal exception report | external communication, approval, write-back |
| Environment | local learner project | production or employer systems |
| Data | fictional non-personal operational records | personal, confidential, regulated, or client data |

Add foreseeable misuse: for example, a manager might treat severity as a
performance rating or send the draft without checking it. State how the design
will discourage that misuse.

### 5. Define a value hypothesis

Use your measured Module 1 baseline. Keep value calculations simple and label
them as scenarios:

```text
monthly hours on the check
  = runs per month × manual active minutes per run ÷ 60

possible monthly labour capacity released
  = monthly hours × tested percentage reduction in active time
```

Do not yet enter an invented percentage reduction. Record it as “to be tested.”
Also record costs and burdens that could cancel the benefit:

- implementation and configuration time;
- subscriptions or usage charges;
- human review time;
- exception correction;
- training and support;
- monitoring and maintenance;
- vendor or policy changes;
- incident handling and fallback operation.

Time released is not automatically cash saved. A useful project may instead
increase capacity, consistency, visibility, or response speed. Say which claim
you intend to test.

### 6. Set provisional success and failure measures

Write measures before implementation. Use provisional thresholds and state
that Module 8 will confirm or revise them.

| Claim to test | Measure | Provisional threshold | Evidence |
|---|---|---:|---|
| Rules are implemented faithfully | expected issues found by correct rule code | 100% on frozen synthetic test data | comparison report |
| The report is traceable | reported issues with work item, field, and rule code | 100% | report inspection |
| The assistant does not invent issues | unsupported report issues | 0 | reviewer check |
| Control is preserved | automatic messages, approvals, payments, or write-backs | 0 | workflow and run log |
| The process is more usable | matched manual versus assisted active time and user feedback | improvement to be tested | timed UAT |
| The fallback works | stopped run can be completed manually | 100% of fallback drill | runbook record |

Do not choose “AI accuracy” as a single vague metric. Measure the specific
claim and the consequence of failure.

### 7. Name change triggers

The following requests reopen scope and require a new risk, privacy, authority,
value, and test review:

- replacing synthetic data with real data;
- adding a new field or source;
- changing rules or severity;
- adding another user group;
- producing customer-facing text;
- writing to another system;
- sending, approving, ordering, paying, ranking, or deciding automatically;
- changing the configured AI provider or important generation settings.

“The technology can do it” is not approval for a scope change.

## Consultant lens

The first consulting deliverable is often a diagnostic, not an automation.
Useful diagnostic work includes:

- observing a real process with permission;
- measuring volume, active time, delay, rework, and error;
- locating authoritative data and rules;
- identifying control and privacy constraints;
- comparing improvement without AI, bought software, configured workflow, and
  custom build;
- recommending go, small pilot, redesign first, or stop.

A responsible “do not automate yet” conclusion can save a Dutch SME more money
than an attractive demo. The opportunity score is a conversation aid, not a
scientific formula. Keep the evidence notes so a client can challenge your
judgement.

Do not market a value hypothesis as guaranteed savings. For a paid engagement,
agree who owns the baseline, assumptions, costs, and acceptance decision.

## Capstone increment

The capstone now has:

- a documented go decision;
- a selected low-consequence internal workflow;
- an intended-purpose statement;
- explicit negative scope and misuse cases;
- named user, reviewer, owner, input, output, and environment;
- a value hypothesis;
- provisional success measures;
- change triggers and stop conditions.

The exception checks remain deterministic. AI is not being used to discover
facts, decide severity, or take action.

## Required artifact

Create `artifacts/opportunity_brief.md` in your learner project.

It must contain:

1. the completed hard-stop screen;
2. the three-candidate scorecard with evidence and confidence notes;
3. the tool-neutral problem statement;
4. the intended-purpose statement;
5. the in-scope/out-of-scope table;
6. foreseeable misuse and protections;
7. the value hypothesis, including costs and uncertainties;
8. provisional success and failure measures;
9. the process owner, user, reviewer, sponsor, and fallback owner;
10. scope-change triggers;
11. a dated decision: `GO`, `REDESIGN FIRST`, or `STOP`, with reasoning.

## Test gate

Pass only when:

- [ ] The opportunity passes every course hard stop.
- [ ] The problem statement contains no product or model name.
- [ ] Intended purpose names the user, context, input, function, output, review,
      and limitations.
- [ ] Negative scope explicitly excludes external action and source write-back.
- [ ] Each score has evidence or is marked unknown.
- [ ] Value is labelled as a hypothesis, not a forecast or guarantee.
- [ ] Costs, review effort, maintenance, and fallback are included.
- [ ] Success measures have a numerator, denominator, threshold, and evidence
      source, or clearly say what still needs defining.
- [ ] A scope change cannot silently expand the workflow.
- [ ] The selected course opportunity is the synthetic internal exception
      report.

Give the brief to another person or an AI tutor with no additional context.
Ask them to list what the system is and is not allowed to do. If their answer
differs from yours, the boundary is not clear enough.

## Stop or rework

Stop or return to Module 1 when:

- the pain point is only an opinion and has no observation or baseline;
- there is no process owner or reviewer;
- real or sensitive data is required to demonstrate the idea;
- the proposal affects rights, safety, employment, health, credit, or access to
  essential services;
- the first version must send, pay, approve, or write to a source system;
- a safe manual fallback does not exist;
- the proposed value depends entirely on eliminating human review;
- the work is too rare or inconsistent to test;
- existing software or a simple process correction has not been considered;
- a stakeholder cannot agree on the authoritative rules.

## Common failures

- Choosing a flashy demo rather than a measured operational problem.
- Treating all spreadsheet work as suitable for AI.
- Giving numerical scores without evidence notes.
- Allowing a high total score to override a hard stop.
- Writing “employees will save 80%” before a matched test exists.
- Forgetting implementation, review, subscription, training, and maintenance
  costs.
- Using AI to interpret a rule that can be written exactly.
- Calling a draft “safe” while allowing it to be sent automatically.
- Describing human review without naming the reviewer's authority.
- Expanding from one register to every company process.

## Estimated time

6–8 hours:

- 1.5 hours for readings and the hard-stop screen;
- 1.5 hours for the candidate comparison;
- 2 hours for purpose, boundaries, misuse, and change triggers;
- 1 hour for value and measurement design;
- 1 hour for the test gate;
- up to 1 additional hour for rework after an independent clarity check.
