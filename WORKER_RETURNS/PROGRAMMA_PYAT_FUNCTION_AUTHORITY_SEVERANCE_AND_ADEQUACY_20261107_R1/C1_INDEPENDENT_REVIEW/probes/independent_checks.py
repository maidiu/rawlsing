#!/usr/bin/env python3
"""Minimal independent #777 C1 Q86 evidence checks; read-only metadata/source."""
from __future__ import annotations
import csv, hashlib, json, re, subprocess
from pathlib import Path

ROOT = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-independent-review')
OUT = ROOT/'WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C1_INDEPENDENT_REVIEW'
CSV = Path('/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/afrobarometer_response_option_authority.csv')
R4_SHA = '0c5b385d858033306c6221bcd344b2f69616ff29'
R4_PATH = 'WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/MAINMAC_COMPOUND_RECLOSURE/R4_HISTORICAL_VERSION/01_ALL_58_HISTORICAL_RELEASE_LEDGER.tsv'
HASHES = ['198f189adafd2f4b9e459184a897c8257fa4631f5f940686cd77736cccd38082', '01ceeb78b8b4788c0732afeaab07374140b974fc1e330f79eb9f948e4c1eaa13']

def main():
    data = CSV.read_bytes()
    rows = list(csv.DictReader(data.decode('utf-8-sig').splitlines()))
    out = {'csv': {'path': str(CSV), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'total_rows': len(rows)}}
    q86 = []
    for var in ('Q86A','Q86B'):
        vr = [r for r in rows if r.get('source_family')=='Afrobarometer' and r.get('wave')=='R5' and r.get('var_name')==var]
        q86.append({'variable': var, 'rows': len(vr), 'handling_rules': sorted({r.get('handling_rule','') for r in vr}),
                    'computations': sorted({r.get('recommended_computation','') for r in vr}),
                    'question_types': sorted({r.get('question_type','') for r in vr}),
                    'response_families': sorted({r.get('response_family','') for r in vr}),
                    'statuses': sorted({r.get('response_semantics_status','') for r in vr}),
                    'contract_hashes': sorted({r.get('response_semantics_contract_hash','') for r in vr}),
                    'substantive_codes': sorted({r.get('value_code_raw','') for r in vr if r.get('is_substantive')=='True'}),
                    'special_codes': sorted({r.get('value_code_raw','') for r in vr if r.get('is_substantive')!='True'})})
    out['q86'] = q86
    # Search current rawlsing_next for literal contract hashes.
    hits = {}
    for p in (ROOT/'rawlsing_next').glob('*.py'):
        t = p.read_text(encoding='utf-8', errors='replace')
        for h in HASHES:
            if h in t:
                hits.setdefault(str(p.relative_to(ROOT)), []).append(h)
    out['contract_hash_hits_in_rawlsing_next'] = hits
    # Non-test call sites.
    def callers(symbol):
        res=[]
        for p in (ROOT/'rawlsing_next').rglob('*.py'):
            if '/tests/' in str(p): continue
            t=p.read_text(encoding='utf-8',errors='replace')
            if symbol in t:
                res.append(str(p.relative_to(ROOT)))
        return res
    out['non_test_callers'] = {s: callers(s) for s in ('execute_and_replay_a2_gt1','build_gt1_q86a_i03_plan','build_gt2_q86a_q86b_i03_plan','produce_exact_conditional_support_profile','build_r5_q86_c11_projection')}
    # Source semantics authority construction.
    proj = (ROOT/'rawlsing_next/wave1_r5_q86_c11_projection.py').read_text(encoding='utf-8')
    out['source_semantics_authority'] = {'constant': 'GT12-A-R5-Q86-SOURCE-SEMANTICS' in proj,
        'operation': 'R5_Q86A_Q86B_NATIVE_RESPONSE_SEMANTICS' in proj,
        'line_contains': [i+1 for i,l in enumerate(proj.splitlines()) if 'GT12-A-R5-Q86-SOURCE-SEMANTICS' in l]}
    # R4 AR-0033 ledger row from immutable Git.
    try:
        raw = subprocess.run(['git','-C',str(ROOT),'show',f'{R4_SHA}:{R4_PATH}'],check=True,stdout=subprocess.PIPE).stdout.decode()
        lines = raw.splitlines()
        hdr = lines[0].split('\t')
        row = None
        for line in lines[1:]:
            vals = line.split('\t')
            if vals and vals[0]=='AR-0033': row=dict(zip(hdr,vals)); break
        out['r4_ar0033'] = row
    except Exception as exc:
        out['r4_ar0033'] = {'error': f'{type(exc).__name__}: {exc}'}
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':
    main()
