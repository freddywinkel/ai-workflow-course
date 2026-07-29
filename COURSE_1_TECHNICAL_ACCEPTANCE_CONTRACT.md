# Course 1 Technical Acceptance and Support Contract

Document ID: `C1-TA`

Version: `1.0`

Effective date: `2026-07-28`

Status: **Normative acceptance baseline; current implementation is unverified
against this baseline**

Owner: Course 1 maintainer

Threat model: `COURSE_1_PRODUCT_THREAT_MODEL.md`

## 1. Purpose

This contract converts the Course 1 product threat model into stable,
testable requirements. It covers the Course 1 runner, learner workspace,
Progressive Web App (PWA), local learning state, dependencies, supported
Windows environment, release evidence, and recovery.

It does not cover Course 4, cloud deployment, live artificial intelligence
(AI), production use, real client data, or external system integration.

The words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** are normative.

Requirement identifiers are permanent. A requirement may be clarified without
changing its identifier only when its acceptance meaning does not change.
Materially changed meaning requires a new identifier. Retired identifiers must
remain listed as retired and must never be reused.

## 2. Acceptance states and evidence rule

Each requirement has one of four evidence states:

- `NOT TESTED`
- `PASS`
- `FAIL`
- `ACCEPTED EXCEPTION`

`PASS` requires the named test evidence from the release candidate. Source
inspection, a phrase in a lesson, a previous version's result, or a learner
attestation cannot substitute for executable evidence where this contract
requires it.

An `ACCEPTED EXCEPTION` must include:

- requirement ID;
- exact affected version and environment;
- reason and impact;
- compensating control;
- owner;
- expiry date no later than 30 days after release;
- explicit release decision.

No exception may authorise real data, paid billing, external action, an
unreviewed dependency, unrelated-file risk, or a known exploitable critical or
high-severity vulnerability.

## 3. Data-boundary requirements

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-DATA-001` | The runner MUST require the exact synthetic-data confirmation and MUST display the selected input and expected-result filenames before the first controlled write. It MUST state that confirmation is an attestation, not proof. | CLI integration tests for absent, wrong, and exact confirmation plus learner-visible output snapshot |
| `C1-TA-DATA-002` | Course 1 MUST use only supplied or learner-created fictional data. The runner and PWA MUST NOT claim to prove that a file contains no real or sensitive data. | Content assertion plus real-looking synthetic misuse fixture that triggers the documented stop/retry path |
| `C1-TA-DATA-003` | If a selected file is unfamiliar or its provenance is uncertain, the documented route MUST preserve it unchanged and use a fresh synthetic retry folder. | Beginner Windows end-to-end scenario and before/after hashes |
| `C1-TA-DATA-004` | Free text from source, reviewer, retry, or backup MUST remain inert. Generated claims MUST be limited to verified structured evidence. CSV exports MUST neutralise formula prefixes after leading whitespace and control characters while JSON retains exact evidence. | Adversarial prose and spreadsheet-formula corpus in unit and end-to-end tests |

## 4. Filesystem and path-confinement requirements

### Supported path model

The controlled runner supports an ordinary local Windows fixed-drive folder on
NTFS. Network shares, Universal Naming Convention (UNC) paths, device
namespaces, alternate data streams, and a controlled root or child implemented
as a symbolic link, junction, mount point, or other reparse point are not
supported in Course 1 and must be rejected safely.

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-FS-001` | Before a read that affects control decisions and before every create, replace, rename, rollback, cleanup, or delete, the runner MUST establish the canonical controlled root and prove that the target is a descendant of that root by filesystem identity, not string prefix alone. | `C1-TST-FS-001`; Windows native containment tests |
| `C1-TA-FS-002` | The controlled root, `runs`, run directory, staging, `source`, `issues`, `draft`, `review`, `audit`, `failures`, and `outbox`, plus every controlled file's parent chain, MUST contain no symbolic link, junction, mount point, or Windows reparse point. | `C1-TST-FS-002`; link/junction/reparse matrix at every component |
| `C1-TA-FS-003` | Every expected file MUST be a regular file and every expected directory MUST be a real directory. File/directory substitutions and special files MUST produce a specific safe stop before mutation. | `C1-TST-FS-003`; substitutions for all controlled roles |
| `C1-TA-FS-004` | The runner MUST detect a target or parent identity change between validation and mutation. A time-of-check/time-of-use (TOCTOU) swap MUST NOT redirect any controlled effect. | `C1-TST-FS-004`; deterministic race injection at every mutation boundary |
| `C1-TA-FS-005` | Recursive cleanup MUST operate only on a newly created internal staging directory with an unguessable name and an ownership marker bound to the current operation. Cleanup MUST never traverse or remove a link/reparse target. | `C1-TST-FS-005`; cleanup and interrupted-staging abuse tests |
| `C1-TA-FS-006` | Rollback and incomplete-marker handling MUST apply the same confinement and no-follow rules as the forward operation. | `C1-TST-FS-006`; injected failure and malicious rollback-target tests |
| `C1-TA-FS-007` | Course 1 MUST reject UNC paths, `\\?\` and `\\.\` device namespaces, alternate data streams, reserved device names, and path components ending in a dot or space before a controlled write. | `C1-TST-FS-007`; Windows path corpus |
| `C1-TA-FS-008` | Case-insensitive path and filename collisions MUST be rejected. The runner MUST behave consistently when Windows preserves case but compares without case. | `C1-TST-FS-008`; collision corpus |
| `C1-TA-FS-009` | A supported learner workspace path MAY contain spaces and Unicode. The complete workspace path MUST be no longer than 175 characters at preflight so every generated path remains below 260 characters. Longer paths MUST stop before mutation with a short-path recovery instruction. | `C1-TST-FS-009`; 174, 175, and 176-character roots plus maximum generated path |
| `C1-TA-FS-010` | Absolute paths and Windows usernames MUST NOT be written to portable review, export, backup, or public evidence. Local failure evidence may contain only a visible basename and a controlled relative locator. | `C1-TST-FS-010`; path-privacy scan across every output |
| `C1-TA-FS-011` | Lock creation, inspection, stale-lock recovery, and release MUST be confined and identity-checked. A lock owned by a live or unverified process MUST NOT be removed automatically. | `C1-TST-FS-011`; live, stale, malformed, replaced, and reparse lock cases |

## 5. Input, resource, and Unicode limits

Limits apply before full parsing or materialisation where technically
possible. A limit failure must use a named safe stop and leave the last valid
state unchanged.

### Runner limits

| ID | Requirement | Limit and behaviour | Required acceptance evidence |
|---|---|---|---|
| `C1-TA-IO-001` | Work-item CSV byte size | Maximum `2 MiB` (`2,097,152` bytes) | Below, exact, and one-byte-over tests |
| `C1-TA-IO-002` | Work-item rows and columns | Exactly 12 headers; maximum `2,000` data rows; no blank trailing record interpreted as work | Boundary and malformed CSV generation |
| `C1-TA-IO-003` | CSV cell size | Maximum `16,384` Unicode code points per cell after strict decoding; no silent truncation | Every column at boundary |
| `C1-TA-IO-004` | Expected-result CSV | Maximum `2 MiB`, `25,000` rows, and `16,384` code points per cell | Boundary and duplicate-key tests |
| `C1-TA-IO-005` | Controlled or candidate JSON file | Maximum `4 MiB` per file, nesting depth `32`, maximum `25,000` array items, maximum `256` object properties, and maximum `65,536` code points per string unless a stricter field contract applies | Generated JSON boundary suite |
| `C1-TA-IO-006` | Audit JSON Lines file | Maximum `16 MiB`, `25,000` non-empty events, and `256 KiB` per line | Boundary, malformed line, and recovery suite |
| `C1-TA-IO-007` | Unexpected stream or special file | Pipes, sockets, devices, sparse abuse, and files that change size or identity during read are unsupported and MUST stop safely | Native special-file and changing-file tests where the operating system permits |
| `C1-TA-IO-008` | Failure output | One malformed input MUST produce bounded output: at most one concise learner message plus controlled failure evidence; no full untrusted content or raw traceback | Output-size and secret/path redaction assertions |

### Encoding and text rules

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-IO-009` | CSV and JSON text MUST decode as strict UTF-8. One leading UTF-8 byte-order mark MAY be accepted; invalid sequences MUST be rejected. | UTF-8 corpus across input roles |
| `C1-TA-IO-010` | U+0000 MUST be rejected. C0 controls other than tab, carriage return, and line feed MUST be rejected in learner-controlled text. | Control-character corpus |
| `C1-TA-IO-011` | Bidirectional formatting and isolation controls U+061C, U+200E–U+200F, U+202A–U+202E, and U+2066–U+2069 MUST be rejected from identifiers, paths, filenames, URLs, decision fields, and generated visible labels. They MAY appear only in quoted raw-source evidence that is never used as an identifier or HTML. | Bidirectional-control corpus |
| `C1-TA-IO-012` | Control identifiers, enum values, dates, currency codes, hashes, run IDs, rule codes, issue IDs, and relative artifact locators MUST use their documented ASCII canonical forms. | Locale-independent contract tests |
| `C1-TA-IO-013` | Free-text Unicode MUST be preserved byte-for-byte in protected source evidence. The runner MUST NOT silently normalise NFC/NFD or convert locale-specific numbers/dates. Validation may trim only where the field contract says so. | Composed/decomposed, accented, emoji, Dutch decimal-comma, and date corpus |

## 6. Capability-denial requirements

The Course 1 runner consists of `course1_capstone/cli.py`,
`course1_capstone/workflow.py`, the Python standard library modules they use,
and any package imported at runtime. The acceptance harness and maintainer
build tools are not part of the runner and must be reported separately.

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-CAP-001` | The runner MUST NOT create IPv4, IPv6, Unix-domain, or other network sockets or perform Domain Name System (DNS) resolution. | `C1-TST-CAP-001`; operating-system-denied egress plus socket/DNS instrumentation for every CLI command |
| `C1-TA-CAP-002` | The runner MUST NOT create a child process, invoke a shell, execute another program, open a browser, or use dynamic code/import to obtain those capabilities. | `C1-TST-CAP-002`; process monitor plus static and runtime instrumentation |
| `C1-TA-CAP-003` | The runner MUST NOT contain or load a provider, e-mail, payment, ordering, source-system approval, webhook, connector, or external write-back client. | `C1-TST-CAP-003`; full runtime dependency/import/call scan |
| `C1-TA-CAP-004` | `EXTERNAL_ACTIONS_ENABLED` MUST remain Boolean `false` in protected control evidence. No environment variable or input may enable an external action. | Existing control-tamper tests plus environment fuzzing |
| `C1-TA-CAP-005` | Runner filesystem writes MUST be limited to the verified controlled workspace. Reads MUST be limited to the named input, expected result, candidate/replacement, runner code/runtime, and controlled workspace. | `C1-TST-CAP-005`; operating-system read/write observation |
| `C1-TA-CAP-006` | Runner console and failure evidence MUST not expose full absolute paths, environment variables, credentials, or untrusted source content. | Redaction corpus and output snapshot |
| `C1-TA-CAP-007` | The PWA is excluded from the runner's no-network claim. It MAY fetch only same-origin public course assets and version metadata and MUST NOT send progress, notes, backup contents, or learner workflow files. | `C1-TST-PWA-NET-001`; browser request interception during every feature |

## 7. PWA storage, privacy, and backup requirements

### Browser-storage boundary

Web Storage is isolated by origin, not URL path. A project path on
`freddywinkel.github.io` is not a storage boundary from sibling projects on
that origin.

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-PWA-001` | On a shared origin, the interface MUST call notes “local learning notes,” not “private” or “confidential,” and MUST prohibit sensitive, real client, employer, workplace, or medical content. | Rendered-text assertion and beginner review |
| `C1-TA-PWA-002` | On a shared origin, the interface MUST explain that browser storage remains in that browser profile but can be accessed by scripts on other pages with the same origin. | Rendered Settings and notes-panel assertion |
| `C1-TA-PWA-003` | A “private notes” claim requires either a dedicated trustworthy origin with no unrelated apps or user-key encryption whose key is never stored on or transmitted to that origin. | Hosting-origin evidence or independent cryptographic design review |
| `C1-TA-PWA-004` | The PWA MUST make zero requests containing progress, notes, preferences, backup content, local file content, or storage identifiers. | Browser network interception on startup, navigation, search, save, backup, import, reset, offline, and update |
| `C1-TA-PWA-005` | Storage failure or quota exhaustion MUST be reported truthfully. In-memory success MUST never be labelled saved. | Denied, full, and disappearing-storage browser tests |
| `C1-TA-PWA-006` | Concurrent browser tabs/windows and installed/browser instances MUST merge non-conflicting progress and notes or present an explicit conflict; they MUST NOT silently replace a newer record. | Multi-context storage-event tests with deterministic interleavings |
| `C1-TA-PWA-007` | Progress and note records MUST have a monotonically comparable revision or timestamp plus writer identity sufficient to detect stale replacement. Clock rollback MUST not defeat conflict detection. | Property/state-machine tests |

### Backup limits and transaction

| ID | Requirement | Limit or behaviour | Required acceptance evidence |
|---|---|---|---|
| `C1-TA-PWA-008` | Backup file size | Maximum `5 MiB` (`5,242,880` bytes), checked before `file.text()` or JSON parsing | Exact browser file-boundary test |
| `C1-TA-PWA-009` | Backup JSON complexity | Maximum depth `12`, `500` properties in any object, and `500` items in any array | Generated hostile-backup corpus |
| `C1-TA-PWA-010` | Backup notes | Maximum `50,000` code points per note and `1,000,000` total note code points; unknown archived notes count maximum `100` | Boundary and over-limit tests |
| `C1-TA-PWA-011` | Backup schema | Exact supported export type, course ID, state schema, closed allowlisted keys, safe ordinary object prototypes, known document/group IDs, bounded values, and no `__proto__`, `prototype`, or `constructor` keys | Prototype-pollution and unknown-key corpus |
| `C1-TA-PWA-012` | Import transaction | Parse and validate without modifying current state; show a bounded preview; require explicit replacement; persist candidate; reload/read it back; only then replace visible state | Failure injection at every import step |
| `C1-TA-PWA-013` | Import rollback | On validation, storage, render, or readback failure, rollback MUST compare each transaction-owned storage key separately. It restores the snapshot only when the current value still equals the transaction-owned value or already equals the snapshot; a value that differs from both is an external change and MUST be preserved. Primary state, reset barrier, recovery, runtime state, route, visible render, and overall verification MUST be reported separately. An external primary-state or reset-barrier value requires reconciliation and MUST NOT be called a fully verified rollback; an external recovery value may be preserved while the other exact dimensions are verified. | Deterministic per-key before/owned/external/after evidence, render-failure injection, and harness-attribution assertions |
| `C1-TA-PWA-014` | Export | Export MUST include a schema/version, course ID, export timestamp, bounded state, and no build secret, absolute local path, browser fingerprint, credential, or unrelated storage | Closed-schema and privacy scan |

## 8. Web rendering and navigation requirements

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-WEB-001` | Markdown, course metadata, error messages, search excerpts, imported strings, and notes MUST be treated as untrusted at every HTML, attribute, URL, style, and text sink. | Sink inventory plus adversarial browser corpus |
| `C1-TA-WEB-002` | The app MUST use context-correct escaping or a reviewed sanitizer. No untrusted string may reach `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, dynamic script/style creation, `eval`, `Function`, or string timers without a proved-safe transformation. | Static sink gate and mutation tests |
| `C1-TA-WEB-003` | Adversarial HTML, SVG, MathML, event-handler, entity, token-collision, malformed-tag, and attribute-breakout payloads MUST remain inert in headings, paragraphs, lists, tables, links, code, metadata, and search. | `C1-TST-WEB-003`; maintained payload corpus in real browsers |
| `C1-TA-WEB-004` | A Content Security Policy (CSP) MUST effectively enforce at least: `default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; manifest-src 'self'; connect-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'`. Inline executable script/style MUST not require `unsafe-inline`. `frame-ancestors 'none'` MUST be delivered as a response header when the host supports headers. | Browser CSP violation collection and live response/header inspection |
| `C1-TA-WEB-005` | Course links MAY use internal fragments/relative course paths or external `https:` URLs. `http:`, `javascript:`, `data:`, `blob:`, `file:`, `vbscript:`, protocol-relative, credential-bearing, control-character, and encoded-scheme bypasses MUST be rejected. | URL-parser differential corpus in browser and unit tests |
| `C1-TA-WEB-006` | External links MUST use a new context with `noopener noreferrer`; URLs MUST contain no progress, notes, local path, or learner identifier. | DOM and navigation-request assertions |
| `C1-TA-WEB-007` | Repository fallback links MUST be constructed from an allowlisted repository base and a normalised repository-relative path that cannot escape with `..`, encoded separators, fragments, or alternate origins. | Path/URL escape corpus |
| `C1-TA-WEB-008` | Notes MUST be rendered only as text or editable form value, never as Markdown or HTML. | Stored payload reopen test |

## 9. Service-worker and release-coherence requirements

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-SW-001` | The service worker MUST intercept only same-origin requests whose normalised path is inside the exact Course 1 scope path segment. | Scope/path corpus including prefix look-alikes and encoded paths |
| `C1-TA-SW-002` | Precache and runtime cache MUST use an explicit generated allowlist. The worker MUST NOT cache arbitrary same-scope requests. | Request/caching inventory test |
| `C1-TA-SW-003` | Before caching, each response MUST be successful, non-opaque, non-redirected, same-origin, from the expected final URL, and have an allowlisted content type. | Redirect, error-page, opaque, wrong-URL, and wrong-type server scenarios |
| `C1-TA-SW-004` | Executable and content assets MUST be bound to the expected build ID and content hashes. The application shell, course bundle, version metadata, and worker MUST agree before a candidate can activate. | Mixed-release and single-byte-tamper tests |
| `C1-TA-SW-005` | Installation MUST populate a candidate cache and delete it on any failure. A partial candidate MUST never replace the last valid active cache. | Failure at every precache request |
| `C1-TA-SW-006` | `SKIP_WAITING` or equivalent activation MUST be accepted only for a fully verified waiting worker and a message from a controlled in-scope client following explicit learner action. | Foreign/sibling client and unsolicited-message tests |
| `C1-TA-SW-007` | Activation MUST delete only obsolete Course 1 caches with the exact owned prefix and MUST preserve unrelated origin caches. | Cache inventory before/after |
| `C1-TA-SW-008` | A controlled update MUST preserve valid progress, practical records, notes, preferences, and unrelated caches; conflict handling remains subject to `C1-TA-PWA-006`. | Old-to-new multi-context update test |
| `C1-TA-SW-009` | If candidate validation or activation fails, the old release MUST cold-reopen online and offline and the learner MUST receive a truthful recovery message. | Interrupted and corrupt-update tests |
| `C1-TA-SW-010` | Navigation fallback MUST return only the verified current application shell. An unexpected page or server error MUST not be stored as the shell. | Online/offline navigation and server-error matrix |

## 10. Dependency, supply-chain, and provenance requirements

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-SC-001` | Every direct and transitive Python dependency MUST have an exact version and SHA-256 hashes for every accepted platform artifact. Installation MUST use hash-required mode and the intended package index. | Clean install with `--require-hashes`; altered-wheel negative test |
| `C1-TA-SC-002` | JavaScript dependencies MUST be lockfile-pinned with integrity values. A dependency-free PWA MUST still record an empty dependency inventory. | Lock verification and dependency inventory |
| `C1-TA-SC-003` | A machine-readable Software Bill of Materials (SBOM) in CycloneDX or SPDX format MUST cover Course 1 Python, Node, GitHub Action, browser-test, and build dependencies. | Schema-valid SBOM attached to release evidence |
| `C1-TA-SC-004` | Release validation MUST scan all dependency versions against current Open Source Vulnerabilities (OSV), GitHub advisories, and an appropriate Python audit source no more than 7 days before release. | Dated machine-readable scan reports |
| `C1-TA-SC-005` | No affected dependency with a known critical/high vulnerability may pass. A known moderate vulnerability with a fixed compatible release MUST be updated before release; otherwise it requires a time-limited exception and compensating control. | Vulnerability-gate negative fixture |
| `C1-TA-SC-006` | Every dependency licence MUST be identified and compatible with repository use and redistribution. Unknown, prohibited, or conflicting licences block release. | Dated licence inventory and policy result |
| `C1-TA-SC-007` | Every GitHub Action MUST be pinned to a reviewed full commit SHA, with repository owner and expected release tag recorded. Workflow permissions MUST be least privilege per job. | Workflow scanner and permission review |
| `C1-TA-SC-008` | Continuous-integration runner image and Python/Node/browser toolchains MUST use explicit supported identities, not an unbounded `latest` contract. Exact resolved versions MUST be recorded in evidence. | Run metadata and configuration scan |
| `C1-TA-SC-009` | Builds and tests MUST run without repository secrets, cloud credentials, paid billing authority, or live provider access. | Environment-name allowlist and secretless CI result |
| `C1-TA-SC-010` | Release evidence MUST map source commit, workflow run, dependency lock/SBOM hash, build ID, content hash, artifact hashes, deployment identifier, and public URL. | Machine-readable provenance manifest |
| `C1-TA-SC-011` | The public artifact MUST be re-downloaded and compared with the accepted artifact or its signed hash manifest after deployment. | Post-deploy comparison report |
| `C1-TA-SC-012` | Dependency and Action advisories MUST be rescanned at least monthly and immediately before a new release. A critical/high advisory triggers a release review and, where relevant, rollback or warning. | Scheduled workflow history and incident procedure |

## 11. Independent testing and oracle requirements

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-TEST-001` | Rule behaviour MUST have an independently reviewed decision table covering normal, boundary, invalid, and combined cases. It MUST not be generated by the runner under test. | Signed/reviewed oracle artifact and review record |
| `C1-TA-TEST-002` | At least one test adapter MUST evaluate the independent oracle without importing runner rule functions or constants. | Test dependency/import inspection |
| `C1-TA-TEST-003` | Parser, lifecycle, approval, audit, rollback, path, storage, renderer, and service-worker properties MUST have generated property-based tests and a persistent minimal regression corpus. | Seeded/reproducible test report and corpus |
| `C1-TA-TEST-004` | Security-critical runner and PWA modules MUST report line and branch coverage. Branch coverage below `90%` or any identified critical branch without a test blocks release. | Coverage report mapped to critical-branch inventory |
| `C1-TA-TEST-005` | Mutation testing MUST cover deterministic rules, approval binding, audit reconciliation, transaction rollback, path guards, Markdown/URL safety, backup validation, storage conflict logic, and service-worker identity. Surviving security-relevant mutants block release. | Mutation report with reviewed exclusions |
| `C1-TA-TEST-006` | Tests MUST deliberately seed at least one known defect in every critical control family and prove the release gate fails. | Negative-control report |
| `C1-TA-TEST-007` | A test count is supporting information only. Acceptance MUST require the exact named scenario inventory and detect removal, skip, expected failure, or non-execution. | Test manifest comparison and skip/failure gate |
| `C1-TA-TEST-008` | Unit tests, clean-room tests, native Windows tests, browser tests, and live artifact tests MUST remain separate evidence layers. One layer cannot substitute for another. | Release evidence index |
| `C1-TA-TEST-009` | Fuzz, property, mutation, and coverage tools are maintainer dependencies and MUST NOT become beginner prerequisites. | Learner dependency-set assertion |

## 12. Windows, locale, filesystem, and browser support matrix

### Learner runner: release-blocking matrix

| ID | Required environment |
|---|---|
| `C1-TA-WIN-001` | Windows 11 on a supported Microsoft build, 64-bit, ordinary local NTFS fixed drive |
| `C1-TA-WIN-002` | Windows PowerShell 5.1 with execution policy `Restricted`; no environment activation script required |
| `C1-TA-WIN-003` | Official Python Install Manager route with supported CPython 3.14 stable, invoked through the exact project interpreter |
| `C1-TA-WIN-004` | CPython 3.12, 3.13, and 3.14 automated compatibility matrix; at least 3.14 must run natively on Windows |
| `C1-TA-WIN-005` | Git current supported Windows stable used by setup; no remote is required for Course 1 |
| `C1-TA-WIN-006` | `nl-NL` and `en-US` Windows regional formats; Europe/Amsterdam and UTC time zones; all data dates remain ISO `YYYY-MM-DD`, timestamps remain explicit UTC, and decimal input remains period-based by contract |
| `C1-TA-WIN-007` | Workspace paths with spaces, parentheses, hyphens, accented Latin characters, and one non-Latin character, within the 175-character root budget |
| `C1-TA-WIN-008` | Read-only or denied folder, full disk/quota simulation, file locked by another process, and antivirus-style transient denial |
| `C1-TA-WIN-009` | OneDrive/cloud-synchronised or reparse-backed workspace is detected as unsupported and routes to a verified ordinary local folder without moving or deleting existing content |
| `C1-TA-WIN-010` | Fresh shell reopen: setup, tests, prepare, inspect, decide, revise/validate where applicable, export, failure recovery, and retry use no hidden PATH or session state |
| `C1-TA-WIN-011` | Beginner follows only published commands from a clean learner account without administrator rights after the official Python installation step |
| `C1-TA-WIN-012` | Windows restart/crash simulation or process termination at durable-write boundaries results in the recovery contract, not silent corruption |

The learner-facing course does not promise Linux or macOS runner support.
Maintainer Linux continuous integration is additional portability evidence,
not a substitute for native Windows acceptance.

### PWA: release-blocking browser matrix

| ID | Required environment and capability |
|---|---|
| `C1-TA-BR-001` | Current stable Google Chrome on Windows 11: browser and installed-PWA modes |
| `C1-TA-BR-002` | Current stable Microsoft Edge on Windows 11: browser and installed-PWA modes |
| `C1-TA-BR-003` | Automated Chromium on the fixed CI runner: unit, six responsive viewports, accessibility, offline, storage, backup, conflict, CSP, and controlled update |
| `C1-TA-BR-004` | Current stable Firefox on Windows: online reader, search, progress/notes, backup/import/reset, keyboard and responsive layout; install is not promised |
| `C1-TA-BR-005` | Current Safari on iOS and current Chrome on Android: reading, search, notes warning, backup export where supported, responsive layout, and offline/home-screen behaviour only if the interface claims it |
| `C1-TA-BR-006` | Keyboard-only, 200% browser zoom, 125% reader text, reduced motion, forced colours where supported, light/dark/system themes, and screen-reader smoke on Windows |
| `C1-TA-BR-007` | Storage disabled, quota exhausted, storage cleared between opens, private-browsing limitations, and service worker unavailable |
| `C1-TA-BR-008` | Exact browser and operating-system versions, mode, viewport, locale, and result recorded in release evidence |

Mobile browsers are reading companions. Course execution and final Course 1
acceptance require the supported Windows computer.

## 13. Recovery requirements

| ID | Requirement | Required acceptance evidence |
|---|---|---|
| `C1-TA-REC-001` | Original selected inputs MUST remain unchanged in every success and failure path. | Hash inventory before/after every scenario |
| `C1-TA-REC-002` | A controlled mutation MUST be atomic or byte-for-byte reversible. Failure before commit leaves the previous valid state; failure after an unrecoverable partial effect leaves a blocking marker. | Failure injection at every durable write |
| `C1-TA-REC-003` | Rollback MUST itself be confinement-checked. If rollback cannot prove restoration, no further run operation may proceed. | Malicious path and rollback-failure scenarios |
| `C1-TA-REC-004` | Damaged state, audit, evaluation, decision, or export MUST produce independent bounded failure evidence without relying on the damaged file. | Corruption corpus |
| `C1-TA-REC-005` | Stale-lock recovery MUST require proof that no live operation owns the lock, preserve the old lock as evidence, and give beginner-safe steps. | Restart/live-PID/malformed-lock scenarios |
| `C1-TA-REC-006` | Idempotent retry MUST create no duplicate run, decision, audit effect, or export and MUST not mutate already valid protected evidence. | Multi-process retry hashes and counts |
| `C1-TA-REC-007` | PWA state migration/import MUST preserve a recoverable pre-change backup until the new state is saved, read back, and rendered successfully. Failure uses the per-key compare-and-preserve and separate-result contract in `C1-TA-PWA-013`; “exact rollback” applies only to keys that remain transaction-owned, not to an external concurrent value that must be preserved. | Failure injection plus per-key rollback and reconciliation evidence |
| `C1-TA-REC-008` | PWA reset MUST name everything removed, require confirmation, report storage failure honestly, and explain recovery from an exported backup. | Browser reset/storage-denial test |
| `C1-TA-REC-009` | Failed PWA update MUST retain the last valid offline release and learner state. A public rollback MUST not require clearing all browser data. | Old-client failure and rollback test |
| `C1-TA-REC-010` | Release rollback MUST identify the last accepted commit/build, redeploy it, verify public assets, and preserve compatible learner state. | Rehearsed rollback report |

## 14. Technical test manifest

These 33 test IDs are the minimum named evidence set. The closed machine mirror
is `audit_control/course1/technical_test_manifest.json`; its bidirectional
requirement edges are in
`audit_control/course1/technical_requirement_graph.json`. Test filenames may
change, but the identifiers and intent may not.

| Test ID | Type | Requirements covered | Required scenario |
|---|---|---|---|
| `C1-TST-DATA-001` | Unit and native beginner Windows | `C1-TA-DATA-001`–`C1-TA-DATA-004` | Synthetic attestation, uncertain provenance, source preservation, inert prose, and formula-safe export |
| `C1-TST-FS-001` | Native Windows integration | `C1-TA-FS-001` | Canonical containment by filesystem identity |
| `C1-TST-FS-002` | Native Windows integration | `C1-TA-FS-002` | Every controlled path component rejects links, junctions, mounts, and reparse points |
| `C1-TST-FS-003` | Native Windows integration | `C1-TA-FS-003` | File/directory/special-file substitutions stop before mutation |
| `C1-TST-FS-004` | Native Windows adversarial | `C1-TA-FS-004` | Deterministic time-of-check/time-of-use swap at every mutation boundary |
| `C1-TST-FS-005` | Native Windows adversarial | `C1-TA-FS-005` | Owned staging cleanup and interrupted-staging abuse matrix |
| `C1-TST-FS-006` | Native Windows adversarial | `C1-TA-FS-006` | Malicious rollback and incomplete-marker target matrix |
| `C1-TST-FS-007` | Native Windows table | `C1-TA-FS-007` | UNC, namespace, alternate-data-stream, reserved-name, dot, and space corpus |
| `C1-TST-FS-008` | Native Windows table | `C1-TA-FS-008` | Case-insensitive path and filename collision corpus |
| `C1-TST-FS-009` | Native Windows table | `C1-TA-FS-009` | 174-, 175-, and 176-character roots plus maximum generated path |
| `C1-TST-FS-010` | Output privacy scan | `C1-TA-FS-010` | Every portable output excludes usernames and absolute paths |
| `C1-TST-FS-011` | Native Windows lock table | `C1-TA-FS-011` | Live, stale, malformed, replaced, and reparse-backed lock cases |
| `C1-TST-IO-001` | Property/fuzz | `C1-TA-IO-001`–`C1-TA-IO-008` | Byte/row/cell/depth/count boundaries and malformed corpus |
| `C1-TST-IO-002` | Property/fuzz on Windows locales | `C1-TA-IO-009`–`C1-TA-IO-013`, `C1-TA-WIN-006`–`C1-TA-WIN-007` | UTF-8, control, bidi, NFC/NFD, path and locale corpus |
| `C1-TST-CAP-001` | Native Windows monitored clean room | `C1-TA-CAP-001`, `C1-TA-CAP-004`, `C1-TA-CAP-006` | Denied network and DNS plus protected-control and redacted-output observation for every CLI command |
| `C1-TST-CAP-002` | Native Windows process monitor | `C1-TA-CAP-002` | Child-process, shell, executable, browser, and dynamic-code attempts are denied and detected |
| `C1-TST-CAP-003` | Runtime dependency and call scan | `C1-TA-CAP-003` | Provider, e-mail, payment, ordering, connector, and write-back clients are absent |
| `C1-TST-CAP-005` | Native Windows filesystem monitor | `C1-TA-CAP-005` | Observed reads and writes remain inside the exact allowlisted set |
| `C1-TST-PWA-NET-001` | Real browser interception | `C1-TA-CAP-007`, `C1-TA-PWA-004` | All PWA features transmit no learner state |
| `C1-TST-PWA-STORAGE-001` | Multi-browser state machine | `C1-TA-PWA-001`–`C1-TA-PWA-007` | Shared origin, conflict, stale writer, quota, and wording |
| `C1-TST-PWA-BACKUP-001` | Real browser property/adversarial | `C1-TA-PWA-008`–`C1-TA-PWA-014` | Exact limits, prototype pollution, rollback, and privacy |
| `C1-TST-WEB-001` | Static sink and URL analysis | `C1-TA-WEB-001`–`C1-TA-WEB-008` | Complete sink inventory and prohibited API/scheme gate |
| `C1-TST-WEB-002` | Real browser adversarial | `C1-TA-WEB-001`–`C1-TA-WEB-008` | Maintained XSS/URL payload corpus and note reopen |
| `C1-TST-WEB-003` | Real browser adversarial corpus | `C1-TA-WEB-003` | HTML, SVG, MathML, event-handler, entity, token, malformed-tag, and attribute-breakout payloads remain inert |
| `C1-TST-SW-001` | Controlled HTTP server/browser | `C1-TA-SW-001`–`C1-TA-SW-006` | Scope, response, hash, partial install, and message abuse |
| `C1-TST-SW-002` | Old-client update/rollback | `C1-TA-SW-007`–`C1-TA-SW-010`, `C1-TA-REC-009` | Preserve state/caches and recover from every failed candidate |
| `C1-TST-SC-001` | CI supply-chain gate | `C1-TA-SC-001`–`C1-TA-SC-009` | Hash, SBOM, vulnerability, licence, Action, image, and secretless build |
| `C1-TST-PROV-001` | Post-deploy | `C1-TA-SC-010`–`C1-TA-SC-012`, `C1-TA-REC-010` | Provenance manifest, public byte/hash comparison, rollback, and a separate final verifier requiring the exact all-33 evidence set |
| `C1-TST-ORACLE-001` | Independent evaluator | `C1-TA-TEST-001`–`C1-TA-TEST-002` | Decision table does not import runner rules |
| `C1-TST-QUALITY-001` | CI quality | `C1-TA-TEST-003`–`C1-TA-TEST-009` | Property, coverage, mutation, negative control, manifest, and learner-dependency isolation |
| `C1-TST-WIN-E2E-001` | Native beginner Windows | `C1-TA-WIN-001`–`C1-TA-WIN-012`, `C1-TA-DATA-001`–`C1-TA-DATA-003` | Clean account from official setup through recovery and shell reopen |
| `C1-TST-BROWSER-MATRIX-001` | Browser/device matrix | `C1-TA-BR-001`–`C1-TA-BR-008` | Exact required browser, mode, accessibility, storage, and viewport evidence |
| `C1-TST-RECOVERY-001` | Failure injection/state machine | `C1-TA-REC-001`–`C1-TA-REC-008` | Every durable-write boundary, corruption, lock, retry, migration, and reset |

## 15. Release acceptance sequence

A Course 1 release may be called technically accepted only in this order:

1. Freeze the release candidate, threat-model version, requirement manifest,
   independent decision table, and dependency locks.
2. Run static contract, schema, source, and sink checks.
3. Run unit, property, fuzz, coverage, mutation, and negative-control tests.
4. Run monitored runner clean rooms on the supported Python matrix.
5. Run native Windows filesystem, locale, failure, and beginner end-to-end
   acceptance.
6. Run PWA unit, adversarial security, storage, browser, accessibility,
   offline, and controlled-update tests.
7. Produce dependency scan, licence inventory, SBOM, and provenance manifest.
8. Build once from the accepted source and publish that exact artifact.
9. Re-read the public artifact and verify hashes, policy, browser behaviour,
   old-client update, and rollback path.
10. Record every requirement as `PASS`, `FAIL`, or a permitted
    `ACCEPTED EXCEPTION`.
11. Use an independent final reviewer who did not implement the repair to
    decide whether the complete evidence supports release.

A green package validator, a test count, or a successful deployment is not by
itself a technical acceptance decision.

## 16. Support statement

At Course 1 scope:

- learner execution is supported only on the release-blocking Windows matrix;
- the runner is synthetic-only, local-only, and has no external-action
  capability;
- the PWA is a course reader and local learning-state tool, not a confidential
  records system;
- mobile is a reading companion, not the Course 1 execution environment;
- cloud-synchronised/reparse-backed workspaces, network shares, real data,
  connectors, provider calls, and production use are unsupported;
- passing this contract does not prove production security or legal
  compliance.

Any proposal to add real data, a live AI provider, cloud runtime, connector,
external action, multi-user access, or production use requires a new scope,
threat model, authority decision, and later-course acceptance contract.
