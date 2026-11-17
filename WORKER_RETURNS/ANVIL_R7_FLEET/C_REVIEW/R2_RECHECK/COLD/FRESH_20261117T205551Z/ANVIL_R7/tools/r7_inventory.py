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
ORIGINAL_ZIP_SHA='526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332'
# Freeze of the authored source-bounded summaries/negatives (D2A/D2B-integrated).
# This is NOT machine proof of source truth; it prevents silent replacement of
# an authored interpretation while retaining the exact source row hash.
SEMANTIC_FREEZE='71714bbf9418513b898a57ac1d267d56a0f1bafdd89fe8ef73310460c4caa0e0'
K3ROOT='PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/K3_HQ_POST_AB_OWNER_DECISIONS_20261116_R1/'
# Independently pinned origin for every family.  The caller may not choose a
# provenance kind, commit, path, blob, ZIP member or expected byte hash.
CANON_PINS={
 'K3_CAP_29.tsv':{'kind':'GIT','commit':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','git_path':K3ROOT+'K3_CONSERVATION_VS_IMPLEMENTATION_29.tsv','git_blob':'a91214b9fd89ab97897ec1c3cd48cb5285b7029c','sha256':'0dfe6539f1a1f7f028c5968c0e85078cbf5f80a847d0c94ea1929f57d20c052d'},
 'K3_PC_26.tsv':{'kind':'GIT','commit':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','git_path':K3ROOT+'K3_R15_26_OWNER_DECISIONS.tsv','git_blob':'1f5a3ae8a40593dccf34753c9fa9577155ebf163','sha256':'6d0766ecc637ee03a705c1772e7bcda39c09c9534f0672cd36a27cfa85e0dfa2'},
 'K3_P4R_14.tsv':{'kind':'GIT','commit':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','git_path':K3ROOT+'K3_P4R_14_OBLIGATION_ROUTES.tsv','git_blob':'5a84ca8cb0a2b16d4a68b2200fa426fd9451b343','sha256':'8adf74cfbf2e916f41641f5836ab82305059b59e1665a2e1647dfb6bdeb0e9d3'},
 'SEAM_25.md':{'kind':'GIT','commit':'596f1230258ff50f98d8543dec42a80e696720f4','git_path':'SEAM/25_RETURN_TO_BOUNDARY_TRANSFORMATIONS_AND_OPEN_REGISTER_R1.md','git_blob':'181ab1aaee26d71524dd7401a59c2ca550b4a81c','sha256':'589379644edbb9f59734d5fe40787683e6836b073a3ba69649cfd5035432c17e'},
 'SEAM_26.md':{'kind':'GIT','commit':'796452b8cb788fa5a02f37a7ce86eafce8312dfe','git_path':'SEAM/26_CONDITIONED_SOCIAL_FIELD_IDENTIFICATION_AND_GENERATIVE_PERSON_REVERSE_CONTRACT_R1.md','git_blob':'a05c21dd0b7b1d404fc500c0ef36c81aee67c96e','sha256':'a53c62b3f68a54947a26be2e8878d1f89bff1ad057833ef4f8c80f38ab9fb50c'},
 'ANVIL_15.md':{'kind':'GIT','commit':'3cc09bba3d0e26c226da0ddca4b64c43dd74e493','git_path':'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/ANVIL/15_SEAM_REVERSE_CONSUMER_SOCIAL_FIELD_AND_C11_DESIGN_IMPLICATIONS_R1.md','git_blob':'6253a632d10f201e0bf446f055f96c82fb4a479f','sha256':'0e09bc34235923b7f7b34d272b8e7cddcea0d4e524953f56665843bba6a0c50a'},
 '02_BOUNDARY_CONTRACTS.json':{'kind':'ZIP','zip_sha256':ORIGINAL_ZIP_SHA,'zip_member':'ANVIL_R7/02_BOUNDARY_CONTRACTS.json','sha256':'89db35d554bbc693eac14595964ab1fe5574bc521e1ab9438e677c48c256502a'},
 '03_FROZEN_SOURCE_CUTS.json':{'kind':'ZIP','zip_sha256':ORIGINAL_ZIP_SHA,'zip_member':'ANVIL_R7/03_FROZEN_SOURCE_CUTS.json','sha256':'cf26afb1264ce0ff44c1159e4143a261928f8712db33a7a07c1d0763565ba854'},
}

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

def _file_pin(source_root,rel):
    if rel not in CANON_PINS: raise SystemExit('unpinned source file: '+rel)
    pin=CANON_PINS[rel];p=pathlib.Path(source_root)/rel
    if not p.is_file(): raise SystemExit('missing source file: '+str(p))
    b=p.read_bytes();d={'path':rel,'sha256':sha(b)}
    if pin['kind']=='GIT': d.update(kind='GIT',commit=pin['commit'],git_path=pin['git_path'],git_blob=pin['git_blob'])
    else: d.update(kind='ZIP',zip_sha256=pin['zip_sha256'],zip_member=pin['zip_member'])
    return d

def build_inventory(source_root,manifest_path,zip_root):
    source_root=pathlib.Path(source_root);zip_root=pathlib.Path(zip_root)
    files=[]
    for rel in CANON_PINS:
        files.append(_file_pin(source_root,rel))
    pins={rel:CANON_PINS[rel] for rel in CANON_PINS}
    entries=[]
    def add(group,rid,necessity,semantics,negative,consumer,why,excerpt,origin,source_file,extra=None):
        e={'group':group,'id':rid,'necessity':necessity,'status':'SOURCE_AUTHENTICATED_IDENTITY',
           'source_file':source_file,'source_anchor':(pins[source_file]['commit']+':'+pins[source_file]['git_path']) if pins[source_file]['kind']=='GIT' else ('ZIP:'+pins[source_file]['zip_member']),
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
            r['_raw'],r['_sha256'],'K3_CAP_29.tsv',{'k3_blob':CANON_PINS['K3_CAP_29.tsv']['git_blob']})
    h,pc=_tsv_rows(source_root/'K3_PC_26.tsv')
    for r in pc:
        add('PYAT_PC',r['proposal_id'],'HISTORICAL_NOT_ADOPTED',
            (r.get('original_topic','')+' | '+r.get('selected_source_requirement','')).strip(),
            r.get('negative_or_nonclaim','') or 'NOT_ADOPTED; no negative claim adopted.',
            r.get('source_owner','') or 'COMPETENT_OWNER_HELD: original requirement remains NOT_ADOPTED',
            '26 prospective owner-decision rows remain NOT_ADOPTED; no new requirement is created. '+r.get('native_science_actor_protection',''),
            r['_raw'],r['_sha256'],'K3_PC_26.tsv',{'k3_blob':CANON_PINS['K3_PC_26.tsv']['git_blob'],'adopted':False,'closed':False})
    h,p4=_tsv_rows(source_root/'K3_P4R_14.tsv')
    for r in p4:
        add('P4R',r['P4R_id'],'HISTORICAL_PROOF_HELD',
            (r.get('original_unproved_edge','')+' | '+r.get('next_bounded_test','')).strip(),
            r.get('HQ_route','') or 'HELD; no proof closure.',
            r.get('original_competent_owner','') or 'COMPETENT_OWNER_HELD',
            'Original P4R proof obligation remains HELD; no finite proof is declared closed. '+r.get('permission_and_native_ceiling',''),
            r['_raw'],r['_sha256'],'K3_P4R_14.tsv',{'k3_blob':CANON_PINS['K3_P4R_14.tsv']['git_blob'],'adopted':False,'closed':False})
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
         'source_authentication':'GIT_AND_ZIP_PINS_VERIFIED',
         'meaning':'118 mixed source/contract identities; NOT 118 adopted functions or requirements.',
         'counts':{g:sum(1 for e in entries if e['group']==g) for g in GROUPS},
         'total':len(entries),'source_files':files,'entries':entries}
    return inv

def _verify_file(src,e,repo,zip_path,errors,code):
    rel=e.get('path');base=pathlib.Path(src).resolve()
    if not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts:
        errors.append(code+':INVALID_PATH');return None
    pin=CANON_PINS.get(rel)
    if pin is None:errors.append(code+':UNPINNED_SOURCE_FILE');return None
    p=(base/rel).resolve()
    if not p.is_relative_to(base) or not p.is_file():errors.append(code+':MISSING_SOURCE_FILE');return None
    b=p.read_bytes()
    if sha(b)!=pin['sha256']:errors.append(code+':BYTES_NOT_CANONICAL');return None
    if e.get('sha256')!=pin['sha256']:errors.append(code+':INVENTORY_HASH_NOT_CANONICAL');return None
    if pin['kind']=='GIT':
        if e.get('kind')!='GIT' or e.get('source_kind') not in (None,'GIT'):
            errors.append(code+':PROVENANCE_KIND_MISMATCH');return None
        if e.get('commit')!=pin['commit'] or e.get('git_path')!=pin['git_path'] or e.get('git_blob')!=pin['git_blob']:
            errors.append(code+':GIT_PIN_NOT_CANONICAL');return None
        if not repo:
            errors.append(code+':REPO_REQUIRED_FOR_GIT_ORIGIN');return None
        commit=pin['commit'];git_path=pin['git_path'];blob=pin['git_blob']
        try:
            t=subprocess.run(['git','-C',str(repo),'cat-file','-t',commit],capture_output=True,text=True,timeout=8)
            if t.returncode or t.stdout.strip()!='commit':errors.append(code+':COMMIT_NOT_FOUND');return None
            r=subprocess.run(['git','-C',str(repo),'rev-parse',commit+':'+git_path],capture_output=True,text=True,timeout=8)
            if r.returncode or r.stdout.strip()!=blob:errors.append(code+':GIT_BLOB_MISMATCH');return None
            g=subprocess.run(['git','-C',str(repo),'show',commit+':'+git_path],capture_output=True,timeout=8)
            if g.returncode or sha(g.stdout)!=pin['sha256']:errors.append(code+':GIT_BYTES_MISMATCH');return None
        except (OSError,subprocess.SubprocessError):errors.append(code+':GIT_UNAVAILABLE');return None
        return b
    # ZIP origin is bound to the original uploaded archive and exact member.
    if e.get('kind')!='ZIP' or e.get('source_kind') not in (None,'ZIP'):
        errors.append(code+':PROVENANCE_KIND_MISMATCH');return None
    if e.get('zip_sha256')!=ORIGINAL_ZIP_SHA or e.get('zip_member')!=pin['zip_member']:
        errors.append(code+':ZIP_PIN_NOT_CANONICAL');return None
    if not zip_path:
        errors.append(code+':ZIP_REQUIRED_FOR_ZIP_ORIGIN');return None
    try:
        zb=pathlib.Path(zip_path).read_bytes()
        if sha(zb)!=ORIGINAL_ZIP_SHA:errors.append(code+':ORIGINAL_ZIP_HASH_MISMATCH');return None
        import zipfile
        with zipfile.ZipFile(pathlib.Path(zip_path)) as z:
            member=z.read(pin['zip_member'])
        if sha(member)!=pin['sha256']:errors.append(code+':ZIP_MEMBER_BYTES_MISMATCH');return None
    except (OSError,KeyError,zipfile.BadZipFile):errors.append(code+':ZIP_MEMBER_UNREADABLE');return None
    return b

def check_inventory(inv,source_root,repo=None,zip_path=None):
    e=[]
    if not isinstance(inv,dict) or inv.get('schema')!=SCHEMA:return {'status':'RED','errors':['INVENTORY:BAD_SCHEMA']}
    if inv.get('status')!='SOURCE_AUTHENTICATED_IDENTITY_INVENTORY_S1_DOCUMENTARY':e.append('INVENTORY:FALSE_STATUS')
    items=[f"{x.get('id')}\t{x.get('source_semantics','')}\t{x.get('negative_meaning','')}" for x in inv.get('entries',[]) if isinstance(x,dict)]
    if sha('\n'.join(items).encode())!=SEMANTIC_FREEZE:e.append('INVENTORY:AUTHORED_SEMANTIC_SUMMARY_FREEZE_MISMATCH')
    if source_root is None:e.append('INVENTORY:NO_SOURCE_ROOT');return {'status':'RED','errors':e}
    files=inv.get('source_files')
    if not isinstance(files,list) or not files:e.append('INVENTORY:NO_SOURCE_FILES');files=[]
    fmap={};bodies={}
    for i,f in enumerate(files):
        if not isinstance(f,dict):e.append('INVENTORY:BAD_SOURCE_FILE');continue
        rel=f.get('path')
        if rel in fmap:e.append('INVENTORY:DUPLICATE_SOURCE_FILE:'+str(rel))
        fmap[rel]=f
        b=_verify_file(source_root,f,repo,zip_path,e,'INVENTORY:FILE:'+str(rel))
        if b is not None:bodies[rel]=b
    # Exact canonical file set, not caller-supplied additions/removals.
    if set(fmap)!=set(CANON_PINS):e.append('INVENTORY:SOURCE_FILE_SET_NOT_CANONICAL')
    expected_auth='GIT_AND_ZIP_PINS_VERIFIED' if any(v['kind']=='ZIP' for v in CANON_PINS.values()) else 'GIT_OBJECT_BLOB_AND_BYTES_VERIFIED'
    actual_auth=expected_auth if (repo and zip_path and len(bodies)==len(CANON_PINS) and not any(x.startswith('INVENTORY:FILE:') for x in e)) else 'UNVERIFIED'
    if inv.get('source_authentication')!=actual_auth:
        e.append('INVENTORY:GRADE_NOT_EARNED')
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
        if sf not in CANON_PINS:e.append('INVENTORY:ORPHAN_SOURCE_FILE:'+rid);continue
        b=bodies.get(sf)
        if b is None:continue
        text=b.decode('utf-8','replace')
        if x.get('source_excerpt') not in text:e.append('INVENTORY:EXCERPT_NOT_IN_SOURCE:'+rid)
        if x.get('origin_sha256')!=sha(x.get('source_excerpt','').encode()):e.append('INVENTORY:ROW_HASH_MISMATCH:'+rid)
        if g in ('PYAT_PC','P4R') and x.get('adopted') is not False:e.append('INVENTORY:UNAUTHORIZED_ADOPTION:'+rid)
        if g=='P4R' and x.get('closed') is not False:e.append('INVENTORY:FALSE_PROOF_CLOSURE:'+rid)
    for g in GROUPS:
        if counts[g]!=GROUP_COUNTS[g]:e.append('INVENTORY:COUNT_DRIFT:'+g+':'+str(counts[g]))
    if len(entries)!=118:e.append('INVENTORY:TOTAL_NOT_118')
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
            'source_authentication':actual_auth,
            'semantic_authentication':'AUTHORED_SOURCE_BOUNDED_FREEZE__EXTERNAL_C_SOURCE_OWNER_HOLD'}

def main():
    ap=argparse.ArgumentParser(description='Build or verify the source-qualified 118 identity inventory (S1 documentary, no architecture)')
    ap.add_argument('action',choices=['build','verify'])
    ap.add_argument('--source-root',required=True);ap.add_argument('--manifest');ap.add_argument('--zip-root')
    ap.add_argument('--inventory');ap.add_argument('--repo');ap.add_argument('--zip');ap.add_argument('--out')
    a=ap.parse_args()
    if a.action=='build':
        if not (a.manifest and a.zip_root):raise SystemExit('build requires --manifest and --zip-root')
        inv=build_inventory(a.source_root,a.manifest,a.zip_root)
        b=(json.dumps(inv,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
        if a.out:pathlib.Path(a.out).write_bytes(b);print(json.dumps({'status':'BUILT','path':a.out,'sha256':sha(b),'total':inv['total'],'counts':inv['counts']},indent=2))
        else:sys.stdout.write(b.decode())
        return 0
    inv=json.loads(pathlib.Path(a.inventory).read_text())
    out=check_inventory(inv,a.source_root,a.repo,a.zip)
    print(json.dumps(out,indent=2));return 0 if out['status'].startswith('PASS') else 2

if __name__=='__main__':sys.exit(main())
