#!/usr/bin/env python3
import pandas as pd,json,hashlib,sys,zipfile,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'RETURN'
errs=[]; checks=[]
def ck(name,cond,detail=''):
 checks.append({'check':name,'pass':bool(cond),'detail':detail})
 if not cond: errs.append(name+(':'+detail if detail else ''))
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
# immutable ancestry
parent=ROOT/'PARENT_T06_RETURN/Rawlsing_S14_T06W05_SourceFirst_Authority_Reconstruction_Return_20260812.zip'
ck('parent_t06_sha_immutable',sha(parent)=='91b2a8a340005be08f5f06d9a61f96ef015b645c8699c2d2a3e7c32b45a912ea',sha(parent))
# tables
acc=pd.read_csv(R/'T15_PRACTICAL_SHORE_ACCOUNTING.csv',dtype=str).fillna(''); pos=pd.read_csv(R/'T15_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',dtype=str).fillna(''); xw=pd.read_csv(R/'T15_CROSSWALK_REVIEW.csv',dtype=str).fillna(''); ov=pd.read_csv(R/'T15_T06_OVERLAP_AND_BOUNDARY.csv',dtype=str).fillna(''); bl=pd.read_csv(R/'T15_BLOCKERS.csv',dtype=str).fillna(''); att=pd.read_csv(R/'T15_WAVE_COMPLETENESS_ATTESTATION.csv',dtype=str).fillna(''); rep=pd.read_csv(R/'T15_UPSTREAM_REPAIRS.csv',dtype=str).fillna('')
ck('accounting_exact_denominator',len(acc)==2986,str(len(acc)))
ck('accounting_unique_ids',acc.question_implementation_id.nunique()==2986,str(acc.question_implementation_id.nunique()))
ck('positive_count',len(pos)==12,str(len(pos)))
ck('strict_overlap_count',len(ov)==18,str(len(ov)))
ck('all_overlap_excluded',set(ov.t15_overlap_disposition)=={'EXCLUDE_FROM_T15__STRICT_T06'},str(ov.t15_overlap_disposition.value_counts().to_dict()))
# positive structure
acc_ids=set(acc.question_implementation_id)
strict_pairs=set()
for _,r in ov.iterrows():
 n=tuple(sorted(json.loads(r.norm_implementation_ids_json or '[]'))); p=tuple(sorted(json.loads(r.praxis_implementation_ids_json or '[]'))); strict_pairs.add((n,p))
for _,r in pos.iterrows():
 rid=r.worker_relation_id
 mem=json.loads(r.member_implementation_ids_json); roles=json.loads(r.role_assignments_json)
 ck('known_members:'+rid,all(i in acc_ids for i in mem),str(mem))
 nr=[z for z in roles if z.get('t15_member_role')=='NORM_SHORE']; pr=[z for z in roles if z.get('t15_member_role')=='PRACTICAL_REALIZATION_SHORE']
 ck('has_norm_and_praxis:'+rid,len(nr)>=1 and len(pr)>=1,f'norm={len(nr)} praxis={len(pr)}')
 n=tuple(sorted(z['implementation_id'] for z in nr)); p=tuple(sorted(z['implementation_id'] for z in pr))
 ck('not_strict_t06_duplicate:'+rid,(n,p) not in strict_pairs,'')
 ck('positive_crosswalk_exists:'+rid,((xw.positive_relation_id==rid)&(xw.disposition=='POSITIVE_T15')).sum()==1,str(((xw.positive_relation_id==rid)&(xw.disposition=='POSITIVE_T15')).sum()))
 # wave-local members
 waves=set(acc.set_index('question_implementation_id').loc[mem].apply(lambda z:(z.source_family,z.wave),axis=1))
 ck('wave_local_members:'+rid,len(waves)==1 and next(iter(waves))==(r.source_family,r.wave),str(waves))
 # instrumental positive explicit authority (none expected)
 if r.manifestation_subtype=='INSTRUMENTAL_ENACTMENT': ck('instrumental_explicit_bridge:'+rid,r.bridge_basis_type in {'SOURCE_EXPLICIT_MEANS','GOVERNED_T04_BRIDGE','SOURCE_NATIVE_BATTERY_BRIDGE'},r.bridge_basis_type)
# blocker closure
for _,r in bl.iterrows():
 ck('blocker_crosswalk:'+r.blocker_id,((xw.blocker_id==r.blocker_id)&(xw.disposition=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY')).sum()==1,'')
# accounting bidirectional closure and counterpart symmetry
for _,r in acc.iterrows():
 if r.t15_norm_candidate=='YES': ck('norm_search:'+r.question_implementation_id,r.norm_to_praxis_search_completed=='YES','')
 if r.t15_praxis_candidate=='YES': ck('praxis_search:'+r.question_implementation_id,r.praxis_to_norm_search_completed=='YES','')
 cps=json.loads(r.plausible_counterpart_implementation_ids_json or '[]')
 for j in cps:
  if j not in acc_ids: ck('counterpart_known:'+r.question_implementation_id,False,j)
# all crosswalk participants show mutual counterpart links
aby=acc.set_index('question_implementation_id')
for _,r in xw.iterrows():
 ns=json.loads(r.norm_implementation_ids_json or '[]'); ps=json.loads(r.praxis_implementation_ids_json or '[]')
 for n in ns:
  cps=set(json.loads(aby.loc[n].plausible_counterpart_implementation_ids_json or '[]')); ck('xw_norm_counterpart:'+r.crosswalk_id+':'+n,set(ps).issubset(cps),str(set(ps)-cps))
 for p in ps:
  cps=set(json.loads(aby.loc[p].plausible_counterpart_implementation_ids_json or '[]')); ck('xw_praxis_counterpart:'+r.crosswalk_id+':'+p,set(ns).issubset(cps),str(set(ns)-cps))
# wave arithmetic
ck('attestation_five_waves',len(att)==5,str(len(att)))
ck('attestation_denominator_sum',att.implementation_denominator.astype(int).sum()==2986,str(att.implementation_denominator.astype(int).sum()))
for _,r in att.iterrows():
 g=pos[(pos.source_family==r.source_family)&(pos.wave==r.wave)]; gx=xw[(xw.source_family==r.source_family)&(xw.wave==r.wave)]
 ck('att_pos:'+r.source_family+':'+r.wave,int(r.positive_t15_count)==len(g),f'{r.positive_t15_count}/{len(g)}')
 ck('att_block:'+r.source_family+':'+r.wave,int(r.blocked_count)==int((gx.disposition=='BLOCKED_SOURCE_OR_BRIDGE_AMBIGUITY').sum()),'')
 ck('att_strict:'+r.source_family+':'+r.wave,int(r.strict_t06_overlap_count)==int((gx.disposition=='EXCLUDE_FROM_T15__STRICT_T06').sum()),'')
# expected hostile counts
expected_sub={'PRACTICAL_VIOLATION':5,'RIGHT_OR_PERMISSION_EXERCISE':3,'DIRECT_ENACTMENT':2,'INSTITUTIONAL_OR_SOCIAL_REALIZATION':2}
ck('subtype_counts',pos.manifestation_subtype.value_counts().to_dict()==expected_sub,str(pos.manifestation_subtype.value_counts().to_dict()))
expected_wave={('GSS','2016'):2,('GSS','1993'):1,('EVS','1999'):2,('Latinobarómetro','2011'):2,('Asian Barometer','W4'):5}
actual=pos.groupby(['source_family','wave']).size().to_dict(); ck('wave_positive_counts',actual==expected_wave,str(actual))
# no coverage defects, repairs anchored
cov=pd.read_csv(R/'T15_SOURCE_COVERAGE_DEFECTS.csv',dtype=str).fillna(''); ck('coverage_defects_zero',len(cov)==0,str(len(cov)))
ck('upstream_repairs_three',len(rep)==3,str(len(rep)))
for _,r in rep.iterrows(): ck('repair_member_known:'+r.repair_id,r.question_implementation_id in acc_ids,r.question_implementation_id)
# provided validator result
val=json.loads((R/'VALIDATION.json').read_text()); ck('provided_validator_pass',val.get('status')=='PASS' and val.get('error_count')==0,str(val))
res={'status':'PASS' if not errs else 'FAIL','error_count':len(errs),'errors':errs,'checks_run':len(checks),'checks':checks}
(R/'HOSTILE_QA.json').write_text(json.dumps(res,indent=2,ensure_ascii=False))
print(json.dumps({k:res[k] for k in ['status','error_count','errors','checks_run']},indent=2))
sys.exit(0 if not errs else 1)
