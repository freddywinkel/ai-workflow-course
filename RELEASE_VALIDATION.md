# Release Validation — Course 2.3 and Progressive Web App (PWA)

## Release rule

Do not publish merely because the build succeeds. A release passes only when
course structure, content, learner state, PWA behavior, responsive layout, and
installed-update behavior have been checked.

## 1. Package structure

- [ ] `curriculum.json` parses.
- [ ] One career course is marked current.
- [ ] Nine foundation and nine module progress lessons exist.
- [ ] Course 1 still has exactly 18 core lessons and its established
      `learningSequenceIds` are unchanged.
- [ ] The optional `course-4-capstone` group is non-core and contains exactly
      the overview plus Labs 0–9.
- [ ] Every capstone page has the Course 4 `courseId` and no Course 4 page
      appears in the Course 1 learning sequence.
- [ ] All stable IDs are unique.
- [ ] All revision dates are valid.
- [ ] Every configured source exists exactly once.
- [ ] Every module contains the required headings in order.
- [ ] Every foundation and module contains one ordered follow-along,
      recreation, read-only Codex check, and pass-criteria sequence.
- [ ] Every Course 4 lab contains the same ordered practice sequence.
- [ ] Every Codex check is limited to one pasted full folder path, explicitly
      forbids changes, and checks for secrets or real data.
- [ ] Required onboarding abbreviations and unfamiliar product names are
      explained before use.
- [ ] Internal links resolve outside ignored future-course archives.
- [ ] JavaScript Object Notation (JSON) schemas pass meta-validation.
- [ ] `stack-manifest.yaml` parses.
- [ ] The controlled-intake implementation package contains its application,
      tests, deployment, live-verification, and teardown scripts.

Run:

```powershell
python tools\validate_package.py
```

Expected: `PASS`.

## 2. Synthetic data

- [ ] `work_items.csv` has 15 rows and 12 expected columns.
- [ ] `expected_issues.csv` has 13 unique issue keys.
- [ ] Rules R001–R011 reproduce all expected issue keys.
- [ ] Assessment date is `2026-07-26`.
- [ ] No real person, employer, customer, or transaction appears.
- [ ] Archived supplier data is excluded from Course 1 validation and PWA.
- [ ] The Course 4 capstone uses synthetic documents only.
- [ ] No real client, employer, medical, or personal data is present.
- [ ] The €60 ceiling, no-paid-billing boundary, file-content deletion, and
      26 October 2026 deadline gate are explicit.

## 2A. Recorded Course 4 implementation evidence

This dated reference evidence is complete. It does not replace the PWA and
installed-client release checks later in this file.
It proves the deployed Google path immediately before teardown. The final
offline audit then added stricter immutable configuration, semantic
action-evidence checks, and repeatable Identity and Access Management (IAM)
plus unauthenticated-access checks. Those fail-closed changes were not
redeployed after the dedicated project entered `DELETE_REQUESTED`.
The redacted records are
[`cloud_deployment_validation.json`](future_courses/course_04_controlled_document_ai/controlled_document_intake_demo/evidence/cloud_deployment_validation.json),
[`live_validation.json`](future_courses/course_04_controlled_document_ai/controlled_document_intake_demo/evidence/live_validation.json),
and
[`teardown_validation.json`](future_courses/course_04_controlled_document_ai/controlled_document_intake_demo/evidence/teardown_validation.json).

- [x] `cloud_deployment_validation.json` records `PASS`.
- [x] Cloud Run was private through Identity and Access Management, ready in
      `europe-west4`, minimum zero, maximum one, and concurrency one.
- [x] The health endpoint was `/api/health`; no `/healthz` claim remains.
- [x] Document AI and Vertex AI were both `eu`, using
      `gemini-3.5-flash-lite`.
- [x] Gemini selected candidate identifiers and one allowed action type; fixed
      application code rendered the exact summary and action wording.
- [x] `live_validation.json` records `PASS` using frozen synthetic files only.
- [x] C001 and C004 were `pending_approval`, with 14 fields and 14 evidence
      links each.
- [x] C008 was `needs_review` with `TOTAL_DISCREPANCY`.
- [x] C012 was `needs_review` with
      `UNTRUSTED_INSTRUCTION_DETECTED`.
- [x] Corrupt input stopped with `PARSER_CORRUPT_FILE`; an unknown hash stopped
      with `SYNTHETIC_ALLOWLIST_REJECTED`.
- [x] Approved C001 comma-separated values and JavaScript Object Notation
      exports are represented by hashes, not document content.
- [x] Every live case reports temporary-file deletion true and raw persistence
      false.
- [x] The account remained an unactivated Free Trial and **Activate** remained
      visible.
- [x] The displayed cost was €0 at the recorded checks, explicitly labelled as
      possibly delayed rather than final.
- [x] The ordinary alerts-only budget was deleted and verified through the
      public Cloud Billing Budget application programming interface.
- [x] The two Preview spend caps were deleted and verified absent through the
      Billing user interface; the final check showed zero course budget rows.
- [x] `teardown_validation.json` records `PASS` and project state
      `DELETE_REQUESTED`.
- [x] All three evidence files exclude document text, model output,
      credentials and Billing account identifiers.
- [x] The post-teardown offline suite proves fake mode remains usable after the
      live deadline, Google mode rejects deadline/model/token/placeholder
      changes, actions cannot cite unrelated field types, and the repeatable
      live verifier checks public IAM members plus an unauthenticated
      `401`/`403`.

## 3. Content consistency

- [ ] README, Overview, Architecture, Capstone, Rubric, modules, schemas, and
      practice-data README describe the same project.
- [ ] Course 1 boundary is prominent.
- [ ] No lesson claims production readiness or legal compliance.
- [ ] `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, and `DO NOT CONTINUE` are the
      only Course 1 final decisions and each remains a valid evidence-backed
      result.
- [ ] Course 1 never authorizes a client pilot; discovery belongs in Course 2
      and supervised low-risk pilot delivery belongs in Course 3.
- [ ] Model IDs are configuration, not durable dependencies.
- [ ] Live AI is optional.
- [ ] Future courses are visibly planned. The Course 4 capstone is labelled an
      optional advanced prototype, not a complete course or production proof.
- [ ] Vague practice instructions were not reintroduced.
- [ ] Foundation 1 includes literal File Explorer and Notepad actions, expected
      files, a different recreation, and a read-only inspection prompt.
- [ ] Source register was opened and checked on the release date.

## 4. PWA build and tests

From `app`:

```powershell
$env:BASE_PATH="/ai-workflow-course/"
node --test tests\*.test.mjs
node scripts\build.mjs
```

- [ ] Bundle schema is 2.
- [ ] Curriculum metadata is inside the content hash.
- [ ] Stable lesson IDs and revisions are present.
- [ ] Optional document-level `courseId` metadata survives the build.
- [ ] Course 4 pages remain non-core and Course 1 core progress remains 18.
- [ ] Built JavaScript passes syntax checks.
- [ ] The complete capstone offline suite passes and is a required GitHub Pages
      deployment job without cloud credentials or live calls.
- [ ] Manifest ID, scope, and start URL remain `/ai-workflow-course/`.
- [ ] Service-worker cache prefix remains compatible.
- [ ] No generated placeholder remains.
- [ ] No external font or image is required.

## 5. Information architecture

Verify:

- [ ] Overview tab explains who the course is for and its boundary.
- [ ] Course navigation follows curriculum metadata.
- [ ] Career tab shows Courses 1–6, the optional specialization, and a distinct
      Course 4 prototype status.
- [ ] **Open the optional capstone** opens the Course 4 overview.
- [ ] Course 4 page marks are visibly separate and never change Course 1's
      18-lesson progress or Resume.
- [ ] Search includes current lessons, the optional capstone, and references.
- [ ] Settings and progress backup work.
- [ ] Previous/next follows explicit reading order.
- [ ] Resume opens the next incomplete current lesson.
- [ ] No supplier-specific home copy remains.

## 6. Learner-state migration

Create both a schema-v1 state and a Course 2.2 state before loading Course 2.3.

- [ ] Theme and font size survive.
- [ ] Notes survive or are retained for export.
- [ ] Equivalent retained foundations preserve completion.
- [ ] Course 2.3 revision dates reopen materially rewritten lessons
      for review without changing stable lesson IDs.
- [ ] unknown old IDs are not misapplied.
- [ ] old JSON backup import works.
- [ ] reset requires confirmation.
- [ ] a migration notice explains any invalidated completion.

## 7. Accessibility and responsive behavior

Test at:

- 320×568;
- 390×844;
- 430×932;
- 834×1112;
- desktop 1440×900.

For each relevant size:

- [ ] no horizontal page overflow;
- [ ] five bottom tabs remain readable and tappable;
- [ ] content is not hidden behind the bottom bar or safe area;
- [ ] sidebar opens, traps focus, closes, and restores focus;
- [ ] skip link works;
- [ ] headings receive logical focus after navigation;
- [ ] 125% reader text remains usable;
- [ ] dark and light themes have sufficient contrast;
- [ ] tables scroll inside their wrapper;
- [ ] reduced motion is respected;
- [ ] landscape does not make the primary controls unreachable.

## 8. Offline behavior

- [ ] First visit succeeds online.
- [ ] Course bundle and Career tab load offline.
- [ ] Optional Course 4 lesson pages can be read offline after the app has
      cached the release.
- [ ] notes and completion save offline.
- [ ] search works offline.
- [ ] app does not claim the capstone itself runs offline.
- [ ] unavailable external source links fail normally without damaging the app.

## 9. Installed-client update

Use an installed or controlled old Course 2.2 client:

1. load and record old build/version;
2. save representative progress and notes;
3. publish or serve Course 2.3 at the same scope;
4. foreground or focus the old client;
5. verify the update prompt appears;
6. choose **Later** and confirm the old version remains usable;
7. choose **Update now**;
8. confirm the new service worker activates;
9. verify the Course 2.3 Overview, practice loop, Course 4 link, and Career tab;
10. verify state migration;
11. cold reload and reopen the installed PWA.

- [ ] new precache resources were fetched with `cache: "reload"`;
- [ ] no broad cache deletion occurred;
- [ ] local state was not erased;
- [ ] Course 2.3 is still present after cold reopen.

## 10. Final release record

Record:

- course version;
- curriculum version;
- build ID;
- content hash;
- verified-through date;
- source audit result;
- package validator result;
- PWA test result;
- viewports and browsers tested;
- offline result;
- installed-update result;
- known limitations;
- release decision and reviewer.

If installed-update verification cannot be performed, label the release
candidate `UNVERIFIED` for deployment even when local tests pass.
