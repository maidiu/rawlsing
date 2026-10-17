from dataclasses import replace

import pytest

from rawlsing_next.pre553_discovery_adaptive import (
    ADAPTIVE_COVERAGE_CLAIM,
    ADAPTIVE_DISCOVERY_CONTRACT_ID,
    ADAPTIVE_SEARCH_POLICY_SCHEMA,
    ADAPTIVE_SEARCH_SCHEMA,
    AdaptiveDiscoveryError,
    AdaptiveExplorationUnit,
    AdaptiveSearchCheckpoint,
    AdaptiveSearchIdentityError,
    AdaptiveUnitOutcome,
    PartialSearchNegativeError,
    execute_adaptive_exploration,
    verify_adaptive_replay,
)
from rawlsing_next.pre553_discovery_exact import I05_CONTRACT_ID
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority, ExactRef, semantic_hash
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _h


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:adaptive:{kind.lower()}:{tag}", _h(f"adaptive:{kind}:{tag}"))


def _grammar_ref(definition, tag):
    digest = semantic_hash(definition)
    return ExactRef("PRE553_ADAPTIVE_SEARCH_UNIVERSE", f"urn:test:adaptive:grammar:{tag}:{digest}", digest)


def _authority(tag="a", *, policy_version="1", mode="ADAPTIVE_EXPLORATORY"):
    frontier = _auth(
        f"adaptive-frontier-{tag}",
        "DISCOVERY_FRONTIER",
        families=("DiscoveryAuthority@1.0.0",),
    )
    replay = _auth(
        f"adaptive-replay-{tag}",
        "REPLAY_PROTOCOL",
        families=("DiscoveryAuthority@1.0.0", "ReplayReceipt@1.0.0"),
    )
    root_rule = _ref("ADAPTIVE_PROPOSAL_RULE", f"root-{tag}")
    child_rule = _ref("ADAPTIVE_PROPOSAL_RULE", f"child-{tag}")
    definition = {
        "schema": ADAPTIVE_SEARCH_SCHEMA,
        "discovery_operation": f"I03-OP-adaptive-frontier-{tag}",
        "replay_operation": f"I03-OP-adaptive-replay-{tag}",
        "allowed_proposal_rule_refs": (root_rule, child_rule),
        "maximum_generation": 3,
        "maximum_frontier_size": 32,
    }
    policy = {
        "schema": ADAPTIVE_SEARCH_POLICY_SCHEMA,
        "policy_id": f"fixture-{tag}",
        "policy_version": policy_version,
        "ranking_rule": "DECLARED_HEURISTIC_RANK_DESC_THEN_UNIT_REF",
        "result_driven_changes_only_between_sealed_units": True,
        "partial_search_negative_forbidden": True,
        "promotion_requires_exact_validation": True,
    }
    adaptive = mode == "ADAPTIVE_EXPLORATORY"
    authority = DiscoveryAuthority(
        typed_state="ADAPTIVE_EXPLORATORY_AUTHORIZED" if adaptive else "EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(frontier.authority_ref, replay.authority_ref),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}-{policy_version}-{mode}"),
        candidate_grammar_ref=_grammar_ref(definition, f"{tag}-{policy_version}-{mode}"),
        candidate_universe_definition=definition,
        source_universe_scope={"kind": "EXACT_AUTHORITY_BOUNDED"},
        risk_set_scope={"kind": "EXACT_AUTHORITY_BOUNDED"},
        topology_scope={"kind": "SEALED_EVALUATION_UNITS"},
        measure_scope={"kind": "EXACT_UNIT_OWNED"},
        support_rules={"kind": "EXACT_UNIT_OWNED"},
        validation_rules={"kind": "EXACT_UNIT_OWNED"},
        coverage_claim=ADAPTIVE_COVERAGE_CLAIM if adaptive else "COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        pruning_contract={
            "kind": "ADAPTIVE_PARTIAL_SEARCH_BETWEEN_SEALED_UNITS",
            "unvisited_state": "UNKNOWN_UNVISITED",
        },
        algorithm_identity_if_semantically_required=ADAPTIVE_DISCOVERY_CONTRACT_ID,
        tie_order_rules="HEURISTIC_RANK_DESC_THEN_UNIT_REF",
        rng_policy_if_any="NONE",
        mode=mode,
        adaptive_search_policy=policy,
    )
    return authority, AuthorityRegistry((frontier, replay)), root_rule, child_rule


def _unit(tag, determinant, rule, *, rank, generation=0, parent=None, extra=()):
    return AdaptiveExplorationUnit(
        unit_ref=_ref("SEALED_EXPLORATION_UNIT", tag),
        proposal_rule_ref=rule,
        generation=generation,
        heuristic_rank=rank,
        determinant_refs=(determinant, *extra),
        parent_unit_ref=parent,
    )


def _sealed_result(unit, suffix="stable"):
    return _ref("SEALED_EXACT_DISCOVERY_RESULT", f"{unit.unit_ref.content_hash[:12]}-{suffix}")


def _no_proposal_evaluator(unit, history):
    del history
    return AdaptiveUnitOutcome(
        unit_ref=unit.unit_ref,
        sealed_result_ref=_sealed_result(unit),
        proposal_basis_ref=_ref("ADAPTIVE_PROPOSAL_BASIS", f"none-{unit.unit_ref.content_hash[:12]}"),
        unit_result_state="SEALED_EXACT_UNIT_COMPLETE",
    )


def test_budget_truncation_preserves_explicit_unknown_and_forbids_partial_negative():
    authority, registry, root_rule, _ = _authority("budget")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "budget")
    roots = (
        _unit("budget-a", determinant, root_rule, rank=30),
        _unit("budget-b", determinant, root_rule, rank=20),
        _unit("budget-c", determinant, root_rule, rank=10),
    )
    result = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=_no_proposal_evaluator,
        budget=1,
    )
    assert result.completeness_state == "PARTIAL_BUDGET_EXHAUSTED"
    assert result.visited_unit_refs == (roots[0].unit_ref,)
    assert set(result.unvisited_unit_refs) == {roots[1].unit_ref, roots[2].unit_ref}
    assert result.global_negative_claim is False
    assert result.semantic_truth_effect is False
    with pytest.raises(PartialSearchNegativeError):
        replace(result, global_negative_claim=True)


def test_result_driven_widening_occurs_only_after_sealed_unit_and_can_reprioritize_future_work():
    authority, registry, root_rule, child_rule = _authority("widen")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "widen")
    root = _unit("widen-root", determinant, root_rule, rank=20)
    later_root = _unit("widen-later-root", determinant, root_rule, rank=10)

    def evaluator(unit, history):
        sealed = _sealed_result(unit)
        proposals = ()
        if unit.unit_ref == root.unit_ref:
            assert len(history) == 0
            proposals = (_unit(
                "widen-child",
                determinant,
                child_rule,
                rank=100,
                generation=1,
                parent=root.unit_ref,
                extra=(sealed,),
            ),)
        return AdaptiveUnitOutcome(
            unit_ref=unit.unit_ref,
            sealed_result_ref=sealed,
            proposal_basis_ref=_ref("ADAPTIVE_PROPOSAL_BASIS", f"basis-{unit.unit_ref.content_hash[:12]}"),
            unit_result_state="SEALED_EXACT_UNIT_COMPLETE",
            proposal_units=proposals,
        )

    result = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=(later_root, root),
        evaluate_unit=evaluator,
        budget=2,
    )
    assert result.visited_unit_refs[0] == root.unit_ref
    assert result.checkpoint.visits[1].unit.parent_unit_ref == root.unit_ref
    assert result.checkpoint.visits[1].unit.heuristic_rank == 100
    assert result.unvisited_unit_refs == (later_root.unit_ref,)


def test_restart_from_canonical_checkpoint_matches_one_shot_exhaustive_completion_and_storage_reorder():
    authority, registry, root_rule, child_rule = _authority("restart")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "restart")
    root = _unit("restart-root", determinant, root_rule, rank=20)
    later = _unit("restart-later", determinant, root_rule, rank=10)

    def evaluator(unit, history):
        del history
        sealed = _sealed_result(unit)
        proposals = ()
        if unit.unit_ref == root.unit_ref:
            proposals = (_unit(
                "restart-child", determinant, child_rule, rank=50,
                generation=1, parent=root.unit_ref, extra=(sealed,),
            ),)
        return AdaptiveUnitOutcome(
            unit_ref=unit.unit_ref,
            sealed_result_ref=sealed,
            proposal_basis_ref=_ref("ADAPTIVE_PROPOSAL_BASIS", f"restart-{unit.unit_ref.content_hash[:12]}"),
            unit_result_state="SEALED_EXACT_UNIT_COMPLETE",
            proposal_units=proposals,
        )

    one_shot = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=(later, root),
        evaluate_unit=evaluator,
        budget=20,
    )
    first = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=(root, later),
        evaluate_unit=evaluator,
        budget=1,
    )
    restored = AdaptiveSearchCheckpoint.from_dict(first.checkpoint.as_dict())
    resumed = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=(later, root),
        evaluate_unit=evaluator,
        budget=20,
        resume_from=restored,
    )
    assert one_shot.completeness_state == resumed.completeness_state == "EXPLORATORY_POLICY_FRONTIER_EXHAUSTED"
    assert one_shot.visited_unit_refs == resumed.visited_unit_refs
    assert one_shot.checkpoint.ref == resumed.checkpoint.ref
    assert one_shot.result_ref == resumed.result_ref
    assert one_shot.unvisited_unit_refs == resumed.unvisited_unit_refs == ()


def test_interruption_stops_only_after_complete_sealed_unit_and_restart_cannot_skip_unvisited():
    authority, registry, root_rule, _ = _authority("interrupt")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "interrupt")
    roots = tuple(_unit(f"interrupt-{idx}", determinant, root_rule, rank=10 - idx) for idx in range(3))
    interrupted = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=_no_proposal_evaluator,
        budget=3,
        interrupt_after=1,
    )
    assert interrupted.completeness_state == "PARTIAL_INTERRUPTED"
    assert len(interrupted.visited_unit_refs) == 1
    assert len(interrupted.unvisited_unit_refs) == 2
    resumed = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=_no_proposal_evaluator,
        budget=3,
        resume_from=AdaptiveSearchCheckpoint.from_dict(interrupted.checkpoint.as_dict()),
    )
    assert len(resumed.visited_unit_refs) == 3
    assert len(set(resumed.visited_unit_refs)) == 3
    assert resumed.unvisited_unit_refs == ()


def test_identical_policy_determinant_and_budget_replay_exactly_and_nondeterminism_is_typed():
    authority, registry, root_rule, _ = _authority("replay")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "replay")
    roots = (_unit("replay-a", determinant, root_rule, rank=2), _unit("replay-b", determinant, root_rule, rank=1))
    expected = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=_no_proposal_evaluator,
        budget=1,
    )
    receipt = verify_adaptive_replay(
        expected,
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=_no_proposal_evaluator,
        budget=1,
    )
    assert receipt.typed_state == receipt.replay_state == "REPLAY_VERIFIED"
    assert receipt.semantic_truth_effect is False
    assert receipt.actor_v3_effect is False

    calls = {"n": 0}
    def unstable(unit, history):
        del history
        calls["n"] += 1
        return AdaptiveUnitOutcome(
            unit_ref=unit.unit_ref,
            sealed_result_ref=_sealed_result(unit, suffix=f"unstable-{calls['n']}"),
            proposal_basis_ref=_ref("ADAPTIVE_PROPOSAL_BASIS", "unstable"),
            unit_result_state="SEALED_EXACT_UNIT_COMPLETE",
        )
    unstable_expected = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=unstable,
        budget=1,
    )
    bad = verify_adaptive_replay(
        unstable_expected,
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=unstable,
        budget=1,
    )
    assert bad.typed_state == bad.replay_state == "NONDETERMINISTIC_REPLAY"


def test_policy_version_change_changes_identity_and_cannot_resume_old_checkpoint():
    a1, r1, root_rule1, _ = _authority("policy", policy_version="1")
    a2, r2, root_rule2, _ = _authority("policy", policy_version="2")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "policy")
    root1 = _unit("policy-root", determinant, root_rule1, rank=1)
    root2 = _unit("policy-root", determinant, root_rule2, rank=1)
    first = execute_adaptive_exploration(
        discovery_authority=a1,
        authority_registry=r1,
        determinant_state_ref=determinant,
        initial_units=(root1,),
        evaluate_unit=_no_proposal_evaluator,
        budget=0,
    )
    second = execute_adaptive_exploration(
        discovery_authority=a2,
        authority_registry=r2,
        determinant_state_ref=determinant,
        initial_units=(root2,),
        evaluate_unit=_no_proposal_evaluator,
        budget=0,
    )
    assert first.search_policy_ref != second.search_policy_ref
    assert first.result_ref != second.result_ref
    with pytest.raises(AdaptiveSearchIdentityError):
        execute_adaptive_exploration(
            discovery_authority=a2,
            authority_registry=r2,
            determinant_state_ref=determinant,
            initial_units=(root2,),
            evaluate_unit=_no_proposal_evaluator,
            budget=1,
            resume_from=first.checkpoint,
        )


def test_partial_valid_empty_unit_never_becomes_global_negative():
    authority, registry, root_rule, _ = _authority("empty")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "empty")
    roots = (_unit("empty-a", determinant, root_rule, rank=2), _unit("empty-b", determinant, root_rule, rank=1))

    def valid_empty(unit, history):
        del history
        return AdaptiveUnitOutcome(
            unit_ref=unit.unit_ref,
            sealed_result_ref=_sealed_result(unit, suffix="valid-empty"),
            proposal_basis_ref=_ref("ADAPTIVE_PROPOSAL_BASIS", "valid-empty"),
            unit_result_state="SEALED_EXACT_VALID_EMPTY",
            global_negative_claim=False,
        )

    partial = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=roots,
        evaluate_unit=valid_empty,
        budget=1,
    )
    assert partial.completeness_state == "PARTIAL_BUDGET_EXHAUSTED"
    assert len(partial.unvisited_unit_refs) == 1
    assert partial.global_negative_claim is False


def test_exact_mode_is_rejected_by_adaptive_service_and_i05_contract_remains_distinct():
    exact_authority, registry, root_rule, _ = _authority("exact", mode="EXACT_BOUNDED")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "exact")
    root = _unit("exact-root", determinant, root_rule, rank=1)
    assert I05_CONTRACT_ID == "PRE553_I05_EXACT_BOUNDED_DISCOVERY@1.0.0"
    assert ADAPTIVE_DISCOVERY_CONTRACT_ID != I05_CONTRACT_ID
    with pytest.raises(AdaptiveDiscoveryError):
        execute_adaptive_exploration(
            discovery_authority=exact_authority,
            authority_registry=registry,
            determinant_state_ref=determinant,
            initial_units=(root,),
            evaluate_unit=_no_proposal_evaluator,
            budget=1,
        )
