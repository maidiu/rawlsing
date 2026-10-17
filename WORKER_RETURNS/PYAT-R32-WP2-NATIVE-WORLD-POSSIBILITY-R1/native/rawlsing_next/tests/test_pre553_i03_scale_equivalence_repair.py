from types import SimpleNamespace

import pytest

import rawlsing_next._pre553_query_eval as qeval
from rawlsing_next._pre553_query_predicate import _build_release_index
from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
from rawlsing_next.pre553_empirical_query import (
    EmpiricalQueryResolutionError,
    replay_empirical_query,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
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
    index.routing_by_respondent[respondent.ref.key].append(conflict)

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
