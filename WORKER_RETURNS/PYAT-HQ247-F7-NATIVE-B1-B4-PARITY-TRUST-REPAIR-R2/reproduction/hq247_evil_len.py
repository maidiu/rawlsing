"""Bounded reproduction: adversarial __len__ against the native constructors.

Run in ITS OWN process. Never alongside a production or parity test.
    HQ_WT=<worktree> PYTHONPATH=<worktree> python3.11 hq247_evil_len.py stage_a|stage_b
Before the HQ246 repair these produced an out-of-bounds read (Stage A: ASAN SEGV).
"""
import os
import sys

sys.path.insert(0, os.environ["HQ_WT"])
which = sys.argv[1] if len(sys.argv) > 1 else "stage_a"

LIES = [0, 1, 5, 64, 10 ** 6, -1, -(10 ** 12), 2 ** 62, 2 ** 63 - 1,
        RuntimeError("boom"), MemoryError("no"), lambda: 4096]


class LyingList(list):
    def __init__(self, items, lie):
        super().__init__(items)
        self._lie = lie

    def __len__(self):
        v = self._lie() if callable(self._lie) else self._lie
        if isinstance(v, BaseException):
            raise v
        return v


class LyingTuple(tuple):
    def __new__(cls, items, lie):
        return super().__new__(cls, items)

    def __init__(self, items, lie):
        self._lie = lie

    def __len__(self):
        v = self._lie() if callable(self._lie) else self._lie
        if isinstance(v, BaseException):
            raise v
        return v


if which == "stage_a":
    import rawlsing_next._p07_native_owner_stage_a as M

    class Ref:
        key = "K|O|" + "a" * 64

    class Rel:
        ref = Ref()
        content_hash = "a" * 64

    for lie in LIES:
        for ctor in (lambda x: LyingList([Rel()], x), lambda x: LyingTuple((Rel(),), x)):
            try:
                o = M.StageAOwner.__new__(M.StageAOwner)
                o.__init__(ctor(lie), object(), lambda x: "f" * 64)
                print("!! ACCEPTED lying container lie=%r  <-- DEFECT" % (lie,))
            except (TypeError, M.SourceRelationIntegrityError):
                pass
            except Exception as e:
                print("!! unexpected %s for lie=%r" % (type(e).__name__, lie))
else:
    import rawlsing_next._p07_native_owner_stage_b as M
    from rawlsing_next.tests.test_pre553_temporal_comparability import (
        _adjudicated_resolver, UNIVERSE_A, UNIVERSE_B)
    from rawlsing_next.pre553_source_relations import semantic_hash
    from rawlsing_next.pre553_empirical_objects import (
        canonicalize, SourceUniverseRelation, AuthoritySnapshot)
    from rawlsing_next.pre553_empirical_authority import require_positive_authority

    r, rel = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(r._registry._by_key.values())
    for lie in LIES:
        for bad in (LyingList([rel], lie), LyingList(snaps, lie),
                    LyingTuple((rel,), lie), LyingTuple(tuple(snaps), lie)):
            kw = dict(relations=snaps and [rel], authority_snapshots=snaps,
                      trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
                      trusted_require_positive_authority=require_positive_authority,
                      relation_class=SourceUniverseRelation,
                      authority_snapshot_class=AuthoritySnapshot)
            kw["relations"] = bad if not isinstance(bad, tuple) else bad
            if bad is snaps:
                kw["relations"] = [rel]
                kw["authority_snapshots"] = LyingList(snaps, lie)
            try:
                M.StageBOwner(**kw)
                print("!! ACCEPTED lying container lie=%r <-- DEFECT" % (lie,))
            except (TypeError, M.SourceRelationIntegrityError):
                pass
            except Exception as e:
                print("!! unexpected %s for lie=%r" % (type(e).__name__, lie))
print("%s: all %d lying-container variants refused without crash" % (which, len(LIES)))
