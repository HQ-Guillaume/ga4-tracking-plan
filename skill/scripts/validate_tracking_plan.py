from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from ecommerce_matrix import EVENT_PARAMETERS_BY_EVENT, OFFICIAL_ITEM_PARAMETERS


ECOMMERCE_EVENTS = {
    "add_payment_info",
    "add_shipping_info",
    "add_to_cart",
    "add_to_wishlist",
    "begin_checkout",
    "purchase",
    "refund",
    "remove_from_cart",
    "select_item",
    "select_promotion",
    "view_cart",
    "view_item",
    "view_item_list",
    "view_promotion",
}

TRANSACTION_EVENTS = {"purchase", "refund"}
VALUE_EVENTS_REQUIRE_CURRENCY = ECOMMERCE_EVENTS | {
    "generate_lead",
    "qualify_lead",
    "disqualify_lead",
    "working_lead",
    "close_convert_lead",
    "close_unconvert_lead",
}

LEGACY_WRAPPER_EVENT_KEYS = {"gtm.custom_event", "custom_event"}
LEGACY_WRAPPER_PARAMETERS = {"event_name", "action", "label"}
AUTOMATIC_EVENTS = {"page_view", "first_visit", "session_start", "user_engagement"}
OFFICIAL_ECOMMERCE_PARAMETER_CLASSES = {"ga4_ecommerce_parameter", "ga4_ecommerce_item_parameter"}

PII_NAME_RE = re.compile(
    r"(^|_)(email|e_mail|mail|hashed_email|sha256_email|phone|telephone|tel|mobile|"
    r"first_name|last_name|full_name|address|postal|zip_code|zipcode|customer_id|"
    r"user_id|client_id|account_id|message|comment|free_text|question_text)($|_)",
    re.IGNORECASE,
)

SAFE_NAME_EXCEPTIONS = {
    "item_name",
    "item_list_name",
    "promotion_name",
    "creative_name",
    "page_title",
    "page_location",
    "page_referrer",
    "form_name",
    "method",
    "video_title",
    "search_term",
    "content_name",
    "file_name",
    "link_text",
    "link_url",
}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and lint a GA4 tracking-plan JSON file.")
    parser.add_argument("plan", type=Path, help="Path to the tracking-plan JSON file.")
    parser.add_argument("--schema", type=Path, default=None, help="Optional JSON schema path. Defaults to references/tracking_plan_schema.json.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    parser.add_argument("--warnings-as-errors", action="store_true", help="Exit non-zero when warnings are present.")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def default_schema_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "tracking_plan_schema.json"


def add_issue(issues: list[Issue], severity: str, code: str, path: str, message: str) -> None:
    issues.append(Issue(severity=severity, code=code, path=path, message=message))


def validate_schema(plan: dict[str, Any], schema_path: Path, issues: list[Issue]) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        add_issue(
            issues,
            "warning",
            "SCHEMA_VALIDATOR_MISSING",
            "dependencies",
            "Install requirements.txt to enable JSON Schema validation.",
        )
        return

    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(plan), key=lambda item: list(item.path)):
        path = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.path)
        add_issue(issues, "error", "SCHEMA_VALIDATION", path, error.message)


def values_at_keys(value: Any, target_keys: set[str], prefix: str = "$") -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}"
            if key in target_keys:
                yield path, child
            yield from values_at_keys(child, target_keys, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from values_at_keys(child, target_keys, f"{prefix}[{index}]")


def walk_keys(value: Any, prefix: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}"
            yield path, key
            yield from walk_keys(child, path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_keys(child, f"{prefix}[{index}]")


def check_duplicates(values: list[str], label: str, path: str, issues: list[Issue]) -> None:
    for value, count in Counter(values).items():
        if value and count > 1:
            add_issue(issues, "error", "DUPLICATE_ID", path, f"{label} '{value}' appears {count} times.")


def check_pii_name(name: str, path: str, issues: list[Issue]) -> None:
    if name in SAFE_NAME_EXCEPTIONS:
        return
    if PII_NAME_RE.search(name):
        add_issue(issues, "error", "PII_FIELD_NAME", path, f"Field '{name}' looks like direct or contact-derived PII.")


def check_event(event: dict[str, Any], index: int, parameter_lookup: dict[str, dict[str, Any]], issues: list[Issue]) -> None:
    base = f"$.events[{index}]"
    event_name = event.get("event_name", "")
    classification = event.get("classification", "")
    parameters = event.get("parameters", [])
    parameter_names = set(parameter_lookup)
    data_layer = event.get("data_layer", {})
    ga4_payload = event.get("ga4_payload", {})
    privacy = event.get("privacy", {})

    for parameter in parameters:
        check_pii_name(str(parameter), f"{base}.parameters", issues)
        if parameter in LEGACY_WRAPPER_PARAMETERS:
            add_issue(
                issues,
                "warning",
                "LEGACY_WRAPPER_PARAMETER",
                f"{base}.parameters",
                f"Parameter '{parameter}' is a legacy wrapper pattern. Prefer direct GA4 event parameters.",
            )
        if parameter.startswith("items[].") and parameter not in OFFICIAL_ITEM_PARAMETERS and parameter not in parameter_names:
            add_issue(issues, "warning", "CUSTOM_ITEM_PARAMETER_NOT_DEFINED", f"{base}.parameters", f"Custom item parameter '{parameter}' must be defined in the parameter reference.")
        elif parameter not in parameter_names and not parameter.startswith("items[]."):
            add_issue(issues, "warning", "PARAMETER_NOT_DEFINED", f"{base}.parameters", f"Parameter '{parameter}' is not in the parameter reference.")

    event_key = data_layer.get("event_key")
    if event_name in LEGACY_WRAPPER_EVENT_KEYS or event_key in LEGACY_WRAPPER_EVENT_KEYS:
        add_issue(
            issues,
            "error",
            "LEGACY_WRAPPER_EVENT",
            f"{base}.data_layer.event_key",
            "Use the GA4 event name directly instead of a wrapper event such as gtm.custom_event.",
        )

    push = data_layer.get("push", {})
    if isinstance(push, dict):
        pushed_event = push.get("event")
        if pushed_event in LEGACY_WRAPPER_EVENT_KEYS:
            add_issue(
                issues,
                "error",
                "LEGACY_WRAPPER_PUSH",
                f"{base}.data_layer.push.event",
                "dataLayer push uses a wrapper event. Push the final GA4 event name directly.",
            )
        for path, key in walk_keys(push, f"{base}.data_layer.push"):
            check_pii_name(key, path, issues)

    payload_name = ga4_payload.get("event_name")
    if payload_name and payload_name != event_name:
        add_issue(issues, "error", "PAYLOAD_EVENT_MISMATCH", f"{base}.ga4_payload.event_name", f"Payload event '{payload_name}' does not match event_name '{event_name}'.")

    payload_parameters = ga4_payload.get("parameters", {}) if isinstance(ga4_payload.get("parameters"), dict) else {}
    for name in payload_parameters:
        check_pii_name(name, f"{base}.ga4_payload.parameters.{name}", issues)

    if event_name in ECOMMERCE_EVENTS and classification != "recommended_ecommerce":
        add_issue(issues, "warning", "ECOMMERCE_CLASSIFICATION", f"{base}.classification", f"Official ecommerce event '{event_name}' should usually be classified as recommended_ecommerce.")
    if classification == "recommended_ecommerce" and event_name not in ECOMMERCE_EVENTS:
        add_issue(issues, "error", "INVALID_ECOMMERCE_EVENT", f"{base}.event_name", f"'{event_name}' is not an official GA4 ecommerce event.")

    if classification == "recommended_ecommerce":
        official_event_parameters = EVENT_PARAMETERS_BY_EVENT.get(event_name, set())
        for name in payload_parameters:
            metadata = parameter_lookup.get(name)
            if name not in official_event_parameters:
                if metadata is None:
                    add_issue(issues, "warning", "CUSTOM_ECOMMERCE_PARAMETER_NOT_DEFINED", f"{base}.ga4_payload.parameters.{name}", f"Custom ecommerce event parameter '{name}' must be defined in the parameter reference.")
                elif metadata.get("classification") in OFFICIAL_ECOMMERCE_PARAMETER_CLASSES:
                    add_issue(issues, "error", "CUSTOM_ECOMMERCE_PARAMETER_MISCLASSIFIED", f"{base}.ga4_payload.parameters.{name}", f"'{name}' is not an official parameter for {event_name}; classify it as custom_event_parameter or remove it.")
        items = ga4_payload.get("items", [])
        if not isinstance(items, list) or not items:
            add_issue(issues, "error", "ECOMMERCE_ITEMS_MISSING", f"{base}.ga4_payload.items", "Ecommerce events need an items array when product/item data is available.")
        for item_index, item in enumerate(items if isinstance(items, list) else []):
            if not isinstance(item, dict):
                continue
            if "item_id" not in item and "item_name" not in item:
                add_issue(issues, "error", "ECOMMERCE_ITEM_ID_OR_NAME", f"{base}.ga4_payload.items[{item_index}]", "Each ecommerce item needs item_id or item_name.")
            if "currency" in item:
                add_issue(issues, "error", "ITEM_SCOPE_CURRENCY", f"{base}.ga4_payload.items[{item_index}].currency", "currency is event-scoped, not item-scoped.")
            for key in item:
                parameter_name = f"items[].{key}"
                metadata = parameter_lookup.get(parameter_name)
                if parameter_name in OFFICIAL_ITEM_PARAMETERS:
                    continue
                if metadata is None:
                    add_issue(issues, "warning", "CUSTOM_ITEM_PARAMETER_NOT_DEFINED", f"{base}.ga4_payload.items[{item_index}].{key}", f"Custom item parameter '{parameter_name}' must be defined in the parameter reference.")
                elif metadata.get("classification") in OFFICIAL_ECOMMERCE_PARAMETER_CLASSES:
                    add_issue(issues, "error", "CUSTOM_ITEM_PARAMETER_MISCLASSIFIED", f"{base}.ga4_payload.items[{item_index}].{key}", f"'{parameter_name}' is not an official GA4 item parameter; classify it as custom_item_parameter or remove it.")
        flush_keys = set(data_layer.get("flush_keys", []))
        if "ecommerce" not in flush_keys:
            add_issue(issues, "warning", "ECOMMERCE_FLUSH_MISSING", f"{base}.data_layer.flush_keys", "Flush ecommerce before ecommerce pushes to prevent stale item data.")

    if event_name in TRANSACTION_EVENTS and "transaction_id" not in payload_parameters:
        add_issue(issues, "error", "TRANSACTION_ID_MISSING", f"{base}.ga4_payload.parameters", f"{event_name} needs transaction_id for deduplication.")
    if event_name in VALUE_EVENTS_REQUIRE_CURRENCY and "value" in payload_parameters and "currency" not in payload_parameters:
        add_issue(issues, "error", "CURRENCY_MISSING", f"{base}.ga4_payload.parameters", "currency is required when value is sent.")

    if privacy.get("pii_risk") == "high":
        add_issue(issues, "error", "HIGH_PII_RISK", f"{base}.privacy.pii_risk", "High PII risk must be resolved before plan approval.")
    if privacy.get("cardinality_risk") == "high":
        add_issue(issues, "warning", "HIGH_CARDINALITY_RISK", f"{base}.privacy.cardinality_risk", "High-cardinality fields should not be registered as reporting dimensions unless justified.")

    qa = event.get("qa", {})
    if not qa.get("qa_id"):
        add_issue(issues, "error", "EVENT_QA_MISSING", f"{base}.qa.qa_id", "Every testable event needs a stable qa_id.")
    if not qa.get("expected_data_layer"):
        add_issue(issues, "warning", "EXPECTED_DATALAYER_MISSING", f"{base}.qa.expected_data_layer", "QA should include expected dataLayer keys or note why none apply.")
    if not qa.get("expected_network"):
        add_issue(issues, "warning", "EXPECTED_NETWORK_MISSING", f"{base}.qa.expected_network", "QA should include expected GA4/network event and key parameters.")


def validate_plan_data(plan: dict[str, Any], schema_path: Path | None = None) -> list[Issue]:
    issues: list[Issue] = []
    schema_path = schema_path or default_schema_path()
    validate_schema(plan, schema_path, issues)

    parameters = plan.get("parameters", [])
    parameter_lookup = {param.get("parameter_name", ""): param for param in parameters if isinstance(param, dict)}
    events = plan.get("events", [])
    qa_cases = plan.get("qa_cases", [])
    custom_definitions = plan.get("custom_definitions", [])
    registered_item_custom_dimensions = {
        definition.get("parameter_name")
        for definition in custom_definitions
        if isinstance(definition, dict)
        and definition.get("scope") == "item"
        and definition.get("registration_type") == "custom_dimension"
    }

    check_duplicates([event.get("event_id", "") for event in events if isinstance(event, dict)], "event_id", "$.events", issues)
    check_duplicates([case.get("qa_id", "") for case in qa_cases if isinstance(case, dict)], "qa_id", "$.qa_cases", issues)

    for index, param in enumerate(parameters):
        if not isinstance(param, dict):
            continue
        name = str(param.get("parameter_name", ""))
        check_pii_name(name, f"$.parameters[{index}].parameter_name", issues)
        classification = param.get("classification")
        if name.startswith("items[]."):
            if name in OFFICIAL_ITEM_PARAMETERS:
                if classification == "custom_item_parameter":
                    add_issue(issues, "warning", "OFFICIAL_ITEM_PARAMETER_MISCLASSIFIED", f"$.parameters[{index}].classification", f"'{name}' is an official GA4 item parameter; classify it as ga4_ecommerce_item_parameter.")
            else:
                if classification in OFFICIAL_ECOMMERCE_PARAMETER_CLASSES:
                    add_issue(issues, "error", "CUSTOM_ITEM_PARAMETER_MISCLASSIFIED", f"$.parameters[{index}].classification", f"'{name}' is not an official GA4 item parameter; classify it as custom_item_parameter.")
                elif classification != "custom_item_parameter":
                    add_issue(issues, "warning", "CUSTOM_ITEM_PARAMETER_CLASSIFICATION", f"$.parameters[{index}].classification", f"'{name}' is item-scoped and non-official; use custom_item_parameter.")
                if param.get("scope") != "item":
                    add_issue(issues, "error", "CUSTOM_ITEM_PARAMETER_SCOPE", f"$.parameters[{index}].scope", f"'{name}' must use item scope.")
                if param.get("register_custom_definition") and name not in registered_item_custom_dimensions:
                    add_issue(issues, "warning", "CUSTOM_ITEM_DIMENSION_MISSING", "$.custom_definitions", f"'{name}' is marked for registration but no matching item-scoped custom dimension is listed.")
        if param.get("pii_risk") == "high":
            add_issue(issues, "error", "HIGH_PII_RISK", f"$.parameters[{index}].pii_risk", f"Parameter '{name}' has high PII risk.")
        if param.get("cardinality_risk") == "high" and param.get("register_custom_definition"):
            add_issue(issues, "warning", "HIGH_CARDINALITY_CUSTOM_DIMENSION", f"$.parameters[{index}]", f"Parameter '{name}' is high-cardinality and marked for custom definition registration.")

    for index, event in enumerate(events):
        if isinstance(event, dict):
            check_event(event, index, parameter_lookup, issues)

    events_by_id = {event.get("event_id"): event for event in events if isinstance(event, dict)}
    event_qa_ids = {event.get("qa", {}).get("qa_id") for event in events if isinstance(event, dict)}
    qa_case_ids = {case.get("qa_id") for case in qa_cases if isinstance(case, dict)}
    for event_id, event in events_by_id.items():
        if event and event.get("qa", {}).get("qa_id") not in qa_case_ids:
            add_issue(issues, "warning", "QA_CASE_MISSING", "$.qa_cases", f"Event '{event_id}' has no matching qa_cases entry.")
    for index, case in enumerate(qa_cases):
        if not isinstance(case, dict):
            continue
        event_id = case.get("event_id")
        event = events_by_id.get(event_id)
        if not event:
            add_issue(issues, "error", "QA_EVENT_NOT_FOUND", f"$.qa_cases[{index}].event_id", f"QA case references unknown event_id '{event_id}'.")
            continue
        if case.get("event_name") != event.get("event_name"):
            add_issue(issues, "error", "QA_EVENT_NAME_MISMATCH", f"$.qa_cases[{index}].event_name", "QA case event_name does not match the referenced event.")
        if case.get("qa_id") not in event_qa_ids:
            add_issue(issues, "warning", "QA_ID_NOT_ON_EVENT", f"$.qa_cases[{index}].qa_id", "QA case qa_id is not referenced by an event qa block.")

    return issues


def render_text(issues: list[Issue]) -> str:
    if not issues:
        return "Tracking plan validation passed with no issues."
    lines = []
    for issue in issues:
        lines.append(f"{issue.severity.upper()} {issue.code} {issue.path}: {issue.message}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    plan = load_json(args.plan)
    issues = validate_plan_data(plan, args.schema or default_schema_path())
    if args.format == "json":
        print(json.dumps([issue.__dict__ for issue in issues], indent=2, ensure_ascii=False))
    else:
        print(render_text(issues))
    has_error = any(issue.severity == "error" for issue in issues)
    has_warning = any(issue.severity == "warning" for issue in issues)
    return 1 if has_error or (args.warnings_as_errors and has_warning) else 0


if __name__ == "__main__":
    sys.exit(main())
