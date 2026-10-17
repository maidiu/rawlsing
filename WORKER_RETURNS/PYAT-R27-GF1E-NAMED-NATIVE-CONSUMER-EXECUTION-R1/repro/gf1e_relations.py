"""GF1E differential-pattern relation builders.

Constructs authentic immutable ``GenericNativePairRelation`` instances (with
correctly recomputed ``object_id``/``content_hash``) for the four separation
patterns the consumer must classify.  These are used by the differential test
and by the cold-process child so both exercise the exact same inputs.
"""
from __future__ import annotations

from generic_native_pair_relation import (
    GenericNativePairRelation,
    semantic_hash,
    _projection,
)
from rawlsing_next._pre553_query_common import ExactRef, AuthorityRef


def _ref(kind, oid, ch):
    return ExactRef(kind, oid, ch)


def build_pair_relation(cells: dict, eligible: int) -> GenericNativePairRelation:
    """Build a SUPPORTED two-binary-item relation for a 2x2 cell table.

    ``cells`` maps ``condition_state`` -> ``{target_state: count}``.  The
    relation identity is recomputed, so the dataclass constructor accepts it
    only when the semantic projection matches.
    """
    cond_order = sorted(cells)
    target_order = sorted(next(iter(cells.values())))

    profile = []
    for c in cond_order:
        denom = sum(cells[c][t] for t in target_order)
        profile.append({
            "condition_state": c,
            "source_native_conditioner": "m01-X",
            "condition_denominator_support": denom,
            "target_counts": tuple({
                "target_state": t,
                "source_native_target": "m01-Y",
                "joint_support_count": cells[c][t],
                "joint_cell_state": ("OBSERVED_POSITIVE" if cells[c][t] > 0
                                     else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"),
            } for t in target_order),
        })

    fields = dict(
        typed_state="SUPPORTED",
        producer_state_blocking=False,
        conditioner_source_native_variable="m01-X",
        target_source_native_variable="m01-Y",
        conditioner_ref=_ref("QUESTION_NATIVE", "urn:test:gf1e:cond", "1" * 64),
        target_ref=_ref("QUESTION_NATIVE", "urn:test:gf1e:tgt", "2" * 64),
        conditioner_domain=tuple(cond_order),
        target_domain=tuple(target_order),
        target_domain_identity="0" * 64,
        joint_order_semantics="SEMANTIC_ORDERED",
        operation_role_order="FORWARD_NATIVE_ORDER",
        native_component_order=("urn:test:gf1e:cond", "urn:test:gf1e:tgt"),
        risk_set_ref=_ref("RISK_SET", "urn:test:gf1e:risk", "3" * 64),
        risk_set_type="COMMON_ELIGIBLE_RISK_SET",
        empirical_universe_refs=(_ref("UNIVERSE", "urn:test:gf1e:universe", "4" * 64),),
        measure_kind="RAW",
        measure_basis_ref=_ref("MEASURE_BASIS", "urn:test:gf1e:basis", "5" * 64),
        source_scope_mode="SINGLE_UNIVERSE",
        response_state_semantics_ref=_ref("RESP_SEM", "urn:test:gf1e:resp", "6" * 64),
        uncertainty_method_or_typed_state="",
        producer_fact_ref=_ref("EMPIRICAL_FACT", "urn:test:gf1e:fact", "7" * 64),
        producer_query_ref=_ref("EMPIRICAL_QUERY", "urn:test:gf1e:query", "8" * 64),
        producer_authority_refs=(AuthorityRef("urn:test:gf1e:auth", "1", "9" * 64),),
        producer_provenance_refs=(_ref("PROVENANCE", "urn:test:gf1e:prov", "a" * 64),),
        producer_replay_ref=_ref("REPLAY", "urn:test:gf1e:replay", "b" * 64),
        producer_condition_predicate_ref=_ref("PREDICATE", "urn:test:gf1e:pred", "c" * 64),
        producer_risk_set_member_refs=(_ref("RISK_MEMBER", "urn:test:gf1e:member", "d" * 64),),
        producer_denominator_member_refs=(_ref("DENOM_MEMBER", "urn:test:gf1e:dmember", "e" * 64),),
        producer_permission_ceiling=("SOURCE_FREE_DEV",),
        relation_permission_ceiling=("SOURCE_FREE_DEV",),
        eligible_joint_risk_total=eligible,
        excluded_ineligible_target_count=0,
        conditional_count_profile=tuple(profile),
    )
    digest = semantic_hash(_projection(fields))
    return GenericNativePairRelation(
        **fields, content_hash=digest,
        object_id=f"urn:rawlsing:gf1:generic-pair-relation:sha256:{digest}")


PATTERNS = {
    "EXACT_PAIR_SEPARATION": ({"0": {"0": 1, "1": 0}, "1": {"0": 0, "1": 1}}, 2),
    "NO_PAIR_SEPARATION": ({"0": {"0": 0, "1": 1}, "1": {"0": 0, "1": 1}}, 2),
    "UNDETERMINED_NO_ELIGIBLE_RISK": ({"0": {"0": 0, "1": 0}, "1": {"0": 0, "1": 1}}, 1),
    "UNDETERMINED_ZERO_SUPPORT_RISK": ({"0": {"0": 0, "1": 0}, "1": {"0": 0, "1": 0}}, 0),
}


def four_relations():
    return {name: build_pair_relation(cells, eligible)
            for name, (cells, eligible) in PATTERNS.items()}
