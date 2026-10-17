import pandas as pd, re
from pathlib import Path
BASE=Path('/mnt/data/r16c_p_next')
res=pd.read_csv(BASE/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_P.csv').fillna(''); res['wave']=res['wave'].astype(str)
front=pd.read_csv(BASE/'PROVENANCE/C3B15_PROPOSITION_BOUNDARY_FRONTIER_R16C_P.csv').fillna(''); front['wave']=front['wave'].astype(str)
key=['source_family','wave','semantic_unit_id']
F=set(map(tuple,front[key].astype(str).values.tolist()))
res['is_prop_boundary']=[tuple(x) in F for x in res[key].astype(str).values.tolist()]
other=res[~res.is_prop_boundary].copy()

P_pred={
'democratic_content_essentiality','democratic_regime_superiority','democracy_suitability_for_respondent_country',
'strong_leader_nonparliamentary_rule','governance-system suitability','democratic_regime_evaluation|democratic_regime_superiority',
'evaluation of anticipated social change','orientation toward greater respect for authority','interracial-marriage acceptance',
'residential integration preference','democratic_regime_evaluation','neighbor acceptance/social distance','international_engagement_preference',
'appropriateness','gender_preference','policy_preference','policy_choice_preference','socioeconomic-neighborhood integration preference',
'Americanization/cultural-assimilation preference','patient-involvement preference','mental-health social-distance tolerance',
'foreign-policy valence judgment','desired_democratic_regime_degree','presidential_dictatorship_rejection',
'authoritarian_president_indifferent_to_parliament_and_elections','government redistribution responsibility','government_responsibility',
'national belonging criterion','support','desired aid level','patient decision deference','social-change strategy orientation',
'religious_legal_interpretation_endorsement','cohabitation_acceptability','responsibility attribution','piety_criterion_attribution',
'marriage_obstacle','status hierarchy constraint','marriage-obstacle appraisal','obstacle_salience','fairness_judgment'
}
P=other[other['sem__measured_predicate'].isin(P_pred)].copy()
P=pd.concat([P,other[other['sem__measured_predicate']=='evaluative judgment']],ignore_index=True).drop_duplicates(key)
P=pd.concat([P,other[other['sem__measured_predicate']=='social-contact objection/acceptance']],ignore_index=True).drop_duplicates(key)
qra_pos_codes={
('Arab Barometer','I','q610'),('Arab Barometer','I','q4022'),('Arab Barometer','I','q4013'),('Arab Barometer','I','q5057'),('Arab Barometer','I','q5056'),
('Arab Barometer','V','Q709B'),
('EVS','1981','v465'),('EVS','1981','v426'),('EVS','1990','q352h'),('EVS','1990','q277'),
('EVS','2017','v206'),('EVS','2017','v77_DE'),
('LiTS','2006','q312_3'),('LiTS','III','q414c'),
('WVS','W1','V93'),('WVS','W4','IV165'),('WVS','W7','Q197'),('WVS','W7','Q196')
}
qra=other[other['sem__measured_predicate']=='CURRENT_GOVERNED_QRA_ANCHOR']
P=pd.concat([P,qra[qra.apply(lambda r:(r.source_family,r.wave,r.source_variable_code) in qra_pos_codes,axis=1)]],ignore_index=True).drop_duplicates(key)
imp=other[other['sem__measured_predicate'].isin(['importance','importance evaluation'])].copy()
pos_imp_re=re.compile(r'(basic needs for all|recognizing people on merits|equal chance education|govt protect right|government protect right|help worse off|never to try to evade taxes|keep watch on action of govt|citizens have adequate standard of living|respect .*political institutions and laws)',re.I)
P=pd.concat([P,imp[imp.apply(lambda r:bool(pos_imp_re.search(r['sem__semantic_summary']+' || '+r['exact_question_text'])),axis=1)]],ignore_index=True).drop_duplicates(key)

N=other[other['sem__measured_predicate'].str.contains('SOURCE_FIRST_SEMANTIC_CORE_ACCEPTED_',regex=False)].copy()
qra_neg_codes={
('Afrobarometer','R1','pfeerd'),('Afrobarometer','R1','pfpsaf'),('Afrobarometer','R1','pfrass'),('Afrobarometer','R1','pfgmp'),('Afrobarometer','R1','pfpcrm'),
('Afrobarometer','R5','Q66A'),('Afrobarometer','R9','Q50A'),('Afrobarometer','R9','Q41D'),('Afrobarometer','R9','Q46F'),('Afrobarometer','R9','Q44C'),('Afrobarometer','R9','Q44D'),('Afrobarometer','R9','Q46Q'),
('Arab Barometer','I','q254'),('Arab Barometer','II','q5242'),('Arab Barometer','II','t3046'),('Arab Barometer','II','q7112'),('Arab Barometer','V','Q853B'),('Arab Barometer','VIII','Q101'),('Arab Barometer','VIII','QGAZA4A'),
('Asian Barometer','W1','q126'),('Asian Barometer','W1','q004'),('Asian Barometer','W4','q108'),('Asian Barometer','W4','q6'),('Asian Barometer','W4','q103'),
('EVS','1981','v162'),('EVS','1999','v6'),('EVS','1999','o47'),('EVS','1999','v108'),('EVS','2008','v261'),('EVS','2008','v124'),('EVS','2017','v59'),
('GSS','1973','porninf'),('GSS','1973','life'),('GSS','1984','usclass6'),('GSS','2010','harmsgrn'),
('LiTS','2006','q301_7'),('LiTS','2006','q301_2'),('LiTS','II','q708'),('LiTS','II','q219a'),('LiTS','II','q219b'),('LiTS','III','q812a'),('LiTS','III','q817d'),('LiTS','III','q814d'),('LiTS','IV','q809b'),('LiTS','IV','q424'),('LiTS','IV','q827ab'),('LiTS','IV','q827ae'),
('South Asia','W1','c20c'),('South Asia','W1','b7'),('South Asia','W1','b8'),('South Asia','W1','b4'),('South Asia','W2','GB3'),('South Asia','W2','GB11'),('South Asia','W2','GBC6'),('South Asia','W2','GBC12a'),
('WVS','W1','V110'),('WVS','W1','V191'),('WVS','W4','ISL36'),('WVS','W4','IV163'),('WVS','W7','Q146'),('WVS','W7','Q225')
}
N=pd.concat([N,qra[qra.apply(lambda r:(r.source_family,r.wave,r.source_variable_code) in qra_neg_codes,axis=1)]],ignore_index=True).drop_duplicates(key)
N_pred={
'net_benefit_harm','helpfulness_evaluation','religious_comfort','parenting-competence equivalence','parenting-structure equivalence','international_cooperation_need','elite_capture_judgment','accountability_risk','anticipated stigma consequence','anticipated_stigma_consequence','professional_reliance','professional_judgment_reliance','religions_limit_democratic_processes','work-derived satisfaction belief','future expectation','future economic/life outlook','future economic/material outlook','retrospective material/economic change','intergenerational comparison','democratic_working_current_assessment','political_efficacy','FALSE_POSITIVE_RECALL','satisfaction_with_democratic_development','religious-institution guidance adequacy'
}
N=pd.concat([N,other[other['sem__measured_predicate'].isin(N_pred)],other[other['sem__measured_predicate']=='social acceptance/tolerance']],ignore_index=True).drop_duplicates(key)
neg_imp_re=re.compile(r'(how important.*in your life|importance assigned to (work|friends|leisure|god|family)|importance.*job|importance.*at work|body image|importance of ethnic group to r|influence of connections|why voluntary work|importance of personal satisfaction|importance of religious beliefs|building a successful professional future|forming a happy secure family|daily prayer)',re.I)
Nimp=other[other['sem__measured_predicate'].isin(['importance','importance evaluation','motivation_importance','family centrality/value orientation'])]
N=pd.concat([N,Nimp[Nimp.apply(lambda r:bool(neg_imp_re.search(r['sem__semantic_summary']+' || '+r['exact_question_text'])),axis=1)]],ignore_index=True).drop_duplicates(key)
Eval=other[other['sem__measured_predicate']=='evaluation']
neg_eval_re=re.compile(r'(own present living conditions|current national political situation|current state of democracy and human rights|current overall economic condition|quality of people serving in the military)',re.I)
N=pd.concat([N,Eval[Eval.apply(lambda r:bool(neg_eval_re.search(r['sem__semantic_summary']+' || '+r['exact_question_text'])),axis=1)]],ignore_index=True).drop_duplicates(key)
pos_eval_re=re.compile(r'(foreign policies are good or bad|foreign policies for the arab region|more power to local authorities|military service is a good experience|political system for governing respondent country|more emphasis on development of technology|placing more emphasis on development of technology)',re.I)
P=pd.concat([P,Eval[Eval.apply(lambda r:bool(pos_eval_re.search(r['sem__semantic_summary']+' || '+r['exact_question_text'])),axis=1)]],ignore_index=True).drop_duplicates(key)
P['rr_norm_disposition']='POSITIVE_RR_NORM'
N['rr_norm_disposition']='NEGATIVE_RR_NORM'
P['c3b16_basis']='EXPLICIT_NORMATIVE_APPROVAL_PREFERENCE_CRITERION_OR_POLICY_SEMANTICS'
N['c3b16_basis']='DESCRIPTIVE_TRUST_STATE_CAPACITY_EXPECTATION_PERSONAL_SALIENCE_OR_CAUSAL_SEMANTICS'
assert len(P)==199, len(P)
assert len(N)==205, len(N)
pk=set(map(tuple,P[key].astype(str).values.tolist())); nk=set(map(tuple,N[key].astype(str).values.tolist())); assert pk.isdisjoint(nk)
selected=pd.concat([P,N],ignore_index=True)
remaining=res[~pd.MultiIndex.from_frame(res[key].astype(str)).isin(pd.MultiIndex.from_frame(selected[key].astype(str)))].copy()
assert len(remaining)==390
assert sum(remaining['is_prop_boundary'])==243
if __name__=='__main__':
    print('P',len(P),'N',len(N),'selected',len(selected),'remaining',len(remaining),'prop-boundary remaining',sum(remaining.is_prop_boundary))
