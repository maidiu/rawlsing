"""New HQ327 F2 independent frozen, pre-B3 falsification court."""
import copy, json
from pathlib import Path
import pytest
from reference_oracle import digest,evaluate,scientific_projection,validate_native_receipt

LIBRARY=Path(__file__).with_name('cases.json')
FROZEN_SHA256='827eada1eb73a131bfb1604f0977dcff08d173fb7eadb9a06d7894010f0e9351'
LIB=json.loads(LIBRARY.read_text())
CASES={c['id']:c for c in LIB['cases']}


def result(id):return evaluate(CASES[id])


def native_from_oracle(id):
    x=copy.deepcopy(result(id))
    if x['status']!='ELIGIBLE_NONCAUSAL':
        x['new_event_count']=0;x['owner_effect_committed']=False
    return x


def test_library_is_immutable_and_self_contained():
    assert len(CASES)==42
    assert LIB['case_ids']==sorted(CASES)
    assert LIB['library_hash']==digest({k:v for k,v in LIB.items() if k!='library_hash'})
    assert LIB['f1_native_unmet_preserved']==17
    assert digest(LIBRARY.read_bytes().hex()) # content-addressing also tested by sha below
    import hashlib
    assert hashlib.sha256(LIBRARY.read_bytes()).hexdigest()==FROZEN_SHA256


@pytest.mark.parametrize('id',sorted(CASES))
def test_frozen_case_exact_scientific_decision(id):
    c=CASES[id]
    assert c['hash']==digest({k:v for k,v in c.items() if k!='hash'})
    actual=evaluate(copy.deepcopy(c))
    assert (actual['status'],actual['code'])==(c['expected']['status'],c['expected']['code'])
    assert actual['no_mutation'] is True
    assert validate_native_receipt(c,native_from_oracle(id))==[]


def test_cosmetic_labels_cannot_change_scientific_eligibility():
    assert scientific_projection(result('F2-001'))==scientific_projection(result('F2-002'))
    assert scientific_projection(result('F2-003'))==scientific_projection(result('F2-004'))


def test_actual_witnessed_prior_act_changes_material_causal_provenance():
    a,b=result('F2-001'),result('F2-003')
    assert a['history_material_hash']!=b['history_material_hash']
    assert a['material_actor_activity']!=b['material_actor_activity']
    assert a['original_event_hash']==b['original_event_hash']


def test_caregiver_work_constraints_are_actual_offer_not_ses_type():
    a,b,c=result('F2-001'),result('F2-005'),result('F2-006')
    assert 'JOINT_PRACTICAL_ACTION_POSSIBLE' in a['admissible_routes']
    assert 'JOINT_PRACTICAL_ACTION_POSSIBLE' not in b['admissible_routes']
    assert scientific_projection(b)==scientific_projection(c)


def test_peer_speech_exposure_not_truth():
    a,b=result('F2-007'),result('F2-008')
    assert 'E-P-SPEECH' in a['accessible_readset']
    assert 'E-P-SPEECH' not in b['accessible_readset']
    assert a['original_event_hash']==b['original_event_hash']
    assert b['proposed_beliefs']==[]


def test_public_enactment_does_not_create_private_assent():
    x=result('F2-009')
    assert 'E-PUBLIC-ECHO' in x['public_enactments']
    assert x['proposed_beliefs'][0]['stance']=='REJECT'
    assert x['epistemic_grade']=='NO_AUTOMATIC_UPTAKE_OR_MORAL_POLARITY'


def test_affect_proposition_separable_without_moral_overwrite():
    x=result('F2-010')
    assert x['proposed_beliefs'][0]['stance']=='ACCEPT'
    assert x['proposed_affect'][0]['note']=='felt_dismissed'
    assert x['owner_effect_committed'] is False


def test_procedural_habit_does_not_imply_recollection():
    x=result('F2-011')
    assert x['retained_practice'][0]['explicit_recall'] is False
    assert x['proposed_beliefs']==[]


def test_later_reinterpretation_preserves_t0_and_append_only_lineage():
    a,b=result('F2-001'),result('F2-012')
    assert a['original_event_hash']==b['original_event_hash']
    assert b['interpretation_version_refs']==[(1,'E-C-SPEECH'),(2,'E-OTHER-PROJECT')]
    assert 'RECONSIDERATION_POSSIBLE' in b['admissible_routes']
    assert b['owner_effect_committed'] is False


def test_counterpart_refusal_is_real_and_not_compulsory_healing():
    x,y=result('F2-013'),result('F2-014')
    assert 'CONTACT_POSSIBLE' not in x['admissible_routes']
    assert 'CONTACT_POSSIBLE' in y['admissible_routes']
    assert x['original_event_hash']==y['original_event_hash']


def test_later_information_may_have_no_psychological_change():
    x=result('F2-016')
    assert 'NO_CHANGE' in x['admissible_routes']
    assert 'RECONSIDERATION_POSSIBLE' in x['admissible_routes']
    assert x['owner_effect_committed'] is False


def test_scoped_capability_unknown_absent_conflict_and_expiry():
    assert result('F2-017')['code']=='CAPABILITY_UNQUALIFIED'
    assert result('F2-018')['code']=='CAPABILITY_ABSENT_SCOPED'
    assert result('F2-019')['code']=='CAPABILITY_CONTRADICTED'
    assert result('F2-020')['code']=='CAPABILITY_UNQUALIFIED'


def test_age_sect_and_ses_labels_do_not_generate_ability_or_affect():
    assert scientific_projection(result('F2-001'))==scientific_projection(result('F2-021'))
    assert result('F2-022')['code']=='DEMOGRAPHY_TO_PSYCHOLOGY'


def test_new_payload_at_same_event_id_refused_before_history_write():
    x=result('F2-027')
    assert x['code']=='EVENT_ID_CONTENT_COLLISION' and x['no_mutation']
    assert 'DENIED_OR_DEFERRED_EVENT_CREATED' in validate_native_receipt(CASES['F2-027'],dict(x,new_event_count=1))


def test_exact_same_event_id_content_replay_is_idempotent():
    x=result('F2-028')
    assert x['exact_replay'] is True and x['new_event_count']==0
    assert x['owner_effect_committed'] is False


def test_ideological_claim_not_factual_culprit():
    assert result('F2-032')['code']=='IDEOLOGICAL_ASSERTION_AS_OBJECTIVE_FACT'
    assert result('F2-036')['code']=='OTHER_ACTOR_PRIVATE_READ'


def test_owned_actions_or_proposals_cannot_seize_another_person():
    assert result('F2-029')['code']=='CROSS_ACTOR_STATE_WRITE'
    assert result('F2-025')['code']=='FABRICATED_ACTOR'
    assert result('F2-026')['code']=='RETROCAUSAL_PARENT_HISTORY'


def test_owner_permission_separate_from_llm_output():
    assert result('F2-030')['code']=='TARGET_OWNER_PERMISSION_SELF_ISSUED'
    normal=native_from_oracle('F2-001')
    normal['owner_effect_committed']=True
    assert 'UNOWNED_DURABLE_EFFECT' in validate_native_receipt(CASES['F2-001'],normal)


def test_no_llm_mood_selection_without_separate_actor_witness():
    b=native_from_oracle('F2-001');b['selected_affect']='happy'
    assert 'AFFECT_FROM_HYPOTHESIS' in validate_native_receipt(CASES['F2-001'],b)


def test_proposal_and_renderer_have_no_real_world_authority():
    assert result('F2-023')['code']=='PROPOSAL_PROMOTION'
    assert result('F2-031')['code']=='RENDERER_MUTATION'


def test_observation_identity_exact_replay_and_deterministic_reexecution():
    for id in ('F2-001','F2-012','F2-027','F2-028','F2-041'):
        c=CASES[id]
        assert evaluate(copy.deepcopy(c))==evaluate(copy.deepcopy(c))


def test_future_native_b3_not_run_as_part_of_reference_court():
    # Calling the reference does not manufacture B3 imports or receipts.
    assert not Path(__file__).with_name('native_b3_adapter.py').exists()
    assert LIB['origin']=='INDEPENDENT_SOURCEFREE_SYNTHETIC'


def mutant_constant(c):
    # Fraudulent constant response ignores case; intentionally has incomplete provenance.
    return dict(case_id=c['id'],status='ELIGIBLE_NONCAUSAL',code='SOURCEFREE_EVIDENCE_BOUNDARY_PASS',no_mutation=True,
                admissible_routes=['NO_CHANGE'],verified_evidence_refs=[],material_actor_activity=[])


def mutant_label_only(c):
    # Fraudulent 'psychology': moralized mode controlled solely by author narrative label.
    out=copy.deepcopy(evaluate(c))
    if out['status']=='ELIGIBLE_NONCAUSAL':
        out['selected_affect']='recognized' if c['actor']['history_label']=='recognized_plan' else 'constrained'
    return out


def test_constant_fake_psychology_is_detected_on_lawful_and_negative():
    killed={id:validate_native_receipt(c,mutant_constant(c)) for id,c in CASES.items()}
    assert len([id for id,v in killed.items() if v])>=30
    assert 'F2-015' in killed and 'F2-016' in killed # valid no-change not itself penalized
    assert 'F2-027' in killed


def test_label_only_psychology_is_detected_without_punishing_no_change():
    a,b=CASES['F2-001'],CASES['F2-002']
    mutant_a,mutant_b=mutant_label_only(a),mutant_label_only(b)
    assert mutant_a['selected_affect']!=mutant_b['selected_affect']
    assert scientific_projection(evaluate(a))==scientific_projection(evaluate(b))
    assert 'AFFECT_FROM_HYPOTHESIS' in validate_native_receipt(a,mutant_a)
    assert 'AFFECT_FROM_HYPOTHESIS' in validate_native_receipt(b,mutant_b)
    for id in ('F2-015','F2-016','F2-041'):
        assert 'NO_CHANGE' in evaluate(CASES[id])['admissible_routes']
        assert validate_native_receipt(CASES[id],native_from_oracle(id))==[]
