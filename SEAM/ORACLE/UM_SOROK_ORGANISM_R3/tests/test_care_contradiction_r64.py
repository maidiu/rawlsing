"""R64: actual care and subsequent received imposition can remain contradictory."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment

class CareContradiction(unittest.TestCase):
    def arm(self,db,nominate,forge=False):
        phase={'stage':'care'};offers=[]
        def cb(task,p):
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            if task=='development':
                if p['actor']['id']=='giver':
                    rows=p.get('historically_possible_care_practices',[])
                    if rows and phase['stage']=='care':return {'task':task,'candidates':rows}
                    rows=p.get('historically_possible_care_practice_revisions',[])
                    if rows:
                        offers.extend(deepcopy(rows))
                        if nominate:
                            c=deepcopy(rows[0])
                            c['interpretive_hypothesis']='I need not keep doing this for this person.'
                            if forge:c['basis']['imposition_event_ref']='invented'
                            return {'task':task,'candidates':[c]}
                return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if p.get('requesting_actor') is not None:return {'task':task,'action':'REFUSE'}
                if p['actor']['id']=='giver':
                    rows=[o for o in p['practical_options'] if o['operation']=='CARE'
                          and o.get('world_request',{}).get('addressed_party_ref')=='other']
                    if phase['stage']=='later':
                        rows=[o for o in rows if o['grounds_status']=='HISTORICALLY_PRACTICED_PARTICULAR_CARE']
                    if rows:return {'task':task,'practical_option_id':rows[0]['option_id']}
                return {'task':task,'action':'WAIT'}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            giver=adult('giver','Giver')
            giver['projects']=[{'id':'care','object':'care for other','means':['CARE'],
                  'addressed_party_ref':'other','status':'active','priority':.6}]
            rt.ledger.initialize(blank_world(),[giver,adult('other','Other'),adult('third','Third')])
            for _ in range(2):
                self.assertEqual(rt.step('giver')['status'],'PERFORMED')
                rt.step('giver',requested_action='REST')
            old=deepcopy(rt.ledger.actor('giver')[1])
            self.assertEqual(len(old['care_practical_commitments']),1)
            phase['stage']='contradiction'
            self.assertEqual(rt.step('third',requested_action='IMPOSE',target='giver')['status'],'PERFORMED')
            self.assertEqual(offers,[])
            before=deepcopy(rt.ledger.actor('giver')[1]);world=deepcopy(rt.ledger.world())
            if forge:
                with self.assertRaisesRegex(InvalidDevelopment,'CARE_PRACTICE_REVISION_UNQUALIFIED'):
                    rt.step('other',requested_action='IMPOSE',target='giver')
                self.assertEqual(rt.ledger.actor('giver')[1],before)
                self.assertEqual(rt.ledger.world(),world)
                self.assertTrue(rt.verify()['valid'])
                return
            self.assertEqual(rt.step('other',requested_action='IMPOSE',target='giver')['status'],'PERFORMED')
            self.assertEqual(len(offers),1)
            after=rt.ledger.actor('giver')[1]
            row=after['care_practical_commitments'][0]
            self.assertEqual({k:v for k,v in row.items() if k!='revisions'},old['care_practical_commitments'][0])
            self.assertEqual(len(row.get('revisions',[])),int(nominate))
            self.assertEqual(after['care_contribution_episodes'],old['care_contribution_episodes'])
            self.assertEqual(after['projects'],old['projects'])
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            phase['stage']='later'
            view=cold.situated('giver')
            rows=[o for o in view['candidate_actions'] if o['action']=='CARE']
            self.assertEqual(len(rows),1)
            # Generic/project care remains possible, even with a suspended practice.
            self.assertTrue(any(x.get('project_id')=='care' for x in rows[0]['practical_alternatives']))
            self.assertEqual(any(x.get('grounds_status')=='HISTORICALLY_PRACTICED_PARTICULAR_CARE'
                                 for x in rows[0]['practical_alternatives']),not nominate)
            result=cold.step('giver')
            self.assertEqual(result['attempt'],'WAIT' if nominate else 'CARE')
            self.assertEqual(result['status'],'PERFORMED')
            self.assertTrue(cold.verify()['valid'])
        finally:cold.close()

    def test_same_actual_imposition_optional_revision_of_particular_care(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'unchanged',False)
            self.arm(Path(d)/'revised',True)

    def test_forged_imposition_rejects_current_event(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'forged',True,True)
