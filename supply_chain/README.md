# Course 1 Supply-Chain Evidence

This directory is maintainer evidence, not a learner installation step.

- `course1-dependencies.json` is the dated inventory and policy for the exact
  Course 1 and validator Python pins plus the dependency-free PWA package
  manifest.
- `course1-sbom.cdx.json` is the matching CycloneDX 1.6 Software Bill of
  Materials (SBOM).
- `python-artifact-lock.json` records every current non-yanked wheel and source
  distribution published for each exact Python dependency.
- `tools/audit_course1_supply_chain.py` proves that the hash-required
  requirement files, artifact lock, inventory, approved licences, CycloneDX
  SBOM, full-commit GitHub Actions, fixed toolchains, current package metadata,
  PyPI/Open Source Vulnerabilities (OSV)/GitHub advisory results, and official
  CycloneDX schema agree.

Both Python requirement files force the official PyPI Simple API,
`--only-binary=:all:`, and `--require-hashes`. Every direct and transitive pin
lists the complete reviewed artifact-hash set, while installation accepts
wheels only. A changed or unlisted artifact therefore fails before package
installation.

`tools/requirements-maintainer.txt` is a third, separate hash-required lock for
coverage tooling used by the release-quality gate. It must not be added to the
beginner installation instructions or merged into `requirements-course.txt`.
The supply-chain audit and quality-contract tests enforce that boundary.

The PWA currently declares zero external npm dependencies. The workflows still
run `npm audit` against its lock and Dependabot monitors npm and GitHub Actions.
The SBOM models the Python artifacts, external Actions, fixed Python and Node
runtimes, declared GitHub-hosted runner family, and recorded local Chrome/Edge
test runtimes. A release record must still capture the exact hosted-runner
revision and browser binaries resolved by that run; repository security
settings and scheduled-run history remain external evidence gates.

For an intentional dependency update:

1. verify current official package metadata and advisories;
2. update every affected exact dependency version and licence record together;
3. run `tools/update_course1_dependency_locks.py` to regenerate the artifact
   lock, both hash-required requirement files, and SBOM from official PyPI
   metadata;
4. review every generated artifact and inventory change;
5. run the offline and online supply-chain audit;
6. perform clean installs, `pip check`, and the full Python 3.12-3.14
   clean-room matrix;
7. preserve the reports and independent review under `release_evidence/`;
8. update the ledger without calling the broader supply chain complete unless
   every frozen technical-acceptance requirement passed.
