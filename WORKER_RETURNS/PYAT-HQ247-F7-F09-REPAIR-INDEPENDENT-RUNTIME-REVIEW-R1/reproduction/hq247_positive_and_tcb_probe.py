#!/usr/bin/env python3
"""HQ247 mandatory independent probes for the frozen f09 repair.

Reviewer-written. Uses the PRE-EXISTING lawful F7 fixture `_adjudicated_resolver` only to
build a genuine production relation; every probe and comparison is the reviewer's.

Usage: <governed python3.11> hq247_positive_and_tcb_probe.py <mode>
"""
import hashlib
import json
import sys

sys.path.insert(0, ".")
from rawlsing_next.tests.test_pre553_temporal_comparability import (  # noqa: E402
    UNIVERSE_A, UNIVERSE_B, _adjudicated_resolver,
)
from rawlsing_next.pre553_empirical_authority import require_positive_authority  # noqa: E402
from rawlsing_next.pre553_empirical_objects import (  # noqa: E402
    AuthoritySnapshot, ExactRef, canonicalize, semantic_hash,
)
from rawlsing_next.pre553_source_relations import SourceUniverseRelation  # noqa: E402
from rawlsing_next import _p07_native_owner_stage_b as M  # noqa: E402


def genuine_owner():
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    snaps = list(resolver._registry._by_key.values())
    owner = M.StageBOwner(
        relations=[relation], authority_snapshots=snaps,
        trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
        trusted_require_positive_authority=require_positive_authority,
        relation_class=SourceUniverseRelation,
        authority_snapshot_class=AuthoritySnapshot)
    return resolver, relation, owner


OUT = {}


def main():
    mode = sys.argv[1]
    resolver, relation, owner = genuine_owner()
    common = dict(relation_kind=relation.relation_kind,
                  source_universe_refs=list(relation.source_universe_refs),
                  operation_scope=relation.operation_scope,
                  target_use=relation.target_use,
                  relation_ref=relation.ref)
    OUT["mode"] = mode
    OUT["relation_effective_scope"] = repr(relation.effective_scope)
    OUT["relation_directionality"] = repr(relation.directionality_or_symmetric)
    OUT["native_object_key_material"] = "hardcoded effective_scope='DISTINCT_BY_DEFAULT', directionality='SYMMETRIC' (admit_relation)"

    if mode == "p1_parity":
        py = resolver.decide(effective_scope=relation.effective_scope, **common)
        OUT["python_state"] = py.state
        OUT["python_authorized"] = bool(py.authorized)
        nat = owner.decide(effective_scope=relation.effective_scope,
                           directionality_or_symmetric=relation.directionality_or_symmetric,
                           **common)
        OUT["native_state"] = nat["state"]
        OUT["native_authorized"] = nat["authorized"]
        OUT["native_reason"] = nat["reason"]
        OUT["parity_holds"] = (OUT["python_state"] == OUT["native_state"])
    elif mode == "p1_parity_exact_key":
        # force the sealed object-key parameters: expect a crash (B2/B3), not a decision
        nat = owner.decide(effective_scope="DISTINCT_BY_DEFAULT",
                           directionality_or_symmetric="SYMMETRIC", **common)
        OUT["native_state"] = nat["state"]
        OUT["native_authorized"] = nat["authorized"]
    elif mode == "b4_replay_nonstr":
        d = owner.decide(effective_scope={}, **common)     # no candidate -> plain decision dict
        OUT["decision_state"] = d["state"]
        d["relation_kind"] = 123
        owner.validate_decision_replay(d)
        OUT["result"] = "SURVIVED"
    elif mode == "t1_attacker_tcb":
        class R2:
            def __init__(self, oid):
                self.kind, self.object_id, self.content_hash = "SourceUniverse", oid, "a" * 64
            @property
            def key(self):
                return f"{self.kind}|{self.object_id}|{self.content_hash}"
            def as_dict(self):
                return {"kind": self.kind, "object_id": self.object_id,
                        "content_hash": self.content_hash}
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
            trusted_semantic_hash=(lambda v: hashlib.sha256(repr(v).encode()).hexdigest()),
            trusted_canonicalize=(lambda v: v),
            trusted_require_positive_authority=(lambda a, b: True),
            relation_class=AttackRel, authority_snapshot_class=AttackSnap)
        OUT["sealed"] = o.sealed
        OUT["counts"] = o.counts
        OUT["custody_hash_len"] = len(o.custody_hash)
        OUT["trusted_seam_identity_visible"] = o.trusted_seam
        try:
            got = o.resolve_exact(AttackRel.ref)
            OUT["resolve_exact_returned"] = type(got).__name__
        except Exception as exc:  # noqa: BLE001
            OUT["resolve_exact_refused"] = f"{type(exc).__name__}: {str(exc)[:80]}"
        OUT["attacker_classes_and_callables_accepted"] = True
    else:
        OUT["result"] = "UNKNOWN_MODE"
    print("HQ247JSON " + json.dumps(OUT, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
