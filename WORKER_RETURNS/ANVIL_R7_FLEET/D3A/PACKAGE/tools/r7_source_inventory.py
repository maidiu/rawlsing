#!/usr/bin/env python3
"""Source-qualified 118 identity inventory for ANVIL S1.

Replaces the *circular* S1 dependency on a finished R5/R6 P2 SPINE with a
source-origin inventory whose every row is located inside an **independently
pinned container**:

  * GIT — resolved by `git rev-parse <commit>:<path>` in a real repository, so
    the blob id and bytes come from the object store, never from the caller's
    working copy; or
  * ZIP — read from the exact original archive whose sha256 is checked.

A caller-created file with matching self-hashes is NOT source evidence.  With
no external anchor the gate refuses; it never degrades to a local shape PASS.

It authenticates SOURCE LOCATION AND BYTES.  It does NOT authenticate
semantics, science, owner rights, native execution or protected receiving.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, subprocess, sys, zipfile

SCHEMA='ANVIL_SOURCE_QUALIFIED_INVENTORY'
GRADE='SOURCE_QUALIFIED_DOCUMENTARY_NOT_SCIENCE'
AUTH='BYTE_VERIFIED_IN_ORIGINAL_GIT_OBJECT_STORE_OR_ORIGINAL_ZIP'
HEX40=re.compile(r'^[a-f0-9]{40}$')
HEX64=re.compile(r'^[a-f0-9]{64}$')
INVALID=('todo','tbd','placeholder','to be determined','see above','n/a','not applicable')

GROUPS=('K1_CAP','PYAT_PC','P4R','SEAM_B','SEAM_S','ANVIL_L','BOUNDARY','TERMINAL')
ORIGIN_KINDS=('K3_TSV_ROW','DOC_ROW','JSON_MEMBER','TERMINAL_TABLE')
ZIP_SHA='526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332'

K3ROOT='PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/K3_HQ_POST_AB_OWNER_DECISIONS_20261116_R1/'
# logical source -> authoritative container locator
SOURCE_INDEX={
 'K3_29':{'container':'GIT','commit':'31291d08179890852246c8742700e055168e9933','path':K3ROOT+'K3_CONSERVATION_VS_IMPLEMENTATION_29.tsv','snapshot':'K3_CONSERVATION_VS_IMPLEMENTATION_29.tsv'},
 'K3_26':{'container':'GIT','commit':'31291d08179890852246c8742700e055168e9933','path':K3ROOT+'K3_R15_26_OWNER_DECISIONS.tsv','snapshot':'K3_R15_26_OWNER_DECISIONS.tsv'},
 'K3_14':{'container':'GIT','commit':'31291d08179890852246c8742700e055168e9933','path':K3ROOT+'K3_P4R_14_OBLIGATION_ROUTES.tsv','snapshot':'K3_P4R_14_OBLIGATION_ROUTES.tsv'},
 'SEAM25':{'container':'GIT','commit':'596f1230258ff50f98d8543dec42a80e696720f4','path':'SEAM/25_RETURN_TO_BOUNDARY_TRANSFORMATIONS_AND_OPEN_REGISTER_R1.md','snapshot':'SEAM_25.md'},
 'SEAM26':{'container':'GIT','commit':'796452b8cb788fa5a02f37a7ce86eafce8312dfe','path':'SEAM/26_CONDITIONED_SOCIAL_FIELD_IDENTIFICATION_AND_GENERATIVE_PERSON_REVERSE_CONTRACT_R1.md','snapshot':'SEAM_26.md'},
 'ANVIL15':{'container':'GIT','commit':'3cc09bba3d0e26c226da0ddca4b64c43dd74e493','path':'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/ANVIL/15_SEAM_REVERSE_CONSUMER_SOCIAL_FIELD_AND_C11_DESIGN_IMPLICATIONS_R1.md','snapshot':'ANVIL_15.md'},
 'HIST05':{'container':'GIT','commit':'31291d08179890852246c8742700e055168e9933','path':'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_HISTORICAL_FUNCTION_SUCCESSION_AND_WORK_SELECTION_LAW_R1.md','snapshot':'05_HISTORICAL_SUCCESSION.md'},
 'ZIP02':{'container':'ZIP','member':'ANVIL_R7/02_BOUNDARY_CONTRACTS.json'},
 'ZIP03':{'container':'ZIP','member':'ANVIL_R7/03_FROZEN_SOURCE_CUTS.json'},
 'ZIP12':{'container':'ZIP','member':'ANVIL_R7/12_ORIGINAL_MANDATE_AND_DECISION_LEVERAGE.md'},
 'ZIP29':{'container':'ZIP','member':'ANVIL_R7/29_R7_INTEGRATED_MISSION_AND_GATES.md'},
}


def good(x,n=12):
    return isinstance(x,str) and len(x.strip())>=n and not any(x.strip().lower()==s for s in INVALID)

def sha(b):return hashlib.sha256(b).hexdigest()
def git_blob(b):return hashlib.sha1(b'blob %d\0'%len(b)+b).hexdigest()
def canon(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def line_sha(line):return hashlib.sha256(line.encode() if isinstance(line,str) else line).hexdigest()
def _tokens_local(text):return {t for t in re.findall(r'[a-z0-9_]{4,}',(text or '').lower())}


# ---------------------------------------------------------------- anchors
class Anchors:
    """External, independently pinned containers.  No anchor => refuse."""
    def __init__(self,git_repo=None,zip_path=None,zip_sha256=None,commits=None):
        self.git_repo=pathlib.Path(git_repo).resolve() if git_repo else None
        self.zip_path=pathlib.Path(zip_path).resolve() if zip_path else None
        self.zip_sha256=zip_sha256
        self.commits=set(commits) if commits else None
        self._zip_cache=None;self._zip_sha=None;self._blob={};self._resolve={}
    def git(self,*args):
        return subprocess.run(['git','-C',str(self.git_repo),*args],capture_output=True)
    def zipfile(self):
        if self._zip_cache is None:
            self._zip_cache=zipfile.ZipFile(self.zip_path)
        return self._zip_cache


def container_bytes(origin,anchors,errors,code):
    """Authoritative bytes from the pinned container, or None."""
    if anchors is None:
        errors.append(code+':NO_EXTERNAL_TRUST_ANCHOR');return None
    container=origin.get('container')
    if container=='GIT':
        commit=origin.get('commit');rel=origin.get('path');blob=origin.get('git_blob')
        if not isinstance(commit,str) or not HEX40.fullmatch(commit):errors.append(code+':UNPINNED_ORIGIN_COMMIT');return None
        if not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts:
            errors.append(code+':UNSAFE_ORIGIN_PATH');return None
        if not isinstance(blob,str) or not HEX40.fullmatch(blob):errors.append(code+':UNPINNED_ORIGIN_BLOB');return None
        if anchors.git_repo is None or not (anchors.git_repo/'.git').exists():
            errors.append(code+':NO_GIT_ANCHOR');return None
        if anchors.commits is not None and commit not in anchors.commits:
            errors.append(code+':ORIGIN_COMMIT_OUTSIDE_PINNED_CUTS');return None
        r=anchors.git('rev-parse','--verify','--quiet',commit+'^{commit}')
        if r.returncode!=0 or r.stdout.decode().strip()!=commit:
            errors.append(code+':ORIGIN_COMMIT_NOT_IN_REPOSITORY');return None
        key=(commit,rel)
        if key in anchors._resolve:
            actual=anchors._resolve[key]
            if actual is None:errors.append(code+':ORIGIN_PATH_NOT_IN_COMMIT');return None
        else:
            r=anchors.git('rev-parse','--verify','--quiet',commit+':'+rel)
            actual=r.stdout.decode().strip() if r.returncode==0 else None
            anchors._resolve[key]=actual
            if actual is None:errors.append(code+':ORIGIN_PATH_NOT_IN_COMMIT');return None
        if actual!=blob:errors.append(code+':ORIGIN_PATH_BLOB_MISMATCH');return None
        if blob in anchors._blob:data=anchors._blob[blob]
        else:
            r=anchors.git('cat-file','blob',blob)
            if r.returncode!=0:errors.append(code+':ORIGIN_BLOB_UNREADABLE');return None
            data=r.stdout;anchors._blob[blob]=data
        if sha(data)!=origin.get('file_sha256'):errors.append(code+':ORIGIN_FILE_SHA_MISMATCH');return None
        return data
    if container=='ZIP':
        member=origin.get('member');zsha=origin.get('zip_sha256');msha=origin.get('member_sha256')
        if not isinstance(member,str) or not member or member.startswith('/') or '..' in member.split('/'):
            errors.append(code+':UNSAFE_ZIP_MEMBER');return None
        if not isinstance(zsha,str) or not HEX64.fullmatch(zsha):errors.append(code+':UNPINNED_ORIGIN_ZIP');return None
        if anchors.zip_path is None or not anchors.zip_path.is_file():
            errors.append(code+':NO_ZIP_ANCHOR');return None
        if anchors._zip_sha is None:anchors._zip_sha=sha(anchors.zip_path.read_bytes())
        actual=anchors._zip_sha
        if actual!=zsha:errors.append(code+':ZIP_CONTAINER_SHA_MISMATCH');return None
        if anchors.zip_sha256 and actual!=anchors.zip_sha256:
            errors.append(code+':ZIP_ANCHOR_SHA_MISMATCH');return None
        try:data=anchors.zipfile().read(member)
        except (KeyError,zipfile.BadZipFile):errors.append(code+':ZIP_MEMBER_ABSENT');return None
        if not isinstance(msha,str) or sha(data)!=msha:errors.append(code+':ZIP_MEMBER_SHA_MISMATCH');return None
        return data
    errors.append(code+':BAD_ORIGIN_CONTAINER');return None


def extract_row(kind,origin,data,errors,code):
    text=data.decode('utf-8',errors='replace')
    if kind=='K3_TSV_ROW':
        rid=origin.get('row_selector')
        if not isinstance(rid,str) or not rid:errors.append(code+':NO_ROW_SELECTOR');return None
        for line in text.split('\n'):
            if line.split('\t',1)[0]==rid:return line_sha(line),line
        errors.append(code+':ROW_NOT_IN_SOURCE');return None
    if kind=='DOC_ROW':
        excerpt=origin.get('exact_excerpt')
        if not good(excerpt,20):errors.append(code+':NO_EXACT_EXCERPT');return None
        if excerpt not in text:errors.append(code+':EXCERPT_NOT_IN_SOURCE');return None
        return sha(excerpt.encode()),excerpt
    if kind=='JSON_MEMBER':
        try:doc=json.loads(data)
        except ValueError:errors.append(code+':SOURCE_NOT_JSON');return None
        member=origin.get('json_member')
        if not isinstance(member,str) or member not in doc:errors.append(code+':JSON_MEMBER_ABSENT');return None
        t=json.dumps(doc[member],sort_keys=True,ensure_ascii=False,separators=(',',':'))
        return sha(t.encode()),t
    if kind=='TERMINAL_TABLE':
        rid=origin.get('row_selector');excerpt=origin.get('exact_excerpt')
        if not isinstance(rid,str) or not rid or not good(excerpt,12):errors.append(code+':NO_TERMINAL_ROW');return None
        if excerpt not in text:errors.append(code+':TERMINAL_EXCERPT_NOT_IN_SOURCE');return None
        return sha((rid+'\x00'+excerpt).encode()),excerpt
    errors.append(code+':BAD_ORIGIN_KIND');return None


def verify_origin(origin,anchors,errors,code):
    """Resolve one identity in its pinned container.  Returns (row_sha,row_text)."""
    if not isinstance(origin,dict):
        errors.append(code+':NO_ORIGIN');return None
    kind=origin.get('kind')
    if kind not in ORIGIN_KINDS:errors.append(code+':BAD_ORIGIN_KIND');return None
    if not isinstance(origin.get('row_sha256'),str) or not HEX64.fullmatch(origin['row_sha256']):
        errors.append(code+':UNPINNED_ROW_SHA');return None
    data=container_bytes(origin,anchors,errors,code)
    if data is None:return None
    got=extract_row(kind,origin,data,errors,code)
    if got is None:return None
    computed,rowtext=got
    if computed!=origin['row_sha256']:errors.append(code+':ROW_BYTES_CHANGED');return None
    return computed,rowtext


# ---------------------------------------------------------------- verification
def verify_inventory(obj,source_root,errors,code='HISTORY',anchors=None):
    """Full S1 gate.  `anchors` is the ONLY source of truth; `source_root` is a cache."""
    if not isinstance(obj,dict) or obj.get('schema')!=SCHEMA:
        errors.append(code+':NOT_SOURCE_QUALIFIED_INVENTORY');return False
    if obj.get('inventory_grade')!=GRADE:errors.append(code+':FALSE_INVENTORY_GRADE')
    if obj.get('source_authentication')!=AUTH:errors.append(code+':FALSE_SOURCE_AUTHENTICATION')
    if not isinstance(obj.get('source_cut'),str) or not HEX40.fullmatch(str(obj.get('source_cut'))):
        errors.append(code+':UNPINNED_SOURCE_CUT')
    from anvil import REQUIRED
    rows=obj.get('rows')
    if not isinstance(rows,list):errors.append(code+':ROWS_NOT_LIST');return False
    if anchors is None:
        errors.append(code+':NO_EXTERNAL_TRUST_ANCHOR')
        return False
    seen={};per_group={g:set() for g in GROUPS}
    for row in rows:
        if not isinstance(row,dict):errors.append(code+':BAD_ROW');continue
        g=row.get('group');rid=row.get('id')
        if g not in GROUPS:errors.append(code+':UNRECOGNIZED_GROUP:'+str(g));continue
        if (g,rid) in seen:errors.append(code+':DUPLICATE_IDENTITY:'+str(rid))
        seen[(g,rid)]=row;per_group[g].add(rid)
        ctx=code+':'+str(rid)
        for k in ('source_anchor','source_semantics','consumer_or_hold','negative_meaning','architecture_effect','why'):
            if not good(row.get(k),12):errors.append(ctx+':SEMANTIC_OR_CONSUMER_LOSS:'+k)
        if not isinstance(row.get('evidence_ids'),list) or not row['evidence_ids']:
            errors.append(ctx+':NO_EVIDENCE')
        if g=='PYAT_PC' and row.get('adopted') is not False:errors.append(ctx+':FALSE_PROSPECTIVE_ADOPTION')
        if g=='P4R' and row.get('closed') is not False:errors.append(ctx+':FALSE_PROOF_CLOSURE')
        if g=='PYAT_PC' and row.get('necessity')!='HISTORICAL_NOT_ADOPTED':errors.append(ctx+':WRONG_NOT_ADOPTED_GRADE')
        if g=='P4R' and row.get('necessity')!='HISTORICAL_PROOF_HELD':errors.append(ctx+':WRONG_PROOF_HELD_GRADE')
        got=verify_origin(row.get('origin'),anchors,errors,ctx+':ORIGIN')
        if got and len(_tokens_local(row.get('source_semantics'))&_tokens_local(got[1]))<2:
            errors.append(ctx+':SEMANTICS_NOT_GROUNDED_IN_ORIGIN')
    for g,ids in REQUIRED.items():
        if per_group.get(g,set())!=set(ids):
            missing=sorted(set(ids)-per_group.get(g,set()));extra=sorted(per_group.get(g,set())-set(ids))
            errors.append(code+':ID_SET_DRIFT:'+g+':missing='+','.join(missing[:4])+':extra='+','.join(extra[:4]))
    if len(rows)!=sum(len(v) for v in REQUIRED.values()):errors.append(code+':COUNT_DRIFT')
    return not any(e.startswith(code) for e in errors)


def row_hash_map(obj):
    return {r['id']:r['origin']['row_sha256'] for r in obj.get('rows',[]) if isinstance(r,dict) and isinstance(r.get('origin'),dict)}

def by_group(obj):
    out={}
    for r in obj.get('rows',[]):
        if isinstance(r,dict):out.setdefault(r.get('group'),{})[r.get('id')]=r
    return out


# ---------------------------------------------------------------- extraction
def _cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]

def _md_rows(text):
    out={}
    for line in text.split('\n'):
        if not line.startswith('|'):continue
        c=_cells(re.sub(r'P\(Y\|D\)','P(Y/D)',line))
        if not c:continue
        m=re.search(r'\b([BLS]-\d\d)\b',c[0])
        if not m or not c[0].startswith('**'+m.group(1)):continue
        if m.group(1) in out:continue
        out[m.group(1)]=(c,line)
    return out

def _tsv(text):
    lines=[l for l in text.split('\n') if l.strip()]
    head=lines[0].split('\t')
    return [dict(zip(head,l.split('\t'))) for l in lines[1:]]


def build_from_sources(snapshot_root,terminal_map,source_cut):
    """Deterministic extraction.  Reads the snapshot (a cache) and emits
    locators that point ONLY at the authoritative Git commit / ZIP member."""
    snap=pathlib.Path(snapshot_root)/'D3A_SOURCE_SNAPSHOT'
    rows=[]
    cache={}
    def raw(key):
        if key not in cache:
            if SOURCE_INDEX[key]['container']=='GIT':
                cache[key]=(snap/SOURCE_INDEX[key]['snapshot']).read_text()
            else:
                raise ValueError('build reads GIT sources only')
        return cache[key]
    # ZIP-sourced documents are read from the private package copy (cache);
    # their authority is established later against the real ZIP archive.
    pkg=pathlib.Path(snapshot_root)
    def pkgtext(rel):return (pkg/rel).read_text()

    def origin_for(key,extra=None):
        spec=dict(SOURCE_INDEX[key])
        if spec['container']=='GIT':
            data=raw(key).encode()
            o={'kind':None,'container':'GIT','commit':spec['commit'],'path':spec['path'],
               'git_blob':git_blob(data),'file_sha256':sha(data)}
        else:
            data=pkgtext(spec['member'].split('ANVIL_R7/',1)[1]).encode() if False else None
            o=None
        return o

    def add(group,rid,anchor,semantics,consumer,negative,effect,why,nec,evidence,origin,adopted=None,closed=None):
        rows.append({'group':group,'id':rid,'necessity':nec,'adopted':adopted,'closed':closed,
                     'source_anchor':anchor,'source_semantics':semantics,'consumer_or_hold':consumer,
                     'negative_meaning':negative,'architecture_effect':effect,'why':why,
                     'evidence_ids':evidence,'origin':origin})

    def git_origin(key,kind,selector=None,**extra):
        spec=SOURCE_INDEX[key];data=raw(key).encode()
        o={'kind':kind,'container':'GIT','commit':spec['commit'],'path':spec['path'],
           'git_blob':git_blob(data),'file_sha256':sha(data)}
        if selector is not None:o['row_selector']=selector
        if extra.get('exact_excerpt') is not None:o['exact_excerpt']=extra['exact_excerpt']
        _e=[];got=extract_row(kind,o,data,_e,'BUILD')
        if got is None:raise ValueError('cannot locate row while building: '+repr(_e))
        o['row_sha256']=got[0]
        return o

    def zip_origin(key,kind,data,selector=None,**extra):
        spec=SOURCE_INDEX[key]
        o={'kind':kind,'container':'ZIP','member':spec['member'],'zip_sha256':ZIP_SHA,
           'member_sha256':sha(data)}
        if selector is not None:o['row_selector']=selector
        if extra.get('exact_excerpt') is not None:o['exact_excerpt']=extra['exact_excerpt']
        _e=[];got=extract_row(kind,o,data,_e,'BUILD')
        if got is None:raise ValueError('cannot locate row while building: '+repr(_e))
        o['row_sha256']=got[0]
        return o

    for r in _tsv(raw('K3_29')):
        rid=r['capability_id']
        add('K1_CAP',rid,f'K3 TSV row {rid}',r['five_test_source_science_and_cost'] or r['historical_paths'],
            r['actual_current_first_reader_or_hold'],r['P2_accepted_falsifier_correction'] or r['new_requirement'],
            r['HQ_specification_choice'],r['existing_owner']+' :: '+r['new_requirement'],
            'MUST_PRESERVE_NOW',['K3_K1_CAP'],git_origin('K3_29','K3_TSV_ROW',rid))

    for r in _tsv(raw('K3_26')):
        rid=r['proposal_id']
        add('PYAT_PC',rid,f'K3 R15 row {rid} ({r["original_modality"]})',
            r['original_topic']+' :: '+r['selected_source_requirement'],r['selected_source_requirement'],
            r['negative_or_nonclaim'],r['HQ_five_test_owner_disposition'],
            r['native_science_actor_protection']+' :: '+r['intelligence_kind'],
            'HISTORICAL_NOT_ADOPTED',['K3_R15'],git_origin('K3_26','K3_TSV_ROW',rid),adopted=False)

    for r in _tsv(raw('K3_14')):
        rid=r['P4R_id']
        add('P4R',rid,f'K3 P4R row {rid} ({r["old_terminal"]})',r['original_unproved_edge'],
            r['HQ_route'],r['permission_and_native_ceiling'],r['next_bounded_test'],
            r['original_competent_owner']+' :: r-14-commission',
            'HISTORICAL_PROOF_HELD',['K3_P4R'],git_origin('K3_14','K3_TSV_ROW',rid),closed=False)

    b=_md_rows(raw('SEAM25'))
    for i in range(1,11):
        rid=f'B-{i:02d}';c,excerpt=b[rid]
        add('SEAM_B',rid,f'SEAM/25 {c[0]}',c[1],c[2],c[2],c[2],c[3],
            'MUST_ALLOW_FUTURE',['SEAM_25'],git_origin('SEAM25','DOC_ROW',exact_excerpt=excerpt))

    s=_md_rows(raw('SEAM26'))
    for i in range(1,9):
        rid=f'S-{i:02d}';c,excerpt=s[rid]
        add('SEAM_S',rid,f'SEAM/26 {c[0]}',c[1],c[2],c[4],c[2],c[3],
            'MUST_ALLOW_FUTURE',['SEAM_26'],git_origin('SEAM26','DOC_ROW',exact_excerpt=excerpt))

    l=_md_rows(raw('ANVIL15'))
    for i in range(1,9):
        rid=f'L-{i:02d}';c,excerpt=l[rid]
        add('ANVIL_L',rid,f'ANVIL/15 {c[0]}',c[1],c[4],c[2],c[4],c[2]+' :: '+c[3],
            'MUST_PRESERVE_NOW',['ANVIL_15'],git_origin('ANVIL15','DOC_ROW',exact_excerpt=excerpt))

    bcb=pkgtext('02_BOUNDARY_CONTRACTS.json');bc=json.loads(bcb)
    for t in bc['boundaries']:
        rid=t['id']
        excerpt=next(l.strip().rstrip(',') for l in bcb.split('\n') if '"id":"'+rid+'"' in l)
        add('BOUNDARY',rid,f'ANVIL_R7/02_BOUNDARY_CONTRACTS.json {rid}',t['must_preserve'],t['first_effect'],
            t['veto'],t['time_class'],t['name'],'MUST_ALLOW_FUTURE',['BOUNDARY_CONTRACT'],
            zip_origin('ZIP02','DOC_ROW',bcb.encode(),exact_excerpt=excerpt))

    frozen=json.loads(pkgtext('03_FROZEN_SOURCE_CUTS.json'))
    docmap={'ZIP12':pkgtext('12_ORIGINAL_MANDATE_AND_DECISION_LEVERAGE.md'),
            'ZIP29':pkgtext('29_R7_INTEGRATED_MISSION_AND_GATES.md'),
            'HIST05':raw('HIST05')}
    for tid,spec in terminal_map.items():
        if tid.startswith('_'):continue
        if tid not in frozen['mandatory']['TERMINAL']:raise ValueError('terminal id not in frozen cut: '+tid)
        key=spec['source']
        data=docmap[key].encode()
        origin=(git_origin(key,'DOC_ROW',exact_excerpt=spec['exact_excerpt']) if SOURCE_INDEX[key]['container']=='GIT'
                else zip_origin(key,'DOC_ROW',data,exact_excerpt=spec['exact_excerpt']))
        add('TERMINAL',tid,spec['anchor'],spec['exact_excerpt'],spec['consumer'],spec['negative'],
            spec['effect'],spec['why'],spec['necessity'],['FROZEN_TERMINAL_CUT'],origin)
    return {'schema':SCHEMA,'inventory_grade':GRADE,'source_authentication':AUTH,'source_cut':source_cut,
            'generated_by':'r7_source_inventory.build_from_sources (deterministic cell copy, no reclassification)',
            'rows':rows}


def _anchors_from_args(a,obj=None):
    return Anchors(git_repo=a.git_repo,zip_path=a.zip,zip_sha256=a.zip_sha256,
                   commits=json.loads(a.commits) if a.commits else None)


def main():
    ap=argparse.ArgumentParser(description='Build/verify the ANVIL source-qualified 118 inventory')
    ap.add_argument('action',choices=['build','verify'])
    ap.add_argument('inventory',nargs='?')
    ap.add_argument('--source-root',required=True)
    ap.add_argument('--terminal-map')
    ap.add_argument('--out')
    ap.add_argument('--git-repo')
    ap.add_argument('--zip')
    ap.add_argument('--zip-sha256',default=ZIP_SHA)
    ap.add_argument('--commits',help='JSON array of allowed commit ids')
    a=ap.parse_args()
    if a.action=='build':
        cut=json.loads((pathlib.Path(a.source_root)/'D3A_SOURCE_SNAPSHOT/SOURCE_CUSTODY.json').read_text())['source_cut']
        tmap=json.loads(pathlib.Path(a.terminal_map).read_text()) if a.terminal_map else {}
        obj=build_from_sources(a.source_root,tmap,cut)
        out=pathlib.Path(a.out or 'INVENTORY.json');out.write_text(json.dumps(obj,indent=1,sort_keys=True)+'\n')
        e=[];verify_inventory(obj,a.source_root,e,anchors=_anchors_from_args(a))
        print(json.dumps({'status':'PASS_ORIGINAL_CONTAINER_BYTES' if not e else 'RED','rows':len(obj['rows']),
                          'out':str(out),'errors':e[:12]},indent=2));return 0 if not e else 2
    obj=json.loads(pathlib.Path(a.inventory).read_text());e=[]
    verify_inventory(obj,a.source_root,e,anchors=_anchors_from_args(a))
    print(json.dumps({'status':'PASS_ORIGINAL_CONTAINER_BYTES' if not e else 'RED','errors':e[:40]},indent=2))
    return 0 if not e else 2

if __name__=='__main__':sys.exit(main())
