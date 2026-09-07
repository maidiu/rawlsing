#!/usr/bin/env python3
"""B12 Node7-v2 fresh combined replay driver.

Fresh-construction inputs are restricted to:
- immutable producer implementation/contract/schema at cfc240aa...;
- immutable Node4A predicate inputs;
- immutable Node4B query inputs;
- immutable protocol-v2 spec;
- committed B11 protocol-v2 serializer implementation.

No Node5A-R2 mapping rows or B11 payload rows are reconstruction inputs.
Historical Node5/Node6 identities are comparison constants only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

PRODUCER_COMMIT = "cfc240aa3a64c59509eab97450a7d3603af813cc"
PRODUCER_BLOB = "d63370dbcadc043dd2f27f5383cf36f0e84d1235"
PRODUCER_SHA256 = "ad7434186e5e72886333f438ed9726cec01a2d2cf740353175da938708a5ef6d"
CONTRACT_BLOB = "26a7d123881513524e26f2342ab93dd1141fb5f6"
EMPIRICAL_OBJECTS_BLOB = "91974c52ce8c0acafa939be0d7d83f4a5c8085b7"
INPUT_SCHEMA_BLOB = "3a15657cb99624a15fc4587b2a9e587dfafe65d3"

NODE4A_BLOB = "504944f9533b7385d201076e2e834b8a9446dee8"
NODE4A_SHA256 = "a5687a9ed938c4c8dd80f0bfd58ffa30c4e8ca6c84629fb19c5a360ae3761155"
QUERY_INPUTS_BLOB = "3f56e3b3c5e3c3be61adef392ee9ca59875827a3"
QUERY_HASHES_BLOB = "aa5aaa3a480e8551dff9a31efd8460b8b1705d57"
PROTOCOL_SPEC_BLOB = "befee68ee14f6e80e88cb3142947a37a7619fc5b"
B11_SERIALIZER_BLOB = "29b61fc7fef8db06e4ba95fedc788a20b8d28d5e"
B11_SERIALIZER_SHA256 = "47307828a471cc525643f870c32ac15efa26565f063191d50ea32c48c72994b6"
PROTOCOL_VALUE = "AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0"
PROSPECTIVE_MAPPING_SHA256 = "06f874df6bdd2e621886f748c8aa12397533e273649f99e654dc3779b5eb59db"
PROSPECTIVE_MAPPING_BLOB = "d62847e9972362bf2fcaeac515360cd5cf99eab7"
PROSPECTIVE_MAPPING_LENGTH = 12364

HISTORICAL_MAPPING_SHA256 = "081e3b8594be3d9348bc0565cd9085cca1e999ae58ef7881f040d11f5da89c7e"
HISTORICAL_MAPPING_DISPOSITION = "IMMUTABLE_HISTORICAL_PROVENANCE__NONREPLAYABLE_AT_CURRENT_EVIDENCE_SURFACE"
HISTORICAL_NODE6_SEAL = "df0395983de34996d33c258d0705cfc178df9cfe7982899431a0002c544481da"
HISTORICAL_NODE6_ROLE = "ACCEPTED_HISTORICAL_COMPARISON_EVIDENCE__NOT_PROSPECTIVE_REPLAY_TARGET"
HISTORICAL_NODE6_CROSSWALK_SHA256 = "6038d22864840311ebe0a1a76040befb0496009657edcbc4bfd90b89fadd53c7"
HISTORICAL_NODE6_CANONICAL_INTEGRITY_SHA256 = "e9c6e7cdc7381cb75ca86f41947203e9e188e73b522601791fda27736aa79169"
HISTORICAL_NODE6_TERRAIN_RECEIPT_SHA256 = "4277d27bb0851f75110d8c5cc6449c832e239fd998bf10ea46e0e096976f4d22"

PREDICATE_CANONICAL_PAYLOAD_SHA256 = "ef5cd10a5af7fcaad82b7dca39f2035ff829c59fe6f45ec681f872810276ac27"
ALIAS_PAYLOAD_SHA256 = "5f3763afced573d70fc72233d3c28d6f2d4d2f3ce8585d050a48a43ef8b00f5d"
NODE5B_QUERY_PACKAGE_SHA256 = "c185a68c3850131f701dae3b2cb20b66d947d40ef447ac69f0bcebe9d467732e"

EXPECTED_ROW_ORDER = [
    "A000","A1V1","A1V2","A1V3","A1V4","A1V5","A1SSUB","A1SSPS","A1SMIS","A1RAPP",
    "A2V1","A2V2","A2V3","A2V4","A2V5","A2SSUB","A2SSPS","A2SMIS","A2RAPP",
]
ROW_FIELDS = [
    "as3_id","source_object_id","source_content_hash","node4a_input_sha256",
    "successor_kind","successor_object_id","successor_content_hash",
    "alias_class","role_key_lookup_preserved",
]
QUERY_ORDER = ["T_Q301_2_RAW","T_Q301_7_RAW","T_Q301_2_Q301_7_RAW"]
QUERY_INPUT_HASHES = {
    "T_Q301_2_RAW":"714dde6e80801a563897f9a5cef707c7147e7fbb649473d707b8c030caecac9e",
    "T_Q301_7_RAW":"39791ee08a60ba2e8e76724200a32b0afe95411983c5eefc72c3ac19393b9416",
    "T_Q301_2_Q301_7_RAW":"ec75b212e57736664e33738ffa8d69483c4c6f82c6b8199aabef414d4846b1f1",
}
ORDERED_QUERY_PACKAGE_SHA256 = "fa68d91d4c40ff606cf4f5b06a3b213b57e3ecfc7e0c029627d7fd29413998a6"
COMPLETE_BUNDLE_SHA256 = "2cf15c20a4c65c2dcb29c6fd015260aa9ed8a70f0537927368c86e561a834e50"
QUERY_TARGETS = {
    "T_Q301_2_RAW":(
        "8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44",
        "16414b17c709dca60e93c4636540febca73dd44e5d0bcd5b236c5c2a6dad3744",
    ),
    "T_Q301_7_RAW":(
        "deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7",
        "2817fa258c30e77f4d9eff632dc570343cab63db28f5b94857b7dd9be170c89e",
    ),
    "T_Q301_2_Q301_7_RAW":(
        "ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053",
        "0bb9a74d85091e8954206669c1b180ea05426511b644e12075a8bbd96a178bd6",
    ),
}
SHARED_PREDICATE_HASH = "ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0"

TERRAIN = {
    "J":2,"K":18,"accepted_as3":"da36f2457513acf2ce734f3509236ef6d2dceec5",
    "candidate_count":82,"candidate_ordering_law":"CANONICAL_CANDIDATE_HASH_ORDER",
    "candidate_semantic_frontier_hash":"ec85fc2c6460a8a014ae90c54e5847f883c495708c32898ea44bfc0ef78c54e6",
    "common_I03_git_blob_sha":"3194ccbd4aede70f587bce32c7d0b70c54a17f4c",
    "common_measurement_law_git_blob_sha":"7c13a3e100e84154c86efa90b0257dc63c0485d0",
    "completion_law":"NONE_EXACT_EVALUATE_ALL","measure_partition":"RAW_ONLY","minimum_raw_denominator":0,
    "predicate_count":19,"predicate_semantic_catalog_hash":"8c559917640242e017b03e206d5a0a950cb2973c36a90e0be43d3c0fe7cc9293",
    "query_count":3,"query_semantic_catalog_hash":"f76ddf2b8a99e6a05884d503aa7a5da8fbf1fb3b07fbcd4cc93597457defa423",
    "recursive_depth":18,"risk_measure_topology_identity_hash":"ed3b76242a588a5e2d4dacbb76f17ceef6185cd27a4080a2e8fb436056abfabf",
    "risk_partition_count":1,"rng":"NONE",
    "route_A_common_candidate_terrain_git_blob_sha":"030b2b98fa2fb38be51cb38bc52d6401fd304d04",
    "route_B_common_candidate_terrain_git_blob_sha":"93b7e23650b3544669ee15e424f42c4ea807ade1",
    "route_C_accelerator_spec_git_blob_sha":"34d2d21e51cff0995301e04bfef994b97c6cc5d8",
    "route_C_invalidation_spec_git_blob_sha":"4fda5eb6ae5c6b215bfeb3a42b111bf6f8880f8a",
    "schema":"PRE553_AS3R3_FROZEN_TERRAIN_COMPATIBILITY_CLAIM@1.0.0",
    "support_rule_hash":"6df2664f4a9cd8fe5d334b954aed4db1b97de4937b4d03e5ce63bcc322baab4c",
    "support_rule_id":"PRE553_PRODUCTION_I05_NO_ADDITIONAL_MINIMUM_RAW_DENOMINATOR@1.0.0",
    "topology_partition_count":2,
    "typed_nonpositive_learned_preV3_target_git_blob_sha":"8527efc27dc23ebba4e7a212a1d6c152c18f720a",
}

class FailClosed(RuntimeError):
    pass

def require(ok: bool, msg: str) -> None:
    if not ok:
        raise FailClosed(msg)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()

def canonical_bytes(value: Any, *, lf: bool=True) -> bytes:
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    return raw + (b"\n" if lf else b"")

def file_identity(path: Path, *, blob: str|None=None, digest: str|None=None) -> dict[str,Any]:
    data=path.read_bytes()
    if blob is not None:
        require(git_blob(data)==blob,f"Git blob mismatch: {path}")
    if digest is not None:
        require(sha256(data)==digest,f"SHA-256 mismatch: {path}")
    return {"git_blob":git_blob(data),"sha256":sha256(data),"byte_length":len(data)}

def load_module(path: Path, name: str):
    spec=importlib.util.spec_from_file_location(name,path)
    require(spec is not None and spec.loader is not None,f"cannot load module {path}")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def object_representation_hash(obj: Any) -> str:
    return sha256(canonical_bytes(obj.as_dict(),lf=True))

def exact_ref_dict(obj: Any) -> dict[str,str]:
    return obj.ref.as_dict()

def input_hash(record: dict[str,Any], *, lf: bool) -> str:
    return sha256(canonical_bytes(record,lf=lf))

def fresh_csv_bytes(rows: list[dict[str,Any]]) -> bytes:
    sio=io.StringIO(newline="")
    w=csv.DictWriter(sio,fieldnames=ROW_FIELDS,lineterminator="\n",quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for row in rows:
        out={k:row[k] for k in ROW_FIELDS}
        out["role_key_lookup_preserved"]="true" if out["role_key_lookup_preserved"] is True else "false"
        w.writerow(out)
    return sio.getvalue().encode("utf-8")

def serialize_v2_with_committed_serializer(serializer_path: Path, protocol_path: Path, csv_path: Path) -> bytes:
    serializer=load_module(serializer_path,"b11_protocol_v2_serializer")
    return serializer.materialize(protocol_path,csv_path)

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--execution-root",required=True,type=Path)
    ap.add_argument("--node4a",required=True,type=Path)
    ap.add_argument("--query-inputs",required=True,type=Path)
    ap.add_argument("--query-hashes",required=True,type=Path)
    ap.add_argument("--protocol-spec",required=True,type=Path)
    ap.add_argument("--b11-serializer",required=True,type=Path)
    ap.add_argument("--output-dir",required=True,type=Path)
    args=ap.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)

    producer_path=args.execution_root/"rawlsing_next/pre553_as3r3_runtime_producer.py"
    contract_path=args.execution_root/"rawlsing_next/pre553_as3r3_runtime_producer_contract.py"
    empirical_path=args.execution_root/"rawlsing_next/pre553_empirical_objects.py"
    schema_path=args.execution_root/"rawlsing_next/pre553_as3r3_runtime_producer_input.schema.json"

    code_ids={
        "producer":file_identity(producer_path,blob=PRODUCER_BLOB,digest=PRODUCER_SHA256),
        "contract":file_identity(contract_path,blob=CONTRACT_BLOB),
        "empirical_objects":file_identity(empirical_path,blob=EMPIRICAL_OBJECTS_BLOB),
        "input_schema":file_identity(schema_path,blob=INPUT_SCHEMA_BLOB),
        "node4a":file_identity(args.node4a,blob=NODE4A_BLOB,digest=NODE4A_SHA256),
        "query_inputs":file_identity(args.query_inputs,blob=QUERY_INPUTS_BLOB),
        "query_hashes":file_identity(args.query_hashes,blob=QUERY_HASHES_BLOB),
        "protocol_spec":file_identity(args.protocol_spec,blob=PROTOCOL_SPEC_BLOB),
        "b11_serializer":file_identity(args.b11_serializer,blob=B11_SERIALIZER_BLOB,digest=B11_SERIALIZER_SHA256),
    }

    sys.path.insert(0,str(args.execution_root))
    node4a=load_module(args.node4a,"node4a_frozen_inputs")
    from rawlsing_next import pre553_as3r3_runtime_producer as producer

    predicate_inputs=node4a.load_predicate_inputs()
    require(len(predicate_inputs)==19,"predicate input count")
    require([x["as3_semantic_source_identity"]["as3_id"] for x in predicate_inputs]==EXPECTED_ROW_ORDER,"predicate order")

    query_doc=json.loads(args.query_inputs.read_text(encoding="utf-8"))
    query_inputs=query_doc["query_inputs"]
    require([x["as3_semantic_source_identity"]["as3_id"] for x in query_inputs]==QUERY_ORDER,"query order")
    require(query_doc["query_count"]==3,"query count")
    require(query_doc["producer_commit"]==PRODUCER_COMMIT,"query producer commit")
    require(query_doc["producer_file_sha256"]==PRODUCER_SHA256,"query producer sha")
    require(query_doc["condition_role_rule"]["role_source_id"]=="A000","A000 role provenance")

    qhash_doc=json.loads(args.query_hashes.read_text(encoding="utf-8"))
    require(qhash_doc["ordered_query_package_sha256"]==ORDERED_QUERY_PACKAGE_SHA256,"frozen ordered query hash receipt")
    require(qhash_doc["complete_future_input_bundle_sha256"]==COMPLETE_BUNDLE_SHA256,"frozen bundle receipt")

    for rec in query_inputs:
        sid=rec["as3_semantic_source_identity"]["as3_id"]
        require(input_hash(rec,lf=True)==QUERY_INPUT_HASHES[sid],f"query input hash {sid}")
    ordered_q=[{"input_sha256":QUERY_INPUT_HASHES[sid],"query_source_id":sid} for sid in QUERY_ORDER]
    require(sha256(canonical_bytes(ordered_q,lf=True))==ORDERED_QUERY_PACKAGE_SHA256,"ordered query package")

    bundle={"schema":"PRE553_AS3R3_SUCCESSOR_RUNTIME_INPUT_BUNDLE@1.0.0",
            "predicate_inputs":predicate_inputs,"query_inputs":query_inputs,"terrain_claim":TERRAIN}
    require(sha256(canonical_bytes(bundle,lf=True))==COMPLETE_BUNDLE_SHA256,"complete future input bundle")
    producer.validate_frozen_terrain_claim(TERRAIN)

    pred_validation_count=0
    pred_constructor_count=0
    original_pred_validate=producer.validate_successor_predicate_input
    def counted_pred_validate(rec):
        nonlocal pred_validation_count
        pred_validation_count+=1
        return original_pred_validate(rec)
    producer.validate_successor_predicate_input=counted_pred_validate

    fresh_predicates=[]
    rows=[]
    for rec in predicate_inputs:
        pred_constructor_count+=1
        obj=producer.construct_successor_predicate(rec)
        src=rec["as3_semantic_source_identity"]
        sid=src["as3_id"]
        alias="{A000,A1RAPP}" if sid in {"A000","A1RAPP"} else ""
        ref=exact_ref_dict(obj)
        rows.append({
            "as3_id":sid,
            "source_object_id":src["object_id"],
            "source_content_hash":src["content_hash"],
            "node4a_input_sha256":input_hash(rec,lf=False),
            "successor_kind":ref["kind"],
            "successor_object_id":ref["object_id"],
            "successor_content_hash":ref["content_hash"],
            "alias_class":alias,
            "role_key_lookup_preserved":True,
        })
        fresh_predicates.append((sid,obj))
    require(pred_validation_count==19 and pred_constructor_count==19,"exact predicate validation/constructor count")
    require([r["as3_id"] for r in rows]==EXPECTED_ROW_ORDER,"fresh mapping row order")

    by_ref={}
    for sid,obj in fresh_predicates:
        k=obj.ref.key
        if k not in by_ref:
            by_ref[k]={"ref":obj.ref.as_dict(),"roles":[],"canonical_representation":obj.as_dict()}
        by_ref[k]["roles"].append(sid)
    predicate_bundle=list(by_ref.values())
    require(len(predicate_bundle)==18,"18 distinct fresh predicates")
    duplicate=[x["roles"] for x in predicate_bundle if len(x["roles"])>1]
    require(duplicate==[["A000","A1RAPP"]],"sole predicate alias")
    require(sha256(canonical_bytes(predicate_bundle,lf=True))==PREDICATE_CANONICAL_PAYLOAD_SHA256,"predicate canonical payload")
    a000_ref=next(obj.ref for sid,obj in fresh_predicates if sid=="A000")
    a1rapp_ref=next(obj.ref for sid,obj in fresh_predicates if sid=="A1RAPP")
    require(a000_ref==a1rapp_ref and a000_ref.content_hash==SHARED_PREDICATE_HASH,"A000/A1RAPP exact shared predicate")

    fresh_csv=fresh_csv_bytes(rows)
    fresh_csv_path=args.output_dir/"fresh_mapping_rows.csv"
    fresh_csv_path.write_bytes(fresh_csv)
    require(git_blob(fresh_csv)=="26a7c35df2e6454c5e270a03b3571599bdf152fd","fresh rows must byte-reconstruct frozen material carrier")
    mapping_bytes=serialize_v2_with_committed_serializer(args.b11_serializer,args.protocol_spec,fresh_csv_path)
    require(len(mapping_bytes)==PROSPECTIVE_MAPPING_LENGTH,"v2 mapping length")
    require(sha256(mapping_bytes)==PROSPECTIVE_MAPPING_SHA256,"v2 mapping sha256")
    require(git_blob(mapping_bytes)==PROSPECTIVE_MAPPING_BLOB,"v2 mapping Git blob")
    (args.output_dir/"fresh_mapping_payload_v2.json").write_bytes(mapping_bytes)

    query_validation_count=0
    query_constructor_count=0
    original_validate_query=producer._validate_query
    def counted_validate_query(rec,condition_keys):
        nonlocal query_validation_count
        query_validation_count+=1
        return original_validate_query(rec,condition_keys)
    producer._validate_query=counted_validate_query

    pred_refs=[obj.ref for _,obj in by_source_distinct(fresh_predicates)]
    query_rows=[]
    query_objects=[]
    for rec in query_inputs:
        query_constructor_count+=1
        obj=producer.construct_successor_query(rec,successor_predicate_refs=pred_refs)
        sid=rec["as3_semantic_source_identity"]["as3_id"]
        ref=obj.ref.as_dict()
        rep_hash=object_representation_hash(obj)
        target_hash,target_rep_hash=QUERY_TARGETS[sid]
        require(ref["content_hash"]==target_hash and ref["object_id"].endswith(target_hash),f"query identity {sid}")
        require(rep_hash==target_rep_hash,f"query representation {sid}")
        query_rows.append({
            "query_source_id":sid,
            "source_object_id":rec["as3_semantic_source_identity"]["object_id"],
            "source_content_hash":rec["as3_semantic_source_identity"]["content_hash"],
            "node4b_input_sha256":QUERY_INPUT_HASHES[sid],
            "successor_kind":ref["kind"],
            "successor_object_id":ref["object_id"],
            "successor_content_hash":ref["content_hash"],
            "canonical_representation_sha256":rep_hash,
            "condition_role_source_id":"A000",
            "condition_successor_content_hash":SHARED_PREDICATE_HASH,
        })
        query_objects.append((sid,obj))
    require(query_validation_count==3 and query_constructor_count==3,"exact query validation/constructor count")
    require(len({obj.ref.key for _,obj in query_objects})==3,"3 distinct queries")

    query_pkg_payload={
        "schema":"AS3R3_NODE5B_SUCCESSOR_QUERY_PACKAGE@1.0.0",
        "producer_commit":PRODUCER_COMMIT,
        "producer_file_sha256":PRODUCER_SHA256,
        "node4b_complete_bundle_sha256":COMPLETE_BUNDLE_SHA256,
        "node4b_ordered_query_input_package_sha256":ORDERED_QUERY_PACKAGE_SHA256,
        "ordered_query_source_ids":QUERY_ORDER,
        "queries":[{
            "query_source_id":sid,
            "node4b_input_sha256":QUERY_INPUT_HASHES[sid],
            "successor_query_ref":obj.ref.as_dict(),
            "canonical_representation_sha256":object_representation_hash(obj),
        } for sid,obj in query_objects],
        "condition_binding":{
            "role_source_id":"A000",
            "successor_predicate_ref":a000_ref.as_dict(),
            "alias_class":["A000","A1RAPP"],
            "role_provenance":"A000_PRESERVED_NOT_RELABELED_AS_A1RAPP",
            "node5a_role_mapping_payload_sha256":HISTORICAL_MAPPING_SHA256,
        },
    }
    require(sha256(canonical_bytes(query_pkg_payload,lf=False))==NODE5B_QUERY_PACKAGE_SHA256,"Node5B query package")

    canonical_predicates=[]
    for item in predicate_bundle:
        canonical_predicates.append({
            "family":"PREDICATE",
            "ref":item["ref"],
            "canonical_representation_sha256":sha256(canonical_bytes(item["canonical_representation"],lf=True)),
        })
    canonical_queries=[{
        "family":"QUERY","ref":obj.ref.as_dict(),
        "canonical_representation_sha256":object_representation_hash(obj),
    } for _,obj in query_objects]
    canonical_objects=sorted(canonical_predicates,key=lambda x:x["ref"]["object_id"])+sorted(canonical_queries,key=lambda x:x["ref"]["object_id"])
    require(len(canonical_objects)==21,"21 canonical successor objects")

    realization={
        "schema":"AS3R3_NODE7_V2_DETERMINISTIC_REALIZATION@1.0.0",
        "status":"PASS__PROSPECTIVE_FRESH_COMBINED_REPLAY_V2_REALIZATION",
        "protocol":PROTOCOL_VALUE,
        "protocol_spec_git_blob":PROTOCOL_SPEC_BLOB,
        "committed_serializer_git_blob":B11_SERIALIZER_BLOB,
        "committed_serializer_sha256":B11_SERIALIZER_SHA256,
        "producer":{"commit":PRODUCER_COMMIT,"git_blob":PRODUCER_BLOB,"file_sha256":PRODUCER_SHA256},
        "inputs":{
            "node4a_git_blob":NODE4A_BLOB,"node4a_file_sha256":NODE4A_SHA256,
            "node4b_query_inputs_git_blob":QUERY_INPUTS_BLOB,
            "node4b_ordered_query_package_sha256":ORDERED_QUERY_PACKAGE_SHA256,
            "node4b_complete_bundle_sha256":COMPLETE_BUNDLE_SHA256,
        },
        "execution_counts":{
            "predicate_validations":pred_validation_count,
            "predicate_constructor_calls":pred_constructor_count,
            "query_validations":query_validation_count,
            "query_constructor_calls":query_constructor_count,
        },
        "mapping":{
            "protocol_v2_payload_sha256":PROSPECTIVE_MAPPING_SHA256,
            "protocol_v2_payload_git_blob":PROSPECTIVE_MAPPING_BLOB,
            "protocol_v2_payload_byte_length":PROSPECTIVE_MAPPING_LENGTH,
            "rows":rows,
        },
        "predicates":{
            "mapping_count":19,"distinct_count":18,
            "sole_alias_class":["A000","A1RAPP"],
            "canonical_payload_sha256":PREDICATE_CANONICAL_PAYLOAD_SHA256,
            "objects":canonical_predicates,
        },
        "queries":{
            "mapping_count":3,"distinct_count":3,
            "node5b_query_package_sha256":NODE5B_QUERY_PACKAGE_SHA256,
            "mappings":query_rows,
            "objects":canonical_queries,
        },
        "combined":{"mapping_count":22,"distinct_successor_objects":21,"objects":canonical_objects},
        "terrain":TERRAIN,
        "historical_comparison":{
            "mapping_payload_sha256":HISTORICAL_MAPPING_SHA256,
            "mapping_payload_disposition":HISTORICAL_MAPPING_DISPOSITION,
            "historical_preimage_or_law_recovery_claimed":False,
            "node6_seal":HISTORICAL_NODE6_SEAL,
            "node6_role":HISTORICAL_NODE6_ROLE,
            "node6_crosswalk_sha256":HISTORICAL_NODE6_CROSSWALK_SHA256,
            "node6_canonical_integrity_receipt_sha256":HISTORICAL_NODE6_CANONICAL_INTEGRITY_SHA256,
            "node6_terrain_receipt_sha256":HISTORICAL_NODE6_TERRAIN_RECEIPT_SHA256,
        },
    }
    realization_bytes=canonical_bytes(realization,lf=True)
    realization_sha=sha256(realization_bytes)
    (args.output_dir/"realization.json").write_bytes(realization_bytes)

    write_csv(args.output_dir/"predicate_crosswalk.csv",rows,ROW_FIELDS)
    query_fields=list(query_rows[0].keys())
    write_csv(args.output_dir/"query_crosswalk.csv",query_rows,query_fields)
    manifest={"schema":"AS3R3_NODE7_V2_REPLAYED_CANONICAL_OBJECT_MANIFEST@1.0.0","count":21,"objects":canonical_objects}
    (args.output_dir/"canonical_manifest.json").write_bytes(canonical_bytes(manifest,lf=True))

    result={
        "schema":"AS3R3_NODE7_V2_FRESH_PROCESS_RESULT@1.0.0",
        "status":"PASS",
        "realization_sha256":realization_sha,
        "realization_git_blob":git_blob(realization_bytes),
        "realization_byte_length":len(realization_bytes),
        "protocol_v2_mapping_sha256":PROSPECTIVE_MAPPING_SHA256,
        "predicate_constructor_calls":pred_constructor_count,
        "query_constructor_calls":query_constructor_count,
        "distinct_predicates":18,
        "distinct_queries":3,
        "distinct_successor_objects":21,
        "sole_alias":["A000","A1RAPP"],
        "node7_downstream_entered":False,
    }
    (args.output_dir/"result.json").write_bytes(canonical_bytes(result,lf=True))
    sys.stdout.write(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n")
    return 0

def by_source_distinct(items):
    seen=set()
    out=[]
    for sid,obj in items:
        if obj.ref.key not in seen:
            seen.add(obj.ref.key); out.append((sid,obj))
    return out

def write_csv(path: Path, rows: list[dict[str,Any]], fields: list[str]) -> None:
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n",quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for row in rows:
            out=dict(row)
            for k,v in out.items():
                if isinstance(v,bool): out[k]="true" if v else "false"
            w.writerow(out)

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, json.JSONDecodeError, csv.Error) as exc:
        sys.stderr.write(f"FAIL_CLOSED: {exc}\n")
        raise SystemExit(2)
