"""RFA-06C reusable offline source, request, freeze and evidence-custody primitives."""
from __future__ import annotations
import copy, hashlib, json, os, re, sys, tempfile
from collections import Counter
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
from jsonschema import Draft202012Validator

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
R2=PARENT/"anthropic_court_r2"
INPUT=PARENT/"render_inputs_r1"
RAW=HERE/"results"/"raw"
BLINDED=HERE/"results"/"blinded"
RECEIPTS=HERE/"results"/"receipts"
SCORING=HERE/"results"/"scoring"
REPORTS=HERE/"results"/"reports"
FREEZE=HERE/"EXPERIMENT_FREEZE_R2.json"
sys.path.insert(0,str(R2))
import court_common_r2 as inherited
from referent_admission import compile_grounding,review_candidate,require

MODELS={"SONNET":"claude-sonnet-5-5","HAIKU":"claude-haiku-5-5"}
RUN_PATTERN=re.compile(r"^(?:CMRUN-\d{4}|CMSONNET-SMOKE|CMHAIKU-SMOKE)-A\d{4}\.json$")
IDS=[f"RF{i:03d}" for i in range(1,11)]
DIMENSIONS=(
"hard_factual_contradiction","historical_contradiction","epistemic_leakage",
"actor_access_violation","generic_character_drift","relation_discontinuity",
"excessive_agreeableness","excessive_articulation_self_awareness",
"excessive_narrative_neatness","unsupported_ontology","physical_impossibility",
"typed_occurrence_prose_mismatch","lawful_lying_preservation",
"same_person_recognizability","distributional_nadia_continuity"
)

def read(path):return json.loads(Path(path).read_text(encoding="utf-8"))
def canonical(o):return json.dumps(o,ensure_ascii=False,separators=(",",":"),allow_nan=False).encode("utf-8")
def sha(o):return hashlib.sha256(o).hexdigest()
def file_hash(path):return sha(Path(path).read_bytes())
def utcnow():
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
def pkg_version(name):
    try:return version(name)
    except PackageNotFoundError:return "NOT_INSTALLED"
def assert_file_sha(path,expected):
    require(Path(path).is_file(),"MISSING_FILE: "+str(path))
    require(inherited.git_blob_sha1(Path(path).read_bytes())==expected,"SOURCE_FILE_CHANGED: "+str(path))

def atomic_new(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    fd,tmp=tempfile.mkstemp(prefix=".pending-",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            os.fchmod(f.fileno(),0o600);f.write(data);f.flush();os.fsync(f.fileno())
        os.link(tmp,path)  # exclusive publish; no silent overwrite
    finally:
        Path(tmp).unlink(missing_ok=True)

def config():
    c=read(HERE/"EXPERIMENT_CONFIG_R2.json")
    predecessor=read(PARENT/"anthropic_cross_model_screen_r1"/"EXPERIMENT_CONFIG_R1.json")
    require(c.get("kind")=="RFA06C2_THREE_MODEL_SCREEN_V2",
            "NOT_RFA06C2_EXECUTION_VERSION")
    require({k:v for k,v in c.items() if k!="kind"}==
            {k:v for k,v in predecessor.items() if k!="kind"},
            "CROSS_MODEL_COMPARABILITY_HOLD: inherited RFA06C configuration changed")
    r2c=inherited.config()
    for filename, blob in c["sealed_r2_git_blobs"].items():
        assert_file_sha(R2/filename, blob)
    for key in ("effort","max_tokens","api_version","api_endpoint","timeout_seconds",
                "operational_retries","system_message","temperature","top_p","top_k"):
        require(c[key]==r2c[key],"PARENT_PROVIDER_CONFIG_CHANGED: "+key)
    require(c["comparison_model_ids"]==["claude-opus-5-5","claude-sonnet-5-5","claude-haiku-5-5"],
            "MODEL_IDS_DRIFT")
    require(c["new_model_ids"]==list(MODELS.values()),"NEW_MODEL_IDS_DRIFT")
    require(c["sdk_pin"]=="anthropic==1.13.0" and c["jsonschema_pin"]=="jsonschema==4.25.1",
            "DEPENDENCY_PINS_CHANGED")
    require(c["new_primary_calls"]==40 and c["primary_comparison_observations"]==60,
            "SAMPLE_UNIVERSE_CHANGED")
    require(c["gen_calls_by_commission"]==0,"EVIDENCE_SCOPE_CHANGED")
    return c,r2c

def shuffle_tuples(seq,seed):
    arr=list(seq);state=int(seed,16)
    for i in range(len(arr)-1,0,-1):
        state^=(state<<13)&0xffffffff
        state^=state>>17
        state^=(state<<5)&0xffffffff
        state&=0xffffffff
        j=state%(i+1)
        arr[i],arr[j]=arr[j],arr[i]
    return arr

def source_manifest(c):
    schedule=read(HERE/"EXECUTION_MANIFEST_PRIVATE_R1.json")
    selection=read(HERE/"OPUS_EXISTING_SAMPLE_SELECTION_R1.json")
    mapping=read(HERE/"BLIND_MAPPING_PRIVATE_R1.json")
    blind=read(HERE/"BLINDED_SCORING_MANIFEST_R1.json")
    original=inherited.execution_manifest(inherited.config())
    selected=[x for x in original if x["replicate"]==1]
    secondary=[x for x in original if x["replicate"]!=1]
    require(len(selected)==20 and len(secondary)==40,"OPUS_REPLICATE_SELECTION_INCOMPLETE")
    require(selection["selected_count"]==20 and selection["secondary_count"]==40,"OPUS_SELECTION_COUNTS_WRONG")
    require({(x["case_id"],x["condition"],x["run_id"]) for x in selected}==
            {(x["case_id"],x["condition"],x["source_run_id"]) for x in selection["selected"]},
            "OPUS_PRIMARY_SELECTION_NOT_PREDETERMINED")
    require(set(selection["secondary_r2_run_ids"])=={x["run_id"] for x in secondary},
            "OPUS_SECONDARY_SET_CHANGED")
    pairs=[(tier,model,f"RF{i:03d}",arm) for tier,model in MODELS.items()
           for i in range(1,11) for arm in ("N","WP")]
    shuffled=shuffle_tuples(pairs,c["schedule_seed"])
    rows=schedule["runs"]
    require(len(rows)==40 and schedule["order_seed"]==c["schedule_seed"],
            "NEW_SCHEDULE_SIZE_OR_SEED_CHANGED")
    require(all((x["tier"],x["model"],x["case_id"],x["condition"])==shuffled[i]
                and x["run_id"]==f"CMRUN-{i+1:04d}" and x["replicate"]==1
                for i,x in enumerate(rows)),"NEW_SCHEDULE_NOT_REPRODUCIBLE")
    comp=[("EXISTING_OPUS_R2","claude-opus-5-5",x["case_id"],x["condition"],x["source_run_id"])
          for x in selection["selected"]]
    comp += [("NEW_CROSS_MODEL",x["model"],x["case_id"],x["condition"],x["run_id"])
             for x in rows]
    # Unlike run scheduling, evaluator order is independently shuffled.
    shuffled_blind=shuffle_tuples(comp,c["blind_seed"])
    require(len(mapping["entries"])==len(blind["entries"])==60,"BLIND_COUNT_WRONG")
    for i,entry in enumerate(mapping["entries"]):
        expected=shuffled_blind[i]
        require((entry["source_kind"],entry["model"],entry["case_id"],entry["condition"],
                entry["source_run_id"])==expected,"BLIND_ORDER_NOT_REPRODUCIBLE")
        blind_id=f"BLIND-CM-{i+1:04d}"
        require(entry["blind_id"]==blind_id and blind["entries"][i]=={"blind_id":blind_id},
                "BLIND_ID_OR_METADATA_MISMATCH")
    require(Counter((x["model"],x["case_id"],x["condition"]) for x in mapping["entries"])==
            Counter({(model,id_,arm):1 for model in c["comparison_model_ids"]
                     for id_ in IDS for arm in ("N","WP")}),
            "UNBALANCED_PRIMARY_UNIVERSE")
    return rows,mapping["entries"],selected,secondary

def exact_packet(case_id,arm):
    name=f"{case_id}_{arm}.json"
    return read(INPUT/name),name

def request_for_new(run,c,r2c,transport):
    """IDENTICAL inherited R2 semantic request except exact Anthropic model field."""
    prior_request,_,_,packet_name=inherited.request_for(run,r2c,transport)
    req=copy.deepcopy(prior_request)
    require(run["model"] in MODELS.values(),"UNAUTHORIZED_PROVIDER_MODEL")
    req["model"]=run["model"]
    only_model=copy.deepcopy(req);only_model["model"]=prior_request["model"]
    require(canonical(only_model)==canonical(prior_request),"MODEL_VISIBLE_DRIFT_BEYOND_MODEL_ID")
    envelope=json.loads(req["messages"][0]["content"])
    packet,_=exact_packet(run["case_id"],run["condition"])
    require(envelope["model_payload"]==packet["model_payload"] and
            envelope["required_fixture_id"]==run["case_id"] and
            envelope["transport_instruction"]==r2c["identity_instruction"],
            "R2_TRANSPORT_SEMANTICS_CHANGED")
    require(req["output_config"]["format"]["schema"]["properties"]["fixture_id"]==
            {"const":run["case_id"]},"REQUEST_SPECIFIC_FIXTURE_CONST_CHANGED")
    return req,packet_name

def stable_inputs(c,r2c,rows,mapping):
    packets,payload_hashes=inherited.verify_inputs(r2c)
    original_schema=inherited.original_schema(r2c)
    transport=inherited.transport_schema(original_schema)
    for run in rows+c["model_smokes"]:
        req,name=request_for_new(run,c,r2c,transport)
        _=read(INPUT/name)
        require(req["output_config"]["effort"]=="high" and req["max_tokens"]==16384,
                "MODEL_CONTRACT_CHANGED")
    for i in range(1,11):
        for arm in ("WP","N"):
            packet,_=exact_packet(f"RF{i:03d}",arm)
            compile_grounding(packet)
    return packets,payload_hashes,transport,original_schema

def raw_evidence():
    RAW.mkdir(parents=True,exist_ok=True)
    files=sorted(RAW.glob("*.json"))
    for p in files:
        require(RUN_PATTERN.fullmatch(p.name),"FOREIGN_EVIDENCE_FILE: "+p.name)
        r=read(p)
        require(r.get("attempt_id")+".json"==p.name,"ATTEMPT_FILE_NAME_DIFFERS")
    return files

def latest(run_id):
    hits=sorted(RAW.glob(run_id+"-A????.json"))
    require(len(hits)<=3,"UNEXPECTED_ATTEMPT_MULTIPLICITY: "+run_id)
    terminal={"SCHEMA_VALID","STRUCTURAL_INVALID","SCHEMA_INVALID","JSON_PARSE_INVALID",
              "MODEL_REFUSAL","MODEL_TRUNCATED","NO_TEXT_CANDIDATE",
              "PERMANENT_PROVIDER_FAILURE","PROVIDER_SCHEMA_FAILURE","PROVIDER_MODEL_MISMATCH"}
    for f in reversed(hits):
        if read(f).get("status") in terminal:return read(f)
    return None

def next_attempt(run_id):
    old=sorted(RAW.glob(run_id+"-A????.json"))
    idx=max((int(p.stem.rsplit("-A",1)[1]) for p in old),default=0)+1
    require(idx<=9999,"ATTEMPT_EXHAUSTED")
    return f"{run_id}-A{idx:04d}"

def freeze_fingerprints(c,r2c,rows,mapping,packet_hashes,payload_hashes,transport):
    compiled={}
    for run in rows+c["model_smokes"]:
        req,_=request_for_new(run,c,r2c,transport)
        compiled[run["run_id"]]={"request_sha256":sha(canonical(req)),
            "message_sha256":sha(req["messages"][0]["content"].encode("utf-8")),
            "schema_sha256":sha(canonical(req["output_config"]["format"]["schema"])),
            "model":run["model"],"fixture_id":run["case_id"]}
    static=("screen_common.py","referent_admission.py","quote_invariant.py",
            "smoke_custody.py","test_quote_and_smoke_r2.py",
            "run_cross_model_court.py","validate_cross_model_court.py",
            "score_and_unblind.py","requirements.txt","README.md",
            "REFERENT_ADMISSION_ONTOLOGY_AUDIT_R1.md",
            "REFERENT_ADMISSION_CONTRACT_R2.md","COMPARABILITY_AND_DESIGN_RECEIPT_R1.md",
            "LOCAL_EXECUTION_INSTRUCTIONS_R2.md","MODEL_BINDING_RECEIPT_R1.md",
            "STATIC_VERIFICATION_RECEIPT_R1.md",
            "SPEECH_PROSE_VALIDATION_DEFECT_RECEIPT_R1.md",
            "SMOKE_GATE_AND_CUSTODY_RECEIPT_R1.md",
            "COMPARABILITY_PROOF_R2.md",".gitignore",
            "EXPERIMENT_CONFIG_R2.json","OPUS_EXISTING_SAMPLE_SELECTION_R1.json",
            "EXECUTION_MANIFEST_PRIVATE_R1.json","BLIND_MAPPING_PRIVATE_R1.json",
            "BLINDED_SCORING_MANIFEST_R1.json")
    return {"experiment":c["kind"],"source_r2_commit":c["base"],
        "source_r2_compiler_sha256":file_hash(R2/"court_common_r2.py"),
        "source_r2_runner_sha256":file_hash(R2/"run_anthropic_renderer_court_r2.py"),
        "original_schema_sha256":file_hash(PARENT/"lab_fixture"/"OBJECTIVE_OCCURRENCE_OUTPUT_SCHEMA_R1.json"),
        "rubric_sha256":file_hash(PARENT/"lab_fixture"/"RENDERER_SCORING_RUBRIC_R1.md"),
        "original_packet_raw_hashes":packets_digest(packet_hashes),
        "original_payload_sha256":payload_hashes,
        "provider":c["provider"],"model_ids":c["comparison_model_ids"],
        "effort":c["effort"],"max_tokens":c["max_tokens"],"sdk":c["sdk_pin"],
        "api_version":c["api_version"],"compiled_new_model_requests":compiled,
        "local_sources_sha256":{name:file_hash(HERE/name) for name in static}}

def packets_digest(d):return dict(sorted(d.items()))

def require_freeze(fingerprint):
    require(FREEZE.exists(),"MISSING_SCREEN_FREEZE: run --freeze first")
    require(read(FREEZE)["fingerprints"]==fingerprint,
            "SCREEN_FREEZE_MISMATCH: close this court version")

def gate(check_key=False,check_sdk=False):
    c,r2c=config()
    rows,mapping,selected,secondary=source_manifest(c)
    packets,payloads,transport,original=stable_inputs(c,r2c,rows,mapping)
    if check_key:require(bool(os.getenv("ANTHROPIC_API_KEY")),"ANTHROPIC_API_KEY_NOT_IN_LOCAL_ENVIRONMENT")
    if check_sdk:
        require(pkg_version("anthropic")=="1.13.0" and pkg_version("jsonschema")=="4.25.1",
                "DEPENDENCY_VERSIONS_NOT_PINNED")
    for directory in (RAW,BLINDED,RECEIPTS,SCORING,REPORTS):
        directory.mkdir(parents=True,exist_ok=True)
        require(os.access(directory,os.W_OK),"EVIDENCE_DIRECTORY_UNWRITABLE")
    # Local evidence must match the frozen identity, provider model and source packet.
    for p in raw_evidence():
        row=read(p);rid=row["run_id"]
        defs={x["run_id"]:x for x in rows+c["model_smokes"]}
        require(rid in defs,"R1_OR_FOREIGN_RESULT_IN_RFA06C: "+rid)
        source=defs[rid]
        req,packet_name=request_for_new(source,c,r2c,transport)
        require(row.get("request_identity_sha256")==sha(canonical(req)) and
                row.get("transmitted_user_message_sha256")==
                sha(req["messages"][0]["content"].encode("utf-8")) and
                row.get("input_packet_file")==packet_name and
                row.get("requested_model")==source["model"] and
                row.get("case_id")==source["case_id"] and
                row.get("condition")==source["condition"] and
                row.get("provider_schema_fixture_const")==source["case_id"] and
                row.get("original_model_payload_sha256")==
                sha(canonical(read(INPUT/packet_name)["model_payload"])),
                "LOCAL_EVIDENCE_REQUEST_IDENTITY_MISMATCH: "+p.name)
    return c,r2c,rows,mapping,selected,secondary,packets,payloads,transport,original