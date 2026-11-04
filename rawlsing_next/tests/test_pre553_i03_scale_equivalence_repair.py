from dataclasses import replace
from types import MappingProxyType, SimpleNamespace

import pytest

import rawlsing_next._pre553_query_eval as qeval
import rawlsing_next.pre553_empirical_query as i03
from rawlsing_next._pre553_query_predicate import _build_release_index
from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
from rawlsing_next.pre553_empirical_query import (
    EmpiricalQueryResolutionError,
    replay_empirical_query,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _astra_query_authority,
    _branch_predicate,
    _build_source,
    _query,
    _query_authority,
    _ref,
    _registry,
    _run,
)


def _joint_fixture(tag: str, *, weighted: bool = False):
    rows = [
        {"id": "R1", "responses": {"X": 0, "Y": 1}},
        {"id": "R2", "responses": {"X": 1, "Y": 0}},
        {"id": "R3", "responses": {"X": 1, "Y": 1}},
    ]
    weights = (
        {
            "R1": ("WEIGHT_VALID_AUTHORIZED", "1/2"),
            "R2": ("WEIGHT_VALID_AUTHORIZED", "3/2"),
            "R3": ("WEIGHT_VALID_AUTHORIZED", "2"),
        }
        if weighted else None
    )
    source = _build_source(tag, rows, weights=weights)
    qa = _query_authority(tag)
    predicate = _branch_predicate(source, qa, tag=f"{tag}-all")
    query = _query(
        source,
        qa,
        predicate,
        ("X", "Y"),
        measure="GOVERNED_WEIGHTED" if weighted else "RAW",
        tag=tag,
    )
    return source, qa, predicate, query


def _legacy_double_routing_result(monkeypatch, source, qa, predicate, query):
    """Test-only behavioral baseline for the pre-repair duplicate routing path."""
    original = qeval._routing_fact_for

    monkeypatch.setattr(qeval, "_UsedObjectAccumulator", list)
    monkeypatch.setattr(qeval, "_UsedAuthorityAccumulator", list)

    def double_routing(*args, **kwargs):
        original(*args, **kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(qeval, "_routing_fact_for", double_routing)
    return _run(source, qa, predicate, query)


def test_normal_path_resolves_routing_once_per_respondent_target(monkeypatch):
    source, qa, predicate, query = _joint_fixture("scale-once")
    original = qeval._routing_fact_for
    calls = []

    def counted(*args, **kwargs):
        respondent = args[0]
        calls.append((respondent.ref.key, kwargs["target_ref"].key))
        return original(*args, **kwargs)

    monkeypatch.setattr(qeval, "_routing_fact_for", counted)
    fact = _run(source, qa, predicate, query).facts[0]

    expected = {
        (respondent.ref.key, source["qrefs"][target].key)
        for respondent in source["respondents"].values()
        for target in ("X", "Y")
    }
    assert fact.typed_state == "SUPPORTED"
    assert len(calls) == len(expected)
    assert set(calls) == expected


def test_conflicting_routing_facts_still_fail_closed():
    source, qa, _, _ = _joint_fixture("scale-conflict")
    release = source["repo"].resolve_release_exact(source["release_ref"])
    index = _build_release_index(release, source["universe"].ref)
    respondent = source["respondents"]["R1"]
    matches = [
        fact
        for fact in index.routing_by_respondent[respondent.ref.key]
        if fact.question_or_target_ref == source["qrefs"]["X"].as_dict()
        or fact.question_or_target_ref == source["qrefs"]["X"]
    ]
    assert len(matches) == 1
    base = matches[0]
    conflict = RoutingEligibilityFact(
        typed_state="NOT_ELIGIBLE",
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", "scale-conflict-second-routing"
        ),
        empirical_universe_ref=base.empirical_universe_ref,
        scoped_respondent_ref=base.scoped_respondent_ref,
        question_or_target_ref=base.question_or_target_ref,
        risk_set_ref=base.risk_set_ref,
        routing_rule_ref=base.routing_rule_ref,
        applicability_state="NOT_ELIGIBLE",
        routing_state="NOT_ELIGIBLE",
        parent_predicate_refs=base.parent_predicate_refs,
        member_set_replay_ref=base.member_set_replay_ref,
    )
    routing = dict(index.routing_by_respondent)
    routing[respondent.ref.key] += (conflict,)
    index = replace(index, routing_by_respondent=MappingProxyType(routing))

    with pytest.raises(
        EmpiricalQueryResolutionError,
        match="conflicting exact routing/risk-set facts",
    ):
        qeval._routing_fact_for(
            respondent,
            index,
            target_ref=source["qrefs"]["X"],
            risk_set_ref=source["risk_refs"]["R"],
            registry=_registry(source, qa),
            used=[],
            used_auth=[],
        )


def test_unresolved_routing_still_fails_closed():
    source = _build_source(
        "scale-unresolved",
        [{"id": "R1", "responses": {"Y": 1}}],
        risk_sets={"R": {"Y": set()}},
        nonmember_routing_state="ROUTING_UNKNOWN",
    )
    qa = _query_authority("scale-unresolved")
    predicate = _branch_predicate(source, qa, tag="scale-unresolved-all")
    query = _query(source, qa, predicate, ("Y",), tag="scale-unresolved")

    fact = _run(source, qa, predicate, query).facts[0]
    assert fact.typed_state == "UNAVAILABLE"
    assert fact.p02_failure_state == "RISK_SET_UNAVAILABLE"


def test_target_specific_noncommon_membership_disagreement_still_fails_closed():
    profile = SimpleNamespace(risk_set_type="ROUTED_APPLICABLE_RISK_SET")
    with pytest.raises(
        EmpiricalQueryResolutionError,
        match="target-specific membership disagreement",
    ):
        qeval._risk_membership(
            ("ELIGIBLE_APPLICABLE", "NOT_ELIGIBLE"),
            profile=profile,
        )


def test_exact_key_accumulators_drop_only_duplicate_intermediate_retention():
    source, qa, _, _ = _joint_fixture("scale-dedup")
    release = source["repo"].resolve_release_exact(source["release_ref"])
    index = _build_release_index(release, source["universe"].ref)
    respondent = source["respondents"]["R1"]
    routing = index.routing_by_respondent[respondent.ref.key][0]

    used = qeval._UsedObjectAccumulator()
    used.extend((routing, routing, routing))
    assert [obj.ref.key for obj in used] == [routing.ref.key]

    auth = qeval._UsedAuthorityAccumulator()
    auth.extend((
        source["routing_auth"].authority_ref,
        source["routing_auth"].authority_ref,
        source["routing_auth"].authority_ref,
    ))
    assert [ref.key for ref in auth] == [source["routing_auth"].authority_ref.key]


def test_positive_fact_replay_provenance_and_authority_are_legacy_equivalent(monkeypatch):
    source, qa, predicate, query = _joint_fixture("scale-equivalence")
    normal = _run(source, qa, predicate, query)
    normal_fact = normal.facts[0]
    assert normal_fact.typed_state == "SUPPORTED"

    with monkeypatch.context() as legacy_patch:
        legacy = _legacy_double_routing_result(
            legacy_patch, source, qa, predicate, query
        )
    legacy_fact = legacy.facts[0]

    assert normal.query_ref == legacy.query_ref
    assert normal_fact.ref == legacy_fact.ref
    assert normal_fact.replay_ref == legacy_fact.replay_ref
    assert (
        normal_fact.source_empirical_provenance_refs
        == legacy_fact.source_empirical_provenance_refs
    )
    assert normal_fact.authority_snapshot_refs == legacy_fact.authority_snapshot_refs
    assert normal_fact.semantic_projection() == legacy_fact.semantic_projection()

    replayed = replay_empirical_query(
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=_registry(source, qa),
        release_refs=(source["release_ref"],),
        expected_fact_refs=(legacy_fact.ref,),
    )
    assert replayed.facts[0].ref == normal_fact.ref


def test_weighted_behavior_and_identity_are_legacy_equivalent(monkeypatch):
    source, qa, predicate, query = _joint_fixture(
        "scale-weighted-equivalence", weighted=True
    )
    normal = _run(source, qa, predicate, query)
    normal_fact = normal.facts[0]
    assert normal_fact.typed_state == "SUPPORTED"
    assert normal_fact.measure_kind == "GOVERNED_WEIGHTED"
    assert normal_fact.weighted_denominator_support_if_authorized == {
        "$exact_fraction": [4, 1]
    }

    with monkeypatch.context() as legacy_patch:
        legacy = _legacy_double_routing_result(
            legacy_patch, source, qa, predicate, query
        )
    legacy_fact = legacy.facts[0]

    assert normal_fact.ref == legacy_fact.ref
    assert normal_fact.replay_ref == legacy_fact.replay_ref
    assert normal_fact.authority_snapshot_refs == legacy_fact.authority_snapshot_refs
    assert normal_fact.source_empirical_provenance_refs == legacy_fact.source_empirical_provenance_refs
    assert (
        normal_fact.weighted_denominator_support_if_authorized
        == legacy_fact.weighted_denominator_support_if_authorized
    )
    assert (
        normal_fact.weighted_numerator_support_if_authorized
        == legacy_fact.weighted_numerator_support_if_authorized
    )


def test_repository_index_reuse_keeps_current_authority_risk_and_release_checks(monkeypatch):
    source, _, _, _ = _joint_fixture("index-cache")
    authority = _astra_query_authority("index-cache")
    predicate = _branch_predicate(source, authority, tag="index-cache")
    query = _query(source, authority, predicate, ("Y",), tag="index-cache")
    repo = source["repo"]
    release_ref = source["release_ref"]
    universe_ref = source["universe"].ref
    key = (release_ref, universe_ref)

    build_index = i03._build_release_index
    builds = []

    def counted(release, universe):
        builds.append((release.release_ref, universe))
        return build_index(release, universe)

    monkeypatch.setattr(i03, "_build_release_index", counted)
    before = _run(source, authority, predicate, query)
    assert before.facts[0].typed_state == "SUPPORTED"
    compatible = _query(source, authority, predicate, ("X",), tag="index-cache-x")
    assert _run(source, authority, predicate, compatible).facts[0].typed_state == "SUPPORTED"
    assert _run(source, authority, predicate, query) == before
    assert builds == [key]

    denied = _astra_query_authority("index-cache", state="DENY")
    refusal = _run(source, denied, predicate, query)
    assert refusal.facts[0].p02_failure_state == "MISSING_REQUIRED_AUTHORITY"

    wrong_risk = _query(
        {**source, "risk_refs": {"R": _ref("RISK_SET", "index-cache-foreign-risk")}},
        authority, predicate, ("Y",), tag="index-cache-wrong-risk",
    )
    refusal = _run(source, authority, predicate, wrong_risk)
    assert refusal.facts[0].p02_failure_state == "RISK_SET_UNAVAILABLE"

    foreign, _, _, _ = _joint_fixture("index-cache-foreign")
    refusal = i03.execute_empirical_query(
        repository=foreign["repo"], query=query, predicate=predicate,
        authority_registry=_registry(source, authority),
        release_refs=(foreign["release_ref"],),
    )
    assert refusal.facts[0].p02_failure_state == "SOURCE_SCOPE_UNAVAILABLE"
    assert builds == [key]

    # Substitute an index for a foreign sealed release under the warm key.
    foreign_release = foreign["repo"].resolve_release_exact(foreign["release_ref"])
    monkeypatch.setitem(repo._i03_release_indices, key, build_index(
        foreign_release, foreign["universe"].ref,
    ))
    restored = _run(source, authority, predicate, query)
    assert builds == [key, key]
    assert restored == before
    assert restored.facts[0].as_dict() == before.facts[0].as_dict()
    assert restored.facts[0].replay_ref == before.facts[0].replay_ref


def _same_identity_corruption_case(tag: str):
    """E2's exact sourcefree case: same exact key, changed cached respondent set."""
    source, _, _, _ = _joint_fixture(tag)
    authority = _astra_query_authority(tag)
    predicate = _branch_predicate(source, authority, tag=tag)
    query = _query(source, authority, predicate, ("Y",), tag=tag)
    return source, authority, predicate, query


def test_same_identity_changed_payload_rebuilds_exact_fact(monkeypatch):
    """Regression for E2 probe_same_identity_cache.py (E1 RED at this assertion)."""
    source, authority, predicate, query = _same_identity_corruption_case(
        "e2-same-identity-corruption"
    )
    repository = source["repo"]
    key = (source["release_ref"], source["universe"].ref)
    original = _run(source, authority, predicate, query)
    assert original.facts[0].typed_state == "SUPPORTED"
    warm_index = repository._i03_release_indices[key]

    # Preserve the SAME sealed release/universe objects while replacing the
    # private payload with a read-only but wrong respondent map (omit R1).
    poisoned = replace(
        warm_index,
        respondents=MappingProxyType({
            respondent_key: respondent
            for respondent_key, respondent in warm_index.respondents.items()
            if respondent_key != source["respondents"]["R1"].ref.key
        }),
    )
    assert poisoned.release is warm_index.release
    assert poisoned.universe is warm_index.universe
    assert len(poisoned.respondents) + 1 == len(warm_index.respondents)
    monkeypatch.setitem(repository._i03_release_indices, key, poisoned)

    rebuilt = _run(source, authority, predicate, query)
    assert rebuilt.facts[0].typed_state == "SUPPORTED"
    assert rebuilt == original  # E1 emitted a DIFFERENT SUPPORTED fact.
    assert rebuilt.facts[0].as_dict() == original.facts[0].as_dict()
    assert rebuilt.facts[0].ref == original.facts[0].ref
    assert rebuilt.facts[0].replay_ref == original.facts[0].replay_ref
    assert repository._i03_release_indices[key] is not poisoned
    assert repository._i03_release_indices[key].respondents == warm_index.respondents
    # Restoring without cache retains the same exact native result.
    del repository._i03_release_indices[key]
    assert _run(source, authority, predicate, query) == original


@pytest.mark.parametrize("field", (
    "respondents", "events_by_respondent", "coordinates_by_respondent",
    "routing_by_respondent", "weights_by_respondent",
))
def test_in_place_index_field_replacement_rebuilds_before_fact(field):
    """Even object.__setattr__ on a frozen cached index must not launder a slot."""
    source, authority, predicate, query = _same_identity_corruption_case(
        "e3-in-place-" + field
    )
    repo = source["repo"]
    key = (source["release_ref"], source["universe"].ref)
    baseline = _run(source, authority, predicate, query)
    cached = repo._i03_release_indices[key]
    previous = getattr(cached, field)
    new_map = MappingProxyType({
        k: v for k, v in previous.items()
        if k != source["respondents"]["R1"].ref.key
    })
    assert len(new_map) + 1 == len(previous)
    # Explicit fault injection, NOT an ordinary mutation API.
    object.__setattr__(cached, field, new_map)
    recovered = _run(source, authority, predicate, query)
    assert recovered == baseline
    assert repo._i03_release_indices[key] is not cached
    assert getattr(repo._i03_release_indices[key], field) == previous


def test_missing_attestation_cannot_authorize_a_poisoned_index():
    source, authority, predicate, query = _same_identity_corruption_case(
        "e3-missing-attestation"
    )
    repo = source["repo"]
    key = (source["release_ref"], source["universe"].ref)
    before = _run(source, authority, predicate, query)
    old = repo._i03_release_indices[key]
    repo._i03_index_attestations.pop(key)
    assert _run(source, authority, predicate, query) == before
    assert repo._i03_release_indices[key] is not old
    assert repo._i03_index_attestations[key][0] is repo._i03_release_indices[key]


def test_parallel_same_release_index_creation_is_serialized(monkeypatch):
    """Concurrent callers share one fresh topology; no partly verified entry."""
    from concurrent.futures import ThreadPoolExecutor

    source, _, _, _ = _joint_fixture("e3-concurrent")
    repo = source["repo"]
    release = repo.resolve_release_exact(source["release_ref"])
    universe_ref = source["universe"].ref
    count = 0
    original_builder = i03._build_release_index

    def counted(r, u):
        nonlocal count
        count += 1
        return original_builder(r, u)

    monkeypatch.setattr(i03, "_build_release_index", counted)
    with ThreadPoolExecutor(max_workers=8) as executor:
        indices = list(executor.map(
            lambda _: i03._release_index_for(repo, release, universe_ref),
            range(32),
        ))
    assert count == 1
    assert all(item is indices[0] for item in indices)
    assert repo._i03_index_attestations[(release.release_ref, universe_ref)][0] is indices[0]
