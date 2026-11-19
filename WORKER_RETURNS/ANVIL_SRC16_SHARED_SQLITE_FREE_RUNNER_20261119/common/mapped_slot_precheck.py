"""Bounded aggregate precheck for mapped source slots.

Pure helper only.  It does not open the source and emits no respondent rows.
The controller-run census uses it after the existing exact resolver admits the
decode; `aggregate_mapped_slots` then reports unresolved physical tokens for
every mapped response/coordinate/weight slot in one bounded pass.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
from rawlsing_next.pre553_source_native_preimage_adapter import token

MAPPED_FAMILIES = (
    ("response", "response_slots"),
    ("coordinate", "coordinate_slots"),
    ("weight", "weight_slots"),
)


def _physical_key(raw_value: Any, missing_state: Any, declaration: Any) -> str:
    return physical_value_binding_key(
        raw_value,
        PhysicalMissingState(missing_state),
        declaration,
    )


def configured_bindings(doc: Mapping[str, Any]) -> dict[tuple[int, str], dict[str, Any]]:
    """Return the exact physical keys admitted by the pinned config."""
    result: dict[tuple[int, str], dict[str, Any]] = {}
    for family, section_name in MAPPED_FAMILIES:
        for section in doc.get(section_name, []):
            slot = section["slot"]
            key = (int(slot["ordinal"]), str(slot["name"]))
            allowed = set()
            for value in section.get("values", ()):
                allowed.add(_physical_key(
                    value.get("raw_value"),
                    value.get("missing_state", "OBSERVED_STORAGE_VALUE"),
                    value.get("source_missing_declaration"),
                ))
            result[key] = {
                "family": family,
                "ordinal": key[0],
                "name": key[1],
                "allowed": frozenset(allowed),
                "configured_values": len(section.get("values", ())),
                "copy_observed": bool(
                    section.get("copy_observed_raw")
                    or section.get("copy_observed_numeric")
                ),
            }
    return result


def aggregate_mapped_slots(
    doc: Mapping[str, Any],
    cells: Iterable[PhysicalCell],
) -> dict[str, Any]:
    """Aggregate unresolved tokens for every mapped slot, without row emission."""
    mapped = configured_bindings(doc)
    expected_rows = int(doc["binding"]["row_count"])
    unresolved: dict[tuple[int, str], Counter] = {}
    observed: Counter = Counter()
    duplicates: Counter = Counter()
    seen: dict[tuple[int, str], set[int]] = {key: set() for key in mapped}
    for cell in cells:
        key = (int(cell.variable_ordinal), str(cell.variable_name))
        if key not in mapped:
            continue
        observed[key] += 1
        row = int(cell.row_ordinal)
        if row in seen[key]:
            duplicates[key] += 1
            continue
        seen[key].add(row)
        if mapped[key]["copy_observed"]:
            continue
        physical = _physical_key(
            cell.raw_value, cell.missing_state, cell.source_missing_declaration)
        if physical in mapped[key]["allowed"]:
            continue
        bucket = unresolved.setdefault(key, Counter())
        bucket[(token(cell.raw_value), str(cell.missing_state),
                str(cell.source_missing_declaration))] += 1
    slot_reports = []
    for key in sorted(unresolved):
        info = mapped[key]
        tokens = [
            {
                "token": raw_token,
                "missing_state": missing_state,
                "source_missing_declaration": declaration,
                "count": count,
            }
            for (raw_token, missing_state, declaration), count in sorted(
                unresolved[key].items())
        ]
        slot_reports.append({
            "family": info["family"],
            "ordinal": info["ordinal"],
            "name": info["name"],
            "configured_values": info["configured_values"],
            "observed_count": observed[key],
            "unresolved_count": sum(tokens_count["count"] for tokens_count in tokens),
            "distinct_unresolved_tokens": len(tokens),
            "tokens": tokens,
        })
    missing = []
    for key, info in mapped.items():
        if observed[key] != expected_rows:
            missing.append({
                "family": info["family"],
                "ordinal": info["ordinal"],
                "name": info["name"],
                "expected_rows": expected_rows,
                "observed_count": observed[key],
                "missing_cells": expected_rows - observed[key],
            })
    duplicate_reports = [
        {"ordinal": key[0], "name": key[1], "duplicate_cells": count}
        for key, count in sorted(duplicates.items())
    ]
    return {
        "mapped_slots": len(mapped),
        "expected_rows": expected_rows,
        "unresolved_slot_count": len(slot_reports),
        "unresolved_cell_count": sum(x["unresolved_count"] for x in slot_reports),
        "unresolved_slots": slot_reports,
        "missing_slot_count": len(missing),
        "missing_slots": missing,
        "duplicate_slot_count": len(duplicate_reports),
        "duplicate_slots": duplicate_reports,
        "respondent_rows_emitted": False,
        "aggregate_only": True,
        "precheck_passed": not slot_reports and not missing and not duplicate_reports,
    }
