"""Run exact author26 tests with only their filesystem context mapped.
Distinct from the independently frozen33. No author conftest is executed.
"""
import os,sys,pathlib,json,hashlib
import phase_b_support_v1 as support
R=pathlib.Path(__file__).resolve().parents[1]
assert support.w.VERSION=='WG0P5_COMPLETE_NATIVE_DESCRIPTOR_PROVENANCE@1'
support.R=R/'runtime_phase_b/p5_return/review'
source=support.R/'tests/phase_b/test_descriptor_p5_v1.py'
record={'test_source':str(source),'test_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'candidate_file':support.w.__file__,'context_transport':'Only helper R maps to exact staged author review path for its HOSTILE_EXPECTATIONS and old original-three test paths; author conftest disabled. Original assertions unchanged.','claim':'AUTHOR26_REGRESSION_REPRODUCED_NOT_WG0M_INDEPENDENT_ACCEPTANCE'}
(R/'observations/P5_author26_transport.json').write_text(json.dumps(record,indent=2)+'\n')
import pytest
args=['-c',str(support.C/'pytest.ini'),'--confcutdir='+str(source.parent),str(source),'-vv','--tb=short','--junitxml='+str(R/'observations/phase_b_P5_author26.xml')]
sys.exit(pytest.main(args))
