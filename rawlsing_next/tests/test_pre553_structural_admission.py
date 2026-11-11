import hashlib
import inspect
from dataclasses import replace

import pytest

import rawlsing_next.pre553_structural_admission as i04
from rawlsing_next.m1_temporal_v554_admission_dedup import DIRECT_SLOTS
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, AuthoritySnapshot, EmpiricalFact, EmpiricalQuerySpec, ExactRef,
    Pre553SemanticCollapseError, semantic_hash,
)
from rawlsing_next.pre553_structural_admission import (
    AdmissionCondition, RequiredAuthorityBinding, StructuralAdmissionRequest,
    StructuralAdmissionRule, evaluate_structural_empirical_admission,
    project_admission_to_m1_direct_basis, project_admission_to_v553_participant,
)


def h(x): return hashlib.sha256(x.encode()).hexdigest()
def ref(k, x): return ExactRef(k, f"urn:test:{k.lower()}:{x}", h(f"{k}:{x}"))
def aref(x, version="1.0.0", digest=None): return AuthorityRef(f"AUTH-{x}", version, digest or h(f"authority:{x}:{version}"))
def root(x): return ref("REPLAY_ROOT", x)

USE = "STRUCTURAL_MEDIATION_INPUT"
U1, U2 = ref("EmpiricalUniverse@1.0.0", "U1"), ref("EmpiricalUniverse@1.0.0", "U2")
Q, P, R = ref("QUESTION", "Q1"), ref("EmpiricalPredicate@1.0.0", "P"), ref("RISK_SET", "R")
SCOPE, TIME, TIME2 = ref("NATIVE_SCOPE", "S"), ref("SOURCE_TIME", "T1"), ref("SOURCE_TIME", "T2")
EST, MEASURE = ref("ESTIMAND", "E"), ref("MEASURE_WEIGHT_AUTHORITY", "M")
UNC, STATE = ref("UNCERTAINTY", "U"), ref("RESPONSE_STATE_SEMANTICS", "RS")
PERM, TARGET = ref("TARGET_USE_PERMISSION", "P"), ref("STRUCTURAL_TARGET", "RESOURCE_PRESSURE")
FOCAL, SSEM = ref("STRUCTURAL_PROPOSITION", "F"), ref("STRUCTURAL_SEMANTICS", "S")
NEG, INTERP = ref("NEGATIVE_AUTHORITY", "NO_ACTOR"), ref("INTERPRETATION_AUTHORITY", "I")
QUERY_AUTH = aref("query")


def authority(tag, kind, op, *, state="ALLOW", digest=None, version="1.0.0", universes=(U1,), families=("StructuralEmpiricalAdmission@1.0.0",)):
    a = aref(tag, version, digest)
    return AuthoritySnapshot(
        typed_state=state, authority_snapshot_refs=(), dependency_refs=(),
        producer_replay_locator_or_reference_root=root(f"a-{tag}-{state}"),
        authority_id=a.authority_id, authority_version=a.authority_version,
        authority_content_hash=a.authority_content_hash, authority_kind=kind,
        decision_state=state, governed_operations=(op,), governed_object_families=families,
        scope_envelope={"source_universe_refs": tuple(universes), "target_use_refs": (USE,)},
        effective_time_or_interval="ALL_TIME", parent_authority_refs=(), negative_limit_refs=(),
        supersession_refs=(), interpretation_semantics_fingerprint=h(f"sem:{tag}:{state}"),
        replay_protocol_ref=ref("REPLAY_PROTOCOL", tag),
    )


def query_fact(*, state="SUPPORTED", n=3, d=5, universes=(U1,), tag="x"):
    q = EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE", authority_snapshot_refs=(QUERY_AUTH,),
        dependency_refs=(), producer_replay_locator_or_reference_root=root(f"q-{tag}"),
        target_refs=(Q,), target_arity_and_topology={"arity": 1, "topology": "SCALAR"},
        condition_predicate_ref=P, risk_set_ref=R, empirical_universe_refs=universes,
        scope_refs=(SCOPE,), measure_basis_ref=MEASURE, requested_output_grain="FULL_TARGET_DISTRIBUTION",
        query_authority_refs=(QUERY_AUTH,),
    )
    f = EmpiricalFact(
        typed_state=state, authority_snapshot_refs=(QUERY_AUTH,), dependency_refs=(q.ref,),
        producer_replay_locator_or_reference_root=root(f"f-{tag}"), empirical_query_spec_ref=q.ref,
        empirical_universe_refs=universes, target_topology={"cells": ("A",)}, condition_predicate_ref=P,
        risk_set_ref=R, raw_numerator_support=n, raw_denominator_support=d,
        weighted_numerator_support_if_authorized=None, weighted_denominator_support_if_authorized=None,
        measure_basis_ref=MEASURE, response_state_semantics_ref=STATE,
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED",
        source_empirical_provenance_refs=(ref("PROVENANCE", tag),), replay_ref=ref("REPLAY", tag),
    )
    return q, f


def request(*, conditions=(), time=(TIME,), legacy=(), native=(SCOPE,), estimand=(EST,), measure=(MEASURE,)):
    return StructuralAdmissionRequest(
        native_scope_identity_refs=native,
        effective_time_or_interval_refs_required_by_target_use=time,
        estimand_refs=estimand, measure_and_weight_authority_refs=measure,
        support_uncertainty_refs=(UNC,), interpretation_critical_authority_refs=(INTERP,),
        conditions=conditions, legacy_compatibility_refs=legacy,
    )


def environment(*, admission_state="ALLOW", allowed_states=("SUPPORTED", "OBSERVED_ZERO", "LOW_SUPPORT"),
                universes=(U1,), negative_only=False, compatibility=False, parity=True, version="1.0.0"):
    qa = authority("query", "PREDICATE_GRAMMAR", "AUTHORIZE_QUERY_FACT", universes=universes,
                   families=("EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"))
    pa = authority("perm", "TARGET_USE_PERMISSION", "ALLOW_STRUCTURAL_USE", universes=universes)
    ta = authority("time", "TEMPORAL_EVIDENCE", "BIND_SOURCE_REFERENCE_TIME", universes=universes)
    ma = authority("measure", "WEIGHT_DESIGN_ESTIMAND", "BIND_MEASURE_ESTIMAND", universes=universes)
    binds = (
        RequiredAuthorityBinding("TARGET_USE_PERMISSION", pa.authority_ref, "TARGET_USE_PERMISSION", "ALLOW_STRUCTURAL_USE", target_use_ref=USE),
        RequiredAuthorityBinding("TEMPORAL_EVIDENCE", ta.authority_ref, "TEMPORAL_EVIDENCE", "BIND_SOURCE_REFERENCE_TIME", source_universe_ref=universes[0]),
        RequiredAuthorityBinding("MEASURE_WEIGHT_ESTIMAND", ma.authority_ref, "WEIGHT_DESIGN_ESTIMAND", "BIND_MEASURE_ESTIMAND", source_universe_ref=universes[0]),
    )
    surface = ref("LEGACY_SEMANTIC_SURFACE", "V552") if compatibility else None
    parity_ref = ref("PARITY_RECEIPT", "V552") if compatibility and parity else None
    retained = ref("RETAINED_STRUCTURAL_MEANING", "V552") if compatibility and parity else None
    pscope = {"producer": "V552", "claim": "EXACT_SEMANTIC_PARITY"} if compatibility and parity else None

    def mk(a):
        return StructuralAdmissionRule(
            admission_authority_ref=a, admission_operation="ADMIT_EMPIRICAL_FACT_TO_STRUCTURAL_USE",
            target_use=USE, allowed_empirical_fact_states=allowed_states,
            allowed_empirical_fact_families=("EmpiricalFact@1.0.0",),
            allowed_empirical_query_families=("EmpiricalQuerySpec@1.0.0",),
            required_empirical_predicate_target_semantics_refs=(Q, P, R, STATE),
            structural_target_identity_refs=(TARGET,), focal_structural_proposition_ref=FOCAL,
            structural_semantic_identity_refs=(SSEM,),
            interpretation_or_transformation_semantics={"kind": "BOUNDED_STRUCTURAL_EVIDENCE"},
            directionality_or_role_semantics={"direction": "EMPIRICAL_TO_STRUCTURAL_PROPOSITION"},
            target_use_permission_refs=(PERM,), allowed_native_scope_identity_refs=(SCOPE,),
            allowed_effective_time_or_interval_refs=(TIME,), allowed_estimand_refs=(EST,),
            allowed_measure_and_weight_authority_refs=(MEASURE,),
            allowed_uncertainty_states=("UNCERTAINTY_UNQUANTIFIED",),
            source_disagreement_noncomparability_policy="PRESERVE_SOURCE_INDEXED_OR_FAIL_CLOSED",
            negative_authority_refs=(NEG,), required_authority_bindings=binds,
            time_geography_applicability={"scope": SCOPE.as_dict(), "time": TIME.as_dict()},
            effective_period={"time": TIME.as_dict()}, downstream_structural_producer_or_use=USE,
            replay_semantics={"exact": True}, negative_authority_only=negative_only,
            compatibility_semantic_surface_ref=surface, compatibility_parity_claim_scope=pscope,
            compatibility_parity_receipt_ref=parity_ref,
            compatibility_retained_structural_meaning_ref=retained,
        )
    provisional = mk(AuthorityRef("AUTH-admit", version, "0" * 64))
    exact = AuthorityRef("AUTH-admit", version, semantic_hash(provisional.semantic_material))
    rule = mk(exact)
    adm = authority("admit", "STRUCTURAL_ADMISSION", "ADMIT_EMPIRICAL_FACT_TO_STRUCTURAL_USE",
                    state=admission_state, digest=exact.authority_content_hash, version=version,
                    universes=universes)
    return rule, AuthorityRegistry((qa, pa, ta, ma, adm)), adm, parity_ref


def evaluate(*, fact_state="SUPPORTED", n=3, d=5, admission_state="ALLOW", req=None, universes=(U1,), **rule_kw):
    q, f = query_fact(state=fact_state, n=n, d=d, universes=universes, tag=fact_state)
    rule, reg, adm, parity = environment(admission_state=admission_state, universes=universes, **rule_kw)
    r = evaluate_structural_empirical_admission(
        query=q, fact=f, requested_admission_authority_ref=adm.authority_ref, rule=rule,
        request=req or request(), authority_registry=reg, producer_replay_locator_or_reference_root=root("i04"),
    )
    return q, f, rule, reg, adm, parity, r


def test_exact_named_rule_is_only_positive_path_and_binds_full_receipt():
    q, f, rule, _, adm, _, out = evaluate()
    assert out.decision_state == "ADMITTED"
    assert out.receipt.typed_state == "ADMITTED_FOR_EXACT_STRUCTURAL_USE"
    assert out.receipt.empirical_query_spec_ref == q.ref.as_dict()
    assert out.receipt.empirical_fact_ref == f.ref.as_dict()
    assert out.receipt.admission_authority_ref == adm.authority_ref.as_dict()
    assert out.receipt.focal_structural_proposition_ref == FOCAL.as_dict()
    assert out.receipt.structural_semantic_identity_refs
    assert out.receipt.source_universe_refs and out.receipt.estimand_refs
    assert out.receipt.measure_and_weight_authority_refs and out.receipt.support_uncertainty_state
    assert out.receipt.authority_closure_refs and out.receipt.structural_interpretation_payload["admission_rule_hash"] == rule.admission_rule_hash


def test_missing_rule_denied_deferred_and_negative_only_never_promote():
    q, f = query_fact()
    _, reg, adm, _ = environment()
    missing = evaluate_structural_empirical_admission(
        query=q, fact=f, requested_admission_authority_ref=aref("missing"), rule=None, request=request(),
        authority_registry=reg, producer_replay_locator_or_reference_root=root("missing"))
    assert missing.decision_state == "MISSING_STRUCTURAL_ADMISSION_AUTHORITY"
    assert missing.m1_direct_projection is None
    for state, expected in (("DENY", "ADMISSION_DENIED"), ("DEFER", "ADMISSION_DEFERRED")):
        assert evaluate(admission_state=state)[-1].decision_state == expected
        assert evaluate(admission_state=state)[-1].m1_direct_projection is None
    assert evaluate(negative_only=True)[-1].decision_state == "NEGATIVE_AUTHORITY_ONLY"


def test_precedence_and_unresolved_target_are_exact():
    denied = AdmissionCondition("ADMISSION_DENIED", "DENY", (ref("BLOCK", "D"),))
    unresolved = AdmissionCondition("STRUCTURAL_TARGET_UNRESOLVED", "TARGET", (ref("BLOCK", "T"),))
    assert evaluate(req=request(conditions=(unresolved, denied)))[-1].decision_state == "ADMISSION_DENIED"
    assert evaluate(req=request(conditions=(unresolved,)))[-1].decision_state == "STRUCTURAL_TARGET_UNRESOLVED"


@pytest.mark.parametrize("state,n,d,allowed,expected", [
    ("OBSERVED_ZERO", 0, 5, ("OBSERVED_ZERO",), "ADMITTED"),
    ("ZERO_SUPPORT", 0, 0, ("SUPPORTED",), "INSUFFICIENT_EVIDENCE_UNDER_RULE"),
    ("LOW_SUPPORT", 1, 5, ("LOW_SUPPORT",), "ADMITTED"),
    ("NONCOMPARABLE", 1, 5, ("NONCOMPARABLE",), "EMPIRICAL_FACT_NONCOMPARABLE"),
    ("VALID_EMPTY", 0, 0, ("VALID_EMPTY",), "VALID_EMPTY"),
])
def test_typed_empirical_states_preserved(state, n, d, allowed, expected):
    out = evaluate(fact_state=state, n=n, d=d, allowed_states=allowed)[-1]
    assert out.decision_state == expected


def test_scope_time_estimand_and_measure_fail_closed():
    assert evaluate(req=request(time=(TIME2,)))[-1].decision_state == "TEMPORAL_SCOPE_MISMATCH"
    assert evaluate(req=request(native=(ref("NATIVE_SCOPE", "OTHER"),)))[-1].decision_state == "SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE"
    assert evaluate(req=request(estimand=(ref("ESTIMAND", "OTHER"),)))[-1].decision_state == "EMPIRICAL_FACT_NONCOMPARABLE"
    assert evaluate(req=request(measure=(ref("MEASURE_WEIGHT_AUTHORITY", "OTHER"),)))[-1].decision_state == "EMPIRICAL_FACT_NONCOMPARABLE"


def test_multi_universe_does_not_compose_without_separate_relation_authority():
    out = evaluate(universes=(U1, U2))[-1]
    assert out.decision_state == "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY"
    assert out.m1_direct_projection is None


def test_legacy_compatibility_requires_exact_parity_and_never_imports_legacy_runtime():
    q, f = query_fact(tag="compat")
    rule, reg, adm, _ = environment(compatibility=True, parity=False)
    blocked = evaluate_structural_empirical_admission(
        query=q, fact=f, requested_admission_authority_ref=adm.authority_ref, rule=rule,
        request=request(legacy=(ref("LEGACY_PACKET", "V552"),)), authority_registry=reg,
        producer_replay_locator_or_reference_root=root("compat"))
    assert blocked.decision_state == "UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY"
    rule, reg, adm, parity_ref = environment(compatibility=True, parity=True)
    ok = evaluate_structural_empirical_admission(
        query=q, fact=f, requested_admission_authority_ref=adm.authority_ref, rule=rule,
        request=request(legacy=(parity_ref,)), authority_registry=reg,
        producer_replay_locator_or_reference_root=root("compat-ok"))
    assert ok.decision_state == "ADMITTED"
    source = inspect.getsource(i04)
    assert "data.ddm_build" not in source and "build_determinicity" not in source


def test_rule_hash_and_query_fact_identity_tamper_fail_integrity():
    q, f, rule, reg, adm, _, _ = evaluate()
    changed = replace(rule, interpretation_or_transformation_semantics={"kind": "BOUNDED_STRUCTURAL_EVIDENCE", "changed": True})
    bad = evaluate_structural_empirical_admission(
        query=q, fact=f, requested_admission_authority_ref=adm.authority_ref, rule=changed,
        request=request(), authority_registry=reg, producer_replay_locator_or_reference_root=root("bad"))
    assert bad.decision_state == "INTEGRITY_FAILURE"
    q2, _ = query_fact(tag="other")
    bad2 = evaluate_structural_empirical_admission(
        query=q2, fact=f, requested_admission_authority_ref=adm.authority_ref, rule=rule,
        request=request(), authority_registry=reg, producer_replay_locator_or_reference_root=root("bad2"))
    assert bad2.decision_state == "INTEGRITY_FAILURE"


def test_actor_position_psyche_and_diagnostic_structuralization_are_rejected():
    rule, _, _, _ = environment()
    for semantics in ({"kind": "GENERATED_ACTOR_POSITION"}, {"kind": "ACTOR_BELIEF"}, {"kind": "DIAGNOSTIC_SCORE_AS_STRUCTURAL_FACT"}):
        with pytest.raises(Pre553SemanticCollapseError):
            replace(rule, interpretation_or_transformation_semantics=semantics)
    with pytest.raises(Pre553SemanticCollapseError):
        replace(rule, structural_target_identity_refs=(ref("GENERATED_ACTOR_POSITION", "X"),))


def test_m1_projection_is_exact_frozen_17_slots_and_only_for_admitted():
    out = evaluate()[-1]
    p = out.m1_direct_projection
    assert tuple(i04.M1_DIRECT_PROJECTION_FIELDS) == tuple(DIRECT_SLOTS)
    assert tuple(p) == tuple(DIRECT_SLOTS) and len(p) == 17
    assert out.m1_projection_hash == semantic_hash(p)
    assert "scr553_decision_state" not in p and "signature_id" not in p
    denied = evaluate(admission_state="DENY")[-1]
    with pytest.raises(i04.StructuralAdmissionProjectionError):
        project_admission_to_m1_direct_basis(denied.receipt)


def test_v553_projection_is_exact_three_field_reference_and_never_temporal_decision():
    for out in (evaluate()[-1], evaluate(admission_state="DENY")[-1]):
        p = project_admission_to_v553_participant(out.receipt, role="STRUCTURAL_EMPIRICAL_ADMISSION", ordinal=2)
        assert tuple(p) == i04.V553_PARTICIPANT_FIELDS
        assert p["structural_empirical_admission_ref"] == out.receipt.ref.as_dict()
        assert "required_temporal_operations" not in p
        assert "V553_REQUIRED" not in p.values() and "V553_NOT_REQUIRED_FOR_THIS_USE" not in p.values()
    assert not i04.V553_INGRESS_CONTRACT["p06_i04_decides_v553_required"]
    assert not i04.V553_INGRESS_CONTRACT["p06_i04_mints_temporal_objects"]


def test_decision_matrix_is_exact_p06_precedence_and_only_admitted_positive():
    assert tuple(i04.DECISION_MATRIX) == i04.DECISION_PRECEDENCE
    assert [s for s, row in i04.DECISION_MATRIX.items() if row["positive_structural_evidence"]] == ["ADMITTED"]
    assert [s for s, row in i04.DECISION_MATRIX.items() if row["m1_direct_projection_allowed"]] == ["ADMITTED"]
    assert all(row["v553_reference_allowed"] for row in i04.DECISION_MATRIX.values())
    assert not any(row["v553_positive_temporal_output_implied"] for row in i04.DECISION_MATRIX.values())


def test_set_order_replay_is_stable_and_rule_version_changes_identity():
    extra = ref("INTERPRETATION_AUTHORITY", "EXTRA")
    q, f = query_fact(tag="replay")
    rule, reg, adm, _ = environment()
    a = StructuralAdmissionRequest((SCOPE,), (TIME,), (EST,), (MEASURE,), (UNC,), (INTERP, extra))
    b = StructuralAdmissionRequest((SCOPE,), (TIME,), (EST,), (MEASURE,), (UNC,), (extra, INTERP, extra))
    x = evaluate_structural_empirical_admission(query=q, fact=f, requested_admission_authority_ref=adm.authority_ref,
        rule=rule, request=a, authority_registry=reg, producer_replay_locator_or_reference_root=root("replay"))
    y = evaluate_structural_empirical_admission(query=q, fact=f, requested_admission_authority_ref=adm.authority_ref,
        rule=rule, request=b, authority_registry=reg, producer_replay_locator_or_reference_root=root("replay"))
    assert x.receipt.ref == y.receipt.ref and x.m1_projection_hash == y.m1_projection_hash
    r2, reg2, adm2, _ = environment(version="2.0.0")
    z = evaluate_structural_empirical_admission(query=q, fact=f, requested_admission_authority_ref=adm2.authority_ref,
        rule=r2, request=a, authority_registry=reg2, producer_replay_locator_or_reference_root=root("replay"))
    assert x.receipt.ref != z.receipt.ref
