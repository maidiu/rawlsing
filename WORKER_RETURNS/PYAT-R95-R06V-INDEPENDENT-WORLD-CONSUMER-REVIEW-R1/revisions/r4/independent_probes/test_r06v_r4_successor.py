"""R95-R06V R4 independent pinned-context successor controls (TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace
import sys
import types

from rawlsing_next.pre553_universal_world_binding import (
    select_r05_world_view,
)
from rawlsing_next.tests.test_universal_world_binding import (
    _actual_execution_for, _build_r05_learned_inprocess,
    _persistent_p41_runtime, _r05_request, _run_r05_p41,
)


def _positive(data):
    return select_r05_world_view(_r05_request(
        data, actual_execution=_actual_execution_for(
            data, _persistent_p41_runtime())),
    )


def test_R4_missing_and_forged_handle_refuse_restore():
    _run_r05_p41(_persistent_p41_runtime())
    data = _build_r05_learned_inprocess()
    execution = _actual_execution_for(data, _persistent_p41_runtime())
    missing = select_r05_world_view(_r05_request(
        data, actual_execution=execution, execution_handle=None,
    ))
    assert missing.state == "REFUSED"
    assert missing.reason_code == "TRUSTED_EXECUTION_HANDLE_REQUIRED"
    forged = select_r05_world_view(_r05_request(
        data, actual_execution=execution, execution_handle="r06ctx-forged",
    ))
    assert forged.state == "REFUSED"
    assert forged.reason_code == "TRUSTED_EXECUTION_HANDLE_INVALID"
    restored = _positive(data)
    assert restored.state == "R05_WORLD_SELECTED_VIEW"


def test_R4_same_context_step_and_learned_substitution_refuse_restore():
    _run_r05_p41(_persistent_p41_runtime())
    data = _build_r05_learned_inprocess()
    execution = _actual_execution_for(data, _persistent_p41_runtime())
    base = _positive(data)
    bad_step = replace(execution, step=dict(execution.step, content_hash="0" * 64))
    step_view = select_r05_world_view(_r05_request(
        data, actual_execution=bad_step,
        execution_handle=execution.execution_handle,
    ))
    assert step_view.state == "REFUSED"
    assert step_view.reason_code in {
        "R05_ACTUAL_STEP_ORIGINAL_MISMATCH", "R05_ACTUAL_STEP_CONSUMER_MISMATCH",
    }
    from rawlsing_next.pre553_empirical_objects import ExactRef
    bad_learned = replace(
        execution.learned_consumer,
        learned_receipt_ref=ExactRef(
            "LearnedWorldCompositionReceipt",
            "urn:test:r06v-r4:forged-learned", "b" * 64,
        ),
    )
    learned_view = select_r05_world_view(_r05_request(
        data, actual_execution=replace(execution, learned_consumer=bad_learned),
        execution_handle=execution.execution_handle,
    ))
    assert learned_view.state == "REFUSED"
    assert learned_view.reason_code == "R05_LEARNED_ORIGINAL_MISMATCH"
    restored = _positive(data)
    assert restored.view_hash == base.view_hash


def test_R4_preloaded_fake_owner_modules_are_purged():
    _run_r05_p41(_persistent_p41_runtime())
    data = _build_r05_learned_inprocess()
    base = _positive(data)

    fake_bootstrap = types.ModuleType("bootstrap")
    fake_bootstrap.install = lambda: None
    fake_p41 = types.ModuleType("p41_service")
    class FakeP41Service:
        def progressive(self, **kwargs):
            raise AssertionError("fake p41_service used")
    fake_p41.P41Service = FakeP41Service
    fake_product = types.ModuleType("product")
    fake_world = types.ModuleType("product.world")
    class FakeCatalog:
        def __init__(self, *args, **kwargs):
            raise AssertionError("fake product used")
    fake_world.SelectedWorldCatalog = FakeCatalog
    replacement = {
        "bootstrap": fake_bootstrap,
        "p41_service": fake_p41,
        "product": fake_product,
        "product.world": fake_world,
    }
    saved = {name: sys.modules.get(name) for name in replacement}
    sys.modules.update(replacement)
    try:
        view = _positive(data)
    finally:
        for name, old in saved.items():
            if old is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old
    assert view.state == "R05_WORLD_SELECTED_VIEW"
    assert view.view_hash == base.view_hash
