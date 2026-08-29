"""Authority-45 current routing/applicability ledger compiler and coverage validator.

This module is deliberately authority-neutral.  It validates that future
source-family adjudication ledgers cover the exact governed 18,276 current
question-implementation universe and that every supplied disposition preserves
its declared evidence/scope/replay information.  It never derives a routing
disposition from catalog metadata.

Historical 700/99/600/699 trial partitions are forensic regression material
only and are rejected as membership authority.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = "authority45_current_routing_disposition_v1"
CATALOG_CONTRACT_VERSION = "authority45_layer1_35wave_active_catalog_v1"
CURRENT_CATALOG_ARCHIVE_NAME = "LAYER1_GOVERNED_35WAVE_CATALOGS.zip"
CURRENT_CATALOG_ARCHIVE_SHA256 = (
    "b569c3677514e627bccb6f920c7aefd7c1d7bb452eb906ddd8913a69d27dac7d"
)
CURRENT_CATALOG_TOTAL_ROWS = 18_276
CURRENT_CATALOG_ACTIVE_SCOPES = 35

DISPOSITIONS = frozenset(
    {
        "GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE",
        "POSITIVE_EXECUTABLE_ROUTING_AUTHORITY",
        "GOVERNED_SCOPED_NONAPPLICABILITY",
        "ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT",
        "STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT",
    }
)

UNRESOLVED = "STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT"
POSITIVE_ROUTING = "POSITIVE_EXECUTABLE_ROUTING_AUTHORITY"
SCOPED_NONAPPLICABILITY = "GOVERNED_SCOPED_NONAPPLICABILITY"

EXACT_MEMBERSHIP_BASIS = "EXACT_CURRENT_IMPLEMENTATION_CATALOG_ID"
FORBIDDEN_MEMBERSHIP_BASES = frozenset(
    {
        "HISTORICAL_700_TRIAL_SET",
        "HISTORICAL_99_SOURCE_SIGNALED",
        "HISTORICAL_600_LMQ004",
        "HISTORICAL_699_UNRESOLVED",
        "AGGREGATE_COUNT",
        "SOURCE_COLUMN_PRESENCE",
        "INFERRED_COMPLETION",
        "QUESTION_TEXT_OR_THEME",
        "NEIGHBORING_WAVE_ANALOGY",
    }
)

WIDENING_SCOPE_TOKENS = frozenset({"*", "ALL", "GLOBAL", "ANY", "ALL_COUNTRIES", "ALL_WAVES"})

LEDGER_COLUMNS = (
    "schema_version",
    "question_implementation_id",
    "catalog_row_sha256",
    "source_family",
    "canonical_wave",
    "source_variable_code",
    "country_scope",
    "form_scope",
    "module_scope",
    "split_scope",
    "member_applicability_scope_json",
    "source_universe_filter_scope_json",
    "disposition",
    "evidence_authority_type",
    "evidence_authority_ref",
    "evidence_authority_sha256",
    "evidence_scope_json",
    "membership_basis",
    "predicate_contract_version",
    "executable_predicate_json",
    "executable_predicate_sha256",
    "replay_contract_version",
    "replay_input_ref",
    "unresolved_blocker_class",
    "adjudication_provenance_ref",
    "adjudication_provenance_sha256",
)

IDENTITY_ALIASES = ("question_implementation_id", "implementation_id")
FAMILY_ALIASES = ("source_family", "source")
WAVE_ALIASES = ("canonical_wave", "wave")
VARIABLE_ALIASES = ("source_variable_code", "var_code", "var_name", "source_var_code")
COUNTRY_ALIASES = ("country_code", "country_code_scope", "country")
FORM_ALIASES = ("form", "form_scope", "form_id")
MODULE_ALIASES = ("module", "module_scope", "module_id")
SPLIT_ALIASES = ("split", "split_scope", "split_id")


class RoutingLedgerError(RuntimeError):
    """Fail-closed validation error for the Authority-45 routing ledger."""


@dataclass(frozen=True)
class FamilyCatalogSpec:
    source_family: str
    filename: str
    rows: int
    sha256: str


@dataclass(frozen=True)
class CatalogContract:
    contract_version: str
    archive_name: str
    archive_sha256: str
    total_rows: int
    active_scopes: int
    families: tuple[FamilyCatalogSpec, ...]


CURRENT_FAMILY_SPECS = (
    FamilyCatalogSpec(
        "GSS",
        "Rawlsing_P2_GSS_Deep_Question_Node_Catalog_v1.csv",
        6021,
        "74496af09f5feba9defc1d2991977e79343da97c87c1fce93f1e9ab4ada31b99",
    ),
    FamilyCatalogSpec(
        "LiTS",
        "Rawlsing_P2_LiTS_Deep_Question_Node_Catalog_v2.csv",
        4434,
        "068cd24a9bcbaaf0e8b70c6c384296884247467f09fd380753d941e09afd39ea",
    ),
    FamilyCatalogSpec(
        "EVS",
        "Rawlsing_P2_EVS_Deep_Question_Node_Catalog_v1.csv",
        2224,
        "61c6f77d266e59f5218babecbd07636619ff90d04b4ffc837357204225729d3b",
    ),
    FamilyCatalogSpec(
        "Arab Barometer",
        "Rawlsing_P2_Arab_Barometer_Deep_Question_Node_Catalog_v1.csv",
        1698,
        "1111699fdde0bbd082267b1ba5eb3b76bbfdcf89aa1e08f500c8393200c394cf",
    ),
    FamilyCatalogSpec(
        "WVS",
        "Rawlsing_P2_WVS_Deep_Question_Node_Catalog_v1.csv",
        1219,
        "cc538e7208e96f2a3333082e3ffdc88faf1bba0eee273664fe2ff213c3821ec0",
    ),
    FamilyCatalogSpec(
        "Afrobarometer",
        "Rawlsing_P2_Afrobarometer_Deep_Question_Node_Catalog_v1.csv",
        913,
        "01561b89960c10a77cec15552a8b065a0d043fe29c99bc77f4cb316991225181",
    ),
    FamilyCatalogSpec(
        "Asian Barometer",
        "Rawlsing_P2_Asian_Barometer_Deep_Question_Node_Catalog_v2.csv",
        814,
        "b27afc4e1ba8bd5707db61388b592525467657d522e782a07c31d04d6b4430cd",
    ),
    FamilyCatalogSpec(
        "Latinobarómetro",
        "Rawlsing_P2_Latinobarometro_Deep_Question_Node_Catalog_v2.csv",
        812,
        "9993607de206a00ed1d6c63b599e5115dc0c1925bffcb10a81544eadaf83cf8c",
    ),
    FamilyCatalogSpec(
        "South Asia",
        "Rawlsing_P2_South_Asia_Deep_Question_Node_Catalog_v2.csv",
        141,
        "1e31a8bc40a76a921668497ad8268e4d048c5c19e65003d44424a89b5a4f73f1",
    ),
)

CURRENT_CATALOG_CONTRACT = CatalogContract(
    contract_version=CATALOG_CONTRACT_VERSION,
    archive_name=CURRENT_CATALOG_ARCHIVE_NAME,
    archive_sha256=CURRENT_CATALOG_ARCHIVE_SHA256,
    total_rows=CURRENT_CATALOG_TOTAL_ROWS,
    active_scopes=CURRENT_CATALOG_ACTIVE_SCOPES,
    families=CURRENT_FAMILY_SPECS,
)


@dataclass(frozen=True)
class CatalogRow:
    question_implementation_id: str
    source_family: str
    canonical_wave: str
    source_variable_code: str
    country_scope: str
    form_scope: str
    module_scope: str
    split_scope: str
    catalog_row_sha256: str
    raw: Mapping[str, str]


@dataclass(frozen=True)
class CatalogBundle:
    contract: CatalogContract
    rows_by_id: Mapping[str, CatalogRow]
    family_ids: Mapping[str, frozenset[str]]
    family_file_sha256: Mapping[str, str]


def _clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_json(value: Any) -> str:
    return _sha256_bytes(_canonical_json(value).encode("utf-8"))


def _require_sha256(value: str, field: str, *, allow_empty: bool = False) -> str:
    value = _clean(value).lower()
    if allow_empty and not value:
        return ""
    if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise RoutingLedgerError(f"{field} must be a lowercase 64-hex SHA-256")
    return value


def _first(row: Mapping[str, str], aliases: Sequence[str], *, required: bool = False) -> str:
    for key in aliases:
        if key in row and _clean(row[key]):
            return _clean(row[key])
    if required:
        raise RoutingLedgerError(f"catalog row missing required identity column from {tuple(aliases)}")
    return ""


def _normalized_catalog_row(row: Mapping[str, str]) -> dict[str, str]:
    return {str(k): _clean(v) for k, v in sorted(row.items())}


def _catalog_row(row: Mapping[str, str], expected_family: str) -> CatalogRow:
    normalized = _normalized_catalog_row(row)
    implementation_id = _first(normalized, IDENTITY_ALIASES, required=True)
    family = _first(normalized, FAMILY_ALIASES, required=True)
    if family != expected_family:
        raise RoutingLedgerError(
            f"catalog family mismatch for {implementation_id}: {family!r} != {expected_family!r}"
        )
    wave = _first(normalized, WAVE_ALIASES, required=True)
    var_code = _first(normalized, VARIABLE_ALIASES, required=True)
    return CatalogRow(
        question_implementation_id=implementation_id,
        source_family=family,
        canonical_wave=wave,
        source_variable_code=var_code,
        country_scope=_first(normalized, COUNTRY_ALIASES),
        form_scope=_first(normalized, FORM_ALIASES),
        module_scope=_first(normalized, MODULE_ALIASES),
        split_scope=_first(normalized, SPLIT_ALIASES),
        catalog_row_sha256=_sha256_json(normalized),
        raw=normalized,
    )


def _read_csv_bytes(path: Path) -> tuple[bytes, list[dict[str, str]]]:
    payload = path.read_bytes()
    text = payload.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    if reader.fieldnames is None:
        raise RoutingLedgerError(f"CSV has no header: {path}")
    return payload, [dict(row) for row in reader]


def load_catalog_bundle(
    catalog_dir: str | Path,
    *,
    contract: CatalogContract = CURRENT_CATALOG_CONTRACT,
) -> CatalogBundle:
    """Load and hash-pin the exact governed family catalogs.

    The production contract accepts only the Authority-45/A07 family bytes.  A
    custom contract is exposed solely so tests and future superseding authority
    can exercise the compiler without weakening the default current contract.
    """

    root = Path(catalog_dir)
    if sum(spec.rows for spec in contract.families) != contract.total_rows:
        raise RoutingLedgerError("catalog contract family counts do not sum to total_rows")

    rows_by_id: dict[str, CatalogRow] = {}
    family_ids: dict[str, frozenset[str]] = {}
    family_hashes: dict[str, str] = {}

    for spec in contract.families:
        path = root / spec.filename
        if not path.is_file():
            raise RoutingLedgerError(f"missing governed family catalog: {path}")
        payload, rows = _read_csv_bytes(path)
        actual_hash = _sha256_bytes(payload)
        if actual_hash != spec.sha256:
            raise RoutingLedgerError(
                f"catalog byte hash mismatch for {spec.source_family}: {actual_hash} != {spec.sha256}"
            )
        if len(rows) != spec.rows:
            raise RoutingLedgerError(
                f"catalog row count mismatch for {spec.source_family}: {len(rows)} != {spec.rows}"
            )

        ids: set[str] = set()
        for raw in rows:
            item = _catalog_row(raw, spec.source_family)
            if item.question_implementation_id in ids:
                raise RoutingLedgerError(
                    f"duplicate implementation ID inside {spec.source_family}: "
                    f"{item.question_implementation_id}"
                )
            if item.question_implementation_id in rows_by_id:
                raise RoutingLedgerError(
                    f"implementation ID appears in multiple families: {item.question_implementation_id}"
                )
            ids.add(item.question_implementation_id)
            rows_by_id[item.question_implementation_id] = item

        family_ids[spec.source_family] = frozenset(ids)
        family_hashes[spec.source_family] = actual_hash

    if len(rows_by_id) != contract.total_rows:
        raise RoutingLedgerError(
            f"catalog coverage mismatch: {len(rows_by_id)} != {contract.total_rows}"
        )

    return CatalogBundle(
        contract=contract,
        rows_by_id=rows_by_id,
        family_ids=family_ids,
        family_file_sha256=family_hashes,
    )


def _parse_json_object(raw: str, field: str, *, allow_empty: bool = False) -> dict[str, Any]:
    raw = _clean(raw)
    if allow_empty and not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RoutingLedgerError(f"{field} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise RoutingLedgerError(f"{field} must serialize a JSON object")
    return value


def _scope_value(scope: Mapping[str, Any], key: str) -> str:
    return _clean(scope.get(key))


def _reject_widening_token(value: str, field: str) -> None:
    if value.upper() in WIDENING_SCOPE_TOKENS:
        raise RoutingLedgerError(f"{field} uses forbidden widening token {value!r}")


def _validate_evidence_scope(row: Mapping[str, str], catalog: CatalogRow) -> dict[str, Any]:
    scope = _parse_json_object(row["evidence_scope_json"], "evidence_scope_json")
    required = {
        "question_implementation_id": catalog.question_implementation_id,
        "source_family": catalog.source_family,
        "canonical_wave": catalog.canonical_wave,
    }
    for key, expected in required.items():
        actual = _scope_value(scope, key)
        if actual != expected:
            raise RoutingLedgerError(
                f"evidence scope {key} mismatch for {catalog.question_implementation_id}: "
                f"{actual!r} != {expected!r}"
            )

    optional = {
        "country_scope": catalog.country_scope,
        "form_scope": catalog.form_scope,
        "module_scope": catalog.module_scope,
        "split_scope": catalog.split_scope,
    }
    for key, expected in optional.items():
        actual = _scope_value(scope, key)
        explicit = _clean(row[key])
        if expected:
            if explicit != expected:
                raise RoutingLedgerError(
                    f"ledger {key} mismatch for {catalog.question_implementation_id}: "
                    f"{explicit!r} != {expected!r}"
                )
            if actual != expected:
                raise RoutingLedgerError(
                    f"evidence scope {key} omits or widens exact catalog scope for "
                    f"{catalog.question_implementation_id}"
                )
        else:
            if explicit and actual != explicit:
                raise RoutingLedgerError(
                    f"evidence scope {key} must preserve ledger scope {explicit!r}"
                )

    if row["disposition"] == SCOPED_NONAPPLICABILITY:
        for key in (
            "question_implementation_id",
            "source_family",
            "canonical_wave",
            "country_scope",
            "form_scope",
            "module_scope",
            "split_scope",
        ):
            value = _scope_value(scope, key)
            if value:
                _reject_widening_token(value, f"evidence_scope_json.{key}")
    return scope


def _validate_scope_json_field(
    raw: str,
    field: str,
    *,
    reject_widening: bool = False,
) -> dict[str, Any]:
    value = _parse_json_object(raw, field, allow_empty=True)
    if reject_widening:
        for key, item in value.items():
            if isinstance(item, str):
                _reject_widening_token(item, f"{field}.{key}")
    return value


def _validate_predicate_contract(row: Mapping[str, str]) -> str:
    disposition = row["disposition"]
    predicate_json = _clean(row["executable_predicate_json"])
    predicate_hash = _clean(row["executable_predicate_sha256"])
    predicate_version = _clean(row["predicate_contract_version"])
    replay_version = _clean(row["replay_contract_version"])
    replay_ref = _clean(row["replay_input_ref"])

    if disposition == POSITIVE_ROUTING:
        if not predicate_version or not replay_version or not replay_ref:
            raise RoutingLedgerError(
                "positive executable routing requires predicate and replay contract/version refs"
            )
        predicate = _parse_json_object(predicate_json, "executable_predicate_json")
        canonical_predicate = _canonical_json(predicate)
        expected = _sha256_json(predicate)
        if _require_sha256(predicate_hash, "executable_predicate_sha256") != expected:
            raise RoutingLedgerError(
                f"executable predicate hash mismatch: {predicate_hash} != {expected}"
            )
        return canonical_predicate
    else:
        if predicate_json or predicate_hash or predicate_version or replay_version or replay_ref:
            raise RoutingLedgerError(
                f"{disposition} may not carry executable predicate/replay semantics"
            )
        return ""


def _validate_ledger_row(raw: Mapping[str, str], catalog: CatalogRow) -> dict[str, str]:
    missing = [column for column in LEDGER_COLUMNS if column not in raw]
    if missing:
        raise RoutingLedgerError(f"ledger row missing required columns: {missing}")
    row = {column: _clean(raw.get(column)) for column in LEDGER_COLUMNS}

    if row["schema_version"] != SCHEMA_VERSION:
        raise RoutingLedgerError(f"unexpected routing ledger schema: {row['schema_version']!r}")
    if row["question_implementation_id"] != catalog.question_implementation_id:
        raise RoutingLedgerError("ledger implementation identity mismatch")
    if _require_sha256(row["catalog_row_sha256"], "catalog_row_sha256") != catalog.catalog_row_sha256:
        raise RoutingLedgerError(
            f"catalog row hash mismatch for {catalog.question_implementation_id}"
        )
    if row["source_family"] != catalog.source_family:
        raise RoutingLedgerError(f"source_family mismatch for {catalog.question_implementation_id}")
    if row["canonical_wave"] != catalog.canonical_wave:
        raise RoutingLedgerError(f"canonical_wave mismatch for {catalog.question_implementation_id}")
    if row["source_variable_code"] != catalog.source_variable_code:
        raise RoutingLedgerError(f"source_variable_code mismatch for {catalog.question_implementation_id}")

    if row["membership_basis"] in FORBIDDEN_MEMBERSHIP_BASES:
        raise RoutingLedgerError(
            f"forbidden membership basis: {row['membership_basis']}"
        )
    if row["membership_basis"] != EXACT_MEMBERSHIP_BASIS:
        raise RoutingLedgerError(
            f"membership_basis must be {EXACT_MEMBERSHIP_BASIS}"
        )

    disposition = row["disposition"]
    if disposition not in DISPOSITIONS:
        raise RoutingLedgerError(f"unknown Authority-45 disposition: {disposition!r}")

    evidence_type = row["evidence_authority_type"]
    if not evidence_type:
        raise RoutingLedgerError("evidence_authority_type must remain explicit")
    evidence_ref = row["evidence_authority_ref"]
    evidence_hash = row["evidence_authority_sha256"]
    if disposition == UNRESOLVED:
        if not row["unresolved_blocker_class"]:
            raise RoutingLedgerError("typed unresolved row requires unresolved_blocker_class")
        if evidence_ref or evidence_hash:
            if not evidence_ref or not evidence_hash:
                raise RoutingLedgerError(
                    "partial evidence reference must preserve both ref and SHA-256"
                )
            _require_sha256(evidence_hash, "evidence_authority_sha256")
    else:
        if row["unresolved_blocker_class"]:
            raise RoutingLedgerError(
                "resolved disposition may not carry unresolved_blocker_class"
            )
        if not evidence_ref:
            raise RoutingLedgerError("resolved disposition requires evidence_authority_ref")
        _require_sha256(evidence_hash, "evidence_authority_sha256")

    evidence_scope = _validate_evidence_scope(row, catalog)
    member_scope = _validate_scope_json_field(
        row["member_applicability_scope_json"],
        "member_applicability_scope_json",
        reject_widening=(disposition == SCOPED_NONAPPLICABILITY),
    )
    universe_scope = _validate_scope_json_field(
        row["source_universe_filter_scope_json"],
        "source_universe_filter_scope_json",
        reject_widening=(disposition == SCOPED_NONAPPLICABILITY),
    )
    canonical_predicate = _validate_predicate_contract(row)
    row["evidence_scope_json"] = _canonical_json(evidence_scope)
    row["member_applicability_scope_json"] = _canonical_json(member_scope)
    row["source_universe_filter_scope_json"] = _canonical_json(universe_scope)
    row["executable_predicate_json"] = canonical_predicate

    if not row["adjudication_provenance_ref"]:
        raise RoutingLedgerError("adjudication_provenance_ref is required")
    _require_sha256(row["adjudication_provenance_sha256"], "adjudication_provenance_sha256")
    return row


def read_family_ledger(path: str | Path) -> list[dict[str, str]]:
    payload = Path(path).read_text(encoding="utf-8-sig")
    reader = csv.DictReader(io.StringIO(payload, newline=""))
    if reader.fieldnames is None:
        raise RoutingLedgerError(f"ledger CSV has no header: {path}")
    missing = [column for column in LEDGER_COLUMNS if column not in reader.fieldnames]
    if missing:
        raise RoutingLedgerError(f"ledger missing required columns: {missing}")
    return [dict(row) for row in reader]


def validate_family_ledger(
    rows: Iterable[Mapping[str, str]],
    *,
    source_family: str,
    catalog: CatalogBundle,
) -> tuple[dict[str, str], ...]:
    if source_family not in catalog.family_ids:
        raise RoutingLedgerError(f"source family not in current catalog contract: {source_family}")
    expected_ids = catalog.family_ids[source_family]
    seen: set[str] = set()
    validated: list[dict[str, str]] = []

    for raw in rows:
        implementation_id = _clean(raw.get("question_implementation_id"))
        if not implementation_id:
            raise RoutingLedgerError("ledger row missing question_implementation_id")
        if implementation_id in seen:
            raise RoutingLedgerError(f"duplicate ledger implementation ID: {implementation_id}")
        seen.add(implementation_id)
        if implementation_id not in expected_ids:
            if implementation_id in catalog.rows_by_id:
                raise RoutingLedgerError(
                    f"ledger for {source_family} contains implementation from another family: "
                    f"{implementation_id}"
                )
            raise RoutingLedgerError(
                f"ledger contains extra/non-current implementation ID: {implementation_id}"
            )
        validated.append(
            _validate_ledger_row(raw, catalog.rows_by_id[implementation_id])
        )

    missing = expected_ids - seen
    extra = seen - expected_ids
    if missing or extra:
        raise RoutingLedgerError(
            f"{source_family} ledger coverage mismatch: "
            f"expected={len(expected_ids)} observed={len(seen)} "
            f"missing={len(missing)} extra={len(extra)}"
        )

    return tuple(sorted(validated, key=lambda row: row["question_implementation_id"]))


def compile_joined_ledger(
    family_ledgers: Mapping[str, Iterable[Mapping[str, str]]],
    *,
    catalog: CatalogBundle,
) -> dict[str, Any]:
    expected_families = tuple(spec.source_family for spec in catalog.contract.families)
    if set(family_ledgers) != set(expected_families):
        missing = sorted(set(expected_families) - set(family_ledgers))
        extra = sorted(set(family_ledgers) - set(expected_families))
        raise RoutingLedgerError(
            f"joined family set mismatch: missing={missing} extra={extra}"
        )

    joined: list[dict[str, str]] = []
    family_counts: dict[str, int] = {}
    for family in expected_families:
        validated = validate_family_ledger(
            family_ledgers[family], source_family=family, catalog=catalog
        )
        family_counts[family] = len(validated)
        joined.extend(validated)

    if len(joined) != catalog.contract.total_rows:
        raise RoutingLedgerError(
            f"joined coverage mismatch: {len(joined)} != {catalog.contract.total_rows}"
        )
    joined.sort(key=lambda row: (row["source_family"], row["question_implementation_id"]))

    joined_hash = _sha256_json(joined)
    unresolved: dict[str, dict[str, int]] = {}
    unresolved_total = 0
    for row in joined:
        if row["disposition"] != UNRESOLVED:
            continue
        unresolved_total += 1
        family = row["source_family"]
        blocker = row["unresolved_blocker_class"]
        unresolved.setdefault(family, {})
        unresolved[family][blocker] = unresolved[family].get(blocker, 0) + 1

    unresolved_summary = {
        "schema_version": SCHEMA_VERSION,
        "catalog_contract_version": catalog.contract.contract_version,
        "catalog_archive_sha256": catalog.contract.archive_sha256,
        "total_current_implementations": len(joined),
        "unresolved_total": unresolved_total,
        "by_family_and_blocker": {
            family: dict(sorted(blockers.items()))
            for family, blockers in sorted(unresolved.items())
        },
    }
    unresolved_hash = _sha256_json(unresolved_summary)

    return {
        "schema_version": SCHEMA_VERSION,
        "catalog_contract_version": catalog.contract.contract_version,
        "catalog_archive_name": catalog.contract.archive_name,
        "catalog_archive_sha256": catalog.contract.archive_sha256,
        "catalog_total_rows": catalog.contract.total_rows,
        "family_counts": family_counts,
        "joined_rows": joined,
        "joined_ledger_sha256": joined_hash,
        "unresolved_summary": unresolved_summary,
        "unresolved_summary_sha256": unresolved_hash,
    }


def write_compilation(result: Mapping[str, Any], output_dir: str | Path) -> None:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)

    joined = result["joined_rows"]
    with (root / "CURRENT_ROUTING_DISPOSITION_LEDGER.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=LEDGER_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(joined)

    (root / "UNRESOLVED_SUMMARY.json").write_text(
        json.dumps(result["unresolved_summary"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    receipt = {key: value for key, value in result.items() if key != "joined_rows"}
    (root / "COMPILATION_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-dir", required=True)
    parser.add_argument("--ledger", action="append", default=[], metavar="FAMILY=CSV")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    catalog = load_catalog_bundle(args.catalog_dir)
    ledgers: dict[str, list[dict[str, str]]] = {}
    for raw in args.ledger:
        if "=" not in raw:
            raise RoutingLedgerError("--ledger must be FAMILY=CSV")
        family, path = raw.split("=", 1)
        family = family.strip()
        if family in ledgers:
            raise RoutingLedgerError(f"duplicate --ledger family: {family}")
        ledgers[family] = read_family_ledger(path)

    result = compile_joined_ledger(ledgers, catalog=catalog)
    write_compilation(result, args.output_dir)
    print(
        json.dumps(
            {
                "status": "PASS_EXACT_CURRENT_ROUTING_LEDGER_COVERAGE",
                "rows": result["catalog_total_rows"],
                "joined_ledger_sha256": result["joined_ledger_sha256"],
                "unresolved_summary_sha256": result["unresolved_summary_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
