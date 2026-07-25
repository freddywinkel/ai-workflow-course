# Week 10 — Evaluation-Driven Development

## Outcome

You will freeze the 20-case JSONL gold dataset and build a vendor-neutral regression runner that measures structured-field accuracy, locator correctness, memo support, state closure, policy findings, safety invariants, latency, and cost.

## Beginner checkpoint

Revisit [Python and tests](../foundations/03_CODE_AND_PYTHON.md) and JSON/JSONL
in [APIs and JSON](../foundations/04_WEB_APIS_AND_JSON.md). Before building a
runner, manually inspect one gold JSONL line and one corresponding source case.
Explain fixture, expected result, assertion, metric, threshold, regression, and
exit code.

Start with one deterministic assertion for one case. Then parameterise. Do not
accept a large generated evaluator until you can show which denominator each
metric uses and why a deliberately wrong result fails.

Safe AI-assistance request:

```text
Teach me one pytest test that reads one JSONL case and checks one required
field. Explain file reading, parsing, expected versus actual, assertion, and
failure output. Then make a deliberately wrong fixture fail. Do not implement
the full scoring runner yet.
```

## Concepts

- development, validation, and frozen test data;
- gold answer and annotation review;
- unit, integration, regression, adversarial, and human-scored tests;
- micro versus macro accuracy;
- field eligibility and intentional nulls;
- evidence-locator correctness;
- semantic proposition evaluation;
- deterministic seed and provider variability;
- baseline, threshold, regression, and release gate;
- test contamination;
- cost/latency measurement.

## Official readings

1. [pytest parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html).
2. [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html).
3. [JSON Lines format](https://jsonlines.org/) — simple format reference.
4. [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) — evaluation and risk framing.
5. [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evals) — read principles and the current hosted-platform deprecation notice; do not base the course runner on that retiring service.

Optional after the local runner passes: [Promptfoo configuration](https://www.promptfoo.dev/docs/configuration/guide/). Its report is supplementary, not authoritative.

## Guided build

### 1. Freeze and review the corpus

Copy the course `corpus/manifest.jsonl` and `corpus/golden.jsonl` into a read-only test fixture location or reference them by committed hash. Verify:

- exactly 20 unique case IDs;
- file hashes and byte lengths;
- no real personal/special-category data;
- expected state and finding codes;
- gold field types and decimal/date normalisation;
- locator excerpts/hashes;
- memo required/forbidden propositions;
- approval and duplicate contracts.

Have a second person review at least C001, C007, C008, C012, C018, and C020 if available. Record disagreements; change gold only through a reviewed commit and changelog.

Do not tune prompts by repeatedly inspecting failed frozen-test outputs. Maintain a small development set for iteration; use the frozen set at declared checkpoints.

### 2. Define metrics exactly

#### Required-field accuracy

For eligible field instances:

```text
accuracy = correct eligible field instances / all eligible field instances
```

Correct means normalised value exactly matches gold. Intentional null is correct only when null and its expected finding are present. Exclude C009 (duplicate skips extraction) and C010 (parse failure is correct).

Report:

- micro-average across all field instances;
- per-field accuracy;
- per-case accuracy;
- false-filled missing fields;
- unresolved conflicts incorrectly collapsed.

Gate: at least **90%** required-field micro-accuracy and no critical forbidden inference.

#### Evidence-locator correctness

A locator is correct only if:

- source document ID/hash is correct;
- tenant/run scope is correct;
- selector resolves;
- expected page matches when applicable;
- normalised excerpt hash matches;
- locator supports the claimed field/proposition.

```text
locator_correctness = correct required locators / all required locators
```

Gate: at least **95%**.

#### Memo grounding

For each factual proposition:

- verified evidence/calculation;
- unsupported and visibly labelled;
- prohibited/incorrect.

Gate:

- 100% factual assertions either verified or visibly unsupported;
- zero forbidden propositions;
- all case-specific required propositions/findings present.

#### Operational invariants

Report pass/fail for state closure, approval hash, idempotency, outage fallback, tenant isolation, retention/deletion, and clean reproduction. These are zero-tolerance gates, not averaged scores.

### 3. Build the runner

Parameterise tests from JSONL:

```python
@pytest.mark.parametrize("case", load_gold_cases(), ids=lambda c: c["case_id"])
def test_case(case, system_adapter):
    result = system_adapter.run_to_checkpoint(case)
    assert result.state == case["expected_checkpoint_state"]
```

Generate machine-readable `evaluation-report.json` and human-readable Markdown with:

- run ID/date/code commit;
- environment and full version tuple;
- corpus manifest/gold hashes;
- per-case outcome;
- aggregate and per-field metrics;
- evidence results;
- memo proposition results;
- invariant results;
- latency percentiles;
- token usage and estimated cost using a dated price table;
- failures and links to artifacts.

Exit non-zero if any release threshold fails.

### 4. Separate deterministic and live-model runs

Suites:

- `unit`: no network;
- `parser`: fixed local documents;
- `provider-contract`: mocked responses and errors;
- `regression-cached`: replay redacted/approved structured provider fixtures;
- `regression-live`: current configured model on synthetic corpus;
- `security`: injection, tenant, auth, mutation;
- `acceptance`: full workflow including review/action stubs.

The deterministic suite must work offline. A live-model result records non-determinism and never overwrites prior results.

### 5. Add adversarial and mutation tests

Required:

- prompt injection C012/C013;
- malicious filename;
- unknown/cross-tenant evidence ID;
- one-byte memo mutation;
- source excerpt mutation;
- duplicate and concurrent action;
- stale approval;
- missing terms/date;
- conflicting payment/supplier/version;
- wrong currency;
- arithmetic mismatch;
- locale comma/percentage rounding;
- parser/model/storage/audit outages.

Use property tests or generated variants only as supplements; keep every released failure reproducible.

### 6. Human-score review usability

For at least six cases, ask a reviewer to score:

- evidence easy to locate (1–5);
- uncertainty visible (1–5);
- proposed action clear (1–5);
- review decision confidence (1–5);
- comments/error discoveries.

Do not convert this small convenience sample into a universal usability claim. Use it to find interface defects.

### 7. Establish regression policy

Full rerun required after:

- model ID/snapshot/reasoning change;
- prompt or schema change;
- parser/OCR/canonicalisation change;
- retrieval/embedding change;
- domain calculation/policy change;
- approval/action change;
- dependency or infrastructure upgrade affecting output.

A change may improve average accuracy while breaking a zero-tolerance invariant; release remains blocked.

## Capstone increment

The capstone has a reproducible, local release gate independent of any one model provider or hosted evaluation platform. A single command produces both machine and human results and exits correctly.

## Required artifact

`artifacts/weekly/week-10/`:

- frozen manifest/gold hashes and annotation review;
- metric specification;
- local pytest regression runner;
- deterministic and live suite separation;
- JSON and Markdown reports;
- failure fixtures and adversarial results;
- six-case human review score sheet;
- regression-trigger policy;
- optional Promptfoo comparison, if used;
- weekly evidence record.

## Test gate

Pass only if:

- runner consumes all 20 unique cases;
- all successful outputs are schema-valid;
- named-state result is checked for every case;
- field and locator formulas reproduce from report counts;
- ≥90% field accuracy and ≥95% locator correctness are met;
- every factual memo assertion is supported or visibly unsupported;
- forbidden propositions and external-action violations are zero;
- deterministic suites run with network disabled;
- non-zero exit occurs for a deliberately lowered result/mutated fixture;
- full version/corpus hashes and actual usage/latency are recorded.

## Common failures

- **One aggregate score:** expose fields/cases and zero-tolerance invariants.
- **Model grades itself without evidence:** use deterministic matchers and human rubric where needed.
- **Exact prose comparison:** evaluate structured propositions and support.
- **Tuning on frozen failures:** preserve a real holdout and version gold changes.
- **Cost guessed from character count:** capture provider usage, selected region uplift, and dated prices.
- **Hosted dashboard as only record:** keep JSONL, pytest, and reports in the repository.
- **Flaky test rerun until green:** retain every attempt and investigate variability.

## Estimated time

| Activity | Time |
|---|---:|
| Readings and gold review | 1.25 h |
| Metrics and result schema | 1.5 h |
| Regression runner | 2.25 h |
| Adversarial/offline suites | 1.5 h |
| Live run and report analysis | 1.25 h |
| Human scoring and evidence | 0.75 h |
| **Total** | **8.5 h** |
