"""Bounded reproduction: B4 malformed replay/request input must be typed, never a crash."""
import os
import sys

sys.path.insert(0, os.environ["HQ_WT"])
import rawlsing_next._p07_native_owner_stage_b as M
from rawlsing_next.tests.test_pre553_temporal_comparability import (
    _adjudicated_resolver, UNIVERSE_A, UNIVERSE_B)
from rawlsing_next.pre553_source_relations import semantic_hash
from rawlsing_next.pre553_empirical_objects import (
    canonicalize, SourceUniverseRelation, AuthoritySnapshot)
from rawlsing_next.pre553_empirical_authority import require_positive_authority

r, rel = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
o = M.StageBOwner(relations=[rel], authority_snapshots=list(r._registry._by_key.values()),
                  trusted_semantic_hash=semantic_hash, trusted_canonicalize=canonicalize,
                  trusted_require_positive_authority=require_positive_authority,
                  relation_class=SourceUniverseRelation,
                  authority_snapshot_class=AuthoritySnapshot)
BAD = [None, 42, b"bytes", [], {}, 3.5, object(), True, ["k"], ("t",), 0, {"a": 1}]
crashes = 0
for bad in BAD:
    for field in ("relation_kind", "target_use"):
        kw = dict(relation_kind=rel.relation_kind,
                  source_universe_refs=list(rel.source_universe_refs),
                  operation_scope=rel.operation_scope, target_use=rel.target_use,
                  effective_scope=rel.effective_scope,
                  directionality_or_symmetric=rel.directionality_or_symmetric)
        kw[field] = bad
        try:
            o.decide(**kw)
        except Exception:
            pass
d = o.decide(relation_kind=rel.relation_kind,
             source_universe_refs=list(rel.source_universe_refs),
             operation_scope=rel.operation_scope, target_use=rel.target_use,
             effective_scope=rel.effective_scope,
             directionality_or_symmetric=rel.directionality_or_symmetric)
for field in ("relation_kind", "target_use", "state", "source_universe_refs",
              "owner_custody_hash", "authority_snapshot_content_hash"):
    for bad in BAD:
        broken = dict(d); broken[field] = bad
        try:
            o.validate_decision_replay(broken)
        except Exception:
            pass
for bad in (None, 42, "x", [], object(), 3.5):
    try:
        o.validate_decision_replay(bad)
    except Exception:
        pass
print("B4: %d malformed inputs across decide and validate_decision_replay, no crash" % (len(BAD) * 2 + len(BAD) * 6 + len(BAD)))
