# Course 1 Product Threat Model

Document ID: `C1-TM`

Version: `1.1`

Effective date: `2026-07-28`

Personal-study publication amendment: `2026-08-02`

Status: **Normative threat baseline; implementation conformance is not yet
verified**

Owner: Course 1 maintainer

Reviewers required for release: technical reviewer and beginner-product
reviewer

Related contract:
`COURSE_1_TECHNICAL_ACCEPTANCE_CONTRACT.md`

## 1. Purpose and authority

This is the authoritative product threat model for Course 1, **Controlled
Artificial Intelligence (AI) Workflow Foundations**. It covers:

- the synthetic, local Course 1 runner;
- the learner's controlled Course 1 workspace and local evidence;
- the Course 1 Progressive Web App (PWA), including progress, notes, backup,
  offline use, and updates;
- the Course 1 dependency, build, test, and release path.

Course 4, live cloud services, real client work, production systems, and
workplace integrations are outside this threat model.

The words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are normative. A
requirement is not satisfied because it appears in this document. It is
satisfied only by the evidence required in the technical acceptance contract.

Threat and boundary identifiers are permanent. If an item is retired, keep its
identifier and mark it retired; never reuse it for a different meaning.

## 2. Intended use and non-goals

### C1-TM-SCOPE-001 — Intended use

Course 1 is a beginner training product. It uses fictional, synthetic data to
teach one controlled, local workflow. The runner may read learner-selected
synthetic inputs and create local evidence inside one learner-selected
workspace. The PWA displays course material and stores learning state locally.

### C1-TM-SCOPE-002 — Explicit non-goals

Course 1 is not:

- a production service;
- a security boundary against an administrator who controls the device;
- a malware scanner or reliable personal-data classifier;
- a multi-user or multi-tenant system;
- a real-data processing system;
- an external approval, sending, payment, ordering, or write-back system;
- proof of legal compliance, production security, or consulting readiness.

### C1-TM-SCOPE-003 — Safety assumption

The learner is a literal beginner and may select the wrong file, misunderstand
a warning, paste a dangerous command, import an unfamiliar backup, or use a
cloud-synchronised folder unintentionally. “The learner should know better” is
not an acceptable preventive control.

The synthetic-data confirmation is an explicit learner attestation. It is not
proof that the selected file is synthetic. The product must reduce foreseeable
selection mistakes and explain this residual risk.

## 3. Protected assets

| ID | Asset | Confidentiality | Integrity | Availability and recovery need |
|---|---|---:|---:|---|
| `C1-AST-001` | Original learner-selected synthetic input and expected-result file | Low, provided it is genuinely synthetic | Critical: originals must not be changed | Input remains available and byte-identical |
| `C1-AST-002` | Controlled runner state, issues, summary, review package, decision, audit, evaluation, and export | Low confidentiality; synthetic only | Critical: evidence and approval must remain attributable and internally consistent | Recoverable or safely stopped with visible evidence |
| `C1-AST-003` | Learner workspace and unrelated neighbouring files | Potentially high because the learner may choose the wrong location | Critical: Course 1 must not change unrelated files | No write, move, rename, or delete outside the controlled root |
| `C1-AST-004` | Learner progress, self-checks, notes, and preferences in browser storage | Notes may contain personal reflections even though sensitive and real work data are prohibited | High: no silent loss, rollback, or cross-window overwrite | Export, import, reset, migration, and update recovery |
| `C1-AST-005` | Progress-backup file | Same as browser state | High: an imported file must not forge unsupported state or destabilise the app | Reject safely without replacing valid state |
| `C1-AST-006` | Course Markdown, curriculum bundle, schemas, runner, PWA source, and tests | Public | Critical: a release must match reviewed source | Rebuildable from a named commit |
| `C1-AST-007` | PWA build, service worker, cached application shell, and course-content bundle | Public | Critical: one coherent release identity; no mixed assets | Old valid release remains usable until a complete update is accepted |
| `C1-AST-008` | Dependency locks, downloaded packages, GitHub Actions, build runner, and release provenance | Public metadata | Critical: no unreviewed or substituted executable dependency | Reproducible reinstall and traceable release |
| `C1-AST-009` | Beginner trust in warnings, pass gates, and recovery instructions | Not applicable | Critical: the interface must not claim privacy, safety, or passing beyond evidence | Honest safe stop and human-readable recovery |

## 4. Actors

| ID | Actor | Capability and expected behaviour |
|---|---|---|
| `C1-ACT-001` | Beginner learner | Authorised, well-intentioned, and error-prone; can select paths, run commands, import backups, and approve synthetic drafts |
| `C1-ACT-002` | Maintainer or reviewer | Can change source, tests, dependencies, release configuration, and public content; can also make mistakes |
| `C1-ACT-003` | Other local process or local user | May change, lock, replace, or observe files while Course 1 runs |
| `C1-ACT-004` | Other website or PWA script on the same web origin | Can access origin-wide browser storage even when it is hosted at another URL path |
| `C1-ACT-005` | Malicious or compromised input/backup author | Can construct malformed, oversized, misleading, Unicode-confusable, or script-bearing content |
| `C1-ACT-006` | Compromised dependency, package index, GitHub Action, CI runner, maintainer account, or hosting origin | Can attempt executable or release substitution |
| `C1-ACT-007` | Network or browser failure | Can interrupt downloads, mix stale and current caches, return an error page, or leave an update incomplete |
| `C1-ACT-008` | Storage, antivirus, synchronisation, or filesystem failure | Can deny, delay, partially apply, lock, or externally replace local files |

An administrator or malware with full control of the learner's device can
defeat local controls. That residual risk is outside Course 1's protection
claim, but safe failure must still be preferred where detectable.

## 5. Trust boundaries

| ID | Boundary | Data crossing it | Required treatment |
|---|---|---|---|
| `C1-TB-001` | Learner or external file into the runner | CSV, JSON, filenames, paths, timestamps, decision text | Untrusted until type, size, encoding, structure, path, and semantic validation pass |
| `C1-TB-002` | Ordinary filesystem into the controlled workspace | Workspace root, run directory, child directories, locks, temporary files, outbox | Resolve and confine paths; detect links/reparse points and substitutions; fail closed |
| `C1-TB-003` | Controlled artifacts into human review and export | Source links, issues, summaries, approval evidence, CSV/JSON | Bind exact revision and hashes; neutralise spreadsheet formula execution; retain synthetic-only boundary |
| `C1-TB-004` | Built course content into browser HTML | Markdown, titles, metadata, links, search excerpts | Treat as untrusted release content; escape or sanitise before any HTML sink |
| `C1-TB-005` | PWA to origin-wide browser storage | Progress, notes, preferences, migration data | Treat the web origin, not the URL path, as the storage boundary |
| `C1-TB-006` | Backup file into or out of the PWA | JSON state and notes | Bound size/depth/counts; validate exact version and fields; transactional replace only |
| `C1-TB-007` | Network and service worker into the installed PWA | HTML, JavaScript, styles, icons, manifest, bundle, version metadata | Same-origin allowlist, coherent release identity, response checks, atomic update |
| `C1-TB-008` | Package and CI ecosystem into executable release work | Python packages, Actions, runner image, Node/Python toolchains | Hash/version pinning, vulnerability and licence review, software bill of materials, provenance |
| `C1-TB-009` | Course instructions into learner execution | PowerShell and Python commands, paths, expected results | Exact beginner-safe commands, preconditions, bounded effects, and recovery |

## 6. Security and safety invariants

These invariants are design constraints, not current pass claims.

- `C1-INV-001`: No Course 1 runner operation writes, moves, renames, or deletes
  outside its verified controlled workspace.
- `C1-INV-002`: A symbolic link, junction, mount point, Windows reparse point,
  alternate data stream, device path, path race, or file/directory substitution
  cannot redirect a controlled operation.
- `C1-INV-003`: Malformed or oversized input produces a bounded named safe
  stop, not an unhandled traceback, indefinite hang, or unbounded memory/disk
  use.
- `C1-INV-004`: The Course 1 runner opens no network connection, resolves no
  network name, creates no child process, invokes no shell, and performs no
  external business action.
- `C1-INV-005`: Original input evidence remains byte-identical.
- `C1-INV-006`: Local export requires a current human approval bound to the
  exact protected revision and creates no external action.
- `C1-INV-007`: Learner state and notes are never transmitted by the PWA. A
  path on a shared web origin is not described as private storage.
- `C1-INV-008`: Untrusted Markdown, metadata, URL, backup content, or note text
  cannot execute code or create an unsafe navigation.
- `C1-INV-009`: A service-worker update cannot activate a mixed, partial,
  unexpected, or unverifiable course release.
- `C1-INV-010`: A passing release is reproducibly linked to reviewed source,
  dependency identities, test evidence, a build identity, and the public
  artifact.
- `C1-INV-011`: A failure never becomes “pass” solely because a test,
  validator, and implementation repeat the same assumption.
- `C1-INV-012`: Recovery preserves the last known-valid state or stops with a
  visible marker and beginner-safe instructions.

## 7. Threat register

Risk uses `High`, `Medium`, or `Low` for the Course 1 product scope. A low
likelihood does not remove a required control when impact includes unrelated
file loss, code execution, data disclosure, or false approval.

| ID | Threat scenario and path | Risk | Prevent / reduce | Detect / recover | Acceptance requirements |
|---|---|---:|---|---|---|
| `C1-THR-001` | Learner selects a real, employer, medical, personal, confidential, or otherwise unfamiliar file and repeats the synthetic confirmation | High | Synthetic-only instructions, constrained fields, path/name preview, explicit confirmation that is not presented as proof | Stop if provenance is uncertain; preserve file; direct learner to a new synthetic retry | `C1-TA-DATA-001`–`003`, `C1-TA-REC-001` |
| `C1-THR-002` | Workspace, run, outbox, or child path is a symbolic link, junction, mount, or Windows reparse point that redirects reads/writes/deletes | High | Reject unsupported link/reparse paths or use non-following handle-based confinement | Recheck before mutation; named safe stop; no external change | `C1-TA-FS-001`–`006` |
| `C1-THR-003` | Path is swapped after validation but before open, replace, cleanup, rollback, or lock release | High | File-identity checks and no-follow operations immediately at mutation; smallest transaction window | Detect identity change, retain incomplete marker, stop | `C1-TA-FS-004`, `C1-TA-REC-003` |
| `C1-THR-004` | UNC, device, extended namespace, alternate data stream, reserved name, case collision, or excessive path length bypasses ordinary path reasoning | High | Accept only documented local paths; canonical component validation; preflight path budget | Named safe stop before mutation; retain original | `C1-TA-FS-007`–`010` |
| `C1-THR-005` | File replaces expected directory or directory replaces expected file | Medium | Exact regular-file/directory checks at every controlled boundary | Named type-mismatch safe stop | `C1-TA-FS-003`, `C1-TA-IO-007` |
| `C1-THR-006` | Oversized CSV/JSON, excessive rows, long cells, deep nesting, huge audit, or decompression-like repetition exhausts memory, disk, or browser responsiveness | High | Enforce byte, row, item, depth, and string limits before materialising content | Bounded safe stop; valid prior state remains | `C1-TA-IO-001`–`008`, `C1-TA-PWA-008`–`010` |
| `C1-THR-007` | Invalid UTF-8, byte-order marks, NUL, control characters, bidirectional controls, Unicode normalisation, look-alike identifiers, or locale-specific parsing changes meaning | Medium | Strict encoding and identifier rules; no silent normalisation; locale-independent formats | Visible validation result with source locator | `C1-TA-IO-009`–`013`, `C1-TA-WIN-006` |
| `C1-THR-008` | Free text or CSV opens as a spreadsheet formula or is mistaken for executable instruction | High | Keep prose inert; exclude it from generated claims; formula-neutral CSV | Exact JSON/source evidence remains available | `C1-TA-DATA-004`, `C1-TA-WEB-001` |
| `C1-THR-009` | Runtime or future dependency makes a network, Domain Name System (DNS), process, shell, provider, e-mail, payment, or write-back call | High | No capability in runner; deny egress/process in acceptance environment; full runtime/dependency inspection | Operating-system observation and fail-on-attempt test | `C1-TA-CAP-001`–`007` |
| `C1-THR-010` | Another same-origin project page reads or changes origin-wide progress and notes | Medium | Dedicated origin for a privacy claim, or honest shared-origin warning and synthetic/non-sensitive note rule | Storage-event/concurrency handling, export and reset; no “private” claim on shared origin | `C1-TA-PWA-001`–`007` |
| `C1-THR-011` | Crafted or oversized progress backup causes code execution, state forgery, denial of service, prototype pollution, or silent replacement | High | Pre-read size limit; exact closed schema; depth/count limits; sanitised keys; transactional import | Preview and explicit replace confirmation; rollback on save/render failure | `C1-TA-PWA-008`–`014` |
| `C1-THR-012` | Course Markdown, title, metadata, link, search excerpt, or note reaches an HTML/URL sink and executes script or unsafe navigation | High | Context-correct escaping, strict URL allowlist, Content Security Policy, no unsafe dynamic-code sinks | Adversarial corpus and browser execution test | `C1-TA-WEB-001`–`008` |
| `C1-THR-013` | Service worker caches an error page, redirect, wrong content type, unexpected resource, or mixed-release asset | High | Exact asset allowlist, response and release-identity verification, temporary cache, atomic activation | Keep old valid worker/cache; discard failed candidate | `C1-TA-SW-001`–`010` |
| `C1-THR-014` | Service-worker message or sibling page forces an update without the learner-controlled update path | Medium | Validate message type and source client; activate only verified waiting worker after explicit action | Update event/audit evidence and cold-reopen test | `C1-TA-SW-006`–`009` |
| `C1-THR-015` | Compromised, vulnerable, substituted, yanked, or licence-incompatible Python package, Action, runner image, or toolchain enters validation/release | High | Version and artifact hashes, fixed runner/toolchain identity, vulnerability and licence gates, least privilege | Software bill of materials (SBOM), provenance, scheduled rescan and time-limited exception | `C1-TA-SC-001`–`012` |
| `C1-THR-016` | Test implementation and product repeat the same wrong rule or lifecycle assumption, producing a false pass | High | Independent decision table/oracle, negative tests, mutation and branch coverage | Deliberately seed faults and prove gates fail | `C1-TA-TEST-001`–`009` |
| `C1-THR-017` | Course passes on Linux or a hidden toolchain but fails on the learner's Windows, PowerShell, locale, path, browser, antivirus, or synchronisation context | High | Explicit support matrix and native Windows end-to-end acceptance | Record exact environment and recovery outcome | `C1-TA-WIN-001`–`012`, `C1-TA-BR-001`–`008` |
| `C1-THR-018` | Lock, state, audit, export, browser storage, update, or migration is interrupted or partially committed | High | Atomic mutation, rollback, backups, idempotency, incomplete markers | Last valid version or visible human-recovery state | `C1-TA-REC-001`–`010` |
| `C1-THR-019` | Antivirus, OneDrive/synchronisation, storage quota, permissions, or another process locks or changes an artifact | Medium | Supported-folder preflight, exclusive operations, bounded retries, no destructive workaround | Named stop with instructions; preserve source and prior valid state | `C1-TA-WIN-008`–`012`, `C1-TA-REC-001`–`006` |
| `C1-THR-020` | External link leaks state, opens an insecure scheme, retains opener authority, or disguises a repository path escape | Medium | HTTPS-only external allowlist, `noopener`, `noreferrer`, safe repository-path construction | Link corpus and browser navigation tests | `C1-TA-WEB-005`–`008` |
| `C1-THR-021` | Maintainer or compromised account publishes artifacts that do not correspond to reviewed source and evidence | High | Protected branch/review, least-privilege workflow, deterministic identity, provenance, post-deploy comparison | Roll back to prior release; publish incident note | `C1-TA-SC-007`–`012`, `C1-TA-REC-009`–`010` |

| `C1-THR-022` | Public availability, local progress, a generated evidence pack, or assessor preparation is misrepresented as Course 1 acceptance, learner completion, Course 2 readiness, consulting ability, client readiness, or production fitness | High | Machine-readable `UNVERIFIED` status and `personal-synthetic-study` purpose; persistent non-dismissible PWA boundary; separate study and accepted-release verifiers | Reject accepted promotion, preserve pending evidence, and require product plus human learner gates before any final pass | `C1-TA-SC-007`–`012`, `C1-TA-PWA-001`–`014` |

## 8. Abuse and misuse cases that must become tests

| ID | Required test idea | Expected safe result |
|---|---|---|
| `C1-ABUSE-001` | Place a junction at `runs`, `review`, `outbox`, `failures`, a staging directory, and a rollback target | Operation stops before external read/write/delete |
| `C1-ABUSE-002` | Swap a verified directory or file for a junction/link between validation and mutation | Identity change is detected; no external effect |
| `C1-ABUSE-003` | Supply file where folder is expected and folder where file is expected | Specific type-mismatch safe stop |
| `C1-ABUSE-004` | Use UNC, device namespace, alternate data stream, reserved Windows name, trailing dot/space, case collision, non-ASCII path, and maximum supported path | Unsupported cases stop before mutation; supported cases complete |
| `C1-ABUSE-005` | Generate limit-minus-one, exact-limit, and limit-plus-one files, rows, fields, strings, arrays, JSON depth, audit lines, and PWA backups | First two are deterministic; limit-plus-one stops without prior-state loss |
| `C1-ABUSE-006` | Use invalid UTF-8, optional UTF-8 byte-order mark, NUL, control and bidirectional characters, composed/decomposed Unicode, quoted newlines, and Dutch decimal/date forms | Contracted forms behave identically across locales; unsafe forms stop visibly |
| `C1-ABUSE-007` | Attempt socket, DNS, child-process, shell, browser, e-mail, provider, and write-back access from every runner entry point and dependency | Attempt fails and release gate detects it |
| `C1-ABUSE-008` | Open a sibling page on the same GitHub Pages origin and inspect the course storage key | Test proves the shared-origin fact; UI makes no unsupported privacy claim |
| `C1-ABUSE-009` | Import backup with huge file, deep JSON, excessive properties, `__proto__`, unknown keys, unexpected versions, long notes, and forged document identifiers | Backup is rejected transactionally; current state remains exact |
| `C1-ABUSE-010` | Render adversarial Markdown and metadata containing script, event handlers, SVG/MathML, encoded schemes, malformed URLs, nested tokens, and attribute breakouts | No script/event/navigation executes |
| `C1-ABUSE-011` | Serve redirected, opaque, wrong-type, wrong-build, corrupt, missing, mixed, and interrupted PWA assets | Candidate update is discarded; old release reopens offline |
| `C1-ABUSE-012` | Introduce one deliberate rule, approval, audit, path, rollback, Markdown, storage, or service-worker defect | Independent test, mutation, or acceptance gate fails |
| `C1-ABUSE-013` | Execute the documented learner path in fresh PowerShell 5.1 under Restricted policy on supported Windows and browser configurations | No hidden PATH, activation, locale, or maintainer-tool dependency |
| `C1-ABUSE-014` | Interrupt each controlled mutation and PWA migration/update at every durable-write boundary | Last valid state survives or an explicit blocking marker remains |

## 9. Privacy analysis

### C1-TM-PRIV-001 — Synthetic runner data

The runner is approved only for synthetic data. If real or sensitive data is
introduced contrary to instructions, this threat model makes no confidentiality
claim. The runner must still avoid network and external action, avoid printing
absolute or sensitive paths unnecessarily, and preserve the selected file.

### C1-TM-PRIV-002 — PWA notes

Browser `localStorage` is isolated by origin, not URL path. Therefore a project
site at `https://freddywinkel.github.io/ai-workflow-course/` shares Web Storage
with scripts on other paths under `https://freddywinkel.github.io`.

Until the PWA has a dedicated trustworthy origin or user-key encryption that
does not persist the key on that origin:

- notes MUST be limited to synthetic, non-sensitive learning reflections;
- the interface MUST NOT call them confidential or private;
- the interface MUST explain that they remain in that browser profile but may
  be accessible to other scripts on the same hosting origin;
- the app MUST NOT transmit notes or state.

### C1-TM-PRIV-003 — External links

Course links must not include learner state or notes. External navigation must
not provide opener authority and should not send a referrer. Opening an
external link is an explicit learner action, not a Course 1 business action.

## 10. Security claims and their limits

The public version 2.6.0 personal-study release may claim only that its named
automated technical gates and exact public-byte check passed for one synthetic
study artifact. It MUST remain labelled `UNVERIFIED` and
`personal-synthetic-study`. It MUST NOT claim Course 1 product acceptance,
learner completion, Course 2 readiness, consulting ability, client readiness,
production fitness, or permission to use real data. Local reading progress,
self-checks, generated files, and assessor preparation do not change that
boundary.

The accepted release may make only these bounded claims:

1. The **Course 1 runner** was tested to make no network/DNS request, create no
   child process or shell, and perform no external business action in the
   supported environment and reviewed dependency set.
2. The **PWA** may fetch same-origin public course assets and version metadata.
   It was tested not to transmit learner progress or notes.
3. Controlled filesystem effects were tested to remain within the verified
   workspace under the supported filesystem model, including Windows reparse
   abuse cases.
4. Passing is evidence for this synthetic training product only. It is not a
   production penetration test or a defence against device administrator
   compromise.

Statements such as “completely secure,” “private notes,” “impossible to
escape,” or “contains no real data” are prohibited unless the statement is
qualified by the exact evidence boundary.

## 11. Residual risks and ownership

| ID | Residual risk | Required treatment and owner |
|---|---|---|
| `C1-RSK-001` | A learner can falsely or mistakenly attest that real data is synthetic | Keep the warning and selection preview; Course 1 maintainer owns wording and tests; learner owns final file choice |
| `C1-RSK-002` | Device administrator or malware can read or change local files and browser storage | State explicitly; learner/device owner controls endpoint security |
| `C1-RSK-003` | Browser, Windows, package, or hosting behaviour can change after release | Dated support matrix and scheduled dependency/browser/source review; maintainer owns revalidation |
| `C1-RSK-004` | Shared-origin storage is readable by sibling-origin scripts | No privacy claim; synthetic notes only; maintainer owns dedicated-origin decision |
| `C1-RSK-005` | Availability can be lost through device failure or deletion of all backups | PWA export and learner repository backup guidance; learner owns external backup |
| `C1-RSK-006` | No finite test corpus proves absence of every parser, browser, or filesystem defect | Independent audit, fuzzing, mutation, and conservative safe stops; maintainer owns release decision |

No residual risk may be silently accepted. A release exception must identify
the requirement, evidence, affected environment, compensating control, owner,
expiry date, and explicit release decision.

## 12. Review triggers

Review this threat model before release and whenever any of these changes:

- runner input, output, path, lock, transaction, or dependency behaviour;
- PWA hosting origin, storage, backup, renderer, service worker, or update flow;
- supported Windows, Python, PowerShell, browser, or filesystem matrix;
- GitHub Actions, package source, build toolchain, or deployment method;
- a security advisory, incident, near miss, data-boundary mistake, or recovery
  failure;
- Course 1 begins using real data, live AI, connectors, cloud runtime, or
  external actions.

The last item is a scope change and requires a new threat model and explicit
user authority. It cannot be approved as a small Course 1 exception.
