"""Offline proof against a frozen accepted law; no warmed producer cache."""
from dataclasses import replace
import copy,json,os,pathlib,subprocess,sys
import pytest
from rawlsing_next import r3_s02_seam_witness as S
from rawlsing_next import pre553_n9_n10w_progressive_candidate as P
from rawlsing_next import pre553_selected_world_progressive_contract as W
from rawlsing_next.pre553_empirical_objects import ExactRef
ROOT=pathlib.Path(__file__).resolve().parents[2]
ARTIFACT=ROOT/'WORKER_RETURNS/PYAT-R3-HQ290-S00V3-OFFLINE-PRODUCER-BINDING-R1/repro/pinned_accepted_artifact.json'

def saved_bundle():
    p=json.loads(ARTIFACT.read_text());c=p['selected_contract'];b=p['bundle']
    contract=W.SelectedWorldContract(**{**c,**{k:ExactRef(**c[k]) for k in ('source_universe_ref','release_ref','risk_set_ref')}})
    return S.SociologicalWorldBundle(bundle_id=b['bundle_id'],contract_version=b['contract_version'],content_hash=b['content_hash'],world_scope=b['world_scope'],channels=tuple(S.ChannelValue(**v) for v in b['channels']),evidence_graph=tuple(b['evidence_graph']),conditions=tuple(b['conditions']),steps=tuple(b['steps']),replay=b['replay'],selected_world_contract=contract)

def rehash(b,**kw):
    b=replace(b,content_hash='',**kw);return replace(b,content_hash=S._content_hash(b.as_dict()))

def disable(monkeypatch):
    def unavailable(*a,**kw):raise AssertionError('original producer unavailable')
    for module,names in [(S,['build_sociological_bundle','build_source_free_native_joint_bundle','select_world','run_progressive_chain','build_synthetic_world']),(W,['select_world','run_selected_world_progressive_chain']),(P,['build_synthetic_world','run_progressive_chain'])]:
        for name in names:monkeypatch.setattr(module,name,unavailable)

def test_saved_p04_offline_without_admission_or_cache(monkeypatch):
    disable(monkeypatch);b=saved_bundle();c=S.ContractOnlySeamConsumer(b)
    result=c.compute_scenario('I01_SOURCEFREE_PROGRESSIVE',list(S.P04_STEPS))
    p=json.loads(ARTIFACT.read_text())
    assert result==p['numeric_result'] and c.get_receipt().as_dict()==p['consumer_receipt']

@pytest.mark.parametrize('attack',['coherent_counts','root','evidence','risk','replay','extra_annotation','wrong_annotation','false_scope'])
def test_offline_tamper_keeps_strong_binding(monkeypatch,attack):
    b=saved_bundle()
    if attack=='coherent_counts':
        channels=[]
        for ch in b.channels:
            if ch.value['step_id']==S.P04_STEPS[-1]:ch=replace(ch,value={**ch.value,'raw_numerator_support':4,'raw_probability_exact_fraction':{'$exact_fraction':[1,2]}})
            channels.append(ch)
        steps=copy.deepcopy(list(b.steps))
        for cell in steps[-1]['cells'].values():cell.update(numerator=4,fraction={'$exact_fraction':[1,2]})
        b=rehash(b,channels=tuple(channels),steps=tuple(steps))
        assert S.ContractOnlySeamConsumer(b)._validate_fraction_closure() is None
    if attack=='root':
        c=replace(b.selected_world_contract,source_universe_ref=ExactRef('SYNTHETIC','forged','0'*64));b=rehash(b,selected_world_contract=c,replay={**b.replay,'input_preimages':[S.contract_content_hash(c)]})
    if attack=='evidence':b=rehash(b,evidence_graph=({**b.evidence_graph[0],'parent_refs':['forged']},*b.evidence_graph[1:]))
    if attack=='risk':b=rehash(b,conditions=({**b.conditions[0],'risk_set_ref':{}},*b.conditions[1:]))
    if attack=='replay':b=rehash(b,replay={**b.replay,'code_ref':'foreign'})
    if attack=='extra_annotation':b=rehash(b,world_scope={**b.world_scope,'arbitrary_claim':'issued'})
    if attack=='wrong_annotation':b=rehash(b,world_scope={**b.world_scope,'unrelated_test_note':123})
    if attack=='false_scope':b=rehash(b,world_scope={**b.world_scope,'qualified_real_source_value_read':True})
    disable(monkeypatch);c=S.ContractOnlySeamConsumer(b);r=c.compute_scenario('offline',list(S.P04_STEPS))
    assert r['status']=='REFUSED' and c.get_receipt().values_read==[]

def test_documentary_note_and_bundle_locator_do_not_change_law(monkeypatch):
    b=saved_bundle();b=rehash(b,bundle_id='another-local-locator',world_scope={**b.world_scope,'unrelated_test_note':'documentary only'})
    disable(monkeypatch)
    assert S.ContractOnlySeamConsumer(b).compute_scenario('offline',list(S.P04_STEPS))['status']=='COMPUTED'

def test_fresh_native_law_offline_and_stale_root_refusal(monkeypatch):
    a=S.build_source_free_native_joint_bundle({(0,0):3,(0,1):1,(1,0):1,(1,1):3})
    b=S.build_source_free_native_joint_bundle({(0,0):3,(0,1):1,(1,0):2,(1,1):2})
    stale=rehash(a,channels=b.channels,steps=b.steps,conditions=tuple({**row,'risk_set_ref':a.selected_world_contract.risk_set_ref.as_dict()} for row in b.conditions))
    disable(monkeypatch)
    for bundle,frac in [(a,[3,4]),(b,[1,2])]:assert S.ContractOnlySeamConsumer(bundle).compute_scenario('offline',['P_Q86A_given_Q86B_1'])['exact_probabilities']['1']['$exact_fraction']==frac
    c=S.ContractOnlySeamConsumer(stale);r=c.compute_scenario('offline',['P_Q86A_given_Q86B_1'])
    assert r['reason']=='PRODUCER_VALUE_IDENTITY_MISMATCH' and c.get_receipt().values_read==[]

def test_fresh_interpreter_no_warmed_producer_cache():
    code='''import sys,json
from pytest import MonkeyPatch
from rawlsing_next.tests.test_hq290_s00v3_offline_binding import disable,saved_bundle,S
m=MonkeyPatch();disable(m)
c=S.ContractOnlySeamConsumer(saved_bundle());r=c.compute_scenario('I01_SOURCEFREE_PROGRESSIVE',list(S.P04_STEPS))
assert r['status']=='COMPUTED'
print(json.dumps({'result':r,'receipt':c.get_receipt().as_dict()}))
'''
    p=subprocess.run([sys.executable,'-c',code],text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(ROOT)})
    assert p.returncode==0,p.stderr
    saved=json.loads(ARTIFACT.read_text());result=json.loads(p.stdout)
    assert result['result']==saved['numeric_result'] and result['receipt']==saved['consumer_receipt']
