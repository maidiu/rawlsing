"""All11 unchanged full-module WG0K expectations ported to actual WG0P4.

Only foreign grant case changes protocol: typed parse rejection instead of
silently normalizing forged permission into a fixture grant. Other function
bodies run unchanged against the new full native module via explicit alias.
"""
import importlib.util,sys,pytest
import wg0p4_workload as w
sys.modules['wg0p3_workload']=w
sp=importlib.util.spec_from_file_location('_frozen_wg0k',w.R/'pinned/predecessors/k/repro/test_wg0k_full_module_hostiles.py')
original=importlib.util.module_from_spec(sp);sp.loader.exec_module(original)
for name,function in vars(original).copy().items():
    if name.startswith('test_'):globals()[name]=function

def test_red_checkpoint_is_not_caller_issued_grant():
    with pytest.raises(w.ColdRestartError,match='CALLER_CANNOT_UPGRADE_FIXTURE_PERMISSION'):
        original.test_red_checkpoint_is_not_caller_issued_grant()
