"""SORACLE P013/P023 R2 — exact source and qualitative genesis adversarial court.

Authoring tests is not test execution. Independent REMONT must run normal,
optimized, cold SQLite, inherited R20 and independent R15 ancestry reconciliation.
"""
import copy
import unittest
from um_sorok_organism.types import adult,newborn
from um_sorok_organism.semantics import ValidatingSemanticService
from um_sorok_organism.blind_parent_probes import (
    blind_operational_interview,actor_evidence_roster)
from um_sorok_organism.psychic_genesis import (
    conserve_lived_episode,possible_contrast_end)
from um_sorok_organism.development import admit,InvalidDevelopment


class StubModel:
    grade="SYNTHETIC_HERMETIC_TEST"
    def __init__(self,result):
        self.result=result
        self.packet=None
    def propose(self,task,packet):
        self.packet=copy.deepcopy(packet)
        return {"task":task,"responses":copy.deepcopy(self.result)}


def op_form(person,ident):
    return {"id":ident,"actor":person["id"],"kind":"PRACTICE",
            "content":"acquired cooperation in ordinary work",
            "cues":["work"],"enables":["WORK"],
            "scope":{},"strength":.5,"lifecycle":"ACTIVE"}

def parent():
    p=adult("mother","Mother")
    p["forms"]["answer_mediator"]={
        "id":"answer_mediator","object":"q1","asserted_answer":"no",
        "content":"fictional stance regarding q1: no",
        "kind":"MEDIATOR","enables":["SPEAK"]}
    p["forms"]["life_practice"]=op_form(p,"life_practice")
    p["projects"]=[{"id":"project:help","object":"help in ordinary life",
                    "means":["CARE","WORK"],"priority":.5}]
    return p

Q=[{"id":"q1","wording":"Fictional question about a situated practice",
    "values":["no","yes"]}]


class BlindParentOperativeAssessment(unittest.TestCase):
    def test_model_never_sees_cached_source_answers_and_must_reference_life(self):
        p=parent()
        model=StubModel({"q1":{
            "status":"HYPOTHETICAL_ACTOR_FUNCTION_READOUT",
            "value":"yes","source_refs":["form:life_practice"]}})
        result=blind_operational_interview(
            p,Q,ValidatingSemanticService(model))
        self.assertEqual(result["responses"],{"q1":"yes"})
        self.assertEqual(result["unanswered"],[])
        self.assertIn("form:life_practice",
                      model.packet["evidence_roster"])
        self.assertNotIn("form:answer_mediator",
                         model.packet["evidence_roster"])
        self.assertNotIn("answer_mediator",
                         model.packet["actor"]["acquired_non_questionnaire_forms"])
        self.assertNotIn("asserted_answer",str(model.packet))
        self.assertNotIn("fictional stance regarding q1",
                         str(model.packet))
        self.assertEqual(result["respondent_fidelity"],"NOT_MEASURED")

    def test_source_answer_change_does_not_change_blind_packet(self):
        p1=parent();p2=parent()
        p2["forms"]["answer_mediator"]["asserted_answer"]="yes"
        p2["forms"]["answer_mediator"]["content"]="fictional stance regarding q1: yes"
        m1=StubModel({});m2=StubModel({})
        blind_operational_interview(p1,Q,ValidatingSemanticService(m1))
        blind_operational_interview(p2,Q,ValidatingSemanticService(m2))
        self.assertEqual(m1.packet,m2.packet)

    def test_answer_without_real_operative_ground_is_refused(self):
        for refs in ([],["form:answer_mediator"],["form:invented"],
                     ["form:life_practice","form:life_practice"]):
            m=StubModel({"q1":{
                "status":"HYPOTHETICAL_ACTOR_FUNCTION_READOUT",
                "value":"yes","source_refs":refs}})
            with self.assertRaises(ValueError):
                blind_operational_interview(parent(),Q,
                                            ValidatingSemanticService(m))

    def test_unqualified_value_and_question_instrument_rejected(self):
        m=StubModel({"q1":{
            "status":"HYPOTHETICAL_ACTOR_FUNCTION_READOUT",
            "value":"maybe","source_refs":["form:life_practice"]}})
        with self.assertRaises(ValueError):
            blind_operational_interview(parent(),Q,ValidatingSemanticService(m))
        with self.assertRaises(ValueError):
            blind_operational_interview(parent(),Q+Q,ValidatingSemanticService(m))

    def test_unsupported_question_abstains_without_fabrication(self):
        m=StubModel({})
        result=blind_operational_interview(
            parent(),Q,ValidatingSemanticService(m))
        self.assertEqual(result["responses"],{})
        self.assertEqual(result["unanswered"],["q1"])


def e(actor,clock,event,act,status,tags,participated=True,felt=True):
    return {"actor":actor["id"],"clock":clock,"ref":"exp:"+event,
            "location":"home","own_action":act,"status":status,
            "participated":participated,
            "perceived_cues":[{
                "id":"cue:"+event,"tags":tags,"modality":"tactile"}],
            "felt_enactment":({
                "attempted_operation":act,
                "objective_result_not_inferred":True} if felt else None)}


class HistoryGovernsOperativeEnd(unittest.TestCase):
    def setUp(self):
        self.n=newborn("nadia","Nadia")
        self.first=e(self.n,1,"first","SIGNAL","PARTIAL",["signal"])
        b=copy.deepcopy(self.n["body"])
        conserve_lived_episode(self.n,self.first,"world:first",b,b)
        self.later=e(self.n,2,"care","RECEIVED_CARE","OBSERVED",
                     ["care","contact"],felt=False)
        after=dict(b);after["comfort"]=min(1.,b["comfort"]+.15)
        self.n["body"]=after
        conserve_lived_episode(self.n,self.later,"world:care",b,after)

    def test_object_of_new_possibility_not_freely_invented_by_llm(self):
        proposed=possible_contrast_end(self.n,self.later,"world:care")
        self.assertEqual(len(proposed),1)
        self.assertEqual(proposed[0]["relieved_bodily_axis"],"comfort")
        bad=dict(proposed[0]);bad["possible_object"]="become a rich adult"
        with self.assertRaises(InvalidDevelopment):
            admit(self.n,self.later,"world:care",[bad])
        self.assertEqual(self.n["possible_ends"],[])
        good=dict(proposed[0])
        good["interpretive_hypothesis"]=(
            "maybe the bodily benefit will become worth approaching")
        admit(self.n,self.later,"world:care",[good])
        end=self.n["possible_ends"][0]
        self.assertEqual(end["possible_object"],proposed[0]["possible_object"])
        self.assertNotEqual(end["possible_object"],"become a rich adult")
        self.assertEqual(end["origin_clock"],2)
        self.assertIn("world:first",end["source_event_refs"])

    def test_unrelated_later_event_cannot_launder_generated_end_into_project(self):
        proposed=possible_contrast_end(self.n,self.later,"world:care")
        admit(self.n,self.later,"world:care",proposed)
        ref=self.n["possible_ends"][0]["id"]
        irrelevant=e(self.n,3,"unrelated","ORIENT","PERFORMED",
                     ["bell","wall"])
        with self.assertRaisesRegex(InvalidDevelopment,
                                    "GENETIC_TAKEUP_NO_REENCOUNTERED_SIGN"):
            admit(self.n,irrelevant,"world:unrelated",[{
                "kind":"TAKE_UP_POSSIBLE_END","possible_end_ref":ref,
                "means":["SIGNAL"]}])
        self.assertEqual(self.n["projects"],[])
        relevant=e(self.n,3,"later_contact","SIGNAL","PERFORMED",
                   ["care","contact"])
        admit(self.n,relevant,"world:later_contact",[{
            "kind":"TAKE_UP_POSSIBLE_END","possible_end_ref":ref,
            "later_perceived_cue_ref":"cue:later_contact",
            "means":["SIGNAL"]}])
        self.assertEqual(len(self.n["projects"]),1)
        self.assertEqual(self.n["projects"][0]["origin"],
                         ["world:care","world:later_contact"])

    def test_same_clock_cannot_fake_second_occasion(self):
        proposed=possible_contrast_end(self.n,self.later,"world:care")
        admit(self.n,self.later,"world:care",proposed)
        ref=self.n["possible_ends"][0]["id"]
        same=e(self.n,2,"same_tick","SIGNAL","PERFORMED",["care"])
        with self.assertRaisesRegex(InvalidDevelopment,
                                    "GENETIC_TAKEUP_NOT_LATER_EXPERIENCE"):
            admit(self.n,same,"world:same_tick",[{
                "kind":"TAKE_UP_POSSIBLE_END","possible_end_ref":ref,
                "later_perceived_cue_ref":"cue:same_tick","means":["SIGNAL"]}])
        self.assertFalse(self.n["projects"])


if __name__=="__main__":
    unittest.main()
