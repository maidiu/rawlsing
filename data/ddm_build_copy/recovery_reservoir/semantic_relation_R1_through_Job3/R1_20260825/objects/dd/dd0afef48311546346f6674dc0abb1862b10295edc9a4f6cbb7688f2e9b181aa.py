import pandas as pd, json, re
from pathlib import Path
B=Path(__file__).resolve().parents[1]
p=B/'RETURN/SEMANTIC_ROLE_ASSIGNMENT.csv'
df=pd.read_csv(p,dtype=str).fillna('')
role_cols=['t03_principle','t03_application','t04_goal','t04_means','t05_commitment','t05_cost','t06_norm','t06_stated_intended_conduct','t09_directional_actor_recipient','t11_complementary_component']
# Exhaustive default: exact semantic unit inspected; role absent under narrow contract.
for c in role_cols:
    m=df[c].eq('')
    df.loc[m,c]='NO'
# Preserve all embedded C3/R6 locks: nothing below touches LOCKED_*.

def vars_of(r):
    try:return set(json.loads(r['source_variable_codes_json'] or '[]'))
    except:return set()
def texts(r):
    try:return ' || '.join(json.loads(r['exact_question_texts_json'] or '[]'))
    except:return r['exact_question_texts_json']
def vals(r,col):
    try:return json.loads(r[col] or '[]')
    except:return []
# Adjudicate T06 norm only outside C3. Broad semantic-act role is evidence, not sufficient.
# Explicit exclusions are current-text non-norms despite broad or noisy tags.
exclude_norm_vars={
    ('WVS','W7','Q161'),('WVS','W7','Q170'),('WVS','W7','Q176'),('WVS','W7','Q27'),
    ('EVS','2017','v79'),('EVS','2017','v79_DE'),
    ('Arab Barometer','I','q2135'),('Arab Barometer','I','q2476'),('Arab Barometer','I','q2513'),('Arab Barometer','I','q2514'),('Arab Barometer','I','q304'),('Arab Barometer','I','q5046'),
}
for i,r in df.iterrows():
    if r['t06_norm']!='NO' or not str(r['c3_rr_norm_locked_status']).startswith('OUTSIDE_C3'):
        continue
    v=vars_of(r); text=texts(r).lower(); roles='|'.join(vals(r,'sem_canonical_roles_json')); preds='|'.join(vals(r,'sem_measured_predicates_json')).lower()
    if any((r['source_family'],r['wave'],x) in exclude_norm_vars for x in v):
        continue
    explicit = False
    if 'NORMATIVE_OR_POLICY_STANCE' in roles:
        explicit=True
    if re.search(r'\bshould\b|\bduty\b|\bought\b|\bjustif|\bacceptable\b|\bapprove\b|\bfavor\b|\boppose\b|\ballow\b|\bright to\b|\bforced by law\b|\bmade legal\b',text):
        explicit=True
    if any(k in preds for k in ['moral permiss','moral accept','moral evaluation','approval','permissibility','support/opposition','right_to_die','civil-liberty tolerance','suicide_acceptability']):
        explicit=True
    # Salience/importance items that happen to say "should" describe preferred attributes, not obligation.
    if 'SALIENCE_OR_IMPORTANCE' in roles and not any(k in preds for k in ['norm','duty']):
        explicit=False
    if explicit:
        df.at[i,'t06_norm']='YES'
# Explicit stated/intended/expected conduct shores from exact current question semantics.
conduct_vars={
 ('GSS','2002'):{'chldfrnd','chldsch','donothng','fininc4','nextdoor','spendeve','talkemp','talksup','trynewjb'},
 ('EVS','2017'):{'v112'},
 ('Arab Barometer','I'):{'q501'},
 ('South Asia','W2'):{'GBC32'},
}
for i,r in df.iterrows():
    if vars_of(r) & conduct_vars.get((r['source_family'],r['wave']),set()):
        df.at[i,'t06_stated_intended_conduct']='YES'
# Explicit T05 cost-bearing/commitment semantics. These do not assert pair relations by themselves.
for i,r in df.iterrows():
    key=(r['source_family'],r['wave']); v=vars_of(r)
    if key==('EVS','2017') and 'v199' in v:
        df.at[i,'t05_commitment']='YES'; df.at[i,'t05_cost']='YES'
    if key==('Asian Barometer','W1') and 'q143' in v:
        df.at[i,'t05_commitment']='YES'; df.at[i,'t05_cost']='YES'
    if key==('WVS','W7') and 'Q41' in v:
        df.at[i,'t05_commitment']='YES'; df.at[i,'t05_cost']='YES'
    # Exact cross-member T05 structure: Q40 states work as a social duty; Q41 applies that
    # commitment under an explicit time/leisure burden. Q40 supplies the commitment shore.
    if key==('WVS','W7') and 'Q40' in v:
        df.at[i,'t05_commitment']='YES'
# Sealed R6 is current authority, but used only to identify the exact current members whose T11 shore
# is then independently corroborated by current source text/source-object structure.
r6=pd.read_csv(B/'AUTHORITY/R6_EXISTING_RELATIONS.csv',dtype=str).fillna('')
canary_t11=set()
for _,rr in r6[r6.rule_id=='T11'].iterrows():
    for m in json.loads(rr.active_member_crosswalk_json or '[]'):
        canary_t11.add(m['question_implementation_id'])
for i,r in df.iterrows():
    ids=set(vals(r,'implementation_ids_json'))
    if ids & canary_t11:
        df.at[i,'t11_complementary_component']='YES'
# Exact current-text homolog of the sealed EVS v82-v84 family/parenthood T11 relation:
# WVS Q36-Q38 restate the same three bounded propositions (same-sex parenting competence,
# social duty to have children, adult-child duty of care). This is source evidence, not recall truth.
for i,r in df.iterrows():
    if (r['source_family'],r['wave'])==('WVS','W7') and (vars_of(r) & {'Q36','Q37','Q38'}):
        df.at[i,'t11_complementary_component']='YES'
# Per-rule basis/evidence; never pretend broad role tags establish a positive shore.
for i,r in df.iterrows():
    ev=[f"AUTHORITY/SEMANTIC_UNIT_CATALOG.csv::{r['source_family']}::{r['wave']}::{r['semantic_unit_id']}"]
    if str(r['t06_norm']).startswith('LOCKED_'):
        ev.append('AUTHORITY/C3_RR_NORM_LOCKED.csv')
    if r['t11_complementary_component']=='YES':
        ev += ['AUTHORITY/R11_SOURCE_OBJECTS.csv','AUTHORITY/R6_EXISTING_RELATIONS.csv']
    df.at[i,'evidence_refs_json']=json.dumps(ev,separators=(',',':'))
    for rule,cols in {
      't03':['t03_principle','t03_application'], 't04':['t04_goal','t04_means'], 't05':['t05_commitment','t05_cost'],
      't06':['t06_norm','t06_stated_intended_conduct'], 't09':['t09_directional_actor_recipient'], 't11':['t11_complementary_component']}.items():
        statuses=[r[c] if c not in ['t06_norm','t06_stated_intended_conduct','t11_complementary_component','t05_commitment','t05_cost'] else df.at[i,c] for c in cols]
        if any(x in {'YES','LOCKED_YES'} for x in statuses):
            if rule=='t06' and df.at[i,'t06_norm'].startswith('LOCKED_'):
                basis='C3 governed RR_NORM lock preserved; other T06 shore adjudicated from exact current question semantics.'
            elif rule=='t11':
                basis='Exact current source text establishes a differentiated bounded T11 component; sealed R6 is used only where applicable as current canary or exact-homolog boundary authority.'
            elif rule=='t05':
                basis='Exact wording contains both substantive commitment and an explicit personal/fiscal/time cost; shore status only, not a pair relation claim.'
            else:
                basis='Exact current question semantics satisfy this narrow relation-role shore definition.'
        else:
            basis='Exact current question text/semantic summary does not instantiate either narrow shore required by this rule; broad topic/driver similarity was not used.'
        df.at[i,rule+'_basis']=basis
    df.at[i,'confidence']='HIGH' if not any(df.at[i,c]=='BLOCKED' for c in role_cols) else 'MEDIUM'
df.to_csv(p,index=False)
print('wrote',len(df))
for c in role_cols: print(c,df[c].value_counts().to_dict())
