# GA4 Tracking Plan

[![Validate skill](https://github.com/HQ-Guillaume/ga4-tracking-plan/actions/workflows/validate-skill.yml/badge.svg)](https://github.com/HQ-Guillaume/ga4-tracking-plan/actions/workflows/validate-skill.yml)

Codex skill package for creating GA4 tracking plans from page or journey context.

## Contents

- `skill/` - Codex skill definition and UI metadata
- `files/lolivier_homepage_ga4_tracking_plan.xlsx` - Example homepage GA4 tracking plan for `https://www.lolivier.fr/`

## Skill Focus

The skill helps design GA4 tracking schemas that start from a measurement brief, verify official GA4 recommended and ecommerce events, classify native versus custom events and parameters, and produce implementation-ready tracking plans.

It is intentionally scoped to tracking-plan creation and review. GTM, dataLayer, and server-side implementation are separate follow-up phases.

## Install Locally

Copy the `skill/` folder into your local Codex skills directory and rename it to `ga4-tracking-plan`:

```text
%USERPROFILE%\.codex\skills\ga4-tracking-plan
```

The installed folder should contain:

```text
SKILL.md
agents/openai.yaml
```

## Example Prompt

```text
Use $ga4-tracking-plan to create a GA4 tracking schema for these pages and journeys.
```

## Release Asset

The latest release includes the example XLSX tracking plan as a downloadable asset.
