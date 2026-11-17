#!/usr/bin/env python3
"""Source-qualified 118 identity inventory for ANVIL S1.

This module replaces the *circular* S1 dependency on a finished R5/R6 P2
SPINE with a source-origin inventory whose every row is byte-located in an
immutable source object (Git commit + blob + exact row bytes).

It authenticates BYTES and LOCATION.  It does NOT authenticate semantics,
science, owner rights, native execution or protected receiving.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, sys

SCHEMA='ANVIL_SOURCE_QUALIFIED_INVENTORY'
CUSTODY_SCHEMA='ANVIL_D3A_SOURCE_CUSTODY'
GRADE='SOURCE_QUALIFIED_DOCUMENTARY_NOT_SCIENCE'
AUTH='BYTE_VERIFIED_AGAINST_SUPPLIED_SOURCE_ROOT_BY_LOCAL_CHECK'
HEX40=re.compile(r'^[a-f0-9]{40}$')
HEX64=re.compile(r'^[a-f0-9]{64}$')
INVALID=('todo','tbd','placeholder','to be determined','see above','n/a','not applicable')

GROUPS=('K1_CAP','PYAT_PC','P4R','SEAM_B','SEAM_S','ANVIL_L','BOUNDARY','TERMINAL')
ORIGIN_KINDS=('K3_TSV_ROW','DOC_ROW','JSON_MEMBER','TERMINAL_TABLE')
ZIP_SHA='526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332'


def good(x,n=12):
    return isinstance(x,str) and len(x.strip())>=n and not any(x.strip().lower()==s for s in INVALID)

def sha(b):return hashlib.sha256(b).hexdigest()

def git_blob(b):return hashlib.sha1(b'blob %d\0'%len(b)+b).hexdigest()

def canon(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def line_sha(line):return hashlib.sha256(line.encode() if isinstance(line,str) else line).hexdigest()


# ---------------------------------------------------------------- source access
class SourceRoot:
    """Read-only view of a materialized exact-byte source snapshot."""
    def __init__(self,root):
        self.root=pathlib.Path(root).resolve()
        self._cache={}
    def bytes(self,rel):
        if rel not in self._cache:
            p=(self.root/rel).resolve()
            if not p.is_relative_to(self.root) or not p.is_file() or p.is_symlink():
                raise FileNotFoundError(rel)
            self._cache[rel]=p.read_bytes()
        return self._cache[rel]
    def text(self,rel):
        return self.bytes(rel).decode('utf-8')


def verify_origin(origin,src,errors,code):
    """Byte-locate one identity's declared origin.  Returns the recomputed row hash."""
    if not isinstance(origin,dict):
        errors.append(code+':NO_ORIGIN');return None
    kind=origin.get('kind');rel=origin.get('path');commit=origin.get('commit');zsha=origin.get('zip_sha256')
    blob=origin.get('git_blob');fsha=origin.get('file_sha256');rsha=origin.get('row_sha256')
    if kind not in ORIGIN_KINDS:errors.append(code+':BAD_ORIGIN_KIND');return None
    if not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts:
        errors.append(code+':UNSAFE_ORIGIN_PATH');return None
    if commit is not None:
        if not isinstance(commit,str) or not HEX40.fullmatch(commit):errors.append(code+':UNPINNED_ORIGIN_COMMIT');return None
    elif zsha is not None:
        if not isinstance(zsha,str) or not HEX64.fullmatch(zsha):errors.append(code+':UNPINNED_ORIGIN_ZIP');return None
    else:
        errors.append(code+':UNPINNED_ORIGIN_CONTAINER');return None
    if not isinstance(blob,str) or not HEX40.fullmatch(blob):errors.append(code+':UNPINNED_ORIGIN_BLOB');return None
    if not isinstance(fsha,str) or not HEX64.fullmatch(fsha):errors.append(code+':UNPINNED_FILE_SHA');return None
    if not isinstance(rsha,str) or not HEX64.fullmatch(rsha):errors.append(code+':UNPINNED_ROW_SHA');return None
    try:data=src.bytes(rel)
    except (FileNotFoundError,OSError):errors.append(code+':SOURCE_FILE_ABSENT');return None
    if sha(data)!=fsha:errors.append(code+':SOURCE_FILE_BYTES_CHANGED');return None
    if git_blob(data)!=blob:errors.append(code+':GIT_BLOB_ID_DISAGREES');return None
    text=data.decode('utf-8',errors='replace')
    computed=None;rowtext=''
    if kind=='K3_TSV_ROW':
        rid=origin.get('row_selector')
        if not isinstance(rid,str) or not rid:errors.append(code+':NO_ROW_SELECTOR');return None
        for line in text.split('\n'):
            if line.split('\t',1)[0]==rid:
                computed=line_sha(line);rowtext=line;break
        if computed is None:errors.append(code+':ROW_NOT_IN_SOURCE');return None
    elif kind=='DOC_ROW':
        excerpt=origin.get('exact_excerpt')
        if not good(excerpt,20):errors.append(code+':NO_EXACT_EXCERPT');return None
        if excerpt not in text:errors.append(code+':EXCERPT_NOT_IN_SOURCE');return None
        computed=sha(excerpt.encode());rowtext=excerpt
    elif kind=='JSON_MEMBER':
        member=origin.get('json_member')
        try:doc=json.loads(data)
        except ValueError:errors.append(code+':SOURCE_NOT_JSON');return None
        if not isinstance(member,str) or member not in doc:errors.append(code+':JSON_MEMBER_ABSENT');return None
        computed=sha(json.dumps(doc[member],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
        rowtext=json.dumps(doc[member],sort_keys=True,ensure_ascii=False,separators=(',',':'))
    elif kind=='TERMINAL_TABLE':
        rid=origin.get('row_selector');excerpt=origin.get('exact_excerpt')
        if not isinstance(rid,str) or not rid or not good(excerpt,12):errors.append(code+':NO_TERMINAL_ROW');return None
        if excerpt not in text:errors.append(code+':TERMINAL_EXCERPT_NOT_IN_SOURCE');return None
        computed=sha((rid+'\x00'+excerpt).encode());rowtext=excerpt
    if computed!=rsha:errors.append(code+':ROW_BYTES_CHANGED');return None
    return computed,rowtext


# ---------------------------------------------------------------- verification
def verify_inventory(obj,source_root,errors,code='HISTORY'):
    """Full S1 gate for a source-qualified inventory.  Returns True when clean."""
    if not isinstance(obj,dict) or obj.get('schema')!=SCHEMA:
        errors.append(code+':NOT_SOURCE_QUALIFIED_INVENTORY');return False
    if obj.get('inventory_grade')!=GRADE:errors.append(code+':FALSE_INVENTORY_GRADE')
    if obj.get('source_authentication')!=AUTH:errors.append(code+':FALSE_SOURCE_AUTHENTICATION')
    if not isinstance(obj.get('source_cut'),str) or not HEX40.fullmatch(str(obj.get('source_cut'))):
        errors.append(code+':UNPINNED_SOURCE_CUT')
    from anvil import REQUIRED
    rows=obj.get('rows')
    if not isinstance(rows,list):errors.append(code+':ROWS_NOT_LIST');return False
    src=SourceRoot(source_root)
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
        got=verify_origin(row.get('origin'),src,errors,ctx+':ORIGIN')
        if got and len(_tokens_local(row.get('source_semantics'))&_tokens_local(got[1]))<2:
            errors.append(ctx+':SEMANTICS_NOT_GROUNDED_IN_ORIGIN')
    for g,ids in REQUIRED.items():
        if per_group.get(g,set())!=set(ids):
            missing=sorted(set(ids)-per_group.get(g,set()));extra=sorted(per_group.get(g,set())-set(ids))
            errors.append(code+':ID_SET_DRIFT:'+g+':missing='+','.join(missing[:4])+':extra='+','.join(extra[:4]))
    if len(rows)!=sum(len(v) for v in REQUIRED.values()):errors.append(code+':COUNT_DRIFT')
    return not any(e.startswith(code) for e in errors)


def _tokens_local(text):
    return {t for t in re.findall(r'[a-z0-9_]{4,}',(text or '').lower())}


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

def _joincells(c,n_tail,n_head=1):
    """Rejoin cells when a source table cell itself contains a literal pipe."""
    if len(c)<=n_head+n_tail:return c
    head=c[:n_head];tail=c[-n_tail:] if n_tail else []
    mid=c[n_head:len(c)-n_tail] if n_tail else c[n_head:]
    return head+['|'.join(mid)]+tail


def _md_rows(text,prefixes):
    """Markdown table rows whose first cell starts with one of prefixes."""
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
    rows=[]
    for l in lines[1:]:
        cells=l.split('\t')
        rows.append((l,dict(zip(head,cells))))
    return head,rows

def build_from_sources(source_root,terminal_map,source_cut):
    """Deterministically extract the 118-row inventory from exact source bytes.

    Extraction is mechanical: it copies verbatim cells.  It does not judge,
    merge, reclassify or add semantic claims.
    """
    src=SourceRoot(source_root);rows=[]

    def file_meta(rel,commit=None,zip_sha256=None):
        b=src.bytes(rel)
        m={'path':rel,'git_blob':git_blob(b),'file_sha256':sha(b)}
        if commit:m['commit']=commit
        else:m['commit']=None
        if zip_sha256:m['zip_sha256']=zip_sha256
        else:m['zip_sha256']=None
        return m

    K3='D3A_SOURCE_SNAPSHOT/'
    K3_COMMIT=source_cut
    seam25=file_meta(K3+'SEAM_25.md','596f1230258ff50f98d8543dec42a80e696720f4')
    seam26=file_meta(K3+'SEAM_26.md','796452b8cb788fa5a02f37a7ce86eafce8312dfe')
    anvil15=file_meta(K3+'ANVIL_15.md','3cc09bba3d0e26c226da0ddca4b64c43dd74e493')
    k1=file_meta(K3+'K3_CONSERVATION_VS_IMPLEMENTATION_29.tsv',K3_COMMIT)
    r15=file_meta(K3+'K3_R15_26_OWNER_DECISIONS.tsv',K3_COMMIT)
    p4r=file_meta(K3+'K3_P4R_14_OBLIGATION_ROUTES.tsv',K3_COMMIT)

    def add(group,rid,anchor,semantics,consumer,negative,effect,why,nec,evidence,origin,adopted=None,closed=None):
        rows.append({'group':group,'id':rid,'necessity':nec,'adopted':adopted,'closed':closed,
                     'source_anchor':anchor,'source_semantics':semantics,'consumer_or_hold':consumer,
                     'negative_meaning':negative,'architecture_effect':effect,'why':why,
                     'evidence_ids':evidence,'origin':origin})

    def tsv_origin(meta,rid):
        return {'kind':'K3_TSV_ROW','path':meta['path'],'commit':meta['commit'],'git_blob':meta['git_blob'],
                'file_sha256':meta['file_sha256'],'row_selector':rid,
                'row_sha256':line_sha(next(l for l in src.text(meta['path']).split('\n') if l.split('\t',1)[0]==rid))}

    _,k1rows=_tsv(src.text(k1['path']))
    for raw,r in k1rows:
        rid=r['capability_id']
        add('K1_CAP',rid,f'K3 TSV row {rid}',r['five_test_source_science_and_cost'] or r['historical_paths'],
            r['actual_current_first_reader_or_hold'],r['P2_accepted_falsifier_correction'] or r['new_requirement'],
            r['HQ_specification_choice'],r['existing_owner']+' :: '+r['new_requirement'],
            'MUST_PRESERVE_NOW',['K3_K1_CAP'],tsv_origin(k1,rid))

    _,r15rows=_tsv(src.text(r15['path']))
    for raw,r in r15rows:
        rid=r['proposal_id']
        add('PYAT_PC',rid,f'K3 R15 row {rid} ({r["original_modality"]})',
            r['original_topic']+' :: '+r['selected_source_requirement'],r['selected_source_requirement'],
            r['negative_or_nonclaim'],r['HQ_five_test_owner_disposition'],
            r['native_science_actor_protection']+' :: '+r['intelligence_kind'],
            'HISTORICAL_NOT_ADOPTED',['K3_R15'],tsv_origin(r15,rid),adopted=False)

    _,p4rrows=_tsv(src.text(p4r['path']))
    for raw,r in p4rrows:
        rid=r['P4R_id']
        add('P4R',rid,f'K3 P4R row {rid} ({r["old_terminal"]})',r['original_unproved_edge'],
            r['HQ_route'],r['permission_and_native_ceiling'],r['next_bounded_test'],
            r['original_competent_owner']+' :: '+r['extra_14_commission'],
            'HISTORICAL_PROOF_HELD',['K3_P4R'],tsv_origin(p4r,rid),closed=False)

    def doc_origin(meta,excerpt):
        return {'kind':'DOC_ROW','path':meta['path'],'commit':meta['commit'],'git_blob':meta['git_blob'],
                'file_sha256':meta['file_sha256'],'exact_excerpt':excerpt,'row_sha256':sha(excerpt.encode())}

    b=_md_rows(src.text(seam25['path']),None)
    for i in range(1,11):
        rid=f'B-{i:02d}';c,excerpt=b[rid]
        add('SEAM_B',rid,f'SEAM/25 {c[0]}',c[1],c[2],c[2],c[2],c[3],
            'MUST_ALLOW_FUTURE',['SEAM_25'],doc_origin(seam25,excerpt))

    s=_md_rows(src.text(seam26['path']),None)
    for i in range(1,9):
        rid=f'S-{i:02d}';c,excerpt=s[rid]
        add('SEAM_S',rid,f'SEAM/26 {c[0]}',c[1],c[2],c[4],c[2],c[3],
            'MUST_ALLOW_FUTURE',['SEAM_26'],doc_origin(seam26,excerpt))

    l=_md_rows(src.text(anvil15['path']),None)
    for i in range(1,9):
        rid=f'L-{i:02d}';c,excerpt=l[rid]
        add('ANVIL_L',rid,f'ANVIL/15 {c[0]}',c[1],c[4],c[2],c[4],c[2]+' :: '+c[3],
            'MUST_PRESERVE_NOW',['ANVIL_15'],doc_origin(anvil15,excerpt))

    bc=json.loads((pathlib.Path(source_root)/'02_BOUNDARY_CONTRACTS.json').read_bytes())
    bcmeta=file_meta('02_BOUNDARY_CONTRACTS.json',zip_sha256=ZIP_SHA)
    bcraw=src.text('02_BOUNDARY_CONTRACTS.json')
    for t in bc['boundaries']:
        rid=t['id']
        excerpt=next(l.strip().rstrip(',') for l in bcraw.split('\n') if '"id":"'+rid+'"' in l)
        add('BOUNDARY',rid,f'ANVIL_R7/02_BOUNDARY_CONTRACTS.json {rid}',t['must_preserve'],t['first_effect'],
            t['veto'],t['time_class'],t['name'],'MUST_ALLOW_FUTURE',['BOUNDARY_CONTRACT'],
            {'kind':'DOC_ROW','path':bcmeta['path'],'commit':bcmeta.get('commit'),'zip_sha256':bcmeta.get('zip_sha256'),
             'git_blob':bcmeta['git_blob'],'file_sha256':bcmeta['file_sha256'],
             'exact_excerpt':excerpt,'row_sha256':sha(excerpt.encode())})

    frozen=json.loads((pathlib.Path(source_root)/'03_FROZEN_SOURCE_CUTS.json').read_bytes())
    cust=json.loads((pathlib.Path(source_root)/'D3A_SOURCE_SNAPSHOT/SOURCE_CUSTODY.json').read_bytes())
    custmap={f['path']:f for f in cust['files']}
    for tid,spec in terminal_map.items():
        if tid.startswith('_'):continue
        if tid not in frozen['mandatory']['TERMINAL']:
            raise ValueError('terminal id not in frozen cut: '+tid)
        if spec['path'] in custmap and custmap[spec['path']].get('commit'):
            meta=file_meta(spec['path'],commit=custmap[spec['path']]['commit'])
        else:
            meta=file_meta(spec['path'],zip_sha256=ZIP_SHA)
        excerpt=spec['exact_excerpt']
        add('TERMINAL',tid,spec['anchor'],excerpt,spec['consumer'],spec['negative'],spec['effect'],
            spec['why'],spec['necessity'],['FROZEN_TERMINAL_CUT'],
            {k:v for k,v in {'kind':'DOC_ROW','path':meta['path'],'commit':meta.get('commit'),
             'zip_sha256':meta.get('zip_sha256'),'git_blob':meta['git_blob'],
             'file_sha256':meta['file_sha256'],'exact_excerpt':excerpt,
             'row_sha256':sha(excerpt.encode())}.items() if v is not None})
    return {'schema':SCHEMA,'inventory_grade':GRADE,'source_authentication':AUTH,'source_cut':source_cut,
            'generated_by':'r7_source_inventory.build_from_sources (deterministic cell copy, no reclassification)',
            'rows':rows}


def main():
    ap=argparse.ArgumentParser(description='Build/verify the ANVIL source-qualified 118 inventory')
    ap.add_argument('action',choices=['build','verify'])
    ap.add_argument('inventory',nargs='?')
    ap.add_argument('--source-root',required=True)
    ap.add_argument('--terminal-map')
    ap.add_argument('--out')
    a=ap.parse_args()
    if a.action=='build':
        cut=json.loads((pathlib.Path(a.source_root)/'D3A_SOURCE_SNAPSHOT/SOURCE_CUSTODY.json').read_text())['source_cut']
        tmap=json.loads(pathlib.Path(a.terminal_map).read_text()) if a.terminal_map else {}
        obj=build_from_sources(a.source_root,tmap,cut)
        out=pathlib.Path(a.out or 'INVENTORY.json');out.write_text(json.dumps(obj,indent=1,sort_keys=True)+'\n')
        e=[];verify_inventory(obj,a.source_root,e)
        print(json.dumps({'status':'PASS_LOCAL_SOURCE_BYTES_ONLY' if not e else 'RED','rows':len(obj['rows']),
                          'out':str(out),'errors':e[:12]},indent=2));return 0 if not e else 2
    obj=json.loads(pathlib.Path(a.inventory).read_text());e=[];verify_inventory(obj,a.source_root,e)
    print(json.dumps({'status':'PASS_LOCAL_SOURCE_BYTES_ONLY' if not e else 'RED','errors':e[:40]},indent=2))
    return 0 if not e else 2

if __name__=='__main__':sys.exit(main())
