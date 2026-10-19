"""Independent I2 adversarial court for PYAT R37 N9J (reviewer-authored).

Written by the independent R38 reviewer from the pinned N9J evidence and the
native owner sources only. Does NOT import or re-execute the worker's test
module; expected quantities are recomputed here from the synthetic E03 rows
and from the pinned native producer objects.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

N9J_ROOT = Path(os.environ.get(
    "PYAT_R38_N9J_ROOT",
    "/Users/matthewsmith/Desktop/Rawlsing/R38-N9TI-N9J-pin-7628840c4",
)).resolve()
RETURN = N9J_ROOT / "WORKER_RETURNS/PYAT-R37-N9J-SELECTED-WORLD-PROGRESSIVE-CONSUMER-R1"
NATIVE = RETURN / "native"

sys.path.insert(0, str(NATIVE))
sys.path.insert(0, str(N9J_ROOT))
import rawlsing_next  # noqa: E402
if str(NATIVE / "rawlsing_next") not in rawlsing_next.__path__:
    rawlsing_next.__path__.append(str(NATIVE / "rawlsing_next"))

import e05_n9_selected_world_adapter as E  # noqa: E402
from product.service import GenericSelectedWorldService  # noqa: E402
from product.nonparent import consume as nonparent  # noqa: E402
from product.scenario import evaluate as proposal  # noqa: E402
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry, GSS, NCA  # noqa: E402
from rawlsing_next import pre553_n9_n10w_progressive_candidate as e03  # noqa: E402

FIXTURE = NATIVE / "WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json"
PROPOSALS = [{"scenario_id": "P_INSTITUTIONAL", "route": "institutional"},
             {"scenario_id": "P_CIVIL", "route": "civil"}]


def _adapter(**flags):
    rows = json.loads(FIXTURE.read_text())["fields"]
    return E.N9SelectedWorldAdapter(
        service=GenericSelectedWorldService(**flags),
        registry=TestOnlyRegistry(rows))


def _serve(adapter, *, budget=5, label="CURRENT_TEST_CLOCK"):
    q = E.standard_request(label=label)
    s = adapter.build_snapshot(q)
    a = adapter.accept(q, s)
    consumers = [nonparent(adapter.service, s, budget_tokens=budget)["material"],
                 proposal(adapter.service, s, PROPOSALS)["material"]]
    r = adapter.serve(q, a, s, consumers=consumers)
    return q, s, a, r


def _rows(changed=False, support_loss=False, same_marginals=False):
    rows = e03.synthetic_world_rows()
    if changed or same_marginals:
        next(r for r in rows if all(r["responses"][q] == 1 for q in ("A", "B", "C"))
             and r["responses"]["Y"] == 0)["responses"]["Y"] = 1
    if same_marginals:
        next(r for r in rows if all(r["responses"][q] == 0 for q in ("A", "B", "C"))
             and r["responses"]["Y"] == 1)["responses"]["Y"] = 0
    if support_loss:
        rows = [r for r in rows if not all(r["responses"][q] == 1 for q in ("A", "B", "C"))]
    return rows


def _count(rows, target, conditions):
    sel = [r for r in rows if all(r["responses"][q] == v for q, v in conditions)]
    y = sum(1 for r in sel if r["responses"][target] == 1)
    return len(sel), y


def test_a01_values_read_originate_from_named_native_producer():
    a = _adapter()
    q, s, _, r = _serve(a)
    non, prop = [c["consumer_material"] for c in r["consumers"]]
    for material in (non, prop):
        assert material["values_read"], "consumer recorded no value reads"
        structural = [x for x in material["values_read"] if x["channel"] == "structural"]
        empirical = [x for x in material["values_read"] if x["channel"] == "empirical"]
        assert structural and empirical
        for record in structural:
            assert record["consumer"] in ("NONPARENT_OPTIONS", "CONCEPTION_SCENARIO_PROPOSALS")
            read = a.service.catalog.read(s, record["scope"])
            assert read["state"] == "SUPPORTED_TEST_ONLY"
            assert record["value_read"] == read["value"]
            ref = record["source_ref"]
            handle = a.service.catalog.handles[ref["content_hash"]]
            assert handle.payload["value"] == record["value_read"]
            assert handle.payload["key"] == record["scope"]
            assert handle.payload["source_root"] == "TEST_ONLY_E04_SOURCE_ROOT"
        for record in empirical:
            assert record["scope"] == "empirical"
            assert record["state"] == "EXACT_SUPPORTED"
            assert [c["raw_numerator_support"] for c in record["value_read"]]
        for record in material["values_read"]:
            assert record["snapshot_ref"] == s.snapshot_hash
    binding = json.dumps(q.binding())
    assert "2388192" not in binding and "23414527" not in binding
    assert "9/16" not in binding and "72.6" not in binding


def test_a02_forward_denominators_and_fractions_recomputed_from_rows():
    _, _, _, r = _serve(_adapter())
    base = _rows()
    expected = [("Y", (("A", 1),)), ("Y", (("A", 1), ("B", 1))), ("Y", (("A", 1), ("B", 1), ("C", 1)))]
    for step, (t, cond) in zip(r["empirical_steps"], expected):
        n, y = _count(base, t, cond)
        cells = {c["cell"]: c["raw_numerator_support"] for c in step["cells"]}
        assert step["denominator"] == n
        assert cells["1"] == y and cells["0"] == n - y
        one = next(c for c in step["cells"] if c["cell"] == "1")
        frac = Fraction(*one["raw_probability_exact_fraction"]["$exact_fraction"])
        assert frac == Fraction(y, n)
    assert [str(Fraction(*next(c for c in st["cells"] if c["cell"] == "1")
                         ["raw_probability_exact_fraction"]["$exact_fraction"]))
            for st in r["empirical_steps"]] == ["9/16", "5/8", "3/4"]


def test_a03_reverse_conditional_denominator_29_independently_derived():
    a = _adapter()
    _, s, _, _ = _serve(a)
    rev = a.service.possibilities(s, target="A", conditions=(("Y", 1),), consumer="I2_REVERSE")
    step = rev["steps"][0]
    base = _rows()
    n_y1 = sum(1 for r in base if r["responses"]["Y"] == 1)
    n_a1_y1 = sum(1 for r in base if r["responses"]["Y"] == 1 and r["responses"]["A"] == 1)
    assert (step["denominator"], {c["cell"]: c["raw_numerator_support"] for c in step["cells"]}) == \
        (n_y1, {"0": n_y1 - n_a1_y1, "1": n_a1_y1}) == (29, {"0": 11, "1": 18})
    frac = Fraction(*next(c for c in step["cells"] if c["cell"] == "1")
                    ["raw_probability_exact_fraction"]["$exact_fraction"])
    assert frac == Fraction(18, 29) != Fraction(18, 32)


def test_a04_minority_options_recomputed_from_rows():
    a = _adapter()
    _, s, _, r = _serve(a)
    base = _rows()
    opposite = a.service.possibilities(s, target="Y",
                                        conditions=(("A", 0), ("B", 1), ("C", 1)),
                                        consumer="I2_MINORITY")
    expect = [_count(base, "Y", (("A", 0),)),
              _count(base, "Y", (("A", 0), ("B", 1))),
              _count(base, "Y", (("A", 0), ("B", 1), ("C", 1)))]
    got = [(x["denominator"], sum(c["raw_numerator_support"] for c in x["cells"] if c["cell"] == "1"))
           for x in opposite["steps"]]
    assert got == expect == [(26, 11), (12, 6), (6, 4)]
    non = r["consumers"][0]["consumer_material"]
    for step in non["empirical"]["steps"]:
        assert {c["cell"] for c in step["cells"]} == {"0", "1"}


def test_a05_same_marginals_intervention_is_a_different_source_change():
    base = _rows()
    same = _rows(same_marginals=True)
    assert sum(r["responses"]["Y"] for r in same) == sum(r["responses"]["Y"] for r in base)
    _, _, _, r_same = _serve(_adapter(same_marginals=True))
    expect = [_count(same, "Y", (("A", 1),)),
              _count(same, "Y", (("A", 1), ("B", 1))),
              _count(same, "Y", (("A", 1), ("B", 1), ("C", 1)))]
    got = [(s["denominator"], {c["cell"]: c["raw_numerator_support"] for c in s["cells"]})
           for s in r_same["empirical_steps"]]
    assert got == [(n, {"0": n - y, "1": y}) for n, y in expect]
    changed = _rows(changed=True)
    _, _, _, r_changed = _serve(_adapter(empirical_changed=True))
    expect_c = [_count(changed, "Y", (("A", 1),)),
                _count(changed, "Y", (("A", 1), ("B", 1))),
                _count(changed, "Y", (("A", 1), ("B", 1), ("C", 1)))]
    got_c = [(s["denominator"], {c["cell"]: c["raw_numerator_support"] for c in s["cells"]})
             for s in r_changed["empirical_steps"]]
    assert got_c == [(n, {"0": n - y, "1": y}) for n, y in expect_c] == \
        [(32, {"0": 13, "1": 19}), (16, {"0": 5, "1": 11}), (8, {"0": 1, "1": 7})]
    assert r_same["receipt_hash"] not in (r_changed["receipt_hash"],)


def test_a06_zero_support_is_typed_at_service_layer_never_fabricated():
    a = _adapter(support_loss=True)
    q = E.standard_request(label="CURRENT_TEST_CLOCK")
    s = a.build_snapshot(q)
    acc = a.accept(q, s)
    assert acc.acceptance_state == "ACCEPTED_ATOMIC_SELECTED_SNAPSHOT"
    evidence = a.service.possibilities(s, consumer="I2_ZERO")
    assert evidence["state"] == "PARTIAL_TYPED_EMPIRICAL_SUPPORT"
    assert evidence["state"] != "PRODUCTIVE_TEST_ONLY"
    last = evidence["steps"][-1]
    assert last["denominator"] == 0
    assert last["cells"] == []
    assert last["state"] != "EXACT_SUPPORTED"
    assert last["uncertainty"] == "NO_SUPPORTED_EVIDENCE"
    for step in evidence["steps"][:-1]:
        assert step["state"] == "EXACT_SUPPORTED"
        for cell in step["cells"]:
            assert cell["raw_probability_exact_fraction"]


def test_a14_adapter_serve_must_type_zero_support_step_without_keyerror():
    """I2 falsifier: the adapter seam, not just the service, must type no-support.

    The worker's own test_05 only proves the SERVICE layer types the zero
    denominator; it never calls adapter.serve() on that path.  This court does.
    """
    a = _adapter(support_loss=True)
    q = E.standard_request(label="CURRENT_TEST_CLOCK")
    s = a.build_snapshot(q)
    acc = a.accept(q, s)
    try:
        receipt = a.serve(q, acc, s)
    except KeyError as exc:
        pytest.fail("UNTYPED_CRASH key=" + repr(exc.args[0]) +
                    " in adapter.serve instead of a typed partial receipt")
    assert receipt["state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    assert receipt["empirical_state"] == "PARTIAL_TYPED_EMPIRICAL_SUPPORT"
    assert receipt["empirical_steps"][-1]["denominator"] == 0
    assert receipt["empirical_steps"][-1]["cells"] == []


def test_a07_source_families_units_and_publications_stay_separate():
    _, _, _, r = _serve(_adapter())
    values = r["native_field_readset"]["values_read"]
    assert len(values) == 2
    by_role = {v["role"]: v for v in values}
    assert set(by_role) == {GSS, NCA}
    gss, nca = by_role[GSS], by_role[NCA]
    assert gss["native_unit"] != nca["native_unit"]
    assert gss["source_family"] != nca["source_family"]
    assert gss["native_geography"] != nca["native_geography"]
    assert gss["publication_date"] != nca["publication_date"]
    assert gss["values"]["numerator"] == 2388192
    assert gss["values"]["denominator"] == 3288063
    assert round(100 * gss["values"]["numerator"] / gss["values"]["denominator"], 1) == \
        gss["values"]["published_percent"] == 72.6
    assert nca["values"]["active_subscriptions"] == 23414527
    assert "NOT_UNIQUE_PERSONS" in nca["native_unit"]
    assert r["pooling"] is False and r["person_exposure"] is False
    # registry rows are test-only and carry no external use grant
    refs = TestOnlyRegistry(json.loads(FIXTURE.read_text())["fields"]).refs_by_role()
    for role in (GSS, NCA):
        row = TestOnlyRegistry(json.loads(FIXTURE.read_text())["fields"]).dereference(refs[role])
        assert row["permission"] == "TEST_ONLY_NO_EXTERNAL_USE_GRANT"
        assert row["fixture_only"] is True and row["issued"] is False


def test_a08_effective_publication_asof_clocks_are_three_distinct_things():
    from dataclasses import replace
    a = _adapter(structural_revision=True)
    base = E.standard_request(label="CURRENT_TEST_CLOCK")

    def serve(valid, asof):
        q = replace(base, clock=E.SelectedWorldClock(mode="AS_OF", valid_at=valid, published_asof=asof))
        s = a.build_snapshot(q)
        acc = a.accept(q, s)
        return a.serve(q, acc, s)

    pre_pub = serve("2027-09-01", "2027-05-31")
    post_pub = serve("2027-09-01", "2027-06-01")
    pre_eff = serve("2026-12-31", "2027-09-01")
    eff_boundary = serve("2027-01-01", "2027-06-01")
    assert pre_pub["structural_values"]["exit_cost"]["value"] == 2
    assert post_pub["structural_values"]["exit_cost"]["value"] == 8
    assert pre_eff["structural_values"]["exit_cost"]["value"] == 2
    assert eff_boundary["structural_values"]["exit_cost"]["value"] == 8
    assert pre_pub["selection"]["valid_at"] == post_pub["selection"]["valid_at"] == "2027-09-01"
    assert pre_pub["selection"]["published_asof"] == "2027-05-31"
    assert pre_pub["native_field_readset"]["as_of"] == "2027-05-31"
    assert post_pub["native_field_readset"]["as_of"] == "2027-06-01"
    v1 = {k: v for k, v in pre_pub["native_field_readset"].items() if k != "as_of"}
    v2 = {k: v for k, v in post_pub["native_field_readset"].items() if k != "as_of"}
    assert v1 == v2
    q_cur = E.standard_request(label="CURRENT_TEST_CLOCK")
    assert q_cur.clock.test_now == q_cur.clock.valid_at == q_cur.clock.published_asof


def test_a09_revocation_dependency_closure_is_directional():
    a = _adapter()
    q, s, acc, r = _serve(a)
    before_steps = r["empirical_steps"]
    hit = a.invalidate("training_access")
    assert r["receipt_hash"] in hit["invalidated_for_fresh_use"]
    after = a.serve(q, acc, s, consumers=[nonparent(a.service, s)["material"]])
    assert after["structural_values"]["training_access"].get("state") in (None, "REVOKED")
    assert after["structural_values"]["training_access"].get("value") in (None, False)
    assert after["empirical_steps"] == before_steps
    assert after["native_field_readset"] == r["native_field_readset"]
    assert after["state"] == "TYPED_PARTIAL_SELECTED_WORLD"
    b = _adapter(extra_field=17)
    _, _, _, rb = _serve(b)
    x = b.invalidate("unrelated_stock")
    assert rb["receipt_hash"] in x["unaffected"]
    assert rb["receipt_hash"] not in x["invalidated_for_fresh_use"]


def test_a10_substitution_and_repooling_are_refused_by_owner_code():
    a1 = _adapter()
    a2 = _adapter(structural_revision=True)
    q1, s1, acc1, r1 = _serve(a1)
    q2, s2, acc2, r2 = _serve(a2)
    with pytest.raises(ValueError) as e1:
        a2.service.catalog.read(s1, "training_fee")
    assert "UNREGISTERED_SELECTED_SNAPSHOT" in str(e1.value)
    with pytest.raises(ValueError) as e2:
        a1.serve(q1, acc2, s1)
    assert "ACCEPTANCE_BINDING_MISMATCH" in str(e2.value)
    with pytest.raises(ValueError) as e3:
        a2.serve(q2, acc2, s1)
    assert "ACCEPTED_SNAPSHOT_SUBSTITUTION" in str(e3.value)
    for flag in ("requested_pooling", "requested_person_exposure", "requested_model_use"):
        with pytest.raises(ValueError):
            E.standard_request(label="CURRENT_TEST_CLOCK", **{flag: True})
    assert r1["state"] == "SELECTED_WORLD_VALUES_SERVED"
    assert r1["operative_N9"] is False and r1["operative_OC05"] is False
    assert r1["pooling"] is False and r1["person_exposure"] is False


def test_a11_cold_replay_digest_two_fresh_processes_match_and_are_not_constant():
    script = (
        "import sys, json; from pathlib import Path;"
        "sys.path.insert(0, {native!r}); sys.path.insert(0, {root!r});"
        "import rawlsing_next; rawlsing_next.__path__.append(str(Path({native!r})/'rawlsing_next'));"
        "src = open({adv!r}).read().split('def test_a01')[0];"
        "exec(src);"
        "q,s,a,r=_serve(_adapter());"
        "print(json.dumps(dict(h=r['receipt_hash'], p=r['receipt_payload_sha256'],"
        "counts=[(x['denominator'],{{c['cell']:c['raw_numerator_support'] for c in x['cells']}}) for x in r['empirical_steps']]), sort_keys=True))"
    )

    def run():
        return subprocess.run([sys.executable, "-c", script.format(
            native=str(NATIVE), root=str(N9J_ROOT), adv=__file__)],
            capture_output=True, text=True, check=True, cwd=str(N9J_ROOT))

    out1, out2 = run(), run()
    assert out1.stdout == out2.stdout and out2.stdout.strip()
    material = json.loads(out1.stdout)
    assert material["h"] and material["p"]
    assert material["counts"] == [[32, {"0": 14, "1": 18}],
                                  [16, {"0": 6, "1": 10}],
                                  [8, {"0": 2, "1": 6}]]
    _, _, _, r_other = _serve(_adapter(empirical_changed=True))
    assert r_other["receipt_hash"] != material["h"]
    assert r_other["receipt_payload_sha256"] != material["p"]


def test_a12_structural_only_leaves_all_empirical_bytes_untouched():
    _, _, _, before = _serve(_adapter())
    _, _, _, after = _serve(_adapter(structural_revision=True))
    assert before["empirical_steps"] == after["empirical_steps"]
    assert before["native_field_readset"] == after["native_field_readset"]
    assert before["structural_values"] != after["structural_values"]
    assert before["selection"] == after["selection"]
    _, _, _, emp = _serve(_adapter(empirical_changed=True))
    assert emp["structural_values"] == before["structural_values"]
    assert emp["selection"] == before["selection"]
    assert emp["native_field_readset"] == before["native_field_readset"]
    assert emp["empirical_steps"] != before["empirical_steps"]


def test_a13_nonparent_and_proposal_are_distinct_implementations_not_clones():
    a = _adapter()
    q = E.standard_request(label="CURRENT_TEST_CLOCK")
    s = a.build_snapshot(q)
    acc = a.accept(q, s)
    non1 = nonparent(a.service, s, budget_tokens=1)["material"]
    prop1 = proposal(a.service, s, PROPOSALS)["material"]
    r1 = a.serve(q, acc, s, consumers=[non1, prop1])
    assert r1["consumers"][1]["consumer_material"]["scenarios"][0]["route"] == "institutional"
    assert non1["consumer"] == "NONPARENT_OPTIONS"
    assert prop1["consumer"] == "CONCEPTION_SCENARIO_PROPOSALS"
    assert set(non1) != set(prop1)
    assert "source_balance_reads" in non1 and "source_balance_reads" not in prop1
    assert "scenarios" in prop1 and "scenarios" not in non1
    assert r1["structural_values"]["training_access"]["value"] is True
    assert non1["structural_routes"]["training"]["state"] == "BLOCKED_BY_MODELED_RULE"
    assert non1["structural_routes"]["exit_constraint"]["state"] == "RESOURCE_CONSTRAINED"
    assert prop1["scenarios"][0]["feasibility"] == "FEASIBLE_MODELED_PREMISE"
    non5 = nonparent(a.service, s, budget_tokens=5)["material"]
    assert non5["structural_routes"]["training"]["state"] == "ELIGIBLE"
    assert non5["structural_routes"]["exit_constraint"]["state"] == "WITHIN_MODELED_BUDGET"
    b = _adapter(structural_revision=True)
    q2 = E.standard_request(label="CURRENT_TEST_CLOCK")
    s2 = b.build_snapshot(q2)
    prop2 = proposal(b.service, s2, PROPOSALS)["material"]
    non2 = nonparent(b.service, s2, budget_tokens=5)["material"]
    assert s2.material["fields"]["training_access"]["value"] is False
    assert s2.material["fields"]["exit_cost"]["value"] == 8
    assert prop2["scenarios"][0]["feasibility"] == "INFEASIBLE_MODELED_PREMISE"
    assert non2["structural_routes"]["training"]["state"] == "BLOCKED_BY_MODELED_RULE"
    assert non2["structural_routes"]["exit_constraint"]["state"] == "RESOURCE_CONSTRAINED"
    assert non2["route_probability"] is None
