"""GF1F — the reviewer's OWN synthetic GenericNativePairRelation builder.

Independent of the GF1E author's differential helper: different field values,
different naming, built only from the relation dataclass schema and the
relation module's own `_projection`/`semantic_hash` so the committed identity is
correct.  Used for the exhaustive universe, the named cases and the mutation
attacks.
"""
from __future__ import annotations

from generic_native_pair_relation import (
    GenericNativePairRelation,
    semantic_hash,
    _projection,
)
from rawlsing_next._pre553_query_common import ExactRef, AuthorityRef


def _r(kind, name, char):
    return ExactRef(kind, "urn:gf1f:review:" + name, char * 64)


def build_relation(cells, *, eligible=None, typed_state="SUPPORTED",
                   operation_role_order="FORWARD_NATIVE_ORDER",
                   conditioner_var="REV_COND", target_var="REV_TARG",
                   conditioner_domain=("0", "1"), target_domain=("0", "1"),
                   excluded=0):
    """Build a frozen relation whose 2x2 is exactly ``cells`` in [cond,targ] order."""
    eligible = sum(cells.values()) if eligible is None else eligible
    profile = []
    for c in conditioner_domain:
        row_counts = tuple(
            dict(target_state=t,
                 source_native_target=target_var,
                 joint_support_count=int(cells[c + t]),
                 joint_cell_state=("OBSERVED_POSITIVE" if cells[c + t] > 0
                                   else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"))
            for t in target_domain)
        profile.append(dict(
            condition_state=c,
            source_native_conditioner=conditioner_var,
            condition_denominator_support=sum(int(cells[c + t]) for t in target_domain),
            target_counts=row_counts))

    fields = dict(
        typed_state=typed_state,
        producer_state_blocking=(typed_state != "SUPPORTED"),
        conditioner_source_native_variable=conditioner_var,
        target_source_native_variable=target_var,
        conditioner_ref=_r("QUESTION_NATIVE", "cond", "1"),
        target_ref=_r("QUESTION_NATIVE", "targ", "2"),
        conditioner_domain=tuple(conditioner_domain),
        target_domain=tuple(target_domain),
        target_domain_identity="a" * 64,
        joint_order_semantics="SEMANTIC_ORDERED",
        operation_role_order=operation_role_order,
        native_component_order=("urn:gf1f:review:cond", "urn:gf1f:review:targ"),
        risk_set_ref=_r("RISK_SET", "risk", "3"),
        risk_set_type="COMMON_ELIGIBLE_RISK_SET",
        empirical_universe_refs=(_r("UNIVERSE", "universe", "4"),),
        measure_kind="RAW",
        measure_basis_ref=_r("MEASURE_BASIS", "basis", "5"),
        source_scope_mode="SINGLE_UNIVERSE",
        response_state_semantics_ref=_r("RESP_SEM", "resp", "6"),
        uncertainty_method_or_typed_state="",
        producer_fact_ref=_r("EMPIRICAL_FACT", "fact", "7"),
        producer_query_ref=_r("EMPIRICAL_QUERY", "query", "8"),
        producer_authority_refs=(AuthorityRef("urn:gf1f:review:auth", "1", "9" * 64),),
        producer_provenance_refs=(_r("PROVENANCE", "prov", "a"),),
        producer_replay_ref=_r("REPLAY", "replay", "b"),
        producer_condition_predicate_ref=_r("PREDICATE", "pred", "c"),
        producer_risk_set_member_refs=(_r("RISK_MEMBER", "member", "d"),),
        producer_denominator_member_refs=(_r("DENOM_MEMBER", "dmember", "e"),),
        producer_permission_ceiling=("SOURCE_FREE_DEV",),
        relation_permission_ceiling=("SOURCE_FREE_DEV",),
        eligible_joint_risk_total=int(eligible),
        excluded_ineligible_target_count=int(excluded),
        conditional_count_profile=tuple(profile) if typed_state == "SUPPORTED" else (),
    )
    digest = semantic_hash(_projection(fields))
    return GenericNativePairRelation(
        **fields, content_hash=digest,
        object_id="urn:rawlsing:gf1:generic-pair-relation:sha256:" + digest)


def cells_of(a, b, c, d):
    return {"00": a, "01": b, "10": c, "11": d}
