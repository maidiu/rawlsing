from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

BASE = Path(__file__).resolve().parent / "recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/RESIDUAL_ZERO_LOSS_EXECUTION_WAVE_R2/B08_V550J_ASIAN_LATIN"
ASIAN = BASE / "ASIAN_BAROMETER_V550J_AUTHORITY_SERIALIZATION.json"
LATIN = BASE / "LATINOBAROMETRO_V550J_AUTHORITY_SERIALIZATION.json"
EVIDENCE = BASE / "R14_SOURCE_STRUCTURE_EVIDENCE_DISPOSITION.csv"

class B08AuthoritySerializationError(RuntimeError):
    pass

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_registry(path: Path) -> dict:
    data=json.loads(path.read_text(encoding="utf-8"))
    required={
        "schema","source_family","eligible_waves","recovery_adjudication_denominator",
        "routing_dependency","denominator_disposition_complete","production_executable_registry",
        "admitted_product_configurations","unresolved_product_authority","archive08_promotion",
        "product_completeness_claim","deterministic_hash_contract",
    }
    missing=sorted(required-set(data))
    if missing: raise B08AuthoritySerializationError("missing fields: "+",".join(missing))
    if data["schema"]!="V550J_SOURCE_FAMILY_AUTHORITY_SERIALIZATION_R1":
        raise B08AuthoritySerializationError("wrong schema")
    den=data["recovery_adjudication_denominator"]
    if den.get("global_source_structure_count")!=2499 or den.get("global_membership_count")!=15990:
        raise B08AuthoritySerializationError("aggregate recovery denominator drift")
    if den.get("exact_b08_source_family_row_partition_materialized_on_start_surface") is not False:
        raise B08AuthoritySerializationError("may not fabricate B08 exact-row denominator")
    if data["denominator_disposition_complete"] is not False:
        raise B08AuthoritySerializationError("no-loss denominator may not be claimed complete")
    if data["production_executable_registry"] is not False:
        raise B08AuthoritySerializationError("blocked serialization may not become executable authority")
    if data["product_completeness_claim"] is not False:
        raise B08AuthoritySerializationError("product completeness forbidden")
    if data["routing_dependency"].get("b02_b05_consumed") is not False:
        raise B08AuthoritySerializationError("B02-B05 sibling consumption forbidden")
    if data["routing_dependency"].get("product_execution_authorized") is not False:
        raise B08AuthoritySerializationError("routing blocker cannot authorize execution")
    if data["admitted_product_configurations"]:
        raise B08AuthoritySerializationError("bounded canary may not be widened into product authority")
    if data["archive08_promotion"] is not False:
        raise B08AuthoritySerializationError("Archive08 promotion forbidden")
    return data

def validate_all() -> dict:
    a=load_registry(ASIAN); l=load_registry(LATIN)
    if a["source_family"]!="Asian Barometer" or a["eligible_waves"]!=["W1","W4","W5"]:
        raise B08AuthoritySerializationError("Asian exact CLOSED_35 scope drift")
    excluded={x["wave"]:x["disposition"] for x in a["explicitly_excluded_waves"]}
    if excluded.get("W6")!="EXCLUDED_BY_GOVERNING_CLOSED_35_SCOPE_LAW":
        raise B08AuthoritySerializationError("Asian W6 must remain expressly excluded")
    if "W6" in a["eligible_waves"]:
        raise B08AuthoritySerializationError("Asian W6 widening forbidden")
    if l["source_family"]!="Latinobarómetro" or l["eligible_waves"]!=["1995","2011","2024"]:
        raise B08AuthoritySerializationError("Latinobarometro source scope drift")
    rows=list(csv.DictReader(EVIDENCE.open(encoding="utf-8-sig",newline="")))
    if len(rows)!=73:
        raise B08AuthoritySerializationError(f"R14 evidence row census drift:{len(rows)}")
    if any(r["source_family"] not in {"Asian Barometer","Latinobarómetro"} for r in rows):
        raise B08AuthoritySerializationError("foreign source-family evidence row")
    if any(r["b08_disposition"]!="R14_RELATION_BACKED_SOURCE_STRUCTURE_EVIDENCE_ONLY__NOT_V550J_J_FAMILY_AUTHORITY" for r in rows):
        raise B08AuthoritySerializationError("R14 evidence promoted to J-family authority")
    if any(r["source_family"]=="Asian Barometer" and r["wave"]=="W6" for r in rows):
        raise B08AuthoritySerializationError("Asian W6 evidence leakage")
    return {
       "status":"PASS_BLOCKED_SERIALIZATION_FAILS_CLOSED",
       "asian_sha256":sha256_file(ASIAN),
       "latin_sha256":sha256_file(LATIN),
       "r14_evidence_sha256":sha256_file(EVIDENCE),
       "r14_evidence_rows":len(rows),
       "production_executable_registries":0,
       "denominator_disposition_complete":False,
    }

if __name__=="__main__":
    print(json.dumps(validate_all(),sort_keys=True))
