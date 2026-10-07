"""Prove the victim's post-attack OWNER DECISION carries the SOURCE custody hash."""
import json, sys, weakref
sys.path.insert(0, ".")
from rawlsing_next.tests import test_pre553_temporal_comparability as T
import rawlsing_next.pre553_source_relations as sr

source, relation = T._adjudicated_resolver(universe_refs=(T.UNIVERSE_A, T.UNIVERSE_B))
victim = sr.SourceRelationResolver(relations=(), authority_registry=source._registry)

loader = next(c.cell_contents for c in (sr.authenticated_source_relation_decision.__closure__ or ())
              if callable(c.cell_contents) and getattr(c.cell_contents, "__name__", "") == "_state_or_refuse")
cell = next(c for c in (loader.__closure__ or ())
            if isinstance(c.cell_contents, tuple) and any(o() is victim for o, _ in c.cell_contents))
ss, vs = loader(source), loader(victim)

def decide(res):
    return res.decide(
        relation_kind="SOURCE_SEMANTIC_EQUIVALENCE",
        source_universe_refs=(T.UNIVERSE_A, T.UNIVERSE_B),
        operation_scope="EXACT_BOUND_UNIVERSE_PAIR",
        target_use=T._ref("TargetUsePermission", "USE-1").object_id,
        effective_scope="EXACT_BOUND_UNIVERSE_PAIR",
        directionality_or_symmetric="SYMMETRIC",
        relation_ref=relation.ref,
    )

def safe(res):
    try:
        d = decide(res)
        return {"state": d.state, "custody_hash": d.owner_custody_hash}
    except Exception as exc:
        return {"refused": f"{type(exc).__name__}: {str(exc)[:90]}"}

before = {"source_decision": safe(source), "victim_decision": safe(victim),
          "source_hash": ss.custody_hash, "victim_hash": vs.custody_hash}

forged = sr._AuthenticatedResolverState(
    owner_ref=weakref.ref(victim), by_ref=ss.by_ref, by_key=ss.by_key,
    authority_snapshots=ss.authority_snapshots, relation_semantic_hashes=ss.relation_semantic_hashes,
    authority_semantic_hashes=ss.authority_semantic_hashes, custody_hash=ss.custody_hash)
cell.cell_contents = tuple((o, forged if o() is victim else s) for o, s in cell.cell_contents)

d_src, d_vic = decide(source), decide(victim)
after = {
    "source_decision_state": d_src.state, "victim_decision_state": d_vic.state,
    "source_decision_custody_hash": d_src.owner_custody_hash,
    "victim_decision_custody_hash": d_vic.owner_custody_hash,
    "victim_decision_carries_source_custody_hash": d_vic.owner_custody_hash == d_src.owner_custody_hash,
    "victim_decision_relation_ref": d_vic.relation_ref.object_id if d_vic.relation_ref else None,
    "source_relation_ref": relation.ref.object_id,
    "victim_decision_binds_source_relation": bool(d_vic.relation_ref) and d_vic.relation_ref.key == relation.ref.key,
    "victim_decision_authorized": d_vic.authorized,
    "victim_receipt": T._run(T._cross_universe_request(victim, relation.ref)).relation_state,
}
print(json.dumps({"before": before, "after": after}, indent=1, default=str))
