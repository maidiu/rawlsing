"""Literal stronger scientific contract. REDs remain RED, never xfail/skip."""
import pytest
from g12_assays import save
@pytest.fixture(scope='module')
def obs():return save()
@pytest.mark.parametrize('name',['forged_endpoint','missing_parent','future_endpoint_as_root_parent','duplicate_effective_index','route_antecedent_removed'])
def test_forward_validator_refuses_invalid_causal_history(obs,name):
    assert not obs['attacks'][name]['lab']['endpoint_match'],name
@pytest.mark.parametrize('path',['target','world','psyche'])
def test_model_input_membrane_blocks_future_child_metadata(obs,path):
    assert not obs['embargo'][path]['sentinel_visible'],path
def test_stopping_law_requires_actual_antecedent_closure(obs):
    assert not obs['stopping_corrupt']['sufficient']
def test_project_specific_heldout_probe_refuses_unrelated_project(obs):
    assert not obs['alien_probes']['heldout_independence_pass']
def test_same_candidate_id_changed_payload_changes_replay_identity(obs):
    a=obs['candidate_payload']['before'];b=obs['candidate_payload']['after']
    assert a['candidate_set_hash']!=b['candidate_set_hash']
def test_lab_sampler_is_accepted_adp020_algorithm(obs):
    assert obs['rng_algorithm']['actual']==obs['rng_algorithm']['required']
