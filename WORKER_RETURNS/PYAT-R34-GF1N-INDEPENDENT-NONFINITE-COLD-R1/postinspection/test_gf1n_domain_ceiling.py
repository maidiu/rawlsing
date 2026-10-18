"""GF1N POST-INSPECTION supplementary domain-ceiling probes.

These are explicitly post-inspection tests, not the frozen prefreeze.  They
target the edges the candidate's nonfinite guard does not obviously cover
(row/cell states, counts, type ceilings) and record precise limits.  They do not
rewrite any frozen expectation and are reported separately from the Phase A
matrix.
"""
from __future__ import annotations

import json
import math
import os
import sys
from decimal import Decimal

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "phase_a"))
import gf1n_probe as P  # noqa: E402

INF = float("inf")
NAN = float("nan")


class InfFloat(float):
    """float subclass whose value is still nonfinite."""


def construct(f):
    try:
        digest = P.h().G.semantic_hash(P.h().G._projection(f))
        rel = P.h().G.GenericNativePairRelation(
            **f, content_hash=digest,
            object_id="urn:rawlsing:gf1:generic-pair-relation:sha256:" + digest)
    except P.h().G.GenericNativePairError as exc:
        return {"outcome": "TYPED_CONSTRUCTION_REFUSAL", "error": type(exc).__name__ + ":" + str(exc)}
    except Exception as exc:  # noqa: BLE001
        return {"outcome": "PRODUCER_DOMAIN_LIMIT", "error": type(exc).__name__ + ":" + str(exc)}
    try:
        result = P.CONS()(rel)
    except Exception as exc:  # noqa: BLE001
        return {"outcome": "UNTYPED_CONSUMER_CRASH", "error": type(exc).__name__ + ":" + str(exc)}
    ok, text, err = P.json_strict_ok(result)
    return {"outcome": "CONSUMER_RESULT", "result": result, "strict_ok": ok, "strict_error": err}


def base(role="condition", domain=("0", "1")):
    f = P.fields()
    cd = tuple(domain) if role in ("condition", "both") else tuple(f["conditioner_domain"])
    td = tuple(domain) if role in ("target", "both") else tuple(f["target_domain"])
    f["conditioner_domain"] = cd
    f["target_domain"] = td
    f["conditional_count_profile"] = P._rows(f, cd, td, None, None,
                                              "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET")
    f["typed_state"] = "SUPPORTED"
    f["producer_state_blocking"] = False
    f["eligible_joint_risk_total"] = 2
    return f


def assert_fails_closed(got):
    assert got["outcome"] in ("TYPED_CONSTRUCTION_REFUSAL", "PRODUCER_DOMAIN_LIMIT",
                              "CONSUMER_RESULT"), got
    if got["outcome"] == "CONSUMER_RESULT":
        result = got["result"]
        assert result.get("decision_state") in (
            "CONSUMER_RELATION_INTEGRITY_REJECTED",
            "CONSUMER_RELATION_IDENTITY_MISMATCH",
            "CONSUMER_PRODUCER_TYPED_STATE_BLOCKING"), result
        assert result.get("separation_class") is None, result
        assert result.get("downstream_value_produced") is False, result
        assert got["strict_ok"], got.get("strict_error")


@pytest.mark.parametrize("role", ["condition", "target"])
def test_nonfinite_row_state_refused(role):
    f = base(role=role)
    if role == "condition":
        f["conditional_count_profile"][0]["condition_state"] = INF
    else:
        f["conditional_count_profile"][0]["target_counts"][0]["target_state"] = NAN
    assert_fails_closed(construct(f))


@pytest.mark.parametrize("role", ["condition", "target"])
@pytest.mark.parametrize("count", [INF, NAN, 1.0, True, -1])
def test_noninteger_or_nonfinite_count_refused(role, count):
    f = base(role=role)
    if role == "condition":
        f["conditional_count_profile"][0]["condition_denominator_support"] = count
    else:
        f["conditional_count_profile"][0]["target_counts"][0]["joint_support_count"] = count
    assert_fails_closed(construct(f))


def test_swapped_target_cells_refused():
    f = base(role="target")
    cells = list(f["conditional_count_profile"][0]["target_counts"])
    f["conditional_count_profile"][0]["target_counts"] = tuple(reversed(cells))
    assert_fails_closed(construct(f))


def test_duplicate_condition_row_refused():
    f = base(role="condition")
    rows = list(f["conditional_count_profile"])
    rows[1] = dict(rows[1], condition_state=rows[0]["condition_state"])
    f["conditional_count_profile"] = tuple(rows)
    assert_fails_closed(construct(f))


@pytest.mark.parametrize("value,label", [
    (Decimal("Infinity"), "decimal_infinity"),
    (Decimal("NaN"), "decimal_nan"),
    (complex(1, 2), "complex"),
    (b"bytes", "bytes"),
])
def test_unsupported_object_never_silently_accepted(value, label):
    """Arbitrary Python objects are outside the measured ceiling.

    A producer-level TypeError/ValueError is a documented construction limit, not
    a candidate acceptance; a consumer path must still fail closed or be strict.
    """
    f = base(role="condition", domain=(value, "1"))
    got = construct(f)
    assert_fails_closed(got)
    assert got["outcome"] != "CONSUMER_RESULT" or got["strict_ok"]


def test_float_subclass_nonfinite_refused():
    f = base(role="condition", domain=(InfFloat(INF), 1.0))
    got = construct(f)
    assert_fails_closed(got)


def test_finite_heterogeneous_numeric_is_lossless():
    """A representable int/float domain is a positive ceiling control."""
    got = P.assess(role="condition", domain=(0, 1.5))
    assert got["outcome"] == "ACCEPTED", got
    result = got["result"]
    assert result["separation_class"] == "EXACT_PAIR_SEPARATION"
    assert result["joint_support_total"] == 2
    keys = list(result["support_vectors"])
    assert len(keys) == 2
    assert type(keys[0]) is int and type(keys[1]) is float, keys
    assert got["strict_ok"] and got.get("deterministic") is True


def test_signed_zero_row_state_is_value_equal_limit():
    """Documented limit: -0.0 row state is value-equal to 0.0 under exact type/value.

    The domain is finite and distinct; the row is matched by Python equality, so
    the sign bit is not a separate identity.  Support is still conserved and the
    result is strict; this is a ceiling note, not a positive-category claim.
    """
    f = base(role="condition", domain=(0.0, 1.0))
    f["conditional_count_profile"][0]["condition_state"] = -0.0
    got = construct(f)
    assert got["outcome"] == "CONSUMER_RESULT", got
    result = got["result"]
    assert result.get("decision_state") == "PAIR_SUPPORT_SIGNATURE_COMPUTED", result
    assert result.get("joint_support_total") == 2, result
    assert got["strict_ok"], got.get("strict_error")


@pytest.mark.parametrize("role", ["condition", "target"])
@pytest.mark.parametrize("domain,label", [
    ((True, "true"), "bool_json_true"),
    ((False, "false"), "bool_json_false"),
    ((None, "null"), "none_json_null"),
    ((True, "True"), "bool_str_true_cap"),
    ((1.0, "1.0"), "float_str_same_text"),
    ((1e308, "1e+308"), "extreme_float_str_same_text"),
])
def test_duplicate_semantic_json_names_fail_closed(role, domain, label):
    got = P.assess(role=role, domain=domain)
    assert got["outcome"] in ("CONSUMER_REFUSED", "CONSTRUCTION_REFUSED", "HOLD"), got
    if got["outcome"] == "CONSUMER_REFUSED":
        result = got["result"]
        assert result.get("decision_state") == "CONSUMER_RELATION_INTEGRITY_REJECTED", result
        assert result.get("separation_class") is None and result.get("downstream_value_produced") is False
        assert not {"result_hash", "support_vectors", "separation_signature"} & result.keys()
        assert got["strict_ok"], got.get("strict_error")
