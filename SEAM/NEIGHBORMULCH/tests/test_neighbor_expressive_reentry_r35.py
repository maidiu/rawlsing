"""R35: acquired expressive activity -> independent visitor exposure ->
actual authored address -> actor-selected focal reception -> optional private
afterlife and new trial. No model of the real visitor or private MII input.
"""
import tempfile
from pathlib import Path
from copy import deepcopy
import sys
import unittest

ROOT=Path(__file__).resolve().parents[3]
for path in (ROOT,ROOT/'SEAM'/'ORACLE'/'UM_SOROK_ORGANISM_R3',
             ROOT/'WORKER_RETURNS'/'SOROK-P5-CONTINUOUS-EXPERIENCE-R1',
             ROOT/'WORKER_RETURNS'/'SOROK-P6-ONE-LIVING-HOUSE-R1',
             ROOT/'WORKER_RETURNS'/'SOROK-P4-CORE-LOOP-R1',
             ROOT/'SEAM'/'NEIGHBORMULCH'):
    sys.path.insert(0,str(path))
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world,canonical
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.attention_field import offer_focal_encounters
from um_sorok_organism.constitution import actor_access
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii

WORDS='I heard your voice pause.'
MEMORY='Someone said they heard my voice pause; I do not know what they understood.'
IMAGINED='Could I leave myself a little time to finish speaking?'

class ExpressiveReentryR35(unittest.TestCase):
    def course(self, *, learn=True, visitor_hears=True, recipient_hears=True,
               acknowledge=True, choose=True, nominate=True, forge=False):
        phase='start'; seen={}; final=[]
        def callback(task,p):
            aid=p.get('actor',{}).get('id')
            if task=='actor_attempt':
                if aid!='worker':
                    seen[aid]=deepcopy(p.get('focal_encounter_options',[]))
                    return {'task':task,'action':'WAIT'}
                if phase=='start':
                    return {'task':task,'action':'REST','project_id':'duty'}
                if phase in ('speech','final'):
                    rows=[x for x in p['practical_options']
                          if x.get('project_id')=='duty' and x['operation']=='SPEAK']
                    self.assertEqual(len(rows),1)
                    self.assertTrue(rows[0].get('course_affective_organizations'))
                    return {'task':task,'practical_option_id':rows[0]['option_id']}
                if phase=='receive':
                    opts=[x for x in p.get('focal_encounter_options',[])
                          if x.get('encounter_kind')=='DIRECTED_VISITOR_SPEECH']
                    seen['opts']=deepcopy(opts)
                    if forge:
                        return {'task':task,'action':'ORIENT','focal_encounter_id':'forged'}
                    if opts and choose:
                        return {'task':task,'action':'ORIENT',
                                'focal_encounter_id':opts[0]['attention_id']}
                if phase=='rehearse':
                    opts=[x for x in p.get('private_rehearsal_options',[])
                          if x.get('focal_encounter',{}).get('encounter_kind')==
                             'DIRECTED_VISITOR_SPEECH']
                    seen['rehearsal']=deepcopy(opts)
                    if opts:
                        return {'task':task,'action':'WAIT',
                                'private_rehearsal_id':opts[0]['rehearsal_id'],
                                'private_rehearsal_content':IMAGINED}
                if phase=='trial':
                    opts=[t for t in p.get('possible_end_trials',[]) if t['operation']=='REST']
                    if opts:return {'task':task,'possible_end_trial_id':opts[0]['trial_id']}
                return {'task':task,'action':'WAIT'}
            if task=='expression':
                obs=p['actor_accessible']
                self.assertNotIn('focal_encounter',obs.get('own_practical_selection') or {})
                self.assertNotIn('focal_encounter_receipt',obs)
                self.assertNotIn(IMAGINED,canonical(p))
                self.assertNotIn('private unease',canonical(p))
                return {'task':task,'surface':'Ordinary activity.'}
            if task=='development':
                if aid!='worker':return {'task':task,'candidates':[]}
                if phase=='appraise':
                    row=p['historically_possible_delayed_appraisals'][0]
                    return {'task':task,'candidates':[{'kind':'APPRAISE_EXPECTED_DIFFERENCE',
                        'expectation_ref':row['expectation_ref'],
                        'perceived_cue_ref':row['source_perceived_cue_ref'],
                        'appraisal':'ACTOR_INTERPRETS_DISAPPOINTED'}]}
                if phase=='affect':
                    row=p['historically_possible_activity_affects'][0]
                    return {'task':task,'candidates':[{'kind':'ACQUIRE_ACTIVITY_AFFECT',
                        'basis':row,'affect_name':'private unease',
                        'personal_sense':'quiet conflicts with duty',
                        'course_orientation':'NO_DIRECT_TENDENCY'}]}
                if phase=='speech':
                    rows=p['historically_possible_expressive_practices']
                    if rows and learn:
                        return {'task':task,'candidates':[{'kind':'ACQUIRE_EXPRESSIVE_PRACTICE',
                                    'basis':rows[0]['basis'],'cadence':'HALTING'}]}
                if phase=='final':
                    final.append(deepcopy(p['experience']))
                if phase=='receive':
                    seen['experience']=deepcopy(p['experience'])
                    q=p.get('historically_possible_focal_encounter_memory')
                    if q and nominate:
                        return {'task':task,'candidates':[{'kind':'MEMORY',
                            'focal_encounter_ref':q['focal_encounter_ref'],
                            'content':MEMORY,'cue_terms':['speech']}]}
                if phase=='rehearse':
                    rec=p.get('actual_private_rehearsal_analyst_only')
                    if rec:
                        return {'task':task,'candidates':[{'kind':'NOTICE_PRIVATE_POSSIBLE_END',
                            'rehearsal_ref':rec['id'],'possible_object':'make time before speaking again',
                            'possible_means':['REST']}]}
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        semantic=ValidatingSemanticService(CallbackLLMProvider(callback))
        with tempfile.TemporaryDirectory(prefix='r35_expression_') as d:
            db=str(Path(d)/'life.sqlite')
            rt=ConstitutiveRuntime(db,semantic=semantic)
            try:
                worker=adult('worker','Mara')
                worker['projects']=[{'id':'duty','object':'sustain availability',
                    'means':['REST','SPEAK'],'status':'active','priority':.5,
                    'expected_difference':{'feature':'availability','direction':'PRESERVE',
                        'sign_tags':['wait']}}]
                rt.ledger.initialize(blank_world(),[worker,adult('hearer','Hearer'),
                    adult('blocked','Blocked')])
                # Existing R47 expressive formation, through real activity.
                rt.step('worker')
                phase='appraise';rt.step('worker')
                phase='affect';rt.step('worker')
                for _ in range(2):
                    phase='quiet';rt.step('worker')
                    phase='speech';self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    self.assertNotIn('vocal_cadence',rt.ledger.world()[1]['cues'][-1])
                n=NeighborEncounter(rt,'visitor',mii_module=mii)
                n.install_sourcefree_conditions({
                    'grade':'SOURCEFREE_TEST_ONLY',
                    'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
                        'hearing':visitor_hears,'sound_path':'audible' if visitor_hears else 'blocked',
                        'legibility':'readable'}},
                    'actor_conditions':{aid:{'facing':'entrance','visual':True,
                        'light':'lit','sightline':'unobstructed','hearing':hears,
                        'sound_path':'audible' if hears else 'blocked'}
                        for aid,hears in [('worker',recipient_hears),('hearer',True),('blocked',False)]}},
                    request_id='geometry')
                n.contribute('arrive','MOVE',destination='home')
                phase='quiet';rt.step('worker')
                phase='final';utterance=n.independent_actor_beat('worker')
                self.assertEqual(utterance['status'],'PERFORMED')
                cue=deepcopy(rt.ledger.world()[1]['cues'][-1])
                self.assertEqual(cue.get('vocal_cadence'),'HALTING' if learn else None)
                own=rt.snapshot('worker')['evidence_paths'][-1]['own_vocal_reception']
                self.assertEqual(own['cadence_as_sensed'],'HALTING' if learn else 'NOT_DIFFERENTIATED')
                before=deepcopy(rt.ledger.actors())
                world=deepcopy(rt.ledger.world())
                profile=n.new_private_profile()
                view=n.private_surface(profile)
                self.assertEqual(rt.ledger.actors(),before)
                self.assertEqual(rt.ledger.world(),world)
                signs=[s for s in view['mandatory'] if s['kind']=='CO_PUBLIC_OCCURRENCE'
                       and s.get('modality')=='auditory']
                self.assertEqual(len(signs),int(visitor_hears))
                if signs:
                    self.assertEqual(signs[0]['source_cue_ref'],cue['id'])
                    self.assertEqual(signs[0]['source_event_ref'],utterance['receipt'])
                    self.assertEqual(signs[0]['text'],'Speech with brief pauses.' if learn
                                     else 'Speech sounds nearby.')
                    self.assertEqual(signs[0]['speaker_identity'],'NOT_ESTABLISHED')
                self.assertNotIn('private unease',canonical(view))
                self.assertEqual(rt.snapshot('worker')['memories'],[])
                path=Path(d)/'mii.json'
                n.save_private_profile(path,profile)
                rt.close()
                rt=ConstitutiveRuntime(db,semantic=semantic)
                n=NeighborEncounter(rt,'visitor',mii_module=mii)
                self.assertEqual(n.load_private_profile(path),profile)
                before=deepcopy(rt.ledger.actors())
                if acknowledge:
                    speech=n.contribute('ack','SAY',text=WORDS,target_actor_ref='worker')
                    self.assertEqual(speech['status'],'PERFORMED')
                    self.assertEqual(rt.ledger.actors(),before)
                    self.assertTrue(n.contribute('ack','SAY',text=WORDS,
                                                 target_actor_ref='worker')['idempotent_replay'])
                    with self.assertRaisesRegex(EncounterRefusal,'REQUEST_REPLAY_CHANGED_PAYLOAD'):
                        n.contribute('ack','SAY',text=WORDS,target_actor_ref='hearer')
                    self.assertEqual(rt.ledger.latest_event(),rt.ledger.events()[-1])
                    event=rt.ledger.world()[1]['neighbor_user_events'][-1]
                    self.assertEqual(event['target_actor_ref'],'worker')
                    # No candidate can be minted by changing a world row or
                    # a claimed receipt independently of the committed act.
                    a0=rt.ledger.actor('worker')[1];w0=rt.ledger.world()[1]
                    acc=actor_access(a0,w0);refs=[x['id'] for x in acc.cues]
                    real=rt.ledger.latest_event()
                    forged=deepcopy(real)
                    forged['envelope']['payload']['payload_hash']='forged'
                    self.assertEqual(offer_focal_encounters(a0,acc,refs,
                        world=w0,ledger_event=forged),[])
                    bad_world=deepcopy(w0)
                    bad_world['neighbor_user_events'][-1]['authored_text']='different words'
                    self.assertEqual(offer_focal_encounters(a0,acc,refs,
                        world=bad_world,ledger_event=real),[])
                    self.assertNotIn('exposure_id',canonical(event))
                    # Overhearer can hear the words, cannot acquire the
                    # recipient's exact addressed focal source.
                    phase='receive'
                    rt.plan('hearer')
                    self.assertEqual(seen['hearer'],[])
                    self.assertFalse(any(x.get('visitor_speech_addressed_to_recipient')
                        for x in actor_access(rt.ledger.actor('hearer')[1],rt.ledger.world()[1]).cues))
                else:
                    n.contribute('silence','WAIT')
                    speech=None
                phase='receive'
                eligible=acknowledge and recipient_hears
                if forge:
                    w=deepcopy(rt.ledger.world());a=deepcopy(rt.ledger.actors())
                    count=len(rt.ledger.events())
                    with self.assertRaisesRegex(ValueError,'FOCAL_ENCOUNTER_UNISSUED'):
                        n.independent_actor_beat('worker')
                    self.assertEqual(rt.ledger.world(),w)
                    self.assertEqual(rt.ledger.actors(),a)
                    self.assertEqual(len(rt.ledger.events()),count)
                    self.assertTrue(rt.verify()['valid'])
                    return
                result=n.independent_actor_beat('worker')
                self.assertEqual(len(seen['opts']),int(eligible))
                selected=eligible and choose
                self.assertEqual(result['attempt'],'ORIENT' if selected else 'WAIT')
                pathrow=rt.snapshot('worker')['evidence_paths'][-1]
                self.assertEqual(bool(pathrow.get('focal_encounter')),selected)
                if selected:
                    source=pathrow['focal_encounter']
                    self.assertEqual(source['source_user_event_ref'],speech['event_ref'])
                    self.assertEqual(source['source_ledger_ref'],speech['receipt'])
                    self.assertIn(source['cue_ref'],pathrow['received_cue_refs'])
                    self.assertEqual(source['encounter_kind'],'DIRECTED_VISITOR_SPEECH')
                    self.assertIn(WORDS,canonical(seen['experience']['perceived_cues']))
                    self.assertNotIn('exposure_id',canonical(seen['experience']))
                    self.assertNotIn('private_profile',canonical(seen['experience']))
                self.assertEqual(rt.snapshot('worker')['historical_orientations'],[])
                formed=selected and nominate
                self.assertEqual(len(rt.snapshot('worker')['memories']),int(formed))
                # Actual private afterlife survives cold reopening and does
                # not require a new authored human utterance or visitor presence.
                n.contribute('depart','LEAVE')
                human=deepcopy(rt.ledger.world()[1]['neighbor_user_events'])
                rt.close()
                rt=ConstitutiveRuntime(db,semantic=semantic)
                n=NeighborEncounter(rt,'visitor',mii_module=mii)
                phase='rehearse';n.independent_actor_beat('worker')
                self.assertEqual(len(seen['rehearsal']),int(formed))
                a=rt.snapshot('worker')
                self.assertEqual(len(a['possible_ends']),int(formed))
                if formed:
                    self.assertEqual(a['memories'][0]['private_rehearsals'][0]['focal_encounter'],source)
                    self.assertEqual(a['possible_ends'][0]['private_focal_encounter'],source)
                    phase='trial';self.assertEqual(n.independent_actor_beat('worker')['attempt'],'REST')
                    self.assertEqual(len(rt.snapshot('worker')['possible_ends'][0]['trial_history']),1)
                self.assertEqual(rt.ledger.world()[1]['neighbor_user_events'],human)
                self.assertNotIn('visitor',rt.ledger.actors())
                self.assertTrue(rt.verify()['valid'])
                return {'cadence':cue.get('vocal_cadence'),'heard':bool(signs),
                        'selected':selected,'formed':formed,'trial':formed}
            finally:rt.close()

    def test_positive_acquired_cadence_actual_acknowledgement_and_private_afterlife(self):
        self.assertEqual(self.course(),{'cadence':'HALTING','heard':True,
                                        'selected':True,'formed':True,'trial':True})

    def test_same_emission_different_visitor_access_does_not_decide_claim_truth(self):
        observed=self.course(visitor_hears=True)
        unobserved=self.course(visitor_hears=False)
        self.assertEqual(observed['cadence'],unobserved['cadence'])
        self.assertNotEqual(observed['heard'],unobserved['heard'])
        self.assertEqual(observed['formed'],unobserved['formed'])
        ordinary=self.course(learn=False)
        self.assertIsNone(ordinary['cadence'])
        self.assertTrue(ordinary['formed']) # statement, not truth of a pause

    def test_distinct_nulls_exposure_without_speech_blocked_unselected_and_no_formation(self):
        for arm in ({'acknowledge':False},{'recipient_hears':False},
                    {'choose':False},{'nominate':False}):
            with self.subTest(arm=arm):self.assertFalse(self.course(**arm)['formed'])

    def test_forged_focal_option_does_not_commit(self):
        self.course(forge=True)

if __name__=='__main__':unittest.main()
