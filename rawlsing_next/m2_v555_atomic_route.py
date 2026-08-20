#!/usr/bin/env python3
"""Fail-closed clean-sideline runtime for frozen M2 / V555 atomic routes."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Mapping, Sequence

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1_CONTRACT_ID, M1DecisionState, M1Evaluation, semantic_hash,
)

M2_CONTRACT_ID = "M2_V554_V555_ATOMIC_ROUTE_EXACT_SEAM_CONTRACT@1.0.0"
SCR555_CONTRACT_ID = "SCR555_V555_ATOMIC_ROUTE_EXACT_CONTRACT@stage-close-r03-1"
SEMANTIC_FAMILY = "STRUCTURAL_MEDIATION_ROUTE_CANDIDATE"
EPISTEMIC_CLASS = "ACTOR_INDEPENDENT_STRUCTURAL_PRIOR"
TARGET_USE = "STRUCTURAL_MEDIATION_INPUT"
ROUTE_AUTHORITY_ID, ROUTE_AUTHORITY_VERSION = "V555_MEDIATION_ROUTE_RULE_REGISTRY", "1.0.0"
ROUTE_RULE_ID, ROUTE_RULE_VERSION = "V555-RR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL", "1.0.0"
ROUTE_SHAPE_ID, ROUTE_SHAPE_VERSION = "V555-RS-001-SOURCE-EXACT-CHANNEL-EXACT-RECEIVER", "1.0.0"
CHANNEL_STRUCTURAL_ROLE_ID = "V555-LCR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL"
RECEIVING_CONSTRAINT_KIND = "V555-RC-001-EXACT-STRUCTURAL-POSITION-REF"
ROUTE_BORN_PREDICATE_AUTHORITY_ID, ROUTE_BORN_PREDICATE_AUTHORITY_VERSION = "V555_ROUTE_BORN_PREDICATE_RULE", "1.0.0"
ROUTE_BORN_PREDICATE_REGISTRY_ID, ROUTE_BORN_PREDICATE_REGISTRY_VERSION = "V555_ROUTE_BORN_PREDICATE_REGISTRY", "1.0.0"
_SHA = re.compile(r"^[0-9a-f]{64}$")
_URNS = {x: re.compile(rf"^urn:rawlsing:v554:{x.lower()}:sha256:([0-9a-f]{{64}})$") for x in ("F1", "F2", "B1")}
_REQ_KEYS = {"route_authority_ref", "route_rule_ref", "route_shape_ref", "f1_reference_closure", "channel_structural_role_id", "receiving_constraint_kind", "producer_allowed_uses", "v556_higher_order_semantics_required", "v557_publication_authority"}

class M2DecisionState(str, Enum):
    ROUTE_CANDIDATE_AUTHORIZED = "ROUTE_CANDIDATE_AUTHORIZED"
    VALID_EMPTY = "VALID_EMPTY"
    V554_STRUCTURAL_USE_DENIED = "V554_STRUCTURAL_USE_DENIED"
    NO_GOVERNED_ROUTE_AUTHORITY = "NO_GOVERNED_ROUTE_AUTHORITY"
    ROUTE_BLOCKED_BY_GOVERNED_RULE = "ROUTE_BLOCKED_BY_GOVERNED_RULE"
    ROUTE_STATIC_AUTHORITY_MISSING = "ROUTE_STATIC_AUTHORITY_MISSING"
    ROUTE_IDENTITY_UNRESOLVED = "ROUTE_IDENTITY_UNRESOLVED"
    DEFERRED_RUNTIME_BINDING_REFERENCED_ONLY = "DEFERRED_RUNTIME_BINDING_REFERENCED_ONLY"
    CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE = "CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE"

@dataclass(frozen=True)
class M2Evaluation:
    contract_id: str
    decision_state: M2DecisionState
    reason: str
    upstream_m1_decision_state: str
    exact_v554_f1_ref: Mapping[str, str] | None
    exact_v554_b1_ref: Mapping[str, str] | None
    inherited_v554_f2_refs: tuple[Mapping[str, str], ...]
    canonical_route_identity: tuple[Any, ...] | None
    canonical_route_identity_hash: str | None
    route: Mapping[str, Any] | None
    route_born_predicate_registry: Mapping[str, Any]
    direct_v557_handoff: Mapping[str, Any] | None
    replay_key_hash: str | None

class _Integrity(ValueError): pass
class _Missing(ValueError): pass
class _NoAuthority(ValueError): pass
class _Unresolved(ValueError): pass

def _text(v: Any, name: str) -> str:
    if not isinstance(v, str) or not v.strip(): raise _Integrity(f"{name} must be non-empty")
    return v.strip()

def _hash(v: Any, name: str, missing: bool = False) -> str:
    if v in (None, "") and missing: raise _Missing(f"{name} missing")
    v = _text(v, name)
    if not _SHA.fullmatch(v): raise _Integrity(f"{name} must be lowercase sha256")
    return v

def _ref(v: Any, name: str) -> dict[str, str]:
    if v is None: raise _Unresolved(f"{name} missing")
    if not isinstance(v, Mapping): raise _Integrity(f"{name} must be mapping")
    need = {"kind", "object_id", "content_hash"}
    if need - set(v): raise _Unresolved(f"{name} missing exact fields")
    if set(v) != need: raise _Integrity(f"{name} has noncanonical fields")
    return {"kind": _text(v["kind"], f"{name}.kind"), "object_id": _text(v["object_id"], f"{name}.object_id"), "content_hash": _hash(v["content_hash"], f"{name}.content_hash")}

def _auth(v: Any, name: str, aid: str, ver: str) -> dict[str, str]:
    if v is None: raise _Missing(f"{name} missing")
    if not isinstance(v, Mapping): raise _Integrity(f"{name} must be mapping")
    need = {"id", "version", "content_hash"}
    if need - set(v): raise _Missing(f"{name} missing exact fields")
    if set(v) != need: raise _Integrity(f"{name} has noncanonical fields")
    out = {"id": _text(v["id"], f"{name}.id"), "version": _text(v["version"], f"{name}.version"), "content_hash": _hash(v["content_hash"], f"{name}.content_hash", True)}
    if out["id"] != aid or out["version"] != ver: raise _NoAuthority(f"{name} is not exact active {aid}@{ver}")
    return out

def _obj(v: Any, family: str) -> dict[str, str]:
    if not isinstance(v, Mapping): raise _Integrity(f"{family} missing")
    oid = _text(v.get(f"{family.lower()}_id"), f"{family}.id")
    material = v.get("material"); match = _URNS[family].fullmatch(oid)
    if not match or not isinstance(material, Mapping) or match.group(1) != semantic_hash(material): raise _Integrity(f"{family} canonical identity/material mismatch")
    return {"kind": family, "object_id": oid, "content_hash": semantic_hash(v)}

def _registry() -> Mapping[str, Any]:
    return {"authority_id": ROUTE_BORN_PREDICATE_AUTHORITY_ID, "authority_version": ROUTE_BORN_PREDICATE_AUTHORITY_VERSION, "registry_id": ROUTE_BORN_PREDICATE_REGISTRY_ID, "registry_version": ROUTE_BORN_PREDICATE_REGISTRY_VERSION, "state": M2DecisionState.VALID_EMPTY.value, "registered_predicate_count": 0, "predicate_refs": ()}

def _empty(state: M2DecisionState, reason: str, upstream: str, f1=None, b1=None, f2=()) -> M2Evaluation:
    return M2Evaluation(M2_CONTRACT_ID, state, reason, upstream, f1, b1, tuple(f2), None, None, None, _registry(), None, None)

def _nonpositive(m1: M1Evaluation) -> M2Evaluation | None:
    s = m1.decision_state
    if s is M1DecisionState.ELIGIBLE: return None
    if s is M1DecisionState.VALID_EMPTY: return _empty(M2DecisionState.VALID_EMPTY, "V554 valid-empty; no filler route", s.value)
    if s is M1DecisionState.INTEGRITY_FAILURE: return _empty(M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE, "V554 integrity failure is presemantic", s.value)
    if s in {M1DecisionState.INELIGIBLE_MISSING_REQUIRED_AUTHORITY, M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY, M1DecisionState.EQUIVALENCE_UNKNOWN}:
        return _empty(M2DecisionState.ROUTE_STATIC_AUTHORITY_MISSING, "V554 required authority/equivalence unresolved; no F1", s.value)
    return _empty(M2DecisionState.V554_STRUCTURAL_USE_DENIED, "V554 is nonpositive for structural mediation; no reconstruction", s.value)

def _upstream(m1: M1Evaluation):
    if m1.contract_id != M1_CONTRACT_ID: raise _Integrity("M1 contract id mismatch")
    if m1.support_count != 1 or m1.f1 is None or m1.b1 is None: raise _Integrity("ELIGIBLE M1 must carry exactly one F1 and B1")
    f1, b1 = m1.f1, m1.b1
    if f1.get("family") != "F1" or f1.get("state") != "ELIGIBLE": raise _Integrity("F1 must be ELIGIBLE")
    if not isinstance(f1.get("material"), Mapping) or f1["material"].get("target_use") != TARGET_USE: raise _Integrity("F1 target use mismatch")
    f1r = _obj(f1, "F1")
    if b1.get("family") != "B1": raise _Integrity("B1 family mismatch")
    b1r = _obj(b1, "B1"); bm = b1.get("material")
    if not isinstance(bm, Mapping) or bm.get("f1_id_or_null") != f1r["object_id"] or b1.get("allowed_v555_structural_use") is not True or bm.get("allowed_v555_structural_use") is not True or bm.get("decision_state") != "ELIGIBLE": raise _Integrity("B1 does not exactly authorize this F1")
    f2r = tuple(sorted((_obj(x, "F2") for x in m1.f2), key=lambda x: x["object_id"]))
    if sorted(bm.get("sorted_f2_ids", ())) != [x["object_id"] for x in f2r]: raise _Integrity("B1/F2 closure mismatch")
    return f1r, b1r, f2r

def _closure(v: Any, f1r: Mapping[str, str]) -> dict[str, Any]:
    if v is None: raise _Unresolved("f1_reference_closure missing")
    if not isinstance(v, Mapping): raise _Integrity("f1_reference_closure must be mapping")
    fields = {"f1_id", "f1_content_hash", "source_structural_position_ref", "structural_channel_ref", "receiving_structural_position_ref", "closure_authority_ref", "closure_content_hash"}
    if fields - set(v): raise _Unresolved("f1_reference_closure missing exact fields")
    if set(v) != fields: raise _Integrity("f1_reference_closure has noncanonical fields")
    material = {"f1_id": _text(v["f1_id"], "closure.f1_id"), "f1_content_hash": _hash(v["f1_content_hash"], "closure.f1_content_hash"), "source_structural_position_ref": _ref(v["source_structural_position_ref"], "closure.source"), "structural_channel_ref": _ref(v["structural_channel_ref"], "closure.channel"), "receiving_structural_position_ref": _ref(v["receiving_structural_position_ref"], "closure.receiver"), "closure_authority_ref": _ref(v["closure_authority_ref"], "closure.authority")}
    if material["f1_id"] != f1r["object_id"] or material["f1_content_hash"] != f1r["content_hash"]: raise _Integrity("reference closure does not bind exact F1")
    seal = _hash(v["closure_content_hash"], "closure.content_hash")
    if semantic_hash(material) != seal: raise _Integrity("reference closure hash mismatch")
    return {**material, "closure_content_hash": seal}

def _parse(req: Any, f1r: Mapping[str, str]) -> dict[str, Any]:
    if not isinstance(req, Mapping): raise _Integrity("route request must be mapping")
    extra = set(req) - _REQ_KEYS
    if extra: raise _Integrity(f"forbidden/non-M2 request fields: {sorted(extra)!r}")
    a = _auth(req.get("route_authority_ref"), "route_authority_ref", ROUTE_AUTHORITY_ID, ROUTE_AUTHORITY_VERSION)
    r = _auth(req.get("route_rule_ref"), "route_rule_ref", ROUTE_RULE_ID, ROUTE_RULE_VERSION)
    s = _auth(req.get("route_shape_ref"), "route_shape_ref", ROUTE_SHAPE_ID, ROUTE_SHAPE_VERSION)
    role = _text(req.get("channel_structural_role_id"), "channel_structural_role_id")
    recv = _text(req.get("receiving_constraint_kind"), "receiving_constraint_kind")
    if role != CHANNEL_STRUCTURAL_ROLE_ID or recv != RECEIVING_CONSTRAINT_KIND: raise _NoAuthority("route role/receiver constraint is outside active first tranche")
    uses = req.get("producer_allowed_uses", ())
    if isinstance(uses, (str, bytes)) or not isinstance(uses, Sequence): raise _Integrity("producer_allowed_uses must be sequence")
    uses = tuple(sorted({_text(x, "producer_allowed_uses") for x in uses}))
    v556 = req.get("v556_higher_order_semantics_required")
    if v556 is not None and not isinstance(v556, bool): raise _Integrity("v556_higher_order_semantics_required must be boolean")
    return {"authority": a, "rule": r, "shape": s, "closure": _closure(req.get("f1_reference_closure"), f1r), "role": role, "recv": recv, "uses": uses, "v556": v556, "publication": req.get("v557_publication_authority")}

def _handoff(route: Mapping[str, Any], p: Mapping[str, Any]) -> Mapping[str, Any] | None:
    if p["v556"] is not False or p["publication"] is None: return None
    x = p["publication"]
    if not isinstance(x, Mapping): raise _Integrity("v557_publication_authority must be mapping")
    fields = {"authority_id", "authority_version", "authority_hash", "producer", "publisher", "decision", "intended_use", "allowed_object_families"}
    if set(x) != fields: raise _Integrity("v557_publication_authority fields are not exact")
    fam = x["allowed_object_families"]
    if isinstance(fam, (str, bytes)) or not isinstance(fam, Sequence): raise _Integrity("allowed_object_families must be sequence")
    aid, ver, ah = _text(x["authority_id"], "publication.id"), _text(x["authority_version"], "publication.version"), _hash(x["authority_hash"], "publication.hash")
    use = _text(x["intended_use"], "publication.intended_use")
    if _text(x["producer"], "publication.producer") != "V555" or _text(x["publisher"], "publication.publisher") != "V557" or _text(x["decision"], "publication.decision") != "AUTHORIZED" or use not in p["uses"] or SEMANTIC_FAMILY not in {_text(y, "allowed_object_families") for y in fam}: return None
    rr = {"kind": SEMANTIC_FAMILY, "object_id": route["route_id"], "content_hash": semantic_hash(route)}
    material = {"route": "V555_TO_V557_DIRECT", "route_ref": rr, "intended_use": use, "publication_authority": {"id": aid, "version": ver, "content_hash": ah}}
    return {"handoff_id": f"urn:rawlsing:v555:v557-handoff:sha256:{semantic_hash(material)}", "route": "V555_TO_V557_DIRECT", "route_ref": rr, "intended_use": use, "material": material}

def evaluate_m2_v555_atomic_route(m1: Any, request: Any) -> M2Evaluation:
    """Build one actor-independent V555 route; never guesses authority or reconstructs F1."""
    if not isinstance(m1, M1Evaluation): return _empty(M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE, "exact accepted M1Evaluation required; raw admission/V553/legacy bypass forbidden", "")
    if m1.contract_id != M1_CONTRACT_ID: return _empty(M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE, "M1 contract id mismatch", m1.decision_state.value)
    prior = _nonpositive(m1)
    if prior is not None: return prior
    try:
        f1r, b1r, f2r = _upstream(m1); p = _parse(request, f1r)
    except _Missing as e: return _empty(M2DecisionState.ROUTE_STATIC_AUTHORITY_MISSING, str(e), m1.decision_state.value)
    except _NoAuthority as e: return _empty(M2DecisionState.NO_GOVERNED_ROUTE_AUTHORITY, str(e), m1.decision_state.value)
    except _Unresolved as e: return _empty(M2DecisionState.ROUTE_IDENTITY_UNRESOLVED, str(e), m1.decision_state.value)
    except (_Integrity, TypeError, ValueError, KeyError) as e: return _empty(M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE, str(e) or "invalid M2 construction", m1.decision_state.value)
    c = p["closure"]
    ident = (f1r["object_id"], f"{ROUTE_RULE_ID}@{ROUTE_RULE_VERSION}", f"{ROUTE_SHAPE_ID}@{ROUTE_SHAPE_VERSION}", p["role"], c["structural_channel_ref"], p["recv"], c["receiving_structural_position_ref"])
    ih = semantic_hash(list(ident)); rid = f"urn:rawlsing:v555:route:sha256:{ih}"
    route = {"semantic_family": SEMANTIC_FAMILY, "epistemic_class": EPISTEMIC_CLASS, "route_id": rid, "canonical_route_identity": ident, "canonical_route_identity_hash": ih, "ordered_structure": ({"ordinal": 1, "role": "SOURCE", "binding": c["source_structural_position_ref"]}, {"ordinal": 2, "role": "MEDIATION_LOCUS", "binding": c["structural_channel_ref"], "channel_structural_role_id": p["role"]}, {"ordinal": 3, "role": "RECEIVER", "binding": c["receiving_structural_position_ref"], "receiving_constraint_kind": p["recv"], "operator": "EXACT_REF_EQ"}), "exact_v554_f1_ref": f1r, "exact_v554_b1_ref": b1r, "inherited_v554_f2_refs": f2r, "f1_reference_closure_hash": c["closure_content_hash"], "route_authority_ref": p["authority"], "route_rule_ref": p["rule"], "route_shape_ref": p["shape"], "producer_allowed_uses": p["uses"], "route_born_predicate_registry": _registry(), "actor_independent": True}
    replay = {"m2_contract_id": M2_CONTRACT_ID, "scr555_contract_id": SCR555_CONTRACT_ID, "m1_contract_id": M1_CONTRACT_ID, "exact_v554_f1_ref": f1r, "exact_v554_b1_ref": b1r, "inherited_v554_f2_refs": list(f2r), "route_authority_ref": p["authority"], "route_rule_ref": p["rule"], "route_shape_ref": p["shape"], "f1_reference_closure_authority_ref": c["closure_authority_ref"], "f1_reference_closure_hash": c["closure_content_hash"], "source_structural_position_ref": c["source_structural_position_ref"], "producer_allowed_uses": list(p["uses"]), "canonical_route_identity": list(ident), "typed_result": M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED.value}
    rh = semantic_hash(replay); route = {**route, "replay_key_hash": rh}
    try: handoff = _handoff(route, p)
    except (_Integrity, TypeError, ValueError, KeyError) as e: return _empty(M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE, str(e) or "invalid V557 handoff authority", m1.decision_state.value, f1r, b1r, f2r)
    return M2Evaluation(M2_CONTRACT_ID, M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED, "exact M1 F1/B1, active V555 authority, immutable closure, and seven-field identity verified", m1.decision_state.value, f1r, b1r, f2r, ident, ih, route, _registry(), handoff, rh)
