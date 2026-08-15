#!/usr/bin/env python3
"""Family-dispatched overlay loader for V550 survey portability.

Resolution is family-normalized, wave-alias aware, repo-root anchored, and
fail-closed.  It never falls back to GSS for a non-GSS family and it prefers
canonical packet filenames over legacy aliases.
"""
from __future__ import annotations

import json
import hashlib
import os
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from data.ddm_build_copy.ddm_survey_identity import (
    canonical_family_key,
    canonical_wave_key,
    family_keys_equal,
    wave_aliases,
    waves_equivalent,
)

ROOT = Path(__file__).resolve().parents[2]

OVERLAY_TYPES = [
    "semantic_authority",
    "position_conditioning",
    "directionality",
    "response_scale_authority",
    "bridge_authority",
    "first_pass_authority",
]

OVERLAY_SUFFIXES = {
    "semantic_authority": ["_semantic_authority_overlay.csv"],
    "position_conditioning": ["_position_conditioning_overlay.csv"],
    "directionality": ["_directionality_overlay.csv", "_directionality_authority.csv"],
    "first_pass_authority": ["_first_pass_authority_table.csv", "_first_pass_authority_overlay.csv"],
    "response_scale_authority": ["_response_scale_authority.csv", "_response_scale_authority_overlay.csv"],
    "bridge_authority": ["_bridge_authority.csv", "_bridge_authority_overlay.csv"],
}

# Ordered canonical stems.  The first existing candidate wins.  Legacy stems
# are deliberately lower priority so stale generated overlays cannot shadow the
# rebuilt packet output.
FAMILY_FILE_STEMS = {
    "latinobarometro": ["latinobarómetro", "latinobarometro", "latinobar_metro"],
    "arab_barometer": ["arab_barometer"],
    "asian_barometer": ["asian_barometer"],
    "south_asia": ["south_asia", "southasia"],
}

WVS_YEAR_BY_WAVE = {"W1": "1981", "W4": "2000", "W7": "2017"}
WAVE_AUTHORITY_REGISTRY = ROOT / "data" / "ddm_build_copy" / "bindings" / "wave_authority_registry_35wave_v1.json"


@dataclass
class OverlayLoadResult:
    survey_family: str = ""
    canonical_wave: str = ""
    country_code: str = ""
    overlay_type: str = ""
    status: str = "UNSUPPORTED_FAMILY"
    path: str = ""
    row_count: int = 0
    columns: list = field(default_factory=list)
    missing_columns: list = field(default_factory=list)
    required: bool = True
    absence_policy: str = "block"
    message: str = ""
    data_frame: Any = None
    resolved_family_from_path: str = ""
    resolved_wave_from_path: str = ""


def _search_roots() -> list[Path]:
    # ``data/ddm_build`` is an immutable legacy tree and is never an authority
    # fallback for active execution.
    return [ROOT / "data" / "ddm_build_copy" / "reports"]


def _family_stems(survey_family: str) -> list[str]:
    key = canonical_family_key(survey_family)
    raw = re.sub(r"[^0-9A-Za-zÀ-ÿ]+", "_", str(survey_family).strip().lower()).strip("_")
    stems = [*FAMILY_FILE_STEMS.get(key, []), raw, key]
    out: list[str] = []
    seen: set[str] = set()
    for stem in stems:
        if stem and stem not in seen:
            seen.add(stem)
            out.append(stem)
    return out


def _candidate_paths(root: Path, survey_family: str, canonical_wave: str, overlay_type: str) -> list[tuple[Path, str]]:
    candidates: list[tuple[Path, str]] = []
    family_key = canonical_family_key(survey_family)
    for stem in _family_stems(survey_family):
        aliases = wave_aliases(survey_family, canonical_wave)
        if family_key == "wvs" and overlay_type == "directionality":
            year_alias = WVS_YEAR_BY_WAVE.get(canonical_wave_key(survey_family, canonical_wave))
            if year_alias:
                aliases = [year_alias, *aliases]
        for wave in dict.fromkeys(aliases):
            wave_tokens = [wave, re.sub(r"[^A-Za-z0-9]+", "_", wave).strip("_")]
            for wave_token in dict.fromkeys(token for token in wave_tokens if token):
                for suffix in OVERLAY_SUFFIXES.get(overlay_type, []):
                    candidates.append((root / f"{stem}_{wave_token}{suffix}", wave))
                    candidates.append((root / f"{stem}{wave_token}{suffix}", wave))
    return candidates


def _frame_matches_request(df: Any, survey_family: str, canonical_wave: str) -> tuple[bool, str]:
    """Validate source/wave columns when they are present.

    A packet file may use W1 in the DB and I in the overlay.  Those are treated
    as aliases only for Arab Barometer.
    """
    if getattr(df, "empty", True):
        return True, ""
    source_column = "source" if "source" in df.columns else None
    wave_column = "canonical_wave" if "canonical_wave" in df.columns else ("wave" if "wave" in df.columns else None)
    if source_column:
        values = [value for value in df[source_column].dropna().astype(str).unique() if str(value).strip()]
        bad = [value for value in values if not family_keys_equal(value, survey_family)]
        if bad:
            return False, f"source column contains nonmatching family values: {bad[:5]}"
    if wave_column:
        values = [value for value in df[wave_column].dropna().astype(str).unique() if str(value).strip()]
        bad = [value for value in values if not waves_equivalent(survey_family, value, canonical_wave)]
        if bad:
            return False, f"{wave_column} column contains nonmatching wave values: {bad[:5]}"
    return True, ""


def _registry_token(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).casefold()
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "", text)


def _registered_wave_entry(survey_family: str, canonical_wave: str) -> dict[str, Any] | None:
    if not WAVE_AUTHORITY_REGISTRY.exists():
        return None
    payload = json.loads(WAVE_AUTHORITY_REGISTRY.read_text(encoding="utf-8"))
    family_token = _registry_token(survey_family)
    wave_token = _registry_token(canonical_wave)
    for entry in payload.get("entries", []):
        if _registry_token(entry.get("source_family")) != family_token:
            continue
        aliases = entry.get("incoming_aliases", [])
        if wave_token == _registry_token(entry.get("canonical_wave")) or any(wave_token == _registry_token(alias) for alias in aliases):
            return entry
    return None


def load_family_overlay(
    survey_family: str,
    canonical_wave: str,
    overlay_type: str,
    *,
    country_code: str | None = None,
    required: bool = True,
    search_roots: list[Path] | None = None,
    absence_policy: str = "block",
    use_registry: bool = True,
) -> OverlayLoadResult:
    result = OverlayLoadResult(
        survey_family=survey_family,
        canonical_wave=canonical_wave,
        overlay_type=overlay_type,
        required=required,
        absence_policy=absence_policy,
        country_code=country_code or "",
    )
    if not canonical_family_key(survey_family) or not canonical_wave_key(survey_family, canonical_wave):
        result.status = "UNSUPPORTED_FAMILY"
        result.message = "survey_family and canonical_wave are required"
        return result
    if overlay_type not in OVERLAY_TYPES:
        result.status = "UNSUPPORTED_FAMILY"
        result.message = f"Unknown overlay type: {overlay_type}"
        return result

    roots = [Path(root) for root in (search_roots or _search_roots())]
    registry_entry = _registered_wave_entry(survey_family, canonical_wave) if use_registry else {"stages": {}}
    if not use_registry:
        # Registry compiler escape hatch: resolve the installed surface once
        # while producing the immutable registry. Runtime callers must use the
        # registry-backed path above.
        for root in roots:
            for path, resolved_wave in _candidate_paths(root, survey_family, canonical_wave, overlay_type):
                path = path.resolve()
                if not path.exists():
                    continue
                try:
                    import pandas as pd
                    df = pd.read_csv(path, low_memory=False)
                except Exception as exc:
                    result.status = "INVALID_SCHEMA"
                    result.message = f"Failed to read {path}: {exc}"
                    return result
                valid, validation_message = _frame_matches_request(df, survey_family, canonical_wave)
                if valid:
                    result.status = "FOUND"
                    result.path = str(path)
                    result.row_count = len(df)
                    result.columns = list(df.columns)
                    result.data_frame = df
                    result.resolved_family_from_path = canonical_family_key(survey_family)
                    result.resolved_wave_from_path = canonical_wave_key(survey_family, resolved_wave)
                    result.message = f"Loaded {result.row_count} rows from {path}"
                    return result
        result.status = "MISSING_REQUIRED" if required else "MISSING_OPTIONAL"
        result.message = f"No {overlay_type} overlay for {survey_family}/{canonical_wave}"
        return result
    if registry_entry is None:
        result.status = "UNREGISTERED_WAVE"
        result.message = f"No closed 35-wave authority registry entry for {survey_family}/{canonical_wave}"
        return result
    # The registry is the canonicalization boundary: aliases such as WVII or
    # 2017 resolve to the registered WVS W7 before identity validation.
    canonical_wave = str(registry_entry.get("canonical_wave") or canonical_wave)
    result.canonical_wave = canonical_wave
    registered_stage = (registry_entry.get("stages") or {}).get(overlay_type)
    if not registered_stage:
        result.status = "UNREGISTERED_AUTHORITY_STAGE"
        result.message = f"No registered {overlay_type} authority for {survey_family}/{canonical_wave}"
        return result
    registered_name = Path(str(registered_stage.get("relative_path", ""))).name
    expected_sha256 = str(registered_stage.get("sha256", ""))
    seen: set[Path] = set()
    for root in roots:
        path = (root / registered_name).resolve()
        if path in seen or not path.exists():
            continue
        seen.add(path)
        if expected_sha256:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != expected_sha256:
                result.status = "AUTHORITY_HASH_MISMATCH"
                result.path = str(path)
                result.message = f"Registered authority hash mismatch for {path}: expected {expected_sha256}, got {digest}"
                return result
        resolved_wave = canonical_wave
        try:
            import pandas as pd

            df = pd.read_csv(path, low_memory=False)
        except Exception as exc:
            result.status = "INVALID_SCHEMA"
            result.message = f"Failed to read {path}: {exc}"
            return result
        valid, validation_message = _frame_matches_request(df, survey_family, canonical_wave)
        if not valid:
            result.status = "INVALID_SCHEMA"
            result.path = str(path)
            result.message = f"Overlay identity mismatch for {path}: {validation_message}"
            return result
        result.status = "FOUND"
        result.path = str(path)
        result.row_count = len(df)
        result.columns = list(df.columns)
        result.data_frame = df
        result.resolved_family_from_path = canonical_family_key(survey_family)
        result.resolved_wave_from_path = canonical_wave_key(survey_family, resolved_wave)
        result.message = f"Loaded {result.row_count} rows from {path}"
        return result

    result.status = "MISSING_REQUIRED" if required else "MISSING_OPTIONAL"
    optional = " (optional)" if not required else ""
    result.message = f"No {overlay_type} overlay for {survey_family}/{canonical_wave}{optional}"
    return result


# ===== Backwards-compatible GSS wrappers =====

def load_gss_position_conditioning_overlay(directory=None, canonical_wave=None):
    from warnings import warn
    warn("load_gss_position_conditioning_overlay deprecated. Use load_family_overlay('GSS', wave, 'position_conditioning')")
    result = load_family_overlay("GSS", canonical_wave, "position_conditioning", search_roots=[Path(directory)] if directory else None)
    return result.data_frame if result.status == "FOUND" and result.data_frame is not None else None


def load_gss_semantic_authority_overlay(directory=None, canonical_wave=None):
    from warnings import warn
    warn("load_gss_semantic_authority_overlay deprecated. Use load_family_overlay('GSS', wave, 'semantic_authority')")
    result = load_family_overlay("GSS", canonical_wave, "semantic_authority", search_roots=[Path(directory)] if directory else None)
    return result.data_frame if result.status == "FOUND" and result.data_frame is not None else None


def load_gss_directionality_overlay(directory=None, canonical_wave=None):
    from warnings import warn
    warn("load_gss_directionality_overlay deprecated. Use load_family_overlay('GSS', wave, 'directionality')")
    result = load_family_overlay("GSS", canonical_wave, "directionality", search_roots=[Path(directory)] if directory else None)
    return result.data_frame if result.status == "FOUND" and result.data_frame is not None else None


def load_gss_first_pass_authority(directory=None, canonical_wave=None):
    from warnings import warn
    warn("load_gss_first_pass_authority deprecated. Use load_family_overlay('GSS', wave, 'first_pass_authority')")
    result = load_family_overlay("GSS", canonical_wave, "first_pass_authority", search_roots=[Path(directory)] if directory else None)
    return result.data_frame if result.status == "FOUND" and result.data_frame is not None else None


# ===== Overlay Manifest Resolution =====

def load_overlay_manifest(manifest_path: str | None = None, survey_family: str = "") -> dict | None:
    if manifest_path and os.path.exists(manifest_path):
        with open(manifest_path) as handle:
            return json.load(handle)
    if survey_family:
        for root in _search_roots():
            for stem in _family_stems(survey_family):
                fp = root / f"{stem}_overlay_manifest.json"
                if fp.exists():
                    with open(fp) as handle:
                        return json.load(handle)
    return None
