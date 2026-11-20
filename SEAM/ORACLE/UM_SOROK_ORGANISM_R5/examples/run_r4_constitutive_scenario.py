"""Joined TCO R4 sourcefree executable: Nadia + caregiver + practical adult.

No one is a whole scientific person; this is an integrated witness to
nonverbal co-regulation, real material failure, different histories, and a
historically produced second-order practice in ONE world and ledger.
"""
import json,tempfile
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (CallbackLLMProvider,ValidatingSemanticService,
                                         HeuristicSemanticProvider)

worker={'source_ref':'DEMO_FICTIONAL_WORKER_NOT_SURVEY_DATA','answers':{'livelihood':'uncertain'},
 'fictional_seed':{'projects':[{'object':'repair workshop for daily collective use',
    'means':['REPAIR','WORK'],'priority':.94,'cue_terms':['repair','stock']}]}}
caregiver={'source_ref':'DEMO_FICTIONAL_CAREGIVER_NOT_SURVEY_DATA','answers':{'care':'variable'},
 'fictional_seed':{'projects':[{'object':'respond to infant signaling','means':['CARE'],
    'priority':.98,'cue_terms':['signal','care']}]}}

def run(path):
    work_sequence=iter(['REPAIR','WORK','REPAIR']*2)
    fallback=HeuristicSemanticProvider()
    def policy(task,packet):
        if task=='actor_attempt':
            actor=packet['actor']['id']
            if actor=='nadia':return {'action':'SIGNAL'}
            if actor=='worker':
                projs=[c for c in packet['situated']['currents']
                       if c['kind']=='ONGOING_ACTIVITY' and 'repair workshop' in c['object']]
                assert len(projs)==1
                return {'action':next(work_sequence),'project_ids':[projs[0]['ref']]}
        return fallback.propose(task,packet)
    rt=ConstitutiveRuntime(str(path),ValidatingSemanticService(CallbackLLMProvider(policy)))
    try:
        rt.initialize([('worker','Worker',worker),('caregiver','Caregiver',caregiver)])
        child_events=[rt.step('nadia',target='caregiver') for _ in range(2)]
        after_child=rt.ledger.actor('nadia')[1]
        child_orientations=list(after_child['nonconceptual_orientations'].values())
        rt.step('worker',requested_action='MOVE',object_ref='workshop')
        work_events=[]
        for _ in range(2):
            for __ in range(3):rt.step('worker',requested_action='REST')
            v,w=rt.ledger.world();w['sites']['workshop']['stock']=0
            rt.ledger.commit(rt.world_id,v,w,{}, {},'EXPLICIT_WORLD_RESEARCH_FIXTURE',None,
                             {'stock':0,'not_actor_memory':True})
            work_events.extend(rt.step('worker') for __ in range(3))
        adult=rt.ledger.actor('worker')[1]
        methods=list(adult['historical_composition_methods'].values())
        for __ in range(3):rt.step('worker',requested_action='REST')
        v,w=rt.ledger.world();w['sites']['workshop']['stock']=0
        rt.ledger.commit(rt.world_id,v,w,{}, {},'EXPLICIT_WORLD_RESEARCH_FIXTURE',None,
                         {'stock':0,'not_actor_memory':True})
        continuation=rt.continue_life('worker')
        chain=rt.verify()
        return {'schema':'TCO_R4_CONNECTED_CONSTITUTIVE_WITNESS@1',
          'world_id':rt.world_id,'sourcefree':True,'actor_ids':sorted(rt.ledger.actors()),
          'child_care_events':[e['objective_outcome'] for e in child_events],
          'child_language':after_child['body']['language'],
          'child_nonconceptual_orientations':child_orientations,
          'worker_historical_actions':[e['attempt']+':'+e['status'] for e in work_events],
          'worker_material_differences':list(adult['acquired_discriminations'].values()),
          'worker_history_generated_methods':methods,
          'actor_self_continuation':{'method':continuation.get('method'),
             'attempts':[a['attempt']+':'+a['status'] for a in continuation['attempts']]},
          'chain':chain,'limitations':['no_live_model','no_native_P2_P3_P6',
           'no_blind_survey_parent_fidelity','no_scientific_human_law',
           'research_world_fixtures_explicit','no_independent_receiving']}
    finally:rt.close()

if __name__=='__main__':
    import sys
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(tempfile.mkdtemp())/'r4.sqlite3'
    print(json.dumps(run(root),indent=2,sort_keys=True,ensure_ascii=False))
