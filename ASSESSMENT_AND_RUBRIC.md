# Assessment and Rubric

## Assessment principle

Course 1 assesses controlled implementation judgment, not how much technology
you used.

The following can all be excellent outcomes:

- a rule-only workflow because AI added no value;
- a bounded AI summary with strong verification;
- a `REWORK` decision because data quality is poor;
- a `DO NOT PILOT` decision because existing software is better.

## Pass prerequisites

All prerequisites must pass before scoring:

- only synthetic data was used;
- no secrets are stored in code, screenshots, notes, or Git;
- the deterministic report works with AI disabled;
- every run ends in a named state;
- expected exceptions are tested;
- unsupported AI claims cannot pass silently;
- no external send, payment, deletion, or record update exists;
- editing invalidates approval;
- manual fallback is demonstrated;
- limitations and assumptions are explicit;
- the learner can explain the system without relying on generated wording.

Any failure is a stop/rework condition.

## Weighted rubric

| Area | Weight |
|---|---:|
| Process discovery and opportunity selection | 20% |
| Data quality and deterministic controls | 20% |
| Bounded AI and evidence | 15% |
| Human control and failure behaviour | 15% |
| Dutch SME risk and tool-fit screen | 15% |
| Evaluation, adoption, and handover | 15% |

Minimum passing score: 75%, with every area at least “competent”.

## Performance levels

### 4 — Strong

Evidence is reproducible, assumptions are separated from observations, failure
behaviour is tested, decisions follow the evidence, and another person can
operate the demonstration.

### 3 — Competent

The required artifacts exist, important claims are supported, controls work,
and limitations are clear. Minor gaps do not undermine the boundary.

### 2 — Rework

The main idea is visible but evidence, tests, ownership, usability, or risk
screening is incomplete.

### 1 — Unsafe or unsupported

The learner relies on AI output, guesses data meaning, hides failures, skips
human authority, or makes production/compliance claims without evidence.

## Area 1 — Process discovery and opportunity selection

Strong evidence includes:

- a clear process trigger, input, output, owner, users, systems, handoffs, and
  fallback;
- two manual walkthroughs;
- an honest baseline with assumption labels;
- an opportunity score that considers frequency, value, reversibility,
  existing-tool fit, data readiness, and failure consequence;
- intended purpose and exclusions;
- explicit allocation to rule, AI, or human;
- a justified go, rework, or stop decision.

Automatic rework:

- beginning with a tool instead of a process;
- invented ROI;
- no process owner;
- no build-versus-buy check.

## Area 2 — Data quality and deterministic controls

Strong evidence includes:

- source inventory and data dictionary;
- stable IDs and named authoritative fields;
- explicit missing, duplicate, type, date, and allowed-value rules;
- reproducible issue IDs;
- correct handling of the supplied expected issues;
- separation between source, derived issues, and output;
- fixed evaluation-date assumptions.

Automatic rework:

- silently filling missing values;
- changing expected results to match faulty code;
- AI determining objective data-quality rules.

## Area 3 — Bounded AI and evidence

Strong evidence includes:

- AI is optional and replaceable;
- structured output;
- prompt and schema versions;
- verified issue records are the only factual input;
- issue references are checked after generation;
- refusal, timeout, malformed output, and unsupported claims are tested;
- a rule-based fallback remains usable.

Automatic rework:

- AI creates authoritative exceptions;
- raw untrusted instructions control the prompt;
- schema validity is treated as truth;
- no offline test path.

## Area 4 — Human control and failure behaviour

Strong evidence includes:

- usable approve, edit, reject, and expire paths;
- reviewer authority and responsibility are stated;
- deterministic and AI content are distinguishable;
- approval is bound to the exact revision;
- edit invalidates approval;
- kill switch and manual fallback work;
- retry and duplicate effects are controlled;
- failures are visible.

Automatic failure:

- external action without exact review;
- ceremonial approval where the reviewer lacks evidence or authority;
- silent failure shown as success.

## Area 5 — Dutch SME risk and tool-fit screen

Strong evidence includes:

- personal/special-category data screen;
- purpose, minimisation, retention, access, vendor, transfer, logging, backup,
  and deletion questions;
- basic provider/deployer and AI-use risk triage;
- specialist escalation points;
- review of existing Microsoft, Google, ERP, CRM, DMS, or other native
  capabilities;
- ownership and recurring-cost record;
- no claim of legal compliance.

Automatic rework:

- real sensitive data in the demonstration;
- regulated or consequential decisions;
- custom build proposed without checking existing capabilities.

## Area 6 — Evaluation, adoption, and handover

Strong evidence includes:

- normal, edge, adversarial, and operational failure cases;
- false-positive, false-negative, supported-claim, time, cost, and usability
  results;
- limitations and unresolved risks;
- UAT with another person using synthetic data;
- user instructions and role-specific AI literacy;
- runbook, fallback, support owner, and change record;
- portfolio story that separates facts from assumptions;
- evidence-backed `PILOT`, `REWORK`, or `DO NOT PILOT`.

Automatic rework:

- claiming savings from one synthetic timing run;
- demo succeeds only when the builder operates it;
- no owner after handover.

## Oral demonstration questions

The learner must answer in plain language:

1. What business problem are you solving?
2. What evidence says it is worth solving?
3. Which data is authoritative?
4. Which decisions are deterministic?
5. What does AI contribute?
6. What happens when AI fails?
7. What exactly does the reviewer approve?
8. What can the system never do?
9. How would you detect regression?
10. Why is your final pilot decision justified?

If the learner cannot answer without reading generated text, the handover gate
has not passed.
