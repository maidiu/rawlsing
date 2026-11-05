"""Run the original immutability court with exactly the proposed identity amendment."""
import inspect
from dataclasses import replace
from unittest.mock import patch
from rawlsing_next._pre553_c11_execution_view import _compact_public_objects
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.tests import test_pre553_empirical_query as tests

original = C11Repository._commit_validated
def commit(self, release):
    public = _compact_public_objects(release, physical_binding=lambda: None,
                                     projection_binding="independent-identity-amendment")
    return original(self, replace(release, public_objects=public) if public else release)

test = tests.test_sealed_release_semantic_bodies_are_deeply_immutable_and_exports_detached
source = inspect.getsource(test)
old = "    assert resolved_event is event"
new = "    assert isinstance(resolved_event, RespondentEvent)\n    assert resolved_event.ref == event.ref\n    assert resolved_event.as_dict() == event.as_dict()"
assert source.count(old) == 1
namespace = dict(test.__globals__)
exec(compile(source.replace(old, new), "<proposed-test-only-identity-amendment>", "exec"), namespace)
with patch.object(C11Repository, "_commit_validated", commit):
    namespace[test.__name__]()
print("PASS: original complete immutability court with only `is` replaced by native type + exact ref + exact body equality")
print("Production code and tracked tests unchanged")
