#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, os, re, sys
from pathlib import Path
import yaml
from docx import Document

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def read_csv(path: Path):
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--json-out")
    args=ap.parse_args()
    root=Path(args.root).resolve()
    sec=root/"43_P3_STRUCTURE_ARTICULATION_AND_IMPLEMENTATION_PLAN"
    checks=[]
    def ck(name, ok, detail=""):
        checks.append({"check":name,"status":"PASS" if ok else "FAIL","detail":detail})
    required = [
        root/"00_START_HERE/CURRENT_STATE.json",
        root/"00_START_HERE/SCOPE_LOCK.json",
        root/"00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v21_20260731.docx",
        sec/"Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v1_20260731.docx",
        sec/"Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v1_20260731.md",
        sec/"P3_CONTROLLED_VOCABULARIES.csv",
        sec/"P3_RELATION_COMPOSITION_MATRIX.csv",
        sec/"P3_STATUS_STATE_MACHINE.csv",
        sec/"P3_EVIDENCE_SUFFICIENCY_MATRIX.csv",
        sec/"P3_ARTIFACT_CATALOG.csv",
        sec/"P3_SCHEMA_DICTIONARY.csv",
        sec/"P3_EXECUTION_SEQUENCE.yaml",
        sec/"P3_PILOT_SELECTION_RULES.yaml",
        sec/"P3_PLAN_LOCK.json",
        sec/"algorithms/P3_ALGORITHMS_AND_PSEUDOCODE.md",
        sec/"sql/p3_postgresql_compatible_ddl.sql",
        sec/"validation/P3_ACCEPTANCE_GATES.csv",
        sec/"validation/P3_TEST_AND_MUTATION_PLAN.csv",
        sec/"validation/P3_CONTINGENCY_MATRIX.csv",
        sec/"validation/P3_DOCUMENT_QA_RETURN.json",
        sec/"downstream/P3_DOWNSTREAM_INTERFACES.md",
        sec/"downstream/P3_DOWNSTREAM_INTERFACE_REGISTRY.csv",
        sec/"release/P3_AUTHORITY_RELEASE_MIGRATION_ROLLBACK_PROTOCOL.md",
        sec/"adjudication/P3_CANDIDATE_PACKET_TEMPLATE.json",
        sec/"adjudication/P3_ADJUDICATION_DECISION_TEMPLATE.json",
    ]
    ck("required_files", all(p.exists() for p in required), f"{sum(p.exists() for p in required)}/{len(required)}")
    # Current state
    cs=load_json(root/"00_START_HERE/CURRENT_STATE.json")
    ck("current_state_v21", cs.get("handoff_version")=="v21")
    ck("global_p2_closed", cs.get("global_p2_closed") is True)
    ck("p3_plan_authored", cs.get("p3_plan_authored") is True and cs.get("p3_implementation_started") is False)
    ck("next_execution_point", cs.get("next_pass")=="P3A_CONTRACT_AND_PILOT_V1_IMPLEMENTATION")
    ck("p2_counts_preserved", (
        cs.get("phase0_implementations")==18276 and
        cs.get("source_local_lineages")==13526 and
        cs.get("semantic_priority_queue_total")==18831 and
        cs.get("semantic_priority_pairs_remaining")==0 and
        cs.get("semantic_priority_authority_class_counts",{}).get("PROPOSITION_RELATION_AUTHORITY")==641
    ))
    ck("no_canonical_authority_claim", cs.get("canonical_j_family_authority_authored") is False and cs.get("p3_candidate_inventory_generated") is False)
    # Plan lock
    pl=load_json(sec/"P3_PLAN_LOCK.json")
    ck("plan_lock", pl.get("next_execution_point")=="P3A_CONTRACT_AND_PILOT_V1_IMPLEMENTATION" and pl.get("execution_started") is False)
    ck("pilot_bounded", pl.get("pilot",{}).get("global_relation_surface")==641 and pl.get("pilot",{}).get("maximum_manual_candidates")==40)
    # V20 baseline verifier return
    pre=load_json(sec/"PRE_V21_ROOT_CONTROLS/V20_CUMULATIVE_VERIFIER_RETURN.json")
    passed = pre.get("status")=="PASS" or pre.get("summary",{}).get("status")=="PASS"
    count_text=json.dumps(pre)
    ck("pre_v21_v20_verifier_pass", passed and ("34" in count_text), pre.get("status",""))
    # Inherited hash preservation
    base_rows=read_csv(sec/"PRE_V21_ROOT_CONTROLS/SHA256SUMS_v20.csv")
    changed_allowed={
        "MASTER_HANDOFF.md","README_FIRST.md","PACKAGE_INDEX.csv","SHA256SUMS.csv","VALIDATION.json",
        "00_START_HERE/CURRENT_STATE.json","00_START_HERE/SCOPE_LOCK.json","00_START_HERE/README_FIRST.md",
        "00_START_HERE/MASTER_HANDOFF.md","00_START_HERE/EXACT_RESUME_POINT.md",
        "00_START_HERE/NEXT_CHAT_OPENING_INSTRUCTION.txt"
    }
    inherited_checked=0; inherited_fail=[]
    for row in base_rows:
        rel=row["relative_path"]
        if rel in changed_allowed: continue
        p=root/rel
        if not p.exists():
            inherited_fail.append((rel,"missing")); continue
        inherited_checked+=1
        if p.stat().st_size != int(row["bytes"]) or sha256_file(p)!=row["sha256"]:
            inherited_fail.append((rel,"changed"))
    ck("inherited_v20_hash_preservation", not inherited_fail, f"checked={inherited_checked}; failures={inherited_fail[:5]}")
    # CSV contracts
    vocab=read_csv(sec/"P3_CONTROLLED_VOCABULARIES.csv")
    keys=[(r["vocabulary_domain"],r["code"]) for r in vocab]
    required_domains={"field_evidence_state","operator","modality","response_topology","pair_relation_type","collision_type","collision_scope","family_lifecycle_status","portability_ceiling","evidence_type","hyperedge_type","object_type"}
    ck("controlled_vocab_unique", len(keys)==len(set(keys)) and len(vocab)>=140, str(len(vocab)))
    ck("controlled_vocab_domains", required_domains.issubset({r["vocabulary_domain"] for r in vocab}))
    comp=read_csv(sec/"P3_RELATION_COMPOSITION_MATRIX.csv")
    ck("composition_matrix_8x8", len(comp)==64 and len({r["left_edge_type"] for r in comp})==8 and len({r["right_edge_type"] for r in comp})==8)
    ck("composition_no_endpoint_authority", all(r["creates_new_pair_authority"]=="NO" and r["requires_direct_endpoint_audit"]=="YES" for r in comp))
    transitions=read_csv(sec/"P3_STATUS_STATE_MACHINE.csv")
    ck("lifecycle_has_no_direct_discovered_accept", not any(r["from_status"]=="DISCOVERED" and r["to_status"].startswith("ACCEPTED") for r in transitions))
    ck("lifecycle_append_history_states", {"SUPERSEDED","DEPRECATED"}.issubset({r["to_status"] for r in transitions}))
    evidence=read_csv(sec/"P3_EVIDENCE_SUFFICIENCY_MATRIX.csv")
    ck("evidence_sufficiency", len(evidence)>=10 and any(r["decision_surface"]=="value_portability" and r["maximum_authority"]=="NO_P3_AUTHORITY" for r in evidence))
    artifacts=read_csv(sec/"P3_ARTIFACT_CATALOG.csv")
    needed_artifacts={"p3_lineage_proposition_signatures.csv","p3_pair_fact_bundles.csv","p3_internal_pair_matrix.csv","p3_closure_obligations.csv","p3_candidate_families.csv","p3_adjudication_decisions.csv","p3_authority_releases.csv"}
    ck("artifact_catalog_complete", needed_artifacts.issubset({r["artifact"] for r in artifacts}))
    schema_dict=read_csv(sec/"P3_SCHEMA_DICTIONARY.csv")
    ck("schema_dictionary", len(schema_dict)>=40 and {"proposition_signature_field","pair_fact_bundle","collision_scope_registry","candidate_family","adjudication_decision","authority_release"}.issubset({r["table_or_artifact"] for r in schema_dict}))
    gates=read_csv(sec/"validation/P3_ACCEPTANCE_GATES.csv")
    tests=read_csv(sec/"validation/P3_TEST_AND_MUTATION_PLAN.csv")
    contingencies=read_csv(sec/"validation/P3_CONTINGENCY_MATRIX.csv")
    ck("acceptance_gates", len(gates)>=40 and all(r["severity"]=="FATAL" for r in gates))
    ck("test_plan", len(tests)>=35 and {"example","property","mutation","gold","integration"}.issubset({r["test_class"] for r in tests}))
    ck("contingency_matrix", len(contingencies)>=30 and all(r["fail_closed"]=="YES" for r in contingencies))
    # YAML
    execution=yaml.safe_load((sec/"P3_EXECUTION_SEQUENCE.yaml").read_text(encoding="utf-8"))
    pilot=yaml.safe_load((sec/"P3_PILOT_SELECTION_RULES.yaml").read_text(encoding="utf-8"))
    ck("execution_sequence", execution["next_execution_point"]=="P3A_CONTRACT_AND_PILOT_V1_IMPLEMENTATION" and len(execution["phases"])>=10)
    ck("pilot_rules", pilot["maximum_manual_candidates"]==40 and sum(x["target_count"] for x in pilot["strata"])==40)
    # JSON schemas
    schema_files=sorted((sec/"schemas").glob("*.schema.json"))
    schema_ok=True
    for p in schema_files:
        obj=load_json(p)
        schema_ok &= obj.get("$schema")=="https://json-schema.org/draft/2020-12/schema" and obj.get("type")=="object"
    ck("json_schemas", schema_ok and len(schema_files)==14, str(len(schema_files)))
    # Templates
    pkt=load_json(sec/"adjudication/P3_CANDIDATE_PACKET_TEMPLATE.json")
    dec=load_json(sec/"adjudication/P3_ADJUDICATION_DECISION_TEMPLATE.json")
    ck("candidate_packet_template", "internal_pair_matrix" in pkt and "explicit_exclusions" in pkt and "decision_form" in pkt)
    ck("decision_template_no_value_authority", dec.get("response_portability_status")=="NOT_AUTHORIZED_BY_P3")
    # DDL
    ddl=(sec/"sql/p3_postgresql_compatible_ddl.sql").read_text(encoding="utf-8")
    required_tables=["p3_authority_release","p3_object_id_registry","p3_lineage_segment","p3_proposition_signature","p3_pair_fact_bundle","p3_collision_scope_registry","p3_candidate_family","p3_internal_pair_matrix","p3_closure_obligation","p3_family_variant","p3_family_exclusion","p3_hyperedge","p3_adjudication_decision","p3_doctrine_delta","p3_family_genealogy","p3_artifact_dependency","p3_failure_ledger"]
    ck("ddl_required_tables", all(re.search(r"CREATE TABLE\s+"+re.escape(t)+r"\b",ddl,re.I) for t in required_tables))
    ck("ddl_non_installing", "ROLLBACK;" in ddl and "NOT an installation script" in ddl)
    ck("ddl_no_p3_value_authority", "NOT_AUTHORIZED_BY_P3" in ddl)
    # Doctrine text
    md=(sec/"Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v1_20260731.md").read_text(encoding="utf-8")
    phrases=[
        "A path never creates a new direct pair authority",
        "family membership does not authorize value harmonization",
        "The assistant will perform P3A, P3B, and P3C",
        "P3A_CONTRACT_AND_PILOT_V1_IMPLEMENTATION",
        "complete internal pair matrix",
        "named and rule-based exclusions",
        "no TypeDB, Neo4j",
        "18,831",
        "641 proposition relations",
    ]
    ck("central_plan_doctrine", all(x.lower() in md.lower() for x in phrases), str([x for x in phrases if x.lower() not in md.lower()]))
    ck("central_plan_substantial", len(md.split())>=5500, str(len(md.split())))
    # DOCX parse and QA
    docx_ok=True
    for p in [required[2],required[3]]:
        try:
            d=Document(p)
            docx_ok &= len(d.paragraphs)>20
        except Exception:
            docx_ok=False
    ck("docx_parse",docx_ok)
    qa=load_json(sec/"validation/P3_DOCUMENT_QA_RETURN.json")
    ck("docx_visual_qa", qa["plan_docx"]["visual_inspection"]=="PASS_ALL_26_PAGES" and qa["master_docx"]["visual_inspection"]=="PASS_ALL_3_PAGES")
    ck("docx_accessibility", all(sum(x["a11y"].values())==0 for x in [qa["plan_docx"],qa["master_docx"]]))
    # No execution overclaim or runtime changes
    scope=load_json(root/"00_START_HERE/SCOPE_LOCK.json")
    ck("scope_prohibitions", "database or registry writes" in scope["prohibited_until_p3_closure_and_shadow_install"] and "automatic canonical family approval" in scope["prohibited_until_p3_closure_and_shadow_install"])
    ck("no_p3_execution_artifacts", not any((sec/name).exists() for name in ["p3_candidate_families.csv","p3_lineage_proposition_signatures.csv","p3_adjudication_decisions.csv"]))
    # Cache/debris
    debris=[str(p.relative_to(root)) for p in root.rglob("*") if p.name in {".pytest_cache","__pycache__"} or p.suffix in {".pyc",".pyo"}]
    ck("no_cache_or_bytecode_debris", not debris, str(debris[:10]))

    # Root and section manifests
    root_manifest_excludes={"PACKAGE_INDEX.csv","SHA256SUMS.csv",
        "43_P3_STRUCTURE_ARTICULATION_AND_IMPLEMENTATION_PLAN/FINAL_RELEASE_GATE_RETURN.json",
        "43_P3_STRUCTURE_ARTICULATION_AND_IMPLEMENTATION_PLAN/validation/V21_CUMULATIVE_VERIFIER_RETURN.json"}
    actual_root_files={str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and str(p.relative_to(root)) not in root_manifest_excludes}
    sha_rows=read_csv(root/"SHA256SUMS.csv")
    pkg_rows=read_csv(root/"PACKAGE_INDEX.csv")
    sha_map={r["relative_path"]:r for r in sha_rows}
    pkg_map={r["relative_path"]:r for r in pkg_rows}
    root_manifest_ok=(set(sha_map)==actual_root_files==set(pkg_map))
    if root_manifest_ok:
        for rel in actual_root_files:
            p=root/rel
            row=sha_map[rel]
            if int(row["bytes"])!=p.stat().st_size or row["sha256"]!=sha256_file(p) or pkg_map[rel]!=row:
                root_manifest_ok=False
                break
    ck("root_manifests_exact",root_manifest_ok,f"manifest={len(sha_map)} actual={len(actual_root_files)}")
    sec_manifest_excludes={"SECTION_MANIFEST.csv","FINAL_RELEASE_GATE_RETURN.json",
        "validation/V21_CUMULATIVE_VERIFIER_RETURN.json"}
    actual_sec_files={str(p.relative_to(sec)) for p in sec.rglob("*") if p.is_file() and str(p.relative_to(sec)) not in sec_manifest_excludes}
    sm_rows=read_csv(sec/"SECTION_MANIFEST.csv")
    sm_map={r["relative_path"]:r for r in sm_rows}
    section_manifest_ok=set(sm_map)==actual_sec_files
    if section_manifest_ok:
        for rel in actual_sec_files:
            p=sec/rel
            row=sm_map[rel]
            if int(row["bytes"])!=p.stat().st_size or row["sha256"]!=sha256_file(p):
                section_manifest_ok=False
                break
    ck("section_manifest_exact",section_manifest_ok,f"manifest={len(sm_map)} actual={len(actual_sec_files)}")

    failed=[x for x in checks if x["status"]=="FAIL"]
    result={
        "verifier":"verify_handoff_v21.py",
        "root":str(root),
        "status":"PASS" if not failed else "FAIL",
        "checks_passed":len(checks)-len(failed),
        "checks_total":len(checks),
        "failed_checks":failed,
        "checks":checks
    }
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"checks_passed":result["checks_passed"],"checks_total":result["checks_total"],"failed":[x["check"] for x in failed]},indent=2))
    return 0 if not failed else 1

if __name__=="__main__":
    raise SystemExit(main())
