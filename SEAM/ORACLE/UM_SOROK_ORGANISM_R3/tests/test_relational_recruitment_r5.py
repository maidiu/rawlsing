"""R5 relational recruitment: native unittest, graded sourcefree negative court.

These tests are *authored* by the construction agent. A clean exact-HEAD
runner and full normal/-O execution receipt are required before claiming PASS.
"""
import unittest

from um_sorok_organism.types import Constitution, AccessibleEncounter, adult, copy
from um_sorok_organism.constitution import compose
from um_sorok_organism.relational_metabolism import (
    validate_motif, InvalidRelationalMotif,
)


def acquired(fid, action, cues, scope=None, body_min=.1, withholding=False):
    form={
        'id':fid,'actor':'mother','kind':'RELATIONAL_INVESTMENT',
        'origin':['fictional_init:mother'],'cues':list(cues),
        'enables':[action],'scope':scope or {},'lifecycle':'ACTIVE',
        'strength':.6,'body_min':body_min,'access':'tacit',
    }
    if withholding:
        form['tendencies']=[{
            'action':'IMPOSE','polarity':'WITHHOLD','cue_terms':['rebuke'],
        }]
    return form


def case(*, recruiting=True, suppressing=True, target_scope=None,
         target_body_min=.1, context=('rebuke',)):
    forms={
        'care':acquired('care','CARE',['rebuke']),
        'authority':acquired('authority','IMPOSE',['rebuke']),
        'distant':acquired('distant','SPEAK',['earlier_harm'],
                           scope=target_scope,body_min=target_body_min,
                           withholding=True),
    }
    links=[{
        'source':'authority','target':'care','relation':'INHIBITS',
        'contexts':['home'],'origin':['earlier_public_discipline'],
    }] if suppressing else []
    effects=[
        {'kind':'RELATION_MEDIATION','source':'care','target':'authority',
         'relation':'SUBORDINATES'},
        {'kind':'ACTION_CURRENT','action':'IMPOSE','polarity':'APPROACH'},
    ]
    if recruiting:
        effects.append({'kind':'RECRUIT_FORM','target_form':'distant'})
    motif={
        'id':'care_became_discipline','source_forms':['care','authority'],
        'cue_terms':['rebuke'],'locations':['home'],'status':'ACTIVE',
        'origin':['fictional_init:mother'],'effects':effects,
    }
    parent=adult('mother','Mother')
    constitution=Constitution(
        actor='mother',clock=1,body=parent['body'],
        forms=forms,links=links,projects=[],activity_links=[],
        memories=[],traces=[],other_models={},self_model={},
        relations=[],unknowns=[],relational_motifs=[motif],
    )
    encounter=AccessibleEncounter(
        'mother',1,'home',[{
            'id':'objective:spoken_rebuke','kind':'speech',
            'tags':list(context),'source_actor':'pastor','location':'home',
        }],[],['objective:spoken_rebuke'],
    )
    return constitution,encounter


class RelationalRecruitmentR5(unittest.TestCase):
    def test_inhibited_care_can_recruit_distant_defense_without_direct_care(self):
        constitution,access=case()
        original=copy(constitution.forms)
        current=compose(constitution,access)
        visible={x['id'] for x in current.recruited}
        actions={x['action'] for x in current.candidate_actions}
        self.assertIn('care',current.inhibited)
        self.assertNotIn('care',visible)
        self.assertIn('authority',visible)
        self.assertIn('distant',visible)
        self.assertIn('SPEAK',actions)
        self.assertNotIn('CARE',actions)
        self.assertTrue(any(
            x['kind']=='HISTORICALLY_RECRUITED_VIA_MOTIF'
            and x['ref']=='distant'
            and x['had_inhibited_source']
            for x in current.currents
        ))
        imposed=next(a for a in current.candidate_actions
                     if a['action']=='IMPOSE')
        self.assertEqual(imposed['psychodynamic_status'],
                         'UNRESOLVED_CONTRADICTION')
        self.assertIn('distant',imposed['opposed_currents']['withhold'])
        self.assertIn('motif:care_became_discipline',
                      imposed['opposed_currents']['approach'])
        self.assertEqual(constitution.forms,original)

    def test_without_acquired_recruitment_edge_defense_stays_unrecruited(self):
        constitution,access=case(recruiting=False)
        current=compose(constitution,access)
        self.assertNotIn('distant',{x['id'] for x in current.recruited})
        self.assertFalse(any(x['kind']=='HISTORICALLY_RECRUITED_VIA_MOTIF'
                             for x in current.currents))

    def test_unqualified_location_is_not_bypassed_by_motif(self):
        constitution,access=case(target_scope={'locations':['workshop']})
        current=compose(constitution,access)
        self.assertNotIn('distant',{x['id'] for x in current.recruited})

    def test_body_limit_is_not_bypassed_by_psychological_pressure(self):
        constitution,access=case(target_body_min=.99)
        current=compose(constitution,access)
        self.assertNotIn('distant',{x['id'] for x in current.recruited})

    def test_ritual_genre_not_magic_without_actually_recruited_sources(self):
        constitution,access=case(context=('ordinary_weather',))
        current=compose(constitution,access)
        self.assertNotIn('distant',{x['id'] for x in current.recruited})
        self.assertFalse(any(x['kind']=='ACQUIRED_RELATIONAL_CONFIGURATION'
                             for x in current.currents))

    def test_unacquired_target_cannot_be_minted_by_a_motif(self):
        constitution,_=case()
        bad=copy(constitution.relational_motifs[0])
        bad['effects'].append({
            'kind':'RECRUIT_FORM','target_form':'inferred_hidden_trauma',
        })
        with self.assertRaisesRegex(
            InvalidRelationalMotif,'MOTIF_RECRUITMENT_TARGET_UNQUALIFIED'
        ):
            validate_motif(bad,constitution.forms)


if __name__=='__main__':
    unittest.main()
