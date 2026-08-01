# Course 1 technical and learning audit control

This folder is maintainer control material. It is not a learner exercise and it
does not make Course 1 technically or educationally accepted.

The authoritative technical contract is
`COURSE_1_TECHNICAL_ACCEPTANCE_CONTRACT.md`. The current control set contains:

- `technical_requirement_graph.json`: all 118 requirement identifiers and all
  33 declared test identifiers, mapped in both directions;
- `technical_test_manifest.json`: the owner, environment, evidence class,
  executable locator or manual procedure, and current evidence state for every
  declared test;
- `manual_test_procedures.md`: the named procedure for every manual or hybrid
  test;
- closed JSON Schemas for the graph, test manifest, candidate-bound technical
  evidence, 32-test promotion record, 33-test post-deployment final record,
  and rollback record.

The authoritative learning contract is
`COURSE_1_LEARNING_VALIDATION_CONTRACT.md`. Its separate control set contains:

- `learning_claim_evidence_matrix.json`: all 17 stable `C1-LV-*`
  requirements, claims, owners, evidence classes, methods, limitations,
  boundaries, and current decisions;
- `learning_claim_evidence_matrix.schema.json`: the closed matrix shape and
  status/evidence vocabulary;
- `learning_evidence_record.schema.json`: the closed candidate-bound learning
  evidence shape, including environment, people, method, observations,
  consent/privacy, limitation, and reviewer decision;
- `release_evidence/templates/COURSE_1_LEARNING_EVIDENCE_RECORD.template.json`:
  a non-evidence starting record whose placeholder values must all be replaced.

`UNVERIFIED` with an empty `records` array is deliberate. Existing supporting
tests or source inspection do not become release evidence until the complete
named procedure is run for one exact candidate. A verified evidence locator is
an object containing a repository-relative path under `release_evidence/` and
the SHA-256 of that exact JSON file. The evidence JSON records the test,
candidate commit, course version, build ID, content hash, result, timestamp,
and reviewer. Its closed `artifacts` array must hash-bind non-empty raw files
under `release_evidence/` and cover every procedure and environment declared
for that test. A command or environment name typed into a summary field is not
evidence. Hash binding proves which bytes were reviewed; it does not prove that
a screenshot, log, trace, or review conclusion is truthful. The named reviewer
still owns that semantic decision, and repository review controls must preserve
the record.

Run the structural and adversarial controls with:

```powershell
python tools\validate_package.py --scope course1
python -m unittest discover -s tools/tests -p "test_*.py"
```

The validator rejects missing, unknown, duplicate, malformed, contradictory,
unparsed, or orphaned graph entries; unsafe or missing evidence paths; hash
mismatches; duplicate evidence; unknown JSON fields and keys; and evidence
bound to different candidates. Pre-promotion acceptance requires passing
records for the 32 tests that can finish before a public deployment. The
post-deploy provenance test can be recorded only after the public artifact
exists. `tools/verify_course1_final_acceptance.py` and the separate
post-deployment workflow then require the exact prior promotion record, exact
public/candidate identities, a valid deployment chronology, and all 33
candidate-bound evidence records. The current test manifest still reports all
33 tests as `UNVERIFIED`: implementing the gate does not create the evidence.
The separately authorized personal-study lane instead uses
`tools/verify_course1_study_release.py` before deployment and
`tools/verify_course1_public_artifact.py` afterward. Those controls prove the
labelled study artifact and served bytes only; they do not satisfy or replace
the 32-test promotion record, the 33-test final record, learner evidence, or a
Course 1 `PASS`.
Rollback requires the declared provenance, recovery, and old-client records
plus a hash-checked prior accepted promotion record for the exact rollback
target.

The learning validator applies the same fail-closed principle. It rejects
missing, reordered, duplicate, unknown, or malformed requirements/methods;
unknown evidence classes or fields; missing procedure locators/selectors;
unsafe, non-versioned, missing, duplicate, wrong-hash, or cross-candidate
evidence; a `PASS` without every required evidence class; and any human record
without the complete synthetic-only consent, access, retention/deletion,
minimisation, and non-evaluation safeguards. The current 17 learning results
remain `UNVERIFIED` and `NOT YET`; a green structural validator does not
upgrade them.
