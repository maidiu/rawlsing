"""Exact LiTS-I DTA decoder representation authority for q301_2/q301_7.

This authority binds only the exact float64 physical tokens observed by the
qualified decoder to the exact Decimal tokens used by the accepted banked
LiTS replay.  The replay remains under the historical physical-key owner; no
generic numeric coercion or new response semantics are authorized here.
"""
from __future__ import annotations

from decimal import Decimal
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_bytes


CONTRACT = "FIABC_LITS_I_DTA_DECODER_REPRESENTATION_REPLAY_BINDING@1.0.0"
AUTHORITY_KIND = "PHYSICAL_NATIVE_REPRESENTATION_BINDING"
OPERATION = "FIABC_LITS_I_Q301_DTA_FLOAT64_TO_ACCEPTED_BANKED_REPLAY@1.0.0"
SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
PROJECTION_IDENTITY = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
ACCEPTED_C11_RELEASE_IDENTITY = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
ACCEPTED_C11_REPLAY_IDENTITY = "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"
DIAGNOSTIC_RECEIPT_SHA256 = "74fc2c53610ad2af5867e4c36728604a812cf9ad3d7b0e4bceebda68fe4ac74b"
DIAGNOSTIC_SCHEMA = "FIABC_LITS_I_DECODER_REPRESENTATION_DIAGNOSTIC@1.0.0"
LEGACY_FACADE_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
LEGACY_FACADE_BLOB = "7c509c2098d0030f253344eb3f682471378812a8"
LEGACY_FACADE_PATH = "rawlsing_next/pre553_source_backed_c11_facade.py"
CURRENT_TYPED_FACADE_BLOB = "8a761119e4a8d68eb291fc4edfadb52e027f8284"
BANKED_PROJECTION_BUILDER_BLOB = "c51b56779ab9d79126619b7733d41f5253c8150f"
TARGET_VARIABLES = MappingProxyType({"q301_2": 194, "q301_7": 199})
NATIVE_CODES = (1, 2, 3, 4, 5, 6, 7)
READER_CONFIG = MappingProxyType({
    "reader": "pyreadstat",
    "reader_version": "1.3.6",
    "format": "DTA",
    "encoding": "latin1",
    "apply_value_formats": False,
    "user_missing": True,
    "python": "3.11.3",
})

AUTHORIZED_DECODER_R5_TOKENS = MappingProxyType({
    1: {"t": "float64_finite", "bits": "3ff0000000000000"},
    2: {"t": "float64_finite", "bits": "4000000000000000"},
    3: {"t": "float64_finite", "bits": "4008000000000000"},
    4: {"t": "float64_finite", "bits": "4010000000000000"},
    5: {"t": "float64_finite", "bits": "4014000000000000"},
    6: {"t": "float64_finite", "bits": "4018000000000000"},
    7: {"t": "float64_finite", "bits": "401c000000000000"},
})
AUTHORIZED_BANKED_R5_TOKENS = MappingProxyType({
    code: {
        "t": "decimal",
        "v": {"sign": 0, "digits": [code, 0], "exponent": -1},
    }
    for code in NATIVE_CODES
})
GOVERNED_RULE_R5_TOKENS = MappingProxyType({
    code: {
        "t": "decimal",
        "v": {"sign": 0, "digits": [code], "exponent": 0},
    }
    for code in NATIVE_CODES
})
_AUTHORIZED_BANKED_VALUES = MappingProxyType({
    1: Decimal("1.0"),
    2: Decimal("2.0"),
    3: Decimal("3.0"),
    4: Decimal("4.0"),
    5: Decimal("5.0"),
    6: Decimal("6.0"),
    7: Decimal("7.0"),
})
_CODEC = R5TypedValueCodec()
_DECODER_TOKEN_TO_CODE = MappingProxyType({
    canonical_bytes(token): code for code, token in AUTHORIZED_DECODER_R5_TOKENS.items()
})

NEGATIVE_LIMITS = (
    "NO_GLOBAL_INT_FLOAT_DECIMAL_COERCION",
    "NO_OTHER_VARIABLES",
    "NO_OTHER_LITS_WAVES",
    "NO_OTHER_SOURCES",
    "NO_CURRENT_TYPED_KEY_EQUIVALENCE",
    "NO_LABEL_OR_FREQUENCY_AUTHORITY",
    "NO_MISSINGNESS_INFERENCE",
    "NO_RESPONSE_SEMANTIC_REMAP",
    "NO_CANONICAL_QUESTION_MAPPING",
    "NO_CANDIDATE_OUTPUT_PARENTAGE",
    "NO_SYSTEM_MISSING_REINTERPRETATION",
)

REPRESENTATION_AUTHORITY_MATERIAL = {
    "contract": CONTRACT,
    "authority_kind": AUTHORITY_KIND,
    "operation": OPERATION,
    "source_sha256": SOURCE_SHA256,
    "source_family": "LiTS",
    "wave": "I",
    "variables": [
        {"name": name, "ordinal": ordinal} for name, ordinal in TARGET_VARIABLES.items()
    ],
    "reader_config": dict(READER_CONFIG),
    "diagnostic": {
        "schema": DIAGNOSTIC_SCHEMA,
        "receipt_sha256": DIAGNOSTIC_RECEIPT_SHA256,
        "response_cells": 58004,
        "observed_cells": 57989,
        "system_missing_cells": 15,
        "unique_representation_classes": 16,
    },
    "authorized_representations": [
        {
            "native_code": code,
            "decoder_r5_token": dict(AUTHORIZED_DECODER_R5_TOKENS[code]),
            "accepted_banked_r5_token": dict(AUTHORIZED_BANKED_R5_TOKENS[code]),
            "governed_rule_r5_token": dict(GOVERNED_RULE_R5_TOKENS[code]),
        }
        for code in NATIVE_CODES
    ],
    "historical_replay": {
        "legacy_facade_commit": LEGACY_FACADE_COMMIT,
        "legacy_facade_blob": LEGACY_FACADE_BLOB,
        "legacy_physical_key_law": "semantic_hash(canonicalize(raw,state,declaration))",
        "banked_projection_builder_blob": BANKED_PROJECTION_BUILDER_BLOB,
        "projection_identity": PROJECTION_IDENTITY,
        "accepted_c11_release_identity": ACCEPTED_C11_RELEASE_IDENTITY,
        "accepted_c11_replay_identity": ACCEPTED_C11_REPLAY_IDENTITY,
    },
    "current_typed_contract_separation": {
        "current_facade_blob": CURRENT_TYPED_FACADE_BLOB,
        "law": "PRE553_PHYSICAL_VALUE_BINDING@2.0.0_REMAINS_UNCHANGED",
        "scope": "EXACT_LITS_ACCEPTED_REPLAY_ROUTE_ONLY",
    },
    "negative_limits": list(NEGATIVE_LIMITS),
}
REPRESENTATION_AUTHORITY_HASH = semantic_hash(REPRESENTATION_AUTHORITY_MATERIAL)
REPRESENTATION_AUTHORITY_REF = AuthorityRef(
    "FIABC-LITS-I-Q301-DTA-DECODER-REPRESENTATION-REPLAY",
    "1.0.0",
    REPRESENTATION_AUTHORITY_HASH,
)
_REPLAY_HASH = semantic_hash({
    "authority_ref": REPRESENTATION_AUTHORITY_REF.as_dict(),
    "legacy_facade_blob": LEGACY_FACADE_BLOB,
    "banked_projection_builder_blob": BANKED_PROJECTION_BUILDER_BLOB,
    "diagnostic_receipt_sha256": DIAGNOSTIC_RECEIPT_SHA256,
})
REPLAY_ROOT = ExactRef(
    "FIABC_LITS_I_REPRESENTATION_REPLAY_ROOT@1.0.0",
    f"urn:rawlsing:pre553:fiabc-lits-i:representation:sha256:{_REPLAY_HASH}",
    _REPLAY_HASH,
)


def _require_variable(variable_name: str, ordinal: int) -> None:
    if TARGET_VARIABLES.get(variable_name) != ordinal:
        raise ValueError("LiTS representation authority variable identity/ordinal mismatch")


def authorized_banked_raw_value(
    *,
    source_sha256: str,
    variable_name: str,
    ordinal: int,
    raw_value: Any,
    missing_state: PhysicalMissingState,
    source_missing_declaration: Mapping[str, Any] | None,
) -> Any:
    """Return only the exact banked value permitted by this bounded authority."""
    if source_sha256 != SOURCE_SHA256:
        raise ValueError("LiTS representation authority source SHA mismatch")
    _require_variable(variable_name, ordinal)
    if missing_state is PhysicalMissingState.SYSTEM_MISSING:
        if raw_value is not None or source_missing_declaration is not None:
            raise ValueError("LiTS system-missing representation drift")
        return None
    if missing_state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE:
        raise ValueError("LiTS representation state outside exact authority")
    if source_missing_declaration is not None:
        raise ValueError("LiTS observed representation has unexpected missing declaration")
    if type(raw_value) is not float:
        raise ValueError("LiTS decoder representation type outside exact authority")
    code = _DECODER_TOKEN_TO_CODE.get(canonical_bytes(_CODEC.encode(raw_value)))
    if code is None:
        raise ValueError("LiTS decoder float token outside exact authority")
    value = _AUTHORIZED_BANKED_VALUES[code]
    if _CODEC.encode(value) != AUTHORIZED_BANKED_R5_TOKENS[code]:
        raise RuntimeError("LiTS authorized banked Decimal/R5 token drift")
    return value


def authorized_replay_cell(*, source_sha256: str, cell: PhysicalCell) -> PhysicalCell:
    """Apply the authority only to the two governed response slots."""
    if TARGET_VARIABLES.get(cell.variable_name) != cell.variable_ordinal:
        return cell
    value = authorized_banked_raw_value(
        source_sha256=source_sha256,
        variable_name=cell.variable_name,
        ordinal=cell.variable_ordinal,
        raw_value=cell.raw_value,
        missing_state=cell.missing_state,
        source_missing_declaration=cell.source_missing_declaration,
    )
    return PhysicalCell(
        row_ordinal=cell.row_ordinal,
        variable_ordinal=cell.variable_ordinal,
        variable_name=cell.variable_name,
        raw_value=value,
        missing_state=cell.missing_state,
        source_missing_declaration=cell.source_missing_declaration,
        raw_value_label=cell.raw_value_label,
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
        governed_object_families=("RespondentEvent@1.0.0",),
        scope_envelope={
            "source_sha256": SOURCE_SHA256,
            "source_family": "LiTS",
            "wave": "I",
            "variables": [
                {"name": name, "ordinal": ordinal}
                for name, ordinal in TARGET_VARIABLES.items()
            ],
            "native_codes": list(NATIVE_CODES),
            "reader_config": dict(READER_CONFIG),
            "legacy_facade_blob": LEGACY_FACADE_BLOB,
            "representation_ceiling": "EXACT_ACCEPTED_REPLAY_REPRESENTATION_ONLY",
        },
        effective_time_or_interval={
            "qualified_runtime": "CPython 3.11.3 / pyreadstat 1.3.6",
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
    "SOURCE_SHA256",
    "PROJECTION_IDENTITY",
    "ACCEPTED_C11_RELEASE_IDENTITY",
    "ACCEPTED_C11_REPLAY_IDENTITY",
    "DIAGNOSTIC_RECEIPT_SHA256",
    "LEGACY_FACADE_COMMIT",
    "LEGACY_FACADE_BLOB",
    "LEGACY_FACADE_PATH",
    "CURRENT_TYPED_FACADE_BLOB",
    "BANKED_PROJECTION_BUILDER_BLOB",
    "TARGET_VARIABLES",
    "NATIVE_CODES",
    "AUTHORIZED_DECODER_R5_TOKENS",
    "AUTHORIZED_BANKED_R5_TOKENS",
    "GOVERNED_RULE_R5_TOKENS",
    "NEGATIVE_LIMITS",
    "REPRESENTATION_AUTHORITY_MATERIAL",
    "REPRESENTATION_AUTHORITY_REF",
    "authorized_banked_raw_value",
    "authorized_replay_cell",
    "representation_authority_snapshot",
]
