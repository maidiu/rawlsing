#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, csv, hashlib, io, json, lzma, pathlib, subprocess, sys, zlib
from collections import Counter, defaultdict

THIS = pathlib.Path(__file__).resolve()
RETURN_ROOT = THIS.parent
def _repo_root():
    for p in [THIS.parent, *THIS.parents]:
        if (p/'.git').exists(): return p
    c=pathlib.Path.cwd()
    if (c/'.git').exists(): return c
    raise RuntimeError('repository root not found')
REPO_ROOT = _repo_root()
MANIFEST = json.loads((RETURN_ROOT/'01_AUTHORITY_JURISDICTION_MANIFEST.json').read_text(encoding='utf-8'))
CODEBOOK = json.loads((RETURN_ROOT/'02_DISPOSITION_CODEBOOK.json').read_text(encoding='utf-8'))
N03 = MANIFEST['accepted_inputs']['N03']; N01 = MANIFEST['accepted_inputs']['N01-R2']; N02 = MANIFEST['accepted_inputs']['N02-R2']
csv.field_size_limit(sys.maxsize)

def sha256(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def run(*args: str, check: bool=True) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)
def ensure_commit(sha: str) -> None:
    p=run('git','cat-file','-e',sha+'^{commit}',check=False)
    if p.returncode:
        q=run('git','fetch','--no-tags','--depth=1','origin',sha,check=False)
        if q.returncode: raise AssertionError(f'cannot fetch accepted commit {sha}: {q.stderr.decode(errors="replace")}')
        assert run('git','cat-file','-e',sha+'^{commit}',check=False).returncode==0

def git_bytes(ref: str, path: str) -> bytes:
    ensure_commit(ref)
    p=run('git','show',f'{ref}:{path}',check=False)
    if p.returncode: raise AssertionError(f'missing {ref}:{path}: {p.stderr.decode(errors="replace")}')
    return p.stdout

def git_blob(ref: str, path: str) -> str:
    ensure_commit(ref)
    p=run('git','rev-parse',f'{ref}:{path}')
    return p.stdout.decode().strip()

def jload(b: bytes): return json.loads(b.decode('utf-8'))
def csvload(b: bytes): return list(csv.DictReader(io.StringIO(b.decode('utf-8-sig'), newline='')))

def reconstruct_n01():
    m=jload(git_bytes(N01['commit'],N01['manifest_path'])); root=N01['return_root']; chunks=[]
    for part in m['carrier']['parts']:
        x=git_bytes(N01['commit'],root+'/'+part['path'])
        assert len(x)==part['bytes'] and sha256(x)==part['sha256']
        chunks.append(x)
    b64=b''.join(chunks); c=m['carrier']; assert sha256(b64)==c['base64_text_sha256']
    comp=base64.b64decode(b64); assert sha256(comp)==c['seed_xz_sha256']
    seed=lzma.decompress(comp,format=lzma.FORMAT_XZ); assert sha256(seed)==c['seed_csv_sha256']
    seeds=csvload(seed); metas={x['source_family']:x for x in m['families']}; ords=defaultdict(int); rows=[]
    for s in seeds:
        fam=s['source_family']; ords[fam]+=1; meta=metas[fam]
        hh=hashlib.sha256((fam+'\x1f'+s['wave']+'\x1f'+s['source_variable_code']).encode()).hexdigest()
        rows.append({'question_implementation_id':'question_impl.phase0.'+hh[:20], 'question_concept_id':'question.phase0.'+hh[:20], **s,
                     'exact_identity_sha256':hh,'source_catalog_member':meta['source_catalog_member'],
                     'source_catalog_sha256':meta['source_catalog_sha256'],'source_catalog_row_ordinal':str(ords[fam])})
    assert len(rows)==18276 and len({r['question_implementation_id'] for r in rows})==18276
    scopes={(r['source_family'],r['wave']) for r in rows}; assert len(scopes)==35 and len(set(r['source_family'] for r in rows))==9
    out=io.StringIO(newline=''); w=csv.DictWriter(out,fieldnames=m['enumerated_fields'],lineterminator='\n'); w.writeheader(); w.writerows(rows)
    assert sha256(out.getvalue().encode())==N01['full_csv_sha256']
    return rows, m

def decode_n02(current_rows):
    m=jload(git_bytes(N02['commit'],N02['manifest_path'])); raw=git_bytes(N02['commit'],N02['vector_path']).strip(); vec=zlib.decompress(base64.b64decode(raw))
    assert len(vec)==18276==m['ledger']['rows']; assert sha256(vec)==m['ledger']['raw_vector_sha256']
    order={x['member']:i for i,x in enumerate(m['carrier']['ordinal_member_order'])}
    rr=sorted(current_rows,key=lambda r:(order[r['source_catalog_member']],int(r['source_catalog_row_ordinal'])))
    ids=[r['question_implementation_id'] for r in rr]
    assert sha256(('\n'.join(ids)+'\n').encode())==m['carrier']['ordinal_qid_stream_sha256']
    assert sha256(('\n'.join(sorted(ids))+'\n').encode())==m['carrier']['sorted_id_set_sha256']
    disp={int(k):v for k,v in m['ledger']['codebook']['disposition_codes'].items()}; auth={int(k):v for k,v in m['ledger']['codebook']['authority_codes'].items()}
    scopes=m['ledger']['scoped_nonapplicability_by_qid']; result={}
    for row,b in zip(rr,vec):
        q=row['question_implementation_id']; result[q]={'routing_authority_code':auth[b//8],'routing_disposition':disp[b%8],'routing_scope':scopes.get(q,'')}
    assert Counter(x['routing_disposition'] for x in result.values())==Counter(m['ledger']['disposition_counts'])
    return result,m

def registry_objects():
    assert git_blob(N03['commit'],N03['return_registry_path'])==N03['return_registry_blob']
    reg=jload(git_bytes(N03['commit'],N03['return_registry_path'])); objs={x['object_id']:x for x in reg['objects']}
    missing=set(MANIFEST['required_object_ids'])-set(objs); assert not missing, missing
    for oid in MANIFEST['required_object_ids']:
        o=objs[oid]
        if o.get('path') and o.get('blob_sha'):
            assert git_blob(N03['commit'],o['path'])==o['blob_sha'], (oid,o['path'])
    return reg,objs

def rows_for(objs,oid):
    o=objs[oid]; return csvload(git_bytes(N03['commit'],o['path']))

def typed_index(rows):
    idx=defaultdict(list)
    for n,r in enumerate(rows,1):
        raw=r.get('member_implementation_ids_json','')
        if not raw: continue
        try: ids=json.loads(raw)
        except Exception: raise AssertionError(f'bad member_implementation_ids_json row {n}')
        aid=r.get('authority_id') or r.get('candidate_id') or r.get('relation_id') or f'row:{n}'
        for q in ids:
            if isinstance(q,str) and q.startswith('question_impl.phase0.'): idx[q].append(aid)
    return idx

def build():
    current,n01m=reconstruct_n01(); routing,n02m=decode_n02(current); reg,objs=registry_objects(); current_ids={r['question_implementation_id'] for r in current}
    fqra=rows_for(objs,'FQRA_R1'); fq=defaultdict(list)
    for i,r in enumerate(fqra,1):
        q=(r.get('p2_question_implementation_id') or '').strip()
        if q: fq[q].append((i,r))
    qsm=rows_for(objs,'QSMV2_IMPLEMENTATION_AUTHORITY_4438'); qm=defaultdict(list)
    for i,r in enumerate(qsm,1):
        q=(r.get('question_implementation_id') or '').strip()
        if q: qm[q].append((i,r))
    blocked=rows_for(objs,'QSMV2_BLOCKED_IMPLEMENTATIONS_41'); qb=defaultdict(list)
    for i,r in enumerate(blocked,1):
        q=(r.get('question_implementation_id') or '').strip()
        if q: qb[q].append((i,r))
    response=rows_for(objs,'V550_V551_RESPONSE_SEMANTICS_BINDING'); response_registry=rows_for(objs,'RESPONSE_SCALE_ENCODING_REGISTRY_35WAVE')
    assert len(response_registry)==objs['RESPONSE_SCALE_ENCODING_REGISTRY_35WAVE']['state_counts']['registry_rows']
    vr=defaultdict(list)
    for i,r in enumerate(response,1): vr[(r['source_family'],r['canonical_wave'],r['var_code'])].append((i,r))
    tp=typed_index(rows_for(objs,'JOB3_R3_POSITIVE_1190')); tr=typed_index(rows_for(objs,'JOB3_R3_REJECT_697')); tb=typed_index(rows_for(objs,'JOB3_R3_BLOCKED_15'))
    assert len(fqra)==objs['FQRA_R1']['state_counts']['rows']; assert len(qsm)==objs['QSMV2_IMPLEMENTATION_AUTHORITY_4438']['state_counts']['implementations']; assert len(blocked)==objs['QSMV2_BLOCKED_IMPLEMENTATIONS_41']['state_counts']['blocked_implementations']; assert len(response)==objs['V550_V551_RESPONSE_SEMANTICS_BINDING']['state_counts']['binding_rows']
    code_by_name={v:int(k) for k,v in CODEBOOK['codes'].items()}; ledger=[]; vector=[]
    for c in current:
        q=c['question_implementation_id']; f=fq.get(q,[]); m=qm.get(q,[]); b=qb.get(q,[]); v=vr.get((c['source_family'],c['wave'],c['source_variable_code']),[]); p=tp.get(q,[]); rej=tr.get(q,[]); blk=tb.get(q,[])
        refs=[]; basis=[]
        if b:
            top='CURRENT_GOVERNED_REVIEW_REQUIRED'; basis.append('EXACT_QSMV2_BLOCKED_IMPLEMENTATION')
            refs.append(f"QSMV2_BLOCKED_IMPLEMENTATIONS_41@{objs['QSMV2_BLOCKED_IMPLEMENTATIONS_41']['blob_sha']}:qid={q}:rows={','.join(str(i) for i,_ in b)}")
        else:
            if f:
                basis.append('FQRA_EXACT_IMPLEMENTATION_ID'); refs.append(f"FQRA_R1@{objs['FQRA_R1']['blob_sha']}:qid={q}:rows={','.join(str(i) for i,_ in f)}")
            if m:
                basis.append('QSMV2_EXACT_IMPLEMENTATION_ID'); refs.append(f"QSMV2_IMPLEMENTATION_AUTHORITY_4438@{objs['QSMV2_IMPLEMENTATION_AUTHORITY_4438']['blob_sha']}:qid={q}:rows={','.join(str(i) for i,_ in m)}")
            if v:
                basis.append('V550_V551_EXPLICIT_SOURCE_WAVE_VAR_BINDING'); refs.append(f"V550_V551_RESPONSE_SEMANTICS_BINDING@{objs['V550_V551_RESPONSE_SEMANTICS_BINDING']['blob_sha']}:key={c['source_family']}|{c['wave']}|{c['source_variable_code']}:rows={','.join(str(i) for i,_ in v)}")
            if p:
                basis.append('CURRENT_TYPED_RELATION_EXACT_MEMBER_ID'); refs.append(f"JOB3_R3_POSITIVE_1190@{objs['JOB3_R3_POSITIVE_1190']['blob_sha']}:authority_ids={','.join(sorted(p))}")
            top='CURRENT_GOVERNED_POSITIVE' if basis else 'CURRENT_TYPED_UNRESOLVED__EXACT_BASIS'
        fq_status=sorted({r.get('authority_status_final_or_current','') for _,r in f if r.get('authority_status_final_or_current','')}); fq_rel=sorted({r.get('relation_use_status_final','') for _,r in f if r.get('relation_use_status_final','')})
        routing_row=routing[q]
        rec={
          'question_implementation_id':q,'source_family':c['source_family'],'wave':c['wave'],'source_variable_code':c['source_variable_code'],
          'top_level_disposition':top,'top_level_binding_basis':basis,'top_level_authority_refs':refs,
          'fqra_match_count':len(f),'fqra_row_numbers':[str(i) for i,_ in f],'fqra_authority_statuses':fq_status,'fqra_relation_use_statuses':fq_rel,
          'qsmv2_implementation_match_count':len(m),'qsmv2_blocked':bool(b),'qsmv2_blocked_row_numbers':[str(i) for i,_ in b],
          'response_binding_count':len(v),'response_registry_key_indices':sorted({r['v551_registry_key_index'] for _,r in v}),
          'typed_positive_authority_ids':sorted(p),'typed_reject_authority_ids':sorted(rej),'typed_blocked_authority_ids':sorted(blk),
          'qsr_currentness_binding':'UNRESOLVED_SUCCESSION__PRESERVED_REFERENCE_JURISDICTION__NO_EXACT_CURRENT_IMPLEMENTATION_MAP',
          'qra_current_precedence_binding':'REVIEW_REQUIRED_WHERE_CURRENT_PRECEDENCE_UNPROVED__NO_IMPLEMENTATION_LEVEL_SUCCESSOR_INFERENCE',
          **routing_row,
          'unresolved_basis':'' if top!='CURRENT_TYPED_UNRESOLVED__EXACT_BASIS' else 'NO_EXACT_CURRENT_IMPLEMENTATION_OR_EXPLICIT_SOURCE_WAVE_VARIABLE_SEMANTIC_AUTHORITY_JOIN_IN_ACCEPTED_N03_OBJECTS'
        }
        if top!='CURRENT_TYPED_UNRESOLVED__EXACT_BASIS': assert refs
        else: assert rec['unresolved_basis']
        ledger.append(rec); vector.append(code_by_name[top])
    assert len(ledger)==18276 and {r['question_implementation_id'] for r in ledger}==current_ids
    canon=b''.join((json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode() for r in ledger)
    vec=bytes(vector); vb64=base64.b64encode(zlib.compress(vec,9))
    unresolved=sorted(r['question_implementation_id'] for r in ledger if r['top_level_disposition']=='CURRENT_TYPED_UNRESOLVED__EXACT_BASIS')
    summary={
      'rows':len(ledger),'unique_ids':len(current_ids),'families':len({r['source_family'] for r in ledger}),'active_scopes':len({(r['source_family'],r['wave']) for r in ledger}),
      'disposition_counts':dict(sorted(Counter(r['top_level_disposition'] for r in ledger).items())),
      'ledger_canonical_jsonl_sha256':sha256(canon),'ledger_canonical_jsonl_bytes':len(canon),
      'top_vector_raw_sha256':sha256(vec),'top_vector_raw_bytes':len(vec),'top_vector_zlib_b64_sha256':sha256(vb64),'top_vector_zlib_b64_bytes':len(vb64),
      'fqra_current_id_coverage':sum(bool(fq.get(q)) for q in current_ids),'qsmv2_current_id_coverage':sum(bool(qm.get(q)) for q in current_ids),
      'qsmv2_blocked_current_ids':sum(bool(qb.get(q)) for q in current_ids),'response_binding_current_ids':sum(bool(vr.get((r['source_family'],r['wave'],r['source_variable_code']))) for r in current),
      'typed_positive_current_ids':sum(bool(tp.get(q)) for q in current_ids),'typed_reject_member_current_ids':sum(bool(tr.get(q)) for q in current_ids),'typed_blocked_member_current_ids':sum(bool(tb.get(q)) for q in current_ids),
      'unresolved_count':len(unresolved),'unresolved_sorted_id_stream_sha256':sha256(('\n'.join(unresolved)+('\n' if unresolved else '')).encode()),
      'nonunresolved_with_exact_provenance':sum(bool(r['top_level_authority_refs']) for r in ledger if r['top_level_disposition']!='CURRENT_TYPED_UNRESOLVED__EXACT_BASIS'),
      'unresolved_with_exact_basis':sum(bool(r['unresolved_basis']) for r in ledger if r['top_level_disposition']=='CURRENT_TYPED_UNRESOLVED__EXACT_BASIS'),
      'n02_routing_disposition_counts':dict(sorted(Counter(r['routing_disposition'] for r in ledger).items())),
      'verified_n03_object_ids':sorted(MANIFEST['required_object_ids']),
      'n01_full_csv_sha256':N01['full_csv_sha256'],'n02_canonical_row_jsonl_sha256':N02['canonical_row_jsonl_sha256']
    }
    return ledger,vec,vb64,summary

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--emit-ledger'); ap.add_argument('--emit-vector'); ap.add_argument('--summary-out'); args=ap.parse_args()
    ledger,vec,vb64,summary=build()
    if args.emit_ledger:
        pathlib.Path(args.emit_ledger).write_bytes(b''.join((json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode() for r in ledger))
    if args.emit_vector: pathlib.Path(args.emit_vector).write_bytes(vb64+b'\n')
    if args.summary_out: pathlib.Path(args.summary_out).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,sort_keys=True))
if __name__=='__main__': main()
