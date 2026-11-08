"""Generic registry over every declared R157 source configuration.

The registry is driven by the portable source roster and the imported package
data.  Source IDs are data keys only; there is no per-wave code path.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.source_configuration.evidence import load_source_roster, roster_by_source
from rawlsing_next.source_configuration.library import (
    INDEX_PATH,
    ROOT,
    SourceConfigLibrary,
    SourceNotPrepared,
)
from rawlsing_next.source_configuration.schema import (
    SourceConfig,
    canonical_config_hash,
    config_file_sha256,
)

FIXTURE_ONLY = "FIXTURE_ONLY"
NOT_RUN = "NOT_RUN"
ORIGINAL_EXECUTION_NOT_RUN = "NOT_RUN"


class UniversalRegistryError(ValueError):
    """The declared source estate is incomplete or internally inconsistent."""


@dataclass(frozen=True)
class SourceSlot:
    source_id: str
    family: str
    wave: str
    original_config: SourceConfig
    fixture_config: SourceConfig
    index_row: Mapping[str, Any]
    roster_row: Mapping[str, Any]
    fixture_stream: Any

    @property
    def declared_supported(self) -> bool:
        return bool(self.original_config.document["supported_scope"]["declared_supported"])

    @property
    def disposition(self) -> str:
        return NOT_RUN if self.declared_supported else FIXTURE_ONLY


class UniversalSourceRegistry:
    """One registry for all 35 declared sources, with no single-wave target."""

    def __init__(
        self,
        *,
        root: str | Path = ROOT,
        index_path: str | Path = INDEX_PATH,
    ) -> None:
        self.root = Path(root).resolve()
        self.index_path = Path(index_path)
        self.library = SourceConfigLibrary(index_path=self.index_path, root=self.root)
        self.roster = load_source_roster()
        self.roster_by_id = roster_by_source()
        self.source_ids = tuple(entry["source_id"] for entry in self.roster["sources"])
        if len(self.source_ids) != 35 or len(set(self.source_ids)) != 35:
            raise UniversalRegistryError("declared source roster is not exactly 35 unique sources")
        if set(self.source_ids) != set(self.library.records):
            raise UniversalRegistryError("roster and portable index disagree on source membership")
        self._slots: dict[str, SourceSlot] = {}

    def slot(self, source_id: str) -> SourceSlot:
        if source_id not in self.source_ids:
            raise SourceNotPrepared(source_id, "UNKNOWN_SOURCE")
        if source_id not in self._slots:
            index_row = self.library.record(source_id)
            roster_row = self.roster_by_id[source_id]
            original = self.library.load_original(source_id)
            fixture_config = self.library.load_fixture_config(source_id)
            fixture_stream = self.library.load_fixture_stream(source_id)
            if original.source_id != source_id or fixture_config.source_id != source_id:
                raise UniversalRegistryError(f"{source_id}: config identity mismatch")
            if fixture_config.identity_class != "NONRESPONDENT_FIXTURE":
                raise UniversalRegistryError(f"{source_id}: fixture identity class is not NONRESPONDENT_FIXTURE")
            if fixture_config.active_source_sha256 != fixture_stream.source_sha256:
                raise UniversalRegistryError(f"{source_id}: fixture SHA binding mismatch")
            if fixture_config.active_row_count != fixture_stream.row_count:
                raise UniversalRegistryError(f"{source_id}: fixture row-count binding mismatch")
            physical_slots = len(original.document.get("physical_slots", ()))
            original_items = len(original.document.get("items", ()))
            if physical_slots != int(roster_row["physical_columns"]):
                raise UniversalRegistryError(f"{source_id}: physical-slot denominator mismatch")
            if original_items != int(roster_row["original_items"]):
                raise UniversalRegistryError(f"{source_id}: original-item denominator mismatch")
            if fixture_config.active_source_sha256 == original.original_source_sha256:
                raise UniversalRegistryError(f"{source_id}: fixture reused the original source SHA")
            self._slots[source_id] = SourceSlot(
                source_id=source_id,
                family=original.document["identity"]["family"],
                wave=original.document["identity"]["wave"],
                original_config=original,
                fixture_config=fixture_config,
                index_row=index_row,
                roster_row=roster_row,
                fixture_stream=fixture_stream,
            )
        return self._slots[source_id]

    def slots(self) -> tuple[SourceSlot, ...]:
        return tuple(self.slot(source_id) for source_id in self.source_ids)

    def config_hashes(self, source_id: str) -> dict[str, str]:
        slot = self.slot(source_id)
        return {
            "original_config_file_sha256": config_file_sha256(
                self.root / slot.index_row["original_config_path"]),
            "original_config_canonical_sha256": canonical_config_hash(slot.original_config),
            "fixture_config_file_sha256": config_file_sha256(
                self.root / slot.index_row["fixture_config_path"]),
            "fixture_config_canonical_sha256": canonical_config_hash(slot.fixture_config),
            "fixture_file_sha256": slot.index_row["fixture_file_sha256"],
            "fixture_source_sha256": slot.fixture_stream.source_sha256,
        }
