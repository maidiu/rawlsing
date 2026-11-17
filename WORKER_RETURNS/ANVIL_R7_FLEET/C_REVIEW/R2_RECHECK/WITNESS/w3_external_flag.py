#!/usr/bin/env python3
"""R2 recheck W3 witness: a self-asserted EXTERNAL_RUNNER_VERIFIED flag plus a
fabricated local receipt can reach C_CONDITIONALLY_ADMIT_DESIGN without any
authenticated external custody. The gate checks a string, not a trust root."""
import hashlib, json, pathlib, shutil, sys, tempfile

R2 = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R2_RECHECK')
TS=(R2/'LOGS/STAMP').read_text().strip(); PKG=R2/f'COLD/FRESH_{TS}/ANVIL_R7'; TOOLS=PKG/'tools'
sys.path.insert(0,str(TOOLS))
from r7_integrated import check, sha  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R2/'WITNESS/W3_EXTERNAL_FLAG'; OUT.mkdir(parents=True,exist_ok=True)
tmp=pathlib.Path(tempfile.mkdtemp(prefix='w3_',dir=str(OUT))); ev=tmp/'EVIDENCE'; shutil.copytree(PKG/'EVIDENCE',ev); source=ev/'SOURCE_118'
mod=source/'fixture_module.py'; mod.write_text('def producer():\n    return 1\n\ndef consumer():\n    return 1\n')
c=json.loads((ev/'C.json').read_text())
log=ev/'fake_runner.log'; log.write_text('fake local stdout that was never executed\n')
cmd='python3 tools/test_r7_integrated.py -q'
receipt={'schema':'ANVIL_R7_EXECUTION_TEST_RECEIPT','command':cmd,'exit_code':0,'execution_kind':'REAL_RUN',
 'first_consumer_effect':'claimed external first-consumer effect','negative_refusal':'claimed refusal',
 'restore_replay':'claimed restore','runner_code_head':'b'*40,'source_or_fixture_sha256':sha((ev/'DECISION.json').read_bytes())}
(ev/'fake_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
present={'id':'present','domain':'CURRENT_FIRST_CONSUMER','grade':'EXECUTED_FIRST_READER_PROOF',
 'producer_symbol':'fixture_module.py::producer','consumer_symbol':'fixture_module.py::consumer',
 'source_head':'a'*40,'producer_sha256':sha(mod.read_bytes()),'consumer_sha256':sha(mod.read_bytes()),
 'test_command':cmd,'first_consumer':'external claimed source consumer',
 'executed_test_receipt':{'path':'fake_receipt.json','sha256':sha((ev/'fake_receipt.json').read_bytes())},
 'receipt':{'argv':['python3','tools/test_r7_integrated.py','-q'],
   'raw_log':{'path':'fake_runner.log','sha256':sha(log.read_bytes())},'host':'claimed-external',
   'time':'2026-11-17T00:00:00Z','runner_head':'a'*40,'stdout_sha256':sha(log.read_bytes()),
   'test_command':cmd,'execution_custody':'EXTERNAL_RUNNER_VERIFIED'}}
future={'id':'future','domain':'FUTURE_NONPRECLUSION','grade':'EXACT_BUILDER_HOLD',
 'exact_hold':'Future actor/world source governance remains an independent owner hold.'}
c['verdict']='C_CONDITIONALLY_ADMIT_DESIGN'; c['actual_first_reader_verified']=True
c['builder_cards']=[present,future]; c['choice_reversing_objection_survives']=False
# Keep the C prose honest about the lack of real external evidence; the gate must
# not promote it to conditional admission merely because the flag is set.
c['actual_first_consumer_assessment']=('This packet contains only a self-asserted external-runner flag and a local fake stdout; '
 'no authenticated external custody or actual native first consumer exists in this review.')
(ev/'C.json').write_text(json.dumps(c,sort_keys=True,indent=2)+'\n')
res=check('C_INTEGRATED',c,ev,source,REPO,ZIP)
report={'schema':'C_REVIEW_R2_W3_EXTERNAL_FLAG','C_INTEGRATED':res,
        'verdict':'EXTERNAL_FLAG_ADMISSION_CONFIRMED_IF_PASS' if res['status'].startswith('PASS') else 'EXTERNAL_FLAG_REFUSED'}
(OUT/'w3_result.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
