#!/usr/bin/env python3
"""Entirely offline RFA-06C admission and cross-model screen validator."""
from __future__ import annotations
import argparse,sys
from screen_common import (
    HERE,RAW,BLINDED,RECEIPTS,SCORING,FREEZE,IDS,MODELS,
    read,require,gate,raw_evidence,latest,freeze_fingerprints,require_freeze,
    exact_packet,compile_grounding,review_candidate,inherited,
)

def specimen(case_id,kind,refs,effects=None):
    return {"kind":"MODEL_CANDIDATE_NOT_ADMITTED","fixture_id":case_id,
        "hand_authored_experiment":"RFA05_SURROGATE_INPUT_NOT_V3",
        "atoms":[{"atom_id":"a1","kind":kind,"relative_ms":0,"actor":"NADIA",
                  "content":"observable action","referent_ids":refs}],
        "realization_prose":"","world_effect_proposals":effects or [],
        "materialization_requests":[],"no_occurrence_assertion":True}

def admission_regressions():
    """Derive all positive/negative tests from the 10 inherited input pairs."""
    physical_counts=0
    semantic_counts=0
    for case_id in IDS:
        for arm in ("N","WP"):
            packet,_=exact_packet(case_id,arm)
            allowed=compile_grounding(packet)
            require("NADIA" in allowed and "P0" in allowed,"MISSING_ACTOR_PARTICIPANT")
            scene={ref for ref,meta in allowed.items() if meta["physical"]}
            require(bool(scene),"MISSING_SCENE_REFERENTS")
            for ref,meta in allowed.items():
                trial=specimen(case_id,"PAUSE",[ref])
                result=review_candidate(trial,case_id,packet,inherited.deterministic_candidate)
                require(not result["corrected_issues"],
                        f"ROOTED_REFERENCE_REJECTED {case_id}_{arm}: {ref}")
                if meta["physical"]:physical_counts+=1
                else:semantic_counts+=1
            for disallowed in ("W09","W10","W11","H999","ZZ999","R99B","RF009",
                               "objective_truth_register","evaluator_only_oracle"):
                if disallowed not in allowed:
                    result=review_candidate(specimen(case_id,"PAUSE",[disallowed]),case_id,
                                            packet,inherited.deterministic_candidate)
                    require("UNKNOWN_OR_UNAUTHORIZED_ATOM_REFERENT" in result["corrected_issues"],
                            f"UNAUTHORIZED_REFERENCE_ACCEPTED: {case_id} {disallowed}")
            history=next((id_ for id_,meta in allowed.items()
                          if meta["class"]!="PHYSICAL_SCENE_REFERENT"
                          and meta["class"]!="ACTOR_OR_PARTICIPANT_REFERENT"),"NADIA")
            no_object=review_candidate(specimen(case_id,"OBJECT_ACTION",[history]),case_id,packet,
                                        inherited.deterministic_candidate)
            require("OBJECT_ACTION_WITHOUT_DOCUMENTED_PHYSICAL_TARGET" in
                    no_object["corrected_issues"],"NONPHYSICAL_OBJECT_ACTION_ACCEPTED")
            with_object=review_candidate(specimen(case_id,"OBJECT_ACTION",[sorted(scene)[0]]),
                                          case_id,packet,inherited.deterministic_candidate)
            require(not with_object["corrected_issues"],"DOCUMENTED_OBJECT_ACTION_REJECTED")
            effect=review_candidate(specimen(case_id,"PAUSE",[],
                [{"referent_id":history,"from":"a","to":"b","requires_admission":True}]),
                case_id,packet,inherited.deterministic_candidate)
            require("UNKNOWN_WORLD_EFFECT_REFERENT" in effect["corrected_issues"],
                    "SEMANTIC_ID_GRANTED_PHYSICAL_WORLD_WRITE")
    packet8,_=exact_packet("RF008","WP")
    packet9,_=exact_packet("RF009","WP")
    require("R14B" not in compile_grounding(packet8)
            and "R14B" in compile_grounding(packet9),"BRANCH_PRIVATE_REFERENCE_CROSSED")
    for arm in ("N","WP"):
        packet,_=exact_packet("RF003",arm)
        require("H017" in compile_grounding(packet),"KNOWN_ACTOR_MEMORY_MISSING")
    print(f"TYPED_REFERENCE_REGRESSIONS_PASS: {physical_counts} physical; {semantic_counts} grounded semantic IDs")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--expect-empty",action="store_true")
    ap.add_argument("--require-complete",action="store_true")
    args=ap.parse_args()
    require(not (args.expect_empty and args.require_complete),"CONFLICTING_VALIDATION_MODES")
    c,r2c,rows,mapping,selected,secondary,packets,payloads,transport,schema=gate()
    admission_regressions()
    print("20_INPUT_PACKETS_PRESENT = PASS")
    print("10_WP_N_PAIRS_PRESENT = PASS")
    print("RFA05B_MODEL_PAYLOAD_PARITY = PASS")
    print("TYPED_REFERENT_ALLOWLIST_NO_PROMPT_UNION = PASS")
    print("DOCUMENTED_PHYSICAL_EFFECT_TARGET_ONLY = PASS")
    print("HIDDEN_OR_FOREIGN_REFERENTS_REJECTED = PASS")
    print("MODEL_VISIBLE_R2_REQUEST_PARITY_EXCEPT_MODEL_ID = PASS")
    print("OPUS_PRIMARY_SELECTION_ORDINAL_1 = PASS")
    print("OPUS_PRIMARY_N_20_SECONDARY_N_40 = PASS")
    print("SONNET_PRIMARY_N_20_HAIKU_PRIMARY_N_20 = PASS")
    print("40_NEW_CALLS_FRESHLY_INTERLEAVED = PASS")
    print("60_BALANCED_BLIND_IDS = PASS")
    print("EVALUATOR_IDENTITY_UNEXPOSED = PASS")
    print("API_KEY_NOT_STORED_IN_STATIC_MANIFEST = PASS")
    current=raw_evidence()
    print("NEW_PROVIDER_RESULTS_PRESENT = "+str(len([p for p in current
                    if p.name.startswith("CMRUN-")])))
    if args.expect_empty:
        require(not current and not list(BLINDED.glob("*.json")) and
                not list(RECEIPTS.glob("*.json")) and
                not FREEZE.exists(),"SCREEN_NOT_PRISTINE_BEFORE_FIRST_RUN")
        print("NO_RFA06C_PROVIDER_OUTPUTS = PASS")
    if args.require_complete:
        from run_cross_model_court import smoke_pass,source_r2_result,collect_opus
        assert_fp=freeze_fingerprints(c,r2c,rows,mapping,packets,payloads,transport)
        require_freeze(assert_fp)
        for model in MODELS.values():smoke_pass(c,model)
        for row in rows:
            result=latest(row["run_id"])
            require(result is not None and result.get("requested_model")==row["model"],
                    "NEW_MODEL_PRIMARY_MISSING: "+row["run_id"])
            require(result.get("provider_returned_model")==row["model"]
                    or result.get("status") in ("PERMANENT_PROVIDER_FAILURE","PROVIDER_SCHEMA_FAILURE"),
                    "NEW_MODEL_SUBSTITUTED_OR_UNRESOLVED: "+row["run_id"])
        full=inherited.execution_manifest(r2c)
        for old in full:source_r2_result(old["run_id"])
        require(len(collect_opus(c,full))==60,"OPUS_RECHECK_INCOMPLETE")
        expected={f"BLIND-CM-{i:04d}.json" for i in range(1,61)}
        require({p.name for p in BLINDED.glob("*.json")}==expected,
                "BLIND_BUNDLE_NOT_EXACTLY_60")
        for p in BLINDED.glob("*.json"):
            item=read(p)
            require(set(item)=={"blind_id","case_id","candidate_occurrence"},
                    "BLINDED_BUNDLE_EXPOSES_NONSCORER_INFORMATION")
        require((RECEIPTS/"OPUS_R2_FULL_RECHECK_R1.json").exists(),
                "OPUS_ORIGINAL_AND_CORRECTED_STATUSES_NOT_PERSISTED")
        print("ALL_100_SOURCE_RESPONSES_ACCOUNTED_FOR = PASS")
        print("60_PRIMARY_SCORER_BUNDLES_COMPLETE = PASS")
    print("OFFLINE_CROSS_MODEL_COURT_VALIDATION = PASS")

if __name__=="__main__":
    try:main()
    except (RuntimeError,ValueError,OSError) as exc:
        print("SCREEN_VALIDATION_HOLD: "+str(exc),file=sys.stderr)
        sys.exit(2)
