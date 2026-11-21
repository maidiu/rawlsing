"""RED: missing canonical byte verification of stored world/actor snapshots."""
import tempfile,unittest
from pathlib import Path
from um_sorok_organism.storage import ResearchLedger
from um_sorok_organism.types import blank_world,adult
class NewP070SnapshotBytes(unittest.TestCase):
    def test_whitespace_mutation_to_stored_world_and_actor_must_not_verify(self):
        with tempfile.TemporaryDirectory() as d:
            l=ResearchLedger(str(Path(d)/'tamper.sqlite'))
            try:
                l.initialize(blank_world(),[adult('ann','Ann')])
                for table in ('worlds','actors'):
                    original=l.conn.execute(f'SELECT body FROM {table} LIMIT 1').fetchone()[0]
                    l.conn.execute(f'UPDATE {table} SET body=?',(' '+original,))
                    with self.subTest(table=table):
                        with self.assertRaisesRegex(AssertionError,'NONCANONICAL|CHANGED'):
                            l.verify_chain()
                    l.conn.execute(f'UPDATE {table} SET body=?',(original,))
                self.assertTrue(l.verify_chain()['valid'])
            finally:l.close()

class NewP071MalformedSensoryState(unittest.TestCase):
    def test_nan_actor_sensor_cannot_see_high_threshold_cue(self):
        from um_sorok_organism.types import blank_world,adult
        from um_sorok_organism.world import add_cue
        from um_sorok_organism.constitution import actor_access
        world=blank_world();world['clock']=1;world['positions']={'ann':'home'}
        cue=add_cue(world,'distant_bell',['bell'],location='home',threshold=.95)
        actor=adult('ann','Ann');actor['body']['sensor']=float('nan')
        with self.assertRaisesRegex(ValueError,'INVALID_BODY_STATE:sensor'):
            actor_access(actor,world)

class NewP070WorldRoster(unittest.TestCase):
    def test_uncommitted_second_world_must_not_be_certified_as_one_world(self):
        with tempfile.TemporaryDirectory() as d:
            l=ResearchLedger(str(Path(d)/'secondworld.sqlite'))
            try:
                l.initialize(blank_world(),[adult('ann','Ann')])
                other=blank_world('w2')
                from um_sorok_organism.types import canonical
                l.conn.execute('INSERT INTO worlds(id,version,body) VALUES(?,?,?)',('w2',0,canonical(other)))
                with self.assertRaisesRegex(AssertionError,'UNCOMMITTED_WORLD_ROSTER'):
                    l.verify_chain()
            finally:l.close()
