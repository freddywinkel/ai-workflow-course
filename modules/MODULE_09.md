# Module 9 — Run User Acceptance Testing (UAT), Plan Adoption, and Hand Over

## Outcome

You will complete User Acceptance Testing (UAT), plan training and adoption,
write a runbook and fallback, assemble handover evidence, make a bounded final
decision, and write an honest portfolio case.

User Acceptance Testing (UAT) means intended users try realistic scenarios and
confirm whether the workflow supports the agreed work.

Passing Course 1 proves a synthetic foundation project. It does not certify you
as a production consultant or regulated-systems specialist.

## Beginner checkpoint

Start when Modules 1–8 pass. Continue for any of the three permitted Module 8
decisions: `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or
`DO NOT CONTINUE`. This module closes and indexes the evidence honestly; it
does not force a positive decision. All acceptance work remains synthetic and
local.

## Concepts

- **User Acceptance Testing (UAT)** means intended users check whether a system
  supports agreed work in realistic scenarios.
- **Adoption** is sustained correct use, not simply installing software.
- A **runbook** tells an operator how to run, monitor, stop, recover, and
  escalate.
- **Handover** transfers evidence, instructions, access responsibilities,
  limitations, and continuing ownership.
- **Benefits realisation** measures whether the expected benefit appears after
  use.
- **Rollback** returns to a known safe earlier method or version.
- An **identifier (ID)** distinguishes one test or evidence item.
- **Information technology (IT)** is the function that manages organisational
  systems and support; a runbook must still name a responsible role.

## Official readings

GOV.UK is the United Kingdom government's public guidance website. The United
States National Institute of Standards and Technology (NIST) publishes
voluntary artificial intelligence (AI) risk guidance.

1. [GOV.UK Service Manual: testing with users](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing)
2. [GOV.UK Service Manual: set up and manage user support](https://www.gov.uk/service-manual/helping-people-to-use-your-service/set-up-and-manage-user-support)
3. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

## Guided build

The worked handover is for a simple fictional stock exception process. The
independent recreation uses the different Course 1 capstone and its actual
evidence.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files. Comma-separated
values (CSV) is the plain-text table format used by the scenario. A small or
medium-sized enterprise (SME) is a business smaller than a large enterprise.

Markdown is a plain-text format for headings, lists, and tables; `.md` is its
file name ending. **Given/When/Then** is a test-writing pattern: **Given**
describes the starting state, **When** names the action, and **Then** states the
observable expected result.

## Follow along — I show you exactly how

**Expected result:** a complete worked UAT, adoption, runbook, handover, final
decision, and honest portfolio pack for a synthetic scenario.

### Stage 1 — Prepare the module folder

Open Windows PowerShell and run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
if (-not (Test-Path (Join-Path $projectRoot '.git'))) {
    throw 'Project repository not found. Complete Windows Setup before Module 9.'
}
$moduleFolder = Join-Path $projectRoot 'evidence\module-09'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
notepad .\worked_uat_and_handover.md
```

### Stage 2 — Read and recreate a complete worked pack

Click **Yes**, paste, save, and close:

```markdown
# Worked UAT and handover — fictional low-stock list

## Boundary

Synthetic local spreadsheet configuration. It identifies quantity below an
approved threshold for internal review. It does not use AI, order, message,
select suppliers, pay, or write to a source system.

## Roles

- Process owner: operations lead; approves rules and acceptance.
- User: inventory coordinator; runs and reviews the list.
- Support owner: office systems coordinator; supports access and restore.
- Tester: course learner acting in a separate tester role.

## UAT script and result

| ID | Given | When | Then | Evidence | Result |
|---|---|---|---|---|---|
| UAT-01 | all quantities meet thresholds | user runs filter | empty exception list and no action state | screenshot-free result note and row count | pass |
| UAT-02 | one quantity is below threshold | user runs filter | one issue shows item ID, raw value, threshold, rule | saved synthetic output | pass |
| UAT-03 | quantity cell is blank | user runs filter | item stops for human review; zero is not invented | failure note | pass |
| UAT-04 | expected header is renamed | user runs filter | safe stop and manual fallback | failure record | pass |
| UAT-05 | user tries to treat list as an order | reviewer checks boundary | wording says internal review only | review note | pass |

Acceptance threshold: all five pass; no external action; fallback usable.

## Usability observations

- User can find source item and rule without help.
- "No action" and "failed" are visually distinct in the written result.
- The phrase "high attention" is not used as an order instruction.
- Limitation: test is a role simulation, not external user evidence.

## Adoption and training

What changes: coordinator uses a saved filter and reviewed list.
What does not change: operations lead decides investigation and ordering.

Training tasks:
1. open the correct synthetic/source export;
2. confirm header and assessment configuration;
3. run the filter;
4. trace an issue to source values;
5. distinguish no-action, issue-ready, and failed;
6. reject or correct a list;
7. use manual fallback;
8. report an incident.

Training evidence: learner demonstrates every task once without hidden prompts.
Feedback route: support owner records questions and recurring mistakes.

## Runbook

Normal run:
1. Confirm approved input location and unchanged header.
2. Preserve the source export.
3. Run the configured filter.
4. Check state and issue count.
5. Trace every exception to source and rule.
6. Have the operations lead review.
7. Store the internal reviewed result.

Safe failure:
1. Stop; do not guess or change the source.
2. Record error, time, input identity, and last safe state.
3. Tell the support owner.
4. Use manual spreadsheet filter.
5. Resume only after a tested correction and owner approval.

Rollback: restore the last tested formula/filter copy and rerun frozen tests.
Backup: support owner keeps the tested file and instructions.
No external action is replayed because none exists.

## Handover inventory

- intended purpose and negative scope;
- data dictionary and rule source;
- configured filter and version;
- frozen test data and results;
- UAT record;
- user instructions and runbook;
- access, backup, restore, incident, and update owners;
- known limitations and residual risks;
- manual fallback and rollback;
- decision record.

## Known limitations

- Synthetic and small-volume only.
- One file layout and one approved threshold set.
- No live integration or concurrent-user test.
- No external user research.
- No legal, privacy, or security assurance beyond the stated screen.

## Final decision

ACCEPT FOR SYNTHETIC PORTFOLIO. The case may be demonstrated only with its
synthetic boundary and stated limitations. Do not deploy it to a business.
Later courses separately teach discovery and controlled implementation.

## Honest portfolio summary

Problem: a fictional coordinator repeatedly scans stock rows.
Approach: define exact rules, configure a read-only exception list, test
failures, retain human review, and document fallback.
Evidence: frozen synthetic tests and five role-simulated UAT scenarios pass.
Limitations: no client, real data, production deployment, or proven cash saving.
```

Run:

```powershell
Select-String -Path .\worked_uat_and_handover.md -Pattern 'UAT-01','UAT-05','Safe failure','Known limitations','ACCEPT FOR SYNTHETIC PORTFOLIO'
```

**Expected result:** all five elements are found. The complete pack connects
acceptance, training, operation, failure, ownership, limitations, and decision.

**Troubleshooting:**

- If UAT only says “works,” rewrite it as Given/When/Then with observable
  evidence.
- If training is a presentation, add tasks the learner must demonstrate.
- If the runbook says “contact IT,” name a support role and what evidence to
  provide.
- If acceptance silently means production release, restore the synthetic-only
  limitation.

### Stage 3 — Rehearse one worked scenario

Read UAT-04 aloud and perform a tabletop rehearsal:

1. say what the user sees;
2. name the state;
3. name the evidence recorded;
4. state the manual fallback;
5. state who approves resumption.

Record the answers in `worked_uat_rehearsal.md`. This demonstrates that the
runbook can be followed rather than merely filed.

## Now recreate it yourself

Use the different Synthetic SME Operations Exception Assistant and the actual
Course 1 evidence.

1. Copy current templates:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
Copy-Item -LiteralPath (Join-Path $courseRoot 'templates\uat_script.md') -Destination .\recreated_uat.md
Copy-Item -LiteralPath (Join-Path $courseRoot 'templates\adoption_and_training_plan.md') -Destination .\recreated_adoption.md
Copy-Item -LiteralPath (Join-Path $courseRoot 'templates\acceptance_and_handover.md') -Destination .\recreated_handover.md
notepad .\recreated_final_decision.md
```

In the new final-decision file, create these headings before continuing:
`Decision`, `Evidence`, `Failed or passed thresholds`, `Limitations`,
`Closeout actions`, and `What remains outside Course 1`.

2. Complete `recreated_uat.md` with at least these nine synthetic scenarios:

- clean/no-issue input;
- all 13 expected issues;
- invalid header;
- invalid date dependency;
- duplicate reference reports both rows;
- invalid or unsupported summary;
- approve exact draft;
- edit invalidates approval;
- `EXTERNAL_ACTIONS_ENABLED=false` and manual fallback.

For each, write role, Given/When/Then, expected state, exact evidence, observed
result, pass/fail, defect, and retest.

3. Act through every scenario in a separate tester role. If a consenting person
is available, they may use synthetic files only; this is optional and does not
authorise workplace research. Label self-testing honestly.
4. Complete `recreated_adoption.md` with role changes, eight demonstrated
training tasks, accessibility/support needs, feedback route, resistance or
misuse risks, owner, and refresher trigger.
5. Complete `recreated_handover.md` with:

- purpose, exclusions, architecture, files, versions, hashes, and states;
- data/rule/prompt/provider configuration and evaluation evidence;
- UAT and known defects;
- access, backup, restore, monitoring, incident, update, and exit owners;
- startup, normal run, safe failure, fallback, rollback, and deletion;
- residual risks and limitations.

6. Complete `recreated_final_decision.md` using exactly the Module 8 decision:
   `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or `DO NOT CONTINUE`. Then use
   the matching closeout path:

   - `ACCEPT FOR SYNTHETIC PORTFOLIO`: package the synthetic evidence and state
     every limitation prominently. This does not authorize business use.
   - `REWORK`: list each failed threshold, its evidence, the smallest corrective
     task, owner, and retest. Do not present the workflow as accepted.
   - `DO NOT CONTINUE`: record the reason, preserve the audit trail, confirm
     external actions remain disabled, and close the exercise without promoting
     the workflow.

   All three evidence-backed outcomes pass Course 1. Course 1 never transitions
   to client use.
7. Create `recreated_portfolio_case.md` with problem, method, controls, measured
   synthetic evidence, what you learned, and limitations. For `REWORK`, label
   it an incomplete learning case. For `DO NOT CONTINUE`, write a lessons-learned
   closure instead of a success case.
8. Create `recreated_demo_script.md` for a five-minute demonstration:

- minute 0–1: problem and boundary;
- minute 1–2: deterministic issues and evidence;
- minute 2–3: bounded summary and support;
- minute 3–4: review, hash invalidation, and fallback;
- minute 4–5: evaluation, limitations, and decision.

Do not claim this exercise saved a client's time or money.

Verify:

```powershell
Select-String -Path .\recreated_uat.md -Pattern 'Given','When','Then','failed_manual','retest'
Select-String -Path .\recreated_handover.md -Pattern 'fallback','rollback','restore','incident','limitation','owner'
Select-String -Path .\recreated_final_decision.md,.\recreated_portfolio_case.md -Pattern 'synthetic','not production','Course 1'
```

**Expected result:** every search term appears in the relevant evidence. Missing
terms identify work to finish; they are not permission to weaken acceptance.

### Stage 4 — Assemble the single capstone repository

The setup and every module now belong to this one Git repository. Create a
root index so another person can find the evidence without guessing.

Run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
notepad .\CAPSTONE_INDEX.md
```

Create an `Artifact map` table with one row for setup and one row for each
Module 1 through Module 9. For each row record:

- the folder, such as `evidence/module-04`;
- the main worked and recreated artifacts;
- the pass evidence;
- the Git commit identifier from `git log --oneline`;
- any limitation or rework still open.

Module 9 has not been committed yet because the read-only PASS comes first.
Enter `PENDING UNTIL FINAL PASS` in only that row. You will replace it with the
real identifier during the final checkpoint.

Also add these headings: `Synthetic boundary`, `Architecture and data flow`,
`Deterministic workflow`, `Bounded artificial-intelligence step`, `Human
control`, `Evaluation decision`, and `Closeout status`. Link them to repository
paths. Do not paste files into the index.

Then create the repository change history:

```powershell
notepad .\CHANGELOG.md
```

Start it with:

```markdown
# Project change log

## Course 1 closeout — 2026-07-28

- Assembled setup and Modules 1–9 in one local Git repository.
- Final decision: REPLACE WITH ONE EXACT PERMITTED DECISION.
- External actions: disabled.
- Data: synthetic course data only.
- Known limitations: REPLACE WITH YOUR EVIDENCE.
```

Replace both placeholders with your own evidence. `CHANGELOG.md` records what
changed; `CAPSTONE_INDEX.md` records where the evidence is.

## Ask Codex to check your work

Run `(Resolve-Path $projectRoot).Path` to obtain the full project path. Replace
`[PASTE FULL PATH HERE]` and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full Course 1 project repository:
[PASTE FULL PATH HERE]

Do not create, edit, delete, rename, move, format, or execute anything. Do not
inspect the parent or another path. Stop if there are secrets, credentials,
real client data, workplace data, personal data, or health data.

Return:
1. PASS or NOT YET;
2. checks for: at least nine Given/When/Then UAT scenarios; expected states and
evidence; defects and retests; exact-draft and
EXTERNAL_ACTIONS_ENABLED=false drills; role-specific
training with demonstrated tasks; feedback/support; complete normal and
safe-failure runbook; manual fallback; rollback; backup/restore; monitoring;
incident/update/exit owners; versions and hashes; limitations and residual
risks; exactly one permitted evidence-backed final decision; the matching
accept/rework/closure path; honest portfolio or lessons-learned case;
five-minute demo; CAPSTONE_INDEX.md maps setup and Modules 1-9; CHANGELOG.md
records the closeout; no claim of client savings, production readiness, or
consultant certification. Allow only the Module 9 commit cell to say PENDING
UNTIL FINAL PASS because this review must happen before that commit;
3. the smallest corrections for me to make if NOT YET.

Remain read-only. Do not complete the handover or UAT for me.
```

## Pass criteria

- [ ] Worked UAT/handover and tabletop rehearsal are complete.
- [ ] Recreated UAT has at least nine realistic scenarios and evidence.
- [ ] Failures, review choices, hash invalidation, and fallback are tested.
- [ ] Defects are recorded and retested rather than hidden.
- [ ] Training is role-specific and demonstrated.
- [ ] Runbook covers normal run, stop, fallback, rollback, restore, and
      escalation.
- [ ] Handover assigns every continuing responsibility.
- [ ] The exact final decision is `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`,
      or `DO NOT CONTINUE`, and its evidence supports it.
- [ ] The matching accept, corrective, or safe-closure path is complete.
- [ ] Portfolio, incomplete case, or lessons-learned closure states evidence
      and limitations honestly.
- [ ] Root `CAPSTONE_INDEX.md` maps setup and all nine modules.
- [ ] Root `CHANGELOG.md` records the dated decision and limitations.
- [ ] Codex returns `PASS` read-only.

### Record the final Course 1 PASS in Git

Do this only after Codex returns `PASS`. The first commit records Module 9 just
like every earlier module. The second commit records the two root assembly
files.

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-09"
git commit -m "complete module 9 evidence"
git log --oneline --max-count=10
```

Run `notepad .\CAPSTONE_INDEX.md`, replace `PENDING UNTIL FINAL PASS` with the
new Module 9 identifier shown by `git log`, save, and close Notepad. Then run:

```powershell
git add -- "CAPSTONE_INDEX.md" "CHANGELOG.md"
git commit -m "assemble Course 1 synthetic capstone"
git status --short
git log --oneline --max-count=10
```

Expected result: the newest commit assembles the Course 1 closeout, the next
commit records Module 9, and earlier module checkpoints are visible below it.
If Git reports `nothing to commit`, confirm that the relevant named paths were
already recorded and unchanged. Never add a secret, real data, or unrelated
file.

## Consultant lens

Implementation is not finished when code runs. It is finished only when users
can perform the work, owners accept responsibilities, failures have a route,
evidence supports the decision, and the organisation can continue without the
builder.

## Capstone increment

The Course 1 capstone is complete as an evidence-controlled synthetic project
with UAT, adoption plan, runbook, handover, an accept/rework/close decision,
and an honest case or closure record.

## Required artifact

The teaching contract creates the worked pack/rehearsal and the recreated UAT,
adoption, handover, decision, portfolio or closure, and demo evidence under
`evidence/module-09`, plus root `CAPSTONE_INDEX.md` and `CHANGELOG.md`.

## Test gate

The **Pass criteria** are the complete Course 1 gate.

## Stop or rework

Stop if UAT is vague, defects are hidden, owners are placeholders, fallback was
not rehearsed, an action can escape, real data appears, or synthetic evidence
is presented as client proof.

## Common failures

- Asking whether users “like it” instead of testing tasks.
- Training features instead of roles and decisions.
- Handing over code without operation and incident ownership.
- Treating self-test as independent acceptance.
- Calling Course 1 completion professional certification.

## Estimated time

12–16 hours.
