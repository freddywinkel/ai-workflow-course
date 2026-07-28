# Foundation 7 — Artificial Intelligence (AI) and Controlled Workflows

A **workflow** is connected human and system activity that moves one unit of
work from a trigger to a declared completion or exception. **Evidence** is
material that supports a claim. A **manual route**, also called a manual
fallback, is the documented safe way to continue or stop without automation.

## Outcome

You will build a small fictional workflow record that separates exact rules,
AI drafting, and human authority. Every draft claim will point to evidence, and
the workflow will have a visible stop and manual route.

## Words you need first

- **Artificial intelligence (AI)** is a broad name for computer systems that
  perform tasks associated with prediction, recognition, language, or
  decision support.
- A **model** is a trained computational component that maps input to candidate
  output.
- A **large language model (LLM)** is a model that interprets and generates text
  by predicting sequences of text pieces.
- A **prompt** is the instruction and context supplied to a model.
- **Context** is the information available to the model for one request.
- A **token** is a piece of text used to measure model input and output.
- A **hallucination** is plausible-looking output that is false or unsupported.
- **Probabilistic** output can vary between valid runs.
- A **schema** is a declared data structure. A schema can constrain shape but
  cannot prove that a value is true.
- **Comma-separated values (CSV)** is a plain-text table format.
- An **identifier (ID)** is a stable value that identifies one record.
- **Provenance** records where data came from and how it changed.
- **Grounding** means constraining a result to supplied, verified evidence.
- A **prompt injection** is untrusted input that tries to override workflow or
  model instructions.
- **Human review** is meaningful when an authorised person can see evidence,
  correct, reject, or escalate, and is not pressured to approve.
- An **audit event** records a significant action, actor or component, time,
  subject, and result.
- An **external-actions safety control** prevents a workflow from sending or
  changing anything outside its local practice files. In this course it is
  written unambiguously as `EXTERNAL_ACTIONS_ENABLED=false`.
- A **deterministic rule** produces the same result for the same input and rule
  version.
- **Autonomy** is the degree to which a system may act without a person's
  approval at that moment.
- **Write-back** means changing data in a source or connected business system.
- A **synthetic** record is deliberately fictional practice data.
- A **network service** is software reached over a computer network rather than
  used only through local files.
- **PowerShell** is the Windows command shell used to create and inspect the
  practice files. **Notepad** is the Windows plain-text editor used to enter
  them.
- A **rule code** or **reason code** is a stable machine-readable label for an
  exact rule or its result, such as `R001`.
- An **intended purpose** states the authorised user, context, input, function,
  and output.
- **Negative scope** states what the workflow will not do.
- A **credential** is a secret value, such as a password, key, or token, that
  can grant access.
- `YYYY-MM-DD` means four-digit year, two-digit month, and two-digit day,
  separated by dashes.
- **Codex** is the AI assistant used for the final read-only check. The check
  prompt limits it to one practice folder.

AI output is a candidate. It is not automatically a fact, source, approval, or
business decision.

## Allocate work before choosing AI

| Best owner | Suitable work | Example |
|---|---|---|
| Deterministic rule | exact repeatable check | required field, allowed status, duplicate ID |
| AI model | bounded interpretation or drafting | summarise already verified issue records |
| Authorised person | judgement, correction, exception, or consequential action | correct a source value, accept risk, approve sending |

Use the lowest autonomy that creates useful value. This foundation permits
internal drafts only. It does not permit automatic sending, purchasing,
payment, deletion, approval, access change, or source-system write-back.

## The controlled pattern

```text
receive allowed synthetic input
→ preserve the source
→ validate the structure
→ run exact rules
→ route failures visibly
→ optionally create a bounded draft
→ check every draft claim against evidence
→ let an authorised person accept, edit, reject, or escalate
→ record the outcome
→ retain a manual fallback and `EXTERNAL_ACTIONS_ENABLED=false`
```

An LLM may change. The process definition, rules, evidence, tests, review
design, and ownership are the durable implementation.

## Safety boundary

Use only the fictional records below. Do not paste employer documents,
spreadsheet exports, emails, personal data, credentials, or confidential
instructions into any AI service.

## Follow along — I show you exactly how

Expected result: three local synthetic files separate issue evidence,
responsibility, and a reviewed draft whose claims cite existing issue IDs.

### Prerequisites and start state

- Foundations 1–6 are complete.
- PowerShell and Notepad are available.
- `Documents\controlled-ai-course-practice` exists.
- No live model, network service, or real data is required.

### Part A — create the lesson folder and issue evidence

Open PowerShell and run:

```powershell
Set-Location ([Environment]::GetFolderPath("MyDocuments"))
```

```powershell
Set-Location "controlled-ai-course-practice"
```

```powershell
New-Item -ItemType Directory -Path "foundation-07"
```

```powershell
Set-Location "foundation-07"
```

What the setup commands do: they enter Documents, enter the existing practice
root, create only `foundation-07`, and enter it.

Run:

```powershell
notepad "issue_records.csv"
```

Enter:

```csv
issue_id,request_id,rule_code,severity,message
ISS-31,REQ-31,R001,high,Required owner role is missing
ISS-32,REQ-32,R004,medium,Due date does not use YYYY-MM-DD
```

Save and close Notepad.

What this does: it creates two deterministic issue records. The stable issue ID
and rule code let a later statement point back to exact evidence.

### Part B — record the intended purpose and responsibility

Run:

```powershell
notepad "controlled_workflow.md"
```

Enter:

```markdown
# Synthetic request-triage workflow

## Intended purpose

This workflow assists an operations reviewer by summarising verified synthetic
issue records into an internal draft. It does not correct source values, decide
priority, contact anyone, or perform an external action.

## Responsibility

| Step | Owner | Reason |
|---|---|---|
| Check required fields and date shape | Deterministic rule | The rule is exact and testable |
| Draft an internal issue summary | AI model or person | Wording may vary but must cite issue IDs |
| Accept, edit, reject, or escalate | Authorised reviewer | A person owns judgement and exceptions |

## Failure route

Invalid input or an unsupported draft receives reason code NEEDS_MANUAL_REVIEW.
The reviewer uses the issue records directly.
`EXTERNAL_ACTIONS_ENABLED=false` blocks every external action but does not hide
existing issue records.
```

Save and close Notepad.

### Part C — create and review an evidence-linked draft

Run:

```powershell
notepad "draft_summary.md"
```

Enter:

```markdown
# Internal synthetic draft

Two issues require review.

- REQ-31 has no recorded owner role. Evidence: ISS-31.
- REQ-32 has a due date that does not use YYYY-MM-DD. Evidence: ISS-32.

Limitations: no source value was corrected and no external action occurred.

Reviewer decision: accepted for this synthetic demonstration.
Reviewer role: course learner.
```

Save and close Notepad.

What this demonstrates:

- the number `Two` can be recalculated from the issue file;
- each factual sentence cites one issue ID;
- the draft does not invent an owner, corrected date, cause, or decision;
- the reviewer records a bounded decision.

Run:

```powershell
Import-Csv -LiteralPath ".\issue_records.csv" | Format-Table -AutoSize
```

Run:

```powershell
Get-Content -LiteralPath ".\draft_summary.md"
```

Run:

```powershell
(Get-Location).Path
```

What the three verification commands do: they read and display the issue
records and draft, then print the exact full folder path. They do not change
the evidence.

### Expected result — exact

- `issue_records.csv` contains exactly `ISS-31` and `ISS-32`;
- `controlled_workflow.md` assigns exact checks, drafting, and review to three
  different responsibilities;
- `draft_summary.md` contains exactly two supported issue claims;
- both claims cite existing issue IDs;
- the files state that no source correction or external action occurred.

### Troubleshooting

- If a draft sentence has no supporting issue ID, label it unsupported and
  remove or reject it; do not invent evidence.
- If a CSV row becomes one long column, check commas and the `.csv` extension.
- If `foundation-07` already exists, do not delete it. Confirm it contains only
  synthetic practice before continuing.
- A model is optional here. If you use one, provide only the two fictional issue
  rows and keep the human review steps unchanged.

## Now recreate it yourself

Create a different synthetic inventory-request example in the same folder:

1. `recreated_issues.csv` with:
   - issue `II-71` for request `INV-71`, rule `R010`, severity `high`, message
     `Duplicate reference detected`;
   - issue `II-72` for request `INV-72`, rule `R007`, severity `medium`, message
     `Owner role is missing`.
2. `recreated_draft.md` with:
   - one supported sentence citing `II-71`;
   - one supported sentence citing `II-72`;
   - one deliberately unsupported sentence:
     `The supplier caused the duplicate.`
3. Add a reviewer section that explicitly rejects the unsupported sentence,
   retains the two supported sentences, and confirms no external action.
4. Add a manual fallback: read the two issue records directly and route them to
   the fictional reviewer role.

This tests whether you can recognise unsupported causal language rather than
copying the first draft.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, or delete anything. Do not call a model or
external service. Do not change any review decision.

Report PASS or NOT YET for each criterion:
1. issue_records.csv contains exactly ISS-31/R001 and ISS-32/R004 with the
   stated fictional messages.
2. controlled_workflow.md assigns exact checks to rules, drafting to an AI
   model or person, and authority to a reviewer.
3. draft_summary.md makes exactly two issue claims and cites ISS-31 and ISS-32.
4. recreated_issues.csv contains exactly II-71/R010 and II-72/R007.
5. recreated_draft.md contains two supported cited statements, identifies and
   rejects the unsupported supplier-cause sentence, and records no external
   action.
6. Both examples include a visible manual or failure route.

Explain NOT YET in beginner language and make no changes.
This folder must contain synthetic course data only. I must not include
secrets, personal data, client data, employer data, or other work data. If you
notice such content, stop, do not repeat it, and tell me to remove it locally.
Confirm that the folder contains no secrets and no real employer, client, or
work data.
```

## Pass criteria

- [ ] I can distinguish deterministic rules, AI drafting, and human authority.
- [ ] Every retained factual draft statement points to an existing issue ID.
- [ ] I identified and rejected the deliberately unsupported causal statement.
- [ ] I can explain hallucination, grounding, prompt injection, provenance, and
      meaningful human review.
- [ ] Both examples state negative scope and a manual or failure route.
- [ ] No external action, live model, secret, or real data was used.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
