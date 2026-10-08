#!/usr/bin/env python3
"""HQ247 independent D1 reproducer for the frozen f09 repair.

Reviewer-written, self-contained. Does NOT reuse author test helpers. For each mode it
constructs the native owner with a list/tuple SUBCLASS whose __len__ lies, in both owner
dimensions, and reports the outcome. Each mode must be run in its own subprocess.

Usage: <governed python3.11> hq247_d1_oob_probe.py <mode>
"""
import json
import sys

sys.path.insert(0, ".")
from rawlsing_next import _p07_native_owner_stage_a as A  # noqa: E402
from rawlsing_next import _p07_native_owner_stage_b as B  # noqa: E402


class Registry:
    """Non-scalar registry object for D6 Stage A admission."""
    def __init__(self):
        self.snapshots = ()


class Ref:
    def __init__(self, oid="U-A", ch="a" * 64, kind="SourceUniverse"):
        self.kind, self.object_id, self.content_hash = kind, oid, ch

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
    """Minimal relation accepted by Stage A (ref.key + content_hash + projection)."""
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


SEM = lambda v: "d" * 64            # noqa: E731
CANON = lambda v: v                 # noqa: E731
REQ = lambda a, b: True             # noqa: E731


def build_a(relations):
    o = A.StageAOwner.__new__(A.StageAOwner)
    o.__init__(relations=relations, authority_registry=Registry(),
               trusted_semantic_hash=SEM)
    return o


def build_b(relations, snaps):
    o = B.StageBOwner.__new__(B.StageBOwner)
    o.__init__(relations=relations, authority_snapshots=snaps,
               trusted_semantic_hash=SEM, trusted_canonicalize=CANON,
               trusted_require_positive_authority=REQ,
               relation_class=BRel, authority_snapshot_class=BSnap)
    return o


class Lie(list):
    def __init__(self, items, claim):
        super().__init__(items)
        self._claim = claim

    def __len__(self):
        if isinstance(self._claim, Exception):
            raise self._claim
        return self._claim


class LieT(tuple):
    def __new__(cls, items, claim):
        self = super().__new__(cls, items)
        self._claim = claim
        return self

    def __len__(self):
        if isinstance(self._claim, Exception):
            raise self._claim
        return self._claim


def main():
    mode = sys.argv[1]
    out = {"mode": mode}
    try:
        if mode == "A_rel_over":
            o = build_a(Lie([ARel()], 9))
            out["result"] = "SURVIVED"; out["sealed"] = o.sealed
        elif mode == "A_rel_under":
            o = build_a(Lie([ARel(), ARel(), ARel()], 0))
            out["result"] = "SURVIVED"; out["sealed"] = o.sealed
        elif mode == "A_tuple_over":
            o = build_a(LieT((ARel(),), 4))
            out["result"] = "SURVIVED"; out["sealed"] = o.sealed
        elif mode == "A_raise_len":
            build_a(Lie([ARel()], RuntimeError("hostile __len__")))
            out["result"] = "SURVIVED"
        elif mode == "A_neg_len":
            build_a(Lie([ARel()], -1))
            out["result"] = "SURVIVED"
        elif mode == "A_exact_control":
            o = build_a([ARel()])
            out["result"] = "SURVIVED"; out["sealed"] = o.sealed
        elif mode == "B_rel_over":
            o = build_b(Lie([BRel() for _ in range(8)], 9), [BSnap()])
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        elif mode == "B_rel_over1":
            o = build_b(Lie([BRel()], 5), [BSnap()])
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        elif mode == "B_snap_over":
            o = build_b([BRel()], Lie([BSnap() for _ in range(8)], 9))
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        elif mode == "B_rel_under":
            o = build_b(Lie([BRel(), BRel(), BRel()], 0), [BSnap()])
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        elif mode == "B_tuple_over":
            o = build_b(LieT((BRel(),), 4), [BSnap()])
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        elif mode == "B_raise_len":
            build_b(Lie([BRel()], RuntimeError("hostile __len__")), [BSnap()])
            out["result"] = "SURVIVED"
        elif mode == "B_neg_len":
            build_b(Lie([BRel()], -1), [BSnap()])
            out["result"] = "SURVIVED"
        elif mode == "B_exact_control":
            o = build_b([BRel()], [BSnap()])
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        else:
            out["result"] = "UNKNOWN_MODE"
    except Exception as exc:  # noqa: BLE001
        out["result"] = "REFUSED"
        out["exc"] = f"{type(exc).__name__}: {str(exc)[:110]}"
        out["exc_module"] = type(exc).__module__
    print("HQ247JSON " + json.dumps(out, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
