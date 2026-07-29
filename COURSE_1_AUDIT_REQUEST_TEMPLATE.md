# How to Request a Course 1 Ground-Up Audit

## The important change

Do not ask only:

> “Do one final audit and fix everything.”

That wording communicates the intention, but it does not force the auditor to
separate diagnosis from repair, inventory requirements that current tests do
not know about, challenge the audit controls themselves, or distinguish local
technical evidence from human and live-release evidence.

The safest audit-and-repair approach uses two explicit requests. Candidate
creation, commit, promotion, and deployment are a separate release decision.

## Request 1 — Diagnose from the ground up

```text
Perform a ground-up, adversarial, evidence-based audit of Course 1 using
COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md.

This first pass is diagnostic and read-only. Do not repair, commit, push,
deploy, activate billing, use cloud resources, or use real data.

Treat every previous PASS, test suite, acceptance record, audit report, and
course claim as something to verify, not as inherited truth.

Course 1 is in scope. Course 4 and later courses are out of scope except for
explicitly shared PWA, workflow, or release surfaces. Keep their statuses and
evidence separate.

Start from the product goal, literal-beginner promise, supported computer,
threat model, technical contract, learning-validation contract, current
ledger, curriculum, exercises, runner, data, schemas, PWA state, service
worker, dependencies, sources, workflows, release controls, public artifact,
and installed-client requirements.

Build a complete machine-readable inventory of every stable requirement,
finding, test, evidence class, claim, environment, and release gate. Map every
requirement to positive, negative, missing, malformed, boundary,
contradictory, and combined evidence where applicable. Verify that every test
maps back to a requirement and actually checks the stated criterion.

Try to disprove the controls in disposable isolated copies, temporary fixtures,
or purpose-built harnesses that cannot change the frozen project baseline.
Include deliberate defects in both the product and the audit mechanism:
omitted tests, stale or wrong-candidate evidence, dirty working tree, parser
row/column/status bypasses, Course 1/Course 4 scope bleed, multi-tab state
races, failed storage/render rollback, hostile backup, cache/manifest tamper,
and post-test changes that should invalidate evidence.

Keep automated, AI-assisted, literal-beginner, assessor/UAT, practitioner,
legal/privacy, security, accessibility/device, repository, manual-source,
installed-client, and live-production evidence separate.

Before proposing repairs, audit your own audit for missing product surfaces,
requirement families, environments, evidence classes, combined failures,
parser bypasses, stale references, and final-change invalidation.

Return:
1. frozen baseline and scope;
2. authority and complete requirement inventory;
3. requirement-test-evidence coverage map;
4. findings with severity, owner, closure test, and evidence class;
5. audit-of-the-audit gap review;
6. confirmed defects versus missing evidence;
7. current authoritative ledger status and any recommended status change;
8. one coherent repair plan, ordered by dependency and risk.

Stop after the plan and wait for my approval.
```

## Request 2 — Implement the approved repair

```text
Implement the approved ground-up Course 1 repair plan using
COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md.

Keep the frozen pre-repair audit unchanged as historical evidence. Give every
repair a finding ID, requirement, owner, positive and adversarial regression
test, evidence class, and closure condition.

Update all affected producers and consumers together, including contracts,
schemas, parsers, templates, workflows, tests, reports, and status language.
Any change to source, content, tests, audit tools, requirements, fixtures,
dependencies, workflows, or evidence invalidates the affected earlier result.

After the final material change:
1. run the complete integrated suite in fresh supported environments;
2. run the audit-assurance rules and deliberate negative controls;
3. obtain independent technical, learning/content, PWA/accessibility, and
   governance rechecks;
4. reconcile disagreements;
5. update the authoritative ledger with the evidence-backed result;
6. if I separately authorized a commit/candidate freeze, create the clean
   immutable candidate and record its exact final hashes. Otherwise stop with
   an explicitly uncommitted, unpromotable evidence snapshot and tell me what
   separate release authorization would be required.

Do not call the product PASS unless every mandatory technical, human,
repository, device, installed-client, and live-release gate has current
evidence. A known defect is REPAIR REQUIRED. Missing evidence without a
reproduced defect is UNVERIFIED.

Do not deploy, commit, push, activate billing, use cloud resources, or use real
data unless I separately authorize that exact action.
```

## Short form

When the project already contains the protocol, this is enough:

```text
Run a read-only ground-up Course 1 audit under
COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md. Treat prior results as claims, build the
complete requirement-test-evidence graph, perform adversarial audit-self-tests,
using only disposable isolation, audit the audit for missing coverage, and
return the frozen findings plus one repair plan. Do not edit the project until
I approve it.
```

The longer request is still preferable before a release or after a serious
audit/control failure.
