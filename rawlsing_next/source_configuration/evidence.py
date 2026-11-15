"""Read-only access to the portable R157 evidence package."""
from __future__ import annotations

import gzip
import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping

from .errors import SourceConfigurationEvidenceError

EVIDENCE_DIR = Path(__file__).resolve().parent / "evidence"
ROSTER_PATH = EVIDENCE_DIR / "SOURCE_ROSTER.json"
MANIFEST_PATH = EVIDENCE_DIR / "EVIDENCE_MANIFEST.json"
PHYSICAL_PATH = EVIDENCE_DIR / "PHYSICAL_SLOTS.jsonl.gz"
CODEBOOK_PATH = EVIDENCE_DIR / "CODEBOOK_ROWS.jsonl.gz"
ITEM_PATH = EVIDENCE_DIR / "ITEM_EVIDENCE.jsonl.gz"
UNMATCHED_PATH = EVIDENCE_DIR / "UNMATCHED_RELATIONS.json"
P2_PATH = EVIDENCE_DIR / "P2_PHASE0.csv.gz"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def load_manifest() -> Mapping[str, Any]:
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SourceConfigurationEvidenceError(f"cannot read evidence manifest: {exc}") from exc


@lru_cache(maxsize=1)
def load_source_roster() -> Mapping[str, Any]:
    try:
        return json.loads(ROSTER_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SourceConfigurationEvidenceError(f"cannot read source roster: {exc}") from exc


def roster_by_source() -> dict[str, Mapping[str, Any]]:
    return {entry["source_id"]: entry for entry in load_source_roster()["sources"]}


def source_roster_entry(source_id: str) -> Mapping[str, Any]:
    try:
        return roster_by_source()[source_id]
    except KeyError as exc:
        raise SourceConfigurationEvidenceError(f"unknown source id {source_id!r}") from exc


def verify_evidence_manifest() -> dict[str, Any]:
    """Verify the on-disk portable files against the pinned manifest."""
    manifest = load_manifest()
    failures = []
    for name, expected in manifest["files"].items():
        path = EVIDENCE_DIR / name
        if not path.is_file():
            failures.append(f"missing:{name}")
            continue
        raw = path.read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        if actual != expected["sha256"] or len(raw) != expected["bytes"]:
            failures.append(f"hash_or_bytes:{name}")
    counts = manifest["counts"]
    if counts != {
        "codebook_only": 401,
        "codebook_rows": 18276,
        "exact_relation_joins": 18250,
        "original_items": 18276,
        "physical_columns": 18413,
        "physical_only": 538,
        "relation_rows_not_imported": 268,
        "relation_rows_total": 18518,
        "sources": 35,
        "unmatched_explicit_ids": 26,
    }:
        failures.append("counts")
    roster = load_source_roster()
    if roster["counts"]["sources"] != 35 or len(roster["sources"]) != 35:
        failures.append("roster35")
    return {"ok": not failures, "failures": failures, "manifest": manifest}


def _iter_gzip_jsonl(path: Path) -> Iterable[Mapping[str, Any]]:
    try:
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)
    except (OSError, json.JSONDecodeError) as exc:
        raise SourceConfigurationEvidenceError(f"cannot read {path.name}: {exc}") from exc


def iter_physical_slots(source_id: str | None = None) -> Iterable[Mapping[str, Any]]:
    for row in _iter_gzip_jsonl(PHYSICAL_PATH):
        if source_id is None or row["source_id"] == source_id:
            yield row


def iter_codebook_rows(source_id: str | None = None) -> Iterable[Mapping[str, Any]]:
    for row in _iter_gzip_jsonl(CODEBOOK_PATH):
        if source_id is None or row["source_id"] == source_id:
            yield row


def iter_item_evidence(source_id: str | None = None) -> Iterable[Mapping[str, Any]]:
    for row in _iter_gzip_jsonl(ITEM_PATH):
        if source_id is None or row["source_id"] == source_id:
            yield row


def load_unmatched_relations() -> Mapping[str, Any]:
    try:
        return json.loads(UNMATCHED_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SourceConfigurationEvidenceError(f"cannot read unmatched relations: {exc}") from exc


def lane_inputs(lane_id: str) -> dict[str, Any]:
    """Return the frozen evidence/interface inputs for a LANES.json lane."""
    lanes = json.loads((Path(__file__).resolve().parents[2] / "SOURCE_PRE553_PLAN/LANES.json").read_text(encoding="utf-8"))
    lane = next((x for x in lanes["lanes"] if x["lane_id"] == lane_id), None)
    if lane is None:
        raise SourceConfigurationEvidenceError(f"unknown lane {lane_id!r}")
    return {
        "lane_id": lane_id,
        "branch": lane["branch"],
        "source_ids": lane["source_ids"],
        "write_paths": lane["write_paths"],
        "shared_schema_and_factory": lane["shared_schema_and_factory"],
        "evidence": {
            "source_roster": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
            "physical_slots": "rawlsing_next/source_configuration/evidence/PHYSICAL_SLOTS.jsonl.gz",
            "codebook_rows": "rawlsing_next/source_configuration/evidence/CODEBOOK_ROWS.jsonl.gz",
            "item_evidence": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
            "unmatched_relations": "rawlsing_next/source_configuration/evidence/UNMATCHED_RELATIONS.json",
            "manifest": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
        },
        "config_contract": {
            "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
            "schema_module": "rawlsing_next.source_configuration.schema",
            "validator": "rawlsing_next.source_configuration.schema.validate_source_config",
            "loader": "rawlsing_next.source_configuration.schema.load_source_config",
            "factory": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "release": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "repository": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
        },
        "stage_queue": lane["stage_queue"],
    }
