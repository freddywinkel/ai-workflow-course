# Week 8 — AVG and AI Safety Engineering

## Outcome

You will prove the capstone uses fictional data, map how a comparable real workflow would allocate AVG and AI Act roles, screen for DPIA and excluded-use conditions, design rights/retention/deletion across every layer, review vendors and transfers, provide an appropriate transparency notice, and create an AI-literacy record.

The outcome is not a declaration that a product is “GDPR compliant.” It is an engineering record of scope, decisions, evidence, safeguards, uncertainty, and stop conditions.

## Beginner checkpoint

This week introduces legal and governance vocabulary, not a demand that you
become a lawyer. Keep the [glossary](../foundations/GLOSSARY.md) open and write
one plain-language sentence beside every Dutch/EU role or legal term. Separate
law already applicable, adopted future obligations, proposals, consultation
drafts, non-binding guidance, and vendor recommendations.

Do not ask an AI assistant “is this GDPR compliant?” Use it to organise facts
and questions, then verify material claims in the official readings and source
register. The capstone remains synthetic; do not add real personal data for
realism.

Safe AI-assistance request:

```text
Turn my synthetic capstone data-flow notes into a table of systems, data,
purpose, access, retention, and deletion. Mark every legal conclusion as a
question until linked to an official source. Do not declare compliance or
invent controller/processor roles.
```

## Concepts

- fictional, anonymous, pseudonymised, and personal data;
- AVG/GDPR principles and privacy by design/default;
- controller (`verwerkingsverantwoordelijke`), processor (`verwerker`), subprocessor (`subverwerker`), joint controllers, and data subject (`betrokkene`);
- processor agreement and vendor chain;
- international transfer and regional processing;
- DPIA (`gegevensbeschermingseffectbeoordeling`) screening;
- rights, retention, and deletion;
- AI Act provider (`aanbieder`), deployer (`gebruiksverantwoordelijke`), and intended purpose;
- Article 50 transparency;
- meaningful human oversight;
- AI literacy;
- medical-software and health-data stop gate;
- legal-status labels.

Use these labels:

```text
LAW—BINDING/APPLICABLE
LAW—ADOPTED, NOT YET IN FORCE
FINAL GUIDANCE—NON-BINDING
VOLUNTARY CODE
DRAFT/CONSULTATION—DO NOT RELY ON AS SETTLED
NATIONAL ADVICE/PROPOSAL—NOT LAW
OPERATIONAL GUIDANCE—NOT LAW
```

### Dated AI Act position

The source audit was performed on 2026-07-25:

- Regulation (EU) 2026/1744 had been adopted and published, but enters into force on 2026-07-27.
- Its amended Article 4 requires providers and deployers to take measures supporting the development of AI literacy, tailored to relevant knowledge, experience, training, context, and affected persons; it does not prescribe a guaranteed competence level.
- Article 50 transparency rules generally apply from 2026-08-02.
- A limited grace period to 2026-12-02 concerns certain pre-existing systems and the provider-side Article 50(2) marking obligation; it is not a general postponement.
- The amended high-risk application dates are generally 2027-12-02 for Annex III systems and 2028-08-02 for Annex I product systems; verify the exact provision, system category, and transition before relying on either date.
- Dutch supervisory allocation material was advice/proposal or a legislative proposal at verification, not proof of a final enacted designation.
- Commission high-risk classification material under consultation was draft, not binding interpretation.

Run the evergreen audit before relying on this position.

## Official readings

Core:

1. [AVG/GDPR — Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng): Articles 4–6, 9, 12–22, 24–25, 28, 30, 32–36, and 44–49.
2. [EDPB Guidelines 07/2020 on controller and processor concepts](https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-of-controller-and-processor-in-the-gdpr_en).
3. [AP mandatory-DPIA list](https://www.autoriteitpersoonsgegevens.nl/documenten/lijst-verplichte-dpia).
4. [AP privacy rights in practice](https://autoriteitpersoonsgegevens.nl/themas/basis-avg/privacyrechten-avg/voor-organisaties-privacyrechten-in-de-praktijk).
5. [AI Act — Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng): Articles 3, 4, 6, 14, 25, 26, 50, and 113.
6. [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng).
7. [Commission final Article 50 guidelines](https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems).
8. [Commission Article 50 FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act).

Boundary:

9. [MDR — Regulation (EU) 2017/745](https://eur-lex.europa.eu/eli/reg/2017/745/oj/eng).
10. [MDCG 2019-11 rev.1 on software qualification/classification](https://health.ec.europa.eu/latest-updates/update-mdcg-2019-11-rev1-qualification-and-classification-software-regulation-eu-2017745-and-2025-06-17_en).
11. [IGJ: safe digital-care products](https://www.igj.nl/onderwerpen/themas-in-het-toezicht/digitale-zorg/veilige-producten).
12. [AP: health data](https://autoriteitpersoonsgegevens.nl/themas/gezondheid).

Do not read everything linearly. Use the provided worksheet questions, then read the relevant articles/sections. Record primary source, legal status, access date, conclusion, and reassessment trigger.

## Guided build

### 1. Prove the synthetic-data boundary

Inspect every corpus item and generator input. Confirm:

- invented organisations and text;
- no real people, addresses, emails, phones, signatures, logos, tax numbers, IBANs, BSNs, or production identifiers;
- no health, Article 9, criminal-conviction, child, employment, credit, or other consequential-decision data;
- no scraped real terms relabelled synthetic.

Distinctions:

- genuinely fictional information unrelated to an identifiable living person is normally outside AVG material scope;
- anonymous data is outside scope only if identification is not reasonably possible;
- pseudonymised data remains personal data;
- removing names does not make production data anonymous;
- hashes, logs, identifiers, and embeddings may remain personal data if linkable.

If potentially real data appears, quarantine before parsing/model/provider processing and activate the stop procedure.

### 2. Map data flows and roles

For each transition—from intake through provider call, review, draft, backup, and deletion—record:

- data/category;
- purpose;
- system/vendor and location;
- access role;
- retention/deletion;
- AVG role;
- AI Act role;
- legal/status assumption;
- evidence;
- unresolved blocker.

A likely future pattern is client as controller and studio as processor, but roles are functional and activity-specific. A vendor may be a subprocessor for customer content and an independent controller for separate account/security/telemetry purposes.

For this course corpus, lawful basis is `N/A—FICTIONAL DATA`; do not invent Article 6 consent or legitimate interest.

AI Act roles vary by component and version. Branding, placing a system on the market/into service under one’s name, substantial modification, or a changed intended purpose can alter role allocation. “Human in the loop” does not determine classification.

### 3. Complete vendor and transfer review

For OpenAI, Supabase, n8n, the OCR stack, and any Week 11 connector/provider, record:

- contracted purpose and role;
- data types;
- input/output/training use;
- abuse/application/log retention;
- storage, inference, backup, support, and telemetry regions;
- subprocessors and change notice;
- support access;
- security/incident commitment;
- deletion mechanism/evidence;
- export/exit path;
- DPA/Article 28 fields for a hypothetical real deployment.

EU hosting alone does not prove absence of an international transfer. Check inference, support, backups, telemetry, subprocessors, and third-country remote access. For a real-data future:

- Article 45 adequacy;
- Article 46 safeguards such as SCCs plus transfer assessment/supplementary measures;
- Article 49 derogation only exceptionally, not routine cloud architecture.

Unknown relevant facts are production blockers. They do not block this fictional demo.

### 4. Run DPIA and excluded-use screens

Two-stage DPIA screen:

1. Is personal data processed?
2. If yes, is high risk to people’s rights/freedoms likely?

Course conclusion:

> The corpus is intentionally fictional and unrelated to identifiable natural persons. An Article 35 DPIA is therefore not legally triggered for the demonstration. A voluntary risk assessment is completed to make the architecture reusable and identify conditions requiring reassessment.

Screen a hypothetical production version for:

- evaluation/scoring;
- solely automated legal/similarly significant decisions;
- systematic monitoring;
- sensitive/highly personal data;
- large scale;
- matching/combining datasets;
- vulnerable people;
- innovative technology;
- preventing access to rights/services/contracts;
- AP mandatory-list entries.

Document reasoning. Two criteria normally strongly indicate a DPIA, but one can suffice. Unmitigated residual high risk may require considering prior consultation under Article 36.

Also complete:

- AI Act prohibited-practice and high-risk screen;
- consequential-use exclusions;
- medical/health boundary.

Medical stop rule:

> Stop and obtain specialist privacy and medical-device advice if a workflow handles patient records, infers health conditions/risks, supports diagnosis, prediction, prognosis, treatment, prescribing, dosing, or monitoring, or claims an intended medical purpose.

Health information can trigger Article 9 AVG even when software is not a medical device. Human review does not automatically prevent device qualification.

### 5. Map rights, retention, and deletion

For every category:

- source;
- parsed text/table/page images/OCR;
- chunks and embeddings;
- extraction;
- memo;
- approvals/actions;
- logs/traces;
- provider state;
- cache/export;
- backup;
- audit reference.

Record purpose, owner, location, retention trigger, duration, deletion method, exception, and verification.

The audit ledger must not become an undeletable copy of source content. Use opaque IDs and minimal redacted metadata. A hash is not automatically anonymous.

Simulate access, correction, restriction, export, and erasure for an invented identity using a compressed test clock. Label the exercise `SIMULATION_ONLY`; the short interval is not a legal default.

### 6. Assess Article 50 and create transparency

Separate:

- Article 50(1): provider disclosure for direct human interaction with AI unless obvious;
- Article 50(2): provider-side machine-readable marking for covered synthetic outputs;
- Article 50(4): deployer disclosure for deepfakes and certain AI-generated/manipulated public-interest text.

The internal supplier review memo is ordinarily not public-interest publication or direct conversational interaction. Record the facts and assumptions; do not state that Article 50 can never apply.

The Commission guidance describes substantive knowledgeable review and editorial control for the relevant public-interest-text exception; superficial review is insufficient.

Voluntarily mark every capstone memo:

```text
AI-assisted draft — human approval required
```

Machine record:

```json
{
  "ai_generated": true,
  "model_id": "...",
  "prompt_sha256": "...",
  "schema_sha256": "...",
  "system_version": "...",
  "approval_status": "pending"
}
```

These support provenance; they do not prove compliance with provider-side machine-readable marking requirements.

### 7. Demonstrate meaningful approval and AI literacy

Keep separate:

- AVG Article 22;
- AI Act Articles 14/26 for high-risk systems;
- Article 50(4) human-review/editorial-control condition.

Apply strong controls voluntarily:

- reviewer sees evidence, uncertainty, conflicts, intended action;
- has competence, time, and authority;
- can approve, edit, reject, stop, or escalate;
- no preselected approval;
- exact output hash;
- edit invalidates approval;
- timeout means no action;
- comments/reasons captured;
- override/approval patterns monitored for automation bias.

Create an AI-literacy record:

- audience/role and baseline knowledge;
- system/intended purpose;
- permitted/prohibited uses;
- limits/failure modes;
- evidence-verification procedure;
- approval authority;
- privacy/security rules;
- incident escalation;
- short assessment result;
- material/trainer version and date;
- refresh trigger.

After 2026-07-27, use the amended Article 4 wording. Annotate older AP guidance that predates it.

## Capstone increment

Add:

```text
governance/
  BOUNDARY_AND_INTENDED_PURPOSE.md
  DATA_FLOW_ROLE_MAP.csv
  DPIA_SCREEN.md
  AI_ACT_ASSESSMENT.md
  MEDICAL_AND_EXCLUDED_USE_GATE.md
  VENDOR_TRANSFER_REGISTER.csv
  RETENTION_RIGHTS_MAP.csv
  TRANSPARENCY_NOTICE.md
  AI_LITERACY_RECORD.md
tests/evidence/
  week08_deletion_drill.json
  week08_approval_paths.json
```

## Required artifact

`artifacts/weekly/week-08/WEEK08_GOVERNANCE_EVIDENCE_PACK/` containing the completed records, source/status snapshot, decisions, rights/deletion simulation, approval results, and unresolved blockers.

## Test gate

Pass only if:

- every corpus item is demonstrably fictional;
- no prohibited/sensitive/production data is present;
- each processing step has owner, purpose, location, role assessment, retention, and deletion;
- unknown vendor/transfer facts are visible real-data blockers;
- DPIA and AI Act screens have reasoned, status-labelled conclusions;
- the memo never recommends/selects a supplier;
- exact-output approval, edit invalidation, reject, and timeout work;
- rights/deletion simulation covers originals, derivatives, indexes, logs, caches, provider state under your control, and audit references;
- Article 50 assessment is context-specific and dated;
- AI-literacy record is role-specific and assessed;
- external action remains draft-only;
- health-data or medical-purpose input triggers a stop.

## Common failures

- **Pseudonymised production data called synthetic:** it remains personal data.
- **Consent selected automatically:** lawful basis depends on actual purpose/context.
- **EU hosting treated as no transfer:** inventory all processing/access paths.
- **Every vendor called a processor:** assess each activity and separate purposes.
- **Consultation draft called law:** attach one of the explicit status labels.
- **Approval button assumed to remove Article 22/high-risk concerns:** examine actual effect, role, purpose, and oversight.
- **Provenance metadata called Article 50 compliance:** marking obligations are distinct.
- **Raw content retained in immutable audit:** minimise and separate.
- **Older Article 4 wording copied without amendment check:** rerun the dated source audit.
- **Administrative healthcare use automatically called a device—or clinician review called an exemption:** apply both health-data and intended-medical-purpose tests.

## Estimated time

| Activity | Time |
|---|---:|
| Selected official reading and status notes | 2.25 h |
| Boundary, data flow, and role map | 1.25 h |
| Vendor/transfer register | 1.25 h |
| DPIA/AI Act/medical screens | 1.25 h |
| Rights/retention simulation | 1.25 h |
| Transparency, approval, literacy | 1.0 h |
| Evidence review | 0.5 h |
| **Total** | **8.75 h** |
