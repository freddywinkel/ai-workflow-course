param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,

    [Parameter(Mandatory = $true)]
    [string]$FreeTrialConfirmation,

    [Parameter(Mandatory = $true)]
    [string]$CostControlsConfirmation
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-OptionalProperty {
    param(
        [AllowNull()]
        [object]$InputObject,

        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    if ($null -eq $InputObject) {
        return $null
    }
    $property = $InputObject.PSObject.Properties[$Name]
    if ($null -eq $property) {
        return $null
    }
    return $property.Value
}

function Assert-GcloudSucceeded {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Context
    )

    if ($LASTEXITCODE -ne 0) {
        throw "$Context failed with Google Cloud CLI exit code $LASTEXITCODE."
    }
}

if ($CostControlsConfirmation -cne "EUR 60 CONTROLS CONFIRMED") {
    throw "First create the course budget/alerts and any available spend caps. Then pass the exact confirmation from the deployment lesson."
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$demoRoot = Split-Path -Parent $scriptRoot
& (Join-Path $scriptRoot "preflight.ps1") `
    -ProjectId $ProjectId `
    -FreeTrialConfirmation $FreeTrialConfirmation

$gcloud = Get-Command gcloud.cmd -ErrorAction SilentlyContinue
if ($null -eq $gcloud) {
    $gcloudFallback = Join-Path $env:LOCALAPPDATA (
        "Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
    )
    if (-not (Test-Path -LiteralPath $gcloudFallback -PathType Leaf)) {
        throw "Google Cloud Command Line Interface (CLI) was not found. Install it before this lab."
    }
    $gcloud = [pscustomobject]@{ Source = $gcloudFallback }
}
$serviceName = "controlled-document-intake"
$serviceAccountName = "controlled-intake-runtime"
$serviceAccount = "$serviceAccountName@$ProjectId.iam.gserviceaccount.com"
$secretName = "controlled-intake-signing-secret"

& $gcloud.Source services enable `
    run.googleapis.com `
    documentai.googleapis.com `
    aiplatform.googleapis.com `
    firestore.googleapis.com `
    cloudbuild.googleapis.com `
    artifactregistry.googleapis.com `
    secretmanager.googleapis.com `
    logging.googleapis.com `
    --project $ProjectId
Assert-GcloudSucceeded -Context "Enabling the bounded capstone services"

$serviceAccountDescription = & $gcloud.Source iam service-accounts list `
    --project $ProjectId `
    --filter="email=$serviceAccount" `
    --format="value(email)" `
    2>$null
$serviceAccountExists = (
    $LASTEXITCODE -eq 0 -and
    -not [string]::IsNullOrWhiteSpace(
        [string]$serviceAccountDescription
    )
)
if (-not $serviceAccountExists) {
    & $gcloud.Source iam service-accounts create $serviceAccountName `
        --display-name="Controlled intake runtime only" `
        --project $ProjectId
    Assert-GcloudSucceeded -Context "Creating the restricted runtime service account"
}

foreach ($role in @(
    "roles/documentai.apiUser",
    "roles/aiplatform.user",
    "roles/datastore.user"
)) {
    & $gcloud.Source projects add-iam-policy-binding $ProjectId `
        --member="serviceAccount:$serviceAccount" `
        --role=$role `
        --condition=None `
        --quiet | Out-Null
    Assert-GcloudSucceeded -Context "Granting runtime role $role"
}

$databases = & $gcloud.Source firestore databases list `
    --project $ProjectId --format=json | ConvertFrom-Json
Assert-GcloudSucceeded -Context "Listing Firestore databases"
$defaultDatabase = @($databases) |
    Where-Object {
        (Get-OptionalProperty -InputObject $_ -Name "name") -match
            '/databases/\(default\)$'
    } |
    Select-Object -First 1
if (-not $defaultDatabase) {
    & $gcloud.Source firestore databases create `
        --project $ProjectId `
        --database="(default)" `
        --location=europe-west4 `
        --type=firestore-native `
        --quiet
    Assert-GcloudSucceeded -Context "Creating the counters-only Firestore database"
}

$secretDescriptions = @(& $gcloud.Source secrets list `
    --project $ProjectId `
    --format="value(name)" `
    2>$null)
$secretExists = (
    $LASTEXITCODE -eq 0 -and
    $secretDescriptions -contains $secretName
)
if (-not $secretExists) {
    & $gcloud.Source secrets create $secretName `
        --replication-policy=user-managed `
        --locations=europe-west4 `
        --project $ProjectId
    Assert-GcloudSucceeded -Context "Creating the European Union signing secret"
}

$secretBytes = New-Object byte[] 48
$randomNumberGenerator = [Security.Cryptography.RandomNumberGenerator]::Create()
try {
    $randomNumberGenerator.GetBytes($secretBytes)
} finally {
    $randomNumberGenerator.Dispose()
}
$signingSecret = [Convert]::ToBase64String($secretBytes)
$signingSecret | & $gcloud.Source secrets versions add $secretName `
    --data-file=- `
    --project $ProjectId | Out-Null
Assert-GcloudSucceeded -Context "Adding the signing-secret version"
$signingSecret = $null
[Array]::Clear($secretBytes, 0, $secretBytes.Length)

& $gcloud.Source secrets add-iam-policy-binding $secretName `
    --member="serviceAccount:$serviceAccount" `
    --role="roles/secretmanager.secretAccessor" `
    --project $ProjectId `
    --quiet | Out-Null
Assert-GcloudSucceeded -Context "Granting runtime access to the signing secret"

$accessToken = (& $gcloud.Source auth print-access-token).Trim()
Assert-GcloudSucceeded -Context "Obtaining a short-lived deployment access token"
if ([string]::IsNullOrWhiteSpace($accessToken)) {
    throw "Google Cloud CLI returned no deployment access token."
}
$headers = @{ Authorization = "Bearer $accessToken" }
$processorBase = "https://eu-documentai.googleapis.com/v1/projects/$ProjectId/locations/eu/processors"
$processorList = Invoke-RestMethod -Method Get -Uri $processorBase -Headers $headers
$listedProcessors = @(
    Get-OptionalProperty -InputObject $processorList -Name "processors"
)
$processor = $listedProcessors |
    Where-Object {
        (Get-OptionalProperty -InputObject $_ -Name "displayName") -eq
            "controlled-intake-enterprise-ocr"
    } |
    Select-Object -First 1
if (-not $processor) {
    $body = @{
        type = "OCR_PROCESSOR"
        displayName = "controlled-intake-enterprise-ocr"
    } | ConvertTo-Json
    $createOperation = Invoke-RestMethod `
        -Method Post `
        -Uri $processorBase `
        -Headers $headers `
        -ContentType "application/json" `
        -Body $body
    $operationName = [string](
        Get-OptionalProperty -InputObject $createOperation -Name "name"
    )
    if ([string]::IsNullOrWhiteSpace($operationName)) {
        throw "Document AI did not return a processor-creation operation name."
    }

    $operation = $null
    $operationComplete = $false
    for ($attempt = 1; $attempt -le 150; $attempt++) {
        $operation = Invoke-RestMethod `
            -Method Get `
            -Uri "https://eu-documentai.googleapis.com/v1/$operationName" `
            -Headers $headers
        $operationError = Get-OptionalProperty `
            -InputObject $operation `
            -Name "error"
        if ($null -ne $operationError) {
            $operationErrorMessage = [string](
                Get-OptionalProperty `
                    -InputObject $operationError `
                    -Name "message"
            )
            throw "Document AI processor creation failed: $operationErrorMessage"
        }
        $operationComplete = [bool](
            Get-OptionalProperty -InputObject $operation -Name "done"
        )
        if ($operationComplete) {
            break
        }
        Start-Sleep -Seconds 2
    }
    if (-not $operationComplete) {
        throw "Document AI processor creation did not finish within five minutes."
    }
    $processor = Get-OptionalProperty `
        -InputObject $operation `
        -Name "response"
}
$processorName = [string](
    Get-OptionalProperty -InputObject $processor -Name "name"
)
if (
    [string]::IsNullOrWhiteSpace($processorName) -or
    $processorName -notmatch '/locations/eu/processors/[^/]+$'
) {
    throw "Document AI returned no usable EU processor name."
}
$processorId = ($processorName -split '/')[-1]
$accessToken = $null
$headers = $null

& $gcloud.Source run deploy $serviceName `
    --project $ProjectId `
    --region=europe-west4 `
    --source=$demoRoot `
    --service-account=$serviceAccount `
    --no-allow-unauthenticated `
    --ingress=all `
    --cpu=1 `
    --memory=512Mi `
    --min=0 `
    --min-instances=0 `
    --max=1 `
    --max-instances=1 `
    --concurrency=1 `
    --timeout=120 `
    --cpu-throttling `
    --no-session-affinity `
    --set-env-vars="PROVIDER_MODE=google,GOOGLE_CLOUD_PROJECT=$ProjectId,DOCUMENT_AI_LOCATION=eu,DOCUMENT_AI_PROCESSOR_ID=$processorId,VERTEX_LOCATION=eu,GEMINI_MODEL=gemini-3.5-flash-lite,GOOGLE_GENAI_USE_ENTERPRISE=true,FIRESTORE_DATABASE=(default),MAX_FILE_BYTES=5000000,MAX_PAGES_PER_DOCUMENT=3,MAX_LIVE_RUNS=20,MAX_TOTAL_PAGES=60,MAX_GEMINI_INPUT_CHARACTERS=24000,MAX_GEMINI_OUTPUT_TOKENS=800,REVIEW_TTL_MINUTES=30,LIVE_HARD_STOP=2026-10-20T00:00:00+00:00" `
    --set-secrets="APP_SIGNING_SECRET=$secretName`:latest" `
    --quiet
Assert-GcloudSucceeded -Context "Deploying the private Cloud Run service"

$activeAccount = (& $gcloud.Source config get-value account 2>$null).Trim()
Assert-GcloudSucceeded -Context "Reading the active learner account"
if (
    [string]::IsNullOrWhiteSpace($activeAccount) -or
    $activeAccount -notmatch '^[^@\s]+@[^@\s]+$'
) {
    throw "The active Google Cloud account was missing or was not a usable learner account."
}

& $gcloud.Source run services add-iam-policy-binding $serviceName `
    --project $ProjectId `
    --region=europe-west4 `
    --member="user:$activeAccount" `
    --role=roles/run.invoker `
    --quiet | Out-Null
Assert-GcloudSucceeded -Context "Granting the learner private Cloud Run access"

& $gcloud.Source logging buckets update _Default `
    --project $ProjectId `
    --location=global `
    --retention-days=1 `
    --quiet | Out-Null
Assert-GcloudSucceeded -Context "Reducing the default application-log retention to one day"

$serviceUrl = (& $gcloud.Source run services describe $serviceName `
    --project $ProjectId `
    --region=europe-west4 `
    --format="value(status.url)").Trim()
Assert-GcloudSucceeded -Context "Reading the private Cloud Run service URL"
if ([string]::IsNullOrWhiteSpace($serviceUrl)) {
    throw "Cloud Run returned no private service URL."
}

[pscustomobject]@{
    Result = "DEPLOYED PRIVATE"
    Service = $serviceName
    Region = "europe-west4"
    DocumentAiProcessor = "controlled-intake-enterprise-ocr"
    DocumentAiLocation = "eu"
    GeminiModel = "gemini-3.5-flash-lite"
    VertexLocation = "eu"
    MinimumInstances = 0
    MaximumInstances = 1
    Concurrency = 1
    Url = $serviceUrl
    Next = "Run verify_live.ps1, then teardown.ps1 in the same session."
} | Format-List
