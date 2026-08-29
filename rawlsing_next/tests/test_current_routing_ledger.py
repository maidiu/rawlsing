from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.current_routing_ledger import (
    CATALOG_CONTRACT_VERSION,
    CURRENT_CATALOG_ARCHIVE_SHA256,
    CURRENT_CATALOG_CONTRACT,
    CURRENT_CATALOG_TOTAL_ROWS,
    CURRENT_FAMILY_SPECS,
    DISPOSITIONS,
    EXACT_MEMBERSHIP_BASIS,
    FORBIDDEN_MEMBERSHIP_BASES,
    LEDGER_COLUMNS,
    POSITIVE_ROUTING,
    SCHEMA_VERSION,
    SCOPED_NONAPPLICABILITY,
    UNRESOLVED,
    CatalogContract,
    FamilyCatalogSpec,
    RoutingLedgerError,
    compile_joined_ledger,
    load_catalog_bundle,
    validate_family_ledger,
)

FIXTURE_JOINED_HASH = "97e96e539c1e328ade142d559ed336597d29b1ec3a7ebc512437e5df7392f39c"
FIXTURE_UNRESOLVED_HASH = "58520955874699f896f2afb429dddc6d133bffb1b60784924a73429f462397f1"

FAMILIES = [
    "GSS",
    "LiTS",
    "EVS",
    "Arab Barometer",
    "WVS",
    "Afrobarometer",
    "Asian Barometer",
    "Latinobarómetro",
    "South Asia",
]

FIXTURE_DISPOSITIONS = [
    POSITIVE_ROUTING,
    SCOPED_NONAPPLICABILITY,
    "GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE",
    "ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT",
    UNRESOLVED,
    UNRESOLVED,
    UNRESOLVED,
    UNRESOLVED,
    "GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE",
]

FIXTURE_BLOCKERS = [
    "",
    "",
    "",
    "",
    "NO_EXACT_SOURCE_AUTHORITY",
    "ROUTING_INSTRUCTION_UNAVAILABLE",
    "ROUTING_INSTRUCTION_UNAVAILABLE",
    "NO_EXACT_SOURCE_AUTHORITY",
    "",
]


def _canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path.read_bytes()


def _fixture_catalog(tmp_path: Path):
    specs = []
    for index, family in enumerate(FAMILIES):
        filename = f"catalog_{index:02d}.csv"
        row = {
            "question_implementation_id": f"question_impl.fixture.{index:02d}",
            "source_family": family,
            "canonical_wave": f"W{index}",
            "source_variable_code": f"V{index:02d}",
            "country_code": f"C{index}",
            "form": f"F{index}",
            "module": f"M{index}",
            "split": f"S{index}",
        }
        payload = _write_csv(
            tmp_path / filename,
            list(row),
            [row],
        )
        specs.append(
            FamilyCatalogSpec(
                source_family=family,
                filename=filename,
                rows=1,
                sha256=hashlib.sha256(payload).hexdigest(),
            )
        )
    contract = CatalogContract(
        contract_version="fixture_contract_v1",
        archive_name="fixture.zip",
        archive_sha256="f" * 64,
        total_rows=9,
        active_scopes=9,
        families=tuple(specs),
    )
    return load_catalog_bundle(tmp_path, contract=contract)


def _ledger_row(catalog, index: int, *, disposition: str | None = None) -> dict[str, str]:
    family = FAMILIES[index]
    item_id = next(iter(catalog.family_ids[family]))
    item = catalog.rows_by_id[item_id]
    disposition = disposition or FIXTURE_DISPOSITIONS[index]
    scope = {
        "question_implementation_id": item.question_implementation_id,
        "source_family": item.source_family,
        "canonical_wave": item.canonical_wave,
        "country_scope": item.country_scope,
        "form_scope": item.form_scope,
        "module_scope": item.module_scope,
        "split_scope": item.split_scope,
    }
    evidence_ref = f"fixture://evidence/{index}"
    provenance_ref = f"fixture://provenance/{index}"
    predicate = {"field": "route", "op": "eq", "value": "1"} if disposition == POSITIVE_ROUTING else None
    unresolved = disposition == UNRESOLVED
    return {
        "schema_version": SCHEMA_VERSION,
        "question_implementation_id": item.question_implementation_id,
        "catalog_row_sha256": item.catalog_row_sha256,
        "source_family": item.source_family,
        "canonical_wave": item.canonical_wave,
        "source_variable_code": item.source_variable_code,
        "country_scope": item.country_scope,
        "form_scope": item.form_scope,
        "module_scope": item.module_scope,
        "split_scope": item.split_scope,
        "member_applicability_scope_json": _canonical({"member": f"m{index}"}),
        "source_universe_filter_scope_json": _canonical({"universe": f"u{index}"}),
        "disposition": disposition,
        "evidence_authority_type": (
            "INSUFFICIENT_SOURCE_AUTHORITY"
            if unresolved
            else "FIXTURE_NATIVE_SOURCE_AUTHORITY"
        ),
        "evidence_authority_ref": "" if unresolved else evidence_ref,
        "evidence_authority_sha256": "" if unresolved else _sha_text(evidence_ref),
        "evidence_scope_json": _canonical(scope),
        "membership_basis": EXACT_MEMBERSHIP_BASIS,
        "predicate_contract_version": "fixture_predicate_v1" if predicate else "",
        "executable_predicate_json": _canonical(predicate) if predicate else "",
        "executable_predicate_sha256": (
            hashlib.sha256(_canonical(predicate).encode("utf-8")).hexdigest()
            if predicate
            else ""
        ),
        "replay_contract_version": "fixture_replay_v1" if predicate else "",
        "replay_input_ref": f"fixture://replay/{index}" if predicate else "",
        "unresolved_blocker_class": FIXTURE_BLOCKERS[index] if unresolved else "",
        "adjudication_provenance_ref": provenance_ref,
        "adjudication_provenance_sha256": _sha_text(provenance_ref),
    }


def _all_family_ledgers(catalog):
    return {
        family: [_ledger_row(catalog, index)]
        for index, family in enumerate(FAMILIES)
    }


def test_authority45_current_catalog_contract_is_exact_18276_surface():
    assert CATALOG_CONTRACT_VERSION == "authority45_layer1_35wave_active_catalog_v1"
    assert CURRENT_CATALOG_ARCHIVE_SHA256 == (
        "b569c3677514e627bccb6f920c7aefd7c1d7bb452eb906ddd8913a69d27dac7d"
    )
    assert CURRENT_CATALOG_TOTAL_ROWS == 18_276
    assert sum(spec.rows for spec in CURRENT_FAMILY_SPECS) == 18_276
    assert {spec.source_family: spec.rows for spec in CURRENT_FAMILY_SPECS} == {
        "GSS": 6021,
        "LiTS": 4434,
        "EVS": 2224,
        "Arab Barometer": 1698,
        "WVS": 1219,
        "Afrobarometer": 913,
        "Asian Barometer": 814,
        "Latinobarómetro": 812,
        "South Asia": 141,
    }
    assert {spec.source_family: spec.sha256 for spec in CURRENT_FAMILY_SPECS} == {
        "GSS": "74496af09f5feba9defc1d2991977e79343da97c87c1fce93f1e9ab4ada31b99",
        "LiTS": "068cd24a9bcbaaf0e8b70c6c384296884247467f09fd380753d941e09afd39ea",
        "EVS": "61c6f77d266e59f5218babecbd07636619ff90d04b4ffc837357204225729d3b",
        "Arab Barometer": "1111699fdde0bbd082267b1ba5eb3b76bbfdcf89aa1e08f500c8393200c394cf",
        "WVS": "cc538e7208e96f2a3333082e3ffdc88faf1bba0eee273664fe2ff213c3821ec0",
        "Afrobarometer": "01561b89960c10a77cec15552a8b065a0d043fe29c99bc77f4cb316991225181",
        "Asian Barometer": "b27afc4e1ba8bd5707db61388b592525467657d522e782a07c31d04d6b4430cd",
        "Latinobarómetro": "9993607de206a00ed1d6c63b599e5115dc0c1925bffcb10a81544eadaf83cf8c",
        "South Asia": "1e31a8bc40a76a921668497ad8268e4d048c5c19e65003d44424a89b5a4f73f1",
    }


def test_disposition_vocabulary_is_exact_authority45_set():
    assert DISPOSITIONS == {
        "GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE",
        "POSITIVE_EXECUTABLE_ROUTING_AUTHORITY",
        "GOVERNED_SCOPED_NONAPPLICABILITY",
        "ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT",
        "STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT",
    }


def test_fixture_join_is_deterministic_and_never_invents_dispositions(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    ledgers = _all_family_ledgers(catalog)
    a = compile_joined_ledger(ledgers, catalog=catalog)
    b = compile_joined_ledger(dict(reversed(list(ledgers.items()))), catalog=catalog)

    assert a["joined_ledger_sha256"] == FIXTURE_JOINED_HASH
    assert a["unresolved_summary_sha256"] == FIXTURE_UNRESOLVED_HASH
    assert b["joined_ledger_sha256"] == FIXTURE_JOINED_HASH
    assert b["unresolved_summary_sha256"] == FIXTURE_UNRESOLVED_HASH
    assert a["catalog_total_rows"] == 9
    assert a["unresolved_summary"]["unresolved_total"] == 4
    assert a["unresolved_summary"]["by_family_and_blocker"] == {
        "Afrobarometer": {"ROUTING_INSTRUCTION_UNAVAILABLE": 1},
        "Asian Barometer": {"ROUTING_INSTRUCTION_UNAVAILABLE": 1},
        "Latinobarómetro": {"NO_EXACT_SOURCE_AUTHORITY": 1},
        "WVS": {"NO_EXACT_SOURCE_AUTHORITY": 1},
    }
    assert [row["disposition"] for row in a["joined_rows"]].count(UNRESOLVED) == 4


def test_catalog_bytes_and_row_counts_are_hash_pinned(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    spec = catalog.contract.families[0]
    path = tmp_path / spec.filename
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(RoutingLedgerError, match="catalog byte hash mismatch"):
        load_catalog_bundle(tmp_path, contract=catalog.contract)

    # Even a newly hash-pinned file may not replace the governed cardinality.
    payload = path.read_bytes()
    mutated = replace(spec, sha256=hashlib.sha256(payload).hexdigest(), rows=2)
    contract = replace(
        catalog.contract,
        total_rows=10,
        families=(mutated,) + catalog.contract.families[1:],
    )
    with pytest.raises(RoutingLedgerError, match="catalog row count mismatch"):
        load_catalog_bundle(tmp_path, contract=contract)


def test_duplicate_and_extra_current_ids_fail_closed(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    row = _ledger_row(catalog, 0)
    with pytest.raises(RoutingLedgerError, match="duplicate ledger implementation ID"):
        validate_family_ledger([row, dict(row)], source_family="GSS", catalog=catalog)

    extra = dict(row)
    extra["question_implementation_id"] = "question_impl.not_current"
    with pytest.raises(RoutingLedgerError, match="extra/non-current implementation ID"):
        validate_family_ledger([extra], source_family="GSS", catalog=catalog)


def test_family_subset_cannot_be_promoted_by_historical_or_aggregate_membership(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    # A zero-row or old-partition-style subset cannot satisfy exact family membership.
    with pytest.raises(RoutingLedgerError, match="coverage mismatch"):
        validate_family_ledger([], source_family="GSS", catalog=catalog)

    row = _ledger_row(catalog, 0)
    row["catalog_row_sha256"] = "0" * 64
    with pytest.raises(RoutingLedgerError, match="catalog row hash mismatch"):
        validate_family_ledger([row], source_family="GSS", catalog=catalog)


@pytest.mark.parametrize("basis", sorted(FORBIDDEN_MEMBERSHIP_BASES))
def test_historical_700_99_600_699_counts_source_presence_and_inferred_completion_rejected(
    tmp_path: Path, basis: str
):
    catalog = _fixture_catalog(tmp_path)
    row = _ledger_row(catalog, 0)
    row["membership_basis"] = basis
    with pytest.raises(RoutingLedgerError, match="forbidden membership basis"):
        validate_family_ledger([row], source_family="GSS", catalog=catalog)


def test_all_nine_families_are_required_for_join(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    ledgers = _all_family_ledgers(catalog)
    ledgers.pop("South Asia")
    with pytest.raises(RoutingLedgerError, match="joined family set mismatch"):
        compile_joined_ledger(ledgers, catalog=catalog)


def test_exact_scope_and_scoped_nonapplicability_cannot_be_widened(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    row = _ledger_row(catalog, 1)
    scope = json.loads(row["evidence_scope_json"])
    scope["country_scope"] = "ALL"
    row["evidence_scope_json"] = _canonical(scope)
    with pytest.raises(RoutingLedgerError, match="omits or widens exact catalog scope"):
        validate_family_ledger([row], source_family="LiTS", catalog=catalog)

    row = _ledger_row(catalog, 1)
    row["country_scope"] = "ALL"
    scope = json.loads(row["evidence_scope_json"])
    scope["country_scope"] = "ALL"
    row["evidence_scope_json"] = _canonical(scope)
    with pytest.raises(RoutingLedgerError, match="ledger country_scope mismatch"):
        validate_family_ledger([row], source_family="LiTS", catalog=catalog)


def test_positive_predicate_requires_canonical_serialization_hash_and_replay(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    row = _ledger_row(catalog, 0)
    row["executable_predicate_sha256"] = "0" * 64
    with pytest.raises(RoutingLedgerError, match="executable predicate hash mismatch"):
        validate_family_ledger([row], source_family="GSS", catalog=catalog)

    row = _ledger_row(catalog, 0)
    row["replay_input_ref"] = ""
    with pytest.raises(RoutingLedgerError, match="requires predicate and replay"):
        validate_family_ledger([row], source_family="GSS", catalog=catalog)


def test_unresolved_stays_typed_and_cannot_smuggle_executable_semantics(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    row = _ledger_row(catalog, 4)
    row["unresolved_blocker_class"] = ""
    with pytest.raises(RoutingLedgerError, match="requires unresolved_blocker_class"):
        validate_family_ledger([row], source_family="WVS", catalog=catalog)

    row = _ledger_row(catalog, 4)
    row["predicate_contract_version"] = "invented"
    row["executable_predicate_json"] = _canonical({"op": "true"})
    row["executable_predicate_sha256"] = hashlib.sha256(
        row["executable_predicate_json"].encode("utf-8")
    ).hexdigest()
    row["replay_contract_version"] = "invented"
    row["replay_input_ref"] = "invented"
    with pytest.raises(RoutingLedgerError, match="may not carry executable predicate"):
        validate_family_ledger([row], source_family="WVS", catalog=catalog)


def test_resolved_row_requires_exact_evidence_hash_and_no_unresolved_blocker(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    row = _ledger_row(catalog, 2)
    row["evidence_authority_sha256"] = ""
    with pytest.raises(RoutingLedgerError, match="64-hex"):
        validate_family_ledger([row], source_family="EVS", catalog=catalog)

    row = _ledger_row(catalog, 2)
    row["unresolved_blocker_class"] = "SHOULD_NOT_EXIST"
    with pytest.raises(RoutingLedgerError, match="may not carry unresolved_blocker_class"):
        validate_family_ledger([row], source_family="EVS", catalog=catalog)


def test_catalog_identity_scope_and_variable_must_match_exact_current_row(tmp_path: Path):
    catalog = _fixture_catalog(tmp_path)
    row = _ledger_row(catalog, 3)
    row["source_variable_code"] = "OTHER"
    with pytest.raises(RoutingLedgerError, match="source_variable_code mismatch"):
        validate_family_ledger([row], source_family="Arab Barometer", catalog=catalog)

    row = _ledger_row(catalog, 3)
    scope = json.loads(row["evidence_scope_json"])
    scope["canonical_wave"] = "OTHER"
    row["evidence_scope_json"] = _canonical(scope)
    with pytest.raises(RoutingLedgerError, match="evidence scope canonical_wave mismatch"):
        validate_family_ledger([row], source_family="Arab Barometer", catalog=catalog)


def test_ledger_schema_columns_are_explicit_and_stable():
    assert len(LEDGER_COLUMNS) == 26
    assert LEDGER_COLUMNS[:6] == (
        "schema_version",
        "question_implementation_id",
        "catalog_row_sha256",
        "source_family",
        "canonical_wave",
        "source_variable_code",
    )
    assert "evidence_scope_json" in LEDGER_COLUMNS
    assert "member_applicability_scope_json" in LEDGER_COLUMNS
    assert "source_universe_filter_scope_json" in LEDGER_COLUMNS
    assert "executable_predicate_sha256" in LEDGER_COLUMNS
