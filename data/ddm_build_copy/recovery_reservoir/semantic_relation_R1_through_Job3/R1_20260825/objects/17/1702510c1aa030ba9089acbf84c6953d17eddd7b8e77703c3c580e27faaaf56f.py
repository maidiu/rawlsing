from pathlib import Path
import json,sys,re
R=Path(__file__).resolve().parents[1];errs=[];checks=[]
def ck(n,x,d=None):checks.append({'check':n,'pass':bool(x),'detail':d});errs.append(n) if not x else None
a=json.load(open(R/'AUDIT/R9B_CANARY_COVERAGE_CORRECTION.json'));ck('math',a['pair_census_addressable_relations']+a['nonpair_or_nonrelational_lane_relations']==a['r6_t03_t11_total_relations']);ck('98',a['pair_census_addressable_relations']==98);ck('19',a['nonpair_or_nonrelational_lane_relations']==19);ck('210',a['nonpair_member_implementation_count']==210);ck('interpretation_nineteen','Nineteen sealed' in a['interpretation']);ck('interpretation_no_twenty','Twenty sealed' not in a['interpretation'])
r=(R/'R9B_COMPOSITE_DENOMINATOR_REPORT.md').read_text();ck('report_19','By rule, the 19 gaps are' in r);ck('report_no_20','By rule, the 20 gaps are' not in r);ck('report_98_117','98 / 117' in r);ck('report_19_117','19 / 117' in r)
s=json.load(open(R/'CURRENT_STATUS_R9B.json'));ck('job3_false',s['job3_authorized'] is False);ck('packs_poisoned',s['r8_worker_packs']=='DO_NOT_EXECUTE')
res={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks};json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R9B.json','w'),indent=2);print(json.dumps({'status':res['status'],'checks':len(checks),'errors':errs}));sys.exit(0 if not errs else 1)
