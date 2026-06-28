# Workbook Generation

Use this file when a tracking plan should be delivered as XLSX.

## Default Flow

1. Create or update the structured tracking-plan JSON.
2. Validate the JSON with `scripts/validate_tracking_plan.py`.
3. Generate the workbook with `scripts/generate_tracking_plan_workbook.py`.
4. Review the Event Matrix for journey grouping, value rules, and test status
   columns.
5. Keep generated workbooks outside the reusable skill package unless they are
   generic examples.

## Command

```powershell
python scripts/generate_tracking_plan_workbook.py path\to\tracking-plan.json --output path\to\tracking-plan.xlsx
```

## Human Readability Check

Before delivery, confirm:

- the Overview tab is limited to document details, workbook navigation, and
  version history;
- GTM Protocol contains shared implementation rules and official links;
- Parameter Reference uses human-readable labels and value rules;
- Event Matrix groups events by journey and compatible event family;
- each expected value/rule column is followed by its test status column;
- Screenshot Register and QA Cases are compact evidence registers;
- internal rationale stays in the structured plan, not as clutter in visible
  workbook tabs.
