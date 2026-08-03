from pathlib import Path
import csv,json,hashlib,subprocess,sys,shutil
ROOT=Path(sys.argv[1]).resolve(); SEC=ROOT/'57_P3A_V7_IDENTITY_MIGRATION_COMPLETE_EVIDENCE_AND_GOVERNED_PILOT'
fail=[]
def need(rel):
 p=SEC/rel
 if not p.exists(): fail.append(f'missing {rel}')
 return p
def j(rel): return json.loads(need(rel).read_text())
def rows(rel):
 p=need(rel)
 return list(csv.DictReader(p.open())) if p.exists() else []
required=['P3A_V35_CANDIDATE_IDENTITY_MIGRATION.csv','P3A_V35_PACKET_IDENTITY_RECONCILIATION.csv','P3A_V35_COMPONENT_IDENTITY_RECONCILIATION.csv','P3A_V35_ALL_CANDIDATE_HASH_RECONCILIATION.csv','P3A_V35_DIRECT_PAIR_CLOSURE_RECONCILIATION.csv','P3A_V35_TYPED_CONSTRAINT_CONVERGENCE.csv','P3A_V35_RANKING_DERIVATION.csv','P3A_V35_PILOT_STRATA_ELIGIBILITY.csv','P3A_V35_PILOT_CANDIDATE_INDEX.csv','P3A_V35_PILOT_SUBSTITUTION_LEDGER.csv','P3A_V35_QUERY_MATRIX.csv','P3A_V35_OBJECT_COUNTS.json','P3A_V35_FIXTURE_RETURN.json','P3A_V35_EXECUTION_FINDINGS.csv','P3A_V35_DOCTRINE_DELTAS.csv']
for r in required: need(r)
for p in ROOT.rglob('*'):
 if p.name=='__pycache__' or p.suffix=='.pyc': fail.append(f'python cache present {p.relative_to(ROOT)}')
# identity append-only
mig=rows('P3A_V35_CANDIDATE_IDENTITY_MIGRATION.csv')
if len(mig)!=141: fail.append('migration ledger not 141 rows')
for r in mig:
 if r.get('same_numeric_id_reused')!='NO' or r.get('status')!='PASS': fail.append('bad identity migration row')
 if r['v35_candidate_family_id'] <= 'P3CAND-000141': fail.append('v35 candidate id did not append')
# packets
pkt_rows=rows('P3A_V35_PACKET_IDENTITY_RECONCILIATION.csv')
if len(pkt_rows)!=40: fail.append('packet reconciliation not 40 rows')
for r in pkt_rows:
 recomputed='P3PKT-'+hashlib.sha256('|'.join([r['candidate_revision_id'],r['evidence_bundle_hash'],r['schema_version']]).encode()).hexdigest()[:16]
 if r['packet_id']!=recomputed or r['status']!='PASS': fail.append(f'packet id mismatch {r.get("candidate_revision_id")}')
# all hashes
h=rows('P3A_V35_ALL_CANDIDATE_HASH_RECONCILIATION.csv')
if len(h)!=141: fail.append('hash reconciliation not 141 rows')
for r in h:
 if r['status']!='PASS' or r['placeholder_hash']!='NO' or len(r['evidence_bundle_hash'])!=64: fail.append('bad candidate hash row')
# direct closure and typed
for rel in ['P3A_V35_DIRECT_PAIR_CLOSURE_RECONCILIATION.csv','P3A_V35_TYPED_CONSTRAINT_CONVERGENCE.csv','P3A_V35_RANKING_DERIVATION.csv']:
 rs=rows(rel)
 if not rs: fail.append(f'{rel} empty')
 for r in rs:
  if r.get('status')!='PASS': fail.append(f'{rel} status not PASS')
counts=j('P3A_V35_OBJECT_COUNTS.json')
if counts.get('status')!='PASS': fail.append('object counts not PASS')
if counts.get('unruled_pairs')!=335 or counts.get('pair_level_obligations')!=345: fail.append('direct-pair count repair not present')
if counts.get('typed_constraints',{}).get('hard_collisions')!=1: fail.append('redirect still counted as hard collision')
# pilot
strata=rows('P3A_V35_PILOT_STRATA_ELIGIBILITY.csv')
if len(strata)!=11: fail.append('pilot strata count not 11')
for r in strata:
 if int(r['selected_count'])>int(r['target']): fail.append('stratum selected over target')
 if r['status'] not in {'PASS','SHORTFALL_RECORDED'}: fail.append('bad stratum status')
idx=rows('P3A_V35_PILOT_CANDIDATE_INDEX.csv')
if len(idx)!=40: fail.append('pilot index not 40 rows')
if len({r['candidate_revision_id'] for r in idx})!=40: fail.append('pilot index duplicates candidates')
# packet validation from artifacts
packets=list((SEC/'candidate_packets').glob('*.json'))
drafts=list((SEC/'draft_decisions').glob('*.json'))
if len(packets)!=40 or len(drafts)!=40: fail.append('packet/draft count not 40')
draft_by_cand={p.name.split('_')[1]:p for p in drafts}
for pp in packets:
 cand=pp.stem.split('_')[-1]
 dp=draft_by_cand.get(cand)
 if not dp: fail.append(f'missing draft for {pp.name}'); continue
 proc=subprocess.run([sys.executable,str(SEC/'validation/validate_p3_candidate_packet_v32.py'),str(pp),str(dp)],text=True,capture_output=True)
 if proc.returncode!=0: fail.append(f'packet validator failed {pp.name}: {proc.stdout[:200]}')
# q matrix only allowed future failures
q=rows('P3A_V35_QUERY_MATRIX.csv')
fails=[r['query_or_gate'] for r in q if r['status']=='FAIL']
if sorted(fails)!=['q01b_postpromotion_pointer','q15b_no_unadjudicated_at_p3_close']: fail.append(f'unexpected q failures {fails}')
fix=j('P3A_V35_FIXTURE_RETURN.json')
if fix.get('status')!='PASS' or len(fix.get('negative_cases',[]))<15: fail.append('fixture return incomplete')
if fix.get('main_p3a_adjudications')!=0 or fix.get('main_p3a_canonical_families')!=0: fail.append('fixture polluted main release')
print(json.dumps({'status':'FAIL' if fail else 'PASS','failures':fail},indent=2))
sys.exit(1 if fail else 0)
