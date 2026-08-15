#!/usr/bin/env python3
"""Shard planning and shard-path helpers for V550 Pax execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now


def slugify(value: str) -> str:
    out = "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in str(value))
    out = out.strip("_")
    return out or "item"


def shard_id_for(source: str, wave: str) -> str:
    return f"{slugify(source)}__{slugify(wave)}"


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

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "created_at": utc_now(),
            "source": self.source,
            "source_family": self.source_family,
            "wave": self.wave,
            "canonical_wave": self.canonical_wave,
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
