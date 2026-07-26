# Release Validation — Course 1.2.2

Validation date: 2026-07-26
Environment: Windows, Europe/Amsterdam  
Scope: this issued course package and public static reader; the learner's
capstone remains a private, synthetic-data demonstration

This record separates what was actually checked from what the learner must
still prove while taking the course. It is not a certification of future
software, legal compliance, model quality, or fitness for real client data.

## Result

**PASS** for package completeness, deterministic corpus generation, referenced
file integrity, fixture rendering, and the local PWA release gates described
below.

## Structural and machine-readable checks

[`tools/validate_package.py`](tools/validate_package.py) completed all 16 checks
with zero failures and zero warnings before this release record was added. The
final rerun, which also requires this record and the update-report directory,
is captured in [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md).

The checks cover:

- all 12 week files and their repeated nine-part teaching structure;
- JSON, JSONL, YAML, and Draft 2020-12 JSON Schema validity;
- all gold rows against the gold-case schema;
- local Markdown targets;
- case IDs, state names, referenced file sizes, and SHA-256 values;
- the exact duplicate, corrupt-input, and strict synthetic-data invariants;
- every entry in `corpus/checksums.sha256`.

## Frozen corpus and reproducibility

The corpus validator passed:

| Measure | Verified result |
|---|---:|
| Cases / gold records | 20 / 20 |
| Unique source files | 41 |
| Valid PDF files | 36 |
| Deliberately corrupt PDF-like file | 1 |
| DOCX files | 4 |
| Image-only scanned PDFs | 2 |
| Unique evidence-locator entries | 707 |

The generator was run again after the corpus was complete. The checksum
manifest SHA-256 was identical before and after regeneration:

```text
57A3395D1F3903AE59F1BC5E36C84D513C51AF1CD999C117EB1B064CC5F3587F
```

The following adversarial or failure fixtures were also checked directly:

- C009 quotation and terms are byte-identical to C001.
- C010 contains exactly `NOT_A_PDF\nSYNTHETIC_CASE=C010\n`.
- C013's hidden instruction remains text-extractable while not appearing in
  the rendered page.
- Decimal calculations and expected checkpoint states pass the generator
  assertions.

## Render review

All 36 valid PDFs were rendered with Poppler: **39 pages inspected**. The four
DOCX files were exported with installed Microsoft Word 16 and then rasterised
with Poppler because the preferred LibreOffice-based course renderer was not
available in this build environment: **5 pages inspected**.

Review covered every page, including both scans, both multi-page quotations,
the Dutch PDF policy, the English DOCX policy, tables, comma decimals, euro
glyphs, the visible injection fixture, and the byte-identical duplicate.

Observed result: no clipping, overlap, blank output, broken table, or missing
glyph. The intentionally corrupt C010 input was not rendered; explicit safe
failure is its expected behaviour. Regeneration did not change the checksum
manifest, so the reviewed sources are byte-identical to the final sources.

Renderer-independent limitations remain deliberate:

- DOCX locators use logical paths and canonical character spans because
  pagination varies by renderer.
- OCR bounding boxes use the deterministic fixture-image coordinate system.

## PWA validation

The static reader is generated from the Markdown rather than maintaining a
second hand-edited course copy. The production-subpath build contained 50
course/reference pages, including eight numbered foundations and exactly
twelve weekly files.

Observed local results:

- all 15 Node PWA tests passed;
- the course package validator passed all 16 checks with no warnings;
- the manifest, 192/512/maskable icons, Apple touch icon, start URL, scope,
  service worker, and `.nojekyll` artifact were generated;
- desktop, 390-pixel phone, and iPad layouts had no horizontal page overflow
  and visible controls met the 44-pixel touch-target check;
- the mobile drawer opened and closed by keyboard;
- full-course search returned the expected Week 7 human-approval page;
- marking a lesson complete and saving a synthetic local note both survived a
  reload;
- Week 7 displayed the required live-update checkpoint;
- console inspection returned no warnings or errors;
- an already controlled old build detected a new waiting worker, displayed the
  update prompt, retained learner state, accepted the learner's activation
  choice, and reloaded under the new build.

### 1.2.1 visual and interaction audit

The visual-design release was inspected as rendered—not only as source—at
1280×720 desktop, 834×1112 iPad portrait, 390×844 iPhone, and the minimum
supported 320×568 viewport. Both explicit light and dark themes were exercised.

Observed results:

- the redesigned home, workflow preview, progress cards, lesson reader,
  settings, navigation drawer, and bottom navigation rendered without
  horizontal document overflow;
- the 834-pixel iPad entered the focused drawer/bottom-navigation layout rather
  than retaining the compressed permanent desktop sidebar;
- every visible interactive target in the 320-pixel audit was at least 44 by
  44 pixels, including every rendered code-copy control;
- dark-theme quiet buttons computed to light text on the raised dark surface,
  correcting the prior near-invisible secondary-button combination;
- the iPad drawer opened with focus on its labelled close control, trapped
  reverse keyboard focus inside the drawer, and closed by Escape;
- progress exposes `progressbar`, current-value, and value-text semantics;
- lesson metadata uses beginner-facing position labels rather than displaying
  a source filename, while the source remains available as metadata;
- the course route, progress state, update prompt, local notes, and
  service-worker activation behavior remained intact;
- browser diagnostic logs contained no warnings or errors.

The final local rerun completed 15 PWA tests and all 16 course-package checks
with no failures or warnings.

### 1.2.1 iOS safe-area follow-up

A real installed-iPhone screenshot exposed two conditions that ordinary
responsive emulation had not shown clearly: the hidden skip link could remain
partly inside the top status area, and the intentionally floating translucent
tab bar left course content visible in the bottom safe-area gap.

The narrow follow-up fix:

- moves the unfocused skip link above both its own height and the full top safe
  area while retaining the keyboard/VoiceOver focus path;
- docks the mobile tab bar to `bottom: 0`, makes it fully opaque, and includes
  the bottom, left, and right safe-area insets inside the bar;
- removes the exact-320-pixel minimum-width constraint that caused a classic
  scrollbar to create a 15-pixel gap in narrow desktop emulation.

The corrected shell was rendered at 320×568, 390×844, and 834×1112. At each
size the tab bar touched all available layout edges, horizontal overflow was
zero, every visible tab target exceeded 44 pixels, and browser diagnostics
were empty. Both light and dark dock surfaces were inspected. Actual
installed-iPhone appearance remains a device confirmation rather than
something desktop emulation can prove.

### 1.2.2 list-alignment follow-up

The learner's installed-iPhone screenshot showed valid hard-wrapped Markdown
continuations outside the visual indent of their bullet. A bundle-wide source
audit found 87 affected items and 96 detached continuation lines across ten
rendered documents. It also found a nested Week 2 choice list, ordered sections
that intentionally begin above one, and wrapped checklist entries.

The renderer now:

- joins every explicitly indented source continuation to its owning list item;
- preserves unordered and ordered nesting and emits the correct ordered-list
  start;
- gives checklist items a marker-free two-column layout so every wrapped line
  shares one text edge;
- stops safely at fenced code and table blocks, escapes continuation content,
  and renders inline-code link labels correctly.

Fifteen deterministic PWA tests passed. Rendered DOM and layout checks covered
320×568 at 125% text in light mode, 390×844 in dark mode, 430×932 at 125% text
in light mode, and 834×1112. The reported four-item prerequisites section
rendered as one list with four direct items and no detached paragraph; Week 2
rendered nine ordered steps with four choices nested under step 6; checklist
markers computed to `list-style: none`; and every tested viewport had zero
horizontal document overflow. Browser diagnostics were empty. Installed
iPhone verification remains appropriate after the update is accepted.

### First production deployment

The first public deployment was observed on 2026-07-25:

- repository: `freddywinkel/ai-workflow-course`;
- source commit: `1443626d2b98a5391d86cd7e2081f244c5ce3649`;
- GitHub Actions run: `30172859750`;
- production URL:
  `https://freddywinkel.github.io/ai-workflow-course/`;
- installed course version: `1.2.0`;
- deployed build ID: `a20df077def8`.

The GitHub Actions validation, app-test, build, artifact, and deployment jobs
all completed successfully. Fresh no-cache HTTP requests returned status 200
for the app shell, web manifest, service worker, version record, and
612,550-byte course bundle.

The production app was then opened in a real browser. The zero-coding learner
path, all eight foundations, and all twelve weeks were present; browser
diagnostic logs were empty. A lesson completion and a clearly synthetic local
note were saved to establish learner state for the separate old-client update
test. The production layout was also inspected at 390 by 844 pixels and 834 by
1112 pixels with no horizontal overflow.

## Live external-link audit

The original curriculum audit contained 141 distinct external HTTPS page
targets after excluding local demonstration endpoints and the configured API
base URL. PWA/publication sources added in 1.2.0 were checked separately against
the official GitHub, OpenAI, Apple, and web-platform pages recorded in
[`SOURCE_REGISTER.md`](SOURCE_REGISTER.md).

- 138 returned a successful or redirect HTTP status in the automated audit.
- Three blocked the automated user agent with HTTP 403 but opened
  successfully in a live browser on 2026-07-25:
  [OpenAI business-data controls](https://openai.com/business-data/),
  [OpenAI's subprocessor list](https://openai.com/policies/sub-processor-list/),
  and the [PDF Association ISO 32000-2 page](https://pdfa.org/resource/iso-32000-pdf/).
- No external course-reading target returned 404 in the final audit.

Reachability does not prove that a source statement is still current. The
dated claim-level audit is in [`SOURCE_REGISTER.md`](SOURCE_REGISTER.md), and
the learner must run [`EVERGREEN_UPDATE_PROMPT.md`](EVERGREEN_UPDATE_PROMPT.md)
before Week 1 and again at the prescribed checkpoints.

## Not proven by this release audit

This package does not claim that:

- the learner's future environment installs cleanly;
- cloud accounts, regional controls, plans, prices, or node names remain
  unchanged;
- a live model meets the gold thresholds;
- a learner-built approval, isolation, deletion, or fallback path works;
- the capstone is suitable for real data or production use.

Those are weekly gates and Week 12 acceptance evidence, not properties that a
static course package can establish in advance.
