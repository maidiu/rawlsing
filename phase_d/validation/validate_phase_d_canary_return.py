#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys, pandas as pd
ap=argparse.ArgumentParser(); ap.add_argument('return_dir',nargs='?',default='.')
a=ap.parse_args(); r=Path(a.return_dir); errs=[]
can=r/'PHASE_D_NINE_FAMILY_CANARY_RETURN.csv'; ev=r/'POSITIONED_RELATIONAL_EVIDENCE_CANARY.csv'; ag=r/'APP_GATE_A_EVIDENCE.csv'; man=r/'PHASE_D_RUN_MANIFEST.json'
for p in [can,ev,ag,man]:
 if not p.exists(): errs.append(f'missing {p.name}')
if not errs:
 c=pd.read_csv(can,dtype=str).fillna(''); e=pd.read_csv(ev,dtype=str).fillna(''); g=pd.read_csv(ag,dtype=str).fillna(''); m=json.loads(man.read_text())
 expected={'Afrobarometer','Arab Barometer','Asian Barometer','EVS','GSS','Latinobarómetro','LiTS','South Asia','WVS'}
 if len(c)!=9 or set(c.source_family)!=expected: errs.append('canary return must contain exact 9 families')
 allowed={'PASS_POSITIVE','PASS_EMPIRICAL_ONLY','PASS_BLOCKED_LOCAL','FAIL'}
 if not set(c.terminal_status).issubset(allowed): errs.append('invalid canary terminal status')
 if (c.terminal_status=='FAIL').any(): errs.append('one or more family scopes FAIL')
 for _,x in c.iterrows():
  if x.terminal_status=='PASS_BLOCKED_LOCAL' and (not x.blocked_code or not x.blocked_detail): errs.append(f'blocked family missing detail: {x.source_family}')
  if not x.evidence_refs_json: errs.append(f'family missing evidence refs: {x.source_family}')
 if e.empty: errs.append('positioned evidence empty')
 else:
  for _,x in e.iterrows():
   if not x.evidence_id or not x.provenance_refs_json: errs.append('evidence row missing id/provenance')
   if x.semantic_relation_posture=='GOVERNED_POSITIVE' and not x.relation_authority_id: errs.append(f'positive semantic row lacks authority id {x.evidence_id}')
   if x.association_mode=='PRODUCTION_ACTIVE':
    if x.design_grade not in {'FULL_SURVEY_DESIGN','SRS_EXPLICITLY_AUTHORIZED'}: errs.append(f'production without design grade {x.evidence_id}')
    try:
     q=float(x.q_value)
     if q>0.05: errs.append(f'production q>0.05 {x.evidence_id}')
    except: errs.append(f'production missing q {x.evidence_id}')
    if x.respondent_universe_status!='EXACT_SAME_RESPONDENT_UNIVERSE' or x.routing_status!='COMPATIBLE': errs.append(f'production join not exact {x.evidence_id}')
 auth_ids=set(); auth_file=r/'JOB3_R3_FINAL_GOVERNED_RELATION_TOPOLOGY_R1.csv'
 if auth_file.exists(): auth_ids=set(pd.read_csv(auth_file,dtype=str).authority_id)
 if auth_ids:
  bad=e[(e.semantic_relation_posture=='GOVERNED_POSITIVE') & ~e.relation_authority_id.isin(auth_ids)]
  if len(bad): errs.append(f'{len(bad)} positive evidence rows reference unknown Job3 authority ids')
 obs_pos=((e.semantic_relation_posture=='GOVERNED_POSITIVE') & (e.empirical_cotravel_posture=='OBSERVED')).any()
 semantic_survives=((e.semantic_relation_posture=='GOVERNED_POSITIVE') & e.empirical_cotravel_posture.isin(['NOT_OBSERVED','UNDERPOWERED','BLOCKED_LOCAL','NOT_TESTED'])).any()
 anti_erase=(e.semantic_relation_posture.isin(['BLOCKED_TYPED_RELATION','NO_GOVERNED_TYPED_RELATION']) & (e.empirical_cotravel_posture=='OBSERVED')).any()
 local_block=(c.terminal_status=='PASS_BLOCKED_LOCAL').any() or (e.empirical_cotravel_posture=='BLOCKED_LOCAL').any()
 for name,ok in [('positive_observed',obs_pos),('semantic_survives_empirical_nonobservation',semantic_survives),('empirical_survives_semantic_block_or_absence',anti_erase),('local_block_preserved',local_block)]:
  if not ok: errs.append(f'missing required archetype: {name}')
 if g.empty: errs.append('APP_GATE_A evidence empty')
 required_dims={'POSITION_DISTRIBUTION','MINORITY_OUTLIER','RECURSIVE_BRANCH','ATTITUDE_CLOUD_OR_COSIGNATURE','V550J_JOINT','SEMANTIC_EMPIRICAL_INDEPENDENCE','STRATA_HORIZON','UNCERTAINTY_PROVENANCE'}
 for fam in expected:
  dims=set(g.loc[g.source_family==fam,'gate_dimension']); miss=required_dims-dims
  if miss: errs.append(f'{fam} missing APP-GATE dimensions {sorted(miss)}')
 if not m.get('local_head_sha'): errs.append('manifest missing local_head_sha')
 if m.get('fused_ancestor_verified') is not True: errs.append('manifest does not attest fused ancestor')
print(json.dumps({'status':'PASS' if not errs else 'FAIL','errors':errs},indent=2)); sys.exit(1 if errs else 0)
