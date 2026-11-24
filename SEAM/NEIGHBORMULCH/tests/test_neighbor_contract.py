"""SOURCEFREE CONTRACT-SPY COURT, NOT full R21/P6 integration execution.

The spy matches the published ResearchLedger.commit signature and world.add_cue
inputs so encounter ownership/permission regressions are executable without an
unavailable exact-source checkout. It cannot establish native producer parity.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':'),
                    ensure_ascii=False).encode()).hexdigest()


def stable_id(prefix, data):
    return prefix+'_'+digest(data)[:16]


fake_pkg = types.ModuleType('um_sorok_organism')
fake_pkg.__path__ = []
fake_types = types.ModuleType('um_sorok_organism.types')
fake_types.digest, fake_types.stable_id = digest, stable_id
fake_types.GRADE = 'SOURCEFREE_RESEARCH_PROVISIONAL'
fake_world = types.ModuleType('um_sorok_organism.world')
fake_objects = types.ModuleType('um_sorok_organism.material_objects')
# Contract spy only. R9's separate real-world court exercises the actual owner.
fake_objects.material_objects_present = lambda world, location: [
    row for row in world.get('material_objects', {}).values()
    if type(row) is dict and row.get('location') == location
    and row.get('visible') is True and type(row.get('id')) is str]


def add_cue(world, kind, tags, location='all', modality='visual',
            description='', source_actor=None, private_to=None, lasting_ticks=0):
    if modality not in ('visual', 'auditory', 'tactile', 'olfactory'):
        raise ValueError('INVALID_CUE_MODALITY')
    item={'id': stable_id('cue', {'clock': world['clock'],
            'i': len(world['cues'])}), 'clock': world['clock'],
          'last_access_clock': world['clock'] + lasting_ticks,
          'kind': kind, 'tags': tags, 'location': location,
          'modality': modality, 'description': description,
          'source_actor': source_actor, 'private_to': private_to}
    world['cues'].append(item)
    return item


fake_world.add_cue = add_cue
_modules = {'um_sorok_organism': fake_pkg,
    'um_sorok_organism.types': fake_types, 'um_sorok_organism.world': fake_world,
    'um_sorok_organism.material_objects': fake_objects}
_old_modules = {name: sys.modules.get(name) for name in _modules}
try:
    sys.modules.update(_modules)
    path = Path(__file__).resolve().parents[1] / 'neighbor_runtime.py'
    spec = importlib.util.spec_from_file_location('neighbormulch_contract_spy', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
finally:
    # Never poison imports of the actual R21 organism in a combined suite.
    for name, old in _old_modules.items():
        if old is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = old
NeighborEncounter = module.NeighborEncounter
EncounterRefusal = module.EncounterRefusal


class LedgerSpy:
    """Finite in-memory transaction spy, NOT an actual SQLite persistence proof."""
    def __init__(self):
        self._world = {'id':'w1','clock':0,
            'positions': {'worker':'workshop', 'elsewhere':'home'},
            'sites': {'workshop':{}, 'home':{}},
            'cues':[], 'material_objects':{}}
        self._version = 0
        self._actors = {'worker':{'id':'worker', 'location':'workshop',
                                 'history':['existing_work'], 'body':{'language':0.9}},
                        'elsewhere':{'id':'elsewhere','location':'home', 'body':{'language':0.9}}}
        self._events = [{'id':'genesis','kind':'INITIALIZATION',
                          'envelope':{'payload':{}}}]
    def world(self, wid):
        self.assert_world(wid)
        return self._version,copy.deepcopy(self._world)
    def assert_world(self,wid):
        if wid!='w1':raise ValueError('wrong world')
    def actors(self):return copy.deepcopy(self._actors)
    def events(self):return copy.deepcopy(self._events)
    def commit(self,wid,expected_world,world,actors,actor_versions,kind,actor_id,payload):
        self.assert_world(wid)
        if self._version!=expected_world:raise RuntimeError('STALE_WORLD')
        if set(world['positions']) != set(self._actors):
            raise RuntimeError('UNREGISTERED_WORLD_POSITION')
        if actors or actor_versions or actor_id is not None:
            raise RuntimeError('NEIGHBOR_CANNOT_WRITE_ACTOR')
        self._world=copy.deepcopy(world)
        self._version+=1
        eid='evt_'+str(self._version)
        self._events.append({'id':eid,'kind':kind,
            'envelope':{'payload':copy.deepcopy(payload)}})
        return {'id':eid}


class RuntimeSpy:
    def __init__(self):
        self.world_id='w1';self.ledger=LedgerSpy();self.calls=[]
    def step(self,actor_id):
        self.calls.append(('step',actor_id))
        return {'receipt': 'actor_step_'+str(len(self.calls)),
                'public_tip': 'The worker continues at the bench.'}


class MIISpy:
    def default_profile(self,scope):
        return {'scope':scope,'exposures':[],'presentation_seq':0,'mode':'NEUTRAL',
                'history':[],'learning_enabled':False}
    def select_detail(self,objects,profile,*,command=None,target=None,offered=None):
        return (target,'EXPLICIT_USER_TARGET') if target in offered else (None,'NONE')
    # Only a contract spy. Real tests exercise protected P6/MII methods.
    def glance_available(self,house,user,target=None):
        p=house['presentation_conditions']
        return (p['grade']=='SOURCEFREE_FIXTURE'
                and p['observer']==user and p['light']=='lit'
                and p['sightline'] in ('partial','unobstructed'))
    def close_available(self,house,user,target=None):
        p=house['presentation_conditions']
        return (self.glance_available(house,user,target)
                and p['sightline']=='unobstructed'
                and p['legibility']=='readable')
    def candidate_details(self,house,room,objects,user):
        return {key:text for key,text in objects.items()
                if house['objects'].get(key,{}).get('room')==room
                and self.glance_available(house,user,key)}
    def update_attention(self,profile,**kw):return False
    def surface(self,**kw):return {'schema':'SOROK_MII_SURFACE@1', **kw}
    def record_exposure(self,profile,**kw):
        profile['exposures'].append(copy.deepcopy(kw))


SOURCE = {'grade':'SOURCEFREE_TEST_ONLY',
'user_conditions': {'workshop': {'light':'lit','sightline':'unobstructed',
                                'hearing':True,'sound_path':'audible'},
                    'home': {'light':'lit','sightline':'unobstructed',
                             'hearing':True,'sound_path':'audible'}},
'actor_conditions':{
    'worker': {'facing':'away','hearing':True,'visual':True,
               'light':'lit','sightline':'unobstructed','sound_path':'audible'},
    'elsewhere': {'facing':'entrance','hearing':True,'visual':True,
               'light':'lit','sightline':'unobstructed','sound_path':'audible'},
}}


class OneWorldContract(unittest.TestCase):
    def setUp(self):
        self.runtime=RuntimeSpy();self.neighbor=NeighborEncounter(self.runtime,'visitor',mii_module=MIISpy())
        self.neighbor.install_sourcefree_conditions(copy.deepcopy(SOURCE),request_id='geometry')
    def test_user_is_not_a_fake_psychological_actor(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        _,w=self.runtime.ledger.world('w1')
        self.assertNotIn('visitor',w['positions'])
        self.assertEqual(set(w['positions']),set(self.runtime.ledger.actors()))
        self.assertEqual(w['neighbor_users']['visitor']['location'],'workshop')
    def test_single_committed_user_move_and_idempotent_replay(self):
        a=self.neighbor.contribute('come','MOVE',destination='workshop')
        count=len(self.runtime.ledger.events())
        b=self.neighbor.contribute('come','MOVE',destination='workshop')
        self.assertEqual(len(self.runtime.ledger.events()),count)
        self.assertEqual(a['receipt'],b['receipt'])
        self.assertEqual(a['event_ref'],b['event_ref'])
        with self.assertRaisesRegex(EncounterRefusal,'REQUEST_REPLAY_CHANGED_PAYLOAD'):
            self.neighbor.contribute('come','MOVE',destination='home')
    def test_footsteps_behind_heard_but_not_seen(self):
        out=self.neighbor.contribute('come','MOVE',destination='workshop')
        self.assertEqual([x['modality'] for x in out['potential_actor_evidence']],['auditory'])
        _,w=self.runtime.ledger.world('w1')
        self.assertEqual(w['cues'][0]['kind'],'visitor_footsteps')
        self.assertEqual(w['cues'][0]['private_to'],'worker')
        self.assertNotIn('visitor',self.runtime.ledger.actors())
    def test_reception_needs_prior_source_not_scene_prose(self):
        r=RuntimeSpy();n=NeighborEncounter(r,'u')
        with self.assertRaisesRegex(EncounterRefusal,'NO_QUALIFIED_SENSORY_SOURCE'):
            n.contribute('start','MOVE',destination='workshop')
        _,w=r.ledger.world('w1')
        self.assertEqual(w['clock'],0)
        self.assertEqual(w['cues'],[])
    def test_user_speech_exact_not_credited_as_actor_motive(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        out=self.neighbor.contribute('say','SAY',text='I disagree with your decision.')
        _,w=self.runtime.ledger.world('w1')
        self.assertEqual(w['neighbor_user_events'][-1]['authored_text'],
                         'I disagree with your decision.')
        self.assertEqual(out['actor_uptake'],'NOT_ESTABLISHED')
        self.assertEqual(w['cues'][-1]['description'],'I disagree with your decision.')
        self.assertNotIn('motives',w['neighbor_user_events'][-1])
    def test_private_gaze_changes_exposure_not_world(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        p=self.neighbor.new_private_profile()
        _,before=self.runtime.ledger.world('w1');events=len(self.runtime.ledger.events())
        v=self.neighbor.private_surface(p,command='look')
        _,after=self.runtime.ledger.world('w1')
        self.assertEqual(before,after)
        self.assertEqual(len(self.runtime.ledger.events()),events)
        self.assertEqual(v['schema'],'SOROK_MII_SURFACE@1')
        self.assertEqual(len(p['exposures']),1)
        self.assertNotIn('public_tip',str(v))
    def test_actor_choice_is_not_user_authored(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        self.neighbor.independent_actor_beat('worker')
        self.assertEqual(self.runtime.calls,[('step','worker')])
        p=self.neighbor.new_private_profile();view=self.neighbor.private_surface(p)
        # A spy.step that returns a prose tip but never commits a real
        # ACTOR_LIFE_TRANSITION must NOT certify it as publicly observed.
        # The actual CO positive path is exercised in the joined R7 court.
        self.assertNotIn('The worker continues',str(view['narration']))
    def test_blocked_move_is_world_history_not_teleport(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        a=self.neighbor.contribute('blocked','MOVE',destination='hall')
        self.assertEqual(a['status'],'BLOCKED')
        _,w=self.runtime.ledger.world('w1')
        self.assertEqual(w['neighbor_users']['visitor']['location'],'workshop')
        self.assertEqual(w['neighbor_user_events'][-1]['perceptual_candidates'],[])
    def test_false_actor_and_false_sensory_source_refused(self):
        with self.assertRaisesRegex(EncounterRefusal,'USER_CANNOT_IMPERSONATE_ACTOR'):
            NeighborEncounter(self.runtime,'worker')
        with self.assertRaisesRegex(EncounterRefusal,'SENSORY_SOURCE_ALREADY_BOUND'):
            x=copy.deepcopy(SOURCE);x['actor_conditions']['worker']['facing']='entrance'
            self.neighbor.install_sourcefree_conditions(x,request_id='change_geometry')
    def test_leave_and_silence_are_not_autohelp(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        wait=self.neighbor.contribute('quiet','WAIT')
        exit=self.neighbor.contribute('bye','LEAVE')
        self.assertEqual((wait['status'],exit['status']),('PERFORMED','PERFORMED'))
        _,w=self.runtime.ledger.world('w1')
        self.assertFalse(w['neighbor_users']['visitor']['present'])
        self.assertEqual(self.runtime.calls,[])
        self.assertEqual(w['neighbor_user_events'][-2]['operation'],'WAIT')
    def test_co_presence_does_not_mint_visibility_or_privileged_tip(self):
        r=RuntimeSpy();source=copy.deepcopy(SOURCE)
        source['user_conditions']['workshop'].update(
            light='dark', sightline='blocked', hearing=False, sound_path='blocked')
        n=NeighborEncounter(r,'visitor',mii_module=MIISpy())
        n.install_sourcefree_conditions(source,request_id='dark')
        n.contribute('come','MOVE',destination='workshop')
        n.independent_actor_beat('worker')
        view=n.private_surface(n.new_private_profile())
        self.assertNotIn('CO_PRESENT_ACTOR',str(view))
        self.assertNotIn('PUBLIC_TIP',str(view))
        self.assertEqual(view['available'],{})

    def test_unqualified_user_view_cannot_become_omniscient(self):
        r=RuntimeSpy();n=NeighborEncounter(r,'visitor',mii_module=MIISpy())
        invalid=copy.deepcopy(SOURCE)
        invalid.pop('user_conditions')
        with self.assertRaisesRegex(EncounterRefusal,'MISSING_USER_SENSORY_CONDITIONS'):
            n.install_sourcefree_conditions(invalid,request_id='wrong')
        self.assertEqual(r.ledger.world('w1')[1]['clock'],0)

    def test_transient_sound_does_not_become_persistent_world_noise(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        _,world=self.runtime.ledger.world('w1')
        cue=world['cues'][-1]
        self.assertEqual(cue['clock'],world['clock'])
        self.assertEqual(cue['last_access_clock'],world['clock'])

    def test_audible_speech_is_not_infant_lexical_understanding(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        self.runtime.ledger._actors['worker']['body']['language']=0.0
        out=self.neighbor.contribute('said','SAY',text='You are late again.')
        self.assertEqual(out['actor_uptake'],'NOT_ESTABLISHED')
        _,world=self.runtime.ledger.world('w1')
        self.assertEqual(world['neighbor_user_events'][-1]['authored_text'],
                         'You are late again.')
        self.assertEqual(world['cues'][-1]['description'],'Speech sounds nearby.')
        self.assertNotIn('You are late again.',str(world['cues'][-1]))

    def test_unqualified_words_cannot_author_outcome(self):
        with self.assertRaisesRegex(EncounterRefusal,'INVALID_USER_SPEECH'):
            self.neighbor.contribute('say','SAY',text='')
        with self.assertRaisesRegex(EncounterRefusal,'UNKNOWN_USER_OPERATION'):
            self.neighbor.contribute('trust','MAKE_ACTOR_TRUST_ME')

if __name__ == '__main__':unittest.main()
