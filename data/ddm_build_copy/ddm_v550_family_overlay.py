#!/usr/bin/env python3
"""Family-dispatched overlay loader for V550 survey portability.

Source/wave identity is delegated to the shared governed UID kernel.  Alias-
named authority candidates are exhaustively enumerated for one governed UID
pair; exact duplicate bytes are equivalent, while divergent bytes fail closed.
Search order is never authority precedence.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    validate_source_wave_identity_coherence,
    verify_frame_source_wave_identity_coherence,
)
from data.ddm_build_copy.ddm_source_wave_identity import (
    ProductionMembershipError,
    SourceWaveIdentityError,
    compatibility_family_key,
    compatibility_wave_aliases,
    compatibility_wave_key,
    load_identity_registry,
    resolve_source_family_identity,
    resolve_source_wave_identity,
)

ROOT = Path(__file__).resolve().parents[2]
AUTHORITY_ROOT_ENV = "DDM_AUTHORITY_ROOT"

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

# Historical filename stems are compatibility locators only.  They are never
# identity authority and never establish precedence over another alias file.
FAMILY_FILE_STEMS = {
    "latinobarometro": ["latinobarómetro", "latinobarometro", "latinobar_metro"],
    "arab_barometer": ["arab_barometer"],
    "asian_barometer": ["asian_barometer"],
    "south_asia": ["south_asia", "southasia"],
}

# Historical WVS directionality filenames used survey year rather than wave.
# This remains a locator only after the governed UID has already been resolved.
WVS_YEAR_BY_WAVE_UID = {
    "wv_wvs_w1_v1": "1981",
    "wv_wvs_w4_v1": "2000",
    "wv_wvs_w7_v1": "2017",
}

REVIEW_ONLY_AUTHORITY_STATUS = "HEURISTIC_REVIEW_ONLY"
NOT_CERTIFIED_STATUS = "NOT_CERTIFIED"

# Compatibility exports used by older V550 helpers.  They delegate to the
# shared W01 kernel's compatibility surface rather than defining a resolver.
canonical_family_key = compatibility_family_key
canonical_wave_key = compatibility_wave_key
wave_aliases = compatibility_wave_aliases


class OverlayAuthorityConflictError(RuntimeError):
    """Raised when UID-equivalent authority candidates have divergent bytes."""


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
    source_family_uid: str = ""
    wave_uid: str = ""
    governance_state: str = ""
    closed_35_member: bool = False
    candidate_paths: list[str] = field(default_factory=list)
    candidate_sha256: list[str] = field(default_factory=list)


def _search_roots() -> list[Path]:
    # ``data/ddm_build`` is an immutable legacy tree and is never an authority
    # fallback for active execution.
    configured = os.getenv(AUTHORITY_ROOT_ENV, "").strip()
    if configured:
        return [Path(configured).expanduser().resolve() / "reports"]
    return [ROOT / "data" / "ddm_build_copy" / "reports"]


def _filename_stem(value: Any) -> str:
    return re.sub(r"[^0-9A-Za-zÀ-ÿ]+", "_", str(value or "").strip().lower()).strip("_")


def _ascii_filename_stem(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    folded = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^0-9A-Za-z]+", "_", folded.strip().lower()).strip("_")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_overlay_identity(
    survey_family: str,
    wave: str,
    *,
    historical_nonproduction: bool = False,
):
    """Resolve family first, then family-scoped wave through the shared kernel."""
    family = resolve_source_family_identity(survey_family)
    identity = resolve_source_wave_identity(
        family.canonical_display_source,
        wave,
        require_closed_35=not historical_nonproduction,
    )
    if not identity.production_authorized and not historical_nonproduction:
        raise ProductionMembershipError(
            f"overlay review generation requires CLOSED_35 identity: {identity.uid_key}"
        )
    return identity


def family_keys_equal(left: Any, right: Any) -> bool:
    try:
        return (
            resolve_source_family_identity(left).source_family_uid
            == resolve_source_family_identity(right).source_family_uid
        )
    except SourceWaveIdentityError:
        return False


def waves_equivalent(survey_family: Any, left: Any, right: Any) -> bool:
    try:
        family = resolve_source_family_identity(survey_family)
        left_identity = resolve_source_wave_identity(family.canonical_display_source, left)
        right_identity = resolve_source_wave_identity(family.canonical_display_source, right)
        return left_identity.wave_uid == right_identity.wave_uid
    except SourceWaveIdentityError:
        return False


def _family_stems_for_identity(identity) -> list[str]:
    registry = load_identity_registry()
    family = registry.source_uid_index[identity.source_family_uid]
    values = [
        *(family.get("aliases") or []),
        family.get("canonical_display_source", ""),
        family.get("compatibility_key", ""),
        *FAMILY_FILE_STEMS.get(str(family.get("compatibility_key", "")), []),
    ]
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        for stem in (_filename_stem(value), _ascii_filename_stem(value)):
            if stem and stem not in seen:
                seen.add(stem)
                out.append(stem)
    return out


def _wave_aliases_for_identity(identity, overlay_type: str) -> list[str]:
    registry = load_identity_registry()
    wave = registry.wave_uid_index[identity.wave_uid]
    values = [
        *(wave.get("aliases") or []),
        wave.get("canonical_display_wave", ""),
        wave.get("compatibility_key", ""),
    ]
    if overlay_type == "directionality":
        legacy_year = WVS_YEAR_BY_WAVE_UID.get(identity.wave_uid)
        if legacy_year:
            values.append(legacy_year)
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if text and text.casefold() not in seen:
            seen.add(text.casefold())
            out.append(text)
    return out


def _candidate_paths(root: Path, survey_family: str, canonical_wave: str, overlay_type: str, *, historical_nonproduction: bool = False) -> list[tuple[Path, str]]:
    identity = resolve_overlay_identity(
        survey_family,
        canonical_wave,
        historical_nonproduction=historical_nonproduction,
    )
    candidates: set[tuple[Path, str]] = set()
    for stem in _family_stems_for_identity(identity):
        for wave in _wave_aliases_for_identity(identity, overlay_type):
            wave_tokens = [wave, re.sub(r"[^A-Za-z0-9]+", "_", wave).strip("_")]
            for wave_token in {token for token in wave_tokens if token}:
                for suffix in OVERLAY_SUFFIXES.get(overlay_type, []):
                    candidates.add((root / f"{stem}_{wave_token}{suffix}", wave))
                    candidates.add((root / f"{stem}{wave_token}{suffix}", wave))
    return sorted(candidates, key=lambda item: str(item[0]))


def _frame_matches_request(df: Any, survey_family: str, canonical_wave: str, *, historical_nonproduction: bool = False) -> tuple[bool, str]:
    """Validate every populated identity representation against one UID pair."""
    try:
        identity = resolve_overlay_identity(
            survey_family,
            canonical_wave,
            historical_nonproduction=historical_nonproduction,
        )
        verify_frame_source_wave_identity_coherence(
            df,
            expected_source_family_uid=identity.source_family_uid,
            expected_wave_uid=identity.wave_uid,
            allow_empty=True,
        )
    except (SourceWaveIdentityError, BoundaryContractError) as exc:
        return False, str(exc)
    return True, ""


def filter_frame_for_overlay_identity(df: Any, identity, *, var_name: str = ""):
    """Select rows by governed UID while rejecting contradictory row identity."""
    import pandas as pd

    if df is None or getattr(df, "empty", True):
        return pd.DataFrame(columns=getattr(df, "columns", []))
    working = df
    if var_name and "var_name" in working.columns:
        working = working[working["var_name"].astype(str).str.strip() == str(var_name).strip()]
    if working.empty:
        return working.copy()

    if {"source_family_uid", "wave_uid"}.issubset(working.columns):
        scoped = working[
            (working["source_family_uid"].astype(str).str.strip() == identity.source_family_uid)
            & (working["wave_uid"].astype(str).str.strip() == identity.wave_uid)
        ].copy()
        if not scoped.empty:
            verify_frame_source_wave_identity_coherence(
                scoped,
                expected_source_family_uid=identity.source_family_uid,
                expected_wave_uid=identity.wave_uid,
                allow_empty=True,
            )
        return scoped

    keep: list[Any] = []
    for index, row in working.iterrows():
        try:
            coherence = validate_source_wave_identity_coherence(
                row.to_dict(),
                require_complete=True,
            )
        except BoundaryContractError as exc:
            raise BoundaryContractError(
                f"OVERLAY_CONTEXT_IDENTITY_INVALID:row={index}:{exc}"
            ) from exc
        if (
            coherence.source_family_uid == identity.source_family_uid
            and coherence.wave_uid == identity.wave_uid
        ):
            keep.append(index)
    return working.loc[keep].copy()


def enforce_review_only_overlay_frame(df: Any):
    """Force generated candidate output to remain review-only/non-certified."""
    if df is None:
        return df
    out = df.copy()
    out["semantic_role_authority_status"] = REVIEW_ONLY_AUTHORITY_STATUS
    out["directionality_authority_status"] = REVIEW_ONLY_AUTHORITY_STATUS
    out["directional_certification_status"] = NOT_CERTIFIED_STATUS
    out["runtime_authority_status"] = NOT_CERTIFIED_STATUS
    out["current_directional_atom_eligible"] = False
    out["manual_review_required"] = True
    return out


def load_family_overlay(
    survey_family: str,
    canonical_wave: str,
    overlay_type: str,
    *,
    country_code: str | None = None,
    required: bool = True,
    search_roots: list[Path] | None = None,
    absence_policy: str = "block",
    historical_nonproduction: bool = False,
) -> OverlayLoadResult:
    result = OverlayLoadResult(
        survey_family=survey_family,
        canonical_wave=canonical_wave,
        overlay_type=overlay_type,
        required=required,
        absence_policy=absence_policy,
        country_code=country_code or "",
    )
    if overlay_type not in OVERLAY_TYPES:
        result.status = "UNSUPPORTED_FAMILY"
        result.message = f"Unknown overlay type: {overlay_type}"
        return result
    try:
        identity = resolve_overlay_identity(
            survey_family,
            canonical_wave,
            historical_nonproduction=historical_nonproduction,
        )
    except SourceWaveIdentityError as exc:
        result.status = "NONPRODUCTION_IDENTITY" if isinstance(exc, ProductionMembershipError) else "UNSUPPORTED_FAMILY"
        result.message = str(exc)
        return result

    result.source_family_uid = identity.source_family_uid
    result.wave_uid = identity.wave_uid
    result.governance_state = identity.governance_state
    result.closed_35_member = identity.closed_35_member

    roots = [Path(root) for root in (search_roots or _search_roots())]
    existing: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for root in roots:
        for path, resolved_wave in _candidate_paths(
            root,
            identity.canonical_display_source,
            identity.canonical_display_wave,
            overlay_type,
            historical_nonproduction=historical_nonproduction,
        ):
            resolved = path.resolve()
            if resolved in seen or not resolved.exists():
                continue
            seen.add(resolved)
            existing.append((resolved, resolved_wave))

    existing.sort(key=lambda item: str(item[0]))
    result.candidate_paths = [str(path) for path, _ in existing]
    if not existing:
        result.status = "MISSING_REQUIRED" if required else "MISSING_OPTIONAL"
        optional = " (optional)" if not required else ""
        result.message = f"No {overlay_type} overlay for {survey_family}/{canonical_wave}{optional}"
        return result

    loaded: list[tuple[Path, str, str, Any]] = []
    for path, resolved_wave in existing:
        try:
            import pandas as pd

            df = pd.read_csv(path, low_memory=False)
        except Exception as exc:
            result.status = "INVALID_SCHEMA"
            result.path = str(path)
            result.message = f"Failed to read {path}: {exc}"
            return result
        valid, validation_message = _frame_matches_request(
            df,
            identity.canonical_display_source,
            identity.canonical_display_wave,
            historical_nonproduction=historical_nonproduction,
        )
        if not valid:
            result.status = "INVALID_SCHEMA"
            result.path = str(path)
            result.message = f"Overlay identity mismatch for {path}: {validation_message}"
            return result
        loaded.append((path, resolved_wave, _sha256_file(path), df))

    hashes = sorted({digest for _, _, digest, _ in loaded})
    result.candidate_sha256 = hashes
    if len(hashes) != 1:
        result.status = "CONFLICTING_AUTHORITY_CANDIDATES"
        result.message = (
            f"UID-equivalent {overlay_type} candidates diverge for {identity.uid_key}: "
            + ", ".join(f"{path}={digest}" for path, _, digest, _ in loaded)
        )
        return result

    path, resolved_wave, _digest, df = loaded[0]
    result.status = "FOUND"
    result.path = str(path)
    result.row_count = len(df)
    result.columns = list(df.columns)
    result.data_frame = df
    result.resolved_family_from_path = identity.compatibility_source_key
    result.resolved_wave_from_path = identity.compatibility_wave_key
    duplicate_note = f"; {len(loaded)} byte-identical UID-equivalent candidates" if len(loaded) > 1 else ""
    result.message = f"Loaded {result.row_count} rows from {path}{duplicate_note}"
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
    if manifest_path:
        path = Path(manifest_path)
        if path.exists():
            with path.open() as handle:
                return json.load(handle)
        return None
    if not survey_family:
        return None

    family = resolve_source_family_identity(survey_family)
    # A manifest is family-scoped, so enumerate every governed family alias stem
    # and compare bytes before choosing any physical path.
    registry = load_identity_registry()
    family_record = registry.source_uid_index[family.source_family_uid]
    values = [
        *(family_record.get("aliases") or []),
        family_record.get("canonical_display_source", ""),
        family_record.get("compatibility_key", ""),
        *FAMILY_FILE_STEMS.get(str(family_record.get("compatibility_key", "")), []),
    ]
    stems: set[str] = set()
    for value in values:
        stems.update(stem for stem in (_filename_stem(value), _ascii_filename_stem(value)) if stem)

    candidates: set[Path] = set()
    for root in _search_roots():
        for stem in stems:
            path = (root / f"{stem}_overlay_manifest.json").resolve()
            if path.exists():
                candidates.add(path)
    if not candidates:
        return None

    loaded: list[tuple[Path, str, dict[str, Any]]] = []
    for path in sorted(candidates, key=str):
        with path.open() as handle:
            payload = json.load(handle)
        try:
            validate_source_wave_identity_coherence(
                payload,
                expected_source_family_uid=family.source_family_uid,
                require_complete=False,
            )
        except BoundaryContractError as exc:
            raise OverlayAuthorityConflictError(
                f"overlay manifest identity mismatch for {path}: {exc}"
            ) from exc
        loaded.append((path, _sha256_file(path), payload))

    hashes = {digest for _, digest, _ in loaded}
    if len(hashes) != 1:
        raise OverlayAuthorityConflictError(
            "UID-equivalent overlay manifests diverge for "
            f"{family.source_family_uid}: "
            + ", ".join(f"{path}={digest}" for path, digest, _ in loaded)
        )
    return loaded[0][2]
