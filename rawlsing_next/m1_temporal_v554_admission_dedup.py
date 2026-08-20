#!/usr/bin/env python3
"""Pure fail-closed runtime for frozen SCR553/SCR554 M1 ingress semantics."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib, json, re
from typing import Any, Mapping, Sequence

M1_CONTRACT_ID = "M1_TEMPORAL_V554_INGRESS_SEAM@1.0.0"
SCR554_CONTRACT_ID = "SCR554_V554_BASIS_DEDUP_AFFORDANCE_EXACT_CONTRACT@1.0.0"
TARGET_USE = "STRUCTURAL_MEDIATION_INPUT"
SIG_001 = "V554-SIG-001-NONTEMPORAL-EXACT"
SIG_002 = "V554-SIG-002-TEMPORAL-POINT-EXACT"
SIG_003 = "V554-SIG-003-TEMPORAL-RELATIONAL-EXACT"
SIGS = {SIG_001, SIG_002, SIG_003}
SHA = re.compile(r"^[0-9a-f]{64}$")

EQ_FIELDS = (
    "focal_structural_proposition_ref", "target_use", "v554_rule_id",
    "v554_rule_version", "v554_rule_hash",
    "rule_relevant_structural_semantic_identity_fingerprint",
    "native_scope_identity_fingerprint",
    "rule_relevant_effective_time_semantics_fingerprint",
    "originating_structural_empirical_admission_lineage_fingerprint",
    "source_universe_fingerprint", "estimand_fingerprint",
    "measure_and_weight_authority_fingerprint",
    "rule_relevant_source_relation_comparability_authority_fingerprint",
    "interpretation_critical_semantic_authority_fingerprint",
)
DIRECT_SLOTS = (
    "structural_empirical_admission_id", "structural_empirical_admission_content_hash",
    "admission_authority_id", "admission_authority_version", "admission_authority_hash",
    "admission_decision_state", "focal_structural_proposition_ref",
    "structural_semantic_identity_refs", "native_scope_identity_refs",
    "target_use_permission_refs", "effective_time_or_interval_refs_required_by_target_use",
    "source_universe_refs", "estimand_refs", "measure_and_weight_authority_refs",
    "applicable_negative_denial_noncomparability_refs", "interpretation_critical_authority_refs",
    "producer_replay_locator_or_reference_root",
)
V553_SLOTS = (
    "v553_object_id", "v553_object_content_hash", "v553_object_family",
    "originating_structural_empirical_admission_refs", "focal_structural_proposition_ref",
    "rule_relevant_temporal_semantic_refs", "native_scope_identity_refs",
    "source_universe_refs", "estimand_refs", "measure_and_weight_authority_refs",
    "source_relation_comparability_authority_refs_where_required",
    "applicable_temporal_limit_negative_refs", "interpretation_critical_authority_refs",
    "producer_replay_locator_or_reference_root",
)
SCR553_STATES = {
    "V553_REQUIRED", "V553_NOT_REQUIRED_FOR_THIS_USE", "V553_NEGATIVE_LIMIT_ONLY",
    "NO_POSITIVE_V553_OUTPUT__ADMISSION_NOT_POSITIVE",
    "NO_POSITIVE_V553_OUTPUT__MISSING_TEMPORAL_AUTHORITY",
    "NO_POSITIVE_V553_OUTPUT__MISSING_COMPARABILITY_AUTHORITY",
    "NO_POSITIVE_V553_OUTPUT__OUT_OF_JURISDICTION",
    "REJECT_NO_V553_OBJECT__INVALID_OR_FORBIDDEN_INTAKE",
}
CONDITION_DISPOSITION = {
    "K01": "DEFERRED", "K02": "DEFERRED", "K03": "DEFERRED",
    "K04": "INFORMATIONAL", "K05": "HARD_BLOCK", "K06": "HARD_BLOCK",
    "K07": "HARD_BLOCK", "K08": "HARD_BLOCK", "K09": "HARD_BLOCK",
}

class BasisKind(str, Enum):
    DIRECT = "DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION"
    V553 = "V553_TEMPORAL_OBJECT"

class TemporalCompleteness(str, Enum):
    COMPLETE_FOR_DIRECT_V554 = "COMPLETE_FOR_DIRECT_V554"
    REQUIRES_V553_OWNED_TEMPORAL_MEANING = "REQUIRES_V553_OWNED_TEMPORAL_MEANING"
    BLOCKED_BY_APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE = "BLOCKED_BY_APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE"
    UNKNOWN_FAIL_CLOSED = "UNKNOWN_FAIL_CLOSED"
    NOT_APPLICABLE_TO_TARGET_USE = "NOT_APPLICABLE_TO_TARGET_USE"

class M1DecisionState(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    VALID_EMPTY = "VALID_EMPTY"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"
    INELIGIBLE_EXPLICIT_DENIAL = "INELIGIBLE_EXPLICIT_DENIAL"
    INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY = "INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY"
    INELIGIBLE_MISSING_REQUIRED_AUTHORITY = "INELIGIBLE_MISSING_REQUIRED_AUTHORITY"
    INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY = "INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY"
    INELIGIBLE_TEMPORAL_SIGNATURE = "INELIGIBLE_TEMPORAL_SIGNATURE"
    EQUIVALENCE_UNKNOWN = "EQUIVALENCE_UNKNOWN"

@dataclass(frozen=True)
class M1Evaluation:
    contract_id: str
    decision_state: M1DecisionState
    reason: str
    governed_use_id: str
    required_basis_kind: str | None
    support_count: int
    canonical_basis_semantic_id: str | None
    f1: Mapping[str, Any] | None
    f2: tuple[Mapping[str, Any], ...]
    b1: Mapping[str, Any] | None
    direct_v557_handoff: Mapping[str, Any] | None
    rejected_or_reference_only_basis_refs: tuple[str, ...]

class Integrity(ValueError): pass
class EquivalenceUnknown(ValueError): pass

def _nonempty(v: Any, name: str) -> str:
    if not isinstance(v, str) or not v.strip(): raise Integrity(f"{name} must be non-empty")
    return v.strip()

def _sha(v: Any, name: str) -> str:
    v = _nonempty(v, name)
    if not SHA.fullmatch(v): raise Integrity(f"{name} must be lowercase sha256")
    return v

def _jsonable(v: Any) -> Any:
    if v is None or isinstance(v, (str, bool, int)): return v
    if isinstance(v, float): raise Integrity("floats forbidden in semantic identity")
    if isinstance(v, Enum): return v.value
    if isinstance(v, Mapping):
        if any(not isinstance(k, str) for k in v): raise Integrity("JSON keys must be strings")
        return {k: _jsonable(x) for k, x in v.items()}
    if isinstance(v, Sequence) and not isinstance(v, (str, bytes, bytearray)):
        return [_jsonable(x) for x in v]
    raise Integrity(f"unsupported identity type {type(v).__name__}")

def canonical_json(v: Any) -> str:
    return json.dumps(_jsonable(v), sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def semantic_hash(v: Any) -> str:
    return hashlib.sha256(canonical_json(v).encode()).hexdigest()

def _urn(family: str, v: Any) -> str:
    return f"urn:rawlsing:{family}:sha256:{semantic_hash(v)}"

def _seq(v: Any, name: str) -> tuple[str, ...]:
    if isinstance(v, (str, bytes)) or not isinstance(v, Sequence): raise Integrity(f"{name} must be sequence")
    return tuple(_nonempty(x, name) for x in v)

def _rule(v: Any, name: str = "v554_rule_ref") -> dict[str, str]:
    if not isinstance(v, Mapping): raise Integrity(f"{name} must be mapping")
    return {"id": _nonempty(v.get("id"), f"{name}.id"), "version": _nonempty(v.get("version"), f"{name}.version"), "hash": _sha(v.get("hash"), f"{name}.hash")}

def _exact_ref(v: Any, name: str) -> dict[str, str]:
    if not isinstance(v, Mapping): raise Integrity(f"{name} must be mapping")
    return {"kind": _nonempty(v.get("kind"), f"{name}.kind"), "object_id": _nonempty(v.get("object_id"), f"{name}.object_id"), "content_hash": _sha(v.get("content_hash"), f"{name}.content_hash")}

def _eq(v: Any) -> dict[str, Any]:
    if not isinstance(v, Mapping): raise EquivalenceUnknown("equivalence key missing")
    if set(v) != set(EQ_FIELDS): raise EquivalenceUnknown("equivalence key fields unresolved")
    out = dict(v)
    for k in EQ_FIELDS:
        if out[k] in (None, "", [], {}): raise EquivalenceUnknown(f"equivalence component unresolved: {k}")
        canonical_json(out[k])
    return out

def _candidate(v: Any) -> dict[str, Any]:
    if not isinstance(v, Mapping): raise Integrity("candidate must be mapping")
    try: kind = BasisKind(_nonempty(v.get("basis_kind"), "basis_kind"))
    except ValueError as e: raise Integrity("unknown basis kind") from e
    ref = _exact_ref(v.get("basis_ref"), "basis_ref")
    projection = v.get("projection")
    if not isinstance(projection, Mapping): raise Integrity("projection must be mapping")
    if semantic_hash(projection) != _sha(v.get("projection_hash"), "projection_hash"): raise Integrity("candidate projection hash mismatch")
    slots = DIRECT_SLOTS if kind is BasisKind.DIRECT else V553_SLOTS
    missing = [x for x in slots if x not in projection]
    if missing: raise Integrity(f"basis projection missing SCR554 consumer slots: {missing!r}")
    canonical_json({x: projection[x] for x in slots})
    if kind is BasisKind.DIRECT:
        _nonempty(projection["structural_empirical_admission_id"], "admission id")
        _sha(projection["structural_empirical_admission_content_hash"], "admission content hash")
        _sha(projection["admission_authority_hash"], "admission authority hash")
    else:
        _nonempty(projection["v553_object_id"], "v553 object id")
        _sha(projection["v553_object_content_hash"], "v553 content hash")
        _nonempty(projection["v553_object_family"], "v553 family")
    semantics = v.get("selected_rule_relevant_basis_semantics")
    if semantics in (None, "", [], {}): raise Integrity("selected rule-relevant semantics missing")
    canonical_json(semantics)
    families = _seq(v.get("v553_families", ()), "v553_families") if v.get("v553_families") else ()
    return {"basis_kind": kind, "basis_ref": ref, "projection": dict(projection), "equivalence_key": _eq(v.get("equivalence_key")), "semantics": semantics, "families": families, "relation_refs": bool(v.get("all_relation_required_support_limit_refs", False))}

def _condition(v: Any) -> dict[str, Any]:
    if not isinstance(v, Mapping): raise Integrity("condition must be mapping")
    kind = _nonempty(v.get("condition_kind_id"), "condition_kind_id")
    if kind not in CONDITION_DISPOSITION: raise Integrity("condition kind must be K01..K09")
    return {
        "candidate_semantic_key": _nonempty(v.get("candidate_semantic_key"), "candidate_semantic_key"),
        "condition_kind_id": kind, "predicate_id": _nonempty(v.get("predicate_id"), "predicate_id"),
        "predicate_version": _nonempty(v.get("predicate_version"), "predicate_version"),
        "semantic_owner": _nonempty(v.get("semantic_owner"), "semantic_owner"),
        "resolution_owner": _nonempty(v.get("resolution_owner"), "resolution_owner"),
        "binding_producer": _nonempty(v.get("binding_producer"), "binding_producer"),
        "evaluator_owner": _nonempty(v.get("evaluator_owner"), "evaluator_owner"),
        "canonical_argument_envelope_fingerprint": _nonempty(v.get("canonical_argument_envelope_fingerprint"), "argument fingerprint"),
        "producer_negative_or_requirement_refs": sorted(set(_seq(v.get("producer_negative_or_requirement_refs", ()), "negative refs"))),
    }

def _publication(v: Any) -> dict[str, Any] | None:
    if v is None: return None
    if not isinstance(v, Mapping): raise Integrity("publication_authority must be mapping")
    return {"authority_id": _nonempty(v.get("authority_id"), "publication id"), "authority_version": _nonempty(v.get("authority_version"), "publication version"), "authority_hash": _sha(v.get("authority_hash"), "publication hash"), "producer": _nonempty(v.get("producer"), "producer"), "publisher": _nonempty(v.get("publisher"), "publisher"), "governed_use_id": _nonempty(v.get("governed_use_id"), "publication use"), "rule_ref": _rule(v.get("rule_ref"), "publication rule"), "decision": _nonempty(v.get("decision"), "publication decision"), "allowed_object_families": tuple(sorted(set(_seq(v.get("allowed_object_families", ()), "allowed families"))))}

def _parse(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, Mapping): raise Integrity("invocation must be mapping")
    if _nonempty(payload.get("use_owner"), "use_owner") != "V554": raise Integrity("use_owner must be V554")
    if _nonempty(payload.get("target_use"), "target_use") != TARGET_USE: raise Integrity("unsupported target use")
    sig = _nonempty(payload.get("signature_id"), "signature_id")
    if sig not in SIGS: raise Integrity("unknown signature")
    try: tc = TemporalCompleteness(_nonempty(payload.get("temporal_completeness"), "temporal_completeness"))
    except ValueError as e: raise Integrity("unknown temporal completeness") from e
    scr = _nonempty(payload.get("scr553_decision_state"), "scr553_decision_state")
    if scr not in SCR553_STATES: raise Integrity("unknown SCR553 decision")
    candidates = payload.get("candidates", ()); conditions = payload.get("conditions", ())
    if isinstance(candidates, (str, bytes)) or not isinstance(candidates, Sequence): raise Integrity("candidates must be sequence")
    if isinstance(conditions, (str, bytes)) or not isinstance(conditions, Sequence): raise Integrity("conditions must be sequence")
    origins = tuple(sorted(set(_seq(payload.get("originating_admission_refs", ()), "originating_admission_refs"))))
    snapshots = tuple(sorted(set(_seq(payload.get("required_authority_snapshot_refs", ()), "authority snapshots"))))
    if not origins or not snapshots: raise Integrity("originating admissions and authority snapshots required")
    auth = payload.get("authority_bundle_material")
    if not isinstance(auth, Mapping) or not auth: raise Integrity("authority_bundle_material required")
    canonical_json(auth)
    return {
        "use": _nonempty(payload.get("governed_use_id"), "governed_use_id"), "rule": _rule(payload.get("v554_rule_ref")),
        "sig": sig, "prop": _nonempty(payload.get("focal_structural_proposition_ref"), "focal proposition"),
        "origins": origins, "scr": scr, "scr_ref": _exact_ref(payload.get("scr553_request_ref"), "scr553_request_ref"),
        "ops": _seq(payload.get("required_temporal_operations", ()), "required_temporal_operations"), "snapshots": snapshots,
        "tc": tc, "candidates": tuple(_candidate(x) for x in candidates), "conditions": tuple(_condition(x) for x in conditions),
        "auth": dict(auth), "spine": _nonempty(payload.get("producer_reference_spine_fingerprint"), "producer spine"),
        "publication": _publication(payload.get("publication_authority")),
    }

def _required(sig: str) -> BasisKind: return BasisKind.DIRECT if sig == SIG_001 else BasisKind.V553

def _block_for_conditions(conditions: Sequence[Mapping[str, Any]]) -> M1DecisionState | None:
    kinds = {x["condition_kind_id"] for x in conditions}
    if "K05" in kinds: return M1DecisionState.INELIGIBLE_EXPLICIT_DENIAL
    if kinds & {"K08", "K09"}: return M1DecisionState.INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY
    if "K06" in kinds: return M1DecisionState.INELIGIBLE_MISSING_REQUIRED_AUTHORITY
    if "K07" in kinds: return M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY
    return None

def _scr553_gate(i: Mapping[str, Any]) -> M1DecisionState | None:
    s = i["scr"]
    if s == "V553_NEGATIVE_LIMIT_ONLY": return M1DecisionState.INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY
    if s in {"NO_POSITIVE_V553_OUTPUT__MISSING_TEMPORAL_AUTHORITY", "NO_POSITIVE_V553_OUTPUT__MISSING_COMPARABILITY_AUTHORITY"}: return M1DecisionState.INELIGIBLE_MISSING_REQUIRED_AUTHORITY
    if s.startswith("NO_POSITIVE_") or s.startswith("REJECT_"): return M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    if i["sig"] == SIG_001 and s != "V553_NOT_REQUIRED_FOR_THIS_USE": return M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    if i["sig"] != SIG_001 and (s != "V553_REQUIRED" or not i["ops"]): return M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    return None

def _temporal_gate(i: Mapping[str, Any]) -> M1DecisionState | None:
    tc = i["tc"]
    if tc is TemporalCompleteness.BLOCKED_BY_APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE: return M1DecisionState.INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY
    if tc is TemporalCompleteness.UNKNOWN_FAIL_CLOSED: return M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY
    if tc is TemporalCompleteness.NOT_APPLICABLE_TO_TARGET_USE: return M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    if i["sig"] == SIG_001 and tc is not TemporalCompleteness.COMPLETE_FOR_DIRECT_V554: return M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    if i["sig"] != SIG_001 and tc is not TemporalCompleteness.REQUIRES_V553_OWNED_TEMPORAL_MEANING: return M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE
    return None

def _f2(conditions: Sequence[Mapping[str, Any]], f1_id: str | None) -> tuple[Mapping[str, Any], ...]:
    out = []
    for c in conditions:
        material = {"contract_version": "1.0.0", **c, "f1_id_or_null": f1_id, "target_use": TARGET_USE}
        out.append({"family": "F2", "f2_id": _urn("v554:f2", material), "condition_kind_id": c["condition_kind_id"], "disposition": CONDITION_DISPOSITION[c["condition_kind_id"]], "material": material})
    return tuple(sorted(out, key=lambda x: x["f2_id"]))

def _b1(i: Mapping[str, Any], state: M1DecisionState, f1_id: str | None, f2: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    key = semantic_hash({"governed_use_id": i["use"], "rule_ref": i["rule"], "signature_id": i["sig"], "target_use": TARGET_USE, "focal_structural_proposition_ref": i["prop"], "originating_admission_refs": list(i["origins"])})
    material = {"contract_version": "1.0.0", "candidate_semantic_key": key, "f1_id_or_null": f1_id, "sorted_f2_ids": sorted(x["f2_id"] for x in f2), "allowed_v555_structural_use": f1_id is not None and state is M1DecisionState.ELIGIBLE, "decision_state": state.value, "producer_reference_spine_fingerprint": i["spine"]}
    return {"family": "B1", "b1_id": _urn("v554:b1", material), "allowed_v555_structural_use": material["allowed_v555_structural_use"], "decision_state": state.value, "material": material}

def _handoff(i: Mapping[str, Any], f1: Mapping[str, Any] | None, f2: Sequence[Mapping[str, Any]], b1: Mapping[str, Any] | None) -> Mapping[str, Any] | None:
    a = i["publication"]
    if not a or a["producer"] != "V554" or a["publisher"] != "V557" or a["governed_use_id"] != i["use"] or a["rule_ref"] != i["rule"] or a["decision"] != "AUTHORIZED": return None
    objs = []
    if f1: objs.append(("F1", f1["f1_id"], semantic_hash(f1)))
    objs += [("F2", x["f2_id"], semantic_hash(x)) for x in f2]
    if b1: objs.append(("B1", b1["b1_id"], semantic_hash(b1)))
    allowed = set(a["allowed_object_families"])
    refs = sorted(({"family": f, "object_id": oid, "content_hash": h} for f, oid, h in objs if f in allowed), key=lambda x: (x["family"], x["object_id"]))
    if not refs: return None
    material = {"route": "V554_TO_V557_DIRECT", "governed_use_id": i["use"], "v554_rule_ref": i["rule"], "publication_authority": {k: a[k] for k in ("authority_id", "authority_version", "authority_hash")}, "object_refs": refs}
    return {"handoff_id": _urn("v554:v557-handoff", material), "route": "V554_TO_V557_DIRECT", "object_refs": refs, "material": material}

def _result(i: Mapping[str, Any], state: M1DecisionState, reason: str, required: BasisKind | None, rejected: Sequence[str] = (), context: bool = False) -> M1Evaluation:
    f2 = _f2(i["conditions"], None) if context and i["conditions"] else ()
    b1 = _b1(i, state, None, f2) if f2 else None
    return M1Evaluation(M1_CONTRACT_ID, state, reason, i["use"], required.value if required else None, 0, None, None, f2, b1, _handoff(i, None, f2, b1) if context else None, tuple(sorted(set(rejected))))

def _parse_failure(state: M1DecisionState, reason: str) -> M1Evaluation:
    return M1Evaluation(M1_CONTRACT_ID, state, reason, "", None, 0, None, None, (), None, None, ())

def evaluate_m1_temporal_v554_admission_dedup(payload: Any) -> M1Evaluation:
    """Evaluate one exact governed-use invocation; never uses latest/fuzzy/clock/RNG/filesystem state."""
    try: i = _parse(payload)
    except EquivalenceUnknown as e: return _parse_failure(M1DecisionState.EQUIVALENCE_UNKNOWN, str(e))
    except (Integrity, TypeError, ValueError, KeyError) as e: return _parse_failure(M1DecisionState.INTEGRITY_FAILURE, str(e) or "invalid invocation")
    required = _required(i["sig"])
    block = _block_for_conditions(i["conditions"])
    if block: return _result(i, block, "producer-governed hard negative/static authority blocks F1", required, context=True)
    block = _scr553_gate(i)
    if block: return _result(i, block, "SCR553 governed-use decision blocks requested M1 route", required)
    block = _temporal_gate(i)
    if block: return _result(i, block, "target-use temporal/signature gate blocks F1", required)
    if not i["candidates"]: return _result(i, M1DecisionState.VALID_EMPTY, "coherent zero candidates; no filler", required)
    try:
        for c in i["candidates"]:
            eq = c["equivalence_key"]
            if (eq["focal_structural_proposition_ref"] != i["prop"] or eq["target_use"] != TARGET_USE or eq["v554_rule_id"] != i["rule"]["id"] or eq["v554_rule_version"] != i["rule"]["version"] or eq["v554_rule_hash"] != i["rule"]["hash"]): raise Integrity("candidate/invocation binding mismatch")
    except Integrity as e: return _result(i, M1DecisionState.INTEGRITY_FAILURE, str(e), required)
    groups: dict[str, list[Mapping[str, Any]]] = {}
    for c in i["candidates"]: groups.setdefault(semantic_hash(c["equivalence_key"]), []).append(c)
    eligible, rejected = [], []
    for key in sorted(groups):
        group = groups[key]; counting = [c for c in group if c["basis_kind"] is required]
        rejected += [c["basis_ref"]["object_id"] for c in group if c["basis_kind"] is not required]
        if not counting: continue
        if required is BasisKind.V553:
            for c in counting:
                families = set(c["families"])
                if i["sig"] == SIG_002 and not {"TEMPORAL_KEY", "TEMPORAL_OBSERVATION"} <= families: return _result(i, M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE, "SIG-002 requires exact key+observation", required, rejected)
                if i["sig"] == SIG_003 and (not {"TEMPORAL_KEY", "TEMPORAL_RELATION"} <= families or not c["relation_refs"]): return _result(i, M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE, "SIG-003 requires exact key+relation+support/limit refs", required, rejected)
        if len({semantic_hash(c["semantics"]) for c in counting}) != 1: return _result(i, M1DecisionState.EQUIVALENCE_UNKNOWN, "equivalent candidates disagree on rule-relevant semantics", required, rejected)
        eligible.append((group[0]["equivalence_key"], counting))
    if not eligible: return _result(i, M1DecisionState.VALID_EMPTY, "no signature-required basis candidate; no filler", required, rejected)
    if len(eligible) != 1:
        rejected += [c["basis_ref"]["object_id"] for _, cs in eligible for c in cs]
        return _result(i, M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY, "multiple distinct basis groups; no winner heuristic", required, rejected)
    eq, counting = eligible[0]; semantics = counting[0]["semantics"]
    basis_material = {"equivalence_key": eq, "required_basis_kind": required.value, "selected_rule_relevant_basis_semantics": semantics}
    basis_id = _urn("v554:basis", basis_material)
    authority_fp = semantic_hash({"scr554_contract": SCR554_CONTRACT_ID, "m1_contract": M1_CONTRACT_ID, "v554_rule_ref": i["rule"], "signature_id": i["sig"], "selected_basis_semantic_identity": basis_id, "required_authority_snapshot_refs": list(i["snapshots"]), "external_authority_bundle_material": i["auth"]})
    f1_material = {"contract_version": "1.0.0", "equivalence_key": eq, "canonical_basis_semantic_id": basis_id, "rule_id": i["rule"]["id"], "rule_version": i["rule"]["version"], "rule_hash": i["rule"]["hash"], "signature_id": i["sig"], "target_use": TARGET_USE, "authority_bundle_fingerprint": authority_fp}
    f1_id = _urn("v554:f1", f1_material)
    f1 = {"family": "F1", "state": "ELIGIBLE", "f1_id": f1_id, "canonical_basis_semantic_id": basis_id, "provenance_alias_refs": sorted({c["basis_ref"]["object_id"] for c in counting}), "authority_bundle_fingerprint": authority_fp, "material": f1_material}
    f2 = _f2(i["conditions"], f1_id); b1 = _b1(i, M1DecisionState.ELIGIBLE, f1_id, f2)
    return M1Evaluation(M1_CONTRACT_ID, M1DecisionState.ELIGIBLE, "all frozen M1 gates passed", i["use"], required.value, 1, basis_id, f1, f2, b1, _handoff(i, f1, f2, b1), tuple(sorted(set(rejected))))
