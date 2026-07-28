param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,

    [Parameter(Mandatory = $true)]
    [string]$FreeTrialConfirmation,

    [string]$PythonExecutable = ""
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

if ($FreeTrialConfirmation -cne "FREE TRIAL CONFIRMED - DO NOT ACTIVATE") {
    throw "Re-check the Billing page. It must still say Free trial and show an Activate button."
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
if ([string]::IsNullOrWhiteSpace($PythonExecutable)) {
    $pythonSource = (Get-Command python.exe -ErrorAction Stop).Source
} else {
    $pythonSource = (Resolve-Path -LiteralPath $PythonExecutable).Path
}
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$serviceUrl = (& $gcloud.Source run services describe `
    controlled-document-intake `
    --project=$ProjectId `
    --region=europe-west4 `
    --format="value(status.url)" 2>$null).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($serviceUrl)) {
    throw "Could not read the private Cloud Run service URL."
}

$iamPolicyText = & $gcloud.Source run services get-iam-policy `
    controlled-document-intake `
    --project=$ProjectId `
    --region=europe-west4 `
    --format=json 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect the Cloud Run Identity and Access Management policy."
}
$iamPolicy = ($iamPolicyText -join [Environment]::NewLine) |
    ConvertFrom-Json
$publicMembers = @()
foreach ($binding in @(Get-OptionalProperty $iamPolicy "bindings")) {
    foreach ($member in @(
        Get-OptionalProperty $binding "members"
    )) {
        if ($member -in @("allUsers", "allAuthenticatedUsers")) {
            $publicMembers += $member
        }
    }
}
if ($publicMembers.Count -gt 0) {
    throw "Cloud Run has a public Identity and Access Management member. Run teardown."
}

$unauthenticatedStatus = $null
try {
    $unauthenticatedResponse = Invoke-WebRequest `
        -Uri "$serviceUrl/api/health" `
        -UseBasicParsing `
        -TimeoutSec 30 `
        -MaximumRedirection 0 `
        -ErrorAction Stop
    $unauthenticatedStatus = [int]$unauthenticatedResponse.StatusCode
} catch {
    if ($null -eq $_.Exception.Response) {
        throw "The unauthenticated Cloud Run check did not return an HTTP status."
    }
    $unauthenticatedStatus = [int]$_.Exception.Response.StatusCode
}
if ($unauthenticatedStatus -notin @(401, 403)) {
    throw "Unauthenticated Cloud Run access was not rejected with 401 or 403."
}

$identityToken = (& $gcloud.Source auth print-identity-token 2>$null).Trim()
$tokenExitCode = $LASTEXITCODE
if ($tokenExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($identityToken)) {
    throw "Could not mint the short-lived learner verification token."
}

try {
    $env:ALLOW_LIVE_GOOGLE_TESTS = "YES"
    $env:FREE_TRIAL_CONFIRMED = "YES"
    $env:PAID_BILLING_ACTIVATED = "NO"
    $env:CLOUD_RUN_PRIVATE_IAM_CONFIRMED = "YES"
    $env:CLOUD_RUN_UNAUTHENTICATED_STATUS = "$unauthenticatedStatus"
    $env:CONTROLLED_INTAKE_BASE_URL = $serviceUrl
    $env:CONTROLLED_INTAKE_AUTH_TOKEN = $identityToken
    & $pythonSource (Join-Path $scriptRoot "verify_live.py")
    if ($LASTEXITCODE -ne 0) {
        throw "Live validation failed. Do not claim completion; run teardown."
    }
} finally {
    $identityToken = $null
    Remove-Item Env:ALLOW_LIVE_GOOGLE_TESTS -ErrorAction SilentlyContinue
    Remove-Item Env:FREE_TRIAL_CONFIRMED -ErrorAction SilentlyContinue
    Remove-Item Env:PAID_BILLING_ACTIVATED -ErrorAction SilentlyContinue
    Remove-Item Env:CLOUD_RUN_PRIVATE_IAM_CONFIRMED -ErrorAction SilentlyContinue
    Remove-Item Env:CLOUD_RUN_UNAUTHENTICATED_STATUS -ErrorAction SilentlyContinue
    Remove-Item Env:CONTROLLED_INTAKE_BASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:CONTROLLED_INTAKE_AUTH_TOKEN -ErrorAction SilentlyContinue
}
