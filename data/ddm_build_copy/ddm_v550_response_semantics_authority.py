#!/usr/bin/env python3
"""Exact V550 -> V551 response-semantics contract binding authority.

`response_semantics_contract_hash` is a governed packet identity minted by the
frozen response-option authority and consumed as an exact key by V551.  It is
not a response-option-map content hash and must never be synthesized from a
whole DataFrame, response family, or inferred scale geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_family_overlay import (
    canonical_family_key,
    canonical_wave_key,
)


ROOT = Path(__file__).resolve().parents[2]
BINDING_PATH = (
    ROOT
    / "data"
    / "ddm_build_copy"
    / "authority"
    / "v550_v551_response_semantics_contract_binding_v1.csv"
)
BINDING_MANIFEST_PATH = BINDING_PATH.with_suffix(".manifest.json")
V551_REGISTRY_PATH = (
    ROOT
    / "data"
    / "ddm_build_copy"
    / "authority"
    / "response_scale_encoding_registry_35wave_active_v1.csv"
)
V551_REGISTRY_MANIFEST_PATH = V551_REGISTRY_PATH.with_suffix(".manifest.json")

BINDING_SCHEMA_VERSION = "v550_v551_response_semantics_contract_binding_v1"
V551_REGISTRY_SCHEMA_VERSION = "v551_scale_encoding_registry_35wave_active_v1"
EXPECTED_ACTIVE_BINDINGS = 236
EXPECTED_DISTINCT_CONTRACTS = 145

REQUIRED_BINDING_COLUMNS = [
    "source_family",
    "canonical_wave",
    "var_code",
    "v551_registry_key_index",
    "substantive_category_count",
]


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return _clean(value).lower() in {"1", "true", "t", "yes", "y"}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def response_option_map_content_sha256(frame: pd.DataFrame) -> str:
    """Stable logical-content digest for a response-option-map DataFrame.

    This digest is artifact/content identity only.  It is deliberately named
    differently from `response_semantics_contract_hash`.
    """
    if frame.empty:
        payload: dict[str, Any] = {"rows": 0, "columns": []}
    else:
        columns = sorted(str(column) for column in frame.columns)
        canonical = frame.loc[:, columns].copy().fillna("").astype(str)
        canonical = canonical.sort_values(columns).reset_index(drop=True)
        payload = {
            "rows": int(len(canonical)),
            "columns": columns,
            "records": canonical.to_dict(orient="records"),
        }
    raw = json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class ResponseSemanticsContractBinding:
    source_family: str
    canonical_wave: str
    var_code: str
    response_semantics_contract_hash: str
    substantive_category_count: int


def _binding_key(source: Any, wave: Any, var_code: Any) -> tuple[str, str, str]:
    family = canonical_family_key(_clean(source))
    canonical_wave = canonical_wave_key(family, _clean(wave)) or _clean(wave)
    return (family, canonical_wave.upper(), _clean(var_code).lower())


@lru_cache(maxsize=1)
def load_v551_registry_key_set() -> frozenset[str]:
    if not V551_REGISTRY_PATH.exists() or not V551_REGISTRY_MANIFEST_PATH.exists():
        raise FileNotFoundError("frozen V551 response-scale registry/manifest is missing")

    manifest = json.loads(V551_REGISTRY_MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != V551_REGISTRY_SCHEMA_VERSION:
        raise ValueError(
            "unsupported V551 response-scale registry schema: "
            f"{manifest.get('schema_version')!r}"
        )
    declared_sha = _clean(manifest.get("registry_sha256"))
    actual_sha = _sha256(V551_REGISTRY_PATH)
    if not declared_sha or actual_sha != declared_sha:
        raise ValueError(
            "V551 response-scale registry SHA-256 mismatch: "
            f"declared={declared_sha!r} actual={actual_sha!r}"
        )

    registry = pd.read_csv(V551_REGISTRY_PATH, dtype=str).fillna("")
    required = {
        "response_semantics_contract_hash",
        "authority_status",
        "review_status",
    }
    missing = sorted(required - set(registry.columns))
    if missing:
        raise ValueError(f"V551 response-scale registry missing columns: {missing}")

    hashes = registry["response_semantics_contract_hash"].map(_clean)
    if hashes.eq("").any():
        raise ValueError("V551 response-scale registry contains blank contract key")
    if hashes.duplicated().any():
        raise ValueError("V551 response-scale registry contains duplicate contract key")
    if not registry["authority_status"].map(_clean).eq("CERTIFIED").all():
        raise ValueError("V551 response-scale registry contains uncertified authority")
    if not registry["review_status"].map(_clean).eq("NO_REVIEW").all():
        raise ValueError("V551 response-scale registry contains review-required authority")
    if len(registry) != EXPECTED_DISTINCT_CONTRACTS:
        raise ValueError(
            "unexpected V551 response-scale registry cardinality: "
            f"{len(registry)} != {EXPECTED_DISTINCT_CONTRACTS}"
        )
    return frozenset(hashes.tolist())


@lru_cache(maxsize=1)
def load_response_semantics_contract_bindings() -> dict[
    tuple[str, str, str], ResponseSemanticsContractBinding
]:
    if not BINDING_PATH.exists() or not BINDING_MANIFEST_PATH.exists():
        raise FileNotFoundError("V550->V551 response-semantics binding authority is missing")

    manifest = json.loads(BINDING_MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != BINDING_SCHEMA_VERSION:
        raise ValueError(
            "unsupported V550->V551 response-semantics binding schema: "
            f"{manifest.get('schema_version')!r}"
        )
    declared_sha = _clean(manifest.get("binding_file_sha256"))
    actual_sha = _sha256(BINDING_PATH)
    if not declared_sha or actual_sha != declared_sha:
        raise ValueError(
            "V550->V551 response-semantics binding SHA-256 mismatch: "
            f"declared={declared_sha!r} actual={actual_sha!r}"
        )

    frame = pd.read_csv(BINDING_PATH, dtype=str).fillna("")
    missing = [column for column in REQUIRED_BINDING_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"response-semantics binding missing columns: {missing}")
    if len(frame) != EXPECTED_ACTIVE_BINDINGS:
        raise ValueError(
            "unexpected response-semantics binding row count: "
            f"{len(frame)} != {EXPECTED_ACTIVE_BINDINGS}"
        )
    v551_keys = load_v551_registry_key_set()
    sorted_v551_keys = sorted(v551_keys)
    out: dict[tuple[str, str, str], ResponseSemanticsContractBinding] = {}
    for row in frame.itertuples(index=False):
        try:
            registry_key_index = int(float(_clean(row.v551_registry_key_index)))
        except Exception as exc:
            raise ValueError(
                "binding authority contains invalid v551_registry_key_index: "
                f"{row.v551_registry_key_index!r}"
            ) from exc
        if registry_key_index < 0 or registry_key_index >= len(sorted_v551_keys):
            raise ValueError(
                "binding authority references V551 registry key index out of range: "
                f"{registry_key_index}"
            )
        contract_hash = sorted_v551_keys[registry_key_index]
        key = _binding_key(row.source_family, row.canonical_wave, row.var_code)
        if not all(key):
            raise ValueError(f"binding authority contains incomplete exact key: {key!r}")
        if key in out:
            raise ValueError(f"duplicate exact response-semantics binding key: {key!r}")
        try:
            substantive_count = int(float(_clean(row.substantive_category_count)))
        except Exception as exc:
            raise ValueError(
                f"invalid substantive_category_count for {key!r}: "
                f"{row.substantive_category_count!r}"
            ) from exc
        out[key] = ResponseSemanticsContractBinding(
            source_family=_clean(row.source_family),
            canonical_wave=_clean(row.canonical_wave),
            var_code=_clean(row.var_code),
            response_semantics_contract_hash=contract_hash,
            substantive_category_count=substantive_count,
        )

    distinct = {binding.response_semantics_contract_hash for binding in out.values()}
    if len(distinct) != EXPECTED_DISTINCT_CONTRACTS:
        raise ValueError(
            "response-semantics binding does not span the frozen V551 key set: "
            f"{len(distinct)} != {EXPECTED_DISTINCT_CONTRACTS}"
        )
    if distinct != set(v551_keys):
        missing_from_producer = sorted(set(v551_keys) - distinct)
        extra_from_producer = sorted(distinct - set(v551_keys))
        raise ValueError(
            "V550/V551 response-semantics compatibility failure: "
            f"missing={missing_from_producer} extra={extra_from_producer}"
        )
    return out


def lookup_governed_response_semantics_contract(
    source: Any, wave: Any, var_code: Any
) -> ResponseSemanticsContractBinding | None:
    return load_response_semantics_contract_bindings().get(
        _binding_key(source, wave, var_code)
    )


def _append_reason(existing: Any, reason: str) -> str:
    tokens = [token for token in _clean(existing).split("|") if token]
    if reason not in tokens:
        tokens.append(reason)
    return "|".join(tokens)


def _mark_group_unresolved(
    out: pd.DataFrame,
    indices: list[int],
    reason: str,
) -> None:
    out.loc[indices, "response_semantics_contract_hash"] = ""
    out.loc[indices, "response_semantics_status"] = (
        "REVIEW_REQUIRED_UNRESOLVED_GOVERNED_CONTRACT"
    )
    out.loc[indices, "response_semantics_source"] = (
        "v550_v551_response_semantics_contract_binding_v1"
    )
    out.loc[indices, "response_semantics_authority_status"] = "REVIEW_REQUIRED"
    out.loc[indices, "manual_review_flag"] = True
    for idx in indices:
        out.at[idx, "manual_review_reason"] = _append_reason(
            out.at[idx, "manual_review_reason"],
            reason,
        )


def bind_governed_response_semantics_contracts(
    frame: pd.DataFrame,
    *,
    live_build: bool,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Bind exact frozen contract identities at the governed question grain.

    Existing certified keys are preserved.  Live codebook rows receive a key
    only when an exact `(source_family, canonical_wave, var_code)` binding
    exists and the locally materialized substantive geometry is complete
    enough to match the frozen validation row count.  Unknown/conflicting
    semantics remain blank and explicitly review-required.
    """
    out = frame.copy()
    if out.empty:
        return out, {
            "applicable_groups": 0,
            "bound_groups": 0,
            "preserved_groups": 0,
            "review_required_groups": 0,
            "unresolved_groups": 0,
        }

    for column, default in [
        ("response_semantics_contract_hash", ""),
        ("response_semantics_status", ""),
        ("response_semantics_source", ""),
        ("response_semantics_authority_status", ""),
        ("manual_review_flag", False),
        ("manual_review_reason", ""),
    ]:
        if column not in out.columns:
            out[column] = default

    bindings = load_response_semantics_contract_bindings()
    registry_keys = load_v551_registry_key_set()
    groups: dict[tuple[str, str, str], list[int]] = {}
    for idx, row in out.iterrows():
        source = _clean(row.get("source_family")) or _clean(row.get("source"))
        wave = _clean(row.get("canonical_wave")) or _clean(row.get("wave"))
        var_code = _clean(row.get("var_code")) or _clean(row.get("var_name"))
        key = _binding_key(source, wave, var_code)
        groups.setdefault(key, []).append(idx)

    summary = {
        "applicable_groups": 0,
        "bound_groups": 0,
        "preserved_groups": 0,
        "review_required_groups": 0,
        "unresolved_groups": 0,
    }

    for key, indices in groups.items():
        binding = bindings.get(key)
        existing_hashes = {
            _clean(value)
            for value in out.loc[indices, "response_semantics_contract_hash"].tolist()
            if _clean(value)
        }

        if binding is None:
            # Preserve an already-governed prebuilt key; never mint one from
            # map-level content or response family.
            if existing_hashes and existing_hashes.issubset(registry_keys):
                continue
            if existing_hashes:
                _mark_group_unresolved(
                    out,
                    indices,
                    "response_semantics_contract_not_in_frozen_v551_registry",
                )
                summary["review_required_groups"] += 1
                summary["unresolved_groups"] += 1
            continue

        summary["applicable_groups"] += 1
        expected = binding.response_semantics_contract_hash
        if existing_hashes == {expected}:
            summary["preserved_groups"] += 1
            continue
        if existing_hashes and not live_build:
            _mark_group_unresolved(
                out,
                indices,
                "prebuilt_response_semantics_contract_conflicts_with_governed_binding",
            )
            summary["review_required_groups"] += 1
            summary["unresolved_groups"] += 1
            continue

        substantive_mask = out.loc[indices, "is_substantive"].map(_truthy)
        substantive = out.loc[list(pd.Index(indices)[substantive_mask.to_numpy()])]
        if len(substantive) != binding.substantive_category_count:
            _mark_group_unresolved(
                out,
                indices,
                "governed_response_semantics_substantive_count_mismatch",
            )
            summary["review_required_groups"] += 1
            summary["unresolved_groups"] += 1
            continue

        direction_complete = True
        if not substantive.empty:
            if "response_direction" not in substantive.columns:
                direction_complete = False
            elif substantive["response_direction"].map(_clean).eq("").any():
                direction_complete = False
            if "response_intensity" not in substantive.columns:
                direction_complete = False
            elif substantive["response_intensity"].map(_clean).eq("").any():
                direction_complete = False
        if not direction_complete:
            _mark_group_unresolved(
                out,
                indices,
                "governed_response_semantics_direction_or_intensity_unresolved",
            )
            summary["review_required_groups"] += 1
            summary["unresolved_groups"] += 1
            continue

        out.loc[indices, "response_semantics_contract_hash"] = expected
        out.loc[indices, "response_semantics_status"] = "CERTIFIED_GOVERNED_CONTRACT"
        out.loc[indices, "response_semantics_source"] = (
            "v550_v551_response_semantics_contract_binding_v1"
        )
        out.loc[indices, "response_semantics_authority_status"] = "CERTIFIED"
        summary["bound_groups"] += 1

    return out, summary


def assert_v551_applicable_contract_compatibility(frame: pd.DataFrame) -> dict[str, int]:
    """Mechanical producer/consumer key compatibility assertion.

    Only exact governed V551-applicable bindings are asserted here.  The
    downstream V551 compiler remains authoritative for projection semantics.
    """
    bindings = load_response_semantics_contract_bindings()
    registry = load_v551_registry_key_set()
    applicable = 0
    unresolved = 0
    for key, binding in bindings.items():
        source_family, canonical_wave, var_code = key
        mask = pd.Series(True, index=frame.index)
        source_series = (
            frame["source_family"] if "source_family" in frame.columns else frame.get("source", "")
        )
        wave_series = (
            frame["canonical_wave"] if "canonical_wave" in frame.columns else frame.get("wave", "")
        )
        var_series = frame["var_code"] if "var_code" in frame.columns else frame.get("var_name", "")
        if not isinstance(source_series, pd.Series) or not isinstance(wave_series, pd.Series) or not isinstance(var_series, pd.Series):
            continue
        mask &= source_series.map(canonical_family_key).eq(source_family)
        mask &= wave_series.map(
            lambda value: (canonical_wave_key(source_family, _clean(value)) or _clean(value)).upper()
        ).eq(canonical_wave)
        mask &= var_series.map(lambda value: _clean(value).lower()).eq(var_code)
        subset = frame.loc[mask]
        if subset.empty:
            continue
        applicable += 1
        hashes = {
            _clean(value)
            for value in subset.get("response_semantics_contract_hash", pd.Series(dtype=str)).tolist()
            if _clean(value)
        }
        if hashes != {binding.response_semantics_contract_hash}:
            unresolved += 1
            continue
        if next(iter(hashes)) not in registry:
            unresolved += 1
    if unresolved:
        raise ValueError(
            "V551-applicable response-semantics contracts failed exact registry compatibility: "
            f"{unresolved}/{applicable}"
        )
    return {"applicable_groups": applicable, "unresolved_groups": unresolved}
