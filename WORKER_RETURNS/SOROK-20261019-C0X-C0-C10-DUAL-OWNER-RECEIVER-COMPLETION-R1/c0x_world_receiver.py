"""Sorok C0X — versioned read-only two-owner world receiver.

This is a receiving facade, not a producer, estimator, issuer or C11 weld. It
consumes the ACTUAL repaired C0P two-contract object (N9 selected-world receipt
plus N10E/N10W ordered-possibility receipt) from the exact upstream blob and
exposes the demand's material world opportunity with native units, source
permission, values-read, four clocks, minority/unknown and no joint probability.

Two owner contracts are transported separately. They are never merged,
substituted, averaged, or converted into a route probability or selection
weight. A non-transportable owner field is preserved and typed, never silently
dropped or fabricated.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "stage/runtime"
UPSTREAM = ROOT / "upstream/c0p_two_contract_port.py"


def _ensure_runtime():
    """Materialize the exact 29-module closure from pinned Git objects.

    The runtime is deliberately not duplicated into the committed tree: it is
    staged on demand from the exact E03/E04T blob preimages and verified by the
    stage script's 29/29 ledger. This keeps inherited native tests out of the
    C0X changed-test surface while preserving exact bytes.
    """
    ledger = RUNTIME.parent / "_c0p_runtime_ledger.json"
    ready = (RUNTIME / "product/nonparent.py").is_file() and ledger.is_file()
    if ready:
        data = json.loads(ledger.read_text())
        ready = (len(data.get("ledger", [])) == 29
                 and all(row.get("all_match") for row in data["ledger"]))
    if not ready:
        env = dict(os.environ)
        env["C0P_REPO"] = str(ROOT.parents[1])
        env["C0P_RUNTIME"] = str(RUNTIME)
        subprocess.run([sys.executable, "-B", str(ROOT / "tools/c0p_stage_runtime.py")],
                       cwd=str(ROOT), env=env, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if str(RUNTIME) not in sys.path:
        sys.path.insert(0, str(RUNTIME))


_ensure_runtime()

_SPEC = importlib.util.spec_from_file_location("c0x_upstream_c0p", UPSTREAM)
FACADE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = FACADE
_SPEC.loader.exec_module(FACADE)

SCHEMA = "SOROK_C0X_WORLD_RECEIVER@1"
RECEIVER_VERSION = "1.0.0"
N9 = "N9"
N10 = "N10E_N10W"
ENV_WORLD = "GENERIC_WORLD_SELECTION@1.0.0"
ENV_POSS = "GENERIC_ORDERED_POSSIBILITY@1.0.0"
WORLD_FIELDS = (
    "contract", "request_id", "receipt_ref", "snapshot_ref", "demand_ref",
    "repository_refs", "native_scopes", "clock", "selection", "payloads",
    "dependency_closure", "generated_criteria_echo", "refresh",
    "issuer_and_use", "grade", "state", "values_read_refs",
)
POSS_FIELDS = (
    "contract", "receipt_ref", "world_snapshot_ref", "world_binding_requirement",
    "target_ref", "direction", "source_universe_ref", "release_ref",
    "same_respondent_joint_ref", "sampling_unit_ref", "response_routing_ref",
    "options", "ordered_steps", "model_and_use", "composition_mode",
    "alternatives", "epistemic_grade", "state", "values_read_refs", "replay_ref",
)
DEMANDS = {
    "NONPARENT_OPTIONS": N9,
    "CONCEPTION_SCENARIO_PROPOSALS": N10,
}
SCIENTIFIC_CEILING = (
    "SOURCEFREE_TEST_ONLY_TWO_OWNER_READ_ONLY_NO_ROUTE_PROBABILITY_"
    "NO_SELECTION_WEIGHT_NO_ACTOR_GENERATION"
)


class ReceiverRefusal(Exception):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _non_transportable(value, path=""):
    """Return exact paths of values JSON cannot transport (callables, etc.)."""
    if isinstance(value, (str, int, float, bool, type(None))):
        return []
    if isinstance(value, dict):
        out = []
        for key, child in value.items():
            out.extend(_non_transportable(child, f"{path}.{key}" if path else str(key)))
        return out
    if isinstance(value, (list, tuple)):
        out = []
        for index, child in enumerate(value):
            out.extend(_non_transportable(child, f"{path}[{index}]"))
        return out
    return [path or "<root>"]


def _structural_state(routes):
    states = {key: (value or {}).get("state") for key, value in (routes or {}).items()}
    if any("UNAVAILABLE" in (state or "") for state in states.values()):
        return "PARTIAL", "MATERIAL_ROUTE_UNAVAILABLE"
    if any("BLOCKED" in (state or "") for state in states.values()):
        return "PARTIAL", "MATERIAL_ROUTE_BLOCKED"
    return "SUPPORTED", None


def make_receipt(consumer, *, service_options=None, select_kwargs=None, proposals=None):
    """Build the ACTUAL upstream receipt; no fixture, no cache."""
    if consumer not in DEMANDS:
        raise ReceiverRefusal("NO_OWNER_CONSUMER_FOR_DEMAND", consumer)
    port = FACADE.TwoContractPort(**(service_options or {}))
    snapshot = port.select(mode="AS_OF", **(select_kwargs or {}))
    if consumer == "NONPARENT_OPTIONS":
        return port.consume_nonparent(snapshot)
    return port.consume_conception_proposals(snapshot, proposals or [])


def _unavailable(demand, reason, detail=""):
    return {
        "schema": SCHEMA,
        "receiver_version": RECEIVER_VERSION,
        "demand": dict(demand or {}),
        "evidence_state": "UNKNOWN",
        "evidence_reasons": [reason],
        "upstream_refusal_detail": detail,
        "owner_contracts": None,
        "owner_identities": None,
        "native_units": None,
        "four_clocks": None,
        "source_permission": None,
        "values_read": None,
        "values_read_refs": None,
        "minority_unknown": None,
        "material_world_opportunity": None,
        "generated_conditioner_limits": None,
        "transport": {"state": "NO_RECEIPT", "json_serializable": False,
                      "non_transportable_fields": []},
        "no_joint_probability": True,
        "route_probability": None,
        "selection_weight": None,
        "real_use_authorized": False,
        "scientific_ceiling": SCIENTIFIC_CEILING,
    }


def receive_demand(consumer, *, demand=None, service_options=None,
                   select_kwargs=None, proposals=None):
    """Wrap actual receipt construction and type upstream temporal refusal."""
    try:
        receipt = make_receipt(consumer, service_options=service_options,
                               select_kwargs=select_kwargs, proposals=proposals)
    except (TypeError, FACADE.FacadeRefusal) as exc:
        return _unavailable({"consumer": consumer, **(demand or {})},
                            "UPSTREAM_TEMPORAL_OR_REFERENCE_REFUSAL", str(exc))
    return receive_receipt(receipt, {"consumer": consumer, **(demand or {})})


def receive_receipt(receipt, demand=None):
    """Read the actual two-owner receipt into a typed material opportunity."""
    if receipt is None:
        raise ReceiverRefusal("MISSING_OWNER_CONTRACT", "receipt is None")
    demand = dict(demand or {})
    world = receipt.world_receipt
    poss = receipt.possibility_receipt
    if not world:
        raise ReceiverRefusal("MISSING_OWNER_CONTRACT", "world receipt absent")
    if not poss:
        raise ReceiverRefusal("MISSING_OWNER_CONTRACT", "possibility receipt absent")
    if world.get("contract") != ENV_WORLD:
        raise ReceiverRefusal("OWNER_CONTRACT_MISMATCH", "world contract")
    if poss.get("contract") != ENV_POSS:
        raise ReceiverRefusal("OWNER_CONTRACT_MISMATCH", "possibility contract")
    if len(world) != 17:
        raise ReceiverRefusal("RECEIPT_FIELD_INCOMPLETE",
                              f"world={len(world)}/17")
    if len(poss) != 20:
        raise ReceiverRefusal("RECEIPT_FIELD_INCOMPLETE",
                              f"possibility={len(poss)}/20")
    if set(world) != set(WORLD_FIELDS):
        raise ReceiverRefusal("RECEIPT_FIELD_SET_MISMATCH", "world fields")
    if set(poss) != set(POSS_FIELDS):
        raise ReceiverRefusal("RECEIPT_FIELD_SET_MISMATCH", "possibility fields")

    consumer = demand.get("consumer") or receipt.owner_payload.get("consumer")
    if consumer not in DEMANDS:
        raise ReceiverRefusal("NO_OWNER_CONSUMER_FOR_DEMAND", str(consumer))
    expected_contract = DEMANDS[consumer]
    if receipt.contract != expected_contract:
        raise ReceiverRefusal("OWNER_SUBSTITUTION",
                              f"{receipt.contract} cannot satisfy {consumer}")
    if receipt.contract_envelope != (ENV_WORLD if expected_contract == N9 else ENV_POSS):
        raise ReceiverRefusal("OWNER_CONTRACT_MISMATCH", "receipt envelope")

    if demand.get("direction", "FORWARD_CONDITIONAL") != "FORWARD_CONDITIONAL":
        raise ReceiverRefusal("REVERSE_HELD", "reverse direction not granted")
    if poss.get("direction") != "FORWARD_CONDITIONAL":
        raise ReceiverRefusal("REVERSE_HELD", "possibility direction")
    use = demand.get("use", "TEST_ONLY_CONTEXT")
    if use not in ("TEST_ONLY_CONTEXT", "SOURCEFREE_EXPERIMENT"):
        raise ReceiverRefusal("PROHIBITED_MODEL_USE", str(use))

    world_ref = world.get("receipt_ref") or {}
    poss_ref = poss.get("receipt_ref") or {}
    if not world_ref or not poss_ref:
        raise ReceiverRefusal("MISSING_OWNER_IDENTITY", "receipt ref absent")
    if world.get("contract") == poss.get("contract") or world == poss:
        raise ReceiverRefusal("OWNER_IDENTITIES_NOT_DISTINCT", "same owner contract")

    owner = receipt.owner_payload or {}
    if owner.get("route_probability") is not None:
        raise ReceiverRefusal("ROUTE_PROBABILITY_ISSUED", "owner route probability")
    if owner.get("selection_weight") is not None:
        raise ReceiverRefusal("SELECTION_WEIGHT_ISSUED", "owner selection weight")
    if owner.get("person_generation") is True or owner.get("actual_conception") is True:
        raise ReceiverRefusal("ACTOR_OR_PERSON_GENERATION", "person/conception")
    if poss.get("same_respondent_joint_ref") is not None:
        raise ReceiverRefusal("JOINT_PROBABILITY_ISSUED", "same-respondent joint")
    if poss.get("composition_mode") != "REFUSED":
        raise ReceiverRefusal("JOINT_PROBABILITY_ISSUED", "composition mode")
    alternatives = poss.get("alternatives") or {}
    if alternatives.get("route_probability") is not None:
        raise ReceiverRefusal("ROUTE_PROBABILITY_ISSUED", "alternatives route")
    if world.get("generated_criteria_echo") != []:
        raise ReceiverRefusal("GENERATED_CONDITIONER_ISSUED", "generated criteria")

    issuer = world.get("issuer_and_use") or {}
    if issuer.get("model_use_ref") is not None:
        raise ReceiverRefusal("PROHIBITED_MODEL_USE", "model use ref")
    allowed = set(issuer.get("source_allowed_use_atoms") or [])
    effective = set(issuer.get("effective_use_atoms") or [])
    if not effective or not effective <= {"TEST_ONLY_CONTEXT"} or not allowed <= {"TEST_ONLY_CONTEXT"}:
        raise ReceiverRefusal("PROHIBITED_MODEL_USE", "non-test use atom")

    clock = world.get("clock") or {}
    for key in ("observation_effective", "publication_knowledge",
                "actor_event", "request_currentness"):
        if key not in clock:
            raise ReceiverRefusal("CLOCK_INCOMPLETE", key)

    structural = owner.get("structural_routes") or {}
    empirical = owner.get("empirical") or {}
    scenarios = owner.get("scenarios") or []
    state, material_reason = _structural_state(structural)
    reasons = []
    if material_reason:
        reasons.append(material_reason)
    if empirical.get("state") != "PRODUCTIVE_TEST_ONLY":
        state = "PARTIAL" if state == "SUPPORTED" else state
        reasons.append("EMPIRICAL_SUPPORT_NOT_PRODUCTIVE")
    if not world.get("selection"):
        state = "PARTIAL" if state == "SUPPORTED" else state
        reasons.append("OWNER_SELECTION_EMPTY")
    if not world.get("payloads"):
        state = "PARTIAL" if state == "SUPPORTED" else state
        reasons.append("OWNER_PAYLOADS_EMPTY")
    if not world.get("native_scopes"):
        state = "PARTIAL" if state == "SUPPORTED" else state
        reasons.append("NATIVE_SCOPE_EMPTY")
    if consumer == "CONCEPTION_SCENARIO_PROPOSALS":
        if not scenarios:
            state = "PARTIAL" if state == "SUPPORTED" else state
            reasons.append("SCENARIO_OUTPUT_EMPTY")
        if any((s or {}).get("selection_weight") is not None for s in scenarios):
            raise ReceiverRefusal("SELECTION_WEIGHT_ISSUED", "scenario weight")

    non_transportable = (
        [f"world_receipt.{p}" for p in _non_transportable(world)]
        + [f"possibility_receipt.{p}" for p in _non_transportable(poss)]
    )
    transport = {
        "state": ("NON_TRANSPORTABLE_OWNER_FIELD" if non_transportable
                  else "LOSSLESS_TWO_CONTRACT_OBJECT"),
        "json_serializable": not non_transportable,
        "non_transportable_fields": non_transportable,
        "world_receipt_fields": len(world),
        "possibility_receipt_fields": len(poss),
    }

    result = {
        "schema": SCHEMA,
        "receiver_version": RECEIVER_VERSION,
        "demand": demand,
        "evidence_state": state,
        "evidence_reasons": reasons,
        "owner_contracts": {
            N9: {
                "contract_version": world.get("contract"),
                "field_count": len(world),
                "owner_receipt_hash": (receipt.owner_receipt_hash
                                       if receipt.contract == N9 else None),
                "receipt_ref": world_ref,
                "receipt": world,
            },
            N10: {
                "contract_version": poss.get("contract"),
                "field_count": len(poss),
                "owner_receipt_hash": (receipt.owner_receipt_hash
                                       if receipt.contract == N10 else None),
                "receipt_ref": poss_ref,
                "receipt": poss,
            },
        },
        "owner_identities": {
            "distinct": (world.get("contract") != poss.get("contract")
                         and world != poss),
            "contract_versions_distinct": world.get("contract") != poss.get("contract"),
            "owner_outputs_distinct": world != poss,
            "receipt_refs_equal": world_ref == poss_ref,
            "note": "distinct owner contract versions and outputs; a shared "
                    "consumer receipt ref is recorded, not hidden",
            "world_receipt_ref": world_ref,
            "possibility_receipt_ref": poss_ref,
            "consumer_receipt_hash": receipt.owner_receipt_hash,
        },
        "native_units": world.get("native_scopes"),
        "four_clocks": clock,
        "actor_clock_is_caller_owned": bool(
            (clock.get("actor_event") or {}).get("caller_owns_time")),
        "historical_entitlement_reconstructed": False,
        "source_permission": issuer,
        "grade": world.get("grade"),
        "values_read": owner.get("values_read"),
        "values_read_refs": world.get("values_read_refs"),
        "minority_unknown": {
            "selection_records": len(world.get("selection") or []),
            "payloads": len(world.get("payloads") or []),
            "empirical_state": empirical.get("state"),
            "empirical_steps": empirical.get("steps"),
            "pruned": False,
            "unknown_preserved": True,
        },
        "material_world_opportunity": {
            "consumer": consumer,
            "structural_routes": structural,
            "empirical_state": empirical.get("state"),
            "empirical_steps": empirical.get("steps"),
            "scenarios": scenarios if consumer == "CONCEPTION_SCENARIO_PROPOSALS" else None,
            "route_probability": None,
            "selection_weight": None,
            "no_joint_probability": True,
            "person_generation": False,
            "actual_conception": False,
        },
        "generated_conditioner_limits": {
            "generated_criteria_echo": world.get("generated_criteria_echo"),
            "same_respondent_joint_ref": poss.get("same_respondent_joint_ref"),
            "composition_mode": poss.get("composition_mode"),
            "model_use_ref": issuer.get("model_use_ref"),
            "actor_generation": False,
            "person_generation": False,
            "actual_conception": False,
        },
        "transport": transport,
        "transport_hold": bool(non_transportable),
        "no_joint_probability": True,
        "route_probability": None,
        "selection_weight": None,
        "real_use_authorized": False,
        "scientific_ceiling": SCIENTIFIC_CEILING,
    }
    return result
