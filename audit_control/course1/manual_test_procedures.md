# Course 1 technical manual and hybrid test procedures

These are maintainer procedures, not learner prerequisites. Each run uses only
synthetic data and writes evidence to a fresh candidate-bound evidence folder.
Record the exact candidate identity, environment, command or procedure, result,
timestamp, reviewer, and raw artifact hash. `UNVERIFIED` remains the status
until the complete named procedure has reproducible evidence.

## C1-TST-DATA-001

Run the clean-room suite, then repeat the synthetic-attestation, uncertain-file,
source-hash, inert-prose, and formula-export cases on native learner Windows.
Pass only when the original hashes remain exact and no real-data claim is made.

## C1-TST-FS-001

Create an ordinary NTFS controlled root plus a same-prefix external sibling.
Exercise every control-affecting read and mutation target. Seed one identity
escape and prove the gate fails before external effect.

## C1-TST-FS-002

Place a symbolic link, junction, mount, or reparse point at each controlled
root, parent, and child role one at a time. Every case must stop before read,
write, replace, cleanup, rollback, or deletion outside the ordinary tree.

## C1-TST-FS-003

Replace each expected regular file with a directory or special file and each
expected directory with a file. Require the named type-mismatch stop and exact
prior-state hashes.

## C1-TST-FS-004

Use a deterministic barrier to swap every verified file or parent between
validation and mutation. Pass only when the identity change is detected and no
operation follows the replacement target.

## C1-TST-FS-005

Exercise owned, unowned, interrupted, malformed-marker, and reparse-backed
staging folders. Cleanup may remove only the newly created transaction-owned
staging tree and must leave every other path byte-identical.

## C1-TST-FS-006

Inject failures that enter rollback and incomplete-marker handling, including a
malicious replacement target. Require the same identity and no-follow checks as
the forward path and a blocking marker whenever restoration is unproved.

## C1-TST-FS-007

Run the complete UNC, device namespace, extended namespace, alternate data
stream, reserved device name, trailing dot, and trailing space corpus. Every
unsupported case must stop before controlled mutation.

## C1-TST-FS-008

Create case-only collisions for every controlled filename and directory role.
Pass only when Windows-preserved spelling cannot create two logical identities.

## C1-TST-FS-009

Run complete workspace roots of 174, 175, and 176 characters and the maximum
generated child. Record the exact lengths; 174 and 175 follow the documented
contract and 176 stops before mutation with the short-path recovery instruction.

## C1-TST-FS-010

Scan every review, export, backup, console, failure, and public-evidence output
for the actual username, drive-root path, and seeded alternate absolute paths.
Portable artifacts may retain only neutral basenames and controlled locators.

## C1-TST-FS-011

Exercise live-owner, exited-owner, unverified process, stale, malformed,
replaced, and reparse-backed locks with multiple processes. Never remove a live
or unverified lock automatically; preserve proved-stale lock evidence.

## C1-TST-IO-001

Run seeded property/fuzz generation at limit-minus-one, exact-limit, and
limit-plus-one for every byte, row, field, string, array, depth, audit, and
backup boundary. Retain minimized failures in a persistent regression corpus.

## C1-TST-IO-002

On `nl-NL` and `en-US`, run invalid UTF-8, optional byte-order mark, NUL,
control, bidirectional, composed/decomposed Unicode, quoted newline, date,
decimal, and supported path cases. Compare exact outputs across locales.

## C1-TST-CAP-001

Deny network and Domain Name System access at the operating-system boundary,
instrument every command, fuzz the external-action environment, and scan
console/failure output. Require zero socket/DNS attempts, immutable `false`
control evidence, and no secret or absolute-path disclosure.

## C1-TST-CAP-002

Monitor every command for child process, shell, executable, browser, dynamic
code, and dynamic import activity. Seed each prohibited attempt and prove both
the operating system and acceptance gate detect it.

## C1-TST-CAP-003

Inventory the complete runtime dependency/import/call graph and instrument
execution for provider, e-mail, payment, order, approval, webhook, connector,
and write-back clients. The accepted observed set must be empty.

## C1-TST-CAP-005

Use an operating-system filesystem monitor for every command and failure path.
Compare canonical reads and writes with the exact allowlist; any extra access,
including a dependency access, blocks.

## C1-TST-PWA-NET-001

Intercept requests while exercising every reader, search, progress, note,
backup, import, reset, offline, and update feature in each required browser
mode. Only same-origin public assets/version metadata may be requested, and no
learner state may appear in a URL, header, or body.

## C1-TST-PWA-STORAGE-001

Run the full multi-window and installed/browser storage state machine: shared
origin, distinct writers, non-conflicting merge, same-key conflict, stale
writer, quota/denial, import/reset rollback, and honest privacy wording.

## C1-TST-PWA-BACKUP-001

Run exact byte, property, item, string, total-note, depth, prototype-key,
version, unknown-key, duplicate-ID, archived-note, and forged-document
boundaries in real browsers. Failed import must leave current durable state and
render exact; portable output must pass the privacy scan.

## C1-TST-WEB-001

Inventory every untrusted-to-HTML/attribute/URL/style/text sink and prohibited
dynamic API. Run the complete accepted/rejected URL differential corpus. An
unknown sink, unsafe API, or scheme bypass blocks.

## C1-TST-WEB-002

Run the maintained cross-browser HTML/URL corpus through all render locations,
including saved-note reopen and search. Collect runtime execution, navigation,
Content Security Policy, referrer, and opener observations.

## C1-TST-WEB-003

Exercise named HTML, SVG, MathML, event-handler, entity, token-collision,
malformed-tag, and attribute-breakout payloads in headings, paragraphs, lists,
tables, links, code, metadata, search, and notes. All payloads remain inert.

## C1-TST-SW-001

Serve valid, redirected, opaque, wrong-type, wrong-build, corrupt, missing,
mixed, interrupted, and foreign-message candidates. Verify scope, URL,
response, content type, build identity, hash, temporary cache, and atomic
activation for every asset.

## C1-TST-SW-002

Start from the exact immutable prior public client in browser and installed
modes. Exercise Later, Update now, corrupt candidates, offline reopen, and
controlled rollback. Preserve learner state, unrelated caches, and the last
valid release without clearing all browser data.

## C1-TST-SC-001

In secretless continuous integration, install exact accepted-platform artifacts
with required hashes, validate JavaScript integrity, the full Software Bill of
Materials, licences, advisories, Action pins, resolved toolchains, permissions,
and prohibited environment names. Seed a failure in every supply-chain gate.

## C1-TST-PROV-001

Bind source commit/tree, workflow run, dependency lock and Software Bill of
Materials hashes, build/content/asset/tree identities, deployment ID, and
public URL. Redownload and compare public bytes, verify scheduled advisory
history, then rehearse an exact last-known-good rollback. Create the closed
post-deployment final record from the tracked template and run
`tools/verify_course1_final_acceptance.py` (or the dedicated final-adjudication
workflow) against the preserved promotion artifact, prior promotion record,
authoritative pre-final ledger, and evidence commit. It must require exactly
all 33 declared technical test records, with `C1-TST-PROV-001` recorded no
earlier than the named deployment.

## C1-TST-ORACLE-001

Have an independent reviewer inspect the decision table and evaluator import
graph, then run normal, boundary, invalid, and combined cases. The evaluator
must not import runner rule functions/constants and disagreements are retained.

## C1-TST-QUALITY-001

Run persistent property/fuzz, critical line/branch coverage, mutation testing,
and one known defect for every critical product/audit family. Require the exact
named inventory across separate evidence layers and prove maintainer tools are
absent from learner prerequisites.

## C1-TST-WIN-E2E-001

From a fresh non-admin Windows account, use the published restricted-PowerShell
route and exact project interpreter. Cover Python 3.12–3.14, Git, locales,
timezones, supported paths, denial/lock/full-disk/transient failure, reparse
redirection, fresh-shell reopen, restart/crash, recovery, and retry.

## C1-TST-BROWSER-MATRIX-001

Record exact browser/operating-system version, mode, viewport, locale, and
result for Chrome and Edge browser/installed modes, fixed CI Chromium, Firefox,
iOS Safari, Android Chrome, keyboard, zoom/text, motion, forced colours,
themes, screen reader, storage denial/clearing/private mode, and unavailable
service worker.

## C1-TST-RECOVERY-001

Inject failure at every durable runner and PWA write boundary plus corruption,
lock, retry, migration, and reset cases. Record primary, barrier, recovery,
runtime, render, and harness effects separately; preserve external concurrent
writes and retain either the last valid state or an explicit blocking marker.
