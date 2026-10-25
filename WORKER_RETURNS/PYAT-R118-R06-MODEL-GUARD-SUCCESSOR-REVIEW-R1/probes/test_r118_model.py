"""R118 focused model-identity successor probes (TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace

from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_universal_world_binding import (
    _progressive_fixture, _progressive_fixture_parts,
)
from rawlsing_next.pre553_universal_world_binding import (
    ProgressiveWorldRequest, configure_progressive_world_context,
    progressive_world_view,
)


def _view(handle):
    return progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL",
    ))


def test_R118_mixed_model_refuses_under_public_path():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    other = fx.make_model_rule(
        prefixes[0].model_rule.source_universe_refs[0], "r118-other",
    )
    mixed = (prefixes[0], replace(prefixes[1], model_rule=other))
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=mixed,
        world_empirical=world,
    )
    view = _view(handle)
    assert view.state == "REFUSED"
    assert view.reason_code == "PROGRESSIVE_WORLD_SOURCE_RELEASE_RISK_MISMATCH"


def test_R118_consistent_alternate_model_is_productive():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    other = fx.make_model_rule(
        prefixes[0].model_rule.source_universe_refs[0], "r118-alternate",
    )
    consistent = tuple(replace(prefix, model_rule=other) for prefix in prefixes)
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=consistent,
        world_empirical=world,
    )
    view = _view(handle)
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert {step["model_rule_hash"] for step in view.n10e_steps} == {
        other.rule_hash,
    }
    assert view.n10w["world_conditioned_state"] == (
        "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    )
    assert all(
        result["native_material"]["state"] == (
            "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
        )
        for result in view.n10w["world_conditioned_prefixes"]
    )


def test_R118_shared_model_preserves_native_world_and_empirical_positive():
    view = _view(_progressive_fixture())
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert {step["model_rule_hash"] for step in view.n10e_steps} == {
        "fa549221d39fbda539703bbaac6b7b52013fec44a798d1410a05a260d780e594",
    }
    native = view.n10w["world_conditioned_prefixes"]
    assert len(native) == 2
    assert all(
        result["native_material"]["state"] == (
            "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
        )
        for result in native
    )
    assert all(
        result["native_material"]["route_probability"] is None
        for result in native
    )
    assert all(
        result["native_material"]["source_balance_reads"] for result in native
    )
