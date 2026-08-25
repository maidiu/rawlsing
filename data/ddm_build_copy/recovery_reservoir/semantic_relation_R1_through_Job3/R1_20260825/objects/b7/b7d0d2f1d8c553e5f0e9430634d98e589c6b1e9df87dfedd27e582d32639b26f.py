from pathlib import Path
import pandas as pd,json,re,hashlib,itertools,collections
B=Path('/mnt/data');R=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811';P=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R11A_20260811'
def jl(x):
 if pd.isna(x) or x=='':return []
 try:return json.loads(x)
 except:return []
def jj(x):return json.dumps(sorted(set(str(v) for v in x if str(v))))
def hid(prefix,*parts):return prefix+'-'+hashlib.sha256('||'.join(map(str,parts)).encode()).hexdigest()[:16]
sp=pd.read_csv(B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811/SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz',dtype=str,low_memory=False).fillna('')
# exact current lookup
lookup=collections.defaultdict(list)
for r in sp[['source_family','wave','source_variable_code','question_implementation_id','sem__audit_unit_id']].itertuples(index=False):lookup[(r.source_family,str(r.wave),r.source_variable_code.lower())].append((r.question_implementation_id,r.sem__audit_unit_id))
wave_alias={('LiTS','I'):'2006'}
def map_codes(sf,waves,codes):
 ims=set();units=set()
 for w in waves:
  w=wave_alias.get((sf,str(w)),str(w))
  for c in codes:
   for im,u in lookup.get((sf,w,c.lower()),[]):ims.add(im);units.add(u) if u else None
 return ims,units
# packet indexes
PK=pd.read_csv(R/'PACKETS/R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv',dtype=str).fillna('')
pi={r.packet_id:set(jl(r.member_implementation_ids_json)) for r in PK.itertuples(index=False)}
pu={r.packet_id:set(jl(r.member_semantic_unit_ids_json)) for r in PK.itertuples(index=False)}
# prefer actual semantic review packets over global pair blockers when ancestry matching
preferred=set(PK[~PK.packet_class.isin(['PAIR_RULE_INPUT_AUTHORITY_BLOCKER','T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH'])].packet_id)
# source object direct
objpid={o:r.packet_id for r in PK[PK.packet_class=='SOURCE_NATIVE_OBJECT'].itertuples(index=False) for o in jl(r.source_object_ids_json)}
# T07 global authority -> R12 packet
T7=pd.read_csv(P/'T07/R11_T07_P2_TARGET_RELATION_79_ROW_ACCOUNTING.csv',dtype=str).fillna('')
originmap=pd.read_csv(R/'MAPPINGS/R12_SPECIALIZED_ORIGIN_TO_PACKET_MAP.csv.gz',dtype=str).fillna('')
opp_to_packet=originmap.groupby('r11_origin_id').r12_packet_id.apply(lambda s:sorted(set(s))).to_dict()
t7global={r.global_semantic_authority_id:opp_to_packet.get(r.opportunity_id,[]) for r in T7.itertuples(index=False)}
# source-specific origin evidence registries
orig_evidence={}
# T03-05
F=pd.read_csv(B/'r8_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R8_20260811/NARROWING/T03_T05_RECONSTRUCTED_CANONICAL_PACKETS_R8.csv',dtype=str).fillna('')
for r in F.itertuples(index=False):orig_evidence[r.packet_id]={'ims':set(jl(r.implementation_ids_json)),'units':set(jl(r.semantic_unit_ids_json)),'direct_packets':set(),'kind':'T03T05'}
# T06 parse members against all current codes in source/waves by substring tokens
T6=pd.read_csv(B/'r11_inputs/t06_r2/T06_CANONICAL_REVIEW_PACKETS_R2.csv',dtype=str).fillna('')
for r in T6.itertuples(index=False):
 waves=[x.strip() for x in str(r.wave).split(';')]; candidates=sp[sp.source_family.eq(r.source_family)&sp.wave.astype(str).isin([wave_alias.get((r.source_family,w),w) for w in waves])].source_variable_code.drop_duplicates().tolist();m=r.members.lower();codes=[c for c in candidates if re.search(r'(?<![a-z0-9_])'+re.escape(c.lower())+r'(?![a-z0-9_])',m)]
 ims,units=map_codes(r.source_family,waves,codes);orig_evidence[r.packet_id]={'ims':ims,'units':units,'direct_packets':set(),'kind':'T06'}
# T07
R3=pd.read_csv(B/'r3_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R3_20260811/NARROWING/T07_CANONICAL_REVIEW_PACKETS_R3.csv',dtype=str).fillna('')
for r in R3.itertuples(index=False):
 direct=set();ims=set();units=set()
 if r.source_surface=='P2':
  if 'rows in T07_P2_TARGET_RELATION_DISPOSITION_R3.csv' in r.evidence_refs:
   if 'P03-' in r.packet_id:
    rows=T7[T7.t07_narrowing_status.eq('REVIEW_REQUIRED_FUNCTIONAL_SUBTARGET_DIRECTION')]
   elif 'P04-' in r.packet_id:
    rows=T7[T7.t07_narrowing_status.eq('REVIEW_REQUIRED_JURISDICTIONAL_OR_NAMING_SCOPE_DIRECTION')]
   else: rows=T7.iloc[0:0]
   for o in rows.opportunity_id:direct.update(opp_to_packet.get(o,[]))
  else:
   for ref in str(r.evidence_refs).split(';'):direct.update(t7global.get(ref.strip(),[]))
 elif r.source_family not in ['MULTI','']:
  waves=[r.wave];cands=sp[sp.source_family.eq(r.source_family)&sp.wave.astype(str).isin([wave_alias.get((r.source_family,str(r.wave)),str(r.wave))])].source_variable_code.drop_duplicates().tolist();m=r.members.lower();codes=[c for c in cands if re.search(r'(?<![a-z0-9_])'+re.escape(c.lower())+r'(?![a-z0-9_])',m)];ims,units=map_codes(r.source_family,waves,codes)
 # direct source object evidence refs
 for ref in str(r.evidence_refs).split(';'):
  if ref.strip() in objpid:direct.add(objpid[ref.strip()])
 orig_evidence[r.packet_id]={'ims':ims,'units':units,'direct_packets':direct,'kind':'T07'}
# T08 reconstruct XOBJ semantic sets / source objects
R4p=pd.read_csv(B/'r4_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R4_20260811/NARROWING/T08_CANONICAL_REVIEW_PACKETS_R4.csv',dtype=str).fillna('')
R4x=pd.read_csv(B/'r4_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R4_20260811/NARROWING/T08_CROSS_OBJECT_SAME_PREDICATE_RECALL_R4.csv',dtype=str).fillna('')
xpacket={}
xc=R4x[R4x.disposition.eq('EMIT_CROSS_OBJECT_T08_RECALL_HYPEREDGE')]
for key,g in xc.groupby(['source_family','measured_predicate','canonical_role','semantic_unit_ids_json','institution_classes_json'],dropna=False):
 sig='|'.join(map(str,key)); pid='T08R4-XOBJ-'+hashlib.sha256(sig.encode()).hexdigest()[:12];xpacket[pid]=set(jl(key[3]))
for r in R4p.itertuples(index=False):
 direct=set();units=xpacket.get(r.packet_id,set())
 ev=r.evidence_object_ids
 try:evs=json.loads(ev) if ev.startswith('[') else [ev]
 except:evs=[ev]
 for o in evs:
  if o in objpid:direct.add(objpid[o]);units |= set(sp[sp.r14c_object_ids_json.str.contains(re.escape(o),regex=True)].sem__audit_unit_id[lambda s:s!=''])
 orig_evidence[r.packet_id]={'ims':set(),'units':units,'direct_packets':direct,'kind':'T08'}
# T09
R5=pd.read_csv(B/'r5_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R5_20260811/NARROWING/T09_CANONICAL_PACKETS_R5.csv',dtype=str).fillna('')
for r in R5.itertuples(index=False):
 cands=sp[sp.source_family.eq(r.source_family)&sp.wave.astype(str).eq(wave_alias.get((r.source_family,str(r.wave)),str(r.wave)))].source_variable_code.drop_duplicates().tolist();m=r.members.lower();codes=[c for c in cands if re.search(r'(?<![a-z0-9_])'+re.escape(c.lower())+r'(?![a-z0-9_])',m)];ims,units=map_codes(r.source_family,[r.wave],codes);orig_evidence[r.packet_id]={'ims':ims,'units':units,'direct_packets':set(),'kind':'T09'}
# T10
R6=pd.read_csv(B/'r6_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R6_20260811/NARROWING/T10_CANONICAL_PACKETS_R6.csv',dtype=str).fillna('')
for r in R6.itertuples(index=False):
    # T10 member notation mixes JSON arrays, slash/plus lists, and compact numeric ranges (e.g. Q550A_1..6).
    # Recover against the exact current source-code registry rather than treating non-JSON notation as absence.
    codes=jl(r.members)
    m=r.members.lower()
    if not codes:
        w=wave_alias.get((r.source_family,str(r.wave)),str(r.wave))
        candidates=sp[sp.source_family.eq(r.source_family)&sp.wave.astype(str).eq(w)].source_variable_code.drop_duplicates().tolist()
        codes=[c for c in candidates if re.search(r'(?<![a-z0-9_])'+re.escape(c.lower())+r'(?![a-z0-9_])',m)]
        # numeric compact ranges PREFIX_N..M
        for pref,a,b in re.findall(r'([a-z0-9_]+?)(\d+)\.\.(\d+)',m):
            for n in range(int(a),int(b)+1):
                c=pref+str(n)
                for cc in candidates:
                    if cc.lower()==c: codes.append(cc)
    ims,units=map_codes(r.source_family,[r.wave],codes);direct=set()
    # If recovered members sit in corrected R14 objects, bind those packets directly too.
    for im in ims:
        row=sp[sp.question_implementation_id.eq(im)]
        if len(row):
            for o in jl(row.iloc[0].r14c_object_ids_json):
                if o in objpid:direct.add(objpid[o])
    orig_evidence[r.packet_id]={'ims':ims,'units':units,'direct_packets':direct,'kind':'T10'}
# T11
R7=pd.read_csv(B/'r7_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R7_20260811/NARROWING/T11_CANONICAL_REVIEW_PACKETS_R7.csv',dtype=str).fillna('')
for r in R7.itertuples(index=False):
 ims=set();units=set()
 for sw in jl(r.source_family_waves_json):
  if '::' not in sw:continue
  sf,w=sw.rsplit('::',1);a,b=map_codes(sf,[w],jl(r.member_source_variable_codes_json));ims|=a;units|=b
 orig_evidence[r.packet_id]={'ims':ims,'units':units,'direct_packets':set(),'kind':'T11'}
# old canonical
old=pd.read_csv(B/'r8_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R8_20260811/NARROWING/T03_T11_CROSS_RULE_DEDUPED_CANONICAL_PACKETS_R8.csv',dtype=str).fillna('')
rows=[]
for rr in old.itertuples(index=False):
 origins=jl(rr.origin_packet_ids_json);ims=set();units=set();direct=set();kinds=set()
 for o in origins:
  e=orig_evidence.get(o)
  if e:ims|=e['ims'];units|=e['units'];direct|=e['direct_packets'];kinds.add(e['kind'])
 # known-no-new is preserved outside review denominator; no packet required
 if rr.queue_class=='KNOWN_NO_NEW':
  status='PRESERVED_AS_EXISTING_OR_KNOWN_NO_NEW_AUTHORITY__NO_R12_REVIEW_PACKET_REQUIRED'; chosen=sorted(direct)
 else:
  # exact/superset member matches, then semantic unit superset, then overlap
  subs=[];usubs=[];overs=[]
  for pid in preferred:
   s=pi.get(pid,set());u=pu.get(pid,set())
   if ims and ims<=s:subs.append(pid)
   if units and units<=u:usubs.append(pid)
   inter=len(ims&s) if ims else 0;uinter=len(units&u) if units else 0
   if inter or uinter:overs.append((inter+uinter,inter,uinter,pid))
  chosen=sorted(direct | set(subs) | set(usubs))
  if chosen:status='PRESERVED_BY_RECOVERED_ORIGIN_AUTHORITY_AND_R12_PACKET_BINDING'
  elif overs:chosen=[x[3] for x in sorted(overs,reverse=True)[:5]];status='PRESERVED_BY_RECOVERED_ORIGIN_MEMBER_OVERLAP__REVALIDATE'
  else:status='NO_R12_PACKET_MATCH_AFTER_ORIGIN_RECOVERY__INVESTIGATE'
 rows.append({'r8_canonical_packet_id':rr.canonical_packet_id,'r8_queue_class':rr.queue_class,'r8_rule_hypotheses':rr.rule_hypotheses,'origin_packet_ids_json':rr.origin_packet_ids_json,'recovered_origin_kinds_json':jj(kinds),'recovered_implementation_count':len(ims),'recovered_semantic_unit_count':len(units),'r12_candidate_packet_ids_json':jj(chosen),'crosswalk_status':status})
O=pd.DataFrame(rows);O.to_csv(R/'ANCESTRY/R8_89_PACKET_TO_R12_COMPRESSION_CROSSWALK.csv',index=False)
# R8C map
r8c=pd.read_csv(B/'r8c_full/Rawlsing_R10K_S14_R8C_Vozhd_Central_Adjudication_20260811/ADJUDICATION/CENTRAL_13_RULE_VERDICTS_R8C.csv',dtype=str).fillna('');am=O.set_index('r8_canonical_packet_id').r12_candidate_packet_ids_json.to_dict();r8c['r12_candidate_packet_ids_json']=r8c.canonical_packet_id.map(am).fillna('[]');r8c['r12_revalidation_status']='PROVISIONAL_R8C_VERDICT_PRESERVED__REVALIDATE_AGAINST_R12_PACKET';r8c.to_csv(R/'ANCESTRY/R8C_33_RULE_VERDICTS_TO_R12_PACKETS.csv',index=False)
print(O.crosswalk_status.value_counts().to_string());print('unmatched',len(O[O.crosswalk_status.str.startswith('NO_')]));print(O[O.crosswalk_status.str.startswith('NO_')].to_string(index=False,max_colwidth=120))
