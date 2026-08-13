#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, pandas as pd, sys
ALLOWED_SURFACES={'branch_relation_co_signature','branch_co_signature','question_response_attitude_cloud','joint_patterns'}
REQ_ARCH={'empirical_survives_semantic_block_or_absence','local_block_preserved'}
EXACT_M6_ERRORS={'missing required archetype: empirical_survives_semantic_block_or_absence','missing required archetype: local_block_preserved'}
EXACT_M6_TERMINAL='M6_BLOCKED_ARCHETYPE_COVERAGE__NO_ANTI_ERASE_EVIDENCE_AND_NO_GENUINE_LOCAL_BLOCK_IN_PINNED_CANARY'
PASS='PHASE_D_GATE_CLOSED'; BLOCK='BLOCKED_SUCCESSOR_ARCHETYPE_CONFORMANCE'

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def validate(root):
 root=Path(root); errs=[]
 fr=root/'freeze'/'FROZEN_CANDIDATE_ORDER_R1.csv'; fsha=root/'freeze'/'FROZEN_CANDIDATE_ORDER_R1.csv.sha256'
 ret=root/'RETURN'/'ARCHETYPE_EXECUTION_RETURN_R1.csv'; att=root/'RETURN'/'NO_OUTCOME_SELECTION_EXECUTION_ATTESTATION_R1.json'; prv=root/'RETURN'/'PRIVACY_SCAN_R1.json'
 anc=root/'ancestry'/'M6_IMMUTABLE_ANCESTRY_R1.json'; old=root/'ancestry'/'M6_UNCHANGED_VALIDATOR_RESULT_R1.json'
 for p in [fr,fsha,ret,att,prv,anc,old]:
  if not p.exists(): errs.append(f'missing required file: {p.relative_to(root)}')
 if errs:return {'status':BLOCK,'errors':errs}
 expected=fsha.read_text().strip().split()[0]; actual=sha(fr)
 if expected!=actual:errs.append('frozen candidate order SHA mismatch')
 F=pd.read_csv(fr,dtype=str).fillna(''); R=pd.read_csv(ret,dtype=str).fillna('')
 try:A=json.loads(att.read_text()); P=json.loads(prv.read_text()); M=json.loads(anc.read_text()); O=json.loads(old.read_text())
 except Exception as e:return {'status':BLOCK,'errors':errs+[f'JSON parse error: {e}']}
 if A.get('frozen_order_sha256')!=expected:errs.append('execution attestation freeze SHA mismatch')
 if A.get('candidate_order_changed_after_outcome_access') is not False:errs.append('candidate order changed or not attested unchanged')
 if A.get('candidate_specific_respondent_outcomes_accessed_before_freeze') is not False:errs.append('outcomes accessed before freeze')
 if A.get('execution_followed_frozen_order') is not True:errs.append('frozen execution order not attested')
 if P.get('status')!='PASS' or P.get('respondent_level_rows_packaged') is not False or P.get('direct_identifiers_packaged') is not False:errs.append('privacy scan not PASS/fail-closed')
 if M.get('m6_terminal')!=EXACT_M6_TERMINAL:errs.append('M6 immutable terminal mismatch')
 if set(M.get('unchanged_validator_errors',[]))!=EXACT_M6_ERRORS:errs.append('M6 ancestry validator issue set mismatch')
 if set(O.get('errors',[]))!=EXACT_M6_ERRORS:errs.append('preserved unchanged M6 validator result mismatch')
 exact_fields=['semantic_posture','semantic_ref_id','source_family','wave']
 for arch in REQ_ARCH:
  ff=F[F.archetype==arch].copy(); rr=R[R.archetype==arch].copy()
  if rr.empty:errs.append(f'missing executed archetype rows: {arch}');continue
  frozen={row.candidate_key:int(row.frozen_rank) for _,row in ff.iterrows()}
  ranks=[]; instantiated=[]
  for _,row in rr.iterrows():
   if row.candidate_key not in frozen:errs.append(f'non-frozen candidate executed: {row.candidate_key}');continue
   frow=ff[ff.candidate_key==row.candidate_key].iloc[0]
   if int(row.frozen_rank)!=frozen[row.candidate_key]:errs.append(f'frozen rank mismatch: {row.candidate_key}')
   if row.frozen_order_sha256!=expected:errs.append(f'return freeze SHA mismatch: {row.candidate_key}')
   for field in exact_fields:
    if str(row[field])!=str(frow[field]):errs.append(f'frozen field mismatch {field}: {row.candidate_key}')
   if row.execution_disposition=='NOT_INSTANTIATED' and (not row.advance_reason.strip() or not row.evidence_detail.strip()):errs.append(f'advance lacks exact reason/evidence: {row.candidate_key}')
   if row.execution_disposition=='ARCHETYPE_INSTANTIATED':instantiated.append(int(row.frozen_rank))
   ranks.append(int(row.frozen_rank))
  if ranks:
   mx=max(ranks); expected_ranks=list(range(1,mx+1))
   if sorted(set(ranks))!=expected_ranks:errs.append(f'frozen order skip for {arch}: executed {sorted(set(ranks))}')
   for n in range(1,mx):
    z=rr[rr.frozen_rank.astype(int)==n]
    if z.empty or not (z.execution_disposition=='NOT_INSTANTIATED').all():errs.append(f'earlier rank {n} for {arch} not lawfully closed before advancement')
   if len(instantiated)>1:errs.append(f'multiple instantiated candidates for {arch}')
   if instantiated and max(instantiated)!=mx:errs.append(f'execution continued after archetype instantiated for {arch}')
 a=R[(R.archetype=='empirical_survives_semantic_block_or_absence')&(R.execution_disposition=='ARCHETYPE_INSTANTIATED')]
 anti_ok=False
 for _,x in a.iterrows():
  f=F[(F.archetype==x.archetype)&(F.candidate_key==x.candidate_key)]
  if f.empty:continue
  if x.semantic_posture not in {'BLOCKED_TYPED_RELATION','NO_GOVERNED_TYPED_RELATION'}:continue
  if x.empirical_cotravel_posture!='OBSERVED':continue
  if x.empirical_source_kind not in ALLOWED_SURFACES:continue
  if x.routing_composability_status not in {'STRUCTURALLY_ALLOWED','COMPOSABLE_OBSERVED'}:continue
  if str(x.semantic_authority_preserved).lower()!='true':continue
  ref=Path(str(x.empirical_source_ref))
  if ref.is_absolute() or '..' in ref.parts or not (root/ref).exists():continue
  anti_ok=True
 if not anti_ok:errs.append('missing successor conformance: empirical_survives_semantic_block_or_absence')
 l=R[(R.archetype=='local_block_preserved')&(R.execution_disposition=='ARCHETYPE_INSTANTIATED')]
 local_ok=False
 for _,x in l.iterrows():
  f=F[(F.archetype==x.archetype)&(F.candidate_key==x.candidate_key)]
  if f.empty:continue
  proof=f.iloc[0].routing_proof_type
  if x.semantic_posture!='GOVERNED_POSITIVE' or x.empirical_cotravel_posture!='BLOCKED_LOCAL':continue
  if proof not in {'EXACT_SPLIT_SAMPLE_EMPTY_INTERSECTION','EXPLICIT_COMMON_COUNTRY_EXCLUSION'}:continue
  if x.routing_proof_type!=proof:continue
  if x.routing_composability_status!='STRUCTURALLY_IMPOSSIBLE_LOCAL':continue
  if str(x.semantic_authority_preserved).lower()!='true':continue
  exact_ref='freeze/FROZEN_CANDIDATE_ORDER_R1.csv#candidate_key='+x.candidate_key
  if x.routing_proof_ref!=exact_ref or not x.evidence_detail.strip():continue
  low=x.evidence_detail.lower()
  if any(q in low for q in ['zero rows therefore','0 rows therefore','not observed therefore','no observations therefore']):continue
  local_ok=True
 if not local_ok:errs.append('missing successor conformance: local_block_preserved')
 return {'status':PASS if not errs else BLOCK,'errors':errs,'frozen_order_sha256':expected,'executed_rows':int(len(R))}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('return_root');ap.add_argument('--write');a=ap.parse_args();r=validate(a.return_root)
 txt=json.dumps(r,indent=2);print(txt)
 if a.write:Path(a.write).write_text(txt+'\n')
 sys.exit(0 if r['status']==PASS else 2)
if __name__=='__main__':main()
