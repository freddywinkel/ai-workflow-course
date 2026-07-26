# Beginner Readiness Audit

Audit date: 2026-07-25  
Learning-path version audited: 1.1.0; carried into course 1.2.2 unchanged
Learner profile tested: no coding knowledge, no CLI knowledge, uses an AI
assistant for “vibe coding”

## Audit conclusion

The original 1.0.0 course was **not** a literal-beginner course. It stated that
the learner should already be comfortable with PowerShell, Git, Markdown,
JSON, YAML, `.env` files, and simple Python. Week 2 then required FastAPI,
Pydantic, HTTP, pytest, n8n, branching, and retries.

Version 1.1.0 removes that hidden prerequisite. It adds a required beginner
foundation sequence and places a prerequisite/explanation checkpoint before
the concepts in every project week.

This does not make the capstone trivial or “no-code.” It makes the learning
path explicit, slower, safer, and inspectable.

## Audit criteria and evidence

| Criterion | Evidence in version 1.1.0 | Result |
|---|---|---|
| Clear first click/order | [`README.md`](README.md#start-here) and [`foundations/README.md`](foundations/README.md) | Pass |
| No assumed CLI knowledge | [`foundations/02_COMMAND_LINE_SURVIVAL.md`](foundations/02_COMMAND_LINE_SURVIVAL.md) | Pass |
| Commands distinguished from prompts/output/file content | CLI chapter and annotated [`SETUP_WINDOWS.md`](SETUP_WINDOWS.md) | Pass |
| Safe copy/paste and stop/recovery rules | CLI chapter plus [`templates/debugging_record.md`](templates/debugging_record.md) | Pass |
| Files, paths, extensions, and text formats taught | [`foundations/01_FILES_AND_TEXT.md`](foundations/01_FILES_AND_TEXT.md) | Pass |
| First Python and test concepts taught | [`foundations/03_CODE_AND_PYTHON.md`](foundations/03_CODE_AND_PYTHON.md) | Pass |
| APIs, HTTP, JSON, auth, timeout, and retry vocabulary taught | [`foundations/04_WEB_APIS_AND_JSON.md`](foundations/04_WEB_APIS_AND_JSON.md) | Pass |
| Git/GitHub distinction, status, diff, commit, and secret safety taught | [`foundations/05_GIT_AND_SAFE_CHANGES.md`](foundations/05_GIT_AND_SAFE_CHANGES.md) | Pass |
| AI limitations, schemas, OCR, retrieval, and approval explained plainly | [`foundations/06_AI_AND_DOCUMENT_WORKFLOWS.md`](foundations/06_AI_AND_DOCUMENT_WORKFLOWS.md) | Pass |
| Vibe-coding method is bounded and test-led | [`foundations/07_SAFE_VIBE_CODING.md`](foundations/07_SAFE_VIBE_CODING.md) and [`templates/ai_assistance_log.md`](templates/ai_assistance_log.md) | Pass |
| n8n, Docker, FastAPI, PostgreSQL, Supabase, and component boundaries explained | [`foundations/08_N8N_DOCKER_AND_DATABASES.md`](foundations/08_N8N_DOCKER_AND_DATABASES.md) | Pass |
| New terminology has a lookup path | [`foundations/GLOSSARY.md`](foundations/GLOSSARY.md) | Pass |
| Each project week states what a beginner must understand first | “Beginner checkpoint” in [`weeks/`](weeks/WEEK_01.md) Weeks 1–12 | Pass |
| Beginner pace is honest | [`foundations/README.md`](foundations/README.md#beginner-pace) | Pass |

## Remaining realities

The course still requires:

- a Windows computer on which software can be installed;
- enough storage and memory for Docker, Python packages, Docling, and OCR;
- creating vendor accounts for the later live labs;
- a small, controlled API budget;
- reading technical errors and working through them;
- learning some Python, JSON, SQL, HTTP, Git, and security concepts;
- extra time beyond 8–10 hours during the first technical weeks;
- willingness to repeat a failed lab instead of accepting an AI assistant's
  unverified claim.

The course cannot responsibly turn the capstone into a click-only/no-code
exercise. Its central proof is that the learner understands and can test the
safety boundaries. A complete beginner can take the course, but must do the
foundation exercises and build in small increments.

## Learner self-check gate

Before Week 1, demonstrate each item without asking an AI assistant for the
answer:

- [ ] Show a full path, file name, and extension.
- [ ] Open PowerShell and run `Get-Location` and `Get-ChildItem`.
- [ ] Explain which text in a lesson is the command and which text is output.
- [ ] Explain how Ctrl+C is used with a local server.
- [ ] Describe what JSON object, array, string, Boolean, and null mean.
- [ ] Read a five-to-ten-line Python function and name its inputs and output.
- [ ] Run a tiny passing test, deliberately make it fail, and restore it.
- [ ] Explain request, response, endpoint, status code, timeout, and retry.
- [ ] Use `git status`, `git diff`, and `git diff --staged`.
- [ ] Explain Git versus GitHub and why `.env` must not be committed.
- [ ] Draw n8n → FastAPI → storage/database and explain each component.
- [ ] Explain why schema-valid AI output can still be factually wrong.
- [ ] Explain why document text is untrusted and approval binds to an exact
  output.
- [ ] Use the safe vibe-coding prompt for one small change and complete an AI
  assistance log.

If any box cannot be demonstrated, return to the linked foundation chapter.
There is no penalty for repeating it.

## Weekly learner check

At the start of every project week:

1. Read the outcome and beginner checkpoint.
2. Define each listed term in your own words.
3. perform the smallest pre-build exercise;
4. copy the week's safe AI-assistance request only after filling in its narrow
   goal;
5. stop if the assistant proposes a broader system than the week's increment.

At the end of every project week:

1. run the stated test gate;
2. save observed output;
3. explain one failure path;
4. explain every AI-assisted material change;
5. state what remains unverified.
