# GA4 Tracking Plan

[![Validate skill](https://github.com/HQ-Guillaume/ga4-tracking-plan/actions/workflows/validate-skill.yml/badge.svg)](https://github.com/HQ-Guillaume/ga4-tracking-plan/actions/workflows/validate-skill.yml)

Codex skill package for creating GA4 tracking plans from page or journey context.

## Contents

- `skill/` - Codex skill definition and UI metadata
- `skill/scripts/` - Runtime scripts bundled with the installed skill
- `files/ga4_tracking_plan_template_v2_1.xlsx` - Human-ready tracking plan template
- `files/ga4_event_scenario_library.xlsx` - GA4 event and scenario reference library
- `skill/references/` - Machine-readable and Markdown event scenario references used by the skill
- `scripts/create_tracking_plan_template.py` - Regenerates the default XLSX template
- `scripts/create_event_scenario_library.py` - Regenerates GA4 scenario references from official documentation
- `scripts/generate_tracking_plan_workbook.py` - Repo wrapper for the bundled JSON-to-XLSX generator
- `scripts/validate_tracking_plan.py` - Repo wrapper for the bundled JSON tracking-plan validator
- `scripts/export_tracking_plan_csv.py` - Repo wrapper for the bundled long-format CSV exporter
- `scripts/validate_package.py` - Validates skill structure, JSON contract, runtime scripts, workbook tabs, ecommerce matrix rules, generated workbook/CSV output, generic release surface, and common secret patterns

## Skill Focus

The skill helps design GA4 tracking schemas that start from a measurement brief, verify official GA4 recommended and ecommerce events, classify native versus custom events and parameters, and produce implementation-ready tracking plans.

It is intentionally scoped to tracking-plan creation and review. GTM, dataLayer, and server-side implementation are separate follow-up phases.

The included event scenario library helps map common website scenarios to automatic, enhanced-measurement, recommended, ecommerce, and typical custom events with expected parameters and dataLayer patterns.

The package also includes scenario-specific playbooks for ecommerce, lead generation, search/listing, account/support/content, SPA routing, data quality/privacy, official-first review, example comparison, ecommerce parameter policy, and QA readiness. These keep the main skill concise while giving the agent targeted references for different tracking-plan situations.

Tracking plans generated with this skill consolidate repeated same-name events whenever the same trigger logic and parameter structure can cover multiple components. Controlled analytics values should use lowercase ASCII `snake_case`, with accents removed, so French labels such as `Nouveautes` become `nouveautes`.

Ecommerce events are handled as a stricter case: they should stay in ecommerce-only blocks and use the official GA4 ecommerce parameter names, including required item parameters from Google documentation. GTM/dataLayer wrapper paths such as `ecommerce.items` are implementation mapping details, not replacements for GA4 parameters like `items` and `items[].item_id`.

## Canonical JSON Contract

Reusable or QA-ready plans should follow `skill/references/tracking_plan_schema.json`. The schema includes the measurement brief, events, parameter dictionary, custom definitions, key events, not-tracked decisions, documentation sources checked, assumptions, and one QA case per testable event.

`skill/references/generic_tracking_plan_fixture.json` is a generic example of that contract. It is intentionally based on `example.com` and placeholder values only.

To generate an XLSX workbook from a JSON plan:

```text
python scripts/generate_tracking_plan_workbook.py skill/references/generic_tracking_plan_fixture.json --output generated_tracking_plan.xlsx
```

To validate a JSON plan and export a long-format CSV:

```text
python scripts/validate_tracking_plan.py skill/references/generic_tracking_plan_fixture.json
python scripts/export_tracking_plan_csv.py skill/references/generic_tracking_plan_fixture.json --output generated_tracking_plan.csv
```

Generated client plans, screenshots, GTM previews, request exports, and test evidence should stay outside this generic package unless they are deliberately anonymized fixtures.

## Install Locally

Copy the `skill/` folder into your local Codex skills directory and rename it to `ga4-tracking-plan`:

```text
%USERPROFILE%\.codex\skills\ga4-tracking-plan
```

The installed folder should contain:

```text
SKILL.md
agents/openai.yaml
assets/ga4_tracking_plan_template.xlsx
references/
scripts/
```

## Example Prompt

```text
Use $ga4-tracking-plan to create a GA4 tracking schema for these pages and journeys.
```

## Release Asset

The latest release includes only generic skill assets: the tracking-plan template and event scenario library. Site-specific tracking plans, tests, client artifacts, and confidential files should not be committed or attached to releases.

## Validate Locally

```text
python -m pip install -r requirements.txt
python scripts/validate_package.py
```
