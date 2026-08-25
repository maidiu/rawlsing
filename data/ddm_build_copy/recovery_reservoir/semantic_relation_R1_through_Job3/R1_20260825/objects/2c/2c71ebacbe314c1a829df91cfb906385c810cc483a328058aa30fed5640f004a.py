import pandas as pd, json, re, hashlib, os, subprocess, sys
from pathlib import Path
B=Path(__file__).resolve().parents[1]
R=B/'RETURN'

def jload(x):
    try: return json.loads(x) if x else []
    except: return []
def jdump(x): return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def hid(prefix,*parts): return prefix+hashlib.sha256('|'.join(map(str,parts)).encode()).hexdigest()[:18]

role=pd.read_csv(B/'TEMPLATES/SEMANTIC_ROLE_ASSIGNMENT.csv',dtype=str).fillna('')
spine=pd.read_csv(B/'AUTHORITY/IMPLEMENTATION_SPINE.csv.gz',dtype=str,compression='gzip',low_memory=False).fillna('')
r6=pd.read_csv(B/'AUTHORITY/R6_EXISTING_RELATIONS.csv',dtype=str).fillna('')
objects=pd.read_csv(B/'AUTHORITY/R11_SOURCE_OBJECTS.csv',dtype=str).fillna('')

# Current R6 canary implementation -> role relation maps, used only with current exact semantic/source-object evidence.
r6_t11_sus=set(); r6_t03_principle=set(); r6_t03_apps=set()
impl_to_su=dict(zip(spine.question_implementation_id,spine.sem__audit_unit_id))
r6_rel_members={}
for _,rr in r6.iterrows():
    mem=jload(rr.active_member_crosswalk_json); r6_rel_members[rr.relation_authority_id]=mem
    if rr.rule_id=='T11':
        for m in mem:
            su=impl_to_su.get(m.get('question_implementation_id',''),'')
            if su: r6_t11_sus.add(su)
    if rr.rule_id=='T03':
        # Current Q67 evidence: first member is the general regime evaluation; three remainder are specific consequence/capacity applications.
        for i,m in enumerate(mem):
            su=impl_to_su.get(m.get('question_implementation_id',''),'')
            if not su: continue
            if i==0: r6_t03_principle.add(su)
            else: r6_t03_apps.add(su)

# Helpers from exact current semantic fields.
def textblob(x):
    vals=[]
    for c in ['exact_question_texts_json','sem_semantic_summaries_json','sem_measured_predicates_json','sem_canonical_roles_json']:
        v=jload(x[c]); vals += [str(z) for z in (v if isinstance(v,list) else [v])]
    return ' '.join(vals).lower()
def evidence_blob(x):
    vals=[]
    for c in ['exact_question_texts_json','sem_semantic_summaries_json','sem_measured_predicates_json']:
        v=jload(x[c]); vals += [str(z) for z in (v if isinstance(v,list) else [v])]
    return ' '.join(vals).lower()

def has_role(x,name): return name in jload(x.sem_canonical_roles_json)

norm_cue=re.compile(r'\b(should|must|ought|norm|normative|justify|justifiable|permissib|support|opposition|approve|approval|favor|favour|acceptable|right to|responsibilit|priority|allowed|allow |prohibit|criminali[sz]|fair to|unfit for|best political system)\b',re.I)
conduct_cue=re.compile(r'willingness|willing to|would vote|would you vote|intend|intention|plan to|prepared to|ready to|fight for country|take risks',re.I)
cost_cue=re.compile(r'willingness_to_financial_sacrifice|cost_sacrifice_willingness|cost-bearing willingness|pay higher|pay more|give part of income|more taxes|cut in living|reduction in living standards|financial sacrifice|paying more in taxes|take risks|risk willingness',re.I)
# T09 is adjudicated by an exact current-text whitelist after hostile review; broad lexical directionality is not sufficient.
T09_EXACT_DIRECTIONAL = {
    ('Asian Barometer','W5'): {'q62','q63','q91','q108','q112','q113','q122','q143'},
    ('EVS','2008'): {'v135'},
    ('LiTS','IV'): {'q826a'},
}

role_cols=['t03_principle','t03_application','t04_goal','t04_means','t05_commitment','t05_cost','t06_norm','t06_stated_intended_conduct','t09_directional_actor_recipient','t11_complementary_component']
for idx,x in role.iterrows():
    blob=textblob(x)
    eblob=evidence_blob(x)
    # default all unlocked roles to NO; each is a semantic membership decision, not a relation negative.
    for c in role_cols:
        if c=='t06_norm': continue
        if not str(role.at[idx,c]).startswith('LOCKED_'):
            role.at[idx,c]='NO'
    # T03 only current exact Q67 structure establishes the principle/application shores.
    if x.semantic_unit_id in r6_t03_principle: role.at[idx,'t03_principle']='YES'
    if x.semantic_unit_id in r6_t03_apps: role.at[idx,'t03_application']='YES'
    # T04: explicit goal/means language is rare; do not promote generic priority/usefulness.
    if re.search(r'\b(goal|aim|objective)\b',blob): role.at[idx,'t04_goal']='YES'
    if re.search(r'\b(means to|means of|method to|mechanism to|way to achieve|best way to)\b',blob): role.at[idx,'t04_means']='YES'
    # T05: exact commitment terminology; cost shore has explicit personal/fiscal/risk/autonomy burden.
    if re.search(r'\b(commitment|committed to|pledge to)\b',blob): role.at[idx,'t05_commitment']='YES'
    if cost_cue.search(blob): role.at[idx,'t05_cost']='YES'
    # T06 norm: preserve C3 locks. Outside C3, require explicit normative wording/predicate, not canonical role alone.
    if role.at[idx,'t06_norm']=='':
        role.at[idx,'t06_norm']='YES' if norm_cue.search(blob) else 'NO'
    # T06 stated/intended conduct: explicit willingness/intention toward an action; descriptive expectations do not qualify.
    if conduct_cue.search(eblob): role.at[idx,'t06_stated_intended_conduct']='YES'
    # Explicitly exclude predicted events/actions by other actors from respondent-conduct shore.
    if any(k in eblob for k in ['likely to lose job','likely to be praised by supervisor','government will solve the most important problem']): role.at[idx,'t06_stated_intended_conduct']='NO'
    # T09 directed proposition: exact current-text adjudication. A directional-looking comparison is not enough;
    # the item itself must state an actor -> recipient/target direction.
    src_codes=set(str(z).lower() for z in jload(x.source_variable_codes_json))
    allowed={z.lower() for z in T09_EXACT_DIRECTIONAL.get((x.source_family,x.wave),set())}
    if src_codes & allowed: role.at[idx,'t09_directional_actor_recipient']='YES'
    # T11: current exact canary structures establish bounded components. Other recall-only groups are handled in Stage D.
    if x.semantic_unit_id in r6_t11_sus: role.at[idx,'t11_complementary_component']='YES'
    # Basis fields
    role.at[idx,'t03_basis']='CURRENT_R10_SEMANTICS_PLUS_Q67_SOURCE_OBJECT_ROLE_TEST' if (role.at[idx,'t03_principle']=='YES' or role.at[idx,'t03_application']=='YES') else 'CURRENT_R10_SEMANTICS_DO_NOT_ESTABLISH_T03_MEMBER_ROLE'
    role.at[idx,'t04_basis']='EXACT_TEXT_EXPLICIT_GOAL_MEANS_ROLE_TEST' if (role.at[idx,'t04_goal']=='YES' or role.at[idx,'t04_means']=='YES') else 'CURRENT_EXACT_TEXT_DOES_NOT_ESTABLISH_EXPLICIT_GOAL_OR_MEANS_ROLE'
    role.at[idx,'t05_basis']='EXACT_TEXT_EXPLICIT_COMMITMENT_COST_ROLE_TEST' if (role.at[idx,'t05_commitment']=='YES' or role.at[idx,'t05_cost']=='YES') else 'CURRENT_EXACT_TEXT_DOES_NOT_ESTABLISH_COMMITMENT_OR_EXPLICIT_COST_ROLE'
    if str(role.at[idx,'t06_norm']).startswith('LOCKED_'):
        role.at[idx,'t06_basis']='C3_LOCK_PRESERVED__PLUS_CURRENT_TEXT_FOR_CONDUCT_SHORE'
    else:
        role.at[idx,'t06_basis']='OUTSIDE_C3__EXPLICIT_NORM_AND_STATED_CONDUCT_TEXT_TEST'
    role.at[idx,'t09_basis']='EXACT_CURRENT_TEXT_ACTOR_TO_RECIPIENT_DIRECTION_ADJUDICATION' if role.at[idx,'t09_directional_actor_recipient']=='YES' else 'CURRENT_TEXT_DOES_NOT_ESTABLISH_EXPLICIT_DIRECTED_ACTOR_TO_RECIPIENT_ROLE'
    role.at[idx,'t11_basis']='CURRENT_SOURCE_OBJECT_PLUS_EXACT_MEMBER_TEXT_RECONSTRUCTION' if role.at[idx,'t11_complementary_component']=='YES' else 'NO_CURRENT_NARROW_COMPLEMENTARY_COMPONENT_AUTHORITY_AT_SEMANTIC_UNIT_LEVEL'
    role.at[idx,'evidence_refs_json']=jdump(['AUTHORITY/SEMANTIC_UNIT_CATALOG.csv','AUTHORITY/IMPLEMENTATION_SPINE.csv.gz','AUTHORITY/RELATION_ROLE_ONTOLOGY_R10.csv'] + (['AUTHORITY/R6_EXISTING_RELATIONS.csv','AUTHORITY/R11_SOURCE_OBJECTS.csv'] if x.semantic_unit_id in (r6_t11_sus|r6_t03_principle|r6_t03_apps) else []))
    role.at[idx,'confidence']='HIGH' if 'BLOCKED' not in [role.at[idx,c] for c in role_cols] else 'MEDIUM'
role.to_csv(R/'SEMANTIC_ROLE_ASSIGNMENT.csv',index=False)

print('Stage A role counts:')
for c in role_cols: print(c,role[c].value_counts().to_dict())
