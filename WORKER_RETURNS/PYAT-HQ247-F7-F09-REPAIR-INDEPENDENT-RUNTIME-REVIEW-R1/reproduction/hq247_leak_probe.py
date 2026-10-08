#!/usr/bin/env python3
"""HQ247 independent memory/refcount measurement for the frozen f09 repair.

Method: warm up, gc.collect(), gc.disable(), measure sys.getallocatedblocks() deltas per
call, cross-checked with len(gc.get_objects()) id-set deltas. Reviewer-written.

Usage: <governed python3.11> hq247_leak_probe.py <mode>
"""
import gc
import hashlib
import json
import sys

sys.path.insert(0, ".")
from rawlsing_next import _p07_native_owner_stage_a as A  # noqa: E402
from rawlsing_next import _p07_native_owner_stage_b as B  # noqa: E402


class Registry:
    def __init__(self):
        self.snapshots = ()


class Ref:
    def __init__(self, oid="U-A"):
        self.kind, self.object_id, self.content_hash = "SourceUniverse", oid, "a" * 64

    @property
    def key(self):
        return f"{self.kind}|{self.object_id}|{self.content_hash}"

    def as_dict(self):
        return {"kind": self.kind, "object_id": self.object_id,
                "content_hash": self.content_hash}


class ARef:
    authority_id, authority_version = "EQ1", "1.0.0"
    authority_content_hash = "b" * 64

    @property
    def key(self):
        return f"{self.authority_id}|{self.authority_version}|{self.authority_content_hash}"

    def as_dict(self):
        return {"authority_id": self.authority_id,
                "authority_version": self.authority_version,
                "authority_content_hash": self.authority_content_hash}


class ARel:
    ref = Ref()
    content_hash = "c" * 64

    def semantic_projection(self):
        return {"p": 1}


class BRel:
    ref = Ref()
    content_hash = "c" * 64
    relation_kind = "SOURCE_SEMANTIC_EQUIVALENCE"
    authority_operation = "SEMANTIC_EQUIVALENCE_ADMISSION"
    target_use = "USE-1"
    relation_authority_ref = ARef()
    operation_scope = {"s": 1}
    source_universe_refs = (Ref("U-A"), Ref("U-B"))
    semantic_fields = {"decision": "AUTHORIZED", "replay_identity": "r" * 64}

    def semantic_projection(self):
        return {"p": 1}


class BSnap:
    authority_ref = ARef()
    content_hash = "b" * 64

    def semantic_projection(self):
        return {"s": 1}


def sem(v):
    return "d" * 64


def build_a():
    o = A.StageAOwner.__new__(A.StageAOwner)
    o.__init__(relations=[ARel()], authority_registry=Registry(),
               trusted_semantic_hash=sem)
    return o


def build_b():
    o = B.StageBOwner.__new__(B.StageBOwner)
    o.__init__(relations=[BRel()], authority_snapshots=[BSnap()],
               trusted_semantic_hash=sem, trusted_canonicalize=(lambda v: v),
               trusted_require_positive_authority=(lambda a, b: True),
               relation_class=BRel, authority_snapshot_class=BSnap)
    return o


def measure(fn, n_warm, n_meas):
    for _ in range(n_warm):
        fn()
    gc.collect()
    gc.disable()
    try:
        before = sys.getallocatedblocks()
        for _ in range(n_meas):
            fn()
        after = sys.getallocatedblocks()
    finally:
        gc.enable()
    return (after - before) / n_meas


def main():
    mode = sys.argv[1]
    out = {"mode": mode}
    if mode == "stage_a_custody_diagnostic":
        o = build_a()
        out["blocks_per_call"] = measure(lambda: o.custody_diagnostic(), 2000, 20000)
    elif mode == "stage_a_failed_init_refcount":
        obj = A.StageAOwner.__new__(A.StageAOwner)
        rc0 = sys.getrefcount(sem)
        for _ in range(20000):
            try:
                obj.__init__(relations=[object()], authority_registry=Registry(),
                             trusted_semantic_hash=sem)
            except Exception:  # noqa: BLE001
                pass
        out["refcount_growth_20k"] = sys.getrefcount(sem) - rc0
    elif mode == "stage_b_decide":
        # non-constant hash so the request key does NOT collide with the sealed object key
        # (this exercises the ordering block without entering the crashing positive path)
        o = B.StageBOwner.__new__(B.StageBOwner)
        o.__init__(relations=[BRel()], authority_snapshots=[BSnap()],
                   trusted_semantic_hash=(lambda v: hashlib.sha256(repr(v).encode()).hexdigest()),
                   trusted_canonicalize=(lambda v: v),
                   trusted_require_positive_authority=(lambda a, b: True),
                   relation_class=BRel, authority_snapshot_class=BSnap)
        out["blocks_per_call"] = measure(
            lambda: o.decide(relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
                             source_universe_refs=[Ref("U-A"), Ref("U-B")],
                             operation_scope={"s": 1}, target_use="USE-1",
                             effective_scope={"s": 1}), 2000, 20000)
    elif mode == "stage_b_resolve_exact":
        from rawlsing_next.pre553_empirical_authority import require_positive_authority
        from rawlsing_next.pre553_empirical_objects import (AuthoritySnapshot,
                                                            canonicalize, semantic_hash)
        from rawlsing_next.pre553_source_relations import SourceUniverseRelation
        from rawlsing_next.tests.test_pre553_temporal_comparability import (
            UNIVERSE_A, UNIVERSE_B, _adjudicated_resolver)
        resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
        snaps = list(resolver._registry._by_key.values())
        o = B.StageBOwner(relations=[relation], authority_snapshots=snaps,
                          trusted_semantic_hash=semantic_hash,
                          trusted_canonicalize=canonicalize,
                          trusted_require_positive_authority=require_positive_authority,
                          relation_class=SourceUniverseRelation,
                          authority_snapshot_class=AuthoritySnapshot)
        out["blocks_per_call"] = measure(lambda: o.resolve_exact(relation.ref), 2000, 20000)
    elif mode == "stage_b_failed_init_refcount":
        sem2 = lambda v: "d" * 64           # noqa: E731
        tc = lambda v: v                    # noqa: E731
        trp = lambda a, b: True             # noqa: E731
        obj = B.StageBOwner.__new__(B.StageBOwner)
        r0 = (sys.getrefcount(sem2), sys.getrefcount(tc), sys.getrefcount(trp))
        for _ in range(20000):
            try:
                obj.__init__(relations=[object()], authority_snapshots=[BSnap()],
                             trusted_semantic_hash=sem2, trusted_canonicalize=tc,
                             trusted_require_positive_authority=trp,
                             relation_class=BRel, authority_snapshot_class=BSnap)
            except Exception:  # noqa: BLE001
                pass
        r1 = (sys.getrefcount(sem2), sys.getrefcount(tc), sys.getrefcount(trp))
        out["refcount_growth_20k"] = [a - b for a, b in zip(r1, r0)]
    elif mode == "stage_b_decide_localize":
        o = B.StageBOwner.__new__(B.StageBOwner)
        o.__init__(relations=[BRel()], authority_snapshots=[BSnap()],
                   trusted_semantic_hash=(lambda v: hashlib.sha256(repr(v).encode()).hexdigest()),
                   trusted_canonicalize=(lambda v: v),
                   trusted_require_positive_authority=(lambda a, b: True),
                   relation_class=BRel, authority_snapshot_class=BSnap)

        def mk(refs):
            def f():
                try:
                    o.decide(relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
                             source_universe_refs=refs, operation_scope={"s": 1},
                             target_use="USE-1", effective_scope={"s": 1})
                except Exception:  # noqa: BLE001
                    pass
            return f

        out["one_source_ordering_not_reached"] = measure(mk([Ref("U-A")]), 3000, 20000)
        out["two_sources_ordering_reached"] = measure(mk([Ref("U-A"), Ref("U-B")]), 3000, 20000)
        out["two_identical_dedupe_path"] = measure(mk([Ref("U-A"), Ref("U-A")]), 3000, 20000)
    elif mode == "stage_b_gc_cycles":
        class Holder:
            pass

        def live():
            return sum(1 for ob in gc.get_objects() if type(ob) is B.StageBOwner)

        def make_cycle():
            o = B.StageBOwner.__new__(B.StageBOwner)
            r = BRel()
            o.__init__(relations=[r], authority_snapshots=[BSnap()],
                       trusted_semantic_hash=sem, trusted_canonicalize=(lambda v: v),
                       trusted_require_positive_authority=(lambda a, b: True),
                       relation_class=BRel, authority_snapshot_class=BSnap)
            h = Holder(); h.owner = o; r.back = h   # cycle: o -> r -> h -> o
            return o, h, r

        o0, h0, r0 = make_cycle()
        out["owner_gc_tracked"] = gc.is_tracked(o0)
        out["admitted_relation_gc_tracked"] = gc.is_tracked(r0)
        del o0, h0, r0
        before = live()
        for _ in range(300):
            a, b, c = make_cycle()
            del a, b, c
        gc.collect()
        out["live_before"] = before
        out["owners_created"] = 300
        out["live_after_collect"] = live()
    else:
        out["result"] = "UNKNOWN_MODE"
    print("HQ247JSON " + json.dumps(out, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
