from __future__ import annotations

from decimal import Decimal

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


R5 = R5TypedValueCodec()

# Current-baseline port of the already-frozen independent G01 oracle.
# These fixtures are exact documentary constants; this test does not import or
# resurrect the historical CLOSED35 qualified-census receipt tree.
EXPECTED_ROWS = (
    {
        "surface_id": "S016",
        "source_id": "02",
        "source_sha256": "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
        "variable_name": "Q10B",
        "ordinal": 58,
        "native_codes": (997,),
    },
    {
        "surface_id": "S037",
        "source_id": "06",
        "source_sha256": "6a5cbad637ce1546833a1d4812ba6d1e8d75f85b5b199b0cf3ec5cf456068dbc",
        "variable_name": "Q101",
        "ordinal": 20,
        "native_codes": (98, 99),
    },
    {
        "surface_id": "S038",
        "source_id": "06",
        "source_sha256": "6a5cbad637ce1546833a1d4812ba6d1e8d75f85b5b199b0cf3ec5cf456068dbc",
        "variable_name": "Q2061B",
        "ordinal": 19,
        "native_codes": (97,),
    },
    {
        "surface_id": "S005",
        "source_id": "21",
        "source_sha256": "c229aff7430c12f246678f385e0776b089681ae9830bac88423e0964ac34ee05",
        "variable_name": "abdefect",
        "ordinal": 5,
        "native_codes": (1, 2),
    },
    {
        "surface_id": "S006",
        "source_id": "21",
        "source_sha256": "c229aff7430c12f246678f385e0776b089681ae9830bac88423e0964ac34ee05",
        "variable_name": "abhlth",
        "ordinal": 6,
        "native_codes": (1, 2),
    },
    {
        "surface_id": "S007",
        "source_id": "21",
        "source_sha256": "c229aff7430c12f246678f385e0776b089681ae9830bac88423e0964ac34ee05",
        "variable_name": "abrape",
        "ordinal": 9,
        "native_codes": (1, 2),
    },
    {
        "surface_id": "S008",
        "source_id": "21",
        "source_sha256": "c229aff7430c12f246678f385e0776b089681ae9830bac88423e0964ac34ee05",
        "variable_name": "abany",
        "ordinal": 4,
        "native_codes": (1, 2),
    },
    {
        "surface_id": "S009",
        "source_id": "21",
        "source_sha256": "c229aff7430c12f246678f385e0776b089681ae9830bac88423e0964ac34ee05",
        "variable_name": "absingle",
        "ordinal": 10,
        "native_codes": (1, 2),
    },
    {
        "surface_id": "S010",
        "source_id": "21",
        "source_sha256": "c229aff7430c12f246678f385e0776b089681ae9830bac88423e0964ac34ee05",
        "variable_name": "abnomore",
        "ordinal": 7,
        "native_codes": (1, 2),
    },
)


def _public_row(row):
    return {
        "surface_id": row["surface_id"],
        "source_id": row["source_id"],
        "source_sha256": row["source_sha256"],
        "variable_name": row["variable_name"],
        "ordinal": row["ordinal"],
        "native_codes": tuple(row["native_codes"]),
    }


def test_exact_nine_surface_current_port_matches_frozen_oracle():
    assert CENSUS_RESULTS_HEAD == "b801c58c8e4d6d10e36e0a42ca62cf6908cbf25a"
    assert len(APPLICABILITY_ROWS) == 9
    assert tuple(_public_row(row) for row in APPLICABILITY_ROWS) == EXPECTED_ROWS
    assert {row["source_id"] for row in APPLICABILITY_ROWS} == {"02", "06", "21"}
    assert all(row["readstat_variable_type"] == "double" for row in APPLICABILITY_ROWS)
    assert all(row["storage_width"] == 8 for row in APPLICABILITY_ROWS)


def test_every_authorized_successor_is_exact_float64_material_not_type_collapse():
    for row in APPLICABILITY_ROWS:
        for native_code in row["native_codes"]:
            value, state, declaration = authorized_sav_numeric_physical_material(
                source_sha256=row["source_sha256"],
                variable_name=row["variable_name"],
                ordinal=row["ordinal"],
                native_code=native_code,
            )
            assert type(value) is float
            assert R5.encode(value) == AUTHORIZED_R5_TOKENS[native_code]
            assert R5.encode(native_code) != R5.encode(value)
            assert physical_value_binding_key(native_code, state, declaration) != physical_value_binding_key(
                value, state, declaration
            )
            assert authorized_sav_numeric_physical_binding_key(
                source_sha256=row["source_sha256"],
                variable_name=row["variable_name"],
                ordinal=row["ordinal"],
                native_code=native_code,
            ) == physical_value_binding_key(value, state, declaration)
    assert R5.encode(1) != R5.encode(1.0)
    assert R5.encode(1.0) != R5.encode(Decimal("1.0"))


def test_q10b_997_preserves_exact_user_missing_physical_state():
    row = next(row for row in APPLICABILITY_ROWS if row["surface_id"] == "S016")
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
def test_wrong_native_code_type_fails_closed(hostile):
    row = next(row for row in APPLICABILITY_ROWS if row["surface_id"] == "S005")
    with pytest.raises(ValueError, match="native code/type"):
        authorized_sav_numeric_physical_material(
            source_sha256=row["source_sha256"],
            variable_name=row["variable_name"],
            ordinal=row["ordinal"],
            native_code=hostile,
        )


def test_wrong_source_variable_ordinal_and_code_fail_closed():
    row = next(row for row in APPLICABILITY_ROWS if row["surface_id"] == "S037")
    base = {
        "source_sha256": row["source_sha256"],
        "variable_name": row["variable_name"],
        "ordinal": row["ordinal"],
        "native_code": 98,
    }
    hostile_cases = (
        {**base, "source_sha256": "0" * 64},
        {**base, "variable_name": "Q101_OTHER"},
        {**base, "ordinal": row["ordinal"] + 1},
        {**base, "native_code": 97},
        {**base, "native_code": 100},
    )
    for case in hostile_cases:
        with pytest.raises(ValueError):
            authorized_sav_numeric_physical_material(**case)


def test_authority_snapshot_is_bounded_to_representation_only():
    snapshot = representation_authority_snapshot()
    assert validate_authority_snapshot(snapshot) == snapshot
    assert snapshot.authority_ref == REPRESENTATION_AUTHORITY_REF
    assert snapshot.authority_kind == AUTHORITY_KIND
    assert OPERATION in snapshot.governed_operations
    assert snapshot.scope_envelope["representation_ceiling"] == "PHYSICAL_DECODER_REPRESENTATION_ONLY"
    for limit in (
        "NO_GLOBAL_INT_FLOAT_COERCION",
        "NO_ARITHMETIC_MAGNITUDE_IDENTITY",
        "NO_FLOAT_DECIMAL_EQUIVALENCE",
        "NO_OTHER_SOURCES",
        "NO_OTHER_VARIABLES",
        "NO_OTHER_NATIVE_CODES",
        "NO_DTA_APPLICABILITY",
        "NO_LABEL_OR_DISPLAY_SEMANTICS",
        "NO_MISSING_STATE_REINTERPRETATION",
        "NO_CROSS_WAVE_INHERITANCE",
        "NO_CANDIDATE_OUTPUT_PARENTAGE",
    ):
        assert limit in NEGATIVE_LIMITS
