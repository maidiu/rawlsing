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
        controls={'focus':'zed','release':release,'forge':forge,'stage':'monitor'}
        proposals=[]; attempts=[]; expressions=[]
        def callback(task,packet):
            if task=='adult_constructor':
                return HeuristicSemanticProvider().propose(task,packet)
            if task=='development':
                if packet['actor']['id']=='mother':
                    if controls['stage']=='new_focus':
                        memory=packet.get('historically_possible_focal_encounter_memory')
                        if memory:
                            return {'task':task,'candidates':[{'kind':'MEMORY',
                                'focal_encounter_ref':memory['focal_encounter_ref'],
                                'content':'I noticed someone else in the room.',
                                'cue_terms':['coactor']}]}
                    rec=packet.get('actual_private_rehearsal_analyst_only')
                    if controls['stage']=='rehearse' and rec:
                        return {'task':task,'candidates':[{'kind':'NOTICE_PRIVATE_POSSIBLE_END',
                            'rehearsal_ref':rec['id'],'possible_object':'explore ordinary surroundings',
                            'possible_means':['ORIENT']}]}
                    if controls['stage']=='takeup':
                        ends=[e for e in packet['actor_possible_ends'] if e.get('private_focal_encounter')]
                        if ends:
                            return {'task':task,'candidates':[{'kind':'TAKE_UP_POSSIBLE_END',
                                'possible_end_ref':ends[0]['id'],'means':['ORIENT']}]}
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
                    stage=controls['stage']
                    if stage=='rehearse':
                        opts=[o for o in packet['private_rehearsal_options'] if o.get('focal_encounter')]
                        if opts:return {'task':task,'action':'WAIT','private_rehearsal_id':opts[0]['rehearsal_id'],
                                        'private_rehearsal_content':'Perhaps I can look around without checking the same person.'}
                        return {'task':task,'action':'WAIT'}
                    if stage=='trial':
                        opts=[o for o in packet['possible_end_trials'] if o.get('private_rehearsal_ref')]
                        if opts:return {'task':task,'possible_end_trial_id':opts[0]['trial_id']}
                        return {'task':task,'action':'WAIT'}
                    if stage=='takeup':
                        return {'task':task,'action':'ORIENT' if packet.get('actor',{}).get('id')=='mother'
                                and release else 'WAIT'}
                    if stage=='project':
                        opts=[o for o in packet['practical_options'] if o.get('project_id')
                              and o['operation']=='ORIENT']
                        if opts:return {'task':task,'practical_option_id':opts[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
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
            controls['stage']='new_focus'
            result=cold.step('mother')
            pathrow=cold.snapshot('mother')['evidence_paths'][-1]
            self.assertTrue(cold.verify()['valid'])
            self.assertNotIn('focal_encounter_receipt',expressions[-1]['actor_accessible'])
            first={'focus':selected,'received':pathrow.get('focal_encounter'),
                   'result':result,'options':attempts[-1].get('focal_encounter_options',[])}
            a=cold.snapshot('mother')
            self.assertEqual(len(a['memories']),int(release))
            if release:
                self.assertEqual(a['memories'][0]['focal_encounter'],first['received'])
            controls['stage']='rehearse';cold.step('mother')
            a=cold.snapshot('mother')
            self.assertEqual(len(a['possible_ends']),int(release))
            if release:
                end=a['possible_ends'][0]
                self.assertEqual(end['private_focal_encounter'],first['received'])
                self.assertEqual(end['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
                self.assertEqual(len(a['projects']),0)
            controls['stage']='trial';cold.step('mother')
            a=cold.snapshot('mother')
            if release:self.assertEqual(len(a['possible_ends'][0]['trial_history']),1)
            controls['stage']='takeup';cold.step('mother')
            self.assertEqual(len(cold.snapshot('mother')['projects']),int(release))
            controls['stage']='project'
            continuation=cold.step('mother')
            self.assertEqual(continuation['attempt'],'ORIENT' if release else 'WAIT')
            self.assertTrue(cold.verify()['valid'])
            self.assertTrue(all('Perhaps I can look around' not in str(x) for x in expressions))
            return first
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
