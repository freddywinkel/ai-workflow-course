# Course 1 learning-validation evidence

Current state: **17 requirements UNVERIFIED — COURSE 1 LEARNING ACCEPTANCE:
NOT YET**.

This directory is an evidence destination, not evidence itself. Do not add a
version folder until one immutable Course 1 candidate exists and a named
method in
`audit_control/course1/learning_claim_evidence_matrix.json` has actually been
performed.

For a real result:

1. copy
   `release_evidence/templates/COURSE_1_LEARNING_EVIDENCE_RECORD.template.json`;
2. place the completed redacted JSON under
   `release_evidence/course1_learning_validation/<course-version>/`;
3. replace every template value and bind the record to the exact full commit,
   course version, practice revision, build ID, and content hash;
4. validate it against
   `audit_control/course1/learning_evidence_record.schema.json`;
5. calculate its Secure Hash Algorithm 256-bit (SHA-256) value and add that
   exact path/hash only to the matching matrix row;
6. rerun the fail-closed package validator.

Do not commit raw audio, video, screen recordings, names, employer details,
health information, credentials, client information, or temporary observation
notes. Human evidence uses participant/reviewer codes and the consent,
access, minimisation, retention/deletion, and non-evaluation fields in the
schema. Missing consent, prohibited data, or an unconsented recording
invalidates the result; do not copy it here.

A matrix row remains `UNVERIFIED` with an empty `records` array until valid
candidate-bound evidence exists. A green structural validator does not change
that state.
