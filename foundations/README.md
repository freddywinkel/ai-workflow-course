# Beginner Foundations — Start Here Before Week 1

This foundation sequence is for a learner who has never programmed and has
never used a command-line interface (CLI). It turns the original technical
prerequisites into lessons. You are not expected to know the vocabulary before
you begin.

The twelve project weeks remain Weeks 1–12. Complete these short chapters first,
at your own pace. A complete beginner should budget roughly 8–12 hours for the
foundation sequence. It is normal for the first three project weeks to take
longer than the published 8–10 hour estimate.

## What you need before starting

- A Windows computer on which you are allowed to install software.
- A normal text editor. Visual Studio Code is recommended, but Notepad is
  sufficient for the first two chapters.
- The supplied synthetic course files.
- Willingness to stop when you do not understand a command or when observed
  output differs from the lesson.

You do **not** need prior knowledge of coding, Git, PowerShell, APIs, databases,
Docker, n8n, or AI development.

## Foundation path

Complete the chapters in this order:

1. [`01_FILES_AND_TEXT.md`](01_FILES_AND_TEXT.md) — files, folders, extensions,
   paths, and plain-text configuration.
2. [`02_COMMAND_LINE_SURVIVAL.md`](02_COMMAND_LINE_SURVIVAL.md) — how to open
   PowerShell, run one command, read output, move between folders, and stop a
   running program.
3. [`03_CODE_AND_PYTHON.md`](03_CODE_AND_PYTHON.md) — what code is, how Python
   executes it, and how to read small functions without pretending to
   understand generated code.
4. [`04_WEB_APIS_AND_JSON.md`](04_WEB_APIS_AND_JSON.md) — browser versus server,
   HTTP, APIs, requests, responses, and JSON.
5. [`05_GIT_AND_SAFE_CHANGES.md`](05_GIT_AND_SAFE_CHANGES.md) — repository,
   status, diff, commit, and recovery without destructive commands.
6. [`06_AI_AND_DOCUMENT_WORKFLOWS.md`](06_AI_AND_DOCUMENT_WORKFLOWS.md) — models,
   prompts, hallucinations, structured output, parsing, OCR, retrieval, and
   human approval.
7. [`07_SAFE_VIBE_CODING.md`](07_SAFE_VIBE_CODING.md) — a safe way to work with
   an AI coding assistant one small, testable change at a time.
8. [`08_N8N_DOCKER_AND_DATABASES.md`](08_N8N_DOCKER_AND_DATABASES.md) — the
   course's main tools and how data moves between them.

Keep [`GLOSSARY.md`](GLOSSARY.md) open while studying. It defines the course
terms in plain language.

## How to study each chapter

For each chapter:

1. Read the outcome and explanation.
2. Perform the small exercise yourself.
3. Compare the observed result with the stated result.
4. Explain what happened in your own words.
5. Complete the chapter check before moving on.

Do not merely paste a command and accept a green message. The learning goal is
to know:

- what the command was supposed to change;
- which folder or file it affected;
- how you checked the result;
- how to stop or recover if it behaved differently.

## Foundation gate

You are ready for Week 1 when all of these are true:

- [ ] I can tell the difference between a folder, a file, a file extension, and
  a full path.
- [ ] I can open PowerShell and identify the prompt, command, output, and error.
- [ ] I can use `Get-Location`, `Get-ChildItem`, and `Set-Location`.
- [ ] I know that code fences, prompts, and example output are not part of a
  command.
- [ ] I can create a plain-text file and recognise Markdown, JSON, YAML, and
  `.env` as different text formats.
- [ ] I can describe a Python variable, function, condition, list, and
  dictionary in simple words.
- [ ] I can explain request, response, endpoint, status code, and JSON.
- [ ] I can run `git status` and read `git diff` without changing files.
- [ ] I can explain why `.env` must not be committed.
- [ ] I can explain that Structured Outputs constrain a response's shape, not
  its factual truth.
- [ ] I can explain why source evidence and human approval remain necessary.
- [ ] I know how to ask an AI coding assistant for one small change, a plain
  explanation, and a test.

If one item is not true, repeat only the relevant chapter. This is a learning
checkpoint, not an intelligence test.

## Beginner pace

The stated 8–10 hours per project week is a target for someone already
comfortable with the tools. A literal beginner may need:

- 10–14 hours for Weeks 1–2;
- 12–16 hours for Weeks 3–5;
- 8–12 hours after the tools become familiar.

You may split any course week across two calendar weeks. Keep the technical
sequence and gates; do not rush through a failed gate to preserve a calendar.

