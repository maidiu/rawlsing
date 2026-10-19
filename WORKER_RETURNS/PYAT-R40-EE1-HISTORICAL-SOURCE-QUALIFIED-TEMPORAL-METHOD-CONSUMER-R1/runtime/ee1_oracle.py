"""Independent EE1 comparison oracle.

Deliberately implements the frozen comparability contract from first
principles.  It imports NOTHING from `data.ddm_build_copy`, NOTHING from
`rawlsing_next`, and NOTHING from the EE1 bridge: it exists so that
wrong-source or wrong-clock crossovers are caught independently of the
machinery under test.
"""
from __future__ import annotations

FIELDS = ("target_population", "estimand", "response_topology",
          "wording_signature", "design_signature")


def _norm(value) -> str:
    return " ".join(str(value).strip().upper().split())


def oracle_verdict(periods, comparison_asof) -> str:
    families = {_norm(p["source"]) for p in periods}
    if len(families) != 1:
        return "NONCOMPARABLE_SOURCE_FAMILY"
    countries = {_norm(p["country_code"]) for p in periods}
    if len(countries) != 1:
        return "NONCOMPARABLE_COUNTRY"
    years = [int(p["temporal_year"]) for p in periods]
    if len(set(years)) != len(years):
        return "DUPLICATE_YEAR_ANCHOR"
    signatures = {tuple(_norm(p.get(field, "")) for field in FIELDS)
                  for p in periods}
    if len(signatures) != 1:
        return "NONCOMPARABLE_POPULATION_OR_ESTIMAND"
    asof = str(comparison_asof)
    for period in periods:
        if str(period.get("rule_publication", "")) > asof and \
                period.get("rule_vintage") != "rev1_selected":
            return "FUTURE_RULE_AT_HISTORICAL_AS_OF"
        if str(period.get("evidence_publication", "")) > asof:
            return "FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF"
        if int(period["observation_year"]) > int(asof[:4]):
            return "OBSERVATION_AFTER_AS_OF"
    if any(p.get("annual_anchors_required") for p in periods):
        span = set(range(min(years), max(years) + 1))
        if span != set(years):
            return "UNKNOWN_GAP"
    return "COMPARABLE"


BRIDGE_FAMILY = {
    "COMPARABLE": {"COMPARABLE_AUTHORIZED", "COMPARABLE_PROBE_ONLY"},
    "NONCOMPARABLE_SOURCE_FAMILY": {"NONCOMPARABLE_SOURCE_FAMILY"},
    "NONCOMPARABLE_COUNTRY": {"NONCOMPARABLE_COUNTRY"},
    "NONCOMPARABLE_POPULATION_OR_ESTIMAND": {"NONCOMPARABLE_POPULATION_OR_ESTIMAND"},
    "FUTURE_RULE_AT_HISTORICAL_AS_OF": {"FUTURE_RULE_AT_HISTORICAL_AS_OF"},
    "FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF": {"FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF"},
    "OBSERVATION_AFTER_AS_OF": {"OBSERVATION_AFTER_AS_OF"},
    "UNKNOWN_GAP": {"MISSING_GAP_UNKNOWN"},
}
