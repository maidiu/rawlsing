#!/usr/bin/env python3
"""HQ236 independent reproduction / falsification of HQ235 F7 coordinated custody substitution.

Written by the HQ236 reviewer. Does NOT import or reuse the HQ235 witness helpers
(_hq235_victim_pair / _hq235_reflection_seam / any test_hq235_* body). It reuses only the
pre-existing lawful court fixtures _adjudicated_resolver / _cross_universe_request / _run,
which the diff proves are byte-unchanged by HQ235 (test file change is 309 added / 0 removed).

No production callable is monkeypatched. The "attacker" uses only:
  * instance attribute assignment on a resolver it holds,
  * closure-cell .cell_contents assignment on a ledger cell recovered by __closure__ walking,
  * direct construction of the public NamedTuple _AuthenticatedResolverState.

Run: <governed python3.11> /tmp/hq236_independent_attack.py
"""
import json
import sys

ROOT = "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq236-f7-coordinated-hostile"
sys.path.insert(0, ROOT)

import rawlsing_next.pre553_source_relations as sr  # noqa: E402
from rawlsing_next.tests import test_pre553_temporal_comparability as T  # noqa: E402

K = "SOURCE_SEMANTIC_EQUIVALENCE"
SCOPE = "EXACT_BOUND_UNIVERSE_PAIR"
OP = "SEMANTIC_EQUIVALENCE_ADMISSION"
USE = T._ref("TargetUsePermission", "USE-1").object_id


def p07(resolver, relation):
    """Exact P07 owner decision via the captured authenticated owner entrypoint."""
    try:
        d = sr.authenticated_source_relation_decision(
            resolver,
            relation_kind=K,
            source_universe_refs=(T.UNIVERSE_A, T.UNIVERSE_B),
            operation_scope=SCOPE,
            target_use=USE,
            effective_scope=SCOPE,
            relation_ref=relation.ref,
            expected_authority_operation=OP,
        )
    except Exception as exc:  # noqa: BLE001
        return {"p07": "REFUSED", "p07_exception": f"{type(exc).__name__}: {exc}"}
    return {
        "p07": d.state,
        "p07_authorized": bool(d.authorized),
        "p07_reason": d.reason,
        "p07_relation_ref": d.relation_ref.as_dict() if d.relation_ref else None,
        "p07_owner_custody_hash": d.owner_custody_hash,
        "p07_authority_snapshot_content_hash": d.authority_snapshot_content_hash,
    }


def f7(resolver, relation):
    """Exact F7 temporal decision for the cross-universe request."""
    try:
        r = T._run(T._cross_universe_request(resolver, relation.ref))
    except Exception as exc:  # noqa: BLE001
        return {"f7": "EXCEPTION", "f7_exception": f"{type(exc).__name__}: {exc}"}
    xu = (r.provenance or {}).get("cross_universe", {}) or {}
    return {
        "f7": r.relation_state,
        "f7_reason": r.relation_state_reason,
        "f7_comparability": r.comparability_status,
        "f7_direction": r.direction_claim,
        "f7_crosses_source_universes": xu.get("crosses_source_universes"),
        "f7_source_equivalence_ref": xu.get("source_equivalence_ref"),
        "f7_receipt_hash": r.receipt_hash,
    }


def probe(resolver, relation):
    return {**f7(resolver, relation), **p07(resolver, relation)}


def find_ledger_cell(victim):
    """Independent reflection: walk closures to the (owner_ref, state) ledger tuple cell."""
    decide_fn = sr.authenticated_source_relation_decision
    loader = None
    for cell in (decide_fn.__closure__ or ()):
        val = cell.cell_contents
        if callable(val) and getattr(val, "__name__", "") == "_state_or_refuse":
            loader = val
    assert loader is not None, "could not recover _state_or_refuse lexically"
    entries_cell = None
    for cell in (loader.__closure__ or ()):
        val = cell.cell_contents
        if isinstance(val, tuple) and any(ref() is victim for ref, _ in val):
            entries_cell = cell
    assert entries_cell is not None, "could not recover the ledger tuple cell"
    return loader, entries_cell, entries_cell.cell_contents


def forge_state(source_state, victim_state, *, by_ref, sealed_by_ref_owner,
                sealed_by_key_owner, fingerprint):
    return sr._AuthenticatedResolverState(
        owner_ref=victim_state.owner_ref,
        by_ref=by_ref,
        by_key=source_state.by_key,
        authority_snapshots=source_state.authority_snapshots,
        relation_semantic_hashes=source_state.relation_semantic_hashes,
        authority_semantic_hashes=source_state.authority_semantic_hashes,
        custody_hash=source_state.custody_hash,
        sealed_by_ref_owner=sealed_by_ref_owner,
        sealed_by_key_owner=sealed_by_key_owner,
        sealed_relations_fingerprint=fingerprint,
    )


def rebind(entries_cell, original, victim, replacement):
    entries_cell.cell_contents = tuple(
        (ref, replacement if ref() is victim else state) for ref, state in original
    )


out = {"script": "hq236_independent_attack", "interpreter": sys.executable}

source, relation = T._adjudicated_resolver(universe_refs=(T.UNIVERSE_A, T.UNIVERSE_B))
victim = sr.SourceRelationResolver(relations=(), authority_registry=source._registry)
loader, entries_cell, original = find_ledger_cell(victim)
source_state = loader(source)
victim_state = loader(victim)

out["victim_live_by_ref_keys"] = sorted(victim._by_ref)
out["source_live_by_ref_keys"] = sorted(source._by_ref)
out["fingerprint_victim_live"] = sr._custody_relations_fingerprint(live_by_ref=victim._by_ref)
out["fingerprint_source_live"] = sr._custody_relations_fingerprint(live_by_ref=source._by_ref)
out["source_owns_relation"] = relation.ref.as_dict()

out["control_A_source_positive"] = probe(source, relation)
out["control_B_victim_negative"] = probe(victim, relation)

# ---- Attack 1: exact HQ234/HQ232 single-cell rebind (source anchor fields) ----------
forged1 = forge_state(
    source_state, victim_state,
    by_ref=source_state.by_ref,
    sealed_by_ref_owner=source_state.sealed_by_ref_owner,
    sealed_by_key_owner=source_state.sealed_by_key_owner,
    fingerprint=source_state.sealed_relations_fingerprint,
)
rebind(entries_cell, original, victim, forged1)
out["attack1_single_cell_rebind"] = probe(victim, relation)
entries_cell.cell_contents = original
out["after_attack1_victim"] = probe(victim, relation)

# ---- Attack 2: candidate "coordinated" substitution (replace live containers) -------
victim_by_ref0, victim_by_key0 = victim._by_ref, victim._by_key
victim._by_ref = dict(source._by_ref)
victim._by_key = dict(source._by_key)
forged2 = forge_state(
    source_state, victim_state,
    by_ref=source_state.by_ref,
    sealed_by_ref_owner=victim._by_ref,
    sealed_by_key_owner=victim._by_key,
    fingerprint=sr._custody_relations_fingerprint(live_by_ref=victim._by_ref),
)
rebind(entries_cell, original, victim, forged2)
out["attack2_coordinated_container_replacement"] = probe(victim, relation)
entries_cell.cell_contents = original
victim._by_ref, victim._by_key = victim_by_ref0, victim_by_key0
out["after_attack2_victim"] = probe(victim, relation)

# ---- Attack 3 (NARROWER): no live-container replacement at all ---------------------
# Anchor fields are simply set to the victim's OWN untouched live containers, and the
# fingerprint is computed from that same untouched live container -- while the payload
# by_ref/by_key/custody_hash still come from the source.
forged3 = forge_state(
    source_state, victim_state,
    by_ref=source_state.by_ref,
    sealed_by_ref_owner=victim._by_ref,
    sealed_by_key_owner=victim._by_key,
    fingerprint=sr._custody_relations_fingerprint(live_by_ref=victim._by_ref),
)
rebind(entries_cell, original, victim, forged3)
out["attack3_payload_only_no_container_replacement"] = probe(victim, relation)
entries_cell.cell_contents = original
out["after_attack3_victim"] = probe(victim, relation)

# ---- Attack 4 (NARROWEST): also keep the victim's empty by_key payload ---------------
forged4 = sr._AuthenticatedResolverState(
    owner_ref=victim_state.owner_ref,
    by_ref=source_state.by_ref,
    by_key=victim_state.by_key,
    authority_snapshots=source_state.authority_snapshots,
    relation_semantic_hashes=source_state.relation_semantic_hashes,
    authority_semantic_hashes=source_state.authority_semantic_hashes,
    custody_hash=source_state.custody_hash,
    sealed_by_ref_owner=victim._by_ref,
    sealed_by_key_owner=victim._by_key,
    sealed_relations_fingerprint=sr._custody_relations_fingerprint(live_by_ref=victim._by_ref),
)
rebind(entries_cell, original, victim, forged4)
out["attack4_payload_by_ref_only"] = probe(victim, relation)
entries_cell.cell_contents = original

# ---- Restored positive control ------------------------------------------------------
out["restored_source_positive"] = probe(source, relation)
out["restored_victim_negative"] = probe(victim, relation)
out["ledger_restored"] = entries_cell.cell_contents == original

print(json.dumps(out, indent=2, sort_keys=True, default=str))
