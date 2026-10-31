# v3/tests/test_architecture_invariants.py
# Wave 2.2: Architecture integrity — render/events/step order/derived not stored.
# These protect the ontological split (physics vs phenomenology; no circular causality).

from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from v3.core.config_loader import (
    get_core_step_ids,
    get_extension_policy,
    get_step_list,
    load_step_order,
    load_v3config,
)
from v3.core.derived import compute_all_derived
from v3.core.invariants import backbone_hash, assert_no_derived_fields_in_backbone
from v3.core.state import BackboneState
from v3.engine.event_engine import sample_events
from v3.io.json_codec import state_to_dict
from v3.render.phenomenology import render_year

# Core step ids (spine). Test asserts these appear in order as a subsequence; extensions allowed per config.
CANONICAL_STEP_IDS = (
    "field_update",
    "autonomy_safety_micro_drift",
    "event_sampling",
    "reproduction_constraints_update",
    "capacity_update",
    "health_drift_update",
    "buffers_update",
    "frameworks_update",
    "domains_update",
    "cracks_and_alienation_update",
    "plasticity_and_metabolization_update",
    "stability_inertia_dissipation",
    "striving_update",
    "practice_and_infrastructure_update",
    "topology_and_boundary_update",
    "attention_and_capture_update",
    "strategy_and_signal_effects",
    "style_trait_drift",
    "render_layer",
)


def test_llm_no_backbone_mutation() -> None:
    """Render must not mutate backbone: only rendered_output may change. Enforced via backbone hash."""
    config = load_v3config()
    state = BackboneState(year=1, age=26)
    derived = compute_all_derived(state)
    state_copy = copy.deepcopy(state)
    hash_before = backbone_hash(state)
    render_year(state, derived, config)
    hash_after = backbone_hash(state)
    assert hash_before == hash_after, (
        "render_layer must not mutate backbone; only state.rendered_output may change. "
        "Backbone hash changed across render_year."
    )
    assert state.rendered_output is not None, "render must set rendered_output"
    # Copy was not rendered; backbone of state should match copy (hash already asserted).
    assert backbone_hash(state_copy) == hash_before
    print(f"  backbone hash unchanged after render; rendered_output set ({len(state.rendered_output or {})} keys)")


def test_events_cannot_write_domains_or_peak_routing() -> None:
    """Events step must not write to domains or peak_routing (prohibits_mutation_of contract).
    We compare only state.domains and state.peak_routing; event payloads may contain domain/strata
    hints (for downstream steps) without failing this test."""
    config = load_v3config()
    state = BackboneState(year=1, age=26)
    derived = compute_all_derived(state)
    before = state_to_dict(copy.deepcopy(state))
    sample_events(state, derived, config)
    after = state_to_dict(state)
    assert after["domains"] == before["domains"], (
        "event_sampling must not mutate state.domains"
    )
    assert after["peak_routing"] == before["peak_routing"], (
        "event_sampling must not mutate state.peak_routing"
    )
    print(f"  event_sampling: domains and peak_routing unchanged (only events_this_year written)")


def test_step_order_immutable() -> None:
    """Core step ids must appear in order as a subsequence of steps. Extensions allowed per extension_policy."""
    step_order = load_step_order()
    core_ids = get_core_step_ids(step_order)
    steps = get_step_list(step_order)
    ids = [s.get("id") for s in steps if s.get("id")]
    assert core_ids == list(CANONICAL_STEP_IDS), (
        f"config core_steps must match canonical spine. Got {core_ids}."
    )
    # Subsequence: core ids must appear in this order (gaps from extensions allowed).
    idx = 0
    for cid in core_ids:
        try:
            pos = ids.index(cid, idx)
        except ValueError:
            raise AssertionError(
                f"Core step id {cid!r} missing or out of order in steps. "
                f"Expected core spine as subsequence; got ids={ids}."
            )
        idx = pos + 1
    # Extension policy: append_only => every step not in core must appear after the last core step.
    policy = get_extension_policy(step_order)
    core_set = set(core_ids)
    extension_positions = [i for i, sid in enumerate(ids) if sid not in core_set]
    if policy == "append_only" and extension_positions and core_ids:
        last_core_position = max(ids.index(c) for c in core_ids)
        for pos in extension_positions:
            assert pos > last_core_position, (
                f"extension_policy=append_only: step id {ids[pos]!r} at position {pos} must be after "
                f"last core step (position {last_core_position}). Move extensions after render_layer."
            )
    print(f"  core_steps ({len(core_ids)} ids) appear in order as subsequence; extension_policy={policy}")


def test_no_derived_fields_in_backbone_state() -> None:
    """BackboneState must not store derived indices (hostage_index, AC, SL, etc.); they are computed only."""
    assert_no_derived_fields_in_backbone()
    print(f"  BackboneState: no stored derived fields (hostage_index, AC, SL, etc. computed only)")


if __name__ == "__main__":
    import inspect
    print("--- test_architecture_invariants ---")
    for _name, obj in inspect.getmembers(sys.modules[__name__], predicate=inspect.isfunction):
        if _name.startswith("test_"):
            obj()
            print(f"  {_name} passed")
    print("All tests passed.")
