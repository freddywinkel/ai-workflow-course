# Cost Controls for the €60 Prototype

## What €60 means

€60 is the maximum allocation for the prototype, not a spending target and not
a guaranteed technical cutoff. The safest condition is that Google Cloud still
shows **Free trial** and an **Activate** button and the learner never clicks
that button.

Ordinary Cloud Billing budgets send alerts; they do not stop use. Preview Spend
cap budgets can pause new use of an eligible service, but they are delayed,
service-specific, and may not stop in-flight or persistent-storage charges.

## Control stack

| Control | Prototype setting | Strength |
|---|---|---|
| account state | unactivated Free Trial | strongest protection against charging a payment method; trial credit can still be consumed |
| project alert budget | €40, project only | alerts at 25%, 50%, 75%, 90%, 100%; not a stop |
| Vertex AI spend cap | €5 if Preview is offered | pause control with delay; not an exact final cap |
| Cloud Run spend cap | €5 if Preview is offered | pause control with delay; not an exact final cap |
| untouched reserve | at least €10 | planning buffer, not a technical control |
| source allowlist | six exact synthetic hashes | hard application gate |
| request limit | 5,000,000 bytes and three pages | hard application gate |
| lifetime use | 20 runs and 60 pages | transactional Firestore gate |
| Gemini bounds | 24,000 input characters and 800 output tokens | hard request settings |
| Cloud Run | minimum zero, maximum one, concurrency one | strong throttle; maximum instances can briefly be exceeded |
| date | live calls stop 20 October 2026 | hard application gate if clock/configuration are correct |
| trial expiry | 26 October 2026 | external deadline; teardown is six days earlier |

Document AI and Artifact Registry are not currently listed among the services
covered by Preview Spend cap budgets. The allowlist, page/run limits, private
authentication, one-instance throttle, and same-session teardown cover that
gap.

## Relevant current list prices

Google publishes prices in United States dollars. Currency conversion, tax,
region, shared billing-account free usage, and future price changes mean these
figures are planning evidence, not a quote.

- Document AI Enterprise Document optical character recognition (OCR): first
  1,000 pages per month per account are currently listed at $0, then $1.50 per
  1,000 pages. Do not create Form Parser/custom extraction or custom processor
  hosting.
- Gemini 3.5 Flash-Lite non-global standard processing is currently listed at
  $0.594 per million input tokens and $4.95 per million output tokens.
- Cloud Run request-based free usage currently includes 180,000 virtual central
  processing unit seconds, 360,000 gibibyte-seconds, and two million requests
  monthly per billing account.
- Artifact Registry currently includes 0.5 gibibyte-month per billing account
  without charge.
- Eligible Cloud Build default-pool use currently includes a monthly free
  allocation.

A deliberately conservative example of 0.5 million Gemini input tokens and
0.1 million output tokens is about $0.79 at those model prices. A small
five-document proof should normally be much lower, but do not rely on this
estimate. Free allocations may already be used elsewhere and billing data can
lag.

## Before deployment

1. Confirm the page says **Free trial** and still shows **Activate**.
2. Do not click **Activate**, **Upgrade**, or any paid-account prompt.
3. Link only the dedicated project to the already-confirmed Free Trial.
4. Create the €40 project-scoped alerts.
5. Add €5 Vertex AI and €5 Cloud Run Spend cap budgets if available.
6. Record `PREVIEW NOT AVAILABLE` honestly if the control is absent.
7. Stop if the billing currency is not euros until a conversion is reviewed.
8. Run every offline test.
9. Confirm the 20 October hard stop and same-session teardown.

## During the proof

- Keep the service private.
- Run the automated live validation once.
- Perform at most the one documented C006 recreation.
- Do not retry a provider failure repeatedly.
- Do not enable Provisioned Throughput, graphics processing units, minimum
  instances, custom processors, grounding, public access, or extra regions.
- Check Billing reports after deployment and after validation.
- Treat a displayed low amount as delayed, not final.

The application counter reserves a run before the provider call. A failed
provider call may therefore consume a run allowance. This is intentional:
failures must not create an unlimited retry path.

## Alerts, caps, and quotas are different

- **Alert:** tells a person about estimated spend; it does not stop use.
- **Spend cap:** pauses new use for one eligible project/service after Google
  processes the threshold; it can still overshoot.
- **Quota:** blocks request volume; it does not know the learner's €60 business
  limit.
- **Application gate:** fixed code refuses files, pages, runs, tokens, dates, or
  unauthorised states before more work is attempted.

Do not use a programmatic “disable billing when a Pub/Sub message arrives”
tutorial for this beginner prototype. Budget notifications can lag, and
automatic billing disablement can make resources unavailable before evidence
or cleanup is safely completed.

## After validation

Run teardown in the same work session. Check Billing reports after deletion and
again the next day because costs can settle later. Never activate paid billing
to keep the demo running.

For teardown, the ordinary alerts-only budget and the two Preview spend caps
are not handled in the same way:

- delete the exact-name ordinary alerts-only budget through the public Cloud
  Billing Budget application programming interface (API); and
- delete the two exact-name Preview spend caps in the Billing user interface,
  then verify that both rows are absent.

Do not claim that the public Budget API removed a Preview spend cap. The
current teardown script deliberately limits public-API deletion to the
ordinary alerts-only budget.

## Recorded cost result — 28 July 2026

For the completed reference proof:

- the Billing page continued to show **Free trial** and **Activate**;
- paid activation remained `NO`;
- the €40 ordinary alert and both €5 Preview spend caps were present before
  the live proof;
- the displayed amount after validation and teardown was €0; and
- €0 is only the value visible at those recorded times, because Billing data
  may arrive later.

During teardown, the ordinary alert was deleted and verified absent through
the public API. The two Preview spend caps were deleted and verified absent in
the Billing user interface. The final Billing page check showed zero course
budget rows. The dedicated project then entered `DELETE_REQUESTED`.

## Current official Google references

- [Google Cloud Free Trial](https://docs.cloud.google.com/free/docs/free-cloud-features)
- [Budgets and alert limitations](https://docs.cloud.google.com/billing/docs/how-to/budgets)
- [Preview Spend cap budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)
- [Document AI pricing](https://cloud.google.com/products/document-ai/pricing)
- [Gemini through Vertex AI pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)
- [Cloud Run pricing and free usage](https://cloud.google.com/run/pricing)
- [Artifact Registry pricing](https://cloud.google.com/artifact-registry/pricing)
- [Cloud Build pricing](https://cloud.google.com/build/pricing)
- [Cloud Run maximum-instance limits](https://docs.cloud.google.com/run/docs/configuring/max-instances-limits)
- [Document AI quotas](https://docs.cloud.google.com/document-ai/quotas)
