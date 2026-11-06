"""Source-neutral empirical-fact ingress to the existing FIELD FORGE relation owner.

This module is a thin, typed facade.  It does not compute conditional support,
reinterpret source values, invent target roles, grant structural meaning, or
replace the frozen GT2 FIELD FORGE owner or the GT12-C->D bridge.

Input: one exact current ``EmpiricalFact`` + ``EmpiricalQuerySpec``.
Output: either the existing frozen ``ExactConditionalSupportProfile`` plus a
typed bridge state, or a typed refusal naming why the existing relation owner
cannot lawfully consume that fact.  Structural admission is never granted here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as bridge
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    exact_ref,
    semantic_hash,
)

INGRESS_CONTRACT_ID = "PRE553_FIELD_FORGE_EMPIRICAL_INGRESS@1.0.0"
INGRESS_RESULT_SCHEMA = "PRE553_FIELD_FORGE_EMPIRICAL_INGRESS_RESULT@1"
STATE_CONDITIONAL_SUPPORT = "CONDITIONAL_SUPPORT_PROFILE"
STATE_TYPED_REFUSAL = "TYPED_REFUSAL"
BRIDGE_TYPED_EVIDENCE = "TYPED_BRIDGE_EVIDENCE_ONLY"
BRIDGE_REFUSED = "BRIDGE_TYPED_REFUSAL"
STRUCTURAL_WITHHELD = "WITHHELD__NO_STRUCTURAL_ADMISSION_GRANT"
REFUSAL_TWO_TARGET_REQUIRED = "FIELD_FORGE_TWO_TARGET_RELATION_REQUIRED"
REFUSAL_RELATION = "FIELD_FORGE_RELATION_TYPED_REFUSAL"


class FieldForgeEmpiricalIngressError(Pre553IntegrityError):
    """Malformed ingress input; never a semantic or structural grant."""


@dataclass(frozen=True)
class FieldForgeEmpiricalIngressResult:
    contract_id: str
    state: str
    fact_ref: ExactRef
    query_ref: ExactRef
    conditioner_ref: ExactRef | None
    target_ref: ExactRef | None
    relation: ff.ExactConditionalSupportProfile | None
    bridge_state: str
    bridge_evidence_ref: ExactRef | None
    bridge_refusal: str
    refusal_code: str
    refusal_detail: str
    structural_grant: bool
    structural_state: str

    def material(self) -> dict[str, Any]:
        relation = self.relation
        return {
            "schema": INGRESS_RESULT_SCHEMA,
            "contract_id": self.contract_id,
            "state": self.state,
            "fact_ref": self.fact_ref.as_dict(),
            "query_ref": self.query_ref.as_dict(),
            "conditioner_ref": None if self.conditioner_ref is None else self.conditioner_ref.as_dict(),
            "target_ref": None if self.target_ref is None else self.target_ref.as_dict(),
            "relation_ref": None if relation is None else relation.ref.as_dict(),
            "relation_family": None if relation is None else relation.family,
            "relation_typed_state": None if relation is None else relation.typed_state,
            "bridge_state": self.bridge_state,
            "bridge_evidence_ref": None if self.bridge_evidence_ref is None else self.bridge_evidence_ref.as_dict(),
            "bridge_refusal": self.bridge_refusal,
            "refusal_code": self.refusal_code,
            "refusal_detail": self.refusal_detail,
            "structural_grant": self.structural_grant,
            "structural_state": self.structural_state,
        }


def _exact_fact_query(fact: EmpiricalFact, query: EmpiricalQuerySpec) -> None:
    if not isinstance(fact, EmpiricalFact):
        raise FieldForgeEmpiricalIngressError("ingress requires an exact EmpiricalFact")
    if not isinstance(query, EmpiricalQuerySpec):
        raise FieldForgeEmpiricalIngressError("ingress requires an exact EmpiricalQuerySpec")
    if semantic_hash(fact.semantic_projection()) != fact.content_hash:
        raise FieldForgeEmpiricalIngressError("fact semantic identity mismatch")
    if semantic_hash(query.semantic_projection()) != query.content_hash:
        raise FieldForgeEmpiricalIngressError("query semantic identity mismatch")
    if exact_ref(fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref") != query.ref:
        raise FieldForgeEmpiricalIngressError("fact does not bind supplied query identity")


def ingest_empirical_fact(
    *,
    fact: EmpiricalFact,
    query: EmpiricalQuerySpec,
    conditioner_ref: ExactRef | Mapping[str, Any] | None = None,
    target_ref: ExactRef | Mapping[str, Any] | None = None,
    producer_permission_ceiling: Iterable[str] = ("FIELD_FORGE_RELATION_PRODUCTION",),
    relation_permission_ceiling: Iterable[str] | None = None,
    try_structural_bridge: bool = True,
) -> FieldForgeEmpiricalIngressResult:
    """Feed one exact empirical fact through the existing frozen FF owner.

    The owner, target roles, and bridge are existing code.  This facade only
    selects the two declared targets, delegates, and converts owner refusals to
    typed outcomes.  It never calls GT12-D admission and never grants structural
    meaning.
    """
    _exact_fact_query(fact, query)
    topology = query.target_arity_and_topology
    arity = topology.get("arity") if isinstance(topology, Mapping) else None
    if arity != 2:
        return FieldForgeEmpiricalIngressResult(
            INGRESS_CONTRACT_ID, STATE_TYPED_REFUSAL, fact.ref, query.ref,
            None, None, None, BRIDGE_REFUSED, None, "",
            REFUSAL_TWO_TARGET_REQUIRED,
            f"FIELD FORGE conditional support requires exactly two targets; got {arity!r}",
            False, STRUCTURAL_WITHHELD,
        )
    targets = tuple(exact_ref(v, "query.target_refs") for v in query.target_refs)
    if len(targets) != 2:
        return FieldForgeEmpiricalIngressResult(
            INGRESS_CONTRACT_ID, STATE_TYPED_REFUSAL, fact.ref, query.ref,
            None, None, None, BRIDGE_REFUSED, None, "",
            REFUSAL_TWO_TARGET_REQUIRED,
            "FIELD FORGE conditional support requires exactly two target refs",
            False, STRUCTURAL_WITHHELD,
        )
    conditioner = exact_ref(conditioner_ref, "conditioner_ref") if conditioner_ref is not None else targets[0]
    target = exact_ref(target_ref, "target_ref") if target_ref is not None else targets[1]
    try:
        relation = ff.produce_exact_conditional_support_profile(
            joint_fact=fact,
            joint_query=query,
            conditioner_ref=conditioner,
            target_ref=target,
            producer_permission_ceiling=producer_permission_ceiling,
            relation_permission_ceiling=relation_permission_ceiling,
        )
    except ff.FieldForgeConditionalSupportError as exc:
        return FieldForgeEmpiricalIngressResult(
            INGRESS_CONTRACT_ID, STATE_TYPED_REFUSAL, fact.ref, query.ref,
            conditioner, target, None, BRIDGE_REFUSED, None, "",
            REFUSAL_RELATION, str(exc), False, STRUCTURAL_WITHHELD,
        )
    bridge_state = BRIDGE_REFUSED
    bridge_ref: ExactRef | None = None
    bridge_refusal = ""
    if try_structural_bridge:
        try:
            evidence = bridge.bridge_gt12_c_relation_to_d_evidence(relation)
        except Exception as exc:
            bridge_refusal = type(exc).__name__ + ":" + str(exc)
        else:
            bridge_state = BRIDGE_TYPED_EVIDENCE
            bridge_ref = evidence.relation_ref
    return FieldForgeEmpiricalIngressResult(
        INGRESS_CONTRACT_ID, STATE_CONDITIONAL_SUPPORT, fact.ref, query.ref,
        conditioner, target, relation, bridge_state, bridge_ref, bridge_refusal,
        "", "", False, STRUCTURAL_WITHHELD,
    )


__all__ = [
    "BRIDGE_REFUSED",
    "BRIDGE_TYPED_EVIDENCE",
    "INGRESS_CONTRACT_ID",
    "INGRESS_RESULT_SCHEMA",
    "REFUSAL_RELATION",
    "REFUSAL_TWO_TARGET_REQUIRED",
    "STATE_CONDITIONAL_SUPPORT",
    "STATE_TYPED_REFUSAL",
    "STRUCTURAL_WITHHELD",
    "FieldForgeEmpiricalIngressError",
    "FieldForgeEmpiricalIngressResult",
    "ingest_empirical_fact",
]
