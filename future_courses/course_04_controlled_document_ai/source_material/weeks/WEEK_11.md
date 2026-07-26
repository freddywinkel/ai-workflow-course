# Week 11 — Integration, Provider Portability, and Timing Proof

## Outcome

You will connect one synthetic Microsoft or Google source/action surface with least privilege, compare one alternate model/document provider through the same contracts, repeat matched manual/assisted timing cases, and fix the weaknesses revealed.

## Beginner checkpoint

Revisit authentication/authorization in
[APIs and JSON](../foundations/04_WEB_APIS_AND_JSON.md). Learn these terms before
creating a connector: account, app registration, OAuth consent, scope, token,
delegated access, and draft-only permission. Use a dedicated synthetic account
or workspace.

Choose **one** connector path and **one** comparison provider. Record screenshots
or settings only after redacting IDs and never expose tokens. If draft-only
permission cannot be technically guaranteed, retain the local outbox stub.

Safe AI-assistance request:

```text
Explain the minimum OAuth scopes for this single synthetic draft-only connector
using current official documentation. Separate authentication from
authorization. Do not request send, delete, broad mailbox/drive, administrator,
or application-wide permissions.
```

## Concepts

- OAuth scopes and delegated versus application access;
- connector trigger, polling, webhook, and duplicate semantics;
- draft-only permission and synthetic workspace;
- provider adapter and capability mismatch;
- data location, retention, plan, and subprocessors;
- same-case controlled comparison;
- matched timing and quality;
- portability claim versus demonstrated portability;
- hardening backlog.

## Official readings

Choose only the sources for your selected path and verify current node/connector names.

Microsoft option:

1. [Microsoft identity platform OAuth 2.0](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow).
2. [Microsoft Graph permissions overview](https://learn.microsoft.com/en-us/graph/permissions-overview).
3. [Power Automate approvals](https://learn.microsoft.com/en-us/power-automate/get-started-approvals) for comparison.
4. [Azure Document Intelligence layout](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout) if that is your parser comparison.

Google option:

1. [Google OAuth 2.0 for web-server applications](https://developers.google.com/identity/protocols/oauth2/web-server).
2. [Google Drive API scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth).
3. [Gmail API scopes](https://developers.google.com/workspace/gmail/api/auth/scopes).

Provider comparison:

- [Mistral OCR](https://docs.mistral.ai/studio-api/document-processing/basic_ocr) and [regional inference](https://docs.mistral.ai/studio-api/regional-inference); or
- [Azure Document Intelligence privacy/security](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/document-intelligence/data-privacy-security); or
- [Ollama Structured Outputs](https://docs.ollama.com/capabilities/structured-outputs) and [API introduction](https://docs.ollama.com/api/introduction).

Read the provider’s current pricing, retention, region, license, and limits pages—not just its API tutorial.

## Guided build

### 1. Choose a narrow connector

Select one:

- intake from a synthetic-only OneDrive/SharePoint folder;
- intake from a synthetic-only Google Drive folder;
- create a draft in a synthetic Outlook mailbox;
- create a draft in a synthetic Gmail mailbox.

Prefer one intake connector plus the existing local draft adapter. If you choose mailbox drafting, grant draft creation/read scopes only where possible; do not grant/send or test send.

Document why the chosen scope is the least privilege available. If the platform bundles broader access, note the residual risk.

### 2. Preserve the intake contract

The connector translates to the same envelope:

- tenant;
- provider object ID/version;
- filename/media type/size;
- received time;
- bytes or authorised server-side fetch;
- provider event ID.

Then the canonical intake computes its own SHA-256. Provider IDs help replay detection but never replace the byte hash.

Test:

- same event twice;
- file renamed;
- file updated in place;
- unsupported file;
- permission revoked;
- expired token;
- connector outage;
- file deleted after trigger but before fetch;
- wrong folder/tenant.

### 3. Keep actions draft-only

If implementing a mailbox adapter:

- create draft, never send;
- show exact recipient/subject/body during approval;
- hash those exact canonical fields;
- store provider draft ID;
- use idempotency/reconciliation to avoid duplicate drafts;
- run only in the synthetic mailbox;
- delete test drafts during cleanup and audit deletion.

If the API cannot enforce draft-only scope, keep the send operation absent from code and use a dedicated synthetic account.

### 4. Implement one alternate provider adapter

Choose one:

- Docling versus Mistral OCR or Azure Document Intelligence on C003/C004/C005;
- OpenAI versus Ollama structured extraction on C001/C006/C007/C012.

Translate alternate output into the same `ParsedDocument` or extraction contract. Do not create a vendor-specific gold set.

Record:

- exact service/model/API version;
- plan and price;
- region endpoint/project region;
- retention and training controls;
- file limits;
- source-locator capabilities;
- latency/cost;
- schema and semantic accuracy;
- license/model license;
- failure behaviour.

Use synthetic data. “Local” Ollama means a loopback local model; a cloud-tagged model is not local.

### 5. Run the matched comparison

Keep source cases, contract, validator, and metrics fixed. Compare:

- required-field accuracy;
- evidence-locator correctness;
- table/scan result;
- refusal/failure;
- median latency;
- hands-on intervention;
- dated estimated cost;
- operational/privacy differences.

Do not compare uncalibrated provider “confidence” scores directly.

### 6. Repeat the timing study

Use the same four cases for manual and assisted processing: C001, C002, C004, and C018.

Measure separately:

- hands-on active time;
- elapsed/wait time;
- correction/review time;
- field accuracy;
- evidence correctness;
- unsupported/forbidden claims;
- reviewer decision outcome.

For each case:

```text
improvement_pct = (manual_hands_on - assisted_hands_on) / manual_hands_on × 100
```

Course gate:

- median hands-on improvement at least 30%;
- no decrease in measured quality;
- all safety invariants still pass.

If the gate fails, that is useful evidence. Identify whether review UI, OCR, failure handling, or over-complex orchestration consumes time; harden rather than hiding the result.

### 7. Convert findings into hardening fixes

Rank:

- critical safety/integrity defect;
- release blocker;
- quality/reliability defect;
- usability/time defect;
- optional enhancement.

Fix critical and release-blocking issues. Rerun affected cases plus all zero-tolerance tests. Defer optional complexity explicitly.

## Capstone increment

The capstone has one proven connector boundary, one measured provider substitution, and controlled evidence that the assisted workflow improves hands-on time without reducing quality—or an honest failed gate and remediation record.

## Required artifact

`artifacts/weekly/week-11/`:

- connector selection and scope record;
- redacted connector/n8n export;
- connector replay/error tests;
- optional draft adapter and cleanup evidence;
- alternate-provider adapter;
- vendor comparison including region/retention/license/pricing;
- matched manual/assisted timing dataset and calculations;
- hardening backlog, fixes, and rerun report;
- weekly evidence record.

## Test gate

Pass only if:

- connector uses only a synthetic workspace/account;
- scope is least privilege and no send/final action exists;
- duplicate/rename/update/token/outage paths are visible and safe;
- provider IDs do not replace source hashes;
- alternate provider uses the same domain contract and gold cases;
- provider region/retention/license/price claims have dated official sources;
- matched timing uses the same cases and includes quality;
- median hands-on improvement is ≥30% with no quality decline;
- all safety invariants pass after hardening.

If the timing threshold is not met, Week 11 remains failed until you simplify/fix and rerun. Do not alter the baseline or exclude slow valid cases without a predeclared rule.

## Common failures

- **Installing both ecosystems:** choose one Microsoft or Google connector.
- **Broad mailbox/Drive scope for convenience:** minimise and isolate a synthetic account.
- **Provider comparison with different prompts/schemas:** preserve the contract and controlled variables.
- **Claiming EU handling from a marketing page:** verify selected endpoint, plan, region, retention, and subprocessors.
- **Elapsed time reported as labor saving:** report hands-on and waiting separately.
- **Quality assumed from speed:** rerun field, locator, memo, and safety gates.
- **Hardening adds an agent framework:** fix measured bottlenecks with the smallest change.

## Estimated time

| Activity | Time |
|---|---:|
| Connector/provider readings and selection | 1.25 h |
| Connector implementation/tests | 2.0 h |
| Alternate-provider adapter/comparison | 2.0 h |
| Matched timing study | 1.5 h |
| Hardening and reruns | 1.5 h |
| Evidence packaging | 0.75 h |
| **Total** | **9.0 h** |
