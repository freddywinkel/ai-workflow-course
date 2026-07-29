[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CandidateArtifact,

    [Parameter(Mandatory = $true)]
    [string]$LastKnownGoodArtifact,

    [Parameter(Mandatory = $true)]
    [string]$LearnerStateBackup,

    [string]$ReportPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-ExistingDirectory {
    param([string]$Path, [string]$Label)
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    if (-not (Test-Path -LiteralPath $resolved -PathType Container)) {
        throw "$Label must be an existing directory: $resolved"
    }
    return [IO.Path]::GetFullPath($resolved)
}

function Resolve-ExistingFile {
    param([string]$Path, [string]$Label)
    $resolved = (Resolve-Path -LiteralPath $Path).Path
    if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) {
        throw "$Label must be an existing file: $resolved"
    }
    return [IO.Path]::GetFullPath($resolved)
}

function Get-ArtifactInventory {
    param([string]$Root)
    $rootPath = [IO.Path]::GetFullPath($Root).TrimEnd(
        [IO.Path]::DirectorySeparatorChar,
        [IO.Path]::AltDirectorySeparatorChar
    )
    $inventory = @()
    Get-ChildItem -LiteralPath $rootPath -Recurse -File -Force |
        Sort-Object FullName |
        ForEach-Object {
            $relative = $_.FullName.Substring($rootPath.Length).TrimStart(
                [IO.Path]::DirectorySeparatorChar,
                [IO.Path]::AltDirectorySeparatorChar
            ).Replace("\", "/")
            $inventory += [ordered]@{
                path = $relative
                sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
                bytes = $_.Length
            }
        }
    return @($inventory)
}

function Read-VersionIdentity {
    param([string]$ArtifactRoot)
    $versionPath = Join-Path $ArtifactRoot "version.json"
    if (-not (Test-Path -LiteralPath $versionPath -PathType Leaf)) {
        throw "Artifact is missing version.json: $ArtifactRoot"
    }
    $version = Get-Content -LiteralPath $versionPath -Raw | ConvertFrom-Json
    foreach ($field in @("courseId", "courseVersion", "buildId", "contentHash", "commit")) {
        if (-not $version.$field) {
            throw "Artifact version.json is missing $field`: $ArtifactRoot"
        }
    }
    if ($version.courseId -ne "course-1-controlled-ai-workflow-foundations") {
        throw "Artifact is not Course 1: $ArtifactRoot"
    }
    $manifestPath = Join-Path $ArtifactRoot "asset-manifest.json"
    $artifactFormat = "manifest-v1"
    if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
        $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
        if (
            $manifest.schemaVersion -ne 1 -or
            $manifest.buildId -ne $version.buildId -or
            $manifest.contentHash -ne $version.contentHash -or
            $manifest.provenance.commit -ne $version.commit
        ) {
            throw "Artifact manifest and version identity do not match: $ArtifactRoot"
        }
    }
    else {
        if (
            $version.courseVersion -ne "2.5.0" -or
            $version.buildId -ne "ad5f59e8f800" -or
            $version.contentHash -ne "ddc88ff3b2a9ac9080b05abebad5f578de122406a6bab00bb52b28a92353258a" -or
            $version.commit -ne "69d868a713d4"
        ) {
            throw "Only the exact accepted legacy v2.5 artifact may omit asset-manifest.json: $ArtifactRoot"
        }
        $artifactFormat = "legacy-v2.5"
    }
    return [ordered]@{
        courseId = $version.courseId
        courseVersion = $version.courseVersion
        buildId = $version.buildId
        contentHash = $version.contentHash
        commit = $version.commit
        artifactFormat = $artifactFormat
    }
}

function Read-LearnerStateCompatibility {
    param(
        [string]$BackupPath,
        [string]$TargetArtifact,
        [System.Collections.IDictionary]$TargetIdentity
    )
    $backup = Get-Content -LiteralPath $BackupPath -Raw | ConvertFrom-Json
    if ($backup.exportType -ne "ai-workflow-course-progress") {
        throw "Learner-state backup has the wrong exportType"
    }
    if ($backup.courseId -ne "course-1-controlled-ai-workflow-foundations") {
        throw "Learner-state backup is not for Course 1"
    }
    $backupKeys = @($backup.PSObject.Properties.Name | Sort-Object)
    $expectedBackupKeys = @(
        "bundleSchemaVersion",
        "courseId",
        "courseVersion",
        "exportType",
        "exportedAt",
        "state"
    ) | Sort-Object
    if (
        @(
            Compare-Object $backupKeys $expectedBackupKeys -SyncWindow 0
        ).Count -ne 0
    ) {
        throw "Learner-state backup has an unsupported top-level shape"
    }
    if ($backup.bundleSchemaVersion -ne 2) {
        throw "Learner-state backup has an unsupported bundle schema"
    }
    if (-not $backup.state -or -not $backup.state.schemaVersion) {
        throw "Learner-state backup is missing state.schemaVersion"
    }
    $schemaVersion = [int]$backup.state.schemaVersion
    $expectedStateKeys = if ($schemaVersion -eq 1) {
        @(
            "completed",
            "expandedGroups",
            "fontSize",
            "lastDocument",
            "lastUpdateCheck",
            "notes",
            "schemaVersion",
            "theme"
        )
    }
    else {
        $nonLegacyStateKeys = @(
            "archivedLegacyNotes",
            "completed",
            "completionRevisions",
            "expandedGroups",
            "fontSize",
            "lastDocument",
            "lastUpdateCheck",
            "migration",
            "notes",
            "practicalPassed",
            "practicalPassRevisions",
            "schemaVersion",
            "theme"
        )
        if ($schemaVersion -ge 3) {
            $nonLegacyStateKeys += "resetEpoch"
        }
        $nonLegacyStateKeys
    }
    $stateKeys = @($backup.state.PSObject.Properties.Name | Sort-Object)
    $expectedStateKeys = @($expectedStateKeys | Sort-Object)
    if (
        @(
            Compare-Object $stateKeys $expectedStateKeys -SyncWindow 0
        ).Count -ne 0
    ) {
        throw "Learner-state backup has an unsupported state shape"
    }
    $supportedSchemas = @(1, 2)
    if ($TargetIdentity.artifactFormat -eq "manifest-v1") {
        $stateScriptPath = Join-Path $TargetArtifact "state.js"
        if (-not (Test-Path -LiteralPath $stateScriptPath -PathType Leaf)) {
            throw "Manifest-format rollback target is missing state.js"
        }
        $stateScript = Get-Content -LiteralPath $stateScriptPath -Raw
        $schemaMatch = [regex]::Match(
            $stateScript,
            'STATE_SCHEMA_VERSION\s*=\s*(\d+)'
        )
        if (-not $schemaMatch.Success) {
            throw "Could not determine the rollback target state schema"
        }
        $targetSchema = [int]$schemaMatch.Groups[1].Value
        $supportedSchemas = @(1, 2, $targetSchema) | Select-Object -Unique
    }
    if ($schemaVersion -notin $supportedSchemas) {
        throw (
            "Learner-state schema $schemaVersion is not readable by rollback target " +
            "$($TargetIdentity.courseVersion) ($($TargetIdentity.artifactFormat)). " +
            "Do not deploy this rollback until a compatible, verified recovery path exists."
        )
    }
    return [ordered]@{
        schemaVersion = $schemaVersion
        targetArtifactFormat = $TargetIdentity.artifactFormat
        targetSupportedSchemas = @($supportedSchemas)
        compatible = $true
    }
}

function Copy-Artifact {
    param([string]$Source, [string]$Destination)
    if (Test-Path -LiteralPath $Destination) {
        throw "Rehearsal destination already exists: $Destination"
    }
    Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
}

function Remove-RehearsalPath {
    param([string]$Path, [string]$RehearsalRoot)
    $resolvedPath = [IO.Path]::GetFullPath($Path)
    $resolvedRoot = [IO.Path]::GetFullPath($RehearsalRoot).TrimEnd(
        [IO.Path]::DirectorySeparatorChar,
        [IO.Path]::AltDirectorySeparatorChar
    )
    $requiredPrefix = $resolvedRoot + [IO.Path]::DirectorySeparatorChar
    if (-not $resolvedPath.StartsWith(
        $requiredPrefix,
        [StringComparison]::OrdinalIgnoreCase
    )) {
        throw "Refusing to remove a path outside the rehearsal directory: $resolvedPath"
    }
    if (Test-Path -LiteralPath $resolvedPath) {
        Remove-Item -LiteralPath $resolvedPath -Recurse -Force
    }
}

$startedAt = [DateTimeOffset]::UtcNow
$rehearsalRoot = Join-Path (
    [IO.Path]::GetTempPath()
) ("course1-rollback-rehearsal-" + [Guid]::NewGuid().ToString("N"))
$result = $null
$exitCode = 1

try {
    $candidatePath = Resolve-ExistingDirectory $CandidateArtifact "Candidate artifact"
    $lastKnownGoodPath = Resolve-ExistingDirectory $LastKnownGoodArtifact "Last-known-good artifact"
    $statePath = Resolve-ExistingFile $LearnerStateBackup "Learner-state backup"
    if ($candidatePath -eq $lastKnownGoodPath) {
        throw "Candidate and last-known-good artifacts must be different directories"
    }

    $candidateIdentity = Read-VersionIdentity $candidatePath
    $lastKnownGoodIdentity = Read-VersionIdentity $lastKnownGoodPath
    if ($candidateIdentity.buildId -eq $lastKnownGoodIdentity.buildId) {
        throw "Candidate and last-known-good build IDs must differ"
    }

    $candidateInventory = @(Get-ArtifactInventory $candidatePath)
    $lastKnownGoodInventory = @(Get-ArtifactInventory $lastKnownGoodPath)
    $stateHashBefore = (
        Get-FileHash -LiteralPath $statePath -Algorithm SHA256
    ).Hash.ToLowerInvariant()
    $stateCompatibility = Read-LearnerStateCompatibility `
        $statePath `
        $lastKnownGoodPath `
        $lastKnownGoodIdentity

    New-Item -ItemType Directory -Path $rehearsalRoot | Out-Null
    $publicPath = Join-Path $rehearsalRoot "public"

    Copy-Artifact $lastKnownGoodPath $publicPath
    Remove-RehearsalPath $publicPath $rehearsalRoot
    Copy-Artifact $candidatePath $publicPath
    $promotedIdentity = Read-VersionIdentity $publicPath
    if ($promotedIdentity.buildId -ne $candidateIdentity.buildId) {
        throw "Candidate promotion identity did not match"
    }

    Remove-RehearsalPath $publicPath $rehearsalRoot
    Copy-Artifact $lastKnownGoodPath $publicPath
    $rolledBackIdentity = Read-VersionIdentity $publicPath
    $rolledBackInventory = @(Get-ArtifactInventory $publicPath)

    $expectedInventoryJson = $lastKnownGoodInventory | ConvertTo-Json -Depth 6 -Compress
    $actualInventoryJson = $rolledBackInventory | ConvertTo-Json -Depth 6 -Compress
    if ($actualInventoryJson -ne $expectedInventoryJson) {
        throw "Rolled-back artifact bytes do not match the last-known-good artifact"
    }
    if ($rolledBackIdentity.buildId -ne $lastKnownGoodIdentity.buildId) {
        throw "Rolled-back version identity does not match last known good"
    }

    $stateHashAfter = (
        Get-FileHash -LiteralPath $statePath -Algorithm SHA256
    ).Hash.ToLowerInvariant()
    if ($stateHashAfter -ne $stateHashBefore) {
        throw "The supplied learner-state backup changed during rehearsal"
    }

    $result = [ordered]@{
        schemaVersion = 1
        result = "PASS"
        startedAt = $startedAt.ToString("o")
        completedAt = [DateTimeOffset]::UtcNow.ToString("o")
        candidate = $candidateIdentity
        lastKnownGood = $lastKnownGoodIdentity
        candidateFileCount = $candidateInventory.Count
        restoredFileCount = $rolledBackInventory.Count
        restoredBytesMatch = $true
        learnerStateBackup = [ordered]@{
            path = $statePath
            sha256Before = $stateHashBefore
            sha256After = $stateHashAfter
            preserved = $true
            compatibility = $stateCompatibility
        }
        limits = @(
            "Local rehearsal only; no GitHub Pages deployment occurred",
            "Installed-browser and public URL checks still require live evidence"
        )
    }
    $exitCode = 0
}
catch {
    $result = [ordered]@{
        schemaVersion = 1
        result = "FAIL"
        startedAt = $startedAt.ToString("o")
        completedAt = [DateTimeOffset]::UtcNow.ToString("o")
        failure = $_.Exception.Message
    }
}
finally {
    if (Test-Path -LiteralPath $rehearsalRoot) {
        Remove-RehearsalPath $rehearsalRoot $(
            Split-Path -Parent $rehearsalRoot
        )
    }
}

$json = $result | ConvertTo-Json -Depth 8
if ($ReportPath) {
    $resolvedReport = [IO.Path]::GetFullPath($ReportPath)
    $reportParent = Split-Path -Parent $resolvedReport
    if ($reportParent -and -not (Test-Path -LiteralPath $reportParent)) {
        New-Item -ItemType Directory -Path $reportParent -Force | Out-Null
    }
    Set-Content -LiteralPath $resolvedReport -Value $json -Encoding UTF8
}
$json
exit $exitCode
