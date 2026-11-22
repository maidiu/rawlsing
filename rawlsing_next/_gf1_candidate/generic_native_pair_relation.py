"""R17 GF1 — NEW NAMESPACED GENERIC NATIVE PAIR RELATION owner (TEST_ONLY candidate).

GRAIN: SOURCEFREE_GENERIC_PAIR_CANDIDATE_TEST_ONLY. UNISSUED. NOT ACCEPTED.
GENERIC_NATIVE_SEMANTICS_HOLD IS RETAINED.

WHY THIS EXISTS
---------------
The ACCEPTED Field Forge semantic owner
(`rawlsing_next/field_forge_conditional_support.py`) hardcodes:

    CONDITIONER_SOURCE_NATIVE_VARIABLE = "Q86B"
    TARGET_SOURCE_NATIVE_VARIABLE     = "Q86A"
    RELATION_FAMILY = "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0"
    SEMANTIC_OWNER  = "FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER"

and rejects any other target-domain identity. That is a SEMANTIC specialisation,
not a data limitation: the accepted native I03 query already carries generic
source-native identities (`urn:test:i03:question_native:m01-Y` / `...-X`).

So the smallest honest move is a SEPARATELY NAMED candidate owner that:
  * consumes the SAME real native EmpiricalFact / EmpiricalQuerySpec objects,
  * derives each role's source-native variable FROM THE ACTUAL QUERY (never from a
    hardcoded specialized label),
  * recomputes the target-domain identity from the actual native components,
  * carries its own relation family / object identity / owner name,
  * and refuses everything the accepted owner refuses (no permission widening,
    RAW/unweighted only, single universe, complete native domain, observed-zero
    versus ZERO_SUPPORT distinction intact, exact risk/authority/provenance
    closure).

It is a CANDIDATE. It issues nothing, changes nothing canonical, and reuses no
accepted owner name.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

GENERIC_RELATION_OWNER = "GF1_GENERIC_PAIR_CANDIDATE_RELATION_OWNER_TEST_ONLY"
GENERIC_RELATION_FAMILY = "GF1_GENERIC_NATIVE_PAIR_RELATION_TEST_ONLY@1.0.0"
GENERIC_CONSUMER_ID = "GF1_PAIR_SUPPORT_SIGNATURE_CONSUMER_TEST_ONLY@1.0.0"
GENERIC_RESULT_FAMILY = "GF1_PAIR_SUPPORT_SIGNATURE_RESULT_TEST_ONLY@1.0.0"
GENERIC_GRAIN = (
    "SOURCEFREE_GENERIC_PAIR_CANDIDATE_TEST_ONLY__UNISSUED__NOT_ACCEPTED__"
    "GENERIC_NATIVE_SEMANTICS_HOLD"
)

CONDITIONER_ROLE = "CONDITIONER"
TARGET_ROLE = "TARGET"
ROLE_ORDER = (CONDITIONER_ROLE, TARGET_ROLE)
STATE_ORDER_SEMANTICS = "IDENTITY_ONLY__NO_ORDINAL_OR_METRIC_MEANING"
INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"
FROZEN_JOINT_ORDER = "SEMANTIC_ORDERED"
REVERSE_PAIR_GRANT_ID = "GF1_REVERSE_X_GIVEN_Y_PAIR_GRANT_TEST_ONLY@1"

ANTI_INFERENCES = (
    "CONDITIONER != CAUSE",
    "TARGET != EFFECT",
    "PAIR_SUPPORT_PROFILE != RELATIONSHIP_OR_DYAD",
    "PAIR_SUPPORT_PROFILE != PEER_OR_PERSON_FACT",
    "PAIR_SUPPORT_PROFILE != CONDITIONAL_REDISTRIBUTION_MECHANISM",
    "POPULATION_FACT != ACTOR_FACT",
    "GENERIC_CANDIDATE != ADOPTED_SEMANTICS",
    "SEPARATION_CLASS != BEHAVIOURAL_OR_PSYCHOLOGICAL_CLAIM",
)

ALLOWED_TYPED_STATES = frozenset({
    "SUPPORTED",
    "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET",
    "ZERO_SUPPORT",
    "UNRESOLVED_TARGET_STATE",
    "MISSING_TARGET_STATE",
    "NONRESPONSE",
})

ZERO_CELL_STATES = frozenset({
    "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET", "ZERO_SUPPORT",
})


class GenericNativePairError(ValueError):
    pass


class GenericPermissionWideningError(GenericNativePairError):
    pass


# --------------------------------------------------------------------------- utils

def canonicalize(value: Any) -> Any:
    if isinstance(value, (list, tuple)):
        return [canonicalize(v) for v in value]
    if isinstance(value, Mapping):
        return {str(k): canonicalize(value[k]) for k in sorted(value)}
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(canonicalize(value), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def semantic_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GenericNativePairError(f"{name} must be a mapping")
    return value


def _sequence(value: Any, name: str, *, allow_empty: bool = False) -> list:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise GenericNativePairError(f"{name} must be a sequence")
    if not allow_empty and not value:
        raise GenericNativePairError(f"{name} must be non-empty")
    return list(value)


def _ref(value: Any, name: str):
    """Normalize a native exact reference exactly as the accepted owner does."""
    from rawlsing_next._pre553_query_common import exact_ref as _native_exact_ref
    try:
        return _native_exact_ref(value, name)
    except Exception as exc:
        raise GenericNativePairError(f"{name} must be an exact native ref: {exc}") from exc


def _ref_seq(values, name: str):
    refs = tuple(_ref(v, name) for v in values)
    return tuple(sorted(set(refs), key=lambda r: r.key))


def _authority_seq(values, name: str):
    from rawlsing_next._pre553_query_common import AuthorityRef
    refs = tuple(values)
    if not all(isinstance(r, AuthorityRef) for r in refs):
        raise GenericNativePairError(f"{name} must use exact native AuthorityRef")
    return tuple(sorted(set(refs), key=lambda r: r.key))


def _ref_dict(ref: Any) -> dict:
    return ref.as_dict() if hasattr(ref, "as_dict") else dict(ref)


def _auth_dict(ref: Any) -> dict:
    d = ref.as_dict() if hasattr(ref, "as_dict") else dict(ref)
    return {"authority_id": d.get("object_id"), "authority_version": d.get("content_hash")}


def _semantic_fields(obj: Any) -> Mapping[str, Any]:
    """Native producer objects keep their real payload under semantic_fields."""
    proj = obj.semantic_projection()
    return _mapping(proj.get("semantic_fields"), "semantic_fields")


# --------------------------------------------------------------------------- relation

@dataclass(frozen=True)
class GenericNativePairRelation:
    """Immutable GF1 generic PAIR relation/result. CANDIDATE, unissued."""

    typed_state: str
    producer_state_blocking: bool
    # roles are declared from the ACTUAL native query, not from hardcoded labels
    conditioner_source_native_variable: str
    target_source_native_variable: str
    conditioner_ref: Any
    target_ref: Any
    conditioner_domain: tuple
    target_domain: tuple
    target_domain_identity: str
    joint_order_semantics: str
    operation_role_order: str
    native_component_order: tuple
    risk_set_ref: Any
    risk_set_type: str
    empirical_universe_refs: tuple
    measure_kind: str
    measure_basis_ref: Any
    source_scope_mode: str
    response_state_semantics_ref: Any
    uncertainty_method_or_typed_state: str
    producer_fact_ref: Any
    producer_query_ref: Any
    producer_authority_refs: tuple
    producer_provenance_refs: tuple
    producer_replay_ref: Any
    producer_condition_predicate_ref: Any
    producer_risk_set_member_refs: tuple
    producer_denominator_member_refs: tuple
    producer_permission_ceiling: tuple
    relation_permission_ceiling: tuple
    eligible_joint_risk_total: int
    excluded_ineligible_target_count: int
    conditional_count_profile: tuple
    content_hash: str
    object_id: str

    def __post_init__(self) -> None:
        if self.typed_state not in ALLOWED_TYPED_STATES:
            raise GenericNativePairError(f"invalid generic typed_state {self.typed_state!r}")
        if self.producer_state_blocking != (self.typed_state != "SUPPORTED"):
            raise GenericNativePairError("producer_state_blocking must reflect typed state")
        if not set(self.relation_permission_ceiling).issubset(set(self.producer_permission_ceiling)):
            raise GenericPermissionWideningError(
                "generic relation permission exceeds producer permission ceiling")
        if self.producer_state_blocking and self.conditional_count_profile:
            raise GenericNativePairError("blocked generic relation may not carry positive counts")
        digest = semantic_hash(self.semantic_projection())
        expected = f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}"
        if self.content_hash != digest or self.object_id != expected:
            raise GenericNativePairError(
                "generic relation object_id/content_hash do not match semantic projection")

    @property
    def family(self) -> str:
        return GENERIC_RELATION_FAMILY

    @property
    def semantic_owner(self) -> str:
        return GENERIC_RELATION_OWNER

    @property
    def ref(self):
        from rawlsing_next._pre553_query_common import ExactRef
        return ExactRef(GENERIC_RELATION_FAMILY, self.object_id, self.content_hash)

    def semantic_projection(self) -> dict:
        return {
            "relation_family": GENERIC_RELATION_FAMILY,
            "semantic_owner": GENERIC_RELATION_OWNER,
            "grain": GENERIC_GRAIN,
            "relation_semantics": "EXACT_GENERIC_TWO_BINARY_ITEM_PAIR_CONDITIONAL_SUPPORT_PROFILE",
            "typed_state": self.typed_state,
            "producer_state_blocking": self.producer_state_blocking,
            "roles": {
                CONDITIONER_ROLE: {
                    "source_native_variable": self.conditioner_source_native_variable,
                    "ref": _ref_dict(self.conditioner_ref),
                },
                TARGET_ROLE: {
                    "source_native_variable": self.target_source_native_variable,
                    "ref": _ref_dict(self.target_ref),
                },
            },
            "participant_cardinality": 2,
            "participant_role_order": list(ROLE_ORDER),
            "state_order_semantics": STATE_ORDER_SEMANTICS,
            "conditioner_domain": canonicalize(self.conditioner_domain),
            "target_domain": canonicalize(self.target_domain),
            "target_domain_identity": self.target_domain_identity,
            "joint_order_semantics": self.joint_order_semantics,
            "operation_role_order": self.operation_role_order,
            "native_component_order": list(self.native_component_order),
            "risk_set_ref": _ref_dict(self.risk_set_ref),
            "risk_set_type": self.risk_set_type,
            "empirical_universe_refs": [_ref_dict(r) for r in self.empirical_universe_refs],
            "measure_kind": self.measure_kind,
            "measure_basis_ref": _ref_dict(self.measure_basis_ref),
            "source_scope_mode": self.source_scope_mode,
            "response_state_semantics_ref": _ref_dict(self.response_state_semantics_ref),
            "uncertainty_method_or_typed_state": self.uncertainty_method_or_typed_state,
            "producer_fact_ref": _ref_dict(self.producer_fact_ref),
            "producer_query_ref": _ref_dict(self.producer_query_ref),
            "producer_authority_refs": [_auth_dict(r) for r in self.producer_authority_refs],
            "producer_provenance_refs": [_ref_dict(r) for r in self.producer_provenance_refs],
            "producer_replay_ref": _ref_dict(self.producer_replay_ref),
            "producer_condition_predicate_ref": _ref_dict(self.producer_condition_predicate_ref),
            "producer_risk_set_member_refs": [_ref_dict(r) for r in self.producer_risk_set_member_refs],
            "producer_denominator_member_refs": [_ref_dict(r) for r in self.producer_denominator_member_refs],
            "producer_permission_ceiling": list(self.producer_permission_ceiling),
            "relation_permission_ceiling": list(self.relation_permission_ceiling),
            "eligible_joint_risk_total": self.eligible_joint_risk_total,
            "excluded_ineligible_target_count": self.excluded_ineligible_target_count,
            "information_loss": INFORMATION_LOSS,
            "conditional_count_profile": canonicalize(self.conditional_count_profile),
            "anti_inferences": list(ANTI_INFERENCES),
        }

    def as_dict(self) -> dict:
        return {**self.semantic_projection(),
                "object_id": self.object_id, "content_hash": self.content_hash}


# --------------------------------------------------------------------------- producer

def _derive_native_variable_name(ref: Any) -> str:
    """Generic: take the source-native name FROM the native ref itself.

    Never returns Q86A/Q86B unless the native source genuinely says so.
    """
    oid = _ref_dict(ref).get("object_id", "")
    tail = str(oid).rsplit(":", 1)[-1]
    return tail or str(oid)


def produce_generic_native_pair_relation(
    *,
    joint_fact,
    joint_query,
    conditioner_ref,
    target_ref,
    producer_permission_ceiling: Iterable[str],
    relation_permission_ceiling: Iterable[str] | None = None,
    reverse_pair_grant: str | None = None,
) -> GenericNativePairRelation:
    """Produce a NEW generic two-binary-item PAIR relation from REAL native objects.

    ROLE BINDING IS OWNER-GATED.
    The native query fixes a two-component order. This TEST_ONLY candidate
    implements CONDITIONER=first and TARGET=second only. Reverse native
    roles are unimplemented and refused even with the legacy TEST_ONLY grant.
    """
    fs = _semantic_fields(joint_fact)
    qs = _semantic_fields(joint_query)

    # ---- identity + closure (mirrors every accepted refusal we must keep) ----
    if semantic_hash(joint_fact.semantic_projection()) != joint_fact.content_hash:
        raise GenericNativePairError("producer fact semantic identity mismatch")
    if semantic_hash(joint_query.semantic_projection()) != joint_query.content_hash:
        raise GenericNativePairError("producer query semantic identity mismatch")
    typed = joint_fact.typed_state
    if typed not in ALLOWED_TYPED_STATES:
        raise GenericNativePairError(f"unsupported native producer typed_state {typed!r}")

    fact_query_ref = _ref(joint_fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref")
    if _ref_dict(fact_query_ref) != _ref_dict(joint_query.ref):
        raise GenericNativePairError("fact does not bind the supplied exact query identity")

    fact_risk = _ref(joint_fact.risk_set_ref, "fact.risk_set_ref")
    query_risk = _ref(joint_query.risk_set_ref, "query.risk_set_ref")
    if _ref_dict(fact_risk) != _ref_dict(query_risk):
        raise GenericNativePairError("fact/query risk-set mismatch")

    universes = _ref_seq(joint_fact.empirical_universe_refs, "fact.empirical_universe_refs")
    if len(universes) != 1 or [_ref_dict(u) for u in universes] != [
            _ref_dict(_ref(u, "query.empirical_universe_refs"))
            for u in joint_query.empirical_universe_refs]:
        raise GenericNativePairError("generic PAIR requires one exact identical SINGLE_UNIVERSE scope")

    grain = _mapping(qs["requested_output_grain"], "requested_output_grain")
    if grain.get("source_scope_mode") != "SINGLE_UNIVERSE":
        raise GenericNativePairError("generic PAIR requires SINGLE_UNIVERSE")
    if grain.get("measure_kind") != "RAW":
        raise GenericNativePairError("generic PAIR is RAW/unweighted only")

    if fs.get("weighted_numerator_support_if_authorized") is not None:
        raise GenericNativePairError("generic PAIR may not consume a weighted numerator")
    if fs.get("weighted_denominator_support_if_authorized") is not None:
        raise GenericNativePairError("generic PAIR may not consume a weighted denominator")

    authorities = _authority_seq(joint_fact.authority_snapshot_refs, "fact.authority_snapshot_refs")
    if not set(joint_query.authority_snapshot_refs).issubset(set(authorities)):
        raise GenericNativePairError("fact authority closure does not preserve query authorities")

    replay_ref = _ref(joint_fact.replay_ref, "fact.replay_ref")
    if _ref(joint_fact.producer_replay_locator_or_reference_root, "fact replay root") != replay_ref:
        raise GenericNativePairError("producer replay root differs from exact fact replay_ref")

    deps = _ref_seq(joint_fact.dependency_refs, "fact.dependency_refs")
    if _ref(joint_query.ref, "query.ref") not in deps or replay_ref not in deps:
        raise GenericNativePairError("fact dependency closure omits query or replay identity")
    provenance = _ref_seq(joint_fact.source_empirical_provenance_refs, "fact.source_empirical_provenance_refs")
    if not provenance or not set(provenance).issubset(set(deps)):
        raise GenericNativePairError("fact provenance closure empty or not retained")

    # ---- native two-component domain, taken from the ACTUAL query ----
    spec = _mapping(qs["target_arity_and_topology"], "target_arity_and_topology")
    if spec.get("arity") != 2:
        raise GenericNativePairError("generic PAIR requires exact two-target arity")
    if spec.get("joint_order_semantics") != FROZEN_JOINT_ORDER:
        raise GenericNativePairError("generic PAIR joint order must be SEMANTIC_ORDERED")
    native_order = (_ref(joint_query.target_refs[0], "query.target_refs[0]"),
                    _ref(joint_query.target_refs[1], "query.target_refs[1]"))
    want = (_ref(conditioner_ref, "conditioner_ref"), _ref(target_ref, "target_ref"))
    if want == native_order:
        operation_role_order = "FORWARD_NATIVE_ORDER"
    elif want == (native_order[1], native_order[0]):
        # GF1-R1: never relabel forward counts as reversed facts.
        # Legacy TEST_ONLY grant is not authority to invent transpose semantics.
        raise GenericNativePairError("REVERSE_PAIR_OPERATION_NOT_SUPPORTED")
    else:
        raise GenericNativePairError("query target role/order is not a native component permutation")
    comps = _sequence(spec.get("components"), "target components")
    if len(comps) != 2:
        raise GenericNativePairError("generic PAIR requires exactly two target components")

    from itertools import product
    normalized, domains = [], []
    for idx, (raw, expect) in enumerate(zip(comps, native_order)):
        comp = _mapping(raw, f"target component {idx}")
        if _ref_dict(_ref(comp["target_ref"], "component.target_ref")) != _ref_dict(expect):
            raise GenericNativePairError("target component ref/order mismatch")
        if comp.get("topology") != "SCALAR_SINGULAR":
            raise GenericNativePairError("generic PAIR requires source-native SCALAR_SINGULAR targets")
        dom = tuple(canonicalize(v) for v in _sequence(comp.get("domain"), "component.domain"))
        if len({canonical_json(v) for v in dom}) != len(dom):
            raise GenericNativePairError("target domain contains duplicate exact states")
        if len(dom) != 2:
            raise GenericNativePairError("generic PAIR is frozen at two-binary-item domains")
        normalized.append({
            "target_ref": _ref_dict(comp["target_ref"]),
            "topology": comp["topology"],
            "domain": list(dom),
            "target_domain_replay_ref": _ref_dict(_ref(comp["target_domain_replay_ref"], "replay ref")),
        })
        domains.append(dom)

    # identity recomputed from the ACTUAL native components (not a stored label)
    domain_identity = semantic_hash({
        "components": normalized,
        "joint_order_semantics": FROZEN_JOINT_ORDER,
        "full_domain": [canonicalize(list(v)) for v in product(*domains)],
    })
    if fs.get("target_domain_identity") != domain_identity:
        raise GenericNativePairError("producer target-domain identity mismatch")

    # ---- complete native cell projection, zero semantics preserved ----
    topology = _mapping(fs["target_topology"], "target_topology")
    if topology.get("arity") != 2:
        raise GenericNativePairError("native fact target topology arity mismatch")
    expected_cells = tuple((c, t) for c in domains[0] for t in domains[1])
    expected_keys = {canonical_json([c, t]) for c, t in expected_cells}
    seen: dict[str, Mapping[str, Any]] = {}
    for raw in _sequence(topology.get("complete_cell_semantic_projection"),
                         "complete_cell_semantic_projection", allow_empty=True):
        row = _mapping(raw, "joint cell")
        cell = _sequence(row.get("cell"), "joint cell identity")
        if len(cell) != 2:
            raise GenericNativePairError("joint cell must contain exactly two states")
        key = canonical_json([canonicalize(cell[0]), canonicalize(cell[1])])
        if key not in expected_keys or key in seen:
            raise GenericNativePairError("joint cell domain incomplete, duplicated or tampered")
        n = row.get("raw_numerator_support")
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            raise GenericNativePairError("joint support must be a nonnegative exact integer")
        cs = row.get("cell_state")
        if n == 0 and cs not in ZERO_CELL_STATES:
            raise GenericNativePairError("zero joint count has inconsistent cell state")
        if n > 0 and cs != "OBSERVED_POSITIVE":
            raise GenericNativePairError("positive joint count has inconsistent cell state")
        seen[key] = row
    if set(seen) != expected_keys:
        raise GenericNativePairError("native fact does not preserve the complete native joint domain")

    cond_denoms: dict[str, int] = {str(c): 0 for c in domains[0]}
    counts = {c: {str(t): 0 for t in domains[1]} for c in cond_denoms}
    zero_sem: dict[str, dict[str, str]] = {c: {str(t): "" for t in domains[1]} for c in cond_denoms}
    for cell_key, row in seen.items():
        cc, tt = json.loads(cell_key)
        key_c, key_t = str(cc), str(tt)
        cond_denoms[key_c] += int(row["raw_numerator_support"])
        counts[key_c][key_t] = int(row["raw_numerator_support"])
        if int(row["raw_numerator_support"]) == 0:
            zero_sem[key_c][key_t] = str(row["cell_state"])
    profile = tuple(
        {
            "condition_state": c,
            "source_native_conditioner": _derive_native_variable_name(conditioner_ref),
            "condition_denominator_support": cond_denoms[c],
            "target_counts": tuple(
                {
                    "target_state": t,
                    "source_native_target": _derive_native_variable_name(target_ref),
                    "joint_support_count": counts[c][t],
                    "joint_cell_state": ("OBSERVED_POSITIVE" if counts[c][t] > 0
                                         else zero_sem[c][t]),
                } for t in domains[1]
            ),
        }
        for c in domains[0]
    )

    eligible_total = int(fs.get("raw_denominator_support") or 0)
    producer_perm = tuple(sorted(set(producer_permission_ceiling)))
    if not producer_perm:
        raise GenericPermissionWideningError(
            "GF1_PRODUCER_PERMISSION_EMPTY: no producer grant")
    # None alone means the documented default; an explicit empty is no grant.
    rel_perm = (producer_perm if relation_permission_ceiling is None
                else tuple(sorted(set(relation_permission_ceiling))))
    if not rel_perm:
        raise GenericPermissionWideningError(
            "GF1_RELATION_PERMISSION_EMPTY: no relation grant")

    fields = dict(
        typed_state=typed,
        producer_state_blocking=(typed != "SUPPORTED"),
        conditioner_source_native_variable=_derive_native_variable_name(conditioner_ref),
        target_source_native_variable=_derive_native_variable_name(target_ref),
        conditioner_ref=conditioner_ref,
        target_ref=target_ref,
        conditioner_domain=tuple(domains[0]),
        target_domain=tuple(domains[1]),
        target_domain_identity=domain_identity,
        joint_order_semantics=FROZEN_JOINT_ORDER,
        operation_role_order=operation_role_order,
        native_component_order=tuple(a.object_id for a in native_order),
        risk_set_ref=fact_risk,
        risk_set_type=str(grain.get("risk_set_type", "COMMON_ELIGIBLE_RISK_SET")),
        empirical_universe_refs=universes,
        measure_kind="RAW",
        measure_basis_ref=_ref(fs["measure_basis_ref"], "measure_basis_ref"),
        source_scope_mode="SINGLE_UNIVERSE",
        response_state_semantics_ref=_ref(grain["response_state_semantics_ref"], "response semantics"),
        uncertainty_method_or_typed_state=str(grain.get("uncertainty_method_or_typed_state", "")),
        producer_fact_ref=joint_fact.ref,
        producer_query_ref=joint_query.ref,
        producer_authority_refs=authorities,
        producer_provenance_refs=provenance,
        producer_replay_ref=replay_ref,
        producer_condition_predicate_ref=_ref(fs["condition_predicate_ref"], "condition_predicate_ref"),
        producer_risk_set_member_refs=_ref_seq(fs.get("risk_set_member_refs") or (), "risk_set_member_refs"),
        producer_denominator_member_refs=_ref_seq(fs.get("denominator_member_refs") or (), "denominator_member_refs"),
        producer_permission_ceiling=producer_perm,
        relation_permission_ceiling=rel_perm,
        eligible_joint_risk_total=eligible_total,
        excluded_ineligible_target_count=0,
        conditional_count_profile=profile,
    )
    digest = semantic_hash(_projection(fields))
    obj = GenericNativePairRelation(
        **fields, content_hash=digest,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}")
    return obj


def _projection(f: Mapping[str, Any]) -> dict:
    """Same shape as the dataclass projection, used to precompute the digest."""
    tmp = dict(
        relation_family=GENERIC_RELATION_FAMILY, semantic_owner=GENERIC_RELATION_OWNER,
        grain=GENERIC_GRAIN,
        relation_semantics="EXACT_GENERIC_TWO_BINARY_ITEM_PAIR_CONDITIONAL_SUPPORT_PROFILE",
        typed_state=f["typed_state"], producer_state_blocking=f["producer_state_blocking"],
        roles={
            CONDITIONER_ROLE: {"source_native_variable": f["conditioner_source_native_variable"],
                               "ref": _ref_dict(f["conditioner_ref"])},
            TARGET_ROLE: {"source_native_variable": f["target_source_native_variable"],
                          "ref": _ref_dict(f["target_ref"])},
        },
        participant_cardinality=2, participant_role_order=list(ROLE_ORDER),
        state_order_semantics=STATE_ORDER_SEMANTICS,
        conditioner_domain=canonicalize(f["conditioner_domain"]),
        target_domain=canonicalize(f["target_domain"]),
        target_domain_identity=f["target_domain_identity"],
        joint_order_semantics=f["joint_order_semantics"],
        operation_role_order=f["operation_role_order"],
        native_component_order=list(f["native_component_order"]),
        risk_set_ref=_ref_dict(f["risk_set_ref"]), risk_set_type=f["risk_set_type"],
        empirical_universe_refs=[_ref_dict(r) for r in f["empirical_universe_refs"]],
        measure_kind=f["measure_kind"], measure_basis_ref=_ref_dict(f["measure_basis_ref"]),
        source_scope_mode=f["source_scope_mode"],
        response_state_semantics_ref=_ref_dict(f["response_state_semantics_ref"]),
        uncertainty_method_or_typed_state=f["uncertainty_method_or_typed_state"],
        producer_fact_ref=_ref_dict(f["producer_fact_ref"]),
        producer_query_ref=_ref_dict(f["producer_query_ref"]),
        producer_authority_refs=[_auth_dict(r) for r in f["producer_authority_refs"]],
        producer_provenance_refs=[_ref_dict(r) for r in f["producer_provenance_refs"]],
        producer_replay_ref=_ref_dict(f["producer_replay_ref"]),
        producer_condition_predicate_ref=_ref_dict(f["producer_condition_predicate_ref"]),
        producer_risk_set_member_refs=[_ref_dict(r) for r in f["producer_risk_set_member_refs"]],
        producer_denominator_member_refs=[_ref_dict(r) for r in f["producer_denominator_member_refs"]],
        producer_permission_ceiling=list(f["producer_permission_ceiling"]),
        relation_permission_ceiling=list(f["relation_permission_ceiling"]),
        eligible_joint_risk_total=f["eligible_joint_risk_total"],
        excluded_ineligible_target_count=f["excluded_ineligible_target_count"],
        information_loss=INFORMATION_LOSS,
        conditional_count_profile=canonicalize(f["conditional_count_profile"]),
        anti_inferences=list(ANTI_INFERENCES),
    )
    return tmp


def replay_generic_native_pair_relation(relation: GenericNativePairRelation,
                                        *, joint_fact, joint_query) -> dict:
    """Deterministic replay: re-derive and compare, exactly like the accepted owner."""
    fresh = produce_generic_native_pair_relation(
        joint_fact=joint_fact, joint_query=joint_query,
        conditioner_ref=relation.conditioner_ref, target_ref=relation.target_ref,
        producer_permission_ceiling=relation.producer_permission_ceiling,
        relation_permission_ceiling=relation.relation_permission_ceiling)
    if fresh.as_dict() != relation.as_dict():
        raise GenericNativePairError("GENERIC_RELATION_REPLAY_MISMATCH")
    return dict(replayed=True, object_id=fresh.object_id,
                content_hash=fresh.content_hash, matches_original=True)