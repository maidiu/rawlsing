"""I05 exact-bounded discovery -> existing I03 joint -> generic FF01 descriptor.

Conserves executed role/query/predicate/fact/receipt and typed *validation*
without re-running discovery, inventing a new I05 engine, choosing adaptive
stopping, or mistaking a VALID_EMPTY candidate for an absent empirical fact.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Mapping

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01ObservedJoint, receive_ff01_observed_joint,
)
from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryResult
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, exact_ref, semantic_hash,
)

CONTRACT = "S04_I05_TO_FF01_EXACT_ROLE_RECEPTION@1.0.0"


class FF01I05IngressError(ValueError):
    """I05 role/fact/receipt closure or FF01 use has failed."""


@dataclass(frozen=True)
class FF01I05RoleReceipt:
    payload: str
    digest: str

    def __post_init__(self) -> None:
        value = loads(self.payload)
        if (canonical_json(value) != self.payload
                or value.get("contract") != CONTRACT
                or semantic_hash(value) != self.digest):
            raise FF01I05IngressError("I05->FF01 receipt identity mismatch")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, f"urn:rawlsing:i05:ff01-role:sha256:{self.digest}", self.digest)

    def material(self) -> dict[str, Any]:
        return loads(self.payload)


def _ref(value: Any) -> ExactRef:
    try:
        return exact_ref(value)
    except (TypeError, KeyError, ValueError, AttributeError) as exc:
        raise FF01I05IngressError("missing exact I05 reference") from exc


def receive_i05_exact_joint_at_ff01(
    *,
    discovery: ExactBoundedDiscoveryResult,
    candidate_receipt_ref: ExactRef,
    query_role: str,
    conditioner_index: int,
    producer_permission_ceiling: tuple[str, ...] = ("FF01_DESCRIPTIVE_SOURCEFREE",),
) -> tuple[FF01ObservedJoint, FF01I05RoleReceipt]:
    """Read one actual I05 *query role* from its entire exact original result.

    This method requires one original single-universe executed I03 fact with
    k>=2 scalar target dimensions. It is NOT a general recursive engine and
    is NOT a selected model rank, even if I05 validated a candidate.
    """
    if type(discovery) is not ExactBoundedDiscoveryResult:
        raise FF01I05IngressError("exact original I05 result required")
    if type(candidate_receipt_ref) is not ExactRef or not isinstance(query_role, str) or not query_role.strip():
        raise FF01I05IngressError("exact receipt and query-role name required")
    receipts = [r for r in discovery.receipts if r.ref == candidate_receipt_ref]
    if len(receipts) != 1:
        raise FF01I05IngressError("receipt is not a unique member of exact evaluated frontier")
    receipt = receipts[0]
    if semantic_hash(receipt.semantic_projection()) != receipt.content_hash:
        raise FF01I05IngressError("discovery receipt semantic preimage mismatch")
    if _ref(receipt.evaluated_frontier_ref) != discovery.evaluated_frontier_ref:
        raise FF01I05IngressError("I05 receipt belongs to different frontier")
    if _ref(receipt.discovery_authority_ref) != discovery.discovery_authority_ref:
        raise FF01I05IngressError("I05 discovery authority ref substituted")
    if receipt.typed_state not in {
        "DISCOVERED_RESULT_SUPPORTED", "VALID_EMPTY", "INSUFFICIENT_SUPPORT",
        "NONCOMPARABLE", "COVERAGE_LIMITED", "PRUNED_BY_AUTHORITY", "UNEVALUATED"
    }:
        raise FF01I05IngressError("unknown I05 validation grade")
    identity = receipt.candidate_identity
    if not isinstance(identity, Mapping):
        raise FF01I05IngressError("missing candidate identity")
    role_rows = identity.get("query_roles")
    if not isinstance(role_rows, (list, tuple)):
        raise FF01I05IngressError("I05 receipt has no executed role catalogue")
    matches = [x for x in role_rows if isinstance(x, Mapping) and x.get("role") == query_role]
    if len(matches) != 1:
        raise FF01I05IngressError("selected role is absent or ambiguous")
    role = matches[0]
    qref = _ref(role.get("query_ref"))
    pref = _ref(role.get("predicate_ref"))
    query_matches = [q for q in discovery.executed_queries if q.ref == qref]
    predicate_matches = [p for p in discovery.executed_predicates if p.ref == pref]
    if len(query_matches) != 1 or len(predicate_matches) != 1:
        raise FF01I05IngressError("I05 role query or predicate exact preimage absent")
    query, predicate = query_matches[0], predicate_matches[0]
    if _ref(query.condition_predicate_ref) != predicate.ref:
        raise FF01I05IngressError("I05 role predicate substituted")
    if semantic_hash(query.semantic_projection()) != query.content_hash:
        raise FF01I05IngressError("I05 role query preimage was altered")
    if semantic_hash(predicate.semantic_projection()) != predicate.content_hash:
        raise FF01I05IngressError("I05 role predicate preimage was altered")
    support = receipt.support_uncertainty_state
    if not isinstance(support, Mapping):
        raise FF01I05IngressError("I05 support state missing")
    role_refs = support.get("query_role_fact_refs")
    if not isinstance(role_refs, Mapping) or query_role not in role_refs:
        raise FF01I05IngressError("I05 role-fact map missing")
    fact_ref_list = role_refs[query_role]
    if not isinstance(fact_ref_list, (list, tuple)) or len(fact_ref_list) != 1:
        raise FF01I05IngressError("one actual I03 fact per selected source role required")
    fact_ref = _ref(fact_ref_list[0])
    receipt_refs = {_ref(r) for r in receipt.empirical_fact_refs}
    if fact_ref not in receipt_refs or fact_ref not in set(discovery.empirical_fact_refs):
        raise FF01I05IngressError("I05 role fact not included in validated candidate/frontier")
    actual = [f for f in discovery.empirical_facts if f.ref == fact_ref]
    if len(actual) != 1 or _ref(actual[0].empirical_query_spec_ref) != query.ref:
        raise FF01I05IngressError("I05 fact/query closure lost")
    if _ref(actual[0].condition_predicate_ref) != predicate.ref:
        raise FF01I05IngressError("I05 fact/predicate closure lost")
    release_refs = tuple(sorted((_ref(ref) for ref in receipt.source_release_refs), key=lambda r: r.key))
    if len(release_refs) != 1 or release_refs[0] not in {_ref(ref) for ref in actual[0].source_empirical_provenance_refs}:
        raise FF01I05IngressError("I05 source release is not actual fact provenance")
    if len(query.empirical_universe_refs) != 1 or query.requested_output_grain.get("source_scope_mode") != "SINGLE_UNIVERSE":
        raise FF01I05IngressError("no pooling at generic FF01 I05 role")
    execution = QueryExecutionResult(
        query_ref=query.ref,
        facts=(actual[0],),
        source_scope_mode="SINGLE_UNIVERSE",
        release_refs=release_refs,
    )
    ff01 = receive_ff01_observed_joint(
        execution=execution,
        query=query,
        conditioner_index=conditioner_index,
        producer_permission_ceiling=producer_permission_ceiling,
    )
    if _ref(ff01.semantic_projection()["producer_fact_ref"]) != fact_ref:
        raise FF01I05IngressError("FF01 did not preserve actual selected I05 role fact")

    payload = {
        "contract": CONTRACT,
        "grade": "EXACT_I05_OWNED_FACT_WITH_RECONSTRUCTED_I03_ENVELOPE__NO_SCIENTIFIC_RANK",
        "discovery_authority_ref": discovery.discovery_authority_ref.as_dict(),
        "discovery_frontier_ref": discovery.evaluated_frontier_ref.as_dict(),
        "discovery_replay_ref": discovery.replay_ref.as_dict(),
        "candidate_receipt_ref": receipt.ref.as_dict(),
        "candidate_validation_state": receipt.typed_state,
        "candidate_coverage_state": receipt.coverage_state,
        "candidate_identity": canonicalize(identity),
        "query_role": query_role,
        "role_query_ref": query.ref.as_dict(),
        "role_predicate_ref": predicate.ref.as_dict(),
        "role_fact_ref": fact_ref.as_dict(),
        "ff01_ref": ff01.ref.as_dict(),
        "release_ref": release_refs[0].as_dict(),
        "no_new_authority": True,
        "not_proven": [
            "RECURSIVE_ADAPTIVE_SEARCH_NOT_PERFORMED_BY_THIS_READER",
            "VALID_EMPTY_DISCOVERY_VALIDATION_IS_NOT_ZERO_SOURCE_POPULATION",
            "I03_QUERY_EXECUTION_ENVELOPE_REASSEMBLED_FROM_I05_FACT_NOT_INDEPENDENT_EXECUTION",
            "SCIENCE_ESTIMATOR_AND_POSTSELECTION_UNISSUED",
            "N10E_N10W_FF02_V3_NOT_CONSUMED_BY_THIS_READER",
        ],
    }
    return ff01, FF01I05RoleReceipt(canonical_json(payload), semantic_hash(payload))


__all__ = ["CONTRACT", "FF01I05IngressError", "FF01I05RoleReceipt", "receive_i05_exact_joint_at_ff01"]
