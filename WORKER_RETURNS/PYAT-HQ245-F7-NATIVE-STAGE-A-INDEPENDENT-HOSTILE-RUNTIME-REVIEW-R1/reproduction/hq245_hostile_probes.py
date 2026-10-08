#!/usr/bin/env python3
"""HQ245 independent hostile probes for F7 native Stage A.

Written by the HQ245 reviewer. Does NOT import or reuse the author's test helpers.
Run: <governed python3.11> reproduction/hq245_hostile_probes.py
"""
import gc
import json
import sys
import weakref

sys.path.insert(0, ".")
import rawlsing_next._p07_native_owner_stage_a as M  # noqa: E402

out = {}


class Ref:
    def __init__(self, kind, oid, ch):
        self.kind, self.object_id, self.content_hash = kind, oid, ch

    @property
    def key(self):
        return f"{self.kind}|{self.object_id}|{self.content_hash}"

    def as_dict(self):
        return {"kind": self.kind, "object_id": self.object_id,
                "content_hash": self.content_hash}


class Standin:
    """Mutable stand-in relation: key+content_hash stay constant, semantics can change."""
    def __init__(self, ref, ch):
        self.ref = ref
        self.content_hash = ch
        self.semantic_payload = {"decision": "DENIED"}

    def semantic_projection(self):
        return dict(self.semantic_payload)


def mk(ch="a" * 64, kind="SourceUniverseRelation@1.0.0", oid="REL-1"):
    ref = Ref(kind, oid, ch)
    return Standin(ref, ch)


SEM_CALLS = {"n": 0}


def counting_semhash(x):
    SEM_CALLS["n"] += 1
    return "f" * 64


# ---------------------------------------------------------------- P1 registry
try:
    o = M.StageAOwner(relations=[mk()], authority_registry=42,
                      trusted_semantic_hash=counting_semhash)
    out["P1_registry_is_decorative"] = {
        "registry_42_accepted": True, "sealed": o.sealed,
        "note": "only 'registry is not None' is checked; Py_TYPE(registry)->tp_name is stored"}
except Exception as e:  # noqa: BLE001
    out["P1_registry_is_decorative"] = {"registry_42_accepted": False, "exc": str(e)}

# ------------------------------------------------- P4 trusted hash never used
SEM_CALLS["n"] = 0
o4 = M.StageAOwner(relations=[mk()], authority_registry=object(),
                   trusted_semantic_hash=counting_semhash)
o4.resolve_exact(mk().ref)
o4.resolve_exact({"kind": "SourceUniverseRelation@1.0.0", "object_id": "REL-1",
                  "content_hash": "a" * 64})
out["P4_trusted_semantic_hash_never_invoked"] = {
    "calls_during_construct_and_two_resolves": SEM_CALLS["n"],
    "claim_of_tcb_seam": "docstring claims semantic_hash is the projection re-verification seam",
}

# ------------------------------------------------------ P5 string-only verify
s = mk()
owner5 = M.StageAOwner(relations=[s], authority_registry=object(),
                       trusted_semantic_hash=counting_semhash)
s.semantic_payload = {"decision": "AUTHORIZED_AFTER_SEAL"}
got = owner5.resolve_exact(s.ref)
out["P5_identity_reverification_is_string_only"] = {
    "resolved_after_semantic_mutation": got is s,
    "mutated_payload_seen": got.semantic_payload,
    "note": "ref.key and content_hash strings unchanged, so semantic mutation is not detected",
}

# ----------------------------------------------------------- P6 unsealed new
u = M.StageAOwner.__new__(M.StageAOwner)
out["P6_unsealed_new"] = {"sealed": u.sealed}
try:
    u.resolve_exact(mk().ref)
    out["P6_unsealed_new"]["resolve"] = "UNEXPECTED_OK"
except M.SourceRelationIntegrityError as e:
    out["P6_unsealed_new"]["resolve"] = "refused: " + str(e)

# ------------------------------------------------- P7 copy/pickle/subclass
out["P7_ownership_transfer"] = {}
for name, fn in (("copy", lambda: __import__("copy").copy(owner5)),
                 ("deepcopy", lambda: __import__("copy").deepcopy(owner5)),
                 ("pickle", lambda: __import__("pickle").dumps(owner5))):
    try:
        fn()
        out["P7_ownership_transfer"][name] = "UNEXPECTED_OK"
    except Exception as e:  # noqa: BLE001
        out["P7_ownership_transfer"][name] = f"refused ({type(e).__name__})"
try:
    type("Sub", (M.StageAOwner,), {})
    out["P7_ownership_transfer"]["subclass"] = "UNEXPECTED_OK"
except TypeError as e:
    out["P7_ownership_transfer"]["subclass"] = f"refused ({e})"

# ---------------------------------------------------- P8 non-authorizing stubs
res8 = {}
for name in ("decide", "require"):
    try:
        getattr(owner5, name)()
        res8[name] = "UNEXPECTED_OK"
    except M.SourceRelationIntegrityError as e:
        res8[name] = str(e)[:60]
res8["positive_symbols_present"] = [
    s for s in dir(M) if s in ("AUTHORIZED", "RelationDecision", "authorize", "issue")]
res8["module_AUTHORIZING"] = getattr(M, "AUTHORIZING", "absent")
out["P8_non_authorizing"] = res8

# ------------------------------------------- P9 source vs empty victim owners
source = M.StageAOwner(relations=[mk(ch="b" * 64, oid="SRC")],
                       authority_registry=object(), trusted_semantic_hash=counting_semhash)
victim = M.StageAOwner(relations=[], authority_registry=object(),
                       trusted_semantic_hash=counting_semhash)
try:
    victim.resolve_exact(mk(ch="b" * 64, oid="SRC").ref)
    out["P9_empty_victim_resolve"] = "UNEXPECTED_OK"
except M.SourceRelationIntegrityError as e:
    out["P9_empty_victim_resolve"] = "refused: " + str(e)[:60]
try:
    M.StageAOwner(relations=[source], authority_registry=object(),
                  trusted_semantic_hash=counting_semhash)
    out["P9_owner_as_relation_input"] = "UNEXPECTED_OK"
except Exception as e:  # noqa: BLE001
    out["P9_owner_as_relation_input"] = f"refused ({type(e).__name__})"
out["P9_source_resolves"] = source.resolve_exact(mk(ch="b" * 64, oid="SRC").ref) is not None

# ---------------------------------------------- P2 custody_diagnostic leak
owner2 = M.StageAOwner(relations=[mk()], authority_registry=object(),
                       trusted_semantic_hash=counting_semhash)
gc.collect()
before = sum(1 for o in gc.get_objects() if isinstance(o, list))
N = 20000
for _ in range(N):
    owner2.custody_diagnostic()
gc.collect()
after = sum(1 for o in gc.get_objects() if isinstance(o, list))
out["P2_custody_diagnostic_list_leak"] = {
    "calls": N, "tracked_lists_before": before, "tracked_lists_after": after,
    "growth": after - before,
    "verdict": "LEAK" if (after - before) > N // 2 else "no obvious leak",
}

# ---------------------------------------- P3 repeated failing __init__ leak
sem = counting_semhash
obj = M.StageAOwner.__new__(M.StageAOwner)
rc0 = sys.getrefcount(sem)
iters = 2000
for _ in range(iters):
    try:
        obj.__init__(relations=[object()], authority_registry=object(),
                     trusted_semantic_hash=sem)
    except Exception:  # noqa: BLE001
        pass
rc1 = sys.getrefcount(sem)
out["P3_repeated_failing_init_refcount_leak"] = {
    "iterations": iters, "refcount_before": rc0, "refcount_after": rc1,
    "growth": rc1 - rc0,
    "verdict": "REFCOUNT LEAK" if (rc1 - rc0) > iters // 2 else "no obvious leak",
}

print(json.dumps(out, indent=2, sort_keys=True, default=str))
