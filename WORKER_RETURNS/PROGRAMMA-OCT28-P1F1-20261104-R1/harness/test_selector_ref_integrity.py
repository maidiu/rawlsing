"""Owner regression: RED at exact P1; a selector ref must not poison provenance."""
from rawlsing_next.tests.test_pre553_route_b_production import _fixture, _execute
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next._pre553_query_predicate import _select_respondent_events


def test_selector_ref_dictionary_fault_cannot_change_supported_fact(monkeypatch):
    monkeypatch.delenv("RAWLSING_C11_ACCELERATOR_DIR", raising=False)
    fx = _fixture()
    route = _execute(fx)
    executor = route.repository_binding.executor
    request = fx["requests"][0]
    before = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
    used = {canonical_json(ref) for fact in before.facts for ref in fact.source_empirical_provenance_refs}
    index = next(iter(executor.repository._i03_release_indices.values()))
    selector = next(event for key in index.respondents for target in fx["qrefs"].values()
                    for event in _select_respondent_events(index, key, target, native_only=True)
                    if canonical_json(event.ref.as_dict()) in used)
    ref = selector.ref
    original_hash = ref.content_hash
    try:
        try:
            ref.__dict__["content_hash"] = "f" * 64
        except (AttributeError, TypeError):
            pass  # Immutable reference storage may reject this fault outright.
        after = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
    finally:
        if hasattr(ref, "__dict__"):
            ref.__dict__["content_hash"] = original_hash
    restored = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
    assert [f.as_dict() for f in restored.facts] == [f.as_dict() for f in before.facts]
    # P1 returns a different SUPPORTED fact here, with forged event provenance.
    assert [f.as_dict() for f in after.facts] == [f.as_dict() for f in before.facts]
