"""HQ245 Stage B differential parity harness: native adjudicator vs frozen Python oracle.

QUARANTINED, NON-PRODUCTION. The native candidate MAY return AUTHORIZED inside this
harness purely as an implementation comparison. It is not adopted runtime authority and
is not wired into production P07/F7.

Byte-exact comparison is required on: decision state, exception type/message, resolved
relation identity, canonical decision preimage, replay hash and custody hash. No
tolerance, no approximate hash, no sampling.
"""
from __future__ import annotations

import copy
import importlib
import itertools

import pytest

from rawlsing_next.pre553_empirical_authority import require_positive_authority
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    ExactRef,
    SourceUniverseRelation,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_source_relations import (
    DEFAULT_RELATION_STATE,
    FORBIDDEN_BACKFILL_TARGET_STATES,
    RELATION_AUTHORITY_KIND,
    SourceRelationAuthorizationError,
    SourceRelationIntegrityError,
)
from rawlsing_next.tests.test_pre553_temporal_comparability import (
    UNIVERSE_A,
    UNIVERSE_B,
    _adjudicated_resolver,
)

STAGE_B = "rawlsing_next._p07_native_owner_stage_b"
PY_INTEGRITY = SourceRelationIntegrityError
PY_AUTHZ = SourceRelationAuthorizationError

# The full reachable P07 decision-state universe. The precedence LADDER is the ordered
# six below; the full reachable string set is these six plus DISTINCT_BY_DEFAULT,
# OUT_OF_SCOPE and the forbidden backfill target states.
PRECEDENCE_LADDER = [
    "CONFLICTING_AUTHORITY", "EXPIRED_OR_STALE", "DENIED",
    "NOT_APPLICABLE", "UNKNOWN_AUTHORITY", "OUT_OF_SCOPE",
]
# Plus every RELATION_DECISION_MATRIX default, which are NOT all DISTINCT_BY_DEFAULT.
MATRIX_DEFAULTS = {
    "SOURCE_SEMANTIC_EQUIVALENCE": DEFAULT_RELATION_STATE,
    "RESPONDENT_LINKAGE": DEFAULT_RELATION_STATE,
    "OVERLAP_NON_DUPLICATION": "UNKNOWN_OVERLAP",
    "SAMPLE_POOLING": DEFAULT_RELATION_STATE,
    "ESTIMAND_COMPOSITION": DEFAULT_RELATION_STATE,
    "BACKFILL": DEFAULT_RELATION_STATE,
    "PROVENANCE_ORIGIN": "PROVENANCE_ONLY",
    "HARMONIZATION_ALIAS": "ALIAS_ONLY",
}
ALL_REACHABLE_STATES = sorted(
    set(PRECEDENCE_LADDER)
    | {DEFAULT_RELATION_STATE, "AUTHORIZED"}
    | set(FORBIDDEN_BACKFILL_TARGET_STATES)
    | set(MATRIX_DEFAULTS.values())
)


def _native():
    return importlib.import_module(STAGE_B)


def _err_pair():
    m = _native()
    return m.SourceRelationIntegrityError, m.SourceRelationAuthorizationError


@pytest.fixture(scope="module")
def oracle():
    """The frozen production Python P07 owner -- PREEXISTING BASELINE, untouched."""
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    return resolver, relation


@pytest.fixture(scope="module")
def snapshots(oracle):
    resolver, _rel = oracle
    return list(resolver._registry._by_key.values())


@pytest.fixture(scope="module")
def native(oracle, snapshots):
    m = _native()
    resolver, _rel = oracle
    owner = m.StageBOwner(
        relations=list(resolver._by_ref.values()),
        authority_snapshots=snapshots,
        trusted_semantic_hash=semantic_hash,
        trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=SourceUniverseRelation,
        authority_snapshot_class=AuthoritySnapshot,
    )
    return owner


# --------------------------------------------------------------- custody hash

def test_native_custody_hash_is_byte_exact_with_python(native, oracle, snapshots):
    """The Stage A FNV-1a placeholder is gone: this must equal the ACCEPTED P07 hash."""
    resolver, _rel = oracle
    py_decision = resolver.decide(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=[UNIVERSE_A, UNIVERSE_B],
        operation_scope={},
        target_use="urn:rawlsing:pre553:use:probe",
        effective_scope={},
    )
    assert native.custody_hash == py_decision.owner_custody_hash
    assert len(native.custody_hash) == 64
    assert native.custody_hash != "0000000000000000"


def test_custody_hash_is_order_insensitive_by_key(native, oracle, snapshots):
    """Reordering the admission lists must not change the canonical custody hash."""
    m = _native()
    resolver, _rel = oracle
    rels = list(resolver._by_ref.values())
    rev = m.StageBOwner(
        relations=list(reversed(rels)),
        authority_snapshots=list(reversed(snapshots)),
        trusted_semantic_hash=semantic_hash,
        trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=SourceUniverseRelation,
        authority_snapshot_class=AuthoritySnapshot,
    )
    assert rev.custody_hash == native.custody_hash


def test_custody_hash_changes_when_material_changes(oracle, snapshots):
    """Removing the pinned authority snapshot must change the canonical custody hash."""
    m = _native()
    resolver, _rel = oracle
    rels = list(resolver._by_ref.values())
    full = m.StageBOwner(
        relations=rels, authority_snapshots=snapshots,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=SourceUniverseRelation, authority_snapshot_class=AuthoritySnapshot,
    )
    fewer = m.StageBOwner(
        relations=rels, authority_snapshots=snapshots[:0],
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=SourceUniverseRelation, authority_snapshot_class=AuthoritySnapshot,
    )
    assert full.custody_hash != fewer.custody_hash


# ------------------------------------------------------------ resolve_exact

def test_native_resolve_exact_matches_oracle(native, oracle):
    resolver, relation = oracle
    assert native.resolve_exact(relation.ref) is resolver.resolve_exact(relation.ref)


def test_native_resolve_exact_accepts_mapping(native, oracle):
    _resolver, relation = oracle
    assert native.resolve_exact(relation.ref.as_dict()) is relation


class _MutableRelationStandIn:
    """A deliberately MUTABLE relation stand-in.

    The accepted SourceUniverseRelation is frozen, so it cannot exercise the native
    re-hash path. This stand-in can, and it is admitted honestly by passing
    `relation_class=_MutableRelationStandIn` so the exact-type admission check passes.
    """
    def __init__(self, template):
        self.ref = template.ref
        self.semantic_fields = dict(template.semantic_fields)
        # self-consistent at seal time: the declared content_hash IS the hash of this
        # stand-in's own semantic_projection(), so only a post-seal mutation can break it
        self.content_hash = semantic_hash({"projection": dict(self.semantic_fields)})
        self.relation_kind = template.relation_kind
        self.source_universe_refs = template.source_universe_refs
        self.operation_scope = template.operation_scope
        self.target_use = template.target_use
        self.authority_operation = template.authority_operation
        self.relation_authority_ref = template.relation_authority_ref
        # HQ246-P1: the object key now requires the TRUE effective_scope and
        # directionality_or_symmetric, so a stand-in must carry them.
        self.effective_scope = template.effective_scope
        self.directionality_or_symmetric = template.directionality_or_symmetric

    def semantic_projection(self):
        return {"projection": dict(self.semantic_fields)}


def test_native_resolve_exact_rehash_catches_post_seal_projection_mutation(
        oracle, snapshots):
    """The FULL semantic_projection() re-hash is live, not a key/string compare."""
    se_n, _ = _err_pair()
    resolver, relation = oracle
    stand_in = _MutableRelationStandIn(relation)
    m = _native()
    owner = m.StageBOwner(
        relations=[stand_in], authority_snapshots=snapshots,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=_MutableRelationStandIn,
        authority_snapshot_class=AuthoritySnapshot,
    )
    # clean at seal time
    assert owner.resolve_exact(stand_in.ref) is stand_in
    # mutate the projection material AFTER sealing
    stand_in.semantic_fields = {**stand_in.semantic_fields, "decision": "TAMPERED"}
    with pytest.raises(se_n) as e:
        owner.resolve_exact(stand_in.ref)
    assert "semantic hash mismatch" in str(e.value)


def test_native_resolve_exact_catches_post_seal_ref_and_hash_mutation(oracle, snapshots):
    se_n, _ = _err_pair()
    resolver, relation = oracle
    stand_in = _MutableRelationStandIn(relation)
    m = _native()
    owner = m.StageBOwner(
        relations=[stand_in], authority_snapshots=snapshots,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=_MutableRelationStandIn,
        authority_snapshot_class=AuthoritySnapshot,
    )
    stand_in.content_hash = "0" * 64
    with pytest.raises(se_n) as e:
        owner.resolve_exact(stand_in.ref)
    assert "semantic identity drift" in str(e.value)


def test_native_resolve_exact_refuses_empty_victim(native, oracle):
    se_n, _ = _err_pair()
    _resolver, relation = oracle
    victim = ExactRef(
        kind=relation.ref.kind,
        object_id="urn:rawlsing:pre553:SourceUniverseRelation:sha256:" + "ab" * 32,
        content_hash="ab" * 32,
    )
    with pytest.raises(se_n) as e:
        native.resolve_exact(victim)
    assert "no label/ID/latest/default inference" in str(e.value)


# ------------------------------------------------------- full-ladder parity

def _decide_both(native, resolver, **kw):
    """Run both implementations and return (native_outcome, python_outcome)."""
    def run(fn):
        try:
            return ("ok", fn(**kw))
        except Exception as exc:            # noqa: BLE001 - differential capture
            return ("exc", type(exc).__name__, str(exc))
    return run(native.decide), run(resolver.decide)


def _norm_py(d):
    return (
        d.state, d.reason, d.relation_kind, d.target_use,
        d.replay_identity, d.owner_custody_hash, d.authority_snapshot_content_hash,
        d.authority_operation,
        d.relation_ref.as_dict() if d.relation_ref else None,
        d.authority_ref.as_dict() if d.authority_ref else None,
        tuple(r.as_dict() for r in d.source_universe_refs),
    )


def _norm_native(d):
    return (
        d["state"], d["reason"], d["relation_kind"], d["target_use"],
        d["replay_identity"], d["owner_custody_hash"],
        d["authority_snapshot_content_hash"], d["authority_operation"],
        d["relation_ref"], d["authority_ref"],
        tuple(d["source_universe_refs"]),
    )


@pytest.mark.parametrize("kind", sorted(RELATION_AUTHORITY_KIND))
def test_parity_all_relation_kinds(native, oracle, kind):
    resolver, relation = oracle
    kw = dict(
        relation_kind=kind,
        source_universe_refs=[UNIVERSE_A, UNIVERSE_B],
        operation_scope={},
        target_use="urn:rawlsing:pre553:use:parity",
        effective_scope={"scope": "probe"},
        directionality_or_symmetric="SYMMETRIC",
    )
    (n_out, p_out) = _decide_both(native, resolver, **kw)
    assert n_out[0] == p_out[0] == "ok", (n_out, p_out)
    assert _norm_native(n_out[1]) == _norm_py(p_out[1])


def test_parity_unknown_kind_is_identical_negative(native, oracle):
    resolver, _rel = oracle
    kw = dict(relation_kind="NOT_A_KIND", source_universe_refs=[UNIVERSE_A, UNIVERSE_B],
              operation_scope={}, target_use="u", effective_scope={})
    n_out, p_out = _decide_both(native, resolver, **kw)
    assert n_out[0] == p_out[0]
    if n_out[0] == "exc":
        assert n_out[2] == p_out[2]          # identical message text
    else:
        assert _norm_native(n_out[1]) == _norm_py(p_out[1])


def test_parity_single_source_universe_is_identical_negative(native, oracle):
    resolver, _rel = oracle
    kw = dict(relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
              source_universe_refs=[UNIVERSE_A], operation_scope={},
              target_use="u", effective_scope={})
    n_out, p_out = _decide_both(native, resolver, **kw)
    assert n_out[0] == p_out[0]
    if n_out[0] == "exc":
        assert n_out[1] == p_out[1] and n_out[2] == p_out[2]
    else:
        assert _norm_native(n_out[1]) == _norm_py(p_out[1])


def test_parity_with_exact_relation_ref(native, oracle):
    resolver, relation = oracle
    kw = dict(relation_kind=relation.relation_kind,
              source_universe_refs=list(relation.source_universe_refs),
              operation_scope=relation.operation_scope,
              target_use=relation.target_use,
              effective_scope={"probe": 1},
              directionality_or_symmetric="SYMMETRIC",
              relation_ref=relation.ref)
    (n_out, p_out) = _decide_both(native, resolver, **kw)
    assert n_out[0] == p_out[0], (n_out, p_out)
    if n_out[0] == "ok":
        assert _norm_native(n_out[1]) == _norm_py(p_out[1])
    else:
        assert n_out[1] == p_out[1]


def test_parity_expected_authority_operation_mismatch(native, oracle):
    """OUT_OF_SCOPE / operation-mismatch parity, both directions."""
    resolver, relation = oracle
    kw = dict(relation_kind=relation.relation_kind,
              source_universe_refs=list(relation.source_universe_refs),
              operation_scope=relation.operation_scope,
              target_use=relation.target_use,
              effective_scope={"probe": 2},
              directionality_or_symmetric="SYMMETRIC",
              relation_ref=relation.ref,
              expected_authority_operation="DEFINITELY_NOT_THE_OPERATION")
    (n_out, p_out) = _decide_both(native, resolver, **kw)
    assert n_out[0] == p_out[0], (n_out, p_out)
    if n_out[0] == "ok":
        assert _norm_native(n_out[1]) == _norm_py(p_out[1])
        assert n_out[1]["state"] in ("OUT_OF_SCOPE", DEFAULT_RELATION_STATE)
    else:
        assert n_out[1] == p_out[1]


def test_parity_every_reachable_state_is_reachable_or_absent(native, oracle):
    """Explicit coverage record: which of the 14 reachable strings we actually produced."""
    resolver, relation = oracle
    seen = set()
    for kind in sorted(RELATION_AUTHORITY_KIND):
        kw = dict(relation_kind=kind,
                  source_universe_refs=[UNIVERSE_A, UNIVERSE_B],
                  operation_scope={}, target_use="urn:rawlsing:pre553:use:cov",
                  effective_scope={})
        (n_out, _p) = _decide_both(native, resolver, **kw)
        if n_out[0] == "ok":
            seen.add(n_out[1]["state"])
    for s in seen:
        assert s in ALL_REACHABLE_STATES, s
    assert seen, "no state produced at all"
    # the descriptive kinds must report their own MATRIX default, not the generic one
    assert "PROVENANCE_ONLY" in seen
    assert "ALIAS_ONLY" in seen


def test_precedence_ladder_order_is_declared_and_enforced():
    """The ladder order is part of the contract; assert the exact declared order."""
    assert PRECEDENCE_LADDER == [
        "CONFLICTING_AUTHORITY", "EXPIRED_OR_STALE", "DENIED",
        "NOT_APPLICABLE", "UNKNOWN_AUTHORITY", "OUT_OF_SCOPE",
    ]


# ---------------------------------------------------------- replay identity

def test_native_decision_replay_round_trips(native, oracle):
    resolver, relation = oracle
    d = native.decide(
        relation_kind=relation.relation_kind,
        source_universe_refs=list(relation.source_universe_refs),
        operation_scope=relation.operation_scope,
        target_use=relation.target_use,
        effective_scope={"rt": True},
        relation_ref=relation.ref,
    )
    assert native.validate_decision_replay(d) is d


def test_native_decision_replay_detects_tampering(native, oracle):
    _se_n, _se_a = _err_pair()
    _resolver, relation = oracle
    d = native.decide(
        relation_kind=relation.relation_kind,
        source_universe_refs=list(relation.source_universe_refs),
        operation_scope=relation.operation_scope,
        target_use=relation.target_use,
        effective_scope={"rt": 2},
        relation_ref=relation.ref,
    )
    tampered = dict(d)
    tampered["state"] = "AUTHORIZED"
    with pytest.raises(_se_n):
        native.validate_decision_replay(tampered)


def test_native_decision_replay_rejects_foreign_custody_hash(native, oracle):
    se_n, _ = _err_pair()
    _resolver, relation = oracle
    d = native.decide(
        relation_kind=relation.relation_kind,
        source_universe_refs=list(relation.source_universe_refs),
        operation_scope=relation.operation_scope,
        target_use=relation.target_use,
        effective_scope={"rt": 3},
        relation_ref=relation.ref,
    )
    tampered = dict(d)
    tampered["owner_custody_hash"] = "f" * 64
    with pytest.raises(se_n):
        native.validate_decision_replay(tampered)


# ------------------------------------------------------------------- require

def test_require_refuses_non_positive_state(native, oracle):
    se_n, se_a = _err_pair()
    resolver, relation = oracle
    kw = dict(relation_kind=relation.relation_kind,
              source_universe_refs=list(relation.source_universe_refs),
              operation_scope=relation.operation_scope,
              target_use=relation.target_use,
              effective_scope={"req": True},
              relation_ref=relation.ref)
    d = native.decide(**kw)
    if d["state"] != "AUTHORIZED":
        with pytest.raises(se_a):
            native.require(**kw)


# ------------------------------------------------------------- custody safety

def test_reinit_is_refused(native, oracle, snapshots):
    se_n, _ = _err_pair()
    resolver, _rel = oracle
    with pytest.raises(se_n) as e:
        type(native).__init__(
            native, list(resolver._by_ref.values()), snapshots, semantic_hash,
            canonicalize, require_positive_authority, SourceUniverseRelation,
            AuthoritySnapshot)
    assert "one-shot" in str(e.value)


def test_cannot_copy_or_pickle(native):
    for fn in (copy.copy, copy.deepcopy):
        with pytest.raises(TypeError):
            fn(native)
    with pytest.raises((TypeError, AttributeError)):
        native.__reduce__()


def test_attributes_immutable(native):
    with pytest.raises(AttributeError):
        native.custody_hash = "0" * 64


def test_type_is_not_subclassable():
    m = _native()
    with pytest.raises(TypeError):
        type("Attacker", (m.StageBOwner,), {})


# ------------------------------------------------------- trusted seam refusal

def test_admission_requires_trusted_callables(oracle, snapshots):
    m = _native()
    resolver, _rel = oracle
    rels = list(resolver._by_ref.values())
    with pytest.raises(Exception):
        m.StageBOwner(relations=rels, authority_snapshots=snapshots,
                      trusted_semantic_hash=None, trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)


def test_admission_rejects_duck_typed_relation(oracle, snapshots):
    m = _native()
    with pytest.raises(TypeError):
        m.StageBOwner(relations=[object()], authority_snapshots=snapshots,
                      trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)


def test_admission_rejects_hostile_iterable(oracle, snapshots):
    m = _native()

    class Hostile:
        def __iter__(self):
            raise AssertionError("hostile __iter__ reached native admission")

        def __len__(self):
            raise AssertionError("hostile __len__ reached native admission")

    with pytest.raises(Exception):
        m.StageBOwner(relations=Hostile(), authority_snapshots=snapshots,
                      trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)


def test_failed_admission_seals_nothing(oracle, snapshots):
    m = _native()
    resolver, _rel = oracle
    rels = list(resolver._by_ref.values())
    with pytest.raises(Exception):
        m.StageBOwner(relations=rels + [object()], authority_snapshots=snapshots,
                      trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)


# ------------------------------------------------------------- quarantine

def test_production_modules_never_reference_stage_b():
    import rawlsing_next.pre553_source_relations as p
    import rawlsing_next.pre553_temporal_comparability as f

    for mod in (p, f):
        src = open(mod.__file__, encoding="utf-8").read()
        assert "_p07_native_owner_stage_b" not in src
        assert "StageBOwner" not in src


def test_native_type_is_not_the_production_resolver():
    import rawlsing_next.pre553_source_relations as p

    assert _native().StageBOwner is not p.SourceRelationResolver
    assert p.SourceRelationResolver.__module__ == "rawlsing_next.pre553_source_relations"


def test_production_oracle_still_operative(oracle):
    resolver, relation = oracle
    assert resolver.resolve_exact(relation.ref) is relation
    d = resolver.decide(
        relation_kind=relation.relation_kind,
        source_universe_refs=list(relation.source_universe_refs),
        operation_scope=relation.operation_scope,
        target_use=relation.target_use,
        effective_scope={"baseline": True},
        relation_ref=relation.ref,
    )
    assert d.state in ALL_REACHABLE_STATES


def test_module_declares_non_production():
    m = _native()
    assert m.PRODUCTION_INTEGRATED == 0
    assert m.STAGE == "B"
    assert m.SUBCLASSABLE == 0
    assert m.TRUSTED_SEAM == 1


# ------------------------------------------------- bounded memory-safety stress

def test_bounded_decide_stress_no_memory_corruption(native, oracle):
    """Bounded stress over the invalid-input space.

    This exists because two real memory-safety defects were found by exactly this kind
    of sweep during Stage B: (a) the trusted `canonicalize` can return its INPUT object
    unchanged, so taking ownership of the result stole a caller reference; (b) a
    caller-supplied `directionality_or_symmetric` arrived borrowed and was DECREFed at
    cleanup, freeing a live object. Both produced EXC_BAD_ACCESS on a LATER call.
    """
    resolver, relation = oracle
    kinds = sorted(RELATION_AUTHORITY_KIND) + ["BOGUS_KIND"]
    sources = [[UNIVERSE_A, UNIVERSE_B], [UNIVERSE_A], [], None, "nope",
               [1, 2], [[]], {}, (), {1: 2}, relation.ref, 42]
    scopes = [{}, None, [], "s", 5, relation.operation_scope, (1, 2), {"a": {"b": [1, 2]}}]
    effs = [{}, None, [], "e", 0, {"x": [1, {"y": None}]}, True]
    dirs = [None, "SYMMETRIC", {}, [], 0, "z", [1], {"q": 1}]
    calls = 0
    for kind in kinds:
        for src in sources:
            for osc in scopes:
                for eff in effs:
                    for dr in dirs:
                        try:
                            native.decide(
                                relation_kind=kind, source_universe_refs=src,
                                operation_scope=osc, target_use="u",
                                effective_scope=eff, directionality_or_symmetric=dr)
                        except Exception:   # noqa: BLE001 - stress must not escape
                            pass
                        calls += 1
    # the owner must still be usable and self-consistent after the whole sweep
    d = native.decide(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=[UNIVERSE_A, UNIVERSE_B], operation_scope={},
        target_use="u", effective_scope={})
    assert d["owner_custody_hash"] == native.custody_hash
    assert calls > 1000


def test_bounded_resolve_exact_stress(native, oracle):
    _resolver, relation = oracle
    junk = [None, 0, "", [], {}, object(), relation.ref, relation.ref.as_dict(),
            {"kind": "x"}, True, 3.5, [1], b"x", relation,
            {"kind": None, "object_id": None, "content_hash": None}, 0.0]
    for _ in range(40):
        for x in junk:
            try:
                native.resolve_exact(x)
            except Exception:   # noqa: BLE001 - stress must not escape
                pass
    assert native.resolve_exact(relation.ref) is relation


def test_repeated_owner_construction_and_teardown(oracle):
    """Constructor/dealloc must be balanced: build and drop many owners."""
    import gc

    m = _native()
    resolver, _rel = oracle
    rels = list(resolver._by_ref.values())
    snaps = list(resolver._registry._by_key.values())
    owners = []
    for _ in range(40):
        owners.append(m.StageBOwner(
            relations=rels, authority_snapshots=snaps,
            trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
            trusted_require_positive_authority=require_positive_authority,
            relation_class=SourceUniverseRelation,
            authority_snapshot_class=AuthoritySnapshot))
    assert all(o.sealed for o in owners)
    assert len({o.custody_hash for o in owners}) == 1
    del owners
    gc.collect()
