"""R111 successor controls for the three R110 repairs (TEST_ONLY)."""
from __future__ import annotations

from rawlsing_next.pre553_universal_world_binding import (
    ProgressiveWorldRequest, configure_progressive_world_context,
    progressive_world_view,
)
from rawlsing_next.tests.test_universal_world_binding import (
    _progressive_fixture, _progressive_fixture_parts,
)


def _view(handle):
    return progressive_world_view(ProgressiveWorldRequest(
        handle, "T0", "GENERIC_POSITIONED_SUBJECT", "HISTORICAL",
    ))


def test_R111_world_rows_hash_mismatch_must_refuse():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    bad = dict(world)
    bad["rows_hash"] = "f" * 64
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=prefixes,
        world_empirical=bad,
    )
    view = _view(handle)
    assert view.state in {"REFUSED", "PROGRESSIVE_WORLD_UNAVAILABLE"}, (
        "world rows_hash mismatch was accepted while a selected view was served"
    )


def test_R111_world_repository_omission_must_refuse():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    bad = dict(world)
    bad["source"] = {
        key: value for key, value in world["source"].items() if key != "repo"
    }
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=prefixes,
        world_empirical=bad,
    )
    view = _view(handle)
    assert view.state in {"REFUSED", "PROGRESSIVE_WORLD_UNAVAILABLE"}, (
        "world source repository omission bypassed repository identity agreement"
    )


def test_R111_repairs_two_and_three_and_prior_positives_remain():
    base = _view(_progressive_fixture())
    assert base.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    step_hashes = {step["content_hash"] for step in base.n10e_steps}
    positioned = base.n10w["positioned_consumptions"]
    assert len(positioned) == len(base.n10e_steps)
    assert set(entry["consumer_result_hash"] for entry in positioned) == step_hashes
    assert all(entry["source"] == "LIVE_TRACE" for entry in positioned)
    changed = _view(_progressive_fixture(conds=(("X", 0), ("O", "AB"))))
    assert changed.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert changed.n10e_steps[0]["cells"] != base.n10e_steps[0]["cells"]
    revoked = progressive_world_view(ProgressiveWorldRequest(
        _progressive_fixture(revoked_scope="empirical"),
        "T1", "GENERIC_POSITIONED_SUBJECT", "AS_OF",
    ))
    assert revoked.state == "PROGRESSIVE_WORLD_UNAVAILABLE"
    assert revoked.reason_code == "WORLD_EMPIRICAL_REVOKED_OR_UNAVAILABLE"
    restored = _view(_progressive_fixture())
    assert restored.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"


def test_R111_mixed_prefix_repository_must_refuse():
    from copy import copy
    from dataclasses import replace
    target, conditions, prefixes, world = _progressive_fixture_parts()
    mixed = (prefixes[0], replace(
        prefixes[1], repository=copy(prefixes[1].repository),
    ))
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=mixed,
        world_empirical=world,
    )
    view = _view(handle)
    assert view.state in {"REFUSED", "PROGRESSIVE_WORLD_UNAVAILABLE"}, (
        "mixed-prefix repository identity was accepted while a selected view was served"
    )


def test_R111_actual_evaluator_value_use_is_required():
    from types import SimpleNamespace
    import rawlsing_next.source_backed_positioned_subject_possibility as sbp
    original = sbp.evaluate_positioned_subject_possibility
    sbp.evaluate_positioned_subject_possibility = (
        lambda **kwargs: SimpleNamespace(result_hash="0" * 64)
    )
    try:
        view = _view(_progressive_fixture())
    finally:
        sbp.evaluate_positioned_subject_possibility = original
    assert view.state == "REFUSED"
    assert view.reason_code == "PROGRESSIVE_ACTUAL_CONSUMER_MISMATCH"
