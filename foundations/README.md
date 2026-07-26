# Beginner Foundations — Start Here

This sequence is for a learner who has never programmed or implemented a
business workflow. It teaches enough technical literacy to build and supervise
small, controlled workflow demonstrations for Dutch SMEs. It does not make you
a production consultant by itself.

The foundations come before the project modules. A complete beginner should
budget roughly 14–20 focused hours and repeat any exercise that is not yet
explainable in their own words. Use only the supplied fictional data.

## What you need

- A Windows computer on which you may install software.
- A text editor. Visual Studio Code is recommended.
- A spreadsheet program that can import CSV files.
- The supplied synthetic course files.
- Permission to stop whenever a command or result is unclear.

You do **not** need previous experience with coding, Git, PowerShell, APIs,
spreadsheets, databases, workflow tools, or AI development.

## Foundation path

Complete the chapters in order:

1. [`01_FILES_AND_TEXT.md`](01_FILES_AND_TEXT.md) — files, folders, extensions,
   paths, and plain-text configuration.
2. [`02_COMMAND_LINE_SURVIVAL.md`](02_COMMAND_LINE_SURVIVAL.md) — PowerShell,
   commands, output, errors, folders, and stopping a running program.
3. [`03_CODE_AND_PYTHON.md`](03_CODE_AND_PYTHON.md) — code, Python, small
   functions, tests, and unexplained generated code.
4. [`04_WEB_APIS_AND_JSON.md`](04_WEB_APIS_AND_JSON.md) — clients, servers,
   HTTP, APIs, requests, responses, and JSON.
5. [`05_GIT_AND_SAFE_CHANGES.md`](05_GIT_AND_SAFE_CHANGES.md) — status, diffs,
   commits, recovery, and protecting secrets.
6. [`06_SPREADSHEETS_CSV_AND_DATA_QUALITY.md`](06_SPREADSHEETS_CSV_AND_DATA_QUALITY.md)
   — tabular data, CSV import, data types, deterministic checks, and issue
   measurement.
7. [`07_AI_AND_CONTROLLED_WORKFLOWS.md`](07_AI_AND_CONTROLLED_WORKFLOWS.md) —
   appropriate AI tasks, evidence, uncertainty, human decisions, and safe
   workflow boundaries.
8. [`08_SAFE_AI_ASSISTED_BUILDING.md`](08_SAFE_AI_ASSISTED_BUILDING.md) — using
   an AI assistant while keeping changes understandable, reviewable, and
   tested.
9. [`09_WORKFLOW_TOOLS_AND_DATA_STORES.md`](09_WORKFLOW_TOOLS_AND_DATA_STORES.md)
   — choosing an orchestrator and storage approach without confusing a tool
   with the business process.

Keep [`GLOSSARY.md`](GLOSSARY.md) open while studying.

## How to study each chapter

For every chapter:

1. Read the outcome.
2. Perform the exercise yourself.
3. Compare the observed result with the stated result.
4. Explain what happened in ordinary language.
5. Complete the chapter check.
6. Save only synthetic practice artifacts.

A command, formula, or AI answer is not evidence merely because it looks
professional. Know:

- what should enter;
- what should happen;
- what should leave;
- what may change;
- what can fail;
- how you checked the result;
- how work continues safely if the tool fails.

## Foundation gate

You are ready for the project modules when all of these are true:

- [ ] I can distinguish a folder, file, extension, full path, and relative path.
- [ ] I can identify a PowerShell prompt, command, output, and error.
- [ ] I can use `Get-Location`, `Get-ChildItem`, and `Set-Location`.
- [ ] I know code fences, prompts, and example output are not command text.
- [ ] I can recognise Markdown, JSON, YAML, CSV, and `.env` files.
- [ ] I can describe a Python variable, function, condition, list, dictionary,
      and test.
- [ ] I can explain request, response, endpoint, status code, and JSON.
- [ ] I can run `git status` and inspect `git diff` without changing files.
- [ ] I know why `.env` and business data must not enter Git or AI chat.
- [ ] I can explain row, column, header, data type, unique ID, blank value, and
      data-quality rule.
- [ ] I can import CSV deliberately and protect the untouched source export.
- [ ] I can distinguish a deterministic rule from an AI interpretation.
- [ ] I can explain why schema-valid or fluent output can still be wrong.
- [ ] I can identify where a human must review, reject, correct, or escalate.
- [ ] I can request one small AI-assisted change, review its diff, and test it.
- [ ] I can describe a manual fallback for a failed workflow.

If one item is not true, repeat only the relevant chapter. This is a learning
checkpoint, not a speed test.

## Safe learning boundary

Do not use employer, customer, patient, employee, supplier, or other real
records in these exercises. Do not connect the demonstrations to workplace
systems. Do not automate external sending, payment, deletion, approval, or
other consequential actions.

The foundation goal is a controlled synthetic demonstration that you can
explain and test—not unsupervised production automation.
