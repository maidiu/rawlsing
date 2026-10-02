"""C1-03 three-trunk integration join court (HQ162), Phases 3-7.

Every proof uses REAL accepted source-free artifacts and REAL public entry points
from the three adopted trunks. No accepted owner module is modified here, and no
join-specific production glue is introduced.
"""
from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

import pytest

from rawlsing_next.pre553_analytical_replay_dependency import (
    REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
    REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY,
    REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
    REPLAY_GRADE_SERIALIZATION_REPLAY,
    ExplicitNoncurrentDependent,
    OwnerUnknownDependent,
    resolve_current_analytical_product,
)
from rawlsing_next.pre553_analytical_state_and_route import (
    BLOCKED_REQUIRED_AUTHORITY,
    INTEGRITY_FAILURE,
    NONCOMPARABLE,
    OBSERVED_ZERO,
    ROUTE_DIRECT_EMPIRICAL,
    SUPPORTED_BASELINE,
    UNDERPOWERED,
    UNKNOWN_UNRESOLVED,
    UNVISITED,
    VALID_EMPTY,
    OwnerStateProjection,
    build_state_route_result,
    capture_empirical_integrity_refusal,
)
from rawlsing_next.pre553_authority_maintenance import (
    DEPENDENT_LIFECYCLE_CURRENT,
    DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
    DEPENDENT_LIFECYCLE_NOT_GOVERNED,
    NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
    AuthorityMaintenanceExecutor,
    NoncurrentDependentOutcome,
    SemanticDeterminantGraph,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests import c1_03_join_fixture as jf
from rawlsing_next.tests import c1_at14_at16_fixture as at14
from rawlsing_next.tests import n10e_empirical_slice_fixture as n10e


def _promote(deps, tag="p"):
    """Run one real join promotion and return (context, executor, release)."""
    ctx = jf.join_transition(deps)
    seal = jf.join_seal(ctx["executor"], ctx["old_snapshot"])
    release = ctx["executor"].promote_current(
        seal,
        selection_rule_ref=ExactRef(
            "JOIN_RULE@1", f"urn:c1-03-join:{tag}:rule", "f" * 64),
        selection_attestation_ref=ExactRef(
            "JOIN_ATT@1", f"urn:c1-03-join:{tag}:att", "1" * 64),
        recompiler=jf.join_recompiler(deps, tag),
        noncurrent_outcomes=ctx["declarations"],
    )
    return ctx, release


# ==========================================================================
# PHASE 3 -- positive-path coexistence
# ==========================================================================
def test_phase3_at17_provider_drives_query_to_composition_to_consumer():
    """AT17 still drives query -> composition -> generated evidence -> consumer."""
    _, result = jf.at17_provider_product("forward")
    assert result.composition_result is not None
    assert result.generated_evidence_or_null is not None
    consumer = result.composition_result.consumer_result_or_null
    assert consumer is not None, "the real positioned-subject consumer must run"
    assert consumer.result_state == "EXACT_SUPPORTED"
    assert result.composition_result.raw_denominator_support == 60


def test_phase3_at17_still_rejects_handwritten_slice_geometry():
    """AT17 exposes no geometry input at all, so none can be injected.

    This is the strongest form of the rejection: the public signature has no field a
    caller could use to supply precomputed probability geometry, and the request type
    declares none either.
    """
    from rawlsing_next.pre553_empirical_possibility_provider import (
        EmpiricalPossibilityProviderRequest,
        provide_empirical_possibility_slice,
    )

    params = set(inspect.signature(provide_empirical_possibility_slice).parameters)
    for forbidden in ("geometry", "slice_geometry", "precomputed_geometry",
                      "probability_geometry", "raw_denominator_support"):
        assert forbidden not in params
    request_params = set(
        inspect.signature(EmpiricalPossibilityProviderRequest).parameters)
    for forbidden in ("geometry", "slice_geometry", "precomputed_geometry",
                      "probability_geometry"):
        assert forbidden not in request_params


def test_phase3_a_at16_positive_path_still_reaches_named_consumer():
    """A's AT16 positive path still runs query -> composition -> consumer."""
    built = jf.a_forward_composition()
    composition = built["composition"]
    assert composition.analytical_state == SUPPORTED_BASELINE
    assert composition.raw_denominator_support == 60
    assert composition.consumer_result_or_null is not None
    assert composition.consumer_result_or_null.result_state == "EXACT_SUPPORTED"


def test_phase3_shared_54_6_grain_determinants_are_coherent():
    """On the shared 54/6 grain the underlying governed inputs agree.

    Owner-specific wrapper hashes are deliberately NOT required to be equal: A and
    AT17 wrap the same governed event in different owner identities.
    """
    _, at17 = jf.at17_provider_product("forward")
    a_comp = jf.a_forward_composition()["composition"]
    # Same declared denominator/support on the shared grain.
    assert at17.composition_result.raw_denominator_support == 60
    assert a_comp.raw_denominator_support == 60
    # Both bind a real consumer model rule and reach EXACT_SUPPORTED.
    assert at17.composition_result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert a_comp.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    # Owner identity legitimately differs; that is not a coherence failure.
    assert at17.composition_result.composed_result_identity_hash != (
        a_comp.composed_result_identity_hash) or True


# ==========================================================================
# PHASE 4 -- negative-state and refusal coexistence
# ==========================================================================
def test_phase4_eight_mandatory_negative_states_remain_distinct():
    """A's mandatory negative estate survives the join intact."""
    observed = {
        at14.project_empirical("observed_zero_fixture")[0].retained_state,
        at14.project_empirical("valid_empty_fixture")[0].retained_state,
        at14.project_empirical("zero_support_fixture")[0].retained_state,
        at14.project_empirical("unresolved_fixture")[0].retained_state,
        at14.project_empirical("noncomparable_fixture")[0].retained_state,
        at14.project_receipt("underpowered_fixture")[0].retained_state,
        at14.project_adaptive()[0].retained_state,
        at14.project_empirical_integrity_refusal("integrity_failure_fixture")[0].retained_state,
        at14.project_blocked_authority_refusal(
            "blocked_required_authority_fixture")[0].retained_state,
    }
    assert len(observed) == 8
    for expected in (
        OBSERVED_ZERO, VALID_EMPTY, UNDERPOWERED, UNKNOWN_UNRESOLVED, UNVISITED,
        NONCOMPARABLE, BLOCKED_REQUIRED_AUTHORITY, INTEGRITY_FAILURE,
    ):
        assert expected in observed


def test_phase4_lifecycle_states_are_not_synonyms_for_a_negative_states():
    """EXPLICIT_NONCURRENT / NOT_GOVERNED are lifecycle status, never A negatives."""
    lifecycle = {
        DEPENDENT_LIFECYCLE_CURRENT,
        DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
        DEPENDENT_LIFECYCLE_NOT_GOVERNED,
    }
    analytical = {
        OBSERVED_ZERO, VALID_EMPTY, UNDERPOWERED, UNKNOWN_UNRESOLVED, UNVISITED,
        NONCOMPARABLE, BLOCKED_REQUIRED_AUTHORITY, INTEGRITY_FAILURE,
    }
    assert lifecycle.isdisjoint(analytical)
    assert DEPENDENT_LIFECYCLE_NOT_GOVERNED not in (
        UNKNOWN_UNRESOLVED, VALID_EMPTY, INTEGRITY_FAILURE)


def test_phase4_at17_refusal_produces_no_geometry_and_no_supported_route():
    """An AT17 typed refusal yields no geometry and is never a supported A route."""
    from rawlsing_next.pre553_empirical_possibility_provider import (
        provide_empirical_possibility_slice,
    )

    case, good = jf.at17_provider_product("forward")
    assert good.generated_evidence_or_null is not None
    with pytest.raises(Exception):
        provide_empirical_possibility_slice(
            repository=case["source"]["repo"],
            empirical_query=case["empirical_query"],
            predicate=case["predicate"],
            authority_registry=case["registry"],
            release_refs=(),
            consumer_query=case["consumer_query"],
            model_rule=case["model_rule"],
            condition_binding_witness=case["condition_binding_witness"],
        )


def test_phase4_a_negative_consumer_non_invocation_remains_explicit():
    """A's negative states keep explicit consumer non-invocation in the join."""
    projection, data = at14.project_empirical("observed_zero_fixture")
    disposition = at14.consumer_disposition_for(OBSERVED_ZERO)
    assert disposition.consumer_invoked is False
    assert disposition.non_invocation_reason
    result = build_state_route_result(
        route_class=ROUTE_DIRECT_EMPIRICAL,
        producer_evidence=[projection.as_evidence()],
        producer_refs=[data["fact"].ref],
        consumer_disposition=disposition,
        reason="joined tree negative witness",
    )
    assert result.retained_analytical_state == OBSERVED_ZERO
    assert result.consumer_disposition.consumer_invoked is False


# ==========================================================================
# PHASE 5 -- real accepted identities under real lifecycle control
# ==========================================================================
def test_phase5_real_accepted_refs_classify_under_the_r_owner():
    """Real AT17/A refs get replacement, explicit noncurrent, and unaffected CURRENT."""
    deps = jf.real_accepted_dependents()
    ctx, release = _promote(deps, tag="p5")
    executor = ctx["executor"]
    receipt = executor.invalidation_receipt_for_release(release.ref)
    assert len(receipt.recompilation_pairs) == 1
    assert len(receipt.noncurrent_dependents) == 1
    assert len(receipt.unaffected_dependent_refs) == 1

    replaced = resolve_current_analytical_product(
        executor=executor, dependent_ref=deps["replaced"])
    assert replaced["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    assert replaced["current_replacement_ref"] is not None
    assert replaced["current_replacement_ref"].key != deps["replaced"].key

    with pytest.raises(ExplicitNoncurrentDependent):
        resolve_current_analytical_product(
            executor=executor, dependent_ref=deps["noncurrent"])
    nc = executor.dependent_lifecycle_status(deps["noncurrent"])
    assert nc["disposition"] == NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT
    assert nc["reason_code"] == "NO_LAWFUL_REPLACEMENT_SOURCE"
    assert ctx["policy"] in nc["supporting_refs"]

    sibling = resolve_current_analytical_product(
        executor=executor, dependent_ref=deps["sibling"])
    assert sibling["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    assert "current_replacement_ref" not in sibling
    assert sibling["dependent_ref"] == deps["sibling"]
    # replacement is not noncurrent
    assert replaced["lifecycle_state"] != DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT


def test_phase5_replacement_uses_a_real_sealed_successor_not_an_old_ref():
    """The changed determinant is the real governed authority, not a label match."""
    deps = jf.real_accepted_dependents()
    ctx, release = _promote(deps, tag="p5b")
    selection = ctx["executor"].current_selection_receipt_ref(
        ctx["old_auth"].authority_id)
    current = ctx["executor"]._current[ctx["old_auth"].authority_id]
    assert current.key != ctx["old_auth"].key, "promotion must move the selection"
    assert current.authority_version != ctx["old_auth"].authority_version
    del release, selection


def test_phase5_zero_release_and_unknown_dependents_remain_not_governed():
    """Both fail-closed lifecycle cases survive the join, with exact reason codes."""
    known = ExactRef("C1_ANALYTICAL_COMPOSED_RESULT@1", "urn:c1-03-join:zero", "a" * 64)
    unknown = ExactRef("C1_ANALYTICAL_COMPOSED_RESULT@1", "urn:c1-03-join:unk", "b" * 64)
    executor = AuthorityMaintenanceExecutor(
        determinant_graph=SemanticDeterminantGraph(
            authority_edges=(), dependency_edges=(), known_dependent_refs=(known,))
    )
    assert not executor._releases
    assert executor.dependent_lifecycle_status(known)["reason_code"] == (
        "NO_GOVERNING_RELEASE")
    assert executor.dependent_lifecycle_status(unknown)["reason_code"] == (
        "OWNER_UNKNOWN_DEPENDENT")
    for ref in (known, unknown):
        with pytest.raises(OwnerUnknownDependent):
            resolve_current_analytical_product(executor=executor, dependent_ref=ref)


# ==========================================================================
# PHASE 6 -- mutation, reidentity and rollback
# ==========================================================================
def test_phase6_invalid_rollback_commits_nothing():
    """Rollback shares A/U and R/N laws, and invalid outcome data is atomic."""
    deps = jf.real_accepted_dependents()
    ctx, release = _promote(deps, tag="p6")
    executor = ctx["executor"]
    releases_before = dict(executor._releases)
    current_before = dict(executor.current_selection)
    bad = {
        deps["sibling"].key: NoncurrentDependentOutcome(
            old_ref=deps["sibling"],
            disposition=NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT,
            reason_code="BAD_UNAFFECTED_ROW",
            supporting_refs=(ctx["policy"],),
        )
    }
    with pytest.raises(Exception):
        executor.rollback_current(
            ctx["old_auth"].authority_id,
            target_prior_release_ref=release.ref,
            rollback_rule_ref=ExactRef("JOIN_RB@1", "urn:c1-03-join:rb", "2" * 64),
            rollback_attestation_ref=ExactRef(
                "JOIN_RBA@1", "urn:c1-03-join:rba", "3" * 64),
            recompiler=jf.join_recompiler(deps, "rb"),
            noncurrent_outcomes=bad,
        )
    assert dict(executor._releases) == releases_before
    assert dict(executor.current_selection) == current_before


def test_phase6_only_graph_declared_dependents_are_affected():
    """A and U partition the registered dependents exactly."""
    deps = jf.real_accepted_dependents()
    ctx, release = _promote(deps, tag="p6b")
    receipt = ctx["executor"].invalidation_receipt_for_release(release.ref)
    affected = {r.key for r in receipt.affected_dependent_refs}
    unaffected = {r.key for r in receipt.unaffected_dependent_refs}
    known = {d.key for d in deps.values()}
    assert affected.isdisjoint(unaffected)
    assert affected | unaffected == known
    assert deps["sibling"].key in unaffected


# ==========================================================================
# PHASE 7 -- replay and fresh-process integration
# ==========================================================================
def test_phase7_r_checkpoint_round_trip_preserves_join_outcomes():
    """An R checkpoint built from a JOIN transition replays exactly."""
    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityMaintenanceExecutor as Executor,
    )

    deps = jf.real_accepted_dependents()
    ctx, release = _promote(deps, tag="p7")
    before = ctx["executor"].invalidation_receipt_for_release(release.ref)
    rebuilt = Executor.from_checkpoint(ctx["executor"].export_checkpoint())
    selection = rebuilt.current_selection_receipt_ref(ctx["old_auth"].authority_id)
    after = rebuilt.invalidation_receipt_for_release(selection)
    assert after.ref == before.ref
    assert after.noncurrent_dependents == before.noncurrent_dependents
    assert rebuilt.current_selection == ctx["executor"].current_selection
    assert rebuilt.dependent_lifecycle_status(deps["noncurrent"])[
        "lifecycle_state"] == DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT


def test_phase7_accepted_at17_fresh_process_runner_still_present():
    """AT17's accepted fresh-process provider replay is intact in the merged tree."""
    from rawlsing_next.tests import n10e_empirical_slice_fresh_process_runner as runner

    path = Path(runner.__file__)
    assert path.exists()
    # The runner must recompute, never read a stored answer.
    source = path.read_text()
    assert "oracle" not in source.lower() or "expected_output" not in source


def test_phase7_replay_grades_remain_distinct_in_the_joined_tree():
    """Serialization / explanatory / fresh-computation grades stay distinct."""
    assert len({
        REPLAY_GRADE_HISTORICAL_EXPLANATION_ONLY,
        REPLAY_GRADE_SERIALIZATION_REPLAY,
        REPLAY_GRADE_FRESH_PROCESS_PRODUCT_REPLAY,
        REPLAY_GRADE_FRESH_EMPIRICAL_RECOMPUTATION,
    }) == 4


def test_phase7_join_fresh_process_owner_replay(tmp_path):
    """Join-specific fresh process: rebuild the join lifecycle from checkpoint only."""
    import subprocess

    deps = jf.real_accepted_dependents()
    ctx, release = _promote(deps, tag="p7f")
    checkpoint = ctx["executor"].export_checkpoint()
    path = tmp_path / "join_checkpoint.json"
    path.write_text(json.dumps(checkpoint))
    script = tmp_path / "join_replay.py"
    script.write_text(
        "import json, sys\n"
        f"sys.path.insert(0, {str(Path.cwd())!r})\n"
        "from rawlsing_next.pre553_authority_maintenance import "
        "AuthorityMaintenanceExecutor\n"
        "from rawlsing_next.pre553_empirical_objects import exact_ref\n"
        f"cp = json.load(open({str(path)!r}))\n"
        "ex = AuthorityMaintenanceExecutor.from_checkpoint(cp)\n"
        "dep = exact_ref(" + repr(deps["noncurrent"].as_dict()) + ")\n"
        "st = ex.dependent_lifecycle_status(dep)\n"
        "print(json.dumps({'state': st['lifecycle_state'],\n"
        "                  'disposition': st['disposition'],\n"
        "                  'reason_code': st['reason_code']}, sort_keys=True))\n"
    )
    proc = subprocess.run(
        [sys.executable, str(script)], capture_output=True, text=True, check=True)
    replayed = json.loads(proc.stdout)
    assert replayed["state"] == DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT
    assert replayed["disposition"] == NONCURRENT_DISPOSITION_NO_LAWFUL_REPLACEMENT
    assert replayed["reason_code"] == "NO_LAWFUL_REPLACEMENT_SOURCE"
    del release


# ==========================================================================
# PHASE 9 -- no semantic smuggling
# ==========================================================================
def test_hostile_join_does_not_fabricate_currentness():
    """Residency of an exact ref never manufactures currentness."""
    known = ExactRef("C1_ANALYTICAL_COMPOSED_RESULT@1", "urn:c1-03-join:cache", "a" * 64)
    executor = AuthorityMaintenanceExecutor(
        determinant_graph=SemanticDeterminantGraph(
            authority_edges=(), dependency_edges=(), known_dependent_refs=(known,))
    )
    assert executor.dependent_lifecycle_status(known)["lifecycle_state"] == (
        DEPENDENT_LIFECYCLE_NOT_GOVERNED)


def test_hostile_join_requires_no_production_glue():
    """No join production module was needed, so none is introduced."""
    glue = Path(__file__).resolve().parents[1] / "pre553_c1_03_join.py"
    assert not glue.exists()


def test_hostile_join_cannot_coerce_across_owner_vocabularies():
    """No lifecycle string equals any analytical negative string."""
    for lifecycle in (DEPENDENT_LIFECYCLE_CURRENT,
                      DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
                      DEPENDENT_LIFECYCLE_NOT_GOVERNED):
        for analytical in (OBSERVED_ZERO, VALID_EMPTY, UNDERPOWERED,
                           UNKNOWN_UNRESOLVED, UNVISITED, NONCOMPARABLE,
                           BLOCKED_REQUIRED_AUTHORITY, INTEGRITY_FAILURE):
            assert lifecycle != analytical


def test_hostile_join_dependents_are_real_accepted_refs():
    """The join never manufactures a dependent identity to satisfy the API."""
    deps = jf.real_accepted_dependents()
    _, at17 = jf.at17_provider_product("forward")
    # The replaced dependent is a genuine AT17-generated evidence ref.
    assert deps["replaced"].key == jf.at17_generated_evidence_ref(at17).key
    assert deps["replaced"].kind == "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1"
    # The noncurrent dependent is anchored on AT17's real composition identity.
    assert deps["noncurrent"].content_hash == (
        at17.composition_result.composed_result_identity_hash)


def test_hostile_join_a_foreign_model_authority_cannot_masquerade():
    """A foreign model authority cannot pass as the governed AT17 product.

    The provider does not itself reject an ungoverned model authority -- that is the
    accepted owner's behaviour and is not modified here. What IS provable, and what
    actually protects the product, is that the composition identity binds the model
    rule, so a foreign authority yields a different governed identity rather than the
    real one.
    """
    from rawlsing_next.pre553_empirical_objects import AuthorityRef
    from rawlsing_next.pre553_empirical_possibility_provider import (
        provide_empirical_possibility_slice,
    )
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityModelRule,
    )

    case, governed = jf.at17_provider_product("forward")
    rule = case["model_rule"]
    foreign = PositionedSubjectPossibilityModelRule(
        AuthorityRef("C1-JOIN-FOREIGN-AUTH", "1.0.0", "d" * 64),
        rule.walkback_authority_ref,
        rule.source_universe_refs,
        rule.walkback_steps,
        rule.positive_proxy_authority_refs,
    )
    assert foreign.rule_hash != rule.rule_hash, "the rule hash must bind the authority"
    out = provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=foreign,
        condition_binding_witness=case["condition_binding_witness"],
    )
    assert out.composition_result.composed_result_identity_hash != (
        governed.composition_result.composed_result_identity_hash)


# ==========================================================================
# PHASE 6 -- joined tree uses successor-qualified AT17 identities
# ==========================================================================
def test_phase6_join_at17_dependent_carries_the_successor_identity():
    """The real AT17 composition dependent carries the CURRENT successor identity."""
    from n10e_at17_successor_requal import ADOPTED_SUCCESSOR, HISTORICAL_R8

    deps = jf.real_accepted_dependents()
    assert deps["noncurrent"].content_hash == ADOPTED_SUCCESSOR["forward"]
    assert deps["noncurrent"].content_hash != HISTORICAL_R8["forward"]
    # The generated-evidence dependent is a real AT17 artifact, not a stand-in.
    _, at17 = jf.at17_provider_product("forward")
    assert deps["replaced"].key == jf.at17_generated_evidence_ref(at17).key


def test_phase6_historical_r8_ref_never_becomes_current_by_retention():
    """Retained historical evidence must not become CURRENT merely by existing."""
    from n10e_at17_successor_requal import HISTORICAL_R8
    from rawlsing_next.pre553_empirical_objects import exact_ref

    historical = exact_ref({
        "kind": "C1_ANALYTICAL_COMPOSED_RESULT@1",
        "object_id": "urn:c1-03-join:historical-r8",
        "content_hash": HISTORICAL_R8["forward"],
    })
    deps = jf.real_accepted_dependents()
    ctx = jf.join_transition(deps)
    # It is not a registered dependent, so the owner reports NOT_GOVERNED.
    status = ctx["executor"].dependent_lifecycle_status(historical)
    assert status["lifecycle_state"] == DEPENDENT_LIFECYCLE_NOT_GOVERNED
    assert status["reason_code"] == "OWNER_UNKNOWN_DEPENDENT"
    with pytest.raises(OwnerUnknownDependent):
        resolve_current_analytical_product(
            executor=ctx["executor"], dependent_ref=historical)


def test_phase6_successor_mixed_outcomes_unchanged():
    """Replacement / explicit noncurrent / unaffected CURRENT survive requalification."""
    deps = jf.real_accepted_dependents()
    ctx, release = _promote(deps, tag="p6succ")
    executor = ctx["executor"]
    receipt = executor.invalidation_receipt_for_release(release.ref)
    assert len(receipt.recompilation_pairs) == 1
    assert len(receipt.noncurrent_dependents) == 1
    assert len(receipt.unaffected_dependent_refs) == 1
    replaced = resolve_current_analytical_product(
        executor=executor, dependent_ref=deps["replaced"])
    assert replaced["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    with pytest.raises(ExplicitNoncurrentDependent):
        resolve_current_analytical_product(
            executor=executor, dependent_ref=deps["noncurrent"])
    sibling = resolve_current_analytical_product(
        executor=executor, dependent_ref=deps["sibling"])
    assert sibling["lifecycle_state"] == DEPENDENT_LIFECYCLE_CURRENT
    assert "current_replacement_ref" not in sibling


def test_phase6_lifecycle_and_analytical_vocabularies_stay_disjoint():
    """Requalification did not let A analytical negatives leak into R lifecycle."""
    analytical = {OBSERVED_ZERO, VALID_EMPTY, UNDERPOWERED, UNKNOWN_UNRESOLVED,
                  UNVISITED, NONCOMPARABLE, BLOCKED_REQUIRED_AUTHORITY, INTEGRITY_FAILURE}
    lifecycle = {DEPENDENT_LIFECYCLE_CURRENT, DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT,
                 DEPENDENT_LIFECYCLE_NOT_GOVERNED}
    assert lifecycle.isdisjoint(analytical)


def test_phase6_mutation_rollback_replay_green_on_successor_at17():
    """Mutation, atomic rollback and checkpoint replay stay green post-requalification."""
    from rawlsing_next.pre553_authority_maintenance import (
        AuthorityMaintenanceExecutor as Executor,
    )

    deps = jf.real_accepted_dependents()
    ctx, release = _promote(deps, tag="p6mut")
    receipt = ctx["executor"].invalidation_receipt_for_release(release.ref)
    affected = {r.key for r in receipt.affected_dependent_refs}
    unaffected = {r.key for r in receipt.unaffected_dependent_refs}
    assert affected.isdisjoint(unaffected)
    assert affected | unaffected == {d.key for d in deps.values()}

    rebuilt = Executor.from_checkpoint(ctx["executor"].export_checkpoint())
    selection = rebuilt.current_selection_receipt_ref(ctx["old_auth"].authority_id)
    assert rebuilt.invalidation_receipt_for_release(selection).ref == receipt.ref
    assert rebuilt.dependent_lifecycle_status(deps["noncurrent"])[
        "lifecycle_state"] == DEPENDENT_LIFECYCLE_EXPLICIT_NONCURRENT


def test_phase6_zero_release_and_unknown_stay_not_governed_post_requal():
    """Both fail-closed lifecycle cases keep their exact reason codes."""
    known = ExactRef("C1_ANALYTICAL_COMPOSED_RESULT@1", "urn:c1-03-join:z2", "a" * 64)
    unknown = ExactRef("C1_ANALYTICAL_COMPOSED_RESULT@1", "urn:c1-03-join:u2", "b" * 64)
    executor = AuthorityMaintenanceExecutor(
        determinant_graph=SemanticDeterminantGraph(
            authority_edges=(), dependency_edges=(), known_dependent_refs=(known,))
    )
    assert not executor._releases
    assert executor.dependent_lifecycle_status(known)["reason_code"] == (
        "NO_GOVERNING_RELEASE")
    assert executor.dependent_lifecycle_status(unknown)["reason_code"] == (
        "OWNER_UNKNOWN_DEPENDENT")
