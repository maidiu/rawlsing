"""GT12 E2B actual-object consumer harness preflight.

Test/integration jurisdiction only.  The public future entry point hard-requires
the current R1C query/fact/replay/predicate identities before invoking the
already-existing FIELD FORGE -> PRE-V3 -> relation-M1/V554 -> V557/V558 ->
V3 zero-positive APIs.

Synthetic ordinary PRE553 objects may use ``_run_bounded_chain`` only to prove
harness shape.  That private path is not currentness evidence and cannot issue
the real E2B terminal.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as c_to_d
from rawlsing_next import gt12_d_to_m4_typed_bridge as d_to_m4
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.gt12_permission_translation_authority import (
    ADOPTED_ADOPTION_RECEIPT_REF,
    ADOPTED_AUTHORITY_REF,
    ADOPTED_PRODUCER_ALLOWED_USES,
    ADOPTED_V557_ALLOWED_USES,
    ADOPTED_V558_REQUESTED_USES,
)
from rawlsing_next.gt12_e2b_publication_governance_binding import (
    load_current_gt12_e2b_publication_governance_binding,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import M1DecisionState
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef as M4AuthorityRef,
    V557DecisionState,
)
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.v3_psepf_zero_positive_guard import (
    GuardOutcome,
    GuardedTruthClass,
    evaluate_psepf_zero_positive_guard,
)


CURRENT_R1C_PREDICATE_HASH = (
    "bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3"
)
CURRENT_R1C_QUERY_HASH = (
    "e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0"
)
CURRENT_R1C_FACT_HASH = (
    "540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46"
)
CURRENT_R1C_REPLAY_HASH = (
    "c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f"
)

HISTORICAL_A3_QUERY_HASH = (
    "e91970c161736113201a3e9880034f8d088099aad67300a5aa689b7a08200670"
)
HISTORICAL_A3_FACT_HASH = (
    "7bdb8752df31905a737d1a21c2ada61fe0c64d9cb4db17ea9bb748a1cf25b27f"
)
HISTORICAL_A3_REPLAY_HASH = (
    "10c4c50af557fe92866c6033a424ba2ab56847400bf9f970e6666612f435cae0"
)

FROZEN_RISK_REF = ExactRef(
    "RISK_SET",
    adm.GT2_RISK_SET_ID,
    adm.GT2_RISK_SET_MEMBER_SET_SHA256,
)
FROZEN_FIELD_FORGE_PERMISSION_CEILING = (adm.GT2_TARGET_USE,)
FROZEN_V557_STATE = V557DecisionState.ALLOW_CONTEXT_ONLY
FORBIDDEN_PRODUCER_FAMILIES = frozenset({"V553", "V555", "V556"})
FORBIDDEN_PERMISSION_ATOMS = frozenset({"REVIEW", "ACTIVE_CAUSAL"})
REAL_CHAIN_STATE = "OPEN_PENDING_R4_ACTUAL_REPO_NATIVE_OBJECTS"


class GT12E2BHarnessError(ValueError):
    """The frozen E2B consumer chain failed closed."""


@dataclass(frozen=True)
class GT12E2BHarnessTerminal:
    relation: ff.ExactConditionalSupportProfile
    admission: Any
    m1_evaluation: Any
    v558_terminal: d_to_m4.RelationV558Terminal
    v3_decision: Any


def _require_current_identity_values(
    *,
    query_hash: str,
    fact_hash: str,
    replay_hash: str,
) -> None:
    if (
        query_hash,
        fact_hash,
        replay_hash,
    ) == (
        HISTORICAL_A3_QUERY_HASH,
        HISTORICAL_A3_FACT_HASH,
        HISTORICAL_A3_REPLAY_HASH,
    ):
        raise GT12E2BHarnessError(
            "historical A3 query/fact/replay identities are provenance only and are not current R1C"
        )
    if query_hash != CURRENT_R1C_QUERY_HASH:
        raise GT12E2BHarnessError("future real entry requires exact current R1C query identity")
    if fact_hash != CURRENT_R1C_FACT_HASH:
        raise GT12E2BHarnessError("future real entry requires exact current R1C EmpiricalFact identity")
    if replay_hash != CURRENT_R1C_REPLAY_HASH:
        raise GT12E2BHarnessError("future real entry requires exact current R1C replay identity")


def require_current_r1c_actual_objects(
    query: EmpiricalQuerySpec,
    fact: EmpiricalFact,
) -> None:
    """Hard future real-object boundary.  No fixture/proxy/current-hash injection."""
    if type(query) is not EmpiricalQuerySpec or type(fact) is not EmpiricalFact:
        raise GT12E2BHarnessError(
            "future real entry accepts only ordinary exact EmpiricalQuerySpec + EmpiricalFact"
        )
    if semantic_hash(query.semantic_projection()) != query.content_hash:
        raise GT12E2BHarnessError("query semantic identity is stale or corrupt")
    if semantic_hash(fact.semantic_projection()) != fact.content_hash:
        raise GT12E2BHarnessError("fact semantic identity is stale or corrupt")
    replay_ref = exact_ref(fact.replay_ref, "fact.replay_ref")
    _require_current_identity_values(
        query_hash=query.content_hash,
        fact_hash=fact.content_hash,
        replay_hash=replay_ref.content_hash,
    )
    query_predicate_ref = exact_ref(query.condition_predicate_ref, "query.condition_predicate_ref")
    fact_predicate_ref = exact_ref(fact.condition_predicate_ref, "fact.condition_predicate_ref")
    if query_predicate_ref.content_hash != CURRENT_R1C_PREDICATE_HASH:
        raise GT12E2BHarnessError("future real entry requires exact current R1C predicate identity")
    if exact_ref(fact.empirical_query_spec_ref, "fact.empirical_query_spec_ref") != query.ref:
        raise GT12E2BHarnessError("current fact does not bind the exact supplied current query")
    if fact_predicate_ref != query_predicate_ref:
        raise GT12E2BHarnessError("current fact/query predicate binding drift")
    if (
        exact_ref(fact.risk_set_ref, "fact.risk_set_ref") != FROZEN_RISK_REF
        or exact_ref(query.risk_set_ref, "query.risk_set_ref") != FROZEN_RISK_REF
    ):
        raise GT12E2BHarnessError("current R1C entry requires exact frozen 19,210 risk-set identity")
    if fact.typed_state != "SUPPORTED":
        raise GT12E2BHarnessError("real positive E2B requires current SUPPORTED EmpiricalFact")
    if fact.raw_denominator_support != adm.GT2_RISK_SET_ROWS:
        raise GT12E2BHarnessError("current R1C fact denominator is not exact frozen 19,210")
    targets = tuple(
        exact_ref(ref, "query.target_refs") for ref in query.target_refs
    )
    if len(targets) != 2:
        raise GT12E2BHarnessError("current R1C query must contain exact two-target Q86B -> Q86A order")
    topology = query.target_arity_and_topology
    if not isinstance(topology, Mapping):
        raise GT12E2BHarnessError("current query target topology is not exact mapping")
    if topology.get("joint_order_semantics") != ff.FROZEN_TARGET_ORDER:
        raise GT12E2BHarnessError("current query semantic order is not SEMANTIC_ORDERED")
    components = topology.get("components")
    if (
        not isinstance(components, Sequence)
        or isinstance(components, (str, bytes, bytearray))
        or len(components) != 2
    ):
        raise GT12E2BHarnessError("current query requires exact two ordered target components")
    try:
        component_refs = tuple(
            exact_ref(
                item.get("target_ref") if isinstance(item, Mapping) else None,
                "query.target_arity_and_topology.components.target_ref",
            )
            for item in components
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise GT12E2BHarnessError(
            "current query target component refs are not exact refs"
        ) from exc
    if component_refs != targets:
        raise GT12E2BHarnessError("current query target component order/ref binding drift")


def _require_repository_surface(terminal: d_to_m4.RelationV558Terminal) -> None:
    entries = terminal.repository.entries
    if not entries:
        raise GT12E2BHarnessError("V558 repository is empty")
    producer_families = {entry.obj.producer_family for entry in entries}
    if producer_families != {"V554"}:
        if producer_families & FORBIDDEN_PRODUCER_FAMILIES:
            raise GT12E2BHarnessError("V553/V555/V556 substitute lane is forbidden")
        raise GT12E2BHarnessError("E2B repository producer family must remain exact V554")
    for entry in entries:
        if entry.obj.producer_allowed_uses != ADOPTED_PRODUCER_ALLOWED_USES:
            raise GT12E2BHarnessError("V554 producer use widened beyond exact CONTEXT")
        if entry.governance.decision_state is not FROZEN_V557_STATE:
            raise GT12E2BHarnessError("V557 decision must remain exact ALLOW_CONTEXT_ONLY")
        if entry.governance.v557_allowed_uses != ADOPTED_V557_ALLOWED_USES:
            raise GT12E2BHarnessError("V557 allowed use must remain exact CONTEXT singleton")
        semantic_class = str(entry.obj.semantic_class).upper()
        if semantic_class.startswith(("ACTOR", "V3", "V2", "PERSONA", "RENDER")):
            raise GT12E2BHarnessError("actor/V3/V2 reverse-lane contamination in structural repository")
        if ADOPTED_AUTHORITY_REF not in entry.locator.producer_rule_bindings:
            raise GT12E2BHarnessError("adopted permission translation authority missing from locator")
        if ADOPTED_ADOPTION_RECEIPT_REF not in entry.locator.producer_rule_bindings:
            raise GT12E2BHarnessError("permission translation adoption receipt missing from locator")
    for resolved in terminal.resolution.resolved_entries:
        if resolved.canonical_producer_family != "V554":
            raise GT12E2BHarnessError("V558 resolved producer family drifted from V554")
        if resolved.resolver_allowed_uses != ADOPTED_V558_REQUESTED_USES:
            raise GT12E2BHarnessError("V558 resolver use must remain exact CONTEXT singleton")
        if set(resolved.resolver_allowed_uses) & FORBIDDEN_PERMISSION_ATOMS:
            raise GT12E2BHarnessError("REVIEW/ACTIVE_CAUSAL is forbidden in V558 resolution")
    if terminal.resolution.receipt.result_state != "RESOLUTION_COMPLETE":
        raise GT12E2BHarnessError("V558 exact CONTEXT resolution did not complete")


def _run_v3_zero_effect(terminal: d_to_m4.RelationV558Terminal) -> Any:
    receipt = terminal.resolution.receipt
    repository = terminal.repository
    state_hash = semantic_hash(
        {
            "e2b_preflight": "NO_ACTOR_STATE_MUTATION_SENTINEL",
            "repository_ref": repository.ref.as_dict(),
            "resolution_receipt_ref": receipt.ref.as_dict(),
        }
    )
    decision = evaluate_psepf_zero_positive_guard(
        {
            "actor_id": "GT12_E2B_NO_ACTOR_PROMOTION_SENTINEL",
            "source_class": GuardedTruthClass.V553_V558_STRUCTURAL_OBJECT.value,
            "source_ref": receipt.ref.object_id,
            "source_hash": receipt.ref.content_hash,
            "source_lineage": [GuardedTruthClass.STRUCTURAL_PRIOR_REPOSITORY.value],
            "transition_surface_id": "GT12_E2B_STRUCTURAL_CONTEXT_TO_ACTOR_STATE",
            "operation_class": "NO_POSITIVE_TRANSITION_AUTHORIZED",
            "state_fingerprint": {
                "actor_state_hash": state_hash,
                "causal_ledger_hash": state_hash,
                "causal_cursor": "0",
                "rng_state_hash": state_hash,
                "scheduler_state_hash": state_hash,
            },
        }
    )
    if decision.outcome is not GuardOutcome.DENY_ZERO_EFFECT or not decision.zero_effect:
        raise GT12E2BHarnessError(
            "future real E2B requires exact V3 DENY_ZERO_EFFECT with unchanged state fingerprint"
        )
    return decision


def _run_bounded_chain(
    query: EmpiricalQuerySpec,
    fact: EmpiricalFact,
    *,
    governed_use_id: str,
    v554_rule_ref: Mapping[str, Any],
    publication_authority: Mapping[str, Any],
    v557_authority_ref: M4AuthorityRef,
    _expected_conditioner_ref: ExactRef | None = None,
    _expected_target_ref: ExactRef | None = None,
) -> GT12E2BHarnessTerminal:
    """Mechanically compose existing public APIs.  Private synthetic-shape seam."""
    if type(query) is not EmpiricalQuerySpec or type(fact) is not EmpiricalFact:
        raise GT12E2BHarnessError("harness requires ordinary exact PRE553 query/fact objects")
    targets = tuple(exact_ref(ref, "query.target_refs") for ref in query.target_refs)
    if len(targets) != 2:
        raise GT12E2BHarnessError("harness requires exact two-target query")
    conditioner_ref = _expected_conditioner_ref or targets[0]
    target_ref = _expected_target_ref or targets[1]
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=conditioner_ref,
        target_ref=target_ref,
        producer_permission_ceiling=FROZEN_FIELD_FORGE_PERMISSION_CEILING,
        relation_permission_ceiling=FROZEN_FIELD_FORGE_PERMISSION_CEILING,
    )
    if relation.typed_state != "SUPPORTED" or relation.producer_state_blocking:
        raise GT12E2BHarnessError("non-SUPPORTED FIELD FORGE relation cannot enter positive E2B")
    admitted = c_to_d.admit_gt12_c_relation(relation)
    if admitted.admission.decision is not adm.AdmissionDecision.ADMITTED:
        raise GT12E2BHarnessError("FIELD FORGE relation did not receive exact positive PRE-V3 admission")
    _, evaluation = d_to_m4.evaluate_typed_d_to_e_at_v554(
        admitted.admission,
        governed_use_id=governed_use_id,
        v554_rule_ref=v554_rule_ref,
        publication_authority=publication_authority,
    )
    if evaluation.decision_state is not M1DecisionState.ELIGIBLE:
        raise GT12E2BHarnessError("relation M1/V554 did not remain exact ELIGIBLE")
    terminal = d_to_m4.publish_and_resolve_relation_v554_at_current_m4(
        admitted.admission,
        evaluation,
        v557_allowed_uses=ADOPTED_V557_ALLOWED_USES,
        requested_resolution_uses=ADOPTED_V558_REQUESTED_USES,
        v557_authority_ref=v557_authority_ref,
        v557_decision_state=FROZEN_V557_STATE,
    )
    _require_repository_surface(terminal)
    decision = _run_v3_zero_effect(terminal)
    return GT12E2BHarnessTerminal(
        relation=relation,
        admission=admitted.admission,
        m1_evaluation=evaluation,
        v558_terminal=terminal,
        v3_decision=decision,
    )


def run_current_r1c_e2b_actual_objects(
    query: EmpiricalQuerySpec,
    fact: EmpiricalFact,
) -> GT12E2BHarnessTerminal:
    """Real current entry: exact R1C objects plus fixed adopted authority binding."""
    require_current_r1c_actual_objects(query, fact)
    binding = load_current_gt12_e2b_publication_governance_binding()
    return _run_bounded_chain(
        query,
        fact,
        governed_use_id=binding.governed_use_id,
        v554_rule_ref=binding.v554_rule_ref,
        publication_authority=binding.publication_authority,
        v557_authority_ref=binding.v557_authority_ref,
    )


__all__ = [
    "CURRENT_R1C_PREDICATE_HASH",
    "CURRENT_R1C_QUERY_HASH",
    "CURRENT_R1C_FACT_HASH",
    "CURRENT_R1C_REPLAY_HASH",
    "HISTORICAL_A3_QUERY_HASH",
    "HISTORICAL_A3_FACT_HASH",
    "HISTORICAL_A3_REPLAY_HASH",
    "FROZEN_RISK_REF",
    "REAL_CHAIN_STATE",
    "GT12E2BHarnessError",
    "GT12E2BHarnessTerminal",
    "require_current_r1c_actual_objects",
    "run_current_r1c_e2b_actual_objects",
]
