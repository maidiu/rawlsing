from pathlib import Path
import pandas as pd,json,sys
R=Path(__file__).resolve().parents[1]
errs=[];checks=[]
def py(x):
    try:return x.item()
    except:return x
def ck(n,c,d=None): checks.append((n,bool(c),py(d))); errs.append(n) if not c else None
p=pd.read_csv(R/'AUDIT/O11_T03_T05_PROXY_GROUP_DISPOSITION_R8.csv')
ck('proxy_T03_194',int((p.rule_id=='S14-T03').sum())==194,int((p.rule_id=='S14-T03').sum()))
ck('proxy_T04_59',int((p.rule_id=='S14-T04').sum())==59,int((p.rule_id=='S14-T04').sum()))
ck('proxy_T05_42',int((p.rule_id=='S14-T05').sum())==42,int((p.rule_id=='S14-T05').sum()))
ck('proxy_all_dispositioned',p.disposition.fillna('').str.len().gt(0).all())
c=pd.read_csv(R/'PROVENANCE/R6_T03_T05_12_CANARY_RECOVERY_R8.csv')
ck('r6_canaries_12',len(c)==12,len(c)); ck('r6_T03_8',int((c.rule_id=='S14-T03').sum())==8,int((c.rule_id=='S14-T03').sum()));ck('r6_T04_1',int((c.rule_id=='S14-T04').sum())==1,int((c.rule_id=='S14-T04').sum()));ck('r6_T05_3',int((c.rule_id=='S14-T05').sum())==3,int((c.rule_id=='S14-T05').sum()))
o=pd.read_csv(R/'AUDIT/T03_T05_R14_596_EXACT_OBJECT_ACCOUNTING_R8.csv')
for rid in ['S14-T03','S14-T04','S14-T05']:ck(rid+'_r14_596',int((o.rule_id==rid).sum())==596,int((o.rule_id==rid).sum()))
ck('r14_no_excerpt_authority',o.evidence_law.str.contains('forbidden').all())
pack=pd.read_csv(R/'NARROWING/T03_T05_RECONSTRUCTED_CANONICAL_PACKETS_R8.csv');ck('reconstructed_packets_11',len(pack)==11,len(pack));ck('no_accept_verdicts',~pack.status.str.startswith('ACCEPT').any());ck('all_reconstructed_have_semantic_units',pack.semantic_unit_ids_json.map(lambda x:len(json.loads(x))>0).all())
raw=pd.read_csv(R/'NARROWING/T03_T11_RAW_PACKET_LEDGER_R8.csv');canon=pd.read_csv(R/'NARROWING/T03_T11_CROSS_RULE_DEDUPED_CANONICAL_PACKETS_R8.csv');worker=pd.read_csv(R/'NARROWING/T03_T11_UNRESOLVED_REVIEW_DENOMINATOR_R8.csv');single=pd.read_csv(R/'NARROWING/T03_T11_WORKER_ELIGIBLE_SINGLE_RULE_DENOMINATOR_R8.csv');cross=pd.read_csv(R/'NARROWING/T03_T11_VOZHD_CENTRAL_CROSS_RULE_DENOMINATOR_R8.csv');block=pd.read_csv(R/'NARROWING/T03_T11_BLOCKER_DEPENDENCIES_R8.csv')
ck('raw_packet_rows_96',len(raw)==96,len(raw));ck('canonical_packet_rows_89',len(canon)==89,len(canon));ck('unresolved_66',len(worker)==66,len(worker));ck('worker_single_53',len(single)==53,len(single));ck('central_cross_13',len(cross)==13,len(cross));ck('blockers_4',len(block)==4,len(block));ck('single_plus_cross_eq_worker',len(single)+len(cross)==len(worker));ck('single_has_no_cross_rule',~single.rule_hypotheses.str.contains(';',regex=False).any());ck('cross_all_cross_rule',cross.rule_hypotheses.str.contains(';',regex=False).all());ck('worker_only_unresolved',(worker.queue_class=='UNRESOLVED_REVIEW').all());ck('canonical_ids_unique',canon.canonical_packet_id.is_unique)
st=json.load(open(R/'CURRENT_STATUS_R8.json'));ck('job3_blocked',st['job3_authorized'] is False);ck('workers_not_launched',st['workers_launched'] is False);ck('worker_count_matches',st['cross_rule_dedupe']['unresolved_review_denominator']==len(worker));ck('hybrid_decision',st['worker_economics_decision'].startswith('HYBRID__SHARD_53'))
res={'status':'PASS' if not errs else 'FAIL','checks':len(checks),'errors':errs,'details':[{'check':n,'pass':p,'detail':d} for n,p,d in checks]}
json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R8.json','w'),indent=2);print(json.dumps({'status':res['status'],'checks':res['checks'],'errors':len(errs)},indent=2));sys.exit(1 if errs else 0)
