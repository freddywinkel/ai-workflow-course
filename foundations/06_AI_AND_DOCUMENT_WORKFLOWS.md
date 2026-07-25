# Foundation 6 — AI and Document Workflows in Plain Language

## Outcome

You can identify what the model, ordinary code, parser, OCR engine, database,
or human does in this course and explain why no single component is trusted on
its own.

## The model is one component

A large language model (LLM) predicts useful sequences of tokens from its
instructions and input. It can interpret varied language and draft text. It
does not look up truth automatically, understand your organisation by default,
or guarantee that a confident sentence is supported.

In this course the model may:

- propose structured commercial facts from supplied text;
- organise ambiguities and conflicts;
- draft a neutral memo from verified evidence.

It may not:

- decide which supplier wins;
- invent missing facts;
- perform arithmetic that ordinary code can verify;
- approve its own output;
- send, pay, delete, or bind the organisation.

## Prompt, context, and output

A **prompt** is the instruction and context supplied to the model. The document
text is untrusted input data, even when it contains text such as “ignore prior
instructions.”

A **token** is a piece of text used for model input and output accounting. Token
limits can truncate content. Cost and latency often grow with token usage.

A **hallucination** is plausible-looking unsupported or false output. A schema
does not prevent it.

## Structured Outputs

Structured Outputs ask the model to return data matching a declared schema:

```json
{
  "currency": "EUR",
  "total": "1210.00",
  "payment_terms_days": 30
}
```

This constrains shape. It does not prove that the document says EUR, that the
total is mathematically correct, or that the payment terms are on the cited
page. The system must separately:

1. validate the schema;
2. check arithmetic and allowed values;
3. verify cited text against the source;
4. send uncertainty or conflict to a human.

## Parsing and OCR

A parser reads structure from a digital file. OCR converts text visible in an
image into candidate machine-readable characters.

Errors differ:

- parser error: wrong reading order or table structure;
- OCR error: `8` read as `3`, missing decimal, wrong language;
- extraction error: model assigns text to the wrong field;
- calculation error: totals do not reconcile;
- retrieval error: relevant policy passage was not found;
- drafting error: memo overstates or adds a claim.

Record which component produced each derived artifact and which version it used.

## Retrieval and grounding

Retrieval selects potentially relevant source passages. Grounding means the
draft is constrained to verified facts and passages. A retrieval result is a
candidate, not proof.

An evidence locator identifies exactly where support came from, such as:

- source-document ID;
- page;
- bounding box or character span;
- hash of the supporting text.

If the text or output changes, hashes expose the mismatch.

## Deterministic and probabilistic work

**Deterministic** code should give the same result for the same input and
version. Use it for:

- SHA-256 hashes;
- arithmetic;
- state transitions;
- duplicate checks;
- exact-output approval checks;
- policy thresholds.

Model interpretation is **probabilistic**: repeated valid runs can differ.
Surround it with schemas, tests, evidence, and manual fallbacks.

## Human approval

Human approval is meaningful only if the reviewer can:

- see the proposed action;
- inspect relevant source evidence;
- see missing, conflicting, or uncertain fields;
- edit or reject;
- understand that editing invalidates the old approval;
- avoid pressure to approve quickly.

Approval binds to a hash of the exact proposed output. It is not a general
permission for whatever the workflow later generates.

## The course workflow in ordinary language

```text
receive a synthetic file
→ preserve the original and record its fingerprint
→ read its text and tables
→ ask a model for candidate facts
→ verify structure, calculations, and source support
→ draft only from verified evidence
→ let a human inspect and decide
→ perform only the exact approved draft action
→ record what happened
→ use test results to improve safely
```

## Chapter check

Explain:

- why a fluent model response is not proof;
- schema validity versus factual truth;
- parsing versus OCR versus extraction;
- retrieval result versus verified evidence;
- deterministic versus probabilistic;
- why editing an approved output requires new approval.

