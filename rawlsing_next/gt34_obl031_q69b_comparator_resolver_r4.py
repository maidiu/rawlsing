"""GT34 OBL031 R4: exact-type closure over the R3 OBL057 grammar binding.

R4 changes one grain only: before any nonmissing current actor input or any
synthetic positive mechanics reaches R3/R2, the grammar binding must be the
exact frozen D08GrammarBinding type and equal the one canonical HQ-current
OBL057 binding. This closes the hostile equality-spoof/type-confusion seam.
"""
from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
import json

from rawlsing_next import gt34_obl031_q69b_comparator_resolver_r3 as _r3

ACTOR_FACT_MISSING_OR_UNAUTHORIZED = _r3.ACTOR_FACT_MISSING_OR_UNAUTHORIZED
CURRENT_ACCEPTED = _r3.CURRENT_ACCEPTED
D08_GRAMMAR_UNRESOLVED = _r3.D08_GRAMMAR_UNRESOLVED
NONCURRENT_SYNTHETIC_PROOF = _r3.NONCURRENT_SYNTHETIC_PROOF
NONCURRENT_SYNTHETIC_TEST_ONLY = _r3.NONCURRENT_SYNTHETIC_TEST_ONLY
Q69BSourceBinding = _r3.Q69BSourceBinding
RespondentDateIntrWindow = _r3.RespondentDateIntrWindow
SyntheticEncounterFixture = _r3.SyntheticEncounterFixture
D08GrammarBinding = _r3.D08GrammarBinding
current_obl048_proof = _r3.current_obl048_proof
current_d08_grammar_binding = _r3.current_d08_grammar_binding

D08_AUTHORITY_ID = _r3.D08_AUTHORITY_ID
D08_AUTHORITY_VERSION = _r3.D08_AUTHORITY_VERSION
D08_AUTHORITY_CONTENT_HASH = _r3.D08_AUTHORITY_CONTENT_HASH
D08_AUTHORITY_KIND = _r3.D08_AUTHORITY_KIND
D08_GOVERNED_OPERATION = _r3.D08_GOVERNED_OPERATION
D08_GOVERNED_OBJECT_FAMILY = _r3.D08_GOVERNED_OBJECT_FAMILY
D08_PREDICATE_LEAF_TYPE = _r3.D08_PREDICATE_LEAF_TYPE
D08_COMPARISON_OPERATOR = _r3.D08_COMPARISON_OPERATOR
D08_OPERATOR_SEMANTICS_REFS = _r3.D08_OPERATOR_SEMANTICS_REFS
D08_HQ_ADOPTION_COMMIT = _r3.D08_HQ_ADOPTION_COMMIT
D08_HQ_ADOPTION_ARTIFACT_BLOB = _r3.D08_HQ_ADOPTION_ARTIFACT_BLOB
D08_HQ_ADOPTION_JSON_BLOB = _r3.D08_HQ_ADOPTION_JSON_BLOB
D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB = _r3.D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB
D08_RESOLUTION_CONTRACT = _r3.D08_RESOLUTION_CONTRACT

R3_SEMANTIC_CANDIDATE = "b7ccad935e7f5f2906390495d9d1a6ecabae618f"
R3_EVIDENCE_EXECUTION = "842ef28c2ce93584a6c78e870d29e8c23e5803db"
R3_HOSTILE_MATRIX_FREEZE = "881c2c509dbcb23836b9bbb66c10348d21bbd75b"
R3_HOSTILE_EVIDENCE_EXECUTION = "a96ae6844e2c630d08b9f605cfb1a67f12d31daa"
R3_HOSTILE_RUN = 34193702341
R3_HOSTILE_JOB = 101956805489

AUTHORITY_ID = _r3.AUTHORITY_ID
AUTHORITY_VERSION = "1.1.3"
AUTHORITY_SCHEMA = f"{AUTHORITY_ID}@{AUTHORITY_VERSION}"


def _canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(v):
    return sha256(_canon(v).encode("utf-8")).hexdigest()


AUTHORITY_MATERIAL = {
    "schema": AUTHORITY_SCHEMA,
    "predecessor_authority": list(_r3.authority_identity()),
    "predecessor_semantic_candidate": R3_SEMANTIC_CANDIDATE,
    "failed_hostile": {
        "matrix_freeze": R3_HOSTILE_MATRIX_FREEZE,
        "evidence_execution": R3_HOSTILE_EVIDENCE_EXECUTION,
        "run": R3_HOSTILE_RUN,
        "job": R3_HOSTILE_JOB,
        "defect": "EQUALITY_SPOOF_TYPE_CONFUSION_COULD_BYPASS_CANONICAL_D08_BINDING",
    },
    "repair_grain": "EXACT_FROZEN_D08GrammarBinding_TYPE_AND_VALUE_ONLY",
    "exact_d08_authority": [D08_AUTHORITY_ID, D08_AUTHORITY_VERSION, D08_AUTHORITY_CONTENT_HASH],
    "exact_hq_selection": [
        D08_HQ_ADOPTION_COMMIT,
        D08_HQ_ADOPTION_ARTIFACT_BLOB,
        D08_HQ_ADOPTION_JSON_BLOB,
        D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB,
    ],
    "resolution_contract": D08_RESOLUTION_CONTRACT,
    "owner_split_unchanged": True,
    "real_first_canary_actor_encounter": "ABSENT__CURRENT_INVOCATION_MUST_FAIL_CLOSED",
    "positive_mechanics": NONCURRENT_SYNTHETIC_TEST_ONLY,
}
AUTHORITY_CONTENT_HASH = _digest(AUTHORITY_MATERIAL)


def _strict_exact_grammar(binding) -> bool:
    return type(binding) is D08GrammarBinding and binding == current_d08_grammar_binding()


def _reseal(result):
    if result.receipt is None:
        return result
    r = result.receipt
    identity = authority_identity()
    replay = _digest({
        "r3_replay": r.deterministic_replay_identity,
        "r4_authority": identity,
        "strict_type_contract": "EXACT_FROZEN_D08GrammarBinding_TYPE_AND_VALUE_ONLY",
    })
    provisional = replace(
        r,
        authority_id=AUTHORITY_ID,
        authority_version=AUTHORITY_VERSION,
        authority_content_hash=AUTHORITY_CONTENT_HASH,
        comparator_rule_identity=identity,
        deterministic_replay_identity=replay,
        receipt_hash="0" * 64,
    )
    receipt_hash = _digest({
        "authority_id": provisional.authority_id,
        "authority_version": provisional.authority_version,
        "authority_content_hash": provisional.authority_content_hash,
        "actor_fact_ref": provisional.actor_fact_ref,
        "actor_fact_hash": provisional.actor_fact_hash,
        "actor_semantic_owner_authority": provisional.actor_semantic_owner_authority,
        "actor_effective_time": provisional.actor_effective_time,
        "subject_ref": provisional.subject_ref,
        "obl048_authority_hash": provisional.obl048_authority_hash,
        "obl048_proposition_hash": provisional.obl048_proposition_hash,
        "source_release_scope": provisional.source_release_scope,
        "empirical_coordinate_refs": provisional.empirical_coordinate_refs,
        "comparator_rule_identity": provisional.comparator_rule_identity,
        "equivalence_crosswalk_time_geography_authorities": provisional.equivalence_crosswalk_time_geography_authorities,
        "d08_grammar_authority": provisional.d08_grammar_authority,
        "d08_hq_selection_closure": provisional.d08_hq_selection_closure,
        "resulting_predicate_ref": provisional.resulting_predicate_ref,
        "resulting_predicate_hash": provisional.resulting_predicate_hash,
        "predecessor_r2_receipt_hash": provisional.predecessor_r2_receipt_hash,
        "deterministic_replay_identity": provisional.deterministic_replay_identity,
        "currentness": provisional.currentness,
    })
    return replace(result, receipt=replace(provisional, receipt_hash=receipt_hash))


def resolve_current(*, actor_record, expected_actor_id, classification_proof,
                    q69b_binding, grammar_binding, respondent_windows):
    # Preserve the mandated current real first-canary negative before grammar.
    if actor_record is None:
        return _r3.resolve_current(
            actor_record=None,
            expected_actor_id=expected_actor_id,
            classification_proof=classification_proof,
            q69b_binding=q69b_binding,
            grammar_binding=None,
            respondent_windows=respondent_windows,
        )
    if not _strict_exact_grammar(grammar_binding):
        return _r3.ComparatorResolution(
            D08_GRAMMAR_UNRESOLVED,
            detail="exact frozen HQ-current OBL057 D08 grammar binding type/value unresolved",
        )
    return _reseal(_r3.resolve_current(
        actor_record=actor_record,
        expected_actor_id=expected_actor_id,
        classification_proof=classification_proof,
        q69b_binding=q69b_binding,
        grammar_binding=grammar_binding,
        respondent_windows=respondent_windows,
    ))


def prove_noncurrent_synthetic(*, fixture, classification_proof, q69b_binding,
                               grammar_binding, respondent_windows):
    if not _strict_exact_grammar(grammar_binding):
        return _r3.ComparatorResolution(
            D08_GRAMMAR_UNRESOLVED,
            detail="exact frozen HQ-current OBL057 D08 grammar binding type/value unresolved",
        )
    return _reseal(_r3.prove_noncurrent_synthetic(
        fixture=fixture,
        classification_proof=classification_proof,
        q69b_binding=q69b_binding,
        grammar_binding=grammar_binding,
        respondent_windows=respondent_windows,
    ))


def authority_identity():
    return AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH
