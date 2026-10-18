"""N9J: native, source-free, PREREGISTERED joined selected-world / possibility court.

Only preexisting owner implementations run. No actor, occurrence, source authority,
model-use, Field Forge issuance, or V3 parent code is installed.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
from fractions import Fraction

import pytest

ROOT = Path(__file__).resolve().parents[2]
RETURN = ROOT / "WORKER_RETURNS/PYAT-R37-N9J-SELECTED-WORLD-PROGRESSIVE-CONSUMER-R1"
NATIVE = RETURN / "native"
sys.path.insert(0, str(NATIVE))
import rawlsing_next
if str(NATIVE / "rawlsing_next") not in rawlsing_next.__path__:
    rawlsing_next.__path__.append(str(NATIVE / "rawlsing_next"))

import e05_n9_selected_world_adapter as E
from product.service import GenericSelectedWorldService
from product.nonparent import consume as nonparent
from product.scenario import evaluate as proposal
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry, GSS, NCA
from rawlsing_next.objective_consumer_bounded_evidence import OC05, NotYetApplicableConsumer, evaluate_current_consumer

FREEZE = json.loads((RETURN / "01_FROZEN_BEFORE_EXPERIMENT.json").read_text())
FIXTURE = NATIVE / "WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json"
PROPOSALS = [
    {"scenario_id": "P_INSTITUTIONAL", "route": "institutional"},
    {"scenario_id": "P_CIVIL", "route": "civil"},
]


def _adapter(**flags):
    rows = json.loads(FIXTURE.read_text())["fields"]
    return E.N9SelectedWorldAdapter(
        service=GenericSelectedWorldService(**flags),
        registry=TestOnlyRegistry(rows),
    )


def _run(*, label="CURRENT_TEST_CLOCK", budget_tokens=5, **flags):
    a = _adapter(**flags)
    q = E.standard_request(label=label)
    snapshot = a.build_snapshot(q)
    acceptance = a.accept(q, snapshot)
    real_consumers = [
        nonparent(a.service, snapshot, budget_tokens=budget_tokens)["material"],
        proposal(a.service, snapshot, PROPOSALS)["material"],
    ]
    receipt = a.serve(q, acceptance, snapshot, consumers=real_consumers)
    return a, q, snapshot, acceptance, receipt


def _pair(receipt):
    non, proposed = [x["consumer_material"] for x in receipt["consumers"]]
    assert non["consumer"] == "NONPARENT_OPTIONS"
    assert proposed["consumer"] == "CONCEPTION_SCENARIO_PROPOSALS"
    return non, proposed


def _fraction(step, label="1"):
    cell = next(c for c in step["cells"] if c["cell"] == label)
    return Fraction(*cell["raw_probability_exact_fraction"]["$exact_fraction"])


def _counts(receipt):
    return [
        (step["denominator"], {
            cell["cell"]: cell["raw_numerator_support"] for cell in step["cells"]
        }) for step in receipt["empirical_steps"]
    ]


def _digestable(receipt):
    return {
        "hash": receipt["receipt_hash"],
        "payload_hash": receipt["receipt_payload_sha256"],
        "snapshot_hash": receipt["snapshot_hash"],
        "counts": _counts(receipt),
        "native": receipt["native_field_readset"],
        "consumer_outputs": receipt["consumers"],
        "clocks": receipt["selection"],
    }


def test_00_precommitted_before_runtime_and_noninstallation():
    assert FREEZE["execution_state"] == "PRECOMMITTED_UNEXECUTED"
    assert FREEZE["controlled_experiment_1"]["expected_fraction_before"] == ["9/16", "5/8", "3/4"]
    assert FREEZE["controlled_experiment_1"]["expected_fraction_after"] == ["19/32", "11/16", "7/8"]
    a, _, _, _, r = _run()
    assert r["state"] == "SELECTED_WORLD_VALUES_SERVED"
    assert r["grade"] == "NONINSTALLING_SOURCEFREE_ADAPTER_CANDIDATE"
    assert r["operative_N9"] is r["operative_OC05"] is r["model_use"] is False
    assert r["installed_OC05"][OC05]["current_applicability"] == "NOT_YET_APPLICABLE"
    with pytest.raises(NotYetApplicableConsumer):
        evaluate_current_consumer(policy_id=OC05, operation_id='TEST_REFUSAL', inputs=(), requested_claim_ceiling=None, partial_allowed=False)


def test_01_empirical_only_precommitted_delta_through_native_generic_consumers():
    a0, _, _, _, before = _run()
    a1, _, _, _, after = _run(empirical_changed=True)
    assert before["selection"] == after["selection"]
    assert before["structural_values"] == after["structural_values"]
    assert before["native_field_readset"] == after["native_field_readset"]
    assert [(d, c.get("1")) for d, c in _counts(before)] == [(32, 18), (16, 10), (8, 6)]
    assert [(d, c.get("1")) for d, c in _counts(after)] == [(32, 19), (16, 11), (8, 7)]
    assert [str(_fraction(s)) for s in before["empirical_steps"]] == FREEZE["controlled_experiment_1"]["expected_fraction_before"]
    assert [str(_fraction(s)) for s in after["empirical_steps"]] == FREEZE["controlled_experiment_1"]["expected_fraction_after"]
    b_non, b_prop = _pair(before)
    a_non, a_prop = _pair(after)
    assert b_non["structural_routes"] == a_non["structural_routes"]
    assert b_non["empirical"] != a_non["empirical"]
    assert b_prop["empirical"] != a_prop["empirical"]
    assert [x["feasibility"] for x in b_prop["scenarios"]] == [x["feasibility"] for x in a_prop["scenarios"]]
    assert [x["source_balance_count"] for x in b_non["source_balance_reads"]] == [4, 4, 4]
    assert [x["source_balance_count"] for x in a_non["source_balance_reads"]] == [6, 6, 6]
    for old, new in zip(before["empirical_steps"], after["empirical_steps"]):
        for k in ("source_universe_ref", "release_ref", "evidence_ref"):
            assert old[k] != new[k], k
    assert a0.service.catalog.empirical_identity() != a1.service.catalog.empirical_identity()


def test_02_structural_only_precommitted_delta_and_justified_invariance():
    _, _, _, _, before = _run()
    _, _, _, _, after = _run(structural_revision=True)
    assert before["selection"] == after["selection"]
    assert before["empirical_steps"] == after["empirical_steps"]
    assert before["native_field_readset"] == after["native_field_readset"]
    expected = FREEZE["controlled_experiment_2"]["expected_fields"]
    assert {
        k: [before["structural_values"][k]["value"], after["structural_values"][k]["value"]]
        for k in expected
    } == expected
    non0, prop0 = _pair(before)
    non1, prop1 = _pair(after)
    assert [non0["structural_routes"]["training"]["state"], non1["structural_routes"]["training"]["state"]] == FREEZE["controlled_experiment_2"]["expected_nonparent_training"]
    assert [non0["structural_routes"]["exit_constraint"]["state"], non1["structural_routes"]["exit_constraint"]["state"]] == FREEZE["controlled_experiment_2"]["expected_nonparent_exit"]
    assert [prop0["scenarios"][0]["feasibility"], prop1["scenarios"][0]["feasibility"]] == FREEZE["controlled_experiment_2"]["expected_proposal_institutional"]
    assert [prop0["scenarios"][1]["feasibility"], prop1["scenarios"][1]["feasibility"]] == FREEZE["controlled_experiment_2"]["expected_proposal_civil"]
    assert non0["empirical"] == non1["empirical"]
    assert prop0["empirical"] == prop1["empirical"]


def test_03_formal_access_is_not_real_affordability_and_proposal_is_narrower():
    _, _, _, _, r = _run(budget_tokens=1)
    non, prop = _pair(r)
    # Formal access remains true; a positive rule does not grant funds.
    assert r["structural_values"]["training_access"]["value"] is True
    assert r["structural_values"]["training_fee"]["value"] == 2
    assert non["structural_routes"]["training"]["state"] == "BLOCKED_BY_MODELED_RULE"
    assert prop["scenarios"][0]["feasibility"] == "FEASIBLE_MODELED_PREMISE"
    assert non["route_probability"] is None
    assert all(s["selection_weight"] is None for s in prop["scenarios"])


def test_04_opposite_minority_and_risk_denominator_never_disappear():
    a, _, s, _, _ = _run()
    opposite = a.service.possibilities(
        s, target="Y", conditions=(("A", 0), ("B", 1), ("C", 1)),
        consumer="N9J_MINORITIES",
    )
    assert [(x["denominator"], {
        c["cell"]: c["raw_numerator_support"] for c in x["cells"]
    }) for x in opposite["steps"]] == [
        (26, {"0": 15, "1": 11}),
        (12, {"0": 6, "1": 6}),
        (6, {"0": 2, "1": 4}),
    ]


def test_05_zero_denominator_is_typed_not_fabricated():
    a = _adapter(support_loss=True)
    q = E.standard_request(label="CURRENT_TEST_CLOCK")
    s = a.build_snapshot(q)
    evidence = a.service.possibilities(s, consumer="N9J_ZERO")
    assert evidence["steps"][-1]["denominator"] == 0
    assert evidence["steps"][-1]["state"] != "EXACT_SUPPORTED"
    assert evidence["state"] != "PRODUCTIVE_TEST_ONLY"


@pytest.mark.parametrize("forbidden", [
    "requested_pooling", "requested_person_exposure", "requested_model_use"
])
def test_06_actor_and_probability_laundering_forbidden(forbidden):
    with pytest.raises(E.N9SelectedWorldRefusal):
        E.standard_request(label="CURRENT_TEST_CLOCK", **{forbidden: True})


def test_07_two_native_units_are_separate_and_clock_bound():
    _, _, _, _, r = _run()
    fields = r["native_field_readset"]["values_read"]
    assert {x["role"] for x in fields} == {GSS, NCA}
    assert len({x["native_unit"] for x in fields}) == 2
    assert len({x["source_family"] for x in fields}) == 2
    assert r["native_field_readset"]["as_of"] == r["selection"]["published_asof"]
    assert r["pooling"] is r["person_exposure"] is False
    assert r["permission_roots"] and r["publication_clocks"] and r["effective_clocks"]


def test_08_current_and_historical_clocks_resolve_distinct_real_revisions():
    _, _, _, _, recent = _run()
    _, _, _, _, historical = _run(label="HISTORICAL_AS_OF")
    assert recent["structural_values"]["training_access"]["value"] is True
    assert historical["structural_values"]["training_access"]["value"] is True
    assert historical["selection"]["valid_at"] == "2026-06-01"
    assert historical["selection"]["published_asof"] == "2026-03-01"
    assert historical["native_field_readset"]["as_of"] == "2026-03-01"
    assert recent["native_field_readset"]["as_of"] == "2027-09-01"
    assert recent["empirical_steps"] == historical["empirical_steps"]


def test_09_revocation_is_targeted_and_old_success_is_archival_only():
    a, q, s, acceptance, r = _run()
    old_hash = r["receipt_hash"]
    hit = a.invalidate("training_access")
    assert old_hash in hit["invalidated_for_fresh_use"]
    assert a.historical_receipt(old_hash)["fresh_use_authorized"] is False
    after = a.serve(q, acceptance, s, consumers=[
        nonparent(a.service, s)["material"],
        proposal(a.service, s, PROPOSALS)["material"],
    ])
    assert after["state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert after["empirical_steps"] == r["empirical_steps"]
    assert after["native_field_readset"] == r["native_field_readset"]


def test_10_empirical_revocation_preserves_world_and_native_units():
    a, q, s, acceptance, r = _run()
    a.invalidate("empirical")
    after = a.serve(q, acceptance, s, consumers=[
        nonparent(a.service, s)["material"],
        proposal(a.service, s, PROPOSALS)["material"],
    ])
    assert after["state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert after["empirical_steps"] == []
    assert after["structural_values"] == r["structural_values"]
    assert after["native_field_readset"] == r["native_field_readset"]


def test_11_unknown_institutional_is_not_false_and_no_selection_model():
    a, q, s, acceptance, r = _run()
    a.invalidate("training_access")
    prop = proposal(a.service, s, PROPOSALS)["material"]
    assert prop["scenarios"][0]["feasibility"] == "UNKNOWN_PREMISE"
    assert prop["scenarios"][1]["feasibility"] == "FEASIBLE_MODELED_PREMISE"
    assert all(x["selection_weight"] is None and x["weight_reason"] ==
               "NO_SCENARIO_SELECTION_MODEL_OR_ISSUER" for x in prop["scenarios"])


def test_12_unrelated_field_invalidation_does_not_mutate_dependency_closure():
    a, q, s, acceptance, r = _run()
    other = _adapter(extra_field=17)
    oq = E.standard_request(label="CURRENT_TEST_CLOCK")
    osnapshot = other.build_snapshot(oq)
    oaccepted = other.accept(oq, osnapshot)
    output = other.serve(oq, oaccepted, osnapshot, consumers=[
        nonparent(other.service, osnapshot)["material"],
        proposal(other.service, osnapshot, PROPOSALS)["material"],
    ])
    assert output["native_field_readset"] == r["native_field_readset"]
    assert output["empirical_steps"] == r["empirical_steps"]
    assert {k: v["value"] for k, v in output["structural_values"].items()} == {k: v["value"] for k, v in r["structural_values"].items()}
    x = other.invalidate("unrelated_stock")
    assert output["receipt_hash"] not in x["invalidated_for_fresh_use"]
    assert output["receipt_hash"] in x["unaffected"]
    assert other.historical_receipt(output["receipt_hash"])["archival_only"] is True


def test_13_real_independent_cold_replay_and_import_paths():
    script = (
        "import sys; from pathlib import Path; "
        "sys.path.insert(0,str(Path.cwd())); "
        "from rawlsing_next.tests import test_pyat_r37_n9j_sourcefree as t; "
        "import json; print(json.dumps(t._digestable(t._run()[-1]),sort_keys=True,separators=(',',':')))"
    )
    a = subprocess.run([sys.executable, "-c", script], cwd=ROOT, capture_output=True, text=True, check=True)
    b = subprocess.run([sys.executable, "-c", script], cwd=ROOT, capture_output=True, text=True, check=True)
    assert a.stdout == b.stdout and a.stdout.strip()
    material = json.loads(a.stdout)
    assert material["counts"][0][0] == 32
    assert material["hash"] and material["payload_hash"]
    assert Path(E.__file__).resolve() == NATIVE / "e05_n9_selected_world_adapter.py"
    assert Path(sys.modules["product.nonparent"].__file__).resolve() == NATIVE / "product/nonparent.py"


def test_14_prepublication_native_field_is_typed_partial_not_zero():
    a, q, s, accepted, r = _run(label="TYPED_PARTIAL_PRE_NCA_PUBLICATION")
    assert r["state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert r["acceptance_state"] == "ACCEPTED_WITH_TYPED_PARTIAL"
    assert "NATIVE_FIELD_REFUSAL:NOT_PUBLISHED_AT_SELECTED_ASOF" in r["inconsistencies"]
    reads = r["native_field_readset"]
    assert len(reads["dependency_readset"]) == 2
    assert {x["role"] for x in reads["values_read"]} == {GSS}
    assert any(x["reason"] == "NOT_PUBLISHED_AT_SELECTED_ASOF" for x in reads["refusals"])
    assert r["pooling"] is False and r["person_exposure"] is False


def test_15_effective_publication_and_asof_clocks_cannot_be_collapsed():
    from dataclasses import replace
    a = _adapter(structural_revision=True)
    base = E.standard_request(label="CURRENT_TEST_CLOCK")
    def serve(valid_at, published_asof):
        q = replace(base, clock=E.SelectedWorldClock(
            mode="AS_OF", valid_at=valid_at, published_asof=published_asof))
        s = a.build_snapshot(q)
        accept = a.accept(q, s)
        consumers = [nonparent(a.service, s)["material"],
                     proposal(a.service, s, PROPOSALS)["material"]]
        return a.serve(q, accept, s, consumers=consumers)
    not_published = serve("2027-09-01", "2027-05-31")
    newly_published = serve("2027-09-01", "2027-06-01")
    not_effective = serve("2026-12-31", "2027-09-01")
    assert [(r["structural_values"]["training_access"]["value"],
             r["structural_values"]["exit_cost"]["value"])
            for r in (not_published, newly_published, not_effective)] == [
                (True, 2), (False, 8), (True, 2)]
    assert not_published["empirical_steps"] == newly_published["empirical_steps"]
    assert not_published["native_field_readset"] == newly_published["native_field_readset"]
    assert not_published["selection"]["valid_at"] == newly_published["selection"]["valid_at"]
    assert not_published["selection"]["published_asof"] != newly_published["selection"]["published_asof"]


def test_16_reverse_respondent_target_under_exact_native_denominator():
    a, q, s, accepted, r = _run()
    reverse = a.service.possibilities(s, target="A", conditions=(("Y", 1),),
                                      consumer="N9J_REVERSE_NATIVE")
    assert reverse["state"] == "PRODUCTIVE_TEST_ONLY"
    assert len(reverse["steps"]) == 1
    step = reverse["steps"][0]
    assert step["denominator"] == 29
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in step["cells"]} == {
        "0": 11, "1": 18}
    assert str(Fraction(*next(cell["raw_probability_exact_fraction"]["$exact_fraction"]
                              for cell in step["cells"] if cell["cell"] == "1"))) == "18/29"


def test_17_native_git_blob_preimages_are_the_exact_imported_modules():
    source_sha = {
        "product/service.py": "facf1c86911a8a4c37db112be51d8c7109cd9f3b",
        "product/nonparent.py": "2181b832d3c4376d4b9428e13f4354f273be8f32",
        "product/scenario.py": "b7e568166cd277c1ba127374ea1a350d1b3841a2",
        "product/empirical.py": "475feb9f9aea495c11c40a56b083f0b628c34e15",
        "product/world.py": "06a74caebda69f7d1baa8719a99138ef57d9c07b",
        "e05_n9_selected_world_adapter.py": "642381bc033aaeef878624bdce71f9f94708043d",
        "rawlsing_next/pre553_hq297_n9c_two_field_reader.py": "03eb46efccadd6880cb34b2e2ac609ffc9b16c59",
        "rawlsing_next/pre553_n9_n10w_progressive_candidate.py": "84d404147547767be8ecd4b6e1541f5fa3a8c8a2",
    }
    for relative, expected in source_sha.items():
        file_path = NATIVE / relative
        out = subprocess.run(["git", "hash-object", str(file_path)],
                             capture_output=True, text=True, check=True, cwd=ROOT)
        assert out.stdout.strip() == expected, relative
