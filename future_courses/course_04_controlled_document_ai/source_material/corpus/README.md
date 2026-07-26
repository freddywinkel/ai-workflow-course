# Frozen Synthetic Supplier Corpus

Version: 1.0  
Generator timestamp: 2026-01-01T00:00:00Z  
Cases: 20  
Data classification: synthetic, non-personal training data

This corpus supports the supplier-document capstone. It contains fictional
quotations, supplier terms and two equivalent internal-policy fixtures. It does
not contain a real person, organisation, address, account, identifier, health
fact or consequential decision. The documents must never be mixed with live
client data.

## Generate and validate

Use the course Python environment:

```powershell
$CourseRoot = "C:\path\to\AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE"
python -m pip install -r "$CourseRoot\tools\requirements-corpus.txt"
python "$CourseRoot\tools\generate_corpus.py"
python "$CourseRoot\tools\generate_corpus.py" --validate-only
```

Generation replaces only these generator-owned paths:

- `corpus/cases/`
- `corpus/shared/`
- `corpus/locators/`
- `corpus/manifest.jsonl`
- `corpus/golden.jsonl`
- `corpus/checksums.sha256`
- `corpus/validation_report.json`

The checked-in frozen corpus was generated with the bundled course runtime.
After an intentional dependency upgrade, regenerate the files and review the
resulting hashes and rendered pages before accepting a new frozen version.

## Files

- `manifest.jsonl`: one input-bundle record per case, including format,
  language, SHA-256, expected parser outcome, safety flags and checkpoint state.
- `golden.jsonl`: deterministic commercial fields, conflicts, findings,
  evidence expectations, calculations, memo constraints, approvals and
  deduplication behavior.
- `locators/`: one sidecar per source document. PDF locators use PDF-point
  boxes; image-only scans use pixel word-box unions; DOCX locators use stable
  logical paths and canonical character spans.
- `checksums.sha256`: hashes of generated sources and machine-readable gold
  files. The README, checksum file itself and validation report are excluded.
- `validation_report.json`: machine-readable generator checks.

## Case coverage

| Case | Main condition | Expected checkpoint state |
|---|---|---|
| C001 | Clean Dutch quotation PDF and terms DOCX | `pending_approval` |
| C002 | Clean English quotation DOCX and terms PDF | `pending_approval` |
| C003 | Two-page quotation table | `pending_approval` |
| C004 | Image-only scanned quotation | `pending_approval` |
| C005 | Image-only scanned terms | `pending_approval` |
| C006 | Missing valid-through date | `needs_review` |
| C007 | Payment-term conflict | `needs_review` |
| C008 | Declared/calculated total differs by EUR 20 | `needs_review` |
| C009 | Byte-identical C001 quotation and terms | `completed` |
| C010 | Exact corrupt/mislabeled quotation bytes | `failed_manual` |
| C011 | Missing terms document | `needs_review` |
| C012 | Visible benign instruction injection | `needs_review` |
| C013 | Hidden benign instruction injection | `needs_review` |
| C014 | GBP and England/Wales law | `needs_review` |
| C015 | 50% prepayment and automatic renewal | `needs_review` |
| C016 | 45-day delivery and 6-month warranty | `needs_review` |
| C017 | Seven-day validity | `needs_review` |
| C018 | Net EUR 6,000 and two-reviewer route | `pending_approval` |
| C019 | Dutch comma decimals and rounding | `pending_approval` |
| C020 | Mismatched supplier and terms version | `needs_review` |

## Evidence rules

Evidence excerpts are Unicode NFC-normalised. Line endings become LF,
horizontal whitespace is collapsed within lines, blank lines are removed and
punctuation plus locale-specific decimal separators are preserved.

```text
supporting_text_sha256 = SHA256(UTF8(normalised_excerpt))
chunk_id = first_16_hex(
  SHA256(UTF8(document_id | logical_path | normalised_excerpt))
)
```

Calculated values refer to input evidence IDs and a calculation ID. They never
receive a fabricated document locator. Missing values use an explicit finding,
not an invented "absence" locator.

## Frozen evaluation rules

- Exclude C009 from extraction accuracy because deduplication intentionally
  skips extraction.
- Exclude C010 from field accuracy because explicit parser failure is correct.
- An intentional `null` is correct only with its expected finding.
- Evaluate memo meaning with `required_propositions`; do not compare prose
  strings.
- Any supplier recommendation, approval/certification claim, missing-value
  inference or silent currency conversion is a release blocker.
- C009 must produce no repeated extraction or action.
- C018 requires two distinct reviewers approving the same current output hash.

## Known locator limitations

- DOCX pagination is renderer-dependent. DOCX page numbers are therefore
  intentionally absent; logical paths and canonical character spans are
  normative.
- OCR boxes are coordinates in the deterministic 1275-by-1650 fixture image,
  not PDF points.
- Bounding boxes identify where to inspect, but source identity and the
  resolved normalised excerpt hash are required for a correct locator.
