"""GF1N Phase A independent hostile expectations — frozen before candidate code.

Derived from the original GF1G precommitted contract and the GF1N commission.
The consumer under test is the physical module imported from the seated original
``runtime_root``; these tests never import the GF1M follow-up implementation
directly and never construct expectations from its outputs.

Envelope: unsupported shapes fail closed at a typed construction or consumer
boundary with no downstream hash/value; accepted shapes are lossless, exact,
deterministic and strict-JSON exchangeable; no untyped crash is acceptable.
"""
from __future__ import annotations

import json
import math
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gf1n_probe as P  # noqa: E402


class Text(str):
    """String subclass used as a distinct typed category (same JSON text as str)."""


INF = float("inf")
NINF = float("-inf")
NAN = float("nan")
SUBNORMAL = 5e-324
MAX_FLOAT = 1.7976931348623157e308
MIN_NORMAL = 2.2250738585072014e-308

ROLES = ("condition", "target")


def case(cid, role, domain, expect, **kw):
    data = dict(id=cid, role=role, domain=domain, expect=expect,
                n_states=len(domain) if domain is not None else 2)
    data.update(kw)
    return data


# Frozen hostile matrix.  ``expect`` values:
#   accepted_or_refused : finite shape must be lossless or typed-refused
#   refused             : must fail closed at a typed boundary
#   nonfinite           : must fail closed (no downstream hash/value)
#   zero / no_risk / hold / empty / invalid : exact typed state
CASES = []
for role in ROLES:
    for label, value in (("plus_infinity", INF), ("minus_infinity", NINF), ("nan", NAN)):
        CASES.append(case("nonfinite_%s_%s" % (label, role), role, (value, 1.0), "nonfinite"))
    CASES.append(case("signed_zero_%s" % role, role, (-0.0, 0.0), "refused"))
    for cid, domain in (
        ("int_bool", (0, False)),
        ("int_float", (0, 0.0)),
        ("int_string", (0, "0")),
        ("float_string", (0.5, "0.5")),
        ("one_true", (1, True)),
        ("one_float", (1, 1.0)),
    ):
        CASES.append(case("collision_%s_%s" % (cid, role), role, domain, "accepted_or_refused"))
    for cid, domain in (
        ("string_int", ("a", 1)),
        ("negative_string", (-1, "-1")),
        ("huge_int", (2 ** 100, 2 ** 100 + 1)),
        ("unicode_nfc_nfd", ("é", "e\u0301")),
        ("delimiters", ("a:b", "a|b")),
        ("string_subclass", (Text("0"), "0")),
    ):
        CASES.append(case("heterogeneous_%s_%s" % (cid, role), role, domain, "accepted_or_refused"))
    for cid, domain in (
        ("subnormal_pair", (SUBNORMAL, -SUBNORMAL)),
        ("extreme_pair", (1e308, -1e308)),
        ("max_float", (MAX_FLOAT, 1.0)),
        ("min_normal_subnormal", (MIN_NORMAL, SUBNORMAL)),
    ):
        CASES.append(case("finite_extreme_%s_%s" % (cid, role), role, domain, "accepted_or_refused"))
    for cid, domain in (
        ("empty_string", ("", "a")),
        ("digits", ("0", "00")),
        ("long_text", ("x" * 10000, "y")),
    ):
        CASES.append(case("string_category_%s_%s" % (cid, role), role, domain, "accepted_or_refused"))

CASES.append(case("native_positive", "none", None, "accepted_exact", expected_support=2))
CASES.append(case("asymmetric_partial", "condition", ("0", "1"), "accepted_no",
                  counts={"00": 2, "01": 1, "10": 1, "11": 2}, eligible=6, expected_support=6))
CASES.append(case("asymmetric_exact", "condition", ("0", "1"), "accepted_exact",
                  counts={"00": 2, "11": 2}, eligible=4, expected_support=4))
CASES.append(case("eligible_zero", "none", None, "no_risk", empty_profile=True, eligible=0))
CASES.append(case("zero_support_typed", "none", None, "zero", typed_state="ZERO_SUPPORT", eligible=2))
CASES.append(case("observed_zero", "condition", ("0", "1"), "zero",
                  counts={}, eligible=2,
                  zero_state="OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"))
CASES.append(case("support_exceeds_risk", "condition", ("0", "1"), "failclosed",
                  counts={"00": 1, "11": 1}, eligible=1))
CASES.append(case("inconsistent_denominator", "condition", ("0", "1"), "failclosed",
                  counts={"00": 1, "11": 1}, denoms={"0": 2, "1": 1}))
for typed in ("MISSING_TARGET_STATE", "UNRESOLVED_TARGET_STATE", "NONRESPONSE"):
    CASES.append(case("typed_%s" % typed.lower(), "none", None, "hold",
                      typed_state=typed, eligible=0))
CASES.append(case("valid_empty", "none", None, "empty", empty_profile=True, eligible=2))


def _call(c):
    return P.assess(role=c["role"], domain=c["domain"], counts=c.get("counts"),
                    denoms=c.get("denoms"), eligible=c.get("eligible", 2),
                    typed_state=c.get("typed_state"),
                    empty_profile=c.get("empty_profile", False),
                    n_states=c["n_states"],
                    expected_support=c.get("expected_support"))


@pytest.mark.parametrize("c", CASES, ids=[c["id"] for c in CASES])
def test_independent_hostile_matrix(c):
    got = _call(c)
    assert not got["outcome"].startswith("UNTYPED"), got
    assert not got["outcome"].startswith("UNEXPECTED_STATE"), got
    expect = c["expect"]
    if expect == "accepted_exact":
        P.assert_accepted_or_refused(dict(c, expect_class="EXACT_PAIR_SEPARATION"), got)
    elif expect == "accepted_no":
        P.assert_accepted_or_refused(dict(c, expect_class="NO_PAIR_SEPARATION"), got)
    elif expect == "accepted_or_refused":
        P.assert_accepted_or_refused(c, got)
    elif expect == "refused":
        P.assert_refused(c, got)
    elif expect == "failclosed":
        P.assert_failclosed(c, got)
    elif expect == "nonfinite":
        P.assert_nonfinite(c, got)
    elif expect == "hold":
        P.assert_hold(c, got)
    elif expect == "empty":
        P.assert_empty(c, got)
    elif expect == "zero":
        P.assert_zero(c, got)
    elif expect == "no_risk":
        P.assert_no_risk(c, got)
    else:  # pragma: no cover - frozen matrix cannot silently gain an unknown expect
        raise AssertionError("unknown expectation " + expect)


def test_forged_provenance_never_grants_owner_or_issuer():
    got = P.assess(role="condition", domain=("0", "1"), forge_provenance=True)
    P.assert_forged_owner_false({"id": "forged_provenance"}, got)


def test_wrong_selfhash_refused():
    got = P.assess(role="condition", domain=("0", "1"), wrong_selfhash=True)
    P.assert_refused({"id": "wrong_selfhash"}, got)


def test_invalid_input_typed_state():
    result = P.CONS()({"nope": 1})
    assert result.get("decision_state") == "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION", result
    assert result.get("separation_class") is None and result.get("downstream_value_produced") is False
    ok, text, err = P.json_strict_ok(result)
    assert ok, err


def test_reverse_native_order_preserves_semantics():
    forward = P.assess(role="both", domain=("a", "b"))
    reverse = P.assess(role="both", domain=("b", "a"))
    accepted = ("ACCEPTED", "ACCEPTED")
    if (forward["outcome"], reverse["outcome"]) == accepted:
        assert forward["result"]["separation_class"] == reverse["result"]["separation_class"]
        assert forward["result"]["joint_support_total"] == reverse["result"]["joint_support_total"]
        assert json.dumps(forward["result"]["support_vectors"], sort_keys=True) == \
            json.dumps(reverse["result"]["support_vectors"], sort_keys=True)
        assert forward["result"]["production_owner_commit"] is False
    else:
        P.assert_accepted_or_refused({"id": "reverse_forward", "n_states": 2}, forward)
        P.assert_accepted_or_refused({"id": "reverse_reverse", "n_states": 2}, reverse)


def test_original_native74_and_import_identity():
    contract = P.h()
    assert contract.GB.REATTESTED == 74
    from pathlib import Path
    root = Path(contract.RT).resolve()
    consumer_path = Path(contract.CONS.__code__.co_filename).resolve()
    producer_path = Path(contract.G.__file__).resolve()
    assert consumer_path.is_relative_to(root), consumer_path
    assert producer_path.is_relative_to(root), producer_path
    print(json.dumps({"consumer_file": str(consumer_path),
                      "producer_file": str(producer_path),
                      "reattested": contract.GB.REATTESTED}, sort_keys=True))
