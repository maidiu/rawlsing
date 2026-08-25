import pandas as pd,json,sys,os
R=os.path.dirname(os.path.dirname(__file__))
e=[];c=0
def ck(n,b,d=None):
 global c;c+=1
 if not b:e.append((n,d))
r6=pd.read_csv(os.path.join(R,'PROVENANCE/R6_T11_62_SEALED_PARENT_ROWS_R7.csv'))
r5=pd.read_csv(os.path.join(R,'AUDIT/R5_T11_118_RECALL_LOCATOR_DISPOSITION_R7.csv'))
r14=pd.read_csv(os.path.join(R,'NARROWING/T11_R14_596_SOURCE_OBJECT_ACCOUNTING_R7.csv'))
direct=pd.read_csv(os.path.join(R,'NARROWING/T11_SOURCE_NATIVE_DIRECT_OPPORTUNITIES_R7.csv'))
cross=pd.read_csv(os.path.join(R,'NARROWING/T11_CROSS_OBJECT_47_GROUP_DISPOSITION_R7.csv'))
old=pd.read_csv(os.path.join(R,'AUDIT/O11_T11_OLD_PROXY_GROUP_DISPOSITION_R7.csv'))
pk=pd.read_csv(os.path.join(R,'NARROWING/T11_CANONICAL_REVIEW_PACKETS_R7.csv'))
st=json.load(open(os.path.join(R,'CURRENT_STATUS_R7.json')))
ck('r6_62',len(r6)==62,len(r6));ck('r5_118',len(r5)==118,len(r5));ck('r5_no_empty',r5.disposition.fillna('').str.len().gt(0).all())
ck('r14_596',len(r14)==596,len(r14));ck('r14_no_empty',r14.disposition.fillna('').str.len().gt(0).all())
ck('direct_valid_two',len(direct)==2,len(direct));ck('cross_47',len(cross)==47,len(cross));ck('cross_no_empty',cross.disposition.fillna('').str.len().gt(0).all())
ck('old_proxy_24',len(old)==24,len(old));ck('packets_nonempty',len(pk)>0,len(pk));ck('all_emit_have_packet',cross.loc[cross.disposition.eq('EMIT_T11_REVIEW_CANDIDATE'),'packet_id'].fillna('').str.len().gt(0).all())
ck('no_authority_accepts',not cross.disposition.str.startswith('ACCEPT').any())
ck('job3_false',st.get('job3_authorized') is False);ck('next_dedupe',st.get('t11',{}).get('next_dependency')=='cross-rule packet dedupe T03-T11')
ck('no_empty_packet_hyp',pk.rule_hypotheses.fillna('').str.len().gt(0).all())
res={'status':'PASS' if not e else 'FAIL','checks':c,'errors':e};json.dump(res,open(os.path.join(R,'VALIDATION/VALIDATION_RESULT_R7.json'),'w'),indent=2);print(json.dumps(res,indent=2));sys.exit(1 if e else 0)
