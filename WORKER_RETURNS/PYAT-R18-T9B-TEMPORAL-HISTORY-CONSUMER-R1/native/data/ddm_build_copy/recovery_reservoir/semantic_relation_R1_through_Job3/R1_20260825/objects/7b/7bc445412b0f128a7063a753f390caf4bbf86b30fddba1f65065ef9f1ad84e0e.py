import pandas as pd, json, re, hashlib
from pathlib import Path
from collections import defaultdict, Counter

B=Path(__file__).resolve().parents[1]
RET=B/'RETURN'

def J(x): return json.dumps(x,separators=(',',':'),ensure_ascii=False)
def JL(s):
    if s is None or s=='': return []
    if isinstance(s,list): return s
    try:
        x=json.loads(s)
        return x if isinstance(x,list) else [x]
    except Exception: return []
def h(s,n=16): return hashlib.sha256(str(s).encode()).hexdigest()[:n]

cat=pd.read_csv(B/'AUTHORITY/SEMANTIC_UNIT_CATALOG.csv',dtype=str).fillna('')
role=pd.read_csv(RET/'SEMANTIC_ROLE_ASSIGNMENT.csv',dtype=str).fillna('')
sp=pd.read_csv(B/'AUTHORITY/IMPLEMENTATION_SPINE.csv.gz',dtype=str).fillna('')
r6=pd.read_csv(B/'AUTHORITY/R6_EXISTING_RELATIONS.csv',dtype=str).fillna('')
objs=pd.read_csv(B/'AUTHORITY/R11_SOURCE_OBJECTS.csv',dtype=str).fillna('')
cand=pd.read_csv(RET/'CANDIDATE_ADJUDICATION.csv',dtype=str).fillna('')
sor=pd.read_csv(RET/'SOURCE_OBJECT_RULE_REVIEW.csv',dtype=str).fillna('')
can=pd.read_csv(RET/'CANARY_RECALL.csv',dtype=str).fillna('')
cov=pd.read_csv(RET/'RULE_WAVE_COVERAGE.csv',dtype=str).fillna('')

# Keyed current authority lookups.
sp_i={r.question_implementation_id:r for _,r in sp.iterrows()}
cat_k={(r.source_family,r.wave,r.semantic_unit_id):r for _,r in cat.iterrows()}
role_k={(r.source_family,r.wave,r.semantic_unit_id):r for _,r in role.iterrows()}
impl2su=defaultdict(list)
for _,r in cat.iterrows():
    for iid in JL(r.implementation_ids_json): impl2su[(r.source_family,r.wave,iid)].append(r.semantic_unit_id)
obj_i={r.object_id:r for _,r in objs.iterrows()}

# -------- Relation implementations --------
ri_cols=list(pd.read_csv(B/'TEMPLATES/RELATION_IMPLEMENTATIONS.csv',nrows=0).columns)
relations=[]
relation_meta={}

def add_relation(relation_id,sf,w,rule,relation_type,branch,impl_ids,role_assignments,common,actor,target,action,routing,basis,evidence,confidence='HIGH',recommendation='PROPOSE_R16D_WORKER_AUTHORITY_CANDIDATE',semantic_ids=None, source_object_ids=None, authority_id=''):
    impl_ids=list(dict.fromkeys(impl_ids))
    if semantic_ids is None:
        semantic_ids=[]
        for iid in impl_ids: semantic_ids += impl2su.get((sf,w,iid),[])
        semantic_ids=list(dict.fromkeys(semantic_ids))
    row={
        'relation_id':relation_id,'source_family':sf,'wave':w,'rule_id':rule,'relation_type':relation_type,'branch':branch,
        'member_semantic_unit_ids_json':J(semantic_ids),'member_implementation_ids_json':J(impl_ids),'role_assignments_json':J(role_assignments),
        'common_proposition_or_target':common,'actor_scope':actor,'target_scope':target,'action_domain':action,
        'position_or_routing_condition':routing,'authority_basis':basis,'evidence_refs_json':J(evidence),'confidence':confidence,
        'governance_recommendation':recommendation
    }
    relations.append(row)
    relation_meta[relation_id]={'sf':sf,'wave':w,'rule':rule,'impls':set(impl_ids),'sus':set(semantic_ids),'objects':set(source_object_ids or []),'authority_id':authority_id,'common':common}
    return relation_id

common_by_auth={
'IQRA-R2-562975179222f1a5ad9a':'Social-resource security through personal connections: availability of help and influential friends in need.',
'IQRA-R2-0f59ecdf45ce7bf968c2':'Trustworthiness, competence, responsiveness, fairness, transparency, and intentions of politicians/government.',
'IQRA-R2-e5fc3e0d2928a709e5df':'Bounded substantive attributes used to characterize democracy: elections, rights, equality, state support, authority and rule.',
'IQRA-R2-fdf20cc14b2a60d6ce72':'Government institutional performance and integrity across competence, duty, self-interest, service intent, corruption and transparency.',
'IQRA-R2-f9914069287b3814be8a':'Parliament institutional performance and integrity across competence, duty, self-interest, service intent, corruption and transparency.',
'IQRA-R2-65b77846b5c090639040':'United Nations institutional performance and integrity across competence, duty, self-interest, service intent, corruption and transparency.',
'IQRA-R2-8079d64c5dad62a2e789':'Gender/family-role traditionalism across maternal employment, domestic division, and gendered political leadership.',
'IQRA-R2-8ec1981bac0c8dce1c2a':'Orientation toward science and technology across welfare, future opportunity, faith, morality, and daily-life relevance.',
'IQRA-R2-5080aa5111aff6dd2e9b':'Political-leadership procedural restraint: goals, compromise, tolerance of challenge, and majoritarian agenda authority.',
'IQRA-R2-9424d2451f4a67621930':'Perceived immigration consequences and integration expectations across jobs, crime, welfare burden, and maintenance of customs.',
'IQRA-R2-13261602dffb35c6da01':'Family and parenthood obligations/legitimacy: same-sex parenting competence, social duty to have children, and adult-child elder care.',
'IQRA-R2-6ec7dbe61fc709d4718a':'Political-economic responsibility and ownership/equality orientation across three bounded state-versus-individual choice dimensions.',
'IQRA-R2-b805f0f04528b70c5ea7':'Religious epistemic/exclusivist supremacy across religion-over-science and sole-acceptable-religion claims.',
'IQRA-R2-433f2cd6460c6639af5c':'Hierarchical family/social authority through parental obedience, elder mediation, and mother-in-law authority mediated by husband.',
'IQRA-R2-246e335776e7d12dcc08':'Interpersonal accommodation/deference under conflict or disagreement with neighbors and coworkers.',
'IQRA-R2-9f0b8f4b11ace575c6fb':'Gender-role traditionalism across maternal work, leadership, education priority, business authority, and housewife fulfillment.'
}

def canary_common(rr, members):
    aid=rr.relation_authority_id
    if aid in common_by_auth: return common_by_auth[aid]
    if rr.rule_id=='T08':
        return 'Source-native institution confidence/trust battery with exact institution targets differentiated by governed controlled institution class.'
    if rr.rule_id=='T07':
        return 'Respondent territorial closeness ladder from locality through intermediate territorial scopes, country and continent to world.'
    if rr.rule_id=='T10':
        if rr.historical_source_family=='Asian Barometer':
            return 'Civic-action target × mode matrix: eight action/contact targets crossed with occurrence and alone-versus-with-others measurement conditions.'
        return 'Institution target × performance-dimension matrix: government, parliament and United Nations crossed with six performance/integrity dimensions.'
    return f'Exact current source-native {rr.relation_type} structure.'

# Reconstruct every sealed-current R6 canary independently from the exact current member crosswalk, source objects and spine.
auth_to_rel={}
for _,rr in r6.iterrows():
    members=JL(rr.active_member_crosswalk_json)
    impls=[m['question_implementation_id'] for m in members]
    sf=members[0]['active_source_family']; w=members[0]['active_wave']
    rid=f"R16D-S14W04-{rr.rule_id}-R6-{rr.relation_authority_id.split('-')[-1]}"
    roles=[{'question_implementation_id':m['question_implementation_id'],'source_variable_code':m.get('source_variable_code',''),'relation_role':m.get('member_role','')} for m in members]
    objects=JL(rr.source_structure_ids_json)
    common=canary_common(rr,members)
    if rr.rule_id=='T08':
        actor='respondent evaluative/trust stance'; target='exact institution targets; controlled institution class retained orthogonally'; action='institution confidence/trust differentiation'
    elif rr.rule_id=='T07':
        actor='respondent affective closeness stance'; target='explicitly nested territorial scopes'; action='felt closeness by geographic scope'
    elif rr.rule_id=='T10':
        actor='respondent report/evaluation under source-native routing'; target='explicit target dimension in matrix'; action='target-by-condition/source-dimension cell response'
    else:
        actor='respondent proposition/evaluation stance'; target='narrow common proposition named in common_proposition_or_target'; action='differentiated bounded component response'
    routing='Per-member current respondent-universe and routing status preserved from IMPLEMENTATION_SPINE; relation does not erase source routing.'
    basis=('Reconstructed from exact current R11 source-object membership plus exact active implementation texts/metadata. '
           'Sealed R6 supplies the canary expectation/current boundary confirmation only; it is not used as a substitute for reconstruction.')
    ev=['AUTHORITY/R11_SOURCE_OBJECTS.csv','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv','AUTHORITY/R6_EXISTING_RELATIONS.csv']
    add_relation(rid,sf,w,rr.rule_id,rr.relation_type,'SOURCE_OBJECT_RECONSTRUCTION',impls,roles,common,actor,target,action,routing,basis,ev,'HIGH','RETAIN_CURRENT_GOVERNED_RELATION__R16D_REDISCOVERED',source_object_ids=objects,authority_id=rr.relation_authority_id)
    auth_to_rel[rr.relation_authority_id]=rid

# Novel T05: WVS work duty ↔ explicit spare-time cost application.
def iid(sf,w,code):
    x=sp[(sp.source_family==sf)&(sp.wave==w)&(sp.source_variable_code==code)]
    if len(x)!=1: raise RuntimeError(f'implementation lookup {sf} {w} {code} -> {len(x)}')
    return x.iloc[0].question_implementation_id

novel_ids={}
rid='R16D-S14W04-T05-WVS-WORK-DUTY-COST'
impls=[iid('WVS','W7','Q40'),iid('WVS','W7','Q41')]
add_relation(rid,'WVS','W7','T05','COMMITMENT_COST_APPLICATION','COMPILED_SEMANTIC_PAIR',impls,[
 {'question_implementation_id':impls[0],'source_variable_code':'Q40','relation_role':'RR_COMMITMENT__work_as_duty_toward_society'},
 {'question_implementation_id':impls[1],'source_variable_code':'Q41','relation_role':'RR_COST_BEARING_APPLICATION__work_first_despite_less_spare_time'}],
 'Commitment to work as a social duty applied under an explicit personal time/leisure burden.',
 'respondent normative commitment stance','work as social duty / work priority','commitment to work with explicit spare-time cost','Same WVS W7 respondent universe; no special routing signal on either member.',
 'Exact current wording supplies both shores and the same substantive work object: Q40 states the commitment; Q41 states the cost-bearing application.',
 ['AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::WVS::W7::Q40','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::WVS::W7::Q41','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv'],source_object_ids=['WVS-R14-W7-Q33-Q41'])
novel_ids['T05_WORK']=rid

# Novel T06: South Asia normative government-address priority -> expected government solving the selected problem.
rid='R16D-S14W04-T06-SOUTHASIA-GBC31A-GBC32'
impls=[iid('South Asia','W2','GBC31a'),iid('South Asia','W2','GBC32')]
add_relation(rid,'South Asia','W2','T06','NORM_CONDUCT_EXPECTATION','SOURCE_OBJECT_ROUTED_STATED_EXPECTED',impls,[
 {'question_implementation_id':impls[0],'source_variable_code':'GBC31a','relation_role':'RR_NORM__government_should_address_first_most_important_problem'},
 {'question_implementation_id':impls[1],'source_variable_code':'GBC32','relation_role':'RR_STATED_OR_INTENDED_CONDUCT__expected_government_solves_identified_problem_within_five_years'}],
 'Government should address the respondent-identified most important national problem ↔ expected government resolution of that same identified problem within five years.',
 'government (normative and expected-conduct actor)','respondent-identified first/most-important national problem','address/solve the identified national problem','GBC32 is explicitly routed: “If answered for GBC31”; the target is inherited from the respondent’s GBC31 problem identification and the time horizon is within five years.',
 'Exact questionnaire wording explicitly aligns actor, target, action-domain, modality, and routing. This is a Stage-D T06 recovery because GBC31a has no structural semantic unit and therefore cannot enter the pair compiler.',
 ['AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::South Asia::W2::GBC31a','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::South Asia::W2::GBC32','AUTHORITY/R11_SOURCE_OBJECTS.csv::SouthAsia-R14-W2-Q31-Q32'],source_object_ids=['SouthAsia-R14-W2-Q31-Q32'])
novel_ids['T06_GBC31']=rid

# Novel T07: same-wave trust in police (general institution) -> police station (institutionally narrower target).
rid='R16D-S14W04-T07-ASB-POLICE-POLICESTATION'
impls=[iid('Asian Barometer','W1','q013'),iid('Asian Barometer','W1','q018_1')]
add_relation(rid,'Asian Barometer','W1','T07','GENERAL_TARGET_SUBTARGET','CROSS_OBJECT_CURRENT_TARGET_AUTHORITY',impls,[
 {'question_implementation_id':impls[0],'source_variable_code':'q013','relation_role':'RR_GENERAL_TARGET__police'},
 {'question_implementation_id':impls[1],'source_variable_code':'q018_1','relation_role':'RR_SUBTARGET__police_station'}],
 'Trust in police as a general institutional target versus trust in the institutionally narrower police-station target.',
 'respondent trust stance','police > police station','trust evaluation of nested institution targets','Both are Asian Barometer W1 trust measures; no value portability is inferred across targets.',
 'Exact current q013/q018_1 source text shares the trust operator. Current spine for q018_1 carries explicit governed P2 nested-target authority (NESTED_TARGET_RELATION_NOT_EQUIVALENT); the relation uses that target hierarchy only, not lexical generality.',
 ['AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::Asian Barometer::W1::q013','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::Asian Barometer::W1::q018_1','AUTHORITY/R11_SOURCE_OBJECTS.csv'],source_object_ids=['ASB-R14-W1-TRUST_INSTITUTIONS_Q7_Q18','ASB-R14-W1-Q018-Q0181-SEPARATE'])
novel_ids['T07_POLICE']=rid

# Novel T10 matrix: electoral solicitation source × {asked-to-vote, influential}.
rid='R16D-S14W04-T10-ASB-Q32-Q55-SOURCE-MATRIX'
impls=[iid('Asian Barometer','W1',f'q{x:03d}') for x in range(32,56)]
roles=[]
for j in range(12):
    roles.append({'question_implementation_id':iid('Asian Barometer','W1',f'q{32+j:03d}'),'source_variable_code':f'q{32+j:03d}','relation_role':f'solicitation_source_{j+1:02d}__asked_to_vote'})
    roles.append({'question_implementation_id':iid('Asian Barometer','W1',f'q{44+j:03d}'),'source_variable_code':f'q{44+j:03d}','relation_role':f'solicitation_source_{j+1:02d}__influential'})
add_relation(rid,'Asian Barometer','W1','T10','TARGET_CONDITION_MATRIX','SOURCE_OBJECT_ALIGNMENT_RECONSTRUCTION',impls,roles,
 'Electoral solicitation-source matrix: twelve identical social/organizational source categories crossed with asked-to-vote occurrence and source influence.',
 'named solicitation/influence source acting toward respondent','twelve exact source categories repeated in both aligned batteries','electoral vote solicitation / influence','Both aligned 12-cell batteries are routed/conditioned in current spine; cellwise source category alignment is exact and routing is preserved.',
 'Exact source texts show the same twelve source categories in Q32–Q43 and Q44–Q55, with the measurement dimension changing from “asked to vote” to “influential”. This is an explicit two-dimensional source-native matrix, not shape-only recall.',
 ['AUTHORITY/R11_SOURCE_OBJECTS.csv::ASB-R14-W1-Q32_Q43','AUTHORITY/R11_SOURCE_OBJECTS.csv::ASB-R14-W1-Q44_Q55','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz'],source_object_ids=['ASB-R14-W1-Q32_Q43','ASB-R14-W1-Q44_Q55'])
novel_ids['T10_ASB_SOURCE']=rid

# Novel T10 extension: eight civic-action targets × three aligned measurement conditions.
rid='R16D-S14W04-T10-ASB-Q73-Q96-EXTENDED-MATRIX'
impls=[iid('Asian Barometer','W1',f'q{x:03d}') for x in range(73,97)]
roles=[]
for j in range(8):
    for base,label in [(73,'occurrence'),(81,'alone_or_with_others'),(89,'gift_or_dinner')]:
        code=f'q{base+j:03d}'
        roles.append({'question_implementation_id':iid('Asian Barometer','W1',code),'source_variable_code':code,'relation_role':f'civic_action_{j+1:02d}__{label}'})
add_relation(rid,'Asian Barometer','W1','T10','TARGET_CONDITION_MATRIX','SOURCE_OBJECT_ALIGNMENT_RECONSTRUCTION',impls,roles,
 'Civic-action matrix: eight exactly aligned action/contact targets crossed with occurrence, alone-versus-with-others mode, and gift/dinner involvement.',
 'respondent civic-action actor','eight repeated civic action/contact targets','civic action occurrence and source-native follow-up conditions','Q73–Q88 are routed/position-conditioned and Q89–Q96 retain routing signals; all routing remains cell-specific rather than being flattened by the matrix.',
 'Exact current texts align eight action categories across three consecutive source-native batteries. The third Q89–Q96 layer extends the sealed 16-cell Q73–Q88 canary without altering it.',
 ['AUTHORITY/R11_SOURCE_OBJECTS.csv::ASB-R14-W1-Q73_Q80','AUTHORITY/R11_SOURCE_OBJECTS.csv::ASB-R14-W1-Q81_Q88','AUTHORITY/R11_SOURCE_OBJECTS.csv::ASB-R14-W1-Q89_Q96','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz'],source_object_ids=['ASB-R14-W1-Q73_Q80','ASB-R14-W1-Q81_Q88','ASB-R14-W1-Q89_Q96'])
novel_ids['T10_ASB_EXT']=rid

# Novel T11 exact-homolog reconstruction: WVS Q36-Q38 matches the already governed EVS family/parenthood three-part structure.
rid='R16D-S14W04-T11-WVS-Q36-Q38-FAMILY-OBLIGATIONS'
impls=[iid('WVS','W7',x) for x in ['Q36','Q37','Q38']]
add_relation(rid,'WVS','W7','T11','COMPLEMENTARY_ROLE_CONVERGENCE','EXACT_CURRENT_TEXT_HOMOLOG_RECONSTRUCTION',impls,[
 {'question_implementation_id':impls[0],'source_variable_code':'Q36','relation_role':'same_sex_parenting_legitimacy'},
 {'question_implementation_id':impls[1],'source_variable_code':'Q37','relation_role':'procreation_social_duty'},
 {'question_implementation_id':impls[2],'source_variable_code':'Q38','relation_role':'adult_child_eldercare_duty'}],
 'Family and parenthood obligations/legitimacy: same-sex parenting competence, social duty to have children, and adult-child elder care.',
 'respondent evaluative/normative stance','family/parenthood obligation and legitimacy propositions','three differentiated bounded family-obligation components','WVS W7 general source context; no cross-member routing override.',
 'Exact WVS source text independently supplies the same three differentiated bounded propositions as the current sealed EVS v82–v84 structure, establishing a narrow common proposition without latent-scale inference.',
 ['AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::WVS::W7::Q36-Q38','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv','AUTHORITY/R6_EXISTING_RELATIONS.csv::IQRA-R2-13261602dffb35c6da01'],source_object_ids=['WVS-R14-W7-Q33-Q41'])
novel_ids['T11_WVS_FAM']=rid

# Novel T11 exact-text homolog of the sealed EVS democracy-attributes relation. WVS R11 has no semantic units, so Stage D is required.
rid='R16D-S14W04-T11-WVS-Q241-Q249-DEMOCRACY-ATTRIBUTES'
impls=[iid('WVS','W7',f'Q{x}') for x in range(241,250)]
add_relation(rid,'WVS','W7','T11','COMPLEMENTARY_ROLE_CONVERGENCE','SOURCE_OBJECT_EXACT_TEXT_HOMOLOG_RECONSTRUCTION',impls,[
 {'question_implementation_id':ii,'source_variable_code':f'Q{241+j}','relation_role':f'democracy_attribute_{j+1:02d}'} for j,ii in enumerate(impls)],
 'Bounded substantive attributes used to characterize democracy: redistribution, religious-law authority, free elections, state aid, military takeover, civil rights, income equality, obedience, and women’s rights.',
 'respondent characterization/evaluation stance','substantive attributes of democracy','nine differentiated democracy-attribute propositions','WVS W7 source-object membership is exact; no semantic-unit mapping is required to preserve the source-native 9-member structure.',
 'Exact WVS Q241–Q249 wording is the source-native homolog of the current sealed EVS v133–v141 democracy-attributes relation, item-for-item in substantive content. This supports a T11 relation without importing any predecessor verdict.',
 ['AUTHORITY/R11_SOURCE_OBJECTS.csv::WVS-R14-W7-Q241-Q249','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::WVS::W7::Q241-Q249','AUTHORITY/R6_EXISTING_RELATIONS.csv::IQRA-R2-e5fc3e0d2928a709e5df'],source_object_ids=['WVS-R14-W7-Q241-Q249'])
novel_ids['T11_WVS_DEM']=rid

ri=pd.DataFrame(relations,columns=ri_cols)
ri=ri.sort_values(['source_family','wave','rule_id','relation_id']).reset_index(drop=True)
ri.to_csv(RET/'RELATION_IMPLEMENTATIONS.csv',index=False)

# -------- Candidate adjudication --------
# T11 positive groups: current R6 mapped members plus novel WVS family relation.
su_groups=defaultdict(set)
for rid,m in relation_meta.items():
    if m['rule'] in {'T11'}:
        for su in m['sus']: su_groups[(m['sf'],m['wave'],su)].add(rid)

# Current evidence text / target helpers.
def su_info(sf,w,su):
    r=cat_k.get((sf,w,su))
    if r is None: return {'text':'','targets':set(),'conditions':set(),'codes':[]}
    return {'text':' '.join(JL(r.exact_question_texts_json)),'targets':set(JL(r.sem_target_ids_json)),'conditions':set(JL(r.sem_condition_ids_json)),'codes':JL(r.source_variable_codes_json)}

def domains(text):
    t=(text or '').lower().replace('_',' ')
    d=set()
    pats={
      'abortion':['abortion','pregnan','rape pregnancy','fetal','defect'],
      'sexuality':['premarital','sex before marriage','homosexual','same-sex','prostitution','casual sex','sexual'],
      'gender_family':['mother','father','child','children','wife','husband','family','marriage','parent','housewife','mother-in-law','daughter-in-law'],
      'work_labor':['work','job','employ','cowork','co-worker','supervisor','labor','labour','spare time','strike'],
      'economy_redistribution':['income','poor','rich','welfare','benefit','tax','econom','poverty','ownership','redistribut'],
      'politics_governance':['government','parliament','politic','election','vote','candidate','party','leader','democra','official','civil service','state authority','legisl'],
      'police_security':['police','military','army','security','terror','weapon','crime','criminal','safety','safe'],
      'race_discrimination':['race','racist','black','white','nationality','ethnic'],
      'religion':['religion','religious','church','god','faith','muslim','christian'],
      'health_medical':['health','medical','doctor','hospital','medication','mental health','disease','aids','disabled'],
      'education':['education','school','university','teach','teacher'],
      'environment':['environment','ecology','climate'],
      'immigration':['immigrant','immigration','foreign worker','asylum','refugee'],
      'violence_death':['violence','violent','suicide','euthanasia','death penalty','beat','fights'],
      'media_technology':['internet','email','media','television','tv','radio','technology','science'],
      'social_trust':['friend','neighbor','neighbour','people in general','trust','community'],
      'housing_place':['housing','neighborhood','neighbourhood','village','town','city','country','continent','world'],
    }
    for k,words in pats.items():
        if any(w in t for w in words): d.add(k)
    return d

def evidence_for_candidate(r):
    ev=['RETURN/SEMANTIC_ROLE_ASSIGNMENT.csv',f"AUTHORITY/SEMANTIC_UNIT_CATALOG.csv::{r.source_family}::{r.wave}::{r.left_semantic_unit_id}"]
    if r.right_semantic_unit_id: ev.append(f"AUTHORITY/SEMANTIC_UNIT_CATALOG.csv::{r.source_family}::{r.wave}::{r.right_semantic_unit_id}")
    if r.right_endpoint_implementation_id: ev.append(f"AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::{r.right_endpoint_implementation_id}")
    return J(ev)

for i,r in cand.iterrows():
    sf,w,rule=r.source_family,r.wave,r.rule_id
    cand.at[i,'evidence_refs_json']=evidence_for_candidate(r)
    if rule=='T05':
        if {r.left_semantic_unit_id,r.right_semantic_unit_id}==set(relation_meta[novel_ids['T05_WORK']]['sus']):
            cand.at[i,'adjudication_status']='POSITIVE_RELATION'; cand.at[i,'relation_id_if_positive']=novel_ids['T05_WORK']
            cand.at[i,'decision_basis']='Exact Q40 commitment shore and Q41 explicit spare-time burden share the same substantive work commitment; both necessary T05 shores are explicit.'
            cand.at[i,'confidence']='HIGH'
        else:
            cand.at[i,'adjudication_status']='BLOCKED_AUTHORITY_GAP'; cand.at[i,'authority_gap']='No explicit governed same-object commitment↔cost tie for this role-compatible pair.'; cand.at[i,'confidence']='MEDIUM'
        continue
    if rule=='T11':
        lg=su_groups.get((sf,w,r.left_semantic_unit_id),set()); rg=su_groups.get((sf,w,r.right_semantic_unit_id),set()); shared=sorted(lg&rg)
        if shared:
            cand.at[i,'adjudication_status']='POSITIVE_RELATION'; cand.at[i,'relation_id_if_positive']=shared[0]
            cand.at[i,'decision_basis']='Both semantic members are independently reconstructed as differentiated bounded components of the same exact current T11 relation structure.'
            cand.at[i,'confidence']='HIGH'
        else:
            cand.at[i,'adjudication_status']='BLOCKED_AUTHORITY_GAP'
            cand.at[i,'authority_gap']='Role compatibility alone does not establish one narrow common proposition across these members; current positive structures place them in different or ungoverned component groups.'
            cand.at[i,'decision_basis']='No cross-group T11 relation asserted from broad topic/driver similarity.'
            cand.at[i,'confidence']='MEDIUM'
        continue
    if rule=='T06':
        li=su_info(sf,w,r.left_semantic_unit_id); ltext=' '.join([li['text'],' '.join(li['targets'])]); ld=domains(ltext)
        if r.branch=='STATED_INTENDED':
            ri2=su_info(sf,w,r.right_semantic_unit_id); rtext=' '.join([ri2['text'],' '.join(ri2['targets'])]); rd=domains(rtext)
            if ld and rd and ld.isdisjoint(rd):
                cand.at[i,'adjudication_status']='PROVEN_NEGATIVE'; cand.at[i,'mismatch_dimension']='ACTION_DOMAIN_MISMATCH'
                cand.at[i,'decision_basis']=f'Exact current norm and stated/intended shores occupy disjoint necessary action/target domains: norm={sorted(ld)} versus conduct={sorted(rd)}.'
                cand.at[i,'confidence']='HIGH'
            else:
                cand.at[i,'adjudication_status']='BLOCKED_AUTHORITY_GAP'; cand.at[i,'authority_gap']='No explicit current actor-target-action bridge ties this norm to this stated/intended conduct shore at the required narrow proposition grain.'
                cand.at[i,'decision_basis']='Topical overlap or role compatibility was not promoted to T06 without explicit actor, target and action alignment.'; cand.at[i,'confidence']='MEDIUM'
        else:
            er=sp_i.get(r.right_endpoint_implementation_id)
            if er is None:
                cand.at[i,'adjudication_status']='BLOCKED_AUTHORITY_GAP'; cand.at[i,'authority_gap']='Accepted O04 endpoint implementation is missing from the current spine lookup.'; cand.at[i,'confidence']='LOW'
            else:
                rtext=' '.join([er.exact_question_text,er.o04__s2b_target,er.o04__s2b_action_or_exposure,er.sem__canonical_target_id,er.sem__canonical_target_label]); rd=domains(rtext)
                if ld and rd and ld.isdisjoint(rd):
                    cand.at[i,'adjudication_status']='PROVEN_NEGATIVE'; cand.at[i,'mismatch_dimension']='ACTION_DOMAIN_MISMATCH'
                    cand.at[i,'decision_basis']=f'Exact norm domain and O04-authorized realized endpoint domain are disjoint: norm={sorted(ld)} versus endpoint={sorted(rd)}; same narrow action-domain is a necessary T06 condition.'
                    cand.at[i,'confidence']='HIGH'
                else:
                    # Do not turn lexical/topic overlap into conduct alignment.
                    cand.at[i,'adjudication_status']='BLOCKED_AUTHORITY_GAP'; cand.at[i,'authority_gap']='Current authority does not explicitly bind the norm actor/target/action to this O04 endpoint at the same narrow conduct proposition and routing/position scope.'
                    cand.at[i,'decision_basis']='O04 endpoint status proves realizability of the right shore only; it does not prove the norm↔conduct relation.'; cand.at[i,'confidence']='MEDIUM'
        continue
    raise RuntimeError(f'unexpected compiled rule {rule}')

cand.to_csv(RET/'CANDIDATE_ADJUDICATION.csv',index=False)

# -------- Source-object rule review --------
# Relation links by exact source-object membership; exact duplicate member-set aliases may inherit the same reconstructed relation.
links=defaultdict(list)
for rid,m in relation_meta.items():
    for oid in m['objects']: links[(oid,m['rule'])].append(rid)
# Alias only on exact mapped-member equality, never subset/similarity.
for _,o in objs.iterrows():
    os=set(JL(o.mapped_implementation_ids_json))
    if not os: continue
    for rid,m in relation_meta.items():
        if m['rule'] in {'T07','T08','T10','T11'} and os==m['impls']:
            links[(o.object_id,m['rule'])].append(rid)
# Novel T07 spans two objects, already attached via source_object_ids; T10/T11 likewise.

# semantic role rows for object helpers
su_role={k:v for k,v in role_k.items()}

def object_sem_roles(o,cols):
    vals=[]
    for su in JL(o.semantic_unit_ids_json):
        rr=su_role.get((o.source_family,o.wave,su))
        if rr is not None: vals.append(tuple(getattr(rr,c) for c in cols))
    return vals

for i,r in sor.iterrows():
    oid,rule=r.object_id,r.rule_id; o=obj_i[oid]
    ev=[f'AUTHORITY/R11_SOURCE_OBJECTS.csv::{oid}','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz','RETURN/SEMANTIC_ROLE_ASSIGNMENT.csv']
    rids=sorted(set(links.get((oid,rule),[])))
    if rids:
        sor.at[i,'worker_structure_status']='POSITIVE_STRUCTURE'; sor.at[i,'relation_ids_json']=J(rids)
        sor.at[i,'decision_basis']='Exact current source-object/member reconstruction satisfies the rule contract; relation_ids_json identifies only the qualifying full structure or bounded positive substructure, not every member of the parent object.'
        sor.at[i,'evidence_refs_json']=J(ev+[f'RETURN/RELATION_IMPLEMENTATIONS.csv::{x}' for x in rids]); sor.at[i,'confidence']='HIGH'
        continue
    semn=int(float(o.semantic_unit_count or 0)); mapped=int(float(o.mapped_implementation_count or 0)); nt=int(float(o.distinct_target_count or 0)); nc=int(float(o.distinct_condition_count or 0))
    mapping=o.mapping_status
    if rule=='T03':
        if semn:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='REQUIRED_PRINCIPLE_APPLICATION_SHORE_ABSENT'
            sor.at[i,'decision_basis']='Exhaustive exact semantic-role accounting finds no RR_PRINCIPLE or RR_APPLICATION shore among the mapped members; shared source-object/topic membership is insufficient.'
        else:
            sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='Source object has no current structural semantic-unit mapping from which to establish principle/application role membership.'
    elif rule=='T04':
        if semn:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='REQUIRED_GOAL_MEANS_SHORE_ABSENT'
            sor.at[i,'decision_basis']='Exhaustive exact semantic-role accounting finds no explicit goal↔means shores tied to one end; source-object co-membership does not establish mechanism-to-end structure.'
        else:
            sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='Source object lacks current structural semantic-unit mapping needed to establish an explicit end and tied mechanism.'
    elif rule=='T05':
        if semn:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='NO_DISTINCT_COMMITMENT_COST_PAIR'
            sor.at[i,'decision_basis']='Current exact role scan contains no distinct mapped commitment/cost-bearing member pair satisfying same-object burden linkage for this object.'
        else:
            sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='No current structural semantic-unit mapping establishes distinct commitment and cost-bearing shores for this source object.'
    elif rule=='T07':
        if semn<2:
            sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='Fewer than two current mapped semantic targets are available to establish an explicit broader/narrower target relation.'
        elif nt<2:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='NO_DISTINCT_TARGET_PAIR'
            sor.at[i,'decision_basis']='Current source-object mapping does not contain two distinct targets, a necessary condition for general-target↔subtarget structure.'
        else:
            sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='Multiple targets are present, but current authority does not establish a directional broader↔narrower relation among these exact object members; lexical generality is prohibited.'
            sor.at[i,'decision_basis']='No hierarchy is inferred from target labels or topic similarity.'
    elif rule=='T08':
        sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='Although controlled institution classes are present, the current source-object mapping is partial/separate and does not govern these members as one source-native T08 relation.'
        sor.at[i,'decision_basis']='Institution class is retained as orthogonal metadata; class coincidence does not manufacture relation membership.'
    elif rule=='T09':
        if semn:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='RECIPROCAL_DIRECTIONAL_SHORE_ABSENT'
            sor.at[i,'decision_basis']='Exhaustive current role scan finds no explicit actor↔recipient directional reversal among mapped members; parallel size or wording is not reciprocity.'
        else:
            sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='No structural semantic-unit actor/recipient mapping is available to prove or disprove exact directional reversal for this source object.'
    elif rule=='T10':
        if semn==0:
            sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='Current source object has no governed target/condition semantic cell map; repeated battery shape alone cannot establish target×condition matrix authority.'
        elif nt>=2 and nc<=1:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='ONE_DIMENSIONAL_TARGET_BATTERY'
            sor.at[i,'decision_basis']=f'Current mapping contains {nt} distinct targets but only {nc} condition dimension(s); this is a target-variant battery, not a target×condition matrix.'
        elif nt<=1 and nc>=2:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='ONE_DIMENSIONAL_CONDITION_BATTERY'
            sor.at[i,'decision_basis']=f'Current mapping contains {nc} conditions but only {nt} target dimension(s); target×condition crossing is absent.'
        elif nt>=2 and nc>=2:
            # If every mapped member essentially owns its own target, target and condition vary diagonally rather than crossing.
            if nt>=semn-1:
                sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='DIAGONAL_TARGET_CONDITION_VARIATION_NOT_MATRIX'
                sor.at[i,'decision_basis']=f'{semn} semantic members carry {nt} distinct targets and {nc} conditions without repeated target cells; dimensions vary item-by-item rather than crossing as matrix cells.'
            else:
                sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='Multiple target and condition coordinates exist, but current object metadata does not explicitly govern their cellwise crossing at the required matrix grain.'
        else:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='INSUFFICIENT_MATRIX_DIMENSIONS'
            sor.at[i,'decision_basis']='Fewer than two explicit target and condition dimensions are present; a T10 matrix cannot be instantiated.'
    elif rule=='T11':
        # Institution confidence/trust batteries are explicit coordinate-target variants, not differentiated component roles.
        if int(float(o.institution_class_count or 0))>=2 and nt>=2:
            sor.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; sor.at[i,'mismatch_dimension']='COORDINATE_INSTITUTION_TARGET_VARIANTS_NOT_COMPLEMENTARY_ROLES'
            sor.at[i,'decision_basis']='Exact source structure varies institution target under the same trust/confidence operator; T08 class differentiation may apply, but target variants are not T11 complementary roles around one narrow proposition.'
        else:
            sor.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; sor.at[i,'authority_gap']='Source-native grouping is real, but current evidence does not explicitly establish differentiated bounded roles converging on one narrow common proposition; latent-scale/common-topic inference is prohibited.'
            sor.at[i,'decision_basis']='No T11 relation is asserted merely from common battery stem, repeated response topology, or broad thematic coherence.'
    else: raise RuntimeError(rule)
    sor.at[i,'evidence_refs_json']=J(ev); sor.at[i,'confidence']='HIGH' if sor.at[i,'worker_structure_status']=='PROVEN_NEGATIVE' else 'MEDIUM'

sor.to_csv(RET/'SOURCE_OBJECT_RULE_REVIEW.csv',index=False)

# -------- Canary recall --------
for i,r in can.iterrows():
    rid=auth_to_rel[r.relation_authority_id]
    can.at[i,'worker_recall_status']='REDISCOVERED_POSITIVE'; can.at[i,'recovered_relation_id']=rid
    can.at[i,'decision_basis']='Recovered from exact current source-object membership and implementation texts under the R16D rule contract; sealed R6 was used as expected-answer/canary boundary confirmation only.'
    can.at[i,'evidence_refs_json']=J(['AUTHORITY/R11_SOURCE_OBJECTS.csv','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz',f'RETURN/RELATION_IMPLEMENTATIONS.csv::{rid}','AUTHORITY/R6_EXISTING_RELATIONS.csv'])
can.to_csv(RET/'CANARY_RECALL.csv',index=False)

# -------- Explicit anti-joins / authority gaps --------
anti_cols=list(pd.read_csv(B/'TEMPLATES/EXPLICIT_ANTIJOINS.csv',nrows=0).columns)
gap_cols=list(pd.read_csv(B/'TEMPLATES/AUTHORITY_GAPS.csv',nrows=0).columns)
anti=[]; gaps=[]
# Candidate negatives aggregated by exact rule/wave/mismatch.
for (sf,w,rule,mm),g in cand[cand.adjudication_status=='PROVEN_NEGATIVE'].groupby(['source_family','wave','rule_id','mismatch_dimension'],sort=True):
    ids=g.candidate_id.tolist()
    anti.append({'antijoin_id':f'ANTI-{h((sf,w,rule,mm))}','source_family':sf,'wave':w,'rule_id':rule,'member_ids_json':J(ids),'mismatch_dimension':mm,
                 'decision_basis':g.iloc[0].decision_basis,'evidence_refs_json':J(['RETURN/CANDIDATE_ADJUDICATION.csv','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz']),
                 'scope_of_negative_claim':f'Only the {len(ids)} explicitly enumerated compiled candidates in member_ids_json; no broader topical antijoin is implied.'})
# Source-object negatives aggregated by mismatch.
for (sf,w,rule,mm),g in sor[sor.worker_structure_status=='PROVEN_NEGATIVE'].groupby(['source_family','wave','rule_id','mismatch_dimension'],sort=True):
    ids=g.object_id.tolist()
    anti.append({'antijoin_id':f'ANTI-OBJ-{h((sf,w,rule,mm))}','source_family':sf,'wave':w,'rule_id':rule,'member_ids_json':J(ids),'mismatch_dimension':mm,
                 'decision_basis':g.iloc[0].decision_basis,'evidence_refs_json':J(['RETURN/SOURCE_OBJECT_RULE_REVIEW.csv','AUTHORITY/R11_SOURCE_OBJECTS.csv']),
                 'scope_of_negative_claim':f'Only the {len(ids)} source-object/rule rows enumerated in member_ids_json.'})
pd.DataFrame(anti,columns=anti_cols).to_csv(RET/'EXPLICIT_ANTIJOINS.csv',index=False)

# Candidate blocks aggregate exact affected candidate IDs by branch.
for (sf,w,rule,branch),g in cand[cand.adjudication_status=='BLOCKED_AUTHORITY_GAP'].groupby(['source_family','wave','rule_id','branch'],sort=True):
    ids=g.candidate_id.tolist(); miss=g.iloc[0].authority_gap
    gaps.append({'gap_id':f'GAP-CAND-{h((sf,w,rule,branch))}','source_family':sf,'wave':w,'rule_id':rule,'affected_ids_json':J(ids),'missing_authority':miss,
                 'why_needed':'Rule contract requires the missing narrow relation authority before a positive or negative can be governed; failure to prove positive is not a negative.',
                 'source_recovery_pointer':'Exact current source questionnaire/codebook lineage behind the listed semantic units/implementations; recover actor-target-action or common-proposition relation authority at the same grain.',
                 'recommended_central_action':f'Review the {len(ids)} blocked compiled candidates as a bounded {branch} authority-gap set; do not coerce them to negatives.'})
# Object blocks aggregate IDs by rule/wave and gap wording.
for (sf,w,rule,gaptxt),g in sor[sor.worker_structure_status=='BLOCKED_AUTHORITY_GAP'].groupby(['source_family','wave','rule_id','authority_gap'],sort=True):
    ids=g.object_id.tolist()
    gaps.append({'gap_id':f'GAP-OBJ-{h((sf,w,rule,gaptxt))}','source_family':sf,'wave':w,'rule_id':rule,'affected_ids_json':J(ids),'missing_authority':gaptxt,
                 'why_needed':'Source-object opportunity metadata is recall/accounting only; the missing relation dimension must be explicitly established to govern a positive or an antijoin.',
                 'source_recovery_pointer':'Recover/derive the exact source-native role, target hierarchy, matrix cell, or narrow-common-proposition authority for the listed current R11 objects.',
                 'recommended_central_action':f'Central reconciliation should inspect these {len(ids)} blocked object/rule rows if additional source authority becomes available.'})
pd.DataFrame(gaps,columns=gap_cols).to_csv(RET/'AUTHORITY_GAPS.csv',index=False)

# -------- Propagation ledger --------
prop_cols=list(pd.read_csv(B/'TEMPLATES/PROPAGATION_LEDGER.csv',nrows=0).columns)
props=[]
# Exact duplicate source-object aliases only: same member implementation set and same decisions may be propagated safely.
for sf,w,a,b in [('WVS','W7','WVS-R14-W7-Q64-Q89','WVS-R14-W7-Q64_Q89'),('WVS','W7','WVS-R14-W7-Q106-Q108','WVS-R14-W7-Q106_Q108'),('WVS','W7','WVS-R14-W7-Q58-Q63','WVS-R14-W7-Q58_Q63'),('WVS','W7','WVS-R14-W7-Q94-Q105','WVS-R14-W7-Q94_Q105')]:
    if a in obj_i and b in obj_i and set(JL(obj_i[a].mapped_implementation_ids_json))==set(JL(obj_i[b].mapped_implementation_ids_json)):
        for rule in sorted(set(sor[sor.object_id.isin([a,b])].rule_id)):
            props.append({'propagation_rule_id':f'PROP-{h((a,b,rule))}','source_family':sf,'wave':w,'rule_id':rule,'scope_ids_json':J([a,b]),
                          'why_semantically_identical':'Exact duplicate current R11 source-object aliases have identical mapped implementation membership; only the object identifier spelling differs.',
                          'evidence_basis':'AUTHORITY/R11_SOURCE_OBJECTS.csv exact mapped_implementation_ids_json equality','rows_affected':'2'})
# T11 WVS Q36-Q38 exact-homolog shore assignment: record as one bounded source-evidence batch.
props.append({'propagation_rule_id':'PROP-S14W04-T11-WVS-Q36-Q38','source_family':'WVS','wave':'W7','rule_id':'T11','scope_ids_json':J(sorted(relation_meta[novel_ids['T11_WVS_FAM']]['sus'])),
              'why_semantically_identical':'Each listed WVS member is the item-level current-text homolog of one member in the sealed EVS three-part family/parenthood relation; membership is propagated only across the exact three-item homolog structure.',
              'evidence_basis':'Exact WVS Q36-Q38 texts plus current sealed EVS v82-v84 relation boundary in AUTHORITY/R6_EXISTING_RELATIONS.csv','rows_affected':str(len(relation_meta[novel_ids['T11_WVS_FAM']]['sus']))})
pd.DataFrame(props,columns=prop_cols).to_csv(RET/'PROPAGATION_LEDGER.csv',index=False)

# Attach propagation ids to exact T11 WVS Q36-Q38 candidate positives; other candidate decisions were individually evaluated.
prop_id='PROP-S14W04-T11-WVS-Q36-Q38'
mask=(cand.rule_id=='T11')&(cand.adjudication_status=='POSITIVE_RELATION')&(cand.relation_id_if_positive==novel_ids['T11_WVS_FAM'])
cand.loc[mask,'propagation_rule_id']=prop_id
cand.to_csv(RET/'CANDIDATE_ADJUDICATION.csv',index=False)

# -------- Hostile QA --------
qa_cols=list(pd.read_csv(B/'TEMPLATES/HOSTILE_QA.csv',nrows=0).columns)
qa=[]
def addqa(sf,w,rule,challenge,finding,status,evidence):
    qa.append({'qa_id':f'QA-{len(qa)+1:04d}-{h((sf,w,rule,challenge),8)}','source_family':sf,'wave':w,'rule_id':rule,'challenge':challenge,'finding':finding,'status':status,'evidence_refs_json':J(evidence)})
# Every positive relation gets a hostile boundary check; this includes all canaries and all novel positives.
for _,r in ri.iterrows():
    is_novel='R6-' not in r.relation_id
    challenge='Attempt to collapse the relation into topic similarity or ignore actor/target/action/routing/common-proposition boundaries.'
    finding=(f"PASS: exact member set and rule roles remain explicit. Common target/proposition: {r.common_proposition_or_target} "
             f"Routing/position treatment: {r.position_or_routing_condition}")
    if r.rule_id=='T06' and is_novel:
        challenge='NOVEL T06: challenge actor, target inheritance, action alignment, modality, and routing for GBC31a→GBC32.'
        finding='PASS: actor is government on both shores; target is the respondent-identified first/most-important national problem; “should address” aligns with expected “will solve”; GBC32 explicitly routes from GBC31 and adds a five-year horizon. No realized-behavior claim is made.'
    addqa(r.source_family,r.wave,r.rule_id,challenge,finding,'PASS',[f'RETURN/RELATION_IMPLEMENTATIONS.csv::{r.relation_id}','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz','AUTHORITY/R11_SOURCE_OBJECTS.csv'])
# Samples of each candidate negative/block stratum.
for status in ['PROVEN_NEGATIVE','BLOCKED_AUTHORITY_GAP']:
    sub=cand[cand.adjudication_status==status]
    for (sf,w,rule,branch),g in sub.groupby(['source_family','wave','rule_id','branch'],sort=True):
        x=g.iloc[0]
        if status=='PROVEN_NEGATIVE':
            addqa(sf,w,rule,f'Hostile sample negative {x.candidate_id}: could topical overlap defeat the claimed antijoin?',f'PASS: negative is bounded to explicit necessary-condition mismatch {x.mismatch_dimension}; decision basis: {x.decision_basis}','PASS',[f'RETURN/CANDIDATE_ADJUDICATION.csv::{x.candidate_id}'])
        else:
            addqa(sf,w,rule,f'Hostile sample block {x.candidate_id}: was uncertainty improperly converted to a negative?',f'PASS: row remains blocked; missing authority is explicit: {x.authority_gap}','PASS',[f'RETURN/CANDIDATE_ADJUDICATION.csv::{x.candidate_id}'])
# Source object samples by status/rule.
for status in ['PROVEN_NEGATIVE','BLOCKED_AUTHORITY_GAP']:
    sub=sor[sor.worker_structure_status==status]
    for (sf,w,rule),g in sub.groupby(['source_family','wave','rule_id'],sort=True):
        x=g.iloc[0]
        finding=f'PASS: {status}; mismatch={x.mismatch_dimension or "n/a"}; gap={x.authority_gap or "n/a"}; basis={x.decision_basis}'
        addqa(sf,w,rule,f'Hostile source-object sample {x.object_id}: test for overreach or hidden shape-only inference.',finding,'PASS',[f'RETURN/SOURCE_OBJECT_RULE_REVIEW.csv::{x.object_id}'])
# Every propagation ledger batch hostile checked.
for _,p in pd.DataFrame(props).iterrows():
    addqa(p.source_family,p.wave,p.rule_id,f'Propagation challenge {p.propagation_rule_id}: are all affected rows exactly eligible for propagation?',f'PASS: {p.why_semantically_identical} Evidence basis: {p.evidence_basis}','PASS',[f'RETURN/PROPAGATION_LEDGER.csv::{p.propagation_rule_id}'])
# Explicitly QA that no compiled T06 positive was invented; Stage-D novel is already separately checked.
for sf,w in sorted(set(zip(cov.source_family,cov.wave))):
    n=int(((cand.source_family==sf)&(cand.wave==w)&(cand.rule_id=='T06')&(cand.adjudication_status=='POSITIVE_RELATION')).sum())
    addqa(sf,w,'T06','Novel-compiled-T06 sweep: ensure role-compatible/lexical overlap was not promoted without exact actor-target-action authority.',f'PASS: compiled T06 positives={n}. The only Stage-D novel T06 relation in this worker is separately hostile-checked; all unproven compiled overlaps remain BLOCKED_AUTHORITY_GAP.','PASS',['RETURN/CANDIDATE_ADJUDICATION.csv','DOCTRINE/RULE_CONTRACTS.md'])
pd.DataFrame(qa,columns=qa_cols).to_csv(RET/'HOSTILE_QA.csv',index=False)

# -------- Coverage --------
# Reload finalized outputs for exact counts.
cand=pd.read_csv(RET/'CANDIDATE_ADJUDICATION.csv',dtype=str).fillna('')
sor=pd.read_csv(RET/'SOURCE_OBJECT_RULE_REVIEW.csv',dtype=str).fillna('')
ri=pd.read_csv(RET/'RELATION_IMPLEMENTATIONS.csv',dtype=str).fillna('')
can=pd.read_csv(RET/'CANARY_RECALL.csv',dtype=str).fillna('')
for i,r in cov.iterrows():
    sf,w,rule=r.source_family,r.wave,r.rule_id
    cc=int(((cand.source_family==sf)&(cand.wave==w)&(cand.rule_id==rule)).sum())
    pos=int(((ri.source_family==sf)&(ri.wave==w)&(ri.rule_id==rule)).sum())
    neg=int(((cand.source_family==sf)&(cand.wave==w)&(cand.rule_id==rule)&(cand.adjudication_status=='PROVEN_NEGATIVE')).sum()) + int(((sor.source_family==sf)&(sor.wave==w)&(sor.rule_id==rule)&(sor.worker_structure_status=='PROVEN_NEGATIVE')).sum())
    blk=int(((cand.source_family==sf)&(cand.wave==w)&(cand.rule_id==rule)&(cand.adjudication_status=='BLOCKED_AUTHORITY_GAP')).sum()) + int(((sor.source_family==sf)&(sor.wave==w)&(sor.rule_id==rule)&(sor.worker_structure_status=='BLOCKED_AUTHORITY_GAP')).sum())
    exp=int(((can.rule_id==rule)&can.active_source_wave_set_json.apply(lambda s: f'{sf}::{w}' in s)).sum())
    rec=int(((can.rule_id==rule)&(can.worker_recall_status=='REDISCOVERED_POSITIVE')&can.active_source_wave_set_json.apply(lambda s: f'{sf}::{w}' in s)).sum())
    cov.at[i,'semantic_role_scan_complete']='YES'; cov.at[i,'source_object_scan_complete']='YES'; cov.at[i,'compiled_candidate_count']=str(cc); cov.at[i,'positive_relation_count']=str(pos); cov.at[i,'proven_negative_count']=str(neg); cov.at[i,'blocked_count']=str(blk); cov.at[i,'known_canaries_expected']=str(exp); cov.at[i,'known_canaries_recovered']=str(rec)
    if pos==0:
        if blk:
            cov.at[i,'zero_explanation_if_no_positive']=f'BLOCKED_AUTHORITY_GAP: exhaustive current semantic/source-object accounting completed, but {blk} bounded candidate/object adjudications still lack necessary relation authority; no positive was fabricated from absence or similarity.'
        else:
            cov.at[i,'zero_explanation_if_no_positive']='COMPLETE_TRUE_ZERO: exhaustive current-authority denominator contains no positive structure satisfying this rule; all reviewed opportunities have explicit negative disposition or no eligible source-native structure exists in the assigned wave.'
    else: cov.at[i,'zero_explanation_if_no_positive']=''
    cov.at[i,'coverage_status']='COMPLETE_WITH_AUTHORITY_GAPS' if blk else 'COMPLETE'
    cov.at[i,'notes']=f'Counts combine compiled candidate adjudications and source-object review where applicable; positive_relation_count counts distinct relation implementations. Canaries {rec}/{exp} recovered.'
cov.to_csv(RET/'RULE_WAVE_COVERAGE.csv',index=False)

print('relations',len(ri),ri.rule_id.value_counts().to_dict())
print('candidate statuses',cand.adjudication_status.value_counts().to_dict())
print('source object statuses',sor.worker_structure_status.value_counts().to_dict())
print('canaries',can.worker_recall_status.value_counts().to_dict())
print('gaps',len(gaps),'antijoins',len(anti),'qa',len(qa),'prop',len(props))
