from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy import compile_v551_relation_evidence_atoms as v551_compiler
from data.ddm_build_copy import ddm_v550_bridge as bridge
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity


def _row(**overrides):
    value = {
        "source": "GSS",
        "source_family": "GSS",
        "wave": "2010",
        "canonical_wave": "2010",
        "country_code": "US",
        "question_id": "q1",
        "var_code": "v1",
        "response_value_raw": "1",
        "response_value_normalized": "1",
        "response_label": "yes",
        "normalized_response_label": "yes",
        "response_family": "yes_no",
        "response_option_map_matched": True,
        "n_unweighted": 10,
        "n_respondents": 20,
    }
    value.update(overrides)
    return value


def _identity_authority(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bridge, "apply_question_relation_authority", lambda row: row)


def test_governed_streaming_bridge_publishes_uid_pair_for_v551(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    pytest.importorskip("pyarrow")
    _identity_authority(monkeypatch)
    expected = resolve_source_wave_identity("GSS", "2010", require_closed_35=True)
    bridge_path = tmp_path / "v551_bridge_index.parquet"

    result = bridge.write_v551_bridge_index_for_shard(
        {"answer_distribution": pd.DataFrame([_row()])},
        run_id="runtime-canary",
        shard_id="GSS__2010",
        bridge_path=bridge_path,
        directionality_overlay_lookup={},
        survey_family="GSS",
        canonical_wave="2010",
    )

    assert result["bridge_rows"] == 1
    published = pd.read_parquet(bridge_path)
    assert "source_family_uid" in published.columns
    assert "wave_uid" in published.columns
    assert published["source_family_uid"].tolist() == [expected.source_family_uid]
    assert published["wave_uid"].tolist() == [expected.wave_uid]
    assert "source_family_uid" in bridge.V551_BRIDGE_INDEX_SCHEMA["required_columns"]
    assert "wave_uid" in bridge.V551_BRIDGE_INDEX_SCHEMA["required_columns"]

    producer_scope = v551_compiler._producer_scope_identity(published)
    assert producer_scope["source_family_uid"] == expected.source_family_uid
    assert producer_scope["wave_uid"] == expected.wave_uid


def test_uid_transport_is_additive_to_frozen_v550_row_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    _identity_authority(monkeypatch)
    expected = resolve_source_wave_identity("GSS", "2010", require_closed_35=True)
    row = _row()

    legacy = bridge._base_bridge_row(
        row,
        run_id="runtime-canary",
        shard_id="GSS__2010",
        empirical_object_type="answer_distribution",
        source_table="answer_distribution",
    )
    governed = bridge._base_bridge_row(
        row,
        run_id="runtime-canary",
        shard_id="GSS__2010",
        empirical_object_type="answer_distribution",
        source_table="answer_distribution",
        source_family_uid=expected.source_family_uid,
        wave_uid=expected.wave_uid,
    )

    assert legacy["source_family_uid"] == ""
    assert legacy["wave_uid"] == ""
    assert governed["source_family_uid"] == expected.source_family_uid
    assert governed["wave_uid"] == expected.wave_uid
    assert governed["source_row_hash"] == legacy["source_row_hash"]
    assert governed["empirical_object_id"] == legacy["empirical_object_id"]


def test_declared_bridge_uid_contradiction_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    _identity_authority(monkeypatch)
    wrong = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    row = _row(source_family_uid=wrong.source_family_uid, wave_uid=wrong.wave_uid)

    with pytest.raises(RuntimeError, match="BLOCKED_V550_BRIDGE_DECLARED_UID_SCOPE_CONTRADICTION"):
        bridge._base_bridge_row(
            row,
            run_id="runtime-canary",
            shard_id="GSS__2010",
            empirical_object_type="answer_distribution",
            source_table="answer_distribution",
        )
