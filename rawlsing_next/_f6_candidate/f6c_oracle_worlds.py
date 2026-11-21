"""R35 F6C independent frozen world fixtures and exact rational oracle.

Independent of the inherited F6C fixture module on purpose: this builder is
written from the producer's own admission contract, not by importing
``f6c_worlds``. Every expected number lives in
01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json, frozen before any candidate ran.

Contract-shaped only: integers / rational strings, required target_id, complete
native joint domains except where a case deliberately breaks positivity.
No raw survey data, no respondent-level join, no actor or route quantity.
"""
from __future__ import annotations

from fractions import Fraction as F

CONSTRUCTS = ("material_security", "employment_position")
LABELS = {
    "material_security": ("secure", "insecure"),
    "employment_position": ("formal", "informal"),
}
# Distinct native codes per source, to prove cross-source comparability is
# established by an explicit reviewed recoding and not by shared naming.
NATIVE_CODES = {
    "S_A": {"material_security": ("A_secure", "A_insecure"),
            "employment_position": ("A_formal", "A_informal")},
    "S_B": {"material_security": ("B_C1", "B_C2"),
            "employment_position": ("B_E1", "B_E2")},
}
CELLS = tuple((a, b) for a in LABELS["material_security"]
              for b in LABELS["employment_position"])


def _axes(sid):
    out = []
    for i, construct in enumerate(CONSTRUCTS):
        out.append({
            "item_ref": f"r35f6c-{sid}-item-{i}@1",
            "construct_ref": construct,
            "mapping_ref": f"r35f6c-{sid}-mapping-{i}@1",
            "mapping_confidence": "HIGH",
            "review_status": "REVIEWED",
            "scale_ref": "named-categories@1",
            "scale_status": "REVIEWED",
            "polarity_ref": "categories-not-score@1",
            "polarity_status": "REVIEWED",
            "instrument_ref": f"r35f6c-{sid}-instrument@1",
            "response_semantics_ref": f"r35f6c-{sid}-named-response-meanings@1",
            # Declared order is insertion order; S03FO canonical order depends on it.
            "category_map": dict(zip(NATIVE_CODES[sid][construct], LABELS[construct])),
        })
    return out


def _source(sid, tag, target, strata_counts, *, lineage=None, sample=None):
    """Build one source-native record.

    strata_counts maps stratum -> either a complete 4-list in declared grid
    order, or an explicit list of (code0, code1, n) triples for sparse cases.
    """
    s = {
        "source_id": sid,
        "product_ref": f"r35f6c-{tag}-{sid}-joint-product@1",
        "survey_lineage": lineage or f"r35f6c-{tag}-survey-{sid}",
        "sample_id": sample or f"r35f6c-{tag}-independent-sample-{sid}",
        "test_origin": True,
        "risk_set_ref": f"r35f6c-{tag}-{sid}-eligible-asked-complete@1",
        "design_ref": f"r35f6c-{tag}-{sid}-stratified-fixed-n@1",
        "weight_ref": "unit-weight@1",
        "routing_ref": f"r35f6c-{tag}-shared-eligibility@1",
        "missingness_ref": "r35f6c-no-missing@1",
        "sampling_limitations": ("Invented fixed-stratum tables built for this court; "
                                 "no real-source design, coverage or weighting "
                                 "validation; not a population estimate"),
        "permission_ref": "SYNTHETIC_ONLY_NO_TRANSPORT_PERMISSION",
        "scope": dict({k: target[k] for k in ("geography", "boundary_ref",
                                              "population", "unit")},
                      start_year=target["year"], end_year=target["year"],
                      fieldwork_ref=f"r35f6c-{target['year']}-{tag}@1"),
    }
    s["measure_basis"] = "UNWEIGHTED"
    s["dependence_kind"] = "MEASURED_SAME_SURVEY_JOINT"
    s["coadministration_ref"] = f"r35f6c-{tag}-{sid}-coadministration@1"
    s["joint_frontier_ref"] = f"r35f6c-{tag}-two-item-complete@1"
    s["axes"] = _axes(sid)
    s["strata"] = {}
    for z, counts in strata_counts.items():
        code0 = NATIVE_CODES[sid]["material_security"]
        code1 = NATIVE_CODES[sid]["employment_position"]
        grid = [(a, b) for a in code0 for b in code1]
        if isinstance(counts, list) and counts and isinstance(counts[0], tuple):
            cells = [{"categories": [a, b], "n": int(n), "mass": int(n)}
                     for a, b, n in counts]
            n = sum(c["n"] for c in cells)
        else:
            assert len(counts) == len(grid), (sid, z, len(grid), len(counts))
            cells = [{"categories": [a, b], "n": int(v), "mass": int(v)}
                     for (a, b), v in zip(grid, counts)]
            n = sum(counts)
        s["strata"][z] = {
            "eligible_n": n, "excluded_n": 0,
            "table_status": "EXHAUSTIVE_DECLARED_JOINT_RISK_SET",
            "support_ref": f"r35f6c-{tag}-{sid}-{z}-support@1",
            "cells": cells,
            "design_variance": {
                # Contract: variances must already be for the MAPPED cell
                # probabilities, i.e. keyed by recoded label, not native code.
                "method_ref": "R35F6C_FIXED_STRATUM_MULTINOMIAL_PLUGIN@1",
                "cells": [{"categories": list(lab),
                           "variance": str(F(v, n) * (1 - F(v, n)) / n)}
                          for lab, v in zip(CELLS, _in_declared_label_order(sid, counts))],
            },
        }
    return s


def _in_declared_label_order(sid, counts):
    """Raw counts expressed in declared LABEL order (the CELLS order).

    The producer requires design variances to be supplied already for the
    mapped cell probabilities, so they must be keyed by recoded label, never by
    the source-native category code.
    """
    if isinstance(counts, list) and counts and isinstance(counts[0], tuple):
        l0 = dict(zip(NATIVE_CODES[sid]["material_security"], LABELS["material_security"]))
        l1 = dict(zip(NATIVE_CODES[sid]["employment_position"], LABELS["employment_position"]))
        ordered = {k: 0 for k in CELLS}
        for a, b, n in counts:
            ordered[(l0[a], l1[b])] = int(n)
        return [ordered[k] for k in CELLS]
    return [int(v) for v in counts]


def _target(tag, region, strata, year=1995):
    return {"target_id": f"R35F6C_{tag}_{year}_ADULT_ELIGIBLE_ASKED_RISK_SET",
            "geography": f"Synthetic Region {region}",
            "boundary_ref": f"r35f6c-boundary-{region}@1",
            "year": year,
            "population": "resident adults in the eligible-and-asked work risk set",
            "unit": "adult respondent",
            "strata_ref": f"r35f6c-population-register-{region}@1",
            "strata": dict(strata)}


def _policy(tag, sids, minimum_raw_support, *, overlap_status="DISJOINT",
            review_ref="r35f6c-independent-sampling-review@1"):
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    return {
        "policy_ref": f"r35f6c-{tag}-standardization-decision@1",
        "scope_review_ref": f"r35f6c-{tag}-scope-review@1",
        "conditional_invariance_ref": f"r35f6c-{tag}-equal-risk-set-law-assumption@1",
        "conditional_invariance_status": "REVIEWED_ASSUMPTION",
        "target_support_ref": f"r35f6c-{tag}-target-support@1",
        "minimum_raw_support": int(minimum_raw_support),
        "maximum_joint_cells": 64,
        "source_weights": {s: 1 for s in sids},
        "mapping_hashes": {},
        "overlap_reviews": {"|".join(sorted(sids)): {"status": overlap_status,
                                                   "review_ref": review_ref}},
        "mapping_bias_radius": "1/100",
        "transport_bias_radius": "1/20",
        "target_share_bias_radius": 0,
    }


def _finish(policy, sources):
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    policy["mapping_hashes"] = {s["source_id"]: semantic_hash(s["axes"]) for s in sources}
    return policy


# ---------------------------------------------------------------- worlds ----

def W1_full_coverage_disjoint():
    """Both sources, both strata, full support, disjoint samples."""
    t = _target("W1", "one", {"majority": "1/2", "minority": "1/2"})
    a = _source("S_A", "W1", t, {"majority": [40, 10, 25, 25], "minority": [25, 25, 10, 40]})
    b = _source("S_B", "W1", t, {"majority": [20, 30, 25, 25], "minority": [40, 10, 25, 25]})
    return t, [a, b], _finish(_policy("W1", ("S_A", "S_B"), 30), [a, b])


def W2_mixed_eligibility_trap():
    """DECISIVE. In stratum minority, S_A fails the aggregate support gate
    (n=10 < 30) while S_B passes. S_A's planned minority share is 1/2 of the
    S_B weight; a correct method must retain 1/4 of the target as unknown."""
    t = _target("W2", "two", {"majority": "1/2", "minority": "1/2"})
    a = _source("S_A", "W2", t, {"majority": [40, 10, 25, 25], "minority": [4, 2, 1, 3]})
    b = _source("S_B", "W2", t, {"majority": [20, 30, 25, 25], "minority": [40, 10, 25, 25]})
    return t, [a, b], _finish(_policy("W2", ("S_A", "S_B"), 30), [a, b])


def W3_minority_whole_stratum_absent():
    """Neither source carries any table for the minority stratum."""
    t = _target("W3", "three", {"majority": "4/5", "minority": "1/5"})
    a = _source("S_A", "W3", t, {"majority": [40, 10, 25, 25]})
    b = _source("S_B", "W3", t, {"majority": [20, 30, 25, 25]})
    return t, [a, b], _finish(_policy("W3", ("S_A", "S_B"), 30), [a, b])


def W4_outcome_leakage():
    """Same coverage as W1; the consumer asks the outcome as its own condition."""
    return W1_full_coverage_disjoint()


def W5_positivity_incomplete_native_domain():
    """S_A omits one native joint cell: (A_insecure, A_informal)."""
    t = _target("W5", "five", {"majority": "1"})
    code0 = NATIVE_CODES["S_A"]["material_security"]
    code1 = NATIVE_CODES["S_A"]["employment_position"]
    sparse = [(code0[0], code1[0], 40), (code0[0], code1[1], 10),
              (code0[1], code1[0], 25)]
    a = _source("S_A", "W5", t, {"majority": sparse})
    b = _source("S_B", "W5", t, {"majority": [20, 30, 25, 25]})
    return t, [a, b], _finish(_policy("W5", ("S_A", "S_B"), 30), [a, b])


def W6_overlap_duplicate_sample():
    """S_A and S_B declare the SAME survey lineage and sample id."""
    t = _target("W6", "six", {"majority": "1"})
    a = _source("S_A", "W6", t, {"majority": [40, 10, 25, 25]},
                lineage="r35f6c-W6-shared-survey", sample="r35f6c-W6-shared-sample")
    b = _source("S_B", "W6", t, {"majority": [20, 30, 25, 25]},
                lineage="r35f6c-W6-shared-survey", sample="r35f6c-W6-shared-sample")
    return t, [a, b], _finish(_policy("W6", ("S_A", "S_B"), 30), [a, b])


def W7_source_excluded_all_strata():
    """S_A fails the aggregate support gate in the only stratum it covers."""
    t = _target("W7", "seven", {"majority": "1/2", "minority": "1/2"})
    a = _source("S_A", "W7", t, {"majority": [2, 1, 1, 2], "minority": [1, 1, 1, 2]})
    b = _source("S_B", "W7", t, {"majority": [20, 30, 25, 25], "minority": [40, 10, 25, 25]})
    return t, [a, b], _finish(_policy("W7", ("S_A", "S_B"), 30), [a, b])


def W8_condition_outside_mapped_support():
    return W1_full_coverage_disjoint()


WORLD_BUILDERS = {
    "W1_full_coverage_disjoint": W1_full_coverage_disjoint,
    "W2_mixed_eligibility_trap": W2_mixed_eligibility_trap,
    "W3_minority_whole_stratum_absent": W3_minority_whole_stratum_absent,
    "W4_outcome_leakage": W4_outcome_leakage,
    "W5_positivity_incomplete_native_domain": W5_positivity_incomplete_native_domain,
    "W6_overlap_duplicate_sample": W6_overlap_duplicate_sample,
    "W7_source_excluded_all_strata": W7_source_excluded_all_strata,
    "W8_condition_outside_mapped_support": W8_condition_outside_mapped_support,
}

# The conditional each case's consumer asks for, and the frozen expectation key.
CONSUMER_REQUEST = {
    "W1_full_coverage_disjoint": ({"material_security": "secure"}, "employment_position"),
    "W2_mixed_eligibility_trap": ({"material_security": "secure"}, "employment_position"),
    "W3_minority_whole_stratum_absent": ({"material_security": "secure"}, "employment_position"),
    "W4_outcome_leakage": ({"employment_position": "formal"}, "employment_position"),
    "W5_positivity_incomplete_native_domain": ({"material_security": "secure"}, "employment_position"),
    "W6_overlap_duplicate_sample": ({"material_security": "secure"}, "employment_position"),
    "W7_source_excluded_all_strata": ({"material_security": "secure"}, "employment_position"),
    "W8_condition_outside_mapped_support": ({"material_security": "unknown_third_state"},
                                           "employment_position"),
}