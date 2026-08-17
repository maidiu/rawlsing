#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import types

import pandas as pd
import pytest

if importlib.util.find_spec("psycopg2") is None:
    psycopg2_stub = types.ModuleType("psycopg2")
    psycopg2_stub.connect = lambda *_args, **_kwargs: (_ for _ in ()).throw(
        RuntimeError("psycopg2 unavailable in unit-test environment")
    )
    sys.modules["psycopg2"] = psycopg2_stub

from data.ddm_build_copy import build_all_survey_overlays as batch


def test_update_index_rejects_later_row_with_contradictory_label_despite_same_uids(
    tmp_path, monkeypatch
):
    authority_dir = tmp_path / "directionality_authority"
    authority_dir.mkdir()
    monkeypatch.setattr(batch, "AUTH_DIR", authority_dir)

    pd.DataFrame(
        [
            {
                "source": "Arab Barometer",
                "wave": "I",
                "canonical_wave": "I",
                "canonical_display_source": "Arab Barometer",
                "canonical_display_wave": "I",
                "source_family_uid": "sf_arab_barometer_v1",
                "wave_uid": "wv_arab_barometer_i_v1",
                "directionality_authority_status": "HEURISTIC_REVIEW_ONLY",
                "directional_certification_status": "NOT_CERTIFIED",
            },
            {
                "source": "Asian Barometer",
                "wave": "I",
                "canonical_wave": "I",
                "canonical_display_source": "Arab Barometer",
                "canonical_display_wave": "I",
                "source_family_uid": "sf_arab_barometer_v1",
                "wave_uid": "wv_arab_barometer_i_v1",
                "directionality_authority_status": "HEURISTIC_REVIEW_ONLY",
                "directional_certification_status": "NOT_CERTIFIED",
            },
        ]
    ).to_csv(
        authority_dir / "arab_barometer_I_directionality_authority.csv",
        index=False,
    )

    with pytest.raises(
        RuntimeError,
        match="REVIEW_OVERLAY_INDEX_IDENTITY_CONTRADICTION",
    ):
        batch.update_index()

    assert not (authority_dir / "directionality_authority_index.csv").exists()
