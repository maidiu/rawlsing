#!/usr/bin/env python3
"""HQ246 independent hostile probes for frozen Stage B (reviewer-written).

Usage: <governed python3.11> hq246_hostile_probes.py <mode>
Each mode is meant to be run in its own subprocess; it prints one JSON line.
"""
import gc
import json
import sys

sys.path.insert(0, ".")
from rawlsing_next import _p07_native_owner_stage_b as M  # noqa: E402


class Ref:
    def __init__(self, oid="U-A", kind="SourceUniverse", ch="a" * 64):
        self.kind, self.object_id, self.content_hash = kind, oid, ch

    @property
    def key(self):
        return f"{self.kind}|{self.object_id}|{self.content_hash}"

    def as_dict(self):
        return {"kind": self.kind, "object_id": self.object_id,
                "content_hash": self.content_hash}


class ARef:
    def __init__(self, aid="EQ1", ver="1.0.0", ch="b" * 64):
        self.authority_id, self.authority_version, self.authority_content_hash = aid, ver, ch

    @property
    def key(self):
        return f"{self.authority_id}|{self.authority_version}|{self.authority_content_hash}"

    def as_dict(self):
        return {"authority_id": self.authority_id,
                "authority_version": self.authority_version,
                "authority_content_hash": self.authority_content_hash}


class FR:
    ref = Ref("U-A")
    content_hash = "d" * 64
    relation_kind = "SOURCE_SEMANTIC_EQUIVALENCE"
    authority_operation = "SEMANTIC_EQUIVALENCE_ADMISSION"
    target_use = "USE-1"
    relation_authority_ref = ARef()
    operation_scope = {"s": 1}
    source_universe_refs = (Ref("U-A"), Ref("U-B"))
    semantic_fields = {"decision": "AUTHORIZED", "replay_identity": "r" * 64}

    def semantic_projection(self):
        return {"p": 1}


class FS:
    authority_ref = ARef()
    content_hash = "d" * 64

    def semantic_projection(self):
        return {"s": 1}


class BadFS(FS):
    content_hash = "b" * 64


SEM = lambda v: "d" * 64           # noqa: E731
CANON = lambda v: v                # noqa: E731
REQ = lambda snap, kw: True        # noqa: E731


def build(rels=None, snaps=None, sem=SEM, canon=CANON, req=REQ, rcls=FR, scls=FS):
    o = M.StageBOwner.__new__(M.StageBOwner)
    o.__init__(relations=[FR()] if rels is None else rels,
               authority_snapshots=[FS()] if snaps is None else snaps,
               trusted_semantic_hash=sem, trusted_canonicalize=canon,
               trusted_require_positive_authority=req,
               relation_class=rcls, authority_snapshot_class=scls)
    return o


DEC_ARGS = dict(relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
                source_universe_refs=[Ref("U-A"), Ref("U-B")],
                operation_scope={"s": 1}, target_use="USE-1",
                effective_scope={"s": 1})


def main():
    mode = sys.argv[1]
    out = {"mode": mode}
    try:
        if mode == "trusted_callable_forgery":
            # A forger supplies its own always-positive require_positive_authority,
            # its own semantic_hash, its own canonicalize AND its own classes.
            o = build()
            d = o.decide(**DEC_ARGS)
            out["state"] = d["state"]
            out["authorized"] = d["authorized"]
            out["custody_hash"] = o.custody_hash
            out["forged"] = (d["state"] == "AUTHORIZED")
        elif mode == "validate_replay_nonstr_relation_kind":
            o = build()
            d = o.decide(**DEC_ARGS)
            before = d["state"]
            d["relation_kind"] = 123
            o.validate_decision_replay(d)
            out["result"] = "SURVIVED"
            out["before"] = before
        elif mode == "validate_replay_nonstr_target_use":
            o = build()
            d = o.decide(**DEC_ARGS)
            d["target_use"] = 123
            o.validate_decision_replay(d)
            out["result"] = "SURVIVED"
        elif mode == "negative_validation_path_crash":
            # decision AUTHORIZED but the snapshot semantic identity does not re-derive,
            # so validate_positive() fails and stb_decide takes the negative ladder path.
            o = build(rels=[FR()], snaps=[BadFS()])
            d = o.decide(**DEC_ARGS)
            out["state"] = d["state"]
            out["result"] = "SURVIVED"
        elif mode == "under_report_truncation":
            class Evil(list):
                def __len__(self):
                    return 1
            o = build(rels=Evil([FR(), FR(), FR()]), snaps=[FS()])
            out["counts"] = o.counts
            out["result"] = "SURVIVED"
        elif mode == "failing_init_refcount_leak":
            sem = lambda v: "d" * 64           # noqa: E731
            obj = M.StageBOwner.__new__(M.StageBOwner)
            rc0 = sys.getrefcount(sem)
            iters = 2000
            for _ in range(iters):
                try:
                    obj.__init__(relations=[object()], authority_snapshots=[FS()],
                                 trusted_semantic_hash=sem, trusted_canonicalize=CANON,
                                 trusted_require_positive_authority=REQ,
                                 relation_class=FR, authority_snapshot_class=FS)
                except Exception:  # noqa: BLE001
                    pass
            rc1 = sys.getrefcount(sem)
            out["iterations"] = iters
            out["refcount_growth"] = rc1 - rc0
        elif mode == "decide_snapshot_missing_op_leak":
            # relation references an authority key with no matching snapshot:
            # validate_positive returns at "snapshot is absent" and leaks the strdup'd op.
            class Rel2(FR):
                relation_authority_ref = ARef("MISSING", "9.9.9", "e" * 64)
            o = build(rels=[Rel2()], snaps=[FS()])
            d = o.decide(**DEC_ARGS)
            out["decide_state"] = d["state"]
            gc.collect()
            before = len(gc.get_objects())
            N = 50000
            for _ in range(N):
                o.decide(**DEC_ARGS)
            gc.collect()
            after = len(gc.get_objects())
            out["decide_calls"] = N
            out["gc_object_growth"] = after - before
        else:
            out["result"] = "UNKNOWN_MODE"
    except Exception as exc:  # noqa: BLE001
        out["result"] = "EXC"
        out["exc"] = f"{type(exc).__name__}: {str(exc)[:120]}"
    print("HQ246JSON " + json.dumps(out, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
