"""REMONT R14 P012: relationally recruited forms must enter the bounded link court."""
import unittest
from um_sorok_organism.types import adult, blank_world, copy
from um_sorok_organism.constitution import compose, materialize, actor_access
from um_sorok_organism.world import add_cue


def scenario(links=(), effects=(), second_effects=(), scoped_c=False):
    actor=adult('alex','Alex')
    specs={'a':('ping',[]), 'b':('ping',[]), 'c':('elsewhere',['SING']),
           'd':('unseen', ['PRACTICE']), 'e':('never',['SPEAK'])}
    for fid,(cue,ops) in specs.items():
        actor['forms'][fid]={'id':fid,'actor':'alex','kind':'PRACTICE',
            'cues':[cue],'enables':ops,'origin':['distinct_lived_event_'+fid],
            'scope':({'locations':['workshop']} if scoped_c and fid=='c' else {}),
            'lifecycle':'ACTIVE','strength':.6,'body_min':0}
    actor['links']=[{'source':a,'target':b,'relation':r,'contexts':[]} for a,b,r in links]
    actor['relational_motifs']=[{
        'id':'first','source_forms':['a','b'],'effects':list(effects),
        'cue_terms':['ping'],'locations':['home'],'status':'ACTIVE',
        'origin':['some_historical_personal_episode']}]
    if second_effects:
        actor['relational_motifs'].append({
            'id':'second','source_forms':['a','c'],'effects':list(second_effects),
            'cue_terms':['ping'],'locations':['home'],'status':'ACTIVE',
            'origin':['subsequent_historical_relation']})
    world=blank_world();world['positions']={'alex':'home'}
    add_cue(world,'bell',['ping'],location='home')
    return actor,world


def view(actor,world):
    return compose(materialize(actor,world),actor_access(actor,world))


class RelationalLinkTransitiveP012(unittest.TestCase):
    def test_motif_recruited_form_recruits_its_separate_link_descendant(self):
        a,w=scenario(links=[('c','d','RECRUITS')],effects=[{'kind':'RECRUIT_FORM','target_form':'c'}])
        s=view(a,w); ids={f['id'] for f in s.recruited}
        self.assertIn('c',ids)
        self.assertIn('d',ids)
        self.assertIn('PRACTICE',{x['action'] for x in s.candidate_actions})

    def test_two_distinct_motifs_cascade_to_another_acquired_form(self):
        a,w=scenario(effects=[{'kind':'RECRUIT_FORM','target_form':'c'}],
                     second_effects=[{'kind':'RECRUIT_FORM','target_form':'e'}])
        s=view(a,w)
        self.assertIn('e',{f['id'] for f in s.recruited})
        self.assertIn('SPEAK',{x['action'] for x in s.candidate_actions})

    def test_motif_recruited_inhibitor_vetoes_directly_seeded_form(self):
        a,w=scenario(links=[('c','b','INHIBITS')],effects=[{'kind':'RECRUIT_FORM','target_form':'c'}])
        s=view(a,w);ids={f['id'] for f in s.recruited}
        self.assertIn('c',ids)
        self.assertNotIn('b',ids)
        self.assertIn('b',s.inhibited)

    def test_motif_recruited_link_descendant_cannot_break_scope(self):
        a,w=scenario(links=[('c','d','RECRUITS')],effects=[{'kind':'RECRUIT_FORM','target_form':'c'}],scoped_c=True)
        s=view(a,w);ids={f['id'] for f in s.recruited}
        self.assertNotIn('c',ids)
        self.assertNotIn('d',ids)
        self.assertNotIn('SING',{x['action'] for x in s.candidate_actions})

    def test_cyclic_relational_and_positive_links_terminate_without_duplicates(self):
        a,w=scenario(links=[('c','d','RECRUITS'),('d','c','SUPPORTS')],effects=[{'kind':'RECRUIT_FORM','target_form':'c'}])
        s=view(a,w); ids=[f['id'] for f in s.recruited]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertIn('d',ids)
        self.assertEqual(a['forms']['d']['cues'],['unseen'])

if __name__=='__main__': unittest.main()
