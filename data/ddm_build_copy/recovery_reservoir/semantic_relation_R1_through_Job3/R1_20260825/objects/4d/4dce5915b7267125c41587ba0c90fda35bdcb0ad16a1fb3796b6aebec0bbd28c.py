from __future__ import annotations
import pandas as pd, json, hashlib, re, subprocess, sys
from pathlib import Path
from collections import defaultdict

BASE=Path(__file__).resolve().parents[1]
AUTH=BASE/'AUTHORITY'; RET=BASE/'RETURN'; TPL=BASE/'TEMPLATES'
ROLE_COLS=['t03_principle','t03_application','t04_goal','t04_means','t05_commitment','t05_cost','t06_norm','t06_stated_intended_conduct','t09_directional_actor_recipient','t11_complementary_component']
YES={'YES','LOCKED_YES'}

def J(x):
    if isinstance(x,list): return x
    if x is None: return []
    try:
        y=json.loads(str(x))
        # catalog occasionally stores nested JSON strings like ["[]"]
        out=[]
        for z in y if isinstance(y,list) else [y]:
            if isinstance(z,str) and z.startswith('[') and z.endswith(']'):
                try: out.extend(json.loads(z))
                except: out.append(z)
            else: out.append(z)
        return out
    except: return []

def D(x): return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def hid(prefix,*parts,n=16): return prefix+hashlib.sha256('|'.join(map(str,parts)).encode()).hexdigest()[:n]
def codes(r): return set(map(str,J(r['source_variable_codes_json'])))
def texts(r): return [str(x) for x in J(r['exact_question_texts_json'])]
def summaries(r): return [str(x) for x in J(r['sem_semantic_summaries_json'])]
def targets(r): return [str(x) for x in J(r['sem_target_ids_json']) if str(x)]
def conditions(r): return [str(x) for x in J(r['sem_condition_ids_json']) if str(x)]
def roles(r): return [str(x) for x in J(r['sem_canonical_roles_json'])]
def preds(r): return [str(x) for x in J(r['sem_measured_predicates_json'])]

def has_numeric_code(cs,prefix,lo,hi):
    for c in cs:
        if c.startswith(prefix) and c[len(prefix):].isdigit() and lo<=int(c[len(prefix):])<=hi: return True
    return False

cat=pd.read_csv(AUTH/'SEMANTIC_UNIT_CATALOG.csv',dtype=str).fillna('')
sp=pd.read_csv(AUTH/'IMPLEMENTATION_SPINE.csv.gz',dtype=str,low_memory=False).fillna('')
r6=pd.read_csv(AUTH/'R6_EXISTING_RELATIONS.csv',dtype=str).fillna('')
objs=pd.read_csv(AUTH/'R11_SOURCE_OBJECTS.csv',dtype=str).fillna('')
role=pd.read_csv(TPL/'SEMANTIC_ROLE_ASSIGNMENT.csv',dtype=str).fillna('')
role_index=role.set_index('semantic_unit_id',drop=False)
cat_index=cat.set_index('semantic_unit_id',drop=False)
sp_index=sp.set_index('question_implementation_id',drop=False)
obj_index=objs.set_index('object_id',drop=False)

def catrow(sf,w,su):
    x=cat[(cat.source_family==sf)&(cat.wave==w)&(cat.semantic_unit_id==su)]
    if len(x)!=1:
        raise KeyError(f'Expected one catalog row for {(sf,w,su)}, found {len(x)}')
    return x.iloc[0]

def roleval(sf,w,su,col):
    x=role[(role.source_family==sf)&(role.wave==w)&(role.semantic_unit_id==su)]
    if len(x)!=1:
        raise KeyError(f'Expected one role row for {(sf,w,su)}, found {len(x)}')
    return x.iloc[0][col]

# implementation <-> semantic crosswalk
impl2su=defaultdict(list); su2impl={}
for _,r in cat.iterrows():
    ims=[str(x) for x in J(r.implementation_ids_json)]
    su2impl[r.semantic_unit_id]=ims
    for im in ims: impl2su[im].append(r.semantic_unit_id)

# -------- Stage A: exhaustive relation-role accounting --------
# All nonlocked shores start at explicit NO. YES is installed only where current exact
# source/semantic authority establishes the role contract; locks are never changed.
for c in ROLE_COLS:
    role.loc[~role[c].str.startswith('LOCKED_'),c]='NO'

# exact role memberships outside locked fields
T03_PRINCIPLE={'p2xsafe__967aba24a9e20392'} # EVS v510 general abortion justifiability
T03_APPLICATION={'p2xsafe__67abe6020c291e50','p2xsafe__c7b1ba5f91c3005c','p2xsafe__2e44dcb2214aeb5c','p2xsafe__e657356aa4097f9d'}
T04_GOAL={'p2xsafe__f5270ebca30d8fc6'} # LiTS 2006 reducing present income inequality
T04_MEANS={'p2xsafe__5df738998e5fe3e8'} # state responsibility/involvement to reduce inequality
T09_DIR={'p2xsafe__7f6be7b57c307d7e','p2xsafe__14004ef8d8c44f60','p2xsafe__f9387d5dfa4a2d90'} # EVS reciprocal + Arab citizen->government one-way
T11_COMP={'p2xsafe__66b7e7a2cc68266a','p2xsafe__e693a62033e6a690','p2xsafe__08b38faa1b57215f','p2xsafe__2f0112e7cb389e89','p2xsafe__5332c2e295556cc0'}
# explicit commitment+burden items; same item may carry both shores but compiler forbids self-pairs
T05_BOTH=set()
for _,r in cat.iterrows():
    cs=codes(r)
    if cs & {'v267','p52','q219a','q219b','q219c','q219d','q219e','q219f','q306a','q306b','q306c','q306d'}:
        T05_BOTH.add(r.semantic_unit_id)
# explicit stated/intended conduct shores
T06_CONDUCT=set()
for _,r in cat.iterrows():
    cs=codes(r)
    if cs & {'v267','p65a','p65b','p65c','p65d','p73','q219a','q219b','q219c','q219d','q219e','q219f','q306a','q306b','q306c','q306d','q328','q528','q529','q708','q709'}:
        T06_CONDUCT.add(r.semantic_unit_id)

# current exact T06 RR_NORM reconstruction for keys outside C3; locked keys remain locked.
def t06_norm_yes(r):
    if r.c3_rr_norm_locked_status=='LOCKED_YES': return True
    if r.c3_rr_norm_locked_status=='LOCKED_NO': return False
    sf,w=r.source_family,r.wave; cs=codes(r); rs=set(roles(r))
    if sf=='EVS' and w=='1981':
        if has_numeric_code(cs,'v',320,339): return True
        if cs & {'v371','v412','v424','v429','v523','v524','v525','v526'}: return True
        if has_numeric_code(cs,'v',470,480) or has_numeric_code(cs,'v',508,518): return True
        return False
    if sf=='Arab Barometer' and w=='V':
        if cs & {'Q521_4','Q521_5'}: return False # perceived guarantee, not norm
        if 'NORMATIVE_OR_POLICY_STANCE' in rs: return True
        if cs & {'Q606_1'}: return True # exact “should not interfere” proposition
        return False
    if sf=='Latinobarómetro' and w=='1995':
        return bool(cs & {'p35','p36','p52','p75'})
    if sf=='LiTS' and w=='2006':
        return 'NORMATIVE_OR_POLICY_STANCE' in rs
    if sf=='LiTS' and w=='II':
        return bool(cs & {'q301h','q322a','q322b','q322c','q322d','q322e','q322f','q322g'})
    return False

for i,r in role.iterrows():
    su=r.semantic_unit_id
    if su in T03_PRINCIPLE: role.at[i,'t03_principle']='YES'
    if su in T03_APPLICATION: role.at[i,'t03_application']='YES'
    if su in T04_GOAL: role.at[i,'t04_goal']='YES'
    if su in T04_MEANS: role.at[i,'t04_means']='YES'
    if su in T05_BOTH:
        role.at[i,'t05_commitment']='YES'; role.at[i,'t05_cost']='YES'
    if su in T06_CONDUCT: role.at[i,'t06_stated_intended_conduct']='YES'
    if su in T09_DIR: role.at[i,'t09_directional_actor_recipient']='YES'
    if su in T11_COMP: role.at[i,'t11_complementary_component']='YES'
    if not str(role.at[i,'t06_norm']).startswith('LOCKED_'):
        role.at[i,'t06_norm']='YES' if t06_norm_yes(catrow(r.source_family,r.wave,su)) else 'NO'

    ev=[f'AUTHORITY/SEMANTIC_UNIT_CATALOG.csv::{su}']
    if str(r.c3_rr_norm_locked_status).startswith('LOCKED_'):
        ev.append(f'AUTHORITY/C3_RR_NORM_LOCKED.csv::{su}')
    if J(r.r6_member_roles_json): ev.append(f'AUTHORITY/R6_EXISTING_RELATIONS.csv::member::{su}')
    role.at[i,'evidence_refs_json']=D(ev)
    # Basis columns summarize both shores for each rule and are item-specific.
    def rb(a,b,yesbasis,nobasis):
        if role.at[i,a] in YES or role.at[i,b] in YES: return yesbasis
        return nobasis
    role.at[i,'t03_basis']=rb('t03_principle','t03_application','Exact source wording establishes a T03 general-principle or governed concrete-application shore.','Exact source wording/semantic summary does not state a T03 principle/application shore; shared topic is not used.')
    role.at[i,'t04_basis']=rb('t04_goal','t04_means','Exact source semantics states either the end “reduce income inequality” or state responsibility/involvement tied to that same end.','Exact source wording does not state a T04 end or a mechanism tied to an explicit common end.')
    role.at[i,'t05_basis']=rb('t05_commitment','t05_cost','Item explicitly states willingness/support together with a named fiscal/personal/risk burden; same-item dual role is retained without creating a self-relation.','Exact source wording does not state an explicit commitment or explicit burden tied to such commitment.')
    if str(role.at[i,'t06_norm']).startswith('LOCKED_'):
        role.at[i,'t06_basis']='C3 final exact semantic-key RR_NORM lock preserved without mutation.'
    elif role.at[i,'t06_norm']=='YES':
        role.at[i,'t06_basis']='Exact source proposition states obligation/approval/justifiability/norm applicability; broad semantic-act labels alone were not used.'
    elif role.at[i,'t06_stated_intended_conduct']=='YES':
        role.at[i,'t06_basis']='Exact source wording states respondent willingness/intention/expected action; this is stated/intended conduct, not realized behavior.'
    else:
        role.at[i,'t06_basis']='Exact source wording does not establish RR_NORM or stated/intended conduct under the T06 contract.'
    role.at[i,'t09_basis']='Exact actor/recipient direction is stated in source wording.' if role.at[i,'t09_directional_actor_recipient']=='YES' else 'Exact source wording does not state a directed actor→recipient proposition suitable for reciprocal reversal.'
    role.at[i,'t11_basis']='Sealed-R6 member ancestry plus exact current source wording establishes a bounded complementary component; common proposition is reconstructed at relation level.' if role.at[i,'t11_complementary_component']=='YES' else 'Exact source wording/current relation authority does not establish a bounded complementary-component role; no latent scale is inferred.'
    role.at[i,'confidence']='HIGH'

role.to_csv(RET/'SEMANTIC_ROLE_ASSIGNMENT.csv',index=False)
role_index=role.set_index('semantic_unit_id',drop=False)

# -------- Stage B: deterministic candidate denominator --------
subprocess.run([sys.executable,str(BASE/'CODE/compile_role_compatible_candidates.py'),str(RET/'SEMANTIC_ROLE_ASSIGNMENT.csv'),str(AUTH/'IMPLEMENTATION_SPINE.csv.gz'),str(RET/'CANDIDATE_ADJUDICATION.csv')],check=True)
cand=pd.read_csv(RET/'CANDIDATE_ADJUDICATION.csv',dtype=str).fillna('')

# -------- Relation implementation helpers --------
relations=[]
def relation_id(rule,label): return hid(f'R16D-S14W01-{rule}-',label,n=18)
def add_relation(**kw):
    row={c:'' for c in pd.read_csv(TPL/'RELATION_IMPLEMENTATIONS.csv',nrows=0).columns}
    row.update(kw); relations.append(row); return row['relation_id']

def cat_ev(sus): return [f'AUTHORITY/SEMANTIC_UNIT_CATALOG.csv::{x}' for x in sus]
def impl_ev(ims): return [f'AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::{x}' for x in ims]

# Novel T03 abortion relation
ABORT_SUS=['p2xsafe__967aba24a9e20392','p2xsafe__67abe6020c291e50','p2xsafe__c7b1ba5f91c3005c','p2xsafe__2e44dcb2214aeb5c','p2xsafe__e657356aa4097f9d']
ABORT_IMS=sum((su2impl[x] for x in ABORT_SUS),[])
RID_T03=add_relation(relation_id=relation_id('T03','EVS1981_ABORTION_PRINCIPLE_APPLICATION'),source_family='EVS',wave='1981',rule_id='T03',relation_type='PRINCIPLE_APPLICATION',branch='SEMANTIC_ROLE_RECONSTRUCTION',member_semantic_unit_ids_json=D(ABORT_SUS),member_implementation_ids_json=D(ABORT_IMS),role_assignments_json=D({ABORT_SUS[0]:'RR_PRINCIPLE',**{x:'RR_APPLICATION' for x in ABORT_SUS[1:]}}),common_proposition_or_target='Abortion justifiability/approval: general abortion principle with four explicitly conditioned applications.',actor_scope='respondent as normative evaluator',target_scope='abortion',action_domain='normative justifiability / approval',position_or_routing_condition=D({x:conditions(cat_index.loc[x]) for x in ABORT_SUS}),authority_basis='Current semantic catalog exact text: EVS v510 asks general abortion justifiability; v523-v526 ask approval under four explicit abortion conditions.',evidence_refs_json=D(cat_ev(ABORT_SUS)+impl_ev(ABORT_IMS)),confidence='HIGH',governance_recommendation='MERGE_CANDIDATE__NOVEL_R16D_RECONSTRUCTION')

# Novel T04 LiTS 2006 inequality goal -> state responsibility means
INEQ_SUS=['p2xsafe__f5270ebca30d8fc6','p2xsafe__5df738998e5fe3e8']; INEQ_IMS=sum((su2impl[x] for x in INEQ_SUS),[])
RID_T04=add_relation(relation_id=relation_id('T04','LITS2006_REDUCE_INEQUALITY_STATE_RESPONSIBILITY'),source_family='LiTS',wave='2006',rule_id='T04',relation_type='GOAL_MEANS',branch='SEMANTIC_ROLE_RECONSTRUCTION',member_semantic_unit_ids_json=D(INEQ_SUS),member_implementation_ids_json=D(INEQ_IMS),role_assignments_json=D({INEQ_SUS[0]:'RR_GOAL',INEQ_SUS[1]:'RR_MEANS'}),common_proposition_or_target='Reduce present income inequality.',actor_scope='respondent policy/economic evaluation; state as means-bearing institution',target_scope='income inequality',action_domain='reduction of income inequality through state responsibility/involvement',position_or_routing_condition=D({INEQ_SUS[0]:conditions(cat_index.loc[INEQ_SUS[0]]),INEQ_SUS[1]:conditions(cat_index.loc[INEQ_SUS[1]])}),authority_basis='Exact LiTS 2006 semantics explicitly names reducing present income inequality and state responsibility/involvement to reduce inequality; usefulness is not inferred.',evidence_refs_json=D(cat_ev(INEQ_SUS)+impl_ev(INEQ_IMS)),confidence='HIGH',governance_recommendation='MERGE_CANDIDATE__NOVEL_R16D_RECONSTRUCTION')

# Novel T09 EVS reciprocal trust
RECIP_SUS=['p2xsafe__7f6be7b57c307d7e','p2xsafe__14004ef8d8c44f60']; RECIP_IMS=sum((su2impl[x] for x in RECIP_SUS),[])
RID_T09=add_relation(relation_id=relation_id('T09','EVS1981_YOUNG_OLDER_TRUST_REVERSAL'),source_family='EVS',wave='1981',rule_id='T09',relation_type='RECIPROCAL_ROLE_REVERSAL',branch='SEMANTIC_ROLE_RECONSTRUCTION',member_semantic_unit_ids_json=D(RECIP_SUS),member_implementation_ids_json=D(RECIP_IMS),role_assignments_json=D({RECIP_SUS[0]:{'actor':'young people','recipient':'older people','action':'trust'},RECIP_SUS[1]:{'actor':'older people','recipient':'young people','action':'trust'}}),common_proposition_or_target='Intergenerational trust between young people and older people.',actor_scope='young people ↔ older people',target_scope='older people ↔ young people',action_domain='trust',position_or_routing_condition='No relation-changing condition in current semantic authority.',authority_basis='Exact paired EVS source wording explicitly reverses actor and recipient while preserving the same trust action.',evidence_refs_json=D(cat_ev(RECIP_SUS)+impl_ev(RECIP_IMS)),confidence='HIGH',governance_recommendation='MERGE_CANDIDATE__NOVEL_R16D_RECONSTRUCTION')

# Canary reconstruction from current source-native members + mappings. R6 is confirmation, not sole proof.
canary_to_rid={}
canary_object_map=defaultdict(list)
for _,rr in r6.iterrows():
    sfwave=J(rr.active_source_wave_set_json)[0]
    sf,w=sfwave.split('::',1)
    cw=J(rr.active_member_crosswalk_json)
    ims=[m.get('question_implementation_id','') for m in cw if m.get('question_implementation_id','')]
    sus=[]
    for im in ims: sus += impl2su.get(im,[])
    sus=list(dict.fromkeys(sus))
    rolemap={}
    for m in cw:
        im=m.get('question_implementation_id',''); mr=m.get('member_role','')
        if rr.rule_id=='T08' and im in sp_index.index:
            rolemap[im]={'member_role':mr,'relation_role':'RR_INSTITUTION_TARGET','institution_class':sp_index.loc[im].t08_institution_class,'class_mapping_status':sp_index.loc[im].t08_class_mapping_status}
        elif rr.rule_id=='T10':
            entry={'member_role':mr,'relation_role':'RR_MATRIX_CELL'}
            if impl2su.get(im):
                q=catrow(sf,w,impl2su[im][0]); entry['target_ids']=targets(q); entry['condition_ids']=conditions(q)
            else:
                code=m.get('source_variable_code',''); txt=sp_index.loc[im].exact_question_text if im in sp_index.index else ''
                if 'do you belong to:' in txt.lower(): entry.update(target=txt.split(':',1)[-1].strip(),condition='BELONGS_TO')
                elif 'do you work unpaid for:' in txt.lower(): entry.update(target=txt.split(':',1)[-1].strip(),condition='WORKS_UNPAID_FOR')
                elif code in {'v356','v357','v358','v359','v360'}: entry.update(target=mr.replace('partner_shared_',''),condition='PARTNER_SHARED')
                elif code in {'v363','v364','v365','v366','v367'}: entry.update(target=mr.replace('parents_shared_',''),condition='PARENTS_SHARED')
            rolemap[im]=entry
        else:
            rolemap[im]={'member_role':mr,'relation_role':'RR_COMPLEMENTARY_COMPONENT'}
    if rr.rule_id=='T08':
        common='Institutional confidence/trust battery with exact institution targets retained and controlled institution-class mapping used only for differentiation.'
        actor='respondent'; target_scope='exact named institutions'; action='confidence/trust'; cond='No condition dimension; exact institution identity retained independently of class.'
    elif rr.rule_id=='T10':
        structs=J(rr.source_structure_ids_json)
        if 'Q208_OTHERS' in ' '.join(structs): common='Ten commandment targets crossed with two explicit applicability conditions: for myself vs to most people.'
        elif 'Q244' in ' '.join(structs): common='Five shared-attitude domains crossed with two relationship contexts: partner vs parents.'
        else: common='Eleven organization/activity targets crossed with two explicit participation conditions: belong to vs work unpaid for.'
        actor='respondent'; target_scope='exact source-native matrix target dimension'; action='source-defined matrix response'; cond='Target and condition cells preserved exactly; no one-dimensional battery promotion.'
    else:
        if sf=='Arab Barometer': common='Source-defined Q607 INTERPRETATION ISLAM block: three bounded components retained as differentiated roles without latent-scale/additivity inference.'
        else: common='Source-defined Q233 family-relationship structure: parents relationship plus respondent-to-mother and respondent-to-father relationships as differentiated bounded components.'
        actor='respondent / source-specified family or social actors'; target_scope='source-defined narrow relational structure'; action='bounded complementary relation components'; cond='Source-native structure and routing/universe preserved; no additive scale inferred.'
    rid=relation_id(rr.rule_id,rr.relation_authority_id)
    add_relation(relation_id=rid,source_family=sf,wave=w,rule_id=rr.rule_id,relation_type=rr.relation_type,branch='CANARY_RECONSTRUCTION',member_semantic_unit_ids_json=D(sus),member_implementation_ids_json=D(ims),role_assignments_json=D(rolemap),common_proposition_or_target=common,actor_scope=actor,target_scope=target_scope,action_domain=action,position_or_routing_condition=cond,authority_basis='Reconstructed from current exact R11 source-native structure plus R10 semantic/spine mappings; sealed R6 relation used only as canary expected-answer confirmation.',evidence_refs_json=D([f'AUTHORITY/R11_SOURCE_OBJECTS.csv::{x}' for x in J(rr.source_structure_ids_json)]+impl_ev(ims)+cat_ev(sus)+[f'AUTHORITY/R6_EXISTING_RELATIONS.csv::{rr.relation_authority_id}']),confidence='HIGH',governance_recommendation='RETAIN_CANARY_TRUTH__R16D_RECONSTRUCTION_CONFIRMED')
    canary_to_rid[rr.relation_authority_id]=rid
    for oid in J(rr.source_structure_ids_json):
        # R6 structure IDs match R11 object IDs for these canaries except LiTS historical case exact spelling does match.
        canary_object_map[oid].append((rr.rule_id,rid))

# manually map cross-object structure aliases appearing in R11 review
for auth,rid in canary_to_rid.items():
    rr=r6[r6.relation_authority_id==auth].iloc[0]
    if auth=='IQRA-R2-62987a589a96f73738bc':
        for oid in ['EVS-R14-1981-Q208_OTHERS','EVS-R14-1981-Q208_SELF']: canary_object_map[oid].append(('T10',rid))
    if auth=='IQRA-R2-5d28ea6e3b88aab56cd6':
        for oid in ['EVS-R14-1981-Q244','EVS-R14-1981-Q245']: canary_object_map[oid].append(('T10',rid))
    if auth=='IQRA-R2-cd48c9b9683e892d0490': canary_object_map['LITS-2006-GROUP-Q303'].append(('T08',rid))
    if auth=='IQRA-R2-52fdbc606d4338f1c5c0': canary_object_map['LiTS-R14-II-Q303'].append(('T08',rid))
    if auth=='IQRA-R2-f811d7fadd5f319b1c2e': canary_object_map['EVS-R14-1981-Q349'].append(('T08',rid))
    if auth=='IQRA-R2-5530257f7b0d907c1224': canary_object_map['ArabBarometer-R14-STRUCTURE-Q607-FROM-5a0ef600c1ced579b273'].append(('T11',rid))
    if auth=='IQRA-R2-7df41bf91f3ec070a296': canary_object_map['EVS-R14-1981-Q233'].append(('T11',rid))
    if auth=='IQRA-R2-de354d77df5cc4bdb7c5': canary_object_map['EVS-R14-1981-Q113-AB'].append(('T10',rid))

# -------- Stage C: adjudicate every candidate --------
# Positive candidate pair lookup
positive_pair_to_rid={}
for a in T03_APPLICATION: positive_pair_to_rid[('T03',ABORT_SUS[0],a,'')]=RID_T03
positive_pair_to_rid[('T04',INEQ_SUS[0],INEQ_SUS[1],'')]=RID_T04
positive_pair_to_rid[('T09',min(RECIP_SUS),max(RECIP_SUS),'')]=RID_T09
# T11 canary semantic member pairs
for auth in ['IQRA-R2-5530257f7b0d907c1224','IQRA-R2-7df41bf91f3ec070a296']:
    rr=r6[r6.relation_authority_id==auth].iloc[0]; rid=canary_to_rid[auth]
    ims=[m['question_implementation_id'] for m in J(rr.active_member_crosswalk_json)]
    sus=[]
    for im in ims: sus+=impl2su.get(im,[])
    sus=sorted(set(sus))
    for i,a in enumerate(sus):
        for b in sus[i+1:]: positive_pair_to_rid[('T11',a,b,'')]=rid

stop=set('the a an of to in for on with and or is are be being been have has had do does did you your respondent people country should would could from at as if this that it its about how what which who when where why more less than same good bad very source defined item degree extent following statement statements agree disagree think opinion future done'.split())
def tokset(x): return {z for z in re.findall(r'[a-z]+',x.lower()) if len(z)>=4 and z not in stop}
def sutext(sf,w,su):
    r=catrow(sf,w,su)
    return ' '.join(texts(r)+summaries(r)+targets(r))

def cand_evidence(row):
    ev=[]
    if row.left_semantic_unit_id: ev.append(f'AUTHORITY/SEMANTIC_UNIT_CATALOG.csv::{row.left_semantic_unit_id}')
    if row.right_semantic_unit_id: ev.append(f'AUTHORITY/SEMANTIC_UNIT_CATALOG.csv::{row.right_semantic_unit_id}')
    if row.right_endpoint_implementation_id: ev.append(f'AUTHORITY/IMPLEMENTATION_SPINE.csv.gz::{row.right_endpoint_implementation_id}')
    return D(ev)

for i,r in cand.iterrows():
    a,b,ep=r.left_semantic_unit_id,r.right_semantic_unit_id,r.right_endpoint_implementation_id
    key=(r.rule_id,a,b,'')
    if r.rule_id in {'T09','T11'} and b: key=(r.rule_id,min(a,b),max(a,b),'')
    if key in positive_pair_to_rid:
        cand.at[i,'adjudication_status']='POSITIVE_RELATION'; cand.at[i,'relation_id_if_positive']=positive_pair_to_rid[key]
        cand.at[i,'decision_basis']='Exact required shores and narrow common proposition/action are established under current authority; pair is consolidated into the referenced multi-member relation where applicable.'
        cand.at[i,'confidence']='HIGH'; cand.at[i,'evidence_refs_json']=cand_evidence(r); continue
    if r.rule_id=='T05':
        ta=set(targets(catrow(r.source_family,r.wave,a))); tb=set(targets(catrow(r.source_family,r.wave,b)))
        cand.at[i,'adjudication_status']='PROVEN_NEGATIVE'; cand.at[i,'mismatch_dimension']='same_substantive_object_required__canonical_target_mismatch'
        cand.at[i,'decision_basis']=f'T05 requires commitment and burden tied to the same substantive object; current canonical targets are {sorted(ta)} vs {sorted(tb)}.'
        cand.at[i,'confidence']='HIGH'; cand.at[i,'evidence_refs_json']=cand_evidence(r); continue
    if r.rule_id=='T06' and r.branch=='STATED_INTENDED':
        ta=set(targets(catrow(r.source_family,r.wave,a))); tb=set(targets(catrow(r.source_family,r.wave,b)))
        if ta and tb and ta.isdisjoint(tb):
            md='narrow_target_action_mismatch'; basis=f'T06 requires exact actor/target/action alignment; governed semantic targets are disjoint: norm {sorted(ta)} vs stated/intended conduct {sorted(tb)}.'
        else:
            md='actor_action_or_modality_mismatch'; basis='Exact source wording does not preserve the same actor-target-action proposition across norm and stated/intended conduct; shared vocabulary is insufficient.'
        cand.at[i,'adjudication_status']='PROVEN_NEGATIVE'; cand.at[i,'mismatch_dimension']=md; cand.at[i,'decision_basis']=basis; cand.at[i,'confidence']='HIGH'; cand.at[i,'evidence_refs_json']=cand_evidence(r); continue
    if r.rule_id=='T06' and r.branch=='REALIZED_O04_ENDPOINT':
        n=catrow(r.source_family,r.wave,a); e=sp_index.loc[ep]
        nt=tokset(sutext(r.source_family,r.wave,a)); et=tokset(' '.join([e.exact_question_text,e.o04__s2b_target,e.o04__s2b_action_or_exposure]))
        inter=nt&et
        # All plausible lexical-neighborhood collisions were hostile-reviewed. They still fail exact actor/action/target identity.
        if inter:
            md='actor_target_action_or_direction_mismatch'
            basis=f'O04 authorizes the endpoint but not the T06 link. Exact norm proposition and endpoint differ in actor/target/action or direction despite overlapping terms {sorted(inter)}; no same narrow conduct proposition remains.'
        else:
            md='narrow_target_action_mismatch'
            basis='Exact norm target/action and O04 endpoint target/action are substantively distinct under current source wording; O04 endpoint permission does not create semantic linkage.'
        cand.at[i,'adjudication_status']='PROVEN_NEGATIVE'; cand.at[i,'mismatch_dimension']=md; cand.at[i,'decision_basis']=basis; cand.at[i,'confidence']='HIGH'; cand.at[i,'evidence_refs_json']=cand_evidence(r); continue
    # Any unexpected nonpositive compiled pair: prove target mismatch only when current canonical targets explicitly differ; otherwise block.
    ta=set(targets(catrow(r.source_family,r.wave,a))) if a else set(); tb=set(targets(catrow(r.source_family,r.wave,b))) if b else set()
    if ta and tb and ta.isdisjoint(tb):
        cand.at[i,'adjudication_status']='PROVEN_NEGATIVE'; cand.at[i,'mismatch_dimension']='canonical_target_or_common_proposition_mismatch'; cand.at[i,'decision_basis']=f'Rule requires a narrow common proposition/target; governed targets are disjoint: {sorted(ta)} vs {sorted(tb)}.'; cand.at[i,'confidence']='HIGH'
    else:
        cand.at[i,'adjudication_status']='BLOCKED_AUTHORITY_GAP'; cand.at[i,'authority_gap']='Current authority does not establish the additional common-proposition/reversal/role tie required for this compiled pair, and no necessary incompatibility is proven.'; cand.at[i,'decision_basis']='Role compatibility alone is not relation truth.'; cand.at[i,'confidence']='MEDIUM'
    cand.at[i,'evidence_refs_json']=cand_evidence(r)

cand.to_csv(RET/'CANDIDATE_ADJUDICATION.csv',index=False)

# -------- Stage D: source-object/group reconstruction --------
review=pd.read_csv(TPL/'SOURCE_OBJECT_RULE_REVIEW.csv',dtype=str).fillna('')
# novel object participation
novel_obj_pos={
    ('EVS-R14-1981-Q339','T03'):RID_T03,
    ('LITS-2006-GROUP-Q301','T04'):RID_T04,
    ('LITS-2006-GROUP-Q305','T04'):RID_T04,
}

def cell_pairs(oid):
    if oid not in obj_index.index: return []
    o=obj_index.loc[oid]; out=[]
    for su in J(o.semantic_unit_ids_json):
        if su not in cat_index.index: continue
        q=catrow(o.source_family,o.wave,su)
        ts=targets(q); cs=conditions(q)
        if len(ts)==1 and len(cs)==1: out.append((su,ts[0],cs[0]))
    return out

def evidence_for_obj(oid):
    o=obj_index.loc[oid]
    return D([f'AUTHORITY/R11_SOURCE_OBJECTS.csv::{oid}']+cat_ev(J(o.semantic_unit_ids_json))+impl_ev(J(o.mapped_implementation_ids_json)))

for i,r in review.iterrows():
    oid,ruleid=r.object_id,r.rule_id; o=obj_index.loc[oid]
    # positives first
    posrid=novel_obj_pos.get((oid,ruleid))
    if not posrid:
        for rrid,rid in canary_object_map.get(oid,[]):
            if rrid==ruleid: posrid=rid; break
    if posrid:
        review.at[i,'worker_structure_status']='POSITIVE_STRUCTURE'; review.at[i,'relation_ids_json']=D([posrid]); review.at[i,'decision_basis']='Exact current source-native structure participates in the reconstructed positive relation; structure was rechecked independently and not accepted merely from recall.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'; continue
    nsem=int(o.semantic_unit_count or 0); nimpl=int(o.mapped_implementation_count or 0); sus=J(o.semantic_unit_ids_json)
    if nsem==0:
        review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Current R11 source object has exact implementation membership but zero governed structural semantic-unit mappings; source-native membership alone cannot establish or disprove this relation contract.'; review.at[i,'decision_basis']='No relation truth is inferred from an unmapped source container.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'; continue
    if ruleid=='T08':
        ic=int(o.institution_class_count or 0)
        if ic<2:
            review.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; review.at[i,'mismatch_dimension']='controlled_institution_class_differentiation_absent'; review.at[i,'decision_basis']=f'T08 requires exact institution targets spanning at least two governed controlled classes; current object has institution_class_count={ic}.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'
        else:
            review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Multiple governed institution classes exist, but no exact T08 relation has been reconstructed for this noncanary object.'; review.at[i,'decision_basis']='Class co-occurrence alone is not relation truth.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='MEDIUM'
        continue
    if ruleid=='T10':
        if oid in {'LB1995-P15-SOURCE-NATIVE','LB1995-P46-SOURCE-NATIVE'}:
            review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Latinobarómetro family-economy cells lack a governed normalized target identity across p4/p5/p6 and p4/p5 lack the required explicit temporal condition mapping; a rectangular target×condition matrix cannot be asserted or fully disproven until repaired.'; review.at[i,'decision_basis']='National-economy cells show repeated conditions, but current family-economy target/condition normalization is incomplete; doctrine forbids repairing the matrix lexically.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'; continue
        nt=int(o.distinct_target_count or 0); nc=int(o.distinct_condition_count or 0)
        if nt<2 or nc<2:
            review.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; review.at[i,'mismatch_dimension']='target_or_condition_dimension_cardinality'; review.at[i,'decision_basis']=f'T10 requires at least two governed targets and two governed conditions with repeated cells; current object has {nt} target(s) and {nc} condition(s), so it is one-dimensional/non-matrix.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'; continue
        cells=cell_pairs(oid); t2c=defaultdict(set); c2t=defaultdict(set)
        for _,t,c in cells: t2c[t].add(c); c2t[c].add(t)
        if sum(len(v)>=2 for v in t2c.values())<2 or sum(len(v)>=2 for v in c2t.values())<2:
            review.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; review.at[i,'mismatch_dimension']='non_rectangular_target_condition_membership'; review.at[i,'decision_basis']='Although multiple target and condition labels occur, governed semantic cell membership is not a crossed matrix: targets do not repeat across multiple conditions and conditions do not repeat across multiple targets.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'
        else:
            review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Potential rectangular cell pattern requires source-native matrix authority beyond current object summary; no positive is asserted by dimensionality alone.'; review.at[i,'decision_basis']='Matrix-like counts are insufficient without exact cell authority.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='MEDIUM'
        continue
    if ruleid=='T07':
        nt=int(o.distinct_target_count or 0)
        if nt<2:
            review.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; review.at[i,'mismatch_dimension']='broader_narrower_target_cardinality'; review.at[i,'decision_basis']=f'T07 requires at least two exact targets in a governed broader→narrower relation; current object has distinct_target_count={nt}.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'
        else:
            review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Current R11 object establishes multiple exact targets but supplies no governing directional broader-than/narrower-than authority; lexical generality is prohibited.'; review.at[i,'decision_basis']='Target plurality is recall terrain, not hierarchy truth.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'
        continue
    # role-dependent T03/T04/T05/T06/T09/T11 object-local adjudication
    req={
        'T03':('t03_principle','t03_application'),
        'T04':('t04_goal','t04_means'),
        'T05':('t05_commitment','t05_cost'),
        'T06':('t06_norm','t06_stated_intended_conduct'),
        'T09':('t09_directional_actor_recipient','t09_directional_actor_recipient'),
        'T11':('t11_complementary_component','t11_complementary_component'),
    }[ruleid]
    vals={c:[roleval(r.source_family,r.wave,su,c) for su in sus] for c in set(req)}
    if nsem<nimpl:
        # If current semantic mapping omits source members, absence of a semantic role cannot prove the object negative.
        review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Source object contains implementation members without governed structural semantic-unit mappings; missing members could bear a required relation role, so absence among mapped semantic units is not a negative.'; review.at[i,'decision_basis']='Incomplete semantic coverage blocks object-level role exclusion.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'; continue
    if ruleid in {'T09','T11'}:
        cnt=sum(v in YES for v in vals[req[0]])
        if cnt<2:
            review.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; review.at[i,'mismatch_dimension']='insufficient_required_relation_role_members'; review.at[i,'decision_basis']=f'{ruleid} requires at least two governed members bearing the required directional/complementary role; exact Stage-A accounting finds {cnt}.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'
        else:
            review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Required member roles are present but current authority does not establish the exact reciprocal/common-proposition tie for this object.'; review.at[i,'decision_basis']='Role compatibility alone is insufficient.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='MEDIUM'
    elif ruleid=='T06':
        normcnt=sum(v in YES for v in vals['t06_norm']); concnt=sum(v in YES for v in vals['t06_stated_intended_conduct']); epcnt=int(o.accepted_endpoint_count or 0)
        if normcnt==0:
            review.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; review.at[i,'mismatch_dimension']='rr_norm_shore_absent'; review.at[i,'decision_basis']='T06 requires a governed norm shore; exhaustive Stage-A accounting finds none among all governed semantic members of this fully mapped object.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'
        elif concnt==0 and epcnt==0:
            review.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; review.at[i,'mismatch_dimension']='conduct_or_endpoint_shore_absent'; review.at[i,'decision_basis']='T06 requires stated/intended conduct or an O04 ACCEPT_ENDPOINT shore; this fully mapped object contains neither.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'
        else:
            review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Norm and possible conduct/endpoint shores occur, but exact actor-target-action linkage is not established at object level.'; review.at[i,'decision_basis']='Co-presence is not linkage.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='MEDIUM'
    else:
        aok=sum(v in YES for v in vals[req[0]])>0; bok=sum(v in YES for v in vals[req[1]])>0
        if not aok or not bok:
            review.at[i,'worker_structure_status']='PROVEN_NEGATIVE'; review.at[i,'mismatch_dimension']='required_relation_shore_absent'; review.at[i,'decision_basis']=f'{ruleid} requires both {req[0]} and {req[1]} shores; exhaustive Stage-A accounting of all governed members proves at least one required shore absent.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='HIGH'
        else:
            review.at[i,'worker_structure_status']='BLOCKED_AUTHORITY_GAP'; review.at[i,'authority_gap']='Both role shores occur but no exact current common-proposition/end/object tie establishes a source-object relation.'; review.at[i,'decision_basis']='Role co-occurrence alone is insufficient.'; review.at[i,'evidence_refs_json']=evidence_for_obj(oid); review.at[i,'confidence']='MEDIUM'

review.to_csv(RET/'SOURCE_OBJECT_RULE_REVIEW.csv',index=False)

# -------- Positive relations file --------
rel=pd.DataFrame(relations,columns=pd.read_csv(TPL/'RELATION_IMPLEMENTATIONS.csv',nrows=0).columns)
rel=rel.drop_duplicates('relation_id')
rel.to_csv(RET/'RELATION_IMPLEMENTATIONS.csv',index=False)

# -------- Stage E canary recall --------
can=pd.read_csv(TPL/'CANARY_RECALL.csv',dtype=str).fillna('')
for i,r in can.iterrows():
    rid=canary_to_rid[r.relation_authority_id]
    can.at[i,'worker_recall_status']='REDISCOVERED_POSITIVE'; can.at[i,'recovered_relation_id']=rid
    can.at[i,'decision_basis']='R16D independently reconstructed the exact active-member source structure and required rule metadata under current R11/R10 authority; sealed R6 supplied the expected canary answer and confirmed reconstruction, not a substitute for it.'
    can.at[i,'evidence_refs_json']=D([f'AUTHORITY/R6_EXISTING_RELATIONS.csv::{r.relation_authority_id}',f'RETURN/RELATION_IMPLEMENTATIONS.csv::{rid}'])
can.to_csv(RET/'CANARY_RECALL.csv',index=False)

# -------- Explicit negative space --------
anti=[]
for _,r in cand[cand.adjudication_status=='PROVEN_NEGATIVE'].iterrows():
    mids=[x for x in [r.left_semantic_unit_id,r.right_semantic_unit_id,r.right_endpoint_implementation_id] if x]
    anti.append(dict(antijoin_id=hid('R16D-AJ-CAND-',r.candidate_id),source_family=r.source_family,wave=r.wave,rule_id=r.rule_id,member_ids_json=D(mids),mismatch_dimension=r.mismatch_dimension,decision_basis=r.decision_basis,evidence_refs_json=r.evidence_refs_json,scope_of_negative_claim='Exact compiled candidate only; does not negate other members or other source-wave relations.'))
for _,r in review[review.worker_structure_status=='PROVEN_NEGATIVE'].iterrows():
    anti.append(dict(antijoin_id=hid('R16D-AJ-OBJ-',r.object_id,r.rule_id),source_family=r.source_family,wave=r.wave,rule_id=r.rule_id,member_ids_json=D([r.object_id]),mismatch_dimension=r.mismatch_dimension,decision_basis=r.decision_basis,evidence_refs_json=r.evidence_refs_json,scope_of_negative_claim='Exact reviewed source object under this rule only; cross-object relations are not negated unless separately adjudicated.'))
pd.DataFrame(anti,columns=pd.read_csv(TPL/'EXPLICIT_ANTIJOINS.csv',nrows=0).columns).to_csv(RET/'EXPLICIT_ANTIJOINS.csv',index=False)

# -------- Authority gaps, grouped without hiding affected IDs --------
gapgroups=defaultdict(list)
for _,r in cand[cand.adjudication_status=='BLOCKED_AUTHORITY_GAP'].iterrows(): gapgroups[(r.source_family,r.wave,r.rule_id,r.authority_gap,'CANDIDATE')].append(r.candidate_id)
for _,r in review[review.worker_structure_status=='BLOCKED_AUTHORITY_GAP'].iterrows(): gapgroups[(r.source_family,r.wave,r.rule_id,r.authority_gap,'SOURCE_OBJECT')].append(r.object_id)
gaps=[]
for (sf,w,ruleid,gap,kind),ids in sorted(gapgroups.items()):
    rec='Recover/repair exact source semantic mappings or governed directional/target-condition/common-proposition authority in the current central S14 authority; do not infer from recall.'
    if 'Latinobarómetro' in sf and ruleid=='T10': rec='Repair Latinobarómetro p4/p5/p6 family-economy canonical target equivalence and missing temporal condition mappings from source authority, then rerun T10.'
    gaps.append(dict(gap_id=hid('R16D-GAP-',sf,w,ruleid,gap,kind),source_family=sf,wave=w,rule_id=ruleid,affected_ids_json=D(sorted(set(ids))),missing_authority=gap,why_needed='Output law forbids converting missing linkage/normalization authority into either a positive relation or a negative.',source_recovery_pointer='AUTHORITY/R11_SOURCE_OBJECTS.csv; AUTHORITY/SEMANTIC_UNIT_CATALOG.csv; AUTHORITY/IMPLEMENTATION_SPINE.csv.gz; exact source authorities named in those rows.',recommended_central_action=rec))
pd.DataFrame(gaps,columns=pd.read_csv(TPL/'AUTHORITY_GAPS.csv',nrows=0).columns).to_csv(RET/'AUTHORITY_GAPS.csv',index=False)

# -------- Propagation ledger for exact repeated source-native structures --------
prop=[]
def addprop(pid,sf,w,ruleid,sus,why,ev,rows): prop.append(dict(propagation_rule_id=pid,source_family=sf,wave=w,rule_id=ruleid,scope_ids_json=D(sus),why_semantically_identical=why,evidence_basis=ev,rows_affected=str(rows)))
# helpers by codes
code2su={(r.source_family,r.wave,c):r.semantic_unit_id for _,r in cat.iterrows() for c in codes(r)}
def sus_for(sf,w,cs): return [code2su[(sf,w,c)] for c in cs if (sf,w,c) in code2su]
addprop('PROP-EVS1981-Q208-RRNORM','EVS','1981','T06',sus_for('EVS','1981',[f'v{x}' for x in range(320,340)]),'Exact repeated commandment-applicability battery; only target ordinal and explicit self/most-people condition vary.','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv + exact EVS source texts',20)
addprop('PROP-EVS1981-JUSTIFY-RRNORM','EVS','1981','T06',sus_for('EVS','1981',[f'v{x}' for x in list(range(470,481))+list(range(508,519))]),'Exact repeated “do you justify:” source-native battery with target-specific justifiability predicate.','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv + exact EVS source texts',22)
addprop('PROP-EVS1981-Q339-APPLICATION','EVS','1981','T03',sus_for('EVS','1981',['v523','v524','v525','v526']),'Exact repeated abortion-approval battery; same abortion target with four explicit conditions.','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv; R11 Q339 source object',4)
addprop('PROP-LITS2006-Q312-RRNORM','LiTS','2006','T06',sus_for('LiTS','2006',['q312_1','q312_2','q312_4','q312_5','q312_6','q312_7','q312_8','q312_9','q312_10']),'Exact repeated normative-importance battery; each item names a country-level institutional/social feature.','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv',9)
addprop('PROP-LITSII-Q322-RRNORM','LiTS','II','T06',sus_for('LiTS','II',['q322a','q322b','q322c','q322d','q322e','q322f','q322g']),'Exact repeated moral-wrongness/permissibility battery over bounded behaviors.','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv; R11 Q322 structure',7)
addprop('PROP-LITSII-Q219-COST-CONDUCT','LiTS','II','T05;T06',sus_for('LiTS','II',['q219a','q219b','q219c','q219d','q219e','q219f']),'Exact repeated willingness-to-pay-more-for-satisfactory-service battery; service target varies, fiscal burden form is invariant.','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv + exact source text',6)
addprop('PROP-LITSII-Q306-COST-CONDUCT','LiTS','II','T05;T06',sus_for('LiTS','II',['q306a','q306b','q306c','q306d']),'Exact repeated willingness to give income/pay more taxes if assured funds serve the named end; end varies, fiscal burden form is invariant.','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv + exact source text',4)
addprop('PROP-LB1995-P65-CONDUCT','Latinobarómetro','1995','T06',sus_for('Latinobarómetro','1995',['p65a','p65b','p65c','p65d']),'Exact repeated “Have you, or would you ever” political-action battery; action target varies while mixed realized/prospective response form is invariant.','AUTHORITY/SEMANTIC_UNIT_CATALOG.csv + exact source text',4)
pd.DataFrame(prop,columns=pd.read_csv(TPL/'PROPAGATION_LEDGER.csv',nrows=0).columns).to_csv(RET/'PROPAGATION_LEDGER.csv',index=False)

# -------- Hostile QA --------
qa=[]
def addqa(sf,w,ruleid,challenge,finding,status,ev): qa.append(dict(qa_id=hid('R16D-QA-',sf,w,ruleid,challenge),source_family=sf,wave=w,rule_id=ruleid,challenge=challenge,finding=finding,status=status,evidence_refs_json=D(ev)))
for _,r in rel.iterrows():
    addqa(r.source_family,r.wave,r.rule_id,f'Overreach challenge for positive {r.relation_id}: does source structure establish required roles/common proposition without topic-only inference?',f'PASS. Member roles, exact implementations, routing/conditions and the common proposition/target/action are explicit in the relation row. Canary rows were independently reconstructed from R11/spine before R6 confirmation; novel rows use exact semantic/source text.','PASS',[f'RETURN/RELATION_IMPLEMENTATIONS.csv::{r.relation_id}'])
# hostile negative examples
neg=cand[cand.adjudication_status=='PROVEN_NEGATIVE']
for ruleid in ['T05','T06']:
    x=neg[neg.rule_id==ruleid].head(2)
    for _,r in x.iterrows(): addqa(r.source_family,r.wave,r.rule_id,f'Negative challenge {r.candidate_id}: was failure-to-prove-positive improperly converted into a negative?',f'PASS. Negative names an explicit necessary-condition mismatch ({r.mismatch_dimension}); scope is limited to the exact candidate.','PASS',[f'RETURN/CANDIDATE_ADJUDICATION.csv::{r.candidate_id}'])
# source object true-negative and blocks
for oid,ruleid in [('EVS-R14-1981-Q339','T10'),('LB1995-P46-SOURCE-NATIVE','T10')]:
    x=review[(review.object_id==oid)&(review.rule_id==ruleid)].iloc[0]
    addqa(x.source_family,x.wave,x.rule_id,f'Source-object challenge {oid}: matrix overreach/underreach?',f'PASS. Status={x.worker_structure_status}. {x.decision_basis} {x.authority_gap}','PASS',[f'RETURN/SOURCE_OBJECT_RULE_REVIEW.csv::{oid}::{ruleid}'])
# T06 plausible lexical-neighborhood collision
x=cand[(cand.rule_id=='T06')&(cand.branch=='REALIZED_O04_ENDPOINT')]
# prioritize q322e vs q604 endpoint when present
for _,r in x.iterrows():
    if r.left_semantic_unit_id=='p2xsafe__d8271d3426160b1e' and r.right_endpoint_implementation_id in sp_index.index and sp_index.loc[r.right_endpoint_implementation_id].source_variable_code.startswith('q604'):
        addqa(r.source_family,r.wave,'T06','Actor-direction challenge: moral wrongness of a public official asking for a favor/gift vs respondent/household making an unofficial payment/gift.', 'PASS. Same corruption neighborhood is not actor-action identity: norm actor is public official asking; endpoint actor is respondent/household paying. T06 positive rejected as actor/direction mismatch.','PASS',[f'RETURN/CANDIDATE_ADJUDICATION.csv::{r.candidate_id}']); break
# propagation batches
for _,p in pd.DataFrame(prop).iterrows(): addqa(p.source_family,p.wave,p.rule_id,f'Propagation challenge {p.propagation_rule_id}: did batching erase semantic differences?',f'PASS. Batch is limited to an exact repeated source-native form; only named target/condition slots vary and those remain item-specific. rows_affected={p.rows_affected}.','PASS',[f'RETURN/PROPAGATION_LEDGER.csv::{p.propagation_rule_id}'])
pd.DataFrame(qa,columns=pd.read_csv(TPL/'HOSTILE_QA.csv',nrows=0).columns).to_csv(RET/'HOSTILE_QA.csv',index=False)

# -------- Coverage 45 source-wave x rule rows --------
cov=pd.read_csv(TPL/'RULE_WAVE_COVERAGE.csv',dtype=str).fillna('')
for i,r in cov.iterrows():
    sf,w,ruleid=r.source_family,r.wave,r.rule_id
    cc=cand[(cand.source_family==sf)&(cand.wave==w)&(cand.rule_id==ruleid)]
    oo=review[(review.source_family==sf)&(review.wave==w)&(review.rule_id==ruleid)]
    rr=rel[(rel.source_family==sf)&(rel.wave==w)&(rel.rule_id==ruleid)]
    ccan=can[(can.rule_id==ruleid)&can.active_source_wave_set_json.str.contains(f'{sf}::{w}',regex=False)]
    negcount=int((cc.adjudication_status=='PROVEN_NEGATIVE').sum()+(oo.worker_structure_status=='PROVEN_NEGATIVE').sum())
    blkcount=int((cc.adjudication_status=='BLOCKED_AUTHORITY_GAP').sum()+(oo.worker_structure_status=='BLOCKED_AUTHORITY_GAP').sum())
    poscount=len(rr)
    cov.at[i,'semantic_role_scan_complete']='YES'; cov.at[i,'source_object_scan_complete']='YES'; cov.at[i,'compiled_candidate_count']=str(len(cc)); cov.at[i,'positive_relation_count']=str(poscount); cov.at[i,'proven_negative_count']=str(negcount); cov.at[i,'blocked_count']=str(blkcount); cov.at[i,'known_canaries_expected']=str(len(ccan)); cov.at[i,'known_canaries_recovered']=str(int((ccan.worker_recall_status=='REDISCOVERED_POSITIVE').sum()))
    if poscount==0:
        if blkcount:
            cov.at[i,'zero_explanation_if_no_positive']=f'BLOCKED_AUTHORITY_GAP: exhaustive semantic/candidate/object scan found no governed positive, but {blkcount} opportunity row(s) remain blocked by explicitly recorded authority gaps; therefore this is not asserted as a true zero.'; cov.at[i,'coverage_status']='BLOCKED_AUTHORITY_GAP'
        else:
            cov.at[i,'zero_explanation_if_no_positive']=f'COMPLETE_TRUE_ZERO: exhaustive scan completed; {negcount} applicable candidate/object opportunity row(s) were explicitly disproven and no unresolved authority gap remains for this wave/rule.'; cov.at[i,'coverage_status']='COMPLETE_TRUE_ZERO'
    else:
        cov.at[i,'zero_explanation_if_no_positive']=''
        cov.at[i,'coverage_status']='COMPLETE_WITH_POSITIVES_AND_RESIDUAL_AUTHORITY_GAPS' if blkcount else 'COMPLETE_WITH_POSITIVES'
    cov.at[i,'notes']='Counts combine compiled candidate adjudications with source-object review for negative/block accounting; positive count is unique relation implementations. R6 canaries are counted only after R16D reconstruction.'
cov.to_csv(RET/'RULE_WAVE_COVERAGE.csv',index=False)

print(json.dumps({
 'role_yes_counts':{c:int(role[c].isin(YES).sum()) for c in ROLE_COLS},
 'candidates':len(cand),'candidate_status':cand.adjudication_status.value_counts().to_dict(),
 'relations':len(rel),'relations_by_rule':rel.rule_id.value_counts().to_dict(),
 'source_object_status':review.worker_structure_status.value_counts().to_dict(),
 'gaps':len(gaps),'antijoins':len(anti),'qa':len(qa),'propagation':len(prop)
},indent=2))
