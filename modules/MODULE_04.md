# Module 4 — Build the Non-AI Workflow First

## Outcome

Build a reliable local workflow that:

- reads the synthetic work-item CSV;
- validates each row;
- applies rules R001–R011;
- creates stable issue records;
- produces a useful exception report;
- records a visible state and run ID;
- handles bad input and duplicate retries;
- works without an AI provider.

## Beginner checkpoint

Before starting, you can:

- open `practice_data/work_items.csv` without changing it;
- explain a CSV header and row;
- write and run a small Python function;
- distinguish source data from derived output;
- explain each rule in `practice_data/README.md`;
- use Git status and diff.

If not, return to Foundations 3, 5, and 6.

## Concepts

### Rule-first workflow

A deterministic rule produces the same answer for the same validated input,
configuration, and assessment date. Missing fields, allowed values, duplicate
references, and date order belong here.

### Normalize, then compare

CSV values arrive as text. Preserve the raw value, then create a normalized
value for validation. Do not replace the raw source.

### Stable issue identity

An issue should be recognizable across identical reruns. Derive its ID from
the work-item ID, field, and rule code, or use another documented stable
method.

### Named state

Every run must visibly be in one state. A thrown error is not a state until the
workflow records it as `failed_manual`.

### Idempotency

Rerunning the same input must not create duplicate logical effects. Course 1
has only local output, but the habit is essential before future connectors.

## Official readings

- [Python `csv` module](https://docs.python.org/3/library/csv.html)
- [Python exceptions](https://docs.python.org/3/tutorial/errors.html)
- [pytest documentation](https://docs.pytest.org/)
- [n8n workflows](https://docs.n8n.io/workflows/)
- [n8n error handling](https://docs.n8n.io/flow-logic/error-handling/)

Use the evergreen audit if a current n8n interface differs from a screenshot.
Assess the observed behavior, not whether buttons remain in the same place.

## Guided build

### 1. Copy, do not edit, the source data

Copy the supplied file into your project:

```text
data/input/work_items.csv
tests/expected_issues.csv
```

Calculate and record the input SHA-256 hash. The hash is evidence that a later
comparison used the same bytes; it does not prove the data is true.

### 2. Define the run configuration

Record:

```json
{
  "rule_set_version": "1.0.0",
  "assessment_date": "2026-07-26",
  "ai_mode": "offline",
  "kill_switch": false
}
```

Do not use today's date for the supplied overdue rule. A moving date would make
the expected result change over time.

### 3. Load rows with explicit encoding

Create a loader that:

- opens UTF-8 text;
- checks that all 12 expected headers exist exactly once;
- returns raw row dictionaries;
- records the source line number;
- rejects a missing or empty file clearly.

Do not continue with a partially understood header.

### 4. Implement small validators

Write one function for each concern:

- required value;
- allowed status;
- allowed priority;
- ISO date format;
- date order;
- status/completion-date relationship;
- owner requirement;
- non-negative amount;
- amount/currency relationship;
- duplicate source reference;
- overdue open work.

Use rule codes R001–R011 from `practice_data/README.md`.

Apply format validation before date comparisons. An invalid date must not be
silently interpreted.

### 5. Create issue records

Each issue contains:

- issue ID;
- work-item ID;
- field;
- rule code;
- severity;
- plain-language message;
- observed value when safe and useful.

Validate the record with `schemas/issue.schema.json`.

### 6. Compare with the expected register

Compare on `(work_item_id, rule_code)`.

Report:

- true positives;
- false positives;
- false negatives;
- exact differences.

The supplied baseline contains 15 rows and 13 expected issues. Do not hard-code
those issue records in the checker.

### 7. Produce the rule-based report

Create:

```text
output/<run_id>/
  issues.json
  issues.csv
  rule_report.md
  run_record.json
```

The Markdown report should show counts, high-priority issues, all issue IDs,
and a limitation that a human must decide what to do.

### 8. Add named states

At minimum:

```text
received → validated → issues_ready
received → failed_manual
validated → no_action_needed
```

Write the current state to the run record and an audit event. Do not use a
filename as the only state.

### 9. Make duplicate runs safe

Derive a run key from:

- input hash;
- rule-set version;
- assessment date.

Rerunning the same key should either reuse the existing output or replace it
atomically according to a written rule. It must not append duplicate issues.

### 10. Orchestrate visibly

In n8n, create a small workflow that:

1. starts manually;
2. receives the input path and configuration;
3. calls the Python checker;
4. branches on success, no issues, or failure;
5. records the final state;
6. stops before any external action.

Export the n8n workflow JSON into Git after removing credentials and local
secrets.

### 11. Test failure cases

Create test copies for:

- missing file;
- wrong header;
- empty file;
- malformed date;
- repeated retry;
- zero-issue input;
- unexpected exception.

Each failure must be understandable without reading a Python stack trace alone.

## Consultant lens

Ask a client:

- Which system owns each field?
- Who defines and approves each business rule?
- Are blank values truly errors or legitimate exceptions?
- What date and timezone govern “overdue”?
- What happens today when a row cannot be processed?
- Which existing report already detects some of these issues?

Request evidence:

- a data dictionary;
- report examples with lawful, minimized test data;
- rule owner;
- exception volume;
- false-alarm cost;
- manual fallback.

Stop when:

- field meaning is disputed;
- no process owner will approve rules;
- expected results are unavailable;
- the source export changes without notice;
- failure would affect a person or binding decision.

Client-style deliverable:

- rule register, exception sample, failure matrix, and rule-only prototype.

## Capstone increment

The capstone now creates the complete deterministic issue register and
rule-based exception report.

AI is still absent. The workflow must already be useful.

## Required artifact

Save:

- `evidence/module_04_rule_register.md`;
- deterministic checker source;
- unit tests;
- comparison report against expected issues;
- exported n8n workflow;
- one normal and one failure run record;
- screenshot or recording of the visible failure path.

## Test gate

- [ ] All 13 supplied expected issues are detected.
- [ ] There are zero unexplained false positives or false negatives.
- [ ] Raw source data remains unchanged.
- [ ] Issue records validate against the schema.
- [ ] The report works with no API key.
- [ ] Every run ends in a named state.
- [ ] Identical reruns create no duplicate logical output.
- [ ] Missing and malformed input fail visibly.
- [ ] I can explain every rule and major code path.

## Stop or rework

Stop if passing requires:

- changing expected issues without evidence;
- letting AI determine objective rules;
- ignoring malformed rows;
- using moving dates;
- connecting a real system;
- hiding an error behind “completed”.

## Common failures

- comparing date strings before validating format;
- treating blank and zero as the same;
- losing leading zeros during spreadsheet import;
- using row number as a permanent business ID;
- appending results on every retry;
- testing only the happy path;
- letting n8n success mean the domain result was successful.

## Estimated time

12–18 hours for a literal beginner. Split the module if the deterministic rules
or tests are not yet understandable.
