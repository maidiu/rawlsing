"""REMONTATHON R3: adversarial ledger existence and objective/private boundaries."""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import Attempt, adult, blank_world
from um_sorok_organism.world import resolve

class NextRealFaults(unittest.TestCase):
    def test_p042_deleting_every_event_cannot_turn_life_into_a_valid_empty_chain(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.sqlite3'))
            try:
                rt.initialize([])  # child only, no source seals to mask the defect
                self.assertEqual(rt.verify()['events'],1)
                rt.ledger.conn.execute('DELETE FROM events')
                with self.assertRaisesRegex(AssertionError,'MISSING_OBJECTIVE_EVENT_HISTORY'):
                    rt.verify()
            finally:rt.close()

    def test_p043_ledger_event_payload_byte_mutation_without_semantic_change_is_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'life.sqlite3'))
            try:
                rt.initialize([])
                original=rt.ledger.conn.execute('SELECT payload FROM events WHERE seq=1').fetchone()[0]
                rt.ledger.conn.execute('UPDATE events SET payload=? WHERE seq=1',(' '+original+' ',))
                with self.assertRaisesRegex(AssertionError,'EVENT_ENVELOPE_NONCANONICAL_BYTES'):
                    rt.verify()
            finally:rt.close()

    def test_p044_private_credit_shortfall_is_not_world_public_history(self):
        world=blank_world()
        world['positions'].update({'buyer':'workshop','witness':'workshop'})
        actors={'buyer':adult('buyer','Buyer',location='workshop'),
                'witness':adult('witness','Witness',location='workshop')}
        result=resolve(world,actors,Attempt('buyer','BUY_FOOD'))
        self.assertEqual(result.status,'BLOCKED')
        self.assertEqual(result.objective_description,'INSUFFICIENT_CLAIM_ON_FOOD')
        self.assertNotIn('INSUFFICIENT_CLAIM_ON_FOOD',str(world['public_history'][-1]))
        self.assertEqual(world['public_history'][-1]['outcome'],'ATTEMPT_NOT_COMPLETED')
        # The privileged objective world receipt is NOT rewritten to please the witness.
        self.assertEqual(result.world_delta['event']['outcome'],'INSUFFICIENT_CLAIM_ON_FOOD')
