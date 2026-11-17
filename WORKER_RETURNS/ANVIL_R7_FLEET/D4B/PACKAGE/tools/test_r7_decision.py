#!/usr/bin/env python3
"""R7 genuine receipt-content tests, entirely synthetic. Cannot issue source or runner authority."""
import copy,hashlib,json,pathlib,tempfile,unittest,sys
from r7_decision import compare,check_decision_dag,digest,sha,POL,FLOOR,CEILING,ROOT
HEAD='7fc00289dd801d2d0a8ce159986c7595fc27a4d9'

def make_fixture(where):
    root=pathlib.Path(where);cells=[];measurements=[]
    f={'schema':'ANVIL_R7_FROZEN_PLAN','policy_sha256':sha((ROOT/'24_R7_MACHINE_POLICY.json').read_bytes()),'version':1,'scope':'C11_QUERY_DESIGN','phase':'FROZEN_BEFORE_FIRST_RESULT','source_cut':HEAD,'candidate_code_heads':{'A':HEAD,'B':'b'*40},'cells':cells,'exclusions':[],'B_discriminators':[]}
    for case,metric in sorted(FLOOR):
        cid=case+'__'+metric
        geom=600 if case in ('W-D','W-S') else 100
        events=(3*100000 if case=='W-S' else geom*100000)
        c=dict(id=cid,workload_case_id=case,metric=metric,input_sha256='c'*64,respondent_count=100000,source_width=geom,event_count=events,source_cut=HEAD,source_grade='SOURCEFREE_SYNTHETIC',fixture_id='SOURCEFREE_SYNTHETIC_100K',runner_id='LOCAL_SYNTHETIC_RUNNER',first_consumer_id='SOURCEFREE_I03_FULL_FIRST_READER',negative_restore_oracle='SOURCEFREE_DENY_AND_RESTORE_CHECK')
        cells.append(c)
        m={'cell_id':cid}
        for side in ('A','B'):
            a,b=(1*1024**3,2*1024**3) if metric=='process_tree_peak_rss_bytes' else (10,20)
            lo,value,hi=([a-1,a,a+1] if side=='A' else [b-1,b,b+1])
            p=f'receipt_{cid}_{side}.json'
            rec=dict(schema='ANVIL_R7_MEASUREMENT_RECEIPT',candidate=side,cell_id=cid,workload_case_id=case,metric=metric,unit=POL['metric_units'][metric],source_cut=HEAD,source_grade=c['source_grade'],fixture_id=c['fixture_id'],runner_id=c['runner_id'],code_head=f['candidate_code_heads'][side],input_sha256=c['input_sha256'],clock_id='SYNTHETIC_TEST_UTC_2026_11_17',first_consumer_id=c['first_consumer_id'],negative_restore_oracle=c['negative_restore_oracle'],runner_command='python tools/test_r7_decision.py',source_width_label='synthetic 100k respondent scope',source_width=geom,respondent_count=100000,event_count=events,low=lo,value=value,high=hi,execution_kind='SYNTHETIC_TEST')
            blob=(json.dumps(rec,sort_keys=True)+'\n').encode();(root/p).write_bytes(blob)
            m[side]=dict(status='MEASURED',receipt_path=p,receipt_sha256=sha(blob),low=lo,value=value,high=hi)
        measurements.append(m)
    fsha=digest(f)
    v=[]
    for side in ('A','B'):
        for vid in POL['required_non_numeric_vetoes']:
            p='veto_'+side+'_'+vid+'.json'
            rec=dict(schema='ANVIL_R7_VETO_RECEIPT',candidate=side,id=vid,status='PASS_AT_MEASURED_SCOPE',source_cut=HEAD,code_head=f['candidate_code_heads'][side],first_consumer_id='SOURCEFREE_I03_FULL_FIRST_READER',negative_or_refusal='SYNTHETIC_REFUSAL_AND_RESTORE',restoration='SYNTHETIC_REPLAY_SAME_ROOT',source_grade='SOURCEFREE_SYNTHETIC')
            blob=(json.dumps(rec,sort_keys=True)+'\n').encode();(root/p).write_bytes(blob)
            v.append(dict(candidate=side,id=vid,status=rec['status'],receipt_path=p,receipt_sha256=sha(blob)))
    d=dict(schema='ANVIL_R7_COMPARATOR_INPUT',candidate_ids=['A','B'],frozen_sha256=fsha,measurements=measurements,hard_veto_checks=v)
    return d,f

def replace_receipt(root,d,cell,side,changes):
    entry=d['measurements'][cell][side];p=root/entry['receipt_path'];rec=json.loads(p.read_text());rec.update(changes)
    b=(json.dumps(rec,sort_keys=True)+'\n').encode();p.write_bytes(b);entry['receipt_sha256']=sha(b)
    for k in ('low','value','high'):
        if k in changes:entry[k]=changes[k]

class R7Tests(unittest.TestCase):
    def setUp(self):
        self.d=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.d.name);self.data,self.frozen=make_fixture(self.root)
    def tearDown(self):self.d.cleanup()
    def check(self):return compare(self.data,self.frozen,self.root)
    def assertRed(self):
        r=self.check();self.assertEqual('RED',r['status'],r)
    def test_positive_A(self):self.assertEqual(('A_DOMINATES_RECEIPT_BOUND_MATERIAL_SET','A'),(self.check()['status'],self.check()['winner']))
    def test_positive_B(self):
        for i,m in enumerate(self.data['measurements']):
            if m['A']['value'] and m['B']['value']:
                a,b=(m['A']['low'],m['A']['value'],m['A']['high']),(m['B']['low'],m['B']['value'],m['B']['high'])
                replace_receipt(self.root,self.data,i,'A',dict(zip(('low','value','high'),b)))
                replace_receipt(self.root,self.data,i,'B',dict(zip(('low','value','high'),a)))
        self.assertEqual(('B_DOMINATES_RECEIPT_BOUND_MATERIAL_SET','B'),(self.check()['status'],self.check()['winner']))
    def test_both_over_ceiling(self):
        for i,m in enumerate(self.data['measurements']):
            if 'process_tree_peak_rss_bytes' in m['cell_id']:
                replace_receipt(self.root,self.data,i,'A',{'low':7*1024**3,'value':7*1024**3+1,'high':7*1024**3+2})
                replace_receipt(self.root,self.data,i,'B',{'low':8*1024**3,'value':8*1024**3+1,'high':8*1024**3+2})
        r=self.check();self.assertEqual(('BOTH_INFEASIBLE',None),(r['status'],r['winner']))
    def test_one_over_ceiling(self):
        for i,m in enumerate(self.data['measurements']):
            if 'process_tree_peak_rss_bytes' in m['cell_id']:
                replace_receipt(self.root,self.data,i,'A',{'low':7*1024**3,'value':7*1024**3+1,'high':7*1024**3+2})
        r=self.check();self.assertEqual(('ONLY_B_FEASIBLE_AT_MEASURED_SCOPE','B'),(r['status'],r['winner']))
    def test_rss_interval_crosses_ceiling(self):
        i=next(i for i,m in enumerate(self.data['measurements']) if 'process_tree_peak_rss_bytes' in m['cell_id'])
        replace_receipt(self.root,self.data,i,'A',{'low':CEILING-10,'value':CEILING,'high':CEILING+10})
        self.assertEqual(('FEASIBILITY_HELD',None),(self.check()['status'],self.check()['winner']))
    def test_numeric_json_tamper_unchanged_receipts(self):self.data['measurements'][0]['A']['value']=14;self.assertRed()
    def test_numeric_receipt_tamper_unchanged_hash(self):
        p=self.root/self.data['measurements'][0]['A']['receipt_path'];p.write_text(p.read_text().replace('"value": 10','"value": 14'));self.assertRed()
    def test_veto_json_tamper(self):self.data['hard_veto_checks'][0]['status']='FAIL';self.assertRed()
    def test_veto_receipt_tamper(self):
        p=self.root/self.data['hard_veto_checks'][0]['receipt_path'];p.write_text(p.read_text()+'garbage');self.assertRed()
    def test_mandatory_measurement_omitted(self):
        self.frozen['cells'].pop();self.data['measurements'].pop();self.data['frozen_sha256']=digest(self.frozen);self.assertRed()
    def test_six_excluded(self):
        self.frozen['cells']=self.frozen['cells'][:1];self.frozen['exclusions']=[{'reason':'not material'}]*10;self.data['measurements']=self.data['measurements'][:1];self.data['frozen_sha256']=digest(self.frozen);self.assertRed()
    def test_missing_rival(self):self.data['measurements'][0]['B']['status']='UNRUN_HELD';self.assertRed()
    def test_fake_receipt_path(self):self.data['measurements'][0]['A']['receipt_path']='not_exists';self.assertRed()
    def test_path_escape(self):self.data['measurements'][0]['A']['receipt_path']='../../etc/passwd';self.assertRed()
    def test_frozen_tamper(self):self.frozen['cells'][0]['runner_id']='DIFFERENT';self.assertRed()
    def test_B_discriminator_unresolved(self):
        self.frozen['B_discriminators']=[{'status':'EXACT_HOLD','B_source_ref':'source rights open'}];self.data['frozen_sha256']=digest(self.frozen);self.assertRed()
    def test_overlap_not_tiebreak(self):
        replace_receipt(self.root,self.data,0,'A',{'low':8,'value':15,'high':22})
        self.assertEqual(('UNRESOLVED_MATERIAL_INTERVAL',None),(self.check()['status'],self.check()['winner']))
    def test_semantic_veto_failure(self):
        v=self.data['hard_veto_checks'][0];p=self.root/v['receipt_path'];r=json.loads(p.read_text());r['status']='FAIL';blob=(json.dumps(r,sort_keys=True)+'\n').encode();p.write_bytes(blob);v.update(status='FAIL',receipt_sha256=sha(blob))
        self.assertNotEqual('A_DOMINATES_RECEIPT_BOUND_MATERIAL_SET',self.check()['status'])
    def test_sparse_density_misreported_as_dense(self):
        i=next(i for i,m in enumerate(self.data['measurements']) if m['cell_id'].startswith('W-D__'))
        replace_receipt(self.root,self.data,i,'A',{'source_width':3,'event_count':300000})
        self.assertRed()
    def test_old_R5_physical_decision_cannot_disappear(self):
        from test_r6 import r6_fixture
        ledger=make_ledger(self.frozen)
        ledger['physical_decisions'][0]['inherited_R5_physical_decision_id']='SOME_OTHER_UNVERIFIED_PHYSICAL_DECISION'
        errors=check_decision_dag(ledger,self.check(),self.frozen,r6_fixture())
        self.assertTrue(any('R5_PHYSICAL' in x for x in errors),errors)
    def test_wrong_case_with_same_cost_metric_cannot_substitute(self):
        ledger=make_ledger(self.frozen)
        d=ledger['physical_decisions'][0]
        i=next(i for i,cid in enumerate(d['material_cell_ids']) if cid=='W-R__cold_open_wall_s')
        d['material_cell_ids'].pop(i);d['material_effects'].pop(i)
        self.assertTrue(any('LACKS_REQUIRED_MATERIAL_CASES' in x for x in check_decision_dag(ledger,self.check(),self.frozen)))
    def test_numeric_value_mismatches_unchanged_valid_receipt_sha(self):
        self.data['measurements'][0]['B']['low']=-1
        self.assertRed()

    def test_positive_decision_dag(self):
        ledger=make_ledger(self.frozen)
        self.assertEqual([],check_decision_dag(ledger,self.check(),self.frozen))
    def test_nonexistent_dependency(self):
        l=make_ledger(self.frozen);l['physical_decisions'][1]['depends_on']=['NONEXISTENT']
        self.assertIn('R7_NONEXISTENT_OR_DUPLICATE_DEPENDENCY:P-INDEX',check_decision_dag(l,self.check(),self.frozen))
    def test_borrow_build_only_for_storage(self):
        l=make_ledger(self.frozen);d=l['physical_decisions'][0];d['material_cell_ids']=d['material_cell_ids'][:1];d['material_effects']=d['material_effects'][:1]
        self.assertTrue(any('LACKS_REQUIRED_COST_DIMENSIONS' in e for e in check_decision_dag(l,self.check(),self.frozen)))
    def test_dependency_cycle(self):
        l=make_ledger(self.frozen);l['physical_decisions'][0]['depends_on']=['P-INDEX']
        self.assertIn('R7_DECISION_DEPENDENCY_CYCLE',check_decision_dag(l,self.check(),self.frozen))
    def test_no_independent_proof_claim(self):self.assertIn('NOT_INDEPENDENTLY',self.check()['runner_proof'])

    def test_valid_B_discovered_metric_pre_result_amendment(self):
        base=copy.deepcopy(self.frozen);base['first_results_seen']=False
        bb=(json.dumps(base,sort_keys=True)+'\n').encode();(self.root/'parent.json').write_bytes(bb)
        new=copy.deepcopy(self.frozen);new['version']=2;new['first_results_seen']=False
        new['parent_plan_ref']={'path':'parent.json','sha256':sha(bb)}
        new['new_metric_units']={'branch_refresh_wall_s':'s'}
        review={'schema':'ANVIL_R7_C_DISCRIMINATOR_REVIEW','new_metric':'branch_refresh_wall_s',
            'workload_case_id':'W-U','pre_result':True,'verdict':'MATERIAL_COMPARATOR_ADDITIONAL_DIMENSION'}
        rb=(json.dumps(review,sort_keys=True)+'\n').encode();(self.root/'B_C_review.json').write_bytes(rb)
        new['B_discriminators']=[{'status':'MEASURED_IN_AMENDED_POLICY','new_metric':'branch_refresh_wall_s',
            'workload_case_id':'W-U','B_source_ref':'B first consumer independently revealed shared branch refresh cost',
            'independent_C_receipt_path':'B_C_review.json','independent_C_receipt_sha256':sha(rb),
            'pre_result_amendment_sha256':sha(bb)}]
        c=dict(self.frozen['cells'][0]);c.update(id='W-U__branch_refresh_wall_s',workload_case_id='W-U',metric='branch_refresh_wall_s',source_width=100,event_count=10000000)
        new['cells'].append(c);m={'cell_id':c['id']}
        for side,baseval in [('A',10),('B',20)]:
            rr=dict(schema='ANVIL_R7_MEASUREMENT_RECEIPT',candidate=side,cell_id=c['id'],workload_case_id='W-U',
                metric=c['metric'],unit='s',source_cut=c['source_cut'],source_grade=c['source_grade'],
                fixture_id=c['fixture_id'],runner_id=c['runner_id'],code_head=new['candidate_code_heads'][side],input_sha256=c['input_sha256'],
                clock_id='SYNTHETIC_TEST_UTC_2026_11_17',first_consumer_id=c['first_consumer_id'],
                negative_restore_oracle=c['negative_restore_oracle'],runner_command='python tools/test_r7_decision.py',
                source_width_label='synthetic width',source_width=c['source_width'],respondent_count=c['respondent_count'],event_count=c['event_count'],
                low=baseval-1,value=baseval,high=baseval+1,execution_kind='SYNTHETIC_TEST')
            path='novel_'+side+'.json';blob=(json.dumps(rr,sort_keys=True)+'\n').encode();(self.root/path).write_bytes(blob)
            m[side]=dict(status='MEASURED',receipt_path=path,receipt_sha256=sha(blob),low=rr['low'],value=rr['value'],high=rr['high'])
        self.data['measurements'].append(m);self.data['frozen_sha256']=digest(new)
        result=compare(self.data,new,self.root)
        self.assertEqual('A_DOMINATES_RECEIPT_BOUND_MATERIAL_SET',result['status'],result)
        new_bad=copy.deepcopy(new);new_bad['parent_plan_ref']['sha256']='0'*64
        self.assertEqual('RED',compare(self.data,new_bad,self.root)['status'])
        new_bad=copy.deepcopy(new);new_bad['first_results_seen']=True
        self.assertEqual('RED',compare(self.data,new_bad,self.root)['status'])


def make_ledger(f):
    def choice(ident,clss,deps):
        req=set(POL['decision_class_metric_requirements'][clss]);req_pairs={tuple(z) for z in POL['decision_class_case_metric_requirements'][clss]};cells=[c for c in f['cells'] if c['metric'] in req or (c['workload_case_id'],c['metric']) in req_pairs]
        return dict(id=ident,inherited_R5_physical_decision_id='DK-PHYSICAL',decision_class=clss,selected_candidate='A',depends_on=deps,first_consumer_id='SOURCEFREE_I03_FIRST_READER',source_semantic_effect='Original instrument code and selection remain exact and available to first consumer',negative_and_restore_effect='Invalid rights CURRENT and changed source failure then restoration do not silently pass',material_cell_ids=[c['id'] for c in cells],material_effects=[dict(cell_id=c['id'],metric=c['metric'],workload_case_id=c['workload_case_id'],causal_dependency='This metric measures an affected cost through the actual source to first-reader path') for c in cells],hard_veto_ids=['SOURCE_SEMANTICS_AND_ROUTING'] if clss=='CANONICAL_SOURCE_LAYOUT' else [])
    return dict(schema='ANVIL_R7_PHYSICAL_DECISION_LEDGER',frozen_sha256=digest(f),physical_decisions=[choice('P-SOURCE','CANONICAL_SOURCE_LAYOUT',[]),choice('P-INDEX','PERSISTENT_INDEX',['P-SOURCE'])])

if __name__=='__main__':unittest.main(verbosity=2)
