"""R3 sourcefree court: real embodied communicative capacity from social activity.

An adult's actual public speech about a real object precedes independently
answered child vocal turns. Two different, age-separated actor-lived SIGNAL
episodes may change motor/expressive capacity under maturation bounds.
No child vocabulary, meanings or adult intentions may be fabricated.
"""
import copy
import unittest

from um_sorok_organism.types import (
    newborn,adult,Attempt,blank_world)
from um_sorok_organism.organism import mature,eligible
from um_sorok_organism.world import IndependentWorldAuthority
from um_sorok_organism.cultural_mediation import (
    conserve_personally_heard_reference)
from um_sorok_organism.social_vocal_development import (
    conserve_reciprocated_vocal_turn,possible_vocal_coordination)
from um_sorok_organism.development import admit,InvalidDevelopment
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    HeuristicSemanticProvider,CallbackLLMProvider,ValidatingSemanticService)
import tempfile
from pathlib import Path


def stage_public_object_speech(child):
    world=blank_world()
    world["positions"]["nadia"]="home"
    world["positions"]["father"]="home"
    world["material_objects"]["object:one"]={
        "id":"object:one","kind":"WORKED_MATERIAL_ARTIFACT",
        "location":"home","visible":True}
    world["clock"]=1
    experience={
        "actor":"nadia","clock":1,"ref":"private:heard_object_speech",
        "location":"home","status":"OBSERVED",
        "own_action":None,"participated":False,"perceived_cues":[{
            "id":"public:speech:one","kind":"performed_speak",
            "modality":"auditory","source_actor":"father",
            "material_object_ref":"object:one",
            "actual_spoken_object_demonstration":True,
            "tags":["speak","public_object_reference"]}]}
    saved=conserve_personally_heard_reference(
        child,experience,"world:spoken_object",world)
    assert len(saved)==1
    return world


def social_turn(child,clock,age_days,speaker="father",responded=True):
    if child["age_days"]>age_days:
        raise ValueError("NONMONOTONIC_TEST_AGE")
    mature(child,age_days-child["age_days"])
    experience={
        "actor":"nadia","clock":clock,"ref":"exp:vocal:"+str(clock),
        "location":"home","own_action":"SIGNAL",
        "status":"PERFORMED","participated":True,
        "felt_enactment":{"attempted_operation":"SIGNAL",
                          "objective_result_not_inferred":True},
        "perceived_cues":[{
            "id":"public:turn:"+str(clock),
            "kind":"performed_signal","source_actor":"nadia",
            "modality":"auditory",
            "actual_independent_speech_response":responded,
            "actor_accessible_speech_responder_ref":speaker,
            "spoken_content":"NOT_CAPTURED_OR_RECONSTRUCTED",
            "tags":["signal","joint_activity_performed"]}]}
    record=conserve_reciprocated_vocal_turn(
        child,experience,"world:turn:"+str(clock))
    return experience,record


class ActualSocialVocalDevelopment(unittest.TestCase):
    def test_bodily_readiness_and_distinct_social_exchanges_create_small_skill(self):
        n=newborn("nadia","Nadia")
        stage_public_object_speech(n)
        a,x=social_turn(n,2,180)
        self.assertIsNotNone(x)
        self.assertEqual(possible_vocal_coordination(
            n,a,"world:turn:2"),[])
        b,y=social_turn(n,3,194)
        self.assertIsNotNone(y)
        possibilities=possible_vocal_coordination(
            n,b,"world:turn:3")
        self.assertEqual(len(possibilities),1)
        self.assertEqual(possibilities[0]["new_capacity_delta"],.07)
        result=admit(n,b,"world:turn:3",possibilities)
        self.assertEqual(result[0]["status"],
                         "ACTUALLY_ACQUIRED_BOUNDED_SOCIAL_VOCAL_CAPACITY")
        self.assertEqual(n["body"]["language"],.07)
        self.assertLess(n["body"]["language"],
                        n["body"]["language_ceiling"])
        self.assertFalse(eligible(n["body"],"SPEAK")[0])
        self.assertEqual(n["projects"],[])
        self.assertEqual(n["self_model"],{})
        self.assertEqual(len(n["vocal_coordination_practices"]),1)

    def test_several_spaced_social_periods_cross_speak_capacity_only_after_maturation(self):
        n=newborn("nadia","Nadia")
        stage_public_object_speech(n)
        for clock,days in enumerate((180,200,220,240,450,470),start=2):
            exp,turn=social_turn(n,clock,days)
            self.assertIsNotNone(turn)
            possibilities=possible_vocal_coordination(
                n,exp,"world:turn:"+str(clock))
            if possibilities:
                admit(n,exp,"world:turn:"+str(clock),possibilities)
            self.assertLessEqual(n["body"]["language"],
                                 n["body"]["language_ceiling"])
        self.assertTrue(eligible(n["body"],"SPEAK")[0])
        self.assertGreaterEqual(n["body"]["language"],.35)
        self.assertFalse(any("word_meaning" in str(r) for r in
                             n["vocal_coordination_practices"]))

    def test_no_demonstration_or_no_independent_reply_no_acquired_capacity(self):
        n=newborn("nadia","Nadia")
        a,r=social_turn(n,2,180)
        self.assertIsNone(r)
        stage_public_object_speech(n)
        b,r=social_turn(n,3,194,responded=False)
        self.assertIsNone(r)
        self.assertEqual(n["vocal_turn_experiences"],[])
        self.assertEqual(n["body"]["language"],0.)

    def test_same_day_repetition_is_not_maturation(self):
        n=newborn("nadia","Nadia")
        stage_public_object_speech(n)
        social_turn(n,2,180)
        b,_=social_turn(n,3,180)
        self.assertEqual(possible_vocal_coordination(
            n,b,"world:turn:3"),[])

    def test_old_turn_cannot_be_reused_to_farm_capacity_each_day(self):
        n=newborn("nadia","Nadia")
        stage_public_object_speech(n)
        social_turn(n,2,180)
        second,_=social_turn(n,3,200)
        admit(n,second,"world:turn:3",possible_vocal_coordination(
            n,second,"world:turn:3"))
        self.assertEqual(n["body"]["language"],.07)
        third,_=social_turn(n,4,201)
        self.assertEqual(possible_vocal_coordination(
            n,third,"world:turn:4"),[])
        self.assertEqual(n["body"]["language"],.07)

    def test_model_cannot_forge_skill_or_coactor_source_atomically(self):
        n=newborn("nadia","Nadia")
        stage_public_object_speech(n)
        social_turn(n,2,180)
        e,_=social_turn(n,3,194)
        original=copy.deepcopy(n)
        allowed=possible_vocal_coordination(
            n,e,"world:turn:3")[0]
        for key,value in (
            ("source_other_ref","fictional_mother"),
            ("earlier_actual_vocal_turn_ref","forged_event"),
            ("new_capacity_delta",.75)):
            proposal=dict(allowed);proposal[key]=value
            with self.assertRaises(InvalidDevelopment):
                admit(n,e,"world:turn:3",[proposal])
            self.assertEqual(n,original)

    def test_world_independently_planned_speech_response_is_a_real_coactivity(self):
        child=newborn("nadia","Nadia")
        father=adult("father","Father")
        w=blank_world()
        w["positions"]={"nadia":"home","father":"home"}
        def independently_formed_father_plan(principal,world,actors):
            self.assertEqual(principal.actor,"nadia")
            self.assertEqual(principal.target,"father")
            self.assertEqual(actors["father"]["id"],"father")
            return Attempt(actor="father",action="SPEAK",target="nadia",
                           intention="INDEPENDENT_FATHER_POLICY_TEST")
        court=IndependentWorldAuthority(independently_formed_father_plan)
        effect,partner,receipt=court.resolve(w,{"nadia":child,"father":father},
            Attempt(actor="nadia",action="SIGNAL",target="father"))
        self.assertEqual(effect.status,"PERFORMED")
        self.assertEqual(effect.objective_description,
                         "JOINT_ACTIVITY_PERFORMED")
        self.assertEqual(partner.actor,"father")
        self.assertEqual(receipt["coactor"],"father")
        cue=w["cues"][-1]
        self.assertTrue(cue["actual_independent_speech_response"])
        self.assertEqual(cue["actor_accessible_speech_responder_ref"],
                         "father")
        self.assertEqual(cue["spoken_content"],
                         "NOT_CAPTURED_OR_RECONSTRUCTED")



class JoinedIndependentAdultSpeechAndInfantVocalHistory(unittest.TestCase):
    def test_actual_world_speaker_different_from_child_self_and_independent_reply(self):
        seed={
            "source_ref":"SOURCEFREE_INDEPENDENT_ADULT_STAGED_SPEECH",
            "answers":{"not_original_PYAT":"fictional_for_world_court"},
            "fictional_seed":{"projects":[{"object":"continuing situated vocal activity",
                "means":["SPEAK"],"priority":.2,"cue_terms":["home"]}]}}
        original=HeuristicSemanticProvider()
        def other_policy(task,packet):
            # Deliberately separate adult provider call and actual speaking
            # from the child's requester. No caller can author adult consent.
            if (task=="actor_attempt" and
                packet.get("requesting_actor")=="nadia" and
                packet.get("requesting_action")=="SIGNAL" and
                packet.get("actor",{}).get("id")=="father"):
                return {"task":"actor_attempt","action":"SPEAK",
                        "project_id":None,
                        "purpose_selection_grade":"INDEPENDENT_SOURCEFREE_ADULT_RESPONSE"}
            return original.propose(task,packet)
        with tempfile.TemporaryDirectory() as folder:
            runtime=ConstitutiveRuntime(
                str(Path(folder)/"real_vocal_world.sqlite"),
                semantic=ValidatingSemanticService(CallbackLLMProvider(
                    other_policy)))
            try:
                runtime.initialize([("father","Father",seed),
                                    ("mother","Mother",seed)])
                making=runtime.step(
                    "father",requested_action="MAKE_OBJECT")
                self.assertEqual(making["status"],"PERFORMED")
                obj=next(iter(runtime.ledger.world("w1")[1]["material_objects"]))
                reference=runtime.step(
                    "father",requested_action="SPEAK",object_ref=obj)
                self.assertEqual(reference["status"],"PERFORMED")
                first=runtime.snapshot("nadia")
                self.assertEqual(len(first["cultural_demonstrations"]),1)
                exchange=runtime.step(
                    "nadia",requested_action="SIGNAL",target="father")
                self.assertEqual(exchange["status"],"PERFORMED")
                self.assertEqual(exchange["coactor"],"SPEAK")
                child=runtime.snapshot("nadia")
                self.assertEqual(len(child["vocal_turn_experiences"]),1)
                self.assertEqual(child["vocal_turn_experiences"][0][
                    "independently_responding_other_ref"],"father")
                self.assertEqual(child["body"]["language"],0.)
                self.assertEqual(child["role"],"child")
                self.assertEqual(child["projects"],[])
                self.assertTrue(runtime.verify()["valid"])
            finally:
                runtime.close()


if __name__=="__main__":
    unittest.main()
