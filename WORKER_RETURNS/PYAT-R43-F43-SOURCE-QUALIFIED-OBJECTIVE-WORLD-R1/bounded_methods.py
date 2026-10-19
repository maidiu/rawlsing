"""F43 method candidates. Mathematical constraints never authenticate source rights.

The rational outputs are identification/sensitivity sets conditional on input
summaries and stated assumptions. They are not sampling confidence intervals.
Only synthetic method evaluation is exposed by this candidate implementation.
"""
from datetime import date
from fractions import Fraction as Q
import math


class MethodError(ValueError):
    pass


def q(value, *, unit=False):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise MethodError('EXACT_RATIONAL_REQUIRED')
    try:
        out = Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise MethodError('EXACT_RATIONAL_REQUIRED') from exc
    if out < 0 or (unit and out > 1):
        raise MethodError('MASS_OUTSIDE_DOMAIN')
    return out


def partial_conditional(covered, unknown, axes, conditions, outcome):
    """Sharp categorywise bounds with unrestricted allocation of missing mass.

    a is covered mass satisfying Y=y,C; b is covered mass satisfying C; u is
    uncovered total target mass. Endpoints are a/(b+u),(a+u)/(b+u).
    Each category's endpoint is attainable, but all upper endpoints need not
    be jointly attainable. Zero measured C and u=0 leaves an undefined ratio.
    """
    u = q(unknown, unit=True)
    if not axes or len(set(axes)) != len(axes):
        raise MethodError('INVALID_TOPOLOGY')
    if outcome not in axes or any(k not in axes for k in conditions):
        raise MethodError('OUTSIDE_TOPOLOGY')
    if outcome in conditions:
        raise MethodError('SELF_CONDITIONING')
    cells = {}
    for cell in covered:
        key = tuple(cell['categories'])
        if len(key) != len(axes) or key in cells:
            raise MethodError('DUPLICATE_OR_MALFORMED_CELL')
        cells[key] = q(cell['probability'], unit=True)
    if sum(cells.values(), Q(0)) + u != 1:
        raise MethodError('UNCOVERED_MASS_NOT_CONSERVED')
    for k, v in conditions.items():
        if v not in {key[axes.index(k)] for key in cells}:
            raise MethodError('CATEGORY_OUTSIDE_SUPPORT')
    labels = sorted({key[axes.index(outcome)] for key in cells})
    if len(labels) < 2:
        raise MethodError('NONTRIVIAL_OUTCOME_DOMAIN_REQUIRED')
    selected = {key: mass for key, mass in cells.items()
                if all(key[axes.index(k)] == v for k, v in conditions.items())}
    b = sum(selected.values(), Q(0))
    if b + u == 0:
        return dict(state='UNDEFINED_ZERO_CONDITION_MASS', bounds=None,
                    supported_point=None, uncovered_target_mass=str(u))
    bounds = {}
    for label in labels:
        a = sum((mass for key, mass in selected.items()
                 if key[axes.index(outcome)] == label), Q(0))
        bounds[label] = dict(lower=str(a / (b + u)), upper=str((a + u) / (b + u)),
                             covered_event_mass=str(a))
    return dict(state='PARTIAL_CONDITIONAL_IDENTIFICATION' if u else 'COMPLETE_TEST_CONDITIONAL',
                covered_condition_mass=str(b), uncovered_target_mass=str(u), bounds=bounds,
                supported_point=None if u else {k: x['lower'] for k, x in bounds.items()},
                uncertainty='IDENTIFICATION_ONLY_NOT_SAMPLING_CI',
                joint_attainability='CATEGORYWISE_ENDPOINTS_NOT_ONE_JOINT_DISTRIBUTION',
                real_use_authorized=False, route_probability=None)


def missing_sensitivity(a, b, u, *, missing_condition_share, missing_event_given_condition):
    """Explicit hypothetical allocation; no renormalization of covered target."""
    a, b, u = q(a, unit=True), q(b, unit=True), q(u, unit=True)
    r, theta = q(missing_condition_share, unit=True), q(missing_event_given_condition, unit=True)
    if a > b or b + u > 1:
        raise MethodError('INVALID_COVERED_EVENT_MASS')
    denominator = b + u*r
    return dict(value=str((a + u*r*theta)/denominator) if denominator else None,
                missing_condition_share=str(r), missing_event_given_condition=str(theta),
                grade='HYPOTHETICAL_SENSITIVITY_NOT_IDENTIFIED_POINT',
                sampling_uncertainty=None, real_use_authorized=False)


def marginal_joint_bounds(p, r):
    """Frechet bounds for two binary margins ALREADY on one target population.

    Distinct surveys can supply margins only after independent population,
    estimand, transport and source rights qualification. This function performs
    no such qualification and claims no observed respondents or measured joint.
    """
    p, r = q(p, unit=True), q(r, unit=True)
    lo, hi = max(Q(0), p+r-1), min(p, r)
    return dict(intersection=dict(lower=str(lo), upper=str(hi)),
                conditional=None if r == 0 else dict(lower=str(lo/r), upper=str(hi/r)),
                independence_scenario=str(p*r), scenario_is_measured=False,
                target_compatibility='EXTERNAL_PRECONDITION_NOT_ESTABLISHED_HERE',
                observed_respondent_join=False, route_probability=None,
                grade='SOURCEFREE_METHOD_DEMONSTRATION')


IDENTITY = ('target_population', 'estimand', 'response_topology',
            'wording_signature', 'design_signature')


def strict_temporal_gate(periods, as_of, native_owner):
    """Pre-guard EE1/V553. Equal missing metadata never proves comparability.

    Does not admit measured source comparisons, fabricate overlays or issue a
    harmonization equivalence. Different designs may be qualified externally;
    this candidate only accepts the inherited exact-key branch.
    """
    if len(periods) != 2:
        return dict(state='TWO_EXACT_PERIODS_REQUIRED')
    try:
        cutoff = date.fromisoformat(as_of)
    except (TypeError, ValueError):
        return dict(state='INVALID_ASOF_DATE')
    required = (*IDENTITY, 'source', 'wave', 'country_code')
    missing = sorted({k for p in periods for k in required
                      if not isinstance(p.get(k), str) or not p[k].strip()})
    if missing:
        return dict(state='UNKNOWN_TEMPORAL_IDENTITY', missing=missing)
    for p in periods:
        if type(p.get('observation_year')) is not int or type(p.get('temporal_year')) is not int:
            return dict(state='UNKNOWN_OBSERVATION_TIME')
        if p['observation_year'] != p['temporal_year']:
            return dict(state='OBSERVATION_ANCHOR_MISMATCH')
        if p['observation_year'] > cutoff.year:
            return dict(state='OBSERVATION_AFTER_AS_OF')
        for key in ('evidence_publication', 'rule_publication'):
            try:
                stamp = date.fromisoformat(p[key])
            except (KeyError, TypeError, ValueError):
                return dict(state='UNKNOWN_PUBLICATION_TIME', field=key)
            if stamp > cutoff:
                return dict(state='FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF' if key == 'evidence_publication'
                            else 'FUTURE_RULE_AT_HISTORICAL_AS_OF', field=key)
    identity = native_owner.identity_report(periods)
    if identity['state'] != 'IDENTITY_OK':
        return identity
    result = native_owner.population_estimand_gate(periods)
    return dict(result, source_comparison_authorized=False,
                candidate_scope='EXACT_KEY_SOURCEFREE_GATE_ONLY')


def design_change(before, after, variance_before, variance_after, *, covariance=None,
                  independent=False):
    """Test-only difference and design uncertainty; never infer independence.

    Unknown cross-wave covariance permits a standard-error range by Cauchy-
    Schwarz, not an invented point standard error. Input variances must be
    supplied by the survey-design owner; a sample size cannot replace them.
    """
    left, right = q(before, unit=True), q(after, unit=True)
    delta = right-left
    if variance_before is None or variance_after is None:
        return dict(delta=str(delta), sampling_state='UNKNOWN_SURVEY_DESIGN_VARIANCE',
                    standard_error=None, confidence_interval=None,
                    grade='SOURCEFREE_METHOD_DEMONSTRATION')
    va, vb = q(variance_before), q(variance_after)
    root = math.sqrt(float(va*vb))
    if independent and covariance not in (None, 0, '0'):
        raise MethodError('INDEPENDENCE_COVARIANCE_CONTRADICTION')
    if independent:
        covariance = '0'
    if covariance is None:
        a, b = math.sqrt(float(va)), math.sqrt(float(vb))
        return dict(delta=str(delta), sampling_state='COVARIANCE_UNKNOWN',
                    standard_error=None, standard_error_range=[abs(a-b), a+b],
                    confidence_interval=None, grade='SOURCEFREE_METHOD_DEMONSTRATION')
    if isinstance(covariance, bool) or not isinstance(covariance, (str, int)):
        raise MethodError('EXACT_COVARIANCE_REQUIRED')
    try:
        cov = Q(covariance)
    except (ValueError, ZeroDivisionError) as exc:
        raise MethodError('EXACT_COVARIANCE_REQUIRED') from exc
    if cov*cov > va*vb:
        raise MethodError('INFEASIBLE_COVARIANCE')
    variance = va+vb-2*cov
    se = math.sqrt(float(variance))
    return dict(delta=str(delta), variance_of_difference=str(variance), standard_error=se,
                normal_approximation_95=[max(-1, float(delta)-1.959963984540054*se),
                                         min(1, float(delta)+1.959963984540054*se)],
                sampling_state='DESIGN_VARIANCE_AND_COVARIANCE_SUPPLIED',
                approximation='NORMAL_APPROXIMATION_REQUIRES_DESIGN_OWNER_QUALIFICATION',
                grade='SOURCEFREE_METHOD_DEMONSTRATION')
