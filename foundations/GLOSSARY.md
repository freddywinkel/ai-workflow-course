# Beginner Glossary

Use this as a lookup page. Definitions are deliberately plain and specific to
the course.

## Abbreviations, short forms, and special names

You do **not** need to memorise this section. Use your browser's page search
(`Ctrl+F`) when you meet a short form you do not recognise. Course lessons
must still write an abbreviation in full the first time it appears; this page
is a backup, not a substitute for that explanation.

The first tables incorporate the supplied
`common_ai_programming_abbreviations` reference. Some entries belong to later
courses or general software work. Their presence here does not make them
Course 1 requirements.

**Git is a product name, not an abbreviation.** Write `Git`, not `GIT`.
Git is the version-control tool; GitHub is an online service that can host Git
repositories.

### Common software and product work

| Short form | Full form or name | Meaning in normal language |
|---|---|---|
| **API** | Application Programming Interface | An agreed way for programs to request information or actions from each other. |
| **SDK** | Software Development Kit | Tools supplied for building with a particular platform or service. |
| **IDE** | Integrated Development Environment | An application for writing and testing code, such as Visual Studio Code. |
| **CLI** | Command-Line Interface | A way to control software by typing commands in a terminal. |
| **GUI** | Graphical User Interface | A way to control software through windows, buttons, menus, and icons. |
| **UI** | User Interface | The parts of a product a person sees and interacts with. |
| **UX** | User Experience | How understandable, efficient, and usable a product feels. |
| **OS** | Operating System | The main software running a device, such as Windows, Android, or iOS. |
| **DB** | Database | An organised place where an application stores information. |
| **SQL** | Structured Query Language | A language used to read and change relational databases. |
| **JSON** | JavaScript Object Notation | A text format for structured information exchanged between systems. |
| **HTML** | HyperText Markup Language | The content and structure of a web page. |
| **CSS** | Cascading Style Sheets | Rules controlling how a web page looks. |
| **JS** | JavaScript | A programming language commonly used to make web pages interactive. |
| **TS** | TypeScript | JavaScript with additional type checks that can catch some mistakes earlier. |
| **URL** | Uniform Resource Locator | A web or application-programming-interface address. |
| **HTTP** | HyperText Transfer Protocol | The protocol commonly used for requests between browsers, applications, and servers. |
| **HTTPS** | HyperText Transfer Protocol Secure | HTTP protected with modern connection encryption. |
| **DNS** | Domain Name System | The system that translates a name such as `example.com` into a network address. |
| **IP** | Internet Protocol | Part of the addressing and communication system used on networks. |
| **PWA** | Progressive Web App | A website that can behave like an installed application and may support offline use. |
| **SPA** | Single-Page Application | A web application that updates its current page instead of loading a whole new page for each action. |
| **MVP** | Minimum Viable Product | The smallest useful product version that can test a value assumption. |
| **PoC** | Proof of Concept | A limited experiment showing whether an idea is technically possible. It does not prove production readiness or business value. |
| **QA** | Quality Assurance | Planned work used to check and improve whether a product meets its quality requirements. |

### Artificial intelligence and machine learning

| Short form | Full form | Meaning in normal language |
|---|---|---|
| **AI** | Artificial Intelligence | The broad field of computer systems performing tasks associated with intelligence. |
| **ML** | Machine Learning | Methods that learn patterns from data instead of relying only on hand-written rules. |
| **DL** | Deep Learning | Machine learning using neural networks with many layers. |
| **NN** | Neural Network | A machine-learning structure made of connected mathematical units. In this course, however, `NN` inside labels such as `module-NN` means “replace this with a number”; check the context before using this definition. |
| **LLM** | Large Language Model | A model trained on large amounts of text to interpret or generate language. |
| **SLM** | Small Language Model | A smaller language model that may need fewer computing resources. |
| **GPT** | Generative Pre-trained Transformer | A family of language-model designs and names; not every artificial-intelligence model is a GPT. |
| **GenAI** | Generative Artificial Intelligence | Artificial intelligence that creates candidate text, images, audio, video, or code. |
| **NLP** | Natural Language Processing | Technology for analysing or producing human language. |
| **NLU** | Natural Language Understanding | Work focused on interpreting meaning in human language. |
| **NLG** | Natural Language Generation | Work focused on producing human-language output. |
| **CV** | Computer Vision | Technology for analysing images or video. |
| **VLM** | Vision-Language Model | A model that works with images and language together. |
| **MLLM** | Multimodal Large Language Model | A large model that can work with multiple formats, such as text and images. |
| **RAG** | Retrieval-Augmented Generation | Retrieving potentially relevant source passages before a model drafts an answer from them. Retrieval does not guarantee that the answer is true. |
| **MCP** | Model Context Protocol | A technical standard through which artificial-intelligence applications can connect to tools and data sources. |
| **AGI** | Artificial General Intelligence | A hypothetical artificial intelligence with broad general ability; current use of the label is disputed. |
| **ANI** | Artificial Narrow Intelligence | Artificial intelligence designed for bounded types of tasks. |
| **ASI** | Artificial Superintelligence | A hypothetical intelligence exceeding humans across most areas. |
| **RL** | Reinforcement Learning | Learning behaviour through reward or penalty signals. |
| **RLHF** | Reinforcement Learning from Human Feedback | Improving model behaviour using human preference or evaluation signals. |
| **RLAIF** | Reinforcement Learning from AI Feedback | A related method using artificial-intelligence-generated evaluation signals. |
| **SFT** | Supervised Fine-Tuning | Further training a model on examples of desired inputs and outputs. |
| **DPO** | Direct Preference Optimization | Training from comparisons between preferred and rejected outputs. |
| **LoRA** | Low-Rank Adaptation | A resource-efficient method for adapting an existing model. |
| **PEFT** | Parameter-Efficient Fine-Tuning | Adapting only a small part of a model's parameters. |
| **MoE** | Mixture of Experts | A model design with specialised components, only some of which are used for each request. |
| **GAN** | Generative Adversarial Network | A model design in which competing networks can learn to generate candidate content. |
| **OCR** | Optical Character Recognition | Turning visible characters in an image or scan into candidate machine-readable text. |
| **ASR** | Automatic Speech Recognition | Turning spoken language into candidate text. |
| **STT** | Speech-to-Text | Another common name for converting speech into text. |
| **TTS** | Text-to-Speech | Producing spoken audio from written text. |

### Web and application development

| Short form | Full form | Meaning in normal language |
|---|---|---|
| **DOM** | Document Object Model | The browser's structured representation of a web page and its elements. |
| **REST** | Representational State Transfer | A common design style for web application programming interfaces. |
| **CRUD** | Create, Read, Update, Delete | Four basic operations performed on stored information. |
| **SSR** | Server-Side Rendering | Building a web page on a server before sending it to the browser. |
| **CSR** | Client-Side Rendering | Building or updating a page in the browser, commonly with JavaScript. |
| **SSG** | Static Site Generation | Creating pages in advance, normally during a build or deployment. |
| **CDN** | Content Delivery Network | Distributed servers that deliver files from locations closer to users. |
| **CORS** | Cross-Origin Resource Sharing | Browser rules controlling whether one web origin may request data from another. |
| **JWT** | JSON Web Token | A signed token format often used to carry identity or authorization claims. A signed token is not automatically encrypted. |
| **OAuth** | Open Authorization | A framework for granting limited access to another service without handing the application your password. |
| **MFA** | Multi-Factor Authentication | Signing in with more than one type of verification factor. |
| **2FA** | Two-Factor Authentication | Multi-factor authentication using exactly two factors. |
| **SSL** | Secure Sockets Layer | An obsolete encryption protocol whose name is still used informally. Modern secure web connections use TLS. |
| **TLS** | Transport Layer Security | The modern protocol that protects HTTPS connections. |
| **TCP** | Transmission Control Protocol | A network protocol that provides ordered, reliable delivery. |
| **UDP** | User Datagram Protocol | A network protocol that sends messages without guaranteeing delivery or order. |
| **RPC** | Remote Procedure Call | Asking a function or procedure to run in another process or system. |
| **URI** | Uniform Resource Identifier | A general identifier for a resource; a URL is one kind of URI. |
| **WASM** | WebAssembly | A compact code format that can run in web browsers and other runtimes. |

### Git and delivery

| Short form | Full form or name | Meaning in normal language |
|---|---|---|
| **VCS** | Version Control System | Software that records changes to files over time. |
| **DVCS** | Distributed Version Control System | Version control in which each working copy can contain the complete project history. Git is a DVCS. |
| **repo** | Repository | Informal shortening for the project folder and its recorded version history; it is not an abbreviation. |
| **PR** | Pull Request | A request to review and merge proposed changes on a platform such as GitHub. |
| **MR** | Merge Request | GitLab's common name for roughly the same review-and-merge request. |
| **SHA** | Secure Hash Algorithm | A family of algorithms used to create fixed-size fingerprints. Course instructions use the more precise `SHA-256`. |
| **SSH** | Secure Shell | A protocol for secure remote connections and authentication. |
| **CI** | Continuous Integration | Automatically building or testing changes when they are submitted. |
| **CD** | Continuous Delivery or Continuous Deployment | Automatically preparing a validated release, or automatically publishing it, depending on the stated meaning. |
| **CI/CD** | Continuous Integration and Continuous Delivery or Deployment | A combined automated path from a code change through checks and release steps. |

Common Git actions such as **commit**, **branch**, **merge**, **clone**,
**fork**, **push**, **pull**, and **rebase** are words, not abbreviations. Their
course-specific definitions appear later on this page.

### Files, data, and databases

| Short form | Full form | Meaning in normal language |
|---|---|---|
| **CSV** | Comma-Separated Values | A plain-text table format. |
| **XML** | Extensible Markup Language | A structured text format used by many systems and documents. |
| **YAML** | YAML Ain't Markup Language | A human-readable configuration format in which indentation matters. |
| **DBMS** | Database Management System | Software used to create and manage databases. |
| **RDBMS** | Relational Database Management System | A database system organised around related tables. |
| **ORM** | Object-Relational Mapping | Software that maps program objects to relational-database records. |
| **ETL** | Extract, Transform, Load | Taking data from a source, changing it, and then loading it elsewhere. |
| **ELT** | Extract, Load, Transform | Loading source data first and transforming it afterward. |
| **ACID** | Atomicity, Consistency, Isolation, Durability | Four properties used to describe reliable database transactions. |
| **NoSQL** | Not Only SQL | A broad label for databases that do not rely only on traditional relational tables. |

### Cloud, hardware, and deployment

| Short form | Full form | Meaning in normal language |
|---|---|---|
| **CPU** | Central Processing Unit | A computer's general-purpose processor. |
| **GPU** | Graphics Processing Unit | A processor suited to parallel calculations and often used for artificial intelligence. |
| **NPU** | Neural Processing Unit | Hardware designed for artificial-intelligence calculations. |
| **TPU** | Tensor Processing Unit | Google-designed hardware for machine-learning calculations. |
| **RAM** | Random Access Memory | Short-term working memory used by running programs. |
| **VRAM** | Video Random Access Memory | Memory used by a graphics processor. |
| **SSD** | Solid-State Drive | Permanent storage without moving disks. |
| **HDD** | Hard Disk Drive | Permanent storage using spinning disks. |
| **I/O** | Input/Output | Information entering or leaving a program, component, or system. |
| **VM** | Virtual Machine | A simulated computer running inside another computer. |
| **VPS** | Virtual Private Server | A rented virtual server used to host applications. |
| **SaaS** | Software as a Service | Software operated by a provider and used as an online service. |
| **PaaS** | Platform as a Service | A hosted platform on which applications can be deployed. |
| **IaaS** | Infrastructure as a Service | Renting computing, network, and storage infrastructure. |
| **FaaS** | Function as a Service | Running individual functions on demand without operating a full server. |
| **AWS** | Amazon Web Services | Amazon's cloud-computing platform. |
| **GCP** | Google Cloud Platform | A common older expansion for Google's cloud platform, now generally called Google Cloud. |
| **LTS** | Long-Term Support | A software version maintained with fixes for an extended period. |

### Testing, product work, and accessibility

| Short form | Full form or name | Meaning in normal language |
|---|---|---|
| **TDD** | Test-Driven Development | Writing a failing test before implementing the behaviour that makes it pass. |
| **BDD** | Behavior-Driven Development | Describing and testing software through expected user or business behaviour. |
| **E2E** | End-to-End | Testing a workflow from its beginning to its final outcome. |
| **UAT** | User Acceptance Testing | Representative users checking agreed business scenarios and acceptance criteria. |
| **SLA** | Service-Level Agreement | A formal agreement about measurable service performance or availability. |
| **SLO** | Service-Level Objective | A measurable reliability or performance target. |
| **KPI** | Key Performance Indicator | A defined measure used to assess a business result. |
| **WCAG** | Web Content Accessibility Guidelines | International guidelines for accessible digital content. |
| **a11y** | Accessibility | A numeronym: eleven letters are replaced by `11` between `a` and `y`. |
| **i18n** | Internationalization | A numeronym: eighteen letters are replaced by `18` between `i` and `n`. |

### JavaScript names and short forms

| Short form | Full form or name | Meaning in normal language |
|---|---|---|
| **npm** | npm package manager | The common package manager used with Node.js. `npm` is its stylised name; do not force it into an expansion. |
| **npx** | npx command | A command that runs a package, often without a global installation. Treat `npx` as a command name. |
| **JSX** | JavaScript Syntax Extension | JavaScript syntax resembling HTML, commonly used by React. |
| **TSX** | TypeScript with JSX | JSX-style syntax used in a TypeScript file. |
| **ES** | ECMAScript | The standard on which JavaScript is based. |
| **ESM** | ECMAScript Modules | The modern JavaScript module system using `import` and `export`. |
| **CJS** | CommonJS | An older JavaScript module system commonly using `require`. |
| **NVM** | Node Version Manager | A tool for switching between Node.js versions. |

### Additional short forms that appear in Course 1 material

These are included because they occur in required lessons, supporting
references, templates, or maintenance material bundled with Course 1.

| Short form | Full form or name | Meaning in normal language |
|---|---|---|
| **SME** | Small and Medium-sized Enterprise | A business smaller than a large enterprise; exact legal or statistical limits depend on context. |
| **ID** | Identifier | A stable label for one record, test, run, or artifact. |
| **IO** | Input/Output | The form used inside some technical labels. `System.IO` is a code library for file and path operations. |
| **PS** | PowerShell | In `PS C:\...>`, `PS` shows that the terminal is using PowerShell. |
| **JSONL** | JavaScript Object Notation Lines | One complete JSON value per line. |
| **SHA-256 / SHA256** | Secure Hash Algorithm 256-bit | Creates a fixed-size fingerprint of file bytes. PowerShell commands commonly use the spelling `SHA256`. |
| **UTF-8 / UTF8** | Unicode Transformation Format 8-bit | The course's standard way to encode text characters. Some commands omit the hyphen. |
| **GB** | Gigabyte | A unit of storage capacity. |
| **EUR / USD** | Euro / United States dollar currency codes | Standard codes identifying the two currencies. |
| **UTC** | Coordinated Universal Time | A timezone-independent standard used in timestamps. |
| **EU / UK / NL** | European Union / United Kingdom / Netherlands | Geographic short forms. `nl-NL` is the Dutch-language Netherlands locale code. |
| **AVG** | Algemene verordening gegevensbescherming | The Dutch name for the General Data Protection Regulation. |
| **GDPR** | General Data Protection Regulation | European Union law governing personal data. |
| **ISO** | International Organization for Standardization | The standard name is written `ISO`; this course mainly mentions unambiguous ISO-style dates. |
| **CBS** | Centraal Bureau voor de Statistiek | Statistics Netherlands, the Dutch national statistical office. |
| **AP** | Autoriteit Persoonsgegevens or Accounts Payable | The Dutch Data Protection Authority in legal/privacy material; the team that handles supplier bills in an operations example. Check the context. |
| **NCSC** | National Cyber Security Centre | The Dutch national cybersecurity authority. |
| **DTC** | Digital Trust Center | Dutch government cybersecurity guidance for businesses. |
| **NIST** | National Institute of Standards and Technology | A United States standards and technology organisation. |
| **RMF** | Risk Management Framework | In this course, part of the NIST artificial-intelligence risk framework. |
| **OECD** | Organisation for Economic Co-operation and Development | An intergovernmental organisation that publishes policy research and guidance. |
| **UWV** | Uitvoeringsinstituut Werknemersverzekeringen | The Dutch Employee Insurance Agency. |
| **IT** | Information Technology | Computers, software, networks, and related organisational services. |
| **BV** | Besloten vennootschap | A Dutch private limited company. |
| **B2B** | Business-to-Business | Work or trade from one business to another. |
| **ADR** | Architecture Decision Record | A dated explanation of a technical choice and its consequences. |
| **SBOM** | Software Bill of Materials | An inventory of software components and dependencies in a product. |
| **PyPI** | Python Package Index | The main online repository from which Python packages are obtained. |
| **PDF** | Portable Document Format | A document format designed to preserve page layout. |
| **DOCX** | Microsoft Word Open XML document | The common modern Microsoft Word file format. |
| **GUID** | Globally Unique Identifier | A long identifier designed to be unique across systems. |
| **MSI** | Windows Installer package | A traditional Windows software-installation package format. |
| **MSIX** | Microsoft application-package format | A newer Windows application-package format; treat `MSIX` as a format name rather than forcing an expansion. |
| **DPIA** | Data Protection Impact Assessment | A formal assessment of privacy risks for processing that may create high risk. |
| **DPA** | Data Processing Agreement or Addendum | In the vendor template, the contract terms governing processing of personal data. It can mean something else in another context. |
| **SCC** | Standard Contractual Clauses | European Union contract clauses used for some international personal-data transfers. |
| **SSRF** | Server-Side Request Forgery | An attack that tricks a server into requesting an unintended address or resource. |
| **ERP** | Enterprise Resource Planning | A business system that can combine areas such as finance, purchasing, inventory, and operations. |
| **CRM** | Customer Relationship Management | A system for managing customer and sales information and activity. |
| **DMS** | Document Management System | A system for storing, organising, finding, and controlling documents. |
| **eQMS** | Electronic Quality Management System | Software supporting controlled quality processes and records. |
| **SOP** | Standard Operating Procedure | An approved instruction describing how a recurring task must be performed. |
| **RTO** | Recovery Time Objective | The target time within which an operation should be restored. |
| **RPO** | Recovery Point Objective | The acceptable amount of data loss, expressed as a period of time. |
| **CAPA** | Corrective and Preventive Action | A quality process for correcting causes and preventing recurrence or occurrence. |
| **BSN** | Burgerservicenummer | A sensitive Dutch citizen-service identifier; never use a real one in course practice. |
| **ROI** | Return on Investment | A comparison between expected financial benefit and investment. Course 1 forbids inventing it without evidence. |
| **ZDR** | Zero Data Retention | A provider-specific retention status that must be verified rather than assumed. |
| **MAM** | Modified Abuse Monitoring | A provider-specific monitoring arrangement that must be verified rather than assumed. |
| **OSV** | Open Source Vulnerabilities | The vulnerability database and scanning ecosystem used by release checks. |
| **N/A** | Not Applicable | The item does not apply; it does not mean missing or unknown. |

Other names you may see are also not abbreviations: **GitHub**, **Python**,
**PowerShell**, **Markdown**, **Codex**, and **pytest**. `pip` is Python's
package installer, `venv` is shorthand for a virtual environment, and `n8n`
is a product name pronounced “n-eight-n.” `PATH` and `LASTEXITCODE` are
variable names. **Token** and **context window** are ordinary artificial-
intelligence terms whose definitions appear later on this page.

## Process, consulting, and adoption

**Acceptance criteria** — observable conditions that must be true before work
is accepted.

**Adoption** — people consistently using a changed process correctly, with the
knowledge and support needed to do so.

**As-is process** — how work is actually performed now, including exceptions,
waiting, workarounds, and manual steps.

**Baseline** — a measured description of current performance used for later
comparison.

**Business owner** — the person accountable for the business outcome and for
deciding whether the workflow should exist.

**Change management** — preparing, involving, training, and supporting people
so a process change can be used and sustained.

**Completion condition** — the observable state that means one unit of work has
finished successfully or reached a declared exception outcome.

**Consequential action** — an action that can materially affect a person,
organisation, contract, payment, access, or external communication.

**Discovery** — structured investigation of the current process, people, data,
problems, constraints, and desired outcome before proposing a solution.

**Escalation** — routing an unresolved, high-risk, or unauthorised case to a
named person with the authority to decide what happens next.

**Handover** — transferring a workflow, documentation, access, knowledge,
operating duties, and known limitations to its future owner.

**Intended purpose** — the specific users, context, inputs, functions, and
outputs for which a workflow is designed and evaluated.

**Key performance indicator (KPI)** — a defined measure used to assess a
business result. A KPI needs a calculation method, source, owner, and period.

**Manual baseline** — observed time, quality, volume, errors, and rework for the
current human process before automation.

**Negative scope** — an explicit statement of what the workflow will not do.

**Opportunity** — a process problem that may be worth improving, subject to
evidence about value, feasibility, risk, ownership, and adoption.

**Pilot** — a limited, time-bounded implementation used to test assumptions and
acceptance criteria before wider use.

**Process** — connected human and system activities that transform a trigger
and inputs into a declared outcome.

**Process owner** — the person accountable for how a process operates, including
its rules, exceptions, and improvement decisions.

**Residual risk** — risk that remains after the selected controls are applied.

**Scope** — the agreed boundary of users, steps, systems, data, deliverables,
time, and exclusions.

**Small or medium-sized enterprise (SME)** — a small or medium-sized business.
The exact legal or statistical thresholds depend on context.

**Stakeholder** — a person or group that performs, owns, supports, is affected
by, or can approve a process change.

**To-be process** — the proposed future process, including changed roles,
controls, exceptions, and fallback.

**Training** — planned instruction and practice that enables a named user group
to perform its part of the workflow.

**User acceptance testing (UAT)** — representative users checking the workflow
against agreed business scenarios and acceptance criteria.

**Unit of work** — one item that moves through a process, such as one request,
order, ticket, invoice, or review.

**Value hypothesis** — a testable statement that a defined change will improve
a defined measure for a defined group under stated assumptions.

## Files, code, and tools

**Argument** — a value passed to a command or function.

**Boolean** — a value that is either true or false.

**Command-line interface (CLI)** — a text interface for giving a program exact
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

**Python** — a programming language that can implement small, testable rules,
transformations, APIs, and workflow components.

**Runtime** — the program/environment that executes code.

**Script** — a file containing commands or code intended to run.

**String** — text data.

**Syntax** — the formal grammar of a language or data format.

**Terminal** — the window that hosts a command-line shell such as PowerShell.

**Type** — a category of value such as string, integer, Boolean, or date.

**Variable** — a name referring to a value.

**Virtual environment** — an isolated set of Python packages for one project.

**YAML** — an indentation-sensitive text configuration format.

## Spreadsheets and data quality

**Cell** — the intersection of one row and one column in a spreadsheet.

**Column** — one named attribute stored for every applicable row in a table.

**Completeness** — whether required data is present.

**Consistency** — whether related values agree with each other and declared
rules.

**Comma-separated values (CSV)** — a plain-text tabular format. CSV does not
preserve workbook formulas, formatting, filters, or multiple sheets.

**Data dictionary** — a controlled description of each field's name, meaning,
type, allowed values, source, owner, and rules.

**Data quality** — fitness of data for a declared purpose, assessed through
dimensions such as completeness, validity, consistency, uniqueness, and
timeliness.

**Delimiter** — the character separating fields in a text table, such as a
comma, semicolon, or tab.

**Derived artifact** — data or a file produced from a source, such as an issue
record, calculation, or summary.

**Encoding** — the convention that maps stored bytes to characters, such as
UTF-8.

**Expected issue** — a deliberately reviewed issue in test data used to check
whether a rule detects the right condition.

**False negative** — an expected issue that a check failed to report.

**False positive** — a reported issue that is not actually an issue under the
declared rule.

**Header row** — the row containing stable column names.

**Issue record** — a structured record connecting a failed rule to the relevant
work item, field, severity, message, and evidence.

**International Organization for Standardization (ISO) date** — in this
course, the unambiguous exchange format `YYYY-MM-DD`.

**Row** — one record or unit of work represented across a table's columns.

**Source export** — an unchanged snapshot exported from a source system at a
recorded time.

**System of record** — the declared authoritative system in which a category of
business data is maintained.

**Timeliness** — whether data is current enough for its declared purpose.

**True positive** — an expected issue that a check correctly reported.

**Unique identifier** — a stable value that identifies one record and is not
reused for another.

**Uniqueness** — whether a record or identifier occurs only as allowed.

**Validity** — whether a value follows its declared type, format, range, or
allowed list.

**Workbook** — a spreadsheet file that may contain multiple worksheets,
formulas, formatting, and controls.

**Working copy** — a separate copy used for analysis or transformation while
the source export remains unchanged.

**Worksheet** — one tabular sheet inside a workbook.

## Web and application programming interfaces (APIs)

**Application programming interface (API)** — an agreed interface through
which software components make requests and receive responses.

**API key** — a secret credential used by software to authenticate.

**Authentication** — verifying who or what is making a request.

**Authorization** — deciding what an authenticated identity may do.

**Client** — software that sends a request.

**Endpoint** — a method and path exposed by an API.

**FastAPI** — a Python web framework that can expose tested functions through an
API.

**Header** — request/response metadata such as content type or authentication.

**Hypertext Transfer Protocol (HTTP)** — the protocol commonly used for API
requests and responses.

**JavaScript Object Notation (JSON)** — a strict text format for objects,
arrays, strings, numbers, Booleans, and null.

**JavaScript Object Notation Lines (JSONL)** — one complete JSON value per
line.

**Localhost** — the current computer as a network host, commonly
`127.0.0.1`.

**Method** — an HTTP action label such as GET or POST.

**Port** — a numbered network door used to reach one service on a host.

**Request** — a message from a client asking a server to do something.

**Response** — the server's answer to a request.

**Software development kit (SDK)** — a vendor-provided set of tools that wraps
an API for a programming language.

**Server** — software that listens for requests and returns responses.

**Status code** — a three-digit HTTP result category such as 200, 404, or 500.

**Timeout** — the client stopped waiting; it does not prove the server performed
no action.

**Uniform Resource Locator (URL)** — an address identifying a web or API
resource.

**Webhook** — an HTTP endpoint called automatically when an event occurs.

## AI and documents

**Artificial intelligence (AI) literacy** — sufficient understanding to use,
supervise, question, and stop an AI system appropriately.

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

**Large language model (LLM)** — a model that generates and interprets text by
predicting token sequences.

**Model** — the trained computational component that maps input to candidate
output.

**Optical character recognition (OCR)** — converting visible image text into
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

**Agent** — an AI-enabled component that may select or perform multiple steps
toward a goal. The label does not establish its accuracy, authority, or safety.

**Approval** — a recorded human decision about an exact proposed output.

**Audit event** — a structured record of a significant system event.

**Circuit breaker** — a control that temporarily stops calls after repeated
failures.

**Control point** — a place where a rule, test, or reviewer can stop progress.

**Connector** — a configured integration that communicates with another system
using declared permissions and credentials.

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

**Safe stop** — a stated condition that disables a capability or action path
and returns the work to a documented manual method.

**Manual fallback** — a documented non-automated way to complete or safely stop
work when the system fails.

**Orchestrator** — software that triggers, connects, routes, waits for, and
monitors workflow steps.

**Probabilistic** — output may vary and is described in terms of likelihood,
not certainty.

**Queue** — a visible holding place for work awaiting processing, retry, review,
or escalation.

**Reason code** — a stable machine-readable label explaining a result or
failure.

**Retry** — another attempt after a declared temporary failure.

**State** — one named stage of a workflow run.

**State machine** — named states plus rules for allowed transitions.

**Trace ID** — an identifier used to connect records from one run across
components.

**Trigger** — the event, schedule, or manual action that starts a workflow run.

**Write-back** — changing data in a source or connected business system.

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

**PostgreSQL** — an open-source relational database engine.

**Regression** — previously working behaviour becomes worse after a change.

**Regression test** — a repeatable test intended to detect that worsening.

**Row level security (RLS)** — database policies restricting which rows an
identity can access.

**Supabase** — a managed platform that supplies PostgreSQL, authentication, and
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

**n8n** — one visual workflow orchestrator that can connect triggers, services,
rules, and review routes.

**Node (n8n)** — one configured workflow step.

**Low-code** — software development that uses visual configuration while still
requiring logic, permissions, testing, and maintenance.

**No-code** — a label for building mainly through configuration rather than
traditional source code; it does not mean no technical risk or ownership.

**Repository** — a project folder tracked by Git.

**Secret** — a credential or value that grants access and must not be exposed.

**Version pin** — selecting an exact software version for reproducibility.

**Volume** — Docker-managed durable storage mounted into a container.

**Workflow** — connected steps that move one unit of work through a process.
