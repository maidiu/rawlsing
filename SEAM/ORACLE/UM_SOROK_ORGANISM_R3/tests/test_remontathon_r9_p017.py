"""R9 SR-P017 bounded persistent signal regression — no invented object permanence."""
import tempfile,unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime

class R9PersistentSignals(unittest.TestCase):
    def test_explicit_lasting_sign_remains_accessible_until_its_recorded_end(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'sign.sqlite'))
            try:
                rt.initialize()
                row=rt.cue(kind='ringing_bell',tags=['bell','rhythm'],
                           location='home',lasting_ticks=2)
                signal_id=row['cue']['id']
                for clock in (1,2,3):
                    self.assertEqual(rt.ledger.world()[1]['clock'],clock)
                    self.assertIn(signal_id,{c['id'] for c in rt.see('nadia')['cues']})
                    if clock<3:rt.step('nadia',requested_action='WAIT')
                rt.step('nadia',requested_action='WAIT')
                self.assertNotIn(signal_id,{c['id'] for c in rt.see('nadia')['cues']})
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()

    def test_default_cue_still_expires_and_infinite_lifetime_is_not_assumed(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'ephemeral.sqlite'))
            try:
                rt.initialize()
                eid=rt.cue(kind='short_knock',tags=['knock'])['cue']['id']
                self.assertIn(eid,{c['id'] for c in rt.see('nadia')['cues']})
                rt.step('nadia',requested_action='WAIT')
                self.assertNotIn(eid,{c['id'] for c in rt.see('nadia')['cues']})
            finally:rt.close()

    def test_invalid_duration_does_not_append_life_or_world_event(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'invalid.sqlite'))
            try:
                rt.initialize()
                before=rt.ledger.world()[1]
                seq=rt.verify()['events']
                for invalid in (True,-1,1.25):
                    with self.assertRaisesRegex(ValueError,'INVALID_CUE_TIME'):
                        rt.cue(kind='bell',tags=['bell'],lasting_ticks=invalid)
                self.assertEqual(rt.ledger.world()[1],before)
                self.assertEqual(rt.verify()['events'],seq)
            finally:rt.close()
if __name__=='__main__':unittest.main()
