"""One-command reproduction; original source/fixtures remain byte-unchanged."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,xml.etree.ElementTree as ET
from materialize import ROOT,materialize


def run(args,cwd,label,*,env=None,expected=0):
    process=subprocess.run(args,cwd=cwd,text=True,capture_output=True,env=env)
    def portable(s):return s.replace(str(ROOT),'<B2_RETURN>').replace(str(Path.home()),'<HOME>')
    (ROOT/'evidence'/f'{label}.log').write_text(portable(process.stdout))
    if process.stderr:(ROOT/'evidence'/f'{label}.stderr.log').write_text(portable(process.stderr))
    result=dict(label=label,command=args,cwd=str(cwd.relative_to(ROOT)),exit_code=process.returncode,
                expected_exit=expected,log='evidence/'+label+'.log')
    assert process.returncode==expected,result
    return result


def main():
    materialize();(ROOT/'evidence').mkdir(exist_ok=True)
    commands=[]
    for name,tests,out in [('B1',['test_bfirst.py'],'b1'),('P1',['tests/test_p1_contract.py','tests/test_p1_completion.py'],'p1'),
                           ('F1/court/f1_frozen_court',['test_frozen_contract.py'],'f1')]:
        cwd=ROOT/'imports'/name
        junit=os.path.relpath(ROOT/'evidence'/f'{out}.xml',cwd)
        commands.append(run(['python3','-m','pytest','-q',*tests,'--junitxml='+junit],cwd,out))
    for source,out in [('03_SOURCEFREE_CAPABILITY_COURT.js','d1_original'),('07_CORRECTED_ABSENCE_CONTRACT_COURT.js','d1_corrected')]:
        commands.append(run(['node',source],ROOT/'imports/D1',out))
    commands.append(run(['python3','-m','pytest','-q','test_integration.py','test_f1_adapter.py','--junitxml=evidence/integration.xml'],ROOT,'integration'))
    commands.append(run(['python3','bridge.py','evidence/vertical'],ROOT,'vertical'))
    commands.append(run(['python3','bridge.py','replay','evidence/vertical/positive/trace.json'],ROOT,'cold_replay'))
    positive=json.loads((ROOT/'evidence/vertical/positive/trace.json').read_text())
    cold=json.loads((ROOT/'evidence/cold_replay.log').read_text())
    assert cold['final_hash']==positive['final_hash']
    assert cold['receipts']==[episode['receipt'] for episode in positive['episodes']]
    commands.append(run(['python3','f1_adapter.py'],ROOT,'f1_applicability'))
    env=dict(os.environ,PYTHONPATH=str(ROOT),F1_NATIVE_B1_ADAPTER='f1_adapter:run_case')
    native=run(['python3','run_native_b1.py'],ROOT/'imports/F1/court/f1_frozen_court','f1_native_gate',env=env,expected=1)
    native['environment']={'PYTHONPATH':'<B2_RETURN>','F1_NATIVE_B1_ADAPTER':'f1_adapter:run_case'};commands.append(native)
    for path in (ROOT/'evidence').glob('*.xml'):
        tree=ET.parse(path)
        for suite in tree.iter('testsuite'):suite.attrib.pop('hostname',None)
        tree.write(path,encoding='utf-8',xml_declaration=True)
    totals={}
    for label,expected in [('b1',39),('p1',74),('f1',97),('integration',81)]:
        suite=ET.parse(ROOT/'evidence'/f'{label}.xml').find('testsuite')
        totals[label]={k:int(suite.attrib[k]) for k in ('tests','failures','errors','skipped')}
        assert totals[label]==dict(tests=expected,failures=0,errors=0,skipped=0)
    original=(ROOT/'evidence/d1_original.log').read_text();corrected=(ROOT/'evidence/d1_corrected.log').read_text()
    assert 'D1 22 / 22 PASS' in original and 'D1 corrected court: 17 / 17' in corrected
    totals['d1_original']=dict(tests=22,grade='HISTORICAL_GUARD_KNOWN_ABSENCE_DEFECT')
    totals['d1_corrected']=dict(tests=17,grade='CORRECTED_RESEARCH_GUARD')
    rows=json.loads((ROOT/'evidence/f1_applicability.json').read_text())
    native_result=json.loads((ROOT/'evidence/f1_native_gate.log').read_text())
    na={r['case_id'] for r in rows if r['result']=='NOT_APPLICABLE_TO_THIS_LAB'}
    assert len(rows)==36 and len(na)==17 and len(native_result['failures'])==17
    assert {r['case_id'] for r in native_result['failures']}==na
    assert all(r['result'] in ('PASS_BOUNDARY_ONLY','NOT_APPLICABLE_TO_THIS_LAB') for r in rows)
    # Verify inherited bytes AGAIN after all execution. No regeneration of frozen data.
    materialize()
    (ROOT/'execution_receipt.json').write_text(json.dumps(dict(
        status='TEST_ONLY_BFIRST_INTEGRATED_PENDING_I2',commands=commands,totals=totals,
        new_tests=dict(connected_integration=45,frozen_applicability_accounting=36),
        f1=dict(reference_tests=97,dispatched_cases=36,boundary_negative_deferral_pass=19,
                native_positive_cases_passed=0,not_applicable=17,raw_native_exit=1,
                raw_native_status='RED',raw_native_failures=17),
        cold_replay='EXACT_RECEIPTS_AND_FINAL_STATE_HASH',
        sanitation='New JUnit hostname removed; new command outputs replace local root/home paths only; inherited bytes not edited.',
        implementation_setup_failure='Initial materializer used Git worktree-relative paths from wrong cwd, produced zero staged inputs; corrected before source imports or tests.',
        unexecuted=['production actor','original survey','live LLM','independent High/I2 acceptance']),indent=2)+'\n')
    print(json.dumps(dict(totals=totals,f1_boundary_pass=19,f1_not_applicable=17,cold_replay='EXACT'),sort_keys=True))

if __name__=='__main__':main()
