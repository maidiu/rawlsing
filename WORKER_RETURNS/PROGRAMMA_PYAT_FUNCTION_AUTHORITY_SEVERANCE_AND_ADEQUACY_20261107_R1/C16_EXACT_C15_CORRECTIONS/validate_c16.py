#!/usr/bin/env python3
"""C16 proportionate validation: actual checks, no vacuous PASS."""
import json,csv,hashlib,subprocess,sys,os
BASE='9651352a846da9ed85d4e64562b7d2b07b90fb07'  # current HQ head at correction; forbidden paths compare to HEAD
C14='f42b73abf2532f9a4ea589e7f80841e15585d8e1'
C14_03='f21823f83e6aed6a64695150bf4ed43df2e7fd88b3310ab26752476acc61a778'
checks=[]
def check(name,cond,detail=''):
    checks.append((name,bool(cond),detail))
    print(('PASS' if cond else 'FAIL'),name,detail)
def load_jsonl(p):
    return [json.loads(l) for l in open(p) if l.strip()]
def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git_show(p):
    return subprocess.check_output(['git','show',f'{BASE}:{p}'])
# 1. 03 case identity
recs=load_jsonl('03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl')
alias=load_jsonl('03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl')
check('03_count_55',len(recs)==55,str(len(recs)))
check('03_unique_55',len({r['case_id'] for r in recs})==55)
from collections import Counter
fam=Counter(r['case_family'] for r in recs)
check('families_1_2_10_2_7_29_4',fam==Counter({'C1':1,'C2':2,'C3':10,'C4':2,'C5':7,'C6':29,'C9':4}),str(dict(fam)))
tax=Counter(r['frozen_taxonomy_verdict'] for r in recs)
check('taxonomy_25_30',tax==Counter({'FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED':25,'NOT_RUN':30}),str(dict(tax)))
check('canonical_alias_equal',recs==alias)
check('canonical_alias_sha_equal',sha('03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl')==sha('03_BIDIRECTIONAL_FUNCTION_AUTHORITY_CASES.jsonl'))
check('c16_03_hash_distinct_from_c14',sha('03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl')!=C14_03,sha('03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl'))
# 2. historical 51 IDs/taxonomy preserved vs C14 snapshot
c14=load_jsonl_from=None
c14_raw=subprocess.check_output(['git','show',f'{C14}:WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl'],text=True)
c14=[json.loads(l) for l in c14_raw.splitlines() if l.strip()]
check('historical_51_ids_preserved',[r['case_id'] for r in recs[:51]]==[r['case_id'] for r in c14[:51]])
check('historical_51_taxonomy_preserved',[r['frozen_taxonomy_verdict'] for r in recs[:51]]==[r['frozen_taxonomy_verdict'] for r in c14[:51]])
check('all_A_J_nonempty',all(all(k in r and r[k] not in (None,'') for k in 'ABCDEFGHIJ') for r in recs))
check('all_forward_reverse_hold',all(r.get('forward_walk') and r.get('reverse_walk') and r.get('exact_hold') for r in recs))
# 3. C9 lineage
c9=[r for r in recs if r['case_id'].startswith('C9-')]
check('c9_4_cases',len(c9)==4)
check('c9_reviewed_target_d540',all(r.get('reviewed_target_cut')=='d540cfcc44359f8f78aceccf8afb247c4a7ad80d' for r in c9))
check('c9_review_05a750ad',all(r.get('review_cut')=='05a750ad6bcab8124c1f5d86b8867181fa4ee92c' for r in c9))
check('c9_correction_02a13a5e',all(r.get('correction_cut')=='02a13a5e01880835434b30d9a3587147f9dab0de' for r in c9))
check('c9_no_independent_rereview',all(r.get('acceptance_lineage',{}).get('correction_review_status')=='NO_INDEPENDENT_REREVIEW_OF_CORRECTION' for r in c9))
# 4. F08 QUC wording
f08=[r for r in recs if r['case_id']=='C6-F08_Q_USE'][0]
check('f08_hold_qualified','NO_QUC_READER' not in f08['exact_hold'] and 'UNKNOWN_NOT_PROVED' in f08['exact_hold'])
check('f08_current_quc_unknown',f08.get('current_quc_owner')=='UNKNOWN_NOT_PROVED' and f08.get('current_quc_first_consumer')=='UNKNOWN_NOT_PROVED' and f08.get('quc_absence_proof') is False)
check('f08_grade_preserved',f08['frozen_taxonomy_verdict']=='NOT_RUN')
# 5. 02/05/01/08 counts
r2=list(csv.DictReader(open('02_CURRENT_IMPLEMENTATIONS_PRE_FORGE_VS_WHOLE_PREV3.tsv'),delimiter='\t'))
r5=list(csv.DictReader(open('05_SEVERED_OR_INCOMPLETE_MINIMAL_OWNER_REPAIRS.tsv'),delimiter='\t'))
r1=list(csv.reader(open('01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv'),delimiter='\t'))
r8=list(csv.reader(open('08_COVERAGE_DENOMINATORS_COLD_HANDOFF.tsv'),delimiter='\t'))
check('02_153_rows',len(r2)==153,str(len(r2)))
check('02_55_case_rows',len({r['CASE_ID'] for r in r2 if r['ROW_TYPE']=='CASE'})==55)
check('02_register_counts',Counter(r['ROW_TYPE'] for r in r2)==Counter({'CASE':55,'748_CURRENT_OWNER':30,'FF_REGISTER':26,'FF_DEPENDENCY':16,'POST_FF_REGISTER':15,'POST_FF_SEAM':11}),str(dict(Counter(r['ROW_TYPE'] for r in r2))))
check('05_55_rows',len(r5)==55 and len({r['CASE_ID'] for r in r5})==55)
check('01_94_rows',len(r1)-1==94,str(len(r1)-1))
check('08_63_rows',len(r8)-1==63,str(len(r8)-1))
check('02_05_03_ids_equal',{r['CASE_ID'] for r in r2 if r['ROW_TYPE']=='CASE'}=={r['CASE_ID'] for r in r5}=={r['case_id'] for r in recs})
# 6. C16 deliverables
for f in ['C16_EXACT_C15_CORRECTIONS/00_RETURN.md','C16_EXACT_C15_CORRECTIONS/FINDING_RESOLUTION.jsonl','C16_EXACT_C15_CORRECTIONS/PARENT_ISSUE_DISPOSITIONS.jsonl','C16_EXACT_C15_CORRECTIONS/GOAL_AUDIT.json']:
    check('exists_'+f,os.path.exists(f))
fr=load_jsonl('C16_EXACT_C15_CORRECTIONS/FINDING_RESOLUTION.jsonl')
pids=load_jsonl('C16_EXACT_C15_CORRECTIONS/PARENT_ISSUE_DISPOSITIONS.jsonl')
check('finding_resolution_10',len(fr)==10,str(len(fr)))
check('finding_ids_exact',{r['finding_id'] for r in fr}=={'C14-G6-T6','C14-F01-C8-LINEAGE','C14-F02-BASE-LINEAGE','C14-F03-REVIEWER-INDEPENDENCE','C14-F04-C9-LINEAGE','C14-F05-C6F08-QUC','C14-G3-T3','C14-G4-T4','C14-F06-C9-WORDING','C14-F07-PROVENANCE-PLACEHOLDER'})
check('parent_rows_12',len(pids)==12,str(len(pids)))
check('parent_union_exact',{r['issue_or_pr'] for r in pids}=={716,748,753,765,766,767,772,769,770,773,774,691})
check('parent_live_states_open',all(r['live_state']=='open' for r in pids))
check('parent_prs_unmerged',all(r['live_merged'] is False for r in pids if r['kind']=='PR'))
# 7. GOAL audit statuses
ga=json.load(open('C16_EXACT_C15_CORRECTIONS/GOAL_AUDIT.json'))
crit={c['criterion_id']:c['status'] for c in ga['terminal_criteria']}
check('T2_typed_hold',crit['T2']=='NOT_SATISFIED__TYPED_HOLD',crit['T2'])
check('T3_limit',crit['T3']=='SATISFIED_AS_LIMIT__ZERO_EQUIVALENCE_CLAIMS__NO_PRODUCT_POSITIVE_PROOF',crit['T3'])
check('T4_limit',crit['T4']=='SATISFIED_AS_LIMIT__ZERO_PROVED_SEVERANCES__NO_PRODUCT_POSITIVE_PROOF',crit['T4'])
check('T6_issue_table',crit['T6'].startswith('SATISFIED_AT_ISSUE-BY-ISSUE_DISPOSITION_RECORDED'),crit['T6'])
check('goal_false',ga['goal_complete'] is False)
# 8. no moving HEAD placeholder / unqualified QUC
for f in ['00_EXECUTIVE_REAL_OPERATIONS_AND_VERDICT.md','09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md']:
    s=open(f).read(); check('no_see_branch_head_'+f,'SEE_BRANCH_HEAD' not in s)
for f in ['00_EXECUTIVE_REAL_OPERATIONS_AND_VERDICT.md','01_LEGACY_SELECTED_AUTHORITY_USE_AND_INCOMPLETE_CALLEE_COVERAGE.tsv','02_CURRENT_IMPLEMENTATIONS_PRE_FORGE_VS_WHOLE_PREV3.tsv','03_BIDIRECTIONAL_AUTHORITY_REQUIREMENT_AND_CONSUMPTION.jsonl','04_PROVED_EQUIVALENCES_AND_NO_BUILD_DECISIONS.md','05_SEVERED_OR_INCOMPLETE_MINIMAL_OWNER_REPAIRS.tsv','06_REAL_LOCAL_TEST_COMMANDS_OUTPUT_HASHES_AND_MUTATIONS.md','08_COVERAGE_DENOMINATORS_COLD_HANDOFF.tsv','09_INDEPENDENT_REVIEW_REQUEST_AND_EXACT_HEAD.md','10_HQ_PRIORITY_AND_NEXT_WORK.md']:
    s=open(f).read(); check('no_unqualified_NO_QUC_READER_'+f,'NO_QUC_READER' not in s)
# 9. forbidden paths unchanged vs BASE
forbidden=['07_SECONDARY_AGENDA_NON_DROP_AND_WORKER_COLLISION.md','CHECKPOINT.json','FLIGHT_BOARD.json','COMMISSIONS','PYAT_CONTROL_ROOM','C14_POST_C9_C13_FANIN','C15_HQ_FANIN_C14_REREVIEW']
for f in forbidden:
    diff=subprocess.check_output(['git','diff','--name-only',BASE,'--',f],text=True).strip()
    check('forbidden_unchanged_'+f,diff=='',diff[:200])
# 10. agenda
check('agenda_17',len(load_jsonl('SECONDARY_AGENDA_FROZEN.jsonl'))==17)
# summary
failed=[c for c in checks if not c[1]]
print(f'\nSUMMARY: {len(checks)-len(failed)}/{len(checks)} checks passed; {len(failed)} failed')
if failed:
    print('FAILED:',[c[0] for c in failed]); sys.exit(1)
print('C16_VALIDATION_PASS')
