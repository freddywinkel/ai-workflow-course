# Module 7 — Apply Dutch Small and Medium-sized Enterprise (SME) Guardrails and Choose the Right Tool

## Outcome

You will perform a conservative Dutch SME risk screen, map data movement,
compare manual improvement, configuration, purchase, and custom build, review
vendor and ownership questions, and record a proportionate decision.

A small and medium-sized enterprise (SME) is a smaller organisation rather
than a large enterprise. In this course, the term describes the practical
client context; it does not replace the official legal or funding definitions.

## Beginner checkpoint

Start when Modules 1–6 pass. The workflow is still synthetic, internal,
reviewed, reversible, and local-draft-only.

## Concepts

- **Build versus buy** compares custom implementation with existing software,
  configuration, and process improvement.
- **Accountability** means the organisation can explain its purpose, data,
  controls, owners, and evidence.
- **Data minimisation** means processing only what the purpose needs.
- A **data flow** shows where information enters, moves, is stored, and leaves.
- A **Data Protection Impact Assessment (DPIA)** is a formal privacy-risk
  assessment required in some higher-risk personal-data situations.
- **Comma-separated values (CSV)** is a plain-text table format.
- An **application programming interface (API)** lets software systems exchange
  requests and responses.
- **Markdown** is a plain-text format for headings, lists, and tables; `.md` is
  its file name ending.
- An **identifier (ID)** distinguishes one item, rule, or record.
- **Python** is the programming language used for the current local proof.
- **Information technology (IT)** is the function that manages organisational
  systems and support; a handover must still name an accountable role.
- **Total cost of ownership** includes implementation, licences, review,
  support, training, monitoring, exit, and failure—not only purchase price.
- **Vendor lock-in** is difficulty moving data or operation away from a vendor.

## Official readings

Artificial intelligence (AI) means software that can generate or infer an
answer. The General Data Protection Regulation (GDPR), called the Algemene
verordening gegevensbescherming (AVG) in Dutch, governs personal-data
processing. Autoriteit Persoonsgegevens is the Dutch Data Protection Authority.
The National Cyber Security Centre (NCSC) publishes Dutch cyber-resilience
guidance.

1. [Autoriteit Persoonsgegevens: AI and algorithms](https://autoriteitpersoonsgegevens.nl/themas/algoritmes-ai)
2. [European Commission: GDPR principles](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en)
3. [European Commission: AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
4. [NCSC Netherlands: basic cyber-resilience measures](https://www.ncsc.nl/basisprincipes/resultaten)

These sources support screening; they do not replace legal, security, labour,
procurement, or sector advice.

## Guided build

The worked example deliberately concludes that AI is unnecessary. The
independent recreation assesses the different Course 1 capstone.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files.

## Start or resume safely

At the start of every study session, rerun Stage 1. Closing PowerShell removes
temporary variables, not saved evidence. Stage 1 restores the paths and opens
the same folder. Recreation copies below are create-once: an existing file is
reported and left unchanged.

Suggested sessions:

1. follow the combined worked decision and scope-change test;
2. inspect both completed worksheet examples, then recreate both forms;
3. perform the evidence check, correct gaps, and make the Git checkpoint.

Save all files and note the last numbered step before stopping. In a new
PowerShell window, rerun Stage 1 instead of guessing the paths.

## Follow along — I show you exactly how

**Expected result:** a complete worked guardrail and tool-fit decision that
rejects unnecessary AI and makes ownership, fallback, and reassessment visible.

### Stage 1 — Prepare and read the complete worked decision

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
$moduleFolder = Join-Path $projectRoot 'evidence\module-07'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
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
Open-CreateOnceCourseFile `
    -Path (Join-Path $moduleFolder 'worked_guardrail_and_tool_decision.md') `
    -RecognizedStart '# Worked guardrail and tool decision' `
    -RequiredPatterns @('## Minimum security and ownership','CONFIGURE EXISTING SPREADSHEET','Reassess only if')
```

The create-once helper never overwrites. Before each call, confirm the named
file is synthetic lesson work. It creates a missing file, reopens an empty or
recognised incomplete one, skips a complete one, and stops without opening a
wrong-type or unfamiliar file. Preserve an unfamiliar file and ask Codex for
read-only diagnosis before a clearly numbered retry.

For `NEW`, paste the completed example, save, and close. For `INCOMPLETE`,
continue without duplicating sections. For `COMPLETE`, move to the checks:

```markdown
# Worked guardrail and tool decision

## Fictional use case

An office-supply SME wants a weekly internal low-stock list from a synthetic
CSV. A coordinator reviews it. The workflow does not order, contact suppliers,
rank products, pay, or write to inventory.

## Intended purpose

User: inventory coordinator.
Input: synthetic item ID, quantity, and approved reorder threshold.
Function: deterministic quantity-below-threshold check.
Output: internal review list.
Reviewer/owner: operations lead.
Fallback: filter the CSV manually.

## Data flow

1. Fictional stock CSV enters a local approved folder.
2. Deterministic rules read item ID, quantity, and threshold.
3. An internal exception CSV is written locally.
4. The operations lead reviews it.
5. No data is sent externally and no source record changes.

## Personal-data and consequence screen

- Personal data: none needed.
- Special-category or health data: none.
- Employee/customer scoring: none.
- Employment, credit, insurance, benefits, education, policing, migration,
  justice, healthcare, or safety decision: none.
- External message, order, payment, approval, contract, or write-back: none.
- AI interaction: none.
- Escalation: reassess before any real data, person-related field, external
  connection, action, or AI step.

## Options

| Option | Fit | Evidence | Main burden | Decision |
|---|---|---|---|---|
| Improve manual spreadsheet filter | good for tiny volume | existing fallback | repeated manual time | retain as fallback |
| Configure spreadsheet formula/filter | best first fit | exact numeric rule | ownership and testing | select |
| Buy workflow platform | excessive | no integration need | licence/admin cost | reject now |
| Custom Python service | excessive | technically possible | maintenance/support | reject now |
| Add generative AI | no useful role | rule is exact | variability and governance | reject |

## Minimum security and ownership

- Approved local folder and named users.
- Least access needed for role.
- Original file preserved.
- Backup and restore owner: operations lead.
- Updates tested before use.
- Incident route: stop, use manual filter, tell owner.
- Data export: CSV remains portable.
- Deletion: local input/output removed according to an approved schedule.
- No secret, API key, or vendor account.

## Cost and exit

Cost categories: coordinator setup, formula test, reviewer time, instructions,
maintenance, fallback drill. Exit is simple: retain CSV and manual filter.

## Decision

CONFIGURE EXISTING SPREADSHEET. Do not build or buy AI. Reassess only if measured
volume or complexity changes. This is an operational recommendation, not legal
approval.
```

Read the decision, then run:

```powershell
Select-String -Path .\worked_guardrail_and_tool_decision.md -Pattern 'none needed','select','reject','fallback','Reassess'
```

**Expected result:** matches show the data screen, selected option, rejected
options, fallback, and scope-change trigger.

**Why each action matters:** purpose limits collection; data flow exposes
transfers; consequence screening prevents an unsuitable beginner project;
option comparison avoids custom-building by habit; ownership makes the chosen
solution operable.

**Troubleshooting:**

- If every option says “AI,” add process improvement and existing-tool
  configuration.
- If “no personal data” is based on not asking rather than inspecting fields,
  mark it unknown and stop.
- If the person who owns backup, access, incident, or exit is “IT” with no
  named role, clarify the role.

### Stage 2 — Test one scope change

Run:

```powershell
Open-CreateOnceCourseFile `
    -Path (Join-Path $moduleFolder 'worked_scope_change.md') `
    -RecognizedStart '# Worked scope-change decision' `
    -RequiredPatterns @('Decision: DO NOT CONTINUE','Do not bolt the request')
```

For `NEW`, paste the example. For `INCOMPLETE`, add only the missing part. For
`COMPLETE`, do not paste again:

```markdown
# Worked scope-change decision

Request: add employee names and automatically message the person responsible.
Effect: introduces personal data and an external action.
Decision: DO NOT CONTINUE. Reopen privacy, authority, security, user,
necessity, transparency, works-council where applicable, vendor, fallback, and
testing review. Do not bolt the request onto the approved workflow.
```

This demonstrates that a small feature request can materially change risk.

### Stage 3 — Inspect the two completed worksheet-shaped examples

The combined worked decision above teaches the reasoning. Before you see the
blank forms, open the completed versions that use the exact same headings and
tables:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
notepad (Join-Path $courseRoot 'worked_examples\module_07_risk_and_escalation_screen.md')
notepad (Join-Path $courseRoot 'worked_examples\module_07_tool_fit_and_ownership_record.md')
```

Read every row. Notice that `not applicable` includes a reason, unknown facts
stay unknown, each continuing duty has a role, and the selected option is
simpler than the learning prototype. These are examples to follow, not answers
to copy into the different capstone recreation.

## Now recreate it yourself

Assess the different Synthetic SME Operations Exception Assistant.

1. Copy the two current worksheets:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
function Copy-NewPracticeFile {
    param([string]$Source, [string]$Destination, [string]$ExpectedHeading)
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Controlled course worksheet is missing or is not a file: $Source"
    }
    if (Test-Path -LiteralPath $Destination) {
        if (-not (Test-Path -LiteralPath $Destination -PathType Leaf) -or
            (Get-Content -LiteralPath $Destination -TotalCount 1) -cne $ExpectedHeading) {
            throw "Existing worksheet is the wrong type or is unfamiliar. Preserve it and ask for read-only diagnosis: $Destination"
        }
        Write-Host "Resume: $Destination already exists and was left unchanged."
    } else {
        Copy-Item -LiteralPath $Source -Destination $Destination
        if ((Get-FileHash -LiteralPath $Source -Algorithm SHA256).Hash -ne
            (Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash) {
            throw "New worksheet copy did not match its controlled source: $Destination"
        }
        Write-Host "Created: $Destination"
    }
}
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\risk_and_escalation_screen.md') .\recreated_risk_screen.md '# Risk and Escalation Screen'
Copy-NewPracticeFile (Join-Path $courseRoot 'templates\tool_fit_and_ownership_record.md') .\recreated_tool_fit.md '# Tool Fit and Ownership Record'
notepad.exe .\recreated_risk_screen.md
notepad.exe .\recreated_tool_fit.md
```

2. Complete every field yourself using evidence from Modules 1–6. Then complete
   `recreated_tool_fit.md`.
3. Compare at least:

- manual process improvement;
- spreadsheet configuration;
- the current local Python workflow;
- a general workflow platform;
- bought SME software with existing exception features;
- custom cloud service;
- no AI;
- bounded replaceable AI summary.

4. For every option record fit, evidence, implementation time, licence or usage
cost, review, support, security, data location/transfer, portability, exit,
failure route, and owner.
5. Your Course 1 decision should keep the local Python proof with the mock
summary for learning, preserve the manual fallback, and state that a real
client recommendation depends on the client's existing tools. It must not
claim production readiness.
6. Add a data-flow list from CSV input through issue output, summary, approval,
local draft, retention, and deletion. Mark every boundary and owner.
7. Add a scope-change test for real employee names plus automatic email. The
   result must be `DO NOT CONTINUE` until a separate qualified assessment is
   complete.

Verify:

```powershell
Select-String -Path .\recreated_risk_screen.md,.\recreated_tool_fit.md -Pattern 'synthetic','manual fallback','owner','exit','DO NOT CONTINUE'
```

**Expected result:** all five concepts appear. Missing output means the
worksheets are incomplete, not that PowerShell failed.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path` to obtain the full path. Replace
`[PASTE FULL PATH HERE]` and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
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

Return:
1. PASS or NOT YET;
2. checks for: intended purpose; complete data flow; personal-data screen;
consequence and AI-use screen; synthetic-only scope; at least seven realistic
options including improve/configure/buy/build/no-AI; evidence rather than
preference; security baseline; transfer and retention; total ownership cost;
named access/backup/incident/exit owners; portability; manual fallback; no
production-readiness claim; scope changes trigger DO NOT CONTINUE and
reassessment; worked
example correctly rejects unnecessary AI;
3. the smallest corrections for me to make if NOT YET.

Remain read-only. Do not make a legal conclusion or replacement recommendation.
```

## Pass criteria

- [ ] Intended purpose and end-to-end data flow are explicit.
- [ ] Personal-data and consequence screens use evidence or say unknown.
- [ ] Options include improve, configure, buy, build, and no AI.
- [ ] The selected tool follows evidence, not enthusiasm.
- [ ] Security, transfer, retention, deletion, support, cost, and exit are
      addressed proportionately.
- [ ] Every continuing responsibility has a role owner.
- [ ] Manual fallback remains viable.
- [ ] Material scope changes stop and reopen assessment.
- [ ] No legal approval or production-readiness claim is made.
- [ ] Codex returns `PASS` read-only.

### Record your Module 7 PASS in Git

Do this only after Codex returns `PASS`. Rerun Stage 1 in this same PowerShell
window so the exact marker and Git-root checks pass again.

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-07"
git commit --only -m "complete module 7 evidence" -- "evidence/module-07"
git status --short
```

`git commit --only` restricts this checkpoint to the repeated module path,
even if a different file had already been staged. If Git reports
`nothing to commit`, confirm that the module evidence was already recorded and
unchanged. Never add secrets, real data, or unrelated files.

## Consultant lens

Clients pay for fit and control, not code volume. Recommending a spreadsheet
configuration or existing product can be better consulting than selling a
custom AI build.

## Capstone increment

The capstone has a Dutch SME guardrail screen, data flow, proportionate tool
decision, ownership, security baseline, cost/exit view, and reassessment
triggers.

## Required artifact

The teaching contract creates the worked decision, worked scope change, and two
completed recreated worksheets under `evidence/module-07`.

## Test gate

The **Pass criteria** are the complete gate.

## Stop or rework

Stop when data necessity is unknown, the use affects people or safety, external
action enters scope, no owner accepts continuing duties, vendor terms or
transfer remain unknown, or the solution is chosen before alternatives.

## Common failures

- Treating “minimal risk” as “no obligations.”
- Buying before mapping existing capabilities.
- Comparing licence price while ignoring support and exit.
- Calling pseudonymous data anonymous.
- Presenting screening as legal advice.

## Estimated time

8–12 hours.
