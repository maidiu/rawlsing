#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, os, re, shutil, subprocess, sys, zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
import pandas as pd

V12=Path('/mnt/data/rawlsing_v12_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v12_20260731')
BUILD=Path('/mnt/data/rawlsing_v13_build')
V13=BUILD/'Rawlsing_J_Family_Authority_Strategy_Handoff_v13_20260731'
S32=V12/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
S33=V13/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2'
DATE='2026-07-31'
NEXT='P2_GLOBAL_SEMANTIC_NEIGHBORHOOD_FULL_ADJUDICATION_AND_STRATA_DOCTRINE_RUNTIME_REPAIR'

def sid(prefix,*parts,n=24):
    return prefix+'_'+hashlib.sha256(chr(31).join(map(str,parts)).encode()).hexdigest()[:n]

def dump_json(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def readcsv(path): return pd.read_csv(path,dtype=str,keep_default_na=False)

def writecsv(df,path):
    df.to_csv(path,index=False,encoding='utf-8')

def jload(s):
    try:return json.loads(s) if s else []
    except:return []

def clean_text(s):
    s=str(s or '').lower().replace('’',"'").replace('´',"'")
    s=re.sub(r'\([^)]*\)',' ',s)
    s=re.sub(r'[^a-z0-9]+',' ',s)
    return re.sub(r'\s+',' ',s).strip()

def canon_member(text):
    t=clean_text(text)
    for p in ('important in a job ','political action ','political system ','aims of respondent '):
        if t.startswith(p): t=t[len(p):]
    rules=[
      ('aim_second',('second choice','2nd most important')),
      ('aim_first',('first choice','most important')),
      ('pol_strong_leader',('strong leader',)),('pol_experts',('experts making decisions','experts make decisions')),
      ('pol_army',('army ruling','army rule')),('pol_democratic',('democratic political system','democratic')),
      ('act_petition',('signing a petition',)),('act_boycott',('joining in boycotts',)),
      ('act_demonstration',('attending lawful demonstrations','attending lawful peaceful demonstrations')),
      ('act_strike',('joining unofficial strikes',)),('act_occupy',('occupying buildings factories','occupying buildings or factories')),
      ('job_good_pay',('good pay',)),('job_pleasant_people',('pleasant people',)),
      ('job_low_pressure',('not too much pressure',)),('job_security',('good job security','job security')),
      ('job_promotion',('chances for promotion',)),('job_respected',('a respected job','respected job')),
      ('job_good_hours',('good hours',)),('job_initiative',('opportunity to use initiative','use initiative')),
      ('job_society',('useful for society',)),('job_holidays',('generous holidays',)),
      ('job_meeting_people',('meeting people',)),('job_achieving',('that you can achieve something','achieving something')),
      ('job_responsible',('a responsible job','responsible job')),('job_interesting',('a job that is interesting','interesting job')),
      ('job_abilities',('a job that meets one s abilities','meeting abilities')),
      ('job_learning',('learning new skills',)),('job_family',('family friendly',)),('job_say',('have a say',)),
      ('job_equal',('people treated equally',)),('job_none',('none of these',)),('job_dk',('i dont know','i don t know')),
      ('job_no_answer',('no answer',)),('job_physical',('good physical working conditions',)),('job_weekends',('time off in weekends',)),
    ]
    for key,phrases in rules:
        if any(p in t for p in phrases): return key
    return 'raw::'+t

def setup():
    if BUILD.exists(): shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    shutil.copytree(V12,V13)
    S33.mkdir()


def build_exact_target():
    exact=readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_Exact_Foundation_Pair_Rulings_v1.csv')
    ids=[
'p2xsrc_63172a3ab6cfd84a5a8d7f7c','p2xsrc_e4a99a98c95ec3c710ddc32e','p2xsrc_0b0ee7d3e42312369e85897b','p2xsrc_62d60c64ff4f4909bb8e60ba','p2xsrc_c9a7488b5017b9828655b310','p2xsrc_7bce831041d2a35ae24ee41d','p2xsrc_ae3da5503a5ed30aec2e9f13','p2xsrc_c38429af98dbc566512c8997','p2xsrc_2778027e6f13e2eae1e6d0ef','p2xsrc_641e895adb99b880602ab853','p2xsrc_7d6149c487e6f226763e5f10','p2xsrc_869f84fa655d29c5d53b0c92','p2xsrc_f620a233aeca6e27efa4ddf2','p2xsrc_54ccf8f97501b547965b3aea','p2xsrc_1cad8401c5ef71b3f6fdd1ca','p2xsrc_32cfd60489154009bcf74484','p2xsrc_8a2badfde214c7e03ecb889f','p2xsrc_e970c68ed503e048e84ba839']
    decision={
ids[0]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','PROPOSITION_EQUIVALENT_RESPONSE_RECODE_REQUIRED','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Radio-news use is the same frequency proposition; category count and direction require an explicit recode.'),
ids[1]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','PROPOSITION_EQUIVALENT_RESPONSE_RECODE_REQUIRED','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Television-news use is the same frequency proposition; category count and direction require an explicit recode.'),
ids[2]:('REJECTED_CROSS_SOURCE_FALSE_EQUIVALENCE','SHARED_TARGET_DIFFERENT_RELATION_AXIS','TARGET_NEIGHBORHOOD_ONLY','Arab Barometer asks extent of air-pollution impact; LiTS encodes a binary air-pollution construct. Shared target does not establish a shared proposition.'),
ids[3]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Both are trust/confidence in regional government within institutional-trust batteries; labels and response families support the same relation axis.'),
ids[4]:('REJECTED_CROSS_SOURCE_FALSE_EQUIVALENCE','SHARED_TARGET_DIFFERENT_RELATION_AXIS','TARGET_NEIGHBORHOOD_ONLY','Arab Barometer evaluates government effectiveness; WVS asks confidence/trust in government.'),
ids[5]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Political parties are trust-battery children on both sides.'),
ids[6]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Local government is a trust-battery child on both sides.'),
ids[7]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Police is a trust-battery child on both sides.'),
ids[8]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Television is a media-confidence/trust battery child on both sides.'),
ids[9]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Parliament is an institutional trust/confidence battery child on both sides.'),
ids[10]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Police is an institutional trust/confidence battery child on both sides.'),
ids[11]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Political parties are an institutional trust/confidence battery child on both sides.'),
ids[12]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Courts are an institutional trust/confidence battery child on both sides.'),
ids[13]:('REJECTED_CROSS_SOURCE_FALSE_EQUIVALENCE','SHARED_TARGET_DIFFERENT_RELATION_AXIS','TARGET_NEIGHBORHOOD_ONLY','GSS asks whether government spending on social security is too little/about right/too much; LiTS encodes social-security receipt or status.'),
ids[14]:('REJECTED_CROSS_SOURCE_FALSE_EQUIVALENCE','SHARED_TARGET_DIFFERENT_RELATION_AXIS','TARGET_NEIGHBORHOOD_ONLY','LiTS political-party affiliation is not WVS active/inactive organizational membership.'),
ids[15]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Police is a trust/confidence battery child on both sides.'),
ids[16]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Abortion is a justifiability battery child on both sides; source-specific value dictionaries remain versioned.'),
ids[17]:('ACCEPTED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','Political parties are a trust/confidence battery child on both sides.')}
    rows=[]
    for i,cid in enumerate(ids,1):
        r=exact.loc[exact.cross_source_candidate_id.eq(cid)].iloc[0].to_dict()
        st,rel,ceil,rat=decision[cid]
        rows.append({
          'target_relation_axis_ruling_id':sid('p2axis',cid),'cross_source_candidate_id':cid,'sequence':i,
          'left_source_family':r['left_source_family'],'right_source_family':r['right_source_family'],
          'left_lineage_id':r['left_lineage_id'],'right_lineage_id':r['right_lineage_id'],
          'left_texts_json':r['left_texts_json'],'right_texts_json':r['right_texts_json'],
          'source_parent_evidence_status':'RECOVERED_FROM_DEEP_NODE_AND_SOURCE_STRUCTURE_RECORDS',
          'relation_type':rel,'authority_status':st,'portability_ceiling':ceil,'adjudication_confidence':'HIGH',
          'two_sided_evidence_status':'COMPLETE_DEEP_REVIEWED_SOURCE_RECORDS_BOTH_SIDES',
          'rationale':rat,'prohibited_use':'No raw-value portability, J-family membership, respondent join, registry installation, or runtime authority.'})
        idx=exact.index[exact.cross_source_candidate_id.eq(cid)][0]
        exact.loc[idx,'adjudication_rule_class']='SOURCE_PARENT_AND_RELATION_AXIS_ADJUDICATED'
        exact.loc[idx,'relation_type']=rel
        exact.loc[idx,'authority_status']=st
        exact.loc[idx,'portability_ceiling']=ceil if st.startswith('ACCEPTED') else 'NONE'
        exact.loc[idx,'adjudication_confidence']='HIGH'
        exact.loc[idx,'two_sided_evidence_status']='COMPLETE_DEEP_REVIEWED_SOURCE_RECORDS_BOTH_SIDES'
        exact.loc[idx,'rationale']=rat
    axis=pd.DataFrame(rows)
    writecsv(axis,S33/'Rawlsing_P2_Exact_Target_Relation_Axis_Rulings_v1.csv')
    writecsv(exact,S33/'Rawlsing_P2_Exact_Foundation_Pair_Rulings_v2.csv')
    return exact,axis


def parse_high_precision_ids():
    out=[]
    for line in Path('/mnt/data/high_precision_121.txt').read_text(encoding='utf-8').splitlines():
        m=re.match(r'^(\d{3})\t([^\t]+)',line)
        if m: out.append((int(m.group(1)),m.group(2)))
    assert len(out)==121 and [n for n,_ in out]==list(range(1,122))
    return out


def build_semantic_rulings():
    q=readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_Semantic_Neighborhood_Pair_Queue_v1.csv')
    lineages=readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv').set_index('lineage_id')
    ids=parse_high_precision_ids()
    codes={1:'A',2:'A',3:'A',4:'A',5:'R',6:'A',7:'C',8:'C',9:'A',10:'A',11:'A',12:'A',13:'M',14:'A',15:'A',16:'A',17:'A',18:'P',19:'A',20:'A',21:'A',22:'A',23:'A',24:'A',25:'A',26:'A',27:'R',28:'N',29:'A',30:'A',31:'R',32:'R',33:'A',34:'C',35:'A',36:'P',37:'C',38:'A',39:'A',40:'C',41:'N',42:'C',43:'C',44:'R',45:'R',46:'A',47:'A',48:'A',49:'R',50:'R',51:'A',52:'A',53:'R',54:'A',55:'R',56:'A',57:'R',58:'R',59:'A',60:'A',61:'A',62:'N',63:'A',64:'A',65:'A',66:'U',67:'A',68:'A',69:'A',70:'A',71:'A',72:'A',73:'A',74:'A',75:'A',76:'A',77:'U',78:'U',79:'U',80:'U',81:'A',82:'A',83:'A',84:'A',85:'U',86:'A',87:'A',88:'A',89:'A',90:'R',91:'P',92:'R',93:'A',94:'A',95:'R',96:'R',97:'A',98:'A',99:'A',100:'A',101:'A',102:'A',103:'A',104:'R',105:'A',106:'A',107:'A',108:'A',109:'A',110:'A',111:'A',112:'A',113:'A',114:'A',115:'A',116:'A',117:'P',118:'A',119:'R',120:'A',121:'A'}
    rationale_override={
      2:'Both ask satisfaction with the current ruling government; the inherited economic semantic ID is wrong and supplies no authority.',
      5:'One item says non-democratic regimes; the other says democratic regimes. The shared predicate does not overcome the opposed target.',
      11:'Both ask difficulty obtaining public medical treatment; the inherited courts semantic ID is wrong.',
      17:'Both ask difficulty obtaining a place in public primary school; the inherited police semantic ID is wrong.',
      27:'Relaxation during leisure is not the importance of leisure in life.',28:'Police and police station share a trust relation but the latter is an institutionally narrower target.',
      31:'Trust in a main Shia party is not trust in national government.',32:'Trust in a main Sunni party is not trust in national government.',
      41:'Opposition political parties are a target subset of political parties; the broader and narrower targets are not equivalent.',
      44:'Trust in relatives is not trust in television.',45:'Trust in relatives is not trust in newspapers.',49:'Computer use and internet use are related access/use coordinates, not the same behavior.',
      50:'Access to police help is not access to school admission.',53:'Trust in a Sunni party is not trust in local government.',55:'Trust in a Shia party is not trust in local government.',57:'School admission access is not police-help access.',58:'Trust in relatives is not trust in internet news.',
      62:'Police and police station share a trust relation but the latter is an institutionally narrower target.',
      66:'The EVS label omits the polarity operator; WVS explicitly says religious leaders should not influence government. Parent wording or category semantics are required.',
      74:'Both items concern same-sex couples’ right to marry; the inherited climate-governance semantic ID is wrong.',
      77:'The Asian and South Asia labels are generic parent prompts; answer statements are absent from the governing record.',78:'The Asian and South Asia labels are generic parent prompts; answer statements are absent from the governing record.',79:'The Asian and South Asia labels are generic parent prompts; answer statements are absent from the governing record.',80:'The Asian and South Asia labels are generic parent prompts; answer statements are absent from the governing record.',
      85:'Both labels are generic “comes closest” parent prompts; the underlying statements are absent.',90:'Asian accountability prompt and South Asia generic statement-choice shell do not establish the same child proposition.',
      92:'EVS respondent attendance is not GSS mother’s attendance.',95:'EVS respondent attendance is not GSS father’s attendance.',96:'Democratic-system evaluation is not strong-leader evaluation.',
      104:'Marital happiness is a domain-specific outcome, not general happiness.',119:'Satisfaction with family life is not the importance of family in life.'}
    type_map={
      'A':('ACCEPTED_REWORDED_CROSS_SOURCE_CONTINUITY','FUNCTIONALLY_COMPARABLE','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY'),
      'P':('ACCEPTED_CROSS_SOURCE_PROPOSITION_ONLY','PROPOSITION_EQUIVALENT_RESPONSE_CONTRACT_NOT_PORTABLE','QUESTION_PROPOSITION_ONLY'),
      'C':('ACCEPTED_CROSS_SOURCE_CONSTRUCT_COORDINATE_ONLY','CONSTRUCT_COORDINATE_COMPARABLE','CONSTRUCT_OR_CONTEXT_COORDINATE_ONLY'),
      'M':('ACCEPTED_CROSS_SOURCE_METADATA_FUNCTION_ONLY','METADATA_FUNCTION_COMPARABLE','CONTEXT_OR_POSITION_COORDINATE_ONLY'),
      'N':('ACCEPTED_CROSS_SOURCE_NESTED_TARGET_RELATION','NESTED_TARGET_RELATION_NOT_EQUIVALENT','TARGET_RELATION_AXIS_ONLY_NO_VALUE_PORTABILITY'),
      'R':('REJECTED_CROSS_SOURCE_FALSE_EQUIVALENCE','NEGATIVE_AUTHORITY_FALSE_FRIEND','NONE'),
      'U':('UNRESOLVED_REQUIRES_PARENT_OR_POLARITY_EVIDENCE','UNRESOLVED','NONE')}
    rows=[]
    selected=set()
    exact_ids=set(readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_Exact_Foundation_Pair_Rulings_v1.csv').cross_source_candidate_id)
    for n,cid in ids:
        r=q.loc[q.semantic_pair_candidate_id.eq(cid)].iloc[0].to_dict(); selected.add(cid)
        code=codes[n]; st,rel,ceil=type_map[code]
        L=lineages.loc[r['left_lineage_id']]; R=lineages.loc[r['right_lineage_id']]
        known_conflict={2,11,15,17,31,32,50,57,68,74,91,119}
        inherited_conflict='true' if n in known_conflict or r['semantic_content_id'] not in set(jload(L['semantic_content_ids_json'])) or r['semantic_content_id'] not in set(jload(R['semantic_content_ids_json'])) else 'false'
        rat=rationale_override.get(n)
        if rat is None:
            if code=='A': rat='Two-sided exact item text establishes the same respondent-facing proposition; source-specific values, routing and population remain versioned.'
            elif code=='P': rat='The respondent-facing proposition is shared, but response categories or anchors differ enough to block response-contract portability.'
            elif code=='C': rat='The records share a derived or contextual construct coordinate; category/value equivalence is not authorized.'
            elif code=='M': rat='The fields perform the same administrative identity function; no substantive semantic family is implied.'
            elif code=='N': rat='The relation axis is shared but one target is narrower; this authorizes a typed nesting relation, not equivalence.'
            elif code=='R': rat='Two-sided evidence shows a target, referent, actor, relation-axis, scope or function conflict despite lexical or inherited-semantic proximity.'
            else: rat='The governing labels omit the parent statement, polarity operator or answer alternatives needed to determine the proposition.'
        rows.append({
          'reworded_pair_ruling_id':sid('p2rew',cid),'sequence':n,'semantic_pair_candidate_id':cid,'semantic_content_id_discovery_only':r['semantic_content_id'],
          'left_source_family':r['left_source_family'],'right_source_family':r['right_source_family'],'left_lineage_id':r['left_lineage_id'],'right_lineage_id':r['right_lineage_id'],
          'left_representative_text':r['left_representative_text'],'right_representative_text':r['right_representative_text'],
          'left_response_topologies_json':L['response_topologies_json'],'right_response_topologies_json':R['response_topologies_json'],
          'left_response_signatures_json':L['response_signatures_json'],'right_response_signatures_json':R['response_signatures_json'],
          'inherited_semantic_coordinate_conflict_detected':inherited_conflict,'adjudication_code':code,
          'relation_type':rel,'authority_status':st,'portability_ceiling':ceil,
          'adjudication_confidence':'HIGH' if code!='U' else 'MEDIUM',
          'two_sided_evidence_status':'COMPLETE_DEEP_REVIEWED_SOURCE_RECORDS_BOTH_SIDES' if code!='U' else 'EXACT_ITEMS_PRESENT_BUT_PARENT_OR_POLARITY_EVIDENCE_MISSING',
          'rationale':rat,'prohibited_use':'No J-family membership, raw-value portability, respondent join, registry installation, or runtime authority.'})
    out=pd.DataFrame(rows)
    writecsv(out,S33/'Rawlsing_P2_Reworded_Translation_High_Precision_Pair_Rulings_v1.csv')
    q2=q.copy(); q2['tranche2_review_status']='PENDING';q2['tranche2_authority_status']='PROVISIONAL_DISCOVERY_PAIR_NOT_ADJUDICATED';q2['tranche2_relation_type']='';q2['tranche2_portability_ceiling']='';q2['tranche2_ruling_id']=''
    byid=out.set_index('semantic_pair_candidate_id')
    for idx,row in q2[q2.semantic_pair_candidate_id.isin(selected)].iterrows():
        z=byid.loc[row.semantic_pair_candidate_id]
        q2.loc[idx,['tranche2_review_status','tranche2_authority_status','tranche2_relation_type','tranche2_portability_ceiling','tranche2_ruling_id']]=['ADJUDICATED',z.authority_status,z.relation_type,z.portability_ceiling,z.reworded_pair_ruling_id]
    writecsv(q2,S33/'Rawlsing_P2_Semantic_Priority_Queue_Status_v2.csv')
    remaining=q2[q2.tranche2_review_status.eq('PENDING')].copy()
    writecsv(remaining,S33/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_v2.csv')
    return out,q2


def build_structures():
    q=readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_Provisional_Structure_Analogy_Queue_v1.csv')
    mem=readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv')
    nodes=readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_All_Nine_Unified_Node_Evidence_Registry_v1.csv').set_index('question_implementation_id')
    rulings=[]; corr=[]
    for _,cand in q.iterrows():
        cid=cand.structure_analogy_candidate_id
        L=mem[mem.source_structure_id.eq(cand.left_source_structure_id)].sort_values('member_order',key=lambda x:x.astype(int))
        R=mem[mem.source_structure_id.eq(cand.right_source_structure_id)].sort_values('member_order',key=lambda x:x.astype(int))
        ld=defaultdict(list);rd=defaultdict(list)
        for _,m in L.iterrows(): ld[canon_member(nodes.loc[m.question_implementation_id,'exact_question_text'])].append(m)
        for _,m in R.iterrows(): rd[canon_member(nodes.loc[m.question_implementation_id,'exact_question_text'])].append(m)
        mapped=0
        for key in sorted(set(ld)&set(rd)):
            for lm,rm in zip(ld[key],rd[key]):
                mapped+=1
                corr.append({'member_correspondence_ruling_id':sid('p2smem',cid,lm.question_implementation_id,rm.question_implementation_id),
                  'structure_analogy_candidate_id':cid,'member_relation':'EQUIVALENT_MEMBER_PROPOSITION','canonical_member_key':key,
                  'left_source_structure_id':cand.left_source_structure_id,'right_source_structure_id':cand.right_source_structure_id,
                  'left_question_implementation_id':lm.question_implementation_id,'right_question_implementation_id':rm.question_implementation_id,
                  'left_lineage_id':lm.lineage_id,'right_lineage_id':rm.lineage_id,
                  'left_variable':lm.source_variable_code,'right_variable':rm.source_variable_code,
                  'left_text':nodes.loc[lm.question_implementation_id,'exact_question_text'],'right_text':nodes.loc[rm.question_implementation_id,'exact_question_text'],
                  'authority_status':'ACCEPTED_MEMBER_LEVEL_CORRESPONDENCE','portability_ceiling':'QUESTION_PROPOSITION_ONLY','rationale':'Member-level text recovers the same battery child; response dictionaries and routing remain source-versioned.'})
        matched_l={r['left_question_implementation_id'] for r in corr if r['structure_analogy_candidate_id']==cid}
        matched_r={r['right_question_implementation_id'] for r in corr if r['structure_analogy_candidate_id']==cid}
        for _,m in L.iterrows():
            if m.question_implementation_id not in matched_l:
                corr.append({'member_correspondence_ruling_id':sid('p2smem',cid,m.question_implementation_id,'LEFT_EXTENSION'),
                  'structure_analogy_candidate_id':cid,'member_relation':'LEFT_SOURCE_LOCAL_EXTENSION','canonical_member_key':canon_member(nodes.loc[m.question_implementation_id,'exact_question_text']),
                  'left_source_structure_id':cand.left_source_structure_id,'right_source_structure_id':cand.right_source_structure_id,
                  'left_question_implementation_id':m.question_implementation_id,'right_question_implementation_id':'','left_lineage_id':m.lineage_id,'right_lineage_id':'',
                  'left_variable':m.source_variable_code,'right_variable':'','left_text':nodes.loc[m.question_implementation_id,'exact_question_text'],'right_text':'',
                  'authority_status':'NEGATIVE_OR_BOUNDARY_AUTHORITY_SOURCE_LOCAL_EXTENSION','portability_ceiling':'NONE','rationale':'This battery member has no proposition-level counterpart in the compared structure.'})
        for _,m in R.iterrows():
            if m.question_implementation_id not in matched_r:
                corr.append({'member_correspondence_ruling_id':sid('p2smem',cid,'RIGHT_EXTENSION',m.question_implementation_id),
                  'structure_analogy_candidate_id':cid,'member_relation':'RIGHT_SOURCE_LOCAL_EXTENSION','canonical_member_key':canon_member(nodes.loc[m.question_implementation_id,'exact_question_text']),
                  'left_source_structure_id':cand.left_source_structure_id,'right_source_structure_id':cand.right_source_structure_id,
                  'left_question_implementation_id':'','right_question_implementation_id':m.question_implementation_id,'left_lineage_id':'','right_lineage_id':m.lineage_id,
                  'left_variable':'','right_variable':m.source_variable_code,'left_text':'','right_text':nodes.loc[m.question_implementation_id,'exact_question_text'],
                  'authority_status':'NEGATIVE_OR_BOUNDARY_AUTHORITY_SOURCE_LOCAL_EXTENSION','portability_ceiling':'NONE','rationale':'This battery member has no proposition-level counterpart in the compared structure.'})
        lc,rc=len(L),len(R)
        if mapped==0:
            st='REJECTED_SHARED_LABEL_WITHOUT_MEMBER_EQUIVALENCE';rel='NON_ANALOGOUS_STRUCTURES';ceil='NONE';rat='The normalized structure label recurs, but member-level evidence has zero proposition overlap.'
        elif mapped==lc==rc:
            st='ACCEPTED_FULL_MEMBER_LEVEL_STRUCTURE_ANALOGY';rel='FULL_MEMBER_LEVEL_ANALOGY';ceil='STRUCTURE_MEMBERSHIP_PATTERN_ONLY';rat='Every member has an explicit proposition-level counterpart. Source-specific response and routing contracts remain separate.'
        else:
            st='ACCEPTED_PARTIAL_MEMBER_LEVEL_STRUCTURE_ANALOGY';rel='PARTIAL_MEMBER_LEVEL_ANALOGY_WITH_SOURCE_EXTENSIONS';ceil='MATCHED_MEMBER_SUBSET_ONLY';rat='A verified member subset corresponds; unmatched members remain explicit source-local extensions.'
        rulings.append({'structure_analogy_ruling_id':sid('p2srule',cid),'structure_analogy_candidate_id':cid,
          'left_source_family':cand.left_source_family,'right_source_family':cand.right_source_family,
          'left_source_structure_id':cand.left_source_structure_id,'right_source_structure_id':cand.right_source_structure_id,
          'left_structure_label':cand.left_structure_label,'right_structure_label':cand.right_structure_label,
          'left_member_count':lc,'right_member_count':rc,'matched_member_count':mapped,'left_unmatched_count':lc-mapped,'right_unmatched_count':rc-mapped,
          'member_correspondence_coverage_left':f'{mapped/lc:.6f}','member_correspondence_coverage_right':f'{mapped/rc:.6f}',
          'relation_type':rel,'authority_status':st,'portability_ceiling':ceil,'adjudication_confidence':'HIGH',
          'two_sided_evidence_status':'COMPLETE_EXACT_MEMBER_RECORDS_BOTH_SIDES','rationale':rat,
          'prohibited_use':'No J-family identity, collision hyperedge, respondent composition, or raw-value portability.'})
    rul=pd.DataFrame(rulings); co=pd.DataFrame(corr)
    writecsv(rul,S33/'Rawlsing_P2_Structure_Analogy_Rulings_v1.csv')
    writecsv(co,S33/'Rawlsing_P2_Structure_Member_Correspondence_Rulings_v1.csv')
    return rul,co


def build_anomaly_overlay():
    a=readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_Semantic_Reference_Anomaly_Queue_v1.csv')
    fixed={
      ('Asian Barometer','W1','relig1'):'P2REF::DEMOGRAPHIC_RELIGIOUS_IDENTITY',('Asian Barometer','W1','se006'):'P2REF::DEMOGRAPHIC_RELIGIOUS_IDENTITY',('Asian Barometer','W1','se014'):'P2REF::DEMOGRAPHIC_LANGUAGE',
      ('Afrobarometer','R1','casenumb'):'P2REF::ADMIN_RESPONDENT_NUMBER',('Afrobarometer','R1','party'):'P2REF::POLITICAL_PARTY_AFFILIATION',('Afrobarometer','R1','xstronld'):'P2REF::DEMOCRACY_VS_STRONG_LEADER_PREFERENCE',
      ('Latinobarómetro','1995','enc'):'P2REF::ADMIN_INTERVIEW_NUMBER',('Latinobarómetro','1995','numero'):'P2REF::ADMIN_RESEARCH_YEAR',('Latinobarómetro','1995','p33b'):'P2REF::POLITICAL_PARTY_SUMMARY_SOURCE_LOCAL_PARENT_UNRESOLVED',('Latinobarómetro','1995','p43a'):'P2REF::EU_MEDIA_AWARENESS',('Latinobarómetro','1995','p45'):'P2REF::FOREIGN_ECONOMIC_AID_SOURCE',
      ('Latinobarómetro','1995','p46a'):'P2REF::EU_COUNTRY_KNOWLEDGE_GERMANY',('Latinobarómetro','1995','p46b'):'P2REF::EU_COUNTRY_KNOWLEDGE_SPAIN',('Latinobarómetro','1995','p46c'):'P2REF::EU_COUNTRY_KNOWLEDGE_FRANCE',('Latinobarómetro','1995','p46d'):'P2REF::EU_COUNTRY_KNOWLEDGE_ENGLAND',('Latinobarómetro','1995','p46e'):'P2REF::EU_COUNTRY_KNOWLEDGE_ITALY',('Latinobarómetro','1995','p46f'):'P2REF::EU_COUNTRY_KNOWLEDGE_PORTUGAL',('Latinobarómetro','1995','p46g'):'P2REF::EU_COUNTRY_KNOWLEDGE_OTHER_EU',('Latinobarómetro','1995','p46h'):'P2REF::EU_COUNTRY_KNOWLEDGE_OTHER_OR_INCORRECT',
      ('Latinobarómetro','1995','p47a'):'P2REF::GEOPOLITICAL_ACTOR_OPINION_EUROPE',('Latinobarómetro','1995','p47b'):'P2REF::GEOPOLITICAL_ACTOR_OPINION_UNITED_STATES',('Latinobarómetro','1995','p47c'):'P2REF::GEOPOLITICAL_ACTOR_OPINION_JAPAN',('Latinobarómetro','1995','pais'):'P2REF::ADMIN_COUNTRY',('Latinobarómetro','1995','region'):'P2REF::ADMIN_REGION',('Latinobarómetro','1995','wt'):'P2REF::ADMIN_WEIGHT',
      ('Latinobarómetro','2024','Q45ST'):'P2REF::SOCIAL_MEDIA_POLITICS_EFFECT',('Latinobarómetro','2024','Q47STC'):'P2REF::PRINT_MEDIA_FAKE_NEWS_PREVALENCE',('Latinobarómetro','2024','Q8NCVA'):'P2REF::ENVIRONMENTAL_COLLECTIVE_EFFICACY',('Latinobarómetro','2024','Q8NCVB'):'P2REF::ENVIRONMENTAL_PERSUASIVE_EFFICACY',('Latinobarómetro','2024','Q8NCVC'):'P2REF::ENVIRONMENTAL_PERSONAL_CLIMATE_EFFICACY'}
    rows=[]
    for _,r in a.iterrows():
        key=(r.source_family,r.wave,r.source_variable_code); cid=fixed[key]
        parent_unresolved=r.source_variable_code=='p33b'
        rows.append({
          'semantic_reference_resolution_id':sid('p2semfix',r.anomaly_id),'anomaly_id':r.anomaly_id,'source_family':r.source_family,'wave':r.wave,'source_variable_code':r.source_variable_code,'question_implementation_id':r.question_implementation_id,'exact_question_text':r.exact_question_text,
          'inherited_semantic_content_id':r.inherited_semantic_content_id,'corrected_semantic_content_id':cid,
          'resolution_type':'REPLACE_CONTRADICTORY_INHERITED_MAPPING' if r.anomaly_type.startswith('INHERITED') else 'ADD_SOURCE_LOCAL_SEMANTIC_REFERENCE',
          'parent_proposition_status':'UNRESOLVED_SOURCE_PARENT' if parent_unresolved else 'SUFFICIENT_AT_ASSIGNED_GRAIN',
          'driver_strata_inheritance_permission':'PROHIBITED_FROM_REPLACED_OR_MISSING_MAPPING',
          'authority_status':'RESOLVED_SOURCE_LOCAL_COORDINATE_PARENT_UNRESOLVED' if parent_unresolved else 'RESOLVED_SEMANTIC_REFERENCE_OVERLAY',
          'rationale':'The corrected coordinate is derived from the exact source item. It supplies no automatic cross-source equivalence, driver, strata or horizon assignment.',
          'prohibited_use':'Do not rewrite the historical inherited master in place; do not propagate its prior driver/strata fields.'})
    out=pd.DataFrame(rows)
    writecsv(out,S33/'Rawlsing_P2_Semantic_Reference_Anomaly_Resolution_v1.csv')
    overlay=out[['question_implementation_id','source_family','wave','source_variable_code','inherited_semantic_content_id','corrected_semantic_content_id','resolution_type','driver_strata_inheritance_permission','authority_status']].copy()
    writecsv(overlay,S33/'Rawlsing_P2_Semantic_Reference_Correction_Overlay_v1.csv')
    return out,overlay


def build_bridge_v2(overlay):
    nodes=readcsv(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_All_Nine_Unified_Node_Evidence_Registry_v1.csv')
    ov=overlay.set_index('question_implementation_id').to_dict('index')
    rows=[]
    for lid,g in nodes.groupby('lineage_id',sort=True):
        sem=[];prim=[];sec=[];corr=[];quar=[]
        for _,r in g.iterrows():
            if r.question_implementation_id in ov:
                z=ov[r.question_implementation_id]; sem.append(z['corrected_semantic_content_id']);corr.append(z['authority_status'])
                if z['inherited_semantic_content_id']: quar.append(z['inherited_semantic_content_id'])
            else:
                if r.semantic_content_id: sem.append(r.semantic_content_id)
                if r.semantic_primary_driver: prim.append(r.semantic_primary_driver)
                if r.semantic_secondary_driver: sec.append(r.semantic_secondary_driver)
        def jj(vals):return json.dumps(sorted(set(v for v in vals if v)),ensure_ascii=False)
        rows.append({'lineage_id':lid,'source_family':g.source_family.iloc[0],'member_count':len(g),
          'semantic_content_ids_json':jj(sem),'semantic_primary_drivers_json':jj(prim),'semantic_secondary_drivers_json':jj(sec),
          'position_conditioning_json':jj(g.position_conditioning),'position_modifiers_json':jj(g.position_modifiers),
          'conditional_strata_weights_json':jj(g.conditional_strata_weights),'horizon_affordance_json':jj(g.horizon_affordance),
          'semantic_reference_correction_statuses_json':jj(corr),'quarantined_inherited_semantic_ids_json':jj(quar),
          'bridge_authority_status':'CORRECTION_OVERLAY_APPLIED_NO_NEW_DRIVER_STRATA_AUTHORITY' if corr else 'INHERITED_DIAGNOSTIC_COORDINATES_REQUIRE_GLOBAL_P2_ADJUDICATION',
          'prohibited_use':'No direct driver, strata, horizon, or J-family installation authority.'})
    out=pd.DataFrame(rows)
    writecsv(out,S33/'Rawlsing_P2_Semantic_Driver_Strata_Bridge_v2.csv')
    return out


def build_sidecar_contract():
    ledger=json.load(open(S33.parent/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'SOURCE_nine_strata_field_lineage_ledger.json'))
    dropped=[r['field_family'] for r in ledger['field_families'] if r['lineage_status']=='present_upstream_dropped_at_v552j']
    core=['stratum_id','stratum_label','strata_relevance','strata_path','conditional_strata_weights','horizon_affordance','horizon_type','horizon_scope','horizon_openness','horizon_reach','horizon_valence','horizon_sustaining_power']
    contract={
      'contract_id':'RAWLSING_V552_TO_V552J_STRATA_HORIZON_SIDECAR_V1','version':'1.0.0','date':DATE,
      'status':'AUTHORED_AND_SYNTHETICALLY_TESTED_NOT_INSTALLED_OR_RUNTIME_EXECUTED',
      'purpose':'Preserve authoritative V552 question_semantic_hierarchy strata/horizon fields into V552J without inferring missing values.',
      'source_artifact':'v552_question_semantic_hierarchy','target_artifacts':['v552j_v553_input_index','v552j_to_v553_handoff_index'],
      'join_key_preference':[
        ['question_implementation_id'],['source','wave','question_id'],['source','wave','source_variable_code']
      ],
      'required_cardinality':'many packet rows to at most one sidecar row per selected key; duplicate sidecar keys fail closed',
      'authoritative_passthrough_fields':core,
      'additional_dropped_fields_requiring_live-repo_review':[x for x in dropped if x not in core],
      'missing_value_policy':'preserve missing; never synthesize labels, weights or horizon classifications',
      'conflict_policy':'fail closed when packet and sidecar both contain different non-empty values',
      'runtime_installation_status':'NOT_INSTALLED',
      'known_evidence':'998 non-null upstream rows across GSS 1972, 1993 and 2002 according to the recovered lineage ledger.'}
    dump_json(S33/'Rawlsing_V552_to_V552J_Strata_Horizon_Sidecar_Contract_v1.json',contract)
    req=[]
    for f in core:
        req.append({'requirement_id':sid('stratareq',f),'field_family':f,'required_source':'V552 question_semantic_hierarchy','required_target':'V552J input and handoff sidecar','authority_rule':'PASS_THROUGH_ONLY','missing_policy':'PRESERVE_MISSING','conflict_policy':'FAIL_CLOSED','runtime_status':'CONTRACT_ONLY_NOT_INSTALLED'})
    writecsv(pd.DataFrame(req),S33/'Rawlsing_P2_Nine_Strata_Doctrine_Requirements_v1.csv')
    adapter='''#!/usr/bin/env python3\n"""Read-only V552→V552J strata/horizon sidecar adapter proposal.\n\nThis module is not installed into the live pipeline. It performs cardinality-checked\npass-through only and refuses to synthesize missing strata or horizon values.\n"""\nfrom __future__ import annotations\nimport pandas as pd\nFIELDS = %r\nKEY_PREFERENCES = [("question_implementation_id",),("source","wave","question_id"),("source","wave","source_variable_code")]\n\ndef _clean(v):\n    if pd.isna(v): return ""\n    return str(v).strip()\n\ndef select_join_key(packet: pd.DataFrame, sidecar: pd.DataFrame):\n    for keys in KEY_PREFERENCES:\n        if all(k in packet.columns and k in sidecar.columns for k in keys):\n            if all(packet[k].map(_clean).ne("").any() and sidecar[k].map(_clean).ne("").any() for k in keys):\n                return list(keys)\n    raise ValueError("no supported join key present on both packet and sidecar")\n\ndef enrich(packet: pd.DataFrame, sidecar: pd.DataFrame) -> pd.DataFrame:\n    keys=select_join_key(packet,sidecar)\n    s=sidecar.copy()\n    dup=s.duplicated(keys,keep=False)\n    if dup.any():\n        raise ValueError("duplicate sidecar join keys: "+repr(s.loc[dup,keys].to_dict("records")[:10]))\n    keep=keys+[f for f in FIELDS if f in s.columns]\n    out=packet.merge(s[keep],how="left",on=keys,suffixes=("","__sidecar"),validate="many_to_one")\n    for f in FIELDS:\n        sf=f+"__sidecar"\n        if sf not in out.columns: continue\n        if f not in packet.columns:\n            out[f]=out[sf]\n        else:\n            left=out[f].map(_clean); right=out[sf].map(_clean)\n            conflict=left.ne("") & right.ne("") & left.ne(right)\n            if conflict.any(): raise ValueError(f"conflicting non-empty values for {f}")\n            out[f]=out[f].where(left.ne(""),out[sf])\n        out.drop(columns=[sf],inplace=True)\n    out["strata_horizon_sidecar_status"]="V552_AUTHORITATIVE_PASS_THROUGH"\n    return out\n''' % core
    (S33/'v552j_strata_horizon_sidecar_adapter.py').write_text(adapter,encoding='utf-8')
    test='''#!/usr/bin/env python3\nimport pandas as pd\nfrom v552j_strata_horizon_sidecar_adapter import enrich\n\np=pd.DataFrame([{\"question_implementation_id\":\"q1\",\"packet_id\":\"p1\"},{\"question_implementation_id\":\"q2\",\"packet_id\":\"p2\"}])\ns=pd.DataFrame([{\"question_implementation_id\":\"q1\",\"stratum_id\":\"s1\",\"horizon_type\":\"bounded\"}])\no=enrich(p,s)\nassert len(o)==2 and o.loc[0,\"stratum_id\"]==\"s1\" and pd.isna(o.loc[1,\"stratum_id\"])\ntry:\n    enrich(p,pd.concat([s,s],ignore_index=True))\nexcept ValueError as e:\n    assert \"duplicate\" in str(e)\nelse:\n    raise AssertionError(\"duplicate sidecar keys did not fail\")\np2=p.copy();p2[\"stratum_id\"]=[\"conflict\",\"\"]\ntry:\n    enrich(p2,s)\nexcept ValueError as e:\n    assert \"conflicting\" in str(e)\nelse:\n    raise AssertionError(\"conflict did not fail\")\nprint(\"PASS: synthetic sidecar tests\")\n'''
    (S33/'test_v552j_strata_horizon_sidecar_adapter.py').write_text(test,encoding='utf-8')
    r=subprocess.run([sys.executable,str(S33/'test_v552j_strata_horizon_sidecar_adapter.py')],cwd=S33,capture_output=True,text=True,check=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    dump_json(S33/'SIDECAR_SYNTHETIC_TEST_RETURN.json',{'status':'PASS','stdout':r.stdout.strip(),'runtime_installation':'NOT_PERFORMED','live_artifact_execution':'NOT_PERFORMED'})
    return contract


def make_docs_and_controls(exact,axis,sem,q2,sr,sm,anom,bridge,contract):
    from docx import Document
    from docx.shared import Inches,Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    def setup_doc(d):
        sec=d.sections[0];sec.top_margin=Inches(.72);sec.bottom_margin=Inches(.72);sec.left_margin=Inches(.78);sec.right_margin=Inches(.78)
        styles=d.styles; styles['Normal'].font.name='Aptos';styles['Normal'].font.size=Pt(9.5)
        for st,sz in [('Title',24),('Subtitle',12),('Heading 1',16),('Heading 2',12)]:
            styles[st].font.name='Aptos Display' if 'Heading' in st or st=='Title' else 'Aptos';styles[st].font.size=Pt(sz)
    def table(d,headers,rows,widths=None):
        t=d.add_table(rows=1,cols=len(headers));t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
        tr=t.rows[0]._tr;pr=tr.get_or_add_trPr();pr.append(OxmlElement('w:tblHeader'))
        for i,h in enumerate(headers):
            c=t.rows[0].cells[i];c.text=str(h);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for run in c.paragraphs[0].runs:run.bold=True
        for row in rows:
            cs=t.add_row().cells
            for i,v in enumerate(row):cs[i].text=str(v)
        return t
    counts=Counter(sem.authority_status); exa=Counter(exact.authority_status); structures=Counter(sr.authority_status)
    md=f'''# P2 global reconciliation tranche 2 report\n\n## Authority boundary\nThis tranche adjudicates a bounded high-precision surface. It does not author J-families, join respondents, install registries, write databases or execute V550/V551/V552.\n\n## Completed\n- Resolved all 18 exact bare-target/relation-axis cases: 14 accepted and 4 rejected. Exact foundation is now 270 accepted, 78 rejected and 403 unresolved.\n- Adjudicated 121 non-exact high-precision semantic pairs: {sum(k.startswith('ACCEPTED_') for k in sem.authority_status)} accepted/typed-positive, {sum(k.startswith('REJECTED_') for k in sem.authority_status)} rejected and {sum(k.startswith('UNRESOLVED_') for k in sem.authority_status)} unresolved.\n- Adjudicated all 19 provisional structure analogies member by member: {structures.get('ACCEPTED_FULL_MEMBER_LEVEL_STRUCTURE_ANALOGY',0)} full, {structures.get('ACCEPTED_PARTIAL_MEMBER_LEVEL_STRUCTURE_ANALOGY',0)} partial and {structures.get('REJECTED_SHARED_LABEL_WITHOUT_MEMBER_EQUIVALENCE',0)} rejected.\n- Resolved the 30 semantic-reference anomalies through an overlay; historical inherited files remain untouched. One vague source-local summary item retains an unresolved parent proposition.\n- Authored and synthetically tested a fail-closed V552→V552J strata/horizon sidecar contract and adapter proposal. It is not installed and has not run on live V552/V552J artifacts.\n\n## Structural result\nStructure-label recurrence alone has no authority. The member correspondence ledger records every matched battery child and every source-local extension.\n\n## Exact continuation\nResume at `{NEXT}`. Work through the remaining 18,710 semantic-priority rows by governed neighborhoods, repair the inherited semantic atlas using the correction overlay, harden thin LiTS cross-source evidence as encountered, recover formal nine-strata doctrine, and apply/test the sidecar in the live repository before declaring the V552→V552J lineage repaired. Global P2 remains open.\n'''
    (S33/'P2_GLOBAL_RECONCILIATION_TRANCHE2_REPORT.md').write_text(md,encoding='utf-8')
    (S33/'README_FIRST.md').write_text('# Section 33 · P2 global reconciliation tranche 2\n\nRead the tranche report, exact target/relation-axis rulings, high-precision reworded pair rulings, structure rulings and member correspondences, anomaly overlay, bridge v2, and strata/horizon sidecar contract. This section is governed P2 authority at the explicit grain recorded in each row. It is not J-family or runtime authority.\n',encoding='utf-8')
    (S33/'AUTHORITY_BOUNDARY_AND_METHOD.md').write_text('# Authority boundary and method\n\nEvery ruling uses two-sided exact item evidence. Inherited semantic IDs and structure labels are discovery coordinates only. Positive rulings are bounded by proposition, construct, target nesting, metadata function, or matched-member subset. Negative and unresolved rulings are first-class authority. The historical semantic master is preserved; corrections are applied by overlay. The sidecar adapter is a contract/test artifact, not a live pipeline patch.\n',encoding='utf-8')
    (S33/'EXACT_RESUME_POINT.md').write_text(f'# Exact resume point\n\nResume at `{NEXT}`.\n\nUse the tranche-2 rulings as constraints at their recorded ceilings. Process the 18,710 remaining semantic priority rows neighborhood by neighborhood; do not rematerialize an unbounded fuzzy pair dump. Apply and validate the semantic correction overlay. Recover formal nine-strata doctrine and install/test the sidecar only in the live repository with actual V552/V552J artifacts. Global P2 remains open.\n',encoding='utf-8')
    d=Document();setup_doc(d);d.add_heading('Rawlsing P2 Global Cross-Source Reconciliation',0);d.add_paragraph('Tranche 2 · reworded propositions, relation axes, structure members, semantic-reference repairs, and strata/horizon sidecar contract',style='Subtitle')
    d.add_heading('1. Result',1);d.add_paragraph('The bounded tranche is complete. It converts lexical and inherited-semantic proximity into typed authority only where exact two-sided evidence supports it, and creates negative or unresolved authority everywhere the target, referent, relation axis, polarity, response contract, or source parent fails.')
    table(d,['Surface','Result'],[
      ('Exact bare-target cases','18 resolved: 14 accepted, 4 rejected'),('Exact foundation v2','270 accepted · 78 rejected · 403 unresolved'),
      ('High-precision non-exact pairs',f"{len(sem)} adjudicated: {sum(x.startswith('ACCEPTED_') for x in sem.authority_status)} typed-positive · {sum(x.startswith('REJECTED_') for x in sem.authority_status)} rejected · {sum(x.startswith('UNRESOLVED_') for x in sem.authority_status)} unresolved"),
      ('Structure analogies',f"19 adjudicated: {structures.get('ACCEPTED_FULL_MEMBER_LEVEL_STRUCTURE_ANALOGY',0)} full · {structures.get('ACCEPTED_PARTIAL_MEMBER_LEVEL_STRUCTURE_ANALOGY',0)} partial · {structures.get('REJECTED_SHARED_LABEL_WITHOUT_MEMBER_EQUIVALENCE',0)} rejected"),
      ('Structure member ledger',f'{len(sm)} matched-member and source-extension rulings'),('Semantic anomalies','30 resolved by overlay; one source parent remains bounded-unresolved'),('Strata/horizon lineage','Sidecar contract and adapter synthetically PASS; not installed')])
    d.add_heading('2. What the evidence changed',1);d.add_paragraph('Bare nouns fractured into relation-specific objects. “Social security” divided spending adequacy from benefit receipt/status. “Political party” divided affiliation from organizational membership. Institutional names became comparable only after their trust/confidence battery parent was recovered. The same rule exposed inherited semantic mislabels: medical access was not courts, primary-school access was not police, and same-sex marriage was not climate governance.')
    d.add_heading('3. Reworded and translated propositions',1);d.add_paragraph('The 121-item high-precision pass accepts exact respondent-facing propositions, proposition-only relations, construct coordinates, metadata functions, and nested targets as distinct authority classes. Eighteen false friends are rejected. Six generic or polarity-deficient records remain unresolved because the governing source record omits the statement options or operator required to identify the proposition.')
    d.add_heading('4. Structures',1);d.add_paragraph('Aims, political-system and political-action batteries support full or bounded member-level analogies. Important-in-a-job batteries overlap partially and retain source-specific extensions. An identically labeled EVS supplement has zero WVS member overlap and is explicit negative authority.')
    d.add_heading('5. Semantic reference repair',1);d.add_paragraph('All 30 inherited-reference anomalies are governed through a non-destructive overlay. Replaced or newly assigned coordinates carry no inherited driver, strata or horizon authority. Bridge v2 applies the overlay and quarantines the three contradictory inherited IDs.')
    d.add_heading('6. V552→V552J lineage',1);d.add_paragraph('A sidecar contract and read-only adapter proposal now specify many-to-one cardinality, pass-through fields, duplicate-key failure, non-empty conflict failure, and missing-value preservation. Synthetic tests pass. Runtime repair remains unclaimed because the live V552 and V552J artifacts are absent from this handoff.')
    d.add_heading('7. Exact continuation',1);d.add_paragraph(f'Resume at {NEXT}. Process the remaining 18,710 priority pairs by semantic neighborhood, apply the correction overlay, harden LiTS evidence when used, recover formal nine-strata doctrine, and install/test the sidecar in the live repository. Global P2 remains open; no J-family authority may be authored yet.')
    d.core_properties.title='Rawlsing P2 Global Cross-Source Reconciliation Tranche 2';d.save(S33/'Rawlsing_P2_Global_Cross_Source_Reconciliation_Tranche2_Report_v1_20260731.docx')
    # move predecessor master to phase history and create updated master based on it
    old=V13/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v12_20260731.docx'
    hist=V13/'05_PHASE_HISTORY'/old.name
    if old.exists(): shutil.move(old,hist)
    m=Document(hist);setup_doc(m)
    m.paragraphs[0].text='Rawlsing J-Family Authority Strategy'
    if len(m.paragraphs)>1:m.paragraphs[1].text='Self-contained master restart handoff v13 · global P2 tranche 2 complete'
    if len(m.paragraphs)>2:m.paragraphs[2].text='READ THIS FIRST · GLOBAL P2 OPEN · NO CANONICAL J-FAMILY AUTHORITY YET AUTHORED'
    
    for para in m.paragraphs:
        if para.text.startswith('P2 global reconciliation tranche 1 is complete.'):
            para.text='P2 global reconciliation tranches 1 and 2 are complete. The exact foundation now contains 270 accepted, 78 rejected and 403 unresolved rulings. Tranche 2 also governs 121 high-precision reworded pairs, all 19 provisional structure analogies, and the 30 semantic-reference anomalies. Global P2 remains open.'
        elif 'The final-four v1 packages and Handoff v9 are forensic history only' in para.text:
            para.text='The final-four v1 packages and Handoff v9 are forensic history only; Handoff v11 is the independently verified predecessor, Handoff v12 records tranche 1, and Handoff v13 is current.'
        elif para.text.startswith('Start with CURRENT_STATE.json'):
            para.text='Start with CURRENT_STATE.json, EXACT_RESUME_POINT.md, SCOPE_LOCK.json, OUTPUT_AND_HANDOFF_PROTOCOL.md and section 33. Verify PACKAGE_INDEX.csv and SHA256SUMS.csv before executing any next-stage work.'
        elif para.text=='16. Exact next pass':
            para.text='16. Tranche 1 continuation record (superseded)'
        elif para.text.startswith('Resume with the global reworded/translation-aware'):
            para.text='Historical tranche-1 continuation record: this pass has now been completed in tranche 2. Its outputs are governed in section 33; do not resume here.'
    m.add_page_break();m.add_heading('17. P2 global reconciliation tranche 2',1)
    m.add_paragraph('Tranche 2 resolves every bare-target exact case, adjudicates a bounded non-exact high-precision surface, converts provisional structure-label recurrence into member-level authority, repairs the semantic-reference anomaly surface by overlay, and authors a fail-closed strata/horizon sidecar contract without claiming live installation.')
    table(m,['Surface','Current governed state'],[
      ('Exact foundation','270 accepted · 78 rejected · 403 unresolved'),('High-precision reworded pass',f'{len(sem)} pair rulings'),('Semantic priority queue',f'121 adjudicated · {len(q2)-121:,} pending'),('Structure analogies','19/19 adjudicated'),('Member correspondence rows',len(sm)),('Semantic anomalies','30/30 overlay resolutions'),('V552→V552J sidecar','Contract + synthetic tests PASS; live runtime open')])
    m.add_heading('18. Exact next pass',1);m.add_paragraph(f'Resume at {NEXT}. Work through the remaining semantic neighborhoods and 18,710 bounded priority rows; repair the inherited semantic atlas via overlay; recover formal strata doctrine; and apply/test the sidecar in the live repository. Global P2 remains open. No J-family authoring, respondent execution, database writes, registry installation or V550/V551/V552 execution.')
    m.core_properties.title='Rawlsing J-Family Authority Strategy Master Handoff v13'
    m.save(V13/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v13_20260731.docx')
    # controls
    current={
      'project':'Rawlsing J-family authority','handoff_version':'v13','handoff_date':DATE,'current_phase':'P2',
      'current_pass':'P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2_COMPLETE','next_pass':NEXT,
      'p1_status':'COMPLETE_FROZEN','p1_5_status':'COMPLETE_FROZEN','source_local_deep_passes_closed':['GSS','WVS','EVS','Arab Barometer','Afrobarometer','Asian Barometer','Latinobarómetro','South Asia','LiTS'],'source_local_deep_passes_remaining':[],
      'active_waves':35,'asian_barometer_w6_in_scope':False,'global_question_nodes':18276,'source_local_lineages':13526,
      'exact_foundation_pair_candidates':751,'exact_foundation_accepted':270,'exact_foundation_rejected':78,'exact_foundation_unresolved':403,
      'semantic_priority_queue_total':18831,'semantic_priority_pairs_adjudicated':121,'semantic_priority_pairs_remaining':18710,
      'tranche2_reworded_pair_rulings':len(sem),'tranche2_reworded_typed_positive':sum(x.startswith('ACCEPTED_') for x in sem.authority_status),'tranche2_reworded_rejected':sum(x.startswith('REJECTED_') for x in sem.authority_status),'tranche2_reworded_unresolved':sum(x.startswith('UNRESOLVED_') for x in sem.authority_status),
      'structure_analogy_candidates':19,'structure_analogy_adjudicated':19,'structure_member_correspondence_rows':len(sm),
      'semantic_reference_anomalies_total':30,'semantic_reference_anomalies_overlay_resolved':30,'semantic_reference_parent_propositions_still_unresolved':1,
      'nine_strata_bridge_status':'SIDECAR_CONTRACT_AUTHORED_SYNTHETIC_TEST_PASS_LIVE_INSTALLATION_OPEN','live_pipeline_modified':False,
      'global_p2_closed':False,'substantive_family_authority_authored':False,'respondents_processed':False,
      'exact_resume_document':'00_START_HERE/EXACT_RESUME_POINT.md','tranche2_report':'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2/P2_GLOBAL_RECONCILIATION_TRANCHE2_REPORT.md','cumulative_output_protocol':'00_START_HERE/OUTPUT_AND_HANDOFF_PROTOCOL.md'}
    dump_json(V13/'00_START_HERE'/'CURRENT_STATE.json',current)
    scope={
      'governing_task':'Complete global semantic-neighborhood adjudication and repair the nine-strata doctrine/runtime lineage',
      'allowed':['use all tranche-1 and tranche-2 rulings only at their explicit portability ceilings','process the remaining 18,710 semantic-priority rows by bounded neighborhood','apply the semantic correction overlay and preserve historical source files','harden LiTS row evidence when it enters a cross-source ruling','recover formal nine-strata doctrine and apply/test the sidecar against live V552/V552J artifacts','preserve negative and unresolved authority'],
      'forbidden':['author canonical J-family authority before global P2 closes','treat semantic IDs, text similarity, structure labels or target labels as authority by themselves','install the sidecar without live cardinality/conflict tests','invent missing strata labels, weights or horizons','join respondents','write to database','execute V550/V551/V552'],
      'scope':{'active_waves':35,'sources':9,'asian_barometer_w6':False},'current_phase':'P2','current_pass':current['current_pass'],'next_pass':NEXT,
      'p2_global_reconciliation_permitted':True,'p2_family_authoring_permitted':False,'p2_respondent_execution_permitted':False,
      'tranche2_authority':{'exact_foundation_accepted':270,'exact_foundation_rejected':78,'exact_foundation_unresolved':403,'semantic_pairs_adjudicated':121,'structure_analogies_adjudicated':19,'semantic_reference_overlays':30}}
    dump_json(V13/'00_START_HERE'/'SCOPE_LOCK.json',scope)
    (V13/'00_START_HERE'/'README_FIRST.md').write_text(f'# Rawlsing J-Family Authority Strategy Handoff v13\n\nThis is the complete cumulative restart package through P2 global reconciliation tranche 2. Read the v13 master, CURRENT_STATE.json, EXACT_RESUME_POINT.md, SCOPE_LOCK.json, OUTPUT_AND_HANDOFF_PROTOCOL.md, and section 33.\n\nTranche 2 resolves all 18 exact relation-axis cases, adjudicates 121 high-precision non-exact pairs, adjudicates all 19 provisional structure analogies member by member, repairs all 30 semantic-reference anomalies by overlay, and supplies a synthetically tested but uninstalled V552→V552J strata/horizon sidecar contract.\n\n**Next:** `{NEXT}`. Global P2 is open. No J-family authoring or respondent/runtime execution. Asian Barometer W6 remains excluded.\n',encoding='utf-8')
    (V13/'00_START_HERE'/'EXACT_RESUME_POINT.md').write_text(f'# Governing v13 resume point\n\nResume at:\n\n`{NEXT}`\n\nUse the 270 accepted and 78 negative exact-foundation rulings, the 121 tranche-2 reworded pair rulings, the 19 structure rulings and member correspondence ledger, and the 30-row correction overlay as constraints at their explicit ceilings. Process the remaining 18,710 semantic-priority rows by neighborhood. Recover formal strata doctrine and apply/test the sidecar in the live repository before claiming the V552→V552J lineage repaired. Global P2 remains open. No J-family authoring, respondent joins, database writes, registry installation, or V550/V551/V552 execution. Asian Barometer W6 remains excluded.\n',encoding='utf-8')
    (V13/'00_START_HERE'/'NEXT_CHAT_OPENING_INSTRUCTION.txt').write_text(f'Read README_FIRST.md, CURRENT_STATE.json, EXACT_RESUME_POINT.md, SCOPE_LOCK.json, OUTPUT_AND_HANDOFF_PROTOCOL.md, the v13 master handoff, and section 33. Resume at {NEXT}. Use tranche-2 rulings only at their explicit ceilings. Process 18,710 remaining semantic-priority rows by governed neighborhood, apply the semantic correction overlay, harden LiTS evidence when used, and apply/test the strata-horizon sidecar only against live artifacts. Do not author J-families, join respondents, write databases, install registries, or execute V550/V551/V552. Asian Barometer W6 remains excluded.\n',encoding='utf-8')
    (V13/'00_START_HERE'/'MASTER_HANDOFF.md').write_text(f'# Current governing handoff\n\nThe authoritative narrative is `Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v13_20260731.docx`.\n\nP2 global reconciliation tranche 2 is complete. Exact foundation: 270 accepted, 78 rejected, 403 unresolved. The bounded reworded pass contains 121 pair rulings. All 19 provisional structure analogies are member-level adjudicated. All 30 semantic-reference anomalies have overlay resolutions. The V552→V552J strata/horizon sidecar contract passes synthetic tests but is not installed.\n\n**Exact next pass:** `{NEXT}`.\n\nRead, in order: README_FIRST.md; CURRENT_STATE.json; EXACT_RESUME_POINT.md; SCOPE_LOCK.json; OUTPUT_AND_HANDOFF_PROTOCOL.md; the v13 master DOCX; and section 33.\n',encoding='utf-8')
    # root validation (section validation added later)
    dump_json(V13/'VALIDATION.json',{'status':'PENDING_FINAL_VERIFIER','handoff_version':'v13','current_pass':current['current_pass'],'next_pass':NEXT,'p2_global_reconciliation_tranche2':{'exact_accepted':270,'exact_rejected':78,'exact_unresolved':403,'semantic_pairs_adjudicated':121,'semantic_pairs_remaining':18710,'structure_analogies_adjudicated':19,'semantic_anomalies_overlay_resolved':30,'sidecar_synthetic_test':'PASS','live_pipeline_modified':False}})


def section_validation(exact,axis,sem,q2,sr,sm,anom,bridge):
    ex=Counter(exact.authority_status); se=Counter(sem.authority_status); st=Counter(sr.authority_status)
    checks=[
      ('exact_axis_18',len(axis)==18),('exact_v2_counts',(sum(k.startswith('ACCEPTED_')*v for k,v in ex.items()),sum(k.startswith('REJECTED_')*v for k,v in ex.items()),sum(k.startswith('UNRESOLVED_')*v for k,v in ex.items()))==(270,78,403)),
      ('semantic_121',len(sem)==121 and sem.semantic_pair_candidate_id.nunique()==121),('queue_partition',len(q2)==18831 and (q2.tranche2_review_status=='ADJUDICATED').sum()==121),
      ('structure_19',len(sr)==19 and sr.structure_analogy_candidate_id.nunique()==19),('member_rows_nonzero',len(sm)>0),('anomalies_30',len(anom)==30),('bridge_lineages',len(bridge)==13526),
      ('sidecar_test',json.load(open(S33/'SIDECAR_SYNTHETIC_TEST_RETURN.json'))['status']=='PASS')]
    v={'status':'PASS' if all(x[1] for x in checks) else 'FAIL','checks':[{'check':n,'status':'PASS' if ok else 'FAIL'} for n,ok in checks],
      'counts':{'exact_target_axis_rulings':18,'exact_accepted':270,'exact_rejected':78,'exact_unresolved':403,'semantic_pair_rulings':121,'semantic_pair_statuses':dict(se),'semantic_priority_remaining':18710,'structure_rulings':19,'structure_statuses':dict(st),'member_correspondence_rows':len(sm),'semantic_reference_resolutions':30,'bridge_lineages':13526},'next_pass':NEXT}
    dump_json(S33/'VALIDATION.json',v)
    writecsv(pd.DataFrame(v['checks']),S33/'VALIDATION_CHECKS.csv')


def manifest_and_hashes():
    # section manifest excludes itself
    files=[]
    for p in sorted(S33.iterdir()):
        if p.is_file() and p.name!='SECTION_MANIFEST.csv': files.append({'relative_path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    writecsv(pd.DataFrame(files),S33/'SECTION_MANIFEST.csv')
    # top manifests exclude both top manifest files
    rows=[]
    for p in sorted(x for x in V13.rglob('*') if x.is_file() and x.name not in ('PACKAGE_INDEX.csv','SHA256SUMS.csv')):
        rows.append({'relative_path':p.relative_to(V13).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    df=pd.DataFrame(rows);writecsv(df,V13/'PACKAGE_INDEX.csv');writecsv(df,V13/'SHA256SUMS.csv')


def main():
    setup(); exact,axis=build_exact_target(); sem,q2=build_semantic_rulings(); sr,sm=build_structures(); anom,overlay=build_anomaly_overlay();bridge=build_bridge_v2(overlay);contract=build_sidecar_contract();make_docs_and_controls(exact,axis,sem,q2,sr,sm,anom,bridge,contract);section_validation(exact,axis,sem,q2,sr,sm,anom,bridge);manifest_and_hashes()
    print(json.dumps({'v13':str(V13),'section':str(S33),'counts':{'exact_v2':len(exact),'axis':len(axis),'semantic':len(sem),'structure':len(sr),'member':len(sm),'anomaly':len(anom),'bridge':len(bridge)}},indent=2))
if __name__=='__main__':main()
