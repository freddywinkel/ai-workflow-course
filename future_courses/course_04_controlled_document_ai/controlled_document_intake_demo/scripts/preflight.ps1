param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectId,

    [Parameter(Mandatory = $true)]
    [string]$FreeTrialConfirmation
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$requiredConfirmation = "FREE TRIAL CONFIRMED - DO NOT ACTIVATE"
$hardStop = [DateTimeOffset]::Parse("2026-10-20T00:00:00+00:00")

if ([DateTimeOffset]::UtcNow -ge $hardStop) {
    throw "The live capstone hard stop has passed. Do not create or call cloud resources."
}
if ($FreeTrialConfirmation -cne $requiredConfirmation) {
    throw "Open Google Cloud Billing first. Continue only while it visibly says Free trial and still shows an Activate button. Then pass the exact confirmation from the guide."
}
if ($ProjectId -notmatch '^controlled-intake-[a-z0-9-]{4,40}$') {
    throw "Use a dedicated project ID beginning with controlled-intake-. Do not reuse another app's project."
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
$account = (& $gcloud.Source config get-value account 2>$null).Trim()
if ($LASTEXITCODE -ne 0) {
    throw "Google Cloud CLI could not read the active account."
}
if (-not $account -or $account -eq "(unset)") {
    throw "No Google Cloud Command Line Interface (CLI) account is active. Run gcloud auth login first."
}

$project = & $gcloud.Source projects describe $ProjectId --format=json |
    ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or $null -eq $project) {
    throw "The dedicated project could not be described."
}
if ($project.lifecycleState -ne "ACTIVE") {
    throw "The dedicated project is not ACTIVE."
}

$billing = & $gcloud.Source billing projects describe $ProjectId --format=json |
    ConvertFrom-Json
if ($LASTEXITCODE -ne 0 -or $null -eq $billing) {
    throw "The dedicated project's billing link could not be inspected."
}
if ($billing.billingEnabled -ne $true) {
    throw "This project is not linked to the already-confirmed Free Trial account. This script deliberately cannot link billing. Stop and inspect the Billing page; never activate a paid account."
}

& $gcloud.Source config set project $ProjectId | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Google Cloud CLI could not select the dedicated project."
}

[pscustomobject]@{
    Result = "PASS"
    Project = $ProjectId
    AccountPresent = $true
    ExistingBillingLink = $true
    BillingTypeConfirmedByUser = "Free trial"
    PaidActivationPerformed = $false
    DocumentAiLocation = "eu"
    VertexLocation = "eu"
    CloudRunRegion = "europe-west4"
    HardStopUtc = $hardStop.ToString("o")
} | Format-List
