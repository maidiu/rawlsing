"""Exact Afrobarometer R5 Q86A/Q86B -> PRE553 C11 binding for GT1/GT2.

Bounded adapter only: no source acquisition, I03 execution, generic survey
compiler, value harmonization, weights, or inference from labels/frequencies.
Numeric source codes are identities only, never order/metric authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot, EmpiricalUniverse, ExactRef, RoutingEligibilityFact, semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule, ExactPhysicalCellStream, GovernedC11Projection, OccurrenceRule,
    PhysicalSlot, ResponseSlotRule, ResponseValueRule, RowRespondentBinding,
    build_validated_source_backed_c11_release_from_stream, physical_value_binding_key,
)

CONTRACT_ID = "GT12_A_R5_Q86_GOVERNED_C11_PROJECTION@1.0.0"
FROZEN_CANARY_COMMIT = "a9416094cbb4653dd2de2e4aa7b67577a355560c"
PROGRAM_COMMIT = "17b9abc5c8c3038d14670c6e68136bb868f5073a"


class R5Q86ProjectionError(ValueError):
    pass


def _text(v: Any, name: str) -> str:
    if not isinstance(v, str) or not v.strip():
        raise R5Q86ProjectionError(f"{name} must be non-empty text")
    return v.strip()


def _sha(v: Any, name: str) -> str:
    if not isinstance(v, str) or len(v) != 64 or v.lower() != v or any(c not in "0123456789abcdef" for c in v):
        raise R5Q86ProjectionError(f"{name} must be lowercase sha256")
    return v


def _ref(kind: str, object_id: str, material: Any) -> ExactRef:
    digest = material if isinstance(material, str) and len(material) == 64 else semantic_hash(material)
    return ExactRef(kind, object_id, _sha(digest, f"{kind}.content_hash"))


@dataclass(frozen=True)
class NativeState:
    code: str
    label: str
    response_state: str


# Codebook presentation order only. No numeric/ordinal meaning is granted.
Q86_NATIVE_STATES = (
    NativeState("0", "No", "SUBSTANTIVE_RESPONSE"),
    NativeState("1", "Yes", "SUBSTANTIVE_RESPONSE"),
    NativeState("9", "Don't know", "DK"),
    NativeState("997", "Not asked", "NOT_ASKED"),
    NativeState("998", "Refused to answer", "REFUSAL"),
    NativeState("-1", "Missing", "MISSING"),
)
_STATE = {x.code: x for x in Q86_NATIVE_STATES}
Q86 = {
    "Q86A": {
        "qimpl": "question_impl.phase0.67f036c0efb7fb98ff4a",
        "identity_sha256": "67f036c0efb7fb98ff4a93dc811bf59cfc095608eda374f6534b006a62241bd3",
        "predicate_id": "C04P.9c3bd54f111f068a22f8",
        "predicate": "COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}",
        "evidence": "SEP.U1.NATIVE.9c63ebbd5ad1126a9d88ba07",
    },
    "Q86B": {
        "qimpl": "question_impl.phase0.2fb3a62609dad4c1306d",
        "identity_sha256": "2fb3a62609dad4c1306d8cfa14f997eab4d6e65ada56083279386a202544a506",
        "predicate_id": "C04P.34fb5970fdb1af3cbaec",
        "predicate": "COUNTRY_ALPHA3 NOT IN {ALG,EGY,MRC,SUD,TUN}",
        "evidence": "SEP.U1.NATIVE.b67bc175b86139b78d81f118",
    },
}


@dataclass(frozen=True)
class R5Q86CarrierBindings:
    source_artifact_id: str
    source_sha256: str
    source_row_count: int
    respondent_carrier_id: str
    respondent_carrier_sha256: str
    response_fact_carrier_sha256: str
    exposure_fact_carrier_sha256: str
    risk_set_id: str
    risk_set_row_count: int
    risk_set_member_set_sha256: str
    source_structure_id: str
    source_structure_sha256: str
    codebook_sha256: str

    def __post_init__(self):
        for name in ("source_artifact_id", "respondent_carrier_id", "risk_set_id", "source_structure_id"):
            _text(getattr(self, name), name)
        for name in ("source_sha256", "respondent_carrier_sha256", "response_fact_carrier_sha256",
                     "exposure_fact_carrier_sha256", "risk_set_member_set_sha256",
                     "source_structure_sha256", "codebook_sha256"):
            _sha(getattr(self, name), name)
        if not isinstance(self.source_row_count, int) or isinstance(self.source_row_count, bool) or self.source_row_count < 1:
            raise R5Q86ProjectionError("source_row_count must be positive integer")
        if not isinstance(self.risk_set_row_count, int) or isinstance(self.risk_set_row_count, bool) or not 0 < self.risk_set_row_count <= self.source_row_count:
            raise R5Q86ProjectionError("risk_set_row_count invalid")

    @property
    def source_ref(self): return ExactRef("SOURCE_SNAPSHOT", self.source_artifact_id, self.source_sha256)
    @property
    def respondent_ref(self): return ExactRef("RESPONDENT_CARRIER", self.respondent_carrier_id, self.respondent_carrier_sha256)
    @property
    def response_ref(self): return ExactRef("RESPONSE_FACT_CARRIER", "FFP017_SELECTED_RESPONSE_FACTS", self.response_fact_carrier_sha256)
    @property
    def exposure_ref(self): return ExactRef("EXPOSURE_FACT_CARRIER", "FFP017_SELECTED_EXPOSURE_FACTS", self.exposure_fact_carrier_sha256)
    @property
    def risk_ref(self): return ExactRef("RISK_SET", self.risk_set_id, self.risk_set_member_set_sha256)
    @property
    def structure_ref(self): return ExactRef("CURRENT_SOURCE_STRUCTURE", self.source_structure_id, self.source_structure_sha256)


FROZEN_BINDINGS = R5Q86CarrierBindings(
    "Data/Afro Barometer Round 5.sav",
    "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651", 51_587,
    "FFP014_R5_CURRENT_RESPONDENT_CARRIER@1",
    "6c2277e8832c8f070d1213f8f68adf54f115e4978f59702d150ab69fffd4a6d5",
    "98526cf33e5344c6e2d5c6ad4b16826ee678b4648be2ada395e4f3ce70fe1709",
    "0920c350aeb900b5922cf3872f86609de6a8cebb8d3991680dc9ee40e85b06ce",
    "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1", 19_210,
    "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b",
    "cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4",
    "ea9614b69e63a8e5bc87e65c944d67445082639fe45262da626bd6aa1a4d9e99",
    "7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735",
)

# FFP017 proved this declared country scope equals the 12-item common-coexposure
# membership for every admitted R5 respondent.
COMMON_RISK_COUNTRIES = ("BFO", "BOT", "CVE", "KEN", "LES", "MAU", "MLW", "MOZ", "NAM", "SAF", "UGA")
CURRENTNESS_REF = _ref("FROZEN_CANARY_CURRENTNESS", f"GT1_GT2_FROZEN_CANARY_CONTRACT_R1@{FROZEN_CANARY_COMMIT}", {
    "commit": FROZEN_CANARY_COMMIT, "program": PROGRAM_COMMIT,
    "state": "FROZEN_FOR_BOUNDED_IMPLEMENTATION__NO_SEMANTIC_WIDENING",
})
GT1_TARGET_USE_REF = _ref("TARGET_USE", "GT1_POSITIVE_EMPIRICAL_FACT_ONLY__NO_STRUCTURAL_OR_ACTOR_PROMOTION", {
    "target_use": "GT1_POSITIVE_EMPIRICAL_FACT_ONLY__NO_STRUCTURAL_OR_ACTOR_PROMOTION"
})
GT2_TARGET_USE_REF = _ref("TARGET_USE", "GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1", {
    "operation": "GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1",
    "ceiling": "EMPIRICAL_INPUT_TO_FROZEN_EXACT_CONDITIONAL_SUPPORT_ONLY__NO_CAUSAL_OR_ACTOR_PROMOTION",
})
REPLAY_PROTOCOL_REF = _ref("REPLAY_PROTOCOL_SPEC", "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0__GT12_R5_Q86", {
    "facade": "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0", "order": "CANONICAL_REF_SORT",
    "currentness": CURRENTNESS_REF.as_dict(),
})
TIE_ORDER_REF = _ref("ORDER_RULE", "GT12_R5_Q86_CANONICAL_REF_SORT", {
    "rule": "CANONICAL_REF_SORT", "numeric_source_codes_are_order_authority": False,
})
COUNTRY_REF = _ref("COORDINATE_NATIVE", "FFP014_R5_CURRENT_RESPONDENT_CARRIER@1:COUNTRY_ALPHA3", {
    "carrier": FROZEN_BINDINGS.respondent_ref.as_dict(), "field": "COUNTRY_ALPHA3",
    "role": "ROUTING_SOURCE_IDENTITY_ONLY",
})
COUNTRY_UNIT_REF = _ref("UNIT_TAXONOMY", "SOURCE_NATIVE_COUNTRY_ALPHA3_IDENTITY", {
    "field": "COUNTRY_ALPHA3", "role": "SOURCE_NATIVE_IDENTITY_ONLY"
})


def question_ref(variable: str) -> ExactRef:
    try: q = Q86[variable]
    except KeyError as exc: raise R5Q86ProjectionError("only Q86A/Q86B are frozen") from exc
    return ExactRef("QUESTION_IMPLEMENTATION", q["qimpl"], q["identity_sha256"])


def exposure_predicate_ref(variable: str) -> ExactRef:
    q = Q86[variable]
    return _ref("C04_EXPOSURE_PREDICATE_PIN", q["predicate_id"], {
        "variable": variable, "qimpl": q["qimpl"], "predicate": q["predicate"], "evidence": q["evidence"]
    })


def domain_ref(variable: str) -> ExactRef:
    if variable not in Q86: raise R5Q86ProjectionError("only Q86A/Q86B are frozen")
    states = sorted(({"code": x.code, "label": x.label, "response_state": x.response_state} for x in Q86_NATIVE_STATES), key=lambda x: x["code"])
    return _ref("SOURCE_NATIVE_DOMAIN", f"Afrobarometer:R5:{variable}:SOURCE_NATIVE_DOMAIN", {
        "variable": variable, "states": states, "codebook_sha256": FROZEN_BINDINGS.codebook_sha256,
        "page": 53, "numeric_codes_are_identity_only": True,
    })


def target_domain_replay_ref(variable: str) -> ExactRef:
    return _ref("TARGET_DOMAIN_REPLAY", f"Afrobarometer:R5:{variable}:TARGET_DOMAIN_REPLAY", {
        "domain": domain_ref(variable).as_dict(), "serialization": [x.code for x in Q86_NATIVE_STATES],
        "serialization_is_not_order_authority": True,
    })


def q86_target_domain(variable: str) -> tuple[Mapping[str, str], ...]:
    if variable not in Q86: raise R5Q86ProjectionError("only Q86A/Q86B are frozen")
    return tuple({"code": x.code, "label": x.label, "response_state": x.response_state} for x in Q86_NATIVE_STATES)


@dataclass(frozen=True)
class R5Q86GovernedRow:
    row_ordinal: int
    country_native: str
    respno: str
    country_alpha3: str
    q86a_raw_value: str | int
    q86a_response_state: str
    q86a_exposure_state: str
    q86b_raw_value: str | int
    q86b_response_state: str
    q86b_exposure_state: str
    respondent_local_id: str | None = None

    def __post_init__(self):
        if not isinstance(self.row_ordinal, int) or isinstance(self.row_ordinal, bool) or self.row_ordinal < 1:
            raise R5Q86ProjectionError("row_ordinal must be positive integer")
        for name in ("country_native", "respno", "country_alpha3", "q86a_response_state",
                     "q86a_exposure_state", "q86b_response_state", "q86b_exposure_state"):
            _text(getattr(self, name), name)
        _native(self.q86a_raw_value, self.q86a_response_state, "Q86A")
        _native(self.q86b_raw_value, self.q86b_response_state, "Q86B")
        if self.respondent_local_id is not None:
            value = _text(self.respondent_local_id, "respondent_local_id")
            if not value.startswith("sha256:"):
                raise R5Q86ProjectionError("respondent_local_id must be sha256-prefixed")
            _sha(value.split(":", 1)[1], "respondent_local_id")

    @property
    def respondent_key(self): return f"{self.country_native}|{self.respno}"
    @property
    def in_common_risk_set(self): return self.country_alpha3 in COMMON_RISK_COUNTRIES


@dataclass(frozen=True)
class R5Q86GovernedInputs:
    bindings: R5Q86CarrierBindings
    rows: tuple[R5Q86GovernedRow, ...]


@dataclass(frozen=True)
class R5Q86RiskSetMember:
    country_native: str
    respno: str
    respondent_local_id: str
    country_alpha3: str

    def __post_init__(self):
        for name in ("country_native", "respno", "respondent_local_id", "country_alpha3"):
            _text(getattr(self, name), name)
        if not self.respondent_local_id.startswith("sha256:"):
            raise R5Q86ProjectionError("risk-set respondent_local_id must be sha256-prefixed")
        _sha(self.respondent_local_id.split(":", 1)[1], "risk-set respondent_local_id")

    @property
    def respondent_key(self): return f"{self.country_native}|{self.respno}"


@dataclass(frozen=True)
class R5Q86ClaimScopedGovernedInputs:
    bindings: R5Q86CarrierBindings
    source_rows: tuple[R5Q86GovernedRow, ...]
    risk_set_members: tuple[R5Q86RiskSetMember, ...]
    risk_set_member_set_sha256: str

    def __post_init__(self):
        _sha(self.risk_set_member_set_sha256, "risk_set_member_set_sha256")


@dataclass(frozen=True)
class R5Q86ProjectionPackage:
    stream: ExactPhysicalCellStream
    projection: GovernedC11Projection
    authority_registry: AuthorityRegistry
    q86a_question_ref: ExactRef
    q86b_question_ref: ExactRef
    q86a_domain_ref: ExactRef
    q86b_domain_ref: ExactRef
    q86a_target_domain_replay_ref: ExactRef
    q86b_target_domain_replay_ref: ExactRef
    risk_set_ref: ExactRef
    currentness_ref: ExactRef
    gt1_target_use_ref: ExactRef
    gt2_target_use_ref: ExactRef


def validate_frozen_bindings(bindings: R5Q86CarrierBindings) -> R5Q86CarrierBindings:
    if not isinstance(bindings, R5Q86CarrierBindings) or bindings != FROZEN_BINDINGS:
        raise R5Q86ProjectionError("R5 Q86 source/carrier/risk-set binding differs from frozen contract")
    return bindings


def _native(value: str | int, state: str, variable: str) -> str:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise R5Q86ProjectionError(f"{variable} native code must be exact string/integer")
    token = str(value).strip()
    if token not in _STATE:
        raise R5Q86ProjectionError(f"{variable} code {token!r} outside frozen source-native domain")
    if state != _STATE[token].response_state:
        raise R5Q86ProjectionError(f"{variable} response state does not match frozen code {token!r}")
    return token


def _declaration(variable: str, state: str, response_sha: str) -> Mapping[str, Any]:
    return {"kind": "GOVERNED_CURRENT_RESPONSE_STATE", "variable": variable, "response_state": state,
            "carrier_sha256": response_sha}


def _auth(authority_id: str, kind: str, operations: Iterable[str], families: Iterable[str],
          scope: Mapping[str, Any], deps: Iterable[ExactRef]) -> AuthoritySnapshot:
    deps = tuple(sorted(set(deps), key=lambda r: r.key)); operations = tuple(sorted(set(operations))); families = tuple(sorted(set(families)))
    material = {"contract": CONTRACT_ID, "id": authority_id, "kind": kind, "operations": operations,
                "families": families, "scope": scope, "deps": [x.as_dict() for x in deps],
                "currentness": CURRENTNESS_REF.as_dict()}
    return AuthoritySnapshot(
        typed_state="ALLOW", authority_snapshot_refs=(), dependency_refs=deps,
        producer_replay_locator_or_reference_root=_ref("AUTHORITY_REPLAY_ROOT", f"{authority_id}:replay", material),
        authority_id=authority_id, authority_version="1.0.0", authority_content_hash=semantic_hash(material),
        authority_kind=kind, decision_state="ALLOW", governed_operations=operations,
        governed_object_families=families, scope_envelope=scope,
        effective_time_or_interval="GT12_FROZEN_CANARY_CURRENTNESS", parent_authority_refs=(),
        negative_limit_refs=(), supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({"material": material, "no_widening": True}),
        replay_protocol_ref=REPLAY_PROTOCOL_REF,
    )


def _authorities(b: R5Q86CarrierBindings):
    qa, qb = question_ref("Q86A"), question_ref("Q86B")
    source = _auth("GT12-A-R5-Q86-SOURCE-SEMANTICS", "SOURCE_SEMANTICS_TOPOLOGY",
        ("R5_Q86A_Q86B_NATIVE_RESPONSE_SEMANTICS",), ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
        {"source": b.source_ref, "structure": b.structure_ref, "questions": (qa, qb),
         "domains": (domain_ref("Q86A"), domain_ref("Q86B")), "currentness": CURRENTNESS_REF},
        (b.source_ref, b.response_ref, b.structure_ref, qa, qb, domain_ref("Q86A"), domain_ref("Q86B"), CURRENTNESS_REF))
    routing = _auth("GT12-A-R5-Q86-COMMON-RISK-ROUTING", "ROUTING_RISK_SET",
        ("R5_Q86A_Q86B_EXACT_COMMON_COEXPOSURE_ROUTING",), ("RoutingEligibilityFact@1.0.0",),
        {"predicate_or_risk_set_refs": (b.risk_ref,), "questions": (qa, qb),
         "exposure_predicates": (exposure_predicate_ref("Q86A"), exposure_predicate_ref("Q86B")),
         "exposure_carrier": b.exposure_ref, "countries": COMMON_RISK_COUNTRIES, "currentness": CURRENTNESS_REF},
        (b.risk_ref, b.exposure_ref, exposure_predicate_ref("Q86A"), exposure_predicate_ref("Q86B"), CURRENTNESS_REF))
    coordinate = _auth("GT12-A-R5-COUNTRY-ALPHA3", "COORDINATE_SEMANTICS",
        ("R5_COUNTRY_ALPHA3_SOURCE_NATIVE_ROUTING_IDENTITY",), ("EmpiricalCoordinateFact@1.0.0",),
        {"coordinate": COUNTRY_REF, "carrier": b.respondent_ref, "use": "ROUTING_SOURCE_IDENTITY_ONLY", "currentness": CURRENTNESS_REF},
        (b.respondent_ref, CURRENTNESS_REF))
    projection = _auth("GT12-A-R5-Q86-CARRIER-REEXPRESSION", "SOURCE_SEMANTICS_TOPOLOGY",
        ("R5_Q86A_Q86B_GOVERNED_CURRENT_CARRIER_REEXPRESSION_ONLY",),
        ("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0"),
        {"source": b.source_ref, "carriers": (b.respondent_ref, b.response_ref), "questions": (qa, qb),
         "semantic_owner_transfer": False, "currentness": CURRENTNESS_REF},
        (b.source_ref, b.respondent_ref, b.response_ref, CURRENTNESS_REF))
    replay = _auth("GT12-A-R5-Q86-C11-REPLAY", "REPLAY_PROTOCOL",
        ("R5_Q86A_Q86B_C11_DETERMINISTIC_REPLAY",), ("ReplayReceipt@1.0.0",),
        {"protocol": REPLAY_PROTOCOL_REF, "source": b.source_ref,
         "carriers": (b.respondent_ref, b.response_ref, b.exposure_ref, b.risk_ref), "currentness": CURRENTNESS_REF},
        (b.source_ref, b.respondent_ref, b.response_ref, b.exposure_ref, b.risk_ref, CURRENTNESS_REF))
    permission = _auth("GT12-A-R5-Q86-FROZEN-TARGET-USE", "TARGET_USE_PERMISSION",
        ("GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1", "GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1"),
        ("EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
        {"target_use_refs": (GT1_TARGET_USE_REF, GT2_TARGET_USE_REF), "predicate_or_risk_set_refs": (b.risk_ref,),
         "questions": (qa, qb), "measure": "RAW", "weights": "NOT_APPLICABLE", "currentness": CURRENTNESS_REF},
        (b.risk_ref, CURRENTNESS_REF))
    return source, routing, coordinate, projection, replay, permission


def projection_identity_ref(bindings: R5Q86CarrierBindings = FROZEN_BINDINGS) -> ExactRef:
    auths = _authorities(bindings)
    return _ref("C11_SEMANTIC_PROJECTION", CONTRACT_ID, {
        "source": bindings.source_ref.as_dict(), "respondents": bindings.respondent_ref.as_dict(),
        "responses": bindings.response_ref.as_dict(), "exposure": bindings.exposure_ref.as_dict(),
        "risk": bindings.risk_ref.as_dict(), "structure": bindings.structure_ref.as_dict(),
        "questions": [question_ref("Q86A").as_dict(), question_ref("Q86B").as_dict()],
        "domains": [domain_ref("Q86A").as_dict(), domain_ref("Q86B").as_dict()],
        "authorities": [a.authority_ref.as_dict() for a in auths], "currentness": CURRENTNESS_REF.as_dict(),
        "transport": "FFP014_FFP017_GOVERNED_REPLAY_EQUIVALENT_Q86_CURRENT_CARRIER_STREAM@1",
        "numeric_codes_are_order_or_metric_authority": False,
    })


def _validate_rows(rows: tuple[R5Q86GovernedRow, ...], b: R5Q86CarrierBindings):
    if len(rows) != b.source_row_count: raise R5Q86ProjectionError("governed row count differs from frozen source")
    if {r.row_ordinal for r in rows} != set(range(1, b.source_row_count + 1)):
        raise R5Q86ProjectionError("row ordinals must cover source exactly once")
    if len({r.respondent_key for r in rows}) != len(rows): raise R5Q86ProjectionError("duplicate (COUNTRY, RESPNO) identity")
    risk = tuple(r for r in rows if r.in_common_risk_set)
    if len(risk) != b.risk_set_row_count: raise R5Q86ProjectionError("common-risk membership differs from frozen risk set")
    for r in risk:
        # Independent exposure facts are mandatory; response values/presence never imply exposure.
        if r.q86a_exposure_state != "EXPOSED__PROVED" or r.q86b_exposure_state != "EXPOSED__PROVED":
            raise R5Q86ProjectionError("common-risk routing requires independent EXPOSED__PROVED Q86A/Q86B facts")


def _validate_claim_scope(
    rows: tuple[R5Q86GovernedRow, ...],
    members: tuple[R5Q86RiskSetMember, ...],
    member_set_sha256: str,
    b: R5Q86CarrierBindings,
) -> tuple[R5Q86GovernedRow, ...]:
    _validate_rows(rows, b)
    if member_set_sha256 != b.risk_set_member_set_sha256:
        raise R5Q86ProjectionError("risk-set semantic member-set SHA differs from frozen contract")
    if len(members) != b.risk_set_row_count:
        raise R5Q86ProjectionError("exact risk-set member count differs from frozen contract")
    member_keys = [m.respondent_key for m in members]
    if len(set(member_keys)) != len(member_keys):
        raise R5Q86ProjectionError("duplicate exact risk-set respondent")
    if len({m.respondent_local_id for m in members}) != len(members):
        raise R5Q86ProjectionError("duplicate exact risk-set respondent ref")
    source_by_key = {r.respondent_key: r for r in rows}
    expected_keys = {r.respondent_key for r in rows if r.in_common_risk_set}
    if set(member_keys) != expected_keys:
        missing = expected_keys - set(member_keys)
        extra = set(member_keys) - expected_keys
        raise R5Q86ProjectionError(
            f"exact risk-set membership mismatch missing={len(missing)} extra={len(extra)}"
        )
    selected = []
    for member in members:
        row = source_by_key.get(member.respondent_key)
        if row is None:
            raise R5Q86ProjectionError("risk-set member absent from governed source carrier")
        if row.country_alpha3 != member.country_alpha3:
            raise R5Q86ProjectionError("risk-set member country identity mismatch")
        if row.respondent_local_id is None:
            raise R5Q86ProjectionError("claim-scoped materialization requires exact respondent_local_id")
        if row.respondent_local_id != member.respondent_local_id:
            raise R5Q86ProjectionError("risk-set exact respondent ref mismatch")
        if row.q86a_exposure_state != "EXPOSED__PROVED" or row.q86b_exposure_state != "EXPOSED__PROVED":
            raise R5Q86ProjectionError("risk-set member lacks exact Q86A/Q86B exposure proof")
        selected.append(row)
    return tuple(sorted(selected, key=lambda r: r.row_ordinal))


def _build(
    rows: tuple[R5Q86GovernedRow, ...],
    b: R5Q86CarrierBindings,
    *,
    projection_rows: tuple[R5Q86GovernedRow, ...] | None = None,
) -> R5Q86ProjectionPackage:
    _validate_rows(rows, b)
    rows = tuple(sorted(rows if projection_rows is None else projection_rows, key=lambda r: r.row_ordinal))
    source_auth, routing_auth, coord_auth, projection_auth, replay_auth, permission_auth = _authorities(b)
    auths = (source_auth, routing_auth, coord_auth, projection_auth, replay_auth, permission_auth)
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED", authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(b.source_ref, b.respondent_ref, b.structure_ref, CURRENTNESS_REF),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "GT12:R5:Q86:UNIVERSE", {
            "source": b.source_ref.as_dict(), "respondents": b.respondent_ref.as_dict(), "currentness": CURRENTNESS_REF.as_dict()}),
        raw_source_identity=b.source_artifact_id, source_family="Afrobarometer", study_product_release="Afrobarometer/R5",
        instrument_release=f"merged_r5_codebook_2.pdf@sha256:{b.codebook_sha256}",
        country_geography="AFROBAROMETER_R5_SOURCE_NATIVE_MULTI_COUNTRY",
        sampling_geography="AFROBAROMETER_R5_SOURCE_NATIVE_SAMPLE_SCOPE", raw_wave="R5", canonical_wave_if_governed="R5",
        field_or_reference_time="AFROBAROMETER_ROUND_5_SOURCE_NATIVE",
        target_population_and_sample_frame="SOURCE_NATIVE_R5_SAMPLE_FRAME__NO_POPULATION_GENERALIZATION_BY_GT12",
        sampling_design_regime="SOURCE_NATIVE_R5__RAW_UNWEIGHTED_GT12_USE", respondent_namespace=b.respondent_carrier_id,
        source_artifact_import_lineage=f"source:{b.source_sha256}|respondents:{b.respondent_carrier_sha256}|responses:{b.response_fact_carrier_sha256}|exposure:{b.exposure_fact_carrier_sha256}",
        harmonization_authority_ref=None, source_relation_refs=())
    respondents = tuple(RespondentIdentity(
        empirical_universe_ref=universe.ref, respondent_key=r.respondent_key,
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", f"{b.respondent_carrier_id}:{r.respondent_key}", {
            "carrier": b.respondent_ref.as_dict(), "COUNTRY": r.country_native, "RESPNO": r.respno}),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE")) for r in rows)
    by_key = {r.respondent_key: obj for r, obj in zip(rows, respondents)}
    questions = tuple(QuestionVariableBinding(
        empirical_universe_ref=universe.ref, native_question_ref=question_ref(v), instrument_question_version="Afrobarometer_R5",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"), component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref, topology_authority_ref=source_auth.authority_ref) for v in ("Q86A", "Q86B"))
    qbind = dict(zip(("Q86A", "Q86B"), questions))

    response_slots = []
    for ordinal, variable in enumerate(("Q86A", "Q86B"), 1):
        occurrence = OccurrenceRule("0", _ref("RESPONSE_TOPOLOGY", f"Afrobarometer:R5:{variable}:SCALAR_SINGULAR", {
            "variable": variable, "kind": "SCALAR_SINGULAR", "numeric_order_authorized": False}), {"kind": "SCALAR_SINGULAR", "index": 0})
        values = tuple(ResponseValueRule(
            physical_value_binding_key(s.code, PhysicalMissingState.OBSERVED_STORAGE_VALUE,
                _declaration(variable, s.response_state, b.response_fact_carrier_sha256)),
            s.response_state, (occurrence,), None, None, ()) for s in Q86_NATIVE_STATES)
        response_slots.append(ResponseSlotRule(PhysicalSlot(ordinal, variable), qbind[variable], values))

    routing_rule = _ref("ROUTING_RULE", "GT12:R5:Q86:COMMON_COEXPOSURE_MEMBERSHIP", {
        "risk": b.risk_ref.as_dict(), "countries": COMMON_RISK_COUNTRIES,
        "q86a": exposure_predicate_ref("Q86A").as_dict(), "q86b": exposure_predicate_ref("Q86B").as_dict(),
        "response_presence_is_exposure_evidence": False})
    member_replay = _ref("MEMBER_SET_REPLAY", f"{b.risk_set_id}:REPLAY", {
        "risk": b.risk_ref.as_dict(), "member_hash": b.risk_set_member_set_sha256, "countries": COMMON_RISK_COUNTRIES})
    routing = []
    for r in rows:
        state = "ELIGIBLE_APPLICABLE" if r.in_common_risk_set else "NOT_ELIGIBLE"; respondent = by_key[r.respondent_key]
        for v in ("Q86A", "Q86B"):
            ep = exposure_predicate_ref(v)
            routing.append(RoutingEligibilityFact(
                typed_state=state, authority_snapshot_refs=(routing_auth.authority_ref,),
                dependency_refs=(respondent.ref, b.risk_ref, b.exposure_ref, ep),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"GT12:R5:{v}:ROUTING:{r.respondent_key}", {
                    "respondent": respondent.ref.as_dict(), "risk": b.risk_ref.as_dict(), "predicate": ep.as_dict(), "state": state}),
                empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref, question_or_target_ref=question_ref(v),
                risk_set_ref=b.risk_ref, routing_rule_ref=routing_rule, applicability_state=state, routing_state=state,
                parent_predicate_refs=(ep,), member_set_replay_ref=member_replay))

    coordinate_slot = CoordinateSlotRule(PhysicalSlot(3, "COUNTRY_ALPHA3"), COUNTRY_REF, COUNTRY_UNIT_REF,
        "AFROBAROMETER_ROUND_5_SOURCE_NATIVE", coord_auth.authority_ref, None, None, (), True)
    projection = GovernedC11Projection(
        projection_identity_ref=projection_identity_ref(b), source_artifact_id=b.source_artifact_id,
        expected_source_sha256=b.source_sha256, source_family_id="Afrobarometer", study_product_id="Afrobarometer",
        release_id="R5_GT12_Q86A_Q86B_FROZEN", instrument_release_id=f"merged_r5_codebook_2.pdf@sha256:{b.codebook_sha256}",
        source_snapshot_retention_ref=b.source_ref, universes=(universe,), respondents=respondents,
        row_bindings=tuple(RowRespondentBinding(r.row_ordinal, by_key[r.respondent_key].ref) for r in rows), questions=questions,
        response_slots=tuple(response_slots), coordinate_slots=(coordinate_slot,), routing=tuple(routing), weight_slots=(),
        authority_snapshots=auths, source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"), predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"), discovery_replay=TypedAbsence("DEFERRED"), structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in auths), projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref, tie_order_ref=TIE_ORDER_REF, replay_protocol_version="1.0.0")

    def cells():
        for r in rows:
            for ordinal, variable, value, state in ((1, "Q86A", r.q86a_raw_value, r.q86a_response_state), (2, "Q86B", r.q86b_raw_value, r.q86b_response_state)):
                token = _native(value, state, variable)
                yield PhysicalCell(r.row_ordinal, ordinal, variable, token, PhysicalMissingState.OBSERVED_STORAGE_VALUE,
                    _declaration(variable, state, b.response_fact_carrier_sha256), _STATE[token].label)
            yield PhysicalCell(r.row_ordinal, 3, "COUNTRY_ALPHA3", r.country_alpha3,
                PhysicalMissingState.OBSERVED_STORAGE_VALUE, None, None)
    stream = ExactPhysicalCellStream(b.source_sha256, len(rows), cells,
        "FFP014_FFP017_GOVERNED_REPLAY_EQUIVALENT_Q86_CURRENT_CARRIER_STREAM@1")
    return R5Q86ProjectionPackage(stream, projection, AuthorityRegistry(auths), question_ref("Q86A"), question_ref("Q86B"),
        domain_ref("Q86A"), domain_ref("Q86B"), target_domain_replay_ref("Q86A"), target_domain_replay_ref("Q86B"),
        b.risk_ref, CURRENTNESS_REF, GT1_TARGET_USE_REF, GT2_TARGET_USE_REF)


def build_r5_q86_c11_projection(inputs: R5Q86GovernedInputs) -> R5Q86ProjectionPackage:
    if not isinstance(inputs, R5Q86GovernedInputs): raise R5Q86ProjectionError("R5Q86GovernedInputs required")
    validate_frozen_bindings(inputs.bindings)
    return _build(tuple(inputs.rows), FROZEN_BINDINGS)


def build_validated_r5_q86_c11_release(inputs: R5Q86GovernedInputs):
    """Validate current full-source C11 only. I03 execution remains GT12-B-owned."""
    package = build_r5_q86_c11_projection(inputs)
    return build_validated_source_backed_c11_release_from_stream(package.stream, package.projection)


def build_claim_scoped_r5_q86_c11_projection(
    inputs: R5Q86ClaimScopedGovernedInputs,
) -> R5Q86ProjectionPackage:
    if not isinstance(inputs, R5Q86ClaimScopedGovernedInputs):
        raise R5Q86ProjectionError("R5Q86ClaimScopedGovernedInputs required")
    validate_frozen_bindings(inputs.bindings)
    claim_rows = _validate_claim_scope(
        tuple(inputs.source_rows),
        tuple(inputs.risk_set_members),
        inputs.risk_set_member_set_sha256,
        FROZEN_BINDINGS,
    )
    return _build(
        tuple(inputs.source_rows),
        FROZEN_BINDINGS,
        projection_rows=claim_rows,
    )


def build_validated_claim_scoped_r5_q86_c11_release(
    inputs: R5Q86ClaimScopedGovernedInputs,
):
    """Build exact 19,210-member claim-scoped C11 after full-source/risk proof."""
    package = build_claim_scoped_r5_q86_c11_projection(inputs)
    return build_validated_source_backed_c11_release_from_stream(
        package.stream, package.projection
    )


__all__ = [
    "CONTRACT_ID", "R5Q86ProjectionError", "NativeState", "Q86_NATIVE_STATES", "Q86", "R5Q86CarrierBindings",
    "FROZEN_BINDINGS", "COMMON_RISK_COUNTRIES", "CURRENTNESS_REF", "GT1_TARGET_USE_REF", "GT2_TARGET_USE_REF",
    "R5Q86GovernedRow", "R5Q86GovernedInputs", "R5Q86RiskSetMember", "R5Q86ClaimScopedGovernedInputs",
    "R5Q86ProjectionPackage", "question_ref", "exposure_predicate_ref",
    "domain_ref", "target_domain_replay_ref", "q86_target_domain", "validate_frozen_bindings", "projection_identity_ref",
    "build_r5_q86_c11_projection", "build_validated_r5_q86_c11_release",
    "build_claim_scoped_r5_q86_c11_projection", "build_validated_claim_scoped_r5_q86_c11_release",
]
