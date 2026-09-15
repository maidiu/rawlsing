#!/usr/bin/env python3
from __future__ import annotations
import argparse,base64,csv,hashlib,io,json,lzma,pathlib,sys,zipfile
from collections import Counter,defaultdict
csv.field_size_limit(50_000_000)
EXPECTED_BUNDLE_SHA='b569c3677514e627bccb6f920c7aefd7c1d7bb452eb906ddd8913a69d27dac7d'; EXPECTED_BUNDLE_BYTES=5257954; EXPECTED_TOTAL=18276
def h(b): return hashlib.sha256(b).hexdigest()
def hf(p): return h(p.read_bytes())
def fail(m): print('FAIL:',m,file=sys.stderr); raise SystemExit(1)
def ident(f,w,v): return hashlib.sha256((f+'\x1f'+w+'\x1f'+v).encode()).hexdigest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('return_root',nargs='?',default='.'); ap.add_argument('--source-bundle'); ap.add_argument('--receipt-out'); ap.add_argument('--emit-csv'); a=ap.parse_args(); root=pathlib.Path(a.return_root)
 mp=root/'N01_R2_CURRENT_IMPLEMENTATION_IDENTITY_MANIFEST.json'; m=json.loads(mp.read_text(encoding='utf-8')); c=m['carrier']; chunks=[]
 for part in c['parts']:
  p=root/part['path']; x=p.read_bytes()
  if len(x)!=part['bytes'] or h(x)!=part['sha256']: fail('carrier part identity '+part['path'])
  chunks.append(x)
 b64=b''.join(chunks); bp=None
 if m.get('schema')!='RAWLSING_PREV3_CURRENT_IMPLEMENTATION_IDENTITY_CARRIER_R2@4.0.0': fail('manifest schema')
 if m['accepted_library_bundle']['sha256']!=EXPECTED_BUNDLE_SHA or m['accepted_library_bundle']['bytes']!=EXPECTED_BUNDLE_BYTES: fail('bundle authority')
 if len(b64)!=c['base64_text_bytes'] or h(b64)!=c['base64_text_sha256']: fail('base64 carrier identity')
 try: comp=base64.b64decode(b64,validate=False)
 except Exception as e: fail(f'base64 decode {e}')
 if len(comp)!=c['seed_xz_bytes'] or h(comp)!=c['seed_xz_sha256']: fail('xz identity')
 seed=lzma.decompress(comp,format=lzma.FORMAT_XZ)
 if len(seed)!=c['seed_csv_bytes'] or h(seed)!=c['seed_csv_sha256']: fail('seed csv identity')
 seeds=list(csv.DictReader(io.StringIO(seed.decode('utf-8'),newline=''))); metas={x['source_family']:x for x in m['families']}; famord=m['family_order']
 if len(seeds)!=EXPECTED_TOTAL: fail('seed denominator')
 ords=defaultdict(int); rows=[]
 for s in seeds:
  fam=s['source_family']; ords[fam]+=1; meta=metas[fam]; hh=ident(fam,s['wave'],s['source_variable_code'])
  rows.append({'question_implementation_id':'question_impl.phase0.'+hh[:20],'question_concept_id':'question.phase0.'+hh[:20],**s,'exact_identity_sha256':hh,'source_catalog_member':meta['source_catalog_member'],'source_catalog_sha256':meta['source_catalog_sha256'],'source_catalog_row_ordinal':str(ords[fam])})
 ids=[r['question_implementation_id'] for r in rows]; scopes={(r['source_family'],r['wave']) for r in rows}
 if len(rows)!=EXPECTED_TOTAL or len(set(ids))!=EXPECTED_TOTAL or len(scopes)!=35 or set(ords)!=set(famord): fail('global reconciliation')
 for fam in famord:
  fr=[r for r in rows if r['source_family']==fam]; meta=metas[fam]
  if len(fr)!=meta['rows'] or dict(Counter(r['wave'] for r in fr))!=meta['wave_counts']: fail(f'{fam} counts')
 if a.emit_csv:
  p=pathlib.Path(a.emit_csv); p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('w',encoding='utf-8',newline='') as f: w=csv.DictWriter(f,fieldnames=m['enumerated_fields'],lineterminator='\n'); w.writeheader(); w.writerows(rows)
 srcres=None
 if a.source_bundle:
  zp=pathlib.Path(a.source_bundle); bb=zp.read_bytes()
  if len(bb)!=EXPECTED_BUNDLE_BYTES or h(bb)!=EXPECTED_BUNDLE_SHA: fail('source bundle identity')
  byfam=defaultdict(list)
  for r in rows: byfam[r['source_family']].append(r)
  with zipfile.ZipFile(io.BytesIO(bb)) as z:
   for fam in famord:
    meta=metas[fam]; raw=z.read(meta['source_catalog_member'])
    if h(raw)!=meta['source_catalog_sha256'] or len(raw)!=meta['source_catalog_bytes']: fail(f'{fam} source member identity')
    src=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''))); carr=byfam[fam]
    if len(src)!=len(carr): fail(f'{fam} source rows')
    for i,(s,crow) in enumerate(zip(src,carr),1):
     if s['question_implementation_id']!=crow['question_implementation_id'] or s['question_concept_id']!=crow['question_concept_id'] or s['exact_identity_sha256']!=crow['exact_identity_sha256']: fail(f'{fam} row {i} derived identity')
     for k in m['seed_fields']:
      if k=='source_family': continue
      if crow[k]!=(s.get(k,'') or ''): fail(f'{fam} row {i} seed {k}')
     if crow['source_catalog_row_ordinal']!=str(i): fail(f'{fam} row {i} ordinal')
   act=m['active_scope_carrier']; ar=z.read(act['member'])
   if h(ar)!=act['sha256'] or len(ar)!=act['bytes']: fail('active scope identity')
   arw=list(csv.DictReader(io.StringIO(ar.decode('utf-8-sig'),newline=''))); active={(r['source_family'],r['wave']) for r in arw if r['active_scope_status']=='ACTIVE_35_WAVE_SCOPE'}
   if active!=scopes: fail('active scope set')
  srcres={'sha256':EXPECTED_BUNDLE_SHA,'bytes':EXPECTED_BUNDLE_BYTES,'rows_verified':18276,'derived_identity_hash_and_ids_match_source':True,'seed_fields_match_source':True,'provenance_ordinal_member_hash_match':True,'catalog_members_verified':9,'active_scope_rows_verified':35}
 receipt={'schema':'RAWLSING_N01_R2_VALIDATION_RECEIPT@3.0.0','terminal':'PASS','grain':m['grain'],'manifest_sha256':hf(mp),'carrier_text_sha256':h(b64),'rows':len(rows),'unique_question_implementation_ids':len(set(ids)),'duplicate_question_implementation_ids':0,'families':9,'active_wave_release_scopes':35,'identity_derivation_verified_for_rows':18276,'source_bundle_verification':srcres,'boundary':'CATALOG_MEMBERSHIP_IDENTITY != SEMANTIC_AUTHORITY != ROUTING_AUTHORITY'}
 if a.receipt_out: pathlib.Path(a.receipt_out).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(receipt,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
