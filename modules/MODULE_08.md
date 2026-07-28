# Module 8 — Evaluate Usefulness and Business Value

## Outcome

You will calculate rule quality, inspect summary support, compare active time,
model cost and capacity honestly, record usability evidence, and make a
bounded evidence-based decision before claiming value.

## Beginner checkpoint

Start when Modules 1–7 pass. Inputs, expected results, configuration, code, and
prompt versions must be frozen for the evaluation run.

## Concepts

- An **evaluation set** has fixed inputs and expected results.
- **Precision** is true positives divided by all reported positives.
- **Recall** is true positives divided by all expected positives.
- A **false positive** is extra; a **false negative** is missed.
- **Supported-claim rate** is supported statements divided by statements
  checked.
- A **matched baseline** compares equivalent manual and assisted work.
- **Regression** is a previously passing behaviour that fails after change.
- A **decision threshold** is written before seeing a result.
- Course 1 uses exactly three final decision labels:
  `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, and `DO NOT CONTINUE`.
  Each is a valid pass when the recorded evidence supports it.

## Official readings

The United States National Institute of Standards and Technology (NIST)
publishes voluntary artificial intelligence (AI) risk guidance. OpenAI is one
AI provider and supplies the evaluation guide below. GOV.UK is the United
Kingdom government's public guidance website.

1. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
2. [OpenAI evaluation best practices](https://platform.openai.com/docs/guides/evals)
3. [GOV.UK Service Manual: measuring success](https://www.gov.uk/service-manual/measuring-success)

## Guided build

The worked example has attractive time savings but deliberately poor rule
quality, so the correct decision is rework. The independent recreation uses
the different 13-issue capstone result.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files. Comma-separated
values (CSV) stores the test rows; JavaScript Object Notation (JSON) stores the
metric report. EUR is the three-letter currency code for the euro.

Python is the programming language used to calculate the metrics. Markdown is
a plain-text format for headings, lists, and tables; `.md` is its file name
ending.

## Follow along — I show you exactly how

### Stage 1 — Create a complete imperfect evaluation

Open Windows PowerShell and run:

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
if (-not (Test-Path (Join-Path $projectRoot '.git'))) {
    throw 'Project repository not found. Complete Windows Setup before Module 8.'
}
$moduleFolder = Join-Path $projectRoot 'evidence\module-08'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
notepad .\worked_expected.csv
```

Paste and save:

```csv
work_item_id,rule_code,severity
WI-7001,R001,high
WI-7002,R004,high
WI-7003,R007,medium
WI-7004,R011,medium
```

Create `worked_found.csv`:

```csv
work_item_id,rule_code,severity
WI-7001,R001,high
WI-7002,R004,high
WI-7003,R007,medium
WI-7999,R009,medium
```

The system found three expected issues, added one false issue, and missed one.

### Stage 2 — Calculate exact metrics

Create `evaluate_worked.py`:

```python
from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
EXPECTED_FILE = BASE / "worked_expected.csv"
FOUND_FILE = BASE / "worked_found.csv"
REPORT_FILE = BASE / "worked_metrics.json"


def load(path: Path) -> dict[tuple[str, str], str]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    result: dict[tuple[str, str], str] = {}
    for row in rows:
        key = (row["work_item_id"], row["rule_code"])
        if key in result:
            raise ValueError(f"Duplicate key in {path.name}: {key}")
        result[key] = row["severity"]
    return result


def ratio(numerator: int, denominator: int) -> float:
    return 1.0 if denominator == 0 else numerator / denominator


def main() -> None:
    expected = load(EXPECTED_FILE)
    found = load(FOUND_FILE)
    expected_keys = set(expected)
    found_keys = set(found)
    true_positive = expected_keys & found_keys
    false_positive = found_keys - expected_keys
    false_negative = expected_keys - found_keys
    severity_mismatches = sorted(
        key for key in true_positive if expected[key] != found[key]
    )
    high_expected = {key for key, value in expected.items() if value == "high"}
    high_found_correctly = high_expected & found_keys

    report = {
        "expected": len(expected_keys),
        "found": len(found_keys),
        "true_positive": len(true_positive),
        "false_positive": sorted(false_positive),
        "false_negative": sorted(false_negative),
        "precision": ratio(len(true_positive), len(found_keys)),
        "recall": ratio(len(true_positive), len(expected_keys)),
        "high_severity_recall": ratio(
            len(high_found_correctly), len(high_expected)
        ),
        "severity_mismatches": severity_mismatches,
    }
    REPORT_FILE.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

Run:

```powershell
python .\evaluate_worked.py
```

**Expected result:** precision `0.75`, recall `0.75`, high-severity recall
`1.0`, one false positive, one false negative, and no severity mismatch.

**Troubleshooting:**

- If a duplicate-key error appears, do not delete evidence blindly; identify
  why one logical issue was recorded twice.
- If precision and recall are confused, remember: precision asks “of what was
  reported, how much was right?” Recall asks “of what should be found, how much
  was found?”

### Stage 3 — Complete the value and usefulness decision

Create `worked_evaluation_decision.md`:

```markdown
# Worked evaluation decision

## Thresholds written before decision

- Precision: 100% on frozen synthetic set.
- Recall: 100%.
- High-severity recall: 100%.
- Severity mismatches: 0.
- Supported summary statements: 100%.
- External actions: 0.
- Manual fallback drill: pass.

## Observed rule result

- Precision: 75% — fail.
- Recall: 75% — fail.
- High-severity recall: 100% — pass.
- Severity mismatches: 0 — pass.

## Summary support

Four statements checked; four supported; supported-claim rate 100%. This does
not repair the rule failures upstream.

## Matched active-time scenario

- Runs per month: 8.
- Manual active minutes per run: 30.
- Assisted active minutes including review: 15.
- Monthly manual time: 8 × 30 / 60 = 4 hours.
- Monthly assisted time: 8 × 15 / 60 = 2 hours.
- Capacity released in this scenario: 2 hours.

## Cost scenario — not a forecast

- Loaded labour assumption: EUR 45/hour.
- Modelled released capacity: 2 × EUR 45 = EUR 90/month.
- Usage/licence assumption: EUR 10/month.
- Maintenance: 1 hour × EUR 45 = EUR 45/month.
- Modelled remainder: EUR 35/month before setup, incident, training, and risk.
- Time released is not automatically cash saved.

## Usability check

Tasks: find source row; find rule; distinguish severity; reject draft; use
fallback. Four of five completed without help. Fallback instructions were
unclear.

## Decision

REWORK. Precision, recall, and usability thresholds fail. Attractive time and
cost scenarios do not override quality. Repair the missed/extra rule result and
fallback wording, rerun the frozen set, then decide again.
```

This is the complete decision logic: quality gates come before benefit claims.

### Stage 4 — Define regression control

Create `worked_regression_policy.md`:

```markdown
# Worked regression policy

Rerun the frozen evaluation after changes to input schema, rules, assessment
date, parsing, issue identity, severity, prompt, response contract, provider
configuration, approval, or output.

Do not change expected results merely because implementation changed. A gold
change requires a documented requirement change, owner approval, version
change, and review of prior evidence.
```

## Now recreate it yourself

Evaluate the different capstone result:

1. Copy files:

```powershell
$courseRoot = Read-Host 'Paste the full path to AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE'
$moduleFour = Join-Path $projectRoot 'evidence\module-04'
Copy-Item -LiteralPath (Join-Path $courseRoot 'practice_data\expected_issues.csv') -Destination .\recreated_expected.csv
Copy-Item -LiteralPath (Join-Path $moduleFour 'found_issues.csv') -Destination .\recreated_found.csv
Copy-Item .\evaluate_worked.py .\evaluate_recreated.py
notepad .\evaluate_recreated.py
```

Change the three file-name constants to the recreated names. Save and run:

```powershell
python .\evaluate_recreated.py
```

**Expected result:** 13 expected, 13 found, precision 1.0, recall 1.0,
high-severity recall 1.0, no false positives, no false negatives, and no
severity mismatches.

2. Create `recreated_evaluation_decision.md`. Include:

- thresholds written before the decision;
- actual rule metrics;
- every Module 5 summary statement and its support decision;
- your Module 1 measured manual active time;
- a newly timed assisted run including review;
- at least low, expected, and high volume/cost scenarios;
- licence/usage, review, maintenance, training, fallback, and incident costs;
- a five-task usability test;
- limitations, including self-testing and synthetic data;
- exactly one decision: `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or
  `DO NOT CONTINUE`.

`ACCEPT FOR SYNTHETIC PORTFOLIO` means the synthetic case may be shown with
its limitations. It does not authorize business use. `REWORK` means record and
repair the gaps. `DO NOT CONTINUE` means close the exercise safely and preserve
the evidence explaining why. Course 1 never transitions to a client or live
business implementation.

3. Create `recreated_regression_policy.md` using the capstone's actual change
triggers.
4. Verify:

```powershell
Select-String -Path .\recreated_evaluation_decision.md -Pattern 'precision','recall','supported','synthetic','not a forecast','fallback','decision'
```

**Expected result:** all seven evidence categories are found.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path` to obtain the full path. Replace
`[PASTE FULL PATH HERE]` and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
[PASTE FULL PATH HERE]

Do not create, edit, delete, rename, move, format, or execute anything. Do not
inspect the parent or another path. Stop if there are secrets, credentials,
real client data, workplace data, personal data, or health data.

Return:
1. PASS or NOT YET;
2. checks for: frozen expected and found sets; unique keys; correct
true-positive/false-positive/false-negative arithmetic; precision and recall;
high-severity recall; severity match; statement-level support review; matched
active time including human review; labelled volume/cost scenarios; all costs;
usability tasks; thresholds set before decision; quality overriding attractive
value; synthetic-portfolio-only boundary; regression triggers; gold-change
control; exactly one permitted final decision with evidence;
3. the smallest corrections for me to make if NOT YET.

Remain read-only and do not recalculate by changing files.
```

## Pass criteria

- [ ] Worked arithmetic produces 0.75 precision and recall and leads to REWORK.
- [ ] Recreated arithmetic reports all 13 expected keys correctly.
- [ ] Summary support is scored statement by statement.
- [ ] Manual and assisted time cover matched work and include review.
- [ ] Cost/value figures are labelled scenarios, not forecasts.
- [ ] Review, support, maintenance, training, fallback, and incident costs are
      included.
- [ ] Usability evidence and limitations are recorded.
- [ ] The decision follows thresholds, not enthusiasm.
- [ ] The decision is exactly `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, or
      `DO NOT CONTINUE`; every outcome can pass when evidence-backed.
- [ ] Regression and gold-change policies are explicit.
- [ ] Codex returns `PASS` read-only.

### Record your Module 8 PASS in Git

Do this only after Codex returns `PASS`.

```powershell
$projectRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\operations-exception-assistant'
Set-Location -LiteralPath $projectRoot
git status --short
git add -- "evidence/module-08"
git commit -m "complete module 8 evidence"
git status --short
```

If Git reports `nothing to commit`, confirm that the module evidence was
already recorded and unchanged. Never add secrets, real data, or unrelated
files.

## Consultant lens

Value claims require a baseline, a denominator, tested quality, full costs, and
limits. A demo that saves time while missing issues is not a successful
implementation.

## Capstone increment

The capstone has frozen metrics, summary support scoring, time and cost
scenarios, usability evidence, a bounded decision, and regression policy.

## Required artifact

The teaching contract creates worked and recreated datasets, metric reports,
evaluation decisions, and regression policies under `evidence/module-08`.

## Test gate

The **Pass criteria** are the complete gate.

## Stop or rework

Stop when expected results change after seeing output, denominators are hidden,
review time is omitted, savings are presented as guaranteed, quality gates are
overridden, or synthetic evidence is used to claim production readiness.

## Common failures

- Reporting only “accuracy.”
- Ignoring false negatives.
- Comparing an easy assisted case with a hard manual case.
- Treating time capacity as cash.
- Letting one perfect run replace regression policy.

## Estimated time

8–12 hours.
