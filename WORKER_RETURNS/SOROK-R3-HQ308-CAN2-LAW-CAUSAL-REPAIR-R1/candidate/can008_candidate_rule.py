"""CAN2 finite synthetic CAN008 rule, never accepted owner authority.

One actor, one world cut, 1998--2000 inclusive, no counterpart/modality/effort,
numeric or stochastic inputs. Registered binding and exact module body digests
are dereferenced on every evaluation. Missing destination authority stays HOLD.
The effect grammar and adopted law are unchanged; sourcefree fixture competence
must not be promoted into production or empirical psychological validity.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .adopted_contract import (
    EFFECT_GRAMMAR, NONPOSITIVE_DECISION_STATES, NONCOLLAPSE_LAWS,
    R2_RULE_OBLIGATION_ITEMS, PINS, CAN008_R2_CONTRACT,
    AdmittedEvent,
)
from .candidate_registry_fixture import CANDIDATE_REGISTRY, CandidateRuleRegistration

RULE_ID = "CAND_R_CAN008_COUPLING_RESPONSE"
RULE_VERSION = "2.0.0-candidate"
RULE_GRAIN = "SOURCEFREE_CANDIDATE_RULE__NOT_ADOPTED__NOT_PRODUCTION"


def _sha(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass(frozen=True)
class CouplingRuleBinding:
    """§16 23-item binding. Every item must be present; omission fails closed."""
    rule_id: str
    rule_version: str
    rule_content_hash: str
    eligible_event_authority_signatures: Tuple[str, ...]
    eligible_event_roles: Tuple[str, ...]
    actor_scope: str
    temporal_scope: str
    receivability_semantics: str
    eligible_conditioning_owner_signatures: Tuple[str, ...]
    conditioning_causal_use_roles: Tuple[str, ...]
    counterpart_scoping: str
    modality_evidence_authorities: Tuple[str, ...]
    uptake_appraisal_semantics: str
    recruitment_semantics: str
    multiplicity_handling: str
    co_determination_closure: str
    prior_response_history_predicates: str
    current_condition_effort_role: str
    effect_kinds: Tuple[str, ...]
    target_authority_kind: str
    target_validation: str
    pff_current_consequence_projection: str
    valid_empty_behavior: str
    missing_deferred_ambiguous_behavior: str
    quantitative_contract: str
    adp020_binding: str
    atomic_commit_behavior: str
    provenance_replay_requirements: str
    obligation_coverage: Tuple[str, ...] = R2_RULE_OBLIGATION_ITEMS

    def validate_complete(self) -> Optional[str]:
        vals = {
            "rule_id_version_content_hash": (self.rule_id, self.rule_version, self.rule_content_hash),
            "eligible_precipitating_event_authority_signatures_and_roles":
                (self.eligible_event_authority_signatures, self.eligible_event_roles),
            "exact_actor_and_temporal_scope": (self.actor_scope, self.temporal_scope),
            "receivability_semantics": (self.receivability_semantics,),
            "eligible_conditioning_owner_signatures": (self.eligible_conditioning_owner_signatures,),
            "conditioning_causal_use_roles": (self.conditioning_causal_use_roles,),
            "counterpart_relationship_scoping": (self.counterpart_scoping,),
            "permitted_modality_evidence_authorities_and_roles": (self.modality_evidence_authorities,),
            "actor_uptake_appraisal_relation_semantics": (self.uptake_appraisal_semantics,),
            "situated_recruitment_relation_semantics": (self.recruitment_semantics,),
            "multiplicity_contradiction_handling": (self.multiplicity_handling,),
            "permitted_co_determination_and_deterministic_closure": (self.co_determination_closure,),
            "prior_response_history_predicates_if_used": (self.prior_response_history_predicates,),
            "current_condition_effort_role_if_used": (self.current_condition_effort_role,),
            "effect_graph_and_existing_can008_effect_kinds": (self.effect_kinds,),
            "target_authority_kind_and_target_validation": (self.target_authority_kind, self.target_validation),
            "pff_current_consequence_projection_if_emitted": (self.pff_current_consequence_projection,),
            "valid_empty_behavior": (self.valid_empty_behavior,),
            "missing_deferred_ambiguous_failure_behavior": (self.missing_deferred_ambiguous_behavior,),
            "quantitative_contract_if_numeric": (self.quantitative_contract,),
            "adp020_binding_if_stochastic": (self.adp020_binding,),
            "atomic_validation_commit_behavior": (self.atomic_commit_behavior,),
            "provenance_replay_requirements": (self.provenance_replay_requirements,),
        }
        for item in R2_RULE_OBLIGATION_ITEMS:
            v = vals.get(item)
            if v is None or any(x is None or x == "" or x == () for x in v):
                return f"RESPONSE_COUPLING_RULE_MISSING:{item}"
        if not set(self.effect_kinds) <= set(EFFECT_GRAMMAR):
            return "RESPONSE_COUPLING_RULE_MISSING:effect_kind_outside_adopted_grammar"
        return None


def build_default_binding(actor_scope: str = "ACTOR_SYNTH_1",
                          temporal_scope: str = "T_1998_2000") -> CouplingRuleBinding:
    content = {
        "semantics": "coupling-response candidate over adopted R2 law",
        "effect_kinds": list(EFFECT_GRAMMAR),
        "target": "CAN008_CURRENT_AND_REQUESTED_OWNER_EFFECTS",
    }
    binding = CouplingRuleBinding(
        rule_id=RULE_ID,
        rule_version=RULE_VERSION,
        rule_content_hash=_sha(_canon(content), PINS["CAN008_R2"]),
        eligible_event_authority_signatures=("ISSUER_AUTH_WORLD_SCHED", "ISSUER_AUTH_INSTITUTION"),
        eligible_event_roles=("PRECIPITATING_EVENT_STREAM",),
        actor_scope=actor_scope,
        temporal_scope=temporal_scope,
        receivability_semantics="event public features receivable to actor scope",
        eligible_conditioning_owner_signatures=("CAN010", "CAN011", "ADP015", "ADP016", "ADP017"),
        conditioning_causal_use_roles=("RECRUITMENT_ONLY",),
        counterpart_scoping="none-required",
        modality_evidence_authorities=("NONE_USED:rule-uses-no-modality-evidence",),
        uptake_appraisal_semantics="appraisal projection; NOT durable belief",
        recruitment_semantics="situated recruitment refs; recruitment != actor access",
        multiplicity_handling="all paths preserved; no winner-take-all",
        co_determination_closure="deterministic single-pass closure",
        prior_response_history_predicates="exact verified prior CAN008_CURRENT_RESPONSE_EFFECT; same actor/world; earlier time; BUFFER -> DEFLECT else AMPLIFY",
        current_condition_effort_role="none",
        effect_kinds=EFFECT_GRAMMAR,
        target_authority_kind="CAN008_CURRENT",
        target_validation="atomic precheck then commit or rollback",
        pff_current_consequence_projection="not-emitted",
        valid_empty_behavior="RESPONSE_EFFECTS_VALID_EMPTY lawful and distinct",
        missing_deferred_ambiguous_behavior="typed nonpositive state; never silent conversion",
        quantitative_contract="none",
        adp020_binding="none (deterministic)",
        atomic_commit_behavior="validate-all-then-commit; rollback on any failure",
        provenance_replay_requirements="§17 receipt content bound and replay-exact",
    )
    return __import__("dataclasses").replace(binding, rule_content_hash=binding_digest(binding))


@dataclass
class OwnerPrestate:
    actor_id: str
    can010_expectations: Tuple[str, ...] = ()
    can010_strivings: Tuple[str, ...] = ()
    can011_practices: Tuple[str, ...] = ()
    can011_tensions: Tuple[str, ...] = ()
    adp016_memory_refs: Tuple[str, ...] = ()
    adp017_claim_refs: Tuple[str, ...] = ()
    prior_can008_response_count: int = 0
    world_ref: str = ""
    world_as_of: str = ""


def binding_digest(binding):
    data=asdict(binding);data.pop('rule_content_hash',None)
    implementation={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('can008_candidate_rule.py','candidate_registry_fixture.py','owner_transitions.py','positive_chain.py','adopted_contract.py')}
    return _sha(_canon(dict(binding=data,implementation=implementation)),PINS['CAN008_R2'])


def _refuse(code):
    return dict(decision_state=code,code=code,status='REFUSED',committed=False)


class CouplingEvaluation(dict):
    """Registry-bound evaluated result; an arbitrary dict is never admission."""
    pass


def occurrence_gate(event,registry):
    from .candidate_registry_fixture import validate_event
    code=validate_event(event)
    if code:return dict(status='REFUSED',code=code)
    admitted=registry.admit_event(event)
    if admitted.get('status')=='REFUSED':return admitted
    return dict(status='ADMITTED_OCCURRENCE',event_id=event.event_id,event_hash=event.event_hash)


def coupline_evaluate(event,prestate,binding,registry):
    from .candidate_registry_fixture import validate_event,digest
    # Omitted conditional descriptors mean this feature is unused, not authority.
    err=binding.validate_complete()
    if err:return _refuse('RESPONSE_COUPLING_RULE_MISSING')
    registered=registry.lookup(binding.rule_id,binding.rule_version)
    if registered is None or registered.binding_digest!=binding_digest(binding) or registered.rule_content_hash!=binding.rule_content_hash or binding.rule_content_hash!=binding_digest(binding):
        return _refuse('RESPONSE_COUPLING_RULE_MISSING')
    if prestate.actor_id!=binding.actor_scope or event.actor_scope!=prestate.actor_id:return _refuse('BLOCK_WRONG_ACTOR_SCOPE')
    if (event.world_ref,event.world_as_of)!=(prestate.world_ref,prestate.world_as_of):return _refuse('BLOCK_STALE_OR_MISMATCHED_WORLD_ASOF')
    code=validate_event(event)
    if code:return _refuse(code)
    if not event.public_features:return _refuse('RESPONSE_EVENT_RECEIVABILITY_UNRESOLVED')
    # Candidate conditioning vocabulary is finite. Unknown strings never become
    # a licensed causal owner input. No arbitrary modalities/effort are accepted.
    if (set(prestate.can010_strivings)-{'KEEP_STABLE_SHIFT'} or set(prestate.can011_practices)-{'ASK_CLARIFICATION'} or prestate.can010_expectations or prestate.can011_tensions):
        return _refuse('RESPONSE_CONDITIONING_BINDING_INVALID')
    if prestate.adp016_memory_refs or prestate.adp017_claim_refs:
        # Exact local state refs must be attached and verified by fixture store.
        ctx=getattr(prestate,'_context',None)
        if ctx is None or not ctx.matches_prestate(prestate):return _refuse('RESPONSE_CONDITIONING_OWNER_UNBOUND')
    gate=occurrence_gate(event,registry)
    if gate['status']!='ADMITTED_OCCURRENCE':return _refuse(gate.get('code','BLOCK_UNADMITTED_EVENT'))
    out=CouplingEvaluation(decision_state='COUPLING_EVALUATED',gate=gate,receivability='RECEIVABLE',uptake_appraisal_projection=dict(projection='bounded public-feature appraisal',is_durable_belief=False,is_machine_reading=False,basis=list(event.public_features)),situated_recruitment=[f'ADP016:{x}:RECRUITMENT_ONLY_NOT_ACCESS' for x in prestate.adp016_memory_refs]+list(prestate.can011_practices)+list(prestate.can010_strivings),recruitment_is_not_access=True,committed=False,event=asdict(event),prestate_hash=digest(asdict(prestate)),binding_digest=binding_digest(binding))
    out._registry=registry;out._key=registry.remember_evaluation(dict(out))
    return out


def response_rule_apply(coupling,prestate,binding,requested_effect):
    from .candidate_registry_fixture import digest
    if requested_effect not in EFFECT_GRAMMAR:return _refuse('RESPONSE_COUPLING_RULE_MISSING')
    if coupling.get('decision_state')!='COUPLING_EVALUATED':return _refuse(coupling.get('decision_state','RESPONSE_INPUTS_VALID_EMPTY'))
    if not isinstance(coupling,CouplingEvaluation) or not coupling._registry.verify_evaluation(coupling._key,dict(coupling)) or coupling['prestate_hash']!=digest(asdict(prestate)) or coupling['binding_digest']!=binding_digest(binding):
        return _refuse('RESPONSE_CONDITIONING_BINDING_INVALID')
    if binding.validate_complete() or requested_effect not in binding.effect_kinds:return _refuse('RESPONSE_COUPLING_RULE_MISSING')
    # Pure working-view result; committed can only become true after the journal
    # transaction. It would be false evidence to mark a proposal already committed.
    return dict(decision_state='RESPONSE_EFFECTS_PRODUCED',current_response_consequence=dict(effect_kind=requested_effect,durability='NON_DURABLE_CURRENT_CONSEQUENCE'),target_owner_effect_requests=[dict(target_owner_kind='CAN008_CURRENT',validated=True,committed=False,request_kind='CANDIDATE_CURRENT_HISTORY_ONLY')],destination_owner_hold='HOLD_NO_ACCEPTED_ADP016_ADP017_POSITIVE_AUTHORITY',committed=False)


def build_response_receipt(event: AdmittedEvent, prestate: OwnerPrestate,
                           binding: CouplingRuleBinding,
                           coupling: Dict[str, Any],
                           response: Dict[str, Any]) -> Dict[str, Any]:
    """§17 V3ResponseEvaluationReceipt content (audit/replay evidence; NOT a
    durable actor uptake/memory/belief state)."""
    receipt = {
        "receipt_kind": "V3ResponseEvaluationReceipt",
        "contract": CAN008_R2_CONTRACT,
        "rule_id": binding.rule_id,
        "rule_version": binding.rule_version,
        "rule_content_hash": binding.rule_content_hash,
        "precipitating_event": {
            "event_id": event.event_id, "event_hash": event.event_hash,
            "issuer_authority_id": event.issuer_authority_id,
            "issuer_authority_version": event.issuer_authority_version,
            "actor_scope":event.actor_scope,"world_ref":event.world_ref,"world_as_of":event.world_as_of,
            "effective_causal_time": event.effective_causal_time,
            "role": "PRECIPITATING_EVENT_STREAM",
        },
        "conditioning_owner_refs": list(binding.eligible_conditioning_owner_signatures),
        "conditioning_causal_use_roles": list(binding.conditioning_causal_use_roles),
        "receivability": coupling.get("receivability"),
        "uptake_appraisal_projection": coupling.get("uptake_appraisal_projection"),
        "situated_recruitment": coupling.get("situated_recruitment"),
        "effect_kind": response.get("current_response_consequence", {}).get("effect_kind"),
        "current_response_consequence": response.get("current_response_consequence"),
        "target_owner_effects": response.get("target_owner_effect_requests"),
        "decision_state": response.get("decision_state"),
        "noncollapse_laws_bound": list(NONCOLLAPSE_LAWS),
        "is_durable_actor_state": False,
        "prestate":asdict(prestate),"coupling_event":coupling.get("event"),
    }
    receipt = deepcopy(receipt)
    receipt["receipt_hash"] = _sha(_canon(receipt))
    return receipt


def register_default_rule(registry=None) -> Dict[str, Any]:
    """Register the candidate rule in the WORKER CANDIDATE REGISTRY FIXTURE only."""
    reg = registry if registry is not None else CANDIDATE_REGISTRY
    binding = build_default_binding()
    err = binding.validate_complete()
    if err:
        return {"status": "REFUSED", "code": err}
    return reg.register(CandidateRuleRegistration(
        rule_id=binding.rule_id,
        rule_version=binding.rule_version,
        rule_content_hash=binding.rule_content_hash,
        issuer_authority_id="ISSUER_AUTH_CANDIDATE_FIXTURE",
        issuer_authority_version="1",
        actor_scope=binding.actor_scope,
        temporal_scope=binding.temporal_scope,
        effect_kinds=binding.effect_kinds,
        target_owner_kind="CAN008_CURRENT",
        admission_state="CANDIDATE_ADMITTED_IN_FIXTURE",
        binding_digest=binding_digest(binding),
    ))


def _with_reverse_flag(event: AdmittedEvent) -> AdmittedEvent:
    """Hostile-case helper: mark a causal-parent chronology inversion on a copy."""
    return AdmittedEvent(**{**event.__dict__, "reverse_chronology_flag": True})
