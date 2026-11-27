"""R38: specific mutually undertaken meeting vs a real finite work opportunity."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.material_conjunction import admit_authored_structural_history
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii


class MeetingTimeR38(unittest.TestCase):
    def build(self,mode,hearing=True):
        tmp=tempfile.TemporaryDirectory(prefix='meeting_r38_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        state={'phase':'accept','packets':[]}
        def cb(task,p):
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            state['packets'].append(deepcopy(p))
            action={'accept':'ACCEPT_MEETING','meet':'MEET_VISITOR','work':'WORK',
                    'latework':'WORK','wait':'WAIT'}[state['phase']]
            if action in ('ACCEPT_MEETING','MEET_VISITOR'):
                opts=[x for x in p['practical_options'] if x['operation']==action]
                if not opts:return {'task':task,'action':'WAIT'}
                self.assertEqual(len(opts),1)
                if mode=='forge':return {'task':task,'practical_option_id':'forged'}
                if mode=='decline':return {'task':task,'action':'WAIT'}
                return {'task':task,'practical_option_id':opts[0]['option_id']}
            if action=='WORK':return {'task':task,'action':'WORK','project_id':'work'}
            return {'task':task,'action':'WAIT'}
        sem=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(db,semantic=sem)
        self.addCleanup(rt.close)
        w=blank_world()
        due=10
        w['ambient']['work_shifts']={'worker':[{'start':due-2,'end':due-1,
                                               'source_ref':'fictional:short_shift'}]}
        w['ambient']['work_shift_coverage_complete']=True
        worker=adult('worker','Worker','workshop')
        worker['projects']=[{'id':'work','object':'earn wage','means':['WORK'],
                             'priority':.8,'status':'active'}]
        spec={'grade':'EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY','source_ref':'fictional:shift',
              'positions':[], 'rules':[{'id':'short_shift','operation':'WORK',
                 'location':'workshop','source_ref':'fictional:shift_gate',
                 'effective_from':0,'effective_until':None,
                 'all_of':[{'kind':'SHIFT_OCCUPIED'}]}]}
        admit_authored_structural_history(w,{'worker'},spec)
        rt.ledger.initialize(w,[worker],
            source_seals=[('authored_structural_history','FICTIONAL_WORLD_CONDITIONING',spec)])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'workshop':{'light':'lit','sightline':'unobstructed',
                   'hearing':True,'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{'worker':{'facing':'entrance','visual':True,
                    'light':'lit','sightline':'unobstructed','hearing':hearing,
                    'sound_path':'audible' if hearing else 'blocked'}}},
            request_id='geometry')
        n.contribute('arrive','MOVE',destination='workshop')
        self.assertEqual(rt.ledger.world()[1]['clock'],2)
        prior=deepcopy(rt.ledger.actors())
        proposal=n.contribute('propose','PROPOSE_MEETING',target_actor_ref='worker',due_clock=due)
        self.assertEqual(rt.ledger.actors(),prior)
        self.assertEqual(proposal['actor_uptake'],'NOT_ESTABLISHED')
        return rt,n,db,state,sem,proposal['meeting_ref'],due

    def row(self,rt,ref):
        return next(x for x in rt.ledger.world()[1]['scheduled_obligations'] if x['id']==ref)

    def test_real_work_and_meeting_compete_at_same_historical_boundary(self):
        for choice in ('meet','work'):
            with self.subTest(choice=choice):
                rt,n,db,state,sem,ref,due=self.build(choice)
                self.assertEqual(self.row(rt,ref)['status'],'PROPOSED')
                self.assertEqual(n.own_meetings()[0]['status'],'PROPOSED')
                self.assertEqual(NeighborEncounter(rt,'outsider',mii_module=mii).own_meetings(),[])
                a=n.independent_actor_beat('worker')
                self.assertEqual((a['attempt'],a['status']),('ACCEPT_MEETING','PERFORMED'))
                self.assertEqual(self.row(rt,ref)['status'],'ACCEPTED')
                self.assertEqual(n.own_meetings()[0]['status'],'ACCEPTED')
                dep=n.contribute('depart','LEAVE')['event_ref']
                state['phase']='wait'
                n.continue_absent_life_until(dep,due-4)
                self.assertEqual(rt.ledger.world()[1]['clock'],due-4)
                n.contribute('return','MOVE',destination='workshop')
                n.contribute('checkin','CHECK_IN_MEETING',target_commitment_ref=ref)
                self.assertEqual(self.row(rt,ref)['status'],'CHECKED_IN')
                self.assertEqual(rt.ledger.world()[1]['clock'],due-2)
                self.assertTrue(n.contribute('checkin','CHECK_IN_MEETING',
                    target_commitment_ref=ref)['idempotent_replay'])
                state['phase']=choice
                a=n.independent_actor_beat('worker')
                self.assertEqual(a['attempt'],'MEET_VISITOR' if choice=='meet' else 'WORK')
                self.assertEqual(a['status'],'PERFORMED')
                w=rt.ledger.world()[1];row=deepcopy(self.row(rt,ref))
                self.assertEqual(row['status'],'MEETING_PERFORMED' if choice=='meet'
                                 else 'ELAPSED_WITHOUT_ACTUAL_MEETING')
                self.assertEqual(w['clock'],due-1)
                self.assertEqual(w['accounts'].get('worker',0),0 if choice=='meet' else .25)
                history=deepcopy(w['public_history'])
                rt.close()
                cold=ConstitutiveRuntime(db,semantic=sem)
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                state['phase']='latework'
                late=nn.independent_actor_beat('worker')
                self.assertEqual(late['status'],'BLOCKED')
                self.assertEqual(cold.ledger.world()[1]['public_history'][:len(history)],history)
                before=deepcopy(cold.ledger.world())
                with self.assertRaisesRegex(EncounterRefusal,'MEETING_CHECKIN_NOT_AUTHORIZED_AT_THIS_CLOCK'):
                    nn.contribute('retroactive-checkin','CHECK_IN_MEETING',target_commitment_ref=ref)
                self.assertEqual(cold.ledger.world(),before)
                self.assertEqual(self.row(cold,ref),row)
                read=nn.own_meetings()[0]
                self.assertEqual(read['status'],row['status'])
                self.assertNotIn('WORK',str(read))
                self.assertNotIn('visitor',cold.ledger.actors())
                self.assertTrue(cold.verify()['valid'])

    def test_no_assent_or_checkin_no_fictitious_waiting(self):
        for mode,hearing in [('decline',True),('inaudible',False),('absent',True)]:
            rt,n,db,state,sem,ref,due=self.build(mode,hearing)
            n.independent_actor_beat('worker')
            self.assertEqual(self.row(rt,ref)['status'],'ACCEPTED' if mode=='absent' else 'PROPOSED')
            dep=n.contribute('depart','LEAVE')['event_ref']
            state['phase']='wait'
            n.continue_absent_life_until(dep,due+1)
            row=self.row(rt,ref)
            self.assertEqual(row['status'],'ELAPSED_WITHOUT_ACTUAL_CHECK_IN'
                            if mode=='absent' else 'ELAPSED_WITHOUT_ACTOR_ASSENT')
            self.assertEqual(row['waiting_breach_or_actor_appraisal'],'NOT_ESTABLISHED')
            self.assertEqual(n.own_meetings()[0]['status'],row['status'])
            self.assertFalse(any(e['operation']=='CHECK_IN_MEETING'
                         for e in rt.ledger.world()[1]['neighbor_user_events']))
            self.assertTrue(rt.verify()['valid'])

    def test_forged_choice_and_early_checkin_do_not_mutate(self):
        rt,n,db,state,sem,ref,due=self.build('forge')
        before=deepcopy(rt.ledger.world()); actors=deepcopy(rt.ledger.actors())
        with self.assertRaisesRegex(ValueError,'UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID'):
            n.independent_actor_beat('worker')
        self.assertEqual(rt.ledger.world(),before)
        self.assertEqual(rt.ledger.actors(),actors)
        with self.assertRaisesRegex(EncounterRefusal,'MEETING_CHECKIN_NOT_AUTHORIZED_AT_THIS_CLOCK'):
            n.contribute('early','CHECK_IN_MEETING',target_commitment_ref=ref)
        self.assertEqual(rt.ledger.world(),before)
        self.assertTrue(rt.verify()['valid'])


if __name__=='__main__':unittest.main()
