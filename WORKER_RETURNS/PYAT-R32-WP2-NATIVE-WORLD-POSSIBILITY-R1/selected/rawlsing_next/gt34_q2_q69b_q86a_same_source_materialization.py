"""GT3/GT4 Q2 exact Q69B + Q86A same-source PRE553/C11 materialization.

Closes only OBL049 at the first-canary grain. Existing exact Q69B and Q86A
semantic/routing identities are repackaged over one shared R5 universe and
respondent set. The only newly minted authority is a package-specific
REPLAY_PROTOCOL authority whose scope is mechanical deterministic replay.

No portability, pooling, new empirical meaning, comparator, PSEPF, actor,
metabolism, CAN-008, V3, or V2 authority is created.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Final, Mapping

from rawlsing_next.pre553_c11_ingest import (
    C11SourceReleaseCandidate,
    INGEST_CONTRACT_VERSION,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    record_counts_for_candidate,
    validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    canonical_json,
    exact_ref,
    semantic_hash,
)
import rawlsing_next.pre553_repo_native_current_payload as current_gt2
import rawlsing_next.wave1_r5_q86_c11_projection as q86
import rawlsing_next.wave2_r5_q69b_conditioner_projection as q69b


class Q2SameSourceMaterializationError(ValueError):
    """Exact Q2 transport or same-source C11 materialization failed closed."""


CONTRACT_ID: Final[str] = "GT34_Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION@1.0.0"
CANDIDATE_RELEASE_ID: Final[str] = "R5_GT34_Q2_Q69B_Q86A_SAME_SOURCE_CANDIDATE_R1"
TRANSPORT_SCHEMA: Final[str] = "GT34_Q2_R5_Q69B_Q86A_SAME_SOURCE_TRANSPORT@1.0.0"
TRANSPORT_SEMANTIC_SHA256: Final[str] = "f179a516f6bd14618e507ca1ebff0cdf85a954e792889d74f37ea93fc1561a61"
TRANSPORT_GZIP_SHA256: Final[str] = "bac725d53f1a125636d0687ecee89ad9ca8a11f5e558e7fe9089a8fb1d57ed82"
TRANSPORT_CANONICAL_BYTES: Final[int] = 4_220_457
TRANSPORT_GZIP_BYTES: Final[int] = 933_040
MATERIALIZED_ROWS: Final[int] = 19_210

Q86A_RECOVERED_SEMANTIC_SHA256: Final[str] = "0061237c37418d9192fce6dbf464aa28391b8c665c5379748941477f3d353d9f"
Q86A_RECOVERED_GZIP_SHA256: Final[str] = "d45ba476e16d6abcac7031536006c413a2c44c3dd351b093a525e2df43bb0669"
FFP017_RISK_SET_SHA256: Final[str] = "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
FFP017_RESPONSE_SHA256: Final[str] = "98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709"
FFP017_EXPOSURE_SHA256: Final[str] = "0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce"
Q69B_CURRENT_RELEASE_SHA256: Final[str] = "2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec"
Q69B_CURRENT_MANIFEST_SHA256: Final[str] = "15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4"

Q86_ACCEPTED_RELEASE_SHA256: Final[str] = "8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295"
Q86_ACCEPTED_REPLAY_MANIFEST_SHA256: Final[str] = "c80d08ca9a5bb4814bdca3c0c21cb4c708da32840d6459b190cca206c3e3b4aa"
Q86AB_SOURCE_KEY_SEQUENCE_SHA256: Final[str] = "b5370c6df7f0e5a987a4469820c44e5cfa7da140da96737418ca9d22b3df7b37"
Q86AB_STATE_PAIRS_RAW_SHA256: Final[str] = "b49116eabdc74c3292795c25f0921545ec148300d078bb8c30d1091796684595"
Q86AB_STATE_PAIRS_GZIP_SHA256: Final[str] = "567aa614d477423ccc0def12f9337290c23050504634c11693c952556cd1e2a8"
Q86AB_STATE_PAIRS_RAW_BYTES: Final[int] = 51_587
Q86AB_STATE_PAIRS_GZIP_BYTES: Final[int] = 12_508
FFP014_RISK_KEY_LOCAL_ID_PAIRS_CARRIER_ORDER_SHA256: Final[str] = "a4ea782fcbc3f1f6e50061c80ba304ce91dddfc0e70ba2da79e40613b636928b"
FFP014_RISK_KEY_LOCAL_ID_PAIR_SET_SHA256: Final[str] = "32579518a258ba376e3221a9fa1416c656027cc5f45188eb5b9ca97c3c103dc6"
_Q86_STATE_ORDER: Final[tuple[str, ...]] = ("-1", "0", "1", "9", "997", "998")
_Q86_NONEXPOSED_ALPHA3: Final[frozenset[str]] = frozenset({"ALG", "EGY", "MRC", "SUD", "TUN"})
_EXPECTED_Q86_SOURCE_EXPOSURE_COUNTS: Final[dict[str, int]] = {
    "EXPOSED__PROVED": 45_598,
    "NONEXPOSURE__PROVED": 5_989,
}

_TRANSPORT_RELATIVE: Final[Path] = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_POST_P_FANIN_REPAIR_WAVE_R1/"
    "Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION_R1/transport/"
    "q69b_q86a_same_source_transport.json.gz"
)

_Q86AB_STATE_PAIRS_RELATIVE: Final[Path] = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_POST_P_FANIN_REPAIR_WAVE_R1/"
    "Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION_R1/transport/"
    "q86ab_ffp017_source_state_pairs.bin.gz"
)

TRANSPORT_REF: Final[ExactRef] = ExactRef(
    "GT34_Q2_SAME_SOURCE_TRANSPORT", TRANSPORT_SCHEMA, TRANSPORT_SEMANTIC_SHA256
)
Q86A_RECOVERED_REF: Final[ExactRef] = ExactRef(
    "FFP017_RECOVERED_Q86A_RISK_VALUES",
    "FFP017:Q86A:CORE_CLAIM_COMMON_RISK_SET@1",
    Q86A_RECOVERED_SEMANTIC_SHA256,
)
Q69B_CURRENT_RELEASE_REF: Final[ExactRef] = ExactRef(
    "C11LogicalRelease", q69b.CANDIDATE_RELEASE_ID, Q69B_CURRENT_RELEASE_SHA256
)
Q86_CURRENT_RELEASE_REF: Final[ExactRef] = q69b.PREDECESSOR_RELEASE_REF

_EXPECTED_Q86A_COUNTS: Final[dict[str, int]] = {"-1": 8, "0": 2643, "1": 15984, "9": 575}
_EXPECTED_Q69B_TYPED_COUNTS: Final[dict[str, int]] = {
    "MISSING": 49,
    "PUBLIC_CLINIC_EXPERIENCE_ABSENT": 2433,
    "PUBLIC_CLINIC_EXPERIENCE_PRESENT": 16604,
    "UNKNOWN": 124,
}
_ROW_SCHEMA: Final[list[str]] = [
    "source_row_ordinal",
    "respondent_key",
    "pre553_respondent_content_hash",
    "country_alpha3",
    "q69b_native_code",
    "q69b_typed_state",
    "dateintr_raw_exact_token",
    "dateintr_iso",
    "dateintr_state",
    "q86a_native_code",
    "q86a_response_state",
    "q86a_exposure_state",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _transport_path() -> Path:
    return _repo_root() / _TRANSPORT_RELATIVE


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _eref(kind: str, object_id: str, material: Any) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash(material))


@dataclass(frozen=True)
class SameSourceRow:
    source_row_ordinal: int
    respondent_key: str
    pre553_respondent_content_hash: str
    country_alpha3: str
    q69b_native_code: int
    q69b_typed_state: str
    dateintr_raw_exact_token: str
    dateintr_iso: str
    dateintr_state: str
    q86a_native_code: str
    q86a_response_state: str
    q86a_exposure_state: str

    @classmethod
    def from_wire(cls, wire: Any) -> "SameSourceRow":
        if not isinstance(wire, list) or len(wire) != 12:
            raise Q2SameSourceMaterializationError("Q2 transport row schema mismatch")
        row = cls(*wire)
        if not isinstance(row.source_row_ordinal, int) or isinstance(row.source_row_ordinal, bool):
            raise Q2SameSourceMaterializationError("Q2 source row ordinal invalid")
        if not isinstance(row.respondent_key, str) or row.respondent_key.count("|") != 1:
            raise Q2SameSourceMaterializationError("Q2 respondent key invalid")
        if (
            not isinstance(row.pre553_respondent_content_hash, str)
            or len(row.pre553_respondent_content_hash) != 64
            or any(ch not in "0123456789abcdef" for ch in row.pre553_respondent_content_hash)
        ):
            raise Q2SameSourceMaterializationError("Q2 PRE553 respondent hash invalid")
        if row.q86a_native_code not in q86._STATE:
            raise Q2SameSourceMaterializationError("Q2 Q86A code outside accepted domain")
        if row.q86a_response_state != q86._STATE[row.q86a_native_code].response_state:
            raise Q2SameSourceMaterializationError("Q2 Q86A state/code mismatch")
        if row.q86a_exposure_state != "EXPOSED__PROVED":
            raise Q2SameSourceMaterializationError("Q2 requires exact FFP017 Q86A exposure proof")
        if row.dateintr_state != "VALID":
            raise Q2SameSourceMaterializationError("Q2 Q69B DATEINTR state must remain VALID")
        return row


@dataclass(frozen=True)
class SameSourceTransport:
    raw: Mapping[str, Any]
    rows: tuple[SameSourceRow, ...]


def _verify_transport_material(material: Any) -> SameSourceTransport:
    if not isinstance(material, Mapping):
        raise Q2SameSourceMaterializationError("Q2 transport root must be mapping")
    if material.get("schema_id") != TRANSPORT_SCHEMA:
        raise Q2SameSourceMaterializationError("Q2 transport schema drift")
    source = material.get("source")
    if not isinstance(source, Mapping) or (
        source.get("object_id") != q69b.SOURCE_ARTIFACT_ID
        or source.get("sha256") != q69b.SOURCE_SHA256
        or source.get("byte_count") != q69b.SOURCE_BYTES
        or source.get("rows") != q69b.SOURCE_ROWS
    ):
        raise Q2SameSourceMaterializationError("Q2 source identity drift")
    scope = material.get("scope")
    if not isinstance(scope, Mapping) or (
        scope.get("risk_set_semantic_sha256") != FFP017_RISK_SET_SHA256
        or scope.get("rows") != MATERIALIZED_ROWS
        or scope.get("empirical_universe_sha256") != q69b.ACCEPTED_UNIVERSE_SHA256
    ):
        raise Q2SameSourceMaterializationError("Q2 risk/universe scope drift")
    pred = material.get("predecessors")
    if not isinstance(pred, Mapping) or (
        pred.get("q69b_release_id") != q69b.CANDIDATE_RELEASE_ID
        or pred.get("q69b_release_semantic_sha256") != Q69B_CURRENT_RELEASE_SHA256
        or pred.get("q69b_release_manifest_sha256") != Q69B_CURRENT_MANIFEST_SHA256
        or pred.get("q69b_transport_semantic_sha256") != q69b.TRANSPORT_SEMANTIC_SHA256
        or pred.get("q69b_transport_gzip_sha256") != q69b.TRANSPORT_GZIP_SHA256
        or pred.get("q86_release_id") != q69b.PREDECESSOR_RELEASE_ID
        or pred.get("q86_release_semantic_sha256") != q69b.PREDECESSOR_RELEASE_SHA256
        or pred.get("q86a_question_ref") != q86.question_ref("Q86A").as_dict()
        or pred.get("q86a_domain_ref") != q86.domain_ref("Q86A").as_dict()
    ):
        raise Q2SameSourceMaterializationError("Q2 predecessor ancestry drift")
    carrier = material.get("ffp017_external_carrier_recovery")
    if not isinstance(carrier, Mapping) or (
        carrier.get("selected_response_facts_sha256") != FFP017_RESPONSE_SHA256
        or carrier.get("selected_exposure_facts_sha256") != FFP017_EXPOSURE_SHA256
        or carrier.get("risk_set_semantic_sha256") != FFP017_RISK_SET_SHA256
        or carrier.get("recovered_q86a_semantic_sha256") != Q86A_RECOVERED_SEMANTIC_SHA256
        or carrier.get("recovered_q86a_gzip_sha256") != Q86A_RECOVERED_GZIP_SHA256
        or carrier.get("response_presence_is_exposure_evidence") is not False
    ):
        raise Q2SameSourceMaterializationError("Q2 FFP017 carrier ancestry drift")
    counts = material.get("counts")
    if not isinstance(counts, Mapping) or (
        dict(counts.get("q86a_native", {})) != _EXPECTED_Q86A_COUNTS
        or dict(counts.get("q69b_typed", {})) != _EXPECTED_Q69B_TYPED_COUNTS
    ):
        raise Q2SameSourceMaterializationError("Q2 typed/native counts drift")
    if material.get("row_schema") != _ROW_SCHEMA:
        raise Q2SameSourceMaterializationError("Q2 row schema drift")
    wires = material.get("rows")
    if not isinstance(wires, list) or len(wires) != MATERIALIZED_ROWS:
        raise Q2SameSourceMaterializationError("Q2 row count drift")
    rows = tuple(SameSourceRow.from_wire(wire) for wire in wires)
    if len({row.source_row_ordinal for row in rows}) != MATERIALIZED_ROWS:
        raise Q2SameSourceMaterializationError("Q2 source row ordinal collision")
    if len({row.respondent_key for row in rows}) != MATERIALIZED_ROWS:
        raise Q2SameSourceMaterializationError("Q2 respondent collision")
    if tuple(row.source_row_ordinal for row in rows) != tuple(sorted(row.source_row_ordinal for row in rows)):
        raise Q2SameSourceMaterializationError("Q2 transport row order drift")
    return SameSourceTransport(material, rows)


def load_same_source_transport() -> SameSourceTransport:
    compressed = _transport_path().read_bytes()
    if len(compressed) != TRANSPORT_GZIP_BYTES or _sha256(compressed) != TRANSPORT_GZIP_SHA256:
        raise Q2SameSourceMaterializationError("Q2 committed gzip identity mismatch")
    canonical = gzip.decompress(compressed)
    if len(canonical) != TRANSPORT_CANONICAL_BYTES or _sha256(canonical) != TRANSPORT_SEMANTIC_SHA256:
        raise Q2SameSourceMaterializationError("Q2 transport semantic identity mismatch")
    material = json.loads(canonical)
    if canonical_json(material).encode("utf-8") != canonical:
        raise Q2SameSourceMaterializationError("Q2 transport is not canonical JSON")
    return _verify_transport_material(material)


def _q2_replay_authority(
    q69b_replay: AuthoritySnapshot,
    q86_replay: AuthoritySnapshot,
) -> AuthoritySnapshot:
    deps = tuple(sorted({
        q69b.SOURCE_REF,
        TRANSPORT_REF,
        Q86A_RECOVERED_REF,
        Q69B_CURRENT_RELEASE_REF,
        Q86_CURRENT_RELEASE_REF,
        q69b.TRANSPORT_REF,
        q86.FROZEN_BINDINGS.response_ref,
        q86.FROZEN_BINDINGS.exposure_ref,
        q86.FROZEN_BINDINGS.risk_ref,
        q69b.CURRENTNESS_REF,
    }, key=lambda ref: ref.key))
    material = {
        "contract": CONTRACT_ID,
        "id": "GT34-Q2-R5-Q69B-Q86A-SAME-SOURCE-REPLAY",
        "version": "1.0.0",
        "kind": "REPLAY_PROTOCOL",
        "operation": "PACKAGE_EXISTING_EXACT_Q69B_AND_Q86A_IDENTITIES_IN_ONE_C11_RELEASE",
        "scope": {
            "source_ref": q69b.SOURCE_REF.as_dict(),
            "q69b_release_ref": Q69B_CURRENT_RELEASE_REF.as_dict(),
            "q86_release_ref": Q86_CURRENT_RELEASE_REF.as_dict(),
            "q2_transport_ref": TRANSPORT_REF.as_dict(),
            "risk_set_ref": q86.FROZEN_BINDINGS.risk_ref.as_dict(),
            "rows": MATERIALIZED_ROWS,
            "semantic_owner_transfer": False,
            "portability": "NONE",
            "pooling": "NONE",
            "predecessor_mutation": False,
        },
        "dependencies": [ref.as_dict() for ref in deps],
        "parents": [
            q69b_replay.authority_ref.as_dict(),
            q86_replay.authority_ref.as_dict(),
        ],
    }
    authority_hash = semantic_hash(material)
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=_eref(
            "AUTHORITY_REPLAY_ROOT",
            "GT34-Q2-R5-Q69B-Q86A-SAME-SOURCE-REPLAY:replay",
            material,
        ),
        authority_id="GT34-Q2-R5-Q69B-Q86A-SAME-SOURCE-REPLAY",
        authority_version="1.0.0",
        authority_content_hash=authority_hash,
        authority_kind="REPLAY_PROTOCOL",
        decision_state="ALLOW",
        governed_operations=("GT34_Q2_Q69B_Q86A_SAME_SOURCE_C11_REPLAY",),
        governed_object_families=("ReplayReceipt@1.0.0",),
        scope_envelope=material["scope"],
        effective_time_or_interval="GT34_Q2_OBL049_CANDIDATE_ONLY__NO_SEMANTIC_WIDENING",
        parent_authority_refs=(
            q69b_replay.authority_ref,
            q86_replay.authority_ref,
        ),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({
            "material": material,
            "mechanical_packaging_only": True,
            "no_semantic_widening": True,
        }),
        replay_protocol_ref=q86.REPLAY_PROTOCOL_REF,
    )


def _q86ab_state_pairs_path() -> Path:
    return _repo_root() / _Q86AB_STATE_PAIRS_RELATIVE


def _ffp014_respondent_local_id(country_native: str, respno: str) -> str:
    """Reproduce the accepted FFP014 carrier-native identity rule, not PRE553 identity."""
    try:
        country = int(country_native)
    except (TypeError, ValueError) as exc:
        raise Q2SameSourceMaterializationError("FFP014 COUNTRY identity is not exact integer text") from exc
    material = json.dumps(
        {
            "source_family": "Afrobarometer",
            "wave": "R5",
            "COUNTRY": country,
            "RESPNO": respno,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ) + "\n"
    return "sha256:" + _sha256(material.encode("utf-8"))


def _load_q86ab_state_pairs(
    q69b_transport: q69b.Q69BTransport,
) -> tuple[tuple[str, str, str], ...]:
    compressed = _q86ab_state_pairs_path().read_bytes()
    if len(compressed) != Q86AB_STATE_PAIRS_GZIP_BYTES or _sha256(compressed) != Q86AB_STATE_PAIRS_GZIP_SHA256:
        raise Q2SameSourceMaterializationError("Q86 accepted-path replay carrier gzip identity mismatch")
    raw = gzip.decompress(compressed)
    if len(raw) != Q86AB_STATE_PAIRS_RAW_BYTES or _sha256(raw) != Q86AB_STATE_PAIRS_RAW_SHA256:
        raise Q2SameSourceMaterializationError("Q86 accepted-path replay carrier semantic identity mismatch")
    if len(q69b_transport.rows) != q69b.SOURCE_ROWS or len(raw) != q69b.SOURCE_ROWS:
        raise Q2SameSourceMaterializationError("Q86 accepted-path source-row count mismatch")

    # Accepted FFP014/FFP017 row order is a replay coordinate, not respondent
    # identity: numeric COUNTRY then exact RESPNO.  Preserve that exact producer
    # order for Q86 event identity, while separately proving that the key set is
    # exactly the same source respondent set carried by accepted Q69B.
    q69b_keys = [row.respondent_key for row in q69b_transport.rows]
    if len(q69b_keys) != len(set(q69b_keys)):
        raise Q2SameSourceMaterializationError("Q69B accepted source respondent key collision")
    accepted_order_keys = sorted(
        q69b_keys,
        key=lambda key: (int(key.split("|", 1)[0]), key.split("|", 1)[1]),
    )
    if _sha256(canonical_json(accepted_order_keys).encode("utf-8")) != Q86AB_SOURCE_KEY_SEQUENCE_SHA256:
        raise Q2SameSourceMaterializationError("accepted Q86 carrier-order respondent-key identity mismatch")

    decoded: list[tuple[str, str, str]] = []
    width = len(_Q86_STATE_ORDER)
    for respondent_key, packed in zip(accepted_order_keys, raw):
        q86a_index, q86b_index = divmod(packed, width)
        if q86a_index >= width or q86b_index >= width:
            raise Q2SameSourceMaterializationError("Q86 accepted-path replay state byte outside frozen domain")
        decoded.append(
            (
                respondent_key,
                _Q86_STATE_ORDER[q86a_index],
                _Q86_STATE_ORDER[q86b_index],
            )
        )
    if len(decoded) != q69b.SOURCE_ROWS:
        raise Q2SameSourceMaterializationError("Q86 accepted-path replay cardinality drift")
    return tuple(decoded)


@lru_cache(maxsize=1)
def _rehydrate_accepted_q86_release():
    """Re-run the accepted claim-scoped Q86 producer and require exact accepted identities."""
    q69b_transport = q69b.load_q69b_transport()
    accepted_replay_rows = _load_q86ab_state_pairs(q69b_transport)

    source_rows = []
    exposure_counts = {"EXPOSED__PROVED": 0, "NONEXPOSURE__PROVED": 0}
    alpha_by_country: dict[str, str] = {}
    for accepted_row_ordinal, (respondent_key, q86a_code, q86b_code) in enumerate(
        accepted_replay_rows, 1
    ):
        country_native, respno = respondent_key.split("|", 1)
        country_alpha3 = respno[:3]
        if len(country_alpha3) != 3 or country_alpha3.upper() != country_alpha3:
            raise Q2SameSourceMaterializationError("FFP014 exact RESPNO country token is malformed")
        prior_alpha = alpha_by_country.setdefault(country_native, country_alpha3)
        if prior_alpha != country_alpha3:
            raise Q2SameSourceMaterializationError("FFP014 COUNTRY to exact RESPNO alpha token is non-functional")
        exposure_state = (
            "NONEXPOSURE__PROVED"
            if country_alpha3 in _Q86_NONEXPOSED_ALPHA3
            else "EXPOSED__PROVED"
        )
        exposure_counts[exposure_state] += 1
        source_rows.append(q86.R5Q86GovernedRow(
            row_ordinal=accepted_row_ordinal,
            country_native=country_native,
            respno=respno,
            country_alpha3=country_alpha3,
            q86a_raw_value=q86a_code,
            q86a_response_state=q86._STATE[q86a_code].response_state,
            q86a_exposure_state=exposure_state,
            q86b_raw_value=q86b_code,
            q86b_response_state=q86._STATE[q86b_code].response_state,
            q86b_exposure_state=exposure_state,
            respondent_local_id=_ffp014_respondent_local_id(country_native, respno),
        ))
    if exposure_counts != _EXPECTED_Q86_SOURCE_EXPOSURE_COUNTS:
        raise Q2SameSourceMaterializationError("FFP017 exact Q86 source exposure counts drift")

    same_source = load_same_source_transport()
    risk_members = []
    risk_local_id_pairs = []
    for row in same_source.rows:
        country_native, respno = row.respondent_key.split("|", 1)
        if row.country_alpha3 != respno[:3]:
            raise Q2SameSourceMaterializationError("Q2 risk-set alpha identity differs from accepted FFP014 rule")
        local_id = _ffp014_respondent_local_id(country_native, respno)
        risk_local_id_pairs.append([row.respondent_key, local_id])
        risk_members.append(q86.R5Q86RiskSetMember(
            country_native=country_native,
            respno=respno,
            respondent_local_id=local_id,
            country_alpha3=row.country_alpha3,
        ))
    # FFP014 explicitly declares row order non-identity.  Preserve its original
    # carrier-order checksum as provenance, but prove the exact COUNTRY|RESPNO
    # -> respondent_local_id mapping as an order-insensitive canonical set.
    risk_local_id_pairs = sorted(risk_local_id_pairs, key=lambda pair: pair[0])
    if _sha256(canonical_json(risk_local_id_pairs).encode("utf-8")) != FFP014_RISK_KEY_LOCAL_ID_PAIR_SET_SHA256:
        raise Q2SameSourceMaterializationError("FFP014 risk-set carrier-native identity set replay drift")

    inputs = q86.R5Q86ClaimScopedGovernedInputs(
        bindings=q86.FROZEN_BINDINGS,
        source_rows=tuple(source_rows),
        risk_set_members=tuple(risk_members),
        risk_set_member_set_sha256=FFP017_RISK_SET_SHA256,
    )
    release = q86.build_validated_claim_scoped_r5_q86_c11_release(inputs)
    if release.semantic_release_hash != Q86_ACCEPTED_RELEASE_SHA256:
        raise Q2SameSourceMaterializationError(
            "accepted Q86 producer path did not reproduce accepted release identity"
        )
    if release.replay_manifest.content_hash != Q86_ACCEPTED_REPLAY_MANIFEST_SHA256:
        raise Q2SameSourceMaterializationError(
            "accepted Q86 producer path did not reproduce accepted replay identity"
        )
    expected_source_artifact_ref = ExactRef(
        "SOURCE_ARTIFACT",
        q86.FROZEN_BINDINGS.source_artifact_id,
        q86.FROZEN_BINDINGS.source_sha256,
    )
    if release.source_artifact_ref != expected_source_artifact_ref:
        raise Q2SameSourceMaterializationError("accepted Q86 producer source artifact identity drift")
    return release


def _accepted_q86_objects(release):
    universe = tuple(obj for obj in release.public_objects if isinstance(obj, EmpiricalUniverse))
    respondents = tuple(obj for obj in release.internal_records if isinstance(obj, RespondentIdentity))
    questions = tuple(obj for obj in release.internal_records if isinstance(obj, QuestionVariableBinding))
    events = tuple(obj for obj in release.public_objects if isinstance(obj, RespondentEvent))
    routing = tuple(obj for obj in release.public_objects if isinstance(obj, RoutingEligibilityFact))
    authorities = tuple(obj for obj in release.public_objects if isinstance(obj, AuthoritySnapshot))
    if (
        len(universe) != 1
        or len(respondents) != MATERIALIZED_ROWS
        or len(questions) != 2
        or len(events) != MATERIALIZED_ROWS * 2
        or len(routing) != MATERIALIZED_ROWS * 2
    ):
        raise Q2SameSourceMaterializationError("accepted Q86 object graph cardinality drift")

    q86a_question = tuple(
        binding for binding in questions
        if exact_ref(binding.native_question_ref).key == q86.question_ref("Q86A").key
    )
    q86a_events = tuple(
        event for event in events
        if exact_ref(event.native_question_ref).key == q86.question_ref("Q86A").key
    )
    q86a_routing = tuple(
        fact for fact in routing
        if exact_ref(fact.question_or_target_ref).key == q86.question_ref("Q86A").key
    )
    if len(q86a_question) != 1 or len(q86a_events) != MATERIALIZED_ROWS or len(q86a_routing) != MATERIALIZED_ROWS:
        raise Q2SameSourceMaterializationError("accepted Q86A object selection drift")
    return universe[0], respondents, q86a_question[0], q86a_events, q86a_routing, authorities


def _assert_q86a_exact_current_identity(events, routing) -> None:
    _manifest, payloads = current_gt2._read_committed_transport()
    current_event_refs = set(current_gt2._decode_exact_ref_hashes("event_refs", payloads["event_refs"]))
    current_routing_refs = set(current_gt2._decode_exact_ref_hashes("routing_refs", payloads["routing_refs"]))
    event_refs = {event.ref for event in events}
    routing_refs = {fact.ref for fact in routing}
    if len(event_refs) != MATERIALIZED_ROWS or not event_refs.issubset(current_event_refs):
        raise Q2SameSourceMaterializationError("Q86A event identities differ from accepted GT2 payload")
    if len(routing_refs) != MATERIALIZED_ROWS or not routing_refs.issubset(current_routing_refs):
        raise Q2SameSourceMaterializationError("Q86A routing identities differ from accepted GT2 payload")


@lru_cache(maxsize=1)
def build_q69b_q86a_same_source_candidate() -> C11SourceReleaseCandidate:
    transport = load_same_source_transport()

    # Rehydrate and validate the already-current Q69B release before reusing any object.
    q69b_transport = q69b.load_q69b_transport()
    q69b_candidate = q69b._candidate_from_transport(q69b_transport)
    q69b_release = validate_c11_source_release(q69b_candidate)
    if q69b_release.semantic_release_hash != Q69B_CURRENT_RELEASE_SHA256:
        raise Q2SameSourceMaterializationError("Q69B predecessor release identity drift")
    if q69b_release.source_release_manifest_hash != Q69B_CURRENT_MANIFEST_SHA256:
        raise Q2SameSourceMaterializationError("Q69B predecessor manifest identity drift")

    # Rehydrate the actual accepted Q86 release through its accepted public producer path.
    # Exact release + replay equality is mandatory before any Q86A object may be reused.
    q86_release = _rehydrate_accepted_q86_release()
    (
        q86_universe,
        q86_respondents,
        q86a_question,
        q86a_events,
        q86a_routing,
        q86_authorities,
    ) = _accepted_q86_objects(q86_release)
    _assert_q86a_exact_current_identity(q86a_events, q86a_routing)

    q69b_universe = q69b_candidate.empirical_universes[0]
    if (
        q69b_universe.content_hash != q69b.ACCEPTED_UNIVERSE_SHA256
        or q86_universe.ref != q69b_universe.ref
    ):
        raise Q2SameSourceMaterializationError(
            "accepted Q69B and Q86 releases do not share exact empirical-universe identity"
        )

    rows_by_key = {row.respondent_key: row for row in transport.rows}
    selected_keys = set(rows_by_key)
    q69b_respondent_by_key = {
        respondent.respondent_key: respondent
        for respondent in q69b_candidate.respondent_identities
        if respondent.respondent_key in selected_keys
    }
    q86_respondent_by_key = {respondent.respondent_key: respondent for respondent in q86_respondents}
    if len(q69b_respondent_by_key) != MATERIALIZED_ROWS or len(q86_respondent_by_key) != MATERIALIZED_ROWS:
        raise Q2SameSourceMaterializationError("Q2 respondent subset cardinality drift")

    respondents = []
    for key, row in rows_by_key.items():
        q69b_respondent = q69b_respondent_by_key.get(key)
        q86_respondent = q86_respondent_by_key.get(key)
        if q69b_respondent is None or q86_respondent is None:
            raise Q2SameSourceMaterializationError("Q2 respondent absent from accepted predecessor")
        if (
            q69b_respondent.ref != q86_respondent.ref
            or q86_respondent.content_hash != row.pre553_respondent_content_hash
        ):
            raise Q2SameSourceMaterializationError(
                "accepted Q69B/Q86 PRE553 respondent identities are not exactly co-resident"
            )
        respondents.append(q86_respondent)

    selected_ref_keys = {respondent.ref.key for respondent in respondents}
    q69b_events = tuple(
        event for event in q69b_candidate.respondent_events
        if exact_ref(event.scoped_respondent_ref).key in selected_ref_keys
    )
    q69b_routing = tuple(
        fact for fact in q69b_candidate.routing_eligibility_facts_or_exact_rules
        if exact_ref(fact.scoped_respondent_ref).key in selected_ref_keys
    )
    q69b_coordinates = tuple(
        fact for fact in q69b_candidate.empirical_coordinate_facts
        if exact_ref(fact.scoped_respondent_ref).key in selected_ref_keys
    )
    if not (
        len(q69b_events)
        == len(q69b_routing)
        == len(q69b_coordinates)
        == MATERIALIZED_ROWS
    ):
        raise Q2SameSourceMaterializationError("Q69B exact subset materialization drift")

    q86_auth_by_id = {authority.authority_id: authority for authority in q86_authorities}
    required_q86_authority_ids = (
        "GT12-A-R5-Q86-SOURCE-SEMANTICS",
        "GT12-A-R5-Q86-COMMON-RISK-ROUTING",
        "GT12-A-R5-Q86-CARRIER-REEXPRESSION",
        "GT12-A-R5-Q86-C11-REPLAY",
    )
    try:
        q86_source_auth, q86_routing_auth, q86_projection_auth, q86_replay_auth = (
            q86_auth_by_id[authority_id] for authority_id in required_q86_authority_ids
        )
    except KeyError as exc:
        raise Q2SameSourceMaterializationError("accepted Q86 required authority object missing") from exc

    q69b_replay_auth = next(
        authority for authority in q69b_candidate.authority_snapshots
        if authority.authority_id == "GT34-N2-R5-Q69B-C11-REPLAY"
    )
    q2_replay_auth = _q2_replay_authority(q69b_replay_auth, q86_replay_auth)

    authority_by_key = {
        authority.authority_ref.key: authority
        for authority in (
            *q69b_candidate.authority_snapshots,
            q86_source_auth,
            q86_routing_auth,
            q86_projection_auth,
            q86_replay_auth,
            q2_replay_auth,
        )
    }
    authorities = tuple(sorted(authority_by_key.values(), key=lambda authority: authority.authority_ref.key))

    candidate = C11SourceReleaseCandidate(
        source_release_manifest=SourceReleaseManifest(
            source_artifact_id=q69b.SOURCE_ARTIFACT_ID,
            source_artifact_content_hash=q69b.SOURCE_SHA256,
            source_family_id="Afrobarometer",
            study_product_id="Afrobarometer",
            release_id=CANDIDATE_RELEASE_ID,
            instrument_release_id=f"merged_r5_codebook_2.pdf@sha256:{q69b.CODEBOOK_SHA256}",
            ingest_contract_version=INGEST_CONTRACT_VERSION,
            declared_universe_refs=(q86_universe.ref,),
            declared_authority_snapshot_refs=tuple(authority.authority_ref for authority in authorities),
            declared_record_counts_by_logical_family={},
            source_snapshot_retention_ref=q69b.SOURCE_REF,
        ),
        empirical_universes=(q86_universe,),
        respondent_identities=tuple(sorted(respondents, key=lambda respondent: respondent.ref.key)),
        question_variable_bindings=tuple(sorted(
            (*q69b_candidate.question_variable_bindings, q86a_question),
            key=lambda binding: binding.ref.key,
        )),
        respondent_events=tuple(sorted((*q69b_events, *q86a_events), key=lambda event: event.ref.key)),
        routing_eligibility_facts_or_exact_rules=tuple(sorted(
            (*q69b_routing, *q86a_routing), key=lambda fact: fact.ref.key
        )),
        empirical_coordinate_facts=tuple(sorted(q69b_coordinates, key=lambda fact: fact.ref.key)),
        weight_measure_facts_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        authority_snapshots=authorities,
        source_universe_relations_or_explicit_distinct_default=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay_bindings_when_retained_objects_require_them=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
        discovery_branch_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
        structural_admission_replay_bindings_or_typed_not_applicable_state=TypedAbsence("NOT_APPLICABLE"),
        candidate_replay_manifest=None,
    )
    counts = dict(record_counts_for_candidate(candidate))
    manifest = replace(
        candidate.source_release_manifest,
        declared_record_counts_by_logical_family={
            name: counts[name]
            for name in (
                "EmpiricalUniverse",
                "RespondentIdentity",
                "QuestionVariableBinding",
                "RespondentEvent",
                "RoutingEligibilityFact",
                "EmpiricalCoordinateFact",
                "AuthoritySnapshot",
            )
        },
    )
    candidate = replace(candidate, source_release_manifest=manifest)
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=q2_replay_auth.authority_ref,
        deterministic_tie_order_rules_ref=q86.TIE_ORDER_REF,
        replay_protocol_version="1.0.0",
    )
    return replace(candidate, candidate_replay_manifest=replay)


def build_validated_q69b_q86a_same_source_release():
    candidate = build_q69b_q86a_same_source_candidate()
    release = validate_c11_source_release(candidate)
    if release.release_id != CANDIDATE_RELEASE_ID:
        raise Q2SameSourceMaterializationError("Q2 release ID drift")
    if release.source_artifact_ref.content_hash != q69b.SOURCE_SHA256:
        raise Q2SameSourceMaterializationError("Q2 source identity drift after validation")
    return release


def identity_report() -> Mapping[str, Any]:
    candidate = build_q69b_q86a_same_source_candidate()
    release = validate_c11_source_release(candidate)
    q86a_event_refs = tuple(
        event.ref for event in candidate.respondent_events
        if exact_ref(event.native_question_ref).key == q86.question_ref("Q86A").key
    )
    q86a_routing_refs = tuple(
        fact.ref for fact in candidate.routing_eligibility_facts_or_exact_rules
        if exact_ref(fact.question_or_target_ref).key == q86.question_ref("Q86A").key
    )
    return {
        "contract": CONTRACT_ID,
        "release_id": release.release_id,
        "release_semantic_sha256": release.semantic_release_hash,
        "release_manifest_sha256": release.source_release_manifest_hash,
        "replay_manifest_sha256": release.replay_manifest.content_hash,
        "source_sha256": release.source_artifact_ref.content_hash,
        "transport_semantic_sha256": TRANSPORT_SEMANTIC_SHA256,
        "transport_gzip_sha256": TRANSPORT_GZIP_SHA256,
        "rows": MATERIALIZED_ROWS,
        "respondents": len(candidate.respondent_identities),
        "questions": len(candidate.question_variable_bindings),
        "events": len(candidate.respondent_events),
        "routing": len(candidate.routing_eligibility_facts_or_exact_rules),
        "coordinates": len(candidate.empirical_coordinate_facts),
        "q86a_exact_current_event_refs": len(q86a_event_refs),
        "q86a_exact_current_routing_refs": len(q86a_routing_refs),
        "q69b_predecessor_release_sha256": Q69B_CURRENT_RELEASE_SHA256,
        "q86_predecessor_release_sha256": q69b.PREDECESSOR_RELEASE_SHA256,
        "q86_predecessor_replay_manifest_sha256": Q86_ACCEPTED_REPLAY_MANIFEST_SHA256,
        "q86_accepted_path_rehydrated_release_sha256": Q86_ACCEPTED_RELEASE_SHA256,
        "q86_accepted_path_rehydrated_replay_sha256": Q86_ACCEPTED_REPLAY_MANIFEST_SHA256,
        "q86ab_source_key_sequence_sha256": Q86AB_SOURCE_KEY_SEQUENCE_SHA256,
        "q86ab_state_pairs_raw_sha256": Q86AB_STATE_PAIRS_RAW_SHA256,
        "q86ab_state_pairs_gzip_sha256": Q86AB_STATE_PAIRS_GZIP_SHA256,
        "ffp014_risk_key_local_id_pairs_carrier_order_sha256": FFP014_RISK_KEY_LOCAL_ID_PAIRS_CARRIER_ORDER_SHA256,
        "ffp014_risk_key_local_id_pair_set_sha256": FFP014_RISK_KEY_LOCAL_ID_PAIR_SET_SHA256,
        "q86a_identity_reuse_mode": "ACTUAL_ACCEPTED_CLAIM_SCOPED_Q86_OBJECTS__NO_INDEPENDENT_EVENT_OR_ROUTING_RECONSTRUCTION",
        "q86a_exact_identity_reuse_proved": True,
        "predecessors_mutated": False,
        "semantic_owner_transfer": False,
        "portability": "NONE",
        "pooling": "NONE",
        "comparator": "NOT_CREATED",
        "psepf": "NOT_CREATED",
        "positive_v3": False,
    }


__all__ = [
    "CONTRACT_ID",
    "CANDIDATE_RELEASE_ID",
    "TRANSPORT_SCHEMA",
    "TRANSPORT_SEMANTIC_SHA256",
    "TRANSPORT_GZIP_SHA256",
    "Q2SameSourceMaterializationError",
    "load_same_source_transport",
    "build_q69b_q86a_same_source_candidate",
    "build_validated_q69b_q86a_same_source_release",
    "identity_report",
]
