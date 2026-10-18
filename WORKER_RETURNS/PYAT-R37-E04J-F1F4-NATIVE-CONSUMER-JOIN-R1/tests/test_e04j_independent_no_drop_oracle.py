"""E04J Phase-A source-free oracle; NOT an owner-integrated acceptance test.

These are prospective, independent expectations for an eventual exact I03/I05 ->
C1/M1/M2/B5/I4 -> E04 nonparent-consumer join. There is no substituted
estimator or fabricated publisher/source/model authority here.
"""
from collections import Counter
from fractions import Fraction
import hashlib
import json
import pytest


def rows(coupling):
    """Two intact same-respondent 2x2 laws, identical A/B marginal counts."""
    cells = {"concordant": ((0, 0, 4), (1, 1, 4)),
             "minority": ((0, 0, 3), (0, 1, 1), (1, 0, 1), (1, 1, 3)),
             "null": ((0, 0, 2), (0, 1, 2), (1, 0, 2), (1, 1, 2))}[coupling]
    return tuple({"respondent_ref": f"{coupling}:R{i}", "A": a, "B": b}
                 for i, (a, b) in enumerate((a, b) for a, b, n in cells for _ in range(n)))


def witnessed_product(records, *, authorized=True, available=True):
    if not available:
        return {"state": "DEVELOPMENT_BLOCKER_MISSING_PIPELINE_ARTIFACT"}
    if not authorized:
        return {"state": "BLOCKED_MISSING_EXACT_QUERY_AND_DENOMINATOR_AUTHORITY"}
    assert len({r["respondent_ref"] for r in records}) == len(records)
    assert all("A" in r and "B" in r for r in records)
    joint = Counter((r["A"], r["B"]) for r in records)
    n = len(records)
    a1 = sum(c for (a, _), c in joint.items() if a == 1)
    b1 = sum(c for (_, b), c in joint.items() if b == 1)
    both = joint[1, 1]
    material = {"rows": records, "joint": sorted((a, b, c) for (a, b), c in joint.items()),
                "denominator": n}
    return {"state": "EMPIRICAL_PRODUCT", "denominator": n, "a1": a1, "b1": b1,
            "joint": joint, "forward": Fraction(both, a1) if a1 else None,
            "reverse_if_permitted": Fraction(both, b1) if b1 else None,
            "producer_replay_digest": hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()}


def test_equal_marginals_cannot_substitute_for_joint_evidence():
    p, q = [witnessed_product(rows(x)) for x in ("concordant", "minority")]
    assert (p["denominator"], p["a1"], p["b1"]) == (q["denominator"], q["a1"], q["b1"]) == (8, 4, 4)
    assert p["joint"] != q["joint"]
    assert p["forward"] == Fraction(1) and q["forward"] == Fraction(3, 4)
    assert p["producer_replay_digest"] != q["producer_replay_digest"]


def test_minority_support_and_replay_are_not_flattened():
    p = witnessed_product(rows("minority"))
    assert p["joint"][0, 1] == p["joint"][1, 0] == 1
    assert sum(p["joint"].values()) == p["denominator"]
    assert witnessed_product(rows("minority"))["producer_replay_digest"] == p["producer_replay_digest"]
    assert p["reverse_if_permitted"] == Fraction(3, 4)


def test_null_is_product_not_pipeline_absence():
    p = witnessed_product(rows("null"))
    assert p["state"] == "EMPIRICAL_PRODUCT"
    assert p["forward"] == Fraction(1, 2)
    assert p["joint"][0, 1] == p["joint"][1, 0] == 2
    assert p["producer_replay_digest"]


def test_unavailable_artifact_is_blocker_not_null():
    assert witnessed_product((), available=False)["state"] == "DEVELOPMENT_BLOCKER_MISSING_PIPELINE_ARTIFACT"
    assert witnessed_product((), authorized=False)["state"] == "BLOCKED_MISSING_EXACT_QUERY_AND_DENOMINATOR_AUTHORITY"


def test_same_person_and_complete_basis_are_mandatory():
    data = list(rows("minority"))
    data[1] = {**data[1], "respondent_ref": data[0]["respondent_ref"]}
    with pytest.raises(AssertionError):
        witnessed_product(data)
    data = list(rows("minority"))
    del data[1]["B"]
    with pytest.raises(AssertionError):
        witnessed_product(data)


def test_invalidation_cannot_use_stale_replay_identity():
    old, new = (witnessed_product(rows(x)) for x in ("concordant", "minority"))
    assert old["producer_replay_digest"] != new["producer_replay_digest"]
    revoked = {old["producer_replay_digest"]}
    assert old["producer_replay_digest"] in revoked
    assert new["producer_replay_digest"] not in revoked
