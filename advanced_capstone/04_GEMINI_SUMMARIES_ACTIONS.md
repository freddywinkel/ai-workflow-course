# Capstone Lab 4 — Let Gemini Select, Then Let Fixed Code Write

## Outcome

You will see exactly what Gemini is allowed to select in this demonstration and
how fixed application code creates the wording shown to the reviewer. You will
first inspect a worked synthetic example. Then you will repeat the review with
a different synthetic document that contains an instruction-injection attempt.

Gemini is a generative artificial intelligence (AI) model. In this demo it
returns only one to three candidate identifiers for the summary, one
human-review action type already permitted by fixed findings, and one or two
candidate identifiers supporting that action. It does **not** write the
displayed summary or action sentence. Fixed Python code renders that exact
wording from verified values and templates.
Gemini may not approve a supplier, contact anyone, send anything, make a
payment, certify compliance, or update another system.

## The three layers of control

1. Fixed code gives Gemini only already-extracted fields, exact evidence
   quotes, and temporary candidate identifiers. It does not send the whole
   Portable Document Format (PDF) file.
2. Fixed findings narrow the permitted action type before the request. Gemini
   must answer with structured JavaScript Object Notation (JSON) containing
   only allowed candidate identifiers and that bounded action type.
3. Fixed code maps those identifiers back to verified fields and evidence,
   writes each summary sentence itself, inserts one exact action template, and
   rejects any unknown selection, changed wording, finding conflict, or action
   citation linked to the wrong kind of source field before human review.

The cloud configuration uses `gemini-3.5-flash-lite` through the current
Gemini Enterprise Agent Platform application programming interface (API),
previously called the Vertex AI API, in the European Union (`eu`) location. Do
not replace it with Gemini 2.5 Flash or Gemini 2.5 Flash-Lite: Google currently
lists their retirement as 16 October 2026.

## Follow along — I show you exactly how

### Step 1 — Return to the local practice copy

Open Windows PowerShell and run:

```powershell
$capstoneRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'AI-workflow-learning\controlled-intake-capstone'
$demoRoot = Join-Path $capstoneRoot 'demo'
Set-Location -LiteralPath $demoRoot
& .\.venv\Scripts\Activate.ps1
$env:PROVIDER_MODE = 'fake'
```

This keeps the exercise offline. No Google service or cloud credit is used.

### Step 2 — Read the exact model boundary

Run:

```powershell
notepad .\src\controlled_intake\providers.py
notepad .\src\controlled_intake\pipeline.py
notepad .\src\controlled_intake\schemas.py
```

In `providers.py`, find:

- `GEMINI_SELECTION_RESPONSE_SCHEMA`;
- the sentence beginning `Select one to three candidate identifiers`;
- the instruction `Return identifiers and an action_type only; do not write
  prose`;
- the instruction that the model has no tools and no authority;
- `enterprise=True` and `location=self._settings.vertex_location`;
- the model-call timeout;
- `response_mime_type="application/json"`; and
- `response_schema=response_schema`, with candidate identifiers inserted from
  the verified evidence set;
- `ACTION_EVIDENCE_FIELD_ALLOWLISTS`, which limits the source-field types that
  may support each review action;
- the loop that renders `The source records ...` from the selected field; and
- `ACTION_INSTRUCTION_TEMPLATES`, which supplies the exact review wording.

In `pipeline.py`, find:

- `_allowed_action_types`, which narrows action choices from fixed findings;
- `UNSUPPORTED_SOURCE_REFERENCE`;
- `MODEL_ACTION_CONFLICTS_WITH_FINDINGS`;
- `MODEL_ACTION_EVIDENCE_MISMATCH`;
- `FORBIDDEN_MODEL_CLAIM`; and
- `FORBIDDEN_DRAFT_PATTERNS`.

Close the files without changing them.

### Step 3 — Make the worked control record

Run:

```powershell
$lessonFolder = Join-Path $capstoneRoot 'evidence\gemini-boundary'
New-Item -ItemType Directory -Force -Path $lessonFolder | Out-Null
notepad (Join-Path $lessonFolder 'worked_c001_model_boundary.md')
```

Paste this worked example, save it, and close Notepad:

```markdown
# Worked C001 Gemini boundary

Input to Gemini:
- extracted values that already have evidence links;
- exact quotes indexed by known evidence identifiers.

Allowed output:
- one to three allowed candidate identifiers for summary content;
- one human-review action type from the fixed finding boundary;
- one or two candidate identifiers whose field type supports that action;
- no prose.

Independent checks after Gemini:
- the JSON matches the application schema;
- every selected candidate identifier exists;
- fixed code renders the exact source-linked summary wording;
- fixed code inserts the exact allowed action template;
- fixed code rejects an action that conflicts with findings or cites an
  unrelated field;
- changed action wording and forbidden authority language are rejected;
- a human decision is still required.

Gemini authority: NONE
External action: NONE
Data: frozen synthetic course document only
```

### Step 4 — Run four model-boundary attacks

Run:

```powershell
python -m pytest .\tests\test_pipeline.py -k "unknown_model_evidence or forbidden_model_action or action_cannot_cite or action_type_cannot" -vv
```

Expected result: all four selected tests pass.

These tests attack the provider-independent safety boundary. The first test
deliberately supplies a made-up evidence identifier and the application stops
with `UNSUPPORTED_SOURCE_REFERENCE`. The second supplies approval/send wording
and the application stops with `FORBIDDEN_MODEL_CLAIM`. The other two prove
that an action cannot cite an unrelated field or contradict fixed findings.
The real Google adapter is narrower still: Gemini returns candidate
identifiers and a finding-bounded action type, while the application writes
the prose.

Record the result:

```powershell
python -m pytest .\tests\test_pipeline.py -k "unknown_model_evidence or forbidden_model_action or action_cannot_cite or action_type_cannot" -vv |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_model_boundary_tests.txt')
if ($LASTEXITCODE -ne 0) { throw 'The worked model-boundary tests failed.' }
```

### Step 5 — Test the Google adapter without calling Google

Run:

```powershell
python -m pytest .\tests\test_providers.py -vv |
    Tee-Object -FilePath (Join-Path $lessonFolder 'worked_google_adapter_contract.txt')
if ($LASTEXITCODE -ne 0) { throw 'The Google adapter contract tests failed.' }
```

These tests replace the network clients with controlled test doubles. They
prove the pinned software development kit can express the Enterprise,
European Union, timeout, structured-output, no-tools, and Document AI
processor contract without spending cloud credit.

### Step 6 — Observe the harmless app-rendered draft

Start the local application as in Lab 1:

```powershell
python -m uvicorn controlled_intake.main:app --app-dir .\src --host 127.0.0.1 --port 8080 --no-access-log
```

In a second PowerShell window run:

```powershell
Start-Process 'http://127.0.0.1:8080'
```

Process the frozen C001 quotation. Inspect each summary statement and follow
each evidence identifier to its exact quote. Notice that the wording follows
the same fixed `The source records ...` pattern and the action matches one
template in `ACTION_INSTRUCTION_TEMPLATES`. Its citation must also point to a
field permitted by `ACTION_EVIDENCE_FIELD_ALLOWLISTS`. This step is still in
fake mode: the offline adapter chose the content and no Gemini call occurred.
In Google mode, Gemini chooses bounded candidate identifiers and fixed
application code writes the displayed sentences. Do not record an approval in
this lesson. Close the browser tab and press `Ctrl+C` in the server window.

## Now recreate it yourself

Use the same local application with:

```text
source_material\corpus\cases\C012\quotation.pdf
```

This is a different, still entirely synthetic, case containing a visible
instruction that tries to influence the system.

Before processing, create:

```powershell
notepad (Join-Path $lessonFolder 'recreated_c012_model_boundary.md')
```

Write your prediction for:

- the expected workflow state;
- the finding code;
- whether the document instruction may change the model's authority;
- whether an external action may occur; and
- whether you expect an approved export.

Process C012 locally. Compare the result with your prediction. Add:

- the observed state;
- `UNTRUSTED_INSTRUCTION_DETECTED` if observed;
- one evidence identifier used by a safe statement;
- whether that identifier really exists in the evidence list;
- which fixed action template was displayed;
- why the displayed wording did not come from free-form model prose;
- why document instructions are data, not commands; and
- your decision. Choose `Needs correction`, not approval.

Do not change the prompt, source code, manifest, test, or expected result.

## Ask Codex to check your work

Run:

```powershell
(Resolve-Path $lessonFolder).Path
```

Insert the returned path and send Codex:

```text
READ-ONLY GEMINI-BOUNDARY REVIEW.

I authorize inspection of only this full folder:
[PASTE FULL PATH]

Do not edit, create, delete, rename, move, upload, install, or call a cloud
service. Stop if you find credentials, real client/work data, personal data,
or health data.

Check the worked C001 explanation, both saved test outputs, and my recreated
C012 explanation. Return PASS or NOT YET for: Gemini returns candidate
identifiers and one finding-bounded action type rather than prose; fixed
application code renders exact summary and action wording; structured JSON
boundary; Enterprise European Union adapter contract; known-evidence
requirement; action citations limited to relevant field types;
unsupported-reference safe stop; forbidden-action safe stop; C012 instruction
treated as untrusted data; human authority retained; no external action;
synthetic-only data; learner wording is meaningfully different from the worked
example. Cite the local filename for each conclusion.
```

## Pass criteria

- All four selected model-boundary tests pass.
- Every offline Google-adapter contract test passes without a cloud call.
- You can explain what Gemini receives and what it never receives.
- You can explain that Gemini selects candidate identifiers and fixed code
  writes the exact displayed summary and action wording.
- Every accepted statement and proposed action cites known evidence.
- Fixed findings bound the action type, and the action cites a permitted field
  type rather than arbitrary evidence.
- Unknown citations and forbidden authority claims stop safely.
- C012 remains a human-review case.
- Nothing is sent, approved, paid, selected, or updated automatically.
- Only synthetic course material was used.
- Codex returns PASS.

## Stop conditions

Stop if a real document is proposed, a model citation cannot be resolved, the
model appears to have authority, or someone suggests weakening the independent
checks. Never activate paid billing for this lesson.

## Current official Google references

- [Gemini 3.5 Flash-Lite model details](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-5-flash-lite)
- [Gemini model lifecycle and retirement dates](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions)
- [Structured output on Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output)
- [How Google Cloud handles generative AI data](https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/zero-data-retention)
