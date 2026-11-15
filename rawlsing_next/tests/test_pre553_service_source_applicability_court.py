"""HQ205 hostile source-free court — service-source applicability.

Synthetic exact refs only. No real source, no survey access, no warrant.

Implements ONLY the HQ-ratified authority:

    ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED

The resolver answers exactly one question: for this exact service/target/scope and
this positively bounded candidate class, which candidate source universes are
APPLICABLE? Every court below either proves that boundary holds or proves it fails
closed.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from rawlsing_next import pre553_service_source_applicability as M
from rawlsing_next.pre553_service_source_applicability import (
    ApplicabilityAuthorityRecord,
    CandidateClassApplicabilityReceipt,
    CandidateClassBinding,
    ServiceApplicabilityRequest,
    ServiceSourceApplicabilityError,
    assert_complete_coverage,
    assert_receipt_does_not_authorize,
    resolve_service_source_applicability,
)

MODULE_PATH = Path(M.__file__).resolve()


def ref(obj_id: str, kind: str = "TQ") -> dict:
    return {"kind": kind, "object_id": obj_id, "content_hash": "a" * 64}


def auth(version: str = "1.0.0", ident: str = "AUTH_APPLICABILITY") -> dict:
    return {"authority_id": ident, "authority_version": version,
            "authority_content_hash": "b" * 64}


SOURCES = [ref("src-a"), ref("src-b"), ref("src-c")]


def build_class(members=None) -> CandidateClassBinding:
    return CandidateClassBinding(
        candidate_class_ref=ref("class-1"),
        candidate_source_universe_refs=members if members is not None else SOURCES,
        binding_authority_ref=auth("1.0.0", "AUTH_CLASS_BINDING"),
        declared_population_scope_ref=ref("pop-national"),
        declared_geography_scope_ref=ref("geo-country"),
    )


def build_request(members=None, **overrides) -> ServiceApplicabilityRequest:
    members = members if members is not None else SOURCES
    kwargs = dict(
        service_id="REVERSE_POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_INFERENCE",
        service_authority_ref=auth("1.0.0", "AUTH_SERVICE"),
        target_use_ref=ref("target-use-coordinate"),
        population_scope_ref=ref("pop-national"),
        geography_scope_ref=ref("geo-country"),
        effective_time_or_interval_ref=ref("interval-2018"),
        candidate_class_ref=ref("class-1"),
        release_identity_ref=ref("release-2026"),
        target_use_permission_refs=[ref("perm-bound")],
        candidate_source_universe_refs=members,
    )
    kwargs.update(overrides)
    return ServiceApplicabilityRequest.build(**kwargs)


def admitted(src, version="1.0.0"):
    return ApplicabilityAuthorityRecord(src, "ADMITTED", auth(version, "AUTH_ADMISSION"))


def negative(src, decision="SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE", basis="neg-authority"):
    return ApplicabilityAuthorityRecord(src, decision, basis_refs=[ref(basis)])


# ============================================================ exact positive/negative
def test_exact_positive_applicability():
    receipt = resolve_service_source_applicability(build_request(), build_class(), [
        admitted(SOURCES[0]), negative(SOURCES[1]), negative(SOURCES[2])])
    assert receipt.outcome == M.OUTCOME_ADMISSIBLE_SET
    assert receipt.candidate_class_coverage == M.COVERAGE_COMPLETE
    assert receipt.no_applicable_source is False
    states = {d["source_universe_ref"]["object_id"]: d["public_typed_state"] for d in receipt.per_source_states()}
    assert states["src-a"] == "APPLICABLE"
    assert receipt.decisions[0].admission_authority_ref is not None


def test_exact_negative_applicability_requires_basis_ref():
    with pytest.raises(ServiceSourceApplicabilityError):
        ApplicabilityAuthorityRecord(SOURCES[0], "SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE")


def test_noncomparability_is_its_own_public_state():
    receipt = resolve_service_source_applicability(build_request(), build_class(),
                                                   [negative(SOURCES[0], "SOURCE_NONCOMPARABLE_AT_THIS_TARGET")])
    states = {d["source_universe_ref"]["object_id"]: d["public_typed_state"] for d in receipt.per_source_states()}
    assert states["src-a"] == "NONCOMPARABLE"
    assert states["src-a"] != "NOT_APPLICABLE", "noncomparability collapsed into not-applicable"


def test_out_of_scope_is_its_own_public_state():
    receipt = resolve_service_source_applicability(build_request(), build_class(),
                                                   [negative(SOURCES[0], "SOURCE_OUT_OF_DECLARED_SCOPE")])
    states = {d["source_universe_ref"]["object_id"]: d["public_typed_state"] for d in receipt.per_source_states()}
    assert states["src-a"] == "OUT_OF_SCOPE"
    assert states["src-a"] != "NOT_APPLICABLE", "out-of-scope collapsed into not-applicable"


def test_missing_authority_is_not_not_applicable():
    """Silence is never a verdict: absent authority is MISSING_AUTHORITY."""
    receipt = resolve_service_source_applicability(build_request(), build_class(), [])
    states = {d["source_universe_ref"]["object_id"]: d["public_typed_state"] for d in receipt.per_source_states()}
    assert states["src-a"] == "MISSING_AUTHORITY"
    assert states["src-a"] != "NOT_APPLICABLE", "absence of evidence of applicability became evidence of inapplicability"
    assert receipt.candidate_class_coverage == M.COVERAGE_INCOMPLETE


def test_no_positive_authority_is_undetermined_then_missing_authority():
    rec = ApplicabilityAuthorityRecord(SOURCES[0], "UNDETERMINED_NO_POSITIVE_AUTHORITY")
    receipt = resolve_service_source_applicability(build_request(), build_class(), [rec])
    states = {d["source_universe_ref"]["object_id"]: d["public_typed_state"] for d in receipt.per_source_states()}
    assert states["src-a"] == "MISSING_AUTHORITY"
    assert receipt.candidate_class_coverage == M.COVERAGE_INCOMPLETE


def test_conflicting_authority_is_unresolved_never_a_negative_finding():
    rec = ApplicabilityAuthorityRecord(SOURCES[0], "UNKNOWN_OR_CONFLICTING_APPLICABILITY_AUTHORITY")
    receipt = resolve_service_source_applicability(build_request(), build_class(), [rec])
    states = {d["source_universe_ref"]["object_id"]: d["public_typed_state"] for d in receipt.per_source_states()}
    assert states["src-a"] == "UNRESOLVED"
    assert states["src-a"] not in ("NOT_APPLICABLE", "NONCOMPARABLE"), "ambiguity read as a negative finding"
    assert receipt.candidate_class_coverage == M.COVERAGE_INCOMPLETE


# ============================================================ candidate-class coverage
def test_incomplete_candidate_class_does_not_masquerade_as_complete():
    receipt = resolve_service_source_applicability(build_request(), build_class(), [admitted(SOURCES[0])])
    assert receipt.candidate_class_coverage == M.COVERAGE_INCOMPLETE
    assert receipt.is_complete_admissible_set() is False
    assert receipt.outcome == M.OUTCOME_ADMISSIBLE_SET_INCOMPLETE


def test_incomplete_class_never_emits_no_applicable_source():
    """No known positive must NOT be laundered into 'no applicable sources'."""
    receipt = resolve_service_source_applicability(build_request(), build_class(), [])
    assert receipt.no_applicable_source is False
    assert receipt.outcome != M.OUTCOME_NO_ADMITTED_SOURCE
    assert receipt.candidate_class_coverage == M.COVERAGE_INCOMPLETE


def test_complete_class_with_zero_applicable_is_a_first_class_success():
    receipt = resolve_service_source_applicability(build_request(), build_class(), [
        negative(SOURCES[0], basis="n0"),
        negative(SOURCES[1], "SOURCE_NONCOMPARABLE_AT_THIS_TARGET", "n1"),
        negative(SOURCES[2], "SOURCE_OUT_OF_DECLARED_SCOPE", "n2"),
    ])
    assert receipt.outcome == M.OUTCOME_NO_ADMITTED_SOURCE
    assert receipt.no_applicable_source is True
    assert receipt.candidate_class_coverage == M.COVERAGE_COMPLETE
    assert len(receipt.per_source_states()) == 3, "per-candidate reason required for EVERY candidate"


def test_complete_class_with_multiple_applicable_is_an_unranked_set():
    receipt = resolve_service_source_applicability(build_request(), build_class(),
                                                   [admitted(SOURCES[0]), admitted(SOURCES[1])])
    admissible = receipt.admissible_source_universe_refs_as_set()
    assert len(admissible) == 2
    assert len(set(receipt.canonical_replay_only_order)) == 2
    d = receipt.as_dict()
    assert d["cardinality_is_not_a_sample_size"] is True
    assert d["canonical_order_grants_no_rank_priority_preference_weight_or_fallback"] is True
    assert d["ordering_semantics"] == M.ORDERING_SEMANTICS
    for text in ("rank", "priority", "weight", "score", "preference", "tie_break"):
        assert text not in {k.lower() for k in d}, f"{text} leaked into the receipt"


def test_no_applicable_source_requires_complete_coverage_even_if_forced():
    with pytest.raises(ServiceSourceApplicabilityError):
        CandidateClassApplicabilityReceipt(
            receipt_id="x", service_request_set_identity="y", service_id="s",
            candidate_class_ref=ref("class-1"), candidate_class_coverage=M.COVERAGE_INCOMPLETE,
            decisions=(), outcome=M.OUTCOME_NO_ADMITTED_SOURCE, no_applicable_source=True,
            candidate_class_binding={}, request_key={})


def test_downstream_exhaustive_operation_fails_closed_until_coverage_complete():
    incomplete = resolve_service_source_applicability(build_request(), build_class(), [admitted(SOURCES[0])])
    with pytest.raises(ServiceSourceApplicabilityError):
        assert_complete_coverage(incomplete, "EXHAUSTIVE_SOURCE_SET_SERVING")
    complete = resolve_service_source_applicability(build_request(), build_class(), [
        admitted(SOURCES[0]), negative(SOURCES[1]), negative(SOURCES[2])])
    assert_complete_coverage(complete, "EXHAUSTIVE_SOURCE_SET_SERVING")


# ============================================================ binding / class integrity
def test_candidate_class_mismatch_is_refused():
    other = build_class([ref("src-x")])
    with pytest.raises(ServiceSourceApplicabilityError):
        resolve_service_source_applicability(build_request(), other, [admitted(SOURCES[0])])


def test_silent_candidate_class_broadening_is_refused():
    """A request may not supply a broader class than the positive bound."""
    broader = SOURCES + [ref("src-unbound")]
    with pytest.raises(ServiceSourceApplicabilityError):
        resolve_service_source_applicability(build_request(broader), build_class(), [])


def test_candidate_class_narrowing_is_also_refused():
    with pytest.raises(ServiceSourceApplicabilityError):
        resolve_service_source_applicability(build_request([SOURCES[0]]), build_class(), [])


def test_authority_outside_the_bounded_class_is_refused():
    with pytest.raises(ServiceSourceApplicabilityError):
        resolve_service_source_applicability(build_request(), build_class(), [admitted(ref("src-outside"))])


def test_unbounded_candidate_class_is_refused():
    with pytest.raises(ServiceSourceApplicabilityError):
        build_class([])


def test_missing_request_component_refuses_no_partial_key():
    with pytest.raises(ServiceSourceApplicabilityError):
        ServiceApplicabilityRequest.build(
            service_id="SVC", service_authority_ref=auth(),
            target_use_ref=ref("u"), population_scope_ref=ref("p"),
            geography_scope_ref=ref("g"), candidate_class_ref=ref("class-1"),
            release_identity_ref=ref("r"))


def test_mutable_authority_selector_is_refused():
    with pytest.raises(ServiceSourceApplicabilityError):
        build_request(service_authority_ref=auth("LATEST"))
    with pytest.raises(ServiceSourceApplicabilityError):
        admitted(SOURCES[0], version="DEFAULT")


def test_admitted_without_provenance_is_refused():
    with pytest.raises(ServiceSourceApplicabilityError):
        ApplicabilityAuthorityRecord(SOURCES[0], "ADMITTED")


def test_nonpositive_must_not_carry_admission_provenance():
    with pytest.raises(ServiceSourceApplicabilityError):
        ApplicabilityAuthorityRecord(SOURCES[0], "SOURCE_OUT_OF_DECLARED_SCOPE",
                                     admission_authority_ref=auth(), basis_refs=[ref("b")])


def test_duplicate_authority_for_one_source_is_refused():
    with pytest.raises(ServiceSourceApplicabilityError):
        resolve_service_source_applicability(build_request(), build_class(),
                                             [admitted(SOURCES[0]), admitted(SOURCES[0])])


def test_unknown_decision_is_refused():
    with pytest.raises(ServiceSourceApplicabilityError):
        ApplicabilityAuthorityRecord(SOURCES[0], "MOSTLY_APPLICABLE")


# ============================================================ replay determinism
def test_deterministic_serialization_under_permuted_input_order():
    records = [admitted(SOURCES[0]), negative(SOURCES[1]), negative(SOURCES[2])]
    a = resolve_service_source_applicability(build_request(), build_class(), records)
    b = resolve_service_source_applicability(build_request(), build_class(), list(reversed(records)))
    c = resolve_service_source_applicability(build_request(), build_class(), records[1:] + records[:1])
    assert a.replay_identity() == b.replay_identity() == c.replay_identity()
    assert a.canonical_replay_only_order == b.canonical_replay_only_order


def test_replay_identity_is_stable_across_repeated_resolution():
    records = [admitted(SOURCES[0]), admitted(SOURCES[2])]
    ids = {resolve_service_source_applicability(build_request(), build_class(), records).replay_identity()
           for _ in range(5)}
    assert len(ids) == 1


def test_replay_identity_changes_when_the_request_changes():
    records = [admitted(SOURCES[0])]
    a = resolve_service_source_applicability(build_request(), build_class(), records)
    b = resolve_service_source_applicability(build_request(target_use_ref=ref("other-target")),
                                            build_class(), records)
    assert a.replay_identity() != b.replay_identity()


# ============================================================ power noncollapse
@pytest.mark.parametrize("purpose", list(M.FORBIDDEN_AUTHORIZED_PURPOSES))
def test_receipt_is_not_authority_for_any_separate_power(purpose):
    receipt = resolve_service_source_applicability(build_request(), build_class(),
                                                   [admitted(SOURCES[0]), negative(SOURCES[1])])
    with pytest.raises(ServiceSourceApplicabilityError):
        assert_receipt_does_not_authorize(receipt, purpose)


def test_no_ranking_metadata_can_be_smuggled_into_the_request_key():
    for name in ("ranking", "score", "weight", "priority", "preference",
                 "selection_reason", "pooling", "linkage", "overlap", "backfill"):
        with pytest.raises(ServiceSourceApplicabilityError):
            ServiceApplicabilityRequest.build(
                service_id="SVC", service_authority_ref=auth(), target_use_ref=ref("u"),
                population_scope_ref=ref("p"), geography_scope_ref=ref("g"),
                effective_time_or_interval_ref=ref("t"), candidate_class_ref=ref("class-1"),
                release_identity_ref=ref("r"), target_use_permission_refs=[ref("perm")],
                candidate_source_universe_refs=SOURCES, **{name: "smuggled"})


def test_no_internal_evidence_field_can_be_smuggled_into_the_request_key():
    for name in ("evidence", "evidence_state", "support", "sufficiency", "sample_size", "denominator"):
        with pytest.raises(ServiceSourceApplicabilityError):
            ServiceApplicabilityRequest.build(
                service_id="SVC", service_authority_ref=auth(), target_use_ref=ref("u"),
                population_scope_ref=ref("p"), geography_scope_ref=ref("g"),
                effective_time_or_interval_ref=ref("t"), candidate_class_ref=ref("class-1"),
                release_identity_ref=ref("r"), target_use_permission_refs=[ref("perm")],
                candidate_source_universe_refs=SOURCES, **{name: "smuggled"})


def test_only_admitted_carries_any_positive_power_flag():
    for state in M.DECISION_PRECEDENCE:
        flags = M.DECISION_MATRIX[state]
        positives = {k for k, v in flags.items() if v is True}
        if state == M.POSITIVE_DECISION:
            assert positives == {"positive_admission", "may_enter_source_set",
                                 "may_constrain_downstream_query_scope"}
        else:
            assert positives == set(), f"{state} carries a power flag it must not have"


def test_no_state_may_pool_transform_or_infer_individual():
    for state in M.DECISION_PRECEDENCE:
        flags = M.DECISION_MATRIX[state]
        assert flags["may_pool_respondents"] is False
        assert flags["may_transform_geometry_or_distribution"] is False
        assert flags["may_support_individual_inference"] is False
        assert flags["may_rank_or_select"] is False
        assert flags["may_condition_F8"] is False
        assert flags["may_grant_target_use_permission"] is False
        assert flags["may_authorise_backfill"] is False


def test_target_use_permission_ref_is_bound_input_not_a_grant():
    request = build_request()
    assert request.as_dict()["target_use_permission_refs_are_bound_input_not_a_grant"] is True
    receipt = resolve_service_source_applicability(request, build_class(), [admitted(SOURCES[0])])
    for state in M.DECISION_PRECEDENCE:
        assert M.DECISION_MATRIX[state]["may_grant_target_use_permission"] is False


def test_state_family_is_new_and_not_aliased():
    assert M.STATE_FAMILY == "SERVICE_SOURCE_APPLICABILITY_STATE"
    receipt = resolve_service_source_applicability(build_request(), build_class(), [admitted(SOURCES[0])])
    assert receipt.as_dict()["state_family"] == "SERVICE_SOURCE_APPLICABILITY_STATE"
    for other in M.MUST_NOT_ALIAS_STATE_FAMILIES:
        assert other != M.STATE_FAMILY
        assert receipt.as_dict()["may_not_alias_state_families"].count(other) == 1


def test_public_vocabulary_is_the_seven_ratified_states_and_cannot_be_widened():
    assert set(M.PUBLIC_STATES) == {"APPLICABLE", "NOT_APPLICABLE", "NONCOMPARABLE", "OUT_OF_SCOPE",
                                   "MISSING_AUTHORITY", "UNRESOLVED", "INTEGRITY_FAILURE"}
    assert M.PUBLIC_STATE_BY_DECISION["ADMITTED"] == "APPLICABLE"
    assert M.POSITIVE_PUBLIC_STATE == "APPLICABLE"
    for decision, public in M.PUBLIC_STATE_BY_DECISION.items():
        assert decision in M.DECISION_PRECEDENCE
        assert public in M.PUBLIC_STATES


def test_decision_precedence_puts_admitted_last_and_integrity_first():
    assert M.DECISION_PRECEDENCE[0] == "INTEGRITY_FAILURE"
    assert M.DECISION_PRECEDENCE[-1] == "ADMITTED"
    assert set(M.NONPOSITIVE_DECISIONS) == set(M.DECISION_PRECEDENCE[:-1])


# ============================================================ evidence distinction
def test_no_admitted_source_is_not_evidence_not_found():
    """The two live at different grains in different families."""
    receipt = resolve_service_source_applicability(build_request(), build_class(), [
        negative(SOURCES[0], basis="n0"), negative(SOURCES[1], basis="n1"), negative(SOURCES[2], basis="n2")])
    assert receipt.no_applicable_source is True
    for d in receipt.per_source_states():
        assert d["public_typed_state"] != "APPLICABLE"
    laws = receipt.as_dict()["non_collapse_laws"]
    assert "NO_ADMITTED_SOURCE_IN_CANDIDATE_CLASS != NO_EVIDENCE_FOUND" in laws


def test_applicable_source_with_missing_internal_evidence_is_a_different_grain():
    """APPLICABLE at source grain, then a downstream evidence state. Not a negative here."""
    receipt = resolve_service_source_applicability(build_request(), build_class(),
                                                   [admitted(SOURCES[0]), negative(SOURCES[1]),
                                                    negative(SOURCES[2])])
    states = {d["source_universe_ref"]["object_id"]: d["public_typed_state"] for d in receipt.per_source_states()}
    assert states["src-a"] == "APPLICABLE"
    assert receipt.no_applicable_source is False


def test_decision_object_carries_no_internal_evidence_field():
    field_names = set(M.ServiceSourceApplicabilityDecision.REQUIRED_FIELDS)
    for forbidden in M.ServiceSourceApplicabilityDecision.FORBIDDEN_FIELDS:
        assert forbidden not in field_names, f"{forbidden} leaked into the decision object"
    receipt = resolve_service_source_applicability(build_request(), build_class(), [admitted(SOURCES[0])])
    d = receipt.decisions[0].as_dict()
    assert d["carries_no_internal_evidence_field"] is True
    assert d["applicability_predates_evidence"] is True
    for forbidden in M.ServiceSourceApplicabilityDecision.FORBIDDEN_FIELDS:
        assert forbidden not in d


def test_no_internal_evidence_state_changes_applicability():
    """The resolver reads no evidence field, so none can move an applicability state."""
    base = resolve_service_source_applicability(build_request(), build_class(),
                                                [admitted(SOURCES[0]), negative(SOURCES[1])])
    again = resolve_service_source_applicability(build_request(), build_class(),
                                                 [admitted(SOURCES[0]), negative(SOURCES[1])])
    assert base.replay_identity() == again.replay_identity()
    source = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    reads = [n.attr for n in ast.walk(source)
             if isinstance(n, ast.Attribute) and n.attr in M.ServiceSourceApplicabilityDecision.FORBIDDEN_FIELDS]
    assert reads == [], f"resolver inspected internal evidence: {sorted(set(reads))}"


def test_no_selection_reason_record_exists():
    receipt = resolve_service_source_applicability(build_request(), build_class(),
                                                   [admitted(SOURCES[0]), negative(SOURCES[1])])
    d = receipt.as_dict()
    assert d["no_selection_reason_record_exists"] is True
    assert d["admission_provenance_is_the_lawful_substitute"] is True
    # No FIELD is a selection-reason record, at receipt or decision grain.
    assert not any(k == "selection_reason" or k.endswith("_selection_reason") for k in d)
    for decision in receipt.decisions:
        names = set(M.ServiceSourceApplicabilityDecision.REQUIRED_FIELDS)
        assert "selection_reason" not in names
        assert not any("selection" in n for n in names)
    assert "selection_reason" not in M.ServiceSourceApplicabilityDecision.REQUIRED_FIELDS


def test_admission_provenance_is_carried_per_admitted_entry():
    receipt = resolve_service_source_applicability(build_request(), build_class(),
                                                   [admitted(SOURCES[0]), admitted(SOURCES[2])])
    for decision in receipt.decisions:
        if decision.applicability_decision == "ADMITTED":
            assert decision.admission_authority_ref is not None
            assert decision.admission_provenance_refs, "admitted entry carried no provenance"
        else:
            assert decision.admission_provenance_refs == ()


def test_admitted_entries_remain_separate_not_a_sample():
    receipt = resolve_service_source_applicability(build_request(), build_class(),
                                                   [admitted(SOURCES[0]), admitted(SOURCES[1])])
    d = receipt.as_dict()
    assert d["admissible_set_is_a_set_of_separate_source_indexed_entries"] is True
    assert d["cardinality_is_not_a_sample_size"] is True
    assert "combined_estimand" not in str(d)
    assert "pooled" not in {k.lower() for k in d}


def test_geography_and_population_are_inclusion_filters_only():
    receipt = resolve_service_source_applicability(build_request(), build_class(), [admitted(SOURCES[0])])
    d = receipt.as_dict()
    assert d["geography_and_population_are_inclusion_filters_only"] is True
    assert d["locality_assigns_no_priority"] is True


# ============================================================ module hygiene
def test_module_declares_no_ranking_weighting_or_pooling_surface():
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            d = ast.get_docstring(node, clean=False)
            if d is not None:
                docstrings.add(d)
    # Naming a forbidden purpose is the REFUSAL mechanism, so the declarative
    # refusal vocabularies are exempt. Only capability surfaces are banned.
    exempt = set(M.FORBIDDEN_AUTHORIZED_PURPOSES) | set(M.NON_COLLAPSE_LAWS) \
        | set(M.FORBIDDEN_REQUEST_KEY_NAMES) | {M.ORDERING_SEMANTICS, M.AUTHORISED_AUTHORITY}
    banned_exact = {"rank", "ranking", "score", "weight", "priority", "preference",
                    "pool", "pooling", "linkage", "backfill"} - {v.lower() for v in exempt}
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value not in docstrings:
            assert node.value.lower() not in banned_exact, f"banned literal {node.value!r}"
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assert node.name.lower() not in banned_exact, f"banned function {node.name!r}"


def test_module_registers_no_state_alias_to_other_families():
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    assert M.STATE_FAMILY not in ("SOURCE_UNIVERSE_RELATION_STATE", "EMPIRICAL_FACT_STATE",
                                  "STRUCTURAL_ADMISSION_STATE", "AUTHORITY_STATE")
    # the module must not import another family's decision objects
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "source_relations" not in node.module, "applicability must not borrow the relation family"
            assert "empirical_query" not in node.module, "applicability must not borrow the evidence family"


def test_receipt_carries_the_exact_ratified_authority_label():
    receipt = resolve_service_source_applicability(build_request(), build_class(), [admitted(SOURCES[0])])
    assert receipt.authorised_authority == "ADMISSIBLE_SET_ONLY__RANKING_AND_SELECTION_NOT_AUTHORIZED"
    assert receipt.as_dict()["authorised_authority"] == M.AUTHORISED_AUTHORITY
