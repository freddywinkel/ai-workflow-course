# Capstone Lab 7 — Deploy Privately Without Upgrading to Paid Billing

## Outcome

You will deploy the tested application to a dedicated Google Cloud project
using guarded scripts. You will verify European Union locations, private
access, scale-to-zero, one-instance throttling, and the €60 prototype controls.

This is the first lesson that can consume Google Cloud trial credit. Local
completion is still valid if you stop here. Deployment is optional.

## Non-negotiable gate

Continue only when all of these are true:

- the Billing page visibly says **Free trial**;
- an **Activate** button is still visible;
- you have not clicked **Activate**;
- the billing account has not been upgraded to paid;
- the dedicated project contains no other work;
- the €40 project budget alerts are configured;
- €5 Vertex AI and €5 Cloud Run spend caps are configured if the Preview
  control is available;
- every offline test passed unchanged;
- only the six frozen synthetic Portable Document Format (PDF) files will be
  used;
- you can complete live validation and teardown in this same work session; and
- the date is before the application hard stop on 20 October 2026.

An ordinary budget sends warnings; it does not stop charges. A Preview spend
cap can pause new eligible use, but it is delayed, service-specific, and not a
guaranteed final-price ceiling. The untouched trial state plus application
limits are the strongest protections in this exercise.

## What the bundled reference deployment actually proved

On 28 July 2026, the controlled reference deployment passed its recorded cloud
checks:

- Cloud Run was private through Identity and Access Management (IAM), ready,
  and located in `europe-west4`;
- minimum instances were zero, maximum instances one, concurrency one and
  request timeout 120 seconds;
- Document AI and Vertex AI were both configured for `eu`;
- the metadata health endpoint was `/api/health`;
- the account still showed **Free trial** and **Activate**; and
- paid activation remained `NO`.

This records that the deployment existed and matched its controls. It does not
mean the service is still running: the dedicated project was torn down after
live validation. The displayed cost at the recorded checks was €0, but Google
Cloud Billing reporting can lag, so €0 is not claimed as the final settled
cost.

## Follow along — I show you exactly how

### Step 1 — Prepare the local deployment evidence folder

Open Windows PowerShell:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$capstoneRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\controlled-intake-capstone'
$demoRoot = Join-Path $capstoneRoot 'demo'
$lessonFolder = Join-Path $capstoneRoot 'evidence\cloud-deployment'
New-Item -ItemType Directory -Force -Path $lessonFolder | Out-Null
Set-Location -LiteralPath $demoRoot
```

Do not put a password, access token, billing account identifier, secret value,
real name, or document text in this folder.

### Step 2 — Check the Google Cloud Command Line Interface

The Google Cloud Command Line Interface (CLI) is the `gcloud` program. Run:

```powershell
gcloud --version
gcloud auth list --filter=status:ACTIVE --format="value(account)"
```

Expected result: a version is shown and exactly one account you control is
active. Do not copy the account email into course evidence.

If no account is active, run:

```powershell
gcloud auth login
```

Complete the Google sign-in in the browser. This does not authorize a paid
upgrade. Never approve an **Activate**, **Upgrade**, **Paid account**, or
post-trial prompt.

### Step 3 — Create or select one dedicated project

Choose a globally unique project identifier beginning with
`controlled-intake-`. It must use lowercase letters, numbers, and hyphens.

```powershell
$projectId = Read-Host 'Enter your dedicated project ID, beginning controlled-intake-'
if ($projectId -notmatch '^controlled-intake-[a-z0-9-]{4,40}$') {
    throw 'The project ID does not match the capstone safety pattern.'
}
$existingProject = gcloud projects describe $projectId --format="value(projectId)" 2>$null
if ($LASTEXITCODE -ne 0) {
    gcloud projects create $projectId --name='Controlled Intake Training'
    if ($LASTEXITCODE -ne 0) { throw 'Project creation failed. Stop and inspect the message.' }
}
gcloud config set project $projectId
gcloud projects describe $projectId --format="table(projectId,lifecycleState)"
```

Expected result: only the dedicated project is selected and its lifecycle state
is `ACTIVE`.

### Step 4 — Check and link only the existing Free Trial

Open the project Billing page:

```powershell
Start-Process "https://console.cloud.google.com/billing/linkedaccount?project=$projectId"
```

Read the page yourself. The page must say **Free trial** and still show an
**Activate** button. Linking this project to the existing Free Trial may be
required. Do not create, activate, upgrade, or link a paid billing account.

Stop if the wording is ambiguous. Do not send Codex a screenshot containing a
billing account identifier.

### Step 5 — Configure the €60 controls in the console

Open:

```powershell
Start-Process 'https://console.cloud.google.com/billing/budgets'
```

Create one project-scoped budget:

1. scope it only to the dedicated project;
2. set the amount to €40;
3. add actual-spend alerts at 25%, 50%, 75%, 90%, and 100%;
4. do not call it a spending stop; and
5. keep email notifications on.

If **Spend cap budget** is offered in your console, create:

- €5 monthly for Vertex AI or its current Agent Platform service label; and
- €5 monthly for Cloud Run.

Spend caps are currently Preview. Document AI and Artifact Registry are not
listed as covered services. If the control is unavailable, record
`SPEND CAP PREVIEW NOT AVAILABLE`; do not pretend it exists. If your billing
currency is not euros, stop and ask for a reviewed conversion before
deployment.

Create this record without billing identifiers:

```powershell
notepad (Join-Path $lessonFolder 'worked_cost_gate.md')
```

The scripts use the international currency code `EUR`, meaning euro.

Use:

```markdown
# Worked deployment cost gate

Billing screen says Free trial: YES/NO
Activate button remains visible: YES/NO
Paid activation performed: NO
Project-only alert budget: EUR 40
Alert percentages: 25, 50, 75, 90, 100
Vertex AI spend cap: EUR 5 / PREVIEW NOT AVAILABLE
Cloud Run spend cap: EUR 5 / PREVIEW NOT AVAILABLE
Document AI covered by spend cap: NO
Maximum application runs: 20
Maximum application pages: 60
Maximum pages per PDF: 3
Live hard stop: 2026-10-20
Trial credit expiry: 2026-10-26
Data: frozen synthetic course PDFs only
```

Do not continue until the first two answers are `YES` and paid activation is
`NO`.

### Step 6 — Run the guarded preflight

Run:

```powershell
$trialConfirmation = 'FREE TRIAL CONFIRMED - DO NOT ACTIVATE'
& .\scripts\preflight.ps1 `
    -ProjectId $projectId `
    -FreeTrialConfirmation $trialConfirmation |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_preflight.txt')
```

Expected result: `PASS`, Free Trial confirmed by the learner, European Union
locations, Netherlands Cloud Run region, and no paid activation.

The script checks an existing project and billing link. It cannot link billing
and cannot upgrade the account.

### Step 7 — Deploy the private service

Run:

```powershell
$costConfirmation = 'EUR 60 CONTROLS CONFIRMED'
& .\scripts\deploy.ps1 `
    -ProjectId $projectId `
    -FreeTrialConfirmation $trialConfirmation `
    -CostControlsConfirmation $costConfirmation |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_deployment.txt')
```

The script:

- enables only the required application programming interfaces (APIs);
- creates a dedicated keyless runtime service account;
- gives it Document AI, Vertex AI, Firestore counter, and secret-access roles;
- creates Enterprise Document optical character recognition (OCR) in `eu`;
- stores only counters in Firestore in `europe-west4`;
- stores the signing secret in Secret Manager in `europe-west4`;
- deploys Cloud Run privately in `europe-west4`;
- sets zero minimum and one maximum instance;
- sets concurrency to one;
- limits each request to three pages and 5 megabytes;
- limits the lifetime prototype to 20 runs and 60 pages;
- configures `gemini-3.5-flash-lite` in `eu`; and
- tries to reduce the `_Default` log retention to one day.

Expected final line: `DEPLOYED PRIVATE`. A private service address is not proof
that validation passed.

The service health path is `/api/health`, not `/healthz`. Because Cloud Run is
private, use the authenticated proxy or an authorised identity rather than
making the service public just to read health metadata.

### Step 8 — Re-check Free Trial immediately

Open the Billing page again. Confirm it still says **Free trial** and still
shows **Activate**. Add the time of this check to `worked_cost_gate.md`.

Do not click the button.

## Now recreate it yourself

Independently inspect the deployed service instead of trusting the deployment
message.

Run:

```powershell
gcloud run services describe controlled-document-intake `
    --project $projectId `
    --region europe-west4 `
    --format=yaml |
    Tee-Object -FilePath (Join-Path $lessonFolder 'recreated_cloud_run_description.txt')

gcloud run services get-iam-policy controlled-document-intake `
    --project $projectId `
    --region europe-west4 `
    --format=json |
    Tee-Object -FilePath (Join-Path $lessonFolder 'recreated_cloud_run_iam_policy.json')

gcloud artifacts repositories list `
    --project $projectId `
    --location europe-west4 `
    --format="table(name,format,location)" |
    Tee-Object -FilePath (Join-Path $lessonFolder 'recreated_artifact_repositories.txt')

gcloud secrets describe controlled-intake-signing-secret `
    --project $projectId `
    --format="table(name,replication.userManaged.replicas.location)" |
    Tee-Object -FilePath (Join-Path $lessonFolder 'recreated_secret_metadata.txt')
```

These commands read metadata. They do not reveal the secret value. Never run
`gcloud secrets versions access` for course evidence.

Open `recreated_cloud_run_iam_policy.json`. It must not contain `allUsers` or
`allAuthenticatedUsers`. Lab 8 performs a second policy check and a real
unauthenticated-request rejection before it uses a learner token.

Create:

```powershell
notepad (Join-Path $lessonFolder 'recreated_deployment_review.md')
```

In your own words, record:

- why the service is private and which two public policy members are absent;
- Cloud Run region;
- Document AI location and processor type;
- Vertex AI location and model;
- minimum instances, maximum instances, and concurrency;
- request timeout, central processing unit, and memory;
- file/page/run limits;
- whether the `_Default` log retention reached one day;
- why maximum instances and budget alerts are not exact euro caps; and
- why teardown is required even with scale-to-zero.

Do not paste account emails, secret values, access tokens, billing identifiers,
or document text.

## Ask Codex to check your work

Run `(Resolve-Path $lessonFolder).Path`, paste the result, and send:

```text
READ-ONLY PRIVATE-DEPLOYMENT REVIEW.

Inspect only this full local evidence folder:
[PASTE FULL PATH]

Do not edit, delete, rename, upload, deploy, enable an API, access a secret,
change Identity and Access Management, change billing, or call the service.
Stop for access tokens, secret values, billing account identifiers, account
emails, or real data.

Return PASS or NOT YET for: preflight PASS; Free trial and Activate-button
checks recorded; paid activation NO; EUR 40 alerts; eligible EUR 5 caps either
recorded or honestly unavailable; deployment private; europe-west4 Cloud Run;
no allUsers or allAuthenticatedUsers policy member; eu Document AI and Vertex
AI; gemini-3.5-flash-lite; minimum zero, maximum one, concurrency one;
application caps; one-day default-log result recorded; scale to zero not
confused with teardown; no credential or real data in evidence. Cite filenames
and redact identifiers.
```

## Pass criteria

- The account remains an unactivated Free Trial.
- The project is dedicated to this synthetic proof.
- Cost warnings and available service caps are present and correctly
  described.
- Every offline test passed before deployment.
- Cloud Run is private in `europe-west4`, with no public policy member.
- Document AI and Vertex AI are configured for `eu`.
- Minimum instances are zero; maximum instances and concurrency are one.
- The application limits and 20 October hard stop remain unchanged.
- The signing secret is not stored in a file or shown in evidence.
- Codex returns PASS.

## Stop conditions

Stop before deployment if billing is not visibly Free Trial, the Activate
button is missing, any paid upgrade is requested, cost controls are absent,
offline tests fail, the date is 20 October 2026 or later, or same-session
teardown is impossible. Stop after deployment if `_Default` log retention could
not be checked; resolve it before live validation.

## Current official Google references

- [Google Cloud Free Trial and paid activation](https://docs.cloud.google.com/free/docs/free-cloud-features)
- [Cloud Billing budgets are alerts](https://docs.cloud.google.com/billing/docs/how-to/budgets)
- [Preview Spend cap budgets and limitations](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)
- [Cloud Run locations](https://docs.cloud.google.com/run/docs/locations)
- [Cloud Run scale-to-zero and autoscaling](https://docs.cloud.google.com/run/docs/about-instance-autoscaling)
- [Cloud Run maximum-instance behavior](https://docs.cloud.google.com/run/docs/configuring/max-instances-limits)
- [Document AI regions](https://docs.cloud.google.com/document-ai/docs/regions)
- [Vertex AI data residency](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/data-residency)
