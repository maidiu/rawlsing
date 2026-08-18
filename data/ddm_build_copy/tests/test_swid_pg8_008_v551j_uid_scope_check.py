from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import (
    V551_V3_COMPILER_VERSION,
    V551_V3_REQUIRED_COLUMNS,
    V551_V3_SCHEMA_VERSION,
    _expected_v551_scope,
    _verify_frame_scope,
)
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity


ARTIFACT = "directional_candidate_adjudication"


def _scope(source: str = "Afrobarometer", wave: str = "R1", country: str = "LS") -> dict[str, object]:
    identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    return {
        "run_id": "run-1",
        "source": identity.canonical_display_source,
        "wave": identity.canonical_display_wave,
        "canonical_wave": identity.canonical_display_wave,
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "country_code": country,
        "country_codes": [country],
        "shard_id": "",
        "scope_kind": "country",
    }


def _frame(
    *,
    source: str = "Afrobarometer",
    wave: str = "ROUND1",
    country: str = "LS",
    run_id: str = "run-1",
) -> pd.DataFrame:
    identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    row = {column: "x" for column in V551_V3_REQUIRED_COLUMNS[ARTIFACT]}
    row.update(
        run_id=run_id,
        source=source,
        source_family=source,
        source_family_uid=identity.source_family_uid,
        canonical_wave=wave,
        wave_uid=identity.wave_uid,
        country_code=country,
        schema_version=V551_V3_SCHEMA_VERSION,
        compiler_version=V551_V3_COMPILER_VERSION,
    )
    return pd.DataFrame([row])


@pytest.mark.parametrize("alias", ["R1", "ROUND1", "Round 1"])
def test_v551j_accepts_afrobarometer_v551_wave_aliases_by_exact_uid(alias: str) -> None:
    _verify_frame_scope(_frame(wave=alias), ARTIFACT, _scope())


def test_v551j_accepts_latinobarometro_source_alias_by_exact_uid() -> None:
    scope = _scope("Latinobarómetro", "1995", "BR")
    _verify_frame_scope(
        _frame(source="Latinobarometro", wave="1995", country="BR"),
        ARTIFACT,
        scope,
    )


def test_v551j_rejects_redundant_label_contradiction_even_when_uid_pair_is_correct() -> None:
    scope = _scope()
    frame = _frame(wave="R1")
    frame.loc[:, "source"] = "EVS"
    frame.loc[:, "source_family"] = "EVS"
    with pytest.raises(BoundaryContractError, match="V551_ARTIFACT_UID_SCOPE_INVALID"):
        _verify_frame_scope(frame, ARTIFACT, scope)


def test_v551j_rejects_wrong_uid_pair_exactly() -> None:
    scope = _scope()
    frame = _frame(wave="R1")
    wrong = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    frame.loc[:, "source_family_uid"] = wrong.source_family_uid
    frame.loc[:, "wave_uid"] = wrong.wave_uid
    with pytest.raises(BoundaryContractError, match="V551_ARTIFACT_IDENTITY_MISMATCH"):
        _verify_frame_scope(frame, ARTIFACT, scope)


@pytest.mark.parametrize(
    ("field", "value"),
    [("run_id", "other-run"), ("country_code", "ZA")],
)
def test_v551j_keeps_run_and_country_boundaries_exact(field: str, value: str) -> None:
    frame = _frame()
    frame.loc[:, field] = value
    with pytest.raises(BoundaryContractError, match="V551_ARTIFACT_IDENTITY_MISMATCH"):
        _verify_frame_scope(frame, ARTIFACT, _scope())


def test_v551j_requires_uid_columns_on_all_v551_canonical_surfaces() -> None:
    for required in V551_V3_REQUIRED_COLUMNS.values():
        assert {"source_family_uid", "wave_uid"}.issubset(required)
    frame = _frame().drop(columns=["wave_uid"])
    with pytest.raises(BoundaryContractError, match="V551_ARTIFACT_SCHEMA_MISSING_COLUMNS"):
        _verify_frame_scope(frame, ARTIFACT, _scope())


def test_expected_v551_scope_inherits_machine_identity_from_v550j_manifest(tmp_path: Path) -> None:
    identity = resolve_source_wave_identity("Afrobarometer", "R1", require_closed_35=True)
    manifest = {
        "run_id": "run-1",
        "source": "Afrobarometer",
        "wave": "R1",
        "canonical_wave": "R1",
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "country_codes": ["LS"],
        "producer_scope_identity": {
            "run_id": "run-1",
            "source": "Afrobarometer",
            "wave": "R1",
            "canonical_wave": "R1",
            "source_family_uid": identity.source_family_uid,
            "wave_uid": identity.wave_uid,
            "country_code": "LS",
            "country_codes": ["LS"],
            "shard_id": "",
            "scope_kind": "country",
        },
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    rows = pd.DataFrame(
        [
            {
                "run_id": "run-1",
                "source_family": "Afrobarometer",
                "canonical_wave": "R1",
                "country_code": "LS",
            }
        ]
    )
    scope = _expected_v551_scope("run-1", rows, rows.copy(), manifest_path)
    assert scope["source_family_uid"] == identity.source_family_uid
    assert scope["wave_uid"] == identity.wave_uid
