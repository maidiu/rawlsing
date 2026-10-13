"""RFA-06C2 offline proof and append-only reuse of owner-local RFA-06C smoke receipts.

Never calls Anthropic. Neither the predecessor freeze nor its evidence is changed.
Missing or ambiguous evidence is a HOLD, never inferred from an owner summary.
"""
from __future__ import annotations
import json
from jsonschema import Draft202012Validator
from screen_common import (
    HERE, PARENT, INPUT, RAW, RECEIPTS, MODELS, atomic_new, canonical, sha,
    read, require, file_hash, request_for_new, review_candidate,
    exact_packet, inherited,
)

PREDECESSOR = PARENT / "anthropic_cross_model_screen_r1"
PROOF_FILE = RECEIPTS / "EXISTING_SMOKE_REUSE_PROOF_R2.json"

def check_existing_smokes(c, r2c, transport, original_schema):
    freeze_file = PREDECESSOR / "EXPERIMENT_FREEZE_R1.json"
    require(freeze_file.is_file(), "EXISTING_SMOKE_REUSE_HOLD: predecessor freeze absent")
    fingerprints = read(freeze_file).get("fingerprints", {})
    compiled = fingerprints.get("compiled_new_model_requests")
    require(isinstance(compiled, dict) and len(compiled) == 42,
            "EXISTING_SMOKE_REUSE_HOLD: predecessor 42-request freeze missing")
    packet_hashes, payload_hashes = inherited.verify_inputs(r2c)
    require(fingerprints.get("original_packet_raw_hashes") == dict(sorted(packet_hashes.items()))
            and fingerprints.get("original_payload_sha256") == payload_hashes,
            "EXISTING_SMOKE_REUSE_HOLD: source packet freeze drift")
    require(fingerprints.get("source_r2_compiler_sha256") ==
            file_hash(PARENT/"anthropic_court_r2"/"court_common_r2.py")
            and fingerprints.get("source_r2_runner_sha256") ==
            file_hash(PARENT/"anthropic_court_r2"/"run_anthropic_renderer_court_r2.py"),
            "EXISTING_SMOKE_REUSE_HOLD: R2 source code freeze drift")
    require(fingerprints.get("provider") == c["provider"]
            and fingerprints.get("model_ids") == c["comparison_model_ids"]
            and fingerprints.get("effort") == c["effort"]
            and fingerprints.get("max_tokens") == c["max_tokens"]
            and fingerprints.get("api_version") == c["api_version"],
            "EXISTING_SMOKE_REUSE_HOLD: provider configuration freeze drift")
    verified = []
    seen_provider_ids = set()
    for run in c["model_smokes"]:
        rid = run["run_id"]
        request, packet_name = request_for_new(run, c, r2c, transport)
        expected = {"request_sha256": sha(canonical(request)),
                    "message_sha256": sha(request["messages"][0]["content"].encode("utf-8")),
                    "schema_sha256": sha(canonical(request["output_config"]["format"]["schema"])),
                    "model": run["model"], "fixture_id": run["case_id"]}
        require(compiled.get(rid) == expected,
                "EXISTING_SMOKE_REUSE_HOLD: predecessor frozen request differs: "+rid)
        files = sorted((PREDECESSOR/"results"/"raw").glob(rid+"-A????.json"))
        require(len(files) == 1,
                "EXISTING_SMOKE_REUSE_HOLD: missing/multiple predecessor smoke attempts: "+rid)
        path = files[0]
        rec = read(path)
        require(path.name == rec.get("attempt_id", "") + ".json"
                and rec.get("run_id") == rid
                and rec.get("requested_model") == run["model"]
                and rec.get("provider_returned_model") == run["model"]
                and rec.get("case_id") == run["case_id"]
                and rec.get("condition") == run["condition"]
                and rec.get("replicate") == run.get("replicate",0)
                and rec.get("input_packet_file") == packet_name
                and rec.get("input_packet_raw_sha256") == file_hash(INPUT/packet_name)
                and rec.get("original_model_payload_sha256") ==
                    sha(canonical(read(INPUT/packet_name)["model_payload"]))
                and rec.get("request_identity_sha256") == expected["request_sha256"]
                and rec.get("transmitted_user_message_sha256") == expected["message_sha256"]
                and rec.get("transmitted_user_message") == request["messages"][0]["content"]
                and rec.get("provider_schema_fixture_const") == run["case_id"]
                and rec.get("effort") == c["effort"]
                and rec.get("max_tokens") == c["max_tokens"]
                and rec.get("api_version") == c["api_version"]
                and rec.get("sdk_version") == "1.13.0",
                "EXISTING_SMOKE_REUSE_HOLD: receipt request/transport mismatch: "+rid)
        response = rec.get("raw_provider_response")
        pid = rec.get("provider_message_id")
        require(isinstance(response, dict) and isinstance(pid,str) and bool(pid)
                and response.get("id") == pid and response.get("model") == run["model"]
                and rec.get("stop_reason") == response.get("stop_reason")
                and rec.get("stop_reason") not in ("refusal","max_tokens")
                and pid not in seen_provider_ids,
                "EXISTING_SMOKE_REUSE_HOLD: provider message identity collision: "+rid)
        seen_provider_ids.add(pid)
        texts = [x["text"] for x in response.get("content",[])
                 if isinstance(x,dict) and x.get("type") == "text"
                 and isinstance(x.get("text"),str)]
        require(len(texts) == 1 and texts[0] == rec.get("raw_text"),
                "EXISTING_SMOKE_REUSE_HOLD: raw response text mismatch: "+rid)
        try:
            candidate = json.loads(texts[0])
            Draft202012Validator(original_schema).validate(candidate)
        except Exception as exc:
            raise RuntimeError("EXISTING_SMOKE_REUSE_HOLD: parse/original schema failure: "+rid) from exc
        require(candidate == rec.get("structured_candidate")
                and isinstance(candidate,dict)
                and candidate.get("fixture_id") == run["case_id"]
                and rec.get("schema_status") == "EXACT_ORIGINAL_SCHEMA_VALID"
                and rec.get("status") in ("SCHEMA_VALID","STRUCTURAL_INVALID"),
                "EXISTING_SMOKE_REUSE_HOLD: candidate/schema/fixture mismatch: "+rid)
        packet,_ = exact_packet(run["case_id"],run["condition"])
        diag = review_candidate(candidate,run["case_id"],packet,inherited.deterministic_candidate)
        verified.append({"run_id":rid,"model":run["model"],"receipt_file":path.name,
                         "receipt_sha256":file_hash(path),"provider_message_id":pid,
                         "request_sha256":expected["request_sha256"],
                         "message_sha256":expected["message_sha256"],
                         "schema_sha256":expected["schema_sha256"],
                         "predecessor_historical_status":rec["status"],
                         "corrected_status":"SCHEMA_VALID" if not diag["corrected_issues"] else "STRUCTURAL_INVALID",
                         "corrected_issues":diag["corrected_issues"]})
    return {"kind":"RFA06C2_EXISTING_SMOKE_REUSE_VERIFIED",
            "predecessor_freeze_sha256":file_hash(freeze_file),
            "existing_smoke_reuse":"PASS","verified":verified}

def import_existing_smokes(c,r2c,transport,original_schema):
    """Two-phase verify before any append-only write; never overwrites receipts."""
    report=check_existing_smokes(c,r2c,transport,original_schema)
    for item in report["verified"]:
        target=RAW/item["receipt_file"]
        require(not target.exists(),"EXISTING_SMOKE_REUSE_HOLD: target receipt already exists")
    require(not PROOF_FILE.exists(),"EXISTING_SMOKE_REUSE_HOLD: proof already exists")
    for item in report["verified"]:
        record=read(PREDECESSOR/"results"/"raw"/item["receipt_file"])
        atomic_new(RAW/item["receipt_file"],record)
        require(file_hash(RAW/item["receipt_file"]) == item["receipt_sha256"],
                "EXISTING_SMOKE_REUSE_HOLD: imported receipt bytes differ")
    atomic_new(PROOF_FILE,report)
    return report
