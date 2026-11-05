"""Exact P1 fault: writable reference descendants in an otherwise frozen selector."""
from rawlsing_next.tests.test_pre553_route_b_production import _fixture, _execute
from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json
from rawlsing_next._pre553_query_predicate import _select_respondent_events
import json
import os

os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
fx = _fixture()
route = _execute(fx)
executor = route.repository_binding.executor
repository = executor.repository
request = fx["requests"][0]
before = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
release = repository.resolve_release_exact(route.c11_release.release_ref)
index = next(iter(repository._i03_release_indices.values()))
selectors = sorted((event for key in index.respondents for target in fx["qrefs"].values()
                    for event in _select_respondent_events(index, key, target, native_only=True)),
                   key=lambda event: event.ref.key)
for event in selectors:
    old_ref = event.ref
    old = old_ref.as_dict()
    native_before = repository.resolve_object_exact(ExactRef(**old)).as_dict()
    # This is a public descendant dictionary write, without object.__setattr__,
    # ctypes, slot replacement, attestation forgery, or production-file edits.
    old_ref.__dict__["content_hash"] = "f" * 64
    after = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
    changed = [fact.as_dict() for fact in after.facts] != [fact.as_dict() for fact in before.facts]
    old_ref.__dict__["content_hash"] = old["content_hash"]
    restored = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
    assert [f.as_dict() for f in restored.facts] == [f.as_dict() for f in before.facts]
    assert repository.resolve_object_exact(ExactRef(**old)).as_dict() == native_before
    assert not changed, "selector descendant changed downstream exact facts"
    if changed:
        print(json.dumps({"mutation":"selector.ref.__dict__[content_hash] = f*64",
                          "original_event_ref":old,
                          "original_facts":[f.ref.as_dict() for f in before.facts],
                          "changed_facts":[f.ref.as_dict() for f in after.facts],
                          "changed_states":[f.typed_state for f in after.facts],
                          "changed_provenance_contains_forged_hash":"f"*64 in canonical_json([f.as_dict() for f in after.facts]),
                          "restored_exact":True,"source_native_body_unchanged":True},indent=2))
        break
else:
    print("PASS: all event-ref faults preserve exact supported facts and sealed native lookup")

for event in selectors:
    question = event.native_question_ref
    old = question.as_dict()
    question.__dict__["object_id"] = "urn:test:forged-question"
    after = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
    changed = [fact.as_dict() for fact in after.facts] != [fact.as_dict() for fact in before.facts]
    question.__dict__.update(old)
    restored = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
    assert [f.as_dict() for f in restored.facts] == [f.as_dict() for f in before.facts]
    assert not changed, "selector descendant changed downstream exact facts"
    if changed:
        print(json.dumps({"mutation":"selector.native_question_ref.__dict__[object_id] = forged-question",
                          "original_question_ref":old,
                          "changed_facts":[f.ref.as_dict() for f in after.facts],
                          "changed_states":[f.typed_state for f in after.facts],
                          "restored_exact":True},indent=2))
        break
else:
    print("PASS: all shared question-ref faults preserve exact facts across respondents and restoration")
