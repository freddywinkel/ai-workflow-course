# Private Deployment and Teardown

Use the detailed beginner sequence in
[Capstone Lab 7](../../../../advanced_capstone/07_CLOUD_RUN_DEPLOYMENT.md),
[Lab 8](../../../../advanced_capstone/08_LIVE_VALIDATION.md), and
[Lab 9](../../../../advanced_capstone/09_TEARDOWN.md). This file is the
concise technical runbook.

## Do not deploy unless

- every offline test passes;
- the Billing page visibly says **Free trial** and still shows **Activate**;
- paid activation is `NO`;
- [cost controls](COST_CONTROLS.md) are configured;
- [retention limits](RETENTION_AND_DATA_BOUNDARY.md) are understood;
- the project identifier starts with `controlled-intake-`;
- only frozen synthetic files are in scope;
- the date is before 20 October 2026; and
- validation plus teardown can finish in the same work session.

## Intended resources

| Resource | Name or type | Location |
|---|---|---|
| project | dedicated `controlled-intake-...` project | project boundary |
| Cloud Run | `controlled-document-intake` | `europe-west4` |
| service account | `controlled-intake-runtime` | keyless identity |
| Document AI | Enterprise Document optical character recognition (OCR) processor | `eu` |
| Vertex AI | `gemini-3.5-flash-lite` | `eu` |
| Firestore | `(default)`, counters only | `europe-west4` |
| Secret Manager | `controlled-intake-signing-secret` | `europe-west4` |
| Artifact Registry | source-deploy image repository | `europe-west4` |
| Cloud Storage | source-deploy staging bucket, if created | provider-selected |
| Billing | one ordinary alert budget and two Preview spend caps | billing-account control plane |

Cloud Run requires authentication. The learner receives only the Invoker role
needed to use the service through an authenticated proxy. The deployment must
not use `--allow-unauthenticated`.

## Preflight and deploy

From a separate practice copy of this folder:

```powershell
$projectId = Read-Host 'Enter the dedicated controlled-intake project ID'
$trialConfirmation = 'FREE TRIAL CONFIRMED - DO NOT ACTIVATE'
$costConfirmation = 'EUR 60 CONTROLS CONFIRMED'

& .\scripts\preflight.ps1 `
    -ProjectId $projectId `
    -FreeTrialConfirmation $trialConfirmation

& .\scripts\deploy.ps1 `
    -ProjectId $projectId `
    -FreeTrialConfirmation $trialConfirmation `
    -CostControlsConfirmation $costConfirmation
```

`preflight.ps1` does not link billing and cannot upgrade the account.
`deploy.ps1` enables the required application programming interfaces, creates
the dedicated resources, and deploys source through Cloud Build.

The Cloud Run configuration is:

```text
authentication: required
region: europe-west4
central processing unit: 1
memory: 512 MiB
request billing: central processing unit throttled outside requests
minimum instances: 0
maximum instances: 1
concurrency: 1
timeout: 120 seconds
session affinity: off
```

Maximum instances is a strong throttle, not an exact cap; Cloud Run documents
brief exceedance cases.

## Runtime configuration

```text
PROVIDER_MODE=google
DOCUMENT_AI_LOCATION=eu
VERTEX_LOCATION=eu
GEMINI_MODEL=gemini-3.5-flash-lite
GOOGLE_GENAI_USE_ENTERPRISE=true
MAX_FILE_BYTES=5000000
MAX_PAGES_PER_DOCUMENT=3
MAX_LIVE_RUNS=20
MAX_TOTAL_PAGES=60
MAX_GEMINI_INPUT_CHARACTERS=24000
MAX_GEMINI_OUTPUT_TOKENS=800
REVIEW_TTL_MINUTES=30
LIVE_HARD_STOP=2026-10-20T00:00:00+00:00
```

The Document AI processor identifier is injected by the script. The signing
secret is generated randomly and mounted from Secret Manager. Do not create a
service-account key or a cloud `.env` file.

## Verify private state

```powershell
gcloud run services describe controlled-document-intake `
    --project $projectId `
    --region europe-west4 `
    --format=yaml

gcloud run services get-iam-policy controlled-document-intake `
    --project $projectId `
    --region europe-west4 `
    --format=json
```

Confirm `europe-west4`, minimum zero, maximum one, concurrency one, bounded
environment variables, the dedicated service account, and no unexpected
revision. In the policy output, confirm neither `allUsers` nor
`allAuthenticatedUsers` appears.

The deployment attempts to reduce `_Default` log retention to one day. Do not
run live documents until that result is checked.

The health endpoint is `/api/health`, not `/healthz`. It reports only bounded
metadata such as provider mode, model and locations. It is protected by the
same private Cloud Run authentication as the rest of the service.

## Live acceptance

Before minting a token, the script independently checks the policy again and
requires an unauthenticated `/api/health` request to return `401` or `403`.
It then uses the signed-in learner's short-lived Google Cloud command-line
identity token. The learner has Cloud Run invoker access to this service only
for the lab. No key file is created, and the service remains private:

```powershell
& .\scripts\verify_live.ps1 `
    -ProjectId $projectId `
    -FreeTrialConfirmation $trialConfirmation
```

It processes only C001, C004, C008 and C012 through providers. Corrupt C010 and
a changed C001 byte sequence must stop before provider calls. It also proves
that a changed review package invalidates approval and unresolved findings
cannot export. Fixed findings narrow the action type; Gemini selects bounded
candidate identifiers; the application renders the exact summary and action
wording and rejects an action linked to an unrelated field. The output
`evidence/live_validation.json` contains metadata and hashes, not document text
or model output.

If validation fails, do not repeatedly retry. Preserve the metadata-only
failure and tear down.

## Teardown

Preview:

```powershell
& .\scripts\teardown.ps1 `
    -ProjectId $projectId `
    -DeleteProject
```

Before confirmed teardown, open **Billing > Budgets & alerts**. Delete only
these two Preview spend caps and verify that both rows disappear:

- `Controlled Intake Vertex EUR 5 Cap`; and
- `Controlled Intake Cloud Run EUR 5 Cap`.

This user-interface step is required. The public Cloud Billing Budget
application programming interface (API) supports the ordinary alerts-only
budget used here, but it is not the deletion/verification path for these
Preview spend caps.

Confirmed deletion of resources and the dedicated project:

```powershell
& .\scripts\teardown.ps1 `
    -ProjectId $projectId `
    -Execute `
    -DeleteProject `
    -ExactProjectConfirmation $projectId
```

The script targets:

- Cloud Run service and revisions;
- Document AI processor;
- Artifact Registry repositories across every location in the dedicated
  project;
- Cloud Storage source-deploy staging buckets in the dedicated project;
- signing secret;
- the runtime service account and its three project role bindings;
- Firestore counter database; and
- only the ordinary budget scoped to this project with the exact display name
  `Controlled Intake EUR 40 Alert`, deleted through the public API; and
- dedicated project.

Deleting a Cloud Run service does not delete its container image. Disabling an
application programming interface does not delete stored data. That is why the
teardown targets resources first and the dedicated project last.

The script resolves the linked Billing account internally but never prints its
identifier. Before deleting the ordinary alert budget, it requires both an
exact display-name match and a matching dedicated-project number. It lists
before deleting, so a second run does not try to delete resources that are
already absent. Ordinary-budget absence is verified before project deletion is
requested. The two Preview spend caps must already have been removed and
verified in the Billing user interface. If the project is already
deletion-requested or unavailable, the script does not guess a Billing
account; verify all three display names manually in the Billing page.

## Verify after teardown

```powershell
gcloud projects describe $projectId --format="value(lifecycleState)"
gcloud run services list --project $projectId --region europe-west4
gcloud artifacts repositories list --project $projectId --location all
gcloud storage buckets list --project $projectId
gcloud secrets list --project $projectId
```

Expected result: project deletion is requested or the project/resources are no
longer available. This is evidence of resource unavailability, not instant
physical erasure. Project deletion has a recovery period and Billing reports
can lag.

Check Billing after teardown and again the next day. The account must remain an
unactivated Free Trial. On the Budgets page, confirm the three exact display
names above are absent. Do not copy a Billing account identifier into evidence.

## Recorded reference execution — 28 July 2026

The bundled evidence records an actual `PASS`:

- Cloud Run was private, ready, and in `europe-west4`, with minimum zero,
  maximum one, concurrency one and 100% traffic to the tested revision;
- `/api/health` reported provider mode `google`;
- Document AI and Vertex AI were both in `eu`;
- C001 and C004 were `pending_approval`;
- C008 was `needs_review` with `TOTAL_DISCREPANCY`;
- C012 was `needs_review` with `UNTRUSTED_INSTRUCTION_DETECTED`;
- temporary deletion was true and raw persistence false;
- C001 approval produced comma-separated values (CSV) and JavaScript Object
  Notation (JSON) hashes;
- the account remained an unactivated Free Trial, while the displayed €0 cost
  remained subject to Billing-report delay;
- the alerts-only budget was deleted through the public API;
- the two Preview spend caps were deleted and verified absent in the Billing
  user interface; and
- project lifecycle state after teardown was `DELETE_REQUESTED`.

The service and project resources are no longer available. These results are
preserved in the three metadata-only JSON files in `../evidence`.

## Current official Google references

- [Deploy Cloud Run from source](https://docs.cloud.google.com/run/docs/deploying-source-code)
- [Cloud Run authentication](https://docs.cloud.google.com/run/docs/authenticating/overview)
- [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity)
- [Authenticated Cloud Run proxy](https://docs.cloud.google.com/sdk/gcloud/reference/run/services/proxy)
- [Document AI access roles](https://docs.cloud.google.com/document-ai/docs/access-control/iam-roles)
- [Document AI processor creation](https://docs.cloud.google.com/document-ai/docs/create-processor)
- [Artifact Registry cleanup](https://docs.cloud.google.com/artifact-registry/docs/repositories/cleanup-policy-overview)
- [Delete Artifact Registry repositories](https://docs.cloud.google.com/artifact-registry/docs/repositories/delete-repos)
- [Delete Cloud Storage buckets recursively](https://docs.cloud.google.com/sdk/gcloud/reference/storage/rm)
- [Delete a Cloud Billing budget](https://docs.cloud.google.com/billing/docs/reference/budget/rest/v1/billingAccounts.budgets/delete)
- [Manage spend cap budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)
- [Delete and restore projects](https://docs.cloud.google.com/resource-manager/docs/delete-restore-projects)
