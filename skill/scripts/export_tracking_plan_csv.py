from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from ecommerce_matrix import (
    event_family,
    OFFICIAL_EVENT_PARAMETERS,
    OFFICIAL_ITEM_PARAMETERS,
    ordered_parameters_for_events,
    parameter_availability,
    parameter_matrix_value,
    parameter_scope,
    parameter_type,
    scope_rule,
)


FIELDS = [
    "block",
    "journey_id",
    "journey_name",
    "event_id",
    "qa_id",
    "event_name",
    "classification",
    "official_ga4_match",
    "business_question",
    "trigger",
    "key_event",
    "priority",
    "parameter_name",
    "parameter_scope",
    "parameter_type",
    "requirement",
    "classification_or_source",
    "expected_value",
    "availability",
    "scope_rule",
    "implementation_notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a GA4 tracking-plan JSON contract to a readable long-format CSV.")
    parser.add_argument("plan", type=Path, help="Path to the canonical tracking-plan JSON file.")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output CSV path.")
    return parser.parse_args()


def load_plan(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parameter_lookup(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {param["parameter_name"]: param for param in plan.get("parameters", []) if isinstance(param, dict)}


def requirement_for(event: dict[str, Any], parameter: str, metadata: dict[str, Any] | None) -> str:
    event_name = str(event.get("event_name", ""))
    if metadata and metadata.get("required"):
        return str(metadata["required"])
    if parameter == "items":
        return "required"
    if parameter in {"items[].item_id", "items[].item_name"}:
        return "one_of_required"
    if parameter == "transaction_id" and event_name in {"purchase", "refund"}:
        return "required"
    if parameter == "currency" and "value" in event.get("ga4_payload", {}).get("parameters", {}):
        return "conditional"
    if parameter == "items[].quantity":
        return "optional_default_1"
    return "optional"


def parameter_source(parameter: str, metadata: dict[str, Any] | None) -> str:
    if metadata:
        classification = str(metadata.get("classification") or metadata.get("source") or "")
        if parameter.startswith("items[].") and parameter not in OFFICIAL_ITEM_PARAMETERS and classification in {"ga4_ecommerce_parameter", "ga4_ecommerce_item_parameter"}:
            return "custom_item_parameter (metadata misclassified)"
        if not parameter.startswith("items[].") and parameter not in OFFICIAL_EVENT_PARAMETERS and classification == "ga4_ecommerce_parameter":
            return "custom_event_parameter (metadata misclassified)"
        return classification
    if parameter.startswith("items[]."):
        return "ga4_ecommerce_item_parameter" if parameter in OFFICIAL_ITEM_PARAMETERS else "custom_item_parameter"
    if parameter in OFFICIAL_EVENT_PARAMETERS:
        return "ga4_ecommerce_parameter"
    return "official_ga4_event_parameter"


def export_rows(plan: dict[str, Any]) -> list[dict[str, Any]]:
    params = parameter_lookup(plan)
    journeys = {brief["journey_id"]: brief["journey_name"] for brief in plan.get("measurement_brief", [])}
    rows: list[dict[str, Any]] = []

    for event in plan.get("events", []):
        block = event_family(event)
        for parameter in ordered_parameters_for_events([event]):
            metadata = params.get(parameter)
            rows.append(
                {
                    "block": block,
                    "journey_id": event.get("journey_id", ""),
                    "journey_name": journeys.get(event.get("journey_id", ""), event.get("journey_id", "")),
                    "event_id": event.get("event_id", ""),
                    "qa_id": event.get("qa", {}).get("qa_id", ""),
                    "event_name": event.get("event_name", ""),
                    "classification": event.get("classification", ""),
                    "official_ga4_match": event.get("official_ga4_match", ""),
                    "business_question": event.get("business_question", ""),
                    "trigger": event.get("trigger", ""),
                    "key_event": str(event.get("key_event", "")).lower(),
                    "priority": event.get("priority", ""),
                    "parameter_name": parameter,
                    "parameter_scope": metadata.get("scope") if metadata else parameter_scope(parameter),
                    "parameter_type": metadata.get("type") if metadata else parameter_type(parameter),
                    "requirement": requirement_for(event, parameter, metadata),
                    "classification_or_source": parameter_source(parameter, metadata),
                    "expected_value": parameter_matrix_value(event, parameter),
                    "availability": parameter_availability(event, parameter),
                    "scope_rule": scope_rule(parameter),
                    "implementation_notes": event.get("implementation_notes", ""),
                }
            )
    return rows


def main() -> int:
    args = parse_args()
    plan = load_plan(args.plan)
    rows = export_rows(plan)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
