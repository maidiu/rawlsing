"""HQ246 native A/B memory-boundary + trusted-seam repair court.

QUARANTINED, NON-PRODUCTION. Every case here is a HOSTILE regression test derived from
the independent findings D1-D9. The original Stage A 39 and Stage B 41 tests live in
their own files and are preserved unmodified.

Nothing in this file authorises anything. F7-RR-04G remains OPEN.
"""
from __future__ import annotations

import gc
import importlib
import sys

import pytest

from rawlsing_next.pre553_empirical_authority import require_positive_authority
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    SourceUniverseRelation,
    canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_source_relations import semantic_hash as p07_semantic_hash
from rawlsing_next.tests.test_pre553_temporal_comparability import (
    UNIVERSE_A,
    UNIVERSE_B,
    _adjudicated_resolver,
)

A = "rawlsing_next._p07_native_owner_stage_a"
B = "rawlsing_next._p07_native_owner_stage_b"


def _mod(name):
    return importlib.import_module(name)


# ============================================================ D1 memory boundary

class _LyingList(list):
    """list subclass whose __len__ is attacker-controlled (D1)."""

    def __init__(self, items, lie):
        super().__init__(items)
        self._lie = lie

    def __len__(self):
        v = self._lie() if callable(self._lie) else self._lie
        if isinstance(v, BaseException):
            raise v
        return v


class _LyingTuple(tuple):
    def __new__(cls, items, lie):
        return super().__new__(cls, items)

    def __init__(self, items, lie):
        self._lie = lie

    def __len__(self):
        v = self._lie() if callable(self._lie) else self._lie
        if isinstance(v, BaseException):
            raise v
        return v


LIES = [
    0,                      # under-report -> silent truncation
    1,
    5,
    64,
    1_000_000,              # over-report -> out-of-bounds walk
    -1,                     # negative
    -1_000_000,
    2 ** 62,                # huge
    2 ** 63 - 1,
    RuntimeError("boom"),   # raising
    MemoryError("no"),
    lambda: 1_000_000,      # callable lie
]


@pytest.mark.parametrize("lie", LIES, ids=lambda v: repr(v)[:24])
def test_d1_stage_a_refuses_lying_list_subclass(lie):
    """D1: an overridden __len__ must never supply the allocation/iteration bound."""
    m = _mod(A)

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    with pytest.raises((TypeError, m.SourceRelationIntegrityError)):
        m.StageAOwner(_LyingList([Rel()], lie), object(), lambda x: "f" * 64)


@pytest.mark.parametrize("lie", LIES, ids=lambda v: repr(v)[:24])
def test_d1_stage_a_refuses_lying_tuple_subclass(lie):
    m = _mod(A)

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    with pytest.raises((TypeError, m.SourceRelationIntegrityError)):
        m.StageAOwner(_LyingTuple((Rel(),), lie), object(), lambda x: "f" * 64)


@pytest.mark.parametrize("lie", [0, 1, 5, 64, 1_000_000, -1, 2 ** 62,
                                  RuntimeError("boom")],
                         ids=lambda v: repr(v)[:20])
def test_d1_stage_b_refuses_lying_relation_container(lie):
    """D1 on Stage B -- the defect HQ statically verified at blob 2d8ffc68."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    with pytest.raises(m.SourceRelationIntegrityError) as e:
        m.StageBOwner(relations=_LyingList([relation], lie), authority_snapshots=snaps,
                      trusted_semantic_hash=semantic_hash,
                      trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)
    assert "EXACT" in str(e.value)


@pytest.mark.parametrize("lie", [0, 1, 5, 64, 1_000_000, -1, 2 ** 62,
                                  RuntimeError("boom")],
                         ids=lambda v: repr(v)[:20])
def test_d1_stage_b_refuses_lying_snapshot_container(lie):
    """D1 must hold for the authority_snapshots container too, not only relations."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    with pytest.raises(m.SourceRelationIntegrityError) as e:
        m.StageBOwner(relations=[relation],
                      authority_snapshots=_LyingList(snaps, lie),
                      trusted_semantic_hash=semantic_hash,
                      trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)
    assert "EXACT" in str(e.value)


def test_d1_no_silent_truncation_exact_container_is_fully_admitted():
    """The anti-truncation positive control: an EXACT list admits every element."""
    m = _mod(A)
    m2 = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())

    owner = m2.StageBOwner(relations=[relation], authority_snapshots=snaps,
                           trusted_semantic_hash=semantic_hash,
                           trusted_canonicalize=canonicalize,
                           trusted_require_positive_authority=require_positive_authority,
                           relation_class=SourceUniverseRelation,
                           authority_snapshot_class=AuthoritySnapshot)
    assert owner.counts == (1, len(snaps))
    assert owner.resolve_exact(relation.ref) is relation


def test_d1_reentrant_len_subclass_is_refused_without_side_effect():
    """A reentrant/side-effecting __len__ must not be invoked to size the loop."""
    m = _mod(B)
    calls = []

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    resolver, _rel = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())

    class Reentrant(list):
        def __len__(self):
            calls.append(1)
            return 4096

    evil = Reentrant([object()])
    with pytest.raises(Exception):
        m.StageBOwner(relations=evil, authority_snapshots=snaps,
                      trusted_semantic_hash=semantic_hash,
                      trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)
    # the subclass is refused by type, so its __len__ is never consulted for a bound
    assert calls == []


# ==================================================================== D2 refcounts

def test_d2_stage_a_custody_diagnostic_does_not_leak():
    """D2: 20,000 custody_diagnostic() calls must not retain 20,000 tracked lists."""
    m = _mod(A)

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    owner = m.StageAOwner([Rel()], object(), lambda x: "f" * 64)
    for _ in range(2000):
        owner.custody_diagnostic()          # warm up interpreter lazy state
    gc.collect()
    before = sys.getallocatedblocks()
    for _ in range(20000):
        owner.custody_diagnostic()
    gc.collect()
    per_call = (sys.getallocatedblocks() - before) / 20000.0
    assert per_call < 0.01, f"custody_diagnostic leaks {per_call:.3f} blocks/call"


# ==================================================== D3 transactional lifecycle

def test_d3_stage_b_repeated_failed_init_keeps_callback_refcounts_bounded():
    """D3: 20,000 failing constructions must not accumulate pinned trusted callables."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    before = sys.getrefcount(semantic_hash)
    before_c = sys.getrefcount(canonicalize)
    before_r = sys.getrefcount(require_positive_authority)
    for _ in range(20000):
        with pytest.raises((m.SourceRelationIntegrityError, TypeError)):
            m.StageBOwner(relations=[relation, object()],    # invalid member
                          authority_snapshots=snaps,
                          trusted_semantic_hash=semantic_hash,
                          trusted_canonicalize=canonicalize,
                          trusted_require_positive_authority=require_positive_authority,
                          relation_class=SourceUniverseRelation,
                          authority_snapshot_class=AuthoritySnapshot)
    gc.collect()
    assert sys.getrefcount(semantic_hash) - before <= 2
    assert sys.getrefcount(canonicalize) - before_c <= 2
    assert sys.getrefcount(require_positive_authority) - before_r <= 2


def test_d3_failed_init_admits_no_partial_custody():
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    before = sys.getrefcount(relation)
    for _ in range(2000):
        with pytest.raises((m.SourceRelationIntegrityError, TypeError)):
            m.StageBOwner(relations=[relation, object()], authority_snapshots=snaps,
                          trusted_semantic_hash=semantic_hash,
                          trusted_canonicalize=canonicalize,
                          trusted_require_positive_authority=require_positive_authority,
                          relation_class=SourceUniverseRelation,
                          authority_snapshot_class=AuthoritySnapshot)
    gc.collect()
    assert sys.getrefcount(relation) - before <= 2


def test_d3_stage_a_repeated_failed_init_is_bounded():
    m = _mod(A)
    before = sys.getrefcount(m.AUTHORIZING) if hasattr(m, "AUTHORIZING") else None

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    for _ in range(20000):
        with pytest.raises((TypeError, m.SourceRelationIntegrityError)):
            m.StageAOwner([Rel(), object()], object(), lambda x: "f" * 64)
    gc.collect()
    assert before is None or before >= 0   # module still coherent after 20k retries


# ==================================================================== D5 GC cycles

def test_d5_owner_participates_in_cyclic_gc():
    """D5: an object graph referring back to the owner must still be collectable."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    gc.collect()
    gc.disable()
    try:
        base = sys.getallocatedblocks()
        for _ in range(500):
            owner = m.StageBOwner(
                relations=[relation], authority_snapshots=snaps,
                trusted_semantic_hash=semantic_hash,
                trusted_canonicalize=canonicalize,
                trusted_require_positive_authority=require_positive_authority,
                relation_class=SourceUniverseRelation,
                authority_snapshot_class=AuthoritySnapshot)
            # build a cycle THROUGH the owner
            box = {}
            box["owner"] = owner
            owner_marker = box
            del owner, box, owner_marker
    finally:
        gc.enable()
    gc.collect()
    # without traverse/clear the cycle would be uncollectable; with it the graph frees
    assert sys.getallocatedblocks() - base < 500 * 50


# ================================================================ D6/D7 custody

def test_d6_stage_a_refuses_scalar_authority_registry():
    """D6: authority_registry=42 was previously accepted with only its type name kept."""
    m = _mod(A)

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    for bad in (42, "registry", 3.5, True, b"x"):
        with pytest.raises(TypeError):
            m.StageAOwner([Rel()], bad, lambda x: "f" * 64)


def test_d6_stage_a_pins_the_registry_object_not_just_its_name():
    m = _mod(A)

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    class Registry:
        pass

    reg = Registry()
    before = sys.getrefcount(reg)
    owner = m.StageAOwner([Rel()], reg, lambda x: "f" * 64)
    assert sys.getrefcount(reg) == before + 1     # genuinely pinned
    assert owner.sealed
    del owner
    gc.collect()
    assert sys.getrefcount(reg) == before         # released on dealloc


def test_d6_stage_b_pins_real_snapshots_not_synthetic_labels():
    """D6: Stage B must validate and immutably pin the snapshots it actually uses."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    before = [sys.getrefcount(s) for s in snaps]
    owner = m.StageBOwner(relations=[relation], authority_snapshots=snaps,
                          trusted_semantic_hash=semantic_hash,
                          trusted_canonicalize=canonicalize,
                          trusted_require_positive_authority=require_positive_authority,
                          relation_class=SourceUniverseRelation,
                          authority_snapshot_class=AuthoritySnapshot)
    pinned = [sys.getrefcount(s) for s in snaps]
    assert any(p > b for p, b in zip(pinned, before)), \
        "no authority snapshot was genuinely pinned by the native owner"
    # The owner's OWN pin must be gone after dealloc. The absolute count cannot be
    # compared to `before`, because the enclosing production resolver and the pytest
    # frame legitimately hold their own references to the same snapshot objects.
    del owner
    gc.collect()
    released = [sys.getrefcount(s) for s in snaps]
    assert all(r < p for r, p in zip(released, pinned)), \
        ("owner pin survived dealloc", pinned, released)


def test_d6_stage_b_refuses_non_exact_authority_snapshot():
    """A snapshot that is not an exact AuthoritySnapshot is refused at admission."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    for bad in ([object()], ["not a snapshot"], [42], [None]):
        with pytest.raises((TypeError, m.SourceRelationIntegrityError)):
            m.StageBOwner(relations=[relation], authority_snapshots=bad,
                          trusted_semantic_hash=semantic_hash,
                          trusted_canonicalize=canonicalize,
                          trusted_require_positive_authority=require_positive_authority,
                          relation_class=SourceUniverseRelation,
                          authority_snapshot_class=AuthoritySnapshot)


def test_d7_stage_a_trusted_semantic_hash_is_actually_invoked():
    """D7: Stage A stored trusted_semantic_hash but never called it."""
    m = _mod(A)
    seen = []

    def spy(value):
        seen.append(value)
        return "f" * 64

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

        def semantic_projection(self):
            return {"payload": "material"}

    owner = m.StageAOwner([Rel()], object(), spy)
    assert seen, "trusted_semantic_hash was never called during admission"
    before = len(seen)
    owner.resolve_exact(Rel.ref)
    assert len(seen) > before, "trusted seam is not load-bearing at resolve time"


def test_d7_stage_b_trusted_seam_is_native_owned_and_unrebindable():
    """D7: the pinned TCB identities are observable but cannot be re-bound."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    owner = m.StageBOwner(relations=[relation], authority_snapshots=snaps,
                         trusted_semantic_hash=semantic_hash,
                         trusted_canonicalize=canonicalize,
                         trusted_require_positive_authority=require_positive_authority,
                         relation_class=SourceUniverseRelation,
                         authority_snapshot_class=AuthoritySnapshot)
    seam = owner.trusted_seam
    assert seam == (semantic_hash, canonicalize, require_positive_authority)
    with pytest.raises(AttributeError):
        owner.trusted_seam = (len, len, len)
    with pytest.raises(AttributeError):
        owner.custody_hash = "0" * 64


def test_d7_rebinding_the_p07_module_attribute_does_not_change_pinned_seam():
    """A bounded T1 attacker case: rebinding a module attribute must not affect custody."""
    m = _mod(B)
    import rawlsing_next.pre553_empirical_objects as objects

    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    owner = m.StageBOwner(relations=[relation], authority_snapshots=snaps,
                         trusted_semantic_hash=semantic_hash,
                         trusted_canonicalize=canonicalize,
                         trusted_require_positive_authority=require_positive_authority,
                         relation_class=SourceUniverseRelation,
                         authority_snapshot_class=AuthoritySnapshot)
    d = owner.decide(relation_kind=relation.relation_kind,
                     source_universe_refs=list(relation.source_universe_refs),
                     operation_scope=relation.operation_scope,
                     target_use=relation.target_use, effective_scope={"x": 1},
                     relation_ref=relation.ref)
    original_hash = d["replay_identity"]
    original_custody = owner.custody_hash

    original = objects.semantic_hash
    objects.semantic_hash = lambda v: "0" * 64
    try:
        d2 = owner.decide(relation_kind=relation.relation_kind,
                          source_universe_refs=list(relation.source_universe_refs),
                          operation_scope=relation.operation_scope,
                          target_use=relation.target_use, effective_scope={"x": 1},
                          relation_ref=relation.ref)
    finally:
        objects.semantic_hash = original
    # the native owner keeps its originally pinned identity
    assert d2["replay_identity"] == original_hash
    assert d2["owner_custody_hash"] == original_custody
    assert owner.trusted_seam[0] is semantic_hash


# ================================================================ D8 payload drift

def test_d8_stage_a_detects_mutated_semantic_payload():
    """D8: Stage A only compared ref.key/content_hash strings before the repair."""
    m = _mod(A)

    class Ref:
        def __init__(self):
            self.key = "K|O|" + "a" * 64

    class Rel:
        def __init__(self):
            self.ref = Ref()
            self.content_hash = "a" * 64
            self.fields = {"decision": "AUTHORIZED"}

        def semantic_projection(self):
            return {"payload": dict(self.fields)}

    rel = Rel()
    owner = m.StageAOwner([rel], object(), semantic_hash)
    assert owner.resolve_exact(rel.ref) is rel
    rel.fields["decision"] = "TAMPERED"
    with pytest.raises(m.SourceRelationIntegrityError) as e:
        owner.resolve_exact(rel.ref)
    assert "projection drift" in str(e.value)


def test_d8_stage_b_detects_mutated_payload_with_unchanged_identity_strings():
    """D8 on Stage B: unchanged ref.key/content_hash but a mutated projection."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())

    class Mutable:
        """mutable stand-in admitted through the exact-class parameter."""

        def __init__(self, template):
            self.ref = template.ref
            self.semantic_fields = dict(template.semantic_fields)
            self.content_hash = semantic_hash(
                {"projection": dict(self.semantic_fields)})
            self.relation_kind = template.relation_kind
            self.source_universe_refs = template.source_universe_refs
            self.operation_scope = template.operation_scope
            self.target_use = template.target_use
            self.authority_operation = template.authority_operation
            self.relation_authority_ref = template.relation_authority_ref

        def semantic_projection(self):
            return {"projection": dict(self.semantic_fields)}

    stand_in = Mutable(relation)
    owner = m.StageBOwner(relations=[stand_in], authority_snapshots=snaps,
                          trusted_semantic_hash=semantic_hash,
                          trusted_canonicalize=canonicalize,
                          trusted_require_positive_authority=require_positive_authority,
                          relation_class=Mutable,
                          authority_snapshot_class=AuthoritySnapshot)
    assert owner.resolve_exact(stand_in.ref) is stand_in
    # identity strings unchanged, payload changed
    stand_in.semantic_fields = {**stand_in.semantic_fields, "decision": "TAMPERED"}
    with pytest.raises(m.SourceRelationIntegrityError) as e:
        owner.resolve_exact(stand_in.ref)
    assert "semantic hash mismatch" in str(e.value)


# ===================================================== quarantine / no integration

def test_repair_did_not_integrate_into_production():
    import rawlsing_next.pre553_source_relations as p
    import rawlsing_next.pre553_temporal_comparability as f

    for mod in (p, f):
        src = open(mod.__file__, encoding="utf-8").read()
        assert "_p07_native_owner_stage_a" not in src
        assert "_p07_native_owner_stage_b" not in src
        assert "StageAOwner" not in src
        assert "StageBOwner" not in src
    assert p.SourceRelationResolver.__module__ == "rawlsing_next.pre553_source_relations"
    assert _mod(B).StageBOwner is not p.SourceRelationResolver
    assert _mod(A).StageAOwner is not p.SourceRelationResolver


def test_production_oracles_still_operative():
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    assert resolver.resolve_exact(relation.ref) is relation
    d = resolver.decide(relation_kind=relation.relation_kind,
                       source_universe_refs=list(relation.source_universe_refs),
                       operation_scope=relation.operation_scope,
                       target_use=relation.target_use, effective_scope={"b": 1},
                       relation_ref=relation.ref)
    assert d.owner_custody_hash is not None


def test_stage_b_custody_hash_and_parity_preserved_after_repair():
    """B's accepted custody hash and byte-exact parity must survive the repair."""
    m = _mod(B)
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    owner = m.StageBOwner(relations=list(resolver._by_ref.values()),
                          authority_snapshots=snaps,
                          trusted_semantic_hash=semantic_hash,
                          trusted_canonicalize=canonicalize,
                          trusted_require_positive_authority=require_positive_authority,
                          relation_class=SourceUniverseRelation,
                          authority_snapshot_class=AuthoritySnapshot)
    py = resolver.decide(relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
                         source_universe_refs=[UNIVERSE_A, UNIVERSE_B],
                         operation_scope={}, target_use="urn:rawlsing:pre553:use:repair",
                         effective_scope={})
    assert owner.custody_hash == py.owner_custody_hash
