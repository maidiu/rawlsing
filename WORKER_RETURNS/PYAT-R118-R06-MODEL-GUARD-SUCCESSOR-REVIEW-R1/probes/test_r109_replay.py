"""R109 independent progressive-world probes (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_universal_world_binding import (
    ProgressiveWorldRequest, configure_progressive_world_context,
    progressive_world_view,
)
from rawlsing_next.tests.test_universal_world_binding import (
    _progressive_fixture, _progressive_fixture_parts,
)


def _view(handle, key="T0", currentness="HISTORICAL"):
    return progressive_world_view(ProgressiveWorldRequest(
        handle, key, "GENERIC_POSITIONED_SUBJECT", currentness,
    ))


def test_R109_actual_positive_and_condition_value_mutation():
    base = _view(_progressive_fixture())
    changed = _view(_progressive_fixture(
        conds=(("X", 0), ("O", "AB")),
    ))
    assert base.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert changed.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert [s["denominator"] for s in base.n10e_steps] == [40, 30]
    assert [s["denominator"] for s in changed.n10e_steps] == [40, 20]
    assert base.n10e_steps[0]["cells"] != changed.n10e_steps[0]["cells"]
    assert base.n10e_steps[1]["cells"] != changed.n10e_steps[1]["cells"]
    assert base.n10w["progressive_update_identity"] != (
        changed.n10w["progressive_update_identity"]
    )
    assert base.world_routes != _view(
        _progressive_fixture(), "T1", "AS_OF"
    ).world_routes
    assert any(cell["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
               for cell in base.alternatives[1]["cells"])
    assert min(cell["raw_numerator_support"]
               for cell in base.alternatives[0]["cells"]) < max(
                   cell["raw_numerator_support"]
                   for cell in base.alternatives[0]["cells"])
    assert base.actor_state == "NOT_TOUCHED"


def test_R109_semantically_unlike_target_shape():
    view = _view(_progressive_fixture(
        target="X", conds=(("Y", 1), ("O", "BA")),
    ))
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert view.target_ref.kind == "QUESTION_NATIVE"
    assert view.prefix_count == 2
    assert len(view.n10e_steps) == 2
    assert len(view.n10w["progressive_update_identity"]) == 2
    assert view.world_routes is not None


def test_R109_foreign_world_source_release_must_refuse():
    target, conditions, prefixes, world = _progressive_fixture_parts()
    foreign = ExactRef("C11LogicalRelease", "REL-r109-foreign", "f" * 64)
    bad_world = dict(world)
    bad_world["release_ref"] = foreign
    bad_world["source"] = dict(world["source"])
    bad_world["source"]["release_ref"] = foreign
    handle = configure_progressive_world_context(
        target_ref=target, conditions=conditions, prefixes=prefixes,
        world_empirical=bad_world,
    )
    view = _view(handle)
    assert view.state in {"REFUSED", "PROGRESSIVE_WORLD_UNAVAILABLE"}, (
        "foreign world release was accepted without source/release refusal"
    )


def test_R109_empirical_revocation_must_not_serve_selected_view():
    handle = _progressive_fixture(revoked_scope="empirical")
    view = _view(handle, "T1", "AS_OF")
    assert view.state != "PROGRESSIVE_WORLD_SELECTED_VIEW" or (
        getattr(view, "n9_world", None) or {}
    ).get("empirical", {}).get("state") in {"REVOKED", "UNAVAILABLE"}, (
        "empirical permission revocation was ignored while a selected view was served"
    )


def test_R109_world_field_revocation_restore_and_actual_dependency():
    revoked = _view(_progressive_fixture(revoked_scope="training_access"),
                    "T1", "AS_OF")
    assert revoked.state == "PROGRESSIVE_WORLD_UNAVAILABLE"
    assert str(revoked.world_routes["training"]).startswith("UNAVAILABLE")
    restored = _view(_progressive_fixture(), "T1", "AS_OF")
    assert restored.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    assert restored.world_routes["training"] == "BLOCKED_BY_MODELED_RULE"


def test_R109_n10w_positioned_consumptions_bind_actual_n10e_hashes():
    view = _view(_progressive_fixture())
    assert view.state == "PROGRESSIVE_WORLD_SELECTED_VIEW"
    step_hashes = {step["content_hash"] for step in view.n10e_steps}
    positioned = view.n10w["positioned_consumptions"]
    assert len(positioned) == len(view.n10e_steps)
    observed = [entry.get("consumer_result_hash") for entry in positioned]
    assert all(isinstance(value, str) and value for value in observed), (
        "N10W positioned consumptions are cached placeholders, not actual N10E bindings"
    )
    assert set(observed) == step_hashes
