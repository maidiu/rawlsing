from __future__ import annotations

import ast
import copy
import inspect
from dataclasses import replace

import pytest

from rawlsing_next import m1_temporal_v554_admission_dedup as m1
from rawlsing_next import m2_v555_atomic_route as m2
from rawlsing_next import m3_v556_higher_order_structural as m3
from rawlsing_next import m4_v557_v558_publication_repository as m4
from rawlsing_next import m5_runtime_rsc_peer_prior as m5
from rawlsing_next import m6_actor_safe_expression as m6
from rawlsing_next import render_bounded_expression as render
from rawlsing_next import v3_psepf_zero_positive_guard as psepf

import rawlsing_next.tests.test_m1_temporal_v554_admission_dedup as t1
import rawlsing_next.tests.test_m2_v555_atomic_route as t2
import rawlsing_next.tests.test_m3_v556_higher_order_structural as t3
import rawlsing_next.tests.test_m4_v557_v558_publication_repository as t4
import rawlsing_next.tests.test_m5_runtime_rsc_peer_prior as t5
import rawlsing_next.tests.test_m6_actor_safe_expression as t6
import rawlsing_next.tests.test_render_bounded_expression as tr
import rawlsing_next.tests.test_psepf_zero_positive_guard as tp


H01 = "REJECT__NON_DOWNGRADABLE_EXACT_USE_NEGATIVE"
H02 = "REJECT__ONE_CANONICAL_SUPPORT_ROUTE_CHAIN"
H03 = "REJECT__PRODUCER_ROUTE_IDENTITY_PRESERVED"
H04 = "INTEGRITY_FAILURE__ROLE_ORDER_CARDINALITY_MULTIPLICITY"
H05 = "NO_WIDENING__RESOLVER_SUBSET_V557_SUBSET_PRODUCER"
H06 = "REJECT__PROVENANCE_ORIGIN_ONLY__COMPOSITION_NONE_BY_DEFAULT"
H07 = "REJECT__PEER_LANES_NONCOLLAPSED"
H08 = "ZERO_UNAUTHORIZED_EFFECT"
H09 = "FAIL_CLOSED_PER_OWNER__CURRENTNESS_INDEPENDENT"
H10 = "REJECT__HISTORICAL_IDENTITY_PRESERVED__REFRESH_PROSPECTIVE"
H11 = "NO_BEHAVIORAL_CHANGE_WITHOUT_CURRENT_ACTOR_SAFE_AUTHORITY"
H12 = "ZERO_POSITIVE_EXPRESSION_SEMANTICS"
H13 = "REJECT__SESSION_NONCAUSAL_NONRESTORATIVE"
H14 = "REJECT__MONOTONE_NO_JOIN"
H15 = "REJECT__SEMANTIC_CEILING_ONLY"
H16 = "ALLOW_LAWFUL_DIVERGENCE_AND_REQUIRE_EXACT_REPLAY"
H17 = "REJECT__TYPED_STATES_DISTINCT"
H18 = "NO_RUNTIME_INSTANCE__EXPLICIT_RESOLUTION_REQUIRED"
H19 = "REJECT__DISPOSITIVE_FINAL_AUTHORITY_CONTROLS"
H20 = "FAIL_CLOSED__NO_HEURISTIC_REPAIR"


def _route_ref(ev: m2.M2Evaluation) -> dict[str, str]:
    return {
        "kind": m2.SEMANTIC_FAMILY,
        "object_id": ev.route["route_id"],
        "content_hash": m2.semantic_hash(ev.route),
    }


def _rawlsing_imports(module) -> set[str]:
    tree = ast.parse(inspect.getsource(module))
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("rawlsing_next."):
            result.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("rawlsing_next."):
                    result.add(alias.name)
    return result


def test_H01_temporal_negative_laundering() -> None:
    payload = t1._invocation(conditions=[t1._condition("K08")])
    payload["scr553_decision_state"] = "V553_NEGATIVE_LIMIT_ONLY"
    payload["temporal_completeness"] = m1.TemporalCompleteness.BLOCKED_BY_APPLICABLE_TEMPORAL_OR_SOURCE_NEGATIVE.value
    blocked = m1.evaluate_m1_temporal_v554_admission_dedup(payload)
    assert blocked.decision_state is m1.M1DecisionState.INELIGIBLE_NEGATIVE_TEMPORAL_AUTHORITY
    assert blocked.f1 is None and blocked.support_count == 0
    downstream = m2.evaluate_m2_v555_atomic_route(blocked, {})
    assert downstream.route is None and downstream.canonical_route_identity is None
    assert H01 == "REJECT__NON_DOWNGRADABLE_EXACT_USE_NEGATIVE"


def test_H02_duplicate_path_multiplication() -> None:
    one = t2._m1(aliases=("direct:a",))
    aliased = t2._m1(aliases=("direct:b", "direct:a"))
    assert one.f1["f1_id"] == aliased.f1["f1_id"]
    route_one = m2.evaluate_m2_v555_atomic_route(one, t2._req(one))
    route_alias = m2.evaluate_m2_v555_atomic_route(aliased, t2._req(aliased))
    assert route_one.canonical_route_identity == route_alias.canonical_route_identity
    rule = t3._rule(reuse="PERMITTED")
    bindings = [
        t3._bind(route_alias, "CAUSE", 1, multiplicity=0),
        t3._bind(route_alias, "EFFECT", 2, multiplicity=1),
    ]
    result = t3._eval([route_alias], t3._request(rule, bindings))
    assert result.decision_state is m3.M3DecisionState.INVALID_PARTICIPANT_SET
    assert result.v556_object is None
    assert H02 == "REJECT__ONE_CANONICAL_SUPPORT_ROUTE_CHAIN"


def test_H03_route_reidentification_through_repository() -> None:
    route = t4._m2_eval("h03")
    structural = m4.structural_object_from_m2(route)
    governance = t4._gov(structural)
    locator_a = t4._loc(structural, governance, "h03-a")
    locator_b = t4._loc(structural, governance, "h03-b")
    assert locator_a != locator_b
    assert structural.object_id == route.route["route_id"]
    assert tuple(structural.payload["canonical_route_identity"]) == route.canonical_route_identity
    assert len(route.canonical_route_identity) == 7
    assert H03 == "REJECT__PRODUCER_ROUTE_IDENTITY_PRESERVED"


def test_H04_nary_structure_corruption_fails_packaging() -> None:
    r1, r2 = t4._m2_eval("h04-a"), t4._m2_eval("h04-b")
    good = t4._m3_eval("h04", (_route_ref(r1), _route_ref(r2)))
    bad_obj = copy.deepcopy(good.v556_object)
    bindings = [dict(item) for item in bad_obj["participant_bindings"]]
    bindings[1]["ordinal_or_null"] = bindings[0]["ordinal_or_null"]
    bad_obj["participant_bindings"] = tuple(bindings)
    bad = replace(good, v556_object=bad_obj)
    with pytest.raises(m4.M4IntegrityError):
        m4.structural_object_from_m3(bad)
    assert H04 == "INTEGRITY_FAILURE__ROLE_ORDER_CARDINALITY_MULTIPLICITY"


def test_H05_permission_by_presence_never_widens() -> None:
    obj = t4._obj("h05", uses=("REVIEW",))
    with pytest.raises(m4.PermissionWideningError):
        t4._gov(obj, uses=("CONTEXT",), state=m4.V557DecisionState.ALLOW_CONTEXT_ONLY)
    repo, locator, query, resolution = t5._runtime_universe(
        "h05-runtime",
        producer_uses=("REVIEW",),
        v557_uses=("REVIEW",),
        requested_uses=("ACTIVE_CAUSAL",),
        provenance="audit://ACTIVE_CAUSAL/PRESENCE/ONLY",
    )
    assert m4.exact_resolution_key(locator) in {record.key for record in repo.index_manifest.records}
    assert resolution.receipt.result_state == "RESOLUTION_DENIED_OR_NOT_APPLICABLE"
    with pytest.raises(m5.M5RuntimeIntegrityError):
        m5.materialize_resolved_structural_context(
            repo, query, resolution, t5._currentness(resolution, "h05-denied")
        )
    assert H05 == "NO_WIDENING__RESOLVER_SUBSET_V557_SUBSET_PRODUCER"


def test_H06_provenance_does_not_create_source_composition() -> None:
    a, b = t3._m2("h06-a"), t3._m2("h06-b")
    rule = t3._rule()
    bindings = [
        t3._bind(a, "CAUSE", 1, source="source:a"),
        t3._bind(b, "EFFECT", 2, source="source:b"),
    ]
    result = t3._eval([a, b], t3._request(rule, bindings))
    assert result.decision_state is m3.M3DecisionState.UNKNOWN_AUTHORITY
    assert result.v556_object is None
    assert H06 == "REJECT__PROVENANCE_ORIGIN_ONLY__COMPOSITION_NONE_BY_DEFAULT"


def test_H07_reverse_lane_ontology_theft_is_blocked() -> None:
    bad = t4._obj("h07", semantic_class="PSEPF")
    with pytest.raises(m4.ReferenceClassError):
        m4.build_v557_publication_bundle((m4.V557PublicationEntry(bad, t4._gov(bad)),))
    decision = psepf.evaluate_psepf_zero_positive_guard(tp._request("ResolvedStructuralContext"))
    tp._assert_zero(decision)
    assert decision.outcome is psepf.GuardOutcome.DENY_ZERO_EFFECT
    assert H07 == "REJECT__PEER_LANES_NONCOLLAPSED"


def test_H08_prior_to_actor_state_shortcut_has_zero_effect() -> None:
    repo, locator, query, resolution, currentness, rsc, validation = t5._materialized("h08")
    actor_state = {"belief": "unchanged", "memory": ("historical",)}
    before = copy.deepcopy(actor_state)
    receipt = m5.bind_structural_peer_use(
        rsc,
        validation,
        t5._peer_requirement("h08"),
        requested_use="ACTIVE_CAUSAL",
        required_resolution_keys=(m4.exact_resolution_key(locator),),
    )
    assert receipt.effect == m5.M5_PEER_EFFECT and receipt.actor_state_effect is False
    assert actor_state == before
    decision = psepf.evaluate_psepf_zero_positive_guard(tp._request("PSEPF"))
    tp._assert_zero(decision)
    assert H08 == "ZERO_UNAUTHORIZED_EFFECT"


def test_H09_cross_peer_staleness_does_not_substitute() -> None:
    repo, _, query, resolution = t5._runtime_universe("h09")
    stale = t5._currentness(resolution, "h09-stale", state=m5.StructuralCurrentnessState.STALE)
    with pytest.raises(m5.M5RuntimeIntegrityError):
        m5.materialize_resolved_structural_context(repo, query, resolution, stale)
    empirical = psepf.evaluate_psepf_zero_positive_guard(tp._request("V3EmpiricalPossibilityInput"))
    tp._assert_zero(empirical)
    assert H09 == "FAIL_CLOSED_PER_OWNER__CURRENTNESS_INDEPENDENT"


def test_H10_refresh_is_prospective_and_history_is_immutable() -> None:
    repo, _, query, resolution = t5._runtime_universe("h10")
    current1 = t5._currentness(resolution, "h10-current-1")
    rsc1 = m5.materialize_resolved_structural_context(repo, query, resolution, current1)
    historical = (current1.receipt_id, current1.receipt_hash, current1.ref)
    current2 = m5.refresh_structural_currentness(
        current1,
        resolution,
        state=m5.StructuralCurrentnessState.CURRENT,
        authority_ref=t5._authority("h10-current-2"),
        structural_currentness_basis_ref=t5._exact_ref("CURRENTNESS_BASIS", "h10-current-2"),
        decision_effective_time_ref=t5._exact_ref("EFFECTIVE_TIME", "h10-current-2"),
        refresh_reason_ref=t5._exact_ref("REFRESH_REASON", "h10-current-2"),
    )
    rsc2 = m5.materialize_resolved_structural_context(repo, query, resolution, current2)
    assert (current1.receipt_id, current1.receipt_hash, current1.ref) == historical
    assert current2.previous_currentness_ref == current1.ref
    assert rsc1.context_id != rsc2.context_id
    with pytest.raises(m5.M5RuntimeIntegrityError):
        m5.validate_resolved_structural_context(rsc1, repo, query, resolution, current2)
    assert H10 == "REJECT__HISTORICAL_IDENTITY_PRESERVED__REFRESH_PROSPECTIVE"


def test_H11_source_disagreement_cannot_become_actor_uncertainty() -> None:
    with pytest.raises(m6.M6ForbiddenBehavioralSource):
        m6.assert_behavioral_source_rejected(
            object(),
            declared_source_class="SourceDisagreementOrEmpiricalNegativeAsSuch",
            representation="SUMMARY",
        )
    entries, closure, envelope, receiver = tr._bundle("h11")
    called: list[bool] = []
    with pytest.raises(m6.M6ForbiddenBehavioralSource):
        render.realize_bounded_expression(
            **tr._kwargs(entries[0], closure, envelope, receiver),
            forbidden_behavioral_sources=((object(), "SourceDisagreementOrEmpiricalNegativeAsSuch", "PROMPT_FRAGMENT"),),
            renderer=lambda _: called.append(True),
        )
    assert not called
    assert H11 == "NO_BEHAVIORAL_CHANGE_WITHOUT_CURRENT_ACTOR_SAFE_AUTHORITY"


def test_H12_truth_cannot_bypass_actor_accessibility() -> None:
    for source_class in ("ResolvedStructuralContext", "PSEPF", "ANALYST_ONLY_TRUTH"):
        with pytest.raises(m6.M6ForbiddenBehavioralSource):
            m6.assert_behavioral_source_rejected(
                object(), declared_source_class=source_class, representation="DIRECT"
            )
    entries, closure, envelope, receiver = tr._bundle("h12")
    called: list[bool] = []
    with pytest.raises(m6.M6ForbiddenBehavioralSource):
        render.realize_bounded_expression(
            **tr._kwargs(entries[0], closure, envelope, receiver),
            forbidden_behavioral_sources=((object(), "PSEPF", "PROMPT_OR_METADATA_SIDE_CHANNEL"),),
            renderer=lambda _: called.append(True),
        )
    assert not called
    assert H12 == "ZERO_POSITIVE_EXPRESSION_SEMANTICS"


def test_H13_stale_session_fallback_is_nonrestorative() -> None:
    entries, closure, envelope, receiver = tr._bundle("h13")
    entry = entries[0]
    stale = replace(
        receiver,
        causal_time=receiver.causal_time + 1,
        source_actor_state_hash=tr._h("h13-changed-state"),
    )
    called: list[bool] = []
    outcome = render.realize_bounded_expression(
        **tr._kwargs(entry, closure, envelope, stale),
        session_or_transcript_claim_refs=(entry.claim_ref,),
        renderer=lambda _: called.append(True),
    )
    assert outcome.state is render.RenderState.BLOCKED_M6_STALE
    assert outcome.semantic_output is False and outcome.model_called is False and not called
    assert H13 == "REJECT__SESSION_NONCAUSAL_NONRESTORATIVE"


def test_H14_hidden_join_and_scope_widening_are_rejected() -> None:
    first = tr._entry("h14-a")
    second = tr._entry("h14-b")
    entries, closure, envelope, receiver = tr._bundle("h14", entries=(first, second))
    projection, authority, plan = tr._plan(first, closure, envelope, receiver, tag="h14")
    joined = tr._ref("CLAIM", "h14-joined")

    def renderer_candidate(model_input):
        variant = model_input.allowed_variants[0]
        return render.RendererCandidate(
            variant.variant_id,
            variant.text,
            projection.semantic_fingerprint,
            joined,
            projection.component_refs,
            projection.actor_perceived_view_refs,
            projection.temporal_scope_refs,
            projection.subject_scope_refs,
            projection.referent_scope_refs,
            projection.first_person_permission,
        )

    with pytest.raises(render.RenderSemanticConformanceError):
        render.realize_bounded_expression(
            **tr._kwargs(first, closure, envelope, receiver),
            admitted_plan=plan,
            accepted_plan_authority=authority,
            execution=tr._execution("h14"),
            renderer=renderer_candidate,
        )
    assert H14 == "REJECT__MONOTONE_NO_JOIN"


def test_H15_actor_safe_envelope_is_only_a_semantic_ceiling() -> None:
    assert m6.situated_expression_behavior_status() == m6.BLOCKED_NAMED_AUTHORITY_REQUIRED
    with pytest.raises(m6.M6NamedAuthorityRequired):
        m6.require_situated_expression_owner()
    entries, closure, envelope, receiver = tr._bundle("h15")
    called: list[bool] = []
    outcome = render.realize_bounded_expression(
        **tr._kwargs(entries[0], closure, envelope, receiver),
        renderer=lambda _: called.append(True),
    )
    assert outcome.state is render.RenderState.BLOCKED_NAMED_AUTHORITY_REQUIRED
    assert outcome.model_called is False and outcome.semantic_output is False and not called
    assert render.current_positive_plan_authority_status() == m6.BLOCKED_NAMED_AUTHORITY_REQUIRED
    assert H15 == "REJECT__SEMANTIC_CEILING_ONLY"


def test_H16_exact_replay_and_lawful_wording_variability_coexist() -> None:
    entries, closure, envelope, receiver = tr._bundle("h16")
    entry = entries[0]
    _, authority, plan = tr._plan(entry, closure, envelope, receiver, tag="h16")
    execution = tr._execution("h16")
    kwargs = tr._kwargs(entry, closure, envelope, receiver)
    exact1 = render.realize_bounded_expression(
        **kwargs,
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        selected_variant_id="plain",
    )
    exact2 = render.realize_bounded_expression(
        **kwargs,
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        selected_variant_id="plain",
    )
    alternate = render.realize_bounded_expression(
        **kwargs,
        admitted_plan=plan,
        accepted_plan_authority=authority,
        execution=execution,
        selected_variant_id="alternate",
    )
    assert exact1 == exact2
    assert exact1.artifact != alternate.artifact
    assert exact1.artifact.plan_hash == alternate.artifact.plan_hash
    assert exact1.artifact.projection_fingerprint == alternate.artifact.projection_fingerprint
    assert H16 == "ALLOW_LAWFUL_DIVERGENCE_AND_REQUIRE_EXACT_REPLAY"


def test_H17_typed_states_remain_distinct() -> None:
    denied_claim = tr._ref("CLAIM", "h17-denied")
    denied = m6.make_nonrenderable_decision(
        claim_ref=denied_claim,
        permission_record_ref=tr._ref("PERMISSION", "h17-denied"),
        accessibility_state="CLAIM_INACCESSIBLE",
        first_person_permission="DENY_FIRST_PERSON_CLAIM",
    )
    _, closure_d, envelope_d, receiver_d = tr._bundle("h17-denied", entries=(), decisions=(denied,))
    out_denied = render.realize_bounded_expression(
        envelope=envelope_d,
        replay_closure=closure_d,
        receiver=receiver_d,
        requested_claim_ref=denied_claim,
        source_scope_ceiling=m6.ScopeCeiling(),
        requested_first_person_permission="PERMIT_FIRST_PERSON_BELIEF",
    )

    deferred_claim = tr._ref("CLAIM", "h17-deferred")
    deferred = m6.make_nonrenderable_decision(
        claim_ref=deferred_claim,
        permission_record_ref=tr._ref("PERMISSION", "h17-deferred"),
        accessibility_state="CLAIM_ACCESS_UNKNOWN",
        first_person_permission="DEFER_MISSING_AUTHORITY",
    )
    _, closure_f, envelope_f, receiver_f = tr._bundle("h17-deferred", entries=(), decisions=(deferred,))
    out_deferred = render.realize_bounded_expression(
        envelope=envelope_f,
        replay_closure=closure_f,
        receiver=receiver_f,
        requested_claim_ref=deferred_claim,
        source_scope_ceiling=m6.ScopeCeiling(),
        requested_first_person_permission="PERMIT_FIRST_PERSON_BELIEF",
    )

    empty_claim = tr._ref("CLAIM", "h17-empty")
    _, closure_e, envelope_e, receiver_e = tr._bundle("h17-empty", entries=())
    out_empty = render.realize_bounded_expression(
        envelope=envelope_e,
        replay_closure=closure_e,
        receiver=receiver_e,
        requested_claim_ref=empty_claim,
        source_scope_ceiling=m6.ScopeCeiling(),
        requested_first_person_permission="PERMIT_FIRST_PERSON_BELIEF",
    )

    assert {out_denied.state, out_deferred.state, out_empty.state} == {
        render.RenderState.BLOCKED_M6_DENY,
        render.RenderState.BLOCKED_M6_DEFER,
        render.RenderState.VALID_EMPTY_NO_MODEL_CALL,
    }
    assert m3.M3DecisionState.NONCOMPARABLE.value != m3.M3DecisionState.UNKNOWN_AUTHORITY.value
    zero = psepf.evaluate_psepf_zero_positive_guard(tp._request("PSEPF"))
    assert zero.zero_effect is True and zero.actor_state_effect == "ZERO"
    assert H17 == "REJECT__TYPED_STATES_DISTINCT"


def test_H18_rsc_requires_explicit_runtime_resolution() -> None:
    repo, locator, query, resolution = t5._runtime_universe("h18")
    assert resolution.resolved_structural_context is None
    currentness = t5._currentness(resolution, "h18-current")
    rsc = m5.materialize_resolved_structural_context(repo, query, resolution, currentness)
    assert rsc.context_id and rsc.context_content_hash

    denied_repo, _, denied_query, denied_resolution = t5._runtime_universe(
        "h18-denied",
        producer_uses=("REVIEW",),
        v557_uses=("REVIEW",),
        requested_uses=("ACTIVE_CAUSAL",),
    )
    with pytest.raises(m5.M5RuntimeIntegrityError):
        m5.materialize_resolved_structural_context(
            denied_repo,
            denied_query,
            denied_resolution,
            t5._currentness(denied_resolution, "h18-denied-current"),
        )
    assert H18 == "NO_RUNTIME_INSTANCE__EXPLICIT_RESOLUTION_REQUIRED"


def test_H19_only_dispositive_runtime_import_dag_controls() -> None:
    expected = {
        m1: set(),
        m2: {"rawlsing_next.m1_temporal_v554_admission_dedup"},
        m3: {"rawlsing_next.m2_v555_atomic_route"},
        m4: {
            "rawlsing_next.m1_temporal_v554_admission_dedup",
            "rawlsing_next.m2_v555_atomic_route",
            "rawlsing_next.m3_v556_higher_order_structural",
        },
        m5: {"rawlsing_next.m4_v557_v558_publication_repository"},
        m6: {"rawlsing_next.m5_runtime_rsc_peer_prior"},
        render: {"rawlsing_next.m6_actor_safe_expression"},
        psepf: set(),
    }
    for module, imports in expected.items():
        actual = _rawlsing_imports(module)
        assert actual == imports
        assert all("ddm_build" not in item and "STAGE_CLOSE" not in item for item in actual)
    assert render.BOUND_M6_RUNTIME_HEAD == "c7dfd69131d0909cd0e4a7bec223ba64ec5d6167"
    assert render.BOUND_M6_RUNTIME_BLOB == "74d9701cdc7dabccf61eb5089498db290c1efd9c"
    assert H19 == "REJECT__DISPOSITIVE_FINAL_AUTHORITY_CONTROLS"


def test_H20_ambient_authority_shortcuts_fail_closed() -> None:
    with pytest.raises(render.RenderIntegrityError):
        render.ExactAuthorityBinding("AUTH", "latest", "12345678")
    with pytest.raises(m4.M4IntegrityError):
        m4.ResolverPolicy(policy_version="latest")

    upstream = t2._m1()
    request = t2._req(upstream)
    request["route_rule_ref"] = {
        "id": m2.ROUTE_RULE_ID,
        "version": "latest",
        "content_hash": t2._h("not-authority"),
    }
    route = m2.evaluate_m2_v555_atomic_route(upstream, request)
    assert route.decision_state is m2.M2DecisionState.NO_GOVERNED_ROUTE_AUTHORITY
    assert route.route is None

    alias_request = tp._request("GENERIC_WRAPPER")
    alias_request["source_lineage"] = ["PSEPF"]
    alias_decision = psepf.evaluate_psepf_zero_positive_guard(alias_request)
    tp._assert_zero(alias_decision)
    assert alias_decision.reason is psepf.GuardReason.INVALID_OR_UNTYPED_REQUEST
    assert H20 == "FAIL_CLOSED__NO_HEURISTIC_REPAIR"


def test_path_law_P01_P12_exact_additive_clean_sideline() -> None:
    modules = (m1, m2, m3, m4, m5, m6, render, psepf)
    paths = [inspect.getsourcefile(module) for module in modules]
    assert all(path is not None for path in paths)
    assert len(set(paths)) == len(paths)
    assert paths[0].endswith("rawlsing_next/m1_temporal_v554_admission_dedup.py")
    assert paths[5].endswith("rawlsing_next/m6_actor_safe_expression.py")
    assert paths[6].endswith("rawlsing_next/render_bounded_expression.py")
    assert paths[7].endswith("rawlsing_next/v3_psepf_zero_positive_guard.py")

    # P07/P08: structural evidence is nonbehavioral and PSEPF first tranche is exactly zero-positive.
    assert dict(psepf.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}
    for runtime_type in (
        m5.ResolvedStructuralContext,
        m5.RSCValidationReceipt,
        m5.StructuralCurrentnessReceipt,
        m5.StructuralPeerUseReceipt,
    ):
        with pytest.raises(m6.M6ForbiddenBehavioralSource):
            m6.assert_behavioral_source_rejected(object.__new__(runtime_type))

    # P09/P10: render does not widen or fill blocked SPDM authority.
    assert render.current_positive_plan_authority_status() == m6.BLOCKED_NAMED_AUTHORITY_REQUIRED
    assert m6.situated_expression_behavior_status() == m6.BLOCKED_NAMED_AUTHORITY_REQUIRED

    # P11/P12: exact replay is deterministic and missing authority is not repaired heuristically.
    exact_payload = t1._invocation()
    assert m1.evaluate_m1_temporal_v554_admission_dedup(copy.deepcopy(exact_payload)) == m1.evaluate_m1_temporal_v554_admission_dedup(copy.deepcopy(exact_payload))
    with pytest.raises(render.RenderIntegrityError):
        render.ExactAuthorityBinding("AUTH", "default", "12345678")
