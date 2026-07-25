# Course Tools

## Generate the frozen corpus

[`generate_corpus.py`](generate_corpus.py) deterministically creates the 20
synthetic case bundles, source locators, manifest, gold answers, checksums, and
generator validation report.

```powershell
python -m pip install -r tools\requirements-corpus.txt
python tools\generate_corpus.py
python tools\generate_corpus.py --validate-only
```

The generator owns only the paths listed in [`../corpus/README.md`](../corpus/README.md).
Review and commit regenerated hashes only after an intentional source or
dependency change and a complete render/evaluation review.

## Validate the package

[`validate_package.py`](validate_package.py) checks:

- required files;
- the 12 repeated week structures;
- JSON, JSONL, YAML, and JSON Schema syntax where dependencies are installed;
- internal Markdown links;
- manifest/gold case IDs and states;
- referenced corpus hashes and byte lengths;
- C009 byte-identical duplicate semantics;
- C010 exact corrupt bytes;
- strict synthetic-data safety flags.

```powershell
python tools\validate_package.py
```

It writes `VALIDATION_REPORT.md` and exits non-zero on a structural failure.
Install the main course requirements to enable the YAML and JSON-Schema
meta-validation checks.

These scripts do not verify current internet sources, visual layout, legal
interpretation, live model quality, or the learner’s capstone. Use the
evergreen audit, render review, and weekly/acceptance tests for those.

