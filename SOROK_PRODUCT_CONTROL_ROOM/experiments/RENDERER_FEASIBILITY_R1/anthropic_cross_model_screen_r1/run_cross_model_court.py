#!/usr/bin/env python3
"""RFA-06C local-only 40-call screening court. Never called by the authoring commission."""
from __future__ import annotations
import argparse, json, sys, time
from jsonschema import Draft202012Validator, ValidationError
from screen_common import (
    HERE, INPUT, RAW, BLINDED, RECEIPTS, FREEZE, MODELS, atomic_new, canonical,
    file_hash, read, sha, utcnow, pkg_version, inherited, require, gate,
    request_for_new, freeze_fingerprints, require_freeze, raw_evidence, latest,
    next_attempt, review_candidate, exact_packet,
)

def find_smoke(c,model):
    return next(x for x in c["model_smokes"] if x["model"]==model)

def smoke_pass(c,model):
    run=find_smoke(c,model)
    record=latest(run["run_id"])
    require(record is not None,f"SMOKE_MISSING_FOR_MODEL: {model}")
    candidate=record.get("structured_candidate")
    require(record.get("status")=="SCHEMA_VALID" and record.get("provider_message_id")
            and record.get("provider_returned_model")==model
            and record.get("requested_model")==model
            and record.get("schema_status")=="EXACT_ORIGINAL_SCHEMA_VALID"
            and isinstance(candidate,dict)
            and candidate.get("fixture_id")==run["case_id"]
            and record.get("provider_schema_fixture_const")==run["case_id"]
            and not record.get("corrected_issues"),
            f"MODEL_SMOKE_HOLD: {model}")
    return True

def new_call(client,run,c,r2c,transport,source_schema):
    import anthropic
    request,packet_name=request_for_new(run,c,r2c,transport)
    request_sha=sha(canonical(request))
    content=request["messages"][0]["content"]
    packet,_=exact_packet(run["case_id"],run["condition"])
    for attempt in range(c["operational_retries"]+1):
        attempt_id=next_attempt(run["run_id"])
        started_at=utcnow();started=time.perf_counter()
        result=None;problem=None
        try:
            result=client.messages.create(**request)
        except (anthropic.APIConnectionError,anthropic.APITimeoutError) as exc:
            problem={"type":type(exc).__name__,"class":"OPERATIONAL_TRANSIENT_NO_CANDIDATE"}
        except anthropic.APIStatusError as exc:
            status=getattr(exc,"status_code",None)
            kind=("OPERATIONAL_TRANSIENT_NO_CANDIDATE"
                  if status==429 or (isinstance(status,int) and 500<=status<=599)
                  else "PROVIDER_SCHEMA_FAILURE" if status==400 else "PERMANENT_PROVIDER_FAILURE")
            problem={"type":type(exc).__name__,"http_status":status,"class":kind}
        except Exception as exc:
            problem={"type":type(exc).__name__,"class":"PERMANENT_PROVIDER_FAILURE"}
        receipt={
            "kind":"RFA06C_PROVIDER_ATTEMPT_NOT_ADMITTED","run_id":run["run_id"],
            "attempt_id":attempt_id,"case_id":run["case_id"],"condition":run["condition"],
            "requested_model":run["model"],"provider_returned_model":None,
            "replicate":run.get("replicate",0),"input_packet_file":packet_name,
            "input_packet_raw_sha256":file_hash(INPUT/packet_name),
            "original_model_payload_sha256":sha(canonical(packet["model_payload"])),
            "request_identity_sha256":request_sha,
            "transmitted_user_message_sha256":sha(content.encode("utf-8")),
            "transmitted_user_message":content,
            "provider_schema_fixture_const":run["case_id"],
            "effort":c["effort"],"max_tokens":c["max_tokens"],
            "api_version":c["api_version"],"sdk_version":pkg_version("anthropic"),
            "started_at_utc":started_at,"ended_at_utc":utcnow(),
            "latency_seconds":round(time.perf_counter()-started,6),
            "provider_message_id":None,"stop_reason":None,
            "usage":None,"raw_provider_response":None,"raw_text":None,
            "structured_candidate":None,"schema_status":"NOT_CHECKED",
            "original_r2_issues":[],"corrected_issues":[],
            "referent_findings":[],"semantic_review_flags":[],
            "error_status":problem,"status":None}
        if problem is not None:
            receipt["status"]=problem["class"]
        else:
            raw=result.model_dump(mode="json")
            receipt.update(provider_message_id=raw.get("id"),
                provider_returned_model=raw.get("model"),
                stop_reason=raw.get("stop_reason"),usage=raw.get("usage"),
                raw_provider_response=raw)
            texts=[x["text"] for x in raw.get("content",[])
                   if x.get("type")=="text" and isinstance(x.get("text"),str)]
            if raw.get("model")!=run["model"]:
                receipt["status"]="PROVIDER_MODEL_MISMATCH"
            elif raw.get("stop_reason")=="refusal":
                receipt["status"]="MODEL_REFUSAL"
            elif raw.get("stop_reason")=="max_tokens":
                receipt["status"]="MODEL_TRUNCATED"
            elif len(texts)!=1:
                receipt["status"]="NO_TEXT_CANDIDATE"
            else:
                receipt["raw_text"]=texts[0]
                try:
                    candidate=json.loads(texts[0])
                    receipt["structured_candidate"]=candidate
                    Draft202012Validator(source_schema).validate(candidate)
                    receipt["schema_status"]="EXACT_ORIGINAL_SCHEMA_VALID"
                    diagnostic=review_candidate(
                        candidate,run["case_id"],packet,inherited.deterministic_candidate)
                    for key in ("original_r2_issues","corrected_issues",
                                "referent_findings","semantic_review_flags"):
                        receipt[key]=diagnostic[key]
                    receipt["status"]=("SCHEMA_VALID" if not diagnostic["corrected_issues"]
                                       else "STRUCTURAL_INVALID")
                except json.JSONDecodeError:
                    receipt["status"]="JSON_PARSE_INVALID"
                except ValidationError as exc:
                    receipt["schema_status"]="EXACT_ORIGINAL_SCHEMA_INVALID"
                    receipt["status"]="SCHEMA_INVALID"
                    receipt["error_status"]={"type":"LOCAL_SCHEMA_VIOLATION",
                        "path":list(exc.absolute_path),"validator":exc.validator}
        atomic_new(RAW/(attempt_id+".json"),receipt)
        print(f"{attempt_id}: {receipt['status']}")
        if receipt["status"]!="OPERATIONAL_TRANSIENT_NO_CANDIDATE":
            return
        if attempt<c["operational_retries"]:
            time.sleep(min(30,2**(attempt+1)))

def source_r2_result(run_id):
    # The real 60 R2 receipts live only in the operator's local R2 directory.
    # Never use user-reported totals to synthesize or infer missing outputs.
    folder=HERE.parent/"anthropic_court_r2"/"results"/"raw"
    attempts=sorted(folder.glob(run_id+"-A????.json"))
    require(bool(attempts),"MISSING_EXISTING_OPUS_R2_RAW: "+run_id)
    terminal={"SCHEMA_VALID","STRUCTURAL_INVALID","SCHEMA_INVALID","JSON_PARSE_INVALID",
              "MODEL_REFUSAL","MODEL_TRUNCATED","NO_TEXT_CANDIDATE",
              "PERMANENT_PROVIDER_FAILURE","PROVIDER_SCHEMA_FAILURE","PROVIDER_MODEL_MISMATCH"}
    existing=[read(p) for p in attempts if read(p).get("status") in terminal]
    require(len(existing)==1,"AMBIGUOUS_EXISTING_OPUS_PRIMARY: "+run_id)
    record=existing[0]
    require(record.get("run_id")==run_id and record.get("model")=="claude-opus-5-5"
            and record.get("provider_returned_model")=="claude-opus-5-5",
            "EXISTING_OPUS_PROVIDER_IDENTITY_MISMATCH: "+run_id)
    # Also verify R2 custody by the exact originally transmitted request.
    parent_config=inherited.config()
    run=next(x for x in inherited.execution_manifest(parent_config) if x["run_id"]==run_id)
    schema=inherited.transport_schema(inherited.original_schema(parent_config))
    prior,request_hash,message_hash,packet_name=inherited.request_for(run,parent_config,schema)
    require(record.get("case_id")==run["case_id"]
            and record.get("condition")==run["condition"]
            and record.get("replicate_ordinal")==run["replicate"]
            and record.get("request_identity_sha256")==request_hash
            and record.get("transmitted_user_message_sha256")==message_hash
            and record.get("input_packet_file")==packet_name
            and record.get("model_payload_sha256")==sha(canonical(
                read(INPUT/packet_name)["model_payload"])),
            "OPUS_SOURCE_REQUEST_IDENTITY_MISMATCH: "+run_id)
    return record

def collect_opus(c,full_r2_rows):
    report=[]
    by_id={r["run_id"]:r for r in full_r2_rows}
    for id_,row in sorted(by_id.items()):
        old=source_r2_result(id_)
        require(old["case_id"]==row["case_id"] and old["condition"]==row["condition"],
                "OPUS_SOURCE_CELL_MISMATCH: "+id_)
        packet,_=exact_packet(row["case_id"],row["condition"])
        candidate=old.get("structured_candidate")
        diagnostics=(review_candidate(candidate,row["case_id"],packet,
                     inherited.deterministic_candidate) if isinstance(candidate,dict)
                     else {"original_r2_issues":old.get("structural_checks",[]),
                           "corrected_issues":["NO_SCHEMA_VALID_CANDIDATE"],
                           "referent_findings":[],"semantic_review_flags":[]})
        if isinstance(candidate,dict) and old.get("schema_status")=="EXACT_ORIGINAL_SCHEMA_VALID":
            require(set(old.get("structural_checks",[]))==
                    set(diagnostics["original_r2_issues"]),
                    "R2_HISTORICAL_STATUS_NOT_REPRODUCIBLE: "+id_)
        report.append({"source_run_id":id_,"case_id":row["case_id"],
            "condition":row["condition"],"replicate":row["replicate"],
            "original_r2_structural_status":old["status"],
            "original_r2_structural_issues":old.get("structural_checks",[]),
            "corrected_referent_admission_status":
                ("SCHEMA_VALID" if not diagnostics["corrected_issues"] else "STRUCTURAL_INVALID"),
            "corrected_issues":diagnostics["corrected_issues"],
            "referent_findings":diagnostics["referent_findings"],
            "semantic_review_flags":diagnostics["semantic_review_flags"]})
    return report

def build_blinded(c,r2c,rows,mapping):
    from screen_common import source_manifest, stable_inputs
    all_opus=inherited.execution_manifest(r2c)
    require(len(all_opus)==60,"OPUS_PRIMARY_ARCHIVE_NOT_SIXTY")
    for run in rows:
        require(latest(run["run_id"]) is not None,"NEW_MODEL_RUN_MISSING: "+run["run_id"])
    for model in MODELS.values():smoke_pass(c,model)
    old_report=collect_opus(c,all_opus)
    target=RECEIPTS/"OPUS_R2_FULL_RECHECK_R1.json"
    if target.exists():require(read(target)==old_report,"OPUS_DIAGNOSTIC_RECEIPT_COLLISION")
    else:atomic_new(target,old_report)
    for entry in mapping:
        if entry["source_kind"]=="EXISTING_OPUS_R2":
            source=source_r2_result(entry["source_run_id"])
        else:
            source=latest(entry["source_run_id"])
            require(source is not None,"CROSS_MODEL_RESULT_MISSING")
        candidate=source.get("structured_candidate")
        blind={"blind_id":entry["blind_id"],"case_id":entry["case_id"],
               "candidate_occurrence":candidate}
        dest=BLINDED/(entry["blind_id"]+".json")
        if dest.exists():require(read(dest)==blind,"BLINDED_EXPORT_COLLISION: "+entry["blind_id"])
        else:atomic_new(dest,blind)
    print("Blinded 60-observation scorer bundle ready. Identity mapping NOT exported.")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument("--preflight",action="store_true")
    group.add_argument("--freeze",action="store_true")
    group.add_argument("--smoke-sonnet",action="store_true")
    group.add_argument("--smoke-haiku",action="store_true")
    group.add_argument("--build-blinded-bundle",action="store_true")
    args=parser.parse_args()
    live=args.smoke_sonnet or args.smoke_haiku or not any(
        (args.preflight,args.freeze,args.build_blinded_bundle))
    c,r2c,rows,mapping,_,_,packets,payloads,transport,source_schema=gate(
        check_key=live or args.preflight,check_sdk=live or args.preflight or args.freeze)
    fingerprints=freeze_fingerprints(c,r2c,rows,mapping,packets,payloads,transport)
    if args.preflight:
        if FREEZE.exists():require_freeze(fingerprints)
        print("PREFLIGHT_PASS: 20 inherited packets; 40 new calls; 60 blind slots; 0 API calls.")
        return
    if args.freeze:
        require(not raw_evidence(),"ALREADY_HAS_SCREEN_PROVIDER_EVIDENCE")
        item={"kind":"RFA06C_CROSS_MODEL_FREEZE","frozen_at_utc":utcnow(),
              "fingerprints":fingerprints}
        if FREEZE.exists():require_freeze(fingerprints)
        else:atomic_new(FREEZE,item)
        print("Frozen cross-model screen. No provider calls.")
        return
    require_freeze(fingerprints)
    if args.build_blinded_bundle:
        build_blinded(c,r2c,rows,mapping)
        return
    import anthropic
    client=anthropic.Anthropic(max_retries=0,timeout=c["timeout_seconds"],
              default_headers={"anthropic-version":c["api_version"]})
    if args.smoke_sonnet or args.smoke_haiku:
        model=MODELS["SONNET" if args.smoke_sonnet else "HAIKU"]
        run=find_smoke(c,model)
        if latest(run["run_id"]) is None:
            new_call(client,run,c,r2c,transport,source_schema)
        smoke_pass(c,model)
        print(model+" independently passed smoke gate.")
        return
    for model in MODELS.values():smoke_pass(c,model)
    for run in rows:
        if latest(run["run_id"]) is not None:
            print(run["run_id"]+" terminal attempt preserved; skip.")
            continue
        new_call(client,run,c,r2c,transport,source_schema)
    print("40-call screen pass complete. Preserve evidence; build blind bundle separately.")

if __name__=="__main__":
    try:main()
    except (RuntimeError,ValueError,OSError) as exc:
        print("CROSS_MODEL_COURT_HOLD: "+str(exc),file=sys.stderr)
        sys.exit(2)
