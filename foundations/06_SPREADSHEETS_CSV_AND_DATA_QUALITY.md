# Foundation 6 — Spreadsheets, CSV, and Data Quality

## Outcome

You can inspect a table, import a CSV file without silently changing it,
identify common data-quality problems, and separate fixed validation rules from
AI interpretation.

This matters because many SME workflows begin with an Excel export, not an AI
model. If the rows are incomplete, inconsistent, duplicated, or misread, a
more capable model only produces a more convincing wrong answer.

## Tables represent units of work

A useful operational table normally has:

- one **row** for one work item, such as an order, ticket, invoice, or review;
- one **column** for one named attribute;
- one **header row** containing stable column names;
- one stable **ID** that identifies each work item;
- declared rules for values, dates, states, and blanks.

Example:

| work_item_id | status | received_date | due_date | owner_role |
|---|---|---|---|---|
| WI-0001 | in_progress | 2026-07-20 | 2026-07-30 | operations |

`WI-0001` is an identifier, not a number to calculate with. Leading zeros are
part of it.

Avoid using colour, cell position, hidden rows, merged cells, or a comment as
the only place where meaning is recorded. Those signals are easy to lose when
data is exported.

## Data types and explicit blanks

Common types include:

- text: `operations`;
- identifier: `WI-0001`;
- whole number: `4`;
- decimal amount: `1210.50`;
- Boolean: `true` or `false`;
- date: `2026-07-26`;
- blank: no recorded value.

A blank is not automatically zero, “no,” or “not applicable.” Decide what it
means for each column.

Use ISO dates in exchanged data:

```text
2026-07-26
```

This avoids ambiguity between day-month-year and month-day-year. Display dates
may be localised for a person, but stored and exchanged values need one declared
format.

For machine exchange, this course uses a dot as the decimal separator:
`1210.50`. A Dutch spreadsheet may display `1.210,50`; do not assume the
underlying export uses the same punctuation.

## CSV is plain text, not a workbook

CSV means comma-separated values. It contains rows and columns, but it does not
preserve formulas, formatting, colours, multiple sheets, filters, data
validation, or comments.

```csv
work_item_id,title,status
WI-0001,Check service request,in_progress
WI-0002,"Confirm price, tax, and reference",new
```

The second title contains commas, so it is wrapped in double quotes.

CSV files can differ in:

- delimiter: comma, semicolon, or tab;
- character encoding, usually UTF-8 for this course;
- decimal and date conventions;
- line endings;
- quoting of commas, quotes, and line breaks.

Do not “fix” a strange import by repeatedly saving the file. Import it
deliberately and select the actual delimiter and encoding. Keep the untouched
source export separately.

## Spreadsheet import protocol

For a supplied CSV:

1. Make a working copy; keep the original read-only.
2. Use the spreadsheet program's **Import from Text/CSV** function.
3. Select UTF-8.
4. Confirm the delimiter from the preview.
5. Import identifiers as text so `WI-0001` and leading zeros survive.
6. Confirm dates and decimals were not silently converted.
7. Count imported rows and compare with the source.
8. Save spreadsheet work as a new file, not over the original CSV.
9. Record the source filename, retrieval date, and any transformation.

Hidden or filtered rows still exist. Clear filters before counting or exporting.
Formula results can also change when a workbook recalculates. When evidence
matters, record whether a value came from the source, a formula, a manual edit,
or a workflow.

## Data quality in ordinary language

Use five basic questions:

| Dimension | Question | Example failure |
|---|---|---|
| Completeness | Is a required value present? | an active item has no owner |
| Validity | Does the value follow its declared rule? | priority is `urgent` when only low/medium/high are allowed |
| Consistency | Do related values agree? | due date is before received date |
| Uniqueness | Is the record represented once? | two rows share one source reference |
| Timeliness | Is it current enough for the purpose? | an open item is past its due date |

“The spreadsheet looks clean” is not a test. Convert each important expectation
into a rule with:

- a stable rule code;
- the exact fields it checks;
- a result: pass, issue, or cannot assess;
- severity and an owner;
- a plain-language message;
- a test case showing the rule works.

## Deterministic checks before AI

Use ordinary formulas or code for rules such as:

- required value present;
- value is in an allowed list;
- date uses the required format;
- due date is not before received date;
- identifier or reference is unique;
- amount is a non-negative number;
- completed status has a completion date;
- open item is overdue relative to a declared assessment date.

These rules are deterministic: the same input and rule version should produce
the same result.

AI can be useful later for bounded work such as:

- classifying an unclear free-text description;
- drafting a short explanation of already detected issues;
- grouping similar issue messages for human review.

AI should not silently repair source values, decide that missing data is
unimportant, invent an owner, or replace a rule that can be written exactly.

## Source, working copy, issue record, and summary

Keep four things distinct:

1. **Source export** — the untouched input snapshot.
2. **Working copy** — formulas or transformations used during analysis.
3. **Issue records** — one structured record for every failed rule.
4. **Summary** — counts and explanations derived from the issue records.

An issue should point back to its work item and rule. A summary should be
recalculable from issue records. Do not keep only a colourful dashboard.

An export is a snapshot, not necessarily the live system of record. Record its
retrieval time and do not write corrections back to a source system during this
course.

## Practice with the synthetic dataset

Use only:

- [`../practice_data/work_items.csv`](../practice_data/work_items.csv);
- [`../practice_data/expected_issues.csv`](../practice_data/expected_issues.csv);
- [`../practice_data/README.md`](../practice_data/README.md).

First inspect the files in a text editor. Then make a working copy and import
`work_items.csv` into your spreadsheet.

Complete these tasks:

1. Confirm there are 15 data rows and 12 columns.
2. Keep `work_item_id` and `source_reference` as text.
3. Create a separate `found_issues` sheet.
4. Apply rules R001–R011 from the practice README using filters, formulas, or
   careful manual checks.
5. Record one row per detected issue.
6. Compare your `(work_item_id, rule_code)` pairs with
   `expected_issues.csv`.
7. Count:
   - true positives: expected issues you found;
   - false positives: issues you reported that were not expected;
   - false negatives: expected issues you missed.
8. Explain one mistake without changing the expected answer file.

The answer file is learning evidence, not production truth. In client work,
expected results require agreement with a process owner and representative test
cases.

## Chapter check

You pass when you can explain:

- why one row should represent one declared unit of work;
- why an ID should often be imported as text;
- why CSV import settings matter;
- blank versus zero versus not applicable;
- completeness, validity, consistency, uniqueness, and timeliness;
- why fixed checks should run before AI summarisation;
- source export versus working copy versus issue records;
- true positive, false positive, and false negative;
- why a dashboard without traceable issue records is weak evidence.
