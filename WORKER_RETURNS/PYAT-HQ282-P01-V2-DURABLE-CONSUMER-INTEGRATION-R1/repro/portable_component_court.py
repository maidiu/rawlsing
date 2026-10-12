"""Portable component baseline; does not establish an integrated consumer run."""
from pathlib import Path
import sys, importlib.util, hashlib, json
root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root))
repro = Path(__file__).resolve().parent
import rawlsing_next.tests.test_pre553_batch_durable_checkpoint_candidate as D
import rawlsing_next.tests.test_pre553_governed_batch_checkpoint_integration_candidate as G
D.WORKER = repro / 'b01c_worker.py'
D.B01D_WORKER = repro / 'b01d_worker.py'
G.WORKER = repro / 'b01e_worker.py'
blob = (repro / 'a05_oracle.py').read_bytes()
assert hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest() == '00a4cc84d321c3fbace0f4aa09be62dbb31994fc'
spec = importlib.util.spec_from_file_location('p01_exact_a05', repro / 'a05_oracle.py')
a05 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = a05
spec.loader.exec_module(a05)
u = a05.frozen_universe()
assert a05.verify(u, a05.honest_manifest(u)).ok
m = a05.honest_manifest(u)
m['jobs'].pop()
v = a05.verify(u, m)
assert not v.ok and 'EXPECTED_OPERATION_OMITTED' in [x['code'] for x in v.failures]
m = a05.honest_manifest(u)
m['expected_derived_from'] = 'RESULT_OUTPUT'
assert not a05.verify(u, m).ok
print(json.dumps({'exact_a05_blob': 'verified', 'positive': True, 'omission_refused': True, 'output_derived_refused': True, 'scope': 'oracle component only; no integrated consumer claim'}), flush=True)
import pytest
raise SystemExit(pytest.main(['-q', '--import-mode=importlib', '-k', 'not test_source_free_posture_no_raw_survey_reads', 'rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py', 'rawlsing_next/tests/test_pre553_original_workload_contract_v2_candidate.py', 'rawlsing_next/tests/test_pre553_batch_durable_checkpoint_candidate.py', 'rawlsing_next/tests/test_pre553_governed_batch_checkpoint_integration_candidate.py']))
