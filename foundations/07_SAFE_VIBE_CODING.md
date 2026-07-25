# Foundation 7 — Safe Vibe Coding

## Outcome

You can use an AI coding assistant as a tutor and pair programmer while keeping
changes small, understandable, reviewable, and tested.

## The beginner-safe loop

Use this loop for every change:

1. **State one outcome.** Describe one behaviour, not an entire platform.
2. **Ask for inspection first.** Let the assistant read the relevant files and
   describe the current behaviour.
3. **Request a small plan.** Require exact files, risks, and tests.
4. **Limit scope.** One function, route, schema, or workflow branch at a time.
5. **Require teaching.** Ask for a plain-language explanation of inputs,
   outputs, side effects, and failure paths.
6. **Review the diff.** Never accept “done” without seeing what changed.
7. **Run tests.** Include happy, failure, boundary, and safety cases.
8. **Observe the real result.** A passing unit test does not prove n8n, storage,
   or the browser behaves correctly.
9. **Record evidence.** Save command, output, versions, and limitations.
10. **Commit only the understood unit.**

If the change is too large to explain, ask the assistant to split it.

## Copy-paste build prompt

```text
You are helping a literal beginner. Work on only this outcome:
[one observable outcome]

Before editing:
1. Inspect the relevant files.
2. Explain the current behaviour in plain language.
3. List the smallest files you need to change.
4. Identify anything that could delete data, expose a secret, call an external
   service, or alter an approved action.

When editing:
- Make one small change at a time.
- Preserve unrelated work.
- Do not use real data or secrets.
- Do not run destructive commands.
- Add tests for success, failure, boundary, duplicate, and unsafe input where
  relevant.

After editing:
1. Show the exact changed files.
2. Explain every new function's inputs, outputs, side effects, and failures.
3. Run the narrow tests, then the relevant broader tests.
4. Report observed results and anything not verified.
5. Give me one manual check I can perform myself.

Stop and ask before any deletion, history rewrite, public deployment, paid API
use beyond the stated limit, or action outside this project.
```

## Copy-paste explanation prompt

```text
Explain this code to someone with no coding background.

For each block, tell me:
- what enters;
- what happens;
- what leaves;
- what can change outside the function;
- what can fail;
- which course safety rule it enforces;
- which test proves it.

Define each new term once. Do not rewrite the code yet. If the code is too large
to explain safely, identify a smaller unit to inspect first.

[paste only non-secret code]
```

## Copy-paste debugging prompt

```text
Diagnose this without changing files yet.

Goal:
Last successful step:
Current folder from Get-Location:
Exact command:
Complete redacted output/error:
Expected result:
Recent change:

Please:
1. Separate facts from hypotheses.
2. Give the most likely cause and one read-only check.
3. Explain the check before I run it.
4. Do not suggest deletion, reset, reinstall, execution-policy changes, or
   credential exposure as a first step.
5. After the check, propose the smallest reversible fix and its verification.
```

## Copy-paste test-review prompt

```text
Review these tests against the stated requirement. Do not edit yet.

Requirement:
[paste one requirement]

Tests/code:
[paste non-secret excerpt]

List:
- behaviour actually proved;
- behaviour only assumed;
- missing failure, boundary, duplicate, timeout, and adversarial cases;
- tests that could pass for the wrong reason;
- the smallest extra tests needed.
```

## What never to paste into an AI chat

- API keys, passwords, tokens, cookies, or private keys;
- `.env` contents;
- real supplier/client documents;
- personal or special-category data;
- database dumps;
- unredacted logs or workflow exports;
- confidential repository contents unless the approved tool and data controls
  explicitly cover them.

Use synthetic examples. Replace identifiers with clear placeholders.

## Warning signs in an AI answer

Pause when the assistant:

- claims success without running a relevant test;
- silently changes multiple unrelated files;
- hard-codes a current model name, credential, or machine path;
- turns off validation, TLS, authentication, RLS, or a kill switch;
- catches every exception and continues;
- logs full documents or secrets;
- says a schema guarantees truth;
- retries every error;
- uses destructive commands as routine cleanup;
- proposes public exposure for a local course demo;
- adds automatic send, payment, deletion, or approval;
- cannot explain how to reproduce or reverse the change.

## Your responsibility

Using AI assistance is allowed throughout this course. Your proof is not that
you typed every line. Your proof is that you can:

- explain the resulting behaviour;
- reproduce it from the repository;
- show its tests and observed output;
- identify its limits;
- stop it safely;
- avoid claiming checks you did not perform.

## Chapter check

Use the build prompt to create one tiny function and test in the practice
repository. Then explain it without asking the assistant. If you cannot, ask
for a smaller change or repeat the line-by-line explanation.

