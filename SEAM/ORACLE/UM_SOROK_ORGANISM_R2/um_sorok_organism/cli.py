"""python -m um_sorok_organism.cli demo --db path | inspect --db path --actor nadia"""
import argparse,json,os
from .runtime import ConstitutiveRuntime
from .types import stable_id


def demo(path):
    if os.path.exists(path):os.remove(path)
    r=ConstitutiveRuntime(path)
    seed=[('mara','Mara',{'source_ref':'synthetic_pseudo_respondent_A','source_grade':'REPRESENTATIVE_TEST_FIXTURE',
           'answers':{'institutional_trust':'mixed','religious_practice':'often',
                      'religious_self_description':'not religious','household_care':'significant'},
           'fictional_seed':{'acquired_forms':[
              {'kind':'PRACTICE','content':'sustain shared singing with household members',
               'cues':['sing','rhythm'],'enables':['SING'],'object':'shared household rhythm'},
              {'kind':'TENSION','content':'affection coexists with constrained daily time',
               'cues':['care','work'],'enables':[],'object':'labor and care conflict'}],
           'projects':[{'object':'keep shared rhythmic activity alive','means':['SING','CARE'],
               'priority':.88,'cue_terms':['sing','home']}]}}),
          ('sam','Sam',{'source_ref':'synthetic_pseudo_respondent_B','source_grade':'REPRESENTATIVE_TEST_FIXTURE',
           'answers':{'institutional_trust':'high','religious_practice':'sometimes',
                      'household_care':'shared'},
           'fictional_seed':{'acquired_forms':[
              {'kind':'PRACTICE','content':'respond to invitations to join familiar activity',
               'cues':['join','sing'],'enables':['JOIN'],'object':'shared rhythm'}],
           'projects':[{'object':'participate in household music when available',
               'means':['JOIN'],'priority':.91,'cue_terms':['home','sing']}]}})]
    report={'initialization':r.initialize(seed)}
    # World-noticeable episodes with distinct participants and consequences.
    report['initial_constitution']={'child_forms':len(r.snapshot('nadia')['forms']),
        'mother_forms':len(r.snapshot('mara')['forms']),
        'father_forms':len(r.snapshot('sam')['forms'])}
    report['infant_signal']=r.step('nadia',requested_action='SIGNAL')
    report['actual_care']=r.step('mara',requested_action='CARE',target='nadia')
    report['ordinary_months']=r.background(240,[{'kind':'care','coverage':'AGGREGATE_MODELED',
        'summary':'modeled recurring care with no invented private conversations'},
        {'kind':'work_conditions','coverage':'AGGREGATE_MODELED','summary':'household and work time remain constrained'}])
    report['independent_joint_activity']=r.step('mara',requested_action='SING',target='sam')
    report['relation_field_after_one']=r.snapshot('sam')['relations']
    report['independent_joint_activity_repeated']=r.step('mara',requested_action='SING',target='sam')
    report['relation_field_after_two']=r.snapshot('sam')['relations']
    report['unacquired_child_actions']=r.situated('nadia')['candidate_actions']
    report['child_practice']=r.step('nadia',requested_action='PRACTICE')
    report['child_singing']=r.step('nadia',requested_action='SING')
    report['child_generated_next_attempt']=r.step('nadia')
    report['child_iceberg']={'forms':len(r.snapshot('nadia')['forms']),
       'traces':len(r.snapshot('nadia')['traces'])}
    report['child_situated']=r.situated('nadia')
    report['mother_interview']=r.interview('mara',['institutional_trust','religious_practice',
                            'religious_self_description','household_care'])
    report['sourcefree_chain']=r.verify()
    r.close()
    # Cold reopen: actors and historical changes must persist.
    r=ConstitutiveRuntime(path)
    report['cold_reopen']={'child_forms':len(r.snapshot('nadia')['forms']),
        'world_clock':r.snapshot('nadia')['clock'],
        'chain':r.verify()}
    r.close()
    return report


def main():
    ap=argparse.ArgumentParser(description='UM-SOROK provisional whole organism')
    sp=ap.add_subparsers(dest='command',required=True)
    de=sp.add_parser('demo');de.add_argument('--db',default='organism_demo.sqlite3')
    for name in ['inspect','situated','see','chain']:
        x=sp.add_parser(name);x.add_argument('--db',required=True);x.add_argument('--actor',default='nadia')
    args=ap.parse_args()
    if args.command=='demo':res=demo(args.db)
    else:
        runtime=ConstitutiveRuntime(args.db)
        res={'inspect':lambda:runtime.snapshot(args.actor),
             'situated':lambda:runtime.situated(args.actor),
             'see':lambda:runtime.see(args.actor),'chain':runtime.verify}[args.command]()
        runtime.close()
    print(json.dumps(res,indent=2,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
