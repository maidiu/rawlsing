"""R116 independent native world+empirical consumer probes (TEST_ONLY)."""
from __future__ import annotations

from rawlsing_next.pre553_universal_world_binding import (
    ProgressiveWorldRequest, progressive_world_view,
)
from rawlsing_next.pre553_world_conditioned_progressive_service import (
    _pinned_nonparent_consume,
)
from rawlsing_next.tests.test_universal_world_binding import (
    _progressive_fixture,
)


def _view(handle, key="T0", currentness="HISTORICAL"):
    return progressive_world_view(ProgressiveWorldRequest(
        handle, key, "GENERIC_POSITIONED_SUBJECT", currentness,
    ))


def test_R116_native_consumer_reads_world_and_empirical_per_prefix():
    view = _view(_progressive_fixture())
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    native = view.n10w["world_conditioned_prefixes"]
    assert len(native) == len(view.n10e_steps) == 2
    assert view.n10w["world_conditioned_state"] == (
        "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    )
    for result, step, positioned in zip(
            native, view.n10e_steps, view.n10w["positioned_consumptions"]):
        material = result["native_material"]
        assert material["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
        assert material["route_probability"] is None
        assert material["route_probability_reason"] == (
            "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL"
        )
        assert result["n10e_consumer_hash"] == step["content_hash"]
        assert positioned["consumer_result_hash"] == step["content_hash"]
        assert result["world_snapshot_hash"] == view.world_snapshot_hash
        assert material["structural_routes"]
        assert material["source_balance_reads"]
        assert material["values_read"]
        channels = {entry["channel"] for entry in material["values_read"]}
        assert channels == {"structural", "empirical"}
        supports = material["source_balance_reads"]
        assert supports[0]["denominator"] == step["denominator"]
        assert supports[0]["all_alternatives"] == step["cells"]


def test_R116_value_and_world_mutations_change_same_native_assertion():
    base = _view(_progressive_fixture())
    value = _view(_progressive_fixture(conds=(("X", 0), ("O", "AB"))))
    world = _view(_progressive_fixture(), "T1", "AS_OF")
    base_native = base.n10w["world_conditioned_prefixes"]
    value_native = value.n10w["world_conditioned_prefixes"]
    world_native = world.n10w["world_conditioned_prefixes"]
    assert base_native[0]["native_material"]["source_balance_reads"] != (
        value_native[0]["native_material"]["source_balance_reads"]
    )
    assert base_native[0]["native_material"]["structural_routes"] != (
        world_native[0]["native_material"]["structural_routes"]
    )
    assert base_native[0]["native_material"]["source_balance_reads"] == (
        world_native[0]["native_material"]["source_balance_reads"]
    )
    assert base.n10w["positioned_consumptions"][0]["consumer_result_hash"] != (
        value.n10w["positioned_consumptions"][0]["consumer_result_hash"]
    )


def test_R116_unlike_target_and_revocation_restore():
    unlike = _view(_progressive_fixture(
        target="X", conds=(("Y", 1), ("O", "BA")),
    ))
    assert unlike.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert unlike.target_ref.kind == "QUESTION_NATIVE"
    assert unlike.n10w["world_conditioned_prefixes"]
    empirical = _view(_progressive_fixture(revoked_scope="empirical"),
                      "T1", "AS_OF")
    assert empirical.state == "PROGRESSIVE_WORLD_UNAVAILABLE"
    assert empirical.n10w["world_conditioned_prefixes"][0]["native_material"][
        "state"
    ] == "EMPIRICAL_REVOKED_OR_UNAVAILABLE"
    world = _view(_progressive_fixture(revoked_scope="training_access"),
                  "T1", "AS_OF")
    assert world.state == "PROGRESSIVE_WORLD_UNAVAILABLE"
    assert str(
        world.n10w["world_conditioned_prefixes"][0]["native_material"][
            "structural_routes"
        ]["training"]["state"]
    ).startswith("UNAVAILABLE")
    restored = _view(_progressive_fixture(), "T1", "AS_OF")
    assert restored.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert restored.n10w["world_conditioned_state"] == (
        "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    )


def test_R116_pinned_nonparent_owner_is_imported():
    consume = _pinned_nonparent_consume()
    assert consume.__module__ == "product.nonparent"
    assert callable(consume)


def test_R116_wrong_prefix_model_must_refuse():
    from dataclasses import replace
    from rawlsing_next.tests.test_universal_world_binding import (
        _progressive_fixture_parts,
    )
    from rawlsing_next.tests import c1_at08_at13_fixture as fx
    from rawlsing_next.pre553_universal_world_binding import (
        configure_progressive_world_context,
    )
    target, conditions, prefixes, world = _progressive_fixture_parts()
    other = fx.make_model_rule(
        prefixes[0].model_rule.source_universe_refs[0], "r116-other-model",
    )
    mixed = (prefixes[0], replace(prefixes[1], model_rule=other))
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=mixed,
        world_empirical=world,
    )
    view = _view(handle)
    assert view.state in {"REFUSED", "PROGRESSIVE_WORLD_UNAVAILABLE"}, (
        "mixed-prefix model identity was accepted while a selected view was served"
    )
