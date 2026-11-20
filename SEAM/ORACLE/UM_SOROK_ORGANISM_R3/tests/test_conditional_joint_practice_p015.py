"""SORACLE P015 — conditional joint practice is acquired, not counted into love."""
import unittest
from um_sorok_organism.types import newborn,blank_world,AccessibleEncounter
from um_sorok_organism.distributed_power import (
    record_actor_participation,conditional_assistance_options,
    choose_uncompelled_assistance)
from um_sorok_organism.joint_practice_genesis import possible_joint_practice
from um_sorok_organism.development import admit,InvalidDevelopment
from um_sorok_organism.constitution import materialize

def participate(actor,event,*,status,partner=None,operation="SIGNAL"):
    experience={
        "actor":actor["id"],"ref":"experience:"+event,
        "clock":int(event.replace("event","")),
        "location":"home","own_action":operation,
        "status":status,"participated":True,
        "felt_enactment":{"attempted_operation":operation,
                          "objective_result_not_inferred":True},
        "perceived_cues":[{"id":"witness:"+event,
                           "kind":"performed_signal",
                           "tags":["signal","response"],
                           "source_actor":actor["id"]}],
        "reciprocated_partner":partner
    }
    record_actor_participation(actor,experience,None,"world:"+event)
    return experience

class SourceQualifiedJointPractice(unittest.TestCase):
    def test_unfinished_then_independent_joint_event_acquires_conditional_practice(self):
        child=newborn("nadia","Nadia")
        participate(child,"event1",status="PARTIAL")
        later=participate(child,"event2",status="PERFORMED",partner="father")
        candidate=possible_joint_practice(child,later,"world:event2")
        self.assertEqual(len(candidate),1)
        result=admit(child,later,"world:event2",candidate)
        self.assertEqual(result[0]["status"],
                         "ADMITTED_CONDITIONAL_PRACTICE_NOT_FORCED_JOINT_SUCCESS")
        self.assertEqual(len(child["joint_practices"]),1)
        self.assertEqual(child["joint_practices"][0]["coactor_ref"],"father")
        self.assertTrue(child["joint_practices"][0][
            "inhibition_and_other_future_refusal_still_possible"])
        self.assertEqual(child["self_model"],{})
        self.assertEqual(child["projects"],[])
        self.assertEqual(child["other_models"],{})

    def test_repetition_alone_does_not_produce_new_joint_competence(self):
        child=newborn("nadia","Nadia")
        participate(child,"event1",status="PERFORMED",partner="father")
        later=participate(child,"event2",status="PERFORMED",partner="father")
        self.assertEqual(possible_joint_practice(
            child,later,"world:event2"),[])
        self.assertEqual(child["joint_practices"],[])

    def test_acquired_practice_discriminates_one_of_two_actual_others(self):
        child=newborn("nadia","Nadia")
        participate(child,"event1",status="PARTIAL")
        father=participate(child,"event2",status="PERFORMED",partner="father")
        admit(child,father,"world:event2",
              possible_joint_practice(child,father,"world:event2"))
        # Mother can also have participated, but there was no differentiated
        # unfinished->successful developmental acquisition with *her*.
        participate(child,"event3",status="PERFORMED",partner="mother")
        child["body"]["comfort"]=.3
        world=blank_world()
        world["positions"][child["id"]]="home"
        constitution=materialize(child,world)
        access=AccessibleEncounter(
            actor="nadia",world_clock=world["clock"],location="home",
            cues=[{"kind":"coactor_present","source_actor":"father"},
                  {"kind":"coactor_present","source_actor":"mother"}],
            affordances=["SIGNAL"],access_receipts=[])
        candidates=conditional_assistance_options(
            constitution,access,{"action":"SIGNAL"})
        self.assertEqual(len(candidates),2)
        father_option=next(x for x in candidates
            if x["supporter_actor_ref"]=="father")
        mother_option=next(x for x in candidates
            if x["supporter_actor_ref"]=="mother")
        self.assertEqual(father_option["grounds_status"],
                         "HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE")
        self.assertEqual(mother_option["grounds_status"],
                         "ACTOR_PREVIOUSLY_EXPERIENCED_CONTINGENT_COACTIVITY")
        proposed=choose_uncompelled_assistance(
            [{"action":"SIGNAL","practical_alternatives":candidates}],
            child["body"])
        self.assertEqual(proposed["practical_option_id"],
                         father_option["option_id"])
        self.assertEqual(father_option["partner_consent"],
                         "MUST_BE_INDEPENDENTLY_AUTHORED")
        self.assertNotEqual(proposed["practical_option_id"],
                            mother_option["option_id"])

    def test_absent_other_cannot_be_summoned_by_past_practice(self):
        child=newborn("nadia","Nadia")
        participate(child,"event1",status="PARTIAL")
        present=participate(child,"event2",status="PERFORMED",partner="father")
        admit(child,present,"world:event2",
              possible_joint_practice(child,present,"world:event2"))
        world=blank_world();world["positions"]["nadia"]="home"
        constitution=materialize(child,world)
        access=AccessibleEncounter(actor="nadia",world_clock=0,
            location="home",cues=[],affordances=["SIGNAL"],
            access_receipts=[])
        self.assertEqual(conditional_assistance_options(
            constitution,access,{"action":"SIGNAL"}),[])

    def test_forged_partner_or_first_episode_fails_atomically(self):
        child=newborn("nadia","Nadia")
        participate(child,"event1",status="PARTIAL")
        second=participate(child,"event2",status="PERFORMED",partner="father")
        proposal=possible_joint_practice(child,second,"world:event2")[0]
        bad=dict(proposal);bad["coactor_ref"]="mother"
        before=list(child["joint_practices"])
        with self.assertRaises(InvalidDevelopment):
            admit(child,second,"world:event2",[bad])
        self.assertEqual(child["joint_practices"],before)
        bad=dict(proposal);bad["prior_unfinished_participation_ref"]="forged"
        with self.assertRaises(InvalidDevelopment):
            admit(child,second,"world:event2",[bad])
        self.assertEqual(child["joint_practices"],[])

if __name__=="__main__":
    unittest.main()
