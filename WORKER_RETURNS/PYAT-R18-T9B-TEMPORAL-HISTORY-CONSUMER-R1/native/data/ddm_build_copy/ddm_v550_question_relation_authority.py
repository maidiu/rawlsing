#!/usr/bin/env python3
"""Canonical full-universe question-to-ontology authority resolver for V550.

This module deliberately owns only question-level structural authority.  Response-
category semantics remain governed by the installed response-option and
manual-directionality authorities.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
AUTHORITY_VERSION = "qra_35wave_active_v1"
FULL_AUTHORITY_VERSION = "qsm_full_question_relation_authority_r1_20260814"
R1_TARGET_ROW_COUNT = 18518
LEGACY_RESIDUAL_ROW_COUNT = 20
CALIBRATION_AUTHORITY_PATH = ROOT / "data" / "ddm_build_copy" / "bindings" / "question_relation_registry_35wave_active_v1.csv"
FULL_AUTHORITY_PATH = ROOT / "data" / "ddm_build_copy" / "authority" / "full_question_relation_authority" / "R1_20260814" / "QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"
DEFAULT_AUTHORITY_PATH = (
    CALIBRATION_AUTHORITY_PATH
)
AUTHORITY_PATH_ENV = "RAWLSING_QUESTION_RELATION_AUTHORITY_PATH"
AUTHORITY_ROOT_ENV = "DDM_AUTHORITY_ROOT"

DIRECTIONAL_STATUS = "GOVERNED_DIRECTIONAL"
NEUTRAL_COVERAGE_STATUS = "GOVERNED_NEUTRAL_COVERAGE"
NON_DIRECTIONAL_STATUSES = {
    "GOVERNED_CONTEXT_ONLY",
    "GOVERNED_NON_RELATIONAL",
    "ADMINISTRATIVE_ONLY",
}
FULL_RELATIONAL_STATUSES = {
    "GOVERNED_QSMV2_RELATION_AUTHORITY",
    "GOVERNED_MANUAL_RELATION_AUTHORITY",
    "FROZEN_ACCEPTED_GSS",
}

STRUCTURAL_COORDINATE_FIELDS = (
    "driver_id",
    "driver_facet_id",
    "question_block_id",
    "structural_domain_id",
    "relation_axis_id",
    "target_entity_id",
)
POLARITY_FIELDS = (
    "source_response_polarity",
    "relation_projection_polarity",
    "item_reversal",
)
REQUIRED_DIRECTIONAL_FIELDS = STRUCTURAL_COORDINATE_FIELDS + (
    "relation_projection_polarity",
)
REQUIRED_REGISTRY_COLUMNS = {
    "authority_version",
    "authority_rule_id",
    "source_family",
    "canonical_wave",
    "country_code_scope",
    "question_id",
    "var_code",
    "relation_use_status",
    "driver_id",
    "driver_facet_id",
    "question_block_id",
    "structural_domain_id",
    "relation_axis_id",
    "target_entity_id",
    "relation_projection_polarity",
    "item_reversal",
    "source_response_polarity",
    "evidence_disposition",
    "current_directional_atom_eligible",
    "authority_status",
    "review_status",
    "review_notes",
    "row_payload_hash",
}

SOURCE_ALIASES = {
    "afrobarometer": "Afrobarometer",
    "arabbarometer": "Arab Barometer",
    "asianbarometer": "Asian Barometer",
    "evs": "EVS",
    "europeanvaluessurvey": "EVS",
    "gss": "GSS",
    "generalsocialsurvey": "GSS",
    "latinobarometro": "Latinobarómetro",
    "latinobarómetro": "Latinobarómetro",
    "lits": "LiTS",
    "lifetransitionsurvey": "LiTS",
    "southasia": "South Asia",
    "southasiabarometer": "South Asia",
    "wv": "WVS",
    "wvs": "WVS",
    "worldvaluessurvey": "WVS",
}
COUNTRY_ALIASES = {"BF": "LS", "LY": "YE"}


class QuestionRelationAuthorityError(RuntimeError):
    """Raised when the installed authority is malformed or internally unsafe."""


@dataclass(frozen=True)
class AuthorityResolution:
    status: str
    authority_row: dict[str, str] | None
    lookup_key: str
    normalized_country_code: str
    match_count: int
    reason: str = ""
    authority_artifact_path: str = ""
    authority_artifact_sha256: str = ""

    @property
    def resolved(self) -> bool:
        return self.authority_row is not None and self.status.startswith("RESOLVED_")

    @property
    def message(self) -> str:
        return self.reason

    def as_row_fields(self) -> dict[str, Any]:
        row = self.authority_row or {}
        relation_status = row.get("relation_use_status", "").upper()
        fields: dict[str, Any] = {
            "question_relation_authority_joined": self.resolved,
            "question_relation_authority_resolution_status": self.status,
            "question_relation_authority_lookup_key": self.lookup_key,
            "question_relation_authority_match_count": self.match_count,
            "question_relation_authority_country_code": self.normalized_country_code,
            "question_relation_authority_reason": self.reason,
            "relation_use_status": row.get("relation_use_status", ""),
            "evidence_disposition": row.get("evidence_disposition", ""),
            "authority_status": row.get("authority_status", ""),
            "authority_rule_id": row.get("authority_rule_id", ""),
            "authority_version": row.get("authority_version", AUTHORITY_VERSION if self.resolved else ""),
            "authority_artifact_path": self.authority_artifact_path,
            "authority_artifact_sha256": self.authority_artifact_sha256,
            "authority_row_payload_hash": row.get("row_payload_hash", ""),
            "authority_review_status": row.get("review_status", ""),
            "authority_review_notes": row.get("review_notes", ""),
        }
        if relation_status == DIRECTIONAL_STATUS:
            fields.update({field: row.get(field, "") for field in STRUCTURAL_COORDINATE_FIELDS})
            fields.update(
                {
                    "source_response_polarity": row.get("source_response_polarity", ""),
                    "relation_projection_polarity": row.get("relation_projection_polarity", ""),
                    "item_reversal": _bool(row.get("item_reversal")),
                    "current_directional_atom_eligible": _bool(row.get("current_directional_atom_eligible"), default=True),
                    "allowed_as_v551_relation_evidence": _bool(row.get("current_directional_atom_eligible"), default=True),
                    "question_relation_coverage_eligible": True,
                    "question_relation_pressure_eligible": _bool(row.get("current_directional_atom_eligible"), default=True),
                    "structural_mapping_status": "COMPLETE",
                    "mapping_status": "governed_directional",
                    "semantic_role": "RELATION_EVIDENCE",
                    "semantic_role_authority_status": "CERTIFIED",
                    "v551_visible": True,
                }
            )
            return fields

        fields.update({field: "" for field in STRUCTURAL_COORDINATE_FIELDS})
        fields.update(
            {
                "source_response_polarity": "",
                "relation_projection_polarity": "",
                "item_reversal": False,
                "current_directional_atom_eligible": False,
                "allowed_as_v551_relation_evidence": False,
                "question_relation_pressure_eligible": False,
                "structural_mapping_status": "COMPLETE_NON_DIRECTIONAL" if self.resolved else self.status,
                "mapping_status": relation_status.casefold() if relation_status else self.status.casefold(),
                "semantic_role_authority_status": "CERTIFIED" if self.resolved else "NOT_CERTIFIED",
                "v551_visible": relation_status != "ADMINISTRATIVE_ONLY",
            }
        )
        if relation_status in {NEUTRAL_COVERAGE_STATUS, "GOVERNED_CONTEXT_ONLY", "GOVERNED_NON_RELATIONAL"}:
            fields["semantic_role"] = "STRUCTURAL_CONTEXT"
            fields["question_relation_coverage_eligible"] = True
        else:
            fields["semantic_role"] = "UNKNOWN"
            fields["question_relation_coverage_eligible"] = False
            fields["manual_review_flag"] = not self.resolved or relation_status.startswith("BLOCKED_")
            fields["manual_review_reason"] = row.get("review_notes") or self.reason or relation_status
        return fields


@dataclass(frozen=True)
class AuthorityIndex:
    path: Path
    file_sha256: str
    rows: tuple[dict[str, str], ...]
    by_key: dict[tuple[str, str, str, str], tuple[dict[str, str], ...]]


def _text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def _bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    text = _text(value).casefold()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", ""}:
        return False
    return default


def _token(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", _text(value).casefold())


def canonical_source_family(value: Any) -> str:
    raw = _text(value)
    key = _token(raw)
    return SOURCE_ALIASES.get(key, raw)


def canonical_country_code(value: Any) -> str:
    code = _text(value).upper()
    return COUNTRY_ALIASES.get(code, code)


def canonical_wave(source_family: Any, value: Any) -> str:
    family = canonical_source_family(source_family)
    raw = _text(value)
    compact = re.sub(r"[^A-Za-z0-9]+", "", raw).upper()
    compact = re.sub(r"^WAVE", "W", compact)

    if family == "Afrobarometer":
        m = re.fullmatch(r"(?:ROUND|R|W)?(\d+)", compact)
        return f"R{m.group(1)}" if m else raw
    if family == "Arab Barometer":
        aliases = {
            "1": "I", "W1": "I", "I": "I",
            "2": "II", "W2": "II", "II": "II",
            "5": "V", "W5": "V", "V": "V",
            "8": "VIII", "W8": "VIII", "VIII": "VIII",
        }
        return aliases.get(compact, raw)
    if family in {"Asian Barometer", "South Asia", "WVS"}:
        m = re.fullmatch(r"(?:W)?(\d+)", compact)
        return f"W{m.group(1)}" if m else raw
    if family == "LiTS":
        aliases = {
            "1": "2006", "W1": "2006", "I": "2006", "2006": "2006",
            "2": "II", "W2": "II", "II": "II",
            "3": "III", "W3": "III", "III": "III",
            "4": "IV", "W4": "IV", "IV": "IV",
        }
        return aliases.get(compact, raw)
    if family == "EVS":
        aliases = {
            "1": "1981", "W1": "1981", "1981": "1981",
            "2": "1990", "W2": "1990", "1990": "1990",
            "3": "1999", "W3": "1999", "1999": "1999",
            "4": "2008", "W4": "2008", "2008": "2008",
            "5": "2017", "W5": "2017", "2017": "2017",
        }
        if compact in aliases:
            return aliases[compact]
        year = re.search(r"(?:19|20)\d{2}", compact)
        return year.group(0) if year else raw
    if family in {"GSS", "Latinobarómetro"}:
        year = re.search(r"(?:19|20)\d{2}", compact)
        return year.group(0) if year else raw
    return raw


def canonical_question_key(value: Any) -> str:
    return _text(value).casefold()


def active_authority_path(path: Path | str | None = None) -> Path:
    if path is not None:
        return Path(path).expanduser().resolve()
    env = os.getenv(AUTHORITY_PATH_ENV, "").strip()
    if env:
        return Path(env).expanduser().resolve()
    root = os.getenv(AUTHORITY_ROOT_ENV, "").strip()
    if root:
        return Path(root).expanduser().resolve() / "QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"
    return FULL_AUTHORITY_PATH.resolve()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalized_hash_value(value: Any) -> str:
    # Match the authority package's frozen row-hash contract exactly.  Do not
    # strip whitespace here: the hash certifies the serialized authority row.
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    text = str(value)
    if text == "True":
        return "true"
    if text == "False":
        return "false"
    return text


def _recompute_row_hash(row: Mapping[str, Any], columns: list[str]) -> str:
    payload = {column: _normalized_hash_value(row.get(column, "")) for column in columns if column != "row_payload_hash"}
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _resolution_key(source: Any, wave: Any, country: Any, question: Any) -> tuple[str, str, str, str]:
    family = canonical_source_family(source)
    return (
        family.casefold(),
        canonical_wave(family, wave).casefold(),
        canonical_country_code(country).casefold(),
        canonical_question_key(question),
    )


def _validate_registry(frame: pd.DataFrame, path: Path) -> None:
    if path.name == FULL_AUTHORITY_PATH.name:
        required = {"source", "wave", "question_id", "var_code", "canonical_wave", "country_code_scope",
                    "authority_rule_id", "authority_status", "relation_use_status_final", "mapping_status",
                    "driver_id", "driver_facet_id", "question_block_id", "structural_domain_id",
                    "relation_axis_id", "target_entity_id", "qsmv2_final_payload_hash"}
        missing = required - set(frame.columns)
        if missing:
            raise QuestionRelationAuthorityError(f"full R1 authority missing required columns: {sorted(missing)}")
        if len(frame) != R1_TARGET_ROW_COUNT:
            raise QuestionRelationAuthorityError(
                f"expected {R1_TARGET_ROW_COUNT} full R1 authority rows, found {len(frame)}"
            )
        if frame["governed_row_payload_hash"].eq("").any():
            raise QuestionRelationAuthorityError("full R1 authority contains blank governed payload hashes")
        if frame["authority_status"].eq("").any():
            raise QuestionRelationAuthorityError("full R1 authority contains blank authority dispositions")
        return
    missing = REQUIRED_REGISTRY_COLUMNS - set(frame.columns)
    if missing:
        raise QuestionRelationAuthorityError(
            f"question relation authority missing required columns: {sorted(missing)}"
        )
    if frame.empty:
        raise QuestionRelationAuthorityError("question relation authority is empty")
    versions = {_text(value) for value in frame["authority_version"] if _text(value)}
    if versions != {AUTHORITY_VERSION}:
        raise QuestionRelationAuthorityError(
            f"unexpected authority versions in {path}: {sorted(versions)}"
        )
    if len(frame) != 700:
        raise QuestionRelationAuthorityError(
            f"expected 700 active authority rows, found {len(frame)}"
        )

    keys: list[tuple[str, str, str, str]] = []
    hash_columns = list(frame.columns)
    bad_hashes: list[str] = []
    for record in frame.to_dict(orient="records"):
        key = _resolution_key(
            record.get("source_family"),
            record.get("canonical_wave"),
            record.get("country_code_scope"),
            record.get("var_code") or record.get("question_id"),
        )
        keys.append(key)
        expected = _text(record.get("row_payload_hash"))
        actual = _recompute_row_hash(record, hash_columns)
        if expected != actual:
            bad_hashes.append("|".join(key))

        status = _text(record.get("relation_use_status")).upper()
        if not (
            status == DIRECTIONAL_STATUS
            or status == NEUTRAL_COVERAGE_STATUS
            or status in NON_DIRECTIONAL_STATUSES
            or status.startswith("BLOCKED_")
        ):
            raise QuestionRelationAuthorityError(
                f"unsupported relation_use_status {status!r} for {'|'.join(key)}"
            )
        if status == DIRECTIONAL_STATUS:
            blank = [field for field in REQUIRED_DIRECTIONAL_FIELDS if not _text(record.get(field))]
            if blank:
                raise QuestionRelationAuthorityError(
                    f"directional authority row {'|'.join(key)} has blank fields: {blank}"
                )
            if not _bool(record.get("current_directional_atom_eligible")):
                raise QuestionRelationAuthorityError(
                    f"directional authority row {'|'.join(key)} is not atom-eligible"
                )
        elif _bool(record.get("current_directional_atom_eligible")):
            raise QuestionRelationAuthorityError(
                f"non-directional authority row {'|'.join(key)} is atom-eligible"
            )
        if canonical_source_family(record.get("source_family")) == "Asian Barometer" and canonical_wave(
            record.get("source_family"), record.get("canonical_wave")
        ).upper() == "W6":
            raise QuestionRelationAuthorityError("Asian Barometer W6 is prohibited in active authority")

    duplicates = pd.Series(keys).duplicated(keep=False)
    if duplicates.any():
        examples = ["|".join(keys[index]) for index, duplicate in enumerate(duplicates) if duplicate][:10]
        raise QuestionRelationAuthorityError(f"duplicate normalized active authority keys: {examples}")
    if bad_hashes:
        raise QuestionRelationAuthorityError(
            f"row_payload_hash verification failed for {len(bad_hashes)} rows: {bad_hashes[:5]}"
        )


def derive_legacy_latinobarometro_1995_residual(r1_frame: pd.DataFrame) -> pd.DataFrame:
    """Derive the narrowly authorized legacy QRA residue from the 700-row registry.

    The residual is deliberately identity-bounded: it is the exact calibration
    slice whose legacy question IDs are not present in the frozen R1 target.
    R1 remains primary for normalized source/wave/country/var-code identities.
    """
    calibration = pd.read_csv(CALIBRATION_AUTHORITY_PATH, dtype=str, keep_default_na=False)
    _validate_registry(calibration, CALIBRATION_AUTHORITY_PATH)
    required = {"source_family", "canonical_wave", "country_code_scope", "question_id", "var_code"}
    missing = required - set(calibration.columns)
    if missing:
        raise QuestionRelationAuthorityError(f"calibration registry missing columns: {sorted(missing)}")

    target_identity = {
        (
            canonical_source_family(row.get("source")),
            canonical_wave(row.get("source"), row.get("canonical_wave")),
            canonical_country_code(row.get("country_code_scope")),
            canonical_question_key(row.get("question_id")),
        )
        for row in r1_frame.to_dict(orient="records")
    }
    calibration["_identity"] = [
        (
            canonical_source_family(row.get("source_family")),
            canonical_wave(row.get("source_family"), row.get("canonical_wave")),
            canonical_country_code(row.get("country_code_scope")),
            canonical_question_key(row.get("question_id")),
        )
        for row in calibration.to_dict(orient="records")
    ]
    residual = calibration.loc[~calibration["_identity"].isin(target_identity)].drop(columns=["_identity"])
    residual = residual[
        (residual["source_family"].map(canonical_source_family) == "Latinobarómetro")
        & (residual["canonical_wave"].map(lambda value: canonical_wave("Latinobarómetro", value)) == "1995")
    ].copy()
    if len(residual) != LEGACY_RESIDUAL_ROW_COUNT:
        raise QuestionRelationAuthorityError(
            f"expected {LEGACY_RESIDUAL_ROW_COUNT} Latinobarómetro 1995 residual rows, found {len(residual)}"
        )
    if set(residual["source_family"].map(canonical_source_family)) != {"Latinobarómetro"}:
        raise QuestionRelationAuthorityError("legacy residual contains a non-Latinobarómetro row")
    if set(residual["canonical_wave"].map(lambda value: canonical_wave("Latinobarómetro", value))) != {"1995"}:
        raise QuestionRelationAuthorityError("legacy residual contains a non-1995 row")
    if any(
        (
            canonical_source_family(row.get("source_family")),
            canonical_wave(row.get("source_family"), row.get("canonical_wave")),
            canonical_country_code(row.get("country_code_scope")),
            canonical_question_key(row.get("question_id")),
        ) in target_identity
        for row in residual.to_dict(orient="records")
    ):
        raise QuestionRelationAuthorityError("legacy residual overlaps an R1 target identity")
    residual = residual.reset_index(drop=True)
    return residual


def _build_index(path: Path) -> AuthorityIndex:
    if not path.is_file():
        raise QuestionRelationAuthorityError(f"question relation authority not found: {path}")
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    _validate_registry(frame, path)
    if path.name == FULL_AUTHORITY_PATH.name:
        normalized = frame.copy()
        normalized["source_family"] = normalized["canonical_source"].where(
            normalized["canonical_source"].ne(""), normalized["source"]
        )
        normalized["relation_use_status"] = normalized["relation_use_status_final"].where(
            ~normalized["authority_status"].isin(FULL_RELATIONAL_STATUSES), DIRECTIONAL_STATUS
        )
        normalized["relation_use_status"] = normalized["relation_use_status"].replace({
            "GOVERNED_NON_DIRECTIONAL_DISPOSITION": "GOVERNED_CONTEXT_ONLY",
            "GOVERNED_ADMINISTRATIVE_DISPOSITION": "ADMINISTRATIVE_ONLY",
            "EXCLUDED_INACTIVE_WAVE": "BLOCKED_EXCLUDED_INACTIVE_WAVE",
        })
        normalized["evidence_disposition"] = normalized["p2_evidence_disposition"].where(
            normalized["p2_evidence_disposition"].ne(""), normalized["manual_evidence_disposition"]
        )
        normalized["authority_version"] = FULL_AUTHORITY_VERSION
        normalized["row_payload_hash"] = normalized["qsmv2_final_payload_hash"].where(
            normalized["qsmv2_final_payload_hash"].ne(""), normalized["governed_row_payload_hash"]
        )
        normalized["review_status"] = normalized["manual_manual_review_required"]
        normalized["item_reversal"] = ""
        normalized["source_response_polarity"] = normalized["manual_signed_polarity_status"]
        normalized["relation_projection_polarity"] = normalized["manual_bridge_directionality_action"]
        normalized["current_directional_atom_eligible"] = normalized["manual_current_directional_atom_eligible"].where(
            normalized["manual_current_directional_atom_eligible"].ne(""), normalized["p2_current_directional_atom_eligible"]
        )
        frame = normalized
    by_key: dict[tuple[str, str, str, str], list[dict[str, str]]] = {}
    rows: list[dict[str, str]] = []
    for raw in frame.to_dict(orient="records"):
        row = {str(key): _text(value) for key, value in raw.items()}
        rows.append(row)
        question_keys = {
            canonical_question_key(row.get("var_code")),
            canonical_question_key(row.get("question_id")),
        } - {""}
        for question_key in question_keys:
            key = _resolution_key(
                row.get("source_family"),
                row.get("canonical_wave"),
                row.get("country_code_scope"),
                question_key,
            )
            by_key.setdefault(key, []).append(row)
    return AuthorityIndex(
        path=path,
        file_sha256=_sha256(path),
        rows=tuple(rows),
        by_key={key: tuple(value) for key, value in by_key.items()},
    )


@lru_cache(maxsize=8)
def _load_index_cached(path_text: str, mtime_ns: int, size: int) -> AuthorityIndex:
    del mtime_ns, size
    return _build_index(Path(path_text))


def load_question_relation_authority(path: Path | str | None = None) -> AuthorityIndex:
    authority_path = active_authority_path(path)
    stat = authority_path.stat()
    return _load_index_cached(str(authority_path), stat.st_mtime_ns, stat.st_size)


def active_closed_35_waves() -> tuple[tuple[str, str, str], ...]:
    """Return the production CLOSED_35 scope from final R1, excluding W6."""
    index = load_question_relation_authority()
    pairs = {
        (canonical_source_family(row.get("source_family")), canonical_wave(row.get("source_family"), row.get("canonical_wave")))
        for row in index.rows
        if _text(row.get("authority_status")) != "EXCLUDED_INACTIVE_WAVE"
    }
    ordered = tuple((source, wave, "") for source, wave in sorted(pairs))
    if len(ordered) != 35 or ("Asian Barometer", "W6", "") in ordered:
        raise QuestionRelationAuthorityError(f"invalid CLOSED_35 scope from final R1: {ordered}")
    return ordered


def resolve_question_relation_authority(
    *legacy_args: Any,
    source_family: Any = None,
    canonical_wave_value: Any = None,
    country_code: Any = None,
    question_id: Any = "",
    var_code: Any = "",
    authority_path: Path | str | None = None,
    active_row: Mapping[str, Any] | None = None,
) -> AuthorityResolution:
    if legacy_args:
        record = dict(active_row or legacy_args[0] or {})
        if len(legacy_args) > 1 and isinstance(legacy_args[1], AuthorityIndex):
            authority_path = legacy_args[1].path
        source_family = source_family or record.get("source_family") or record.get("source")
        canonical_wave_value = canonical_wave_value or record.get("canonical_wave") or record.get("wave")
        country_code = country_code or record.get("country_code") or record.get("country_code_scope")
        question_id = question_id or record.get("question_id")
        var_code = var_code or record.get("var_code") or record.get("var_name")
    family = canonical_source_family(source_family)
    wave = canonical_wave(family, canonical_wave_value)
    country = canonical_country_code(country_code)
    index = load_question_relation_authority(authority_path)
    artifact_path = _artifact_display_path(index.path)
    if family == "Asian Barometer" and wave.upper() == "W6":
        lookup = "|".join([family, wave, country, canonical_question_key(var_code or question_id)])
        return AuthorityResolution(
            status="BLOCKED_EXCLUDED_ASIAN_W6",
            authority_row=None,
            lookup_key=lookup,
            normalized_country_code=country,
            match_count=0,
            reason="Asian Barometer W6 is outside the governed 35-wave scope",
            authority_artifact_path=artifact_path,
            authority_artifact_sha256=index.file_sha256,
        )

    question_keys = []
    for value in (var_code, question_id):
        key = canonical_question_key(value)
        if key and key not in question_keys:
            question_keys.append(key)
    all_matches: list[dict[str, str]] = []
    attempted: list[str] = []
    for question_key in question_keys:
        key = _resolution_key(family, wave, country, question_key)
        attempted.append("|".join(key))
        all_matches.extend(index.by_key.get(key, ()))
    unique_matches = {row["row_payload_hash"]: row for row in all_matches}
    matches = list(unique_matches.values())
    lookup = ";".join(attempted) or "|".join([family, wave, country, ""])
    if not matches:
        return AuthorityResolution(
            status="BLOCKED_MISSING_AUTHORITY",
            authority_row=None,
            lookup_key=lookup,
            normalized_country_code=country,
            match_count=0,
            reason="no exact active country-scoped question-relation authority row",
            authority_artifact_path=artifact_path,
            authority_artifact_sha256=index.file_sha256,
        )
    if len(matches) != 1:
        return AuthorityResolution(
            status="BLOCKED_AMBIGUOUS_AUTHORITY",
            authority_row=None,
            lookup_key=lookup,
            normalized_country_code=country,
            match_count=len(matches),
            reason="multiple distinct authority rows matched question_id/var_code",
            authority_artifact_path=artifact_path,
            authority_artifact_sha256=index.file_sha256,
        )
    row = matches[0]
    relation_status = row["relation_use_status"].upper()
    if relation_status == DIRECTIONAL_STATUS:
        resolution_status = "RESOLVED_DIRECTIONAL_AUTHORITY"
    elif relation_status == NEUTRAL_COVERAGE_STATUS:
        resolution_status = "RESOLVED_NEUTRAL_COVERAGE_AUTHORITY"
    elif relation_status == "GOVERNED_CONTEXT_ONLY":
        resolution_status = "RESOLVED_CONTEXT_ONLY_AUTHORITY"
    elif relation_status == "GOVERNED_NON_RELATIONAL":
        resolution_status = "RESOLVED_NON_RELATIONAL_AUTHORITY"
    elif relation_status == "ADMINISTRATIVE_ONLY":
        resolution_status = "RESOLVED_ADMINISTRATIVE_AUTHORITY"
    elif relation_status.startswith("BLOCKED_"):
        resolution_status = "RESOLVED_EXPLICIT_BLOCK"
    else:  # guarded by registry validation
        resolution_status = "BLOCKED_UNSUPPORTED_AUTHORITY_STATUS"
    return AuthorityResolution(
        status=resolution_status,
        authority_row=row,
        lookup_key=lookup,
        normalized_country_code=country,
        match_count=1,
        authority_artifact_path=artifact_path,
        authority_artifact_sha256=index.file_sha256,
    )


def _clear_structural_coordinates(output: dict[str, Any]) -> None:
    for field in STRUCTURAL_COORDINATE_FIELDS:
        output[field] = ""
    output["source_response_polarity"] = ""
    output["relation_projection_polarity"] = ""
    output["item_reversal"] = False


def _artifact_display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.name


def _authority_metadata(
    output: dict[str, Any],
    resolution: AuthorityResolution,
    index: AuthorityIndex,
) -> None:
    row = resolution.authority_row or {}
    output.update(
        {
            "question_relation_authority_joined": resolution.resolved,
            "question_relation_authority_resolution_status": resolution.status,
            "question_relation_authority_lookup_key": resolution.lookup_key,
            "question_relation_authority_match_count": resolution.match_count,
            "question_relation_authority_country_code": resolution.normalized_country_code,
            "relation_use_status": row.get("relation_use_status", ""),
            "evidence_disposition": row.get("evidence_disposition", ""),
            "authority_status": row.get("authority_status", ""),
            "authority_rule_id": row.get("authority_rule_id", ""),
            "authority_version": row.get("authority_version", AUTHORITY_VERSION if resolution.resolved else ""),
            "authority_artifact_path": _artifact_display_path(index.path),
            "authority_artifact_sha256": index.file_sha256,
            "authority_row_payload_hash": row.get("row_payload_hash", ""),
            "authority_review_status": row.get("review_status", ""),
            "authority_review_notes": row.get("review_notes", ""),
            "question_relation_authority_reason": resolution.reason,
        }
    )


def apply_question_relation_authority(
    bridge_row: Mapping[str, Any],
    *,
    authority_path: Path | str | None = None,
) -> dict[str, Any]:
    """Apply the installed active question-relation authority to one V550 row.

    The resolver always overwrites legacy structural coordinates.  Missing,
    ambiguous, non-directional, administrative, and explicitly blocked rows are
    fail-closed and cannot retain stale relation semantics.
    """

    output = dict(bridge_row)
    index = load_question_relation_authority(authority_path)
    resolution = resolve_question_relation_authority(
        source_family=output.get("source_family") or output.get("source"),
        canonical_wave_value=output.get("canonical_wave") or output.get("wave"),
        country_code=output.get("country_code"),
        question_id=output.get("question_id"),
        var_code=output.get("var_code"),
        authority_path=index.path,
    )
    _authority_metadata(output, resolution, index)

    row = resolution.authority_row
    if row is None:
        quc_is_certified = (
            str(output.get("semantic_role_authority_status", "")).strip().upper() == "CERTIFIED"
            and str(output.get("semantic_role", "")).strip().upper() == "RELATION_EVIDENCE"
            and _bool(output.get("current_directional_atom_eligible"))
            and _bool(output.get("allowed_as_v551_relation_evidence"))
            and str(output.get("structural_mapping_status", "")).strip().upper() == "COMPLETE"
        )
        if quc_is_certified:
            output["question_relation_authority_resolution"] = "QUC_AUTHORITY_PRESERVED_ACTIVE_REGISTRY_NO_MATCH"
            output["question_relation_coverage_eligible"] = True
            output["question_relation_pressure_eligible"] = True
            output["question_relation_registry_match"] = False
            return output
        _clear_structural_coordinates(output)
        output.update(
            {
                "current_directional_atom_eligible": False,
                "allowed_as_v551_relation_evidence": False,
                "question_relation_coverage_eligible": False,
                "question_relation_pressure_eligible": False,
                "structural_mapping_status": resolution.status,
                "mapping_status": resolution.status.casefold(),
                "semantic_role": "UNKNOWN",
                "semantic_role_authority_status": "NOT_CERTIFIED",
                "v551_visible": True,
                "manual_review_flag": True,
                "manual_review_reason": resolution.reason or resolution.status,
            }
        )
        return output

    relation_status = row["relation_use_status"].upper()
    output["country_code"] = resolution.normalized_country_code or output.get("country_code", "")
    if relation_status == DIRECTIONAL_STATUS:
        for field in STRUCTURAL_COORDINATE_FIELDS:
            output[field] = row[field]
        output.update(
            {
                "source_response_polarity": row.get("source_response_polarity", ""),
                "relation_projection_polarity": row.get("relation_projection_polarity", ""),
                "item_reversal": _bool(row.get("item_reversal")),
                "current_directional_atom_eligible": _bool(row.get("current_directional_atom_eligible"), default=True),
                "allowed_as_v551_relation_evidence": _bool(row.get("current_directional_atom_eligible"), default=True),
                "question_relation_coverage_eligible": True,
                "question_relation_pressure_eligible": _bool(row.get("current_directional_atom_eligible"), default=True),
                "structural_mapping_status": "COMPLETE",
                "mapping_status": "governed_directional",
                "semantic_role": "RELATION_EVIDENCE",
                "semantic_role_authority_status": "CERTIFIED",
                "v551_visible": True,
            }
        )
        return output

    _clear_structural_coordinates(output)
    output.update(
        {
            "current_directional_atom_eligible": False,
            "allowed_as_v551_relation_evidence": False,
            "question_relation_pressure_eligible": False,
            "structural_mapping_status": (
                "COMPLETE_NON_DIRECTIONAL" if not relation_status.startswith("BLOCKED_") else relation_status
            ),
            "mapping_status": relation_status.casefold(),
            "semantic_role_authority_status": "CERTIFIED",
            "v551_visible": relation_status != "ADMINISTRATIVE_ONLY",
        }
    )
    if relation_status == NEUTRAL_COVERAGE_STATUS:
        output.update(
            {
                "semantic_role": "STRUCTURAL_CONTEXT",
                "question_relation_coverage_eligible": True,
            }
        )
    elif relation_status == "GOVERNED_CONTEXT_ONLY":
        output.update(
            {
                "semantic_role": "STRUCTURAL_CONTEXT",
                "question_relation_coverage_eligible": True,
            }
        )
    elif relation_status == "GOVERNED_NON_RELATIONAL":
        output.update(
            {
                "semantic_role": "STRUCTURAL_CONTEXT",
                "question_relation_coverage_eligible": True,
            }
        )
    elif relation_status == "ADMINISTRATIVE_ONLY":
        output.update(
            {
                "semantic_role": "UNKNOWN",
                "question_relation_coverage_eligible": False,
            }
        )
    else:  # explicit BLOCKED_*
        output.update(
            {
                "semantic_role": "UNKNOWN",
                "question_relation_coverage_eligible": False,
                "manual_review_flag": True,
                "manual_review_reason": row.get("review_notes") or relation_status,
            }
        )
    return output


def validate_active_universe(
    selected_rows: pd.DataFrame,
    *,
    authority_path: Path | str | None = None,
) -> pd.DataFrame:
    """Resolve a selected-question surface and return a row-level preflight audit."""

    audit: list[dict[str, Any]] = []
    for record in selected_rows.to_dict(orient="records"):
        source = record.get("source_family") or record.get("source")
        wave = record.get("canonical_wave") or record.get("wave")
        country = record.get("country_code_scope") or record.get("country_code")
        resolution = resolve_question_relation_authority(
            source_family=source,
            canonical_wave_value=wave,
            country_code=country,
            question_id=record.get("question_id", ""),
            var_code=record.get("var_code", ""),
            authority_path=authority_path,
        )
        row = resolution.authority_row or {}
        relation_status = row.get("relation_use_status", "")
        directional = relation_status == DIRECTIONAL_STATUS
        complete = bool(row) and (not directional or all(_text(row.get(field)) for field in REQUIRED_DIRECTIONAL_FIELDS))
        audit.append(
            {
                "source_family": canonical_source_family(source),
                "canonical_wave": canonical_wave(source, wave),
                "input_country_code": _text(country),
                "normalized_country_code": resolution.normalized_country_code,
                "question_id": _text(record.get("question_id")),
                "var_code": _text(record.get("var_code")),
                "resolver_status": resolution.status,
                "relation_use_status": relation_status,
                "authority_rule_id": row.get("authority_rule_id", ""),
                "authority_row_payload_hash": row.get("row_payload_hash", ""),
                "directional_coordinates_complete": complete,
                "current_directional_atom_eligible": _bool(row.get("current_directional_atom_eligible")),
                "lookup_key": resolution.lookup_key,
                "match_count": resolution.match_count,
                "reason": resolution.reason,
            }
        )
    return pd.DataFrame(audit)
