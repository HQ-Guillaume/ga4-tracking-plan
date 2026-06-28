# Validation Commands

Use this file to decide which local checks to run and when.

## Package Checks

Run before committing or releasing the reusable skill package:

```powershell
python scripts/validate_package.py
git diff --check
git status --short
```

If Python is unavailable, run the non-Python checks and state the Python
blocker.

## Tracking Plan JSON Checks

Run when producing or reviewing a structured tracking plan:

```powershell
python scripts/validate_tracking_plan.py path\to\tracking-plan.json
python scripts/validate_tracking_plan.py path\to\tracking-plan.json --warnings-as-errors
```

The validator checks structure, journey alignment, event classifications,
official GA4 and Piano rules, ecommerce parameter scope, custom-event
justification, privacy-sensitive field names, and QA links.

## Workbook And CSV Checks

Run when generating reviewer-facing files:

```powershell
python scripts/generate_tracking_plan_workbook.py path\to\tracking-plan.json --output path\to\tracking-plan.xlsx
python scripts/export_tracking_plan_csv.py path\to\tracking-plan.json --output path\to\tracking-plan.csv
```

Generated files should remain outside the reusable skill package unless they
are deliberate, generic examples.
