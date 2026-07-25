# Course Changelog

This file records issued course changes. Dated audit reports belong in `updates/`.

## 1.2.1 — 2026-07-25

Visual-design and accessibility release.

Changed:

- rebuilt the home screen around a course-specific source → extraction →
  human-review → approved-output visual;
- replaced equal-weight statistics with a prominent overall progress ring and
  separate foundation/build-week progress;
- replaced platform-dependent interface glyphs with one offline inline-SVG
  icon system;
- strengthened card hierarchy, spacing, motion, touch feedback, light/dark
  surfaces, and the iPhone/iPad navigation treatment;
- widened the mobile/tablet shell breakpoint so an 834-pixel iPad uses the
  focused drawer and bottom navigation;
- reduced technical noise in lesson metadata and constrained prose to a more
  readable line length;
- improved the next-step path, source-currency card, search results, settings,
  notes, and previous/next lesson controls.

Fixed:

- dark-theme secondary buttons no longer inherit near-invisible dark text;
- course progress now exposes real progressbar semantics;
- route changes move keyboard focus meaningfully;
- the mobile course drawer has an explicit close control and focus containment;
- search result counts are announced, hidden file import receives a visible
  focus state, and code-copy/range controls meet the 44-pixel target;
- the skip link stays fully outside the iOS status area until keyboard focus
  makes it relevant;
- the mobile tab bar is docked to the viewport edge, fills the bottom safe
  area, and no longer lets course content show beneath its floating gap.

## 1.2.0 — 2026-07-25

Course-reader and maintained-publication release.

Added:

- a dependency-free iPhone/iPad/desktop PWA generated directly from the course
  Markdown;
- full-course search, a glossary path, local completion tracking, private
  device notes, progress export/import, themes, and adjustable text size;
- an iOS/iPadOS installation guide and offline core-reading cache;
- a learner-controlled waiting-service-worker update prompt;
- deterministic PWA content hashes, generated PNG/maskable icons, and eleven
  build/update/accessibility tests;
- a GitHub Pages workflow that validates the course, tests the PWA, builds the
  repository subpath, and deploys only after every gate passes;
- an eight-week Codex maintenance schedule that runs the evergreen official-
  source audit and publishes only verified, allowlisted, tested course edits.

Verified:

- desktop, 390-pixel phone, and iPad responsive layouts without horizontal
  overflow;
- course navigation, full-text search, Week 7 update checkpoint, local progress
  and note persistence;
- a real old-worker → waiting-worker prompt → learner activation → new-version
  reload sequence;
- current GitHub Pages action majors, Apple installation steps, and Codex
  scheduled-task constraints against official sources.

## 1.1.0 — 2026-07-25

Beginner-accessibility revision.

Added:

- an eight-chapter pre-Week-1 foundation sequence for a learner with no coding
  or command-line experience;
- a plain-language glossary;
- PowerShell copy/paste, error-reporting, stop, and destructive-command safety;
- first-Python, API/JSON, Git, AI/document-workflow, n8n/Docker/database, and
  safe vibe-coding lessons;
- reusable AI-assistance and debugging records;
- an explicit beginner-readiness audit and self-check gate;
- explicit beginner checkpoints in every project week.

Changed:

- removed prior technical knowledge as an assumed prerequisite;
- clarified that complete beginners may need extra time or two calendar weeks
  for one formal course week;
- annotated the Windows setup to distinguish commands, file content, output,
  long-running servers, and verification checks.

## 1.0.0 — 2026-07-25

Initial standalone course release.

Added:

- 12 build weeks at 8–10 hours each with consistent outcome, concepts, official readings, guided build, capstone increment, artifact, gate, failure, and time sections;
- Windows setup based on observed local preflight state;
- canonical n8n/Python/FastAPI/Pydantic/Docling/pytest/OpenAI Responses/Supabase path;
- six portable contracts, state machine, and approval/idempotency invariants;
- synthetic supplier-review capstone and reproducible frozen 20-case corpus;
- local vendor-neutral JSONL evaluation contract;
- AVG/AI Act/legal-status engineering week;
- security, failure, observability, restoration, deletion, and clean-start requirements;
- templates, schemas, software matrix, stack manifest, source register, and evergreen audit prompt.

Dated source decisions:

- Responses selected; Assistants excluded because of its 2026-08-26 shutdown.
- Hosted OpenAI Evals excluded because of 2026-10-31 read-only and 2026-11-30 shutdown dates.
- GPT-5.6 Terra/Luna selected as configurable benchmark candidates; Sol optional as quality ceiling.
- Regulation (EU) 2026/1744 recorded as adopted/published but not yet in force on audit date; entry into force 2026-07-27.
- Article 50 general application date recorded as 2026-08-02 with limited transition explained.
- Amended high-risk dates recorded generally as 2027-12-02 for Annex III systems and 2028-08-02 for Annex I product systems, subject to exact scope.
- Dutch supervisory/proposal and consultation material labelled according to non-final status.

Validation state:

- generated structural, schema, JSON/JSONL/YAML, internal-link, and corpus-integrity results are in [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md);
- deterministic regeneration, official-link audit, and visual review of every rendered corpus page are recorded separately in [`RELEASE_VALIDATION.md`](RELEASE_VALIDATION.md).
