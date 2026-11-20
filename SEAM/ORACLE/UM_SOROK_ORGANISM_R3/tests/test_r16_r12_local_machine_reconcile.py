"""R16: import true non-overlapping R12 local-machine fixes onto R15."""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.types import adult, blank_world, stable_id, copy
from um_sorok_organism.storage import ResearchLedger
from um_sorok_organism.constitution import actor_access, compose, materialize
from um_sorok_organism.world import add_cue
from um_sorok_organism.development import admit, InvalidDevelopment


class ExactSnapshotTypeR16(unittest.TestCase):
    def test_canonical_nonobject_world_snapshot_is_a_typed_failure(self):
        with tempfile.TemporaryDirectory() as d:
            l = ResearchLedger(str(Path(d)/'w.db'))
            try:
                l.initialize(blank_world(), [adult('ann','Ann')])
                for literal in ('[]', 'null', 'true', '42', '"literal"'):
                    with self.subTest(literal=literal):
                        original=l.conn.execute('SELECT body FROM worlds').fetchone()[0]
                        try:
                            l.conn.execute('UPDATE worlds SET body=?',(literal,))
                            with self.assertRaisesRegex(AssertionError, 'WORLD_SNAPSHOT_NOT_OBJECT'):
                                l.verify_chain()
                        finally:
                            l.conn.execute('UPDATE worlds SET body=?',(original,))
                self.assertTrue(l.verify_chain()['valid'])
            finally: l.close()

    def test_canonical_nonobject_actor_snapshot_is_a_typed_failure(self):
        with tempfile.TemporaryDirectory() as d:
            l = ResearchLedger(str(Path(d)/'a.db'))
            try:
                l.initialize(blank_world(), [adult('ann','Ann')])
                for literal in ('[]', 'null', 'false', '0', '"actor"'):
                    with self.subTest(literal=literal):
                        original=l.conn.execute('SELECT body FROM actors').fetchone()[0]
                        try:
                            l.conn.execute('UPDATE actors SET body=?',(literal,))
                            with self.assertRaisesRegex(AssertionError, 'ACTOR_SNAPSHOT_NOT_OBJECT'):
                                l.verify_chain()
                        finally:
                            l.conn.execute('UPDATE actors SET body=?',(original,))
                self.assertTrue(l.verify_chain()['valid'])
            finally: l.close()


class SortedRecruitmentR16(unittest.TestCase):
    def test_recruited_forms_are_deterministically_sorted(self):
        actor=adult('ann','Ann')
        # All same cue, independent and qualified: set ordering is not actor evidence.
        ids=['kappa','omega','alpha','zeta','mu','theta','beta','phi','eta','gamma',
             'nu','delta','xi','sigma','rho','iota','tau']
        for fid in ids:
            actor['forms'][fid]={
                'id':fid,'actor':'ann','kind':'PRACTICE','origin':['historical:'+fid],
                'cues':['bell'],'enables':['SING'],'strength':.4,'body_min':0,
                'lifecycle':'ACTIVE','scope':{}}
        world=blank_world();world['positions']={'ann':'home'}
        add_cue(world,'bell',['bell'],location='home')
        situated=compose(materialize(actor,world),actor_access(actor,world))
        self.assertEqual([f['id'] for f in situated.recruited], sorted(ids))
        sing=next(x for x in situated.candidate_actions if x['action']=='SING')
        self.assertEqual([v for v in sing['basis'] if v in ids],sorted(ids))


class TrialBoundaryR16(unittest.TestCase):
    def test_issued_trial_cannot_take_up_another_possible_end_in_same_event(self):
        a=adult('a','A')
        a['possible_ends']=[{
            'id':v,'origin_event':'old_event_'+v,'experience_ref':'old_experience_'+v,
            'possible_object':v+'_possible','possible_means':['SING'],
            'cue_terms':['song'],'status':'POSSIBLE_NOT_ACQUIRED_MOTIVE'}
            for v in ('end_a','end_b')]
        ex={'actor':'a','ref':'current_experience','own_action':'SING','status':'PERFORMED',
            'participated':True,'felt_enactment':{'attempted_operation':'SING'},
            'perceived_cues':[{'id':'cue_received','tags':['song']} ]}
        ticket={'trial_id':stable_id('end_trial',{'actor':'a','clock':4,
                       'end':'end_a','operation':'SING'}),
                'actor':'a','as_of_clock':4,'possible_end_ref':'end_a',
                'operation':'SING','origin_event':'old_event_end_a',
                'origin_experience_ref':'old_experience_end_a','actor_project_ref':None}
        before=copy(a)
        # This is a distinct, already noticed end, but today's ACT is issued
        # as exploratory for end_a, not an opportunity to mint a separate
        # mature project for end_b from the same disputed world event.
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_NOT_MATURE_MOTIVE'):
            admit(a,ex,'current_event',[{'kind':'TAKE_UP_POSSIBLE_END',
                'possible_end_ref':'end_b','means':['SING'],'priority':.35}],
                issued_trial=ticket)
        self.assertEqual(a,before)

if __name__ == '__main__': unittest.main()
