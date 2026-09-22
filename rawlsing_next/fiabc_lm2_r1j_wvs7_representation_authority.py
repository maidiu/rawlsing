"""FIABC-LM2-R1J exact WVS7 Q291 SAV decoder representation authority.

This module authorizes one representation relation only:
source-native SPSS numeric codes/states for the exact WVS7 Q291G5/Q291P5
variables -> the exact Python float64 material emitted by the accepted
pyreadstat/ReadStat SAV numeric-double lane.

It does not authorize semantics, question mapping, generic int/float coercion,
cross-source equivalence, system-missing reinterpretation, or candidate output.
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
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec

CONTRACT = "FIABC_LM2_R1J_WVS7_SAV_DECODER_REPRESENTATION_BINDING@1.0.0"
AUTHORITY_KIND = "PHYSICAL_NATIVE_REPRESENTATION_BINDING"
OPERATION = "FIABC_LM2_R1J_WVS7_Q291_SAV_NUMERIC_REPRESENTATION_BINDING@1.0.0"
SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
PHYSICAL_METADATA_DIGEST = "ac24f5a7a624587c0072b9af937cd3d10abc7fdcd3537e7a2d2b98480d187110"
PHYSICAL_METADATA_RECEIPT_IDENTITY = "97ced560ffb07620809dbeeeb6d01823782227c9bdf4764bb9dae29b134121c7"
Q291_VARIABLES = MappingProxyType({
    "Q291G5": 388,
    "Q291P5": 394,
})
NATIVE_CODES = (1, 2, 3, 4, 5, -1, -2, -4, -5)

# Deliberately literal, not computed by float(native_code): this table is the
# bounded authority surface. Nearby numeric values and other Python types have
# no representation permission.
_AUTHORIZED_FLOATS = MappingProxyType({
    1: 1.0,
    2: 2.0,
    3: 3.0,
    4: 4.0,
    5: 5.0,
    -1: -1.0,
    -2: -2.0,
    -4: -4.0,
    -5: -5.0,
})
AUTHORIZED_R5_TOKENS = MappingProxyType({
    1: {"t": "float64_finite", "bits": "3ff0000000000000"},
    2: {"t": "float64_finite", "bits": "4000000000000000"},
    3: {"t": "float64_finite", "bits": "4008000000000000"},
    4: {"t": "float64_finite", "bits": "4010000000000000"},
    5: {"t": "float64_finite", "bits": "4014000000000000"},
    -1: {"t": "float64_finite", "bits": "bff0000000000000"},
    -2: {"t": "float64_finite", "bits": "c000000000000000"},
    -4: {"t": "float64_finite", "bits": "c010000000000000"},
    -5: {"t": "float64_finite", "bits": "c014000000000000"},
})
READER_CONFIG = MappingProxyType({
    "reader": "pyreadstat",
    "accepted_runtime_version": "1.3.6",
    "persisted_carrier_version": "1.3.2",
    "format": "SAV",
    "encoding": None,
    "apply_value_formats": False,
    "user_missing": True,
    "q291_display_format": "F3.0",
})
UPSTREAM_VERSION_EVIDENCE = MappingProxyType({
    "pyreadstat_1_3_2": {
        "tag": "v1.3.2",
        "commit": "97a124bfebcdf225ffbec7430e81f2868238a115",
        "bundled_readstat_revision": "b2d5407d62caf3c33caadc0495c9f7684b6a0df7",
        "readstat_value_blob": "62aac39820184626df90451f0d999887d77ea884",
        "sav_core_blob": "62188bba9d26b73ff03ede34e50d936432f8bc82",
        "sav_read_blob": "731d8addb14379cc7a9700f17cf217cd0c927e01",
        "parser_blob": "b9733bcf4112fed59271007533e7f5398d0ba5e6",
    },
    "pyreadstat_1_3_6": {
        "tag": "v1.3.6",
        "commit": "ae4bfa5d84ed5da0a1b040be472703585bdfeefc",
        "bundled_readstat_revision": "634f40a80d27221848ba57e9fb633b41146bac36",
        "readstat_value_blob": "62aac39820184626df90451f0d999887d77ea884",
        "sav_core_blob": "62188bba9d26b73ff03ede34e50d936432f8bc82",
        "sav_read_blob": "5810f1ff8a92d010d8ad86d05ddd64aa227c0b92",
        "parser_blob": "bd43be1928139e343469cbad456f8773c41131bf",
    },
    "version_delta_holding": (
        "readstat_value.c and readstat_sav.c are blob-identical; "
        "readstat_sav_read.c differs only in multiple-response-set parser context; "
        "the SAV numeric-double cell lane and Python READSTAT_TYPE_DOUBLE->np.float64 lane are unchanged"
    ),
})
NEGATIVE_LIMITS = (
    "NO_GLOBAL_INT_FLOAT_COERCION",
    "NO_OTHER_VARIABLES",
    "NO_OTHER_WVS_WAVES",
    "NO_OTHER_SOURCES",
    "NO_CANONICAL_QUESTION_MAPPING",
    "NO_NATIVE_TO_CANONICAL_MAPPING_BEYOND_R1E",
    "NO_CROSS_SOURCE_EQUIVALENCE",
    "NO_LABEL_OR_FREQUENCY_AUTHORITY",
    "NO_CANDIDATE_OUTPUT_PARENTAGE",
    "NO_SYSTEM_MISSING_REINTERPRETATION",
)

REPRESENTATION_AUTHORITY_MATERIAL = {
    "contract": CONTRACT,
    "authority_kind": AUTHORITY_KIND,
    "operation": OPERATION,
    "source_sha256": SOURCE_SHA256,
    "source_family": "WVS",
    "wave": "W7",
    "variables": [
        {
            "name": name,
            "ordinal": ordinal,
            "accepted_readstat_storage_type": "double",
            "storage_width": 8,
            "display_format": "F3.0",
        }
        for name, ordinal in Q291_VARIABLES.items()
    ],
    "reader_config": dict(READER_CONFIG),
    "authorized_native_to_physical_r5": [
        {"native_code": code, "physical_r5_token": dict(AUTHORIZED_R5_TOKENS[code])}
        for code in NATIVE_CODES
    ],
    "accepted_physical_metadata": {
        "digest": PHYSICAL_METADATA_DIGEST,
        "receipt_identity": PHYSICAL_METADATA_RECEIPT_IDENTITY,
        "evidence_path": "WORKER_RETURNS/FIABC-LM2/wvs7_physical_evidence_material.json",
    },
    "upstream_version_evidence": {
        key: dict(value) if isinstance(value, Mapping) else value
        for key, value in UPSTREAM_VERSION_EVIDENCE.items()
    },
    "semantic_layer_separation": {
        "decoder_law_role": "REPRESENTATION_ONLY",
        "source_semantics_role": "EE_R6A_P2F2_UNCHANGED",
        "native_to_program_token_role": "FIABC_LM2_R1E_UNCHANGED",
    },
    "negative_limits": list(NEGATIVE_LIMITS),
}
REPRESENTATION_AUTHORITY_HASH = semantic_hash(REPRESENTATION_AUTHORITY_MATERIAL)
REPRESENTATION_AUTHORITY_REF = AuthorityRef(
    "FIABC-LM2-R1J-WVS7-Q291-SAV-DECODER-REPRESENTATION",
    "1.0.0",
    REPRESENTATION_AUTHORITY_HASH,
)
_REPLAY_HASH = semantic_hash({
    "authority_ref": REPRESENTATION_AUTHORITY_REF.as_dict(),
    "material_hash": REPRESENTATION_AUTHORITY_HASH,
    "law": "EXACT_SOURCE_Q291_SAV_DOUBLE_REPRESENTATION_ONLY",
})
REPLAY_ROOT = ExactRef(
    "FIABC_LM2_R1J_REPRESENTATION_REPLAY_ROOT@1.0.0",
    f"urn:rawlsing:pre553:fiabc-lm2-r1j:representation:sha256:{_REPLAY_HASH}",
    _REPLAY_HASH,
)


def authorized_decoder_physical_value(
    *,
    source_sha256: str,
    variable_name: str,
    ordinal: int,
    native_code: Any,
) -> float:
    """Return only the exact decoder material explicitly authorized by R1J."""
    if source_sha256 != SOURCE_SHA256:
        raise ValueError("representation authority source SHA mismatch")
    if Q291_VARIABLES.get(variable_name) != ordinal:
        raise ValueError("representation authority variable identity/ordinal mismatch")
    if type(native_code) is not int or native_code not in _AUTHORIZED_FLOATS:
        raise ValueError("native code/type outside exact representation authority")
    value = _AUTHORIZED_FLOATS[native_code]
    if R5TypedValueCodec().encode(value) != AUTHORIZED_R5_TOKENS[native_code]:
        raise RuntimeError("authorized float literal/R5 token drift")
    return value


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
            "source_family": "WVS",
            "wave": "W7",
            "variables": [
                {"name": name, "ordinal": ordinal}
                for name, ordinal in Q291_VARIABLES.items()
            ],
            "native_codes": list(NATIVE_CODES),
            "reader_config": dict(READER_CONFIG),
            "representation_ceiling": "PHYSICAL_DECODER_REPRESENTATION_ONLY",
        },
        effective_time_or_interval={
            "pyreadstat_versions_proved_equivalent_for_this_lane": ["1.3.2", "1.3.6"],
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
    "Q291_VARIABLES",
    "NATIVE_CODES",
    "AUTHORIZED_R5_TOKENS",
    "READER_CONFIG",
    "UPSTREAM_VERSION_EVIDENCE",
    "NEGATIVE_LIMITS",
    "REPRESENTATION_AUTHORITY_MATERIAL",
    "REPRESENTATION_AUTHORITY_REF",
    "authorized_decoder_physical_value",
    "representation_authority_snapshot",
]
