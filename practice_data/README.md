# Synthetic Work-Item Practice Data

These files support Foundation 6 and the first controlled workflow exercises.
Every row is fictional. The titles, identifiers, dates, roles, and amounts do
not describe a real person, employer, customer, or transaction.

Do not replace these files with workplace or customer exports.

Terms used below:

- **comma-separated values (CSV):** a plain-text table format;
- **identifier (ID):** a value used to distinguish one fictional record from
  another;
- **International Organization for Standardization (ISO) date:** the
  year-month-day format `YYYY-MM-DD`;
- **EUR:** the three-letter currency code for the euro.

## Files

- `work_items.csv` — 15 fictional operational work items, including deliberate
  data-quality problems.
- `expected_issues.csv` — the 13 issues that rules R001–R011 should detect.

Use the pair `(work_item_id, rule_code)` when comparing results. Do not edit the
expected file to make a check pass.

## Work-item columns

| Column | Meaning | Rule |
|---|---|---|
| `work_item_id` | stable fictional work-item ID | required; unique |
| `source_reference` | fictional reference from a source system | required; unique |
| `title` | short non-sensitive description | required |
| `owner_role` | role, never a person's name | required for in-progress, waiting, or completed work |
| `status` | current workflow state | `new`, `in_progress`, `waiting`, `completed`, or `cancelled` |
| `priority` | declared attention level | `low`, `medium`, or `high` |
| `received_date` | intake date | required ISO date `YYYY-MM-DD` |
| `due_date` | optional target date | ISO date; not before received date |
| `completed_date` | completion date | required only when status is `completed`; otherwise blank |
| `amount` | optional fictional amount | blank or a non-negative decimal using a dot |
| `currency` | currency for amount | `EUR` when amount is present; otherwise blank |
| `category` | operational work type | required |

## Rule register

Use the fixed assessment date **2026-07-26**.

| Code | Check |
|---|---|
| R001 | Required value is present. |
| R002 | Status is in the allowed status list. |
| R003 | Priority is `low`, `medium`, or `high`. |
| R004 | A populated date uses `YYYY-MM-DD`. |
| R005 | Due date is on or after received date. |
| R006 | Completed status has a completion date; other statuses do not. |
| R007 | `in_progress`, `waiting`, and `completed` items have an owner role. |
| R008 | A populated amount is a non-negative decimal. |
| R009 | A populated amount has currency `EUR`. |
| R010 | Source reference is unique across the file. |
| R011 | A `new`, `in_progress`, or `waiting` item with a due date before 2026-07-26 is overdue. |

Apply format checks before comparisons. If a date is invalid under R004, do not
invent a date to run R005 or R011.

## Suggested exercise evidence

This is a reference list, not a standalone exercise. First follow the complete
worked example in Foundation 6 or the matching module. That lesson then asks
you to recreate the check and gives you a read-only Codex inspection prompt.

Save these separately from the source files:

- imported row and column counts;
- `found_issues.csv` or a `found_issues` worksheet;
- true-positive, false-positive, and false-negative counts;
- one paragraph explaining a missed or extra issue;
- the formula, code, or manual procedure used for each rule.

Keep the original CSV files unchanged.
