"""Receive every declared fixture release through the current C11 consumer.

The branch-only R157 factory is used only to turn a declared configuration into
the governed projection.  The deciding receive path is the *current installed*
facade/ingest/repository: candidate construction, M01-M18 validation and atomic
repository commit.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    RespondentEvent,
    RoutingEligibilityFact,
    WeightMeasureFact,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_validated_source_backed_c11_release_from_stream,
    project_c11_candidate_from_physical_cells,
)
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    row_native_keys_from_transport,
)

from .registry import UniversalSourceRegistry


class ConsumerReceiptError(AssertionError):
    """A release did not survive the current C11 consumer exactly."""


@dataclass(frozen=True)
class ConsumerReceipt:
    source_id: str
    family: str
    wave: str
    disposition: str
    original_execution: str
    original_config_path: str
    original_config_file_sha256: str
    original_config_canonical_sha256: str
    fixture_config_path: str
    fixture_config_file_sha256: str
    fixture_path: str
    fixture_file_sha256: str
    fixture_source_sha256: str
    fixture_row_count: int
    projection_identity_ref: dict[str, Any]
    projection_counts: dict[str, int]
    release_ref: dict[str, Any]
    semantic_release_hash: str
    facade_release_ref: dict[str, Any]
    ingest_disposition: str
    ingest_accepted: bool
    repository_release_refs: tuple[dict[str, Any], ...]
    public_object_counts: dict[str, int]
    m01_m18_coverage: dict[str, tuple[str, ...]]
    source_read_performed: bool
    original_respondent_rows_read: bool
    source_bytes_copied: bool
    original_workload_issued: bool
    native_source_package_required: bool

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["m01_m18_coverage"] = {
            key: list(value) for key, value in self.m01_m18_coverage.items()
        }
        payload["repository_release_refs"] = [dict(ref) for ref in self.repository_release_refs]
        return payload


def _object_counts(release: C11LogicalRelease) -> dict[str, int]:
    counts: dict[str, int] = {}
    for obj in release.public_objects:
        name = type(obj).__name__
        counts[name] = counts.get(name, 0) + 1
    for name in (
        RespondentEvent.__name__,
        RoutingEligibilityFact.__name__,
        EmpiricalCoordinateFact.__name__,
        WeightMeasureFact.__name__,
    ):
        counts.setdefault(name, 0)
    return dict(sorted(counts.items()))


def receive_fixture_release(
    registry: UniversalSourceRegistry,
    source_id: str,
) -> ConsumerReceipt:
    """Construct, validate and atomically receive one declared fixture release."""
    slot = registry.slot(source_id)
    stream = slot.fixture_stream
    fixture_config = slot.fixture_config

    keys = row_native_keys_from_transport(fixture_config, stream=stream)
    projection = build_governed_c11_projection(fixture_config, row_native_keys=keys)

    # Current installed facade: source-backed candidate + M01-M18 validation.
    facade_release = build_validated_source_backed_c11_release_from_stream(stream, projection)

    # Current installed ingest + repository: independent candidate construction,
    # deciding validation, and atomic append-only commit.
    candidate = project_c11_candidate_from_physical_cells(
        source_sha256=stream.source_sha256,
        row_count=stream.row_count,
        cells=stream.iter_cells(),
        projection=projection,
    )
    repository = C11Repository()
    ingest_result = ingest_c11_source_release(candidate, repository)
    if not ingest_result.accepted or ingest_result.release_ref is None:
        raise ConsumerReceiptError(
            f"{source_id}: current C11 ingest refused: {ingest_result.disposition}: "
            f"{'; '.join(ingest_result.errors)}")
    direct_release = repository.resolve_release_exact(ingest_result.release_ref)

    if facade_release.release_ref != direct_release.release_ref:
        raise ConsumerReceiptError(
            f"{source_id}: facade and current-ingest release refs differ")
    if facade_release.semantic_release_hash != direct_release.semantic_release_hash:
        raise ConsumerReceiptError(
            f"{source_id}: facade and current-ingest semantic hashes differ")
    expected = slot.index_row.get("release_ref") or {}
    if expected.get("content_hash") and expected["content_hash"] != direct_release.release_ref.content_hash:
        raise ConsumerReceiptError(
            f"{source_id}: release does not match the recorded R157 native receipt")
    if tuple(repository.release_refs) != (direct_release.release_ref,):
        raise ConsumerReceiptError(
            f"{source_id}: repository inventory is not the single exact release")

    projection_counts = {
        "universes": len(projection.universes),
        "respondents": len(projection.respondents),
        "row_bindings": len(projection.row_bindings),
        "questions": len(projection.questions),
        "response_slots": len(projection.response_slots),
        "coordinate_slots": len(projection.coordinate_slots),
        "routing_facts": len(projection.routing),
        "weight_slots": len(projection.weight_slots),
        "authority_snapshots": len(projection.authority_snapshots),
        "slot_owner_sets": len(projection.slot_owner_sets),
    }

    return ConsumerReceipt(
        source_id=source_id,
        family=slot.family,
        wave=slot.wave,
        disposition=slot.disposition,
        original_execution="NOT_RUN",
        original_config_path=slot.index_row["original_config_path"],
        original_config_file_sha256=slot.index_row["original_config_file_sha256"],
        original_config_canonical_sha256=slot.index_row["original_config_canonical_sha256"],
        fixture_config_path=slot.index_row["fixture_config_path"],
        fixture_config_file_sha256=slot.index_row["fixture_config_file_sha256"],
        fixture_path=slot.index_row["fixture_path"],
        fixture_file_sha256=slot.index_row["fixture_file_sha256"],
        fixture_source_sha256=stream.source_sha256,
        fixture_row_count=stream.row_count,
        projection_identity_ref=projection.projection_identity_ref.as_dict(),
        projection_counts=projection_counts,
        release_ref=direct_release.release_ref.as_dict(),
        semantic_release_hash=direct_release.semantic_release_hash,
        facade_release_ref=facade_release.release_ref.as_dict(),
        ingest_disposition=ingest_result.disposition.value,
        ingest_accepted=ingest_result.accepted,
        repository_release_refs=tuple(ref.as_dict() for ref in repository.release_refs),
        public_object_counts=_object_counts(direct_release),
        m01_m18_coverage={
            key: tuple(value) for key, value in direct_release.m01_m18_coverage.items()
        },
        source_read_performed=False,
        original_respondent_rows_read=False,
        source_bytes_copied=False,
        original_workload_issued=False,
        native_source_package_required=False,
    )


def receive_all(
    registry: UniversalSourceRegistry,
) -> tuple[ConsumerReceipt, ...]:
    return tuple(receive_fixture_release(registry, source_id) for source_id in registry.source_ids)
