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
from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _cell_map, _query, _query_authority,
)


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
    first = old_routing[0]
    alternate_fields = dict(first.as_dict()["semantic_fields"])
    alternate_fields["member_set_replay_ref"] = {
        **alternate_fields["member_set_replay_ref"], "content_hash": "d" * 64
    }
    new_first = RoutingEligibilityFact(
        typed_state=first.typed_state,
        authority_snapshot_refs=first.authority_snapshot_refs,
        dependency_refs=first.dependency_refs,
        producer_replay_locator_or_reference_root=first.producer_replay_locator_or_reference_root,
        **alternate_fields,
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


def test_c1_changed_row_owner_propagates_to_actual_i03_fact_and_restores():
    """R1 is the first reader: swapping two people changes its Y distribution."""
    fx = _fixture("agent-b-first-reader")
    source = _stream(fx)
    base = fx["projection"]
    rows = base.row_bindings
    altered = replace(
        base, row_bindings=(
            replace(rows[0], respondent_ref=rows[1].respondent_ref),
            replace(rows[1], respondent_ref=rows[0].respondent_ref),
            *rows[2:],
        )
    )
    cache = SourceBackedC11SessionCache()
    old_repo, old_release = build_source_backed_c11_repository(source, base, cache=cache)
    independent = build_validated_source_backed_c11_release_from_stream(source, altered)
    new_repo, new_release = build_source_backed_c11_repository(source, altered, cache=cache)
    assert new_release.release_ref == independent.release_ref

    query_auth = _query_authority("agent-b-i03-first-reader")
    predicate = _branch_predicate(
        fx, query_auth, members=(fx["respondents"]["R1"],), tag="agent-b-single-r1",
    )
    query = _query(fx, query_auth, predicate, ("Y",), tag="agent-b-y-r1")
    registry = AuthorityRegistry((*fx["authorities"], query_auth))

    def execute(repo, release):
        return execute_empirical_query(
            repository=repo, query=query, predicate=predicate,
            authority_registry=registry, release_refs=(release.release_ref,),
        ).facts[0]

    original_fact = execute(old_repo, old_release)
    independent_fact = execute(C11Repository((independent,)), independent)
    cache_fact = execute(new_repo, new_release)
    assert original_fact.ref != independent_fact.ref
    assert cache_fact.ref == independent_fact.ref
    assert _cell_map(original_fact) != _cell_map(independent_fact)
    assert original_fact.raw_denominator_support == independent_fact.raw_denominator_support == 1
    assert _cell_map(original_fact)["1"]["raw_numerator_support"] == 1
    assert _cell_map(independent_fact)["0"]["raw_numerator_support"] == 1

    cache.clear()
    restored_repo, restored_release = build_source_backed_c11_repository(
        source, base, cache=cache,
    )
    assert execute(restored_repo, restored_release).ref == original_fact.ref


def test_c1_one_shot_authority_iterable_produces_same_private_cache_binding(tmp_path, monkeypatch):
    """Current-authority iterator is consumed once, not lost before disk binding."""
    fx = _fixture("agent-b-one-shot")
    source = _stream(fx)
    filenames = []
    for label, current in (
        ("tuple", fx["authorities"]),
        ("generator", (authority for authority in fx["authorities"])),
    ):
        root = tmp_path / label
        root.mkdir(mode=0o700)
        monkeypatch.setenv("RAWLSING_C11_ACCELERATOR_DIR", str(root))
        _, result = build_source_backed_c11_repository(
            source, fx["projection"], current_authorities=current,
        )
        assert result.release_ref is not None
        created = sorted(path.name for path in root.glob("c11-events-*.parquet"))
        assert created, "expected governed private sourcefree accelerator cache"
        filenames.append(created)
    assert filenames[0] == filenames[1]


def test_c1_projection_mutation_during_source_read_must_not_poison_cache_key():
    """The key must still describe the actual I02-validated result after build.

    Dataclass frozen=True does not freeze user-owned nested Mapping payloads.
    A source read can legitimately interleave with an owner updating such a
    payload; returning a new release under the old preimage is a TOCTOU error.
    This is a sourcefree scheduling witness, not an authority grant.
    """
    import pytest
    from rawlsing_next.pre553_source_backed_c11_facade import SourceBackedC11FacadeError

    fx = _fixture("agent-a-projection-race")
    base = fx["projection"]
    slot = base.response_slots[0]
    mutable_semantic_value = {"response": "before"}
    changed_rule = replace(slot.values[0], canonical_value=mutable_semantic_value)
    changed_projection = replace(
        base,
        response_slots=(replace(slot, values=(changed_rule, *slot.values[1:])),
                        *base.response_slots[1:]),
    )
    original_key = changed_projection.cache_identity
    expected_before = build_validated_source_backed_c11_release_from_stream(
        _stream(fx), changed_projection
    )

    def mutate_then_read():
        mutable_semantic_value["response"] = "after"
        # Ordinary caller-owned mapping mutation no longer changes the frozen
        # projection; a hostile explicit bypass of dataclass immutability must
        # still be rejected by the final key coherence check.
        object.__setattr__(
            changed_projection.response_slots[0].values[0],
            "canonical_value", {"response": "after"},
        )
        return iter(fx["cells"])

    source = ExactPhysicalCellStream(
        source_sha256=fx["source_sha"], row_count=3,
        cell_iter_factory=mutate_then_read,
    )
    cache = SourceBackedC11SessionCache()
    with pytest.raises(SourceBackedC11FacadeError, match="cache input changed during C11 build"):
        build_source_backed_c11_repository(source, changed_projection, cache=cache)
    assert changed_projection.cache_identity != original_key
    assert cache.entry_count == 0

    # The altered governed input is still legitimate after its explicit change,
    # and it has a different real C11 release from the earlier one.
    _, expected_after = build_source_backed_c11_repository(
        _stream(fx), changed_projection, cache=cache
    )
    assert expected_after.release_ref != expected_before.release_ref
    assert cache.entry_count == 1


def test_c1_cache_hit_callback_cannot_change_governed_input_while_serving():
    """A warm cache entry must not outlive its full semantic preimage."""
    import pytest
    from rawlsing_next.pre553_source_backed_c11_facade import SourceBackedC11FacadeError

    fx = _fixture("agent-a-warm-hit-race")
    base = fx["projection"]
    slot = base.response_slots[0]
    mutable_semantic_value = {"response": "before"}
    projection = replace(
        base,
        response_slots=(replace(
            slot, values=(replace(slot.values[0], canonical_value=mutable_semantic_value),
                          *slot.values[1:]),
        ), *base.response_slots[1:]),
    )

    class CallbackCache(SourceBackedC11SessionCache):
        mutate_on_read = False

        def get(self, key):
            if self.mutate_on_read:
                mutable_semantic_value["response"] = "after"
                object.__setattr__(
                    projection.response_slots[0].values[0],
                    "canonical_value", {"response": "after"},
                )
            return super().get(key)

    cache = CallbackCache()
    source = _stream(fx)
    _, before = build_source_backed_c11_repository(source, projection, cache=cache)
    assert cache.entry_count == 1
    cache.mutate_on_read = True
    with pytest.raises(SourceBackedC11FacadeError, match="cache input changed during C11 build"):
        build_source_backed_c11_repository(source, projection, cache=cache)
    assert cache.entry_count == 1

    # No silent replacement of the previously legitimate entry.
    cache.mutate_on_read = False
    mutable_semantic_value["response"] = "before"
    object.__setattr__(
        projection.response_slots[0].values[0],
        "canonical_value", {"response": "before"},
    )
    _, restored = build_source_backed_c11_repository(source, projection, cache=cache)
    assert restored.release_ref == before.release_ref


def test_c1_uncached_physical_read_cannot_use_changed_governed_semantics():
    """An absent session cache must not bypass coherent governed projection custody.

    A before/after semantic mutation is not made safe by omitting the optional
    accelerator. Both cached and uncached entrypoints must refuse the same
    changed governing input before returning an apparently valid C11 release.
    """
    import pytest
    from rawlsing_next.pre553_source_backed_c11_facade import SourceBackedC11FacadeError

    fx = _fixture("agent-a-uncached-projection-race")
    p = fx["projection"]
    slot = p.response_slots[0]
    governed_value = {"response": "issued"}
    p = replace(
        p,
        response_slots=(replace(slot, values=(
            replace(slot.values[0], canonical_value=governed_value),
            *slot.values[1:],
        )), *p.response_slots[1:]),
    )
    issued_preimage = p.cache_identity

    def mutate():
        governed_value["response"] = "different"
        object.__setattr__(
            p.response_slots[0].values[0],
            "canonical_value", {"response": "different"},
        )
        return iter(fx["cells"])

    source = ExactPhysicalCellStream(
        source_sha256=fx["source_sha"], row_count=3,
        cell_iter_factory=mutate,
    )
    with pytest.raises(
        SourceBackedC11FacadeError,
        match="cache input changed during C11 build",
    ):
        build_source_backed_c11_repository(source, p, cache=None)
    assert p.cache_identity != issued_preimage

    # A stable, explicitly revised projection can still legitimately build.
    _, current = build_source_backed_c11_repository(_stream(fx), p, cache=None)
    assert current.release_ref is not None


def test_c1_transient_semantic_rewrite_and_restore_cannot_cache_mixed_release():
    """Same hash before/after is insufficient if actual emitted events were mixed."""
    from rawlsing_next.pre553_source_backed_c11_facade import SourceBackedC11FacadeError

    fx = _fixture("agent-a-transient-semantics")
    p = fx["projection"]
    y = p.response_slots[1]
    governed_value = {"answer": "EARLY"}
    p = replace(
        p, response_slots=(
            p.response_slots[0],
            replace(y, values=(replace(y.values[0], canonical_value=governed_value),
                               *y.values[1:])),
            *p.response_slots[2:],
        )
    )
    before_key = p.cache_identity
    baseline = build_validated_source_backed_c11_release_from_stream(_stream(fx), p)

    def temporary_rewrite():
        for cell in fx["cells"]:
            if (cell.variable_name, cell.row_ordinal) == ("Y", 3):
                governed_value["answer"] = "LATE"
            yield cell
        governed_value["answer"] = "EARLY"

    source = ExactPhysicalCellStream(
        source_sha256=fx["source_sha"], row_count=3,
        cell_iter_factory=temporary_rewrite,
    )
    cache = SourceBackedC11SessionCache()
    try:
        _, emitted = build_source_backed_c11_repository(source, p, cache=cache)
    except SourceBackedC11FacadeError:
        pass  # Explicit refusal is valid.
    else:
        # Alternatively, an immutable governed input snapshot may emit the
        # exact original C11 release, regardless of attempted caller mutation.
        assert emitted.release_ref == baseline.release_ref
    assert p.cache_identity == before_key  # The attack defeats entry/exit hashing.


def test_c1_governed_nested_semantic_input_is_detached_and_readonly():
    """Changing an owner's original dict cannot silently rewrite an issued C11 rule."""
    import pytest
    fx = _fixture("agent-a-immutable-governed-contract")
    p = fx["projection"]
    x = p.response_slots[0]
    canonical = {"values": [{"answer": "ISSUED"}]}
    ranks = {"kind": "SCALAR_SINGULAR", "positions": [0]}
    altered_occurrence = replace(x.values[0].occurrences[0],
                                 multiplicity_order_rank_fields=ranks)
    rule = replace(x.values[0], canonical_value=canonical,
                   occurrences=(altered_occurrence,))
    p = replace(p, response_slots=(
        replace(x, values=(rule, *x.values[1:])),
        *p.response_slots[1:],
    ))
    original_key = p.cache_identity
    canonical["values"][0]["answer"] = "MUTATED"
    ranks["positions"].append(55)
    assert p.cache_identity == original_key
    assert p.response_slots[0].values[0].canonical_value["values"][0]["answer"] == "ISSUED"
    assert tuple(p.response_slots[0].values[0].occurrences[0].
                 multiplicity_order_rank_fields["positions"]) == (0,)
    with pytest.raises(TypeError):
        p.response_slots[0].values[0].canonical_value["values"][0]["answer"] = "INTRUSION"
    with pytest.raises(TypeError):
        p.response_slots[0].values[0].occurrences[0].multiplicity_order_rank_fields["kind"] = "WRONG"


def test_c1_session_cache_rejects_conflicting_valid_release_rebind():
    """One full preimage may not silently be rebound to a different I02 release.

    A seal/source-SHA check is necessary but not sufficient: both releases
    are independently I02-valid, under the same source SHA, while their
    respondent ownership and actual I03 output differ.
    """
    import pytest
    from rawlsing_next.pre553_source_backed_c11_facade import (
        SourceBackedC11FacadeError, source_backed_facade_key,
    )

    fx = _fixture("s1a-b-cache-rebind")
    source = _stream(fx)
    p = fx["projection"]
    rows = p.row_bindings
    different = replace(p, row_bindings=(
        replace(rows[0], respondent_ref=rows[1].respondent_ref),
        replace(rows[1], respondent_ref=rows[0].respondent_ref),
        *rows[2:],
    ))
    cache = SourceBackedC11SessionCache()
    _, initial = build_source_backed_c11_repository(source, p, cache=cache)
    other = build_validated_source_backed_c11_release_from_stream(source, different)
    assert initial.source_artifact_ref.content_hash == other.source_artifact_ref.content_hash
    assert initial.release_ref != other.release_ref
    key = source_backed_facade_key(source, p)

    # Identical producer receipt may be inserted again without changing custody.
    cache.put(key, initial)
    with pytest.raises(SourceBackedC11FacadeError, match="conflicting cache rebind"):
        cache.put(key, other)
    assert cache.get(key).release_ref == initial.release_ref
    assert cache.entry_count == 1


def test_c1_empty_cache_rejects_unowned_valid_release_and_preserves_i03():
    """First cache admission requires the *actual* governed C11 producer.

    Both potential releases have independent I02 seals and the same source
    SHA, but a different row/respondent association changes R1's Y fact.
    A public cache.put for an empty slot must not grant either release the
    authority of the unrelated governed projection key.
    """
    import pytest
    from rawlsing_next.pre553_source_backed_c11_facade import (
        SourceBackedC11FacadeError, source_backed_facade_key,
    )

    fx = _fixture("s1a-a-first-cache-admission")
    source = _stream(fx)
    base = fx["projection"]
    rows = base.row_bindings
    altered = replace(base, row_bindings=(
        replace(rows[0], respondent_ref=rows[1].respondent_ref),
        replace(rows[1], respondent_ref=rows[0].respondent_ref),
        *rows[2:],
    ))
    actual = build_validated_source_backed_c11_release_from_stream(source, base)
    foreign = build_validated_source_backed_c11_release_from_stream(source, altered)
    assert actual.release_ref != foreign.release_ref
    assert actual.source_artifact_ref == foreign.source_artifact_ref
    key = source_backed_facade_key(source, base)
    cache = SourceBackedC11SessionCache()

    with pytest.raises(SourceBackedC11FacadeError, match="producer-only cache admission"):
        cache.put(key, foreign)
    assert cache.entry_count == 0

    # Even a genuinely valid release with the correct governed context is
    # not first-admitted through the public put: that caller did not prove
    # it came through the source-backed producer for this session.
    with pytest.raises(SourceBackedC11FacadeError, match="producer-only cache admission"):
        cache.put(key, actual)
    assert cache.entry_count == 0

    repo, admitted = build_source_backed_c11_repository(source, base, cache=cache)
    assert admitted.release_ref == actual.release_ref
    assert cache.entry_count == 1

    query_auth = _query_authority("s1a-a-first-cache-admission")
    predicate = _branch_predicate(
        fx, query_auth, members=(fx["respondents"]["R1"],),
        tag="s1a-a-first-cache-r1",
    )
    query = _query(fx, query_auth, predicate, ("Y",), tag="s1a-a-first-cache-y")
    registry = AuthorityRegistry((*fx["authorities"], query_auth))

    def fact(repository, release):
        return execute_empirical_query(
            repository=repository, query=query, predicate=predicate,
            authority_registry=registry, release_refs=(release.release_ref,),
        ).facts[0]

    expected = fact(C11Repository((actual,)), actual)
    poisoned = fact(C11Repository((foreign,)), foreign)
    observed = fact(repo, admitted)
    assert observed.ref == expected.ref
    assert observed.ref != poisoned.ref
    assert observed.raw_denominator_support == poisoned.raw_denominator_support == 1
    assert _cell_map(observed)["1"]["raw_numerator_support"] == 1
    assert _cell_map(poisoned)["0"]["raw_numerator_support"] == 1
    cache.clear()
    _, restored = build_source_backed_c11_repository(source, base, cache=cache)
    assert restored.release_ref == actual.release_ref
