"""GT34 OBL031 one-field ADP-010 -> R5 Q69B comparator resolver.

Authority constitution is deliberately separate from positive runtime invocation.
The current path requires an independently current OBL048 subject classification
and an independently lawful current OBL055/ADP-010 ENCOUNTER record for the same
subject.  Synthetic proof fixtures use a different type and can never be passed
to resolve_current(), entered into actor history, OBL056 state, or PRE553
production.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Iterable, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalPredicate,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.v3_adp010_oee_executor import (
    ADP010_AUTHORITY_ID,
    ADP010_AUTHORITY_VERSION,
    EFFECT_ENCOUNTER,
    STATE_ENCOUNTER,
    V3OEERealizationRecord,
)
from rawlsing_next.v3_adp010_oee_executor_obl055_replay_canonical import (
    EXECUTOR_ID as OBL055_EXECUTOR_ID,
    validate_record as validate_obl055_record,
)

AUTHORITY_ID = "GT34_OBL031_ADP010_Q69B_FIELD_SPECIFIC_COMPARATOR_AUTHORITY"
AUTHORITY_VERSION = "1.1.0"
AUTHORITY_SCHEMA = f"{AUTHORITY_ID}@{AUTHORITY_VERSION}"

EXACT_SUBJECT_REF = "urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
EXACT_SUBJECT_HASH = "a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33"
OBL048_AUTHORITY_ID = "GT34_OBL048_EXACT_FIRST_CANARY_SUBJECT_CLASSIFICATION_AUTHORITY"
OBL048_AUTHORITY_VERSION = "1.0.0"
OBL048_AUTHORITY_HASH = "a0cd9714145ea4c7edd862b2a0dfdd50c2912c5ae2de598632dbe6fd2bc62794"
OBL048_PROPOSITION = "SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL"
OBL048_PROPOSITION_HASH = "90c69c1d6f548214ae4c33f3aceac76e78b083d5b03218fcf4139f3922e3ea11"
SUBJECT_REQUIREMENT_ID = "GT34_ADP010_Q69B_PUBLIC_CLINIC_SUBJECT_SEMANTIC_REQUIREMENT@1.1.0"
SUBJECT_REQUIREMENT_HASH = "219fe6714efbcda30b6d9ea69cec6b99f3fe86a92c43ae7122a68e404f795fca"

Q69B_SOURCE_SHA256 = "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
Q69B_UNIVERSE_HASH = "4dc56730f5c3b06838cc8a6116e0f4c78662b76d75b578918f7207cea3902dd1"
Q69B_RELEASE_ID = "R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1"
Q69B_RELEASE_HASH = "2343023560ea963b6b290575d93361256825897a7c32ff315e3d2425b595ec"
# Historical documents sometimes omit one 'f' in prose; the accepted value is
# normalized below by the explicit manifest binding supplied by callers.
Q69B_ACCEPTED_RELEASE_HASH = "2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec"
Q69B_SOURCE_RELEASE_MANIFEST_HASH = "15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4"
Q69B_REPLAY_HASH = "8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539"
Q69B_COORDINATE_ID = "Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_STATUS"
Q69B_COORDINATE_HASH = "7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937"
Q69B_COORDINATE_AUTHORITY_ID = "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY"
Q69B_COORDINATE_AUTHORITY_VERSION = "1.0.0"
Q69B_COORDINATE_AUTHORITY_HASH = "cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c"
Q69B_CROSSWALK_ID = "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_STATUS_CROSSWALK@1.0.0"
Q69B_CROSSWALK_HASH = "fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095"
Q69B_TIME_AUTHORITY_ID = "R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR@1.0.0"
Q69B_TIME_AUTHORITY_HASH = "4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2"
Q69B_MEASURE_BASIS_HASH = "f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3"
Q69B_CURRENTNESS_HASH = "467a98d69e49a715527c79f35dbfe65dc95bfbfee7ae455053465b8b438c3a08"
Q69B_PRESENT_VALUE = "PUBLIC_CLINIC_EXPERIENCE_PRESENT"
RELATION_PROOF_ID = "GT34_L1A_Q69B_TO_ADP010_ENCOUNTER_RELATION_PROOF@1.0.0"
RELATION_PROOF_HASH = "7eaa5197a26c3e5ddc65b631453007f2a5ed9ba9310da6c9c233eaef6fb12aa9"

CURRENT_ACCEPTED = "CURRENT_ACCEPTED"
NONCURRENT_SYNTHETIC_TEST_ONLY = "NONCURRENT_SYNTHETIC_TEST_ONLY"

ACTOR_FACT_MISSING_OR_UNAUTHORIZED = "ACTOR_FACT_MISSING_OR_UNAUTHORIZED"
EMPIRICAL_COORDINATE_AUTHORITY_MISSING = "EMPIRICAL_COORDINATE_AUTHORITY_MISSING"
COMPARATOR_RULE_MISSING = "COMPARATOR_RULE_MISSING"
NONCOMPARABLE = "NONCOMPARABLE"
UNRESOLVED = "UNRESOLVED"
SOURCE_TIME_GEOGRAPHY_EQUIVALENCE_UNRESOLVED = "SOURCE_TIME_GEOGRAPHY_EQUIVALENCE_UNRESOLVED"
AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING = "AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING"
NO_EXACT_MATCH = "NO_EXACT_MATCH"
LAWFUL_VALID_EMPTY = "LAWFUL_VALID_EMPTY"
INTEGRITY_REF_HASH_REPLAY_FAILURE = "INTEGRITY_REF_HASH_REPLAY_FAILURE"
D08_GRAMMAR_UNRESOLVED = "D08_GRAMMAR_UNRESOLVED"
RESOLVED = "RESOLVED"
NONCURRENT_SYNTHETIC_PROOF = "NONCURRENT_SYNTHETIC_PROOF"


def _canon(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value) -> str:
    return sha256(_canon(value).encode("utf-8")).hexdigest()


def _parse_time(value: str) -> datetime:
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("time must be timezone-aware")
    return dt


AUTHORITY_MATERIAL = {
    "schema": AUTHORITY_SCHEMA,
    "jurisdiction": "ONE_FIELD_ONLY__ADP010_PUBLIC_CLINIC_ENCOUNTER_TO_R5_Q69B_PRESENT",
    "input_premises": [
        "CURRENT_EXACT_OBL048_SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
        "INDEPENDENT_LAWFUL_ADP010_ENCOUNTER_SAME_SUBJECT",
        "EXACT_ACTOR_EFFECTIVE_TIME",
        "EXACT_R5_Q69B_COORDINATE_RELEASE_TIME_AND_D08_GRAMMAR",
    ],
    "positive_output_ceiling": ["EXACT_D08_EMPIRICAL_PREDICATE", "COMPARATOR_PROVENANCE_RECEIPT"],
    "subject_requirement": [SUBJECT_REQUIREMENT_ID, SUBJECT_REQUIREMENT_HASH],
    "relation_proof": [RELATION_PROOF_ID, RELATION_PROOF_HASH],
    "forbidden": [
        "ACTOR_TO_Q69B_ABSENT_FROM_SILENCE",
        "GENERATED_STRUCTURAL_POSITION_INTERMEDIATE",
        "STRING_OR_LABEL_SIMILARITY",
        "FUZZY_MATCHING",
        "EMBEDDING_SIMILARITY",
        "NEAREST_COHORT_SUBSTITUTION",
        "LLM_OR_NARRATIVE_EQUIVALENCE",
        "ACTOR_BELIEF_KNOWLEDGE_RESPONSE_PERSONA",
        "PSEPF",
        "V3_MUTATION",
        "METABOLISM",
        "CAN_008",
        "V2",
    ],
}
AUTHORITY_CONTENT_HASH = _digest(AUTHORITY_MATERIAL)


@dataclass(frozen=True, slots=True)
class OBL048ClassificationProof:
    subject_ref: str
    subject_hash: str
    authority_id: str
    authority_version: str
    authority_hash: str
    proposition: str
    proposition_hash: str
    currentness: str
    provenance_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Q69BSourceBinding:
    source_sha256: str = Q69B_SOURCE_SHA256
    universe_hash: str = Q69B_UNIVERSE_HASH
    release_id: str = Q69B_RELEASE_ID
    release_hash: str = Q69B_ACCEPTED_RELEASE_HASH
    source_release_manifest_hash: str = Q69B_SOURCE_RELEASE_MANIFEST_HASH
    replay_hash: str = Q69B_REPLAY_HASH
    coordinate_id: str = Q69B_COORDINATE_ID
    coordinate_hash: str = Q69B_COORDINATE_HASH
    coordinate_authority_id: str = Q69B_COORDINATE_AUTHORITY_ID
    coordinate_authority_version: str = Q69B_COORDINATE_AUTHORITY_VERSION
    coordinate_authority_hash: str = Q69B_COORDINATE_AUTHORITY_HASH
    crosswalk_id: str = Q69B_CROSSWALK_ID
    crosswalk_hash: str = Q69B_CROSSWALK_HASH
    time_authority_id: str = Q69B_TIME_AUTHORITY_ID
    time_authority_hash: str = Q69B_TIME_AUTHORITY_HASH
    measure_basis_hash: str = Q69B_MEASURE_BASIS_HASH
    currentness_hash: str = Q69B_CURRENTNESS_HASH
    currentness: str = CURRENT_ACCEPTED


@dataclass(frozen=True, slots=True)
class D08GrammarBinding:
    authority_id: str
    authority_version: str
    authority_hash: str
    authority_kind: str
    governed_operation: str
    governed_object_family: str
    operator_semantics_refs: tuple[ExactRef, ...]
    currentness: str
    provenance_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RespondentDateIntrWindow:
    respondent_ref: ExactRef
    dateintr_ref: ExactRef
    window_start: str
    window_end: str
    lower_edge_inclusive: bool | None
    currentness: str


@dataclass(frozen=True, slots=True)
class SyntheticEncounterFixture:
    fixture_mode: str
    actor_id: str
    subject_ref: str
    authority_id: str
    authority_version: str
    realization_state: str
    event_effect_kind: str
    effective_from: str
    fixture_hash: str

    @classmethod
    def build(cls, actor_id: str, effective_from: str) -> "SyntheticEncounterFixture":
        material = {
            "fixture_mode": NONCURRENT_SYNTHETIC_TEST_ONLY,
            "actor_id": actor_id,
            "subject_ref": EXACT_SUBJECT_REF,
            "authority_id": ADP010_AUTHORITY_ID,
            "authority_version": ADP010_AUTHORITY_VERSION,
            "realization_state": STATE_ENCOUNTER,
            "event_effect_kind": EFFECT_ENCOUNTER,
            "effective_from": effective_from,
        }
        return cls(**material, fixture_hash=_digest(material))


@dataclass(frozen=True, slots=True)
class SyntheticPredicatePreview:
    fixture_mode: str
    predicate_ast: dict
    predicate_hash: str
    coordinate_question_value_refs: tuple[ExactRef, ...]
    scope_refs: tuple[ExactRef, ...]
    operator_semantics_refs: tuple[ExactRef, ...]


@dataclass(frozen=True, slots=True)
class ComparatorProvenanceReceipt:
    authority_id: str
    authority_version: str
    authority_content_hash: str
    actor_fact_ref: str
    actor_fact_hash: str
    actor_semantic_owner_authority: str
    actor_effective_time: str
    subject_ref: str
    obl048_authority_hash: str
    obl048_proposition_hash: str
    source_release_scope: tuple[str, ...]
    empirical_coordinate_refs: tuple[str, ...]
    comparator_rule_identity: tuple[str, str, str]
    equivalence_crosswalk_time_geography_authorities: tuple[str, ...]
    d08_grammar_authority: tuple[str, str, str]
    resulting_predicate_ref: str
    resulting_predicate_hash: str
    deterministic_replay_identity: str
    currentness: str
    receipt_hash: str


@dataclass(frozen=True, slots=True)
class ComparatorResolution:
    outcome: str
    predicate: EmpiricalPredicate | None = None
    receipt: ComparatorProvenanceReceipt | None = None
    synthetic_preview: SyntheticPredicatePreview | None = None
    detail: str = ""


def current_obl048_proof() -> OBL048ClassificationProof:
    return OBL048ClassificationProof(
        subject_ref=EXACT_SUBJECT_REF,
        subject_hash=EXACT_SUBJECT_HASH,
        authority_id=OBL048_AUTHORITY_ID,
        authority_version=OBL048_AUTHORITY_VERSION,
        authority_hash=OBL048_AUTHORITY_HASH,
        proposition=OBL048_PROPOSITION,
        proposition_hash=OBL048_PROPOSITION_HASH,
        currentness=CURRENT_ACCEPTED,
        provenance_refs=("HQ_OBL048_ADOPTION", SUBJECT_REQUIREMENT_ID),
    )


def _validate_classification(proof: OBL048ClassificationProof) -> bool:
    return proof == current_obl048_proof()


def _validate_source(binding: Q69BSourceBinding) -> str | None:
    if binding.currentness != CURRENT_ACCEPTED:
        return EMPIRICAL_COORDINATE_AUTHORITY_MISSING
    if binding != Q69BSourceBinding():
        return INTEGRITY_REF_HASH_REPLAY_FAILURE
    return None


def _validate_grammar(binding: D08GrammarBinding | None, *, current: bool) -> str | None:
    if binding is None:
        return D08_GRAMMAR_UNRESOLVED
    if binding.authority_kind != "PREDICATE_GRAMMAR":
        return D08_GRAMMAR_UNRESOLVED
    if binding.governed_object_family != "EmpiricalPredicate@1.0.0":
        return D08_GRAMMAR_UNRESOLVED
    if binding.governed_operation != "RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE_EQ_PREDICATE":
        return D08_GRAMMAR_UNRESOLVED
    if not binding.operator_semantics_refs:
        return D08_GRAMMAR_UNRESOLVED
    if not binding.provenance_refs:
        return INTEGRITY_REF_HASH_REPLAY_FAILURE
    if current and binding.currentness != CURRENT_ACCEPTED:
        return D08_GRAMMAR_UNRESOLVED
    if not current and binding.currentness != NONCURRENT_SYNTHETIC_TEST_ONLY:
        return D08_GRAMMAR_UNRESOLVED
    return None


def _temporal_scope(event_time: str, windows: Sequence[RespondentDateIntrWindow], *, current: bool):
    if not windows:
        return LAWFUL_VALID_EMPTY, ()
    seen: dict[str, tuple[str, str, bool | None]] = {}
    included: list[RespondentDateIntrWindow] = []
    event = _parse_time(event_time)
    for window in windows:
        expected_currentness = CURRENT_ACCEPTED if current else NONCURRENT_SYNTHETIC_TEST_ONLY
        if window.currentness != expected_currentness:
            return SOURCE_TIME_GEOGRAPHY_EQUIVALENCE_UNRESOLVED, ()
        key = window.respondent_ref.key
        signature = (window.window_start, window.window_end, window.lower_edge_inclusive)
        if key in seen and seen[key] != signature:
            return AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING, ()
        seen[key] = signature
        start, end = _parse_time(window.window_start), _parse_time(window.window_end)
        if start > end:
            return INTEGRITY_REF_HASH_REPLAY_FAILURE, ()
        if event == start and window.lower_edge_inclusive is None:
            return NONCOMPARABLE, ()
        lower_ok = event > start or (event == start and window.lower_edge_inclusive is True)
        if lower_ok and event <= end:
            included.append(window)
    if not included:
        return NO_EXACT_MATCH, ()
    included.sort(key=lambda w: w.respondent_ref.key)
    return RESOLVED, tuple(included)


def _predicate_material(included: Sequence[RespondentDateIntrWindow]):
    scope_keys = [w.respondent_ref.key for w in included]
    ast = {
        "op": "LEAF",
        "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
        "coordinate_ref": Q69B_COORDINATE_ID,
        "comparison_operator": "EQ",
        "canonical_value": Q69B_PRESENT_VALUE,
        "source_release": [Q69B_RELEASE_ID, Q69B_ACCEPTED_RELEASE_HASH],
        "respondent_scope_refs": scope_keys,
        "temporal_authority": [Q69B_TIME_AUTHORITY_ID, Q69B_TIME_AUTHORITY_HASH],
    }
    refs = (
        ExactRef("EMPIRICAL_COORDINATE", Q69B_COORDINATE_ID, Q69B_COORDINATE_HASH),
        ExactRef("EMPIRICAL_VALUE", f"{Q69B_COORDINATE_ID}:{Q69B_PRESENT_VALUE}", _digest({"coordinate": Q69B_COORDINATE_ID, "value": Q69B_PRESENT_VALUE})),
    )
    scopes = tuple(w.respondent_ref for w in included)
    return ast, refs, scopes


def _receipt(*, actor_ref: str, actor_hash: str, effective_time: str,
             grammar: D08GrammarBinding, predicate_ref: str, predicate_hash: str,
             currentness: str) -> ComparatorProvenanceReceipt:
    core = {
        "authority_id": AUTHORITY_ID,
        "authority_version": AUTHORITY_VERSION,
        "authority_content_hash": AUTHORITY_CONTENT_HASH,
        "actor_fact_ref": actor_ref,
        "actor_fact_hash": actor_hash,
        "actor_semantic_owner_authority": f"{ADP010_AUTHORITY_ID}@{ADP010_AUTHORITY_VERSION}",
        "actor_effective_time": effective_time,
        "subject_ref": EXACT_SUBJECT_REF,
        "obl048_authority_hash": OBL048_AUTHORITY_HASH,
        "obl048_proposition_hash": OBL048_PROPOSITION_HASH,
        "source_release_scope": (Q69B_SOURCE_SHA256, Q69B_UNIVERSE_HASH, Q69B_RELEASE_ID, Q69B_ACCEPTED_RELEASE_HASH),
        "empirical_coordinate_refs": (Q69B_COORDINATE_ID, Q69B_COORDINATE_HASH),
        "comparator_rule_identity": (AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH),
        "equivalence_crosswalk_time_geography_authorities": (Q69B_CROSSWALK_HASH, Q69B_TIME_AUTHORITY_HASH, RELATION_PROOF_HASH),
        "d08_grammar_authority": (grammar.authority_id, grammar.authority_version, grammar.authority_hash),
        "resulting_predicate_ref": predicate_ref,
        "resulting_predicate_hash": predicate_hash,
        "currentness": currentness,
    }
    replay = _digest(core)
    with_replay = {**core, "deterministic_replay_identity": replay}
    return ComparatorProvenanceReceipt(**with_replay, receipt_hash=_digest(with_replay))


def resolve_current(*, actor_record: V3OEERealizationRecord | None,
                    expected_actor_id: str,
                    classification_proof: OBL048ClassificationProof,
                    q69b_binding: Q69BSourceBinding,
                    grammar_binding: D08GrammarBinding | None,
                    respondent_windows: Sequence[RespondentDateIntrWindow]) -> ComparatorResolution:
    """Resolve only from real current inputs.  No current actor fact => typed negative."""
    if actor_record is None:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="no current accepted actor ENCOUNTER fact supplied")
    if isinstance(actor_record, SyntheticEncounterFixture):
        return ComparatorResolution(INTEGRITY_REF_HASH_REPLAY_FAILURE, detail="synthetic fixture cannot enter current resolver")
    try:
        actor_record = validate_obl055_record(actor_record)
    except Exception as exc:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail=f"OBL055/ADP010 validation failed: {type(exc).__name__}")
    if (actor_record.authority_id, actor_record.authority_version) != (ADP010_AUTHORITY_ID, ADP010_AUTHORITY_VERSION):
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong ADP-010 owner")
    if actor_record.realization_state != STATE_ENCOUNTER or actor_record.event_effect_kind != EFFECT_ENCOUNTER:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong state/effect")
    if actor_record.actor_id != expected_actor_id:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong actor")
    if actor_record.subject_ref != EXACT_SUBJECT_REF:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong subject")
    if not _validate_classification(classification_proof):
        return ComparatorResolution(NONCOMPARABLE, detail="wrong or stale OBL048 subject classification proof")
    source_error = _validate_source(q69b_binding)
    if source_error:
        return ComparatorResolution(source_error, detail="Q69B source/release/coordinate currentness or integrity failed")
    grammar_error = _validate_grammar(grammar_binding, current=True)
    if grammar_error:
        return ComparatorResolution(grammar_error, detail="exact current D08 grammar unresolved")
    temporal, included = _temporal_scope(actor_record.effective_from, respondent_windows, current=True)
    if temporal != RESOLVED:
        return ComparatorResolution(temporal, detail="respondent-specific DATEINTR temporal relation did not resolve")
    assert grammar_binding is not None
    ast, coordinate_refs, scope_refs = _predicate_material(included)
    predicate_hash = semantic_hash(ast)
    replay_seed = _digest({"actor_record_hash": actor_record.record_hash, "ast_hash": predicate_hash, "scope": [x.key for x in scope_refs]})
    predicate = EmpiricalPredicate(
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(
            AuthorityRef(grammar_binding.authority_id, grammar_binding.authority_version, grammar_binding.authority_hash),
            AuthorityRef(Q69B_COORDINATE_AUTHORITY_ID, Q69B_COORDINATE_AUTHORITY_VERSION, Q69B_COORDINATE_AUTHORITY_HASH),
        ),
        dependency_refs=coordinate_refs,
        producer_replay_locator_or_reference_root=f"urn:rawlsing:gt34:obl031:replay:{replay_seed}",
        predicate_ast=ast,
        predicate_hash=predicate_hash,
        grammar_authority_ref=AuthorityRef(grammar_binding.authority_id, grammar_binding.authority_version, grammar_binding.authority_hash),
        coordinate_question_value_refs=coordinate_refs,
        risk_set_refs=(),
        scope_refs=scope_refs,
        same_respondent_binding_semantics="EXACT_RESPONDENT_REF__Q69B_DATEINTR_NATIVE_WINDOW",
        operator_semantics_refs=grammar_binding.operator_semantics_refs,
    )
    receipt = _receipt(actor_ref=actor_record.record_id, actor_hash=actor_record.record_hash,
                       effective_time=actor_record.effective_from, grammar=grammar_binding,
                       predicate_ref=predicate.object_id, predicate_hash=predicate.content_hash,
                       currentness=CURRENT_ACCEPTED)
    return ComparatorResolution(RESOLVED, predicate=predicate, receipt=receipt)


def prove_noncurrent_synthetic(*, fixture: SyntheticEncounterFixture,
                               classification_proof: OBL048ClassificationProof,
                               q69b_binding: Q69BSourceBinding,
                               grammar_binding: D08GrammarBinding,
                               respondent_windows: Sequence[RespondentDateIntrWindow]) -> ComparatorResolution:
    """Mechanically prove the positive rule without creating a production predicate.

    The fixture type is intentionally not V3OEERealizationRecord and this function
    returns SyntheticPredicatePreview, intentionally not EmpiricalPredicate.
    """
    if fixture.fixture_mode != NONCURRENT_SYNTHETIC_TEST_ONLY:
        return ComparatorResolution(INTEGRITY_REF_HASH_REPLAY_FAILURE, detail="synthetic fixture mode required")
    expected = SyntheticEncounterFixture.build(fixture.actor_id, fixture.effective_from)
    if fixture != expected:
        return ComparatorResolution(INTEGRITY_REF_HASH_REPLAY_FAILURE, detail="synthetic fixture hash/replay drift")
    if (fixture.authority_id, fixture.authority_version) != (ADP010_AUTHORITY_ID, ADP010_AUTHORITY_VERSION):
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong synthetic ADP-010 owner")
    if fixture.realization_state != STATE_ENCOUNTER or fixture.event_effect_kind != EFFECT_ENCOUNTER:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong synthetic state/effect")
    if fixture.subject_ref != EXACT_SUBJECT_REF:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong synthetic subject")
    if not _validate_classification(classification_proof):
        return ComparatorResolution(NONCOMPARABLE, detail="wrong OBL048 proof")
    # Synthetic proof uses the exact frozen Q69B identity but does not claim Q69B current production.
    if q69b_binding != Q69BSourceBinding():
        return ComparatorResolution(INTEGRITY_REF_HASH_REPLAY_FAILURE, detail="Q69B binding drift")
    grammar_error = _validate_grammar(grammar_binding, current=False)
    if grammar_error:
        return ComparatorResolution(grammar_error, detail="synthetic D08 grammar fixture invalid")
    temporal, included = _temporal_scope(fixture.effective_from, respondent_windows, current=False)
    if temporal != RESOLVED:
        return ComparatorResolution(temporal, detail="synthetic DATEINTR relation did not resolve")
    ast, coordinate_refs, scope_refs = _predicate_material(included)
    predicate_hash = semantic_hash(ast)
    preview = SyntheticPredicatePreview(
        fixture_mode=NONCURRENT_SYNTHETIC_TEST_ONLY,
        predicate_ast=ast,
        predicate_hash=predicate_hash,
        coordinate_question_value_refs=coordinate_refs,
        scope_refs=scope_refs,
        operator_semantics_refs=grammar_binding.operator_semantics_refs,
    )
    preview_ref = f"urn:rawlsing:gt34:obl031:noncurrent-synthetic-predicate-preview:sha256:{_digest(asdict(preview))}"
    receipt = _receipt(actor_ref=f"urn:rawlsing:gt34:obl031:synthetic-encounter:{fixture.fixture_hash}",
                       actor_hash=fixture.fixture_hash, effective_time=fixture.effective_from,
                       grammar=grammar_binding, predicate_ref=preview_ref,
                       predicate_hash=predicate_hash, currentness=NONCURRENT_SYNTHETIC_TEST_ONLY)
    return ComparatorResolution(NONCURRENT_SYNTHETIC_PROOF, receipt=receipt, synthetic_preview=preview)


def authority_identity() -> tuple[str, str, str]:
    return AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH
