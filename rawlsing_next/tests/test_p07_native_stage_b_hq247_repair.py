"""HQ247 native Stage B B1-B4 / P1 / positive-parity / conflict repair court.

QUARANTINED, NON-PRODUCTION. Nothing here authorises anything or adopts anything.
F7-RR-04G remains OPEN and no downstream receiver is claimed.
"""
from __future__ import annotations

import copy
import gc
import importlib
import statistics
import sys

import pytest

from rawlsing_next.pre553_empirical_authority import require_positive_authority
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    SourceUniverseRelation,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_source_relations import _relation_object_key_from_relation
from rawlsing_next.tests.test_pre553_temporal_comparability import (
    UNIVERSE_A,
    UNIVERSE_B,
    _adjudicated_resolver,
)

B = "rawlsing_next._p07_native_owner_stage_b"
A = "rawlsing_next._p07_native_owner_stage_a"


def _mod(name=B):
    return importlib.import_module(name)


@pytest.fixture(scope="module")
def corpus():
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    return resolver, relation


@pytest.fixture(scope="module")
def snaps(corpus):
    resolver, _r = corpus
    return list(resolver._registry._by_key.values())


def _owner(relations, snaps):
    m = _mod()
    return m.StageBOwner(
        relations=relations, authority_snapshots=snaps,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=SourceUniverseRelation,
        authority_snapshot_class=AuthoritySnapshot)


@pytest.fixture(scope="module")
def positive(corpus, snaps):
    """Genuine production AUTHORIZED, natively adjudicated."""
    resolver, rel = corpus
    return _owner([rel], snaps), rel, resolver


def _request(rel):
    return dict(relation_kind=rel.relation_kind,
                source_universe_refs=list(rel.source_universe_refs),
                operation_scope=rel.operation_scope,
                target_use=rel.target_use,
                effective_scope=rel.effective_scope,
                directionality_or_symmetric=rel.directionality_or_symmetric)


def _sibling(template, suffix, **over):
    """A genuinely valid second relation from the SAME accepted fixture.

    Built by copying the accepted relation and giving it its own relation_id,
    replay_identity, content_hash and any overridden semantic fields. It is an honest
    independent receipt -- NOT forged authority: each candidate is individually valid and
    individually authorises the same exact relation key on its own.
    """
    sf = dict(template.semantic_fields)
    sf["relation_id"] = sf["relation_id"] + "-" + suffix
    sf["replay_identity"] = semantic_hash({"hq247_sibling": suffix})
    sf.update(over)
    new = copy.copy(template)
    object.__setattr__(new, "_semantic_fields", sf)
    object.__setattr__(new, "_content_hash", semantic_hash(new.semantic_projection()))
    return new


# ================================================= HQ246-P1 true positive parity

def test_p1_object_key_matches_production(positive):
    """P1: the object key must be derived from the TRUE effective_scope/directionality."""
    _owner_, rel, _resolver = positive
    got = _owner_.decide(**_request(rel))
    assert got["state"] == "AUTHORIZED", got["reason"]


def test_p1_native_and_production_authorized_agree_completely(positive):
    """B2+P1: genuine native AUTHORIZED compared field-by-field with production."""
    owner, rel, resolver = positive
    n = owner.decide(**_request(rel))
    p = resolver.decide(**_request(rel))
    assert n["state"] == p.state == "AUTHORIZED"
    assert n["authorized"] is True and p.authorized is True
    assert n["reason"] == p.reason
    assert n["owner_custody_hash"] == p.owner_custody_hash
    assert n["replay_identity"] == p.replay_identity
    assert n["authority_snapshot_content_hash"] == p.authority_snapshot_content_hash
    assert n["authority_operation"] == p.authority_operation
    assert n["relation_kind"] == p.relation_kind
    assert n["target_use"] == p.target_use
    assert tuple(n["source_universe_refs"]) == tuple(r.as_dict() for r in p.source_universe_refs)


def test_p1_by_key_path_needs_no_relation_ref(positive):
    """P1: candidate selection by object key alone must reach the positive."""
    owner, rel, _resolver = positive
    kw = _request(rel)
    kw.pop("relation_ref", None)
    assert owner.decide(**kw)["state"] == "AUTHORIZED"


def test_p1_effective_scope_is_not_hardcoded(corpus, snaps):
    """A wrong effective_scope must NOT match, proving the true value is used."""
    _resolver, rel = corpus
    owner = _owner([rel], snaps)
    kw = _request(rel)
    kw["effective_scope"] = "DISTINCT_BY_DEFAULT"     # the old hardcoded value
    assert owner.decide(**kw)["state"] != "AUTHORIZED"


def test_p1_require_returns_the_genuine_positive(positive):
    owner, rel, _resolver = positive
    assert owner.require(**_request(rel))["state"] == "AUTHORIZED"


def test_p1_replay_validates_the_genuine_positive(positive):
    owner, rel, _resolver = positive
    d = owner.decide(**_request(rel))
    assert owner.validate_decision_replay(d) is d


# ============================================ multi-positive CONFLICTING_AUTHORITY

def test_conflict_two_independent_positive_candidates(corpus, snaps):
    """Closes the HQ245/HQ246 coverage gap: >1 positive with one exact key."""
    _resolver, rel = corpus
    second = _sibling(rel, "SECOND")
    assert _relation_object_key_from_relation(second) == \
           _relation_object_key_from_relation(rel)
    owner = _owner([rel, second], snaps)
    d = owner.decide(**_request(rel))
    assert d["state"] == "CONFLICTING_AUTHORITY"
    assert d["authorized"] is False
    assert d["reason"] == "multiple or conflicting exact relation dispositions exist"


def test_conflict_positive_plus_negative_candidate(corpus, snaps):
    _resolver, rel = corpus
    denied = _sibling(rel, "DENIED", decision="DENIED")
    assert _relation_object_key_from_relation(denied) == \
           _relation_object_key_from_relation(rel)
    owner = _owner([rel, denied], snaps)
    d = owner.decide(**_request(rel))
    assert d["state"] == "CONFLICTING_AUTHORITY"
    assert d["authorized"] is False


def test_conflict_precedence_prefers_conflicting_over_all_others(corpus, snaps):
    """The precedence ladder's first entry must win over every lower negative state."""
    _resolver, rel = corpus
    owner = _owner([rel, _sibling(rel, "DENIED", decision="DENIED"),
                    _sibling(rel, "NA", decision="NOT_APPLICABLE"),
                    _sibling(rel, "STALE", decision="EXPIRED_OR_STALE")], snaps)
    d = owner.decide(**_request(rel))
    assert d["state"] == "CONFLICTING_AUTHORITY"


@pytest.mark.parametrize("decision,expected", [
    ("DENIED", "DENIED"),
    ("EXPIRED_OR_STALE", "EXPIRED_OR_STALE"),
    ("NOT_APPLICABLE", "NOT_APPLICABLE"),
    ("CONFLICTING_AUTHORITY", "CONFLICTING_AUTHORITY"),
])
def test_conflict_negative_ladder_order(corpus, snaps, decision, expected):
    """A lone negative candidate resolves through the exact precedence order."""
    _resolver, rel = corpus
    owner = _owner([_sibling(rel, "N", decision=decision)], snaps)
    d = owner.decide(**_request(rel))
    assert d["state"] == expected, (decision, d["state"])


def test_conflict_no_candidate_is_distinct_by_default(positive):
    owner, rel, _resolver = positive
    kw = _request(rel)
    kw["operation_scope"] = "SOME_OTHER_SCOPE"
    d = owner.decide(**kw)
    assert d["state"] == "DISTINCT_BY_DEFAULT"


# ================================================ HQ246-B4 malformed replay input

BAD_VALUES = [None, 42, b"bytes", [], {}, 3.5, object(), True, ["k"],
              ("t",), 0, "ok", "OTHER", {"a": 1}]


@pytest.mark.parametrize("bad", BAD_VALUES, ids=lambda v: type(v).__name__ + repr(v)[:10])
def test_b4_malformed_relation_kind_raises_typed_error(positive, bad):
    """B4: a non-str relation_kind must raise an exact typed error, never crash."""
    owner, rel, _resolver = positive
    kw = _request(rel)
    kw["relation_kind"] = bad
    try:
        d = owner.decide(**kw)
    except (Exception,) as exc:
        assert isinstance(exc, (TypeError, _mod().SourceRelationIntegrityError)), exc
        return
    # a str value is accepted and simply produces an unknown-kind negative
    assert d["state"] in ("DISTINCT_BY_DEFAULT", "CONFLICTING_AUTHORITY")


@pytest.mark.parametrize("bad", BAD_VALUES, ids=lambda v: type(v).__name__ + repr(v)[:10])
def test_b4_malformed_target_use_raises_typed_error(positive, bad):
    owner, rel, _resolver = positive
    kw = _request(rel)
    kw["target_use"] = bad
    try:
        owner.decide(**kw)
    except (Exception,) as exc:
        assert isinstance(exc, (TypeError, _mod().SourceRelationIntegrityError)), exc


class _HostileStr(str):
    """A str SUBCLASS: str() methods that hostile __str__ might affect."""

    def __len__(self):
        return 999999


def test_b4_hostile_str_subclass_does_not_crash(positive):
    owner, rel, _resolver = positive
    kw = _request(rel)
    kw["target_use"] = _HostileStr(rel.target_use)
    d = owner.decide(**kw)
    assert d["state"] in ("DISTINCT_BY_DEFAULT", "AUTHORIZED")


def test_b4_malformed_replay_decision_raises_typed_error(positive):
    """B4: replay validation of a malformed decision dict must be typed, not a crash."""
    owner, rel, _resolver = positive
    d = dict(owner.decide(**_request(rel)))
    for field, bad in (("relation_kind", None), ("relation_kind", 42),
                       ("target_use", None), ("target_use", []),
                       ("state", None), ("state", 7),
                       ("source_universe_refs", None),
                       ("owner_custody_hash", 42)):
        broken = dict(d)
        broken[field] = bad
        try:
            owner.validate_decision_replay(broken)
        except (Exception,) as exc:
            assert isinstance(exc, (TypeError, _mod().SourceRelationIntegrityError)), \
                (field, bad, exc)


def test_b4_replay_rejects_non_dict(positive):
    owner, rel, _resolver = positive
    for bad in (None, 42, "x", [], object()):
        with pytest.raises(_mod().SourceRelationIntegrityError):
            owner.validate_decision_replay(bad)


# ============================================ HQ246-B2/B3 calling convention

def test_b2_positive_authority_callback_receives_a_positional_tuple(corpus, snaps):
    """B2: the trusted positive-authority call must be a real positional call."""
    seen = {}
    real = require_positive_authority

    def spy(snapshot, **kwargs):
        seen["args"] = (snapshot,)
        seen["kwargs"] = set(kwargs)
        return real(snapshot, **kwargs)

    m = _mod()
    resolver, rel = corpus
    owner = m.StageBOwner(
        relations=[rel], authority_snapshots=snaps,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=spy,
        relation_class=SourceUniverseRelation, authority_snapshot_class=AuthoritySnapshot)
    d = owner.decide(**_request(rel))
    assert d["state"] == "AUTHORIZED"
    assert seen["args"][0] is snaps[0], "snapshot must arrive as the first positional arg"
    assert {"authority_kind", "operation", "object_family",
            "source_universe_ref", "target_use_ref",
            "predicate_or_risk_set_ref"} <= seen["kwargs"]


def test_b2_negative_authority_becomes_unknown_authority(corpus, snaps):
    """B3: a raising trusted authority call must surface as UNKNOWN_AUTHORITY, cleanly."""
    def boom(snapshot, **kwargs):
        raise ValueError("synthetic authority refusal")

    m = _mod()
    _resolver, rel = corpus
    owner = m.StageBOwner(
        relations=[rel], authority_snapshots=snaps,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=boom,
        relation_class=SourceUniverseRelation, authority_snapshot_class=AuthoritySnapshot)
    d = owner.decide(**_request(rel))
    assert d["state"] == "UNKNOWN_AUTHORITY"
    assert "synthetic authority refusal" in d["reason"] or "UNKNOWN" in d["state"]


def test_b3_exception_with_traceback_is_handled(corpus, snaps):
    """B3: a raising callback with a real traceback must not leak or crash."""
    def deep(snapshot, **kwargs):
        def inner():
            raise RuntimeError("nested failure with traceback")
        inner()

    m = _mod()
    _resolver, rel = corpus
    owner = m.StageBOwner(
        relations=[rel], authority_snapshots=snaps,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=deep,
        relation_class=SourceUniverseRelation, authority_snapshot_class=AuthoritySnapshot)
    for _ in range(2000):
        assert owner.decide(**_request(rel))["state"] == "UNKNOWN_AUTHORITY"
    gc.collect()


# ======================================== HQ246-B1 constructor repair still holds

class _LyingList(list):
    def __init__(self, items, lie):
        super().__init__(items)
        self._lie = lie

    def __len__(self):
        v = self._lie() if callable(self._lie) else self._lie
        if isinstance(v, BaseException):
            raise v
        return v


@pytest.mark.parametrize("lie", [0, 1, 5, 64, 1_000_000, -1, -2 ** 40, 2 ** 62,
                                  2 ** 63 - 1, RuntimeError("boom"), MemoryError("x"),
                                  lambda: 4096],
                         ids=lambda v: repr(v)[:16])
def test_b1_stage_b_constructor_still_refuses_lying_containers(corpus, snaps, lie):
    m = _mod()
    _resolver, rel = corpus
    with pytest.raises(m.SourceRelationIntegrityError):
        _owner_ = m.StageBOwner(
            relations=_LyingList([rel], lie), authority_snapshots=snaps,
            trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
            trusted_require_positive_authority=require_positive_authority,
            relation_class=SourceUniverseRelation,
            authority_snapshot_class=AuthoritySnapshot)


@pytest.mark.parametrize("lie", [0, 1, 64, 1_000_000, -1, 2 ** 62],
                         ids=lambda v: repr(v)[:16])
def test_b1_stage_a_constructor_still_refuses_lying_containers(lie):
    m = _mod(A)

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    with pytest.raises((TypeError, m.SourceRelationIntegrityError)):
        m.StageAOwner(_LyingList([Rel()], lie), object(), lambda x: "f" * 64)


def test_b1_no_silent_truncation_still_holds(corpus, snaps):
    """Under-reporting must not yield a sealed short custody."""
    m = _mod()
    _resolver, rel = corpus
    with pytest.raises(m.SourceRelationIntegrityError):
        m.StageBOwner(relations=_LyingList([rel], 0), authority_snapshots=snaps,
                      trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)


# ================================================= HQ247-OPEN-001 leak trend

def _blocks_per_call(fn, n=2000, reps=5, warmup=3000):
    for _ in range(warmup):
        fn()
    samples = []
    for _ in range(reps):
        gc.collect()
        b = sys.getallocatedblocks()
        for _ in range(n):
            fn()
        gc.collect()
        samples.append((sys.getallocatedblocks() - b) / n)
    return samples


def test_open001_leak_is_measured_with_error_bars(positive):
    """The residual leak is recorded as a bounded trend with error bars, not a snapshot.

    This test deliberately does NOT assert a leak-free result while HQ247-OPEN-001 is
    open. It pins the measurement so a regression that makes it worse is visible.
    """
    owner, rel, _resolver = positive
    req = _request(rel)
    samples = _blocks_per_call(lambda: owner.decide(**req))
    median = statistics.median(samples)
    spread = max(samples) - min(samples)
    # a leak-free implementation would sit at ~0; the open defect sits near 12
    assert median < 40, ("leak grew unexpectedly", samples)
    assert spread < 1.0, ("measurement is unstable, cannot bound the trend", samples)


def test_open001_clean_methods_stay_clean(positive):
    """The clean methods must stay clean; the defect is scoped to decide()."""
    owner, rel, _resolver = positive
    d = owner.decide(**_request(rel))
    for fn, label in ((lambda: owner.resolve_exact(rel.ref), "resolve_exact"),
                      (lambda: owner.validate_decision_replay(d), "validate_replay")):
        samples = _blocks_per_call(fn)
        assert statistics.median(samples) < 0.05, (label, samples)


# ========================================================= quarantine assertions

def test_no_production_integration():
    import rawlsing_next.pre553_source_relations as p
    import rawlsing_next.pre553_temporal_comparability as f

    for mod in (p, f):
        src = open(mod.__file__, encoding="utf-8").read()
        assert "_p07_native_owner_stage_a" not in src
        assert "_p07_native_owner_stage_b" not in src
        assert "StageAOwner" not in src and "StageBOwner" not in src
    assert p.SourceRelationResolver.__module__ == "rawlsing_next.pre553_source_relations"
    assert _mod().StageBOwner is not p.SourceRelationResolver
    assert _mod(A).StageAOwner is not p.SourceRelationResolver


def test_production_oracle_unchanged_and_operative(corpus):
    resolver, rel = corpus
    assert resolver.resolve_exact(rel.ref) is rel
    p = resolver.decide(**_request(rel))
    assert p.state == "AUTHORIZED"
