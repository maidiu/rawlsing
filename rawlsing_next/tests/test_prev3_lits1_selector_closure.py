import copy

import pytest

from rawlsing_next.pre553_empirical_objects import EmpiricalPredicate
from rawlsing_next.prev3_lits1_selector_closure import (
    BASE_C11_HASH,
    D02_FRONTIER_INVARIANTS,
    REAL_SOURCE_SCAN,
    SELECTOR_IDS,
    SOURCE_ROWS,
    SOURCE_SHA256,
    SelectorClosureError,
    build_frontier_readoption,
    build_selector_closure,
    scan_records,
    typed_native_value,
    verify_real_source_summary,
)


def test_closure_mints_new_release_and_exact_six_selectors():
    a = build_selector_closure()
    b = build_selector_closure()
    assert a == b
    assert a["source"]["sha256"] == SOURCE_SHA256
    assert a["new_release_ref"]["content_hash"] != BASE_C11_HASH
    assert a["new_release_ref"] == b["new_release_ref"]
    assert set(a["selectors"]) == set(SELECTOR_IDS.values())
    assert len(a["selectors"]) == 6


def test_q310_q311_are_native_nondirectional_and_missing_distinct():
    closure = build_selector_closure()
    for q in ("q310", "q311"):
        item = closure["questions"][q]
        assert item["directionality"] == "PRESERVED_NON_DIRECTIONAL__NO_SIGN"
        assert set(item["value_state_refs"]) == {"1", "2", "3", "MISSING"}
        assert item["value_state_refs"]["MISSING"] not in [
            item["value_state_refs"][str(v)] for v in (1, 2, 3)
        ]
        assert "PSYCHOLOGICAL" in item["negative_ceiling"]
        assert "CAUSAL" in item["negative_ceiling"]


def test_selector_refs_are_canonical_empirical_predicates():
    closure = build_selector_closure()
    for selector in closure["selectors"].values():
        p = selector["predicate_projection"]
        obj = EmpiricalPredicate(
            typed_state=p["typed_state"],
            authority_snapshot_refs=p["authority_snapshot_refs"],
            dependency_refs=p["dependency_refs"],
            producer_replay_locator_or_reference_root=p["producer_replay_locator_or_reference_root"],
            **p["semantic_fields"],
        )
        assert obj.ref.as_dict() == selector["predicate_ref"]
        assert selector["operation"] == "survey_response_EQ"
        assert selector["source_native_value"] in (1, 2, 3)


def test_real_source_summary_exact_and_all_rows_accounted_for():
    verify_real_source_summary(REAL_SOURCE_SCAN)
    for q in ("q310", "q311"):
        assert sum(REAL_SOURCE_SCAN[q]["counts"].values()) == SOURCE_ROWS
        assert set(REAL_SOURCE_SCAN[q]["counts"]) == {"1", "2", "3", "MISSING"}
    bad = copy.deepcopy(REAL_SOURCE_SCAN)
    bad["q310"]["counts"]["1"] += 1
    with pytest.raises(SelectorClosureError, match="source replay summary mismatch"):
        verify_real_source_summary(bad)


def test_frontier_readoption_is_preimage_only_and_rejects_mutation():
    closure = build_selector_closure()
    receipt = build_frontier_readoption(closure)
    assert receipt["d02_frontier_source"]["artifact_bytes_mutated"] is False
    assert receipt["allowed_mutation"] == "SELECTOR_PREIMAGE_SUBSTITUTION_ONLY"
    assert receipt["workload_execution"] == "NOT_EXECUTED"
    assert len(receipt["selector_preimage_substitutions"]) == 6
    assert receipt["frozen_invariants"] == D02_FRONTIER_INVARIANTS
    bad = copy.deepcopy(D02_FRONTIER_INVARIANTS)
    bad["expected_compiled_candidate_count"] = 49
    with pytest.raises(SelectorClosureError, match="frontier mutation forbidden"):
        build_frontier_readoption(closure, bad)


def test_no_selector_fallback_or_special_value_laundering():
    assert typed_native_value(1) == ("SUBSTANTIVE_RESPONSE", 1)
    assert typed_native_value(2.0) == ("SUBSTANTIVE_RESPONSE", 2)
    assert typed_native_value(None) == ("MISSING", None)
    assert typed_native_value(float("nan")) == ("MISSING", None)
    for value in (0, 4, 6, 7, 99, 1.5, True):
        with pytest.raises(SelectorClosureError):
            typed_native_value(value)


def test_row_scan_deterministic_and_exact_cardinality():
    rows = [
        {"row_ordinal": i, "q310": (i % 3) + 1, "q311": None if i % 11 == 0 else ((i + 1) % 3) + 1}
        for i in range(SOURCE_ROWS)
    ]
    a = scan_records(rows)
    b = scan_records(rows)
    assert a == b
    assert sum(a["q310"]["counts"].values()) == SOURCE_ROWS
    assert sum(a["q311"]["counts"].values()) == SOURCE_ROWS
    with pytest.raises(SelectorClosureError, match="exact source rows"):
        scan_records(rows[:-1])


def test_no_learned_execution_surface_exported():
    import rawlsing_next.prev3_lits1_selector_closure as m
    exported = set(m.__all__)
    assert all("execute" not in name.lower() for name in exported)
    assert all("i03" not in name.lower() and "i05" not in name.lower() for name in exported)
