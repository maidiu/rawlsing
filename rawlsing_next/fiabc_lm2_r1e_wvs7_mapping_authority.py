"""Exact bounded WVS7/P2 native-response -> program-token mapping authority.

This is a separate immutable authority object.  It does not relabel source
semantics, authorize canonical question mapping, map source-special states, or
grant any cross-source relation.  Its semantic material is mechanically
parented by the exact accepted R1D/P2F2 provenance graph.
"""
from __future__ import annotations

from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    canonicalize,
    semantic_hash,
)

CONTRACT = "FIABC_LM2_R1E_WVS7_P2_RESPONSE_MAPPING_AUTHORITY@1.0.0"
GOVERNING_HQ_SEAL = "04b43460c4ed13e610f493188fccfa265a02a91f"
COMMISSION_COMMIT = "da233da3176db69607a0d7cf5db0413e8551e5f4"
SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
TARGET_USE = "EXACT_FROZEN_WVS7_P2_PROGRAM_ONLY"
AUTHORITY_ID = "FIABC-LM2-R1E-WVS7-P2-RESPONSE-MAPPING"
AUTHORITY_VERSION = "1.0.0"
AUTHORITY_KIND = "NATIVE_CANONICAL_MAPPING_HARMONIZATION"
GOVERNED_OPERATION = "MAP_NATIVE_CANONICAL_VALUE"

SOURCE_AUTH_REF = AuthorityRef(
    "EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY",
    "1.0.0",
    "c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f",
)
PREDICATE_GRAMMAR_AUTH_REF = AuthorityRef(
    "EE-P2F2-WVS7-PRE553-I03-PREDICATE-GRAMMAR",
    "1.0.0",
    "92fc0bf93937b8e38cd181df7915c8786abdc16465833d731daa90ca1218dec5",
)

RESPONSE_SEMANTICS_REF = ExactRef(
    "WVS7ResponseStateSemantics@1.0.0",
    "urn:rawlsing:pre553:ee-p2f2:response-semantics:sha256:8aaa37c601f0dac74870c585567403520ce77287feae525832c59841dac1b710",
    "8aaa37c601f0dac74870c585567403520ce77287feae525832c59841dac1b710",
)
TARGET_DOMAIN_REPLAY_REF = ExactRef(
    "WVS7TargetDomainReplay@1.0.0",
    "urn:rawlsing:pre553:ee-p2f2:q291-domain:sha256:5d0a1ca4cc23c198a6afd4b935d425d51c7dd5cd143d056b351740c059608ef4",
    "5d0a1ca4cc23c198a6afd4b935d425d51c7dd5cd143d056b351740c059608ef4",
)
PROGRAM_SCOPE_REF = ExactRef(
    "WVS7ExactProgramScope@1.0.0",
    "urn:rawlsing:pre553:ee-p2f2:program-scope:sha256:ed669953b33512f0032abc40973f85be1bede1993f6d520f901c11bcd7e8666e",
    "ed669953b33512f0032abc40973f85be1bede1993f6d520f901c11bcd7e8666e",
)
UNIVERSE_REF = ExactRef(
    "EmpiricalUniverse@1.0.0",
    "urn:rawlsing:pre553:EmpiricalUniverse:sha256:f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e",
    "f9b1cdffc5783ace87d258ebe2ae1c75040ce786c373e255f53da4be4259d95e",
)
RISK_SET_REF = ExactRef(
    "WVS7RiskSetBinding@1.0.0",
    "urn:rawlsing:pre553:ee-p2f2:risk-set:sha256:0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7",
    "0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7",
)

Q0_REF = ExactRef(
    "WVS7QuestionBinding@1.0.0",
    "question_impl.phase0.03ea3430fb4f08a1f0da",
    "4574aecc9db3ec15ba255a5e6f6ce17304ccb610c7d7d9f4b7baddc6d4a77176",
)
Q1_REF = ExactRef(
    "WVS7QuestionBinding@1.0.0",
    "question_impl.phase0.068ef710ac1c269b8adf",
    "304fbead4df5035bd97c02ff04000363cc5041129456555e3047ff3ff2efc185",
)

# Exact refs are copied from the accepted P2F2 objects cited by R1D-A.  They are
# deliberately explicit rather than reconstructed from naming resemblance.
MAPPING_ROWS = (
    ("Q291G5", 1, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q0-1:sha256:fe59b34a25ac4a76a08f7507a71294c3569826d6cc4408a7fe9a9109145e3be2", "fe59b34a25ac4a76a08f7507a71294c3569826d6cc4408a7fe9a9109145e3be2"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:afe05c229c77cafeb3b2147e3f52d033f370845dc7ab6e97526a2b3c0135d5d8", "afe05c229c77cafeb3b2147e3f52d033f370845dc7ab6e97526a2b3c0135d5d8"), "1"),
    ("Q291G5", 2, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q0-2:sha256:2a15f85f601f5dd145351cc5179247fe18f13b707dcb88addbd33caa56781094", "2a15f85f601f5dd145351cc5179247fe18f13b707dcb88addbd33caa56781094"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:8c0e8cce557bb71adb99ba9ee9835594fb643032fe39e11a1d8c319316028f48", "8c0e8cce557bb71adb99ba9ee9835594fb643032fe39e11a1d8c319316028f48"), "2"),
    ("Q291G5", 3, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q0-3:sha256:6566a9353a7bc1268019e70b5fc7ebae88efb3d7d70cd54bf87de9b5875d1b3d", "6566a9353a7bc1268019e70b5fc7ebae88efb3d7d70cd54bf87de9b5875d1b3d"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:b19ca77ef63dccef9236d0bf73d4914f042cb0cd28ca9cec6fdd4a20678fecf3", "b19ca77ef63dccef9236d0bf73d4914f042cb0cd28ca9cec6fdd4a20678fecf3"), "3"),
    ("Q291G5", 4, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q0-4:sha256:1bd0d39d693860453e8164e55396c1101a6e0c4c26b27fee2565598e7c567f9e", "1bd0d39d693860453e8164e55396c1101a6e0c4c26b27fee2565598e7c567f9e"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:361ffc5a51d93e23321ab9cf7ae9a6918ac6d3fc151daac8db893fd0648d328d", "361ffc5a51d93e23321ab9cf7ae9a6918ac6d3fc151daac8db893fd0648d328d"), "4"),
    ("Q291G5", 5, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q0-5:sha256:d28bbdfa0022613de2f6c43bf8fa7aec233936901d4967df1e994586ca038ec8", "d28bbdfa0022613de2f6c43bf8fa7aec233936901d4967df1e994586ca038ec8"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:59d3ffbdd5dc937319d2f9f44493303047095240351bdba06fd4e2959f12c73c", "59d3ffbdd5dc937319d2f9f44493303047095240351bdba06fd4e2959f12c73c"), "5"),
    ("Q291P5", 1, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q1-1:sha256:4f34da6a78e75c9c00125dfd7e5cd1469a094646b8362260d83ea56c4ebaa9fc", "4f34da6a78e75c9c00125dfd7e5cd1469a094646b8362260d83ea56c4ebaa9fc"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:55a652713bf0827fc701b3dc05a9e26d7375b4be6792e230dd65f8e8bc3d1e93", "55a652713bf0827fc701b3dc05a9e26d7375b4be6792e230dd65f8e8bc3d1e93"), "1"),
    ("Q291P5", 2, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q1-2:sha256:45459f3e76a19bdc19b38a78491b62acc577977ed11b04eefd813bb162f3eb81", "45459f3e76a19bdc19b38a78491b62acc577977ed11b04eefd813bb162f3eb81"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:85cb7e47ce083deb8614a31bb1b7738c81103e5c81171a931965348338a53766", "85cb7e47ce083deb8614a31bb1b7738c81103e5c81171a931965348338a53766"), "2"),
    ("Q291P5", 3, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q1-3:sha256:d9a9bb8f35fef19aada7e209137a7bc92b1d52a475483b6cb9f7cb6b76f92e64", "d9a9bb8f35fef19aada7e209137a7bc92b1d52a475483b6cb9f7cb6b76f92e64"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:5a239598cf7408de9c588c50e009b873e9a5025092206684ef8f84720ec32dd5", "5a239598cf7408de9c588c50e009b873e9a5025092206684ef8f84720ec32dd5"), "3"),
    ("Q291P5", 4, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q1-4:sha256:bf2d8543a920854a958b5f5109507fda099e364e84955be4fb938c1fb5e5bc57", "bf2d8543a920854a958b5f5109507fda099e364e84955be4fb938c1fb5e5bc57"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:2db758ac0c9100292621d7db3ee9f8fe91c1aa60e897f3513577c11571929365", "2db758ac0c9100292621d7db3ee9f8fe91c1aa60e897f3513577c11571929365"), "4"),
    ("Q291P5", 5, ExactRef("WVS7ResponseValue@1.0.0", "urn:rawlsing:pre553:ee-p2f2:q1-5:sha256:d97b6d0287bf0002fcc6e8c433bf3d9ec823468de18a90b4088b34b4b3f0a967", "d97b6d0287bf0002fcc6e8c433bf3d9ec823468de18a90b4088b34b4b3f0a967"), ExactRef("EmpiricalPredicate@1.0.0", "urn:rawlsing:pre553:EmpiricalPredicate:sha256:880b8cdb115581e231708da4209f6bd9bb469b6288aa4246491d7a9b4d848b99", "880b8cdb115581e231708da4209f6bd9bb469b6288aa4246491d7a9b4d848b99"), "5"),
)

NEGATIVE_LIMITS = (
    "NO_CANONICAL_QUESTION_MAPPING",
    "NO_SPECIAL_CODE_MAPPING_MINUS5_MINUS4_MINUS2_MINUS1",
    "NO_OTHER_WVS7_QUESTION",
    "NO_OTHER_RESPONSE_VALUE",
    "NO_OTHER_WVS_WAVE",
    "NO_OTHER_SOURCE",
    "NO_CROSS_SOURCE_EQUIVALENCE",
    "NO_POOLING",
    "NO_RESPONDENT_LINKAGE",
    "NO_BACKFILL",
    "NO_NEW_RESPONSE_MEANING",
    "NO_NEW_TOPOLOGY",
    "NO_NEW_ROUTING",
    "NO_WEIGHT_AUTHORITY",
    "NO_DESIGN_AUTHORITY",
    "NO_ESTIMAND_AUTHORITY",
    "NO_COORDINATE_SEMANTICS",
    "NO_POPULATION_GENERALIZATION",
    "NO_CANDIDATE_OUTPUT_PARENTAGE",
)

def _negative_limit_ref(limit: str) -> ExactRef:
    material = {"contract": CONTRACT, "negative_limit": limit}
    h = semantic_hash(material)
    return ExactRef(
        "FIABC_LM2_R1E_MAPPING_NEGATIVE_LIMIT@1.0.0",
        f"urn:rawlsing:fiabc:lm2:r1e:mapping-negative-limit:sha256:{h}",
        h,
    )

NEGATIVE_LIMIT_REFS = tuple(_negative_limit_ref(x) for x in NEGATIVE_LIMITS)

MAPPING_AUTHORITY_MATERIAL: Mapping[str, Any] = {
    "schema": CONTRACT,
    "authority_kind": AUTHORITY_KIND,
    "source": {
        "family": "WVS",
        "wave": "W7",
        "source_sha256": SOURCE_SHA256,
    },
    "questions": {
        "Q291G5": Q0_REF.as_dict(),
        "Q291P5": Q1_REF.as_dict(),
    },
    "native_substantive_values": [1, 2, 3, 4, 5],
    "program_semantic_tokens": ["1", "2", "3", "4", "5"],
    "target_use": TARGET_USE,
    "mapping_rows": [
        {
            "question": question,
            "native_code": code,
            "native_response_value_ref": response_ref.as_dict(),
            "accepted_predicate_ref": predicate_ref.as_dict(),
            "relation": "EQ",
            "program_semantic_token": token,
        }
        for question, code, response_ref, predicate_ref, token in MAPPING_ROWS
    ],
    "parents": [
        SOURCE_AUTH_REF.as_dict(),
        PREDICATE_GRAMMAR_AUTH_REF.as_dict(),
    ],
    "provenance_dependencies": [
        RESPONSE_SEMANTICS_REF.as_dict(),
        TARGET_DOMAIN_REPLAY_REF.as_dict(),
        PROGRAM_SCOPE_REF.as_dict(),
        UNIVERSE_REF.as_dict(),
        RISK_SET_REF.as_dict(),
        *[row[2].as_dict() for row in MAPPING_ROWS],
        *[row[3].as_dict() for row in MAPPING_ROWS],
    ],
    "negative_limits": list(NEGATIVE_LIMITS),
    "canonical_question_mapping": "ABSENT_NOT_AUTHORIZED",
    "special_states_mapping": "ABSENT_NOT_AUTHORIZED",
    "cross_source_relation": "NONE_AUTHORIZED",
    "candidate_output_parentage": "FORBIDDEN",
}

MAPPING_AUTHORITY_HASH = semantic_hash(MAPPING_AUTHORITY_MATERIAL)
MAPPING_AUTHORITY_REF = AuthorityRef(
    AUTHORITY_ID,
    AUTHORITY_VERSION,
    MAPPING_AUTHORITY_HASH,
)

def mapping_authority_snapshot() -> AuthoritySnapshot:
    replay_material = {
        "contract": CONTRACT,
        "authority_ref": MAPPING_AUTHORITY_REF.as_dict(),
        "material_hash": MAPPING_AUTHORITY_HASH,
        "governing_hq_seal": GOVERNING_HQ_SEAL,
        "commission_commit": COMMISSION_COMMIT,
    }
    replay_hash = semantic_hash(replay_material)
    replay_ref = ExactRef(
        "FIABC_LM2_R1E_MAPPING_AUTHORITY_REPLAY_ROOT@1.0.0",
        f"urn:rawlsing:fiabc:lm2:r1e:mapping-authority-replay:sha256:{replay_hash}",
        replay_hash,
    )
    dependencies = (
        RESPONSE_SEMANTICS_REF,
        TARGET_DOMAIN_REPLAY_REF,
        PROGRAM_SCOPE_REF,
        UNIVERSE_REF,
        RISK_SET_REF,
        *(row[2] for row in MAPPING_ROWS),
        *(row[3] for row in MAPPING_ROWS),
    )
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=dependencies,
        producer_replay_locator_or_reference_root=replay_ref,
        authority_id=MAPPING_AUTHORITY_REF.authority_id,
        authority_version=MAPPING_AUTHORITY_REF.authority_version,
        authority_content_hash=MAPPING_AUTHORITY_REF.authority_content_hash,
        authority_kind=AUTHORITY_KIND,
        decision_state="ALLOW",
        governed_operations=(GOVERNED_OPERATION,),
        governed_object_families=("RespondentEvent@1.0.0",),
        scope_envelope={
            "source_universe_refs": [UNIVERSE_REF.as_dict()],
            "target_use_refs": [TARGET_USE],
            "predicate_or_risk_set_refs": [RISK_SET_REF.as_dict()],
            "program_scope_refs": [PROGRAM_SCOPE_REF.as_dict()],
            "question_refs": [Q0_REF.as_dict(), Q1_REF.as_dict()],
            "native_substantive_values": [1, 2, 3, 4, 5],
        },
        effective_time_or_interval={
            "governing_hq_seal": GOVERNING_HQ_SEAL,
            "commission_commit": COMMISSION_COMMIT,
            "commission": "FIABC-LM2-R1E",
        },
        parent_authority_refs=(SOURCE_AUTH_REF, PREDICATE_GRAMMAR_AUTH_REF),
        negative_limit_refs=NEGATIVE_LIMIT_REFS,
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({
            "authority_ref": MAPPING_AUTHORITY_REF.as_dict(),
            "target_use": TARGET_USE,
            "mapping_rows": MAPPING_AUTHORITY_MATERIAL["mapping_rows"],
            "negative_limits": list(NEGATIVE_LIMITS),
        }),
        replay_protocol_ref=replay_ref,
    )

def authority_parent_and_scope_ledger() -> Mapping[str, Any]:
    snapshot = mapping_authority_snapshot()
    return {
        "schema": "FIABC_LM2_R1E_AUTHORITY_PARENT_AND_SCOPE_LEDGER@1.0.0",
        "authority_ref": MAPPING_AUTHORITY_REF.as_dict(),
        "authority_snapshot_ref": snapshot.ref.as_dict(),
        "authority_kind": snapshot.authority_kind,
        "parents": canonicalize(snapshot.parent_authority_refs),
        "dependencies": [x.as_dict() for x in snapshot.dependency_refs],
        "scope_envelope": canonicalize(snapshot.scope_envelope),
        "negative_limit_refs": canonicalize(snapshot.negative_limit_refs),
        "mapping_material": MAPPING_AUTHORITY_MATERIAL,
    }

__all__ = [
    "AUTHORITY_ID",
    "AUTHORITY_KIND",
    "AUTHORITY_VERSION",
    "COMMISSION_COMMIT",
    "CONTRACT",
    "GOVERNING_HQ_SEAL",
    "GOVERNED_OPERATION",
    "MAPPING_AUTHORITY_HASH",
    "MAPPING_AUTHORITY_MATERIAL",
    "MAPPING_AUTHORITY_REF",
    "MAPPING_ROWS",
    "NEGATIVE_LIMITS",
    "NEGATIVE_LIMIT_REFS",
    "PREDICATE_GRAMMAR_AUTH_REF",
    "PROGRAM_SCOPE_REF",
    "RISK_SET_REF",
    "SOURCE_AUTH_REF",
    "SOURCE_SHA256",
    "TARGET_DOMAIN_REPLAY_REF",
    "TARGET_USE",
    "UNIVERSE_REF",
    "authority_parent_and_scope_ledger",
    "mapping_authority_snapshot",
]
