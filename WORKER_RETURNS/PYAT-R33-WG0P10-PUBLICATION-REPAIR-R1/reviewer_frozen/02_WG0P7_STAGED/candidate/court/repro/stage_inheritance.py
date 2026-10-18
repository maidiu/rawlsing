"""WG0M exact historical inheritance. Does not resolve/read WG0P5."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1]
P='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-WG0L-INDEPENDENT-FULL-ENGINE-COURT-R1/'
PIN='bec9a128922e4e431ce2ed862aa7802c902813ed'
rows=[]
def stage(commit,source,dest,expected=None):
 data=subprocess.check_output(['git','-c','gc.auto=0','show',commit+':'+source],cwd=R)
 sha=hashlib.sha256(data).hexdigest()
 if expected and sha!=expected:raise RuntimeError(source)
 path=R/dest;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
 rows.append(dict(commit=commit,source_path=source,staged_path=dest,sha256=sha,git_blob_sha1=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),bytes=len(data)))
def old(source,dest=None):stage(PIN,P+source,dest or source)
for name in ['01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json','observations/PRECOMMITTED_TEST_ROOT.json','observations/original_WG0J_oracle.json','observations/original_WG0K_oracle.json','observations/phase_b/candidate_read_cut.json','observations/phase_b/reviewer_second_frontier_register.json','observations/phase_b/accepted_owner_test_selector.json','repro/precommitted_contract.py','tests/test_precommitted_phase_b.py','repro/phase_b_support_v1.py','repro/phase_b_adapter_v1.py','repro/phase_b_cold_worker_v1.py','repro/reviewer_common_v1.py','repro/prepare_inherited_v1.py','tests/phase_b/test_original_j_adapter_v1.py','tests/phase_b/test_original_k_adapter_v1.py','tests/phase_b/test_additional_descriptor_binding_red.py']:
 old(name)
for name in ['00_VERDICT_OR_PHASE_A.md','02_ACTUAL_FULL_OWNER_EXECUTION_OR_PRECISE_ENV_HOLD.json','observations/phase_b/extra_descriptor_findings_register.json']:
 old(name,'inherited_records/'+Path(name).name)
cut=json.loads((R/'observations/phase_b/candidate_read_cut.json').read_text())
for row in cut['source_rows']:stage(row['commit'],row['path'],row['staged_path'],row['sha256'])
for row in json.loads((R/'observations/phase_b/accepted_owner_test_selector.json').read_text()):stage(row['commit'],row['source_path'],row['staged_path'],row['sha256'])
(R/'observations/inheritance_source_selector.json').write_text(json.dumps({'schema':'WG0M_PHASE_A_HISTORICAL_SOURCES_ONLY@1','WG0P5_source_read':False,'files':rows},indent=2)+'\n')
print('EXACT_HISTORICAL_FILES_STAGED',len(rows))
