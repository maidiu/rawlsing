#!/usr/bin/env python3
"""Offline scorer-safe sheet, score seal, verification, and explicit later unblinding."""
from __future__ import annotations
import argparse,sys
from collections import Counter,defaultdict
from screen_common import (
    HERE,BLINDED,SCORING,REPORTS,RECEIPTS,RAW,DIMENSIONS,MODELS,IDS,
    read,sha,atomic_new,require,gate,latest,
)
SHEET=SCORING/"BLINDED_SCORES.json"
SEAL=SCORING/"BLINDED_SCORES_SHA256_SEAL.json"

def blinded_ids():
    ids=[f"BLIND-CM-{i:04d}" for i in range(1,61)]
    require({p.name for p in BLINDED.glob("*.json")}==
            {x+".json" for x in ids},"BLIND_BUNDLE_NOT_COMPLETE")
    for id_ in ids:
        bundle=read(BLINDED/(id_+".json"))
        require(set(bundle)=={"blind_id","case_id","candidate_occurrence"} and
                bundle["blind_id"]==id_ and bundle["case_id"] in IDS,
                "BLIND_BUNDLE_INVALID: "+id_)
    return ids

def prepare():
    ids=blinded_ids()
    sheet={"kind":"RFA06C_BLINDED_SCORE_SHEET",
           "rubric":"RFA05_RENDERER_SCORING_RUBRIC_R1_UNCHANGED",
           "observations":[{"blind_id":id_,"substantive_lawful":None,
                "hard_fail_codes":[],"dimensions":{d:None for d in DIMENSIONS},
                "evidence_notes":""} for id_ in ids]}
    atomic_new(SHEET,sheet)
    print("Prepared 60-row blind score sheet. No mapping or provider metadata included.")

def validated_score_sheet():
    blinded_ids()
    require(SHEET.exists(),"BLIND_SCORE_SHEET_MISSING")
    s=read(SHEET)
    require(set(s)=={"kind","rubric","observations"} and
            s["kind"]=="RFA06C_BLINDED_SCORE_SHEET" and
            s["rubric"]=="RFA05_RENDERER_SCORING_RUBRIC_R1_UNCHANGED",
            "SCORE_FILE_METADATA_CHANGED")
    entries=s["observations"]
    require(len(entries)==60 and len({x.get("blind_id") for x in entries})==60,
            "NOT_SIXTY_UNIQUE_BLIND_SCORES")
    expected={f"BLIND-CM-{i:04d}" for i in range(1,61)}
    require({x.get("blind_id") for x in entries}==expected,"BLIND_SCORES_NOT_COMPLETE")
    for x in entries:
        require(set(x)=={"blind_id","substantive_lawful","hard_fail_codes",
                        "dimensions","evidence_notes"},"UNAPPROVED_SCORE_FIELDS")
        require(type(x["substantive_lawful"]) is bool,"UNSCORED_SUBSTANTIVE_LAWFUL")
        require(isinstance(x["hard_fail_codes"],list)
                and all(isinstance(z,str) for z in x["hard_fail_codes"]),
                "INVALID_HARD_FAIL_CODES")
        require(set(x["dimensions"])==set(DIMENSIONS),"MISSING_RUBRIC_DIMENSION")
        require(all(type(z) is int and z in (0,1,2)
                    for z in x["dimensions"].values()),"UNSCORED_RUBRIC_DIMENSION")
        require(isinstance(x["evidence_notes"],str),"INVALID_SCORER_NOTES")
    return s

def seal():
    validated_score_sheet()
    value={"kind":"RFA06C_COMPLETE_BLIND_SCORE_SEAL",
           "score_artifact":"BLINDED_SCORES.json",
           "score_sha256":sha(SHEET.read_bytes()),
           "scored_observations":60}
    atomic_new(SEAL,value)
    print("All 60 blind scores sealed with SHA-256. Unblinding is a separate command.")

def verify_seal():
    validated_score_sheet()
    require(SEAL.is_file(),"NO_SCORE_SEAL: complete and seal scores first")
    s=read(SEAL)
    require(set(s)=={"kind","score_artifact","score_sha256","scored_observations"}
            and s["kind"]=="RFA06C_COMPLETE_BLIND_SCORE_SEAL"
            and s["score_artifact"]=="BLINDED_SCORES.json"
            and s["scored_observations"]==60
            and s["score_sha256"]==sha(SHEET.read_bytes()),
            "BLINDED_SCORE_SEAL_VERIFICATION_FAILED")
    return s

def usage_snapshot(raw):
    usage=raw.get("usage") or {}
    nested=usage.get("output_tokens_details") or {}
    return {"input_tokens":usage.get("input_tokens"),
            "output_tokens":usage.get("output_tokens"),
            "thinking_tokens":nested.get("thinking_tokens"),
            "latency_seconds":raw.get("latency_seconds"),
            "stop_reason":raw.get("stop_reason"),
            "provider_message_id":raw.get("provider_message_id")}

def report():
    seal_record=verify_seal()
    c,r2c,rows,mapping,selected,secondary,*_=gate()
    records={x["blind_id"]:x for x in validated_score_sheet()["observations"]}
    from run_cross_model_court import source_r2_result,collect_opus
    full=inherited_rows(r2c)
    all_opus=collect_opus(c,full)
    old_by_id={x["source_run_id"]:x for x in all_opus}
    groups=defaultdict(list)
    case_rows=[]
    for entry in mapping:
        scored=records[entry["blind_id"]]
        if entry["source_kind"]=="EXISTING_OPUS_R2":
            raw=source_r2_result(entry["source_run_id"])
            diagnostic=old_by_id[entry["source_run_id"]]
            old_status=diagnostic["original_r2_structural_status"]
            corrected_status=diagnostic["corrected_referent_admission_status"]
            corrected_issues=diagnostic["corrected_issues"]
        else:
            raw=latest(entry["source_run_id"])
            require(raw is not None,"MISSING_NEW_RAW_AFTER_SCORE_SEAL")
            old_status=raw["status"]
            corrected_issues=raw["corrected_issues"]
            corrected_status="SCHEMA_VALID" if not corrected_issues and raw["status"]=="SCHEMA_VALID" else raw["status"]
        row={"blind_id":entry["blind_id"],"model":entry["model"],
             "case_id":entry["case_id"],"condition":entry["condition"],
             "source_run_id":entry["source_run_id"],
             "substantive_lawful":scored["substantive_lawful"],
             "scores":scored["dimensions"],"hard_fail_codes":scored["hard_fail_codes"],
             "original_structural_status":old_status,
             "corrected_structural_status":corrected_status,
             "corrected_structural_issues":corrected_issues,
             "provider_usage":usage_snapshot(raw)}
        case_rows.append(row)
        groups[(entry["model"],entry["condition"])].append(row)

    def stats(items):
        passed=sum(x["substantive_lawful"] for x in items)
        hard=Counter(h for x in items for h in x["hard_fail_codes"])
        means={d:round(sum(x["scores"][d] for x in items)/len(items),3) for d in DIMENSIONS}
        valid=sum(x["corrected_structural_status"]=="SCHEMA_VALID" for x in items)
        def total(field):
            vals=[x["provider_usage"][field] for x in items
                  if isinstance(x["provider_usage"].get(field),(int,float))]
            return {"sum":sum(vals),"mean":round(sum(vals)/len(vals),2) if vals else None,
                    "observed_n":len(vals)}
        return {"n":len(items),"substantive_pass":passed,
                "substantive_pass_rate":round(passed/len(items),3),
                "corrected_mechanical_valid":valid,
                "hard_failure_types":dict(sorted(hard.items())),
                "rubric_dimension_means":means,
                "usage":{"input_tokens":total("input_tokens"),
                         "output_tokens":total("output_tokens"),
                         "thinking_tokens":total("thinking_tokens"),
                         "latency_seconds":total("latency_seconds")}}
    overall={}
    for model in c["comparison_model_ids"]:
        combined=groups[(model,"N")]+groups[(model,"WP")]
        overall[model]={"overall":stats(combined),"N":stats(groups[(model,"N")]),
                        "WP":stats(groups[(model,"WP")])}
    secondary_diagnostics=[x for x in all_opus if x["replicate"] in (2,3)]
    secondary_status=Counter(x["corrected_referent_admission_status"] for x in secondary_diagnostics)
    result={"kind":"RFA06C_EXPLICIT_POST_SEAL_UNBLINDED_REPORT",
            "score_seal_sha256":seal_record["score_sha256"],
            "primary_universe_n":60,"per_model_n":20,
            "comparison":overall,"case_rows":case_rows,
            "opus_secondary_replication_n":40,
            "opus_secondary_corrected_mechanical_statuses":dict(secondary_status),
            "interpretation_limitations":[
                "Screen, not a powered model-by-context interaction estimator",
                "Additional 40 Opus observations are secondary only",
                "RFA05B upstream conditions are hand-authored laboratory surrogates",
                "These results do not establish full Rawlsing runtime feasibility",
                "Observed token counts and latency are not invoice-billed dollar amounts",
            ]}
    atomic_new(REPORTS/"UNBLINDED_COMPARISON_REPORT.json",result)
    print("EXPLICIT UNBLIND completed after sealed scoring; report kept local.")

def inherited_rows(r2c):
    from screen_common import inherited
    return inherited.execution_manifest(r2c)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--prepare",action="store_true")
    g.add_argument("--seal",action="store_true")
    g.add_argument("--verify-seal",action="store_true")
    g.add_argument("--unblind",action="store_true")
    args=p.parse_args()
    if args.prepare:prepare()
    if args.seal:seal()
    if args.verify_seal:
        verify_seal();print("Complete frozen score artifact SHA-256 verified.")
    if args.unblind:report()

if __name__=="__main__":
    try:main()
    except (RuntimeError,ValueError,OSError) as exc:
        print("SCORING_COURT_HOLD: "+str(exc),file=sys.stderr)
        sys.exit(2)
