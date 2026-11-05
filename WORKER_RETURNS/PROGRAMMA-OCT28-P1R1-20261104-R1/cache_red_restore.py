"""Sever hash comparison in memory only; require independent corruption court RED."""
import inspect
import pytest
from rawlsing_next import _pre553_c11_execution_view as view

target = __file__.replace("cache_red_restore.py", "test_independent_review.py") + "::test_cache_faults_slots_and_binding_invalidation"
args = [target, "-q", "-o", "addopts=", "-p", "no:cacheprovider"]
assert pytest.main(args) == 0
original = view._read_bodies
source = inspect.getsource(original)
condition = "\n                            or sha256(scalar.as_buffer()).hexdigest() != selectors[offset].ref.content_hash"
assert source.count(condition) == 1
namespace = dict(original.__globals__)
exec(compile(source.replace(condition, "", 1), "<independent-in-memory-sever>", "exec"), namespace)
try:
    view._read_bodies = namespace["_read_bodies"]
    outcome = pytest.main(args)
    print("HASH_CHECK_SEVERED_EXPECTED_RED_EXIT", int(outcome), flush=True)
    assert outcome == 1
finally:
    view._read_bodies = original
assert pytest.main(args) == 0
print("HASH_CHECK_RESTORED_PASS", flush=True)
