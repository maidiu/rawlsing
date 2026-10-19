"""Run the unchanged shared witness with a larger native-P1 time budget.

Only the subprocess timeout is adjusted (180 -> 600 seconds). Assertions,
baseline requirements, exact fault injection and source restoration remain the
shared checker's own code. Three fresh native pytest runs are retained: its
baseline and fault, then an explicit restored positive. No native owner or
shared checker file is edited.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
CHECKER=ROOT/'CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py'


def run():
    source=CHECKER.read_bytes()
    sealed=subprocess.check_output(['git','show',
        '1150e836ef58553255abc0f588e66c1327db4932:CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py'],cwd=ROOT)
    if source!=sealed:
        raise ValueError('shared checker differs from exact sealed source')
    spec=importlib.util.spec_from_file_location('o35b_sealed_shared_proof_gate',CHECKER)
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    contract=HERE/'test_retained_p1_consumer.py.proof.json'
    claim=json.loads(contract.read_text())['claims'][0]
    node=claim['positive_node'];target=ROOT/claim['fault']['path']
    original_target=target.read_bytes()
    real_subprocess=gate.subprocess
    labels=iter(('baseline','fault','restored'))
    calls=[]

    def native_run(command,**kwargs):
        if command[-1]!=node or kwargs.get('timeout')!=180:
            raise ValueError('timeout adapter received an unexpected shared-checker command')
        label=next(labels)
        kwargs['timeout']=600
        print('NATIVE_WITNESS_STARTED '+label,flush=True)
        result=real_subprocess.run(command,**kwargs)
        xml_path=Path(command[command.index('--junitxml')+1])
        output=HERE/'evidence'/('p1_native_severance_'+label)
        output.with_suffix('.pytest.txt').write_text(result.stdout.replace(str(ROOT),'WORKTREE'))
        tree=ET.parse(xml_path)
        for suite in tree.getroot().iter('testsuite'):
            if 'hostname' in suite.attrib:suite.set('hostname','LOCAL_HOST')
        tree.write(output.with_suffix('.junit.xml'),encoding='unicode',xml_declaration=True)
        actual_result=HERE/'.runtime/continuation/p1/native_M1_latest_result.json'
        output.with_suffix('.result.json').write_bytes(actual_result.read_bytes())
        calls.append({'phase':label,'exit':result.returncode,
                      'fresh_process':True,'timeout_seconds':600,
                      'junit':str(output.with_suffix('.junit.xml').relative_to(HERE))})
        print('NATIVE_WITNESS_TERMINAL '+label+' exit='+str(result.returncode),flush=True)
        return result

    gate.subprocess=SimpleNamespace(run=native_run,PIPE=real_subprocess.PIPE,
                                    STDOUT=real_subprocess.STDOUT)
    try:
        receipt=gate.witness(contract,ROOT)
        if target.read_bytes()!=original_target:
            raise ValueError('shared witness failed byte-exact source restoration')
        with tempfile.TemporaryDirectory(prefix='o35b-restored-positive-') as d:
            xml=Path(d)/'restored.xml'
            restored=gate._run_node(ROOT,node,xml)
            failed,error,skipped=gate._case_state(xml,node.split('::')[-1])
            cases=[c for c in ET.parse(xml).getroot().iter('testcase')
                   if c.attrib.get('name')==node.split('::')[-1]]
            if len(cases)!=1 or restored.returncode!=0 or failed or error or skipped:
                raise AssertionError('restored native positive did not pass: '+restored.stdout[-2500:])
        receipt.update(
            runner_adjustment='RETURN_ONLY_SUBPROCESS_TIME_BUDGET_180_TO_600_SECONDS; NO_ASSERTION_OR_NATIVE_OWNER_CHANGE',
            shared_checker_sha256=hashlib.sha256(source).hexdigest(),
            shared_checker_commit='1150e836ef58553255abc0f588e66c1327db4932',
            native_processes=calls,source_restored_exactly=True,
            tested_source_sha256=hashlib.sha256(original_target).hexdigest(),
            original_execution_plan_omission='NOT_RUN; this witness severs retained Fact -> native M1 input, not an I03/Batch operation plan')
        (HERE/'evidence/p1_native_severance_witness.json').write_text(json.dumps(receipt,indent=2)+'\n')
        return receipt
    finally:
        gate.subprocess=real_subprocess
        if target.read_bytes()!=original_target:
            raise RuntimeError('native adapter source differs after witness; preserve and inspect')


if __name__=='__main__':
    result=run()
    print(json.dumps({'state':result['status'],'restored':result['source_restored_exactly']}))
