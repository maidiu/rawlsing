"""Non-semantic physical-incidence to existing I02 validation bridge."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from rawlsing_next.pre553_c11_ingest import C11SourceReleaseCandidate, validate_c11_source_release
from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalSourceIncidence


class PhysicalC11BridgeError(ValueError):
    pass


@dataclass(frozen=True)
class PhysicalSourceAuthorityProjection:
    """Caller-owned source authority; SR06 does not infer any field meaning."""
    required_authority_refs: tuple[Any, ...]
    candidate_builder: Callable[[PhysicalSourceIncidence, Iterable[PhysicalCell], "PhysicalSourceAuthorityProjection"], C11SourceReleaseCandidate]


def build_validated_c11_release(
    incidence: PhysicalSourceIncidence,
    authority: PhysicalSourceAuthorityProjection | None,
    *, batch_size: int = 10_000,
) -> C11LogicalRelease:
    if not isinstance(incidence, PhysicalSourceIncidence):
        raise PhysicalC11BridgeError("format-neutral physical incidence is required")
    if authority is None or not authority.required_authority_refs or not callable(authority.candidate_builder):
        raise PhysicalC11BridgeError("explicit source-authority projection is required; no semantic inference permitted")
    candidate = authority.candidate_builder(incidence, incidence.iter_cells(batch_size), authority)
    if not isinstance(candidate, C11SourceReleaseCandidate):
        raise PhysicalC11BridgeError("authority projection must build C11SourceReleaseCandidate")
    return validate_c11_source_release(candidate)


__all__ = ["PhysicalC11BridgeError", "PhysicalSourceAuthorityProjection", "build_validated_c11_release"]
