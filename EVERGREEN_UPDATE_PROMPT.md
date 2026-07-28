# Evergreen Course Audit Prompt — Maintainers Only

## Purpose

This is a release-maintenance prompt for a person responsible for the course.
It may authorize course edits, so it is not a learner setup step. Learners use
the read-only current-software report in
[BEGINNER_SOFTWARE_CHECK.md](BEGINNER_SOFTWARE_CHECK.md) instead.

Use this prompt with a web-enabled research and coding agent when preparing a
course release.

The audit verifies current facts. It must not rewrite durable lessons merely
because a vendor changed wording or navigation.

## Copy-paste prompt

```text
You are auditing Course 1 — Controlled AI Workflow Foundations for Dutch SMEs.

Course root:
AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE

Current course version:
Read it from README.md and curriculum.json.

Audit date and timezone:
Use today's date in Europe/Amsterdam.

Goal:
Determine whether the course remains safe, current, internally consistent, and
appropriate for a literal beginner building a synthetic low-risk workflow.

Authority rules:
1. Use primary and official sources.
2. For OpenAI application programming interface (API) facts, use official
   OpenAI developer documentation.
3. For Dutch privacy, use Autoriteit Persoonsgegevens and official law/guidance.
4. For the EU AI Act, use European Commission or EUR-Lex material.
5. For cyber guidance, prefer NCSC/DTC and other official sources.
6. For software, use official documentation, release notes, and compatibility
   pages.
7. Search snippets and model memory are not evidence.
8. Clearly separate verified fact, course judgment, inference, and unresolved
   question.

Audit these areas:

A. Curriculum integrity
- curriculum.json parses and has one current course;
- exactly 9 foundation and 9 module progress lessons exist;
- every configured source exists once;
- stable IDs and revision dates are unique and valid;
- future career courses do not count toward progress;
- all internal Markdown links resolve outside ignored archives;
- all required module headings are present and ordered;
- the capstone, dataset, schemas, templates, and assessment agree.

B. Dutch SME relevance
- refresh current Statistics Netherlands (*Centraal Bureau voor de Statistiek*,
  CBS) evidence about small and medium-sized enterprise (SME) artificial
  intelligence (AI) adoption, barriers, and automation;
- check whether Course 1 still targets a meaningful low-risk administrative
  implementation gap;
- identify native-platform advances that commoditize simple workflow building;
- confirm the curriculum emphasizes process, data, evaluation, adoption, and
  ownership rather than tool clicks.

C. General Data Protection Regulation (GDPR/AVG) and AI Act literacy
- verify current Dutch Data Protection Authority (*Autoriteit
  Persoonsgegevens*, AP) guidance linked in SOURCE_REGISTER.md;
- verify current Commission guidance on provider/deployer roles, AI literacy,
  risk categories, and transparency;
- identify any new obligation or effective date that changes Course 1;
- keep exact legal classification out of the learner's competence;
- confirm real data and consequential decisions remain excluded.

D. Security baseline
- verify current National Cyber Security Centre (NCSC) and Digital Trust Center
  (DTC) baseline guidance;
- confirm secrets, access, logging, backup, incident,
  `EXTERNAL_ACTIONS_ENABLED=false`, and fallback concepts remain appropriate;
- flag any unsafe command or default.

E. Learning stack
- verify a supported Python >=3.12 path for Windows;
- verify the exact required offline pytest pin and complete clean-install
  freeze;
- keep OpenAI, Node.js, and n8n outside the required Course 1 installation;
- if an optional n8n crosswalk is retained, verify and record a compatible
  Node.js Long-Term Support release and exact n8n version;
- do not add Docker, FastAPI, Supabase, optical character recognition (OCR),
  retrieval-augmented generation (RAG), or production infrastructure back to
  Course 1 without a curriculum-level reason.

F. Optional AI lab
- resolve current recommended OpenAI model guidance;
- verify the current Responses API and JSON Schema structured-output pattern;
- keep model ID configurable;
- verify refusal and error handling;
- verify provider data-control documentation;
- do not require a flagship model or live API key to pass;
- confirm the offline fixture remains the required path.

G. Synthetic data and rules
- parse practice_data/work_items.csv;
- confirm 15 rows and 12 columns;
- parse practice_data/expected_issues.csv;
- confirm 13 unique expected issue keys;
- independently implement or inspect R001-R011 using 2026-07-26 as the fixed
  assessment date;
- confirm exact agreement;
- confirm no real organization or personal data appears.

H. Progressive web app (PWA)
- run the metadata-driven build and tests;
- verify curriculum-only changes alter content hash/build ID;
- verify manifest ID, scope, start URL, base path, and cache prefix remain
  stable;
- test Overview, Course, Career, Search, and Settings;
- test state-v1 migration and backup import;
- test 320, 390, 430, and 834 px viewport widths;
- test light/dark/system, 125% text, keyboard focus, reduced motion, safe areas,
  offline reading, back/forward, and no horizontal overflow;
- rehearse an old installed-client update.

I. Claims and tone
- Course 1 must not claim consultant, legal, compliance, production, clinical,
  security, or regulated-platform competence;
- synthetic timing must not be presented as forecast savings;
- `ACCEPT FOR SYNTHETIC PORTFOLIO`, `REWORK`, and `DO NOT CONTINUE` must all
  remain valid evidence-based Course 1 pass outcomes;
- archived supplier material must remain clearly assigned to a later course;
- every lesson should include a consultant lens and stop/rework behavior.

Required execution:
1. Read the complete relevant files.
2. Run deterministic validators and PWA tests.
3. Open official sources and record exact supporting URLs.
4. Make the narrowest coherent updates necessary.
5. Increment material lesson revisions and course version appropriately.
6. Do not edit generated app/dist files.
7. Build and visually test the PWA after changes.

Output:
- AUDIT RESULT: PASS, PASS WITH NON-BLOCKING NOTES, or UNVERIFIED;
- date and timezone;
- changed files;
- verified sources;
- current tool selections and why;
- legal/guidance changes;
- validation/test results;
- visual/PWA results;
- unresolved blockers;
- explicit recommendation whether a learner may continue.

Return UNVERIFIED when a required official source or test cannot be checked.
Do not convert unavailable evidence into a confident assumption.
```

## How to use the result

- `PASS`: save the report under `updates/` and continue.
- `PASS WITH NON-BLOCKING NOTES`: save it, understand the notes, and continue
  only if none affects the current module.
- `UNVERIFIED`: stop at the relevant module until the missing evidence or test
  is resolved.

An audit is dated evidence, not a permanent certification.
