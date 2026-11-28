"""R34: a joined, persistent household course, not a new psychology.

Sourcefree scenario + hermetic semantic transport. F/E compare reversible
transport; P is a deliberately experimental developmental packet, never the
runtime's default or an authority for admission. Lbad is a destructive
control. No remote processor, token estimate, human learning claim, or
counterfeit visitor psyche. All actual development goes through CO admission.
"""
from collections import Counter, defaultdict
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
for path in (ROOT, ROOT / 'SEAM' / 'ORACLE' / 'UM_SOROK_ORGANISM_R3',
             ROOT / 'WORKER_RETURNS' / 'SOROK-P5-CONTINUOUS-EXPERIENCE-R1',
             ROOT / 'WORKER_RETURNS' / 'SOROK-P6-ONE-LIVING-HOUSE-R1',
             ROOT / 'WORKER_RETURNS' / 'SOROK-P4-CORE-LOOP-R1'):
    sys.path.insert(0, str(path))
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    HeuristicSemanticProvider, ValidatingSemanticService)
from um_sorok_organism.live_psychological_llm import (
    ExplicitJSONLLMProvider, _expand_exact_aliases, _expand_structured_fields)
from um_sorok_organism.psychic_genesis import PRODUCTIVE_VOCAL_FAMILY
from um_sorok_organism.types import canonical, digest
from neighbor_runtime import NeighborEncounter
import mii

ARMS = ('F', 'E', 'P', 'Lbad', 'F_abstain')
SEED = {'source_ref':'SOURCEFREE_R34_PARENT_NOT_PYAT',
        'answers':{'fictional':'not survey evidence'},
        'fictional_seed':{'projects':[{'object':'ordinary speech',
            'means':['SPEAK'],'priority':.2,'cue_terms':['home']},
            {'object':'ordinary material production','means':['MAKE_OBJECT'],
             'priority':.5,'cue_terms':['home']}]}}
MOTHER = {'source_ref':'SOURCEFREE_R34_MOTHER_NOT_PYAT',
          'answers':{'fictional':'not survey evidence'},
          'fictional_seed':{'projects':[{'object':'vocal practice',
              'means':['SING'],'priority':.5,'cue_terms':['sing']}]}}

def size(value):
    return len(canonical(value).encode('utf-8'))

def require(ok, label):
    # Still enforced under python -O.
    if not ok:
        raise RuntimeError(label)

def developmental_projection(packet, ordinal):
    """Only remove elaborate practical enumeration; retain all other fields.

    Independent periodic full expansion and rotating exact peripheral row
    are experimental sampling, NOT evidence of semantic sufficiency.
    No new source, actor permission, perception or claim of actual attention.
    """
    selected = packet.get('selected_constitution')
    if (ordinal % 4 == 0 or not isinstance(selected, dict)
            or not isinstance(selected.get('candidate_actions'), list)):
        return deepcopy(packet), 'FULL_PERIODIC_OR_NO_ROSTER'
    reduced = deepcopy(packet)
    roster = reduced['selected_constitution'].pop('candidate_actions')
    summaries = []
    for row in roster:
        options = row.get('practical_alternatives', [])
        if not isinstance(options, list):
            return deepcopy(packet), 'FULL_UNSUPPORTED_SHAPE'
        summaries.append({
            'action':row.get('action'),
            'psychodynamic_status':row.get('psychodynamic_status'),
            'qualified_alternative_count':len(options),
            'binding_status_counts':dict(Counter(
                str(x.get('binding_status','UNSPECIFIED')) for x in options)),
            'trial_count':len(row.get('possible_end_trials',[])),
        })
    reduced['developmental_roster_projection_analytic_only'] = {
        'scope':'SAME_ACTOR_SAME_CALL_NONEXHAUSTIVE_ANALYTIC_VIEW',
        'summary':summaries,
        'periodic_full_expansion_every':4,
        'peripheral_exact_row':deepcopy(roster[(ordinal-1)%len(roster)])
            if roster else None,
        'not_actor_apprehension_or_new_evidence':True,
        'unexpanded_rows_remain_in_canonical_owner':True}
    # Never send a larger candidate projection merely to claim economy.
    if size(reduced) >= size(packet):
        return deepcopy(packet), 'FULL_NO_BYTE_GAIN'
    return reduced, 'PROJECTED_ROTATING_PERIPHERY'

class CourseWire:
    """Use the existing real wire compiler and receipt metrics, mock transport."""
    def __init__(self, arm, callback):
        require(arm in ARMS, 'UNKNOWN_ARM')
        self.arm = arm
        self.ordinal = 0
        self.routes = Counter()
        self.original_bytes = Counter()
        self.witness = []
        def transport(request):
            body = json.loads(request['messages'][1]['content'])
            task = body['task']
            packet = _expand_exact_aliases(task, body['actor_source_packet'],
                body.get('same_call_exact_aliases',{}))
            packet = _expand_structured_fields(task,packet,
                body.get('reconstructed_fields',{}))
            if task == 'expression':
                accessible = packet.get('actor_accessible',{})
                selection = accessible.get('own_practical_selection') or {}
                require('cross_object_attention_analytic_only' not in selection,
                        'ANALYTIC_ATTENTION_LEAK')
                require('developmental_roster_projection_analytic_only' not in packet,
                        'DEVELOPMENTAL_PROJECTION_LEAK')
            answer = callback(task, packet)
            self.witness.append((task,digest(packet),digest(answer)))
            return {'choices':[{'message':{'content':canonical(answer)}}]}
        self.wire = ExplicitJSONLLMProvider(
            endpoint='https://example.invalid/chat/completions',
            model='sourcefree-r34-fixture',api_key='not-a-key',
            allow_private_actor_data=True,transport=transport,
            compact_exact_packet=arm in ('E','P'),
            compact_structured_packet=arm in ('E','P'),
            metrics_capacity=10000,profile_semantic_demand=True)
        self.grade = self.wire.grade

    def propose(self, task, packet):
        self.original_bytes[task] += size(packet)
        if task == 'development':
            self.ordinal += 1
            if self.arm == 'P':
                packet, route = developmental_projection(packet,self.ordinal)
                self.routes[route] += 1
            elif self.arm == 'Lbad':
                # Intentionally crippled, not a candidate for receiving.
                packet = {k:deepcopy(packet[k]) for k in
                          ('actor','clock','experience') if k in packet}
                self.routes['DESTRUCTIVE_SELECTED_ACTIVITY_CONTROL'] += 1
        return self.wire.propose(task,packet)

    def stats(self):
        snap = self.wire.usage_snapshot()
        require(snap['evicted']==0,'INCOMPLETE_USAGE_RECEIPTS')
        totals = defaultdict(lambda:dict(calls=0,packet_bytes=0,request_bytes=0))
        for receipt in snap['receipts']:
            require(receipt['transport']=='MOCK','UNEXPECTED_REMOTE_CALL')
            require(receipt['usage']['input_tokens'] is None,'INVENTED_TOKEN_COUNT')
            row = totals[receipt['task']]
            row['calls'] += 1
            row['packet_bytes'] += receipt['packet_bytes']
            row['request_bytes'] += receipt['request_bytes']
        return {'by_task':dict(totals),'original_packet_bytes':dict(self.original_bytes),
                'projection_routes':dict(self.routes),'provider_tokens':None}

def run_course(db, arm, *, routine_admission=None):
    """Two connected organs in one real household/ledger over elapsed life.

    Material course: actual demonstration/inspection -> acquired apprehension
    -> OTHER's independent new production -> newly situated inspection ->
    possible end -> distinct trial/reencounter -> new project -> repeated use.
    Reciprocal course: own vocal activity -> acquired project -> independently
    heard exercise refunctions mother's existing undertaking -> later ORIENT.
    Distinct causal chains share one continuing person, not a claim that the
    material project causes the vocal project or vice versa.
    """
    phase = 'old'
    new = None
    fallback = HeuristicSemanticProvider()
    acquired = arm not in ('Lbad','F_abstain')
    observed = []
    routine_threshold=None
    routine_result=None
    def policy(task,p):
        aid = p.get('actor',{}).get('id')
        if task == 'adult_constructor':
            return fallback.propose(task,p)
        if task == 'expression':
            return {'task':task,'surface':'Ordinary activity continues.'}
        if task == 'development':
            if arm=='F_abstain':
                return {'task':task,'candidates':[]}
            if aid=='mother' and phase=='vocal-project':
                return {'task':task,'candidates':p.get(
                    'historically_possible_productive_witness_reorganizations',[])}
            if aid!='nadia':
                return {'task':task,'candidates':[]}
            if phase=='old':
                return {'task':task,'candidates':p.get(
                    'historically_possible_cultural_references',[])}
            if phase=='new':
                q=p.get('historically_possible_cross_object_significance',[])
                if q:
                    return {'task':task,'candidates':[{
                        'kind':'NOTICE_POSSIBLE_END',
                        'perceived_cue_ref':q[0]['source_cue_ref'],
                        'origin_material_object_ref':q[0]['world_material_object_ref'],
                        'possible_object':'discover how different made things can be cared for',
                        'possible_means':['INSPECT'],'cue_terms':['material_object'],
                        'incidental_object_end_basis':deepcopy(q[0]['incidental_object_end_basis'])}]}
            if phase=='takeup':
                q=p.get('historically_possible_incidental_takeup',[])
                if q:
                    return {'task':task,'candidates':[{
                        'kind':'TAKE_UP_POSSIBLE_END',
                        'possible_end_ref':q[0]['possible_end_ref'],
                        'later_perceived_cue_ref':q[0]['later_perceived_cue_ref'],
                        'incidental_takeup_basis':q[0],'means':['INSPECT']}]}
            if phase=='vocal-own':
                return {'task':task,'candidates':[x for x in p.get(
                    'historically_possible_genetic_ends',[])
                    if x.get('genesis_family')==PRODUCTIVE_VOCAL_FAMILY]}
            if phase=='vocal-takeup':
                return {'task':task,'candidates':p.get(
                    'historically_possible_productive_vocal_takeups',[])}
            if phase=='routine-vocal' and routine_admission:
                rows=[x for x in p.get('historically_possible_recurrent_routines',[])
                      if x['basis']['operation']=='SING']
                if rows:
                    return {'task':task,'candidates':[{
                        'kind':'ACQUIRE_RECURRENT_ROUTINE','basis':rows[0]['basis'],
                        'window_days':60,'hours_per_active_day':2.,
                        'provisional_exposure_fraction':.75}]}
            return {'task':task,'candidates':[]}
        if task=='actor_attempt':
            rows=p.get('practical_options',[])
            def choose(predicate):
                opts=[x for x in rows if predicate(x)]
                return ({'task':task,'practical_option_id':opts[0]['option_id']}
                        if opts else {'task':task,'action':'WAIT'})
            if aid=='father':
                return {'task':task,'action':'MAKE_OBJECT' if phase=='make-new' else 'REST'}
            if aid=='mother':
                if p.get('requesting_actor'):
                    return choose(lambda x:x.get('operation')=='SING' and x.get('project_id'))
                if phase=='receive':
                    return choose(lambda x:x.get('productive_witness_attention'))
                return {'task':task,'action':'REST'}
            if phase=='old':
                return fallback.propose(task,p)
            if phase=='new':
                return choose(lambda x:x.get('cross_object_attention_analytic_only'))
            if phase in ('trial','vocal-trial'):
                ts=[x for x in p.get('possible_end_trials',[])
                    if (x.get('source_material_object_ref')==new
                        if phase=='trial' else x.get('operation')=='SING')]
                return ({'task':task,'possible_end_trial_id':ts[0]['trial_id']}
                        if ts else {'task':task,'action':'WAIT'})
            if phase in ('takeup','material-project'):
                if not acquired:
                    return {'task':task,'action':'WAIT'}
                return choose(lambda x:x.get('operation')=='INSPECT'
                    and x.get('world_request',{}).get('material_object_ref')==new
                    and bool(x.get('project_id'))==(phase=='material-project'))
            if phase in ('vocal-project','routine-vocal'):
                return choose(lambda x:x.get('operation')=='SING' and x.get('project_id'))
            if phase=='routine-rest':return {'task':task,'action':'REST'}
            if phase=='routine-late':
                # A controlled policy exercises a facility-sensitive choice.
                # No claim that this estimate is conscious self-knowledge.
                value=next((x['situated_component_facility']['technical_component_facility_estimate']
                            for x in p['options'] if x['action']=='SING'),None)
                if value is not None and value>routine_threshold:
                    return choose(lambda x:x.get('operation')=='SING' and x.get('project_id'))
                return {'task':task,'action':'WAIT'}
            if phase in ('vocal-own','vocal-takeup'):
                return {'task':task,'action':'SING'}
            return {'task':task,'action':'WAIT'}
        raise AssertionError(task)

    wire = CourseWire(arm,policy)
    semantic = ValidatingSemanticService(wire)
    rt = ConstitutiveRuntime(str(db),semantic=semantic)
    def beat(actor, expected=None):
        result=n.independent_actor_beat(actor)
        require(result.get('selection_grade')!='INJECTED_NOT_NATIVE_ACTOR_CHOICE',
                'INDEPENDENT_SELECTION_BYPASSED')
        if expected:
            require(result['attempt']==expected and result['status']=='PERFORMED',
                    'EXPECTED_PERFORMED_'+expected+':'+str(result.get('attempt'))+':'+str(result.get('status')))
        observed.append((actor,result['attempt'],result['status']))
        return result
    def cold():
        nonlocal rt,n
        rt.close()
        rt=ConstitutiveRuntime(str(db),semantic=semantic)
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        require(rt.verify()['valid'],'COLD_CHAIN')
    try:
        rt.initialize([('father','Father',SEED),('mother','Mother',MOTHER)])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
                'hearing':True,'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{aid:{'facing':'entrance','visual':True,
                'light':'lit','sightline':'unobstructed','hearing':True,
                'sound_path':'audible'} for aid in ('father','mother','nadia')}},
            request_id='geometry')
        require(n.contribute('enter','MOVE',destination='home')['status']=='PERFORMED',
                'VISITOR_ENTRY')
        # Two explicitly stipulated initial acts, not autonomous selection evidence.
        require(rt.step('father',requested_action='MAKE_OBJECT')['status']=='PERFORMED',
                'FIRST_ARTIFACT')
        old=next(iter(rt.ledger.world('w1')[1]['material_objects']))
        require(rt.step('father',requested_action='SPEAK',object_ref=old)['status']=='PERFORMED',
                'ACTUAL_REFERENCE')
        beat('nadia','INSPECT')
        require(len(rt.snapshot('nadia')['cultural_reference_practices'])==int(acquired),
                'CULTURAL_ACQUISITION')
        require(not rt.snapshot('nadia')['possible_ends'],'PREINSTALLED_END')
        phase='make-new'
        beat('father','MAKE_OBJECT')
        new=next(x for x in rt.ledger.world('w1')[1]['material_objects'] if x!=old)
        phase='new'
        before=deepcopy(rt.snapshot('nadia'))
        rows=rt.situated('nadia')['attention_frame'].get('cross_object_attention',[])
        require(len(rows)==int(acquired),'ACQUIRED_APPREHENSION')
        require(rt.snapshot('nadia')==before,'READ_MUTATED_PSYCHOLOGY')
        # Finite MII presentation before the sign expires; no new world turn.
        surface=n.private_surface(n.new_private_profile())
        require(rt.snapshot('nadia')==before,'PRIVATE_SURFACE_MUTATED_ACTOR')
        require('cross_object_attention' not in canonical(surface),'ANALYTIC_PRIVATE_LEAK')
        cold()
        beat('nadia','INSPECT' if acquired else 'WAIT')
        ends=rt.snapshot('nadia')['possible_ends']
        require(len(ends)==int(acquired),'NEW_POSSIBLE_END')
        if acquired:
            require(ends[0]['origin_material_object_ref']==new,'WRONG_NEW_OBJECT')
        phase='trial';beat('nadia','INSPECT' if acquired else 'WAIT')
        phase='takeup';beat('nadia','INSPECT' if acquired else 'WAIT')
        material=[p for p in rt.snapshot('nadia')['projects']
                  if p.get('material_object_ref')==new]
        require(len(material)==int(acquired),'NO_ACTUAL_MATERIAL_PROJECT')
        cold()
        phase='material-project'
        for _ in range(3):
            beat('nadia','INSPECT' if acquired else 'WAIT')
        material=[p for p in rt.snapshot('nadia')['projects']
                  if p.get('material_object_ref')==new]
        material_exercises=sum(x.get('operation')=='INSPECT' and
            x.get('performed_status')=='PERFORMED'
            for p in material for x in p.get('operational_history',[]))
        require(material_exercises>=3 if acquired else material_exercises==0,
                'NO_REPEATED_PROJECT_EFFICACY')
        require(n.contribute('look-new','LOOK',target_object_ref=new)['status']=='PERFORMED',
                'ACTUAL_VISITOR_LOOK')
        surface=n.private_surface(n.new_private_profile(),command='look',target=new)
        require('incidental_object_end_basis' not in canonical(surface),'PRIVATE_END_LEAK')
        require(n.contribute('leave','LEAVE')['status']=='PERFORMED','ACTUAL_DEPARTURE')
        visitor_history=deepcopy(rt.ledger.world('w1')[1]['neighbor_user_events'])
        phase='elapsed';rt.background(280)
        cold()
        # Reuse R52 actual joint starting occasion; mother independently selects
        # her own project. Nadia's initial joint act is a stipulated setup.
        phase='vocal-joint'
        rt.step('nadia',requested_action='SING',target='mother')
        old_mother=deepcopy(rt.snapshot('mother')['projects'][0])
        require(old_mother['operational_history'][-1]['performed_status']=='PERFORMED',
                'JOINT_VOCAL_SOURCE')
        phase='vocal-own';beat('nadia','SING')
        phase='vocal-trial';beat('nadia','SING' if acquired else 'WAIT')
        phase='vocal-takeup';beat('nadia','SING')
        vocal=[p for p in rt.snapshot('nadia')['projects'] if 'SING' in p.get('means',[])]
        require(len(vocal)==int(acquired),'VOCAL_PROJECT_GENESIS')
        phase='vocal-project';beat('nadia','SING' if acquired else 'WAIT')
        updated=rt.snapshot('mother')['projects'][0]
        require(updated['id']==old_mother['id'],'REPLACED_OTHER_PROJECT')
        require(updated['object']==old_mother['object'],'REPLACED_OTHER_OBJECT')
        require(updated['means']==(['SING','ORIENT'] if acquired else ['SING']),
                'RECIPROCAL_REFUNCT_FAILURE')
        cold()
        phase='receive';mother_later=beat('mother','ORIENT' if acquired else 'WAIT')['attempt']
        require(rt.ledger.world('w1')[1]['neighbor_user_events']==visitor_history,
                'FABRICATED_ABSENT_VISITOR')
        if routine_admission is not None:
            require(acquired and arm=='E','ROUTINE_REQUIRES_FULL_ACQUIRED_EXACT_ARM')
            # Continue the very SAME child's acquired purpose, not a seeded
            # adult-like project or a newly initialized person.
            for _ in range(2):
                phase='routine-rest';beat('nadia','REST')
                phase='routine-vocal';beat('nadia','SING')
            phase='routine-rest';beat('nadia','REST')
            before=deepcopy(rt.ledger.actor('nadia')[1])
            projects=[p for p in before['projects'] if 'SING' in p.get('means',[])]
            require(len(projects)==1,'ROUTINE_NO_ACTUALLY_ACQUIRED_PROJECT')
            sources=[x for x in rt.ledger.world()[1]['routine_source_registry'].values()
                     if x.get('actor')=='nadia' and x.get('operation')=='SING']
            require(len(sources)==int(routine_admission),'ROUTINE_SOURCE_ADMISSION')
            from um_sorok_organism.mediated_efficacy import situated_component_efficacy
            prior_component=situated_component_efficacy(before,'SING','home')
            # Fixed matched threshold relative to the actual pre-period
            # competence, not knowledge of which arm was selected.
            routine_threshold=prior_component['technical_component_facility_estimate']+.02
            start=rt.ledger.world()[1]['clock'];dep=visitor_history[-1]['event_ref']
            phase='elapsed';cold()
            result=n.continue_absent_life_until(dep,start+40,
                historical_cadence={'cadence_origin':start,'ordinary_span':40,'detail_beats':3})
            require(result['status']=='AT_OR_PAST_ABSENCE_TARGET','ROUTINE_CONTINUATION')
            require(rt.ledger.world()[1]['neighbor_user_events']==visitor_history,
                    'ROUTINE_FABRICATED_ABSENT_USER')
            current=deepcopy(rt.ledger.actor('nadia')[1])
            require(current['power_exercises']==before['power_exercises'],
                    'ROUTINE_INVENTED_INDIVIDUAL_PRACTICE')
            require(current['memories']==before['memories'],'ROUTINE_INVENTED_MEMORIES')
            # R008 extension now conserves actual aggregate afterlife ON the
            # same project/routine. Compare everything except this new receipt
            # carrier; verify it actually exists only in the admitted arm.
            def purpose_only(projects):
                result=deepcopy(projects)
                for project in result:
                    for row in project.get('recurrent_routines',[]):
                        row.pop('modeled_course_receipts',None)
                return result
            require(purpose_only(current['projects'])==purpose_only(before['projects']),
                    'ROUTINE_REPLACED_PURPOSE')
            require(bool([x for p in current['projects'] for row in p.get('recurrent_routines',[])
                          for x in row.get('modeled_course_receipts',[])])==routine_admission,
                    'ROUTINE_MODELED_AFTERLIFE_MISSING')
            later_component=situated_component_efficacy(current,'SING','home')
            require(later_component['technical_component_facility_estimate']>
                    routine_threshold if routine_admission else later_component==prior_component,
                    'ROUTINE_DID_NOT_CHANGE_EXISTING_FACILITY')
            cold()
            require(n.contribute('return-after-routine','MOVE',destination='home')['status']=='PERFORMED',
                    'ROUTINE_RETURN')
            phase='routine-late'
            actual=beat('nadia','SING' if routine_admission else 'WAIT')
            surface=n.private_surface(n.new_private_profile())
            require('recurrent_routines' not in canonical(surface),'ROUTINE_PRIVATE_LEAK')
            routine_result={'project_id':projects[0]['id'],'actual_later_operation':actual['attempt'],
                'facility_before':prior_component['technical_component_facility_estimate'],
                'facility_after':later_component['technical_component_facility_estimate'],
                'aggregate_practice_periods':later_component['qualified_compressed_practice_periods'],
                'individual_exercises_before_period':prior_component['actual_participation_events'],
                'individual_exercises_after_period':later_component['actual_participation_events'],
                'body_age_days':current['age_days'],'source_count':len(sources),
                'threshold_is_controlled_policy_not_science':True}
        require('visitor' not in rt.ledger.actors(),'COUNTERFEIT_VISITOR')
        require(rt.verify()['valid'],'FINAL_CHAIN')
        final={'world':rt.ledger.world('w1')[1],'actors':rt.ledger.actors(),
               'events':rt.ledger.events(),'verification':rt.verify()}
        return {'arm':arm,'state_digest':digest(final),'events':len(final['events']),
                'clock':final['world']['clock'],'actual_independent_course':observed,
                'cultural_practice':int(acquired),'new_material_project':int(bool(material)),
                'actual_material_project_exercises':material_exercises,
                'vocal_project':len(vocal),'mother_means':updated['means'],
                'mother_actual_later_operation':mother_later,
                **({'acquired_routine_course':routine_result} if routine_result is not None else {}),
                'wire_witness_digest':digest(wire.witness),'cost':wire.stats(),
                'sourcefree_not_live_model':True,
                'no_inference_token_or_population_forecast':True}
    finally:
        rt.close()

def run_campaign():
    with tempfile.TemporaryDirectory(prefix='r34_acquired_life_') as tmp:
        return {a:run_course(Path(tmp)/(a+'.sqlite'),a) for a in ARMS}



def run_integrated_life_course(db, *, resume=True, acquire=True):
    """One persistent family from antecedent adults to later visitor return.

    This is a sourcefree executable composition of existing historical and
    constitutive owners, not a scripted player story, native PYAT evidence,
    or an automatic endpoint in adult psychology. Controlled semantic policy
    selects only actual options; every event passes the real ledger/world.
    """
    from um_sorok_organism.types import newborn
    from um_sorok_organism.plural_care_paths import choose_one_grounded_plural_acquisition
    fallback=HeuristicSemanticProvider()
    phase='ancestor'
    constructor_calls=[]
    def seed(aid):
        projects=[{'object':'continue embodied life','means':['REST','EAT'],'priority':.4},
                  {'object':'ordinary speech','means':['SPEAK'],'priority':.6},
                  {'object':'care for Nadia if present','means':['CARE'],
                   'addressed_party_ref':'nadia','priority':.7}]
        if aid=='father':
            projects.append({'object':'care for Mother','means':['CARE'],
                             'addressed_party_ref':'mother','priority':.8})
        return {'input_kind':'THIN_BIOGRAPHY',
                'source_grade':'EXPLICIT_FICTIONAL_HISTORICAL_INPUT',
                'source_ref':'fictional:integrated:'+aid,
                'biographical_context':{'ordinary_life':aid},
                'fictional_seed':{'projects':projects}}
    def policy(task,p):
        aid=p.get('actor',{}).get('id')
        if task=='adult_constructor':
            constructor_calls.append(p['actor_id'])
            return fallback.propose(task,p)
        if task=='family_pathway_selection':
            return {'task':task,'pathway_id':'existing-family'}
        if task=='expression':
            if p.get('expression_phase')=='LEXICAL_REALIZATION_BEFORE_EXPERIENCE':
                return {'task':task,'speech':'We have been living our ordinary lives.'}
            return {'task':task,'surface':'Ordinary activity continues.'}
        if task=='development':
            if aid=='nadia' and acquire:
                return {'task':task,'candidates':choose_one_grounded_plural_acquisition(
                    p.get('historically_possible_plural_care',[]))}
            return {'task':task,'candidates':[]}
        if task=='actor_attempt':
            opts=p.get('practical_options',[])
            actions={x['action'] for x in p.get('options',[])}
            if p.get('requesting_actor') is not None:
                return {'task':task,'action':'REFUSE'}
            def exact(op,target=None):
                return next((x for x in opts if x['operation']==op and
                    x.get('world_request',{}).get('addressed_party_ref')==target),None)
            def choose(row):
                return {'task':task,'practical_option_id':row['option_id']}
            if phase=='ancestor':
                q=exact('CARE','mother') if aid=='father' else None
                return choose(q) if q else {'task':task,'action':'WAIT'}
            if phase=='initial-care':
                if aid=='nadia':return {'task':task,'action':'ORIENT'}
                q=exact('CARE','nadia')
                return choose(q) if q else {'task':task,'action':'REST'}
            if phase=='visitor-speech' and aid=='father':
                q=next((x for x in p.get('addressed_lexical_options',[])
                        if x.get('world_request',{}).get('addressed_party_ref')=='visitor'),None)
                if q:
                    return {**choose(q),'speech_intent':'Acknowledge this actual visitor.'}
            if phase=='child-address' and aid=='nadia':
                rows=[o for o in opts if o.get('grounds_status')=='HISTORICALLY_ACQUIRED_CO_REGULATION']
                if rows:
                    ranked=[]
                    for row in rows:
                        clocks=[x['event_clock'] for x in row.get('personally_sensed_support_history',[])
                                if x.get('bodily_regulation_sensed') is True]
                        if clocks:ranked.append((max(clocks),row))
                    if ranked:return choose(max(ranked,key=lambda x:x[0])[1])
                return {'task':task,'action':'ORIENT'}
            # No authored user choice here. Body conditions and current
            # practical alternatives determine what this controlled policy does.
            body=p['actor']['body']
            if body['rest']<.42 and 'REST' in actions:
                return {'task':task,'action':'REST'}
            if body['nutrition']<.38 and 'EAT' in actions:
                return {'task':task,'action':'EAT'}
            if aid=='nadia' and 'PRACTICE' in actions:
                return {'task':task,'action':'PRACTICE'}
            if aid!='nadia':
                q=exact('CARE','nadia')
                if q and body['rest']>.65:return choose(q)
            return {'task':task,'action':'WAIT'}
        return fallback.propose(task,p)
    wire=CourseWire('E',policy)
    semantic=ValidatingSemanticService(wire)
    rt=ConstitutiveRuntime(str(db),semantic=semantic)
    n=None
    def cold():
        nonlocal rt,n
        rt.close();rt=ConstitutiveRuntime(str(db),semantic=semantic)
        if n is not None:n=NeighborEncounter(rt,'visitor',mii_module=mii)
        require(rt.verify()['valid'],'INTEGRATED_COLD_CHAIN')
    def world():return rt.ledger.world(rt.world_id)[1]
    def actor(aid):return rt.ledger.actor(aid)[1]
    def step(aid,operation=None):
        out=rt.step(aid)
        require(out.get('selection_grade')!='INJECTED_NOT_NATIVE_ACTOR_CHOICE',
                'INTEGRATED_NONINDEPENDENT_CHOICE')
        if operation:require(out['attempt']==operation and out['status']=='PERFORMED',
            'INTEGRATED_EXPECTED_'+operation+':'+str(out.get('attempt'))+':'+str(out.get('status')))
        return out
    try:
        rt.initialize_antecedent_adult('mother','Mother',seed('mother'),
            other_adults=[('father','Father',seed('father'))])
        sid=rt.register_family_pathways('mother',[{
            'id':'existing-family','source_ref':'fictional:family-path',
            'intersection_clock':2,'intersection_site':'home',
            'conception_clock':3,'birth_clock':5,
            'counterpart_id':'father','counterpart_name':'Father','counterpart_packet':None,
            'child_id':'nadia','child_name':'Nadia',
            'prior_shared_effects':'RETAIN_EXISTING_ACTUAL_HISTORY'}])['source_seal_id']
        step('father','CARE');step('mother','WAIT')
        old_actors=deepcopy(rt.ledger.actors());old_events=deepcopy(rt.ledger.events())
        require(rt.select_family_intersection(sid)['actor']=='father','INTEGRATED_FAMILY_SELECTION')
        require(rt.ledger.actors()==old_actors,'INTEGRATED_RECREATED_ADULT')
        require(rt.ledger.events()[:len(old_events)]==old_events,'INTEGRATED_REWROTE_ANCESTOR_HISTORY')
        step('father','CARE');rt.admit_family_conception()
        require('nadia' not in rt.ledger.actors(),'INTEGRATED_PREBORN_PSYCHOLOGY')
        birth=rt.continue_mixed_history(5,ordinary_span=20,detail_beats=3)
        require(birth['status']=='MODELED_HISTORY_CUT_REACHED' and birth['conditional_births']==1,
                'INTEGRATED_EXACT_BIRTH')
        require(actor('nadia')==newborn('nadia','Nadia'),'INTEGRATED_NEWBORN_INHERITED_PURPOSE')
        phase='initial-care'
        step('father','CARE');step('mother','CARE');step('nadia','ORIENT');step('nadia','ORIENT')
        care=deepcopy(actor('nadia')['experienced_care_events'])
        require({q['giver_ref'] for q in care}=={'mother','father'},'INTEGRATED_PLURAL_ACTUAL_CARE')
        before_orientations=deepcopy(actor('nadia')['co_regulation_orientations'])
        require({q['caregiver_ref'] for q in before_orientations}==
                ({'mother','father'} if acquire else set()),'INTEGRATED_PLURAL_ACQUISITION')
        start=world()['clock'];sources=[]
        for aid,begin,end in [('mother',start,start+45),('father',start+10,start+90)]:
            src=rt.register_historical_routine_source({
                'kind':'QUALIFIED_REPRODUCTIVE_CARE','actor':aid,'location':'home',
                'start_clock':begin,'end_clock':end,'max_hours_per_active_day':2,
                'description':'Explicit fictional bounded aggregate care arrangement'})
            sources.append({'kind':'QUALIFIED_REPRODUCTIVE_CARE','actor':aid,'location':'home',
                'source_ref':src['source_ref'],'recipient':'nadia',
                'hours_per_active_day':1.,'provisional_exposure_fraction':.25})
        phase='ordinary'
        cadence={'cadence_origin':0,'ordinary_span':30,'detail_beats':3}
        target=start+320
        history_receipts=[]
        if resume:
            part=rt.continue_mixed_history(target,period_processes=sources,max_segments=3,**cadence)
            require(part['status']=='HELD_AT_MIXED_HISTORY_BOUNDARY','INTEGRATED_EXPECTED_PARTIAL')
            history_receipts.extend(part['segments'])
            cold()
        rest=rt.continue_mixed_history(target,period_processes=sources,**cadence)
        require(rest['status']=='MODELED_HISTORY_CUT_REACHED','INTEGRATED_PREVISIT_CUT')
        history_receipts.extend(rest['segments'])
        require(not world().get('neighbor_user_events'),'INTEGRATED_FABRICATED_VISITOR')
        require(actor('nadia')['experienced_care_events'][:len(care)]==care,'INTEGRATED_LOST_CARE_HISTORY')
        require(actor('nadia')['co_regulation_orientations'][:len(before_orientations)]==before_orientations,
                'INTEGRATED_LOST_ORIENTATION_HISTORY')
        require(actor('nadia')['age_days']>250,'INTEGRATED_AGE_DID_NOT_ADVANCE')
        require(any(x.get('operation')=='PRACTICE' for x in actor('nadia')['power_exercises']),
                'INTEGRATED_NO_ACTUAL_CHILD_EXERCISE')
        registry=world()['routine_source_registry']
        for period in world()['historical_periods']:
            for proc in period['processes']:
                if proc.get('source_ref') in registry:
                    src=registry[proc['source_ref']]
                    require(src['from_clock']<=period['start']<period['end']<=src['through_clock'],
                            'INTEGRATED_ROUTINE_WINDOW_OVERREACH')
        previsit={'clock':world()['clock'],'age':actor('nadia')['age_days'],
                  'care_periods':len(world().get('reproductive_labor_periods',[])),
                  'practice_events':len(actor('nadia')['power_exercises']),
                  'detailed_beats':sum(x['kind']=='INDEPENDENT_DETAIL' for x in history_receipts)}
        require(previsit['detailed_beats']>=12,'INTEGRATED_INSUFFICIENT_POLYCENTRIC_DETAIL')
        cold()
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
               'hearing':True,'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{a:{'facing':'entrance','visual':True,'light':'lit',
                'sightline':'unobstructed','hearing':True,'sound_path':'audible'}
                for a in ('mother','father','nadia')}},request_id='geometry')
        require(n.contribute('enter','MOVE',destination='home')['status']=='PERFORMED','INTEGRATED_ENTRY')
        phase='visitor-speech'
        speech=n.independent_actor_beat('father')
        require(speech['attempt']=='SPEAK' and speech['status']=='PERFORMED','INTEGRATED_VOLUNTARY_SPEECH')
        profile=n.new_private_profile()
        surface=n.private_surface(profile)
        require(any(x.get('spoken_text')=='We have been living our ordinary lives.'
                    and x.get('lexical_acquisition_route')=='VOLUNTARILY_ADDRESSED_TO_SELF'
                    for x in surface['mandatory']),'INTEGRATED_ACTUAL_WORDS_NOT_RENDERED')
        # An actual later care occasion, not an inference from the aggregate period.
        phase='initial-care'
        step('nadia','ORIENT')
        later_care=len(actor('nadia')['experienced_care_events'])
        step('mother','CARE')
        require(len(actor('nadia')['experienced_care_events'])>later_care,'INTEGRATED_LATER_CARE_NOT_SENSED')
        phase='child-address'
        child=n.independent_actor_beat('nadia')
        require(child['attempt']==('SIGNAL' if acquire else 'ORIENT'),'INTEGRATED_ACQUIRED_ADDRESS:'+str(child['attempt'])+':'+str(child['status']))
        if acquire:require(child['status']=='PARTIAL','INTEGRATED_NO_INDEPENDENT_REFUSAL')
        require(n.contribute('depart','LEAVE')['status']=='PERFORMED','INTEGRATED_DEPARTURE')
        absent_history=deepcopy(world()['neighbor_user_events'])
        dep=absent_history[-1]['event_ref'];departure_clock=world()['clock']
        phase='ordinary';cold()
        continued=n.continue_absent_life_until(dep,departure_clock+70,
            historical_cadence=cadence,period_processes=sources)
        require(continued['status']=='AT_OR_PAST_ABSENCE_TARGET' and
                continued['independent_actor_beats']>=3,'INTEGRATED_ABSENT_LIFE')
        require(world()['neighbor_user_events']==absent_history,'INTEGRATED_ABSENT_VISITOR_FABRICATED')
        age_after=actor('nadia')['age_days']
        require(age_after>previsit['age'],'INTEGRATED_ABSENCE_DID_NOT_AGE')
        cold()
        arrival=n.contribute('return','MOVE',destination='home')
        require(arrival['status']=='PERFORMED','INTEGRATED_RETURN')
        frames=n.continue_present_life_until(arrival['event_ref'],world()['clock']+6,profile=profile)
        require(frames['beats_committed_this_call']==6,'INTEGRATED_PRESENT_POLYCENTRIC_LIFE')
        require(len(frames['new_present_surfaces'])==6,'INTEGRATED_PRESENT_ACTUAL_EXPOSURES')
        require('visitor' not in rt.ledger.actors(),'INTEGRATED_FAKE_VISITOR_PSYCHOLOGY')
        require(constructor_calls==['mother','father'],'INTEGRATED_RECONSTRUCTED_PERSON')
        require(rt.verify()['valid'],'INTEGRATED_FINAL_CHAIN')
        final={'world':world(),'actors':rt.ledger.actors(),'events':rt.ledger.events()}
        return {'state_digest':digest(final),'clock':world()['clock'],'events':len(final['events']),
                'previsit':previsit,'age_after_absence':age_after,
                'child_address_operation':child['attempt'],'child_address_status':child['status'],
                'present_beats':frames['beats_committed_this_call'],
                'absence_beats':continued['independent_actor_beats'],
                'constructor_calls':constructor_calls,'cost':wire.stats(),
                'not_live_model_or_native_evidence':True}
    finally:rt.close()

if __name__=='__main__':
    print(canonical(run_campaign()))
