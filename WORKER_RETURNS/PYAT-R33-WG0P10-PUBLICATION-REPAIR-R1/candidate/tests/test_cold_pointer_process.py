"""Additional actual fresh-process pointer forgery, using genuine prior receipt."""
import json,os,shutil,subprocess,sys,uuid
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_fresh_process_pointer_substitution_cannot_restore_signed_prior_facts():
 summary=json.loads((R/'court/observations/phase_b/inherited_v1/observations/cold_comparison.json').read_text())
 source=Path(summary['cold_directory'])
 folder=R/'runtime'/('cold-pointer-'+uuid.uuid4().hex);folder.mkdir()
 shutil.copytree(source/'owner',folder/'owner');shutil.copy2(source/'checkpoint.json',folder/'checkpoint.json')
 child=subprocess.run([sys.executable,'-B',str(R/'repro/cold_pointer_worker.py'),str(folder)],capture_output=True,text=True,env=os.environ)
 result=json.loads((folder/'result.json').read_text())
 result['child_exit']=child.returncode;result['stdout']=child.stdout;result['stderr']=child.stderr
 result['original_crash_pid']=json.loads((source/'crash.json').read_text())['pid']
 assert child.returncode==0 and result['pid']!=result['original_crash_pid']
 assert result['error']['type']=='IdentityError' and result['new_I03_calls']==0
 assert result['same_original_manifest'] and result['manifest_units']==3
 assert result['owner_journal_unchanged'] and result['custody_unchanged'] and result['restored_receipts']==0
 (R/'observations/fresh_process_source_pointer_refusal.json').write_text(json.dumps(result,indent=2)+'\n')
