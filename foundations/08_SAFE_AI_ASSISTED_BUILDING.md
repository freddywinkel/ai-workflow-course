# Foundation 8 — Safe AI-Assisted Building

## Outcome

You can use an AI coding assistant as a tutor and implementation partner while
keeping each change bounded, understandable, reviewable, and supported by
observed tests.

AI can accelerate implementation. It does not transfer responsibility for the
result away from the person delivering the workflow.

## Prepare before asking for code

For one requested change, write:

- the observable outcome;
- the allowed files and data;
- what must not change;
- acceptance tests;
- possible side effects;
- how to recover;
- what requires a pause or approval.

Classify the input first. Use fictional examples in this course. Never include
credentials, workplace records, personal data, confidential configurations, or
unredacted logs merely because an assistant asks for “more context.”

## The inspection-to-evidence loop

Use this loop for every material change:

1. **Inspect.** Read the relevant files and current behaviour.
2. **Define.** State one observable outcome and its exclusions.
3. **Plan.** Name the smallest files, risks, and tests.
4. **Patch.** Make one reversible unit of change.
5. **Explain.** Identify inputs, outputs, side effects, and failure paths.
6. **Review.** Inspect the exact diff and unexpected files.
7. **Test.** Run success, failure, boundary, and safety cases.
8. **Observe.** Check the real spreadsheet, workflow, API, or interface.
9. **Record.** Save the command/procedure, result, version, and limitation.
10. **Commit.** Record only the understood unit.

Passing tests are evidence for the behaviour they actually exercise. They are
not proof that every requirement, connector, permission, or user experience is
correct.

If a change is too large to explain, split it before running it.

## A copy-paste implementation prompt

```text
Help me implement one bounded outcome:
[one observable outcome]

Allowed synthetic input:
[file or example]

Acceptance criteria:
- [observable result]
- [failure result]
- [unchanged behaviour]

Before editing:
1. Inspect the relevant files and explain current behaviour.
2. Name the smallest files that need to change.
3. Identify data exposure, external calls, side effects, and recovery.
4. Stop if the request needs a secret, real business data, deletion, public
   deployment, paid use, or a consequential external action.

While editing:
- preserve unrelated work;
- make one small change;
- do not weaken validation, access control, logging, review, or fallback;
- use no real data or credentials;
- add tests for success, failure, boundary, malformed input, and duplicates
  where relevant.

After editing:
1. List every changed file.
2. Explain inputs, outputs, side effects, and failure routes.
3. Show the diff.
4. Run narrow tests and then relevant broader tests.
5. Report observed results separately from unverified claims.
6. Give me one manual check I can perform.
```

## A copy-paste explanation prompt

```text
Explain this non-secret code or configuration to a beginner. Do not edit it.

For each block, state:
- what enters;
- what happens;
- what leaves;
- what can change outside the block;
- what can fail;
- which business or safety rule it implements;
- which test proves that behaviour.

Define each new term once. Identify anything you cannot establish from the
provided evidence. If the unit is too large, select a smaller unit first.
```

## A copy-paste diagnosis prompt

```text
Diagnose this without changing files yet.

Goal:
Last successful step:
Current folder from Get-Location:
Exact command or user action:
Complete redacted output/error:
Expected result:
Recent change:

Please:
1. Separate observed facts from hypotheses.
2. Propose one read-only check for the most likely cause.
3. Explain the check before I run it.
4. Do not begin with deletion, reset, reinstall, security disablement, or
   credential exposure.
5. After the evidence, propose the smallest reversible fix and verification.
```

## A copy-paste test review

```text
Review these tests against one requirement. Do not edit yet.

Requirement:
[one falsifiable requirement]

Tests and relevant code:
[non-secret excerpt]

List:
- behaviour actually proved;
- behaviour assumed but not proved;
- missing failure, boundary, duplicate, timeout, and unsafe-input cases;
- tests that could pass for the wrong reason;
- the smallest additional tests required.
```

## Treat generated dependencies and commands as proposals

An assistant may invent a package name, use outdated syntax, select an
inappropriate licence, or suggest a destructive command. Before adding a
dependency:

- confirm it exists in its official source;
- confirm maintenance and licence;
- check whether the existing stack already solves the problem;
- pin or record the selected version;
- review what data or network access it receives;
- test removal or replacement where practical.

Before running an unfamiliar command, identify its current folder, exact target,
side effects, and recovery. Do not run downloaded text directly or weaken
security settings just to make a demo pass.

## Never supply these to an unapproved AI service

- API keys, passwords, tokens, cookies, certificates, or private keys;
- `.env` contents;
- employer, client, supplier, employee, or patient records;
- database dumps or production exports;
- confidential prompts, configurations, contracts, or source code;
- unredacted logs, screenshots, or workflow exports;
- personal or special-category data.

Replacing a name with initials does not necessarily make data anonymous. Use
the supplied synthetic practice data.

## Warning signs

Pause when an assistant:

- claims success without a relevant observed test;
- changes multiple unrelated files;
- silently changes the requirement;
- invents citations, package details, or current product behaviour;
- hard-codes credentials, model names, prices, or machine-specific paths;
- disables validation, authentication, access control, TLS, audit, or a kill
  switch;
- catches every error and continues;
- logs full inputs or secrets;
- retries all failures;
- adds automatic external sending, payment, deletion, or approval;
- treats a schema as proof of truth;
- cannot explain reproduction, rollback, or manual fallback.

## Evidence before consulting claims

Keep a small claim/evidence table:

| Claim | Required evidence | Observed result | Limitation |
|---|---|---|---|
| detects overdue items | fixed test rows plus expected issue IDs | | |
| does not modify the source | file comparison or read-only design check | | |
| handles missing columns | failure test and reason code | | |
| reviewer can reject | observed review-path test | | |

Say “not verified” when evidence is missing. A consultant’s credibility depends
more on accurate boundaries than on a flawless demonstration.

## Practice

Ask an assistant to create one small function that checks whether `title` is
blank in a fictional work-item dictionary and returns reason code `R001`.
Require:

- one valid case;
- one missing-title case;
- one whitespace-only case;
- no file, network, or external-service side effect;
- a plain-language explanation.

Review the diff and tests. Then explain the function yourself without the
assistant. If you cannot, request a smaller implementation or more explanation.

## Chapter check

You pass when you can:

- define one bounded outcome and acceptance criteria;
- distinguish inspection, implementation, test, and observed evidence;
- review a diff for unexpected scope;
- identify secrets and business data that must not enter AI chat;
- explain why generated commands and dependencies are proposals;
- name warning signs that require a pause;
- report limitations without converting them into success claims.
