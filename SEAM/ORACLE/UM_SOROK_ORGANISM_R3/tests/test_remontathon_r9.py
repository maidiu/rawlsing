"""R9 SR-P011: sourcefree action ≠ earned continuing motive.

A deterministic fallback must not manufacture a durable end solely because
one SING operation succeeded. Qualified project proposal/admission remains
possible through the pre-existing owner interface. No general learning law.
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import HeuristicSemanticProvider
from um_sorok_organism.development import admit
from um_sorok_organism.types import newborn


def performed_packet():
    return {'actor':{'id':'nadia','location':'home'}, 'clock':1,
        'actor_forms':{},'selected_constitution':{'recruited':[]},
        'experience':{'actor':'nadia','ref':'exp:1','own_action':'SING',
                      'participated':True,'status':'PERFORMED',
                      'perceived_cues':[{'kind':'song','tags':['sing','rhythm']}]}}


class P011SingleEpisodeNotEnd(unittest.TestCase):
    def test_single_successful_song_cannot_heuristically_mint_continuing_project(self):
        row=HeuristicSemanticProvider().propose('development',performed_packet())
        self.assertTrue(any(x['kind']=='ADD_FORM' for x in row['candidates']))
        self.assertFalse(any(x['kind']=='ADD_PROJECT' for x in row['candidates']),
            'one technically performed song cannot prove an enduring project')

    def test_first_song_records_practice_without_creating_project_in_real_runtime(self):
        with tempfile.TemporaryDirectory() as directory:
            r=ConstitutiveRuntime(str(Path(directory)/'p011.sqlite'))
            try:
                r.initialize()
                r.background(365)
                r.step('nadia',requested_action='SING')
                person=r.snapshot('nadia')
                self.assertTrue(any('SING' in form.get('enables',[]) for form in person['forms'].values()))
                self.assertFalse(any('rhythm' in p.get('object','') for p in person['projects']))
                self.assertTrue(r.verify()['valid'])
            finally:
                r.close()

    def test_separately_owner_admitted_project_remains_possible(self):
        actor=newborn('nadia','Nadia')
        exp={'actor':'nadia','ref':'exp:1','own_action':'SING','participated':True,
             'status':'PERFORMED','perceived_cues':[{'kind':'song','tags':['sing']}],
             'felt_enactment':{'attempted_operation':'SING'}}
        project={'id':'project:proposed_by_semantics','object':'test whether a song can continue',
                 'means':['SING','PRACTICE'],'priority':.3,'cue_terms':['sing'],
                 'status':'active'}
        reported=admit(actor,exp,'event:1',[{'kind':'ADD_PROJECT','project':project}])
        self.assertTrue(any(x['kind']=='ADD_PROJECT' for x in reported))
        self.assertEqual(actor['projects'][0]['id'],'project:proposed_by_semantics')
        self.assertEqual(actor['projects'][0]['origin'],['event:1'])

if __name__=='__main__':unittest.main()
