"""GF1N POST-INSPECTION supported-input conservation and reverse orientation.

Post-inspection supplementary court (not the frozen prefreeze).  It verifies an
explicitly representable heterogeneous numeric/string domain preserves exact
cell counts, role keys/types, support total and reverse orientation, and remains
strict-JSON and deterministic.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "phase_a"))
import gf1n_probe as P  # noqa: E402

COUNTS = {"00": 2, "01": 1, "10": 0, "11": 3}
REVERSED = {"00": 3, "01": 0, "10": 1, "11": 2}


def test_supported_counts_roles_and_reverse_conserved():
    forward = P.assess(role="both", domain=None)  # template domains for shape
    # explicit heterogeneous conditioner (int/float) and target (strings)
    f = P.fields()
    cd = (0, 1.5)
    td = ("a", "b")
    f["conditioner_domain"] = cd
    f["target_domain"] = td
    f["conditional_count_profile"] = P._rows(
        f, cd, td, COUNTS, None, "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET")
    f["typed_state"] = "SUPPORTED"
    f["producer_state_blocking"] = False
    f["eligible_joint_risk_total"] = 6
    digest = P.h().G.semantic_hash(P.h().G._projection(f))
    rel = P.h().G.GenericNativePairRelation(
        **f, content_hash=digest,
        object_id="urn:rawlsing:gf1:generic-pair-relation:sha256:" + digest)
    got = P.CONS()(rel)
    assert got["decision_state"] == "PAIR_SUPPORT_SIGNATURE_COMPUTED", got
    assert got["joint_support_total"] == 6, got
    assert got["separation_class"] == "NO_PAIR_SEPARATION", got
    vectors = got["support_vectors"]
    assert list(vectors) == [0, 1.5], list(vectors)
    assert [type(k) for k in vectors] == [int, float]
    assert vectors[0] == {"a": 2, "b": 1}, vectors
    assert vectors[1.5] == {"a": 0, "b": 3}, vectors
    assert got["condition_states_with_positive_denominator"] == [0, 1.5]
    assert json.dumps(got, sort_keys=True, allow_nan=False)
    assert got["result_hash"] == P.CONS()(rel)["result_hash"]

    # reverse both domains and both orders; counts map to the reversed indices
    g = P.fields()
    rcd = (1.5, 0)
    rtd = ("b", "a")
    g["conditioner_domain"] = rcd
    g["target_domain"] = rtd
    g["conditional_count_profile"] = P._rows(
        g, rcd, rtd, REVERSED, None, "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET")
    g["typed_state"] = "SUPPORTED"
    g["producer_state_blocking"] = False
    g["eligible_joint_risk_total"] = 6
    rdigest = P.h().G.semantic_hash(P.h().G._projection(g))
    rrel = P.h().G.GenericNativePairRelation(
        **g, content_hash=rdigest,
        object_id="urn:rawlsing:gf1:generic-pair-relation:sha256:" + rdigest)
    rgot = P.CONS()(rrel)
    assert rgot["joint_support_total"] == 6 and rgot["separation_class"] == "NO_PAIR_SEPARATION"
    assert [type(k) for k in rgot["support_vectors"]] == [float, int]
    assert json.dumps(got["support_vectors"], sort_keys=True) == \
        json.dumps(rgot["support_vectors"], sort_keys=True)
    assert json.dumps(got, sort_keys=True, allow_nan=False)
