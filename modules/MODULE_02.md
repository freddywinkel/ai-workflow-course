# Module 2 — Select and Bound a Worthwhile Opportunity

## Outcome

You will select a small, measurable, reversible workflow opportunity and write
an intended purpose, negative scope, value hypothesis, success measures, and
stop conditions. You will learn that “do not automate this yet” can be the
correct consulting result.

## Beginner checkpoint

Start when Module 1 passes and you have a measured manual baseline. Its
evidence is recorded by **Git**, a version-control tool that records file
changes, in the one course **repository**, a project folder whose changes are
tracked together. The start state contains synthetic evidence only. You do not
need a customer, application programming interface (API), paid subscription, or
artificial intelligence (AI) model.

## Concepts

- An **opportunity** is a bounded process improvement, not a product idea.
- **Intended purpose** states the user, context, input, function, output, and
  limitation.
- **Negative scope** states what the system must not do.
- **Consequence** is what can happen when an output is wrong or misused.
- **Reversibility** is how easily a person can stop the workflow and return to
  the manual method.
- A **value hypothesis** is a benefit to test, not promised savings.
- A **hard stop** overrides a numerical score.
- A **scope-change trigger** is a proposed change that requires a new review.
- **Markdown** is a plain-text format for headings, lists, and tables; `.md` is
  its file name ending.

## Official readings

The Centraal Bureau voor de Statistiek (CBS) is Statistics Netherlands. The
United States National Institute of Standards and Technology (NIST) publishes
voluntary risk guidance. The General Data Protection Regulation (GDPR), called
the Algemene verordening gegevensbescherming (AVG) in Dutch, governs personal
data processing. These definitions are orientation, not legal advice.

1. [CBS: AI use by Dutch microbusinesses](https://www.cbs.nl/nl-nl/longread/rapportages/2026/gebruik-van-ai-technologie-door-nederlandse-microbedrijven?onepage=true)
2. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
3. [European Commission: AI Act risk-based approach](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
4. [European Commission: GDPR processing principles](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en)

The course boundary is deliberately more conservative than a legal
classification.

## Guided build

The worked decision shows the full reasoning. Your recreation then applies the
same method to different synthetic candidates.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files.

## Start or resume safely

At the start of every study session, rerun Stage 1. PowerShell variables vanish
when its window closes; your saved files do not. Stage 1 restores the two paths
and returns to the same evidence folder without deleting anything. Later copy
steps deliberately leave an existing learner file unchanged.

Suggested sessions:

1. complete and check the worked brief and worked scorecard;
2. screen and score the three different recreation candidates;
3. run the Codex check, correct the records, and make the Git checkpoint.

Before stopping, save every file and note the last completed numbered step.
After reopening PowerShell, rerun Stage 1 and continue with the next step.

## Follow along — I show you exactly how

### Stage 1 — Prepare the module folder

**Prerequisite:** Module 1 passes and its evidence is committed in the one
project repository created during Windows Setup. Foundations remain in
`Documents\controlled-ai-course-practice`; Modules 1–9 do not.

Open Windows PowerShell and run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
if (-not (Test-Path (Join-Path $projectRoot '.git'))) { throw 'Project Git repository not found. Complete Windows Setup before Module 2.' }
$moduleFolder = Join-Path $projectRoot 'evidence\module-02'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
(Get-Location).Path
```

The `if` line stops rather than letting you create a second untracked module
project. **Expected result:** one path ending in
`\AI-workflow-learning\operations-exception-assistant\evidence\module-02`.

If it does not, run `Get-Location`, then repeat `Set-Location -LiteralPath
$moduleFolder`. If the repository error appears, stop and complete Windows
Setup; do not remove the check.

### Stage 2 — Follow a complete opportunity-selection decision

Run `notepad .\worked_opportunity_brief.md`, click **Yes**, paste the completed
example below, and save with **Ctrl+S**:

```markdown
# Worked opportunity brief — fictional stock administration

## Evidence available

- Four weekly checks per month.
- Demonstration baseline: 35 active minutes per check.
- Input can be represented with fictional stock rows.
- An inventory coordinator and operations lead can review the result.

## Hard-stop screen

| Candidate | Hard stop? | Reason |
|---|---|---|
| A. Automatically approve customer refunds | yes | external financial decision and source write-back |
| B. Prepare an internal low-stock exception list | no | internal draft, deterministic thresholds, human review |
| C. Generate marketing slogans | no | low consequence, but no measured operational pain |

## Opportunity score

Use the same scale as the reusable Course 1 scorecard:

- 0 = absent, unknown, or unsuitable;
- 1 = weak evidence;
- 2 = useful evidence with open questions;
- 3 = strong observed evidence.

| Factor | A | B | C |
|---|---:|---:|---:|
| Repeated volume or frequency | 3 | 3 | 1 |
| Measurable time, waiting, error, or rework | 2 | 3 | 0 |
| Stable unit of work and completion condition | 2 | 3 | 1 |
| Rules can be stated and tested | 1 | 3 | 0 |
| Input data is available and understandable | 1 | 3 | 1 |
| Process owner and reviewer are available | 1 | 3 | 1 |
| Course evaluation can be synthetic, bounded, and reversible | 0 | 3 | 3 |
| Users have a reason and capacity to adopt it | 1 | 2 | 0 |
| Manual fallback is practical | 1 | 3 | 2 |
| **Total, maximum 27** | **12** | **26** | **9** |

Candidate A remains stopped regardless of score. Candidate B is selected. A
score supports a discussion; it never overrides the stop screen or an
authorised owner's decision.

## Problem statement

When the weekly stock export becomes available, the inventory coordinator
manually identifies items below an approved reorder threshold so that an
operations lead can decide what to investigate. The demonstration takes 35
active minutes. We will test whether a controlled internal report reduces
active checking time without inventing stock facts or placing an order.

## Intended purpose

The system assists a fictional inventory coordinator by reading a synthetic
stock export, applying approved numerical thresholds, and preparing an internal
exception report. A human reviews the report. It does not change stock, select
a supplier, place an order, send a message, or make a payment.

## Negative scope and misuse

- No real or personal data.
- No prediction of future demand.
- No supplier ranking.
- No automatic order or source-system update.
- Risk of misuse: a user may treat the report as an order instruction.
- Protection: every page says "internal review draft — no action taken."

## Value hypothesis

Current monthly active time = 4 × 35 / 60 = 2.33 hours.
Time reduction remains "to be tested." Released time is capacity, not guaranteed
cash savings. Costs include configuration, review, testing, support, software,
and fallback work.

## Provisional measures

- Expected threshold exceptions found: 100% on frozen tests.
- Unsupported exceptions: 0.
- Issues linked to source row and rule: 100%.
- External actions and write-backs: 0.
- Manual fallback drill: passes once.
- Active-time change: measured later, with no promised percentage.

## Scope-change triggers

Real data, new data fields, a new user group, changed thresholds, external
messages, ordering, payments, recommendations, or source write-back all require
new assessment and approval.

## Selection decision

SELECT FOR SYNTHETIC PROOF. Owner: operations lead. User: inventory
coordinator. Reviewer: operations lead. Fallback owner: inventory coordinator.
```

Read it from top to bottom, then run:

```powershell
Get-Item -LiteralPath .\worked_opportunity_brief.md
Select-String -Path .\worked_opportunity_brief.md -Pattern 'SELECT FOR SYNTHETIC PROOF','does not','to be tested','Scope-change'
```

**Explanation:** `Get-Item` returns information about one named file without
opening or changing it. `-LiteralPath` treats the path exactly as written. The
second command finds the decision, negative scope, honest value language, and
change control.

**Expected output:** one file-information row containing
`worked_opportunity_brief.md`, followed by at least one matching line for each
search term.

**Troubleshooting:**

- If `Get-Item` says the file does not exist, save the Notepad file in
  `module-02` and rerun the command.
- If “SELECT FOR SYNTHETIC PROOF” is missing, confirm that the file was saved.
- A total score never cancels a hard stop. If Candidate A looks attractive,
  read its consequence and action again.
- Do not replace “to be tested” with an invented saving.

### Stage 3 — See how the brief maps to the scorecard template

The worked brief contains the reasoning. The reusable **workflow opportunity
scorecard** gives that reasoning a consistent evidence trail. Follow one small
completed example before recreating it.

Run `notepad .\worked_workflow_opportunity_scorecard.md`, click **Yes**, paste,
save, and close:

```markdown
# Worked workflow opportunity scorecard

- Artifact ID: WORKED-M02-SCORECARD
- Version/date: 1.0 / 2026-07-28
- Opportunity: fictional internal low-stock attention list
- Unit: one stock row
- Completion: operations lead records a review decision
- Process owner: operations lead
- Manual fallback: coordinator checks each row against approved thresholds

## Evidence and stop screen

Observed demonstration baseline: 35 active minutes per weekly check.
Assumption to test: a controlled report may reduce repeated checking.
Hard stop: automatic refunds are excluded because they create an external
financial action. No hard stop applies to the internal draft list.

## Simplest-option comparison

Clarifying thresholds and using a spreadsheet rule must be compared before AI.
The bounded rule-first report is selected only for a synthetic proof.

## Opportunity score

Scale: 0 = absent, unknown, or unsuitable; 1 = weak evidence; 2 = useful
evidence with open questions; 3 = strong observed evidence.

| Factor | Score | Evidence and limitation |
|---|---:|---|
| Repeated volume or frequency | 3 | Four observed checks per month |
| Measurable time, waiting, error, or rework | 3 | Worked baseline is 35 active minutes per check |
| Stable unit of work and completion condition | 3 | One stock row; complete when reviewer records a decision |
| Rules can be stated and tested | 3 | Quantity is compared with an approved threshold |
| Input data is available and understandable | 3 | Synthetic item ID, quantity, and threshold are defined |
| Process owner and reviewer are available | 3 | Operations lead owns and reviews the process |
| Course evaluation can be synthetic, bounded, and reversible | 3 | Local fictional rows and manual fallback |
| Users have a reason and capacity to adopt it | 2 | Repeated scanning exists; adoption capacity is assumed and must be tested |
| Manual fallback is practical | 3 | Coordinator can apply the approved spreadsheet filter |
| **Total, maximum 27** | **26** | The number does not override the stop screen |

## Selection decision

SELECT FOR SYNTHETIC PROOF. No client test, message, order, payment, approval,
or source-system write-back is authorized.
```

Check it without editing:

```powershell
Get-Item .\worked_workflow_opportunity_scorecard.md
Select-String -Path .\worked_workflow_opportunity_scorecard.md -Pattern 'baseline','Hard stop','maximum 27','26','spreadsheet','SELECT FOR SYNTHETIC PROOF'
```

**Expected result:** the file exists and all six evidence concepts are found.
If a term is missing, compare your pasted text with the example and correct
your own file.

## Now recreate it yourself

Small and medium-sized enterprise (SME) describes the fictional client type
below. Comma-separated values (CSV) is the plain-text table format used for its
supplied practice data.

First copy the blank scorecard template, then create
`recreated_opportunity_brief.md` for these different candidates:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$scorecardTemplate = Join-Path $courseRoot 'templates\workflow_opportunity_scorecard.md'
if (Test-Path -LiteralPath .\workflow_opportunity_scorecard.md) {
    Write-Host 'Resume: workflow_opportunity_scorecard.md already exists and was left unchanged.'
} else {
    Copy-Item -LiteralPath $scorecardTemplate -Destination .\workflow_opportunity_scorecard.md
}
Get-Item .\workflow_opportunity_scorecard.md
```

`Copy-Item` preserves the blank source template and gives your completed
capstone record the exact required name.

1. the Synthetic SME Operations Exception Assistant using
   `practice_data/work_items.csv`;
2. automatic ranking of employees by performance;
3. an internal meeting-summary generator with no measured baseline.

Use the same nine scoring factors, but write your own evidence note beside
every score. Candidate 2 must hit the course hard stop because it ranks people
for employment-related use. Select Candidate 1 and include:

- the Module 1 baseline;
- the exact user, reviewer, owner, trigger, input, function, and output;
- an internal report only;
- explicit exclusions for real data, decisions about people, supplier
  selection, messages, approvals, payments, contracts, and write-back;
- at least one foreseeable misuse and protection;
- a value formula with no invented improvement;
- measurable provisional thresholds;
- a manual fallback;
- scope-change triggers;
- a dated `SELECT FOR SYNTHETIC PROOF`, `DISCOVER FURTHER`, or `DISCARD`
  selection decision.

Use Notepad, save the file under `module-02`, reuse the demonstrated
`Get-Item` check, and verify:

```powershell
Get-Item .\recreated_opportunity_brief.md
Select-String -Path .\recreated_opportunity_brief.md -Pattern 'Synthetic SME Operations Exception Assistant','human','fallback','write-back'
```

**Expected output:** the file exists and all four concepts are found.

If the brief names a particular AI model or automation product in the problem
statement, remove it; the problem must remain tool-neutral.

Open `workflow_opportunity_scorecard.md` in Notepad and complete every relevant
section using the same evidence and decision as your recreated brief. For the
evidence status, mark observations, assumptions, decisions, and unresolved
claims separately. Complete the stop screen, compare all six improvement
options, give an evidence note for every score, and keep the manual fallback.
Write `not applicable — synthetic course` where a field truly does not apply;
do not leave an unexplained blank.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path` to obtain the full path, replace
`[PASTE FULL PATH HERE]`, and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize you to inspect only this full path:
[PASTE FULL PATH HERE]

Do not edit, create, delete, rename, move, or format files. Do not inspect the
parent folder or any other folder. This folder must contain no secrets and no
real client or workplace data. Stop if it contains credentials, personal data,
or health data.

Review worked_opportunity_brief.md,
worked_workflow_opportunity_scorecard.md,
recreated_opportunity_brief.md, and workflow_opportunity_scorecard.md. Return:
1. PASS or NOT YET;
2. a checklist for: evidence-backed problem; hard-stop screen; scores with
evidence; hard stops overriding totals; tool-neutral statement; complete
intended purpose; explicit negative scope; human reviewer; manual fallback;
misuse protection; value labelled as a hypothesis; costs included; measurable
thresholds; scope-change triggers; dated decision and owners;
completed scorecard evidence statuses; all six improvement options; score
evidence; the scorecard and brief use the same selection decision;
3. the smallest corrections for me to make if NOT YET.

Remain read-only. Do not rewrite the brief. Do not request or use any real
business information.
```

## Pass criteria

- [ ] Only synthetic scenarios are used.
- [ ] Three candidates are screened and scored with evidence.
- [ ] The employment-ranking candidate is stopped regardless of score.
- [ ] The selected opportunity is small, internal, measurable, and reversible.
- [ ] Intended purpose names user, context, input, function, output, review,
      and limitations.
- [ ] Negative scope excludes every consequential action listed above.
- [ ] Value is a hypothesis with costs, not guaranteed savings.
- [ ] Measures state what will be counted and the provisional threshold.
- [ ] Manual fallback, owners, misuse, and scope-change triggers are present.
- [ ] `workflow_opportunity_scorecard.md` separates evidence statuses,
      completes the stop screen, compares all six options, and explains every
      score.
- [ ] The scorecard and brief use the same dated selection decision.
- [ ] Codex returns `PASS` after read-only inspection.

## Consultant lens

The first useful deliverable may be a diagnostic rather than an automation.
Compare process correction, existing software, configured workflow, and custom
build later; this module only decides whether an opportunity deserves further
discovery.

## Capstone increment

The capstone has a justified selection decision, completed workflow opportunity
scorecard, intended purpose, negative scope, value hypothesis, owners, measures,
and change triggers.

## Required artifact

The teaching contract produces `worked_opportunity_brief.md`,
`worked_workflow_opportunity_scorecard.md`,
`recreated_opportunity_brief.md`, and
`workflow_opportunity_scorecard.md` in `evidence\module-02`.

## Test gate

The **Pass criteria** are the complete module gate.

## After PASS — make the Git checkpoint

Do this only after Codex returns `PASS`. Inspect the module folder yourself and
confirm it contains only synthetic course evidence: no password, secret key,
personal data, employer data, client data, patient data, or unrelated file.
Then run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-02"
git commit -m "complete module 2 evidence"
git status --short
```

`git status --short` previews changes. `git add --` stages only this module;
`--` marks the end of Git options. `git commit` records the passed checkpoint.
If a rerun produces “nothing to commit,” the unchanged evidence is already
recorded. Do not broaden the path to force a commit.

## Stop or rework

Stop if real data is required, no reviewer or process owner exists, a first
version must decide about people or take external action, rules cannot be
approved, or value depends on removing human review.

## Common failures

- Selecting a fashionable AI idea instead of measured work.
- Hiding uncertainty behind a numerical score.
- Confusing time capacity with cash savings.
- Letting any trial send, approve, rank, order, pay, or write back.
- Asking Codex to improve the file instead of checking it read-only.

## Estimated time

6–8 hours.
