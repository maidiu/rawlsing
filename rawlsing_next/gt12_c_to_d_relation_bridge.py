"""Lossless GT12-C ExactConditionalSupportProfile -> GT12-D PRE-V3 admission bridge."""
from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Any, Mapping
from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, exact_ref, semantic_hash

BRIDGE_CONTRACT_ID = "GT12_C_TO_D_TYPED_LOSSLESS_BRIDGE@1.0.0"
CLOSURE_PROGRAM_COMMIT = "a473091473f5729dd9aa6e54d68b88de49f9d608"
EXPECTED_RELATION_OWNER = ff.SEMANTIC_OWNER
EXPECTED_RELATION_FAMILY = ff.RELATION_FAMILY

class GT12CToDBridgeError(ValueError): pass
class GT12CToDBridgeTypeError(GT12CToDBridgeError): pass

def _dref(kind: str, ns: str, material: Mapping[str, Any]) -> ExactRef:
    h = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:gt12:c-to-d:{ns}:sha256:{h}", h)

def frozen_gt12_c_relation_rule_ref() -> ExactRef:
    return _dref("FIELD_FORGE_RELATION_RULE", "conditional-support-rule", {
        "relation_family": ff.RELATION_FAMILY,
        "semantic_owner": EXPECTED_RELATION_OWNER,
        "relation_semantics": ff.RELATION_SEMANTICS,
        "conditioner": [ff.CONDITIONER_ROLE, ff.CONDITIONER_SOURCE_NATIVE_VARIABLE],
        "target": [ff.TARGET_ROLE, ff.TARGET_SOURCE_NATIVE_VARIABLE],
        "participant_role_order": [ff.CONDITIONER_ROLE, ff.TARGET_ROLE],
        "state_order_semantics": ff.STATE_ORDER_SEMANTICS,
        "target_order": ff.FROZEN_TARGET_ORDER,
        "information_loss": ff.INFORMATION_LOSS,
        "producer_function": "produce_exact_conditional_support_profile",
    })

def _risk() -> ExactRef:
    return ExactRef("RISK_SET", adm.GT2_RISK_SET_ID, adm.GT2_RISK_SET_MEMBER_SET_SHA256)

def _source() -> ExactRef:
    return ExactRef("SOURCE_ARTIFACT", adm.GT2_SOURCE_PATH, adm.GT2_SOURCE_SHA256)

def _selection(r: ff.ExactConditionalSupportProfile) -> ExactRef:
    return _dref("FIELD_FORGE_RELATION_CURRENT_SELECTION", "current-selection", {
        "contract": BRIDGE_CONTRACT_ID, "closure_program_commit": CLOSURE_PROGRAM_COMMIT,
        "frozen_canary_commit": adm.FROZEN_CANARY_COMMIT, "relation_ref": r.ref.as_dict(),
        "relation_rule_ref": frozen_gt12_c_relation_rule_ref().as_dict(),
        "state": "CURRENT_EXACT_GT12_C_RELATION_FOR_BOUNDED_D_ADMISSION_ONLY",
        "authority_effect": "NONE__IDENTITY_SELECTION_ONLY",
    })

def _blocker(r: ff.ExactConditionalSupportProfile) -> ExactRef:
    return _dref("FIELD_FORGE_RELATION_TYPED_BLOCKER", "producer-state-blocker", {
        "contract": BRIDGE_CONTRACT_ID, "relation_ref": r.ref.as_dict(),
        "relation_typed_state": r.typed_state, "producer_state_blocking": r.producer_state_blocking,
        "conditional_count_profile_is_empty": not bool(r.conditional_count_profile),
        "semantic_effect": "PRESERVE_UPSTREAM_BLOCKER__NO_ADMISSION_PROMOTION",
    })

def _validate(value: object) -> ff.ExactConditionalSupportProfile:
    if type(value) is not ff.ExactConditionalSupportProfile:
        raise GT12CToDBridgeTypeError("only actual ExactConditionalSupportProfile is accepted; no EmpiricalFact/I04/duck coercion")
    r = value
    if r.semantic_owner != EXPECTED_RELATION_OWNER:
        raise GT12CToDBridgeError("FIELD FORGE relation semantic owner substitution detected")
    if adm.GT2_RELATION_OWNER != EXPECTED_RELATION_OWNER:
        raise GT12CToDBridgeError("GT12-D relation-owner binding differs from actual GT12-C owner")
    if adm.OWNER == EXPECTED_RELATION_OWNER:
        raise GT12CToDBridgeError("relation semantic owner must differ from PRE-V3 admission owner")
    if r.family != EXPECTED_RELATION_FAMILY or adm.GT2_RELATION_FAMILY != EXPECTED_RELATION_FAMILY:
        raise GT12CToDBridgeError("relation family mismatch")
    p = r.semantic_projection()
    if semantic_hash(p) != r.content_hash or r.ref.content_hash != r.content_hash or r.ref.object_id != r.object_id:
        raise GT12CToDBridgeError("relation ref/hash identity mismatch")
    roles = p.get("roles")
    if not isinstance(roles, Mapping) or p.get("participant_role_order") != [ff.CONDITIONER_ROLE, ff.TARGET_ROLE]:
        raise GT12CToDBridgeError("CONDITIONER/TARGET role order drift")
    c, t = roles.get(ff.CONDITIONER_ROLE), roles.get(ff.TARGET_ROLE)
    if not isinstance(c, Mapping) or not isinstance(t, Mapping): raise GT12CToDBridgeError("participant role material missing")
    if c.get("source_native_variable") != "Q86B" or t.get("source_native_variable") != "Q86A":
        raise GT12CToDBridgeError("frozen Q86B CONDITIONER / Q86A TARGET drift")
    if canonicalize(c.get("ref")) != canonicalize(r.conditioner_ref.as_dict()) or canonicalize(t.get("ref")) != canonicalize(r.target_ref.as_dict()):
        raise GT12CToDBridgeError("participant ref loss")
    if p.get("information_loss") != ff.INFORMATION_LOSS: raise GT12CToDBridgeError("information-loss drift")
    if r.risk_set_ref != _risk(): raise GT12CToDBridgeError("frozen risk-set exact identity mismatch")
    if len(r.empirical_universe_refs) != 1: raise GT12CToDBridgeError("bounded bridge requires one exact universe")
    if r.producer_fact_ref.kind != "EmpiricalFact@1.0.0" or r.producer_query_ref.kind != "EmpiricalQuerySpec@1.0.0":
        raise GT12CToDBridgeError("producer fact/query exact family mismatch")
    if not r.producer_authority_refs or not r.producer_provenance_refs: raise GT12CToDBridgeError("producer closure missing")
    # A hash-consistent Field Forge profile can declare a different physical
    # SOURCE_ARTIFACT while this bridge would otherwise stamp the frozen one.
    # Reject *contradictory* declared source identities before D can admit them.
    # This check is not native C11/source authentication: the fixed current
    # transport has a large release/event provenance closure rather than a
    # direct SOURCE_ARTIFACT ref. Missing source refs remain an explicit hold.
    declared_sources = tuple(ref for ref in r.producer_provenance_refs
                             if ref.kind == "SOURCE_ARTIFACT")
    if declared_sources and (len(declared_sources) != 1 or declared_sources[0] != _source()):
        raise GT12CToDBridgeError("declared producer source contradicts frozen GT12 physical source")
    if not set(r.relation_permission_ceiling) <= set(r.producer_permission_ceiling): raise GT12CToDBridgeError("permission widening")
    if r.producer_state_blocking != (r.typed_state != "SUPPORTED"): raise GT12CToDBridgeError("typed-state blocker mismatch")
    if r.producer_state_blocking == bool(r.conditional_count_profile): raise GT12CToDBridgeError("blocking/profile inconsistency")
    return r

def bridge_gt12_c_relation_to_d_evidence(relation: ff.ExactConditionalSupportProfile) -> adm.FieldForgeRelationEvidence:
    r = _validate(relation); rule = frozen_gt12_c_relation_rule_ref(); source = _source()
    participants = (
        adm.ParticipantBinding("CONDITIONER", 0, adm.GT2_CONDITIONER, adm.GT2_CONDITIONER_IMPL, adm.GT2_Q86_SOURCE_STRUCTURE, r.conditioner_ref),
        adm.ParticipantBinding("TARGET", 1, adm.GT2_TARGET, adm.GT2_TARGET_IMPL, adm.GT2_Q86_SOURCE_STRUCTURE, r.target_ref),
    )
    sem = tuple(sorted({r.ref, r.conditioner_ref, r.target_ref, r.producer_fact_ref, r.producer_query_ref}, key=lambda x:x.key))
    scope = tuple(sorted({r.conditioner_ref, r.target_ref, r.risk_set_ref}, key=lambda x:x.key))
    deps = tuple(sorted({source, r.risk_set_ref, r.producer_fact_ref, r.producer_query_ref, r.producer_replay_ref, *r.empirical_universe_refs, *r.producer_provenance_refs}, key=lambda x:x.key))
    negatives = (_blocker(r),) if r.producer_state_blocking else ()
    replay = _dref("FIELD_FORGE_RELATION_REPLAY_ROOT", "relation-replay", {
        "contract": BRIDGE_CONTRACT_ID, "relation_ref": r.ref.as_dict(), "relation_rule_ref": rule.as_dict(),
        "producer_fact_ref": r.producer_fact_ref.as_dict(), "producer_query_ref": r.producer_query_ref.as_dict(),
        "producer_replay_ref": r.producer_replay_ref.as_dict(), "information_loss": ff.INFORMATION_LOSS,
    })
    return adm.FieldForgeRelationEvidence(
        r.ref, r.content_hash, r.family, r.semantic_owner, rule, rule.content_hash, r.typed_state,
        source, adm.GT2_SOURCE_FAMILY, adm.GT2_SOURCE_WAVE, r.risk_set_ref, adm.GT2_RISK_SET_ROWS,
        participants, r.relation_permission_ceiling, r.producer_authority_refs, (_selection(r),), sem, scope,
        r.empirical_universe_refs, deps, negatives, ff.INFORMATION_LOSS, replay,
    )

def make_gt12_c_to_d_admission_rule(relation: ff.ExactConditionalSupportProfile) -> adm.FieldForgeRelationAdmissionRule:
    r = _validate(relation)
    return adm.make_gt2_relation_admission_rule(allowed_relation_rule_ref=frozen_gt12_c_relation_rule_ref(), condition_participant_ref=r.conditioner_ref, target_participant_ref=r.target_ref)

@dataclass(frozen=True)
class GT12CToDAdmissionResult:
    relation_ref: ExactRef
    evidence: adm.FieldForgeRelationEvidence
    rule: adm.FieldForgeRelationAdmissionRule
    admission: adm.Prev3FieldForgeRelationAdmission
    # Diagnostic at the entrypoint only; never part of the D scientific or issuer receipt.
    # Lower-tier consumers that strip this wrapper lose the qualification and must
    # NOT imply that D's own receipt authenticates a physical source.
    sourcefree_origin_path: str = "DECLARED_SOURCE_CONTRADICTION_ONLY__ORIGIN_UNVERIFIED"
    def __post_init__(self):
        if self.evidence.relation_ref != self.relation_ref or self.admission.relation_ref != self.relation_ref:
            raise GT12CToDBridgeError("relation exact ref was replaced across bridge")
        if self.admission.relation_owner != EXPECTED_RELATION_OWNER:
            raise GT12CToDBridgeError("FIELD FORGE owner was not preserved")

def admit_gt12_c_relation(relation: ff.ExactConditionalSupportProfile) -> GT12CToDAdmissionResult:
    r = _validate(relation); evidence = bridge_gt12_c_relation_to_d_evidence(r); rule = make_gt12_c_to_d_admission_rule(r)
    receipt = adm.evaluate_gt2_relation_admission(adm.RelationAdmissionRequest(evidence), rule)
    return GT12CToDAdmissionResult(r.ref, evidence, rule, receipt)

def admit_gt12_c_relation_from_verified_current_objects(
    relation: ff.ExactConditionalSupportProfile,
    *,
    joint_query: "EmpiricalQuerySpec",
    joint_fact: "EmpiricalFact",
) -> GT12CToDAdmissionResult:
    """Bind an existing current R1C object pair to the relation, no second 76,843-ref load.

    All accepted hashes refer to the immutable *committed transport*; the
    object and relation content are independently reverified here. This is
    sourcefree content identity, not a new physical SAV/source-use certificate.
    A caller cannot substitute a fresh arbitrary source, or claim a generalized
    Field Forge / scientific / actor authority. The selected R1C E2B harness
    invokes this API only after its own exact preflight.
    """
    from rawlsing_next.pre553_empirical_objects import (
        EmpiricalFact, EmpiricalQuerySpec,
    )
    from rawlsing_next.pre553_repo_native_current_payload import (
        CURRENT_QUERY_HASH, CURRENT_FACT_HASH, CURRENT_REPLAY_HASH,
        CURRENT_PREDICATE_HASH,
    )
    r = _validate(relation)
    if type(joint_query) is not EmpiricalQuerySpec or type(joint_fact) is not EmpiricalFact:
        raise GT12CToDBridgeTypeError("verified current path requires actual query/fact objects")
    if r.typed_state != "SUPPORTED" or r.producer_state_blocking:
        raise GT12CToDBridgeError("verified current positive transport requires SUPPORTED relation")
    if (r.producer_permission_ceiling != (adm.GT2_TARGET_USE,)
            or r.relation_permission_ceiling != (adm.GT2_TARGET_USE,)):
        raise GT12CToDBridgeError("verified current path refuses non-exact permission budgets")
    if (semantic_hash(joint_query.semantic_projection()) != joint_query.content_hash
            or semantic_hash(joint_fact.semantic_projection()) != joint_fact.content_hash):
        raise GT12CToDBridgeError("current query/fact content hash integrity failure")
    if (joint_query.content_hash != CURRENT_QUERY_HASH
            or joint_fact.content_hash != CURRENT_FACT_HASH
            or exact_ref(joint_fact.replay_ref, "current fact.replay_ref").content_hash != CURRENT_REPLAY_HASH):
        raise GT12CToDBridgeError("not the exact fixed current fact/query/replay")
    if (exact_ref(joint_fact.empirical_query_spec_ref) != joint_query.ref
            or exact_ref(joint_query.condition_predicate_ref) != exact_ref(joint_fact.condition_predicate_ref)
            or exact_ref(joint_query.condition_predicate_ref).content_hash != CURRENT_PREDICATE_HASH):
        raise GT12CToDBridgeError("current fact/query/predicate closure mismatch")
    if (r.producer_query_ref != joint_query.ref or r.producer_fact_ref != joint_fact.ref
            or r.producer_replay_ref != exact_ref(joint_fact.replay_ref)):
        raise GT12CToDBridgeError("relation is not the exact fixed current fact/query/replay")
    canonical = ff.produce_exact_conditional_support_profile(
        joint_fact=joint_fact, joint_query=joint_query,
        conditioner_ref=joint_query.target_refs[0],
        target_ref=joint_query.target_refs[1],
        producer_permission_ceiling=(adm.GT2_TARGET_USE,),
        relation_permission_ceiling=(adm.GT2_TARGET_USE,),
    )
    if canonical.ref != r.ref or canonical.semantic_projection() != r.semantic_projection():
        raise GT12CToDBridgeError("relation differs from verified current fact/query reconstruction")
    return replace(
        admit_gt12_c_relation(r),
        sourcefree_origin_path="EXACT_PINNED_R1C_TRANSPORT_CONTENT__SOURCEFREE_ONLY",
    )


def admit_gt12_c_relation_from_fixed_current_transport(
    relation: ff.ExactConditionalSupportProfile,
) -> GT12CToDAdmissionResult:
    """Opt-in cold reconstruction of the fixed current sourcefree transport.

    Reconstructs the entire committed closure and delegates to the exact
    object verifier. This is slower than supplying already verified query/fact
    objects and still grants no original SAV/native source rights.
    """
    from rawlsing_next.pre553_repo_native_current_payload import (
        load_current_gt2_query_fact_from_committed_transport,
    )
    query, fact = load_current_gt2_query_fact_from_committed_transport()
    return admit_gt12_c_relation_from_verified_current_objects(
        relation, joint_query=query, joint_fact=fact,
    )

def replay_gt12_c_to_d_admission(relation: ff.ExactConditionalSupportProfile, historical: adm.Prev3FieldForgeRelationAdmission) -> adm.Prev3FieldForgeRelationAdmission:
    e = bridge_gt12_c_relation_to_d_evidence(relation); rule = make_gt12_c_to_d_admission_rule(relation)
    return adm.replay_gt2_relation_admission(relation=e, rule=rule, historical_receipt=historical)

__all__ = ["BRIDGE_CONTRACT_ID","CLOSURE_PROGRAM_COMMIT","EXPECTED_RELATION_OWNER","EXPECTED_RELATION_FAMILY","GT12CToDBridgeError","GT12CToDBridgeTypeError","GT12CToDAdmissionResult","frozen_gt12_c_relation_rule_ref","bridge_gt12_c_relation_to_d_evidence","make_gt12_c_to_d_admission_rule","admit_gt12_c_relation","admit_gt12_c_relation_from_fixed_current_transport","admit_gt12_c_relation_from_verified_current_objects","replay_gt12_c_to_d_admission"]
