#!/usr/bin/env python3
"""Local synthetic/structural test runner; NEVER a source-science or independent-review verdict."""
import json,subprocess,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
SCRIPTS=['test_r5.py','test_stage.py','test_compare.py','test_anvil.py','test_r4.py','preflight_launches.py','test_r6.py','test_r6_design_ready.py','test_conservation.py']
records=[]
for script in SCRIPTS:
    p=subprocess.run([sys.executable,str(ROOT/'tools'/script)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=30)
    report={'command':'python3 tools/'+script,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    records.append(report)
    (ROOT/'tests'/script.replace('.py','.json')).write_text(json.dumps(report,indent=2)+'\n')
status='PASS_LOCAL_SYNTHETIC_AND_FORMAT_ONLY' if all(x['exit_code']==0 for x in records) else 'RED_LOCAL_TEST_FAILURE'
summary={'status':status,'tests':[{'command':x['command'],'exit_code':x['exit_code']} for x in records], 'scope':'LOCAL_SYNTHETIC_AND_FORMAT_ONLY_NO_GITHUB_CURRENTNESS_NO_ORIGINAL_SOURCE_NO_INDEPENDENT_RECEIVING','canonical_mcr_lite_checker':'SOURCE_INSPECTED_ON_GITHUB_NOT_EXECUTED_IN_ACTUAL_CHECKOUT','full_native_scale':'NOT_EXECUTED','scientific_or_actor_grant':'NOT_GRANTED'}
(ROOT/'tests'/'QUALITY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
sys.exit(0 if status.startswith('PASS') else 2)
