"""F6P — source-free partial-bound evidence consumer over the ACTUAL F6M bundle.

This module is a consumer, not a producer, not an issuer and not a route model.
It reads the exact bundle returned by the accepted F6M producer and exposes the
evidence the F6M contract actually supports:

* adequately measured, complete target synthesis;
* incomplete target coverage / lost planned source share;
* partially identified marginal bounds, with no point;
* completely unidentified joint;
* unverified transport and prohibited model-use refusals;
* source-specific exclusion;
* incompatible populations, strata or respondent identities;
* self-conditioning (outcome-as-own-condition) refusal;
* missing design/weight evidence, never imputed as weight 1.

It never issues route_probability or selection_weight, never invents a common
respondent, and never promotes an experimental bundle to real use.
"""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NATIVE = ROOT / "native"
if str(NATIVE) not in sys.path:
    sys.path.insert(0, str(NATIVE))

from rawlsing_next import pre553_heterogeneous_synthesis as f6m  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

SCHEMA = "F6P_PARTIAL_BOUND_EVIDENCE@1"
CONSUMER_ID = "F6P_F6M_PARTIAL_BOUND_CONSUMER@1"
SCIENTIFIC_CEILING = (
    "SOURCEFREE_TEST_ONLY_NO_ROUTE_PROBABILITY_NO_SELECTION_WEIGHT_NO_MODEL_USE"
)

SUPPORTED = "SUPPORTED_SYNTHESIS"
PARTIAL = "PARTIAL_IDENTIFICATION"
UNIDENTIFIED = "UNIDENTIFIED_JOINT"
SOURCE_EXCLUDED = "SOURCE_EXCLUDED"
FALSE_FULL = "FALSE_FULL_COVERAGE"
INCONSISTENT = "PRODUCT_INCONSISTENT"
SELF_CONDITIONING = "SELF_CONDITIONING"
CATEGORY_OUTSIDE = "CATEGORY_OUTSIDE_SUPPORT"
INCOMPATIBLE_RESPONDENT = "INCOMPATIBLE_RESPONDENT"
INCOMPATIBLE_POPULATION = "INCOMPATIBLE_POPULATION_OR_STRATUM"
WRONG_VERSION = "WRONG_SOURCE_VERSION"
UNVERIFIED_TRANSPORT = "UNVERIFIED_TRANSPORT"
INCOMPLETE_DOMAIN = "INCOMPLETE_NATIVE_JOINT_DOMAIN"
WEIGHT_UNKNOWN = "WEIGHT_OR_DESIGN_UNKNOWN"
PROHIBITED = "PROHIBITED_MODEL_USE"
REVOKED = "REVOKED_EVIDENCE"


class ConsumerRefusal(Exception):
    """Typed refusal at the consumer boundary; never a silent fallback."""


def _q(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ConsumerRefusal("NON_RATIONAL_VALUE")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ConsumerRefusal("NON_RATIONAL_VALUE") from exc


def _cell_map(cells):
    out = {}
    for cell in cells or []:
        key = "|".join(cell["categories"])
        out[key] = cell["probability"]
    return out


def _flatten_refusals(refusals):
    reasons = []
    for source_id, values in (refusals or {}).items():
        for value in values or []:
            reasons.append((source_id, value))
    return reasons


def _exclusions(candidate):
    out = []
    for stratum, spec in (candidate.get("support") or {}).items():
        reasons = spec.get("exclusion_reasons") or {}
        for source_id in spec.get("excluded_sources") or []:
            out.append({
                "stratum": stratum,
                "source_id": source_id,
                "reason": reasons.get(source_id, "UNKNOWN"),
                "uncovered_target_share": spec.get("uncovered_target_share"),
                "planned_source_share_lost": spec.get("uncovered_target_share"),
            })
    return out


def _source_ids(candidate, bundle):
    ids = set()
    for stratum, spec in (candidate.get("support") or {}).items():
        for row in spec.get("sources") or []:
            ids.add(row["source_id"])
        for source_id in spec.get("excluded_sources") or []:
            ids.add(source_id)
    for parent in candidate.get("parent_refs") or []:
        if isinstance(parent, dict) and parent.get("source_id"):
            ids.add(parent["source_id"])
    for parent in bundle.get("evidence_graph") or []:
        if isinstance(parent, dict) and parent.get("source_id"):
            ids.add(parent["source_id"])
    return ids


def _git_blob(path):
    raw = Path(path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def verify_f6m_bundle(bundle):
    """Verify the exact F6M replay identity. A fixture without this fails."""
    if not isinstance(bundle, dict):
        raise ConsumerRefusal("NOT_AN_F6M_BUNDLE")
    if bundle.get("real_use_authorized") is True:
        raise ConsumerRefusal("FORGED_MODEL_USE_ADMISSION")
    material = {k: v for k, v in bundle.items() if k != "content_hash"}
    actual = semantic_hash(material)
    if bundle.get("content_hash") != actual:
        raise ConsumerRefusal("BUNDLE_REPLAY_MISMATCH")
    text = json.dumps(bundle, sort_keys=True)
    if '"route_probability"' in text or '"selection_weight"' in text:
        raise ConsumerRefusal("PROHIBITED_FIELD_IN_PRODUCT")
    if bundle.get("owner_admission_status") not in (
            None, "UNVERIFIED_INTEGRATION_BOUNDARY"):
        raise ConsumerRefusal("FORGED_OWNER_ADMISSION")
    return actual


def _conditional(bundle, request):
    conditions = request.get("conditions")
    outcome = request.get("outcome")
    if conditions is None or outcome is None:
        return None
    try:
        return f6m.conditional(bundle, dict(conditions), outcome,
                              use="SOURCEFREE_EXPERIMENT")
    except f6m.SynthesisError as exc:
        raise ConsumerRefusal("F6M_CONDITIONAL_REFUSED:" + str(exc)) from exc


def _sampling(candidate, request):
    uncertainty = candidate.get("uncertainty") or {}
    status = uncertainty.get("sampling_status")
    variance = uncertainty.get("sampling_variance")
    design_known = status == "EXTERNAL_DESIGN_DIAGONAL_ONLY" and variance is not None
    wants_population = request.get("requested_use") == "POPULATION_ESTIMATE"
    return {
        "sampling_status": status,
        "sampling_variance_present": variance is not None,
        "design_known": design_known,
        "population_estimate_requested": wants_population,
        "population_estimate_permitted": bool(design_known),
        "weight_defaulted_to_one": False,
        "weight_imputation": "NONE",
        "note": "unknown design/weight is exposed as unknown, never set to 1",
    }


def _state_from_refusals(reasons):
    values = {r[1] for r in reasons}
    if "TARGET_SCOPE_MISMATCH" in values:
        return INCOMPATIBLE_POPULATION, "TARGET_SCOPE_MISMATCH"
    if "NO_COMMON_JOINT_ESTIMAND" in values:
        return INCOMPATIBLE_POPULATION, "NO_COMMON_JOINT_ESTIMAND"
    if "TIME_NOT_APPLICABLE" in values:
        return WRONG_VERSION, "TIME_NOT_APPLICABLE"
    if "JOINT_DOMAIN_EXCEEDS_BUDGET" in values:
        return INCOMPLETE_DOMAIN, "JOINT_DOMAIN_EXCEEDS_BUDGET"
    if "TRANSPORT_PERMISSION_NOT_ADMITTED" in values:
        return UNVERIFIED_TRANSPORT, "TRANSPORT_PERMISSION_NOT_ADMITTED"
    return None, None


def consume_f6m_evidence(bundle, request=None):
    """Consume the actual F6M product; return typed evidence, never a new right."""
    request = dict(request or {})
    use = request.get("use", "SOURCEFREE_EXPERIMENT")
    if use not in ("SOURCEFREE_EXPERIMENT", "TEST_ONLY"):
        return _result(bundle, request, PROHIBITED,
                       ["MODEL_USE_NOT_ADMITTED_BY_EXISTING_OWNERS"], None)
    if request.get("admission") or request.get("transport_permission"):
        return _result(bundle, request, PROHIBITED,
                       ["SELF_DECLARED_MODEL_USE_OR_TRANSPORT_ADMISSION"], None)

    bundle_hash = verify_f6m_bundle(bundle)
    candidate = bundle.get("candidate")
    if candidate is None:
        overlap = bundle.get("overlap_diagnostics") or []
        if overlap:
            return _result(bundle, request, INCOMPATIBLE_RESPONDENT,
                           ["DUPLICATE_OR_FICTITIOUS_COMMON_RESPONDENTS"], None,
                           overlap=overlap)
        state, reason = _state_from_refusals(_flatten_refusals(bundle.get("refusals")))
        if state:
            return _result(bundle, request, state, [reason], None)
        return _result(bundle, request, UNIDENTIFIED, ["NO_CANDIDATE_JOINT"], None)

    source_ids = _source_ids(candidate, bundle)
    revoked = set(request.get("revoked_source_ids") or []) & source_ids
    if revoked:
        return _result(bundle, request, REVOKED,
                       ["REVOKED_SOURCE:" + "|".join(sorted(revoked))], candidate)

    overlap = bundle.get("overlap_diagnostics") or []
    if overlap:
        return _result(bundle, request, INCOMPATIBLE_RESPONDENT,
                       ["DUPLICATE_OR_FICTITIOUS_COMMON_RESPONDENTS"], candidate,
                       overlap=overlap)

    state, reason = _state_from_refusals(_flatten_refusals(bundle.get("refusals")))
    if state in (INCOMPATIBLE_POPULATION, WRONG_VERSION, INCOMPLETE_DOMAIN, UNVERIFIED_TRANSPORT):
        return _result(bundle, request, state, [reason], candidate)

    uncovered = _q(candidate["uncovered_target_mass"])
    covered_cells = candidate.get("covered_subprobability") or []
    covered_sum = sum((_q(c["probability"]) for c in covered_cells), F(0))
    distribution = candidate.get("distribution")
    exclusions = _exclusions(candidate)

    if covered_sum + uncovered != 1:
        return _result(bundle, request, INCONSISTENT,
                       ["COVERED_AND_UNCOVERED_MASS_DO_NOT_CONSERVE"], candidate)
    if distribution is not None and uncovered != 0:
        return _result(bundle, request, INCONSISTENT,
                       ["COMPLETE_DISTRIBUTION_WITH_UNCOVERED_MASS"], candidate)
    if distribution is None and uncovered == 0:
        return _result(bundle, request, INCONSISTENT,
                       ["NO_DISTRIBUTION_WITH_ZERO_UNCOVERED_MASS"], candidate)
    if exclusions and uncovered == 0:
        return _result(bundle, request, FALSE_FULL,
                       ["EXCLUDED_SOURCE_WITH_ZERO_UNCOVERED_MASS"], candidate)
    if covered_sum == 0 and exclusions:
        return _result(bundle, request, SOURCE_EXCLUDED,
                       ["ALL_SOURCE_CONTRIBUTIONS_EXCLUDED"], candidate)

    complete = distribution is not None and uncovered == 0
    expected_decision = ("SYNTHETIC_CANDIDATE" if complete
                         else "PARTIAL_IDENTIFICATION_ONLY")
    expected_status = ("COMPLETE_EXPERIMENTAL_TARGET_JOINT" if complete
                       else "NO_COMPLETE_TARGET_JOINT")
    if (bundle.get("decision") != expected_decision
            or bundle.get("target_joint_status") != expected_status):
        return _result(bundle, request, INCONSISTENT,
                       ["DECISION_OR_TARGET_STATUS_DOES_NOT_MATCH_COVERAGE"], candidate)

    conditional = _conditional(bundle, request)
    if conditional is not None:
        cond_state = conditional.get("state")
        if conditional.get("self_conditioning_status") == "OUTCOME_LEAKAGE_TAUTOLOGY":
            return _result(bundle, request, SELF_CONDITIONING,
                           ["OUTCOME_LEAKAGE_TAUTOLOGY"], candidate,
                           conditional=conditional)
        if cond_state == "UNAVAILABLE" and conditional.get("reason") == "CATEGORY_OUTSIDE_MAPPED_SUPPORT":
            return _result(bundle, request, CATEGORY_OUTSIDE,
                           ["CATEGORY_OUTSIDE_MAPPED_SUPPORT"], candidate,
                           conditional=conditional)

    sampling = _sampling(candidate, request)
    if sampling["population_estimate_requested"] and not sampling["design_known"]:
        return _result(bundle, request, WEIGHT_UNKNOWN,
                       ["UNKNOWN_DESIGN_OR_WEIGHT_FOR_POPULATION_ESTIMATE"], candidate,
                       conditional=conditional, sampling=sampling)

    if uncovered > 0:
        return _result(bundle, request, PARTIAL,
                       ["INCOMPLETE_TARGET_COVERAGE"], candidate,
                       conditional=conditional, sampling=sampling)
    if conditional is not None and conditional.get("state") == "SUPPORTED_MODEL":
        return _result(bundle, request, SUPPORTED,
                       ["COMPLETE_MEASURED_TARGET_JOINT"], candidate,
                       conditional=conditional, sampling=sampling)
    if conditional is not None and conditional.get("state") == "UNAVAILABLE":
        return _result(bundle, request, UNIDENTIFIED,
                       [conditional.get("reason", "CONDITIONAL_UNAVAILABLE")], candidate,
                       conditional=conditional, sampling=sampling)
    return _result(bundle, request, SUPPORTED,
                   ["COMPLETE_MEASURED_TARGET_JOINT"], candidate,
                   conditional=conditional, sampling=sampling)


def _result(bundle, request, state, reasons, candidate, *, conditional=None,
            sampling=None, overlap=None):
    covered = _cell_map((candidate or {}).get("covered_subprobability") or [])
    bounds = ((candidate or {}).get("uncertainty") or {}).get(
        "source_disagreement_and_uncovered_bounds") or []
    bias = ((candidate or {}).get("uncertainty") or {}).get(
        "bias_sensitivity_bounds") or []
    exclusions = _exclusions(candidate or {})
    uncertainty = (candidate or {}).get("uncertainty")
    point = None
    if state == SUPPORTED and conditional is not None:
        point = conditional.get("probabilities")
    result = {
        "schema": SCHEMA,
        "consumer_id": CONSUMER_ID,
        "evidence_state": state,
        "evidence_reasons": reasons,
        "request": dict(request),
        "input_bundle": {
            "content_hash": (bundle or {}).get("content_hash"),
            "implementation_version": (bundle or {}).get("implementation_version"),
            "decision": (bundle or {}).get("decision"),
            "target_joint_status": (bundle or {}).get("target_joint_status"),
            "test_origin": (bundle or {}).get("test_origin"),
            "use_scope": (bundle or {}).get("use_scope"),
            "owner_admission_status": (bundle or {}).get("owner_admission_status"),
            "real_use_authorized": (bundle or {}).get("real_use_authorized"),
        },
        "source_product": {
            "module_file": str(f6m.__file__),
            "module_sha256": hashlib.sha256(Path(f6m.__file__).read_bytes()).hexdigest(),
            "module_git_blob": _git_blob(f6m.__file__),
        },
        "covered_subprobability": covered,
        "uncovered_target_mass": (candidate or {}).get("uncovered_target_mass"),
        "bounds": bounds,
        "bias_sensitivity_bounds": bias,
        "supported_point": point,
        "conditional": conditional,
        "exclusions": exclusions,
        "lost_planned_source_share": exclusions,
        "overlap": overlap or [],
        "sampling": sampling or {
            "weight_defaulted_to_one": False,
            "weight_imputation": "NONE",
            "note": "no sampling block read",
        },
        "transport": {
            "status": "UNVERIFIED_INTEGRATION_BOUNDARY",
            "permitted": False,
            "note": "no owner transport/model-use permission is issued by this consumer",
        },
        "uncertainty": uncertainty,
        "values_read": [
            "content_hash", "decision", "target_joint_status", "candidate",
            "candidate.covered_subprobability", "candidate.uncovered_target_mass",
            "candidate.support", "candidate.uncertainty",
            "candidate.uncertainty.source_disagreement_and_uncovered_bounds",
            "candidate.uncertainty.sampling_status", "refusals",
            "overlap_diagnostics", "conditional",
        ],
        "no_route_probability": True,
        "no_selection_weight": True,
        "no_common_respondent_inference": True,
        "real_use_authorized": False,
        "scientific_ceiling": SCIENTIFIC_CEILING,
    }
    result["output_hash"] = semantic_hash(
        {k: v for k, v in result.items() if k != "output_hash"})
    return result
