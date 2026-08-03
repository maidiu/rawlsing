from __future__ import annotations
import argparse,csv,hashlib,json,os,sys
from pathlib import Path
ROOT_SECTION='52_P3A_V7_PHASE3_OBJECT_GRAPH_AND_VERTICAL_SLICE'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--output'); a=ap.parse_args(); root=Path(a.root)
    checks=[]
    def ck(name,cond,detail=''):
        checks.append({'name':name,'pass':bool(cond),'detail':str(detail)})
    st=json.loads((root/'00_START_HERE/CURRENT_STATE.json').read_text())
    ck('state_v30_blocked',st.get('handoff_version')=='v30' and st.get('latest_section')==ROOT_SECTION)
    sec=root/ROOT_SECTION
    blocker=json.loads((sec/'outputs/P3A_PHASE3_BLOCKER_REPRODUCER.json').read_text())
    ck('blocker_present',blocker.get('sqlstate')=='42703' and blocker.get('classification')=='GOVERNING_V7_CONTRACT_DDL_BINDING_CONTRADICTION')
    bind=list(csv.DictReader((root/'49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v7.csv').open()))
    ck('stale_binding_present',any(r['table_name']=='p3_lineage_disposition' and r['column_name']=='subject_type' for r in bind))
    pkg=list(csv.DictReader((root/'PACKAGE_INDEX.csv').open()))
    bad=[]
    for r in pkg:
        p=root/r['relative_path']
        if not p.exists() or p.stat().st_size!=int(r['bytes']) or sha(p)!=r['sha256']:
            bad.append(r['relative_path'])
    ck('package_manifest_hashes',not bad,bad[:5])
    result={'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks),'failures':[c for c in checks if not c['pass']]}
    text=json.dumps(result,indent=2)+'\n'; print(text,end='')
    if a.output: Path(a.output).write_text(text)
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
