#!/usr/bin/env python3
"""Complete local R5/R6/mainMAC/R7 synthetic and format regression runner.

Does NOT run a source-native 100k benchmark, certify independent review, or
exercise real GitHub/host-scoped source rights. Explicitly record those holds.
"""
from __future__ import annotations
import json,pathlib,subprocess,sys,traceback
ROOT=pathlib.Path(__file__).resolve().parents[1]
LEGACY=[['tools/run_quality.py']]
MAINMAC=[['tools/preflight.py'],['tools/test_r6.py']]
R7=[['tools/test_r7_decision.py'],['tools/test_r7_stage.py'],['tools/test_r7_typed.py'],['tools/test_r7_conservation.py'],['tools/test_r7_synthesis.py'],['tools/test_r7_integrated.py']]
results=[]
for group,base,files in [('R5_R6_INHERITED',ROOT,LEGACY),('MAINMAC_R6_REFERENCE',ROOT/'MAINMAC_R6_REFERENCE/ANVIL_R6',MAINMAC),('MAINMAC_R7_REFERENCE',ROOT/'MAINMAC_R7_REFERENCE', [['tools/preflight.py'],['tools/test_r7.py']]),('R7_NEW',ROOT,R7)]:
    for item in files:
        cmd=[sys.executable,*item]
        try:
            r=subprocess.run(cmd,cwd=base,timeout=120,capture_output=True,text=True)
            exit_code=r.returncode;so=r.stdout;se=r.stderr
        except (OSError,subprocess.TimeoutExpired) as ex:exit_code=127;so='';se=repr(ex)
        results.append({'group':group,'command':' '.join([sys.executable,*item]),'cwd':str(base.relative_to(ROOT)),
                        'exit_code':exit_code,'stdout_tail':so[-12000:],'stderr_tail':se[-12000:]})
    # R6 inherited quality runner uses NINE subprocesses; independently inspect
    # its JSON record to prevent an umbrella process concealing failures.
    if group=='R5_R6_INHERITED':
        try:
            report=json.loads((ROOT/'tests/QUALITY_SUMMARY.json').read_text())
            checks=report['tests'];valid=len(checks)==9 and all(z['exit_code']==0 for z in checks)
            results.append({'group':'R5_R6_INHERITED_SUBTESTS','command':'verify run_quality.py nine actual child results',
                            'cwd':'.','exit_code':0 if valid else 2,'subtests':[{'command':z['command'],'exit_code':z['exit_code']} for z in checks]})
        except (OSError,KeyError,ValueError,TypeError) as ex:results.append({'group':'R5_R6_INHERITED_SUBTESTS','exit_code':2,'error':str(ex)})
status='PASS_LOCAL_SYNTHETIC_AND_FORMAT_ONLY' if all(z['exit_code']==0 for z in results) else 'RED_LOCAL_TEST_FAILURE'
record={'schema':'ANVIL_R7_QUALITY_REPORT','status':status,'commands_checked':len(results),
    'R5_R6_original_child_tests':9,'mainmac_original_tests':38,'R7_new_unittest_cases':'see actual executed tool stdout',
    'R7_new_cases_note':'Computed from test methods at this source cut; rely on actual stdout for exact count',
    'scope':'RECONSTRUCTED_SYNTHETIC_AND_FORMAT_ONLY__NO_NATIVE_ORIGINAL_SOURCE_100K_FULL_PHYSICAL_RUN__NO_INDEPENDENT_C__NO_PROTECTED_H1',
    'tests':results}
(ROOT/'tests/R7_QUALITY_REPORT.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':status,'commands_checked':len(results),'exit_codes':[z['exit_code'] for z in results],
    'record':'tests/R7_QUALITY_REPORT.json','scope':record['scope']},indent=2))
sys.exit(0 if status.startswith('PASS') else 2)
