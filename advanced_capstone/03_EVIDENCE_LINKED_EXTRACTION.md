# Capstone Lab 3 — Turn OCR Text into Exact Evidence-Linked Fields

## Outcome

You will trace how fixed Python code turns Document AI text into structured
fields, exact quotes, page numbers, character positions, and quote hashes. You
will recreate the check with a different synthetic case.

## What “source linked” means

An extracted value is not enough. Every present field contains an evidence
identifier such as `EV-P1-003`. That identifier resolves to:

- the SHA-256 hash of the exact source PDF;
- a one-based page number;
- start and end character positions in Document AI text;
- the exact normalized quote;
- the SHA-256 hash of that quote; and
- a normalized bounding box when Document AI returns one.

The application resolves the positions back to text and recalculates the quote
hash before the field is accepted. A page number alone is not sufficient.

## Follow along — I show you exactly how

### Step 1 — Run only the extraction proof

```powershell
Set-Location -LiteralPath $demoRoot
& .\.venv\Scripts\Activate.ps1
python -m pytest .\tests\test_pipeline.py -k happy_path -vv
```

Expected result: one passing test.

### Step 2 — Inspect the field and evidence contracts

```powershell
notepad .\src\controlled_intake\schemas.py
notepad .\src\controlled_intake\evidence.py
```

Find:

- `ExtractedField`;
- `EvidenceLink`;
- `FIELD_PATTERNS`;
- `extract_fields`;
- `verify_evidence`.

Write a worked explanation in:

```powershell
$evidenceFolder = Join-Path $capstoneRoot 'evidence\evidence-links'
New-Item -ItemType Directory -Force -Path $evidenceFolder | Out-Null
notepad (Join-Path $evidenceFolder 'worked_evidence_link.md')
```

Use:

```markdown
# Worked C001 evidence link

Field: quote_reference
Expected value: Q-C001-2026
Source page: 1
Required binding: document hash + character range + exact quote + quote hash

Why this matters:
A model or parser can return a plausible value. The application accepts the
field only when the evidence identifier resolves to the actual frozen source.
```

### Step 3 — Inspect the local approved JSON

Open the C001 JSON export from Lab 1. Search for `quote_reference`, follow its
evidence identifier into the `evidence` list, and compare:

- `document_sha256`;
- `page_number`;
- `exact_quote`;
- `quote_sha256`;
- `start_index`;
- `end_index`.

Do not edit the export.

### Step 4 — Check deterministic money handling

The application reads `net_total_ex_vat`, `vat_amount`, and `total_inc_vat`.
Python `Decimal` performs money arithmetic without binary floating-point
rounding.

Run:

```powershell
python -m pytest .\tests\test_pipeline.py -k known_failure -vv
```

Expected result: C008 produces a `TOTAL_DISCREPANCY` finding and remains
`needs_review`. The declared source value is preserved.

## Now recreate it yourself

Use the local app to process C008. In a new
`recreated_c008_evidence.md`, record:

- the field name and source evidence identifier for the declared total;
- its page number;
- the exact source quote;
- the first eight characters of the quote hash;
- the declared total;
- the calculated `net + VAT` total;
- why neither value is silently overwritten.

Then process C006. Record why a missing value has:

- `value: null`;
- `status: missing`;
- no invented evidence locator; and
- a visible `MISSING_FIELD:valid_until` finding.

Use different wording from the worked C001 explanation.

## Ask Codex to check your work

```text
READ-ONLY EVIDENCE-LINK REVIEW.

Inspect only:
[PASTE FULL EVIDENCE FOLDER PATH]

Do not edit or run cloud calls. You may compare the saved synthetic JSON files
with the Markdown records. Stop for real data or credentials.

Return PASS or NOT YET for:
1. C001 quote_reference resolves to a real evidence item;
2. the document hash, page, character range, exact quote and quote hash exist;
3. C008 preserves declared and calculated totals and records a discrepancy;
4. C006 uses null plus a missing finding without a fabricated locator;
5. all evidence refers only to frozen synthetic cases;
6. the recreation is explained in the learner's own words.
```

## Pass criteria

- Every present field in the inspected cases cites known evidence.
- Every exact quote hash resolves.
- C008 discrepancy is deterministic.
- Missing data is not invented.
- The original source stays unchanged.
- Codex returns PASS.

## Stop conditions

Stop if a citation identifier is unknown, positions resolve to different text,
a quote hash differs, or a missing value is filled by inference.
