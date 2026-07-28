# Certified-Beginner Foundations — Start Here

This sequence assumes you have never programmed, used a command line, built an
automation, or implemented artificial intelligence (AI). It teaches the minimum
technical literacy needed to begin the controlled workflow course.

It does not make you a production consultant. It gives you a safe practice
method and objective evidence that you can recreate the basics.

## What you need to begin Foundation 1

- A Windows computer on which you may install the course software.
- File Explorer, the Windows file-and-folder browser, and Notepad, the Windows
  plain-text editor.
- PowerShell, the command shell already included with Windows for typing and
  running text commands.
- Permission to create this deliberately fictional, or **synthetic**, practice
  root:

  ```text
  Documents\controlled-ai-course-practice
  ```

Do not use employer, client, supplier, employee, patient, or other real records.
Do not connect these exercises to a workplace system.

You do **not** need Python or Git before Foundation 1. After Foundation 2, the
Beginner Software Check first shows what is already present on this computer.
Windows Setup then installs and verifies Python, a programming language, and
Git, a version-control tool. Git is its name, not an acronym.

## Complete the lessons in order

After Foundation 2, complete
[`BEGINNER_SOFTWARE_CHECK.md`](../BEGINNER_SOFTWARE_CHECK.md) and then
[`SETUP_WINDOWS.md`](../SETUP_WINDOWS.md) before continuing with Foundation 3.
Do not skip the software check: it distinguishes software that is genuinely
installed from Windows Store command shortcuts that only offer an installation.

1. [`01_FILES_AND_TEXT.md`](01_FILES_AND_TEXT.md) — Windows folders, extensions,
   Notepad, Markdown (plain-text formatting), and JavaScript Object Notation
   (JSON), a strict structured-text format.
2. [`02_COMMAND_LINE_SURVIVAL.md`](02_COMMAND_LINE_SURVIVAL.md) — PowerShell and
   the command-line interface (CLI), a text interface for exact commands.
3. [`03_CODE_AND_PYTHON.md`](03_CODE_AND_PYTHON.md) — small Python functions
   (named reusable blocks of code), conditions, Boolean true-or-false results,
   and assertions (executable expectations that fail visibly when false).
4. [`04_WEB_APIS_AND_JSON.md`](04_WEB_APIS_AND_JSON.md) — application
   programming interfaces (APIs), which are software communication contracts;
   Hypertext Transfer Protocol (HTTP), the rules for web requests and
   responses; and JSON validation.
5. [`05_GIT_AND_SAFE_CHANGES.md`](05_GIT_AND_SAFE_CHANGES.md) — Git status (the
   current change summary), diffs (line-by-line changes), staging (selecting a
   change for the next saved checkpoint), and local commits (recorded
   checkpoints).
6. [`06_SPREADSHEETS_CSV_AND_DATA_QUALITY.md`](06_SPREADSHEETS_CSV_AND_DATA_QUALITY.md)
   — spreadsheets; comma-separated values (CSV), a plain-text table format;
   deterministic checks that give the same result for the same input and rule;
   and issue records that preserve what a check found.
7. [`07_AI_AND_CONTROLLED_WORKFLOWS.md`](07_AI_AND_CONTROLLED_WORKFLOWS.md) —
   exact rules, AI drafting, evidence, human authority, and a manual fallback,
   which is the documented safe way to continue or stop without automation.
8. [`08_SAFE_AI_ASSISTED_BUILDING.md`](08_SAFE_AI_ASSISTED_BUILDING.md) — one
   bounded AI-assisted change with acceptance evidence: observed proof that
   the stated conditions were met.
9. [`09_WORKFLOW_TOOLS_AND_DATA_STORES.md`](09_WORKFLOW_TOOLS_AND_DATA_STORES.md)
   — workflow tools; workflow state, meaning the current status and ownership
   of a work item; audit events, which record significant actions and results;
   source/state/audit separation; ownership; and minimal architecture, the
   documented arrangement of components and responsibilities.

Keep [`GLOSSARY.md`](GLOSSARY.md) open as a lookup page, but do not use it as a
substitute for explaining a lesson in your own words.

## The fixed lesson contract

**Codex** is the artificial intelligence (AI) assistant used for the read-only
checks in this course.

Every foundation uses the same four-stage practice loop:

1. **Follow along — I show you exactly how.** Start from a declared state,
   perform exact clicks or commands, read what each action does, compare the
   exact expected result, and use the narrow troubleshooting note if needed.
2. **Now recreate it yourself.** Build a meaningfully different example with
   new names or values. This tests transfer rather than copying.
3. **Ask Codex to check your work.** Codex is the AI assistant used in this
   course. Give it one explicit full practice-folder path and authorise
   read-only inspection. In a lesson that requires local validation, also give
   it the one exact project `python.exe` path printed by that lesson and
   authorise only read-only execution of the named local files. Codex must not
   access another location or change the work. Codex reports apparent sensitive
   content without repeating it; not noticing any is not proof that none
   exists. The learner supplies the synthetic-only attestation.
4. **Pass criteria.** Mark only objective checkboxes supported by observed
   files, output, and the read-only review.

If the guided example does not match its expected result, stop before the
recreation exercise. Do not rush forward to preserve a calendar.

## How to use commands safely

A **code block** is a visually separated example. **Backticks** are the `` ` ``
marks around or above and below that example; they are not command text.

- Copy only command text inside a code block, not the backticks or language
  label.
- Run one command at a time.
- Confirm the current folder before a changing command.
- Read all output before continuing.
- Do not improvise deletion, reset, or administrator commands, which run with
  elevated system rights.
- Do not improvise an **execution-policy change**, which alters PowerShell's
  rules for allowing scripts, or run a **downloaded script**, which is a file of
  commands obtained from another source.
- Treat an error as evidence to diagnose.

## Foundation completion gate

- [ ] Every lesson's guided example matches its exact expected result.
- [ ] Every recreation uses meaningfully different names or data.
- [ ] Every Codex review limited file inspection to one explicit practice
      folder. When a lesson required local validation, only its pasted project
      `python.exe` path executed the named local files, without changing them.
- [ ] Every pass criterion is supported by observed evidence.
- [ ] I can explain the difference between exact rules, AI candidates, and
      human authority.
- [ ] I can explain source input, workflow state, issue evidence, and audit
      events.
- [ ] I attest that I used only synthetic course data and intentionally added
      no **secrets**, meaning passwords, keys, tokens, or other values that
      grant access.
- [ ] I know that foundation completion is preparation for Course 1, not
      production readiness.

Repeat only the lesson whose evidence is incomplete. This is a learning gate,
not an intelligence or speed test.
