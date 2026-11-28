"""R62: existing adults remain themselves through a selected genealogy.
Sourcefree conditional conception/birth, no inferred reproductive consent.
"""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import newborn
from um_sorok_organism.storage import Conflict
from um_sorok_organism.semantics import (
    HeuristicSemanticProvider, CallbackLLMProvider, ValidatingSemanticService)


def packet(who):
    return {'input_kind':'THIN_BIOGRAPHY','source_grade':'EXPLICIT_FICTIONAL_HISTORICAL_INPUT',
            'source_ref':'fictional:'+who,'biographical_context':{'ordinary_life':who},
            'fictional_seed':{'projects':[{'object':'ordinary life '+who,
                  'means':['REST','EAT'],'priority':.5}]}}


def pathway():
    return {'id':'retained','source_ref':'fictional:path','intersection_clock':2,
            'intersection_site':'home','conception_clock':3,'birth_clock':5,
            'counterpart_id':'father','counterpart_name':'Father','counterpart_packet':None,
            'child_id':'nadia','child_name':'Nadia',
            'prior_shared_effects':'RETAIN_EXISTING_ACTUAL_HISTORY'}


class ExistingFamilyContinuity(unittest.TestCase):
    def test_actual_adult_history_survives_binding_birth_and_later_activity(self):
        with tempfile.TemporaryDirectory() as d:
            calls=[];fallback=HeuristicSemanticProvider();phase={'acquire':True}
            def cb(task,p):
                if task=='adult_constructor':
                    calls.append(p['actor_id']);return fallback.propose(task,p)
                if task=='family_pathway_selection':
                    self.assertNotIn('counterpart_packet',str(p['eligible_pathways']))
                    self.assertNotIn('father secret',str(p))
                    return {'task':task,'pathway_id':'retained'}
                if task=='development':
                    if p['actor']['id']=='father' and phase['acquire']:
                        phase['acquire']=False
                        return {'task':task,'candidates':[{'kind':'ACQUIRE_HISTORICAL_ORIENTATION',
                            'operation':'EAT','orientation_mode':'WITHHOLD'},
                            {'kind':'MEMORY','content':'father secret','cue_terms':['rest']}]}
                    return {'task':task,'candidates':[]}
                if task=='actor_attempt':
                    if p['actor']['id']=='father':
                        return {'task':task,'action':'EAT' if any(x['action']=='EAT' for x in p['options']) else 'WAIT'}
                    return {'task':task,'action':'WAIT'}
                if task=='expression':
                    self.assertNotIn('father secret',str(p))
                    return {'task':task,'surface':'Ordinary life.'}
                return fallback.propose(task,p)
            service=ValidatingSemanticService(CallbackLLMProvider(cb))
            db=Path(d)/'family.sqlite'
            rt=ConstitutiveRuntime(str(db),semantic=service)
            try:
                rt.initialize_antecedent_adult('mother','Mother',packet('mother'),
                    other_adults=[('father','Father',packet('father'))])
                self.assertEqual(calls,['mother','father'])
                sid=rt.register_family_pathways('mother',[pathway()])['source_seal_id']
                self.assertEqual(rt.step('father',requested_action='REST')['status'],'PERFORMED')
                self.assertEqual(rt.step('mother')['status'],'PERFORMED')
                old=deepcopy(rt.ledger.actor('father')[1]);mother=deepcopy(rt.ledger.actor('mother')[1])
                events=deepcopy(rt.ledger.events());version,world=rt.ledger.world()
                self.assertTrue(old['historical_orientations'])
                self.assertTrue(old['memories'])
                self.assertEqual(rt.select_family_intersection(sid)['actor'],'father')
                self.assertEqual(calls,['mother','father'])
                self.assertEqual(rt.ledger.actor('father')[1],old)
                self.assertEqual(rt.ledger.actor('mother')[1],mother)
                self.assertEqual(rt.ledger.events()[:len(events)],events)
                after=rt.ledger.world()[1]
                self.assertEqual({k:v for k,v in after.items() if k!='family_genesis'},world)
                self.assertEqual(set(rt.ledger.actors()),{'mother','father'})
                self.assertEqual(rt.step('father',requested_action='CARE',target='mother')['status'],'PERFORMED')
                rt.admit_family_conception()
                rt.background(2)
                rt.realize_family_birth()
                self.assertEqual(rt.ledger.actor('nadia')[1],newborn('nadia','Nadia'))
                self.assertEqual(rt.ledger.actor('father')[1]['historical_orientations'],old['historical_orientations'])
                self.assertEqual(rt.ledger.actor('father')[1]['memories'],old['memories'])
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
            rt=ConstitutiveRuntime(str(db),semantic=service)
            try:
                self.assertEqual(rt.step('father')['attempt'],'WAIT')
                self.assertEqual(rt.step('father',requested_action='CARE',target='nadia')['status'],'PERFORMED')
                self.assertTrue(rt.ledger.actor('nadia')[1]['experienced_care_events'])
                self.assertEqual(calls,['mother','father'])
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()

    def test_unlocated_existing_counterpart_and_forged_binding_refused(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'negative.sqlite'))
            try:
                rt.initialize_antecedent_adult('mother','Mother',packet('mother'),
                    other_adults=[('father','Father',packet('father'))])
                bad=pathway();bad['counterpart_packet']=packet('father')
                with self.assertRaisesRegex(ValueError,'FAMILY_PATHWAY_OVERLAP_OR_IDENTITY'):
                    rt.register_family_pathways('mother',[bad])
                sid=rt.register_family_pathways('mother',[pathway()])['source_seal_id']
                rt.step('father',requested_action='MOVE',object_ref='workshop')
                rt.step('mother',requested_action='WAIT')
                v,world=rt.ledger.world();before=deepcopy(world);n=rt.verify()['events']
                with self.assertRaisesRegex(ValueError,'FAMILY_NO_SITUATED_PATHWAY'):
                    rt.select_family_intersection(sid)
                forged=deepcopy(world);forged['family_genesis']={'stage':'COUNTERPART_ADMITTED'}
                with self.assertRaises(Conflict):
                    rt.ledger.commit(rt.world_id,v,forged,{}, {},
                        'FAMILY_EXISTING_COUNTERPART_BOUND','father',{'family_genesis':forged['family_genesis']})
                self.assertEqual(rt.ledger.world()[1],before)
                self.assertEqual(rt.verify()['events'],n)
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
