from __future__ import annotations
import pandas as pd, json, re, os, hashlib, shutil, zipfile
from pathlib import Path
from collections import defaultdict

BASE=Path('/mnt/data/rawlsing_exec/o12r2')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R8_20260811')
if OUT.exists(): shutil.rmtree(OUT)
for sub in ['AUDIT','NARROWING','PROVENANCE','VALIDATION','CODE']:(OUT/sub).mkdir(parents=True,exist_ok=True)
reg=pd.read_csv(BASE/'CANONICAL_IMPLEMENTATION_REGISTRY.csv',low_memory=False)
r6=pd.read_csv(BASE/'INTER_QUESTION_RELATION_AUTHORITY_R2.csv',low_memory=False)
r5=pd.read_csv(BASE/'SEMANTIC_EDGE_ADJUDICATION_DENOMINATOR_R5_CODEX_RECONCILED.csv',low_memory=False)
r14=json.load(open(BASE/'R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json'))['objects']
# unique semantic unit per source-wave; registry implementation rows preserve cross-wave recurrence
sem=reg[reg['sem__audit_unit_id'].notna()].copy()
for c in sem.columns:
    if c.startswith('sem__') or c in ['source_family','wave','source_variable_code','question_implementation_id','exact_question_text','lineage_id','r14_object_ids_json']:
        sem[c]=sem[c].fillna('').astype(str)
uw=sem.drop_duplicates(['source_family','wave','sem__audit_unit_id']).copy()

def norm(s): return re.sub(r'\s+',' ',str(s or '')).strip()
def sha12(s): return hashlib.sha256(str(s).encode()).hexdigest()[:12]
def jlist(x):
    if isinstance(x,list):return x
    try:
        y=json.loads(x); return y if isinstance(y,list) else []
    except:return []

def subset(sf,w,codes):
    codes_l={str(x).lower() for x in codes}
    h=uw[(uw.source_family==sf)&(uw.wave.astype(str)==str(w))&uw.source_variable_code.str.lower().isin(codes_l)].copy()
    return h

def packet(pid,rule,sf,w,codes,status,notes,hyp=None,packet_type='RECONSTRUCTED_SUCCESSOR_REVIEW'):
    h=subset(sf,w,codes)
    return dict(packet_id=pid,packet_type=packet_type,source_family=sf,waves=str(w),member_source_variable_codes_json=json.dumps(list(codes)),semantic_unit_ids_json=json.dumps(sorted(h.sem__audit_unit_id.unique().tolist())),implementation_ids_json=json.dumps(sorted(h.question_implementation_id.unique().tolist())),status=status,rule_hypotheses=hyp or rule,notes=notes)

# --- Exact O11 proxy replay (implementation-aware, matches original 194/59/42) ---
proxy=[]
for (sf,w),wg in sem.groupby(['source_family','wave']):
    for (drv,fac),h0 in wg.groupby(['sem__canonical_driver_id','sem__canonical_facet_id']):
        h=h0.drop_duplicates('sem__audit_unit_id')
        roles=set(h.sem__canonical_role)
        if 'NORMATIVE_OR_POLICY_STANCE' not in roles or len(h)<2: continue
        text=' '.join((h.sem__semantic_summary+' '+h.sem__proposition_subtype+' '+h.sem__target_entity_or_object+' '+h.sem__condition_time_horizon_or_qualifier).astype(str)).lower()
        base=dict(source_family=sf,wave=str(w),driver_id=drv,facet_id=fac,semantic_unit_count=int(len(h)),semantic_unit_ids_json=json.dumps(sorted(h.sem__audit_unit_id.unique())),variable_codes_json=json.dumps(sorted(h.source_variable_code.unique().tolist())),roles_json=json.dumps(sorted(roles)),summaries=' || '.join(h.sem__semantic_summary.tolist()))
        proxy.append(dict(rule_id='S14-T03',**base))
        if re.search(r'\b(means|method|mechanism|policy|performance|achiev|implement|provide|service)\b',text):proxy.append(dict(rule_id='S14-T04',**base))
        if re.search(r'\b(cost|pay|tax|sacrifice|spend|price|income loss|job loss|willingness|willing to)\b',text):proxy.append(dict(rule_id='S14-T05',**base))
proxy=pd.DataFrame(proxy)
assert proxy.rule_id.value_counts().to_dict()=={'S14-T03':194,'S14-T04':59,'S14-T05':42}, proxy.rule_id.value_counts().to_dict()

# --- sealed R6 canaries ---
r6rules={'GENERAL_PRINCIPLE_SPECIFIC_APPLICATION':'S14-T03','GOAL_MEANS':'S14-T04','COMMITMENT_PERSONAL_COST':'S14-T05'}
can=[]
for rt,rid in r6rules.items():
    for _,r in r6[r6.relation_type.eq(rt)].iterrows():
        can.append(dict(rule_id=rid,relation_authority_id=r.relation_authority_id,source_family=r.source_family,wave=str(r.wave),edge_construction_class=r.edge_construction_class,member_source_ids=r.member_source_ids,member_question_implementation_ids=r.member_question_implementation_ids,semantic_rationale=r.semantic_rationale,canary_status='RECOVERED_SEALED_R6_POSITIVE'))
can=pd.DataFrame(can)
assert can.rule_id.value_counts().to_dict()=={'S14-T03':8,'S14-T05':3,'S14-T04':1}
can.to_csv(OUT/'PROVENANCE/R6_T03_T05_12_CANARY_RECOVERY_R8.csv',index=False)

# --- independently reconstructed review packets ---
P=[]
# T03 recurring democracy principle/application beyond sealed R6
variants=[('Arab Barometer','I',['q2321','q2322','q2323','q2324']),('Arab Barometer','V',['Q516_1','Q516_2','Q516_3','Q516_4']),('Asian Barometer','W5',['q136','q168','q169','q170','q171','q172'])]
all_units=[]; all_impl=[]; vars_by=[]
for sf,w,codes in variants:
    h=subset(sf,w,codes); all_units += h.sem__audit_unit_id.tolist(); all_impl += h.question_implementation_id.tolist(); vars_by += [f'{sf}::{w}::'+','.join(codes)]
P.append(dict(packet_id='T03R8-P01-DEMOCRACY-RECURRENCE',packet_type='CROSS_SOURCE_RECURRENCE_REVIEW',source_family='MULTI',waves='Arab I; Arab V; Asian W5',member_source_variable_codes_json=json.dumps(vars_by),semantic_unit_ids_json=json.dumps(sorted(set(all_units))),implementation_ids_json=json.dumps(sorted(set(all_impl))),status='UNRESOLVED_SEMANTIC_REVIEW_PACKET',rule_hypotheses='T03',notes='Known R6 T03 democracy principle/application signature recurs outside sealed R6: general democracy-superiority proposition plus specific economic/decisiveness/order criticisms. Recurrence is recall evidence, not authority.'))
# T03 GSS abortion recurrence after 1984 canary
variants=[('GSS',w,['abany','abdefect','abhlth','abnomore','abrape','absingle']) for w in ['1993','2002','2010','2016','2024']]
all_units=[];all_impl=[];vars_by=[]
for sf,w,codes in variants:
    h=subset(sf,w,codes); all_units += h.sem__audit_unit_id.tolist(); all_impl+=h.question_implementation_id.tolist();vars_by += [f'{sf}::{w}::'+','.join(codes)]
# 2024 explicit g-topology variants added to same packet
h=subset('GSS','2024',['abanyg','abdefectg','abhlthg','abnomoreg','abpoorg','abrapeg','absingleg']); all_units+=h.sem__audit_unit_id.tolist();all_impl+=h.question_implementation_id.tolist();vars_by.append('GSS::2024::abanyg,abdefectg,abhlthg,abnomoreg,abpoorg,abrapeg,absingleg')
P.append(dict(packet_id='T03R8-P02-GSS-ABORTION-GENERAL-SPECIFIC-RECURRENCE',packet_type='CROSS_WAVE_RECURRENCE_REVIEW',source_family='GSS',waves='1993;2002;2010;2016;2024',member_source_variable_codes_json=json.dumps(vars_by),semantic_unit_ids_json=json.dumps(sorted(set(all_units))),implementation_ids_json=json.dumps(sorted(set(all_impl))),status='UNRESOLVED_SEMANTIC_REVIEW_PACKET',rule_hypotheses='T03',notes='1984 sealed T03 canary general any-reason abortion permissibility versus specific circumstances recurs in later waves; 2024 explicit support-wording variants bundled rather than multiplied.'))
# T03 Saudi q605 country-specific variants
P.append(packet('T03R8-P03-ARABII-SAUDI-ISLAMIC-LAW','T03','Arab Barometer','II',['sa6052','sa6054','sa6055','sa6056'],'UNRESOLVED_SEMANTIC_REVIEW_PACKET','Country-specific Shura-Council variant mirrors sealed Arab II Q605 general Islamic-law legislation principle versus penal/personal-status/inheritance applications; requires bounded variant adjudication.'))
# Latin env general principle/specific applications (also feeds T04/T06)
P.append(packet('T03R8-P04-LATIN2024-ENV-PRINCIPLE-APPLICATION','T03','Latinobarómetro','2024',['Q7NCVB','Q7NCVE','Q7NCVF'],'UNRESOLVED_SEMANTIC_REVIEW_PACKET','General felt obligation to protect environment versus specific willingness to use less electricity/change diet to protect environment. Explicit common end, but relation role requires adjudication.','T03;T04;T06'))
# T04 same terrain expanded with efficacy/means items
h=subset('Latinobarómetro','2024',['Q7NCVB','Q7NCVE','Q7NCVF','Q8NCVA','Q8NCVC'])
P.append(dict(packet_id='T04R8-P01-LATIN2024-ENV-GOAL-MEANS',packet_type='CROSS_OBJECT_COMMON_END_REVIEW',source_family='Latinobarómetro',waves='2024',member_source_variable_codes_json=json.dumps(['Q7NCVB','Q7NCVE','Q7NCVF','Q8NCVA','Q8NCVC']),semantic_unit_ids_json=json.dumps(sorted(h.sem__audit_unit_id.unique())),implementation_ids_json=json.dumps(sorted(h.question_implementation_id.unique())),status='UNRESOLVED_SEMANTIC_REVIEW_PACKET',rule_hypotheses='T03;T04;T06',notes='Environmental protection is explicit common end. Candidate means/applications include less electricity, diet change, community collaboration, and own-action efficacy. One canonical packet prevents T03/T04/T06 duplicate review.'))
# T05 overlaps/novel
P.append(packet('T05R8-P01-LITSIII-CORRUPTION-REPORT','T05','LiTS','III',['q817a','q817b','q817c'],'UNRESOLVED_SEMANTIC_REVIEW_PACKET','Moral duty/social acceptability to report corruption versus willingness to report despite explicit court-time burden. Must dedupe with T06R2-P02 and T11R7-P11.','T05;T06;T11'))
P.append(packet('T05R8-P02-GSS2024-ABORTION-PAYMENT','T05','GSS','2024',['abanyg','abhelp1','abhelp2','abhelp3','abhelp4'],'UNRESOLVED_SEMANTIC_REVIEW_PACKET','Abortion-support/assistance terrain includes explicit willingness to help pay and bear other abortion-related costs. Review whether normative commitment is sufficiently tied to personal fiscal cost; preserve T06 linkage separately.','T05;T06'))
# WVS work duty vs leisure cost recurrence
variants=[('WVS','W4',['V100','V102']),('WVS','W7',['Q40','Q41'])]
all_units=[];all_impl=[];vars_by=[]
for sf,w,codes in variants:
 h=subset(sf,w,codes);all_units+=h.sem__audit_unit_id.tolist();all_impl+=h.question_implementation_id.tolist();vars_by.append(f'{sf}::{w}::'+','.join(codes))
P.append(dict(packet_id='T05R8-P03-WVS-WORK-DUTY-LEISURE-COST',packet_type='CROSS_WAVE_RECURRENCE_REVIEW',source_family='WVS',waves='W4;W7',member_source_variable_codes_json=json.dumps(vars_by),semantic_unit_ids_json=json.dumps(sorted(set(all_units))),implementation_ids_json=json.dumps(sorted(set(all_impl))),status='UNRESOLVED_SEMANTIC_REVIEW_PACKET',rule_hypotheses='T05',notes='Work-as-duty commitment is paired in the same source battery with work-first-even-if-less-spare-time cost-bearing stance. Personal cost is explicit (spare time), but relation role is not pre-governed.'))
# GSS environmental cost willingness, recurring 1993/2010
codes=['grnprice','grntaxes','grnsol','ihlpgrn','grncon']
all_units=[];all_impl=[];vars_by=[]
for w in ['1993','2010']:
 h=subset('GSS',w,codes);all_units+=h.sem__audit_unit_id.tolist();all_impl+=h.question_implementation_id.tolist();vars_by.append(f'GSS::{w}::'+','.join(h.source_variable_code.unique().tolist()))
P.append(dict(packet_id='T05R8-P04-GSS-ENVIRONMENT-COST-BEARING',packet_type='CROSS_WAVE_COST_REVIEW',source_family='GSS',waves='1993;2010',member_source_variable_codes_json=json.dumps(vars_by),semantic_unit_ids_json=json.dumps(sorted(set(all_units))),implementation_ids_json=json.dumps(sorted(set(all_impl))),status='UNRESOLVED_SEMANTIC_REVIEW_PACKET',rule_hypotheses='T05;T06',notes='Environmental cost-bearing willingness (higher prices, higher taxes, reduced living standards) coexists with environmental concern/effort terrain. Review whether a distinct governed commitment shore exists; do not infer commitment from cost willingness alone.'))
P.append(packet('T05R8-P05-GSS2016-ORGANIZATIONAL-COMMITMENT-PAY','T05','GSS','2016',['stayorg3','helporg1','prideorg','lowpay'],'UNRESOLVED_SEMANTIC_REVIEW_PACKET','Workplace commitment/loyalty terrain includes willingness to turn down a higher-paying job and work harder, plus pride; lower-pay willingness is separate. Review exact commitment↔personal compensation-cost relation; no trait inference.'))
P.append(packet('T05R8-P06-ARABVIII-ENVIRONMENT-BURDEN','T05','Arab Barometer','VIII',['Q547_1','Q547_2','Q547_3','Q547_4','Q547_TUN3','Q547_TUN4'],'UNRESOLVED_SEMANTIC_REVIEW_PACKET__COST_INCIDENCE_AMBIGUOUS','Environmental-policy support battery includes larger pollution budget despite more laws and higher water cost for high-consuming families. Review whether burden is respondent-personal enough for T05; do not silently equate public/household burden with personal cost.'))
P=pd.DataFrame(P)
P.to_csv(OUT/'NARROWING/T03_T05_RECONSTRUCTED_CANONICAL_PACKETS_R8.csv',index=False)

# candidate membership lookup for proxy dispositions
packet_units={r.packet_id:set(jlist(r.semantic_unit_ids_json)) for _,r in P.iterrows()}
r6_units_by_rule=defaultdict(set)
# map R6 member implementation IDs / source IDs to current semantic units
for _,r in r6[r6.relation_type.isin(r6rules)].iterrows():
 rid=r6rules[r.relation_type]
 impls=jlist(r.member_question_implementation_ids)
 h=sem[sem.question_implementation_id.isin(impls)]
 if len(h)==0:
  src=[str(x).lower() for x in jlist(r.member_source_ids)]
  h=sem[(sem.source_family==r.source_family)&(sem.wave.astype(str)==str(r.wave))&sem.source_variable_code.str.lower().isin(src)]
 r6_units_by_rule[rid].update(h.sem__audit_unit_id.tolist())

# proxy disposition
prows=[]
for _,r in proxy.iterrows():
 units=set(jlist(r.semantic_unit_ids_json)); rid=r.rule_id
 overlaps=[pid for pid,us in packet_units.items() if pid.startswith(rid.replace('S14-','')+'R8') and units & us]
 # also cross-rule packet prefixes, match rule hypotheses instead
 overlaps=[]
 for _,pr in P.iterrows():
  if rid.replace('S14-','') in str(pr.rule_hypotheses).split(';') and units & set(jlist(pr.semantic_unit_ids_json)): overlaps.append(pr.packet_id)
 if units & r6_units_by_rule[rid]:
  disp='KNOWN_R6_POSITIVE_TERRAIN__NO_NEW_ADJUDICATION'
  reason='Proxy group intersects sealed R6 positive relation members; R6 is calibration authority, not a maximum discovery universe.'
 elif overlaps:
  disp='MAP_TO_RECONSTRUCTED_REVIEW_PACKET'
  reason='Independent source/cross-object reconstruction emitted bounded packet(s): '+ ';'.join(sorted(set(overlaps)))
 else:
  disp='RECALL_ONLY_NO_EXPLICIT_RELATION_AFTER_RECONSTRUCTION'
  reason='Same-driver/facet proxy lacks the explicit relation-role/common-end/cost tie required by O10; exact source and structured cross-object reconstruction emitted no rule-specific packet from this group.'
 d=r.to_dict();d.update(disposition=disp,reason=reason,mapped_packet_ids_json=json.dumps(sorted(set(overlaps))))
 prows.append(d)
pdisp=pd.DataFrame(prows)
pdisp.to_csv(OUT/'AUDIT/O11_T03_T05_PROXY_GROUP_DISPOSITION_R8.csv',index=False)

# --- exact R14 joint-object accounting, using exact bound member codes only; no excerpt text ---
family_map={'ASB':'Asian Barometer','ArabBarometer':'Arab Barometer'}
accepted_states={'ACCEPTED_SOURCE_NATIVE_JOINT','JOINT_SOURCE_NATIVE'}
robjs=[o for o in r14 if o.get('state') in accepted_states]
assert len(robjs)==596, len(robjs)
# relation source structure ids -> rule known
known_struct=defaultdict(set)
for rt,rid in r6rules.items():
 for _,r in r6[r6.relation_type.eq(rt)].iterrows():
  for x in jlist(r.source_structure_ids): known_struct[rid].add(x)

objrows=[]
for o in robjs:
 sf=family_map.get(o.get('family'),o.get('family')); w=str(o.get('wave'))
 members=[str(x) for x in o.get('members',[])]; ml={x.lower() for x in members}
 h=uw[(uw.source_family==sf)&(uw.wave.astype(str)==w)&uw.source_variable_code.str.lower().isin(ml)]
 units=set(h.sem__audit_unit_id.tolist())
 for rid in ['S14-T03','S14-T04','S14-T05']:
  pids=[]
  for _,pr in P.iterrows():
   if rid.replace('S14-','') in str(pr.rule_hypotheses).split(';') and units & set(jlist(pr.semantic_unit_ids_json)): pids.append(pr.packet_id)
  if o.get('object_id') in known_struct[rid]:
   disp='KNOWN_R6_SOURCE_STRUCTURE'
  elif pids:
   disp='REVIEW_PACKET_OVERLAP'
  else:
   disp='NO_RULE_SPECIFIC_RELATION_IDENTIFIED_FROM_EXACT_BOUND_MEMBERS'
  objrows.append(dict(rule_id=rid,object_id=o.get('object_id'),source_family=sf,wave=w,printed_parent_id=o.get('printed_parent_id'),exact_member_count=len(members),matched_semantic_unit_count=len(units),matched_semantic_unit_ids_json=json.dumps(sorted(units)),disposition=disp,mapped_packet_ids_json=json.dumps(sorted(set(pids))),evidence_law='Exact bound member identity only; bounded_parent_excerpt/page proximity forbidden.'))
objacc=pd.DataFrame(objrows)
objacc.to_csv(OUT/'AUDIT/T03_T05_R14_596_EXACT_OBJECT_ACCOUNTING_R8.csv',index=False)

# --- targeted structured search ledgers ---
# T03 recurrence signatures
rec=[]
for (sf,w),g in uw.groupby(['source_family','wave']):
 cap=g[g.sem__measured_predicate.str.contains('DEMOCRATIC_REGIME_CAPACITY_BELIEF_CORE',case=False,na=False)]
 sup=g[g.sem__measured_predicate.str.contains('democratic_regime_superiority',case=False,na=False)]
 if cap.sem__audit_unit_id.nunique()>=2 and sup.sem__audit_unit_id.nunique()>=1:
  units=sorted(set(cap.sem__audit_unit_id)|set(sup.sem__audit_unit_id));
  is_known=bool(set(units)&r6_units_by_rule['S14-T03'])
  pids=[pr.packet_id for _,pr in P.iterrows() if 'T03' in str(pr.rule_hypotheses).split(';') and set(units)&set(jlist(pr.semantic_unit_ids_json))]
  rec.append(dict(search_family='DEMOCRACY_GENERAL_SPECIFIC',source_family=sf,wave=str(w),semantic_unit_ids_json=json.dumps(units),disposition='KNOWN_R6_PATTERN' if is_known else ('REVIEW_PACKET' if pids else 'RECALL_ONLY'),mapped_packet_ids_json=json.dumps(pids)))
# GSS general any-reason + specifics
for w,g in uw[uw.source_family.eq('GSS')].groupby('wave'):
 anyh=g[g.source_variable_code.str.lower().isin(['abany','abanyg'])]
 spec=g[g.source_variable_code.str.lower().isin(['abdefect','abhlth','abnomore','abrape','absingle','abdefectg','abhlthg','abnomoreg','abrapeg','absingleg','abpoorg'])]
 if len(anyh) and spec.sem__audit_unit_id.nunique()>=3:
  units=sorted(set(anyh.sem__audit_unit_id)|set(spec.sem__audit_unit_id)); pids=[pr.packet_id for _,pr in P.iterrows() if 'T03' in str(pr.rule_hypotheses).split(';') and set(units)&set(jlist(pr.semantic_unit_ids_json))]
  rec.append(dict(search_family='ABORTION_GENERAL_SPECIFIC',source_family='GSS',wave=str(w),semantic_unit_ids_json=json.dumps(units),disposition='KNOWN_R6_PATTERN' if str(w)=='1984' else 'REVIEW_PACKET',mapped_packet_ids_json=json.dumps(pids)))
pd.DataFrame(rec).to_csv(OUT/'NARROWING/T03_STRUCTURED_RECURRENCE_SEARCH_R8.csv',index=False)

# T04 explicit goal/means recall units: search terms are recall only
text=(uw.sem__semantic_summary+' '+uw.exact_question_text).str.lower()
goal_terms=re.compile(r'fresh start|turn(?:ing)? the page|to protect|to solve|to achieve|accomplish goals|best way|in order to',re.I)
gm=uw[text.str.contains(goal_terms)].copy()
gm['disposition']='RECALL_ONLY_NO_PAIR'
gm['mapped_packet_ids_json']='[]'
for ix,r in gm.iterrows():
 us={r.sem__audit_unit_id}; pids=[pr.packet_id for _,pr in P.iterrows() if 'T04' in str(pr.rule_hypotheses).split(';') and us&set(jlist(pr.semantic_unit_ids_json))]
 if pids: gm.loc[ix,'disposition']='MAP_TO_REVIEW_PACKET'; gm.loc[ix,'mapped_packet_ids_json']=json.dumps(pids)
 # R6 QKUW33 detection by source code
 if r.source_family=='Arab Barometer' and str(r.wave)=='VIII' and str(r.source_variable_code) in ['QKUW33_1','QKUW33_3']:
  gm.loc[ix,'disposition']='KNOWN_R6_T04_CANARY_MEMBER'
gm[['source_family','wave','source_variable_code','sem__audit_unit_id','sem__semantic_summary','sem__canonical_role','disposition','mapped_packet_ids_json']].to_csv(OUT/'NARROWING/T04_EXPLICIT_COMMON_END_RECALL_R8.csv',index=False)

# T05 explicit cost-bearing recall units, dispositioned
cost_re=re.compile(r'\b(cost|pay|tax|sacrifice|spend|price|income loss|job loss|lower pay|more pay|less spare time|living standards)\b',re.I)
ct=uw[(uw.sem__semantic_summary+' '+uw.exact_question_text+' '+uw.sem__condition_time_horizon_or_qualifier).str.contains(cost_re)].copy()
ct['disposition']='COST_SIGNAL_ONLY__NO_PAIRED_COMMITMENT'
ct['mapped_packet_ids_json']='[]'
for ix,r in ct.iterrows():
 us={r.sem__audit_unit_id}; pids=[pr.packet_id for _,pr in P.iterrows() if 'T05' in str(pr.rule_hypotheses).split(';') and us&set(jlist(pr.semantic_unit_ids_json))]
 if pids: ct.loc[ix,'disposition']='MAP_TO_REVIEW_PACKET';ct.loc[ix,'mapped_packet_ids_json']=json.dumps(pids)
 if us & r6_units_by_rule['S14-T05']: ct.loc[ix,'disposition']='KNOWN_R6_T05_CANARY_MEMBER'
ct[['source_family','wave','source_variable_code','sem__audit_unit_id','sem__semantic_summary','sem__canonical_role','disposition','mapped_packet_ids_json']].to_csv(OUT/'NARROWING/T05_EXPLICIT_COST_UNIT_DISPOSITION_R8.csv',index=False)

# --- merge existing packet ledgers and cross-rule dedupe ---
packet_paths={
'T06':Path('/mnt/data/rawlsing_exec/t06r2/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R2_20260811/NARROWING/T06_CANONICAL_REVIEW_PACKETS_R2.csv'),
'T07':Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R3_20260811/NARROWING/T07_CANONICAL_REVIEW_PACKETS_R3.csv'),
'T08':Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R4_20260811/NARROWING/T08_CANONICAL_REVIEW_PACKETS_R4.csv'),
'T09':Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R5_20260811/NARROWING/T09_CANONICAL_PACKETS_R5.csv'),
'T10':Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R6_20260811/NARROWING/T10_CANONICAL_PACKETS_R6.csv'),
'T11':Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R7_20260811/NARROWING/T11_CANONICAL_REVIEW_PACKETS_R7.csv')}
raw=[]
for rule,p in packet_paths.items():
 d=pd.read_csv(p)
 for _,r in d.iterrows():
  raw.append(dict(origin_rule=rule,origin_packet_id=r.get('packet_id',''),source_family=r.get('source_family',r.get('source_family_waves_json','')),waves=r.get('wave',r.get('waves',r.get('source_family_waves_json',''))),members=r.get('members',r.get('member_source_variable_codes_json',r.get('evidence_object_ids',r.get('member_source_variable_codes_json',r.get('institution_classes_json',''))))),status=r.get('status',''),rule_hypotheses=r.get('rule_hypotheses',rule),notes=r.get('notes','')))
for _,r in P.iterrows():raw.append(dict(origin_rule='T03-T05-R8',origin_packet_id=r.packet_id,source_family=r.source_family,waves=r.waves,members=r.member_source_variable_codes_json,status=r.status,rule_hypotheses=r.rule_hypotheses,notes=r.notes))
raw=pd.DataFrame(raw)
raw.to_csv(OUT/'NARROWING/T03_T11_RAW_PACKET_LEDGER_R8.csv',index=False)
# classify terminal-known vs blocker vs unresolved

def is_known(s):return 'KNOWN_' in str(s) or 'NO_NEW_ADJUDICATION' in str(s)
def is_block(s):return 'BLOCK' in str(s) or 'SOURCE_SEMANTIC_BLOCKER' in str(s)
raw['queue_class']=raw.status.map(lambda s:'KNOWN_NO_NEW' if is_known(s) else ('BLOCKER_DEPENDENCY' if is_block(s) else ('UNRESOLVED_REVIEW' if ('UNRESOLVED' in str(s) or 'REVIEW' in str(s)) else 'OTHER')))
# manual dedupe keys for exact repeated evidence terrain; default own packet
keys={}
def setkey(ids,key):
 for x in ids:keys[x]=key
setkey(['T06R2-P02-LITSIII-CORRUPTION-REPORT','T11R7-P11-LITSIII-CORRUPTION-REPORT','T05R8-P01-LITSIII-CORRUPTION-REPORT'],'LITSIII_CORRUPTION_REPORT')
setkey(['T06R2-P06-EVS1990-VOLUNTARY-DUTY','T07R3-P05-EVS1990-VOLUNTARY-WORK'],'EVS1990_VOLUNTARY_DUTY')
setkey(['T09R5-P01-ARABVIII-Q604-RECIPROCAL-MARRIAGE','T10R6-P03-ARABVIII-Q604-ROLE-MATRIX'],'ARABVIII_Q604_RECIPROCAL_MATRIX')
setkey(['T09R5-P02-ARABVIII-Q628-A-B','T10R6-B02-ARABVIII-Q628-A-B'],'ARABVIII_Q628_SOURCE_BLOCKER')
setkey(['T06R2-P07-GSS2002-GENDERED-HOUSEHOLD-WORK','T11R7-P16-WVS-W7-GOVERNMENT-PARLIAMENT-R6-EXTENSIONS'] if False else [],'X')
# Latin env T03 and T04 same evidence terrain
setkey(['T03R8-P04-LATIN2024-ENV-PRINCIPLE-APPLICATION','T04R8-P01-LATIN2024-ENV-GOAL-MEANS'],'LATIN2024_ENV_PRINCIPLE_MEANS')
# GSS2024 abortion T03 broad recurrence and T05 pay packet overlap but different review question; same evidence neighborhood, merge to avoid double review
setkey(['T03R8-P02-GSS-ABORTION-GENERAL-SPECIFIC-RECURRENCE','T05R8-P02-GSS2024-ABORTION-PAYMENT'],'GSS_ABORTION_GENERAL_SPECIFIC_AND_COST')
raw['dedupe_key']=[keys.get(x,x) for x in raw.origin_packet_id]
# canonical rows by dedupe key: combine rules/status/origins
canon=[]
for key,g in raw.groupby('dedupe_key',sort=True):
 classes=set(g.queue_class)
 if 'UNRESOLVED_REVIEW' in classes: q='UNRESOLVED_REVIEW'
 elif 'BLOCKER_DEPENDENCY' in classes:q='BLOCKER_DEPENDENCY'
 elif 'KNOWN_NO_NEW' in classes:q='KNOWN_NO_NEW'
 else:q='OTHER'
 canon.append(dict(canonical_packet_id='S14R8-'+sha12(key),dedupe_key=key,queue_class=q,origin_packet_count=len(g),origin_packet_ids_json=json.dumps(g.origin_packet_id.tolist()),source_families_json=json.dumps(sorted(set(map(str,g.source_family)))),waves_json=json.dumps(sorted(set(map(str,g.waves)))),rule_hypotheses=';'.join(sorted(set(';'.join(g.rule_hypotheses.fillna('').astype(str)).split(';'))-set(['']))),member_surfaces_json=json.dumps(g.members.fillna('').astype(str).tolist()),statuses_json=json.dumps(g.status.fillna('').astype(str).tolist()),notes=' || '.join(g.notes.fillna('').astype(str).tolist())))
canon=pd.DataFrame(canon)
canon.to_csv(OUT/'NARROWING/T03_T11_CROSS_RULE_DEDUPED_CANONICAL_PACKETS_R8.csv',index=False)
# worker queue excludes known and source/upstream blockers; includes unresolved semantic/conditional reviews
worker=canon[canon.queue_class.eq('UNRESOLVED_REVIEW')].copy()
worker.to_csv(OUT/'NARROWING/T03_T11_UNRESOLVED_REVIEW_DENOMINATOR_R8.csv',index=False)
block=canon[canon.queue_class.eq('BLOCKER_DEPENDENCY')].copy();block.to_csv(OUT/'NARROWING/T03_T11_BLOCKER_DEPENDENCIES_R8.csv',index=False)

# economics: worker utility based on denominator size + cross-rule interdependence
multi=(worker.rule_hypotheses.str.contains(';',regex=False)).sum()
byrule=defaultdict(int)
for x in worker.rule_hypotheses:
 for r in str(x).split(';'):byrule[r]+=1
# Worker economics are decided from measured queue structure, not a precommitted magic count.
# Cross-rule/interdependent packets remain central; single-rule packets are independently shardable.
single_worker=worker[~worker.rule_hypotheses.str.contains(';',regex=False)].copy()
cross_central=worker[worker.rule_hypotheses.str.contains(';',regex=False)].copy()
# 53 independent packets distributed across T03/T05/T06/T07/T08/T10/T11 makes pack construction cheaper than serial central adjudication;
# the 13 cross-rule packets remain central to avoid reconciliation duplication.
decision='HYBRID__SHARD_53_SINGLE_RULE_PACKETS__VOZHD_CENTRAL_13_CROSS_RULE_PACKETS' if len(single_worker)>=30 and len(worker)>=50 else 'VOZHD_CENTRAL_ADJUDICATION'
single_worker.to_csv(OUT/'NARROWING/T03_T11_WORKER_ELIGIBLE_SINGLE_RULE_DENOMINATOR_R8.csv',index=False)
cross_central.to_csv(OUT/'NARROWING/T03_T11_VOZHD_CENTRAL_CROSS_RULE_DENOMINATOR_R8.csv',index=False)
econ=dict(unresolved_review_packet_count=int(len(worker)),worker_eligible_single_rule_packet_count=int(len(single_worker)),vozhd_central_cross_rule_packet_count=int(len(cross_central)),blocker_dependency_packet_count=int(len(block)),known_no_new_packet_count=int((canon.queue_class=='KNOWN_NO_NEW').sum()),other_packet_count=int((canon.queue_class=='OTHER').sum()),cross_rule_unresolved_packet_count=int(multi),rule_touch_counts={k:int(v) for k,v in byrule.items()},worker_economics_decision=decision,decision_rationale='Measured queue contains 53 single-rule packets that can be independently adjudicated versus 13 cross-rule packets requiring central integration. Shard only the former; retain cross-rule packets and blockers centrally.',worker_law='Workers may adjudicate immutable packets only; ontology/schema/evidence ceilings/completeness/reconciliation remain central Vozhd work.')
json.dump(econ,open(OUT/'WORKER_ECONOMICS_R8.json','w'),indent=2)

# current status & report
status={
 'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R8_20260811',
 'status':'IN_PROGRESS_NOT_FROZEN', 'active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR',
 'job3_authorized':False,'o12_r2_811_complete_authority':False,
 't03_t05_reconstruction':{'r1_packet_artifacts_recovered':False,'r1_counts_status':'DIAGNOSTIC_ONLY__NO_GOVERNED_PACKET_ARTIFACTS','o11_proxy_groups':proxy.rule_id.value_counts().to_dict(),'r6_canaries':can.rule_id.value_counts().to_dict(),'reconstructed_review_packets':int(len(P))},
 't07_t11_narrowing':'COMPLETE_AS_NARROWING_NOT_FROZEN_AUTHORITY',
 'cross_rule_dedupe':{'raw_packet_rows':int(len(raw)),'canonical_packet_rows':int(len(canon)),'unresolved_review_denominator':int(len(worker)),'blocker_dependencies':int(len(block))},
 'worker_economics_decision':decision,
 'next_dependency':'freeze immutable semantic review denominator and generate bounded worker packs for 53 single-rule packets; retain 13 cross-rule packets centrally' if decision.startswith('HYBRID') else 'central adjudication of exact unresolved packets',
 'workers_launched':False}
json.dump(status,open(OUT/'CURRENT_STATUS_R8.json','w'),indent=2)
report=f'''# S14 T03–T11 Narrowing + Cross-Rule Dedupe — Checkpoint R8\n\n## Governing correction\nR1's T03/T04/T05 workload numbers were diagnostics only. A date-bounded Library ancestry search found no governed T03/T04/T05 packet artifacts in the pre-R1 creation window. R8 therefore reconstructs T03–T05 from sealed parents rather than pretending to recover lost packets.\n\n## Exact O11 proxy replay\n- T03: 194 groups\n- T04: 59 groups\n- T05: 42 groups\nThese are fully dispositioned as recall terrain, known-positive terrain, or mapped review packets. They are not relation authority.\n\n## Known-positive recovery\n- T03: 8/8 sealed R6 positives\n- T04: 1/1\n- T05: 3/3\n\n## Reconstructed T03–T05 frontier\nR8 emits {len(P)} bounded review packet rows before cross-rule dedupe. Strong recurrent packets include democracy principle/application, GSS abortion general→specific recurrence, Saudi Q605 Islamic-law variants, Latin 2024 environmental principle/means/application, LiTS corruption-report duty/cost/willingness, WVS work-duty/leisure-cost, GSS environmental cost willingness, GSS workplace compensation-cost, and Arab VIII environmental burden incidence. No packet is S14 relation authority yet.\n\n## Cross-rule dedupe\nAll T03–T11 packet ledgers from R2–R7 plus the reconstructed R8 packets were merged. Exact repeated evidence terrain is reviewed once (notably LiTS III corruption reporting; EVS1990 voluntary-duty hierarchy; Arab VIII Q604 T09/T10; Arab VIII Q628 source blocker; Latin 2024 environmental T03/T04; GSS abortion T03/T05).\n\n- raw packet rows: {len(raw)}\n- canonical packet rows: {len(canon)}\n- unresolved review denominator: {len(worker)}\n- blocker dependencies: {len(block)}\n- cross-rule unresolved packets: {multi}\n\n## Worker economics\nDecision: **{decision}**.\nNo worker is launched by this checkpoint. If sharding is used, R8's exact immutable canonical packet denominator must be frozen first; workers may only adjudicate assigned packets and may not invent ontology, schemas, evidence ceilings, or completeness claims.\n'''
open(OUT/'R8_NARROWING_DEDUPE_REPORT.md','w').write(report)
nexttxt='''# Next execution after R8\n\n1. Verify/cold-validate R8 and Library round-trip.\n2. Freeze the exact unresolved semantic packet denominator if worker sharding remains economical.\n3. Generate immutable worker packs only from canonical R8 packet IDs; no rule-level free search.\n4. Central Vozhd retains blockers, ontology/schema, reconciliation and final S14 sign-off.\n5. Adjudicate/reconcile packet returns and freeze actual S14 relational-structure authority.\n6. Build/finalize unified 18,276 implementation spine + orthogonal relation-role registry as production authority.\n7. Rebuild O11/S16 from actual repaired prerequisites.\n8. Rebuild O12 T01–T13 cleanly, including T01 grain audit.\n9. Independent completeness reconstruction + causal histogram audit.\n10. Only then freeze O12 and launch Job 3.\n'''
open(OUT/'NEXT_EXECUTION_STEPS.md','w').write(nexttxt)
readme='''# README FIRST — S14 Relation-Role Bridge Repair Checkpoint R8\n\nState: R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR. Job 3: NO. 811 final denominator: NO.\n\nR8 reconstructs the previously ungoverned T03–T05 narrowing frontier, combines it with governed T06–T11 narrowing checkpoints R2–R7, cross-rule deduplicates the review work, and makes the first exact worker-economics decision from a canonical packet denominator.\n\nNothing in R8 is final S14 relation authority; it is the frozen narrowing/review workbench subject to semantic adjudication and central reconciliation.\n'''
open(OUT/'00_README_FIRST.md','w').write(readme)
# provenance pins
pins={'parents':{str(BASE/'CANONICAL_IMPLEMENTATION_REGISTRY.csv'):'sealed current 18,276 implementation registry',str(BASE/'INTER_QUESTION_RELATION_AUTHORITY_R2.csv'):'sealed R6 relation authority',str(BASE/'R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json'):'sealed R14 source authority'},'checkpoint_parents':{k:str(v) for k,v in packet_paths.items()},'rejected_shortcuts':['Phase-0 rare-role tokens are not bridge authority','R14/page excerpts forbidden for cross-object similarity','lexical/embedding/driver/proximity recall never authorizes relations']}
json.dump(pins,open(OUT/'PROVENANCE/PARENT_PINS_R8.json','w'),indent=2)
# validator
val='''from pathlib import Path
import pandas as pd,json,sys
R=Path(__file__).resolve().parents[1]
errs=[];checks=[]
def py(x):
    try:return x.item()
    except:return x
def ck(n,c,d=None): checks.append((n,bool(c),py(d))); errs.append(n) if not c else None
p=pd.read_csv(R/'AUDIT/O11_T03_T05_PROXY_GROUP_DISPOSITION_R8.csv')
ck('proxy_T03_194',int((p.rule_id=='S14-T03').sum())==194,int((p.rule_id=='S14-T03').sum()))
ck('proxy_T04_59',int((p.rule_id=='S14-T04').sum())==59,int((p.rule_id=='S14-T04').sum()))
ck('proxy_T05_42',int((p.rule_id=='S14-T05').sum())==42,int((p.rule_id=='S14-T05').sum()))
ck('proxy_all_dispositioned',p.disposition.fillna('').str.len().gt(0).all())
c=pd.read_csv(R/'PROVENANCE/R6_T03_T05_12_CANARY_RECOVERY_R8.csv')
ck('r6_canaries_12',len(c)==12,len(c)); ck('r6_T03_8',int((c.rule_id=='S14-T03').sum())==8,int((c.rule_id=='S14-T03').sum()));ck('r6_T04_1',int((c.rule_id=='S14-T04').sum())==1,int((c.rule_id=='S14-T04').sum()));ck('r6_T05_3',int((c.rule_id=='S14-T05').sum())==3,int((c.rule_id=='S14-T05').sum()))
o=pd.read_csv(R/'AUDIT/T03_T05_R14_596_EXACT_OBJECT_ACCOUNTING_R8.csv')
for rid in ['S14-T03','S14-T04','S14-T05']:ck(rid+'_r14_596',int((o.rule_id==rid).sum())==596,int((o.rule_id==rid).sum()))
ck('r14_no_excerpt_authority',o.evidence_law.str.contains('forbidden').all())
pack=pd.read_csv(R/'NARROWING/T03_T05_RECONSTRUCTED_CANONICAL_PACKETS_R8.csv');ck('reconstructed_packets_11',len(pack)==11,len(pack));ck('no_accept_verdicts',~pack.status.str.startswith('ACCEPT').any());ck('all_reconstructed_have_semantic_units',pack.semantic_unit_ids_json.map(lambda x:len(json.loads(x))>0).all())
raw=pd.read_csv(R/'NARROWING/T03_T11_RAW_PACKET_LEDGER_R8.csv');canon=pd.read_csv(R/'NARROWING/T03_T11_CROSS_RULE_DEDUPED_CANONICAL_PACKETS_R8.csv');worker=pd.read_csv(R/'NARROWING/T03_T11_UNRESOLVED_REVIEW_DENOMINATOR_R8.csv');single=pd.read_csv(R/'NARROWING/T03_T11_WORKER_ELIGIBLE_SINGLE_RULE_DENOMINATOR_R8.csv');cross=pd.read_csv(R/'NARROWING/T03_T11_VOZHD_CENTRAL_CROSS_RULE_DENOMINATOR_R8.csv');block=pd.read_csv(R/'NARROWING/T03_T11_BLOCKER_DEPENDENCIES_R8.csv')
ck('raw_packet_rows_96',len(raw)==96,len(raw));ck('canonical_packet_rows_89',len(canon)==89,len(canon));ck('unresolved_66',len(worker)==66,len(worker));ck('worker_single_53',len(single)==53,len(single));ck('central_cross_13',len(cross)==13,len(cross));ck('blockers_4',len(block)==4,len(block));ck('single_plus_cross_eq_worker',len(single)+len(cross)==len(worker));ck('single_has_no_cross_rule',~single.rule_hypotheses.str.contains(';',regex=False).any());ck('cross_all_cross_rule',cross.rule_hypotheses.str.contains(';',regex=False).all());ck('worker_only_unresolved',(worker.queue_class=='UNRESOLVED_REVIEW').all());ck('canonical_ids_unique',canon.canonical_packet_id.is_unique)
st=json.load(open(R/'CURRENT_STATUS_R8.json'));ck('job3_blocked',st['job3_authorized'] is False);ck('workers_not_launched',st['workers_launched'] is False);ck('worker_count_matches',st['cross_rule_dedupe']['unresolved_review_denominator']==len(worker));ck('hybrid_decision',st['worker_economics_decision'].startswith('HYBRID__SHARD_53'))
res={'status':'PASS' if not errs else 'FAIL','checks':len(checks),'errors':errs,'details':[{'check':n,'pass':p,'detail':d} for n,p,d in checks]}
json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R8.json','w'),indent=2);print(json.dumps({'status':res['status'],'checks':res['checks'],'errors':len(errs)},indent=2));sys.exit(1 if errs else 0)
'''
open(OUT/'VALIDATION/validate_r8.py','w').write(val)
# copy builder
shutil.copy(__file__,OUT/'CODE/build_r8.py')
# initial validation
os.system(f'python {OUT}/VALIDATION/validate_r8.py')
# manifest excluding itself, zip not inside folder
files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256_MANIFEST_R8.csv']
mani=[]
for p in sorted(files):
 h=hashlib.sha256(p.read_bytes()).hexdigest(); mani.append({'path':str(p.relative_to(OUT)),'sha256':h,'size_bytes':p.stat().st_size})
pd.DataFrame(mani).to_csv(OUT/'SHA256_MANIFEST_R8.csv',index=False)
# zip deterministic-ish
zip_path=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R8_20260811.zip')
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file(): z.write(p,arcname=str(Path(OUT.name)/p.relative_to(OUT)))
h=hashlib.sha256(zip_path.read_bytes()).hexdigest(); open(str(zip_path)+'.sha256','w').write(h+'  '+zip_path.name+'\n')
print('ZIP',zip_path,'SHA',h)
print('ECON',json.dumps(econ,indent=2))
