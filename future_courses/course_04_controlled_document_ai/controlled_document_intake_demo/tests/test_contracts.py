from __future__ import annotations

from pathlib import Path


def test_cloud_adapters_use_eu_endpoints_and_bounded_model_configuration():
    root = Path(__file__).resolve().parents[1]
    provider_source = (
        root / "src" / "controlled_intake" / "providers.py"
    ).read_text(encoding="utf-8")
    settings_source = (
        root / "src" / "controlled_intake" / "settings.py"
    ).read_text(encoding="utf-8")

    assert 'f"{self._settings.document_ai_location}-documentai.googleapis.com"' in provider_source
    assert "enterprise=True" in provider_source
    assert "vertexai=True" not in provider_source
    assert "location=self._settings.vertex_location" in provider_source
    assert "response_schema=response_schema" in provider_source
    assert "GEMINI_SELECTION_RESPONSE_SCHEMA" in provider_source
    assert '"gemini-3.5-flash-lite"' in settings_source
    assert '"GEMINI_MODEL"' in settings_source
    assert "os.getenv(" in settings_source
    assert "PROTOTYPE_GEMINI_MODEL" in settings_source
    assert "PROTOTYPE_LIVE_HARD_STOP" in settings_source
    assert "MAX_GEMINI_INPUT_CHARACTERS_CEILING" in settings_source
    assert "MAX_GEMINI_OUTPUT_TOKENS_CEILING" in settings_source
    assert "replace-with-at-least-32-random-characters" in settings_source
    assert 'self.document_ai_location != "eu"' in settings_source
    assert 'self.vertex_location != "eu"' in settings_source


def test_ui_states_boundaries_and_exports_are_visible():
    root = Path(__file__).resolve().parents[1]
    html = (root / "static" / "index.html").read_text(encoding="utf-8")
    script = (root / "static" / "app.js").read_text(encoding="utf-8")

    for text in [
        "Synthetic fixtures only",
        "Inspect every claim before deciding",
        "Record your decision on this exact output",
        "Download JSON",
        "Download CSV",
        "no autonomous",
    ]:
        assert text in html
    assert "X-Synthetic-Acknowledged" in script
    assert 'URL.revokeObjectURL(url)' in script
    assert "innerHTML" not in script


def test_processor_scripts_handle_empty_lists_and_wait_for_creation():
    root = Path(__file__).resolve().parents[1]
    deploy = (root / "scripts" / "deploy.ps1").read_text(encoding="utf-8")
    teardown = (root / "scripts" / "teardown.ps1").read_text(
        encoding="utf-8"
    )

    assert "$processorList.processors" not in deploy
    assert "$list.processors" not in teardown
    assert "Get-OptionalProperty" in deploy
    assert "Get-OptionalProperty" in teardown
    assert "$createOperation" in deploy
    assert "$operationComplete" in deploy
    assert "did not finish within five minutes" in deploy
    assert "$escapedProjectNumber" in teardown
    assert "/locations/eu/processors/[A-Za-z0-9_-]+$" in teardown


def test_runtime_dependencies_match_the_raw_body_contract():
    root = Path(__file__).resolve().parents[1]
    runtime = (root / "requirements.txt").read_text(encoding="utf-8")
    development = (root / "requirements-dev.txt").read_text(encoding="utf-8")

    assert "python-multipart" not in runtime
    assert "httpx2==2.9.1" in development


def test_powershell_deployment_fails_closed_on_native_command_errors():
    root = Path(__file__).resolve().parents[1]
    preflight = (root / "scripts" / "preflight.ps1").read_text(
        encoding="utf-8"
    )
    deploy = (root / "scripts" / "deploy.ps1").read_text(encoding="utf-8")

    assert "Assert-GcloudSucceeded" in deploy
    for context in [
        "Enabling the bounded capstone services",
        "Creating the restricted runtime service account",
        "Creating the European Union signing secret",
        "Deploying the private Cloud Run service",
        "Reducing the default application-log retention to one day",
    ]:
        assert context in deploy
    assert "$serviceAccountExists = (" in deploy
    assert "$secretExists = (" in deploy
    assert "iam service-accounts list" in deploy
    assert "secrets list" in deploy
    assert "iam service-accounts describe" not in deploy
    assert "secrets describe" not in deploy
    assert "RandomNumberGenerator]::Create()" in deploy
    assert "RandomNumberGenerator]::Fill" not in deploy
    assert "GOOGLE_CLOUD_PROJECT=$ProjectId" in deploy
    assert 'roles/run.invoker' in deploy
    assert "--min=0" in deploy
    assert "--min-instances=0" in deploy
    assert "--max=1" in deploy
    assert "--max-instances=1" in deploy
    assert preflight.count("$LASTEXITCODE -ne 0") >= 4
    for script_name in [
        "preflight.ps1",
        "deploy.ps1",
        "verify_live.ps1",
        "teardown.ps1",
    ]:
        script = (root / "scripts" / script_name).read_text(encoding="utf-8")
        assert "Get-Command gcloud.cmd" in script
        assert "Get-Command gcloud " not in script


def test_teardown_is_idempotent_scoped_and_powershell_5_safe():
    root = Path(__file__).resolve().parents[1]
    teardown = (root / "scripts" / "teardown.ps1").read_text(
        encoding="utf-8"
    )

    assert "Invoke-GcloudCommand" in teardown
    assert "$LASTEXITCODE" in teardown
    assert teardown.count("& $script:GcloudPath") == 1
    assert "Native command details were suppressed" in teardown
    assert '"X-Goog-User-Project" = $ProjectId' in teardown
    assert "Get-Command gcloud.cmd" in teardown
    assert "& $gcloud.Source" not in teardown

    for budget_name in [
        "Controlled Intake EUR 40 Alert",
        "Controlled Intake Vertex EUR 5 Cap",
        "Controlled Intake Cloud Run EUR 5 Cap",
    ]:
        assert budget_name in teardown
    assert "Get-Budgets" in teardown
    assert "Test-BudgetBelongsToProject" in teardown
    assert 'projects/$ProjectNumber' in teardown
    assert "nextPageToken" in teardown
    assert "billingAccountResource = $null" in teardown
    assert "exact-name alerts-only project budget remains" in teardown
    assert "$alertsOnlyBudgetDisplayNames" in teardown
    assert "$spendCapDisplayNames" in teardown
    assert "preview spend caps to verify in Billing UI" in teardown
    assert "@(Get-OutputLines -Result $remainingRepositories).Count" in teardown
    assert "@(Get-OutputLines -Result $remainingBuckets).Count" in teardown

    assert '"--location=all"' in teardown
    assert '"artifacts", "repositories", "list"' in teardown
    assert '"--format=json"' in teardown
    assert "$escapedRepositoryProjectNumber" in teardown
    assert '"storage", "rm", $bucketTarget' in teardown
    assert '$bucketTarget = "gs://$($matches[1])"' in teardown
    assert '"--recursive"' in teardown
    assert '"--all-versions"' in teardown
    assert "$expectedSecretNames" in teardown
    assert "projects/$projectNumber/secrets/$secretName" in teardown
    assert "--filter=name=$secretName" not in teardown
    for role in [
        "roles/documentai.apiUser",
        "roles/aiplatform.user",
        "roles/datastore.user",
    ]:
        assert role in teardown
    assert "remove-iam-policy-binding" in teardown
    assert "DELETE_REQUESTED" in teardown
    assert "DELETE_IN_PROGRESS" in teardown
    assert "projects describe $ProjectId" not in teardown


def test_live_verification_uses_the_private_learner_identity():
    root = Path(__file__).resolve().parents[1]
    powershell = (root / "scripts" / "verify_live.ps1").read_text(
        encoding="utf-8"
    )
    python = (root / "scripts" / "verify_live.py").read_text(encoding="utf-8")

    assert "auth print-identity-token" in powershell
    assert "run services get-iam-policy" in powershell
    assert '"allUsers", "allAuthenticatedUsers"' in powershell
    assert "Invoke-WebRequest" in powershell
    assert "$unauthenticatedStatus -notin @(401, 403)" in powershell
    assert "CLOUD_RUN_PRIVATE_IAM_CONFIRMED" in powershell
    assert "CLOUD_RUN_UNAUTHENTICATED_STATUS" in powershell
    assert "--impersonate-service-account" not in powershell
    assert "CONTROLLED_INTAKE_AUTH_TOKEN" in powershell
    assert "run services proxy" not in powershell
    assert 'merged_headers["Authorization"]' in python
    assert '"private_access"' in python
    assert "PACKAGE_CHANGED_AFTER_REVIEW" in python
    assert "PACKAGE_NOT_APPROVABLE" in python
    assert '"needs_correction_export"' in python
