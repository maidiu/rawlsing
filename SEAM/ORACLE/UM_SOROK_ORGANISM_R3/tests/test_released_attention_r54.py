"""R54: actual exercised focal practice and the release of its priority."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider, ValidatingSemanticService, HeuristicSemanticProvider)
from um_sorok_organism.development import InvalidDevelopment

PARENT={'source_ref':'R54_FICTIONAL_PARENT','source_grade':'SOURCEFREE_TEST_FIXTURE_NOT_EMPIRICAL',
        'answers':{'r54':'not_a_survey_observation'},'fictional_seed':{'projects':[]}}

class ReleasedAttentionR54(unittest.TestCase):
    def run_arm(self, path, release, forge=False):
        controls={'focus':'zed','release':release,'forge':forge}
        proposals=[]; attempts=[]; expressions=[]
        def callback(task,packet):
            if task=='adult_constructor':
                return HeuristicSemanticProvider().propose(task,packet)
            if task=='development':
                offered=packet.get('historically_possible_monitoring_changes',[])
                if packet['actor']['id']=='mother' and offered:
                    proposals.extend(deepcopy(offered))
                    candidates=[p for p in offered if p['kind']=='ACQUIRE_HISTORICAL_ORIENTATION'
                                or (p['revision_mode']=='INHIBIT' and controls['release'])]
                    if controls['forge'] and candidates and candidates[0].get('revision_mode')=='INHIBIT':
                        candidates=deepcopy(candidates)
                        candidates[0]['monitoring_revision_basis']['counterpart_ref']='foreign'
                    return {'task':task,'candidates':candidates}
                return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if packet['actor']['id']=='mother':
                    attempts.append(deepcopy(packet))
                    for opt in packet.get('focal_encounter_options',[]):
                        if opt['counterpart_ref']==controls['focus']:
                            return {'task':task,'action':'ORIENT','focal_encounter_id':opt['attention_id']}
                return {'task':task,'action':'WAIT'}
            if task=='expression':
                expressions.append(deepcopy(packet))
                return {'task':task,'surface':'The household continues.'}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(callback))
        rt=ConstitutiveRuntime(str(path),semantic=service)
        guests=['x'+str(i) for i in range(8)]
        def rows(runtime):
            return [r for r in runtime.snapshot('mother')['historical_orientations']
                    if r.get('acquisition')=='LIVED_DIRECTED_MONITORING_PRACTICE']
        def focus(runtime):
            frame=runtime.situated('mother')['attention_frame']
            refs=set(frame['focally_eligible_cue_refs'])
            return {c['source_actor'] for c in runtime.see('mother')['cues']
                    if c['id'] in refs and c['kind']=='coactor_present'}
        try:
            rt.initialize([(a,a,PARENT) for a in ['mother','zed']+guests])
            for g in guests:
                self.assertEqual(rt.step(g,requested_action='MOVE',object_ref='workshop')['status'],'PERFORMED')
            rt.step('zed',requested_action='IMPOSE',target='mother')
            self.assertEqual(rows(rt),[])
            rt.step('mother')
            self.assertEqual(rows(rt),[])
            rt.step('mother')
            self.assertEqual(len(rows(rt)),1)
            original=deepcopy(rows(rt)[0])
            self.assertEqual(original['monitoring_basis']['counterpart_ref'],'zed')
            for g in guests:
                self.assertEqual(rt.step(g,requested_action='MOVE',object_ref='home')['status'],'PERFORMED')
            self.assertIn('zed',focus(rt))
            self.assertEqual(rt.situated('mother')['attention_frame']['monitoring_orientation_refs'],
                             [original['id']])
            rt.step('zed',requested_action='CARE',target='mother')
            self.assertEqual(rows(rt)[0]['revisions'],[])
            if forge:
                before=deepcopy(rt.ledger.actors()); world=deepcopy(rt.ledger.world(rt.world_id))
                with self.assertRaises(InvalidDevelopment):
                    rt.step('zed',requested_action='CARE',target='mother')
                self.assertEqual(rt.ledger.actors(),before)
                self.assertEqual(rt.ledger.world(rt.world_id),world)
                self.assertTrue(rt.verify()['valid'])
                return None
            rt.step('zed',requested_action='CARE',target='mother')
            self.assertTrue(any(p.get('revision_mode')=='INHIBIT' for p in proposals))
            row=rows(rt)[0]
            self.assertEqual({k:v for k,v in row.items() if k!='revisions'},
                             {k:v for k,v in original.items() if k!='revisions'})
            self.assertEqual(len(row['revisions']),int(release))
            self.assertEqual(rt.snapshot('mother')['memories'],[])
            selected=focus(rt);self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=ConstitutiveRuntime(str(path),semantic=service)
        try:
            self.assertEqual(focus(cold),selected)
            self.assertEqual(rows(cold)[0]['id'],original['id'])
            # Real independently selected focal activity with a different
            # available Other, not a new interest or motive by fiat.
            controls['focus']='x5'
            result=cold.step('mother')
            pathrow=cold.snapshot('mother')['evidence_paths'][-1]
            self.assertTrue(cold.verify()['valid'])
            self.assertNotIn('focal_encounter_receipt',expressions[-1]['actor_accessible'])
            return {'focus':selected,'received':pathrow.get('focal_encounter'),
                    'result':result,'options':attempts[-1].get('focal_encounter_options',[])}
        finally:cold.close()

    def test_actual_matched_release_changes_focal_selection_after_cold_reopen(self):
        with tempfile.TemporaryDirectory() as d:
            active=self.run_arm(Path(d)/'active.sqlite3',False)
            released=self.run_arm(Path(d)/'released.sqlite3',True)
        self.assertIn('zed',active['focus'])
        self.assertNotIn('zed',released['focus'])
        newly=released['focus']-active['focus']
        self.assertTrue(newly,(active['focus'],released['focus']))
        self.assertIn('x5',newly,(active['focus'],released['focus']))
        self.assertIsNone(active['received'])
        self.assertEqual(released['received']['counterpart_ref'],'x5')
        self.assertEqual(released['result']['status'],'PERFORMED')

    def test_forged_release_rolls_back_whole_event(self):
        with tempfile.TemporaryDirectory() as d:
            self.run_arm(Path(d)/'forged.sqlite3',True,forge=True)

if __name__=='__main__':unittest.main()
