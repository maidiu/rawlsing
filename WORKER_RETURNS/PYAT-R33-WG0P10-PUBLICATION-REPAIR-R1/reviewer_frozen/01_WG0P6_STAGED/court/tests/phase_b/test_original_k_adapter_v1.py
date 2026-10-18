"""WG0L runs all11 original WG0K full-module hostiles; one early refusal map."""
import importlib.util,sys,pytest
from phase_b_support_v1 import w,C
sys.modules['wg0p3_workload']=w
sp=importlib.util.spec_from_file_location('_wg0l_original_k_tests',C/'pinned/predecessors/k/repro/test_wg0k_full_module_hostiles.py')
original=importlib.util.module_from_spec(sp);sp.loader.exec_module(original)
for name,fn in vars(original).copy().items():
 if name.startswith('test_'):globals()[name]=fn

def test_red_checkpoint_is_not_caller_issued_grant():
 with pytest.raises(w.ColdRestartError,match='CALLER_CANNOT_UPGRADE_FIXTURE_PERMISSION'):
  original.test_red_checkpoint_is_not_caller_issued_grant()
