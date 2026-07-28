# Capstone Lab 9 — Delete the Prototype and Prove What Is Gone

## Outcome

You will preview the exact deletion targets, delete the private application and
its supporting resources, request deletion of the dedicated project, and
record read-only verification.

Scale-to-zero means no Cloud Run instance normally remains active without
traffic. It does not delete container images, a Document AI processor,
Firestore counters, a secret, logs, or the project. Teardown is a separate
control.

Project deletion enters a limited recovery period. Provider-side backups,
administrative logs, delayed billing records, and deletion queues mean this
lesson must not claim instantaneous physical erasure or “zero retention.”

Approved synthetic exports use comma-separated values (CSV) and JavaScript
Object Notation (JSON). An application programming interface (API) is the
defined way one program asks a service to do something.

## Recorded reference result — actual teardown PASS

The reference project was torn down on 28 July 2026. The redacted evidence
records:

- project lifecycle state `DELETE_REQUESTED`;
- zero remaining Cloud Run services;
- zero remaining Cloud Storage buckets;
- Hypertext Transfer Protocol (HTTP) status 404 for the deleted service;
- the Cloud Run service, Document AI processor, Artifact Registry repository,
  staging buckets, runtime roles and identity, and Firestore counters removed
  before project deletion;
- the ordinary €40 alerts-only budget deleted and verified absent through the
  public Cloud Billing Budget API;
- both €5 Preview spend caps deleted and verified absent in the Billing user
  interface; and
- zero remaining course budget rows on the final Billing-page check.

A direct Secret Manager check was unavailable after project deletion disabled
billing. The evidence therefore treats project deletion as the final cleanup
boundary; it does not invent a separate post-deletion secret check.

The account remained an unactivated Free Trial and **Activate** remained
visible. The displayed post-validation cost was €0, but Billing data may lag;
this is not a claim that the final settled amount must be zero.

## Follow along — I show you exactly how

### Step 1 — Preserve only safe local evidence

Open Windows PowerShell:

```powershell
$capstoneRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\controlled-intake-capstone'
$demoRoot = Join-Path $capstoneRoot 'demo'
$lessonFolder = Join-Path $capstoneRoot 'evidence\teardown'
New-Item -ItemType Directory -Force -Path $lessonFolder | Out-Null
$projectId = Read-Host 'Enter the dedicated controlled-intake project ID'
if ($projectId -notmatch '^controlled-intake-[a-z0-9-]{4,40}$') {
    throw 'Project ID refused. Do not delete anything.'
}
Set-Location -LiteralPath $demoRoot
```

Keep only:

- metadata-only test and live-validation reports;
- approved synthetic CSV/JSON exports you intentionally want for a portfolio;
- file hashes; and
- the teardown record.

Do not preserve source uploads, temporary files, credentials, access tokens,
secret values, account emails, billing identifiers, or real data.

### Step 2 — Read the teardown script before using it

Run:

```powershell
notepad .\scripts\teardown.ps1
```

Confirm it refuses project identifiers outside the
`controlled-intake-...` pattern and requires both `-Execute` and the exact
project identifier before deleting anything.

Close the file without editing it.

### Step 3 — Run the safe dry run

Run:

```powershell
& .\scripts\teardown.ps1 `
    -ProjectId $projectId `
    -DeleteProject |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_teardown_dry_run.txt')
```

Expected first line: `DRY RUN. Nothing will be deleted.`

Confirm that the list includes:

- Cloud Run service;
- Document AI processor;
- Artifact Registry repositories;
- Cloud Storage source-deploy staging buckets;
- Secret Manager secret;
- runtime service account;
- Firestore counter database;
- the €40 alerts-only budget marked for public-API deletion;
- the two €5 Preview spend caps marked for Billing user-interface deletion and
  absence verification; and
- the dedicated project when project deletion is selected.

### Step 4 — Create the before-deletion decision record

Run:

```powershell
notepad (Join-Path $lessonFolder 'worked_teardown_decision.md')
```

Use:

```markdown
# Teardown decision

Project is dedicated to this capstone: YES/NO
Project identifier checked character by character: YES/NO
Required synthetic evidence saved locally: YES/NO
Real/client/work/medical/personal data ever used: NO
Paid billing activated: NO
Further live validation required: NO
Dry-run targets reviewed: YES/NO
Decision: DELETE / STOP
```

Continue only when every safety answer supports `DELETE`.

### Step 5 — Delete the two Preview spend caps in Billing

Open **Google Cloud Billing > Budgets & alerts**. Delete only these two exact
Preview rows:

- `Controlled Intake Vertex EUR 5 Cap`; and
- `Controlled Intake Cloud Run EUR 5 Cap`.

Refresh the page and verify both names are absent. Record only the two display
names and `ABSENT`; do not record the Billing account identifier.

This manual step is required because the public Cloud Billing Budget API used
by the teardown script deletes the ordinary alerts-only budget, not these
Preview spend caps. Do not claim API deletion for a cap that was removed in
the Billing user interface.

### Step 6 — Delete resources and request project deletion

This is intentionally destructive. Read the command before pressing Enter:

```powershell
& .\scripts\teardown.ps1 `
    -ProjectId $projectId `
    -Execute `
    -DeleteProject `
    -ExactProjectConfirmation $projectId |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_teardown_execution.txt')
```

The script first lists resources so an already-absent target is safe. It
deletes the named service resources, removes the runtime identity's three
project roles, deletes any source-deploy staging bucket, and deletes only the
ordinary project-scoped alert budget whose display name exactly matches
`Controlled Intake EUR 40 Alert`.

It resolves the Billing account internally and suppresses the identifier from
output. It verifies that ordinary alert budget is absent through the public
API before asking Google Cloud to delete the dedicated project. The two Preview
spend caps must already be absent from Step 5. If the script reports an error,
do not assume cleanup failed or succeeded. Continue with the read-only checks
below.

### Step 7 — Perform read-only verification

Run:

```powershell
$projectState = gcloud projects describe $projectId --format="value(lifecycleState)" 2>$null
if ($LASTEXITCODE -ne 0 -or -not $projectState) {
    $projectState = 'NOT RETURNED BY PROJECT DESCRIBE'
}
$projectState | Tee-Object -FilePath (Join-Path $lessonFolder 'worked_project_state.txt')
```

If the project still returns `ACTIVE`, stop and inspect the deletion error. A
deletion-requested state or an unavailable project is expected.

Then run these read-only listings. Empty results or project-unavailable errors
are expected after successful project deletion:

```powershell
gcloud run services list `
    --project $projectId `
    --region europe-west4 `
    --format="value(metadata.name)" 2>&1 |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_remaining_cloud_run.txt')

gcloud artifacts repositories list `
    --project $projectId `
    --location all `
    --format="value(name)" 2>&1 |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_remaining_artifacts.txt')

gcloud storage buckets list `
    --project $projectId `
    --format="value(name)" 2>&1 |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_remaining_storage.txt')

gcloud secrets list `
    --project $projectId `
    --format="value(name)" 2>&1 |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_remaining_secrets.txt')
```

Do not mistake an “API disabled” or “project unavailable” message for proof of
instant physical deletion. It proves only that the resource is no longer
available through that query.

### Step 8 — Check Billing reports later

Google Cloud cost reporting can lag behind use and teardown. Check the Billing
report after teardown and again the next day. Record amounts and times without
the billing account identifier:

```powershell
notepad (Join-Path $lessonFolder 'worked_delayed_billing_checks.md')
```

The account must remain Free Trial. On **Budgets & alerts**, confirm the
ordinary alert name from Step 6 and both Preview names from Step 5 are absent.
Record only `ABSENT` or `REMAINS` for each name; never copy the Billing account
identifier. Never click **Activate** to inspect an old report.

## Now recreate it yourself

Build your own teardown proof table from the saved files:

```powershell
notepad (Join-Path $lessonFolder 'recreated_teardown_inventory.md')
```

Use this structure and complete every row in your own words:

```markdown
| Target | Before | Deletion evidence | Read-only result | What this does not prove |
|---|---|---|---|---|
| Cloud Run service | | | | |
| Document AI processor | | | | |
| Artifact Registry images | | | | |
| Cloud Storage staging bucket | | | | |
| signing secret | | | | |
| runtime service account | | | | |
| Firestore counters | | | | |
| ordinary alerts-only budget — public API | | | | |
| two Preview spend caps — Billing user interface | | | | |
| dedicated project | | | | |
| delayed billing record | | | | |
```

Add:

- why API disablement alone would not delete stored data;
- why deleting Cloud Run alone would leave images;
- why lifecycle cleanup is delayed rather than immediate;
- why project deletion has a recovery period;
- which local synthetic evidence you kept; and
- the date on which the next Billing report check is due.

Do not restore the project merely to make the table easier to complete.

## Ask Codex to check your work

Run `(Resolve-Path $lessonFolder).Path`, paste the result, and send:

```text
READ-ONLY TEARDOWN-EVIDENCE REVIEW.

I authorize inspection of only this full local folder:
[PASTE FULL PATH]

You may also run only this read-only command if needed:
gcloud projects describe [PROJECT ID] --format=value(lifecycleState)

Do not edit, create, delete, restore, enable, disable, deploy, call an
application service, access a secret, or change billing. Stop for credentials,
secret values, account emails, billing identifiers, source text, model output,
or real data.

Return PASS or NOT YET for: dry run happened before execution; the two exact
Preview spend caps were deleted and verified in the Billing user interface;
the exact dedicated project confirmation was used; execution output exists;
the ordinary alerts-only budget was deleted and verified through the public
API; project is not reported ACTIVE; Cloud Run, Artifact Registry and Secret
Manager checks are empty or unavailable; Cloud Storage is empty or
unavailable; all three exact budget display names are recorded absent; the
recreated inventory covers every target; delayed billing is acknowledged; no
zero-retention claim is made; only approved synthetic local evidence remains;
paid activation stayed NO.
Distinguish resource unavailability from physical-erasure proof and cite
filenames.
```

## Pass criteria

- Dry run preceded destructive execution.
- The two Preview spend caps were removed and verified through the Billing user
  interface.
- The exact dedicated project was confirmed.
- Cloud Run, Document AI, Artifact Registry, the signing secret, runtime
  identity, Firestore counters, and Cloud Storage staging buckets were
  targeted.
- The ordinary alerts-only budget was deleted and verified through the public
  API; the course does not falsely claim that API removed the Preview caps.
- The dedicated project is deletion-requested or unavailable, not active.
- Local evidence contains no credential, real data, source text, or model
  output.
- Delayed Billing checks are scheduled and recorded.
- The account remains an unactivated Free Trial.
- The report makes no false zero-retention or instant-erasure claim.
- Codex returns PASS.

## Stop conditions

Stop before deletion if the project is not dedicated, its identifier is
uncertain, needed synthetic evidence has not been saved, or another project
appears in scope. After execution, stop and investigate if the project remains
`ACTIVE`. Never use a broad wildcard and never activate paid billing.

## Current official Google references

- [Delete and restore a Google Cloud project](https://docs.cloud.google.com/resource-manager/docs/delete-restore-projects)
- [Delete Cloud Run services](https://docs.cloud.google.com/run/docs/managing/services)
- [Delete Artifact Registry repositories](https://docs.cloud.google.com/artifact-registry/docs/repositories/delete-repos)
- [Delete Cloud Storage buckets recursively](https://docs.cloud.google.com/sdk/gcloud/reference/storage/rm)
- [Delete a Document AI processor](https://docs.cloud.google.com/document-ai/docs/reference/rest/v1/projects.locations.processors/delete)
- [Delete a Cloud Billing budget](https://docs.cloud.google.com/billing/docs/reference/budget/rest/v1/billingAccounts.budgets/delete)
- [Manage spend cap budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)
- [Why disabling an API is not data deletion](https://docs.cloud.google.com/service-usage/docs/enable-disable)
- [Cloud Logging retention periods](https://docs.cloud.google.com/logging/quotas)
