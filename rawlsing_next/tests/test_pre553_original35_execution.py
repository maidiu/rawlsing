"""D original35 manifest selection and bounded execution bridge tests."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from rawlsing_next.pre553_original35_execution import (
    Original35ExecutionError, execute_source, load_runtime_binding,
)
from rawlsing_next.pre553_original35_operations import build_original35_operation_plan
from rawlsing_next.source_configuration.library import SourceConfigLibrary

INDEX = "source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json"


def _binding():
    try:
        return load_runtime_binding()
    except Original35ExecutionError:
        pytest.skip("local source runtime binding unavailable")


def test_all35_manifest_selection_and_operation_accounting():
    binding = _binding()
    root = binding["USER_ORIGINAL35_DATA_ROOT"]
    library = SourceConfigLibrary(index_path=INDEX, source_root=root)
    docs = [library.load_original(sid).document for sid in library.source_ids()]
    plan = build_original35_operation_plan(
        docs, source_presence={sid: True for sid in library.source_ids()},
        require_all35=True, expected_item_count=18276,
        expected_physical_slot_count=18413)
    assert len(plan.rows) == 35
    assert plan.item_count == 18276
    assert plan.physical_slot_count == 18413
    assert plan.no_drop_ok is True
    assert set(plan.counts) == {
        "EXECUTABLE_RAW", "HELD", "ABSTAIN", "INAPPLICABLE",
        "DEFERRED", "NOT_REQUESTED"}
    assert sum(plan.counts.values()) == len(plan.operations) == 18467
    assert plan.counts == {
        "ABSTAIN": 0, "DEFERRED": 51, "EXECUTABLE_RAW": 5630,
        "HELD": 4655, "INAPPLICABLE": 8131, "NOT_REQUESTED": 0}
    for sid in library.source_ids():
        selected = library.select(sid, source_root=root)
        assert selected["source_resolution"]["status"] == "RESOLVED_UNDER_EFFECTIVE_ROOT"
        assert selected["source_read_performed"] is False


def test_manifest_only_source_result_and_typed_path_resolution():
    binding = _binding()
    root = binding["USER_ORIGINAL35_DATA_ROOT"]
    library = SourceConfigLibrary(index_path=INDEX, source_root=root)
    result = execute_source(
        "SRC31", library=library, source_root=root, allow_decode=False)
    assert result.status == "MANIFEST_ONLY"
    assert result.source_id == "SRC31"
    assert result.row_count == 0
    assert result.physical_slots == 68
    assert result.response_slots == 64
    assert result.operation_counts["EXECUTABLE_RAW"] > 0
    assert result.reasons == ("MANIFEST_ONLY_NOT_DECODED",)
    assert result.material()["native"] is False
