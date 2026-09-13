#!/usr/bin/env python3
"""Independent E06 qualification probes for the exact D06 M3 R2 implementation.

This file is evidence-only. It imports the frozen D06 fixture helpers without
modifying production code, then exercises additional alias, schema-shape,
authority-binding, and identity-mutation cases.
"""
from __future__ import annotations

import copy
import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[11]
FIXTURE = ROOT / "rawlsing_next/tests/test_m3_v556_higher_order_structural.py"
ns = runpy.run_path(str(FIXTURE))

M3_CONTRACT_ID = ns["M3_CONTRACT_ID"]
M3DecisionState = ns["M3DecisionState"]
semantic_hash = ns["semantic_hash"]
_m2 = ns["_m2"]
_rule = ns["_rule"]
_request = ns["_request"]
_bind = ns["_bind"]
_eval = ns["_eval"]
_ref = ns["_ref"]
_string = ns["_string"]
_object = ns["_object"]
_array = ns["_array"]
_schema_structural = ns["_schema_structural"]
_schema_actor_position = ns["_schema_actor_position"]
_schema_actor_opportunity = ns["_schema_actor_opportunity"]


def require(label: str, condition: bool, detail: str, rows: list[dict[str, str]]) -> None:
    if not condition:
        raise AssertionError(f"{label}: {detail}")
    rows.append({"case": label, "result": "PASS", "detail": detail})


def pair():
    return _m2("e06-a"), _m2("e06-b")


def eval_payload(rule, payload):
    a, b = pair()
    return _eval(
        [a, b],
        _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=payload),
    )


def body_hash_material(rule, binding_ref):
    return {
        "contract_id": M3_CONTRACT_ID,
        "rule_id": rule["rule_id"],
        "rule_version": rule["rule_version"],
        "semantic_family": rule["semantic_family"],
        "participant_roles": list(rule["participant_roles"]),
        "participant_order_policy": rule["participant_order_policy"],
        "minimum_cardinality": rule["minimum_cardinality"],
        "maximum_cardinality_or_unbounded_marker": rule["maximum_cardinality_or_unbounded_marker"],
        "multiplicity_policy": rule["multiplicity_policy"],
        "same_route_reuse_policy": rule["same_route_reuse_policy"],
        "source_composition_policy": rule["source_composition_policy"],
        "allowed_typed_outcome_states": sorted(set(rule["allowed_typed_outcome_states"])),
        "producer_allowed_uses": sorted(set(rule["producer_allowed_uses"])),
        "result_contract_binding_ref": binding_ref,
    }


def rebind_same_rule(rule, binding):
    material = {
        "contract_id": M3_CONTRACT_ID,
        **{k: v for k, v in binding.items() if k != "binding_content_hash"},
    }
    binding["binding_content_hash"] = semantic_hash(material)
    binding_ref = {
        "kind": rule["result_contract_binding_ref"]["kind"],
        "object_id": f"{binding['binding_id']}@{binding['binding_version']}",
        "content_hash": binding["binding_content_hash"],
    }
    rule["result_contract_binding_ref"] = binding_ref
    rule["rule_content_hash"] = semantic_hash(body_hash_material(rule, binding_ref))
    rule.result_contract = binding
    rule.result_contract_ref = binding_ref
    return rule


def main() -> None:
    rows: list[dict[str, str]] = []

    # A01: flat undeclared person-state alias cannot enter a closed structural schema.
    rule = _rule(tag="e06-a01")
    x = eval_payload(rule, {"relation_kind": "TEST_HIGHER_ORDER", "temperament_code": "T4"})
    require(
        "E06-A01-flat-alias",
        x.decision_state is M3DecisionState.RESULT_SCHEMA_NONCONFORMING and x.v556_object is None,
        "undeclared temperament alias rejected by exact closed schema",
        rows,
    )

    # A02: nested object alias cannot hide under an otherwise objective grouping.
    nested = _object(
        {"status": _string("OBJECTIVE_STATUS", ["OPEN", "CLOSED"])},
        ("status",),
    )
    schema = _schema_structural(
        extra_fields={"facts": nested},
        required_extra=("facts",),
        schema_id="E06_NESTED_FACTS",
    )
    rule = _rule(schema=schema, tag="e06-a02")
    payload = {"relation_kind": "TEST_HIGHER_ORDER", "facts": {"status": "OPEN", "motive_code": "approval"}}
    x = eval_payload(rule, payload)
    require(
        "E06-A02-nested-alias",
        x.decision_state is M3DecisionState.RESULT_SCHEMA_NONCONFORMING and x.v556_object is None,
        "nested undeclared motive alias rejected recursively",
        rows,
    )

    # A03: aliases inside array items are also recursively rejected.
    item = _object(
        {
            "actor_ref": _string("OBJECTIVE_ACTOR_INDEX"),
            "status": _string("OBJECTIVE_STATUS", ["OPEN", "CLOSED"]),
        },
        ("actor_ref", "status"),
    )
    schema = _schema_structural(
        extra_fields={"entries": _array(item, minimum=1)},
        required_extra=("entries",),
        schema_id="E06_ARRAY_FACTS",
    )
    rule = _rule(schema=schema, actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="e06-a03")
    payload = {
        "relation_kind": "TEST_HIGHER_ORDER",
        "entries": [{"actor_ref": "urn:e06:actor:1", "status": "OPEN", "belief_vector": "x"}],
    }
    x = eval_payload(rule, payload)
    require(
        "E06-A03-array-alias",
        x.decision_state is M3DecisionState.RESULT_SCHEMA_NONCONFORMING and x.v556_object is None,
        "array-item belief alias rejected recursively",
        rows,
    )

    # S01: a schema cannot legalize person-state by hiding a forbidden semantic role under a neutral field name.
    schema = _schema_structural(
        extra_fields={"signal": _string("MOTIVATION")},
        required_extra=("signal",),
        schema_id="E06_FORBIDDEN_ROLE",
    )
    rule = _rule(schema=schema, tag="e06-s01")
    x = eval_payload(rule, {"relation_kind": "TEST_HIGHER_ORDER", "signal": "approval"})
    require(
        "E06-S01-forbidden-role",
        x.decision_state is M3DecisionState.INTEGRITY_FAILURE and x.v556_object is None,
        "forbidden person-state semantic role invalidates exact result contract",
        rows,
    )

    # S02: open/additional-field result schemas are invalid authority, not permissive fallback.
    schema = _schema_structural(schema_id="E06_OPEN_SCHEMA")
    schema["root"]["additional_fields"] = True
    rule = _rule(schema=schema, tag="e06-s02")
    x = eval_payload(rule, {"relation_kind": "TEST_HIGHER_ORDER"})
    require(
        "E06-S02-open-schema",
        x.decision_state is M3DecisionState.INTEGRITY_FAILURE and x.v556_object is None,
        "additional_fields=true rejected as schema-integrity failure",
        rows,
    )

    # S03/S04: actor indexing is explicit and structurally checked both directions.
    rule = _rule(schema=_schema_actor_position(), actor_mode="NO_ACTOR_INDEX", tag="e06-s03")
    x = eval_payload(
        rule,
        {"actor_ref": "urn:e06:actor:1", "institution_ref": "urn:e06:inst:1", "position_kind": "EMPLOYEE_OF"},
    )
    require(
        "E06-S03-no-index-with-actor-schema",
        x.decision_state is M3DecisionState.INTEGRITY_FAILURE and x.v556_object is None,
        "NO_ACTOR_INDEX cannot bind schema containing objective actor index",
        rows,
    )
    rule = _rule(schema=_schema_structural(schema_id="E06_NO_ACTOR"), actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="e06-s04")
    x = eval_payload(rule, {"relation_kind": "TEST_HIGHER_ORDER"})
    require(
        "E06-S04-indexed-without-actor-schema",
        x.decision_state is M3DecisionState.INTEGRITY_FAILURE and x.v556_object is None,
        "OBJECTIVE_ACTOR_INDEXED requires objective actor-index role in schema",
        rows,
    )

    # O01: semantic-owner current-selection mutation without re-binding is detected.
    a, b = pair()
    rule = _rule(tag="e06-o01")
    binding = copy.deepcopy(rule.result_contract)
    binding["result_semantic_owner_current_selection_ref"] = _ref(
        "M3_RESULT_OWNER_CURRENT_SELECTION", "owner-current:e06-mutated"
    )
    req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], result_contract=binding)
    x = _eval([a, b], req)
    require(
        "E06-O01-owner-current-mutation-stale-binding",
        x.decision_state is M3DecisionState.INTEGRITY_FAILURE and x.v556_object is None,
        "owner-current-selection mutation breaks binding hash",
        rows,
    )

    # O02: even after rehashing the binding, the active rule's old exact binding ref blocks substitution.
    binding = copy.deepcopy(rule.result_contract)
    binding["result_semantic_owner_ref"] = _ref("M3_RESULT_SEMANTIC_OWNER", "owner:e06-substitute")
    material = {
        "contract_id": M3_CONTRACT_ID,
        **{k: v for k, v in binding.items() if k != "binding_content_hash"},
    }
    binding["binding_content_hash"] = semantic_hash(material)
    req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], result_contract=binding)
    x = _eval([a, b], req)
    require(
        "E06-O02-owner-substitution-rule-ref",
        x.decision_state is M3DecisionState.INTEGRITY_FAILURE and x.v556_object is None,
        "rehashed owner substitution still conflicts with rule's exact binding ref",
        rows,
    )

    # I01: coherent owner mutation with binding+rule re-derived is a new valid identity, never the old identity.
    a, b = pair()
    base_rule = _rule(tag="e06-i01")
    base_req = _request(base_rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)])
    base = _eval([a, b], base_req)
    mutated_rule = copy.deepcopy(base_rule)
    mutated_binding = copy.deepcopy(base_rule.result_contract)
    mutated_binding["result_semantic_owner_ref"] = _ref("M3_RESULT_SEMANTIC_OWNER", "owner:e06-coherent-mutant")
    mutated_rule = rebind_same_rule(mutated_rule, mutated_binding)
    mutated_req = _request(
        mutated_rule,
        [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)],
        result_contract=mutated_rule.result_contract,
    )
    mutated = _eval([a, b], mutated_req)
    require(
        "E06-I01-owner-mutation-new-identity",
        base.decision_state is M3DecisionState.SUPPORTED
        and mutated.decision_state is M3DecisionState.SUPPORTED
        and base.replay_key_hash != mutated.replay_key_hash
        and base.v556_object["object_id"] != mutated.v556_object["object_id"]
        and base_rule["rule_content_hash"] != mutated_rule["rule_content_hash"],
        "coherent semantic-owner mutation changes rule/replay/object identity",
        rows,
    )

    # I02: lawful objective actor-indexed position remains positive.
    rule = _rule(schema=_schema_actor_position(), actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="e06-i02")
    x = eval_payload(
        rule,
        {"actor_ref": "urn:e06:actor:9", "institution_ref": "urn:e06:institution:4", "position_kind": "EMPLOYEE_OF"},
    )
    require(
        "E06-I02-lawful-objective-position",
        x.decision_state is M3DecisionState.SUPPORTED
        and x.v556_object["actor_indexing_mode"] == "OBJECTIVE_ACTOR_INDEXED"
        and x.v556_object["person_state_absent"] is True,
        "lawful objective actor-indexed position remains representable",
        rows,
    )

    # I03: opportunity availability is positive; actor uptake alias is not.
    rule = _rule(schema=_schema_actor_opportunity(), actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="e06-i03")
    good = {
        "actor_ref": "urn:e06:actor:9",
        "opportunity_ref": "urn:e06:opportunity:2",
        "availability_state": "AVAILABLE",
    }
    ok = eval_payload(rule, good)
    bad = dict(good)
    bad["acceptance_state"] = "ACCEPTED"
    rejected = eval_payload(rule, bad)
    require(
        "E06-I03-opportunity-vs-uptake-alias",
        ok.decision_state is M3DecisionState.SUPPORTED
        and rejected.decision_state is M3DecisionState.RESULT_SCHEMA_NONCONFORMING
        and rejected.v556_object is None,
        "objective opportunity passes while undeclared uptake/acceptance alias fails closed",
        rows,
    )

    # F01: fuzzy/default result-binding version selection is forbidden.
    a, b = pair()
    rule = _rule(tag="e06-f01")
    binding = copy.deepcopy(rule.result_contract)
    binding["binding_version"] = "default"
    req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], result_contract=binding)
    x = _eval([a, b], req)
    require(
        "E06-F01-fuzzy-binding-version",
        x.decision_state is M3DecisionState.INTEGRITY_FAILURE and x.v556_object is None,
        "mutable/default binding selection is rejected",
        rows,
    )

    print(json.dumps({"e06_independent_qualification": rows, "count": len(rows)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
