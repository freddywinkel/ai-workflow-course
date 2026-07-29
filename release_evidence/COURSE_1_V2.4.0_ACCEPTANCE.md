# Course 1 version 2.4.0 acceptance record

> **Historical record — `SUPERSEDED` for current-status purposes.** This file
> preserves the decision and evidence available for version 2.4.0. It is not
> the current Course 1 decision. Read
> [`COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md`](../COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md)
> before using any result below.

- Verified: 2026-07-28
- Reviewer: Codex, with two independent read-only acceptance passes
- Decision: PASS — released and verified at the public PWA scope

## Release identity

- Course: Controlled Artificial Intelligence (AI) Workflow Foundations
- Course version: 2.4.0
- Curriculum schema version: 2
- Practice revision: 3
- Local candidate build ID: `9c8e758aefbb`
- Local candidate content hash:
  `5e03c79d2b9f0be80f512acadcbd2f209b747cce3452e26dd1052e488070a36b`
- Verified-through date: 2026-07-28

The build ID and content hash are derived from the final bundled source and
match the public assets.

## Course and execution acceptance

- Package validator: PASS, 37/37 checks, zero failures, zero warnings.
- Course 1 clean-room acceptance:
  - Python 3.12.13: PASS, 41/41 tests.
  - Python 3.13.14: PASS, 41/41 tests.
  - Python 3.14.6: PASS, 41/41 tests.
- Every clean-room run used a fresh temporary workspace, 13 expected issues,
  two local export files, zero external actions, unchanged protected source
  files, and automatic workspace removal.
- Learner PowerShell examples: PASS, 277/277 blocks parse.
- Module 9 learner-style acceptance: PASS. UAT-01 through UAT-09 and UAT-D01
  passed in fresh workspaces; safe stops preserved the last valid workflow
  state, recorded `failed_manual`, produced no forbidden output, and performed
  zero external actions.
- Future Course 4 controlled-document prototype offline suite: PASS, 44/44
  tests in fake-provider mode with all billing and live-use flags set to `NO`.
- Synthetic data only. No real client, employer, medical, or personal data was
  used.

## Progressive Web App acceptance

- Application unit tests: PASS, 33/33.
- Production build: PASS.
- Browser smoke: PASS in desktop Chrome.
- Controlled local old-to-new update smoke: PASS. **Later** kept the old
  build; **Update now** activated the candidate; reading state, practical
  state, notes, and an unrelated cache survived; the obsolete course cache
  was removed.
- Real public version 2.3.0-to-2.4.0 update: PASS. The preserved client began
  on build `87610cbdd2b6`. **Later** left the old interface usable with its
  saved completion and note. **Update now** activated build `9c8e758aefbb`;
  the note remained, the materially revised lesson correctly reopened for
  review, the new practical self-check stayed empty, the old course cache was
  removed, and an unrelated proof cache remained. No browser dialogue
  appeared.
- Responsive viewports:
  - 320 by 568
  - 390 by 844
  - 430 by 932
  - 834 by 1112
  - 1440 by 900
  - 844 by 390 landscape
- At 320 pixels and 125% reader text, all 21 required Course 1 pages passed
  overflow and control-visibility checks.
- All 21 pages were also opened from the public deployment at 320 by 568;
  horizontal overflow remained zero, every practical panel appeared, and all
  five bottom tabs were at least 59 pixels high.
- Keyboard focus, skip link, two-way sidebar focus wrapping and restoration,
  reduced motion, forced colours, light and dark contrast, table containment,
  backup/import/reset, blocked-storage reporting, migration, offline reload,
  and offline search passed.
- The public Career tab contained six ordered course stages. Its Google Cloud
  page opened as an optional Course 4 prototype and explicitly did not affect
  Course 1 reading or practice records.
- A fresh browser cached the public build, closed its online page, went
  offline, cold-opened a new page, and returned Course 1 search results with
  no Course 4 result.

## Source audit

PASS for the Course 1 release boundary.

- Official European Commission AI literacy guidance was re-opened. Core
  lessons keep role-, context-, and risk-based literacy and escalation without
  freezing a legal conclusion or date.
- Official OpenAI model guidance was re-opened. The dated model-family note
  remains in the source register only; Course 1 makes no live provider call.
- Official Dutch statistics, Organisation for Economic Co-operation and
  Development, and Dutch security references support the market and control
  context without being treated as proof of customer demand or legal
  compliance.
- Vendor-specific model, price, interface, and legal details remain dated
  references that must be checked again before real work.

## Current-computer gate

This Windows computer has Git, Visual Studio Code, Chrome, and Edge. It
currently has only the Windows Store Python command alias, not a working
learner Python installation. Course 1 now detects that condition before any
Python exercise and gives the learner an official, checkpointed installation
route. No system-wide Python installation or PowerShell security-policy change
was performed during this audit.

This is an honest learner prerequisite, not a hidden failure: the learner can
complete the first two foundations before the software check, then follows the
installation lesson and asks Codex for a read-only folder check before
continuing.

## Safety boundary

- Course 1 runs locally with deterministic rules and an offline mock. It does
  not call Google, OpenAI, or any other live artificial intelligence provider.
- The Google Cloud capstone is visibly optional future Course 4 material. It
  is not required to finish Course 1 or become ready for Course 2.
- No paid billing was activated and no cloud action was performed during this
  release audit.
- Course 1 does not claim production readiness, legal compliance, or
  permission to run a client pilot.

## Known limitations

- Automated browser accessibility checks do not replace a future manual audit
  with multiple assistive technologies.
- Python still needs to be installed by the learner through the official
  Windows lesson before the Python-dependent exercises can run on this
  computer.

## Post-deployment fields

- Public URL:
  `https://freddywinkel.github.io/ai-workflow-course/`
- Accepted bundled-source commit:
  `ee1c2322a3cd1c2e9a9f55b57b3cd1ab9488e0ff`
- Public build ID: `9c8e758aefbb`
- Public content hash:
  `5e03c79d2b9f0be80f512acadcbd2f209b747cce3452e26dd1052e488070a36b`
- GitHub Actions release gate: PASS, run `30375498967`.
- Real preserved-client update: PASS.
- Offline cold reopen at the public scope: PASS.
- Final decision: PASS.
