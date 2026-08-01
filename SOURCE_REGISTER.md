# Source Register

Verified through: 2026-07-28
Rule: prefer current primary and official sources. Recheck dated or
vendor-specific statements through `EVERGREEN_UPDATE_PROMPT.md`.

## Dutch SME need and market context

| Topic | Official source | Course use |
|---|---|---|
| AI use by Dutch business size and adoption barriers | [CBS — Bedrijven gebruiken AI vaakst voor marketing of verkoop](https://www.cbs.nl/nl-nl/nieuws/2025/50/bedrijven-gebruiken-ai-vaakst-voor-marketing-of-verkoop) | Target-market rationale; lack of experience, privacy, and legal uncertainty |
| SME productivity and automation response | [CBS — Bedrijven zetten meer in op automatisering door personeelstekort](https://www.cbs.nl/nl-nl/nieuws/2026/23/bedrijven-zetten-meer-in-op-automatisering-door-personeelstekort) | Measure process improvement rather than sell AI novelty |
| SME AI readiness and adoption | [OECD — AI adoption by small and medium-sized enterprises](https://www.oecd.org/en/publications/ai-adoption-by-small-and-medium-sized-enterprises_426399c1-en.html) | Data, skills, leadership, integration, and iterative adoption |

## Dutch and EU privacy, AI, and security

| Topic | Official source | Course boundary |
|---|---|---|
| AVG accountability | [Autoriteit Persoonsgegevens — Verantwoordingsplicht](https://autoriteitpersoonsgegevens.nl/themas/basis-avg/avg-algemeen/verantwoordingsplicht) | Basic accountability questions; no legal conclusion |
| Generative AI conditions under the AVG | [Autoriteit Persoonsgegevens — AVG-randvoorwaarden voor generatieve AI](https://autoriteitpersoonsgegevens.nl/system/files?file=2025-05%2FAVG-Randvoorwaarden+voor+generatieve+AI.pdf) | Data minimisation, roles, risks, and escalation |
| AI Act roles and obligations | [European Commission — Navigating the AI Act](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act) | Provider/deployer literacy and escalation |
| AI literacy | [European Commission — AI literacy questions and answers](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers) | Training appropriate to role, context, and risk |
| Transparency guidance | [European Commission — Article 50 transparency guidelines](https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems) | Current-law panel; recheck before real use |
| Digital resilience basics | [NCSC and DTC — basisprincipes digitale weerbaarheid](https://www.ncsc.nl/nieuws/ncsc-en-dtc-lanceren-gezamenlijke-basisprincipes-voor-digitale-weerbaarheid) | Identify, protect, limit access, prepare, and recover |

Exact legal applicability and dates are intentionally not frozen into the
core lessons. Check current official text and use qualified legal/privacy
review for real work.

## AI risk and evaluation

| Topic | Official source | Course use |
|---|---|---|
| Intended scope, testing, human oversight, monitoring | [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | Evaluation and lifecycle thinking |
| AI workflow safety | [OpenAI — Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices) | Later-course provider-specific safety reference |
| Structured output | [OpenAI — Structured model outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | Later-course bounded-output reference |
| Responses API | [OpenAI — Migrate to the Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses) | Later-course provider pattern; recheck before use |
| Model guidance | [OpenAI — Model guidance](https://developers.openai.com/api/docs/guides/latest-model) | Later-course model selection; recheck before use |
| API data controls | [OpenAI — Your data](https://developers.openai.com/api/docs/guides/your-data) | Later-course provider review; never use real Course 1 data |

The current official OpenAI model guidance identified GPT-5.6 as the current
family on 2026-07-28. Course 1 does not use a live provider. These links are
retained only for a later-course dated audit; model availability, cost, and
behaviour can change. Course 1 requires the offline mock and deterministic
fallback.

## Workflow platforms and commoditisation

| Topic | Official source | Course use |
|---|---|---|
| n8n installation with Node Package Manager (npm) | [n8n documentation](https://docs.n8n.io/deploy/host-n8n/install-options/install-with-npm) | Optional visual-platform crosswalk; not required for Course 1 |
| n8n human fallback and errors | [n8n workflow documentation](https://docs.n8n.io/build/understand-workflows) | Orchestration concepts; verify current nodes in live audit |
| Microsoft agent flows | [Microsoft Copilot Studio — Agent flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview) | Platform crosswalk and build-versus-buy |
| Google Workspace Studio | [Google Workspace — Workspace Studio](https://workspace.google.com/blog/product-announcements/introducing-google-workspace-studio-agents-for-everyday-work) | Platform crosswalk and natural-language workflow creation |

Vendor interfaces are updateable labs. The durable assessment is based on
process, contracts, tests, human control, failures, ownership, and evidence.

## Development tools

| Tool | Official source |
|---|---|
| Python on Windows | [Official Python documentation](https://docs.python.org/3/using/windows.html) |
| Python comma-separated values (CSV) module | [Official Python documentation](https://docs.python.org/3/library/csv.html) |
| Python virtual environments | [Official Python documentation](https://docs.python.org/3/library/venv.html) |
| pytest | [Official pytest documentation](https://docs.pytest.org/) |
| JavaScript Object Notation (JSON) Schema | [Official JSON Schema guide](https://json-schema.org/learn/getting-started-step-by-step) |
| Git | [Official Git documentation](https://git-scm.com/doc) |
| Node.js | [Official Node.js downloads](https://nodejs.org/en/download) |
| Visual Studio Code | [Official Visual Studio Code documentation](https://code.visualstudio.com/docs) |

## Source maintenance rules

`source_claims.json` is the machine-readable claim-level control for every URL
in this register. Each entry records a stable source ID, topic, exact locator,
course use, owner, access date, maximum age, automated or manual availability
check, and review triggers. A URL merely opening is not evidence that the
supported claim remains correct.

Run the deterministic ownership and freshness gate from the course root:

```powershell
python tools\audit_course1_sources.py
```

Maintainers and continuous integration use `--online` to check configured
official pages and save the JSON report. Sources marked `manual-browser` still
require a human to open the named locator and compare the claim. A stale,
unavailable, moved, or materially changed source reopens the affected ledger
item; it must not be silently treated as current.

For every material update:

1. open the official source;
2. record the access date;
3. distinguish facts from course judgment;
4. avoid copying pricing or legal dates into durable lessons unless necessary;
5. update the source register and affected lesson together;
6. rerun package and PWA tests;
7. increment the lesson revision in `curriculum.json` when learner meaning
   changes;
8. preserve the manual fallback when a vendor feature disappears.

## Source exclusions

Do not treat these as authoritative:

- marketing claims without a primary technical or legal source;
- search-result snippets;
- generated summaries without opening the source;
- community examples as proof of production safety;
- model memory about current laws, prices, versions, or product features;
- employer-specific practice as a general Dutch market fact.
