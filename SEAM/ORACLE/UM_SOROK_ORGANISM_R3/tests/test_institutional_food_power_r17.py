"""SORACLE R17 — material control, encountered procedure, independent collective change.

These are original-repository tests, NOT assertions that SORACLE executed the
entire checked-out suite. Run both normal and optimized under independent
REMONT checkout and pin exact branch HEAD before interpreting results.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.types import blank_world,adult,newborn
from um_sorok_organism.food_access_struggle import (
    configure_food_power, can_draw_shared_food, food_petition_available,
    contribute_food_petition, choose_food_petition)
from um_sorok_organism.material_provisioning import (
    perform_one_actual_feeding,settle_provisioning,PROVISION_KIND)
from um_sorok_organism.world import _effective_material_controller
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.routine_sources import (
    register_sourcefree_period_envelope)
from um_sorok_organism.historical_social_reproduction import (
    qualify_period_allocation)


SOURCEFREE_PARENT={
    "source_ref":"r17_explicit_fictional_not_PYAT",
    "source_grade":"UNQUALIFIED_FICTIONAL_TEST_FIXTURE",
    "answers":{"r17_fictional_survey_observation":"synthetic_condition"},
    "fictional_seed":{"projects":[]}
}


def household():
    w=blank_world()
    actors={
        "mother":adult("mother","Mother"),
        "father":adult("father","Father"),
        "nadia":newborn("nadia","Nadia"),
    }
    for who,actor in actors.items():
        w["positions"][who]="home"
        actor["location"]="home"
        if actor["role"]=="adult":
            actor["projects"]=[{
                "id":"fictional_care_course:"+who,
                "status":"active","means":["CARE","FEED"],
                "object":"ongoing material care"}]
    return w,actors


def declaration():
    return {
        "grade":"EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO",
        "source_ref":"hypothetical_household_food_relation_r17",
        "site":"home","controller_actor":"mother",
        "initially_permitted_givers":["mother"],
        "eligible_petitioners":["father","mother"],
        "quorum":2}


def inspected(actor,notice):
    actor.setdefault("notice_exposures",[]).append({
        "id":"personally_inspected:"+actor["id"],
        "public_notice_ref":notice,
        "public_words_available":[
            "public_petition","household_food","collective_food_access"],
        "actor_comprehension":"NOT_ESTABLISHED"})


def feeding_source(w,a,giver,recipient,days=3):
    source=register_sourcefree_period_envelope(w,a,{
        "kind":PROVISION_KIND,"actor":giver,"location":"home",
        "start_clock":w["clock"],"end_clock":w["clock"]+days,
        "max_hours_per_active_day":2,
        "description":"sourcefree actor/material time conditional "+giver})
    return {
        "kind":PROVISION_KIND,"actor":giver,"recipient":recipient,
        "location":"home","source_ref":source["id"],
        "supply_origin":"SHARED_SITE_FOOD",
        "food_units_per_active_day":1,
        "hours_per_active_day":2,
        "provisional_exposure_fraction":1.0}


class R17ObjectivePower(unittest.TestCase):
    def setUp(self):
        self.world,self.actors=household()
        self.order=configure_food_power(
            self.world,self.actors,declaration())

    def test_material_stock_is_present_but_father_cannot_provide(self):
        before=self.actors["nadia"]["body"]["nutrition"]
        out=perform_one_actual_feeding(
            self.world,self.actors,"father","nadia","home",
            "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
        self.assertEqual(out["status"],"BLOCKED")
        self.assertEqual(out["outcome"],"HOUSEHOLD_FOOD_ACCESS_RESTRICTED")
        self.assertEqual(self.world["sites"]["home"]["food"],12)
        self.assertEqual(self.actors["nadia"]["body"]["nutrition"],before)
        self.assertFalse(can_draw_shared_food(self.world,"father","home"))
        self.assertTrue(can_draw_shared_food(self.world,"mother","home"))
        self.assertFalse(self.world.get("material_feeding_events",[]))

    def test_private_food_right_does_not_become_property_of_pantry(self):
        self.world["holdings"]={"father":{"food":2.0}}
        reply=perform_one_actual_feeding(
            self.world,self.actors,"father","nadia","home",
            "INJECTED_NOT_NATIVE_ACTOR_CHOICE")
        self.assertEqual(reply["status"],"PERFORMED")
        self.assertEqual(self.world["holdings"]["father"]["food"],1)
        self.assertEqual(self.world["sites"]["home"]["food"],12)
        self.assertTrue(self.world["material_feeding_events"][-1][
            "external_action_not_actor_motive"])

    def test_uninspected_procedure_is_not_granted_to_every_adult(self):
        self.assertFalse(food_petition_available(
            self.world,self.actors["father"],"home"))
        attempt=contribute_food_petition(
            self.world,self.actors,"father","home",
            "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
        self.assertEqual(attempt["status"],"BLOCKED")
        self.assertEqual(self.world["institutions"]["household_food_board"][
            "signatures"],[])
        self.assertFalse(can_draw_shared_food(
            self.world,"father","home"))

    def test_injected_signature_does_not_mint_collective_autonomy(self):
        for a in ("mother","father"):
            inspected(self.actors[a],self.order["public_notice_ref"])
        one=contribute_food_petition(
            self.world,self.actors,"father","home",
            "INJECTED_NOT_NATIVE_ACTOR_CHOICE")
        two=contribute_food_petition(
            self.world,self.actors,"mother","home",
            "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
        self.assertEqual(one["status"],"PERFORMED")
        self.assertFalse(one["institutional_rule_change"])
        self.assertEqual(two["independent_signatures"],1)
        self.assertFalse(two["institutional_rule_change"])
        self.assertFalse(can_draw_shared_food(
            self.world,"father","home"))

    def test_distinct_independent_signers_transform_resource_rights(self):
        for a in ("mother","father"):
            inspected(self.actors[a],self.order["public_notice_ref"])
        one=contribute_food_petition(
            self.world,self.actors,"father","home",
            "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
        two=contribute_food_petition(
            self.world,self.actors,"mother","home",
            "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
        self.assertFalse(one["institutional_rule_change"])
        self.assertTrue(two["institutional_rule_change"])
        self.assertEqual(two["independent_signatures"],2)
        self.assertTrue(can_draw_shared_food(
            self.world,"father","home"))
        self.assertTrue(can_draw_shared_food(
            self.world,"nadia","home"))
        self.assertEqual(len(self.world["institutions"][
            "household_food_board"]["rule_history"]),1)
        self.assertEqual(self.actors["nadia"]["self_model"],{})
        out=perform_one_actual_feeding(
            self.world,self.actors,"father","nadia","home",
            "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
        self.assertEqual(out["status"],"PERFORMED")
        self.assertEqual(self.world["sites"]["home"]["food"],11)

    def test_aggregate_food_history_preserves_inaccessible_vs_absent(self):
        p=feeding_source(self.world,self.actors,"father","nadia")
        allocation=qualify_period_allocation(
            self.world,self.actors,[p],0,3)
        before_food=self.world["sites"]["home"]["food"]
        rows=settle_provisioning(
            self.world,self.actors,allocation)
        self.assertEqual(len(rows),1)
        r=rows[0]
        self.assertEqual(r["consumed_food_units"],0)
        self.assertEqual(r["uncovered_food_units"],3)
        self.assertEqual(r["uncovered_due_to_institutional_rights_units"],3)
        self.assertEqual(r["uncovered_due_to_material_shortage_units"],0)
        self.assertTrue(r["physical_stock_was_present_but_inaccessible"])
        self.assertEqual(r["material_status"],"INSTITUTIONAL_RIGHTS_DENIED")
        self.assertEqual(self.world["sites"]["home"]["food"],before_food)

    def test_institutional_entitlements_partition_competing_feeding_claims(self):
        p1=feeding_source(self.world,self.actors,"father","nadia")
        p2=feeding_source(self.world,self.actors,"mother","nadia")
        allocation=qualify_period_allocation(
            self.world,self.actors,[p2,p1],0,3)
        rows=settle_provisioning(
            self.world,self.actors,allocation)
        by_giver={r["giver"]:r for r in rows}
        self.assertEqual(by_giver["father"]["consumed_food_units"],0)
        self.assertEqual(by_giver["mother"]["consumed_food_units"],3)
        self.assertEqual(self.world["sites"]["home"]["food"],9)

    def test_food_title_does_not_grant_title_to_home_work_and_other_sites(self):
        controller,invalid=_effective_material_controller(
            self.world,"home",self.world["sites"]["home"])
        self.assertIsNone(controller)
        self.assertFalse(invalid)
        self.assertTrue(can_draw_shared_food(
            self.world,"father","workshop"))
        self.assertEqual(self.world["sites"]["home"]["stock"],8)
        self.assertEqual(self.world["sites"]["workshop"]["stock"],5)

    def test_false_controller_and_actor_roster_do_not_grant_rights(self):
        with self.assertRaisesRegex(ValueError,"FOOD_POWER_ALREADY_REGISTERED"):
            configure_food_power(self.world,self.actors,declaration())
        self.world["sites"]["home"]["food_access_authority"]="fictional"
        with self.assertRaisesRegex(
                ValueError,"FOOD_POWER_WORLD_AUTHORITY_INCONSISTENT"):
            can_draw_shared_food(self.world,"father","home")


class R17IntegratedLife(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.rt=ConstitutiveRuntime(
            str(Path(self.tmp.name)/"r17_food_power.sqlite3"))
        self.addCleanup(self.rt.close)
        self.rt.initialize([
            ("mother","Mother",SOURCEFREE_PARENT),
            ("father","Father",SOURCEFREE_PARENT)])
        self.order=self.rt.register_sourcefree_food_control(declaration())

    def test_a_real_actor_inspection_enables_politics_but_not_initial_omniscience(self):
        first=self.rt.situated("father")
        self.assertFalse(any(x["action"]=="SIGN_FOOD_PETITION"
                for x in first["candidate_actions"]))
        blocked=self.rt.step(
            "father",requested_action="FEED",target="nadia")
        self.assertEqual(blocked["status"],"BLOCKED")
        self.assertEqual(blocked["objective_outcome"],
                         "HOUSEHOLD_FOOD_ACCESS_RESTRICTED")
        self.assertFalse(self.rt.snapshot("father")["self_model"])
        examined=self.rt.step(
            "father",requested_action="INSPECT",
            object_ref=self.order["public_notice_ref"])
        self.assertEqual(examined["status"],"PERFORMED")
        self.assertEqual(len(self.rt.snapshot("father")[
            "notice_exposures"]),1)
        now=self.rt.situated("father")
        self.assertIn("SIGN_FOOD_PETITION",[
            x["action"] for x in now["candidate_actions"]])

    def test_separate_actor_choices_change_food_rights_for_unsigning_child(self):
        self.rt.step("father",requested_action="FEED",target="nadia")
        self.rt.step("mother",requested_action="FEED",target="nadia")
        for aid in ("father","mother"):
            self.rt.step(aid,requested_action="INSPECT",
                object_ref=self.order["public_notice_ref"])
        father=self.rt.step("father")
        self.assertEqual(father["attempt"],"SIGN_FOOD_PETITION")
        self.assertEqual(father["status"],"PERFORMED")
        self.assertEqual(self.rt.ledger.world("w1")[1]["institutions"][
            "household_food_board"]["food_rights"],"CONTROLLED")
        mother=self.rt.step("mother")
        self.assertEqual(mother["attempt"],"SIGN_FOOD_PETITION")
        self.assertEqual(mother["selection_grade"],
                         "ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE")
        world=self.rt.ledger.world("w1")[1]
        self.assertEqual(world["institutions"]["household_food_board"][
            "food_rights"],"SHARED_BY_COLLECTIVE_ACTS")
        self.assertEqual(len(world["institutions"][
            "household_food_board"]["rule_history"]),1)
        self.assertEqual(self.rt.snapshot("nadia")["self_model"],{})
        before_food=world["sites"]["home"]["food"]
        response=self.rt.step(
            "father",requested_action="FEED",target="nadia")
        self.assertEqual(response["status"],"PERFORMED")
        new_world=self.rt.ledger.world("w1")[1]
        self.assertEqual(new_world["sites"]["home"]["food"],
                         before_food-1)
        self.assertTrue(self.rt.verify()["valid"])

    def test_externally_injected_signatures_do_not_count_as_independent(self):
        for aid in ("father","mother"):
            self.rt.step(aid,requested_action="INSPECT",
                object_ref=self.order["public_notice_ref"])
        a=self.rt.step(
            "father",requested_action="SIGN_FOOD_PETITION")
        b=self.rt.step(
            "mother",requested_action="SIGN_FOOD_PETITION")
        self.assertEqual(a["status"],"PERFORMED")
        self.assertEqual(b["status"],"PERFORMED")
        board=self.rt.ledger.world("w1")[1][
            "institutions"]["household_food_board"]
        self.assertEqual(board["food_rights"],"CONTROLLED")
        self.assertEqual(len(board["signatures"]),2)
        self.assertFalse(any(x[
            "independently_selected_in_research_runtime"]
            for x in board["signatures"]))
        self.assertTrue(self.rt.verify()["valid"])


if __name__=="__main__":
    unittest.main()
