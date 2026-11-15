"""R112 world-conditioned progressive successor qualification (TEST_ONLY)."""
from __future__ import annotations

from rawlsing_next.pre553_universal_world_binding import (
    ProgressiveWorldRequest, progressive_world_view,
)
from rawlsing_next.tests.test_l01_reviewed_progressive_world import _progressive_fixture


def _view(handle, key="T0", currentness="HISTORICAL"):
    return progressive_world_view(ProgressiveWorldRequest(
        handle, key, "GENERIC_POSITIONED_SUBJECT", currentness,
    ))


def test_native_nonparent_consumer_runs_per_prefix_with_both_inputs():
    view = _view(_progressive_fixture())
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    native = view.n10w["world_conditioned_prefixes"]
    assert len(native) == 2
    step_hashes = {step["content_hash"] for step in view.n10e_steps}
    for result in native:
        material = result["native_material"]
        assert material["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
        assert material["route_probability"] is None
        assert material["route_probability_reason"] == (
            "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL"
        )
        assert result["n10e_consumer_hash"] in step_hashes
        assert material["structural_routes"]
        assert material["source_balance_reads"]
        assert result["world_snapshot_hash"] == view.world_snapshot_hash
    assert {
        key: value["state"]
        for key, value in native[0]["native_material"]["structural_routes"].items()
    } == dict(view.world_routes)


def test_world_rule_and_prefix_values_change_same_native_assertion():
    base = _view(_progressive_fixture())
    different_prefix = _view(_progressive_fixture(conds=(("X", 0), ("O", "AB"))))
    different_world = _view(_progressive_fixture(), "T1", "AS_OF")
    base_native = base.n10w["world_conditioned_prefixes"]
    prefix_native = different_prefix.n10w["world_conditioned_prefixes"]
    world_native = different_world.n10w["world_conditioned_prefixes"]
    assert base_native[0]["native_material"]["source_balance_reads"][0][
        "source_balance_count"
    ] != prefix_native[0]["native_material"]["source_balance_reads"][0][
        "source_balance_count"
    ]
    assert base_native[0]["native_material"]["structural_routes"] != (
        world_native[0]["native_material"]["structural_routes"]
    )
    assert base_native[0]["native_material"]["source_balance_reads"] == (
        world_native[0]["native_material"]["source_balance_reads"]
    )
    assert base.n10w["positioned_consumptions"][0]["consumer_result_hash"] != (
        different_prefix.n10w["positioned_consumptions"][0]["consumer_result_hash"]
    )


def test_revoked_empirical_and_world_dependencies_are_nonproductive_and_restore():
    empirical = _view(_progressive_fixture(revoked_scope="empirical"),
                      "T1", "AS_OF")
    assert empirical.state == "PROGRESSIVE_WORLD_UNAVAILABLE"
    assert empirical.n10w["world_conditioned_state"] == (
        "TYPED_PARTIAL_OPTIONS_OR_SOURCE_SUPPORT"
    )
    assert empirical.n10w["world_conditioned_prefixes"][0]["native_material"][
        "state"
    ] == "EMPIRICAL_REVOKED_OR_UNAVAILABLE"
    assert empirical.n9_world["empirical"]["state"] == "REVOKED"
    world = _view(_progressive_fixture(revoked_scope="training_access"),
                  "T1", "AS_OF")
    assert world.state == "PROGRESSIVE_WORLD_UNAVAILABLE"
    assert world.n10w["world_conditioned_state"] != (
        "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    )
    assert world.n10w["world_conditioned_prefixes"][0]["native_material"][
        "structural_routes"
    ]["training"]["state"].startswith("UNAVAILABLE")
    restored = _view(_progressive_fixture(), "T1", "AS_OF")
    assert restored.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert restored.n10w["world_conditioned_state"] == (
        "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    )
