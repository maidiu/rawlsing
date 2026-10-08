"""Bounded reproduction: warmed allocated-block trend for decide/resolve/construct.

    HQ_WT=<worktree> PYTHONPATH=<worktree> python3.11 hq248_leak_trend.py
Reports medians over repetitions with full spread so a zero-leak path is
distinguishable from a small constant leak and from measurement noise.
"""
import gc
import os
import statistics
import sys

sys.path.insert(0, os.environ.get("HQ_WT", "."))
import rawlsing_next._p07_native_owner_stage_b as M            # noqa: E402
from rawlsing_next.pre553_empirical_authority import require_positive_authority  # noqa: E402
from rawlsing_next.pre553_empirical_objects import (              # noqa: E402
    AuthoritySnapshot, SourceUniverseRelation, canonicalize, semantic_hash)
from rawlsing_next.tests.test_pre553_temporal_comparability import (  # noqa: E402
    UNIVERSE_A, UNIVERSE_B, _adjudicated_resolver)

r, rel = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
rels = list(r._by_ref.values())
snaps = list(r._registry._by_key.values())
srcs = list(rel.source_universe_refs)


def mk(rr=None, ss=None):
    return M.StageBOwner(relations=rels if rr is None else rr,
                         authority_snapshots=snaps if ss is None else ss,
                         trusted_semantic_hash=semantic_hash,
                         trusted_canonicalize=canonicalize,
                         trusted_require_positive_authority=require_positive_authority,
                         relation_class=SourceUniverseRelation,
                         authority_snapshot_class=AuthoritySnapshot)


o = mk()


def pos():
    return o.decide(relation_kind=rel.relation_kind, source_universe_refs=srcs,
                    operation_scope=rel.operation_scope, target_use=rel.target_use,
                    effective_scope=rel.effective_scope,
                    directionality_or_symmetric=rel.directionality_or_symmetric)


def neg():
    return o.decide(relation_kind="PROVENANCE_ORIGIN", source_universe_refs=srcs,
                    operation_scope={}, target_use="u", effective_scope={})


def trend(fn, label, n=2000, reps=7, warmup=4000):
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
    med = statistics.median(samples)
    verdict = "CLEAN (noise floor)" if med < 0.05 else "LEAK"
    print("  %-34s median=%9.5f spread=%.5f  %s" % (label, med, max(samples) - min(samples), verdict))
    return med


print("interpreter:", sys.version.split()[0])
trend(pos, "decide POSITIVE (genuine AUTHORIZED)")
trend(neg, "decide negative (descriptive)")
trend(lambda: o.resolve_exact(rel.ref), "resolve_exact")
d = pos()
trend(lambda: o.validate_decision_replay(d), "validate_decision_replay")
print("  --- admission path (bounded, per construction) ---")
trend(lambda: (lambda x: None)(mk([], [])),      "construct 0 rel 0 snap", 1500)
trend(lambda: (lambda x: None)(mk([], snaps)),   "construct 0 rel 1 snap", 1500)
trend(lambda: (lambda x: None)(mk(rels, [])),    "construct 1 rel 0 snap", 1500)
trend(lambda: (lambda x: None)(mk(rels, snaps)), "construct 1 rel 1 snap", 1500)
