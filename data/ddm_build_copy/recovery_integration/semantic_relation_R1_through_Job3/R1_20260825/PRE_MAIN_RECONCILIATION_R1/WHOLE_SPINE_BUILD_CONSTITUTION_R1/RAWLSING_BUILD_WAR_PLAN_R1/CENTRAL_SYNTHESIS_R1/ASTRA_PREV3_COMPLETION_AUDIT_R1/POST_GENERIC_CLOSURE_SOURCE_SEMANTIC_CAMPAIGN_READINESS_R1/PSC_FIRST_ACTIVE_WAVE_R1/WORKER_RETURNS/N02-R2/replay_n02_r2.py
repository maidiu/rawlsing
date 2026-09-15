#!/usr/bin/env python3
import argparse,base64,csv,hashlib,io,json,pathlib,sys,zipfile,zlib
from collections import Counter
R=pathlib.Path(__file__).resolve().parent
M=json.loads((R/'01_AUTHORITY_AND_LEDGER_MANIFEST.json').read_text())
raw=(R/M['ledger']['vector_path']).read_bytes().strip(); vec=zlib.decompress(base64.b64decode(raw))
assert len(vec)==18276==M['ledger']['rows']
assert hashlib.sha256(vec).hexdigest()==M['ledger']['raw_vector_sha256']
disp={int(k):v for k,v in M['ledger']['codebook']['disposition_codes'].items()}; auth={int(k):v for k,v in M['ledger']['codebook']['authority_codes'].items()}
decoded=[(auth[b//8],disp[b%8]) for b in vec]
assert Counter(d for _,d in decoded)==Counter(M['ledger']['disposition_counts'])
ap=argparse.ArgumentParser(); ap.add_argument('--carrier',required=True); ap.add_argument('--emit-csv'); ns=ap.parse_args()
p=pathlib.Path(ns.carrier); assert hashlib.sha256(p.read_bytes()).hexdigest()==M['carrier']['sha256']
rows=[]; order=[]; csv.field_size_limit(sys.maxsize)
with zipfile.ZipFile(p) as z:
 for n in z.namelist():
  if n.lower().endswith('.csv') and 'Active_35_Wave_Scope' not in n:
   rr=list(csv.DictReader(io.StringIO(z.read(n).decode('utf-8-sig')))); order.append({'member':n,'rows':len(rr)}); rows+=rr
assert order==M['carrier']['ordinal_member_order'] and len(rows)==18276
ids=[r['question_implementation_id'] for r in rows]; assert len(set(ids))==18276
assert hashlib.sha256(('\n'.join(ids)+'\n').encode()).hexdigest()==M['carrier']['ordinal_qid_stream_sha256']
assert hashlib.sha256(('\n'.join(sorted(ids))+'\n').encode()).hexdigest()==M['carrier']['sorted_id_set_sha256']
scopes=M['ledger']['scoped_nonapplicability_by_qid']; deriv=set(M['authorities']['B03-W05']['derivative_quarantine_qids'])
def prov(ac,qid):
 a=M['authorities'][ac]
 if ac=='CEN-O06': return f"sha256={a['sha256']};path={a['ledger_path']};qid={qid}"
 if ac.startswith('B03-'):
  if ac=='B03-W05' and qid in deriv: return f"commit={a['authority_commit']};path={a['derivative_quarantine_review_path']};qid={qid}"
  return f"commit={a['authority_commit']};source_return_sha256={a['source_return_sha256']};path={a['source_path']};qid={qid}"
 if ac=='B04-A44': return f"commit={a['authority_commit']};path={a['authority_path']};qid={qid}"
 if ac=='B05-A44': return f"commit={a['authority_commit']};directory={a['authority_directory']};shard_set_sha256={a['shard_set_sha256']};qid={qid}"
 raise AssertionError(ac)
out=[]
for c,(ac,dc) in zip(rows,decoded):
 qid=c['question_implementation_id']; out.append({'question_implementation_id':qid,'source_family':c['source_family'],'wave':c['wave'],'source_variable_code':c['source_variable_code'],'disposition':dc,'authority_code':ac,'provenance_locator':prov(ac,qid),'scope':scopes.get(qid,'')})
canon=''.join(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n' for r in out).encode(); sha=hashlib.sha256(canon).hexdigest(); assert sha==M['ledger']['canonical_row_jsonl_sha256']
assert sum(1 for r in out if r['scope'])==17
assert all(r['provenance_locator'] for r in out if r['disposition']=='UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY')
print('PASS',len(out),sha)
if ns.emit_csv:
 flds=list(out[0]);
 with open(ns.emit_csv,'w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=flds,lineterminator='\n'); w.writeheader(); w.writerows(out)
