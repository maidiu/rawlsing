"""SORACLE developmental-first receiving court (candidate, not certification).

P004/P011/P023: two actually experienced, different events are necessary
before a *new possible end* can be constructed. Later experience is necessary
to turn possibility into an active motive. P014: LLM provider must be explicit,
network-safe, actor-scoped, and typed owner remains effective.
"""
import tempfile
import unittest
import json
from pathlib import Path

from um_sorok_organism.types import newborn,adult
from um_sorok_organism.psychic_genesis import (
    conserve_lived_episode,possible_contrast_end)
from um_sorok_organism.development import admit,InvalidDevelopment
from um_sorok_organism.live_psychological_llm import ExplicitJSONLLMProvider
from um_sorok_organism.semantics import ValidatingSemanticService
from um_sorok_organism.runtime import ConstitutiveRuntime

GRADE_FIXTURE={
    "source_ref":"nadia_first_fictional_parent_condition",
    "source_grade":"UNQUALIFIED_FICTIONAL_TEST_FIXTURE",
    "answers":{"fictional_parent_test_only":"not_a_survey_source"},
    "fictional_seed":{"projects":[]}
}

def experience(actor,event,*,clock,action,status,cues=(),felt=True):
    return {
        "actor":actor,"clock":clock,"location":"home",
        "ref":"experience:"+actor+":"+event,
        "own_action":action,"status":status,
        "participated":True,
        "perceived_cues":list(cues),
        "felt_enactment":({
            "attempted_operation":action,
            "objective_result_not_inferred":True}
            if felt else None),
        "actor_access_grade":"SOURCEFREE_TEST"
    }

def witness_pair(actor):
    early=experience(actor["id"],"unfulfilled_signal",clock=1,
                     action="SIGNAL",status="PARTIAL",cues=[
                         {"id":"earlier:own_signal","tags":["signal"],
                          "modality":"auditory"}])
    b=dict(actor["body"])
    first=conserve_lived_episode(actor,early,"world:earlier",b,b,
        "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
    later=experience(actor["id"],"real_relief",clock=2,
                     action="RECEIVED_CARE",status="OBSERVED",felt=False,
                     cues=[{"id":"later:received_care",
                            "tags":["care","contact"],
                            "modality":"tactile"}])
    prior=dict(actor["body"])
    after=dict(prior)
    after["comfort"]=min(1.0,prior["comfort"]+.15)
    actor["body"]=after
    second=conserve_lived_episode(actor,later,"world:later",prior,after)
    proposed=possible_contrast_end(actor,later,"world:later")
    return first,second,later,proposed

class ContrastedPsychicGenesis(unittest.TestCase):
    def test_nadia_distinct_history_produces_provisional_new_end(self):
        child=newborn("nadia","Nadia")
        first,second,later,proposals=witness_pair(child)
        self.assertTrue(first["unfinished_own_activity"])
        self.assertTrue(second["received_relief"]["comfort"]>=.025)
        self.assertEqual(len(proposals),1)
        before_projects=list(child["projects"])
        admitted=admit(child,later,"world:later",proposals)
        self.assertEqual(admitted[0]["status"],
                         "ADMITTED_CONTRASTED_POSSIBILITY_NOT_YET_MOTIVE")
        self.assertEqual(child["projects"],before_projects)
        self.assertEqual(child["possible_ends"][0]["status"],
                         "POSSIBLE_NOT_ACQUIRED_MOTIVE")
        self.assertEqual(child["possible_ends"][0][
            "actual_contrasted_episode_refs"],[first["id"],second["id"]])
        self.assertFalse("I know why" in str(child["possible_ends"]))
        self.assertEqual(child["self_model"],{})

    def test_no_intrinsic_end_from_only_one_good_episode(self):
        child=newborn("nadia","Nadia")
        good=experience("nadia","care",clock=1,action="RECEIVED_CARE",
                        status="OBSERVED",felt=False,
                        cues=[{"id":"felt-care","tags":["care"]}])
        before=dict(child["body"]);after=dict(before);after["comfort"]+=.12
        conserve_lived_episode(child,good,"world:care",before,after)
        self.assertEqual(possible_contrast_end(child,good,"world:care"),[])
        self.assertEqual(child["projects"],[])
        self.assertEqual(child["possible_ends"],[])

    def test_same_event_cannot_be_contrasted_with_itself(self):
        child=newborn("nadia","Nadia")
        early=experience("nadia","both",clock=1,action="SIGNAL",
                         status="PARTIAL",cues=[{
                             "id":"signal-and-relief","tags":["contact"]}])
        b=dict(child["body"]);a=dict(b);a["comfort"]+=.10
        conserve_lived_episode(child,early,"world:both",b,a)
        self.assertEqual(possible_contrast_end(child,early,"world:both"),[])

    def test_forged_earlier_or_later_source_rejected_atomically(self):
        child=newborn("nadia","Nadia")
        _,_,later,proposed=witness_pair(child)
        bad=dict(proposed[0]);bad["prior_unfinished_episode_ref"]="invented"
        before=json.dumps(child,sort_keys=True)
        with self.assertRaises(InvalidDevelopment):
            admit(child,later,"world:later",[bad])
        self.assertEqual(json.dumps(child,sort_keys=True),before)
        bad=dict(proposed[0]);bad["possible_means"]=["WORK"]
        with self.assertRaises(InvalidDevelopment):
            admit(child,later,"world:later",[bad])
        self.assertEqual(json.dumps(child,sort_keys=True),before)

    def test_perceived_event_must_have_bodily_differential_and_sign(self):
        child=newborn("nadia","Nadia")
        first=experience("nadia","failed",clock=1,action="SIGNAL",
                         status="BLOCKED")
        b=dict(child["body"])
        conserve_lived_episode(child,first,"world:1",b,b)
        later=experience("nadia","claimed",clock=2,action="RECEIVED_CARE",
                         status="OBSERVED",felt=False)
        after=dict(b);after["comfort"]+=.18
        self.assertIsNone(conserve_lived_episode(
            child,later,"world:2",b,after))
        self.assertEqual(possible_contrast_end(child,later,"world:2"),[])

    def test_a_third_experience_can_form_an_active_end_not_retcon_intent(self):
        child=newborn("nadia","Nadia")
        _,_,later,proposal=witness_pair(child)
        admitted=admit(child,later,"world:later",proposal)
        end=child["possible_ends"][0]
        another=experience("nadia","third",clock=3,
            action="SIGNAL",status="PERFORMED",
            cues=[{"id":"third:care","tags":["care"],
                   "modality":"auditory"}])
        before=len(child["projects"])
        report=admit(child,another,"world:third",[{
            "kind":"TAKE_UP_POSSIBLE_END","possible_end_ref":end["id"],
            "later_perceived_cue_ref":"third:care",
            "means":["SIGNAL"],"priority":.4}])
        self.assertEqual(report[0]["kind"],"TAKE_UP_POSSIBLE_END")
        self.assertEqual(len(child["projects"]),before+1)
        project=child["projects"][-1]
        self.assertEqual(project["origin"],["world:later","world:third"])
        self.assertTrue(project["original_attempt_purpose_not_rewritten"])
        self.assertIn("world:earlier",end["source_event_refs"])
        self.assertEqual(child["possible_ends"][0]["status"],
                         "TAKEN_UP_AS_PRACTICAL_PROJECT")


class ExplicitLiveLLMContract(unittest.TestCase):
    def test_remote_disclosure_is_not_default(self):
        with self.assertRaises(ValueError):
            ExplicitJSONLLMProvider(endpoint="https://example.org/chat/completions",
                model="caller-supplied",api_key="dummy")
        with self.assertRaises(ValueError):
            ExplicitJSONLLMProvider(endpoint="http://example.org/chat/completions",
                model="caller-supplied",api_key="dummy",
                allow_private_actor_data=True)

    def test_explicit_model_hypothesis_reaches_typed_owner_not_world(self):
        captured=[]
        def transport(request):
            captured.append(request)
            return {"choices":[{"message":{"content":json.dumps({
                "task":"development","candidates":[{"kind":"NO_CHANGE"}]
            })}}]}
        provider=ExplicitJSONLLMProvider(
            endpoint="https://example.org/chat/completions",
            model="caller-supplied",api_key="dummy",
            allow_private_actor_data=True,transport=transport)
        packet={"actor":{"id":"nadia","role":"child"},
                "experience":{"actor":"nadia","perceived_cues":[]}}
        out=ValidatingSemanticService(provider).proposal("development",packet)
        self.assertEqual(out["candidates"],[{"kind":"NO_CHANGE"}])
        self.assertEqual(len(captured),1)
        self.assertIn("NO_CHANGE",captured[0]["messages"][0]["content"])
        self.assertNotIn("dummy",json.dumps(captured[0]))

    def test_model_cannot_bypass_actor_owned_source_checks(self):
        child=newborn("nadia","Nadia")
        _,_,later,correct=witness_pair(child)
        def transport(request):
            return {"choices":[{"message":{"content":json.dumps({
                "task":"development","candidates":[{
                    **correct[0],
                    "prior_unfinished_episode_ref":"invented_external_episode"
                }]
            })}}]}
        provider=ExplicitJSONLLMProvider(
            endpoint="https://example.org/chat/completions",
            model="test",api_key="dummy",allow_private_actor_data=True,
            transport=transport)
        candidate=ValidatingSemanticService(provider).proposal(
            "development",{"experience":later})["candidates"]
        with self.assertRaises(InvalidDevelopment):
            admit(child,later,"world:later",candidate)
        self.assertEqual(child["possible_ends"],[])


class JoinedNadiaGeneticLife(unittest.TestCase):
    def test_attempted_unanswered_signal_followed_by_bodily_care_changes_future(self):
        with tempfile.TemporaryDirectory() as directory:
            rt=ConstitutiveRuntime(str(Path(directory)/"one_nadia.sqlite"))
            try:
                rt.initialize([
                    ("mother","Mother",GRADE_FIXTURE),
                    ("father","Father",GRADE_FIXTURE)])
                # Distinct world permission and adult action; not a
                # hypothetical fabricated developmental event.
                moved=rt.step("mother",requested_action="MOVE",
                              object_ref="workshop")
                self.assertEqual(moved["status"],"PERFORMED")
                unfulfilled=rt.step("nadia",requested_action="SIGNAL",
                                    target="mother")
                self.assertIn(unfulfilled["status"],("PARTIAL","BLOCKED"))
                cared=rt.step("father",requested_action="CARE",
                              target="nadia")
                self.assertEqual(cared["status"],"PERFORMED")
                child=rt.ledger.actor("nadia")[1]
                self.assertGreaterEqual(len(child["lived_genesis_episodes"]),2)
                self.assertTrue(any(x.get("genesis_witness_ref")
                    for x in child["possible_ends"]))
                self.assertEqual(child["projects"],[])
                self.assertEqual(child["self_model"],{})
                self.assertTrue(rt.verify())
            finally:
                rt.close()


if __name__=="__main__":
    unittest.main()
