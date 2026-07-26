# Software Matrix — Course 1

## Selection rule

Course 1 uses a small local stack so the learner can understand every
component. Tool names are implementation examples, not the professional
identity.

Before any real pilot, repeat the build-versus-buy assessment and prefer the
client's supported platform when it already meets the need.

## Required

| Tool or capability | Course role | Selection policy |
|---|---|---|
| Windows 11 | Learning workstation | Keep supported and updated |
| Visual Studio Code or plain editor | Read and edit text/code | Any editor that preserves UTF-8 is acceptable |
| Git | Inspect and version changes | Current supported release |
| Python | CSV checks, reports, and tests | Python 3.12+; course examples target 3.13 |
| `venv` and `pip` | Isolated Python dependencies | Included with Python |
| pytest | Reproducible tests | Compatible current major, locked in the learner project |
| JSON Schema validator | Validate contracts | Compatible current major |
| n8n | Visual orchestration and human pause | Current stable verified by live audit; pin the selected release |
| Node.js | Local n8n runtime | A Node LTS release supported by the selected n8n version |
| Browser | n8n UI and PWA | Current Edge, Chrome, Safari, or Firefox |

## Optional

| Tool or capability | Course role | Boundary |
|---|---|---|
| OpenAI Responses API | Optional live structured-summary lab | Synthetic verified issues only; model ID in configuration |
| Another provider with JSON Schema output | Portability comparison | Same tests and boundary |
| Power Automate / Copilot Studio | Microsoft concept crosswalk | Do not buy or configure solely for Course 1 |
| Google Workspace Studio | Google concept crosswalk | Do not buy or configure solely for Course 1 |
| Make | Orchestration comparison | Not a parallel mandatory track |
| SQLite | Optional local state extension | JSON/files are enough for required capstone |

## Explicitly deferred

These are useful later but not Course 1 prerequisites:

- FastAPI or another production web service;
- Docker Desktop;
- PostgreSQL, Supabase, or multi-tenant storage;
- PDF/DOCX parsing and OCR;
- embeddings, vector databases, or advanced RAG;
- OAuth production connectors;
- hosted observability platforms;
- autonomous or computer-use agents;
- infrastructure-as-code;
- Veeva or eQMS platform configuration.

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

`requirements-course.txt` provides compatible ranges for the learning
environment. In the capstone repository:

1. create a virtual environment;
2. install the audited set;
3. run tests;
4. freeze the complete working environment;
5. commit the lock or freeze record;
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
