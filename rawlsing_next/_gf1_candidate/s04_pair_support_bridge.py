"""KUDA-074/075: bounded non-Q86 native I03 -> S04 -> GF1 first-consumer.

No source reader, query engine, new authority, generic Field Forge science,
predictor ranking, real dyad, pressure mechanism or actor is issued here.
The existing native I03 execution and S04 receipt are reused unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next._gf1_candidate.generic_native_pair_relation import (
    GENERIC_GRAIN,
    GenericNativePairRelation,
    produce_generic_native_pair_relation,
)
from rawlsing_next._gf1_candidate.gf1_pair_support_consumer import (
    compute_pair_support_signature,
)
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec, ExactRef, semantic_hash,
)
from rawlsing_next.pre553_s04_first_consumer import S04OnePassResult


class GF1S04FirstConsumerError(ValueError):
    """Exact prior execution/S04 custody or sourcefree scope is missing."""


@dataclass(frozen=True)
class GF1S04FirstConsumer:
    s04_knowledge_ref: ExactRef
    source_query_ref: ExactRef
    source_fact_ref: ExactRef
    relation: GenericNativePairRelation
    signature: Mapping[str, Any]
    grade: str = GENERIC_GRAIN


def receive_gf1_pair_from_s04(
    *,
    s04: S04OnePassResult,
    query: EmpiricalQuerySpec,
    producer_permission_ceiling: tuple[str, ...] = ("GF1_SOURCEFREE_TEST",),
) -> GF1S04FirstConsumer:
    """Compute a test-only real GF1 result from a *previous* genuine I03/S04.

    The native query itself determines role ordering. Reverse, non-binary,
    unsupported and unissued scientific requests are rejected by the existing
    GF1 producer/consumer. Do not silently coerce a pair into frozen Q86 GT2.
    """
    if type(s04) is not S04OnePassResult or type(query) is not EmpiricalQuerySpec:
        raise GF1S04FirstConsumerError("exact existing S04 and query required")
    if s04.ff01 is not None:
        raise GF1S04FirstConsumerError(
            "specialized FF01 and generic GF1 must remain separate owners"
        )
    execution = s04.execution
    if (query.ref != execution.query_ref or len(query.target_refs) != 2
            or len(execution.facts) != 1):
        raise GF1S04FirstConsumerError("exact two-target native execution required")
    fact = execution.facts[0]
    if fact.typed_state != "SUPPORTED":
        raise GF1S04FirstConsumerError(
            "unavailable or unresolved empirical fact cannot become a supported GF1 relation"
        )
    material = s04.knowledge.material()
    if (material.get("source_query_ref") != query.ref.as_dict()
            or material.get("fact_ref") != fact.ref.as_dict()
            or s04.receipt.material().get("s04_knowledge_ref")
                != s04.knowledge.ref.as_dict()
            or s04.receipt.material().get("source_fact_ref") != fact.ref.as_dict()):
        raise GF1S04FirstConsumerError(
            "S04 knowledge/query/fact/receipt custody differs from native execution"
        )
    relation = produce_generic_native_pair_relation(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=query.target_refs[0],
        target_ref=query.target_refs[1],
        producer_permission_ceiling=producer_permission_ceiling,
        relation_permission_ceiling=producer_permission_ceiling,
    )
    signature = compute_pair_support_signature(relation)
    if (signature.get("decision_state") != "PAIR_SUPPORT_SIGNATURE_COMPUTED"
            or signature.get("downstream_value_produced") is not True
            or signature.get("read_relation_content_hash") != relation.content_hash):
        raise GF1S04FirstConsumerError("GF1 consumer did not produce a bound value")
    return GF1S04FirstConsumer(
        s04_knowledge_ref=s04.knowledge.ref,
        source_query_ref=query.ref,
        source_fact_ref=fact.ref,
        relation=relation,
        signature=signature,
    )


__all__ = [
    "GF1S04FirstConsumerError", "GF1S04FirstConsumer",
    "receive_gf1_pair_from_s04",
]
