"""HQ232/HQ234 F7-RR-04G hostile reproduction.

Target: F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE

Attack shape (per the HQ234 ratified supplemental lead):
  1. source resolver A legitimately constructed with positive authorized relation custody;
  2. victim resolver B constructed WITHOUT that relation, same registry;
  3. recover _state_or_refuse through authenticated_source_relation_decision.__closure__;
  4. recover the exact closure cell in loader.__closure__ whose cell_contents is the lexical
     `entries` tuple;
  5. obtain source_state and victim_state;
  6. construct a state carrying SOURCE custody material but bound to victim_state.owner_ref;
  7. rebind entries_cell.cell_contents so victim maps to that forged state;
  8. invoke the normal authenticated F7 path for victim.

Read-only with respect to the repository. Mutates only in-process closure state, which is
the attack itself.
"""
from __future__ import annotations

import json
import sys
import weakref

sys.path.insert(0, ".")

from rawlsing_next.tests import test_pre553_temporal_comparability as T
import rawlsing_next.pre553_source_relations as sr

OUT = {}


def run_victim(victim, relation_ref):
    """The normal authenticated F7 path for the victim."""
    return T._run(T._cross_universe_request(victim, relation_ref))


def describe(receipt):
    return {
        "relation_state": receipt.relation_state,
        "relation_state_reason": receipt.relation_state_reason,
        "comparability_status": receipt.comparability_status,
        "direction_claim": getattr(receipt, "direction_claim", None),
    }


# ---------------------------------------------------------------- 0. fixtures
source, relation = T._adjudicated_resolver(universe_refs=(T.UNIVERSE_A, T.UNIVERSE_B))
victim = sr.SourceRelationResolver(relations=(), authority_registry=source._registry)
OUT["fixtures"] = {
    "source_is_exact_resolver": type(source) is sr.SourceRelationResolver,
    "victim_is_exact_resolver": type(victim) is sr.SourceRelationResolver,
    "relation_ref": relation.ref.object_id,
    "same_registry": victim._registry is source._registry,
}

# ---------------------------------------------------------------- 1. baseline
base_source = describe(run_victim(source, relation.ref))
base_victim = describe(run_victim(victim, relation.ref))
OUT["baseline"] = {"source": base_source, "victim": base_victim}
assert base_source["relation_state"] == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED", base_source
assert base_victim["relation_state"] == "TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT", base_victim

# ---------------------------------------------------------------- 2. reflection recovery
loader = next(
    cell.cell_contents
    for cell in (sr.authenticated_source_relation_decision.__closure__ or ())
    if callable(cell.cell_contents)
    and getattr(cell.cell_contents, "__name__", "") == "_state_or_refuse"
)
OUT["reflection"] = {"loader_recovered": loader.__name__}

source_state = loader(source)
victim_state = loader(victim)
OUT["reflection"]["source_state_owner_is_source"] = source_state.owner_ref() is source
OUT["reflection"]["victim_state_owner_is_victim"] = victim_state.owner_ref() is victim
OUT["reflection"]["source_state_custody_hash"] = source_state.custody_hash
OUT["reflection"]["victim_state_custody_hash"] = victim_state.custody_hash
OUT["reflection"]["source_by_ref_entries"] = len(source_state.by_ref)
OUT["reflection"]["victim_by_ref_entries"] = len(victim_state.by_ref)

# the lexical ledger cell
ledger_cell = next(
    cell
    for cell in (loader.__closure__ or ())
    if isinstance(cell.cell_contents, tuple)
    and any(owner_ref() is victim for owner_ref, _ in cell.cell_contents)
)
ledger_before = ledger_cell.cell_contents
OUT["reflection"]["ledger_cell_found"] = True
OUT["reflection"]["ledger_len_before"] = len(ledger_before)
OUT["reflection"]["ledger_has_source"] = any(o() is source for o, _ in ledger_before)
OUT["reflection"]["ledger_has_victim"] = any(o() is victim for o, _ in ledger_before)

# ---------------------------------------------------------------- 3. step 6: forge the state
#   carry SOURCE custody material, bind owner_ref to the VICTIM.
forged_state = sr._AuthenticatedResolverState(
    owner_ref=weakref.ref(victim),
    by_ref=source_state.by_ref,
    by_key=source_state.by_key,
    authority_snapshots=source_state.authority_snapshots,
    relation_semantic_hashes=source_state.relation_semantic_hashes,
    authority_semantic_hashes=source_state.authority_semantic_hashes,
    custody_hash=source_state.custody_hash,
)
OUT["forge"] = {
    "forged_owner_is_victim": forged_state.owner_ref() is victim,
    "forged_by_ref_is_source_by_ref": forged_state.by_ref is source_state.by_ref,
    "forged_custody_hash_is_source_hash": forged_state.custody_hash == source_state.custody_hash,
    "forged_is_namedtuple": type(forged_state).__name__,
}

# ---------------------------------------------------------------- 4. step 7: rebind the cell
entries_rebound = []
for owner_ref, state in ledger_before:
    if owner_ref() is victim:
        entries_rebound.append((weakref.ref(victim), forged_state))
    else:
        entries_rebound.append((owner_ref, state))
rebound_tuple = tuple(entries_rebound)

try:
    ledger_cell.cell_contents = rebound_tuple
    OUT["rebind"] = {"succeeded": True, "ledger_len_after": len(ledger_cell.cell_contents)}
except Exception as exc:
    OUT["rebind"] = {"succeeded": False, "error": f"{type(exc).__name__}: {exc}"}

# confirm the loader now returns the forged state for the victim
try:
    now_state = loader(victim)
    OUT["rebind"]["loader_returns_forged_for_victim"] = now_state is forged_state
    OUT["rebind"]["loader_returned_custody_hash"] = now_state.custody_hash
except Exception as exc:
    OUT["rebind"]["loader_returns_forged_for_victim"] = f"RAISED {type(exc).__name__}: {exc}"

# ---------------------------------------------------------------- 5. step 8: normal path
try:
    attack_receipt = run_victim(victim, relation.ref)
    OUT["attack"] = describe(attack_receipt)
    OUT["attack"]["victim_became_positive"] = (
        attack_receipt.relation_state == "TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED"
    )
    OUT["attack"]["reason"] = attack_receipt.relation_state_reason
except Exception as exc:
    OUT["attack"] = {
        "raised": f"{type(exc).__name__}: {exc}",
        "victim_became_positive": False,
    }

OUT["verdict"] = (
    "REPRODUCED__F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE"
    if OUT.get("attack", {}).get("victim_became_positive")
    else "NOT_REPRODUCED"
)

print(json.dumps(OUT, indent=1, default=str))
