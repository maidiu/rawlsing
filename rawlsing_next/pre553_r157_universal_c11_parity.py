"""KUDA-082: retain the modern two-path C11 receipt parity, without R157's
obsolete source_configuration package or the 456-file 35-source fixture copy.

This narrow function only accepts an already-decoded NONRESPONDENT_FIXTURE.
Both execution paths use the existing current R157/C11 owners and independent
ingest. It neither reads original source bytes nor grants source permission.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence
from rawlsing_next.pre553_r157_projection_adapter import (
    IDENTITY_CLASS_FIXTURE,
    SourceConfig,
    build_governed_c11_projection,
    project_c11_candidate_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_validated_source_backed_c11_release,
)


class UniversalC11ReceiptError(ValueError):
    """Two independent current C11 receiving paths did not agree exactly."""


@dataclass(frozen=True)
class FixtureC11ParityReceipt:
    release_ref: ExactRef
    source_sha256: str
    source_rows: int
    facade_release_ref: ExactRef
    repository_release_refs: tuple[ExactRef, ...]
    semantic_release_hash: str
    family_counts: Mapping[str, int]
    m01_m18_coverage: Mapping[str, tuple[str, ...]]
    receipt_hash: str
    original_execution: str = "NOT_RUN"
    grade: str = "NONRESPONDENT_FIXTURE_ONLY__NO_SOURCE_READ_PERMISSION"


def receive_r157_fixture_c11_parity(
    *,
    config: SourceConfig,
    incidence: PhysicalSourceIncidence,
    expected_release_ref: ExactRef | None = None,
    batch_size: int = 10_000,
) -> FixtureC11ParityReceipt:
    """Use existing C11 facade and ingest independently; require exact parity.

    A source owner must never use this fixture-only API for ORIGINAL_SOURCE.
    The original KUDA-082 35-source metadata ledger is not claimed or copied.
    """
    if type(config) is not SourceConfig or config.identity_class != IDENTITY_CLASS_FIXTURE:
        raise UniversalC11ReceiptError("EXACT_NONRESPONDENT_FIXTURE_CONFIG_REQUIRED")
    if not isinstance(incidence, PhysicalSourceIncidence):
        raise UniversalC11ReceiptError("EXACT_ALREADY_DECODED_PHYSICAL_INCIDENCE_REQUIRED")
    if type(batch_size) is not int or batch_size < 1:
        raise UniversalC11ReceiptError("POSITIVE_EXACT_BATCH_SIZE_REQUIRED")
    if expected_release_ref is not None and (
        type(expected_release_ref) is not ExactRef or expected_release_ref.kind != "C11LogicalRelease"
    ):
        raise UniversalC11ReceiptError("EXPECTED_EXACT_C11_RELEASE_REF_REQUIRED")

    # Preexisting current R157 source-native keys, exact bound projection,
    # native facade and native direct I02 ingress. No new physical decoder.
    keys = row_native_keys_from_transport(config, incidence=incidence, batch_size=batch_size)
    projection = build_governed_c11_projection(
        config, source_sha256=incidence.source_sha256,
        row_count=incidence.row_count, row_native_keys=keys,
    )
    facade = build_validated_source_backed_c11_release(
        incidence, projection, batch_size=batch_size,
    )
    candidate = project_c11_candidate_from_config(
        config, projection,
        cells_factory=lambda: incidence.iter_cells(batch_size),
        row_native_keys=keys,
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
    )
    repository = C11Repository()
    ingest = ingest_c11_source_release(candidate, repository)
    if not ingest.accepted or ingest.release_ref is None:
        raise UniversalC11ReceiptError(
            f"CURRENT_INGEST_REFUSED:{ingest.disposition}:{tuple(ingest.errors)}"
        )
    direct = repository.resolve_release_exact(ingest.release_ref)
    if (facade.release_ref != direct.release_ref
            or facade.semantic_release_hash != direct.semantic_release_hash
            or facade.source_artifact_ref != direct.source_artifact_ref
            or facade.m01_m18_coverage != direct.m01_m18_coverage):
        raise UniversalC11ReceiptError("R157_FACADE_AND_DIRECT_INGEST_DIVERGED")
    if expected_release_ref is not None and expected_release_ref != direct.release_ref:
        raise UniversalC11ReceiptError("PINNED_EXPECTED_C11_REF_MISMATCH")
    if repository.release_refs != (direct.release_ref,):
        raise UniversalC11ReceiptError("ATOMIC_ONE_RELEASE_INVENTORY_MISMATCH")

    counts = dict(sorted(Counter(type(x).__name__ for x in direct.public_objects).items()))
    coverage = {k: tuple(v) for k, v in direct.m01_m18_coverage.items()}
    material = {
        "release_ref": direct.release_ref.as_dict(),
        "facade_release_ref": facade.release_ref.as_dict(),
        "repository_release_refs": [x.as_dict() for x in repository.release_refs],
        "source_sha256": incidence.source_sha256,
        "source_rows": incidence.row_count,
        "semantic_release_hash": direct.semantic_release_hash,
        "family_counts": counts,
        "m01_m18_coverage": coverage,
        "original_execution": "NOT_RUN",
        "grade": "NONRESPONDENT_FIXTURE_ONLY__NO_SOURCE_READ_PERMISSION",
    }
    return FixtureC11ParityReceipt(
        release_ref=direct.release_ref,
        source_sha256=incidence.source_sha256,
        source_rows=incidence.row_count,
        facade_release_ref=facade.release_ref,
        repository_release_refs=repository.release_refs,
        semantic_release_hash=direct.semantic_release_hash,
        family_counts=counts,
        m01_m18_coverage=coverage,
        receipt_hash=semantic_hash(material),
    )


__all__ = ["UniversalC11ReceiptError", "FixtureC11ParityReceipt",
           "receive_r157_fixture_c11_parity"]
