"""Two generic consumers that ACTUALLY read selected world values.

CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY — finite-scenario consumer: eligible
scenario constraints and minority alternatives; never a parent object, partner
selection or biography.
NONPARENT_APPRENTICESHIP_ENTRY — nonparent consumer: possible apprenticeship /
education access routes and restrictions; never a generated learner psyche.

Both emit a values-read receipt naming every world VALUE they consumed.
"""
from __future__ import annotations

import copy
from typing import Any, Mapping

from port.contracts import PortContractError, semantic_digest
from port.world_baseline import CONSUMER_SPECS

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


def run_consumer(
    provider: Any,
    selection: Mapping[str, Any],
    possibility: Mapping[str, Any],
    consumer_id: str,
) -> dict[str, Any]:
    if consumer_id not in CONSUMER_SPECS:
        raise PortContractError("REJECT_ACTOR_FIREWALL", f"unknown consumer {consumer_id!r}")
    spec = CONSUMER_SPECS[consumer_id]
    values_receipt = provider.read_values(selection, list(spec["reads"]))
    world = selection["world"]

    if consumer_id == "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY":
        rule_public = values_receipt["values"]["fx:rule:public_access_2008"]
        rule_mutual = values_receipt["values"]["fx:rule:mutual_aid"]
        route_public = world["routes"]["fx:r:public"]
        route_mutual = world["routes"]["fx:r:mutual"]
        output = {
            "eligible_scenario_constraints": [
                {
                    "constraint_id": "SC_PUBLIC_ACCESS",
                    "derived_from_rule": rule_public["text"],
                    "rule_effective": rule_public["effective"],
                    "route": "fx:r:public",
                    "route_availability": route_public["availability"],
                    "route_values": copy.deepcopy(route_public["values"]),
                    "category_refs": list(route_public["category_refs"]),
                    "sanction_refs": list(route_public["sanction_refs"]),
                },
                {
                    "constraint_id": "SC_SPONSOR_REQUIRED",
                    "derived_from_rule": rule_mutual["text"],
                    "rule_effective": rule_mutual["effective"],
                    "route": "fx:r:mutual",
                    "route_availability": route_mutual["availability"],
                    "route_values": copy.deepcopy(route_mutual["values"]),
                    "category_refs": list(route_mutual["category_refs"]),
                    "sanction_refs": list(route_mutual["sanction_refs"]),
                },
            ],
            "horizon_bound": values_receipt["values"]["fx:AH"]["extent"],
        }
        minority_alternatives = copy.deepcopy(world["contradictory_alternatives"])
        restrictions = [
            "no parent object",
            "no partner selection",
            "no biography",
            "scenario constraints are objective world structure only",
        ]
    else:
        rule_public = values_receipt["values"]["fx:rule:public_access_2008"]
        rule_mutual = values_receipt["values"]["fx:rule:mutual_aid"]
        route_public = world["routes"]["fx:r:public"]
        route_mutual = world["routes"]["fx:r:mutual"]
        output = {
            "apprenticeship_access_routes": [
                {
                    "route": "fx:r:public",
                    "kind": route_public["kind"],
                    "availability": route_public["availability"],
                    "entry_values": copy.deepcopy(route_public["values"]),
                    "rule": rule_public["text"],
                },
                {
                    "route": "fx:r:mutual",
                    "kind": route_mutual["kind"],
                    "availability": route_mutual["availability"],
                    "entry_values": copy.deepcopy(route_mutual["values"]),
                    "rule": rule_mutual["text"],
                },
            ],
            "empirical_access_support": {
                "base_ratio": possibility["support"]["base_ratio"],
                "minority_ratio": possibility["support"]["minority_ratio"],
                "ordered_condition_chain": copy.deepcopy(possibility["ordered_condition_chain"]),
            },
        }
        minority_alternatives = [
            {"route": "fx:r:public", "state": "POSSIBLE"},
            {"route": "fx:r:mutual", "state": "POSSIBLE_WITH_SPONSOR"},
            {"route": "fx:r:public", "state": "CONTRADICTORY_SOURCE_SCOPE", "witness": "public rule B"},
        ]
        restrictions = [
            "no generated learner psyche",
            "no parent or coparent tag",
            "route access is objective structure, not actor uptake",
        ]

    effect = {
        "consumer_id": consumer_id,
        "output": output,
        "values_read": values_receipt,
        "minority_alternatives": minority_alternatives,
        "restrictions": restrictions,
        "person_generation": "NONE",
        "consumer_digest": semantic_digest(
            {"output": output, "values": values_receipt["digest"], "consumer_id": consumer_id}
        ),
    }
    # scan only the produced OUTPUT for affirmative forbidden content;
    # restriction strings are declarative prohibitions and are not claims
    leak = _scan_forbidden(repr(output))
    if leak:
        raise PortContractError(
            "REJECT_ACTOR_FIREWALL", f"consumer output contains forbidden content: {leak}"
        )
    return effect


def apply_consumers(
    provider: Any,
    selection: Mapping[str, Any],
    possibility: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    return {
        consumer_id: run_consumer(provider, selection, possibility, consumer_id)
        for consumer_id in sorted(CONSUMER_SPECS)
    }
