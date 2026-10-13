"""S00M @2.0.0 M01-M13: fresh synthetic law vs downstream tamper."""
from dataclasses import replace
from fractions import Fraction
import copy
import pytest
from rawlsing_next import r3_s02_seam_witness as S

SCHEMA='PYAT_R3_HQ288_S00M_SOURCEFREE_COUNT_DERIVED_FRACTION_ACCEPTANCE@2.0.0'
JOINT={(0,0):3,(0,1):1,(1,0):1,(1,1):3}
NATIVE='P_Q86A_given_Q86B_1'

def native(joint=None):return S.build_source_free_native_joint_bundle(JOINT if joint is None else joint)
def rehash(b,**kw):
    b=replace(b,content_hash='',**kw);return replace(b,content_hash=S._content_hash(b.as_dict()))
def change(b,cid,**kw):
    return rehash(b,channels=tuple(replace(c,value={**c.value,**kw}) if c.channel_id==cid else c for c in b.channels))
def compute(b,steps=None,label='v2'):
    c=S.ContractOnlySeamConsumer(b);r=c.compute_scenario(label,[NATIVE] if steps is None else steps);return c,r

def refused(b,reason=None,steps=None):
    c,r=compute(b,steps)
    assert r['status']=='REFUSED'
    if reason:assert r['reason']==reason
    assert c.get_receipt().values_read==[]
    assert 'exact_probabilities' not in r
    return r

def test_M01_P04_CUMULATIVE():
    b=S.build_sociological_bundle();c,r=compute(b,list(S.P04_STEPS))
    assert [(t['raw_denominator_support'],t['raw_numerators'],t['exact_probabilities']['1']['$exact_fraction']) for t in r['progressive_trace']]==[(32,{'0':14,'1':18},[9,16]),(16,{'0':6,'1':10},[5,8]),(8,{'0':2,'1':6},[3,4])]
    assert len(c.get_receipt().values_read)==6
    assert all(x.semantic_effect=='VALUE_USED_IN_EXACT_CONDITIONAL' for x in c.get_receipt().values_read)
    assert b.selected_world_contract.selection_metadata['row_count']==58
    for steps,support in [(list(S.P04_STEPS[:2]),16),(list(S.P04_STEPS[1:]),8)]:
        assert compute(b,steps)[1]['raw_denominator_support']==support

def test_M02_NATIVE_BASE():
    c,r=compute(native());assert r['status']=='COMPUTED'
    assert r['raw_numerators']=={'0':1,'1':3} and r['raw_denominator_support']==4
    assert r['exact_probabilities']['1']['$exact_fraction']==[3,4]
    assert len(c.get_receipt().values_read)==2
    assert all(x.semantic_effect=='VALUE_USED_IN_EXACT_CONDITIONAL' for x in c.get_receipt().values_read)

def test_M03_NATIVE_REISSUED_SYNTH():
    old=native();new=native({**JOINT,(1,0):2,(1,1):2})
    for key in ('source_universe_ref','release_ref','risk_set_ref'):
        assert getattr(old.selected_world_contract,key)!=getattr(new.selected_world_contract,key)
    a=compute(old)[1];c,b=compute(new)
    assert a['exact_probabilities']['1']['$exact_fraction']==[3,4]
    assert b['exact_probabilities']['1']['$exact_fraction']==[1,2]
    assert a['source_value_dependency']['used_input_refs']!=b['source_value_dependency']['used_input_refs']
    assert len(c.get_receipt().values_read)==2

def test_M04_STALE_COUNT_ONLY():
    b=change(native(),'CH_'+NATIVE+'_0',raw_numerator_support=2)
    b=change(b,'CH_'+NATIVE+'_1',raw_numerator_support=2)
    refused(b,'FRACTION_CLOSURE_MISMATCH')

def test_M05_STALE_FRACTION():
    refused(change(native(),'CH_'+NATIVE+'_1',raw_probability_exact_fraction={'$exact_fraction':[100,101]}),'FRACTION_CLOSURE_MISMATCH')

def test_M06_STALE_STEP():
    b=native();steps=copy.deepcopy(list(b.steps));steps[1]['cells']['1']['numerator']=234
    refused(rehash(b,steps=tuple(steps)),'STEP_CELL_NUMERATOR_MISMATCH')

def test_M07_LOCAL_REHASH_STALE_ROOT():
    old=native();fresh=native({**JOINT,(1,0):2,(1,1):2})
    # All downstream geometry coherent; old roots/replay/evidence preserved.
    b=rehash(old,channels=fresh.channels,steps=fresh.steps,conditions=tuple({**row,'risk_set_ref':old.selected_world_contract.risk_set_ref.as_dict()} for row in fresh.conditions))
    assert S.ContractOnlySeamConsumer(b)._validate_fraction_closure() is None
    assert S.ContractOnlySeamConsumer(b)._validate_step_geometry() is None
    refused(b,'PRODUCER_VALUE_IDENTITY_MISMATCH')

def test_M08_UNRELATED_VALID_PRODUCER():
    a=native();b=native({**JOINT,(0,0):5,(0,1):7})
    ar=compute(a)[1];br=compute(b)[1]
    assert ar['exact_probabilities']==br['exact_probabilities']
    assert ar['raw_numerators']==br['raw_numerators']
    assert a.selected_world_contract.release_ref!=b.selected_world_contract.release_ref
    assert br['status']=='COMPUTED'

def test_M09_UNRELATED_INVALID_GLOBAL():
    b=S.build_sociological_bundle();b=change(b,'CH_P_Y_given_A_B_C_1',raw_numerator_support=999,raw_probability_exact_fraction=None)
    refused(b,steps=['P_Y_given_A'])

@pytest.mark.parametrize('fraction',[None,{},[],{'$exact_fraction':None},{'$exact_fraction':[]},{'$exact_fraction':[1]},{'$exact_fraction':[1,0]},{'$exact_fraction':['3',4]},{'$exact_fraction':[True,4]},{'$exact_fraction':[3,-4]},{'$exact_fraction':[6,8]},{'$exact_fraction':[3,4],'extra':1}])
def test_M10_NULL_MALFORMED(fraction):
    refused(change(native(),'CH_'+NATIVE+'_1',raw_probability_exact_fraction=fraction))

def test_M10_MISSING_FRACTION():
    b=native();ch=b.channels[-1];v=dict(ch.value);v.pop('raw_probability_exact_fraction')
    refused(rehash(b,channels=(*b.channels[:-1],replace(ch,value=v))),'MISSING_EXACT_FRACTION')

def test_M11_ZERO_SUPPORT():
    b=native({**JOINT,(1,0):0,(1,1):0});c,r=compute(b)
    assert (r['status'],r['reason'])==('ZERO_SUPPORT','ZERO_DENOMINATOR_ABSTENTION')
    assert 'exact_probabilities' not in r
    assert not any(x.semantic_effect=='VALUE_USED_IN_EXACT_CONDITIONAL' for x in c.get_receipt().values_read)
    assert all(ch.value['raw_probability_exact_fraction'] is None for ch in b.channels[2:])

@pytest.mark.parametrize('label',['Democracy_Support','INSTITUTIONAL_TRUST','democratic_attitudes'])
def test_M12_FALSE_LABELS(label):
    c,r=compute(native(),label=label)
    assert (r['status'],r['reason'])==('REFUSED','FALSE_S00_Q86_SOURCE_MEANING')
    assert c.get_receipt().values_read==[]

def test_M13_GT2_ISSUER():
    with pytest.raises(S.SeamContractError,match=S.GT2_VALUE_HOLD):
        S.build_retained_gt2_bundle(issued_source_owned_values={'coexposure':19210,'cells':[1,3]},issued_use_authority='caller-token')

@pytest.mark.parametrize('attack',['missing_channel','extra_channel','missing_step','extra_step','missing_condition','extra_condition','missing_cell','extra_cell','wrong_cell','conditioner','source_root','release_root','risk_root','evidence','step_fraction','channel_bool','channel_negative','denom_bool','step_string'])
def test_complete_domain_and_identity(attack):
    b=native()
    if attack=='missing_channel':b=rehash(b,channels=b.channels[:-1])
    if attack=='extra_channel':b=rehash(b,channels=(*b.channels,replace(b.channels[0],channel_id='extra')))
    if attack in ('missing_step','extra_step'):
        b=rehash(b,steps=b.steps[:-1] if attack=='missing_step' else (*b.steps,{**b.steps[0],'step_id':'extra'}))
    if attack in ('missing_condition','extra_condition'):
        b=rehash(b,conditions=b.conditions[:-1] if attack=='missing_condition' else (*b.conditions,{**b.conditions[0],'step_id':'extra'}))
    if attack in ('missing_cell','extra_cell','step_fraction','step_string'):
        steps=copy.deepcopy(list(b.steps))
        if attack=='missing_cell':steps[1]['cells'].pop('0')
        if attack=='extra_cell':steps[1]['cells']['9']={'numerator':0}
        if attack=='step_fraction':steps[1]['cells']['1']['fraction']={'$exact_fraction':[1,2]}
        if attack=='step_string':steps[1]['cells']['1']['numerator']='3'
        b=rehash(b,steps=tuple(steps))
    if attack=='wrong_cell':b=change(b,b.channels[-1].channel_id,cell='9')
    if attack=='conditioner':b=change(b,b.channels[-1].channel_id,conditioners=[['Q86A','1']])
    if attack.endswith('_root'):
        field={'source_root':'source_universe_ref','release_root':'release_ref','risk_root':'risk_set_ref'}[attack]
        c=replace(b.selected_world_contract,**{field:getattr(b.selected_world_contract,field).__class__('SYNTHETIC','foreign','0'*64)})
        b=rehash(b,selected_world_contract=c,replay={**b.replay,'input_preimages':[S.contract_content_hash(c)]})
    if attack=='evidence':b=rehash(b,evidence_graph=({**b.evidence_graph[0],'parent_refs':['foreign']},))
    if attack in ('channel_bool','channel_negative'):
        b=change(b,b.channels[-1].channel_id,raw_numerator_support=True if attack=='channel_bool' else -1)
    if attack=='denom_bool':b=rehash(b,channels=(*b.channels[:-1],replace(b.channels[-1],support=True)))
    refused(b)

def test_P04_coherent_stale_evidence_and_roots():
    b=S.build_sociological_bundle();step=b.steps[-1]['step_id']
    channels=[]
    for ch in b.channels:
        if ch.value['step_id']==step:
            n=4;ch=replace(ch,value={**ch.value,'raw_numerator_support':n,'raw_probability_exact_fraction':{'$exact_fraction':[1,2]}})
        channels.append(ch)
    steps=copy.deepcopy(list(b.steps))
    for cell in steps[-1]['cells'].values():cell.update(numerator=4,fraction={'$exact_fraction':[1,2]})
    b=rehash(b,channels=tuple(channels),steps=tuple(steps))
    assert S.ContractOnlySeamConsumer(b)._validate_fraction_closure() is None
    refused(b,'PRODUCER_VALUE_IDENTITY_MISMATCH',steps=list(S.P04_STEPS))

@pytest.mark.parametrize('joint',[{(0,0):1}, {(0,0):True,(0,1):1,(1,0):1,(1,1):1}, {(0,0):-1,(0,1):1,(1,0):1,(1,1):1}, {(0,0):1,(0,1):1,(1,0):1,(1,1):1,(9,9):0}])
def test_builder_invalid_joint_is_typed(joint):
    with pytest.raises(S.SeamContractError,match='EXACT_NONNEGATIVE_2X2'):native(joint)


def test_M08_unrelated_documentary_annotation():
    b=S.build_sociological_bundle()
    annotated=rehash(b,world_scope={**b.world_scope,'unrelated_test_note':'This is not a measured value'})
    assert compute(b,['P_Y_given_A_B'])[1]==compute(annotated,['P_Y_given_A_B'])[1]

@pytest.mark.parametrize('attack',['channel_value_none','missing_count','condition_none','condition_missing_id','step_none','step_missing_cells','step_cells_none','step_cell_none','step_missing_numerator','support_none','support_string','negative_support','denominator_none','denominator_string','fraction_float','fraction_missing','evidence_none','replay_none','scope_none'])
def test_malformed_bundle_values_are_typed(attack):
    b=native()
    if attack=='channel_value_none':b=replace(b,channels=(*b.channels[:-1],replace(b.channels[-1],value=None)))
    if attack=='missing_count':
        v=dict(b.channels[-1].value);v.pop('raw_numerator_support');b=rehash(b,channels=(*b.channels[:-1],replace(b.channels[-1],value=v)))
    if attack.startswith('condition_'):
        conditions=copy.deepcopy(list(b.conditions))
        if attack=='condition_none':conditions[-1]=None
        if attack=='condition_missing_id':conditions[-1].pop('step_id')
        b=replace(b,conditions=tuple(conditions))
    if attack.startswith('step_'):
        steps=copy.deepcopy(list(b.steps))
        if attack=='step_none':steps[-1]=None
        if attack=='step_missing_cells':steps[-1].pop('cells')
        if attack=='step_cells_none':steps[-1]['cells']=None
        if attack=='step_cell_none':steps[-1]['cells']['1']=None
        if attack=='step_missing_numerator':steps[-1]['cells']['1'].pop('numerator')
        b=replace(b,steps=tuple(steps))
    if attack in ('support_none','support_string','negative_support'):
        value={'support_none':None,'support_string':'4','negative_support':-1}[attack]
        b=rehash(b,channels=(*b.channels[:-1],replace(b.channels[-1],support=value)))
    if attack.startswith('denominator_'):
        conditions=copy.deepcopy(list(b.conditions));conditions[-1]['denominator']=None if attack=='denominator_none' else '4';b=rehash(b,conditions=tuple(conditions))
    if attack.startswith('fraction_'):b=change(b,b.channels[-1].channel_id,raw_probability_exact_fraction={'$exact_fraction':[0.75,1]} if attack=='fraction_float' else None)
    if attack=='evidence_none':b=replace(b,evidence_graph=(None,))
    if attack=='replay_none':b=replace(b,replay=None)
    if attack=='scope_none':b=replace(b,world_scope=None)
    # Broken representations may not even be serializable/hashable; still
    # refuse at the actual consumer boundary without arbitrary exceptions.
    refused(b)
