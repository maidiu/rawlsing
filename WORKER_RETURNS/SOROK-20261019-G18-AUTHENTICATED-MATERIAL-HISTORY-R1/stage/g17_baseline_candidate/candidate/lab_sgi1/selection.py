"""Governed simulation-selection policy with full ADP020-style receipts.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
Distinctly recorded: hard feasibility | synthetic support | model plausibility |
simulation-selection weights. No verbal ranking becomes a fake frequency.
No unreported redraws. Scope hash never contains future-child material.

G13 REPAIR (defect family 6 -- selector integrity).

The pre-repair ``class_set_hash`` hashed only ``(class_key, representative_id)``.
A candidate whose substantive payload was mutated after deduplication therefore
kept an identical selection identity and an identical replay hash: "same ID,
changed payload" could masquerade as the same candidate. ADP-020 s10 requires an
immutable ``candidate_replay_hash`` per entry precisely to forbid that.

The repaired selector recomputes every candidate's authoritative replay hash from
its ACTUAL content and binds those hashes into the canonical candidate set, so a
stale class identity can no longer preserve selection authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .core import h_obj, h_concat, typed, S, ScopedRNG, Ledger, RngAuthorityError, canon

DECISION_KIND = "CONCEPTION_SCENARIO_SELECTION"
DECISION_SEMANTICS_VERSION = "SELECTION_DECISION_SEMANTICS@2.0-G15"
STREAM = "v3.causal.adp015.conception_scenario_selection"

# Keys that constitute the class IDENTITY itself. Everything else in a candidate
# entry is substantive payload and is bound by its replay hash.
_CLASS_IDENTITY_KEYS = frozenset({"class_key", "representative_id"})

# Deduplication bookkeeping about HOW MANY paraphrases collapsed into a class.
# This is not candidate content: N phrasings of one scenario must not change the
# candidate's replay identity (the original dedup contract, and ADP-020's
# "phrasing multiplicity cannot alter the class set"). It is receipted in
# `merge_receipts` / `class_member_index` instead.
_MULTIPLICITY_KEYS = frozenset({"member_ids", "member_count", "raw_proposals", "raw_admission_findings"})

ADP020_CANDIDATE_SET_PREFIX = "ADP020_CANDIDATE_SET_V1\x00"

POLICIES = {
    "SIM_UNIFORM_CLASSES": {
        "method": "UNIFORM_CANDIDATE",
        "integer_weight_units": None,
        "status": "SIMULATION_POLICY",
        "no_claim_of_population_frequency_IF_SIMULATION": True,
    },
    "SIM_INTEGER_WEIGHT_A": {
        "method": "WEIGHTED_CANDIDATE_INTEGER",
        "integer_weight_units": [3, 2, 1, 1, 1, 1],
        "status": "SIMULATION_POLICY",
        "no_claim_of_population_frequency_IF_SIMULATION": True,
    },
    "SIM_INTEGER_WEIGHT_B": {
        "method": "WEIGHTED_CANDIDATE_INTEGER",
        "integer_weight_units": [1, 1, 3, 2, 1, 1],
        "status": "SIMULATION_POLICY",
        "no_claim_of_population_frequency_IF_SIMULATION": True,
    },
}


def policy_hash(policy_name: str) -> str:
    return h_obj({"policy": policy_name, "def": POLICIES[policy_name]})


def scope_hash(causal_run_id: str, mother_anchor_hash: str, target_hash: str,
               grammar_version: str, anchor_event_index: int = -1,
               anchor_event_id: Optional[str] = None) -> str:
    """Scope binds run+anchor+target+grammar+decision semantics ONLY.

    NEVER child outcome, mutable model wording, or transient loop count.
    """
    from .core import register_research_scope
    record=dict(causal_run_id=causal_run_id,mother_anchor_hash=mother_anchor_hash,target_hash=target_hash,
        grammar_version=grammar_version,decision_semantics_version=DECISION_SEMANTICS_VERSION,
        source_authority='G15_SOURCEFREE_RESEARCH_ONLY',anchor_event_index=anchor_event_index,
        anchor_event_id_or_init_checkpoint_hash=anchor_event_id or 'INIT:'+mother_anchor_hash,
        rule_invocation_id='G15_FINITE_SELECTION:'+h_obj(dict(run=causal_run_id,checkpoint=mother_anchor_hash,target=target_hash)))
    return register_research_scope(h_obj(record),record)



def _weights_for(policy_name: str, n_classes: int) -> List[int]:
    p = POLICIES[policy_name]
    if p["method"] == "UNIFORM_CANDIDATE":
        return [1] * n_classes
    units = p["integer_weight_units"]
    if len(units) >= n_classes:
        return units[:n_classes]
    return units + [1] * (n_classes - len(units))


def candidate_replay_hash(entry: Dict[str, Any]) -> str:
    """ADP-020 s10 immutable per-candidate replay hash over ACTUAL content.

    Binds the substantive payload of the candidate entry, not merely its class
    identity, so a mutated payload cannot retain a stale class identity.

    Dedup multiplicity (``member_ids``/``member_count``) is deliberately NOT
    bound: how many paraphrases collapsed into a class is not candidate content,
    and binding it would let phrasing count alter the replay identity.
    """
    payload = {k: v for k, v in entry.items()
               if k not in _CLASS_IDENTITY_KEYS and k not in _MULTIPLICITY_KEYS}
    from .membrane import semantic_candidate
    if isinstance(payload.get("candidate"),dict):
        payload["candidate"] = semantic_candidate(payload["candidate"])
    return h_obj({
        "candidate_id": entry.get("class_key"),
        "representative_id": entry.get("representative_id"),
        "bound_payload_keys": sorted(payload),
        "bound_payload": payload,
    })


def candidate_set_hash(ordered: List[Dict[str, Any]], weights: List[int],
                       policy_name: str) -> str:
    """ADP-020 s10.2 canonical candidate-set hash binding replay hashes."""
    entries = [
        {
            "candidate_id": e.get("class_key"),
            "representative_id": e.get("representative_id"),
            "candidate_replay_hash": candidate_replay_hash(e),
            "weight_units": w,
        }
        for e, w in zip(ordered, weights)
    ]
    entries.sort(key=lambda x: (str(x["candidate_id"]),
                                x["candidate_replay_hash"]))
    canonical = canon({
        "identity_mode": "SET_CANONICAL",
        "candidate_owner_authority": "SOROK_SOURCEFREE_GENEALOGY_LAB",
        "policy_name": policy_name,
        "entries": entries,
    })
    import hashlib as _h
    return "sha256:" + _h.sha256(
        ADP020_CANDIDATE_SET_PREFIX.encode("utf-8") + canonical
    ).hexdigest()


def adp020_select(policy_name: str, eligible_classes: List[Dict[str, Any]],
                  root_seed: str, scope: str, occurrence_index: int = 0,
                  force_index: Optional[int] = None,
                  upstream_class_set_hash: Optional[str] = None) -> Dict[str, Any]:
    """Deterministic selection over canonical class order.

    Deterministic singleton consumes ZERO draws. Every draw is receipted.
    force_index is used ONLY by explicitly-declared counterfactual test hooks
    (e.g. RETRY-BIAS forced-C1) and is recorded in the receipt as a declared
    intervention, never a silent redraw.

    G13 repair: a malformed root seed is refused with a typed RNG failure BEFORE
    any draw, and the candidate-set hash binds actual candidate payload.
    """
    if not isinstance(policy_name,str) or policy_name not in POLICIES:
        return typed(S.SELECTION_AUTHORITY_UNBOUND,
                     reason="policy not registered", policy=policy_name)
    if not isinstance(eligible_classes,list) or any(not isinstance(c,dict) for c in eligible_classes):
        return typed(S.NOT_EXECUTED_AUTHORITY_HOLD,reason='UNCLASSIFIED_CANDIDATE_CONTAINER',n_draws=0)
    if not eligible_classes:
        return typed(S.SCENARIOS_VALID_EMPTY,
                     reason="no eligible classes; zero draws", n_draws=0)

    import unicodedata
    from .membrane import output_findings, leak_paths
    ids=[unicodedata.normalize("NFC",str(c.get("class_key",""))) for c in eligible_classes]
    rep_ids=[unicodedata.normalize("NFC",str(c.get("representative_id",""))) for c in eligible_classes]
    if not all(ids) or not all(rep_ids) or len(ids)!=len(set(ids)) or len(rep_ids)!=len(set(rep_ids)):
        return typed(S.DEDUP_UNDERDETERMINED,reason="DUPLICATE_OR_MISSING_CLASS_OR_REPRESENTATIVE_ID",n_draws=0)
    for entry in eligible_classes:
        findings=output_findings(entry["candidate"]) if isinstance(entry.get("candidate"),dict) else leak_paths(entry)
        if 'candidate' not in entry:
            allowed={'class_key','representative_id','payload','member_ids','member_count'}
            if set(entry)-allowed or not isinstance(entry.get('class_key'),str) or entry.get('class_key') not in {'A','B','C1','C2'} or not isinstance(entry.get('representative_id'),str) or entry.get('representative_id') not in {'A','B','R1','R2','RA','RB'}:
                findings+=['UNREGISTERED_DIAGNOSTIC_ENVELOPE']
            if 'payload' in entry and (not isinstance(entry['payload'],str) or entry['payload'] not in {'ORIGINAL','OTHER','CHANGED','MUTATED','X','Y','1','2','MUTATED_HISTORY_REQUIREMENT'}):
                findings+=['UNCLASSIFIED_DIAGNOSTIC_PAYLOAD']
        for raw in entry.get('raw_proposals',[]):findings+=output_findings(raw)
        if findings or entry.get("raw_admission_findings"):
            diagnostic_order=sorted(eligible_classes,key=lambda e:str(e.get('class_key')))
            return typed(S.NOT_EXECUTED_AUTHORITY_HOLD,reason="OUTPUT_MEMBRANE_HOLD",findings=findings,n_draws=0,
                candidate_set_hash=candidate_set_hash(diagnostic_order,_weights_for(policy_name,len(diagnostic_order)),policy_name),
                diagnostic_hash_only_no_selection=True)
    ordered = sorted(eligible_classes, key=lambda c: unicodedata.normalize("NFC",c["class_key"]).encode("utf-8"))
    n = len(ordered)
    weights = _weights_for(policy_name, n)
    total = sum(weights)
    class_set_hash = candidate_set_hash(ordered, weights, policy_name)
    replay_hashes = {e["class_key"]: candidate_replay_hash(e) for e in ordered}

    try:
        rng = ScopedRNG(root_seed, STREAM, scope)
        # Classify eagerly inside the guard: an unlawful root is refused here,
        # BEFORE any draw and BEFORE any selection identity is published.
        rng.classification
    except RngAuthorityError as exc:
        return typed(
            S.NOT_EXECUTED_AUTHORITY_HOLD,
            reason="root seed metadata unlawful; no draw consumed",
            rng_failure_code=exc.code,
            rng_failure_detail=exc.detail,
            n_draws=0,
            unreported_redraws=0,
            status_is_HOLD_not_INFEASIBLE=True,
        )

    ledger: Dict[str, Any] = {
        "decision_kind": DECISION_KIND,
        "decision_semantics_version": DECISION_SEMANTICS_VERSION,
        "stream": STREAM,
        "scope_hash": scope,
        "root_seed": root_seed,
        "root_seed_provenance": rng.classification["root_seed_provenance"],
        "adp020_entitlement": rng.classification["adp020_entitlement"],
        "adp020_hold": rng.classification.get("hold"),
        "sampler": (rng.draws[0].sampler if rng.draws else None),
        "policy_name": policy_name,
        "policy_hash": policy_hash(policy_name),
        "policy_status": POLICIES[policy_name]["status"],
        "no_population_frequency_claim": True,
        "candidate_set_hash": class_set_hash,
        "candidate_set_hash_binds_payload": True,
        "candidate_replay_hashes": replay_hashes,
        "upstream_class_set_hash": upstream_class_set_hash,
        "canonical_class_order": [c["class_key"] for c in ordered],
        "eligible_set": [c["representative_id"] for c in ordered],
        "class_weights": [
            {"class_key": c["class_key"], "weight_units": w}
            for c, w in zip(ordered, weights)
        ],
        "total_weight_units": total,
        "occurrence_index": occurrence_index,
    }

    if n == 1 and force_index is None:
        ledger["draw"] = None
        ledger["draw_receipts"] = []
        ledger["n_draws"] = 0
        ledger["draw_mode"] = "DETERMINISTIC_SINGLETON_ZERO_DRAWS"
        chosen = ordered[0]
        ledger["selected_class_key"] = chosen["class_key"]
        ledger["selected_representative_id"] = chosen["representative_id"]
        ledger["status"] = S.COMMITTED
        ledger["unreported_redraws"] = 0
        return _seal_decision(ledger, rng, ordered)

    if force_index is not None:
        chosen = ordered[force_index % n]
        ledger["draw"] = None
        ledger["draw_receipts"] = []
        ledger["n_draws"] = 0
        ledger["draw_mode"] = "DECLARED_TEST_INTERVENTION_FORCE_INDEX"
        ledger["declared_intervention"] = {"force_index": force_index}
        ledger["selected_class_key"] = chosen["class_key"]
        ledger["selected_representative_id"] = chosen["representative_id"]
        ledger["status"] = S.COMMITTED
        ledger["unreported_redraws"] = 0
        ledger["bias_note"] = (
            "declared counterfactual hook; NOT a stochastic draw; "
            "excluded from empirical acceptance-rate accounting"
        )
        return _seal_decision(ledger, rng, ordered)

    rec = rng.draw(total, "conception_scenario_selection", class_set_hash,
                   occurrence_index)
    acc = 0
    chosen = ordered[-1]
    for c, w in zip(ordered, weights):
        acc += w
        if rec.draw_value < acc:
            chosen = c
            break
    ledger["draw"] = rec.as_dict()
    ledger["draw_receipts"] = [r.as_dict() for r in rng.draws]
    ledger["n_draws"] = rng.draw_count
    ledger["draw_mode"] = "SCOPED_DETERMINISTIC_STREAM"
    ledger["selected_class_key"] = chosen["class_key"]
    ledger["selected_representative_id"] = chosen["representative_id"]
    ledger["status"] = S.COMMITTED
    ledger["unreported_redraws"] = 0
    return _seal_decision(ledger, rng, ordered)


LAB_RULE_REGISTRATION = {
 "semantic_rule_id":"G15_SOURCEFREE_FINITE_SELECTION",
 "semantic_rule_version":"1.0.0",
 "issuing_scope":"WORKER_RESEARCH_ONLY",
 "native_semantic_grant":"NOT_GRANTED",
 "stream":STREAM,
 "operations":["UNIFORM_CANDIDATE","WEIGHTED_CANDIDATE_INTEGER"],
 "policies":POLICIES,
}

def _seal_decision(ledger,rng,ordered):
    lineage=rng.lineage_receipt()
    parameters=dict(operation=POLICIES[ledger['policy_name']]['method'],class_weights=ledger['class_weights'])
    selected=next(e for e in ordered if e['class_key']==ledger['selected_class_key'])
    ledger.update(semantic_rule_id=LAB_RULE_REGISTRATION['semantic_rule_id'],
        semantic_rule_version=LAB_RULE_REGISTRATION['semantic_rule_version'],
        semantic_rule_registry_hash=h_obj(LAB_RULE_REGISTRATION),
        semantic_rule_registration=LAB_RULE_REGISTRATION,
        stochastic_parameters_hash=h_obj(parameters),stochastic_parameters=parameters,
        causal_run_id=lineage['scope_registration'].get('source_record',{}).get('causal_run_id',ledger['scope_hash']),lineage=lineage,
        candidate_set_record=ordered,draw_consumed=bool(ledger['n_draws']),
        selected_candidate_replay_hash=candidate_replay_hash(selected),
        result_v3_event_id=None,result_v3_event_index=None,
        native_semantic_grant='NOT_GRANTED')
    coordinates=[x.get('entropy_coordinate') for x in ledger['draw_receipts']]
    actual_coordinate=rng.entropy_coordinate('conception_scenario_selection',ledger['occurrence_index'],0,0,ledger['total_weight_units'])
    ledger['decision_coordinate']={k:v for k,v in actual_coordinate.items() if k not in {'draw_index','uniform_below_n','block_index'}}
    ledger['coordinate_profile']='G15_EXACT_HISTORY_CUT_RESEARCH_ONLY' if 'source_record' in lineage['scope_registration'] else 'G14_FROZEN_DIAGNOSTIC_NOT_NATIVE_ANCHOR'
    identity={k:ledger[k] for k in ['decision_semantics_version','semantic_rule_id','semantic_rule_version',
        'semantic_rule_registry_hash','stochastic_parameters_hash','candidate_set_hash','lineage','decision_coordinate',
        'draw_mode','selected_class_key','selected_candidate_replay_hash','causal_run_id']}
    identity['entropy_coordinates']=coordinates
    identity['draw_replay_hashes']=[r.get('draw_replay_hash') for r in ledger['draw_receipts']]
    identity['declared_intervention']=ledger.get('declared_intervention')
    ledger['decision_replay_identity_hash']=h_obj(identity)
    ledger['raw_proposal_record_hashes']=[h_obj(raw) for e in ordered for raw in e.get('raw_proposals',[])]
    ledger['exact_candidate_packet_hash']=h_obj(ordered)
    ledger['decision_receipt_id']=h_obj(dict(replay_identity=identity,draws=ledger['draw_receipts'],exact_candidate_packet_hash=ledger['exact_candidate_packet_hash']))
    ledger['decision_replay_preimage']=identity
    return ledger


def replay_decision(receipt):
    """Recompute raw entropy, choice and complete custody from persisted inputs."""
    try:
        from .core import register_research_scope
        reg=receipt['lineage']['scope_registration']
        if 'source_record' in reg:register_research_scope(receipt['scope_hash'],reg['source_record'])
        result=adp020_select(receipt['policy_name'],receipt['candidate_set_record'],receipt['root_seed'],
            receipt['scope_hash'],receipt['occurrence_index'],
            force_index=(receipt.get('declared_intervention') or {}).get('force_index'),
            upstream_class_set_hash=receipt.get('upstream_class_set_hash'))
    except (KeyError,TypeError,ValueError):
        return typed(S.EXACT_REPLAY_DIVERGENCE,reason='INCOMPLETE_DECISION_RECEIPT')
    return typed('EXACT_REPLAY' if result==receipt else S.EXACT_REPLAY_DIVERGENCE,
                 recomputed=result,full_receipt_equal=result==receipt)


class DecisionJournal:
    """Persistent research coordinate-use index; hashes never self-grant authority."""
    def __init__(self,records=None):
        from copy import deepcopy
        self.records={} if records is None else deepcopy(records)
    def record(self,receipt):
        verified=replay_decision(receipt)
        if verified['status']!='EXACT_REPLAY':return verified
        key=h_obj(receipt['decision_coordinate'])
        if key in self.records:
            if self.records[key]!=receipt:
                return typed('RNG_DRAW_COORDINATE_REUSE_CONFLICT',n_draws=0)
            return typed('IDEMPOTENT_REPLAY',receipt=__import__('copy').deepcopy(self.records[key]))
        self.records[key]=__import__('copy').deepcopy(receipt)
        return typed('RECORDED_RESEARCH_ONLY',receipt=__import__('copy').deepcopy(receipt))
