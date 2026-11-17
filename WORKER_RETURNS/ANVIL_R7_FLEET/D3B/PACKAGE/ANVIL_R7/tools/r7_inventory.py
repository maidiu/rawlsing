#!/usr/bin/env python3
"""Source-qualified 118 identity inventory for the active ANVIL R7 instrument.

This is S1 documentary accounting.  It does NOT accept 118 functions, adopt the
26 prospective rows, close the 14 held proofs, authenticate survey rights, or
select an architecture.  Every identity is reconstructed from exact pinned
bytes and carries a row/file origin hash.

The legacy R5/R6 SPINE is deliberately NOT required.  A completed P2 SPINE was
an expected R5 output, not a historical input; requiring one creates a fake
"source" and a circular transfer check.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, subprocess, sys

SCHEMA='ANVIL_R7_SOURCE_IDENTITY_INVENTORY'
GROUPS=('K1_CAP','PYAT_PC','P4R','SEAM_B','SEAM_S','ANVIL_L','BOUNDARY','TERMINAL')
GROUP_COUNTS={'K1_CAP':29,'PYAT_PC':26,'P4R':14,'SEAM_B':10,'SEAM_S':8,'ANVIL_L':8,'BOUNDARY':7,'TERMINAL':16}
HEX40=re.compile(r'^[a-f0-9]{40}$'); HEX64=re.compile(r'^[a-f0-9]{64}$')

def sha(b): return hashlib.sha256(b).hexdigest()
def good(x,n=12): return isinstance(x,str) and len(x.strip())>=n and x.strip().lower() not in {
    'todo','tbd','placeholder','to be determined','see above','n/a','not applicable','unknown'}

def _rows(path):
    text=path.read_text(encoding='utf-8')
    lines=text.splitlines()
    return lines

def _tsv_rows(path):
    lines=_rows(path); header=lines[0].split('\t'); out=[]
    for line in lines[1:]:
        if line.strip():
            rec=dict(zip(header,line.split('\t'))); rec['_raw']=line; rec['_sha256']=sha(line.encode())
            out.append(rec)
    return header,out

def _markdown_rows(path,prefix):
    out=[]; lines=_rows(path)
    for line in lines:
        s=line.strip()
        if s.startswith('| **'+prefix) or s.startswith('|**'+prefix):
            out.append(s)
    return out

def _boundary_contracts(zip_root):
    return json.loads((zip_root/'02_BOUNDARY_CONTRACTS.json').read_text())

def _terminal_ids(zip_root):
    o=json.loads((zip_root/'03_FROZEN_SOURCE_CUTS.json').read_text())
    return list(o['mandatory']['TERMINAL']),o

def _file_pin(source_root,rel,commit,git_path,git_blob,extra=None):
    p=source_root/rel
    if not p.is_file(): raise SystemExit('missing source file: '+str(p))
    b=p.read_bytes()
    d={'path':rel,'sha256':sha(b),'commit':commit,'git_path':git_path,'git_blob':git_blob,'bytes':len(b)}
    for k in ('source_kind','zip_sha256'):
        if extra and k in extra: d[k]=extra[k]
    return d

def build_inventory(source_root,manifest_path,zip_root):
    source_root=pathlib.Path(source_root);zip_root=pathlib.Path(zip_root)
    man=json.loads(pathlib.Path(manifest_path).read_text())
    pins={x['path']:x for x in man['files']}
    files=[]
    for rel in pins:
        x=pins[rel];files.append(_file_pin(source_root,rel,x.get('commit'),x.get('git_path',rel),x.get('git_blob'),x))
    entries=[]
    def add(group,rid,necessity,semantics,negative,consumer,why,excerpt,origin,source_file,extra=None):
        e={'group':group,'id':rid,'necessity':necessity,'status':'SOURCE_AUTHENTICATED_IDENTITY',
           'source_file':source_file,'source_anchor':pins[source_file].get('commit','ZIP')+':'+pins[source_file].get('git_path',source_file),
           'source_excerpt':excerpt,'source_semantics':semantics,'negative_meaning':negative,
           'consumer_or_hold':consumer,'why':why,'origin_sha256':origin,'evidence_ids':['SRC:'+rid]}
        if len(consumer.strip())<8: consumer='COMPETENT_OWNER_HELD: '+consumer
        e['consumer_or_hold']=consumer
        if extra: e.update(extra)
        entries.append(e)
    # K3 exact TSV rows
    h,cap=_tsv_rows(source_root/'K3_CAP_29.tsv')
    for r in cap:
        add('K1_CAP',r['capability_id'],'HISTORICAL_FUNCTION',
            (r.get('historical_paths','')+' | '+r.get('actual_current_first_reader_or_hold','')).strip(),
            r.get('P2_accepted_falsifier_correction','') or 'No accepted falsifier correction; historical negative retained.',
            r.get('existing_owner','') or 'COMPETENT_OWNER_HELD',
            'K3 protected 29-row conservation identity; not proof of native runtime equivalence. '+r.get('receiving',''),
            r['_raw'],r['_sha256'],'K3_CAP_29.tsv',{'k3_blob':pins['K3_CAP_29.tsv']['git_blob']})
    h,pc=_tsv_rows(source_root/'K3_PC_26.tsv')
    for r in pc:
        add('PYAT_PC',r['proposal_id'],'HISTORICAL_NOT_ADOPTED',
            (r.get('original_topic','')+' | '+r.get('selected_source_requirement','')).strip(),
            r.get('negative_or_nonclaim','') or 'NOT_ADOPTED; no negative claim adopted.',
            r.get('source_owner','') or 'COMPETENT_OWNER_HELD: original requirement remains NOT_ADOPTED',
            '26 prospective owner-decision rows remain NOT_ADOPTED; no new requirement is created. '+r.get('native_science_actor_protection',''),
            r['_raw'],r['_sha256'],'K3_PC_26.tsv',{'k3_blob':pins['K3_PC_26.tsv']['git_blob'],'adopted':False,'closed':False})
    h,p4=_tsv_rows(source_root/'K3_P4R_14.tsv')
    for r in p4:
        add('P4R',r['P4R_id'],'HISTORICAL_PROOF_HELD',
            (r.get('original_unproved_edge','')+' | '+r.get('next_bounded_test','')).strip(),
            r.get('HQ_route','') or 'HELD; no proof closure.',
            r.get('original_competent_owner','') or 'COMPETENT_OWNER_HELD',
            'Original P4R proof obligation remains HELD; no finite proof is declared closed. '+r.get('permission_and_native_ceiling',''),
            r['_raw'],r['_sha256'],'K3_P4R_14.tsv',{'k3_blob':pins['K3_P4R_14.tsv']['git_blob'],'adopted':False,'closed':False})
    # SEAM/25 B rows
    for line in _markdown_rows(source_root/'SEAM_25.md','B-'):
        rid=re.search(r'\*\*(B-\d\d)',line).group(1)
        add('SEAM_B',rid,'BOUNDARY_TRANSFORMATION_QUESTION',line,line,
            re.search(r'\|([^|]+)\|\s*$',line).group(1).strip() if line.count('|')>=4 else 'SEAM owner held',
            'SEAM/25 boundary transformation question, not an executed function.',line,sha(line.encode()),'SEAM_25.md')
    for line in _markdown_rows(source_root/'SEAM_26.md','S-'):
        rid=re.search(r'\*\*(S-\d\d)',line).group(1)
        add('SEAM_S',rid,'REVERSE_CONSUMER_REQUIREMENT',line,line,
            'Existing owner/status carried in the exact SEAM/26 row; downstream science remains held.',
            'SEAM/26 social-field/person reverse requirement, not an eight-table C11 mandate.',line,sha(line.encode()),'SEAM_26.md')
    for line in _markdown_rows(source_root/'ANVIL_15.md','L-'):
        rid=re.search(r'\*\*(L-\d\d)',line).group(1)
        add('ANVIL_L',rid,'IRREVERSIBLE_INFORMATION_RISK',line,line,
            re.search(r'\|([^|]+)\|\s*$',line).group(1).strip() if line.count('|')>=4 else 'ANVIL owner held',
            'ANVIL/15 irreversible source-to-C11 information-loss risk; conservation requirement, not proof of implementation.',line,sha(line.encode()),'ANVIL_15.md')
    # T1-T7 exact contracts from supplied ZIP
    bc=_boundary_contracts(zip_root)
    for b in bc['boundaries']:
        add('BOUNDARY',b['id'],'BOUNDARY_CONTRACT',
            b['name']+' | producer: '+b['producers']+' | receiver: '+b['receivers']+' | preserve: '+b['must_preserve'],
            b['veto'],b['receivers'],'Seven architectural interrogations, not seven new pipeline stages or independently accredited science.',
            ('"id":"'+b['id']+'"'),sha(('"id":"'+b['id']+'"').encode()),
            '02_BOUNDARY_CONTRACTS.json',{'contract_name':b['name'],'time_class':b['time_class'],'owner':b['owners']})
    # 16 terminal identifiers from supplied ZIP
    terminal,raw=_terminal_ids(zip_root)
    for rid in terminal:
        add('TERMINAL',rid,'TERMINAL_IDENTITY',rid+' | '+json.dumps(raw.get('mandatory',{}).get('TERMINAL',[]),ensure_ascii=False),
            'TERMINAL_INCLUSION_IS_NOT_ACCEPTANCE_OR_IMPLEMENTATION', 'Terminal owner/consumer remains scope- and authority-qualified.',
            'Terminal identifier included for whole-machine scope analysis; not implemented or accepted by inventory.',
            ('"'+rid+'"'),sha(('"'+rid+'"').encode()),'03_FROZEN_SOURCE_CUTS.json')
    inv={'schema':SCHEMA,'status':'SOURCE_AUTHENTICATED_IDENTITY_INVENTORY_S1_DOCUMENTARY',
         'source_authentication':'EXACT_BYTES_PINNED_GIT_UNVERIFIED',
         'meaning':'118 mixed source/contract identities; NOT 118 adopted functions or requirements.',
         'counts':{g:sum(1 for e in entries if e['group']==g) for g in GROUPS},
         'total':len(entries),'source_files':files,'entries':entries}
    return inv

def _verify_file(src,e,repo,errors,code):
    rel=e.get('path');base=pathlib.Path(src).resolve()
    if not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts:
        errors.append(code+':INVALID_PATH');return None
    p=(base/rel).resolve()
    if not p.is_relative_to(base) or not p.is_file():errors.append(code+':MISSING_SOURCE_FILE');return None
    b=p.read_bytes()
    if sha(b)!=e.get('sha256'):errors.append(code+':BYTES_CHANGED');return None
    if repo:
        if e.get('source_kind')=='SUPPLIED_ZIP':
            if e.get('zip_sha256') and not HEX64.fullmatch(str(e.get('zip_sha256'))):
                errors.append(code+':BAD_ZIP_PIN')
            return b
        commit=e.get('commit');git_path=e.get('git_path');blob=e.get('git_blob')
        if not (isinstance(commit,str) and HEX40.fullmatch(commit) and isinstance(git_path,str) and isinstance(blob,str) and re.fullmatch(r'[a-f0-9]{40}',blob)):
            errors.append(code+':INCOMPLETE_GIT_PIN');return b
        try:
            t=subprocess.run(['git','-C',str(repo),'cat-file','-t',commit],capture_output=True,text=True,timeout=8)
            if t.returncode or t.stdout.strip()!='commit':errors.append(code+':COMMIT_NOT_FOUND');return b
            r=subprocess.run(['git','-C',str(repo),'rev-parse',commit+':'+git_path],capture_output=True,text=True,timeout=8)
            if r.returncode or r.stdout.strip()!=blob:errors.append(code+':GIT_BLOB_MISMATCH');return b
            g=subprocess.run(['git','-C',str(repo),'show',commit+':'+git_path],capture_output=True,timeout=8)
            if g.returncode or sha(g.stdout)!=e.get('sha256'):errors.append(code+':GIT_BYTES_MISMATCH');return b
        except (OSError,subprocess.SubprocessError):errors.append(code+':GIT_UNAVAILABLE');return b
    return b

def check_inventory(inv,source_root,repo=None):
    e=[]
    if not isinstance(inv,dict) or inv.get('schema')!=SCHEMA:return {'status':'RED','errors':['INVENTORY:BAD_SCHEMA']}
    if inv.get('status')!='SOURCE_AUTHENTICATED_IDENTITY_INVENTORY_S1_DOCUMENTARY':e.append('INVENTORY:FALSE_STATUS')
    if inv.get('source_authentication') not in ('EXACT_BYTES_PINNED_GIT_UNVERIFIED','GIT_OBJECT_BLOB_AND_BYTES_VERIFIED'):
        e.append('INVENTORY:FALSE_AUTHENTICATION_GRADE')
    if source_root is None:e.append('INVENTORY:NO_SOURCE_ROOT');return {'status':'RED','errors':e}
    files=inv.get('source_files')
    if not isinstance(files,list) or not files:e.append('INVENTORY:NO_SOURCE_FILES');files=[]
    fmap={};bodies={}
    for i,f in enumerate(files):
        if not isinstance(f,dict):e.append('INVENTORY:BAD_SOURCE_FILE');continue
        fmap[f.get('path')]=f
        b=_verify_file(source_root,f,repo,e,'INVENTORY:FILE:'+str(f.get('path')))
        if b is not None:bodies[f.get('path')]=b
    if repo and len(bodies)==len(files) and not any(x.startswith('INVENTORY:FILE:') for x in e):
        inv_auth='GIT_OBJECT_BLOB_AND_BYTES_VERIFIED'
    else:inv_auth='EXACT_BYTES_PINNED_GIT_UNVERIFIED'
    if inv.get('source_authentication')=='GIT_OBJECT_BLOB_AND_BYTES_VERIFIED' and inv_auth!='GIT_OBJECT_BLOB_AND_BYTES_VERIFIED':
        e.append('INVENTORY:FALSE_GIT_AUTHENTICATION')
    entries=inv.get('entries')
    if not isinstance(entries,list):e.append('INVENTORY:NO_ENTRIES');entries=[]
    counts={g:0 for g in GROUPS};ids={g:set() for g in GROUPS};byid={}
    for x in entries:
        if not isinstance(x,dict):e.append('INVENTORY:BAD_ENTRY');continue
        g=x.get('group');rid=x.get('id')
        if g not in GROUPS or not isinstance(rid,str):e.append('INVENTORY:BAD_GROUP_OR_ID');continue
        counts[g]+=1
        if rid in ids[g]:e.append('INVENTORY:DUPLICATE_ID:'+rid)
        ids[g].add(rid);byid[rid]=x
        for k in ('source_anchor','source_excerpt','source_semantics','negative_meaning','consumer_or_hold','why','origin_sha256','source_file'):
            if not good(x.get(k),3 if k=='source_excerpt' else 8):e.append('INVENTORY:VACUOUS:'+rid+':'+k)
        sf=x.get('source_file')
        if sf not in fmap:e.append('INVENTORY:ORPHAN_SOURCE_FILE:'+rid);continue
        b=bodies.get(sf)
        if b is None:continue
        text=b.decode('utf-8','replace')
        if x.get('source_excerpt') not in text:e.append('INVENTORY:EXCERPT_NOT_IN_SOURCE:'+rid)
        if x.get('origin_sha256')!=sha(x.get('source_excerpt','').encode()):e.append('INVENTORY:ROW_HASH_MISMATCH:'+rid)
        if g in ('PYAT_PC','P4R'):
            if x.get('adopted') is not False:e.append('INVENTORY:UNAUTHORIZED_ADOPTION:'+rid)
        if g=='P4R' and x.get('closed') is not False:e.append('INVENTORY:FALSE_PROOF_CLOSURE:'+rid)
    for g in GROUPS:
        if counts[g]!=GROUP_COUNTS[g]:e.append('INVENTORY:COUNT_DRIFT:'+g+':'+str(counts[g]))
    if len(entries)!=118:e.append('INVENTORY:TOTAL_NOT_118')
    # Exact K3 row set/hash census against the source file, not against the inventory itself.
    for g,fname in (('K1_CAP','K3_CAP_29.tsv'),('PYAT_PC','K3_PC_26.tsv'),('P4R','K3_P4R_14.tsv')):
        b=bodies.get(fname)
        if not b:continue
        lines=b.decode('utf-8').splitlines();actual={}
        for line in lines[1:]:
            if line.strip():actual[line.split('\t',1)[0]]=sha(line.encode())
        if set(actual)!=ids[g]:e.append('INVENTORY:K3_ID_CENSUS_CHANGED:'+g)
        for rid,h in actual.items():
            if byid.get(rid,{}).get('origin_sha256')!=h:e.append('INVENTORY:K3_ROW_HASH_MISMATCH:'+rid)
    return {'status':'RED' if e else 'PASS_SOURCE_IDENTITY_INVENTORY_S1_DOCUMENTARY',
            'errors':sorted(set(e)),'counts':counts,'total':len(entries),
            'source_authentication':inv_auth}

def main():
    ap=argparse.ArgumentParser(description='Build or verify the source-qualified 118 identity inventory (S1 documentary, no architecture)')
    ap.add_argument('action',choices=['build','verify'])
    ap.add_argument('--source-root',required=True);ap.add_argument('--manifest');ap.add_argument('--zip-root')
    ap.add_argument('--inventory');ap.add_argument('--repo');ap.add_argument('--out')
    a=ap.parse_args()
    if a.action=='build':
        if not (a.manifest and a.zip_root):raise SystemExit('build requires --manifest and --zip-root')
        inv=build_inventory(a.source_root,a.manifest,a.zip_root)
        b=(json.dumps(inv,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
        if a.out:pathlib.Path(a.out).write_bytes(b);print(json.dumps({'status':'BUILT','path':a.out,'sha256':sha(b),'total':inv['total'],'counts':inv['counts']},indent=2))
        else:sys.stdout.write(b.decode())
        return 0
    inv=json.loads(pathlib.Path(a.inventory).read_text())
    out=check_inventory(inv,a.source_root,a.repo)
    print(json.dumps(out,indent=2));return 0 if out['status'].startswith('PASS') else 2

if __name__=='__main__':sys.exit(main())
