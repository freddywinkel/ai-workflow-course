# Module 8 — Evaluate Usefulness and Business Value

## Outcome

Run a reproducible evaluation that measures technical correctness, failure
behavior, reviewer usefulness, time, and cost, then make an honest pilot
decision.

## Beginner checkpoint

- normal and failure runs are reproducible;
- expected issues are frozen;
- the AI step is optional;
- review and fallback work;
- intended purpose and success measures are written before testing.

## Concepts

### Evaluation set

A useful set includes normal cases, known exceptions, boundary cases,
adversarial input, and operational failure.

### False positive and false negative

A false positive wastes reviewer attention. A false negative hides a real
issue. Their business costs may differ.

### Supported-claim rate

Every factual summary claim should refer to a verified issue. A fluent but
unsupported sentence is a failure.

### Baseline

Compare the workflow with the current manual method using the same cases and a
written procedure.

### Decision, not demonstration

The goal is evidence for `PILOT`, `REWORK`, or `DO NOT PILOT`, not a perfect
video.

## Official readings

- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html)

Use provider evaluation tools only after the local test set is understandable
and portable.

## Guided build

### 1. Freeze the evaluation inputs

Record hashes for:

- `work_items.csv`;
- `expected_issues.csv`;
- rule-set version;
- prompt;
- schemas;
- offline fixture;
- optional model configuration.

Do not edit the expected results after seeing the workflow output without a
documented rule-owner decision.

### 2. Define metrics before the run

Required deterministic metrics:

- true positives;
- false positives;
- false negatives;
- precision;
- recall;
- exact issue-key agreement;
- repeatability.

Required summary metrics:

- schema-valid output;
- real issue references;
- unknown issue references;
- unsupported factual statements;
- refusal/failure fallback success.

Required operational metrics:

- runs reaching a named state;
- duplicate effects;
- approval revision mismatches blocked;
- kill-switch success;
- manual fallback success.

### 3. Add test variants

Besides the supplied data, create separate test fixtures for:

- no issues;
- one issue;
- malformed header;
- empty file;
- invalid encoding;
- duplicated retry;
- AI timeout and refusal;
- unknown issue reference;
- prompt-injection-style text in a description;
- edit after approval;
- outbox failure.

Do not add real text copied from an employer.

### 4. Run deterministic evaluation

Run the complete local suite twice from a clean output folder.

The required supplied result is 13 expected issue keys with no unexplained
extras or misses.

Capture command, environment, duration, and result.

### 5. Human-score the summary

For each summary group, ask:

- Is it understandable?
- Is every factual statement supported?
- Does it preserve issue severity?
- Does it avoid inventing cause or obligation?
- Does it help the reviewer act faster?
- Does it clearly require review?

Use at least two summary variants if running a live model comparison.

### 6. Measure the manual baseline

Using the same synthetic cases:

1. review manually with the written rule register;
2. record active handling time;
3. record mistakes or rework;
4. run the assisted method;
5. record review time, not only machine time;
6. repeat to reduce one-run noise.

Label the result a small synthetic observation, not a savings forecast.

### 7. Record cost

Include:

- model call cost if used;
- local setup and maintenance time;
- reviewer time;
- likely monitoring and support;
- training;
- failures and rework;
- platform subscriptions.

Course 1 does not require pricing a client engagement.

### 8. Conduct a usability test

Ask one other person to use the synthetic review package without your help.
Observe:

- whether they find the source evidence;
- whether AI and rule content are distinguishable;
- whether they understand approval consequences;
- whether they can reject, edit, and use fallback;
- where they hesitate.

Do not coach during the first attempt.

### 9. Make the pilot decision

Use:

#### `PILOT`

Correctness, control, ownership, and likely value support a small supervised
next test.

#### `REWORK`

The idea may help, but specified gaps must be repaired and retested.

#### `DO NOT PILOT`

AI adds no value, existing tools are better, economics are weak, data is not
ready, or risk/ownership is unacceptable.

There is no mandatory improvement percentage.

### 10. Define regression policy

Rerun the relevant suite after:

- rule change;
- schema change;
- prompt change;
- model/provider change;
- n8n change;
- data export change;
- review UI change.

Set unacceptable-regression thresholds before the next change.

## Consultant lens

Ask:

- What error matters most to the business?
- What baseline evidence already exists?
- How much reviewer time is available?
- What success would justify a pilot?
- What result would stop it?
- Who accepts residual errors?
- How will benefit be checked after use?

Request:

- representative test cases;
- accepted expected outcomes;
- current process timing;
- error/rework records;
- review feedback;
- recurring cost assumptions.

Stop when:

- expected answers are unknown;
- the builder alone scores quality;
- the comparison uses different cases;
- a demo is substituted for measurement;
- unsupported claims are tolerated for convenience.

Client-style deliverable:

- evaluation report and pilot decision with limitations.

## Capstone increment

The full system now has frozen evaluation evidence, a human usability result,
and a justified pilot decision.

## Required artifact

- `evidence/module_08_evaluation_report.md`;
- machine-readable test results;
- hashes and configuration;
- manual versus assisted timing sheet;
- summary human-score sheet;
- usability observation;
- cost record;
- final decision draft.

## Test gate

- [ ] Expected and observed issue keys are compared exactly.
- [ ] False positives and false negatives are explained.
- [ ] AI support and fallback metrics are reported.
- [ ] Operational invariants pass.
- [ ] Identical reruns are consistent.
- [ ] Manual and assisted methods use the same cases.
- [ ] Another person completed the usability test.
- [ ] Cost includes review and support, not only tokens.
- [ ] The decision follows evidence and allows `DO NOT PILOT`.

## Stop or rework

Stop if:

- a test is removed because it fails;
- model output is manually corrected before scoring;
- one synthetic timing is presented as an annual saving;
- no stop criterion exists;
- the result cannot be reproduced from recorded inputs.

## Common failures

- measuring model latency instead of end-to-end review time;
- counting schema validity as factual accuracy;
- ignoring false-alarm burden;
- changing multiple components before regression;
- selecting only impressive screenshots;
- making an ROI forecast from course data.

## Estimated time

12–16 hours.
