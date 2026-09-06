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
import gzip
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Final, Mapping

from rawlsing_next.pre553_c11_ingest import (
    C11SourceReleaseCandidate,
    INGEST_CONTRACT_VERSION,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    record_counts_for_candidate,
    validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    RoutingEligibilityFact,
    canonical_json,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    OccurrenceRule,
    PhysicalSlot,
    ResponseSlotRule,
    ResponseValueRule,
    _event,
    physical_value_binding_key,
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

_TRANSPORT_RELATIVE: Final[Path] = Path(
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "GT3_GT4_POST_P_FANIN_REPAIR_WAVE_R1/"
    "Q2_Q69B_Q86A_SAME_SOURCE_MATERIALIZATION_R1/transport/"
    "q69b_q86a_same_source_transport.json.gz"
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


def _exact_q86a_question_binding(universe_ref: ExactRef, source_auth: AuthoritySnapshot) -> QuestionVariableBinding:
    return QuestionVariableBinding(
        empirical_universe_ref=universe_ref,
        native_question_ref=q86.question_ref("Q86A"),
        instrument_question_version="Afrobarometer_R5",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref,
    )


def _exact_q86a_event(
    row: SameSourceRow,
    respondent,
    question: QuestionVariableBinding,
    source_auth: AuthoritySnapshot,
    projection_auth: AuthoritySnapshot,
):
    state = q86._STATE[row.q86a_native_code]
    topology_ref = q86._ref(
        "RESPONSE_TOPOLOGY",
        "Afrobarometer:R5:Q86A:SCALAR_SINGULAR",
        {"variable": "Q86A", "kind": "SCALAR_SINGULAR", "numeric_order_authorized": False},
    )
    occurrence = OccurrenceRule(
        "0",
        topology_ref,
        {"kind": "SCALAR_SINGULAR", "index": 0},
    )
    declaration = q86._declaration(
        "Q86A", state.response_state, q86.FROZEN_BINDINGS.response_fact_carrier_sha256
    )
    value = ResponseValueRule(
        physical_value_binding_key(
            row.q86a_native_code,
            PhysicalMissingState.OBSERVED_STORAGE_VALUE,
            declaration,
        ),
        state.response_state,
        (occurrence,),
        None,
        None,
        (),
    )
    slot = ResponseSlotRule(PhysicalSlot(1, "Q86A"), question, (value,))
    cell = PhysicalCell(
        row.source_row_ordinal,
        1,
        "Q86A",
        row.q86a_native_code,
        PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        declaration,
        state.label,
    )
    projection = SimpleNamespace(
        projection_identity_ref=q86.projection_identity_ref(q86.FROZEN_BINDINGS),
        projection_authority_ref=projection_auth.authority_ref,
    )
    return _event(
        q69b.SOURCE_SHA256,
        row.source_row_ordinal,
        respondent,
        slot,
        cell,
        value,
        occurrence,
        projection,
    )


def _exact_q86a_routing(
    row: SameSourceRow,
    respondent,
    routing_auth: AuthoritySnapshot,
) -> RoutingEligibilityFact:
    b = q86.FROZEN_BINDINGS
    exposure_predicate = q86.exposure_predicate_ref("Q86A")
    routing_rule = q86._ref(
        "ROUTING_RULE",
        "GT12:R5:Q86:COMMON_COEXPOSURE_MEMBERSHIP",
        {
            "risk": b.risk_ref.as_dict(),
            "countries": q86.COMMON_RISK_COUNTRIES,
            "q86a": q86.exposure_predicate_ref("Q86A").as_dict(),
            "q86b": q86.exposure_predicate_ref("Q86B").as_dict(),
            "response_presence_is_exposure_evidence": False,
        },
    )
    member_replay = q86._ref(
        "MEMBER_SET_REPLAY",
        f"{b.risk_set_id}:REPLAY",
        {
            "risk": b.risk_ref.as_dict(),
            "member_hash": b.risk_set_member_set_sha256,
            "countries": q86.COMMON_RISK_COUNTRIES,
        },
    )
    state = "ELIGIBLE_APPLICABLE"
    return RoutingEligibilityFact(
        typed_state=state,
        authority_snapshot_refs=(routing_auth.authority_ref,),
        dependency_refs=(respondent.ref, b.risk_ref, b.exposure_ref, exposure_predicate),
        producer_replay_locator_or_reference_root=q86._ref(
            "REPLAY_ROOT",
            f"GT12:R5:Q86A:ROUTING:{row.respondent_key}",
            {
                "respondent": respondent.ref.as_dict(),
                "risk": b.risk_ref.as_dict(),
                "predicate": exposure_predicate.as_dict(),
                "state": state,
            },
        ),
        empirical_universe_ref=respondent.empirical_universe_ref,
        scoped_respondent_ref=respondent.ref,
        question_or_target_ref=q86.question_ref("Q86A"),
        risk_set_ref=b.risk_ref,
        routing_rule_ref=routing_rule,
        applicability_state=state,
        routing_state=state,
        parent_predicate_refs=(exposure_predicate,),
        member_set_replay_ref=member_replay,
    )


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

    rows_by_key = {row.respondent_key: row for row in transport.rows}
    selected_keys = set(rows_by_key)
    respondents = tuple(
        respondent
        for respondent in q69b_candidate.respondent_identities
        if respondent.respondent_key in selected_keys
    )
    if len(respondents) != MATERIALIZED_ROWS:
        raise Q2SameSourceMaterializationError("Q2 respondent subset cardinality drift")
    respondent_by_key = {respondent.respondent_key: respondent for respondent in respondents}
    for key, row in rows_by_key.items():
        respondent = respondent_by_key.get(key)
        if respondent is None or respondent.content_hash != row.pre553_respondent_content_hash:
            raise Q2SameSourceMaterializationError("Q2 respondent exact identity bridge drift")

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

    q86_source_auth, q86_routing_auth, _q86_coord_auth, q86_projection_auth, q86_replay_auth, _q86_permission_auth = (
        q86._authorities(q86.FROZEN_BINDINGS)
    )
    universe = q69b_candidate.empirical_universes[0]
    if universe.content_hash != q69b.ACCEPTED_UNIVERSE_SHA256:
        raise Q2SameSourceMaterializationError("shared empirical universe identity drift")

    q86a_question = _exact_q86a_question_binding(universe.ref, q86_source_auth)
    q86a_events = tuple(
        _exact_q86a_event(row, respondent_by_key[row.respondent_key], q86a_question, q86_source_auth, q86_projection_auth)
        for row in transport.rows
    )
    q86a_routing = tuple(
        _exact_q86a_routing(row, respondent_by_key[row.respondent_key], q86_routing_auth)
        for row in transport.rows
    )
    _assert_q86a_exact_current_identity(q86a_events, q86a_routing)

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
            declared_universe_refs=(universe.ref,),
            declared_authority_snapshot_refs=tuple(authority.authority_ref for authority in authorities),
            declared_record_counts_by_logical_family={},
            source_snapshot_retention_ref=q69b.SOURCE_REF,
        ),
        empirical_universes=(universe,),
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
