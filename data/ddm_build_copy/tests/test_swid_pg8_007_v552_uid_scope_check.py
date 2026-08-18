from __future__ import annotations

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v552_structural_ddm import _verify_frame_scope
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity


def _scope(source: str, wave: str, country: str = "LS") -> dict[str, str]:
    identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    return {
        "source": identity.canonical_display_source,
        "wave": identity.canonical_display_wave,
        "canonical_wave": identity.canonical_display_wave,
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "country_code": country,
        "shard_id": "",
        "scope_kind": "country",
    }


def _frame(source: str, wave: str, country: str = "LS", run_id: str = "run-1") -> pd.DataFrame:
    identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    return pd.DataFrame([
        {
            "run_id": run_id,
            "source": source,
            "source_family": source,
            "source_family_uid": identity.source_family_uid,
            "canonical_wave": wave,
            "wave_uid": identity.wave_uid,
            "country_code": country,
        }
    ])


@pytest.mark.parametrize("alias", ["R1", "ROUND1", "Round 1"])
def test_v552_scope_accepts_afrobarometer_wave_aliases_by_uid(alias: str) -> None:
    scope = _scope("Afrobarometer", "R1")
    _verify_frame_scope(
        _frame("Afrobarometer", alias),
        run_id="run-1",
        scope=scope,
        label="coverage",
    )


def test_v552_scope_accepts_latinobarometro_source_alias_by_uid() -> None:
    scope = _scope("Latinobarómetro", "1995", country="BR")
    _verify_frame_scope(
        _frame("Latinobarometro", "1995", country="BR"),
        run_id="run-1",
        scope=scope,
        label="coverage",
    )


def test_v552_scope_still_rejects_true_source_wave_identity_contradiction() -> None:
    scope = _scope("Afrobarometer", "R1")
    frame = _frame("Afrobarometer", "R1")
    wrong = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    frame.loc[:, "source_family_uid"] = wrong.source_family_uid
    frame.loc[:, "wave_uid"] = wrong.wave_uid
    with pytest.raises(RuntimeError, match="BLOCKED_V552_COVERAGE_IDENTITY_COHERENCE"):
        _verify_frame_scope(frame, run_id="run-1", scope=scope, label="coverage")


@pytest.mark.parametrize(
    ("field", "value"),
    [("run_id", "different-run"), ("country_code", "ZA")],
)
def test_v552_scope_keeps_run_and_country_exact(field: str, value: str) -> None:
    scope = _scope("Afrobarometer", "R1")
    frame = _frame("Afrobarometer", "ROUND1")
    frame.loc[:, field] = value
    with pytest.raises(RuntimeError, match="BLOCKED_V552_COVERAGE_SCOPE_MISMATCH"):
        _verify_frame_scope(frame, run_id="run-1", scope=scope, label="coverage")
