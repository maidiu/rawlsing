#!/usr/bin/env python3
"""Runtime loader for the closed 35-wave P2 deep-question authority binding."""

from __future__ import annotations

import hashlib
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_family_overlay import family_keys_equal, waves_equivalent


HERE = Path(__file__).resolve().parent
DEFAULT_PATH = HERE / "bindings" / "p2_deep_question_authority_35wave_v1.csv"
DEFAULT_MANIFEST = HERE / "bindings" / "p2_deep_question_authority_35wave_v1.manifest.json"
PATH_ENV = "RAWLSING_P2_DEEP_QUESTION_AUTHORITY_PATH"
REQUIRED_COLUMNS = {
    "authority_version",
    "source",
    "canonical_wave",
    "var_name",
    "semantic_role",
    "designation_confidence",
    "manual_designation_required",
    "semantic_role_authority_status",
    "response_topology",
    "current_directional_atom_eligible",
    "directional_certification_status",
    "directionality_authority_status",
    "authority_row_sha256",
}


class DeepQuestionAuthorityError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def active_path(path: Path | str | None = None) -> Path:
    resolved = Path(path) if path is not None else Path(os.environ.get(PATH_ENV, DEFAULT_PATH))
    if not resolved.is_file():
        raise DeepQuestionAuthorityError(f"missing compiled P2 deep-question authority binding: {resolved}")
    return resolved


@lru_cache(maxsize=4)
def _load_cached(path_text: str, mtime_ns: int, size: int) -> pd.DataFrame:
    del mtime_ns, size
    path = Path(path_text)
    frame = pd.read_csv(path, low_memory=False, dtype=object, keep_default_na=False)
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise DeepQuestionAuthorityError(f"compiled P2 deep authority missing columns: {sorted(missing)}")
    duplicate = frame.duplicated(["source", "canonical_wave", "var_name"], keep=False)
    if duplicate.any():
        sample = frame.loc[duplicate, ["source", "canonical_wave", "var_name"]].head(20).to_dict(orient="records")
        raise DeepQuestionAuthorityError(f"ambiguous compiled P2 deep authority keys: {sample}")
    return frame


def load_deep_question_authority(
    source_family: Any,
    canonical_wave: Any,
    *,
    path: Path | str | None = None,
) -> pd.DataFrame:
    resolved = active_path(path)
    stat = resolved.stat()
    frame = _load_cached(str(resolved), stat.st_mtime_ns, stat.st_size)
    source = str(source_family or "").strip()
    wave = str(canonical_wave or "").strip()
    mask = frame["source"].map(lambda value: family_keys_equal(value, source))
    mask &= frame["canonical_wave"].map(lambda value: waves_equivalent(source, value, wave))
    scoped = frame.loc[mask].copy()
    scoped.attrs["authority_artifact_path"] = str(resolved)
    scoped.attrs["authority_artifact_sha256"] = _sha256(resolved)
    scoped.attrs["authority_version"] = (
        scoped["authority_version"].iloc[0] if not scoped.empty else "p2_deep_question_authority_35wave_v1"
    )
    return scoped


def authority_receipt(path: Path | str | None = None) -> dict[str, Any]:
    resolved = active_path(path)
    manifest_path = DEFAULT_MANIFEST if resolved == DEFAULT_PATH else resolved.with_suffix(".manifest.json")
    receipt: dict[str, Any] = {
        "path": str(resolved),
        "sha256": _sha256(resolved),
        "manifest_path": str(manifest_path) if manifest_path.is_file() else "",
    }
    if manifest_path.is_file():
        try:
            receipt["manifest"] = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise DeepQuestionAuthorityError(f"invalid deep-authority manifest: {manifest_path}: {exc}") from exc
    return receipt
