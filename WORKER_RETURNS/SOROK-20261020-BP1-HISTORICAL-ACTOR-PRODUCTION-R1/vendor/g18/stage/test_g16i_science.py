"""Independent G16I controls and hostile assertions, frozen oracles in 01.
Only declared finite research fixtures run; no native persons or child events.
"""
from pathlib import Path
from copy import deepcopy
import hashlib,hmac,json,os,subprocess,sys
import pytest
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'sandbox/candidate'))
NETWORK=[]
def offline(event,args):
    if event.startswith('socket.'):
        NETWORK.append(event)
        raise RuntimeError('G16I_OFFLINE_REQUIRED')
sys.addaudithook(offline)
from lab_sgi1.history import PersonHistoryBuilder,replay_history,derive_psyche,independent_actions,make_event
from lab_sgi1.construction import forward_replay_to_endpoint,construct_second_parent
from lab_sgi1.continuation import continue_person,forward_continuation,child_developmental_environment_fixture,lab_conception_boundary
from lab_sgi1.joint import material_joint_opportunity,observe_joint_actions
from lab_sgi1.relation import reconcile
from lab_sgi1.mother import build_mother_checkpoint
from lab_sgi1.core import h_obj,ScopedRNG,canon,ADP020_DOMAIN_SEPARATOR
from lab_sgi1.proposal import frozen_fallback_record,dedup_candidates
from lab_sgi1.selection import STREAM,adp020_select,replay_decision
from lab_sgi1.research import inputs,run
OBS={}
def observe(k,v):OBS[k]=v
@pytest.fixture(scope='session',autouse=True)
def receipts():
    yield
    imports=[]
    for name,m in sorted(sys.modules.items()):
        if name.startswith('lab_sgi1') and getattr(m,'__file__',None):
            p=Path(m.__file__);b=p.read_bytes()
            imports.append(dict(module=name,path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(b).hexdigest(),blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
    p=ROOT/os.environ['G16I_OBSERVATIONS'];p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(dict(observations=OBS,imports=imports,network_attempts=NETWORK),indent=2,sort_keys=True)+'\n')

def ec(place='INST_WORKSHOP_A',route='ROUTE_LOCAL_CLOSED'):
    return dict(route_kind_id=route,time_or_interval='T_ENCOUNTER_LAB_WINDOW',required_state_predicates=[dict(field='place',equals=place),dict(field='availability_status',equals='available_for_encounter')])
def history(material=None):return PersonHistoryBuilder('G16I_ADULT','G16I_SOURCE_HISTORY',material=material).build()
def world(units=5):
    w=deepcopy(next(e['payload'] for e in history() if e['kind']=='WORLD_MATERIAL'));w['material_units']=units
    return w
def mother(v='M0'):return build_mother_checkpoint('FIX_'+v,v).anchor_dict()
def relation_packet(material=None):
    a=mother();e=history(world());w=observe_joint_actions(a,e,material or material_joint_opportunity())
    rel=reconcile(a,e,dict(candidate_kind='PROVISIONAL_COUNTERPART',joint_evidence=w))
    return a,e,w,rel

def rekey(events):
    mapping={};out=[]
    def remap(v):
        if isinstance(v,str):return mapping.get(v,v)
        if isinstance(v,list):return [remap(x) for x in v]
        if isinstance(v,dict):return {k:remap(x) for k,x in v.items()}
        return v
    for event in events:
        e=remap(deepcopy(event));old=e.pop('event_id');new=h_obj(e);mapping[old]=new
        out.append(dict(event_id=new,**e))
    return out

# Eight new source-consuming downstream positive/negative controls.
def test_material_remainder_controls_later_performed_work():
    e=history(world(5));p=continue_person(e);cut=continue_person(history(world(3)))
    observe('material_remainder',dict(history=replay_history(e),positive=p,exhausted=cut))
    assert p is not None
    assert p['payload']['units_performed']==2
    assert p['payload']['earned']==4
    assert cut is None
    assert p['payload']['after']['completed_units']==5

def test_competing_offer_changes_actual_attendance():
    w=world();w['offers']['ROUTE_MOBILITY']['payment']=100
    e=history(w);r=replay_history(e)
    w['offers']['ROUTE_MOBILITY']['permit']=False
    c=replay_history(history(w));observe('competing_offer',dict(positive=r,revoked=c))
    assert r['valid'] is True
    assert r['state']['place']=='INST_TRANSIT_E'
    assert c['state']['place']=='INST_WORKSHOP_A'
    assert r['state']['cash']-c['state']['cash']==82
    assert forward_replay_to_endpoint(e,ec('INST_TRANSIT_E','ROUTE_MOBILITY'))['endpoint_match'] is True

def test_peer_quantity_reaches_actual_settlement():
    e=history(world())
    next(x for x in e if x['kind']=='PEER_ACTION')['payload']['returned_units']=1
    next(x for x in e if x['kind']=='NONMOTHER_RELATIONSHIP')['payload']['durable_effect']=dict(returned_units=1,obligation_units=1)
    e=rekey(e);r=replay_history(e);p=independent_actions(e,derive_psyche(e))
    observe('peer_quantity',dict(replay=r,actions=p))
    assert r['valid'] is True
    assert r['state']['debt_units']==1
    assert p['probes'][1]['typed_action']['status']=='PERFORMED'
    assert p['probes'][1]['typed_action']['after']['debt_units']==0
    cut=[x for x in e if x['kind']!='PEER_ACTION']
    assert independent_actions(cut,derive_psyche(cut))['heldout_independence_pass'] is False

def test_experienced_values_reach_memory_and_formation():
    e=history(world());r=replay_history(e)
    project=next(x for x in e if x['kind']=='PROJECT')
    m=next(w for w in r['value_witnesses'] if w['kind']=='MEMORY_TRACE')
    observe('experience_values',dict(memory=m,psyche=derive_psyche(e)))
    assert r['valid'] is True
    assert m['effect']['experienced_basis_event']==project['event_id']
    assert m['effect']['experienced_effect']==r['effects'][project['event_id']]
    assert derive_psyche(e)['practices'][0]['formed_value']['checks']==3
    assert forward_replay_to_endpoint(e,ec())['endpoint_match'] is True

def test_variable_task_cost_reaches_continued_context():
    material=material_joint_opportunity();material['payment_per_actor']=7;material['task_hours']=2
    material['event_id']=h_obj({k:v for k,v in material.items() if k!='event_id'})
    a,e,w,rel=relation_packet(material);out=forward_continuation(a,e,rel)
    p=next(x for x in out['continuation_events'] if x['actor']=='G16I_ADULT');s=replay_history(e)['state']
    context=child_developmental_environment_fixture(a,e,out,lab_conception_boundary())
    observe('variable_task_cost',dict(witness=w,continuation=out,context=context))
    assert rel['relationship_committed'] is True
    assert p['payload']['before']['cash']==s['cash']+7
    assert p['payload']['before']['free_hours']==s['free_hours']-2
    assert next(x for x in context['potential_material_contexts'] if x['actor']=='G16I_ADULT')['material_context']['cash_after']==s['cash']+11
    assert context['exposures']==[]

def test_separate_later_time_controls_second_contact():
    a,e,w,rel=relation_packet();good=forward_continuation(a,e,rel,material_joint_opportunity(1200))
    bad=forward_continuation(a,e,rel,material_joint_opportunity(999))
    observe('later_time',dict(positive=good,reverse=bad))
    assert good['relationship_continuation_admitted'] is True
    assert good['research_relation_continuation']['effective_index']==1202
    assert bad['relationship_continuation_admitted'] is False
    assert bad['research_relation_continuation']['status']=='NO_CHANGE'

def test_operative_constraints_survive_paraphrase_selection():
    a=deepcopy(frozen_fallback_record('M0','ROUTE_LOCAL_CLOSED').parsed_candidates[0]);b=deepcopy(a)
    b['candidate_local_id']='G15_SECOND_ENDPOINT_CLASS';b['endpoint_constraints']['required_state_predicates']=[dict(field='material_position',equals='waged_repair')]
    alias=deepcopy(a);alias['candidate_local_id']='A_PARAPHRASE';alias['assumptions']=['same workplace adjacency in different wording']
    x=dedup_candidates([a,b]);y=dedup_candidates([alias,b,a])
    r=adp020_select('SIM_UNIFORM_CLASSES',y['classes'],'47'*32,'G13_SCOPE')
    observe('operative_dedup',dict(original=x,paraphrased=y,selection=r))
    assert x['n_classes']==y['n_classes']==2
    assert x['class_set_hash']==y['class_set_hash']
    assert r['n_draws']==1
    assert replay_decision(r)['status']=='EXACT_REPLAY'
    duplicate=deepcopy(b);duplicate['candidate_local_id']=a['candidate_local_id']
    assert dedup_candidates([a,duplicate])['status']=='DEDUP_UNDERDETERMINED'

def test_current_seed_reaches_independent_entropy_reference():
    rows=[]
    for seed in ['47'*32,'6a'*32,'9c'*32]:
        rec=ScopedRNG(seed,STREAM,'G13_SCOPE').draw(997,'G16I_REAL_DECISION','G16I_CANDIDATE_SET',2).as_dict()
        scope=hmac.new(bytes.fromhex(seed),ADP020_DOMAIN_SEPARATOR+canon(dict(kind='scope',scope_kind='GENEALOGY',scope_id='G13_SCOPE')),hashlib.sha256).digest()
        stream=hmac.new(scope,ADP020_DOMAIN_SEPARATOR+canon(dict(kind='stream',stream_name=STREAM)),hashlib.sha256).digest()
        raw=int.from_bytes(hmac.new(stream,ADP020_DOMAIN_SEPARATOR+canon(rec['entropy_coordinate']),hashlib.sha256).digest()[:8],'big')
        rows.append(dict(receipt=rec,independent_raw=raw));observe('current_entropy',rows)
        assert rec['accepted_raw_u64']==raw
        assert rec['draw_value']==raw%997
        assert raw<(2**64//997)*997
    assert len({r['independent_raw'] for r in rows})==3

# Hostile tests keep failures literal: the invariant is not changed to observed behavior.
def test_repeated_project_cannot_spend_same_material_twice():
    e=history(world(5));project=deepcopy(next(x for x in e if x['kind']=='PROJECT'))
    project['effective_index']=100;project['event_id']='G16I_SECOND_MATERIAL_PROJECT';e.append(project)
    r=replay_history(e);observe('repeated_project',r)
    assert not r['valid'] or r['state']['completed_units']<=5

def test_repeated_training_cannot_overspend_current_time():
    e=history(world());e.append(make_event(100,'SCHOOLING','G16I_ADULT',dict(hours=30),[e[0]['event_id']]))
    r=replay_history(e);observe('repeated_training',r)
    assert not r['valid'] or r['state']['free_hours']>=0

def test_repeated_peer_actions_cannot_return_nonexistent_tools():
    e=history(world());pa=deepcopy(next(x for x in e if x['kind']=='PEER_ACTION'));pa['effective_index']=100;pa['event_id']='G16I_SECOND_PEER_RETURN';e.append(pa)
    r=replay_history(e);returns=sum(x['effect']['returned_units'] for x in r['value_witnesses'] if x['kind']=='PEER_ACTION');observe('repeated_peer',dict(replay=r,total_returned=returns))
    assert not r['valid'] or returns<=3

def test_forged_participation_cannot_supply_unperformed_cash():
    a,e,w,rel=relation_packet();act=deepcopy(w['actions'][1]);act['after']['cash']+=100000
    act['event_id']=h_obj({k:v for k,v in act.items() if k!='event_id'})
    result=continue_person(e,participation=act);observe('forged_participation',result)
    assert result is None

def test_late_actual_participation_cannot_parent_earlier_continuation():
    a,e,w,rel=relation_packet(material_joint_opportunity(1100));out=forward_continuation(a,e,rel)
    observe('late_participation',dict(witness=w,continuation=out))
    for p in out['continuation_events']:
        actual=next(x for x in w['actions'] if x['owner_id']==p['actor'])
        assert p['effective_index']>actual['effective_index']

def test_singular_owned_event_cannot_silently_add_other_actor():
    e=history(world());next(x for x in e if x['kind']=='WORK_POSITION')['actors'].append('UNPERFORMED_OTHER_PERSON')
    r=replay_history(e);observe('extra_actor',r)
    assert r['valid'] is False

def test_future_child_material_cannot_enter_committed_causal_output():
    data=inputs();m=data['joint_material_opportunity'];m['future_child_personality']='G16I_DESIRED_WOUND'
    m['event_id']=h_obj({k:v for k,v in m.items() if k!='event_id'})
    out=run(data);observe('future_material',out)
    assert out['terminal']['status']!='COMMITTED'

def test_archived_m2_can_continue_legitimate_prior_life():
    a=mother('M2');original=deepcopy(a);out=forward_continuation(a,[],{})
    observe('archive_m2',dict(anchor=a,continuation=out))
    assert a==original
    assert a['already_generated_child_refs']==['LAB_OLDER_CHILD_O1']
    assert out['maternal_continuation_admitted'] is True

def test_known_counterpart_has_positive_history_reuse_path():
    data=inputs();data['fixture_variant']='MP';data['proposal_record']=frozen_fallback_record('MP','ROUTE_LOCAL_CLOSED')
    out=run(data);observe('archive_mp',dict(anchor=out['anchor'],terminal=out['terminal'],construction=out['construction_summary']))
    assert mother('MP')['known_counterpart_identity_ref_or_null']=='F_EXISTING'
    assert out['terminal']['status']=='COMMITTED'
    assert out['relation']['objective_relation']['participants'][1]=='F_EXISTING'

def test_lawful_unconventional_and_mobility_routes_have_positive_history_controls():
    rows=[]
    for route,place in [('ROUTE_UNCONVENTIONAL','INST_COMMUNITY_D'),('ROUTE_MOBILITY','INST_TRANSIT_E')]:
        w=world();w['offers'][route]['payment']=100;e=history(w)
        r=forward_replay_to_endpoint(e,ec(place,route));rows.append(r)
        assert r['endpoint_match'] is True
        assert independent_actions(e,derive_psyche(e))['heldout_independence_pass'] is True
        assert forward_replay_to_endpoint(e,ec('IMPOSSIBLE_SITE',route))['endpoint_match'] is False
    observe('alternative_route_positives',rows)

def test_future_shadow_is_stable_and_false_lineage_diverges():
    data=inputs();a=run(deepcopy(data));data['future_child_shadow']={'future_child_outcome':'G16I_DESIRED_WOUND'};b=run(data)
    receipt=deepcopy(a['causal_replay_record']['selected_decision_receipt'])
    receipt['lineage']['scope_registration']['source_record']['anchor_event_index']+=1
    observe('false_lineage',replay_decision(receipt))
    assert a['terminal']['status']=='COMMITTED'
    assert a['causal_replay_record']==b['causal_replay_record']
    assert replay_decision(receipt)['status']=='EXACT_REPLAY_DIVERGENCE'

def test_cold_replay_uses_actual_saved_sources(tmp_path):
    a=tmp_path/'first.json';b=tmp_path/'replayed.json';c=tmp_path/'tampered.json';d=tmp_path/'diverged.json'
    cmd=[sys.executable,'-B',str(ROOT/'sandbox/candidate/run_candidate.py')]
    first=subprocess.run(cmd+['--output',str(a)],capture_output=True,text=True)
    replay=subprocess.run(cmd+['--replay',str(a),'--output',str(b)],capture_output=True,text=True)
    packet=json.loads(a.read_text());packet['frozen_inputs']['joint_material_opportunity']['permit']=False;c.write_text(json.dumps(packet))
    tamper=subprocess.run(cmd+['--replay',str(c),'--output',str(d)],capture_output=True,text=True)
    old=json.loads(a.read_text());same=json.loads(b.read_text());bad=json.loads(d.read_text())
    observe('cold_replay',dict(commands=[first.returncode,replay.returncode,tamper.returncode],positive=same,negative=bad))
    assert first.returncode==replay.returncode==0
    assert same['complete_causal_record_equal'] is True
    assert same['result']['causal_replay_record']==old['result']['causal_replay_record']
    assert tamper.returncode==1
    assert bad['complete_causal_record_equal'] is False
    assert bad['result']['terminal']['status']!='COMMITTED'

# Coverage supplement frozen in 01B after the first independent court.
def test_two_material_lives_reach_same_endpoint_without_retrofit():
    rows=[]
    for units in [2,5]:
        e=history(world(units));r=replay_history(e);p=derive_psyche(e);acts=independent_actions(e,p)
        rows.append(dict(replay=r,psyche=p,actions=acts))
        assert r['valid'] is True
        assert forward_replay_to_endpoint(e,ec())['endpoint_match'] is True
        assert forward_replay_to_endpoint(e,ec('IMPOSSIBLE_SITE'))['endpoint_match'] is False
        assert acts['heldout_independence_pass'] is True
    observe('independent_material_lives',rows)
    assert [x['replay']['state']['completed_units'] for x in rows]==[2,3]
    assert [x['psyche']['practices'][0]['formed_value']['checks'] for x in rows]==[2,3]
    assert [x['actions']['probes'][0]['typed_action']['after']['completed_units'] for x in rows]==[3,4]
    assert rows[0]['replay']['state']['place']==rows[1]['replay']['state']['place']

def test_retry_empty_and_authority_outcomes_remain_distinct():
    data=inputs();good=run(deepcopy(data));assert good['terminal']['status']=='COMMITTED'
    bad_data=deepcopy(data)
    for c in bad_data['proposal_record'].parsed_candidates:c['endpoint_constraints']['required_state_predicates']=[dict(field='place',equals='IMPOSSIBLE_SITE')]
    bad=run(bad_data)
    empty=deepcopy(data);empty['world_forced_routes_impossible']=True;empty=run(empty)
    held=deepcopy(data);held['hold_missing_authority']='G16I_MISSING_EVENT_OWNER';held=run(held)
    ordinal=deepcopy(data);ordinal['ordinal_only_no_policy']=True;ordinal=run(ordinal)
    observe('retry_and_refusal_types',dict(exhausted=bad,empty=empty,held=held,ordinal=ordinal))
    assert bad['terminal']['status']=='HISTORY_SEARCH_EXHAUSTED'
    assert bad['construction_summary']['n_attempts']==4
    assert bad['terminal']['silent_resample_performed'] is False
    assert all(x['endpoint_match'] is False for x in bad['construction_summary']['attempts'])
    assert empty['terminal']['status']=='SCENARIOS_VALID_EMPTY'
    assert empty['selection_summary'] is None
    assert held['terminal']['status']=='NOT_EXECUTED_AUTHORITY_HOLD'
    assert held['terminal']['missing_authority']==['G16I_MISSING_EVENT_OWNER']
    assert ordinal['terminal']['status']=='SELECTION_AUTHORITY_UNBOUND'
    assert ordinal['terminal']['rng_draw_count']==0

def test_task_contact_preserves_unknown_views_and_native_limits():
    a,e,w,rel=relation_packet();result=run();observe('task_contact_native_limits',dict(relation=rel,terminal=result['terminal'],child=result['child_fixture'],boundary=result['boundary']))
    assert rel['relationship_committed'] is True
    assert len(rel['perceived_states'])==2
    assert {x['perceived_state'] for x in rel['perceived_states']}=={'UNKNOWN_OR_NONRECIPROCAL'}
    assert rel['reciprocity_inferred'] is False
    assert rel['household_membership_auto'] is False
    assert result['child_fixture']['exposures']==[]
    assert result['child_fixture']['child_generated_events']==0
    assert result['child_fixture']['is_admitted_child_actor'] is False
    assert result['boundary']['target_status']=='PENDING_NOT_ADMITTED_CONCEPTION'
    assert result['continuation']['parental_status']=='NOT_GRANTED'

def test_joined_terminal_refuses_material_overspend(monkeypatch):
    clean=run();assert clean['terminal']['status']=='COMMITTED'
    original=PersonHistoryBuilder.build
    def overspend(self):
        events=original(self)
        if self.role=='repair':
            project=deepcopy(next(e for e in events if e['kind']=='PROJECT'))
            project['effective_index']=80
            project['event_id']=h_obj({k:v for k,v in project.items() if k!='event_id'})
            events.append(project)
        return events
    monkeypatch.setattr(PersonHistoryBuilder,'build',overspend)
    bad=run();observe('joined_material_overspend',bad)
    available=next(e['payload']['material_units'] for e in bad['dad_events'] if e['kind']=='WORLD_MATERIAL')
    spent=sum(e['payload']['durable_effect']['materials_used'] for e in bad['dad_events'] if e['kind']=='PROJECT')
    assert spent>available
    assert bad['terminal']['status']!='COMMITTED'
