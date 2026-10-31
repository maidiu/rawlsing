"""Maximal-distinction sourcefree baseline world (K10 baseline + K9 fixture world).

Invented municipal 2008 fixture.  Not historical evidence, not an operative N9
selected world, not a source release.  Value-bearing: every selected object
carries actual values that consumers must read.
"""
from __future__ import annotations

from typing import Any

BASELINE_WORLD: dict[str, Any] = {
    "semantic_world_id": "fx:municipal:2008:respondent-universe",
    "source_ref": "fx:source:synthetic",
    "source_release_ref": "fx:release:fixture1",
    "epistemic_grade": "TEST_FIXTURE_ONLY",
    "native_unit": "RESPONDENT",
    "native_strata": ["fx:stratum:A", "fx:stratum:B"],
    "absolute_horizon": "fx:AH",
    "nary": {
        "id": "fx:f1:three-party",
        "participants": [
            {"role": "institution", "ordinal": 0, "ref": "inst:1"},
            {"role": "applicant", "ordinal": 1, "ref": "selector:opaque"},
            {"role": "third-party", "ordinal": 2, "ref": "mutual_aid:3"},
        ],
        "ordered": True,
        "cardinality": 3,
        "route_refs": ["fx:r:public", "fx:r:mutual"],
    },
    "f2": {
        "id": "fx:f2:separate",
        "v555_routes": ["fx:r:public", "fx:r:mutual"],
        "f1_refs": ["fx:f1:three-party"],
        "motif": "ORIGINAL_NARY_TOPOLOGY",
        "predicate_ref": "fx:pred:historical_sponsorship",
        "history_requirement_ref": "fx:runtime-requirement:unbound",
        "selection": "DEFERRED_UNBOUND",
        "not_satisfaction": True,
    },
    "f1_refs": ["fx:f1:three-party"],
    "f2_requirement_ref": "fx:runtime-requirement:unbound",
    "public_categories": ["fx:category:license", "fx:category:recognized-club"],
    "public_sanctions": ["fx:sanction:fine", "fx:sanction:exclusion"],
    "authority_ref": "fx:issuer:fixture_only",
    "time_axes": {
        "observation_valid": "2008",
        "published": "2010",
        "as_of": "2009",
        "actor_event": "2008",
        "requested": "2026",
    },
    "clock_mode": "KNOWLEDGE_AS_OF",
    "contradictory_alternatives": [
        {"id": "route_open", "witness": "public rule A", "state": "POSSIBLE"},
        {"id": "route_closed", "witness": "public rule B", "state": "CONTRADICTORY_SOURCE_SCOPE"},
    ],
    "support": {
        "target_yes": 54,
        "target_no": 6,
        "denominator": 60,
        "base_ratio": "54/60",
        "minority_ratio": "6/60",
        "risk_set": "fx:risk:asked_eligible",
        "routing": "fx:routing:asked",
        "weight": "fx:design_weight:unit",
        "uncertainty": "fx:u:fixture_no_real_inference",
    },
    "negative_states": [
        {"scope": "fx:scope:measured-zero", "state": "OBSERVED_ZERO", "measure": 0},
        {"scope": "fx:scope:complete-empty", "state": "VALID_EMPTY", "observed_complete": True},
        {"scope": "fx:scope:missing", "state": "MISSING", "measure": None},
        {"scope": "fx:scope:power", "state": "UNDERPOWERED", "measure": None},
        {"scope": "fx:scope:notasked", "state": "NOT_ASKED", "measure": None},
        {"scope": "fx:scope:incomparable", "state": "NONCOMPARABLE", "measure": None},
        {"scope": "fx:scope:held", "state": "HELD_AUTHORITY", "measure": None},
        {"scope": "fx:scope:denied", "state": "DENIED", "measure": None},
    ],
    "routes": {
        "fx:r:public": {
            "kind": "PUBLIC_APPRENTICESHIP_ACCESS",
            "availability": "OPEN_UNDER_RULE",
            "values": {"seat_fee": "ABOLISHED_IN_2008_RULE", "min_age": 14, "quota": 30},
            "rule_ref": "fx:rule:public_access_2008",
            "sanction_refs": ["fx:sanction:fine"],
            "category_refs": ["fx:category:license"],
        },
        "fx:r:mutual": {
            "kind": "MUTUAL_AID_APPRENTICESHIP",
            "availability": "AVAILABLE_WITH_SPONSOR",
            "values": {"sponsor_required": True, "quota": 12},
            "rule_ref": "fx:rule:mutual_aid",
            "sanction_refs": ["fx:sanction:exclusion"],
            "category_refs": ["fx:category:recognized-club"],
        },
    },
    "permission_ceiling": {
        "use_atoms": ["WORLD_READ", "POSSIBILITY_QUERY"],
        "revocable": True,
        "revoked_atoms": [],
    },
    "values": {
        "fx:rule:public_access_2008": {
            "text": "public apprenticeship seats are open to resident applicants aged 14+",
            "effective": "2008",
        },
        "fx:rule:mutual_aid": {
            "text": "mutual-aid apprenticeship requires an acknowledged sponsor",
            "effective": "2008",
        },
        "fx:AH": {"text": "collective horizon of the fixture municipality", "extent": "fx:scope:town2008"},
        "fx:stratum:A": {"label": "native:municipal-role", "size": 40},
        "fx:stratum:B": {"label": "native:regional-role", "size": 20},
    },
    "generated_binding_echo": {
        "caller_fact": "location-binding-echo-0",
        "channel": "H3_GENERATED_BINDING_ECHO_FILTER_ONLY",
        "upstream_authorship": False,
    },
}

EMPIRICAL: dict[str, Any] = {
    "universe": "fx:universe:single_source",
    "sampling_unit": "RESPONDENT",
    "release": "fx:release:v1",
    "target": "fx:response:access_yes",
    "direction": "FORWARD_CONDITIONAL",
    "base_n": 60,
    "cells": [
        {"value": "YES", "n": 54},
        {"value": "NO", "n": 6},
    ],
    "condition_chain": [
        {"index": 0, "ref": "fx:cond:area", "n": 60},
        {"index": 1, "ref": "fx:cond:school", "n": 30},
        {"index": 2, "ref": "fx:cond:caretime", "n": 12},
    ],
    "minority": "fx:response:access_no",
    "uncertainty": "fx:uncertainty:sourcefree-not-real",
    "model_use": "TEST_ONLY",
    "routing": "fx:routing:asked",
    "risk_set": "fx:risk:asked_eligible",
    "weight": "fx:design_weight:unit",
    "walkback": {
        "ordered_steps": ["fx:cond:area", "fx:cond:school", "fx:cond:caretime"],
        "proxy_authority": None,
        "specificity_loss_tracked": True,
    },
}

CONSUMER_SPECS: dict[str, dict[str, Any]] = {
    "CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY": {
        "input": "generic world conditions and distribution",
        "reads": [
            "fx:rule:public_access_2008",
            "fx:rule:mutual_aid",
            "fx:r:public",
            "fx:r:mutual",
            "fx:AH",
        ],
        "output_template": "eligible scenario constraints and minority alternatives",
        "forbidden": ["parent object", "partner selection", "biography"],
    },
    "NONPARENT_APPRENTICESHIP_ENTRY": {
        "input": "same generic world and distribution",
        "reads": [
            "fx:rule:public_access_2008",
            "fx:rule:mutual_aid",
            "fx:r:public",
            "fx:r:mutual",
        ],
        "output_template": "possible apprenticeship/education access routes and restrictions",
        "forbidden": ["generated learner psyche", "parent or coparent tag"],
    },
}

REVERSAL_GRANT_SCOPED: dict[str, Any] = {
    "grant_id": "fx:grant:scoped-reversal-v1",
    "issuer": "fx:issuer:fixture_only",
    "binds": {
        "target": "fx:response:access_yes",
        "reverse_target": "fx:response:access_yes",
        "risk_set": "fx:risk:asked_eligible",
        "denominator": 60,
        "operation": "ROLE_REVERSAL_CONDITIONAL_QUERY",
    },
    "scope": "fx:universe:single_source|fx:release:v1",
}

REVERSAL_GRANT_FORGED: dict[str, Any] = {
    "grant_id": "fx:grant:forged-reversal",
    "issuer": "fx:issuer:not-competent",
    "binds": {"target": "fx:response:access_yes", "operation": "ROLE_REVERSAL_CONDITIONAL_QUERY"},
    "scope": "fx:universe:single_source|fx:release:v1",
}
