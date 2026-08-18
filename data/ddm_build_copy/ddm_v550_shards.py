#!/usr/bin/env python3
"""Shard planning and shard-path helpers for V550 Pax execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    validate_source_wave_identity_coherence,
)
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity
from data.ddm_build_copy.ddm_v550_manifest import utc_now


V550_IDENTITY_TRANSPORT_VERSION = "v550-source-wave-uid-1"


def slugify(value: str) -> str:
    out = "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in str(value))
    out = out.strip("_")
    return out or "item"


def shard_id_for(source: str, wave: str) -> str:
    """Return the frozen historical V550 shard id.

    Source/wave UIDs are deliberately not incorporated here. Historical shard
    ids, checkpoint paths, and cache spellings remain physical compatibility
    surfaces under the source-wave identity campaign.
    """
    return f"{slugify(source)}__{slugify(wave)}"


def require_v550_execution_identity(
    source: str,
    wave: str,
    *,
    expected_source_family_uid: str = "",
    expected_wave_uid: str = "",
    redundant_identity: Mapping[str, Any] | None = None,
):
    """Resolve one governed CLOSED_35 V550 execution identity fail-closed.

    The W01 kernel owns recognition and authorization. W05 owns redundant
    identity coherence. This W03 helper only composes those frozen contracts at
    the V550 execution boundary.
    """
    identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
    if expected_source_family_uid and identity.source_family_uid != str(expected_source_family_uid).strip():
        raise BoundaryContractError(
            "V550_SOURCE_FAMILY_UID_MISMATCH:"
            f"expected={str(expected_source_family_uid).strip()}:actual={identity.source_family_uid}"
        )
    if expected_wave_uid and identity.wave_uid != str(expected_wave_uid).strip():
        raise BoundaryContractError(
            "V550_WAVE_UID_MISMATCH:"
            f"expected={str(expected_wave_uid).strip()}:actual={identity.wave_uid}"
        )
    if redundant_identity is not None:
        coherence = validate_source_wave_identity_coherence(
            redundant_identity,
            expected_source=source,
            expected_wave=wave,
            expected_source_family_uid=identity.source_family_uid,
            expected_wave_uid=identity.wave_uid,
            require_complete=True,
        )
        if coherence.source_family_uid != identity.source_family_uid or coherence.wave_uid != identity.wave_uid:
            raise BoundaryContractError(
                "V550_REDUNDANT_IDENTITY_MISMATCH:"
                f"resolved={coherence.source_family_uid}/{coherence.wave_uid}:"
                f"execution={identity.source_family_uid}/{identity.wave_uid}"
            )
    return identity


def v550_identity_fields(source: str, wave: str) -> dict[str, Any]:
    """Return additive governed identity fields without changing raw coordinates."""
    identity = require_v550_execution_identity(source, wave)
    return {
        "raw_source": str(source),
        "raw_wave": str(wave),
        "raw_db_source": str(source),
        "raw_db_wave": str(wave),
        "canonical_display_source": identity.canonical_display_source,
        "canonical_display_wave": identity.canonical_display_wave,
        "source_family_uid": identity.source_family_uid,
        "wave_uid": identity.wave_uid,
        "governance_state": identity.governance_state,
        "closed_35_member": bool(identity.closed_35_member),
        "identity_transport_version": V550_IDENTITY_TRANSPORT_VERSION,
    }


@dataclass
class ShardPlanRow:
    run_id: str
    source: str
    source_family: str
    wave: str
    canonical_wave: str
    countries: list[str]
    country_count: int
    respondent_count: int
    response_row_count: int
    mapped_row_count: int
    facet_row_count: int
    position_field_count: int
    weight_status: str
    readiness_status: str
    skip_by_default: bool
    skip_reason: str | None
    estimated_question_count: int
    output_dir: str
    shard_id: str
    command: str
    source_family_uid: str = ""
    wave_uid: str = ""
    governance_state: str = ""
    closed_35_member: bool = False
    raw_db_source: str = ""
    raw_db_wave: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "created_at": utc_now(),
            "source": self.source,
            "source_family": self.source_family,
            "wave": self.wave,
            "canonical_wave": self.canonical_wave,
            "source_family_uid": self.source_family_uid,
            "wave_uid": self.wave_uid,
            "governance_state": self.governance_state,
            "closed_35_member": self.closed_35_member,
            "raw_db_source": self.raw_db_source or self.source,
            "raw_db_wave": self.raw_db_wave or self.wave,
            "countries": self.countries,
            "country_count": self.country_count,
            "respondent_count": self.respondent_count,
            "response_row_count": self.response_row_count,
            "mapped_row_count": self.mapped_row_count,
            "facet_row_count": self.facet_row_count,
            "position_field_count": self.position_field_count,
            "weight_status": self.weight_status,
            "readiness_status": self.readiness_status,
            "skip_by_default": self.skip_by_default,
            "skip_reason": self.skip_reason,
            "estimated_question_count": self.estimated_question_count,
            "output_dir": self.output_dir,
            "shard_id": self.shard_id,
            "command": self.command,
        }


def plan_dataframe_to_json(plan_df: pd.DataFrame, *, run_id: str, planner_version: str, repo_root: Path, db_used: bool, filters: dict[str, list[str]], thresholds: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "created_at": utc_now(),
        "planner_version": planner_version,
        "repo_root": str(repo_root),
        "db_used": db_used,
        "filters": filters,
        "thresholds": thresholds,
        "shards": plan_df.to_dict(orient="records"),
    }
