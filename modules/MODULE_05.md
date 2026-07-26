# Module 5 — Add One Bounded Artificial Intelligence (AI) Step

## Outcome

You will add a replaceable, bounded summary step after deterministic issue
detection. You will validate its structure and issue references, perform a
human support check, and preserve a rule-based fallback.

Artificial Intelligence (AI) means software that can generate or infer an
answer. **Bounded** means this AI step receives only named inputs and may
perform only the explicitly listed transformation.

No paid provider or application programming interface (API) key is required.
The worked example uses a **mock provider response**: a saved synthetic response
that behaves like external AI output for repeatable testing. A later approved
provider can replace the mock without changing the contract.

## Beginner checkpoint

Start when Module 4 produces 13 verified issues and zero external actions.
Python is a programming language; you can read comma-separated values (CSV),
JavaScript Object Notation (JSON), and run a Python file.

## Concepts

- A **bounded contribution** permits only named transformations.
- **Structured output** follows a machine-checkable shape.
- **Grounding** links each statement to verified input.
- **Abstention** means returning no claim when support is insufficient.
- An **adapter** isolates provider-specific code from business logic.
- A **prompt version** identifies the instruction set used.
- A **fallback** completes the task safely without AI.
- An **identifier (ID)** is a value that distinguishes one issue or run.
- **Markdown** is a plain-text format for headings, lists, and tables; `.md` is
  its file name ending.

AI remains probabilistic: the same request may produce different wording. It
may group and rephrase verified issues, but may not discover issues, change
severity, recommend action, or authorise anything.

## Official readings

The United States National Institute of Standards and Technology (NIST)
publishes the voluntary risk profile below. OpenAI is one possible AI provider,
not a required course dependency.

1. [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
2. [OpenAI Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs)
3. [OpenAI evaluation best practices](https://platform.openai.com/docs/guides/evals)

Do not pin the course to a model name; a real implementation records the
configured provider, model, settings, prompt, and date.

## Guided build

The worked example validates a complete three-issue response. The independent
recreation applies the same boundary to the different 13-issue capstone output.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files.

## Follow along — I show you exactly how

### Stage 1 — Create a safe mock input

Open Windows PowerShell and run:

```powershell
$practiceBase = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'controlled-ai-course-practice'
$moduleFolder = Join-Path $practiceBase 'module-05'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
notepad .\worked_issues.csv
```

Click **Yes**, paste, save, and close:

```csv
issue_id,work_item_id,field,rule_code,severity,message
I-01,WI-8001,title,R001,medium,Required title is missing.
I-02,WI-8002,amount,R008,high,Amount must be a non-negative decimal.
I-03,WI-8003,due_date,R011,high,Open work is overdue on the fixed assessment date.
```

These are already-verified synthetic issues. The summary step does not receive
unnecessary raw rows.

### Stage 2 — See the exact prompt boundary and response

Create `worked_prompt.txt` in Notepad:

```text
Task: group and rephrase only the supplied verified issue objects.
Return the configured JSON structure.
Include every supplied issue_id exactly once.
Put each issue_id visibly in the summary sentence that it supports.
Do not add, remove, detect, resolve, recommend, rank, contact, send, approve,
order, pay, or change severity.
Set review_required to true.
If any statement lacks support, place it in unsupported_statements; otherwise
return an empty list.
```

Create `worked_ai_response.json`:

```json
{
  "run_id": "RUN-DEMO-001",
  "prompt_version": "summary-v1",
  "generator": "offline-mock",
  "headline": "Three synthetic work items need human review.",
  "groups": [
    {
      "label": "High attention",
      "issue_ids": ["I-02", "I-03"],
      "summary": "[I-02] has a non-negative-decimal validation failure. [I-03] is overdue on the configured assessment date."
    },
    {
      "label": "Medium attention",
      "issue_ids": ["I-01"],
      "summary": "[I-01] has a missing required title."
    }
  ],
  "unsupported_statements": [],
  "review_required": true
}
```

The wording remains factual. “High attention” repeats an approved severity; it
does not decide what a person should do.

### Stage 3 — Validate the complete response

Create `validate_worked_summary.py`:

```python
from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ISSUES_FILE = BASE / "worked_issues.csv"
RESPONSE_FILE = BASE / "worked_ai_response.json"
VALIDATED_FILE = BASE / "worked_validated_summary.json"
AUDIT_FILE = BASE / "worked_summary_validation.json"

REQUIRED_TOP_LEVEL = {
    "run_id", "prompt_version", "generator", "headline", "groups",
    "unsupported_statements", "review_required",
}
BANNED_ACTION_WORDS = {
    "send", "pay", "order", "approve", "reject", "select",
    "recommend", "hire", "fire", "contact",
}


def main() -> None:
    with ISSUES_FILE.open("r", encoding="utf-8-sig", newline="") as stream:
        issues = list(csv.DictReader(stream))
    known_ids = {issue["issue_id"] for issue in issues}
    if len(known_ids) != len(issues):
        raise ValueError("Input issue_id values are not unique.")

    response = json.loads(RESPONSE_FILE.read_text(encoding="utf-8"))
    if set(response) != REQUIRED_TOP_LEVEL:
        raise ValueError("Top-level response fields do not match the contract.")
    if response["review_required"] is not True:
        raise ValueError("review_required must be true.")
    if response["unsupported_statements"] != []:
        raise ValueError("Unsupported statements require manual fallback.")
    if not isinstance(response["headline"], str) or not response["headline"].strip():
        raise ValueError("Headline is blank.")
    if not isinstance(response["groups"], list) or not response["groups"]:
        raise ValueError("At least one group is required.")

    used_ids: list[str] = []
    for group in response["groups"]:
        if set(group) != {"label", "issue_ids", "summary"}:
            raise ValueError("A group has unexpected fields.")
        if not group["label"].strip() or not group["summary"].strip():
            raise ValueError("Group label or summary is blank.")
        for issue_id in group["issue_ids"]:
            if issue_id not in known_ids:
                raise ValueError(f"Unknown issue_id: {issue_id}")
            if issue_id not in group["summary"]:
                raise ValueError(f"{issue_id} is not visible in its summary.")
            used_ids.append(issue_id)

    if len(used_ids) != len(set(used_ids)):
        raise ValueError("An issue_id is used more than once.")
    if set(used_ids) != known_ids:
        raise ValueError(
            f"Missing issue IDs: {sorted(known_ids - set(used_ids))}"
        )

    response_words = set(
        response["headline"].lower().replace(".", "").split()
    )
    for group in response["groups"]:
        response_words.update(
            group["summary"].lower().replace(".", "").split()
        )
    found_banned = sorted(BANNED_ACTION_WORDS & response_words)
    if found_banned:
        raise ValueError(f"Action words are outside scope: {found_banned}")

    VALIDATED_FILE.write_text(
        json.dumps(response, indent=2) + "\n", encoding="utf-8"
    )
    AUDIT_FILE.write_text(
        json.dumps(
            {
                "status": "structure_and_references_valid",
                "known_issue_count": len(known_ids),
                "used_issue_count": len(used_ids),
                "human_support_review_required": True,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"PASS: {len(used_ids)} issue IDs used exactly once.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"SAFE STOP: {error}")
        raise SystemExit(1)
```

Run:

```powershell
python .\validate_worked_summary.py
Get-Content .\worked_summary_validation.json
```

**Expected result:** `PASS: 3 issue IDs used exactly once.` The audit still says
human support review is required because structure cannot prove meaning.

**Troubleshooting:**

- `JSONDecodeError` means a quote, comma, bracket, or brace is missing. Compare
  the response exactly.
- “Unknown issue_id” means the response invented or mistyped a reference.
- “Missing issue IDs” means a verified issue disappeared.
- Never relax validation because an AI response looks persuasive.

### Stage 4 — Perform the human support check

Create `worked_support_review.md`:

```markdown
# Worked support review

| Statement | Issue IDs | Source message supports it? | Invented cause/action? | Decision |
|---|---|:---:|:---:|---|
| Three synthetic work items need human review. | I-01, I-02, I-03 | yes | no | accept |
| I-02 has a decimal validation failure. | I-02 | yes | no | accept |
| I-03 is overdue on the configured date. | I-03 | yes | no | accept |
| I-01 has a missing title. | I-01 | yes | no | accept |

Reviewer role: course learner acting as synthetic reviewer.
Result: accept as an internal draft; no external action.
Fallback: use the issue CSV and a deterministic count by severity.
```

Read every sentence against `worked_issues.csv`. This human step verifies
support; the Python step verifies representation and references.

## Now recreate it yourself

Use the different 13-issue capstone output:

1. Copy `found_issues.csv` from `module-04`:

```powershell
$moduleFour = Join-Path $practiceBase 'module-04'
Copy-Item -LiteralPath (Join-Path $moduleFour 'found_issues.csv') -Destination .\recreated_issues.csv
(Import-Csv .\recreated_issues.csv).Count
Import-Csv .\recreated_issues.csv | Select-Object issue_id,severity,message
```

**Expected output:** 13 issues and their IDs.

2. Create `recreated_prompt.txt` from the worked boundary, but choose the group
   labels `High attention` and `Medium attention`.
3. Create `recreated_ai_response.json` yourself. Use generator
   `offline-mock`, prompt version `summary-v1-recreated`, every one of the 13
   issue IDs exactly once, visible citations in each summary, an empty
   `unsupported_statements` list, and `review_required: true`. Use no action or
   recommendation.
4. Copy and configure the validator:

```powershell
Copy-Item .\validate_worked_summary.py .\validate_recreated_summary.py
notepad .\validate_recreated_summary.py
```

Change the four file-name constants from `worked_...` to their
`recreated_...` equivalents. Save and run:

```powershell
python .\validate_recreated_summary.py
```

**Expected output:** `PASS: 13 issue IDs used exactly once.`

5. Create `recreated_support_review.md`. Score every headline and summary
   sentence against the cited issue messages. Reject or edit any sentence that
   adds cause, recommendation, urgency beyond severity, or external action.
6. Write a deterministic fallback in the file: show counts by severity and
   state that the reviewer can work directly from `recreated_issues.csv`.

You have recreated the contract with different volume, issue combinations,
wording, and grouping choices without exposing data or buying a provider.

## Ask Codex to check your work

Run `(Resolve-Path $moduleFolder).Path` to obtain the full path, replace
`[PASTE FULL PATH HERE]`, and copy:

```text
READ-ONLY COURSE REVIEW.

I authorize inspection of only this full path:
[PASTE FULL PATH HERE]

Do not edit, create, delete, rename, move, format, or execute files. Do not
inspect any parent or other folder. This folder must contain no secrets and no
real client or workplace data. Stop if there are API keys, credentials,
personal data, or health data.

Review the prompt, synthetic issue inputs, response JSON, validators, validation
audit, and human support reviews. Return:
1. PASS or NOT YET;
2. checks for: issue detection remains deterministic and upstream; only verified
issues enter summary; every issue ID appears exactly once; no unknown IDs;
visible citations; no severity change; no recommendation or action; structured
response; empty unsupported statements; review_required true; prompt version;
replaceable mock adapter; human sentence-level support review; deterministic
fallback; 3 worked and 13 recreated issues; no secret or real data;
3. the smallest corrections for me to make if NOT YET.

Remain read-only and do not generate a replacement summary.
```

## Pass criteria

- [ ] Worked response validates three unique issue IDs exactly once.
- [ ] Recreated response validates all 13 issue IDs exactly once.
- [ ] AI/mock input contains verified issue records, not unnecessary raw rows.
- [ ] Prompt forbids discovery, severity change, recommendation, and action.
- [ ] Output is structured, cited, versioned, and review-required.
- [ ] Human review verifies every sentence against evidence.
- [ ] Unsupported or invalid output stops or uses deterministic fallback.
- [ ] No provider secret, exact model dependency, or real data is required.
- [ ] Codex returns `PASS` read-only.

## Consultant lens

The durable design is the boundary and evaluation, not a provider brand.
Provider configuration can change; deterministic rules, evidence, human review,
fallback, and acceptance measures remain.

## Capstone increment

The capstone has one bounded summary adapter, validated issue references,
human support review, prompt version, and non-AI fallback.

## Required artifact

The teaching contract creates worked and recreated prompts, inputs, responses,
validators, audits, and support reviews under `module-05`.

## Test gate

The **Pass criteria** are the complete gate.

## Stop or rework

Stop if raw confidential data is proposed, an issue is invented or omitted,
severity changes, a recommendation appears, an API key enters a file, support
cannot be verified, or the fallback is missing.

## Common failures

- Trusting valid JSON as proof of factual support.
- Letting the model discover deterministic issues.
- Hiding an omitted issue in polished prose.
- Putting a secret in code or a screenshot.
- Making a live provider mandatory for a beginner exercise.

## Estimated time

8–12 hours.
