# Acceptance Criteria

Use this file to decide whether a tracking plan is good enough to deliver.

## Complete Result Criteria

A complete tracking plan must show:

- scope, source evidence, assumptions, and open questions;
- website or journey coverage evidence when the request covers a broad site,
  multi-journey scope, or greenfield plan;
- journey-level measurement logic tied to business goals and analysis needs;
- events grouped so each journey is easy to identify, read, implement, and test;
- macro conversions, micro conversions, diagnostic events, and context events
  separated by role but connected to the same journey model;
- official GA4 events used when their meaning fits the action;
- GA4 ecommerce events isolated from non-ecommerce events and documented with
  official ecommerce event and item parameters;
- custom events justified by business or diagnostic value, with official
  alternatives considered;
- parameters reused consistently across events when they represent the same
  business concept;
- controlled values normalized and useful for reporting;
- not-tracked decisions for noisy, duplicate, sensitive, unavailable, or
  non-actionable interactions;
- QA cases linked to the same journey and event structure;
- next step that names the required approval, evidence, implementation, or QA.

## Journey And Parameter Synergy

The event set is acceptable only when proposed events and parameters work
together around the business goal and potential analysis needs.

For each meaningful journey:

- the plan should make related events easy to find in the Event Matrix;
- shared context parameters should be reused rather than reinvented;
- event-specific parameters should add useful analysis detail, not noise;
- conversion, progression, diagnostic, and context events should explain one
  coherent measurement flow;
- future pages or variants should be able to reuse the taxonomy without a full
  redesign.

## Privacy And Sensitive Data

Personal, sensitive, or user-provided data must not be silently included.

A plan can reference privacy-sensitive data when the use case requires it, such
as enhanced conversions, user-provided data, media matching signals, CRM/vendor
matching, or server-side processing. In those cases, the plan must clearly
highlight the field and state:

- why the field is needed;
- whether it is excluded from ordinary GA4 event parameters;
- whether it is used only for a specific platform feature or server/vendor
  process;
- consent, hashing, storage, and ownership expectations when relevant;
- required legal, privacy, or implementation validation.

The skill does not approve legal or privacy use. It marks the risk and required
validation path so users can handle it carefully.

## Failure Criteria

Mark the deliverable incomplete or blocked when:

- events are listed without business or analysis purpose;
- related journey events are scattered or hard to identify;
- ecommerce events omit required official GA4 ecommerce parameters;
- custom events are generic click tracking without a clear decision use;
- parameters have no reporting purpose or value rules;
- sensitive data is hidden inside generic fields;
- QA cases are missing for testable events;
- historical or Universal Analytics schema is copied into a GA4 plan.
- a whole-site plan has no explicit coverage map, source list, or uncovered
  journey assumptions.
