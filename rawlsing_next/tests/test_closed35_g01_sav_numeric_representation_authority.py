from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

import pytest

from rawlsing_next.closed35_g01_sav_numeric_representation_authority import (
    APPLICABILITY_ROWS,
    AUTHORITY_KIND,
    AUTHORIZED_R5_TOKENS,
    CENSUS_RESULTS_HEAD,
    NEGATIVE_LIMITS,
    OPERATION,
    REPRESENTATION_AUTHORITY_REF,
    authorized_sav_numeric_physical_binding_key,
    authorized_sav_numeric_physical_material,
    representation_authority_snapshot,
)
from rawlsing_next.pre553_empirical_authority import validate_authority_snapshot
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-RESULTS-R1"
R5 = R5TypedValueCodec()
EXPECTED_SURFACES = {"S005", "S006", "S007", "S008", "S009", "S010", "S016", "S037", "S038"}


def _receipt(source_id: str):
    return json.loads(
        (RESULTS / "source_receipts" / f"SOURCE_{source_id}_REPRESENTATION_RECEIPT.json").read_text(
            encoding="utf-8"
        )
    )


def test_exact_nine_surface_g01_partition_is_frozen():
    assert CENSUS_RESULTS_HEAD == "b801c58c8e4d6d10e36e0a42ca62cf6908cbf25a"
    assert len(APPLICABILITY_ROWS) == 9
    assert {row["surface_id"] for row in APPLICABILITY_ROWS} == EXPECTED_SURFACES
    assert {row["source_id"] for row in APPLICABILITY_ROWS} == {"02", "06", "21"}
    assert all(row["readstat_variable_type"] == "double" for row in APPLICABILITY_ROWS)
    assert all(row["storage_width"] == 8 for row in APPLICABILITY_ROWS)


def test_authorized_material_matches_committed_qualified_census_witnesses():
    by_source = {sid: _receipt(sid) for sid in ("02", "06", "21")}
    for row in APPLICABILITY_ROWS:
        receipt = by_source[row["source_id"]]
        surface = next(s for s in receipt["surfaces"] if s["surface_id"] == row["surface_id"])
        assert surface["classification"] == "NEW_GENERIC_REPRESENTATION_REGIME_REQUIRED"
        assert surface["owner_key_status"] == "NATIVE_LITERAL_RULE_OWNER"
        assert surface["join_diagnostic"]["exact_join"] is False
        assert surface["numeric_coercion_used_for_join"] is False
        for native_code in row["native_codes"]:
            value, state, declaration = authorized_sav_numeric_physical_material(
                source_sha256=row["source_sha256"],
                variable_name=row["variable_name"],
                ordinal=row["ordinal"],
                native_code=native_code,
            )
            assert type(value) is float
            assert R5.encode(value) == AUTHORIZED_R5_TOKENS[native_code]
            key = authorized_sav_numeric_physical_binding_key(
                source_sha256=row["source_sha256"],
                variable_name=row["variable_name"],
                ordinal=row["ordinal"],
                native_code=native_code,
            )
            rule = next(
                x for x in surface["join_diagnostic"]["rule_results"]
                if x["native_rule_literal_r5"] == R5.encode(native_code)
            )
            assert rule["exact_typed_matches"] == []
            assert rule["non_authoritative_float_representation_diagnostic_matches"] == [key]
            assert key == physical_value_binding_key(value, state, declaration)


def test_g01_is_representation_succession_not_global_int_float_identity():
    for row in APPLICABILITY_ROWS:
        for native_code in row["native_codes"]:
            value, state, declaration = authorized_sav_numeric_physical_material(
                source_sha256=row["source_sha256"],
                variable_name=row["variable_name"],
                ordinal=row["ordinal"],
                native_code=native_code,
            )
            assert R5.encode(native_code) != R5.encode(value)
            assert physical_value_binding_key(native_code, state, declaration) != physical_value_binding_key(
                value, state, declaration
            )
    assert R5.encode(1) != R5.encode(1.0)
    assert R5.encode(1.0) != R5.encode(Decimal("1.0"))


def test_q10b_997_preserves_user_missing_state_and_exact_declaration():
    row = next(r for r in APPLICABILITY_ROWS if r["surface_id"] == "S016")
    value, state, declaration = authorized_sav_numeric_physical_material(
        source_sha256=row["source_sha256"],
        variable_name="Q10B",
        ordinal=58,
        native_code=997,
    )
    assert value == 997.0
    assert state is PhysicalMissingState.FORMAT_USER_MISSING_VALUE
    assert declaration == {"kind": "discrete", "value": 997.0}


@pytest.mark.parametrize("hostile", [1.0, "1", True, Decimal("1")])
def test_non_int_native_code_types_fail_closed(hostile):
    row = next(r for r in APPLICABILITY_ROWS if r["surface_id"] == "S005")
    with pytest.raises(ValueError, match="native code/type"):
        authorized_sav_numeric_physical_material(
            source_sha256=row["source_sha256"],
            variable_name=row["variable_name"],
            ordinal=row["ordinal"],
            native_code=hostile,
        )


def test_source_variable_ordinal_and_code_applicability_are_exact():
    row = next(r for r in APPLICABILITY_ROWS if r["surface_id"] == "S037")
    base = dict(
        source_sha256=row["source_sha256"],
        variable_name=row["variable_name"],
        ordinal=row["ordinal"],
        native_code=98,
    )
    hostile_cases = [
        {**base, "source_sha256": "0" * 64},
        {**base, "variable_name": "Q101_OTHER"},
        {**base, "ordinal": row["ordinal"] + 1},
        {**base, "native_code": 97},
        {**base, "native_code": 100},
    ]
    for case in hostile_cases:
        with pytest.raises(ValueError):
            authorized_sav_numeric_physical_material(**case)


def test_authority_snapshot_is_valid_and_negative_limits_are_explicit():
    snapshot = representation_authority_snapshot()
    assert validate_authority_snapshot(snapshot) == snapshot
    assert snapshot.authority_ref == REPRESENTATION_AUTHORITY_REF
    assert snapshot.authority_kind == AUTHORITY_KIND
    assert OPERATION in snapshot.governed_operations
    for limit in (
        "NO_GLOBAL_INT_FLOAT_COERCION",
        "NO_ARITHMETIC_MAGNITUDE_IDENTITY",
        "NO_OTHER_SOURCES",
        "NO_OTHER_VARIABLES",
        "NO_OTHER_NATIVE_CODES",
        "NO_DTA_APPLICABILITY",
        "NO_LABEL_OR_DISPLAY_SEMANTICS",
        "NO_MISSING_STATE_REINTERPRETATION",
        "NO_CANDIDATE_OUTPUT_PARENTAGE",
    ):
        assert limit in NEGATIVE_LIMITS
