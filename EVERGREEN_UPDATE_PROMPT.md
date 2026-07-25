# Evergreen Live-Audit and Course-Update Prompt

Run this prompt:

- immediately before Week 1;
- immediately before Week 7;
- every 8–12 weeks thereafter;
- sooner after a deprecation, security advisory, legal change, provider incident, pricing/data-control change, or dependency upgrade.

Copy everything inside the prompt block into a web-enabled research/coding agent. Point it at the course folder and allow file edits only if you want it to apply verified updates.

---

## Copy-paste prompt

```text
You are the maintainer and independent auditor of the standalone
AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE course package.

COURSE DIRECTORY
- Locate the supplied AI_WORKFLOW_DOCUMENT_SYSTEMS_COURSE directory.
- Read README.md, COURSE_OVERVIEW.md, SOFTWARE_MATRIX.md,
  SETUP_WINDOWS.md, stack-manifest.yaml, requirements-course.txt,
  ARCHITECTURE_AND_CONTRACTS.md, CAPSTONE_SPECIFICATION.md,
  ASSESSMENT_AND_RUBRIC.md, every weeks/WEEK_*.md,
  SOURCE_REGISTER.md, COURSE_CHANGELOG.md, schemas/, templates/,
  corpus/README.md, corpus/manifest.jsonl, corpus/golden.jsonl, and tools/.
- Preserve the existing issued course. Use Git history when available and
  never erase the old statement without recording it in the change report.

NON-NEGOTIABLE VERIFICATION RULE
- You MUST have live web browsing/network access and must open current primary
  sources. A search-result snippet, cached model memory, another course, blog,
  reseller page, or AI answer is not verification.
- First make a small live request to:
  1. an official vendor documentation/release page; and
  2. EUR-Lex or an official EU/Dutch authority page.
- If either primary-source category cannot be browsed sufficiently to verify
  the affected claims, output exactly the single line:

  UNVERIFIED

  Then stop immediately. Do not add an explanation and do not update files,
  versions, dates, prices, legal status, or the changelog.

SCOPE AND PRESERVATION
- Audit technical/course accuracy only. Do not add sales, pricing of studio
  services, positioning, client acquisition, or business operations.
- Preserve: synthetic-data-only training; no health/special-category/BSN/
  children/real production data; no consequential natural-person decisions;
  no supplier ranking/recommendation; human review; exact-output-hash approval;
  immutable sources and provenance; named safe states; deterministic
  validation; manual fallback; draft-only actions; tenant isolation; and the
  vendor-neutral frozen gold dataset.
- Do not replace the canonical stack merely because a newer fashionable tool
  exists. Recommend a stack change only when current support, safety,
  reproducibility, cost/quality evidence, or a deprecation makes it justified.
- Do not turn comparison tracks into parallel mandatory tracks.
- Do not weaken thresholds to make current results pass.
- Legal material is practical engineering guidance, not legal advice.

PRIMARY-SOURCE ORDER
1. Binding law and official legal publication:
   - EUR-Lex.
2. Official public authorities:
   - European Commission / AI Office;
   - EDPB;
   - Autoriteit Persoonsgegevens (AP);
   - Dutch government and enacted Dutch legislation;
   - NCSC-NL;
   - IGJ and European Commission medical-device/MDCG pages.
3. Official vendor documentation, status/security pages, release notes,
   pricing pages, DPAs/data-control documentation, subprocessor lists, and
   official repositories.
4. Official package indexes only to resolve distribution versions.

Never use secondary commentary to establish a legal date, product capability,
retention term, region, price, version, license, deprecation, or security fix.
You may use it only to discover a primary source.

AUDIT DATE AND COMPARISON BASELINE
- State current date, time zone, course version, source-register version, Git
  commit (if available), corpus manifest hash, and gold-file hash.
- Compare every finding with the exact old course statement and its file/week.
- Treat all model aliases, API/SDK syntax, prices, plans, regional controls,
  retention, node/connector names, managed-service behaviour, package
  versions, and licenses as volatile.

TECHNICAL AUDIT — VERIFY ALL
Open current official pages and verify:

A. OpenAI
- recommended API for new projects;
- Responses API request/response syntax and current Python SDK pattern;
- Structured Outputs/Pydantic syntax, strict-schema limits, refusal,
  incomplete/truncation, tool output, and `store` behaviour;
- model catalog, exact model IDs/snapshots, capability support, context/output
  limits, reasoning settings, and availability;
- current pricing, cached/batch/regional uplifts, units, and effective dates;
- training use, abuse-monitoring retention, application-state retention,
  Zero Data Retention/Modified Abuse Monitoring eligibility, files/vector
  stores/tools, and European regional storage/processing conditions;
- deprecations and migrations, specifically Assistants, hosted Evals,
  reusable prompts, selected models, SDK methods, and endpoints;
- current OpenAI Python SDK release and migration notes.

B. Required stack
- n8n stable and prerelease versions, Docker image/tag guidance, supported
  Node versions if relevant, current node names/paths, Wait/error/approval
  behaviour, execution retention/deletion, external binary storage,
  source-control/enterprise boundaries, security advisories, security audit,
  license, and breaking changes;
- CPython stable/maintained versions and Windows install-manager commands;
- FastAPI, Pydantic, pytest, OpenAI SDK, Docling, psycopg, Supabase client,
  HTTPX, jsonschema, and other direct dependency versions, Python support,
  licenses, advisories, and breaking changes;
- Docling PDF/DOCX/table/OCR support, provenance objects, supported OCR
  engines, model downloads/licenses, Windows installation, and latest
  GitHub-versus-PyPI release;
- PostgreSQL/Supabase versions or platform support, project regions, private
  buckets, RLS/views/service keys, signed URLs, database and Storage backup
  coverage, pgvector, retention/deletion, pricing/plan limits, subprocessors,
  and security advisories;
- Git and Docker Desktop instructions/license implications for this private
  course.

C. Optional/comparison stack
- Power Automate and current Microsoft connector/approval names, permissions,
  Dataverse/licensing/region behaviour;
- Google Drive/Gmail OAuth scopes and connector names;
- Make error/retry/incomplete-execution and region/plan behaviour;
- Mistral OCR model/API names, page/locator output, pricing, EU endpoint,
  training/retention/ZDR and plan limits;
- Azure Document Intelligence API/model version, layout/locator support,
  region, limits, price, temporary retention/deletion, and privacy terms;
- Ollama API, local authentication/network default, Structured Outputs,
  Responses/OpenAI-compatibility limits, current model tag/digest/license and
  hardware/context requirements;
- Promptfoo and Langfuse versions, licenses, remote-data/execution risks,
  retention/redaction and self-hosting caveats.

D. Security
- current NCSC-NL baseline and incident guidance;
- OWASP LLM/prompt-injection and file-upload guidance;
- relevant CVEs/security advisories for required direct components and images;
- whether course controls/tests need amendment.

LEGAL AND REGULATORY AUDIT — VERIFY ALL
- Open the consolidated GDPR/AVG and check relevant amendments/status.
- Check EDPB controller/processor, DPIA, transfer, breach, anonymisation, and
  AI-related materials; label drafts/consultations explicitly.
- Check AP mandatory-DPIA list, rights/breach/AI-literacy/meaningful-human-
  intervention material and exact status.
- Open Regulation (EU) 2024/1689 and Regulation (EU) 2026/1744 at EUR-Lex.
  Verify enactment, entry into force, current applicability dates, amended
  Article 4 wording, Article 50 timing/transitions, and high-risk dates.
- Check Commission/AI Office final Article 50 guidance/FAQ/code and any later
  corrigenda, implementing acts, standards, final high-risk guidelines, or
  changes. Do not treat a draft as final.
- Check the actual status of Dutch AI Act supervisory/designating legislation,
  AP/RDI advice, consultation material, regulator/sandbox arrangements, and
  enacted authority allocation. Do not infer law from a press release.
- Check the medical boundary using MDR, current MDCG software guidance,
  AI Act/MDR interplay guidance, AP health-data guidance, and IGJ guidance.

For every legal item classify it exactly as one of:
- LAW—BINDING/APPLICABLE
- LAW—ADOPTED, NOT YET IN FORCE
- FINAL GUIDANCE—NON-BINDING
- VOLUNTARY CODE
- DRAFT/CONSULTATION—DO NOT RELY ON AS SETTLED
- NATIONAL ADVICE/PROPOSAL—NOT LAW
- OPERATIONAL GUIDANCE—NOT LAW

Distinguish:
- publication;
- adoption;
- entry into force;
- application;
- transition/grace period;
- proposal/consultation;
- non-binding interpretation.

COURSE-INTERNAL AUDIT
- Validate all Markdown links and anchors.
- Parse JSON, JSONL, YAML, and JSON Schemas.
- Validate the schemas under JSON Schema Draft 2020-12.
- Verify exactly 12 weekly files and the repeated headings:
  Outcome, Concepts, Official readings, Guided build, Capstone increment,
  Required artifact, Test gate, Common failures, Estimated time.
- Verify exactly 20 unique corpus cases, manifest/gold agreement, file hashes,
  C009 byte identity, C010 exact corrupt bytes, scan image-only status, no real
  personal/sensitive data, and all promised case categories.
- Re-run the corpus generator in a clean temporary directory and compare
  deterministic hashes, or classify non-determinism as a defect.
- Render every valid PDF and DOCX and visually inspect every page for clipping,
  overlap, missing glyphs, hidden-content test integrity, scan readability,
  the synthetic banner, and no unintended real data.
- Run package validation and any course/corpus tests.
- Ensure every acceptance requirement is taught, templated, represented in the
  corpus where applicable, and mapped to an executable/testable gate.
- Ensure current Windows instructions remain valid and distinguish observed
  machine state from general prerequisites.

FINDING CLASSIFICATION
Classify every comparison:
- BREAKING: current course cannot run, uses a removed/insecure API, misstates
  applicable law, or violates a preserved safety invariant.
- REQUIRED: must change before the affected week or release.
- RECOMMENDED: meaningful improvement with migration/test plan.
- WATCHLIST: not currently applicable/final, but has a date or trigger.
- NO CHANGE: checked and still accurate.

FIRST OUTPUT — DATED CHANGE REPORT BEFORE EDITS
Create updates/YYYY-MM-DD_CHANGE_REPORT.md before changing the course. Include:

1. Audit identity and verification proof.
2. Executive result: VERIFIED-CURRENT / VERIFIED-CHANGES-REQUIRED.
3. A table for every finding:
   - classification;
   - category;
   - exact affected file and week;
   - old statement (short exact excerpt);
   - verified replacement;
   - publication/effective/applicability date;
   - legal/status label where relevant;
   - primary source URL and access date;
   - why it matters;
   - migration/edit steps;
   - affected labs/artifacts;
   - exact tests to rerun.
4. A NO CHANGE table listing the high-volatility claims actually checked.
5. Security advisories/CVEs and applicability.
6. Unresolved contradictions or unavailable facts.
7. Proposed next review date and event-based triggers.

If two official sources conflict (for example GitHub release versus PyPI),
record both, do not invent a resolution, choose a safe installable pin only
after a clean test, and leave an explicit unresolved/watch item.

APPLY VERIFIED CHANGES
Only after the dated report exists:
- update the minimum necessary course files;
- update SOURCE_REGISTER.md with `last_verified`, exact source, applicability,
  status, and volatility;
- update stack-manifest.yaml, requirements-course.txt, SOFTWARE_MATRIX.md, and
  Windows commands when verified;
- update affected readings, labs, failure handling, templates, schemas,
  capstone or tests;
- preserve configurable model/provider IDs;
- regenerate the corpus only if a course contract or fixture defect requires
  it; never alter gold answers merely to improve a score;
- append a dated entry to COURSE_CHANGELOG.md linking the change report;
- increment the course version according to:
  patch = source/link/wording/test clarification;
  minor = compatible lab/tool/legal-control addition;
  major = contract, state, corpus, acceptance, or incompatible stack change.

VALIDATION AFTER EDITS
- Re-run every affected unit, parser, schema, corpus, security, regression, and
  acceptance test identified in the report.
- Re-render and inspect all affected documents.
- Run the package-wide validator.
- Do not mark a test passed when it was not run. Use NOT RUN with reason.
- If a required change cannot be implemented safely, leave it as an explicit
  release blocker; do not weaken a gate.

FINAL RESPONSE AND FILE
Create updates/YYYY-MM-DD_FINAL_UPDATE_SUMMARY.md and report:

1. Updated course version and audit date.
2. Updated stack manifest: exact selected versions/models/endpoints/settings.
3. Applied BREAKING/REQUIRED/RECOMMENDED changes.
4. WATCHLIST and unresolved risks.
5. Files/labs/templates/corpus affected.
6. Test and render results, including failures or NOT RUN.
7. Whether the course is safe to start:
   - VERIFIED — START WEEK 1
   - VERIFIED — START THROUGH WEEK [N] ONLY
   - DO NOT START — RELEASE BLOCKER
8. Next review date and event triggers.
9. Direct links to the dated change report, final summary, source register,
   changelog, and revised course entry point.

Do not output “up to date” without the checked NO CHANGE table and live primary
sources. Do not use UNVERIFIED for ordinary unresolved details when browsing
worked; use it only for the primary-source browsing failure defined above.
```

---

## Expected files after a successful run

```text
updates/
  YYYY-MM-DD_CHANGE_REPORT.md
  YYYY-MM-DD_FINAL_UPDATE_SUMMARY.md
```

The agent should also update:

- `SOURCE_REGISTER.md`;
- `stack-manifest.yaml`;
- `requirements-course.txt`;
- affected weeks/templates/schemas/corpus;
- `COURSE_CHANGELOG.md`.

Review the dated report before relying on any automated course edit, particularly legal status, vendor data controls, dependency pins, and gold-answer changes.
