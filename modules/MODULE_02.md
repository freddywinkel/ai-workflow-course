# Module 2 — Select and Bound a Worthwhile Opportunity

## Outcome

Using only fictional evidence, you will rehearse how to select a small,
measurable, reversible workflow opportunity and write an intended purpose,
negative scope, value hypothesis, success measures, and stop conditions. You
will learn that “do not automate this yet” can be the correct result; this is
not a claim that real client discovery occurred.

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
4. [European Commission: GDPR processing principles](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en)

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

Use eight focused blocks of 45–60 minutes. Never continue a block past 60
minutes or join two blocks because you feel behind.

- **UNDERSTAND** means you must explain the evidence, assumption, hard stop,
  score, decision, and smallest next step in your own words.
- **PROTECTED PLUMBING — RUN AND OBSERVE** means you may run the supplied
  path, create-once, hash-lock, and Git commands without memorising syntax. You
  must understand what each protects, inspect its result, and stop on an error.

1. **PROTECTED PLUMBING — RUN AND OBSERVE:** run Stage 1, verify the project
   boundary, and safely create or resume the Module 2 evidence folder.
2. **UNDERSTAND:** read the worked brief in Stage 2 and identify its evidence,
   assumptions, hard stops, intended purpose, exclusions, and fallback.
3. **UNDERSTAND:** complete the worked scorecard and explain why hard stops
   override its maximum-27 total and why every score needs evidence.
4. **UNDERSTAND:** study Stage 3's completed worksheet mapping, then read the
   three different synthetic recreation candidates without scoring yet.
5. **UNDERSTAND:** screen and score all three candidates, including existing
   tools, costs, reversibility, owner, success measure, and stop conditions.
6. **UNDERSTAND + PROTECTED PLUMBING:** decide between Candidates A and B
   before feedback, save the record, and create its Secure Hash Algorithm
   256-bit (SHA-256) lock.
7. **UNDERSTAND:** open the separate calibration only after the lock, preserve
   the first decision, write any reassessment separately, and finish the
   recreated opportunity brief and scorecard.
8. **UNDERSTAND + PROTECTED PLUMBING:** run the bounded Codex review, make your
   own corrections without altering locked evidence, check the pass criteria,
   and run only the supplied Module 2 Git checkpoint commands.

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
$projectMarker = Join-Path $projectRoot 'COURSE_PROJECT.md'
$expectedMarker = @'
# Course 1 synthetic learner project

This folder is only for the fictional Course 1 practice project.
Never place real client, employer, medical, or personal data here.
'@
if (-not (Test-Path -LiteralPath $projectMarker -PathType Leaf)) {
    throw 'Course project marker missing. Do not enter or change this folder.'
}
$actualMarker = (Get-Content -Raw -LiteralPath $projectMarker) -replace "`r`n", "`n"
if ($actualMarker -ne ($expectedMarker -replace "`r`n", "`n")) {
    throw 'Course project marker is unfamiliar. Do not enter or change this folder.'
}
$savedGitRoot = git -C $projectRoot rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0 -or
    (Resolve-Path -LiteralPath $savedGitRoot).Path -ne
    (Resolve-Path -LiteralPath $projectRoot).Path) {
    throw 'The marked Course 1 Git repository is missing or belongs to another folder.'
}
$moduleFolder = Join-Path $projectRoot 'evidence\module-02'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
(Get-Location).Path
function Open-CreateOnceCourseFile {
    param(
        [string]$Path,
        [string]$RecognizedStart,
        [string[]]$RequiredPatterns
    )
    if (Test-Path -LiteralPath $Path) {
        if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
            throw "Expected a lesson file but found another path type: $Path"
        }
        $content = Get-Content -Raw -LiteralPath $Path
        if ($null -eq $content) { $content = '' }
        $firstLine = Get-Content -LiteralPath $Path -TotalCount 1
        if (-not [string]::IsNullOrEmpty($content) -and
            $firstLine -cne $RecognizedStart) {
            throw "Existing file is unfamiliar. It was not opened or changed: $Path"
        }
        $complete = -not [string]::IsNullOrWhiteSpace($content)
        foreach ($pattern in $RequiredPatterns) {
            if (-not $content.Contains($pattern)) { $complete = $false }
        }
        if ($complete) {
            Write-Host "COMPLETE: keeping $Path unchanged."
            return
        }
        Write-Host 'INCOMPLETE: continue the recognised synthetic file without duplicating lines.'
    } else {
        New-Item -ItemType File -Path $Path | Out-Null
        Write-Host 'NEW: paste the supplied lesson content once.'
    }
    & notepad.exe $Path
}
```

The marker and Git-root checks are read-only and stop before a folder is
created unless this is the exact synthetic Course 1 project made by setup.
**Expected result:** one path ending in
`\AI-workflow-learning\operations-exception-assistant\evidence\module-02`.

If it does not, run `Get-Location`, then repeat `Set-Location -LiteralPath
$moduleFolder`. If the repository error appears, stop and complete Windows
Setup; do not remove the check.

The create-once helper below never overwrites. Before using it, confirm the
named file is synthetic lesson work. It creates a missing file, reopens an
empty or recognised incomplete one, skips a complete one, and stops without
opening a wrong-type or unfamiliar file. Preserve any unfamiliar file and ask
Codex for read-only diagnosis before starting a clearly numbered retry.

### Stage 2 — Follow a complete opportunity-selection decision

Run:

```powershell
Open-CreateOnceCourseFile `
    -Path (Join-Path $moduleFolder 'worked_opportunity_brief.md') `
    -RecognizedStart '# Worked opportunity brief' `
    -RequiredPatterns @('## Scope-change triggers','SELECT FOR SYNTHETIC PROOF')
```

For `NEW`, paste the completed example below and save with **Ctrl+S**. For
`INCOMPLETE`, continue only the missing part of the recognised file. For
`COMPLETE`, do not paste it again:

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

Run:

```powershell
Open-CreateOnceCourseFile `
    -Path (Join-Path $moduleFolder 'worked_workflow_opportunity_scorecard.md') `
    -RecognizedStart '# Worked workflow opportunity scorecard' `
    -RequiredPatterns @('Artifact ID: WORKED-M02-SCORECARD','**26**','SELECT FOR SYNTHETIC PROOF')
```

For `NEW`, paste, save, and close. For `INCOMPLETE`, continue without
duplicating existing sections. For `COMPLETE`, move to the checks:

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
if (-not (Test-Path -LiteralPath $scorecardTemplate -PathType Leaf)) {
    throw 'The controlled scorecard template is missing or is not a file.'
}
if (Test-Path -LiteralPath .\workflow_opportunity_scorecard.md) {
    if (-not (Test-Path -LiteralPath .\workflow_opportunity_scorecard.md -PathType Leaf) -or
        (Get-Content -LiteralPath .\workflow_opportunity_scorecard.md -TotalCount 1) -cne '# Workflow Opportunity Scorecard') {
        throw 'Existing scorecard is the wrong type or is unfamiliar. Preserve it and ask for read-only diagnosis.'
    }
    Write-Host 'Resume: workflow_opportunity_scorecard.md already exists and was left unchanged.'
} else {
    Copy-Item -LiteralPath $scorecardTemplate -Destination .\workflow_opportunity_scorecard.md
    if ((Get-FileHash -LiteralPath $scorecardTemplate -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath .\workflow_opportunity_scorecard.md -Algorithm SHA256).Hash) {
        throw 'The new scorecard copy did not match its controlled source.'
    }
}
Get-Item .\workflow_opportunity_scorecard.md
notepad.exe .\workflow_opportunity_scorecard.md
```

`Copy-Item` preserves the blank source template and gives your completed
capstone record the exact required name.

### Independent decision lab — lock your judgment before calibration

This decision lab is separate from the fixed capstone teaching vehicle. There
is deliberately no single preferred label. Do not read the calibration rules
below until you have recorded and fingerprinted your decision.

Assess these two previously unused fictional candidates:

**Candidate A — internal training-material review dates**

- a 40-row shared spreadsheet lists fictional material IDs, owner roles, and
  review dates;
- a coordinator spends about 25 active minutes each week checking due dates;
- the list contains no people, customer, medical, or financial decisions;
- Microsoft 365 is already available, but its native reminder capability has
  not been inspected;
- two weeks of measured volume exist; missed review means a stale internal
  handout, not an external action.

**Candidate B — repair-part photo description draft**

- a fictional workshop receives about 12 part photos per day;
- staff say descriptions are inconsistent, but no timed baseline or error count
  exists;
- a possible AI step would draft a short internal description from a synthetic
  image;
- a technician would review every draft and no order or message would be sent;
- image quality, allowed vocabulary, current system capability, and failure
  consequence remain unknown.

Create and complete the decision record before reading further:

```powershell
$independentDecision = Join-Path $moduleFolder 'independent_opportunity_decision.md'
if (Test-Path -LiteralPath $independentDecision) {
    if (-not (Test-Path -LiteralPath $independentDecision -PathType Leaf) -or
        (Get-Content -LiteralPath $independentDecision -TotalCount 1) -cne '# Independent opportunity decision') {
        throw 'Existing independent decision is unfamiliar. Preserve it and ask for read-only diagnosis.'
    }
    Write-Host "KEEPING existing $independentDecision"
} else {
    @'
# Independent opportunity decision

Decision made before calibration: YES / NO

| Candidate | Hard stop and reason | Evidence versus assumption | Existing-tool question | Reversibility and failure consequence | SELECT / DISCOVER FURTHER / DISCARD | Smallest next evidence |
|---|---|---|---|---|---|---|
| A | | | | | | |
| B | | | | | | |

Preferred next step and why:
What evidence could change it:
What I deliberately did not assume:
'@ | Set-Content -LiteralPath $independentDecision -Encoding utf8
}
notepad $independentDecision
```

After completing and closing the file, lock its current bytes:

```powershell
$independentDecisionHash = (
    Get-FileHash -LiteralPath $independentDecision -Algorithm SHA256
).Hash
$independentHashPath = Join-Path $moduleFolder 'independent_opportunity_decision.sha256'
if (Test-Path -LiteralPath $independentHashPath) {
    $lockedHash = (Get-Content -Raw -LiteralPath $independentHashPath).Trim()
    if ($lockedHash -cne $independentDecisionHash) {
        throw 'The locked independent decision changed. Preserve it and write only a separate reassessment.'
    }
    Write-Host 'PASS: existing decision lock still matches'
} else {
    $independentDecisionHash |
        Set-Content -LiteralPath $independentHashPath -Encoding ascii
    Write-Host 'CREATED: independent decision lock'
}
$independentDecisionHash
```

Do not edit the locked record after this point.

#### Open the separate calibration page only now

Only after the hash is saved and confirmed, open
[Module 2 Opportunity-Decision Calibration](../OPPORTUNITY_DECISION_CALIBRATION.md).
That separate page contains the calibration criteria and reassessment
instructions. Keeping it off this decision page prevents you from seeing the
criteria before the original record is locked.

Never replace the original decision to make it look as though you knew the
calibration first.

Create or reopen the brief before writing:

```powershell
$briefPath = Join-Path $moduleFolder 'recreated_opportunity_brief.md'
if (Test-Path -LiteralPath $briefPath) {
    if (-not (Test-Path -LiteralPath $briefPath -PathType Leaf) -or
        (Get-Content -LiteralPath $briefPath -TotalCount 1) -cne '# Recreated opportunity brief') {
        throw 'Existing opportunity brief is the wrong type or is unfamiliar. Preserve it and ask for read-only diagnosis.'
    }
    Write-Host "Resume: $briefPath already exists and was left unchanged."
} else {
    "# Recreated opportunity brief`r`n" |
        Set-Content -LiteralPath $briefPath -Encoding utf8
    Write-Host "Created: $briefPath"
}
notepad.exe $briefPath
```

Now assess the fixed capstone teaching candidates:

1. the Synthetic SME Operations Exception Assistant using
   `practice_data/work_items.csv`;
2. automatic ranking of employees by performance;
3. an internal meeting-summary generator with no measured baseline.

Use the same nine scoring factors, but write your own evidence note beside
every score. Candidate 2 must hit the course hard stop because it ranks people
for employment-related use. The course continues with Candidate 1 as the fixed
technical teaching vehicle; that is not evidence that you independently chose
it. Give Candidate 1 your own `SELECT FOR SYNTHETIC PROOF`,
`DISCOVER FURTHER`, or `DISCARD` judgment and include:

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

Learner attestation: I created these files for this fictional exercise and
have not knowingly put real client, employer, personal, medical, credential,
or secret data in them. This statement is an attestation, not proof.

You may only list names, read files, and calculate hashes inside the authorised
path. Do not create, edit, delete, rename, move, or format any file. Do not
execute lesson scripts, use a network, or inspect a parent
or other location. If apparent sensitive data is noticed, do not quote or
repeat it: return NOT YET with only the filename and general category, then
stop. If none is noticed, say that non-detection is not proof that none exists.

Review worked_opportunity_brief.md,
worked_workflow_opportunity_scorecard.md,
independent_opportunity_decision.md,
independent_opportunity_decision.sha256,
and independent_opportunity_reassessment.md when it exists,
recreated_opportunity_brief.md, and workflow_opportunity_scorecard.md. Return:
1. PASS or NOT YET;
2. a checklist for: evidence-backed problem; hard-stop screen; scores with
evidence; hard stops overriding totals; tool-neutral statement; complete
intended purpose; explicit negative scope; human reviewer; manual fallback;
misuse protection; value labelled as a hypothesis; costs included; measurable
thresholds; scope-change triggers; dated decision and owners;
completed scorecard evidence statuses; all six improvement options; score
evidence; the scorecard and brief use the same selection decision;
3. a separate check that the saved SHA-256 matches the unchanged independent
decision; both multi-outcome candidate decisions distinguish evidence from
assumption, existing-tool fit, reversibility, failure consequence, and next
evidence; no particular label is required when reasoning is supported; any
post-calibration correction is preserved separately;
4. the smallest corrections for me to make if NOT YET.

Remain read-only. Do not rewrite the brief. Do not request or use any real
business information.
```

## Pass criteria

- [ ] Only synthetic scenarios are used.
- [ ] I locked the independent record containing both candidate decisions
      before calibration, the SHA-256 still matches, and any correction is a
      separate reassessment.
- [ ] The independent decision uses evidence, uncertainty, existing-tool fit,
      reversibility, consequence, and next evidence; it does not depend on one
      prescribed label.
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
the locked independent opportunity decision and optional reassessment,
`recreated_opportunity_brief.md`, and
`workflow_opportunity_scorecard.md` in `evidence\module-02`.

## Test gate

The **Pass criteria** are the complete module gate.

## After PASS — make the Git checkpoint

Do this only after Codex returns `PASS`. Inspect the module folder yourself and
confirm it contains only synthetic course evidence: no password, secret key,
personal data, employer data, client data, patient data, or unrelated file.
Rerun Stage 1 in this same PowerShell window so the exact marker and Git-root
checks pass again. Then run:

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-02"
git commit --only -m "complete module 2 evidence" -- "evidence/module-02"
git status --short
```

`git status --short` previews changes. `git add --` stages only this module;
`--` marks the end of Git options. `git commit --only` records only the
repeated module path, even if a different file had already been staged. If a
rerun produces “nothing to commit,” the unchanged evidence is already
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

6–8 hours. This is an **AUTHOR ESTIMATE — NOT BEGINNER MEASURED**.
