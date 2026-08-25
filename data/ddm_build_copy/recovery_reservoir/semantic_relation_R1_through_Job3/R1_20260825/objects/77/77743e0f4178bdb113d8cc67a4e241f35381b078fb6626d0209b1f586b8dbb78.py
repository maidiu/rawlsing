from pathlib import Path
import pandas as pd,json,re,sys
R=Path(sys.argv[1] if len(sys.argv)>1 else '.')
checks=[]
def ck(n,v):
 checks.append((n,bool(v)));
 if not v: raise AssertionError(n)
neg=pd.read_csv(R/'RESOLUTION/C3B10_DEMOCRATICNESS_ASSESSMENT_NEGATIVE_RR_NORM_AUTHORITY_R16C_K.csv',dtype=str)
res=pd.read_csv(R/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_K.csv',dtype=str)
ret=pd.read_csv(R/'RESOLUTION/C3B10_RETIRED_T06_PRIMITIVE_ROWS_R16C_K.csv.gz',dtype=str)
proof=pd.read_csv(R/'PROVENANCE/C3B10_SOURCE_REVIEWED_IMPLEMENTATION_PROOF_R16C_K.csv',dtype=str)
front=pd.read_csv(R/'PROVENANCE/C3B10_DEMOCRACY_TERRAIN_EXCLUSION_FRONTIER_R16C_K.csv',dtype=str)
q=pd.read_csv(R/'QUEUE/R16C_K_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv')
st=json.load(open(R/'CURRENT_STATUS_R16C_K.json'))
preds={'external_or_named_country_democraticness_assessment','current_or_target_country_democraticness_assessment','current_own_country_democraticness_assessment','past_regime_democraticness_assessment','expected_future_democraticness_assessment'}
pat=re.compile(r'\\b(?:should|must|ought|duty|obligat\\w*|responsib(?:le|ility)|acceptable|unacceptable|allow(?:ed)?|forbid\\w*|prohibit\\w*|right to|deserve\\w*|better if|necessary to|need to)\\b',re.I)
ck('neg_42',len(neg)==42)
ck('residual_1173',len(res)==1173)
ck('five_predicates_only',set(neg.sem__measured_predicate)==preds)
ck('role_exact',set(neg.sem__canonical_role)=={'SOURCE_BOUNDED_RELATIONAL_MEASURE'})
ck('no_r2_norm',set(neg.in_r2_norm_shore.fillna('False').str.lower())=={'false'})
ck('no_norm_operator',not any(pat.search(str(a)+' '+str(b)) for a,b in zip(neg.exact_question_text.fillna(''),neg.sem__semantic_summary.fillna(''))))
ck('retired_1228',len(ret)==1228 and ret.opportunity_id.nunique()==1228)
ck('retired_42_decisions',ret[['source_family','wave','semantic_unit_id']].drop_duplicates().shape[0]==42)
ck('proof_42',len(proof)==42 and proof.question_implementation_id.nunique()==42)
ck('proof_source_reviewed',set(proof.p2_authority_status)=={'source_reviewed'})
ck('proof_source_authority',proof.source_authority.fillna('').str.len().gt(0).all())
ck('front_content_open',(front.sem__measured_predicate=='democratic_content_essentiality').sum()>=13)
ck('front_superiority_open',(front.sem__measured_predicate=='democratic_regime_superiority').sum()>=8)
ck('front_suitability_open',(front.sem__measured_predicate=='democracy_suitability_for_respondent_country').sum()>=8)
ck('queue_114',len(q)==114)
ck('queue_atoms_33227',int(q.decision_atom_count.sum())==33227)
ck('status_math',st['c3_negative_rr_norm']+st['c3_positive_rr_norm']+st['residual_rr_norm']==3119)
ck('job3_false',st['job3_authorized'] is False and st['worker_packs_changed'] is False)
out={'pass':all(v for _,v in checks),'checks_passed':sum(v for _,v in checks),'checks_total':len(checks),'checks':[{'name':n,'pass':v} for n,v in checks]}
print(json.dumps(out,indent=2))
