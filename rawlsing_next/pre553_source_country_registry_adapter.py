"""Historical 35-wave country-code registry -> exact source-issuer *candidate*.

The legacy CSV is evidence, NOT a new source-science permission and NOT an
EmpiricalUniverse, AuthoritySnapshot or I03 query. It is only admissible as
a proposed exact raw-country-code translation after the caller pins the CSV
hash, source artifact hash, family, wave and source-native country variable.
The actual source owner must verify the matching C11 coordinate and issue
the separate positive COORDINATE_SEMANTICS snapshot.

No fuzzy country aliases, guesses, implicit GSS country splitter, or
cross-wave/cross-source lookup. Real CSV quotes are read by csv.DictReader.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from hashlib import sha256
from io import StringIO
from types import MappingProxyType
from typing import Any, Mapping

COUNTRY_REGISTRY_SCHEMA = "PYAT_SOURCE_COUNTRY_REGISTRY_CANDIDATE@1"
REQUIRED = frozenset({
    "source_family", "canonical_wave", "source_file_sha256",
    "country_variable", "raw_country_value", "canonical_iso2",
    "source_mapping_status", "authority_path", "authority_artifact_sha256",
})
POSITIVE_SOURCE_ROW = "SOURCE_MAPPING_RESOLVED"
IMPLICIT_COUNTRY_VARIABLE = "IMPLICIT_US_FROM_GSS_SOURCE"


class SourceCountryRegistryError(ValueError):
    """Missing, ambiguous, unresolved or stale source-country mapping."""


@dataclass(frozen=True)
class CountryRegistryCandidate:
    source_family: str
    canonical_wave: str
    source_sha256: str
    country_variable: str
    registry_sha256: str
    country_values_by_canonical_code: Mapping[str, str]
    authority_artifact_refs: tuple[tuple[str, str], ...]
    mapping_status: str = "CANDIDATE_ONLY_NOT_ISSUED"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "country_values_by_canonical_code",
            MappingProxyType(dict(self.country_values_by_canonical_code)),
        )

    def source_authority_scope_candidate(
        self, *, universe_country_geography: Any,
        country_coordinate_semantic_ref: Mapping[str, Any],
        universe_ref: Mapping[str, Any],
    ) -> dict[str, Any]:
        """For a real source issuer to assess; this does NOT issue authority."""
        if self.country_variable == IMPLICIT_COUNTRY_VARIABLE:
            raise SourceCountryRegistryError(
                "GSS_IMPLICIT_COUNTRY_NO_SOURCE_COORDINATE_TO_ISSUE")
        if not isinstance(universe_ref, Mapping) or not isinstance(
                country_coordinate_semantic_ref, Mapping):
            raise SourceCountryRegistryError("ACTUAL_SOURCE_COORDINATE_REF_REQUIRED")
        return {
            "country_scope_kind": "MULTICOUNTRY_SOURCE_COORDINATE",
            "source_universe_refs": [dict(universe_ref)],
            "source_universe_country_geography": universe_country_geography,
            "country_coordinate_semantic_ref": dict(country_coordinate_semantic_ref),
            "country_values_by_canonical_code": dict(
                sorted(self.country_values_by_canonical_code.items())),
            "candidate_registry_source_sha256": self.source_sha256,
            "candidate_registry_sha256": self.registry_sha256,
            "candidate_authority_artifact_refs": [
                {"path": path, "sha256": digest}
                for path, digest in self.authority_artifact_refs
            ],
            "candidate_only_not_positive_authority": True,
        }


def country_registry_for_exact_source(
    *, csv_bytes: bytes, expected_registry_sha256: str,
    source_family: str, canonical_wave: str,
    source_file_sha256: str, country_variable: str,
) -> CountryRegistryCandidate:
    """Refuse ambiguity rather than silently misassign countries to people."""
    if not isinstance(csv_bytes, bytes):
        raise SourceCountryRegistryError("COUNTRY_REGISTRY_BYTES_REQUIRED")
    actual_hash = sha256(csv_bytes).hexdigest()
    if (len(expected_registry_sha256) != 64 or
            actual_hash != expected_registry_sha256):
        raise SourceCountryRegistryError("COUNTRY_REGISTRY_HASH_MISMATCH")
    if (any(not isinstance(x, str) or not x.strip() for x in
            (source_family, canonical_wave, source_file_sha256, country_variable))
            or len(source_file_sha256) != 64):
        raise SourceCountryRegistryError("EXACT_SOURCE_WAVE_HASH_VARIABLE_REQUIRED")
    try:
        stream = StringIO(csv_bytes.decode("utf-8-sig"), newline="")
        reader = csv.DictReader(stream)
        if not REQUIRED.issubset(set(reader.fieldnames or ())):
            raise SourceCountryRegistryError("COUNTRY_REGISTRY_SCHEMA_INCOMPLETE")
        rows = [
            row for row in reader
            if (row["source_family"] == source_family
                and row["canonical_wave"] == canonical_wave
                and row["source_file_sha256"] == source_file_sha256
                and row["country_variable"] == country_variable)
        ]
    except UnicodeDecodeError as exc:
        raise SourceCountryRegistryError("COUNTRY_REGISTRY_NOT_UTF8") from exc
    if not rows:
        raise SourceCountryRegistryError("NO_EXACT_COUNTRY_SOURCE_MAPPING")
    if any(row["source_mapping_status"] != POSITIVE_SOURCE_ROW for row in rows):
        raise SourceCountryRegistryError("SOME_COUNTRY_MAPPING_ROWS_HELD")
    values: dict[str, str] = {}
    reverse: dict[str, str] = {}
    authority_artifacts: set[tuple[str, str]] = set()
    for row in rows:
        iso = row["canonical_iso2"]
        raw = row["raw_country_value"]
        evidence = (row["authority_path"], row["authority_artifact_sha256"])
        if (not isinstance(iso, str) or len(iso) != 2 or iso.upper() != iso
                or not isinstance(raw, str) or not raw
                or not evidence[0] or len(evidence[1]) != 64):
            raise SourceCountryRegistryError("COUNTRY_MAPPING_VALUE_OR_PROVENANCE_INVALID")
        if (iso in values and values[iso] != raw or
                raw in reverse and reverse[raw] != iso):
            raise SourceCountryRegistryError("COUNTRY_MAPPING_NONBIJECTIVE")
        values[iso] = raw
        reverse[raw] = iso
        authority_artifacts.add(evidence)
    if country_variable == IMPLICIT_COUNTRY_VARIABLE:
        # No fake per-respondent GSS country coordinate: admission occurs via
        # an exact US EmpiricalUniverse country_geography assertion instead.
        if values != {"US": "US"}:
            raise SourceCountryRegistryError("IMPLICIT_COUNTRY_IS_NOT_SINGLE_US")
    return CountryRegistryCandidate(
        source_family=source_family,
        canonical_wave=canonical_wave,
        source_sha256=source_file_sha256,
        country_variable=country_variable,
        registry_sha256=actual_hash,
        country_values_by_canonical_code=values,
        authority_artifact_refs=tuple(sorted(authority_artifacts)),
    )
