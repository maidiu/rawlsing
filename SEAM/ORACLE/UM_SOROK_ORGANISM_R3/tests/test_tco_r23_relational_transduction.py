"""SEAM/30 THREE_AGENT_MULCH R23: acquired relations can be causally operative.

Not approval of objective harm, unconscious mind-reading, a real church model,
or a scientifically unique human response. All forms and witnesses are
explicitly sourcefree fictional fixtures; owner-qualified historical admission
and independent world settlement remain independent.
"""
from dataclasses import asdict
import unittest

from um_sorok_organism.types import AccessibleEncounter, Constitution, adult, copy
from um_sorok_organism.constitution import compose
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.relational_metabolism import (
    validate_motif, InvalidRelationalMotif,
)


def form(fid, operation, *, tendency=None):
    return {
        'id':fid,'actor':'mother','kind':'RELATIONAL_INVESTMENT',
        'origin':['sourcefree_fictional_prior:mother'],
        'grade':'SOURCEFREE_RESEARCH_PROVISIONAL',
        'cues':['corrective_ritual'],'enables':[operation],
        'scope':{},'lifecycle':'ACTIVE','strength':.7,
        'body_min':.1,'access':'tacit',
        'tendencies':[tendency] if tendency else [],
    }


def motif():
    return {
        'id':'historically_learned_care_authority',
        'source_forms':['care','authority'],
        'cue_terms':['corrective_ritual'],
        'locations':['home'],
        'witnessed_source_actor_ref':'pastor',
        'origin':['sourcefree_fictional_prior:care_and_authority'],
        'status':'ACTIVE',
        'effects':[{
            'kind':'RELATION_MEDIATION',
            'source':'care','target':'authority',
            'relation':'SUBORDINATES',
            'mediated_action':'IMPOSE','polarity':'APPROACH',
        }],
    }


def read_model(*, inhibited=None, withhold=False, motif_override=None):
    forms={
        'care':form('care','CARE'),
        'authority':form('authority','IMPOSE',tendency={
            'action':'IMPOSE','polarity':'WITHHOLD',
            'cue_terms':['corrective_ritual'],
        } if withhold else None),
    }
    links=[]
    if inhibited:
        forms['guard']=form('guard','WAIT')
        links=[{
            'source':'guard','target':inhibited,'relation':'INHIBITS',
            'contexts':['home'],'origin':['sourcefree_prohibition'],
        }]
    c=Constitution(
        actor='mother',clock=7,
        body=adult('mother','Mother')['body'],
        forms=forms,links=links,projects=[],
        activity_links=[],composition_methods=[],
        memories=[],traces=[],other_models={},self_model={},
        relations=[],unknowns=[],
        relational_motifs=[copy(motif_override if motif_override is not None
                                 else motif())],
    )
    return c


def encounter(*, speaker='pastor', kind='speech', place='home',
              tags=('corrective_ritual',)):
    return AccessibleEncounter(
        'mother',7,place,[{
            'id':'objective:rebuke:7',
            'clock':7,'kind':kind,'tags':list(tags),
            'source_actor':speaker,'location':place,
            'modality':'auditory',
        }],[],['objective:rebuke:7'])


def mediated(s):
    return [c for c in s.currents
            if c['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT'
            and c.get('mediation_mode')==
            'HISTORICALLY_ACQUIRED_RELATION_TRANSDUCTION']


def lived():
    return {'actor':'mother','ref':'lived:mother:new_contrast',
            'participated':True,
            'perceived_cues':[{'id':'objective:neighbor_contrast'}],
            'status':'OBSERVED','own_action':None}


class ThreeAgentMulchR23(unittest.TestCase):
    def test_admitted_relation_itself_operates_not_merely_narrates(self):
        s=compose(read_model(),encounter())
        self.assertEqual(len(mediated(s)),1)
        self.assertEqual(mediated(s)[0]['action'],'IMPOSE')
        self.assertEqual(mediated(s)[0]['polarity'],'APPROACH')
        self.assertEqual(mediated(s)[0]['relation_transduced'],'SUBORDINATES')
        self.assertTrue(mediated(s)[0]['not_objective_justification_of_conduct'])
        a=next(o for o in s.candidate_actions if o['action']=='IMPOSE')
        self.assertEqual(
            a['psychodynamic_status'],
            'ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT')
        self.assertIn('motif:historically_learned_care_authority',
                      a['support_currents'])
        self.assertTrue(any(
            c['kind']=='ACQUIRED_PERSONAL_SENSE_MEDIATION'
            and c['operative_mediation'] for c in s.currents))
        self.assertIn('historically_learned_care_authority',s.readset)

    def test_same_words_by_different_other_do_not_identify_authority(self):
        s=compose(read_model(),encounter(speaker='neighbor'))
        self.assertEqual(mediated(s),[])
        self.assertNotIn('historically_learned_care_authority',s.readset)
        self.assertIn('IMPOSE',{o['action'] for o in s.candidate_actions})
        self.assertFalse(any(
            o.get('support_currents') for o in s.candidate_actions
            if o['action']=='IMPOSE'))

    def test_ambient_co_presence_is_not_a_witnessed_authority_event(self):
        s=compose(read_model(),encounter(kind='coactor_present'))
        self.assertEqual(mediated(s),[])
        self.assertFalse(any(
            c['kind']=='ACQUIRED_RELATIONAL_CONFIGURATION'
            for c in s.currents))

    def test_material_setting_and_ritual_genre_are_conditional(self):
        for e in (
            encounter(place='market'),
            encounter(tags=('unfamiliar_utterance',)),
        ):
            with self.subTest(place=e.location,tags=e.cues[0]['tags']):
                self.assertEqual(mediated(compose(read_model(),e)),[])

    def test_inhibited_care_remains_indirectly_causal_not_restored(self):
        s=compose(read_model(inhibited='care'),encounter())
        self.assertIn('care',s.inhibited)
        self.assertNotIn('care',{f['id'] for f in s.recruited})
        self.assertNotIn('CARE',{o['action'] for o in s.candidate_actions})
        self.assertEqual(len(mediated(s)),1)
        self.assertTrue(mediated(s)[0]['has_inhibited_source'])
        self.assertTrue(any(
            c['kind']=='ACQUIRED_PERSONAL_SENSE_MEDIATION'
            and c['has_inhibited_source'] for c in s.currents))

    def test_inhibited_target_is_not_resurrected_to_act(self):
        s=compose(read_model(inhibited='authority'),encounter())
        self.assertIn('authority',s.inhibited)
        self.assertEqual(mediated(s),[])
        self.assertNotIn('IMPOSE',{o['action'] for o in s.candidate_actions})
        self.assertTrue(any(
            c['kind']=='ACQUIRED_PERSONAL_SENSE_MEDIATION'
            and not c['operative_mediation'] and
            not c['target_directly_recruited'] for c in s.currents))

    def test_opposed_relational_and_direct_currents_remain_unresolved(self):
        s=compose(read_model(withhold=True),encounter())
        self.assertEqual(len(mediated(s)),1)
        o=next(o for o in s.candidate_actions if o['action']=='IMPOSE')
        self.assertEqual(o['psychodynamic_status'],'UNRESOLVED_CONTRADICTION')
        self.assertIn('authority',o['opposed_currents']['withhold'])
        self.assertIn('motif:historically_learned_care_authority',
                      o['opposed_currents']['approach'])
        self.assertTrue(any(x['action']=='IMPOSE' for x in s.antagonisms))

    def test_operative_target_must_be_previously_acquired_mean_not_magic(self):
        bad=motif()
        bad['effects'][0]['mediated_action']='FEED'
        with self.assertRaisesRegex(
                InvalidRelationalMotif,
                'MOTIF_MEDIATED_ACTION_NOT_ACQUIRED_BY_TARGET'):
            validate_motif(bad,read_model().forms)
        for changes in ({'polarity':'COMPULSORY'},
                        {'mediated_action':None},
                        {'polarity':None}):
            candidate=motif()
            candidate['effects'][0].update(changes)
            with self.subTest(changes=changes):
                with self.assertRaises(InvalidRelationalMotif):
                    validate_motif(candidate,read_model().forms)

    def test_bad_actor_witness_ref_cannot_create_unbounded_authority(self):
        for badref in ('',False,42,[],{}):
            candidate=motif()
            candidate['witnessed_source_actor_ref']=badref
            with self.subTest(ref=badref):
                with self.assertRaisesRegex(
                        InvalidRelationalMotif,
                        'INVALID_MOTIF_WITNESSED_SOURCE_ACTOR'):
                    validate_motif(candidate,read_model().forms)

    def test_relation_requalification_preserves_prior_historical_meaning(self):
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        actor['relational_motifs']=[motif()]
        original=copy(actor)
        admitted=admit(actor,lived(),'objective:new_counterexample',[{
            'kind':'REORGANIZE_RELATIONAL_MOTIF',
            'motif_id':'historically_learned_care_authority',
            'witnessed_source_actor_ref':'neighbor',
        }])
        self.assertEqual(admitted[0]['status'],
                         'ADMITTED_SOURCEFREE_MOTIF_REORGANIZATION')
        changed=actor['relational_motifs'][0]
        self.assertEqual(changed['witnessed_source_actor_ref'],'neighbor')
        self.assertEqual(changed['motif_history'][-1]['previous']
                         ['witnessed_source_actor_ref'],'pastor')
        self.assertEqual(changed['origin'],original['relational_motifs'][0]['origin'])
        self.assertEqual(mediated(compose(
            read_model(motif_override=changed),encounter())),[])
        self.assertEqual(len(mediated(compose(
            read_model(motif_override=changed),
            encounter(speaker='neighbor')))),1)

    def test_invalid_requalification_rolls_back_entire_actor(self):
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        actor['relational_motifs']=[motif()]
        before=copy(actor)
        with self.assertRaisesRegex(
                InvalidDevelopment,'INVALID_MOTIF_WITNESSED_SOURCE_ACTOR'):
            admit(actor,lived(),'objective:bad_reinterpretation',[{
                'kind':'REORGANIZE_RELATIONAL_MOTIF',
                'motif_id':'historically_learned_care_authority',
                'witnessed_source_actor_ref':'',
            }])
        self.assertEqual(actor,before)

    def test_read_cannot_write_other_psyche_or_world_permission(self):
        c=read_model()
        a=encounter()
        before_c=copy(asdict(c)); before_a=copy(asdict(a))
        s=compose(c,a)
        self.assertEqual(asdict(c),before_c)
        self.assertEqual(asdict(a),before_a)
        self.assertFalse(any(x['action']=='FEED' for x in s.candidate_actions))
        self.assertFalse(any(
            x.get('objective_consent') is True or x.get('institutional_right') is True
            for x in s.currents if isinstance(x,dict)))


if __name__=='__main__':
    unittest.main()
