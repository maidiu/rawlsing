"""Phase A owner/environment assertions, never a WG0P4 verdict."""
from pathlib import Path
import ast,hashlib,importlib,json,subprocess,sys,os,pytest
from precommitted_contract import ORACLE,CASES,assert_cold
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root'
def test_frozen_oracle_unchanged_and_65_hostiles_ready():
 digest=(R/'observations/frozen_oracle.sha256').read_text().split()[0]
 assert hashlib.sha256((R/'01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json').read_bytes()).hexdigest()==digest
 assert len(CASES)==65 and len(ORACLE['operations'])==25
 assert {s:sum(o['disposition']==s for o in ORACLE['operations']) for s in ('PRODUCED','HELD','INADMISSIBLE')}=={'PRODUCED':3,'HELD':16,'INADMISSIBLE':6}
@pytest.mark.parametrize('path,blob',list(ORACLE['required_owner_blobs'].items())+[('rawlsing_next/pre553_c11_integrity.py','7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd')])
def test_actual_module_file_and_git_hash_object(path,blob):
 m=importlib.import_module(path[:-3].replace('/','.'));physical=Path(m.__file__)
 assert physical==RT/path
 assert subprocess.check_output(['git','hash-object',str(physical)]).decode().strip()==blob
 data=physical.read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob

def test_genuine_original_manifest_cross_process_owner_rehearsal():
 p=subprocess.run([sys.executable,str(R/'repro/owner_cold_rehearsal.py'),'orchestrate'],capture_output=True,text=True)
 (R/'observations/owner_cold_rehearsal.stdout').write_text(p.stdout+p.stderr)
 assert p.returncode==0,p.stdout+p.stderr
 e=json.loads((R/'observations/owner_cold_rehearsal.json').read_text());assert_cold(e)
 assert e['summary']['populated_data_execution_claim'] is False

def test_original_test_sources_remain_unmodified():
 s=json.loads((R/'source_selector_phase_a.json').read_text())
 for row in s['files']:
  p=RT/row['staged_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']

def test_precommitted_suite_collects_65_without_candidate_execution():
 env=dict(os.environ);p=subprocess.run([sys.executable,'-m','pytest',str(R/'tests/test_precommitted_phase_b.py'),'--collect-only','-q'],env=env,capture_output=True,text=True)
 (R/'observations/precommitted_collection.stdout').write_text(p.stdout+p.stderr)
 assert p.returncode==0 and '65 tests collected' in p.stdout
