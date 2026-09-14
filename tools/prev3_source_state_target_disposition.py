"""Source-agnostic PRE-V3 source-state -> product-disposition contract.

This helper is deliberately semantic-source neutral. Raw native values are
opaque observations. Meaning enters only through exact, content-addressed
source-local authority; denominator membership enters only through exact
pre-query routing/risk-set authority; product target membership enters only
through exact target-use authority.
"""
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
import hashlib
import json
import re
from typing import Any, Mapping, Sequence

CONTRACT_ID = "PREV3_EMPIRICAL_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_CONTRACT_R1"

RAW_SOURCE_STATE = "RAW_SOURCE_STATE"
SOURCE_LOCAL_GOVERNED_STATE = "SOURCE_LOCAL_GOVERNED_STATE"
PRODUCT_TARGET_DISPOSITION = "PRODUCT_TARGET_DISPOSITION"
DENOMINATOR_RESOLUTION_CHECK = "DENOMINATOR_RESOLUTION_CHECK"
EMPIRICAL_RESULT = "EMPIRICAL_RESULT"

SOURCE_SUBSTANTIVE = "SOURCE_SUBSTANTIVE"
TYPED_MISSING_NONRESPONSE = "TYPED_MISSING_NONRESPONSE"
SOURCE_NOT_APPLICABLE_OR_INELIGIBLE = "SOURCE_NOT_APPLICABLE_OR_INELIGIBLE"
SOURCE_SPECIFIC_SPECIAL = "SOURCE_SPECIFIC_SPECIAL"
SOURCE_UNKNOWN = "SOURCE_UNKNOWN"
SOURCE_STATE_CLASSES = frozenset({
    SOURCE_SUBSTANTIVE,
    TYPED_MISSING_NONRESPONSE,
    SOURCE_NOT_APPLICABLE_OR_INELIGIBLE,
    SOURCE_SPECIFIC_SPECIAL,
    SOURCE_UNKNOWN,
})

TARGET_MEMBER = "TARGET_MEMBER"
RESOLVED_NON_TARGET = "RESOLVED_NON_TARGET"
PRODUCT_TYPED_MISSING_NONRESPONSE = "TYPED_MISSING_NONRESPONSE"
PRODUCT_NOT_APPLICABLE_OR_INELIGIBLE = "NOT_APPLICABLE_OR_INELIGIBLE"
AUTHORIZED_PREQUERY_EXCLUSION = "AUTHORIZED_PREQUERY_EXCLUSION"
UNRESOLVED = "UNRESOLVED"
PRODUCT_DISPOSITIONS = frozenset({
    TARGET_MEMBER,
    RESOLVED_NON_TARGET,
    PRODUCT_TYPED_MISSING_NONRESPONSE,
    PRODUCT_NOT_APPLICABLE_OR_INELIGIBLE,
    AUTHORIZED_PREQUERY_EXCLUSION,
    UNRESOLVED,
})

TARGET_DOMAIN_MEMBER = "TARGET_DOMAIN_MEMBER"
TARGET_DOMAIN_RESOLVED_COMPLEMENT = "TARGET_DOMAIN_RESOLVED_COMPLEMENT"
MISSING_NONRESPONSE_BINDING = "MISSING_NONRESPONSE_BINDING"
NOT_APPLICABLE_OR_INELIGIBLE_BINDING = "NOT_APPLICABLE_OR_INELIGIBLE_BINDING"
PREQUERY_ELIGIBILITY_EXCLUSION_BINDING = "PREQUERY_ELIGIBILITY_EXCLUSION_BINDING"
NO_COMPETENT_BINDING = "NO_COMPETENT_BINDING"
DISPOSITION_BASES = {
    TARGET_MEMBER: TARGET_DOMAIN_MEMBER,
    RESOLVED_NON_TARGET: TARGET_DOMAIN_RESOLVED_COMPLEMENT,
    PRODUCT_TYPED_MISSING_NONRESPONSE: MISSING_NONRESPONSE_BINDING,
    PRODUCT_NOT_APPLICABLE_OR_INELIGIBLE: NOT_APPLICABLE_OR_INELIGIBLE_BINDING,
    AUTHORIZED_PREQUERY_EXCLUSION: PREQUERY_ELIGIBILITY_EXCLUSION_BINDING,
    UNRESOLVED: NO_COMPETENT_BINDING,
}

DENOMINATOR_MEMBER = "DENOMINATOR_MEMBER"
PREQUERY_EXCLUDED = "PREQUERY_EXCLUDED"
ELIGIBILITY_UNRESOLVED = "ELIGIBILITY_UNRESOLVED"
ELIGIBILITY_DECISIONS = frozenset({DENOMINATOR_MEMBER, PREQUERY_EXCLUDED, ELIGIBILITY_UNRESOLVED})

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ContractError(ValueError):
    """The supplied authority/binding material cannot satisfy the contract."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} must be non-empty text")
    return value.strip()


def _sha(value: Any, name: str) -> str:
    value = _text(value, name)
    if not SHA256_RE.fullmatch(value):
        raise ContractError(f"{name} must be lowercase sha256")
    return value


def canonicalize(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        raise ContractError("binary float is forbidden in deterministic identity material")
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ContractError("non-finite Decimal is forbidden")
        return {"$exact_decimal": format(value.normalize(), "f")}
    if isinstance(value, Fraction):
        return {"$exact_fraction": [value.numerator, value.denominator]}
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise ContractError("identity mapping keys must be strings")
        return {k: canonicalize(value[k]) for k in sorted(value)}
    if isinstance(value, (set, frozenset)):
        values = [canonicalize(v) for v in value]
        return sorted(values, key=canonical_json)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [canonicalize(v) for v in value]
    raise ContractError(f"unsupported identity material: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(canonicalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def semantic_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def validate_authority_ref(value: Any, *, expected_kind: str, name: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be an exact authority mapping")
    required = {"authority_id", "authority_version", "authority_content_hash", "authority_kind"}
    if set(value) != required:
        raise ContractError(f"{name} must contain exactly {sorted(required)!r}")
    result = {
        "authority_id": _text(value["authority_id"], f"{name}.authority_id"),
        "authority_version": _text(value["authority_version"], f"{name}.authority_version"),
        "authority_content_hash": _sha(value["authority_content_hash"], f"{name}.authority_content_hash"),
        "authority_kind": _text(value["authority_kind"], f"{name}.authority_kind"),
    }
    if result["authority_kind"] != expected_kind:
        raise ContractError(f"{name}.authority_kind must be {expected_kind}")
    forbidden = {"LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER_FALLBACK", "*"}
    if result["authority_id"].upper() in forbidden or result["authority_version"].upper() in forbidden:
        raise ContractError(f"{name} may not use mutable/fuzzy authority selection")
    return result


def validate_exact_ref(value: Any, name: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{name} must be an exact reference mapping")
    required = {"kind", "object_id", "content_hash"}
    if set(value) != required:
        raise ContractError(f"{name} must contain exactly {sorted(required)!r}")
    return {
        "kind": _text(value["kind"], f"{name}.kind"),
        "object_id": _text(value["object_id"], f"{name}.object_id"),
        "content_hash": _sha(value["content_hash"], f"{name}.content_hash"),
    }


def _authority_key(ref: Mapping[str, str]) -> str:
    return canonical_json(ref)


def validate_query_envelope(payload: Mapping[str, Any]) -> dict[str, Any]:
    envelope = payload.get("query_envelope")
    if not isinstance(envelope, Mapping):
        raise ContractError("query_envelope must be a mapping")
    if envelope.get("world_scope") != "OBJECTIVE":
        raise ContractError("PRE-V3 contract is objective-world only")
    if envelope.get("authority_phase") != "FROZEN_PRE_OUTCOME":
        raise ContractError("query authority must be frozen before outcome binding")
    expected = envelope.get("expected_record_ids")
    if not isinstance(expected, Sequence) or isinstance(expected, (str, bytes, bytearray)) or not expected:
        raise ContractError("expected_record_ids must be a non-empty sequence")
    expected_ids = tuple(sorted(_text(x, "expected_record_id") for x in expected))
    if len(expected_ids) != len(set(expected_ids)):
        raise ContractError("expected_record_ids contains duplicates")

    source_refs_raw = envelope.get("source_semantic_authority_refs")
    if not isinstance(source_refs_raw, Sequence) or isinstance(source_refs_raw, (str, bytes, bytearray)) or not source_refs_raw:
        raise ContractError("source_semantic_authority_refs must be a non-empty sequence")
    source_refs = tuple(sorted(
        (validate_authority_ref(x, expected_kind="SOURCE_SEMANTICS_TOPOLOGY", name="source_semantic_authority_ref") for x in source_refs_raw),
        key=_authority_key,
    ))
    if len({_authority_key(x) for x in source_refs}) != len(source_refs):
        raise ContractError("duplicate source semantic authority ref")

    result = {
        "query_id": _text(envelope.get("query_id"), "query_id"),
        "target_id": _text(envelope.get("target_id"), "target_id"),
        "world_scope": "OBJECTIVE",
        "authority_phase": "FROZEN_PRE_OUTCOME",
        "expected_record_ids": expected_ids,
        "source_semantic_authority_refs": source_refs,
        "target_authority_ref": validate_authority_ref(envelope.get("target_authority_ref"), expected_kind="TARGET_USE_PERMISSION", name="target_authority_ref"),
        "risk_set_authority_ref": validate_authority_ref(envelope.get("risk_set_authority_ref"), expected_kind="ROUTING_RISK_SET", name="risk_set_authority_ref"),
        "replay_authority_ref": validate_authority_ref(envelope.get("replay_authority_ref"), expected_kind="REPLAY_PROTOCOL", name="replay_authority_ref"),
        "target_domain_ref": validate_exact_ref(envelope.get("target_domain_ref"), "target_domain_ref"),
        "risk_set_ref": validate_exact_ref(envelope.get("risk_set_ref"), "risk_set_ref"),
    }
    result["query_envelope_hash"] = semantic_hash({"contract_id": CONTRACT_ID, **result})
    supplied_hash = envelope.get("query_envelope_hash")
    if supplied_hash is not None and _sha(supplied_hash, "query_envelope_hash") != result["query_envelope_hash"]:
        raise ContractError("query_envelope_hash does not match frozen query material")
    return result


def _audit_record(record: Mapping[str, Any], envelope: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(record, Mapping):
        raise ContractError("record must be a mapping")
    record_id = _text(record.get("record_id"), "record_id")
    raw = record.get("raw_source_state")
    if not isinstance(raw, Mapping) or "native_state" not in raw:
        raise ContractError(f"{record_id}: raw_source_state with native_state is required")
    raw_normalized = {
        "source_id": _text(raw.get("source_id"), f"{record_id}.source_id"),
        "native_state": canonicalize(raw["native_state"]),
    }

    governed = record.get("source_local_governed_state")
    if not isinstance(governed, Mapping):
        raise ContractError(f"{record_id}: source_local_governed_state must be a mapping")
    state_class = governed.get("state_class")
    if state_class not in SOURCE_STATE_CLASSES:
        raise ContractError(f"{record_id}: invalid source-local state_class")
    source_auth = validate_authority_ref(governed.get("authority_ref"), expected_kind="SOURCE_SEMANTICS_TOPOLOGY", name=f"{record_id}.source_authority_ref")
    accepted_source_keys = {_authority_key(x) for x in envelope["source_semantic_authority_refs"]}
    if _authority_key(source_auth) not in accepted_source_keys:
        raise ContractError(f"{record_id}: source authority is outside the frozen query authority manifest")
    governed_normalized = {
        "semantic_state": _text(governed.get("semantic_state"), f"{record_id}.semantic_state"),
        "state_class": state_class,
        "authority_ref": source_auth,
    }
    source_binding_hash = semantic_hash({
        "contract_id": CONTRACT_ID,
        "record_id": record_id,
        "raw_source_state": raw_normalized,
        "source_local_governed_state": governed_normalized,
    })

    eligibility = record.get("prequery_eligibility")
    if not isinstance(eligibility, Mapping):
        raise ContractError(f"{record_id}: prequery_eligibility must be a mapping")
    decision = eligibility.get("decision")
    if decision not in ELIGIBILITY_DECISIONS:
        raise ContractError(f"{record_id}: invalid prequery eligibility decision")
    if eligibility.get("phase") != "PRE_QUERY":
        raise ContractError(f"{record_id}: denominator eligibility must be PRE_QUERY")
    risk_auth = validate_authority_ref(eligibility.get("authority_ref"), expected_kind="ROUTING_RISK_SET", name=f"{record_id}.eligibility_authority_ref")
    if risk_auth != envelope["risk_set_authority_ref"]:
        raise ContractError(f"{record_id}: eligibility authority differs from frozen risk-set authority")
    risk_set_ref = validate_exact_ref(eligibility.get("risk_set_ref"), f"{record_id}.risk_set_ref")
    if risk_set_ref != envelope["risk_set_ref"]:
        raise ContractError(f"{record_id}: risk_set_ref differs from frozen query risk set")
    basis_ref = validate_exact_ref(eligibility.get("basis_ref"), f"{record_id}.eligibility_basis_ref")
    eligibility_normalized = {
        "decision": decision,
        "phase": "PRE_QUERY",
        "authority_ref": risk_auth,
        "risk_set_ref": risk_set_ref,
        "basis_ref": basis_ref,
    }

    product = record.get("product_target_disposition")
    if not isinstance(product, Mapping):
        raise ContractError(f"{record_id}: product_target_disposition must be a mapping")
    disposition = product.get("disposition")
    if disposition not in PRODUCT_DISPOSITIONS:
        raise ContractError(f"{record_id}: invalid product target disposition")
    basis = product.get("resolution_basis")
    if basis != DISPOSITION_BASES[disposition]:
        raise ContractError(f"{record_id}: disposition/resolution_basis mismatch")
    target_auth = validate_authority_ref(product.get("authority_ref"), expected_kind="TARGET_USE_PERMISSION", name=f"{record_id}.target_authority_ref")
    if target_auth != envelope["target_authority_ref"]:
        raise ContractError(f"{record_id}: target authority differs from frozen query target authority")
    target_domain_ref = validate_exact_ref(product.get("target_domain_ref"), f"{record_id}.target_domain_ref")
    if target_domain_ref != envelope["target_domain_ref"]:
        raise ContractError(f"{record_id}: target domain differs from frozen query target domain")

    if state_class in {SOURCE_SPECIFIC_SPECIAL, SOURCE_UNKNOWN} and disposition != UNRESOLVED:
        raise ContractError(f"{record_id}: source-special/unknown state cannot receive a positive universal disposition")
    if decision == PREQUERY_EXCLUDED and disposition != AUTHORIZED_PREQUERY_EXCLUSION:
        raise ContractError(f"{record_id}: pre-query exclusion must carry AUTHORIZED_PREQUERY_EXCLUSION")
    if decision != PREQUERY_EXCLUDED and disposition == AUTHORIZED_PREQUERY_EXCLUSION:
        raise ContractError(f"{record_id}: target disposition cannot delete a denominator member")

    product_normalized = {
        "disposition": disposition,
        "resolution_basis": basis,
        "authority_ref": target_auth,
        "target_domain_ref": target_domain_ref,
    }
    target_binding_hash = semantic_hash({
        "contract_id": CONTRACT_ID,
        "record_id": record_id,
        "source_binding_hash": source_binding_hash,
        "product_target_disposition": product_normalized,
    })

    return {
        "record_id": record_id,
        "audit_trail": [
            {"stage": RAW_SOURCE_STATE, "value": raw_normalized},
            {"stage": SOURCE_LOCAL_GOVERNED_STATE, "value": governed_normalized, "binding_hash": source_binding_hash},
            {"stage": PRODUCT_TARGET_DISPOSITION, "value": product_normalized, "binding_hash": target_binding_hash},
        ],
        "prequery_eligibility": eligibility_normalized,
    }


def audit_record(record: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and audit one record against one frozen query envelope."""
    return _audit_record(record, validate_query_envelope(payload))


def denominator_resolution_check(payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ContractError("payload must be a mapping")
    envelope = validate_query_envelope(payload)
    records = payload.get("records")
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes, bytearray)):
        raise ContractError("records must be a sequence")
    audited = [_audit_record(record, envelope) for record in records]
    ids = [item["record_id"] for item in audited]
    if len(ids) != len(set(ids)):
        raise ContractError("records contain duplicate record_id")
    if tuple(sorted(ids)) != envelope["expected_record_ids"]:
        raise ContractError("records do not exactly account for the frozen expected_record_ids")
    audited = sorted(audited, key=lambda item: item["record_id"])

    denominator_ids: list[str] = []
    excluded_ids: list[str] = []
    unresolved_ids: list[str] = []
    numerator_ids: list[str] = []
    resolved_non_target_ids: list[str] = []

    for item in audited:
        record_id = item["record_id"]
        decision = item["prequery_eligibility"]["decision"]
        disposition = item["audit_trail"][2]["value"]["disposition"]
        if decision == PREQUERY_EXCLUDED:
            excluded_ids.append(record_id)
            continue
        if decision == ELIGIBILITY_UNRESOLVED:
            unresolved_ids.append(record_id)
            continue
        denominator_ids.append(record_id)
        if disposition == TARGET_MEMBER:
            numerator_ids.append(record_id)
        elif disposition == RESOLVED_NON_TARGET:
            resolved_non_target_ids.append(record_id)
        else:
            unresolved_ids.append(record_id)

    resolved_support = len(numerator_ids) + len(resolved_non_target_ids)
    passed = not unresolved_ids and resolved_support == len(denominator_ids)
    ledger = {
        "expected_record_ids": list(envelope["expected_record_ids"]),
        "denominator_member_ids": denominator_ids,
        "authorized_prequery_exclusion_ids": excluded_ids,
        "unresolved_record_ids": sorted(set(unresolved_ids)),
        "target_member_ids": numerator_ids,
        "resolved_non_target_ids": resolved_non_target_ids,
        "raw_denominator_support": len(denominator_ids),
        "raw_resolved_target_support": resolved_support,
    }
    gate_hash = semantic_hash({
        "contract_id": CONTRACT_ID,
        "query_envelope_hash": envelope["query_envelope_hash"],
        "ledger": ledger,
        "audited_records": audited,
    })
    return {
        "stage": DENOMINATOR_RESOLUTION_CHECK,
        "contract_id": CONTRACT_ID,
        "query_envelope_hash": envelope["query_envelope_hash"],
        "passed": passed,
        "ledger": ledger,
        "audited_records": audited,
        "gate_hash": gate_hash,
    }


def emit_empirical_result(payload: Mapping[str, Any]) -> dict[str, Any]:
    gate = denominator_resolution_check(payload)
    if not gate["passed"]:
        raise ContractError(
            "EMPIRICAL_RESULT forbidden: denominator members are not completely resolved; "
            f"unresolved={gate['ledger']['unresolved_record_ids']!r}"
        )
    denominator = gate["ledger"]["raw_denominator_support"]
    numerator = len(gate["ledger"]["target_member_ids"])
    value = None if denominator == 0 else Fraction(numerator, denominator)
    result_material = {
        "contract_id": CONTRACT_ID,
        "query_envelope_hash": gate["query_envelope_hash"],
        "gate_hash": gate["gate_hash"],
        "numerator": numerator,
        "denominator": denominator,
        "value": value,
        "ledger": gate["ledger"],
    }
    return {
        "stage": EMPIRICAL_RESULT,
        **result_material,
        "result_hash": semantic_hash(result_material),
        "audited_records": gate["audited_records"],
    }
