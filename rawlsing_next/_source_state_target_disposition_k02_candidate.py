"""Source-agnostic PRE-V3 source-state -> product-target disposition law.

This module is deliberately free of source-family/native-code tables.  Raw
source material is retained only as opaque audit identity; matching is done on
an explicitly governed source-local semantic state supplied by the PRE553
adapter.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

CONTRACT_ID = "PREV3_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_PRODUCTION@1.0.0"
WORLD_SCOPE = "OBJECTIVE"
AUTHORITY_PHASE = "FROZEN_PRE_OUTCOME"

RAW_SOURCE_STATE = "RAW_SOURCE_STATE"
SOURCE_LOCAL_GOVERNED_STATE = "SOURCE_LOCAL_GOVERNED_STATE"
PRODUCT_TARGET_DISPOSITION = "PRODUCT_TARGET_DISPOSITION"
DENOMINATOR_RESOLUTION_CHECK = "DENOMINATOR_RESOLUTION_CHECK"
EMPIRICAL_RESULT = "EMPIRICAL_RESULT"

TARGET_MEMBER = "TARGET_MEMBER"
RESOLVED_NON_TARGET = "RESOLVED_NON_TARGET"
UNRESOLVED = "UNRESOLVED"

DISPOSITIONS = frozenset({TARGET_MEMBER, RESOLVED_NON_TARGET, UNRESOLVED})
STATE_CLASSES = frozenset({
    "SOURCE_SUBSTANTIVE",
    "TYPED_MISSING_NONRESPONSE",
    "NOT_APPLICABLE_OR_INELIGIBLE",
    "SOURCE_SPECIFIC_SPECIAL",
    "SOURCE_UNKNOWN",
})


class SourceStateDispositionContractError(ValueError):
    """The generic source-state disposition contract is malformed or unresolved."""


@dataclass(frozen=True)
class ContractExecutionReceipt:
    contract_hash: str
    denominator_checks: tuple[Mapping[str, Any], ...]
    empirical_result: Mapping[str, Any]
    replay_identity: str


def _canonical(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise SourceStateDispositionContractError("binary floats are forbidden in contract identity")
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise SourceStateDispositionContractError("contract mapping keys must be strings")
        return {key: _canonical(value[key]) for key in sorted(value)}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_canonical(item) for item in value]
    if isinstance(value, (set, frozenset)):
        items = [_canonical(item) for item in value]
        return sorted(items, key=canonical_json)
    raise SourceStateDispositionContractError(
        f"unsupported contract identity value {type(value).__name__}"
    )


def canonical_json(value: Any) -> str:
    return json.dumps(_canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def semantic_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise SourceStateDispositionContractError(f"{name} must be a mapping")
    return value


def _require_sequence(value: Any, name: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise SourceStateDispositionContractError(f"{name} must be a sequence")
    if not allow_empty and not value:
        raise SourceStateDispositionContractError(f"{name} may not be empty")
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceStateDispositionContractError(f"{name} must be non-empty text")
    return value.strip()


def _exact_keys(mapping: Mapping[str, Any], expected: set[str], name: str) -> None:
    actual = set(mapping)
    if actual != expected:
        raise SourceStateDispositionContractError(
            f"{name} keys must be exactly {sorted(expected)!r}; got {sorted(actual)!r}"
        )


def _state_key(universe_ref: Any, response_state: str, canonical_response_value: Any) -> str:
    return canonical_json({
        "empirical_universe_ref": _canonical(universe_ref),
        "response_state": response_state,
        "canonical_response_value": _canonical(canonical_response_value),
    })


def normalize_contract(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate and canonicalize the reusable contract declaration.

    The declaration can name exact universe/authority/reference identities and
    governed semantic states, but it has no field in which a native/raw code or
    source-family table can be expressed.
    """
    raw = _require_mapping(raw, "contract")
    _exact_keys(raw, {
        "contract_id", "world_scope", "authority_phase", "risk_set_ref", "components"
    }, "contract")
    if raw.get("contract_id") != CONTRACT_ID:
        raise SourceStateDispositionContractError("unsupported source-state contract id")
    if raw.get("world_scope") != WORLD_SCOPE:
        raise SourceStateDispositionContractError("PRE-V3 source-state contract is objective-world only")
    if raw.get("authority_phase") != AUTHORITY_PHASE:
        raise SourceStateDispositionContractError("denominator authority must be frozen pre-outcome")

    components_out: list[dict[str, Any]] = []
    target_keys: set[str] = set()
    for component_index, component_raw in enumerate(
        _require_sequence(raw.get("components"), "contract.components")
    ):
        component = _require_mapping(component_raw, f"contract.components[{component_index}]")
        _exact_keys(component, {
            "target_ref", "target_domain_ref", "authority_bindings", "state_bindings"
        }, f"contract.components[{component_index}]")
        target_ref = _canonical(component["target_ref"])
        target_key = canonical_json(target_ref)
        if target_key in target_keys:
            raise SourceStateDispositionContractError("duplicate exact target_ref in contract")
        target_keys.add(target_key)

        authorities_out: list[dict[str, Any]] = []
        authority_universes: set[str] = set()
        for authority_index, binding_raw in enumerate(
            _require_sequence(component["authority_bindings"], "authority_bindings")
        ):
            binding = _require_mapping(binding_raw, f"authority_bindings[{authority_index}]")
            _exact_keys(binding, {
                "empirical_universe_ref",
                "source_semantic_authority_ref", "source_semantic_operation",
                "target_use_authority_ref", "target_use_operation",
                "risk_set_authority_ref", "risk_set_operation",
                "replay_authority_ref", "replay_operation",
            }, f"authority_bindings[{authority_index}]")
            universe_ref = _canonical(binding["empirical_universe_ref"])
            universe_key = canonical_json(universe_ref)
            if universe_key in authority_universes:
                raise SourceStateDispositionContractError(
                    "duplicate exact universe authority binding for one target"
                )
            authority_universes.add(universe_key)
            target_auth = _canonical(binding["target_use_authority_ref"])
            risk_auth = _canonical(binding["risk_set_authority_ref"])
            if canonical_json(target_auth) == canonical_json(risk_auth):
                raise SourceStateDispositionContractError(
                    "target-domain authority and denominator/risk-set authority must be distinct"
                )
            authorities_out.append({
                "empirical_universe_ref": universe_ref,
                "source_semantic_authority_ref": _canonical(binding["source_semantic_authority_ref"]),
                "source_semantic_operation": _text(binding["source_semantic_operation"], "source_semantic_operation"),
                "target_use_authority_ref": target_auth,
                "target_use_operation": _text(binding["target_use_operation"], "target_use_operation"),
                "risk_set_authority_ref": risk_auth,
                "risk_set_operation": _text(binding["risk_set_operation"], "risk_set_operation"),
                "replay_authority_ref": _canonical(binding["replay_authority_ref"]),
                "replay_operation": _text(binding["replay_operation"], "replay_operation"),
            })

        states_out: list[dict[str, Any]] = []
        seen_state_keys: set[str] = set()
        for state_index, binding_raw in enumerate(
            _require_sequence(component["state_bindings"], "state_bindings", allow_empty=True)
        ):
            binding = _require_mapping(binding_raw, f"state_bindings[{state_index}]")
            _exact_keys(binding, {
                "empirical_universe_ref", "response_state", "canonical_response_value",
                "state_class", "product_target_disposition",
            }, f"state_bindings[{state_index}]")
            response_state = _text(binding["response_state"], "response_state")
            state_class = _text(binding["state_class"], "state_class")
            if state_class not in STATE_CLASSES:
                raise SourceStateDispositionContractError("unknown source-local state_class")
            disposition = _text(binding["product_target_disposition"], "product_target_disposition")
            if disposition not in DISPOSITIONS:
                raise SourceStateDispositionContractError("unknown product_target_disposition")
            universe_ref = _canonical(binding["empirical_universe_ref"])
            canonical_value = _canonical(binding["canonical_response_value"])
            key = _state_key(universe_ref, response_state, canonical_value)
            if key in seen_state_keys:
                raise SourceStateDispositionContractError(
                    "duplicate source-local governed state binding for one target"
                )
            seen_state_keys.add(key)
            if canonical_json(universe_ref) not in authority_universes:
                raise SourceStateDispositionContractError(
                    "state binding has no exact universe authority binding"
                )
            if (
                response_state == "SUBSTANTIVE_RESPONSE"
                and canonical_value is None
                and disposition != UNRESOLVED
            ):
                raise SourceStateDispositionContractError(
                    "substantive response without authorized canonical value cannot resolve target disposition"
                )
            states_out.append({
                "empirical_universe_ref": universe_ref,
                "response_state": response_state,
                "canonical_response_value": canonical_value,
                "state_class": state_class,
                "product_target_disposition": disposition,
            })

        components_out.append({
            "target_ref": target_ref,
            "target_domain_ref": _canonical(component["target_domain_ref"]),
            "authority_bindings": sorted(authorities_out, key=lambda row: canonical_json(row["empirical_universe_ref"])),
            "state_bindings": sorted(states_out, key=lambda row: _state_key(
                row["empirical_universe_ref"], row["response_state"], row["canonical_response_value"]
            )),
        })

    normalized = {
        "contract_id": CONTRACT_ID,
        "world_scope": WORLD_SCOPE,
        "authority_phase": AUTHORITY_PHASE,
        "risk_set_ref": _canonical(raw["risk_set_ref"]),
        "components": sorted(components_out, key=lambda row: canonical_json(row["target_ref"])),
    }
    return MappingProxyType(normalized)


def contract_hash(contract: Mapping[str, Any]) -> str:
    return semantic_hash(normalize_contract(contract))


def component_for_target(contract: Mapping[str, Any], target_ref: Any) -> Mapping[str, Any]:
    normalized = normalize_contract(contract)
    key = canonical_json(target_ref)
    for component in normalized["components"]:
        if canonical_json(component["target_ref"]) == key:
            return component
    raise SourceStateDispositionContractError("exact target_ref absent from source-state contract")


def authority_binding_for_universe(component: Mapping[str, Any], universe_ref: Any) -> Mapping[str, Any]:
    key = canonical_json(universe_ref)
    for binding in component["authority_bindings"]:
        if canonical_json(binding["empirical_universe_ref"]) == key:
            return binding
    raise SourceStateDispositionContractError("exact universe authority binding unavailable")


def audit_observation(
    *,
    component: Mapping[str, Any],
    record_id: str,
    universe_ref: Any,
    event_ref: Any,
    opaque_raw_state_hash: str,
    response_state: str,
    canonical_response_value: Any,
    source_semantic_authority_ref: Any,
) -> Mapping[str, Any]:
    """Resolve one event without consulting its raw/native value.

    ``opaque_raw_state_hash`` participates in audit/replay identity only.  The
    only lookup key is the governed tuple (universe, response state, authorized
    canonical response value).
    """
    _text(record_id, "record_id")
    _text(opaque_raw_state_hash, "opaque_raw_state_hash")
    response_state = _text(response_state, "response_state")
    canonical_value = _canonical(canonical_response_value)
    universe = _canonical(universe_ref)
    key = _state_key(universe, response_state, canonical_value)
    selected = None
    for binding in component["state_bindings"]:
        if _state_key(
            binding["empirical_universe_ref"],
            binding["response_state"],
            binding["canonical_response_value"],
        ) == key:
            selected = binding
            break
    if selected is None:
        state_class = "SOURCE_UNKNOWN"
        disposition = UNRESOLVED
        binding_state = "NO_TARGET_SPECIFIC_BINDING"
    else:
        state_class = selected["state_class"]
        disposition = selected["product_target_disposition"]
        binding_state = "EXACT_TARGET_SPECIFIC_BINDING"

    return MappingProxyType({
        "record_id": record_id,
        "target_ref": _canonical(component["target_ref"]),
        "audit_trail": (
            MappingProxyType({
                "stage": RAW_SOURCE_STATE,
                "value": MappingProxyType({
                    "event_ref": _canonical(event_ref),
                    "opaque_raw_state_hash": opaque_raw_state_hash,
                }),
            }),
            MappingProxyType({
                "stage": SOURCE_LOCAL_GOVERNED_STATE,
                "value": MappingProxyType({
                    "empirical_universe_ref": universe,
                    "response_state": response_state,
                    "canonical_response_value": canonical_value,
                    "source_semantic_authority_ref": _canonical(source_semantic_authority_ref),
                    "state_class": state_class,
                    "binding_state": binding_state,
                }),
            }),
            MappingProxyType({
                "stage": PRODUCT_TARGET_DISPOSITION,
                "value": disposition,
            }),
        ),
    })


def unresolved_observation(*, record_id: str, target_ref: Any, reason: str) -> Mapping[str, Any]:
    """Create an explicit unresolved target observation without inventing source state."""
    record_id = _text(record_id, "record_id")
    reason = _text(reason, "reason")
    return MappingProxyType({
        "record_id": record_id,
        "target_ref": _canonical(target_ref),
        "audit_trail": (
            MappingProxyType({
                "stage": RAW_SOURCE_STATE,
                "value": MappingProxyType({"typed_absence": reason}),
            }),
            MappingProxyType({
                "stage": SOURCE_LOCAL_GOVERNED_STATE,
                "value": MappingProxyType({
                    "state_class": "SOURCE_UNKNOWN",
                    "binding_state": reason,
                }),
            }),
            MappingProxyType({
                "stage": PRODUCT_TARGET_DISPOSITION,
                "value": UNRESOLVED,
            }),
        ),
    })


def build_record_audit(record_id: str, observations: Iterable[Mapping[str, Any]]) -> Mapping[str, Any]:
    record_id = _text(record_id, "record_id")
    rows = tuple(sorted((_canonical(row) for row in observations), key=canonical_json))
    if not rows:
        # An exact denominator member without a target event is unresolved.  No
        # source meaning is manufactured to fill the absence.
        return MappingProxyType({
            "record_id": record_id,
            "observations": (),
            "resolved": False,
            "resolution_state": "TARGET_EVENT_UNAVAILABLE",
        })
    if any(row.get("record_id") != record_id for row in rows):
        raise SourceStateDispositionContractError("observation record_id mismatch")
    dispositions = [row["audit_trail"][2]["value"] for row in rows]
    resolved = all(value in {TARGET_MEMBER, RESOLVED_NON_TARGET} for value in dispositions)
    return MappingProxyType({
        "record_id": record_id,
        "observations": rows,
        "resolved": resolved,
        "resolution_state": "RESOLVED" if resolved else "UNRESOLVED",
    })


def denominator_resolution_check(
    *,
    contract: Mapping[str, Any],
    scope_identity: Mapping[str, Any],
    expected_record_ids: Iterable[str],
    record_audits: Iterable[Mapping[str, Any]],
) -> Mapping[str, Any]:
    normalized = normalize_contract(contract)
    expected = tuple(sorted(_text(value, "expected_record_id") for value in expected_record_ids))
    if len(expected) != len(set(expected)):
        raise SourceStateDispositionContractError("expected record ids contain duplicates")
    audits = tuple(sorted((_canonical(row) for row in record_audits), key=lambda row: row["record_id"]))
    actual = tuple(row["record_id"] for row in audits)
    if len(actual) != len(set(actual)):
        raise SourceStateDispositionContractError("record audit ids contain duplicates")
    if actual != expected:
        raise SourceStateDispositionContractError(
            "denominator accounting does not cover exactly all expected record ids"
        )
    unresolved = tuple(row["record_id"] for row in audits if not row["resolved"])
    raw_denominator = len(expected)
    raw_resolved = raw_denominator - len(unresolved)
    payload = {
        "stage": DENOMINATOR_RESOLUTION_CHECK,
        "contract_hash": semantic_hash(normalized),
        "scope_identity": _canonical(scope_identity),
        "expected_record_ids": list(expected),
        "record_audits": list(audits),
        "unresolved_record_ids": list(unresolved),
        "raw_denominator_support": raw_denominator,
        "raw_resolved_target_support": raw_resolved,
        "passed": not unresolved and raw_resolved == raw_denominator,
    }
    payload["check_hash"] = semantic_hash(payload)
    return MappingProxyType(payload)


def empirical_result_receipt(
    *,
    contract: Mapping[str, Any],
    denominator_checks: Iterable[Mapping[str, Any]],
    query_ref: Any,
    release_refs: Iterable[Any],
    fact_rows: Iterable[Mapping[str, Any]],
) -> Mapping[str, Any]:
    normalized = normalize_contract(contract)
    checks = tuple(sorted((_canonical(row) for row in denominator_checks), key=canonical_json))
    if not checks:
        raise SourceStateDispositionContractError("at least one denominator check is required")
    if any(not row["passed"] for row in checks):
        raise SourceStateDispositionContractError(
            "EMPIRICAL_RESULT is forbidden before all denominator-resolution checks pass"
        )
    facts = tuple(sorted((_canonical(row) for row in fact_rows), key=canonical_json))
    for row in facts:
        if row.get("typed_state") == "SUPPORTED":
            if row.get("raw_resolved_target_support") != row.get("raw_denominator_support"):
                raise SourceStateDispositionContractError(
                    "resolved empirical fact violates raw_resolved_target_support == raw_denominator_support"
                )
    payload = {
        "stage": EMPIRICAL_RESULT,
        "contract_hash": semantic_hash(normalized),
        "query_ref": _canonical(query_ref),
        "release_refs": sorted((_canonical(ref) for ref in release_refs), key=canonical_json),
        "denominator_check_hashes": sorted(row["check_hash"] for row in checks),
        "facts": list(facts),
    }
    payload["result_hash"] = semantic_hash(payload)
    return MappingProxyType(payload)


def replay_identity(
    *,
    contract: Mapping[str, Any],
    denominator_checks: Iterable[Mapping[str, Any]],
    empirical_result: Mapping[str, Any],
) -> str:
    normalized = normalize_contract(contract)
    material = {
        "contract_hash": semantic_hash(normalized),
        "source_state_bindings": [
            {
                "target_ref": component["target_ref"],
                "state_bindings": component["state_bindings"],
                "authority_bindings": component["authority_bindings"],
            }
            for component in normalized["components"]
        ],
        "denominator_ledger": sorted((_canonical(row) for row in denominator_checks), key=canonical_json),
        "empirical_result": _canonical(empirical_result),
    }
    return semantic_hash(material)


__all__ = [
    "CONTRACT_ID", "WORLD_SCOPE", "AUTHORITY_PHASE",
    "RAW_SOURCE_STATE", "SOURCE_LOCAL_GOVERNED_STATE", "PRODUCT_TARGET_DISPOSITION",
    "DENOMINATOR_RESOLUTION_CHECK", "EMPIRICAL_RESULT",
    "TARGET_MEMBER", "RESOLVED_NON_TARGET", "UNRESOLVED",
    "DISPOSITIONS", "STATE_CLASSES", "SourceStateDispositionContractError",
    "ContractExecutionReceipt", "canonical_json", "semantic_hash", "normalize_contract",
    "contract_hash", "component_for_target", "authority_binding_for_universe",
    "audit_observation", "unresolved_observation", "build_record_audit", "denominator_resolution_check",
    "empirical_result_receipt", "replay_identity",
]
