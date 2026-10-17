#!/usr/bin/env python3
"""Family-aware repository discovery for V553 wave harmonization.

Discovery keys every candidate by ``(source, canonical_wave, country)``.  Legacy GSS
directory names remain readable as an adapter, but are not the discovery model.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from data.ddm_build_copy.ddm_survey_identity import (
    SurveyIdentityError,
    canonical_country_code,
    canonical_family_key,
    canonical_wave_key,
    require_survey_identity,
)
from data.ddm_build_copy.ddm_v550_family_overlay import load_family_overlay


LEGACY_GSS_DIR_RE = re.compile(
    r"^gss(?P<wave>\d{4})(?:[_-].*)?$",
    re.IGNORECASE,
)
KNOWN_SOURCE_PREFIXES = (
    "arab_barometer",
    "asian_barometer",
    "south_asia",
    "latinobarometro",
    "afrobarometer",
    "gss",
    "wvs",
    "evs",
    "lits",
)
IDENTITY_JSON_CANDIDATES = (
    "shard_manifest.json",
    "run_manifest.json",
    "manifest.json",
    "shard_scope.json",
)


@dataclass(frozen=True)
class DiscoveredWaveRun:
    source: str
    source_key: str
    wave: str
    canonical_wave: str
    country_code: str
    temporal_year: int | None
    run_root: str
    source_root: str
    mtime_ns: int
    depth: int
    identity_basis: str


def _path_depth(root: Path, path: Path) -> int:
    try:
        return len(path.relative_to(root).parts)
    except Exception:
        return 999


def _mapping_identity(
    payload: dict[str, Any],
) -> tuple[str, str, str, int | None] | None:
    source = str(payload.get("source") or payload.get("source_family") or "").strip()
    wave = str(payload.get("canonical_wave") or payload.get("wave") or "").strip()
    if not source or not wave:
        return None
    country = canonical_country_code(
        payload.get("country_code") or payload.get("country")
    )
    temporal_year_text = str(
        payload.get("temporal_year")
        or payload.get("fieldwork_year")
        or payload.get("survey_year")
        or payload.get("year")
        or ""
    ).strip()
    temporal_year = (
        int(temporal_year_text)
        if temporal_year_text.isdigit()
        and 1000 <= int(temporal_year_text) <= 3000
        else None
    )
    return source, wave, country, temporal_year


def _identity_from_fixed_manifests(
    path: Path,
) -> tuple[str, str, str, int | None, str] | None:
    candidates = [path / name for name in IDENTITY_JSON_CANDIDATES]
    candidates.extend(path / "manifest" / name for name in IDENTITY_JSON_CANDIDATES)
    for candidate in candidates:
        if not candidate.is_file():
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        identity = _mapping_identity(payload)
        if identity:
            return (
                identity[0],
                identity[1],
                identity[2],
                identity[3],
                f"manifest:{candidate.name}",
            )
    return None


def _identity_from_name(
    path: Path,
) -> tuple[str, str, str, int | None, str] | None:
    legacy = LEGACY_GSS_DIR_RE.match(path.name)
    if legacy:
        return (
            "GSS",
            legacy.group("wave"),
            "",
            int(legacy.group("wave")),
            "legacy_gss_directory_adapter",
        )

    if "__" in path.name:
        source, wave = path.name.rsplit("__", 1)
        if canonical_family_key(source) and canonical_wave_key(source, wave):
            return source, wave, "", None, "source_double_underscore_wave"

    normalized_name = re.sub(r"[^A-Za-z0-9]+", "_", path.name).strip("_")
    lowered = normalized_name.lower()
    for prefix in KNOWN_SOURCE_PREFIXES:
        marker = f"{prefix}_"
        if not lowered.startswith(marker):
            continue
        wave = normalized_name[len(marker) :]
        if canonical_wave_key(prefix, wave):
            return prefix, wave, "", None, "known_source_prefix"
    return None


def _candidate_identity(
    path: Path,
) -> tuple[str, str, str, int | None, str] | None:
    return _identity_from_fixed_manifests(path) or _identity_from_name(path)


def discover_latest_wave_runs(
    search_roots: Iterable[str | Path],
) -> list[DiscoveredWaveRun]:
    best: dict[tuple[str, str, str], DiscoveredWaveRun] = {}
    for search_root in search_roots:
        root = Path(search_root)
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_dir():
                continue
            candidate_identity = _candidate_identity(path)
            if candidate_identity is None:
                continue
            source, wave, country_code, temporal_year, basis = candidate_identity
            try:
                identity = require_survey_identity(source, wave)
                stat = path.stat()
            except Exception:
                continue
            candidate = DiscoveredWaveRun(
                source=identity.source,
                source_key=identity.source_key,
                wave=str(wave),
                canonical_wave=identity.canonical_wave,
                country_code=canonical_country_code(country_code),
                temporal_year=temporal_year,
                run_root=str(path),
                source_root=str(root),
                mtime_ns=int(
                    getattr(
                        stat,
                        "st_mtime_ns",
                        int(stat.st_mtime * 1_000_000_000),
                    )
                ),
                depth=_path_depth(root, path),
                identity_basis=basis,
            )
            key = (
                identity.source_key,
                identity.canonical_wave,
                canonical_country_code(country_code),
            )
            current = best.get(key)
            if current is None or (
                candidate.mtime_ns,
                -candidate.depth,
                candidate.run_root,
            ) > (
                current.mtime_ns,
                -current.depth,
                current.run_root,
            ):
                best[key] = candidate
    return [best[key] for key in sorted(best)]


def _overlay_count(authority_dir: Path, source: str, wave: str) -> int:
    count = 0
    for overlay_type in (
        "semantic_authority",
        "directionality",
        "position_conditioning",
    ):
        result = load_family_overlay(
            source,
            wave,
            overlay_type,
            required=False,
            search_roots=[authority_dir],
        )
        count += int(result.status == "FOUND")
    return count


def choose_best_authority_dir(
    source: str,
    wave: str,
    candidates: Iterable[str | Path],
) -> tuple[str, dict[str, int]]:
    scored: list[tuple[int, int, int, str]] = []
    counts: dict[str, int] = {}
    for index, candidate in enumerate(candidates):
        path = Path(candidate)
        if not path.exists():
            continue
        count = _overlay_count(path, source, wave)
        counts[str(path)] = count
        if count > 0:
            scored.append((count, -index, -len(path.parts), str(path)))
    if not scored:
        return "", counts
    scored.sort(reverse=True)
    return scored[0][3], counts


def latest_run_root_for_wave(
    root: str | Path,
    source: str,
    wave: str,
    country_code: str = "",
) -> str:
    identity = require_survey_identity(source, wave)
    requested_country = canonical_country_code(country_code)
    matches = [
        item
        for item in discover_latest_wave_runs([root])
        if item.source_key == identity.source_key
        and item.canonical_wave == identity.canonical_wave
        and (
            not requested_country
            or item.country_code == requested_country
        )
    ]
    return matches[0].run_root if len(matches) == 1 else ""


def build_wave_descriptors_from_repo(
    *,
    repo_root: str | Path,
    survey_family: str = "",
    country_code: str = "",
    authority_candidates: Iterable[str | Path] = (),
    layer_search_roots: Iterable[str | Path] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = Path(repo_root)
    requested_key = canonical_family_key(survey_family)
    requested_country = canonical_country_code(country_code)
    if not requested_key:
        raise SurveyIdentityError(
            "V553 repository discovery requires an explicit survey_family"
        )
    if not requested_country:
        raise SurveyIdentityError(
            "V553 repository discovery requires an explicit country_code"
        )
    if layer_search_roots is None:
        layer_search_roots = (
            root / "data" / "ddm_repository_copy" / "v5_thin_end_to_end" / "runs",
            root / "data" / "ddm_repository_copy" / "v552" / "runs",
            root / "data" / "ddm_repository_copy" / "v551" / "runs",
            root / "data" / "ddm_repository_copy" / "v550j" / "runs",
            root / "data" / "ddm_repository_copy" / "v551j" / "runs",
            root / "data" / "ddm_repository_copy" / "v550" / "shard_runs",
        )
    if not authority_candidates:
        authority_candidates = (
            root / "data" / "ddm_build_copy" / "reports",
            root / "data" / "ddm_build_copy" / "directionality_authority",
        )

    discovered = discover_latest_wave_runs(layer_search_roots)
    discovered = [
        item
        for item in discovered
        if item.source_key == requested_key
        and item.country_code == requested_country
    ]
    discovered_sources = sorted({item.source_key for item in discovered})
    if len(discovered_sources) > 1:
        raise RuntimeError(
            "repository discovery found multiple survey families; pass an "
            f"explicit source filter: {discovered_sources}"
        )
    descriptors: list[dict[str, Any]] = []
    authority_choice_counts: dict[str, dict[str, int]] = {}
    for item in discovered:
        authority_dir, counts = choose_best_authority_dir(
            item.source,
            item.canonical_wave,
            authority_candidates,
        )
        latest_v552j_root = latest_run_root_for_wave(
            root / "data" / "ddm_repository_copy" / "v552j" / "runs",
            item.source,
            item.canonical_wave,
            requested_country or item.country_code,
        )
        latest_v552j_readiness = ""
        if latest_v552j_root:
            readiness_path = (
                Path(latest_v552j_root)
                / "manifest"
                / "v552j_readiness_report.json"
            )
            if readiness_path.exists():
                latest_v552j_readiness = str(readiness_path)
        scope_key = f"{item.source_key}::{item.canonical_wave}"
        authority_choice_counts[scope_key] = counts
        descriptors.append(
            {
                "wave": item.wave,
                "source": item.source,
                "canonical_wave": item.canonical_wave,
                "country_code": requested_country or item.country_code,
                "temporal_year": item.temporal_year,
                "run_root": item.run_root,
                "authority_dir": authority_dir,
                "latest_v552j_root": latest_v552j_root,
                "latest_v552j_readiness_report": latest_v552j_readiness,
                "discovered_from": item.source_root,
                "identity_basis": item.identity_basis,
                "run_root_mtime_ns": item.mtime_ns,
                "run_root_depth": item.depth,
            }
        )

    report = {
        "repo_root": str(root),
        "source_filter": survey_family,
        "country_filter": requested_country,
        "wave_count": len(descriptors),
        "scopes": [
            {
                "source": item["source"],
                "canonical_wave": item["canonical_wave"],
                "country_code": item["country_code"],
            }
            for item in descriptors
        ],
        "authority_choice_counts": authority_choice_counts,
        "layer_search_roots": [str(path) for path in layer_search_roots],
        "authority_candidates": [
            str(Path(candidate)) for candidate in authority_candidates
        ],
    }
    return descriptors, report


__all__ = [
    "DiscoveredWaveRun",
    "build_wave_descriptors_from_repo",
    "choose_best_authority_dir",
    "discover_latest_wave_runs",
    "latest_run_root_for_wave",
]
