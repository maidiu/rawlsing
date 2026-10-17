"""Invented material/work distributions, never a proxy for any real survey.

The illustrative scope name/year situates the contract, not an empirical claim.
Native instruments differ by category code and sample-stratum proportions.
"""
from fractions import Fraction as F
from rawlsing_next.pre553_empirical_objects import semantic_hash

CELLS = [("secure", "formal"), ("secure", "informal"),
         ("insecure", "formal"), ("insecure", "informal")]


def fixtures():
    target = {"target_id": "SYNTHETIC_REGION_2012_ADULT_WORK_RISK_SET",
              "geography": "Synthetic Region", "boundary_ref": "synthetic-boundary@1",
              "year": 2012, "population": "resident adults in shared eligible/asked work risk set",
              "unit": "adult respondent", "strata_ref": "synthetic-population-register@1",
              "strata": {"majority": "4/5", "minority": "1/5"}}
    sources = []
    for sid, counts, native in [
        ("A", {"majority": [63, 9, 9, 9], "minority": [1, 1, 1, 7]}, [CELLS, CELLS]),
        ("B", {"majority": [12, 4, 2, 2], "minority": [8, 16, 16, 40]},
         [[("1", "10"), ("1", "20"), ("2", "10"), ("2", "20")]] * 2),
    ]:
        s = {"source_id": sid, "product_ref": f"synthetic-{sid}-joint-product@1",
             "survey_lineage": f"synthetic-survey-{sid}", "sample_id": f"independent-{sid}",
             "test_origin": True, "risk_set_ref": f"synthetic-{sid}-eligible-asked-complete@1",
             "design_ref": f"synthetic-{sid}-stratified-SRS-fixed-n@1", "weight_ref": "unit-weight@1",
             "routing_ref": "synthetic-shared-eligibility@1", "missingness_ref": "synthetic-no-missing@1",
             "sampling_limitations": "Invented fixed-stratum SRS tables; no real-source design/coverage validation",
             "permission_ref": "SYNTHETIC_ONLY", "scope": {k: target[k] for k in ("geography", "boundary_ref", "population", "unit")},
             "measure_basis": "UNWEIGHTED", "dependence_kind": "MEASURED_SAME_SURVEY_JOINT",
             "coadministration_ref": f"synthetic-{sid}-coadministration@1",
             "joint_frontier_ref": "synthetic-two-item-complete@1", "axes": [], "strata": {}}
        s["scope"].update(start_year=2012, end_year=2012, fieldwork_ref="synthetic-2012@1")
        for i, (construct, labels) in enumerate([("material_security", ["secure", "insecure"]),
                                                 ("employment_position", ["formal", "informal"])]):
            codes = labels if sid == "A" else (["1", "2"] if i == 0 else ["10", "20"])
            s["axes"].append({"item_ref": f"synthetic-{sid}-item-{i}@1", "construct_ref": construct,
                              "mapping_ref": f"synthetic-{sid}-mapping-{i}@1", "mapping_confidence": "HIGH",
                              "review_status": "REVIEWED", "scale_ref": "named-categories@1",
                              "scale_status": "REVIEWED", "polarity_ref": "categories-not-score@1",
                              "polarity_status": "REVIEWED", "instrument_ref": f"synthetic-{sid}-instrument@1",
                              "response_semantics_ref": f"synthetic-{sid}-named-response-meanings@1",
                              "category_map": dict(zip(codes, labels))})
        for z, cat in zip(counts, native):
            n = sum(counts[z])
            s["strata"][z] = {"eligible_n": n, "excluded_n": 0,
                              "table_status": "EXHAUSTIVE_DECLARED_JOINT_RISK_SET",
                              "support_ref": f"synthetic-{sid}-{z}-support@1",
                              "cells": [{"categories": list(k), "n": v, "mass": v} for k, v in zip(cat, counts[z])]}
            # Synthetic multinomial SRS approximation is an externally supplied
            # fixture variance. It does not qualify any actual survey design.
            s["strata"][z]["design_variance"] = {
                "method_ref": "SYNTHETIC_FIXED_STRATUM_MULTINOMIAL_PLUGIN@1",
                "cells": [{"categories": list(k), "variance": str(F(v, n) * (1 - F(v, n)) / n)} for k, v in zip(CELLS, counts[z])]}
        sources.append(s)
    policy = {"policy_ref": "synthetic-standardization-decision@1", "scope_review_ref": "synthetic-scope-review@1",
              "conditional_invariance_ref": "synthetic-equal-risk-set-and-stratum-law-assumption@1",
              "conditional_invariance_status": "REVIEWED_ASSUMPTION",
              "target_support_ref": target["strata_ref"], "minimum_raw_support": 1,
              "maximum_joint_cells": 64,
              "source_weights": {"A": 1, "B": 1}, "mapping_hashes": {s["source_id"]: semantic_hash(s["axes"]) for s in sources},
              "overlap_reviews": {"A|B": {"status": "DISJOINT", "review_ref": "synthetic-independent-sampling@1"}},
              "mapping_bias_radius": "1/100", "transport_bias_radius": "1/20", "target_share_bias_radius": 0}
    return target, sources, policy
