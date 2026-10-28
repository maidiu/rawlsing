"""Focused source-free checks for the full SRC04 completion lane."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from campaign_src04_completion.release import full_runner as runner
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import load_source_config, validate_source_config
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from campaign_src04_completion.bindings.numeric_domain_binding import apply_observed_domain, TARGET_SLOTS


def test_scope_accounts_for_all_181_slots_and_163_complete_fields():
    scope = runner._scope_from_accepted_selection()
    assert scope["configured_response_slots"] == 178
    assert scope["configured_coordinate_slots"] == 3
    assert len(scope["accepted_complete_response_slots"]) == 163
    assert len(scope["accepted_held_response_slots"]) == 15
    assert scope["accepted_coordinate_slots"] == [1, 2]
    assert scope["accepted_held_coordinate_slots"] == [158]
    assert scope["selected_response_positions"] == 1_195_931
    assert scope["physical_slots"] == 181
    assert scope["source_read_performed"] is False


def test_absent_full_grant_refuses_before_source_io(tmp_path):
    with pytest.raises(runner.FullRunRefusal) as exc:
        runner.load_full_grant(tmp_path / "missing-grant.json", "0" * 64)
    assert exc.value.code == "FULL_SOURCE_GRANT_ABSENT"


def test_first_slice_foreign_source_and_foreign_purpose_are_refused():
    first = json.loads(runner.A_USER_GRANT_PATH.read_text(encoding="utf-8"))
    with pytest.raises(runner.FullRunRefusal) as exc:
        runner.validate_grant_document(first, "0" * 64)
    assert exc.value.code in {"GRANT_PURPOSE_MISMATCH", "GRANT_SCHEMA_MISMATCH"}
    foreign = dict(first, source_id="SRC17", schema=runner.FULL_GRANT_SCHEMA)
    with pytest.raises(runner.FullRunRefusal) as exc:
        runner.validate_grant_document(foreign, "0" * 64)
    assert exc.value.code == "GRANT_SOURCE_MISMATCH"
    purpose = dict(first, purpose="FOREIGN_PURPOSE", schema=runner.FULL_GRANT_SCHEMA)
    with pytest.raises(runner.FullRunRefusal) as exc:
        runner.validate_grant_document(purpose, "0" * 64)
    assert exc.value.code == "GRANT_PURPOSE_MISMATCH"


def test_prepare_does_not_touch_source_path(monkeypatch, tmp_path):
    grant = json.loads(runner.A_USER_GRANT_PATH.read_text(encoding="utf-8"))
    source_path = str(grant["source_path"])
    opened: list[str] = []
    original_open = Path.open

    def guarded_open(self, *args, **kwargs):
        if str(self) == source_path:
            opened.append(str(self))
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    assert runner.prepare_no_source_blocker() == 0
    assert opened == []
    scope = json.loads(runner.SCOPE_PATH.read_text(encoding="utf-8"))
    assert scope["source_read_performed"] is False
    assert scope["native_release_constructed"] is False


def test_committed_metadata_files_are_exact():
    assert hashlib.sha256(runner.PROGRAM_PATH.read_bytes()).hexdigest() == runner.EXPECTED_PROGRAM_SHA256
    assert hashlib.sha256(runner.CONFIG_PATH.read_bytes()).hexdigest() == runner.EXPECTED_CONFIG_FILE_SHA256
    assert json.loads(runner.A_SELECTION_PATH.read_text(encoding="utf-8"))["complete_response_slots"]

def test_full_163_fixture_construction_path_builds_release():
    """Source-free fixture smoke for the full 163+2 factory path; not original proof."""
    cfg = load_source_config(runner.ROOT / "source_pre553_validation/SRC04/fixture.config.json")
    stream = load_fixture_stream(runner.ROOT / "source_pre553_validation/SRC04/fixture.json")
    selection = {
        "selected_response_slots": runner._scope_from_accepted_selection()["accepted_complete_response_slots"],
        "selected_coordinate_slots": [1, 2],
    }
    slice_config, withheld = runner._slice_config(cfg, selection)
    release = build_validated_c11_release_from_config(slice_config, stream=stream)
    assert len(slice_config.document["response_slots"]) == 163
    assert len(slice_config.document["coordinate_slots"]) == 2
    assert withheld > 0
    assert release.source_artifact_ref.content_hash == stream.source_sha256
    assert release.release_ref.kind == "C11LogicalRelease"
    assert len(release.public_objects) > 0


def test_fixed_b_builder_is_wired_after_admission_before_selection(monkeypatch):
    cfg = load_source_config(runner.B_CONFIG_PATH)
    calls = []

    def fake_builder(config, transport, **kwargs):
        calls.append("builder")
        assert transport.source_sha256 == runner.EXPECTED_SOURCE_SHA256
        assert kwargs["expected_config_canonical_sha256"] == runner.B_CONFIG_CANONICAL_SHA256
        return {
            "config": config.document,
            "base_config_canonical_sha256": runner.B_CONFIG_CANONICAL_SHA256,
            "runtime_config_canonical_sha256": runner.B_CONFIG_CANONICAL_SHA256,
            "added_rule_counts": {"q715withoutmorocco": 2, "q716withoutmorocco": 2},
            "observed_missing_states": {},
        }

    def fake_runtime(config, transport):
        calls.append("runtime")
        return config

    def fake_selection(config, transport):
        calls.append("selection")
        return {"selected_response_slots": [], "selected_coordinate_slots": [],
                "selected_response_positions": 0, "all_181_physical_slots_accounted": True}

    class Admitted:
        source_sha256 = runner.EXPECTED_SOURCE_SHA256
        row_count = runner.EXPECTED_SOURCE_ROWS

    monkeypatch.setattr(runner, "build_numeric_domain_runtime_config", fake_builder)
    monkeypatch.setattr(runner, "_runtime_config", fake_runtime)
    monkeypatch.setattr(runner, "_scan_selection", fake_selection)
    runtime, selection, join = runner._join_and_select(cfg, Admitted(), repaired=True)
    assert calls == ["builder", "runtime", "selection"]
    assert join["builder_called_before_selection"] is True
    assert join["selection_after_binding"] is True


def test_fixed_b_observed_domain_covers_both_income_fields_on_nonrespondent_cells():
    """Synthetic nonrespondent cells exercise the fixed B helper only; no original data."""
    cfg = load_source_config(runner.B_CONFIG_PATH)
    slots = {s["slot"]["name"]: s["slot"] for s in cfg.document["response_slots"]}
    cells = [
        PhysicalCell(1, slots["q715withoutmorocco"]["ordinal"], "q715withoutmorocco", 1234.5, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(1, slots["q716withoutmorocco"]["ordinal"], "q716withoutmorocco", 2000.25, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, slots["q715withoutmorocco"]["ordinal"], "q715withoutmorocco", 0.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, slots["q716withoutmorocco"]["ordinal"], "q716withoutmorocco", 1500.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
    ]
    applied = apply_observed_domain(cfg, iter(cells))
    assert applied["added_rule_counts"].get("q715withoutmorocco", 0) >= 2
    assert applied["added_rule_counts"].get("q716withoutmorocco", 0) >= 2
    validate_source_config(applied["config"])


def test_pinned_b_config_and_builder_are_exact():
    assert hashlib.sha256(runner.B_CONFIG_PATH.read_bytes()).hexdigest() == runner.B_CONFIG_FILE_SHA256
    cfg = load_source_config(runner.B_CONFIG_PATH)
    assert len(cfg.document["response_slots"]) == 178
    assert len(cfg.document["coordinate_slots"]) == 3
    assert runner.B_PINNED_COMMIT
    assert runner.B_BUILDER.endswith("build_numeric_domain_runtime_config")


def test_native_pickle_stream_roundtrip_for_local_product(tmp_path):
    cfg = load_source_config(runner.ROOT / "source_pre553_validation/SRC04/fixture.config.json")
    stream = load_fixture_stream(runner.ROOT / "source_pre553_validation/SRC04/fixture.json")
    selection = {
        "selected_response_slots": runner._scope_from_accepted_selection()["accepted_complete_response_slots"][:3],
        "selected_coordinate_slots": [1, 2],
    }
    slice_config, _ = runner._slice_config(cfg, selection)
    release = build_validated_c11_release_from_config(slice_config, stream=stream)
    path = tmp_path / "objects.pkl"
    count, size, digest = runner._write_pickle_stream(path, release.public_objects)
    assert count == len(release.public_objects)
    assert size == path.stat().st_size
    assert digest == hashlib.sha256(path.read_bytes()).hexdigest()
    assert sum(1 for _ in runner._iter_pickle_stream(path)) == count


def test_numeric_binding_targets_actual_income_deciles_without_labels():
    cfg = load_source_config(runner.B_CONFIG_PATH)
    slots = {s["slot"]["name"]: s["slot"] for s in cfg.document["response_slots"]}
    cells = [
        PhysicalCell(1, slots["q715incomedeciles"]["ordinal"], "q715incomedeciles", 1.5, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(1, slots["q716incomedeciles"]["ordinal"], "q716incomedeciles", 5.5, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, slots["q715incomedeciles"]["ordinal"], "q715incomedeciles", 8.5, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, slots["q716incomedeciles"]["ordinal"], "q716incomedeciles", 7.5, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
    ]
    applied = apply_observed_domain(cfg, iter(cells), target_slots=runner.NUMERIC_TARGET_SLOTS)
    assert applied["added_rule_counts"].get("q715incomedeciles", 0) >= 2
    assert applied["added_rule_counts"].get("q716incomedeciles", 0) >= 2
    for name in ("q715incomedeciles", "q716incomedeciles"):
        slot = next(s for s in applied["config"]["response_slots"] if s["slot"]["name"] == name)
        for value in slot["values"]:
            if value["raw_value"] in (1.5, 8.5, 5.5, 7.5):
                assert value["canonical_value"] is None
