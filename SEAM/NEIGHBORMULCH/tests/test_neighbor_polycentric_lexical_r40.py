"""R40 one actual utterance -> optional distinct project significance -> cold action.
Controlled actor policies, no universal psychology of words or trust.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_lexical_occurrence_r39 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world,canonical
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.world import register_recursive_encounter_paths
from neighbor_runtime import NeighborEncounter
import mii

WORDS='I finished the work.'
MEANINGS={'first':'Perhaps I can stop for a while without leaving all the work undone.',
          'second':'If others are done, I still need my own wages.'}

class PolycentricLexicalR40(unittest.TestCase):
    def course(self,mode='admit'):
        tmp=tempfile.TemporaryDirectory(prefix='lexical_r40_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'life.sqlite')
        state={'phase':'prior','offers':{},'packets':[]}
        listeners=('first','second','null','blocked')
        def cb(task,p):
            state['packets'].append((task,deepcopy(p)))
            if task=='expression':
                return {'task':task,'speech':WORDS if p.get('expression_phase')==
                        'LEXICAL_REALIZATION_BEFORE_EXPERIENCE' else None,
                        'surface':'Ordinary activity.'}
            aid=p['actor']['id']
            if task=='actor_attempt':
                if state['phase']=='prior':
                    return {'task':task,'action':'WORK','project_id':'livelihood'}
                if state['phase']=='utter':
                    return {'task':task,'action':'SPEAK','project_id':'talk',
                            'speech_intent':'Say that the work is finished.'}
                # One identical selection rule for every listener and control,
                # reading ONLY the existing operative project courses, not
                # actor identity, test arm, utterance, or saved interpretation.
                courses=[(v['priority'],o['action'],v['project_id'])
                         for o in p['options'] for v in o.get('project_courses',[])]
                _,operation,project=max(courses)
                return {'task':task,'action':operation,'project_id':project}
            if task=='development':
                offers=p.get('historically_possible_lexical_project_revaluations',[])
                if state['phase']!='utter':return {'task':task,'candidates':[]}
                state['offers'][aid]=deepcopy(offers)
                if aid not in ('first','second') or mode=='null':
                    return {'task':task,'candidates':[]}
                self.assertEqual(len(offers),1)
                q=offers[0];basis=deepcopy(q['lexical_revaluation_basis'])
                if mode=='forge' and aid=='second':
                    # First actor's real receipt is not the second's history.
                    basis=deepcopy(state['offers']['first'][0]['lexical_revaluation_basis'])
                proposal={'kind':'REORGANIZE_PROJECT','project_id':q['project_id'],
                          'lexical_revaluation_basis':basis,
                          'priority':.1 if aid=='first' else .9,
                          'personal_significance':MEANINGS[aid]}
                return {'task':task,'candidates':[proposal]}
            raise AssertionError(task)
        sem=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(db,semantic=sem);self.addCleanup(rt.close)
        w=blank_world()
        speaker=adult('speaker','Speaker','workshop')
        speaker['projects']=[{'id':'talk','object':'speak','means':['SPEAK'],'priority':.6,'status':'active'}]
        people=[speaker]
        for aid in listeners:
            a=adult(aid,aid,'workshop')
            a['projects']=[{'id':'livelihood','object':'maintain livelihood','means':['WORK'],
                            'priority':.65,'status':'active'},
                           {'id':'rest','object':'recover strength','means':['REST'],
                            'priority':.4,'status':'active'}]
            people.append(a)
        register_recursive_encounter_paths(w,{a['id']:a for a in people},{
            'grade':'SOURCEFREE_TEST_ONLY','source_ref':'fictional:polycentric',
            'paths':[{'observer':aid,'source_actor':'speaker','location':'workshop',
                      'from_clock':0,'through_clock':100,'hearing':aid!='blocked',
                      'sound_path':'audible' if aid!='blocked' else 'blocked',
                      'visual':aid=='second','light':'lit','sightline':'unobstructed',
                      'facing':'source' if aid=='second' else 'away'} for aid in listeners]})
        rt.ledger.initialize(w,people)
        # Different actual antecedent life: first has two lived work attempts,
        # second/null/blocked one. No hypothetical biography is installed.
        for aid in ('first','first','second','null','blocked'):
            self.assertEqual(rt.step(aid)['status'],'PERFORMED')
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'workshop':{'light':'lit','sightline':'unobstructed',
                'hearing':True,'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{a['id']:{'facing':'entrance','visual':True,'light':'lit',
                'sightline':'unobstructed','hearing':True,'sound_path':'audible'} for a in people}},
            request_id='geometry')
        n.contribute('arrive','MOVE',destination='workshop')
        before=deepcopy(rt.ledger.world());actors=deepcopy(rt.ledger.actors())
        events=deepcopy(rt.ledger.events());state['phase']='utter'
        count=len(state['packets'])
        if mode=='forge':
            with self.assertRaisesRegex(ValueError,'LEXICAL_PROJECT_REVALUATION_UNQUALIFIED'):
                n.independent_actor_beat('speaker')
            self.assertEqual(rt.ledger.world(),before)
            self.assertEqual(rt.ledger.actors(),actors);self.assertEqual(rt.ledger.events(),events)
            self.assertTrue(rt.verify()['valid'])
            return
        speech=n.independent_actor_beat('speaker');self.assertEqual(speech['status'],'PERFORMED')
        self.assertEqual(sum(t=='expression' for t,p in state['packets'][count:]),1)
        w=rt.ledger.world()[1]
        self.assertEqual(w['material_claims'],before[1]['material_claims'])
        self.assertEqual(w['cues'][-1]['spoken_text'],WORDS)
        for aid in ('first','second','null'):
            self.assertEqual(len(state['offers'][aid]),1)
        self.assertFalse(state['offers'].get('blocked',[]))
        self.assertFalse(state['offers'].get('speaker',[]))
        first=state['offers']['first'][0]['lexical_revaluation_basis']
        second=state['offers']['second'][0]['lexical_revaluation_basis']
        self.assertEqual(first['received_cue_ref'],second['received_cue_ref'])
        self.assertEqual(first['received_words_hash'],second['received_words_hash'])
        self.assertNotEqual(first['origin_event_ref'],second['origin_event_ref'])
        self.assertIsNone(first['visually_eligible_source_ref'])
        self.assertEqual(second['visually_eligible_source_ref'],'speaker')
        for aid in listeners:
            project=rt.ledger.actor(aid)[1]['projects'][0]
            self.assertEqual(project['priority'],
                {'first':.1,'second':.9}.get(aid,.65) if mode=='admit' else .65)
            self.assertEqual(project['means'],['WORK'])
            self.assertEqual(project['operational_history'],actors[aid]['projects'][0]['operational_history'])
            histories=[v['lexical_revaluation'] for v in project.get('history',[]) if v.get('lexical_revaluation')]
            if aid in MEANINGS and mode=='admit':
                self.assertEqual(len(histories),1)
                self.assertEqual(histories[0]['personal_significance'],MEANINGS[aid])
            else:self.assertEqual(histories,[])
        view=n.private_surface(n.new_private_profile())
        self.assertIn(WORDS,canonical(view))
        for meaning in MEANINGS.values():self.assertNotIn(meaning,canonical(view))
        rt.close();cold=ConstitutiveRuntime(db,semantic=sem);self.addCleanup(cold.close)
        nn=NeighborEncounter(cold,'visitor',mii_module=mii)
        state['phase']='later';result={}
        for aid in listeners:
            cash=cold.ledger.world()[1]['accounts'][aid]
            out=nn.independent_actor_beat(aid)
            self.assertEqual(out['status'],'PERFORMED')
            result[aid]=(out['attempt'],cold.ledger.world()[1]['accounts'][aid]-cash)
        self.assertTrue(cold.verify()['valid'])
        return result

    def test_same_words_different_admission_and_independent_cold_material_course(self):
        actual=self.course('admit');null=self.course('null')
        self.assertEqual(actual['first'],('REST',0))
        self.assertEqual(null['first'],('WORK',.25))
        for aid in ('second','null','blocked'):
            self.assertEqual(actual[aid],('WORK',.25))
            self.assertEqual(actual[aid],null[aid])

    def test_foreign_receipt_aborts_whole_transition(self):
        self.course('forge')

if __name__=='__main__':unittest.main()
