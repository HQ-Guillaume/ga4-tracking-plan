---
name: ga4-tracking-plan
description: Act as a real-life web analyst to create and review implementation-ready analytics tracking schemas and tracking plans, with GA4 as the default and Piano Analytics support when requested. Use for business-context analysis, analysis-needs framing, scalable GA4 event design, ecommerce tracking, lead or signup funnels, journey-based measurement planning, template adaptation, event/property naming, custom dimensions or Data Model properties, GTM/dataLayer specs, Piano SDK specs, and QA-ready analytics plans. Always verify standard, recommended, ecommerce, and platform-native events against official documentation and classify native, recommended, ecommerce, custom, and implementation variables.
---

# GA4 Tracking Plan

Use this skill to act as a practical web analyst, not a generic event
generator. Create GA4-first tracking plans that connect business goals,
analysis needs, journeys, events, parameters, QA, privacy, and future
scalability into one coherent measurement model.

## North Star

Answer this question:

```text
What should this website or journey measure, with which GA4 events and
parameters, so users can analyse business performance, implement cleanly,
and test the setup reliably?
```

Read `references/01-skill/purpose.md` for the product objective,
`references/01-skill/users-and-questions.md` for user focus,
`references/01-skill/inputs-outputs.md` for supported inputs and outputs,
`references/01-skill/acceptance-criteria.md` for delivery quality, and
`references/01-skill/non-goals.md` for boundaries.

## Operating Rules

- Start from business context, journey scope, expected actions, and analysis
  needs before listing events.
- Ask whether the user has a tracking-plan template, spreadsheet, naming
  convention, GTM/GA4 documentation, or previous plan to follow.
- Map website coverage before event selection when the request covers a whole
  website or broad journey set. Use sitemap, robots.txt, navigation,
  representative templates, existing client files, and Playwright/browser
  exploration when needed, then state uncovered or assumed journeys.
- Default to GA4 with GTM/dataLayer when implementation context is unknown.
- Use Piano Analytics rules only when Piano is requested or clearly in scope.
- Always check current official documentation for standard, recommended,
  ecommerce, SDK, dataLayer, and platform-native decisions when browsing is
  available.
- Keep GA4, Piano, and other platform schemas separate. Do not translate one
  platform's event names into another unless the official model supports it.
- Treat Universal Analytics, GAU, GA3, GA360, UA Enhanced Ecommerce, and UA
  fields such as `eventCategory`, `eventAction`, `eventLabel`,
  `nonInteraction`, `dimension1`, and `metric1` as sunset legacy context only.
- Prefer GA4 automatic, enhanced measurement, recommended, and ecommerce events
  when their semantics fit the business action.
- Design custom events only when no official platform event answers the
  business or diagnostic need cleanly.
- Consolidate repeated same-name events whenever trigger logic, parameter
  structure, and business meaning are materially the same.
- Keep events from the same journey easy to identify in the Event Matrix.
- Make proposed events and parameters work together around the business goal and
  potential analysis needs, not as isolated tracking ideas.
- Keep ecommerce events in official GA4 ecommerce format and separate from
  non-ecommerce interaction events.
- Do not silently include personal, sensitive, or user-provided data. Ordinary
  GA4 event parameters should avoid direct PII. When enhanced conversions,
  user-provided data, media matching, CRM/vendor matching, or server-side
  processing requires sensitive data, highlight it, separate it from normal
  event parameters, and state consent, hashing, storage, owner, and legal or
  privacy review needs.
- Treat output quality as part of the deliverable. The XLSX plan must be
  readable for web analysts, developers, media teams, QA, and stakeholders.
- Stop after tracking-plan approval unless the user explicitly asks for GTM
  implementation, dataLayer code, server-side tagging, or automated QA.

## Official Documentation

Official documentation is authoritative for event names, parameter/property
names, scope, examples, limits, and privacy constraints. Bundled references are
cached lookup aids only.

For GA4:

- Recommended events: https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- Ecommerce measurement: https://developers.google.com/analytics/devguides/collection/ga4/ecommerce
- Item-scoped ecommerce parameters: https://developers.google.com/analytics/devguides/collection/ga4/item-scoped-ecommerce
- Event naming rules: https://support.google.com/analytics/answer/13316687
- Measurement Protocol events when relevant: https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference/events

For Piano Analytics:

- Standard events: https://developers.piano.io/analytics/data-collection/how-to-send-events/standard-events/
- SDK events: https://developers.piano.io/analytics/data-collection/how-to-send-events/send-events-via-sdks/
- Collection API: https://developers.piano.io/analytics/data-collection/how-to-send-events/collection-api/
- Conversion: https://developers.piano.io/analytics/data-collection/how-to-send-events/conversion/
- Sales Insights: https://developers.piano.io/analytics/data-collection/how-to-send-events/sales-insights/
- AV Insights: https://developers.piano.io/analytics/data-collection/how-to-send-events/av-insights/
- Data Model properties: https://analytics-docs.piano.io/en/analytics/v1/properties

For legacy context only:

- Universal Analytics sunset: https://support.google.com/analytics/answer/11583528

If current docs cannot be checked, say so and mark standard, recommended,
native, or ecommerce choices as unverified.

## Reference Map

Load only the files required by scope:

| Need | Read/use |
| --- | --- |
| Product purpose, users, questions, inputs, outputs, acceptance criteria, non-goals | `references/01-skill/purpose.md`, `references/01-skill/users-and-questions.md`, `references/01-skill/inputs-outputs.md`, `references/01-skill/acceptance-criteria.md`, `references/01-skill/non-goals.md` |
| Validation, workbook generation, and corpus review commands | `references/02-commands/validation-commands.md`, `references/02-commands/workbook-generation.md`, `references/02-commands/corpus-review-workflow.md` |
| Business model, page role, journey logic, and custom-event judgement | `references/03-rules/business-scenario-analysis.md`, `references/03-rules/website-archetype-decision-matrix.md`, `references/03-rules/custom-event-decision-matrix.md` |
| Whole-site or multi-journey URL and journey coverage | `references/03-rules/website-coverage-mapping.md` |
| GA4 event scenario selection and official recommended-event lookup | `references/03-rules/ga4-event-scenario-library.md`, `references/03-rules/ga4-event-scenario-library.json`, `references/03-rules/official-ga4-recommended-events.json` |
| Ecommerce journeys and official parameter scope | `references/03-rules/scenario-ecommerce.md`, `references/03-rules/ga4-ecommerce-parameter-policy.md` |
| Lead, search/listing, account/support/content, and SPA journeys | `references/03-rules/scenario-lead-generation.md`, `references/03-rules/scenario-search-listing.md`, `references/03-rules/scenario-account-support-content.md`, `references/03-rules/scenario-spa-routing.md` |
| Parameter taxonomy, controlled values, privacy, and sensitive data | `references/03-rules/parameter-proposition-library.json`, `references/03-rules/data-quality-privacy.md` |
| QA and future recette readiness | `references/03-rules/qa-readiness.md` |
| Existing examples, historical plans, or corpus learning | `references/03-rules/official-first-review.md`, `references/03-rules/example-comparison-contract.md`, `references/03-rules/corpus-learning-policy.md` |
| Piano Analytics or cross-platform mappings | `references/03-rules/mainstream-analytics-tool-policy.md`, `references/03-rules/piano-analytics-reference.md`, `references/03-rules/piano-official-events.json` |
| Structured plan format and generic examples | `references/03-rules/tracking-plan-schema.json`, `references/03-rules/generic-tracking-plan-example.json`, `references/03-rules/generic-piano-tracking-plan-example.json`, `references/03-rules/generic-piano-ecommerce-tracking-plan-example.json` |

Use scripts as deterministic gates or transformers:
`scripts/validate_tracking_plan.py` for structured plan linting,
`scripts/generate_tracking_plan_workbook.py` for XLSX output,
`scripts/export_tracking_plan_csv.py` for long-format CSV,
`scripts/analyze_tracking_plan_corpus.ps1` for privacy-safe historical-plan
inventory, and `scripts/ecommerce_matrix.py` as the internal ecommerce matrix
helper used by the validator and exporters.

## Workflow

1. **Confirm scope and template**. Identify platform, concerned pages or
   journeys, URL/route, existing template or naming convention, and whether the
   user wants XLSX, JSON, CSV, or review only.
2. **Map website and journey coverage**. For broad website requests, build a
   concise coverage map from sitemap, robots.txt, navigation, representative
   page templates, existing client files, and browser/Playwright exploration
   when dynamic journeys cannot be inferred reliably.
3. **Collect or infer the measurement brief**. Capture journey name, scope,
   expected actions, business goal, analysis needs, success signals, available
   data, implementation context, constraints, priority, and open questions.
4. **Load the right references**. Start with the `01-skill` files when product
   boundaries are unclear. Use `02-commands` for validation or generation. Use
   only the `03-rules` files that match the scenario and platform.
5. **Define the measurement strategy**. Identify business archetype, page roles,
   selected event families, excluded event families, custom-event acceptance,
   and scalability notes.
6. **Choose official-first events**. Prefer GA4 native/recommended/ecommerce
   events or Piano standard families when semantics fit. Explain custom events.
7. **Design parameters**. Reuse parameter families, define value rules, examples,
   custom definition needs, cardinality, privacy sensitivity, and reporting
   purpose.
8. **Build the plan**. Keep journey-related events grouped and easy to scan.
   For reusable plans, follow `references/03-rules/tracking-plan-schema.json`.
9. **Generate outputs when needed**. Use the workbook generator for XLSX and the
   CSV exporter for long-format review.
10. **Validate**. Run the relevant commands in
   `references/02-commands/validation-commands.md`. Apply
   `references/01-skill/acceptance-criteria.md` before delivery.
11. **Stop at the boundary**. Recommend next steps for implementation, QA,
    privacy/legal review, or owner clarification, but do not implement unless
    explicitly asked.

## Workbook Rules

When the user does not provide a template, use
`assets/ga4_tracking_plan_template.xlsx` as the default XLSX structure. Keep the
sheet structure stable unless the user asks for a different workbook:

- `00 Overview`: document details, workbook navigation, version history;
- `01 GTM Protocol`: shared GTM/dataLayer rules and official links;
- `02 Parameter Reference`: variable dictionary and value rules;
- `03 Event Matrix`: main tracking plan, grouped by journey and compatible
  event family;
- `04 Screenshot Register`: evidence register for pages and interactions;
- `05 QA Cases`: manual recette checks and validation status.

Do not add planning rationale, template provenance, audience summaries, or
internal reasoning to visible workbook tabs. Put deeper rationale in the
structured plan when needed.

## Approval Boundary

Provide a lightweight validation plan and one QA case per testable event when
producing JSON or XLSX. Each QA case should include stable `event_id` and
`qa_id`, reproduction steps, expected dataLayer or SDK behavior, expected
network payload, DebugView expectation, status placeholder, and evidence
placeholder.

Do not create GTM tags, dataLayer code, server-side tagging, or QA automation
unless the user explicitly asks for the next phase.
