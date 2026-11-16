"""Exact LiTS-I D03 R2/R7/R27 risk-set successor authority.

This module republishes the lossless compact extension frozen at accepted
commit ``1dc316b4a388949c1736aa65a20c8d43cfb2c8ba``.  It does not derive
membership from current values, labels, frequencies, or missingness.  The
payload is verified by its accepted compressed/raw hashes before use.
"""
from __future__ import annotations

import base64
import hashlib
import zlib

from rawlsing_next.fiabc_lits_i_i03_operation_authority import QUERY_REFS
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash


SCHEMA = "FIABC_LITS_I_D03_RISK_SET_SUCCESSOR_AUTHORITY@1.0.0"
SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
ROW_COUNT = 29_002
D03_COMMIT = "1dc316b4a388949c1736aa65a20c8d43cfb2c8ba"
D03_MANIFEST_PATH = "WORKER_RETURNS/EE-R3B/01_EXTENTIONAL_ROOTS_AND_TYPED_ACCOUNTING.json"
D03_MANIFEST_BLOB = "8ad99f6221ac5dc087063753be437bde2dd4e1b1"
COMPRESSED_SHA256 = "989e67a736663831a5595dfb3dbe1b1073a69e9f29a3ea16e1e69169d81727af"
RAW_PAYLOAD_SHA256 = "357aa62675c880b335d20e6c43fe18ce7c76c4890743f4a4ce3f84eb7480116b"
RAW_PAYLOAD_LENGTH = 18_128

BASE_RELEASE_REF = ExactRef(
    "C11LogicalRelease",
    "LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79",
    "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26",
)
SUCCESSOR_RELEASE_REF = ExactRef(
    "C11LogicalRelease",
    "LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669",
    "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
)
RELEASE_REFS = (BASE_RELEASE_REF, SUCCESSOR_RELEASE_REF)
# Backward-compatible name for callers that explicitly test the historical base.
RELEASE_REF = BASE_RELEASE_REF
UNIVERSE_REF = ExactRef(
    "EmpiricalUniverse@1.0.0",
    "urn:rawlsing:pre553:EmpiricalUniverse:sha256:83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080",
    "83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080",
)
RISK_SET_REF = ExactRef(
    "RISK_SET",
    "urn:rawlsing:pre553:as2b:lits1-q301-bounded:sha256:31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45",
    "31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45",
)
Q301_2_REF = ExactRef(
    "QUESTION_NATIVE",
    "urn:rawlsing:pre553:as2b:lits1-q301_2:sha256:d827e1c0a4363a7f45430a717bb5fd809f85be5d72e0ef9b339942f0418a7f83",
    "d827e1c0a4363a7f45430a717bb5fd809f85be5d72e0ef9b339942f0418a7f83",
)
Q301_7_REF = ExactRef(
    "QUESTION_NATIVE",
    "urn:rawlsing:pre553:as2b:lits1-q301_7:sha256:c2d934d3687e1200ab524a51d8f51b3d920c548754b4aefbefe506b01986806f",
    "c2d934d3687e1200ab524a51d8f51b3d920c548754b4aefbefe506b01986806f",
)

ROOTS = {
    "R2": {
        "member_count": 24_897,
        "canonical_full_tsv_sha256": "f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3",
    },
    "R7": {
        "member_count": 28_325,
        "canonical_full_tsv_sha256": "0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844",
    },
    "R27": {
        "member_count": 24_630,
        "canonical_full_tsv_sha256": "f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29",
    },
}

RESPONDENT_KEY_PREFIX = f"LITS1_SELECTED_RESPONDENT__{SOURCE_SHA256}__ROW_"

# Concatenation of accepted 04_EXTENSION_PAYLOAD_B64_PART_01..03.  The bytes
# are authority material only after all accepted hashes below validate.
PAYLOAD_B64 = """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"""

IDENTITY_MATERIAL = canonicalize({
    "authority_id": "urn:rawlsing:fiabc:lits-i:d03-risk-set-successor",
    "authority_version": "1.0.0",
    "source_sha256": SOURCE_SHA256,
    "row_count": ROW_COUNT,
    "release_refs": [ref.as_dict() for ref in RELEASE_REFS],
    "source_universe_ref": UNIVERSE_REF.as_dict(),
    "risk_set_ref": RISK_SET_REF.as_dict(),
    "target_role_map": [
        {"target_refs": [Q301_2_REF.as_dict()], "root_id": "R2"},
        {"target_refs": [Q301_7_REF.as_dict()], "root_id": "R7"},
        {"target_refs": [Q301_2_REF.as_dict(), Q301_7_REF.as_dict()], "root_id": "R27"},
    ],
    "query_refs": [ref.as_dict() for ref in QUERY_REFS],
    "respondent_key_prefix": RESPONDENT_KEY_PREFIX,
    "accepted_d03": {
        "commit": D03_COMMIT,
        "manifest_path": D03_MANIFEST_PATH,
        "manifest_blob": D03_MANIFEST_BLOB,
        "compressed_sha256": COMPRESSED_SHA256,
        "raw_payload_sha256": RAW_PAYLOAD_SHA256,
        "raw_payload_length": RAW_PAYLOAD_LENGTH,
        "payload_layout": {
            "encoding": "ZLIB9_BASE64",
            "row_count": ROW_COUNT,
            "r2_offset": 0,
            "r2_length": 7_251,
            "r7_offset": 7_251,
            "r7_length": 7_251,
            "r27_offset": 14_502,
            "r27_length": 3_626,
            "two_bit_member_code": 0,
            "bit_member_code": 1,
        },
        "roots": ROOTS,
    },
    "accepted_successor_preservation": {
        "r5b_commit": "648a39ad5bed42f66e066410af5869604d29c12d",
        "base_release_ref": BASE_RELEASE_REF.as_dict(),
        "successor_release_ref": SUCCESSOR_RELEASE_REF.as_dict(),
        "successor_replay_hash": "30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08",
        "successor_candidate_projection_hash": "23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb",
        "preservation_law": (
            "BASE_Q301_QUESTION_BINDINGS_EVENTS_ROUTING_AND_RESPONDENTS_RETAINED_EXACT__"
            "SUCCESSOR_ADDS_ONLY_F02_Q310_Q311"
        ),
    },
    "negative_limits": [
        "NO_VALUE_LABEL_OR_FREQUENCY_INFERENCE",
        "NO_CURRENT_SOURCE_VALUE_DERIVATION",
        "NO_OTHER_SOURCE_RELEASE_UNIVERSE_RISK_SET_TARGET_OR_QUERY",
        "NO_RISK_SET_EXTENSION_TO_Q310_Q311_OR_OTHER_TARGETS",
        "NO_GENERIC_MISSINGNESS_OR_DENOMINATOR_RULE",
        "NO_CANDIDATE_OUTPUT_PARENTAGE",
        "NO_C11_RELEASE_MUTATION",
    ],
})
AUTHORITY_CONTENT_HASH = semantic_hash(IDENTITY_MATERIAL)


def risk_set_successor_authority_record():
    return {
        "schema": SCHEMA,
        "authority_content_hash": AUTHORITY_CONTENT_HASH,
        "identity_material": IDENTITY_MATERIAL,
        "payload_base64": PAYLOAD_B64,
    }


def decode_membership_payload() -> dict[str, frozenset[int]]:
    if len(PAYLOAD_B64) != 8_944:
        raise ValueError("LiTS D03 payload base64 length drift")
    compressed = base64.b64decode(PAYLOAD_B64, validate=True)
    if len(compressed) != 6_707 or hashlib.sha256(compressed).hexdigest() != COMPRESSED_SHA256:
        raise ValueError("LiTS D03 compressed payload identity drift")
    raw = zlib.decompress(compressed)
    if len(raw) != RAW_PAYLOAD_LENGTH or hashlib.sha256(raw).hexdigest() != RAW_PAYLOAD_SHA256:
        raise ValueError("LiTS D03 raw payload identity drift")
    r2_raw, r7_raw, r27_raw = raw[:7_251], raw[7_251:14_502], raw[14_502:]

    def two_bit_members(data: bytes) -> frozenset[int]:
        return frozenset(
            row for row in range(1, ROW_COUNT + 1)
            if ((data[(row - 1) // 4] >> (6 - 2 * ((row - 1) % 4))) & 0b11) == 0
        )

    def bit_members(data: bytes) -> frozenset[int]:
        return frozenset(
            row for row in range(1, ROW_COUNT + 1)
            if ((data[(row - 1) // 8] >> (7 - ((row - 1) % 8))) & 0b1) == 1
        )

    decoded = {
        "R2": two_bit_members(r2_raw),
        "R7": two_bit_members(r7_raw),
        "R27": bit_members(r27_raw),
    }
    for root_id, members in decoded.items():
        if len(members) != ROOTS[root_id]["member_count"]:
            raise ValueError(f"LiTS D03 {root_id} member count drift")
    if decoded["R27"] != decoded["R2"] & decoded["R7"]:
        raise ValueError("LiTS D03 R27 intersection drift")
    return decoded


__all__ = [
    "SCHEMA", "SOURCE_SHA256", "ROW_COUNT", "D03_COMMIT", "D03_MANIFEST_BLOB",
    "BASE_RELEASE_REF", "SUCCESSOR_RELEASE_REF", "RELEASE_REFS", "RELEASE_REF",
    "UNIVERSE_REF", "RISK_SET_REF", "Q301_2_REF", "Q301_7_REF",
    "ROOTS", "RESPONDENT_KEY_PREFIX", "PAYLOAD_B64", "IDENTITY_MATERIAL",
    "AUTHORITY_CONTENT_HASH", "risk_set_successor_authority_record",
    "decode_membership_payload",
]
