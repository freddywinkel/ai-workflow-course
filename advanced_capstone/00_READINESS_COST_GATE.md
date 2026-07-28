# Capstone Gate 0 — Readiness, Data Boundary, and the €60 Maximum

## Outcome

You will create a written go/no-go record before any paid-capable Google Cloud
service is called. You will understand why the €60 figure is a maximum
allocation, not a target or a guaranteed technical cutoff.

## Start here

Do not run the cloud deployment if any statement is false:

- Course 1 is complete or you can explain its controlled workflow;
- you know that Google Cloud Platform (GCP) is a collection of hosted services;
- you can use Windows PowerShell, the Windows command application;
- you understand that the Google Cloud Command Line Interface (CLI) is the
  `gcloud` program;
- the Billing page visibly says **Free trial**;
- the page still shows an **Activate** button, proving paid activation was not
  performed;
- the trial credit expiry is **26 October 2026**;
- no real employer, client, medical, personal, quality-system, or confidential
  document will be used;
- you can delete the dedicated project after the proof.

Stop if the account says paid, invoiced, upgraded, postpay, or anything other
than Free trial. Never click **Activate** during this course.

## What the cost controls really do

| Control | What it protects | Important limit |
|---|---|---|
| Free Trial remains unactivated | prevents a payment-method charge during the trial | resources stop when credit/trial ends |
| €40 project budget alerts | warns at 25%, 50%, 75%, 90%, and 100% | ordinary budgets do not stop use |
| €5 Vertex AI spend cap, if offered | pauses new eligible Gemini use | Preview, delayed, service-specific |
| €5 Cloud Run spend cap, if offered | pauses new eligible Cloud Run use | Preview, delayed, service-specific |
| six exact file hashes | rejects every unknown document | adding a new fixture requires a reviewed manifest change |
| 20-run and 60-page lifetime counter | limits live provider calls | stored transactionally in Firestore |
| maximum three pages and 5 megabytes | bounds each request | not a price guarantee |
| Cloud Run maximum one instance/concurrency one | throttles parallel use | brief platform overage can occur |
| 20 October hard stop | leaves six days for teardown | computer clock and configuration must be correct |
| immediate teardown | stops further use | source-deploy images also need deletion |

The €40 alert plus the €5 + €5 eligible-service caps leave at least €10 of the
€60 allocation untouched. Document AI is not covered by the current spend-cap
Preview. The six-file allowlist, page limits, authentication, counters, and
same-session teardown cover that gap.

Plan the exit before deploying: the ordinary alerts-only budget can be deleted
through the public Cloud Billing Budget application programming interface
(API). The two Preview spend caps require deletion and absence verification in
the Billing user interface. Lab 9 shows both paths separately.

## Follow along — I show you exactly how

### Step 1 — Create a private evidence folder

Open Windows PowerShell. Run:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$gateFolder = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\controlled-intake-capstone\evidence\gate-00'
New-Item -ItemType Directory -Force -Path $gateFolder | Out-Null
Set-Location -LiteralPath $gateFolder
notepad .\worked_readiness.md
```

Click **Yes** if Notepad asks to create the file. Paste:

```markdown
# Worked cloud readiness decision

Date checked: 2026-07-28
Data class: frozen synthetic course PDFs only
Maximum allocation: EUR 60
Project alert: EUR 40
Eligible service caps: EUR 5 Vertex AI and EUR 5 Cloud Run, if available
Application caps: 20 live runs, 60 pages total, 3 pages per PDF
Live-call hard stop: 2026-10-20
Credit expiry: 2026-10-26
Paid activation allowed: NO
Activate button clicked: NO
Real client/work/medical/personal data allowed: NO
Public unauthenticated service allowed: NO
Teardown required in the same work session: YES

Decision: READY FOR LOCAL WORK ONLY

Cloud deployment remains locked until the Billing page is checked again,
the dedicated project exists, the EUR 40 alerts are present, and any available
service spend caps are present.
```

Save and close.

### Step 2 — Verify the implementation limits without calling Google

Run:

```powershell
$demoRoot = Join-Path $courseRoot 'future_courses\course_04_controlled_document_ai\controlled_document_intake_demo'
Select-String -Path (Join-Path $demoRoot '.env.example') -Pattern 'MAX_|LIVE_HARD_STOP|LOCATION|GEMINI_MODEL'
Get-Content (Join-Path $demoRoot 'fixtures\manifest.json') | Select-String -Pattern '"case_id"|"sha256"'
```

Expected result:

- `DOCUMENT_AI_LOCATION=eu`;
- `VERTEX_LOCATION=eu`;
- maximum 20 runs and 60 total pages;
- three pages per document;
- hard stop 20 October 2026;
- model `gemini-3.5-flash-lite`;
- six case identifiers and six SHA-256 values.

No cloud resource is created by these commands.

### Step 3 — Record a no-go trigger

Add this to `worked_readiness.md`:

```markdown
Immediate no-go trigger:
If the Billing page does not visibly say Free trial and show an Activate
button, stop. Do not deploy, enable APIs, link another billing account, or
change the account to paid.
```

## Now recreate it yourself

Create `recreated_readiness.md` without copying the worked decision. Use a
different layout and explain, in your own words:

- why €60 is not a guaranteed hard cap;
- why the alert is set to €40;
- which two services may have €5 spend caps;
- why Document AI still needs application controls;
- which six files are allowed;
- why 20 October is earlier than 26 October;
- what exact screen evidence must be checked before deployment;
- what would make you stop.

Set your current decision to one of:

- `LOCAL WORK ONLY`;
- `READY FOR GUARDED CLOUD PREFLIGHT`; or
- `NO-GO`.

Do not write `READY FOR GUARDED CLOUD PREFLIGHT` until you actually check the
Free Trial screen and the budget controls.

## Ask Codex to check your work

Run `(Resolve-Path $gateFolder).Path`, insert the result below, and send:

```text
READ-ONLY CAPSTONE GATE REVIEW.

I authorize inspection of only this full folder:
[PASTE FULL PATH]

Do not edit, create, delete, rename, move, upload, or execute anything. Do not
open a browser or change Google Cloud. Stop if the folder contains credentials,
billing account identifiers, personal data, health data, employer data, or a
real document.

Check worked_readiness.md and recreated_readiness.md. Return PASS or NOT YET
for: synthetic-only boundary; no paid activation; EUR 60 maximum; EUR 40 alert;
eligible EUR 5 service caps described as limited; 20-run/60-page/3-page limits;
2026-10-20 hard stop; 2026-10-26 expiry; same-session teardown; exact no-go
trigger; learner explanation in different wording. List evidence by filename.
```

## Pass criteria

- Both readiness files exist.
- Neither contains a credential, billing account identifier, or real data.
- The learner can explain alert versus spend cap versus application cap.
- The exact dates 20 and 26 October 2026 are not confused.
- Paid activation is explicitly forbidden.
- The current decision is honest.
- Codex returns PASS.

## Stop conditions

Stop and use `NO-GO` if billing status is ambiguous, a paid upgrade is
requested, the Free Trial cannot be proved, the budget controls are missing,
or any real data is proposed.
