"""Explicit P6 candidate-root transport for the unchanged author69 source."""
import sys
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[1]
P=R/'court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate'
# The inherited reviewer helper temporarily prepends its old P4 root. Restore
# the actual repaired candidate before the original author imports common_v1.
sys.path[:0]=[str(P/'repro'),str(P/'pinned')]
import common_v1
assert common_v1.R==P and Path(common_v1.w.__file__).resolve()==P/'repro/wg0p4_workload.py'
sys.exit(pytest.main(['-c',str(P/'pytest.ini'),str(P/'tests/test_wg0p4.py'),'-vv','--tb=short',
                     '--junitxml='+str(R/'observations/author69.xml')]))
