"""SC0F strict consumers — extends original consumers with values-read refs."""
from __future__ import annotations

import copy
from typing import Any, Mapping

from sc0f.strict_receipts import _ref


FORBIDDEN_OUTPUT_TOKENS = (
    "PARENT_OBJECT", "PARTNER_SELECTION", "BIOGRAPHY", "LEARNER_PSYCHE",
    "COPARENT", "ENNEAGRAM", "PERSONALITY", "ACTOR_STATE",
)


def _scan_forbidden(text: str) -> str | None:
    upper = text.upper()
    for token in FORBIDDEN_OUTPUT_TOKENS:
        if token in upper:
            return token
    return None


CONSUMER_SPECS: dict[str, dict[str, Any]] = {
    "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY": {
        "reads": [
            "fx:rule:public_access_2008",
            "fx:rule:mutual_aid",
            "fx:r:public",
            "fx:r:mutual",
            "fx:AH",
        ],
    },
    "NONPARENT_APPRENTICESHIP_ENTRY": {
        "reads": [
            "fx:rule:public_access_2008",
            "fx:rule:mutual_aid",
            "fx:r:public",
            "fx:r:mutual",
        ],
    },
}


def apply_consumers_strict(
    provider: Any,
    selection: Mapping[str, Any],
    possibility: Mapping[str, Any],
) -> dict[str, Any]:
    """Run both consumers and emit values-read refs for strict receipts."""
    effects: dict[str, Any] = {}
    for consumer_id, spec in sorted(CONSUMER_SPECS.items()):
        values_receipt = provider.read_values(selection, list(spec["reads"]))
        values = values_receipt["values"]
        world = selection["world"]

        values_read_refs = [
            _ref("VALUE_READ", f"{consumer_id}:{key}", values[key])
            for key in sorted(values)
        ]

        if consumer_id == "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY":
            rule_public = values.get("fx:rule:public_access_2008", {})
            rule_mutual = values.get("fx:rule:mutual_aid", {})
            route_public = world.get("routes", {}).get("fx:r:public", {})
            route_mutual = world.get("routes", {}).get("fx:r:mutual", {})
            output = {
                "eligible_scenario_constraints": [
                    {
                        "constraint_id": "SC_PUBLIC_ACCESS",
                        "derived_from_rule": rule_public.get("text", ""),
                        "rule_effective": rule_public.get("effective", ""),
                        "route": "fx:r:public",
                        "route_availability": route_public.get("availability", ""),
                        "route_values": copy.deepcopy(route_public.get("values", {})),
                    },
                    {
                        "constraint_id": "SC_MUTUAL_AID",
                        "derived_from_rule": rule_mutual.get("text", ""),
                        "rule_effective": rule_mutual.get("effective", ""),
                        "route": "fx:r:mutual",
                        "route_availability": route_mutual.get("availability", ""),
                        "route_values": copy.deepcopy(route_mutual.get("values", {})),
                    },
                ],
                "minority_alternatives": possibility.get("minority", ""),
                "empirical_support": possibility.get("support", {}),
            }
        else:
            rule_public = values.get("fx:rule:public_access_2008", {})
            route_public = world.get("routes", {}).get("fx:r:public", {})
            output = {
                "apprenticeship_routes": [
                    {
                        "route": "fx:r:public",
                        "availability": route_public.get("availability", ""),
                        "values": copy.deepcopy(route_public.get("values", {})),
                        "rule": rule_public.get("text", ""),
                    },
                ],
                "empirical_support": possibility.get("support", {}),
            }

        scan = _scan_forbidden(str(output))
        if scan:
            raise Exception(f"REJECT_ACTOR_FIREWALL: forbidden token {scan!r} in {consumer_id}")

        effects[consumer_id] = {
            "consumer_id": consumer_id,
            "output": output,
            "values_read": {k: copy.deepcopy(v) for k, v in values.items()},
            "values_read_refs": values_read_refs,
            "consumer_digest": _ref("CONSUMER_EFFECT", consumer_id, output),
        }
    return effects
