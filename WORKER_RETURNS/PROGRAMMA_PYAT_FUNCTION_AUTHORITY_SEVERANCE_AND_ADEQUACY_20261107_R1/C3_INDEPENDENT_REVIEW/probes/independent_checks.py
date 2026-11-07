#!/usr/bin/env python3
"""Minimal C3 independent checks: source blobs, receipts, repo-wide non-test callers."""
from __future__ import annotations
import csv, hashlib, json, subprocess
from pathlib import Path

ROOT = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-ff-postff-independent-review')
C3 = ROOT/'WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C3_FF_POSTFF_CONSUMER'

def main():
    out = {}
    rows = list(csv.DictReader((C3/'06_HASH_AND_SOURCE_MANIFEST.tsv').open(), delimiter='\t'))
    sources = [r for r in rows if r['kind']=='source']
    src = []
    for r in sources:
        p = ROOT/r['path_or_register']
        actual_blob = subprocess.run(['git','hash-object','--no-filters',str(p)],check=True,stdout=subprocess.PIPE,text=True).stdout.strip()
        actual_sha = hashlib.sha256(p.read_bytes()).hexdigest()
        src.append({'path':r['path_or_register'],'blob_match':actual_blob==r['git_blob_sha1'],'sha_match':actual_sha==r['sha256'],'bytes':p.stat().st_size})
    out['source_blobs'] = {'rows':len(src),'all_match':all(x['blob_match'] and x['sha_match'] for x in src),'bad':[x for x in src if not (x['blob_match'] and x['sha_match'])]}
    aj = list(csv.DictReader((C3/'05_REGISTER_ANTIJOIN.tsv').open(), delimiter='\t'))
    out['antijoin'] = {'rows':len(aj),'unmatched':sum(1 for r in aj if r['case_id_or_status'].startswith('UNMATCHED'))}
    symbols = ['produce_exact_conditional_support_profile','admit_gt12_c_relation','prepare_typed_d_to_e_relation_basis','compute_pair_support_signature','select_r05_world_view','configure_evidence_world_context']
    calls = {}
    for s in symbols:
        hits=[]
        for p in (ROOT/'rawlsing_next').rglob('*.py'):
            if '/tests/' in str(p): continue
            if s in p.read_text(encoding='utf-8',errors='replace'): hits.append(str(p.relative_to(ROOT)))
        calls[s]=hits
    out['non_test_symbol_files'] = calls
    # imports of FF/GT12/GF1/FFX module names outside tests
    mods = ['field_forge_conditional_support','gt12_c_to_d_relation_bridge','gt12_d_to_m4_typed_bridge','gf1_pair_support_consumer','ffx002_r2_integrated_stack','ffx002_r2_local_geometry']
    imp = {}
    for m in mods:
        hits=[]
        for p in (ROOT/'rawlsing_next').rglob('*.py'):
            if '/tests/' in str(p): continue
            t=p.read_text(encoding='utf-8',errors='replace')
            if m in t: hits.append(str(p.relative_to(ROOT)))
        imp[m]=hits
    out['module_name_files'] = imp
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
