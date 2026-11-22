"""SORACLE R3 — whole-source cultural mediation and material sign integrity.

Sourcefree code court, not empirical language science: world-owned artifact,
actual adult speech about that artifact, child audible experience, child own
different inspection, typed acquired conditional reference, later prospective
attention. Neither adult private meanings nor lexical comprehension appear.
"""
import copy
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.types import (
    adult,newborn,blank_world,AccessibleEncounter)
from um_sorok_organism.constitution import materialize
from um_sorok_organism.cultural_mediation import (
    conserve_personally_heard_reference,possible_cultural_object_inquiry,
    admit_cultural_reference,cultural_object_alternatives,
    choose_culturally_situated_object_inquiry,
    possible_reference_revision,admit_reference_revision)
from um_sorok_organism.development import admit,InvalidDevelopment
from um_sorok_organism.runtime import ConstitutiveRuntime

SEED={"source_ref":"SOURCEFREE_FICTIONAL_PARENT_NOT_PYAT",
      "answers":{"fictional_instrument_field":"fictional_no_source_truth"},
      # Sourcefree parent has already acquired capacity to use SPEAK; no
      # questionnaire answer is assumed to endow the child with language.
      "fictional_seed":{"projects":[{
          "object":"participate in already acquired ordinary speech",
          "means":["SPEAK"],"priority":.2,"cue_terms":["home"]}]}}


def world_with_object():
    w=blank_world()
    w["positions"]={"nadia":"home","father":"home"}
    obj={"id":"artifact:a","kind":"WORKED_MATERIAL_ARTIFACT",
         "location":"home","visible":True,"owner":"father",
         "maker":"father","possessor":"father","condition":.7}
    w["material_objects"][obj["id"]]=obj
    return w


def heard_experience(child,w,event="objective:speech",cue_ref="audible:speech"):
    return {"actor":child["id"],"clock":w["clock"],
            "location":"home","ref":"private:heard:"+cue_ref,
            "own_action":None,"status":"OBSERVED","participated":False,
            "felt_enactment":None,"perceived_cues":[{
                "id":cue_ref,"clock":w["clock"],
                "kind":"performed_speak","source_actor":"father",
                "modality":"auditory","material_object_ref":"artifact:a",
                "actual_spoken_object_demonstration":True,
                "tags":["speak","public_object_reference"]}]}


def inspected_experience(child,w,clock,object_ref="artifact:a"):
    w["clock"]=clock
    return {"actor":child["id"],"clock":clock,"location":"home",
            "ref":"private:inspect:"+str(clock),
            "own_action":"INSPECT","status":"PERFORMED","participated":True,
            "felt_enactment":{"attempted_operation":"INSPECT",
                              "objective_result_not_inferred":True},
            "perceived_cues":[{
                "id":"private:cued_inspect:"+str(clock),
                "kind":"performed_inspect","source_actor":"nadia",
                "modality":"visual","material_object_ref":object_ref,
                "tags":["inspect","material_object"]}]}


class SourceSpecificCulture(unittest.TestCase):
    def test_heard_other_then_personally_inspected_object_acquires_only_reference(self):
        n=newborn("nadia","Nadia");w=world_with_object();w["clock"]=1
        heard=heard_experience(n,w)
        self.assertEqual(len(conserve_personally_heard_reference(
            n,heard,"world:speech",w)),1)
        self.assertEqual(n["cultural_reference_practices"],[])
        self.assertEqual(n["body"]["language"],0.0)
        inspect=inspected_experience(n,w,2)
        proposals=possible_cultural_object_inquiry(n,inspect,"world:inspect")
        self.assertEqual(len(proposals),1)
        effect=admit(n,inspect,"world:inspect",proposals)
        self.assertEqual(effect[0]["status"],
                         "ACQUIRED_SOURCEFREE_SITUATED_REFERENCE_NOT_WORD")
        acquired=n["cultural_reference_practices"]
        self.assertEqual(len(acquired),1)
        self.assertEqual(acquired[0]["source_event_refs"],
                         ["world:speech","world:inspect"])
        self.assertEqual(acquired[0]["status"],
                         "ACQUIRED_SITUATED_PUBLIC_OBJECT_REFERENCE")
        self.assertEqual(n["body"]["language"],0.0)
        self.assertEqual(n["self_model"],{})
        self.assertEqual(n["projects"],[])
        view=materialize(n,w)
        access=AccessibleEncounter(actor="nadia",world_clock=2,
            location="home",cues=[{"id":"visible:a",
                "kind":"material_object_present",
                "material_object_ref":"artifact:a"}],
            affordances=["INSPECT"],access_receipts=[])
        alternatives=cultural_object_alternatives(
            view,access,{"action":"INSPECT"})
        self.assertEqual(len(alternatives),1)
        self.assertEqual(alternatives[0]["world_request"][
            "material_object_ref"],"artifact:a")
        selected=choose_culturally_situated_object_inquiry([{
            "action":"INSPECT","practical_alternatives":alternatives}])
        self.assertEqual(selected["practical_option_id"],
                         alternatives[0]["option_id"])
        self.assertNotIn("lexical_word",str(acquired))

    def test_absent_or_unheard_source_cannot_confer_meaning(self):
        n=newborn("nadia","Nadia");w=world_with_object();w["clock"]=1
        received=heard_experience(n,w)
        w["material_objects"]["artifact:a"]["location"]="workshop"
        self.assertEqual(conserve_personally_heard_reference(
            n,received,"world:speech",w),[])
        self.assertEqual(n["cultural_demonstrations"],[])
        w["material_objects"]["artifact:a"]["location"]="home"
        received["perceived_cues"][0]["source_actor"]="nadia"
        self.assertEqual(conserve_personally_heard_reference(
            n,received,"world:speech",w),[])
        received["perceived_cues"][0]["source_actor"]="father"
        received["perceived_cues"][0]["actual_spoken_object_demonstration"]=False
        self.assertEqual(conserve_personally_heard_reference(
            n,received,"world:speech",w),[])

    def test_unrelated_object_or_single_event_is_not_a_cultural_skill(self):
        n=newborn("nadia","Nadia");w=world_with_object();w["clock"]=1
        seen=heard_experience(n,w)
        conserve_personally_heard_reference(n,seen,"world:speech",w)
        other=inspected_experience(n,w,2,object_ref="artifact:other")
        self.assertEqual(possible_cultural_object_inquiry(
            n,other,"world:inspect_other"),[])
        same=inspected_experience(n,w,1)
        self.assertEqual(possible_cultural_object_inquiry(
            n,same,"world:speech"),[])

    def test_model_forged_speaker_and_object_do_not_enter_actor(self):
        n=newborn("nadia","Nadia");w=world_with_object();w["clock"]=1
        spoken=heard_experience(n,w)
        conserve_personally_heard_reference(n,spoken,"world:speech",w)
        inspected=inspected_experience(n,w,2)
        proposal=possible_cultural_object_inquiry(
            n,inspected,"world:inspected")[0]
        for field,value in [("speaker_ref","invented_person"),
                            ("demonstration_ref","invented_episode"),
                            ("object_ref","artifact:invented"),
                            ("hypothesis","INNATE_FLUENT_LANGUAGE")]:
            bad=dict(proposal);bad[field]=value
            with self.assertRaises(InvalidDevelopment):
                admit(n,inspected,"world:inspected",[bad])
            self.assertEqual(n["cultural_reference_practices"],[])

    def test_later_failed_personal_inquiry_can_suspend_but_not_erase_history(self):
        n=newborn("nadia","Nadia");w=world_with_object();w["clock"]=1
        seen=heard_experience(n,w)
        conserve_personally_heard_reference(n,seen,"world:speech",w)
        own=inspected_experience(n,w,2)
        admit(n,own,"world:inspect",possible_cultural_object_inquiry(
            n,own,"world:inspect"))
        failed={"actor":"nadia","clock":3,"ref":"private:failed",
                "own_action":"INSPECT","status":"PARTIAL",
                "felt_enactment":{"attempted_operation":"INSPECT",
                                  "objective_result_not_inferred":True},
                "participated":True,"perceived_cues":[],
                "own_practical_selection":{"world_request":{
                    "operation":"INSPECT","material_object_ref":"artifact:a"}}}
        revisions=possible_reference_revision(
            n,failed,"world:lost_object")
        self.assertEqual(len(revisions),1)
        admit(n,failed,"world:lost_object",revisions)
        row=n["cultural_reference_practices"][0]
        self.assertEqual(row["status"],
                         "SUSPENDED_AFTER_FAILED_OBJECT_INQUIRY")
        self.assertEqual(row["source_event_refs"],
                         ["world:speech","world:inspect"])
        self.assertEqual(len(row["revisions"]),1)


class JoinedNadiaWorld(unittest.TestCase):
    def test_father_actual_object_production_speech_nadia_personal_inspection(self):
        with tempfile.TemporaryDirectory() as directory:
            rt=ConstitutiveRuntime(str(Path(directory)/"culture.sqlite"))
            try:
                rt.initialize([
                    ("father","Father",SEED),("mother","Mother",SEED)])
                made=rt.step("father",requested_action="MAKE_OBJECT")
                self.assertEqual(made["status"],"PERFORMED")
                world=rt.ledger.world("w1")[1]
                self.assertEqual(len(world["material_objects"]),1)
                obj=next(iter(world["material_objects"]))
                said=rt.step("father",requested_action="SPEAK",object_ref=obj)
                self.assertEqual(said["status"],"PERFORMED")
                after_speech=rt.snapshot("nadia")
                self.assertEqual(len(after_speech["cultural_demonstrations"]),1)
                self.assertEqual(after_speech["cultural_reference_practices"],[])
                self.assertEqual(after_speech["body"]["language"],0.)
                proposal=rt.situated("nadia")
                inspect=[x for x in proposal["candidate_actions"]
                         if x["action"]=="INSPECT"]
                self.assertEqual(len(inspect),1)
                practice_options=[x for x in inspect[0]["practical_alternatives"]
                    if x.get("grounds_status")==(
                        "UNTESTED_PERSONALLY_HEARD_PUBLIC_OBJECT_REFERENCE")]
                self.assertEqual(len(practice_options),1)
                self.assertEqual(practice_options[0]["world_request"][
                    "material_object_ref"],obj)
                # Unlike a researcher-forced INSPECT, Nadia's subsequent
                # operation is now chosen by HER situated actor policy
                # because she personally heard this speaker/thing relation.
                inspected=rt.step("nadia")
                self.assertEqual(inspected["attempt"],"INSPECT")
                self.assertEqual(inspected["status"],"PERFORMED")
                self.assertEqual(inspected["selection_grade"],
                                 "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
                after=rt.snapshot("nadia")
                self.assertEqual(len(after["cultural_reference_practices"]),1)
                self.assertEqual(after["cultural_reference_practices"][0][
                    "object_ref"],obj)
                self.assertEqual(world["material_objects"][obj]["owner"],"father")
                self.assertTrue(rt.verify()["valid"])
            finally:
                rt.close()

    def test_unspoken_artifact_does_not_create_nadia_cultural_references(self):
        with tempfile.TemporaryDirectory() as directory:
            rt=ConstitutiveRuntime(str(Path(directory)/"no_speech.sqlite"))
            try:
                rt.initialize([
                    ("father","Father",SEED),("mother","Mother",SEED)])
                made=rt.step("father",requested_action="MAKE_OBJECT")
                self.assertEqual(made["status"],"PERFORMED")
                obj=next(iter(rt.ledger.world("w1")[1]["material_objects"]))
                rt.step("father",requested_action="REST")
                rt.step("nadia",requested_action="INSPECT",object_ref=obj)
                self.assertEqual(rt.snapshot("nadia")[
                    "cultural_reference_practices"],[])
                self.assertEqual(rt.snapshot("nadia")[
                    "cultural_demonstrations"],[])
                self.assertTrue(rt.verify()["valid"])
            finally:rt.close()

if __name__=="__main__":
    unittest.main()
