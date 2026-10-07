"""HQ236 narrowest-path focus: ledger-cell rebind WITHOUT any live-container replacement."""
import json, sys
ROOT="/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq236-f7-coordinated-hostile"
sys.path.insert(0, ROOT)
import rawlsing_next.pre553_source_relations as sr
from rawlsing_next.tests import test_pre553_temporal_comparability as T

out={}
source, relation = T._adjudicated_resolver(universe_refs=(T.UNIVERSE_A, T.UNIVERSE_B))
victim = sr.SourceRelationResolver(relations=(), authority_registry=source._registry)

# independent reflection seam
loader=None
for cell in (sr.authenticated_source_relation_decision.__closure__ or ()):
    v=cell.cell_contents
    if callable(v) and getattr(v,"__name__","")=="_state_or_refuse": loader=v
entries_cell=None
for cell in (loader.__closure__ or ()):
    v=cell.cell_contents
    if isinstance(v,tuple) and any(r() is victim for r,_ in v): entries_cell=cell
original=entries_cell.cell_contents
source_state=loader(source); victim_state=loader(victim)

live_by_ref_id_before=id(victim._by_ref); live_by_key_id_before=id(victim._by_key)
out["live_by_ref_id_before"]=live_by_ref_id_before
out["live_by_key_id_before"]=live_by_key_id_before
out["live_by_ref_keys_before"]=sorted(victim._by_ref)
out["live_by_key_keys_before"]=sorted(victim._by_key)
out["live_fingerprint_before"]=sr._custody_relations_fingerprint(live_by_ref=victim._by_ref)

forged = sr._AuthenticatedResolverState(
    owner_ref=victim_state.owner_ref,
    by_ref=source_state.by_ref,          # payload from SOURCE
    by_key=victim_state.by_key,          # victim's own empty payload
    authority_snapshots=source_state.authority_snapshots,
    relation_semantic_hashes=source_state.relation_semantic_hashes,
    authority_semantic_hashes=source_state.authority_semantic_hashes,
    custody_hash=source_state.custody_hash,
    sealed_by_ref_owner=victim._by_ref,  # victim's OWN live container, untouched
    sealed_by_key_owner=victim._by_key,  # victim's OWN live container, untouched
    sealed_relations_fingerprint=sr._custody_relations_fingerprint(live_by_ref=victim._by_ref),
)
entries_cell.cell_contents = tuple((r, forged if r() is victim else s) for r,s in original)

r = T._run(T._cross_universe_request(victim, relation.ref))
out["victim_f7_state_after_forgery"]=r.relation_state
out["victim_f7_reason"]=r.relation_state_reason
out["victim_f7_direction"]=r.direction_claim
out["live_by_ref_id_after"]=id(victim._by_ref)
out["live_by_key_id_after"]=id(victim._by_key)
out["live_by_ref_keys_after"]=sorted(victim._by_ref)
out["live_by_key_keys_after"]=sorted(victim._by_key)
out["no_live_container_replaced"]=(
    id(victim._by_ref)==live_by_ref_id_before
    and id(victim._by_key)==live_by_key_id_before
    and sorted(victim._by_ref)==[] and sorted(victim._by_key)==[]
)
entries_cell.cell_contents=original
out["ledger_restored"]=entries_cell.cell_contents==original
print(json.dumps(out, indent=2, sort_keys=True))
