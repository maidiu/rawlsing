"""E04J bounded native E04 consumer court.

Uses exact retained E04 owner files, with real C1/N10E I03 producer imports.
The synthetic same-marginal law is the existing E04 source fixture, not a
new estimator. Does not assert M1/M2/B5/I4 learning or native I05 recursion.
This suite must be run cold with repository root and ../runtime on PYTHONPATH.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

import pytest

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from product.service import GenericSelectedWorldService
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next import pre553_n9_n10w_progressive_candidate as original_rows


def _consumer_read(*, same_marginals=False):
    service = GenericSelectedWorldService(same_marginals=same_marginals)
    snapshot = service.select(
        mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01"
    )
    returned = consume(service, snapshot)
    assert returned["material"]["consumer"] == "NONPARENT_OPTIONS"
    return service, snapshot, returned


def _empirical(receipt):
    return receipt["material"]["empirical"]


def _binary_counts(step):
    return {c["cell"]: c["raw_numerator_support"] for c in step["cells"]}


def test_actual_native_producer_values_reach_original_nonparent_consumer():
    service, snapshot, receipt = _consumer_read()
    assert receipt["material"]["state"] == "OPTIONS_AND_SOURCE_SUPPORT_PRODUCED"
    assert _empirical(receipt)["state"] == "PRODUCTIVE_TEST_ONLY"
    steps = _empirical(receipt)["steps"]
    assert len(steps) == 3
    assert [s["denominator"] for s in steps] == [32, 16, 8]
    assert [_binary_counts(s)["1"] for s in steps] == [18, 10, 6]
    assert [_binary_counts(s)["0"] for s in steps] == [14, 6, 2]
    assert len(receipt["material"]["source_balance_reads"]) == 3
    actual_readset = [r for r in receipt["material"]["values_read"] if r["channel"] == "empirical"]
    assert len(actual_readset) == 3
    for native, read, balance in zip(steps, actual_readset, receipt["material"]["source_balance_reads"]):
        assert read["value_read"] == native["cells"]
        assert read["denominator"] == native["denominator"]
        assert read["evidence_ref"] == balance["evidence_ref"] == native["evidence_ref"]
        assert native["producer_query_ref"] and native["producer_fact_ref"]
        assert native["source_universe_ref"] and native["release_ref"]
        assert native["authority_refs"] and native["provenance_refs"]
    assert receipt["material"]["route_probability"] is None
    assert receipt["material"]["person_generation"] if "person_generation" in receipt["material"] else True
    assert service.provider.trace
    assert any(t["call"] == "compose_positioned_subject_possibility" for t in service.provider.trace)
    assert any(t["call"] == "provide_empirical_possibility_slice" for t in service.provider.trace)


def test_equal_marginals_but_different_native_conditional_reach_same_consumer():
    left, _, lr = _consumer_read(same_marginals=False)
    right, _, rr = _consumer_read(same_marginals=True)
    la = _empirical(lr)["steps"]
    ra = _empirical(rr)["steps"]
    assert [s["denominator"] for s in la] == [s["denominator"] for s in ra] == [32, 16, 8]
    assert [_binary_counts(s)["1"] for s in la] == [18, 10, 6]
    assert [_binary_counts(s)["1"] for s in ra] == [19, 11, 7]
    assert lr["material"]["source_balance_reads"] != rr["material"]["source_balance_reads"]
    assert la[2]["evidence_ref"] != ra[2]["evidence_ref"]
    assert left.catalog.empirical_identity()["source_universe_ref"] != right.catalog.empirical_identity()["source_universe_ref"]
    assert lr["material"]["values_read"][-1]["value_read"] != rr["material"]["values_read"][-1]["value_read"]

    # Independent source-fixture marginal check: two opposite Y flips,
    # one inside and one outside the exact A=B=C=1 joint branch.
    rows = original_rows.synthetic_world_rows()
    tally = Counter(r["responses"]["Y"] for r in rows)
    assert len(rows) == 58
    assert tally == Counter({0: 29, 1: 29})
    changed = [dict(r, responses=dict(r["responses"])) for r in rows]
    next(r for r in changed if all(r["responses"][q] == 1 for q in ("A", "B", "C")) and r["responses"]["Y"] == 0)["responses"]["Y"] = 1
    next(r for r in changed if all(r["responses"][q] == 0 for q in ("A", "B", "C")) and r["responses"]["Y"] == 1)["responses"]["Y"] = 0
    assert Counter(r["responses"]["Y"] for r in changed) == tally


def test_minority_and_respondent_joint_alternatives_survive_read_boundary():
    _, _, a = _consumer_read()
    _, _, b = _consumer_read(same_marginals=True)
    assert _binary_counts(_empirical(a)["steps"][2]) == {"0": 2, "1": 6}
    assert _binary_counts(_empirical(b)["steps"][2]) == {"0": 1, "1": 7}
    for receipt in (a, b):
        final = _empirical(receipt)["steps"][2]
        assert final["denominator"] == sum(_binary_counts(final).values())
        assert final["geometry"]["denominator"]["raw_denominator_support"] == final["denominator"]
        assert len(final["geometry"]["denominator"]["denominator_member_refs"]) == final["denominator"]
        assert final["geometry"]["target"]["arity"] == 1
        assert final["uncertainty"] != "NO_SUPPORTED_EVIDENCE"


def test_reverse_query_only_at_explicit_existing_role_and_denominator():
    first = GenericSelectedWorldService()
    second = GenericSelectedWorldService(same_marginals=True)
    base = first.provider.step("A", (("Y", 1),))
    changed = second.provider.step("A", (("Y", 1),))
    assert base["denominator"] == changed["denominator"] == 29
    assert _binary_counts(base) == {"0": 11, "1": 18}
    assert _binary_counts(changed) == {"0": 10, "1": 19}
    with pytest.raises(ValueError, match="TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE"):
        first.provider.step("A", (("B", 1),))


def test_source_revision_replay_and_invalidation_preserve_historical_evidence():
    service, snapshot, old = _consumer_read()
    new_service, _, new = _consumer_read(same_marginals=True)
    assert old["receipt_hash"] != new["receipt_hash"]
    old_hash = old["receipt_hash"]
    result = service.invalidate("empirical")
    assert old_hash in result["invalidated_for_fresh_use"]
    historical = service.historical_receipt(old_hash)
    assert historical["archival_only"] is True
    assert historical["fresh_use_authorized"] is False
    refused = consume(service, snapshot)
    assert refused["material"]["state"] == "PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT"
    assert refused["material"]["empirical"]["state"] != "PRODUCTIVE_TEST_ONLY"
    assert refused["material"]["empirical"]["steps"] == []
    assert new_service.provider._identity() != service.provider._identity()


def test_missing_basis_is_not_relabelled_empirical_null():
    service = GenericSelectedWorldService(support_loss=True)
    snapshot = service.select(mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01")
    material = consume(service, snapshot)["material"]
    assert material["empirical"]["state"] == "PARTIAL_TYPED_EMPIRICAL_SUPPORT"
    assert any(s["state"] != "EXACT_SUPPORTED" for s in material["empirical"]["steps"])
    service.invalidate("empirical")
    unavailable = consume(service, snapshot)["material"]
    assert unavailable["empirical"]["state"] != "PRODUCTIVE_TEST_ONLY"
    assert unavailable["empirical"]["steps"] == []


def test_second_original_consumer_reads_evidence_without_selecting_person():
    service = GenericSelectedWorldService(same_marginals=True)
    snapshot = service.select(mode="AS_OF", valid_at="2027-09-01", published_asof="2027-09-01")
    proposal = evaluate(service, snapshot, [{"scenario_id": "P1", "route": "institutional"}])["material"]
    assert proposal["consumer"] == "CONCEPTION_SCENARIO_PROPOSALS"
    assert proposal["scenarios"][0]["selection_weight"] is None
    assert proposal["person_generation"] is False
    assert proposal["actual_conception"] is False
    assert proposal["values_read"]
    assert proposal["scenarios"][0]["empirical_profiles"][2]["denominator"] == 8
