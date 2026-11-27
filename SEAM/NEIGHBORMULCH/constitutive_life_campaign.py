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
            'means':['SPEAK'],'priority':.2,'cue_terms':['home']}]}}
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

def run_course(db, arm):
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
            if phase=='vocal-project':
                return choose(lambda x:x.get('operation')=='SING' and x.get('project_id'))
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
        phase='receive';beat('mother','ORIENT' if acquired else 'WAIT')
        require(rt.ledger.world('w1')[1]['neighbor_user_events']==visitor_history,
                'FABRICATED_ABSENT_VISITOR')
        require('visitor' not in rt.ledger.actors(),'COUNTERFEIT_VISITOR')
        require(rt.verify()['valid'],'FINAL_CHAIN')
        final={'world':rt.ledger.world('w1')[1],'actors':rt.ledger.actors(),
               'events':rt.ledger.events(),'verification':rt.verify()}
        return {'arm':arm,'state_digest':digest(final),'events':len(final['events']),
                'clock':final['world']['clock'],'actual_independent_course':observed,
                'cultural_practice':int(acquired),'new_material_project':int(bool(material)),
                'actual_material_project_exercises':material_exercises,
                'vocal_project':len(vocal),'mother_means':updated['means'],
                'mother_actual_later_operation':observed[-1][1],
                'wire_witness_digest':digest(wire.witness),'cost':wire.stats(),
                'sourcefree_not_live_model':True,
                'no_inference_token_or_population_forecast':True}
    finally:
        rt.close()

def run_campaign():
    with tempfile.TemporaryDirectory(prefix='r34_acquired_life_') as tmp:
        return {a:run_course(Path(tmp)/(a+'.sqlite'),a) for a in ARMS}

if __name__=='__main__':
    print(canonical(run_campaign()))
