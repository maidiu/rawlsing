"""C5/N5 courts for the retained current GT2 structural-context service.

AT22 (exact retained input/support/topology/provenance and repeatable identity),
AT23 (exact structural authority/admission and its hostiles), AT24 (actual
objective consumption).

The service under test is a composition of already-retained owners. These courts
assert that it composes them faithfully, never recomputes their semantics, never
translates them, and never widens the adopted authority ceiling.
"""
from __future__ import annotations

import inspect

import pytest

from rawlsing_next import current_gt2_structural_context as c5
from rawlsing_next.current_gt2_structural_context import (
    CurrentGT2StructuralContextError,
    evaluate_current_gt2_structural_context,
)


@pytest.fixture(scope="module")
def served():
    """One authoritative service evaluation shared by the read-only courts."""
    return evaluate_current_gt2_structural_context()


# ===========================================================================
# AT22 - exact retained input, support, topology, provenance, repeatable identity
# ===========================================================================


def test_at22_service_takes_no_caller_arguments():
    """AT22: the public entry is zero-argument and therefore not caller-shaped."""
    signature = inspect.signature(evaluate_current_gt2_structural_context)
    assert list(signature.parameters) == [], (
        "the service must accept no caller arguments"
    )


def test_at22_retained_input_floor_is_exact(served):
    """AT22: exact retained query/fact/replay/risk identity and support."""
    assert served.query.ref.content_hash == c5.RETAINED_QUERY_HASH
    assert served.fact.ref.content_hash == c5.RETAINED_FACT_HASH
    assert served.fact_state == c5.RETAINED_FACT_STATE
    assert served.raw_denominator_support == c5.RETAINED_DENOMINATOR
    assert served.replay_ref["content_hash"] == c5.RETAINED_REPLAY_HASH
    assert served.risk_set_ref["content_hash"] == c5.RETAINED_RISK_SET_HASH


def test_at22_conditioner_target_direction_is_q86b_to_q86a(served):
    """AT22: frozen source-native conditioner -> target role and order."""
    from rawlsing_next.field_forge_conditional_support import (
        CONDITIONER_SOURCE_NATIVE_VARIABLE,
        TARGET_SOURCE_NATIVE_VARIABLE,
    )

    assert CONDITIONER_SOURCE_NATIVE_VARIABLE == c5.RETAINED_CONDITIONER_VARIABLE
    assert TARGET_SOURCE_NATIVE_VARIABLE == c5.RETAINED_TARGET_VARIABLE
    # The producer query carries exactly [conditioner, target] in that order.
    assert tuple(served.query.target_refs) == (
        served.query.target_refs[0],
        served.query.target_refs[1],
    )
    topology = served.query.target_arity_and_topology
    assert topology["arity"] == 2
    assert topology["joint_order_semantics"] == "SEMANTIC_ORDERED"
    assert [
        component["topology"] for component in topology["components"]
    ] == ["SCALAR_SINGULAR", "SCALAR_SINGULAR"]


def test_at22_relation_and_admission_identities_are_the_frozen_ones(served):
    """AT22: exact retained relation identity and admission identity."""
    assert served.relation_ref["content_hash"] == c5.RETAINED_RELATION_IDENTITY
    assert served.admission_ref["content_hash"] == c5.RETAINED_ADMISSION_IDENTITY


def test_at22_relation_identity_is_repeatable(served):
    """AT22: repeatable relation identity across independent service calls."""
    again = evaluate_current_gt2_structural_context()
    assert again.relation_ref == served.relation_ref
    assert again.admission_ref == served.admission_ref
    assert again.query_ref == served.query_ref
    assert again.fact_ref == served.fact_ref
    assert again.publication_hash == served.publication_hash
    assert again.resolution_key == served.resolution_key
    assert again.selection_record_id == served.selection_record_id


def test_at22_service_returns_owner_objects_without_recomputation(served):
    """AT22: the service relays owner objects, it does not rebuild them."""
    import rawlsing_next.field_forge_conditional_support as ff
    import rawlsing_next.gt12_d_to_m4_typed_bridge as d2m
    import rawlsing_next.wave1_ff_prev3_relation_admission as adm

    assert isinstance(served.relation, ff.ExactConditionalSupportProfile)
    assert isinstance(served.admission, adm.Prev3FieldForgeRelationAdmission)
    assert isinstance(served.terminal, d2m.RelationV558Terminal)

    # The relayed relation is byte-identical to the owner's own production.
    owner_relation = ff.produce_exact_conditional_support_profile(
        joint_fact=served.fact,
        joint_query=served.query,
        conditioner_ref=served.query.target_refs[0],
        target_ref=served.query.target_refs[1],
        producer_permission_ceiling=(c5.TARGET_USE,),
    )
    assert owner_relation.ref == served.relation.ref
    assert owner_relation.as_dict() == served.relation.as_dict()


def test_at22_no_handwritten_relation_geometry_in_service(served):
    """AT22: no relation geometry/profile is authored inside the service."""
    import inspect as _inspect

    source = _inspect.getsource(c5)
    # The service must not construct cell/profile/geometry material itself.
    for forbidden in (
        "complete_cell_semantic_projection",
        "raw_probability",
        "exact_fraction",
        "conditional_support_profile=",
    ):
        assert forbidden not in source, f"service appears to author {forbidden!r}"
    # Every count/geometry value it reports comes from the owner objects.
    assert tuple(served.relation.conditional_count_profile)


def test_at22_provenance_is_carried_from_the_retained_fact(served):
    """AT22: exact provenance and replay closure come from the producer fact."""
    assert tuple(served.fact.source_empirical_provenance_refs)
    assert dict(served.fact.replay_ref)["content_hash"] == c5.RETAINED_REPLAY_HASH
    # The relation carries the producer replay binding through the admission.
    assert served.admission.producer_replay_locator_or_reference_root is not None
    assert tuple(served.admission.dependency_refs)


# ===========================================================================
# AT23 - exact structural authority and admission
# ===========================================================================


def test_at23_admission_is_exactly_positive_admitted(served):
    """AT23: exact positive ADMITTED for STRUCTURAL_MEDIATION_INPUT only."""
    assert served.admission.is_positive is True
    assert str(served.admission.decision).endswith("ADMITTED")
    assert tuple(served.admission.relation_permission_ceiling) == (c5.TARGET_USE,)
    assert c5.TARGET_USE == "STRUCTURAL_MEDIATION_INPUT"
    assert served.admission.reason_code == (
        "EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT"
    )


def test_at23_admission_authority_is_the_frozen_current_authority(served):
    """AT23: exact current admission authority id/version/scope."""
    authority = served.admission.admission_authority_ref
    assert authority.authority_id == c5.RETAINED_ADMISSION_AUTHORITY_ID
    assert authority.authority_version == c5.RETAINED_ADMISSION_AUTHORITY_VERSION
    assert c5.RETAINED_ADMISSION_SCOPE == "CURRENT_FOR_FROZEN_GT2_CANARY_ONLY"


def test_at23_no_applicable_negative_or_denial_refs(served):
    """AT23: no applicable negative/denial/noncomparability refs are present."""
    assert tuple(served.admission.applicable_negative_denial_noncomparability_refs) == ()


def test_at23_relation_owner_and_family_are_owner_native(served):
    """AT23: relation family/owner are FIELD FORGE's, not the service's."""
    from rawlsing_next.gt12_c_to_d_relation_bridge import (
        EXPECTED_RELATION_FAMILY,
        EXPECTED_RELATION_OWNER,
    )

    assert served.admission.relation_owner == EXPECTED_RELATION_OWNER
    assert EXPECTED_RELATION_OWNER == "FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER"
    assert EXPECTED_RELATION_FAMILY == "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0"
    # The relation itself is the owner's own object, not a service-authored one.
    assert type(served.relation).__module__ == "rawlsing_next.field_forge_conditional_support"


def test_at23_hostile_wrong_source_identity_is_rejected():
    """AT23 hostile: a drifted current source identity fails closed."""
    with pytest.raises(CurrentGT2StructuralContextError):
        c5._verify_retained_floor(
            type("Q", (), {"ref": type("R", (), {"content_hash": "0" * 64})()})(),
            _loaded_fact(),
        )


def test_at23_hostile_wrong_risk_set_is_rejected():
    """AT23 hostile: a drifted risk-set identity fails closed."""
    with pytest.raises(CurrentGT2StructuralContextError, match="risk-set"):
        c5._verify_retained_floor(_loaded_query(), _tampered_fact(risk="1" * 64))


def test_at23_hostile_non_supported_fact_state_is_rejected():
    """AT23 hostile: a non-SUPPORTED relation state fails closed."""
    with pytest.raises(CurrentGT2StructuralContextError, match="fact state"):
        c5._verify_retained_floor(_loaded_query(), _tampered_fact(state="UNRESOLVED"))


def test_at23_hostile_wrong_denominator_is_rejected():
    """AT23 hostile: a drifted denominator fails closed."""
    with pytest.raises(CurrentGT2StructuralContextError, match="denominator"):
        c5._verify_retained_floor(_loaded_query(), _tampered_fact(denominator=99))


def test_at23_hostile_reversed_conditioner_target_role_is_rejected():
    """AT23 hostile: reversed/mutated conditioner-target role or order fails closed."""
    import rawlsing_next.field_forge_conditional_support as ff

    query, fact = _loaded_query(), _loaded_fact()
    # Reversing the conditioner/target arguments is owner-rejected.
    with pytest.raises(ff.FieldForgeConditionalSupportError):
        ff.produce_exact_conditional_support_profile(
            joint_fact=fact,
            joint_query=query,
            conditioner_ref=query.target_refs[1],
            target_ref=query.target_refs[0],
            producer_permission_ceiling=(c5.TARGET_USE,),
        )


def test_at23_hostile_target_use_permission_widening_is_rejected():
    """AT23 hostile: permission widening is rejected by the producer owner."""
    import rawlsing_next.field_forge_conditional_support as ff

    query, fact = _loaded_query(), _loaded_fact()
    with pytest.raises(ff.FieldForgePermissionWideningError):
        ff.produce_exact_conditional_support_profile(
            joint_fact=fact,
            joint_query=query,
            conditioner_ref=query.target_refs[0],
            target_ref=query.target_refs[1],
            producer_permission_ceiling=(c5.TARGET_USE,),
            relation_permission_ceiling=("CONTEXT", "ACTIVE_CAUSAL", "REVIEW"),
        )


def test_at23_hostile_missing_target_use_permission_is_rejected():
    """AT23 hostile: an empty target-use ceiling is refused by the producer owner."""
    import rawlsing_next.field_forge_conditional_support as ff

    query, fact = _loaded_query(), _loaded_fact()
    with pytest.raises(ff.FieldForgeConditionalSupportError, match="may not be empty"):
        ff.produce_exact_conditional_support_profile(
            joint_fact=fact,
            joint_query=query,
            conditioner_ref=query.target_refs[0],
            target_ref=query.target_refs[1],
            producer_permission_ceiling=(),
        )


def test_at23_hostile_wrong_target_use_is_rejected():
    """AT23 hostile: an admission whose ceiling is not exactly the target use fails."""
    import rawlsing_next.field_forge_conditional_support as ff

    query, fact = _loaded_query(), _loaded_fact()
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=query.target_refs[0],
        target_ref=query.target_refs[1],
        producer_permission_ceiling=("CONTEXT",),
    )
    with pytest.raises(CurrentGT2StructuralContextError, match="permission ceiling"):
        c5._require_positive_admission(_admission_shell(relation))


def test_at23_hostile_nonpositive_admission_is_rejected():
    """AT23 hostile: a nonpositive admission decision fails closed."""
    import rawlsing_next.field_forge_conditional_support as ff

    query, fact = _loaded_query(), _loaded_fact()
    relation = ff.produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=query.target_refs[0],
        target_ref=query.target_refs[1],
        producer_permission_ceiling=(c5.TARGET_USE,),
    )
    shell = _admission_shell(relation)
    object.__setattr__(shell, "is_positive", False)
    with pytest.raises(CurrentGT2StructuralContextError, match="not positive"):
        c5._require_positive_admission(shell)


def test_at23_no_causal_or_mechanism_or_actor_semantics_are_claimed():
    """AT23: the service claims no causal/mechanism/actor semantics."""
    import inspect as _inspect

    source = _inspect.getsource(c5)
    for forbidden in ("ACTIVE_CAUSAL", "REVIEW"):
        # These appear only as explicit prohibitions, never as a requested use.
        assert f'"{forbidden}"' not in source or "FORBIDDEN_USE_CLASSES" in source
    record = evaluate_current_gt2_structural_context().audit_record()
    assert tuple(record["v557_allowed_uses"]) == ("CONTEXT",)
    assert tuple(record["resolved_uses"]) == ("CONTEXT",)
    assert c5.CEILING_NO_CAUSAL_ROLE_IDENTITY is True
    assert c5.CEILING_NO_MECHANISM_IDENTITY is True
    assert c5.CEILING_NO_ACTOR_STATE is True
    assert c5.CEILING_NO_POSITIVE_V3_AUTHORITY is True


# ===========================================================================
# AT24 - actual objective consumption
# ===========================================================================


def test_at24_m1_is_eligible_over_the_admitted_relation_basis(served):
    """AT24: M1 ELIGIBLE over the admitted FIELD FORGE relation basis."""
    assert served.m1_decision_state == "ELIGIBLE"
    assert served.m1_required_basis_kind == "ADMITTED_FIELD_FORGE_RELATION"
    assert served.m1_evaluation.contract_id == c5.M1_CONTRACT_ID
    assert c5.M1_CONTRACT_ID == "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0"


def test_at24_route_is_the_direct_v554_to_v557_descent(served):
    """AT24: the only admissible descent is V554 -> V557 direct."""
    # The typed bridge names the exact basis kind and no substitute is possible.
    assert served.bridge.preparation.state.name == "RELATION_BASIS_READY"
    assert c5.M1_ROUTE == "V554_TO_V557_DIRECT"
    from rawlsing_next.gt12_d_to_m4_typed_bridge import RELATION_BASIS_KIND

    assert served.m1_evaluation.required_basis_kind == RELATION_BASIS_KIND


def test_at24_publication_family_is_f1_only(served):
    """AT24: publication family F1 only."""
    assert served.publication_family == "F1"
    assert c5.PUBLICATION_FAMILY == "F1"
    assert tuple(served.terminal.publication.entries)[0].obj.semantic_class == "F1"


def test_at24_v557_is_allow_context_only(served):
    """AT24: V557 ALLOW_CONTEXT_ONLY with CONTEXT uses only."""
    assert served.v557_state == "ALLOW_CONTEXT_ONLY"
    assert tuple(served.v557_allowed_uses) == ("CONTEXT",)


def test_at24_v558_resolution_is_complete_over_v554(served):
    """AT24: V558 RESOLUTION_COMPLETE with a resolved V554 producer."""
    selection = served.terminal.resolution.selection_records[0]
    assert selection.decision == "SELECTED"
    assert selection.typed_state == "ELIGIBLE"
    assert served.producer_family == "V554"
    assert served.resolution_key == str(selection.resolution_key)


def test_at24_no_v553_v555_v556_substitute_basis(served):
    """AT24: no V553/V555/V556 substitute basis may be resolved."""
    for forbidden in ("V553", "V555", "V556"):
        assert served.producer_family != forbidden
        assert forbidden not in str(dict(served.audit_record()))
    assert c5.FORBIDDEN_SUBSTITUTE_BASES == ("V553", "V555", "V556")


def test_at24_review_and_active_causal_are_absent(served):
    """AT24: REVIEW and ACTIVE_CAUSAL are absent from the resolved context."""
    for forbidden in ("REVIEW", "ACTIVE_CAUSAL"):
        assert forbidden not in served.v557_allowed_uses
        assert forbidden not in served.resolved_uses
    assert served.terminal.resolution.resolved_structural_context is None


def test_at24_existing_v3_zero_effect_behavior_is_unchanged():
    """AT24: the service creates no actor state and no V3 effect."""
    served = evaluate_current_gt2_structural_context()
    # Nothing actor-shaped is reachable from the resolved context.
    assert served.terminal.resolution.resolved_structural_context is None
    audit = dict(served.audit_record())
    assert not any("actor" in key.lower() for key in audit)
    # The publication entry is an F1 structural context object produced by V554,
    # not an actor/person object and not a V3 effect.
    entry = served.terminal.publication.entries[0].obj
    assert entry.producer_family == "V554"
    assert entry.semantic_class == "F1"
    assert tuple(entry.producer_allowed_uses) == ("CONTEXT",)
    assert entry.source_stage == "M1_RELATION_V554_TO_V557"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _loaded_query():
    from rawlsing_next.pre553_repo_native_seal import load_current_gt2_query_fact

    return load_current_gt2_query_fact()[0]


def _loaded_fact():
    from rawlsing_next.pre553_repo_native_seal import load_current_gt2_query_fact

    return load_current_gt2_query_fact()[1]


def _tampered_fact(*, risk=None, state=None, denominator=None):
    """Return the loaded fact with one identity field swapped, via a shell object."""
    fact = _loaded_fact()

    class _Shell:
        def __init__(self, **overrides):
            self.ref = fact.ref
            self.typed_state = overrides.get("state") or fact.typed_state
            self.raw_denominator_support = (
                overrides.get("denominator")
                if overrides.get("denominator") is not None
                else fact.raw_denominator_support
            )
            self.replay_ref = fact.replay_ref
            self.risk_set_ref = (
                dict(fact.risk_set_ref) | {"content_hash": risk}
                if risk else fact.risk_set_ref
            )

    return _Shell(state=state, denominator=denominator)


def _admission_shell(relation):
    """A minimal admission-shaped object for the positive-guard hostile."""
    class _Ref:
        content_hash = c5.RETAINED_ADMISSION_IDENTITY

    class _Shell:
        is_positive = True
        decision = "ADMITTED"
        reason_code = "EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT"
        ref = _Ref()
        relation_ref = relation.ref
        relation_permission_ceiling = relation.relation_permission_ceiling
        applicable_negative_denial_noncomparability_refs = ()

    return _Shell()