"""Bounded LiTS-I AS2B -> shared PRE553 I03 operation succession.

The accepted AS3R3 successor queries name the shared PRE553 I03 execution
contract while retaining the exact AS2B LiTS-I query authority ref.  This
record binds only that already-adopted pairing.  It does not alias operations
generically and does not alter the frozen runtime catalog or workload.
"""
from __future__ import annotations

from types import MappingProxyType

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    canonicalize,
    semantic_hash,
)


SCHEMA = "FIABC_LITS_I_I03_OPERATION_SUCCESSOR_AUTHORITY@1.0.0"
SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
PART_A_PROJECTION_AUTHORITY_HASH = "9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06"
RUNTIME_CATALOG_IDENTITY = "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02"
RUNTIME_SNAPSHOT_CONTENT_HASH = "a3435ceb84a1ebf1efb9c031bd56c4bff61cdbba55a837043d64a0a5d4f3aef7"
PARENT_OPERATION = "AS2B_LITS1_I03_QUERY"
SUCCESSOR_OPERATION = "PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0"

PARENT_AUTHORITY_REF = AuthorityRef(
    "urn:rawlsing:pre553:as2b:lits1:authority:i03_query",
    "AS2A-BANKED-1.0.0",
    "6c6d2f5fb5f4165e5de19989bd456ee8c09f42ab175fa4d10572dc2b9403ca0d",
)
SOURCE_UNIVERSE_REF = ExactRef(
    "EmpiricalUniverse@1.0.0",
    "urn:rawlsing:pre553:EmpiricalUniverse:sha256:83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080",
    "83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080",
)
_EXECUTED_QUERY_HASHES = (
    "06ce0011b9871286a0d1eb271cdf85b2333652acebc9378c3dab7f32651bd748",
    "086c4d9bdad91aeacb93c84fa6cba1e61e77f9390438638251c4f8cce548b3e8",
    "09770b9d4ceb11481cd589d31b5dda3235984651f9b513cb7b9168370b94f507",
    "147b633895dba227e8334e167a1ed46b1e6b05585a7743e45fd7e14bc113085e",
    "169774a791eff18a8bd9541785bccab4a525774c750375aaccad1ff630d47a9d",
    "192a85dded0dc18f1eb88dd3d3a7252fff80ca551b1681be1923156e6a13fd4d",
    "1afcc022903de7fadae3c960ba7bd6009f7b7e096b1a476ae2a43b263a5bd7e9",
    "1dfe1daab85e6113fbb5a200197bbffa5e21e203cb9303f18c8be34474612f01",
    "2815a6e1838a1934672222ff500d1c29c869a9acf92613c1e563254a30fc14ca",
    "28f51ca4c082588bc74b6228b3c6d4709928528c125c87256f305919fc9454be",
    "29a7c0bd51bf7c62c67128799a004eee942fea5f93220ee83d6075819da19fd0",
    "3419fd8377bd3b681315191bd22a3c37a95443946c0a0477b2c591e6690bfbd0",
    "34856cd6b89cce0ad311c166611e572443da6ce8fc3622f212eaa9e20d7efed7",
    "36d8174678099d9d8e15f2526353065fbe700267797782385ca03558f1f4aa52",
    "4089fb78d6e5cdf06b8a518257c82ee68c3c97876b1cb96c4090f0ba0fa6be36",
    "44339ced9e03b76a6ef7308d0b113eb5bb5c36e3d456b8ae9235f1efbcef82a4",
    "44f7b9968ec91be074b4f71782f8ca52e7a2f186c81bebedf3af66ab0a2e76fa",
    "47e1a30a35234e8fc14501f3f0c015f503fb978045fafd471977ca079726cca5",
    "5fd37f8902a648a764f5e306e0b8db5971ac7a69a369b2f8ac6b989e04f22a62",
    "62c66b9cdf84e942f8a0e6ab4b40931fed54c049a319c982be11b9caf7e16e20",
    "6e71468b9c1275803d982d8eebb572b97b115822b6fbb2b020daa0bbced53f9a",
    "6ee12199bb7b5aabd62f0bd18d469d115b48d2cb0b5f30b36ff48a23903c6cbd",
    "711dd75cc656d1f0036a7079b43b9d130c3ec2e282fb6d62297eecb02df6ab51",
    "73e2c496ff927a23f884771961b1d7d541541d03d3c12e5cd032400c1d271faf",
    "757682be7272f4f8424480f813bdcd41f7643f059be91cecef9f528be7966b12",
    "7667c01922bf5044c14a15e7ca39ebebcfb474bab38fde2c7889fd4020fac3e6",
    "76fbb05d79b0d9f348b4682f502bc8c2450891cd3b28b37bcbfe4c40aa01d1fb",
    "7888ceb9eb1883bdc50885ff18369003aa3c98dcfb26b4e826d86ba702324093",
    "7a4c1f25d870760bedc58cdb7fd7c547ab8d7d966fed3456a60586a60f2c7b63",
    "7abe35df3bcf4e586c0aa70f4d3b6968e4bf9b3e76329b759d9c9dce1a0fe9ee",
    "7d11f83b66d3e7c5c6dd252df1adc6f5c735ef4d8d4f80da1719e76d554c4cb6",
    "83caf8175926832e61429e097f4ad352361b95b66a2bafcef3edd32583377bd6",
    "8ccb5378f50b6ab84b259701303b166fff28feef502367f322c0e04810c8b769",
    "96ccfc6bb20ea26ad88b44e7704a28d164e201d24a75d5e2a96437aaf2cef867",
    "9740250f2e9efbd50e0279a88fc464a6921d87c8dcb67f2f190289f14a1aead6",
    "9871c16351bdaffa100d0195a7ab28162e99d5af443f1636e980beb5f6db79ee",
    "9bee1dc15060f45c74d72e3bc83d50d39905b509a394540c86ef294e9ca0caed",
    "a0be3406c8c81c37e51851399b7ad42ba7249ff3d049505d3aef28becdff8a3a",
    "a213a3278a9e3b6128dd142f8d47f02a92ad0d41abac904b0c1c4898033281f5",
    "a4aead8d8df9a68ff769d6879d5be1b68d065f6410cda115d85d1c7cf9732849",
    "aa0b18b085f85c0031c4b9f71d14c7a1a9f6b0e3cd46a33339cdfa974c99514b",
    "ad29b4175844ef08314ca612f2e6ed46ebe65380624db5758bc8132f64204c21",
    "af81acf2f2e2386b8effcdee79d74edf8f543c8df911767e7ae8c8bb102ca7e7",
    "b83bcfc7850a9d8d6e680b0f77ac08160f158bb16d8e05e0d701ddf61591c002",
    "bbceb7cb073eb477e335e7a1f17d47d1ebde8c7fae5dd6f590ad88a3b57a31b2",
    "c74fe0e73ea6d3cec08258000ba8f6a4310d2c073eb886ab7649f98e15df247c",
    "cc1d24d9a5d8e6fd0962cb03c02c34d7d73694292f1d9fec0d1e1ae688bf870b",
    "cd9d885cc2e88f3ea86114be18654ce59e1127ac5b0f0802e24ea5a4b364e794",
    "d13de9565d9eaa570ae02cb8e013e501f6c79b855427ce6eee5c6fbef0ae9d94",
    "d1c77eb61624ee787cb52497ccdc34f30185d4f0334c702fd6d505d4d13177cc",
    "d54cca4abc855e81f7589ce47d522fdafd41042ffd01452e1eadc89086d8d102",
    "d86f9c44abbbe07e42f25f39cca62dcab716eacf59d63d09cdadd2a16fcd47e1",
    "e12c7136bb568f95c5776a474badf1ce506062b402b6a454a300935b00144f88",
    "e1f8e70c8b016e21b96cbdf261bab0e7bde27264ed7aa528ffec09cf46245ac7",
    "e8b406030cfaa555feb58143c768cc583c5662e29cbec73b33aac989f2957f65",
    "ea4ff8eb268ae6f0cbde8d8d60d237a277482ffd3194b3d098f4774f67ebee2b",
    "ed1c941742a5c84a6d1b9bbd95a1a7a9c8ad557d2fea3d7b60b38aada02c95bf",
    "f6a59cef7a8fe15cfef01186ab599236fec3a3d3fae4f4e5aa125ca00c3e5032",
    "f6e8c7670128b19ff909a1375f1ff930e53fdd26a400d7de5401b96aae043ace",
    "fc6c461521979fff781a65a89464cd2b71231590c59bb663d3387d25145a3fc8",
)
QUERY_REFS = tuple(
    ExactRef(
        "EmpiricalQuerySpec@1.0.0",
        f"urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:{digest}",
        digest,
    )
    for digest in _EXECUTED_QUERY_HASHES
)
GOVERNED_OBJECT_FAMILIES = (
    "EmpiricalFact@1.0.0",
    "EmpiricalPredicate@1.0.0",
    "EmpiricalQuerySpec@1.0.0",
)
SUCCESSION_AUTHORITY_REFS = (
    AuthorityRef(
        "urn:rawlsing:governance:authority-28:28_AS3R3_RUNTIME_IDENTITY_SUCCESSION_HQ_ADOPTION.md",
        "git:fdef92776e055e1d4a667d8e616d01c44e84b688",
        "49b33bca6b64e1557817e94d108e573a45756a40e39157ebba754d32a64b89b5",
    ),
    AuthorityRef(
        "urn:rawlsing:governance:authority-29:29_AS3R3_PRODUCER_IDENTITY_FREEZE_AND_INPUT_FREEZE_AUTHORIZATION.md",
        "git:fdef92776e055e1d4a667d8e616d01c44e84b688",
        "6e2e51d4157bfc5d7de49014b0a960575758cfff03f9083085ab1d8a8caf040e",
    ),
    AuthorityRef(
        "urn:rawlsing:governance:authority-30:30_AS3R3_TWO_PHASE_PREDICATE_THEN_QUERY_INPUT_AND_MINT_SEQUENCE_CORRECTION.md",
        "git:fdef92776e055e1d4a667d8e616d01c44e84b688",
        "2217a905270cda0aeb23ccb4b6ece0cd1342f31a85e015652718eade00fed38c",
    ),
    AuthorityRef(
        "urn:rawlsing:governance:authority-34:34_PREV3_WAVE1_R2_AND_AS3R3_CARDINALITY_ADOPTION.md",
        "git:16098c57883fde512e933eb1a220ea59b6c526a8",
        "53b0fe9d963da7887c0a5052a035772d1efde968f4652450916e63ca427cd627",
    ),
)
NEGATIVE_LIMITS = (
    "NO_GENERIC_OPERATION_ALIAS",
    "NO_OTHER_QUERY_REFS",
    "NO_OTHER_SOURCE_UNIVERSE",
    "NO_OTHER_RUNTIME_CATALOG",
    "NO_WORKLOAD_OR_CANDIDATE_IDENTITY_MUTATION",
    "NO_RESPONSE_SEMANTIC_REMAP",
    "NO_VALUE_LABEL_FREQUENCY_OR_MISSINGNESS_INFERENCE",
    "NO_CANDIDATE_OUTPUT_PARENTAGE",
)

IDENTITY_MATERIAL = MappingProxyType(canonicalize({
    "source_sha256": SOURCE_SHA256,
    "runtime_catalog_identity": RUNTIME_CATALOG_IDENTITY,
    "runtime_snapshot_content_hash": RUNTIME_SNAPSHOT_CONTENT_HASH,
    "parent_authority_ref": PARENT_AUTHORITY_REF.as_dict(),
    "parent_operation": PARENT_OPERATION,
    "successor_operation": SUCCESSOR_OPERATION,
    "source_universe_refs": [SOURCE_UNIVERSE_REF.as_dict()],
    "query_refs": [ref.as_dict() for ref in QUERY_REFS],
    "governed_object_families": list(GOVERNED_OBJECT_FAMILIES),
    "frozen_workload": {"candidate_count": 50, "query_role_executions": 77},
    "succession_authority_refs": [ref.as_dict() for ref in SUCCESSION_AUTHORITY_REFS],
    "historical_preimage": {
        "owner_commit": "3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f",
        "builder_blob": "c51b56779ab9d79126619b7733d41f5253c8150f",
        "parent_authority_families": list(GOVERNED_OBJECT_FAMILIES),
    },
    "negative_limits": list(NEGATIVE_LIMITS),
}))
AUTHORITY_CONTENT_HASH = semantic_hash(IDENTITY_MATERIAL)


def operation_successor_authority_record():
    """Return a detached exact authority record for runtime adoption."""
    return {
        "schema": SCHEMA,
        "authority_content_hash": AUTHORITY_CONTENT_HASH,
        "identity_material": canonicalize(IDENTITY_MATERIAL),
    }


def _historical_ref(kind: str, tag: str, material) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(
        kind,
        f"urn:rawlsing:pre553:as2b:{tag}:sha256:{digest}",
        digest,
    )


def historical_projection_authority_snapshot() -> AuthoritySnapshot:
    """Reconstruct the exact accepted AS2B Part-A projection snapshot."""
    role = "part_a_projection"
    kind = "SOURCE_SEMANTICS_TOPOLOGY"
    families = (
        "EmpiricalUniverse@1.0.0",
        "RespondentEvent@1.0.0",
        "EmpiricalCoordinateFact@1.0.0",
        "RoutingEligibilityFact@1.0.0",
    )
    material = {
        "court": "AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827",
        "role": role,
        "kind": kind,
        "source_sha256": SOURCE_SHA256,
        "part_a_projection_authority_hash": PART_A_PROJECTION_AUTHORITY_HASH,
        "families": families,
    }
    replay_root = _historical_ref("REPLAY_ROOT", f"authority-{role}", material)
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=replay_root,
        authority_id="urn:rawlsing:pre553:as2b:lits1:authority:part_a_projection",
        authority_version="AS2A-BANKED-1.0.0",
        authority_content_hash=PART_A_PROJECTION_AUTHORITY_HASH,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=("AS2B_LITS1_PART_A_PROJECTION",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="LITS1_2006_AS2B_EXECUTION",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({
            **material,
            "ceiling": "AS2A_BANKED_ONLY",
        }),
        replay_protocol_ref=_historical_ref(
            "REPLAY_PROTOCOL", f"authority-{role}", material
        ),
    )


def historical_i03_parent_authority_snapshot() -> AuthoritySnapshot:
    """Reconstruct the exact accepted AS2B I03 parent authority snapshot."""
    role = "i03_query"
    kind = "PREDICATE_GRAMMAR"
    # Preserve the banked builder's pre-hash family sequence exactly.
    # AuthoritySnapshot canonicalizes governed_object_families later, but the
    # historical authority_content_hash was minted from this ordered material.
    families = (
        "EmpiricalPredicate@1.0.0",
        "EmpiricalQuerySpec@1.0.0",
        "EmpiricalFact@1.0.0",
    )
    material = {
        "court": "AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827",
        "role": role,
        "kind": kind,
        "source_sha256": SOURCE_SHA256,
        "part_a_projection_authority_hash": PART_A_PROJECTION_AUTHORITY_HASH,
        "families": families,
    }
    authority_hash = semantic_hash(material)
    if authority_hash != PARENT_AUTHORITY_REF.authority_content_hash:
        raise RuntimeError("banked AS2B I03 parent authority identity drift")
    replay_root = _historical_ref("REPLAY_ROOT", f"authority-{role}", material)
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=replay_root,
        authority_id=PARENT_AUTHORITY_REF.authority_id,
        authority_version=PARENT_AUTHORITY_REF.authority_version,
        authority_content_hash=authority_hash,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(PARENT_OPERATION,),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="LITS1_2006_AS2B_EXECUTION",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({
            **material,
            "ceiling": "AS2A_BANKED_ONLY",
        }),
        replay_protocol_ref=_historical_ref(
            "REPLAY_PROTOCOL", f"authority-{role}", material
        ),
    )


__all__ = [
    "SCHEMA",
    "SOURCE_SHA256",
    "PART_A_PROJECTION_AUTHORITY_HASH",
    "RUNTIME_CATALOG_IDENTITY",
    "RUNTIME_SNAPSHOT_CONTENT_HASH",
    "PARENT_OPERATION",
    "SUCCESSOR_OPERATION",
    "PARENT_AUTHORITY_REF",
    "SOURCE_UNIVERSE_REF",
    "QUERY_REFS",
    "GOVERNED_OBJECT_FAMILIES",
    "SUCCESSION_AUTHORITY_REFS",
    "NEGATIVE_LIMITS",
    "IDENTITY_MATERIAL",
    "AUTHORITY_CONTENT_HASH",
    "operation_successor_authority_record",
    "historical_projection_authority_snapshot",
    "historical_i03_parent_authority_snapshot",
]
