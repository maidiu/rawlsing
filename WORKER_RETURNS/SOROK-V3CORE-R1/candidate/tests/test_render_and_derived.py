from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from conftest import projection

from v3.core.invariants import (
    DERIVED_INDEX_NAMES,
    assert_no_derived_fields_in_backbone,
    backbone_hash,
)
from v3.core.state import BackboneState
from v3core_adapter.contracts import Status
from v3core_adapter.derived_scope import derive_scoped, material_capacity_index
from v3core_adapter.render import render_readonly


def test_default_render_is_nonmutating() -> None:
    proj = projection()
    before = backbone_hash(proj.state)
    outcome = render_readonly(proj.state, None)
    assert outcome.status == Status.DERIVED_EVALUATED_SCOPED
    assert outcome.backbone_hash_before == outcome.backbone_hash_after == before
    assert proj.state.rendered_output is not None


def test_malicious_renderer_mutation_is_rolled_back() -> None:
    proj = projection()
    before = backbone_hash(proj.state)

    def renderer(state, derived, config) -> None:
        state.domains["empire_occupation"].A = 99.0

    outcome = render_readonly(proj.state, None, renderer=renderer)
    assert outcome.status == Status.HELD_RENDERER_MUTATION
    assert outcome.reason == "renderer_mutated_backbone"
    assert backbone_hash(proj.state) == before
    assert proj.state.domains["empire_occupation"].A == 0
    assert proj.state.rendered_output is None


def test_derivation_is_scoped_and_does_not_mutate_live_state() -> None:
    proj = projection()
    before = proj.state_hash()
    before_index = material_capacity_index(proj.state)
    outcome = derive_scoped(proj.state)
    assert outcome.status == Status.DERIVED_EVALUATED_SCOPED
    assert outcome.live_state_mutated is False
    assert proj.state_hash() == before
    assert outcome.published is not None
    assert outcome.published.material_capacity_index == before_index
    assert outcome.published.index_status["agency_capacity_AC"] == Status.HELD_MISSING_ISSUED_RULE.value
    assert outcome.published.index_status["insulation_score"] == Status.HELD_MISSING_ISSUED_RULE.value
    assert outcome.diagnostic["hostage_index"] >= 0
    assert proj.state.metabolic_style == {}
    assert proj.state.registers.public_expression_gate == 0


def test_published_derived_is_immutable() -> None:
    outcome = derive_scoped(projection().state)
    with pytest.raises(FrozenInstanceError):
        outcome.published.material_capacity_index = 99.0  # type: ignore[misc]


def test_derived_fields_are_not_backbone_fields() -> None:
    assert_no_derived_fields_in_backbone()
    assert DERIVED_INDEX_NAMES.isdisjoint(BackboneState.__dataclass_fields__)
