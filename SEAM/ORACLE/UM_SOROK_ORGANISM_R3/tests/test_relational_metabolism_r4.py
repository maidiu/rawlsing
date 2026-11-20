"""R4 sourcefree executable psychological relation-history and world coupling court.

Actual test runs, when performed, MUST report the exact tested Git SHA.
A sourcefree passed court never issues clinical science, CAN/ADP, or personhood.
"""
from dataclasses import asdict

import unittest

from um_sorok_organism.types import (
    AccessibleEncounter, Constitution, newborn, adult, copy,
)
from um_sorok_organism.constitution import compose
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.relational_metabolism import (
    validate_motif, link_ref, InvalidRelationalMotif,
)
from um_sorok_organism.parents import construct_parent
from um_sorok_organism.semantics import ValidatingSemanticService
from um_sorok_organism.runtime import ConstitutiveRuntime


def _f(fid, action, tags, tendency=None):
    return {
        "id": fid, "actor": "mother", "kind": "RELATIONAL_INVESTMENT",
        "origin": ["fictional_init:mother"], "grade": "SOURCEFREE_RESEARCH_PROVISIONAL",
        "cues": list(tags), "enables": [action], "scope": {},
        "lifecycle": "ACTIVE", "strength": .65, "body_min": .1,
        "access": "tacit", "tendencies": [tendency] if tendency else [],
    }


def _motif():
    return {
        "id": "moralized-care", "source_forms": ["care", "authority"],
        "cue_terms": ["rebuke"], "locations": ["home"],
        "origin": ["fictional_init:mother"], "status": "ACTIVE",
        "effects": [
            {"kind": "RELATION_MEDIATION", "source": "care",
             "target": "authority", "relation": "SUBORDINATES"},
            {"kind": "ACTION_CURRENT", "action": "IMPOSE", "polarity": "APPROACH"},
        ],
    }


def _constitution(suppress=False, withhold=False, motif=True):
    forms={
        "care": _f("care", "CARE", ["community", "rebuke"]),
        "authority": _f("authority", "IMPOSE", ["community", "rebuke"],
            {"action": "IMPOSE", "polarity": "WITHHOLD", "cue_terms": ["rebuke"]}
            if withhold else None),
    }
    links=[{"source": "authority", "target": "care", "relation": "INHIBITS",
            "contexts": ["home"], "origin": ["past-rebuke"]}] if suppress else []
    a=adult("mother", "Mother")
    return Constitution(
        actor="mother", clock=0, body=a["body"], forms=forms, links=links,
        projects=[], activity_links=[], composition_methods=[], memories=[],
        traces=[], other_models={}, self_model={}, relations=[], unknowns=[],
        relational_motifs=[_motif()] if motif else [],
    )


def _access(tags=("community", "rebuke")):
    return AccessibleEncounter(
        "mother", 0, "home", [{
            "id": "world:cue", "kind": "speech", "tags": list(tags),
            "source_actor": "pastor", "location": "home",
        }], [], ["world:cue"],
    )


def _situated(suppress=False, withhold=False, tags=("community", "rebuke")):
    c=_constitution(suppress=suppress, withhold=withhold)
    return compose(c,_access(tags))


def _actual_experience():
    return {
        "actor":"mother", "ref":"lived:mother:event-1",
        "participated":True, "perceived_cues":[{"id":"cue:public-rebuke"}],
        "status":"OBSERVED", "own_action":None,
    }



class RelationalMetabolismR4(unittest.TestCase):
    def test_moralized_care_is_a_historically_acquired_action_current_not_trait(self):
        p=_situated()
        self.assertTrue(any(x["kind"]=="ACQUIRED_PERSONAL_SENSE_MEDIATION" and
                   x["relation"]=="SUBORDINATES" for x in p.currents))
        self.assertTrue(any(x["kind"]=="RELATIONALLY_MEDIATED_ACTION_CURRENT" and
                   x["action"]=="IMPOSE" and x["polarity"]=="APPROACH"
                   for x in p.currents))
        options={x["action"]:x for x in p.candidate_actions}
        self.assertTrue(options["IMPOSE"]["psychodynamic_status"]==(
            "ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT"))
        self.assertTrue("moralized-care" in p.readset)


    def test_inhibited_care_still_mediates_authority_without_restored_care_action(self):
        p=_situated(suppress=True)
        self.assertTrue("care" in p.inhibited)
        self.assertTrue("care" not in {x["id"] for x in p.recruited})
        self.assertTrue("CARE" not in {x["action"] for x in p.candidate_actions})
        self.assertTrue(any(x["kind"]=="INDIRECT_INHIBITED_RELATION" and
                   x["target_form_ref"]=="care" for x in p.currents))
        self.assertTrue(any(x["kind"]=="ACQUIRED_RELATIONAL_CONFIGURATION" and
                   "care" in x["inhibited_source_refs"] for x in p.currents))
        self.assertTrue(any(x["kind"]=="RELATIONALLY_MEDIATED_ACTION_CURRENT" and
                   x["has_inhibited_source"] for x in p.currents))
        self.assertTrue("care" in p.readset)


    def test_an_opposed_learned_current_survives_relational_mediation(self):
        p=_situated(withhold=True)
        a=next(x for x in p.candidate_actions if x["action"]=="IMPOSE")
        self.assertTrue(a["psychodynamic_status"]=="UNRESOLVED_CONTRADICTION")
        self.assertTrue("authority" in a["opposed_currents"]["withhold"])
        self.assertTrue("motif:moralized-care" in a["opposed_currents"]["approach"])
        self.assertTrue(any(x["action"]=="IMPOSE" for x in p.antagonisms))


    def test_institutional_genre_cue_is_conditional_not_magic(self):
        p=_situated(tags=("community",))
        self.assertTrue(not any(x["kind"]=="RELATIONALLY_MEDIATED_ACTION_CURRENT"
                       for x in p.currents))
        self.assertTrue(not any(x["kind"]=="ACQUIRED_RELATIONAL_CONFIGURATION"
                       for x in p.currents))
        self.assertTrue("IMPOSE" in {x["action"] for x in p.candidate_actions})


    def test_new_motif_does_not_mutate_its_read_model_or_world(self):
        c=_constitution()
        before=copy(asdict(c))
        p=compose(c,_access())
        self.assertTrue(asdict(c)==before)
        self.assertTrue("moralized-care" in p.readset)


    def test_new_historied_motif_admitted_and_recruited_next_encounter(self):
        actor=adult("mother","Mother")
        actor["forms"]={
            "care":_f("care","CARE",["rebuke"]),
            "authority":_f("authority","IMPOSE",["rebuke"]),
        }
        candidate={"kind":"ACQUIRE_RELATIONAL_MOTIF", "motif": {
            "source_forms":["care","authority"],"cue_terms":["rebuke"],
            "locations":["home"],
            "effects":[{"kind":"ACTION_CURRENT","action":"IMPOSE",
                        "polarity":"APPROACH"}],
        }}
        report=admit(actor,_actual_experience(),"objective:event-1",[candidate])
        self.assertTrue(report[0]["status"]=="ADMITTED_SOURCEFREE_RELATIONAL_FORMATION")
        self.assertTrue(actor["relational_motifs"][0]["origin"]==["objective:event-1"])
        c=_constitution(motif=False)
        c.relational_motifs=copy(actor["relational_motifs"])
        p=compose(c,_access())
        self.assertTrue("IMPOSE" in {x["action"] for x in p.candidate_actions})
        self.assertTrue(any(x["kind"]=="RELATIONALLY_MEDIATED_ACTION_CURRENT" for x in p.currents))


    def test_revalue_relation_preserves_its_earlier_meaning_and_stable_ref(self):
        a=adult("mother","Mother")
        a["forms"]={"care":_f("care","CARE",["rebuke"]),
                    "authority":_f("authority","IMPOSE",["rebuke"])}
        link={"source":"care","target":"authority","relation":"SUPPORTS",
              "contexts":["home"],"origin":["former-coactivity"]}
        a["links"]=[link]
        ident=link_ref(link)
        result=admit(a,_actual_experience(),"objective:disillusionment",[
            {"kind":"REVALUE_RELATION","relation_id":ident,
             "new_relation":"CONFLICTS_WITH"},
        ])
        self.assertTrue(result[0]["status"]=="ADMITTED_SOURCEFREE_RELATIONAL_REVALUATION")
        self.assertTrue(a["links"][0]["id"]==ident)
        self.assertTrue(a["links"][0]["relation"]=="CONFLICTS_WITH")
        self.assertTrue(a["links"][0]["relational_history"][0]["relation"]=="SUPPORTS")
        self.assertTrue(a["links"][0]["relational_history"][0]["event"]=="objective:disillusionment")


    def test_reorganization_preserves_old_configuration_in_own_history(self):
        a=adult("mother","Mother")
        a["forms"]={"care":_f("care","CARE",["rebuke"]),
                    "authority":_f("authority","IMPOSE",["rebuke"])}
        a["relational_motifs"]=[_motif()]
        admit(a,_actual_experience(),"objective:changed-setting",[
            {"kind":"REORGANIZE_RELATIONAL_MOTIF","motif_id":"moralized-care",
             "status":"DORMANT","cue_terms":["public-exclusion"]},
        ])
        x=a["relational_motifs"][0]
        self.assertTrue(x["status"]=="DORMANT")
        self.assertTrue(x["motif_history"][0]["previous"]["status"]=="ACTIVE")
        self.assertTrue(x["motif_history"][0]["previous"]["cue_terms"]==["rebuke"])
        self.assertTrue(x["motif_history"][0]["experience_ref"]==_actual_experience()["ref"])


    def test_unqualified_motif_or_late_invalid_proposal_rolls_back_entire_actor(self):
        a=adult("mother","Mother")
        a["forms"]={"care":_f("care","CARE",["rebuke"]),
                    "authority":_f("authority","IMPOSE",["rebuke"])}
        before=copy(a)
        with self.assertRaises(InvalidDevelopment):
            admit(a,_actual_experience(),"objective:1",[
                {"kind":"ACQUIRE_RELATIONAL_MOTIF", "motif":{
                    "source_forms":["care","authority"],
                    "effects":[{"kind":"ACTION_CURRENT","action":"IMPOSE",
                                "polarity":"APPROACH"}],
                }},
                {"kind":"REVALUE_RELATION","relation_id":"forged",
                 "new_relation":"SUPPORTS"},
            ])
        self.assertTrue(a==before)
        with self.assertRaises(InvalidRelationalMotif):
            validate_motif({"source_forms":["care","unknown"],
                            "effects":[{"kind":"ACTION_CURRENT","action":"CARE",
                                        "polarity":"APPROACH"}]},a["forms"])


    def test_fictional_parent_explicit_motif_not_survey_imputation(self):
        packet={
            "answers":{"question_1":"answer_1"},
            "fictional_seed":{
                "acquired_forms":[
                    {"kind":"RELATIONAL_INVESTMENT","content":"care for others",
                     "cues":["rebuke"],"enables":["CARE"]},
                    {"kind":"MEDIATOR","content":"pastoral authority recognition",
                     "cues":["rebuke"],"enables":["IMPOSE"]},
                ],
                "relational_motifs":[{
                    "source_indices":[0,1],"cue_terms":["rebuke"],
                    "effects":[
                        {"kind":"RELATION_MEDIATION","source_index":0,
                         "target_index":1,"relation":"SUBORDINATES"},
                        {"kind":"ACTION_CURRENT","action":"IMPOSE",
                         "polarity":"APPROACH"},
                    ],
                }]
            },
        }
        x=construct_parent("mother","Mother",packet,ValidatingSemanticService())
        self.assertTrue(len(x["relational_motifs"])==1)
        m=x["relational_motifs"][0]
        self.assertTrue(m["not_respondent_unconscious_truth"] is True)
        self.assertTrue(all(s in x["forms"] for s in m["source_forms"]))
        self.assertTrue(x["initialization"]["questionnaire_as_live_behavior"]==(
            "UNPROVEN_WITHOUT_BLIND_SURVEY_RECONSTRUCTION"))


    def test_runtime_private_pre_event_metabolism_is_not_public_expression(tmp_path):
        packet={
            "answers":{"Q":"some answer"},
            "fictional_seed":{
                "acquired_forms":[
                    {"kind":"RELATIONAL_INVESTMENT","cues":["rebuke"],
                     "enables":["CARE"],"content":"care"},
                    {"kind":"MEDIATOR","cues":["rebuke"],
                     "enables":["IMPOSE"],"content":"authority"},
                ],
                "relational_motifs":[{
                    "source_indices":[0,1],"cue_terms":["rebuke"],
                    "effects":[{"kind":"ACTION_CURRENT","action":"IMPOSE",
                                "polarity":"APPROACH"}],
                }],
            },
        }
        rt=ConstitutiveRuntime(tmp_path/"person.db")
        try:
            rt.initialize([("mother","Mother",packet)])
            rt.cue(kind="public_rebuke",tags=["rebuke"],location="home")
            view=rt.situated("mother")
            self.assertTrue(any(x["kind"]=="RELATIONALLY_MEDIATED_ACTION_CURRENT"
                       for x in view["currents"]))
            step=rt.step("mother",requested_action="REST")
            self.assertTrue("private_pre_event_psychodynamics" not in step)
            event=rt.ledger.events()[-1]
            envelope=event["envelope"]
            serialized=str(envelope)
            self.assertTrue("private_pre_event_psychodynamics" in serialized)
            self.assertTrue("ACQUIRED_RELATIONAL_CONFIGURATION" in serialized)
            self.assertTrue("SOURCEFREE_RESEARCH_PROVISIONAL" in serialized)
            self.assertTrue(rt.verify())
        finally:
            rt.close()
