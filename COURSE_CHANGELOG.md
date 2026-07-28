# Course Changelog

## 2.2.0 — 2026-07-28

### One reproducible learner project

- Kept foundation rehearsals in `controlled-ai-course-practice`, then moved
  every module increment into the one Git repository created during Windows
  Setup: `AI-workflow-learning\operations-exception-assistant`.
- Added a consistent `evidence\module-01` through `evidence\module-09`
  structure, a pass-only Git checkpoint after every module, and a final
  `CAPSTONE_INDEX.md` plus project `CHANGELOG.md`.
- Connected every required capstone artifact to the module that teaches and
  produces it, including the previously unused stakeholder, baseline,
  opportunity, and data-quality worksheets.

### Honest Course 1 decision boundary

- Replaced conflicting pilot language with exactly three evidence-backed
  Course 1 outcomes: `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, and
  `DO NOT CONTINUE`.
- Made all three outcomes completable in Module 9. None authorizes a client
  pilot: discovery belongs in Course 2 and supervised low-risk pilot delivery
  belongs in Course 3.
- Standardised the external-action safety setting as
  `EXTERNAL_ACTIONS_ENABLED=false`.
- Replaced ambiguous kill-switch and Course 1 pilot-phase wording with
  explicit safe-stop, synthetic-portfolio, and later-course boundaries.

### Beginner setup and durable dependencies

- Separated the learner's read-only software check from the maintainer-only
  course update prompt.
- Made the core Course 1 path local and rule-first; the OpenAI package and n8n
  are optional labs rather than required setup.
- Pinned the small required Python package set, taught the learner to record
  the installed environment, and pinned release validation and GitHub Actions
  dependencies.
- Added the missing Python list and membership demonstration before the
  learner recreates it independently.

### Progressive web app product fixes

- Prevented private notes from being lost during immediate navigation and
  report storage failures truthfully.
- Made Resume choose the next incomplete actionable lesson.
- Added an actionable learning sequence so Resume and previous/next insert the
  read-only software check and Windows Setup between Foundations 2 and 3,
  without counting those setup gates as core progress.
- Added secure CommonMark web links, an accessible note label and lesson
  statuses, heading focus after navigation, clearer install guidance, and
  reading-time wording that does not understate practice time.
- Reset each newly rendered page to the top after button, browser-history, or
  copied-link navigation.
- Included the build generator in update identity so manifest or icon build
  changes reach existing installed clients.
- Added regression checks for the unified repository, artifact coverage,
  decision vocabulary, maintainer boundary, links, learner state,
  accessibility, and update identity.

## 2.1.0 — 2026-07-26

### Certified-beginner practice

- Rebuilt every foundation and module exercise around a four-part
  **follow → recreate → ask Codex to check → pass** method.
- Added exact Windows clicks, commands, expected results, and bounded
  troubleshooting before independent work.
- Added a meaningfully different recreation task so copying the demonstration
  is not treated as understanding.
- Added copy-and-paste prompts for read-only Codex inspection of one explicitly
  named practice folder.
- Added objective pass criteria and kept corrections in the learner's hands.
- Rewrote the Windows setup and readiness rehearsal for a learner with no
  assumed computer or coding knowledge.
- Added a first-use terminology rule: abbreviations are written in full before
  their short form, and unfamiliar product names such as Git are defined before
  use.
- Increased the beginner planning range to 140–180 hours to include the worked
  example, independent recreation, and correction loop.

## 2.0.0 — 2026-07-26

### Career outcome

- Changed the end goal from a supplier-document system builder to a first
  foundation for becoming a **Controlled AI Workflow Implementation Consultant
  for Dutch SMEs**.
- Added an honest Course 1 capability boundary.
- Added a separate career sequence covering diagnostics, integrations,
  controlled document AI, production governance, adoption, and optional
  quality/eQMS specialization.

### Curriculum

- Preserved and expanded the absolute-beginner foundation.
- Added spreadsheets, CSV, and SME data quality as a dedicated foundation.
- Reframed AI as a bounded workflow component rather than the system authority.
- Replaced “safe vibe coding” with professional safe AI-assisted building.
- Simplified workflow-tool and data-store learning; moved Docker, FastAPI,
  Supabase, OCR, RAG, and multi-tenancy to later courses.
- Replaced 12 calendar weeks with nine gate-based consultant modules.
- Added a consultant lens, stop/rework behavior, and client-style artifact to
  every module.

### Capstone

- Replaced the advanced supplier-document capstone with a Synthetic SME
  Operations Exception Assistant using 15 fictional work items.
- Added a frozen 13-issue expected register and rules R001–R011.
- Made the deterministic exception report useful without AI.
- Made the live model lab optional and kept model ID in configuration.
- Added meaningful review, exact-revision approval, local draft outbox, kill
  switch, fallback, evaluation, UAT, adoption, and handover.
- Made `PILOT`, `REWORK`, and `DO NOT PILOT` equally valid evidence-based
  outcomes.

### Preserved advanced material

- Moved the former 12 weeks, 20-case supplier corpus, supplier schemas, and
  generation tools into
  `future_courses/course_04_controlled_document_ai/source_material/`.
- Excluded archived source material from Course 1 progress and validation.

### PWA architecture

- Added canonical `curriculum.json`.
- Added stable lesson IDs and revisions.
- Made course grouping, progress, reading order, checkpoints, and career path
  metadata-driven.
- Added a separate Career tab.
- Added state-v1 migration and old-backup support.
- Included curriculum metadata in the content and service-worker build hash.
- Preserved manifest identity, base path, cache prefix, offline bundle, and
  learner-controlled updates.

### Validation

- Replaced fixed 8-foundation/12-week/supplier-corpus assertions with
  metadata-driven Course 1 checks.
- Added practice-data and schema checks.
- Expanded PWA tests for career separation, stable IDs, migration, mobile
  navigation, and offline/update behavior.

## 1.2.x and earlier

The earlier course built a controlled synthetic supplier quotation and terms
review system. Its engineering material remains preserved as future Course 4
source material. See the archived legacy documents for the detailed 1.x
history and design.
