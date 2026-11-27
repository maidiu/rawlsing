"""R58: actual worker-funded relief and the optional revision of work pressure."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider
from um_sorok_organism.development import InvalidDevelopment
from test_labor_dependency_r19 import PARENT, employment_spec
from test_tco_r25_recurrent_work_organization import proposal

class ReliefReconstitution(unittest.TestCase):
    def arm(self,db,nominate,*,forge=False):
        phase={'stage':'work'}
        offers=[]
        def cb(task,p):
            if task=='adult_constructor':return HeuristicSemanticProvider().propose(task,p)
            if task=='expression':return {'task':task,'surface':'Ordinary life continues.'}
            if task=='development':
                if p['actor']['id']!='mother':return {'task':task,'candidates':[]}
                if phase['stage']=='work':
                    q=p.get('historically_possible_recurrent_livelihood_orientation',[])
                    return {'task':task,'candidates':[proposal(q[0],'APPROACH')] if q else []}
                if phase['stage']=='relief':
                    q=p.get('historically_possible_relief_reconstitution',[])
                    offers.extend(deepcopy(q))
                    if q and nominate:
                        v=deepcopy(q[0])
                        if forge:v['relief_reconstitution_basis']['unfinished_work_ref']='foreign'
                        return {'task':task,'candidates':[v]}
                return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if phase['stage']=='relief':return {'task':task,'action':'DRAW_WAGE_RELIEF'}
                if phase['stage']=='later':
                    # Actual historical recruitment, not an invented mandatory refusal.
                    options=p.get('practical_options',[])
                    if any(x.get('operation')=='WORK' for x in options) and any(
                            c.get('action')=='WORK' and c.get('kind')=='HISTORICALLY_RECRUITED_PRE_CUE_PRESSURE'
                            for c in p['situated']['currents']):
                        return {'task':task,'action':'WORK'}
                return {'task':task,'action':'WAIT'}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            rt.initialize([('mother','Mother',PARENT),('father','Father',PARENT)])
            spec=rt.register_sourcefree_work_regime(employment_spec())
            for a in ('mother','father'):
                rt.step(a,requested_action='MOVE',object_ref='workshop')
                rt.step(a,requested_action='INSPECT',object_ref=spec['terms_notice_ref'])
                self.assertEqual(rt.step(a,requested_action='ACCEPT_WORK_TERMS')['status'],'PERFORMED')
            for i in range(3):
                rt.step('mother',requested_action='REST')
                rt.step('mother',requested_action='REST')
                self.assertEqual(rt.step('mother',requested_action='WORK')['status'],'PERFORMED')
            old=deepcopy(rt.snapshot('mother')['historical_orientations'][0])
            self.assertEqual(old['orientation_mode'],'APPROACH')
            phase['stage']='quiet'
            rt.step('mother',requested_action='REST')
            rt.step('mother',requested_action='REST')
            rt.step('father',requested_action='REST')
            rt.step('father',requested_action='WORK')
            self.assertEqual(rt.step('father',requested_action='CONTRIBUTE_WAGE_RELIEF')['status'],'PERFORMED')
            self.assertEqual(rt.step('father',requested_action='SUSPEND_WAGE_WORK',target='mother')['status'],'PERFORMED')
            self.assertEqual(rt.step('mother',requested_action='WORK')['status'],'BLOCKED')
            before=deepcopy(rt.ledger.world('w1')[1]); actor_before=deepcopy(rt.snapshot('mother'))
            phase['stage']='relief'
            if forge:
                with self.assertRaises(InvalidDevelopment):rt.step('mother')
                self.assertEqual(rt.snapshot('mother'),actor_before)
                self.assertEqual(rt.ledger.world('w1')[1],before)
                self.assertTrue(rt.verify()['valid'])
                return
            self.assertEqual(rt.step('mother')['status'],'PERFORMED')
            self.assertEqual(len(offers),1)
            world=rt.ledger.world('w1')[1]
            self.assertEqual(world['accounts']['mother'],before['accounts']['mother']+.25)
            self.assertEqual(world['accounts'][spec['relief_pool_ref']],0)
            self.assertEqual(world['work_regimes']['workshop']['contracts']['mother']['status'],'ACTIVE')
            row=rt.snapshot('mother')['historical_orientations'][0]
            self.assertEqual({k:v for k,v in row.items() if k!='revisions'},
                             {k:v for k,v in old.items() if k!='revisions'})
            self.assertEqual(len(row['revisions']),int(nominate))
            phase['stage']='quiet'
            for _ in range(5):rt.step('mother',requested_action='REST')
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            view=cold.situated('mother')
            self.assertTrue(any(o['action']=='WORK' for o in view['candidate_actions']))
            currents=[c for c in view['currents'] if c.get('ref')==old['id']
                      and c.get('action')=='WORK']
            self.assertEqual(bool(currents),not nominate)
            # Fresh actor selection remains lawful in both cases, even after
            # the old historical pressure is suspended.
            phase['stage']='later'
            self.assertEqual(cold.step('mother')['attempt'],'WAIT' if nominate else 'WORK')
            self.assertTrue(cold.verify()['valid'])
        finally:cold.close()
    def test_same_real_relief_optional_work_orientation_revision(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'retained.sqlite',False)
            self.arm(Path(d)/'revised.sqlite',True)
    def test_foreign_relief_lineage_refused_atomically(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'forged.sqlite',True,forge=True)
