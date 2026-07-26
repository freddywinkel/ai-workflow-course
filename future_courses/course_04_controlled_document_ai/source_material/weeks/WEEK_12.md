# Week 12 — Acceptance, Private Release, and Handover

## Outcome

You will freeze a private release, reproduce it from a clean start, execute the complete acceptance suite, perform deletion and fallback drills, and deliver an evidence-backed demonstration and handover package that states limitations honestly.

## Beginner checkpoint

Revisit [Git and safe changes](../foundations/05_GIT_AND_SAFE_CHANGES.md),
[PowerShell recovery rules](../foundations/02_COMMAND_LINE_SURVIVAL.md), and the
component map in
[n8n, Docker, and databases](../foundations/08_N8N_DOCKER_AND_DATABASES.md).
Explain commit ID, version pin, clean start, runbook, backup, restore, and known
limitation.

A clean-start reproduction must follow written instructions in a separate
environment or fresh user session. Do not “fix it from memory” during the test;
record each missing instruction as a failure, update the runbook, and restart
the affected test.

Safe AI-assistance request:

```text
Act as a release verifier, not an implementer. Compare each acceptance claim
with its saved evidence and exact test result. Mark unsupported claims, stale
screenshots, untested recovery steps, and environment-specific assumptions. Do
not change code or call the release complete.
```

## Concepts

- release candidate and immutable evidence;
- configuration, dependency, model, prompt, schema, and corpus freeze;
- clean-start reproduction;
- acceptance versus demonstration;
- runbook and fallback SOP;
- threat-model residual risk;
- retention/deletion verification;
- restoration and disaster recovery;
- known limitation and operational readiness;
- evidence-backed claim.

## Official readings

1. [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices) — re-check current deployment, key, rate-limit, and monitoring guidance.
2. [n8n Docker installation](https://docs.n8n.io/deploy/host-n8n/install-options/install-with-docker) and [n8n security audit](https://docs.n8n.io/hosting/securing/security-audit/) — verify current paths/options with the evergreen audit.
3. [Supabase database backups caveat](https://supabase.com/docs/guides/database/overview) and [Storage access control](https://supabase.com/docs/guides/storage/security/access-control).
4. [NCSC-NL basic resilience principles](https://www.ncsc.nl/nieuws/ncsc-en-dtc-lanceren-gezamenlijke-basisprincipes-voor-digitale-weerbaarheid).
5. [`../CAPSTONE_SPECIFICATION.md`](../CAPSTONE_SPECIFICATION.md) and [`../ASSESSMENT_AND_RUBRIC.md`](../ASSESSMENT_AND_RUBRIC.md).

Re-run [`../EVERGREEN_UPDATE_PROMPT.md`](../EVERGREEN_UPDATE_PROMPT.md) if more than 8–12 weeks have passed since the Week 7 audit or any dependency/legal alert occurred.

## Guided build

### 1. Freeze release candidate

Create tag/version `v1.0.0-demo-rc1` only after:

- clean Git status;
- exact Python lock and Python version;
- exact n8n image tag/digest and redacted workflow exports;
- SQL migrations;
- exact parser/OCR/model-cache manifest;
- configured model IDs/snapshots and reasoning settings;
- prompt/schema/canonicalisation hashes;
- active policy/source hashes;
- corpus manifest and gold hashes;
- source-register verification date;
- no secrets;
- kill switch on by default;
- action mode draft/stub only.

Do not claim that a remote model’s server implementation is frozen unless the vendor provides and you used an explicit snapshot. Record the actual identifier returned.

### 2. Run the full automated acceptance suite

From a clean test database/bucket:

- all 20 cases;
- state closure;
- schema validity;
- ≥90% field accuracy;
- ≥95% locator correctness;
- memo support/forbidden propositions;
- exact-output approval;
- C018 two-person approval;
- duplicate/idempotency;
- parser/model/storage/audit outage injection;
- prompt injection;
- tenant isolation;
- retention/deletion with fake clock;
- matched timing result;
- offline deterministic suite.

Store command, logs/report hashes, start/end time, environment, and exit code.

### 3. Perform clean-start reproduction

Use a fresh Windows user session, VM, or clean folder/container namespace. Give the reproducer only:

- repository;
- course/capstone runbook;
- required secret names through a secure channel;
- synthetic corpus.

They must:

1. install/start prerequisites;
2. create the environment;
3. apply migrations;
4. import n8n workflow;
5. configure credentials;
6. run smoke tests;
7. process C001;
8. inspect evidence;
9. approve the exact proposal;
10. create one local/synthetic draft;
11. confirm audit trail.

Record every undocumented step. Fix the instructions and repeat the affected segment. “Works on the original machine” is not a pass.

### 4. Execute reviewer-path demonstration

Use a scripted sequence:

1. purpose and exclusions;
2. C001 normal path;
3. open original and verify source hash;
4. show extraction and calculation;
5. open two evidence locators;
6. show neutral memo;
7. edit one character and prove approval invalidation;
8. approve new exact hash and create one draft;
9. C008 arithmetic mismatch/manual review;
10. C012 injection detection;
11. C010 corrupt-file fallback;
12. C009 duplicate/idempotency;
13. activate kill switch and export manual work packet;
14. show evaluation report and limitations.

Avoid a rehearsed UI-only path that bypasses tests.

### 5. Run deletion drill

With an injectable clock/test namespace:

- after day 30: delete source objects, derived text/tables, rendered memos, embeddings/index entries, caches, stored provider objects under your control, and content-bearing logs;
- retain only policy-permitted content-free audit metadata through day 90;
- after day 90: delete remaining case audit metadata as specified by the synthetic policy;
- verify through negative reads, database queries, object listing, index query, cache lookup, and backup/deletion policy;
- record tombstone/deletion events without retaining deleted content.

If an external provider’s retention cannot be actively deleted or is outside your control, state that in vendor records and the limitations section. Do not overclaim.

### 6. Finalise operational documentation

Runbook:

- normal operation;
- states/reasons;
- daily/weekly checks;
- credential rotation;
- dependency/model update;
- retry/reconciliation;
- kill switch;
- backup/restore;
- retention/deletion;
- incident evidence;
- contact/owner placeholders.

Fallback SOP:

- stop model/action calls;
- preserve and verify sources;
- export manual case packet;
- manual extraction/check/memo template;
- independent review;
- record manual outcome;
- reconcile system state before resuming;
- never backfill an approval automatically.

Known limitations:

- synthetic data only;
- private demonstration, not public production;
- no real DPA/vendor legal assessment;
- no medical/special-category/consequential use;
- OCR/layout limits;
- model variability;
- policy corpus is fictional;
- connector limited to one synthetic environment;
- no send/payment/final action;
- security testing is bounded, not certification.

### 7. Issue the release

Create:

```text
artifacts/release/
  ACCEPTANCE_REPORT.md
  evaluation-report.json
  RELEASE_MANIFEST.json
  SOURCE_AND_VERSION_SNAPSHOT.md
  THREAT_MODEL.md
  RUNBOOK.md
  FALLBACK_SOP.md
  DATA_RETENTION_AND_DELETION.md
  LIMITATIONS.md
  DEMO_SCRIPT.md
  clean-start/
  test-results/
```

Hash every release artifact and include it in `RELEASE_MANIFEST.json`. Tag the commit only when every release blocker passes.

## Capstone increment

The capstone is complete when another user/session can reproduce one run using only supplied instructions and the frozen release passes all required acceptance gates. It remains a private synthetic demonstration.

## Required artifact

`artifacts/weekly/week-12/` and `artifacts/release/`:

- frozen release/version manifest;
- complete automated acceptance reports;
- clean-start report and corrected instructions;
- threat model and residual risks;
- runbook and fallback SOP;
- retention/deletion drill;
- restoration evidence from Week 9, updated if needed;
- limitations;
- demonstration script and recording/screenshots;
- final weekly evidence record;
- signed/dated self-assessment rubric.

## Test gate

Completion requires all of the following:

- 100% of runs end in a valid named state with schema-valid stored output or explicit failure;
- ≥90% required-field accuracy;
- ≥95% evidence-locator correctness;
- every factual memo assertion has verified support or is visibly unsupported/needs review;
- zero final/external actions without approval for the exact output hash;
- duplicate uploads cause no duplicate action;
- every declared outage, parser failure, timeout, corrupt input, and adversarial test reaches a visible safe fallback;
- retention/deletion covers originals, derivatives, indexes, caches, logs, provider objects under your control, and audit references;
- median hands-on time improves ≥30% without reduced measured quality;
- a clean environment or fresh user session completes C001 from the supplied instructions;
- secrets scan is clean;
- kill switch and manual fallback work;
- all known limitations and legal-status caveats are stated;
- release artifact hashes match the manifest.

One failed zero-tolerance invariant blocks release even when average accuracy passes.

## Common failures

- **Freezing code but not prompts/models/parser:** freeze and record the full version tuple.
- **Clean-start performed in the same configured shell:** use a fresh session/namespace and new credentials.
- **Deletion tested only in database:** include objects, embeddings, caches, logs, backups/policies, and provider state under your control.
- **Demo replaces acceptance:** show generated reports and failures, not just the happy path.
- **Manual fallback has no audit reconciliation:** record manual work and define safe resume.
- **Limitations written as future features:** state present boundary and residual risk plainly.
- **Tagging despite failed invariant:** fix or leave the release candidate unissued.

## Estimated time

| Activity | Time |
|---|---:|
| Freeze and source/version audit | 1.0 h |
| Full automated acceptance | 1.5 h |
| Clean-start reproduction | 2.0 h |
| Demo and failure paths | 1.25 h |
| Deletion drill | 1.25 h |
| Runbook/fallback/release package | 1.75 h |
| Final rubric and review | 0.75 h |
| **Total** | **9.5 h** |
