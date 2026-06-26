---
name: ga4-tracking-plan
description: Create and review Google Analytics 4 tracking schemas and tracking plans. Use when the user wants GA4 event design, ecommerce tracking, lead or signup funnel tracking, journey-based measurement planning, tracking-plan template adaptation, event and parameter naming, custom dimension planning, or implementation-ready analytics specifications before GTM, gtag.js, dataLayer, or server-side implementation. Always verify standard GA4 and ecommerce events against official Google Analytics documentation and classify native, recommended, ecommerce, custom events, parameters, and implementation variables.
---

# GA4 Tracking Plan

Create an implementation-ready GA4 tracking schema that is useful for analysis, not just a list of trackable interactions. Optimize for business questions, clean reporting, low noise, privacy, and maintainable implementation.

## Operating Rules

- Start from the user's measurement context and concerned journeys before designing events.
- Ask whether the user already has a tracking plan template, spreadsheet, schema file, naming convention, or previous GA4/GTM documentation.
- If a template exists, analyze its structure and reuse its format where practical.
- Always check current official Google Analytics and Google Tag Manager documentation before recommending standard, recommended, ecommerce, dataLayer, or GTM setup decisions.
- Privilege official GA4/GTM setup over client examples unless the user explicitly asks to preserve a legacy implementation.
- Prefer GA4 automatic, enhanced measurement, and recommended events when their semantics fit.
- Design custom events only when no native or recommended GA4 option answers the business need cleanly.
- Explicitly flag native, recommended, ecommerce, custom, and implementation-specific fields.
- Never collect direct PII or contact-derived identifiers in GA4, including email, phone, hashed email, hashed phone, customer IDs, postal addresses, order notes, or free-text messages. Flag PII and data minimization risks.
- Avoid low-signal click tracking unless it answers a real analysis question.
- Consolidate repeated same-name events whenever the trigger logic, parameter structure, and business meaning are materially the same; use one event definition and list possible values per variable instead of creating many near-duplicate event columns.
- Do not block plan creation when implementation context is unknown. If the user gives only a page or journey, assume a standard GTM web container with dataLayer and GA4 web stream, then flag the assumption.
- When a plan should be reusable, testable, or converted to XLSX, design it against `references/tracking_plan_schema.json`.
- Keep future QA usage in mind: each testable event should have a stable `event_id`, `qa_id`, expected dataLayer behavior, expected GA4/network payload, and test status.
- Never commit or release client-specific tracking plans, screenshots, test evidence, URLs, exports, or confidential data into a generic skill package.
- Stop after the GA4 tracking schema or tracking plan is approved unless the user asks for implementation.

## Official Documentation

Use official Google sources for GA4 standard decisions. Browse or otherwise verify current docs during the task when available. Official documentation is authoritative for event names, parameter names, parameter scope, dataLayer examples, GTM mapping, reserved names, limits, and privacy constraints. Bundled official-reference files are cached lookup aids only; do not treat them as a replacement for checking current official docs when browsing is available.

- Recommended events: https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- Ecommerce measurement: https://developers.google.com/analytics/devguides/collection/ga4/ecommerce
- Item-scoped ecommerce parameters: https://developers.google.com/analytics/devguides/collection/ga4/item-scoped-ecommerce
- Event naming rules: https://support.google.com/analytics/answer/13316687
- Measurement Protocol event constraints when relevant: https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference/events

If current docs cannot be checked, say so and mark standard/recommended choices as unverified.

## Official-First Review

When reviewing an existing tracking plan example, translating a legacy implementation plan into GA4, or preparing a plan for future QA/recette usage, read `references/official_first_review.md`. When comparing a fresh draft with user-provided examples, also read `references/example_comparison_contract.md`. Use them to lint event names, parameter scope, dataLayer examples, privacy risks, mandatory flags, workbook density, and QA readiness against official GA4/GTM setup.

## Default Workbook Template

When the user does not provide an existing tracking-plan template, use `assets/ga4_tracking_plan_template.xlsx` as the default human-facing XLSX structure. Adapt its sheets and event matrix to the user's journeys instead of inventing a new workbook layout.

Treat the bundled XLSX template as the primary delivery format for analyst-facing tracking plans. Improve readability through the generator's styling and grouping rules, but keep the default sheet structure stable unless the user explicitly asks for a different workbook.

For template improvements learned from examples, prefer reusable sections inside the stable workbook: workbook navigation, compact event inventory, custom-definition registration, grouped event matrix, and QA/recette records. Do not create one tab per event by default unless the user explicitly asks for that format.

When the plan is available as canonical JSON and an XLSX artifact is requested or implied, use `scripts/generate_tracking_plan_workbook.py` from this skill folder to generate the workbook rather than manually rebuilding every sheet. Run `scripts/validate_tracking_plan.py` first, or rely on the generator's built-in validation gate, before sharing workbook output.

Use `scripts/export_tracking_plan_csv.py` only when the user requests CSV output or needs a secondary long-format view for review, QA ingestion, or diffing. Do not replace the default workbook template with a CSV-only deliverable. The CSV includes event context, parameter scope, requirement, expected value, availability, and scope rule for each row.

`scripts/ecommerce_matrix.py` is the internal ecommerce parameter and matrix helper used by the workbook generator, CSV exporter, and JSON validator.

## Reference Routing

Before designing events, read `references/ga4_event_scenario_library.md` when available. Use it to map the user's website or journey to:

- automatic and enhanced-measurement events
- official GA4 recommended events
- official GA4 ecommerce events and item parameters
- typical custom events by scenario
- expected event variables/parameters
- dataLayer push formats and GTM mapping notes

Use `references/ga4_event_scenario_library.json` for structured lookup when producing machine-readable tracking-plan outputs. Treat typical custom events in the library as patterns, not standards: always prefer official GA4 events when their semantics match.

Read only the additional scenario references that match the requested scope:

- `references/scenario_ecommerce.md` for product, cart, checkout, purchase, refund, and promotion journeys
- `references/ga4_ecommerce_parameter_policy.md` for official ecommerce parameter scope, event-level versus item-level fallback rules, stable row order, and matrix grouping
- `references/scenario_lead_generation.md` for forms, quote flows, signup, appointment, callback, and lead submission
- `references/scenario_search_listing.md` for search, filters, listing pages, result selection, and product discovery lists
- `references/scenario_account_support_content.md` for account entry, login/signup context, support, FAQ, downloads, content, video, and contact intent
- `references/scenario_spa_routing.md` for single-page apps, client-side routing, virtual pages, and duplicate page_view risk
- `references/data_quality_privacy.md` for naming, value normalization, data minimization, cardinality, and privacy checks
- `references/qa_contract.md` for DebugView, GTM Preview, network, evidence, and future testing-skill readiness
- `references/official_first_review.md` when reviewing example plans, translating legacy wrappers, or optimizing for both web analysts and future QA/recette agents
- `references/example_comparison_contract.md` when comparing a generated plan with user-provided examples and deciding whether the skill should evolve
- `references/tracking_plan_schema.json` when producing machine-readable JSON
- `references/generic_tracking_plan_fixture.json` as a generic example of the contract only, never as client evidence
- `references/official_ga4_recommended_events.json` for structured official recommended-event lookup when available

## Step 1: Collect Measurement Brief

Before creating the schema, collect the context for each concerned page or user journey. Ask concise questions when important fields are missing; if the user cannot answer everything, continue with clear assumptions and open questions.

Collect:

- `journey_name`: clear name such as Product discovery, Lead form submission, Checkout, Account signup
- `scope`: what is included and excluded
- `url_or_route`: exact URL, route pattern, or app screen
- `page_type`: landing page, listing page, product page, cart, checkout, form, account area, content page
- `expected_user_actions`: views, clicks, submissions, searches, filters, downloads, video plays, purchases, errors
- `business_goal`: why the journey matters
- `analysis_needs`: questions the tracking must answer
- `success_signals`: conversions, key events, funnel steps, revenue actions, qualified engagement
- `audience_or_segment_needs`: user type, login state, customer type, country, device, campaign
- `data_available`: page metadata, product data, form metadata, transaction data, user/account state
- `implementation_context`: GTM, gtag.js, dataLayer, CMS, ecommerce platform, SPA routing, server-side tagging. If unknown, assume standard GTM + dataLayer and continue.
- `constraints`: privacy, PII risk, technical limits, reporting limits
- `priority`: `must`, `should`, or `could`

Summarize the interpreted brief before the event schema:

| journey_name | scope | url_or_route | expected_actions | analysis_needs | priority | open_questions |
|---|---|---|---|---|---|---|

## Step 2: Define Measurement Strategy

For each journey, identify:

- macro conversions and whether they should be GA4 key events
- micro conversions that explain funnel progression
- diagnostic events that help debug drop-off or UX friction
- events that should be avoided because they are noisy, redundant, or not actionable
- reporting dimensions and segments needed to answer the analysis questions

Prefer fewer, better events with useful parameters over many single-purpose events.

## Step 3: Select GA4 Event Types

Classify every event:

- `automatic`: collected by GA4 without custom implementation
- `enhanced_measurement`: collected by GA4 enhanced measurement when enabled and sufficient
- `recommended`: official GA4 recommended event
- `recommended_ecommerce`: official GA4 ecommerce event
- `custom`: business-specific event

For ecommerce journeys:

- verify event names and parameters against current official ecommerce docs
- keep ecommerce events in ecommerce-only event blocks; do not mix ecommerce event slots with page, search, signup, support, account, or other interaction events in the same matrix block
- split ecommerce blocks by compatible parameter family, for example promotions, product lists, product detail, cart, checkout, and transactions
- list ecommerce rows using the official GA4 event parameter names and item parameter names, for example `currency`, `value`, `transaction_id`, `items`, `items[].item_id`; do not substitute generic interaction fields such as `event_data.*` inside ecommerce event definitions
- respect parameter scope. Prefer event-level list and promotion parameters when all items share the same list or promotion. Use item-level equivalents only when items in the same event genuinely need different values.
- use the official `items` array pattern where applicable
- include every official required or conditionally required ecommerce parameter for the selected event; if a required parameter is unavailable, mark the event as not implementable for that context rather than weakening the GA4 ecommerce format
- include official optional ecommerce parameters when the business or page data can provide them, and mark unavailable optional parameters as `not_available`, `not_applicable`, or `event_level_used` rather than leaving them visually missing
- classify non-official item fields as `custom_item_parameter`, never as `ga4_ecommerce_item_parameter`; add them only when they answer a clear analysis need and list a matching item-scoped custom dimension if GA4 UI reporting is required
- use official `items[].item_variant` for product variant/color when it is sufficient; do not create separate custom color or size item fields by default
- include stable item identifiers and merchandising context when available
- require transaction identifiers for purchase-like events to support deduplication
- avoid inventing ecommerce event names when an official GA4 ecommerce event fits

For custom events:

- explain the business reason
- identify the page, component, or journey step
- state why native, enhanced, recommended, or ecommerce GA4 events are not sufficient
- flag required custom dimensions or metrics

## Step 4: Design Names And Parameters

Use GA4-safe names:

- lowercase `snake_case`
- start with a letter
- use only letters, numbers, and underscores
- avoid reserved names and prefixes
- keep names semantic and stable

Normalize controlled values used for analysis:

- use lowercase ASCII `snake_case` values by default
- replace spaces, punctuation, and separators with underscores
- remove accents and other diacritics, especially for French labels
- keep values concise and stable, for example `Nouveautes` -> `nouveautes`, `Pret-a-porter femme` -> `pret_a_porter_femme`, `60+` -> `60_plus`
- list finite options as normalized values separated by ` | `
- preserve official IDs, ISO codes, numeric values, URLs, and raw native/user-entered fields only when required or explicitly intended, such as `page_title`, `page_location`, `search_term`, `item_name`, or product IDs
- never normalize by sending PII or sensitive raw text to GA4

Classify every parameter, property, or implementation variable:

- `ga4_auto_collected_parameter`
- `ga4_native_parameter`
- `ga4_recommended_parameter`
- `ga4_ecommerce_item_parameter`
- `custom_event_parameter`
- `custom_item_parameter`
- `custom_user_property`
- `gtm_builtin_variable`
- `data_layer_variable`
- `custom_javascript_variable`
- `dom_selector_variable`
- `server_variable`

For each parameter, define:

- type
- scope: `event`, `user`, or `item`
- required status
- example value
- allowed values when finite
- source of truth
- reporting purpose
- custom dimension or custom metric registration need
- cardinality risk
- PII or data minimization risk

## Step 5: Build The Tracking Schema

In XLSX event matrices, an event slot should represent one reusable event definition, not one visual component whenever the same event can cover multiple components. For example, use one `select_content` slot for category, size, and catalogue-entry selections when the only difference is `content_type`, `content_id`, `content_name`, or `cta_location`. Use one `view_promotion` slot and one `select_promotion` slot for homepage promotions when the same official ecommerce parameter structure applies. Split into separate event slots only when the trigger, data availability, QA method, business meaning, or official GA4 event format is genuinely different.

For ecommerce XLSX blocks:

- use ecommerce-only blocks such as `Ecommerce promotions`, `Product list`, `Cart`, `Checkout`, or `Purchase`
- keep compatible ecommerce families separate when their event-level parameters differ materially. Do not group product-list, PDP, cart, checkout, and purchase events into the same event matrix block merely because they are part of one journey.
- use official GA4 ecommerce parameter names in the matrix rows (`currency`, `value`, `items`, `items[].item_id`, etc.)
- keep dataLayer wrapper paths such as `ecommerce.currency` as implementation notes or GTM mapping details, not as replacements for the official GA4 parameter names
- use a stable official-first row order inside each ecommerce family and show `not_available`, `not_applicable`, or `event_level_used` for rows that are not sent
- do not add custom interaction rows to ecommerce events unless they are clearly documented custom event or item parameters and do not replace required GA4 ecommerce parameters
- if the page cannot provide required ecommerce parameters, recommend a non-ecommerce intent event instead of forcing an incomplete ecommerce event

Default event table columns:

| event_name | classification | official_ga4_match | business_question | trigger | page_or_component | key_event | parameters | parameter_classification | priority | custom_dimension_needed | documentation_checked | implementation_notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Also include:

- Common parameters shared across events
- Event-specific parameters
- User properties, only when analytically justified
- Key event recommendations
- Custom dimensions and metrics to register in GA4
- Events intentionally not tracked and why
- Assumptions and open questions

When the user requests a machine-readable artifact, produce `ga4-tracking-schema.json` with this shape:

```json
{
  "schema_version": "1.0.0",
  "plan_id": "project_or_journey_id",
  "document": {},
  "measurement_brief": [],
  "events": [],
  "parameters": [],
  "custom_definitions": [],
  "key_events": [],
  "not_tracked": [],
  "assumptions": [],
  "documentation_sources_checked": [],
  "qa_cases": []
}
```

The full required structure is defined by `references/tracking_plan_schema.json`. Use it as the source of truth when generating or validating machine-readable plans.

## Step 6: Analyst Review

Before finalizing, review the plan as a web analyst:

- Does every event answer a stated business question?
- Are macro conversions separated from supporting interactions?
- Are funnel steps measurable without overtracking every click?
- Are native GA4 events and parameters used where appropriate?
- Are custom events justified and named consistently?
- Are parameters useful for segmentation and reporting?
- Are repeated same-name events consolidated where possible, with possible values listed per variable?
- Are controlled values normalized to lowercase ASCII `snake_case`, with accents removed where needed?
- Are ecommerce events isolated from non-ecommerce events and documented with official GA4 ecommerce parameters?
- Are all required or conditionally required ecommerce parameters present, especially `items`, one of `items[].item_id` or `items[].item_name`, and `transaction_id` for purchase/refund?
- Are high-cardinality fields avoided or flagged?
- Are PII and data minimization risks flagged?
- Is ecommerce revenue deduplication possible?
- Are expected reports, explorations, or audiences supported by the schema?
- Is implementation feasible from available page, dataLayer, or server data?

## Step 7: QA And Approval Boundary

Provide a lightweight validation plan and, when producing a JSON/XLSX artifact, include one QA case per testable event:

- DebugView checks
- GTM Preview checks when GTM is in scope
- browser/network request checks
- expected parameter examples
- funnel or key event validation cases
- ecommerce purchase deduplication checks when relevant

Each QA case should include:

- stable `event_id` and `qa_id`
- reproduction steps
- expected dataLayer keys and values
- expected GA4/network event name and important parameters
- DebugView expectation
- status placeholder: `Cannot test` in XLSX drafts or `not_started` in JSON drafts
- evidence placeholder for future screenshots, request exports, or notes

Stop after schema approval. Do not create GTM tags, dataLayer code, server-side tagging, or QA automation unless the user explicitly asks for the next phase.
