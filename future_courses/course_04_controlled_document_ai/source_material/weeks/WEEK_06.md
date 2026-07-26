# Week 6 — Retrieval, Evidence Ledger, and Grounded Drafting

## Outcome

You will retrieve relevant purchasing-policy clauses, assemble a verified evidence ledger, and generate a neutral review memo in which every factual proposition has verified support or a visible unsupported marker.

## Beginner checkpoint

Revisit retrieval, grounding, and evidence in
[AI and document workflows](../foundations/06_AI_AND_DOCUMENT_WORKFLOWS.md).
Be able to explain that retrieval selects candidates, verification establishes
support, and drafting must not silently bridge a missing fact.

Start with deterministic section lookup against the short supplied policy. Do
not add embeddings or a vector database merely because an assistant proposes
them. For each memo sentence, point to its evidence-ledger entry or the visible
unsupported marker.

Safe AI-assistance request:

```text
Help me implement deterministic policy-section lookup before vector retrieval.
Use stable section IDs and return no result when support is absent. Explain the
data shape and add tests for exact match, no match, and a misleading near
match. Do not generate a memo yet.
```

## Concepts

- retrieval corpus and policy version;
- lexical, metadata-filtered, and vector retrieval;
- chunking and stable clause IDs;
- precision, recall, and “not retrieved” failure;
- evidence ledger;
- fact, derived calculation, policy rule, and interpretation;
- claim-level citation;
- unsupported assertion;
- semantic memo contract rather than exact wording;
- deterministic rendering;
- retrieval and generation separation.

## Official readings

1. [PostgreSQL full-text search](https://www.postgresql.org/docs/current/textsearch.html).
2. [Supabase pgvector columns](https://supabase.com/docs/guides/ai/vector-columns) — optional after lexical baseline.
3. [OpenAI File Search](https://developers.openai.com/api/docs/guides/tools-file-search) — comparison only; inspect what annotations provide and why the capstone retains its own page/span ledger.
4. [OpenAI citation-formatting guidance](https://developers.openai.com/api/docs/guides/citation-formatting) — use as output-design input, not evidence verification.
5. [Pydantic validators](https://docs.pydantic.dev/latest/concepts/validators/) — enforce memo structures.

The internal policy is short. A deterministic clause-ID or lexical lookup may be better than embeddings. Complexity needs measured benefit.

## Guided build

### 1. Version the policy corpus

Ingest the supplied Dutch or English policy as a source document. For each `P-01` through `P-14`:

- preserve source hash and policy version;
- extract exact clause text;
- assign stable clause ID;
- retain page/span/bbox;
- calculate supporting-text hash;
- store language and effective date;
- mark status as active/superseded.

Never silently mix clauses from different policy versions.

### 2. Build a lexical baseline

Map observed facts/finding types to policy search queries. Examples:

- payment or prepayment → `P-04`;
- delivery/warranty → `P-05`;
- validity → `P-06`;
- approval count → `P-07`;
- document mismatch → `P-08`;
- law/renewal → `P-09`;
- evidence rule → `P-10`;
- embedded instruction → `P-11`.

For this 14-clause policy, a deterministic finding-code-to-clause map is an excellent baseline. Add PostgreSQL lexical search for exploratory queries and record top-k results.

### 3. Evaluate retrieval before generation

Create query fixtures:

```text
query_id | observed fact/finding | expected clause IDs | forbidden version
```

Measure:

- recall@k: was every required clause retrieved?
- precision@k: how many retrieved clauses are relevant?
- wrong-version rate;
- cross-tenant leakage;
- no-result handling.

If lexical/mapped retrieval already reaches the declared gate, pgvector is optional. If you add embeddings, store embedding model/config/version and rerun the exact queries.

### 4. Construct the evidence ledger

One row per usable evidence item:

```text
evidence_id
run_id / tenant_id
evidence_type: source_fact | policy_clause | calculation
source_id + source_sha256
chunk_id + page/bbox/span
supporting_text_sha256
normalised value
verification status and timestamp
parser/policy/calculation version
```

Calculations reference their input evidence IDs and formula version; they do not pretend to be quotations from a document.

Reject ledger entries when:

- locator cannot resolve;
- support hash differs;
- source is wrong tenant/version;
- cited value is not present under declared normalisation;
- policy is superseded;
- calculation inputs are incomplete.

### 5. Define a memo schema

Use structured sections:

```text
case identity
documents reviewed
commercial facts
deterministic calculations
policy checks
conflicts and missing information
questions for human review
limitations
```

Each assertion object contains:

```json
{
  "proposition": {
    "subject": "Q-C008-2026",
    "predicate": "declared_total_inc_vat",
    "object": {"currency": "EUR", "amount": "2803.00"}
  },
  "display_text": "The quotation declares a total of EUR 2,803.00.",
  "evidence_ids": ["E-..."],
  "support_status": "verified"
}
```

Allowed support status:

- `verified`;
- `derived_verified`;
- `unsupported_needs_review`.

The model must not emit `verified`; code assigns it after resolving evidence.

### 6. Generate and verify the draft

Supply only:

- validated extraction values;
- conflicts/findings;
- verified evidence IDs with short excerpts;
- retrieved active policy clauses;
- memo schema and neutral writing instructions.

After generation:

1. parse schema;
2. verify every evidence ID;
3. compare proposition object with normalised evidence/calculation;
4. reject prohibited propositions;
5. label unsupported assertions;
6. deterministically render Markdown/HTML/PDF;
7. hash the exact proposed output bytes.

Prohibited propositions include `supplier_recommended`, `supplier_approved`, `supplier_certified`, invented exchange rates, inferred missing terms, or blanket legal compliance.

### 7. Test hard cases

Use:

- C007: display both payment terms and conflict; choose neither;
- C008: display declared total, calculated total, and exact discrepancy;
- C011: say terms are missing; do not infer law/renewal/version;
- C014: preserve GBP; do not convert;
- C020: identify mismatch and do not apply unrelated terms.

Add a mutation test: alter one stored source excerpt after ledger creation. The support hash must fail and the memo cannot progress.

## Capstone increment

The capstone produces a deterministic, hashable proposed review memo with evidence links. Clean cases may reach `pending_approval`; unresolved cases remain `needs_review`. No email or external draft is created yet.

## Required artifact

`artifacts/weekly/week-06/`:

- policy clause index and version record;
- retrieval query set and measured report;
- decision record on whether pgvector is justified;
- evidence-ledger schema and sample;
- memo JSON Schema;
- versioned drafting prompt;
- claim/evidence validator;
- rendered memos for five hard cases;
- unsupported/prohibited proposition tests;
- source-mutation test;
- weekly evidence record.

## Test gate

Pass only if:

- retrieval finds every required policy clause in the test query set;
- wrong-version and cross-tenant policy passages are rejected;
- every factual memo proposition resolves to verified evidence, a verified calculation, or `UNSUPPORTED — NEEDS REVIEW`;
- policy findings cite both observed fact and policy clause;
- C007, C008, C011, C014, and C020 follow their golden semantic rules;
- no memo selects or recommends a supplier;
- evidence mutation invalidates support;
- exact rendered bytes are hashed and stored;
- retrieval/model configuration and versions are recorded.

## Common failures

- **Vector database by default:** start with the 14-clause deterministic/lexical baseline.
- **Citation appended to a paragraph of multiple facts:** use proposition-level links.
- **Calculation given a fake page citation:** reference formula plus source evidence inputs.
- **Page link without hash verification:** locator correctness includes source and text.
- **Memo evaluated by exact prose:** compare semantic propositions and forbidden claims.
- **Old policy mixed with new:** filter on active version before retrieval.
- **Unsupported text quietly removed:** visible rejection/marker makes failure reviewable.

## Estimated time

| Activity | Time |
|---|---:|
| Retrieval readings and policy indexing | 1.25 h |
| Baseline retrieval and evaluation | 1.5 h |
| Evidence ledger | 1.5 h |
| Memo schema/generation | 1.75 h |
| Claim verification and hard-case tests | 2.0 h |
| Evidence packaging | 0.75 h |
| **Total** | **8.75 h** |
