"""SORACLE builder-owned joined longitudinal child-life first consumer.

Executable (when an authorized Python checkout is available):
  python -m um_sorok_organism.joined_longitudinal_demo --directory /tmp/nadia_join

Two materially equal fictional households differ in one historical public
act (father SPEAK about his actual worked object vs father REST). Every
subsequent Nadia step is selected by Nadia's own situated actor policy. Her
acquired practices and continued physiology are world/personal ledgers,
never scripted adult targets. No PYAT-native survey or human-science claim.
"""
import argparse
import json
import tempfile
from pathlib import Path

from .runtime import ConstitutiveRuntime
from .storage import ResearchLedger

PARENT_PACKET={
    "source_ref":"SORACLE_SOURCEFREE_PARENT_EXAMPLE_NOT_EMPIRICAL_PYAT",
    "source_grade":"HYPOTHETICAL_NOT_ORIGINAL_SURVEY_SCIENCE",
    "answers":{"fictional_question_only":"fictional_response_only"},
    "fictional_seed":{"projects":[{
        "object":"practice already-acquired ordinary speech",
        "means":["SPEAK"],"priority":0.2,"cue_terms":["home"],
    }]},
}


def _frozen_child_view(actor):
    return {
        "actor":actor["id"],"role":actor["role"],
        "age_days":actor.get("age_days"),
        "body_language":actor["body"].get("language"),
        "body_language_ceiling":actor["body"].get("language_ceiling"),
        "cultural_demonstration_count":len(
            actor.get("cultural_demonstrations",[])),
        "cultural_practice_refs":[
            {"id":p["id"],"object_ref":p["object_ref"],
             "status":p["status"],"source_event_refs":p["source_event_refs"]}
            for p in actor.get("cultural_reference_practices",[])],
        "social_vocal_practices":len(
            actor.get("vocal_coordination_practices",[])),
        "possible_end_count":len(actor.get("possible_ends",[])),
        "learned_joint_practices":len(actor.get("joint_practices",[])),
        "care_received":len(actor.get("co_regulation_episodes",[])),
        "sources_in_own_history_only":True,
    }


def _path_case(db,*,father_public_speech,days,beats):
    rt=ConstitutiveRuntime(str(db))
    try:
        rt.initialize([
            ("father","Father",PARENT_PACKET),
            ("mother","Mother",PARENT_PACKET),
        ])
        creation=rt.step("father",requested_action="MAKE_OBJECT")
        if creation["status"]!="PERFORMED":
            raise RuntimeError("COUNTERFACTUAL_SOURCE_OBJECT_NOT_MADE")
        objects=rt.ledger.world("w1")[1]["material_objects"]
        if len(objects)!=1:
            raise RuntimeError("COUNTERFACTUAL_SOURCE_OBJECT_NOT_UNIQUE")
        object_id=next(iter(objects))
        if father_public_speech:
            source=rt.step("father",requested_action="SPEAK",
                           object_ref=object_id)
        else:
            source=rt.step("father",requested_action="REST")
        if source["status"]!="PERFORMED":
            raise RuntimeError("COUNTERFACTUAL_SOURCE_ACT_NOT_PERFORMED")
        before=rt.ledger.actor("nadia")[1]
        # NEVER request this child's act; adult first activity is a
        # deliberately different WORLD history, not child adult destiny.
        own=rt.step("nadia")
        after_own=rt.ledger.actor("nadia")[1]
        if days:
            rt.background(days,processes=[])
        continuation=rt.continue_without_user(beats=beats) if beats else {
            "beats_requested":0,"beats_committed":0,"events":[]}
        final=rt.ledger.actor("nadia")[1]
        world=rt.ledger.world("w1")[1]
        in_process_verify=rt.verify()
        if in_process_verify.get("valid") is not True:
            raise RuntimeError("JOINED_SOURCEFREE_LEDGER_NOT_VERIFIED")
        record={
            "sourcefree_world_branch":(
                "FATHER_PUBLIC_OBJECT_SPEECH" if father_public_speech
                else "FATHER_REST_SAME_MATERIAL_OBJECT"),
            "world_object_ref":object_id,
            "world_object_owner":objects[object_id]["owner"],
            "father_source_action":source["attempt"],
            "actor_selected_nadia_action":own["attempt"],
            "actor_selected_nadia_status":own["status"],
            "early_nadia_before":_frozen_child_view(before),
            "early_nadia_after":_frozen_child_view(after_own),
            "later_nadia":_frozen_child_view(final),
            "independent_beats_requested":beats,
            "independent_beats_reported":continuation["beats_committed"],
            "world_clock":world["clock"],
            "world_integrity":in_process_verify,
            "full_actor_world_sources_not_exposed_to_child":True,
        }
    finally:
        rt.close()
    cold=ResearchLedger(str(db))
    try:
        receipt=cold.verify_chain()
        if receipt.get("valid") is not True:
            raise RuntimeError("JOINED_COLD_SQLITE_LEDGER_NOT_VERIFIED")
        record["cold_integrity"]=receipt
        record["cold_nadia"]=_frozen_child_view(cold.actor("nadia")[1])
        if record["cold_nadia"]!=record["later_nadia"]:
            raise RuntimeError("COLD_REOPEN_PSYCHE_NOT_PRESERVED")
    finally:
        cold.close()
    return record


def run_counterfactual(directory,*,days=14,beats=12):
    if type(days) is not int or days<0 or days>3650:
        raise ValueError("INVALID_SOURCEFREE_DAYS")
    if type(beats) is not int or beats<0 or beats>24:
        raise ValueError("INVALID_INDEPENDENT_BEATS")
    target=Path(directory)
    target.mkdir(parents=True,exist_ok=True)
    speech=_path_case(target/"speaking.sqlite3",
                      father_public_speech=True,days=days,beats=beats)
    unspoken=_path_case(target/"silent.sqlite3",
                        father_public_speech=False,days=days,beats=beats)
    early_differ=(
        speech["early_nadia_after"]["cultural_practice_refs"] !=
        unspoken["early_nadia_after"]["cultural_practice_refs"])
    if (not early_differ or
        len(speech["early_nadia_after"]["cultural_practice_refs"])!=1 or
        len(unspoken["early_nadia_after"]["cultural_practice_refs"])!=0):
        raise RuntimeError("NADIA_CULTURAL_HISTORY_NOT_CAUSALLY_DIVERGENT")
    # We do not claim adult convergence/divergence or political enlightenment.
    # This court proves only one real changed acquired capability plus its
    # subsequent source/persistence in continuing, independent actor beats.
    return {
        "grade":"SOURCEFREE_CONSTRUCTIVE_COUNTERFACTUAL_NOT_HUMAN_SCIENCE",
        "implemented_code_executes_if_this_function_returns":True,
        "world_condition_varied":"ACTUAL_PUBLIC_SPEECH_ABOUT_SAME_MATERIAL_OBJECT",
        "nadia_action_not_externally_requested":True,
        "early_historical_cultural_divergence_observed":early_differ,
        "unscripted_adult_destination":True,
        "contrast":{"spoken":speech,"unspoken":unspoken},
        "external_pyat_correspondence":"NOT_ISSUED",
        "native_actor_authority":"NOT_ISSUED",
    }


def main(argv=None):
    parser=argparse.ArgumentParser(
        description="R3×R18 joined two-history sourcefree Nadia life")
    parser.add_argument("--directory",default=None)
    parser.add_argument("--days",type=int,default=14)
    parser.add_argument("--beats",type=int,default=12)
    args=parser.parse_args(argv)
    if args.directory:
        print(json.dumps(run_counterfactual(
            args.directory,days=args.days,beats=args.beats),
            sort_keys=True,indent=2))
    else:
        with tempfile.TemporaryDirectory() as folder:
            print(json.dumps(run_counterfactual(
                folder,days=args.days,beats=args.beats),
                sort_keys=True,indent=2))


if __name__=="__main__":
    main()
