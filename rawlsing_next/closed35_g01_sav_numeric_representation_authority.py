"""CLOSED35 G01 exact SAV native-int rule -> float64 physical representation authority.

This authority closes only the repeated physical-representation class measured by
CLOSED35 on nine governed surfaces across exact sources 02, 06 and 21.

It does NOT make Python int and float physically identical.  It authorizes an
explicit successor representation relation for an enumerated finite native-code
domain when all exact source, variable, storage, decoder and missing-state
applicability facts match the qualified CLOSED35 census evidence.
"""
from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key


CONTRACT = "PREMAIN_CLOSED35_G01_SAV_NUMERIC_REPRESENTATION_AUTHORITY@1.0.0"
AUTHORITY_KIND = "PHYSICAL_NATIVE_REPRESENTATION_BINDING"
OPERATION = "PREMAIN_CLOSED35_G01_SAV_NATIVE_INT_RULE_TO_FLOAT64_PHYSICAL_BINDING@1.0.0"
QUALIFIED_RUNTIME = MappingProxyType({
    "platform": "Darwin",
    "machine": "x86_64",
    "cpython": "3.11.3",
    "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1",
})
READER_CONFIG = MappingProxyType({
    "reader": "pyreadstat.read_sav",
    "format": "SAV",
    "encoding": None,
    "apply_value_formats": False,
    "user_missing": True,
})

# These are representation literals, not computed with float(native_code).
_AUTHORIZED_FLOATS = MappingProxyType({
    1: 1.0,
    2: 2.0,
    97: 97.0,
    98: 98.0,
    99: 99.0,
    997: 997.0,
})
AUTHORIZED_R5_TOKENS = MappingProxyType({
    1: {"t": "float64_finite", "bits": "3ff0000000000000"},
    2: {"t": "float64_finite", "bits": "4000000000000000"},
    97: {"t": "float64_finite", "bits": "4058400000000000"},
    98: {"t": "float64_finite", "bits": "4058800000000000"},
    99: {"t": "float64_finite", "bits": "4058c00000000000"},
    997: {"t": "float64_finite", "bits": "408f280000000000"},
})

CENSUS_RESULTS_HEAD = "b801c58c8e4d6d10e36e0a42ca62cf6908cbf25a"
CENSUS_RECEIPTS = MappingProxyType({
    "02": MappingProxyType({
        "blob": "0105df99d513859a2f40e2228d4d81c1655f905d",
        "source_sha256": "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
        "source_file": "Afro Barometer Round 5.sav",
    }),
    "06": MappingProxyType({
        "blob": "895c5a6c1fbcb9a931ba97d18a225a14243f4ccf",
        "source_sha256": "6a5cbad637ce1546833a1d4812ba6d1e8d75f85b5b199b0cf3ec5cf456068dbc",
        "source_file": "Arab Barometer Wave 5.sav",
    }),
    "21": MappingProxyType({
        "blob": "0d2c614e196d9ce279d6de5657176d2c2437f299",
        "source_sha256": "c229aff7430c12f246678f385e0776b089681ae9830bac88423e0964ac34ee05",
        "source_file": "GSS2010.sav",
    }),
})

# Exact source applicability.  Each entry is derived from the qualified census
# receipt; it is not a survey-semantic mapping.
_APPLICABILITY_ROWS = (
    {
        "surface_id": "S016",
        "source_id": "02",
        "source_sha256": CENSUS_RECEIPTS["02"]["source_sha256"],
        "variable_name": "Q10B",
        "ordinal": 58,
        "original_variable_type": "F3.0",
        "readstat_variable_type": "double",
        "storage_width": 8,
        "native_codes": (997,),
        "physical_state_by_code": {997: PhysicalMissingState.FORMAT_USER_MISSING_VALUE.value},
        "physical_declaration_by_code": {997: {"kind": "discrete", "value": 997.0}},
        "expected_binding_key_by_code": {
            997: "fa4b2337a92f76ad5a9af4a0efd5826ead2acc8888b11cbff292e31a25e4ac21",
        },
    },
    {
        "surface_id": "S037",
        "source_id": "06",
        "source_sha256": CENSUS_RECEIPTS["06"]["source_sha256"],
        "variable_name": "Q101",
        "ordinal": 20,
        "original_variable_type": "F8.2",
        "readstat_variable_type": "double",
        "storage_width": 8,
        "native_codes": (98, 99),
        "physical_state_by_code": {
            98: PhysicalMissingState.OBSERVED_STORAGE_VALUE.value,
            99: PhysicalMissingState.OBSERVED_STORAGE_VALUE.value,
        },
        "physical_declaration_by_code": {98: None, 99: None},
        "expected_binding_key_by_code": {
            98: "da7e0bd63766f92c885de245114037182c706727c17b6913db6b1e7323965541",
            99: "0a2cbc59f99c088a50a8f9342d0404a4e891a0e9ab914c0db2f4b06230ab2217",
        },
    },
    {
        "surface_id": "S038",
        "source_id": "06",
        "source_sha256": CENSUS_RECEIPTS["06"]["source_sha256"],
        "variable_name": "Q2061B",
        "ordinal": 19,
        "original_variable_type": "F8.2",
        "readstat_variable_type": "double",
        "storage_width": 8,
        "native_codes": (97,),
        "physical_state_by_code": {97: PhysicalMissingState.OBSERVED_STORAGE_VALUE.value},
        "physical_declaration_by_code": {97: None},
        "expected_binding_key_by_code": {
            97: "1e64987255e306600e37d73f6bcc6291710831523be8a22a2641d25f64b4247c",
        },
    },
    *tuple({
        "surface_id": surface_id,
        "source_id": "21",
        "source_sha256": CENSUS_RECEIPTS["21"]["source_sha256"],
        "variable_name": variable_name,
        "ordinal": ordinal,
        "original_variable_type": "F4.0",
        "readstat_variable_type": "double",
        "storage_width": 8,
        "native_codes": (1, 2),
        "physical_state_by_code": {
            1: PhysicalMissingState.OBSERVED_STORAGE_VALUE.value,
            2: PhysicalMissingState.OBSERVED_STORAGE_VALUE.value,
        },
        "physical_declaration_by_code": {1: None, 2: None},
        "expected_binding_key_by_code": {
            1: "47f141e43fb2a330ebd2286a0bb658eaa6320768d1bb75a0b969761731ace7bd",
            2: "4b48b50efb20c6194106eaad0cc975ecd5df143681a0ee990e6647b1164e313f",
        },
    } for surface_id, variable_name, ordinal in (
        ("S005", "abdefect", 5),
        ("S006", "abhlth", 6),
        ("S007", "abrape", 9),
        ("S008", "abany", 4),
        ("S009", "absingle", 10),
        ("S010", "abnomore", 7),
    )),
)
APPLICABILITY_ROWS = tuple(MappingProxyType(row) for row in _APPLICABILITY_ROWS)

UPSTREAM_SAV_DOUBLE_EVIDENCE = MappingProxyType({
    "pyreadstat_tag": "v1.3.6",
    "pyreadstat_commit": "ae4bfa5d84ed5da0a1b040be472703585bdfeefc",
    "bundled_readstat_revision": "634f40a80d27221848ba57e9fb633b41146bac36",
    "readstat_value_blob": "62aac39820184626df90451f0d999887d77ea884",
    "sav_core_blob": "62188bba9d26b73ff03ede34e50d936432f8bc82",
    "sav_read_blob": "5810f1ff8a92d010d8ad86d05ddd64aa227c0b92",
    "parser_blob": "bd43be1928139e343469cbad456f8773c41131bf",
    "holding": (
        "ReadStat SAV numeric double storage reaches pyreadstat through the "
        "READSTAT_TYPE_DOUBLE physical lane; CLOSED35 separately binds exact "
        "source/variable applicability and observed float64 R5 tokens."
    ),
})

NEGATIVE_LIMITS = (
    "NO_GLOBAL_INT_FLOAT_COERCION",
    "NO_ARITHMETIC_MAGNITUDE_IDENTITY",
    "NO_FLOAT_DECIMAL_EQUIVALENCE",
    "NO_DECIMAL_EXPONENT_NORMALIZATION",
    "NO_OTHER_SOURCES",
    "NO_OTHER_VARIABLES",
    "NO_OTHER_NATIVE_CODES",
    "NO_DTA_APPLICABILITY",
    "NO_LABEL_OR_DISPLAY_SEMANTICS",
    "NO_FREQUENCY_BASED_AUTHORITY",
    "NO_CANONICAL_QUESTION_MAPPING",
    "NO_MISSING_STATE_REINTERPRETATION",
    "NO_CROSS_WAVE_INHERITANCE",
    "NO_CANDIDATE_OUTPUT_PARENTAGE",
)


def _row_for(*, source_sha256: str, variable_name: str, ordinal: int) -> Mapping[str, Any]:
    matches = [
        row for row in APPLICABILITY_ROWS
        if row["source_sha256"] == source_sha256
        and row["variable_name"] == variable_name
        and row["ordinal"] == ordinal
    ]
    if len(matches) != 1:
        raise ValueError("G01 source/variable/ordinal outside exact applicability registry")
    return matches[0]


def authorized_sav_numeric_physical_material(
    *,
    source_sha256: str,
    variable_name: str,
    ordinal: int,
    native_code: Any,
) -> tuple[float, PhysicalMissingState, Mapping[str, Any] | None]:
    """Return exact authorized physical material for one enumerated G01 rule literal."""
    row = _row_for(
        source_sha256=source_sha256,
        variable_name=variable_name,
        ordinal=ordinal,
    )
    if type(native_code) is not int or native_code not in row["native_codes"]:
        raise ValueError("G01 native code/type outside exact applicability registry")
    value = _AUTHORIZED_FLOATS[native_code]
    token = R5TypedValueCodec().encode(value)
    if token != AUTHORIZED_R5_TOKENS[native_code]:
        raise RuntimeError("G01 authorized float literal/R5 token drift")
    state = PhysicalMissingState(row["physical_state_by_code"][native_code])
    declaration = row["physical_declaration_by_code"][native_code]
    key = physical_value_binding_key(value, state, declaration)
    if key != row["expected_binding_key_by_code"][native_code]:
        raise RuntimeError("G01 authorized physical binding key drift")
    return value, state, declaration


def authorized_sav_numeric_physical_binding_key(
    *,
    source_sha256: str,
    variable_name: str,
    ordinal: int,
    native_code: Any,
) -> str:
    value, state, declaration = authorized_sav_numeric_physical_material(
        source_sha256=source_sha256,
        variable_name=variable_name,
        ordinal=ordinal,
        native_code=native_code,
    )
    return physical_value_binding_key(value, state, declaration)


REPRESENTATION_AUTHORITY_MATERIAL = {
    "contract": CONTRACT,
    "authority_kind": AUTHORITY_KIND,
    "operation": OPERATION,
    "qualified_runtime": dict(QUALIFIED_RUNTIME),
    "reader_config": dict(READER_CONFIG),
    "census_results_head": CENSUS_RESULTS_HEAD,
    "census_receipts": {
        sid: dict(record) for sid, record in CENSUS_RECEIPTS.items()
    },
    "applicability": [
        {
            **{k: v for k, v in row.items() if k not in {
                "physical_state_by_code",
                "physical_declaration_by_code",
                "expected_binding_key_by_code",
            }},
            "code_bindings": [
                {
                    "native_code": code,
                    "physical_state": row["physical_state_by_code"][code],
                    "physical_declaration": row["physical_declaration_by_code"][code],
                    "expected_binding_key": row["expected_binding_key_by_code"][code],
                    "authorized_r5_token": dict(AUTHORIZED_R5_TOKENS[code]),
                }
                for code in row["native_codes"]
            ],
        }
        for row in APPLICABILITY_ROWS
    ],
    "upstream_sav_double_evidence": dict(UPSTREAM_SAV_DOUBLE_EVIDENCE),
    "negative_limits": list(NEGATIVE_LIMITS),
}
REPRESENTATION_AUTHORITY_HASH = semantic_hash(REPRESENTATION_AUTHORITY_MATERIAL)
REPRESENTATION_AUTHORITY_REF = AuthorityRef(
    "PREMAIN-CLOSED35-G01-SAV-NATIVE-INT-TO-FLOAT64-REPRESENTATION",
    "1.0.0",
    REPRESENTATION_AUTHORITY_HASH,
)
_REPLAY_HASH = semantic_hash({
    "authority_ref": REPRESENTATION_AUTHORITY_REF.as_dict(),
    "material_hash": REPRESENTATION_AUTHORITY_HASH,
    "law": "EXACT_G01_SOURCE_VARIABLE_CODE_SAV_DOUBLE_REPRESENTATION_ONLY",
})
REPLAY_ROOT = ExactRef(
    "PREMAIN_CLOSED35_G01_REPRESENTATION_REPLAY_ROOT@1.0.0",
    f"urn:rawlsing:pre553:closed35:g01:sha256:{_REPLAY_HASH}",
    _REPLAY_HASH,
)


def representation_authority_snapshot() -> AuthoritySnapshot:
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=REPLAY_ROOT,
        authority_id=REPRESENTATION_AUTHORITY_REF.authority_id,
        authority_version=REPRESENTATION_AUTHORITY_REF.authority_version,
        authority_content_hash=REPRESENTATION_AUTHORITY_REF.authority_content_hash,
        authority_kind=AUTHORITY_KIND,
        decision_state="ALLOW",
        governed_operations=(OPERATION,),
        governed_object_families=("PhysicalValueBinding@1.0.0",),
        scope_envelope={
            "census_results_head": CENSUS_RESULTS_HEAD,
            "source_sha256s": sorted({row["source_sha256"] for row in APPLICABILITY_ROWS}),
            "surfaces": [
                {
                    "surface_id": row["surface_id"],
                    "source_id": row["source_id"],
                    "source_sha256": row["source_sha256"],
                    "variable_name": row["variable_name"],
                    "ordinal": row["ordinal"],
                    "native_codes": list(row["native_codes"]),
                }
                for row in APPLICABILITY_ROWS
            ],
            "reader_config": dict(READER_CONFIG),
            "representation_ceiling": "PHYSICAL_DECODER_REPRESENTATION_ONLY",
        },
        effective_time_or_interval={
            "qualified_runtime": dict(QUALIFIED_RUNTIME),
        },
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({
            "authority_ref": REPRESENTATION_AUTHORITY_REF.as_dict(),
            "ceiling": "REPRESENTATION_ONLY__NO_SEMANTIC_INFERENCE",
            "negative_limits": list(NEGATIVE_LIMITS),
        }),
        replay_protocol_ref=REPLAY_ROOT,
    )


__all__ = [
    "CONTRACT",
    "AUTHORITY_KIND",
    "OPERATION",
    "QUALIFIED_RUNTIME",
    "READER_CONFIG",
    "AUTHORIZED_R5_TOKENS",
    "CENSUS_RESULTS_HEAD",
    "CENSUS_RECEIPTS",
    "APPLICABILITY_ROWS",
    "UPSTREAM_SAV_DOUBLE_EVIDENCE",
    "NEGATIVE_LIMITS",
    "REPRESENTATION_AUTHORITY_MATERIAL",
    "REPRESENTATION_AUTHORITY_REF",
    "authorized_sav_numeric_physical_material",
    "authorized_sav_numeric_physical_binding_key",
    "representation_authority_snapshot",
]
