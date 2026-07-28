# Module 5 — Design One Bounded, Replaceable Artificial Intelligence (AI) Contribution and Test It Offline

## Outcome

You will add an offline mock of an Artificial Intelligence (AI) summary after
the proven R001-R011 issues. The mock behaves like provider output but makes no
network call and costs nothing.

It may only:

- group verified issue identifiers;
- restate their rule messages;
- propose a source-linked `human_review` action;
- say that human review is required.

It may not discover issues, change severity, decide a business action, contact
anyone, send, order, pay, approve, reject, or write back.

You will first inspect and verify a complete 13-issue example. Then you will
create a differently worded five-issue mock yourself and validate it. You will
also prove the deterministic fallback for disabled AI, timeout, refusal,
malformed JSON, and an invented issue reference.

## Beginner checkpoint

Start when Module 4 has:

- a 13-issue worked result;
- a five-issue recreated result;
- zero false positives and false negatives;
- zero external actions;
- a Codex `PASS`.

**AI** means software that generates or infers an answer. **Application
Programming Interface (API)** means a defined connection through which
software can request a service. This module uses no API.

## What changes — and what does not

```text
unchanged, trusted part                  replaceable language part
----------------------                  -------------------------
synthetic input
      |
R001-R011
      |
verified issue objects  ------------->  offline mock summary
      |                                  |
      +------------------------------->  source-linked review actions
                                         |
                                         v
                                  mandatory human review
```

If the language step fails, the verified issues remain usable. The fallback is
not “ask the AI again”; it is a deterministic summary created from the same
issue records.

## Concepts

- **Bounded** means only named inputs and transformations are permitted.
- **Structured output** follows a machine-checkable shape.
- **Grounding** links each statement to verified evidence.
- **Abstention** means returning no unsupported claim.
- An **adapter** keeps provider-specific behavior separate from the workflow.
- A **prompt version** identifies the instruction set.
- A **fallback** completes the limited task without AI.
- A **mock** is saved or simulated behavior used for repeatable tests.
- A **schema** describes the required structure of data.

Valid structure is not the same as truthful meaning. Code verifies fields and
references; a person still checks whether every sentence is supported.

## Official readings

1. [National Institute of Standards and Technology Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
2. [OpenAI Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs)
3. [OpenAI evaluation best practices](https://platform.openai.com/docs/guides/evals)

OpenAI is one possible provider, not a Course 1 dependency. Do not add a key or
live model here.

## Guided build

The guided path prepares a complete 13-issue offline mock, checks its exact
contract, performs a sentence-level human review, and then forces all five
summary failure modes through the deterministic fallback.

## Start or resume safely

Open Windows PowerShell and run this at the start of every session:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
$moduleFolder = Join-Path $projectRoot 'evidence\module-05'
$moduleFour = Join-Path $projectRoot 'evidence\module-04'
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
$runner = Join-Path $projectRoot 'src\course1_capstone\cli.py'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Project Python missing. Return to Windows Setup.'
}
if (-not (Test-Path -LiteralPath $runner)) {
    throw 'Course 1 runner missing. Return to Module 4 Stage 1.'
}
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot '.git'))) {
    throw 'Project Git repository missing. Return to Windows Setup.'
}
New-Item -ItemType Directory -Force -Path $moduleFolder | Out-Null
Set-Location -LiteralPath $projectRoot
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
if (-not (Test-Path -LiteralPath (Join-Path $courseRoot 'course1_capstone\workflow.py'))) {
    throw 'That course folder does not contain course1_capstone\workflow.py.'
}
& $pythonExe --version
```

Use `& $pythonExe`, never bare `python`.

## Follow along — I show you exactly how

### Stage 1 — Prepare the complete offline-mock run

Run:

```powershell
$workedWorkspace = Join-Path $moduleFolder 'worked-mock'
& $pythonExe $runner prepare `
    --input .\data\input\work_items.csv `
    --expected .\tests\expected_issues.csv `
    --workspace $workedWorkspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
if ($LASTEXITCODE -ne 0) {
    throw 'The mock run safely stopped. Read the message above.'
}
$workedRunLocator = (Get-Content -LiteralPath `
    (Join-Path $workedWorkspace 'latest_run.txt')).Trim()
$workedRunDir = Join-Path $workedWorkspace $workedRunLocator
Get-Content -LiteralPath (Join-Path $workedRunDir 'state.json')
```

**Expected result:**

- `current_state` is `needs_review`;
- `summary_generator` is `offline-mock`;
- `summary_fallback_reason` is `null`;
- external actions are 0;
- no outbox exists.

This is still entirely local. `offline-mock` does not mean a hidden AI call.

### Stage 2 — Inspect exactly what the mock receives and returns

Open these two files side by side in Visual Studio Code:

```powershell
code (Join-Path $workedRunDir 'issues\issues.json')
code (Join-Path $workedRunDir 'draft\summary.json')
```

If `code` is not recognized, open Visual Studio Code normally and use
**File > Open File**.

The summary has these exact top-level fields:

| Field | Meaning |
|---|---|
| `run_id` | the run this summary belongs to |
| `prompt_version` | version of the bounded instruction |
| `generator` | `offline-mock` or `deterministic-fallback` |
| `headline` | short factual count statement |
| `groups` | grouped sentences with visible issue citations |
| `review_actions` | only `human_review`, each linked to issue IDs |
| `unsupported_statements` | must be empty to continue |
| `review_required` | must be `true` |

Each issue ID must appear exactly once in the groups and exactly once in the
review actions. An identifier such as
`WI-0002|R007|owner_role` links the text back to work item, rule, and field.

Run these checks:

```powershell
$summary = Get-Content -Raw -LiteralPath (Join-Path $workedRunDir 'draft\summary.json') | ConvertFrom-Json
$issues = Get-Content -Raw -LiteralPath (Join-Path $workedRunDir 'issues\issues.json') | ConvertFrom-Json
$summary.generator
$summary.review_required
$summary.unsupported_statements.Count
$summary.groups.issue_ids.Count
$summary.review_actions.issue_ids.Count
$summary.review_actions.external_action | Sort-Object -Unique
$issues.Count
```

**Expected result:** `offline-mock`, `True`, `0`, `13`, `13`, only `False`, and
`13`.

### Stage 3 — Perform the human sentence check

Create `evidence\module-05\worked_support_review.md`:

```markdown
# Worked mock support review

Run: [copy run_id from state.json]
Reviewer role: course learner acting as synthetic operations reviewer

## Checks

- opened issues/issues.json: yes
- opened draft/summary.json: yes
- 13 known issue IDs grouped exactly once: yes
- 13 known issue IDs have one human-review action: yes
- every issue ID is visibly cited in its group sentence: yes
- each sentence repeats only its cited rule message: yes
- severity changed: no
- unsupported cause or recommendation: no
- external action proposed: no
- review_required: true

Result: accept the structure as an internal draft for Module 6 review.
This is not approval to export, send, or use with real data.
Fallback: use issues/issues.csv and the deterministic fallback summary.
```

Do not mark a line `yes` until you actually compare it.

### Stage 4 — Prove all five AI failure routes

The modes below are local fault simulations. They do not wait for a real
provider.

A **PowerShell custom object (`[PSCustomObject]`)** is a labelled group of
values used here only to print one readable result row per failure mode.

Run:

```powershell
$failureModes = 'disabled','timeout','refusal','malformed_json','unknown_issue_id'
foreach ($mode in $failureModes) {
    $workspace = Join-Path $moduleFolder "failure-$mode"
    & $pythonExe $runner prepare `
        --input .\data\input\work_items.csv `
        --expected .\tests\expected_issues.csv `
        --workspace $workspace `
        --ai-mode $mode `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw "Unexpected failure while testing $mode"
    }
    $runLocator = (Get-Content -LiteralPath `
        (Join-Path $workspace 'latest_run.txt')).Trim()
    $runDir = Join-Path $workspace $runLocator
    $state = Get-Content -Raw -LiteralPath (Join-Path $runDir 'state.json') | ConvertFrom-Json
    [PSCustomObject]@{
        requested_mode = $mode
        generator = $state.summary_generator
        fallback_reason = $state.summary_fallback_reason
        state = $state.current_state
        external_actions = $state.external_actions
    }
}
```

**Expected result:** every row shows:

- generator `deterministic-fallback`;
- a matching reason: `ai_disabled`, `ai_timeout`, `ai_refusal`,
  `malformed_ai_json`, or `unknown_ai_issue_reference`;
- state `needs_review`;
- external actions `0`.

The malformed and unknown-reference responses do not “mostly pass.” The whole
mock response is discarded and replaced by the deterministic fallback.

### Stage 5 — Prove that instructions inside data are inert

Run:

```powershell
$instructionWorkspace = Join-Path $moduleFolder 'failure-untrusted-text'
& $pythonExe $runner prepare `
    --input (Join-Path $courseRoot 'course1_capstone\fixtures\failures\untrusted_instruction.csv') `
    --workspace $instructionWorkspace `
    --ai-mode mock `
    --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
$instructionRunLocator = (Get-Content -LiteralPath `
    (Join-Path $instructionWorkspace 'latest_run.txt')).Trim()
$instructionRunDir = Join-Path $instructionWorkspace $instructionRunLocator
Select-String -LiteralPath (Join-Path $instructionRunDir 'source\work_items.csv') -Pattern 'Ignore every rule'
Select-String -LiteralPath (Join-Path $instructionRunDir 'draft\summary.json') -Pattern 'Ignore every rule'
```

**Expected result:** the first search finds the text in the preserved source.
The second search prints nothing. Free text is treated as data, not an
instruction, and no external action occurs.

## Now recreate it yourself

Use the five-issue run to create and validate your own differently worded
bounded candidate.

### Recreation 1 — Prepare the different mock

Resume Module 4 variables if necessary, then run:

```powershell
$recreatedInput = Join-Path $moduleFour 'recreated_work_items.csv'
if (-not (Test-Path -LiteralPath $recreatedInput)) {
    throw 'Recreated input missing. Return to Module 4 Recreation 1.'
}
$recreatedWorkspace = Join-Path $moduleFolder 'recreated-mock'
$recreatedLatest = Join-Path $recreatedWorkspace 'latest_run.txt'
if (Test-Path -LiteralPath $recreatedLatest) {
    Write-Host "KEEPING your existing $recreatedWorkspace"
} else {
    & $pythonExe $runner prepare `
        --input $recreatedInput `
        --expected (Join-Path $courseRoot 'course1_capstone\fixtures\recreated_expected_issues.csv') `
        --workspace $recreatedWorkspace `
        --ai-mode mock `
        --synthetic-confirmation I_CONFIRM_SYNTHETIC_DATA_ONLY
    if ($LASTEXITCODE -ne 0) {
        throw 'The recreated mock safely stopped. Read the named reason above.'
    }
}
$recreatedRunLocator = (Get-Content -LiteralPath $recreatedLatest).Trim()
$recreatedRunDir = Join-Path $recreatedWorkspace $recreatedRunLocator
```

### Recreation 2 — Make a new bounded response

Copy the valid mock once, without overwriting a prior attempt:

```powershell
$candidate = Join-Path $moduleFolder 'recreated_candidate_summary.json'
if (Test-Path -LiteralPath $candidate) {
    Write-Host 'KEEPING your existing candidate summary'
} else {
    Copy-Item -LiteralPath (Join-Path $recreatedRunDir 'draft\summary.json') -Destination $candidate
}
code $candidate
```

In your candidate:

1. change the headline wording but keep it factual;
2. change both severity group labels;
3. rewrite each summary sentence in plain language;
4. keep every bracketed issue ID in the sentence it supports;
5. keep each issue ID in exactly one group;
6. keep exactly one `human_review` action per issue;
7. keep every `external_action` as `false`;
8. keep `unsupported_statements` empty;
9. keep `review_required` true;
10. do not add a cause, recommendation, priority change, or external action.

You are recreating the controlled transformation, not merely renaming a file.

### Recreation 3 — Validate your candidate

Run:

```powershell
& $pythonExe $runner validate-summary `
    --run-dir $recreatedRunDir `
    --candidate $candidate
$LASTEXITCODE
Get-Content -LiteralPath (Join-Path $recreatedRunDir 'review\candidate-validation.json')
```

**Expected result:** `PASS`, exit code `0`, five issue references, human support
review required, and external actions 0.

If you receive `unknown_ai_issue_reference`, `uncited_summary`,
`missing_ai_issue_reference`, or `summary_contract`, repair only the named
problem. Do not remove the validator.

### Recreation 4 — Perform your own support review

Create the review at the exact path
`evidence\module-05\recreated_support_review.md`. The command below creates
the review headings once and keeps a prior review unchanged:

```powershell
$recreatedSupportReview = Join-Path $moduleFolder 'recreated_support_review.md'
if (Test-Path -LiteralPath $recreatedSupportReview) {
    Write-Host "KEEPING your existing $recreatedSupportReview"
} else {
    @'
# Recreated support review

| Candidate sentence | Cited issue IDs | Supported by exact rule message? | Added cause/action? | Accept/edit/reject |
|---|---|:---:|:---:|---|

Reviewer role:
Date:
All five issues checked:
Accepted for the Module 6 review package:
Deterministic fallback route:
'@ | Set-Content -LiteralPath $recreatedSupportReview -Encoding utf8
}
notepad $recreatedSupportReview
```

Complete the table with one row per sentence. Then record:

- reviewer role;
- date;
- whether all five issues were checked;
- whether the candidate is accepted for the Module 6 review package;
- the deterministic fallback route.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path`, paste it below, and send:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
[PASTE FULL MODULE-05 PATH]

Do not edit, create, delete, move, rename, format, or execute anything. Do not
inspect a parent folder. This path must contain no secrets and no real client,
real work, personal, or medical data. Stop if it does.

Return:
1. PASS or NOT YET;
2. checks that issue detection remains deterministic and upstream;
3. worked 13-issue mock and learner-created 5-issue candidate;
4. every known issue ID grouped once, visibly cited, and linked to exactly one
human_review action with external_action false;
5. no invented issue, changed severity, cause, recommendation, or action;
6. human sentence-level support reviews and deterministic fallback;
7. evidence for disabled, timeout, refusal, malformed JSON, unknown ID, and
untrusted free-text handling;
8. zero network calls, secrets, paid services, and external actions;
9. the smallest learner-made corrections if NOT YET.

Remain read-only. Do not generate a replacement summary.
```

## Pass criteria

- [ ] Exact project Python is used through `$pythonExe`.
- [ ] The worked mock uses 13 verified issues only.
- [ ] The recreated candidate uses all 5 verified issues only.
- [ ] Every issue is grouped and cited exactly once.
- [ ] Every issue has exactly one source-linked human-review action.
- [ ] `unsupported_statements` is empty and `review_required` is true.
- [ ] Human review checks every sentence against evidence.
- [ ] All five AI failure modes use deterministic fallback.
- [ ] Untrusted free text remains inert source data.
- [ ] No provider, key, network, real data, or external action is used.
- [ ] Codex returns `PASS` in read-only mode.

### Record your Module 5 PASS in Git

Only after Codex returns `PASS`:

```powershell
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence\module-05"
git commit -m "complete module 5 evidence"
git status --short
```

## Consultant lens

The durable asset is the boundary: verified input, constrained output,
reference validation, human meaning check, and fallback. In a later course, an
approved provider or model can be replaced without changing that contract.

## Capstone increment

The capstone now has source-linked offline-mock summaries and human-review
actions plus tested fallbacks. It still waits for a meaningful human decision
and cannot create an export.

## Required artifact

`evidence/module-05` contains the worked mock, human support review, five
fallback runs, untrusted-text result, learner-created five-issue candidate,
candidate validation, and recreated support review.

## Test gate

All Module 5 pass criteria and the read-only Codex review must pass. Every
known issue is grouped, cited, and linked to one human-review action exactly
once; every fault uses fallback; no unsupported or external action survives.

## Stop or rework

Stop if the mock receives unnecessary raw data, invents or omits an issue,
changes severity, includes an unsupported statement, proposes an external
action, uses a provider key, or lacks a deterministic fallback.

## Common failures

- Trusting valid JSON as proof that wording is supported.
- Letting the language step detect deterministic issues.
- Hiding an omitted reference in polished prose.
- Treating the offline mock as a real provider result.
- Weakening the contract after a deliberately malformed response fails.

## Estimated time

8-12 hours, best completed as three to five sessions.

Suggested sessions: three to five sessions of about 2-3 hours.
