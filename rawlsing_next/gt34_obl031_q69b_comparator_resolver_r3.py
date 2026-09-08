"""GT34 OBL031 R3 successor: pin exact HQ-current OBL057 D08 grammar authority.

This module deliberately preserves the frozen R2 comparator mechanics and closes
only the D08 grammar-authority mutation seam. OBL048 remains subject
classification only; ADP-010 remains actor ENCOUNTER occurrence only; OBL057
owns predicate grammar/operator semantics only; Q69B authority owns coordinate
semantics only; OBL031 performs only the exact bounded mapping among those
already-authorized inputs.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Sequence

from rawlsing_next.pre553_empirical_objects import EmpiricalPredicate, ExactRef
from rawlsing_next import gt34_obl031_q69b_comparator_resolver_r2 as _r2

ACTOR_FACT_MISSING_OR_UNAUTHORIZED = _r2.ACTOR_FACT_MISSING_OR_UNAUTHORIZED
AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING = _r2.AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING
CURRENT_ACCEPTED = _r2.CURRENT_ACCEPTED
D08_GRAMMAR_UNRESOLVED = _r2.D08_GRAMMAR_UNRESOLVED
EMPIRICAL_COORDINATE_AUTHORITY_MISSING = _r2.EMPIRICAL_COORDINATE_AUTHORITY_MISSING
INTEGRITY_REF_HASH_REPLAY_FAILURE = _r2.INTEGRITY_REF_HASH_REPLAY_FAILURE
LAWFUL_VALID_EMPTY = _r2.LAWFUL_VALID_EMPTY
NO_EXACT_MATCH = _r2.NO_EXACT_MATCH
NONCOMPARABLE = _r2.NONCOMPARABLE
NONCURRENT_SYNTHETIC_PROOF = _r2.NONCURRENT_SYNTHETIC_PROOF
NONCURRENT_SYNTHETIC_TEST_ONLY = _r2.NONCURRENT_SYNTHETIC_TEST_ONLY
OBL048_AUTHORITY_HASH = _r2.OBL048_AUTHORITY_HASH
OBL048_PROPOSITION_HASH = _r2.OBL048_PROPOSITION_HASH
Q69B_ACCEPTED_RELEASE_HASH = _r2.Q69B_ACCEPTED_RELEASE_HASH
SOURCE_TIME_GEOGRAPHY_EQUIVALENCE_UNRESOLVED = _r2.SOURCE_TIME_GEOGRAPHY_EQUIVALENCE_UNRESOLVED
RESOLVED = _r2.RESOLVED

OBL048ClassificationProof = _r2.OBL048ClassificationProof
Q69BSourceBinding = _r2.Q69BSourceBinding
RespondentDateIntrWindow = _r2.RespondentDateIntrWindow
SyntheticEncounterFixture = _r2.SyntheticEncounterFixture
SyntheticPredicatePreview = _r2.SyntheticPredicatePreview
current_obl048_proof = _r2.current_obl048_proof

R2_HEAD = "3edf370c31682cd231bff25bafbe469a39e88c94"
R2_IMPLEMENTATION_BLOB = "5df5e1fe5459d642aa3aa7f5dc0c3c36cb3ef757"
R2_AUTHORITY_ID, R2_AUTHORITY_VERSION, R2_AUTHORITY_CONTENT_HASH = _r2.authority_identity()

D08_AUTHORITY_ID = "GT34_D08_EMPIRICAL_PREDICATE_GRAMMAR_AUTHORITY"
D08_AUTHORITY_VERSION = "1.0.0"
D08_AUTHORITY_CONTENT_HASH = "acec40d03b5602aaa553f1f63cf2506bffe0491c008678ff973e39c3f7dcedd4"
D08_AUTHORITY_KIND = "PREDICATE_GRAMMAR"
D08_GOVERNED_OPERATION = "RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE_EQ_PREDICATE"
D08_GOVERNED_OBJECT_FAMILY = "EmpiricalPredicate@1.0.0"
D08_PREDICATE_LEAF_TYPE = "EMPIRICAL_POSITION_COORDINATE"
D08_COMPARISON_OPERATOR = "EQ"
D08_HISTORICAL_SEMANTIC_COURT = "db03fcbcb5e34c28b486070628377ead0408e13a"

D08_OPERATOR_POSITION_REF = ExactRef(
    "PREDICATE_OPERATOR_SEMANTICS",
    "D08_EMPIRICAL_POSITION_COORDINATE@1.0.0",
    "53e3593784cebdd50f68f8d993786b7643ff64280b8b63efbd09bd6d6a6ae8cf",
)
D08_OPERATOR_EQ_REF = ExactRef(
    "PREDICATE_OPERATOR_SEMANTICS",
    "D08_EMPIRICAL_POSITION_COORDINATE_EQ@1.0.0",
    "4d1dd3a2514b86b5c1d633527bfa6d7ba2b0188b754d4f12c2edc89c4343dd69",
)
D08_OPERATOR_SEMANTICS_REFS = (D08_OPERATOR_POSITION_REF, D08_OPERATOR_EQ_REF)
D08_OWNER_JURISDICTION_REF = ExactRef(
    "OWNER_JURISDICTION",
    "VOZHD_HQ_PRE_MAIN:GT34_D08_EMPIRICAL_PREDICATE_GRAMMAR_ONLY",
    "900d13df2f3c8167be47be574549b8b98a1d87dc02d0f273104dbc353aa783bb",
)
D08_HQ_ADOPTION_COMMIT = "ffd580daf88cce0a3be3a87c461c165916bad9cc"
D08_HQ_ADOPTION_ARTIFACT_BLOB = "d6270869655c86729150f81fc0e11e0f82ac7a22"
D08_HQ_ADOPTION_JSON_BLOB = "1f9ce9e9019cbe6451a8a49e5e4bd893b2196755"
D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB = "ee54aa2965e13ba39b77f169170dc857b0fea6aa"
D08_CURRENT_SELECTION_STATUS = CURRENT_ACCEPTED
D08_RESOLUTION_CONTRACT = "EXACT_TUPLE_ONLY__NO_LATEST_DEFAULT_FUZZY_FALLBACK"

AUTHORITY_ID = _r2.AUTHORITY_ID
AUTHORITY_VERSION = "1.1.2"
AUTHORITY_SCHEMA = f"{AUTHORITY_ID}@{AUTHORITY_VERSION}"


def _canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(v):
    return sha256(_canon(v).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class D08GrammarBinding:
    authority_id: str
    authority_version: str
    authority_hash: str
    authority_kind: str
    governed_operation: str
    governed_object_family: str
    predicate_leaf_type: str
    comparison_operator: str
    operator_semantics_refs: tuple[ExactRef, ...]
    owner_jurisdiction_ref: ExactRef
    hq_adoption_commit: str
    hq_adoption_artifact_blob: str
    hq_adoption_json_blob: str
    hq_current_selection_receipt_blob: str
    currentness: str
    resolution_contract: str
    provenance_refs: tuple[str, ...]


def current_d08_grammar_binding() -> D08GrammarBinding:
    return D08GrammarBinding(
        authority_id=D08_AUTHORITY_ID,
        authority_version=D08_AUTHORITY_VERSION,
        authority_hash=D08_AUTHORITY_CONTENT_HASH,
        authority_kind=D08_AUTHORITY_KIND,
        governed_operation=D08_GOVERNED_OPERATION,
        governed_object_family=D08_GOVERNED_OBJECT_FAMILY,
        predicate_leaf_type=D08_PREDICATE_LEAF_TYPE,
        comparison_operator=D08_COMPARISON_OPERATOR,
        operator_semantics_refs=D08_OPERATOR_SEMANTICS_REFS,
        owner_jurisdiction_ref=D08_OWNER_JURISDICTION_REF,
        hq_adoption_commit=D08_HQ_ADOPTION_COMMIT,
        hq_adoption_artifact_blob=D08_HQ_ADOPTION_ARTIFACT_BLOB,
        hq_adoption_json_blob=D08_HQ_ADOPTION_JSON_BLOB,
        hq_current_selection_receipt_blob=D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB,
        currentness=D08_CURRENT_SELECTION_STATUS,
        resolution_contract=D08_RESOLUTION_CONTRACT,
        provenance_refs=(
            f"HQ_OBL057_ADOPTION_COMMIT:{D08_HQ_ADOPTION_COMMIT}",
            f"HQ_OBL057_ADOPTION_ARTIFACT_BLOB:{D08_HQ_ADOPTION_ARTIFACT_BLOB}",
            f"HQ_OBL057_ADOPTION_JSON_BLOB:{D08_HQ_ADOPTION_JSON_BLOB}",
            f"HQ_OBL057_CURRENT_SELECTION_RECEIPT_BLOB:{D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB}",
            f"HISTORICAL_D08_SEMANTIC_COURT_ONLY:{D08_HISTORICAL_SEMANTIC_COURT}",
        ),
    )


D08_CURRENT_BINDING = current_d08_grammar_binding()

AUTHORITY_MATERIAL = {
    "schema": AUTHORITY_SCHEMA,
    "predecessor": {
        "head": R2_HEAD,
        "implementation_blob": R2_IMPLEMENTATION_BLOB,
        "authority": [R2_AUTHORITY_ID, R2_AUTHORITY_VERSION, R2_AUTHORITY_CONTENT_HASH],
    },
    "repair_grain": "PIN_EXACT_HQ_CURRENT_OBL057_D08_GRAMMAR_AUTHORITY_ONLY",
    "d08_current_binding": {
        "authority": [D08_AUTHORITY_ID, D08_AUTHORITY_VERSION, D08_AUTHORITY_CONTENT_HASH],
        "kind": D08_AUTHORITY_KIND,
        "operation": D08_GOVERNED_OPERATION,
        "family": D08_GOVERNED_OBJECT_FAMILY,
        "leaf": D08_PREDICATE_LEAF_TYPE,
        "operator": D08_COMPARISON_OPERATOR,
        "operator_semantics_refs": [r.as_dict() for r in D08_OPERATOR_SEMANTICS_REFS],
        "owner_jurisdiction_ref": D08_OWNER_JURISDICTION_REF.as_dict(),
        "hq_adoption_commit": D08_HQ_ADOPTION_COMMIT,
        "hq_adoption_artifact_blob": D08_HQ_ADOPTION_ARTIFACT_BLOB,
        "hq_adoption_json_blob": D08_HQ_ADOPTION_JSON_BLOB,
        "hq_current_selection_receipt_blob": D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB,
        "currentness": D08_CURRENT_SELECTION_STATUS,
        "resolution_contract": D08_RESOLUTION_CONTRACT,
    },
    "owner_split": {
        "OBL048": "SUBJECT_CLASSIFICATION_ONLY",
        "ADP010": "ACTUAL_ACTOR_ENCOUNTER_OCCURRENCE_ONLY",
        "OBL057": "D08_PREDICATE_GRAMMAR_OPERATOR_SEMANTICS_ONLY",
        "Q69B": "Q69B_COORDINATE_SEMANTICS_ONLY",
        "OBL031": "EXACT_BOUNDED_MAPPING_AMONG_ALREADY_AUTHORIZED_INPUTS_ONLY",
    },
    "real_first_canary_actor_encounter": "ABSENT__CURRENT_INVOCATION_MUST_FAIL_CLOSED",
    "positive_mechanics": "NONCURRENT_SYNTHETIC_TEST_ONLY",
}
AUTHORITY_CONTENT_HASH = _digest(AUTHORITY_MATERIAL)


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
    d08_hq_selection_closure: tuple[str, ...]
    resulting_predicate_ref: str
    resulting_predicate_hash: str
    predecessor_r2_receipt_hash: str
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


def _validate_grammar(binding: D08GrammarBinding | None) -> str | None:
    if binding is None:
        return D08_GRAMMAR_UNRESOLVED
    if binding != D08_CURRENT_BINDING:
        return D08_GRAMMAR_UNRESOLVED
    return None


def _to_r2(binding: D08GrammarBinding, *, synthetic: bool) -> _r2.D08GrammarBinding:
    return _r2.D08GrammarBinding(
        authority_id=binding.authority_id,
        authority_version=binding.authority_version,
        authority_hash=binding.authority_hash,
        authority_kind=binding.authority_kind,
        governed_operation=binding.governed_operation,
        governed_object_family=binding.governed_object_family,
        operator_semantics_refs=binding.operator_semantics_refs,
        currentness=NONCURRENT_SYNTHETIC_TEST_ONLY if synthetic else CURRENT_ACCEPTED,
        provenance_refs=binding.provenance_refs,
    )


def _selection_closure(binding: D08GrammarBinding) -> tuple[str, ...]:
    return (
        binding.authority_id,
        binding.authority_version,
        binding.authority_hash,
        binding.authority_kind,
        binding.governed_operation,
        binding.governed_object_family,
        binding.predicate_leaf_type,
        binding.comparison_operator,
        *(r.key for r in binding.operator_semantics_refs),
        binding.owner_jurisdiction_ref.key,
        binding.hq_adoption_commit,
        binding.hq_adoption_artifact_blob,
        binding.hq_adoption_json_blob,
        binding.hq_current_selection_receipt_blob,
        binding.currentness,
        binding.resolution_contract,
        *binding.provenance_refs,
    )


def _wrap_receipt(r: _r2.ComparatorProvenanceReceipt, binding: D08GrammarBinding) -> ComparatorProvenanceReceipt:
    closure = _selection_closure(binding)
    core = {
        "authority_id": AUTHORITY_ID,
        "authority_version": AUTHORITY_VERSION,
        "authority_content_hash": AUTHORITY_CONTENT_HASH,
        "actor_fact_ref": r.actor_fact_ref,
        "actor_fact_hash": r.actor_fact_hash,
        "actor_semantic_owner_authority": r.actor_semantic_owner_authority,
        "actor_effective_time": r.actor_effective_time,
        "subject_ref": r.subject_ref,
        "obl048_authority_hash": r.obl048_authority_hash,
        "obl048_proposition_hash": r.obl048_proposition_hash,
        "source_release_scope": r.source_release_scope,
        "empirical_coordinate_refs": r.empirical_coordinate_refs,
        "comparator_rule_identity": (AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH),
        "equivalence_crosswalk_time_geography_authorities": r.equivalence_crosswalk_time_geography_authorities,
        "d08_grammar_authority": (binding.authority_id, binding.authority_version, binding.authority_hash),
        "d08_hq_selection_closure": closure,
        "resulting_predicate_ref": r.resulting_predicate_ref,
        "resulting_predicate_hash": r.resulting_predicate_hash,
        "predecessor_r2_receipt_hash": r.receipt_hash,
        "currentness": r.currentness,
    }
    replay = _digest({"predecessor_r2_replay": r.deterministic_replay_identity, "r3_core": core})
    with_replay = {**core, "deterministic_replay_identity": replay}
    return ComparatorProvenanceReceipt(**with_replay, receipt_hash=_digest(with_replay))


def _wrap_result(result: _r2.ComparatorResolution, binding: D08GrammarBinding | None) -> ComparatorResolution:
    receipt = None
    if result.receipt is not None:
        assert binding is not None
        receipt = _wrap_receipt(result.receipt, binding)
    return ComparatorResolution(
        outcome=result.outcome,
        predicate=result.predicate,
        receipt=receipt,
        synthetic_preview=result.synthetic_preview,
        detail=result.detail,
    )


def resolve_current(*, actor_record, expected_actor_id: str,
                    classification_proof: OBL048ClassificationProof,
                    q69b_binding: Q69BSourceBinding,
                    grammar_binding: D08GrammarBinding | None,
                    respondent_windows: Sequence[RespondentDateIntrWindow]):
    if actor_record is None:
        return _wrap_result(_r2.resolve_current(
            actor_record=None,
            expected_actor_id=expected_actor_id,
            classification_proof=classification_proof,
            q69b_binding=q69b_binding,
            grammar_binding=None,
            respondent_windows=respondent_windows,
        ), None)
    grammar_error = _validate_grammar(grammar_binding)
    if grammar_error:
        return ComparatorResolution(grammar_error, detail="exact HQ-current OBL057 D08 grammar binding unresolved")
    assert grammar_binding is not None
    result = _r2.resolve_current(
        actor_record=actor_record,
        expected_actor_id=expected_actor_id,
        classification_proof=classification_proof,
        q69b_binding=q69b_binding,
        grammar_binding=_to_r2(grammar_binding, synthetic=False),
        respondent_windows=respondent_windows,
    )
    return _wrap_result(result, grammar_binding)


def prove_noncurrent_synthetic(*, fixture: SyntheticEncounterFixture,
                               classification_proof: OBL048ClassificationProof,
                               q69b_binding: Q69BSourceBinding,
                               grammar_binding: D08GrammarBinding | None,
                               respondent_windows: Sequence[RespondentDateIntrWindow]):
    grammar_error = _validate_grammar(grammar_binding)
    if grammar_error:
        return ComparatorResolution(grammar_error, detail="exact HQ-current OBL057 D08 grammar binding unresolved")
    assert grammar_binding is not None
    result = _r2.prove_noncurrent_synthetic(
        fixture=fixture,
        classification_proof=classification_proof,
        q69b_binding=q69b_binding,
        grammar_binding=_to_r2(grammar_binding, synthetic=True),
        respondent_windows=respondent_windows,
    )
    return _wrap_result(result, grammar_binding)


def authority_identity():
    return AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH
