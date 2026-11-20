"""Exact source-country registry handoff: multicountry/implicit single/held.

Checks the real historical country_source_mapping_registry.csv parser plus
small attacker fixtures. This is not a source-permission or I03-native test.
"""
import csv
from hashlib import sha256
from io import StringIO
from pathlib import Path

import pytest

from rawlsing_next.pre553_source_country_registry_adapter import (
    IMPLICIT_COUNTRY_VARIABLE, SourceCountryRegistryError,
    country_registry_for_exact_source,
)

REG = (Path(__file__).resolve().parents[2] / "data/ddm_build_copy/manifests"
       / "country_source_mapping_registry.csv")
AFRO_HASH = "6c9869a7cc7321cc74efb708835e21c8b65286a25c76deac45aba84d75697ee2"


def _read(**scope):
    raw = REG.read_bytes()
    return country_registry_for_exact_source(
        csv_bytes=raw, expected_registry_sha256=sha256(raw).hexdigest(),
        source_family="Afrobarometer", canonical_wave="R1",
        source_file_sha256=AFRO_HASH, country_variable="country", **scope,
    )


def test_real_multicountry_wave_country_mappings_are_exact_and_nonissued():
    result = _read()
    assert result.country_values_by_canonical_code["NG"] == "7"
    assert result.country_values_by_canonical_code["UG"] == "10"
    assert len(result.country_values_by_canonical_code) >= 4
    assert result.mapping_status == "CANDIDATE_ONLY_NOT_ISSUED"
    payload = result.source_authority_scope_candidate(
        universe_country_geography="MULTI_COUNTRY",
        country_coordinate_semantic_ref={"kind": "COORDINATE_NATIVE",
                                         "object_id": "country", "content_hash": "a" * 64},
        universe_ref={"kind": "EmpiricalUniverse@1.0.0",
                      "object_id": "survey", "content_hash": "b" * 64},
    )
    assert payload["country_values_by_canonical_code"]["NG"] == "7"
    assert payload["candidate_only_not_positive_authority"] is True
    assert payload["country_scope_kind"] == "MULTICOUNTRY_SOURCE_COORDINATE"


def test_source_wave_or_artifact_hash_mismatch_never_falls_back():
    raw = REG.read_bytes()
    for family, wave, source_hash, variable in [
        ("Afrobarometer", "R8", AFRO_HASH, "country"),
        ("Afrobarometer", "R1", "0" * 64, "country"),
        ("GSS", "R1", AFRO_HASH, "country"),
        ("Afrobarometer", "R1", AFRO_HASH, "COUNTRY"),
    ]:
        with pytest.raises(SourceCountryRegistryError, match="NO_EXACT"):
            country_registry_for_exact_source(
                csv_bytes=raw, expected_registry_sha256=sha256(raw).hexdigest(),
                source_family=family, canonical_wave=wave,
                source_file_sha256=source_hash, country_variable=variable)


def test_original_registry_must_be_hash_pinned_not_latest():
    with pytest.raises(SourceCountryRegistryError, match="HASH_MISMATCH"):
        country_registry_for_exact_source(
            csv_bytes=REG.read_bytes(), expected_registry_sha256="0" * 64,
            source_family="Afrobarometer", canonical_wave="R1",
            source_file_sha256=AFRO_HASH, country_variable="country")


def test_implicit_gss_country_does_not_create_fake_position_coordinate():
    raw = REG.read_bytes()
    first = next(row for row in csv.DictReader(StringIO(raw.decode("utf-8-sig")))
                 if row["source_family"] == "GSS"
                 and row["source_mapping_status"] == "SOURCE_MAPPING_RESOLVED")
    result = country_registry_for_exact_source(
        csv_bytes=raw, expected_registry_sha256=sha256(raw).hexdigest(),
        source_family="GSS", canonical_wave=first["canonical_wave"],
        source_file_sha256=first["source_file_sha256"],
        country_variable=IMPLICIT_COUNTRY_VARIABLE)
    assert dict(result.country_values_by_canonical_code) == {"US": "US"}
    with pytest.raises(SourceCountryRegistryError, match="NO_SOURCE_COORDINATE"):
        result.source_authority_scope_candidate(
            universe_country_geography="US",
            country_coordinate_semantic_ref={"kind": "FAKE"},
            universe_ref={"kind": "FAKE"})


def _mini_csv(rows):
    fields = sorted({
        "source_family", "canonical_wave", "source_file_sha256",
        "country_variable", "raw_country_value", "canonical_iso2",
        "source_mapping_status", "authority_path", "authority_artifact_sha256",
    })
    target = StringIO(newline="")
    writer = csv.DictWriter(target, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({
            "source_family": "S", "canonical_wave": "W1",
            "source_file_sha256": "a" * 64, "country_variable": "COUNTRY",
            "raw_country_value": "7", "canonical_iso2": "NG",
            "source_mapping_status": "SOURCE_MAPPING_RESOLVED",
            "authority_path": "a/source.csv",
            "authority_artifact_sha256": "b" * 64, **row,
        })
    return target.getvalue().encode("utf-8")


def _mini_run(raw):
    return country_registry_for_exact_source(
        csv_bytes=raw, expected_registry_sha256=sha256(raw).hexdigest(),
        source_family="S", canonical_wave="W1",
        source_file_sha256="a" * 64, country_variable="COUNTRY")


def test_conflicting_country_codes_are_not_coalesced():
    with pytest.raises(SourceCountryRegistryError, match="NONBIJECTIVE"):
        _mini_run(_mini_csv([
            {}, {"canonical_iso2": "UG", "raw_country_value": "7"},
        ]))
    with pytest.raises(SourceCountryRegistryError, match="NONBIJECTIVE"):
        _mini_run(_mini_csv([
            {}, {"canonical_iso2": "NG", "raw_country_value": "10"},
        ]))


def test_held_mapping_or_missing_authority_trace_blocks_country_issue():
    with pytest.raises(SourceCountryRegistryError, match="ROWS_HELD"):
        _mini_run(_mini_csv([{"source_mapping_status": "UNRESOLVED"}]))
    with pytest.raises(SourceCountryRegistryError, match="PROVENANCE_INVALID"):
        _mini_run(_mini_csv([{"authority_artifact_sha256": ""}]))
