"""Control: the same native ref property returns a detached value on baseline."""
from rawlsing_next.tests.test_pre553_route_b_production import _fixture, _execute

fx = _fixture()
route = _execute(fx)
executor = route.repository_binding.executor
request = fx["requests"][0]
before = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
native = next(obj for obj in route.c11_release.public_objects if obj.schema_id == "RespondentEvent")
original = native.ref
detached = native.ref
detached.__dict__["content_hash"] = "f" * 64
assert native.ref == original
after = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
assert [f.as_dict() for f in after.facts] == [f.as_dict() for f in before.facts]
print("PASS baseline: changing the returned native event ref dictionary leaves native identity and exact fact unchanged")
