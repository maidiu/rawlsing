"""CLR3: actual historical V3 recurrence + explicitly provisional canon contract.

No new numerical psychology. Existing legacy formulas remain unadopted. The
closed-grammar narrator and history/exposure policy are research mocks, not
native ADP owners or arbitrary-natural-language semantic validation.
"""
from __future__ import annotations
from dataclasses import asdict
from copy import deepcopy
from pathlib import Path
import hashlib,json,random,sys
from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parent
# Reuse the frozen reviewed source closure; only this research wrapper changes.
SOURCE_ROOT=ROOT.parents[1]/'reconstructed/clr3'
sys.path.insert(0,str(SOURCE_ROOT/'sources/legacy'))
sys.path.insert(0,str(SOURCE_ROOT/'sources'))
from v3.core.state import BackboneState,DomainState
from v3.core.enums import DOMAIN_NAMES
from v3.core.derived import compute_all_derived
from v3.core.config_loader import load_v3config,load_step_order
from v3.engine.yearly_step import run_one_year
from v3.engine.effects.delta_templates import delta_from_event,merge_deltas,apply_deltas_to_state,build_state_deltas_applied_summary
from v3.engine.llm_contract import parse_candidate_packet,build_render_packet,state_summary_from_backbone
import r1_world

GRADE='PROVISIONAL_HISTORICAL_RECURRENCE_AND_RESEARCH_CANON; NATIVE_OWNER_INTERFACES_UNISSUED'


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def require(condition,code):
    if not condition:raise ValueError(code)


def named_choice(seed,name,values):
    derived=int(digest([seed,name]),16)
    index=random.Random(derived).randrange(len(values))
    return values[index],dict(stream=name,seed_commitment=digest([seed,name]),index=index,value=values[index],empirical_probability=False)


def initial_state():
    # Defaults come from the actual recovered schema, not a newly invented trait
    # system. Every value is explicitly a synthetic fixture, not a generated life.
    state=BackboneState(year=2006,age=6,domains={n:DomainState() for n in DOMAIN_NAMES})
    state.initial_state_provenance={'grade':'SYNTHETIC_LEGACY_SCHEMA_DEFAULT_FIXTURE','source':'TD_R05 member-hash-matched BackboneState and DomainState','not_generated_actor':True}
    return state


def config_and_order():
    config=load_v3config()
    # Suppress rejected generic pseudo-event sampling, not ordinary V3 dynamics.
    # Existing source supports max_events=0. No numerical formula is replaced.
    config.setdefault('execution',{})['max_events_per_year']=0
    config['seed']=20261018
    return config,load_step_order()


def changes(before,after):
    return [key for key in before if before[key]!=after[key]]


def numeric_changes(before,after,prefix=''):
    result=[]
    if isinstance(before,dict) and isinstance(after,dict):
        for key in before.keys() & after.keys():result.extend(numeric_changes(before[key],after[key],prefix+'.'+key if prefix else key))
    elif isinstance(before,list) and isinstance(after,list):
        for i,(a,b) in enumerate(zip(before,after)):result.extend(numeric_changes(a,b,f'{prefix}[{i}]'))
    elif isinstance(before,(int,float)) and not isinstance(before,bool) and isinstance(after,(int,float)) and before!=after:
        result.append(dict(path=prefix,before=before,after=after))
    return sorted(result,key=lambda x:x['path'])


@contextmanager
def recorded_engine_rng(year):
    """Inject explicit seeded streams at legacy random-module boundaries.

    No numerical update/formula changes. Default-constructed RNGs get named
    replay seeds; explicit source seeds are retained. Each used output is saved.
    This adapter is sequential, not thread safe and is not native ADP020.
    """
    from v3.engine import striving_objects
    from v3.engine.effects import metabolization_effects
    from v3.systems import autonomy_safety
    records=[]
    class TracedRandom:
        def __init__(self,rng,namespace,instance):self.rng=rng;self.namespace=namespace;self.instance=instance
        def __getattr__(self,name):
            member=getattr(self.rng,name)
            if not callable(member):return member
            def draw(*args,**kwargs):
                result=member(*args,**kwargs)
                records.append(dict(namespace=self.namespace,instance=self.instance,operation=name,args=deepcopy(args),kwargs=deepcopy(kwargs),output=deepcopy(result)))
                return result
            return draw
    def facade(namespace):
        counter=[0]
        def factory(seed=None):
            n=counter[0];counter[0]+=1
            actual=seed if seed is not None else int(digest(['legacy-rng',year,namespace,n]),16)
            records.append(dict(namespace=namespace,instance=n,operation='Random',seed=actual,source_seed_was_explicit=seed is not None))
            return TracedRandom(random.Random(actual),namespace,n)
        global_stream=factory(int(digest(['legacy-global',year,namespace]),16))
        return SimpleNamespace(Random=factory,random=global_stream.random,choices=global_stream.choices,choice=global_stream.choice,uniform=global_stream.uniform,randint=global_stream.randint)
    with patch.object(striving_objects,'random',facade('striving')),patch.object(metabolization_effects,'random',facade('metabolization')),patch.object(autonomy_safety,'random',facade('ordinary-drift')):
        yield records


def advance(state,config,order,clock,label):
    before=asdict(state);d=compute_all_derived(state)
    with recorded_engine_rng(state.year) as rng_outputs:
        run_one_year(state,d,config,order)
    after=asdict(state)
    return dict(clock=clock,stage=label,before=before,after=after,before_hash=digest(before),after_hash=digest(after),changed_sections=changes(before,after),numeric_changes=numeric_changes(before,after),derived=asdict(d),executed='v3.engine.yearly_step.run_one_year',rng_outputs=rng_outputs,pressure_status=state.yearly_integrity.get('pressure_flow',{}).get('status'))


def event(id,kind,**extra):
    return dict(id=id,kind=kind,label=id,logline=id,intensity='minor',channels=['family'],implicated={'domains':['family_household','body_self']},hooks={'wound_hooks':[],'capacity_hooks':[]},magnets={'offers':[],'costs':[]},**extra)


def admit_first_proposal(packet,state):
    def inspect(value):
        if isinstance(value,dict):
            for key,child in value.items():
                require(key not in {'desired_personality','target_personality','persona_outcome','capacity_deltas','wound_deltas','domain_deltas'},'ENDPOINT_OR_DIRECT_STATE_WRITE_FORBIDDEN')
                if key in {'branch_hypotheses','trajectory_branches'}:require(not child,'ENDPOINT_BRANCH_FORBIDDEN')
                inspect(child)
        elif isinstance(value,list):
            for child in value:inspect(child)
    inspect(packet)
    require(packet.get('age')==state.age and packet.get('year')==state.year,'PROPOSAL_CONTEXT_MISMATCH')
    return parse_candidate_packet(packet)


def propose_situations(state):
    packet=dict(year=state.year,age=state.age,event_candidates=[event('bike-missing','loss'),event('actual-shared-attention','relationship'),event('later-lock-practice','practice')],magnet_candidates=[],branch_hypotheses=[])
    packet['event_candidates'][1]['magnets']['offers']=['care']
    return dict(authority='RECORDED_MOCK_NOT_ISSUED_CAN008',confidence='UNCALIBRATED',conditioning={'state_hash':digest(asdict(state)),'age':state.age,'habitus_contract':'UNISSUED; legacy field/calibration projection only'},raw_packet=packet,legacy_parsed_packet=admit_first_proposal(packet,state),situational_options=[dict(workplace=w,material=r1_world.work_facts(w),issuer='INDEPENDENT_EMPLOYER_FIXTURE') for w in r1_world.WORK_OUTCOMES],state_summary=state_summary_from_backbone(state,compute_all_derived(state)))


def apply_existing_events(state,selected,config,clock):
    before=asdict(state)
    deltas=merge_deltas([delta_from_event(e,config) for e in selected])
    apply_deltas_to_state(state,deltas,config,selected_events=selected)
    derived=compute_all_derived(state)
    after=asdict(state)
    return dict(clock=clock,before=before,after=after,before_hash=digest(before),after_hash=digest(after),selected_events=deepcopy(selected),legacy_deltas=deltas,changed_sections=changes(before,after),numeric_changes=numeric_changes(before,after),derived=asdict(derived),executed='legacy delta_from_event -> apply_deltas_to_state -> compute_all_derived',qualified_psychological_law=False)


def render_text(facts,variant):
    location={'hall_drawer':'hall drawer','garage_shelf':'garage shelf'}[facts['lock_location']]
    father='Father was present for a conversation.' if facts['father_present'] else 'Father was still at work.'
    if variant=='plain':return f'The bicycle was missing. The child saw the existing lock in the {location}. {father}'
    if variant=='alternate':return f'At home after discovering the missing bicycle, the child noticed the existing lock in the {location}. {father}'
    raise ValueError('UNSUPPORTED_RENDER_VARIANT')


def propose_realization(frame,location='hall_drawer',variant='plain'):
    facts=dict(bicycle_missing=True,father_present=frame['resolved']['father_present'],lock_location=location,lock_id='existing-lock',actor_observed=True)
    return dict(actor='child',clock=24,source_ref=frame['id'],prestate_hash=frame['effect']['before_hash'],poststate_hash=frame['effect']['after_hash'],facts=facts,psychological_changes={},variant=variant,text=render_text(facts,variant))


def validate_source_encounter(frame):
    """Check the existing fixture's encounter account before canon admission.

    This is not a new response rule or validation of arbitrary psychological
    computation. The recorded shared-attention event and the resolved presence
    flag must describe the same encounter; the existing event's kind/care offer
    and, when supplied, its material-time account must agree as well.
    """
    present=frame['resolved']['father_present']
    require(isinstance(present,bool),'SOURCE_ENCOUNTER_MISMATCH')
    selected=frame['effect']['selected_events']
    attention=[e for e in selected if e.get('id')=='actual-shared-attention']
    require(len(attention)<=1 and bool(attention)==present,'SOURCE_ENCOUNTER_MISMATCH')
    if attention:
        e=attention[0]
        require(e.get('kind')=='relationship' and 'care' in (e.get('magnets') or {}).get('offers',[]),'SOURCE_ENCOUNTER_MISMATCH')
    response=frame['resolved'].get('father_response')
    if response is not None:
        require((response['available_minutes']>=10)==present,'SOURCE_ENCOUNTER_MISMATCH')


def validate_canon_consistency(prior,entry):
    """One ledger is one research world; same-time particulars must agree."""
    for previous in prior:
        if previous['kind']!='REALIZATION' or previous['clock']!=entry['clock']:
            continue
        a,b=previous['facts'],entry['facts']
        if a['lock_id']==b['lock_id']:
            require(a['lock_location']==b['lock_location'],'CANON_OBJECT_LOCATION_CONFLICT')
        if previous['actor']==entry['actor']:
            require(a['father_present']==b['father_present'],'CANON_ACTOR_FACT_CONFLICT')


class CanonLedger:
    """Append-only test-only archive, with complete source preimages, not actor mind."""
    def __init__(self):self._entries=[];self._sources={}
    @property
    def entries(self):return deepcopy(self._entries)
    def verify(self):
        for index,e in enumerate(self._entries):
            body={k:v for k,v in e.items() if k!='hash'}
            require(digest(body)==e['hash'],'HISTORY_REWRITE')
            if e['kind']=='REALIZATION':
                require(e['source_ref'] in self._sources,'SOURCE_MISSING')
                require(digest(self._sources[e['source_ref']])==e['source_hash'],'SOURCE_PREIMAGE_REWRITE')
                validate_source_encounter(self._sources[e['source_ref']])
                validate_canon_consistency(self._entries[:index],e)
        return True
    def admit(self,frame,candidate):
        self.verify()
        require(frame['id'] not in self._sources,'SOURCE_ID_REUSE')
        require(candidate['source_ref']==frame['id'],'SOURCE_REF_MISMATCH')
        require(candidate['clock']>=frame['effect']['clock'],'FUTURE_SOURCE')
        require(candidate['actor']=='child','ACTOR_MISMATCH')
        require(candidate['prestate_hash']==frame['effect']['before_hash'] and candidate['poststate_hash']==frame['effect']['after_hash'],'STATE_MISMATCH')
        require(digest(frame['effect']['before'])==candidate['prestate_hash'] and digest(frame['effect']['after'])==candidate['poststate_hash'],'STATE_SNAPSHOT_REWRITE')
        validate_source_encounter(frame)
        require(isinstance(candidate['psychological_changes'],dict) and not candidate['psychological_changes'],'UNSUPPORTED_PSYCHOLOGICAL_CHANGE')
        require(set(candidate)=={'actor','clock','source_ref','prestate_hash','poststate_hash','facts','psychological_changes','variant','text'},'UNSUPPORTED_REALIZATION_FIELD')
        f=candidate['facts'];require(set(f)=={'bicycle_missing','father_present','lock_location','lock_id','actor_observed'},'UNSUPPORTED_FACT')
        require(f['bicycle_missing'] is True and isinstance(f['father_present'],bool) and f['father_present']==frame['resolved']['father_present'],'CONTRADICTORY_WORLD_FACT')
        require(f['lock_id']==frame['world']['lock_id'] and f['lock_location'] in frame['world']['available_storage_slots'],'INCOMPATIBLE_OBJECT_DETAIL')
        require(f['actor_observed'] is True and frame['resolved']['child_at_home'],'UNWITNESSED_ACCESS')
        require(candidate['text']==render_text(f,candidate['variant']),'PROSE_NOT_SUPPORTED_BY_TYPED_REALIZATION')
        body=dict(id='canon:'+str(len(self._entries)),kind='REALIZATION',source_ref=frame['id'],source_hash=digest(frame),prestate_hash=candidate['prestate_hash'],poststate_hash=candidate['poststate_hash'],actor='child',clock=candidate['clock'],facts=deepcopy(f),text=candidate['text'],grade='RESEARCH_CANON_NOT_NATIVE_ADP016_OR_ACTOR_MEMORY')
        validate_canon_consistency(self._entries,body)
        body['hash']=digest(body)
        # Both validations precede either write: a refused source reserves no ID
        # and cannot leave an orphan preimage or partial canon append.
        self._sources[frame['id']]=deepcopy(frame)
        self._entries.append(body);return deepcopy(body)
    def append_unrelated(self,clock=25):
        self.verify();body=dict(id='audit:'+str(len(self._entries)),kind='UNRELATED_OTHER_PROJECT',actor='neighbor',clock=clock,facts={'project':'library_inventory'},numerical_effect=None)
        body['hash']=digest(body);self._entries.append(body);return deepcopy(body)
    def later_consume(self,canon_id,clock=31,actor='child',busy=True):
        self.verify();entry=next((e for e in self._entries if e['id']==canon_id),None)
        require(entry is not None,'CANON_REF_MISSING')
        require(entry['kind']=='REALIZATION' and entry['actor']==actor,'HISTORY_ACCESS_DENIED')
        require(entry['clock']<clock,'FUTURE_CANON_READ')
        # This actor-accessible physical detail is actually used to construct the
        # later observable action. No latent disposition is inferred from prose.
        place=entry['facts']['lock_location']
        return dict(clock=clock,actor=actor,action='FETCH_EXISTING_LOCK',target_location=place,lock_id=entry['facts']['lock_id'],canon_read=dict(id=canon_id,hash=entry['hash'],field='facts.lock_location',value=place),counterpart=dict(actor='neighbor',independent_project='library_inventory',action='DECLINE_CONTACT' if busy else 'ALLOW_CONTACT',focal_child_state_read=False),grade='MOCK_ACCESS_POLICY_AND_WORLD_TASK_NOT_PSYCHOLOGICAL_SELECTION')


def request_native_trajectory():
    """Explicit missing-owner path; never silently substitute the legacy replay."""
    return dict(status='BLOCKED_OWNER',executed=False,legacy_fallback=False,missing=['qualified initialization/age/habitus API','accepted ADP021 scheduler','concrete CAN008/CAN011 transition rules and target grants','ADP019 narrative admission','ADP016/017 memory/access implementations','registered ADP020 stream/rate contract'],semantic_contracts_may_exist=True)


def run_trajectory(workplace='ROUTINE',seed=23,location=None,variant='plain',father=None,busy=True):
    state=initial_state();config,order=config_and_order();initial=asdict(state)
    ticks=[advance(state,config,order,10,'ordinary_before_1'),advance(state,config,order,20,'ordinary_before_2')]
    pre_encounter=asdict(state);proposal=propose_situations(state)
    draw,work_rng=named_choice(seed,'employer',list(r1_world.WORK_OUTCOMES))
    chosen=workplace if workplace is not None else draw
    work=r1_world.work_facts(chosen);history=father or r1_world.FatherHistory()
    response=r1_world.father_action(work,history,175,18)
    lock_location,narrative_rng=named_choice(seed,'narrative_detail',['hall_drawer','garage_shelf'])
    unrelated,neighbor_rng=named_choice(seed,'neighbor_project',['inventory','catalogue'])
    world=dict(theft={'id':'theft','clock':22,'object':'child-bike','culprit':'UNKNOWN'},spare_bike_id='shared-household-spare',lock_id='existing-lock',available_storage_slots=['hall_drawer','garage_shelf'],initial_biographies={'father':asdict(history),'child':'actual legacy synthetic initial state','neighbor':'library worker'},pressure_config_hash=digest(config))
    resolved=dict(workplace={'clock':21,'facts':work,'independent_of_theft':True},father_response=response,father_present=response['available_minutes']>=10,child_at_home=True,encounter_clock=23,neighbor_activity={'clock':25,'project':unrelated,'independent_of_child':True})
    events=proposal['legacy_parsed_packet']['event_candidates']
    selected=[events[0]]+([events[1]] if resolved['father_present'] else [])
    effect=apply_existing_events(state,selected,config,23)
    render_packet=build_render_packet(state.year,state.age,selected,[],build_state_deltas_applied_summary(effect['legacy_deltas']),{'no_unsupported_psychological_changes':True})
    frame=dict(id='episode-theft',world=world,resolved=resolved,effect=effect,proposal=proposal,render_packet=render_packet)
    narrative_input=dict(before=effect['before'],after=effect['after'],resolved=resolved,legacy_render_packet=render_packet,constraints={'objective_theft_fixed':True,'no_additional_psychological_change':True,'compatible_substantive_details_allowed':True})
    ledger=CanonLedger();candidate=propose_realization(frame,location or lock_location,variant)
    before_narration=digest(asdict(state));accepted=ledger.admit(frame,candidate)
    require(digest(asdict(state))==before_narration,'NARRATOR_MUTATED_ENGINE')
    preserved=deepcopy(effect)
    ledger.append_unrelated()
    ticks.append(advance(state,config,order,30,'ordinary_after_encounter'))
    later=ledger.later_consume(accepted['id'],busy=busy)
    later_event=event('observed-lock-task','practice')
    delayed=apply_existing_events(state,[later_event],config,32)
    delayed['actual_activity_source']=deepcopy(later)
    ticks.append(advance(state,config,order,40,'ordinary_after_feedback'))
    require(effect==preserved,'PAST_SNAPSHOT_CHANGED')
    record=dict(grade=GRADE,native_grade='CONTRACT_HOLD_MISSING_OWNER_API',initial=initial,pre_encounter=pre_encounter,world=world,proposal=proposal,resolved=resolved,immediate=effect,narrative_input=narrative_input,recorded_second_call=candidate,canon=ledger.entries,source_preimages=deepcopy(ledger._sources),later=later,delayed_feedback=delayed,ticks=ticks,final_state=asdict(state),rng=[dict(**work_rng,intervention=workplace),narrative_rng,neighbor_rng],policy_limits=['legacy numerical templates unadopted','annual time, not a qualified hybrid scheduler','closed grammar, not general semantic fidelity','test-only canon/access, native grants UNISSUED','synthetic default initialization and field/habitus projection, not generated person'])
    record['trace_hash']=digest(record);return record


if __name__=='__main__':
    print(json.dumps(run_trajectory(),sort_keys=True))
