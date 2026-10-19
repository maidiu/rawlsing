"""Frozen synthetic TEST_ONLY period descriptors for the EE1 experiments.

All values are frozen in 02_EE1_FROZEN_EXPERIMENT_PLAN.json before any
implementation output existed.  Everything here is synthetic; no real source,
no Ghana, no measured claim.
"""
from __future__ import annotations

ASOF = "2026-04-15"
ASOF_LATE = "2022-12-31"
SHARES = {"2020": 0.40, "2022": 0.55}
NAIVE_DELTA = 0.15

_IDENTITY = dict(
    source="TESTONLY_EE1_PANEL",
    country_code="ZZ",
    target_population="adults_18plus_all",
    estimand="share_3_4_among_0_4",
    response_topology="SCALE_0_4",
    wording_signature="WSIG_A",
    design_signature="DSIG_A",
    rule_publication="2026-03-01",
    rule_vintage="rev1_selected",
)


def _period(wave, year, value, **overrides):
    period = dict(_IDENTITY)
    period.update(dict(wave=wave, temporal_year=year,
                       observation_year=year, probe_value=value))
    period.update(overrides)
    return period


def comparable_pair():
    return [
        _period("2020", 2020, SHARES["2020"], evidence_publication="2021-06-01"),
        _period("2022", 2022, SHARES["2022"], evidence_publication="2023-06-01"),
    ]


def mixed_family():
    pair = comparable_pair()
    pair[1]["source"] = "TESTONLY_EE1_OTHER"
    return pair


def mixed_country():
    pair = comparable_pair()
    pair[1]["country_code"] = "UT"
    return pair


def population_change():
    pair = comparable_pair()
    pair[1]["target_population"] = "adults_18plus_excl_mobile_only"
    return pair


def estimand_change():
    pair = comparable_pair()
    pair[1]["estimand"] = "share_4_among_0_4"
    return pair


def future_rule():
    pair = comparable_pair()
    pair[1]["rule_publication"] = "2027-06-01"
    pair[1]["rule_vintage"] = "rev2_selected"
    return pair


def future_evidence():
    pair = comparable_pair()
    pair[1]["evidence_publication"] = "2027-06-01"
    return pair


def observation_after_asof():
    pair = comparable_pair()
    pair[1]["evidence_publication"] = "2022-01-01"
    pair[1]["observation_year"] = 2023
    return pair


def annual_gap():
    pair = comparable_pair()
    pair[0]["annual_anchors_required"] = True
    return pair


def duplicate_year():
    pair = comparable_pair()
    pair[1]["wave"] = "2021"
    pair[1]["temporal_year"] = 2020
    return pair
