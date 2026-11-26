"""R53: actual counterhistory can release, not merely oppose, a current."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.types import adult
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.historical_self_organization import (
    possible_lived_directional_orientation, possible_counterhistory_release)
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider)
import test_historical_self_precue_r19 as inherited
from test_historical_self_precue_r19 import option

class CounterhistoryRelease(unittest.TestCase):
    def test_repeated_adverse_then_counterhistory_optional_and_reversible(self):
        a = adult('a','A')
        course = inherited.HistoricalSelfAndPrecueR19._r29_lived_in_other_presence
        course(a,'a1',1,'father','WITHHOLD')
        e = course(a,'a2',2,'father','WITHHOLD')
        ref = admit(a,e,'world:a2',possible_lived_directional_orientation(
            a,e,'world:a2'))[0]['ref']
        original = deepcopy(a['historical_orientations'][0])
        e = course(a,'b1',3,'father','APPROACH')
        self.assertEqual(possible_counterhistory_release(a,e,'world:b1'),[])
        e = course(a,'b2',4,'father','APPROACH')
        offered = possible_counterhistory_release(a,e,'world:b2')
        self.assertEqual(len(offered),1)
        self.assertIsNone(option(inherited.HistoricalSelfAndPrecueR19._r29_situated_beside(a,'father')))
        before = deepcopy(a)
        forged = deepcopy(offered)
        forged[0]['counterhistory_release_basis']['source_event_refs'][0]='world:a1'
        with self.assertRaises(InvalidDevelopment):
            admit(a,e,'world:b2',forged)
        self.assertEqual(a,before)
        admit(a,e,'world:b2',offered)
        self.assertIsNotNone(option(inherited.HistoricalSelfAndPrecueR19._r29_situated_beside(a,'father')))
        row=a['historical_orientations'][0]
        self.assertEqual({k:v for k,v in row.items() if k!='revisions'},
                         {k:v for k,v in original.items() if k!='revisions'})
        self.assertEqual(a['memories'],[])
        self.assertEqual(len(a['historical_orientations']),1)
        self.assertEqual(row['id'],ref)
        e=course(a,'c1',5,'father','WITHHOLD')
        self.assertEqual(possible_lived_directional_orientation(a,e,'world:c1'),[])
        e=course(a,'c2',6,'father','WITHHOLD')
        reopen=possible_lived_directional_orientation(a,e,'world:c2')
        self.assertEqual(reopen[0]['revision_mode'],'REINSTATE')
        admit(a,e,'world:c2',reopen)
        self.assertIsNone(option(inherited.HistoricalSelfAndPrecueR19._r29_situated_beside(a,'father')))
        self.assertEqual(len(a['historical_orientations']),1)

    def test_different_other_or_interruption_does_not_release(self):
        a=adult('a','A'); course=inherited.HistoricalSelfAndPrecueR19._r29_lived_in_other_presence
        course(a,'a1',1,'father','WITHHOLD')
        e=course(a,'a2',2,'father','WITHHOLD')
        admit(a,e,'world:a2',possible_lived_directional_orientation(a,e,'world:a2'))
        course(a,'b1',3,'mother','APPROACH')
        e=course(a,'b2',4,'mother','APPROACH')
        self.assertEqual(possible_counterhistory_release(a,e,'world:b2'),[])
        course(a,'c1',5,'father','APPROACH')
        course(a,'c2',6,'father','WITHHOLD')
        e=course(a,'c3',7,'father','APPROACH')
        self.assertEqual(possible_counterhistory_release(a,e,'world:c3'),[])

    def test_actual_runtime_release_of_r19_hypothesis_survives_cold_reopen(self):
        parent={'source_ref':'R53_FICTIONAL_PARENT','source_grade':'SOURCEFREE_TEST_FIXTURE_NOT_EMPIRICAL',
                'answers':{'r53':'not_a_survey_observation'},'fictional_seed':{'projects':[]}}
        state={'acquire':True,'release':False}; offered=[]; packets=[]
        def callback(task,packet):
            if task=='adult_constructor':
                return HeuristicSemanticProvider().propose(task,packet)
            if task=='development':
                candidates=[]
                if packet['actor']['id']=='mother' and packet['experience'].get('own_action')=='EAT':
                    if state['acquire']:
                        candidates=[{'kind':'ACQUIRE_HISTORICAL_ORIENTATION',
                                     'operation':'EAT','orientation_mode':'WITHHOLD'}]
                        state['acquire']=False
                    else:
                        available=packet['historically_possible_counterhistory_release']
                        offered.append(deepcopy(available))
                        if state['release']:candidates=available
                return {'task':task,'candidates':candidates}
            if task=='actor_attempt':
                if packet['actor']['id']=='mother':
                    packets.append(deepcopy(packet))
                    if any(o['action']=='EAT' for o in packet['options']):
                        return {'task':task,'action':'EAT'}
                return {'task':task,'action':'WAIT'}
            if task=='expression':return {'task':task,'surface':'The household continues.'}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(callback))
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/'counterhistory.sqlite3')
            rt=ConstitutiveRuntime(db,semantic=service)
            try:
                rt.initialize([('mother','Mother',parent),('father','Father',parent)])
                rt.step('mother',requested_action='EAT')
                row=rt.snapshot('mother')['historical_orientations'][0]
                ref=row['id']
                self.assertTrue(any(x['action']=='EAT' for x in rt.situated('mother')['suspended_actions']))
                rt.step('mother',requested_action='EAT')
                self.assertFalse(any(offered))
                state['release']=True
                rt.step('mother',requested_action='EAT')
                self.assertTrue(any(offered),repr(rt.snapshot('mother')['lived_genesis_episodes']))
                self.assertFalse(any(x['action']=='EAT' for x in rt.situated('mother')['suspended_actions']))
                self.assertEqual(rt.snapshot('mother')['memories'],[])
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
            cold=ConstitutiveRuntime(db,semantic=service)
            try:
                self.assertEqual(cold.snapshot('mother')['historical_orientations'][0]['id'],ref)
                self.assertFalse(any(x['action']=='EAT' for x in cold.situated('mother')['suspended_actions']))
                self.assertTrue(any(x['action']=='EAT' for x in cold.situated('mother')['candidate_actions']))
                result=cold.step('mother')
                self.assertEqual(result['status'],'PERFORMED')
                self.assertTrue(packets)
                self.assertTrue(cold.verify()['valid'])
            finally:cold.close()

if __name__=='__main__':unittest.main()
