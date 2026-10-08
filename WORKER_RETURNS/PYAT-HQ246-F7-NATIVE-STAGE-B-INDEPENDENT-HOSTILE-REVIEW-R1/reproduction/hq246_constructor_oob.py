#!/usr/bin/env python3
"""HQ246 independent reproduction of the inherited Stage B constructor bounds defect.

Reviewer-written. Uses NO author test helper. It builds the native StageBOwner with
attacker-supplied relation/snapshot classes and trusted callables (which is itself the
trusted-seam forgery surface) so that admission of element 0 SUCCEEDS and the loop can be
driven past the true sequence length by an over-reporting __len__.

Modes are run in separate subprocesses by the driver; this file prints one JSON line.
Usage: <governed python3.11> hq246_constructor_oob.py <mode>
"""
import json
import sys

sys.path.insert(0, ".")
import rawlsing_next._p07_native_owner_stage_b as B  # noqa: E402


class Ref:
    def __init__(self, kind="SourceUniverse", object_id="U-A", content_hash="a" * 64):
        self.kind, self.object_id, self.content_hash = kind, object_id, content_hash

    @property
    def key(self):
        return f"{self.kind}|{self.object_id}|{self.content_hash}"

    def as_dict(self):
        return {"kind": self.kind, "object_id": self.object_id,
                "content_hash": self.content_hash}


class ARef:
    def __init__(self, authority_id="EQ1", authority_version="1.0.0",
                 authority_content_hash="b" * 64):
        self.authority_id = authority_id
        self.authority_version = authority_version
        self.authority_content_hash = authority_content_hash

    @property
    def key(self):
        return f"{self.authority_id}|{self.authority_version}|{self.authority_content_hash}"

    def as_dict(self):
        return {"authority_id": self.authority_id,
                "authority_version": self.authority_version,
                "authority_content_hash": self.authority_content_hash}


class FakeRel:
    ref = Ref()
    content_hash = "c" * 64
    relation_kind = "SOURCE_SEMANTIC_EQUIVALENCE"
    authority_operation = "SEMANTIC_EQUIVALENCE_ADMISSION"
    target_use = "USE-1"
    relation_authority_ref = ARef()
    operation_scope = {"scope": "EXACT_BOUND_UNIVERSE_PAIR"}
    source_universe_refs = (Ref(object_id="U-A"), Ref(object_id="U-B"))
    semantic_fields = {"decision": "AUTHORIZED", "replay_identity": "r" * 64}

    def semantic_projection(self):
        return {"p": 1}


class FakeSnap:
    authority_ref = ARef()
    content_hash = "b" * 64

    def semantic_projection(self):
        return {"s": 1}


SEM = lambda v: "d" * 64          # noqa: E731  attacker-supplied trusted hash
CANON = lambda v: v               # noqa: E731  attacker-supplied canonicalize
REQ = lambda snap, kw: True       # noqa: E731  attacker-supplied always-positive authority


def make_rel_list():
    return [FakeRel()]


def make_snap_list():
    return [FakeSnap()]


def build(relations, snaps):
    obj = B.StageBOwner.__new__(B.StageBOwner)
    obj.__init__(relations=relations, authority_snapshots=snaps,
                 trusted_semantic_hash=SEM, trusted_canonicalize=CANON,
                 trusted_require_positive_authority=REQ,
                 relation_class=FakeRel, authority_snapshot_class=FakeSnap)
    return obj


def main():
    mode = sys.argv[1]
    out = {"mode": mode}
    try:
        if mode == "rel_over":
            class Evil(list):
                def __len__(self):
                    return 5
            o = build(Evil(make_rel_list()), make_snap_list())
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        elif mode == "snap_over":
            class Evil(list):
                def __len__(self):
                    return 5
            o = build(make_rel_list(), Evil(make_snap_list()))
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        elif mode == "rel_under":
            class Evil(list):
                def __len__(self):
                    return 1
            o = build(Evil(make_rel_list() + make_rel_list() + make_rel_list()),
                      make_snap_list())
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        elif mode == "rel_raise_len":
            class Evil(list):
                def __len__(self):
                    raise RuntimeError("hostile __len__")
            try:
                build(Evil(make_rel_list()), make_snap_list())
                out["result"] = "SURVIVED"
            except Exception as exc:  # noqa: BLE001
                out["result"] = "EXC"; out["exc"] = f"{type(exc).__name__}: {exc}"
        elif mode == "rel_neg_len":
            class Evil(list):
                def __len__(self):
                    return -1
            try:
                build(Evil(make_rel_list()), make_snap_list())
                out["result"] = "SURVIVED"
            except Exception as exc:  # noqa: BLE001
                out["result"] = "EXC"; out["exc"] = f"{type(exc).__name__}: {exc}"
        elif mode == "rel_huge_len":
            class Evil(list):
                def __len__(self):
                    return 2 ** 31
            try:
                build(Evil(make_rel_list()), make_snap_list())
                out["result"] = "SURVIVED"
            except Exception as exc:  # noqa: BLE001
                out["result"] = "EXC"; out["exc"] = f"{type(exc).__name__}: {exc}"
        elif mode == "rel_tuple_over":
            class EvilT(tuple):
                def __len__(self):
                    return 4
            try:
                o = build(EvilT(tuple(make_rel_list())), make_snap_list())
                out["result"] = "SURVIVED"; out["counts"] = o.counts
            except Exception as exc:  # noqa: BLE001
                out["result"] = "EXC"; out["exc"] = f"{type(exc).__name__}: {exc}"
        elif mode == "exact_control":
            o = build(make_rel_list(), make_snap_list())
            out["result"] = "SURVIVED"; out["counts"] = o.counts
        else:
            out["result"] = "UNKNOWN_MODE"
    except Exception as exc:  # noqa: BLE001
        out["result"] = "EXC"; out["exc"] = f"{type(exc).__name__}: {exc}"
    print("HQ246JSON " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
