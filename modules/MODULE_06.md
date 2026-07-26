# Module 6 — Keep Humans in Control

## Outcome

You will bind a human decision to one exact draft revision, invalidate approval
after any change, expire old approval, keep an external-action kill switch off,
create only a local draft outbox, and demonstrate manual fallback.

## Beginner checkpoint

Start when Module 5 has a validated synthetic summary and a completed human
support review. Python is a programming language; you can run a Python file and
inspect JavaScript Object Notation (JSON). Windows PowerShell is the Windows
command application used below.

## Concepts

- **Meaningful human review** gives a reviewer the evidence, time, authority,
  and real options to approve, edit, reject, or expire.
- A **revision** is one identified version of a draft.
- A **hash** is a digital fingerprint of exact bytes.
- **Secure Hash Algorithm 256-bit (SHA-256)** is the fingerprint method used
  below; PowerShell spells its command option `SHA256`.
- Python's standard-library **`hashlib` module** calculates hashes such as
  SHA-256.
- **Comma-separated values (CSV)** is a plain-text table format.
- An **identifier (ID)** is a value that distinguishes one issue, run, or
  decision.
- **Markdown** is a plain-text format for headings, lists, and tables; `.md` is
  its file name ending.
- **Time of check versus time of use** means approval can become invalid
  between review and later use.
- A **kill switch** disables a class of action.
- A **draft outbox** is local prepared content; it is not a sent message.
- An **audit event** records what happened without claiming more than occurred.

## Official readings

The European Union Artificial Intelligence (AI) Act is the European Union's
AI law. The United States National Institute of Standards and Technology
(NIST) publishes voluntary AI risk guidance. Neither short description is a
legal assessment of a client's workflow.

1. [European Commission: AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
2. [NIST AI Risk Management Framework Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
3. [Python `hashlib` documentation](https://docs.python.org/3/library/hashlib.html)

## Guided build

The worked lifecycle approves one exact mock draft and then proves that an edit
invalidates that approval. The independent recreation uses a different draft
revision and decision history.

Windows PowerShell is the Windows command application used below. Notepad is
the Windows plain-text editor used to create practice files.

## Follow along — I show you exactly how

### Stage 1 — Assemble a complete review package

Open Windows PowerShell and run:

```powershell
$practiceBase = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'controlled-ai-course-practice'
$moduleFolder = Join-Path $practiceBase 'module-06'
New-Item -ItemType Directory -Force -Path $moduleFolder
Set-Location -LiteralPath $moduleFolder
$moduleFive = Join-Path $practiceBase 'module-05'
Copy-Item -LiteralPath (Join-Path $moduleFive 'worked_issues.csv') -Destination .\worked_issues.csv
Copy-Item -LiteralPath (Join-Path $moduleFive 'worked_validated_summary.json') -Destination .\worked_draft.json
Get-FileHash .\worked_draft.json -Algorithm SHA256
```

Create `worked_review.md` in Notepad:

```markdown
# Worked human review

- Draft revision: 1
- Reviewer role: operations_lead
- Source issues opened: yes
- Every issue ID visible exactly once: yes
- Every statement supported: yes
- Severity changed: no
- Recommendation or external action added: no
- Decision: approve this exact internal draft
- Reason: structure and cited statements match the three synthetic issues
- External action authorised: no
```

**Expected result:** the package contains the issue evidence, exact draft, hash,
reviewer role, review checks, decision, and reason.

If `worked_validated_summary.json` is missing, return to Module 5. Do not create
an approval for an unvalidated response.

### Stage 2 — Create an approval bound to exact bytes

In PowerShell, run:

```powershell
$workedHash = (Get-FileHash .\worked_draft.json -Algorithm SHA256).Hash.ToLower()
$workedApproval = [ordered]@{
  decision_id = 'DEC-WORKED-001'
  run_id = 'RUN-DEMO-001'
  reviewer_role = 'operations_lead'
  decision = 'approve'
  draft_revision = 1
  draft_sha256 = $workedHash
  decided_at = '2026-07-26T10:00:00+00:00'
  expires_at = '2026-07-27T10:00:00+00:00'
  reason = 'Synthetic evidence and statements match.'
}
$workedApproval | ConvertTo-Json | Set-Content .\worked_approval.json -Encoding utf8
$workedControl = [ordered]@{
  external_actions_enabled = $false
  allowed_output = 'local_draft_only'
}
$workedControl | ConvertTo-Json | Set-Content .\worked_control.json -Encoding utf8
Get-Content .\worked_approval.json
Get-Content .\worked_control.json
```

`ConvertTo-Json` converts the PowerShell object into JSON. The hash binds the
decision to revision 1. The kill switch is explicitly false.

### Stage 3 — Verify before creating a local draft

Create `check_worked_approval.py`:

```python
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
NOW = datetime.fromisoformat("2026-07-26T12:00:00+00:00")


def safe_stop(message: str) -> None:
    print(f"NOT VALID: {message}")
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 4:
        safe_stop("use: python check_worked_approval.py DRAFT APPROVAL CONTROL")
    draft_path = BASE / sys.argv[1]
    approval_path = BASE / sys.argv[2]
    control_path = BASE / sys.argv[3]

    draft_bytes = draft_path.read_bytes()
    current_hash = hashlib.sha256(draft_bytes).hexdigest()
    approval = json.loads(approval_path.read_text(encoding="utf-8-sig"))
    control = json.loads(control_path.read_text(encoding="utf-8-sig"))

    if control.get("external_actions_enabled") is not False:
        safe_stop("external-action kill switch must remain off")
    if control.get("allowed_output") != "local_draft_only":
        safe_stop("only local_draft_only is permitted")
    if approval.get("decision") != "approve":
        safe_stop("decision is not approve")
    if approval.get("draft_sha256") != current_hash:
        safe_stop("draft bytes changed after review")
    if int(approval.get("draft_revision", 0)) < 1:
        safe_stop("draft revision is invalid")
    expires_at = datetime.fromisoformat(approval["expires_at"])
    if NOW >= expires_at:
        safe_stop("approval expired")

    outbox = BASE / "worked_outbox"
    outbox.mkdir(exist_ok=True)
    destination = outbox / "internal_review_draft.json"
    destination.write_bytes(draft_bytes)
    audit = {
        "state": "approved_draft",
        "decision_id": approval["decision_id"],
        "draft_sha256": current_hash,
        "output": str(destination.name),
        "external_actions": 0,
        "human_review_required_before_any_use": True,
    }
    (BASE / "worked_audit.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8"
    )
    print("PASS: exact approved revision copied to local draft outbox.")


if __name__ == "__main__":
    main()
```

Run:

```powershell
python .\check_worked_approval.py worked_draft.json worked_approval.json worked_control.json
Get-Content .\worked_audit.json
Get-ChildItem .\worked_outbox
```

**Expected result:** `PASS`, state `approved_draft`, a local draft file, and
`external_actions` equal to 0. Nothing is sent.

**Troubleshooting:**

- “kill switch must remain off” means the control file is unsafe; restore
  `false`.
- “draft bytes changed” means approval no longer applies. Review a new
  revision; never copy the old hash.
- A missing outbox is correct after a safe stop.

### Stage 4 — Prove that an edit invalidates approval

Copy and edit the draft:

```powershell
Copy-Item .\worked_draft.json .\worked_draft_edited.json
notepad .\worked_draft_edited.json
```

Add one space inside the headline string, save, and close. Then run:

```powershell
python .\check_worked_approval.py worked_draft_edited.json worked_approval.json worked_control.json
```

**Expected result:** `NOT VALID: draft bytes changed after review` and exit code
1. Even a harmless-looking edit changes the reviewed bytes.

### Stage 5 — Demonstrate manual fallback

Create `worked_fallback.md`:

```markdown
# Worked manual fallback

Trigger: approval invalid, expired, rejected, or system unavailable.
Owner: operations coordinator.
Steps:
1. Stop automated progression.
2. Open worked_issues.csv.
3. Recreate the internal list directly from verified issue rows.
4. Have the operations lead review the new exact draft.
5. Create a new revision and decision; never reuse the old hash.
External action: none.
```

The fallback is a real route, not “try the AI again.”

## Now recreate it yourself

Use the different 13-issue summary from Module 5.

1. Copy `recreated_issues.csv` and `recreated_validated_summary.json` into
   `module-06` as `recreated_issues.csv` and `recreated_draft_v1.json`.
2. Write `recreated_review_v1.md` with decision `edit` because you want a
   clearer headline. Do not create an approval for v1.
3. Copy v1 to `recreated_draft_v2.json`, change only the headline, and perform a
   full new support review in `recreated_review_v2.md`.
4. Create `recreated_approval.json` using the PowerShell pattern above with:
   revision 2, a new decision ID, v2's exact hash, reviewer role
   `course_reviewer`, and a future fixed expiry.
5. Create `recreated_control.json` with the kill switch false.
6. Copy the checker to `check_recreated_approval.py`. Change only
   `worked_outbox` and `worked_audit.json` to recreated names.
7. Run it for v2 and expect `PASS`. Run it for v1 with the v2 approval and
   expect `NOT VALID`.
8. Create a new `recreated_fallback.md` for the 13-issue process.

Verify:

```powershell
Get-FileHash .\recreated_draft_v1.json -Algorithm SHA256
Get-FileHash .\recreated_draft_v2.json -Algorithm SHA256
Get-Content .\recreated_audit.json
```

**Expected result:** different v1/v2 hashes, only v2 passes its approval, and
the audit still reports zero external actions.

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
2. checks for: evidence package; meaningful reviewer choices; exact draft hash;
revision; decision reason; expiry; edit invalidation; reject/edit not treated as
approval; external-action kill switch false; local draft-only outbox; zero
external actions; audit event; worked and recreated mismatch tests; practical
manual fallback; synthetic data only;
3. the smallest corrections for me to make if NOT YET.

Remain read-only and do not provide replacement files.
```

## Pass criteria

- [ ] Approval is bound to one exact hash and revision.
- [ ] Edited or expired drafts cannot reuse approval.
- [ ] Approve, edit, reject, and expire are meaningful decisions.
- [ ] The external-action kill switch remains false.
- [ ] The only output is a local internal draft.
- [ ] Audit records zero external actions.
- [ ] A new review and decision are required for v2.
- [ ] Manual fallback is complete and role-owned.
- [ ] All files are synthetic and secret-free.
- [ ] Codex returns `PASS` read-only.

## Consultant lens

“A person is in the loop” is insufficient. The reviewer needs evidence,
authority, time, visible changes, and a real ability to stop progression.

## Capstone increment

The capstone has exact-revision approval, expiry, change invalidation, local
draft-only output, kill switch, audit evidence, and manual fallback.

## Required artifact

The teaching contract creates worked and recreated review packages, decisions,
controls, checkers, outboxes, audits, mismatch tests, and fallback records.

## Test gate

The **Pass criteria** are the complete gate.

## Stop or rework

Stop if approval survives changed bytes, an expired decision passes, an action
switch is on, a sent-message function appears, or a reviewer lacks evidence or
authority.

## Common failures

- Approving “whatever the latest version is.”
- Treating silence as approval.
- Hiding an edit after review.
- Calling a local draft a sent message.
- Providing a kill switch that is never tested.

## Estimated time

8–12 hours.
