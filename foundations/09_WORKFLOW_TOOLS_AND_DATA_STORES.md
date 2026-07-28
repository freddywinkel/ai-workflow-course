# Foundation 9 — Workflow Tools and Data Stores

A **workflow** is connected human and system activity that moves one unit of
work from a trigger to a declared completion or exception. **Architecture** is
the documented arrangement of components, data, and responsibilities. **Source
input** is the received record or unchanged snapshot. **Workflow state**, also
called work state, is the current status, owner, timestamps, and reason code. An
**audit event** is a structured record of a significant business or control
event.

## Outcome

You will document a minimal fictional workflow architecture, separate source
input from work state and audit events, assign ownership, and explain why the
simplest maintainable tool is the correct starting point.

## Words you need first

- A **trigger** is the event, schedule, or manual action that starts a workflow.
- An **orchestrator** is software that triggers, connects, routes, waits for,
  and monitors workflow steps.
- A **node** is one configured step in a visual orchestrator.
- A **credential** is a secret value, such as a password, key, or token, that
  can grant access.
- An **integration** is a deliberate connection through which systems exchange
  data or actions.
- A **connector** is an integration that communicates with another system using
  declared permissions and credentials.
- **Artificial intelligence (AI)** is a broad name for computer systems that
  perform prediction, recognition, language, or decision-support tasks.
- An **application programming interface (API)** is an agreed interface through
  which software sends requests and receives responses.
- **Configuration** is the settings that determine how software behaves.
- **Low-code** describes development that uses visual configuration while still
  requiring logic, permissions, tests, and maintenance.
- A **data store** holds information beyond one program step.
- **Comma-separated values (CSV)** is a plain-text table format.
- An **identifier (ID)** is a stable value that identifies one record.
- A **database** is structured durable storage that can be queried and updated.
- A **relational database** stores rows in related tables and can enforce
  constraints.
- A **binary object** stores non-plain-text content as computer bytes, such as a
  document or image file.
- **Object storage** holds files or other large binary objects.
- A **log** is time-ordered operational information used mainly to understand
  what software did.
- A technical log is not automatically an authoritative audit record.
- A **reason code** is a stable machine-readable label for a result, such as
  `R001`.
- **Write-back** means changing data in a source or connected business system.
- A **system of record** is the authorised source in which the official value
  is maintained.
- **Discovery** is the early work of understanding a process and its problem.
  A **pilot** is a limited trial used to test assumptions before a wider
  implementation.
- **Concurrency** means multiple work items or actions can be active at the same
  time. **Access control** determines who or what may view or change something.
  **Durable state** remains available after a program step or restart.
- **Monitoring** observes whether a workflow is operating as expected.
  **Recovery** is the documented method for restoring safe operation after a
  failure.
- **Markdown** is a plain-text documentation format.
- **PowerShell** is the Windows command shell used to create and inspect the
  practice files. **Notepad** is the Windows plain-text editor used to enter
  them.
- A **manual fallback** is the documented safe way to continue or stop without
  automation.
- A **synthetic** record is deliberately fictional practice data. A **dataset**
  is a collection of related records used together.
- A **server** is software that stays running to listen for requests.
- A **network call** communicates with another computer or online service. A
  **public deployment** makes software available beyond the local practice
  computer.
- A **deterministic rule** produces the same result for the same input and rule
  version.
- `Import-Csv` reads CSV rows into PowerShell objects. `Format-Table` displays
  those objects as a table, `-AutoSize` adjusts displayed column widths, and
  `Get-ChildItem` lists files and folders.
- **Codex** is the AI assistant used for the final read-only check. The check
  prompt limits it to one practice folder.

**n8n** is a product name for a workflow automation tool. **Microsoft Power
Automate** is a workflow product in the Microsoft business-software ecosystem.
Both are examples of visual orchestrators.
Knowing either product is less durable than knowing the process, rules, data,
exceptions, evidence, ownership, and fallback.

## Four data categories

1. **Source input** — the received record or unchanged snapshot.
2. **Workflow state** — current status, owner, timestamps, and reason code.
3. **Derived artifact** — an issue, calculation, draft, or summary created from
   the source.
4. **Audit event** — what happened, to which item, by which role or component,
   and with what result.

Do not silently overwrite source evidence. A correction should become a new
version or an authorised change in the system of record.

## Add tools only for named requirements

A spreadsheet and manual review may be enough for discovery or a small
synthetic demonstration. Add an orchestrator, code service, or database only when a
requirement such as concurrency, access control, durable state, integration,
volume, monitoring, or recovery justifies the extra ownership.

**Docker** is a product family for packaging and running software in isolated
containers. An **image** is the package definition, a **container** is a running
instance, and a **volume** preserves selected data. Docker does not by itself
provide correct rules, access control, a backup, or an owner.

## Safety boundary

This lesson uses local fictional CSV and Markdown files. It makes no connector,
network call, external write, public deployment, or workplace-system change.

## Follow along — I show you exactly how

Expected result: four local synthetic files separate source input, workflow
state, audit events, and the documented minimal architecture that owns them.

### Prerequisites and start state

- Foundations 1–8 are complete.
- PowerShell and Notepad are available.
- `Documents\controlled-ai-course-practice` exists.
- No work account, connector, credential, or real dataset is open.

### Start or resume safely — run this at every new PowerShell session

Run this whole block whenever you start or resume Foundation 9:

```powershell
$documentsPath = [Environment]::GetFolderPath("MyDocuments")
$practiceRoot = Join-Path $documentsPath "controlled-ai-course-practice"
$lessonFolderName = "foundation-09"
if ($lessonFolderName -notmatch '^foundation-09(?:-retry-\d{2,})?$') {
    throw "STOP: use foundation-09 or a retry name created by this lesson."
}
$lessonPath = Join-Path $practiceRoot $lessonFolderName

function New-FoundationRetryAttempt {
    param([string]$BaseName, [string]$PracticeRoot)
    $retryNumber = 1
    do {
        $retryName = "$BaseName-retry-{0:D2}" -f $retryNumber
        $retryPath = Join-Path $PracticeRoot $retryName
        $retryNumber += 1
    } while (Test-Path -LiteralPath $retryPath)
    New-Item -ItemType Directory -Path $retryPath -ErrorAction Stop | Out-Null
    $retryPath
}

function Open-GuardedPracticeFile {
    param([string]$AttemptPath, [string]$FileName)
    $filePath = Join-Path $AttemptPath $FileName
    if (Test-Path -LiteralPath $filePath -PathType Container) {
        throw "STOP: $FileName is a folder. Do not change it; use a fresh retry attempt."
    }
    if (Test-Path -LiteralPath $filePath -PathType Leaf) {
        "EXISTING — DO NOT EDIT OR OVERWRITE: $FileName"
        Get-Content -LiteralPath $filePath
        return
    }
    New-Item -ItemType File -Path $filePath -ErrorAction Stop | Out-Null
    "CREATED ONCE — enter the requested content: $FileName"
    notepad $filePath
}

if (-not (Test-Path -LiteralPath $practiceRoot -PathType Container)) {
    throw "STOP: the controlled-ai-course-practice folder is missing. Return to Foundation 1."
}
if (Test-Path -LiteralPath $lessonPath -PathType Leaf) {
    throw "STOP: the selected Foundation 9 attempt is a file, not a folder. Do not change it."
}
if (-not (Test-Path -LiteralPath $lessonPath -PathType Container)) {
    New-Item -ItemType Directory -Path $lessonPath | Out-Null
    "Created a new Foundation 9 attempt: $lessonFolderName"
}
else {
    "Existing Foundation 9 attempt found; nothing was overwritten: $lessonFolderName"
}

Set-Location -LiteralPath $lessonPath
Get-Location
Get-ChildItem -Force
```

Expected result: the location ends in `foundation-09` or the selected numbered
retry name. The block creates an absent attempt and lists existing contents
without changing them.

### Decide whether to resume or use a fresh attempt

The two helper functions have narrow jobs:
`New-FoundationRetryAttempt` creates the next unused retry folder;
`Open-GuardedPracticeFile` creates a named file only when absent, or displays an
existing file without opening it for editing.

Apply this decision before Part A and after every interruption:

1. An empty attempt continues at Part A.
2. The only expected names are `queue_input.csv`, `work_state.csv`,
   `audit_events.csv`, `architecture.md`, `service_input.csv`,
   `service_state.csv`, `service_audit.csv`, and `service_architecture.md`. For
   an attempt containing only those names, use each guarded step:
   - `EXISTING` plus exactly complete synthetic content means leave the file
     unchanged and skip its creation;
   - an absent expected file may be created;
   - incomplete, different, unfamiliar, or apparently real/sensitive content
     means do not edit, rename, delete, or overwrite anything.
3. An unexpected item also requires a fresh attempt.
4. For either stop condition, run:

   ```powershell
   $lessonPath = New-FoundationRetryAttempt -BaseName "foundation-09" -PracticeRoot $practiceRoot
   $lessonFolderName = Split-Path -Leaf $lessonPath
   Set-Location -LiteralPath $lessonPath
   "Selected fresh attempt: $lessonFolderName"
   ```

5. Record the retry name. In a new PowerShell session, replace only
   `"foundation-09"` in `$lessonFolderName` with that exact name. Restart at
   Part A in the new empty folder.

### Part A — create source input, state, and audit event files

Run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "queue_input.csv"
```

If it reports `EXISTING`, leave the file unchanged only when it exactly matches
the complete source below; otherwise use a fresh retry attempt. Only after
`CREATED ONCE` should you enter:

```csv
work_item_id,title,owner_role
WI-901,Synthetic queue request,
```

Save and close Notepad.

What this is: the unchanged fictional source input. The blank owner is
deliberate.

Run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "work_state.csv"
```

If it reports `EXISTING`, leave the file unchanged only when it exactly matches
the complete state below; otherwise use a fresh retry attempt. Only after
`CREATED ONCE` should you enter:

```csv
work_item_id,state,review_owner_role,last_reason_code
WI-901,needs_review,operations,R001
```

Save and close Notepad.

What this is: the workflow's current state and review ownership. It does not
alter `queue_input.csv`.

Run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "audit_events.csv"
```

If it reports `EXISTING`, leave the file unchanged only when it exactly matches
the complete events below; otherwise use a fresh retry attempt. Only after
`CREATED ONCE` should you enter:

```csv
event_id,work_item_id,event_type,occurred_on,actor_role,result
EV-901,WI-901,issue_detected,2026-08-01,rule_checker,R001
EV-902,WI-901,review_queued,2026-08-01,workflow,needs_review
```

Save and close Notepad.

What this is: two business-relevant events. The dates are fictional.

### Part B — document the minimal architecture and ownership

Run the create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "architecture.md"
```

If it reports `EXISTING`, leave the file unchanged only when it exactly matches
the complete architecture below; otherwise use a fresh retry attempt. Only
after `CREATED ONCE` should you enter:

```markdown
# Synthetic queue architecture

## Flow

Manual trigger
→ read queue_input.csv without changing it
→ apply deterministic required-owner rule
→ record work_state.csv and audit_events.csv
→ operations reviewer handles the exception manually

## Tool decision

Selected: local CSV files plus PowerShell inspection.

Reason: one synthetic item does not justify an orchestrator, connector,
database, Docker container, or external AI model.

## Ownership

| Responsibility | Owner role |
|---|---|
| Process rule | operations process owner |
| Source input | fictional data owner |
| Exception review | operations reviewer |
| File maintenance | course learner |
| Stop and manual fallback | operations process owner |

## Boundaries

No connector, write-back, external action, real data, or public deployment.
Manual fallback: read the source row and issue reason directly.
```

Save and close Notepad.

What this does: it records why the smallest architecture fits the current
requirement and who would own each responsibility.

### Part C — verify the separation

Run:

```powershell
Import-Csv ".\queue_input.csv" | Format-Table -AutoSize
```

Run:

```powershell
Import-Csv ".\work_state.csv" | Format-Table -AutoSize
```

Run:

```powershell
Import-Csv ".\audit_events.csv" | Format-Table -AutoSize
```

Run:

```powershell
Get-ChildItem
```

Run:

```powershell
(Get-Location).Path
```

What the verification commands do: the first three read and display source,
state, and audit rows; `Get-ChildItem` lists the files; the last command prints
the exact full folder path. None changes the stored data.

### Expected result — exact

- `queue_input.csv` has one source row with a blank owner;
- `work_state.csv` has one state row for the same ID and reason `R001`;
- `audit_events.csv` has exactly two events, `EV-901` and `EV-902`;
- `architecture.md` chooses a local minimal toolset and assigns five owner
  roles;
- `Get-ChildItem` lists exactly those four files before the recreation exercise.

### Troubleshooting

- If a CSV displays as one column, preserve that attempt and use a fresh retry
  with commas and the correct `.csv` extension.
- If IDs do not match across files, do not correct or overwrite that attempt.
  Preserve it and use a fresh retry before claiming traceability.
- If a tool suggestion requires credentials or a public connection, stop. It
  is outside this foundation.
- If the selected attempt already exists, do not delete or overwrite it. Apply
  the attempt decision and use a fresh retry for any non-complete file.

## Now recreate it yourself

Create a separate fictional service-notice architecture using four new files.
Before entering each file, run its create-once guard:

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "service_input.csv"
```

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "service_state.csv"
```

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "service_audit.csv"
```

```powershell
Open-GuardedPracticeFile -AttemptPath $lessonPath -FileName "service_architecture.md"
```

Run and finish one guard before moving to the next. Leave an `EXISTING` file
unchanged only when it already meets its complete requirement below. Any other
existing content requires a fresh retry attempt; do not edit or overwrite it.
After `CREATED ONCE`, use these requirements:

1. `service_input.csv` — one source row with notice ID `SN-81`, category
   `maintenance`, and blank `assigned_role`;
2. `service_state.csv` — state `manual_review`, reviewer role
   `service_coordinator`, and a new reason code for missing assignment;
3. `service_audit.csv` — exactly two events: issue detection and manual-review
   routing, both linked to `SN-81`;
4. `service_architecture.md` — document trigger, rule, human review, manual
   fallback, no-write-back boundary, tool choice, and owner roles.

Choose a different reason code and event IDs from the guided example. Explain
why a local file design is sufficient for this one-item synthetic exercise and
name one future requirement that could justify a database or orchestrator.

## Ask Codex to check your work

Replace `[PASTE THE EXACT PATH]` with the full path output from
`(Get-Location).Path`.

```text
You may inspect READ-ONLY this one practice folder and no other location:
[PASTE THE EXACT PATH]

Do not create, edit, move, rename, or delete anything. Do not start a
container, server, workflow, connector, model, or external service. Run only
read-only file and CSV inspection.

Report PASS or NOT YET for each criterion:
1. The guided queue_input, work_state, and audit files link WI-901 to R001 and
   exactly two audit events without changing the source row.
2. architecture.md selects the local minimal toolset, assigns the five owner
   roles, and states no connector or write-back.
3. The recreated service files all link to SN-81 and use a new reason code.
4. service_audit.csv has exactly two traceable events.
5. service_architecture.md includes trigger, exact rule, human review, manual
   fallback, boundaries, owners, and one future requirement that could justify
   a larger tool.
6. The expected fictional identifiers and roles are present; report any
   apparent sensitive content only under the non-disclosure rule below.

Explain NOT YET in beginner language and make no changes.
I attest that I created this attempt with synthetic course data only and did
not intentionally add secrets, personal data, client data, employer data, or
other real work data. If you notice content that appears sensitive, stop the
inspection,
do not quote or repeat it, report only the file name and general category, and
report NOT YET. If you notice none, say: "No apparent sensitive content noticed
in this bounded inspection; this is not proof that none exists." Do not claim
that an inspection proves the folder is free of secrets or real data.
```

## Pass criteria

- [ ] I can distinguish source input, workflow state, derived artifact, log,
      and audit event.
- [ ] IDs connect source, state, and audit evidence in both examples.
- [ ] I can explain trigger, orchestrator, node, connector, API, database, and
      write-back.
- [ ] I selected the smallest sufficient tool and named what might justify a
      larger one.
- [ ] Ownership, manual fallback, and no-write-back boundaries are documented.
- [ ] No account, connector, container, or network service was used. I attest
      that all information I entered was synthetic and that I did not
      intentionally add secrets or real data.
- [ ] Codex reported PASS for every read-only criterion, or I corrected each
      NOT YET item myself.
