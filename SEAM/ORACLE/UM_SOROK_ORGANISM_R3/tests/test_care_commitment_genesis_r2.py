"""SORACLE P006/P015 R2 — caregiver-side practical commitment first consumer.

Two independently actor-selected costly actions by a caregiver are historical
work, not proof of love. A named recipient reappears as a practical target
only when actually present and bodily action feasible. The world still owns
material outcome and the recipient's independent development.
"""
import copy
import unittest
from um_sorok_organism.types import adult,newborn,Attempt,blank_world,AccessibleEncounter
from um_sorok_organism.care_commitment_genesis import (
    conserve_costly_offered_care,candidate_care_commitment,
    practiced_care_alternatives)
from um_sorok_organism.development import admit,InvalidDevelopment
from um_sorok_organism.constitution import materialize

CHOSEN="ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE"


def experience(actor,when,who="nadia",kind="CARE"):
    return {
        "actor":actor["id"],"ref":"experienced:care:"+str(when),
        "clock":when,"location":"home","own_action":kind,
        "status":"PERFORMED","participated":True,
        "felt_enactment":{"attempted_operation":kind,
                          "objective_result_not_inferred":True},
        "perceived_cues":[{"id":"presence:"+who+":"+str(when),
            "kind":"coactor_present","source_actor":who,
            "tags":["coactor",who]}]
    }


def record(actor,when,who="nadia",kind="CARE",
           chosen=CHOSEN,as_coactor=False,cost=.15):
    before=copy.deepcopy(actor["body"])
    after=dict(before);after["rest"]-=cost
    actual=Attempt(actor=actor["id"],action=kind,target=who,
                   intention=chosen)
    summary=({"actor":who,"action":"SIGNAL",
              "coactor":actor["id"],"coactor_action":kind,
              "outcome":"JOINT_ACTIVITY_PERFORMED","status":"PERFORMED"}
             if as_coactor else
             {"actor":actor["id"],"action":kind,"target":who,
              "outcome":"CARE_GIVEN","status":"PERFORMED"})
    exp=experience(actor,when,who,kind)
    result=conserve_costly_offered_care(
        actor,exp,"world:"+str(when),actual,
        summary,before,after)
    return exp,result


class HistoricallyPracticedCare(unittest.TestCase):
    def test_two_real_actor_chosen_costly_care_events_form_future_named_possibility(self):
        mom=adult("mother","Mother")
        first,one=record(mom,1)
        later,two=record(mom,2)
        self.assertIsNotNone(one)
        self.assertIsNotNone(two)
        possibility=candidate_care_commitment(mom,later,"world:2")
        self.assertEqual(len(possibility),1)
        result=admit(mom,later,"world:2",possibility)
        self.assertEqual(result[0]["status"],
                         "ADMITTED_PRACTICED_CARE_NOT_UNCONDITIONAL_LOVE")
        self.assertEqual(len(mom["care_practical_commitments"]),1)
        self.assertFalse("love" in str(mom["self_model"]).lower())
        self.assertEqual(mom["projects"],[])
        world=blank_world();world["clock"]=2
        world["positions"]={"mother":"home","nadia":"home"}
        view=materialize(mom,world)
        access=AccessibleEncounter(actor="mother",world_clock=2,
            location="home",cues=[{"kind":"coactor_present",
                                  "source_actor":"nadia"}],
            affordances=["CARE"],access_receipts=[])
        options=practiced_care_alternatives(view,access,{"action":"CARE"})
        self.assertEqual(len(options),1)
        self.assertEqual(options[0]["world_request"][
            "addressed_party_ref"],"nadia")
        self.assertEqual(options[0]["future_sufficient_bodily_material_resources"],
                         "WORLD_MUST_CHECK")
        no_child=AccessibleEncounter(actor="mother",world_clock=2,
            location="home",cues=[],affordances=["CARE"],access_receipts=[])
        self.assertFalse(practiced_care_alternatives(
            view,no_child,{"action":"CARE"}))

    def test_injected_research_care_cannot_be_mislabeled_independent_care_investment(self):
        mom=adult("mother","Mother")
        for when in (1,2):
            _,result=record(mom,when,chosen="INJECTED_NOT_NATIVE_ACTOR_CHOICE")
            self.assertIsNone(result)
        self.assertEqual(mom["care_contribution_episodes"],[])
        self.assertEqual(mom["care_practical_commitments"],[])

    def test_an_actual_independent_coactor_response_is_caregiver_labor(self):
        mom=adult("mother","Mother")
        first,_=record(mom,1,as_coactor=True)
        second,receipt=record(mom,2,as_coactor=True)
        self.assertIsNotNone(receipt)
        self.assertEqual(receipt["recipient_ref"],"nadia")
        self.assertEqual(len(candidate_care_commitment(
            mom,second,"world:2")),1)

    def test_missing_recipient_or_cost_does_not_create_love(self):
        mom=adult("mother","Mother")
        record(mom,1,who="nadia")
        two,result=record(mom,2,who="other")
        self.assertIsNotNone(result)
        self.assertEqual(candidate_care_commitment(
            mom,two,"world:2"),[])
        three,result=record(mom,3,who="nadia",cost=0)
        self.assertIsNone(result)
        self.assertEqual(candidate_care_commitment(
            mom,three,"world:3"),[])

    def test_forged_other_ref_is_rejected_atomically(self):
        mom=adult("mother","Mother")
        record(mom,1)
        second,_=record(mom,2)
        offered=candidate_care_commitment(mom,second,"world:2")[0]
        bad=dict(offered);bad["recipient_ref"]="unknown"
        with self.assertRaises(InvalidDevelopment):
            admit(mom,second,"world:2",[bad])
        self.assertEqual(mom["care_practical_commitments"],[])


if __name__=="__main__":
    unittest.main()
