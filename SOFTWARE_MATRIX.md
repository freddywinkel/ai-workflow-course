# Software Matrix — Course 1

## Selection rule

Course 1 uses a small local stack so the learner can understand every
component. Tool names are implementation examples, not the professional
identity.

**Artificial intelligence (AI)** means software that can generate or classify
content but can still be wrong.

Before any real implementation, repeat the build-versus-buy assessment and
prefer the organisation's supported platform when it already meets the need.

## Required

| Tool or capability | Course role | Selection policy |
|---|---|---|
| Windows 11 | Learning workstation | Keep supported and updated |
| Visual Studio Code or plain editor | Read and edit text/code | Any editor that preserves 8-bit Unicode Transformation Format (UTF-8) is acceptable |
| Git | Inspect and version changes | Current supported release |
| Python | Comma-separated values (CSV) checks, reports, and tests | Python 3.12+; course examples target 3.13 |
| `venv` and `pip` | Isolated Python dependencies | Included with Python |
| pytest | Reproducible tests | Exact version pinned in `requirements-course.txt` |
| Browser | Course progressive web app (PWA) | Current Edge, Chrome, Safari, or Firefox |

## Optional

| Tool or capability | Course role | Boundary |
|---|---|---|
| n8n plus Node.js | Optional visual-orchestration crosswalk after the capstone passes | Not installed or required in the core path; verify and pin compatible versions before use |
| OpenAI Responses application programming interface (API) | Optional live structured-summary lab | Synthetic verified issues only; model identifier (ID) in configuration |
| Another provider with JavaScript Object Notation (JSON) Schema output | Portability comparison | Same tests and boundary |
| Power Automate / Copilot Studio | Microsoft concept crosswalk | Do not buy or configure solely for Course 1 |
| Google Workspace Studio | Google concept crosswalk | Do not buy or configure solely for Course 1 |
| Make | Orchestration comparison | Not a parallel mandatory track |
| SQLite | Optional local state extension | JSON/files are enough for required capstone |

## Explicitly deferred

These are useful later but not Course 1 prerequisites:

- FastAPI or another production web service;
- Docker Desktop;
- PostgreSQL, Supabase, or multi-tenant storage;
- Portable Document Format (PDF), Microsoft Word Open XML Document (DOCX)
  parsing, and optical character recognition (OCR);
- embeddings, vector databases, or advanced retrieval-augmented generation
  (RAG);
- Open Authorization (OAuth) production connectors;
- hosted observability platforms;
- autonomous or computer-use agents;
- infrastructure-as-code;
- Veeva or electronic quality management system (eQMS) platform
  configuration.

## Model policy

The required capstone uses an offline fixture and passes without an API key.

For the optional live lab:

- put the model name in `AI_MODEL`;
- select a currently supported model with structured output;
- record the exact model identifier and date in the evidence log;
- test a cost-appropriate model rather than automatically choosing the
  flagship;
- never rely on an alias remaining behaviourally identical;
- rerun the evaluation after a model, prompt, schema, or provider change.

## Dependency policy

`requirements-course.txt` provides the exact required offline learning
dependency. In the capstone repository:

1. create a virtual environment;
2. install the audited set;
3. run tests;
4. run `python -m pip freeze | Set-Content
   evidence\setup-dependencies.txt` to freeze the complete working
   environment;
5. inspect and commit that freeze record;
6. change one dependency group at a time;
7. rerun the regression set after every material change.

## Client portability rule

Do not sell “n8n workflows” as the outcome. Describe:

- trigger;
- validated input;
- rules;
- AI boundary;
- human decision;
- output;
- failure path;
- audit evidence;
- ownership.

Those concepts can be implemented in n8n, Microsoft, Google, Make, custom
services, or existing line-of-business software.
