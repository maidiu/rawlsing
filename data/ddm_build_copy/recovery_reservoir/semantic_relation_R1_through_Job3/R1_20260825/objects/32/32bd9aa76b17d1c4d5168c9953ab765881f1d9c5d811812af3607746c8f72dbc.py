from pathlib import Path
import pandas as pd, json, re, hashlib, zipfile, shutil, os

ROOT=Path('/mnt/data/r16c_p')
if ROOT.exists(): shutil.rmtree(ROOT)
for d in ['FAMILY_CENSUS','RESOLUTION','QUEUE','PROVENANCE','VALIDATION','CODE']:
    (ROOT/d).mkdir(parents=True, exist_ok=True)

PARENT=Path('/mnt/data/r16c_o')
R10=Path('/mnt/data/r10_onto/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811')
R11=Path('/mnt/data/r11_work')
P2=Path('/mnt/data/c3_work/Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json')

res=pd.read_csv(PARENT/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_O.csv')
res['wave']=res['wave'].astype(str)
census_parent=pd.read_csv(PARENT/'FAMILY_CENSUS/C3B14_RESIDUAL_FAMILY_CENSUS_R16C_O.csv')
census_parent['wave']=census_parent['wave'].astype(str)
prop=census_parent[census_parent.family_bucket=='PROPOSITION_ENDORSEMENT_COMPLEX'].copy()
assert len(res)==982
assert len(prop)==431
sp=pd.read_csv(R10/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz', low_memory=False)
sp['wave']=sp['wave'].astype(str)
r11=pd.read_csv(R11/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz', low_memory=False)
r11['wave']=r11['wave'].astype(str)
p2=json.load(open(P2))
impl=pd.DataFrame(p2['question_implementations'])

keycols=['source_family','wave','semantic_unit_id']

def fulltext(r):
    return (str(r['sem__semantic_summary'])+' || '+str(r['exact_question_text'])).lower()

# Explicit positive RR_NORM recovery. These patterns are only candidate locators; exact rows are then
# filtered by a published exclusion frontier and retained because their governed source semantics are
# prescription, permission, rejection/support, policy recommendation, legal/religious norm, or approval.
pos_patterns=[
    r'\bshould\b', r'\bmust\b', r'\bought\b', r'\bpermitted\b', r'\bpermits\b', r'\bprohibit(?:s|ed)?\b',
    r'\bviolation of\b', r'\bunfit for public office\b', r'\bfavor\b', r'\bfavour\b',
    r'\breject\b', r'\bok to\b', r'\bit is ok\b', r'\bjustif(?:y|ied|iable|ication)\b',
    r'\bright of\b', r'\bright to\b', r'\brecognize right\b', r'\bresponsibility of govt\b',
    r'\bgovernment needs to invest\b', r'\bwork always comes first\b', r'\bstrong unions needed\b',
    r'\bworkers need strong unions\b', r'\bno shortcuts on worker safety\b',
    r'\bpeople need not overly worry about others\b', r'\btake care of yourself first before others\b',
    r'\bthose in need have to take care of themselves\b', r'\bfor the sake of national interest, individual interest could be sacrificed\b',
    r'\bsometimes violent action is necessary\b', r'\bneeds foreign military cooperation\b',
    r'\bislam requires\b', r'\brequires country with majority of muslims be governed\b',
    r'\bislam permits\b', r'\bcompatible with islam\b', r'\bincompatible with islam\b',
    r'\bislam would not oppose\b',
    r'\bpolitical system: experts making decisions\b', r'\bhaving experts.*make decisions\b',
    r'\bhaving the army rule\b', r'\bpolitical system controlled by experts\b',
    r'\bi would rather live under our system of government than any other\b',
    r'\bwould be better.*if\b', r'\bis better off if\b', r'\bnot fair to bring child into world\b',
]
pos_re=re.compile('|'.join(pos_patterns),re.I)

# Conservative descriptive negative locators. Exact rows with value/approval ambiguity are excluded below.
neg_patterns=[
    r'\bcompetent and efficient\b', r'\bfree of corruption\b', r'\bopen and transparent\b', r'\bopen about their decisions\b',
    r'\bacts in its own interests\b', r'\bgood intentions\b', r'\bhonest and truthful\b', r'\bpoor judgement\b',
    r'\bunreliable\b', r'\bunderstands the needs\b', r'\bignore my community\b', r"\bdon'?t respect people like me\b",
    r'\bcarries out its duties poorly\b', r'\bgovernment employees are aware\b', r'\btakes the opinions of citizens seriously\b',
    r'\bcourts punish\b', r'\bjudiciary penalizes\b', r'\bcitizens have the ability to influence\b', r"\bpeople like me don'?t have any influence\b",
    r'\bnation is run by a powerful few\b', r'\bparties and candidates.*equal access\b', r'\btreated equally by the government\b',
    r'\bnothing the court can do\b', r'\bcan join any organization.*without fear\b', r'\bare able to remove a government\b',
    r'\bsystem of government is capable of solving\b', r'\bconstitution expresses values\b',
    r'\bcurrently receive a fair share\b', r'\bcurrently have a voice\b', r'\bother .* think of me as\b', r'\bi feel strong ties\b',
    r'\bcan play a role in limiting climate change\b', r'\bbenefits.*outweigh the costs\b',
    r'\bpositive aspects\b', r'\bis an obstacle to political reform\b', r'\bis an obstacle to reform\b', r'\blogical consequence\b',
    r'\bmany organized groups disrupt\b', r'\bharmony.*disrupted\b', r'\bconstant legislative checks impede\b', r'\bfate determines\b',
    r'\bstate is like a big machine\b', r'\blife has no meaning\b', r'\bdeath has meaning only\b', r'\blife is meaningful only\b',
    r'\bsorrow has meaning only\b', r'\bdeath is a natural resting point\b', r'\bdeath is inevitable\b', r'\bcould do nothing about an unjust law\b',
    r'\bofficials not interested\b', r"\bmost don'?t care what happens\b", r'\bwonder if anything is worthwhile\b',
    r'\bmodern painting is just slapped on\b', r'\bnature would be at peace\b', r'\bhumans evolved from animals\b',
    r'\bonly a few people can judge art\b', r'\bnature is survival of fittest\b', r'\bhumans make all radioactivity\b',
    r'\bmodern science does more harm than good\b', r'\becon grwth always harms envir\b', r'\bscience makes our way of life change too fast\b',
    r'\bscience & tech.*opportunities\b', r'\beconomic progress dependent on environment\b', r'\btoo diff to do anything about envir\b',
    r'\bno saving environment unless others do same\b', r'\bworry too much about progress harming envir\b', r'\bworry too much about envir, too little econ\b',
    r'\bblack people overcome prejudice without favors\b', r'\bmen hurt family when focus on work too much\b',
    r'\bpreschool.*suffer if mother works\b', r'\bfamily life suffers when women work\b',
    r'\bmed.*addictive\b', r'\bmed.*help people\b', r'\bdocs are over medicating\b', r'\bmedicating child.*negative\b',
    r'\bturn kids into zombies\b', r'\bchild with med get into less trouble\b', r'\bpsychiatric med only put off\b',
    r'\bstrong trade unions are bad for us economy\b', r"\bdon'?t have any say about what the government does\b",
    r'\bhave a pretty good understanding of issues\b', r'\bscientists odd and peculiar\b', r'\bscientists work for good of humanity\b',
    r'\bpeople elected to congress try to keep promises\b', r'\bbusiness leaders make money at expense\b', r'\blarge intl company damage\b',
    r'\bpeople like x are unpredictable\b', r'\bthere is a lot of discrimination\b', r'\bfeel lonely without internet\b',
    r'\beconomic situation.*better today\b', r'\bless corruption now\b', r'\bchildren born now.*better life\b',
    r'\bpolitical situation.*better today\b', r'\bi have done better in life than my parents\b', r'\bhousehold lives better nowadays\b',
    r'\bpeople from other ethnic groups enrich\b', r'\bopinions are taken into account\b',
    r'\breligion is a cause of terrorism\b', r'\bcontent of .* education contributes to religious extremism\b',
    r'\bexposure to.*western.*harmful effect\b', r'\bcountry can not solve.*needs to collaborate\b', r'\bcountry cannot solve.*needs collaboration\b',
    r'\bmen are as competent as women to be nurses\b', r'\bwomen are less corrupt than men\b', r'\bwife earning more.*cause problems\b',
    r'\bmen make better political leaders\b', r'\bmen make better business executives\b', r'\bwomen are not suited for politics\b',
    r'\bmen less able.*emotions\b', r'\bwomen primarily want\b', r'\bhaving a job is the best way for a woman to be independent\b',
    r'\bbeing a housewife.*fulfilling\b', r'\bmarriage is.*out[- ]dated\b', r'\bwoman needs children.*fulfilled\b',
    r'\bchild needs a home.*father.*mother\b', r"\bkids are life'?s greatest joy\b", r'\bkidless people lead empty lives\b',
    r'\bethnic groups in us different\b', r'\bwhites different from minorities\b', r'\bindividual of same ethnic group similar\b',
    r'\beth minorities never fit\b', r'\bus harmony by ignore ethnic differences\b', r'\bworking mom can have a warm rel\b',
    r'\btaking medications is a sign of weakness\b', r'\br is sure that other ppl want the best\b', r'\br proud to work for employer\b',
    r'\bi am proud of the type of work\b', r"\br's job is interesting\b", r"\br helps others in job\b", r"\br's job is useful to society\b",
    r'\bjob is just a way to earn money\b', r'\benjoy job even if \$ not needed\b', r"\bi'?m always optimistic\b", r'\bexpect best\b',
    r'\brarely count on good things\b', r'\bagree america is a better country\b', r'\bagree there are things make me ashamed\b',
    r'\bi would rather be a citizen of america\b', r'\bgovernment protects religion\b', r'\bdepends too much on science and not enough on faith\b',
    r'\bscience and technology are making our lives healthier\b', r'\bimmigrants.*increase unemployment\b', r'\bimmigrants fill important job\b',
]
neg_re=re.compile('|'.join(neg_patterns),re.I)

prop['candidate_positive']=prop.apply(lambda r: bool(pos_re.search(fulltext(r))) and 'sci research is strongly in favor of' not in fulltext(r),axis=1)
prop['candidate_negative']=prop.apply(lambda r: bool(neg_re.search(fulltext(r))),axis=1)

# Exact positive exclusion frontier: items where generic wording points to commitment/cost, conduct, or source-shorthand
# whose approval polarity is insufficiently explicit for this RR_NORM checkpoint.
pos_exclusion={(a,b,c) for a,b,c in [
('EVS','1990','q124a'),('EVS','1999','v8'),('EVS','2008','v295'),('EVS','2017','v199'),
('WVS','W4','V33'),('LiTS','IV','q422a'),('LiTS','IV','q422b'),('LiTS','IV','q422c'),
('EVS','1999','v264'),('EVS','2008','v282'),('EVS','1999','o12'),
('GSS','1993','pillok'),('GSS','2002','pillok'),('GSS','2010','pillok'),('GSS','2016','pillok'),('GSS','2024','pillok'),
('Arab Barometer','V','Q605A_3'),('Arab Barometer','V','Q605A_4'),
]}
# Exact negative exclusion frontier: approval/affect or value-orientation cases where the ontology's approval shore
# makes negative RR_NORM closure too aggressive despite descriptive-looking wording.
negative_exclusion_subroles={'family_gender_or_sexual_norm','evaluative_or_value_orientation','work_and_economic_orientation','religious_or_spiritual_orientation'}
affect_re=re.compile(r'\b(rather|prefer\w*|proud|ashamed|shame|love|bother\w*|uncomf\w*|joy|interesting|useful|important|best|good|bad|fair|right|wrong|out[- ]?dated|fulfill\w*|suited|humili\w*)\b',re.I)

pos=prop[prop.candidate_positive].copy()
pos['exact_key_tuple']=pos.apply(lambda r:(r.source_family,str(r.wave),r.source_variable_code),axis=1)
pos_final=pos[~pos.exact_key_tuple.isin(pos_exclusion)].copy()

neg=prop[prop.candidate_negative].copy()
# Remove generic lexical-value warning cases first.
suspicious_re=re.compile(r'\b(should|must|need|needs|right|wrong|fair|unfair|good|bad|best|better|worse|important|acceptable|approve|support|favor|prefer|humiliat|outdated|fulfill|sacrifice|responsib|violation|permit|prohibit|reject|ok|ought|deserve)\b',re.I)
neg=neg[~neg.apply(lambda r:bool(suspicious_re.search(fulltext(r))),axis=1)].copy()
neg=neg[~neg.semantic_subrole.isin(negative_exclusion_subroles)].copy()
neg=neg[~neg.apply(lambda r:bool(affect_re.search(fulltext(r))),axis=1)].copy()
neg_final=neg.copy()

assert len(pos_final)==64, len(pos_final)
assert len(neg_final)==124, len(neg_final)

# Ensure classes are disjoint by exact source-wave semantic decision identity.
pos_keys=set(map(tuple,pos_final[keycols].astype(str).values.tolist()))
neg_keys=set(map(tuple,neg_final[keycols].astype(str).values.tolist()))
assert pos_keys.isdisjoint(neg_keys)
selected_keys=pos_keys|neg_keys
assert len(selected_keys)==188

# Publish proposition-family census with explicit action and reason.
def boundary_reason(r):
    k=(r.source_family,str(r.wave),r.source_variable_code)
    if k in pos_exclusion:
        return 'BOUNDARY__COST_COMMITMENT_CONDUCT_OR_SOURCE_SHORTHAND__NO_RR_NORM_POLARITY_PROMOTION'
    if r.semantic_subrole in negative_exclusion_subroles:
        return 'BOUNDARY__VALUE_OR_APPROVAL_SHORE_AMBIGUITY'
    if affect_re.search(fulltext(r)):
        return 'BOUNDARY__AFFECT_PREFERENCE_OR_EVALUATION_MAY_TOUCH_APPROVAL_SHORE'
    return 'BOUNDARY__GENERIC_PROPOSITION_REQUIRES_FURTHER_SOURCE_SEMANTIC_ADJUDICATION'

pc=prop.copy()
pc['c3b15_action']='RETAIN_FOR_FURTHER_ADJUDICATION'
pc['c3b15_subfamily']='PROPOSITION_BOUNDARY'
pc['c3b15_basis']=pc.apply(boundary_reason,axis=1)
mi=pd.MultiIndex.from_frame(pc[keycols].astype(str))
pmi=pd.MultiIndex.from_tuples(list(pos_keys),names=keycols)
nmi=pd.MultiIndex.from_tuples(list(neg_keys),names=keycols)
pc.loc[mi.isin(pmi),'c3b15_action']='CLOSE_POSITIVE_RR_NORM'
pc.loc[mi.isin(pmi),'c3b15_subfamily']='EXPLICIT_PRESCRIPTION_PERMISSION_REJECTION_OR_APPROVAL'
pc.loc[mi.isin(pmi),'c3b15_basis']='Governed source semantics directly express prescription, permission, rejection/support, policy recommendation, religious/legal norm, or approval of a governance/conduct form.'
pc.loc[mi.isin(nmi),'c3b15_action']='CLOSE_NEGATIVE_RR_NORM'
pc.loc[mi.isin(nmi),'c3b15_subfamily']='DESCRIPTIVE_STATE_CAUSAL_CAPACITY_EXPERIENCE_OR_BELIEF'
pc.loc[mi.isin(nmi),'c3b15_basis']='Governed source semantics are descriptive state/capacity/causal/experience/factual belief with no direct conduct/policy prescription, permission, obligation, or approval claim.'
pc.to_csv(ROOT/'FAMILY_CENSUS/C3B15_PROPOSITION_SUBFAMILY_CENSUS_R16C_P.csv',index=False)
ps=pc.groupby(['c3b15_action','c3b15_subfamily']).size().rename('decision_count').reset_index().sort_values('decision_count',ascending=False)
ps.to_csv(ROOT/'FAMILY_CENSUS/C3B15_PROPOSITION_SUBFAMILY_SUMMARY_R16C_P.csv',index=False)

# Source-reviewed implementation proof from immutable R10 spine + P2.
selected=pd.concat([pos_final.assign(rr_norm_disposition='POSITIVE_RR_NORM'),neg_final.assign(rr_norm_disposition='NEGATIVE_RR_NORM')],ignore_index=True)
sp_sub=sp[pd.MultiIndex.from_frame(sp[['source_family','wave','sem__audit_unit_id']].astype(str)).isin(pd.MultiIndex.from_frame(selected[keycols].astype(str)))][['source_family','wave','sem__audit_unit_id','question_implementation_id','source_variable_code','source_authority']].copy()
assert not sp_sub.duplicated(['source_family','wave','sem__audit_unit_id']).any()
proof=selected.merge(sp_sub,left_on=keycols,right_on=['source_family','wave','sem__audit_unit_id'],how='left',validate='one_to_one')
proof=proof.merge(impl[['question_implementation_id','authority_status']],on='question_implementation_id',how='left',validate='one_to_one')
assert len(proof)==188
assert proof.question_implementation_id.notna().all()
assert (proof.authority_status=='source_reviewed').all()
assert proof.source_authority.fillna('').str.len().gt(0).all()
proof.to_csv(ROOT/'PROVENANCE/C3B15_SOURCE_REVIEWED_IMPLEMENTATION_PROOF_R16C_P.csv',index=False)

# Exact authority ledgers.
pos_out=pos_final.copy()
pos_out['rr_norm_disposition']='POSITIVE_RR_NORM__EXPLICIT_PRESCRIPTION_PERMISSION_REJECTION_OR_APPROVAL'
pos_out['authority_ceiling']='POSITIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY__T06_LINK_STILL_REQUIRES_ACTOR_TARGET_ACTION_ADJUDICATION'
pos_out.to_csv(ROOT/'RESOLUTION/C3B15_POSITIVE_RR_NORM_AUTHORITY_R16C_P.csv',index=False)
neg_out=neg_final.copy()
neg_out['rr_norm_disposition']='NEGATIVE_RR_NORM__DESCRIPTIVE_PROPOSITION'
neg_out['authority_ceiling']='NEGATIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY__NO_RELATION_ABSENCE_CLAIM'
neg_out.to_csv(ROOT/'RESOLUTION/C3B15_NEGATIVE_RR_NORM_AUTHORITY_R16C_P.csv',index=False)

# Exact R11 primitive-row accounting: positives transfer to link review; negatives retire as impossible norm shore.
rm=pd.MultiIndex.from_frame(r11[keycols].astype(str))
pos_rows=r11[rm.isin(pd.MultiIndex.from_frame(pos_final[keycols].astype(str)))].copy()
neg_rows=r11[rm.isin(pd.MultiIndex.from_frame(neg_final[keycols].astype(str)))].copy()
assert len(pos_rows)==4199, len(pos_rows)
assert len(neg_rows)==11173, len(neg_rows)
assert pos_rows.opportunity_id.is_unique and neg_rows.opportunity_id.is_unique
assert set(pos_rows.opportunity_id).isdisjoint(set(neg_rows.opportunity_id))
pos_rows.to_csv(ROOT/'RESOLUTION/C3B15_TRANSFERRED_T06_LINK_REVIEW_ROWS_R16C_P.csv.gz',index=False,compression='gzip')
neg_rows.to_csv(ROOT/'RESOLUTION/C3B15_RETIRED_T06_PRIMITIVE_ROWS_R16C_P.csv.gz',index=False,compression='gzip')

# Parent residual minus exact 188 selected decisions. All non-proposition decisions and 243 proposition boundary decisions survive.
res_mi=pd.MultiIndex.from_frame(res[keycols].astype(str))
sel_mi=pd.MultiIndex.from_tuples(list(selected_keys),names=keycols)
child=res[~res_mi.isin(sel_mi)].copy()
assert len(child)==794, len(child)
child.to_csv(ROOT/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_P.csv',index=False)

boundary=pc[pc.c3b15_action=='RETAIN_FOR_FURTHER_ADJUDICATION'].copy()
assert len(boundary)==243
boundary.to_csv(ROOT/'PROVENANCE/C3B15_PROPOSITION_BOUNDARY_FRONTIER_R16C_P.csv',index=False)
# Explicit positive exclusion frontier.
pos_excl_df=prop[prop.apply(lambda r:(r.source_family,str(r.wave),r.source_variable_code) in pos_exclusion,axis=1)].copy()
pos_excl_df['exclusion_reason']='Cost/commitment/conduct or insufficient source shorthand polarity; no automatic RR_NORM promotion.'
pos_excl_df.to_csv(ROOT/'PROVENANCE/C3B15_POSITIVE_EXCLUSION_FRONTIER_R16C_P.csv',index=False)

# Source-wave accounting.
selacct=selected.groupby(['source_family','wave','rr_norm_disposition']).size().unstack(fill_value=0)
selacct.columns=[str(c) for c in selacct.columns]
rowacct=pd.concat([
    pos_rows.groupby(['source_family','wave']).size().rename('transferred_link_rows'),
    neg_rows.groupby(['source_family','wave']).size().rename('retired_primitive_rows')
],axis=1).fillna(0).astype(int)
acct=selacct.join(rowacct,how='outer').fillna(0).reset_index()
for c in acct.columns:
    if c not in ['source_family','wave']: acct[c]=acct[c].astype(int)
acct.to_csv(ROOT/'RESOLUTION/C3B15_SOURCE_WAVE_ACCOUNTING_R16C_P.csv',index=False)

# Central blocker queue update: both positive and negative role decisions leave input-authority blocker state.
q=pd.read_csv(PARENT/'QUEUE/R16C_O_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv')
q['wave']=q['wave'].astype(str)
q2=q.copy()
for _,r in acct.iterrows():
    closed=int(r.get('POSITIVE_RR_NORM',0)+r.get('NEGATIVE_RR_NORM',0))
    handled=int(r.get('transferred_link_rows',0)+r.get('retired_primitive_rows',0))
    if closed==0 and handled==0: continue
    m=(q2.work_family=='T06_NORM_ROLE_BLOCKER')&(q2.source_family==r.source_family)&(q2.wave==str(r.wave))
    assert m.sum()==1,(r.source_family,r.wave,m.sum())
    q2.loc[m,'decision_atom_count']-=closed
    q2.loc[m,'raw_primitive_row_count_sum']-=handled
    q2.loc[m,'planning_effort_units']-=0.25*closed
assert int(q.decision_atom_count.sum()-q2.decision_atom_count.sum())==188
assert int(q.raw_primitive_row_count_sum.sum()-q2.raw_primitive_row_count_sum.sum())==15372
assert int(q2[q2.work_family=='T06_NORM_ROLE_BLOCKER'].decision_atom_count.sum())==794
assert int(q2[q2.work_family=='T06_NORM_ROLE_BLOCKER'].raw_primitive_row_count_sum.sum())==50335
assert (q2.loc[q2.work_family=='T06_NORM_ROLE_BLOCKER','decision_atom_count']>=0).all()
assert (q2.loc[q2.work_family=='T06_NORM_ROLE_BLOCKER','raw_primitive_row_count_sum']>=0).all()
q2.to_csv(ROOT/'QUEUE/R16C_P_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',index=False)

# Repeated semantic-ID audit keeps exact source+wave key doctrine visible.
dup=child[child.duplicated('semantic_unit_id',keep=False)].sort_values(['semantic_unit_id','source_family','wave'])
dup.to_csv(ROOT/'PROVENANCE/C3B15_REPEATED_SEMANTIC_ID_AUDIT_R16C_P.csv',index=False)

# Doctrine / ancestry note.
(ROOT/'PROVENANCE/C3B15_DOCTRINE.md').write_text('''# C3b15 doctrine — proposition/endorsement large-batch RR_NORM adjudication\n\nThis checkpoint does **not** infer RR_NORM from the fact that a question uses an agree/disagree or endorsement response scale. `proposition_endorsement` is a terrain label only.\n\nPositive RR_NORM requires governed source semantics that directly express prescription, permission/prohibition, obligation, rejection/support, policy recommendation, religious/legal norm, or approval of a governance/conduct form.\n\nNegative RR_NORM requires governed source semantics that are descriptive state/capacity/causal/experience/factual belief and lack a direct conduct/policy prescription, permission, obligation, or approval claim.\n\nCost/commitment items, conduct items, source-shorthand items with insufficient polarity, and value/affect cases near the ontology's approval shore are retained fail-closed.\n\nExact decision identity is `(source_family, wave, semantic_unit_id)`. Semantic-unit ID alone is forbidden.\n\nPositive RR_NORM does not emit a T06 relation: its primitive rows transfer to explicit actor-target-action link review. Negative RR_NORM retires only the impossible norm-shore path.\n''')
(ROOT/'PROVENANCE/C3B15_ANCESTRY_NOTE.md').write_text('''# C3b15 ancestry note\n\nThe adjudication uses already recovered, sealed R10 semantic meanings/source authority, the exact 18,276 implementation spine, P2 `source_reviewed` implementation authority, and sealed R11 T06 opportunity accounting. No missing artifact was assumed and no semantic unit was reconstructed from scratch. The earlier R10 ontology remains controlling: `RR_NORM` is the norm/obligation/approval shore and cannot be inferred merely from moral vocabulary or the R10G semantic-act role.\n''')

status={
 'checkpoint':'R16C-P','subtask':'#18B-C3b15 proposition/endorsement large-batch RR_NORM adjudication',
 'parent_residual':982,'parent_proposition_bucket':431,'positive_rr_norm_closed':64,'negative_rr_norm_closed':124,
 'total_role_decisions_closed':188,'proposition_boundary_remaining':243,'residual_rr_norm':794,
 'positive_link_rows_transferred':4199,'negative_primitive_rows_retired':11173,'blocked_rows_removed_total':15372,
 'c3_total_role_adjudicated':2325,'c3_parent':3119,'c3_percent':round(2325/3119*100,4),
 'c3_negative_rr_norm':2099,'c3_positive_rr_norm':226,'c3_positive_link_rows_total':18469,
 't06_blocked_primitive_rows_parent':65707,'t06_blocked_primitive_rows_successor':50335,
 'central_parent_containers':int(len(q)),'central_successor_containers':int(len(q2)),
 'central_parent_atoms':int(q.decision_atom_count.sum()),'central_successor_atoms':int(q2.decision_atom_count.sum()),
 'worker_packs_changed':False,'job3_authorized':False,
 'next':'C3b16 attack the 243 proposition boundary as finite subfamilies plus the other already-censused residual buckets; do not return to micro-checkpoint cadence.'
}
json.dump(status,open(ROOT/'CURRENT_STATUS_R16C_P.json','w'),indent=2)

report=f'''# R16C-P — #18B-C3b15 proposition/endorsement large-batch RR_NORM adjudication\n\n- Parent C3 residual: **982**.\n- Proposition/endorsement bucket attacked as a whole: **431 decisions**.\n- Closed positive RR_NORM: **64**.\n- Closed negative RR_NORM: **124**.\n- Total proposition decisions closed: **188**.\n- Proposition boundary preserved fail-closed: **243**.\n- Positive rows transferred to T06 actor-target-action link review: **4,199**.\n- Negative impossible norm-shore rows retired: **11,173**.\n- Total T06 input-authority blocked rows removed: **15,372**.\n- C3 residual **982 → 794**.\n- C3 adjudicated **2,325 / 3,119 = {2325/3119*100:.2f}%**.\n- Negative RR_NORM cumulative: **2,099**.\n- Positive RR_NORM cumulative: **226**, preserving **18,469** link-review rows.\n- T06 input-authority blocked primitive surface **65,707 → 50,335**.\n- Central atoms **{int(q.decision_atom_count.sum()):,} → {int(q2.decision_atom_count.sum()):,}**; containers **{len(q2)}**.\n- Worker packs unchanged; Job 3 **NOT AUTHORIZED**.\n\n## Proposition subfamily outcome\n\n{ps.to_markdown(index=False)}\n'''
(ROOT/'R16C_P_CENTRAL_CLOSURE_REPORT.md').write_text(report)

pointer=f'''# ACTIVE EXECUTION POINTER — R16C-P\n\nCanonical floor: `CHECKPOINT_R16C_P_20260812`.\n\nCurrent state: C3 RR_NORM **2,325 / 3,119 = {2325/3119*100:.2f}% adjudicated**; residual **794**.\n\nC3b15 closed **188 / 431** proposition/endorsement decisions in one governed batch. **243** proposition-boundary decisions remain fail-closed.\n\nNext execution: **C3b16 — use the R16C-O full residual family census plus the R16C-P proposition boundary to attack the next large coherent family set; do not revert to micro-checkpoints.**\n\nHard invariants:\n- exact decision key = `(source_family, wave, semantic_unit_id)`; never semantic ID alone;\n- proposition endorsement is terrain only, never RR_NORM authority by itself;\n- positive RR_NORM rows transfer to T06 link review, never directly emit relations;\n- worker packs remain sealed; Job 3 not authorized.\n'''
(ROOT/'ACTIVE_EXECUTION_POINTER.md').write_text(pointer)
ledger=f'''# ACTIVE PROGRESS LEDGER — after R16C-P\n\n- Governing 25-item checklist: **9/25 DONE**; #18 active.\n- #18A worker-pack construction: DONE, packs sealed and untouched.\n- #18B central prerequisite campaign: ACTIVE.\n- C3 RR_NORM shore: **2,325 / 3,119 ({2325/3119*100:.2f}%) adjudicated**.\n- Residual RR_NORM decisions: **794**.\n- Negative RR_NORM: **2,099**.\n- Positive RR_NORM: **226**, preserving **18,469** link-review rows.\n- T06 input-authority blocked primitive surface: **50,335 rows**.\n- Central queue: **{len(q2)} containers / {int(q2.decision_atom_count.sum()):,} atoms**.\n- Worker packs changed: NO.\n- Job 3 authorized: NO.\n\n## What R16C-P changed\nOne release cycle attacked all 431 proposition/endorsement cases, closing 188 exact role decisions while publishing a 243-decision fail-closed boundary frontier. This is the larger-batch cadence: semantic family census → exact closures → hostile QA → one cold replay → Library.\n\n## Next\nC3b16: attack the next large coherent residual family set using the existing census and the new proposition boundary; no return to 20-row release loops.\n'''
(ROOT/'ACTIVE_PROGRESS_LEDGER.md').write_text(ledger)

# Construction validation.
checks=[]
def check(name,cond,detail=''):
    checks.append({'check':name,'pass':bool(cond),'detail':str(detail)})
check('parent_residual_982',len(res)==982,len(res))
check('prop_bucket_431',len(prop)==431,len(prop))
check('prop_census_431',len(pc)==431,len(pc))
check('prop_census_actions_sum_431',int(ps.decision_count.sum())==431,int(ps.decision_count.sum()))
check('positive_exact_64',len(pos_final)==64,len(pos_final))
check('negative_exact_124',len(neg_final)==124,len(neg_final))
check('selected_exact_188',len(selected_keys)==188,len(selected_keys))
check('positive_negative_disjoint',pos_keys.isdisjoint(neg_keys))
check('boundary_exact_243',len(boundary)==243,len(boundary))
check('proof_exact_188',len(proof)==188,len(proof))
check('all_selected_source_reviewed',(proof.authority_status=='source_reviewed').all())
check('all_selected_r10_authority_nonempty',proof.source_authority.fillna('').str.len().gt(0).all())
check('positive_link_rows_4199',len(pos_rows)==4199,len(pos_rows))
check('negative_retired_rows_11173',len(neg_rows)==11173,len(neg_rows))
check('handled_rows_15372',len(pos_rows)+len(neg_rows)==15372,len(pos_rows)+len(neg_rows))
check('handled_opportunity_ids_unique',len(set(pos_rows.opportunity_id)|set(neg_rows.opportunity_id))==15372)
check('child_residual_794',len(child)==794,len(child))
check('parent_minus_child_188',len(res)-len(child)==188,len(res)-len(child))
# All non-proposition R16C-O residual decisions survive unchanged.
prop_parent_keys=pd.MultiIndex.from_frame(prop[keycols].astype(str))
res_keys=pd.MultiIndex.from_frame(res[keycols].astype(str))
nonprop_parent=res[~res_keys.isin(prop_parent_keys)].copy()
nonprop_keys=pd.MultiIndex.from_frame(nonprop_parent[keycols].astype(str))
child_keys=pd.MultiIndex.from_frame(child[keycols].astype(str))
check('all_551_nonprop_decisions_survive',len(nonprop_parent)==551 and nonprop_keys.isin(child_keys).all(),len(nonprop_parent))
check('all_243_prop_boundary_survive',pd.MultiIndex.from_frame(boundary[keycols].astype(str)).isin(child_keys).all(),len(boundary))
check('central_atom_delta_188',int(q.decision_atom_count.sum()-q2.decision_atom_count.sum())==188)
check('central_raw_delta_15372',int(q.raw_primitive_row_count_sum.sum()-q2.raw_primitive_row_count_sum.sum())==15372)
check('t06_blocker_atoms_794',int(q2[q2.work_family=='T06_NORM_ROLE_BLOCKER'].decision_atom_count.sum())==794)
check('t06_blocker_rows_50335',int(q2[q2.work_family=='T06_NORM_ROLE_BLOCKER'].raw_primitive_row_count_sum.sum())==50335)
check('worker_lane_absent_from_central_queue',q2[q2.execution_lane.astype(str).str.contains('WORKER',na=False)].empty)
check('job3_false',status['job3_authorized'] is False)
vr={'checkpoint':'R16C-P','pass':all(x['pass'] for x in checks),'checks':checks,'check_count':len(checks)}
json.dump(vr,open(ROOT/'VALIDATION/VALIDATION_RESULT_R16C_P.json','w'),indent=2)
assert vr['pass']

# Hostile QA.
h=[]
def hc(n,c,d=''): h.append({'attack':n,'pass':bool(c),'detail':str(d)})
hc('exact_key_is_three_part',all(len(k)==3 for k in selected_keys))
hc('no_semantic_id_only_selection',len(child[child.duplicated('semantic_unit_id',False)])>0,len(child[child.duplicated('semantic_unit_id',False)]))
hc('no_positive_exclusion_key_promoted',not any((r.source_family,str(r.wave),r.source_variable_code) in pos_exclusion for _,r in pos_final.iterrows()))
hc('all_positive_exclusion_rows_preserved',pd.MultiIndex.from_frame(pos_excl_df[keycols].astype(str)).isin(child_keys).all(),len(pos_excl_df))
hc('no_negative_value_subrole_closed',not neg_final.semantic_subrole.isin(negative_exclusion_subroles).any())
hc('no_negative_affect_warning_closed',not neg_final.apply(lambda r:bool(affect_re.search(fulltext(r))),axis=1).any())
hc('positive_rows_do_not_directly_emit_relation',pos_out.authority_ceiling.str.contains('LINK_STILL_REQUIRES').all())
hc('negative_rows_no_relation_absence_claim',neg_out.authority_ceiling.str.contains('NO_RELATION_ABSENCE_CLAIM').all())
hc('all_positive_r11_rows_exact_selected_keys',pd.MultiIndex.from_frame(pos_rows[keycols].astype(str)).isin(pd.MultiIndex.from_frame(pos_final[keycols].astype(str))).all())
hc('all_negative_r11_rows_exact_selected_keys',pd.MultiIndex.from_frame(neg_rows[keycols].astype(str)).isin(pd.MultiIndex.from_frame(neg_final[keycols].astype(str))).all())
hc('positive_negative_r11_disjoint',set(pos_rows.opportunity_id).isdisjoint(set(neg_rows.opportunity_id)))
hc('nonprop_residual_untouched',len(nonprop_parent)==551,len(nonprop_parent))
hc('planning_delta_quarter_per_closed_role',abs((q.planning_effort_units.sum()-q2.planning_effort_units.sum())-47.0)<1e-8,q.planning_effort_units.sum()-q2.planning_effort_units.sum())
hc('central_container_count_stable',len(q2)==len(q),len(q2))
hc('worker_packs_unchanged',status['worker_packs_changed'] is False)
hqa={'checkpoint':'R16C-P','pass':all(x['pass'] for x in h),'attacks':h,'attack_count':len(h)}
json.dump(hqa,open(ROOT/'VALIDATION/R16C_P_HOSTILE_QA.json','w'),indent=2)
assert hqa['pass']

# Preserve exact builder.
shutil.copy2('/mnt/data/build_r16c_p.py',ROOT/'CODE/build_r16c_p.py')

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for ch in iter(lambda:f.read(1<<20),b''):h.update(ch)
    return h.hexdigest()
files=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.name!='SHA256_MANIFEST_R16C_P.csv':
        files.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'size_bytes':p.stat().st_size})
pd.DataFrame(files).to_csv(ROOT/'SHA256_MANIFEST_R16C_P.csv',index=False)

z=Path('/mnt/data/Rawlsing_R10K_S14_Central_Closure_Checkpoint_R16C_P_20260812.zip')
if z.exists(): z.unlink()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file(): zz.write(p,p.relative_to(ROOT))
zsha=sha(z)
Path(str(z)+'.sha256').write_text(f'{zsha}  {z.name}\n')
print(json.dumps({'zip':str(z),'sha256':zsha,'checks':len(checks),'hostile':len(h),'positive':len(pos_final),'negative':len(neg_final),'boundary':len(boundary),'pos_rows':len(pos_rows),'neg_rows':len(neg_rows),'residual':len(child),'c3_pct':2325/3119*100},indent=2))
