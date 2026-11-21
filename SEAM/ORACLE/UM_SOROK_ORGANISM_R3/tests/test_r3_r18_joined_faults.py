"""SORACLE builder-owned R3+REMONT R18 functional convergence court.

Tests explicitly RETEST the bugs found and repaired by REMONT, as applied
to the *newer* SORACLE actor/constitution, plus a new author-local atomicity
issue. These tests are not a claim of actual Python execution.
"""
import copy
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.activity import record_activity_afterlife
from um_sorok_organism.constitution import compose,materialize,actor_access
from um_sorok_organism.storage import ResearchLedger,Conflict
from um_sorok_organism.types import adult,blank_world,stable_id
from um_sorok_organism.development import admit,InvalidDevelopment
from um_sorok_organism.runtime import ConstitutiveRuntime, _bind_actor_trial_particular_object
from um_sorok_organism.semantics import ValidatingSemanticService, CallbackLLMProvider
from um_sorok_organism.world import add_cue


def actor_and_site():
    actor=adult("nadias_father","Father")
    for name,action in (("a","SING"),("b","WORK"),("c","REPAIR")):
        actor["forms"][name]={
            "id":name,"actor":actor["id"],"kind":"PRACTICE",
            "cues":["encounter"],"enables":[action],
            "strength":.65,"body_min":0,"lifecycle":"ACTIVE","scope":{}
        }
    world=blank_world()
    world["positions"]={actor["id"]:"home"}
    add_cue(world,"bell",["encounter"],location="home")
    return actor,world


class JoinedPsychicRecruitmentR15(unittest.TestCase):
    def test_stratified_inhibition_not_conservative_false_negative(self):
        a,w=actor_and_site()
        a["links"]=[
            {"source":"a","target":"b","relation":"INHIBITS","contexts":[]},
            {"source":"b","target":"c","relation":"INHIBITS","contexts":[]},
        ]
        first=compose(materialize(a,w),actor_access(a,w))
        self.assertEqual({form["id"] for form in first.recruited},
                         {"a","c"})
        self.assertNotIn("c",first.inhibited)
        a["links"].reverse()
        second=compose(materialize(a,w),actor_access(a,w))
        self.assertEqual({form["id"] for form in second.recruited},
                         {"a","c"})

    def test_r3_new_suppresses_relation_still_obeys_r15_truth(self):
        a,w=actor_and_site()
        a["links"]=[
            {"source":"a","target":"b","relation":"SUPPRESSES","contexts":[]},
            {"source":"b","target":"c","relation":"SUPPRESSES","contexts":[]},
        ]
        result=compose(materialize(a,w),actor_access(a,w))
        self.assertEqual({form["id"] for form in result.recruited},
                         {"a","c"})
        self.assertIn("b",result.inhibited)
        self.assertNotIn("c",result.inhibited)

    def test_conflicting_cyclic_inhibition_remains_unresolved(self):
        a,w=actor_and_site()
        a["links"]=[
            {"source":"a","target":"b","relation":"INHIBITS","contexts":[]},
            {"source":"b","target":"a","relation":"INHIBITS","contexts":[]},
        ]
        result=compose(materialize(a,w),actor_access(a,w))
        self.assertFalse({"a","b"} & {x["id"] for x in result.recruited})


class JoinedPurposeP004(unittest.TestCase):
    def _actor(self):
        a=adult("parent","Parent")
        a["projects"]=[
            {"id":"care","object":"care for this child",
             "means":["CARE"],"operational_history":[]},
            {"id":"speak","object":"learn to speak together",
             "means":["SPEAK"],"operational_history":[]}
        ]
        return a

    def _purpose(self,ids):
        return {"status":(
            "ACTOR_POLICY_SELECTED_PROJECT_COURSE" if len(ids)==1 else
            "ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES"),
            "project_id":ids[0] if len(ids)==1 else None,
            "project_ids":ids}

    def test_actor_selected_incompatible_project_must_not_silently_disappear(self):
        a=self._actor();before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,
                                    "ACTIVITY_SELECTED_MEANS_CONTRADICTION"):
            record_activity_afterlife(
                a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
                ["project:care"],"evt_wrong",
                purpose_selection=self._purpose(["care"]))
        self.assertEqual(a,before)

    def test_mixed_compatible_and_incompatible_selection_is_atomic(self):
        a=self._actor();before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,
                                    "ACTIVITY_SELECTED_MEANS_CONTRADICTION"):
            record_activity_afterlife(
                a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
                ["project:care","project:speak"],"evt_mixed",
                purpose_selection=self._purpose(["care","speak"]))
        self.assertEqual(a,before)

    def test_missing_actor_selected_project_does_not_disappear(self):
        a=self._actor();before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,
                                    "ACTIVITY_SELECTED_MEANS_CONTRADICTION"):
            record_activity_afterlife(
                a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
                ["project:ghost"],"evt_ghost",
                purpose_selection=self._purpose(["ghost"]))
        self.assertEqual(a,before)

    def test_project_history_collision_is_atomic_in_multi_project_selection(self):
        a=self._actor()
        a["projects"][0]["means"].append("SPEAK")
        a["projects"][1]["operational_history"].append({
            "event":"evt_same","operation":"SPEAK"})
        before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,
                                    "DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT"):
            record_activity_afterlife(
                a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
                ["project:care","project:speak"],"evt_same",
                purpose_selection=self._purpose(["care","speak"]))
        self.assertEqual(a,before)

    def test_provisional_end_trial_is_real_projectless_activity_not_a_motive(self):
        a=self._actor()
        prior=copy.deepcopy(a)
        receipts=record_activity_afterlife(
            a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
            ["operative_speech"],"evt_trial",
            purpose_selection={
                "status":"ACTOR_POLICY_PROVISIONAL_END_TRIAL_NOT_DURABLE_MOTIVE",
                "project_id":None,"project_ids":[],
                "possible_end_ref":"qualified_possible_end_prior"})
        self.assertEqual(receipts,[])
        self.assertEqual(a,prior)
        self.assertEqual(a["activity_history"],prior["activity_history"])

    def test_actual_selected_project_retains_its_practical_object(self):
        a=self._actor()
        record_activity_afterlife(
            a,"SPEAK","PERFORMED","SPEECH_PERFORMED",
            ["project:speak"],"evt_ok",
            purpose_selection=self._purpose(["speak"]))
        self.assertEqual(len(a["projects"][1]["operational_history"]),1)
        self.assertEqual(a["projects"][1]["operational_history"][0][
            "practical_object"],"learn to speak together")
        self.assertEqual(a["projects"][0]["operational_history"],[])


class JoinedSourcePreflightP018(unittest.TestCase):
    def test_corrupt_history_blocks_all_existing_authority_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/"preflight.sqlite3")
            l=ResearchLedger(path)
            try:
                l.initialize(blank_world(),[adult("parent","Parent")],
                             source_seals=[("seed","FICTIONAL",{"person":"A"})])
                self.assertEqual(l.source("seed")["content"],{"person":"A"})
                l.conn.execute(
                    "UPDATE events SET payload='{}' WHERE seq=1")
                with self.assertRaisesRegex(Conflict,
                                            "SOURCE_HISTORY_INVALID"):
                    l.source("seed")
                with self.assertRaisesRegex(Conflict,
                                            "SOURCE_HISTORY_INVALID"):
                    l.seal_source("late","FICTIONAL",{"person":"B"})
                version,w=l.world()
                with self.assertRaisesRegex(Conflict,
                                            "SOURCE_HISTORY_INVALID"):
                    l.commit("w1",version,w,{},{},"OBJECTIVE_CUE",None,
                             {"no":"unsafe_append"})
                self.assertEqual(l.conn.execute(
                    "SELECT count(*) FROM events").fetchone()[0],1)
            finally:
                l.close()



class JoinedTrialIssuerAndCueProvenance(unittest.TestCase):
    """Regressions previously authored on REMONT R11-R13, now in R3."""

    def fixture(self, *, actor_id='mother'):
        a=adult(actor_id,actor_id.title())
        a['possible_ends']=[{
            'id':'old_end','status':'POSSIBLE_NOT_ACQUIRED_MOTIVE',
            'origin_event':'world:prior','experience_ref':'lived:prior',
            'possible_means':['SING'],'possible_object':'possible song',
            'cue_terms':['song'],
        }]
        e={'actor':actor_id,'ref':'lived:now','own_action':'SING',
           'status':'PERFORMED','participated':True,
           'felt_enactment':{'attempted_operation':'SING'},
           'perceived_cues':[]}
        ticket={'actor':actor_id,'as_of_clock':7,
                'possible_end_ref':'old_end','operation':'SING',
                'origin_event':'world:prior',
                'origin_experience_ref':'lived:prior',
                'actor_project_ref':None,'functional_bridge_ref':None}
        ticket['trial_id']=stable_id('end_trial',{
            'actor':actor_id,'clock':7,'possible_end':'old_end',
            'operation':'SING','functional_bridge':None})
        return a,e,ticket

    def test_model_relabels_issued_trial_as_new_durable_project_atomic(self):
        actor,experience,ticket=self.fixture()
        before=copy.deepcopy(actor)
        with self.assertRaisesRegex(
                InvalidDevelopment,'CURRENT_TRIAL_CANNOT_ACQUIRE_DURABLE_PROJECT'):
            admit(actor,experience,'world:now',[
                {'kind':'TRACE','cue_terms':['new_song'],'content':'tentative'},
                {'kind':'ADD_PROJECT','project':{
                    'object':'my permanent song','motive':'now my destiny',
                    'means':['SING'],'priority':1}}],
                issued_trial=ticket)
        self.assertEqual(actor,before)

    def test_valid_r3_issued_trial_auto_records_once_without_project(self):
        actor,experience,ticket=self.fixture()
        records=admit(actor,experience,'world:now',[],issued_trial=ticket)
        self.assertEqual([r['kind'] for r in records],
                         ['RECORD_POSSIBLE_END_TRIAL'])
        self.assertEqual(len(actor['possible_ends'][0]['trial_history']),1)
        self.assertEqual(actor['projects'],[])
        with self.assertRaisesRegex(
                InvalidDevelopment,'POSSIBLE_END_TRIAL_EVENT_ALREADY_CONSUMED'):
            admit(actor,experience,'world:now',[],issued_trial=ticket)
        self.assertEqual(len(actor['possible_ends'][0]['trial_history']),1)

    def test_r3_runtime_inserted_trial_record_not_double_written(self):
        actor,experience,ticket=self.fixture()
        records=admit(actor,experience,'world:now',[
            {'kind':'RECORD_POSSIBLE_END_TRIAL','trial':copy.deepcopy(ticket)}],
            issued_trial=ticket)
        self.assertEqual(len(records),1)
        self.assertEqual(len(actor['possible_ends'][0]['trial_history']),1)

    def test_fake_trial_without_issuer_or_with_bad_ticket_is_rejected(self):
        actor,experience,ticket=self.fixture()
        before=copy.deepcopy(actor)
        with self.assertRaisesRegex(InvalidDevelopment,'UNISSUED_POSSIBLE_END_TRIAL'):
            admit(actor,experience,'world:now',[
                {'kind':'RECORD_POSSIBLE_END_TRIAL','trial':ticket}])
        fake={**ticket,'trial_id':'model_forged_trial'}
        with self.assertRaisesRegex(InvalidDevelopment,'UNISSUED_POSSIBLE_END_TRIAL'):
            admit(actor,experience,'world:now',[],issued_trial=fake)
        self.assertEqual(actor,before)

    def test_nontrial_later_new_project_still_legal(self):
        actor,experience,_=self.fixture()
        result=admit(actor,experience,'world:later',[
            {'kind':'ADD_PROJECT','project':{'object':'new later concern',
                'motive':'unknown provisional','means':['SING'],'priority':.2}}])
        self.assertEqual(result[0]['kind'],'ADD_PROJECT')
        self.assertEqual(len(actor['projects']),1)

    def test_cue_falsey_not_coerced_and_explicit_empty_stays_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            rt=ConstitutiveRuntime(str(Path(directory)/'tags.sqlite3'))
            try:
                rt.initialize()
                count=rt.verify()['events']
                for invalid in (False,'',(),0,{}):
                    with self.assertRaisesRegex(ValueError,'INVALID_CUE_TAGS'):
                        rt.cue('nadia',kind='contact',tags=invalid)
                    self.assertEqual(rt.verify()['events'],count)
                result=rt.cue('nadia',kind='contact',tags=[])
                self.assertEqual(result['cue']['tags'],[])
                self.assertEqual(rt.verify()['events'],count+1)
                default=rt.cue('nadia',kind='contact')
                self.assertEqual(default['cue']['tags'],['contact'])
            finally:
                rt.close()



class JoinedIssuedTrialAndParticularObject(unittest.TestCase):
    def _option(self, ref, grounds, option_id, *, project=None, binding=None):
        return {
            'option_id': option_id,
            'operation': 'INSPECT',
            'project_id': project,
            'grounds_status': grounds,
            'binding_status': binding or
                'OBJECT_CURRENTLY_VISIBLE_NOT_EVIDENCE_OF_RIGHTS',
            'world_request': {
                'operation': 'INSPECT',
                'material_object_ref': ref,
                'addressed_party_ref': None,
            },
        }

    def test_trial_object_has_one_world_identity_despite_two_cultural_groundings(self):
        # The same thing can be visually available AND personally heard about.
        # Two psychological alternatives must not become two material objects.
        trial={'operation':'INSPECT','source_material_object_ref':'woodwork-A'}
        seen=self._option('woodwork-A',
                          'PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE','visible')
        heard=self._option('woodwork-A',
                           'UNTESTED_PERSONALLY_HEARD_PUBLIC_OBJECT_REFERENCE','heard')
        chosen=_bind_actor_trial_particular_object([heard,seen],trial)
        self.assertEqual(chosen['option_id'],'visible')
        self.assertIsNone(chosen['project_id'])
        self.assertEqual(chosen['world_request']['material_object_ref'],'woodwork-A')
        self.assertEqual(len([seen,heard]),2)

    def test_trial_never_substitutes_another_object_or_incompatible_project(self):
        trial={'operation':'INSPECT','source_material_object_ref':'woodwork-A'}
        foreign=self._option('woodwork-B',
                             'PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE','foreign')
        attached=self._option('woodwork-A',
                              'PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE','project',
                              project='adult_gift_purpose')
        with self.assertRaisesRegex(ValueError,'TRIAL_MATERIAL_OBJECT_NOT_UNIQUELY_BINDABLE'):
            _bind_actor_trial_particular_object([foreign,attached],trial)

    def test_two_unresolved_equivalent_objects_require_a_nonambiguous_binding(self):
        trial={'operation':'INSPECT','source_material_object_ref':'woodwork-A'}
        a=self._option('woodwork-A','PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE','a')
        b=self._option('woodwork-A','PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE','b')
        with self.assertRaisesRegex(ValueError,'TRIAL_MATERIAL_OBJECT_NOT_UNIQUELY_BINDABLE'):
            _bind_actor_trial_particular_object([a,b],trial)

    def test_semantic_trial_id_is_a_complete_action_selector_without_action(self):
        semantic=ValidatingSemanticService(CallbackLLMProvider(
            lambda task,packet: {'task':task,'possible_end_trial_id':'issued_ticket'}))
        self.assertEqual(semantic.proposal('actor_attempt',{})['possible_end_trial_id'],
                         'issued_ticket')
        with self.assertRaisesRegex(ValueError,'NO_ACTION_OR_PRACTICAL_OPTION'):
            ValidatingSemanticService(CallbackLLMProvider(
                lambda task,packet:{'task':task})).proposal('actor_attempt',{})


if __name__=="__main__":
    unittest.main()
