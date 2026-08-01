# Course 1 Release and Supply-Chain Repair Evidence

> **Historical intermediate repair record — superseded.**
> This file preserves the state observed during an earlier repair step on
> 2026-07-28. Its blocked Python result and `REPAIR REQUIRED` statement are not
> current. Follow
> [`COURSE_1_V2.6.0_REPAIR_CANDIDATE_2026-07-28.md`](COURSE_1_V2.6.0_REPAIR_CANDIDATE_2026-07-28.md)
> and the authoritative ledger for the final candidate status.
>
> **Later follow-up — 2026-07-29:** `C1-GOV-007` is now
> `EVIDENCE PENDING`, not implementation-failed; its repository, scheduled-run,
> and named manual-source evidence remains missing. `C1-GOV-011` is also
> `EVIDENCE PENDING` with its all-33-test gate implemented, while
> `C1-GOV-013` and `C1-GOV-015` are `CLOSED`. The current product status is
> `UNVERIFIED`.

## Decision boundary

- Date: `2026-07-28`
- Timezone: `Europe/Amsterdam`
- Scope: local implementable portions of `C1-TECH-003`, `C1-TECH-006`,
  `C1-GOV-002`, `C1-GOV-006`, and `C1-GOV-007`
- Result: **PARTIAL REPAIR EVIDENCE**
- Product decision at that intermediate point: unchanged; the ledger remained
  `REPAIR REQUIRED`
- External changes performed: none
- GitHub deployment, settings, environments, services, secrets, and alerts:
  not changed

This record is repair evidence, not release acceptance and not a Course 1
`PASS`.

## Dependency evidence

- Replaced vulnerable `pytest==9.0.2` with `pytest==9.1.1` everywhere in the
  active Course 1 setup, stack, and evidence checks.
- Added the previously floating Python 3.12 transitive requirement
  `typing-extensions==4.16.0` to both exact requirement sets.
- The offline inventory, licence allow-list, source-distribution provenance,
  and CycloneDX SBOM agreement gate passed for 13 exact Python packages.
- The online PyPI metadata, PyPI vulnerability, and OSV querybatch gate passed
  for all 13 exact versions with no reported vulnerability.
- Clean installation, `pip check`, and the then-current 67-test clean-room
  acceptance passed on Windows with Python `3.13.14` and `3.14.6`. A later
  integrated audit-timestamp change introduced a current regression described
  in the validation table; both versions require a fresh green run after that
  owning repair.
- Python `3.12.13` was not repeated locally because that security-only Python
  release has no official Windows embeddable package. The pinned
  `ubuntu-24.04` continuous-integration matrix owns the exact `3.12.13` run.
- Node `24.18.0` was downloaded from the official Node distribution and its
  Windows archive SHA-256 matched `SHASUMS256.txt`.
- `npm ci` and `npm audit` passed with one package root and zero
  vulnerabilities.
- Every full GitHub Action commit used by the four workflows resolved through
  the official GitHub API and matched the exact version tag written beside it.

Official evidence:

- `https://github.com/advisories/GHSA-6w46-j5rx-g56g`
- `https://pypi.org/project/pytest/9.1.1/`
- `https://google.github.io/osv.dev/api/`
- `https://nodejs.org/dist/v24.18.0/SHASUMS256.txt`

Remaining supply-chain limits are explicit in `supply_chain/README.md`.
Source-distribution hashes are not wheel-install hashes; pip
`--require-hashes`, full wheel provenance, GitHub Action/toolchain SBOM
coverage, end-of-life automation, and live repository alert settings were not
yet complete. Therefore, at that intermediate repair point, broader
supply-chain governance remained `PARTIAL`.

## Source-monitoring evidence

- `source_claims.json` maps all 27 URLs in `SOURCE_REGISTER.md` one to one.
- Every entry has a stable ID, topic, exact locator, course use, owner, access
  date, maximum age, check mode, and review trigger.
- All 26 automated official-source requests passed.
- The OECD small and medium-sized enterprise AI-adoption publication was
  opened manually at its exact official locator on `2026-07-28`.
- The machine report truthfully returns
  `PASS_WITH_MANUAL_REVIEW_REQUIRED` when a manual locator still needs dated
  human evidence; automated availability is not treated as claim correctness.

## Course 1 and Course 4 release separation

- Course 1 validation uses `--scope course1`; it checks Course 4 only for
  non-core structural isolation and shared-reader compatibility.
- Course 4 lesson, runnable-package, and fake-provider checks run in
  `.github/workflows/course4-offline.yml`.
- The Course 1 Pages dependency chain contains no Course 4 implementation job.
- A read-only negative control simulated a missing Course 4 demo `Dockerfile`:
  Course 1 scope passed and full Course 4 scope failed as intended.
- Shared `app/**`, `curriculum.json`, and validator changes trigger the Course
  4 shared-reader job.
- Actionlint `1.7.12` passed every workflow.

Actual independent GitHub workflow runs and a deliberate Course 4 failure run
are still required before `C1-TECH-006` can close.

## Candidate, promotion, and rollback controls

- Ordinary pull requests and pushes now validate only; no push-triggered job
  can deploy.
- Manual promotion requires the full candidate commit, a separate immutable
  post-review evidence commit, a matching acceptance record, all validation
  jobs, and the protected Pages environment.
- Acceptance and rollback match the complete artifact-tree SHA-256, including
  the service worker and every published file.
- The deployment job downloads the already tested artifact and does not
  rebuild.
- Empty, abbreviated, moving, or mismatched commit references fail explicitly
  instead of producing a successful skipped promotion.
- Promotion-record verification passed a controlled positive test and rejected
  the unchanged template/current `REPAIR REQUIRED` ledger as expected.
- Rollback has a separate manual workflow and authorization contract, so
  `REPAIR REQUIRED` does not disable emergency recovery.
- Rollback-record verification passed a controlled positive test.
- The local rollback rehearsal promoted a test candidate, restored last known
  good byte for byte, preserved the supplied learner-state backup hash, removed
  its own temporary public copy, and returned `PASS`.

Owner-controlled branch protection, required checks, Pages environment
reviewers, deployment, public identity, installed-client update, and live
rollback were not changed or claimed. Follow `ROLLBACK_RUNBOOK.md`.

## Validation results

| Gate | Result |
|---|---|
| JSON parsing for manifests, SBOM, claims, and templates | PASS |
| YAML parsing for stack, workflows, and Dependabot | PASS |
| Actionlint for all workflows | PASS |
| `git diff --check` | PASS |
| Course 1 package validator with optional dependencies | PASS, 37 checks, 0 warnings |
| Full package validator | PASS, 37 checks, 0 warnings |
| Supply-chain gate, offline and online | PASS |
| Claim-source gate, online | PASS WITH MANUAL REVIEW REQUIRED; OECD manually opened |
| Python 3.13.14 clean-room acceptance | EARLIER PASS, 67 tests; rerun required after current integrated regression |
| Python 3.14.6 clean-room acceptance | BLOCKED; latest run had 5 failures and 4 errors across 67 tests after audit-timestamp hardening |
| Node 24.18.0 PWA unit/contract tests | PASS, 41 tests |
| npm advisory gate | PASS, 0 vulnerabilities |
| Local rollback rehearsal | PASS |
| Promotion and rollback verifier positive tests | PASS |
| Promotion verifier current-release negative control | EXPECTED FAIL |
| Real-browser PWA smoke | PASS; deterministic two-window merge, visible same-note conflict recovery, and cross-window reset propagation |
| Old-client update smoke | PASS; later build preserved, accepted update activated, learner state and unrelated caches survived |

The first real-browser run exposed a genuine two-window lost-update failure.
After the owning PWA repair, the exact Node `24.18.0` test, build, browser-smoke,
and old-client-update sequence passed on `2026-07-28`. The browser run covered
41 unit/contract tests and the real-browser concurrency, recovery,
accessibility, responsive-layout, offline, backup/import/reset, and blocked
storage controls described by the smoke runner. This closes that local blocker;
it does not replace the owner-controlled and live-environment gates listed
above.

The latest exact Python `3.14.6` clean-room run found a separate integrated
regression after the earlier green dependency evidence: decision and follow-up
fixtures now conflict with enforced nondecreasing audit timestamps. That runner
and test repair is outside this release-control file scope and blocks
promotion until the owner fixes it and all pinned Python jobs pass again.
