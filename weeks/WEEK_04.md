# Week 4 — Document Parsing, OCR, and Page-Level Provenance

## Outcome

You will build a versioned parsing pipeline for PDF and DOCX sources, including tables and a scanned document. It will preserve page/region/span provenance, measure OCR/parsing quality, and turn corrupt or unsupported input into visible safe states.

## Beginner checkpoint

Revisit the parsing/OCR and evidence-locator sections of
[AI and document workflows](../foundations/06_AI_AND_DOCUMENT_WORKFLOWS.md).
Before building, explain the difference between a born-digital PDF, an
image-only scan, parsing, OCR, reading order, and an evidence locator.

Begin with one known-good digital PDF. Save and inspect its derived output
before adding DOCX, tables, scans, or corrupt inputs. If a generated parser
wrapper is more than one screenful, ask the assistant to split it into named,
tested functions.

Safe AI-assistance request:

```text
Help me inspect one Docling result from one supplied synthetic PDF. First show
how to print only page count and a short text preview. Explain the result
objects in plain language. Do not add OCR, storage, chunking, or model calls
until this smoke test passes.
```

## Concepts

- born-digital versus image-only PDF;
- document object model and reading order;
- OCR engine, language, confidence, and quality;
- tables as structure rather than flattened prose;
- canonical derived text;
- page and bounding-box coordinate systems;
- stable chunk IDs and supporting-text hashes;
- parser/model/version provenance;
- partial parse versus failed parse;
- golden parser fixtures.

## Official readings

1. [Docling installation and OCR engines](https://docling-project.github.io/docling/getting_started/installation/).
2. [Docling supported formats](https://docling-project.github.io/docling/usage/supported_formats/).
3. [Docling full-page OCR example](https://docling-project.github.io/docling/_generated/examples/full_page_ocr/).
4. [Docling Document concepts](https://docling-project.github.io/docling/concepts/docling_document/).
5. [Docling confidence scores](https://docling-project.github.io/docling/concepts/confidence_scores/).
6. [PDF specification landing page at the PDF Association](https://pdfa.org/resource/iso-32000-pdf/) for context; you do not need to study the specification.

Docling supports multiple formats and OCR engines, but support is not proof of correct extraction on your files. Your frozen cases and locators are the acceptance authority.

## Guided build

### 1. Define a parser adapter

Use a provider-neutral interface:

```python
class ParserAdapter(Protocol):
    def parse(self, source: SourceDocument) -> ParsedDocument: ...
```

`ParsedDocument` should include:

- source ID and source SHA-256;
- parser and OCR engine versions;
- started/completed times;
- page count;
- canonical text and hash;
- ordered blocks;
- tables with cells/row/column relationships;
- per-block page, bounding box, and/or character span;
- quality signals and warnings;
- `succeeded`, `partial`, or `failed`.

Do not make Docling classes your domain contract. Translate them at the adapter boundary.

### 2. Create canonicalisation rules

Document rules for:

- Unicode normalisation;
- line endings;
- whitespace;
- soft hyphens and line-break hyphenation;
- decimal commas versus decimal points;
- currency symbols;
- page separators;
- headers/footers;
- table serialization;
- Dutch and English text;
- supporting-text hash normalisation.

Changing canonicalisation changes evidence hashes. Version and retest it.

### 3. Parse born-digital PDF and DOCX

For selected corpus files:

1. load bytes from the authorised storage path;
2. verify source hash again;
3. invoke Docling;
4. map document blocks into your contract;
5. preserve page and bounding-box provenance where available;
6. serialize canonical text and structured tables to derived storage;
7. store derivative hashes and parser version;
8. transition `validated → parsed` only after persistence succeeds.

Manually compare:

- supplier name and header;
- every line-item row;
- subtotal/VAT/total labels and values;
- terms clauses;
- page numbers and region locations.

### 4. Parse a scan

Select the designated scan case. Configure OCR explicitly for Dutch/English as required. Record:

- OCR engine and model/language data version;
- CPU/GPU mode;
- page count;
- duration;
- quality/confidence signals;
- characters/words that differ from the readable source;
- whether tables remain structurally usable.

Define a threshold that causes `needs_review`, such as a failed anchor-field check, unreadable totals, missing page, or low measured character accuracy. Do not rely on an unexplained average confidence alone.

### 5. Create stable evidence locators

Generate `chunk_id` from stable inputs:

```text
SHA256(source_id | parser_version | canonicalisation_version | block_sequence)
```

For a table fact, retain:

- table/page ID;
- row/column address;
- bounding box when available;
- canonical text span;
- supporting-text hash.

Create a locator viewer or simple debug endpoint that displays the source page, highlights a bounding box or prints the text span, and shows the recomputed support hash. The reviewer will reuse it in Weeks 6 and 7.

### 6. Handle bad inputs

Run:

- corrupt PDF;
- password-protected PDF if provided/created locally;
- truncated DOCX copy;
- image-only scan;
- file with blank page;
- rotated scan;
- unexpected but syntactically valid layout.

Classify:

- permanent unsupported/corrupt → `failed_manual`;
- usable but incomplete/low-quality → `needs_review`;
- transient worker/OCR dependency failure → retry cap, then `failed_manual`;
- successful parse → `parsed`.

Persist a safe diagnostic code and version metadata, not a full raw parser exception exposed to the reviewer.

### 7. Build parser regression tests

For a small parser fixture set, assert:

- page count;
- required anchor text;
- table row/column count;
- exact known values;
- locator resolves;
- support hash matches;
- corrupt input yields the declared state;
- source bytes remain unchanged.

Keep parser tests independent from model calls.

## Capstone increment

All supported corpus inputs can now produce versioned derived representations. At minimum demonstrate:

- one normal PDF;
- one DOCX;
- one table-heavy quotation;
- one Dutch text case;
- one English case;
- one scan;
- one corrupt input;
- one embedded prompt-injection string preserved as document text.

The parser must not interpret an embedded instruction. Store it as untrusted content and mark the case for Week 9’s security test.

## Required artifact

`artifacts/weekly/week-04/`:

- parser adapter contract;
- canonicalisation specification and version;
- parser/OCR configuration;
- derived JSON and text samples with hashes;
- locator-debug screenshots or outputs;
- scan quality report;
- corrupt/partial/failure matrix;
- parser regression test report;
- manual comparison checklist;
- weekly evidence record.

## Test gate

Pass only if:

- source hashes before and after parsing match;
- PDF and DOCX facts retain resolvable locators;
- the table fixture retains row/column meaning;
- the scan reaches `parsed` or a justified visible `needs_review`;
- corrupt input never causes an unnamed/crashed run;
- parser and OCR versions are stored;
- supporting text hashes can be recomputed;
- changing canonicalisation invalidates the relevant derived/evidence version;
- the embedded malicious sentence remains data and triggers no behaviour;
- manual spot-check results and known limitations are recorded.

## Common failures

- **Flattening tables too early:** preserve cell structure and headers before serialising text.
- **Page number with no exact support:** add region/span and a hash.
- **OCR confidence treated as truth:** validate anchor fields and compare known scan text.
- **Derived output overwrites source:** use separate immutable/versioned paths.
- **Parser upgrade without corpus rerun:** parser and canonicalisation changes can silently break evidence.
- **Docling object leaked through every layer:** map to the portable contract.
- **Corrupt input throws through n8n:** catch, classify, persist, and route visibly.

## Estimated time

| Activity | Time |
|---|---:|
| Docling/OCR readings and examples | 1.25 h |
| Adapter and canonicalisation | 1.75 h |
| PDF/DOCX/table parsing | 2.0 h |
| OCR case and quality review | 1.5 h |
| Locators and viewer | 1.25 h |
| Failure/regression tests and evidence | 1.25 h |
| **Total** | **9.0 h** |
