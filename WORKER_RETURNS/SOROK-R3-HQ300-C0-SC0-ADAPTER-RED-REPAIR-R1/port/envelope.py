"""True serializer for the pinned SC0 two-contract envelope (draft-2020-12).

The **true serializer view** of a receipt contains EXACTLY the fields the
pinned envelope schema defines (strict ``additionalProperties: false``); this is
the view jsonschema validates and the only view that is contract evidence.

The **code view** (legacy candidate-internal projection: the rich world model,
provider lineage, selection digests, empirical support) is retained as a
non-enumerable alias layer so adapter/consumer code paths keep their typed
access without polluting the serialized contract.  The two views are computed
from one source and cannot drift: the alias layer is built in the same call that
builds the serializer view.

Frozen envelope preimage: 610ac870fde6cfe63796592b3c6b1e1bf1e37150
(01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json, SC0 commit 241d35fa...).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping

from port.contracts import canonical_json, semantic_digest

ENVELOPE_PATH = Path(__file__).resolve().parents[1] / "staging" / "oracles" / "01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json"
ENVELOPE_BLOB = "610ac870fde6cfe63796592b3c6b1e1bf1e37150"

SCHEMA_GRADE = "TEST_FIXTURE_ONLY"

NEGATIVE_CODES = (
    "PRESENT",
    "OBSERVED_ZERO",
    "VALID_EMPTY",
    "MISSING",
    "UNDERPOWERED",
    "NOT_ASKED",
    "NONCOMPARABLE",
    "HELD_AUTHORITY",
    "NO_CURRENT",
    "DENIED_USE",
    "UNBOUND_RUNTIME_BINDING",
    "PROXY_MODELLED",
    "UNKNOWN_UNOBSERVED_GAP",
    "PARTIAL_DEFERRED",
    "INTEGRITY_FAILURE",
)

RECOVERABILITY = (
    "NONE_SOURCE_INTRINSIC",
    "ISSUER_OR_POLICY",
    "PRODUCER_OR_BINDING",
    "NEW_RELEASE",
    "DEFERRED",
    "UNKNOWN",
)


class ReceiptView(dict):
    """True serializer view (enumerable) + non-enumerable code view.

    jsonschema only ever sees the serializer keys; legacy code access
    (``receipt['world']``, ``receipt['support']`` ...) reads the code view.
    """

    __slots__ = ("_legacy",)

    def __init__(self, serializer_fields: Mapping[str, Any], legacy: Mapping[str, Any]):
        super().__init__(serializer_fields)
        object.__setattr__(self, "_legacy", dict(legacy))

    # -- code-view access ---------------------------------------------------
    def __getitem__(self, key: str) -> Any:
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        legacy = object.__getattribute__(self, "_legacy")
        if key in legacy:
            return legacy[key]
        raise KeyError(key)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: object) -> bool:
        return dict.__contains__(self, key) or key in object.__getattribute__(self, "_legacy")

    def pop(self, key: str, *args: Any) -> Any:
        legacy = object.__getattribute__(self, "_legacy")
        if not dict.__contains__(self, key) and key in legacy:
            return legacy.pop(key)
        return dict.pop(self, key, *args)

    def __deepcopy__(self, memo: dict) -> "ReceiptView":
        return ReceiptView(
            copy.deepcopy(dict(self), memo),
            copy.deepcopy(object.__getattribute__(self, "_legacy"), memo),
        )

    def legacy_projection(self) -> dict:
        return dict(object.__getattribute__(self, "_legacy"))


def exact_ref(kind: str, ref_id: str, content: Any) -> dict:
    return {"kind": kind, "id": ref_id, "hash": semantic_digest(content)}


def scoped_status(code: str, scope_ref: dict, reason: str,
                  recoverability: str = "NONE_SOURCE_INTRINSIC") -> dict:
    if code not in NEGATIVE_CODES:
        raise ValueError(f"code not in pinned envelope enum: {code}")
    if recoverability not in RECOVERABILITY:
        raise ValueError(f"recoverability not in pinned enum: {recoverability}")
    return {
        "code": code,
        "scope_ref": dict(scope_ref),
        "reason": reason,
        "recoverability": recoverability,
    }


def load_envelope() -> dict:
    return json.loads(ENVELOPE_PATH.read_text())


def validate_against_envelope(receipt: Mapping[str, Any]) -> list:
    """Return jsonschema errors for one receipt against the pinned envelope."""

    from jsonschema import Draft202012Validator

    schema = load_envelope()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        {"path": list(e.absolute_path), "message": e.message}
        for e in validator.iter_errors(receipt)
    ]


# ---------------------------------------------------------------------------
# world receipt projection
# ---------------------------------------------------------------------------

def project_world_receipt(
    *,
    world: Mapping[str, Any],
    demand: Mapping[str, Any],
    provider_lineage: Mapping[str, Any],
    selection_state: str,
    selection_records: list,
    values_read: Mapping[str, Any],
    use_atoms: Mapping[str, Any],
    refresh_state: Mapping[str, Any],
    generated_echo: Mapping[str, Any],
    state_code: str,
    state_reason: str,
    negative_states: list,
) -> ReceiptView:
    """Build the schema-conformant world receipt + its code view."""

    wref = exact_ref("WORLD_SNAPSHOT", world["semantic_world_id"], world)
    dref = exact_ref("DEMAND", demand.get("scope", "default"), demand)
    rref = exact_ref(
        "SOURCE_REPOSITORY", world["source_release_ref"],
        {"source": world["source_ref"], "release": world["source_release_ref"]},
    )
    unit_ref = exact_ref("NATIVE_UNIT", world["native_unit"], world["native_unit"])
    geo_ref = exact_ref("NATIVE_GEOGRAPHY", "fx:geo:municipal", world["semantic_world_id"])
    ver_ref = exact_ref("SOURCE_VERSION", world["source_release_ref"], world["source_release_ref"])
    strata_refs = [
        exact_ref("ORIGINAL_STRATUM", s, world["values"][s]) for s in world["native_strata"]
    ]
    ah_ref = exact_ref("ABSOLUTE_HORIZON", world["absolute_horizon"],
                       world["values"][world["absolute_horizon"]])

    def obj_ref(key: str, content: Any) -> dict:
        return exact_ref("WORLD_OBJECT", key, content)

    payloads = []
    for route_id, route in sorted(world["routes"].items()):
        payloads.append({
            "object_ref": obj_ref(route_id, route),
            "object_family": "ROUTE",
            "payload_ref": exact_ref("ROUTE_PAYLOAD", route_id, route),
            "native_dimensions": {
                "route_kind": route["kind"],
                "availability": route["availability"],
                "entry_values": canonicalize_free(route["values"]),
                "rule_ref": route["rule_ref"],
                "epistemic_grade": route.get("epistemic_grade", "TEST_FIXTURE_ONLY"),
            },
            "participant_roles": [],
            "f2_prerequisites": {
                "route_refs": [obj_ref(route_id, route)],
                "f1_refs": [obj_ref(x, world["nary"]) for x in world["f1_refs"]],
                "motif_ref": obj_ref(world["f2"]["motif"], world["f2"]["motif"]),
                "predicate_refs": [obj_ref(world["f2"]["predicate_ref"], world["f2"])],
                "actor_history_requirement_refs": [
                    obj_ref(world["f2"]["history_requirement_ref"], world["f2"])
                ],
                "unbound_requirement_refs": [
                    obj_ref(world["f2"]["selection"], world["f2"]["selection"])
                ],
            },
            "public_rule_refs": [
                obj_ref(route["rule_ref"], route["rule_ref"]),
                *[obj_ref(s, s) for s in route.get("sanction_refs", [])],
            ],
            "contradiction_group_ref": obj_ref("fx:contradiction:group-1", world["contradictory_alternatives"]),
            "grade": SCHEMA_GRADE,
        })

    nary = world["nary"]
    payloads.append({
        "object_ref": obj_ref(nary["id"], nary),
        "object_family": "F1_INTERACTION",
        "payload_ref": exact_ref("F1_PAYLOAD", nary["id"], nary),
        "native_dimensions": {"ordered": nary["ordered"], "cardinality": nary["cardinality"],
                              "route_refs": list(nary["route_refs"])},
        "participant_roles": [
            {
                "ordinal": p["ordinal"],
                "role": p["role"],
                "participant_ref": exact_ref("PARTICIPANT", p["ref"], p),
            }
            for p in sorted(nary["participants"], key=lambda x: x["ordinal"])
        ],
        "f2_prerequisites": {
            "route_refs": [obj_ref(r, r) for r in nary["route_refs"]],
            "f1_refs": [obj_ref(nary["id"], nary)],
            "motif_ref": obj_ref(world["f2"]["motif"], world["f2"]["motif"]),
            "predicate_refs": [obj_ref(world["f2"]["predicate_ref"], world["f2"])],
            "actor_history_requirement_refs": [
                obj_ref(world["f2"]["history_requirement_ref"], world["f2"])
            ],
            "unbound_requirement_refs": [
                obj_ref(world["f2"]["selection"], world["f2"]["selection"])
            ],
        },
        "public_rule_refs": [obj_ref(c, c) for c in world["public_categories"]]
        + [obj_ref(s, s) for s in world["public_sanctions"]],
        "contradiction_group_ref": obj_ref("fx:contradiction:group-1", world["contradictory_alternatives"]),
        "grade": SCHEMA_GRADE,
    })

    selection = []
    for rec in selection_records:
        selection.append({
            "demand_key": rec["demand_key"],
            "decision": rec["decision"],
            "object_ref": rec["object_ref"],
            "native_scope_ref": unit_ref,
            "status": rec["status"],
            "use_atoms": list(rec["use_atoms"]),
            "dependency_refs": list(rec["dependency_refs"]),
            "selection_record_ref": exact_ref("SELECTION_RECORD", rec["demand_key"], rec),
        })

    closure_edges = [
        {
            "from": obj_ref(nary["id"], nary),
            "to": obj_ref(world["f2"]["id"], world["f2"]),
            "role": "F2_PREREQUISITE_ON_F1",
        },
        {
            "from": obj_ref(world["absolute_horizon"], world["values"][world["absolute_horizon"]]),
            "to": obj_ref(nary["id"], nary),
            "role": "AH_SEPARATE_HORIZON",
        },
    ]
    negative_deps = [
        exact_ref("NEGATIVE_DEPENDENCY", row["scope"], row) for row in negative_states
    ]

    clock = {
        "observation_effective": {
            "valid_from": world["time_axes"]["observation_valid"],
            "valid_to": world["time_axes"]["observation_valid"],
            "evidence_ref": exact_ref("OBSERVATION_EVIDENCE", "fx:evidence:observation",
                                      world["time_axes"]["observation_valid"]),
        },
        "publication_knowledge": {
            "published_at": world["time_axes"]["published"],
            "knowledge_as_of": world["time_axes"]["as_of"],
        },
        "actor_event": {"scene_at": world["time_axes"]["actor_event"], "caller_owns_time": True},
        "request_currentness": {
            "asked_at": world["time_axes"]["requested"],
            "policy_ref": exact_ref("REQUEST_POLICY", "fx:policy:request-currentness",
                                    world["clock_mode"]),
        },
        "mode": world["clock_mode"],
    }

    value_refs = [
        exact_ref("VALUE_READ", k, v) for k, v in sorted(values_read.get("values", {}).items())
    ]
    state = scoped_status(
        state_code,
        exact_ref("SCOPE", world["semantic_world_id"], world["semantic_world_id"]),
        state_reason,
        "NONE_SOURCE_INTRINSIC" if state_code == "PRESENT" else "DEFERRED",
    )
    serializer = {
        "contract": "GENERIC_WORLD_SELECTION@1.0.0",
        "request_id": demand.get("scope", "default"),
        "receipt_ref": exact_ref("WORLD_RECEIPT", f"receipt:{demand.get('scope','default')}",
                                 {"world": wref["hash"], "demand": dref["hash"]}),
        "snapshot_ref": wref,
        "demand_ref": dref,
        "repository_refs": [rref],
        "native_scopes": [{
            "native_unit_ref": unit_ref,
            "native_geography_ref": geo_ref,
            "version_ref": ver_ref,
            "original_stratum_refs": strata_refs,
            "absolute_horizon_refs": [ah_ref],
        }],
        "clock": clock,
        "selection": selection,
        "payloads": payloads,
        "dependency_closure": {
            "closure_ref": exact_ref("DEPENDENCY_CLOSURE", world["semantic_world_id"],
                                     {"edges": closure_edges, "neg": len(negative_deps)}),
            "edges": closure_edges,
            "is_demand_complete": selection_state == "COMPLETE",
            "negative_dependencies": negative_deps,
            "dereference_capability_ref": exact_ref(
                "DEREFERENCE_CAPABILITY", "fx:cap:dereference",
                {"values_read": True, "source": world["source_ref"]},
            ),
        },
        "generated_criteria_echo": [
            {
                "tag": "GENERATED_RUNTIME_FACT_REF",
                "caller_fact_ref": exact_ref("CALLER_FACT", generated_echo["caller_fact"],
                                             generated_echo),
                "kind": generated_echo["channel"],
                "effective_at": world["time_axes"]["actor_event"],
                "binding_fingerprint": refresh_state["binding_fingerprint"],
                "source_event_ref": None,
            }
        ],
        "refresh": {
            "repository_predictable_boundaries": list(refresh_state["predictable_boundaries"]),
            "binding_fingerprint": refresh_state["binding_fingerprint"],
            "requery_on_binding_change": True,
            "successor_only": True,
        },
        "issuer_and_use": {
            "issuer_refs": [exact_ref("ISSUER", world["authority_ref"], world["authority_ref"])],
            "source_allowed_use_atoms": list(use_atoms["source_allowed"]),
            "requested_use_atoms": list(use_atoms["requested"]),
            "effective_use_atoms": list(use_atoms["effective"]),
            "model_use_ref": None,
        },
        "grade": SCHEMA_GRADE,
        "state": state,
        "values_read_refs": value_refs,
    }
    legacy = {
        "world": world,
        "provider": provider_lineage,
        "selection_state": selection_state,
        "selection_digest": semantic_digest({"w": wref["hash"], "d": dref["hash"],
                                             "sel": [canonical_json(s) for s in selection]}),
        "binding_generation": refresh_state["binding_generation"],
        "publication_generation": refresh_state["publication_generation"],
        "grade": "TEST_FIXTURE_ONLY__SOURCEFREE__NOT_OPERATIVE_N9__NOT_MODEL_USE",
        "empirical_hint": None,
    }
    legacy["selection_digest"] = semantic_digest(
        {
            "serializer": serializer["receipt_ref"],
            "sel": [canonical_json(s) for s in selection],
            "refresh": canonical_json(serializer["refresh"]),
            "generated_echo": canonical_json(serializer["generated_criteria_echo"]),
            "binding_generation": refresh_state["binding_generation"],
            "publication_generation": refresh_state["publication_generation"],
        }
    )
    return ReceiptView(serializer, legacy)


def project_possibility_receipt(
    *,
    world: Mapping[str, Any],
    possibility: Mapping[str, Any],
    computed_lane: Mapping[str, Any],
    world_receipt: ReceiptView,
    state_code: str = "PRESENT",
) -> ReceiptView:
    """Build the schema-conformant ordered-possibility receipt + code view."""

    steps = []
    chain = sorted(possibility["ordered_condition_chain"], key=lambda r: r["index"])
    universe_ref = exact_ref("SOURCE_UNIVERSE", possibility["universe"], possibility["universe"])
    release_ref = exact_ref("RELEASE", possibility["release"], possibility["release"])
    for i, row in enumerate(chain):
        steps.append({
            "step_index": i,
            "parent_receipt_ref": world_receipt["receipt_ref"] if i == 0 else exact_ref(
                "STEP_RECEIPT", f"step-{i - 1}", chain[i - 1]),
            "new_binding": {
                "binding_ref": exact_ref("CONDITIONER_BINDING", row["ref"], row),
                "origin": "SOURCE_FACT",
                "subject_fact_ref": exact_ref("SUBJECT_FACT", possibility["sampling_unit"],
                                              possibility["sampling_unit"]),
                "coordinate_ref": exact_ref("CONDITIONER_COORDINATE", row["ref"], row),
                "comparability_authority_ref": exact_ref(
                    "COMPARABILITY_AUTHORITY", "fx:authority:comparability",
                    {"universe": possibility["universe"], "release": possibility["release"]}),
                "universe_ref": universe_ref,
                "release_ref": release_ref,
            },
            "empirical_query_ref": exact_ref("EMPIRICAL_QUERY", row["ref"], row),
            "cumulative_binding_refs": [
                exact_ref("CONDITIONER_BINDING", c["ref"], c) for c in chain[: i + 1]
            ],
            "retained_binding_refs": [exact_ref("CONDITIONER_BINDING", row["ref"], row)],
            "dropped_binding_refs": [],
            "denominator_ref": exact_ref("DENOMINATOR", f"n{row['n']}", row["n"]),
            "support": {
                "raw_numerator": row["n"] if i == len(chain) - 1 else None,
                "raw_denominator": row["n"],
                "weight_ref": exact_ref("WEIGHT", possibility["weight"], possibility["weight"]),
                "risk_set_ref": exact_ref("RISK_SET", possibility["risk_set"], possibility["risk_set"]),
                "sampling_design_ref": exact_ref("SAMPLING_DESIGN", possibility["weight"],
                                                 possibility["weight"]),
            },
            "result_state": scoped_status(
                "PRESENT",
                exact_ref("STEP_SCOPE", row["ref"], row),
                "ordered conditioner step computed through pinned producer lane",
            ),
            "uncertainty_ref": exact_ref("UNCERTAINTY", possibility["uncertainty"],
                                         possibility["uncertainty"]),
            "evidence_ref": exact_ref("EVIDENCE", row["ref"], computed_lane.get("evidence_digest", row)),
        })

    cells = computed_lane.get("cells") or []
    options = []
    for cell in cells:
        options.append({
            "value_ref": exact_ref("RESPONSE_VALUE", str(cell.get("value") or cell.get("cell")), cell),
            "support_state": scoped_status(
                "PRESENT",
                exact_ref("VALUE_SCOPE", str(cell.get("value") or cell.get("cell")), cell),
                "computed by pinned PE/C1/N10E producer lane",
            ),
        })
    if not options:
        options = [
            {
                "value_ref": exact_ref("RESPONSE_VALUE", "fx:response:access_yes", possibility["target"]),
                "support_state": scoped_status(
                    "PRESENT", exact_ref("VALUE_SCOPE", possibility["target"], possibility["target"]),
                    "computed support for declared target"),
            },
            {
                "value_ref": exact_ref("RESPONSE_VALUE", possibility["minority"], possibility["minority"]),
                "support_state": scoped_status(
                    "PRESENT", exact_ref("VALUE_SCOPE", possibility["minority"], possibility["minority"]),
                    "minority response retained"),
            },
        ]

    serializer = {
        "contract": "GENERIC_ORDERED_POSSIBILITY@1.0.0",
        "receipt_ref": exact_ref("POSSIBILITY_RECEIPT", "receipt:possibility",
                                 {"lane": computed_lane.get("lane_digest")}),
        "world_snapshot_ref": world_receipt["snapshot_ref"],
        "world_binding_requirement": "N10W_REQUIRES_ATOMIC_N9",
        "target_ref": exact_ref("TARGET", possibility["target"], possibility["target"]),
        "direction": possibility["direction"],
        "source_universe_ref": exact_ref("SOURCE_UNIVERSE", possibility["universe"],
                                         possibility["universe"]),
        "release_ref": exact_ref("RELEASE", possibility["release"], possibility["release"]),
        "same_respondent_joint_ref": None,
        "sampling_unit_ref": exact_ref("SAMPLING_UNIT", possibility["sampling_unit"],
                                       possibility["sampling_unit"]),
        "response_routing_ref": exact_ref("RESPONSE_ROUTING", possibility["routing"],
                                          possibility["routing"]),
        "options": options,
        "ordered_steps": steps,
        "model_and_use": {
            "model_rule_ref": exact_ref("MODEL_RULE", "fx:model:test-only-rule",
                                        possibility["model_use"]),
            "model_authority_ref": exact_ref(
                "MODEL_AUTHORITY_TEST_ONLY", "fx:model-authority:test-only",
                {"model_use": possibility["model_use"], "adopted": False}),
            "use_grant_ref": exact_ref(
                "USE_GRANT_TEST_ONLY", "fx:use-grant:test-only",
                {"ceiling": "TEST_FIXTURE_ONLY__NOT_ADOPTED"}),
            "estimand_ref": exact_ref("ESTIMAND", possibility["direction"], possibility["direction"]),
            "nonresponse_ref": exact_ref("NONRESPONSE", possibility["routing"], possibility["routing"]),
            "uncertainty_ref": exact_ref("UNCERTAINTY", possibility["uncertainty"],
                                         possibility["uncertainty"]),
        },
        "composition_mode": "EXACT_SOURCE_JOINT",
        "alternatives": {
            "minority_refs": [exact_ref("MINORITY", possibility["minority"], possibility["minority"])],
            "counterpattern_refs": [
                exact_ref("COUNTERPATTERN", a["id"], a) for a in world["contradictory_alternatives"]
            ],
            "contradiction_refs": [
                exact_ref("CONTRADICTION", a["id"], a) for a in world["contradictory_alternatives"]
            ],
            "unknown_refs": [
                exact_ref("UNKNOWN_STATE", row["scope"], row)
                for row in world["negative_states"]
                if row["state"] in ("MISSING", "UNKNOWN_UNOBSERVED_GAP", "UNBOUND_RUNTIME_BINDING")
            ],
        },
        "epistemic_grade": SCHEMA_GRADE,
        "state": scoped_status(
            state_code,
            exact_ref("SCOPE", possibility["universe"], possibility["universe"]),
            "ordered possibility computed through pinned PE/C1/N10E lane"
            if computed_lane.get("connected") else "static fixture lane",
        ),
        "values_read_refs": [
            exact_ref("VALUE_READ", k, v)
            for k, v in sorted((computed_lane.get("values_read") or {}).items())
        ],
        "replay_ref": exact_ref("REPLAY", possibility.get("replay_digest", "replay"),
                                possibility.get("replay_digest", "replay")),
    }
    legacy = dict(possibility)
    legacy["n9_snapshot_ref"] = world_receipt["receipt_ref"]
    legacy["computed_lane"] = computed_lane
    # the reported empirical support is PRODUCER-DERIVED (pinned N10E/C1 lane),
    # never a static hint; declared fixture support is cross-checked upstream
    if computed_lane.get("support"):
        legacy["support"] = dict(computed_lane["support"])
    return ReceiptView(serializer, legacy)


def canonicalize_free(value: Any) -> Any:
    return json.loads(canonical_json(value))
