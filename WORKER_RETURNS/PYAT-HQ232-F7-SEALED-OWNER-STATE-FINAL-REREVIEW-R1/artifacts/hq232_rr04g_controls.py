"""HQ232 F7-RR-04G controls: isolate what is load-bearing and rule out confounds."""
from __future__ import annotations

import json
import sys
import weakref

sys.path.insert(0, ".")

from rawlsing_next.tests import test_pre553_temporal_comparability as T
import rawlsing_next.pre553_source_relations as sr

OUT = {}


def path(victim, relation_ref):
    r = T._run(T._cross_universe_request(victim, relation_ref))
    return {"state": r.relation_state, "reason": r.relation_state_reason}


def fresh_pair():
    source, relation = T._adjudicated_resolver(universe_refs=(T.UNIVERSE_A, T.UNIVERSE_B))
    victim = sr.SourceRelationResolver(relations=(), authority_registry=source._registry)
    return source, relation, victim


def loader_of():
    return next(
        cell.cell_contents
        for cell in (sr.authenticated_source_relation_decision.__closure__ or ())
        if callable(cell.cell_contents)
        and getattr(cell.cell_contents, "__name__", "") == "_state_or_refuse"
    )


def ledger_cell_of(loader, victim):
    return next(
        cell for cell in (loader.__closure__ or ())
        if isinstance(cell.cell_contents, tuple)
        and any(o() is victim for o, _ in cell.cell_contents)
    )


def forge(source_state, victim):
    return sr._AuthenticatedResolverState(
        owner_ref=weakref.ref(victim),
        by_ref=source_state.by_ref, by_key=source_state.by_key,
        authority_snapshots=source_state.authority_snapshots,
        relation_semantic_hashes=source_state.relation_semantic_hashes,
        authority_semantic_hashes=source_state.authority_semantic_hashes,
        custody_hash=source_state.custody_hash,
    )


# ---------------------------------------------------------------- C1: confound check
# Is direct construction of _AuthenticatedResolverState ALONE enough, with no ledger
# rebinding and no monkeypatching? (i.e. is the forged state reachable by the victim
# through any already-caller-reachable path?)
source, relation, victim = fresh_pair()
loader = loader_of()
source_state = loader(source)
forged = forge(source_state, victim)
OUT["C1_direct_construction_alone_is_insufficient"] = {
    "forged_constructible_by_caller": True,
    "victim_state_before": loader(victim).custody_hash == source_state.custody_hash,
    "victim_positive_before_rebind": path(victim, relation.ref)["state"],
    "note": "constructing the forged state does not by itself expose it to the victim; the loader still "
            "returns the victim's own nonpositive state until the ledger binding is changed",
}

# ---------------------------------------------------------------- C2: minimal local rebind
# Replace ONLY the second element of the victim's ledger entry (the state) rather than
# rebuilding the whole tuple. Same-model primitive, smaller footprint than the lead's step 7.
source2, relation2, victim2 = fresh_pair()
loader2 = loader_of()
cell2 = ledger_cell_of(loader2, victim2)
source_state2 = loader2(source2)
entries = list(cell2.cell_contents)
for i, (o, s) in enumerate(entries):
    if o() is victim2:
        entries[i] = (o, forge(source_state2, victim2))
cell2.cell_contents = tuple(entries)
OUT["C2_minimal_local_rebind"] = {
    "result": path(victim2, relation2.ref),
    "note": "only the victim's own ledger entry state was replaced; the tuple rebuild uses the same "
            "cell rebinding primitive",
}

# ---------------------------------------------------------------- C3: namedtuple _replace confound
# Does a caller even need cell rebinding, or can the ledger be swapped via a shape-only rebuild?
source3, relation3, victim3 = fresh_pair()
loader3 = loader_of()
cell3 = ledger_cell_of(loader3, victim3)
source_state3 = loader3(source3)
entries3 = cell3.cell_contents
rebuilt = tuple((o, forge(source_state3, victim3) if o() is victim3 else s) for o, s in entries3)
cell3.cell_contents = rebuilt
OUT["C3_tuple_item_assignment_still_refused"] = {
    "tuple_item_assignment_raises": None,
    "note": "the original court proved ledger[0] = ledger[-1] raises TypeError; that remains true. The "
            "defeat is not tuple mutability - it is rebinding the CELL that holds the tuple.",
}
try:
    entries3[0] = entries3[-1]
    OUT["C3_tuple_item_assignment_still_refused"]["tuple_item_assignment_raises"] = False
except TypeError:
    OUT["C3_tuple_item_assignment_still_refused"]["tuple_item_assignment_raises"] = True

# ---------------------------------------------------------------- C4: does the custody hash bind owner?
# The forged state carries the SOURCE's custody_hash while being bound to the victim. Is that
# hash ever re-derived from, or checked against, the owning resolver?
source4, relation4, victim4 = fresh_pair()
loader4 = loader_of()
cell4 = ledger_cell_of(loader4, victim4)
ss4 = loader4(source4)
vs4 = loader4(victim4)
forged4 = forge(ss4, victim4)
cell4.cell_contents = tuple((o, forged4 if o() is victim4 else s) for o, s in cell4.cell_contents)
r4 = T._run(T._cross_universe_request(victim4, relation4.ref))
OUT["C4_custody_hash_not_owner_bound"] = {
    "source_custody_hash": ss4.custody_hash,
    "victim_original_custody_hash": vs4.custody_hash,
    "victim_receipt_owner_custody_hash": getattr(r4, "owner_custody_hash", None),
    "receipt_carries_source_hash": getattr(r4, "owner_custody_hash", None) == ss4.custody_hash,
    "hashes_differ": ss4.custody_hash != vs4.custody_hash,
    "note": "the victim's positive receipt carries the SOURCE's custody hash. No code path re-derives "
            "the custody hash from the resolver that actually owns the state, so the hash is not an "
            "owner-binding invariant - it is a transcription.",
    "receipt_state": r4.relation_state,
}

# ---------------------------------------------------------------- C5: sealer is not load-bearing
# The lead's step 7 bypasses _seal entirely. Confirm the single-assignment sealer guard is
# therefore irrelevant to the reachable attack.
source5, relation5, victim5 = fresh_pair()
loader5 = loader_of()
cell5 = ledger_cell_of(loader5, victim5)
ss5 = loader5(source5)
cell5.cell_contents = tuple((o, forge(ss5, victim5) if o() is victim5 else s) for o, s in cell5.cell_contents)
OUT["C5_sealer_irrelevant_to_this_route"] = {
    "result": path(victim5, relation5.ref),
    "note": "the attack never calls _seal; the 'owner custody already sealed' guard is not on the "
            "reachable path because the ledger cell is rebound directly",
}

print(json.dumps(OUT, indent=1, default=str))
