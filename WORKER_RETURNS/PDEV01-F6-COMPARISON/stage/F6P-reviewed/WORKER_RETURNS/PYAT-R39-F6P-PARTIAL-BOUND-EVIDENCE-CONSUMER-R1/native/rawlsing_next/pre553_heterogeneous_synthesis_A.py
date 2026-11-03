"""Bounded descriptive synthesis of admitted survey joint summaries.

No source reader, respondent linker, semantic issuer, or selected-world adapter.
Inputs retain source-native tables; standardization is a separately inferred
distribution. Real use requires an external owner admission callback, including
scope/operation/permissions verification. Hashes are replay identities, not rights.
All identity-bearing numeric inputs are integers or rational strings.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from typing import Callable

from rawlsing_next.pre553_empirical_objects import semantic_hash

METHOD = "PRE553_TARGET_JOINT_STANDARDIZATION@1"


class SynthesisError(ValueError):
    pass


def _q(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise SynthesisError("numeric inputs must be integers or rational strings")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise SynthesisError("invalid rational") from exc


def _number(value, low=0, high=None):
    q = _q(value)
    if q < low or (high is not None and q > high):
        raise SynthesisError("numeric input outside bounds")
    return q


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise SynthesisError("missing identity/semantic material")
    return value


def _distribution(table):
    total = sum(table.values(), F(0))
    return {k: str(v / total) for k, v in sorted(table.items())} if total else {}


def _target_check(target):
    for k in ("target_id", "geography", "boundary_ref", "population", "unit", "strata_ref"):
        _text(target[k])
    if type(target["year"]) is not int or not target["strata"]:
        raise SynthesisError("invalid target time/support")
    strata = {_text(k): _number(v) for k, v in target["strata"].items()}
    if sum(strata.values()) != 1:
        raise SynthesisError("target shares must sum to one")
    return strata


def _source_check(source):
    for k in ("source_id", "product_ref", "survey_lineage", "sample_id", "risk_set_ref",
              "design_ref", "weight_ref", "routing_ref", "missingness_ref", "permission_ref", "sampling_limitations"):
        _text(source[k])
    if type(source["test_origin"]) is not bool:
        raise SynthesisError("explicit synthetic origin required")
    scope = source["scope"]
    for k in ("geography", "boundary_ref", "population", "unit", "fieldwork_ref"):
        _text(scope[k])
    if any(type(scope[k]) is not int for k in ("start_year", "end_year")) or scope["start_year"] > scope["end_year"]:
        raise SynthesisError("invalid source dates")
    axes = source["axes"]
    if not axes or len({a["construct_ref"] for a in axes}) != len(axes):
        raise SynthesisError("empty/duplicate construct topology")
    for a in axes:
        for k in ("item_ref", "construct_ref", "mapping_ref", "scale_ref", "polarity_ref", "instrument_ref", "response_semantics_ref"):
            _text(a[k])
        if not a["category_map"] or any(not isinstance(k, str) or not isinstance(v, str)
                                        for k, v in a["category_map"].items()):
            raise SynthesisError("invalid category map")
    if source["measure_basis"] not in ("UNWEIGHTED", "WEIGHTED"):
        raise SynthesisError("invalid measure basis")
    if source["dependence_kind"] != "MEASURED_SAME_SURVEY_JOINT":
        raise SynthesisError("marginals or modeled dependence cannot claim measured joint")
    _text(source["coadministration_ref"])
    _text(source["joint_frontier_ref"])
    if not source["strata"]:
        raise SynthesisError("empty source support")
    for z, table in source["strata"].items():
        _text(z)
        _text(table["support_ref"])
        if table["table_status"] != "EXHAUSTIVE_DECLARED_JOINT_RISK_SET":
            raise SynthesisError("suppressed/unvisited cells cannot be treated as zeros")
        if type(table["eligible_n"]) is not int or type(table["excluded_n"]) is not int or table["excluded_n"] < 0:
            raise SynthesisError("invalid risk set counts")
        seen = set()
        for cell in table["cells"]:
            categories = tuple(cell["categories"])
            if len(categories) != len(axes) or categories in seen:
                raise SynthesisError("duplicate or malformed joint cell")
            seen.add(categories)
            if any(cat not in a["category_map"] for cat, a in zip(categories, axes)):
                raise SynthesisError("unmapped native category; preserve missing states upstream")
            n = cell["n"]
            if type(n) is not int or n < 0:
                raise SynthesisError("invalid raw support")
            w = _number(cell["mass"])
            if source["measure_basis"] == "UNWEIGHTED" and w != n:
                raise SynthesisError("unweighted mass must equal raw count")
            if (n == 0) != (w == 0):
                raise SynthesisError("weighted/raw zero support mismatch")
        if sum(c["n"] for c in table["cells"]) + table["excluded_n"] != table["eligible_n"]:
            raise SynthesisError("denominator/exclusion conservation failed")
        # S03F Fix 1: require complete categorical joint domain.  An omitted
        # original category must not silently become an observed zero.  The
        # producer must issue either a complete cross-product of native
        # category values or an explicit sparse-zero coverage proof.
        domain_size = 1
        for a in axes:
            domain_size *= len(a["category_map"])
        if len(seen) != domain_size:
            raise SynthesisError(
                "incomplete native joint domain; omitted category cannot be "
                "silently manufactured as zero (domain_size=%d, observed=%d)"
                % (domain_size, len(seen))
            )


def _mapping_reasons(source):
    reasons = []
    for a in source["axes"]:
        if a["review_status"] != "REVIEWED" or a["mapping_confidence"] != "HIGH":
            reasons.append("MAPPING_UNQUALIFIED")
        if a["scale_status"] != "REVIEWED" or a["polarity_status"] != "REVIEWED":
            reasons.append("SCALE_OR_POLARITY_UNQUALIFIED")
    return sorted(set(reasons))


def _mapped(source):
    tables = {}
    for z, native in source["strata"].items():
        table = {}
        for c in native["cells"]:
            key = tuple(a["category_map"][v] for a, v in zip(source["axes"], c["categories"]))
            table[key] = table.get(key, F(0)) + _q(c["mass"])
        tables[z] = table
    return tables


def _cells(table, category_order=None):
    if category_order is not None:
        index = {k: i for i, k in enumerate(category_order)}
        items = sorted(table.items(), key=lambda kv: index.get(kv[0], len(index)))
    else:
        items = sorted(table.items())
    return [{"categories": list(k), "probability": str(v)} for k, v in items]


def _baseline(source, expected_mapping_hash):
    reasons = _mapping_reasons(source)
    if expected_mapping_hash != semantic_hash(source["axes"]):
        reasons.append("MAPPING_REVIEW_PREIMAGE_MISMATCH")
    mapped = _mapped(source)
    aggregate = {}
    for table in mapped.values():
        for k, v in table.items():
            aggregate[k] = aggregate.get(k, F(0)) + v
    total = sum(aggregate.values(), F(0))
    return {"source_id": source["source_id"], "evidence_mode": "MEASURED" if reasons else "TRANSFORMED",
            "measured_parent_ref": source["product_ref"],
            "native_summary": deepcopy(source), "input_hash": semantic_hash(source),
            "target_applicability": "SOURCE_NATIVE_ONLY",
            "mapping_refusals": reasons,
            "mapped_joint": _cells({k: v / total for k, v in aggregate.items()}) if total and not reasons else None,
            "mapping_uncertainty": "UNKNOWN" if reasons else "REVIEWED_NOT_ERROR_FREE",
            "design_uncertainty": "EXTERNAL_DESIGN_VARIANCE_ONLY_OR_UNKNOWN"}


def synthesize(target: dict, sources: list[dict], policy: dict,
               admit: Callable[[dict, dict, str], bool] | None = None) -> dict:
    """Return native baseline plus one optional inferred target mixture.

    Real summaries need owner-verified admission for baseline AND transport. A
    callback is an integration boundary, not an authentication implementation.
    Unknown overlap excludes the candidate, while lawful baselines survive.
    """
    target, sources, policy = deepcopy((target, sources, policy))
    strata = _target_check(target)
    if not sources or len({s["source_id"] for s in sources}) != len(sources):
        raise SynthesisError("empty or duplicate source IDs")
    if set(policy["source_weights"]) != {s["source_id"] for s in sources}:
        raise SynthesisError("source weights must exactly name contributions")
    weights = {k: _number(v, low=0) for k, v in policy["source_weights"].items()}
    if any(w <= 0 for w in weights.values()):
        raise SynthesisError("remove a contribution explicitly instead of assigning zero")
    for k in ("policy_ref", "scope_review_ref", "conditional_invariance_ref", "target_support_ref"):
        _text(policy[k])
    if policy["conditional_invariance_status"] != "REVIEWED_ASSUMPTION":
        raise SynthesisError("transport requires an explicit reviewed invariance assumption")
    for k in ("mapping_bias_radius", "transport_bias_radius", "target_share_bias_radius"):
        _number(policy[k], high=1)
    if policy["minimum_raw_support"] < 1 or type(policy["minimum_raw_support"]) is not int:
        raise SynthesisError("invalid support threshold")
    if type(policy["maximum_joint_cells"]) is not int or policy["maximum_joint_cells"] < 1:
        raise SynthesisError("invalid joint-domain budget")
    for s in sources:
        _source_check(s)
        if not s["test_origin"] and (admit is None or admit(deepcopy(s), deepcopy(target), "SOURCE_INDEXED_BASELINE") is not True):
            raise SynthesisError("real source baseline lacks external owner admission")
    sources.sort(key=lambda s: s["source_id"])
    baseline = [_baseline(s, policy["mapping_hashes"].get(s["source_id"])) for s in sources]
    diagnostics = {b["source_id"]: list(b["mapping_refusals"]) for b in baseline}
    for s in sources:
        sid = s["source_id"]
        if any(s["scope"][k] != target[k] for k in ("geography", "boundary_ref", "population", "unit")):
            diagnostics[sid].append("TARGET_SCOPE_MISMATCH")
        if not s["scope"]["start_year"] <= target["year"] <= s["scope"]["end_year"]:
            diagnostics[sid].append("TIME_NOT_APPLICABLE")
        if not s["test_origin"] and admit(deepcopy(s), deepcopy(target), "TARGET_JOINT_STANDARDIZATION") is not True:
            diagnostics[sid].append("TRANSPORT_PERMISSION_NOT_ADMITTED")
    # An independent overlap review is required even when sample labels differ.
    overlap = []
    for i, a in enumerate(sources):
        for b in sources[i + 1:]:
            pair = "|".join(sorted((a["source_id"], b["source_id"])))
            review = policy["overlap_reviews"].get(pair, {})
            duplicate = (a["product_ref"] == b["product_ref"] or
                         (a["survey_lineage"], a["sample_id"]) == (b["survey_lineage"], b["sample_id"]))
            if duplicate or review.get("status") != "DISJOINT" or not review.get("review_ref"):
                overlap.append({"pair": pair, "reason": "DUPLICATE_SAMPLE" if duplicate else "OVERLAP_UNRESOLVED"})
    topology = [a["construct_ref"] for a in sources[0]["axes"]]
    category_sets = [set(a["category_map"].values()) for a in sources[0]["axes"]]
    # S03FO: declared category order from category_map insertion order
    declared_order = [list(dict.fromkeys(a["category_map"].values())) for a in sources[0]["axes"]]
    domain_size = 1
    for cats in category_sets:
        domain_size *= len(cats)
    for s in sources:
        if [a["construct_ref"] for a in s["axes"]] != topology or [set(a["category_map"].values()) for a in s["axes"]] != category_sets:
            diagnostics[s["source_id"]].append("NO_COMMON_JOINT_ESTIMAND_KEEP_COMPLEMENTARY_CHANNELS")
        if domain_size > policy["maximum_joint_cells"]:
            diagnostics[s["source_id"]].append("JOINT_DOMAIN_EXCEEDS_BUDGET")
    out = {"contract_version": METHOD, "world_scope": target, "baseline": baseline,
           "candidate": None, "refusals": diagnostics, "overlap_diagnostics": overlap,
           "test_origin": all(s["test_origin"] for s in sources),
           "real_source_qualification": "EXTERNAL_REVIEW_REQUIRED",
           "replay": {"target": target, "sources": sources, "policy": policy},
           "consumer_requirements_ref": "S03_CONSUMER_REQUIREMENTS@1"}
    out["evidence_graph"] = []
    for s, b in zip(sources, baseline):
        native_id = "native:" + s["source_id"]
        out["evidence_graph"].append({"node_id": native_id, "evidence_mode": "MEASURED",
            "test_origin": s["test_origin"], "producer_ref": s["product_ref"], "parents": [],
            "value_ref": "baseline/" + s["source_id"] + "/native_summary", "value_hash": b["input_hash"],
            "authority_ceiling": "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE"})
        if b["mapped_joint"] is not None:
            out["evidence_graph"].append({"node_id": "mapped:" + s["source_id"],
                "evidence_mode": "TRANSFORMED", "test_origin": s["test_origin"], "parents": [native_id],
                "method": "REVIEWED_CATEGORY_RECODING@1", "mapping_hash": semantic_hash(s["axes"]),
                "value_ref": "baseline/" + s["source_id"] + "/mapped_joint"})
    if overlap or any(diagnostics.values()):
        out["decision"] = "SOURCE_INDEXED_BACKOFF"
        out["content_hash"] = semantic_hash(out)
        return out
    mapped = {s["source_id"]: _mapped(s) for s in sources}
    keys = list(product(*declared_order))
    joint = {k: F(0) for k in keys}
    lower = {k: F(0) for k in keys}
    upper = {k: F(0) for k in keys}
    variances = {k: F(0) for k in keys}
    unknown_variance = False
    coverage, uncovered = {}, F(0)
    for z, share in sorted(strata.items()):
        if not share:
            continue
        eligible = []
        for s in sources:
            sid = s["source_id"]
            t = s["strata"].get(z)
            if t and sum(c["n"] for c in t["cells"]) >= policy["minimum_raw_support"] and sum(mapped[sid][z].values()) > 0:
                eligible.append(s)
        denom = sum(weights[s["source_id"]] for s in eligible)
        coverage[z] = {"target_share": str(share), "sources": [], "excluded_sources": [s["source_id"] for s in sources if s not in eligible]}
        if not denom:
            uncovered += share
            unknown_variance = True
            for k in keys:
                upper[k] += share
            continue
        distributions = []
        for s in eligible:
            sid = s["source_id"]
            alpha = weights[sid] / denom
            table = mapped[sid][z]
            mass = sum(table.values())
            p = {k: table.get(k, F(0)) / mass for k in keys}
            distributions.append(p)
            coverage[z]["sources"].append({"source_id": sid, "coefficient": str(share * alpha),
                                            "conditional_source_weight": str(alpha),
                                            "raw_support": sum(c["n"] for c in s["strata"][z]["cells"]),
                                            "weighted_support": str(mass), "support_ref": s["strata"][z]["support_ref"]})
            native_mass = sum(sum(t.values()) for t in mapped[sid].values())
            coverage[z]["sources"][-1].update(native_stratum_share=str(mass / native_mass),
                                               target_to_native_share_ratio=str(share * native_mass / mass))
            v = s["strata"][z].get("design_variance")
            if v is None:
                unknown_variance = True
            else:
                _text(v["method_ref"])
                # Variances must already be for the mapped cell probabilities.
                supplied = {tuple(c["categories"]): _number(c["variance"], high=1) for c in v["cells"]}
                if len(supplied) != len(v["cells"]) or set(supplied) != set(keys):
                    raise SynthesisError("design variance coverage must match mapped joint")
                for k in keys:
                    variances[k] += (share * alpha) ** 2 * supplied[k]
            for k in keys:
                joint[k] += share * alpha * p[k]
        for k in keys:
            lower[k] += share * min(p[k] for p in distributions)
            upper[k] += share * max(p[k] for p in distributions)
    radius = sum(_q(policy[k]) for k in ("mapping_bias_radius", "transport_bias_radius", "target_share_bias_radius"))
    candidate = {"evidence_mode": "INFERRED", "method": METHOD, "construct_topology": topology,
                 "parent_refs": [s["product_ref"] for s in sources], "assumptions_ref": policy["policy_ref"],
                 "ordered_categories": [list(k) for k in keys],
                 "distribution": _cells(joint, keys) if uncovered == 0 else None,
                 "covered_subprobability": _cells(joint, keys), "uncovered_target_mass": str(uncovered),
                 "support": coverage, "sample_size": None,
                 "dependence": "SOURCE_JOINTS_TRANSPORTED_AND_MIXED; NO_CROSS_SURVEY_RESPONDENT_LINKS",
                 "uncertainty": {"sampling_variance": None if unknown_variance else [{"categories": list(k), "variance": str(v)} for k, v in sorted(variances.items())],
                                 "sampling_status": "UNKNOWN_DESIGN" if unknown_variance else "EXTERNAL_DESIGN_DIAGONAL_ONLY",
                                 "source_disagreement_and_uncovered_bounds": [{"categories": list(k), "lower": str(lower[k]), "upper": str(upper[k])} for k in keys],
                                 "bias_sensitivity_bounds": [{"categories": list(k), "lower": str(max(F(0), lower[k] - radius)), "upper": str(min(F(1), upper[k] + radius))} for k in keys],
                                 "radii": {k: policy[k] for k in ("mapping_bias_radius", "transport_bias_radius", "target_share_bias_radius")},
                                 "limitations": "Sensitivity envelopes are not confidence intervals; fixed target shares and disjoint sources/strata for sampling variance; covariance and conditional uncertainty unavailable."}}
    out["candidate"] = candidate
    out["evidence_graph"].append({"node_id": "target_joint", "evidence_mode": "INFERRED",
        "test_origin": out["test_origin"], "parents": ["mapped:" + s["source_id"] for s in sources],
        "method": METHOD, "parameters_hash": semantic_hash(policy),
        "value_ref": "candidate", "value_hash": semantic_hash(candidate),
        "authority_ceiling": "DESCRIPTIVE_SOCIOLOGICAL_MODEL_ONLY"})
    out["decision"] = "SYNTHETIC_CANDIDATE" if out["test_origin"] else "INFERRED_CANDIDATE_REQUIRES_REVIEW"
    out["content_hash"] = semantic_hash(out)
    return out


def conditional(bundle: dict, conditions: dict[str, str], outcome: str) -> dict:
    """Value-reading sociological consumer; cumulative predicates on one joint.

    This is a contract consumer only, not Worker 1's selected-world service.
    No conditional uncertainty is inferred from diagonal marginal variances.
    """
    material = {k: v for k, v in bundle.items() if k != "content_hash"}
    if bundle.get("content_hash") != semantic_hash(material):
        raise SynthesisError("bundle replay hash mismatch")
    c = bundle.get("candidate")
    if c is None or c["distribution"] is None:
        return {"state": "UNAVAILABLE", "reason": "NO_COMPLETE_TARGET_JOINT", "bundle_hash": bundle["content_hash"]}
    axes = c["construct_topology"]
    if outcome not in axes or any(k not in axes for k in conditions):
        raise SynthesisError("condition/outcome outside common joint topology")
    if any(v not in {cell["categories"][axes.index(k)] for cell in c["distribution"]}
           for k, v in conditions.items()):
        return {"state": "UNAVAILABLE", "reason": "CATEGORY_OUTSIDE_MAPPED_SUPPORT", "bundle_hash": bundle["content_hash"]}
    selected = [cell for cell in c["distribution"] if all(cell["categories"][axes.index(k)] == v for k, v in conditions.items())]
    denom = sum((_q(cell["probability"]) for cell in selected), F(0))
    table = {}
    for cell in selected:
        v = cell["categories"][axes.index(outcome)]
        table[v] = table.get(v, F(0)) + _q(cell["probability"])
    # S03F Fix 2: outcome-as-conditioning-predicate must not masquerade as
    # a nontrivial predictive conditional.  Return a strictly descriptive
    # self-conditioning status, not generic predictive SUPPORTED_MODEL.
    self_conditioning = outcome in conditions
    if self_conditioning and denom:
        state = "DESCRIPTIVE_SELF_CONDITIONING"
        self_cond_status = "OUTCOME_LEAKAGE_TAUTOLOGY"
    elif self_conditioning:
        state = "ZERO_MODEL_SUPPORT"
        self_cond_status = "OUTCOME_LEAKAGE_TAUTOLOGY"
    else:
        state = "SUPPORTED_MODEL" if denom else "ZERO_MODEL_SUPPORT"
        self_cond_status = None
    result = {"state": state,
              "evidence_mode": "INFERRED", "conditions": conditions, "outcome": outcome,
              "probabilities": _distribution(table), "model_denominator_mass": str(denom),
              "observed_denominator": None, "uncertainty": "CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED",
              "bundle_hash": bundle["content_hash"], "values_read_hash": semantic_hash(c["distribution"])}
    if self_cond_status is not None:
        result["self_conditioning_status"] = self_cond_status
    result["output_hash"] = semantic_hash(result)
    return result


def complementary_binary_bounds(p, q):
    """Unidentified cross-channel event intersection; never an observed joint."""
    p, q = _number(p, high=1), _number(q, high=1)
    return {"evidence_mode": "INFERRED", "dependence": "UNIDENTIFIED",
            "lower": str(max(F(0), p + q - 1)), "upper": str(min(p, q)),
            "independence_scenario": str(p * q), "scenario_is_measured": False}
