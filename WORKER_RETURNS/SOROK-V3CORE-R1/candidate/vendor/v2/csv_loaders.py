# Shared CSV loaders for item_content_map.csv and driver_content_map.csv.
# This deduplicates the near-identical functions previously in data_access.py
# and etl/barometer_utils.py.
from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

_V2_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _V2_DIR.parent
_DATA_DIR = _REPO_ROOT / "data" / "final_codebooks"
_ITEM_CONTENT_PATH = _DATA_DIR / "item_content_map.csv"
_DRIVER_CONTENT_PATH = _V2_DIR / "driver_content_map.csv"


def _is_skippable_first_cell(value: str) -> bool:
    stripped = value.strip()
    return not stripped or stripped.startswith("#") or stripped.startswith("//")


def iter_item_content_pairs(path: Path | None = None) -> list[tuple[str, str]]:
    """Return `(item_id, content_id)` pairs from the item-content CSV."""
    path = path or _ITEM_CONTENT_PATH
    if not path.exists():
        return []
    pairs: list[tuple[str, str]] = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2:
                continue
            item_id = row[0].strip()
            content_id = row[1].strip()
            if _is_skippable_first_cell(item_id):
                continue
            if item_id.lower() in {"item_id", "var_name"}:
                continue
            if not content_id:
                continue
            pairs.append((item_id, content_id))
    return pairs


def load_item_to_content(path: Path | None = None) -> dict[str, str]:
    """
    Load item_content_map.csv → {var_suffix: content_id} mapping.
    Var suffix is the last component of var_name after the last '/'.
    Skips comment rows and rows without a content_id.
    """
    path = path or _ITEM_CONTENT_PATH
    if not path.exists():
        return {}
    mapping: dict[str, str] = {}
    for item_id, content_id in iter_item_content_pairs(path):
        var_suffix = item_id.rsplit("/", 1)[-1] if "/" in item_id else item_id
        mapping[var_suffix] = content_id
    return mapping


def iter_driver_content_pairs(path: Path | None = None) -> list[tuple[str, str]]:
    """Return `(driver_name, content_id)` pairs from the driver-content CSV."""
    path = path or _DRIVER_CONTENT_PATH
    if not path.exists():
        return []
    pairs: list[tuple[str, str]] = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2:
                continue
            first = row[0].strip()
            second = row[1].strip()
            if _is_skippable_first_cell(first):
                continue
            first_lower = first.lower()
            second_lower = second.lower()
            if first_lower in {"driver", "driver_name"} and second_lower == "content_id":
                continue
            if first_lower == "content_id" and second_lower in {"driver", "driver_name"}:
                continue
            if not first or not second:
                continue
            pairs.append((first, second))
    return pairs


def load_content_to_drivers(path: Path | None = None) -> dict[str, list[str]]:
    """
    Load driver_content_map.csv → {content_id: [driver_names]} mapping.
    A single content_id can map to multiple driver names.
    """
    mapping: dict[str, list[str]] = {}
    for driver_name, content_id in iter_driver_content_pairs(path):
        if content_id not in mapping:
            mapping[content_id] = []
        mapping[content_id].append(driver_name)
    return mapping


def load_driver_sources_availability(
    item_content_path: Path | None = None,
    driver_content_path: Path | None = None,
) -> dict[str, dict[str, Any]]:
    """
    Build a combined {driver_name: {sources, content_ids}} availability dict.
    Formerly _load_driver_sources_availability() in data_access.py.
    """
    item_to_content = load_item_to_content(item_content_path)
    content_to_drivers = load_content_to_drivers(driver_content_path)
    driver_sources: dict[str, dict[str, Any]] = {}
    for content_id, driver_names in content_to_drivers.items():
        for driver_name in driver_names:
            if driver_name not in driver_sources:
                driver_sources[driver_name] = {
                    "sources": set(),
                    "content_ids": set(),
                }
            driver_sources[driver_name]["content_ids"].add(content_id)
    for var_suffix, content_id in item_to_content.items():
        if "/" in var_suffix:
            source_part = var_suffix.split("/")[0]
        else:
            source_part = "unknown"
        if content_id in content_to_drivers:
            for driver_name in content_to_drivers[content_id]:
                if driver_name in driver_sources:
                    driver_sources[driver_name]["sources"].add(source_part)
    return {
        driver_name: {
            "sources": sorted(info["sources"]),
            "content_ids": sorted(info["content_ids"]),
        }
        for driver_name, info in driver_sources.items()
    }
