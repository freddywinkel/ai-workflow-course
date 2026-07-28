# Career Sequence — Controlled Artificial Intelligence (AI) Workflow Implementation Consultant

## Target role

The proposed destination is:

> I help Dutch small and medium-sized enterprises (SMEs) identify one
> recurring administrative bottleneck and implement a workflow with clear
> limits in their existing systems. A person reviews important results, the
> outcome is measured, a documented manual way of working remains available,
> and every responsibility has an owner.

The role combines understanding how work happens, building the change, testing
whether it works, helping people use it, and checking it regularly. It is not
defined by one model or automation platform.

## Plain-language terms used below

- **Production** means real daily business use rather than a practice
  demonstration.
- A **capability gate** is proof you must show before taking on the next level
  of responsibility.
- **Paid validation** means testing whether real firms will pay for a small
  service before you invest heavily in building it.
- A **problem assessment**, also called a **diagnostic**, is a fixed-scope
  investigation of the current work, pain, evidence, and possible next step.
- A **pilot** is a small controlled trial, not a full rollout.
- A **capstone** is the final practice project that combines earlier lessons.
- **Rule-first** means using ordinary fixed rules before considering AI.
- A **bounded AI step** is one narrow artificial intelligence task with stated
  inputs, outputs, limits, and human review.
- An **exception** is a record or situation that a stated rule says needs
  attention.
- An **integration** is a controlled connection through which systems exchange
  data or actions.

## Why the path is split into courses

No single course can responsibly take a literal beginner from zero knowledge
to independent production consultant.

Splitting the path:

- creates honest capability gates;
- allows paid market validation before years of technical study;
- separates low-risk pilot delivery from advanced document and production
  engineering;
- makes tool and legal updates easier;
- prevents one large capstone from being mistaken for complete professional
  readiness.

Course 1 is built in full in this progressive web app (PWA), an installable
website that can keep working without an internet connection. Course 4 now
also has one optional advanced capstone prototype. That prototype is useful
practice and a technical proof, but it is not the complete Course 4. Courses 2,
3, 5, 6, and the rest of Course 4 remain proposed separate builds.

## Course 1 — Controlled AI Workflow Foundations

Status: **Current course**

Outcome:

- observe and bound one low-risk process;
- build a rule-first workflow using made-up (synthetic) data;
- design one optional bounded AI contribution and test its controls with an
  offline mock; no live provider is used in Course 1;
- test failures and human control;
- evaluate and hand over a portfolio demonstration.

Proof:

- the Synthetic SME Operations Exception Assistant, a made-up-data practice
  workflow;
- final practice project (capstone) handover pack;
- one evidence-backed Course 1 result: `ACCEPT FOR SYNTHETIC PORTFOLIO`,
  `REWORK`, or `DO NOT CONTINUE`. Each result can pass when the evidence and
  closeout support it.

Boundary after completion:

- portfolio learner / workflow analyst in training;
- not ready for an independent production deployment, real sensitive data, or
  a client pilot. Discovery is taught in Course 2; a supervised low-risk pilot
  is taught in Course 3.

## Course 2 — Workflow Discovery and Paid Problem Assessments

Status: **Build next**

Purpose: learn to find a problem worth solving before offering implementation.

Proposed modules:

1. ethical outreach and confidentiality;
2. process interviews and observation;
3. stakeholder, system, and data mapping;
4. measure current volume, delay, repeated work, and current costs;
5. check what the existing software can already do and compare building with
   buying;
6. rank opportunities and exclude unsafe or unsuitable work;
7. write a problem-assessment report and a small-trial plan;
8. scope, assumptions, stop criteria, and presentation;
9. paid-validation practice using made-up or explicitly authorised low-risk
   cases.

Proof:

- one complete fictional diagnostic;
- interview script and notes template;
- fixed-scope diagnostic report;
- pilot recommendation with success and stop criteria.

Boundary after completion:

- may offer a clearly bounded workflow diagnostic;
- must not promise production implementation competence;
- legal, privacy, security, and regulated-domain conclusions remain excluded.

Market gate:

- interview 15 external target firms;
- identify at least five reporting materially similar pain;
- seek three genuinely paid diagnostics before building reusable software.

## Course 3 — Connect Small-Business Systems and Deliver a Small Trial

Status: **Planned**

Purpose: turn a diagnostic into one controlled low-risk pilot inside a
client-owned environment.

**Low-code** means building mainly with visual workflow blocks and settings,
while still using small amounts of code when necessary.

Proposed modules:

- application programming interfaces (APIs), which let systems exchange
  requests and responses;
- webhooks, which send an automatic notice when an event occurs, and Open
  Authorization (OAuth), a standard for granting limited access without
  sharing a password;
- connectors (prebuilt links between systems) and least privilege (grant only
  the access a task needs);
- n8n, a workflow-automation platform, plus maps of equivalent Microsoft and
  Google features;
- separate development, test, and live production environments;
- settings and secrets, meaning sensitive credentials such as passwords and
  access keys;
- safe repeat handling (idempotency), trying a failed step again (retry),
  queues for failed items, and returning to a known safe state (rollback);
- client-owned software environments (tenants) and sign-in credentials;
- user acceptance testing (UAT), release, and support boundaries;
- one low-risk internal pilot.

Proof:

- one reproducible integration lab;
- one supervised low-risk pilot or realistic isolated test environment
  (sandbox);
- proof that the result was accepted and that a known safe state can be
  restored.

Boundary after completion:

- bounded pilot implementer under client information technology (IT), privacy,
  and security review;
- not yet an advanced document-AI or high-risk systems specialist.

## Course 4 — Controlled Document AI Systems

Status: **Planned course; optional advanced capstone prototype available**

Purpose: build workflows whose statements remain tied to source evidence for
recurring business documents.

The available **Controlled Document Intake** capstone is not the recommended
next step for a certified beginner immediately after Course 1. First complete
Course 1 and gain the Course 3-equivalent skills needed to understand cloud
deployment, permissions, secrets, retries, and rollback. Then the capstone can
be used to combine those skills in one bounded Google Cloud demonstration.

The prototype:

- uses synthetic documents only;
- deploys a private scale-to-zero service on Google Cloud Run;
- uses European Union (EU)-supported Document AI and Vertex AI locations;
- lets fixed findings narrow the action type, then lets Gemini select bounded
  candidate identifiers within that boundary;
- uses fixed application code to render the exact source-linked summary and
  action wording and reject unrelated action evidence;
- requires a person to approve the exact output before comma-separated values
  (CSV) or JavaScript Object Notation (JSON) export;
- automatically removes uploaded file content;
- imposes a €60 prototype ceiling and includes teardown evidence;
- never authorizes activating paid billing or uploading real client, employer,
  medical, or personal data.

The bundled reference implementation recorded a live `PASS` on 28 July 2026
and was then torn down to project state `DELETE_REQUESTED`. The service is no
longer available. The account remained an unactivated Free Trial; the displayed
€0 cost is retained only as a timestamped value because Billing reports can
lag.

Open the capstone from the PWA Career Path tab or start with
[`advanced_capstone/README.md`](advanced_capstone/README.md).

The previous supplier course becomes the foundation for this course:

- source-file preservation and digital fingerprints (hashes);
- reading Portable Document Format (PDF) and Microsoft Word (`.docx`) files,
  including optical character recognition (OCR) for scanned text;
- references to exact source locations (evidence locators);
- extracting fields into a fixed structure (schema-constrained extraction);
- fixed checks that always give the same result for the same input
  (deterministic checks);
- finding the correct approved policy text (policy retrieval);
- drafting only claims tied to cited evidence (grounded drafting);
- human approval of the exact final output;
- document evaluation.

Proof:

- controlled synthetic document-intake demonstration;
- evidence that document reading and extraction still work after changes
  (regression evidence);
- reviewer demonstration;
- private deployment, cost-control, live-validation, and teardown evidence.

Boundary after completion:

- advanced synthetic document-workflow capability;
- production deployment still requires Course 5 controls and client review.

## Course 5 — Controls for Secure and Reliable Live Systems

Status: **Planned**

Purpose: learn the controls needed to keep a workflow trustworthy after a demo.

Proposed modules:

- General Data Protection Regulation (GDPR), called the Algemene verordening
  gegevensbescherming (AVG) in Dutch, accountability records and Data
  Protection Impact Assessment (DPIA) escalation;
- checking the organisation's legal role and use case under the European Union
  Artificial Intelligence Act (AI Act), with current-law updates;
- reviewing vendors that process data (processors and subprocessors), how long
  data is kept (retention), and data transfers;
- identifying plausible attacks (threat modelling) and defending against
  instructions hidden in untrusted content (prompt injection);
- user identity, permission to act (authorization), separate client
  environments (tenancy), and sensitive credentials (secrets);
- logging, monitoring, cost limits, and incident response;
- backup, restore, deletion, target restore times, and acceptable data loss
  (recovery objectives);
- change control for the artificial intelligence model, its instruction
  (prompt), and the fixed data structure (schema);
- production acceptance evidence.

Proof:

- a documented readiness pack for a low-risk fictional live workflow;
- incident and recovery exercise;
- specialist escalation record.

Boundary after completion:

- can support low-risk workflows with documented rules and oversight;
- high-risk, regulated, or especially sensitive personal data such as health
  information (special-category data) still requires qualified specialists and
  appropriate client controls.

## Course 6 — Adoption, Consulting Delivery, and Ongoing Checks

Status: **Planned**

Purpose: deliver the organizational change and recurring service around the
technology.

Proposed modules:

- deciding whether to accept a client request and setting ethical boundaries;
- proposals, assumptions, exclusions, and change control;
- facilitation and stakeholder communication;
- role-specific AI literacy;
- UAT, training, and adoption measurement;
- measuring whether the promised benefits appear;
- handover and support design;
- monthly checks that earlier behaviour still works after changes (regression),
  plus supplier, permission, and cost review;
- incident, escalation, and termination boundaries;
- a repeatable fixed-scope problem assessment, a short proof-building project,
  and a recurring check service.

Proof:

- complete fictional client-project pack;
- adoption plan and benefit review;
- step-by-step operating procedure for recurring checks.

Boundary after completion:

- controlled AI workflow implementation consultant for low-risk SME work,
  subject to real supervised delivery evidence and professional insurance,
  contracts, and specialist support.

## Optional specialization — Quality and Controlled Documents

Status: **Only after market evidence**

This specialization may fit a learner with quality or laboratory experience,
but it should not be the first commercial promise.

Topics:

- controlled-document and training relationships;
- change control, corrective and preventive action (CAPA), deviations, and
  audit expectations;
- data readiness and information that describes each document (metadata);
- validation expectations and evidence;
- vendor/platform boundaries;
- Veeva, a quality-document platform, and electronic quality management system
  (eQMS) configuration versus surrounding process problems;
- patterns for finding records that need attention across systems and checking
  that those systems agree (reconciliation);
- regulated-domain escalation.

Do not use employer documents, configurations, incidents, patient/sample data,
or internal screenshots as course or portfolio material.

## Honest title progression

| Evidence held | Honest description |
|---|---|
| Course 1 complete | Workflow analyst in training |
| Course 2 plus paid diagnostic evidence | AI workflow diagnostic practitioner |
| Course 3 plus two safe pilot outcomes | Controlled AI workflow pilot implementer |
| Courses 4–6 plus live delivery and renewal evidence | Controlled AI workflow implementation consultant |
| Repeated quality-sector demand plus domain/platform evidence | Quality workflow specialist |

Courses alone do not create consulting experience. Capability claims must
follow demonstrated work, client outcomes, and maintained controls.
