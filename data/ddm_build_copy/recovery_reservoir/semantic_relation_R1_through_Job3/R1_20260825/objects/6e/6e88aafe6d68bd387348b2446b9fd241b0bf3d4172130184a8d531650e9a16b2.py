from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];checks=[];errs=[]
def ck(n,x,d=None):checks.append({'check':n,'pass':bool(x),'detail':d});errs.append(n) if not x else None
s=json.load(open(R/'CURRENT_STATUS_R9C.json'));ck('job3_false',s['job3_authorized'] is False);ck('packs_poisoned',s['r8_worker_packs']=='DO_NOT_EXECUTE');ck('98_19',s['r6_t03_t11_canary_coverage']=={'pair_addressable':98,'nonpair_or_nonrelational':19});ck('pair_scope','3324' in s['pair_census'] and '364094' in s['pair_census'])
r=(R/'R9C_COMPOSITE_DENOMINATOR_REPORT.md').read_text();ck('report_title',r.startswith('# R9C —'));ck('report_no_stale_20','20 gaps' not in r and 'Twenty sealed' not in r);ck('report_counts','98 / 117' in r and '19 / 117' in r and '210 member' in r)
p=(R/'ACTIVE_EXECUTION_POINTER.md').read_text();ck('pointer_r9c','CHECKPOINT_R9C_20260811' in p);ck('pointer_poison','DO NOT EXECUTE' in p);ck('pointer_job3','NOT AUTHORIZED' in p);ck('pointer_math','117 total = 98 pair-addressable + 19' in p)
a=json.load(open(R/'AUDIT/R9C_CANARY_COVERAGE_STATE.json'));ck('audit_math',a['pair_census_addressable_relations']+a['nonpair_or_nonrelational_lane_relations']==117)
res={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks};json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R9C.json','w'),indent=2);print(json.dumps({'status':res['status'],'checks':len(checks),'errors':errs}));sys.exit(0 if not errs else 1)
