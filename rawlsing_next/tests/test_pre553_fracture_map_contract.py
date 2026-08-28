import pytest

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    assert_zero_actor_v3_v2_effect,
    require_public_object_family,
    semantic_hash,
)
from rawlsing_next.pre553_fracture_map_contract import (
    AUTHORITY37_MAXIMUM_DEPTH,
    AUTHORITY37_MINIMUM_REPORT_RAW_N,
    AUTHORITY37_MINIMUM_SPLIT_RAW_N,
    EmpiricalFractureMapReceipt,
    FractureMapContinuationDecision,
    FractureMapControllerPolicy,
)


def _h(tag):
    return semantic_hash({"tag": tag})


def _ref(kind, tag):
    return ExactRef(kind, f"urn:test:{kind}:{tag}", _h(f"{kind}:{tag}"))


def _aref(tag):
    return AuthorityRef(
        f"urn:test:authority:{tag}",
        "git:test",
        _h(f"authority:{tag}"),
    )


def _policy(tag="p", **overrides):
    return FractureMapControllerPolicy(
        policy_authority_ref=_aref(tag),
        **overrides,
    )


def _decision(policy, tag="d", *, continuation="RETAIN_AND_CONTINUE_ELIGIBLE",
              retention="RETAIN_EXACT_BRANCH", stop_reason="NONE",
              producer_state="DISCOVERED_RESULT_SUPPORTED", depth=0):
    return FractureMapContinuationDecision(
        controller_policy_ref=policy.ref,
        controller_policy_authority_ref=policy.policy_authority_ref,
        branch_predicate_ref=_ref("EmpiricalPredicate@1.0.0", f"branch:{tag}"),
        producer_state_bindings=(
            (_ref("DiscoveryResultReceipt@1.0.0", f"producer:{tag}"), producer_state),
        ),
        retention_disposition=retention,
        continuation_disposition=continuation,
        stop_reason=stop_reason,
        depth=depth,
    )


def _receipt(tag="r", *, source_order=("a", "b"), branch_order=("a", "b"),
             extra_dependencies=(), **extra):
    authority = _aref(f"policy:{tag}")
    policy = FractureMapControllerPolicy(policy_authority_ref=authority)
    decision = FractureMapContinuationDecision(
        controller_policy_ref=policy.ref,
        controller_policy_authority_ref=authority,
        branch_predicate_ref=_ref("EmpiricalPredicate@1.0.0", f"branch:{tag}:a"),
        producer_state_bindings=(
            (_ref("DiscoveryResultReceipt@1.0.0", f"producer:{tag}"), "DISCOVERED_RESULT_SUPPORTED"),
        ),
        retention_disposition="RETAIN_EXACT_BRANCH",
        continuation_disposition="RETAIN_TERMINAL_STOP",
        stop_reason="MAX_DEPTH",
        depth=4,
    )

    root = _ref("EmpiricalQuerySpec@1.0.0", f"root:{tag}")
    sources = tuple(_ref("C11LogicalRelease", f"{tag}:{x}") for x in source_order)
    branches = tuple(
        _ref("EmpiricalPredicate@1.0.0", f"branch:{tag}:{x}") for x in branch_order
    )
    ancestry = (_ref("PRE553_RECURSIVE_HANDOFF", f"ancestor:{tag}"),)
    frontiers = (
        _ref("PRE553_I05_EVALUATED_FRONTIER", f"frontier:{tag}:0"),
        _ref("PRE553_I05_EVALUATED_FRONTIER", f"frontier:{tag}:1"),
    )
    facts = (_ref("EmpiricalFact@1.0.0", f"fact:{tag}"),)
    discovery = (_ref("DiscoveryResultReceipt@1.0.0", f"discovery:{tag}"),)
    topology = (_ref("PRE553_BRANCH_COSIGNATURE_TOPOLOGY_CLOSURE", f"cosig:{tag}"),)
    decisions = (decision.ref,)
    replay = _ref("PRE553_FRACTURE_MAP_REPLAY", f"replay:{tag}")

    dependencies = (
        root,
        *sources,
        policy.ref,
        *branches,
        *ancestry,
        *frontiers,
        *facts,
        *discovery,
        *topology,
        *decisions,
        replay,
        *extra_dependencies,
    )
    fields = dict(
        root_query_ref=root,
        source_release_refs=sources,
        controller_policy_ref=policy.ref,
        controller_policy_authority_ref=authority,
        branch_predicate_refs=branches,
        branch_ancestry_refs=ancestry,
        generation_frontier_refs=frontiers,
        empirical_fact_refs=facts,
        discovery_result_receipt_refs=discovery,
        branch_cosignature_topology_closure_refs=topology,
        continuation_decision_refs=decisions,
        final_replay_ref=replay,
        closure_state="FRACTURE_MAP_CLOSURE_COMPLETE",
        copied_empirical_payload=False,
        pre_v3_actor_independent=True,
        requires_separate_semantic_transformation_authority=True,
        requires_separate_structural_admission_authority=True,
        requires_separate_actor_binding_authority=True,
        requires_explicit_v3_metabolism_authority=True,
        actor_state_effect=False,
        v3_state_effect=False,
        v2_state_effect=False,
        persona_effect=False,
        belief_effect=False,
        response_effect=False,
    )
    fields.update(extra)
    return EmpiricalFractureMapReceipt(
        typed_state="FRACTURE_MAP_CLOSURE_COMPLETE",
        authority_snapshot_refs=(authority,),
        dependency_refs=dependencies,
        producer_replay_locator_or_reference_root=replay,
        **fields,
    )


def test_authority37_v1_policy_identity_is_deterministic_and_defaults_are_exact():
    left = _policy("same")
    right = _policy("same")
    assert left.ref == right.ref
    assert left.minimum_split_raw_n == AUTHORITY37_MINIMUM_SPLIT_RAW_N == 50
    assert left.minimum_report_raw_n == AUTHORITY37_MINIMUM_REPORT_RAW_N == 25
    assert left.maximum_depth == AUTHORITY37_MAXIMUM_DEPTH == 4
    assert left.semantic_projection()["branch_retention_policy"] == (
        "STOP_RECURSION_NEVER_DELETES_RETAINED_BRANCH"
    )


def test_authority37_v1_threshold_change_requires_policy_version_change():
    authority = _aref("version")
    with pytest.raises(Pre553IntegrityError):
        FractureMapControllerPolicy(
            policy_authority_ref=authority,
            minimum_split_raw_n=51,
        )
    v2 = FractureMapControllerPolicy(
        policy_authority_ref=authority,
        policy_version="1.0.1",
        minimum_split_raw_n=51,
    )
    v1 = FractureMapControllerPolicy(policy_authority_ref=authority)
    assert v1.ref != v2.ref


def test_retention_is_not_recursion():
    policy = _policy("retention")
    continued = _decision(policy, "same")
    stopped = _decision(
        policy,
        "same",
        continuation="RETAIN_REPORT_ONLY_STOP",
        retention="RETAIN_RESULT_WITH_LIMITATION",
        stop_reason="LOW_N_OR_INSUFFICIENT_SUPPORT",
    )
    assert continued.retains_branch_or_typed_result is True
    assert stopped.retains_branch_or_typed_result is True
    assert continued.may_recurse is True
    assert stopped.may_recurse is False
    assert continued.ref != stopped.ref


def test_continuation_decision_preserves_producer_typed_state_exactly():
    policy = _policy("typed")
    decision = FractureMapContinuationDecision(
        controller_policy_ref=policy.ref,
        controller_policy_authority_ref=policy.policy_authority_ref,
        branch_predicate_ref=_ref("EmpiricalPredicate@1.0.0", "typed-branch"),
        producer_state_bindings=(
            (_ref("EmpiricalFact@1.0.0", "typed-fact"), "VALID_EMPTY"),
            (_ref("DiscoveryResultReceipt@1.0.0", "typed-discovery"), "NONCOMPARABLE"),
        ),
        retention_disposition="RETAIN_TYPED_RESULT",
        continuation_disposition="RETAIN_TYPED_NONPOSITIVE_STOP",
        stop_reason="VALID_EMPTY",
        depth=1,
    )
    assert decision.producer_typed_states == ("NONCOMPARABLE", "VALID_EMPTY")
    projection_states = tuple(
        binding["producer_typed_state"]
        for binding in decision.semantic_projection()["producer_state_bindings"]
    )
    assert projection_states == ("NONCOMPARABLE", "VALID_EMPTY")


def test_stopped_decision_requires_exact_stop_reason_and_continue_requires_none():
    policy = _policy("stops")
    with pytest.raises(Pre553IntegrityError):
        _decision(
            policy,
            "bad-stop",
            continuation="RETAIN_TERMINAL_STOP",
            stop_reason="SOME_NEARBY_REASON",
        )
    with pytest.raises(Pre553IntegrityError):
        _decision(
            policy,
            "bad-continue",
            continuation="RETAIN_AND_CONTINUE_ELIGIBLE",
            stop_reason="MAX_DEPTH",
        )


def test_map_receipt_is_public_ref_only_and_set_order_canonical():
    assert require_public_object_family("EmpiricalFractureMapReceipt") == (
        "EmpiricalFractureMapReceipt"
    )
    left = _receipt("same", source_order=("a", "b"), branch_order=("a", "b"))
    right = _receipt("same", source_order=("b", "a"), branch_order=("b", "a"))
    assert left.ref == right.ref
    assert left.copied_empirical_payload is False
    assert_zero_actor_v3_v2_effect(left)


def test_map_receipt_rejects_copied_empirical_payload_and_unknown_payload_field():
    with pytest.raises(Pre553SemanticCollapseError):
        _receipt("payload", copied_empirical_payload=True)
    with pytest.raises(Pre553IntegrityError):
        _receipt("extra", empirical_payload={"respondents": ["R1"]})


def test_map_receipt_requires_full_exact_dependency_closure_and_replay_root():
    good = _receipt("closure")
    assert good.final_replay_ref == good.producer_replay_locator_or_reference_root.as_dict()

    authority = _aref("bad-closure")
    policy = FractureMapControllerPolicy(policy_authority_ref=authority)
    root = _ref("EmpiricalQuerySpec@1.0.0", "bad-root")
    source = _ref("C11LogicalRelease", "bad-source")
    frontier = _ref("PRE553_I05_EVALUATED_FRONTIER", "bad-frontier")
    replay = _ref("PRE553_FRACTURE_MAP_REPLAY", "bad-replay")
    with pytest.raises(Pre553IntegrityError):
        EmpiricalFractureMapReceipt(
            typed_state="FRACTURE_MAP_CLOSURE_BLOCKED",
            authority_snapshot_refs=(authority,),
            dependency_refs=(root, source, policy.ref, frontier),  # replay deliberately missing
            producer_replay_locator_or_reference_root=replay,
            root_query_ref=root,
            source_release_refs=(source,),
            controller_policy_ref=policy.ref,
            controller_policy_authority_ref=authority,
            branch_predicate_refs=(),
            branch_ancestry_refs=(),
            generation_frontier_refs=(frontier,),
            empirical_fact_refs=(),
            discovery_result_receipt_refs=(),
            branch_cosignature_topology_closure_refs=(),
            continuation_decision_refs=(),
            final_replay_ref=replay,
            closure_state="FRACTURE_MAP_CLOSURE_BLOCKED",
            copied_empirical_payload=False,
            pre_v3_actor_independent=True,
            requires_separate_semantic_transformation_authority=True,
            requires_separate_structural_admission_authority=True,
            requires_separate_actor_binding_authority=True,
            requires_explicit_v3_metabolism_authority=True,
            actor_state_effect=False,
            v3_state_effect=False,
            v2_state_effect=False,
            persona_effect=False,
            belief_effect=False,
            response_effect=False,
        )


def test_policy_and_decision_firewall_fields_are_inert():
    policy = _policy("firewall")
    decision = _decision(policy, "firewall")
    for projection in (policy.semantic_projection(), decision.semantic_projection()):
        assert projection["pre_v3_actor_independent"] is True
        for field in (
            "actor_state_effect",
            "v3_state_effect",
            "v2_state_effect",
            "persona_effect",
            "belief_effect",
            "response_effect",
        ):
            assert projection[field] is False
