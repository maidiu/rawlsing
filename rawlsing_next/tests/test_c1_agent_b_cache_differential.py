"""C-1 Agent B: independent sourcefree cache-identity differentials.

The projection ref and source SHA are deliberately held fixed while qualified
semantic inputs change. Cached reuse must be observationally identical to a
freshly built C11 release, not merely self-consistent with a cached one.
No original35 source, science, or host permission is claimed by this fixture.
"""
from dataclasses import replace

from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    SourceBackedC11SessionCache,
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture


def _stream(fx, *, digest=None):
    return ExactPhysicalCellStream(
        source_sha256=fx["source_sha"],
        row_count=3,
        cell_iter_factory=lambda: iter(fx["cells"]),
        decoder_metadata_digest=digest,
    )


def test_c1_changed_semantic_value_must_not_reuse_same_key_cached_release():
    fx = _fixture("agent-b-value")
    source = _stream(fx)
    base = fx["projection"]
    x = base.response_slots[0]
    changed_value = replace(x.values[0], canonical_value="C1-DIFFERENT-SEMANTIC-VALUE")
    changed_slot = replace(x, values=(changed_value, *x.values[1:]))
    alternative = replace(
        base,
        response_slots=(changed_slot, *base.response_slots[1:]),
    )
    assert base.projection_identity_ref == alternative.projection_identity_ref
    assert base.required_authority_refs == alternative.required_authority_refs
    assert base.expected_source_sha256 == alternative.expected_source_sha256
    assert base.cache_identity != alternative.cache_identity

    cache = SourceBackedC11SessionCache()
    _, original = build_source_backed_c11_repository(source, base, cache=cache)
    independent = build_validated_source_backed_c11_release_from_stream(source, alternative)
    assert original.release_ref != independent.release_ref

    _, cached_alternative = build_source_backed_c11_repository(
        source, alternative, cache=cache
    )
    assert cached_alternative.release_ref == independent.release_ref
    assert cached_alternative.public_objects == independent.public_objects
    assert cache.entry_count == 2

    cache.clear()
    _, restored = build_source_backed_c11_repository(source, alternative, cache=cache)
    assert restored.release_ref == independent.release_ref


def test_c1_changed_row_to_respondent_binding_cannot_reuse_old_c11():
    fx = _fixture("agent-b-row")
    source = _stream(fx)
    original_projection = fx["projection"]
    rows = original_projection.row_bindings
    altered = replace(
        original_projection,
        row_bindings=(
            replace(rows[0], respondent_ref=rows[1].respondent_ref),
            replace(rows[1], respondent_ref=rows[0].respondent_ref),
            *rows[2:],
        ),
    )
    assert altered.cache_identity != original_projection.cache_identity

    cache = SourceBackedC11SessionCache()
    _, old = build_source_backed_c11_repository(
        source, original_projection, cache=cache
    )
    independent = build_validated_source_backed_c11_release_from_stream(source, altered)
    assert old.release_ref != independent.release_ref

    _, from_cache = build_source_backed_c11_repository(source, altered, cache=cache)
    assert from_cache.release_ref == independent.release_ref
    assert cache.entry_count == 2


def test_c1_decoder_metadata_context_changes_cache_admission_not_c11_semantics():
    fx = _fixture("agent-b-decoder")
    cache = SourceBackedC11SessionCache()
    source_a = _stream(fx, digest="a" * 64)
    source_b = _stream(fx, digest="b" * 64)
    _, first = build_source_backed_c11_repository(
        source_a, fx["projection"], cache=cache
    )
    _, second = build_source_backed_c11_repository(
        source_b, fx["projection"], cache=cache
    )
    # The source observations are identical, so the logical C11 release is identical.
    assert first.release_ref == second.release_ref
    # The qualified physical decoder evidence is not identical.
    assert cache.entry_count == 2


def test_c1_changed_routing_and_occurrence_are_distinct_cache_inputs():
    fx = _fixture("agent-b-routing")
    source = _stream(fx)
    base = fx["projection"]
    old_routing = base.routing
    # A different independently specified routing member-set ref must not
    # reuse a release with the previous administration receipt.
    new_first = replace(
        old_routing[0],
        member_set_replay_ref=replace(
            old_routing[0].member_set_replay_ref, content_hash="d" * 64
        ),
    )
    new_routing = replace(base, routing=(new_first, *old_routing[1:]))
    assert new_routing.cache_identity != base.cache_identity

    original_slot = base.response_slots[2]
    old_response = original_slot.values[0]
    altered_occurrence = replace(
        old_response.occurrences[0],
        multiplicity_order_rank_fields={"kind": "MULTISELECT", "index": 8},
    )
    altered_response = replace(
        old_response,
        occurrences=(altered_occurrence, *old_response.occurrences[1:]),
    )
    altered_slot = replace(
        original_slot, values=(altered_response, *original_slot.values[1:])
    )
    altered = replace(
        base, response_slots=(*base.response_slots[:2], altered_slot, *base.response_slots[3:])
    )
    assert altered.cache_identity != base.cache_identity
    cache = SourceBackedC11SessionCache()
    _, before = build_source_backed_c11_repository(source, base, cache=cache)
    independently = build_validated_source_backed_c11_release_from_stream(source, altered)
    assert independently.release_ref != before.release_ref
    _, after = build_source_backed_c11_repository(source, altered, cache=cache)
    assert after.release_ref == independently.release_ref
    assert cache.entry_count == 2


def test_c1_authority_set_cache_isolation_does_not_mint_authority():
    fx = _fixture("agent-b-current-authority")
    source = _stream(fx)
    cache = SourceBackedC11SessionCache()
    _, base = build_source_backed_c11_repository(
        source, fx["projection"], cache=cache, current_authorities=()
    )
    _, full = build_source_backed_c11_repository(
        source, fx["projection"], cache=cache, current_authorities=fx["authorities"]
    )
    assert base.release_ref == full.release_ref
    assert cache.entry_count == 2
