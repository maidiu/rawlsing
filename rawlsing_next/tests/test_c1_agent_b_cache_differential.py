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
    assert base.cache_identity == alternative.cache_identity  # legacy weak key

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
    assert altered.cache_identity == original_projection.cache_identity

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
