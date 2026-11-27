"""R33: same inscription, different material acquisition history.
Only fictional already exposed face is read. No search of private interiors,
automatic human belief, or Other's knowledge of the private presentation.
"""
from copy import deepcopy
import unittest
import test_neighbor_public_notice_r10 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from neighbor_runtime import NeighborEncounter
import mii

WORDS = inherited.WORDS
HIDDEN = 'Unexposed fictional interior; never present this.'
def document(**changes):
    row = {'id':'bill', 'kind':'INCIDENTALLY_EXPOSED_DOCUMENT',
           'location':'workshop', 'visible':True, 'grade':'SOURCEFREE_TEST_ONLY',
           'exposed_face':WORDS, 'public_glance':'Do not use generic text.',
           'public_close':HIDDEN,
           'public_recognition':{'identity':HIDDEN,'marking':'face','evidence':WORDS}}
    row.update(changes)
    return row

class ResistantEvidenceR33(unittest.TestCase):
    def build(self, **kw):
        inherited.PublicNoticeR10.build(self, **kw)

    def read(self, ref, request):
        result = self.n.contribute(request, 'LOOK', target_object_ref=ref)
        self.assertEqual(result['status'], 'PERFORMED')
        world = deepcopy(self.rt.ledger.world('w1'))
        actors = deepcopy(self.rt.ledger.actors())
        surface = self.n.private_surface_stored(self.sidecar, command='look', target=ref)
        self.assertEqual(self.rt.ledger.world('w1'), world)
        self.assertEqual(self.rt.ledger.actors(), actors)
        self.assertNotIn(HIDDEN, str(surface))
        self.assertEqual(surface['optional']['acquisition_provenance']['look_receipt'],
                         result['receipt'])
        return result, surface['optional']

    def test_equal_text_different_cold_acquisition_and_independent_afterlife(self):
        self.build(objects={'bill':document()})
        _, notice = self.read('hall-poster','public')
        _, face = self.read('bill','face')
        self.assertEqual(notice['text'], face['text'])
        self.assertEqual(face['text'], WORDS)
        pub = notice['acquisition_provenance']
        inc = face['acquisition_provenance']
        self.assertEqual(pub['route'],'PUBLIC_INSTITUTIONAL_DISPLAY')
        self.assertEqual(inc['route'],'INCIDENTALLY_EXPOSED_MATERIAL_FACE')
        self.assertNotEqual(pub['look_receipt'],inc['look_receipt'])
        self.assertEqual(inc['personal_entrusting'],'NOT_ESTABLISHED')
        self.assertEqual(inc['content_truth'],'NOT_ESTABLISHED')
        self.assertEqual(inc['human_comprehension'],'NOT_ESTABLISHED')
        self.assertEqual(inc['further_access'],'NOT_GRANTED')
        self.assertFalse(any(WORDS in c['description'] for c in self.rt.see('worker')['cues']))
        self.assertEqual(self.rt.ledger.actors()['worker'].get('notice_exposures',[]),[])
        self.n.contribute('wait','WAIT')
        self.rt.close()
        self.rt=ConstitutiveRuntime(self.db)
        self.n=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        p=self.n.load_private_profile(self.sidecar)
        saved=[e['rendered']['optional']['acquisition_provenance']
               for e in p['exposures']]
        self.assertEqual(saved,[pub,inc])
        self.assertNotIn(HIDDEN,str(p))
        # Actual freely authored speech is a separate event. It can disclose
        # a claim about the acquisition route; the actor cannot borrow MII.
        said='I saw the words on an exposed document.'
        result=self.n.contribute('tell','SAY',text=said)
        self.assertEqual(result['status'],'PERFORMED')
        cues=self.rt.see('worker')['cues']
        self.assertTrue(any(c.get('description')==said for c in cues))
        self.assertFalse(any('acquisition_provenance' in c for c in cues))
        beat=self.n.independent_actor_beat('worker')
        last=self.rt.ledger.events()[-1]
        self.assertEqual(last['kind'],'ACTOR_LIFE_TRANSITION')
        readset=last['envelope']['payload']['private_pre_event_psychodynamics']['worker']['readset']
        for cue in result['potential_actor_evidence']:
            self.assertIn(cue['cue_ref'],readset)
        self.assertNotIn('visitor',self.rt.ledger.actors())
        self.assertTrue(self.rt.verify()['valid'])

    def test_face_requires_real_turn_and_legibility_in_present_world(self):
        self.build(notices=[],objects={'bill':document()},legibility='unreadable')
        first=self.n.private_surface(self.n.new_private_profile(),command='look',target='bill')
        self.assertEqual(first['optional']['text'],'An exposed document lies here.')
        out=self.n.contribute('look','LOOK',target_object_ref='bill')
        self.assertEqual(out['status'],'PERFORMED')
        after=self.n.private_surface(self.n.new_private_profile(),command='look',target='bill')
        self.assertEqual(after['optional']['text'],first['optional']['text'])
        self.assertNotIn('acquisition_provenance',after['optional'])
        self.assertNotIn(WORDS,str(after))
        self.assertNotIn(HIDDEN,str(after))

    def test_unexposed_or_unqualified_document_cannot_be_read_or_turned_toward(self):
        for change in ({'visible':False},{'grade':'UNQUALIFIED'},
                       {'id':'wrong'},{'exposed_face':None}):
            with self.subTest(change=change):
                self.build(notices=[],objects={'bill':document(**change)})
                self.assertEqual(self.n.contribute('look','LOOK',target_object_ref='bill')['status'],
                                 'BLOCKED')
                view=self.n.private_surface(self.n.new_private_profile(),command='look',target='bill')
                self.assertIsNone(view['optional'])
                self.assertNotIn(HIDDEN,str(view))
                self.assertTrue(self.rt.verify()['valid'])
                self.rt.close()

if __name__=='__main__':unittest.main()
