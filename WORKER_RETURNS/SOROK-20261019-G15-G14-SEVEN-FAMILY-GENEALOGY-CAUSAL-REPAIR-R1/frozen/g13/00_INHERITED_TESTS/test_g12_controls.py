import json
import pytest
from g12_assays import save,ROOT,strict_causal_oracle

@pytest.fixture(scope='module')
def obs():return save()

@pytest.mark.parametrize('name',['A','B'])
def test_independent_conflicting_endpoint_and_mother_preservation(obs,name):
    s=obs['scenarios'][name]
    assert s['mother_before']==s['mother_after']
    assert not s['replay']['endpoint_match']
    assert s['oracle']['accepted']
    assert not s['new_actor_created']
    assert s['conception']=='PENDING_NONCAUSAL'

def test_older_child_preserved(obs):
    assert obs['scenarios']['B']['prior_child_refs']==['LAB_OLDER_CHILD_O1']
    assert obs['scenarios']['A']['prior_child_refs']==[]

@pytest.mark.parametrize('name',['forged_endpoint','missing_parent','future_endpoint_as_root_parent','duplicate_effective_index','route_antecedent_removed'])
def test_independent_oracle_detects_mutation(obs,name):
    x=obs['attacks'][name]
    assert x['lab']['endpoint_match']
    assert not x['independent']['accepted']
    assert x['independent']['errors']

@pytest.mark.parametrize('path',['target','world','psyche'])
def test_embargo_input_counterexample_recorded(obs,path):
    assert obs['embargo'][path]['sentinel_visible']

def test_unchanged_lab_stopping_has_no_missing_parent_detection(obs):
    assert obs['stopping_corrupt']['sufficient']
    assert obs['stopping_corrupt']['checks']['no_outstanding_mandatory_antecedent_missing_authority']

def test_alien_project_and_counterpart_probe_counterexample(obs):
    assert obs['alien_probes']['heldout_independence_pass']
    assert obs['alien_probes']['probes'][0]['typed_action']['decision']=='TAKE_REPAIR_ROTATION_LEAD_AND_UPDATE_LEDGER'

def test_candidate_payload_change_is_unbound_in_lab(obs):
    a=obs['candidate_payload']['before'];b=obs['candidate_payload']['after']
    assert a['candidate_set_hash']==b['candidate_set_hash']
    assert a==b

def test_exact_prospective_retry_bias(obs):
    assert obs['survivor_fractions']==['4/5','1/5']
    assert obs['retry']['n_attempts']==4
    assert obs['retry']['terminal_status']=='HISTORY_SEARCH_EXHAUSTED'
    assert obs['retry']['selected_events'] is None
    assert len(obs['retry']['attempts'])==4

def test_zero_draw_laboratory_controls(obs):
    assert obs['empty']['n_draws']==0
    assert obs['singleton']['n_draws']==0
    assert obs['unissued']['status']=='SELECTION_AUTHORITY_UNBOUND'

def test_actual_native_candidate_positive_and_idempotent_replay(obs):
    n=obs['native']
    assert n['control_commit']['status']=='ADP016_TRACE_COMMITTED_IN_FIXTURE'
    assert n['control_state_changed']
    assert not n['control_commit']['production_owner_commit']
    assert n['control_replay']['status']=='IDEMPOTENT_REPLAY'

def test_actual_native_project_refusal_and_zero_mutation(obs):
    assert obs['native']['project_refusal']=='UNAUTHORIZED_TRANSITION'
    assert obs['native']['project_zero_mutation']

def test_actual_native_actor_and_future_limits(obs):
    assert obs['native']['wrong_actor']['code']=='BLOCK_WRONG_ACTOR_SCOPE'
    assert obs['native']['future_event']['code']=='BLOCK_HIDDEN_FUTURE_LEAK'

@pytest.mark.parametrize('operation',['ACTOR_INITIALIZATION','GENEALOGY_HISTORY_TRACE','CONCEPTION_OCCURRED','BIRTH_OCCURRED','CHILD_GENERATED'])
def test_actual_production_denial(obs,operation):
    n=obs['native'];d=n['production'][operation]
    assert n['registry_empty']
    assert d['outcome']=='DENY_ZERO_EFFECT'
    assert d['reason']=='ZERO_POSITIVE_REGISTRY'
    assert d['zero_effect']

def test_original_source_bytes_and_actual_imports(obs):
    import hashlib
    rows=json.loads((ROOT/'source_manifest.json').read_text())+json.loads((ROOT/'native_source_manifest.json').read_text())
    for row in rows:
        b=(ROOT/row['staged_path']).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
    manifest={r['staged_path']:r['git_blob_sha1'] for r in rows}
    for row in obs['native']['imports'].values():
        assert manifest[row['module_file']]==row['git_blob_sha1']
