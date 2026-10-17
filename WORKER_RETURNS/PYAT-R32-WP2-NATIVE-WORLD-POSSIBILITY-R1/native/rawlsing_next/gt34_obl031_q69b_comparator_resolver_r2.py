"""GT34 OBL031 R2 one-field ADP-010 -> R5 Q69B comparator resolver.

R2 repairs only the worker-ancestry dependency defect found by the R1 governed
court.  The campaign branch consumes HQ state prospectively, so the adopted
OBL055 implementation is not physically present on this worker ancestry.  R2
therefore imports the exact current OBL055 validator only when a real current
actor fact is actually supplied.  The mandated no-current-fact invocation and
all NONCURRENT_SYNTHETIC_TEST_ONLY proof mechanics remain executable without
copying/rebasing HQ production code into the campaign.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Sequence

from rawlsing_next.pre553_empirical_objects import AuthorityRef, EmpiricalPredicate, ExactRef, semantic_hash
from rawlsing_next.v3_adp010_oee_executor import (
    ADP010_AUTHORITY_ID,
    ADP010_AUTHORITY_VERSION,
    EFFECT_ENCOUNTER,
    STATE_ENCOUNTER,
    V3OEERealizationRecord,
)

AUTHORITY_ID = "GT34_OBL031_ADP010_Q69B_FIELD_SPECIFIC_COMPARATOR_AUTHORITY"
AUTHORITY_VERSION = "1.1.1"
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
Q69B_ACCEPTED_RELEASE_HASH = "2343023560ea963b6b290575d93361256825897a7c32ff31519e3d2425b595ec"
Q69B_SOURCE_RELEASE_MANIFEST_HASH = "15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4"
Q69B_REPLAY_HASH = "8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539"
Q69B_COORDINATE_ID = "Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_STATUS"
Q69B_COORDINATE_HASH = "7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937"
Q69B_COORDINATE_AUTHORITY_ID = "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY"
Q69B_COORDINATE_AUTHORITY_VERSION = "1.0.0"
Q69B_COORDINATE_AUTHORITY_HASH = "cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c"
Q69B_CROSSWALK_HASH = "fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095"
Q69B_TIME_AUTHORITY_ID = "R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR@1.0.0"
Q69B_TIME_AUTHORITY_HASH = "4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2"
Q69B_MEASURE_BASIS_HASH = "f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3"
Q69B_CURRENTNESS_HASH = "467a98d69e49a715527c79f35dbfe65dc95bfbfee7ae455053465b8b438c3a08"
Q69B_PRESENT_VALUE = "PUBLIC_CLINIC_EXPERIENCE_PRESENT"
RELATION_PROOF_HASH = "7eaa5197a26c3e5ddc65b631453007f2a5ed9ba9310da6c9c233eaef6fb12aa9"
CURRENT_OBL055_EXECUTOR = "GT34_V3P5_ADP010_OBL056_CANONICAL_RECONSTRUCTED_REPLAY_EXECUTOR@3.1.1"
CURRENT_OBL055_IMPLEMENTATION_BLOB = "e8c6edab3b310b797997a3826b8acb32f7f08ce9"
CURRENT_OBL055_SUCCESSOR_HASH = "273f7cc59acfd60942158bac4ca6b5d1cef40521f7eb343436b6723822d93251"

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


def _canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(v):
    return sha256(_canon(v).encode("utf-8")).hexdigest()


def _parse_time(value: str) -> datetime:
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("time must be timezone-aware")
    return dt


AUTHORITY_MATERIAL = {
    "schema": AUTHORITY_SCHEMA,
    "jurisdiction": "ONE_FIELD_ONLY__ADP010_PUBLIC_CLINIC_ENCOUNTER_TO_R5_Q69B_PRESENT",
    "required_separate_positive_premises": [
        "OBL048_SUBJECT_IS_PUBLIC_CLINIC_OR_HOSPITAL",
        "ADP010_ENCOUNTER_OEE_ENCOUNTER_OCCURRED_SAME_SUBJECT",
        "ACTOR_EFFECTIVE_TIME",
    ],
    "current_obl055_dependency": [CURRENT_OBL055_EXECUTOR, CURRENT_OBL055_IMPLEMENTATION_BLOB, CURRENT_OBL055_SUCCESSOR_HASH],
    "positive_output_ceiling": ["EXACT_D08_EMPIRICAL_PREDICATE", "COMPARATOR_PROVENANCE_RECEIPT"],
    "synthetic_firewall": "NONCURRENT_SYNTHETIC_TEST_ONLY_NEVER_PRE553_PRODUCTION",
    "forbidden": [
        "ACTOR_TO_Q69B_ABSENT_FROM_SILENCE_OR_NONOCCURRENCE",
        "GENERATED_STRUCTURAL_POSITION_INTERMEDIATE",
        "STRING_LABEL_FUZZY_EMBEDDING_NEAREST_COHORT_LLM_NARRATIVE_EQUIVALENCE",
        "ACTOR_BELIEF_KNOWLEDGE_RESPONSE_PERSONA",
        "PSEPF_V3_MUTATION_METABOLISM_CAN008_V2",
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
    crosswalk_hash: str = Q69B_CROSSWALK_HASH
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
    def build(cls, actor_id: str, effective_from: str):
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


def current_obl048_proof():
    return OBL048ClassificationProof(
        EXACT_SUBJECT_REF, EXACT_SUBJECT_HASH, OBL048_AUTHORITY_ID,
        OBL048_AUTHORITY_VERSION, OBL048_AUTHORITY_HASH, OBL048_PROPOSITION,
        OBL048_PROPOSITION_HASH, CURRENT_ACCEPTED,
        ("HQ_OBL048_ADOPTION", SUBJECT_REQUIREMENT_ID, SUBJECT_REQUIREMENT_HASH),
    )


def _validate_classification(proof):
    return proof == current_obl048_proof()


def _validate_source(binding):
    if binding.currentness != CURRENT_ACCEPTED:
        return EMPIRICAL_COORDINATE_AUTHORITY_MISSING
    if binding != Q69BSourceBinding():
        return INTEGRITY_REF_HASH_REPLAY_FAILURE
    return None


def _validate_grammar(binding, current: bool):
    if binding is None or binding.authority_kind != "PREDICATE_GRAMMAR":
        return D08_GRAMMAR_UNRESOLVED
    if binding.governed_object_family != "EmpiricalPredicate@1.0.0":
        return D08_GRAMMAR_UNRESOLVED
    if binding.governed_operation != "RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE_EQ_PREDICATE":
        return D08_GRAMMAR_UNRESOLVED
    if not binding.operator_semantics_refs:
        return D08_GRAMMAR_UNRESOLVED
    if not binding.provenance_refs:
        return INTEGRITY_REF_HASH_REPLAY_FAILURE
    expected = CURRENT_ACCEPTED if current else NONCURRENT_SYNTHETIC_TEST_ONLY
    return None if binding.currentness == expected else D08_GRAMMAR_UNRESOLVED


def _temporal_scope(event_time, windows: Sequence[RespondentDateIntrWindow], current: bool):
    if not windows:
        return LAWFUL_VALID_EMPTY, ()
    event = _parse_time(event_time)
    expected = CURRENT_ACCEPTED if current else NONCURRENT_SYNTHETIC_TEST_ONLY
    seen = {}
    included = []
    for w in windows:
        if w.currentness != expected:
            return SOURCE_TIME_GEOGRAPHY_EQUIVALENCE_UNRESOLVED, ()
        sig = (w.window_start, w.window_end, w.lower_edge_inclusive)
        if w.respondent_ref.key in seen and seen[w.respondent_ref.key] != sig:
            return AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING, ()
        seen[w.respondent_ref.key] = sig
        start, end = _parse_time(w.window_start), _parse_time(w.window_end)
        if start > end:
            return INTEGRITY_REF_HASH_REPLAY_FAILURE, ()
        if event == start and w.lower_edge_inclusive is None:
            return NONCOMPARABLE, ()
        if (event > start or (event == start and w.lower_edge_inclusive is True)) and event <= end:
            included.append(w)
    if not included:
        return NO_EXACT_MATCH, ()
    return RESOLVED, tuple(sorted(included, key=lambda w: w.respondent_ref.key))


def _predicate_material(included):
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
    return ast, refs, tuple(w.respondent_ref for w in included)


def _receipt(actor_ref, actor_hash, effective_time, grammar, predicate_ref, predicate_hash, currentness):
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


def _validate_real_actor_record(record):
    """Invoke the exact project-current OBL055 validator only for a real record."""
    try:
        from rawlsing_next.v3_adp010_oee_executor_obl055_replay_canonical import validate_record
    except ModuleNotFoundError as exc:
        return None, f"current OBL055 implementation not materialized on this campaign ancestry: {exc.name}"
    try:
        return validate_record(record), ""
    except Exception as exc:
        return None, f"OBL055/ADP010 validation failed: {type(exc).__name__}"


def resolve_current(*, actor_record: V3OEERealizationRecord | None, expected_actor_id: str,
                    classification_proof: OBL048ClassificationProof, q69b_binding: Q69BSourceBinding,
                    grammar_binding: D08GrammarBinding | None,
                    respondent_windows: Sequence[RespondentDateIntrWindow]):
    if actor_record is None:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="no current accepted actor ENCOUNTER fact supplied")
    if isinstance(actor_record, SyntheticEncounterFixture):
        return ComparatorResolution(INTEGRITY_REF_HASH_REPLAY_FAILURE, detail="synthetic fixture cannot enter current resolver")
    actor_record, detail = _validate_real_actor_record(actor_record)
    if actor_record is None:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail=detail)
    if (actor_record.authority_id, actor_record.authority_version) != (ADP010_AUTHORITY_ID, ADP010_AUTHORITY_VERSION):
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong ADP-010 owner")
    if actor_record.realization_state != STATE_ENCOUNTER or actor_record.event_effect_kind != EFFECT_ENCOUNTER:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong state/effect")
    if actor_record.actor_id != expected_actor_id or actor_record.subject_ref != EXACT_SUBJECT_REF:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED, detail="wrong actor/subject")
    if not _validate_classification(classification_proof):
        return ComparatorResolution(NONCOMPARABLE, detail="wrong OBL048 proof")
    source_error = _validate_source(q69b_binding)
    if source_error:
        return ComparatorResolution(source_error, detail="Q69B identity/currentness failure")
    grammar_error = _validate_grammar(grammar_binding, True)
    if grammar_error:
        return ComparatorResolution(grammar_error, detail="exact current D08 grammar unresolved")
    temporal, included = _temporal_scope(actor_record.effective_from, respondent_windows, True)
    if temporal != RESOLVED:
        return ComparatorResolution(temporal)
    assert grammar_binding is not None
    ast, coordinate_refs, scope_refs = _predicate_material(included)
    p_hash = semantic_hash(ast)
    replay_seed = _digest({"actor_record_hash": actor_record.record_hash, "predicate_hash": p_hash, "scope": [x.key for x in scope_refs]})
    predicate = EmpiricalPredicate(
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(
            AuthorityRef(grammar_binding.authority_id, grammar_binding.authority_version, grammar_binding.authority_hash),
            AuthorityRef(Q69B_COORDINATE_AUTHORITY_ID, Q69B_COORDINATE_AUTHORITY_VERSION, Q69B_COORDINATE_AUTHORITY_HASH),
        ),
        dependency_refs=coordinate_refs,
        producer_replay_locator_or_reference_root=f"urn:rawlsing:gt34:obl031:replay:{replay_seed}",
        predicate_ast=ast,
        predicate_hash=p_hash,
        grammar_authority_ref=AuthorityRef(grammar_binding.authority_id, grammar_binding.authority_version, grammar_binding.authority_hash),
        coordinate_question_value_refs=coordinate_refs,
        risk_set_refs=(), scope_refs=scope_refs,
        same_respondent_binding_semantics="EXACT_RESPONDENT_REF__Q69B_DATEINTR_NATIVE_WINDOW",
        operator_semantics_refs=grammar_binding.operator_semantics_refs,
    )
    receipt = _receipt(actor_record.record_id, actor_record.record_hash, actor_record.effective_from,
                       grammar_binding, predicate.object_id, predicate.content_hash, CURRENT_ACCEPTED)
    return ComparatorResolution(RESOLVED, predicate=predicate, receipt=receipt)


def prove_noncurrent_synthetic(*, fixture: SyntheticEncounterFixture,
                               classification_proof: OBL048ClassificationProof,
                               q69b_binding: Q69BSourceBinding,
                               grammar_binding: D08GrammarBinding,
                               respondent_windows: Sequence[RespondentDateIntrWindow]):
    if fixture.fixture_mode != NONCURRENT_SYNTHETIC_TEST_ONLY:
        return ComparatorResolution(INTEGRITY_REF_HASH_REPLAY_FAILURE)
    if fixture != SyntheticEncounterFixture.build(fixture.actor_id, fixture.effective_from):
        return ComparatorResolution(INTEGRITY_REF_HASH_REPLAY_FAILURE)
    if (fixture.authority_id, fixture.authority_version) != (ADP010_AUTHORITY_ID, ADP010_AUTHORITY_VERSION):
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED)
    if fixture.realization_state != STATE_ENCOUNTER or fixture.event_effect_kind != EFFECT_ENCOUNTER:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED)
    if fixture.subject_ref != EXACT_SUBJECT_REF:
        return ComparatorResolution(ACTOR_FACT_MISSING_OR_UNAUTHORIZED)
    if not _validate_classification(classification_proof):
        return ComparatorResolution(NONCOMPARABLE)
    if q69b_binding != Q69BSourceBinding():
        return ComparatorResolution(INTEGRITY_REF_HASH_REPLAY_FAILURE)
    grammar_error = _validate_grammar(grammar_binding, False)
    if grammar_error:
        return ComparatorResolution(grammar_error)
    temporal, included = _temporal_scope(fixture.effective_from, respondent_windows, False)
    if temporal != RESOLVED:
        return ComparatorResolution(temporal)
    ast, coordinate_refs, scope_refs = _predicate_material(included)
    p_hash = semantic_hash(ast)
    preview = SyntheticPredicatePreview(NONCURRENT_SYNTHETIC_TEST_ONLY, ast, p_hash, coordinate_refs, scope_refs, grammar_binding.operator_semantics_refs)
    preview_ref = f"urn:rawlsing:gt34:obl031:noncurrent-synthetic-predicate-preview:sha256:{_digest(asdict(preview))}"
    receipt = _receipt(f"urn:rawlsing:gt34:obl031:synthetic-encounter:{fixture.fixture_hash}", fixture.fixture_hash,
                       fixture.effective_from, grammar_binding, preview_ref, p_hash, NONCURRENT_SYNTHETIC_TEST_ONLY)
    return ComparatorResolution(NONCURRENT_SYNTHETIC_PROOF, receipt=receipt, synthetic_preview=preview)


def authority_identity():
    return AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH
