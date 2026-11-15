from __future__ import annotations

import pytest

from rawlsing_next.pre553_discovery_adaptive import (
    AdaptiveDiscoveryError,
    AdaptiveSearchCheckpoint,
    AdaptiveSearchIdentityError,
    AdaptiveUnitOutcome,
    execute_adaptive_exploration,
)
from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority
from rawlsing_next.tests.test_pre553_discovery_adaptive import (
    _authority,
    _no_proposal_evaluator,
    _ref,
    _sealed_result,
    _unit,
)


def test_a04_determinant_state_change_invalidates_old_checkpoint():
    authority, registry, root_rule, _ = _authority("a04-determinant")
    determinant_a = _ref("ADAPTIVE_DETERMINANT_STATE", "a04-a")
    determinant_b = _ref("ADAPTIVE_DETERMINANT_STATE", "a04-b")
    root_a = _unit("a04-root", determinant_a, root_rule, rank=1)
    root_b = _unit("a04-root", determinant_b, root_rule, rank=1)

    first = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant_a,
        initial_units=(root_a,),
        evaluate_unit=_no_proposal_evaluator,
        budget=0,
    )
    restored = AdaptiveSearchCheckpoint.from_dict(first.checkpoint.as_dict())

    with pytest.raises(AdaptiveSearchIdentityError, match="determinant state changed"):
        execute_adaptive_exploration(
            discovery_authority=authority,
            authority_registry=registry,
            determinant_state_ref=determinant_b,
            initial_units=(root_b,),
            evaluate_unit=_no_proposal_evaluator,
            budget=1,
            resume_from=restored,
        )


def test_a04_same_version_policy_content_change_invalidates_old_checkpoint():
    authority, registry, root_rule, _ = _authority("a04-policy-content", policy_version="1")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "a04-policy-content")
    root = _unit("a04-policy-root", determinant, root_rule, rank=1)

    first = execute_adaptive_exploration(
        discovery_authority=authority,
        authority_registry=registry,
        determinant_state_ref=determinant,
        initial_units=(root,),
        evaluate_unit=_no_proposal_evaluator,
        budget=0,
    )

    semantic_fields = dict(authority.semantic_fields)
    changed_policy = dict(semantic_fields["adaptive_search_policy"])
    assert changed_policy["policy_version"] == "1"
    changed_policy["same_version_policy_content_revision"] = "A04_HOSTILE_CHANGE"
    semantic_fields["adaptive_search_policy"] = changed_policy
    changed = DiscoveryAuthority(
        typed_state=authority.typed_state,
        authority_snapshot_refs=authority.authority_snapshot_refs,
        dependency_refs=authority.dependency_refs,
        producer_replay_locator_or_reference_root=authority.producer_replay_locator_or_reference_root,
        **semantic_fields,
    )
    assert changed.ref != authority.ref

    with pytest.raises(AdaptiveSearchIdentityError, match="resume authority changed|search policy/version changed"):
        execute_adaptive_exploration(
            discovery_authority=changed,
            authority_registry=registry,
            determinant_state_ref=determinant,
            initial_units=(root,),
            evaluate_unit=_no_proposal_evaluator,
            budget=1,
            resume_from=first.checkpoint,
        )


def test_a04_unsealed_evaluation_outcome_cannot_enter_adaptive_frontier():
    authority, registry, root_rule, _ = _authority("a04-unsealed")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "a04-unsealed")
    root = _unit("a04-unsealed-root", determinant, root_rule, rank=1)

    def evaluator(unit, history):
        del history
        return AdaptiveUnitOutcome(
            unit_ref=unit.unit_ref,
            sealed_result_ref=_sealed_result(unit),
            proposal_basis_ref=_ref("ADAPTIVE_PROPOSAL_BASIS", "a04-unsealed"),
            unit_result_state="PARTIAL_UNIT_RESULT",
            sealed_unit_coverage="PARTIAL_EVALUATION_UNIT",
        )

    with pytest.raises(AdaptiveDiscoveryError, match="complete sealed evaluation units"):
        execute_adaptive_exploration(
            discovery_authority=authority,
            authority_registry=registry,
            determinant_state_ref=determinant,
            initial_units=(root,),
            evaluate_unit=evaluator,
            budget=1,
        )
