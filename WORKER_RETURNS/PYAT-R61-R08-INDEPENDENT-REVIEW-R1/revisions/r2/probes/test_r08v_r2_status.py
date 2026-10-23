from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_evidence_binding import (
    EvidenceResolver,
    EvidenceResult,
    reduce_required_support,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case
from rawlsing_next.tests.test_universal_evidence_binding import _binding, _request


def _control(state: str, denominator=10):
    return EvidenceResult(
        request_key=semantic_hash({"control": state, "d": denominator}),
        eligibility_state="ELIGIBLE",
        execution_state="COMPLETED",
        result_state=state,
        provenance="TYPED_REFUSAL",
        denominator=denominator,
        typed_refusal="CONTROL" if state in {"ZERO_SUPPORT", "UNKNOWN", "UNSUPPORTED"} else None,
    )


def test_valid_products_keep_distinct_productive_states():
    for state in ("VALID_NULL", "DIFFUSE", "VALID_EMPTY", "OBSERVED_ZERO"):
        summary = reduce_required_support([_control(state)])
        assert summary.support_state == f"{state}_PRODUCTIVE", summary.support_state
        assert summary.productive_all_required is True
        assert summary.exact_all_support is False
        assert summary.positive_support_count == 0


def test_zero_unknown_and_mixed_valid_do_not_become_exact_support():
    zero = _control("ZERO_SUPPORT", denominator=0)
    zero_summary = reduce_required_support([zero])
    assert zero_summary.support_state == "ZERO_SUPPORT"
    assert zero_summary.exact_all_support is False
    assert zero_summary.productive_all_required is False

    unknown = EvidenceResult(
        request_key=semantic_hash({"control": "z-unresolved"}),
        eligibility_state="UNKNOWN",
        execution_state="COMPLETED",
        result_state="UNKNOWN",
        provenance="TYPED_REFUSAL",
        denominator=16,
        typed_refusal="Z_UNRESOLVED",
    )
    unknown_summary = reduce_required_support([unknown])
    assert unknown_summary.support_state == "UNKNOWN_SUPPORT"
    assert unknown_summary.unresolved_denominator_support == 16
    assert unknown_summary.exact_all_support is False
    assert unknown_summary.productive_all_required is False

    mixed = reduce_required_support([_control("VALID_NULL"), _control("DIFFUSE")])
    assert mixed.support_state == "MIXED_VALID_PRODUCTS"
    assert mixed.exact_all_support is False
    assert mixed.productive_all_required is True

    case = build_provider_case("forward")
    request = _request(case, request_id="r08v-r2-status-positive")
    resolver = EvidenceResolver()
    resolver.bind(_binding(request, case))
    positive = resolver.resolve(request)
    assert positive.result_state == "SUPPORTED"
    exact = reduce_required_support([positive])
    assert exact.support_state == "EXACT_SUPPORT"
    assert exact.exact_all_support is True
    assert exact.positive_support_count == 1
