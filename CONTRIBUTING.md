# Contributing

Thanks for improving this GA4 tracking-plan skill package.

## Scope

Good contributions keep the skill focused on GA4 tracking-plan creation and review:

- measurement brief intake
- GA4 event and parameter design
- official GA4 recommended/ecommerce event checks
- native versus custom classification
- tracking-plan XLSX examples
- QA notes for analytics implementation

Implementation work for GTM, dataLayer, server-side tagging, or browser automation should be proposed separately unless the skill scope changes.

## Pull Requests

- Keep changes small and explain the analytics reason for the change.
- Update `skill/SKILL.md` when the skill behavior changes.
- Update examples in `files/` only when they remain reusable and non-sensitive.
- Do not commit client secrets, API keys, PII, private tracking plans, or proprietary analytics data.

## Validation

Before opening a pull request, confirm:

- `skill/SKILL.md` exists.
- The skill frontmatter includes `name` and `description`.
- The skill name remains lowercase hyphen-case.
- XLSX examples contain no personal data or confidential client data.
