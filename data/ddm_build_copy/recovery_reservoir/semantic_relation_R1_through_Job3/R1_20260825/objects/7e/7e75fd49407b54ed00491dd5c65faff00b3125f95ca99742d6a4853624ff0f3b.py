import pandas as pd, json, gzip, re, os, hashlib
from pathlib import Path
BASE=Path('/mnt/data/t06w04_source_first/authority/Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812')
ROOT=Path('/mnt/data/t06w04_source_first/T06W04'); R=ROOT/'RETURN'; R.mkdir(parents=True,exist_ok=True)
wave_dirs=['GSS__2002','Arab_Barometer__VIII','EVS__2008','EVS__1990','Asian_Barometer__W5','South_Asia__W1']
frames=[]
for wd in wave_dirs:
    frames.append(pd.read_csv(BASE/'BY_WAVE'/wd/'IMPLEMENTATION_SOURCE_CONTEXT.csv',dtype=str).fillna(''))
D=pd.concat(frames,ignore_index=True)
assert len(D)==3052

def jd(x): return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def hid(prefix,*parts,n=18): return prefix+hashlib.sha256('||'.join(map(str,parts)).encode()).hexdigest()[:n]
# Load native pages per wave for exact source excerpts.
pages={}
for wd in wave_dirs:
    arr=[]
    with gzip.open(BASE/'BY_WAVE'/wd/'NATIVE_SOURCE_PAGE_TEXT.jsonl.gz','rt',encoding='utf-8') as f:
        for line in f:
            o=json.loads(line); arr.append((str(o.get('relative_path','')),str(o.get('page_number','')),str(o.get('page_text') or o.get('text') or '')))
    pages[wd]=arr
wdmap={('GSS','2002'):'GSS__2002',('Arab Barometer','VIII'):'Arab_Barometer__VIII',('EVS','2008'):'EVS__2008',('EVS','1990'):'EVS__1990',('Asian Barometer','W5'):'Asian_Barometer__W5',('South Asia','W1'):'South_Asia__W1'}

def row(fam,wave,code):
    z=D[(D.source_family==fam)&(D.wave==str(wave))&(D.source_variable_code.str.lower()==code.lower())]
    if len(z)!=1: raise ValueError((fam,wave,code,len(z)))
    return z.iloc[0]

def native_evidence(fam,wave,code):
    r=row(fam,wave,code); wd=wdmap[(fam,str(wave))]; candidates=pages[wd]
    # explicit page first
    if r.explicit_source_relative_path and r.explicit_source_page:
        pnum=str(int(float(r.explicit_source_page))) if re.match(r'^\d+(\.0)?$',r.explicit_source_page) else r.explicit_source_page
        candidates=sorted(candidates,key=lambda x:0 if (x[0]==r.explicit_source_relative_path and x[1]==pnum) else 1)
    pats=[re.escape(code)]
    # add distinctive first 6 words from exact text
    words=re.findall(r'[A-Za-z0-9]+',r.exact_question_text)
    if len(words)>=4: pats.append(re.escape(' '.join(words[:min(8,len(words))])))
    for path,pno,txt in candidates:
        for pat in pats:
            m=re.search(pat,txt,re.I)
            if m:
                # line/sentence-like excerpt around occurrence
                s=max(0,m.start()-220); e=min(len(txt),m.end()+700)
                ex=re.sub(r'\s+',' ',txt[s:e]).strip()
                return ex, f'{path} p.{pno}'
    # fallback explicit page whole beginning
    for path,pno,txt in candidates:
        if r.explicit_source_relative_path and path==r.explicit_source_relative_path:
            ex=re.sub(r'\s+',' ',txt[:900]).strip(); return ex,f'{path} p.{pno}'
    docs=json.loads(r.native_document_set_json) if r.native_document_set_json else []
    prov=docs[0].get('relative_path','wave-local native source') if docs else 'wave-local native source'
    return r.exact_question_text, prov+' [flattened source search did not isolate a narrower excerpt]'

# Initial source-first classification heuristic, then positive-member/manual battery corrections are overlaid.
A=D.copy()
A['substantive_implementation']=A.current_o07_measurement_use_class_DIAGNOSTIC_ONLY.map(lambda x:'FALSE' if x=='ADMIN' else 'TRUE')
A['implementation_classification']='OTHER'
t=A.exact_question_text.str.lower()
norm_pat=r'\b(should|ought|must|right to|wrong|justif|acceptable|allow|approve|approval|ideal|duty|obligation|essential|morally|moral obligation|need children|responsibility of the government|responsible for)\b'
A.loc[t.str.contains(norm_pat,regex=True,na=False),'implementation_classification']='NORM_SHORE'
conduct_pat=r'\b(have you|did you|do you |will you|would you|ever |past [0-9]|last year|last week|currently|living with|lived with|worked|work unpaid|labor force status|marital status|number of children|age when|where do you work|attended|signed|boycott|contacted|voted|vote in|freedom of choice|have influence|guaranteed|how many children)\b'
cm=(A.implementation_classification=='OTHER') & t.str.contains(conduct_pat,regex=True,na=False)
A.loc[cm,'implementation_classification']='CONDUCT_SHORE'
# Known source-binding ambiguities relevant to T06 where labels exist but native page/item binding is not recovered.
amb_gss=['adcou','addoc','adfam','adhdcon','adhdknow','adhdknw','adhdmed','adhdreal','adhos','adpsy','adtch','agekdbrn_9422','docvig','forcedoc','forcehos','forcemed','knwmhosp','adcoumed','addocmed']
for c in amb_gss:
    m=(A.source_family=='GSS')&(A.wave=='2002')&(A.source_variable_code.str.lower()==c.lower())
    A.loc[m,'implementation_classification']='SOURCE_AMBIGUOUS'
for c in ['q106c','q106d','q106e']:
    m=(A.source_family=='Asian Barometer')&(A.wave=='W5')&(A.source_variable_code.str.lower()==c.lower())
    A.loc[m,'implementation_classification']='SOURCE_AMBIGUOUS'
# Force known relation members to correct shores.
base_specs=[]
def spec(fam,wave,norms,conducts,common,actor,target,action,condition,basis,grain=''):
    base_specs.append((fam,str(wave),norms,conducts,common,actor,target,action,condition,basis,grain))
# GSS 13
spec('GSS',2002,['wrknokid'],['rwrknokd'],'women working outside home after marriage before children','women; female respondent instance','work outside home before children','work outside home','after marriage; before children; R21 ever-had-children routing','Family 2002 norm and realized-work lifecycle cell have same action and lifecycle condition.','One lifecycle cell; female respondent-instance condition required downstream.')
spec('GSS',2002,['fewknokd'],['rwrknokd'],'women working outside home before first child','women; female respondent instance','work outside home before first child','work outside home','couple not yet had child / after marriage before children','Family N23 norm aligns to R21a realized-work cell at the same pre-child lifecycle stage.','Female respondent-instance condition required.')
spec('GSS',2002,['wrkbaby'],['rwrkbaby'],'women working outside home while child preschool age','women; female respondent instance','child under school age','work outside home','child under school age; R21 ever-had-children routing','Family R3b and R21b repeat the same lifecycle condition.','Female respondent-instance condition required.')
spec('GSS',2002,['wrksch'],['rwrksch'],'women working outside home after youngest starts school','women; female respondent instance','youngest child started school','work outside home','after youngest child starts school','Family R3c/R21c same lifecycle action/condition.','Female respondent-instance condition required.')
spec('GSS',2002,['wrkgrown'],['rwrkgrwn'],'women working outside home after children leave home','women; female respondent instance','after children leave home','work outside home','after children leave home','Family R3d/R21d same lifecycle action/condition.','Female respondent-instance condition required.')
spec('GSS',2002,['ftwork'],['wrkstat'],'full-time employment','young person; respondent as instance','full-time employment','be employed full-time','Adult Transition criterion vs current/last-week labor-force state','Adult Transition makes full-time employment an adulthood criterion; WRKSTAT records realized employment status.')
spec('GSS',2002,['getmar'],['marital'],'marriage','young person; respondent as instance','marriage','get/be married','Adult Transition criterion vs realized marital status','Exact marriage action/state identity at source grain.')
spec('GSS',2002,['havchld'],['childs'],'having a child','young person; respondent as instance','childbearing','have a child','Adult Transition criterion vs lifetime child count','Exact childbearing action; CHILDS records realized lifetime childbearing.')
spec('GSS',2002,['havchld1'],['agekdbrn'],'age at first childbearing','young person; respondent as instance','age at first birth','have first child by/at age','HAVCHLD importance routing; AGEKDBRN CHILDS>0 routing','Normative age threshold and realized age at first birth are directly comparable.')
spec('GSS',2002,['chldidel'],['childs'],'number of children','family/people; respondent instance','number of children','have children','ideal family-size vs lifetime realized count','Ideal number of children and realized child count share same count target/action domain.')
spec('GSS',2002,['othshelp'],['hlpneedy'],'helping people in need','people; respondent instance','less-fortunate/needy people','help by contributing time','Altruism ballot vs Adult Transition past-five-year conduct','Norm asks people to help less-fortunate others; endpoint records contribution of time to help needy people.')
spec('GSS',2002,['peoptrbl'],['hlpneedy'],'helping people in need','respondent','people in trouble/needy people','personally help/assist','personal importance vs past-five-year conduct','Personal importance of assisting people in trouble aligns to realized help of needy people at compatible need-based target scope.')
spec('GSS',2002,['mehhwork'],['hhwkfair'],'share of household work','men; male respondent instance','household work share','do/share household work','Family module; male respondent conditioning','Norm says men ought to do larger share; endpoint reports respondent share relative to spouse/partner. Male conditioning resolves actor scope.')
# Arab 4
spec('Arab Barometer','VIII',['Q606_3B'],['Q606_3'],'religious clerics influencing government decisions','religious clerics','government decisions','have influence','Q606 split A/B wording preserved','Q606 explicitly fields have-influence versus should-have-influence formulations with identical actor/action/target.')
spec('Arab Barometer','VIII',['Q606_NT_3'],['Q606_NT_3B'],'religious uluma influencing government decisions','religious uluma','government decisions','have influence','Q606 NT split wording preserved','Q606 explicitly fields should-have-influence versus have-influence formulations with identical actor/action/target.')
spec('Arab Barometer','VIII',['Q601_5'],['Q628_3A'],'gender equality in opportunity/freedom to get a job','men and women','employment/getting a job','have equal work opportunity / freedom to get a job','gender battery item conditions preserved','Norm of equal work opportunities aligns to measured gendered freedom to get a job.')
spec('Arab Barometer','VIII',['Q601_13B'],['Q628_4B'],'gender equality in choosing whom to marry','men and women','choice of marriage partner','choose whom to marry','gender battery item conditions preserved','Norm of equal say in whom to marry aligns to measured gendered freedom to choose whom to marry.')
# EVS 2008 8
spec('EVS','2008',['v95'],['v89'],'working / employment','people/respondent','employment','work/be employed','EVS respondent universe','Work-as-duty norm aligns to employed/not-employed realized state.')
spec('EVS','2008',['v95'],['v337'],'working / employment','people/respondent','paid employment','work/be in paid employment','EVS respondent universe','Work-as-duty norm aligns to paid-employment endpoint.')
spec('EVS','2008',['v149'],['v321'],'having children','women; female respondent instance','childbearing','have children','EVS respondent universe','Norm/criterion that women need children aligns to realized child count for female respondents.')
spec('EVS','2008',['v152'],['v321'],'having children','men; male respondent instance','childbearing','have children','EVS respondent universe','Norm/criterion that men need children aligns to realized child count for male respondents.')
spec('EVS','2008',['v156'],['v321'],'having children','people/respondent','childbearing','have children','EVS respondent universe','Explicit duty toward society to have children aligns to realized child count.')
spec('EVS','2008',['v155'],['v314'],'cohabiting without being married at the time','two people/couple; respondent instance','unmarried cohabitation','live together without marriage','pre-marital/pre-registration branch','Permissibility of unmarried cohabitation aligns to realized pre-marital cohabitation.')
spec('EVS','2008',['v155'],['v315'],'cohabiting without being married at the time','two people/couple; respondent instance','unmarried cohabitation','live together without marriage','current-partner routing preserved','Permissibility of unmarried cohabitation aligns to current cohabitation under source routing.')
spec('EVS','2008',['v155'],['v319'],'cohabiting without being married at the time','two people/couple; respondent instance','unmarried cohabitation','live together before marriage/registration','partner/marriage routing preserved','Permissibility of unmarried cohabitation aligns to realized cohabitation before marriage/registration.')
# EVS 1990 3
spec('EVS','1990',['q439'],['q437'],'number of children','family/people; respondent instance','number of children','have children','EVS 1990 respondent universe','Ideal family size aligns to realized number of children ever had.')
spec('EVS','1990',['q442'],['q437'],'having children','women; female respondent instance','childbearing','have children','EVS 1990 respondent universe','Norm/criterion that women need children aligns to realized childbearing for female respondents.')
vol=[f'q{i}b' for i in range(149,165)]
spec('EVS','1990',['q170d'],vol,'unpaid voluntary work under a felt duty/moral obligation','respondent','unpaid voluntary work','perform unpaid voluntary work','Q170 reason conditioned on voluntary work; Q149b-Q164b source battery','Explicit duty/moral-obligation motive for voluntary work aligns to the source-native unpaid-work endpoint battery.')
# Asian 2, South 1
spec('Asian Barometer','W5',['q106'],['q107'],'government action on respondent-identified most-important national problem','government','respondent-identified most-important problem','address/solve problem','Q107 explicitly refers back to most important problem; five-year horizon','Q106 asks what government should address; Q107 asks expected government solving of that same identified problem.')
spec('Asian Barometer','W5',['q93'],['q79'],'participation in protests and demonstrations','people; respondent instance','political protest participation','take part in protest/demonstration','democracy-characteristic norm; Q79 behavior/willingness response scale','Freedom to participate in protests as a normative democracy criterion aligns to respondent protest participation/willingness.')
spec('South Asia','W1',['c31c'],['d5'],'women going out to work','women; female respondent instance','employment/work','go out and work','female respondent conditioning required','C31c grants women equal freedom to work; D5 records respondent work status. Relation applies to female respondent instances.')

# Force all spec members to shores and complete action signatures.
for fam,w,norms,conds,common,actor,target,action,condition,basis,grain in base_specs:
    for c in norms:
        m=(A.source_family==fam)&(A.wave==w)&(A.source_variable_code.str.lower()==c.lower()); A.loc[m,'implementation_classification']='NORM_SHORE'
    for c in conds:
        m=(A.source_family==fam)&(A.wave==w)&(A.source_variable_code.str.lower()==c.lower()); A.loc[m,'implementation_classification']='CONDUCT_SHORE'

# Common action signature, refined enough for search accounting. Source-native detail in positives/crosswalk controls authority.
def generic_sig(r,cls):
    txt=r.exact_question_text
    actor='respondent/reporting subject' if cls=='CONDUCT_SHORE' else ('general/source-specified actor' if cls=='NORM_SHORE' else '')
    modality={'NORM_SHORE':'normative/criterion/permissibility as source wording indicates','CONDUCT_SHORE':'realized/stated/expected/exposure endpoint as source wording indicates','SOURCE_AMBIGUOUS':'unresolved','OTHER':'non-T06 or no shore role established'}[cls]
    return jd({'actor':actor,'action':txt,'target_or_object':txt,'modality':modality,'condition':'preserve native item/stem/routing','respondent_universe':'preserve wave-local native routing','source_battery_or_stem':'wave-local instrument reconstruction'})
A['action_signature_json']=[generic_sig(r,A.iloc[i].implementation_classification) for i,r in D.iterrows()]
A['source_battery_or_stem']='wave-local instrument reconstruction'
def basis_for(r):
    if r.explicit_source_relative_path and r.explicit_source_page: return f'Native source authority: {r.explicit_source_relative_path} p.{r.explicit_source_page}; implementation spine binds exact code/ID.'
    return 'Wave-local native document set searched first; implementation spine binds exact code/ID; generated labels used only for navigation.'
A['source_basis']=[basis_for(r) for _,r in D.iterrows()]
A.loc[A.implementation_classification=='SOURCE_AMBIGUOUS','source_basis']='T06-relevant implementation label exists but exact native item/page/routing binding was not sufficiently resolved from flattened authority; preserved as SOURCE_AMBIGUOUS rather than negative.'
A['source_binding_status']=D.source_binding_status
A['native_document_set_json']=D.native_document_set_json
A['norm_to_conduct_search_complete']=''
A['conduct_to_norm_search_complete']=''
A.loc[A.implementation_classification=='NORM_SHORE','norm_to_conduct_search_complete']='TRUE'
A.loc[A.implementation_classification=='CONDUCT_SHORE','conduct_to_norm_search_complete']='TRUE'
A['plausible_crosswalk_review_count']='0'
A['accounting_confidence']=A.implementation_classification.map({'NORM_SHORE':'MEDIUM','CONDUCT_SHORE':'MEDIUM','OTHER':'MEDIUM','SOURCE_AMBIGUOUS':'MEDIUM'})
A['accounting_note']='Source-first wave reconstruction; classification is a recall/search aid, not relation authority.'
acc_cols=['question_implementation_id','source_family','wave','source_variable_code','source_row_index','exact_question_text','substantive_implementation','implementation_classification','action_signature_json','source_battery_or_stem','source_basis','source_binding_status','native_document_set_json','explicit_source_relative_path','explicit_source_page','existing_governed_r11_source_object_ids_json','norm_to_conduct_search_complete','conduct_to_norm_search_complete','plausible_crosswalk_review_count','accounting_confidence','accounting_note']
A=A[acc_cols]

# Build source-first positive table under R16F schema contract.
schema=pd.read_csv('/mnt/data/t06w04_source_first/schema_only/CENTRAL_POSITIVE_S14_RELATION_AUTHORITY_R16F.csv',nrows=0).columns.tolist()
P=[]; X=[]
for fam,w,norms,conds,common,actor,target,action,condition,basis,grain in base_specs:
    key=f'{fam}|{w}|{",".join(norms)}|{",".join(conds)}'; wr=hid('T06W04-T06-',key,n=16)
    roles=[]; impls=[]
    for c in norms+conds:
        rr=row(fam,w,c); impls.append(rr.question_implementation_id); ex,prov=native_evidence(fam,w,c)
        role='RR_NORM' if c in norms else ('RR_STATED_OR_INTENDED_CONDUCT' if (fam=='Asian Barometer' and c=='q107') else 'RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT')
        roles.append({'implementation_id':rr.question_implementation_id,'semantic_unit_id':'','source_variable_code':c,'relation_role':role,'exact_question_text':rr.exact_question_text,'native_source_text':ex,'source_provenance':prov,'actor':actor,'action':action,'target':target,'modality':'normative source shore' if c in norms else 'source-proven conduct/expected/exposure endpoint','condition':condition,'respondent_universe':'preserve native wave/item routing'})
    rec={c:'' for c in schema}; rec.update({'index':str(len(P)),'central_relation_id':'T06SF-'+wr,'authority_class':'SOURCE_FIRST_ACCEPTED_T06_T06W04','rule_id':'T06','relation_type':'NORM_CONDUCT_ALIGNMENT','source_family':fam,'wave':w,'active_source_wave_set_json':jd([f'{fam}::{w}']),'member_semantic_unit_ids_json':'[]','member_implementation_ids_json':jd(impls),'role_assignments_json':jd(roles),'common_proposition_or_target':common,'actor_scope':actor,'target_scope':target,'action_domain':action,'position_or_routing_condition':condition,'central_basis':basis,'confidence':'HIGH','worker_origin':'T06W04','worker_relation_id':wr,'grain_note':grain,'r16f_freeze_status':'','r16f_freeze_basis':''}); P.append(rec)
    X.append({'review_id':hid('T06W04-XW-',key,n=18),'source_family':fam,'wave':w,'norm_source_variable_codes_json':jd(norms),'conduct_source_variable_codes_json':jd(conds),'norm_implementation_ids_json':jd([row(fam,w,c).question_implementation_id for c in norms]),'conduct_implementation_ids_json':jd([row(fam,w,c).question_implementation_id for c in conds]),'disposition':'POSITIVE_T06','linked_positive_worker_relation_id':wr,'bidirectional_search_status':'BIDIRECTIONAL_COMPLETE','source_first_adjudication_basis':basis,'source_proven_mismatch_dimension':'','blocker_code':'','confidence':'HIGH'})
P=pd.DataFrame(P,columns=schema)
X=pd.DataFrame(X,columns=['review_id','source_family','wave','norm_source_variable_codes_json','conduct_source_variable_codes_json','norm_implementation_ids_json','conduct_implementation_ids_json','disposition','linked_positive_worker_relation_id','bidirectional_search_status','source_first_adjudication_basis','source_proven_mismatch_dimension','blocker_code','confidence'])
# initial repairs for source-proven endpoints that current O08 does not represent.
U=[]
for _,pr in P.iterrows():
    roles=json.loads(pr.role_assignments_json)
    for ro in roles:
        if ro['relation_role']=='RR_NORM': continue
        rr=D[D.question_implementation_id==ro['implementation_id']].iloc[0]
        if rr.current_o08_position_lane_DIAGNOSTIC_ONLY=='NOT_POSITION':
            key=rr.question_implementation_id+'|endpoint';
            U.append({'repair_id':hid('T06W04-REPAIR-',key,n=18),'source_family':pr.source_family,'wave':pr.wave,'source_variable_code':ro['source_variable_code'],'question_implementation_id':ro['implementation_id'],'repair_type':'T06_CONDUCT_ENDPOINT_BRIDGE_MISSING','current_metadata_state':'current_o08_position_lane_DIAGNOSTIC_ONLY=NOT_POSITION','source_proven_fact':ro['native_source_text']+' | '+ro['source_provenance'],'required_upstream_fix':'Install/bridge the source-proven T06 endpoint role; preserve current O08 lane as diagnostic rather than treating NOT_POSITION as source absence.','related_worker_relation_ids_json':jd([pr.worker_relation_id]),'confidence':'HIGH'})
U=pd.DataFrame(U,columns=['repair_id','source_family','wave','source_variable_code','question_implementation_id','repair_type','current_metadata_state','source_proven_fact','required_upstream_fix','related_worker_relation_ids_json','confidence']).drop_duplicates('repair_id')
C=pd.DataFrame(columns=['defect_id','source_family','wave','native_source_structure','missing_shore','native_source_text','source_provenance','selected_universe_check','required_repair','confidence'])
B=pd.DataFrame(columns=['blocker_id','source_family','wave','blocker_code','affected_crosswalk_review_id','affected_implementation_ids_json','source_basis','required_resolution','confidence'])
ATT=pd.DataFrame(columns=['source_family','wave','total_implementations','substantive_implementations_accounted','norm_shore_count','conduct_shore_count','other_count','source_ambiguous_count','bidirectional_crosswalk_completion','positive_t06_count','blocked_candidate_count','source_proven_mismatch_count','source_coverage_defect_count','unresolved_source_count','zero_t06_currently_supportable','parallel_battery_reconstruction_note','hostile_qa_result'])
A.to_csv(R/'T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv',index=False); P.to_csv(R/'T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',index=False); X.to_csv(R/'T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv',index=False); U.to_csv(R/'T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv',index=False); C.to_csv(R/'T06_SOURCE_COVERAGE_DEFECTS.csv',index=False); B.to_csv(R/'T06_SOURCE_FIRST_BLOCKERS.csv',index=False); ATT.to_csv(R/'T06_WAVE_COMPLETENESS_ATTESTATION.csv',index=False)
(ROOT/'00_WORKER_SCOPE.md').write_text('# T06W04\n\nSource-first T06 reconstruction for GSS 2002; Arab Barometer VIII; EVS 2008; EVS 1990; Asian Barometer W5; South Asia W1. R15/C4/R16D candidate universes are non-authoritative and were not used for discovery.\n',encoding='utf-8')
print('BASE',len(A),len(P),len(X),len(U))
print(A.groupby(['source_family','wave','implementation_classification']).size().to_string())
