# Module 7 — Apply Dutch SME Guardrails and Choose the Right Tool

## Outcome

Produce a practical pre-screen that helps a Dutch SME decide whether to
configure an existing tool, build a small controlled workflow, rework the
process first, or stop and seek specialist review.

This module teaches implementation literacy, not legal advice.

## Beginner checkpoint

- you can draw the capstone data flow;
- you know where configuration, data, output, logs, and secrets live;
- the workflow uses synthetic data only;
- no external action exists;
- you can distinguish a course decision from a legal conclusion.

## Concepts

### Build versus buy

The first question is not “Which automation tool?” It is whether existing
processes or software already solve the problem.

### Accountability

The client remains responsible for its purpose, data, users, decisions, and
suppliers. A consultant provides implementation evidence and escalates
questions outside the agreed competence.

### Data minimisation

Use only fields necessary for the intended purpose. Convenience is not a
reason to copy an entire database into a model prompt.

### AI role and use-case triage

Identify who provides and who deploys the AI system, what the system does, who
is affected, and whether the use may fall into a prohibited, high-risk, or
otherwise regulated category. Do not classify a real use case legally without
qualified review.

### Ownership

A workflow without a process owner, technical owner, reviewer, budget, and
fallback is not ready for a pilot.

## Official readings

- [Autoriteit Persoonsgegevens — Verantwoordingsplicht](https://autoriteitpersoonsgegevens.nl/nl/onderwerpen/algemene-informatie-avg/verantwoordingsplicht)
- [AP — AVG-randvoorwaarden voor generatieve AI](https://autoriteitpersoonsgegevens.nl/system/files?file=2025-05%2FAVG-Randvoorwaarden+voor+generatieve+AI.pdf)
- [European Commission — Navigating the AI Act](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act)
- [European Commission — AI literacy Q&A](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers)
- [NCSC and DTC digital resilience principles](https://www.ncsc.nl/nieuws/ncsc-en-dtc-lanceren-gezamenlijke-basisprincipes-voor-digitale-weerbaarheid)
- [Microsoft Copilot Studio agent flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview)
- [Google Workspace Studio](https://workspace.google.com/blog/product-announcements/introducing-google-workspace-studio-agents-for-everyday-work)

Run the evergreen audit for current legal guidance and product capability.

## Guided build

### 1. Write the intended purpose

Use one sentence:

> Help an internal operations reviewer find deterministic data-quality
> exceptions in a fictional weekly work-item export and read a draft summary.

Then list exclusions:

- no compliance decision;
- no employee or customer judgment;
- no external action;
- no real data;
- no source-system update;
- no autonomous prioritization.

### 2. Map the data flow

For each step, record:

- data category;
- source;
- destination;
- purpose;
- owner;
- access;
- storage;
- retention;
- deletion;
- provider/subprocessor;
- location or transfer question;
- log content.

For Course 1, all data remains fictional and local except the optional live AI
call containing verified synthetic issues.

### 3. Run the personal-data screen

Ask:

- Is any person identifiable directly or indirectly?
- Are employee, customer, patient, financial, location, or behavioral fields
  present?
- Is special-category or criminal-offence data present?
- Can free text unexpectedly contain personal data?
- Is each field necessary for the stated purpose?

For the supplied course data the answer is synthetic/no real personal data.
Document the evidence; do not merely tick a box.

### 4. Run the consequence screen

Stop and escalate if a proposed real workflow affects:

- employment or worker management;
- credit, insurance, housing, or essential services;
- education admission;
- healthcare or clinical care;
- policing, migration, or justice;
- biometric identification;
- safety-critical operations;
- another consequential decision about a person.

Course 1 excludes all of these.

### 5. Inspect existing capabilities

Create a tool-fit table:

| Candidate | Already owned? | Meets rule checks? | Human review? | Logging? | Data location? | Recurring cost? | Owner? |
|---|---:|---:|---:|---:|---|---:|---|
| Current line-of-business system | | | | | | | |
| Spreadsheet/report | | | | | | | |
| Microsoft option | | | | | | | |
| Google option | | | | | | | |
| n8n + Python | | | | | | | |
| No automation / process fix | | | | | | | |

The correct answer may be a saved report, better required fields, staff
training, or configuration.

### 6. Review vendor and access questions

Ask:

- Who contracts with the vendor?
- Who is controller, processor, or subprocessor?
- Is customer content used for provider improvement?
- What retention and deletion controls exist?
- Where is data processed?
- Is MFA available?
- Who can create credentials?
- What scopes are required?
- What audit information exists?
- How are incidents and model changes communicated?
- What happens when the service is unavailable or cancelled?

Record unknown answers as blockers, not assumptions.

### 7. Set the minimum security baseline

For a future low-risk pilot require:

- client-owned accounts and tenant;
- least-privilege access;
- MFA;
- secrets outside workflow exports and source control;
- restricted logs;
- dependency and change records;
- manual fallback;
- backup and recovery ownership;
- incident contact and kill switch.

Course 1 demonstrates the concepts locally; it does not prove production
security.

### 8. Record total ownership and cost

Include:

- platform subscription;
- model usage;
- implementation time;
- review time;
- support and monitoring;
- training;
- failure and rework;
- vendor change;
- exit or migration.

Do not compare only API token prices.

### 9. Decide

Choose and justify:

- `CONFIGURE EXISTING TOOL`;
- `PROCESS FIX FIRST`;
- `BUILD CONTROLLED PROTOTYPE`;
- `SEEK SPECIALIST REVIEW`;
- `STOP`.

## Consultant lens

Ask:

- Who owns the process and budget?
- What does the existing license already include?
- Which data cannot leave the current environment?
- Which specialists must sign off?
- Who supports the workflow after handover?
- What would make the organization stop the pilot?

Request:

- current architecture and approved-tool inventory;
- information-security and privacy contacts;
- vendor agreements and data documentation;
- retention schedule;
- access model;
- incident process;
- existing reports and automation.

Do not request confidential material during an initial market interview.

Stop when:

- no accountable owner exists;
- lawful use of data is unresolved;
- access cannot be limited;
- an existing safe feature makes custom work unnecessary;
- the consultant is expected to provide legal certification;
- the use is outside the agreed low-risk boundary.

Client-style deliverable:

- one-page risk/escalation screen and tool-fit recommendation.

## Capstone increment

Complete the supplied risk, tool-fit, and ownership worksheets for the
fictional capstone. The likely answer may still be to keep the prototype local.

## Required artifact

- `evidence/module_07_risk_screen.md`;
- data-flow map;
- minimisation table;
- build-versus-buy comparison;
- vendor/access question record;
- ownership and cost record;
- escalation list;
- implementation decision.

## Test gate

- [ ] Intended purpose and exclusions are specific.
- [ ] Every data flow and storage location is visible.
- [ ] Personal-data and consequence screens are complete.
- [ ] Existing-tool alternatives were examined.
- [ ] Unknown legal/security/vendor answers are blockers.
- [ ] Owners and recurring costs are named.
- [ ] No document claims legal compliance.
- [ ] A stop/configure/process-fix decision is allowed.

## Stop or rework

Stop if the analysis assumes:

- synthetic evidence proves real-data safety;
- a vendor's marketing page proves compliance;
- human review removes all AI Act or AVG questions;
- the client can use your personal tenant;
- a custom build is automatically more valuable.

## Common failures

- beginning vendor selection before intended purpose;
- treating all internal data as non-personal;
- forgetting free text and logs;
- evaluating token cost but not review/support;
- calling a checklist a DPIA or legal assessment;
- using “EU region” as the entire transfer analysis.

## Estimated time

10–14 hours. Real client analysis takes longer and requires appropriate
specialists.
