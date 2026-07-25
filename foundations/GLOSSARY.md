# Beginner Glossary

Use this as a lookup page. Definitions are deliberately plain and specific to
the course.

## Files, code, and tools

**Argument** — a value passed to a command or function.

**Boolean** — a value that is either true or false.

**CLI (command-line interface)** — a text interface for giving a program exact
commands.

**Code** — precise instructions written in a programming language.

**Code fence** — the three-backtick Markdown wrapper used to display code. The
backticks and language label are not part of a copied command.

**Command** — one instruction entered into a terminal.

**Configuration** — settings that alter behaviour without changing core code.

**Dependency** — another package or service that the project relies on.

**Dictionary / object** — named keys mapped to values.

**Environment variable** — a named value supplied to a running program, often
used for configuration or secrets.

**Exception** — a Python error raised while code is running.

**File extension** — the suffix such as `.py`, `.json`, or `.md` that indicates
a file's format or purpose.

**Function** — a named reusable unit of code with inputs, behaviour, and output.

**List / array** — an ordered sequence of values.

**Markdown** — a plain-text documentation format using simple markers for
headings, lists, links, and emphasis.

**Module** — a Python file or library component that can be imported.

**Null / `None`** — an explicit absence of a value; not zero or an empty string.

**Package** — installable software or a collection of code modules.

**PATH** — the operating-system list of folders searched for executable
programs.

**Path** — a file or folder address.

**PowerShell** — the Windows command shell used by this course.

**Prompt (terminal)** — the terminal text showing it is ready for a command.
This differs from an AI prompt.

**Python** — the programming language used for the capstone's tested domain
logic.

**Runtime** — the program/environment that executes code.

**Script** — a file containing commands or code intended to run.

**String** — text data.

**Syntax** — the formal grammar of a language or data format.

**Terminal** — the window that hosts a command-line shell such as PowerShell.

**Type** — a category of value such as string, integer, Boolean, or date.

**Variable** — a name referring to a value.

**Virtual environment** — an isolated set of Python packages for one project.

**YAML** — an indentation-sensitive text configuration format.

## Web and APIs

**API** — an agreed interface through which software components make requests
and receive responses.

**API key** — a secret credential used by software to authenticate.

**Authentication** — verifying who or what is making a request.

**Authorization** — deciding what an authenticated identity may do.

**Client** — software that sends a request.

**Endpoint** — a method and path exposed by an API.

**FastAPI** — the Python web framework used for the local domain API.

**Header** — request/response metadata such as content type or authentication.

**HTTP** — the protocol commonly used for API requests and responses.

**JSON** — a strict text format for objects, arrays, strings, numbers, Booleans,
and null.

**JSONL** — JSON Lines: one complete JSON value per line.

**Localhost** — the current computer as a network host, commonly
`127.0.0.1`.

**Method** — an HTTP action label such as GET or POST.

**Port** — a numbered network door used to reach one service on a host.

**Request** — a message from a client asking a server to do something.

**Response** — the server's answer to a request.

**SDK** — a vendor-provided software development kit that wraps an API for a
programming language.

**Server** — software that listens for requests and returns responses.

**Status code** — a three-digit HTTP result category such as 200, 404, or 500.

**Timeout** — the client stopped waiting; it does not prove the server performed
no action.

**URL** — an address identifying a web or API resource.

**Webhook** — an HTTP endpoint called automatically when an event occurs.

## AI and documents

**AI literacy** — sufficient understanding to use, supervise, question, and
stop an AI system appropriately.

**Bounding box** — coordinates identifying a rectangular region on a page.

**Chunk** — a bounded passage of source text used for retrieval or processing.

**Confidence** — a component's estimate or signal about uncertainty; it is not
proof of correctness.

**Context** — information supplied to a model for one request.

**Embedding** — a numeric representation used to compare semantic similarity.

**Evidence locator** — a precise pointer from a claim to supporting source
content.

**Extraction** — turning source content into named fields or facts.

**Grounding** — restricting a result to supplied and verified source evidence.

**Hallucination** — plausible-looking model output that is false or unsupported.

**Inference** — running a trained model to produce an output.

**LLM (large language model)** — a model that generates and interprets text by
predicting token sequences.

**Model** — the trained computational component that maps input to candidate
output.

**OCR** — optical character recognition: converting visible image text into
candidate machine-readable characters.

**Parser** — software that reads a file's text and structural elements.

**Prompt (AI)** — instructions and context sent to a model.

**Prompt injection** — untrusted content attempting to alter the model or
workflow's instructions.

**Provenance** — the recorded origin and transformation history of data.

**Refusal** — a model response declining to produce the requested result.

**Retrieval** — selecting potentially relevant passages from a source
collection.

**Schema** — a machine-readable definition of allowed data structure and types.

**Structured Outputs** — model output constrained to a declared schema; this
constrains shape, not truth.

**Token** — a piece of text used in model input/output limits and pricing.

## Workflow and safety

**Approval** — a recorded human decision about an exact proposed output.

**Audit event** — a structured record of a significant system event.

**Circuit breaker** — a control that temporarily stops calls after repeated
failures.

**Control point** — a place where a rule, test, or reviewer can stop progress.

**Dead-letter/manual route** — a visible destination for work automation cannot
complete safely.

**Deterministic** — expected to produce the same result for the same input and
version.

**Hash** — a fixed-size fingerprint of bytes; changing the bytes changes the
fingerprint with overwhelming probability.

**Human in the loop** — a person performs a meaningful review or decision
inside the process, not merely a decorative click.

**Idempotency** — repeated equivalent attempts produce one intended effect
rather than duplicates.

**Immutable** — not altered after creation; corrections become new versions.

**Invariant** — a condition that must always remain true.

**Kill switch** — a control that disables a capability or action path.

**Manual fallback** — a documented non-automated way to complete or safely stop
work when the system fails.

**Probabilistic** — output may vary and is described in terms of likelihood,
not certainty.

**Reason code** — a stable machine-readable label explaining a result or
failure.

**Retry** — another attempt after a declared temporary failure.

**State** — one named stage of a workflow run.

**State machine** — named states plus rules for allowed transitions.

**Trace ID** — an identifier used to connect records from one run across
components.

## Data, testing, and operations

**Artifact** — a saved deliverable or evidence file produced by the work.

**Constraint** — a database or schema rule preventing invalid values/states.

**Database** — structured durable storage queried and updated by software.

**Fixture** — controlled input data used in a test.

**Gold dataset** — a reviewed set of inputs and expected results used for
evaluation.

**Integration test** — a test of components working together.

**Latency** — elapsed time for an operation.

**Log** — time-ordered operational messages or structured records.

**Metric** — a numeric measurement tracked over time.

**Migration** — a versioned change to database structure or stored data.

**Object storage** — storage for files/blobs addressed as objects.

**PostgreSQL** — the relational database used by the course.

**Regression** — previously working behaviour becomes worse after a change.

**Regression test** — a repeatable test intended to detect that worsening.

**RLS (Row Level Security)** — database policies restricting which rows an
identity can access.

**Supabase** — a managed platform supplying PostgreSQL, authentication, and
object storage.

**Test gate** — an explicit pass/fail condition required before continuing.

**Unit test** — a focused test of a small unit of logic.

**Validation** — checking data or behaviour against declared rules.

## Delivery and version control

**Branch** — a named line of Git development.

**Commit** — a recorded Git snapshot with an identifier and message.

**Container** — a running isolated instance of a Docker image.

**Diff** — a representation of lines added, removed, or changed.

**Docker** — tooling for packaging and running services in containers.

**Docker Compose** — a YAML description of related container services.

**Git** — local distributed version-control software.

**GitHub** — an online service that hosts Git repositories.

**Image (Docker)** — a packaged filesystem and startup definition used to
create containers.

**n8n** — the visual workflow orchestrator used in the course.

**Node (n8n)** — one configured workflow step.

**Repository** — a project folder tracked by Git.

**Secret** — a credential or value that grants access and must not be exposed.

**Version pin** — selecting an exact software version for reproducibility.

**Volume** — Docker-managed durable storage mounted into a container.

**Workflow** — connected steps that move one unit of work through a process.

