"""Source/hash-bound factual corrections to pinned R157 source configurations.

Corrections are versioned resource data, never source-name branches.  A
correction is applied only when the source identity, original source SHA-256,
config purpose, identity class and exact base-config canonical hash all match.
No label/frequency inference is performed here; the correction file carries the
exact declared raw value, missing state, missing declaration and response state.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

CORRECTIONS_PATH = Path(__file__).resolve().parent / "corrections" / "SOURCE_CONFIGURATION_CORRECTIONS.json"
CORRECTION_SCHEMA = "PYAT_R157_SOURCE_CONFIGURATION_CORRECTION@1.0.0"


class SourceCorrectionError(ValueError):
    pass


def _canonical_hash(document: Mapping[str, Any]) -> str:
    material = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _load_registry(path: str | Path | None = None) -> Mapping[str, Any]:
    target = Path(path) if path is not None else CORRECTIONS_PATH
    try:
        document = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SourceCorrectionError(f"cannot read source-configuration corrections: {exc}") from exc
    if document.get("schema") != CORRECTION_SCHEMA:
        raise SourceCorrectionError("unexpected source-configuration correction schema")
    return document


def _same_raw(left: Any, right: Any) -> bool:
    return type(left) is type(right) and left == right


def _slot_key(slot: Mapping[str, Any]) -> tuple[int, str]:
    return int(slot["ordinal"]), str(slot["name"])


def apply_source_config_corrections(
    document: Mapping[str, Any],
    *,
    registry_path: str | Path | None = None,
    base_commit: str | None = None,
    base_config_path: str | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Return a corrected deep copy and the exact applied-correction records.

    Only an ORIGINAL_SOURCE / SOURCE_PREPARATION document with matching source
    SHA and base canonical hash is eligible.  The pinned R157 document is never
    mutated.
    """
    registry = _load_registry(registry_path)
    base_hash = _canonical_hash(document)
    identity = document.get("identity") or {}
    binding = document.get("binding") or {}
    source_id = identity.get("source_id")
    source_sha = identity.get("expected_source_sha256")
    purpose = document.get("config_purpose")
    identity_class = binding.get("identity_class")
    matches = [
        entry for entry in registry.get("entries", ())
        if entry.get("source_id") == source_id
        and entry.get("source_sha256") == source_sha
        and entry.get("base_config_canonical_sha256") == base_hash
        and entry.get("config_purpose", "SOURCE_PREPARATION") == purpose
        and entry.get("identity_class", "ORIGINAL_SOURCE") == identity_class
    ]
    if not matches:
        return copy.deepcopy(dict(document)), []
    # Corrections are applied only when the trusted loader/provider supplies
    # the exact immutable base commit and repository-relative config path.
    # Registry self-assertion is not provenance.
    if base_commit is None or base_config_path is None:
        return copy.deepcopy(dict(document)), []
    for entry in matches:
        if entry.get("base_commit") != base_commit or entry.get("base_config_path") != base_config_path:
            raise SourceCorrectionError(
                "CORRECTION_BASE_PROVENANCE_MISMATCH: trusted base commit/path differ from registry")
    corrected = copy.deepcopy(dict(document))
    applied: list[dict[str, Any]] = []
    slots = {(int(s["slot"]["ordinal"]), str(s["slot"]["name"])): s
             for s in corrected.get("response_slots", ())}
    coordinate_slots = {(int(s["slot"]["ordinal"]), str(s["slot"]["name"])): s
                        for s in corrected.get("coordinate_slots", ())}
    for entry in matches:
        for change in entry.get("response_value_changes", ()):
            key = _slot_key(change["slot"])
            slot = slots.get(key)
            if slot is None:
                raise SourceCorrectionError(f"correction references unknown response slot {key}")
            values = slot.get("values") or []
            raw = change["raw_value"]
            existing = next((v for v in values if _same_raw(v.get("raw_value"), raw)), None)
            if existing is not None:
                for field in ("missing_state", "source_missing_declaration", "response_state", "canonical_value"):
                    if field in change:
                        existing[field] = copy.deepcopy(change[field])
                applied.append({
                    "action": "REPLACE_RESPONSE_VALUE",
                    "slot": list(key),
                    "raw_value": raw,
                    "missing_state": change.get("missing_state"),
                    "response_state": change.get("response_state"),
                    "correction_id": entry["correction_id"],
                    "base_commit": entry["base_commit"],
                    "base_config_path": entry["base_config_path"],
                })
                continue
            if not change.get("add_if_absent", False):
                raise SourceCorrectionError(f"correction raw value {raw!r} absent in slot {key}")
            template = values[0] if values else None
            if template is None:
                raise SourceCorrectionError(f"cannot add value to empty response slot {key}")
            value = copy.deepcopy(template)
            value["raw_value"] = raw
            value["missing_state"] = change.get("missing_state", "OBSERVED_STORAGE_VALUE")
            value["source_missing_declaration"] = copy.deepcopy(change.get("source_missing_declaration"))
            value["response_state"] = change.get("response_state", "INVALID_UNRESOLVED")
            value["canonical_value"] = copy.deepcopy(change.get("canonical_value"))
            values.append(value)
            applied.append({
                "action": "ADD_RESPONSE_VALUE",
                "slot": list(key),
                "raw_value": raw,
                "missing_state": value["missing_state"],
                "response_state": value["response_state"],
                "correction_id": entry["correction_id"],
                "base_commit": entry["base_commit"],
                "base_config_path": entry["base_config_path"],
            })
        for change in entry.get("coordinate_value_changes", ()):
            key = _slot_key(change["slot"])
            slot = coordinate_slots.get(key)
            if slot is None:
                raise SourceCorrectionError(f"correction references unknown coordinate slot {key}")
            values = slot.get("values") or []
            raw = change["raw_value"]
            existing = next((v for v in values if _same_raw(v.get("raw_value"), raw)), None)
            if existing is not None:
                for field in ("missing_state", "source_missing_declaration", "coordinate_state", "canonical_value"):
                    if field in change:
                        existing[field] = copy.deepcopy(change[field])
                applied.append({
                    "action": "REPLACE_COORDINATE_VALUE",
                    "slot": list(key),
                    "raw_value": raw,
                    "missing_state": change.get("missing_state"),
                    "coordinate_state": change.get("coordinate_state"),
                    "correction_id": entry["correction_id"],
                    "base_commit": entry["base_commit"],
                    "base_config_path": entry["base_config_path"],
                })
                continue
            if not change.get("add_if_absent", False):
                raise SourceCorrectionError(f"correction raw coordinate {raw!r} absent in slot {key}")
            template = values[0] if values else None
            if template is None:
                raise SourceCorrectionError(f"cannot add coordinate to empty slot {key}")
            value = copy.deepcopy(template)
            value["raw_value"] = raw
            value["missing_state"] = change.get("missing_state", "OBSERVED_STORAGE_VALUE")
            value["source_missing_declaration"] = copy.deepcopy(change.get("source_missing_declaration"))
            value["coordinate_state"] = change.get("coordinate_state", "UNKNOWN")
            value["canonical_value"] = copy.deepcopy(change.get("canonical_value"))
            values.append(value)
            applied.append({
                "action": "ADD_COORDINATE_VALUE",
                "slot": list(key),
                "raw_value": raw,
                "missing_state": value["missing_state"],
                "coordinate_state": value["coordinate_state"],
                "correction_id": entry["correction_id"],
                "base_commit": entry["base_commit"],
                "base_config_path": entry["base_config_path"],
            })
    return corrected, applied


__all__ = [
    "CORRECTIONS_PATH", "CORRECTION_SCHEMA", "SourceCorrectionError",
    "apply_source_config_corrections",
]
