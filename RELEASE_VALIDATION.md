# Release Validation — Course 2.2 and Progressive Web App (PWA)

## Release rule

Do not publish merely because the build succeeds. A release passes only when
course structure, content, learner state, PWA behavior, responsive layout, and
installed-update behavior have been checked.

## 1. Package structure

- [ ] `curriculum.json` parses.
- [ ] One career course is marked current.
- [ ] Nine foundation and nine module progress lessons exist.
- [ ] All stable IDs are unique.
- [ ] All revision dates are valid.
- [ ] Every configured source exists exactly once.
- [ ] Every module contains the required headings in order.
- [ ] Every foundation and module contains one ordered follow-along,
      recreation, read-only Codex check, and pass-criteria sequence.
- [ ] Every Codex check is limited to one pasted full folder path, explicitly
      forbids changes, and checks for secrets or real data.
- [ ] Required onboarding abbreviations and unfamiliar product names are
      explained before use.
- [ ] Internal links resolve outside ignored future-course archives.
- [ ] JSON schemas pass meta-validation.
- [ ] `stack-manifest.yaml` parses.

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
- [ ] Future courses are visibly planned, not secretly counted as current.
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
- [ ] Built JavaScript passes syntax checks.
- [ ] Manifest ID, scope, and start URL remain `/ai-workflow-course/`.
- [ ] Service-worker cache prefix remains compatible.
- [ ] No generated placeholder remains.
- [ ] No external font or image is required.

## 5. Information architecture

Verify:

- [ ] Overview tab explains who the course is for and its boundary.
- [ ] Course navigation follows curriculum metadata.
- [ ] Career tab shows Courses 1–6 and optional specialization.
- [ ] Only Course 1 has progress controls.
- [ ] Search includes current lessons and references.
- [ ] Settings and progress backup work.
- [ ] Previous/next follows explicit reading order.
- [ ] Resume opens the next incomplete current lesson.
- [ ] No supplier-specific home copy remains.

## 6. Learner-state migration

Create both a schema-v1 state and a Course 2.1 state before loading Course 2.2.

- [ ] Theme and font size survive.
- [ ] Notes survive or are retained for export.
- [ ] Equivalent retained foundations preserve completion.
- [ ] Course 2.2 revision dates reopen materially rewritten lessons
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
- [ ] notes and completion save offline.
- [ ] search works offline.
- [ ] app does not claim the capstone itself runs offline.
- [ ] unavailable external source links fail normally without damaging the app.

## 9. Installed-client update

Use an installed or controlled old Course 2.1 client:

1. load and record old build/version;
2. save representative progress and notes;
3. publish or serve Course 2.2 at the same scope;
4. foreground or focus the old client;
5. verify the update prompt appears;
6. choose **Later** and confirm the old version remains usable;
7. choose **Update now**;
8. confirm the new service worker activates;
9. verify the Course 2.2 Overview, practice loop, and Career tab;
10. verify state migration;
11. cold reload and reopen the installed PWA.

- [ ] new precache resources were fetched with `cache: "reload"`;
- [ ] no broad cache deletion occurred;
- [ ] local state was not erased;
- [ ] Course 2.2 is still present after cold reopen.

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
