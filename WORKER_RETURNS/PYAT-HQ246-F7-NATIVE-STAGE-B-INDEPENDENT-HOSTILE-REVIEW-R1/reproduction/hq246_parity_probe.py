#!/usr/bin/env python3
"""HQ246 parity probe: can native Stage B decide() select a genuine positive candidate?

Reviewer-written. Uses the PRE-EXISTING lawful F7 fixture `_adjudicated_resolver` only to
build a genuine production relation; the probes and comparisons are the reviewer's.

Usage: <governed python3.11> hq246_parity_probe.py <mode>
"""
import json
import sys

sys.path.insert(0, ".")
from rawlsing_next.tests.test_pre553_temporal_comparability import (  # noqa: E402
    UNIVERSE_A, UNIVERSE_B, _adjudicated_resolver,
)
from rawlsing_next.pre553_empirical_authority import require_positive_authority  # noqa: E402
from rawlsing_next.pre553_empirical_objects import (  # noqa: E402
    AuthoritySnapshot, canonicalize, semantic_hash,
)
from rawlsing_next.pre553_source_relations import SourceUniverseRelation  # noqa: E402
from rawlsing_next import _p07_native_owner_stage_b as M  # noqa: E402


def build():
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    owner = M.StageBOwner(
        relations=[relation], authority_snapshots=snaps,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=SourceUniverseRelation,
        authority_snapshot_class=AuthoritySnapshot)
    return resolver, relation, owner


def main():
    mode = sys.argv[1]
    resolver, relation, owner = build()
    out = {
        "mode": mode,
        "relation_kind": relation.relation_kind,
        "relation_effective_scope": repr(relation.effective_scope),
        "relation_directionality": repr(relation.directionality_or_symmetric),
        "native_object_key_material_uses": "effective_scope='DISTINCT_BY_DEFAULT', directionality='SYMMETRIC' (hardcoded in admit_relation)",
    }
    common = dict(relation_kind=relation.relation_kind,
                  source_universe_refs=list(relation.source_universe_refs),
                  operation_scope=relation.operation_scope,
                  target_use=relation.target_use,
                  relation_ref=relation.ref)

    if mode == "python_baseline":
        d = resolver.decide(effective_scope=relation.effective_scope, **common)
        out["python_state"] = d.state
        out["python_authorized"] = bool(d.authorized)
    elif mode == "native_real_params":
        d = owner.decide(effective_scope=relation.effective_scope,
                         directionality_or_symmetric=relation.directionality_or_symmetric,
                         **common)
        out["native_state"] = d["state"]
        out["native_authorized"] = d["authorized"]
        out["native_reason"] = d["reason"]
    elif mode == "native_hardcoded_key_params":
        d = owner.decide(effective_scope="DISTINCT_BY_DEFAULT",
                         directionality_or_symmetric="SYMMETRIC", **common)
        out["native_state"] = d["state"]
        out["native_authorized"] = d["authorized"]
        out["native_reason"] = d["reason"]
    else:
        out["result"] = "UNKNOWN_MODE"
    print("HQ246JSON " + json.dumps(out, sort_keys=True, default=str))


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------- extra modes
def _extra(mode):
    """Modes appended by the reviewer for TCB-provenance and negative-path parity."""
    if mode == "attacker_custody_owner":
        from rawlsing_next.pre553_empirical_objects import ExactRef
        class ARef2:
            authority_id, authority_version = "EQ1", "1.0.0"
            authority_content_hash = "b" * 64
            @property
            def key(self):
                return f"{self.authority_id}|{self.authority_version}|{self.authority_content_hash}"
            def as_dict(self):
                return {"authority_id": self.authority_id,
                        "authority_version": self.authority_version,
                        "authority_content_hash": self.authority_content_hash}
        class R2:
            def __init__(self, oid):
                self.kind, self.object_id, self.content_hash = "SourceUniverse", oid, "a" * 64
            @property
            def key(self):
                return f"{self.kind}|{self.object_id}|{self.content_hash}"
            def as_dict(self):
                return {"kind": self.kind, "object_id": self.object_id,
                        "content_hash": self.content_hash}
        class AttackRel:
            ref = R2("U-A"); content_hash = "d" * 64
            relation_kind = "SOURCE_SEMANTIC_EQUIVALENCE"
            authority_operation = "SEMANTIC_EQUIVALENCE_ADMISSION"
            target_use = "USE-1"; relation_authority_ref = ARef2()
            operation_scope = {"s": 1}; source_universe_refs = (R2("U-A"), R2("U-B"))
            semantic_fields = {"decision": "AUTHORIZED", "replay_identity": "r" * 64}
            def semantic_projection(self):
                return {"p": 1}
        class AttackSnap:
            authority_ref = ARef2(); content_hash = "d" * 64
            def semantic_projection(self):
                return {"s": 1}
        o = M.StageBOwner(
            relations=[AttackRel()], authority_snapshots=[AttackSnap()],
            trusted_semantic_hash=(lambda v: "d" * 64),
            trusted_canonicalize=(lambda v: v),
            trusted_require_positive_authority=(lambda a, b: True),
            relation_class=AttackRel, authority_snapshot_class=AttackSnap)
        got = o.resolve_exact(AttackRel.ref)
        return {"attacker_classes_and_callables_accepted": True,
                "sealed": o.sealed, "counts": o.counts,
                "resolve_exact_returned_attacker_relation": type(got).__name__,
                "custody_hash_len": len(o.custody_hash)}
    if mode == "unknown_kind_unresolvable_ref":
        from rawlsing_next.pre553_empirical_objects import ExactRef
        ghost = ExactRef("SourceUniverseRelation@1.0.0", "GHOST",
                         "0" * 64)
        try:
            resolver.decide(relation_kind="NOT_A_KIND",
                            source_universe_refs=list(relation.source_universe_refs),
                            operation_scope=relation.operation_scope,
                            target_use=relation.target_use,
                            effective_scope=relation.effective_scope,
                            relation_ref=ghost)
            py = "NO_ERROR"
        except Exception as exc:  # noqa: BLE001
            py = f"{type(exc).__name__}: {exc}"
        try:
            owner.decide(relation_kind="NOT_A_KIND",
                         source_universe_refs=list(relation.source_universe_refs),
                         operation_scope=relation.operation_scope,
                         target_use=relation.target_use,
                         effective_scope=relation.effective_scope,
                         relation_ref=ghost)
            nat = "NO_ERROR"
        except Exception as exc:  # noqa: BLE001
            nat = f"{type(exc).__name__}: {exc}"
        return {"python": py, "native": nat}
    return {"result": "UNKNOWN_EXTRA_MODE"}


_EXTRA_MODES = {"attacker_custody_owner", "unknown_kind_unresolvable_ref"}

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] in _EXTRA_MODES:
    _resolver, _relation, _owner = build()
    resolver, relation, owner = _resolver, _relation, _owner
    print("HQ246JSON " + json.dumps(_extra(sys.argv[1]), sort_keys=True, default=str))
    sys.exit(0)
