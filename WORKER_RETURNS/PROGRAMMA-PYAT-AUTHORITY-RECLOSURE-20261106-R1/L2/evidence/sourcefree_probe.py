#!/usr/bin/env python3
"""S2 sourcefree L2 diagnostic; never touches original respondent data."""
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

import pandas as pd
from data.ddm_build_copy import ddm_v551_atoms as a
from data.ddm_build_copy import ddm_v552_structural as s

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def update_manifest(manifest, csv):
    payload=json.loads(manifest.read_text())
    payload["registry_sha256"]=digest(csv)
    manifest.write_text(json.dumps(payload,sort_keys=True))

def main():
    original=a.SCALE_REGISTRY_PATH
    original_manifest=a.SCALE_REGISTRY_MANIFEST_PATH
    assert digest(original)==json.loads(original_manifest.read_text())["registry_sha256"]
    certified=a._load_registry()
    key=next(k for k,v in certified.items() if v["authority_intensity_semantics"]=="DIRECTIONAL_MAGNITUDE")
    out=[]
    out.append(("certified_registry_row_count",len(certified)))
    with tempfile.TemporaryDirectory(prefix="l2-sourcefree-") as tmp:
        p=Path(tmp)/"registry.csv"; m=Path(tmp)/"manifest.json"
        shutil.copyfile(original,p);shutil.copyfile(original_manifest,m)
        a.SCALE_REGISTRY_PATH=p;a.SCALE_REGISTRY_MANIFEST_PATH=m;a._registry_cache=None
        baseline=a._load_registry()[key]["projection_rule_id"]
        a.SCALE_REGISTRY_PATH=p.with_name("missing_registry.csv");a._registry_cache=None
        try:
            a._load_registry()
            out.append(("missing_registry_rejected",False))
        except RuntimeError as e:
            out.append(("missing_registry_rejected",str(e)))
        a.SCALE_REGISTRY_PATH=p
        payload=json.loads(m.read_text())
        payload["schema_version"]="L2_SYNTHETIC_WRONG_VERSION"
        m.write_text(json.dumps(payload,sort_keys=True));a._registry_cache=None
        try:
            a._load_registry()
            out.append(("wrong_version_rejected",False))
        except RuntimeError as e:
            out.append(("wrong_version_rejected",str(e)))
        shutil.copyfile(original_manifest,m)
        data=pd.read_csv(p,dtype=str).fillna("")
        data.loc[data.response_semantics_contract_hash.eq(key),"projection_rule_id"]="L2_SYNTHETIC_CHANGED_RULE"
        data.to_csv(p,index=False)
        a._registry_cache=None
        try:
            a._load_registry()
            out.append(("wrong_hash_rejected",False))
        except RuntimeError as e:
            out.append(("wrong_hash_rejected",str(e)))
        update_manifest(m,p)
        changed=a._load_registry()[key]["projection_rule_id"]
        out.append(("changed_rule_after_fresh_load",changed))
        data=pd.read_csv(p,dtype=str).fillna("")
        data.loc[data.index[1],"response_semantics_contract_hash"]=key
        data.to_csv(p,index=False);update_manifest(m,p);a._registry_cache=None
        try:
            a._load_registry()
            out.append(("duplicate_key_rejected",False))
        except RuntimeError as e:
            out.append(("duplicate_key_rejected",str(e)))
        data.loc[data.index[1],"response_semantics_contract_hash"]=pd.read_csv(original,dtype=str).iloc[1]["response_semantics_contract_hash"]
        data.loc[data.response_semantics_contract_hash.eq(key),"review_status"]="REVIEW_REQUIRED"
        data.to_csv(p,index=False);update_manifest(m,p)
        a._registry_cache=None
        try:
            a._load_registry()
            out.append(("review_required_row_accepted_by_v551_loader",True))
        except RuntimeError as e:
            out.append(("review_required_row_accepted_by_v551_loader",False))
        shutil.copyfile(original,p);shutil.copyfile(original_manifest,m)
        a._registry_cache=None
        loaded_before=a._load_registry()[key]["projection_rule_id"]
        data=pd.read_csv(p,dtype=str).fillna("")
        data.loc[data.response_semantics_contract_hash.eq(key),"projection_rule_id"]="L2_SYNTHETIC_OTHER_RULE"
        data.to_csv(p,index=False);update_manifest(m,p)
        loaded_stale=a._load_registry()[key]["projection_rule_id"]
        a._registry_cache=None
        loaded_fresh=a._load_registry()[key]["projection_rule_id"]
        out.append(("same_process_cache_stale_after_manifest_matched_mutation",loaded_before==loaded_stale and loaded_fresh!=loaded_stale))
        shutil.copyfile(original,p);shutil.copyfile(original_manifest,m)
        a._registry_cache=None
        out.append(("restoration_exact_digest",digest(p)==digest(original) and a._load_registry()[key]["projection_rule_id"]==baseline))
    a.SCALE_REGISTRY_PATH=original;a.SCALE_REGISTRY_MANIFEST_PATH=original_manifest;a._registry_cache=None
    bridge=pd.DataFrame([{
        "run_id":"L2_SYNTHETIC","source":"L2_SYNTHETIC","source_family":"L2_SYNTHETIC",
        "wave":"SYNTHETIC_WAVE","canonical_wave":"SYNTHETIC_WAVE","country_code":"XX",
        "analysis_scope":"country","source_table":"answer_distribution","source_row_hash":"synthetic-hash",
        "question_id":"synthetic-q","var_code":"synthetic-v","position_field":"","position_value":"",
        "response_value_raw":"1","response_value_normalized":"1","response_label":"synthetic",
        "response_family":"ordered_subjective_scale","response_direction":"positive","response_intensity":0.5,
        "directional_applicability_status":"APPLICABLE_BY_AUTHORITY","bridge_evidence_lane":"direct_relation_response",
        "is_substantive":True,"is_missing":False,"is_special":False,
        "response_semantics_contract_hash":key,"semantic_role":"RELATION_EVIDENCE",
        "semantic_role_authority_status":"CERTIFIED","response_semantics_authority_status":"CERTIFIED",
        "directionality_authority_status":"CERTIFIED","structural_mapping_status":"COMPLETE",
        "response_option_map_matched":True,"usable_for_evidence":True,
        "allowed_as_v551_relation_evidence":True,"n_unweighted":50,"n_respondents":50,
        "pct_unweighted":100.0,"weight_status":"unweighted_only","manual_review_flag":False,
        "source_structure_review_required":False,"question_use_contract_row_hash":"synthetic-claim",
        "question_use_contract_artifact_hash":"synthetic-claim",
    }])
    adj=a.build_v551_directional_candidate_adjudication(bridge)
    atoms,non=a.build_v551_relation_evidence_atoms(bridge)
    cov=a.build_v551_directional_distribution_coverage(adj)
    out.append(("synthetic_v551_promotable",len(atoms)==1 and len(non)==0))
    try:
        built=s.build_v552_structural_outputs(atoms,cov,adj,run_id="L2_SYNTHETIC")
        pressure=built["v552_pressure_observation_index"].iloc[0]["pressure_score"]
        out.append(("synthetic_v552_pressure_score",pressure))
        out.append(("synthetic_v552_conditional_audit_rows",len(built["conditional_determinicity_status_audit"])))
        changed_cond=s.build_v552_structural_outputs(atoms,cov,adj,pd.DataFrame([{"marker":"L2_CHANGED_CONDITIONAL"}]),run_id="L2_SYNTHETIC")
        out.append(("conditional_input_ignored_in_pressure",changed_cond["v552_pressure_observation_index"].iloc[0]["pressure_score"]==pressure and len(changed_cond["conditional_determinicity_status_audit"])==0))
        with tempfile.TemporaryDirectory(prefix="l2-authority-mutation-") as tmp:
            p=Path(tmp)/"registry.csv";m=Path(tmp)/"manifest.json"
            shutil.copyfile(original,p);shutil.copyfile(original_manifest,m)
            data=pd.read_csv(p,dtype=str).fillna("")
            mask=data.response_semantics_contract_hash.eq(key)
            data.loc[mask,"authority_intensity_semantics"]="ORDINAL_COORDINATE"
            data.loc[mask,"neutral_coordinate"]="0"
            data.loc[mask,"negative_endpoint"]="-1"
            data.loc[mask,"positive_endpoint"]="2"
            data.to_csv(p,index=False);update_manifest(m,p)
            a.SCALE_REGISTRY_PATH=p;a.SCALE_REGISTRY_MANIFEST_PATH=m;a._registry_cache=None
            adj2=a.build_v551_directional_candidate_adjudication(bridge)
            atoms2,non2=a.build_v551_relation_evidence_atoms(bridge)
            cov2=a.build_v551_directional_distribution_coverage(adj2)
            built2=s.build_v552_structural_outputs(atoms2,cov2,adj2,run_id="L2_SYNTHETIC")
            changed_score=built2["v552_pressure_observation_index"].iloc[0]["pressure_score"]
            out.append(("synthetic_scale_mutation_changed_v551_v552_pressure",(pressure,changed_score)))
            data.loc[mask,"authority_status"]="REVOKED"
            data.to_csv(p,index=False);update_manifest(m,p)
            a._registry_cache=None
            try:
                a._load_registry()
                out.append(("revocation_rejected",False))
            except RuntimeError as err:
                out.append(("revocation_rejected",str(err)))
            a.SCALE_REGISTRY_PATH=original;a.SCALE_REGISTRY_MANIFEST_PATH=original_manifest;a._registry_cache=None
        badbridge=bridge.copy()
        badbridge.loc[0,"response_semantics_contract_hash"]="L2_UNKNOWN_KEY"
        badadj=a.build_v551_directional_candidate_adjudication(badbridge)
        out.append(("unknown_registry_key",badadj.iloc[0]["adjudication_outcome"]+":"+badadj.iloc[0]["adjudication_reason"]))
    except Exception as e:
        out.append(("synthetic_v552_error",type(e).__name__+":"+str(e)))
    for k,v in out:
        print(f"{k}={v}")

if __name__=="__main__":
    main()
