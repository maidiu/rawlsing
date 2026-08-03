#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, io, json, os, py_compile, sys, tempfile, zipfile
from pathlib import Path
from collections import Counter, defaultdict
from docx import Document
try:
    import yaml
except Exception:
    yaml=None
csv.field_size_limit(sys.maxsize)

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def one(root, pattern):
    xs=list(root.glob(pattern))
    if len(xs)!=1: raise RuntimeError(f'{root}: {pattern}: {xs}')
    return xs[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root',nargs='?',default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--json-out')
    a=ap.parse_args(); root=Path(a.root).resolve()
    failures=[]; checks=[]
    def ck(name,ok,detail=''):
        checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
        if not ok: failures.append({'check':name,'detail':detail})
    # Top-level manifests.
    idx=root/'PACKAGE_INDEX.csv'; sums=root/'SHA256SUMS.csv'
    for m in [idx,sums]:
        rs=rows(m); bad=[]
        for r in rs:
            p=root/r['relative_path']
            if not p.exists() or sha(p)!=r['sha256']: bad.append(r['relative_path'])
            if 'bytes' in r and p.exists() and int(r['bytes'])!=p.stat().st_size: bad.append(r['relative_path']+':size')
        actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p not in (idx,sums)}
        listed={r['relative_path'] for r in rs}
        ck(m.name+':hashes',not bad,json.dumps(bad))
        ck(m.name+':coverage',actual==listed,json.dumps({'actual':len(actual),'listed':len(listed),'only_actual':sorted(actual-listed),'only_listed':sorted(listed-actual)}))
    # Type-aware readability.
    file_count=0
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        file_count+=1; ext=p.suffix.lower()
        try:
            if p.stat().st_size==0: raise ValueError('empty')
            if ext=='.csv':
                with p.open(encoding='utf-8-sig',newline='') as f:
                    r=csv.reader(f); hdr=next(r)
                    for n,row in enumerate(r,2):
                        if len(row)!=len(hdr): raise ValueError(f'row {n} has {len(row)} vs {len(hdr)} columns')
            elif ext=='.json': json.load(p.open(encoding='utf-8'))
            elif ext in ('.yaml','.yml'):
                if yaml is None: raise RuntimeError('PyYAML missing')
                yaml.safe_load(p.read_text(encoding='utf-8'))
            elif ext=='.py':
                compile(p.read_text(encoding='utf-8'),str(p),'exec')
            elif ext=='.docx': Document(p)
            elif ext=='.zip':
                with zipfile.ZipFile(p) as z:
                    if z.testzip() is not None: raise ValueError('bad zip member')
            else: p.open('rb').read(1)
        except Exception as e: failures.append({'check':'readability:'+p.relative_to(root).as_posix(),'detail':repr(e)})
    ck('all_files_type_readable',not any(x['check'].startswith('readability:') for x in failures),str(file_count))
    # Recursive archive integrity.
    seen=set(); archive_instances=0
    def walk(label,data,depth=0):
        nonlocal archive_instances
        archive_instances+=1; seen.add(hashlib.sha256(data).hexdigest())
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            bad=z.testzip()
            if bad: failures.append({'check':'zip:'+label,'detail':bad})
            for i in z.infolist():
                if not i.is_dir() and i.filename.lower().endswith('.zip'): walk(label+'!/'+i.filename,z.read(i),depth+1)
    for p in sorted(root.rglob('*.zip')):
        try: walk(p.relative_to(root).as_posix(),p.read_bytes())
        except Exception as e: failures.append({'check':'zip:'+p.relative_to(root).as_posix(),'detail':repr(e)})
    ck('recursive_zip_integrity',not any(x['check'].startswith('zip:') for x in failures),json.dumps({'instances':archive_instances,'unique_payloads':len(seen)}))
    # Governing source counts and identity universe.
    phase=json.load((root/'08_P2_PHASE0'/'Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json').open())
    by=defaultdict(set)
    for r in phase['question_implementations']: by[r['source_family']].add(r['question_implementation_id'])
    roots={
      'GSS':root/'09_P2_GSS_PASS1','WVS':root/'10_P2_WVS_PASS1','EVS':root/'12_P2_EVS_PASS1',
      'Arab Barometer':root/'15_P2_ARAB_BAROMETER_PASS1','Afrobarometer':root/'19_P2_AFROBAROMETER_PASS1',
      'Asian Barometer':root/'24_P2_ASIAN_BAROMETER_PASS1'/'PACKAGE_CONTENTS',
      'Latinobarómetro':root/'25_P2_LATINOBAROMETRO_PASS1'/'PACKAGE_CONTENTS',
      'South Asia':root/'26_P2_SOUTH_ASIA_PASS1'/'PACKAGE_CONTENTS',
      'LiTS':root/'27_P2_LITS_PASS1'/'PACKAGE_CONTENTS'}
    closure={r['source_family']:r for r in rows(root/'28_P2_ALL_NINE_SOURCE_LOCAL_CLOSURE'/'Rawlsing_P2_All_Nine_Source_Local_Closure_Summary_v2.csv')}
    union=set(); totals=Counter()
    for s,sr in roots.items():
        nodes=rows(one(sr,'**/*Deep_Question_Node_Catalog*.csv')); ids={r['question_implementation_id'] for r in nodes}; union|=ids
        gaps_files=list(sr.glob('**/*Response_Authority_Gaps*.csv'))
        if gaps_files: gaps=rows(gaps_files[0])
        else: gaps=[r for r in nodes if 'gap' in r.get('response_binding_status','').lower() or r.get('response_binding_status') in ('unbound','blocked')]
        edges=rows(one(sr,'**/*Accepted_Longitudinal_Continuity_Edges*.csv'))
        inv=rows(one(sr,'**/*Source_Structure_Inventory*.csv'))
        c=closure[s]
        ck(s+':phase0_identity',ids==by[s],json.dumps({'deep':len(ids),'phase0':len(by[s])}))
        ck(s+':counts',len(nodes)==int(c['nodes']) and len(gaps)==int(c['response_gaps']) and len(edges)==int(c['accepted_continuity_edges']) and len(inv)==int(c['source_structures']),json.dumps({'nodes':len(nodes),'gaps':len(gaps),'edges':len(edges),'structures':len(inv)}))
        bad_edges=[r for r in edges if r['left_question_implementation_id'] not in ids or r['right_question_implementation_id'] not in ids or r['left_question_implementation_id']==r['right_question_implementation_id']]
        ck(s+':edge_referential_integrity',not bad_edges,str(len(bad_edges)))
        mem=list(sr.glob('**/*Source_Structure_Memberships*.csv'))
        if mem:
            m=rows(mem[0]); sidkey='structure_id' if 'structure_id' in inv[0] else 'source_structure_id'; msidkey='structure_id' if 'structure_id' in m[0] else 'source_structure_id'
            sids={r[sidkey] for r in inv}; nodekeys={(r.get('wave',''),r.get('source_variable_code','')) for r in nodes}
            bad=[r for r in m if r[msidkey] not in sids or (('question_implementation_id' in r and r['question_implementation_id'] not in ids) if 'question_implementation_id' in r else ((r.get('wave',''),r.get('source_variable_code','')) not in nodekeys))]
            ck(s+':structure_membership_integrity',not bad,str(len(bad)))
        totals['nodes']+=len(nodes); totals['gaps']+=len(gaps); totals['bound']+=len(nodes)-len(gaps); totals['edges']+=len(edges); totals['structures']+=len(inv)
    phaseall=set().union(*by.values())
    ck('all_nine_union_exact_phase0',union==phaseall,json.dumps({'union':len(union),'phase0':len(phaseall),'missing':len(phaseall-union),'extra':len(union-phaseall)}))
    ck('global_totals',dict(totals)=={'nodes':18276,'gaps':1968,'bound':16308,'edges':4759,'structures':2499},json.dumps(totals))
    cur=json.load((root/'00_START_HERE'/'CURRENT_STATE.json').open()); scope=json.load((root/'00_START_HERE'/'SCOPE_LOCK.json').open()); val=json.load((root/'VALIDATION.json').open())
    ck('restart_controls_current',cur.get('handoff_version')=='v11' and scope.get('current_pass')==cur.get('current_pass') and val.get('next_pass')=='P2_GLOBAL_CROSS_SOURCE_RECONCILIATION' and len(val.get('source_local_deep_passes_closed',[]))==9,'')
    result={'status':'PASS' if not failures else 'FAIL','root':str(root),'checks_passed':sum(x['status']=='PASS' for x in checks),'checks_total':len(checks),'failures':failures,'checks':checks}
    out=json.dumps(result,indent=2,ensure_ascii=False)
    if a.json_out: Path(a.json_out).write_text(out+'\n',encoding='utf-8')
    print(out)
    raise SystemExit(0 if not failures else 1)
if __name__=='__main__': main()
