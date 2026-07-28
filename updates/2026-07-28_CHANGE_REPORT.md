# Version 2.2 Corrective Product Audit

Audit date: **2026-07-28**

Course: **Controlled Artificial Intelligence (AI) Workflow Foundations**

Audit decision: **REVISE AND RELEASE AFTER FULL VALIDATION**

## Why this audit was needed

Version 2.1 had the right broad career direction and a useful beginner practice
pattern, but the product still contained contradictions that could mislead a
new learner:

- the setup, foundations, and modules did not consistently build one
  reproducible project;
- required artifacts were named in the final project but not always taught and
  created in the modules;
- final decision language could be mistaken for permission to run a client
  pilot;
- required and optional software were not separated clearly enough;
- the app's Resume and previous/next controls could skip setup gates;
- rapidly leaving a note could lose the newest text;
- some release dependencies could change without review.

Those are product defects, not learner failures.

## Original and replacement course contracts

| Area | Earlier contract | Version 2.2 replacement |
|---|---|---|
| Learner project | Exercises could create separate module folders without a single cumulative history. | Foundations rehearse safely; Windows Setup creates one local Git repository named `operations-exception-assistant`; Modules 1–9 extend that repository. |
| Evidence | The capstone expected artifacts that were not all produced by a named lesson. | Every required artifact is introduced, created, checked, and recorded by a named module. |
| Module checkpoint | Git use varied between lessons. | Each module has one pass-only checkpoint and an `evidence\module-NN` folder. |
| Course 1 decision | Pilot-oriented terms could imply market or client readiness. | The only outcomes are `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, and `DO NOT CONTINUE`. None authorises a client pilot. |
| External action control | More than one safety-setting name appeared. | The single setting is `EXTERNAL_ACTIONS_ENABLED=false`. |
| Setup | Provider packages and a visual workflow tool could appear required. | Visual Studio Code, Git, Python, and the pinned small Python test set form the core setup. Node.js, n8n, and a live OpenAI lab are optional. |
| Software currency | A beginner could encounter a mutating maintainer prompt while trying to check software. | A separate read-only beginner software check reports what is present and sends the learner to the manual setup guide. |
| Learning order | Group order could send the learner from Foundation 2 directly to Foundation 3. | The actionable sequence is Foundation 2 → read-only software check → Windows Setup → Foundation 3. |
| App notes | The entire state write was delayed, so immediate navigation could lose the newest note. | The note value and document identity are captured immediately; only the storage write is delayed and is flushed at navigation and lifecycle boundaries. |
| App updates | Build-generator changes did not affect the update identity. | Curriculum, source, static assets, and the build generator contribute to the immutable build identity. |

## Affected material

The corrective revision affects the course overview, readiness and setup path,
Foundations 3 and 7, all nine implementation modules, the capstone
specification, assessment rubric, architecture and contracts, selected
worksheets, career boundary, software and source records, release workflow,
validator, tests, and progressive web app (PWA).

Foundations 1 and 2 retain their Version 2.1 revision because their learner
meaning did not change. Materially changed learner pages use revision
`2026-07-28`, so an existing learner is asked to review only affected work.

## Source and sustainability audit

Primary or official sources were checked on the audit date for:

- Dutch small and medium-sized enterprise (SME) adoption context and
  automation pressure;
- Dutch privacy accountability and European Union Artificial Intelligence Act
  (AI Act) literacy and oversight;
- durable Artificial Intelligence Risk Management Framework concepts;
- current Python, Git, Visual Studio Code, Node.js, pytest, and JavaScript
  Object Notation (JSON) Schema guidance;
- current OpenAI model and Application Programming Interface (API) guidance;
- current n8n installation and workflow documentation;
- current GitHub Pages release actions.

The exact links and course use are recorded in
[`../SOURCE_REGISTER.md`](../SOURCE_REGISTER.md). Vendor interfaces, model
names, pricing, and low-code features remain replaceable details. The durable
course assessment is based on workflow observation, explicit inputs and
outputs, deterministic rules, tests, failure handling, human authority,
evidence, ownership, and a manual fallback.

This makes the course a foundation for later consulting work rather than
training for one tool that may be automated away.

## Migration and compatibility

- Stable lesson identifiers are retained.
- Only materially changed lessons receive a new revision date.
- Existing notes remain local and are retained.
- Existing completion for unchanged lessons remains valid.
- Rewritten lessons reopen for review.
- The app keeps the same manifest identity, start address, scope, and
  compatible cache family.
- The old client remains usable when the learner chooses **Later** and changes
  only after **Update now**.

## Required verification before publication

The release candidate must pass all of the following after this report is
saved:

1. deterministic package validation with zero failures and zero warnings;
2. all PWA regression tests;
3. an immutable build at the production base path;
4. manual learner-flow checks, including the inserted setup gates;
5. responsive checks at the release viewports without page overflow;
6. an online-to-offline course, Career, notes, progress, and search check;
7. a controlled Version 2.1 → Version 2.2 update with **Later**, **Update
   now**, completion migration, and note retention;
8. a successful GitHub Pages deployment and direct inspection of live
   `version.json`, manifest, course bundle, and service worker.

The executable checklist is
[`../RELEASE_VALIDATION.md`](../RELEASE_VALIDATION.md). The generated
deterministic result is
[`../VALIDATION_REPORT.md`](../VALIDATION_REPORT.md).

## Known limits

- Course 1 produces a synthetic portfolio demonstration, not production
  readiness, legal compliance, a professional certification, or proof of
  customer demand.
- It does not authorise real employer, patient, or client data.
- It does not teach client discovery or a supervised client pilot; those are
  separate later courses.
- Browser and operating-system installation wording can change and must be
  rechecked during maintenance.
- Static GitHub Pages hosting cannot add every security header available to a
  server-controlled deployment.

## Next review

Review no later than **2026-10-20**, or earlier after a material legal,
official-source, dependency, platform, or security change.

Reopen the course sooner if a beginner cannot reproduce the project from a
clean Windows setup or if an old installed client cannot update without losing
local state.
