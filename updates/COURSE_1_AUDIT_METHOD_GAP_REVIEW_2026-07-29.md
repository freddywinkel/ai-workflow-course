# Course 1 Audit-Method Gap Review

> **Current follow-up — later on 2026-07-29:** this dated review correctly
> recorded the parser bypasses present when it ran. The subsequent
> audit-control repair closed `C1-GOV-012` with closed schemas, broad
> Markdown-container detection, hash-bound raw evidence, verified rollback
> ancestry, and adversarial tests. The body below remains unchanged as
> historical finding evidence. Follow
> `COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md` for current status.
> `C1-GOV-011` is now `EVIDENCE PENDING`: its all-33-test gate is implemented,
> but its immutable candidate-bound evidence is still missing.
> `C1-GOV-013` and `C1-GOV-015` are now `CLOSED`; `C1-GOV-007` is
> `EVIDENCE PENDING`. The current product status is `UNVERIFIED`, not `PASS`.

- Date: `2026-07-29`
- Timezone: `Europe/Amsterdam`
- Scope: Course 1 audit method and its local governance controls
- Mode: read-only audit-of-the-audit followed by the user-authorized addition
  of permanent audit rules
- Strategic decision: `STRATEGIC FIT: PASS`
- Deployment, commit, push, cloud, billing, and real-data actions: none

## Why this review was needed

Earlier Course 1 reviews found additional requirement families after repairs
had already started. That pattern showed that passing the current checks was
not the same as proving that the checks covered the whole product. This review
therefore started from the product promises, risks, contracts, environments,
evidence classes, and release path, then examined whether the audit itself had
complete controls.

## Permanent audit-method gaps identified

The earlier process did not consistently require:

1. a frozen untouched baseline before repair;
2. a machine-enumerated inventory of every normative ID and product surface;
3. a bidirectional requirement-test-evidence graph;
4. deliberate defects that prove audit gates fail for the intended reason;
5. exact separation of automated, learner, assessor, practitioner, legal,
   security, accessibility/device, repository, installed-client, and live
   evidence;
6. combined PWA concurrency, storage, render, recovery, hostile-backup, and
   service-worker tamper scenarios;
7. exact authoritative status parsing that cannot select historical prose or
   the wrong table column;
8. clean learner and maintainer environments without inherited packages,
   profiles, sessions, or caches;
9. immutable candidate identity and evidence bound to that exact candidate;
10. an invalidation map and complete rerun after the final material change;
11. independent reproduction and retained disagreement;
12. Course 1 and Course 4 scope, status, and evidence separation; and
13. an explicit audit-of-the-audit decision before repair;
14. consistency between normative authorities and every rendered/status
    consumer; and
15. operational separation of read-only diagnosis, disposable mutation tests,
    repository evidence writes, repairs, candidate commits, and release
    authority; and
16. one unambiguous meaning and independent evidence path for every revision,
    verification, execution, candidate, and release date or status.

These are now normative rules `C1-AA-001` through `C1-AA-016` in
`COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md`.

## Confirmed current defect: incomplete technical coverage map

Machine enumeration of
`COURSE_1_TECHNICAL_ACCEPTANCE_CONTRACT.md` found:

- `118` unique `C1-TA-*` requirement IDs;
- `33` unique referenced `C1-TST-*` test IDs;
- only `22` declared test-manifest rows; and
- `11` referenced test IDs with no declaration:
  `C1-TST-CAP-002`, `C1-TST-CAP-003`, `C1-TST-CAP-005`, and
  `C1-TST-FS-004` through `C1-TST-FS-011`.

The filesystem requirement rows cite individual `C1-TST-FS-*` IDs, while the
test manifest groups the same requirements under `C1-TST-FS-001` through
`C1-TST-FS-003`. Those two mappings cannot both be the complete authoritative
mapping as written. There is also no current 118-row evidence matrix proving
the state and locator for every technical requirement.

This is a reproduced governance defect, not merely unavailable external
evidence. It is recorded as open High finding `C1-GOV-011`, so the current
Course 1 status is `REPAIR REQUIRED`.

## Partially repaired parser controls

The promotion verifier previously:

1. accepted a substring rather than requiring exactly one authoritative
   current-status marker, allowing historical or quoted text to mislead the
   check; and
2. discovered only High and Medium rows, so an unknown severity such as
   `Critical` could be omitted from evaluation.

The verifier now rejects the tested unknown-severity/status, duplicate,
historical-only or quoted-only status, shifted-column, and extra-cell cases.
The audit-of-the-audit then reproduced additional fail-open paths:

- malformed, unbackticked, wrong-prefix, and undeclared-family finding IDs can
  be invisible to the row inventory;
- rollback validation still searches status text as a substring rather than
  using the exact authoritative marker;
- acceptance JSON permits unknown keys and duplicate last-value-wins keys; and
- arbitrary non-empty evidence locators are not proved to exist, match a hash,
  or belong to the candidate.

`C1-GOV-012` is therefore `PARTIAL`, not closed. The passing targeted tests are
retained without presenting them as proof of complete parser safety.

## Confirmed current defect: contradictory rollback semantics

`C1-TA-PWA-013` says every failed import must leave the exact prior durable
state, while the concurrency requirement says one context must not overwrite
another context's write. Those statements conflict when another page writes
after the failed transaction starts.

The ground-up protocol now defines per-key compare-and-preserve behavior:
restore a snapshot only when the current value is still transaction-owned or
already equals the snapshot; preserve a value changed externally; and report
primary state, reset barrier, recovery, runtime state, visible render, and
rollback verification separately. It also names the real duplicated-tab
writer-identity case and requires proof that test-harness close, reload,
timer, timeout, and storage-stub actions do not create the mutation under
test.

This requirements conflict is recorded as open Medium finding `C1-GOV-013`.
It remains open until the technical contract and deterministic tests use the
same non-contradictory semantics.

## Authority and mode inconsistencies corrected

The review also found stale or conflicting current-status, maintenance,
publication, and artifact-flow language. The release page now defers to the
ledger's `REPAIR REQUIRED` decision; older acceptance records are visibly
historical; Evergreen explicitly separates read-only delta diagnosis from an
approved delta repair; a learning-validation candidate is local/unpromoted
evidence collection; and promotion may revalidate a byte/fingerprint-identical
build while deployment uses that tested artifact without another rebuild.
This propagation is recorded under `C1-GOV-014`.

## Confirmed current defect: one date carries two meanings

The package schema currently uses `course.verifiedThrough` both as a statement
about research and source review and as the latest permitted revision date for
every bundled page. Four governance and release pages, plus this regenerated
validation report, were honestly revised on `2026-07-29`, while the last full
semantic source review remains `2026-07-28`. Advancing `verifiedThrough` merely
to make those editorial changes pass would create a false research-currentness
claim.

The fresh source check returned `PASS` for all `25` automated URL checks and
marked the OECD locator for manual review. The official OECD page was opened
and matched the registered report title and publication date. That proves the
locator is currently available; it is not a substitute for rechecking every
course claim against every source. The course therefore keeps
`verifiedThrough: 2026-07-28`, and the package validator correctly exposes the
metadata conflict instead of receiving a false date.

This is recorded as open Medium finding `C1-GOV-015`. Closure requires separate
content-revision and source-verification fields, independently labelled
rendered values, migration handling, and negative controls proving that
changing one cannot silently advance the other.

## Rules and request contract added

- `COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md` is the authoritative audit method.
- `COURSE_1_AUDIT_REQUEST_TEMPLATE.md` gives the learner a reusable two-stage
  request: read-only diagnosis first, approved repair second.
- `AGENTS.md` now makes the protocol mandatory for any full, final, last,
  100-percent, ground-up, or full-product-pass request.
- `COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md` remains authoritative for the
  resulting product status and finding states.

The two audit documents are deliberately unbundled governance files. However,
correcting stale bundled release and maintenance guidance does change the
learner-facing Progressive Web App source, so the existing build identity is
invalidated and must be rebuilt and retested. That rebuild is local evidence,
not a release or deployment.

## Local validation of the rule integration

After the final bundled guidance change:

- all `21/21` audit-protocol and promotion-verifier unit tests passed;
- Course 1 package validation executed all `37` checks with zero warnings but
  correctly returned `FAIL`: the `curriculum-documents` check reports that five
  governance/release pages revised on `2026-07-29` are later than the
  research/source `verifiedThrough` date of `2026-07-28`;
- all `44/44` PWA state, security, build, and contract tests passed;
- the six-viewport browser smoke passed, including duplicated-tab writer
  identity, concurrent state, dialogs, storage/recovery, accessibility modes,
  navigation, offline use, and Course 1 isolation;
- the controlled update smoke passed, including Later, Update now, state and
  unrelated-cache preservation, asset/manifest tamper, verified repair, and
  offline fallback; and
- an isolated rendered-browser review showed Course version `2.6.0`, revision
  `2026-07-29` on the five changed bundled pages, the ledger's
  `REPAIR REQUIRED` state, the two explicit Evergreen modes, the approved-only
  update checklist, the corrected changelog limitations, and no console
  warnings or errors.

The resulting uncommitted local PWA identity is build `85013e8f2adb`, content
hash
`7568ec394bb6450ad36d573327cfde877227f23658ce47f8bbe6e70934c02b64`,
and asset-manifest SHA-256
`5852348d5c755f0fef4d8e9b1f2f0783b3ba00bd65b0993413dc90d39b5d9477`.
This closes the rendered-consumer portion of `C1-GOV-014`. It is not an
immutable candidate, deployment, or release acceptance and does not close
`C1-GOV-011`, `C1-GOV-012`, `C1-GOV-013`, or `C1-GOV-015`.

## Decision

The project now has a stronger ground-up audit contract, but adding audit
rules does not make the product pass. `C1-GOV-011`, `C1-GOV-012`,
`C1-GOV-013`, and `C1-GOV-015` require separately approved repairs that
normalize the technical test manifest, create the complete machine-checked
requirement-test-evidence graph, close the parser/schema bypasses, reconcile
rollback semantics with adversarial negative controls, and separate content
revision from source verification.
