"""P6 version of M's filesystem-only author26 transport, frozen tests unchanged."""
import sys
from pathlib import Path
import phase_b_support_v1 as support
import pytest
R=Path(__file__).resolve().parents[1]
assert support.w.VERSION=='WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1'
support.R=R/'court/runtime_phase_b/p5_return/review'
source=support.R/'tests/phase_b/test_descriptor_p5_v1.py'
sys.exit(pytest.main(['-c',str(support.C/'pytest.ini'),'--confcutdir='+str(source.parent),str(source),'-vv','--tb=short',
                     '--junitxml='+str(R/'observations/author26.xml')]))
