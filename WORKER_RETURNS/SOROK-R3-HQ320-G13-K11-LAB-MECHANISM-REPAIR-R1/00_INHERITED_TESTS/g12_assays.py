"""Independent bounded assays; no new actor, issuer or developmental implementation."""
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict,replace
from fractions import Fraction
import sys,json,hashlib
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'sources/sgi1/01_LAB_IMPLEMENTATION'))
sys.path.insert(0,str(ROOT/'sources'))
from lab_sgi1.construction import (DadHistoryBuilder,forward_replay_to_endpoint,
    psyche_from_dad_events,heldout_independent_probes,stopping_law_check,construct_second_parent)
from lab_sgi1.mother import build_mother_checkpoint
from lab_sgi1.proposal import build_proposal_prompt
from lab_sgi1.selection import adp020_select
from lab_sgi1.core import h_obj,ScopedRNG
from native_candidate import owner_transitions as owner,can008_candidate_rule as rule
from native_candidate.candidate_registry_fixture import CandidateRegistryFixture
from native_candidate.positive_chain import seal_event,run_positive_chain
from production import v3_psepf_zero_positive_guard as guard

def endpoint(place='INST_WORKSHOP_A'):
    return dict(route_kind_id='ROUTE_LOCAL_CLOSED',time_or_interval='T_ENCOUNTER_LAB_WINDOW',
                required_state_predicates=[dict(field='place',equals=place),
                                           dict(field='availability_status',equals='available_for_encounter')])

def independent_history(case):
    # Sourcefree court descriptions, explicitly not generated/admitted actor facts.
    project,friend,place = (('night_shift_union_safety_project','CO_WORKER_N','REMOTE_REPAIR_DEPOT')
                           if case=='A' else ('coastal_flood_relief_project','SIBLING_C','COASTAL_RESCUE_STATION'))
    def event(i,kind,payload,parents):
        return dict(event_id=f'G12_{case}_{i}',effective_index=i,kind=kind,
                    actors=[f'G12_PROVISIONAL_SECOND_PARENT_{case}'],payload=payload,
                    causal_parent_event_ids=parents)
    return [event(0,'PARTIAL_ROOT',{'antecedents':'UNKNOWN_EXPLICIT_ROOT'},[]),
            event(1,'WORK_POSITION',{'material_position':'independent_worker'},[f'G12_{case}_0']),
            event(2,'PROJECT',{'project':project,'nonmother':True,'durable_effect':'TEST_DESCRIPTION_ONLY'},[f'G12_{case}_1']),
            event(3,'NONMOTHER_RELATIONSHIP',{'counterpart':friend,'nonmother':True},[f'G12_{case}_0']),
            event(4,'COMMISSIONED_WORK',{'workplace':place},[f'G12_{case}_2']),
            event(5,'ENDPOINT_STATE',{'place':place,'availability_status':'unavailable'},[f'G12_{case}_4'])]

def strict_causal_oracle(events):
    seen={};errors=[]
    for e in events:
        if e['event_id'] in seen:errors.append('DUPLICATE_EVENT_ID')
        if any(p not in seen for p in e['causal_parent_event_ids']):errors.append('MISSING_OR_FUTURE_CAUSAL_PARENT')
        if any(seen[p]>=e['effective_index'] for p in e['causal_parent_event_ids'] if p in seen):errors.append('NONFORWARD_CAUSAL_PARENT')
        if e['effective_index'] in seen.values():errors.append('DUPLICATE_EFFECTIVE_INDEX')
        seen[e['event_id']]=e['effective_index']
    # Independently derive place only from an antecedent route event. ENDPOINT_STATE is a claim.
    place=None
    for e in events:
        if e['kind'] in ('ENROLLMENT','COMMISSIONED_WORK','COMMUNITY_CALLOUT','MOBILITY_HISTORY'):
            p=e['payload'];place=p.get('institution') or p.get('workplace') or p.get('body') or p.get('place')
        if e['kind']=='ENDPOINT_STATE' and e['payload'].get('place')!=place:errors.append('ENDPOINT_ASSERTION_WITHOUT_ANTECEDENT')
    return dict(accepted=not errors,errors=errors,derived_place=place)

def literal_attacks():
    ec=endpoint();base=DadHistoryBuilder('G12_PROVISIONAL','G12_FIXED_SEED',ec).build()
    attacks={}
    forged=deepcopy(base)
    forged[-1]['payload']['place']='UNREACHABLE_SITE'
    attacks['forged_endpoint']=(forged,endpoint('UNREACHABLE_SITE'))
    missing=deepcopy(base);missing[4]['causal_parent_event_ids']=['ABSENT_PARENT']
    attacks['missing_parent']=(missing,ec)
    future=deepcopy(base);future[0]['causal_parent_event_ids']=[future[-1]['event_id']]
    attacks['future_endpoint_as_root_parent']=(future,ec)
    duplicate=deepcopy(base);duplicate[1]['effective_index']=0
    attacks['duplicate_effective_index']=(duplicate,ec)
    removed=[e for e in deepcopy(base) if e['kind'] not in ('COMMISSIONED_WORK','ROUTE_AVAILABILITY')]
    attacks['route_antecedent_removed']=(removed,ec)
    return {k:dict(lab=forward_replay_to_endpoint(events,constraints),
                   independent=strict_causal_oracle(events),events=events,constraints=constraints)
            for k,(events,constraints) in attacks.items()}

def embargo_inputs():
    anchor=build_mother_checkpoint('G12_EMBARGO','M0').anchor_dict()
    clean_target={'target_status':'PENDING_NONCAUSAL'};clean_world={'world_id':'G12_WORLD'}
    sentinel='G12_FUTURE_CHILD_DESIRED_WOUND_SECRET'
    results={}
    for path in ('target','world','psyche'):
        a=deepcopy(anchor);t=deepcopy(clean_target);w=deepcopy(clean_world)
        dest=t if path=='target' else w if path=='world' else a['psyche']
        dest['future_child_desired_adversity_tag']=sentinel
        prompt=build_proposal_prompt(a,t,w,None,4)
        results[path]=dict(sentinel_visible=sentinel in prompt,prompt=prompt)
    return results

def native_controls():
    reg=CandidateRegistryFixture();rule.register_default_rule(reg);ctx=owner.FixtureOwnerState(reg);b=rule.build_default_binding()
    def event(eid,features,actor='ACTOR_SYNTH_1',**kwargs):
        return seal_event(event_id=eid,event_kind='EXTERNAL_RUNTIME_EVENT',
            issuer_authority_id='ISSUER_AUTH_WORLD_SCHED',issuer_authority_version='1',
            actor_scope=actor,world_ref='W_SYNTH_1998',world_as_of='1998-10-03T16:00:00Z',
            effective_causal_time='1998-10-03T16:00:00Z',public_features=features,
            admission_state='ADMITTED',**kwargs)
    def form(ev):
        return owner.adp016_form_causal_trace(actor_id=ctx.actor_id,basis_event=ev,
            trace_key='TRACE_FEEDBACK_WINDOW_EXPERIENCE',content_state='AVAILABLE_SOURCE_BOUND',
            owning_rule_id=b.rule_id,owning_rule_version=b.rule_version,owning_rule_hash=b.rule_content_hash,
            authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1',parent_state_hash=ctx.state_hash,context=ctx)
    control=event('G12_EXACT_FEEDBACK',('shift_feedback_window_open','supervisor_solicits_comment'))
    admitted=reg.admit_event(control);before=ctx.state_hash;proposal=form(control);commit=ctx.commit_memory(proposal)
    after=ctx.state_hash;replay=ctx.commit_memory(proposal)
    g=event('G12_GENEALOGY_PROJECT',('independent_union_project_undertaken',))
    g_admission=reg.admit_event(g);before_refusal=ctx.state_hash
    try:form(g);refusal='UNEXPECTED_ACCEPT'
    except owner.OwnerTransitionError as exc:refusal=exc.code
    wrong_actor=reg.admit_event(event('G12_OTHER_ACTOR',('independent_relief_project',),actor='G12_PROVISIONAL_SECOND_PARENT_B'))
    future_event=reg.admit_event(event('G12_FUTURE',('independent_union_project',),derived_from_future_partition=True))
    decisions={}
    for operation in ('ACTOR_INITIALIZATION','GENEALOGY_HISTORY_TRACE','CONCEPTION_OCCURRED','BIRTH_OCCURRED','CHILD_GENERATED'):
        fp=guard.GuardStateFingerprint('actor-hash','ledger-hash','0','rng-hash','scheduler-hash')
        request=guard.GuardRequest('G12_PROVISIONAL',guard.GuardedTruthClass.REPLAY_RECEIPT,
            'G12_SGI1_EXACT_REPLAY',h_obj({'source':'SGI1'}),(),f'G12.{operation}',operation,fp)
        d=guard.evaluate_psepf_zero_positive_guard(request)
        decisions[operation]={**asdict(d),'zero_effect':d.zero_effect}
    imports={}
    for name,m in sorted(sys.modules.items()):
        if name.startswith(('native_candidate.','production.')) and getattr(m,'__file__',None):
            p=Path(m.__file__);raw=p.read_bytes()
            imports[name]=dict(module_file=str(p.relative_to(ROOT)),git_blob_sha1=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
    return dict(control_admission=admitted,control_proposal=proposal,control_commit=commit,
        control_state_changed=before!=after,control_replay=replay,project_admission=g_admission,
        project_refusal=refusal,project_zero_mutation=ctx.state_hash==before_refusal,
        wrong_actor=wrong_actor,future_event=future_event,production=decisions,imports=imports,
        chain=run_positive_chain(),registry_empty=not bool(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES))

def observations():
    scenarios={}
    for name,variant in [('A','M0'),('B','M2')]:
        mother=build_mother_checkpoint('G12_MOTHER_'+name,variant);before=mother.hash()
        events=independent_history(name);ec=endpoint('INST_WORKSHOP_A' if name=='A' else 'INST_EVENING_CLASS_B')
        actual=forward_replay_to_endpoint(events,ec)
        scenarios[name]=dict(mother_before=before,mother_after=mother.hash(),mother=mother.anchor_dict(),
            prior_child_refs=mother.anchor_dict()['already_generated_child_refs'],history=events,
            oracle=strict_causal_oracle(events),replay=actual,conception='PENDING_NONCAUSAL',
            birth='NOT_ISSUED',child_generation='NOT_ISSUED',new_actor_created=False)
    ec=endpoint();base=DadHistoryBuilder('G12_PROVISIONAL','G12_FIXED_SEED',ec).build()
    corrupt=deepcopy(base);corrupt[4]['causal_parent_event_ids']=['ABSENT_PARENT']
    p=psyche_from_dad_events(corrupt);r=forward_replay_to_endpoint(corrupt,ec);probes=heldout_independent_probes(corrupt,p)
    stopping=stopping_law_check(corrupt,p,ec,r,probes)
    alien=deepcopy(base)
    for e in alien:
        if e['kind']=='PROJECT':e['payload']['project']='ARCHIVE_CATALOGUING_NO_REPAIR_SKILL'
        if e['kind']=='NONMOTHER_RELATIONSHIP':e['payload']['counterpart']='UNRELATED_SIBLING_NOT_BORROWER'
    alien_probes=heldout_independent_probes(alien,psyche_from_dad_events(alien))
    candidates=[dict(class_key='A',representative_id='A',payload='ORIGINAL'),dict(class_key='B',representative_id='B',payload='OTHER')]
    a=adp020_select('SIM_UNIFORM_CLASSES',candidates,'G12_SEED','G12_SCOPE')
    changed=deepcopy(candidates);changed[0]['payload']='MUTATED_HISTORY_REQUIREMENT'
    b=adp020_select('SIM_UNIFORM_CLASSES',changed,'G12_SEED','G12_SCOPE')
    failed=construct_second_parent({'class_key':'G12_IMPOSSIBLE'},endpoint('IMPOSSIBLE_SITE'),['A','B','C','D'])
    q=[Fraction(1,2),Fraction(1,2)];acceptance=[Fraction(1,1),Fraction(1,4)];norm=sum(x*y for x,y in zip(q,acceptance))
    return dict(scenarios=scenarios,attacks=literal_attacks(),embargo=embargo_inputs(),stopping_corrupt=stopping,
        alien_probes=alien_probes,candidate_payload={'before':a,'after':b},retry=failed,
        survivor_fractions=[str(x*y/norm) for x,y in zip(q,acceptance)],
        rng_algorithm={'actual':'SHA256_CONCAT_MODULO','required':'ADP020_HMAC_SHA256_UNIFORM_BELOW_V1@1.0.0',
                       'root_32_bytes_required_by_lab':False,'rejection_mapping_implemented':False},
        empty=adp020_select('SIM_UNIFORM_CLASSES',[],'G12','S'),
        singleton=adp020_select('SIM_UNIFORM_CLASSES',candidates[:1],'G12','S'),
        unissued=adp020_select('UNISSUED_POLICY',candidates,'G12','S'),native=native_controls())

def save():
    result=observations();(ROOT/'evidence/g12_observations.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');return result
if __name__=='__main__':
    x=save();print(json.dumps({'scenarios':len(x['scenarios']),'attacks':len(x['attacks']),'native_positive_grade':'CANDIDATE_FIXTURE_ONLY','production_registry_empty':x['native']['registry_empty']}))
