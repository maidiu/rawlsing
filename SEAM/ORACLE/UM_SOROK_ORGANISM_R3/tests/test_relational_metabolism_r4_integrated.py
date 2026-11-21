"""R4 behavioral court, integrated into R9 REMONT owner with explicit sourcefree grade.
Adapted from GitHub R4 test contract at 739da5a (11 checks).
"""
from dataclasses import asdict
from pathlib import Path
import tempfile, unittest
from um_sorok_organism.types import AccessibleEncounter, Constitution, adult, copy
from um_sorok_organism.constitution import compose
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.relational_metabolism import validate_motif, link_ref, InvalidRelationalMotif
from um_sorok_organism.parents import construct_parent
from um_sorok_organism.semantics import ValidatingSemanticService
from um_sorok_organism.runtime import ConstitutiveRuntime

def form(fid,action,tags,tendency=None):
    return {'id':fid,'actor':'mother','kind':'RELATIONAL_INVESTMENT',
      'origin':['fictional_init:mother'],'cues':list(tags),'enables':[action],
      'scope':{},'lifecycle':'ACTIVE','strength':.65,'body_min':.1,'access':'tacit',
      'tendencies':[tendency] if tendency else []}

def motif():
    return {'id':'moralized-care','source_forms':['care','authority'],
      'cue_terms':['rebuke'],'locations':['home'],'origin':['fictional_init:mother'],
      'status':'ACTIVE','effects':[
        {'kind':'RELATION_MEDIATION','source':'care','target':'authority','relation':'SUBORDINATES'},
        {'kind':'ACTION_CURRENT','action':'IMPOSE','polarity':'APPROACH'}]}

def constitution(suppress=False,withhold=False,motif_present=True):
    forms={'care':form('care','CARE',['community','rebuke']),
      'authority':form('authority','IMPOSE',['community','rebuke'],
          {'action':'IMPOSE','polarity':'WITHHOLD','cue_terms':['rebuke']} if withhold else None)}
    links=[{'source':'authority','target':'care','relation':'INHIBITS',
            'contexts':['home'],'origin':['past-rebuke']}] if suppress else []
    return Constitution('mother',0,adult('mother','Mother')['body'],forms,links,
       [],[],[],[],{}, {},[],[],
       relational_motifs=[motif()] if motif_present else [])

def access(tags=('community','rebuke')):
    return AccessibleEncounter('mother',0,'home',[{'id':'world:cue','kind':'speech',
        'tags':list(tags),'source_actor':'pastor','location':'home'}],[],['world:cue'])

def lived():
    return {'actor':'mother','ref':'lived:mother:event-1','participated':True,
      'perceived_cues':[{'id':'cue:public-rebuke'}], 'status':'OBSERVED','own_action':None}

class RelationalMetabolismR4Integrated(unittest.TestCase):
    def situated(self,**kwargs):return compose(constitution(**kwargs),access())
    def test_moralized_care_relation_and_approach(self):
        x=self.situated()
        self.assertTrue(any(c['kind']=='ACQUIRED_PERSONAL_SENSE_MEDIATION' and c['relation']=='SUBORDINATES' for c in x.currents))
        self.assertTrue(any(c['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT' and c['action']=='IMPOSE' for c in x.currents))
        self.assertEqual(next(o for o in x.candidate_actions if o['action']=='IMPOSE')['psychodynamic_status'],
                         'ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT')
        self.assertIn('moralized-care',x.readset)
    def test_inhibited_care_remains_indirectly_productive(self):
        x=self.situated(suppress=True)
        self.assertIn('care',x.inhibited)
        self.assertNotIn('care',{f['id'] for f in x.recruited})
        self.assertNotIn('CARE',{a['action'] for a in x.candidate_actions})
        self.assertTrue(any(c['kind']=='INDIRECT_INHIBITED_RELATION' and c['target_form_ref']=='care' for c in x.currents))
        self.assertTrue(any(c['kind']=='ACQUIRED_RELATIONAL_CONFIGURATION' and 'care' in c['inhibited_source_refs'] for c in x.currents))
        self.assertTrue(any(c['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT' and c['has_inhibited_source'] for c in x.currents))
    def test_opposed_motif_and_withholding_remain_unresolved(self):
        x=self.situated(withhold=True)
        a=next(a for a in x.candidate_actions if a['action']=='IMPOSE')
        self.assertEqual(a['psychodynamic_status'],'UNRESOLVED_CONTRADICTION')
        self.assertIn('authority',a['opposed_currents']['withhold'])
        self.assertIn('motif:moralized-care',a['opposed_currents']['approach'])
    def test_genre_without_specific_cue_is_not_magic(self):
        x=compose(constitution(),access(('community',)))
        self.assertFalse(any(c['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT' for c in x.currents))
        self.assertIn('IMPOSE',{a['action'] for a in x.candidate_actions})
    def test_motif_read_is_pure(self):
        c=constitution();original=copy(asdict(c));compose(c,access());self.assertEqual(asdict(c),original)
    def test_actor_can_acquire_new_motif_after_real_encounter(self):
        a=adult('mother','Mother');a['forms']={'care':form('care','CARE',['rebuke']),
          'authority':form('authority','IMPOSE',['rebuke'])}
        row=admit(a,lived(),'objective:1',[{'kind':'ACQUIRE_RELATIONAL_MOTIF',
          'motif':{'source_forms':['care','authority'],'cue_terms':['rebuke'],
            'locations':['home'],'effects':[{'kind':'ACTION_CURRENT','action':'IMPOSE','polarity':'APPROACH'}]}}])
        self.assertEqual(row[0]['status'],'ADMITTED_SOURCEFREE_RELATIONAL_FORMATION')
        self.assertEqual(a['relational_motifs'][0]['origin'],['objective:1'])
        c=constitution(motif_present=False);c.relational_motifs=copy(a['relational_motifs'])
        self.assertTrue(any(y['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT' for y in compose(c,access()).currents))
    def test_relation_revalue_preserves_prior_meaning_and_identity(self):
        a=adult('mother','Mother');a['forms']={'care':form('care','CARE',['rebuke']),
          'authority':form('authority','IMPOSE',['rebuke'])}
        a['links']=[{'source':'care','target':'authority','relation':'SUPPORTS',
          'contexts':['home'],'origin':['former-coactivity']}]
        ref=link_ref(a['links'][0]);r=admit(a,lived(),'objective:disillusionment',[
          {'kind':'REVALUE_RELATION','relation_id':ref,'new_relation':'CONFLICTS_WITH'}])
        self.assertEqual(r[0]['status'],'ADMITTED_SOURCEFREE_RELATIONAL_REVALUATION')
        self.assertEqual(a['links'][0]['id'],ref)
        self.assertEqual(a['links'][0]['relational_history'][0]['relation'],'SUPPORTS')
    def test_motif_reorganization_preserves_old_configuration(self):
        a=adult('mother','Mother');a['forms']={'care':form('care','CARE',['rebuke']),
          'authority':form('authority','IMPOSE',['rebuke'])};a['relational_motifs']=[motif()]
        admit(a,lived(),'objective:changed',[{'kind':'REORGANIZE_RELATIONAL_MOTIF',
          'motif_id':'moralized-care','status':'DORMANT','cue_terms':['public-exclusion']}])
        self.assertEqual(a['relational_motifs'][0]['motif_history'][0]['previous']['cue_terms'],['rebuke'])
        self.assertEqual(a['relational_motifs'][0]['motif_history'][0]['experience_ref'],lived()['ref'])
    def test_invalid_second_effect_rolls_back_first(self):
        a=adult('mother','Mother');a['forms']={'care':form('care','CARE',['rebuke']),
          'authority':form('authority','IMPOSE',['rebuke'])};old=copy(a)
        with self.assertRaises(InvalidDevelopment):admit(a,lived(),'objective:1',[
          {'kind':'ACQUIRE_RELATIONAL_MOTIF','motif':{'source_forms':['care','authority'],
             'effects':[{'kind':'ACTION_CURRENT','action':'IMPOSE','polarity':'APPROACH'}]}},
          {'kind':'REVALUE_RELATION','relation_id':'forged','new_relation':'SUPPORTS'}])
        self.assertEqual(a,old)
        with self.assertRaises(InvalidRelationalMotif):validate_motif({'source_forms':['care','unknown'],
          'effects':[{'kind':'ACTION_CURRENT','action':'CARE','polarity':'APPROACH'}]},a['forms'])
    def test_parent_seed_motif_from_fictional_forms_not_survey_answer(self):
        packet={'answers':{'Q':'answer'},'fictional_seed':{'acquired_forms':[
          {'kind':'RELATIONAL_INVESTMENT','cues':['rebuke'],'enables':['CARE']},
          {'kind':'MEDIATOR','cues':['rebuke'],'enables':['IMPOSE']}],
          'relational_motifs':[{'source_indices':[0,1],'cue_terms':['rebuke'],
              'effects':[{'kind':'ACTION_CURRENT','action':'IMPOSE','polarity':'APPROACH'}]}]}}
        a=construct_parent('mother','Mother',packet,ValidatingSemanticService())
        self.assertEqual(len(a['relational_motifs']),1)
        self.assertTrue(a['relational_motifs'][0]['not_respondent_unconscious_truth'])
        self.assertTrue(all(x in a['forms'] for x in a['relational_motifs'][0]['source_forms']))
    def test_private_pre_event_record_not_rendered_to_user(self):
        packet={'answers':{'Q':'answer'},'fictional_seed':{'acquired_forms':[
          {'kind':'RELATIONAL_INVESTMENT','cues':['rebuke'],'enables':['CARE']},
          {'kind':'MEDIATOR','cues':['rebuke'],'enables':['IMPOSE']}],
          'relational_motifs':[{'source_indices':[0,1],'cue_terms':['rebuke'],
             'effects':[{'kind':'ACTION_CURRENT','action':'IMPOSE','polarity':'APPROACH'}]}]}}
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(Path(d)/'person.db')
            try:
                rt.initialize([('mother','Mother',packet)])
                rt.cue(kind='public_rebuke',tags=['rebuke'],location='home')
                self.assertTrue(any(x['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT' for x in rt.situated('mother')['currents']))
                step=rt.step('mother',requested_action='REST')
                self.assertNotIn('private_pre_event_psychodynamics',step)
                self.assertIn('private_pre_event_psychodynamics',str(rt.ledger.events()[-1]['envelope']))
                self.assertTrue(rt.verify()['valid'])
            finally: rt.close()
