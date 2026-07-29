# Course 1 Ground-Up Audit Protocol

- Document ID: `C1-GAP`
- Protocol version: `1.0.0`
- Effective date: `2026-07-29`
- Scope: Course 1 only
- Status: **Normative audit-method and audit-assurance baseline**
- Owner: Course 1 maintainer

## 1. Why this protocol exists

A “full,” “final,” “last,” “100%,” or “ground-up” audit must test whether the
audit itself is complete. It is not a larger wording review, a maintenance
refresh, a green test run, or a sequence of repairs followed by the assumption
that everything now passes.

This protocol was added after repeated Course 1 audits found important defects
only after earlier findings had been repaired. The permanent lesson is:

> Do not begin with the current tests and ask whether they pass. Begin with the
> product, its promises, risks, requirements, users, environments, evidence
> classes, and release path; then prove that every one is represented by an
> adequate current check.

## 2. Authority hierarchy

Use these authorities together without allowing one to substitute for another:

1. `AGENTS.md` and `STRATEGIC_FOCUS.md` authorize or reject material work.
2. This protocol owns the **ground-up audit method** and audit-of-audit rules.
3. `COURSE_1_PRODUCT_THREAT_MODEL.md` owns protected assets, threats, trust
   boundaries, abuse cases, and review triggers.
4. `COURSE_1_TECHNICAL_ACCEPTANCE_CONTRACT.md` owns technical requirements and
   required technical evidence.
5. `COURSE_1_LEARNING_VALIDATION_CONTRACT.md` owns learning, beginner,
   assessment, accessibility, and human-evidence requirements.
6. `COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md` owns current product status,
   finding status, and reopen decisions.
7. `EVERGREEN_UPDATE_PROMPT.md` is a time-sensitive market, source, legal,
   security, and software-delta module. It is not a substitute for this
   protocol and cannot silently turn diagnosis into repair.
8. `RELEASE_VALIDATION.md` and `ROLLBACK_RUNBOOK.md` own post-audit candidate,
   promotion, live-verification, and recovery execution.

If two documents conflict, stop and open a named finding. Do not choose the
more convenient interpretation.

## 3. When the protocol is mandatory

Run this complete protocol when:

- an audit, review, or product-pass request uses “full,” “final,” “last,”
  “100% sure,” “from the ground up,” “full product pass,” or equivalent
  wording;
- Course 1 is proposed for acceptance, promotion, or a new `PASS`;
- the product promise, learning sequence, assessment, runner, PWA state,
  service worker, release controls, supported environment, or evidence
  vocabulary changes materially;
- a serious defect, audit bypass, near miss, stale acceptance claim, or
  contradictory evidence is found;
- a prior audit repeatedly discovers new requirement families only after
  repairs have begun.

A scheduled source refresh, single-file review, narrow regression check, or
configuration inspection is a **delta audit**. Label it as such and do not call
it a full product audit.

## 4. Audit modes must stay separate

### Mode A — Ground-up diagnosis

Read-only with respect to the frozen project baseline. Freeze the baseline,
inventory the product and requirement universe, challenge the current checks,
record findings, audit the proposed audit for missing coverage, and produce a
repair plan. Deliberate mutations may run only in disposable isolated copies,
temporary fixtures, or purpose-built harnesses that cannot alter the baseline.
Return artifacts in the response or a separately authorized temporary
location. Do not persist audit outputs in the repository or repair anything
while the baseline is still being diagnosed.

### Mode B — Approved repair

Requires the user’s approval and `STRATEGIC FIT: PASS`. Repair the named
findings, add positive and negative regression evidence, and update all
affected contracts, schemas, parsers, templates, workflows, and status
consumers together.

### Mode C — Post-repair independent re-audit

Use the final changed tree, fresh environments, and reviewers who did not own
the relevant repairs. Repeat the complete integrated audit and the
audit-of-audit checks. A repair author’s green rerun is useful evidence but is
not independent acceptance.

### Mode D — Release acceptance

Freeze a clean immutable candidate. If promotion revalidates or rebuilds that
source, require the resulting bytes and fingerprints to match the accepted
candidate evidence. Deployment must use the tested promotion artifact without
another rebuild. Complete public, installed-client, accessibility/device, and
rollback evidence. Local technical success alone cannot become product
`PASS`.

## 5. Required ground-up sequence

### Phase 0 — Classify and constrain

1. Record the audit mode, scope, exclusions, date, timezone, and authority.
2. Apply the strategic-focus gate.
3. Keep Course 4 and later courses out of scope except for explicitly
   classified shared files and release coupling.
4. Record prohibited actions: no deployment, billing, cloud activation, real
   data, external messages, or destructive action unless separately
   authorized.

### Phase 1 — Freeze the untouched baseline

1. Record branch, full commit, dirty/untracked state, file inventory, file
   hashes, configured course version, practice revision, build identity, and
   existing public identity if relevant.
2. Preserve the pre-repair status ledger and dated audit report.
3. Record the exact computer, operating system, shell, browser, runtime,
   locale, timezone, filesystem, and installed/ordinary-browser mode.
4. Do not treat a maintainer runtime, cached dependency folder, or existing
   browser profile as the learner’s clean setup.

### Phase 2 — Build the complete requirement universe

Machine-enumerate every current:

- threat, invariant, abuse, residual-risk, and review-trigger ID;
- technical acceptance requirement and named technical test ID;
- learning-validation requirement and evidence class;
- ledger finding and closure test;
- curriculum promise, learning outcome, assessment gate, support claim, and
  release claim;
- schema, fixture, rule, template, workflow, dependency, source claim, PWA
  route, persistent-state key, cache, and published artifact.

Unknown, duplicate, malformed, retired-ID reuse, unparsed, missing, or
contradictory entries fail this phase.

### Phase 3 — Build the requirement-test-evidence graph

For every requirement, record:

- requirement ID and owner;
- risk or learner claim;
- positive case;
- negative, missing, malformed, boundary, contradictory, and combined cases
  where applicable;
- test or manual procedure ID;
- execution environment;
- evidence class;
- exact evidence locator and hash;
- candidate identity;
- current result;
- limitation and expiry or rerun trigger.

Every test must map back to a requirement. A file, phrase, heading, checkbox,
non-empty cell, test count, or narrative summary is not sufficient when the
criterion concerns meaning, behavior, recovery, comprehension, or human use.

### Phase 4 — Challenge the product and the audit controls

Attempt to disprove each critical control. Deliberately seed:

- one product defect per critical control family;
- a removed, renamed, skipped, or uncounted test;
- stale, missing, wrong-hash, or wrong-candidate evidence;
- an unknown, duplicate, shifted, extra-column, missing, or contradictory
  ledger/status record;
- an out-of-scope Course 4 failure and a genuine shared-reader change;
- a dirty working tree and a build whose commit label does not describe its
  content;
- a post-test change that should invalidate earlier evidence; and
- a test-harness action such as closing or reloading a dirty page, firing a
  timer, replacing storage, or reaching a timeout that could itself create
  the mutation attributed to the product.

The gate must fail for the expected reason. A negative test that fails for an
unrelated reason is not evidence that the intended control works. For every
concurrency or rollback scenario, retain the deterministic interleaving and
raw before/after values for each affected key, and prove that harness actions
did not create the observed mutation.

### Phase 5 — Audit every product layer

The audit must cover all of these as separate evidence layers:

1. strategic fit, product promise, non-goals, and Dutch small and medium-sized
   enterprise relevance;
2. literal-beginner onboarding, current-computer setup, prerequisite order,
   first-use explanations, resume/retry paths, time and cognitive load;
3. explain → guided example → different recreation → read-only check → exact
   pass-criteria learning loops;
4. learner authorship, independent judgment, unseen transfer, delayed
   retention, oral assessment, real synthetic User Acceptance Testing (UAT),
   and accessibility evidence;
5. synthetic data, schemas, deterministic rules, oracle independence,
   evaluation, approval, source links, exports, failure, recovery, and
   prohibition of external actions;
6. runner input limits, path and file identity, lifecycle/audit ordering,
   atomicity, rollback, retry, bounded errors, environment denial, and exact
   clean-room test inventory;
7. PWA rendering, navigation, local-state privacy, startup failure,
   multi-tab/window/installed-context concurrency, conflicts, pending notes,
   reset barriers, recovery, and hostile backups. Include a real
   `window.open`/duplicated-tab scenario in which the new page inherits a
   `sessionStorage` sentinel but still receives a distinct per-page writer
   identity; `sessionStorage` reuse cannot be the writer-identity mechanism;
8. import and reset as full durable-storage **and visible-render**
   transactions, including injected failure at each boundary. Pre-import
   recovery remains durable until candidate save, readback, visible render,
   runtime trackers, note timers, route, and appearance all succeed; cleanup
   or finalisation failure is tested and recovery is removed only afterward;
9. per-key compare-and-preserve rollback. Restore the snapshot only when the
   current value still equals the failed transaction's last owned value or
   already equals the snapshot. If it differs from both, classify it as an
   external concurrent change and do not overwrite it. Preserve concurrent
   recovery evidence. Report primary state, reset barrier, recovery, runtime
   state, visible render, and rollback verification separately. A concurrent
   primary-state or reset-barrier change requires reconciliation and cannot be
   called a fully verified rollback. Use “changed/external,” not merely
   “newer,” because timestamps alone do not prove ordering;
10. in-app destructive confirmation, keyboard operation, Escape, focus
    containment/restoration, safe cancellation, zoom, forced colours, reduced
    motion, and assistive-technology limitations; native browser confirmation
    dialogs are prohibited for product actions;
11. the exact responsive viewports `320x568`, `390x844`, `430x932`,
    `834x1112`, `1440x900`, and landscape `844x390`; all 21 required pages at
    `320` CSS pixels with 125% reader text; themes, text scaling, landscape,
    safe areas, back/forward, console errors, unhandled rejections, Content
    Security Policy violations, and network interception for learner-state
    leakage;
12. service-worker provenance, exact asset hashes, candidate cache
    verification, redirects/content types, asset and manifest tamper, mixed or
    interrupted releases, Later/Update now, unrelated-cache preservation,
    offline cold reopen, and old-client state preservation;
13. exact fresh Python/runtime matrix, dependencies, licences, Software Bill of
    Materials (SBOM), advisories, toolchain identities, workflow permissions,
    source-claim currency, and every manual-browser locator;
14. Course 1/Course 4 structural, test, status, evidence, and release
    separation;
15. candidate, promotion, public identity, installed-client update, rollback,
    and learner-state preservation.

Static inspection, unit tests, real rendered-browser tests, installed-client
tests, human evidence, repository settings, and live-public checks remain
separate. No layer can silently substitute for another.

### Phase 6 — Audit the proposed audit before repairs

Before presenting a repair plan, answer:

1. Which product surface, promise, requirement family, environment, evidence
   class, failure mode, or release stage has no check?
2. Which check proves only presence or non-blank content rather than the stated
   semantic or behavioral criterion?
3. Which test reuses implementation constants or logic and therefore is not an
   independent oracle?
4. Which result depends on an existing cache, profile, interpreter, PATH,
   `PYTHONPATH`, session, network state, or hidden tool?
5. Which combined or concurrent failure is missing even though the individual
   steps pass?
6. Which parser can omit an unknown row, match the wrong column, accept a
   duplicate status, or find a historical marker instead of the authoritative
   one?
7. Which evidence reference does not exist, is stale, is not hash-bound, or
   belongs to another version/course?
8. Which edit would invalidate evidence already collected?
9. Which claim still relies on a human, device, repository, installed-client,
   or live check that has not happened?
10. What would a skeptical independent reviewer try that this audit did not?

Save this gap review with the untouched baseline findings. Only then propose
repairs.

### Phase 7 — Repair and invalidate honestly

1. Give every repair a finding ID, owner, requirement, test, evidence class,
   and closure condition.
2. Update a new status or vocabulary value in every producer and consumer:
   documentation, schema, parser, regular expression, template, workflow,
   verifier, tests, and report.
3. Changing source, content, tests, audit tools, requirements, fixtures,
   dependencies, workflows, or evidence invalidates every affected earlier
   result. Changing an audit tool invalidates that tool’s own earlier evidence.
4. Run affected tests during repair, then run the complete integrated suite
   after the **last** material change.
5. Do not record final build hashes before the content and build logic are
   frozen.

### Phase 8 — Freeze, reproduce, and adjudicate

This phase requires separate authority to create a Git commit or other
immutable candidate. Without that authority, stop after the final integrated
rerun with an explicitly uncommitted, unpromotable evidence snapshot and
request authorization.

1. Create a clean immutable candidate when authorized.
2. Install exact dependencies in fresh environments and profiles.
3. Run the frozen command/scenario manifest with zero unexplained skips.
4. Save raw outputs and hashes, not only summaries.
5. Have independent technical, curriculum/learning, PWA/accessibility, and
   governance reviewers reproduce their layers.
6. Preserve disagreements and adjudication.
7. Run this protocol’s audit-assurance rules against the final evidence.

### Phase 9 — Hand off to release controls

Only after the diagnostic, repairs, complete rerun, and independent
adjudication may the candidate enter `RELEASE_VALIDATION.md`. If promotion
rebuilds for revalidation, its bytes and fingerprints must match the accepted
candidate evidence; deployment uses that tested artifact without rebuilding
again. Public and installed-client checks follow promotion; missing live
evidence keeps the product `UNVERIFIED`.

## 6. Audit-assurance rules

These stable rules test whether the audit itself is trustworthy.

| ID | Rule | Minimum acceptance criteria |
|---|---|---|
| `C1-AA-001` | Frozen authority and scope | Clean full commit; exact in-scope file/hash inventory; explicit exclusions; every shared Course 1/Course 4 file classified; add/delete/rename/move negative controls fail. |
| `C1-AA-002` | Complete normative inventory | Every technical, learning, threat, abuse, finding, and test ID is uniquely machine-enumerated; unknown, duplicate, malformed, unparsed, or retired-ID reuse fails. |
| `C1-AA-003` | Requirement-test-evidence graph | Every requirement maps to a named executable or manual procedure, environment, owner, evidence class, and locator; every test maps back; no missing, contradictory, orphaned, skipped, or nonexistent scenario. |
| `C1-AA-004` | Status semantics | Product, finding, technical-evidence, and learning-result vocabularies remain separate and closed; `CLOSED` requires current candidate-bound evidence; `PARTIAL` always blocks; promotion permits `EVIDENCE PENDING` only where the ledger explicitly allows it. |
| `C1-AA-005` | Evidence provenance and freshness | Each result records candidate identity, command/procedure, exit/result, raw-log or artifact hash, tool/runtime/environment, reviewer, timestamp, evidence class, expiry, and rerun trigger; narrative prose alone cannot close. |
| `C1-AA-006` | Adversarial negative controls | A known defect is seeded in every critical product and audit-control family; the expected gate fails for the expected reason, including missing/skipped tests, stale evidence, wrong hashes, scope escape, dirty tree, malformed status records, and concurrency-harness side effects. |
| `C1-AA-007` | Exact candidate identity | Bind commit/tree, course/practice versions, content/build IDs, full artifact tree, asset manifest, requirement/test manifests, schemas, fixtures/oracle, locks/SBOM, source claims, workflows, and audit-tool hashes; compare public bytes after deployment. |
| `C1-AA-008` | Independent reproduction | A non-owner reviewer uses a separate clean environment, fresh installs, the exact candidate and commands, retained raw output, and recorded disagreement/adjudication; AI-assisted independence cannot substitute for named human expertise. |
| `C1-AA-009` | Final-change invalidation | A change-to-evidence map identifies every invalidated gate; all affected evidence is rerun; one integrated rerun follows the last material change; audit/test changes invalidate their own prior results. |
| `C1-AA-010` | Fail-closed audit parsers | Exact bounded schemas/rows/keys; exactly one authoritative current-status marker; complete row discovery; closed severity/status vocabularies; unknown, duplicate, historical-only, quoted-only, shifted, extra, missing, or contradictory data fails. |
| `C1-AA-011` | Clean environments | Clean Git state, fresh workspace/browser profile, exact supported runtimes/pins, dependency health checks, environment allowlist, no secrets/hidden session state, explicit locale/timezone/network boundary, and post-run pollution check. |
| `C1-AA-012` | External-evidence boundary | Automated, AI-assisted, learner, assessor/UAT, practitioner/legal/security, accessibility/device, repository, manual-source, installed-client, and production evidence remain machine-labelled and non-substitutable; missing evidence is `UNVERIFIED`, observed failure is `REPAIR REQUIRED`. |
| `C1-AA-013` | Meta-audit completeness | One machine-readable report lists every `C1-AA-*` rule as `PASS`, `FAIL`, or `UNVERIFIED`, with evidence and exclusions; overall audit `PASS` requires every mandatory rule and required external gate to pass. |
| `C1-AA-014` | Authority and consumer consistency | Every normative authority and every status, release, maintenance, assessment, and PWA consumer is inventoried; conflicting requirements or stale current-status text opens a named finding; one changed value is propagated to every producer, parser, template, workflow, report, and rendered consumer or the audit fails. |
| `C1-AA-015` | Authorization-safe execution | Diagnosis does not mutate the frozen baseline; destructive or defect-seeding trials use disposable isolation; repository evidence writes, repairs, commits, pushes, deployments, billing, external actions, and real-data use each require the authority stated by the controlling mode; impossible or contradictory requested actions stop with an explicit boundary. |
| `C1-AA-016` | Single-meaning metadata | Every date, version, revision, status, and verification field has one named meaning, owner, evidence source, and consumer set; content revision, claim/source review, tool execution, candidate identity, and release acceptance remain separate; changing one cannot silently advance another, and independent negative controls prove the separation. |

Stable audit-assurance IDs must not be renumbered or reused. A material change
to their acceptance meaning requires a new ID and retained retirement record.

## 7. Required audit artifacts

After repository-writing authority is granted, store a ground-up audit under:

`release_evidence/course1_ground_up_audit/<course-version>/<audit-date>/`

During read-only Mode A, return the same artifact set in the response or write
it only to a separately authorized temporary or external location. Repository
persistence begins in an authorized repair/evidence phase and must preserve
the untouched diagnostic baseline.

At minimum preserve:

1. `scope-and-authority.json`
2. `baseline-file-inventory.json`
3. `normative-id-inventory.json`
4. `requirement-test-evidence-graph.json`
5. `test-and-scenario-manifest.json`
6. `change-to-evidence-map.json`
7. `environment-and-toolchain.json`
8. `raw-evidence-index.json`
9. `pre-repair-findings.md`
10. `audit-gap-review.md`
11. `repair-and-invalidation-record.md`
12. `independent-review-and-adjudication.md`
13. `audit-assurance-result.json`
14. `final-decision.md`

The machine-readable files require closed schemas before they can support a
release. A path or non-empty string is not sufficient evidence: the referenced
artifact must exist, match its hash, belong to the named candidate, and have
the required evidence class.

## 8. Status handoff

Use qualified results:

| Layer | Allowed result |
|---|---|
| One audit-assurance rule | `PASS`, `FAIL`, `UNVERIFIED`, or explicitly justified `NOT APPLICABLE` |
| One technical requirement | the states defined by the technical acceptance contract |
| One learning requirement | the states and evidence classes defined by the learning validation contract |
| One repair finding | `OPEN`, `PARTIAL`, `EVIDENCE PENDING`, `CLOSED`, or `REOPENED` |
| Current Course 1 product | `PASS`, `REPAIR REQUIRED`, `UNVERIFIED`, or historical `SUPERSEDED` |

- A reproduced defect maps to `REPAIR REQUIRED`.
- Missing, expired, or unavailable evidence without a reproduced failure maps
  to `UNVERIFIED`.
- `EVIDENCE PENDING` is a finding status, not permission to infer a pass.
- A local automated pass may be reported as local automated evidence only.
- No score, average, majority, or reviewer confidence may compensate for a
  missing mandatory evidence class.

## 9. Permanent lessons from the 2026-07-28 to 2026-07-29 audit

| Observed audit gap | Permanent rule |
|---|---|
| Earlier acceptance and green checks were treated as a starting truth. | Rebuild the full authority, requirement, test, and evidence inventory from the current tree (`C1-AA-001`–`003`). |
| Audit and repair happened in the same discovery loop, so new requirement families appeared after fixes. | Freeze a read-only baseline and complete the audit-gap review before repair. |
| Structural/non-blank checks passed while semantic criteria were weak. | Require criterion-specific positive, negative, malformed, boundary, and combined evidence. |
| Automated evidence was mixed with beginner, assessor, UAT, accessibility, repository, and live evidence. | Keep evidence classes non-substitutable (`C1-AA-012`). |
| A new finding status was added to prose before every parser and template understood it. | Change every producer and consumer together; unknown values fail (`C1-AA-004`, `C1-AA-010`). |
| Greedy or substring parsing could read the wrong table column or a historical status marker. | Inventory broadly, parse the exact authoritative structure, require one marker, and adversarially shift/duplicate fields (`C1-AA-010`). |
| An evidence report was referenced before it existed, and old reports retained stale current-status language. | Verify existence, hash, candidate binding, history banner, and current-status precedence (`C1-AA-005`). |
| PWA state tests missed combined multi-tab reset, pending-note, render-failure, and concurrent-recovery races. | Require deterministic interleavings, full transactions, and compare-and-preserve rollback. |
| A duplicated or opener-created tab could inherit `sessionStorage` and reuse a writer identity. | Exercise a real `window.open` inheritance case and require a distinct per-page writer identity. |
| “Exact prior state” rollback wording conflicted with preserving an external concurrent recovery or state write. | Define per-key transaction ownership, compare-and-preserve semantics, separate result dimensions, and mandatory reconciliation of external primary/barrier changes. |
| Closing a dirty test tab triggered a page-hide write and created the mutation that the test blamed on the product. | Retain raw per-key before/after values and prove that close, reload, timer, timeout, and storage-stub harness actions did not cause the tested effect. |
| Browser-native confirmation and source inspection looked acceptable until the real interaction was exercised. | Test rendered keyboard/focus behavior and prohibit native product dialogs. |
| Service-worker success did not initially prove cached bytes and manifest integrity. | Tamper assets and manifest separately; require verified repair and last-valid offline fallback. |
| A clean test run used or risked inheriting packages and profiles from the machine. | Use fresh exact environments and record pollution boundaries (`C1-AA-011`). |
| Final documentation edits changed the PWA content hash after evidence had been recorded. | Any final change invalidates affected evidence; freeze identity only after the last change (`C1-AA-007`, `C1-AA-009`). |
| Course 4 implementation evidence appeared inside Course 1 release validation. | Classify shared surfaces and keep product evidence/status separate. |
| A local working copy was described as a candidate even though it was not an immutable commit. | Release identity requires a clean frozen commit/tree and exact tested artifact. |
| The audit did not initially test whether its own requirement-to-test map was complete. | Machine-check all stable IDs and both directions of the graph (`C1-AA-002`, `C1-AA-003`, `C1-AA-013`). |
| Read-only diagnosis, repository artifact storage, mutation tests, and candidate commits were requested together without matching authority. | Separate modes and make every write, isolated mutation, and candidate-freeze boundary operationally possible (`C1-AA-015`). |
| The ledger changed while release, maintenance, learning, and historical documents retained incompatible current-status or publishing language. | Inventory all normative authorities and consumers, open conflicts, and propagate changes everywhere (`C1-AA-014`). |
| The package validator used one `verifiedThrough` date both as a research/source claim and as the ceiling for unrelated governance-page revisions. | Give revision and verification fields one meaning each, validate them independently, and never advance source currency merely to make a content edit pass (`C1-AA-016`). |

## 10. What this protocol does not prove

Adding this protocol does not close a technical, learning, human, repository,
device, installed-client, or production finding. It defines how future audits
must detect and classify those gaps. The current product status remains whatever
the authoritative ledger says after the latest dated finding.
