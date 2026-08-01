# Course 1 Release, Promotion, and Rollback Runbook

## Boundary

This is maintainer guidance for the Course 1 Progressive Web App (PWA). It is
not a learner exercise and it does not authorize a deployment.

The repository now separates five decisions:

1. **candidate validation** tests a frozen commit and preserves its built
   artifact;
2. **personal-study publication** distributes an exact technically checked
   artifact while keeping product and competence status `UNVERIFIED`;
3. **acceptance** is an independent, post-build evidence decision;
4. **promotion** revalidates a byte/fingerprint-identical build and manually
   deploys that tested artifact without another rebuild;
5. **rollback** manually restores the named last-known-good commit through a
   separate controlled path.

This is the intended lifecycle, not proof that every release gate has passed.
The fail-closed parser repair recorded under `C1-GOV-012` is covered by
adversarial tests; candidate, public, installed-client, and repository-control
evidence remain separate gates. Do not treat this runbook wording as release
evidence.

An ordinary pull request or push to `main` validates only. It cannot deploy.
Only the separately authorized `personal-study` or `promote` dispatch can
publish.
Course 4 offline tests also have their own workflow and are not a Course 1
deployment dependency.

## One-time repository controls still requiring an owner

The files in this repository cannot configure these GitHub account settings.
Before treating the release path as controlled, the repository owner must:

1. set Pages to use **GitHub Actions**;
2. protect `main`, require a pull request, prevent bypass for ordinary
   maintainers, and require the Course 1 validation jobs;
3. do not make the Course 4 offline-demo job a required Course 1 promotion
   check;
4. protect the `github-pages` environment with a required reviewer;
5. enable the dependency graph, Dependabot alerts, and security updates;
6. confirm scheduled-workflow failure notifications reach the maintainer.

Record screenshots or settings locators in the release evidence. Until these
controls are verified, `C1-GOV-002` remains `EVIDENCE PENDING`.

## Personal-study publication

Use this lane only when the user has explicitly authorized distribution for
their own synthetic study before the complete human evidence exists.

1. Keep the authoritative product status exactly `UNVERIFIED` and the
   machine-readable distribution purpose exactly `personal-synthetic-study`.
2. Confirm that no High or Medium finding is `OPEN`, `PARTIAL`, or `REOPENED`
   and that every `EVIDENCE PENDING` finding is in the study verifier's closed
   allowlist. This permission does not close any finding.
3. Freeze a clean full commit through a pull request and pass every validation,
   Python matrix, source/supply-chain, quality, PWA, browser, offline, and
   version 2.5 update-rehearsal check.
4. Preserve a version 2.5 learner-state backup and the exact accepted version
   2.5 rollback artifact.
5. Manually run **Course 1 candidate validation and controlled Pages
   publication** on `main` with:
   - `mode`: `personal-study`;
   - `accepted_commit`: the exact current full `main` commit;
   - `study_boundary_acknowledgement`:
     `UNVERIFIED-SYNTHETIC-STUDY-ONLY`.
6. If the owner has configured a required reviewer on `github-pages`, approve
   it only after the isolated study verifier reports the exact commit,
   `UNVERIFIED` product status, `personal-synthetic-study` purpose, no known
   defect, and the intended evidence-pending set. If no approval prompt exists,
   record that missing repository control under `C1-GOV-002`; the typed study
   acknowledgement and main-only policy still bind this authorized dispatch
   but do not substitute for reviewer protection.
7. Immediately verify the public version, manifest assets, asset manifest,
   service worker, browser console, navigation, offline cold reopen, and the
   preserved old-client update. GitHub Pages does not serve `.nojekyll`; verify
   it in the uploaded artifact and exclude it from the public served-tree hash.
   The workflow runs `tools/verify_course1_public_artifact.py` for the exact
   learner-facing root and public bytes; preserve its report, then perform the
   browser and installed-client checks that byte comparison cannot prove.

This lane cannot produce product `PASS`, `COURSE 1 COMPETENCE: PASS`, or Course
2 readiness. A live defect triggers rollback; missing human evidence remains
`UNVERIFIED`.

## Candidate and acceptance for an accepted release

The current 2.6.0 personal-study artifact cannot enter this lane. Before these
steps, create and review a new commit that intentionally changes the closed
distribution metadata and matching build/PWA validators from
`personal-synthetic-study` to `accepted-release-candidate`. That change creates
a new artifact and must repeat all technical and human gates; it must never be
applied as a deployment-time relabel.

1. Resolve every non-promotion-dependent High and Medium ledger item.
2. Set the authoritative release status to `UNVERIFIED`: no known defect
   remains, but public and installed-client evidence does not yet exist.
3. Freeze the candidate as a full 40-character commit SHA.
4. Manually run **Course 1 candidate validation and controlled Pages
   publication** at that exact commit with mode `validate`.
5. Download and retain:
   - `course1-candidate-<commit>`;
   - `course1-audit-evidence-<commit>`;
   - the complete workflow run URL and logs.
6. Have an independent reviewer reproduce the required gates and inspect the
   ledger. Copy
   `release_evidence/templates/course1-promotion-acceptance.template.json` to a
   dated JSON record. Generate the exact candidate block from the unpacked
   workflow artifact:

   ```powershell
   python tools\course1_artifact_identity.py `
     --commit REPLACE_WITH_FULL_CANDIDATE_SHA `
     --dist C:\path\to\unpacked-candidate
   ```

   This includes the complete artifact-tree fingerprint, including the service
   worker, rather than only selected metadata.
7. Commit only that post-review record on a review/evidence branch. Record this
   separate full commit SHA. This avoids changing the already tested candidate.

## Manual accepted-release promotion

Run **Course 1 candidate validation and controlled Pages publication** again at
the exact candidate commit:

- `mode`: `promote`
- `accepted_commit`: exact candidate commit
- `acceptance_record`: the record path beginning with `release_evidence/`
- `acceptance_record_commit`: exact commit that stores the post-review record

The workflow rebuilds and retests the candidate, downloads the already tested
artifact rather than rebuilding in the deployment job, and verifies its commit,
course version, build ID, content hash, asset-manifest hash, reviewer, gates,
and ledger state. The protected `github-pages` environment is the final manual
promotion stop.

## Immediate live verification

Keep a prior installed client and a learner-state backup before either
publication lane. After deployment, record all of the following:

- public URL and deployment run;
- commit, course version, build ID, content hash, manifest ID, scope, and start
  URL;
- asset-manifest, uploaded complete-artifact-tree, and public served-tree
  Secure Hash Algorithm 256-bit (SHA-256) values. The public served tree is the
  manifest-listed assets plus `asset-manifest.json` and `sw.js`; `.nojekyll`
  remains an uploaded deployment control and is expected to return HTTP 404;
- clean navigation, console, offline cold reopen, and search;
- **Later**, **Update now**, foreground return, and cold reopen from the prior
  installed client;
- preserved reading state, practical checks, notes, and appearance;
- browser, version, operating system, device, install mode, reviewer, and
  timestamps.

Only after those checks pass may the release become `PASS`. Missing live
evidence is `UNVERIFIED`; an observed defect is `REPAIR REQUIRED`.

## Rollback triggers

Start rollback for a blocking public mismatch, boot failure, broken offline
reopen, destructive state migration, unusable navigation, wrong release
identity, or another release-blocking defect. Stop further promotion and
capture the failed identity before changing production.

Rollback must never depend on changing the failed candidate or relabelling it
as accepted.

## Local rollback rehearsal

Keep an unpacked candidate artifact, an unpacked last-known-good artifact, and
a PWA learner-state backup export in three different locations. Then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File `
  tools\rehearse_course1_rollback.ps1 `
  -CandidateArtifact "C:\path\to\candidate" `
  -LastKnownGoodArtifact "C:\path\to\last-known-good" `
  -LearnerStateBackup "C:\path\to\learner-state-backup.json" `
  -ReportPath "C:\path\to\course1-rollback-rehearsal.json"
```

The rehearsal copies only into a unique temporary directory, promotes the
candidate there, restores last known good, compares every restored file hash,
confirms that the supplied learner-state backup did not change, and checks that
the rollback target can read that backup's state schema. It removes its own
temporary directory. It does not deploy, open a browser, or alter the source
artifact directories. A schema-compatibility failure is a stop result, not a
warning to ignore.

Use `release_evidence/templates/course1-rollback-evidence.template.json` for
the live drill evidence. A local rehearsal is useful but cannot close the
installed-client or public rollback requirement.

## Controlled production rollback

1. Set the ledger to `REPAIR REQUIRED` or `UNVERIFIED` and record the trigger.
2. Fill
   `release_evidence/templates/course1-rollback-authorization.template.json`
   with the failed commit, exact last-known-good commit and identity, prior
   acceptance locator, state-risk assessment, evidence, and authorizer. The
   prior acceptance locator is a closed `path` plus `sha256` object. For a
   normal `manifest-v1` rollback, it must resolve to a hash-valid, independently
   accepted promotion JSON record for the exact rollback target, with complete
   32-test evidence no later than this authorization. The v2.5 exception must
   resolve to the exact pinned historical Markdown record. Its closed rollback
   evidence array must include candidate-bound passing records for
   `C1-TST-PROV-001`, `C1-TST-RECOVERY-001`, and `C1-TST-SW-002`; other test
   IDs, missing IDs, duplicates, unsafe paths, wrong hashes, missing raw
   artifacts, or incomplete procedure/environment coverage block rollback.
3. Commit the authorization record to the current control branch.
4. Manually run **Course 1 controlled Pages rollback**:
   - `last_known_good_commit`: full immutable 40-character commit SHA;
   - `rollback_record`: authorization path beginning with
     `release_evidence/`.
5. If the required `github-pages` reviewer control is configured, approve it
   only after the workflow rebuilds the old commit, passes its clean-room and
   PWA tests, and proves that the artifact matches the authorization record.
   Without that live control, keep `C1-GOV-002` pending and do not claim a
   reviewer-protected rollback.
6. Verify public identity, offline cold reopen, and preserved learner state.
7. Complete the rollback evidence template and reopen the affected ledger IDs.

### Explicit legacy v2.5 artifact

The accepted v2.5 source commit
`69d868a713d42b19b12ec11c64898b29e829be71` predates
`asset-manifest.json`. It is permitted only as the exact rollback-only format
`legacy-v2.5`, with:

- version `2.5.0`;
- build ID `ad5f59e8f800`;
- content hash
  `ddc88ff3b2a9ac9080b05abebad5f578de122406a6bab00bb52b28a92353258a`;
- artifact-tree SHA-256
  `df958cd62ff5ddd76cace021d86c46eb6f4a252215467487170639d72d84462d`;
- the exact historical 14-file inventory;
- `assetManifestSha256: null`.

Any other artifact without `asset-manifest.json` fails. This exception cannot
be used for promotion, a different commit, a modified v2.5 build, or a future
release.

Identity validation is not learner-state compatibility. v2.5 reads state
schemas 1 and 2; it does not read the v2.6 schema-3 storage envelope. Therefore
a successful legacy artifact check does **not** authorize a downgrade for a
browser that has already used v2.6. Preserve the raw browser storage and
backup, run the compatibility rehearsal, and do not approve deployment until a
verified recovery path satisfies `C1-TA-REC-009` and `C1-TA-REC-010`. The
immutable browser regression proves the supported v2.5-to-v2.6 upgrade; it does
not claim that the reverse direction is safe.

The rollback workflow accepts exactly one unquoted authoritative
`REPAIR REQUIRED` or `UNVERIFIED` status, while personal-study publication and
normal accepted-release promotion each accept exactly one unquoted
authoritative `UNVERIFIED` status through separate verifiers. Historical prose,
quoted text, duplicate markers, and status substrings are rejected by the
adversarial parser suite recorded under `C1-GOV-012`; finding-like rows inside
block quotes are rejected as misleading rather than ignored.

## Failure handling

- If candidate validation fails, repair and create a new candidate commit.
- If acceptance evidence disagrees, retain both reports and adjudicate; do not
  promote.
- If the promotion verifier fails, do not edit the record to force a pass.
  Correct the evidence or rerun the complete candidate process.
- If rollback verification fails before deployment, keep the current public
  version in place and investigate the named mismatch.
- If learner-state recovery is uncertain, preserve backups and raw browser
  storage evidence before trying another migration or reset.
