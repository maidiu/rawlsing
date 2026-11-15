from dataclasses import replace
import hashlib
import inspect
import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next import wave1_ff_prev3_relation_admission as adm


def h(seed: str) -> str:
    return hashlib.sha256(seed.encode()).hexdigest()


def ref(kind: str, object_id: str, seed: str) -> ExactRef:
    return ExactRef(kind, object_id, h(seed))


def auth(seed: str = "relation-auth") -> AuthorityRef:
    return AuthorityRef("FF_REL_AUTH", "R1", h(seed))


def base_rule():
    relation_rule = ref("FIELD_FORGE_RELATION_RULE", adm.GT2_RELATION_FAMILY, "relation-rule")
    conditioner = ref("QUESTION_PARTICIPANT", adm.GT2_CONDITIONER, "q86b")
    target = ref("QUESTION_PARTICIPANT", adm.GT2_TARGET, "q86a")
    return adm.make_gt2_relation_admission_rule(
        allowed_relation_rule_ref=relation_rule,
        condition_participant_ref=conditioner,
        target_participant_ref=target,
    )


def relation(*, state="SUPPORTED", permissions=(adm.GT2_TARGET_USE,), negatives=(), rule=None, **overrides):
    rule = rule or base_rule()
    kwargs = dict(
        relation_ref=ref("FIELD_FORGE_EXACT_RELATION", "gt2:conditional-support", "relation-instance"),
        relation_content_hash_echo=h("relation-instance"),
        relation_family=adm.GT2_RELATION_FAMILY,
        relation_owner=adm.GT2_RELATION_OWNER,
        relation_rule_ref=rule.allowed_relation_rule_ref,
        relation_rule_content_hash_echo=rule.allowed_relation_rule_ref.content_hash,
        relation_typed_state=state,
        source_artifact_ref=rule.required_source_artifact_ref,
        source_family=adm.GT2_SOURCE_FAMILY,
        source_wave=adm.GT2_SOURCE_WAVE,
        risk_set_ref=rule.required_risk_set_ref,
        risk_set_row_count=adm.GT2_RISK_SET_ROWS,
        participants=rule.required_participants,
        relation_permission_ceiling=permissions,
        relation_authority_refs=(auth(),),
        relation_current_selection_refs=(ref("CURRENT_SELECTION", "ff-relation-current", "current"),),
        relation_semantic_identity_refs=(ref("RELATION_SEMANTIC_IDENTITY", "conditional-support", "sem"),),
        native_scope_identity_refs=(ref("SCOPE", "r5-common-risk-set", "scope"),),
        source_universe_refs=(ref("EMPIRICAL_UNIVERSE", "afrobarometer-r5", "universe"),),
        relation_dependency_refs=(ref("EMPIRICAL_FACT", "gt2-joint-fact", "joint-fact"),),
        relation_negative_or_limit_refs=negatives,
        relation_information_loss_declaration=adm.ADMISSION_LOCAL_INFORMATION_LOSS,
        relation_replay_root=ref("REPLAY_ROOT", "gt2-relation", "replay"),
    )
    kwargs.update(overrides)
    return adm.FieldForgeRelationEvidence(**kwargs), rule


def evaluate(rel, rule, **request_overrides):
    return adm.evaluate_gt2_relation_admission(
        adm.RelationAdmissionRequest(rel, **request_overrides), rule
    )


def test_positive_gt2_admission_is_exact_and_narrow():
    rel, rule = relation()
    receipt = evaluate(rel, rule)
    assert receipt.decision is adm.AdmissionDecision.ADMITTED
    assert receipt.is_positive
    assert receipt.target_use == adm.GT2_TARGET_USE
    assert receipt.target_use_permissions == (adm.GT2_TARGET_USE,)
    assert set(receipt.target_use_permissions).issubset(set(rel.relation_permission_ceiling))
    assert receipt.relation_ref == rel.relation_ref
    assert receipt.relation_typed_state == "SUPPORTED"
    assert receipt.admission_information_loss_declaration == "NONE__REFERENCE_PRESERVING"
    assert receipt.material()["semantic_ceiling"]["empirical_fact_created"] is False
    assert receipt.material()["semantic_ceiling"]["structural_empirical_admission_created"] is False
    assert receipt.material()["semantic_ceiling"]["actor_inference_allowed"] is False


def test_observed_zero_is_nonpositive_even_without_blocker_refs():
    rel, rule = relation(state="OBSERVED_ZERO", negatives=())
    receipt = evaluate(rel, rule)
    assert adm.POSITIVE_RELATION_STATES == frozenset({"SUPPORTED"})
    assert receipt.decision is adm.AdmissionDecision.UNRESOLVED
    assert receipt.reason_code == "UPSTREAM_RELATION_OBSERVED_ZERO"
    assert receipt.relation_typed_state == "OBSERVED_ZERO"
    assert receipt.target_use_permissions == ()
    assert receipt.applicable_negative_denial_noncomparability_refs == ()


@pytest.mark.parametrize(
    "state,expected",
    [
        ("VALID_EMPTY", adm.AdmissionDecision.VALID_EMPTY),
        ("ZERO_DENOMINATOR_ABSTENTION", adm.AdmissionDecision.VALID_EMPTY),
        ("UNDEFINED_FOR_OBJECT", adm.AdmissionDecision.OUT_OF_SCOPE),
        ("OUT_OF_SCOPE", adm.AdmissionDecision.OUT_OF_SCOPE),
        ("DENIED", adm.AdmissionDecision.DENIED),
        ("MISSING_AUTHORITY", adm.AdmissionDecision.MISSING_AUTHORITY),
        ("UNRESOLVED_AUTHORITY", adm.AdmissionDecision.MISSING_AUTHORITY),
        ("UNRESOLVED", adm.AdmissionDecision.UNRESOLVED),
        ("NONCOMPARABLE", adm.AdmissionDecision.NONCOMPARABLE),
        ("NO_TRANSPORT", adm.AdmissionDecision.NONCOMPARABLE),
        ("BLOCKED_EXPLICIT_AUTHORITY", adm.AdmissionDecision.BLOCKED_EXPLICIT_AUTHORITY),
        ("OBSERVABILITY_LIMIT", adm.AdmissionDecision.OBSERVABILITY_LIMIT),
        ("INTEGRITY_FAILURE", adm.AdmissionDecision.INTEGRITY_FAILURE),
    ],
)
def test_upstream_typed_negative_is_preserved_without_positive_permission(state, expected):
    rel, rule = relation(state=state)
    receipt = evaluate(rel, rule)
    assert receipt.decision is expected
    assert receipt.relation_typed_state == state
    assert receipt.target_use_permissions == ()


def test_target_use_mismatch_fails_closed():
    rel, rule = relation()
    receipt = evaluate(rel, rule, target_use="OTHER_USE")
    assert receipt.decision is adm.AdmissionDecision.OUT_OF_SCOPE
    assert receipt.reason_code == "TARGET_USE_MISMATCH"
    assert receipt.target_use_permissions == ()


def test_downstream_contract_mismatch_fails_closed():
    rel, rule = relation()
    receipt = evaluate(rel, rule, downstream_contract="OTHER_CONTRACT")
    assert receipt.decision is adm.AdmissionDecision.OUT_OF_SCOPE
    assert receipt.reason_code == "DOWNSTREAM_CONTRACT_MISMATCH"


def test_missing_relation_permission_denies():
    rel, rule = relation(permissions=("REFERENCE_ONLY",))
    receipt = evaluate(rel, rule)
    assert receipt.decision is adm.AdmissionDecision.DENIED
    assert receipt.reason_code == "TARGET_USE_NOT_PERMITTED_BY_RELATION"


def test_rule_cannot_grant_general_prev3_permission():
    rule = base_rule()
    with pytest.raises(adm.RelationAdmissionError):
        replace(rule, output_permission_subset=(adm.GT2_TARGET_USE, "GENERAL_PREV3"))


def test_rule_cannot_reclassify_observed_zero_as_positive():
    rule = base_rule()
    with pytest.raises(adm.RelationAdmissionError, match="genuinely positive"):
        replace(rule, allowed_relation_states=("SUPPORTED", "OBSERVED_ZERO"))


def test_relation_rule_tamper_is_integrity_failure():
    rel, rule = relation()
    other = ref("FIELD_FORGE_RELATION_RULE", "other", "other-rule")
    tampered = replace(rel, relation_rule_ref=other, relation_rule_content_hash_echo=other.content_hash)
    receipt = evaluate(tampered, rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "RELATION_RULE_REF_MISMATCH"


def test_risk_set_tamper_is_integrity_failure():
    rel, rule = relation(risk_set_row_count=adm.GT2_RISK_SET_ROWS - 1)
    receipt = evaluate(rel, rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "RISK_SET_ROW_COUNT_MISMATCH"


def test_participant_role_order_tamper_is_integrity_failure():
    rel, rule = relation()
    conditioner, target = rel.participants
    tampered = replace(rel, participants=(replace(target, ordinal=0), replace(conditioner, ordinal=1)))
    receipt = evaluate(tampered, rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "PARTICIPANT_ROLE_ORDER_IDENTITY_MISMATCH"


def test_information_loss_cannot_be_improved_or_rewritten():
    rel, rule = relation(relation_information_loss_declaration="LOSSY_COUNT_ONLY")
    receipt = evaluate(rel, rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "RELATION_INFORMATION_LOSS_MISMATCH"


def test_upstream_negative_refs_block_even_supported_relation():
    rel, rule = relation(negatives=(ref("NEGATIVE_LIMIT", "limit", "limit"),))
    receipt = evaluate(rel, rule)
    assert receipt.decision is adm.AdmissionDecision.UNRESOLVED
    assert receipt.target_use_permissions == ()
    assert receipt.applicable_negative_denial_noncomparability_refs == rel.relation_negative_or_limit_refs


def test_supported_without_required_positive_authority_closure_does_not_admit():
    rel, rule = relation(state="SUPPORTED")
    tampered = replace(rel, relation_authority_refs=())
    receipt = evaluate(tampered, rule)
    assert receipt.decision is adm.AdmissionDecision.MISSING_AUTHORITY
    assert receipt.reason_code == "UPSTREAM_RELATION_AUTHORITY_OR_CURRENT_SELECTION_MISSING"
    assert receipt.target_use_permissions == ()


def test_admission_authority_denial_is_typed_and_zero_permission():
    rel, rule = relation()
    denied_rule = replace(rule, authority_binding=replace(rule.authority_binding, decision_state="DENY"))
    receipt = evaluate(rel, denied_rule)
    assert receipt.decision is adm.AdmissionDecision.DENIED
    assert receipt.reason_code == "ADMISSION_AUTHORITY_DENIED"
    assert receipt.target_use_permissions == ()


def test_deterministic_receipt_and_historical_replay():
    rel, rule = relation()
    first = evaluate(rel, rule)
    second = evaluate(rel, rule)
    assert first.ref == second.ref
    replayed = adm.replay_gt2_relation_admission(relation=rel, rule=rule, historical_receipt=first)
    assert replayed.ref == first.ref


def test_historical_replay_rejects_authority_tamper():
    rel, rule = relation()
    receipt = evaluate(rel, rule)
    tampered = replace(receipt, historical_authority_material_hash=h("tampered"))
    with pytest.raises(adm.RelationAdmissionReplayError):
        adm.replay_gt2_relation_admission(relation=rel, rule=rule, historical_receipt=tampered)


def test_no_coercion_or_duck_typed_relation_input():
    class EmpiricalFact:
        pass
    with pytest.raises(adm.RelationAdmissionTypeError):
        adm.RelationAdmissionRequest(EmpiricalFact())
    with pytest.raises(adm.RelationAdmissionTypeError):
        adm.evaluate_gt2_relation_admission(object(), base_rule())


def test_module_does_not_import_or_call_i04_p06():
    source = inspect.getsource(adm)
    assert "pre553_structural_admission" not in source
    assert "evaluate_structural_empirical_admission" not in source
    assert "M1_BASIS_KIND" not in source


def test_frozen_authority_and_rule_identity_are_deterministic():
    assert adm.frozen_gt2_admission_authority_binding() == adm.frozen_gt2_admission_authority_binding()
    first = base_rule()
    second = base_rule()
    assert first.ref == second.ref
    assert first.authority_binding.frozen_contract_commit == adm.FROZEN_CANARY_COMMIT
    assert first.authority_binding.central_fanin_commit == adm.WAVE1_CENTRAL_FANIN_COMMIT


def test_relation_content_hash_echo_mismatch_is_rejected_before_admission():
    rel, _ = relation()
    with pytest.raises(adm.RelationAdmissionError):
        replace(rel, relation_content_hash_echo=h("not-the-relation"))


def test_relation_rule_hash_echo_mismatch_is_rejected_before_admission():
    rel, _ = relation()
    with pytest.raises(adm.RelationAdmissionError):
        replace(rel, relation_rule_content_hash_echo=h("not-the-rule"))


def test_source_artifact_hash_tamper_is_integrity_failure():
    bad_source = ExactRef("SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, h("other-source"))
    rel, rule = relation(source_artifact_ref=bad_source)
    receipt = evaluate(rel, rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "SOURCE_ARTIFACT_IDENTITY_MISMATCH"
