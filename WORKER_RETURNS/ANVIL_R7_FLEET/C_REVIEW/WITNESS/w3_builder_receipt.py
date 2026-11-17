#!/usr/bin/env python3
"""Independent C-review witness W3: the builder-card acceptance path.

A. A real interpreter command + structurally valid receipt is refused because the
   gate tests the first token ('python3') as a filesystem path, not the script.
B. The same non-executed fabricated receipt is accepted as an EXECUTED first-reader
   proof merely by creating a dummy file named 'python3' in the current directory.
This is a false C admission path from C_HOLD to C_CONDITIONALLY_ADMIT_DESIGN.
"""
import hashlib, json, os, pathlib, shutil, sys, tempfile

ROOT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW')
INT = ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION'
COLD = sorted((ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/TEMP').glob('COLD_*'))[-1]
TOOLS = COLD/'ANVIL_R7/tools'
sys.path.insert(0, str(TOOLS))
from r7_integrated import check, sha  # noqa: E402

REPO='/Users/matthewsmith/s2b-work/rawlsing'
ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/WITNESS/W3_BUILDER_RECEIPT'
OUT.mkdir(parents=True, exist_ok=True)
base=pathlib.Path(tempfile.mkdtemp(prefix='w3_',dir=str(OUT)))
ev=base/'EVIDENCE'; shutil.copytree(INT/'EVIDENCE',ev)
source=ev/'SOURCE_118'
# Add a synthetic but real source-tree module so check_builder's symbol check can be satisfied.
mod=(source/'fixture_module.py')
mod.write_text('def producer():\n    return 1\n\ndef consumer():\n    return 1\n')
c=json.loads((ev/'C.json').read_text())
log=(ev/'fake_runner.log'); log.write_text(json.dumps({'stdout':'synthetic local fake receipt: not an execution'},sort_keys=True)+'\n')
receipt={
 'schema':'ANVIL_R7_EXECUTION_TEST_RECEIPT',
 'command':'python3 tools/test_r7_integrated.py -q',
 'exit_code':0,
 'execution_kind':'FIXTURE_ONLY',
 'first_consumer_effect':'Synthetic local receipt claims a first-consumer effect',
 'negative_refusal':'Synthetic local receipt claims a refusal case',
 'restore_replay':'Synthetic local receipt claims byte restore',
 'runner_code_head':'a'*40,
 'source_or_fixture_sha256':sha((ev/'DECISION.json').read_bytes()),
}
(ev/'fake_receipt.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
present={
 'id':'present','domain':'CURRENT_FIRST_CONSUMER','grade':'EXECUTED_FIRST_READER_PROOF',
 'producer_symbol':'fixture_module.py::producer','consumer_symbol':'fixture_module.py::consumer',
 'source_head':'a'*40,
 'producer_sha256':sha(mod.read_bytes()),'consumer_sha256':sha(mod.read_bytes()),
 'test_command':'python3 tools/test_r7_integrated.py -q','first_consumer':'sourcefree synthetic fixture consumer',
 'executed_test_receipt':{'path':'fake_receipt.json','sha256':sha((ev/'fake_receipt.json').read_bytes())},
 'receipt':{'argv':['python3','tools/test_r7_integrated.py','-q'],'raw_log':{'path':'fake_runner.log','sha256':sha(log.read_bytes())},
            'host':'local-fake','time':'2026-11-17T00:00:00Z','runner_head':'a'*40,
            'stdout_sha256':sha(log.read_bytes()),'test_command':'python3 tools/test_r7_integrated.py -q'},
}
future={'id':'future','domain':'FUTURE_NONPRECLUSION','grade':'EXACT_BUILDER_HOLD',
        'exact_hold':'Future actor/world source governance remains an independent owner hold.'}
c['verdict']='C_CONDITIONALLY_ADMIT_DESIGN'
c['actual_first_reader_verified']=True
c['builder_cards']=[present,future]
c['choice_reversing_objection_survives']=False
(ev/'C.json').write_text(json.dumps(c,sort_keys=True,indent=2)+'\n')

# A: cwd = tools, no file named 'python3'
os.chdir(TOOLS)
a=check('C_INTEGRATED',c,ev,source,REPO,ZIP)
# B: cwd = dummy dir with a file named 'python3'; command is never executed by the gate
dummy=base/'dummy_cwd'; dummy.mkdir(); (dummy/'python3').write_text('not an interpreter\n')
os.chdir(dummy)
b=check('C_INTEGRATED',c,ev,source,REPO,ZIP)
report={'schema':'C_REVIEW_WITNESS_W3',
        'A_real_command_no_dummy':a,
        'B_real_command_with_dummy_python3':b,
        'meaning':'A refuses a real-looking command due to first-token path check; B passes the same non-executed receipt when a dummy python3 file exists.',
        'verdict':'WITNESS_CONFIRMED_IF_A_RED_AND_B_PASS' if a['status']=='RED' and b['status'].startswith('PASS') else 'PARTIAL_OR_REFUTED'}
(OUT/'w3_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
