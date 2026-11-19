"""S04 -> existing FF01 observed-joint first consumer, no second I03 query.

S04 owns the pre-Field-Forge full knowledge object. This adapter does NOT
query respondents or create another empirical store/estimator. It verifies
the original selected I03 execution against S04 before consuming S04's
already-produced joint cells. The original I03 fact is required because an
untrusted client can otherwise rehash a counterfeit S04 payload; a digest
alone does not issue SOURCE/CURRENT or scientific authority.

The result is the EXISTING FF01ObservedJoint ABI, not a parallel FF engine.
A caller must carry its own original source/host/CURRENT grant as usual.
"""
from __future__ import annotations

from itertools import product
from typing import Any, Iterable

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.field_forge_generic_empirical_ingress import (
    ANTI_INFERENCES, BLOCKED_GRADE, FAMILY, FF01ObservedJoint, GRADE,
    FF01GenericIngressError, _domain, _permission_set,
)
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec, ExactRef, canonical_json, canonicalize, exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, receive_s04_i03_research,
)


class S04FF01SeamError(FF01GenericIngressError):
    """No valid exact S04-issued, I03-backed FF01 descriptive reception."""


def _same(material: dict[str, Any], key: str, value: Any) -> None:
    if canonical_json(material.get(key)) != canonical_json(value):
        raise S04FF01SeamError("S04/FF01 source identity mismatch: " + key)


def receive_ff01_from_s04(
    *,
    knowledge: S04ObservedKnowledge,
    query: EmpiricalQuerySpec,
    execution: QueryExecutionResult,
    conditioner_index: int,
    producer_permission_ceiling: Iterable[str],
    relation_permission_ceiling: Iterable[str] | None = None,
) -> FF01ObservedJoint:
    """Value-consuming edge: one original I03 execution, S04, then FF01.

    Do NOT accept a self-rehashed S04 object alone as authenticated source.
    Reconcile it with the retained original I03 query and fact WITHOUT running
    I03 again. FF01 cells below are read from S04, not from execution.facts.
    """
    if (type(knowledge) is not S04ObservedKnowledge
            or type(query) is not EmpiricalQuerySpec
            or type(execution) is not QueryExecutionResult):
        raise S04FF01SeamError("actual S04 knowledge and original I03 query/result required")
    authenticated = receive_s04_i03_research(query=query, execution=execution)
    if authenticated.ref != knowledge.ref:
        raise S04FF01SeamError("S04 knowledge not issued by retained exact I03 fact")
    material = knowledge.material()
    if (material.get("source_authenticity")
            != "I03_HASH_AND_ISSUER_INTERNAL_CLOSURE__ORIGINAL_SOURCE_RIGHTS_UNVERIFIED"):
        raise S04FF01SeamError("S04 source authority falsely promoted")
    if material.get("source_scope_mode") != "SINGLE_UNIVERSE" or material.get("measure_kind") != "RAW":
        raise S04FF01SeamError("S04 cannot promote pooled or weighted science")
    for key, value in (
        ("query_ref", query.ref.as_dict()),
        ("fact_ref", execution.facts[0].ref.as_dict()),
        ("release_ref", execution.release_refs[0].as_dict()),
        ("full_query_target_topology", canonicalize(query.target_arity_and_topology)),
        ("target_refs", [
            exact_ref(x, "selected I03 target").as_dict() for x in query.target_refs
        ]),
    ):
        _same(material, key, value)

    targets, domains, domain_identity = _domain(query)
    if len(targets) < 2:
        raise S04FF01SeamError("existing FF01 requires genuine multi-target joint")
    if type(conditioner_index) is not int or not 0 <= conditioner_index < len(targets):
        raise S04FF01SeamError("FF01 conditioner is not an exact source role")
    if material["target_arity"] != len(targets):
        raise S04FF01SeamError("target arity changed at S04/FF01 seam")
    _same(material, "target_domains", [list(d) for d in domains])
    producer_permissions = _permission_set(producer_permission_ceiling, "producer permissions")
    relation_permissions = _permission_set(
        producer_permissions if relation_permission_ceiling is None else relation_permission_ceiling,
        "relation permissions",
    )
    if not set(relation_permissions).issubset(set(producer_permissions)):
        raise S04FF01SeamError("consumer permissions widen producer permissions")
    supported = material["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE"
    if supported != (material["producer_typed_state"] == "SUPPORTED"):
        raise S04FF01SeamError("S04 negative state/positive source disagreement")
    if supported and material["native_fact_target_domain_identity"] != domain_identity:
        raise S04FF01SeamError("S04 selected joint domain identity differs from I03")
    eligible = material["raw_eligible_condition_denominator"]
    resolved = material["raw_fully_resolved_joint_n"]
    if any(type(x) is not int or x < 0 for x in (eligible, resolved)) or resolved > eligible:
        raise S04FF01SeamError("I03 risk/resolved count contradiction")
    if material["per_cell_respondent_membership"] != "NOT_IN_AGGREGATE_EMPIRICAL_FACT":
        raise S04FF01SeamError("S04 invented per-cell respondent provenance")
    m = {
        "family": FAMILY,
        "claim_grade": GRADE if supported else BLOCKED_GRADE,
        "producer_state": material["producer_typed_state"],
        "source_permission_grade": "CALLER_DECLARED__NOT_INDEPENDENTLY_ISSUED",
        "producer_permission_ceiling": list(producer_permissions),
        "relation_permission_ceiling": list(relation_permissions),
        "producer_query_ref": material["query_ref"],
        "producer_fact_ref": material["fact_ref"],
        "producer_replay_ref": material["replay_ref"],
        "release_ref": material["release_ref"],
        "universe_ref": material["universe_ref"],
        "risk_set_ref": material["risk_set_ref"],
        "measure_basis_ref": material["measure_basis_ref"],
        "condition_predicate_ref": material["predicate_ref"],
        "authority_snapshot_refs": material["authority_refs"],
        "source_provenance_refs": material["source_provenance_refs"],
        "target_refs": material["target_refs"],
        "target_domain_identity": domain_identity,
        "conditioner_index": conditioner_index,
        "conditioner_ref": targets[conditioner_index].as_dict(),
        "joint_order_semantics": material["joint_order_semantics"],
        "joint_arity": len(targets),
        "raw_eligible_condition_denominator": eligible,
        "raw_fully_resolved_joint_n": resolved,
        "held_observed_n_if_nonpositive": None if supported else resolved,
        # Exact source-known-true/unknown condition extents are preserved
        # downstream as HELD provenance only, never candidate support.
        # The same original I03 fact was already revalidated above.
        "held_condition_membership_uncertainty": (
            {
                # FF01's producer permissions are caller-declared, not an
                # independently issued respondent-level access grant.
                # Preserve provenance by commitment to the exact roster
                # already held under source-scoped S04, never by exporting
                # identifying member refs into this portable receipt.
                "source_knowledge_ref": knowledge.ref.as_dict(),
                # The exact S04 knowledge ref already commits to the entire
                # authenticated source statement, including the restricted
                # roster. Do NOT publish a separate enumerable hash oracle
                # over respondent identifiers under caller-declared rights.
                "roster_binding": "EXACT_S04_KNOWLEDGE_REF_ONLY__NO_EXPORTED_ROSTER_DIGEST",
                "unknown_member_n": len(
                    material["source_unknown_condition_member_refs"]
                ),
                "member_refs_exported": False,
                "known_true_denominator_n": material["source_known_true_denominator_n"],
                "eligible_risk_n": material["source_eligible_risk_n"],
                "state": "UNRESOLVED_CONDITION_MEMBERSHIP__NO_FULL_DISTRIBUTION",
            }
            if not supported and "source_unknown_condition_member_refs" in material
            else None
        ),
        "uncertainty_state": material["producer_uncertainty_state"],
        "zero_means": (
            "OBSERVED_ZERO_WITHIN_SUPPORTED_ASKED_RISK__NOT_IMPOSSIBLE"
            if supported else "NO_ZERO_INFERENCE_FROM_NONPOSITIVE_PRODUCER_STATE"
        ),
        "complete_cells": [],
        "conditioned_complete_case_support": [],
        "not_proven": [
            "PER_CELL_RESPONDENT_MEMBERSHIP_NOT_PRESENT_IN_AGGREGATE_FACT",
            "RECURSIVE_DISCOVERY_NOT_ISSUED_BY_THIS_CONSUMER",
            "POPULATION_WEIGHT_VARIANCE_NOT_ESTABLISHED",
            "FF02_OR_MATERIAL_POWER_NOT_ISSUED",
            "PREDICTOR_IMPORTANCE_ESTIMATOR_NOT_ISSUED",
            "N10E_V3_ACTOR_NOT_CONSUMED_HERE",
        ],
        "anti_inferences": list(ANTI_INFERENCES),
    }
    if supported:
        if resolved <= 0:
            raise S04FF01SeamError("SUPPORTED source has no real joint")
        expected = {canonical_json(list(row)) for row in product(*domains)}
        found: dict[str, tuple[list[Any], int]] = {}
        for row in material["complete_cells"]:
            cell = canonicalize(row["cell"])
            key = canonical_json(cell)
            n = row["raw_count"]
            if (key not in expected or key in found or type(n) is not int or n < 0
                    or row["cell_state"] != (
                        "OBSERVED_POSITIVE" if n else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
                    )):
                raise S04FF01SeamError("altered S04 full joint cell/value/state")
            found[key] = (cell, n)
        if set(found) != expected or sum(n for _, n in found.values()) != resolved:
            raise S04FF01SeamError("S04 full joint no longer conserves original risk")
        m["respondent_extent_grade"] = (
            "INTERNALLY_CONSISTENT_I03_ENUMERATION__SOURCE_AUTHORITY_UNVERIFIED"
        )
        m["complete_cells"] = [
            {"cell": cell, "raw_support": n,
             "cell_state": "OBSERVED_POSITIVE" if n else "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"}
            for cell, n in (found[k] for k in sorted(found))
        ]
        for state in domains[conditioner_index]:
            selected = [
                {"remaining_state": [v for j, v in enumerate(cell) if j != conditioner_index],
                 "raw_support": n}
                for cell, n in found.values() if cell[conditioner_index] == state
            ]
            m["conditioned_complete_case_support"].append({
                "condition_value": state,
                "fully_resolved_condition_n": sum(x["raw_support"] for x in selected),
                "remaining_joint_cells": sorted(
                    selected, key=lambda x: canonical_json(x["remaining_state"])
                ),
            })
    elif material["complete_cells"] or (
        resolved > 0 and material["producer_typed_state"] not in (
            "LOW_SUPPORT", "UNCERTAINTY_UNQUANTIFIED", "UNRESOLVED"
        )
    ):
        raise S04FF01SeamError("held I03 evidence falsely promoted to observed joint")
    digest = semantic_hash(m)
    return FF01ObservedJoint(
        projection_json=canonical_json(m), content_hash=digest,
        object_id=f"urn:rawlsing:ff01:observed-joint:sha256:{digest}",
    )


__all__ = ["S04FF01SeamError", "receive_ff01_from_s04"]
