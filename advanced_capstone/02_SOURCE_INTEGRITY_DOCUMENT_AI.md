# Capstone Lab 2 — Protect the Source and Bound Document AI

## Outcome

You will understand and test the exact boundary before Google Document AI is
allowed to perform optical character recognition (OCR). You will prove that an
unknown hash, wrong media type, oversized document, too many pages, or corrupt
file stops before a provider call.

## Why the hash allowlist matters

A checkbox saying “synthetic” can be wrong. This demo also calculates Secure
Hash Algorithm 256-bit (SHA-256) and compares it with a reviewed six-file
manifest. One changed byte creates a different hash.

The live adapter then uses:

- processor type: Enterprise Document OCR;
- processor location: `eu`;
- endpoint: `eu-documentai.googleapis.com`;
- synchronous `RawDocument` call;
- maximum three pages and 5 megabytes;
- no Google Cloud Storage bucket.

The source bytes exist only in the incoming request and a short-lived Cloud Run
memory-backed temporary file. The application deletes that file in `finally`,
which means cleanup runs on success and on failure.

## Follow along — I show you exactly how

### Step 1 — Inspect the six allowed hashes

In the activated local practice environment:

```powershell
Set-Location -LiteralPath $demoRoot
Get-Content .\fixtures\manifest.json
```

Write down the six case identifiers. Do not write down a billing identifier or
credential.

### Step 2 — Verify C001 yourself

```powershell
$c001 = Join-Path $courseRoot 'future_courses\course_04_controlled_document_ai\source_material\corpus\cases\C001\quotation.pdf'
$hash = (Get-FileHash -LiteralPath $c001 -Algorithm SHA256).Hash.ToLowerInvariant()
$hash
Select-String -Path .\fixtures\manifest.json -Pattern $hash
```

Expected result: a 64-character hash and one manifest match.

### Step 3 — Run the boundary tests

```powershell
python -m pytest .\tests\test_pipeline.py -k 'unknown_hash or media_type or corrupt or deletes_temporary'
```

Expected result: all selected tests pass.

Read these files without editing:

```powershell
notepad .\src\controlled_intake\fixtures.py
notepad .\src\controlled_intake\security.py
notepad .\src\controlled_intake\pipeline.py
```

Find the order:

1. allowlist match;
2. PDF type/size/page validation;
3. usage reservation;
4. temporary file creation;
5. provider call;
6. deletion in `finally`.

### Step 4 — Reproduce the corrupt safe stop

Start the local app as in Lab 1. Select:

```text
source_material\corpus\cases\C010\quotation_corrupt.pdf
```

Expected result:

```text
PARSER_CORRUPT_FILE
```

The corrupt file is deliberately on the synthetic allowlist so the parser
failure path can be tested. No Document AI or Gemini call occurs.

## Now recreate it yourself

Make a changed copy of C001 **only in your practice evidence folder**:

```powershell
$recreatedFolder = Join-Path $capstoneRoot 'evidence\source-boundary-recreated'
New-Item -ItemType Directory -Force -Path $recreatedFolder | Out-Null
$changedCopy = Join-Path $recreatedFolder 'changed-synthetic-c001.pdf'
Copy-Item -LiteralPath $c001 -Destination $changedCopy
Add-Content -LiteralPath $changedCopy -Value 'one deliberate changed byte'
Get-FileHash -LiteralPath $changedCopy -Algorithm SHA256
```

Upload the changed copy locally. Predict and observe
`SYNTHETIC_ALLOWLIST_REJECTED`.

Do **not** add its hash to the manifest. Delete nothing; keep it as evidence
that one changed byte is rejected.

Create `recreated_boundary.md` with:

- original hash;
- changed-copy hash;
- observed safe-stop code;
- whether a provider call occurred;
- why a filename or checkbox alone is weaker.

Do not paste document content.

## Ask Codex to check your work

```text
READ-ONLY SOURCE-INTEGRITY REVIEW.

Inspect only this full practice folder:
[PASTE FULL PATH]

Do not edit, delete, rename, upload, or call any cloud service. Do not inspect
outside the folder. Stop for credentials or real data.

Return PASS or NOT YET for:
- original and changed SHA-256 values are different and 64 hexadecimal chars;
- recreated_boundary.md records SYNTHETIC_ALLOWLIST_REJECTED;
- the changed hash was not added to the allowed manifest;
- C010 records PARSER_CORRUPT_FILE;
- the written order places all checks before provider calls;
- deletion is described for success and failure;
- no document content or personal data was copied into evidence.
```

## Pass criteria

- The allowlist and corrupt-file tests pass.
- The changed C001 copy is refused.
- The original frozen file remains unchanged.
- The `eu` endpoint and synchronous call are correctly explained.
- Temporary deletion is proved in the test suite.
- Codex returns PASS.

## Stop conditions

Never “fix” a rejected real or changed file by adding its hash. A new synthetic
fixture requires a generator, documented review, expected outputs, and a
separate manifest revision.
