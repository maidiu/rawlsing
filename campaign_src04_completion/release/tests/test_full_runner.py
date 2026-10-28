"""Focused source-free checks for the full SRC04 completion lane."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from campaign_src04_completion.release import full_runner as runner
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import load_source_config


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
