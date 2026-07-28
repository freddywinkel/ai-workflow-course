param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,

    [switch]$Execute,

    [switch]$DeleteProject,

    [string]$ExactProjectConfirmation = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$serviceName = "controlled-document-intake"
$processorDisplayName = "controlled-intake-enterprise-ocr"
$serviceAccountName = "controlled-intake-runtime"
$serviceAccount = "$serviceAccountName@$ProjectId.iam.gserviceaccount.com"
$secretName = "controlled-intake-signing-secret"
$alertsOnlyBudgetDisplayNames = @(
    "Controlled Intake EUR 40 Alert"
)
$spendCapDisplayNames = @(
    "Controlled Intake Vertex EUR 5 Cap",
    "Controlled Intake Cloud Run EUR 5 Cap"
)
$budgetDisplayNames = @(
    $alertsOnlyBudgetDisplayNames + $spendCapDisplayNames
)

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

function Invoke-GcloudCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [Parameter(Mandatory = $true)]
        [string]$Context,

        [switch]$AllowFailure
    )

    # Windows PowerShell 5 does not turn a native non-zero exit code into a
    # catchable exception. Capture it explicitly, suppress potentially
    # sensitive native stderr, and return one predictable result object.
    $previousErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        $nativeOutput = @(& $script:GcloudPath @Arguments 2>$null)
        $exitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }

    if ($exitCode -ne 0 -and -not $AllowFailure) {
        throw "$Context failed with Google Cloud CLI exit code $exitCode. Native command details were suppressed to avoid recording account identifiers."
    }

    return [pscustomobject]@{
        ExitCode = $exitCode
        Output = @($nativeOutput | ForEach-Object { [string]$_ })
    }
}

function Convert-GcloudJson {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Result,

        [Parameter(Mandatory = $true)]
        [string]$Context
    )

    $json = ($Result.Output -join [Environment]::NewLine).Trim()
    if ([string]::IsNullOrWhiteSpace($json)) {
        return $null
    }
    try {
        return $json | ConvertFrom-Json
    } catch {
        throw "$Context returned unreadable JSON. Command output was suppressed."
    }
}

function Get-OutputLines {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Result
    )

    return @(
        $Result.Output |
            ForEach-Object { ([string]$_).Trim() } |
            Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    )
}

function Invoke-GoogleApiRequest {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("Get", "Delete")]
        [string]$Method,

        [Parameter(Mandatory = $true)]
        [string]$Uri,

        [Parameter(Mandatory = $true)]
        [hashtable]$Headers,

        [Parameter(Mandatory = $true)]
        [string]$Context
    )

    try {
        return Invoke-RestMethod `
            -Method $Method `
            -Uri $Uri `
            -Headers $Headers `
            -ErrorAction Stop
    } catch {
        throw "$Context failed. Provider response details were suppressed to avoid recording account or resource identifiers."
    }
}

function Get-AccessHeaders {
    $tokenResult = Invoke-GcloudCommand `
        -Arguments @("auth", "print-access-token") `
        -Context "Obtaining a short-lived teardown access token"
    $token = ($tokenResult.Output -join "").Trim()
    if ([string]::IsNullOrWhiteSpace($token)) {
        throw "Google Cloud CLI returned no teardown access token."
    }
    return @{
        Authorization = "Bearer $token"
        "X-Goog-User-Project" = $ProjectId
    }
}

function Get-Budgets {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BillingAccountResource,

        [Parameter(Mandatory = $true)]
        [hashtable]$Headers
    )

    $budgets = @()
    $pageToken = ""
    do {
        $uri = "https://billingbudgets.googleapis.com/v1/$BillingAccountResource/budgets?pageSize=1000"
        if (-not [string]::IsNullOrWhiteSpace($pageToken)) {
            $encodedPageToken = [Uri]::EscapeDataString($pageToken)
            $uri = "$uri&pageToken=$encodedPageToken"
        }
        $response = Invoke-GoogleApiRequest `
            -Method Get `
            -Uri $uri `
            -Headers $Headers `
            -Context "Listing the course billing budgets"
        $budgets += @(
            Get-OptionalProperty -InputObject $response -Name "budgets"
        )
        $pageToken = [string](
            Get-OptionalProperty -InputObject $response -Name "nextPageToken"
        )
    } while (-not [string]::IsNullOrWhiteSpace($pageToken))

    return @($budgets)
}

function Test-BudgetBelongsToProject {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Budget,

        [Parameter(Mandatory = $true)]
        [string]$ProjectNumber
    )

    $budgetFilter = Get-OptionalProperty `
        -InputObject $Budget `
        -Name "budgetFilter"
    $projects = @(
        Get-OptionalProperty -InputObject $budgetFilter -Name "projects"
    )
    return $projects -contains "projects/$ProjectNumber"
}

function Remove-ControlledIntakeBudgets {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BillingAccountResource,

        [Parameter(Mandatory = $true)]
        [string]$ProjectNumber,

        [Parameter(Mandatory = $true)]
        [hashtable]$Headers
    )

    if ($BillingAccountResource -notmatch '^billingAccounts/[A-Za-z0-9-]+$') {
        throw "The linked billing account resource was not in the expected format. No budget was deleted."
    }
    if ($ProjectNumber -notmatch '^[0-9]+$') {
        throw "The dedicated project number was unavailable. No budget was deleted."
    }

    $budgets = Get-Budgets `
        -BillingAccountResource $BillingAccountResource `
        -Headers $Headers
    foreach ($budget in $budgets) {
        $displayName = [string](
            Get-OptionalProperty -InputObject $budget -Name "displayName"
        )
        if (
            $alertsOnlyBudgetDisplayNames -notcontains $displayName -or
            -not (
                Test-BudgetBelongsToProject `
                    -Budget $budget `
                    -ProjectNumber $ProjectNumber
            )
        ) {
            continue
        }

        $budgetName = [string](
            Get-OptionalProperty -InputObject $budget -Name "name"
        )
        if (
            [string]::IsNullOrWhiteSpace($budgetName) -or
            -not $budgetName.StartsWith("$BillingAccountResource/budgets/")
        ) {
            throw "A course budget returned an unexpected resource name. No unsafe deletion was attempted."
        }

        Invoke-GoogleApiRequest `
            -Method Delete `
            -Uri "https://billingbudgets.googleapis.com/v1/$budgetName" `
            -Headers $Headers `
            -Context "Deleting exact-name course budget '$displayName'" |
            Out-Null
        Write-Output "Deleted exact-name project budget: $displayName"
    }

    $remainingBudgets = @()
    for ($attempt = 1; $attempt -le 5; $attempt++) {
        $remainingBudgets = @(
            Get-Budgets `
                -BillingAccountResource $BillingAccountResource `
                -Headers $Headers |
                Where-Object {
                    $displayName = [string](
                        Get-OptionalProperty `
                            -InputObject $_ `
                            -Name "displayName"
                    )
                    $alertsOnlyBudgetDisplayNames -contains $displayName -and
                        (
                            Test-BudgetBelongsToProject `
                                -Budget $_ `
                                -ProjectNumber $ProjectNumber
                        )
                }
        )
        if ($remainingBudgets.Count -eq 0) {
            break
        }
        Start-Sleep -Seconds 1
    }
    if (@($remainingBudgets).Count -ne 0) {
        throw "Teardown verification failed: the exact-name alerts-only project budget remains."
    }
    Write-Output "Verified absent through the public API: exact-name alerts-only project budget."
}

function Remove-DocumentAiProcessors {
    param(
        [Parameter(Mandatory = $true)]
        [hashtable]$Headers
    )

    $base = "https://eu-documentai.googleapis.com/v1/projects/$ProjectId/locations/eu/processors"
    $pageToken = ""
    $processorsToDelete = @()
    do {
        $uri = $base
        if (-not [string]::IsNullOrWhiteSpace($pageToken)) {
            $encodedPageToken = [Uri]::EscapeDataString($pageToken)
            $uri = "$base?pageToken=$encodedPageToken"
        }
        $list = Invoke-GoogleApiRequest `
            -Method Get `
            -Uri $uri `
            -Headers $Headers `
            -Context "Listing the dedicated Document AI processors"
        $listedProcessors = @(
            Get-OptionalProperty -InputObject $list -Name "processors"
        )
        foreach ($processor in $listedProcessors) {
            $displayName = [string](
                Get-OptionalProperty -InputObject $processor -Name "displayName"
            )
            if ($displayName -eq $processorDisplayName) {
                $processorsToDelete += $processor
            }
        }
        $pageToken = [string](
            Get-OptionalProperty -InputObject $list -Name "nextPageToken"
        )
    } while (-not [string]::IsNullOrWhiteSpace($pageToken))

    foreach ($processor in $processorsToDelete) {
        $processorName = [string](
            Get-OptionalProperty -InputObject $processor -Name "name"
        )
        $escapedProjectId = [regex]::Escape($ProjectId)
        $escapedProjectNumber = [regex]::Escape($projectNumber)
        $expectedPattern = (
            "^projects/(?:$escapedProjectId|$escapedProjectNumber)" +
            "/locations/eu/processors/[A-Za-z0-9_-]+$"
        )
        if (
            [string]::IsNullOrWhiteSpace($processorName) -or
            $processorName -notmatch $expectedPattern
        ) {
            throw "Document AI returned an unexpected processor resource name. No unsafe deletion was attempted."
        }
        Invoke-GoogleApiRequest `
            -Method Delete `
            -Uri "https://eu-documentai.googleapis.com/v1/$processorName" `
            -Headers $Headers `
            -Context "Deleting the exact-name Document AI processor" |
            Out-Null
        Write-Output "Document AI processor deletion accepted."
    }
}

if ($ProjectId -notmatch '^controlled-intake-[a-z0-9-]{4,40}$') {
    throw "Refusing teardown because this is not a dedicated controlled-intake project ID."
}

$targets = @(
    "Cloud Run service controlled-document-intake in europe-west4",
    "Document AI processor controlled-intake-enterprise-ocr in eu",
    "all Artifact Registry repositories in the dedicated project",
    "all Cloud Storage staging buckets in the dedicated project",
    "Secret Manager secret controlled-intake-signing-secret",
    "runtime service account controlled-intake-runtime and its three project roles",
    "Firestore default database containing counters only",
    "alerts-only budget through the public API: $($alertsOnlyBudgetDisplayNames -join '; ')",
    "preview spend caps to verify in Billing UI: $($spendCapDisplayNames -join '; ')"
)
if ($DeleteProject) {
    $targets += "Dedicated project $ProjectId (strongest cleanup; recoverable for a limited period)"
}

if (-not $Execute) {
    Write-Output "DRY RUN. Nothing will be deleted."
    $targets | ForEach-Object { Write-Output " - $_" }
    Write-Output "Re-run with -Execute and -ExactProjectConfirmation '$ProjectId'."
    exit 0
}
if ($ExactProjectConfirmation -cne $ProjectId) {
    throw "The exact project confirmation does not match. No resource was deleted."
}

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
$script:GcloudPath = $gcloud.Source

$projectResult = Invoke-GcloudCommand `
    -Arguments @(
        "projects", "describe", $ProjectId,
        "--format=json"
    ) `
    -Context "Reading the dedicated project" `
    -AllowFailure
if ($projectResult.ExitCode -ne 0) {
    if ($DeleteProject) {
        Write-Output "The dedicated project is already unavailable. No cloud mutation was attempted."
        Write-Output "Budget absence cannot be re-proved without a live project-to-billing link; inspect the three exact display names in Billing."
        exit 0
    }
    throw "The dedicated project is unavailable. Resource-only teardown cannot continue."
}

$project = Convert-GcloudJson `
    -Result $projectResult `
    -Context "Reading the dedicated project"
$projectNumber = [string](
    Get-OptionalProperty -InputObject $project -Name "projectNumber"
)
if ($projectNumber -notmatch '^[0-9]+$') {
    throw "The dedicated project number was missing or invalid. No further resource was deleted."
}
$lifecycleState = [string](
    Get-OptionalProperty -InputObject $project -Name "lifecycleState"
)
if ($lifecycleState -in @("DELETE_REQUESTED", "DELETE_IN_PROGRESS")) {
    Write-Output "The dedicated project is already deletion-requested. No resource mutation was repeated."
    Write-Output "Budget absence cannot be re-proved from this state; inspect the three exact display names in Billing."
    exit 0
}
if ($lifecycleState -ne "ACTIVE") {
    throw "The dedicated project is not active. Its exact state is intentionally not printed."
}

$billingResult = Invoke-GcloudCommand `
    -Arguments @(
        "billing", "projects", "describe", $ProjectId,
        "--format=value(billingAccountName)"
    ) `
    -Context "Resolving the dedicated project's billing link"
$billingAccountResource = (
    $billingResult.Output -join ""
).Trim()
$billingResult = $null
if (
    [string]::IsNullOrWhiteSpace($billingAccountResource) -or
    $billingAccountResource -notmatch '^billingAccounts/[A-Za-z0-9-]+$'
) {
    throw "No valid billing link was returned. No resource was deleted."
}

$runList = Invoke-GcloudCommand `
    -Arguments @(
        "run", "services", "list",
        "--project", $ProjectId,
        "--region=europe-west4",
        "--filter=metadata.name=$serviceName",
        "--format=value(metadata.name)"
    ) `
    -Context "Listing the capstone Cloud Run service"
if ((Get-OutputLines -Result $runList) -contains $serviceName) {
    Invoke-GcloudCommand `
        -Arguments @(
            "run", "services", "delete", $serviceName,
            "--project", $ProjectId,
            "--region=europe-west4",
            "--quiet"
        ) `
        -Context "Deleting the capstone Cloud Run service" |
        Out-Null
    Write-Output "Deleted Cloud Run service."
}

$documentHeaders = Get-AccessHeaders
try {
    Remove-DocumentAiProcessors -Headers $documentHeaders
} finally {
    $documentHeaders.Authorization = $null
    $documentHeaders = $null
}

$repositoryList = Invoke-GcloudCommand `
    -Arguments @(
        "artifacts", "repositories", "list",
        "--project", $ProjectId,
        "--location=all",
        "--format=json"
    ) `
    -Context "Listing Artifact Registry repositories"
$repositoryItems = @(
    Convert-GcloudJson `
        -Result $repositoryList `
        -Context "Listing Artifact Registry repositories"
) | Where-Object { $null -ne $_ }
foreach ($repository in $repositoryItems) {
    $repositoryResource = [string](
        Get-OptionalProperty -InputObject $repository -Name "name"
    )
    $escapedRepositoryProjectId = [regex]::Escape($ProjectId)
    $escapedRepositoryProjectNumber = [regex]::Escape($projectNumber)
    $match = [regex]::Match(
        $repositoryResource,
        (
            "^projects/(?:$escapedRepositoryProjectId|" +
            "$escapedRepositoryProjectNumber)/locations/([^/]+)" +
            "/repositories/([^/]+)$"
        )
    )
    if (-not $match.Success) {
        throw "Artifact Registry returned an unexpected repository resource name. No unsafe deletion was attempted."
    }
    $repositoryLocation = $match.Groups[1].Value
    $repositoryName = $match.Groups[2].Value
    Invoke-GcloudCommand `
        -Arguments @(
            "artifacts", "repositories", "delete", $repositoryName,
            "--project", $ProjectId,
            "--location=$repositoryLocation",
            "--quiet"
        ) `
        -Context "Deleting an Artifact Registry repository" |
        Out-Null
    Write-Output "Deleted a dedicated-project Artifact Registry repository."
}

$bucketList = Invoke-GcloudCommand `
    -Arguments @(
        "storage", "buckets", "list",
        "--project", $ProjectId,
        "--format=value(name)"
    ) `
    -Context "Listing dedicated-project Cloud Storage buckets"
foreach ($bucketResource in (Get-OutputLines -Result $bucketList)) {
    if ($bucketResource -match '^gs://([a-z0-9][a-z0-9._-]+)/?$') {
        $bucketTarget = "gs://$($matches[1])"
    } elseif ($bucketResource -match '^([a-z0-9][a-z0-9._-]+)$') {
        $bucketTarget = "gs://$($matches[1])"
    } else {
        throw "Cloud Storage returned an unexpected bucket resource name. No unsafe deletion was attempted."
    }
    Invoke-GcloudCommand `
        -Arguments @(
            "storage", "rm", $bucketTarget,
            "--recursive",
            "--all-versions",
            "--quiet"
        ) `
        -Context "Deleting a dedicated-project Cloud Storage staging bucket" |
        Out-Null
    Write-Output "Deleted a dedicated-project Cloud Storage staging bucket."
    $bucketTarget = $null
}

$secretList = Invoke-GcloudCommand `
    -Arguments @(
        "secrets", "list",
        "--project", $ProjectId,
        "--format=value(name)"
    ) `
    -Context "Listing the signing secret"
$expectedSecretNames = @(
    $secretName,
    "projects/$ProjectId/secrets/$secretName",
    "projects/$projectNumber/secrets/$secretName"
)
$matchingSecret = Get-OutputLines -Result $secretList |
    Where-Object { $expectedSecretNames -contains $_ } |
    Select-Object -First 1
if ($matchingSecret) {
    Invoke-GcloudCommand `
        -Arguments @(
            "secrets", "delete", $secretName,
            "--project", $ProjectId,
            "--quiet"
        ) `
        -Context "Deleting the signing secret" |
        Out-Null
    Write-Output "Deleted signing secret."
}
$matchingSecret = $null
$expectedSecretNames = $null

$projectPolicyResult = Invoke-GcloudCommand `
    -Arguments @(
        "projects", "get-iam-policy", $ProjectId,
        "--format=json"
    ) `
    -Context "Reading project role bindings"
$projectPolicy = Convert-GcloudJson `
    -Result $projectPolicyResult `
    -Context "Reading project role bindings"
$runtimeMember = "serviceAccount:$serviceAccount"
foreach ($role in @(
    "roles/documentai.apiUser",
    "roles/aiplatform.user",
    "roles/datastore.user"
)) {
    $bindingExists = @(
        Get-OptionalProperty -InputObject $projectPolicy -Name "bindings"
    ) |
        Where-Object {
            (
                Get-OptionalProperty -InputObject $_ -Name "role"
            ) -eq $role -and
            @(
                Get-OptionalProperty -InputObject $_ -Name "members"
            ) -contains $runtimeMember
        } |
        Select-Object -First 1
    if ($bindingExists) {
        Invoke-GcloudCommand `
            -Arguments @(
                "projects", "remove-iam-policy-binding", $ProjectId,
                "--member=$runtimeMember",
                "--role=$role",
                "--condition=None",
                "--quiet"
            ) `
            -Context "Removing runtime project role $role" |
            Out-Null
        Write-Output "Removed runtime project role: $role"
    }
}

$serviceAccountList = Invoke-GcloudCommand `
    -Arguments @(
        "iam", "service-accounts", "list",
        "--project", $ProjectId,
        "--filter=email=$serviceAccount",
        "--format=value(email)"
    ) `
    -Context "Listing the runtime service account"
if ((Get-OutputLines -Result $serviceAccountList) -contains $serviceAccount) {
    Invoke-GcloudCommand `
        -Arguments @(
            "iam", "service-accounts", "delete", $serviceAccount,
            "--project", $ProjectId,
            "--quiet"
        ) `
        -Context "Deleting the runtime service account" |
        Out-Null
    Write-Output "Deleted runtime service account."
}

$databaseList = Invoke-GcloudCommand `
    -Arguments @(
        "firestore", "databases", "list",
        "--project", $ProjectId,
        "--format=value(name)"
    ) `
    -Context "Listing Firestore databases"
$defaultDatabaseSuffix = "/databases/(default)"
if (
    Get-OutputLines -Result $databaseList |
        Where-Object { $_.EndsWith($defaultDatabaseSuffix) } |
        Select-Object -First 1
) {
    Invoke-GcloudCommand `
        -Arguments @(
            "firestore", "databases", "delete",
            "--project", $ProjectId,
            "--database=(default)",
            "--quiet"
        ) `
        -Context "Deleting the counters-only Firestore database" |
        Out-Null
    Write-Output "Firestore database deletion accepted."
}

$budgetHeaders = Get-AccessHeaders
try {
    Remove-ControlledIntakeBudgets `
        -BillingAccountResource $billingAccountResource `
        -ProjectNumber $projectNumber `
        -Headers $budgetHeaders
} finally {
    $budgetHeaders.Authorization = $null
    $budgetHeaders = $null
    $billingAccountResource = $null
}

$remainingRun = Invoke-GcloudCommand `
    -Arguments @(
        "run", "services", "list",
        "--project", $ProjectId,
        "--region=europe-west4",
        "--filter=metadata.name=$serviceName",
        "--format=value(metadata.name)"
    ) `
    -Context "Verifying Cloud Run service removal"
if ((Get-OutputLines -Result $remainingRun) -contains $serviceName) {
    throw "Teardown verification failed: the Cloud Run service remains."
}

$remainingRepositories = Invoke-GcloudCommand `
    -Arguments @(
        "artifacts", "repositories", "list",
        "--project", $ProjectId,
        "--location=all",
        "--format=value(name)"
    ) `
    -Context "Verifying Artifact Registry removal"
if (@(Get-OutputLines -Result $remainingRepositories).Count -ne 0) {
    throw "Teardown verification failed: an Artifact Registry repository remains."
}

$remainingBuckets = Invoke-GcloudCommand `
    -Arguments @(
        "storage", "buckets", "list",
        "--project", $ProjectId,
        "--format=value(name)"
    ) `
    -Context "Verifying Cloud Storage removal"
if (@(Get-OutputLines -Result $remainingBuckets).Count -ne 0) {
    throw "Teardown verification failed: a Cloud Storage bucket remains."
}

if ($DeleteProject) {
    Invoke-GcloudCommand `
        -Arguments @(
            "projects", "delete", $ProjectId,
            "--quiet"
        ) `
        -Context "Requesting dedicated project deletion" |
        Out-Null
    $stateResult = Invoke-GcloudCommand `
        -Arguments @(
            "projects", "describe", $ProjectId,
            "--format=value(lifecycleState)"
        ) `
        -Context "Verifying dedicated project deletion state" `
        -AllowFailure
    if ($stateResult.ExitCode -ne 0) {
        Write-Output "Teardown complete. The dedicated project is no longer available."
        exit 0
    }
    $state = ($stateResult.Output -join "").Trim()
    if ($state -notin @("DELETE_REQUESTED", "DELETE_IN_PROGRESS")) {
        throw "Project deletion was requested but the project is still active or returned an unexpected state."
    }
    Write-Output "Teardown complete. Dedicated project deletion is requested."
    exit 0
}

Write-Output "Resource teardown completed. Deleting the dedicated project remains the strongest final cleanup."
