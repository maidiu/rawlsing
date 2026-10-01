"""C5/N5 — smallest production-facing current structural-context service.

This module is a *service over already-retained current owners*. It composes no
semantics of its own:

1. the current GT2 query/fact come only from
   ``pre553_repo_native_seal.load_current_gt2_query_fact()``;
2. the relation comes only from
   ``field_forge_conditional_support.produce_exact_conditional_support_profile``;
3. admission comes only from ``gt12_c_to_d_relation_bridge.admit_gt12_c_relation``;
4. consumption comes only from
   ``gt12_d_to_m4_typed_bridge.evaluate_typed_d_to_e_at_v554``;
5. publication/resolution come only from
   ``gt12_d_to_m4_typed_bridge.publish_and_resolve_relation_v554_at_current_m4``;
6. publication/governance material comes only from
   ``gt12_e2b_publication_governance_binding``
   .load_current_gt12_e2b_publication_governance_binding()``.

No caller arguments. No handwritten relation geometry, profile, ratio, topology
or publication. No semantic translation: the returned objects and refs are the
owners' own, returned unchanged so a caller can audit them.

Authority ceiling (all carried by the adopted governance bundle, asserted here,
never widened):

* target use exactly ``STRUCTURAL_MEDIATION_INPUT``;
* M1 contract ``M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0``;
* SIG-004 ``V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT``;
* V557 ``ALLOW_CONTEXT_ONLY`` with uses ``("CONTEXT",)``;
* V558 requested uses ``("CONTEXT",)``;
* publication family ``F1`` only;
* no REVIEW, no ACTIVE_CAUSAL, no actor state, no positive V3 authority.

In particular this service never claims conditioner=CAUSE, target=EFFECT,
support=mechanism, or population fact=actor fact. Those require separate
authority that this scope does not have and does not invent.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

CONTRACT_ID = "PYAT_C5_N5_CURRENT_GT2_STRUCTURAL_CONTEXT@1.0.0"

# ---------------------------------------------------------------------------
# Exact retained floor. These are the only current inputs this service accepts.
# A drift in any of them is a hard stop, not a silent recomputation.
# ---------------------------------------------------------------------------
RETAINED_QUERY_HASH = "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0"
RETAINED_FACT_HASH = "540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46"
RETAINED_REPLAY_HASH = "c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f"
RETAINED_RISK_SET_HASH = "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
RETAINED_FACT_STATE = "SUPPORTED"
RETAINED_DENOMINATOR = 19_210
RETAINED_CONDITIONER_VARIABLE = "Q86B"
RETAINED_TARGET_VARIABLE = "Q86A"
RETAINED_RELATION_IDENTITY = "1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19"
RETAINED_ADMISSION_IDENTITY = "a445e43da99405e0f8181f7ab6c428d9b0dd14fefc7fc5091f21f2d21f00b08d"

RETAINED_ADMISSION_AUTHORITY_ID = "GT2_FF_PREV3_RELATION_ADMISSION_AUTHORITY"
RETAINED_ADMISSION_AUTHORITY_VERSION = "R1"
RETAINED_ADMISSION_SCOPE = "CURRENT_FOR_FROZEN_GT2_CANARY_ONLY"
TARGET_USE = "STRUCTURAL_MEDIATION_INPUT"

M1_CONTRACT_ID = "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0"
M1_BASIS_KIND = "ADMITTED_FIELD_FORGE_RELATION"
M1_ROUTE = "V554_TO_V557_DIRECT"
SIG_004 = "V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT"
V557_STATE_NAME = "ALLOW_CONTEXT_ONLY"
V557_ALLOWED_USES = ("CONTEXT",)
V558_REQUESTED_USES = ("CONTEXT",)
V558_RESOLUTION_STATE = "RESOLUTION_COMPLETE"
PUBLICATION_FAMILY = "F1"
REQUIRED_PRODUCER_FAMILY = "V554"
FORBIDDEN_SUBSTITUTE_BASES = ("V553", "V555", "V556")
FORBIDDEN_USE_CLASSES = ("REVIEW", "ACTIVE_CAUSAL")

# Ceiling assertions the service makes about what it will NOT do.
CEILING_NO_ACTOR_STATE = True
CEILING_NO_POSITIVE_V3_AUTHORITY = True
CEILING_NO_CAUSAL_ROLE_IDENTITY = True
CEILING_NO_MECHANISM_IDENTITY = True


class CurrentGT2StructuralContextError(Exception):
    """Raised when the retained current structural context cannot be served."""


@dataclass(frozen=True)
class CurrentGT2StructuralContext:
    """Auditable result carrying the owners' own objects and refs, untranslated."""

    contract_id: str

    # Owner-produced objects, returned exactly as their owner produced them.
    query: Any
    fact: Any
    relation: Any
    admission: Any
    bridge: Any
    m1_evaluation: Any
    terminal: Any
    governance_binding: Any

    # Exact retained identities, read from the owner objects.
    query_ref: Mapping[str, Any]
    fact_ref: Mapping[str, Any]
    relation_ref: Mapping[str, Any]
    admission_ref: Mapping[str, Any]
    publication_id: str
    publication_hash: str
    resolution_key: str
    selection_record_id: str

    # What the service observed, without interpreting it.
    fact_state: str
    raw_denominator_support: int
    risk_set_ref: Mapping[str, Any]
    replay_ref: Mapping[str, Any]
    m1_decision_state: str
    m1_required_basis_kind: str
    v557_state: str
    v557_allowed_uses: tuple[str, ...]
    resolved_uses: tuple[str, ...]
    publication_family: str
    producer_family: str

    def audit_record(self) -> Mapping[str, Any]:
        """Return the auditable owner-produced view. No semantics added."""
        return {
            "contract_id": self.contract_id,
            "query_ref": dict(self.query_ref),
            "fact_ref": dict(self.fact_ref),
            "relation_ref": dict(self.relation_ref),
            "admission_ref": dict(self.admission_ref),
            "publication_id": self.publication_id,
            "publication_hash": self.publication_hash,
            "resolution_key": self.resolution_key,
            "selection_record_id": self.selection_record_id,
            "fact_state": self.fact_state,
            "raw_denominator_support": self.raw_denominator_support,
            "risk_set_ref": dict(self.risk_set_ref),
            "replay_ref": dict(self.replay_ref),
            "m1_decision_state": self.m1_decision_state,
            "m1_required_basis_kind": self.m1_required_basis_kind,
            "v557_state": self.v557_state,
            "v557_allowed_uses": list(self.v557_allowed_uses),
            "resolved_uses": list(self.resolved_uses),
            "publication_family": self.publication_family,
            "producer_family": self.producer_family,
        }


def _hash(value: Any) -> str:
    if hasattr(value, "content_hash"):
        return str(value.content_hash)
    if isinstance(value, Mapping):
        return str(value.get("content_hash", ""))
    return ""


def _enum_name(value: Any) -> str:
    """Return the bare enum member name, e.g. ELIGIBLE for M1DecisionState.ELIGIBLE."""
    return str(getattr(value, "name", None) or getattr(value, "value", None) or value)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CurrentGT2StructuralContextError(message)


def _verify_retained_floor(query: Any, fact: Any) -> None:
    """Fail closed unless the loaded current objects are the frozen canary."""
    _require(
        query.ref.content_hash == RETAINED_QUERY_HASH,
        f"current GT2 query drifted: {query.ref.content_hash}",
    )
    _require(
        fact.ref.content_hash == RETAINED_FACT_HASH,
        f"current GT2 fact drifted: {fact.ref.content_hash}",
    )
    _require(
        fact.typed_state == RETAINED_FACT_STATE,
        f"current GT2 fact state is {fact.typed_state!r}, not {RETAINED_FACT_STATE!r}",
    )
    _require(
        fact.raw_denominator_support == RETAINED_DENOMINATOR,
        f"current GT2 denominator is {fact.raw_denominator_support}, "
        f"not {RETAINED_DENOMINATOR}",
    )
    _require(
        _hash(dict(fact.replay_ref)) == RETAINED_REPLAY_HASH,
        "current GT2 replay ref drifted",
    )
    _require(
        _hash(dict(fact.risk_set_ref)) == RETAINED_RISK_SET_HASH,
        "current GT2 risk-set ref drifted",
    )


def _require_positive_admission(admission: Any) -> None:
    """Require exact positive ADMITTED for STRUCTURAL_MEDIATION_INPUT only."""
    _require(
        getattr(admission, "is_positive", False) is True,
        "current GT2 relation admission is not positive",
    )
    _require(
        str(getattr(admission, "decision", "")) .endswith("ADMITTED"),
        f"current GT2 relation admission decision is {getattr(admission, 'decision', None)!r}",
    )
    _require(
        tuple(admission.relation_permission_ceiling) == (TARGET_USE,),
        f"admission permission ceiling is {admission.relation_permission_ceiling!r}, "
        f"not exactly ({TARGET_USE!r},)",
    )
    _require(
        tuple(admission.applicable_negative_denial_noncomparability_refs) == (),
        "admission carries applicable negative/denial/noncomparability refs",
    )
    _require(
        admission.ref.content_hash == RETAINED_ADMISSION_IDENTITY,
        f"current GT2 admission identity drifted: {admission.ref.content_hash}",
    )


def _require_consumer_ceiling(result: "CurrentGT2StructuralContext") -> None:
    """Assert the adopted M1/V554/V557/V558 ceiling was honoured exactly."""
    _require(
        _enum_name(result.m1_decision_state) == "ELIGIBLE",
        f"M1 decision state is {result.m1_decision_state!r}, not ELIGIBLE",
    )
    _require(
        result.m1_required_basis_kind == M1_BASIS_KIND,
        f"M1 basis kind is {result.m1_required_basis_kind!r}",
    )
    _require(
        result.producer_family == REQUIRED_PRODUCER_FAMILY,
        f"resolved producer family is {result.producer_family!r}, "
        f"not {REQUIRED_PRODUCER_FAMILY!r}",
    )
    _require(
        result.publication_family == PUBLICATION_FAMILY,
        f"publication family is {result.publication_family!r}, not {PUBLICATION_FAMILY!r}",
    )
    _require(
        result.v557_state == V557_STATE_NAME,
        f"V557 state is {result.v557_state!r}, not {V557_STATE_NAME!r}",
    )
    _require(
        tuple(result.v557_allowed_uses) == V557_ALLOWED_USES,
        f"V557 allowed uses are {result.v557_allowed_uses!r}, not {V557_ALLOWED_USES!r}",
    )
    _require(
        tuple(result.resolved_uses) == V558_REQUESTED_USES,
        f"resolved uses are {result.resolved_uses!r}, not {V558_REQUESTED_USES!r}",
    )
    for forbidden in FORBIDDEN_SUBSTITUTE_BASES:
        _require(
            result.producer_family != forbidden,
            f"V558 resolved a {forbidden} substitute basis instead of V554",
        )
    for forbidden in FORBIDDEN_USE_CLASSES:
        _require(
            forbidden not in result.v557_allowed_uses and forbidden not in result.resolved_uses,
            f"forbidden use class {forbidden!r} reached the resolved context",
        )


def evaluate_current_gt2_structural_context() -> CurrentGT2StructuralContext:
    """Serve the one current GT2 structural context. No caller arguments.

    Every step is an existing retained owner called through its public API. This
    function adds no relation geometry, no profile, no ratio, no topology, no
    publication and no semantic translation.
    """
    # 1. Current retained query/fact -- only through the sealed repo-native loader.
    from rawlsing_next.pre553_repo_native_seal import load_current_gt2_query_fact

    query, fact = load_current_gt2_query_fact()
    _verify_retained_floor(query, fact)

    # The conditioner/target role and order are the frozen Q86B -> Q86A direction.
    conditioner_ref, target_ref = query.target_refs[0], query.target_refs[1]

    # 2. Relation -- only through FIELD FORGE conditional support.
    from rawlsing_next.field_forge_conditional_support import (
        produce_exact_conditional_support_profile,
    )

    relation = produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=conditioner_ref,
        target_ref=target_ref,
        producer_permission_ceiling=(TARGET_USE,),
    )
    _require(
        relation.ref.content_hash == RETAINED_RELATION_IDENTITY,
        f"current GT2 relation identity drifted: {relation.ref.content_hash}",
    )

    # 3. Admission -- only through the GT12 C->D relation bridge.
    from rawlsing_next.gt12_c_to_d_relation_bridge import admit_gt12_c_relation

    admitted = admit_gt12_c_relation(relation)
    admission = admitted.admission
    _require_positive_admission(admission)

    # 4. Consumption -- only through the typed D->E V554 bridge, using the
    #    adopted publication/governance binding (never caller-selected).
    from rawlsing_next.gt12_e2b_publication_governance_binding import (
        load_current_gt12_e2b_publication_governance_binding,
    )
    from rawlsing_next.gt12_d_to_m4_typed_bridge import (
        evaluate_typed_d_to_e_at_v554,
        publish_and_resolve_relation_v554_at_current_m4,
    )

    binding = load_current_gt12_e2b_publication_governance_binding()
    _require(
        binding.governed_use_id is not None,
        "current publication/governance binding lacks its governed use id",
    )
    bridge, m1_evaluation = evaluate_typed_d_to_e_at_v554(
        admission,
        governed_use_id=binding.governed_use_id,
        v554_rule_ref=binding.v554_rule_ref,
        publication_authority=binding.publication_authority,
    )

    # 5. Publication and resolution -- only through the M4 traversal.
    terminal = publish_and_resolve_relation_v554_at_current_m4(
        admission,
        m1_evaluation,
        v557_allowed_uses=V557_ALLOWED_USES,
        requested_resolution_uses=V558_REQUESTED_USES,
        v557_authority_ref=binding.v557_authority_ref,
        v557_decision_state=V557_STATE_NAME,
    )

    publication = terminal.publication
    resolution = terminal.resolution
    entries = tuple(publication.entries)
    _require(
        len(entries) == 1,
        f"current GT2 publication carries {len(entries)} entries, expected exactly 1",
    )
    entry = entries[0]
    selection = resolution.selection_records[0]

    result = CurrentGT2StructuralContext(
        contract_id=CONTRACT_ID,
        query=query,
        fact=fact,
        relation=relation,
        admission=admission,
        bridge=bridge,
        m1_evaluation=m1_evaluation,
        terminal=terminal,
        governance_binding=binding,
        query_ref=query.ref.as_dict(),
        fact_ref=fact.ref.as_dict(),
        relation_ref=relation.ref.as_dict(),
        admission_ref=admission.ref.as_dict(),
        publication_id=str(publication.publication_id),
        publication_hash=str(publication.publication_hash),
        resolution_key=str(terminal.resolution_keys[0]),
        selection_record_id=str(selection.selection_record_id),
        fact_state=str(fact.typed_state),
        raw_denominator_support=int(fact.raw_denominator_support),
        risk_set_ref=dict(fact.risk_set_ref),
        replay_ref=dict(fact.replay_ref),
        m1_decision_state=_enum_name(m1_evaluation.decision_state),
        m1_required_basis_kind=_enum_name(m1_evaluation.required_basis_kind),
        v557_state=V557_STATE_NAME,
        v557_allowed_uses=tuple(selection.v557_allowed_uses),
        resolved_uses=tuple(selection.producer_allowed_uses),
        publication_family=str(entry.obj.semantic_class),
        producer_family=str(entry.obj.producer_family),
    )
    _require_consumer_ceiling(result)
    return result


__all__ = [
    "CONTRACT_ID",
    "RETAINED_QUERY_HASH",
    "RETAINED_FACT_HASH",
    "RETAINED_REPLAY_HASH",
    "RETAINED_RISK_SET_HASH",
    "RETAINED_FACT_STATE",
    "RETAINED_DENOMINATOR",
    "RETAINED_CONDITIONER_VARIABLE",
    "RETAINED_TARGET_VARIABLE",
    "RETAINED_RELATION_IDENTITY",
    "RETAINED_ADMISSION_IDENTITY",
    "RETAINED_ADMISSION_AUTHORITY_ID",
    "RETAINED_ADMISSION_AUTHORITY_VERSION",
    "RETAINED_ADMISSION_SCOPE",
    "TARGET_USE",
    "M1_CONTRACT_ID",
    "M1_BASIS_KIND",
    "M1_ROUTE",
    "SIG_004",
    "V557_STATE_NAME",
    "V557_ALLOWED_USES",
    "V558_REQUESTED_USES",
    "V558_RESOLUTION_STATE",
    "PUBLICATION_FAMILY",
    "REQUIRED_PRODUCER_FAMILY",
    "FORBIDDEN_SUBSTITUTE_BASES",
    "FORBIDDEN_USE_CLASSES",
    "CurrentGT2StructuralContextError",
    "CurrentGT2StructuralContext",
    "evaluate_current_gt2_structural_context",
]