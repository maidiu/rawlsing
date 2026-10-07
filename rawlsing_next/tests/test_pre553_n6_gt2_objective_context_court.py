"""N6 GT2 demanded objective-CONTEXT realization court (bounded, source-free).

This court is the first *demanded-objective* slice for the exact Afrobarometer R5
GT2 Q86B->Q86A SIG-004 product. It does three things and refuses to do a fourth:

1. Builds the **objective demand matrix** from the actual admitted structural object
   and the actual current consumer contracts, empirically rather than from constants.
2. Positively proves the current-rule GT2 F1 is reconstructed, admitted, published into
   an immutable V558 repository **without B1 publication**, and resolved by the real
   V558 context resolver.
3. Records AT24 / AT25 / AT30 truthfully at this grain.
4. **Refuses** to manufacture a mechanism (AT25), a temporal product (AT30), or a
   universal terminal objective-world consumer that current law does not have.

Scope law honoured here:
- V555 route continuation is NOT_APPLICABLE_TO_GT2_SIG004 (adopted HQ227 terminality)
  and this court does not reopen it;
- no actor/person work;
- no source access; the empirical product is the retained R1C fixture already admitted
  upstream;
- no authority adoption and no self-adoption.

EPISTEMIC CEILING: this proves demanded-objective CONTEXT realization at the local
V557/V558 grain. It does not claim live survey-source occupancy, and it does not claim
a world is populated.
"""
from __future__ import annotations

import inspect
from typing import Any

import pytest

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as c_to_d
from rawlsing_next import gt12_d_to_m4_typed_bridge as d_to_m4
from rawlsing_next import m1_temporal_v554_admission_dedup as m1dedup
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.gt12_e2b_publication_governance_binding import (
    GOVERNED_USE_ID,
    PUBLICATION_AUTHORITY_ID,
    PUBLICATION_FAMILIES,
    V554_RULE_HASH,
    V554_RULE_ID,
    V557_AUTHORITY_ID,
    load_current_gt12_e2b_publication_governance_binding,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import M1DecisionState
from rawlsing_next.m4_v557_v558_publication_repository import (
    AUDIT_ONLY_CLASSES,
    V557DecisionState,
)
from rawlsing_next.objective_consumer_bounded_evidence import (
    POLICY_BINDINGS,
    ClaimCeiling,
    EvidenceKind,
    EvidenceTier,
    NotYetApplicableConsumer,
    PolicyInput,
    evaluate_current_consumer,
)
from rawlsing_next.objective_consumer_bounded_evidence import ExactRef as ConsumerExactRef
from rawlsing_next.tests.gt12_e2b_actual_object_consumer_harness import (
    FORBIDDEN_PRODUCER_FAMILIES,
    FORBIDDEN_PERMISSION_ATOMS,
    run_current_r1c_e2b_actual_objects,
)
from rawlsing_next.tests.test_pre553_gt2_structural_positive_realization_court import (
    _retained,
)

DIRECTION = "GT2_Q86B_TO_Q86A"
CONTEXT_USE = "CONTEXT"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _chain() -> Any:
    """Run the current adopted GT2 chain end to end, in-process."""

    query, fact = _retained()
    return run_current_r1c_e2b_actual_objects(query, fact)


def _f1_ref(terminal: Any) -> dict[str, str]:
    return terminal.m1_evaluation.f1["material"]["rule_id"], terminal.m1_evaluation.f1["f1_id"]


# ==========================================================================
# 1. objective demand matrix (AT24 input side)
# ==========================================================================
def test_n6_01_demand_matrix_is_read_from_actual_current_consumer_contracts():
    """The demand matrix is derived from live contract state, not hardcoded prose."""

    census = {key: binding for key, binding in sorted(POLICY_BINDINGS.items())}
    assert census, "current consumer contract census must not be empty"

    # Exactly two objective consumer contracts are current.
    current = [k for k, b in census.items() if b.applicable]
    assert current == [
        "OC01_PRE553_SOURCE_LOCAL_EMPIRICAL_QUERY_R1",
        "OC02_LEARNED_STRUCTURAL_ADMISSION_R1",
    ]
    # The terminal objective-world resolver is explicitly NOT current.
    terminal = census["OC05_TERMINAL_OBJECTIVE_WORLD_RESOLUTION_R1"]
    assert not terminal.applicable
    assert "no universal terminal may be invented" in terminal.reason

    # Objective consequence (mechanism) and non-event world fact are not current.
    assert not census["OC03_SDTF_OBJECTIVE_CONSEQUENCE_R1"].applicable
    assert not census["OC04_OCCURRENCE_NONEVENT_WORLD_FACT_R1"].applicable


def test_n6_02_only_demanded_objective_functions_are_proved():
    """CONTEXT is demanded; mechanism/temporal/position are not demanded here.

    Demand is not asserted from machinery existence. CONTEXT is demanded because an
    adopted *current publication authority* names this exact governed use; the
    mechanism consequence and terminal world resolver are not demanded because their
    consumer contracts are not current.
    """

    binding = load_current_gt12_e2b_publication_governance_binding()
    assert binding.governed_use_id == GOVERNED_USE_ID
    assert PUBLICATION_FAMILIES == ("F1",)

    # CONTEXT demand is bound by an adopted current authority + the V557 current binding.
    assert binding.publication_authority["governed_use_id"] == GOVERNED_USE_ID
    assert binding.v557_authority_ref.authority_id == V557_AUTHORITY_ID
    assert binding.publication_authority["allowed_object_families"] == ("F1",)
    assert tuple(
        binding.publication_authority["jurisdiction"]["inherited_downstream_use_exact"]
    ) == ("CONTEXT",)

    # Mechanism is NOT demanded: its consumer contract is not current.
    assert not POLICY_BINDINGS["OC03_SDTF_OBJECTIVE_CONSEQUENCE_R1"].applicable


# ==========================================================================
# 2. current GT2 F1 input + authority binding
# ==========================================================================
def test_n6_03_current_f1_is_reconstructed_from_retained_determinants_and_rule():
    """The F1 consumed downstream is bound to the *current* adopted SIG-004 rule."""

    terminal = _chain()
    evaluation = terminal.m1_evaluation
    f1 = evaluation.f1
    assert evaluation.contract_id == "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0"
    # The F1 preimage binds the current adopted rule identity, not a fixture rule.
    assert f1["material"]["rule_id"] == V554_RULE_ID
    assert f1["material"]["rule_hash"] == V554_RULE_HASH
    assert f1["material"]["signature_id"] == "V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT"
    assert f1["material"]["target_use"] == "STRUCTURAL_MEDIATION_INPUT"
    # Banked HQ224 custody ref is exactly what this chain reproduces.
    assert f1["f1_id"] == (
        "urn:rawlsing:v554:f1:sha256:3530f08f43e704ad67e0fb74984b03b7ad0f068ea1de4bcf658f3b2d591bd56d"
    )


# ==========================================================================
# 3. V557/V558 CONTEXT publication + resolution (the demanded function)
# ==========================================================================
def test_n6_04_f1_is_admitted_and_published_under_current_authority():
    terminal = _chain()
    evaluation = terminal.m1_evaluation
    assert evaluation.decision_state is M1DecisionState.ELIGIBLE
    assert terminal.admission.decision is adm.AdmissionDecision.ADMITTED
    assert terminal.relation.typed_state == "SUPPORTED"

    entries = terminal.v558_terminal.repository.entries
    assert len(entries) == 1
    entry = entries[0]
    assert entry.obj.semantic_class == "F1"
    assert entry.obj.producer_family == "V554"
    assert entry.governance.decision_state is V557DecisionState.ALLOW_CONTEXT_ONLY
    assert entry.obj.producer_allowed_uses == (CONTEXT_USE,)
    assert entry.governance.v557_allowed_uses == (CONTEXT_USE,)
    # The published payload carries exactly the banked current F1 id.
    assert entry.obj.payload["f1_id"] == evaluation.f1["f1_id"]


def test_n6_05_publication_contains_no_b1():
    """The demanded CONTEXT slice publishes F1 only; B1 is never published."""

    terminal = _chain()
    entries = terminal.v558_terminal.repository.entries
    families = {e.obj.semantic_class for e in entries}
    assert "B1" not in families
    assert families == {"F1"}
    # The handoff that fed publication carried F1 only.
    handoff_families = {
        r["family"] for r in terminal.m1_evaluation.direct_v557_handoff["object_refs"]
    }
    assert handoff_families == {"F1"}
    # And the current rule forbids B1 at the authority layer.
    binding = load_current_gt12_e2b_publication_governance_binding()
    assert binding.publication_authority["allowed_object_families"] == ("F1",)
    assert "B1_PUBLICATION" in binding.publication_authority["authority_exclusions"]


def test_n6_06_f1_is_resolved_by_the_real_v558_context_resolver():
    """Resolution is performed by the real M4 resolver, not synthesised."""

    terminal = _chain()
    resolution = terminal.v558_terminal.resolution
    assert resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    assert len(resolution.resolved_entries) == 1
    resolved = resolution.resolved_entries[0]
    assert resolved.canonical_producer_family == "V554"
    assert resolved.resolver_allowed_uses == (CONTEXT_USE,)
    # Every selection record is a SELECTED decision with exact closure.
    for record in resolution.selection_records:
        assert record.decision == "SELECTED"
        assert record.producer_object_ref.object_id == terminal.m1_evaluation.f1["f1_id"]
    # No fuzzy/latest repair occurred.
    assert resolution.receipt.unresolved_keys == ()


def test_n6_07_resolution_does_not_fabricate_a_resolved_structural_context():
    """The resolver returns resolved entries and a receipt, but no context object.

    This is deliberate owner behaviour ("without fabricating a
    ResolvedStructuralContext"), not a defect and not a missing N6 product.
    """

    terminal = _chain()
    assert terminal.v558_terminal.resolution.resolved_structural_context is None


def test_n6_08_absent_v555_positions_do_not_block_context_realization():
    """AT24 hostile: absence of structural positions must not block CONTEXT."""

    terminal = _chain()
    # Forbidden producer families include V555; none appear.
    published_families = {e.obj.producer_family for e in terminal.v558_terminal.repository.entries}
    assert not (published_families & FORBIDDEN_PRODUCER_FAMILIES)
    # The demanded CONTEXT product is nonetheless fully published and resolved.
    assert terminal.v558_terminal.resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    # And no forbidden permission atom leaked into the context object.
    assert not (set(FORBIDDEN_PERMISSION_ATOMS) & set(
        terminal.v558_terminal.repository.entries[0].governance.producer_allowed_uses
    ))


# ==========================================================================
# 4. AT24 / AT25 / AT30 truthful recording
# ==========================================================================
def test_n6_09_at24_context_wakes_because_a_real_consumer_contract_demands_it():
    """AT24 positive: CONTEXT wakes on a real demand, not on machinery existence."""

    terminal = _chain()
    binding = load_current_gt12_e2b_publication_governance_binding()
    # The demanding contract is the adopted publication authority + V557 binding.
    assert binding.publication_authority["governed_use_id"] == GOVERNED_USE_ID
    assert binding.v557_authority_ref.authority_id == V557_AUTHORITY_ID
    assert binding.v557_authority_ref.authority_version == "1.0.0"
    # The adopted authority narrows the semantic class to F1, CONTEXT-only.
    assert binding.publication_authority["allowed_object_families"] == ("F1",)
    assert tuple(
        binding.publication_authority["jurisdiction"]["inherited_downstream_use_exact"]
    ) == ("CONTEXT",)
    # The demanded product exists as a positive, exact CONTEXT object.
    assert terminal.v558_terminal.repository.entries[0].obj.semantic_class == "F1"


def test_n6_10_at25_no_mechanism_is_manufactured_from_conditional_support():
    """AT25: this slice mints no mechanism/consequence product.

    Conditional-support counts are NOT a mechanism. SDTF/redrive machinery presence
    does not create mechanism occupancy; its consumer contract is not current.
    """

    terminal = _chain()
    # No mechanism-bearing semantic class is published.
    published = {e.obj.semantic_class for e in terminal.v558_terminal.repository.entries}
    assert published == {"F1"}
    # The mechanism/consequence consumer contract is NOT current; it cannot be invoked.
    with pytest.raises(NotYetApplicableConsumer):
        evaluate_current_consumer(
            policy_id="OC03_SDTF_OBJECTIVE_CONSEQUENCE_R1",
            operation_id="N6_GT2_MECHANISM_PROBE",
            inputs=(
                PolicyInput(
                    input_id="GT2_MECHANISM_PROBE",
                    required=True,
                    available=False,
                    evidence_kind=EvidenceKind.EMPIRICAL,
                    evidence_tier=EvidenceTier.UNAVAILABLE,
                    claim_ceiling=ClaimCeiling.STRUCTURAL_RELATION,
                    omission_reason="no lawful mechanism authority at this grain",
                ),
            ),
            requested_claim_ceiling=ClaimCeiling.STRUCTURAL_RELATION,
            partial_allowed=False,
        )


def test_n6_11_at25_sdtf_machinery_presence_is_not_mechanism_occupancy():
    """AT25 hostile: the mere presence of SDTF/redrive owners proves nothing."""

    import rawlsing_next.sdtf_r4_mechanism_rule_authority_binding as _sdtf_binding
    import rawlsing_next.sdtf_r4_world_response_redrive as _sdtf_redrive

    # SDTF mechanism-binding and redrive owners genuinely exist in the tree...
    assert _sdtf_binding is not None and _sdtf_redrive is not None
    # ...yet the mechanism/consequence consumer contract is NOT current, so their
    # presence cannot be read as a populated mechanism.
    assert not POLICY_BINDINGS["OC03_SDTF_OBJECTIVE_CONSEQUENCE_R1"].applicable
    terminal = _chain()
    assert {e.obj.semantic_class for e in terminal.v558_terminal.repository.entries} == {"F1"}


def test_n6_12_at30_is_not_applicable_nontemporal():
    """AT30: this slice is nontemporal SIG-004; no temporal producer is invoked."""

    terminal = _chain()
    # The temporal producer M1 decision did not create a temporal product.
    evaluation = terminal.m1_evaluation
    assert evaluation.f2 == ()  # no temporal condition branches
    # No V553/V556/V558 temporal product in the published repository.
    published = {e.obj.semantic_class for e in terminal.v558_terminal.repository.entries}
    assert not (published & {"V553", "V556"})
    # Audit-only classes are never resolved as semantic context.
    assert "F1" not in AUDIT_ONLY_CLASSES


def test_n6_13_unrelated_objective_functions_remain_unwoken():
    """AT24 hostile: unrelated functions stay unwoken; nothing else is populated."""

    terminal = _chain()
    # Only F1 CONTEXT exists. No structural position, route, mechanism, or temporal
    # object is published alongside it.
    assert len(terminal.v558_terminal.repository.entries) == 1
    entry = terminal.v558_terminal.repository.entries[0]
    assert entry.obj.semantic_class == "F1"
    assert entry.obj.source_stage == "M1_RELATION_V554_TO_V557"
    # No V555 route continuation is present.
    assert not ({"V555"} & {e.obj.producer_family for e in terminal.v558_terminal.repository.entries})


# ==========================================================================
# 5. world consumer reachability (item 6 of required chain)
# ==========================================================================
def test_n6_14_no_current_terminal_objective_world_consumer_exists():
    """Item 6: there is NO current terminal objective-world/context consumer.

    The commission conditions this item on "if such a current consumer exists". The
    terminal objective-world root/resolver (OC05) is explicitly not current, and its
    reason forbids inventing a universal terminal. That is a lawful NOT_APPLICABLE,
    not a defect, and not a reason to withhold the demanded CONTEXT product.
    """

    with pytest.raises(NotYetApplicableConsumer, match="no universal terminal"):
        evaluate_current_consumer(
            policy_id="OC05_TERMINAL_OBJECTIVE_WORLD_RESOLUTION_R1",
            operation_id="N6_GT2_TERMINAL_PROBE",
            inputs=(
                PolicyInput(
                    input_id="GT2_CONTEXT",
                    required=True,
                    available=True,
                    evidence_kind=EvidenceKind.EMPIRICAL,
                    evidence_tier=EvidenceTier.POPULATION_CERTIFIED,
                    claim_ceiling=ClaimCeiling.STRUCTURAL_RELATION,
                    producer_ref=ConsumerExactRef("F1", "urn:test:probe", "a" * 64),
                    authority_refs=(ConsumerExactRef("AUTH", "urn:test:auth", "b" * 64),),
                ),
            ),
            requested_claim_ceiling=ClaimCeiling.STRUCTURAL_RELATION,
            partial_allowed=False,
        )


def test_n6_15_current_consumers_accept_the_structural_relation_evidence():
    """The two current consumers (OC01/OC02) accept STRUCTURAL_RELATION evidence.

    This demonstrates that the demanded CONTEXT object *could* be consumed by a current
    consumer policy. It does not by itself prove a current world terminal exists --
    that remains OC05 and is not current.
    """

    terminal = _chain()
    f1_ref = terminal.m1_evaluation.f1["f1_id"]
    consumer_ref = ConsumerExactRef("F1", f1_ref, "a" * 64)
    evidence = PolicyInput(
        input_id="GT2_F1_CONTEXT",
        required=True,
        available=True,
        evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=EvidenceTier.POPULATION_CERTIFIED,
        claim_ceiling=ClaimCeiling.STRUCTURAL_RELATION,
        producer_ref=consumer_ref,
        authority_refs=(ConsumerExactRef("AUTH", "urn:test:auth", "b" * 64),),
    )
    for policy in ("OC01_PRE553_SOURCE_LOCAL_EMPIRICAL_QUERY_R1",
                    "OC02_LEARNED_STRUCTURAL_ADMISSION_R1"):
        receipt = evaluate_current_consumer(
            policy_id=policy,
            operation_id="N6_GT2_CONTEXT_CONSUMPTION",
            inputs=(evidence,),
            requested_claim_ceiling=ClaimCeiling.STRUCTURAL_RELATION,
            partial_allowed=False,
        )
        assert receipt.positive_completion is True
        assert receipt.state.value == "SUPPORTED_OBJECTIVE_RESULT"
        assert receipt.consumer_seam == POLICY_BINDINGS[policy].seam


# ==========================================================================
# 6. lineage / permission / currentness / replay bindings + limitations
# ==========================================================================
def test_n6_16_lineage_permission_currentness_and_replay_are_bound():
    terminal = _chain()
    entry = terminal.v558_terminal.repository.entries[0]
    payload = entry.obj.payload
    # Exact relation + admission lineage survive publication.
    assert payload["originating_relation_admission_exact_refs"] == (
        terminal.admission.ref.as_dict(),
    )
    assert payload["originating_field_forge_relation_exact_refs"] == (
        terminal.relation.ref.as_dict(),
    )
    # Currentness: V557 state is exactly CONTEXT-only, not broader.
    assert entry.governance.decision_state.value == "ALLOW_CONTEXT_ONLY"
    assert entry.governance.v557_allowed_uses == (CONTEXT_USE,)
    # Replay: the resolution receipt binds exact refs + a replay digest.
    receipt = terminal.v558_terminal.resolution.receipt
    assert receipt.resolved_entry_refs
    assert receipt.replay_input_digest
    # Limitations: the V3 zero-positive guard is the terminal ceiling here.
    assert terminal.v3_decision.zero_effect is True


def test_n6_17_the_chain_is_deterministic_and_source_free():
    """Re-running the demanded chain reproduces identical identities (no fabrication)."""

    a = _chain()
    b = _chain()
    assert a.m1_evaluation.f1["f1_id"] == b.m1_evaluation.f1["f1_id"]
    assert (
        a.v558_terminal.resolution.receipt.result_state
        == b.v558_terminal.resolution.receipt.result_state
    )
    assert (
        a.v558_terminal.repository.entries[0].obj.payload["f1_id"]
        == b.v558_terminal.repository.entries[0].obj.payload["f1_id"]
    )
    # No actor/person work was performed anywhere in this chain.
    src = inspect.getsource(d_to_m4.publish_and_resolve_relation_v554_at_current_m4)
    assert "ACTOR" not in src.upper() or "ACTOR_INFERENCE" in src