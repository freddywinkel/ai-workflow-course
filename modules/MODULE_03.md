# Module 3 — Understand the Data and Rules

Lesson ID: `course-1-module-03`
Revision: 2026-07-26

## Outcome

You will turn a spreadsheet-like business process into an explicit data
contract and an approved rule register before building a workflow.

Using the supplied synthetic files, you will learn what each column means, how
blank and invalid values must be handled, which checks are deterministic, which
checks depend on earlier checks, and what evidence every reported issue must
contain.

At the end of the module, another beginner should be able to implement the
checks without asking you to “use common sense.” No AI is required to detect
the capstone issues.

## Beginner checkpoint

Complete the Module 2 test gate. Your intended purpose must still be limited to
a synthetic, internal, reviewed exception report with no source-system
write-back or external action.

Revisit the foundations on files and text, code and Python, web APIs and JSON,
and AI and document workflows. Be able to explain:

- a row, column, value, header, and CSV file;
- text, date, decimal number, and blank value;
- required, unique, and allowed-list constraints;
- why a deterministic rule should give the same result for the same input and
  configuration;
- why a language model should not be asked to calculate or guess a rule that
  can be written exactly.

CSV is plain text organised into rows and separated values. It is not the same
file format as an Excel workbook: it has no sheets, formulas, cell colours, or
formatting. A spreadsheet application can open CSV, but may silently reinterpret
dates, decimals, or identifiers. Preserve the source and work on a copy or
derived output.

## Concepts

- **Schema:** the expected fields, types, and structural constraints of data.
- **Data dictionary:** a human-readable description of every field and its
  meaning.
- **Raw value:** the exact value received from the source.
- **Normalised value:** a controlled representation used after validation,
  such as a parsed date. Keep the raw value for evidence.
- **Blank versus zero:** an empty amount means “not supplied”; `0` is a supplied
  numeric value. They are not interchangeable.
- **Missing versus unknown:** missing means no value is present. Unknown means
  the value is not known. Do not convert one into the other without an approved
  rule.
- **Allowed list:** the complete set of accepted values, such as `low`,
  `medium`, and `high`.
- **Cross-field rule:** a rule using more than one field, such as requiring a
  completion date when status is `completed`.
- **Rule dependency:** an order requirement between checks. A malformed date
  must fail its format check before date comparisons are attempted.
- **Reference date:** a configured date used for repeatable time-based rules.
  The capstone uses `2026-07-26`; it must not silently use the computer's
  current date.
- **Gold or expected result:** a frozen answer set used to evaluate an
  implementation.
- **True positive:** an expected issue that the workflow found.
- **False positive:** an issue the workflow reported but the expected set does
  not contain.
- **False negative:** an expected issue the workflow missed.
- **Provenance:** information showing which source record, field, rule, and
  value support an output.

## Official readings

1. [Python documentation: the `csv` module](https://docs.python.org/3/library/csv.html)
   explains CSV reading and writing, dialect differences, and why CSV is not as
   universal as it first appears.
2. [European Commission: GDPR processing principles](https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en)
   covers purpose limitation, data minimisation, accuracy, storage limitation,
   and accountability.
3. [European Commission: data protection by design and by default](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations/what-does-data-protection-design-and-default-mean_en)
   explains why safeguards should be requirements from the start.
4. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
   treats data, context, limitations, human roles, and test measures as part of
   mapping and measuring risk.

The practice data contains no personal data. The privacy readings matter
because a consultant must ask whether each future client field is necessary
and permitted before moving it into an automation or AI service.

## Guided build

### 1. Preserve and inventory the source files

The authoritative practice-data description is
`practice_data/README.md`. Read it before inspecting the answer key.

The two supplied files are:

- `practice_data/work_items.csv`: 15 fictional input rows;
- `practice_data/expected_issues.csv`: 13 frozen expected issues.

Do not edit either file. In PowerShell, from the course root, you can inspect
their identities:

```powershell
Get-FileHash .\practice_data\work_items.csv -Algorithm SHA256
Get-FileHash .\practice_data\expected_issues.csv -Algorithm SHA256
```

Record both hashes in your artifact. Re-run the commands at the test gate. A
changed hash means the source or answer key changed and the comparison is no
longer controlled.

Confirm counts without changing the files:

```powershell
$workItems = Import-Csv .\practice_data\work_items.csv
$expectedIssues = Import-Csv .\practice_data\expected_issues.csv
$workItems.Count
$expectedIssues.Count
$workItems[0].PSObject.Properties.Name
```

The expected results are a test oracle, not the business requirements. The
requirements live in the practice-data README and the approved rule register.
Never edit the answer key to make an implementation pass.

### 2. Profile the input without “cleaning” it

Inspect the distinct values in important fields:

```powershell
$workItems | Group-Object status | Select-Object Name, Count
$workItems | Group-Object priority | Select-Object Name, Count
$workItems | Select-Object work_item_id, source_reference, owner_role, received_date, due_date, completed_date, amount, currency
```

In a spreadsheet, you may use filters or a pivot table instead. Do not overwrite
the CSV.

Record:

- row count and column count;
- exact headers;
- blank-value counts per field;
- distinct statuses, priorities, currencies, and categories;
- apparent duplicates;
- suspicious date and amount formats.

Describe what is present. Do not silently correct `urgent`, `on_hold`, a
day-month-year date, a negative amount, or a blank field. An invalid input is
evidence for an exception, not permission to manufacture a replacement.

### 3. Create the field dictionary

Document all 12 source fields:

| Field | Meaning | Type or format | Required or conditional | Allowed values or constraint | Blank meaning | Example |
|---|---|---|---|---|---|---|
| `work_item_id` | stable fictional item identifier | text | required | unique | invalid | `WI-0001` |
| `source_reference` | reference from the fictional source system | text | required | unique | invalid | `REF-1001` |
| `title` | non-sensitive work description | text | required | non-blank | invalid | `Confirm delivery window` |
| `owner_role` | responsible role, never a person's name | text | conditional | required for `in_progress`, `waiting`, and `completed` | no owner recorded | `operations` |
| `status` | workflow state | text | required | `new`, `in_progress`, `waiting`, `completed`, `cancelled` | invalid | `in_progress` |
| `priority` | declared attention level | text | required | `low`, `medium`, `high` | invalid | `medium` |
| `received_date` | intake date | ISO date | required | real calendar date in `YYYY-MM-DD` | invalid | `2026-07-20` |
| `due_date` | target date | ISO date | optional | blank or valid date not before received date | no target recorded | `2026-07-30` |
| `completed_date` | completion date | ISO date | conditional | required only for `completed`; otherwise blank | depends on status | `2026-07-18` |
| `amount` | fictional operational amount | decimal text | optional | blank or non-negative decimal using a dot | no amount supplied | `125.00` |
| `currency` | currency of amount | text | conditional | `EUR` when amount is present; otherwise blank | no currency supplied | `EUR` |
| `category` | operational work type | text | required | non-blank in this course | invalid | `order_admin` |

If a real client cannot agree on a field's meaning, owner, or allowed values,
that is a discovery finding. Do not solve disagreement by hiding it in a
prompt.

### 4. Translate requirements into deterministic rules

Create one row per rule:

| Code | Exact condition | Fields | Severity | Dependency | Evidence on failure | Requirement owner or source |
|---|---|---|---|---|---|---|
| R001 | | | | | | |

Use these approved capstone meanings:

- **R001 — required values:** `work_item_id`, `source_reference`, `title`,
  `received_date`, and `category` are non-blank. The supplied deliberate R001
  case is a missing title. Severity: medium.
- **R002 — status list:** status must be exactly `new`, `in_progress`,
  `waiting`, `completed`, or `cancelled`. Severity: high.
- **R003 — priority list:** priority must be exactly `low`, `medium`, or
  `high`. Severity: medium.
- **R004 — ISO dates:** each populated date must be a real calendar date written
  `YYYY-MM-DD`. Checking only the shape of the text is insufficient; for
  example, `2026-02-31` is not a real date. Severity: high.
- **R005 — date order:** when received and due dates are valid, the due date
  must be on or after the received date. Severity: high.
- **R006 — completion consistency:** `completed` requires a valid completion
  date. Every other allowed status requires a blank completion date. A missing
  date on completed work is high severity; an unexpected date on active work
  is medium severity.
- **R007 — owner requirement:** `in_progress`, `waiting`, and `completed`
  require a non-blank `owner_role`. Severity: medium.
- **R008 — amount:** a populated amount must parse as a decimal and be zero or
  greater. Severity: high.
- **R009 — currency:** a populated amount requires currency `EUR`. The data
  dictionary also says currency is blank when no amount is supplied; record a
  test for both directions rather than assuming spreadsheet formatting will
  enforce it. Severity: medium.
- **R010 — unique reference:** each non-blank `source_reference` must be unique
  across the complete file. Report every row participating in a duplicate, not
  only the second row encountered. Severity: high.
- **R011 — overdue open item:** when status is `new`, `in_progress`, or
  `waiting`, and `due_date` is valid and earlier than `2026-07-26`, report the
  item as overdue. A due date equal to the reference date is not overdue.
  Severity: high.

Severity is an internal attention level in this fictional exercise. It is not a
legal, clinical, safety, or employee-performance judgement.

### 5. Define rule order and failure behaviour

Write the planned order:

1. preserve the raw row;
2. check required values;
3. check allowed lists;
4. validate dates and amount;
5. run cross-field checks only on valid prerequisite values;
6. check duplicate references across the complete file;
7. check overdue status using the configured reference date;
8. create evidence-linked issue records;
9. route processing or configuration failures to human review.

Important examples:

- If `received_date` fails R004, do not invent a parsed date for R005.
- If `due_date` fails R004, do not run R005 or R011 on that value.
- If status fails R002, do not guess that it means `waiting`.
- If an amount is blank, do not turn it into zero.
- If the file header is missing or changed, stop the run. Do not ask AI to
  guess which column was intended.

These choices prevent one malformed value from generating misleading secondary
issues.

### 6. Define the issue output contract

Every later workflow issue must contain:

| Output field | Purpose |
|---|---|
| `work_item_id` | links the issue to one input row |
| `source_reference` | provides a second traceable source reference |
| `field` | names the affected field |
| `raw_value` | preserves the relevant received value, including blank |
| `rule_code` | links to R001–R011 |
| `severity` | uses the approved rule/scenario severity |
| `message` | states the observed problem without inventing a cause or remedy |
| `assessment_date` | records the configured `2026-07-26` reference date |

For comparison with the answer key, the stable match key is
`(work_item_id, rule_code)`. Preserve the field and evidence as well; a passing
pair with the wrong explanation is not a useful consulting result.

A good message says:

> WI-0010 is open and has due date 2026-07-10, which is before the configured
> assessment date 2026-07-26.

A poor message says:

> The operations team forgot this important customer and should contact them
> immediately.

The poor message invents a cause, a customer relationship, and an action.

### 7. Make boundary tests before implementation

For every rule, specify:

- one valid example;
- one failing example;
- one blank or not-applicable example where relevant;
- one boundary example;
- a dependency or malformed-input example where relevant.

Include at least:

- due date equal to received date;
- due date equal to the assessment date;
- zero amount;
- blank amount and blank currency;
- completed item with and without a completion date;
- cancelled item without an owner;
- two and three rows sharing a source reference;
- a correctly shaped but impossible date;
- a changed or missing CSV header.

The supplied 15 rows are a small frozen acceptance set, not proof that the
rules work for every possible future row. Boundary tests expose gaps before
code makes them harder to notice.

### 8. Compare your manual interpretation with the frozen answer

Now open `practice_data/expected_issues.csv`. It contains 13 issue instances
covering R001–R011.

Create a comparison table:

| Work item | Rule | In your manual list? | In expected list? | Result | Explanation or correction |
|---|---|:---:|:---:|---|---|
| | | | | true positive / false positive / false negative | |

Do not erase a difference. Explain it, correct your rule interpretation if
needed, and keep the original observation in your learning record.

The final rule register must account for all 13 expected instances. The purpose
of this manual comparison is understanding, not a claim that the future
workflow already works.

### 9. Perform a data-minimisation screen

For every field, ask:

- Is it necessary for an approved rule, evidence, or reviewer context?
- Is a role sufficient instead of a person's name?
- Does it need to be passed to the later AI step?
- How long would a client need to keep the raw and derived data?
- Who should be able to see it?

For the capstone, later AI should receive only the already-detected synthetic
issue records needed to draft a summary. It does not need to discover issues in
the complete raw register.

In real consulting, synthetic data is not automatically representative.
Replacing it with real data requires a new scope, privacy, security, access,
retention, and testing decision.

## Consultant lens

Data and rules are business contracts, not merely technical details.

For a client engagement:

- ask which system and field are authoritative;
- identify the owner authorised to approve each rule;
- capture the rule source, version, effective date, exceptions, and examples;
- distinguish written policy from a person's habitual workaround;
- ask how blanks, conflicts, late updates, duplicates, and corrections are
  handled today;
- show the rule table back to users in plain language;
- require approval before implementation;
- version rule changes and rerun tests.

“Everyone knows what overdue means” is not a usable requirement. It could mean
before today, on or before today, after a grace period, or only for certain
statuses. The fixed date and exact `<` comparison in R011 demonstrate the
precision you need.

The most durable consultant skill here is not memorising CSV syntax. It is
making hidden meanings, ownership, dependencies, and failure behaviour visible
enough to test and hand over.

## Capstone increment

The capstone now has:

- preserved synthetic input and expected-output identities;
- an inventory of 15 input rows and 12 columns;
- a field dictionary;
- an approved R001–R011 rule register;
- a fixed assessment date;
- explicit rule dependencies and stop behaviour;
- an evidence-linked issue-output contract;
- boundary-test cases;
- a manual comparison with 13 expected issues;
- a data-minimisation decision.

The assistant still contains no AI. In Module 4, the deterministic workflow can
be implemented against this contract.

## Required artifact

Create `artifacts/data_and_rules_register.md` in your learner project.

It must contain:

1. source and expected-file SHA-256 hashes;
2. row count, column count, and exact header list;
3. the 12-field data dictionary;
4. R001–R011 with exact condition, fields, severity, dependency, evidence, and
   authoritative source;
5. the rule execution order and skip/stop behaviour;
6. the issue-output contract;
7. at least one valid and one failing test per rule plus the listed boundary
   cases;
8. the 13-row expected-issue comparison and explanations for initial
   differences;
9. the data-minimisation screen;
10. unresolved ambiguities, owner, version, approval status, and date.

You may save a separate manual `found_issues.csv`, but do not replace the
Markdown explanation with an unexplained spreadsheet.

## Test gate

Pass only when:

- [ ] `work_items.csv` still has 15 data rows and 12 expected headers.
- [ ] `expected_issues.csv` still has 13 data rows.
- [ ] Before-and-after hashes match for both supplied files.
- [ ] Every field has a meaning, type, requirement, allowed values or
      constraint, and blank-value interpretation.
- [ ] Every R001–R011 result can be decided without AI.
- [ ] All 13 expected `(work_item_id, rule_code)` pairs map to your rule
      register.
- [ ] Invalid dates cannot trigger R005 or R011.
- [ ] R010 reports both WI-0006 and WI-0007.
- [ ] R011 uses configured date `2026-07-26`, not “today.”
- [ ] Blank amount is not converted to zero.
- [ ] Raw values are preserved in issue evidence.
- [ ] A missing or changed header stops processing.
- [ ] The later AI boundary excludes discovering, adding, removing, or
      reprioritising issues.

Ask another person or an AI tutor to read one rule row and predict the result
for its valid, invalid, blank, and boundary examples. Give no spoken hints. If
the predictions differ from yours, the rule is not precise enough.

## Stop or rework

Stop or rework when:

- a supplied file was edited or its hash changed;
- a rule was inferred only from the errors in the sample rather than the
  authoritative requirement;
- a field's meaning, owner, or blank behaviour remains unstated;
- current date, locale, spreadsheet formatting, or model judgement can change
  a deterministic result;
- invalid input is silently corrected;
- dependent rules run on invalid prerequisite values;
- false positives or false negatives are hidden or removed from the record;
- the expected file is altered to match an implementation;
- severity is invented by AI;
- real workplace or client data is introduced.

If an authorised rule owner cannot resolve a material ambiguity in a real
engagement, the affected rule remains disabled or the project stops. Code is
not a substitute for authority.

## Common failures

- Letting a spreadsheet convert identifiers, dates, or decimals on save.
- Treating CSV appearance as proof of data type.
- Confusing blank, zero, false, and unknown.
- Using the computer's current date in a frozen test.
- Running comparisons after date parsing failed.
- Reporting only the second member of a duplicate pair.
- Writing broad rules such as “flag anything unusual.”
- Asking a language model to infer allowed values from the dataset.
- Omitting source field and raw value from an issue.
- Treating the answer key as requirements instead of a test oracle.
- Adding personal names because they feel more realistic.
- Making severity sound like a judgement about an employee.
- Correcting the source instead of detecting and reporting the exception.

## Estimated time

8–10 hours:

- 1 hour for readings and source inventory;
- 2 hours for profiling and the field dictionary;
- 2.5 hours for exact rules, dependencies, and output contract;
- 1.5 hours for boundary cases;
- 1 hour for the manual comparison and data-minimisation screen;
- 1–2 hours for corrections and the test gate.
