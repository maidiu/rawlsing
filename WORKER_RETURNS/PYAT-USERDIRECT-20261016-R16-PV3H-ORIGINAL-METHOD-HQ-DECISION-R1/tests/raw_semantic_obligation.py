"""Apply the exact preserved raw assertion to this new actual positive output.
It must remain a raw FAIL; it is not xfailed or counted as a method defect.
"""
import pathlib,sys,importlib.util,json,pytest
R=pathlib.Path(__file__).resolve().parents[1];C=R/'runtime/court';RT=C/'runtime_root'
sys.path[:0]=list(map(str,[C/'repro',RT,RT/'candidate/repro',C/'frozen_pv2i/repro']))
source=C/'frozen_pv2i/tests/test_independent.py'
spec=importlib.util.spec_from_file_location('original_pv2i_case_source',source);original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
@pytest.fixture
def court():return None,json.loads((R/'evidence/handoff/first.json').read_text())['report']
test_generic_native_labels_not_specialized_Q86=original.test_generic_native_labels_not_specialized_Q86
